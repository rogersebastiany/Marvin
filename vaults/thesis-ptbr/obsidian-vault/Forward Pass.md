# Forward Pass

A passagem do input pela [[Rede Neural]] para produzir um output. Cada neurônio aplica sua [[Activation Function]] e o sinal propaga adiante, camada por camada.

---

## Definição

No forward pass, o input entra pela primeira camada, é multiplicado pelos pesos, somado com o [[Bias]], passa pela [[Activation Function]], e o resultado alimenta a próxima camada. Repete até a camada de output produzir a previsão final.

É a fase de "teste" — a rede produz uma resposta com os pesos atuais. A [[Loss Function]] então mede se a resposta está correta.

## No Ciclo de Treinamento

Forward pass → Loss → [[Backpropagation]] → [[Gradient Descent]] → Forward pass novamente.

O forward pass é o "boolean" em ação — cada neurônio ativa ou não, cada camada filtra e transforma, até que emerge o output.

## Na Inferência

Quando o modelo já está treinado ([[Matriz M]] congelada), cada interação com o usuário é um forward pass. O [[Contexto]] entra, propaga pelas camadas, e o output (próximo token) emerge. Repete token por token até completar a resposta.

---

Relaciona-se com: [[Rede Neural]], [[Activation Function]], [[Bias]], [[Loss Function]], [[Backpropagation]], [[Matriz M]]
