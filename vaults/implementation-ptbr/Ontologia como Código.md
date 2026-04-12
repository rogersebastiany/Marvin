# Ontologia como Código

A materialização da [[Ontologia]] em artefatos de software. Na POC, a ontologia não é um diagrama conceitual — é código, markdown, e descrições de [[Primitivas MCP|tools]] que o modelo consome diretamente.

---

## Onde Vive a Ontologia na POC

A ontologia está distribuída em três camadas:

**1. Documentação em `docs/`**
Arquivos markdown que contêm o conhecimento do domínio. O [[docs-server]] os expõe via `search_docs`, `list_docs`, e o resource `docs://{filename}`. Cada arquivo é um pedaço da ontologia — a definição de "o que existe" num domínio específico.

**2. Diagramas em `diagrams/`**
Arquivos `.mmd` ([[Mermaid.js]]) que codificam relações arquiteturais. O [[system-design]] os gera, avalia, e expõe via `diagrams://{filename}`. A ontologia visual — como as entidades se conectam.

**3. Descrições de Tools**
Cada `@mcp.tool()` tem uma docstring que é [[Tokenização|tokenizada]], [[Embedding|embeddada]], e vira [[Tool como Bias|bias]] no cálculo do próximo token. A descrição `"Search across all documentation files for a keyword or phrase"` não é apenas documentação para humanos — é ontologia para o modelo.

## Ontologia Expansível

A ontologia na POC não é estática. O [[web-to-docs]] expande o `docs/` continuamente:
- `save_as_doc(url, filename)` → adiciona uma página
- `batch_convert(urls)` → adiciona múltiplas páginas
- `crawl_docs(url, max_pages)` → crawlea uma seção inteira de documentação

Cada adição expande a [[Ontologia]], reduz o [[Espaço Amostral]] efetivo, e aumenta o [[Determinismo Mensurável|determinismo]]. É o [[Feedback Loop Determinístico]] em ação.

## Ontologia Servida vs Ontologia Treinada

A [[Matriz M]] contém a ontologia aprendida no treinamento — fixa, genérica, desatualizada. A ontologia via [[MCP]] é dinâmica, específica, e atual. A POC demonstra que o caminho para [[Determinismo]] não é retreinar o modelo — é servir a ontologia correta no momento certo.

Na [[Arquitetura de Produção]], `docs/` local vira [[S3 como Ontologia Persistente|S3 encriptado]] — a mesma ontologia, mas com escala, durabilidade, e isolamento por [[Tenant Isolation|tenant]].

## Evolução: Ontologia Viva

A ontologia estática em `docs/` e `diagrams/` é o ponto de partida. A evolução: [[Neo4j]] como knowledge graph (conceitos + relações, traversáveis) + [[Milvus]] como memória episódica (tool calls + decisões + sessões, buscáveis por similaridade). O [[Loop de Auto-Melhoria]] enriquece a ontologia a cada interação do agente. A ontologia deixa de ser "código" e passa a ser "organismo."

---

Relaciona-se com: [[Ontologia]], [[docs-server]], [[web-to-docs]], [[system-design]], [[Primitivas MCP]], [[Tool como Bias]], [[Feedback Loop Determinístico]], [[Contexto Programático]], [[MCP]], [[S3 como Ontologia Persistente]], [[Neo4j]], [[Milvus]], [[Loop de Auto-Melhoria]]
