# Space Reduction in Practice

Each tool call in the POC is a [[Redução de Dimensionalidade]] operation on the [[Espaço Amostral]]. The model goes from operating in the entire S to operating in an increasingly smaller and more precise [[Subconjunto]] A.

---

## Concrete Example

Without tools, the agent receives: "how does authentication work in our system?"
The model operates in the entire S -- the whole [[Matriz M]] is a candidate. High uncertainty, risk of [[Alucinação]].

With tools in the POC:

```
1. list_docs() -> ["api-reference.md", "architecture.md", "getting-started.md", ...]
   Reduction: the model knows which docs exist. S -> S1 subset of S

2. search_docs("authentication") -> matches in architecture.md lines 45-52
   Reduction: the model knows what the docs say about auth. S1 -> S2 subset of S1

3. get_doc_summary("architecture.md") -> section about JWT + middleware
   Reduction: the model has the architectural context. S2 -> S3 subset of S2

4. generate_diagram("auth flow with JWT") -> diagram with syntax refs
   Reduction: the model has the visual representation. S3 -> S4 subset of S3
```

Each step is a conditioning in [[Probabilidade Condicional]]:
P(response|prompt) -> P(response|prompt, docs) -> P(response|prompt, docs, search) -> P(response|prompt, docs, search, diagram)

## The 4 Servers as 4 Dimensions of Reduction

| Server | Dimension it reduces |
|---|---|
| [[docs-server]] | "What do we know?" -- eliminates the unknown |
| [[web-to-docs]] | "What can we know?" -- expands and then eliminates |
| [[prompt-engineer]] | "How to ask?" -- eliminates ambiguity |
| [[system-design]] | "What does it look like?" -- eliminates wrong visual interpretations |

Together, the 4 servers attack the 4 main sources of uncertainty in the [[Espaço Amostral]].

## Subset Intersection

In [[Teoria dos Conjuntos]], each tool defines a subset T subset of S. The intersection of multiple tools refines:

- A (prompt) intersection T1 (docs) intersection T2 (search) intersection T3 (diagram) = highly precise subset

When this intersection contains few viable candidates, the response is nearly [[Tautologia|tautological]] -- true by construction, not by probability.

---

Related to: [[Espaço Amostral]], [[Subconjunto]], [[Redução de Dimensionalidade]], [[Probabilidade Condicional]], [[Teoria dos Conjuntos]], [[Cadeia de Servers]], [[docs-server]], [[web-to-docs]], [[prompt-engineer]], [[system-design]], [[Contexto Programático]], [[Tautologia]]
