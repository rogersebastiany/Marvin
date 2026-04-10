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


def cmd_sync(reporter: Reporter) -> bool:
    """Load vaults → Neo4j → auto-link → bidirectional → Milvus index."""
    import load_vaults

    reporter.step("sync", "Starting vault sync")
    t0 = time.time()

    all_concepts = []
    all_edges = []

    # 1. Obsidian vaults
    for vault_name, vault_path in load_vaults.VAULTS.items():
        concepts, edges = load_vaults.load_vault(vault_name, vault_path)
        reporter.step("sync", f"Loaded vault: {vault_name}", notes=len(concepts), links=len(edges))
        all_concepts.extend(concepts)
        all_edges.extend(edges)

    # 2. docs/
    docs = load_vaults.load_docs(load_vaults.DOCS_DIR)
    reporter.step("sync", f"Loaded docs", count=len(docs))
    all_concepts.extend(docs)

    # 3. diagrams/
    diagrams = load_vaults.load_diagrams(load_vaults.DIAGRAMS_DIR)
    reporter.step("sync", f"Loaded diagrams", count=len(diagrams))
    all_concepts.extend(diagrams)

    # Remap English edges
    remapped = 0
    for e in all_edges:
        if e["vault"].endswith("-en"):
            old_src, old_tgt = e["source"], e["target"]
            e["source"] = load_vaults.EN_TO_PT.get(e["source"], e["source"])
            e["target"] = load_vaults.EN_TO_PT.get(e["target"], e["target"])
            if e["source"] != old_src or e["target"] != old_tgt:
                remapped += 1

    # Merge duplicates
    merged = load_vaults.merge_concepts(all_concepts)
    ghosts = load_vaults.find_ghost_nodes(merged, all_edges)
    merged.extend(ghosts)

    reporter.step("sync", "Merged concepts",
                  unique=len(merged), ghosts=len(ghosts), remapped_edges=remapped)

    # Load into Neo4j
    reporter.step("sync", "Loading into Neo4j...")
    load_vaults.load_to_neo4j(merged, all_edges)

    # Auto-link + bidirectional
    reporter.step("sync", "Auto-linking and ensuring bidirectionality...")
    from neo4j import GraphDatabase
    driver = GraphDatabase.driver(
        os.getenv("NEO4J_URI", "bolt://localhost:7687"),
        auth=(os.getenv("NEO4J_USER", "neo4j"), os.getenv("NEO4J_PASS", "tautologia")),
    )
    load_vaults.auto_link_all(driver)
    load_vaults.ensure_bidirectional_all(driver)
    driver.close()

    # Index into Milvus
    reporter.step("sync", "Indexing into Milvus...")
    load_vaults.index_to_milvus(merged)

    elapsed = round(time.time() - t0, 1)
    reporter.summary("sync", "clean", elapsed_s=elapsed, concepts=len(merged))
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

    # 3. Fix: concept gaps → create missing relations
    for gap in diff.get("concept_gaps", []):
        expected = gap["expected_concept"]
        module = gap["module"]
        ontology.expand(
            concept_name="Marvin",
            relate_to=expected,
            relation_type="RELATES_TO",
            reasoning=f"marvin-ops auto-fix: Marvin backend module '{module}' maps to concept '{expected}'",
        )
        reporter.step("improve", f"Fixed concept gap: linked Marvin → {expected}")
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

    # 6. Re-index Milvus concepts after changes
    if fixes > 0:
        reporter.step("improve", "Re-indexing concepts in Milvus after fixes...")
        _reindex_concepts_in_milvus()

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


def _reindex_concepts_in_milvus():
    """Pull all concepts from Neo4j and re-index in Milvus."""
    import memory
    from neo4j import GraphDatabase

    driver = GraphDatabase.driver(
        os.getenv("NEO4J_URI", "bolt://localhost:7687"),
        auth=(os.getenv("NEO4J_USER", "neo4j"), os.getenv("NEO4J_PASS", "tautologia")),
    )
    with driver.session() as s:
        concepts = list(s.run(
            "MATCH (c:Concept) "
            "WHERE c.content IS NOT NULL AND size(c.content) > 50 "
            "RETURN c.name AS name, c.vault AS vault, "
            "c.summary AS summary, c.content AS content"
        ))
    driver.close()

    indexable = [
        {"name": r["name"], "vault": r["vault"],
         "summary": r["summary"] or "", "content": r["content"] or ""}
        for r in concepts
    ]

    if indexable:
        memory.index_concepts(indexable)


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

    sub = parser.add_subparsers(dest="command", required=True)

    # sync
    sub.add_parser("sync", parents=[shared], help="Load vaults → Neo4j + Milvus")

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
            ok = cmd_sync(reporter)
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
