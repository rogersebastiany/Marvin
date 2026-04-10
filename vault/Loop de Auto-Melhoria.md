# Loop de Auto-Melhoria

O ciclo em que o [[Agente na POC|agente]] usa sua própria ontologia ([[Neo4j]]) e memória ([[Milvus]]) para melhorar a si mesmo. Cada ação enriquece o contexto da próxima ação. O sistema fica mais determinístico com o uso.

---

## O Ciclo

```
1. Agente recebe objetivo
2. Consulta Neo4j (mcp-ontology-server): "O que sei sobre esse domínio?"
3. Consulta Milvus (mcp-memory-server): "Já fiz algo parecido?"
4. Age informado — com contexto ontológico + memória episódica
5. Loga a ação em Milvus (tool call, decisão)
6. Descobre novo conceito/relação → registra em Neo4j
7. Próximo ciclo: Neo4j mais rico + Milvus com mais memória
```

Cada ciclo:
- **Expande a [[Ontologia como Código|ontologia]]**: mais conceitos e relações no grafo
- **Acumula memória**: mais tool calls, decisões, e sessões no Milvus
- **Aumenta [[Determinismo Mensurável|determinismo]]**: mais [[Contexto Programático|contexto]] disponível → menor [[Espaço Amostral]] → menos [[Drift]]

## Evolução do Feedback Loop

O [[Feedback Loop Determinístico]] da POC opera em `docs/` — busca → não achou → crawl → salva → busca de novo. É o loop curto.

O Loop de Auto-Melhoria é a evolução:
- **POC**: docs em filesystem → busca textual
- **Evolução**: ontologia em [[Neo4j]] → busca semântica por conceitos e relações + memória em [[Milvus]] → busca por similaridade vetorial

O mecanismo é o mesmo (acumulação monotônica), mas a representação é mais rica: grafo + vetores em vez de texto plano.

## Paralelo com HCC

O artigo [[Ultra-Long-Horizon Agentic Science]] valida este design com o HCC:

| HCC | Loop de Auto-Melhoria |
|---|---|
| L1 — Evolving Experience | Tool calls logadas no [[Milvus]] |
| L2 — Refined Knowledge | Decisões logadas no [[Milvus]] |
| L3 — Prior Wisdom | Sessões logadas no [[Milvus]] |
| Context Prefetching | `retrieve()` busca memória antes de agir |
| Context Promotion | Conceitos descobertos → [[Neo4j]] via `expand` |

A diferença: HCC usa sumarização/compressão. Nós usamos [[Embedding|embeddings]] + similaridade de cosseno. Mas a estrutura de três tiers é a mesma, e a ablation study do HCC valida que todas as três camadas são necessárias.

## Por que É "Auto"

O agente melhora a si mesmo sem intervenção:
- Descobre um conceito não mapeado → adiciona ao [[Neo4j]]
- Uma abordagem falha → logada no [[Milvus]] → evitada no futuro
- Uma abordagem funciona → logada → reutilizada

Não é fine-tuning do modelo. É enriquecimento do [[Contexto Programático|contexto]]. O modelo é o mesmo — o que muda é a [[Ontologia como Código|ontologia]] e a memória acessíveis via [[MCP]].

## Na Tese

Este loop é a materialização completa da [[Tautologia Ontológica]]: a [[Ontologia]] se torna cada vez mais completa com o uso → a [[Tautologia]] se estabelece progressivamente → o [[Determinismo]] cresce monotonicamente.

É o [[Deterministic Trajectory Optimization]] em ação: começa probabilístico (pouca ontologia), itera (cada ciclo adiciona contexto), converge para determinístico (ontologia completa).

---

Relaciona-se com: [[Neo4j]], [[Milvus]], [[mcp-ontology-server]], [[mcp-memory-server]], [[Feedback Loop Determinístico]], [[Acumulação Cognitiva]], [[Determinismo Mensurável]], [[Ontologia como Código]], [[Contexto Programático]], [[MCP]], [[Tautologia Ontológica]]
