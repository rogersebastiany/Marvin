// ═══════════════════════════════════════════════════════════════════
// Neo4j Browser exploration queries — Tautologia Ontologica
//
// Run these one at a time in Neo4j Browser to explore the graph.
// The GraSS stylesheet (neo4j-browser-style.grass) colors nodes
// by label and edges by type.
// ═══════════════════════════════════════════════════════════════════


// ── 1. Full overview — all Concept nodes (limit to avoid browser crash) ──
MATCH (c:Concept)-[r]->(t:Concept)
RETURN c, r, t
LIMIT 300;


// ── 2. Hub concepts — most connected nodes ──
MATCH (c:Concept)-[r]-()
WITH c, count(r) AS degree
ORDER BY degree DESC
LIMIT 25
MATCH (c)-[r]-(neighbor:Concept)
RETURN c, r, neighbor;


// ── 3. Thesis core — concepts from the thesis vaults ──
MATCH (c:Concept)-[r]-(t:Concept)
WHERE c.vault IS NULL AND t.vault IS NULL
RETURN c, r, t
LIMIT 200;


// ── 4. Agent-discovered concepts — what Marvin learned on its own ──
MATCH (c:Concept {vault: 'agent'})-[r]-(t:Concept)
RETURN c, r, t;


// ── 5. Ghost concepts — referenced but not yet fully defined ──
MATCH (c:Concept {vault: 'ghost'})-[r]-(t:Concept)
RETURN c, r, t;


// ── 6. Edge type distribution ──
MATCH ()-[r]->()
RETURN type(r) AS edge_type, count(r) AS count
ORDER BY count DESC;


// ── 7. COMPOSES tree — the part-of hierarchy (largest edge type) ──
MATCH path = (child:Concept)-[:COMPOSES*1..3]->(parent:Concept)
RETURN path
LIMIT 200;


// ── 8. IMPLEMENTS chain — concrete realizations of abstractions ──
MATCH path = (concrete:Concept)-[:IMPLEMENTS]->(abstract:Concept)
RETURN path
LIMIT 100;


// ── 9. REQUIRES dependencies — what depends on what ──
MATCH path = (a:Concept)-[:REQUIRES]->(b:Concept)
RETURN path
LIMIT 100;


// ── 10. CONTRADICTS — mutual oppositions (rare, high signal) ──
MATCH (a:Concept)-[:CONTRADICTS]-(b:Concept)
RETURN a, b;


// ── 11. Isolated concepts — no edges at all ──
MATCH (c:Concept)
WHERE NOT (c)-[]-()
RETURN c.name AS orphan, c.vault AS vault
ORDER BY c.name;


// ── 12. Cross-vault bridges — agent concepts linking to Cognee concepts ──
MATCH (a:Concept {vault: 'agent'})-[r]-(c:Concept)
WHERE c.vault IS NULL OR c.vault <> 'agent'
RETURN a, r, c;


// ── 13. Concept neighborhood — pick a concept and see its 2-hop graph ──
// Replace 'Tautologia Ontologica' with any concept name
MATCH path = (c:Concept {name: 'Tautologia Ontologica'})-[*1..2]-(n:Concept)
RETURN path;


// ── 14. Shortest path between two concepts ──
// Replace names as needed
MATCH path = shortestPath(
  (a:Concept {name: 'Milvus'})-[*]-(b:Concept {name: 'Neo4j'})
)
RETURN path;


// ── 15. Security cluster — OWASP and related concepts ──
MATCH path = (c:Concept)-[*1..2]-(n:Concept)
WHERE c.name CONTAINS 'OWASP' OR c.name CONTAINS 'Security'
   OR c.name CONTAINS 'Authentication' OR c.name CONTAINS 'CWE'
RETURN path;


// ── 16. Cognee internals — TextDocument → DocumentChunk → TextSummary ──
// (These are the Cognee pipeline artifacts, not Marvin concepts)
MATCH (d:TextDocument)-[r]-(chunk)
RETURN d, r, chunk
LIMIT 50;


// ── 17. Stats dashboard ──
CALL {
  MATCH (c:Concept) RETURN 'concepts' AS metric, count(c) AS value
  UNION ALL
  MATCH (c:Concept {vault: 'agent'}) RETURN 'agent_concepts' AS metric, count(c) AS value
  UNION ALL
  MATCH (c:Concept {vault: 'ghost'}) RETURN 'ghost_concepts' AS metric, count(c) AS value
  UNION ALL
  MATCH ()-[r]->() RETURN 'edges' AS metric, count(r) AS value
  UNION ALL
  MATCH (c:Concept) WHERE NOT (c)-[]-() RETURN 'orphans' AS metric, count(c) AS value
}
RETURN metric, value
ORDER BY metric;
