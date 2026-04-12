# Activation Function

O "boolean" do neurônio. Função que decide se um neurônio ativa ou não, baseado na soma ponderada de seus inputs.

---

## Definição

Uma activation function f recebe o resultado da transformação linear (W · x + b) e aplica uma não-linearidade. Sem ela, camadas empilhadas seriam equivalentes a uma única transformação linear — a rede não poderia aprender padrões complexos.

## ReLU — O Boolean Sofisticado

ReLU (Rectified Linear Unit): f(x) = max(0, x)

Se o valor é positivo, passa. Se é negativo, vira zero. É o boolean mais usado em redes neurais modernas.

Na tese: "marcar com boolean quando encontrar algo" — o neurônio com ReLU faz exatamente isso. Encontrou padrão (valor positivo) → ativa (passa o valor). Não encontrou (valor negativo) → não ativa (zero).

## Outras Activation Functions

- **Sigmoid**: f(x) = 1/(1+e^(-x)) — output entre 0 e 1, útil para probabilidades
- **Tanh**: f(x) = (e^x - e^(-x))/(e^x + e^(-x)) — output entre -1 e 1
- **Softmax**: normaliza um vetor de valores em distribuição de probabilidade — usada na camada final de LLMs para escolher o próximo token

## Relação com Decision Boundary

A activation function cria [[Decision Boundary|fronteiras de decisão]]. Onde a função transita de "não ativa" para "ativa" é a fronteira. Quando o domínio tem descontinuidades (como o 0 que não pertence à relação ímpares/pares), a rede precisa de mais neurônios com mais ativações para modelar essas fronteiras.

---

Relaciona-se com: [[Decision Boundary]], [[Rede Neural]], [[Bias]], [[Relação Não-Linear]], [[Relação Linear]]
