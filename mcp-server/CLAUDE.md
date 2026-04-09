# mcp-server — Marvin

Unified MCP server implementing the Tautologia Ontologica thesis. The agent's sole interface to all knowledge and memory.

## Run

```bash
uv sync
uv run python marvin_server.py          # production (stdio)
uv run fastmcp run marvin_server.py --reload  # dev mode (auto-reload on file changes)
```

## Architecture

Single server (`marvin_server.py`) wrapping 6 backend modules:

| Module | Backend | What It Does |
|--------|---------|-------------|
| `ontology.py` | Neo4j | Knowledge graph — concepts, relations, traversal, auto-link, bidirectionality |
| `memory.py` | Milvus + OpenAI | Episodic memory — tool calls (L1), decisions (L2), sessions (L3) |
| `docs_backend.py` | Filesystem | Search/browse local markdown docs (`docs/`) |
| `web_to_docs_backend.py` | httpx + BS4 | Fetch web → markdown → save to `docs/` |
| `prompt_engineer_backend.py` | — | Transformer-Driven Prompt Architect framework |
| `system_design_backend.py` | Filesystem | Mermaid.js diagram generation/review (`diagrams/`) |

## 32 Tools (8 categories)

| Category | Tools | Tautological? |
|----------|-------|--------------|
| Retrieval | `retrieve`, `get_concept`, `traverse`, `why_exists` | Yes |
| Logging | `log_tool_call`, `log_decision`, `log_session` | Yes |
| Enrichment | `expand`, `link`, `auto_link`, `ensure_bidirectional` | Yes |
| Evolution | `propose_schema_change`, `execute_schema_change` | Yes (human gate) |
| Documentation | `search_docs`, `list_docs`, `get_doc`, `fetch_url`, `save_doc`, `crawl_docs`, `research_topic` | Yes |
| Prompt Engineering | `generate_prompt`, `refine_prompt`, `audit_prompt` | Partial |
| Diagrams | `generate_diagram`, `judge_diagram`, `save_diagram`, `list_diagrams`, `get_diagram` | Partial |
| Introspection | `inspect_schemas`, `stats` | Yes |

## Configuration

All credentials via environment variables (`.env` in project root):

```
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASS=tautologia
MILVUS_HOST=localhost
MILVUS_PORT=19530
OPENAI_API_KEY=sk-...
EMBEDDING_MODEL=text-embedding-3-small
```

## Data Directories

- `docs/` — 210+ fetched markdown docs (Python, AWS, Kotlin, SE patterns, CI/CD, etc.)
- `diagrams/` — Saved Mermaid.js `.mmd` files

## Key Design Decisions

- **Non-destructive graph ops**: MERGE not DELETE. Agent-owned concepts (vault="agent") never overwritten.
- **Bidirectional edges**: Every A→B has B→A. Deterministic traversal from any direction.
- **Auto-linking**: Scans concept content for references to other concept names. Tautological — found or not found.
- **Three-tier memory**: Maps to HCC (Hierarchical Cognitive Caching) — L1 Experience, L2 Knowledge, L3 Wisdom.
- **Path traversal protection**: `_safe_path()` / `_safe_diagram_path()` on all file ops.
- **User-Agent on HTTP**: Polite fetching with identifying header.

## Wire into Claude Code

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
