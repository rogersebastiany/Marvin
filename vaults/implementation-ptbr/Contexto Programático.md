# Contexto Programático

[[Contexto]] entregue via código — [[Primitivas MCP|tools]], [[Primitivas MCP|resources]], e [[Primitivas MCP|prompts]] MCP — em vez de copy-paste manual. O modelo acessa conhecimento externo programaticamente em O(1) via [[MCP]].

---

## A Diferença

**Sem contexto programático:** o humano lê a documentação, copia trechos relevantes, cola no prompt. Lento, incompleto, propenso a erro. O [[Contexto]] depende da capacidade humana de selecionar informação.

**Com contexto programático:** o [[Agente na POC|agente]] invoca `search_docs("authentication")` e recebe os trechos relevantes diretamente. Rápido, sistemático, completo dentro do escopo da busca. O contexto é entregue pela máquina.

## Formas de Contexto Programático na POC

**Tools (funções invocáveis):**
- `search_docs(query)` → busca keyword em todos os docs, retorna matches com contexto
- `crawl_docs(url, max_pages)` → crawlea documentação online e salva localmente
- `generate_diagram(description)` → gera diagrama com syntax references como contexto
- `audit_prompt(prompt)` → avalia prompt contra framework estruturado

**Resources (dados acessíveis):**
- `docs://{filename}` → conteúdo completo de um doc
- `diagrams://{filename}` → código mermaid de um diagrama

**Prompts (templates estruturados):**
- `explain_concept(topic)` → template para explicar um conceito usando docs
- `design_system(description)` → template para design end-to-end
- `research_and_answer(question)` → template para buscar local + web + responder

Cada forma é uma maneira diferente de injetar [[Ontologia como Código|ontologia]] no [[Contexto]] do modelo. Todas reduzem o [[Espaço Amostral]] efetivo.

## O(1) via MCP

O [[MCP]] torna o acesso ao contexto O(1) — para o modelo, chamar `search_docs` tem o mesmo custo cognitivo que acessar memória local. Não importa se o conhecimento está num arquivo markdown local ou (em produção) num [[S3 como Ontologia Persistente|bucket S3 encriptado na Irlanda]]. A interface é a mesma, o custo é constante.

Isso é o que torna a [[Ontologia]] completa viável em tempo real. Sem [[FastMCP]] e [[stdio]], cada acesso a contexto externo teria latência variável, autenticação diferente, formatos incompatíveis.

## Contexto Programático como [[Redução de Espaço na Prática|Redução de Espaço]]

Cada tool call é um condicionamento adicional na [[Probabilidade Condicional]]:

```
P(token|prompt) — primeira restrição
P(token|prompt, search_docs) — segunda restrição
P(token|prompt, search_docs, get_diagram) — terceira restrição
```

É [[Redução de Dimensionalidade]] concreta — cada chamada elimina dimensões irrelevantes do espaço de possibilidades.

---

Relaciona-se com: [[Contexto]], [[Primitivas MCP]], [[MCP]], [[FastMCP]], [[Ontologia como Código]], [[Redução de Espaço na Prática]], [[Agente na POC]], [[docs-server]], [[web-to-docs]], [[prompt-engineer]], [[system-design]]
