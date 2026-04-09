# Cognitive Accumulation

The process by which an [[Agente]] transforms transient experience into validated knowledge and, eventually, into reusable wisdom. It is not linear aggregation of [[Contexto]] -- it is progressive distillation.

---

## Definition

Cognitive Accumulation is the mechanism that enables increasing [[Determinismo]] over time. Each agent interaction produces raw experience. That experience is refined into knowledge. Knowledge, validated across tasks, crystallizes into wisdom.

Experience -> Knowledge -> Wisdom.

## The HCC Framework

The paper [[Ultra-Long-Horizon Agentic Science]] formalizes this in Hierarchical Cognitive Caching (HCC):

- **L1 (Experience)**: Execution traces, patches, logs. Working memory.
- **L2 (Knowledge)**: Judgments, insights, strategic summaries. Medium-term memory.
- **L3 (Wisdom)**: Transferable strategies, reusable pipelines, stable priors. Long-term memory, retrievable via [[Embedding]] and cosine similarity.

Context migration moves information between layers: prefetching (L3->context), context hit (L1 or L2->context), context promotion (L1->L2 via P1, L2->L3 via P2).

## In the Thesis

The [[Tautologia Ontológica]] equation -- Spec + BDD + TDD + ADR + Observability + [[MCP]] + [[RAG]] -- is a cognitive accumulation framework. Each layer adds structured [[Contexto]] that persists and accumulates:

- Specs and BDD/TDD = validated knowledge (L2)
- ADR = wisdom from architectural decisions (L3)
- Observability = continuous experience (L1)
- [[MCP]] + [[RAG]] = O(1) access mechanism to all layers

The [[Feedback Loop Determinístico]] is the promotion mechanism: experience from one session -> saved docs -> knowledge available in the next session -> wisdom accumulated in the corpus.

## Crucial Distinction

Cognitive Accumulation is not larger context. The paper shows that linear context grows to 200k+ tokens and saturates. HCC maintains ~70k effective tokens. The difference: distillation and promotion, not concatenation.

In the [[Redução de Dimensionalidade|same logic]]: more information is not more context. Distilled and structured information is more context.

---

Related to: [[Ultra-Long-Horizon Agentic Science]], [[Determinismo]], [[Contexto]], [[Agente]], [[RAG]], [[MCP]], [[Embedding]], [[Tautologia Ontológica]], [[Feedback Loop Determinístico]]
