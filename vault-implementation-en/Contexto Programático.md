# Programmatic Context

[[Contexto]] delivered via code -- [[Primitivas MCP|tools]], [[Primitivas MCP|resources]], and [[Primitivas MCP|prompts]] MCP -- instead of manual copy-paste. The model accesses external knowledge programmatically in O(1) via [[MCP]].

---

## The Difference

**Without programmatic context:** the human reads the documentation, copies relevant excerpts, pastes them into the prompt. Slow, incomplete, error-prone. The [[Contexto]] depends on the human's ability to select information.

**With programmatic context:** the [[Agente na POC|agent]] invokes `search_docs("authentication")` and receives the relevant excerpts directly. Fast, systematic, complete within the scope of the search. The context is delivered by the machine.

## Forms of Programmatic Context in the POC

**Tools (invocable functions):**
- `search_docs(query)` -> keyword search across all docs, returns matches with context
- `crawl_docs(url, max_pages)` -> crawls online documentation and saves locally
- `generate_diagram(description)` -> generates diagram with syntax references as context
- `audit_prompt(prompt)` -> evaluates prompt against a structured framework

**Resources (accessible data):**
- `docs://{filename}` -> complete content of a doc
- `diagrams://{filename}` -> mermaid code of a diagram

**Prompts (structured templates):**
- `explain_concept(topic)` -> template for explaining a concept using docs
- `design_system(description)` -> template for end-to-end design
- `research_and_answer(question)` -> template for local + web search + answer

Each form is a different way of injecting [[Ontologia como Código|ontology]] into the model's [[Contexto]]. All of them reduce the effective [[Espaço Amostral]].

## O(1) via MCP

[[MCP]] makes context access O(1) -- for the model, calling `search_docs` has the same cognitive cost as accessing local memory. It does not matter whether the knowledge is in a local markdown file or (in production) in an [[S3 como Ontologia Persistente|encrypted S3 bucket in Ireland]]. The interface is the same, the cost is constant.

This is what makes complete [[Ontologia]] viable in real time. Without [[FastMCP]] and [[stdio]], each access to external context would have variable latency, different authentication, incompatible formats.

## Programmatic Context as [[Redução de Espaço na Prática|Space Reduction]]

Each tool call is an additional conditioning in [[Probabilidade Condicional]]:

```
P(token|prompt) -- first constraint
P(token|prompt, search_docs) -- second constraint
P(token|prompt, search_docs, get_diagram) -- third constraint
```

It is concrete [[Redução de Dimensionalidade]] -- each call eliminates irrelevant dimensions from the space of possibilities.

---

Related to: [[Contexto]], [[Primitivas MCP]], [[MCP]], [[FastMCP]], [[Ontologia como Código]], [[Redução de Espaço na Prática]], [[Agente na POC]], [[docs-server]], [[web-to-docs]], [[prompt-engineer]], [[system-design]]
