# Ultra-Long-Horizon Agentic Science

Paper presenting ML-Master 2.0, an autonomous agent that maintains strategic coherence over long cycles (24h+) through hierarchical [[Cognitive Accumulation]]. Introduces the HCC (Hierarchical Cognitive Caching) framework.

---

## Reference

**Toward Ultra-Long-Horizon Agentic Science: Cognitive Accumulation for Machine Learning Engineering**
Xinyu Zhu, Yuzhu Cai, Zexi Liu et al. -- Shanghai Jiao Tong University, DP Technology, Shanghai AI Laboratory
https://arxiv.org/abs/2601.10402

## Contribution

The paper redefines long-horizon autonomy not as context expansion, but as an evolutionary process of [[Cognitive Accumulation]]: transient experience -> validated knowledge -> reusable wisdom. Introduces HCC as a concrete mechanism.

## Hierarchical Cognitive Caching (HCC)

Three-layer memory hierarchy, inspired by computer cache:

**L1 -- Evolving Experience (working memory)**
Raw execution traces: code patches, terminal output, current research plan. High fidelity, short duration. The [[Agent]]'s scratchpad.

**L2 -- Refined Knowledge (medium-term strategic memory)**
Key judgments ("feature X is harmful"), experimental insights ("CV leakage under split Y"), progress summaries. Distilled from L1 after each phase. Enables long-term planning without carrying verbose logs.

**L3 -- Prior Wisdom (long-term memory)**
Transferable strategies, reusable pipelines, stable hyperparameter priors. Persists across tasks. Stored as ([[Embedding]], text) pairs and retrieved via cosine similarity.

## Context Migration

Three operations move information between layers:

- **Prefetching**: Before starting a task, embeds the task descriptor and retrieves similar wisdom from L3 via a cosine threshold delta. The agent starts already informed.
- **Context Hit**: Cache-like policy -- searches L1 if available, otherwise falls back to L2 summaries.
- **Context Promotion**: P1 compresses L1->L2 (phase-based summarization), P2 distills L2->L3 (task-based wisdom extraction). Experience crystallizes into knowledge, which crystallizes into wisdom.

## Results

- **56.44% medal rate** on MLE-Bench (75 real Kaggle tasks) -- SOTA, surpassing all proprietary and open-source.
- **92.7% improvement** over ML-Master 1.0.
- HCC limits peak context from **200k+ tokens to ~70k**, retaining strategic coherence.
- Surpasses 50% of human participants on 63.1% of tasks.

## Ablation -- Each Layer Matters

| Configuration | Valid Submission | Medal Rate |
|---|---|---|
| Without L1 (Experience) | 54.5% | 22.7% |
| Without L2 (Knowledge) | 95.5% | 59.1% |
| Without L3 (Wisdom) | 95.5% | 54.5% |
| **Complete (L1+L2+L3)** | **95.5%** | **72.7%** |

L1 is the most critical -- without raw experience, the agent cannot iterate on its errors. L3 has the most impact on quality -- without prior wisdom, the agent explores inefficiently.

## The "+" of 89%+

This paper supports the "plus" of the 89%+ demonstrated by the [[DFAH]]. [[Determinism]] is not static -- it grows over time when [[Context]] is cumulative and structured in layers.

Mechanism: each [[ReAct]] cycle of the [[Agent]] produces new knowledge -> distilled into L2 -> crystallized into L3 -> available in the next cycle -> richer context -> greater determinism.

The central insight: **[[Cognitive Accumulation]] is not linear aggregation of context**. It is experience -> knowledge -> wisdom. Each level has different temporal dynamics and levels of abstraction.

---

Related to: [[Determinism]], [[RAG]], [[Agent]], [[ReAct]], [[DFAH]], [[Context]], [[Ontological Tautology]], [[Cognitive Accumulation]], [[Embedding]]
