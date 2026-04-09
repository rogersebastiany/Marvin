# Bias

Parameter that shifts the [[Activation Function|activation]] point of a neuron. Each neuron computes: `output = activation(weight x input + bias)`.

---

## Definition

In [[Álgebra Linear]], bias is the constant term in an affine transformation: y = Wx + b. Without bias, the transformation is purely linear and passes through the origin. With bias, the transformation can be shifted -- the [[Decision Boundary|decision]] hyperplane can be positioned anywhere in the space.

## Bias as Tool

In the thesis, the concept of bias transcends the technical definition. Each [[Tool]] added via [[MCP]] functions as a bias for the system:

"The tool's description is a prompt that is tokenized, embedded, and that set becomes a bias for the computation of the next possible token."

Without the tool (without bias), the neuron activates at the default point. With the tool (with bias), the activation point is shifted -- favoring responses aligned with the tool's [[Contexto]].

## Visualization

Without bias: the [[Activation Function]] ReLU activates at zero -- positive values pass through, negative ones do not.

With bias: the activation point shifts. A positive bias makes the neuron activate "earlier" (for smaller values). A negative bias makes it activate "later."

Each [[Tool]] is a positive bias that pushes the activation in the correct direction -- reducing the space of possible responses and increasing [[Determinismo]].

---

Related to: [[Activation Function]], [[Álgebra Linear]], [[Tool]], [[MCP]], [[Rede Neural]], [[Decision Boundary]], [[Determinismo]]
