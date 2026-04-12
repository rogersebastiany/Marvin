 ate q ta l# Contexto

O input que reduz o [[Espaço Amostral]]. Composto por prompt, [[Tool|tools]], histórico, e qualquer informação que condiciona a resposta do modelo. É o mecanismo central da [[Tautologia Ontológica]].

---

## Definição

Contexto é toda informação disponível para o modelo no momento da inferência. Inclui: o prompt do usuário, instruções do sistema, [[Tool|tools]] disponíveis e seus resultados, histórico da conversa, e qualquer dado injetado via [[MCP]].

Na [[Teoria dos Conjuntos]]: contexto é o operador que define o [[Subconjunto]] A ⊂ S do [[Espaço Amostral]].

## Contexto como Subconjunto de Vetores

O contexto é, em última instância, um conjunto de [[Vetor|vetores]]. O prompt é tokenizado ([[Tokenização]]), cada token é embeddado ([[Embedding]]) num vetor, e esses vetores definem a região do espaço onde o modelo opera.

Mais contexto = mais vetores = subconjunto mais preciso = menor erro de aproximação no cálculo de probabilidade.

## Contexto e Determinismo

Quanto mais enriquecido o contexto, menor o erro de aproximação no cálculo do próximo token. Contexto pobre → [[Drift]]. Contexto rico → [[Determinismo]].

O artigo [[DFAH]] demonstra quantitativamente essa relação: contexto estruturado (harness) produz 89-90%+ de determinismo.

## Formas de Contexto

Toda forma de contexto é equivalente funcionalmente — são [[Subconjunto|subconjuntos]] de [[Vetor|vetores]] que restringem S:

- **Prompt**: contexto explícito do usuário
- **[[Tool|Tools]]**: contexto programático (docs, APIs, specs)
- **[[MCP]]**: contexto externo em O(1) (logs, DBs, métricas)
- **[[RAG]]**: contexto histórico vetorizado (decisões passadas)
- **System prompt**: contexto de personalidade/role do [[Agente]]

Cumulativamente, todas essas formas constroem a [[Ontologia]].

---

Relaciona-se com: [[Espaço Amostral]], [[Subconjunto]], [[Vetor]], [[Ontologia]], [[Determinismo]], [[Drift]], [[Tool]], [[MCP]], [[RAG]], [[Agente]], [[Probabilidade Condicional]], [[DFAH]], [[Tautologia Ontológica]]
