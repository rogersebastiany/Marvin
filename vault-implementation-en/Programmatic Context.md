# Programmatic Context

[[Context]] delivered via code -- [[MCP Primitives|tools]], [[MCP Primitives|resources]], and [[MCP Primitives|prompts]] MCP -- instead of manual copy-paste. The model accesses external knowledge programmatically in O(1) via [[MCP]].

---

## The Difference

**Without programmatic context:** the human reads the documentation, copies relevant excerpts, pastes them into the prompt. Slow, incomplete, error-prone. The [[Context]] depends on the human's ability to select information.

**With programmatic context:** the [[Agent in POC|agent]] invokes `search_docs("authentication")` and receives the relevant excerpts directly. Fast, systematic, complete within the scope of the search. The context is delivered by the machine.

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

Each form is a different way of injecting [[Ontology as Code|ontology]] into the model's [[Context]]. All of them reduce the effective [[Sample Space]].

## O(1) via MCP

[[MCP]] makes context access O(1) -- for the model, calling `search_docs` has the same cognitive cost as accessing local memory. It does not matter whether the knowledge is in a local markdown file or (in production) in an [[S3 as Persistent Ontology|encrypted S3 bucket in Ireland]]. The interface is the same, the cost is constant.

This is what makes complete [[Ontology]] viable in real time. Without [[FastMCP]] and [[stdio]], each access to external context would have variable latency, different authentication, incompatible formats.

## Programmatic Context as [[Space Reduction in Practice|Space Reduction]]

Each tool call is an additional conditioning in [[Conditional Probability]]:

```
P(token|prompt) -- first constraint
P(token|prompt, search_docs) -- second constraint
P(token|prompt, search_docs, get_diagram) -- third constraint
```

It is concrete [[Dimensionality Reduction]] -- each call eliminates irrelevant dimensions from the space of possibilities.

---

Related to: [[Context]], [[MCP Primitives]], [[MCP]], [[FastMCP]], [[Ontology as Code]], [[Space Reduction in Practice]], [[Agent in POC]], [[docs-server]], [[web-to-docs]], [[prompt-engineer]], [[system-design]]
