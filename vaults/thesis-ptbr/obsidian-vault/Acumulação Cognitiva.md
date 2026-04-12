# Acumulação Cognitiva

O processo pelo qual um [[Agente]] transforma experiência transiente em conhecimento validado e, eventualmente, em sabedoria reutilizável. Não é agregação linear de [[Contexto]] — é destilação progressiva.

---

## Definição

Acumulação Cognitiva é o mecanismo que permite [[Determinismo]] crescente ao longo do tempo. Cada interação do agente produz experiência raw. Essa experiência é refinada em conhecimento. O conhecimento, validado entre tarefas, cristaliza em sabedoria.

Experiência → Conhecimento → Sabedoria.

## O Framework HCC

O artigo [[Ultra-Long-Horizon Agentic Science]] formaliza isso no Hierarchical Cognitive Caching (HCC):

- **L1 (Experience)**: Traces de execução, patches, logs. Working memory.
- **L2 (Knowledge)**: Julgamentos, insights, resumos estratégicos. Memória de médio prazo.
- **L3 (Wisdom)**: Estratégias transferíveis, priors estáveis. Memória de longo prazo, recuperável via [[Embedding]] e similaridade de cosseno.

Context migration move informação entre camadas: prefetching (L3→contexto), context hit (L1 ou L2→contexto), context promotion (L1→L2 via P1, L2→L3 via P2).

## Na Tese

A equação da [[Tautologia Ontológica]] — Spec + BDD + TDD + ADR + Observabilidade + [[MCP]] + [[RAG]] — é um framework de acumulação cognitiva. Cada camada adiciona [[Contexto]] estruturado que persiste e se acumula:

- Specs e BDD/TDD = conhecimento validado (L2)
- ADR = sabedoria de decisões arquiteturais (L3)
- Observabilidade = experiência contínua (L1)
- [[MCP]] + [[RAG]] = mecanismo de acesso O(1) a todas as camadas

O [[Feedback Loop Determinístico]] é o mecanismo de promoção: experiência de uma sessão → docs salvos → conhecimento disponível na próxima sessão → sabedoria acumulada no corpus.

## Distinção Crucial

Acumulação Cognitiva ≠ contexto maior. O artigo mostra que contexto linear cresce para 200k+ tokens e satura. HCC mantém ~70k tokens efetivos. A diferença: destilação e promoção, não concatenação.

Na [[Redução de Dimensionalidade|mesma lógica]]: mais informação não é mais contexto. Informação destilada e estruturada é mais contexto.

---

Relaciona-se com: [[Ultra-Long-Horizon Agentic Science]], [[Determinismo]], [[Contexto]], [[Agente]], [[RAG]], [[MCP]], [[Embedding]], [[Tautologia Ontológica]], [[Feedback Loop Determinístico]]
