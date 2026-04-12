# LLM Output Drift

Artigo que define e analisa o fenômeno de [[Drift]] em LLMs — a variação de respostas mesmo com temperatura zero e input constante. Classifica modelos em três tiers de comportamento e revela que modelos maiores driftam mais.

---

## Referência

**LLM Output Drift: Cross-Provider Validation & Mitigation for Financial Workflows**
Raffi Khatchadourian, Rolando Franco — AI4F Workshop, ACM ICAIF '25 (Singapura, Nov. 2025)
https://arxiv.org/abs/2511.07585

## Contribuição

Explica por que, sem [[Contexto]] rígido, a IA varia respostas mesmo com temperatura zero. Define formalmente o drift e propõe estratégias de mitigação: validação cross-provider e contexto estruturado.

## Três Tiers de Drift

O artigo classifica modelos em três níveis de comportamento a T=0.0:

- **Tier 1** (pequenos, 7-8B parâmetros): 100% consistência. Perfeitamente determinísticos, mas acurácia limitada.
- **Tier 2** (médios, 20-70B): Alta consistência, bom equilíbrio entre determinismo e capacidade.
- **Tier 3** (grandes, 100B+, e.g. GPT-OSS-120B): Apenas 12.5% consistência. Mais parâmetros = mais [[Drift]].

Achado contra-intuitivo: modelos maiores driftam **mais**, não menos. A [[Matriz M]] maior tem mais [[Vetor|vetores]], o [[Espaço Amostral]] é maior, há mais candidatos próximos competindo.

## Sensibilidade por Tipo de Tarefa

Nem todas as tarefas driftam igual:

- **[[RAG]]**: Mais sensível a temperatura. Pequenas variações no contexto recuperado cascateam para respostas diferentes.
- **Sumarização**: Sensibilidade moderada.
- **Classificação**: Mais robusta. O espaço de saída é discreto e pequeno.

Isso importa: a busca em `docs/` na POC é uma tarefa RAG — exatamente a categoria de maior risco para drift. O [[Contexto]] estruturado via [[Tool|tools]] é a mitigação necessária.

## Validação Cross-Provider

O mesmo prompt em providers diferentes produz resultados diferentes. Porém, o **padrão de determinismo transfere**: se uma tarefa é determinística num provider, tende a ser determinística em outro. A estrutura do [[Contexto]] importa mais que o modelo.

Isso valida que o [[Agente]] pode ser agnóstico a ferramenta — o que importa é a qualidade da [[Ontologia]], não o provider.

## Framework de Mitigação

O artigo mapeia drift para frameworks regulatórios (SOC, MiFID II) e propõe mitigação em três camadas:
1. Validação cross-provider (testar o mesmo prompt em múltiplos modelos)
2. [[Contexto]] estruturado rígido (reduzir ambiguidade)
3. Harness de determinismo ([[DFAH]])

Na tese: [[Tool|tools]] via [[MCP]], specs, BDD, TDD, ADR, observabilidade. Cada camada adicionada é uma camada de redução do [[Espaço Amostral]].

## Na Tese

Este artigo fundamenta a relação inversa entre [[Contexto]] e [[Drift]]: contexto pobre → drift alto. Contexto rico ([[Ontologia]]) → drift baixo → [[Determinismo]].

Complementa o [[DFAH]]: enquanto o DFAH mostra o que acontece com contexto (89%+), este artigo mostra o que acontece sem — e por que.

---

Relaciona-se com: [[Drift]], [[Determinismo]], [[DFAH]], [[Contexto]], [[Ontologia]], [[Tautologia Ontológica]], [[Matriz M]], [[Espaço Amostral]], [[RAG]], [[MCP]], [[Agente]]
