# Orquestrador

Motor de planejamento que transforma objetivos em sequências de tools. Dado um goal em linguagem natural, o orquestrador mapeia para uma chain pré-definida de passos que qualquer cliente MCP pode seguir. Zero LLM na seleção da chain — é pattern matching determinístico.

---

## Por que Existe

Workflows multi-step são frágeis quando o agente decide a ordem. "Melhore este código" pode significar: rodar testes primeiro? Melhorar direto? Verificar testes depois? O orquestrador codifica a sequência correta — o agente executa, não inventa.

Isso é [[Enforcement Arquitetural]] aplicado a workflows: a chain define o espaço de ações possíveis, não o agente.

## 6 Chains

| Chain | Triggers | Passos | O que faz |
|-------|----------|--------|-----------|
| `tdd_improve` | improve, refactor, tdd | 7 | tdd → escrever testes → green → improve_code → aplicar → green → issue |
| `full_improvement` | full improve, full cycle | 9 | TDD completo + improve + verificar + checar knowledge gaps |
| `research` | research, docs | 3 | rank_urls → filtrar 60+ → research_topic |
| `prompt_lifecycle` | prompt, generate prompt | 4 | generate → audit → se <7 → refine |
| `code_to_knowledge` | enrich, knowledge gap | 4 | improve_code → encontrar gaps → retrieve → expand |
| `sync_and_audit` | sync, vault, audit | 4 | sync_vaults → audit_code → review → self_improve |

## Como Funciona

1. `orchestrate(goal)` recebe o objetivo em texto
2. Busca em [[Milvus]] por prior art (planos anteriores similares)
3. Faz pattern matching dos triggers contra o goal
4. Retorna a chain como plano estruturado: lista de steps com tool name, parâmetros, e instruções
5. O cliente MCP executa step-by-step

O orquestrador **planeja**, não **executa**. É LLM-agnostic — qualquer cliente pode seguir o plano.

## Tautologia no Orchestrador

Cada chain é um [[Tool Tautológica|tool tautológico]] de alto nível: dado um goal que matcha um trigger, a sequência de passos é determinística. Não há ambiguidade sobre qual tool chamar em qual ordem. O espaço de possibilidades é reduzido de "qualquer combinação de 44 tools" para "esta sequência específica de N steps."

## Prior Art via Milvus

Antes de selecionar uma chain, o orquestrador busca planos anteriores similares em Milvus (`refine_plan`). Se um plano existente é encontrado, ele é contrastado contra o novo goal — refinamento tautológico em vez de geração do zero.

---

Relaciona-se com: [[Marvin]], [[Enforcement Arquitetural]], [[Tool Tautológica]], [[Milvus]], [[Loop de Auto-Melhoria]]
