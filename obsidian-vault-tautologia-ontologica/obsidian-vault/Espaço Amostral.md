# Espaço Amostral

O [[Conjunto]] S que contém todos os [[Vetor|vetores]] da [[Matriz M]]. Representa a totalidade de possibilidades de resposta de um modelo de LLM.

---

## Definição

Em probabilidade, o espaço amostral é o conjunto de todos os resultados possíveis de um experimento. Para um LLM, o "experimento" é gerar o próximo token, e S contém todos os vetores que representam todos os tokens possíveis em todos os contextos possíveis.

S é vasto — modelos modernos operam em espaços de milhares de dimensões com vocabulários de centenas de milhares de tokens. Cada posição na sequência abre um novo espaço de possibilidades.

## Redução via Contexto

O [[Contexto]] define um [[Subconjunto]] A ⊂ S. Sem contexto, o modelo opera em S inteiro — máxima incerteza. Com contexto, opera em A — incerteza reduzida proporcionalmente à qualidade do contexto.

Na [[Probabilidade Condicional]]: P(token) em S é distribuída. P(token|contexto) em A é concentrada. [[Redução de Dimensionalidade]] é o nome formal desse efeito.

Quando A é tão preciso que |candidatos viáveis| → 1, temos [[Tautologia]]. O [[Determinismo]] emerge da redução extrema do espaço amostral.

## Zonas do Espaço

Na [[Teoria dos Conjuntos]]:
- **A** (subconjunto definido pelo contexto): zona de operação segura
- **S \ A** (complemento): zona de [[Alucinação]] — se o modelo opera aqui, produz respostas fora do domínio definido
- **A ∩ B** (interseção de contextos): refinamento adicional quando múltiplas [[Tool|tools]] contribuem com contexto

## Relação com Vetores

Cada ponto em S é um [[Vetor]] em R^n. Vetores próximos representam conceitos semanticamente similares — produzidos pelo [[Embedding]]. A geometria do espaço amostral (distâncias, clusters, fronteiras) é o que a [[Rede Neural]] aprendeu durante o treinamento.

---

Relaciona-se com: [[Conjunto]], [[Vetor]], [[Matriz M]], [[Contexto]], [[Subconjunto]], [[Probabilidade Condicional]], [[Redução de Dimensionalidade]], [[Tautologia]], [[Alucinação]], [[Teoria dos Conjuntos]]
