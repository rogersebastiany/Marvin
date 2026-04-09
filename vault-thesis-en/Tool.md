# Tool

A [[Subset]] of [[Vector|vectors]] that functions as [[Bias]] for the computation of the next token. Any source of structured [[Context]] that restricts the [[Sample Space]].

---

## Definition

In the context of LLMs and [[MCP]], a tool is a function or external resource that the model can invoke to obtain information. Documentation, APIs, specs, integrations.

"A tool is nothing more than a subset of vectors. The tool's description is a prompt that is tokenized, embedded, and that set becomes a bias for the computation of the next possible token."

## How Tools Work

The tool's description is processed in the same way as any [[Context]]: [[Tokenization]] -> [[Embedding]] -> [[Vector|vectors]] in the [[Sample Space]]. These additional vectors restrict the search space, functioning as [[Bias]] that shifts the [[Activation Function|activation]] in the correct direction.

## Tools as Ontology

Each tool represents a piece of the domain's [[Ontology]]. The AWS SQS documentation tool contains the ontology of queues. The system specs tool contains the ontology of expected behavior. Cumulatively, all tools build the complete ontology.

Tools are served via [[MCP]] for O(1) access -- the open gate between the model and context.

## Tautological Tool

A [[Tautological Tool]] is a tool whose I/O contract is complete and unambiguous -- given a valid input, there exists exactly one correct output. `search_docs` finds or does not find. `get_doc` returns the content or "not found." There is no third option.

When all tools in a domain are tautological, [[Determinism]] implies accuracy. The null correlation (r = -0.11) from [[DFAH]] between determinism and accuracy applies to generic tools with ambiguous output -- not to tautological tools.

---

Related to: [[Bias]], [[Context]], [[MCP]], [[Subset]], [[Vector]], [[Ontology]], [[Sample Space]], [[Activation Function]], [[Tautological Tool]], [[DFAH]]
