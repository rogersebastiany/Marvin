# RAG Implícito

O diretório `docs/` da POC funciona como um [[RAG]] simplificado. Sem vector database, sem [[Embedding|embeddings]] para busca semântica — mas o padrão é o mesmo: salvar conhecimento → recuperar depois → contexto cumulativo.

---

## Como Funciona na POC

**Retrieval:** `search_docs(query)` busca keyword em todos os `.md` de `docs/`. Não é busca semântica (por [[Vetor|vetores]]), é busca por substring — mas o efeito é análogo: dado uma query, retorna contexto relevante.

**Augmented:** O resultado de `search_docs` entra no [[Contexto Programático|contexto]] do [[Agente na POC]]. O modelo gera a resposta com base no que foi recuperado, não no que "lembra" do treinamento.

**Generation:** O modelo gera usando o contexto recuperado como [[Tool como Bias|bias]] — os docs encontrados deslocam o cálculo na direção correta.

## Retrieval → Augmented → Generation na POC

```
1. Retrieval: search_docs("JWT") → matches em architecture.md
2. Augmented: resultado injetado no contexto do agente
3. Generation: agente responde com base nos docs, não na Matriz M
```

## O que Falta para RAG Completo

| Aspecto | POC (RAG Implícito) | RAG Completo |
|---|---|---|
| Storage | Filesystem local (`docs/`) | Vector DB (Pinecone, Weaviate, etc.) |
| Busca | Keyword (substring match) | Semântica (cosine similarity de [[Embedding\|embeddings]]) |
| Indexação | Nenhuma (glob + read) | [[Embedding]] de chunks + índice vetorial |
| Persistência | Arquivos `.md` | Vetores + metadados |
| Acumulação | `crawl_docs` salva novos docs | Cada interação gera novos embeddings |

## Papel na Tese

Na tese, [[RAG]] é a "memória de longo prazo" — vetoriza metadados e permite busca semântica no histórico completo. O [[RAG Implícito]] da POC é uma versão degradada mas funcional: o histórico está nos arquivos de `docs/`, não em vetores, mas o princípio é o mesmo.

O artigo [[Ultra-Long-Horizon Agentic Science]] descreve como acumulação de conhecimento estruturado aumenta o [[Determinismo]] ao longo do tempo. Na POC, cada `crawl_docs` e `save_as_doc` é acumulação concreta. O "+" do 89%+ ([[DFAH]]) vem daqui.

## Caminho para RAG Completo

O [[mcp-memory-server]] com [[Milvus]] é a evolução direta: busca por similaridade vetorial em três coleções (tool calls, decisões, sessões). O [[mcp-ontology-server]] com [[Neo4j]] adiciona busca por relações no grafo de conceitos.

O artigo [[LLM Output Drift]] mostra que tarefas RAG são as **mais sensíveis a drift**. Isso torna a evolução de keyword search para busca semântica ainda mais crítica — a busca semântica retorna contexto mais preciso, reduzindo o [[Espaço Amostral]] mais efetivamente.

---

Relaciona-se com: [[RAG]], [[docs-server]], [[web-to-docs]], [[Feedback Loop Determinístico]], [[Contexto Programático]], [[Tool como Bias]], [[Agente na POC]], [[Ultra-Long-Horizon Agentic Science]], [[DFAH]], [[S3 como Ontologia Persistente]], [[Embedding]], [[Milvus]], [[Neo4j]], [[mcp-memory-server]], [[mcp-ontology-server]], [[LLM Output Drift]]
