# Determinism

The state in which, given an input and a [[Context]], the output is predictable and reproducible. There is no variation, no surprise -- the result is a necessary consequence of the initial conditions.

---

## Definition

In philosophy and physics, determinism is the doctrine that every event is causally determined by an unbroken chain of prior events. Given the complete state of a system at one instant, all future states are predictable.

In computational systems, determinism means that the same input produces the same output, always. A pure function is deterministic. A hash is deterministic. An LLM with temperature zero and complete [[Context]] approaches deterministic behavior.

## The Problem with LLMs

LLMs are probabilistic by nature -- they compute probability distributions over tokens and sample the next one. Even at temperature zero (always choosing the most probable token), internal variations (floating-point precision, batching, model version) can cause [[Drift]] -- different responses for the same input.

The paper [[LLM Output Drift]] formalizes this phenomenon: without rigid [[Context]], the AI varies responses even at temperature zero, especially cross-provider.

## How to Achieve Determinism

The [[Ontological Tautology]] thesis proposes that determinism in LLMs is not a model problem -- it is a [[Context]] problem. The model is probabilistic, but if the effective [[Sample Space]] is reduced to a point (via complete [[Ontology]]), the probability of the correct token approaches 1.

The paper [[DFAH]] demonstrates empirically: structured context (specs, harness, typed tools) produces 89-90%+ trajectory determinism. Specifically, it is **schema-first architecture** -- tool definitions with explicit types and formatted returns -- that produces this number. Three formal metrics capture different granularities: ActDet (actions), SigDet (signatures), DecDet (decisions).

The paper [[Ultra-Long-Horizon Agentic Science]] shows that this number grows with [[Cognitive Accumulation]] -- not linear aggregation, but progressive distillation of experience into knowledge into wisdom (L1->L2->L3).

The path: [[Ontology]] -> [[Tautology]] -> Determinism.

## Determinism is not Accuracy (in the general case)

The [[DFAH]] reveals a null correlation (r = -0.11) between determinism and accuracy **in agents with generic tools**. Small models (7-20B) achieve 100% determinism at T=0.0 but make many errors. Large models are less deterministic but more capable.

In the general case: determinism without complete [[Ontology]] is merely consistency in error.

## Determinism = Accuracy (with Tautological Tools)

When tools are [[Tautological Tool|tautological]] -- complete I/O contract, finite output, explicit failure -- determinism **implies** accuracy. The tool can only return the correct answer or "I don't know." If the system is deterministic with tautological tools, it is deterministically correct.

The r = -0.11 from DFAH measures the general case. The [[Ontological Tautology]] thesis operates in the specific case: complete [[Ontology]] (total coverage) with tautological tools (complete contracts). In this case, the correlation between determinism and accuracy is positive by construction.

## Determinism vs Convergence

[[Convergence]] is the process of approaching determinism. The [[Loss Function]] converges during training -- the error decreases to a minimum. Analogously, [[Context]] converges the [[Sample Space]] -- it reduces candidates until (ideally) one remains.

Determinism is the final state. [[Convergence]] is the path to it.

## Determinism and Auditability

Determinism implies auditability: if the result is reproducible, it can be verified, tested, and validated. In regulated domains (finance, healthcare, law), determinism is not desirable -- it is mandatory.

11% indeterminism (the complement of the 89%) is manageable. 100% indeterminism (no context) is unacceptable.

The correct metric for regulated domains is **pass^k** (all k attempts must succeed), not pass@k (at least one). A system with pass@5 = 95% and pass^5 = 40% appears reliable but is not.

---

Related to: [[Tautology]], [[Ontology]], [[Drift]], [[Convergence]], [[Context]], [[Sample Space]], [[DFAH]], [[LLM Output Drift]], [[Ultra-Long-Horizon Agentic Science]], [[Cognitive Accumulation]], [[Ontological Tautology]], [[Tautological Tool]]
