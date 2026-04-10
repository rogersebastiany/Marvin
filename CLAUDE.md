# CLAUDE.md

## Foundational Rule — Retrieve Before Act

Before writing, editing, or generating ANY code, config, or infrastructure:

1. `retrieve` first — Milvus semantic search across ontology, episodic memory, and docs
2. Deep-dive if needed — `get_concept` or `traverse` for KG nodes, `get_doc` for full doc content
3. Fetch if missing — if `retrieve` returns nothing, call `fetch_url`/`save_doc`/`research_topic` BEFORE proceeding
4. Only then act — with verified context, not training weights

This applies to every technology: Python, FastMCP, Neo4j, Milvus, httpx, Terraform, AWS, Docker — no exceptions. Correct output from weights is luck, not construction.

The MCP server enforces this architecturally for Marvin tools via `RetrieveBeforeActMiddleware`. You must also enforce it on yourself for host tool actions (file edits, bash commands, code generation).

## Session Start

Call `stats` for a live system overview. Marvin's identity prompt is built dynamically from the knowledge graph at startup via `self_description` and cached in Milvus — no static file.

## Workspace

- **`mcp-server/`** — Marvin. Single unified MCP server (35 tools). FastMCP 3.x, Python 3.12, managed with `uv`.
- **`obsidian-vault-tautologia-ontologica/`** — Obsidian vault (PT-BR). 42 thesis concepts. Loaded into Neo4j as `thesis` vault.
- **`load-vaults/`** — Vault loader scripts. Parses Obsidian markdown → Neo4j + Milvus.
- **`marvin_ops.py`** — CI orchestrator. Sync, audit, improve. Zero LLM tokens.

### Build & Run

```bash
cd mcp-server
uv sync
uv run python marvin_server.py              # production (stdio)
uv run fastmcp run marvin_server.py --reload  # dev (auto-reload)
```

### Architecture

Single server (`marvin_server.py`) with 6 backend modules:

| Module | Backend |
|--------|---------|
| `ontology.py` | Neo4j — knowledge graph |
| `memory.py` | Milvus + OpenAI — episodic memory (L2/L3 only, no L1 per HCC) |
| `docs_backend.py` | Filesystem — local markdown docs |
| `web_to_docs_backend.py` | httpx + BS4 — web → markdown → docs/ |
| `prompt_engineer_backend.py` | Transformer-Driven Prompt Architect framework |
| `system_design_backend.py` | Mermaid.js diagrams |

**Middleware:** `RetrieveBeforeActMiddleware` blocks write tools unless retrieval happened first. Returns `ToolError` for self-correction.

### Knowledge Graph — Edge Types

10 semantic edge types via `relation_type` param in `link` and `expand`:

| Type | Direction | Meaning |
|------|-----------|---------|
| `RELATES_TO` | Symmetric | General association (default) |
| `CONTRADICTS` | Symmetric | Mutual opposition |
| `IMPLEMENTS` | Directional | Concrete realization of abstract |
| `PROVES` | Directional | Evidence or demonstration |
| `REQUIRES` | Directional | Dependency / precondition |
| `EXTENDS` | Directional | Specialization or enhancement |
| `ENABLES` | Directional | Makes possible |
| `EXEMPLIFIES` | Directional | Instance or illustration |
| `COMPOSES` | Directional | Part-of / building block |
| `EVOLVES_FROM` | Directional | Historical lineage |

Symmetric: A→B auto-creates B→A same type. Directional: A→B creates B→A as `RELATES_TO` for traversability.

### Key Implementation Details

- All credentials via `.env` (see `.env.example`)
- Filesystem writes confined to `docs/` and `diagrams/` via `_safe_path()`
- Non-destructive graph ops: MERGE not DELETE
- Bidirectional edges enforced: every A→B has B→A
- `log_decision` is async fire-and-forget (daemon thread)

### CI Pipeline (marvin-ops)

| Trigger | Pipeline |
|---------|----------|
| PR | sync + audit |
| Push to main | sync + audit + improve |
| Weekly schedule | sync + audit + improve |
| workflow_dispatch | user picks |

Self-audit compares code AST against KG claims. Zero LLM tokens — pure set operations.
