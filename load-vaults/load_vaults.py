"""
Load all knowledge sources into Neo4j as a knowledge graph.

Sources:
  1. Obsidian thesis vault     → vault="thesis"
  2. Obsidian implementation vault → vault="implementation"
  3. docs/ (fetched documentation) → vault="docs"
  4. diagrams/ (.mmd files)     → vault="diagrams"

Schema:
  - Nodes: :Concept {name, vault, summary, content, ghost, created_at, updated_at}
  - Edges: Typed from relation_types.json {weight, reasoning, discovered_by}

Pipeline:
  1. Parse — Obsidian vaults, docs, diagrams → concepts + edges with context
  2. Classify — OpenAI classifies edge types from sentence context (can be skipped)
  3. Load — MERGE into Neo4j with pre-typed edges

Behavior:
  - Uses MERGE, not DELETE — agent-discovered concepts/relations survive re-runs.
  - Vault-sourced nodes get updated content on re-run (vault wins for its own nodes).
  - Nodes with vault="agent" are NEVER touched — they belong to the agent.
  - Edge types loaded from mcp-server/relation_types.json (single source of truth).
"""

import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import openai
from dotenv import load_dotenv
from neo4j import GraphDatabase

# Import relationship type definitions from ontology backend
sys.path.insert(0, str(Path(__file__).parent.parent / "mcp-server"))
from ontology import RELATION_DESCRIPTIONS, RELATION_TYPES, SYMMETRIC_TYPES

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

# Sentence-level regex: split on period, colon, or newline boundaries
_SENTENCE_RE = re.compile(r"[.!?\n]")


def extract_wikilinks(content: str) -> list[str]:
    """Extract all wikilink targets from markdown content."""
    return list(set(WIKILINK_RE.findall(content)))


def extract_wikilinks_with_context(content: str) -> list[dict]:
    """Extract wikilinks with the sentence they appear in.

    Returns list of {target, context} where context is the surrounding sentence.
    Deduplicates by target — keeps the richest context sentence.
    """
    results: dict[str, str] = {}
    for match in WIKILINK_RE.finditer(content):
        target = match.group(1)
        # Find sentence boundaries around the match
        start = content.rfind("\n", 0, match.start())
        if start == -1:
            start = 0
        end = content.find("\n", match.end())
        if end == -1:
            end = len(content)
        sentence = content[start:end].strip()
        # Strip markdown formatting for cleaner context
        sentence = WIKILINK_RE.sub(lambda m: m.group(1), sentence)
        sentence = sentence.lstrip("#- ").strip()
        # Keep the longest/richest context per target
        if target not in results or len(sentence) > len(results[target]):
            results[target] = sentence[:500]
    return [{"target": t, "context": c} for t, c in results.items()]


def _build_classifier_prompt() -> str:
    """Build the classifier prompt from relation_types.json descriptions."""
    type_lines = "\n".join(f"- {name}: {desc}" for name, desc in RELATION_DESCRIPTIONS.items())
    return f"""Classify the relationship between two concepts based on context.

Edge types:
{type_lines}

Respond with ONLY the edge type name. If the context is a bare list ("Relaciona-se com: ...") or too vague to determine a specific type, respond RELATES_TO."""


_BARE_LIST_RE = re.compile(r"^(Relaciona-se com|Related to)\s*:", re.IGNORECASE)


def classify_edges(edges: list[dict], batch_size: int = 50, summaries: dict[str, str] | None = None) -> list[dict]:
    """Classify edge types using OpenAI. Mutates edges in-place, adding rel_type field.

    Args:
        edges: list of {source, target, context, vault, ...}
        batch_size: edges per API call (batched as multi-line prompt)
        summaries: optional {concept_name: summary} for enriching bare-list contexts

    Returns the same list with rel_type added to each edge.
    """
    client = openai.OpenAI()
    valid_types = set(RELATION_TYPES)
    type_names = ", ".join(RELATION_TYPES)
    summaries = summaries or {}

    # Build rules from descriptions
    rules = "\n".join(f"- {name}: {desc}" for name, desc in RELATION_DESCRIPTIONS.items())

    classified = 0
    for i in range(0, len(edges), batch_size):
        batch = edges[i : i + batch_size]

        lines = []
        for j, e in enumerate(batch):
            ctx = e["context"][:200]
            # Enrich bare-list contexts with concept summaries
            if _BARE_LIST_RE.match(ctx) or len(ctx.strip()) < 20:
                src_sum = summaries.get(e["source"], "")
                tgt_sum = summaries.get(e["target"], "")
                if src_sum or tgt_sum:
                    ctx = f"[Source: {src_sum[:150]}] [Target: {tgt_sum[:150]}]"
            lines.append(f"{j}. Source: {e['source']} | Target: {e['target']} | Context: {ctx}")

        prompt = f"""Classify each relationship. For each line, respond with ONLY the number and edge type, one per line.

Edge types: {type_names}

Rules:
{rules}

Use RELATES_TO only when no other type fits.

Edges:
{chr(10).join(lines)}"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=batch_size * 10,
        )

        # Parse response lines
        type_map = {}
        for line in response.choices[0].message.content.strip().split("\n"):
            line = line.strip()
            if not line:
                continue
            parts = line.split(".", 1)
            if len(parts) == 2:
                try:
                    idx = int(parts[0].strip())
                    edge_type = parts[1].strip().upper().replace(" ", "")
                    if edge_type in valid_types:
                        type_map[idx] = edge_type
                except (ValueError, IndexError):
                    pass

        for j, e in enumerate(batch):
            e["rel_type"] = type_map.get(j, "RELATES_TO")
            classified += 1

    # Summary
    type_counts: dict[str, int] = {}
    for e in edges:
        t = e["rel_type"]
        type_counts[t] = type_counts.get(t, 0) + 1
    print(f"  Classified {classified} edges: {type_counts}")

    return edges


def extract_summary(content: str) -> str:
    """First non-empty, non-heading line as summary."""
    for line in content.split("\n"):
        line = line.strip()
        if line and not line.startswith("#") and line != "---":
            return WIKILINK_RE.sub(lambda m: m.group(1), line)[:300]
    return ""


def load_vault(vault_name: str, vault_path: Path) -> tuple[list[dict], list[dict]]:
    """Parse an Obsidian vault into concepts and edges with context."""
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
        links_with_ctx = extract_wikilinks_with_context(content)

        concepts.append({
            "name": name,
            "vault": vault_name,
            "summary": summary,
            "content": content,
            "ghost": False,
        })

        for link in links_with_ctx:
            edges.append({
                "source": name,
                "target": link["target"],
                "context": link["context"],
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
    """Scan ALL concept content for references to other concept names and create typed edges.

    Unlike the MCP tool version (which only processes isolated nodes),
    this processes every concept to maximize cross-vault connectivity.
    Edges are classified via OpenAI using the surrounding sentence as context.
    """
    with driver.session() as s:
        all_names = [
            r["name"] for r in s.run("MATCH (c:Concept) RETURN c.name AS name")
        ]
        # Pre-filter: skip very short names (≤2 chars) to avoid false positives
        linkable_names = [n for n in all_names if len(n) > 2]

        # Get ALL concepts with content + summaries
        targets = list(s.run(
            "MATCH (c:Concept) "
            "WHERE c.content IS NOT NULL AND size(c.content) > 10 "
            "RETURN c.name AS name, c.content AS content, c.summary AS summary"
        ))
        summaries = {t["name"]: t["summary"] or "" for t in targets}

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

        new_edges = []
        for t in targets:
            concept_name = t["name"]
            content_raw = t["content"] or ""
            content_lower = content_raw.lower()

            for candidate in linkable_names:
                if candidate == concept_name:
                    continue
                if (concept_name, candidate) in existing_edges:
                    continue
                pos = content_lower.find(candidate.lower())
                if pos >= 0:
                    # Extract sentence context around the match
                    start = content_raw.rfind("\n", 0, pos)
                    start = 0 if start == -1 else start
                    end = content_raw.find("\n", pos + len(candidate))
                    end = len(content_raw) if end == -1 else end
                    context = content_raw[start:end].strip()[:500]

                    new_edges.append({
                        "source": concept_name,
                        "target": candidate,
                        "context": context,
                        "vault": "auto_link",
                    })
                    existing_edges.add((concept_name, candidate))

        if not new_edges:
            print("Auto-link: no new links found.")
            return

        # Classify then create
        print(f"Auto-link: classifying {len(new_edges)} new edges...")
        classify_edges(new_edges, summaries=summaries)

        for e in new_edges:
            rel_type = e.get("rel_type", "RELATES_TO")
            if rel_type not in RELATION_TYPES:
                rel_type = "RELATES_TO"
            s.run(
                f"MATCH (a:Concept {{name: $src}}) "
                f"MATCH (b:Concept {{name: $tgt}}) "
                f"CREATE (a)-[r:{rel_type} {{discovered_by: 'auto_link', "
                f"  weight: 1.0, reasoning: $reasoning}}]->(b)",
                src=e["source"], tgt=e["target"],
                reasoning=f"Concept '{e['target']}' found in content of '{e['source']}'",
            )

        print(f"Auto-link: created {len(new_edges)} typed links from {len(targets)} concept(s)")


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

        # MERGE edges with pre-classified types (don't touch agent edges)
        edge_count = 0
        for e in edges:
            rel_type = e.get("rel_type", "RELATES_TO")
            if rel_type not in RELATION_TYPES:
                rel_type = "RELATES_TO"

            # Delete old RELATES_TO if we're upgrading to a typed edge
            if rel_type != "RELATES_TO":
                session.run(
                    "MATCH (a:Concept {name: $source})-[r:RELATES_TO]->(b:Concept {name: $target}) "
                    "WHERE r.discovered_by = 'vault_import' "
                    "DELETE r",
                    source=e["source"],
                    target=e["target"],
                )

            # Neo4j doesn't allow parameterized relationship types in MERGE,
            # so we use a validated type from RELATION_TYPES
            result = session.run(
                f"MATCH (a:Concept {{name: $source}}) "
                f"MATCH (b:Concept {{name: $target}}) "
                f"MERGE (a)-[r:{rel_type}]->(b) "
                f"ON CREATE SET r.discovered_by = 'vault_import', "
                f"              r.weight = 1.0, "
                f"              r.reasoning = $reasoning "
                f"RETURN r",
                source=e["source"],
                target=e["target"],
                reasoning=f"Wikilink in {e['vault']} vault: [[{e['target']}]] — classified from context",
            )
            if result.single():
                edge_count += 1

        print(f"Edges: {edge_count} merged (vault-sourced, pre-classified)")

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

    # Ensure collections exist (needed after a full wipe)
    memory.ensure_collections()

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

    # Build summaries lookup for enriching bare-list contexts
    summaries = {c["name"]: c["summary"] for c in merged if c.get("summary")}

    # Classify edges (separate step — can be cached/skipped)
    print(f"\nClassifying {len(all_edges)} edges...")
    classify_edges(all_edges, summaries=summaries)

    # Load into Neo4j (receives pre-typed edges)
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
