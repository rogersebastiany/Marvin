# MCP Primitives

The three types of [[Programmatic Context|programmatic context]] that an [[MCP]] server can expose: **Tools** (invocable functions), **Resources** (accessible data), and **Prompts** (structured templates). Each type is a different mechanism for delivering [[Ontology as Code|ontology]] to the model.

---

## Tools

Functions that the [[Agent in POC|agent]] can invoke. The agent decides when and how to call. Each tool receives parameters, executes logic, and returns the result as new [[Context]].

In the POC: `search_docs(query)`, `crawl_docs(url)`, `generate_diagram(description)`, `audit_prompt(prompt)`, etc.

In the thesis: each tool is a [[Subset]] of [[Vector|vectors]] that functions as [[Tool as Bias|bias]]. The tool description is tokenized and embedded -- the model "knows" the tool exists and what it does before even calling it.

Registered via `@mcp.tool()` in [[FastMCP]].

## Resources

Data that the agent can read directly. O(1) access to content without search logic -- the agent specifies the URI and receives the complete content.

In the POC:
- `docs://{filename}` -> complete content of a markdown in `docs/`
- `diagrams://{filename}` -> mermaid code of a diagram in `diagrams/`

In the thesis: resources are direct access to the relevant [[Subset]] of the [[Ontology as Code|ontology]]. While tools search and filter, resources deliver raw content.

Registered via `@mcp.resource("uri://{param}")` in [[FastMCP]].

## Prompts

Templates that guide the agent in complex workflows. The agent does not need to invent the tool sequence -- the prompt defines the step-by-step.

In the POC:
- `research_and_answer(question)` -> local search -> web -> save -> respond
- `design_system(description)` -> generate diagram -> explain -> trade-offs -> save
- `improve_my_prompt()` -> audit -> refine

In the thesis: MCP prompts are [[Context]] that reduces the "how to do it?" dimension of the [[Sample Space]]. The agent does not need to reason about the strategy -- it is defined in the template.

Registered via `@mcp.prompt()` in [[FastMCP]].

## Interaction Between Primitives

The three types complement each other:

1. **Prompt** defines the strategy: "search local, then web, then respond"
2. **Tool** executes the action: `search_docs()`, `crawl_docs()`
3. **Resource** provides additional data: `docs://architecture.md`

Together, they cover the three dimensions of [[Programmatic Context]]: what to do (prompts), how to do it (tools), and with what to do it (resources).

---

Related to: [[MCP]], [[FastMCP]], [[Programmatic Context]], [[Tool as Bias]], [[Ontology as Code]], [[Agent in POC]], [[Tool Catalog]], [[docs-server]], [[web-to-docs]], [[prompt-engineer]], [[system-design]]
