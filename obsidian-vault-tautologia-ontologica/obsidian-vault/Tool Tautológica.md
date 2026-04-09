# Tool Tautológica

Uma [[Tool]] cujo contrato de entrada/saída é completo e inequívoco. Dado um input válido, existe exatamente um output correto. A tool não pode retornar uma resposta errada — ela ou retorna a resposta certa ou informa que não pode responder.

---

## Definição

Uma tool é tautológica quando sua especificação (input types, output format, comportamento em edge cases) não deixa espaço para ambiguidade. O resultado é [[Determinismo|determinístico]] por construção — verdadeiro para todas as valorações possíveis dos inputs, como uma [[Tautologia]] lógica.

Exemplos:
- `search_docs("lambda")` → retorna linhas que contêm "lambda" ou "No results found". Não existe terceira opção.
- `get_doc("architecture.md")` → retorna o conteúdo do arquivo ou "Document not found". Não inventa conteúdo.
- `save_diagram(code, filename)` → salva o arquivo ou retorna erro. Não modifica o código.

Contra-exemplo: uma tool `answer_question(query)` que gera texto livre **não** é tautológica — o espaço de saída é aberto.

## Por que Importa

O [[DFAH]] revela que [[Determinismo]] e acurácia têm correlação nula (r = -0.11) em agentes com tools genéricas. Um sistema pode ser perfeitamente determinístico e perfeitamente errado — modelos pequenos (7-8B) provam isso.

Mas esse achado se aplica a tools cujo output é ambíguo. Quando as tools são tautológicas, [[Determinismo]] **implica** acurácia. Se a tool só pode retornar a resposta certa ou "não sei", e o sistema é determinístico, o sistema é deterministicamente correto.

A correlação nula do DFAH mede agentes com tools genéricas. A tese [[Tautologia Ontológica]] opera com tools tautológicas — um universo onde r = -0.11 não se aplica.

## Critérios

Uma tool é tautológica quando:
1. **Input tipado**: Parâmetros com tipos explícitos, sem ambiguidade
2. **Output finito**: Espaço de saída é fechado (enum de possibilidades, não texto livre)
3. **Falha explícita**: Quando não pode responder, retorna "não encontrado" / erro, nunca inventa
4. **Idempotência**: Mesmo input sempre produz mesmo output
5. **Contrato completo**: Docstring/spec cobre todos os comportamentos possíveis

## Na POC

As tools da POC são majoritariamente tautológicas:

| Tool | Tautológica? | Por quê |
|---|---|---|
| `search_docs` | Sim | Busca substring — encontra ou não encontra |
| `list_docs` | Sim | Lista arquivos — retorno é o filesystem |
| `get_doc` | Sim | Lê arquivo — retorna conteúdo ou "not found" |
| `crawl_docs` | Sim | Faz HTTP + salva — sucesso ou erro |
| `save_diagram` | Sim | Escreve arquivo — sucesso ou erro |
| `generate_prompt` | **Parcial** | Gera texto via LLM — output aberto, mas framework de 6 seções restringe |
| `generate_diagram` | **Parcial** | Gera Mermaid.js — output semi-aberto, mas syntax refs restringem |
| `judge_diagram` | **Parcial** | Score 0-10 em 4 dimensões — output é numérico, mas julgamento envolve inferência |

As tools parcialmente tautológicas são as que envolvem geração. O [[Transformer-Driven Prompt Architect]] e o [[Scoring de Diagramas]] são mecanismos que aproximam essas tools da tautologia — restringem o espaço de saída sem fechá-lo completamente.

## Ontologia Completa = Cobertura Total de Tools Tautológicas

A [[Ontologia]] de um domínio é completa quando **todo método/processo do domínio tem uma tool tautológica correspondente**. Verificável: enumere os métodos, verifique cobertura, confirme que cada tool é tautológica.

Se toda tool é tautológica e toda ação do domínio é coberta por uma tool, o sistema é tautológico por construção — não por probabilidade.

---

Relaciona-se com: [[Tool]], [[Tautologia]], [[Determinismo]], [[DFAH]], [[Ontologia]], [[Tautologia Ontológica]], [[MCP]], [[Contexto]], [[Espaço Amostral]]
