# Álgebra Linear

O campo da matemática que descreve operações com [[Vetor|vetores]] e [[Matriz M|matrizes]]. É a base matemática real da IA — não há magia, há álgebra linear.

---

## Definição

Álgebra Linear estuda espaços vetoriais e transformações lineares entre eles. Conceitos centrais: vetores, matrizes, transformações, autovalores, produto escalar, normas, projeções.

"Quando criamos um contexto rico e bem amarrado, utilizando conceitos e boas práticas conhecidos de engenharia de software, é aí que a gente cria a mágica. Que na verdade é álgebra linear."

## Conceitos Aplicados na Tese

**Espaço Vetorial R^n**: o domínio onde os [[Embedding|embeddings]] vivem. Cada [[Vetor]] tem n dimensões — modelos modernos usam 768, 1024, ou mais dimensões.

**Transformação Linear**: uma função que preserva adição e multiplicação escalar. Mapeia vetores de um espaço para outro. As camadas da [[Rede Neural]] aplicam transformações lineares (multiplicação por matriz de pesos) seguidas de [[Activation Function|ativações]] não-lineares.

**Produto Escalar / Similaridade por Cosseno**: como o modelo mede proximidade entre [[Vetor|vetores]]. Dois vetores com alta similaridade por cosseno representam conceitos semanticamente próximos. É a operação central do mecanismo de atenção (attention) dos Transformers.

**Projeção**: operação que mapeia um vetor para um subespaço. O [[Contexto]] funciona como uma projeção — projeta o [[Espaço Amostral]] completo num subespaço relevante.

## Bias como Álgebra Linear

Cada neurônio calcula: `output = activation(W · x + b)` onde W é a matriz de pesos, x é o input, e b é o [[Bias]]. É uma transformação afim — álgebra linear com deslocamento.

Quando uma [[Tool]] adiciona contexto, ela está adicionando um componente ao vetor de bias, deslocando o cálculo na direção correta. Não é metáfora — é literalmente uma operação de álgebra linear.

---

Relaciona-se com: [[Vetor]], [[Matriz M]], [[Embedding]], [[Rede Neural]], [[Bias]], [[Activation Function]], [[Espaço Amostral]]
