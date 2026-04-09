# Alucinação

Ocorre quando o modelo produz respostas fora do domínio definido pelo [[Contexto]]. O modelo opera no complemento S \ A do [[Espaço Amostral]] — a zona não mapeada pela [[Ontologia]].

---

## Definição

Em LLMs, alucinação é a geração de conteúdo que parece plausível mas é factualmente incorreto, inventado, ou inconsistente com o domínio.

"Se você exigir algo que não foi mapeado previamente, ele vai halucinar, e isso é 100% das vezes."

## Causa

Alucinação não é um bug — é a consequência lógica de operar sem [[Contexto]] suficiente. Na [[Teoria dos Conjuntos]], o modelo está operando em S \ A (complemento) — a região do [[Espaço Amostral]] não coberta pelo contexto.

Sem [[Tool|tools]], sem specs, sem [[Ontologia]] — o modelo infere a partir do espaço inteiro, e a probabilidade de acertar é baixa.

## Prevenção

A prevenção é a própria tese: construir [[Ontologia]] completa via [[Contexto]] rico. Cada camada adicionada (spec, BDD, TDD, ADR, observabilidade, [[RAG]]) reduz a zona de complemento e consequentemente reduz a probabilidade de alucinação.

"VOCÊ NÃO PENSA. QUEM PENSA SOU EU. APENAS EXECUTE O QUE ESTIVER MAPEADO VIA TOOL. CASO CONTRÁRIO VOCÊ NÃO EXECUTA, E INFORMA QUE É INCAPAZ." — Essa instrução transforma alucinação de bug em feature: o modelo recusa em vez de inventar.

---

Relaciona-se com: [[Contexto]], [[Ontologia]], [[Espaço Amostral]], [[Teoria dos Conjuntos]], [[Tool]], [[Drift]], [[RAG]]
