# Primitivas MCP

Os três tipos de [[Contexto Programático|contexto programático]] que um server [[MCP]] pode expor: **Tools** (funções invocáveis), **Resources** (dados acessíveis), e **Prompts** (templates estruturados). Cada tipo é um mecanismo diferente de entregar [[Ontologia como Código|ontologia]] ao modelo.

---

## Tools

Funções que o [[Agente na POC|agente]] pode invocar. O agente decide quando e como chamar. Cada tool recebe parâmetros, executa lógica, e retorna resultado como novo [[Contexto]].

Na POC: `search_docs(query)`, `crawl_docs(url)`, `generate_diagram(description)`, `audit_prompt(prompt)`, etc.

Na tese: cada tool é um [[Subconjunto]] de [[Vetor|vetores]] que funciona como [[Tool como Bias|bias]]. A descrição da tool é tokenizada e embeddada — o modelo "sabe" que a tool existe e o que ela faz antes mesmo de chamá-la.

Registradas via `@mcp.tool()` no [[FastMCP]].

## Resources

Dados que o agente pode ler diretamente. Acesso O(1) a conteúdo sem lógica de busca — o agente especifica o URI e recebe o conteúdo completo.

Na POC:
- `docs://{filename}` → conteúdo completo de um markdown em `docs/`
- `diagrams://{filename}` → código mermaid de um diagrama em `diagrams/`

Na tese: resources são acesso direto ao [[Subconjunto]] relevante da [[Ontologia como Código|ontologia]]. Enquanto tools buscam e filtram, resources entregam o conteúdo bruto.

Registrados via `@mcp.resource("uri://{param}")` no [[FastMCP]].

## Prompts

Templates que guiam o agente em workflows complexos. O agente não precisa inventar a sequência de tools — o prompt define o passo-a-passo.

Na POC:
- `research_and_answer(question)` → busca local → web → salva → responde
- `design_system(description)` → gera diagrama → explica → trade-offs → salva
- `improve_my_prompt()` → audit → refine

Na tese: prompts MCP são [[Contexto]] que reduz a dimensão "como fazer?" do [[Espaço Amostral]]. O agente não precisa raciocinar sobre a estratégia — está definida no template.

Registrados via `@mcp.prompt()` no [[FastMCP]].

## Interação entre Primitivas

Os três tipos se complementam:

1. **Prompt** define a estratégia: "busca local, depois web, depois responde"
2. **Tool** executa a ação: `search_docs()`, `crawl_docs()`
3. **Resource** provê dados adicionais: `docs://architecture.md`

Juntos, cobrem as três dimensões de [[Contexto Programático]]: o quê fazer (prompts), como fazer (tools), e com o quê fazer (resources).

---

Relaciona-se com: [[MCP]], [[FastMCP]], [[Contexto Programático]], [[Tool como Bias]], [[Ontologia como Código]], [[Agente na POC]], [[Catálogo de Tools]], [[docs-server]], [[web-to-docs]], [[prompt-engineer]], [[system-design]]
