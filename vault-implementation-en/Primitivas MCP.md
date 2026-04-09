# MCP Primitives

The three types of [[Contexto Programático|programmatic context]] that an [[MCP]] server can expose: **Tools** (invocable functions), **Resources** (accessible data), and **Prompts** (structured templates). Each type is a different mechanism for delivering [[Ontologia como Código|ontology]] to the model.

---

## Tools

Functions that the [[Agente na POC|agent]] can invoke. The agent decides when and how to call. Each tool receives parameters, executes logic, and returns the result as new [[Contexto]].

In the POC: `search_docs(query)`, `crawl_docs(url)`, `generate_diagram(description)`, `audit_prompt(prompt)`, etc.

In the thesis: each tool is a [[Subconjunto]] of [[Vetor|vectors]] that functions as [[Tool como Bias|bias]]. The tool description is tokenized and embedded -- the model "knows" the tool exists and what it does before even calling it.

Registered via `@mcp.tool()` in [[FastMCP]].

## Resources

Data that the agent can read directly. O(1) access to content without search logic -- the agent specifies the URI and receives the complete content.

In the POC:
- `docs://{filename}` -> complete content of a markdown in `docs/`
- `diagrams://{filename}` -> mermaid code of a diagram in `diagrams/`

In the thesis: resources are direct access to the relevant [[Subconjunto]] of the [[Ontologia como Código|ontology]]. While tools search and filter, resources deliver raw content.

Registered via `@mcp.resource("uri://{param}")` in [[FastMCP]].

## Prompts

Templates that guide the agent in complex workflows. The agent does not need to invent the tool sequence -- the prompt defines the step-by-step.

In the POC:
- `research_and_answer(question)` -> local search -> web -> save -> respond
- `design_system(description)` -> generate diagram -> explain -> trade-offs -> save
- `improve_my_prompt()` -> audit -> refine

In the thesis: MCP prompts are [[Contexto]] that reduces the "how to do it?" dimension of the [[Espaço Amostral]]. The agent does not need to reason about the strategy -- it is defined in the template.

Registered via `@mcp.prompt()` in [[FastMCP]].

## Interaction Between Primitives

The three types complement each other:

1. **Prompt** defines the strategy: "search local, then web, then respond"
2. **Tool** executes the action: `search_docs()`, `crawl_docs()`
3. **Resource** provides additional data: `docs://architecture.md`

Together, they cover the three dimensions of [[Contexto Programático]]: what to do (prompts), how to do it (tools), and with what to do it (resources).

---

Related to: [[MCP]], [[FastMCP]], [[Contexto Programático]], [[Tool como Bias]], [[Ontologia como Código]], [[Agente na POC]], [[Catálogo de Tools]], [[docs-server]], [[web-to-docs]], [[prompt-engineer]], [[system-design]]
