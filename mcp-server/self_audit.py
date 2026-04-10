"""
self_audit.py — Marvin Self-Audit Tool

Pure Python script that compares Marvin's source code against its own
knowledge graph representation. Produces a markdown report identifying
drift between what the code IS and what the ontology CLAIMS it is.

Designed to run in CI (GitHub Actions) on push or schedule.
Zero LLM tokens — deterministic set comparison.

Usage:
    uv run python self_audit.py              # print report to stdout
    uv run python self_audit.py --save       # also save to docs/self-audit-report.md
"""

import ast
import argparse
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from neo4j import GraphDatabase

# ─── Config ───────────────────────────────────────────────────────────────────

REPO_ROOT = Path(__file__).parent
load_dotenv(REPO_ROOT.parent / ".env")

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_AUTH = (os.getenv("NEO4J_USER", "neo4j"), os.getenv("NEO4J_PASS", "tautologia"))

SOURCE_FILES = [
    "marvin_server.py",
    "ontology.py",
    "memory.py",
    "docs_backend.py",
    "web_to_docs_backend.py",
    "prompt_engineer_backend.py",
    "system_design_backend.py",
]

# Concepts in the KG that directly describe Marvin's implementation
MARVIN_IMPLEMENTATION_CONCEPTS = [
    "Marvin",
    "Catálogo de Tools",
    "Loop de Auto-Melhoria",
    "Self-Referential Proof",
    "Enforcement Arquitetural",
    "Feedback Loop Determinístico",
    "Anti-Alucinação",
    "Tool Tautológica",
    "Tool como Bias",
    "Ontologia como Código",
    "Contexto Programático",
    "RAG Implícito",
    "ReAct na POC",
    "Agente na POC",
]


# ─── Code Extraction (AST) ───────────────────────────────────────────────────


def extract_code_structure() -> dict:
    """Parse all source files and extract structural information."""
    structure = {
        "tools": [],            # MCP tool names from @mcp.tool decorators
        "backends": {},         # module -> list of public functions
        "constants": {},        # important constants and their values
        "middleware": [],       # middleware classes
        "imports": {},          # module -> list of imports
    }

    for filename in SOURCE_FILES:
        filepath = REPO_ROOT / filename
        if not filepath.exists():
            continue

        source = filepath.read_text()
        tree = ast.parse(source, filename=filename)
        module_name = filename.replace(".py", "")

        # Extract public functions
        public_funcs = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and not node.name.startswith("_"):
                public_funcs.append(node.name)
        structure["backends"][module_name] = public_funcs

        # Extract MCP tools (functions decorated with @mcp.tool)
        if filename == "marvin_server.py":
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    for decorator in node.decorator_list:
                        if _is_mcp_tool_decorator(decorator):
                            structure["tools"].append(node.name)

            # Extract key constants
            for node in ast.iter_child_nodes(tree):
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name) and target.id in (
                            "MARVIN_TOOLS", "RETRIEVAL_TOOLS", "GUARDED_TOOLS",
                        ):
                            structure["constants"][target.id] = _extract_set_or_list(node.value)

                # Also handle classes (middleware)
                if isinstance(node, ast.ClassDef):
                    for base in node.bases:
                        if isinstance(base, ast.Name) and base.id == "Middleware":
                            structure["middleware"].append(node.name)

        # Extract imports
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


def _is_mcp_tool_decorator(node: ast.expr) -> bool:
    """Check if a decorator is @mcp.tool(...)."""
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
    """Extract string elements from a list, set, or frozenset literal."""
    elements = []
    if isinstance(node, (ast.List, ast.Set)):
        for elt in node.elts:
            if isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                elements.append(elt.value)
    elif isinstance(node, ast.Call):
        # frozenset({...})
        if node.args:
            return _extract_set_or_list(node.args[0])
    return sorted(elements)


# ─── Knowledge Graph Extraction ──────────────────────────────────────────────


def extract_kg_claims(driver) -> dict:
    """Query Neo4j for what the ontology claims about Marvin."""
    claims = {
        "marvin_concept": None,
        "marvin_relations": [],
        "implementation_concepts": {},
        "relation_types_in_kg": [],
        "tool_references": set(),       # tool names mentioned in concept content
        "backend_references": set(),    # backend/module names mentioned
        "total_concepts": 0,
        "total_relations": 0,
    }

    with driver.session() as s:
        # Get Marvin concept
        result = s.run(
            "MATCH (c:Concept {name: 'Marvin'}) "
            "RETURN c.summary AS summary, c.content AS content, c.vault AS vault"
        )
        record = result.single()
        if record:
            claims["marvin_concept"] = dict(record)

        # Get Marvin's relations (both directions)
        result = s.run(
            "MATCH (c:Concept {name: 'Marvin'})-[r]->(t:Concept) "
            "RETURN type(r) AS rel_type, t.name AS target, 'outgoing' AS direction"
        )
        claims["marvin_relations"] = [dict(r) for r in result]

        result = s.run(
            "MATCH (c:Concept {name: 'Marvin'})<-[r]-(t:Concept) "
            "RETURN type(r) AS rel_type, t.name AS target, 'incoming' AS direction"
        )
        claims["marvin_incoming"] = [dict(r) for r in result]

        # Get implementation concepts
        for name in MARVIN_IMPLEMENTATION_CONCEPTS:
            result = s.run(
                "MATCH (c:Concept {name: $name}) "
                "RETURN c.name AS name, c.summary AS summary, c.content AS content",
                name=name,
            )
            record = result.single()
            if record:
                claims["implementation_concepts"][name] = dict(record)

        # Get all relation types actually used
        result = s.run(
            "MATCH ()-[r]->() RETURN DISTINCT type(r) AS rel_type, count(*) AS count "
            "ORDER BY count DESC"
        )
        claims["relation_types_in_kg"] = [(r["rel_type"], r["count"]) for r in result]

        # Get totals
        result = s.run("MATCH (c:Concept) RETURN count(c) AS n")
        claims["total_concepts"] = result.single()["n"]

        result = s.run("MATCH ()-[r]->() RETURN count(r) AS n")
        claims["total_relations"] = result.single()["n"]

        # Scan implementation concept content for tool/backend references
        for name, data in claims["implementation_concepts"].items():
            content = (data.get("content") or "") + " " + (data.get("summary") or "")
            # Look for tool-like references (backtick-quoted or plain function names)
            import re
            for match in re.finditer(r"`(\w+)`|(\w+_\w+)", content):
                ref = match.group(1) or match.group(2)
                if ref:
                    claims["tool_references"].add(ref)
                    claims["backend_references"].add(ref)

    return claims


# ─── Diff Engine ──────────────────────────────────────────────────────────────


def compute_diff(code: dict, kg: dict) -> dict:
    """Compare code structure against KG claims. Pure set operations."""
    diff = {
        "tool_count_mismatch": None,
        "tools_in_code_not_kg": [],
        "tools_in_kg_not_code": [],
        "canonical_list_drift": [],
        "middleware_gaps": [],
        "relation_type_drift": [],
        "stale_references": [],
        "concept_gaps": [],
    }

    # 1. Tool count: KG says "27 tools" but code has N
    code_tools = set(code["tools"])
    marvin_content = (kg["marvin_concept"] or {}).get("content", "")
    import re
    tool_count_match = re.search(r"(\d+)\s+(?:tautological\s+)?tools", marvin_content)
    if tool_count_match:
        kg_tool_count = int(tool_count_match.group(1))
        if kg_tool_count != len(code_tools):
            diff["tool_count_mismatch"] = {
                "kg_claims": kg_tool_count,
                "code_has": len(code_tools),
            }

    # 2. MARVIN_TOOLS canonical list vs actual @mcp.tool decorators
    canonical = set(code["constants"].get("MARVIN_TOOLS", []))
    if canonical and canonical != code_tools:
        diff["canonical_list_drift"] = {
            "in_list_not_decorated": sorted(canonical - code_tools),
            "decorated_not_in_list": sorted(code_tools - canonical),
        }

    # 3. RETRIEVAL_TOOLS + GUARDED_TOOLS coverage
    retrieval = set(code["constants"].get("RETRIEVAL_TOOLS", []))
    guarded = set(code["constants"].get("GUARDED_TOOLS", []))
    unclassified = code_tools - retrieval - guarded
    # Some tools are intentionally unclassified (always-allowed), but flag for review
    always_allowed = code_tools - retrieval - guarded
    if always_allowed:
        diff["middleware_gaps"] = sorted(always_allowed)

    # 4. Relation types: code RELATION_TYPES vs what KG actually uses
    # Parse ontology.py for RELATION_TYPES
    ontology_path = REPO_ROOT / "ontology.py"
    if ontology_path.exists():
        tree = ast.parse(ontology_path.read_text())
        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == "RELATION_TYPES":
                        code_rel_types = set(_extract_set_or_list(node.value))
                        kg_rel_types = {rt for rt, _ in kg["relation_types_in_kg"]}
                        in_code_not_kg = code_rel_types - kg_rel_types
                        in_kg_not_code = kg_rel_types - code_rel_types
                        if in_code_not_kg or in_kg_not_code:
                            diff["relation_type_drift"] = {
                                "defined_not_used": sorted(in_code_not_kg),
                                "used_not_defined": sorted(in_kg_not_code),
                            }

    # 5. Stale references in KG content (e.g. removed tools, old architecture)
    removed_patterns = {
        "log_tool_call": "Tool was removed — L1 is transient context memory",
        "mcp as docs_mcp": "Old multi-server import pattern — Marvin is unified",
        "mcp as web_mcp": "Old multi-server import pattern — Marvin is unified",
        "mcp as design_mcp": "Old multi-server import pattern — Marvin is unified",
        "4 POC servers": "Now 6 backend modules in a single server",
        "search_tool_calls": "Not exposed as MCP tool — internal to retrieve()",
        "search_decisions": "Not exposed as MCP tool — internal to retrieve()",
        "search_sessions": "Not exposed as MCP tool — internal to retrieve()",
    }

    for name, data in kg["implementation_concepts"].items():
        content = (data.get("content") or "") + " " + (data.get("summary") or "")
        for pattern, reason in removed_patterns.items():
            if pattern in content:
                diff["stale_references"].append({
                    "concept": name,
                    "reference": pattern,
                    "reason": reason,
                })

    # 6. Concepts that should describe code features but are missing/outdated
    # Check if the KG has concepts for each backend module
    backend_concept_map = {
        "ontology": "Neo4j",
        "memory": "Milvus",
        "docs_backend": "docs-server",
        "web_to_docs_backend": "web-to-docs",
        "prompt_engineer_backend": "prompt-engineer",
        "system_design_backend": "system-design",
    }

    all_related = {r["target"] for r in kg["marvin_relations"]}
    all_related |= {r["target"] for r in kg.get("marvin_incoming", [])}
    for module, concept_name in backend_concept_map.items():
        if concept_name not in all_related:
            diff["concept_gaps"].append({
                "module": module,
                "expected_concept": concept_name,
                "issue": f"Marvin has no relation to '{concept_name}' in KG",
            })

    return diff


# ─── Report Generation ───────────────────────────────────────────────────────


def generate_report(code: dict, kg: dict, diff: dict) -> str:
    """Generate a markdown audit report."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        "# Marvin Self-Audit Report",
        f"\nGenerated: {now}",
        "",
        "## Summary",
        "",
        f"- **Code tools**: {len(code['tools'])}",
        f"- **Canonical MARVIN_TOOLS list**: {len(code['constants'].get('MARVIN_TOOLS', []))}",
        f"- **KG concepts**: {kg['total_concepts']}",
        f"- **KG relations**: {kg['total_relations']}",
        f"- **Backend modules**: {len(code['backends'])}",
        "",
    ]

    # Findings
    findings = []

    if diff["tool_count_mismatch"]:
        m = diff["tool_count_mismatch"]
        findings.append(
            f"**Tool count drift**: KG claims {m['kg_claims']} tools, "
            f"code has {m['code_has']}"
        )

    if diff["canonical_list_drift"]:
        d = diff["canonical_list_drift"]
        if d["in_list_not_decorated"]:
            findings.append(
                f"**MARVIN_TOOLS has entries without @mcp.tool**: "
                f"{', '.join(d['in_list_not_decorated'])}"
            )
        if d["decorated_not_in_list"]:
            findings.append(
                f"**@mcp.tool decorators not in MARVIN_TOOLS**: "
                f"{', '.join(d['decorated_not_in_list'])}"
            )

    if diff["relation_type_drift"]:
        d = diff["relation_type_drift"]
        if d["defined_not_used"]:
            findings.append(
                f"**Relation types defined in code but never used in KG**: "
                f"{', '.join(d['defined_not_used'])}"
            )
        if d["used_not_defined"]:
            findings.append(
                f"**Relation types in KG but not defined in code**: "
                f"{', '.join(d['used_not_defined'])}"
            )

    if diff["stale_references"]:
        for ref in diff["stale_references"]:
            findings.append(
                f"**Stale reference in '{ref['concept']}'**: "
                f"`{ref['reference']}` — {ref['reason']}"
            )

    if diff["concept_gaps"]:
        for gap in diff["concept_gaps"]:
            findings.append(
                f"**Missing relation**: {gap['issue']}"
            )

    if findings:
        lines.append("## Findings")
        lines.append("")
        for i, f in enumerate(findings, 1):
            lines.append(f"{i}. {f}")
        lines.append("")
    else:
        lines.append("## Findings")
        lines.append("")
        lines.append("No drift detected. Code and ontology are aligned.")
        lines.append("")

    # Detail sections
    lines.append("## Code Structure")
    lines.append("")
    lines.append(f"### Tools ({len(code['tools'])})")
    lines.append("")
    for t in sorted(code["tools"]):
        retrieval = code["constants"].get("RETRIEVAL_TOOLS", [])
        guarded = code["constants"].get("GUARDED_TOOLS", [])
        if t in retrieval:
            classification = "retrieval"
        elif t in guarded:
            classification = "guarded"
        else:
            classification = "always-allowed"
        lines.append(f"- `{t}` [{classification}]")
    lines.append("")

    lines.append(f"### Backends ({len(code['backends'])})")
    lines.append("")
    for module, funcs in sorted(code["backends"].items()):
        lines.append(f"- **{module}**: {', '.join(funcs)}")
    lines.append("")

    lines.append("### Middleware")
    lines.append("")
    for m in code["middleware"]:
        lines.append(f"- `{m}`")
    lines.append("")

    # Middleware classification detail
    if diff["middleware_gaps"]:
        lines.append("### Always-Allowed Tools (not in RETRIEVAL or GUARDED)")
        lines.append("")
        for t in diff["middleware_gaps"]:
            lines.append(f"- `{t}`")
        lines.append("")

    lines.append("## KG Claims")
    lines.append("")
    if kg["marvin_concept"]:
        lines.append(f"### Marvin Node")
        lines.append(f"- Vault: {kg['marvin_concept'].get('vault', '?')}")
        summary = kg["marvin_concept"].get("summary", "")
        lines.append(f"- Summary: {summary}")
        lines.append("")

    lines.append(f"### Marvin Relations ({len(kg['marvin_relations'])})")
    lines.append("")
    for rel in sorted(kg["marvin_relations"], key=lambda r: (r["rel_type"], r["target"])):
        lines.append(f"- —[{rel['rel_type']}]→ {rel['target']}")
    lines.append("")

    lines.append("---")
    lines.append(f"*Self-audit script: `mcp-server/self_audit.py`*")

    return "\n".join(lines)


# ─── Main ─────────────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(description="Marvin Self-Audit")
    parser.add_argument("--save", action="store_true", help="Save report to docs/")
    args = parser.parse_args()

    # Extract code structure
    code = extract_code_structure()

    # Connect to Neo4j and extract KG claims
    driver = GraphDatabase.driver(NEO4J_URI, auth=NEO4J_AUTH)
    try:
        kg = extract_kg_claims(driver)
    finally:
        driver.close()

    # Compute diff
    diff = compute_diff(code, kg)

    # Generate report
    report = generate_report(code, kg, diff)

    print(report)

    if args.save:
        out_path = REPO_ROOT / "docs" / "self-audit-report.md"
        out_path.write_text(report)
        print(f"\nReport saved to {out_path}")


if __name__ == "__main__":
    main()
