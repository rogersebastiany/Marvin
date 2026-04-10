# Acumulação Cognitiva

O processo pelo qual o [[Agente na POC|agente]] transforma experiência em conhecimento e conhecimento em sabedoria. Formalizado pelo HCC (Hierarchical Cognitive Caching) do artigo [[Ultra-Long-Horizon Agentic Science]]. Validado pelo design de três coleções do [[Milvus]].

---

## Definição

Acumulação Cognitiva ≠ contexto maior. Concatenar tudo produz saturação (200k+ tokens). Acumulação Cognitiva é **destilação progressiva**: experiência raw → julgamentos validados → sabedoria transferível.

## Três Camadas na Arquitetura

| Camada HCC | Papel | Implementação |
|---|---|---|
| L1 — Experience | Working memory, traces raw | Tool calls no [[Milvus]] (~6KB cada) |
| L2 — Knowledge | Julgamentos e insights destilados | Decisões no [[Milvus]] (~6KB cada) |
| L3 — Wisdom | Estratégias transferíveis entre tarefas | Sessões no [[Milvus]] (~6KB cada) |

O artigo prova que todas as três camadas são necessárias:
- Sem L1: medal rate cai de 72.7% para 22.7%
- Sem L2: cai para 59.1%
- Sem L3: cai para 54.5%

## Na POC Atual

O [[Feedback Loop Determinístico]] já implementa uma versão simples:
- `docs/` como L2/L3 (conhecimento e sabedoria persistidos)
- Tool call outputs como L1 (experiência da sessão)

A evolução para [[Neo4j]] + [[Milvus]] adiciona:
- [[Embedding|Embeddings]] para busca semântica
- Grafo para relações entre conceitos
- Três coleções separadas para três granularidades

## Context Migration

Três operações da [[Acumulação Cognitiva]] mapeadas para o [[Loop de Auto-Melhoria]]:

- **Prefetching**: Antes de agir, o agente chama `retrieve()` que busca sabedoria similar no Milvus (decisões e sessões). Começa informado.
- **Context Hit**: Durante a execução, busca experiência recente (`search_tool_calls`). Reutiliza o que funcionou.
- **Context Promotion**: Após completar, destila experiência em decisão (`log_decision`) e decisão em sessão (`log_session`). Cristaliza aprendizado.

---

Relaciona-se com: [[Ultra-Long-Horizon Agentic Science]], [[Milvus]], [[Neo4j]], [[Feedback Loop Determinístico]], [[Loop de Auto-Melhoria]], [[Embedding]], [[Determinismo Mensurável]], [[Contexto Programático]]
