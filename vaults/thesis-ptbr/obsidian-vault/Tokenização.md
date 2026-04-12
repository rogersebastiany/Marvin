# Tokenização

Processo automático que quebra o input em chunks (tokens). É o primeiro passo antes do [[Embedding]].

---

## Definição

Tokenização divide texto em unidades menores — podem ser palavras, subpalavras, caracteres, ou combinações. Cada token recebe um ID numérico que o modelo usa internamente.

Exemplo: "Engenharia de Software" → ["Engen", "haria", " de", " Software"] (subword tokenization)

## No Pipeline

[[Tokenização]] → [[Embedding]] → [[Vetor|vetores]] no [[Espaço Amostral]] → cálculo → embedding reverso → tokenização reversa → output.

A qualidade da tokenização afeta o [[Contexto]]: tokens mais granulares capturam mais nuance, mas consomem mais da janela de contexto.

---

Relaciona-se com: [[Embedding]], [[Contexto]], [[Vetor]], [[Espaço Amostral]]
