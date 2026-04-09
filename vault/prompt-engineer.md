# prompt-engineer

O otimizador de [[Contexto Programático|contexto]]. `prompt_engineer_server.py` gera, refina e audita prompts usando o framework [[Transformer-Driven Prompt Architect]]. Auto-descobre todas as tools dos servers irmãos e injeta o [[Catálogo de Tools]] completo em cada prompt gerado.

---

## Implementação

```python
mcp = FastMCP("prompt-engineer",
    instructions="A Transformer-Driven Prompt Architect agent that generates structured, optimized prompts.")
```

Quatro [[Primitivas MCP|tools]], dois [[Primitivas MCP|prompts]]:

| Tipo | Nome | Função |
|---|---|---|
| Tool | `list_mcp_tools()` | Lista todas as tools de todos os servers |
| Tool | `generate_prompt(task, domain)` | Gera prompt estruturado com 6 seções + catálogo de tools |
| Tool | `refine_prompt(original, feedback)` | Melhora prompt existente baseado em feedback |
| Tool | `audit_prompt(prompt)` | Avalia prompt contra o framework, score 1-10, reescreve |
| Prompt | `architect_prompt(task)` | Template: gera prompt production-grade |
| Prompt | `improve_my_prompt()` | Template: audit → refine workflow |

## Auto-Discovery de Tools

No import time, o server descobre tools dos irmãos:

```python
def _discover_mcp_tools() -> str:
    from server import mcp as docs_mcp
    from web_to_docs_server import mcp as web_mcp
    from system_design_server import mcp as design_mcp
    # ... asyncio.run() para listar tools de cada server
```

Isso cria um acoplamento: os 3 servers irmãos devem ser importáveis quando o prompt-engineer inicia. O `asyncio.run()` dentro do import pode conflitar se o event loop já estiver rodando — caveat para produção.

O resultado é o `MCP_TOOL_CATALOG` — string com todas as tools formatadas — injetado em `generate_prompt` e `refine_prompt`. É a [[Ontologia como Código|ontologia]] das capacidades do sistema.

## Papel na Tese

O prompt-engineer é o server que otimiza a **entrega** de [[Contexto Programático|contexto]]. Os outros servers proveem ontologia bruta (docs, diagramas). O prompt-engineer garante que essa ontologia é entregue de forma estruturada — com role, few-shots, CoT, constraints.

Na tese: [[Contexto]] pobre → [[Drift]]. [[Contexto]] rico e **estruturado** → [[Determinismo]]. O prompt-engineer é o estruturador.

O [[Transformer-Driven Prompt Architect]] com suas 6 seções mandatórias é uma formalização de como montar [[Contexto]] que maximiza [[Determinismo Mensurável|determinismo]] — cada seção ataca uma dimensão do [[Espaço Amostral]].

## Na [[Cadeia de Servers]]

O prompt-engineer é o quarto server na cadeia. Opera sobre o conhecimento já disponível (via [[docs-server]] e [[web-to-docs]]) para gerar prompts otimizados. O [[Catálogo de Tools]] que ele injeta inclui tools dos outros 3 servers — é o meta-server que sabe o que o sistema inteiro pode fazer.

---

Relaciona-se com: [[Transformer-Driven Prompt Architect]], [[Catálogo de Tools]], [[Contexto Programático]], [[FastMCP]], [[Primitivas MCP]], [[Ontologia como Código]], [[Cadeia de Servers]], [[Determinismo Mensurável]], [[Anti-Alucinação]], [[docs-server]], [[web-to-docs]], [[system-design]]
