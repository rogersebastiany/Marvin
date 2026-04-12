# Mermaid.js

Linguagem de diagramação baseada em texto usada pelo [[system-design]] para gerar e avaliar diagramas arquiteturais. Os syntax refs em `docs/mermaid-*.md` são carregados como [[Contexto Programático|contexto]] no startup.

---

## Tipos de Diagrama na POC

| Tipo | Keyword | Uso |
|---|---|---|
| C4Context | `C4Context` | Visão alto nível: sistemas, atores, relações |
| C4Container | `C4Container` | Zoom num sistema: apps, APIs, DBs, queues |
| C4Component | `C4Component` | Zoom num container: módulos internos |
| Flowchart | `flowchart` | Fluxos de processo, data pipelines, CI/CD |
| Sequence | `sequenceDiagram` | Request flows, auth handshakes |
| Architecture (beta) | `architecture-beta` | Topologia de infraestrutura cloud com ícones |

## Syntax Refs como Ontologia

O [[system-design]] carrega `docs/mermaid-*.md` no startup:

```python
def _load_syntax_refs() -> str:
    refs = []
    for doc in sorted(DOCS_DIR.glob("mermaid-*.md")):
        refs.append(doc.read_text())
    return "\n\n---\n\n".join(refs)
```

Esses docs contêm a [[Ontologia como Código|ontologia]] da linguagem Mermaid: sintaxe válida, keywords, edge types, subgraph syntax, C4 macros. Sem eles, o modelo dependeria do que lembra do treinamento ([[Matriz M]]) — propenso a erros de sintaxe e features desatualizadas.

Com eles, o modelo tem a referência completa e atualizada como [[Tool como Bias|bias]]. É [[Redução de Espaço na Prática|redução de espaço]]: o universo de "formas possíveis de escrever um diagrama" é restringido à sintaxe válida documentada.

## Arquivos .mmd

Diagramas são salvos como `.mmd` em `diagrams/`. O formato é texto puro — o código mermaid sem fences. Acessíveis via `diagrams://{filename}` (resource) ou `get_diagram(filename)` (tool).

Na POC, existem dois diagramas pré-salvos: `aws-deployment.mmd` e `secure-mcp-platform.mmd` — que documentam a [[Arquitetura de Produção]].

---

Relaciona-se com: [[system-design]], [[Scoring de Diagramas]], [[Ontologia como Código]], [[Tool como Bias]], [[Contexto Programático]], [[Redução de Espaço na Prática]], [[Arquitetura de Produção]]
