"""
Ontological Determinism Report.

Measures how close the knowledge graph is to ontological completeness —
the condition under which the Tautologia Ontológica thesis predicts
deterministic behavior.

Aligned with Cognee Era 2 schema:
  - Concept nodes have `description` (not `content`), no `vault`, no `ghost`
  - TextSummary nodes linked via COMPOSES
  - 16 typed edge types (not just RELATES_TO)
  - No vault property — replaced with Edge Type Diversity

Metrics:
  1. Grounding         — % of concepts linked to source documents
  2. Content Coverage  — % of concepts with description text
  3. Summary Coverage  — % of concepts with linked TextSummary
  4. Connectivity      — min degree, avg degree, isolated nodes
  5. Bidirectionality  — % of semantic edges that are reciprocal
  6. Edge Diversity    — % of concepts with 2+ different edge types
  7. Tool Tautology    — % of tool-concepts classified as tautological
  8. Completeness Score — weighted composite of all metrics

Usage:
    uv run python determinism_report.py
"""

import os

from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
AUTH = (os.getenv("NEO4J_USER", "neo4j"), os.getenv("NEO4J_PASS", "tautologia"))

# Semantic edge types between Concepts (excludes COMPOSES which is structural)
SEMANTIC_EDGE_TYPES = [
    "RELATES_TO", "PROVES", "ENABLES", "IMPLEMENTS", "COMPOSES_CONCEPT",
    "EXEMPLIFIES", "REQUIRES", "EXTENDS", "CONTRADICTS", "EVOLVES_FROM",
    "REDUCES", "MITIGATES", "ANALOGOUS_TO", "DEFINES", "FORMALIZES", "INFERS",
]

# Symmetric edge types — A→B implies B→A by definition
SYMMETRIC_TYPES = {"RELATES_TO", "CONTRADICTS", "ANALOGOUS_TO"}


def report(session):
    metrics = {}

    total = session.run("MATCH (c:Concept) RETURN count(c) AS n").single()["n"]

    # 1. Grounding — concepts linked to source documents via DocumentChunk
    grounded = session.run(
        "MATCH (c:Concept)-[:COMPOSES]-(dc:DocumentChunk)-[:COMPOSES]-(td:TextDocument) "
        "RETURN count(DISTINCT c) AS n"
    ).single()["n"]
    grounding_pct = grounded / total * 100 if total else 0
    metrics["grounding"] = grounding_pct

    # 2. Content Coverage — concepts with description
    with_content = session.run(
        "MATCH (c:Concept) WHERE c.description IS NOT NULL AND size(c.description) > 10 "
        "RETURN count(c) AS n"
    ).single()["n"]
    content_coverage = with_content / total * 100 if total else 0
    metrics["content_coverage"] = content_coverage

    # 3. Summary Coverage — concepts with linked TextSummary (via DocumentChunk)
    with_summary = session.run(
        "MATCH (c:Concept)-[:COMPOSES]-(:DocumentChunk)-[:COMPOSES]-(s:TextSummary) "
        "RETURN count(DISTINCT c) AS n"
    ).single()["n"]
    summary_coverage = with_summary / total * 100 if total else 0
    metrics["summary_coverage"] = summary_coverage

    # 4. Connectivity — using ALL edge types
    degree_stats = session.run(
        "MATCH (c:Concept)-[r]-() "
        "WITH c, count(r) AS deg "
        "RETURN min(deg) AS min_deg, max(deg) AS max_deg, "
        "  avg(deg) AS avg_deg, count(c) AS connected_nodes"
    ).single()

    isolated = session.run(
        "MATCH (c:Concept) WHERE NOT (c)-[]-() "
        "RETURN count(c) AS n"
    ).single()["n"]

    min_deg = degree_stats["min_deg"] or 0
    avg_deg = degree_stats["avg_deg"] or 0
    max_deg = degree_stats["max_deg"] or 0
    connected = degree_stats["connected_nodes"] or 0

    connectivity_score = 0
    if total > 0:
        connected_pct = connected / total * 100
        min_deg_score = min(min_deg / 3, 1.0) * 100
        connectivity_score = (connected_pct + min_deg_score) / 2
    metrics["connectivity"] = connectivity_score

    # Total edges — ALL types
    all_edges = session.run(
        "MATCH ()-[r]->() RETURN count(r) AS n"
    ).single()["n"]

    # Semantic edges only (Concept→Concept, excluding structural COMPOSES)
    semantic_edges = session.run(
        "MATCH (a:Concept)-[r]->(b:Concept) "
        "WHERE type(r) <> 'COMPOSES' "
        "RETURN count(r) AS n"
    ).single()["n"]

    # Edge density
    max_edges = total * (total - 1)
    density = all_edges / max_edges * 100 if max_edges else 0

    # Edge type breakdown
    edge_types = session.run(
        "MATCH ()-[r]->() RETURN type(r) AS t, count(r) AS c ORDER BY c DESC"
    )
    edge_breakdown = {r["t"]: r["c"] for r in edge_types}

    # 5. Bidirectionality — semantic edges only
    # Symmetric types count as 100% bidirectional
    symmetric_count = session.run(
        "MATCH (a:Concept)-[r]->(b:Concept) "
        "WHERE type(r) IN ['RELATES_TO', 'CONTRADICTS', 'ANALOGOUS_TO'] "
        "RETURN count(r) AS n"
    ).single()["n"]

    # Directional types: check for actual reverse edge (any type)
    directional_reciprocal = session.run(
        "MATCH (a:Concept)-[r]->(b:Concept) "
        "WHERE NOT type(r) IN ['RELATES_TO', 'CONTRADICTS', 'ANALOGOUS_TO', 'COMPOSES'] "
        "AND (b)-[]->(a) "
        "RETURN count(r) AS n"
    ).single()["n"]

    directional_total = session.run(
        "MATCH (a:Concept)-[r]->(b:Concept) "
        "WHERE NOT type(r) IN ['RELATES_TO', 'CONTRADICTS', 'ANALOGOUS_TO', 'COMPOSES'] "
        "RETURN count(r) AS n"
    ).single()["n"]

    bidir_numerator = symmetric_count + directional_reciprocal
    bidir_denominator = symmetric_count + directional_total
    bidirectional_pct = bidir_numerator / bidir_denominator * 100 if bidir_denominator else 0
    metrics["bidirectionality"] = bidirectional_pct

    # 6. Edge Type Diversity — concepts with 2+ different semantic edge types
    diverse = session.run(
        "MATCH (c:Concept)-[r]-(other:Concept) "
        "WHERE type(r) <> 'COMPOSES' "
        "WITH c, count(DISTINCT type(r)) AS edge_types "
        "WHERE edge_types >= 2 "
        "RETURN count(c) AS n"
    ).single()["n"]
    # Score: % of connected concepts (not total) that have diverse edges
    concepts_with_semantic = session.run(
        "MATCH (c:Concept)-[r]-(other:Concept) "
        "WHERE type(r) <> 'COMPOSES' "
        "RETURN count(DISTINCT c) AS n"
    ).single()["n"]
    edge_diversity = diverse / concepts_with_semantic * 100 if concepts_with_semantic else 0
    metrics["edge_diversity"] = edge_diversity

    # 7. Tool Tautology — updated for 44 tools
    tautological = [
        # Retrieval — found or not found, deterministic
        "retrieve", "get_concept", "traverse", "why_exists", "get_memory",
        "search_docs", "list_docs", "get_doc", "list_concepts",
        # Logging — append-only, always succeeds
        "log_decision", "log_session",
        # Graph enrichment — deterministic MERGE operations
        "expand", "link", "auto_link", "ensure_bidirectional",
        "set_aliases", "batch_set_aliases",
        # Schema evolution — runs cypher, returns result
        "execute_schema_change",
        # Web/docs — fetch or fail, no ambiguity
        "fetch_url", "save_doc", "crawl_docs", "rank_urls",
        # Diagrams — file operations
        "save_diagram", "list_diagrams", "get_diagram",
        # Introspection — read-only state
        "inspect_schemas", "stats", "self_description",
        # Plans — deterministic save/refine
        "refine_plan", "save_plan",
        # Ops — deterministic sync/audit
        "sync_vaults", "audit_code",
    ]
    partial = [
        # Generation tools — constrained output but not fully closed
        "generate_prompt", "refine_prompt", "audit_prompt",
        "generate_diagram", "judge_diagram",
        "propose_schema_change",
        # Code/knowledge — LLM-assisted analysis
        "improve_code", "tdd", "research_topic",
        # Orchestration — deterministic chain selection but LLM-assisted context
        "orchestrate",
        # Self-improvement — applies LLM-generated fixes
        "self_improve",
    ]
    total_tools = len(tautological) + len(partial)
    tool_tautology = (len(tautological) + len(partial) * 0.5) / total_tools * 100
    metrics["tool_tautology"] = tool_tautology

    # --- Composite Score ---
    weights = {
        "grounding": 0.15,           # Concepts traced to source documents
        "content_coverage": 0.20,    # Concepts with substance
        "summary_coverage": 0.05,    # Concepts with summaries
        "connectivity": 0.20,        # Everything connects
        "bidirectionality": 0.10,    # Relationships validated from both sides
        "edge_diversity": 0.15,      # Rich typed relationships
        "tool_tautology": 0.15,      # Tools are tautological
    }

    composite = sum(metrics[k] * weights[k] for k in weights)

    # ========== PRINT REPORT ==========
    print("=" * 65)
    print("  ONTOLOGICAL DETERMINISM REPORT")
    print("  Tautologia Ontologica — Knowledge Graph Assessment")
    print("=" * 65)
    print()

    print(f"  Graph: {total} concepts, {all_edges} edges ({semantic_edges} semantic)")
    print(f"  Edge types: {len(edge_breakdown)} ({', '.join(f'{t}:{c}' for t, c in list(edge_breakdown.items())[:5])}...)")
    print(f"  Density: {density:.2f}% of max possible edges")
    print(f"  Degree: min={min_deg}, avg={avg_deg:.1f}, max={max_deg}")
    print(f"  Isolated: {isolated}")
    print()

    print("-" * 65)
    print(f"  {'Metric':<40} {'Score':>8}  {'Status':<15}")
    print("-" * 65)

    labels = {
        "grounding": "Grounding (linked to source docs)",
        "content_coverage": "Content Coverage (has description)",
        "summary_coverage": "Summary Coverage (has TextSummary)",
        "connectivity": "Connectivity (no orphans, min 3)",
        "bidirectionality": "Bidirectionality (reciprocal edges)",
        "edge_diversity": "Edge Diversity (2+ edge types)",
        "tool_tautology": "Tool Tautology (tautological tools)",
    }

    for key in weights:
        score = metrics[key]
        status = _status(score)
        w = weights[key]
        print(f"  {labels[key]:<40} {score:>7.1f}%  {status:<15}  (w={w})")

    print("-" * 65)
    print(f"  {'COMPOSITE DETERMINISM SCORE':<40} {composite:>7.1f}%  {_status(composite)}")
    print("=" * 65)

    # Gaps
    print()
    print("GAPS TO 100%:")
    print()

    if grounding_pct < 100:
        ungrounded = total - grounded
        print(f"  ⚠ {ungrounded} concepts not grounded in source documents")
        ungrounded_list = session.run(
            "MATCH (c:Concept) "
            "WHERE NOT EXISTS { "
            "  MATCH (c)-[:COMPOSES]-(:DocumentChunk)-[:COMPOSES]-(:TextDocument) "
            "} "
            "RETURN c.name AS name ORDER BY name LIMIT 15"
        )
        names = [r["name"] for r in ungrounded_list]
        if names:
            for n in names:
                print(f"      - {n}")
            if ungrounded > 15:
                print(f"      ... and {ungrounded - 15} more")

    if content_coverage < 100:
        no_content_count = total - with_content
        no_content = session.run(
            "MATCH (c:Concept) "
            "WHERE c.description IS NULL OR size(c.description) <= 10 "
            "RETURN c.name AS name ORDER BY name LIMIT 10"
        )
        names = [r["name"] for r in no_content]
        if names:
            print(f"  ⚠ {no_content_count} concepts without description: {', '.join(names)}")

    if min_deg < 3:
        weak = session.run(
            "MATCH (c:Concept)-[r]-() "
            "WITH c, count(r) AS deg WHERE deg < 3 "
            "RETURN c.name AS name, deg ORDER BY deg LIMIT 30"
        )
        weak_list = list(weak)
        if weak_list:
            print(f"  ⚠ Weakly connected concepts (< 3 edges, showing first 30):")
            for r in weak_list:
                print(f"      - {r['name']} ({r['deg']} edges)")

    if bidirectional_pct < 80:
        print(f"  ⚠ Only {bidirectional_pct:.0f}% of semantic edges are bidirectional")
        print(f"      ({symmetric_count} symmetric + {directional_reciprocal} reciprocal directional"
              f" / {bidir_denominator} total)")

    if edge_diversity < 80:
        print(f"  ⚠ Only {diverse}/{concepts_with_semantic} semantically connected concepts have 2+ edge types")
        print(f"      Rich typing is key to determinism — single-type connections are weak signals")

    if tool_tautology < 100:
        print(f"  ⚠ Tool tautology at {tool_tautology:.0f}% ({len(tautological)} full + {len(partial)} partial = {total_tools} tools)")
        print(f"      Partial: {', '.join(partial)}")

    if composite >= 95:
        print("\n  ✓ Graph is approaching ontological completeness.")
    elif composite >= 80:
        print("\n  → Graph is well-structured. Address gaps above to approach 100%.")
    else:
        print("\n  → Significant gaps remain. Focus on content and connectivity.")

    print()

    return metrics, weights, composite


def _status(score):
    if score >= 95:
        return "TAUTOLOGICAL"
    elif score >= 80:
        return "HIGH"
    elif score >= 60:
        return "MODERATE"
    elif score >= 40:
        return "LOW"
    else:
        return "CRITICAL"


def main():
    driver = GraphDatabase.driver(URI, auth=AUTH)
    with driver.session() as session:
        report(session)
    driver.close()


if __name__ == "__main__":
    main()
