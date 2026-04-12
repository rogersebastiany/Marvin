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

Single server (`marvin_server.py`) wrapping 9 backend modules in `backends/`:

| Module | Backend | What It Does |
|--------|---------|-------------|
| `backends/ontology.py` | Neo4j | Knowledge graph — concepts, relations, traversal, auto-link, bidirectionality |
| `backends/memory.py` | Milvus + OpenAI | Episodic memory — decisions (L2), sessions (L3), plans, vector search |
| `backends/docs_backend.py` | Filesystem | Search/browse local markdown docs (`docs/`) |
| `backends/web_to_docs_backend.py` | httpx + BS4 | Fetch web → markdown → save to `docs/` |
| `backends/prompt_engineer_backend.py` | — | Transformer-Driven Prompt Architect framework |
| `backends/system_design_backend.py` | Filesystem | Mermaid.js diagram generation/review (`diagrams/`) |
| `backends/code_improvement_backend.py` | Milvus | AST chunking + vector walk (improve_code, tdd) |
| `backends/orchestrator_backend.py` | Milvus | Goal → execution plan, 6 tool chains |
| `backends/ops_backend.py` | Neo4j + Milvus + LanceDB | Vault sync, self-audit, self-improve |

<!-- AUTO:TOOLS:START -->
## Marvin's Tools (46 total)

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
| `extract_keywords` | Write (gated) | Extract keywords from a doc for knowledge graph densification. |
| `classify_keywords` | Milvus (sets gate) | Classify extracted keywords against Milvus into 3 tiers. |
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
| **Milvus (sets gate)** | 8 | `classify_keywords`, `get_memory`, `improve_code`, `orchestrate`, `refine_plan`, `retrieve`, `search_docs`, `tdd` |
| **Overview (ungated)** | 8 | `get_diagram`, `get_doc`, `inspect_schemas`, `list_concepts`, `list_diagrams`, `list_docs`, `self_description`, `stats` |
| **Neo4j Read (gated)** | 4 | `audit_code`, `get_concept`, `traverse`, `why_exists` |
| **Write (gated)** | 18 | `auto_link`, `batch_set_aliases`, `crawl_docs`, `ensure_bidirectional`, `execute_schema_change`, `expand`, `extract_keywords`, `generate_diagram`, `generate_prompt`, `link`, `refine_prompt`, `research_topic`, `save_diagram`, `save_doc`, `save_plan`, `self_improve`, `set_aliases`, `sync_vaults` |
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
| `research` | research, docs, documentation | 8 | Knowledge-enriched research: rank URLs, fetch, consolidate, extract keywords, fill knowledge gaps, sync |
| `prompt_lifecycle` | prompt, generate prompt, write prompt | 4 | Generate, audit, and refine a prompt using the Prompt Architect framework |
| `code_to_knowledge` | enrich, knowledge gap, missing concept | 4 | Review code against KB, then enrich the ontology with missing concepts |
| `full_improvement` | full improve, full cycle, complete improvement | 9 | Full file improvement cycle: TDD guard → improve → verify → check for new knowledge |
| `sync_and_audit` | sync, vault, audit | 4 | Sync all vaults to Milvus, then audit code vs KG for drift |
| `densify` | densify, densification, keywords | 5 | Knowledge graph densification: extract keywords from docs, classify against Milvus, enrich matches, research gaps, sync |

### Milvus Gate Middleware

All Neo4j reads and write tools are **blocked** unless a Milvus tier tool was called first in the session. Architectural enforcement (P=0), not prompt bias.
<!-- AUTO:TOOLS:END -->

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

- `../docs/` — Fetched reference docs (67 markdown files, at project root)
- `../diagrams/` — Saved Mermaid.js `.mmd` files (at project root)
- `../vaults/` — Obsidian vaults (Cognee input, at project root)

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
