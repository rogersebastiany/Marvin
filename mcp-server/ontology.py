"""
Ontology backend — Python library wrapping Neo4j.

Not an MCP server. Used internally by mcp-marvin.
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_AUTH = (os.getenv("NEO4J_USER", "neo4j"), os.getenv("NEO4J_PASS", "tautologia"))

_driver = None

# Load relation types from single source of truth
_RELATION_TYPES_PATH = Path(__file__).parent / "relation_types.json"
_RELATION_TYPES_DATA: dict = json.loads(_RELATION_TYPES_PATH.read_text())

RELATION_TYPES: list[str] = list(_RELATION_TYPES_DATA.keys())
SYMMETRIC_TYPES: frozenset[str] = frozenset(
    name for name, meta in _RELATION_TYPES_DATA.items() if meta["symmetric"]
)
RELATION_DESCRIPTIONS: dict[str, str] = {
    name: meta["description"] for name, meta in _RELATION_TYPES_DATA.items()
}

# Cypher fragment for matching any relationship type
_ANY_REL = "|".join(RELATION_TYPES)


def _get_driver():
    global _driver
    if _driver is None:
        _driver = GraphDatabase.driver(NEO4J_URI, auth=NEO4J_AUTH)
    return _driver


def query(text: str, limit: int = 10) -> str:
    """Semantic search over concepts via Milvus. Keyword fallback if Milvus is down."""
    # Primary: semantic search via Milvus
    try:
        import memory
        hits = memory.search_concepts_semantic(text, limit=limit)
        if hits:
            lines = [f"Found {len(hits)} concept(s):\n"]
            for h in hits:
                summary = f" — {h['summary']}" if h.get("summary") else ""
                lines.append(f"- [{h.get('vault', '?')}] {h.get('name', '?')} (score={h['score']:.3f}){summary}")
            return "\n".join(lines)
    except Exception:
        pass

    # Fallback: keyword search in Neo4j
    driver = _get_driver()
    with driver.session() as s:
        result = s.run(
            "MATCH (c:Concept) "
            "WHERE toLower(c.name) CONTAINS toLower($text) "
            "   OR toLower(c.summary) CONTAINS toLower($text) "
            "   OR toLower(c.content) CONTAINS toLower($text) "
            "   OR (c.aliases IS NOT NULL AND any(a IN c.aliases WHERE toLower(a) CONTAINS toLower($text))) "
            "RETURN c.name AS name, c.vault AS vault, c.summary AS summary, "
            "  c.ghost AS ghost, c.aliases AS aliases "
            "ORDER BY CASE "
            "  WHEN toLower(c.name) CONTAINS toLower($text) THEN 0 "
            "  WHEN c.aliases IS NOT NULL AND any(a IN c.aliases WHERE toLower(a) CONTAINS toLower($text)) THEN 1 "
            "  ELSE 2 END, name "
            "LIMIT $limit",
            text=text,
            limit=limit,
        )
        records = list(result)

    if records:
        lines = [f"Found {len(records)} concept(s) (keyword fallback):\n"]
        for r in records:
            ghost = " (ghost)" if r["ghost"] else ""
            summary = f" — {r['summary']}" if r["summary"] else ""
            aliases = f" (aka: {', '.join(r['aliases'])})" if r["aliases"] else ""
            lines.append(f"- [{r['vault']}] {r['name']}{ghost}{aliases}{summary}")
        return "\n".join(lines)

    return f"No concepts found for '{text}'."


def set_aliases(name: str, aliases: list[str]) -> str:
    """Set English aliases for a concept. Enables cross-language search."""
    driver = _get_driver()
    with driver.session() as s:
        node = s.run(
            "MATCH (c:Concept {name: $name}) RETURN c", name=name
        ).single()
        if not node:
            return f"Concept '{name}' not found."
        s.run(
            "MATCH (c:Concept {name: $name}) SET c.aliases = $aliases",
            name=name,
            aliases=aliases,
        )
    return f"Set aliases for '{name}': {', '.join(aliases)}"


def batch_set_aliases(mappings: list[dict]) -> str:
    """Set aliases for multiple concepts at once.

    Args:
        mappings: List of dicts with 'name' and 'aliases' keys.
    """
    driver = _get_driver()
    results = []
    with driver.session() as s:
        for m in mappings:
            name = m["name"]
            aliases = m["aliases"]
            node = s.run(
                "MATCH (c:Concept {name: $name}) RETURN c", name=name
            ).single()
            if not node:
                results.append(f"  ✗ '{name}' not found")
                continue
            s.run(
                "MATCH (c:Concept {name: $name}) SET c.aliases = $aliases",
                name=name,
                aliases=aliases,
            )
            results.append(f"  ✓ '{name}' → {', '.join(aliases)}")
    return f"Processed {len(mappings)} concept(s):\n" + "\n".join(results)


def get_concept(name: str) -> str:
    """Get a concept with its full content and all relations."""
    driver = _get_driver()
    with driver.session() as s:
        node = s.run(
            "MATCH (c:Concept {name: $name}) RETURN c", name=name
        ).single()

        if not node:
            suggestions = s.run(
                "MATCH (c:Concept) WHERE toLower(c.name) CONTAINS toLower($name) "
                "RETURN c.name LIMIT 5",
                name=name,
            )
            names = [r[0] for r in suggestions]
            if names:
                return f"Concept '{name}' not found. Did you mean: {', '.join(names)}?"
            return f"Concept '{name}' not found."

        c = node["c"]
        lines = [
            f"# {c['name']}",
            f"Vault: {c['vault']}",
            f"Ghost: {c['ghost']}",
            f"Summary: {c['summary'] or '(none)'}",
            "",
        ]

        if c["content"]:
            lines.append("## Content")
            lines.append(c["content"][:2000])
            if len(c["content"]) > 2000:
                lines.append(f"\n... ({len(c['content'])} chars total)")
            lines.append("")

        out = list(s.run(
            "MATCH (c:Concept {name: $name})-[r]->(t:Concept) "
            "RETURN t.name AS target, type(r) AS rel_type, "
            "  r.reasoning AS reasoning, r.weight AS weight, "
            "  r.discovered_by AS by "
            "ORDER BY rel_type, target",
            name=name,
        ))
        if out:
            lines.append(f"## Links to ({len(out)})")
            for r in out:
                w = f" (w={r['weight']})" if r["weight"] else ""
                by = f" [{r['by']}]" if r["by"] else ""
                lines.append(f"  —[{r['rel_type']}]→ {r['target']}{w}{by}")

        inc = list(s.run(
            "MATCH (c:Concept {name: $name})<-[r]-(s:Concept) "
            "RETURN s.name AS source, type(r) AS rel_type, "
            "  r.reasoning AS reasoning, r.weight AS weight, "
            "  r.discovered_by AS by "
            "ORDER BY rel_type, source",
            name=name,
        ))
        if inc:
            lines.append(f"\n## Linked from ({len(inc)})")
            for r in inc:
                w = f" (w={r['weight']})" if r["weight"] else ""
                by = f" [{r['by']}]" if r["by"] else ""
                lines.append(f"  ←[{r['rel_type']}]— {r['source']}{w}{by}")

        return "\n".join(lines)


def traverse(name: str, hops: int = 2) -> str:
    """Traverse the graph from a concept, returning its neighborhood."""
    hops = max(1, min(4, hops))
    driver = _get_driver()
    with driver.session() as s:
        node = s.run(
            "MATCH (c:Concept {name: $name}) RETURN c", name=name
        ).single()
        if not node:
            return f"Concept '{name}' not found."

        result = list(s.run(
            f"MATCH path = (c:Concept {{name: $name}})-[:{_ANY_REL}*1..{hops}]-(n:Concept) "
            "WHERE c <> n "
            "RETURN DISTINCT n.name AS name, n.vault AS vault, n.ghost AS ghost, "
            f"  length(shortestPath((c)-[:{_ANY_REL}*]-(n))) AS distance "
            "ORDER BY distance, vault, name",
            name=name,
        ))

    if not result:
        return f"'{name}' has no connections within {hops} hops."

    lines = [f"Neighborhood of '{name}' ({hops} hops, {len(result)} concepts):\n"]
    current_dist = None
    for r in result:
        if r["distance"] != current_dist:
            current_dist = r["distance"]
            lines.append(f"  Hop {current_dist}:")
        ghost = " (ghost)" if r["ghost"] else ""
        lines.append(f"    [{r['vault']}] {r['name']}{ghost}")

    return "\n".join(lines)


def why_exists(name: str) -> str:
    """Explain why a concept exists — shows all edge reasoning."""
    driver = _get_driver()
    with driver.session() as s:
        node = s.run(
            "MATCH (c:Concept {name: $name}) RETURN c", name=name
        ).single()
        if not node:
            return f"Concept '{name}' not found."

        c = node["c"]
        lines = [
            f"# Why '{name}' exists",
            f"Vault: {c['vault']}",
            f"Ghost: {c['ghost']}",
            "",
        ]

        if c["ghost"]:
            lines.append("This is a ghost node — referenced by other concepts but has no note of its own.")
            lines.append("")

        edges = list(s.run(
            "MATCH (c:Concept {name: $name})-[r]-(other:Concept) "
            "RETURN other.name AS other, type(r) AS rel_type, "
            "  r.reasoning AS reasoning, r.discovered_by AS by, "
            "  r.weight AS weight, "
            "  CASE WHEN startNode(r) = c THEN '→' ELSE '←' END AS dir "
            "ORDER BY rel_type, dir, other",
            name=name,
        ))

        if not edges:
            lines.append("No relations found — this concept is isolated.")
        else:
            lines.append(f"Relations ({len(edges)}):\n")
            for e in edges:
                reasoning = e["reasoning"] or "(no reasoning recorded)"
                by = f" [{e['by']}]" if e["by"] else ""
                lines.append(f"  {e['dir']}[{e['rel_type']}] {e['other']}{by}")
                lines.append(f"    {reasoning}")

        return "\n".join(lines)


def expand(
    concept_name: str,
    summary: str = "",
    content: str = "",
    relate_to: str = "",
    reasoning: str = "",
    relation_type: str = "RELATES_TO",
) -> str:
    """Add a new concept or relation to the knowledge graph."""
    driver = _get_driver()
    now = datetime.now(timezone.utc).isoformat()
    actions = []

    with driver.session() as s:
        existing = s.run(
            "MATCH (c:Concept {name: $name}) RETURN c", name=concept_name
        ).single()

        if existing:
            if summary or content:
                updates = []
                params = {"name": concept_name, "now": now}
                if summary:
                    updates.append("c.summary = $summary")
                    params["summary"] = summary
                if content:
                    updates.append("c.content = $content")
                    params["content"] = content
                updates.append("c.updated_at = $now")
                s.run(
                    f"MATCH (c:Concept {{name: $name}}) SET {', '.join(updates)}",
                    **params,
                )
                actions.append(f"Updated concept '{concept_name}'")
            else:
                actions.append(f"Concept '{concept_name}' already exists")
        else:
            s.run(
                "CREATE (c:Concept {name: $name, vault: 'agent', summary: $summary, "
                "  content: $content, ghost: false, created_at: $now, updated_at: $now})",
                name=concept_name,
                summary=summary,
                content=content,
                now=now,
            )
            actions.append(f"Created concept '{concept_name}' (vault: agent)")

        if relate_to:
            # Validate relation type
            rel = relation_type.upper() if relation_type else "RELATES_TO"
            if rel not in RELATION_TYPES:
                rel = "RELATES_TO"

            target = s.run(
                "MATCH (c:Concept {name: $name}) RETURN c", name=relate_to
            ).single()
            if not target:
                s.run(
                    "CREATE (c:Concept {name: $name, vault: 'ghost', summary: '', "
                    "  content: '', ghost: true, created_at: $now, updated_at: $now})",
                    name=relate_to,
                    now=now,
                )
                actions.append(f"Created ghost node '{relate_to}'")

            # Dynamic relationship type via APOC-free pattern:
            # Neo4j MERGE doesn't support parameterized rel types,
            # so we use f-string with validated rel (from RELATION_TYPES whitelist)
            s.run(
                f"MATCH (a:Concept {{name: $source}}) "
                f"MATCH (b:Concept {{name: $target}}) "
                f"MERGE (a)-[r:{rel}]->(b) "
                f"SET r.discovered_by = 'agent', r.weight = 1.0, "
                f"  r.reasoning = $reasoning",
                source=concept_name,
                target=relate_to,
                reasoning=reasoning or f"Agent-discovered relation: {concept_name} —[{rel}]→ {relate_to}",
            )
            actions.append(f"Created relation: {concept_name} —[{rel}]→ {relate_to}")

    return "\n".join(actions)


def auto_link(name: str = "") -> str:
    """Scan concept content for references to other concepts and create links.

    If name is given, only process that concept. Otherwise, process all
    concepts that have zero outgoing edges (isolated nodes).
    """
    driver = _get_driver()
    now = datetime.now(timezone.utc).isoformat()

    with driver.session() as s:
        # Get all concept names for matching
        all_names = [
            r["name"] for r in s.run("MATCH (c:Concept) RETURN c.name AS name")
        ]
        name_set = set(all_names)

        # Get target concepts to process
        if name:
            targets = list(s.run(
                "MATCH (c:Concept {name: $name}) RETURN c.name AS name, c.content AS content",
                name=name,
            ))
            if not targets:
                return f"Concept '{name}' not found."
        else:
            # All concepts with no outgoing edges
            targets = list(s.run(
                "MATCH (c:Concept) "
                "WHERE NOT (c)-[:RELATES_TO]->() "
                "RETURN c.name AS name, c.content AS content"
            ))

        if not targets:
            return "No isolated concepts to process."

        total_links = 0
        results = []

        for t in targets:
            concept_name = t["name"]
            content = (t["content"] or "").lower()
            if not content:
                continue

            links_created = []
            for candidate in all_names:
                if candidate == concept_name:
                    continue
                # Case-insensitive search for concept name in content
                if candidate.lower() in content:
                    # Check edge doesn't already exist
                    existing = s.run(
                        "MATCH (a:Concept {name: $src})-[:RELATES_TO]->(b:Concept {name: $tgt}) "
                        "RETURN count(*) AS n",
                        src=concept_name, tgt=candidate,
                    ).single()["n"]
                    if existing == 0:
                        s.run(
                            "MATCH (a:Concept {name: $src}) "
                            "MATCH (b:Concept {name: $tgt}) "
                            "CREATE (a)-[r:RELATES_TO {discovered_by: 'auto_link', "
                            "  weight: 1.0, reasoning: $reasoning}]->(b)",
                            src=concept_name, tgt=candidate,
                            reasoning=f"Concept '{candidate}' found in content of '{concept_name}'",
                        )
                        links_created.append(candidate)

            if links_created:
                total_links += len(links_created)
                results.append(f"  {concept_name} → {', '.join(links_created)} ({len(links_created)})")

        if not results:
            return f"Processed {len(targets)} concept(s), no new links found."

        header = f"Created {total_links} links from {len(results)} concept(s):\n"
        return header + "\n".join(results)


def ensure_bidirectional(name: str = "") -> str:
    """For every A→B symmetric edge, ensure B→A also exists (same type).

    Only processes symmetric relationship types (RELATES_TO, CONTRADICTS).
    Directional types (IMPLEMENTS, REQUIRES, COMPOSES, etc.)
    are left as-is — A IMPLEMENTS B does not mean B IMPLEMENTS A.

    If name is given, only process edges involving that concept.
    Otherwise, process the entire graph.
    """
    driver = _get_driver()
    sym_cypher = "|".join(SYMMETRIC_TYPES)

    with driver.session() as s:
        if name:
            exists = s.run(
                "MATCH (c:Concept {name: $name}) RETURN c", name=name
            ).single()
            if not exists:
                return f"Concept '{name}' not found."

            missing = list(s.run(
                f"MATCH (a:Concept)-[r:{sym_cypher}]->(b:Concept) "
                "WHERE (a.name = $name OR b.name = $name) "
                "  AND a <> b "
                "WITH a, b, type(r) AS rel_type "
                "WHERE NOT EXISTS { MATCH (b)-[r2]->(a) WHERE type(r2) = rel_type } "
                "RETURN a.name AS src, b.name AS tgt, rel_type",
                name=name,
            ))
        else:
            missing = list(s.run(
                f"MATCH (a:Concept)-[r:{sym_cypher}]->(b:Concept) "
                "WHERE a <> b "
                "WITH a, b, type(r) AS rel_type "
                "WHERE NOT EXISTS { MATCH (b)-[r2]->(a) WHERE type(r2) = rel_type } "
                "RETURN a.name AS src, b.name AS tgt, rel_type"
            ))

        if not missing:
            return "All symmetric edges are already bidirectional."

        created = 0
        for m in missing:
            rel = m["rel_type"]
            s.run(
                f"MATCH (a:Concept {{name: $src}}) "
                f"MATCH (b:Concept {{name: $tgt}}) "
                f"CREATE (b)-[r:{rel} {{discovered_by: 'bidirectional', "
                f"  weight: 1.0, reasoning: $reasoning}}]->(a)",
                src=m["src"], tgt=m["tgt"],
                reasoning=f"Bidirectional completion: {m['src']} —[{rel}]→ {m['tgt']} existed",
            )
            created += 1

        return f"Created {created} reverse edges (symmetric types only)."


def run_cypher(cypher: str) -> str:
    """Run arbitrary Cypher query. Used by Marvin for schema evolution."""
    driver = _get_driver()
    with driver.session() as s:
        result = s.run(cypher)
        records = list(result)
        if not records:
            return "(no results)"
        keys = records[0].keys()
        lines = []
        for rec in records:
            parts = [f"{k}={rec[k]}" for k in keys]
            lines.append("  ".join(parts))
        return "\n".join(lines)


def get_vault_concepts(vault: str) -> list[dict]:
    """Get all concepts from a vault with summaries, content, and outgoing relations."""
    driver = _get_driver()
    with driver.session() as s:
        result = list(s.run(
            "MATCH (c:Concept {vault: $vault}) "
            "OPTIONAL MATCH (c)-[r]->(t:Concept) "
            "WITH c, collect(CASE WHEN t IS NOT NULL "
            "  THEN {target: t.name, type: type(r)} END) AS rels "
            "RETURN c.name AS name, c.summary AS summary, c.content AS content, rels "
            "ORDER BY c.name",
            vault=vault,
        ))

    concepts = []
    for r in result:
        rels = [rel for rel in r["rels"] if rel is not None]
        concepts.append({
            "name": r["name"],
            "summary": r["summary"] or "",
            "content": r["content"] or "",
            "relations": rels,
        })
    return concepts


def list_concepts() -> str:
    """Return all concept names grouped by vault."""
    driver = _get_driver()
    with driver.session() as s:
        result = list(s.run(
            "MATCH (c:Concept) "
            "RETURN c.name AS name, c.vault AS vault "
            "ORDER BY c.vault, c.name"
        ))

    if not result:
        return "No concepts in the graph."

    vaults: dict[str, list[str]] = {}
    for r in result:
        vaults.setdefault(r["vault"], []).append(r["name"])

    lines = [f"{len(result)} concepts:\n"]
    for vault, names in vaults.items():
        lines.append(f"  [{vault}] ({len(names)}): {', '.join(names)}")
    return "\n".join(lines)


def get_stats() -> dict:
    """Return ontology stats as a dict (nodes, edges, ghosts, vaults, agent_edges, edge_types)."""
    driver = _get_driver()
    with driver.session() as s:
        nodes = s.run("MATCH (c:Concept) RETURN count(c) AS n").single()["n"]
        edges = s.run("MATCH ()-[r]->() RETURN count(r) AS n").single()["n"]
        ghosts = s.run("MATCH (c:Concept {ghost: true}) RETURN count(c) AS n").single()["n"]
        vaults = list(s.run(
            "MATCH (c:Concept) RETURN c.vault AS vault, count(*) AS n ORDER BY n DESC"
        ))
        agent_edges = s.run(
            "MATCH ()-[r {discovered_by: 'agent'}]->() RETURN count(r) AS n"
        ).single()["n"]
        edge_types = list(s.run(
            "MATCH ()-[r]->() RETURN type(r) AS rel_type, count(r) AS n ORDER BY n DESC"
        ))
    return {
        "nodes": nodes,
        "edges": edges,
        "ghosts": ghosts,
        "vaults": [(r["vault"], r["n"]) for r in vaults],
        "agent_edges": agent_edges,
        "edge_types": [(r["rel_type"], r["n"]) for r in edge_types],
    }


def get_schema() -> str:
    """Return current Neo4j schema (labels, relationships, constraints, indexes)."""
    driver = _get_driver()
    with driver.session() as s:
        labels = list(s.run("CALL db.labels()"))
        rel_types = list(s.run("CALL db.relationshipTypes()"))
        constraints = list(s.run("SHOW CONSTRAINTS"))
        indexes = list(s.run("SHOW INDEXES"))

    lines = ["# Neo4j Schema\n"]
    lines.append("## Labels")
    for r in labels:
        lines.append(f"  - {r[0]}")
    lines.append("\n## Relationship Types")
    for r in rel_types:
        lines.append(f"  - {r[0]}")
    lines.append(f"\n## Constraints ({len(constraints)})")
    for r in constraints:
        lines.append(f"  - {r['name']}: {r['type']} on {r['labelsOrTypes']} {r['properties']}")
    lines.append(f"\n## Indexes ({len(indexes)})")
    for r in indexes:
        lines.append(f"  - {r['name']}: {r['type']} on {r['labelsOrTypes']} {r['properties']}")
    return "\n".join(lines)
