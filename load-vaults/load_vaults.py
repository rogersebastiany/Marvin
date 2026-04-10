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
import sys
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from neo4j import GraphDatabase

# Import relationship type definitions from ontology backend
sys.path.insert(0, str(Path(__file__).parent.parent / "mcp-server"))
from ontology import RELATION_TYPES, SYMMETRIC_TYPES

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASS = os.getenv("NEO4J_PASS", "tautologia")

ROOT = Path(__file__).parent.parent

VAULTS = {
    "thesis": ROOT / "obsidian-vault-tautologia-ontologica" / "obsidian-vault",
    "implementation": ROOT / "vault",
    "thesis-en": ROOT / "vault-thesis-en",
    "implementation-en": ROOT / "vault-implementation-en",
}

DOCS_DIR = ROOT / "mcp-server" / "docs"
DIAGRAMS_DIR = ROOT / "mcp-server" / "diagrams"

# English → Portuguese name mapping for cross-language vault merging.
# English vault concepts get merged INTO the Portuguese concept (same node).
# The English name becomes an alias on the Portuguese node — one concept, two names.
EN_TO_PT: dict[str, str] = {
    # thesis vault
    "Agent": "Agente",
    "Architectural Enforcement": "Enforcement Arquitetural",
    "Cognitive Accumulation": "Acumulação Cognitiva",
    "Complete Directed Graph": "Grafo Dirigido Completo",
    "Conditional Probability": "Probabilidade Condicional",
    "Context": "Contexto",
    "Convergence": "Convergência",
    "Deduction": "Dedução",
    "Determinism": "Determinismo",
    "Dimensionality Reduction": "Redução de Dimensionalidade",
    "Divergence": "Divergência",
    "Hallucination": "Alucinação",
    "Inference": "Inferência",
    "Linear Algebra": "Álgebra Linear",
    "Linear Relationship": "Relação Linear",
    "Matrix M": "Matriz M",
    "Neural Network": "Rede Neural",
    "Non-Linear Relationship": "Relação Não-Linear",
    "Ontological Tautology": "Tautologia Ontológica",
    "Ontology": "Ontologia",
    "Sample Space": "Espaço Amostral",
    "Set": "Conjunto",
    "Set Theory": "Teoria dos Conjuntos",
    "Subset": "Subconjunto",
    "Tautological Tool": "Tool Tautológica",
    "Tautology": "Tautologia",
    "Tokenization": "Tokenização",
    "Vector": "Vetor",
    # implementation vault
    "Agent in POC": "Agente na POC",
    "Anti-Hallucination": "Anti-Alucinação",
    "Deterministic Feedback Loop": "Feedback Loop Determinístico",
    "Diagram Scoring": "Scoring de Diagramas",
    "HTML to Markdown": "HTML para Markdown",
    "Implicit RAG": "RAG Implícito",
    "MCP Primitives": "Primitivas MCP",
    "Measurable Determinism": "Determinismo Mensurável",
    "Ontological Tautology — Thesis and Proof": "Tautologia Ontológica — Tese e Prova",
    "Ontology as Code": "Ontologia como Código",
    "Production Architecture": "Arquitetura de Produção",
    "Programmatic Context": "Contexto Programático",
    "ReAct in POC": "ReAct na POC",
    "S3 as Persistent Ontology": "S3 como Ontologia Persistente",
    "Self-Improvement Loop": "Loop de Auto-Melhoria",
    "Server Chain": "Cadeia de Servers",
    "Space Reduction in Practice": "Redução de Espaço na Prática",
    "Three Security Layers": "Três Camadas de Segurança",
    "Tool as Bias": "Tool como Bias",
    "Tool Catalog": "Catálogo de Tools",
}

# Reverse: Portuguese name → English alias
PT_TO_EN: dict[str, str] = {v: k for k, v in EN_TO_PT.items()}

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


def load_docs(docs_dir: Path, min_chars: int = 200) -> list[dict]:
    """Parse docs/ markdown files into concepts (no wikilinks).

    Skips files smaller than min_chars (likely JS redirects or empty fetches).
    """
    concepts = []
    skipped = []

    if not docs_dir.exists():
        print(f"  WARNING: docs path does not exist: {docs_dir}")
        return concepts

    for md_file in sorted(docs_dir.glob("*.md")):
        name = md_file.stem
        content = md_file.read_text(encoding="utf-8")

        if len(content) < min_chars:
            skipped.append(f"{name} ({len(content)} chars)")
            continue

        summary = extract_summary(content)

        concepts.append({
            "name": name,
            "vault": "docs",
            "summary": summary,
            "content": content,
            "ghost": False,
        })

    if skipped:
        print(f"  Skipped {len(skipped)} too-small files: {', '.join(skipped)}")

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
    """Merge concepts that appear in multiple vaults.

    English vaults (thesis-en, implementation-en) merge INTO the Portuguese
    concept using EN_TO_PT mapping. If no mapping exists, falls back to
    exact name match. English content is appended with a separator.
    """
    by_name: dict[str, dict] = {}

    for c in all_concepts:
        name = c["name"]
        vault = c["vault"]

        # For English vault concepts, resolve to the Portuguese name
        merge_key = name
        if vault.endswith("-en"):
            merge_key = EN_TO_PT.get(name, name)

        if merge_key in by_name:
            existing = by_name[merge_key]
            if vault.endswith("-en"):
                existing["content"] += f"\n\n---\n\n<!-- English translation -->\n\n{c['content']}"
            else:
                existing["vault"] = "both"
                existing["content"] += f"\n\n---\n\n<!-- From {vault} vault -->\n\n{c['content']}"
            if not existing["summary"]:
                existing["summary"] = c["summary"]
        else:
            c = c.copy()
            if vault.endswith("-en"):
                c["vault"] = vault.removesuffix("-en")
                # Store under the Portuguese name so future merges find it
                c["name"] = merge_key
            by_name[merge_key] = c

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


def _get_driver():
    return GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASS))


def auto_link_all(driver):
    """Scan ALL concept content for references to other concept names and create edges.

    Unlike the MCP tool version (which only processes isolated nodes),
    this processes every concept to maximize cross-vault connectivity.
    """
    with driver.session() as s:
        all_names = [
            r["name"] for r in s.run("MATCH (c:Concept) RETURN c.name AS name")
        ]
        # Pre-filter: skip very short names (≤2 chars) to avoid false positives
        linkable_names = [n for n in all_names if len(n) > 2]

        # Get ALL concepts with content
        targets = list(s.run(
            "MATCH (c:Concept) "
            "WHERE c.content IS NOT NULL AND size(c.content) > 10 "
            "RETURN c.name AS name, c.content AS content"
        ))

        if not targets:
            print("Auto-link: no concepts with content to process.")
            return

        # Pre-fetch all existing edges (any type) to avoid N queries
        existing_edges = set()
        for r in s.run(
            "MATCH (a:Concept)-[]->(b:Concept) "
            "RETURN a.name AS src, b.name AS tgt"
        ):
            existing_edges.add((r["src"], r["tgt"]))

        total_links = 0
        new_edges = []
        for t in targets:
            concept_name = t["name"]
            content = (t["content"] or "").lower()

            for candidate in linkable_names:
                if candidate == concept_name:
                    continue
                if (concept_name, candidate) in existing_edges:
                    continue
                if candidate.lower() in content:
                    new_edges.append((concept_name, candidate))
                    existing_edges.add((concept_name, candidate))

        # Batch create edges
        if new_edges:
            for src, tgt in new_edges:
                s.run(
                    "MATCH (a:Concept {name: $src}) "
                    "MATCH (b:Concept {name: $tgt}) "
                    "CREATE (a)-[r:RELATES_TO {discovered_by: 'auto_link', "
                    "  weight: 1.0, reasoning: $reasoning}]->(b)",
                    src=src, tgt=tgt,
                    reasoning=f"Concept '{tgt}' found in content of '{src}'",
                )
            total_links = len(new_edges)

        print(f"Auto-link: created {total_links} links from {len(targets)} concept(s)")


def ensure_bidirectional_all(driver):
    """For every A→B symmetric edge, ensure B→A also exists (same type).

    Only processes symmetric types (RELATES_TO, TRANSLATES_TO, CONTRADICTS).
    Directional types are left as-is.
    """
    sym_cypher = "|".join(SYMMETRIC_TYPES)

    with driver.session() as s:
        missing = list(s.run(
            f"MATCH (a:Concept)-[r:{sym_cypher}]->(b:Concept) "
            "WHERE a <> b "
            "WITH a, b, type(r) AS rel_type "
            "WHERE NOT EXISTS { MATCH (b)-[r2]->(a) WHERE type(r2) = rel_type } "
            "RETURN a.name AS src, b.name AS tgt, rel_type"
        ))

        if not missing:
            print("Bidirectional: all symmetric edges already bidirectional.")
            return

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

        print(f"Bidirectional: created {len(missing)} reverse edges (symmetric types only).")


def load_to_neo4j(concepts: list[dict], edges: list[dict]):
    """Load everything into Neo4j using MERGE (non-destructive)."""
    driver = _get_driver()
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

        # Set English aliases on Portuguese concepts
        alias_count = 0
        for pt_name, en_name in PT_TO_EN.items():
            session.run(
                "MATCH (c:Concept {name: $name}) SET c.aliases = [$alias]",
                name=pt_name,
                alias=en_name,
            )
            alias_count += 1
        print(f"Aliases: set {alias_count} EN aliases on PT concepts")

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
            "MATCH ()-[r]->() RETURN count(r) AS n"
        ).single()["n"]
        agent_edges = session.run(
            "MATCH ()-[r]->() WHERE r.discovered_by = 'agent' RETURN count(r) AS n"
        ).single()["n"]
        edge_types = list(session.run(
            "MATCH ()-[r]->() RETURN type(r) AS t, count(r) AS n ORDER BY n DESC"
        ))
        print(f"\nTotal edges: {total_edges} ({agent_edges} agent-discovered)")
        if edge_types:
            print("By type:")
            for et in edge_types:
                print(f"  {et['t']}: {et['n']}")

    driver.close()
    print("\nDone.")


def index_to_milvus(merged_concepts: list[dict]):
    """Index docs and concepts into Milvus for semantic search.

    Indexes vault-sourced concepts from the merge + agent-owned concepts
    from Neo4j (since those aren't in the vault files).
    """
    # Import from mcp-server
    sys.path.insert(0, str(Path(__file__).parent.parent / "mcp-server"))
    import memory

    # 1. Index doc chunks
    print(f"\nIndexing docs into Milvus (doc_chunks)...")
    result = memory.index_docs(str(DOCS_DIR))
    print(f"  {result}")

    # 2. Collect ALL concepts: vault-sourced + agent-owned from Neo4j
    indexable = [
        c for c in merged_concepts
        if not c.get("ghost") and len(c.get("content", "")) > 50
    ]

    # Also pull agent-owned concepts from Neo4j
    driver = _get_driver()
    with driver.session() as s:
        agent_concepts = list(s.run(
            "MATCH (c:Concept) WHERE c.vault = 'agent' "
            "AND c.content IS NOT NULL AND size(c.content) > 50 "
            "RETURN c.name AS name, c.vault AS vault, "
            "c.summary AS summary, c.content AS content"
        ))
        for r in agent_concepts:
            indexable.append({
                "name": r["name"],
                "vault": r["vault"],
                "summary": r["summary"] or "",
                "content": r["content"] or "",
            })
    driver.close()

    print(f"Indexing concepts into Milvus (concepts)...")
    print(f"  {len(indexable)} concepts ({len(agent_concepts)} agent-owned)")
    result = memory.index_concepts(indexable)
    print(f"  {result}")


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

    # Remap English edges to Portuguese concept names
    remapped = 0
    for e in all_edges:
        if e["vault"].endswith("-en"):
            old_src, old_tgt = e["source"], e["target"]
            e["source"] = EN_TO_PT.get(e["source"], e["source"])
            e["target"] = EN_TO_PT.get(e["target"], e["target"])
            if e["source"] != old_src or e["target"] != old_tgt:
                remapped += 1
    print(f"Remapped {remapped} English edges to Portuguese concept names")

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

    # Auto-link isolated concepts by scanning content
    print("\nAuto-linking isolated concepts...")
    driver = _get_driver()
    auto_link_all(driver)

    # Ensure all edges are bidirectional
    print("Ensuring bidirectionality...")
    ensure_bidirectional_all(driver)
    driver.close()

    # Index into Milvus for semantic search
    index_to_milvus(merged)


if __name__ == "__main__":
    main()
