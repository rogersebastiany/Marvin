# Set Theory

Mathematical framework that underpins the entire relationship between [[Sample Space]], [[Context]], and [[Subset|subsets]]. It is the formal language for describing how context restricts the space of possibilities.

---

## Definition

Set Theory is the branch of mathematics that studies collections of objects (sets), their properties, and operations between them. Formalized by Georg Cantor in the late 19th century, it is considered the foundation of modern mathematics.

Fundamental concepts: membership (∈), subset (⊂), union (∪), intersection (∩), complement (\), empty set (∅), universe set (U).

## Application in the Thesis

In [[Ontological Tautology]], Set Theory formalizes the mechanics of [[Context]]:

- **S** (universe set) = complete [[Sample Space]] of the [[Matrix M]]
- **A ⊂ S** (subset) = region defined by [[Context]] (prompt)
- **T ⊂ S** (subset) = region defined by each [[Tool]]
- **A ∩ T** (intersection) = refinement -- combining context + tools narrows the space
- **S \ A** (complement) = [[Hallucination]] zone -- everything outside the context
- **|A| -> 1** = when the subset contains only one viable element = [[Tautology]]

## Operations and Their Effects

**Union (A ∪ B)**: expanding the context -- adding more information, more [[Tool|tools]]. Increases domain coverage.

**Intersection (A ∩ B)**: refining the context -- combining multiple sources that agree. Reduces ambiguity.

**Complement (S \ A)**: everything that was not mapped. If the model operates here, it produces [[Hallucination]]. Complete [[Ontology]] minimizes the complement.

## Conditional Probability

In [[Conditional Probability]], P(A|B) = P(A ∩ B) / P(B). Context B restricts the effective space, and the probability of the correct token increases within this restriction.

It is the formalization of why a rich prompt works: you are conditioning the probability to a smaller subset of the sample space.

---

Related to: [[Sample Space]], [[Context]], [[Subset]], [[Conditional Probability]], [[Hallucination]], [[Ontology]], [[Tool]], [[Tautology]], [[Matrix M]]
