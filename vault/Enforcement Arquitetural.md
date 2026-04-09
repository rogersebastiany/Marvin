# Enforcement Arquitetural

Restrições de comportamento do [[Agente na POC|agente]] devem ser impostas pela arquitetura (quais tools estão no config MCP), não pelo prompt. Se a tool não existe, a ação é impossível por construção.

---

## O Problema do Prompt

Um prompt é um [[Tool como Bias|bias]] — desloca probabilidade, não a elimina. "Não acesse a internet" é uma restrição soft. O modelo opera em espaço probabilístico — pode ignorar, reinterpretar, ou overridear a instrução.

A arquitetura é uma restrição absoluta. Se `web-to-docs` não está no `mcp.json`, o [[Agente na POC|agente]] não tem vetores de acesso web no [[Espaço Amostral]]. A probabilidade de ação web é zero — não baixa, zero.

## Duas Fases na POC

**Fase 1 — Construção da Ontologia**

```json
{
  "mcpServers": {
    "docs-server": { ... },
    "web-to-docs": { ... },
    "prompt-engineer": { ... },
    "system-design": { ... }
  }
}
```

O agente tem `web-to-docs`. Pode crawlear, salvar, expandir `docs/`. A [[Ontologia como Código|ontologia]] está incompleta — o acesso web é necessário para construí-la. É o [[Feedback Loop Determinístico]] em ação: não encontrou → buscou na web → salvou → agora encontra.

**Fase 2 — Uso da Ontologia**

```json
{
  "mcpServers": {
    "docs-server": { ... },
    "prompt-engineer": { ... },
    "system-design": { ... },
    "mcp-ontology-server": { ... },
    "mcp-memory-server": { ... }
  }
}
```

`web-to-docs` removido. [[mcp-ontology-server]] e [[mcp-memory-server]] adicionados. O agente opera exclusivamente sobre conhecimento mapeado — [[Neo4j]] para ontologia, [[Milvus]] para memória, `docs/` para texto. Se `search_docs` retorna "not found", o agente informa que é incapaz. Não inventa, não busca na web.

A transição é o momento em que a ontologia se torna completa: todo método do domínio tem uma [[Tool Tautológica]] correspondente.

## Em Produção

O [[MCP Gateway]] pode enforçar fases por configuração:
- Fase 1: gateway roteia para `web-to-docs` + `docs-server`
- Fase 2: gateway bloqueia `web-to-docs`, roteia para ontology + memory servers
- Audit log registra qualquer tentativa de acesso a tool bloqueada

O enforcement é no nível de infraestrutura, não de prompt.

## O Agente Ontologicamente Tautológico

O espaço de ações do agente É a ontologia do agente. As tools disponíveis definem o que pode fazer. Remover tool = reduzir S. Adicionar tool = expandir S.

A [[Tautologia Ontológica — Tese e Prova|tese]] se aplica recursivamente: a ontologia do agente (suas tools) deve ser ela mesma tautológica. Cada tool disponível deve ser [[Tool Tautológica|tautológica]]. Nenhuma tool desnecessária deve existir. O agente tem **exatamente** as tools que precisa — nem mais, nem menos.

---

Relaciona-se com: [[Tool Tautológica]], [[Tool como Bias]], [[Agente na POC]], [[Cadeia de Servers]], [[MCP Gateway]], [[Feedback Loop Determinístico]], [[Ontologia como Código]], [[Neo4j]], [[Milvus]], [[mcp-ontology-server]], [[mcp-memory-server]], [[Tautologia Ontológica — Tese e Prova]]
