# Deterministic Trajectory Optimization

Paper that reformulates deterministic optimal control as probabilistic inference, demonstrating guaranteed convergence of probabilistic policies to the deterministic optimal trajectory via Expectation-Maximization. The same pattern as the thesis applied to dynamical systems.

---

## Reference

**Deterministic Trajectory Optimization through Probabilistic Optimal Control**
Mohammad Mahmoudi Filabadi, Tom Lefebvre, Guillaume Crevecoeur -- Ghent University, Belgium
https://arxiv.org/abs/2407.13316

## Contribution

Reformulates the deterministic optimal control problem as a Maximum Likelihood Estimation (MLE) problem. Introduces latent optimality variables and uses EM to iteratively refine probabilistic policies until converging to the deterministic optimal policy.

## The Mechanism

1. **Starts probabilistic**: the initial policy is a distribution over possible actions (the complete [[Espaço Amostral]]).
2. **E-step**: Evaluates the current policy against the system model (the structured information).
3. **M-step**: Refines the policy by maximizing the ELBO (Evidence Lower BOund).
4. **Iterates**: At each iteration, the policy becomes less uncertain. The risk parameter gamma controls the speed of [[Convergência]].
5. **Converges**: EM guarantees monotonic improvement. The probabilistic policies converge to the deterministic optimal policy.

## Two Algorithms

- **SP-PDP** (Sigma-Point Probabilistic Dynamic Programming): Forward pass evaluates the policy, backward pass updates. Related to classic DDP.
- **SP-BSC** (Sigma-Point Bayesian Smoothing Control): Forward and backward passes happen simultaneously. Faster convergence.

Both use sigma-point methods (unscented transform) instead of gradients -- they work on non-linear systems without requiring differentiability.

## The Gamma Parameter

Gamma controls exploration vs exploitation:
- High gamma -> more exploratory policies (more probabilistic)
- Low gamma -> more deterministic policies
- gamma -> 0 -> policy converges to the deterministic optimum

This is analogous to temperature in LLMs: high T -> more variation ([[Drift]]), low T -> more [[Determinismo]]. The structure of [[Contexto]] is what makes low T work well instead of collapsing.

## Guaranteed Convergence

EM guarantees:
- Monotonic improvement of log-likelihood at each iteration
- A sequence of probabilistic policies that converges to the deterministic optimum
- Policy uncertainty scales with the degree of necessary exploration

Tested on inverted pendulum and cart-pole -- non-linear systems. SP-BSC achieves better overall performance.

## Connection to the Thesis

The concept is identical to [[Ontological Tautology]], only the domain and the computation change:

- **This paper**: dynamical system + model + EM -> deterministic trajectory
- **The thesis**: LLM + complete [[Ontologia]] + [[Tool|tools]] -> deterministic output

The pattern: structured information + iterative refinement -> [[Convergência]] to [[Determinismo]]. In the thesis, the "EM" is the [[Feedback Loop Determinístico]] -- each tool call cycle enriches the [[Contexto]], reduces the [[Espaço Amostral]], and brings the response closer to deterministic.

"THIS PAPER HERE SAYS THAT COMPLETE CONTEXT (ONTOLOGY) YOU CAN REACH 89% DETERMINISM, WITHOUT NEEDING TO COMPUTE THE BEST PATH IN THE CALCULATION THOSE PHYSICS NERDS ARE DOING OVER THERE." The thesis achieves determinism through the completeness of the [[Ontologia]], not through optimal computation -- but the convergent pattern is the same.

---

Related to: [[Determinismo]], [[Convergência]], [[Ontologia]], [[Ontological Tautology]], [[Espaço Amostral]], [[Drift]], [[Feedback Loop Determinístico]], [[Tool]]
