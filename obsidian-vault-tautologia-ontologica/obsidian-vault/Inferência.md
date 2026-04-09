# Inferência

O processo pelo qual o modelo produz uma resposta a partir de um input. Em LLMs, é probabilística — calcula distribuições e amostra tokens.

---

## Definição

Inferência é a fase de uso do modelo já treinado ([[Matriz M]] congelada). O input passa por um [[Forward Pass]] e o modelo produz o output, token por token, baseado nas probabilidades calculadas.

## Inferência Probabilística vs Dedução

Inferência em LLMs é inerentemente probabilística — o modelo calcula P(token|contexto) e escolhe (ou amostra) o mais provável. Isso introduz variabilidade ([[Drift]]).

[[Dedução]] é determinística — a conclusão é necessária dado as premissas. Na tese [[Tautologia Ontológica]], [[Contexto]] completo transforma inferência probabilística em algo que se aproxima de dedução: quando P(token correto|contexto) → 1, a "escolha" probabilística tem apenas um candidato viável.

---

Relaciona-se com: [[Dedução]], [[Forward Pass]], [[Matriz M]], [[Contexto]], [[Drift]], [[Determinismo]], [[Probabilidade Condicional]]
