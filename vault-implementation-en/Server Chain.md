# Server Chain

The 4 MCP servers in the POC complement each other in a chain of cumulative [[Programmatic Context|context]]. Each server addresses a gap the previous one does not cover, and the output of one feeds the next.

---

## The Chain

```
docs-server <- "what do we know?"
     |
web-to-docs <- "what can we know?"
     |
prompt-engineer <- "how to ask well?"
     |
system-design <- "how to visualize?"
```

## Typical Flow

1. [[Agent in POC]] needs information -> calls [[docs-server]] `search_docs("lambda")`
2. Not found -> calls [[web-to-docs]] `crawl_docs("https://docs.aws.amazon.com/lambda/...")`
3. web-to-docs saves pages to `docs/` -> now searchable by docs-server
4. Agent searches again -> `search_docs("lambda")` -> found
5. Agent needs an optimized prompt -> [[prompt-engineer]] `generate_prompt("Lambda expert", "cloud")`
6. prompt-engineer injects the complete [[Tool Catalog]] into the generated prompt
7. Agent needs a diagram -> [[system-design]] `generate_diagram("Lambda with API Gateway")`
8. system-design injects syntax refs from `docs/mermaid-*.md` into the context

## Couplings

**docs-server <-> web-to-docs:** Share `docs/`. web-to-docs writes, docs-server reads. The `docs/` directory is the integration point.

**prompt-engineer -> all 3:** Imports the 3 sibling servers at startup to build the [[Tool Catalog]]. Tight coupling -- all 3 must be importable.

**system-design -> docs-server:** Reads `docs/mermaid-*.md` at startup as syntax reference. Depends on the docs existing.

## In the Thesis

The chain implements the progressive reduction of the [[Sample Space]]:

1. docs-server: constrains to what is documented (A subset of S)
2. web-to-docs: expands A and then constrains with verified content
3. prompt-engineer: constrains the way of asking (eliminates ambiguity)
4. system-design: constrains visual representation (eliminates interpretations)

Each link is an intersection operation in [[Set Theory]]: A intersection T1 intersection T2 intersection T3 -> precise [[Subset]] -> [[Measurable Determinism|determinism]].

It is [[Space Reduction in Practice]] materialized in software architecture.

## Evolution: 6 Servers

The original chain (4 servers) operates on static ontology in `docs/`. Two new servers add living ontology and memory:

```
docs-server <- "what do we know?" (text)
     |
web-to-docs <- "what can we know?"
     |
prompt-engineer <- "how to ask well?"
     |
system-design <- "how to visualize?"
     |
mcp-ontology-server <- "what do we know?" (semantic graph)
     |
mcp-memory-server <- "what have we already done?"
```

The [[mcp-ontology-server]] queries [[Neo4j]] -- concepts and relationships as a graph. The [[mcp-memory-server]] queries [[Milvus]] -- tool calls, decisions, and sessions as vectors.

The two new servers enable the [[Self-Improvement Loop]]: the agent queries -> acts -> logs -> discovers -> enriches -> next cycle is richer.

---

Related to: [[docs-server]], [[web-to-docs]], [[prompt-engineer]], [[system-design]], [[mcp-ontology-server]], [[mcp-memory-server]], [[Deterministic Feedback Loop]], [[Space Reduction in Practice]], [[Tool Catalog]], [[Agent in POC]], [[Programmatic Context]], [[Self-Improvement Loop]]
