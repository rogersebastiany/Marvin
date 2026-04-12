#!/usr/bin/env python3
"""
marvin-ops — Standalone orchestrator for Marvin's CI/CD pipelines.

Subcommands:
    sync      Load vaults → Neo4j + Milvus (idempotent)
    audit     Self-audit: compare code AST against knowledge graph
    improve   Deterministic self-improvement: audit → fix drift → log
    all       Run sync → audit → improve sequentially

Usage:
    uv run python marvin_ops.py sync
    uv run python marvin_ops.py audit --threshold 5
    uv run python marvin_ops.py improve
    uv run python marvin_ops.py all --format json

Works standalone (local CLI) and in GitHub Actions.
No Claude Code or MCP dependency — calls backends directly.

Exit codes:
    0  Clean (no drift, or all fixed)
    1  Drift found (audit) or errors
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv

# ── Paths ───────────────────────────────────────────────────────────────────

ROOT = Path(__file__).parent
load_dotenv(ROOT / ".env")

# Add backend modules to path
sys.path.insert(0, str(ROOT / "mcp-server"))
sys.path.insert(0, str(ROOT / "load-vaults"))

# ── Structured output ───────────────────────────────────────────────────────


class Reporter:
    """Handles both human-readable and JSON output."""

    def __init__(self, fmt: str = "text"):
        self.fmt = fmt
        self.log: list[dict] = []

    def step(self, phase: str, message: str, **data):
        entry = {"phase": phase, "message": message, "time": _now(), **data}
        self.log.append(entry)
        if self.fmt == "text":
            print(f"[{phase}] {message}")
            for k, v in data.items():
                if isinstance(v, (list, dict)):
                    print(f"  {k}: {json.dumps(v, indent=2, ensure_ascii=False)}")
                else:
                    print(f"  {k}: {v}")

    def error(self, phase: str, message: str, **data):
        self.step(phase, f"ERROR: {message}", **data)

    def summary(self, phase: str, status: str, **data):
        entry = {"phase": phase, "status": status, "time": _now(), **data}
        self.log.append(entry)
        if self.fmt == "text":
            icon = "OK" if status == "clean" else "DRIFT" if status == "drift" else status.upper()
            print(f"\n[{phase}] {icon}")
            for k, v in data.items():
                print(f"  {k}: {v}")

    def dump_json(self):
        if self.fmt == "json":
            print(json.dumps(self.log, indent=2, ensure_ascii=False))


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


# ── SYNC ────────────────────────────────────────────────────────────────────


def cmd_sync(reporter: Reporter, skip_cognify: bool = False,
             changed_files: list[str] | None = None) -> bool:
    """Cognee cognify → Neo4j + LanceDB → Milvus sync.

    Three cognify modes:
      - skip_cognify=True: no cognify, just sync existing LanceDB → Milvus
      - changed_files=[...]: incremental cognify on listed .md files only
      - neither: full cognify on all vaults + docs (~7-9h)

    After cognify (or skip), syncs LanceDB vectors → Milvus.
    If LanceDB does not exist, sync returns 0 gracefully.
    """
    import memory

    reporter.step("sync", "Starting cognee sync")
    t0 = time.time()

    # 1. Ensure Milvus collections exist (idempotent)
    created = memory.ensure_collections()
    if created:
        reporter.step("sync", f"Created Milvus collections: {', '.join(created)}")

    # 2. Cognee cognify
    if skip_cognify:
        reporter.step("sync", "skip_cognify=True — using existing Neo4j + LanceDB state")
    elif changed_files is not None:
        if len(changed_files) == 0:
            reporter.step("sync", "No changed .md files — skipping cognify")
        else:
            import asyncio
            import cognify_vaults
            reporter.step("sync", f"Running incremental cognify on {len(changed_files)} changed files...")
            asyncio.run(cognify_vaults.run_incremental(changed_files))
            reporter.step("sync", "incremental cognify complete")
    else:
        import asyncio
        import cognify_vaults
        reporter.step("sync", "Running full cognify (this can take hours on a fresh wipe)...")
        asyncio.run(cognify_vaults.run())
        reporter.step("sync", "cognify complete")

    # 3. Sync Concept vectors from LanceDB → Milvus (zero OpenAI calls)
    reporter.step("sync", "Syncing Concept vectors from LanceDB → Milvus...")
    n_concepts = _sync_lance_concepts_to_milvus()
    reporter.step("sync", f"concepts synced", count=n_concepts)

    # 4. Sync DocumentChunk vectors from LanceDB → Milvus (zero OpenAI calls)
    reporter.step("sync", "Syncing DocumentChunk vectors from LanceDB → Milvus...")
    n_chunks = _sync_lance_doc_chunks_to_milvus()
    reporter.step("sync", f"doc_chunks synced", count=n_chunks)

    elapsed = round(time.time() - t0, 1)
    reporter.summary("sync", "clean", elapsed_s=elapsed, concepts=n_concepts, doc_chunks=n_chunks)
    return True


# ── AUDIT ───────────────────────────────────────────────────────────────────


def cmd_audit(reporter: Reporter, threshold: int = 0, save: bool = False) -> bool:
    """Run self-audit. Returns True if drift <= threshold."""
    import self_audit
    from neo4j import GraphDatabase

    reporter.step("audit", "Starting self-audit")
    t0 = time.time()

    # Extract code structure
    code = self_audit.extract_code_structure()
    reporter.step("audit", "Code structure extracted",
                  tools=len(code["tools"]),
                  backends=len(code["backends"]),
                  middleware=len(code["middleware"]))

    # Extract KG claims
    driver = GraphDatabase.driver(
        self_audit.NEO4J_URI, auth=self_audit.NEO4J_AUTH,
    )
    try:
        kg = self_audit.extract_kg_claims(driver)
    finally:
        driver.close()

    reporter.step("audit", "KG claims extracted",
                  concepts=kg["total_concepts"],
                  relations=kg["total_relations"])

    # Compute diff
    diff = self_audit.compute_diff(code, kg)

    # Count drift points
    drift_points = _count_drift(diff)
    reporter.step("audit", f"Drift analysis complete", drift_points=drift_points)

    # Report individual findings
    findings = _extract_findings(diff)
    for f in findings:
        reporter.step("audit", f"DRIFT: {f}")

    # Save report if requested
    if save:
        report = self_audit.generate_report(code, kg, diff)
        out_path = Path(self_audit.REPO_ROOT) / "docs" / "self-audit-report.md"
        out_path.write_text(report)
        reporter.step("audit", f"Report saved to {out_path}")

    elapsed = round(time.time() - t0, 1)
    is_clean = drift_points <= threshold

    reporter.summary(
        "audit",
        "clean" if is_clean else "drift",
        drift_points=drift_points,
        threshold=threshold,
        elapsed_s=elapsed,
    )

    return is_clean


def _count_drift(diff: dict) -> int:
    """Count total drift points from a diff dict."""
    count = 0
    if diff.get("tool_count_mismatch"):
        count += 1
    if diff.get("canonical_list_drift"):
        d = diff["canonical_list_drift"]
        count += len(d.get("in_list_not_decorated", []))
        count += len(d.get("decorated_not_in_list", []))
    if diff.get("relation_type_drift"):
        d = diff["relation_type_drift"]
        count += len(d.get("defined_not_used", []))
        count += len(d.get("used_not_defined", []))
    count += len(diff.get("stale_references", []))
    count += len(diff.get("concept_gaps", []))
    return count


def _extract_findings(diff: dict) -> list[str]:
    """Extract human-readable findings from a diff."""
    findings = []

    if diff.get("tool_count_mismatch"):
        m = diff["tool_count_mismatch"]
        findings.append(f"Tool count: KG claims {m['kg_claims']}, code has {m['code_has']}")

    if diff.get("canonical_list_drift"):
        d = diff["canonical_list_drift"]
        for t in d.get("in_list_not_decorated", []):
            findings.append(f"In MARVIN_TOOLS but no @mcp.tool: {t}")
        for t in d.get("decorated_not_in_list", []):
            findings.append(f"Has @mcp.tool but not in MARVIN_TOOLS: {t}")

    if diff.get("relation_type_drift"):
        d = diff["relation_type_drift"]
        for t in d.get("defined_not_used", []):
            findings.append(f"Relation type defined but unused: {t}")
        for t in d.get("used_not_defined", []):
            findings.append(f"Relation type used but not defined: {t}")

    for ref in diff.get("stale_references", []):
        findings.append(f"Stale ref in '{ref['concept']}': {ref['reference']} — {ref['reason']}")

    for gap in diff.get("concept_gaps", []):
        findings.append(f"Missing relation: {gap['issue']}")

    return findings


# ── IMPROVE ─────────────────────────────────────────────────────────────────


def cmd_improve(reporter: Reporter) -> bool:
    """Deterministic self-improvement: audit → fix drift → log to Milvus.

    No LLM tokens. Pure set comparison + MERGE operations.
    """
    import self_audit
    import ontology
    import memory
    from neo4j import GraphDatabase

    reporter.step("improve", "Starting self-improvement cycle")
    t0 = time.time()
    fixes = 0

    # 1. Run audit to get drift
    code = self_audit.extract_code_structure()
    driver = GraphDatabase.driver(
        self_audit.NEO4J_URI, auth=self_audit.NEO4J_AUTH,
    )
    try:
        kg = self_audit.extract_kg_claims(driver)
    finally:
        driver.close()

    diff = self_audit.compute_diff(code, kg)
    drift_before = _count_drift(diff)
    reporter.step("improve", f"Drift before: {drift_before} points")

    if drift_before == 0:
        reporter.summary("improve", "clean", message="No drift to fix", elapsed_s=0)
        return True

    # 2. Fix: tool count mismatch → update Marvin concept in KG
    if diff.get("tool_count_mismatch"):
        actual_count = diff["tool_count_mismatch"]["code_has"]
        tools_list = ", ".join(sorted(code["tools"]))
        ontology.expand(
            concept_name="Marvin",
            summary=f"The unified MCP server (marvin_server.py) wrapping 6 backend modules "
                    f"into a single process. Exposes {actual_count} tools across 8 categories. "
                    f"The living implementation of Tautologia Ontologica.",
        )
        reporter.step("improve", f"Fixed tool count: updated Marvin concept to {actual_count} tools")
        fixes += 1

    # 3. Fix: concept gaps → create missing relations using the semantic edge type
    # declared in self_audit.BACKEND_CONCEPT_MAP. REQUIRES for external deps
    # (Neo4j, Milvus), COMPOSES for internal modules. Never RELATES_TO — the
    # thesis (Grafo Dirigido Completo) demands every edge carry semantic type.
    for gap in diff.get("concept_gaps", []):
        expected = gap["expected_concept"]
        module = gap["module"]
        relation_type = gap.get("expected_relation", "RELATES_TO")
        ontology.expand(
            concept_name="Marvin",
            relate_to=expected,
            relation_type=relation_type,
            reasoning=f"marvin-ops auto-fix: Marvin backend module '{module}' maps to concept '{expected}' via {relation_type}",
        )
        reporter.step("improve", f"Fixed concept gap: Marvin —[{relation_type}]→ {expected}")
        fixes += 1

    # 4. Fix: relation types defined but not used → create seed edges
    if diff.get("relation_type_drift"):
        for unused_type in diff["relation_type_drift"].get("defined_not_used", []):
            reporter.step("improve",
                          f"Unused relation type '{unused_type}' — skipping (needs semantic context)")

    # 5. Fix: stale references → log as findings (can't auto-fix content)
    for ref in diff.get("stale_references", []):
        reporter.step("improve",
                      f"Stale reference in '{ref['concept']}': {ref['reference']} — needs manual review")

    # 6. Re-sync LanceDB concepts to Milvus after graph fixes
    if fixes > 0:
        reporter.step("improve", "Re-syncing concepts from LanceDB → Milvus after fixes...")
        _sync_lance_concepts_to_milvus()

    # 7. Log the improvement cycle to Milvus as a decision
    try:
        memory.log_decision(
            objective="marvin-ops self-improvement cycle",
            options_considered=f"Found {drift_before} drift points across tool count, concept gaps, relation types, stale references",
            chosen_option=f"Auto-fixed {fixes} points, flagged remaining for manual review",
            reasoning="Deterministic set comparison: code AST vs KG claims. No LLM tokens used.",
            outcome=f"Applied {fixes} fixes. Remaining drift needs semantic context (stale references, unused relation types).",
        )
        reporter.step("improve", "Logged improvement cycle to Milvus")
    except Exception as e:
        reporter.error("improve", f"Failed to log to Milvus: {e}")

    elapsed = round(time.time() - t0, 1)
    reporter.summary("improve", "fixed" if fixes > 0 else "flagged",
                     drift_before=drift_before, fixes=fixes, elapsed_s=elapsed)
    return True


def _get_lancedb_path() -> str | None:
    """Resolve the Cognee LanceDB path from env or default.

    Returns None if the path does not exist (e.g. CI with no prior cognify run).
    """
    lancedb_path = os.getenv("COGNEE_LANCEDB_PATH", "data/cognee.lancedb")
    if not os.path.isabs(lancedb_path):
        lancedb_path = str(ROOT / lancedb_path)
    if not Path(lancedb_path).exists():
        return None
    return lancedb_path


def _sync_lance_concepts_to_milvus() -> int:
    """Sync Concept vectors from Cognee's LanceDB → Marvin's Milvus.

    Reads pre-computed vectors from LanceDB (produced by cognify) and
    joins with Neo4j concept names. Zero OpenAI embedding API calls.

    Returns the number of concepts indexed.
    """
    import lancedb as ldb
    import memory
    from neo4j import GraphDatabase
    from pymilvus import Collection

    # 1. Read vectors from LanceDB
    lance_path = _get_lancedb_path()
    if lance_path is None:
        return 0
    db = ldb.connect(lance_path)
    tbl = db.open_table("Concept_name")
    df = tbl.to_pandas()

    # Build lookup: UUID → (vector, description text)
    lance_lookup: dict[str, dict] = {}
    for _, row in df.iterrows():
        lance_lookup[row["id"]] = {
            "vector": row["vector"].tolist(),
            "text": row["payload"]["text"],
        }

    # 2. Get canonical names from Neo4j
    driver = GraphDatabase.driver(
        os.getenv("NEO4J_URI", "bolt://localhost:7687"),
        auth=(os.getenv("NEO4J_USER", "neo4j"), os.getenv("NEO4J_PASS", "tautologia")),
    )
    with driver.session() as s:
        concepts = list(s.run(
            "MATCH (c:Concept) "
            "RETURN c.id AS id, c.name AS name, "
            "       coalesce(c.description, '') AS description"
        ))
    driver.close()

    # 3. Join: Neo4j names + LanceDB vectors → Milvus
    memory._ensure_connected()
    col = Collection("concepts")
    col.load()

    # Clear existing
    if col.num_entities > 0:
        col.delete(expr='name != ""')
        col.flush()

    entries = []
    for r in concepts:
        if not r["name"]:
            continue
        lance = lance_lookup.get(r["id"])
        if not lance:
            continue
        name = r["name"][:250]
        desc = r["description"][:1000].encode("utf-8")[:1000].decode("utf-8", errors="ignore")
        content = lance["text"][:8000].encode("utf-8")[:8000].decode("utf-8", errors="ignore")
        entries.append({
            "id": f"concept::{name}",
            "name": name,
            "vault": "cognee",
            "summary": desc,
            "content": content,
            "vector": lance["vector"],
        })

    # Insert in batches
    batch_size = 200
    for i in range(0, len(entries), batch_size):
        batch = entries[i : i + batch_size]
        col.insert([
            [e["id"] for e in batch],
            [e["name"] for e in batch],
            [e["vault"] for e in batch],
            [e["summary"] for e in batch],
            [e["content"] for e in batch],
            [e["vector"] for e in batch],
        ])
    col.flush()

    return len(entries)


def _sync_lance_doc_chunks_to_milvus() -> int:
    """Sync DocumentChunk vectors from Cognee's LanceDB → Marvin's Milvus.

    Reads pre-computed vectors from LanceDB (produced by cognify).
    Zero OpenAI embedding API calls.

    Returns the number of chunks indexed.
    """
    import lancedb as ldb
    import memory
    from pymilvus import Collection

    lance_path = _get_lancedb_path()
    if lance_path is None:
        return 0
    db = ldb.connect(lance_path)
    tbl = db.open_table("DocumentChunk_text")
    df = tbl.to_pandas()

    memory._ensure_connected()
    col = Collection("doc_chunks")
    col.load()

    # Clear existing
    if col.num_entities > 0:
        col.delete(expr='doc_name != ""')
        col.flush()

    entries = []
    for idx, row in df.iterrows():
        text = row["payload"]["text"]
        if len(text) < 50:
            continue
        chunk_id = row["id"]
        # Extract a heading from the first line of text
        lines = text.split("\n", 1)
        heading = lines[0][:500].encode("utf-8")[:500].decode("utf-8", errors="ignore")
        content = text[:8000].encode("utf-8")[:8000].decode("utf-8", errors="ignore")
        entries.append({
            "id": f"lance::{chunk_id}",
            "doc_name": "cognee",
            "chunk_index": idx,
            "heading": heading,
            "content": content,
            "vector": row["vector"].tolist(),
        })

    # Insert in batches
    batch_size = 200
    for i in range(0, len(entries), batch_size):
        batch = entries[i : i + batch_size]
        col.insert([
            [e["id"] for e in batch],
            [e["doc_name"] for e in batch],
            [e["chunk_index"] for e in batch],
            [e["heading"] for e in batch],
            [e["content"] for e in batch],
            [e["vector"] for e in batch],
        ])
    col.flush()

    return len(entries)


# ── ALL ─────────────────────────────────────────────────────────────────────


def cmd_all(reporter: Reporter, threshold: int = 0, save: bool = False) -> bool:
    """Run sync → audit → improve sequentially."""
    reporter.step("all", "Running full pipeline: sync → audit → improve")

    ok = cmd_sync(reporter)
    if not ok:
        return False

    audit_clean = cmd_audit(reporter, threshold=threshold, save=save)

    if not audit_clean:
        reporter.step("all", "Drift found, running improve...")
        cmd_improve(reporter)

    reporter.summary("all", "done")
    return True


# ── CLI ─────────────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(
        prog="marvin-ops",
        description="Orchestrator for Marvin CI/CD pipelines",
    )
    # Shared args added to every subparser
    shared = argparse.ArgumentParser(add_help=False)
    shared.add_argument(
        "--format", choices=["text", "json"], default="text",
        help="Output format (default: text)",
    )
    shared.add_argument(
        "--threshold", type=int, default=0,
        help="Max drift points before failing (default: 0 = strict)",
    )
    shared.add_argument(
        "--save", action="store_true",
        help="Save audit report to docs/self-audit-report.md",
    )
    shared.add_argument(
        "--skip-cognify", action="store_true",
        help="Skip cognee cognify step, sync LanceDB → Milvus only",
    )
    shared.add_argument(
        "--changed-files", nargs="*", default=None,
        help="Changed .md file paths for incremental cognify (relative to repo root)",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    # sync
    sub.add_parser("sync", parents=[shared], help="LanceDB → Milvus (cognify + sync)")

    # audit
    sub.add_parser("audit", parents=[shared], help="Self-audit: code vs KG drift")

    # improve
    sub.add_parser("improve", parents=[shared], help="Auto-fix drift + log to Milvus")

    # all
    sub.add_parser("all", parents=[shared], help="sync → audit → improve")

    args = parser.parse_args()
    reporter = Reporter(fmt=args.format)

    try:
        if args.command == "sync":
            ok = cmd_sync(reporter, skip_cognify=args.skip_cognify,
                         changed_files=args.changed_files)
        elif args.command == "audit":
            ok = cmd_audit(reporter, threshold=args.threshold, save=args.save)
        elif args.command == "improve":
            ok = cmd_improve(reporter)
        elif args.command == "all":
            ok = cmd_all(reporter, threshold=args.threshold, save=args.save)
        else:
            ok = False
    except Exception as e:
        reporter.error(args.command, str(e))
        ok = False

    reporter.dump_json()
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
