# RAG

Retrieval Augmented Generation. Memória de longo prazo do sistema. Vetoriza metadados via [[Embedding]] e permite busca semântica no histórico completo.

---

## Definição

RAG é a técnica de aumentar a geração do modelo com informação recuperada de uma base de conhecimento vetorial. Em vez de depender apenas do que o modelo aprendeu no treinamento ([[Matriz M]]), o RAG busca informação relevante em tempo real e injeta no [[Contexto]].

## O Problema que Resolve

Sem RAG, o [[Contexto]] é limitado à janela do modelo naquela sessão. Conversas anteriores, decisões passadas, histórico do projeto — tudo se perde.

Com RAG vetorizando metadados (decisões, specs, resultados de testes, ADRs), o [[Agente]] consulta toda a história do projeto em O(1) via [[MCP]].

## O que Vetorizar

Não precisa vetorizar tudo — vetoriza os metadados: qual decisão foi tomada, quando, por quê, qual foi o resultado. Na hora da query, o RAG puxa os metadados relevantes via busca por similaridade de [[Vetor|vetores]] ([[Embedding]]), e o agente sabe onde buscar o contexto completo.

## Feedback Loop Determinístico

RAG fecha o ciclo: cada interação do [[Agente]] com o código é registrada → vetorizada → buscável. A próxima interação tem mais contexto → mais [[Determinismo]]. O loop só melhora com o tempo.

É o componente que viabiliza a acumulação de conhecimento estruturado descrita no artigo [[Ultra-Long-Horizon Agentic Science]]. O "+" do 89%+ vem daqui — [[Determinismo]] crescente com histórico crescente.

---

Relaciona-se com: [[Embedding]], [[MCP]], [[Contexto]], [[Vetor]], [[Agente]], [[Determinismo]], [[Ultra-Long-Horizon Agentic Science]], [[Ontologia]]
