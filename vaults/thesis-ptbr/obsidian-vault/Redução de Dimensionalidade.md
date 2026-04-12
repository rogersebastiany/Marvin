# Redução de Dimensionalidade

O efeito prático da [[Probabilidade Condicional]]: o [[Contexto]] reduz as dimensões efetivas do problema. O modelo opera num subespaço menor e mais preciso.

---

## Definição

Em matemática e machine learning, redução de dimensionalidade é o processo de reduzir o número de variáveis aleatórias sob consideração, obtendo um conjunto menor de variáveis principais.

No contexto da tese: o [[Espaço Amostral]] S opera em R^n com n na casa dos milhares. Cada [[Tool]], spec, ou [[Contexto]] adicional efetivamente elimina dimensões irrelevantes, projetando o problema para um subespaço de dimensão menor.

## Mecanismo

Cada peça de contexto é uma restrição dimensional:
- "O projeto usa Java 21" — elimina todas as dimensões relacionadas a outras linguagens
- "O banco é PostgreSQL" — elimina dimensões de MySQL, MongoDB, etc.
- "A API segue REST" — elimina dimensões de GraphQL, gRPC, etc.

Cumulativamente, essas restrições reduzem o espaço de possibilidades de bilhões para milhares, depois centenas, depois dezenas. Quando restam poucos candidatos viáveis, o [[Determinismo]] é natural.

## Relação com o Método

Cada componente do método contribui com redução dimensional:
- **Spec Driven Design**: restringe o comportamento esperado
- **BDD**: restringe os cenários válidos
- **TDD**: restringe a implementação correta
- **ADR**: restringe as decisões arquiteturais
- **Observabilidade**: restringe o estado real do sistema
- **[[RAG]]**: restringe com histórico de decisões passadas

O efeito cumulativo é a [[Ontologia]] completa — todas as dimensões irrelevantes eliminadas.

---

Relaciona-se com: [[Probabilidade Condicional]], [[Contexto]], [[Espaço Amostral]], [[Determinismo]], [[Ontologia]], [[Tool]], [[RAG]]
