# Tool como Bias

Cada [[Primitivas MCP|tool MCP]] funciona como um [[Bias]] no cálculo do próximo token. A descrição da tool é um prompt que é [[Tokenização|tokenizado]], [[Embedding|embeddado]], e esse conjunto de [[Vetor|vetores]] desloca a [[Activation Function|ativação]] na direção correta.

---

## O Mecanismo

Na [[Álgebra Linear]], o neurônio calcula: `output = activation(W · x + b)`. O bias `b` desloca o ponto de ativação. Sem bias, a ativação é centrada na origem. Com bias, é deslocada — favorecendo certas regiões do [[Espaço Amostral]].

Uma tool MCP funciona exatamente assim. Quando o [[Agente na POC]] tem acesso a `search_docs(query)`, a descrição dessa tool — `"Search across all documentation files for a keyword or phrase"` — entra no [[Contexto Programático|contexto]] como vetores adicionais que enviesam o modelo para buscar em documentação local antes de inventar.

## Na POC: 4 Fontes de Bias

Cada server contribui com bias diferente:

| Server | Bias que introduz |
|---|---|
| [[docs-server]] | "Existe documentação local. Busque antes de inferir." |
| [[web-to-docs]] | "Se não existe localmente, pode buscar na web e salvar." |
| [[prompt-engineer]] | "Existe um framework estruturado para criar prompts." |
| [[system-design]] | "Diagramas devem seguir Mermaid.js com syntax references." |

O [[Catálogo de Tools]] construído pelo [[prompt-engineer]] no startup é a soma de todos os biases — injetado em cada prompt gerado. É [[Ontologia como Código|ontologia]] servida como bias.

## Bias Acumulativo

Cada tool chamada retorna um resultado que entra no contexto como novo bias. É cumulativo:

1. `list_docs()` → bias: "existem estes docs disponíveis"
2. `search_docs("auth")` → bias: "a documentação diz isto sobre auth"
3. `generate_diagram(...)` → bias: "a arquitetura se parece com isto"

Cada passo adiciona bias → restringe o [[Espaço Amostral]] → aproxima do [[Determinismo]]. É a [[Redução de Espaço na Prática]] via bias acumulativo.

## Não é Metáfora

"Não é magia, é [[Álgebra Linear]]." A tool não "ajuda" o modelo metaforicamente. Ela literalmente adiciona vetores ao input que deslocam o cálculo matemático do próximo token. O [[Subconjunto]] de vetores relevantes fica menor e mais preciso. A [[Probabilidade Condicional]] do token correto aumenta.

## Tool como Bias + Tool Tautológica

O bias desloca o cálculo. Mas para onde? Se a tool é [[Tool Tautológica|tautológica]] — contrato I/O completo, output finito, falha explícita — o bias desloca na **única direção correta**. A combinação bias + tautologia garante que o deslocamento não é apenas consistente ([[Determinismo]]) mas correto (acurácia).

Na POC: `search_docs` é bias (restringe o espaço) + tautológica (encontra ou "not found"). O resultado é determinístico **e** correto por construção.

---

Relaciona-se com: [[Bias]], [[Primitivas MCP]], [[Catálogo de Tools]], [[Contexto Programático]], [[Redução de Espaço na Prática]], [[Álgebra Linear]], [[Ontologia como Código]], [[Agente na POC]], [[docs-server]], [[prompt-engineer]], [[Tool Tautológica]]
