# LLM Output Drift

Paper that defines and analyzes the phenomenon of [[Drift]] in LLMs -- the variation of responses even at temperature zero and constant input. Classifies models into three tiers of behavior and reveals that larger models drift more.

---

## Reference

**LLM Output Drift: Cross-Provider Validation & Mitigation for Financial Workflows**
Raffi Khatchadourian, Rolando Franco -- AI4F Workshop, ACM ICAIF '25 (Singapore, Nov. 2025)
https://arxiv.org/abs/2511.07585

## Contribution

Explains why, without rigid [[Context]], the AI varies responses even at temperature zero. Formally defines drift and proposes mitigation strategies: cross-provider validation and structured context.

## Three Tiers of Drift

The paper classifies models into three levels of behavior at T=0.0:

- **Tier 1** (small, 7-8B parameters): 100% consistency. Perfectly deterministic, but limited accuracy.
- **Tier 2** (medium, 20-70B): High consistency, good balance between determinism and capability.
- **Tier 3** (large, 100B+, e.g. GPT-OSS-120B): Only 12.5% consistency. More parameters = more [[Drift]].

Counter-intuitive finding: larger models drift **more**, not less. The larger [[Matrix M]] has more [[Vector|vectors]], the [[Sample Space]] is larger, there are more close candidates competing.

## Sensitivity by Task Type

Not all tasks drift equally:

- **[[RAG]]**: Most sensitive to temperature. Small variations in retrieved context cascade into different responses.
- **Summarization**: Moderate sensitivity.
- **Classification**: Most robust. The output space is discrete and small.

This matters: the search in `docs/` in the POC is a RAG task -- exactly the category with the highest drift risk. Structured [[Context]] via [[Tool|tools]] is the necessary mitigation.

## Cross-Provider Validation

The same prompt on different providers produces different results. However, the **determinism pattern transfers**: if a task is deterministic on one provider, it tends to be deterministic on another. The structure of [[Context]] matters more than the model.

This validates that the [[Agent]] can be tool-agnostic -- what matters is the quality of the [[Ontology]], not the provider.

## Mitigation Framework

The paper maps drift to regulatory frameworks (SOC, MiFID II) and proposes mitigation in three layers:
1. Cross-provider validation (test the same prompt across multiple models)
2. Rigid structured [[Context]] (reduce ambiguity)
3. Determinism harness ([[DFAH]])

In the thesis: [[Tool|tools]] via [[MCP]], specs, BDD, TDD, ADR, observability. Each layer added is a layer of [[Sample Space]] reduction.

## In the Thesis

This paper grounds the inverse relationship between [[Context]] and [[Drift]]: poor context -> high drift. Rich context ([[Ontology]]) -> low drift -> [[Determinism]].

It complements the [[DFAH]]: while the DFAH shows what happens with context (89%+), this paper shows what happens without -- and why.

---

Related to: [[Drift]], [[Determinism]], [[DFAH]], [[Context]], [[Ontology]], [[Ontological Tautology]], [[Matrix M]], [[Sample Space]], [[RAG]], [[MCP]], [[Agent]]
