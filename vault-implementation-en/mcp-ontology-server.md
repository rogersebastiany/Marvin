# mcp-ontology-server

MCP server that exposes the [[Neo4j]] knowledge graph as tools for the [[Agente na POC|agent]]. It allows querying, traversing, and enriching the [[Ontologia como Código|ontology]].

---

## Tools

| Tool | Description |
|---|---|
| `query` | Searches concepts by name, tag, or free text |
| `get_concept` | Returns a complete concept with its relationships |
| `traverse` | Walks N hops from a concept, returning the neighborhood |
| `why_exists` | Explains why a concept exists in the ontology -- returns the edge reasoning |
| `expand` | Adds a new concept or new relationship to the graph |

## Difference from docs-server

The [[docs-server]] searches text in markdown files. The mcp-ontology-server searches **concepts and relationships** in a graph. The difference:

- `search_docs("determinism")` -> lines of text containing "determinism"
- `query("Determinism")` -> the Determinism node with its 11 relationships, weights, and reasoning

The graph has semantics that text does not.

## Enrichment by the Agent

The agent can use `expand` to add concepts and relationships it discovers during work. If during a session the agent realizes that "FastMCP implements schema-first architecture", it can create that relationship in the graph.

Edges created by the agent have `discovered_by: "agent"` -- distinguishable from those imported from vaults (`discovered_by: "vault_import"`).

## In the Server Chain

The mcp-ontology-server integrates into the existing [[Cadeia de Servers]]:

```
Agent needs to understand a concept -> mcp-ontology-server (traverse)
    | concept has ghost nodes
Agent fills gaps -> mcp-ontology-server (expand)
    | needs detailed docs
docs-server (search_docs)
    | not found
web-to-docs (crawl_docs) -> saves -> docs-server finds it
    | updates the graph
mcp-ontology-server (expand)
```

---

Related to: [[Neo4j]], [[Ontologia como Código]], [[Cadeia de Servers]], [[docs-server]], [[Loop de Auto-Melhoria]], [[MCP]], [[FastMCP]]
