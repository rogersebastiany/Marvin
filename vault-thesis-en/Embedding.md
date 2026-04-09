# Embedding

The process of transforming tokens (text, audio, video) into numerical [[Vector|vectors]] in the [[Sample Space]]. The bridge between human language and [[Linear Algebra]].

---

## Definition

Embedding is the representation of discrete objects (words, tokens) as continuous vectors in R^n. The embedding model "knows" the [[Matrix M]] and positions each token at a point in vector space such that semantic relationships translate into geometric relationships.

## Process

1. [[Tokenization]] breaks the input into chunks (tokens)
2. Embedding transforms each token into a vector in R^n
3. The vectors are positioned in the [[Sample Space]]
4. The model operates on these vectors
5. The output vectors pass through reverse embedding
6. Output tokens are decoded back into text

"The resulting vectors transform into chunks, and finally into the expected output format, using the same embedding model. The reverse process basically."

## Properties

Close vectors = similar concepts. Cosine similarity ([[Linear Algebra]]) measures this proximity. This is what allows [[RAG]] to work -- vector similarity search finds semantically relevant content even without exact word matching.

---

Related to: [[Vector]], [[Tokenization]], [[Matrix M]], [[Sample Space]], [[Linear Algebra]], [[RAG]]
