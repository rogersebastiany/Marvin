# FastMCP

The Python library that implements [[MCP]] (Model Context Protocol). It abstracts the protocol into simple decorators -- `@mcp.tool()`, `@mcp.resource()`, `@mcp.prompt()` -- that register [[Primitivas MCP]] automatically.

---

## Usage in the POC

Each server instantiates a `FastMCP` with name and instructions:

```python
from fastmcp import FastMCP
mcp = FastMCP("docs-server", instructions="Search and browse project documentation.")
```

And registers primitives via decorators:

```python
@mcp.tool()
def search_docs(query: str) -> str:
    """Search across all documentation files for a keyword or phrase."""
    ...

@mcp.resource("docs://{filename}")
def read_doc(filename: str) -> str:
    ...

@mcp.prompt()
def explain_concept(topic: str) -> str:
    ...
```

The `mcp.run()` in `__main__` starts the server on the [[stdio]] transport.

## What FastMCP Abstracts

**MCP Protocol:** JSON-RPC serialization/deserialization, capabilities handshake, listing of tools/resources/prompts.

**[[stdio]] Transport:** reading from stdin, writing to stdout, message framing. The bidirectional pipe between [[Agente na POC|agent]] and server.

**Type extraction:** FastMCP extracts parameters and types from Python signatures and docstrings. `search_docs(query: str)` becomes a JSON schema with `{"query": {"type": "string"}}`. This automatic extraction is what allows the [[prompt-engineer]] to auto-discover tools via `await server_mcp.list_tools()`.

## FastMCP as Enabler

In the thesis, [[MCP]] is the O(1) indirect addressing for external [[Contexto]]. FastMCP is the implementation that makes this trivial for the developer. Without FastMCP, each server would need to implement the protocol manually -- serialization, transport, schema.

With FastMCP, adding a tool is adding a Python function with a decorator. The barrier to building [[Ontologia como Código|ontology]] drops to nearly zero.

## Dependency

```toml
[project]
dependencies = [
    "fastmcp>=3.0.0",
    "mcp[cli]>=1.4.1",
]
```

`fastmcp>=3.0.0` is the main library. `mcp[cli]>=1.4.1` provides the CLI and base protocol utilities.

---

Related to: [[MCP]], [[Primitivas MCP]], [[stdio]], [[Ontologia como Código]], [[Catálogo de Tools]], [[docs-server]], [[web-to-docs]], [[prompt-engineer]], [[system-design]], [[Agente na POC]]
