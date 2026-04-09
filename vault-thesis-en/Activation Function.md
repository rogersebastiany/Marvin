# Activation Function

The neuron's "boolean." A function that decides whether a neuron fires or not, based on the weighted sum of its inputs.

---

## Definition

An activation function f takes the result of the linear transformation (W . x + b) and applies a non-linearity. Without it, stacked layers would be equivalent to a single linear transformation -- the network could not learn complex patterns.

## ReLU -- The Sophisticated Boolean

ReLU (Rectified Linear Unit): f(x) = max(0, x)

If the value is positive, it passes through. If negative, it becomes zero. It is the most widely used boolean in modern neural networks.

In the thesis: "flag with a boolean when you find something" -- the neuron with ReLU does exactly this. Found a pattern (positive value) -> fires (passes the value). Did not find one (negative value) -> does not fire (zero).

## Other Activation Functions

- **Sigmoid**: f(x) = 1/(1+e^(-x)) -- output between 0 and 1, useful for probabilities
- **Tanh**: f(x) = (e^x - e^(-x))/(e^x + e^(-x)) -- output between -1 and 1
- **Softmax**: normalizes a vector of values into a probability distribution -- used in the final layer of LLMs to choose the next token

## Relationship with Decision Boundary

The activation function creates [[Decision Boundary|decision boundaries]]. Where the function transitions from "not active" to "active" is the boundary. When the domain has discontinuities (like the 0 that does not belong to the odd/even relation), the network needs more neurons with more activations to model these boundaries.

---

Related to: [[Decision Boundary]], [[Rede Neural]], [[Bias]], [[Relação Não-Linear]], [[Relação Linear]]
