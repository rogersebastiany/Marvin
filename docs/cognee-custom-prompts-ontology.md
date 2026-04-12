# Cognee Custom Prompts and Ontology-Grounded Extraction


---

## 1. custom-prompts

A minimal guide to shaping graph extraction with a custom LLM prompt. You’ll pass your prompt via `custom_prompt` to `cognee.cognify()` to control entity types, relationship labels, and extraction rules.

For the built-in graph extraction prompts selected through `GRAPH_PROMPT_PATH`, see [Cognify](/core-concepts/main-operations/cognify).

**Before you start:**

* Complete [Quickstart](getting-started/quickstart) to understand basic operations
* Ensure you have [LLM Providers](setup-configuration/llm-providers) configured
* Have some text or files to process

## [​](#code-in-action) Code in Action

```
import asyncio
import cognee
from cognee.api.v1.search import SearchType

custom_prompt = """
Extract only people and cities as entities.
Connect people to cities with the relationship "lives_in".
Ignore all other entities.
"""

async def main():
    await cognee.add([
        "Alice moved to Paris in 2010, while Bob has always lived in New York.",
        "Andreas was born in Venice, but later settled in Lisbon.",
        "Diana and Tom were born and raised in Helsingy. Diana currently resides in Berlin, while Tom never moved."
    ])
    await cognee.cognify(custom_prompt=custom_prompt)

    res = await cognee.search(
        query_type=SearchType.GRAPH_COMPLETION,
        query_text="Where does Alice live?",
    )
    print(res)

if     asyncio.run(main())
```

This simple example uses a few strings for demonstration. In practice, you can add multiple documents, files, or entire datasets - the custom prompt processing works the same way across all your data.

## [​](#what-just-happened) What Just Happened

### [​](#step-1-add-your-data) Step 1: Add Your Data

```
await cognee.add([
    "Alice moved to Paris in 2010, while Bob has always lived in New York.",
    "Andreas was born in Venice, but later settled in Lisbon.",
    "Diana and Tom were born and raised in Helsingy. Diana currently resides in Berlin, while Tom never moved."
])
```

This adds text data to Cognee using the standard `add` function. The same approach works with multiple documents, files, or entire datasets.

### [​](#step-2-write-a-custom-prompt) Step 2: Write a Custom Prompt

```
custom_prompt = """
Extract only people and cities as entities.
Connect people to cities with the relationship "lives_in".
Ignore all other entities.
"""
```

The custom prompt overrides the default system prompt used during entity/relationship extraction. It constrains node types, enforces relationship naming, and reduces noise.

`custom_prompt` is ignored when `temporal_cognify=True`.

### [​](#step-3-cognify-with-your-custom-prompt) Step 3: Cognify with Your Custom Prompt

```
await cognee.cognify(custom_prompt=custom_prompt)
```

This processes your data using the custom prompt to control extraction behavior. You can also scope to specific datasets by passing the `datasets` parameter.

### [​](#step-4-ask-questions) Step 4: Ask Questions

```
res = await cognee.search(
    query_type=SearchType.GRAPH_COMPLETION,
    query_text="Where does Alice live?",
)
```

Use `SearchType.GRAPH_COMPLETION` to get answers that leverage your custom extraction rules.

## [​](#additional-examples) Additional examples

Additional examples about Custom prompts are available on our [github](https://github.com/topoteretes/cognee/tree/dev/examples/guides).

## Core Concepts

Understand knowledge graph fundamentals

## Ontology Quickstart

Learn about ontology integration

## API Reference

Explore API endpoints

---

## 2. memify-triplet-embeddings

## [​](#when-to-use-this) When to use this

You need `SearchType.TRIPLET_COMPLETION` to return results. This search type matches queries against text representations of graph triplets (source → relationship → target). The `create_triplet_embeddings` pipeline creates these embeddings.
**Before you start:**

* Complete [Quickstart](/getting-started/quickstart) to understand basic operations
* Ensure you have [LLM Providers](/setup-configuration/llm-providers) configured
* Have an existing knowledge graph (add → cognify completed)

## [​](#code-in-action) Code in Action

```
import asyncio
import cognee
from cognee import SearchType
from cognee.memify_pipelines.create_triplet_embeddings import create_triplet_embeddings
from cognee.modules.users.methods import get_default_user

async def main():
    await cognee.add(
        ["GraphRAG combines vector search with graph traversal for better context."],
        dataset_name="triplet_demo",
    )
    await cognee.cognify(datasets=["triplet_demo"])

    user = await get_default_user()
    await create_triplet_embeddings(user=user, dataset="triplet_demo")

    results = await cognee.search(
        query_type=SearchType.TRIPLET_COMPLETION,
        query_text="How does GraphRAG work?",
    )
    for result in results:
        print(result)

asyncio.run(main())
```

## [​](#what-just-happened) What Just Happened

1. **Add + Cognify** — builds a knowledge graph with entities and relationships from your text.
2. **`get_default_user()`** — retrieves the authenticated user. This pipeline requires a `User` object with write access to the dataset.
3. **`create_triplet_embeddings(user, dataset)`** — iterates over all graph triplets, converts each to a text representation, and indexes them in the vector DB.
4. **Search with `TRIPLET_COMPLETION`** — queries the new `Triplet_text` collection by semantic similarity.

## [​](#what-changed-in-your-graph) What Changed in Your Graph

* The `Triplet_text` collection is populated in the vector DB. Each entry is a text representation of a graph triplet (source → relationship → target).
* `SearchType.TRIPLET_COMPLETION` queries now return results by matching your query against these triplet embeddings.

Parameters

* **`user`** (`User`, required) — authenticated user with write access. Obtain via `await get_default_user()`.
* **`dataset`** (`str`, default: `"main_dataset"`) — the dataset whose graph triplets to index.
* **`run_in_background`** (`bool`, default: `False`) — run asynchronously and return immediately.
* **`triplets_batch_size`** (`int`, default: `100`) — how many triplets to index per batch. Lower values use less memory; higher values are faster.

Under the hood

Two tasks run in sequence:

1. **`get_triplet_datapoints`** — iterates over graph triplets and yields `Triplet` objects with embeddable text.
2. **`index_data_points`** — indexes each triplet in the vector DB under the `Triplet_text` collection.

Troubleshooting

* **Empty results from `TRIPLET_COMPLETION`** — ensure the graph has been built (cognify completed) and that `create_triplet_embeddings` finished without errors.
* **Error: no graph data found** — run `cognee.add()` and `cognee.cognify()` before calling this pipeline.
* **LLM errors** — verify that your LLM provider is configured. See [LLM Providers](/setup-configuration/llm-providers).
* **Permission errors** — the user must have write access to the target dataset. See [Permissions](/core-concepts/multi-user-mode/permissions-system/datasets).

## Memify Concept

Understand how memify pipelines work

## Memify Quickstart

Run the default coding-rules pipeline

## Search

Query the enriched graph with specialized search types

---

## Bibliography

1. [custom-prompts](https://docs.cognee.ai/guides/custom-prompts)
2. [memify-triplet-embeddings](https://docs.cognee.ai/guides/memify-triplet-embeddings)