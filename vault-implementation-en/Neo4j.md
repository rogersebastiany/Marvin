# Neo4j

Graph database that stores the [[Ontologia como Código|ontology]] as a knowledge graph. Each concept from the vaults becomes a node, each link becomes an edge. The [[Agente na POC|agent]] queries and enriches the graph via [[mcp-ontology-server]].

---

## Why a Graph

The [[Ontologia como Código|ontology]] in the Obsidian vaults is already a graph -- notes are nodes, wikilinks are edges. Neo4j materializes this graph into a queryable, traversable, and agent-enrichable database.

Unlike a relational database, Neo4j allows traversal queries (2 hops, 3 hops, path between concepts) in constant time relative to the neighborhood, not the total graph size.

## Agreed Schema

**Nodes** -- Label `:Concept`
- `name`: Concept name (e.g. "Tautologia Ontologica")
- `vault`: Which vault it came from ("thesis", "implementation", or "both" if merged)
- `summary`: One-line summary
- `content`: Complete content of the markdown note
- `ghost`: Boolean -- true if the concept is referenced but has no own note (ghost node in Obsidian)
- `created_at`, `updated_at`: Timestamps

**Edges** -- Single type `:RELATES_TO` with property bag
- `type`: Semantic type of the relationship (e.g. "implements", "validates", "contradicts")
- `weight`: Relationship strength (0.0 to 1.0)
- `reasoning`: Why this relationship exists
- `discovered_by`: Who created it -- "vault_import", "agent", "user"

Flat edges with property bags instead of multiple edge types. The agent can create non-linear relationships between concepts without needing new edge types -- just add properties to the existing edge.

## Concept Merging

Concepts that appear in both vaults (e.g. "Determinismo" in the thesis vault and "Determinismo Mensuravel" in the implementation vault) are merged into a single node with `vault: "both"`. The content combines perspectives -- theoretical and practical.

Ghost nodes (referenced but without a note) become nodes with `ghost: true`. The agent can fill in these nodes over time.

## Role in the Architecture

Neo4j is the backend of [[mcp-ontology-server]]. The agent queries the graph to:
- Understand concepts and their relationships
- Traverse the neighborhood (what relates to X?)
- Discover gaps (which ghost nodes exist?)
- Enrich the ontology (add concepts, relationships, properties)

It is the living [[Ontologia como Código|ontology]] -- not static, enriched with every interaction of the [[Loop de Auto-Melhoria]].

---

Related to: [[Ontologia como Código]], [[mcp-ontology-server]], [[Loop de Auto-Melhoria]], [[Agente na POC]], [[MCP]]
