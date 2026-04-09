# Probabilidade Condicional

P(token|contexto) em vez de P(token). A probabilidade de um evento dado que outro evento já ocorreu. É a formalização matemática de por que [[Contexto]] rico funciona.

---

## Definição

P(A|B) = P(A ∩ B) / P(B)

A probabilidade de A dado B é a probabilidade da interseção de A e B dividida pela probabilidade de B. O evento B "restringe" o [[Espaço Amostral]] — só consideramos os resultados onde B é verdadeiro.

## Aplicação em LLMs

Sem [[Contexto]]: o modelo calcula P(token) no [[Espaço Amostral]] S inteiro. Muitos candidatos, alta incerteza, risco de [[Drift]].

Com contexto: o modelo calcula P(token|contexto) no [[Subconjunto]] A ⊂ S. Poucos candidatos, alta certeza, tendência ao [[Determinismo]].

O contexto B funciona como o "evento dado" — ele elimina regiões inteiras de S da consideração. O modelo não precisa avaliar tokens irrelevantes — o condicionamento já os excluiu.

## Redução Progressiva

Cada camada de [[Contexto]] é um condicionamento adicional:

P(token|prompt) — primeira restrição
P(token|prompt, tool) — segunda restrição
P(token|prompt, tool, spec) — terceira restrição
P(token|prompt, tool, spec, ADR, logs...) — [[Ontologia]] completa

Cada condicionamento reduz o espaço efetivo. É o mecanismo formal da [[Redução de Dimensionalidade]].

Quando o condicionamento é total (ontologia completa), P(token correto|contexto) → 1. Isso é [[Tautologia]].

---

Relaciona-se com: [[Espaço Amostral]], [[Contexto]], [[Redução de Dimensionalidade]], [[Determinismo]], [[Tautologia]], [[Drift]], [[Teoria dos Conjuntos]], [[Subconjunto]]
