# CLAUDE.md

## Foundational Rule — Use the System Before Acting

Two things to check before doing anything:

**1. Retrieve first** — before writing, editing, or generating ANY code, config, or infrastructure:
- `retrieve` → Milvus semantic search across ontology, episodic memory, and docs
- Deep-dive if needed → `get_concept`, `traverse`, `get_doc`
- Fetch if missing → `fetch_url`/`save_doc`/`research_topic` BEFORE proceeding
- Only then act — with verified context, not training weights

The MCP server enforces this via the Milvus Gate (`RetrieveBeforeActMiddleware`): ALL Neo4j access is blocked unless a Milvus tool was called first. Enforce it on yourself for host tool actions too.

**2. Orchestrate first** — before running a multi-step workflow manually, check if it matches a chain:

| Trigger words | Chain | Steps |
|---------------|-------|-------|
| sync, vault, audit | `sync_and_audit` | sync_vaults → audit_code → review → self_improve |
| improve, refactor, tdd | `tdd_improve` | tdd → tests → green → improve → apply → green |
| full improve, full cycle | `full_improvement` | full TDD + improve + verify + knowledge check |
| research, docs | `research` | rank_urls → filter → research_topic |
| prompt, generate prompt | `prompt_lifecycle` | generate → audit → refine |
| enrich, knowledge gap | `code_to_knowledge` | improve_code → find gaps → retrieve → expand |

Call `orchestrate` with the goal. Don't reinvent the sequence manually.

## Session Start

Call `stats` for a live system overview. Marvin's identity prompt is built dynamically from the knowledge graph at startup via `self_description` and cached in Milvus — no static file.

## Workspace

- **`mcp-server/`** — Marvin. Single unified MCP server (44 tools, 9 backends). FastMCP 3.x, Python 3.12, managed with `uv`.
  - `backends/` — 9 backend modules (Python package with `__init__.py`)
  - `tests/` — 314 tests (pytest)
  - `scripts/` — utility scripts (update_tool_list, rebuild_docs, etc.)
- **`vaults/`** — Obsidian vaults loaded into Neo4j via Cognee.
  - `thesis-ptbr/` — Tautologia Ontologica (PT-BR)
  - `thesis-en/` — Thesis (English)
  - `implementation-ptbr/` — Implementation notes (PT-BR)
  - `implementation-en/` — Implementation notes (English)
- **`docs/`** — Fetched reference docs (67 markdown files)
- **`diagrams/`** — Saved Mermaid diagrams
- **`load-vaults/`** — Cognee-based KG extraction. `cognify_vaults.py` → Neo4j + LanceDB.

### Build & Run

```bash
cd mcp-server
uv sync
uv run python marvin_server.py              # production (stdio)
uv run fastmcp run marvin_server.py --reload  # dev (auto-reload)
```

### Architecture

Single server (`marvin_server.py`) with 9 backend modules in `backends/`:

| Module | Backend |
|--------|---------|
| `backends/ontology.py` | Neo4j — knowledge graph |
| `backends/memory.py` | Milvus + OpenAI — episodic memory (L2/L3 only, no L1 per HCC) |
| `backends/docs_backend.py` | Filesystem — local markdown docs |
| `backends/web_to_docs_backend.py` | httpx + BS4 — web → markdown → docs/ |
| `backends/prompt_engineer_backend.py` | Transformer-Driven Prompt Architect framework |
| `backends/system_design_backend.py` | Mermaid.js diagrams |
| `backends/code_improvement_backend.py` | AST chunking + Milvus vector walk (improve_code, tdd) |
| `backends/orchestrator_backend.py` | Goal → execution plan (6 tool chains) |
| `backends/ops_backend.py` | Vault sync, self-audit, self-improve (migrated from marvin_ops.py) |

<!-- AUTO:TOOLS:START -->
## Marvin's Tools (44 total)

| Tool | Tier | Description |
|------|------|-------------|
| `retrieve` | Milvus (sets gate) | Unified retrieval across ontology, episodic memory, and docs. |
| `get_concept` | Neo4j Read (gated) | Get a concept with full content and all relations from the ontology. |
| `traverse` | Neo4j Read (gated) | Walk the knowledge graph from a concept, returning its neighborhood. |
| `why_exists` | Neo4j Read (gated) | Explain why a concept exists in the ontology — edge reasoning. |
| `list_concepts` | Overview (ungated) | List all concept names in the knowledge graph, grouped by vault. |
| `get_memory` | Milvus (sets gate) | Deep-dive into episodic memory — HCC prefetching (L2/L3 → context). |
| `set_aliases` | Write (gated) | Set English aliases for a concept. Enables cross-language search. |
| `batch_set_aliases` | Write (gated) | Set aliases for multiple concepts at once. |
| `log_decision` | Always Allowed | Record a decision to episodic memory (L2 Knowledge). Fire-and-forget — returns immediately. |
| `log_session` | Always Allowed | Record a session summary to episodic memory (L3 Wisdom). |
| `expand` | Write (gated) | Add a new concept or relation to the knowledge graph. |
| `link` | Write (gated) | Create a direct relation between two existing concepts. |
| `auto_link` | Write (gated) | Scan concept content for references to other concepts and auto-create links. |
| `ensure_bidirectional` | Write (gated) | For every A→B edge, ensure B→A also exists. |
| `propose_schema_change` | Always Allowed | Propose a schema change to Neo4j or Milvus. |
| `execute_schema_change` | Write (gated) | Execute a previously proposed schema change. |
| `search_docs` | Milvus (sets gate) | Search local documentation files for a keyword or phrase. |
| `list_docs` | Overview (ungated) | List all available local documentation files. |
| `get_doc` | Overview (ungated) | Read a local documentation file. |
| `fetch_url` | Always Allowed | Fetch a webpage and return as markdown. |
| `save_doc` | Write (gated) | Fetch a webpage and save as local documentation. |
| `rank_urls` | Always Allowed | Probe URLs and rank them by documentation quality BEFORE fetching. |
| `crawl_docs` | Write (gated) | Crawl a documentation site and save pages as local docs. |
| `research_topic` | Write (gated) | Fetch multiple URLs, merge into a single consolidated doc with bibliography. |
| `generate_prompt` | Write (gated) | Generate a structured prompt using the Prompt Architect framework. |
| `refine_prompt` | Write (gated) | Refine an existing prompt based on feedback. |
| `audit_prompt` | Always Allowed | Audit a prompt against the Prompt Architect framework. |
| `generate_diagram` | Write (gated) | Generate a Mermaid.js system design diagram. |
| `judge_diagram` | Always Allowed | Review a Mermaid.js diagram for correctness and quality. |
| `save_diagram` | Write (gated) | Save a mermaid diagram to diagrams/. |
| `list_diagrams` | Overview (ungated) | List all saved mermaid diagrams. |
| `get_diagram` | Overview (ungated) | Read a saved mermaid diagram. |
| `inspect_schemas` | Overview (ungated) | Show current schemas for Neo4j and Milvus. |
| `stats` | Overview (ungated) | Quick overview of the entire knowledge system. |
| `self_description` | Overview (ungated) | Rebuild Marvin's identity prompt from the knowledge graph and cache it. |
| `get_user_score` | Always Allowed | Look up WhatsApp user politeness scores from the conversation database. |
| `refine_plan` | Milvus (sets gate) | Contrast a plan draft against Milvus prior art — tautological refinement. |
| `save_plan` | Write (gated) | Upsert a plan into the plans collection in Milvus. |
| `improve_code` | Milvus (sets gate) | Contrast a code file against all Milvus knowledge — tautological code review. |
| `tdd` | Milvus (sets gate) | Code + Milvus knowledge → structured context for test generation. |
| `orchestrate` | Milvus (sets gate) | Goal → structured execution plan. LLM-agnostic orchestration. |
| `sync_vaults` | Write (gated) | Cognify vaults → Neo4j + LanceDB → Milvus vector sync. |
| `audit_code` | Neo4j Read (gated) | Self-audit: compare code AST against knowledge graph claims. |
| `self_improve` | Write (gated) | Deterministic self-improvement: audit → fix drift → log to Milvus. |

### Tier Summary

| Tier | Count | Tools |
|------|-------|-------|
| **Milvus (sets gate)** | 7 | `get_memory`, `improve_code`, `orchestrate`, `refine_plan`, `retrieve`, `search_docs`, `tdd` |
| **Overview (ungated)** | 8 | `get_diagram`, `get_doc`, `inspect_schemas`, `list_concepts`, `list_diagrams`, `list_docs`, `self_description`, `stats` |
| **Neo4j Read (gated)** | 4 | `audit_code`, `get_concept`, `traverse`, `why_exists` |
| **Write (gated)** | 17 | `auto_link`, `batch_set_aliases`, `crawl_docs`, `ensure_bidirectional`, `execute_schema_change`, `expand`, `generate_diagram`, `generate_prompt`, `link`, `refine_prompt`, `research_topic`, `save_diagram`, `save_doc`, `save_plan`, `self_improve`, `set_aliases`, `sync_vaults` |
| **Always Allowed** | 8 | `audit_prompt`, `fetch_url`, `get_user_score`, `judge_diagram`, `log_decision`, `log_session`, `propose_schema_change`, `rank_urls` |

### Backends (9 modules)

| Module | Description |
|--------|-------------|
| `ontology.py` | Ontology backend — Python library wrapping Neo4j. |
| `memory.py` | Memory backend — Python library wrapping Milvus. |
| `docs_backend.py` | Docs backend — Python library for searching/browsing local markdown docs. |
| `web_to_docs_backend.py` | Web-to-docs backend — Fetch websites and convert to local markdown. |
| `prompt_engineer_backend.py` | Prompt engineer backend — Transformer-Driven Prompt Architect. |
| `system_design_backend.py` | System design backend — Mermaid.js diagram generation and review. |
| `code_improvement_backend.py` | Code improvement backend — contrast code against Milvus knowledge. |
| `orchestrator_backend.py` | Orchestrator backend — goal-driven tool chain planner. |
| `ops_backend.py` | Ops backend — vault sync, self-audit, and self-improvement. |

### Orchestrator Chains

| Chain | Triggers | Steps | Description |
|-------|----------|-------|-------------|
| `tdd_improve` | improve, refactor, tdd | 7 | TDD-guarded code improvement: lock behavior with tests, improve code, verify tests still pass |
| `research` | research, docs, documentation | 3 | Knowledge-enriched research: rank URLs, fetch the good ones, consolidate into a doc |
| `prompt_lifecycle` | prompt, generate prompt, write prompt | 4 | Generate, audit, and refine a prompt using the Prompt Architect framework |
| `code_to_knowledge` | enrich, knowledge gap, missing concept | 4 | Review code against KB, then enrich the ontology with missing concepts |
| `full_improvement` | full improve, full cycle, complete improvement | 9 | Full file improvement cycle: TDD guard → improve → verify → check for new knowledge |
| `sync_and_audit` | sync, vault, audit | 4 | Sync all vaults to Milvus, then audit code vs KG for drift |

### Milvus Gate Middleware

All Neo4j reads and write tools are **blocked** unless a Milvus tier tool was called first in the session. Architectural enforcement (P=0), not prompt bias.
<!-- AUTO:TOOLS:END -->

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
