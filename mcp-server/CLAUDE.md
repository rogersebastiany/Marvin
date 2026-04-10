# mcp-server — Marvin

Unified MCP server implementing the Tautologia Ontologica thesis. The agent's sole interface to all knowledge and memory.

## Identity

Marvin's identity prompt is **not a static file**. It is built dynamically from the knowledge graph via `self_description`:

1. At startup (lifespan): check Milvus `self_description` collection for cached prompt
2. **Cache hit** → use cached prompt as server instructions
3. **Cache miss** → build from Neo4j thesis vault + code introspection → cache in Milvus → set instructions

Call `self_description` tool to rebuild after updating the thesis vault or adding tools.

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

## 35 Tools (8 categories)

| Category | Tools | Tautological? |
|----------|-------|--------------|
| Retrieval | `retrieve`, `get_concept`, `traverse`, `why_exists`, `list_concepts`, `get_memory` | Yes |
| Logging | `log_decision` (async fire-and-forget), `log_session` | Yes |
| Enrichment | `expand`, `link`, `auto_link`, `ensure_bidirectional`, `set_aliases`, `batch_set_aliases` | Yes |
| Evolution | `propose_schema_change`, `execute_schema_change` | Yes (human gate) |
| Documentation | `search_docs`, `list_docs`, `get_doc`, `fetch_url`, `save_doc`, `rank_urls`, `crawl_docs`, `research_topic` | Yes |
| Prompt Engineering | `generate_prompt`, `refine_prompt`, `audit_prompt` | Partial |
| Diagrams | `generate_diagram`, `judge_diagram`, `save_diagram`, `list_diagrams`, `get_diagram` | Partial |
| Introspection | `inspect_schemas`, `stats`, `self_description` | Yes |

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
- **Two-tier episodic memory**: L2 Knowledge (decisions) + L3 Wisdom (sessions) in Milvus. L1 Experience (tool traces) is transient working memory in the context window — not persisted per HCC design.
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
