# prompt-engineer

The [[Programmatic Context|context]] optimizer. `prompt_engineer_server.py` generates, refines, and audits prompts using the [[Transformer-Driven Prompt Architect]] framework. It auto-discovers all tools from sibling servers and injects the complete [[Tool Catalog]] into every generated prompt.

---

## Implementation

```python
mcp = FastMCP("prompt-engineer",
    instructions="A Transformer-Driven Prompt Architect agent that generates structured, optimized prompts.")
```

Four [[MCP Primitives|tools]], two [[MCP Primitives|prompts]]:

| Type | Name | Function |
|---|---|---|
| Tool | `list_mcp_tools()` | Lists all tools from all servers |
| Tool | `generate_prompt(task, domain)` | Generates structured prompt with 6 sections + tool catalog |
| Tool | `refine_prompt(original, feedback)` | Improves existing prompt based on feedback |
| Tool | `audit_prompt(prompt)` | Evaluates prompt against the framework, scores 1-10, rewrites |
| Prompt | `architect_prompt(task)` | Template: generate production-grade prompt |
| Prompt | `improve_my_prompt()` | Template: audit -> refine workflow |

## Auto-Discovery of Tools

At import time, the server discovers tools from its siblings:

In unified [[Marvin]], the catalog is built directly from the `MARVIN_TOOLS` list in `marvin_server.py`:

```python
catalog = "\n".join(f"- `{t}`" for t in MARVIN_TOOLS)
```

Injected into `generate_prompt` and `refine_prompt`. It is the [[Ontology as Code|ontology]] of the system's capabilities -- no inter-module coupling.

## Role in the Thesis

The prompt-engineer is the server that optimizes the **delivery** of [[Programmatic Context|context]]. The other servers provide raw ontology (docs, diagrams). The prompt-engineer ensures this ontology is delivered in a structured way -- with role, few-shots, CoT, constraints.

In the thesis: poor [[Context]] -> [[Drift]]. Rich and **structured** [[Context]] -> [[Determinism]]. The prompt-engineer is the structurer.

The [[Transformer-Driven Prompt Architect]] with its 6 mandatory sections is a formalization of how to assemble [[Context]] that maximizes [[Measurable Determinism|determinism]] -- each section attacks a dimension of the [[Sample Space]].

## In the [[Server Chain]]

The prompt-engineer is the fourth server in the chain. It operates on knowledge already available (via [[docs-server]] and [[web-to-docs]]) to generate optimized prompts. The [[Tool Catalog]] it injects includes tools from the other 3 servers -- it is the meta-server that knows what the entire system can do.

---

Related to: [[Transformer-Driven Prompt Architect]], [[Tool Catalog]], [[Programmatic Context]], [[FastMCP]], [[MCP Primitives]], [[Ontology as Code]], [[Server Chain]], [[Measurable Determinism]], [[Anti-Hallucination]], [[docs-server]], [[web-to-docs]], [[system-design]]
