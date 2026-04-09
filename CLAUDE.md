# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Foundational Rule — Retrieve Before Act

This is the single most important rule in this repository. It overrides all defaults.

**Before writing, editing, or generating ANY code, config, or infrastructure**, you MUST:

1. **Check the knowledge graph** — call `get_concept`, `traverse`, or `retrieve` for relevant concepts
2. **Check local docs** — call `search_docs` for the technologies involved
3. **Fetch if missing** — if docs/ has nothing for the technology, call `fetch_url`/`save_doc`/`research_topic` to get it BEFORE proceeding
4. **Only then act** — with verified context from the ontology and docs, not from training weights

This applies to EVERYTHING: Python, FastMCP, Neo4j, Milvus, httpx, Terraform, AWS, Docker, Mermaid.js — any external technology. No exceptions. If you catch yourself about to write code without having checked, stop and retrieve first.

**Why this exists:** The core thesis of this project (Tautologia Ontológica) states that complete ontological context yields deterministic behavior. Relying on training weights instead of verified documentation is the exact anti-pattern this project exists to eliminate. Correct output from weights is luck, not construction.

The MCP server architecturally enforces this for Marvin tool calls via `RetrieveBeforeActMiddleware`. But you must also enforce it on yourself for all other work (file edits, bash commands, code generation).

## Workspace Overview

This workspace contains two projects:

- **`mcp-server/`** — Marvin, a single unified MCP server (32 tools) wrapping Neo4j (ontology), Milvus (episodic memory), local docs, prompt engineering, and system design diagrams. Built with FastMCP 3.x.
- **`obsidian-vault-tautologia-ontologica/`** — An Obsidian knowledge vault (Portuguese) with 45 concept notes on "Tautologia Ontológica" — the thesis that complete ontological context yields deterministic LLM behavior. Loaded into Neo4j as the `thesis` vault.

## MCP Server

### Build & Run

```bash
cd mcp-server
uv sync                                        # install dependencies
uv run python marvin_server.py                  # production (stdio)
uv run fastmcp run marvin_server.py --reload    # dev mode (auto-reload on file changes)
```

### Architecture

Single MCP server (`marvin_server.py`) with 6 backend modules:

| Module | Backend | What It Does |
|--------|---------|-------------|
| `ontology.py` | Neo4j | Knowledge graph — concepts, relations, traversal, auto-link, bidirectionality |
| `memory.py` | Milvus + OpenAI | Episodic memory — tool calls (L1), decisions (L2), sessions (L3) |
| `docs_backend.py` | Filesystem | Search/browse local markdown docs (`docs/`) |
| `web_to_docs_backend.py` | httpx + BS4 | Fetch web → markdown → save to `docs/`. Includes `research_topic` (multi-URL → consolidated doc with bibliography) |
| `prompt_engineer_backend.py` | — | Transformer-Driven Prompt Architect framework (6 mandatory sections) |
| `system_design_backend.py` | Filesystem | Mermaid.js diagram generation/review (`diagrams/`) |

**Middleware:** `RetrieveBeforeActMiddleware` — architectural enforcement that blocks write/generate tools unless a retrieval tool has been called first in the session. Returns `ToolError` with instructions for self-correction.

**Data flow:** Agent needs info → retrieval tools (search_docs, retrieve, traverse) → not found → web-to-docs fetches and saves → now searchable → prompt-engineer generates optimized prompts → system-design generates/reviews diagrams.

### Key Implementation Details

- Python 3.12, managed with `uv` (see `pyproject.toml` and `uv.lock`)
- Dependencies: `fastmcp>=3.0.0`, `markdownify>=1.2.2`, `mcp[cli]>=1.4.1`, `neo4j>=6.1.0`, `openai>=2.31.0`, `pymilvus>=2.6.12`, `python-dotenv>=1.2.2`
- All credentials via environment variables (`.env` in project root, see `.env.example`)
- Filesystem writes confined to `docs/` and `diagrams/` via `_safe_path()` / `_safe_diagram_path()`
- Non-destructive graph ops: MERGE not DELETE. Agent-owned concepts (vault="agent") never overwritten
- Bidirectional edges: every A→B has B→A. Deterministic traversal from any direction

### Session Start — Mandatory KG Load

On the **first interaction of every session**, before responding to any user request, you MUST load the full knowledge graph context from Marvin:

1. Call `stats` for a system overview
2. Call `traverse` from root concepts (`Tautologia Ontológica`, `Determinismo`, `MCP`) with `hops=4`
3. Call `retrieve` with a broad query to load recent episodic memory

The agent cannot reason about an ontology it hasn't seen. Do not skip this.

### Production Path (documented in README and obsidian vault)

POC → AWS deployment: ECS Fargate + ALB + WAF + S3/KMS + Secrets Manager + Entra ID JWT auth. Key changes needed: MCP Gateway (auth proxy), S3 storage backend, tenant isolation, audit middleware, IaC.
