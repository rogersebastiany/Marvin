# Catálogo de Tools

A lista completa de todas as [[Primitivas MCP|tools]] disponíveis em todos os servers, auto-descoberta pelo [[prompt-engineer]] no startup. É a [[Ontologia como Código|ontologia]] das capacidades do sistema — o modelo sabe o que pode e o que não pode fazer.

---

## Auto-Discovery

O `prompt_engineer_server.py` importa os 3 servers irmãos e lista suas tools:

```python
from server import mcp as docs_mcp
from web_to_docs_server import mcp as web_mcp
from system_design_server import mcp as design_mcp

servers = [
    ("docs-server", docs_mcp),
    ("web-to-docs", web_mcp),
    ("system-design", design_mcp),
]

async def _gather():
    catalog = []
    for server_name, server_mcp in servers:
        tools = await server_mcp.list_tools()
        # formata cada tool: nome, params, descrição
```

`asyncio.run()` executa a discovery síncrona no import time. O resultado é armazenado em `MCP_TOOL_CATALOG` — constante global usada em todas as tools do prompt-engineer.

## O Catálogo como Ontologia

O catálogo contém, para cada tool: nome, parâmetros (nome + tipo), e descrição. Formatado em markdown:

```
### docs-server
- `search_docs(query: string)` — Search across all documentation files...
- `list_docs()` — List all available documentation files
- `get_doc_summary(filename: string)` — Return the first section...

### web-to-docs
- `convert_url(url: string)` — Fetch a webpage and return...
...
```

Este catálogo é a resposta para "o que o sistema sabe fazer?" É a [[Ontologia]] das capacidades — não do domínio, mas das ferramentas que acessam o domínio.

## Injeção nos Prompts

O catálogo é injetado em `generate_prompt` e `refine_prompt`:

```python
f"## Available MCP Tools\n"
f"The following tools are available in this workspace. Use them in section 2 "
f"(KNOWLEDGE BEYOND WEIGHTS) of the generated prompt.\n\n"
f"{MCP_TOOL_CATALOG}\n\n"
```

Cada prompt gerado pelo [[Transformer-Driven Prompt Architect]] inclui a lista completa de tools. O modelo que recebe o prompt sabe exatamente quais ferramentas invocar — não precisa adivinhar. É [[Anti-Alucinação]] de capacidades.

## Papel na Tese

Na tese, [[Tool|tools]] são [[Subconjunto|subconjuntos]] de [[Vetor|vetores]] que funcionam como [[Tool como Bias|bias]]. O catálogo é o meta-bias — informa o modelo sobre todos os biases disponíveis. É [[Contexto]] sobre [[Contexto]].

O fato de ser auto-descoberto (não hardcoded) significa que adicionar um novo server com novas tools automaticamente expande o catálogo. A [[Ontologia como Código|ontologia]] cresce sem editar o prompt-engineer.

---

Relaciona-se com: [[prompt-engineer]], [[Primitivas MCP]], [[Ontologia como Código]], [[Tool como Bias]], [[Transformer-Driven Prompt Architect]], [[Anti-Alucinação]], [[Cadeia de Servers]], [[docs-server]], [[web-to-docs]], [[system-design]]
