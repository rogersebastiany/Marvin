# Cognee

Modular framework for building and querying knowledge graphs from text. Replaced the legacy Pythonistic pipeline (`load_vaults.py`) as the KG extraction engine. The [[Agent in POC|agent]] uses Cognee indirectly -- the Obsidian vaults go through Cognee and become `:Concept` nodes in [[Neo4j]].

---

## Why Cognee

The previous pipeline used regex + classifier to map existing wikilinks into typed relations. This created a ceiling: it could only classify links that already existed in the notes, never discovering new concepts or relations. In practice, 58.2% typed edges -- the rest fell back to generic `RELATES_TO`.

Cognee solves this by using an LLM to read prose and extract entities + typed relations from context. It does not depend on pre-existing wikilinks. The paper that validated the approach -- "Optimizing the Interface Between Knowledge Graphs and LLMs for Complex Reasoning" (arXiv 2505.24478) -- shows that systematic parameter tuning (chunking, graph construction, retrieval) produces measurable gains on multi-hop reasoning benchmarks (HotPotQA, TwoWikiMultiHop, MuSiQue).

## Two Eras

**Era 1 -- Default KnowledgeGraph + post-processing.** Cognee with the default `KnowledgeGraph` model produced 13,659 edges, but with LLM typos in relation type names, mapping gaps, and 16% `RELATES_TO` fallback. Post-processing via keyword matching tried to fix this, but was fragile.

**Era 2 -- Custom Concept(DataPoint).** A `Concept` model inheriting from `DataPoint` with 16 typed relation fields (Pydantic). The JSON schema enforces types at extraction time -- the LLM cannot invent types. Result: 547 concepts, 1,844 edges, 16 exact types, zero typos.

The key was discovering the branch in Cognee's `extract_graph_from_data.py`: when `graph_model is not KnowledgeGraph`, it bypasses the default `Entity`-creating flow and writes the model's class as the Neo4j label directly.

## Rate Limiting

Cognee's `llm_rate_limit_requests` is a reactive backoff (post-429), not a preemptive throttle. With large batches, it fires dozens of parallel calls and burns the rate limit instantly. Configuration that works on OpenAI Tier 1: `chunks_per_batch=1, data_per_batch=1, llm_rate_limit_requests=2`. Runtime: ~7h for a full wipe, ~14-17 chunks/min.

## Pipeline

```
Obsidian Vaults → cognify_vaults.py → Cognee → Neo4j (:Concept)
                                                  ↓
                                    sync (ops_backend) → Milvus
```

1. `cognify_vaults.py` reads the 4 vaults and feeds Cognee with `graph_model=Concept`
2. Cognee extracts concepts and relations, persists to [[Neo4j]] and LanceDB
3. `sync_vaults` (MCP tool) or `ops_backend.sync()` re-indexes `:Concept` nodes from Neo4j into [[Milvus]]

The agent never calls Cognee directly. Cognee is ingestion infrastructure, not query infrastructure.

## Role in the Architecture

Cognee is the link between Obsidian vaults (human knowledge) and the knowledge graph (computable knowledge). Without Cognee, vault concepts would be loose text. With Cognee, each concept becomes a traversable node with typed relations -- the foundation for [[Space Reduction in Practice|space reduction]] and [[Measurable Determinism|determinism]].

---

Related to: [[Neo4j]], [[Milvus]], [[Ontology as Code]], [[Self-Improvement Loop]], [[Agent in POC]]
