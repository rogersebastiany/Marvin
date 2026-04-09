"""
Load all knowledge sources into Neo4j as a knowledge graph.

Sources:
  1. Obsidian thesis vault     → vault="thesis"
  2. Obsidian implementation vault → vault="implementation"
  3. docs/ (fetched documentation) → vault="docs"
  4. diagrams/ (.mmd files)     → vault="diagrams"

Schema:
  - Nodes: :Concept {name, vault, summary, content, ghost, created_at, updated_at}
  - Edges: :RELATES_TO {type, weight, reasoning, discovered_by}

Behavior:
  - Uses MERGE, not DELETE — agent-discovered concepts/relations survive re-runs.
  - Vault-sourced nodes get updated content on re-run (vault wins for its own nodes).
  - Nodes with vault="agent" are NEVER touched — they belong to the agent.
"""

import os
import re
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASS = os.getenv("NEO4J_PASS", "tautologia")

ROOT = Path(__file__).parent.parent

VAULTS = {
    "thesis": ROOT / "obsidian-vault-tautologia-ontologica" / "obsidian-vault",
    "implementation": ROOT / "vault",
}

DOCS_DIR = ROOT / "mcp-server-poc" / "docs"
DIAGRAMS_DIR = ROOT / "mcp-server-poc" / "diagrams"

# Skip non-concept directories inside vaults
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
            return WIKILINK_RE.sub(lambda m: m.group(1), line)[:300]
    return ""


def load_vault(vault_name: str, vault_path: Path) -> tuple[list[dict], list[dict]]:
    """Parse an Obsidian vault into concepts and edges."""
    concepts = []
    edges = []

    if not vault_path.exists():
        print(f"  WARNING: vault path does not exist: {vault_path}")
        return concepts, edges

    for md_file in sorted(vault_path.glob("*.md")):
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


def load_docs(docs_dir: Path) -> list[dict]:
    """Parse docs/ markdown files into concepts (no wikilinks)."""
    concepts = []

    if not docs_dir.exists():
        print(f"  WARNING: docs path does not exist: {docs_dir}")
        return concepts

    for md_file in sorted(docs_dir.glob("*.md")):
        name = md_file.stem
        content = md_file.read_text(encoding="utf-8")
        summary = extract_summary(content)

        concepts.append({
            "name": name,
            "vault": "docs",
            "summary": summary,
            "content": content,
            "ghost": False,
        })

    return concepts


def load_diagrams(diagrams_dir: Path) -> list[dict]:
    """Parse diagrams/ .mmd files into concepts."""
    concepts = []

    if not diagrams_dir.exists():
        print(f"  WARNING: diagrams path does not exist: {diagrams_dir}")
        return concepts

    for mmd_file in sorted(diagrams_dir.glob("*.mmd")):
        name = mmd_file.stem
        content = mmd_file.read_text(encoding="utf-8")

        concepts.append({
            "name": name,
            "vault": "diagrams",
            "summary": f"Mermaid diagram: {name}",
            "content": content,
            "ghost": False,
        })

    return concepts


def merge_concepts(all_concepts: list[dict]) -> list[dict]:
    """Merge concepts that appear in multiple vaults."""
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
    """Load everything into Neo4j using MERGE (non-destructive)."""
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASS))
    now = datetime.now(timezone.utc).isoformat()

    with driver.session() as session:
        # Create constraints
        session.run(
            "CREATE CONSTRAINT concept_name IF NOT EXISTS "
            "FOR (c:Concept) REQUIRE c.name IS UNIQUE"
        )

        # MERGE concepts — only update non-agent nodes
        created = 0
        updated = 0
        skipped = 0
        for c in concepts:
            result = session.run(
                "MATCH (c:Concept {name: $name}) RETURN c.vault AS vault",
                name=c["name"],
            ).single()

            if result and result["vault"] == "agent":
                # Never overwrite agent-created concepts
                skipped += 1
                continue

            if result:
                # Update existing vault-sourced concept
                session.run(
                    """
                    MATCH (c:Concept {name: $name})
                    SET c.vault = $vault,
                        c.summary = $summary,
                        c.content = $content,
                        c.ghost = $ghost,
                        c.updated_at = $now
                    """,
                    name=c["name"],
                    vault=c["vault"],
                    summary=c["summary"],
                    content=c["content"],
                    ghost=c["ghost"],
                    now=now,
                )
                updated += 1
            else:
                # Create new concept
                session.run(
                    """
                    CREATE (c:Concept {
                        name: $name, vault: $vault, summary: $summary,
                        content: $content, ghost: $ghost,
                        created_at: $now, updated_at: $now
                    })
                    """,
                    name=c["name"],
                    vault=c["vault"],
                    summary=c["summary"],
                    content=c["content"],
                    ghost=c["ghost"],
                    now=now,
                )
                created += 1

        real = sum(1 for c in concepts if not c["ghost"])
        ghost = sum(1 for c in concepts if c["ghost"])
        print(f"Concepts: {created} created, {updated} updated, {skipped} skipped (agent-owned)")
        print(f"  {real} real + {ghost} ghost = {len(concepts)} total from sources")

        # MERGE edges — only for vault-sourced edges (don't touch agent edges)
        edge_count = 0
        for e in edges:
            result = session.run(
                """
                MATCH (a:Concept {name: $source})
                MATCH (b:Concept {name: $target})
                MERGE (a)-[r:RELATES_TO]->(b)
                ON CREATE SET r.discovered_by = 'vault_import',
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

        print(f"Edges: {edge_count} merged (vault-sourced)")

        # Stats
        result = session.run(
            "MATCH (c:Concept) RETURN c.vault AS vault, count(*) AS n ORDER BY vault"
        )
        print("\nBy vault:")
        for record in result:
            print(f"  {record['vault']}: {record['n']}")

        total_edges = session.run(
            "MATCH ()-[r:RELATES_TO]->() RETURN count(r) AS n"
        ).single()["n"]
        agent_edges = session.run(
            "MATCH ()-[r:RELATES_TO]->() WHERE r.discovered_by = 'agent' RETURN count(r) AS n"
        ).single()["n"]
        print(f"\nTotal edges: {total_edges} ({agent_edges} agent-discovered)")

    driver.close()
    print("\nDone.")


def main():
    all_concepts = []
    all_edges = []

    # 1. Obsidian vaults
    for vault_name, vault_path in VAULTS.items():
        print(f"Loading {vault_name} vault: {vault_path}")
        concepts, edges = load_vault(vault_name, vault_path)
        print(f"  {len(concepts)} notes, {len(edges)} links")
        all_concepts.extend(concepts)
        all_edges.extend(edges)

    # 2. docs/
    print(f"Loading docs: {DOCS_DIR}")
    docs = load_docs(DOCS_DIR)
    print(f"  {len(docs)} documents")
    all_concepts.extend(docs)

    # 3. diagrams/
    print(f"Loading diagrams: {DIAGRAMS_DIR}")
    diagrams = load_diagrams(DIAGRAMS_DIR)
    print(f"  {len(diagrams)} diagrams")
    all_concepts.extend(diagrams)

    # Merge duplicates across vaults
    merged = merge_concepts(all_concepts)
    print(f"\nAfter merge: {len(merged)} unique concepts")

    # Find ghost nodes (from wikilinks pointing to non-existent notes)
    ghosts = find_ghost_nodes(merged, all_edges)
    merged.extend(ghosts)
    print(f"Ghost nodes: {len(ghosts)}")

    # Load into Neo4j
    print(f"\nLoading into Neo4j at {NEO4J_URI}...")
    load_to_neo4j(merged, all_edges)


if __name__ == "__main__":
    main()
