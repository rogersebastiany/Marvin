# Decision Boundary

A fronteira que separa regiões diferentes no espaço de dados. Onde o modelo decide que um input pertence a uma classe ou outra.

---

## Definição

Em machine learning, a decision boundary é a superfície no espaço de features que separa classes. Pontos de um lado são classificados como classe A, do outro como classe B.

## O Insight: "Divisão na Rede Neural"

"A relação desses dois vetores está no domínio dos números inteiros positivos e é x=(x-1)+2. Porém o número 0 não está no domínio da relação. Aí haveria uma divisão na rede neural."

Quando o domínio tem descontinuidades (o 0 não pertence), a [[Rede Neural]] precisa aprender onde está essa fronteira. Cada descontinuidade requer neurônios adicionais com [[Activation Function|ativações]] específicas para modelar a separação.

## No Espaço Amostral

O [[Contexto]] cria uma decision boundary no [[Espaço Amostral]]:
- Dentro do [[Subconjunto]] A = relevante (ativa)
- Fora de A = irrelevante (não ativa)

Mais [[Tool|tools]] e specs criam fronteiras mais precisas — o modelo sabe exatamente onde está a linha entre resposta válida e [[Alucinação]].

---

Relaciona-se com: [[Activation Function]], [[Rede Neural]], [[Espaço Amostral]], [[Contexto]], [[Subconjunto]], [[Alucinação]]
