# Loss Function

A function that measures the error between the model's output and the expected result. The goal of all training is to minimize the loss -- to make it [[Convergência|converge]] to a minimum.

---

## Definition

The loss function (or cost function) quantifies "how wrong" the model is. Common examples: Mean Squared Error (MSE), Cross-Entropy Loss, Binary Cross-Entropy.

For LLMs, the typical loss is Cross-Entropy -- it measures the divergence between the probability distribution predicted by the model and the actual distribution (the correct token).

## In Training

The cycle: [[Forward Pass]] produces output -> loss function measures the error -> [[Backpropagation]] propagates the error -> [[Gradient Descent]] adjusts weights -> repeat.

The loss should [[Convergência|converge]] (decrease) over iterations. If it [[Divergência|diverges]] (increases), training is failing.

## Relationship with the Thesis

Complete [[Ontologia]] is like giving the loss function a clear target. When [[Contexto]] precisely defines what is "correct," the loss converges faster and more stably. Without ontology, the target is ambiguous -- the loss oscillates.

---

Related to: [[Convergência]], [[Divergência]], [[Backpropagation]], [[Gradient Descent]], [[Forward Pass]], [[Rede Neural]], [[Ontologia]]
