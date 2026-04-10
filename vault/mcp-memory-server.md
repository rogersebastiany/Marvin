# mcp-memory-server

MCP server que expõe o vector database [[Milvus]] como tools para o [[Agente na POC|agente]]. Permite buscar memórias similares e logar novas ações.

---

## Tools

| Tool | Descrição |
|---|---|
No [[Marvin]] unificado, a memória episódica é acessada via:
- `retrieve()` — busca unificada que internamente consulta `search_tool_calls`, `search_decisions`, `search_sessions` no [[Milvus]]
- `log_decision` — registra uma decisão (objetivo, opções, escolha, reasoning)
- `log_session` — registra resumo de sessão (objetivo, abordagem, resultado, lições)

As funções de busca (`search_*`) são internas ao módulo `memory.py` — o agente nunca as chama diretamente, apenas através de `retrieve()`.

## Busca Antes de Agir

O padrão de uso: antes de tomar uma decisão, o agente chama `retrieve()` que busca no [[Milvus]] por ações similares. "Já fiz algo parecido? Funcionou? O que aprendi?"

```
Agente recebe objetivo → retrieve("migrar serviço para ECS")
    ↓ encontra decisão similar do passado (via Milvus)
    ↓ "última vez, usar Fargate foi melhor que EC2 porque..."
Agente decide informado → executa → log_decision(resultado)
```

Isso é **prefetching** no vocabulário do HCC ([[Acumulação Cognitiva]]): recuperar sabedoria similar antes de começar.

## Log Automático

Cada ação significativa é logada automaticamente:
- Tool calls: capturadas no momento da execução
- Decisões: capturadas quando o agente escolhe entre alternativas
- Sessões: capturadas no final de cada sessão

O log é append-only — nunca se apaga memória. O agente acumula experiência monotonicamente.

## Diferença do RAG Implícito

O [[RAG Implícito]] da POC busca texto em `docs/`. O mcp-memory-server busca **experiência semântica** por similaridade vetorial. A diferença:

- `search_docs("lambda")` → documentação sobre Lambda
- `search_tool_calls("deploy lambda function")` → as últimas 5 vezes que o agente fez deploy de Lambda, com contexto e resultado

Um é conhecimento do domínio. O outro é memória de ações.

---

Relaciona-se com: [[Milvus]], [[Embedding]], [[RAG Implícito]], [[Loop de Auto-Melhoria]], [[Acumulação Cognitiva]], [[Cadeia de Servers]], [[MCP]], [[FastMCP]]
