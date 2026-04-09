# FastMCP

A biblioteca Python que implementa o [[MCP]] (Model Context Protocol). Abstrai o protocolo em decorators simples — `@mcp.tool()`, `@mcp.resource()`, `@mcp.prompt()` — que registram [[Primitivas MCP]] automaticamente.

---

## Uso na POC

Cada server instancia um `FastMCP` com nome e instruções:

```python
from fastmcp import FastMCP
mcp = FastMCP("docs-server", instructions="Search and browse project documentation.")
```

E registra primitivas via decorators:

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

O `mcp.run()` no `__main__` inicia o server no transporte [[stdio]].

## O que FastMCP Abstrai

**Protocolo MCP:** serialização/deserialização JSON-RPC, handshake de capabilities, listagem de tools/resources/prompts.

**Transporte [[stdio]]:** leitura de stdin, escrita em stdout, framing de mensagens. O pipe bidirecional entre [[Agente na POC|agente]] e server.

**Type extraction:** FastMCP extrai parâmetros e tipos das assinaturas Python e docstrings. `search_docs(query: str)` vira um schema JSON com `{"query": {"type": "string"}}`. Essa extração automática é o que permite ao [[prompt-engineer]] auto-descobrir tools via `await server_mcp.list_tools()`.

## FastMCP como Viabilizador

Na tese, [[MCP]] é o endereçamento indireto O(1) para [[Contexto]] externo. FastMCP é a implementação que torna isso trivial para o desenvolvedor. Sem FastMCP, cada server precisaria implementar o protocolo manualmente — serialização, transporte, schema.

Com FastMCP, adicionar uma tool é adicionar uma função Python com um decorator. A barreira para construir [[Ontologia como Código|ontologia]] cai para quase zero.

## Dependência

```toml
[project]
dependencies = [
    "fastmcp>=3.0.0",
    "mcp[cli]>=1.4.1",
]
```

`fastmcp>=3.0.0` é a biblioteca principal. `mcp[cli]>=1.4.1` fornece o CLI e utilities do protocolo base.

---

Relaciona-se com: [[MCP]], [[Primitivas MCP]], [[stdio]], [[Ontologia como Código]], [[Catálogo de Tools]], [[docs-server]], [[web-to-docs]], [[prompt-engineer]], [[system-design]], [[Agente na POC]]
