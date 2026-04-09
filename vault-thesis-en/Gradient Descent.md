# Gradient Descent

The algorithm that adjusts the weights of the [[Rede Neural]] in the direction that reduces the error. The gradient is the derivative -- it indicates "which way to go down to make fewer mistakes."

---

## Definition

Gradient Descent is an iterative optimization algorithm. At each step, it moves the parameters in the opposite direction of the [[Loss Function]] gradient: w = w - alpha x dLoss/dw, where alpha is the learning rate.

The classic analogy: a ball rolling down a mountain in the dark. The gradient is the slope of the terrain under your feet -- it indicates which direction is "downhill." The ball takes a step in that direction, recalculates, and repeats until reaching a valley (minimum).

## Learning Rate

The learning rate alpha controls the step size. Too large -> the ball "jumps" over the valley and [[Divergência|diverges]]. Too small -> the ball descends too slowly. The ideal value produces smooth [[Convergência]].

## Variants

- **SGD (Stochastic)**: uses a subset of data at each step -- noisier, faster
- **Mini-batch**: middle ground between SGD and full batch
- **Adam**: adapts the learning rate per parameter -- the most widely used in practice

## In the Thesis

"Look at the non-linear vector, guess a formula, see that you were wrong, and adjust the guess in the right direction" -- this is gradient descent in natural language. The gradient is the guide that transforms brute-force into directed optimization.

---

Related to: [[Backpropagation]], [[Loss Function]], [[Convergência]], [[Divergência]], [[Rede Neural]]
