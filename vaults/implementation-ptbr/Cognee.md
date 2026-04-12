# Cognee

Framework modular para construir e consultar knowledge graphs a partir de texto. Substituiu o pipeline Pythonístico legado (`load_vaults.py`) como o engine de extração de KG. O [[Agente na POC|agente]] usa Cognee indiretamente — os vaults Obsidian passam por Cognee e viram nós `:Concept` no [[Neo4j]].

---

## Por que Cognee

O pipeline anterior usava regex + classificador para mapear wikilinks existentes em relações tipadas. Isso criava um teto: só classificava links que já existiam nas notas, nunca descobria conceitos ou relações novas. Na prática, 58.2% de arestas tipadas — o resto caía em `RELATES_TO` genérico.

Cognee resolve isso usando LLM para ler prosa e extrair entidades + relações tipadas do contexto. Não depende de wikilinks pré-existentes. O paper que validou a abordagem — "Optimizing the Interface Between Knowledge Graphs and LLMs for Complex Reasoning" (arXiv 2505.24478) — mostra que o tuning sistemático de parâmetros (chunking, construção de grafo, retrieval) produz ganhos mensuráveis em benchmarks de raciocínio multi-hop (HotPotQA, TwoWikiMultiHop, MuSiQue).

## Duas Eras

**Era 1 — KnowledgeGraph default + pós-processamento.** Cognee com modelo `KnowledgeGraph` padrão produziu 13.659 arestas, mas com typos de LLM nos tipos de relação, gaps de mapeamento, e 16% de fallback `RELATES_TO`. O pós-processamento via keyword matching tentava corrigir, mas era frágil.

**Era 2 — Concept(DataPoint) customizado.** Modelo `Concept` herdando de `DataPoint` com 16 campos de relação tipados (Pydantic). O schema JSON impõe os tipos no momento da extração — o LLM não inventa tipos. Resultado: 547 conceitos, 1.844 arestas, 16 tipos exatos, zero typos.

A chave foi descobrir o branch no `extract_graph_from_data.py` do Cognee: quando `graph_model is not KnowledgeGraph`, ele bypassa o fluxo default de `Entity` e escreve o label do modelo diretamente no Neo4j.

## Rate Limiting

O `llm_rate_limit_requests` do Cognee é um backoff reativo (pós-429), não um throttle preventivo. Com batches grandes, dispara dezenas de chamadas paralelas e estoura o rate limit instantaneamente. Configuração que funciona no Tier 1 da OpenAI: `chunks_per_batch=1, data_per_batch=1, llm_rate_limit_requests=2`. Runtime: ~7h para wipe completo, ~14-17 chunks/min.

## Pipeline

```
Vaults Obsidian → cognify_vaults.py → Cognee → Neo4j (:Concept)
                                                  ↓
                                    sync (ops_backend) → Milvus
```

1. `cognify_vaults.py` lê os 4 vaults e alimenta Cognee com `graph_model=Concept`
2. Cognee extrai conceitos e relações, persiste no [[Neo4j]] e LanceDB
3. `sync_vaults` (tool MCP) ou `ops_backend.sync()` re-indexa os `:Concept` do Neo4j no [[Milvus]]

O agente nunca chama Cognee diretamente. Cognee é infraestrutura de ingestão, não de consulta.

## Papel na Arquitetura

Cognee é o elo entre vaults Obsidian (conhecimento humano) e o knowledge graph (conhecimento computável). Sem Cognee, os conceitos dos vaults seriam texto solto. Com Cognee, cada conceito vira um nó traversável com relações tipadas — a base para [[Redução de Espaço na Prática|redução de espaço]] e [[Determinismo Mensurável|determinismo]].

---

Relaciona-se com: [[Neo4j]], [[Milvus]], [[Ontologia como Código]], [[Loop de Auto-Melhoria]], [[Agente na POC]]
