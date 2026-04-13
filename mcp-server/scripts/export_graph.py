"""
Export Neo4j knowledge graph to JSON for the standalone HTML visualization.

Usage:
    uv run python scripts/export_graph.py

Produces scripts/graph-data.js consumed by neo4j-viz.html.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from backends.ontology import _get_driver


def export():
    driver = _get_driver()
    nodes = {}
    edges = []

    with driver.session() as s:
        # All concepts with properties
        result = s.run("""
            MATCH (c:Concept)
            RETURN id(c) AS id, c.name AS name, c.vault AS vault,
                   c.summary AS summary, labels(c) AS labels
        """)
        for r in result:
            nid = r["id"]
            vault = r["vault"] or "cognee"
            if vault not in ("agent", "ghost"):
                vault = "cognee"
            nodes[nid] = {
                "id": nid,
                "name": r["name"] or "?",
                "vault": vault,
                "summary": (r["summary"] or "")[:200],
                "labels": r["labels"],
            }

        # All edges between concepts
        result = s.run("""
            MATCH (a:Concept)-[r]->(b:Concept)
            RETURN id(r) AS id, id(a) AS source, id(b) AS target, type(r) AS type
        """)
        for r in result:
            src = r["source"]
            tgt = r["target"]
            if src in nodes and tgt in nodes:
                edges.append({
                    "id": r["id"],
                    "source": src,
                    "target": tgt,
                    "type": r["type"],
                })

    # Compute degree + dominant edge type for coloring
    degree = {}
    edge_counts = {}  # node_id → {edge_type: count}
    for e in edges:
        degree[e["source"]] = degree.get(e["source"], 0) + 1
        degree[e["target"]] = degree.get(e["target"], 0) + 1
        for nid in (e["source"], e["target"]):
            if nid not in edge_counts:
                edge_counts[nid] = {}
            edge_counts[nid][e["type"]] = edge_counts[nid].get(e["type"], 0) + 1

    for nid, node in nodes.items():
        node["degree"] = degree.get(nid, 0)
        counts = edge_counts.get(nid, {})
        if counts:
            node["dominant_edge"] = max(counts, key=counts.get)
        else:
            node["dominant_edge"] = "NONE"

    data = {
        "nodes": list(nodes.values()),
        "edges": edges,
        "stats": {
            "total_nodes": len(nodes),
            "total_edges": len(edges),
            "by_vault": {
                "cognee": sum(1 for n in nodes.values() if n["vault"] == "cognee"),
                "agent": sum(1 for n in nodes.values() if n["vault"] == "agent"),
                "ghost": sum(1 for n in nodes.values() if n["vault"] == "ghost"),
            },
        },
    }

    out = Path(__file__).parent / "graph-data.js"
    out.write_text(f"const GRAPH_DATA = {json.dumps(data, ensure_ascii=False)};")
    print(f"Exported {len(nodes)} nodes, {len(edges)} edges → {out}")


if __name__ == "__main__":
    export()
