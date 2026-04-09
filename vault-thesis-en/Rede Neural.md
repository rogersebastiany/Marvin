# Neural Network

A computational model inspired by the biological brain. Composed of layers of artificial neurons that learn patterns in data through iterative training.

---

## Definition

A neural network is a directed graph of neurons organized in layers: input, hidden (one or more), and output. Each neuron applies a transformation: `output = f(W . x + b)` where W is the weights, x is the input, b is the [[Bias]], and f is the [[Activation Function]].

## The Fundamental Insight

"If I want to stress-test a [[Relação Não-Linear]], I can open a neural network and search for patterns in brute-force mode, opening a tree to stress-test possibilities until it makes some sense, at least for part of the [[Conjunto]], which is when the vectors [[Convergência|converge]]. These possibilities I refer to are like neurons, hence the name, so they are flags, booleans, stored at the position of some number in the mapping of possible numbers that is the neural network."

This insight captures the essence: the neural network is a mapping of possible numbers, where each neuron is a flag/boolean that fires or not for certain patterns. Training is the intelligent brute-force that finds which flags should fire for which inputs.

## Training

The learning cycle:
1. [[Forward Pass]] -- tests the input, propagates through the network
2. [[Loss Function]] -- measures the error between output and expected result
3. [[Backpropagation]] -- propagates the error back, computes gradients
4. [[Gradient Descent]] -- adjusts the weights in the direction that reduces error
5. Repeats until [[Convergência]]

The result of training is the [[Matriz M]] -- the final weights that encode the learned patterns.

## Linear vs Non-Linear Relationships

For [[Relação Linear|linear relationships]] (obvious patterns like odd/even), the network converges trivially -- few neurons, few iterations.

For [[Relação Não-Linear|non-linear relationships]] (complex patterns that converge and diverge), the network needs more layers, more neurons, more [[Activation Function|activations]] -- each one testing a different condition via structured brute-force.

---

Related to: [[Activation Function]], [[Bias]], [[Forward Pass]], [[Loss Function]], [[Backpropagation]], [[Gradient Descent]], [[Convergência]], [[Matriz M]], [[Relação Linear]], [[Relação Não-Linear]], [[Decision Boundary]]
