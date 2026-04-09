# Tokenization

An automatic process that breaks input into chunks (tokens). It is the first step before [[Embedding]].

---

## Definition

Tokenization divides text into smaller units -- which can be words, subwords, characters, or combinations. Each token receives a numeric ID that the model uses internally.

Example: "Software Engineering" -> ["Software", " Engine", "ering"] (subword tokenization)

## In the Pipeline

[[Tokenização]] -> [[Embedding]] -> [[Vetor|vectors]] in the [[Espaço Amostral]] -> computation -> reverse embedding -> reverse tokenization -> output.

The quality of tokenization affects [[Contexto]]: more granular tokens capture more nuance, but consume more of the context window.

---

Related to: [[Embedding]], [[Contexto]], [[Vetor]], [[Espaço Amostral]]
