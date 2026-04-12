# Vetor

Representação numérica de um token ou conceito no [[Espaço Amostral]]. Um array de números em R^n que codifica significado semântico numa posição geométrica.

---

## Definição

Na [[Álgebra Linear]], um vetor é um elemento de um espaço vetorial — uma lista ordenada de números reais. Em R^n, um vetor tem n componentes: v = (v₁, v₂, ..., vₙ).

No contexto de LLMs, cada token (palavra, subpalavra, caractere) é representado por um vetor de centenas ou milhares de dimensões. Esse vetor é produzido pelo processo de [[Embedding]].

## Significado Geométrico

Vetores próximos no espaço representam conceitos semanticamente similares. "Rei" e "Rainha" estão próximos. "Rei" e "Banana" estão distantes. A [[Rede Neural]] aprendeu a posicionar os vetores de forma que a geometria reflita relações semânticas.

A similaridade entre vetores é medida pelo produto escalar ou similaridade por cosseno — conceitos centrais da [[Álgebra Linear]].

## Relações entre Vetores

Uma [[Relação Linear]] entre vetores é previsível: `[1,3,5,7,9...]` e `[0,2,4,6,8...]` seguem um padrão claro. A [[Rede Neural]] resolve isso trivialmente.

Uma [[Relação Não-Linear]] é imprevisível: `[1,5,45,123,890,11448...]` — momentos de [[Convergência]] e [[Divergência]]. A rede precisa de mais neurônios, mais camadas, mais [[Activation Function|ativações]] para encontrar padrões.

## Vetores como Contexto

O [[Contexto]] é, em última instância, um conjunto de vetores. O prompt é tokenizado, cada token é embeddado num vetor, e esses vetores definem o [[Subconjunto]] A do [[Espaço Amostral]] onde o modelo vai operar.

[[Tool|Tools]] adicionam mais vetores ao contexto — funcionando como [[Bias]] que desloca o cálculo na direção correta.

---

Relaciona-se com: [[Álgebra Linear]], [[Embedding]], [[Espaço Amostral]], [[Matriz M]], [[Relação Linear]], [[Relação Não-Linear]], [[Contexto]], [[Bias]], [[Rede Neural]]
