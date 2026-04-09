# Ontology as Code

The materialization of [[Ontologia]] into software artifacts. In the POC, the ontology is not a conceptual diagram -- it is code, markdown, and [[Primitivas MCP|tool]] descriptions that the model consumes directly.

---

## Where the Ontology Lives in the POC

The ontology is distributed across three layers:

**1. Documentation in `docs/`**
Markdown files containing domain knowledge. The [[docs-server]] exposes them via `search_docs`, `list_docs`, and the `docs://{filename}` resource. Each file is a piece of the ontology -- the definition of "what exists" in a specific domain.

**2. Diagrams in `diagrams/`**
`.mmd` files ([[Mermaid.js]]) that encode architectural relationships. The [[system-design]] generates, evaluates, and exposes them via `diagrams://{filename}`. The visual ontology -- how entities connect.

**3. Tool Descriptions**
Each `@mcp.tool()` has a docstring that is [[Tokenização|tokenized]], [[Embedding|embedded]], and becomes [[Tool como Bias|bias]] in the next token calculation. The description `"Search across all documentation files for a keyword or phrase"` is not just documentation for humans -- it is ontology for the model.

## Expandable Ontology

The ontology in the POC is not static. [[web-to-docs]] continuously expands `docs/`:
- `save_as_doc(url, filename)` -> adds a page
- `batch_convert(urls)` -> adds multiple pages
- `crawl_docs(url, max_pages)` -> crawls an entire documentation section

Each addition expands the [[Ontologia]], reduces the effective [[Espaço Amostral]], and increases [[Determinismo Mensurável|determinism]]. It is the [[Feedback Loop Determinístico]] in action.

## Served Ontology vs Trained Ontology

The [[Matriz M]] contains the ontology learned during training -- fixed, generic, outdated. The ontology via [[MCP]] is dynamic, specific, and current. The POC demonstrates that the path to [[Determinismo]] is not retraining the model -- it is serving the correct ontology at the right moment.

In the [[Arquitetura de Produção]], the local `docs/` becomes [[S3 como Ontologia Persistente|encrypted S3]] -- the same ontology, but with scale, durability, and isolation per [[Tenant Isolation|tenant]].

## Evolution: Living Ontology

The static ontology in `docs/` and `diagrams/` is the starting point. The evolution: [[Neo4j]] as a knowledge graph (concepts + relationships, traversable) + [[Milvus]] as episodic memory (tool calls + decisions + sessions, searchable by similarity). The [[Loop de Auto-Melhoria]] enriches the ontology with every agent interaction. The ontology ceases to be "code" and becomes an "organism."

---

Related to: [[Ontologia]], [[docs-server]], [[web-to-docs]], [[system-design]], [[Primitivas MCP]], [[Tool como Bias]], [[Feedback Loop Determinístico]], [[Contexto Programático]], [[MCP]], [[S3 como Ontologia Persistente]], [[Neo4j]], [[Milvus]], [[Loop de Auto-Melhoria]]
