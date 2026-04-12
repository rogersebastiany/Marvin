"""
Smoke test for Concept(DataPoint) custom graph_model.

Validates that Cognee 0.5.8's entity-centric custom-graph-model branch
(extract_graph_from_data.py:99-103) actually works at runtime with our
Concept model — before betting the full vault sweep on Path A.

Uses two short texts with unique made-up concept names so the resulting
:Concept nodes are trivially distinguishable from any pre-existing
cognee :Concept nodes already in Neo4j.

Pass criteria:
1. cognify() returns without ValidationError
2. Neo4j has new :Concept nodes named FlibberWidget, ZorbProtocol,
   GlimmerEngine, WhirligigStandard
3. At least one typed edge among them (implements/requires/enables/etc)
"""

import asyncio
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

from cognee_models import Concept

SMOKE_TEXTS = [
    """The FlibberWidget is a hypothetical software component invented for testing.
A FlibberWidget implements the ZorbProtocol, the standard for inter-widget
communication. To operate, every FlibberWidget requires the GlimmerEngine,
which provides the runtime environment.""",
    """The ZorbProtocol is a specification that defines how FlibberWidgets exchange
messages. ZorbProtocol contradicts the older WhirligigStandard, which it was
designed to replace. The GlimmerEngine enables modern ZorbProtocol
implementations by handling message routing.""",
]

UNIQUE_NAMES = ["FlibberWidget", "ZorbProtocol", "GlimmerEngine", "WhirligigStandard"]


async def smoke():
    import cognee
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

    config.set_llm_config({
        "llm_provider": "openai",
        "llm_model": "gpt-4o-mini",
        "llm_api_key": os.getenv("OPENAI_API_KEY"),
        "llm_rate_limit_enabled": True,
        "llm_rate_limit_requests": 10,
        "llm_rate_limit_interval": 60,
    })

    config.set_embedding_config({
        "embedding_provider": "openai",
        "embedding_model": "text-embedding-3-small",
        "embedding_dimensions": 1536,
        "embedding_api_key": os.getenv("OPENAI_API_KEY"),
    })

    print("── Smoke test: Concept(DataPoint) custom graph_model ──")
    print(f"  Texts: {len(SMOKE_TEXTS)}")
    print(f"  Unique concept names: {UNIQUE_NAMES}")

    print("\n── cognee.add ──")
    await cognee.add(SMOKE_TEXTS, dataset_name="smoke_concept_model")
    print("  added")

    print("\n── cognee.cognify(graph_model=Concept) ──")
    await cognee.cognify(
        datasets=["smoke_concept_model"],
        graph_model=Concept,
        chunks_per_batch=5,
        data_per_batch=5,
    )
    print("  cognify complete")

    print("\n── Neo4j inspection ──")
    from neo4j import GraphDatabase
    driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_pass))
    with driver.session() as session:
        for name in UNIQUE_NAMES:
            r = session.run(
                "MATCH (c:Concept) WHERE toLower(c.name) = toLower($n) "
                "RETURN c.name as name, c.description as desc, c.id as id",
                n=name,
            ).single()
            if r:
                print(f"  ✓ {r['name']}: {(r['desc'] or '')[:80]}")
                print(f"     id={r['id']}")
            else:
                print(f"  ✗ MISSING: {name}")

        print("\n  Edges between smoke concepts:")
        edges = session.run(
            "MATCH (a:Concept)-[r]->(b:Concept) "
            "WHERE toLower(a.name) IN [n IN $names | toLower(n)] "
            "  AND toLower(b.name) IN [n IN $names | toLower(n)] "
            "RETURN a.name as src, type(r) as rel, b.name as dst",
            names=UNIQUE_NAMES,
        ).data()
        if edges:
            for e in edges:
                print(f"    {e['src']} -[{e['rel']}]-> {e['dst']}")
        else:
            print("    (none — extraction succeeded but no inter-concept edges)")

    driver.close()
    print("\n── Done. Pass = all 4 names found + at least 1 edge ──")


if __name__ == "__main__":
    os.environ["ENABLE_BACKEND_ACCESS_CONTROL"] = "false"
    asyncio.run(smoke())
