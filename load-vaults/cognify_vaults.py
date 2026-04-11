"""
Run Cognee's cognify pipeline on all knowledge sources.

Points Cognee at our existing Neo4j backend, feeds it all vault content
+ docs, and lets gpt-4o-mini extract entities and typed relationships.

Cognee uses its default KnowledgeGraph model (Node/Edge) with a custom
prompt that guides the LLM toward our 16 relation types. After extraction,
a post-processing step normalizes snake_case edges → SCREAMING_CASE using
the mapping in relation_types.json.

Usage:
    uv run python cognify_vaults.py
"""

import asyncio
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

ROOT = Path(__file__).parent.parent

# Load our relation types (single source of truth)
RELATION_TYPES_PATH = ROOT / "mcp-server" / "relation_types.json"
with open(RELATION_TYPES_PATH) as f:
    RELATION_TYPES = json.load(f)

# ── snake_case → SCREAMING_CASE mapping ──────────────────────────
# Cognee's default KnowledgeGraph outputs snake_case edge names.
# We normalize them to our SCREAMING_CASE ontology types.
EDGE_NORMALIZE: dict[str, str] = {}
for type_name in RELATION_TYPES:
    # Direct lowercase match: "implements" → "IMPLEMENTS"
    EDGE_NORMALIZE[type_name.lower()] = type_name
# Add common Cognee defaults that map to our types.
# Expanded 2026-04-10 after first successful run showed ~150 edges falling
# through to RELATES_TO that had a clear semantic home.
EDGE_NORMALIZE.update({
    # ── COMPOSES (part-of / building block) ──
    "contains": "COMPOSES",
    "is_part_of": "COMPOSES",
    "part_of": "COMPOSES",
    "made_from": "COMPOSES",
    "components": "COMPOSES",
    "encompasses": "COMPOSES",
    "encapsulates": "COMPOSES",
    "includes": "COMPOSES",
    "forms": "COMPOSES",
    # ── EXEMPLIFIES (instance / illustration) ──
    "is_a": "EXEMPLIFIES",
    "is": "EXEMPLIFIES",
    "_exemplifies": "EXEMPLIFIES",
    # ── ENABLES (makes possible) ──
    "enabled_by": "ENABLES",
    "enabled": "ENABLES",
    "enabling": "ENABLES",
    "enabler": "ENABLES",
    "used_by": "ENABLES",
    "supports": "ENABLES",
    "provides": "ENABLES",
    "produces": "ENABLES",
    "encourages": "ENABLES",
    "required_by": "ENABLES",       # reverse of REQUIRES
    "enebles": "ENABLES",           # LLM typo
    # ── REQUIRES (dependency / precondition) ──
    "depends_on": "REQUIRES",
    "uses": "REQUIRES",
    "required": "REQUIRES",
    "constrains": "REQUIRES",
    # ── IMPLEMENTS (concrete realization) ──
    "implementis": "IMPLEMENTS",    # LLM typo
    "impliments": "IMPLEMENTS",     # LLM typo
    "implants": "IMPLEMENTS",       # LLM typo
    "implices": "IMPLEMENTS",       # LLM typo
    "imples": "IMPLEMENTS",         # LLM typo
    # ── EXTENDS (specialization / enhancement) ──
    "specializes": "EXTENDS",
    "generalizes": "EXTENDS",
    "enhances": "EXTENDS",
    "enhance": "EXTENDS",
    "expands": "EXTENDS",
    # ── DEFINES ──
    "defined_by": "DEFINES",
    "define": "DEFINES",
    "defenes": "DEFINES",           # LLM typo
    # ── PROVES ──
    "demonstrates": "PROVES",
    "validates": "PROVES",
    "evidences": "PROVES",
    # ── INFERS ──
    "inferred_from": "INFERS",
    "implies": "INFERS",
    "infer": "INFERS",
    # ── FORMALIZES ──
    "formalized_by": "FORMALIZES",
    # ── EVOLVES_FROM ──
    "inspired_by": "EVOLVES_FROM",
    "derived_from": "EVOLVES_FROM",
    "based_on": "EVOLVES_FROM",
    # ── ANALOGOUS_TO ──
    "similar_to": "ANALOGOUS_TO",
    "like": "ANALOGOUS_TO",
    "alternative_to": "ANALOGOUS_TO",
    # ── CONTRADICTS ──
    "opposes": "CONTRADICTS",
    "conflicts_with": "CONTRADICTS",
    "defies": "CONTRADICTS",
    # ── MITIGATES ──
    "mitigated_by": "MITIGATES",
    "reduces_risk_of": "MITIGATES",
    "defends": "MITIGATES",
    "protects": "MITIGATES",
})


def build_custom_prompt() -> str:
    """Build extraction prompt constrained to our ontology's relation types."""
    type_lines = "\n".join(
        f"- {name}: {info['description']}"
        for name, info in RELATION_TYPES.items()
        if name != "RELATES_TO"  # discourage generic
    )
    symmetric = [name for name, info in RELATION_TYPES.items() if info.get("symmetric")]

    return f"""You are a knowledge graph extraction engine for the Tautologia Ontológica thesis.

## Entity extraction rules
- Extract concepts, mathematical constructs, software components, and theoretical principles as entities.
- Use the entity's canonical name (e.g., "Contexto", "Rede Neural", "MCP Server").
- Preserve the original language (Portuguese or English) as it appears in the text.
- Do NOT extract generic terms like "system", "process", "thing", "it".

## Relationship extraction rules
Prefer these relationship types (use the exact snake_case form):

{type_lines}

- Use "relates_to" only as an absolute last resort when no other type fits.
- Symmetric types ({', '.join(symmetric)}): if A→B then B→A is implied.
- All other types are directional: choose the correct direction carefully.
- Extract logically implied relationships if they enhance clarity.
- Never invent relationship types not in the list above.
"""


# ── Vault paths ──────────────────────────────────────────────────
VAULTS = {
    "thesis": ROOT / "obsidian-vault-tautologia-ontologica" / "obsidian-vault",
    "implementation": ROOT / "vault",
    "thesis-en": ROOT / "vault-thesis-en",
    "implementation-en": ROOT / "vault-implementation-en",
}
DOCS_DIR = ROOT / "mcp-server" / "docs"


def collect_texts() -> list[tuple[str, str]]:
    """Collect all texts to feed Cognee. Returns [(label, content), ...]."""
    texts = []

    # Obsidian vaults
    for vault_name, vault_path in VAULTS.items():
        if not vault_path.exists():
            print(f"  SKIP vault {vault_name}: {vault_path} not found")
            continue
        for md_file in sorted(vault_path.glob("*.md")):
            content = md_file.read_text(encoding="utf-8")
            if len(content) < 100:
                continue
            texts.append((f"{vault_name}/{md_file.stem}", content))

    # Docs
    if DOCS_DIR.exists():
        for md_file in sorted(DOCS_DIR.glob("*.md")):
            content = md_file.read_text(encoding="utf-8")
            if len(content) < 200:
                continue
            texts.append((f"docs/{md_file.stem}", content))

    return texts


async def post_process_edges():
    """Normalize Cognee's snake_case edges to our SCREAMING_CASE ontology types."""
    from neo4j import GraphDatabase

    neo4j_uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    neo4j_user = os.getenv("NEO4J_USER", "neo4j")
    neo4j_pass = os.getenv("NEO4J_PASS", "tautologia")

    driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_pass))

    with driver.session() as session:
        # Get all edge types
        result = session.run(
            "MATCH ()-[r]->() RETURN DISTINCT type(r) as edge_type, count(r) as cnt "
            "ORDER BY cnt DESC"
        ).data()

        print("\n── Post-processing edges ──")
        print("Current edge types:")
        for row in result:
            print(f"  {row['edge_type']}: {row['cnt']}")

        normalized = 0
        unmapped = []

        for row in result:
            edge_type = row["edge_type"]
            lower = edge_type.lower()

            # Already SCREAMING_CASE and in our types? Skip.
            if edge_type in RELATION_TYPES:
                continue

            # Find mapping
            target = EDGE_NORMALIZE.get(lower)
            if not target:
                # Try removing common prefixes
                for prefix in ("has_", "is_", "was_"):
                    if lower.startswith(prefix):
                        stem = lower[len(prefix):]
                        target = EDGE_NORMALIZE.get(stem)
                        if target:
                            break

            if target:
                # Rename edges via APOC or manual: create new + delete old
                count = session.run(
                    f"MATCH (a)-[r:`{edge_type}`]->(b) "
                    f"CREATE (a)-[r2:`{target}`]->(b) "
                    "SET r2 = properties(r) "
                    "DELETE r "
                    "RETURN count(r2) as cnt"
                ).single()["cnt"]
                print(f"  {edge_type} → {target}: {count} edges renamed")
                normalized += count
            else:
                unmapped.append((edge_type, row["cnt"]))

        if unmapped:
            print(f"\n  Unmapped edge types (→ RELATES_TO):")
            for edge_type, cnt in unmapped:
                count = session.run(
                    f"MATCH (a)-[r:`{edge_type}`]->(b) "
                    f"CREATE (a)-[r2:RELATES_TO]->(b) "
                    "SET r2 = properties(r) "
                    "DELETE r "
                    "RETURN count(r2) as cnt"
                ).single()["cnt"]
                print(f"    {edge_type} → RELATES_TO: {count} edges")
                normalized += count

        print(f"\n  Total edges normalized: {normalized}")

        # Final count
        result = session.run(
            "MATCH ()-[r]->() RETURN DISTINCT type(r) as edge_type, count(r) as cnt "
            "ORDER BY cnt DESC"
        ).data()
        print("\nFinal edge types:")
        for row in result:
            marker = " ✓" if row["edge_type"] in RELATION_TYPES else " ?"
            print(f"  {row['edge_type']}: {row['cnt']}{marker}")

    driver.close()


async def run():
    import cognee
    from cognee import config

    # ── Configure backends ────────────────────────────────────────
    neo4j_uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    neo4j_user = os.getenv("NEO4J_USER", "neo4j")
    neo4j_pass = os.getenv("NEO4J_PASS", "tautologia")

    config.set_graph_database_provider("neo4j")
    config.set_graph_db_config({
        "graph_database_url": neo4j_uri,
        "graph_database_username": neo4j_user,
        "graph_database_password": neo4j_pass,
    })

    # Cognee 0.5.8 dropped Milvus from core — use LanceDB for Cognee's
    # own vector needs (chunking/embeddings). Our Milvus stays for Marvin.
    # What matters is Neo4j: Cognee writes extracted entities+edges there.

    config.set_llm_config({
        "llm_provider": "openai",
        "llm_model": "gpt-4o-mini",
        "llm_api_key": os.getenv("OPENAI_API_KEY"),
        # Rate limiting — Tier 1: 200k TPM, 500 RPM
        "llm_rate_limit_enabled": True,
        "llm_rate_limit_requests": 10,   # 10 req/min — ~60k TPM, safe under 200k
        "llm_rate_limit_interval": 60,
    })

    config.set_embedding_config({
        "embedding_provider": "openai",
        "embedding_model": "text-embedding-3-small",
        "embedding_dimensions": 1536,
        "embedding_api_key": os.getenv("OPENAI_API_KEY"),
    })

    # ── Collect content ───────────────────────────────────────────
    texts = collect_texts()
    print(f"\nCollected {len(texts)} documents")
    for label, content in texts[:5]:
        print(f"  {label} ({len(content)} chars)")
    if len(texts) > 5:
        print(f"  ... and {len(texts) - 5} more")

    # ── Feed to Cognee ────────────────────────────────────────────
    print("\n── Adding documents to Cognee ──")
    content_list = [content for _, content in texts]
    await cognee.add(content_list, dataset_name="tautologia")
    print(f"  Added {len(content_list)} documents to dataset 'tautologia'")

    # ── Cognify with default KnowledgeGraph + custom prompt ───────
    # We use Cognee's default graph model (Node/Edge) because custom
    # graph_model must follow Cognee's entity-centric pattern (fields
    # as relationships, not nodes/edges lists). The custom_prompt guides
    # the LLM toward our types; post-processing normalizes the rest.
    custom_prompt = build_custom_prompt()
    print("\n── Running cognify (gpt-4o-mini extraction) ──")
    print(f"  Custom prompt: {len(custom_prompt)} chars")
    print(f"  Graph model: default KnowledgeGraph (post-process normalization)")
    print(f"  Target types: {', '.join(RELATION_TYPES.keys())}")

    await cognee.cognify(
        datasets=["tautologia"],
        custom_prompt=custom_prompt,
        chunks_per_batch=5,
        data_per_batch=5,
    )
    print("  cognify complete!")

    # ── Post-process: normalize edge types ────────────────────────
    await post_process_edges()

    # ── Quick verification ────────────────────────────────────────
    print("\n── Verification search ──")
    from cognee.api.v1.search import SearchType

    results = await cognee.search(
        query_type=SearchType.GRAPH_COMPLETION,
        query_text="What is Tautologia Ontológica?",
    )
    print(f"  Got {len(results)} results for 'Tautologia Ontológica'")
    for r in results[:3]:
        print(f"    {r}")


if __name__ == "__main__":
    os.environ["ENABLE_BACKEND_ACCESS_CONTROL"] = "false"
    asyncio.run(run())
