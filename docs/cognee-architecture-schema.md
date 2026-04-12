# Cognee Architecture - Schema, Graph Structure, Ontology, Storage Backends


---

## 1. search

## [​](#what-is-search) What is search

`search` lets you ask questions over everything you’ve ingested and cognified.  
Under the hood, Cognee blends **vector similarity**, **graph structure**, and **LLM reasoning** to return answers with context and provenance.

## [​](#the-big-picture) The big picture

* **Dataset-aware**: searches run against one or more datasets you can read *(requires `ENABLE_BACKEND_ACCESS_CONTROL=true`)*
* **Multiple modes**: from simple chunk lookup to graph-aware Q&A
* **Hybrid retrieval**: vectors find relevant pieces; graphs provide structure; LLMs compose answers
* **Conversational memory**: for GRAPH\_COMPLETION, RAG\_COMPLETION, and TRIPLET\_COMPLETION, use `session_id` to maintain conversation history across searches *(requires caching enabled)*. When caching is on, omitting `session_id` uses `default_session` and still stores history. Other search types do not use session history.
* **Safe by default**: permissions are checked before any retrieval
* **Observability**: telemetry is emitted for query start/completion

**Dataset scoping** requires specific configuration. See [permissions system](/core-concepts/multi-user-mode/permissions-system/datasets#dataset-isolation-how-access-is-enforced) for details on access control requirements and supported database setups.

## [​](#where-search-fits) Where search fits

Use `search` after you’ve run `.add` and `.cognify`.
At that point, your dataset has chunks, summaries, embeddings, and a knowledge graph—so queries can leverage both **similarity** and **structure**.

## [​](#how-it-works-conceptually) How it works (conceptually)

1. **Scope & permissions**  
   Resolve target datasets (by name or id) and enforce read access.
2. **Mode dispatch**  
   Pick a search mode (default: **graph-aware completion**) and route to its retriever.
3. **Retrieve → (optional) generate**  
   Collect context via vectors and/or graph traversal; some modes then ask an LLM to compose a final answer.
4. **Return results**  
   Depending on mode: answers, chunks/summaries with metadata, graph records, Cypher results, or code contexts.

For a practical guide to using search with examples and detailed parameter explanations, see [Search Basics](/guides/search-basics).

## [​](#retrievers) Retrievers

Each search type is handled by a **retriever**. The pipeline is: `get_retrieved_objects` → `get_context_from_objects` → `get_completion_from_context` (skipped when `only_context=True`).

| Search type | Retriever |
| --- | --- |
| GRAPH\_COMPLETION | GraphCompletionRetriever |
| RAG\_COMPLETION | CompletionRetriever |
| CHUNKS | ChunksRetriever |
| SUMMARIES | SummariesRetriever |
| GRAPH\_SUMMARY\_COMPLETION | GraphSummaryCompletionRetriever |
| GRAPH\_COMPLETION\_COT | GraphCompletionCotRetriever |
| GRAPH\_COMPLETION\_CONTEXT\_EXTENSION | GraphCompletionContextExtensionRetriever |
| TRIPLET\_COMPLETION | TripletRetriever |
| CHUNKS\_LEXICAL | JaccardChunksRetriever |
| CODING\_RULES | CodingRulesRetriever |
| TEMPORAL | TemporalRetriever |
| CYPHER | CypherSearchRetriever |
| NATURAL\_LANGUAGE | NaturalLanguageRetriever |

You can register a custom retriever for a search type via `use_retriever(SearchType, RetrieverClass)`; the class must implement the same three-step interface (`BaseRetriever`). See the API reference for `BaseRetriever` and `register_retriever`.

### [​](#multi-query-batch) Multi-query (batch)

**GraphCompletionRetriever**, **GraphCompletionCotRetriever**, and **GraphCompletionContextExtensionRetriever** support **batch mode**: pass `query_batch` (a non-empty list of strings) instead of `query`. You get one result per query; session cache is not used in batch mode. The public `cognee.search()` API accepts only a single `query_text`; batch is available when you use the retrievers directly (e.g. in custom pipelines).

GRAPH\_COMPLETION (default)

Graph-aware question answering.

* **What it does**: Finds relevant graph triplets using vector hints across indexed fields, resolves them into readable context, and asks an LLM to answer your question grounded in that context.
* **Why it’s useful**: Combines fuzzy matching (vectors) with precise structure (graph) so answers reflect relationships, not just nearby text.
* **Typical output**: A natural-language answer with references to the supporting graph context.

RAG\_COMPLETION

Retrieve-then-generate over text chunks.

* **What it does**: Pulls top-k chunks via vector search, stitches a context window, then asks an LLM to answer.
* **When to use**: You want fast, text-only RAG without graph structure.
* **Output**: An LLM answer grounded in retrieved chunks.

CHUNKS

Direct chunk retrieval.

* **What it does**: Returns the most similar text chunks to your query via vector search.
* **When to use**: You want raw passages/snippets to display or post-process.
* **Output**: Chunk dicts with `text`, `chunk_index`, `chunk_size`, and an `is_part_of` field carrying the source document’s `name` and `raw_data_location`. See [Citation and Source Tracking](/guides/search-basics#citation-and-source-tracking) for field details and examples.

SUMMARIES

Search over precomputed summaries.

* **What it does**: Vector search on `TextSummary` content for concise, high-signal hits.
* **When to use**: You prefer short summaries instead of full chunks.
* **Output**: Summary dicts with `text` and a `made_from` field that traces back to the source document via `made_from.is_part_of.name` and `made_from.is_part_of.raw_data_location`. See [Citation and Source Tracking](/guides/search-basics#citation-and-source-tracking) for field details and examples.

GRAPH\_SUMMARY\_COMPLETION

Graph-aware summary answering.

* **What it does**: Builds graph context like GRAPH\_COMPLETION, then condenses it before answering.
* **When to use**: You want a tighter, summary-first response.
* **Output**: A concise answer grounded in graph context.

GRAPH\_COMPLETION\_COT

Chain-of-thought over the graph.

* **What it does**: Iterative rounds of graph retrieval and LLM reasoning to refine the answer.
* **When to use**: Complex questions that benefit from stepwise reasoning.
* **Output**: A refined answer produced through multiple reasoning steps.

GRAPH\_COMPLETION\_CONTEXT\_EXTENSION

Iterative context expansion.

* **What it does**: Starts with initial graph context, lets the LLM suggest follow-ups, fetches more graph context, repeats.
* **When to use**: Open-ended queries that need broader exploration.
* **Output**: An answer assembled after expanding the relevant subgraph.

NATURAL\_LANGUAGE

Natural language to Cypher to execution.

* **What it does**: Infers a Cypher query from your question using the graph schema, runs it, returns the results.
* **When to use**: You want structured graph answers without writing Cypher.
* **Output**: Executed graph results.

CYPHER

Run Cypher directly.

* **What it does**: Executes your Cypher query against the graph database.
* **When to use**: You know the schema and want full control.
* **Output**: Raw query results.

**CYPHER** and **NATURAL\_LANGUAGE** are disabled when `ALLOW_CYPHER_QUERY=false` (environment variable).

CODING\_RULES

Code-focused retrieval (coding rules / codebase search).

* **What it does**: Retrieves rules or code context from the `coding_agent_rules` nodeset and returns structured code information.
* **When to use**: Codebases or coding guidelines indexed by Cognee (e.g. via memify).
* **Output**: Structured code contexts and related graph information.
* **Prereq**: The `coding_agent_rules` nodeset must be populated (e.g. via [memify](/guides/memify-quickstart)).

TRIPLET\_COMPLETION

Triple-based retrieval with LLM completion (no full graph traversal).

* **What it does**: Retrieves graph triplets by vector similarity, resolves them to text, and asks an LLM to answer.
* **When to use**: You want triplet-level context without full graph expansion.
* **Output**: An LLM answer grounded in retrieved triplets.
* **Prereq**: Triplet embeddings must exist—set `TRIPLET_EMBEDDING=true` before running [cognify](/core-concepts/main-operations/cognify) or run the [`create_triplet_embeddings`](/guides/memify-triplet-embeddings) memify pipeline (retriever uses the `Triplet_text` collection).

CHUNKS\_LEXICAL

Lexical (keyword-style) chunk search.

* **What it does**: Returns chunks that match your query using token-based similarity (e.g. Jaccard), not semantic embeddings.
* **When to use**: Exact-term or keyword-style lookups; stopword-aware search.
* **Output**: Ranked text chunks, optionally with scores.

TEMPORAL

Time-aware retrieval.

* **What it does**: Retrieves and ranks content by temporal relevance (dates, events) and answers with time context.
* **When to use**: Queries about “before/after X”, “in 2020”, or event timelines.
* **Output**: An answer grounded in time-filtered graph context. See [Time-awareness](/guides/time-awareness) for setup.

FEELING\_LUCKY

Automatic mode selection.

* **What it does**: Uses an LLM to pick the most suitable search mode for your query, then runs it.
* **When to use**: You’re not sure which mode fits best.
* **Output**: Results from the selected mode.

**Feedback** is handled via [Sessions](/core-concepts/sessions-and-caching) and the [Feedback System](/guides/feedback-system)—use `cognee.session.add_feedback` and `cognee.session.delete_feedback`. See the [Sessions Guide](/guides/sessions) and [Feedback System](/guides/feedback-system) for full details.

## Add

First bring data into Cognee

## Cognify

Build the knowledge graph that search queries

## Architecture

Understand how vector and graph stores work together

## Sessions and Caching

Enable conversational memory with sessions

---

## 2. memify

## [​](#what-is-the-memify-operation) What is the memify operation

The `.memify` operation runs enrichment pipelines on an existing knowledge graph. It requires a graph built by [Add](/core-concepts/main-operations/add) and [Cognify](/core-concepts/main-operations/cognify) — it does not ingest raw data or build the graph from scratch.
Every memify pipeline is composed of two stages:

* **Extraction** — selects or prepares data from the existing graph. For example, pulling document chunks, loading graph triplets, or reading cached sessions.
* **Enrichment** — processes the extracted data (typically via LLM) and writes new or updated nodes and edges back to the graph. For example, deriving coding rules, indexing triplet embeddings, or consolidating entity descriptions.

Memify chains extraction tasks and enrichment tasks into a single pipeline and runs them in sequence. When you call `await cognee.memify()` with no arguments, it runs the default pipeline. You can also call one of the other built-in pipelines directly, or supply your own custom tasks.

Parameters (cognee.memify)

* **`extraction_tasks`** (`List[Task]`, default: `[Task(extract_subgraph_chunks)]`) — tasks that select or prepare the data to process. When omitted, memify pulls document chunks from the existing graph.
* **`enrichment_tasks`** (`List[Task]`, default: `[Task(add_rule_associations, rules_nodeset_name="coding_agent_rules")]`) — tasks that create or update nodes and edges from the extracted data. When omitted, memify derives coding-rule associations.
* **`data`** (`Any`, default: `None`) — input data forwarded to the first extraction task. When `None`, memify loads the graph (or a filtered subgraph) as input.
* **`dataset`** (`str` or `UUID`, default: `"main_dataset"`) — the dataset to process. The user must have write access.
* **`node_type`** (`Type`, default: `NodeSet`) — filter the graph to nodes of this type. Only used when `data` is `None`.
* **`node_name`** (`List[str]`, default: `None`) — filter the graph to nodes with these names. Only used when `data` is `None`.
* **`run_in_background`** (`bool`, default: `False`) — if `True`, memify starts processing and returns immediately. Use the returned `pipeline_run_id` to monitor progress.

## [​](#built-in-pipelines) Built-in pipelines

Cognee ships four built-in pipelines. Each one calls `cognee.memify()` with a pre-configured pair of extraction and enrichment tasks. The default pipeline runs when you call `cognee.memify()` with no arguments. The other three are convenience functions that call `cognee.memify()` internally with their own tasks.

Coding rules (default)

Runs when you call `await cognee.memify()` with no task arguments.

* **Extraction** (`extract_subgraph_chunks`) — pulls document chunk texts from the existing graph
* **Enrichment** (`add_rule_associations`) — sends chunks to the LLM, which derives coding-rule associations

**Produces:** `Rule` nodes connected to source chunks via `rule_associated_from` edges, grouped under the `coding_agent_rules` [node set](/core-concepts/further-concepts/node-sets). Enables [`SearchType.CODING_RULES`](/core-concepts/main-operations/search) queries.Guide: [Memify Quickstart](/guides/memify-quickstart)

Triplet embeddings

Calls `cognee.memify()` with triplet-specific tasks via `await create_triplet_embeddings(user, dataset)`.

* **Extraction** (`get_triplet_datapoints`) — reads graph triplets (source → relationship → target) and converts each to an embeddable text
* **Enrichment** (`index_data_points`) — indexes those texts in the vector DB under the `Triplet_text` collection

**Produces:** a searchable `Triplet_text` vector collection. Enables [`SearchType.TRIPLET_COMPLETION`](/core-concepts/main-operations/search) queries.Guide: [Triplet Embeddings Guide](/guides/memify-triplet-embeddings)

Session persistence

Calls `cognee.memify()` with session-specific tasks via `await persist_sessions_in_knowledge_graph_pipeline(user, session_ids)`. Requires [caching to be enabled](/core-concepts/sessions-and-caching).

* **Extraction** (`extract_user_sessions`) — reads Q&A data from the session cache for the specified session IDs
* **Enrichment** (`cognify_session`) — processes session data through `cognee.add` + `cognee.cognify`

**Produces:** new graph nodes from the session content, grouped under the `user_sessions_from_cache` [node set](/core-concepts/further-concepts/node-sets).Guide: [Session Persistence Guide](/guides/memify-session-persistence)

Entity consolidation

Calls `cognee.memify()` with entity-consolidation tasks via `await consolidate_entity_descriptions_pipeline()`. Useful when entity descriptions are fragmented or repetitive across chunks after [cognify](/core-concepts/main-operations/cognify).

* **Extraction** (`get_entities_with_neighborhood`) — loads `Entity` nodes along with their edges and neighbors
* **Enrichment** (`generate_consolidated_entities` → `add_data_points`) — sends each entity and its neighborhood to the LLM, which returns a refined description

**Produces:** updated `Entity` descriptions written back in place — no new nodes are created.Guide: [Entity Consolidation Guide](/guides/memify-entity-consolidation)

## Cognify

Build the knowledge graph that memify enriches

## Memify Quickstart

Run the default memify pipeline step by step

## Search

Query the enriched graph with specialized search types

---

## 3. 

## [​](#introduction) Introduction

Cognee is an open source tool and platform that transforms your raw data into intelligent, searchable memory. It combines vector search with graph databases to make your data both searchable by meaning and connected by relationships.

**Dual storage architecture** gives you both semantic search and structural reasoning

**Modular design** composes [Tasks](./building-blocks/tasks), [Pipelines](./building-blocks/pipelines), and [DataPoints](./building-blocks/datapoints)

**Main operations** handle the complete workflow from ingestion to search: add, cognify, memify, search.

## [​](#table-of-contents) Table of Contents

Architecture

Cognee uses three complementary storage systems, each playing a different role:

* **Relational store** — Tracks documents, chunks, and provenance (where data came from and how it’s linked)
* **Vector store** — Holds embeddings for semantic similarity (numerical representations that find conceptually related content)
* **Graph store** — Captures entities and relationships in a knowledge graph (nodes and edges that show connections between concepts)

This architecture makes your data both **searchable** (via vectors) and **connected** (via graphs). Cognee ships with lightweight defaults that run locally, and you can swap in production-ready backends when needed.For detailed information about the storage architecture, see [Architecture](./architecture).

Building Blocks

Cognee’s processing system is built from three fundamental components:

* **[DataPoints](./building-blocks/datapoints)** — Structured data units that become graph nodes, carrying both content and metadata for indexing
* **[Tasks](./building-blocks/tasks)** — Individual processing units that transform data, from text analysis to relationship extraction
* **[Pipelines](./building-blocks/pipelines)** — Orchestration of Tasks into coordinated workflows, like assembly lines for data transformation

These building blocks work together to create a flexible system where you can:

* Use built-in Tasks for common operations
* Create custom Tasks for domain-specific logic by extending DataPoints
* Compose Tasks into Pipelines that match your workflow

Main Operations

Cognee provides four main operations that users interact with:

* **[Add](./main-operations/add)** — Ingest and prepare data for processing, handling various file formats and data sources
* **[Cognify](./main-operations/cognify)** — Create knowledge graphs from processed data through cognitive processing and entity extraction
* **[Memify](./main-operations/memify)** — Optional post-cognify enrichment that adds derived nodes and edges (e.g., coding rules, triplet embeddings) to an existing graph
* **[Search](./main-operations/search)** — Query and retrieve information using semantic similarity, graph traversal, or hybrid approaches

**Note:** Search works with the basic Add → Cognify → Search workflow. Memify is an optional step that enriches the graph with additional derived knowledge.

Further Concepts

Beyond the core workflow, Cognee offers advanced features for sophisticated knowledge management:

* **[Node Sets](./further-concepts/node-sets)** — Tagging and organization system that helps categorize and filter your knowledge base content
* **[Agent Memory Decorator](./further-concepts/agent-memory-decorator)** — A clean way to attach Cognee memory retrieval to an async agent function
* **[Ontologies](./further-concepts/ontologies)** — External knowledge grounding through RDF/XML ontologies that connect your data to established knowledge structures
* **[Loaders](./further-concepts/loaders)** — Components that handle reading and normalizing various file formats into text
* **[Chunkers](./further-concepts/chunkers)** — Tools for splitting documents into manageable pieces for processing and embedding

These concepts extend Cognee’s capabilities for:

* **Organization** — Managing growing knowledge bases with systematic tagging
* **Knowledge grounding** — Connecting your data to external, validated knowledge sources
* **Domain expertise** — Leveraging existing ontologies for specialized fields like medicine, finance, or research

## [​](#next-steps) Next steps

A good way to learn Cognee is to start with its [architecture](./architecture), move on to [building blocks](./building-blocks/datapoints), practice the [main operations](./main-operations/add), and finally explore [advanced features](./further-concepts/node-sets).

## Architecture

Understand Cognee’s three storage systems and how they work together

## Building Blocks

Learn about DataPoints, Tasks, and Pipelines that power the system

## Main Operations

Master Add, Cognify, and Search operations for your workflows

---

## 4. Mix labelled and plain items in one call

## [​](#what-is-the-add-operation) What is the add operation

The `.add` operation is how you bring content into Cognee. It takes your files, directories, or raw text, normalizes them into plain text, and records them into a dataset that Cognee can later expand into vectors and graphs with [Cognify](../main-operations/cognify).

* **Ingestion-only**: no embeddings, no graph yet
* **Flexible input**: raw text, local files, directories, any [Docling](https://github.com/docling-project/docling) supported format or S3 URIs
* **Normalized storage**: everything is turned into text and stored consistently
* **Deduplicated**: Cognee uses content hashes to avoid duplicates
* **Dataset-first**: everything you add goes into a dataset
  + Datasets are how Cognee keeps different collections organized (e.g. “research-papers”, “customer-reports”)
  + Each dataset has its own ID, owner, and permissions for access control
  + You can read more about them below

## [​](#where-add-fits) Where add fits

* First step before you run [Cognify](../main-operations/cognify)
* Use it to **create a dataset** from scratch, or **append new data** over time
* Ideal for both local experiments and programmatic ingestion from storage (e.g. S3)

## [​](#what-happens-under-the-hood) What happens under the hood

1. **Expand your input**
   * Directories are walked, S3 paths are expanded, raw text is passed through
   * Result: a flat list of items (files, text, handles)
2. **Ingest and register**
   * Files are saved into Cognee’s storage and converted to text
   * Cognee computes a stable content hash to prevent duplicates
   * Each item becomes a record in the database and is attached to your dataset
   * **Text extraction**: Converts various file formats into plain text
   * **Metadata preservation**: Keeps file-system metadata like name, extension, MIME type, file size, and content hash — not arbitrary user-defined fields
   * **Content normalization**: Ensures consistent text encoding and formatting
3. **Return a summary**
   * You get a pipeline run info object that tells you where everything went and which dataset is ready for the next step

## [​](#after-add-finishes) After add finishes

After `.add` completes, your data is ready for the next stage:

* **Files are safely stored** in Cognee’s storage system with metadata preserved
* **Database records** track each ingested item and link it to your dataset
* **Dataset is prepared** for transformation with [Cognify](../main-operations/cognify) — which will chunk, embed, and connect everything

## [​](#further-details) Further details

Input sources

* Mix and match: `["some text", "/path/to/file.pdf", "s3://bucket/data.csv"]`
* Works with directories (recursively), S3 prefixes, and file handles
* Local and cloud sources are normalized into the same format

Structured data (dlt)

Cognee integrates with [dlt](https://dlthub.com/) to ingest structured relational data directly into the knowledge graph:

* **dlt resources**: Pass `@dlt.resource()` decorated generators directly to `cognee.add()`
* **CSV files**: `.csv` files are auto-detected and ingested via dlt
* **Database connections**: Pass a connection string (`postgresql://...`, `sqlite:///...`) to ingest tables directly
* Foreign key relationships become graph edges automatically
* Structured data bypasses LLM extraction — the graph is built deterministically from the schema
* See the full [dlt integration guide](/integrations/dlt-integration) for details

Supported formats

Cognee automatically selects the best loader based on file extension. The table below lists all supported extensions and whether optional extras are needed:

| Loader | Extensions | Install extra |
| --- | --- | --- |
| **TextLoader** | `.txt` `.md` `.json` `.xml` `.yaml` `.yml` `.log` | — (built-in) |
| **CsvLoader** | `.csv` | — (built-in) |
| **PyPdfLoader** | `.pdf` | — (built-in) |
| **ImageLoader** | `.png` `.jpg` `.jpeg` `.gif` `.webp` `.bmp` `.tif` `.tiff` `.heic` `.avif` `.ico` `.psd` `.apng` `.cr2` `.dwg` `.xcf` `.jxr` `.jpx` | — (built-in) |
| **AudioLoader** | `.mp3` `.wav` `.aac` `.flac` `.ogg` `.m4a` `.mid` `.amr` `.aiff` | — (built-in) |
| **UnstructuredLoader** | `.docx` `.doc` `.odt` `.xlsx` `.xls` `.ods` `.pptx` `.ppt` `.odp` `.rtf` `.html` `.htm` `.eml` `.msg` `.epub` | `pip install cognee[docs]` |
| **AdvancedPdfLoader** | `.pdf` (layout-aware, preserves tables) | `pip install cognee[docs]` |
| **BeautifulSoupLoader** | `.html` | `pip install cognee[scraping]` |

* **ImageLoader** uses a vision-capable LLM to describe image content.
* **AudioLoader** transcribes audio using a Whisper-compatible model.
* **AdvancedPdfLoader** preserves page layout and table structure; falls back to PyPdfLoader automatically on error.
* Cognee can also ingest the `DoclingDocument` format directly — any format [Docling](https://github.com/docling-project/docling) supports can be pre-converted and passed to `cognee.add()`.

You can learn more about how loaders work, override defaults, or register custom loaders in the [Loaders](/core-concepts/further-concepts/loaders) section.

Datasets

* A dataset is your “knowledge base” — a grouping of related data that makes sense together
* Datasets are **first-class objects in Cognee’s database** with their own ID, name, owner, and permissions
* They provide **scope**: `.add` writes into a dataset, [Cognify](../main-operations/cognify) processes per-dataset
* Think of them as separate shelves in your library — e.g., a “research-papers” dataset and a “customer-reports” dataset
* If you name a dataset that doesn’t exist, Cognee creates it for you; if you don’t specify, a default one is used
* More detail: [Datasets](/core-concepts/further-concepts/datasets)

Users and ownership

* Every dataset and data item belongs to a user
* If you don’t pass a user, Cognee creates/uses a default one
* Ownership controls who can later read, write, or share that dataset

Node sets

* Optional labels to group or tag data on ingestion
* Example: `node_set=["AI", "FinTech"]`
* Useful later when you want to focus on subgraphs
* More detail: [NodeSets](/core-concepts/further-concepts/node-sets)

Custom metadata and labeling

`cognee.add()` automatically preserves only **file-system metadata** like name, MIME type, extension, content hash.If you need to associate extra information with ingested data, three mechanisms are available:**1. `node_set` — categorical tags applied to a whole batch**Pass a list of string tags to mark every item in that `add()` call:

```
await cognee.add(
    "Quarterly earnings report Q4 2024.",
    node_set=["finance", "Q4-2024"]
)
```

Tags flow into the knowledge graph as `NodeSet` nodes connected with `belongs_to_set` edges, and can be used to scope searches later — see [NodeSets](/core-concepts/further-concepts/node-sets).**2. `DataItem` — per-item string label**Wrap individual data items in `DataItem` to attach a single string label to each one. The label is stored in the relational database alongside the ingested record.

```
from cognee.tasks.ingestion.data_item import DataItem

await cognee.add(
    DataItem(data="/path/to/report.pdf", label="q4-earnings-report")
)

# Mix labelled and plain items in one call
await cognee.add([
    DataItem(data="Contract text …", label="contract-2024"),
    DataItem(data="Meeting notes …", label="meeting-2024-03"),
])
```

**3. `dataset_name` — logical grouping**Separate collections of data into [named datasets](/core-concepts/further-concepts/datasets) to keep different knowledge domains apart:

```
await cognee.add("Legal contract text.", dataset_name="legal-docs")
await cognee.add("Product spec text.",   dataset_name="product-specs")
```

**Limitation**Arbitrary key-value metadata (e.g. `{"source": "CRM", "author": "Alice"}`) cannot currently be attached via `add()`. If rich metadata is important for your use case, consider encoding it as part of the text content itself, or combine [datasets](/core-concepts/further-concepts/datasets) (via `dataset_name`) and [NodeSets](/core-concepts/further-concepts/node-sets) (via `node_set`) to represent the dimensions you care about.

Troubleshooting 409 Conflict errors

`POST /api/v1/add` returns **409 Conflict** whenever an unhandled exception occurs during the add operation. It is a catch-all — the actual problem is always in the `error` field of the response body:

```
{
  "error": "<description of what went wrong>"
}
```

Read that message first. The table below maps the most common error patterns to their fixes.

| Symptom (error field contains…) | Cause | Fix |
| --- | --- | --- |
| `"API key"`, `"authentication"`, `"invalid_api_key"`, `"401"` | Missing or invalid LLM API key | Set `LLM_API_KEY` in your environment (`.env` file or shell). Even though `add` itself does not call the LLM, the database setup that runs on every request uses the configured provider. |
| `"connection refused"`, `"could not connect"`, `"timeout"`, `"OperationalError"` | Database unreachable | Verify your database service is running. For Docker setups, use `DB_HOST=host.docker.internal` instead of `localhost`. Check `DB_HOST`, `DB_PORT`, `DB_USERNAME`, `DB_PASSWORD`, and `DB_NAME`. |
| `"permission denied"`, `"not authorized"`, `"forbidden"`, `"403"` | The authenticated user lacks write access to the target dataset | Either use `datasetId` of a dataset you own, or disable access control with `ENABLE_BACKEND_ACCESS_CONTROL=False` in development. |
| `"decode"`, `"encoding"`, `"UnicodeDecodeError"`, `"failed to process"` | Corrupted or non-text file content | Confirm the file is readable and in a [supported format](/core-concepts/main-operations/add#supported-formats). As a workaround, read the file yourself and pass the text string directly instead of a file path. |
| `"No such file or directory"`, `"FileNotFoundError"` | The file path does not exist on the server | Use an absolute path. If calling the HTTP API, upload the file as a multipart form attachment instead of passing a path string. |
| `"SSL"`, `"certificate"` | TLS/certificate issue connecting to an external database or S3 | Check SSL settings for your database or storage backend. Set `DB_SSL=false` in development if certificates are self-signed. |

### [​](#enabling-debug-logs) Enabling debug logs

For errors not covered above, enable verbose logging to see the full stack trace:

```
LITELLM_LOG="DEBUG"
ENV="development"
```

Then re-run the request. The server logs will show exactly where the failure occurred.

### [​](#still-stuck) Still stuck?

* Check [Setup Configuration](/setup-configuration/overview) to verify your environment variables.
* Ask in the [Discord community](https://discord.gg/m63hxKsp4p) with the full `error` field from the 409 response.
* Open an issue on [GitHub](https://github.com/topoteretes/cognee/issues).

## Cognify

Expand data into chunks, embeddings, and graphs

## DataPoints

The units you’ll see after Cognify

## Building Blocks

Learn about Tasks and Pipelines behind Add

---

## 5. 

Configure Cognee to use your preferred LLM, embedding engine, relational database, vector store, and graph store via environment variables in a local `.env` file.
This section provides beginner-friendly guides for setting up different backends, with detailed technical information available in expandable sections.

## [​](#what-you-can-configure) What You Can Configure

Cognee uses a flexible architecture that lets you choose the best tools for your needs. We recommend starting with the defaults to get familiar with Cognee, then customizing each component as needed:

* **[LLM Providers](./llm-providers)** — Choose from OpenAI, Azure OpenAI, Google Gemini, Anthropic, Ollama, or custom providers (like vLLM) for text generation and reasoning tasks
* **[Structured Output Backends](./structured-output-backends)** — Configure LiteLLM + Instructor or BAML for reliable data extraction from LLM responses
* **[Embedding Providers](./embedding-providers)** — Select from OpenAI, Azure OpenAI, Google Gemini, Mistral, Ollama, Fastembed, or custom embedding services to create vector representations for semantic search
* **[Relational Databases](./relational-databases)** — Use SQLite for local development or Postgres for production to store metadata, documents, and system state
* **[Vector Stores](./vector-stores)** — Store embeddings in LanceDB, PGVector, Qdrant, Redis, ChromaDB, FalkorDB, or Neptune Analytics for similarity search
* **[Graph Stores](./graph-stores)** — Build knowledge graphs with Kuzu, Kuzu-remote, Neo4j, Neptune, Neptune Analytics, or Memgraph to manage relationships and reasoning
* **[Dataset Separation & Access Control](./permissions)** — Configure dataset-level permissions and isolation
* **[Sessions & Caching](../core-concepts/sessions-and-caching)** — Enable conversational memory with Redis or filesystem cache adapters

Want to run Cognee without a cloud API key? See the [Local Setup guide](/guides/local-setup) for step-by-step instructions using Ollama and Fastembed.

## [​](#environment-variable-quick-reference) Environment Variable Quick Reference

The tables below list the most commonly used configuration variables. For full details on each group, follow the links to the dedicated guides.

Only a small number of internal variables use the `COGNEE_` prefix: `COGNEE_LOGS_DIR`, `COGNEE_TRACING_ENABLED`, `COGNEE_CLOUD_API_URL`, and `COGNEE_CLOUD_AUTH_TOKEN`. All other configuration keys (LLM, embedding, database, etc.) are used without any prefix.

LLM

| Variable | Default | Description |
| --- | --- | --- |
| `LLM_PROVIDER` | `openai` | Provider: `openai`, `azure`, `gemini`, `anthropic`, `ollama`, `mistral`, `bedrock`, `custom` |
| `LLM_MODEL` | `openai/gpt-4o-mini` | Model in `provider/model-name` format |
| `LLM_API_KEY` | — | API key for the LLM provider |
| `LLM_ENDPOINT` | — | Custom endpoint URL (required for Ollama, vLLM, etc.) |
| `LLM_API_VERSION` | — | API version (required for Azure) |
| `LLM_TEMPERATURE` | `0.0` | Response temperature (0.0–2.0) |

Embeddings

| Variable | Default | Description |
| --- | --- | --- |
| `EMBEDDING_PROVIDER` | `openai` | Provider: `openai`, `ollama`, `fastembed`, `gemini`, `mistral`, `bedrock`, `custom` |
| `EMBEDDING_MODEL` | `openai/text-embedding-3-large` | Model in `provider/model-name` format |
| `EMBEDDING_DIMENSIONS` | `3072` | Vector dimension size (must match your vector store) |
| `EMBEDDING_API_KEY` | — | API key (falls back to `LLM_API_KEY` if unset) |
| `EMBEDDING_ENDPOINT` | — | Custom endpoint URL (required for Ollama, etc.) |
| `HUGGINGFACE_TOKENIZER` | — | HuggingFace Hub model ID for token counting with Ollama (e.g. `nomic-ai/nomic-embed-text-v1.5`) |

Databases

| Variable | Default | Description |
| --- | --- | --- |
| `DB_PROVIDER` | `sqlite` | Relational DB: `sqlite`, `postgres` |
| `DB_HOST` / `DB_PORT` / `DB_USERNAME` / `DB_PASSWORD` | — | Postgres connection details |
| `VECTOR_DB_PROVIDER` | `lancedb` | Vector store: `lancedb`, `pgvector`, `qdrant`, `chromadb`, `weaviate`, `milvus` |
| `VECTOR_DB_URL` | — | Vector store connection URL |
| `GRAPH_DATABASE_PROVIDER` | `kuzu` | Graph store: `kuzu`, `kuzu-remote`, `neo4j`, `neptune` |
| `GRAPH_DATABASE_URL` | — | Graph store connection URL |
| `GRAPH_DATABASE_USERNAME` / `GRAPH_DATABASE_PASSWORD` | — | Graph store credentials |

Storage & Logging

| Variable | Default | Description |
| --- | --- | --- |
| `STORAGE_BACKEND` | `local` | Storage backend: `local`, `s3` |
| `DATA_ROOT_DIRECTORY` | `.data_storage` | Root directory for data files |
| `SYSTEM_ROOT_DIRECTORY` | `.cognee_system` | Root directory for system files |
| `COGNEE_LOGS_DIR` | `{package}/logs` | Override the logs directory path |
| `LOG_LEVEL` | `INFO` | Logging level: `DEBUG`, `INFO`, `WARNING`, `ERROR` |
| `TELEMETRY_DISABLED` | `false` | Set `true` to disable anonymous telemetry |

Debug Mode

To enable verbose logging in a self-hosted Cognee instance, set `LOG_LEVEL` in your `.env`:

```
LOG_LEVEL="DEBUG"
```

Verbose logging covers pipeline execution, LLM calls, database queries, and graph operations—useful when troubleshooting data processing or provider configuration.

## [​](#docker-environment-variables) Docker Environment Variables

Use the same variable names as in your `.env`; pass them with `docker run -e` or load them from a file with `--env-file`.

Examples

```
docker run \
  -e LLM_PROVIDER=ollama \
  -e LLM_MODEL=ollama/llama3.2 \
  -e LLM_ENDPOINT=http://host.docker.internal:11434 \
  -e EMBEDDING_PROVIDER=ollama \
  -e EMBEDDING_MODEL=nomic-embed-text:latest \
  -e EMBEDDING_ENDPOINT=http://host.docker.internal:11434/api/embed \
  -e EMBEDDING_DIMENSIONS=768 \
  -e HUGGINGFACE_TOKENIZER=nomic-ai/nomic-embed-text-v1.5 \
  cognee/cognee:main
```

Or using an env file:

```
docker run --env-file .env cognee/cognee:main
```

## [​](#observability-&-telemetry) Observability & Telemetry

Cognee includes built-in telemetry to help you monitor and debug your knowledge graph operations. You can control telemetry behavior with environment variables:

* **`TELEMETRY_DISABLED`** (boolean, optional): Set to `true` to disable all telemetry collection (default: `false`)

When telemetry is enabled, Cognee automatically collects:

* Search query performance metrics
* Processing pipeline execution times
* Error rates and debugging information
* System resource usage

Telemetry data helps improve Cognee’s performance and reliability. It’s collected anonymously and doesn’t include your actual data content.

## [​](#configuration-workflow) Configuration Workflow

1. Install Cognee with all optional dependencies:
   * **Local setup**: `uv sync --all-extras`
   * **Library**: `pip install "cognee[all]"`
2. Create a `.env` file in your project root (if you haven’t already) — see [Installation](/getting-started/installation) for details
3. Choose your preferred providers and follow the configuration instructions from the guides below

**Configuration Changes**: If you’ve already run Cognee with default settings and are now changing your configuration (e.g., switching from SQLite to Postgres, or changing vector stores), you should call pruning operations before the next cognification to ensure data consistency.

**LLM/Embedding Configuration**: If you configure only LLM or only embeddings, the other defaults to OpenAI. Ensure you have a working OpenAI API key, or configure both LLM and embeddings to avoid unexpected defaults.

## LLM Providers

Configure OpenAI, Azure, Gemini, Anthropic, Ollama, or custom LLM providers (like vLLM)

## Structured Output Backends

Configure LiteLLM + Instructor or BAML for reliable data extraction

## Embedding Providers

Set up OpenAI, Mistral, Ollama, Fastembed, or custom embedding services

## Relational Databases

Choose between SQLite for local development or Postgres for production

## Vector Stores

Configure LanceDB, PGVector, Qdrant, Redis, ChromaDB, FalkorDB, or Neptune Analytics

## Graph Stores

Set up Kuzu, Neo4j, or Neptune for knowledge graph storage

---

## 6. cognify

## [​](#what-is-the-cognify-operation) What is the cognify operation

The `.cognify` operation takes the ingested data with [Add](../main-operations/add) and turns plain text into structured knowledge: chunks, embeddings, summaries, nodes, and edges that live in Cognee’s vector and graph stores. It prepares your data for downstream operations like [Search](../main-operations/search).

* **Transforms ingested data**: builds chunks, embeddings, and summaries
* **Graph creation**: extracts entities and relationships to form a knowledge graph
* **Vector indexing**: makes everything searchable via embeddings
* **Dataset-scoped**: runs per dataset, respecting ownership and permissions

`.cognify` can be run multiple times as the dataset grows, and Cognee will skip what’s already processed. Read more about **Incremental loading** in **[Examples and details](#examples-and-details)**

## [​](#what-happens-under-the-hood) What happens under the hood

The `.cognify` pipeline is made of six ordered [Tasks](../building-blocks/tasks). Each task takes the output of the previous one and moves your data closer to becoming a searchable knowledge graph.

1. **Classify documents** — wrap each ingested file as a `Document` object with metadata and optional node sets
2. **Check permissions** — enforce that you have write access to the target dataset
3. **Extract chunks** — split documents into smaller pieces (paragraphs, sections)
4. **Extract graph** — use LLMs to identify entities and relationships, inserting them into the graph DB
5. **Summarize text** — generate summaries for each chunk, stored as `TextSummary` [DataPoints](../building-blocks/datapoints)
6. **Add data points** — embed nodes and summaries, write them into the vector store, and update graph edges

The result is a fully searchable, structured knowledge graph connected to your data.

## [​](#after-cognify-finishes) After cognify finishes

When `.cognify` completes for a dataset:

* **DocumentChunks** exist in memory as the granular breakdown of your files
* **Summaries** are stored and indexed in the vector database for semantic search
* **Knowledge graph nodes and edges** are committed to the graph database
* **Dataset metadata** is updated with token counts and pipeline status
* Your dataset is now **query-ready**: you can run [Search](../main-operations/search) or graph queries immediately

## [​](#examples-and-details) Examples and details

Pipeline tasks (detailed)

1. **Classify documents**
   * Turns raw `Data` rows into `Document` objects
   * Chooses the right document type (PDF, text, image, audio, etc.)
   * Attaches metadata and optional node sets
2. **Check permissions**
   * Verifies that the user has write access to the dataset
3. **Extract chunks**
   * Splits documents into `DocumentChunk`s using a chunker
   * You can customize the chunk size and strategy — see [Chunkers](/core-concepts/further-concepts/chunkers) for details
   * Updates token counts in the relational DB
4. **Extract graph**
   * Calls the LLM to extract entities and relationships
   * Deduplicates nodes and edges, commits to the graph DB
5. **Summarize text**
   * Generates concise summaries per chunk
   * Stores them as `TextSummary` [DataPoints](../building-blocks/datapoints) for vector search
6. **Add data points**
   * Converts summaries and other [DataPoints](../building-blocks/datapoints) into graph + vector nodes
   * Embeds them in the vector store, persists in the graph DB

Default extraction prompts

Cognee ships with several built-in system prompts for entity and relationship extraction, stored in `cognee/infrastructure/llm/prompts/`. The active prompt is controlled by the `GRAPH_PROMPT_PATH` environment variable (default: `generate_graph_prompt.txt`).

| Prompt file | Use case | What it does |
| --- | --- | --- |
| `generate_graph_prompt.txt` | Default balanced extraction | Extracts entities and relationships using the standard Cognee rules: basic node types, human-readable IDs, normalized dates, `snake_case` relationships, and coreference consistency. |
| `generate_graph_prompt_simple.txt` | Lightweight extraction | Uses a shorter, more compact rule set for straightforward graph extraction while keeping the same core conventions around node types, IDs, dates, and relationship naming. |
| `generate_graph_prompt_strict.txt` | Tighter schema control | Applies a more explicit prompt with named node categories, stronger relationship constraints, examples, and a strict instruction not to infer facts that are not present in the text. |
| `generate_graph_prompt_guided.txt` | More directed graph shaping | Adds guidance for edge direction, allows multi-word entity labels, and encourages logically implied facts when they improve graph clarity without repeating the same fact. |

To switch to a different built-in prompt, set the environment variable:

```
GRAPH_PROMPT_PATH=generate_graph_prompt_strict.txt
```

Or configure it at runtime via `cognee.config`:

```
import cognee

cognee.config.llm_config.graph_prompt_path = "generate_graph_prompt_strict.txt"
```

If you need to use a custom prompt, refer to our [Custom Prompts guide](../../guides/custom-prompts)

Datasets and permissions

* Cognify always runs on a dataset
* You must have **write access** to the target dataset
* Permissions are enforced at pipeline start
* Each dataset maintains its own cognify status and token counts

Incremental loading

* By default, `.cognify` processes all data in a dataset
* With `incremental_loading=True`, only new or updated files are processed
* Saves time and compute for large, evolving datasets

Re-cognify after schema changes

If you update your data model (e.g., add new entity fields or relationships) and want to reprocess existing data:

1. **Delete the dataset** first, then re-add and re-cognify:

   ```
   # Clear existing processed data
   await cognee.datasets.empty_dataset(dataset_id=my_dataset.id)

   # Re-add source files
   await cognee.add(source_files, dataset_name="my_dataset")

   # Re-cognify with the updated schema
   await cognee.cognify()
   ```
2. **Alternatively, use [Memify](/core-concepts/main-operations/memify)** for additive enrichment — it runs extraction and enrichment tasks over the existing graph without re-ingesting data. This is useful when you want to add new derived facts without reprocessing from scratch.

`.cognify` skips already-processed data by default. Simply re-running `.cognify` on unchanged files will not pick up schema changes. You must delete and re-add the data, or use memify for enrichment.

Final outcome

* Vector database contains embeddings for summaries and nodes
* Graph database contains entities and relationships
* Relational database tracks token counts and pipeline run status
* Your dataset is now ready for [Search](../main-operations/search) (semantic or graph-based)

## Add

First bring data into Cognee

## Search

Query embeddings or graph structures built by Cognify

## Memify

Enrich your graph with derived facts after cognify

---

## 7. Optional: override location

Graph stores capture entities and relationships in knowledge graphs. They enable Cognee to understand structure and navigate connections between concepts, providing powerful reasoning capabilities.

**New to configuration?**See the [Setup Configuration Overview](./overview) for the complete workflow:install extras → create `.env` → choose providers → handle pruning.

## [​](#supported-providers) Supported Providers

Cognee supports multiple graph store options:

* **Kuzu** — Local file-based graph database (default)
* **Kuzu-remote** — Kuzu with HTTP API access
* **Neo4j** — Production-ready graph database (self-hosted or Docker)
* **Neo4j Aura** — Neo4j’s fully managed cloud service
* **Neptune** — Amazon Neptune cloud graph database
* **Neptune Analytics** — Amazon Neptune Analytics hybrid solution
* **Memgraph** — In-memory graph database (community adapter)

**Local vs. cloud storage**: By default Cognee stores its graph in a local Kuzu file. To persist data in the cloud, switch to a remote provider such as Neo4j Aura, Neptune, or a self-hosted Neo4j instance on a remote server.

## [​](#configuration) Configuration

Environment Variables

Set these environment variables in your `.env` file:

* `GRAPH_DATABASE_PROVIDER` — The graph store provider (kuzu, kuzu-remote, neo4j, neptune, neptune\_analytics)
* `GRAPH_DATABASE_URL` — Database URL or connection string
* `GRAPH_DATABASE_USERNAME` — Database username (optional)
* `GRAPH_DATABASE_PASSWORD` — Database password (optional)
* `GRAPH_DATABASE_NAME` — Database name (optional)

## [​](#setup-guides) Setup Guides

Kuzu (Default)

Kuzu is file-based and requires no network setup. It’s perfect for local development and single-user scenarios.

```
GRAPH_DATABASE_PROVIDER="kuzu"
# Optional: override location
# SYSTEM_ROOT_DIRECTORY=/absolute/path/.cognee_system
# The graph file will default to <SYSTEM_ROOT_DIRECTORY>/databases/cognee_graph_kuzu
```

**Installation**: Kuzu is included by default with Cognee. No additional installation required.**Data Location**: The graph is stored on disk. Path defaults under the Cognee system directory and is created automatically.

**Concurrency Limitation**: Kuzu uses file-based locking and is not suitable for concurrent use from different agents or processes. For multi-agent scenarios, use Neo4j instead.

Kuzu (Remote API)

Use Kuzu with an HTTP API when you need remote access or want to run Kuzu as a service.

```
GRAPH_DATABASE_PROVIDER="kuzu-remote"
GRAPH_DATABASE_URL="http://localhost:8000"
GRAPH_DATABASE_USERNAME="<optional>"
GRAPH_DATABASE_PASSWORD="<optional>"
```

**Installation**: Requires a running Kuzu service exposing an HTTP API.

Neo4j (Self-Hosted)

Neo4j is recommended for production environments and multi-user scenarios. Data is stored on the Neo4j server (local or remote), not on the Cognee host machine.

```
GRAPH_DATABASE_PROVIDER="neo4j"
GRAPH_DATABASE_URL="bolt://localhost:7687"
GRAPH_DATABASE_NAME="neo4j"
GRAPH_DATABASE_USERNAME="neo4j"
GRAPH_DATABASE_PASSWORD="pleaseletmein"
```

**Installation**: Install Neo4j extras:

```
pip install "cognee[neo4j]"
```

**Docker Setup**: Start the bundled Neo4j service with APOC + GDS plugins:

```
docker compose --profile neo4j up -d
```

Neo4j Aura (Cloud)

[Neo4j Aura](https://neo4j.com/docs/aura/) is Neo4j’s fully managed cloud service. Graph data is stored in Neo4j’s cloud infrastructure — nothing is stored locally on your machine.There are two ways to use Neo4j Aura with Cognee:**Option 1 — Connect to an existing Aura instance**Create a free or paid Aura instance at [console.neo4j.io](https://console.neo4j.io), then point Cognee at it using the `neo4j+s://` connection URI provided in your Aura console:

```
GRAPH_DATABASE_PROVIDER="neo4j"
GRAPH_DATABASE_URL="neo4j+s://<your-instance-id>.databases.neo4j.io"
GRAPH_DATABASE_NAME="neo4j"
GRAPH_DATABASE_USERNAME="neo4j"
GRAPH_DATABASE_PASSWORD="<your-aura-password>"
```

**Option 2 — Auto-provisioned Aura instances per dataset (multi-user mode)**Cognee’s `Neo4jAuraDevDatasetDatabaseHandler` can automatically create and delete a dedicated Neo4j Aura instance for each Cognee dataset. This requires Neo4j Aura API credentials (OAuth):

```
GRAPH_DATABASE_PROVIDER="neo4j"
GRAPH_DATASET_DATABASE_HANDLER="neo4j_aura_dev"
NEO4J_CLIENT_ID=<your_oauth_client_id>
NEO4J_CLIENT_SECRET=<your_oauth_client_secret>
NEO4J_TENANT_ID=<your_aura_tenant_id>
NEO4J_ENCRYPTION_KEY=<key_for_encrypting_stored_credentials>
```

See the [Neo4j Aura Dataset Database Handler](/core-concepts/multi-user-mode/dataset-database-handlers/existing-dataset-database-handlers/neo4j-aura-dev) page for full details on Option 2.**Installation**: Install Neo4j extras:

```
pip install "cognee[neo4j]"
```

Neptune (Graph-only)

Use Amazon Neptune for cloud-based graph storage.

```
GRAPH_DATABASE_PROVIDER="neptune"
GRAPH_DATABASE_URL="neptune://<GRAPH_ID>"
# AWS credentials via environment or default SDK chain
```

**Installation**: Install Neptune extras:

```
pip install "cognee[neptune]"
```

**Note**: AWS credentials should be configured via environment variables or AWS SDK.

Neptune Analytics (Hybrid)

Use Amazon Neptune Analytics as a hybrid vector + graph backend.

```
GRAPH_DATABASE_PROVIDER="neptune_analytics"
GRAPH_DATABASE_URL="neptune-graph://<GRAPH_ID>"
# AWS credentials via environment or default SDK chain
```

**Installation**: Install Neptune extras:

```
pip install "cognee[neptune]"
```

**Note**: This is the same as the vector store configuration. Neptune Analytics serves both purposes.

## [​](#advanced-options) Advanced Options

Backend Access Control

Enable per-user dataset isolation for multi-tenant scenarios.

```
ENABLE_BACKEND_ACCESS_CONTROL="true"
```

This feature is available for Kuzu and other supported graph stores.

## [​](#provider-comparison) Provider Comparison

Graph Store Comparison

| Provider | Data Location | Setup | Performance | Use Case |
| --- | --- | --- | --- | --- |
| Kuzu | Local disk | Zero setup | Good | Local development |
| Kuzu-remote | Remote server | Server required | Good | Remote access |
| Neo4j (self-hosted) | Neo4j server | Server required | Excellent | Production |
| Neo4j Aura | Neo4j cloud | Aura account required | Excellent | Managed cloud |
| Neptune | AWS cloud | AWS required | Excellent | Cloud solution |
| Neptune Analytics | AWS cloud | AWS required | Excellent | Hybrid cloud solution |

## [​](#important-considerations) Important Considerations

Data Location

* **Local providers** (Kuzu): Graph files are created automatically under `SYSTEM_ROOT_DIRECTORY`
* **Remote providers** (Neo4j, Neptune): Require running services or cloud setup
* **Path management**: Local graphs are managed automatically, no manual path configuration needed

Performance Notes

* **Kuzu**: Single-file storage with good local performance
* **Neo4j**: Excellent for production workloads with proper indexing
* **Neptune**: Cloud-scale performance with managed infrastructure
* **Hybrid solutions**: Combine graph and vector capabilities in one system

## [​](#community-maintained-providers) Community-Maintained Providers

Additional graph stores are available through community-maintained adapters:

* **[Memgraph](/setup-configuration/community-maintained/memgraph)** — In-memory graph database (Bolt protocol)

## [​](#notes) Notes

* **Backend Access Control**: When enabled, Kuzu supports per-user dataset isolation
* **Path Management**: Local Kuzu databases are created automatically under the system directory
* **Cloud Integration**: Neptune providers require AWS credentials and proper IAM permissions

## Vector Stores

Configure vector databases for embedding storage

## Relational Databases

Set up SQLite or Postgres for metadata storage

## Overview

Return to setup configuration overview

---

## 8. Optional, can be a path or URL. Defaults to <SYSTEM_ROOT_DIRECTORY>/databases/cognee.lancedb

Vector stores hold embeddings for semantic similarity search. They enable Cognee to find conceptually related content based on meaning rather than exact text matches.

**New to configuration?**See the [Setup Configuration Overview](./overview) for the complete workflow:install extras → create `.env` → choose providers → handle pruning.

## [​](#supported-providers) Supported Providers

Cognee supports multiple vector store options:

* **LanceDB** — File-based vector store, works out of the box (default)
* **PGVector** — Postgres-backed vector storage with pgvector extension
* **Qdrant** — High-performance vector database and similarity search engine
* **Redis** — Fast vector similarity search via Redis Search module
* **ChromaDB** — HTTP server-based vector database
* **FalkorDB** — Hybrid graph + vector database
* **Neptune Analytics** — Amazon Neptune Analytics hybrid solution

## [​](#configuration) Configuration

Environment Variables

Set these environment variables in your `.env` file:

* `VECTOR_DB_PROVIDER` — The vector store provider (lancedb, pgvector, qdrant, redis, chromadb, falkordb, neptune\_analytics)
* `VECTOR_DB_URL` — Database URL or connection string
* `VECTOR_DB_KEY` — Authentication key (provider-specific)
* `VECTOR_DB_PORT` — Database port (for some providers)

## [​](#setup-guides) Setup Guides

LanceDB (Default)

LanceDB is file-based and requires no additional setup. It’s perfect for local development and single-user scenarios.

```
VECTOR_DB_PROVIDER="lancedb"
# Optional, can be a path or URL. Defaults to <SYSTEM_ROOT_DIRECTORY>/databases/cognee.lancedb
# VECTOR_DB_URL=/absolute/or/relative/path/to/cognee.lancedb
```

**Installation**: LanceDB is included by default with Cognee. No additional installation required.**Data Location**: Vectors are stored in a local directory. Defaults under the Cognee system path if `VECTOR_DB_URL` is empty.

PGVector

PGVector stores vectors inside your Postgres database using the pgvector extension.

```
VECTOR_DB_PROVIDER="pgvector"
# Uses the same Postgres connection as your relational DB (DB_HOST, DB_PORT, DB_NAME, DB_USERNAME, DB_PASSWORD)
```

**Installation**: Install the Postgres extras:

```
pip install "cognee[postgres]"
# or for binary version
pip install "cognee[postgres-binary]"
```

**Docker Setup**: Use the built-in Postgres with pgvector:

```
docker compose --profile postgres up -d
```

**Note**: If using your own Postgres, ensure `CREATE EXTENSION IF NOT EXISTS vector;` is available in the target database.

Qdrant

Qdrant requires a running instance of the Qdrant server.

```
VECTOR_DB_PROVIDER="qdrant"
VECTOR_DB_URL="http://localhost:6333"
```

**Installation**: Since Qdrant is a community adapter, you have to install the community package:

```
pip install cognee-community-vector-adapter-qdrant
```

**Configuration**: To make sure Cognee uses Qdrant, you have to register it beforehand with the following line:

```
from cognee_community_vector_adapter_qdrant import register
```

For more details on setting up Qdrant, visit the [more detailed description](/setup-configuration/community-maintained/qdrant) of this adapter.**Docker Setup**: Start the Qdrant service:

```
docker run -p 6333:6333 -p 6334:6334 \
    -v "$(pwd)/qdrant_storage:/qdrant/storage:z" \
    qdrant/qdrant
```

**Access**: Default port is 6333 for the database, and you can access the Qdrant dashboard at “localhost:6333/dashboard”.

Redis

Redis can be used as a vector store through the Redis Search module, providing fast vector similarity search capabilities.

```
VECTOR_DB_PROVIDER="redis"
VECTOR_DB_URL="redis://localhost:6379"
# VECTOR_DB_KEY is optional and not used by Redis
```

**Installation**: Since Redis is a community adapter, you have to install the community package:

```
pip install cognee-community-vector-adapter-redis
```

**Configuration**: To make sure Cognee uses Redis, you have to register it beforehand with the following line:

```
from cognee_community_vector_adapter_redis import register
```

You can also configure Redis programmatically:

```
from cognee import config

config.set_vector_db_config({
    "vector_db_provider": "redis",
    "vector_db_url": "redis://localhost:6379",
})
```

For more details on setting up Redis, visit the [more detailed description](/setup-configuration/community-maintained/redis) of this adapter.**Docker Setup**: Start a Redis instance with Search module enabled:

```
docker run -d --name redis -p 6379:6379 redis:8.0.2
```

Or use **Redis Cloud** with the Search module enabled: [Redis Cloud](https://redis.io/try-free)**Connection URL Examples**:

* Local: `redis://localhost:6379`
* With authentication: `redis://user:password@localhost:6379`
* With SSL: `rediss://localhost:6380`

ChromaDB

ChromaDB requires a running Chroma server and authentication token.

```
VECTOR_DB_PROVIDER="chromadb"
VECTOR_DB_URL="http://localhost:3002"
VECTOR_DB_KEY="<your_token>"
```

**Installation**: Install ChromaDB extras:

```
pip install "cognee[chromadb]"
# or directly
pip install chromadb
```

**Docker Setup**: Start the bundled ChromaDB server:

```
docker compose --profile chromadb up -d
```

FalkorDB

FalkorDB can serve as both graph and vector store, providing a hybrid solution.

```
VECTOR_DB_PROVIDER="falkordb"
VECTOR_DB_URL="localhost"
VECTOR_DB_PORT="6379"
```

**Installation**: Since FalkorDB is a community adapter, you have to install the community package:

```
pip install cognee-community-hybrid-adapter-falkor
```

**Configuration**: To make sure Cognee uses FalkorDB, you have to register it beforehand with the following line:

```
from cognee_community_hybrid_adapter_falkor import register
```

For more details on setting up FalkorDB, visit the [more detailed description](/setup-configuration/community-maintained/falkordb) of this adapter.**Docker Setup**: Start the FalkorDB service:

```
docker run -p 6379:6379 -p 3000:3000 -it --rm falkordb/falkordb:edge
```

**Access**: Default ports are 6379 (DB) and 3000 (UI).

Neptune Analytics

Use Amazon Neptune Analytics as a hybrid vector + graph backend.

```
VECTOR_DB_PROVIDER="neptune_analytics"
VECTOR_DB_URL="neptune-graph://<GRAPH_ID>"
# AWS credentials via environment or default SDK chain
```

**Installation**: Install Neptune extras:

```
pip install "cognee[neptune]"
```

**Note**: URL must start with `neptune-graph://` and AWS credentials should be configured via environment variables or AWS SDK.

## [​](#important-considerations) Important Considerations

Dimension Consistency

Ensure `EMBEDDING_DIMENSIONS` matches your vector store collection/table schemas:

* PGVector column size
* LanceDB Vector size
* ChromaDB collection schema

Changing dimensions requires recreating collections.

Provider Comparison

| Provider | Setup | Performance | Use Case |
| --- | --- | --- | --- |
| LanceDB | Zero setup | Good | Local development |
| PGVector | Postgres required | Excellent | Production with Postgres |
| Qdrant | Server required | Excellent | High-performance vector search |
| Redis | Server required | Excellent | Low-latency in-memory search |
| ChromaDB | Server required | Good | Dedicated vector store |
| FalkorDB | Server required | Good | Hybrid graph + vector |
| Neptune Analytics | AWS required | Excellent | Cloud hybrid solution |

## [​](#community-maintained-providers) Community-Maintained Providers

Additional vector stores are available through community-maintained adapters:

* **[Qdrant](/setup-configuration/community-maintained/qdrant)** — Vector search engine with cloud and self-hosted options
* **[Redis](/setup-configuration/community-maintained/redis)** — Fast vector similarity search
* **[FalkorDB](/setup-configuration/community-maintained/falkordb)** — Hybrid vector and graph store
* **[Turbopuffer](/setup-configuration/community-maintained/turbopuffer)** — High-performance vector database
* **Milvus, Pinecone, Weaviate, and more** — See [all community adapters](/setup-configuration/community-maintained/overview)

## [​](#notes) Notes

* **Embedding Integration**: Vector stores use your embedding engine from the Embeddings section
* **Dimension Matching**: Keep `EMBEDDING_DIMENSIONS` consistent between embedding provider and vector store
* **Performance**: Local providers (LanceDB) are simpler but cloud providers offer better scalability

## Embedding Providers

Configure embedding providers for vector generation

## Graph Stores

Set up graph databases for knowledge graphs

## Overview

Return to setup configuration overview

---

## 9. [​](#datapoints-atomic-units-of-knowledge) DataPoints: Atomic Units of Knowledge

DataPoints are the smallest building blocks in Cognee.  
They represent **atomic units of knowledge** — carrying both your actual content and the context needed to process, index, and connect it.
They’re the reason Cognee can turn raw documents into something that’s both **searchable** (via vectors) and **connected** (via graphs).

## [​](#what-are-datapoints) What are DataPoints

* **Atomic** — each DataPoint represents one concept or unit of information.
* **Structured** — implemented as [Pydantic](https://docs.pydantic.dev/) models for validation and serialization.
* **Contextual** — carry provenance, versioning, and indexing hints so every step downstream knows where data came from and how to use it.

## [​](#core-structure) Core Structure

A DataPoint is just a Pydantic model with a set of standard fields.

See example class definition

```
class DataPoint(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    created_at: int = ...
    updated_at: int = ...
    version: int = 1
    topological_rank: Optional[int] = 0
    metadata: Optional[dict] = {"index_fields": []}
    type: str = "DataPoint"
    belongs_to_set: Optional[List["DataPoint"]] = None
```

Key fields:

* `id` — unique identifier (shared across all three stores, linking vector, graph, and relational records for the same DataPoint)
* `created_at`, `updated_at` — timestamps (ms since epoch)
* `version` — for tracking changes and schema evolution
* `topological_rank` — an integer indicating the DataPoint’s position in a dependency hierarchy. Lower ranks mean fewer dependencies. For example, an `Entity` that other DataPoints reference would have a lower rank than a `TextSummary` that depends on it. Defaults to `0`.
* `metadata.index_fields` — critical: determines which fields are embedded for vector search
* `type` — the Python class name of the DataPoint subclass (e.g., `"Person"`, `"Book"`)
* `belongs_to_set` — groups related DataPoints

## [​](#indexing-&-embeddings) Indexing & Embeddings

The `metadata.index_fields` tells Cognee which fields to embed into the vector store.
This is the mechanism behind semantic search.

* Fields in `index_fields` → converted into embeddings
* Each indexed field → its own vector collection named `Class_field` (e.g., a `Person` DataPoint with `index_fields=["name"]` creates a `Person_name` vector collection). The `Class` part comes from the Python class name of your DataPoint subclass.
* Non-indexed fields → stay as regular properties in the graph and relational stores
* Choosing what to index controls search granularity

**Cross-store retrieval:** When a vector search finds a match, Cognee uses the shared `id` to retrieve the full DataPoint from the graph store, which holds all properties (not just the indexed field). This is how Cognee returns complete results from a semantic search.

## [​](#from-datapoints-to-the-graph) From DataPoints to the Graph

When you call `add_data_points()`, Cognee automatically:

* Embeds the indexed fields into vectors
* Converts the object into **nodes** and **edges** in the knowledge graph
* Stores provenance in the relational store

This is how Cognee creates both **semantic similarity** (vector) and **structural reasoning** (graph) from the same unit.

## [​](#examples-and-details) Examples and details

Example: indexing only one field

```
class Person(DataPoint):
    name: str
    age: int
    metadata: dict = {"index_fields": ["name"]}
```

Only `"name"` is semantically searchable

Example: Book → Author transformation

```
class Book(DataPoint):
    title: str
    author: Author
    metadata: dict = {"index_fields": ["title"]}

# Produces:
# `Node(Book)` with `{title, type, ...}`
# Node(Author) with {name, type, ...}
# Edge(Book → Author, type="author")
```

Relationship syntax options

```
# Simple relationship
`author: Author`

# With edge metadata
`has_items: (Edge(weight=0.8), list[Item])`

# List relationship
`chapters: list[Chapter]`
```

Built-in DataPoint types

Cognee ships with several built-in DataPoint types:

* **Documents** — wrappers for source files (Text, PDF, Audio, Image)
  + `Document` (`metadata.index_fields=["name"]`)
* **Chunks** — segmented portions of documents
  + `DocumentChunk` (`metadata.index_fields=["text"]`)
* **Summaries** — generated text or code summaries
  + `TextSummary` / `CodeSummary` (`metadata.index_fields=["text"]`)
* **Entities** — named objects (people, places, concepts)
  + `Entity`, `EntityType` (`metadata.index_fields=["name"]`)
* **Edges** — relationships between DataPoints
  + `Edge` — links between DataPoints

Example: custom DataPoint with best practices

```
class Product(DataPoint):
    name: str
    description: str
    price: float
    category: Category

    # Index name + description for search
    metadata: dict = {"index_fields": ["name", "description"]}
```

**Best Practices:**

* **Keep it small** — one concept per DataPoint
* **Index carefully** — only fields that matter for semantic search
* **Use built-in types first** — extend with custom subclasses when needed
* **Version deliberately** — track changes with `version`
* **Group related points** — with `belongs_to_set`

## Tasks

Learn how DataPoints are created and processed

## Pipelines

See how DataPoints flow through processing workflows

## Main Operations

Understand how DataPoints are used in Add, Cognify, and Search

---

## Bibliography

1. [search](https://docs.cognee.ai/core-concepts/main-operations/search)
2. [memify](https://docs.cognee.ai/core-concepts/main-operations/memify)
3. [](https://docs.cognee.ai/core-concepts/)
4. [Mix labelled and plain items in one call](https://docs.cognee.ai/core-concepts/main-operations/)
5. [](https://docs.cognee.ai/setup-configuration/)
6. [cognify](https://docs.cognee.ai/core-concepts/main-operations/cognify)
7. [Optional: override location](https://docs.cognee.ai/setup-configuration/graph-stores)
8. [Optional, can be a path or URL. Defaults to <SYSTEM_ROOT_DIRECTORY>/databases/cognee.lancedb](https://docs.cognee.ai/setup-configuration/vector-stores)
9. [[​](#datapoints-atomic-units-of-knowledge) DataPoints: Atomic Units of Knowledge](https://docs.cognee.ai/core-concepts/building-blocks)