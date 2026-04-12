# Implicit RAG

The `docs/` directory in the POC works as a simplified [[RAG]]. No vector database, no [[Embedding|embeddings]] for semantic search -- but the pattern is the same: save knowledge -> retrieve later -> cumulative context.

---

## How It Works in the POC

**Retrieval:** `search_docs(query)` does keyword search across all `.md` files in `docs/`. It is not semantic search (by [[Vector|vectors]]), it is substring search -- but the effect is analogous: given a query, it returns relevant context.

**Augmented:** The `search_docs` result enters the [[Agent in POC]]'s [[Programmatic Context|context]]. The model generates the response based on what was retrieved, not on what it "remembers" from training.

**Generation:** The model generates using the retrieved context as [[Tool as Bias|bias]] -- the found docs shift the calculation in the correct direction.

## Retrieval -> Augmented -> Generation in the POC

```
1. Retrieval: search_docs("JWT") -> matches in architecture.md
2. Augmented: result injected into the agent's context
3. Generation: agent responds based on docs, not on the Matriz M
```

## What Is Missing for Full RAG

| Aspect | POC (Implicit RAG) | Full RAG |
|---|---|---|
| Storage | Local filesystem (`docs/`) | Vector DB (Pinecone, Weaviate, etc.) |
| Search | Keyword (substring match) | Semantic (cosine similarity of [[Embedding\|embeddings]]) |
| Indexing | None (glob + read) | [[Embedding]] of chunks + vector index |
| Persistence | `.md` files | Vectors + metadata |
| Accumulation | `crawl_docs` saves new docs | Each interaction generates new embeddings |

## Role in the Thesis

In the thesis, [[RAG]] is the "long-term memory" -- vectorizes metadata and enables semantic search across complete history. The POC's [[Implicit RAG]] is a degraded but functional version: the history is in `docs/` files, not in vectors, but the principle is the same.

The [[Ultra-Long-Horizon Agentic Science]] paper describes how accumulation of structured knowledge increases [[Determinism]] over time. In the POC, each `crawl_docs` and `save_as_doc` is concrete accumulation. The "+" of 89%+ ([[DFAH]]) comes from here.

## Path to Full RAG

The [[mcp-memory-server]] with [[Milvus]] is the direct evolution: vector similarity search across three collections (tool calls, decisions, sessions). The [[mcp-ontology-server]] with [[Neo4j]] adds relationship search in the concept graph.

The [[LLM Output Drift]] paper shows that RAG tasks are the **most sensitive to drift**. This makes the evolution from keyword search to semantic search even more critical -- semantic search returns more precise context, reducing the [[Sample Space]] more effectively.

---

Related to: [[RAG]], [[docs-server]], [[web-to-docs]], [[Deterministic Feedback Loop]], [[Programmatic Context]], [[Tool as Bias]], [[Agent in POC]], [[Ultra-Long-Horizon Agentic Science]], [[DFAH]], [[S3 as Persistent Ontology]], [[Embedding]], [[Milvus]], [[Neo4j]], [[mcp-memory-server]], [[mcp-ontology-server]], [[LLM Output Drift]]
