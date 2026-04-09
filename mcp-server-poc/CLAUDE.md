# MCP Server POC

## Build & Run
```bash
uv sync                                  # install dependencies
uv run python server.py                  # docs server (stdio)
uv run python web_to_docs_server.py      # web-to-docs server (stdio)
uv run python prompt_engineer_server.py  # prompt engineer server (stdio)
uv run python system_design_server.py    # system design server (stdio)
```

## Docker
```bash
docker build -t mcp-docs-server .
docker run -i --rm mcp-docs-server
```

## Architecture
- `server.py` — Docs search/browse over `docs/` directory
- `web_to_docs_server.py` — Fetch websites → markdown → save to `docs/`
- `prompt_engineer_server.py` — Generate/refine/audit prompts (Transformer-Driven Prompt Architect framework)
- `system_design_server.py` — Generate/judge Mermaid.js system design diagrams, saves to `diagrams/`
- `docs/` — Markdown documentation (sample Nexus platform docs + mermaid syntax refs)
- `diagrams/` — Saved mermaid diagram files (.mmd)
- `.cursor/mcp.json` — Cursor IDE config (all 4 servers, stdio via `uv run`)

## Server Primitives
| Server | Tools | Resources | Prompts |
|--------|-------|-----------|---------|
| docs-server | `search_docs`, `list_docs`, `get_doc_summary` | `docs://{filename}` | `explain_concept`, `onboarding_guide` |
| web-to-docs | `convert_url`, `save_as_doc`, `batch_convert`, `crawl_docs` | — | `research_and_answer`, `fetch_project_docs` |
| prompt-engineer | `generate_prompt`, `refine_prompt`, `audit_prompt` | — | `architect_prompt`, `improve_my_prompt` |
| system-design | `generate_diagram`, `judge_diagram`, `save_diagram`, `list_diagrams`, `get_diagram` | `diagrams://{filename}` | `design_system`, `review_architecture` |
