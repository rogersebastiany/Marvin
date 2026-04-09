# Matrix M

The mathematical structure resulting from training an LLM model. Contains all of the model's "intelligence" in the form of numbers -- weights, biases, embeddings -- organized in vectors and matrices.

---

## Definition

M is composed of m row [[Vector|vectors]] (in R^n) or n column vectors (R^m). Each vector represents a dimension of the knowledge learned during training. The set of all vectors in M forms the [[Sample Space]] S.

In concrete terms: a model like GPT-4 or Claude has billions of parameters. These parameters are numbers organized in matrices -- attention layer weights, token embeddings, query/key/value projections. Matrix M is the abstraction that encompasses all these matrices as a single mathematical object.

## The Matrix as Knowledge

The numbers in Matrix M do not need to make sense individually to a human. A weight of 0.0342 in a specific layer has no isolated meaning. But these numbers make sense among themselves -- their relationships encode patterns of language, reasoning, facts, and associations learned during training.

"AI is a model, a program, a representation of a gigantic vector space full of strange numbers -- and these numbers don't need to make sense to you, but they make sense among themselves."

## Relationship with Context

[[Context]] (prompt) selects a [[Subset]] of [[Vector|vectors]] within M that are relevant to the task. The model does not use all of Matrix M for each response -- it activates specific regions, guided by the input.

In [[Linear Algebra]]: the prompt is a projection operation that maps the complete space M to a relevant subspace. The more precise the prompt, the more precise the projection, the smaller the subspace, the greater the [[Determinism]].

## Training and Neural Network

Matrix M is produced by training the [[Neural Network]]. The process of [[Backpropagation]] + [[Gradient Descent]] iteratively adjusts the values of M to minimize the [[Loss Function]]. When training [[Convergence|converges]], M represents an optimized approximation of the patterns in the training data.

After training, M is fixed (frozen). What changes between interactions is the [[Context]] -- which determines how M is queried.

---

Related to: [[Sample Space]], [[Vector]], [[Linear Algebra]], [[Embedding]], [[Context]], [[Neural Network]], [[Backpropagation]], [[Determinism]]
