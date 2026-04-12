# Dimensionality Reduction

The practical effect of [[Conditional Probability]]: [[Context]] reduces the effective dimensions of the problem. The model operates in a smaller and more precise subspace.

---

## Definition

In mathematics and machine learning, dimensionality reduction is the process of reducing the number of random variables under consideration, obtaining a smaller set of principal variables.

In the context of the thesis: the [[Sample Space]] S operates in R^n with n in the thousands. Each [[Tool]], spec, or additional [[Context]] effectively eliminates irrelevant dimensions, projecting the problem to a lower-dimensional subspace.

## Mechanism

Each piece of context is a dimensional constraint:
- "The project uses Java 21" -- eliminates all dimensions related to other languages
- "The database is PostgreSQL" -- eliminates dimensions of MySQL, MongoDB, etc.
- "The API follows REST" -- eliminates dimensions of GraphQL, gRPC, etc.

Cumulatively, these constraints reduce the space of possibilities from billions to thousands, then hundreds, then tens. When few viable candidates remain, [[Determinism]] is natural.

## Relationship with the Method

Each component of the method contributes dimensional reduction:
- **Spec Driven Design**: constrains the expected behavior
- **BDD**: constrains the valid scenarios
- **TDD**: constrains the correct implementation
- **ADR**: constrains the architectural decisions
- **Observability**: constrains the actual state of the system
- **[[RAG]]**: constrains with the history of past decisions

The cumulative effect is the complete [[Ontology]] -- all irrelevant dimensions eliminated.

---

Related to: [[Conditional Probability]], [[Context]], [[Sample Space]], [[Determinism]], [[Ontology]], [[Tool]], [[RAG]]
