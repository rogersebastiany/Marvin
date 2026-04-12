"""
Ops backend — vault sync, self-audit, and self-improvement.

Migrated from marvin_ops.py + self_audit.py into an MCP-callable backend.
No CLI, no Reporter — returns structured dicts. The MCP tool layer
handles formatting.

Three operations:
  - sync: cognify vaults → Neo4j + LanceDB → Milvus (zero OpenAI for vector transfer)
  - audit: AST vs KG diff — what the code IS vs what the ontology CLAIMS
  - self_improve: audit → fix drift → log to Milvus (deterministic, zero LLM)
"""

import ast
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv

REPO_ROOT = Path(__file__).parent.parent.parent
MCP_SERVER = Path(__file__).parent.parent

load_dotenv(REPO_ROOT / ".env")

# Add load-vaults to path for cognify imports
sys.path.insert(0, str(REPO_ROOT / "load-vaults"))


# ═══════════════════════════════════════════════════════════════════════════════
# SYNC — cognify + LanceDB → Milvus
# ═══════════════════════════════════════════════════════════════════════════════


def _get_lancedb_path() -> str | None:
    """Resolve the Cognee LanceDB path. Returns None if it doesn't exist."""
    lancedb_path = os.getenv("COGNEE_LANCEDB_PATH", "data/cognee.lancedb")
    if not os.path.isabs(lancedb_path):
        lancedb_path = str(REPO_ROOT / lancedb_path)
    if not Path(lancedb_path).exists():
        return None
    return lancedb_path


def _sync_lance_concepts_to_milvus() -> int:
    """Sync Concept vectors from Cognee's LanceDB → Marvin's Milvus.

    Reads pre-computed vectors from LanceDB (produced by cognify) and
    joins with Neo4j concept names. Zero OpenAI embedding API calls.
    """
    import lancedb as ldb
    from . import memory
    from neo4j import GraphDatabase
    from pymilvus import Collection

    lance_path = _get_lancedb_path()
    if lance_path is None:
        return 0
    db = ldb.connect(lance_path)
    tbl = db.open_table("Concept_name")
    df = tbl.to_pandas()

    lance_lookup: dict[str, dict] = {}
    for _, row in df.iterrows():
        lance_lookup[row["id"]] = {
            "vector": row["vector"].tolist(),
            "text": row["payload"]["text"],
        }

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

    memory._ensure_connected()
    col = Collection("concepts")
    col.load()

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

    Zero OpenAI embedding API calls.
    """
    import lancedb as ldb
    from . import memory
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

    if col.num_entities > 0:
        col.delete(expr='doc_name != ""')
        col.flush()

    entries = []
    for idx, row in df.iterrows():
        text = row["payload"]["text"]
        if len(text) < 50:
            continue
        chunk_id = row["id"]
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


def sync(skip_cognify: bool = False, changed_files: list[str] | None = None) -> dict:
    """Cognify vaults → Neo4j + LanceDB → Milvus.

    Three modes:
      - skip_cognify=True: sync existing LanceDB → Milvus only
      - changed_files=[...]: incremental cognify on listed .md files
      - neither: full cognify (~7-9h on fresh wipe)

    Returns: {"concepts": int, "doc_chunks": int, "elapsed_s": float, "cognify_mode": str}
    """
    from . import memory

    t0 = time.time()

    memory.ensure_collections()

    if skip_cognify:
        cognify_mode = "skipped"
    elif changed_files is not None:
        if len(changed_files) == 0:
            cognify_mode = "skipped (no changed files)"
        else:
            import asyncio
            import cognify_vaults
            asyncio.run(cognify_vaults.run_incremental(changed_files))
            cognify_mode = f"incremental ({len(changed_files)} files)"
    else:
        import asyncio
        import cognify_vaults
        asyncio.run(cognify_vaults.run())
        cognify_mode = "full"

    n_concepts = _sync_lance_concepts_to_milvus()
    n_chunks = _sync_lance_doc_chunks_to_milvus()

    return {
        "concepts": n_concepts,
        "doc_chunks": n_chunks,
        "cognify_mode": cognify_mode,
        "elapsed_s": round(time.time() - t0, 1),
    }


# ═══════════════════════════════════════════════════════════════════════════════
# AUDIT — AST vs KG diff
# ═══════════════════════════════════════════════════════════════════════════════

SOURCE_FILES = [
    "marvin_server.py",
    "backends/ontology.py",
    "backends/memory.py",
    "backends/docs_backend.py",
    "backends/web_to_docs_backend.py",
    "backends/prompt_engineer_backend.py",
    "backends/system_design_backend.py",
    "backends/code_improvement_backend.py",
    "backends/orchestrator_backend.py",
    "backends/ops_backend.py",
]

BACKEND_CONCEPT_MAP = {
    "ontology": ("Neo4j", "REQUIRES"),
    "memory": ("Milvus", "REQUIRES"),
    "docs_backend": ("docs-server", "COMPOSES"),
    "web_to_docs_backend": ("web-to-docs", "COMPOSES"),
    "prompt_engineer_backend": ("prompt-engineer", "COMPOSES"),
    "system_design_backend": ("system-design", "COMPOSES"),
}


def _is_mcp_tool_decorator(node: ast.expr) -> bool:
    if isinstance(node, ast.Call):
        return _is_mcp_tool_decorator(node.func)
    if isinstance(node, ast.Attribute):
        return (
            isinstance(node.value, ast.Name)
            and node.value.id == "mcp"
            and node.attr == "tool"
        )
    return False


def _extract_set_or_list(node: ast.expr) -> list[str]:
    elements = []
    if isinstance(node, (ast.List, ast.Set)):
        for elt in node.elts:
            if isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                elements.append(elt.value)
    elif isinstance(node, ast.Call):
        if node.args:
            return _extract_set_or_list(node.args[0])
    return sorted(elements)


def extract_code_structure() -> dict:
    """Parse all source files and extract structural information."""
    structure = {
        "tools": [],
        "backends": {},
        "constants": {},
        "middleware": [],
        "imports": {},
    }

    for filename in SOURCE_FILES:
        filepath = MCP_SERVER / filename
        if not filepath.exists():
            continue

        source = filepath.read_text()
        tree = ast.parse(source, filename=filename)
        module_name = Path(filename).stem

        public_funcs = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and not node.name.startswith("_"):
                public_funcs.append(node.name)
        structure["backends"][module_name] = public_funcs

        if filename == "marvin_server.py":
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    for decorator in node.decorator_list:
                        if _is_mcp_tool_decorator(decorator):
                            structure["tools"].append(node.name)

            for node in ast.iter_child_nodes(tree):
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name) and target.id in (
                            "MARVIN_TOOLS",
                            "MILVUS_TOOLS", "NEO4J_READ_TOOLS", "WRITE_TOOLS",
                            "GATED_TOOLS", "OVERVIEW_TOOLS",
                        ):
                            structure["constants"][target.id] = _extract_set_or_list(node.value)

                if isinstance(node, ast.ClassDef):
                    for base in node.bases:
                        if isinstance(base, ast.Name) and base.id == "Middleware":
                            structure["middleware"].append(node.name)

        module_imports = []
        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    module_imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    module_imports.append(node.module)
        structure["imports"][module_name] = module_imports

    return structure


def extract_kg_claims() -> dict:
    """Query Neo4j for what the ontology claims about Marvin."""
    from neo4j import GraphDatabase

    driver = GraphDatabase.driver(
        os.getenv("NEO4J_URI", "bolt://localhost:7687"),
        auth=(os.getenv("NEO4J_USER", "neo4j"), os.getenv("NEO4J_PASS", "tautologia")),
    )

    claims = {
        "marvin_concept": None,
        "marvin_relations": [],
        "relation_types_in_kg": [],
        "total_concepts": 0,
        "total_relations": 0,
    }

    try:
        with driver.session() as s:
            result = s.run(
                "MATCH (c:Concept {name: 'Marvin'}) "
                "RETURN c.summary AS summary, c.content AS content, c.vault AS vault"
            )
            record = result.single()
            if record:
                claims["marvin_concept"] = dict(record)

            result = s.run(
                "MATCH (c:Concept {name: 'Marvin'})-[r]->(t:Concept) "
                "RETURN type(r) AS rel_type, t.name AS target"
            )
            claims["marvin_relations"] = [dict(r) for r in result]

            result = s.run(
                "MATCH (:Concept)-[r]->(:Concept) "
                "RETURN DISTINCT type(r) AS rel_type, count(*) AS count "
                "ORDER BY count DESC"
            )
            claims["relation_types_in_kg"] = [(r["rel_type"], r["count"]) for r in result]

            result = s.run("MATCH (c:Concept) RETURN count(c) AS n")
            claims["total_concepts"] = result.single()["n"]

            result = s.run("MATCH (:Concept)-[r]->(:Concept) RETURN count(r) AS n")
            claims["total_relations"] = result.single()["n"]
    finally:
        driver.close()

    return claims


def compute_diff(code: dict, kg: dict) -> dict:
    """Compare code structure against KG claims. Pure set operations."""
    diff = {
        "tool_count_mismatch": None,
        "canonical_list_drift": None,
        "relation_type_drift": None,
        "concept_gaps": [],
        "middleware_gaps": [],
    }

    code_tools = set(code["tools"])

    # Tool count in KG content vs actual
    marvin_content = (kg["marvin_concept"] or {}).get("content", "")
    tool_count_match = re.search(r"(\d+)\s+(?:tautological\s+)?tools", marvin_content)
    if tool_count_match:
        kg_tool_count = int(tool_count_match.group(1))
        if kg_tool_count != len(code_tools):
            diff["tool_count_mismatch"] = {
                "kg_claims": kg_tool_count,
                "code_has": len(code_tools),
            }

    # MARVIN_TOOLS list vs @mcp.tool decorators
    canonical = set(code["constants"].get("MARVIN_TOOLS", []))
    if canonical and canonical != code_tools:
        diff["canonical_list_drift"] = {
            "in_list_not_decorated": sorted(canonical - code_tools),
            "decorated_not_in_list": sorted(code_tools - canonical),
        }

    # Middleware tier coverage
    milvus = set(code["constants"].get("MILVUS_TOOLS", []))
    overview = set(code["constants"].get("OVERVIEW_TOOLS", []))
    neo4j_read = set(code["constants"].get("NEO4J_READ_TOOLS", []))
    write = set(code["constants"].get("WRITE_TOOLS", []))
    classified = milvus | overview | neo4j_read | write
    always_allowed = code_tools - classified
    if always_allowed:
        diff["middleware_gaps"] = sorted(always_allowed)

    # Relation types: code vs KG
    rel_types_path = MCP_SERVER / "relation_types.json"
    if rel_types_path.exists():
        code_rel_types = set(json.loads(rel_types_path.read_text()).keys())
        kg_rel_types = {rt for rt, _ in kg["relation_types_in_kg"]}
        in_code_not_kg = code_rel_types - kg_rel_types
        in_kg_not_code = kg_rel_types - code_rel_types
        if in_code_not_kg or in_kg_not_code:
            diff["relation_type_drift"] = {
                "defined_not_used": sorted(in_code_not_kg),
                "used_not_defined": sorted(in_kg_not_code),
            }

    # Concept gaps: expected backend relations
    all_related = {r["target"] for r in kg["marvin_relations"]}
    for module, (concept_name, relation_type) in BACKEND_CONCEPT_MAP.items():
        if concept_name not in all_related:
            diff["concept_gaps"].append({
                "module": module,
                "expected_concept": concept_name,
                "expected_relation": relation_type,
            })

    return diff


def _count_drift(diff: dict) -> int:
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
    count += len(diff.get("concept_gaps", []))
    return count


def audit() -> dict:
    """Run self-audit: code AST vs KG claims.

    Returns: {"drift_points": int, "findings": [...], "code_summary": {...}, "kg_summary": {...}}
    """
    t0 = time.time()

    code = extract_code_structure()
    kg = extract_kg_claims()
    diff = compute_diff(code, kg)
    drift_points = _count_drift(diff)

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
    for gap in diff.get("concept_gaps", []):
        findings.append(f"Missing relation: Marvin → {gap['expected_concept']} ({gap['expected_relation']})")

    return {
        "drift_points": drift_points,
        "findings": findings,
        "diff": diff,
        "code_summary": {
            "tools": len(code["tools"]),
            "backends": len(code["backends"]),
            "middleware": code["middleware"],
        },
        "kg_summary": {
            "concepts": kg["total_concepts"],
            "relations": kg["total_relations"],
            "relation_types": len(kg["relation_types_in_kg"]),
        },
        "elapsed_s": round(time.time() - t0, 1),
    }


# ═══════════════════════════════════════════════════════════════════════════════
# SELF-IMPROVE — audit → fix drift → log
# ═══════════════════════════════════════════════════════════════════════════════


def self_improve() -> dict:
    """Deterministic self-improvement: audit → fix drift → log to Milvus.

    Zero LLM tokens. Pure set comparison + MERGE operations.

    Returns: {"drift_before": int, "fixes": int, "actions": [...], "elapsed_s": float}
    """
    from . import ontology
    from . import memory

    t0 = time.time()
    actions = []

    code = extract_code_structure()
    kg = extract_kg_claims()
    diff = compute_diff(code, kg)
    drift_before = _count_drift(diff)

    if drift_before == 0:
        return {"drift_before": 0, "fixes": 0, "actions": ["No drift"], "elapsed_s": 0}

    fixes = 0

    # Fix tool count
    if diff.get("tool_count_mismatch"):
        actual_count = diff["tool_count_mismatch"]["code_has"]
        ontology.expand(
            concept_name="Marvin",
            summary=f"The unified MCP server (marvin_server.py) wrapping backend modules "
                    f"into a single process. Exposes {actual_count} tools. "
                    f"The living implementation of Tautologia Ontologica.",
        )
        actions.append(f"Updated Marvin concept to {actual_count} tools")
        fixes += 1

    # Fix concept gaps
    for gap in diff.get("concept_gaps", []):
        ontology.expand(
            concept_name="Marvin",
            relate_to=gap["expected_concept"],
            relation_type=gap["expected_relation"],
            reasoning=f"ops auto-fix: backend '{gap['module']}' maps to '{gap['expected_concept']}'",
        )
        actions.append(f"Marvin —[{gap['expected_relation']}]→ {gap['expected_concept']}")
        fixes += 1

    # Re-sync after fixes
    if fixes > 0:
        _sync_lance_concepts_to_milvus()
        actions.append("Re-synced concepts LanceDB → Milvus")

    # Log to Milvus
    try:
        memory.log_decision(
            objective="ops self-improvement cycle",
            options_considered=f"Found {drift_before} drift points",
            chosen_option=f"Auto-fixed {fixes} points",
            reasoning="Deterministic set comparison: code AST vs KG claims. Zero LLM tokens.",
            outcome=f"Applied {fixes} fixes.",
        )
        actions.append("Logged to Milvus decisions")
    except Exception as e:
        actions.append(f"Failed to log: {e}")

    return {
        "drift_before": drift_before,
        "fixes": fixes,
        "actions": actions,
        "elapsed_s": round(time.time() - t0, 1),
    }
