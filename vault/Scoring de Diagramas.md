# Scoring de Diagramas

O framework de avaliação do [[system-design]]. `judge_diagram` avalia diagramas [[Mermaid.js]] em 4 dimensões com score 1-10 cada. Se o score overall é < 7, gera versão melhorada. É [[Anti-Alucinação]] aplicada a diagramas.

---

## As 4 Dimensões

**1. Syntax Correctness (Sintaxe)**
O código mermaid é válido? Renderiza sem erros? Node IDs, edge syntax, e keywords corretos?

Reduz: a dimensão "está sintaticamente correto?" do [[Espaço Amostral]]. O modelo recebe syntax refs completas como [[Contexto Programático|contexto]], então erros de sintaxe indicam que o contexto não foi seguido.

**2. Completeness (Completude)**
Todos os componentes e relações estão representados? Sistemas externos/atores são mostrados? Databases, queues, caches modelados explicitamente?

Reduz: a dimensão "está tudo mapeado?" — a [[Ontologia como Código|ontologia]] do diagrama está completa?

**3. Clarity & Readability (Clareza)**
Labels descritivos? Relações anotadas com protocolos? Layout direction apropriado? Subgraphs usados efetivamente? Um novo membro do time entenderia a arquitetura?

Reduz: a dimensão "é compreensível?" — a ontologia é acessível?

**4. Best Practices (Boas Práticas)**
Segue convenções de system design? Trust boundaries, async vs sync? Tipo de diagrama correto pro conteúdo? Focado (um concern por diagrama)?

Reduz: a dimensão "segue as regras do domínio?" — o diagrama está dentro do [[Subconjunto]] de práticas aceitas?

## Output Format

```
SYNTAX:         X/10 — [notes]
COMPLETENESS:   X/10 — [notes]
CLARITY:        X/10 — [notes]
BEST PRACTICES: X/10 — [notes]
OVERALL:        X/10
```

Seguido de: Issues (problemas específicos), Suggestions (melhorias concretas), Improved Version (diagrama corrigido).

## Auto-Correção

O prompt `review_architecture` implementa o loop: carrega diagrama → julga → se score < 7, gera versão melhorada e salva. É um [[Feedback Loop Determinístico]] dentro de um único server — iteração até [[Convergência]].

## Papel na Tese

O scoring transforma avaliação subjetiva ("esse diagrama é bom?") em avaliação objetiva (4 scores numéricos). É [[Determinismo Mensurável|determinismo]] na avaliação: dados os mesmos critérios e o mesmo diagrama, o score é reproduzível.

As 4 dimensões são 4 [[Decision Boundary|fronteiras de decisão]] — separam "diagrama aceitável" de "diagrama que precisa de melhoria." Cada dimensão com score < 7 é uma zona de [[Alucinação]] detectada e corrigida.

---

Relaciona-se com: [[system-design]], [[Mermaid.js]], [[Anti-Alucinação]], [[Determinismo Mensurável]], [[Feedback Loop Determinístico]], [[Ontologia como Código]], [[Contexto Programático]], [[Convergência]]
