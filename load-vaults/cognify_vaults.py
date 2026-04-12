"""
Run Cognee's cognify pipeline on all knowledge sources.

Points Cognee at our existing Neo4j backend, feeds it all vault content
+ docs, and lets gpt-4o-mini extract concepts and typed relationships
into ``:Concept`` nodes — the same label Marvin's ``ontology.py`` queries.

This uses the custom ``Concept(DataPoint)`` model from ``cognee_models.py``
as ``graph_model``. Per cognee 0.5.8 ``extract_graph_from_data.py:99-103``,
passing a custom graph_model bypasses the default ``Entity``-creating
flow and writes our model's class as the Neo4j label directly. The
model uses ``uuid5(slug(name))`` for IDs so the same concept extracted
across multiple chunks resolves to a single node.

After extraction, a post-processing step normalizes the snake_case edge
types (which come from our model's field names: ``implements``,
``requires``, ...) to SCREAMING_CASE matching ``relation_types.json``.

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

# Custom DataPoint model — defines the :Concept node shape and 16
# typed relation fields. See cognee_models.py for the design rationale.
from cognee_models import Concept

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
    """Build extraction prompt for the Concept(DataPoint) graph_model.

    The schema itself (Pydantic JSON schema for ``Concept``) already
    constrains the LLM's output to the 16 relation fields. This prompt
    adds the things the schema can't express: canonical naming, language
    preservation, and which relation types to prefer over the generic
    ``relates_to`` fallback.
    """
    type_lines = "\n".join(
        f"- {name.lower()}: {info['description']}"
        for name, info in RELATION_TYPES.items()
        if name != "RELATES_TO"  # discourage generic
    )
    symmetric = [
        name.lower() for name, info in RELATION_TYPES.items() if info.get("symmetric")
    ]

    return f"""You are a knowledge graph extraction engine for the Tautologia Ontológica thesis.

You will populate a ``Concept`` Pydantic model whose fields are
``name``, ``description``, and 16 typed relationship lists. Each
relationship field holds a list of related ``Concept`` objects with
their own ``name`` and ``description``.

## Concept extraction rules
- Extract concepts, mathematical constructs, software components, and
  theoretical principles. Each becomes a ``Concept`` with a name and a
  one-sentence description.
- Use the canonical name (e.g., "Contexto", "Rede Neural", "MCP Server").
- Preserve the original language (Portuguese or English) as it appears
  in the source. Do NOT translate.
- Do NOT extract generic terms like "system", "process", "thing", "it".
- The same concept name across chunks must resolve to the same node —
  spell it identically every time (case-insensitive matching is applied
  downstream, but consistency improves the LLM's own reasoning).

## Relationship extraction rules
Populate the appropriate field on the root Concept for each relation
you find. The available fields and their meaning:

{type_lines}

- Use ``relates_to`` only as an absolute last resort when no other
  field fits the semantics.
- Symmetric fields ({', '.join(symmetric)}): if A→B then B→A is implied
  — you only need to populate one direction.
- All other fields are directional. Choose the correct direction
  carefully (e.g., ``Marvin.implements = [Tautologia Ontológica]``,
  not the other way around).
- Extract logically implied relationships if they sharpen the graph.
- Do not invent fields outside the schema.
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


def _configure_cognee():
    """Set up cognee backends (Neo4j, LanceDB, LLM, embeddings)."""
    from cognee import config

    neo4j_uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    neo4j_user = os.getenv("NEO4J_USER", "neo4j")
    neo4j_pass = os.getenv("NEO4J_PASS", "tautologia")

    config.set_graph_database_provider("neo4j")
    config.set_graph_db_config({
        "graph_database_url": neo4j_uri,
        "graph_database_username": neo4j_user,
        "graph_database_password": neo4j_pass,
    })

    # Redirect LanceDB to a stable project-level path (outside venv).
    # marvin_ops reads these vectors during sync → Milvus.
    lancedb_path = os.getenv("COGNEE_LANCEDB_PATH", "data/cognee.lancedb")
    if not os.path.isabs(lancedb_path):
        lancedb_path = str(ROOT / lancedb_path)
    config.set_vector_db_config({"vector_db_url": lancedb_path})

    config.set_llm_config({
        "llm_provider": "openai",
        "llm_model": "gpt-4o-mini",
        "llm_api_key": os.getenv("OPENAI_API_KEY"),
        # Rate limiting — Tier 1: 200k TPM, 500 RPM
        # 2 RPM × 40k tokens/req = 80k TPM → 60% headroom, sustainable.
        # =1/=1 batch forces strict serialization.
        "llm_rate_limit_enabled": True,
        "llm_rate_limit_requests": 2,
        "llm_rate_limit_interval": 60,
    })

    config.set_embedding_config({
        "embedding_provider": "openai",
        "embedding_model": "text-embedding-3-small",
        "embedding_dimensions": 1536,
        "embedding_api_key": os.getenv("OPENAI_API_KEY"),
    })


# ── Path → label mapping (inverted from VAULTS) ──────────────
# Used by collect_changed_texts to derive labels from file paths.
_PATH_TO_VAULT: list[tuple[Path, str]] = [
    (v, name) for name, v in VAULTS.items()
]
_PATH_TO_VAULT.append((DOCS_DIR, "docs"))


def collect_changed_texts(file_paths: list[str]) -> list[tuple[str, str]]:
    """Read only the given files and return [(label, content), ...].

    Paths are relative to the repo root. Maps each path to a vault label
    using the same naming as collect_texts().
    """
    texts = []
    for rel_path in file_paths:
        full_path = ROOT / rel_path
        if not full_path.exists() or not full_path.suffix == ".md":
            print(f"  SKIP {rel_path}: not found or not .md")
            continue
        content = full_path.read_text(encoding="utf-8")
        if len(content) < 100:
            print(f"  SKIP {rel_path}: too short ({len(content)} chars)")
            continue

        # Derive label from path
        label = rel_path
        for vault_path, vault_name in _PATH_TO_VAULT:
            try:
                relative = full_path.relative_to(vault_path)
                label = f"{vault_name}/{relative.stem}"
                break
            except ValueError:
                continue

        texts.append((label, content))
    return texts


async def run():
    import cognee

    _configure_cognee()

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

    # ── Cognify with custom Concept graph_model + custom prompt ───
    # graph_model=Concept makes Cognee write :Concept nodes (via the
    # entity-centric branch in extract_graph_from_data.py:99-103) with
    # our 16 relation fields as edges. Deterministic IDs from the
    # model's _set_deterministic_id validator handle dedup across chunks.
    custom_prompt = build_custom_prompt()
    print("\n── Running cognify (gpt-4o-mini extraction) ──")
    print(f"  Custom prompt: {len(custom_prompt)} chars")
    print(f"  Graph model: Concept(DataPoint) — entity-centric")
    print(f"  Target types: {', '.join(RELATION_TYPES.keys())}")

    # Serialize fully: both knobs = 1.
    # cognee's `llm_rate_limit_requests` throttles request COUNT/min but
    # does NOT prevent concurrent in-flight requests within a batch.
    # chunks_per_batch=5 fires 5 parallel LLM calls per doc. data_per_batch=5
    # fires 5 docs in parallel. 5×5 = 25 concurrent ~40k-token requests on
    # launch = instant 200k TPM ceiling burn = 429 storm, 0 forward progress.
    # =1/=1 forces strict serialization so the 2 RPM ceiling actually applies.
    await cognee.cognify(
        datasets=["tautologia"],
        graph_model=Concept,
        custom_prompt=custom_prompt,
        chunks_per_batch=1,
        data_per_batch=1,
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


async def run_incremental(changed_paths: list[str]):
    """Cognify only the given changed files. Same pipeline as run() but selective."""
    import cognee

    _configure_cognee()

    texts = collect_changed_texts(changed_paths)
    if not texts:
        print("No changed files to cognify.")
        return

    print(f"\nCollected {len(texts)} changed documents")
    for label, content in texts:
        print(f"  {label} ({len(content)} chars)")

    print("\n── Adding changed documents to Cognee ──")
    content_list = [content for _, content in texts]
    await cognee.add(content_list, dataset_name="tautologia")
    print(f"  Added {len(content_list)} documents to dataset 'tautologia'")

    custom_prompt = build_custom_prompt()
    print("\n── Running incremental cognify ──")
    await cognee.cognify(
        datasets=["tautologia"],
        graph_model=Concept,
        custom_prompt=custom_prompt,
        chunks_per_batch=1,
        data_per_batch=1,
    )
    print("  cognify complete!")

    await post_process_edges()


if __name__ == "__main__":
    os.environ["ENABLE_BACKEND_ACCESS_CONTROL"] = "false"
    asyncio.run(run())
