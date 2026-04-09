# Anti-Alucinação

O conjunto de mecanismos na POC que previnem [[Alucinação]] — o modelo operar fora do [[Subconjunto]] definido pelo [[Contexto Programático|contexto]], produzindo respostas inventadas.

---

## O Problema

Sem [[Ontologia como Código|ontologia]], o modelo opera no [[Espaço Amostral]] S inteiro. A probabilidade de produzir uma resposta factualmente correta é baixa — está na zona S \ A, o complemento do [[Contexto]].

"Se você exigir algo que não foi mapeado previamente, ele vai halucinar, e isso é 100% das vezes."

## Mecanismos na POC

**1. Tools como delimitadores**
Cada [[Primitivas MCP|tool]] restringe o que o agente pode fazer. `search_docs` só busca em `docs/`. `get_diagram` só lê de `diagrams/`. O agente não precisa inventar — tem ferramentas concretas para acessar conhecimento verificado.

**2. O [[Feedback Loop Determinístico]]**
Se a informação não existe localmente, o agente não precisa inventar — pode buscar via [[web-to-docs]]. O caminho "não encontrou → `crawl_docs` → salvou → agora encontra" transforma alucinação potencial em conhecimento verificado.

**3. O framework [[Transformer-Driven Prompt Architect]]**
A seção 5 — "ATTENTION MASK (CONSTRAINTS)" — é um "DO NOT" list explícito. Cada prompt gerado pelo [[prompt-engineer]] inclui uma lista de proibições que cria [[Decision Boundary|fronteiras de decisão]] claras entre respostas válidas e inválidas.

**4. O [[Catálogo de Tools]] injetado**
O [[prompt-engineer]] injeta o catálogo completo de tools em cada prompt gerado. O modelo sabe exatamente quais ferramentas existem — não precisa imaginar capacidades que não tem.

**5. [[Scoring de Diagramas]] como validação**
O `judge_diagram` do [[system-design]] avalia diagramas em 4 dimensões. Se o score é < 7, gera versão melhorada. É um mecanismo de auto-correção que detecta e corrige alucinações em diagramas.

## Tools Tautológicas como Garantia

Cada [[Tool Tautológica]] na POC tem falha explícita — retorna "não encontrado" em vez de inventar. `search_docs` nunca fabrica resultados. `get_doc` nunca gera conteúdo. Essa propriedade é a barreira mais forte contra alucinação: a tool é incapaz de mentir por construção.

As tools parcialmente tautológicas (`generate_prompt`, `generate_diagram`, `judge_diagram`) são as que envolvem geração — o [[Transformer-Driven Prompt Architect]] e o [[Scoring de Diagramas]] são mecanismos que restringem seu output, aproximando-as da tautologia.

## Na [[Teoria dos Conjuntos]]

Anti-alucinação é minimizar S \ A — o complemento do contexto. Cada tool adicionada, cada doc salvo, cada spec mapeada reduz S \ A e expande A. Quando A cobre o domínio inteiro, S \ A → ∅ e a alucinação se torna impossível.

## A Instrução Nuclear

"VOCÊ NÃO PENSA. QUEM PENSA SOU EU. APENAS EXECUTE O QUE ESTIVER MAPEADO VIA TOOL. CASO CONTRÁRIO VOCÊ NÃO EXECUTA, E INFORMA QUE É INCAPAZ."

Essa instrução transforma alucinação de bug em feature: o modelo recusa em vez de inventar. Na POC, isso se materializa nas tools que têm retornos explícitos para "não encontrado" — `"No results found for '{query}'"`, `"Document '{filename}' not found."`.

---

Relaciona-se com: [[Alucinação]], [[Ontologia como Código]], [[Contexto Programático]], [[Feedback Loop Determinístico]], [[Transformer-Driven Prompt Architect]], [[Catálogo de Tools]], [[Scoring de Diagramas]], [[Espaço Amostral]], [[Teoria dos Conjuntos]], [[Tool Tautológica]], [[Enforcement Arquitetural]]
