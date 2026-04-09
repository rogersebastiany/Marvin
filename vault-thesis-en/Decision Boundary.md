# Decision Boundary

The boundary that separates different regions in the data space. Where the model decides that an input belongs to one class or another.

---

## Definition

In machine learning, the decision boundary is the surface in feature space that separates classes. Points on one side are classified as class A, on the other as class B.

## The Insight: "Division in the Neural Network"

"The relationship between these two vectors is in the domain of positive integers and is x=(x-1)+2. However, the number 0 is not in the domain of the relationship. Then there would be a division in the neural network."

When the domain has discontinuities (0 does not belong), the [[Rede Neural]] needs to learn where this boundary is. Each discontinuity requires additional neurons with specific [[Activation Function|activations]] to model the separation.

## In the Sample Space

[[Contexto]] creates a decision boundary in the [[Espaço Amostral]]:
- Inside the [[Subconjunto]] A = relevant (active)
- Outside A = irrelevant (not active)

More [[Tool|tools]] and specs create more precise boundaries -- the model knows exactly where the line is between a valid response and [[Alucinação]].

---

Related to: [[Activation Function]], [[Rede Neural]], [[Espaço Amostral]], [[Contexto]], [[Subconjunto]], [[Alucinação]]
