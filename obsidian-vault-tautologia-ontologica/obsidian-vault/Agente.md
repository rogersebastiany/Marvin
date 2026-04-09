# Agente

[[Contexto]] personificado com loop de pensamento [[ReAct]]. Recebe um papel e opera com [[Tool|tools]] disponíveis via [[MCP]].

---

## Definição

"O agente é a mesma coisa, contexto, mas ele tem um caráter humanizado. Ele personifica uma entidade. Você dá o papel a ele de Senior Software Engineer, QA, PM, etc. Tudo vai depender do quanto você consegue enriquecer o contexto desse agente."

Um agente é um LLM + system prompt (role) + tools + loop de execução. Não é um programa diferente — é o mesmo modelo operando com [[Contexto]] especializado e capacidade de ação.

## Loop ReAct

O agente opera num ciclo [[ReAct]]:
1. **Reason**: analisa a tarefa, projeta o plano
2. **Act**: invoca uma [[Tool]] via [[MCP]]
3. **Observe**: incorpora o resultado como novo contexto
4. Repete até o objetivo ser atingido

## AGI por Domínio

Com [[Ontologia]] completa de um domínio (todas as [[Tool|tools]] mapeando todo o conhecimento), um agente atinge [[Determinismo]] quase total naquele domínio. É AGI de domínio fechado — não é a AGI universal, mas é funcional, determinística, e replicável.

"VOCÊ NÃO PENSA. QUEM PENSA SOU EU. APENAS EXECUTE O QUE ESTIVER MAPEADO VIA TOOL." — Essa instrução transforma o agente de inferidor probabilístico para executor determinístico.

## Multi-Agentes

Múltiplos agentes, cada um com seu papel e [[Tool|tools]], colaborando. O sistema distribui responsabilidades e cada agente opera na sua zona de [[Ontologia]].

---

Relaciona-se com: [[ReAct]], [[MCP]], [[Tool]], [[Contexto]], [[Ontologia]], [[Determinismo]]
