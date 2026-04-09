# Linear Algebra

The field of mathematics that describes operations with [[Vetor|vectors]] and [[Matriz M|matrices]]. It is the actual mathematical foundation of AI -- there is no magic, there is linear algebra.

---

## Definition

Linear Algebra studies vector spaces and linear transformations between them. Core concepts: vectors, matrices, transformations, eigenvalues, dot product, norms, projections.

"When we create a rich and well-connected context, using known software engineering concepts and best practices, that is where we create the magic. Which is actually linear algebra."

## Concepts Applied in the Thesis

**Vector Space R^n**: the domain where [[Embedding|embeddings]] live. Each [[Vetor]] has n dimensions -- modern models use 768, 1024, or more dimensions.

**Linear Transformation**: a function that preserves addition and scalar multiplication. Maps vectors from one space to another. The layers of a [[Rede Neural]] apply linear transformations (multiplication by weight matrix) followed by non-linear [[Activation Function|activations]].

**Dot Product / Cosine Similarity**: how the model measures proximity between [[Vetor|vectors]]. Two vectors with high cosine similarity represent semantically close concepts. It is the central operation of the Transformer attention mechanism.

**Projection**: an operation that maps a vector to a subspace. [[Contexto]] works as a projection -- it projects the complete [[Espaço Amostral]] onto a relevant subspace.

## Bias as Linear Algebra

Each neuron computes: `output = activation(W . x + b)` where W is the weight matrix, x is the input, and b is the [[Bias]]. It is an affine transformation -- linear algebra with displacement.

When a [[Tool]] adds context, it is adding a component to the bias vector, shifting the computation in the correct direction. This is not a metaphor -- it is literally a linear algebra operation.

---

Related to: [[Vetor]], [[Matriz M]], [[Embedding]], [[Rede Neural]], [[Bias]], [[Activation Function]], [[Espaço Amostral]]
