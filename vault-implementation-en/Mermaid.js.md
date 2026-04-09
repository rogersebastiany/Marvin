# Mermaid.js

Text-based diagramming language used by [[system-design]] to generate and evaluate architectural diagrams. The syntax refs in `docs/mermaid-*.md` are loaded as [[Contexto Programático|context]] at startup.

---

## Diagram Types in the POC

| Type | Keyword | Usage |
|---|---|---|
| C4Context | `C4Context` | High-level view: systems, actors, relationships |
| C4Container | `C4Container` | Zoom into a system: apps, APIs, DBs, queues |
| C4Component | `C4Component` | Zoom into a container: internal modules |
| Flowchart | `flowchart` | Process flows, data pipelines, CI/CD |
| Sequence | `sequenceDiagram` | Request flows, auth handshakes |
| Architecture (beta) | `architecture-beta` | Cloud infrastructure topology with icons |

## Syntax Refs as Ontology

The [[system-design]] loads `docs/mermaid-*.md` at startup:

```python
def _load_syntax_refs() -> str:
    refs = []
    for doc in sorted(DOCS_DIR.glob("mermaid-*.md")):
        refs.append(doc.read_text())
    return "\n\n---\n\n".join(refs)
```

These docs contain the [[Ontologia como Código|ontology]] of the Mermaid language: valid syntax, keywords, edge types, subgraph syntax, C4 macros. Without them, the model would depend on what it remembers from training ([[Matriz M]]) -- prone to syntax errors and outdated features.

With them, the model has the complete and up-to-date reference as [[Tool como Bias|bias]]. It is [[Redução de Espaço na Prática|space reduction]]: the universe of "possible ways to write a diagram" is constrained to the documented valid syntax.

## .mmd Files

Diagrams are saved as `.mmd` in `diagrams/`. The format is plain text -- the mermaid code without fences. Accessible via `diagrams://{filename}` (resource) or `get_diagram(filename)` (tool).

In the POC, there are two pre-saved diagrams: `aws-deployment.mmd` and `secure-mcp-platform.mmd` -- which document the [[Arquitetura de Produção]].

---

Related to: [[system-design]], [[Scoring de Diagramas]], [[Ontologia como Código]], [[Tool como Bias]], [[Contexto Programático]], [[Redução de Espaço na Prática]], [[Arquitetura de Produção]]
