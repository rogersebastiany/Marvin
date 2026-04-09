# Non-Linear Relationship

An unpredictable relationship between [[Vetor|vectors]] where the pattern is not obvious. At times it [[Convergência|converges]], at others it [[Divergência|diverges]].

---

## Example

`[1,5,45,123,890,11448,102332,1233872...]`
`[1,5,45,123,11449,102333,1233872...]`

"A relationship like this is clearly non-linear. 'To the naked eye,' at times it converges, at others it diverges."

## How the Neural Network Solves It

"If I want to stress-test this relationship, I can open a [[Rede Neural]] and search for patterns in brute-force mode, opening a tree to stress-test possibilities until it makes some sense, at least for part of the [[Conjunto]], which is when the vectors converge."

The network needs more neurons, more layers, more [[Activation Function|activations]] to model non-linear relationships. Each neuron tests a different condition -- a flag/boolean at the position of a certain number in the mapping of possible numbers that is the neural network.

## Discontinuities

"The number 0 is not in the domain of the relationship. Then there would be a division in the neural network." -- When the domain has discontinuities, the network needs additional [[Decision Boundary|decision boundaries]] to model these "divisions."

## In the Thesis

Without [[Contexto]], every problem is non-linear for the model -- many possibilities, hidden pattern, brute-force needed. With complete [[Ontologia]], the problem becomes quasi-[[Relação Linear|linear]] -- the pattern emerges naturally from the restricted [[Subconjunto]].

---

Related to: [[Relação Linear]], [[Convergência]], [[Divergência]], [[Rede Neural]], [[Activation Function]], [[Decision Boundary]], [[Contexto]], [[Ontologia]]
