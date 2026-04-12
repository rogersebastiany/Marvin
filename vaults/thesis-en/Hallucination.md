# Hallucination

Occurs when the model produces responses outside the domain defined by [[Context]]. The model operates in the complement S \ A of the [[Sample Space]] -- the zone not mapped by the [[Ontology]].

---

## Definition

In LLMs, hallucination is the generation of content that appears plausible but is factually incorrect, fabricated, or inconsistent with the domain.

"If you demand something that was not previously mapped, it will hallucinate, and this happens 100% of the time."

## Cause

Hallucination is not a bug -- it is the logical consequence of operating without sufficient [[Context]]. In [[Set Theory]], the model is operating in S \ A (complement) -- the region of the [[Sample Space]] not covered by context.

Without [[Tool|tools]], without specs, without [[Ontology]] -- the model infers from the entire space, and the probability of getting it right is low.

## Prevention

Prevention is the thesis itself: building a complete [[Ontology]] via rich [[Context]]. Each layer added (spec, BDD, TDD, ADR, observability, [[RAG]]) reduces the complement zone and consequently reduces the probability of hallucination.

"YOU DO NOT THINK. I AM THE ONE WHO THINKS. JUST EXECUTE WHAT IS MAPPED VIA TOOL. OTHERWISE YOU DO NOT EXECUTE, AND YOU REPORT THAT YOU ARE INCAPABLE." -- This instruction turns hallucination from a bug into a feature: the model refuses instead of inventing.

---

Related to: [[Context]], [[Ontology]], [[Sample Space]], [[Set Theory]], [[Tool]], [[Drift]], [[RAG]]
