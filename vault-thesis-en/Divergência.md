# Divergence

When a series, process, or system moves away from a stable value. The error oscillates or increases. The opposite of [[Convergência]].

---

## Definition

A series diverges if it does not tend to a finite limit. In optimization, divergence means the algorithm is moving away from the minimum -- the error grows instead of decreasing.

## In Neural Networks

The [[Loss Function]] diverges when training fails: learning rate too high, noisy data, inadequate architecture. The weights oscillate instead of converging.

## Relationship with Drift

Divergence in training is analogous to [[Drift]] in inference. Without rigid [[Contexto]], the model "diverges" -- producing responses increasingly distant from the correct result.

In the observation about [[Vetor|non-linear vectors]]: "at times it converges, at others it diverges" -- the network needs more structure (more layers, more neurons, better [[Activation Function]]) to resolve the divergent regions.

---

Related to: [[Convergência]], [[Drift]], [[Loss Function]], [[Rede Neural]], [[Relação Não-Linear]]
