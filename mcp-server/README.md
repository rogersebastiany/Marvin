# Marvin — MCP Server

Unified [Model Context Protocol](https://modelcontextprotocol.io/) server implementing the Tautologia Ontologica thesis. Single server, 29 tools, 6 backends. The agent's sole interface to all knowledge and memory.

## Quick Start

```bash
uv sync
uv run python marvin_server.py
```

Requires Neo4j, Milvus, and an OpenAI API key. See [Configuration](#configuration).

## Architecture

```
Agent ←→ marvin_server.py ←→ 6 backends
                                ├── ontology.py        → Neo4j (knowledge graph)
                                ├── memory.py          → Milvus + OpenAI (episodic memory)
                                ├── docs_backend.py    → Filesystem (markdown docs)
                                ├── web_to_docs_backend.py → httpx (web → markdown → docs/)
                                ├── prompt_engineer_backend.py (prompt generation)
                                └── system_design_backend.py → Filesystem (Mermaid diagrams)
```

The agent never talks to Neo4j, Milvus, or the filesystem directly — only through Marvin.

## 29 Tools

| Category | Tools | Tautological |
|----------|-------|:------------:|
| **Retrieval** | `retrieve`, `get_concept`, `traverse`, `why_exists` | Yes |
| **Logging** | `log_tool_call`, `log_decision`, `log_session` | Yes |
| **Enrichment** | `expand`, `link`, `auto_link`, `ensure_bidirectional` | Yes |
| **Evolution** | `propose_schema_change`, `execute_schema_change` | Yes (human gate) |
| **Documentation** | `search_docs`, `list_docs`, `get_doc`, `fetch_url`, `save_doc`, `crawl_docs` | Yes |
| **Prompt Engineering** | `generate_prompt`, `refine_prompt`, `audit_prompt` | Partial |
| **Diagrams** | `generate_diagram`, `judge_diagram`, `save_diagram`, `list_diagrams`, `get_diagram` | Partial |
| **Introspection** | `inspect_schemas`, `stats` | Yes |

**Tautological** = given valid input, exactly one correct output exists (found/not-found, saved/failed). **Partial** = output depends on LLM generation but is constrained by structured frameworks.

## Configuration

All credentials via `.env` in the project root:

```env
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASS=tautologia
MILVUS_HOST=localhost
MILVUS_PORT=19530
OPENAI_API_KEY=sk-...
EMBEDDING_MODEL=text-embedding-3-small
```

## Wire into Claude Code

Add to `.mcp.json` at your project root:

```json
{
  "mcpServers": {
    "mcp-marvin": {
      "type": "stdio",
      "command": "uv",
      "args": ["run", "python", "marvin_server.py"],
      "cwd": "/path/to/mcp-server"
    }
  }
}
```

## Data Directories

- **`docs/`** — 210+ fetched markdown docs (Python, AWS, Kotlin, SE patterns, CI/CD, etc.)
- **`diagrams/`** — Saved Mermaid.js `.mmd` files

## Design Decisions

- **Non-destructive graph ops** — MERGE, not DELETE. Agent-owned concepts never overwritten.
- **Bidirectional edges** — Every A→B gets a B→A. Deterministic traversal from any direction.
- **Auto-linking** — Scans concept content for references to other concept names. Tautological — found or not found.
- **Three-tier memory** — L1 tool calls (experience), L2 decisions (knowledge), L3 sessions (wisdom). Maps to HCC.
- **Path traversal protection** — `_safe_path()` / `_safe_diagram_path()` on all file operations.
- **Polite HTTP** — Identifying User-Agent on all web fetches.

## Execution Pattern

```
1. RETRIEVE BEFORE ACT   — query ontology + memory before generating
2. FETCH IF MISSING       — if no docs exist for a technology, fetch first
3. ACT WITH CONTEXT       — each tool call reduces the sample space
4. LOG AFTER ACT          — record actions, decisions, session summaries
5. ENRICH                 — expand the ontology with new concepts and relations
```
