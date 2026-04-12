# Gradient Descent

O algoritmo que ajusta os pesos da [[Rede Neural]] na direção que reduz o erro. O gradiente é a derivada — indica "pra qual lado descer pra errar menos."

---

## Definição

Gradient Descent é um algoritmo de otimização iterativo. A cada passo, move os parâmetros na direção oposta ao gradiente da [[Loss Function]]: w = w - α × ∂Loss/∂w, onde α é o learning rate.

A analogia clássica: uma bola descendo uma montanha no escuro. O gradiente é a inclinação do terreno sob seus pés — indica qual direção é "para baixo." A bola dá um passo nessa direção, recalcula, e repete até chegar num vale (mínimo).

## Learning Rate

O learning rate α controla o tamanho do passo. Muito grande → a bola "pula" o vale e [[Divergência|diverge]]. Muito pequeno → a bola desce devagar demais. O valor ideal produz [[Convergência]] suave.

## Variantes

- **SGD (Stochastic)**: usa um subconjunto dos dados a cada passo — mais ruidoso, mais rápido
- **Mini-batch**: meio-termo entre SGD e batch completo
- **Adam**: adapta o learning rate por parâmetro — o mais usado na prática

## Na Tese

"Olhar pro vetor não-linear, chutar uma fórmula, ver que errou, e ajustar o chute na direção certa" — isso é gradient descent em linguagem natural. O gradiente é o guia que transforma brute-force em otimização direcionada.

---

Relaciona-se com: [[Backpropagation]], [[Loss Function]], [[Convergência]], [[Divergência]], [[Rede Neural]]
