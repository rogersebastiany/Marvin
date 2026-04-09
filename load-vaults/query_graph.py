"""
Interactive Neo4j graph explorer.

Usage:
    uv run python query_graph.py [command] [args...]

Commands:
    stats                       Graph overview
    top [n]                     Most connected concepts (default: 20)
    concept <name>              Full concept detail + neighbors
    search <text>               Search concepts by name or content
    neighbors <name> [hops]     Show neighborhood (default: 1 hop)
    path <from> <to>            Shortest path between two concepts
    vault <name>                All concepts in a vault (thesis/implementation/both)
    orphans                     Concepts with fewest connections
    bridges                     Concepts that connect both vaults
    clusters                    Community detection via connected components
    edges <name>                All edges for a concept with details
    cypher <query>              Run raw Cypher query
"""

import sys
from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
AUTH = ("neo4j", "tautologia")


def get_driver():
    return GraphDatabase.driver(URI, auth=AUTH)


def cmd_stats(driver):
    with driver.session() as s:
        nodes = s.run("MATCH (c:Concept) RETURN count(c) AS n").single()["n"]
        edges = s.run("MATCH ()-[r:RELATES_TO]->() RETURN count(r) AS n").single()["n"]
        vaults = s.run(
            "MATCH (c:Concept) RETURN c.vault AS vault, count(*) AS n ORDER BY n DESC"
        )
        ghosts = s.run(
            "MATCH (c:Concept {ghost: true}) RETURN count(c) AS n"
        ).single()["n"]
        print(f"Nodes: {nodes}")
        print(f"Edges: {edges}")
        print(f"Ghosts: {ghosts}")
        print(f"\nBy vault:")
        for r in vaults:
            print(f"  {r['vault']}: {r['n']}")

        density = s.run(
            "MATCH (c:Concept)-[r]-() "
            "WITH c, count(r) AS deg "
            "RETURN min(deg) AS min, max(deg) AS max, avg(deg) AS avg, "
            "percentileDisc(deg, 0.5) AS median"
        ).single()
        print(f"\nDegree: min={density['min']}, max={density['max']}, "
              f"avg={density['avg']:.1f}, median={density['median']}")


def cmd_top(driver, n=20):
    with driver.session() as s:
        result = s.run(
            "MATCH (c:Concept)-[r]-() "
            "RETURN c.name AS name, c.vault AS vault, count(r) AS connections "
            "ORDER BY connections DESC LIMIT $n",
            n=int(n),
        )
        print(f"{'Concept':<45} {'Vault':<16} {'Connections':>5}")
        print("-" * 70)
        for r in result:
            print(f"{r['name']:<45} {r['vault']:<16} {r['connections']:>5}")


def cmd_concept(driver, name):
    with driver.session() as s:
        c = s.run(
            "MATCH (c:Concept {name: $name}) RETURN c", name=name
        ).single()
        if not c:
            print(f"Concept '{name}' not found.")
            _suggest(s, name)
            return

        node = c["c"]
        print(f"# {node['name']}")
        print(f"Vault: {node['vault']}")
        print(f"Ghost: {node['ghost']}")
        print(f"Summary: {node['summary']}")
        print(f"Created: {node['created_at']}")
        print()

        # Outgoing
        out = s.run(
            "MATCH (c:Concept {name: $name})-[r:RELATES_TO]->(t:Concept) "
            "RETURN t.name AS target, r.reasoning AS reasoning "
            "ORDER BY target",
            name=name,
        )
        out_list = list(out)
        if out_list:
            print(f"Links to ({len(out_list)}):")
            for r in out_list:
                print(f"  → {r['target']}")

        # Incoming
        inc = s.run(
            "MATCH (c:Concept {name: $name})<-[r:RELATES_TO]-(s:Concept) "
            "RETURN s.name AS source "
            "ORDER BY source",
            name=name,
        )
        inc_list = list(inc)
        if inc_list:
            print(f"\nLinked from ({len(inc_list)}):")
            for r in inc_list:
                print(f"  ← {r['source']}")


def cmd_search(driver, text):
    with driver.session() as s:
        result = s.run(
            "MATCH (c:Concept) "
            "WHERE toLower(c.name) CONTAINS toLower($text) "
            "   OR toLower(c.summary) CONTAINS toLower($text) "
            "   OR toLower(c.content) CONTAINS toLower($text) "
            "RETURN c.name AS name, c.vault AS vault, c.summary AS summary "
            "ORDER BY CASE WHEN toLower(c.name) CONTAINS toLower($text) THEN 0 ELSE 1 END, name",
            text=text,
        )
        results = list(result)
        if not results:
            print(f"No results for '{text}'.")
            return
        print(f"Found {len(results)} concepts:\n")
        for r in results:
            print(f"  [{r['vault']}] {r['name']}")
            if r["summary"]:
                print(f"    {r['summary'][:100]}")


def cmd_neighbors(driver, name, hops=1):
    with driver.session() as s:
        c = s.run("MATCH (c:Concept {name: $name}) RETURN c", name=name).single()
        if not c:
            print(f"Concept '{name}' not found.")
            _suggest(s, name)
            return

        result = s.run(
            "MATCH (c:Concept {name: $name})-[:RELATES_TO*1..$hops]-(n:Concept) "
            "RETURN DISTINCT n.name AS name, n.vault AS vault "
            "ORDER BY vault, name",
            name=name,
            hops=int(hops),
        )
        results = list(result)
        print(f"Neighborhood of '{name}' ({hops} hop{'s' if int(hops)>1 else ''}, {len(results)} concepts):\n")
        current_vault = None
        for r in results:
            if r["vault"] != current_vault:
                current_vault = r["vault"]
                print(f"  [{current_vault}]")
            print(f"    {r['name']}")


def cmd_path(driver, from_name, to_name):
    with driver.session() as s:
        result = s.run(
            "MATCH p = shortestPath("
            "  (a:Concept {name: $from})-[:RELATES_TO*]-(b:Concept {name: $to})"
            ") "
            "RETURN [n IN nodes(p) | n.name] AS path, length(p) AS hops",
            **{"from": from_name, "to": to_name},
        )
        rec = result.single()
        if not rec:
            print(f"No path from '{from_name}' to '{to_name}'.")
            return
        print(f"Path ({rec['hops']} hops):")
        print(f"  {' → '.join(rec['path'])}")


def cmd_vault(driver, vault_name):
    with driver.session() as s:
        result = s.run(
            "MATCH (c:Concept)-[r]-() "
            "WHERE c.vault = $vault "
            "RETURN c.name AS name, count(r) AS connections "
            "ORDER BY connections DESC",
            vault=vault_name,
        )
        results = list(result)
        if not results:
            print(f"No concepts in vault '{vault_name}'. Try: thesis, implementation, both")
            return
        print(f"Vault '{vault_name}' ({len(results)} concepts):\n")
        print(f"{'Concept':<45} {'Connections':>5}")
        print("-" * 52)
        for r in results:
            print(f"{r['name']:<45} {r['connections']:>5}")


def cmd_orphans(driver):
    with driver.session() as s:
        result = s.run(
            "MATCH (c:Concept)-[r]-() "
            "WITH c, count(r) AS connections "
            "ORDER BY connections ASC "
            "LIMIT 15 "
            "RETURN c.name AS name, c.vault AS vault, connections"
        )
        print(f"{'Concept':<45} {'Vault':<16} {'Connections':>5}")
        print("-" * 70)
        for r in result:
            print(f"{r['name']:<45} {r['vault']:<16} {r['connections']:>5}")


def cmd_bridges(driver):
    """Concepts that have edges to both thesis and implementation vault concepts."""
    with driver.session() as s:
        result = s.run(
            "MATCH (c:Concept)-[:RELATES_TO]-(t:Concept {vault: 'thesis'}) "
            "WITH c, count(DISTINCT t) AS thesis_links "
            "MATCH (c)-[:RELATES_TO]-(i:Concept {vault: 'implementation'}) "
            "WITH c, thesis_links, count(DISTINCT i) AS impl_links "
            "RETURN c.name AS name, c.vault AS vault, "
            "  thesis_links, impl_links, thesis_links + impl_links AS total "
            "ORDER BY total DESC LIMIT 20"
        )
        print(f"{'Concept':<40} {'Vault':<14} {'Thesis':>6} {'Impl':>6} {'Total':>6}")
        print("-" * 76)
        for r in result:
            print(f"{r['name']:<40} {r['vault']:<14} {r['thesis_links']:>6} "
                  f"{r['impl_links']:>6} {r['total']:>6}")


def cmd_clusters(driver):
    """Find loosely connected subgraphs."""
    with driver.session() as s:
        # Use APOC if available, otherwise manual BFS
        try:
            result = s.run(
                "CALL apoc.algo.unionFind('Concept', 'RELATES_TO') "
                "YIELD nodeId, setId "
                "WITH setId, collect(gds.util.asNode(nodeId).name) AS members "
                "RETURN setId, size(members) AS size, members "
                "ORDER BY size DESC"
            )
            for r in result:
                print(f"Cluster {r['setId']} ({r['size']} members): {', '.join(r['members'][:5])}...")
        except Exception:
            # Fallback: just show isolated components
            result = s.run(
                "MATCH (c:Concept) "
                "WHERE NOT (c)-[:RELATES_TO]-() "
                "RETURN c.name AS name, c.vault AS vault"
            )
            isolated = list(result)
            if isolated:
                print("Isolated nodes (no edges):")
                for r in isolated:
                    print(f"  [{r['vault']}] {r['name']}")
            else:
                print("No isolated nodes. Graph is fully connected.")
                # Show weakly connected nodes
                result = s.run(
                    "MATCH (c:Concept)-[r]-() "
                    "WITH c, count(r) AS deg WHERE deg <= 3 "
                    "RETURN c.name AS name, c.vault AS vault, deg "
                    "ORDER BY deg, name"
                )
                weak = list(result)
                if weak:
                    print(f"\nWeakly connected (≤3 edges, {len(weak)} concepts):")
                    for r in weak:
                        print(f"  {r['deg']}  [{r['vault']}] {r['name']}")


def cmd_edges(driver, name):
    with driver.session() as s:
        c = s.run("MATCH (c:Concept {name: $name}) RETURN c", name=name).single()
        if not c:
            print(f"Concept '{name}' not found.")
            _suggest(s, name)
            return

        result = s.run(
            "MATCH (c:Concept {name: $name})-[r:RELATES_TO]->(t:Concept) "
            "RETURN '→' AS dir, t.name AS other, r.weight AS weight, "
            "  r.reasoning AS reasoning, r.discovered_by AS by "
            "UNION ALL "
            "MATCH (c:Concept {name: $name})<-[r:RELATES_TO]-(s:Concept) "
            "RETURN '←' AS dir, s.name AS other, r.weight AS weight, "
            "  r.reasoning AS reasoning, r.discovered_by AS by "
            "ORDER BY dir, other",
            name=name,
        )
        results = list(result)
        print(f"Edges for '{name}' ({len(results)}):\n")
        for r in results:
            w = f" w={r['weight']}" if r["weight"] else ""
            by = f" [{r['by']}]" if r["by"] else ""
            print(f"  {r['dir']} {r['other']}{w}{by}")


def cmd_cypher(driver, query):
    with driver.session() as s:
        try:
            result = s.run(query)
            records = list(result)
            if not records:
                print("(no results)")
                return
            keys = records[0].keys()
            for rec in records:
                parts = [f"{k}={rec[k]}" for k in keys]
                print("  ".join(parts))
        except Exception as e:
            print(f"Error: {e}")


def _suggest(session, name):
    """Suggest similar concept names."""
    result = session.run(
        "MATCH (c:Concept) WHERE toLower(c.name) CONTAINS toLower($name) "
        "RETURN c.name LIMIT 5",
        name=name,
    )
    suggestions = [r[0] for r in result]
    if suggestions:
        print(f"Did you mean: {', '.join(suggestions)}?")


COMMANDS = {
    "stats": (cmd_stats, 0),
    "top": (cmd_top, 1),
    "concept": (cmd_concept, 1),
    "search": (cmd_search, 1),
    "neighbors": (cmd_neighbors, 2),
    "path": (cmd_path, 2),
    "vault": (cmd_vault, 1),
    "orphans": (cmd_orphans, 0),
    "bridges": (cmd_bridges, 0),
    "clusters": (cmd_clusters, 0),
    "edges": (cmd_edges, 1),
    "cypher": (cmd_cypher, 1),
}


def main():
    args = sys.argv[1:]

    if not args or args[0] in ("-h", "--help", "help"):
        print(__doc__)
        return

    cmd_name = args[0]
    cmd_args = args[1:]

    if cmd_name not in COMMANDS:
        print(f"Unknown command: {cmd_name}")
        print(f"Available: {', '.join(COMMANDS.keys())}")
        return

    func, max_extra = COMMANDS[cmd_name]
    driver = get_driver()
    try:
        if cmd_name == "cypher":
            func(driver, " ".join(cmd_args))
        elif cmd_name in ("neighbors",):
            func(driver, cmd_args[0] if cmd_args else "", cmd_args[1] if len(cmd_args) > 1 else 1)
        elif cmd_name == "path":
            if len(cmd_args) < 2:
                print("Usage: path <from> <to>")
                return
            func(driver, cmd_args[0], cmd_args[1])
        elif cmd_args:
            func(driver, cmd_args[0])
        else:
            func(driver)
    finally:
        driver.close()


if __name__ == "__main__":
    main()
