# Context

The input that reduces the [[Espaço Amostral]]. Composed of prompt, [[Tool|tools]], history, and any information that conditions the model's response. It is the central mechanism of the [[Tautologia Ontológica]].

---

## Definition

Context is all information available to the model at the time of inference. It includes: the user's prompt, system instructions, available [[Tool|tools]] and their results, conversation history, and any data injected via [[MCP]].

In [[Teoria dos Conjuntos]]: context is the operator that defines the [[Subconjunto]] A ⊂ S of the [[Espaço Amostral]].

## Context as a Subset of Vectors

Context is, ultimately, a set of [[Vetor|vectors]]. The prompt is tokenized ([[Tokenização]]), each token is embedded ([[Embedding]]) into a vector, and these vectors define the region of the space where the model operates.

More context = more vectors = more precise subset = smaller approximation error in probability computation.

## Context and Determinism

The more enriched the context, the smaller the approximation error in computing the next token. Poor context -> [[Drift]]. Rich context -> [[Determinismo]].

The paper [[DFAH]] demonstrates this relationship quantitatively: structured context (harness) produces 89-90%+ determinism.

## Forms of Context

All forms of context are functionally equivalent -- they are [[Subconjunto|subsets]] of [[Vetor|vectors]] that restrict S:

- **Prompt**: explicit context from the user
- **[[Tool|Tools]]**: programmatic context (docs, APIs, specs)
- **[[MCP]]**: external context at O(1) (logs, DBs, metrics)
- **[[RAG]]**: vectorized historical context (past decisions)
- **System prompt**: personality/role context of the [[Agente]]

Cumulatively, all these forms build the [[Ontologia]].

---

Related to: [[Espaço Amostral]], [[Subconjunto]], [[Vetor]], [[Ontologia]], [[Determinismo]], [[Drift]], [[Tool]], [[MCP]], [[RAG]], [[Agente]], [[Probabilidade Condicional]], [[DFAH]], [[Tautologia Ontológica]]
