# Milvus Gate Middleware

Architectural middleware that blocks ALL Neo4j reads and write operations until a Milvus search has been performed in the session. Implements the [[Architectural Enforcement|Retrieve Before Act]] principle with P=0 -- not prompt bias, architectural impossibility.

---

## Why It Exists

The [[Agent in POC|agent]] tends to act before consulting. Prompts saying "search first" are bias -- the model can ignore them. The middleware transforms "should search" into "cannot act without searching." Action without context becomes impossible, not improbable.

## 4-Tier Tool Classification

Every [[Marvin]] tool belongs to exactly one tier:

| Tier | Behavior | Examples |
|------|----------|----------|
| **Milvus (opens gate)** | Semantic search -- opens access | `retrieve`, `get_memory`, `search_docs`, `improve_code`, `tdd`, `orchestrate`, `refine_plan` |
| **Overview (always allowed)** | Lightweight reads, no side effects | `stats`, `list_concepts`, `list_docs`, `self_description`, `inspect_schemas` |
| **Neo4j Read (gated)** | Graph reads -- requires open gate | `get_concept`, `traverse`, `why_exists`, `audit_code` |
| **Write (gated)** | Writes to any backend -- requires open gate | `expand`, `link`, `save_doc`, `sync_vaults`, `self_improve` |
| **Always Allowed** | No-risk operations | `log_decision`, `log_session`, `fetch_url`, `audit_prompt` |

## How It Works

```
RetrieveBeforeActMiddleware.on_call_tool(tool_name):
    if tool in MILVUS_TOOLS:
        session.milvus_gate = True    # opens the gate
        return proceed()
    if tool in OVERVIEW_TOOLS or tool in ALWAYS_ALLOWED:
        return proceed()              # always passes
    if tool in GATED_TOOLS:
        if not session.milvus_gate:
            return BLOCKED             # P=0, impossible
        return proceed()
```

The gate is per-session. Each new MCP session starts closed. The first useful operation must be a semantic search.

## Relation to Ontology Phases

The thesis describes two phases:
- **Phase 1 (Build)**: web access enabled, research tools available
- **Phase 2 (Use)**: tautological tools only, web blocked

The Milvus Gate is Phase 1.5 -- allows everything but forces the agent to consult before acting. Full Phase 2 transition requires enforcement at the host level (Claude Code hooks), not just the MCP server.

## Implementation

Class `RetrieveBeforeActMiddleware` in `marvin_server.py`. Uses FastMCP's middleware system -- intercepts `on_call_tool` before execution. Constants `MILVUS_TOOLS`, `OVERVIEW_TOOLS`, `NEO4J_READ_TOOLS`, `WRITE_TOOLS` as frozensets for O(1) lookup.

---

Related to: [[Architectural Enforcement]], [[Marvin]], [[Milvus]], [[Neo4j]], [[Tautological Tool]]
