"""
Load both Obsidian vaults into Neo4j as a knowledge graph.

Schema:
  - Nodes: :Concept {name, vault, summary, content, ghost, created_at, updated_at}
  - Edges: :RELATES_TO {type, weight, reasoning, discovered_by}

This script is disposable — once the vaults are loaded, the mcp-ontology-server
manages the graph.
"""

import re
import os
from datetime import datetime, timezone
from pathlib import Path
from neo4j import GraphDatabase

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASS = "tautologia"

VAULTS = {
    "thesis": Path(__file__).parent.parent / "obsidian-vault-tautologia-ontologica" / "obsidian-vault",
    "implementation": Path(__file__).parent.parent / "vault",
}

# Skip non-concept files
SKIP_DIRS = {".obsidian", "poc docs", "diagrams", "docs"}

WIKILINK_RE = re.compile(r"\[\[([^\]|\\]+)(?:\\?\|[^\]]+)?\]\]")


def extract_wikilinks(content: str) -> list[str]:
    """Extract all wikilink targets from markdown content."""
    return list(set(WIKILINK_RE.findall(content)))


def extract_summary(content: str) -> str:
    """First non-empty, non-heading line as summary."""
    for line in content.split("\n"):
        line = line.strip()
        if line and not line.startswith("#") and line != "---":
            # Strip wikilinks for summary
            return WIKILINK_RE.sub(lambda m: m.group(1), line)[:300]
    return ""


def load_vault(vault_name: str, vault_path: Path) -> tuple[list[dict], list[dict]]:
    """Parse a vault into concepts and edges."""
    concepts = []
    edges = []

    for md_file in sorted(vault_path.glob("*.md")):
        # Skip dotfiles and non-concept dirs
        if any(part in SKIP_DIRS for part in md_file.parts):
            continue

        name = md_file.stem
        content = md_file.read_text(encoding="utf-8")
        summary = extract_summary(content)
        links = extract_wikilinks(content)

        concepts.append({
            "name": name,
            "vault": vault_name,
            "summary": summary,
            "content": content,
            "ghost": False,
        })

        for target in links:
            edges.append({
                "source": name,
                "target": target,
                "vault": vault_name,
            })

    return concepts, edges


def merge_concepts(all_concepts: list[dict]) -> list[dict]:
    """Merge concepts that appear in both vaults."""
    by_name: dict[str, dict] = {}

    for c in all_concepts:
        name = c["name"]
        if name in by_name:
            existing = by_name[name]
            existing["vault"] = "both"
            existing["content"] += f"\n\n---\n\n<!-- From {c['vault']} vault -->\n\n{c['content']}"
            if not existing["summary"]:
                existing["summary"] = c["summary"]
        else:
            by_name[name] = c.copy()

    return list(by_name.values())


def find_ghost_nodes(concepts: list[dict], edges: list[dict]) -> list[dict]:
    """Find referenced concepts that don't have their own note."""
    known = {c["name"] for c in concepts}
    ghosts = set()

    for e in edges:
        if e["target"] not in known and e["target"] not in ghosts:
            ghosts.add(e["target"])

    return [
        {"name": name, "vault": "ghost", "summary": "", "content": "", "ghost": True}
        for name in sorted(ghosts)
    ]


def load_to_neo4j(concepts: list[dict], edges: list[dict]):
    """Load everything into Neo4j."""
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASS))
    now = datetime.now(timezone.utc).isoformat()

    with driver.session() as session:
        # Clear existing data
        session.run("MATCH (n) DETACH DELETE n")
        print("Cleared existing graph.")

        # Create constraints
        session.run(
            "CREATE CONSTRAINT concept_name IF NOT EXISTS "
            "FOR (c:Concept) REQUIRE c.name IS UNIQUE"
        )

        # Create concepts
        for c in concepts:
            session.run(
                """
                MERGE (c:Concept {name: $name})
                SET c.vault = $vault,
                    c.summary = $summary,
                    c.content = $content,
                    c.ghost = $ghost,
                    c.created_at = $now,
                    c.updated_at = $now
                """,
                name=c["name"],
                vault=c["vault"],
                summary=c["summary"],
                content=c["content"],
                ghost=c["ghost"],
                now=now,
            )

        real = sum(1 for c in concepts if not c["ghost"])
        ghost = sum(1 for c in concepts if c["ghost"])
        print(f"Created {real} concepts + {ghost} ghost nodes = {len(concepts)} total.")

        # Create edges
        edge_count = 0
        for e in edges:
            result = session.run(
                """
                MATCH (a:Concept {name: $source})
                MATCH (b:Concept {name: $target})
                MERGE (a)-[r:RELATES_TO]->(b)
                SET r.discovered_by = 'vault_import',
                    r.weight = 1.0,
                    r.reasoning = $reasoning
                RETURN r
                """,
                source=e["source"],
                target=e["target"],
                reasoning=f"Wikilink in {e['vault']} vault: [[{e['target']}]]",
            )
            if result.single():
                edge_count += 1

        print(f"Created {edge_count} edges.")

        # Stats
        result = session.run(
            "MATCH (c:Concept) RETURN c.vault AS vault, count(*) AS n ORDER BY vault"
        )
        print("\nBy vault:")
        for record in result:
            print(f"  {record['vault']}: {record['n']}")

        result = session.run(
            "MATCH (c:Concept) WHERE c.ghost = true "
            "RETURN c.name AS name ORDER BY name"
        )
        ghosts = [r["name"] for r in result]
        if ghosts:
            print(f"\nGhost nodes ({len(ghosts)}):")
            for g in ghosts:
                print(f"  - {g}")

    driver.close()
    print("\nDone.")


def main():
    all_concepts = []
    all_edges = []

    for vault_name, vault_path in VAULTS.items():
        print(f"Parsing {vault_name} vault: {vault_path}")
        concepts, edges = load_vault(vault_name, vault_path)
        print(f"  {len(concepts)} notes, {len(edges)} links")
        all_concepts.extend(concepts)
        all_edges.extend(edges)

    # Merge duplicates
    merged = merge_concepts(all_concepts)
    print(f"\nAfter merge: {len(merged)} unique concepts")

    # Find ghost nodes
    ghosts = find_ghost_nodes(merged, all_edges)
    merged.extend(ghosts)
    print(f"Ghost nodes: {len(ghosts)}")

    # Load
    print(f"\nLoading into Neo4j at {NEO4J_URI}...")
    load_to_neo4j(merged, all_edges)


if __name__ == "__main__":
    main()
