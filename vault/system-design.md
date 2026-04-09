# system-design

Ferramenta de domínio para diagramas arquiteturais. `system_design_server.py` gera e avalia diagramas [[Mermaid.js]] com um [[Scoring de Diagramas|framework de scoring]] em 4 dimensões. Carrega referências de sintaxe de `docs/mermaid-*.md` como [[Contexto Programático|contexto]] no startup.

---

## Implementação

```python
mcp = FastMCP("system-design",
    instructions="Generate and review system design diagrams using Mermaid.js syntax.")
DIAGRAMS_DIR = Path(__file__).parent / "diagrams"
```

Cinco [[Primitivas MCP|tools]], um [[Primitivas MCP|resource]], dois [[Primitivas MCP|prompts]]:

| Tipo | Nome | Função |
|---|---|---|
| Tool | `generate_diagram(description, type, save_as)` | Gera diagrama mermaid a partir de descrição natural |
| Tool | `judge_diagram(mermaid_code)` | Avalia diagrama em 4 dimensões, score 1-10 |
| Tool | `save_diagram(mermaid_code, filename)` | Salva `.mmd` em `diagrams/` |
| Tool | `list_diagrams()` | Lista diagramas salvos |
| Tool | `get_diagram(filename)` | Lê um diagrama salvo |
| Resource | `diagrams://{filename}` | Acesso O(1) a diagramas |
| Prompt | `design_system(description)` | Template: gera + explica + trade-offs + salva |
| Prompt | `review_architecture(filename)` | Template: carrega + julga + melhora se score < 7 |

## Contexto de Sintaxe

No startup, carrega todos os `docs/mermaid-*.md` como referência:

```python
def _load_syntax_refs() -> str:
    refs = []
    for doc in sorted(DOCS_DIR.glob("mermaid-*.md")):
        refs.append(doc.read_text())
    return "\n\n---\n\n".join(refs)
```

Esses syntax refs são injetados em `generate_diagram` e `judge_diagram`. O modelo não precisa lembrar sintaxe Mermaid do treinamento — recebe a referência completa como [[Contexto Programático|contexto]]. É [[Tool como Bias|bias]] concreto: "use ESTA sintaxe, não o que você acha que lembra."

## DIAGRAM_GUIDELINES

Constante com guidelines de design: quando usar C4Context vs Flowchart vs Sequence, best practices (label relationships, use boundaries, show external systems), e common patterns (API Gateway, Event-Driven, CQRS).

São as constraints que o [[Transformer-Driven Prompt Architect]] chamaria de "ATTENTION MASK" — dizem ao modelo como NÃO desenhar.

## Papel na Tese

O system-design demonstra [[Ontologia como Código|ontologia de domínio]]. A ontologia de diagramas arquiteturais está codificada em: syntax refs (como), guidelines (quando), e scoring (quão bem). O modelo não infere o que é um "bom diagrama" — está definido em 4 dimensões mensuráveis via [[Scoring de Diagramas]].

É [[Determinismo Mensurável|determinismo]] em ação: dado a mesma descrição e os mesmos syntax refs, o diagrama gerado é previsível e avaliável objetivamente.

## [[Path Traversal Protection]]

Usa `_safe_diagram_path()` — mesma lógica do [[docs-server]], mas confinada a `diagrams/`.

---

Relaciona-se com: [[Mermaid.js]], [[Scoring de Diagramas]], [[FastMCP]], [[Primitivas MCP]], [[Ontologia como Código]], [[Contexto Programático]], [[Tool como Bias]], [[Cadeia de Servers]], [[Path Traversal Protection]], [[Determinismo Mensurável]]
