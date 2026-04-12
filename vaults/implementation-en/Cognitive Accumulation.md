# Cognitive Accumulation

The process by which the [[Agent in POC|agent]] transforms experience into knowledge and knowledge into wisdom. Formalized by the HCC (Hierarchical Cognitive Caching) from the [[Ultra-Long-Horizon Agentic Science]] paper. Validated by the three-collection design of [[Milvus]].

---

## Definition

Cognitive Accumulation is not the same as a larger context. Concatenating everything produces saturation (200k+ tokens). Cognitive Accumulation is **progressive distillation**: raw experience -> validated judgments -> transferable wisdom.

## Three Layers in the Architecture

| HCC Layer | Role | Implementation |
|---|---|---|
| L1 -- Experience | Working memory, raw traces | Tool calls in [[Milvus]] (~6KB each) |
| L2 -- Knowledge | Distilled judgments and insights | Decisions in [[Milvus]] (~6KB each) |
| L3 -- Wisdom | Strategies transferable across tasks | Sessions in [[Milvus]] (~6KB each) |

The paper proves that all three layers are necessary:
- Without L1: medal rate drops from 72.7% to 22.7%
- Without L2: drops to 59.1%
- Without L3: drops to 54.5%

## In the Current POC

The [[Deterministic Feedback Loop]] already implements a simple version:
- `docs/` as L2/L3 (persisted knowledge and wisdom)
- Tool call outputs as L1 (session experience)

The evolution to [[Neo4j]] + [[Milvus]] adds:
- [[Embedding|Embeddings]] for semantic search
- Graph for relationships between concepts
- Three separate collections for three granularities

## Context Migration

Three [[Cognitive Accumulation]] operations mapped to the [[Self-Improvement Loop]]:

- **Prefetching**: Before acting, the agent calls `retrieve()` which searches similar wisdom in Milvus (decisions and sessions). It starts informed.
- **Context Hit**: During execution, it retrieves recent experience (`search_tool_calls`). It reuses what worked.
- **Context Promotion**: After completion, it distills experience into a decision (`log_decision`) and a decision into a session (`log_session`). It crystallizes learning.

---

Related to: [[Ultra-Long-Horizon Agentic Science]], [[Milvus]], [[Neo4j]], [[Deterministic Feedback Loop]], [[Self-Improvement Loop]], [[Embedding]], [[Measurable Determinism]], [[Programmatic Context]]
