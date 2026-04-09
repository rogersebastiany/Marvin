# Tautology

A proposition that is true for all possible valuations within a domain. It does not depend on external conditions -- it is true by construction.

---

## Formal Definition

In propositional logic, a tautology is a formula that evaluates to true for every possible assignment of truth values to its variables. Classic example: `P v ~P` (a thing is true or it is not). Regardless of the value of P -- the proposition is always true.

In [[Teoria dos Conjuntos]], if for every element x of a [[Conjunto]] C the property P(x) holds, then P is tautological in C. The universality of the property within the domain is what makes it tautological.

## Tautology in AI Systems

In the context of LLMs, tautology emerges when [[Contexto]] is so complete that all reasoning paths lead to the same answer. The answer is not "probable" -- it is necessary.

This happens because the [[Espaço Amostral]] has been reduced to a [[Subconjunto]] so precise that the number of viable candidates for the next token tends to 1. The model is not "choosing" -- it is deducing.

The difference between probabilistic inference and [[Dedução|tautological deduction]] is the difference between "I think the answer is X" and "the answer can only be X given the context."

## Relationship with Ontology

[[Ontologia]] defines the domain. Tautology is what emerges when the domain is completely defined. They are complementary concepts -- the ontology is the cause, the tautology is the effect.

When the [[Ontologia]] is incomplete, the system operates by probability. When it is complete, it operates by deduction. The transition point is what the [[Tautologia Ontológica]] thesis formalizes.

## Relationship with Determinism

[[Determinismo]] is the practical manifestation of tautology in computational systems. If the answer is tautologically true given the context, it is deterministic -- reproducible, predictable, auditable.

The paper [[DFAH]] demonstrates empirically that structured context (partial ontology) already produces 89-90% determinism. Complete ontology -> tautology -> total determinism.

## Tautology in Tools

A [[Tool Tautológica]] is a tool whose I/O specification is itself tautological -- for every valid input, there exists exactly one correct output. `search_docs("x")` finds or does not find. There is no third option. The tool's contract is true by construction.

When all tools in a domain are tautological and cover all methods of the domain, the entire system is tautological. The agent's response is not "probable" -- it is deduced from tools that can only return truth.

---

Related to: [[Ontologia]], [[Determinismo]], [[Dedução]], [[Espaço Amostral]], [[Contexto]], [[DFAH]], [[Tautologia Ontológica]], [[Tool Tautológica]], [[Tool]]
