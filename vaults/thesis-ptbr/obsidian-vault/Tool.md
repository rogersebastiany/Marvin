# Tool

Um [[Subconjunto]] de [[Vetor|vetores]] que funciona como [[Bias]] para o cálculo do próximo token. Qualquer fonte de [[Contexto]] estruturado que restringe o [[Espaço Amostral]].

---

## Definição

No contexto de LLMs e [[MCP]], uma tool é uma função ou recurso externo que o modelo pode invocar para obter informação. Documentação, APIs, specs, integrações.

"Uma tool nada mais é do que um subconjunto de vetores. A descrição da tool é um prompt que é tokenizado, embeddado, e esse conjunto vira um bias para o cálculo do próximo possível token."

## Como Tools Funcionam

A descrição da tool é processada da mesma forma que qualquer [[Contexto]]: [[Tokenização]] → [[Embedding]] → [[Vetor|vetores]] no [[Espaço Amostral]]. Esses vetores adicionais restringem o espaço de busca, funcionando como [[Bias]] que desloca a [[Activation Function|ativação]] na direção correta.

## Tools como Ontologia

Cada tool representa um pedaço da [[Ontologia]] do domínio. A tool de documentação da AWS SQS contém a ontologia de filas. A tool de specs do sistema contém a ontologia do comportamento esperado. Cumulativamente, todas as tools constroem a ontologia completa.

Tools são servidas via [[MCP]] para acesso O(1) — a porteira aberta entre o modelo e o contexto.

## Tool Tautológica

Uma [[Tool Tautológica]] é uma tool cujo contrato I/O é completo e inequívoco — dado input válido, existe exatamente um output correto. `search_docs` encontra ou não encontra. `get_doc` retorna o conteúdo ou "not found". Não há terceira opção.

Quando todas as tools de um domínio são tautológicas, [[Determinismo]] implica acurácia. A correlação nula (r = -0.11) do [[DFAH]] entre determinismo e acurácia se aplica a tools genéricas com output ambíguo — não a tools tautológicas.

---

Relaciona-se com: [[Bias]], [[Contexto]], [[MCP]], [[Subconjunto]], [[Vetor]], [[Ontologia]], [[Espaço Amostral]], [[Activation Function]], [[Tool Tautológica]], [[DFAH]]
