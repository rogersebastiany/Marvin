# Conditional Probability

P(token|context) instead of P(token). The probability of an event given that another event has already occurred. It is the mathematical formalization of why rich [[Contexto]] works.

---

## Definition

P(A|B) = P(A ∩ B) / P(B)

The probability of A given B is the probability of the intersection of A and B divided by the probability of B. Event B "restricts" the [[Espaço Amostral]] -- we only consider outcomes where B is true.

## Application in LLMs

Without [[Contexto]]: the model computes P(token) in the entire [[Espaço Amostral]] S. Many candidates, high uncertainty, risk of [[Drift]].

With context: the model computes P(token|context) in the [[Subconjunto]] A ⊂ S. Few candidates, high certainty, tendency toward [[Determinismo]].

The context B works as the "given event" -- it eliminates entire regions of S from consideration. The model does not need to evaluate irrelevant tokens -- the conditioning has already excluded them.

## Progressive Reduction

Each layer of [[Contexto]] is an additional conditioning:

P(token|prompt) -- first restriction
P(token|prompt, tool) -- second restriction
P(token|prompt, tool, spec) -- third restriction
P(token|prompt, tool, spec, ADR, logs...) -- complete [[Ontologia]]

Each conditioning reduces the effective space. This is the formal mechanism of [[Redução de Dimensionalidade]].

When the conditioning is total (complete ontology), P(correct token|context) -> 1. This is [[Tautologia]].

---

Related to: [[Espaço Amostral]], [[Contexto]], [[Redução de Dimensionalidade]], [[Determinismo]], [[Tautologia]], [[Drift]], [[Teoria dos Conjuntos]], [[Subconjunto]]
