# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Foundational Rule — Retrieve Before Act

This is the single most important rule in this repository. It overrides all defaults.

**Before writing, editing, or generating ANY code, config, or infrastructure**, you MUST:

1. **`retrieve` first** — this is the single entry point for all search. It queries Milvus (semantic search) across ontology concepts, episodic memory, AND documentation simultaneously. Always start here.
2. **Deep-dive if needed** — use `get_concept` or `traverse` for specific KG nodes, `get_doc` for full doc content
3. **Fetch if missing** — if `retrieve` returns nothing for the technology, call `fetch_url`/`save_doc`/`research_topic` to get it BEFORE proceeding
4. **Only then act** — with verified context from Milvus search, not from training weights

**Milvus is the primary search layer.** All knowledge (concepts, docs, memory) is indexed there. Do NOT use `search_docs` as a first step — it's a filesystem fallback, not the primary path. `retrieve` covers everything `search_docs` does, plus semantic similarity.

This applies to EVERYTHING: Python, FastMCP, Neo4j, Milvus, httpx, Terraform, AWS, Docker, Mermaid.js — any external technology. No exceptions. If you catch yourself about to write code without having checked, stop and retrieve first.

**Why this exists:** The core thesis of this project (Tautologia Ontológica) states that complete ontological context yields deterministic behavior. Relying on training weights instead of verified documentation is the exact anti-pattern this project exists to eliminate. Correct output from weights is luck, not construction.

The MCP server architecturally enforces this for Marvin tool calls via `RetrieveBeforeActMiddleware`. But you must also enforce it on yourself for all other work (file edits, bash commands, code generation).

## Workspace Overview

This workspace contains two projects:

- **`mcp-server/`** — Marvin, a single unified MCP server (31 tools) wrapping Neo4j (ontology), Milvus (episodic memory), local docs, prompt engineering, and system design diagrams. Built with FastMCP 3.x.
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
| `memory.py` | Milvus + OpenAI | Episodic memory — decisions (L2), sessions (L3). L1 tool traces are transient context-window memory per HCC |
| `docs_backend.py` | Filesystem | Search/browse local markdown docs (`docs/`) |
| `web_to_docs_backend.py` | httpx + BS4 | Fetch web → markdown → save to `docs/`. Includes `research_topic` (multi-URL → consolidated doc with bibliography) |
| `prompt_engineer_backend.py` | — | Transformer-Driven Prompt Architect framework (6 mandatory sections) |
| `system_design_backend.py` | Filesystem | Mermaid.js diagram generation/review (`diagrams/`) |

**Middleware:** `RetrieveBeforeActMiddleware` — architectural enforcement that blocks write/generate tools unless a retrieval tool has been called first in the session. Returns `ToolError` with instructions for self-correction.

**Data flow:** Agent needs info → `retrieve` (Milvus semantic search across all knowledge) → not found → web-to-docs fetches and saves → now indexed in Milvus → prompt-engineer generates optimized prompts → system-design generates/reviews diagrams.

### Key Implementation Details

- Python 3.12, managed with `uv` (see `pyproject.toml` and `uv.lock`)
- Dependencies: `fastmcp>=3.0.0`, `markdownify>=1.2.2`, `mcp[cli]>=1.4.1`, `neo4j>=6.1.0`, `openai>=2.31.0`, `pymilvus>=2.6.12`, `python-dotenv>=1.2.2`
- All credentials via environment variables (`.env` in project root, see `.env.example`)
- Filesystem writes confined to `docs/` and `diagrams/` via `_safe_path()` / `_safe_diagram_path()`
- Non-destructive graph ops: MERGE not DELETE. Agent-owned concepts (vault="agent") never overwritten
- Bidirectional edges: every A→B has B→A. Deterministic traversal from any direction
- `log_decision` is async fire-and-forget (daemon thread) — no latency hit. `log_tool_call` removed: L1 is transient working memory per HCC

### Knowledge Graph — Relationship Types

The ontology supports 10 semantic edge types. Use `relation_type` param in `link` and `expand`.

| Type | Direction | Meaning | Example |
|------|-----------|---------|---------|
| `RELATES_TO` | Symmetric | General association (default) | MCP ↔ Marvin |
| `CONTRADICTS` | Symmetric | Mutual opposition | Alucinação ↔ Determinismo |
| `IMPLEMENTS` | Directional | Concrete realization of abstract concept | Marvin → Tautologia Ontológica |
| `PROVES` | Directional | Evidence or demonstration | Self-Referential Proof → TO |
| `REQUIRES` | Directional | Dependency / precondition | Determinismo → Ontologia |
| `EXTENDS` | Directional | Specialization or enhancement | Enforcement Arquitetural → Bias |
| `ENABLES` | Directional | Makes possible | Neo4j → Marvin |
| `EXEMPLIFIES` | Directional | Instance or illustration | Tool Tautológica → TO |
| `COMPOSES` | Directional | Part-of / building block | Ontologia → TO |
| `EVOLVES_FROM` | Directional | Historical lineage | Marvin → Cadeia de Servers |

**Symmetric** types: A→B auto-creates B→A with same type. **Directional** types: A→B does NOT imply B→A — a generic `RELATES_TO` reverse is created instead for traversability.

### Session Start — Mandatory KG Load

On the **first interaction of every session**, before responding to any user request, you MUST:

1. Call `stats` for a system overview
2. Call `list_concepts` to learn every node name in the graph

That's it. The graph is a lookup tool — use `get_concept`, `traverse`, or `retrieve` on demand when you actually need content. Do not bulk-load the graph into the context window.

### Tool Dispatch Table

| Trigger | Tool(s) | Rule |
|---|---|---|
| Session starts | `stats` + `list_concepts` | [RULE_RETRIEVE] |
| Any question from user | `retrieve` first (Milvus semantic search) | [RULE_RETRIEVE] |
| About to write/edit code | `retrieve` for the technology → `get_doc` for full content | [RULE_FETCH] |
| retrieve returns nothing | `fetch_url`/`save_doc`/`research_topic` to ingest, then `retrieve` again | [RULE_FETCH] |
| Multiple candidate URLs | `rank_urls` THEN `research_topic` | [RULE_FETCH] |
| Need deep detail on a concept | `get_concept` | [RULE_RETRIEVE] |
| Need concept neighborhood | `traverse` | [RULE_RETRIEVE] |
| Choosing between alternatives | `log_decision` | [RULE_LOG] |
| Session ending | `log_session` | [RULE_LOG] |
| Discovered new concept | `expand` (retrieve first!) | [RULE_RETRIEVE] |
| Found relation between concepts | `link` with typed `relation_type` (retrieve first!) | [RULE_RETRIEVE] |
| Need to change graph schema | `propose_schema_change` → user approval → `execute_schema_change` | [RULE_QUALITY] |
| Need a structured prompt | `generate_prompt` → review → `refine_prompt` | [RULE_QUALITY] |
| Evaluating a prompt | `audit_prompt` | [RULE_QUALITY] |
| Need a system diagram | `generate_diagram` → `judge_diagram` → `save_diagram` | [RULE_QUALITY] |

### Constraints

1. **NEVER answer from weights alone** — if `retrieve` returns nothing, either fetch the missing docs or say "not found". Do NOT generate from training weights.
2. **NEVER skip retrieval before writes** — the middleware will reject it, but don't even try.
3. **NEVER execute schema changes without proposal + human approval.**
4. **NEVER use probabilistic language about ontology state** — say "found" or "not found", never "probably" or "I think".
5. **NEVER skip logging decisions** — every choice between alternatives gets `log_decision`. It's async, no excuse.
6. **NEVER write code for a technology without docs** — if `retrieve` returns nothing for the technology, `save_doc`/`research_topic` first.

### Few-Shot Examples

**Example 1: Code change request**
```
Input: "Add a CloudWatch alarm to monitoring.tf"

WRONG: Immediately edit using training knowledge
CORRECT:
  1. retrieve("terraform cloudwatch alarm")  ← Milvus searches concepts + docs + memory
  2. retrieve returns nothing for terraform → docs missing
  3. save_doc(url, "terraform-cloudwatch-alarm.md")
  4. get_doc("terraform-cloudwatch-alarm.md")
  5. NOW edit with verified docs
  6. log_decision(...)
```

**Example 2: Concept question**
```
Input: "What is Determinismo?"

WRONG: Answer from weights about determinism
CORRECT:
  1. retrieve("Determinismo")  ← Milvus returns concept + related docs + similar past queries
  2. get_concept("Determinismo") → full content + typed edges (if needed for depth)
  3. Answer using ONLY retrieved content
```

### Production Path (documented in README and obsidian vault)

POC → AWS deployment: ECS Fargate + ALB + WAF + S3/KMS + Secrets Manager + Entra ID JWT auth. Key changes needed: MCP Gateway (auth proxy), S3 storage backend, tenant isolation, audit middleware, IaC.
