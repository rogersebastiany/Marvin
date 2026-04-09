# Tool as Bias

Each [[Primitivas MCP|MCP tool]] functions as a [[Bias]] in the next token calculation. The tool description is a prompt that is [[Tokenização|tokenized]], [[Embedding|embedded]], and this set of [[Vetor|vectors]] shifts the [[Activation Function|activation]] in the correct direction.

---

## The Mechanism

In [[Álgebra Linear]], the neuron computes: `output = activation(W * x + b)`. The bias `b` shifts the activation point. Without bias, activation is centered at the origin. With bias, it is shifted -- favoring certain regions of the [[Espaço Amostral]].

An MCP tool works exactly like this. When the [[Agente na POC]] has access to `search_docs(query)`, the description of that tool -- `"Search across all documentation files for a keyword or phrase"` -- enters the [[Contexto Programático|context]] as additional vectors that bias the model toward searching local documentation before inventing.

## In the POC: 4 Sources of Bias

Each server contributes a different bias:

| Server | Bias it introduces |
|---|---|
| [[docs-server]] | "Local documentation exists. Search before inferring." |
| [[web-to-docs]] | "If it doesn't exist locally, you can search the web and save." |
| [[prompt-engineer]] | "A structured framework for creating prompts exists." |
| [[system-design]] | "Diagrams must follow Mermaid.js with syntax references." |

The [[Catálogo de Tools]] built by [[prompt-engineer]] at startup is the sum of all biases -- injected into every generated prompt. It is [[Ontologia como Código|ontology]] served as bias.

## Cumulative Bias

Each tool called returns a result that enters the context as new bias. It is cumulative:

1. `list_docs()` -> bias: "these docs are available"
2. `search_docs("auth")` -> bias: "the documentation says this about auth"
3. `generate_diagram(...)` -> bias: "the architecture looks like this"

Each step adds bias -> constrains the [[Espaço Amostral]] -> approaches [[Determinismo]]. It is [[Redução de Espaço na Prática]] via cumulative bias.

## It Is Not a Metaphor

"It's not magic, it's [[Álgebra Linear]]." The tool does not "help" the model metaphorically. It literally adds vectors to the input that shift the mathematical calculation of the next token. The [[Subconjunto]] of relevant vectors becomes smaller and more precise. The [[Probabilidade Condicional]] of the correct token increases.

## Tool as Bias + Tautological Tool

The bias shifts the calculation. But in which direction? If the tool is [[Tool Tautológica|tautological]] -- complete I/O contract, finite output, explicit failure -- the bias shifts in the **only correct direction**. The combination of bias + tautology guarantees that the shift is not only consistent ([[Determinismo]]) but correct (accuracy).

In the POC: `search_docs` is bias (constrains the space) + tautological (finds or "not found"). The result is deterministic **and** correct by construction.

---

Related to: [[Bias]], [[Primitivas MCP]], [[Catálogo de Tools]], [[Contexto Programático]], [[Redução de Espaço na Prática]], [[Álgebra Linear]], [[Ontologia como Código]], [[Agente na POC]], [[docs-server]], [[prompt-engineer]], [[Tool Tautológica]]
