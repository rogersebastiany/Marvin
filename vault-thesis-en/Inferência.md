# Inference

The process by which the model produces a response from an input. In LLMs, it is probabilistic -- it computes distributions and samples tokens.

---

## Definition

Inference is the phase of using an already-trained model ([[Matriz M]] frozen). The input passes through a [[Forward Pass]] and the model produces the output, token by token, based on the computed probabilities.

## Probabilistic Inference vs Deduction

Inference in LLMs is inherently probabilistic -- the model computes P(token|context) and chooses (or samples) the most probable one. This introduces variability ([[Drift]]).

[[Dedução]] is deterministic -- the conclusion is necessary given the premises. In the [[Tautologia Ontológica]] thesis, complete [[Contexto]] transforms probabilistic inference into something that approaches deduction: when P(correct token|context) -> 1, the probabilistic "choice" has only one viable candidate.

---

Related to: [[Dedução]], [[Forward Pass]], [[Matriz M]], [[Contexto]], [[Drift]], [[Determinismo]], [[Probabilidade Condicional]]
