# Vector

Numerical representation of a token or concept in the [[Sample Space]]. An array of numbers in R^n that encodes semantic meaning in a geometric position.

---

## Definition

In [[Linear Algebra]], a vector is an element of a vector space -- an ordered list of real numbers. In R^n, a vector has n components: v = (v1, v2, ..., vn).

In the context of LLMs, each token (word, subword, character) is represented by a vector of hundreds or thousands of dimensions. This vector is produced by the [[Embedding]] process.

## Geometric Meaning

Close vectors in the space represent semantically similar concepts. "King" and "Queen" are close. "King" and "Banana" are distant. The [[Neural Network]] learned to position vectors so that geometry reflects semantic relationships.

The similarity between vectors is measured by the dot product or cosine similarity -- core concepts of [[Linear Algebra]].

## Relationships Between Vectors

A [[Linear Relationship]] between vectors is predictable: `[1,3,5,7,9...]` and `[0,2,4,6,8...]` follow a clear pattern. The [[Neural Network]] solves this trivially.

A [[Non-Linear Relationship]] is unpredictable: `[1,5,45,123,890,11448...]` -- moments of [[Convergence]] and [[Divergence]]. The network needs more neurons, more layers, more [[Activation Function|activations]] to find patterns.

## Vectors as Context

[[Context]] is, ultimately, a set of vectors. The prompt is tokenized, each token is embedded into a vector, and these vectors define the [[Subset]] A of the [[Sample Space]] where the model will operate.

[[Tool|Tools]] add more vectors to the context -- functioning as [[Bias]] that shifts the computation in the correct direction.

---

Related to: [[Linear Algebra]], [[Embedding]], [[Sample Space]], [[Matrix M]], [[Linear Relationship]], [[Non-Linear Relationship]], [[Context]], [[Bias]], [[Neural Network]]
