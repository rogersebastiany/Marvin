# Rede Neural

Modelo computacional inspirado no cérebro biológico. Composta por camadas de neurônios artificiais que aprendem padrões nos dados através de treinamento iterativo.

---

## Definição

Uma rede neural é um grafo direcionado de neurônios organizados em camadas: input, hidden (uma ou mais), e output. Cada neurônio aplica uma transformação: `output = f(W · x + b)` onde W são pesos, x é input, b é [[Bias]], e f é a [[Activation Function]].

## O Insight Fundamental

"Se eu quiser estressar uma [[Relação Não-Linear]], eu posso abrir uma rede neural e ir buscando padrões no modo brute-force, abrindo uma árvore para estressar possibilidades até que faça algum sentido, pelo menos para parte do [[Conjunto]], que é quando os vetores [[Convergência|convergem]]. Essas possibilidades que me refiro são tipo neurônios, daí o nome, então são flags, booleans, guardados na posição de um certo número qualquer no mapeamento de possíveis números que é a rede neural."

Este insight captura a essência: a rede neural é um mapeamento de números possíveis, onde cada neurônio é um flag/boolean que ativa ou não para certos padrões. O treinamento é o brute-force inteligente que encontra quais flags devem ativar para quais inputs.

## Treinamento

O ciclo de aprendizado:
1. [[Forward Pass]] — testa o input, propaga pela rede
2. [[Loss Function]] — mede o erro entre output e resultado esperado
3. [[Backpropagation]] — propaga o erro de volta, calcula gradientes
4. [[Gradient Descent]] — ajusta os pesos na direção que reduz o erro
5. Repete até [[Convergência]]

O resultado do treinamento é a [[Matriz M]] — os pesos finais que codificam os padrões aprendidos.

## Relações Lineares vs Não-Lineares

Para [[Relação Linear|relações lineares]] (padrões óbvios como ímpares/pares), a rede converge trivialmente — poucos neurônios, poucas iterações.

Para [[Relação Não-Linear|relações não-lineares]] (padrões complexos que convergem e divergem), a rede precisa de mais camadas, mais neurônios, mais [[Activation Function|ativações]] — cada uma testando uma condição diferente via brute-force estruturado.

---

Relaciona-se com: [[Activation Function]], [[Bias]], [[Forward Pass]], [[Loss Function]], [[Backpropagation]], [[Gradient Descent]], [[Convergência]], [[Matriz M]], [[Relação Linear]], [[Relação Não-Linear]], [[Decision Boundary]]
