# Backpropagation

The process of propagating the error measured by the [[Loss Function]] back through the [[Rede Neural]], computing the gradient of each weight to determine how to adjust it.

---

## Definition

Backpropagation (reverse propagation) uses the chain rule from differential calculus to compute the partial derivative of the loss with respect to each weight in the network. These derivatives (gradients) indicate the direction and magnitude of the necessary adjustment.

## The Intelligent Brute-Force

In the thesis: "open a neural network and search for patterns in brute-force mode." Backpropagation is what makes this brute-force intelligent -- instead of testing random combinations, it calculates exactly in which direction each weight must change to reduce the error.

The [[Forward Pass]] tests. The [[Loss Function]] measures. Backpropagation calculates the direction. [[Gradient Descent]] executes the adjustment. Repeat until [[Convergência]].

## Differential Calculus

Backpropagation is fundamentally differential calculus -- partial derivatives composed via the chain rule. For each weight w: dLoss/dw = dLoss/doutput x doutput/dw.

Each layer propagates the gradient to the previous layer, multiplying by local derivatives. This is why very deep networks can have "vanishing gradients" problems -- the derivatives multiply and become very small.

---

Related to: [[Loss Function]], [[Gradient Descent]], [[Forward Pass]], [[Rede Neural]], [[Convergência]]
