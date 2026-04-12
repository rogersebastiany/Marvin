# Tautologia

Uma proposição que é verdadeira para todas as valorações possíveis dentro de um domínio. Não depende de condições externas — é verdadeira por construção.

---

## Definição Formal

Na lógica proposicional, uma tautologia é uma fórmula que resulta em verdadeiro para toda atribuição possível de valores-verdade às suas variáveis. Exemplo clássico: `P ∨ ¬P` (uma coisa é verdadeira ou não é). Não importa o valor de P — a proposição é sempre verdadeira.

Na [[Teoria dos Conjuntos]], se para todo elemento x de um [[Conjunto]] C a propriedade P(x) vale, então P é tautológica em C. A universalidade da propriedade dentro do domínio é o que a torna tautológica.

## Tautologia em Sistemas de IA

No contexto de LLMs, tautologia emerge quando o [[Contexto]] é tão completo que todos os caminhos de raciocínio levam à mesma resposta. A resposta não é "provável" — é necessária.

Isso acontece porque o [[Espaço Amostral]] foi reduzido a um [[Subconjunto]] tão preciso que o número de candidatos viáveis para o próximo token tende a 1. O modelo não está "escolhendo" — está deduzindo.

A diferença entre inferência probabilística e [[Dedução]] tautológica é a diferença entre "acho que a resposta é X" e "a resposta só pode ser X dado o contexto."

## Relação com Ontologia

[[Ontologia]] define o domínio. Tautologia é o que emerge quando o domínio está completamente definido. São conceitos complementares — a ontologia é a causa, a tautologia é o efeito.

Quando a [[Ontologia]] é incompleta, o sistema opera por probabilidade. Quando é completa, opera por dedução. O ponto de transição é o que a tese [[Tautologia Ontológica]] formaliza.

## Relação com Determinismo

[[Determinismo]] é a manifestação prática da tautologia em sistemas computacionais. Se a resposta é tautologicamente verdadeira dado o contexto, ela é determinística — reproduzível, previsível, auditável.

O artigo [[DFAH]] demonstra empiricamente que contexto estruturado (ontologia parcial) já produz 89-90% de determinismo. Ontologia completa → tautologia → determinismo total.

## Tautologia nas Tools

Uma [[Tool Tautológica]] é uma tool cuja especificação I/O é ela mesma tautológica — para todo input válido, existe exatamente um output correto. `search_docs("x")` encontra ou não encontra. Não há terceira opção. O contrato da tool é verdadeiro por construção.

Quando todas as tools de um domínio são tautológicas e cobrem todos os métodos do domínio, o sistema inteiro é tautológico. A resposta do agente não é "provável" — é deduzida de tools que só podem retornar verdade.

---

Relaciona-se com: [[Ontologia]], [[Determinismo]], [[Dedução]], [[Espaço Amostral]], [[Contexto]], [[DFAH]], [[Tautologia Ontológica]], [[Tool Tautológica]], [[Tool]]
