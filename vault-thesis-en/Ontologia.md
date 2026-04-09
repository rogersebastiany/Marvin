# Ontology

The study of what exists and how entities in a domain relate to each other. Defines the conceptual structure of a system -- the "map" of everything that is real within a scope.

---

## Philosophical Origin

Ontology comes from the Greek *ontos* (being) + *logos* (study). In philosophy, it is the branch of metaphysics that investigates the nature of being, existence, and reality. Aristotle called it "first philosophy" -- the study of the fundamental categories of everything that exists.

The central question of ontology is: "what exists?" And the answer organizes the world into categories, properties, and relations between entities.

## Ontology in Computer Science

In computer science, ontology is the formal and explicit specification of a shared conceptualization. This means: defining all entities of a domain, their properties, and the relations between them, in a way that a computational system can operate on these definitions.

Examples:
- Defining what a node is, what an edge is, and what a [[Grafo Dirigido Completo]] is -- that is graph ontology
- Defining what a microservice is, an SQS queue, an endpoint, and how they connect -- that is architecture ontology
- Defining all possible interactions of a payment system -- that is financial domain ontology

## Ontology as Complete Context

In the [[Ontological Tautology]] thesis, ontology is synonymous with complete [[Contexto]]. When all entities, relations, behaviors, and constraints of a domain are defined and accessible to the model via [[Tool|tools]] and [[MCP]], the model has the complete ontology of that domain.

The direct consequence: if the ontology is complete, [[Inferência]] transforms into [[Dedução]], and the result is [[Tautologia|tautological]].

## Ontology and the Sample Space

In [[Teoria dos Conjuntos]], ontology defines which [[Subconjunto]] of the [[Espaço Amostral]] is relevant. Without ontology, the model operates in the entire space S -- high uncertainty, high risk of [[Alucinação]]. With complete ontology, it operates in a [[Subconjunto]] A ⊂ S so precise that the correct answer is deducible.

Each layer of ontology added (specs, tests, ADRs, docs, logs) is an additional constraint on S -- reducing dimensions, eliminating invalid candidates, bringing A closer to a single point.

## Ontology by Domain

The universal ontology does not exist -- nobody has mapped everything that exists across all domains. But ontology by domain is constructible. A post-doc in biology possesses the ontology of the field of biology. If that ontology is translated into [[Tool|tools]] and served via [[MCP]], an [[Agente]] operating in that domain achieves near-total [[Determinismo]].

This is replicable for any domain: law, medicine, engineering, finance. Change the ontology, change the tools, the framework is the same.

## When the Ontology Is Complete

A domain's ontology is complete when **every method/process of the domain has a corresponding [[Tool Tautológica]]**. There is no method in the company or area that the agent would need to execute but has no tool for.

This is verifiable:
1. Enumerate all methods/processes of the domain
2. For each one, verify: does a corresponding tool exist?
3. For each tool, verify: is it [[Tool Tautológica|tautological]]? (complete I/O contract, finite output, explicit failure)

If yes for all -> complete ontology -> [[Tautologia]] by construction -> [[Determinismo]] with accuracy.

Completeness is not abstract -- it is a concrete checklist.

---

Related to: [[Tautologia]], [[Contexto]], [[Espaço Amostral]], [[Teoria dos Conjuntos]], [[Tool]], [[Tool Tautológica]], [[MCP]], [[Determinismo]], [[Alucinação]], [[Ontological Tautology]]
