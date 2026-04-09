"""
Ontological Determinism Report.

Measures how close the knowledge graph is to ontological completeness —
the condition under which the Tautologia Ontológica thesis predicts
deterministic behavior.

Metrics:
  1. Ghost Coverage     — % of referenced concepts that have definitions
  2. Content Coverage   — % of concepts with actual content (not empty)
  3. Summary Coverage   — % of concepts with summaries
  4. Connectivity       — min degree (weakest link), avg degree, density
  5. Bidirectionality   — % of edges that are reciprocal (A→B and B→A)
  6. Vault Bridging     — % of concepts reachable from both vaults
  7. Tool Tautology     — % of tool-concepts classified as tautological
  8. Completeness Score — weighted composite of all metrics

Usage:
    uv run python determinism_report.py
"""

from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
AUTH = ("neo4j", "tautologia")


def report(session):
    metrics = {}

    # 1. Ghost Coverage
    total = session.run("MATCH (c:Concept) RETURN count(c) AS n").single()["n"]
    ghosts = session.run(
        "MATCH (c:Concept {ghost: true}) RETURN count(c) AS n"
    ).single()["n"]
    ghost_coverage = (total - ghosts) / total * 100 if total else 0
    metrics["ghost_coverage"] = ghost_coverage

    # 2. Content Coverage
    with_content = session.run(
        "MATCH (c:Concept) WHERE c.content IS NOT NULL AND size(c.content) > 10 "
        "RETURN count(c) AS n"
    ).single()["n"]
    content_coverage = with_content / total * 100 if total else 0
    metrics["content_coverage"] = content_coverage

    # 3. Summary Coverage
    with_summary = session.run(
        "MATCH (c:Concept) WHERE c.summary IS NOT NULL AND size(c.summary) > 5 "
        "RETURN count(c) AS n"
    ).single()["n"]
    summary_coverage = with_summary / total * 100 if total else 0
    metrics["summary_coverage"] = summary_coverage

    # 4. Connectivity
    degree_stats = session.run(
        "MATCH (c:Concept)-[r]-() "
        "WITH c, count(r) AS deg "
        "RETURN min(deg) AS min_deg, max(deg) AS max_deg, "
        "  avg(deg) AS avg_deg, count(c) AS connected_nodes"
    ).single()

    isolated = session.run(
        "MATCH (c:Concept) WHERE NOT (c)-[:RELATES_TO]-() "
        "RETURN count(c) AS n"
    ).single()["n"]

    min_deg = degree_stats["min_deg"] or 0
    avg_deg = degree_stats["avg_deg"] or 0
    max_deg = degree_stats["max_deg"] or 0
    connected = degree_stats["connected_nodes"] or 0

    # Connectivity score: 100% when no isolated nodes and min degree >= 3
    connectivity_score = 0
    if total > 0:
        connected_pct = connected / total * 100
        min_deg_score = min(min_deg / 3, 1.0) * 100  # 3+ edges = fully connected
        connectivity_score = (connected_pct + min_deg_score) / 2
    metrics["connectivity"] = connectivity_score

    # Edge density: actual edges / max possible edges
    edges = session.run(
        "MATCH ()-[r:RELATES_TO]->() RETURN count(r) AS n"
    ).single()["n"]
    max_edges = total * (total - 1)  # directed graph
    density = edges / max_edges * 100 if max_edges else 0

    # 5. Bidirectionality
    reciprocal = session.run(
        "MATCH (a:Concept)-[r1:RELATES_TO]->(b:Concept) "
        "WHERE (b)-[:RELATES_TO]->(a) "
        "RETURN count(r1) AS n"
    ).single()["n"]
    bidirectional_pct = reciprocal / edges * 100 if edges else 0
    metrics["bidirectionality"] = bidirectional_pct

    # 6. Vault Bridging
    # Concepts that are reachable from at least one thesis AND one implementation concept
    bridge_concepts = session.run(
        "MATCH (c:Concept)-[:RELATES_TO]-(t:Concept) "
        "WHERE t.vault IN ['thesis', 'both'] "
        "WITH c, count(DISTINCT t) AS thesis_neighbors "
        "WHERE thesis_neighbors > 0 "
        "MATCH (c)-[:RELATES_TO]-(i:Concept) "
        "WHERE i.vault IN ['implementation', 'both'] "
        "WITH c, count(DISTINCT i) AS impl_neighbors "
        "WHERE impl_neighbors > 0 "
        "RETURN count(c) AS n"
    ).single()["n"]
    vault_bridging = bridge_concepts / total * 100 if total else 0
    metrics["vault_bridging"] = vault_bridging

    # 7. Tool Tautology
    # Check concepts that represent tools (server names + tool-related concepts)
    tool_concepts = session.run(
        "MATCH (c:Concept) "
        "WHERE c.name IN ['docs-server', 'web-to-docs', 'prompt-engineer', 'system-design', "
        "  'mcp-ontology-server', 'mcp-memory-server'] "
        "RETURN count(c) AS total"
    ).single()["total"]

    tautological_tools = session.run(
        "MATCH (c:Concept) "
        "WHERE c.name IN ['docs-server', 'web-to-docs', 'mcp-ontology-server', 'mcp-memory-server'] "
        "RETURN count(c) AS n"
    ).single()["n"]

    # prompt-engineer and system-design are partially tautological
    partial_tools = session.run(
        "MATCH (c:Concept) "
        "WHERE c.name IN ['prompt-engineer', 'system-design'] "
        "RETURN count(c) AS n"
    ).single()["n"]

    tool_tautology = 0
    if tool_concepts > 0:
        tool_tautology = (tautological_tools + partial_tools * 0.5) / tool_concepts * 100
    metrics["tool_tautology"] = tool_tautology

    # --- Composite Score ---
    weights = {
        "ghost_coverage": 0.20,      # Referenced = defined
        "content_coverage": 0.15,    # Defined = has substance
        "summary_coverage": 0.05,    # Nice to have
        "connectivity": 0.20,        # Everything connects
        "bidirectionality": 0.10,    # Relationships validated from both sides
        "vault_bridging": 0.15,      # Theory meets implementation
        "tool_tautology": 0.15,      # Tools are tautological
    }

    composite = sum(metrics[k] * weights[k] for k in weights)

    # ========== PRINT REPORT ==========
    print("=" * 65)
    print("  ONTOLOGICAL DETERMINISM REPORT")
    print("  Tautologia Ontológica — Knowledge Graph Assessment")
    print("=" * 65)
    print()

    print(f"  Graph: {total} concepts, {edges} edges, {ghosts} ghosts")
    print(f"  Density: {density:.2f}% of max possible edges")
    print(f"  Degree: min={min_deg}, avg={avg_deg:.1f}, max={max_deg}")
    print(f"  Isolated: {isolated}")
    print()

    print("-" * 65)
    print(f"  {'Metric':<35} {'Score':>8}  {'Status':<15}")
    print("-" * 65)

    labels = {
        "ghost_coverage": "Ghost Coverage (defined/referenced)",
        "content_coverage": "Content Coverage (has substance)",
        "summary_coverage": "Summary Coverage (has summary)",
        "connectivity": "Connectivity (no orphans, min 3)",
        "bidirectionality": "Bidirectionality (A→B and B→A)",
        "vault_bridging": "Vault Bridging (theory↔impl)",
        "tool_tautology": "Tool Tautology (tautological tools)",
    }

    for key in weights:
        score = metrics[key]
        status = _status(score)
        w = weights[key]
        print(f"  {labels[key]:<35} {score:>7.1f}%  {status:<15}  (w={w})")

    print("-" * 65)
    print(f"  {'COMPOSITE DETERMINISM SCORE':<35} {composite:>7.1f}%  {_status(composite)}")
    print("=" * 65)

    # Gaps
    print()
    print("GAPS TO 100%:")
    print()

    if ghost_coverage < 100:
        print(f"  ⚠ {ghosts} ghost nodes (referenced but undefined)")
        ghost_list = session.run(
            "MATCH (c:Concept {ghost: true}) RETURN c.name AS name"
        )
        for r in ghost_list:
            print(f"      - {r['name']}")

    if content_coverage < 100:
        no_content = session.run(
            "MATCH (c:Concept) "
            "WHERE c.content IS NULL OR size(c.content) <= 10 "
            "RETURN c.name AS name ORDER BY name"
        )
        names = [r["name"] for r in no_content]
        if names:
            print(f"  ⚠ {len(names)} concepts without content: {', '.join(names[:10])}")

    if min_deg < 3:
        weak = session.run(
            "MATCH (c:Concept)-[r]-() "
            "WITH c, count(r) AS deg WHERE deg < 3 "
            "RETURN c.name AS name, deg ORDER BY deg"
        )
        weak_list = list(weak)
        if weak_list:
            print(f"  ⚠ {len(weak_list)} weakly connected concepts (< 3 edges):")
            for r in weak_list:
                print(f"      - {r['name']} ({r['deg']} edges)")

    if bidirectional_pct < 80:
        print(f"  ⚠ Only {bidirectional_pct:.0f}% of edges are bidirectional")
        print(f"      One-directional links = unvalidated from one side")

    if vault_bridging < 80:
        unbridged = session.run(
            "MATCH (c:Concept) "
            "WHERE NOT EXISTS { "
            "  MATCH (c)-[:RELATES_TO]-(t:Concept) "
            "  WHERE t.vault IN ['thesis', 'both'] "
            "} OR NOT EXISTS { "
            "  MATCH (c)-[:RELATES_TO]-(i:Concept) "
            "  WHERE i.vault IN ['implementation', 'both'] "
            "} "
            "RETURN c.name AS name, c.vault AS vault ORDER BY vault, name"
        )
        unbridged_list = list(unbridged)
        if unbridged_list:
            print(f"  ⚠ {len(unbridged_list)} concepts not bridging both vaults:")
            for r in unbridged_list[:15]:
                print(f"      - [{r['vault']}] {r['name']}")
            if len(unbridged_list) > 15:
                print(f"      ... and {len(unbridged_list) - 15} more")

    if tool_tautology < 100:
        print(f"  ⚠ Tool tautology at {tool_tautology:.0f}%")
        print(f"      prompt-engineer and system-design are partially tautological")
        print(f"      (generation tools — output is constrained but not closed)")

    if composite >= 95:
        print("\n  ✓ Graph is approaching ontological completeness.")
    elif composite >= 80:
        print("\n  → Graph is well-structured. Address gaps above to approach 100%.")
    else:
        print("\n  → Significant gaps remain. Focus on content and connectivity.")

    print()


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
