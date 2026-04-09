# Backpropagation

O processo de propagar o erro medido pela [[Loss Function]] de volta pela [[Rede Neural]], calculando o gradiente de cada peso para saber como ajustá-lo.

---

## Definição

Backpropagation (propagação reversa) usa a regra da cadeia do cálculo diferencial para computar a derivada parcial da loss em relação a cada peso da rede. Essas derivadas (gradientes) indicam a direção e magnitude do ajuste necessário.

## O Brute-Force Inteligente

Na tese: "abrir uma rede neural e ir buscando padrões no modo brute-force." Backpropagation é o que torna esse brute-force inteligente — em vez de testar combinações aleatórias, ele calcula exatamente em qual direção cada peso deve mudar para reduzir o erro.

O [[Forward Pass]] testa. A [[Loss Function]] mede. O Backpropagation calcula a direção. O [[Gradient Descent]] executa o ajuste. Repete até [[Convergência]].

## Cálculo Diferencial

Backpropagation é fundamentalmente cálculo diferencial — derivadas parciais compostas pela regra da cadeia. Para cada peso w: ∂Loss/∂w = ∂Loss/∂output × ∂output/∂w.

Cada camada propaga o gradiente para a camada anterior, multiplicando pelas derivadas locais. É por isso que redes muito profundas podem ter problemas de "vanishing gradients" — as derivadas se multiplicam e ficam muito pequenas.

---

Relaciona-se com: [[Loss Function]], [[Gradient Descent]], [[Forward Pass]], [[Rede Neural]], [[Convergência]]
