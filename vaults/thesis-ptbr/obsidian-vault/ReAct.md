# ReAct

Loop de pensamento do [[Agente]]: Reason → Act → Observe. Repete até o objetivo ser atingido.

---

## Definição

ReAct (Reasoning + Acting) é um paradigma onde o modelo alterna entre raciocínio (pensar sobre o que fazer) e ação (executar uma [[Tool]]). Após cada ação, o modelo observa o resultado e incorpora como novo [[Contexto]].

## O Ciclo

1. **Reason (Razão)**: navega no [[Espaço Amostral]] e projeta — "para garantir isso, preciso da spec"
2. **Act (Ação)**: chama uma [[Tool]]/[[MCP]] para buscar dados
3. **Observe (Observação)**: recebe o resultado como novo [[Contexto]] e reinicia o ciclo

Cada ciclo enriquece o contexto. É o Feedback Loop Determinístico em ação — cada iteração aproxima o [[Agente]] do [[Determinismo]].

## Relação com a Tese

ReAct é o mecanismo prático da [[Tautologia Ontológica]]. A cada ciclo, o agente acumula mais [[Contexto]] (razão → observação), reduz o [[Espaço Amostral]], e se aproxima da resposta [[Tautologia|tautológica]].

Com [[RAG]] no loop, o agente também consulta decisões passadas — acumulação de conhecimento estruturado conforme descrito no artigo [[Ultra-Long-Horizon Agentic Science]].

---

Relaciona-se com: [[Agente]], [[Tool]], [[MCP]], [[Contexto]], [[Espaço Amostral]], [[Determinismo]], [[RAG]], [[Ultra-Long-Horizon Agentic Science]]
