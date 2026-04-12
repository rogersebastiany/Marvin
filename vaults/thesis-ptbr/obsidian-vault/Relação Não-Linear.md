# Relação Não-Linear

Relação imprevisível entre [[Vetor|vetores]] onde o padrão não é óbvio. Em momentos [[Convergência|converge]], em outros [[Divergência|diverge]].

---

## Exemplo

`[1,5,45,123,890,11448,102332,1233872...]`
`[1,5,45,123,11449,102333,1233872...]`

"Uma relação como essa é claramente não linear. 'A olho nu', em momentos ela converge, outros ela diverge."

## Como a Rede Neural Resolve

"Se eu quiser estressar essa relação, eu posso abrir uma [[Rede Neural]] e ir buscando padrões no modo brute-force, abrindo uma árvore para estressar possibilidades até que faça algum sentido, pelo menos para parte do [[Conjunto]], que é quando os vetores convergem."

A rede precisa de mais neurônios, mais camadas, mais [[Activation Function|ativações]] para modelar relações não-lineares. Cada neurônio testa uma condição diferente — um flag/boolean na posição de um certo número no mapeamento de possíveis números que é a rede neural.

## Descontinuidades

"O número 0 não está no domínio da relação. Aí haveria uma divisão na rede neural." — Quando o domínio tem descontinuidades, a rede precisa de [[Decision Boundary|fronteiras de decisão]] adicionais para modelar essas "divisões."

## Na Tese

Sem [[Contexto]], todo problema é não-linear para o modelo — muitas possibilidades, padrão escondido, brute-force necessário. Com [[Ontologia]] completa, o problema se torna quase-[[Relação Linear|linear]] — o padrão emerge naturalmente do [[Subconjunto]] restrito.

---

Relaciona-se com: [[Relação Linear]], [[Convergência]], [[Divergência]], [[Rede Neural]], [[Activation Function]], [[Decision Boundary]], [[Contexto]], [[Ontologia]]
