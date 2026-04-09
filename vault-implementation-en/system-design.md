# system-design

Domain tool for architectural diagrams. `system_design_server.py` generates and evaluates [[Mermaid.js]] diagrams with a [[Scoring de Diagramas|scoring framework]] across 4 dimensions. Loads syntax references from `docs/mermaid-*.md` as [[Contexto Programático|context]] at startup.

---

## Implementation

```python
mcp = FastMCP("system-design",
    instructions="Generate and review system design diagrams using Mermaid.js syntax.")
DIAGRAMS_DIR = Path(__file__).parent / "diagrams"
```

Five [[Primitivas MCP|tools]], one [[Primitivas MCP|resource]], two [[Primitivas MCP|prompts]]:

| Type | Name | Function |
|---|---|---|
| Tool | `generate_diagram(description, type, save_as)` | Generates mermaid diagram from natural language description |
| Tool | `judge_diagram(mermaid_code)` | Evaluates diagram across 4 dimensions, scores 1-10 |
| Tool | `save_diagram(mermaid_code, filename)` | Saves `.mmd` to `diagrams/` |
| Tool | `list_diagrams()` | Lists saved diagrams |
| Tool | `get_diagram(filename)` | Reads a saved diagram |
| Resource | `diagrams://{filename}` | O(1) access to diagrams |
| Prompt | `design_system(description)` | Template: generate + explain + trade-offs + save |
| Prompt | `review_architecture(filename)` | Template: load + judge + improve if score < 7 |

## Syntax Context

At startup, loads all `docs/mermaid-*.md` as reference:

```python
def _load_syntax_refs() -> str:
    refs = []
    for doc in sorted(DOCS_DIR.glob("mermaid-*.md")):
        refs.append(doc.read_text())
    return "\n\n---\n\n".join(refs)
```

These syntax refs are injected into `generate_diagram` and `judge_diagram`. The model does not need to remember Mermaid syntax from training -- it receives the complete reference as [[Contexto Programático|context]]. It is concrete [[Tool como Bias|bias]]: "use THIS syntax, not what you think you remember."

## DIAGRAM_GUIDELINES

A constant with design guidelines: when to use C4Context vs Flowchart vs Sequence, best practices (label relationships, use boundaries, show external systems), and common patterns (API Gateway, Event-Driven, CQRS).

These are the constraints that the [[Transformer-Driven Prompt Architect]] would call "ATTENTION MASK" -- they tell the model how NOT to draw.

## Role in the Thesis

system-design demonstrates [[Ontologia como Código|domain ontology]]. The architectural diagram ontology is encoded in: syntax refs (how), guidelines (when), and scoring (how well). The model does not infer what a "good diagram" is -- it is defined in 4 measurable dimensions via [[Scoring de Diagramas]].

It is [[Determinismo Mensurável|determinism]] in action: given the same description and the same syntax refs, the generated diagram is predictable and objectively evaluable.

## [[Path Traversal Protection]]

Uses `_safe_diagram_path()` -- same logic as [[docs-server]], but confined to `diagrams/`.

---

Related to: [[Mermaid.js]], [[Scoring de Diagramas]], [[FastMCP]], [[Primitivas MCP]], [[Ontologia como Código]], [[Contexto Programático]], [[Tool como Bias]], [[Cadeia de Servers]], [[Path Traversal Protection]], [[Determinismo Mensurável]]
