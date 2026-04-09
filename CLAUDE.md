# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Workspace Overview

This workspace contains two projects:

- **`mcp-server-poc/`** — A proof-of-concept of 4 custom MCP (Model Context Protocol) servers in Python, built with FastMCP. Designed to demonstrate Cursor IDE productivity through custom MCP tooling for private documentation, prompt engineering, system design diagrams, and web-to-docs conversion.
- **`obsidian-vault-tautologia-ontologica/`** — An Obsidian knowledge vault (in Portuguese) exploring "Tautologia Ontológica" — a framework arguing that complete ontological context (Spec + BDD + TDD + ADR + Observability + MCP + RAG) yields deterministic LLM behavior. Contains interconnected concept notes on ML fundamentals, MCP infrastructure, and security.

## MCP Server POC

### Build & Run

```bash
cd mcp-server-poc
uv sync                                  # install dependencies
uv run python server.py                  # docs server (stdio)
uv run python web_to_docs_server.py      # web-to-docs server (stdio)
uv run python prompt_engineer_server.py  # prompt engineer server (stdio)
uv run python system_design_server.py    # system design server (stdio)
```

Docker (docs server only):
```bash
docker build -t mcp-docs-server .
docker run -i --rm mcp-docs-server
```

### Architecture

Four MCP servers that chain together, all using FastMCP and communicating via stdio:

1. **`server.py`** (docs-server) — Searches/browses local markdown in `docs/`. The knowledge base. Path-traversal protection via `_safe_path()`.
2. **`web_to_docs_server.py`** (web-to-docs) — Fetches websites, converts HTML→markdown (via `markdownify` + `BeautifulSoup`), saves to `docs/`. Includes a crawler (`crawl_docs`) that follows same-prefix links up to 100 pages. **Note:** uses `verify=False` on httpx — must be fixed for production.
3. **`prompt_engineer_server.py`** (prompt-engineer) — Generates/refines/audits prompts using the "Transformer-Driven Prompt Architect" framework (6 mandatory sections). Auto-discovers all tools from sibling servers at import time via `asyncio.run()` and injects the catalog into every generated prompt.
4. **`system_design_server.py`** (system-design) — Generates/judges Mermaid.js diagrams. Loads `docs/mermaid-*.md` syntax references at startup. Scores diagrams on 4 dimensions (syntax, completeness, clarity, best practices). Saves `.mmd` files to `diagrams/`.

**Data flow:** Agent needs info → searches local docs → not found → web-to-docs fetches and saves → now searchable → prompt-engineer generates optimized prompts → system-design generates/reviews diagrams.

### Key Implementation Details

- Python 3.12, managed with `uv` (see `pyproject.toml` and `uv.lock`)
- Dependencies: `fastmcp>=3.0.0`, `markdownify>=1.2.2`, `mcp[cli]>=1.4.1`
- All servers expose MCP primitives: Tools, Resources (`docs://`, `diagrams://`), and Prompts
- `.cursor/mcp.json` configures all 4 servers for Cursor IDE auto-launch
- `prompt_engineer_server.py` imports the other 3 servers at module level to discover their tools — this creates a coupling where all servers must be importable when the prompt engineer starts
- Filesystem writes are confined to `docs/` and `diagrams/` via `_safe_path()` / `_safe_diagram_path()` helpers

### Production Path (documented in README and obsidian vault)

POC → AWS deployment: ECS Fargate + ALB + WAF + S3/KMS + Secrets Manager + Entra ID JWT auth. Key changes needed: MCP Gateway (auth proxy), S3 storage backend, tenant isolation, audit middleware, IaC.
