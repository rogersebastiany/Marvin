# Self-Improvement Loop

The cycle in which the [[Agent in POC|agent]] uses its own ontology ([[Neo4j]]) and memory ([[Milvus]]) to improve itself. Each action enriches the context for the next action. The system becomes more deterministic with use.

---

## The Cycle

```
1. Agent receives objective
2. Queries Neo4j (mcp-ontology-server): "What do I know about this domain?"
3. Queries Milvus (mcp-memory-server): "Have I done something similar before?"
4. Acts informed -- with ontological context + episodic memory
5. Logs the action in Milvus (tool call, decision)
6. Discovers new concept/relationship -> registers in Neo4j
7. Next cycle: richer Neo4j + Milvus with more memory
```

Each cycle:
- **Expands the [[Ontology as Code|ontology]]**: more concepts and relationships in the graph
- **Accumulates memory**: more tool calls, decisions, and sessions in Milvus
- **Increases [[Measurable Determinism|determinism]]**: more [[Programmatic Context|context]] available -> smaller [[Sample Space]] -> less [[Drift]]

## Evolution of the Feedback Loop

The [[Deterministic Feedback Loop]] in the POC operates on `docs/` -- search -> not found -> crawl -> save -> search again. It is the short loop.

The Self-Improvement Loop is the evolution:
- **POC**: docs on filesystem -> text search
- **Evolution**: ontology in [[Neo4j]] -> semantic search by concepts and relationships + memory in [[Milvus]] -> vector similarity search

The mechanism is the same (monotonic accumulation), but the representation is richer: graph + vectors instead of plain text.

## Parallel with HCC

The [[Ultra-Long-Horizon Agentic Science]] paper validates this design with the HCC:

| HCC | Self-Improvement Loop |
|---|---|
| L1 -- Evolving Experience | Tool calls logged in [[Milvus]] |
| L2 -- Refined Knowledge | Decisions logged in [[Milvus]] |
| L3 -- Prior Wisdom | Sessions logged in [[Milvus]] |
| Context Prefetching | `search_decisions` before acting |
| Context Promotion | Discovered concepts -> [[Neo4j]] via `expand` |

The difference: HCC uses summarization/compression. We use [[Embedding|embeddings]] + cosine similarity. But the three-tier structure is the same, and the HCC ablation study validates that all three layers are necessary.

## Why It Is "Self"

The agent improves itself without intervention:
- Discovers an unmapped concept -> adds to [[Neo4j]]
- An approach fails -> logged in [[Milvus]] -> avoided in the future
- An approach works -> logged -> reused

It is not model fine-tuning. It is enrichment of [[Programmatic Context|context]]. The model is the same -- what changes is the [[Ontology as Code|ontology]] and memory accessible via [[MCP]].

## In the Thesis

This loop is the complete materialization of [[Ontological Tautology]]: the [[Ontology]] becomes increasingly complete with use -> the [[Tautology]] establishes itself progressively -> [[Determinism]] grows monotonically.

It is [[Deterministic Trajectory Optimization]] in action: starts probabilistic (little ontology), iterates (each cycle adds context), converges to deterministic (complete ontology).

---

Related to: [[Neo4j]], [[Milvus]], [[mcp-ontology-server]], [[mcp-memory-server]], [[Deterministic Feedback Loop]], [[Cognitive Accumulation]], [[Measurable Determinism]], [[Ontology as Code]], [[Programmatic Context]], [[MCP]], [[Ontological Tautology]]
