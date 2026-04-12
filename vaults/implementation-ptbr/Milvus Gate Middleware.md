# Milvus Gate Middleware

Middleware arquitetural que bloqueia TODAS as operações de leitura Neo4j e escrita até que uma busca Milvus tenha sido feita na sessão. Implementa o princípio [[Enforcement Arquitetural|Retrieve Before Act]] com P=0 — não é bias de prompt, é impossibilidade arquitetural.

---

## Por que Existe

O [[Agente na POC|agente]] tende a agir antes de consultar. Prompts dizendo "busque primeiro" são bias — o modelo pode ignorar. A middleware transforma "deveria buscar" em "não consegue agir sem buscar". A ação sem contexto se torna impossível, não improvável.

## Classificação de Tools em 4 Tiers

Cada tool do [[Marvin]] pertence a exatamente um tier:

| Tier | Comportamento | Exemplos |
|------|--------------|----------|
| **Milvus (abre o gate)** | Busca semântica — abre acesso | `retrieve`, `get_memory`, `search_docs`, `improve_code`, `tdd`, `orchestrate`, `refine_plan` |
| **Overview (sempre permitido)** | Leitura leve, sem side effects | `stats`, `list_concepts`, `list_docs`, `self_description`, `inspect_schemas` |
| **Neo4j Read (gated)** | Leitura do grafo — requer gate aberto | `get_concept`, `traverse`, `why_exists`, `audit_code` |
| **Write (gated)** | Escrita em qualquer backend — requer gate aberto | `expand`, `link`, `save_doc`, `sync_vaults`, `self_improve` |
| **Always Allowed** | Operações sem risco | `log_decision`, `log_session`, `fetch_url`, `audit_prompt` |

## Como Funciona

```
RetrieveBeforeActMiddleware.on_call_tool(tool_name):
    if tool in MILVUS_TOOLS:
        session.milvus_gate = True    # abre o gate
        return proceed()
    if tool in OVERVIEW_TOOLS or tool in ALWAYS_ALLOWED:
        return proceed()              # sempre passa
    if tool in GATED_TOOLS:
        if not session.milvus_gate:
            return BLOCKED             # P=0, impossível
        return proceed()
```

O gate é por sessão. Cada nova sessão MCP começa fechado. A primeira operação útil deve ser uma busca semântica.

## Relação com Fases da Ontologia

A tese descreve duas fases:
- **Fase 1 (Construção)**: acesso web habilitado, tools de pesquisa disponíveis
- **Fase 2 (Uso)**: só tools tautológicas, web bloqueado

O Milvus Gate é Fase 1.5 — permite tudo, mas força o agente a consultar antes de agir. A transição para Fase 2 completa requer enforcement no nível do host (Claude Code hooks), não só no MCP server.

## Implementação

Classe `RetrieveBeforeActMiddleware` em `marvin_server.py`. Usa o sistema de middleware do FastMCP — intercepta `on_call_tool` antes da execução. Constantes `MILVUS_TOOLS`, `OVERVIEW_TOOLS`, `NEO4J_READ_TOOLS`, `WRITE_TOOLS` como frozensets para lookup O(1).

---

Relaciona-se com: [[Enforcement Arquitetural]], [[Marvin]], [[Milvus]], [[Neo4j]], [[Tool Tautológica]]
