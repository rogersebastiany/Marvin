# CLAUDE.md

## Foundational Rule — Retrieve Before Act

Before writing, editing, or generating ANY code, config, or infrastructure:

1. `retrieve` first — Milvus semantic search across ontology, episodic memory, and docs
2. Deep-dive if needed — `get_concept` or `traverse` for KG nodes, `get_doc` for full doc content
3. Fetch if missing — if `retrieve` returns nothing, call `fetch_url`/`save_doc`/`research_topic` BEFORE proceeding
4. Only then act — with verified context, not training weights

This applies to every technology: Python, FastMCP, Neo4j, Milvus, httpx, Terraform, AWS, Docker — no exceptions. Correct output from weights is luck, not construction.

The MCP server enforces this architecturally via the Milvus Gate (`RetrieveBeforeActMiddleware`): ALL Neo4j access (reads AND writes) is blocked unless `retrieve`, `get_memory`, or `search_docs` was called first. You must also enforce it on yourself for host tool actions (file edits, bash commands, code generation).

## Session Start

Call `stats` for a live system overview. Marvin's identity prompt is built dynamically from the knowledge graph at startup via `self_description` and cached in Milvus — no static file.

## Workspace

- **`mcp-server/`** — Marvin. Single unified MCP server (44 tools, 9 backends). FastMCP 3.x, Python 3.12, managed with `uv`.
- **`obsidian-vault-tautologia-ontologica/`** — Obsidian vault (PT-BR). Thesis concepts. Loaded into Neo4j via Cognee.
- **`load-vaults/`** — Cognee-based KG extraction. `cognify_vaults.py` → Neo4j + LanceDB.
- **`marvin_ops.py`** — Local CLI for sync/audit/improve. Logic also available as MCP tools via `ops_backend.py`.

### Build & Run

```bash
cd mcp-server
uv sync
uv run python marvin_server.py              # production (stdio)
uv run fastmcp run marvin_server.py --reload  # dev (auto-reload)
```

### Architecture

Single server (`marvin_server.py`) with 9 backend modules:

| Module | Backend |
|--------|---------|
| `ontology.py` | Neo4j — knowledge graph |
| `memory.py` | Milvus + OpenAI — episodic memory (L2/L3 only, no L1 per HCC) |
| `docs_backend.py` | Filesystem — local markdown docs |
| `web_to_docs_backend.py` | httpx + BS4 — web → markdown → docs/ |
| `prompt_engineer_backend.py` | Transformer-Driven Prompt Architect framework |
| `system_design_backend.py` | Mermaid.js diagrams |
| `code_improvement_backend.py` | AST chunking + Milvus vector walk (improve_code, tdd) |
| `orchestrator_backend.py` | Goal → execution plan (6 tool chains) |
| `ops_backend.py` | Vault sync, self-audit, self-improve (migrated from marvin_ops.py) |

**Middleware (Milvus Gate):** `RetrieveBeforeActMiddleware` blocks Neo4j reads and write tools unless a Milvus retrieval tool was called first. 5-tier classification: Milvus (7 tools, set gate), Overview (8, ungated), Neo4j Read (4, gated), Write (17, gated), Always Allowed (8).

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

### Orchestrator Chains

The `orchestrate` tool plans tool execution sequences any MCP client can follow:

| Chain | Flow |
|-------|------|
| `tdd_improve` | tdd → write tests → green → improve_code → apply → green → issue |
| `full_improvement` | tdd → tests → green → improve → apply → green → tdd again → delta → issue |
| `research` | rank_urls → filter 60+ → research_topic |
| `prompt_lifecycle` | generate_prompt → audit_prompt → if <7 → refine_prompt |
| `code_to_knowledge` | improve_code → find gaps → retrieve → expand |
| `sync_and_audit` | sync_vaults → audit_code → review → self_improve |
