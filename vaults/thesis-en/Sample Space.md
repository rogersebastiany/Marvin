# Sample Space

The [[Set]] S that contains all [[Vector|vectors]] of the [[Matrix M]]. Represents the totality of possible responses from an LLM model.

---

## Definition

In probability, the sample space is the set of all possible outcomes of an experiment. For an LLM, the "experiment" is generating the next token, and S contains all vectors representing all possible tokens in all possible contexts.

S is vast -- modern models operate in spaces of thousands of dimensions with vocabularies of hundreds of thousands of tokens. Each position in the sequence opens a new space of possibilities.

## Reduction via Context

[[Context]] defines a [[Subset]] A ⊂ S. Without context, the model operates in all of S -- maximum uncertainty. With context, it operates in A -- uncertainty reduced proportionally to the quality of the context.

In [[Conditional Probability]]: P(token) in S is distributed. P(token|context) in A is concentrated. [[Dimensionality Reduction]] is the formal name for this effect.

When A is so precise that |viable candidates| -> 1, we have [[Tautology]]. [[Determinism]] emerges from the extreme reduction of the sample space.

## Zones of the Space

In [[Set Theory]]:
- **A** (subset defined by context): safe operating zone
- **S \ A** (complement): [[Hallucination]] zone -- if the model operates here, it produces responses outside the defined domain
- **A intersection B** (intersection of contexts): additional refinement when multiple [[Tool|tools]] contribute context

## Relationship with Vectors

Each point in S is a [[Vector]] in R^n. Close vectors represent semantically similar concepts -- produced by [[Embedding]]. The geometry of the sample space (distances, clusters, boundaries) is what the [[Neural Network]] learned during training.

---

Related to: [[Set]], [[Vector]], [[Matrix M]], [[Context]], [[Subset]], [[Conditional Probability]], [[Dimensionality Reduction]], [[Tautology]], [[Hallucination]], [[Set Theory]]
