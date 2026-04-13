# Marvin — MCP Server

Unified [Model Context Protocol](https://modelcontextprotocol.io/) server implementing the Ontological Tautology thesis. 47 tools, 9 backends, 2 middlewares. The agent's sole interface to all knowledge and memory.

Built with [FastMCP](https://github.com/jlowin/fastmcp) 3.x, Python 3.12, managed with [uv](https://docs.astral.sh/uv/).

## Quick Start

```bash
uv sync
cp .env.example ../.env   # edit with your credentials
uv run python marvin_server.py              # production (stdio)
uv run fastmcp run marvin_server.py --reload  # dev (auto-reload)
```

Requires Neo4j, Milvus, and an OpenAI API key. See [Configuration](#configuration).

## Architecture

```
MCP Client (Claude Code, Cursor, VS Code, etc.)
  |
  +-- marvin_server.py
        |
        |  Dynamic identity (built from KG at startup)
        |  RetrieveBeforeActMiddleware (Milvus Gate, P=0)
        |  OrchestrationGateMiddleware (Plan Gate, P=0)
        |
        +-- backends/
              +-- ontology.py             -> Neo4j (knowledge graph)
              +-- memory.py               -> Milvus + OpenAI (episodic memory)
              +-- docs_backend.py         -> Filesystem (markdown docs)
              +-- web_to_docs_backend.py  -> httpx + BS4 (web -> markdown)
              +-- prompt_engineer_backend.py  (Prompt Architect framework)
              +-- system_design_backend.py   (Mermaid.js diagrams)
              +-- code_improvement_backend.py (AST chunking + Milvus vector walk)
              +-- orchestrator_backend.py    (goal -> execution plan, 7 chains)
              +-- ops_backend.py             (vault sync, self-audit, self-improve)
```

The agent never talks to Neo4j, Milvus, or the filesystem directly — only through Marvin's tools.

## Middlewares

Two FastMCP `Middleware` classes intercept every tool call. Hard gates (P=0) — the server raises `ToolError` and refuses execution. No prompt can bypass them.

### Milvus Gate (`RetrieveBeforeActMiddleware`)

All Neo4j reads and writes are blocked unless a Milvus-tier tool (`retrieve`, `get_memory`, `search_docs`) was called first in the session. Forces the agent to ground itself in existing knowledge before acting.

### Orchestration Gate (`OrchestrationGateMiddleware`)

Enrichment tools (`expand`, `link`, `auto_link`, etc.) are blocked unless `orchestrate` was called first. Prevents ad-hoc graph mutations from LLM impulse — all changes must follow a planned chain.

Provenance enforcement: `expand` additionally requires `source_doc` when called within a densify/research chain.

## Tool Tiers

| Tier | Count | Effect |
|------|-------|--------|
| **Milvus (sets gate)** | 10 | Semantic search — sets the "grounded" flag |
| **Overview (ungated)** | 8 | Read-only metadata — no gate needed |
| **Neo4j Read (gated)** | 4 | Blocked until Milvus flag is set |
| **Write (gated)** | 18 | Blocked until Milvus flag is set |
| **Always Allowed** | 7 | Logging, audits, URL fetching |

Run `uv run python scripts/update_tool_list.py` for the full tool catalog, or `--write` to update docs.

## Dynamic Identity

Marvin's `instructions` (what the MCP client sees as the server's system prompt) are built from the knowledge graph at startup — not a static string:

1. Check Milvus `self_description` collection for cached identity
2. Cache miss -> query Neo4j thesis vault + introspect tool catalog + assemble identity -> cache in Milvus
3. Call `self_description` tool to rebuild after updating the thesis vault or adding tools

## Configuration

All credentials via `.env` in the project root:

```env
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASS=changeme
MILVUS_HOST=localhost
MILVUS_PORT=19530
OPENAI_API_KEY=sk-...
EMBEDDING_MODEL=text-embedding-3-small
```

Toggle enforcement (for development):

```env
MARVIN_DISABLE_MILVUS_GATE=1        # disable Milvus Gate middleware
MARVIN_DISABLE_ORCHESTRATION_GATE=1  # disable Orchestration Gate middleware
MARVIN_DISABLE_PROVENANCE=1          # disable source_doc requirement on expand
```

## Wire into your MCP client

```json
{
  "mcpServers": {
    "mcp-marvin": {
      "type": "stdio",
      "command": "uv",
      "args": ["run", "python", "marvin_server.py"],
      "cwd": "/path/to/Marvin/mcp-server"
    }
  }
}
```

## Data Directories

- **`../docs/`** — 72 fetched markdown docs (Cognee, MCP, OWASP, Neo4j, Milvus, etc.)
- **`../diagrams/`** — Saved Mermaid.js `.mmd` files
- **`../vaults/`** — Obsidian vaults (Cognee input)

## Tests

```bash
uv run pytest   # 365 tests
```

## Design Decisions

- **Non-destructive graph ops** — MERGE, not DELETE. Agent-owned concepts (vault="agent") never overwritten.
- **Bidirectional edges** — Every A->B gets a B->A. Deterministic traversal from any direction.
- **Auto-linking** — Scans concept content for references to other concept names. Tautological — found or not found.
- **Three-tier episodic memory (HCC)** — L2 decisions + L3 sessions in Milvus. L1 tool traces are transient context window memory — not persisted per HCC design.
- **Path traversal protection** — `_safe_path()` / `_safe_diagram_path()` on all file operations.
- **Polite HTTP** — Identifying User-Agent on all web fetches.
- **`log_decision` is async fire-and-forget** — daemon thread, never blocks the agent.

## Execution Pattern

```
1. RETRIEVE BEFORE ACT   — query Milvus (ontology + memory + docs) before anything
2. FETCH IF MISSING       — if no docs exist for a technology, fetch first
3. ORCHESTRATE            — establish an execution plan before mutations
4. ACT WITH CONTEXT       — each tool call reduces the sample space
5. LOG AFTER ACT          — record decisions (L2), session summaries (L3)
6. ENRICH                 — expand the ontology with new concepts and relations
```
