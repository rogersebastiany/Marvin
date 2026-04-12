# Agente na POC

Qualquer cliente [[MCP]] que consome as 33 tools do [[Marvin]] (servidor unificado). Pode ser uma IDE (Cursor, VS Code, JetBrains), Claude Code, ou qualquer agente com suporte a MCP. Opera via [[ReAct na POC|ReAct]] com as [[Primitivas MCP|tools]] disponíveis via [[stdio]].

---

## Configuração

Os servers são configurados via `mcp.json` (formato padrão MCP):

```json
{
  "mcpServers": {
    "docs-server": { "type": "stdio", "command": "uv", "args": ["run", "python", "server.py"] },
    "web-to-docs": { "type": "stdio", "command": "uv", "args": ["run", "python", "web_to_docs_server.py"] },
    "prompt-engineer": { "type": "stdio", "command": "uv", "args": ["run", "python", "prompt_engineer_server.py"] },
    "system-design": { "type": "stdio", "command": "uv", "args": ["run", "python", "system_design_server.py"] }
  }
}
```

O cliente MCP spawna os 4 processos. Cada server fica disponível como fonte de [[Primitivas MCP|tools, resources e prompts]]. Nenhum start manual necessário.

## O Agente como Contexto Personificado

Na tese, [[Agente]] é "[[Contexto]] personificado com loop [[ReAct]]." Qualquer cliente MCP é exatamente isso:

- **Contexto:** system prompt + codebase + MCP tools + regras do projeto
- **Persona:** definida pelo system prompt (Senior Engineer, QA, PM, etc.)
- **ReAct loop:** raciocina (planeja), age (invoca tools), observa (incorpora resultado)
- **[[Tool|Tools]]:** as 15+ tools dos 4 servers, acessíveis via [[MCP]]

O agente não "sabe" a ontologia do domínio. Ele "acessa" a ontologia via [[docs-server]], "expande" via [[web-to-docs]], "otimiza" a entrega via [[prompt-engineer]], e "visualiza" via [[system-design]].

## O Ciclo do Agente na POC

```
Usuário pergunta "como funciona Lambda?"
    ↓
Agente raciocina: "vou buscar nos docs"
    ↓ Act
search_docs("lambda") → "No results found"
    ↓ Observe
Agente raciocina: "não tem docs locais, vou buscar na web"
    ↓ Act
crawl_docs("https://docs.aws.amazon.com/lambda/...") → "Crawled 15 pages"
    ↓ Observe
Agente raciocina: "agora tenho docs, vou buscar de novo"
    ↓ Act
search_docs("lambda") → matches em 8 arquivos
    ↓ Observe
Agente raciocina: "tenho informação suficiente para responder"
    ↓
Resposta baseada em docs verificados
```

Cada ciclo reason→act→observe é um passo do [[Feedback Loop Determinístico]]. Cada tool call é [[Redução de Espaço na Prática|redução de espaço]].

## Agnosticismo de Ferramenta

O protocolo [[MCP]] é padronizado. Qualquer cliente que implemente o protocolo pode consumir os 4 servers. O config `mcp.json` é portável entre ferramentas. A [[Ontologia como Código|ontologia]] servida não depende de qual agente a consome — a mesma [[Cadeia de Servers]] funciona com qualquer cliente MCP.

Isso reforça a tese: o [[Determinismo Mensurável|determinismo]] vem do [[Contexto Programático|contexto]] (a ontologia servida), não do agente. Troque o agente, mantenha as tools — o determinismo se mantém.

## Enforcement Arquitetural

O que o agente pode fazer é definido pela lista de tools no config MCP — não pelo prompt. Se `web-to-docs` não está no `mcp.json`, o agente não pode acessar a internet. Não é "por favor não faça" — é "não pode fazer." Restrições devem ser [[Enforcement Arquitetural|arquiteturais]], não textuais. Ver [[Enforcement Arquitetural]].

---

Relaciona-se com: [[Agente]], [[ReAct na POC]], [[stdio]], [[Primitivas MCP]], [[Cadeia de Servers]], [[Feedback Loop Determinístico]], [[Redução de Espaço na Prática]], [[Ontologia como Código]], [[Determinismo Mensurável]], [[docs-server]], [[web-to-docs]], [[prompt-engineer]], [[system-design]], [[mcp-ontology-server]], [[mcp-memory-server]], [[Loop de Auto-Melhoria]], [[Enforcement Arquitetural]]
