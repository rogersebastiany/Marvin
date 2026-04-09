# Forward Pass

The passage of input through the [[Neural Network]] to produce an output. Each neuron applies its [[Activation Function]] and the signal propagates forward, layer by layer.

---

## Definition

In the forward pass, the input enters through the first layer, is multiplied by the weights, added to the [[Bias]], passes through the [[Activation Function]], and the result feeds the next layer. This repeats until the output layer produces the final prediction.

It is the "test" phase -- the network produces a response with its current weights. The [[Loss Function]] then measures whether the response is correct.

## In the Training Cycle

Forward pass -> Loss -> [[Backpropagation]] -> [[Gradient Descent]] -> Forward pass again.

The forward pass is the "boolean" in action -- each neuron fires or not, each layer filters and transforms, until the output emerges.

## In Inference

When the model is already trained ([[Matrix M]] frozen), each interaction with the user is a forward pass. The [[Context]] enters, propagates through the layers, and the output (next token) emerges. Repeats token by token until the response is complete.

---

Related to: [[Neural Network]], [[Activation Function]], [[Bias]], [[Loss Function]], [[Backpropagation]], [[Matrix M]]
