// ═══════════════════════════════════════════════════════════════════
// Neo4j label setup — add vault-based secondary labels for styling.
//
// Neo4j Browser GraSS can only style by LABEL, not property value.
// This script adds secondary labels so vault-based coloring works:
//   :Concept:Cognee   — blue (extracted by Cognee from vaults)
//   :Concept:Agent    — green (discovered by Marvin)
//   :Concept:Ghost    — grey (referenced but undefined)
//
// Run once, then re-run after sync_vaults if new concepts appear.
// Safe to re-run — uses SET, not CREATE.
// ═══════════════════════════════════════════════════════════════════


// ── Add :Cognee label to vault-less concepts (Cognee-extracted) ──
MATCH (c:Concept)
WHERE c.vault IS NULL OR c.vault = ''
SET c:Cognee
RETURN count(c) AS cognee_labeled;


// ── Add :Agent label to agent-discovered concepts ──
MATCH (c:Concept {vault: 'agent'})
SET c:Agent
RETURN count(c) AS agent_labeled;


// ── Add :Ghost label to ghost (referenced-but-undefined) concepts ──
MATCH (c:Concept {vault: 'ghost'})
SET c:Ghost
RETURN count(c) AS ghost_labeled;


// ── Verify label distribution ──
CALL {
  MATCH (c:Cognee) RETURN 'Cognee' AS label, count(c) AS count
  UNION ALL
  MATCH (c:Agent) RETURN 'Agent' AS label, count(c) AS count
  UNION ALL
  MATCH (c:Ghost) RETURN 'Ghost' AS label, count(c) AS count
}
RETURN label, count
ORDER BY count DESC;
