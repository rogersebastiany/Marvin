# Tool Tautológica

Uma tool cujo contrato de entrada/saída é completo e inequívoco — dado input válido, existe exatamente um output correto. A tool retorna a resposta certa ou informa que não pode responder. Não existe terceira opção.

---

## Na POC

| Tool | Tautológica? | Contrato |
|---|---|---|
| `search_docs(query)` | **Sim** | Busca substring → encontra ou "No results found" |
| `list_docs()` | **Sim** | Lista filesystem → retorno é o estado real |
| `get_doc(filename)` | **Sim** | Lê arquivo → conteúdo ou "not found" |
| `save_as_doc(url, filename)` | **Sim** | HTTP + salva → sucesso ou erro |
| `crawl_docs(url, max_pages)` | **Sim** | Crawl + salva → sucesso ou erro |
| `batch_convert(urls)` | **Sim** | Múltiplos HTTP + salva → sucesso parcial ou total |
| `save_diagram(code, filename)` | **Sim** | Escreve arquivo → sucesso ou erro |
| `get_diagram(filename)` | **Sim** | Lê arquivo → conteúdo ou "not found" |
| `list_diagrams()` | **Sim** | Lista filesystem → retorno é o estado real |
| `generate_prompt(...)` | **Parcial** | Framework de 6 seções restringe, mas output é gerado |
| `generate_diagram(...)` | **Parcial** | Syntax refs restringem, mas output é gerado |
| `judge_diagram(...)` | **Parcial** | Score numérico, mas julgamento envolve inferência |
| `refine_prompt(...)` | **Parcial** | Framework restringe, mas refinamento é gerado |

## Padrão: Read é Tautológico, Write é Parcial

Tools que **lêem** dados existentes (search, list, get) são tautológicas por natureza — o output é o dado real ou "não existe". Tools que **geram** conteúdo (generate, refine, judge) são parcialmente tautológicas — frameworks restringem o espaço de saída mas não o fecham completamente.

O [[Transformer-Driven Prompt Architect]] (6 seções mandatórias) e o [[Scoring de Diagramas]] (4 dimensões numéricas) são mecanismos que **aproximam** tools parciais da tautologia. Quanto mais restrito o framework, mais tautológica a tool.

## Por que Importa

O [[DFAH]] mostra correlação nula (r = -0.11) entre [[Determinismo]] e acurácia em agentes com tools genéricas. Mas com tools tautológicas, determinismo **implica** acurácia — a tool só pode retornar verdade ou "não sei".

Isso é a defesa da tese contra o achado mais provocativo do DFAH. O r = -0.11 mede o caso geral. A [[Tautologia Ontológica]] opera no caso onde tools são tautológicas e a [[Ontologia como Código|ontologia]] é completa.

## Completude = Cobertura

A [[Ontologia como Código|ontologia]] é completa quando todo método do domínio tem uma tool tautológica correspondente. Verificável:
1. Enumere métodos/processos do domínio
2. Cada um tem tool? → cobertura
3. Cada tool é tautológica? → qualidade

Se sim para todos → [[Tautologia]] por construção.

---

Relaciona-se com: [[Tool como Bias]], [[DFAH]], [[Determinismo Mensurável]], [[Anti-Alucinação]], [[Ontologia como Código]], [[Transformer-Driven Prompt Architect]], [[Scoring de Diagramas]], [[Tautologia Ontológica — Tese e Prova]], [[Catálogo de Tools]]
