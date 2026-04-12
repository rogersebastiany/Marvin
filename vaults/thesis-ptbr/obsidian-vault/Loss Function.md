# Loss Function

Função que mede o erro entre o output do modelo e o resultado esperado. O objetivo de todo treinamento é minimizar a loss — fazê-la [[Convergência|convergir]] para um mínimo.

---

## Definição

A loss function (ou função de perda/custo) quantifica "quão errado" o modelo está. Exemplos comuns: Mean Squared Error (MSE), Cross-Entropy Loss, Binary Cross-Entropy.

Para LLMs, a loss típica é Cross-Entropy — mede a divergência entre a distribuição de probabilidade prevista pelo modelo e a distribuição real (o token correto).

## No Treinamento

O ciclo: [[Forward Pass]] produz output → loss function mede o erro → [[Backpropagation]] propaga o erro → [[Gradient Descent]] ajusta pesos → repete.

A loss deve [[Convergência|convergir]] (diminuir) ao longo das iterações. Se [[Divergência|diverge]] (aumenta), o treinamento está falhando.

## Relação com a Tese

[[Ontologia]] completa é como dar à loss function um alvo claro. Quando o [[Contexto]] define precisamente o que é "correto", a loss converge mais rápido e mais estavelmente. Sem ontologia, o alvo é ambíguo — a loss oscila.

---

Relaciona-se com: [[Convergência]], [[Divergência]], [[Backpropagation]], [[Gradient Descent]], [[Forward Pass]], [[Rede Neural]], [[Ontologia]]
