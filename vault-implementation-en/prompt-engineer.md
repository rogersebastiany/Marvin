# prompt-engineer

The [[Contexto Programático|context]] optimizer. `prompt_engineer_server.py` generates, refines, and audits prompts using the [[Transformer-Driven Prompt Architect]] framework. It auto-discovers all tools from sibling servers and injects the complete [[Catálogo de Tools]] into every generated prompt.

---

## Implementation

```python
mcp = FastMCP("prompt-engineer",
    instructions="A Transformer-Driven Prompt Architect agent that generates structured, optimized prompts.")
```

Four [[Primitivas MCP|tools]], two [[Primitivas MCP|prompts]]:

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

```python
def _discover_mcp_tools() -> str:
    from server import mcp as docs_mcp
    from web_to_docs_server import mcp as web_mcp
    from system_design_server import mcp as design_mcp
    # ... asyncio.run() to list tools from each server
```

This creates a coupling: the 3 sibling servers must be importable when prompt-engineer starts. The `asyncio.run()` inside the import may conflict if the event loop is already running -- caveat for production.

The result is `MCP_TOOL_CATALOG` -- a string with all tools formatted -- injected into `generate_prompt` and `refine_prompt`. It is the [[Ontologia como Código|ontology]] of the system's capabilities.

## Role in the Thesis

The prompt-engineer is the server that optimizes the **delivery** of [[Contexto Programático|context]]. The other servers provide raw ontology (docs, diagrams). The prompt-engineer ensures this ontology is delivered in a structured way -- with role, few-shots, CoT, constraints.

In the thesis: poor [[Contexto]] -> [[Drift]]. Rich and **structured** [[Contexto]] -> [[Determinismo]]. The prompt-engineer is the structurer.

The [[Transformer-Driven Prompt Architect]] with its 6 mandatory sections is a formalization of how to assemble [[Contexto]] that maximizes [[Determinismo Mensurável|determinism]] -- each section attacks a dimension of the [[Espaço Amostral]].

## In the [[Cadeia de Servers]]

The prompt-engineer is the fourth server in the chain. It operates on knowledge already available (via [[docs-server]] and [[web-to-docs]]) to generate optimized prompts. The [[Catálogo de Tools]] it injects includes tools from the other 3 servers -- it is the meta-server that knows what the entire system can do.

---

Related to: [[Transformer-Driven Prompt Architect]], [[Catálogo de Tools]], [[Contexto Programático]], [[FastMCP]], [[Primitivas MCP]], [[Ontologia como Código]], [[Cadeia de Servers]], [[Determinismo Mensurável]], [[Anti-Alucinação]], [[docs-server]], [[web-to-docs]], [[system-design]]
