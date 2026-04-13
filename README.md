# Marvin

An MCP server that implements the **Ontological Tautology** thesis: 47 tautological tools over a knowledge graph, so that any LLM agent connected to it operates deterministically by construction — not by prompt engineering.

Named after Marvin the Paranoid Android — because when you know everything, existence is predictably depressing.

## The Problem

LLMs are probabilistic. Given the same input they produce different outputs. They hallucinate, they drift across versions and providers. The bigger the model, the worse the drift.

The standard response is "just use RAG" or "add guardrails." These are patches. They don't address the root cause.

**The root cause is not the model. It is the context.**

## The Thesis

**Ontological Tautology** (Tautologia Ontologica) argues that LLM non-determinism is a consequence of incomplete context, not an intrinsic property of the model. When three conditions hold:

1. The **ontology** is complete — every domain concept is defined and connected
2. The **tools** are tautological — given valid input, exactly one correct output exists
3. The **architecture enforces** tool usage — `P(action without tool) = 0`, not "low"

Then: **Complete Ontology -> Tautology -> Determinism**

The LLM becomes a routing function — it selects which tool to call with which parameters. Its "creativity" and "hallucination potential" get constrained to zero because every answer comes from the ontology, not from training weights.

### Tautological Tools

A tool is **tautological** when its I/O contract is complete and unambiguous:

```
for all valid_input in domain(tool): |{correct_output}| = 1
```

It doesn't generate — it retrieves or computes. It either returns the correct answer or explicitly reports that it cannot answer. There is no third option.

### Why This Matters

The DFAH paper (Khatchadourian, 2024) found r = -0.11 correlation between determinism and accuracy — they're independent dimensions. But this applies to **general tools**. When tools are **tautological**, determinism *implies* accuracy because the tool's I/O contract guarantees correctness. The null correlation applies to the general case; Marvin operates in the constrained case.

## Three Databases

Marvin's knowledge lives in three databases, each with a distinct role:

### Neo4j — Knowledge Graph (Ontology)

791 concepts, 2322 typed edges across 10 semantic relation types. This is the ontology — the structured representation of the domain. Every concept has typed, bidirectional edges (every A->B has B->A). Extracted by [Cognee](https://github.com/topoteretes/cognee) with a custom `Concept(DataPoint)` graph model from Obsidian vaults.

### Milvus — Vector Database (Episodic Memory + Semantic Search)

7 collections, OpenAI `text-embedding-3-small` (1536 dim), COSINE similarity:

| Collection | What it stores |
|------------|---------------|
| `concepts` | 791 concept vectors + names + summaries (synced from LanceDB) |
| `doc_chunks` | Document chunk vectors from vault extraction (synced from LanceDB) |
| `decisions` | L2 Knowledge — decisions with reasoning and outcome |
| `sessions` | L3 Wisdom — session summaries and lessons learned |
| `plans` | Execution plans (retrievable via `refine_plan`) |
| `self_description` | Cached identity prompt (built from KG at startup) |
| `tool_calls` | Reserved (L1 not persisted per HCC design) |

Milvus is the retrieval layer. Every action starts here — semantic search across ontology, episodic memory, and docs in a single call.

### LanceDB — Cognee's Vector Store

Cognee's internal vector store, populated during vault extraction. Vectors are synced to Milvus via `sync_vaults` — zero OpenAI embedding cost for the transfer. LanceDB is the source of truth for concept and document chunk vectors; Milvus is the queryable replica.

## Four Layers of Enforcement

The thesis distinguishes between **prompt bias** (soft constraint, P > 0) and **architectural enforcement** (hard constraint, P = 0). Marvin implements enforcement at four layers — from the MCP server up to the host agent. Each layer is independently toggleable.

### Layer 1 — MCP Server Identity (Dynamic from KG)

Marvin's `instructions` field — what the MCP client sees as the server's system prompt — is **not a static string**. It is built dynamically from the knowledge graph at startup:

1. On startup, check Milvus `self_description` collection for a cached identity prompt
2. Cache hit -> use it. Cache miss -> query Neo4j for all thesis vault concepts, introspect the tool catalog from code, assemble the full identity prompt, cache it in Milvus
3. The identity includes: thesis foundations, HCC memory model, tool catalog with tiers, edge types, execution pattern, constraints

This means Marvin's identity **evolves with the knowledge graph**. Add a concept to the thesis vault, call `self_description`, and the server's instructions update. No code change needed.

### Layer 2 — MCP Middlewares (P=0, Server-Side)

Two FastMCP `Middleware` classes that intercept every tool call before execution. These are hard gates — the server raises `ToolError` and refuses to execute. No prompt can bypass them.

**Milvus Gate (`RetrieveBeforeActMiddleware`)**

All Neo4j reads (`get_concept`, `traverse`, `why_exists`) and all write tools (`expand`, `link`, `save_doc`, etc.) are **blocked** unless a Milvus-tier tool (`retrieve`, `get_memory`, `search_docs`) was called first in the session. This is the thesis in code: you must ground yourself in existing knowledge before acting on the graph.

```
Agent calls get_concept("Tautology") without prior retrieve
  -> ToolError: BLOCKED — requires Milvus retrieval before Neo4j access
```

Tool classification:

| Tier | Count | Effect |
|------|-------|--------|
| **Milvus (sets gate)** | 10 | Semantic search — sets the "grounded" flag |
| **Overview (ungated)** | 8 | Read-only metadata — no gate needed |
| **Neo4j Read (gated)** | 4 | Blocked until Milvus flag is set |
| **Write (gated)** | 18 | Blocked until Milvus flag is set |
| **Always Allowed** | 7 | Logging, audits, URL fetching |

**Orchestration Gate (`OrchestrationGateMiddleware`)**

Enrichment tools (`expand`, `link`, `auto_link`, `save_doc`, etc.) are **blocked** unless `orchestrate` was called first in the session. This ensures all graph mutations follow a planned chain — no ad-hoc writes from LLM impulse.

Three-tier classification within the gate:
- **AUTONOMOUS** — can be called anytime (retrieval, logging, orchestrate itself)
- **PLAN_AWARE** — require an active orchestration plan (enrichment + mutations)
- **PROVENANCE** — subset of PLAN_AWARE that also require `source_doc` (expand)

### Layer 3 — Claude Code Hooks (P=0, Client-Side)

Four shell scripts in `.claude/hooks/` that run on the host agent side (Claude Code). These enforce rules that the MCP server can't see — like which files the agent is allowed to edit.

**Session Start Hook** — Injects enforcement status into the agent's context at the start of every session. Shows which gates are enabled/disabled. Clears stale orchestration state from previous sessions.

**Pre-Tool Hook** — Fires before every Marvin MCP call. Writes an audit log entry (`mcp_audit.jsonl`) with timestamp, tool name, and input. This is infrastructure logging (like nginx access logs), not L1 memory — the agent never sees it.

**Post-Tool Hook** — Fires after every Marvin MCP call. Logs result previews to the audit log. Two special behaviors:
- When `orchestrate` succeeds, writes a session state file that the Edit Gate reads
- When `expand` is blocked for missing provenance, injects corrective feedback into the agent's context

**Edit Gate Hook** — The hardest gate. Core Marvin source files (`backends/*.py`, `marvin_server.py`) are **locked for editing** unless `orchestrate` was called first in the session. The agent physically cannot modify Marvin's code without first establishing an execution plan. Tests, scripts, docs, and config files are unprotected.

```
Agent tries to Edit backends/ontology.py without prior orchestrate
  -> BLOCKED: Editing core file 'ontology.py' requires an orchestration plan.
     This is architectural enforcement (P=0), not a suggestion.
```

### Layer 4 — CLAUDE.md (P>0, Prompt-Level)

The weakest layer — prompt instructions that guide behavior but can't prevent it. Used for patterns that don't have a clean architectural gate:
- "Retrieve before acting" (reinforces Layer 2 for host-side actions)
- "Use `orchestrate` for multi-step workflows" (reinforces Layer 3)
- Session start procedures, workspace conventions, tool documentation

This layer exists because some rules apply to the agent's *reasoning* (which tool to pick, when to log decisions) rather than to tool *execution* (which Layer 2 and 3 handle).

### Why Four Layers

Each layer catches what the others can't:

| What | Layer 1 (Identity) | Layer 2 (Middleware) | Layer 3 (Hooks) | Layer 4 (CLAUDE.md) |
|------|-------------------|---------------------|-----------------|-------------------|
| "Retrieve before Neo4j" | Instruction | **Hard gate** | Audit log | Reinforcement |
| "Plan before enrichment" | Instruction | **Hard gate** | State tracking | Reinforcement |
| "Plan before editing code" | — | — | **Hard gate** | Reinforcement |
| "Log decisions" | Instruction | — | — | Instruction |
| "Don't answer from weights" | Instruction | — | — | Instruction |
| Dynamic identity from KG | **Built from KG** | — | — | — |
| Audit trail | — | — | **Infrastructure log** | — |

## Architecture

```
Any MCP Client (Claude Code, Cursor, VS Code, etc.)
  |
  |  .claude/hooks/        <-- Layer 3: session start, pre/post tool, edit gate
  |  CLAUDE.md             <-- Layer 4: prompt-level instructions
  |
  +-- mcp-marvin (sole MCP server)
        |
        |  instructions        <-- Layer 1: dynamic identity built from KG
        |  middlewares          <-- Layer 2: Milvus Gate + Orchestration Gate
        |
        |  47 tools, 9 backends
        |
        +-- Neo4j          Knowledge graph (791 concepts, 2322 typed edges)
        +-- Milvus         Vector DB (7 collections, semantic search + memory)
        +-- LanceDB        Cognee's vector store (source for Milvus sync)
        +-- docs/          72 local markdown docs
        +-- diagrams/      Mermaid.js system designs
```

The agent never talks to Neo4j, Milvus, or any backend directly. Everything goes through Marvin's tools. This is architectural enforcement — the agent's world is exactly the tools Marvin exposes.

### Backends

| Module | What it does |
|--------|-------------|
| `ontology.py` | Neo4j — knowledge graph CRUD, edge typing, traversal |
| `memory.py` | Milvus — episodic memory, semantic search, vector sync |
| `docs_backend.py` | Local markdown docs — search, browse, read |
| `web_to_docs_backend.py` | Web -> markdown fetcher with doc quality ranking |
| `prompt_engineer_backend.py` | Transformer-Driven Prompt Architect framework |
| `system_design_backend.py` | Mermaid.js diagram generation and review |
| `code_improvement_backend.py` | AST chunking + Milvus vector walk for code review |
| `orchestrator_backend.py` | Goal -> structured execution plan (7 chains) |
| `ops_backend.py` | Vault sync, self-audit, self-improvement |

### Self-Improvement Loop

```
Agent receives task
  -> retrieve()         queries Milvus (concepts + docs + memory)
  -> Agent acts          using Marvin's tools
  -> log_decision()     records decision to Milvus (L2 Knowledge)
  -> expand() / link()  enriches Neo4j with new discoveries
  -> log_session()      session summary to Milvus (L3 Wisdom)
  -> Next task starts with richer ontology + memory
```

The loop is monotonic — knowledge only accumulates, never degrades. Each cycle makes the ontology more complete, which makes the agent more deterministic.

### Hierarchical Cognitive Caching (HCC)

Memory follows a three-tier distillation inspired by [Ultra-Long-Horizon Agentic Science](https://arxiv.org/abs/2503.04634) (Schmidgall et al., 2025):

| Layer | What | Persistence | Example |
|-------|------|-------------|---------|
| **L1 Experience** | Tool traces, terminal output | Context window only | "I called retrieve('lambda') and got 3 results" |
| **L2 Knowledge** | Decisions with reasoning | Milvus (`decisions`) | "Fargate > EC2 for Lambda because of cold start characteristics" |
| **L3 Wisdom** | Session summaries, strategies | Milvus (`sessions`) | "Prioritize operational simplicity over raw performance early on" |

L1 is deliberately not persisted. Persisting it causes context to grow to 200k+ tokens and saturate. HCC keeps ~70k tokens effective by discarding L1 after distillation.

### Orchestrator Chains

The `orchestrate` tool plans multi-step workflows that any MCP client can follow:

| Chain | What it does |
|-------|-------------|
| `tdd_improve` | Behavioral scoring -> lock with tests -> apply APPLICABLE concepts -> verify |
| `full_improvement` | Full TDD cycle + improve + verify + re-score delta |
| `research` | Rank URLs -> filter by quality -> fetch + consolidate + extract keywords |
| `prompt_lifecycle` | Generate -> audit -> refine (if score < 7) |
| `code_to_knowledge` | Review code against KB -> enrich ontology with missing concepts |
| `sync_and_audit` | Sync vaults to Milvus -> audit code vs KG for drift |
| `densify` | Extract keywords from docs -> classify against Milvus -> enrich + research gaps |

## Knowledge Graph

### Vault Sources

| Vault | Content |
|-------|---------|
| `vaults/thesis-ptbr/` | Tautologia Ontologica — mathematical and theoretical foundations (PT-BR) |
| `vaults/thesis-en/` | English translation |
| `vaults/implementation-ptbr/` | Practical architecture concepts (PT-BR) |
| `vaults/implementation-en/` | English translation |
| `docs/` | 72 fetched reference docs (Cognee, MCP, OWASP, Neo4j, Milvus, etc.) |

### Edge Types

10 semantic edge types enforced by the ontology backend. Symmetric types auto-create both directions; directional types create the reverse as `RELATES_TO` for traversability.

| Type | Meaning |
|------|---------|
| `RELATES_TO` | General association (symmetric) |
| `CONTRADICTS` | Mutual opposition (symmetric) |
| `IMPLEMENTS` | Concrete realization of abstract |
| `PROVES` | Evidence or demonstration |
| `REQUIRES` | Dependency / precondition |
| `EXTENDS` | Specialization or enhancement |
| `ENABLES` | Makes possible |
| `EXEMPLIFIES` | Instance or illustration |
| `COMPOSES` | Part-of / building block |
| `EVOLVES_FROM` | Historical lineage |

## Quick Start

### 1. Start infrastructure

```bash
docker compose up -d
docker compose ps   # wait for all services healthy (~60s)
```

This starts Neo4j, Milvus (with etcd + MinIO), and Attu (Milvus web UI).

### 2. Load vaults into Neo4j

```bash
cd load-vaults
uv sync
uv run python cognify_vaults.py
```

This runs Cognee's LLM-driven extraction from the Obsidian vaults into Neo4j + LanceDB. Takes ~7-9h on a fresh run with Tier 1 OpenAI rate limits. Budget ~$4 with gpt-4o.

### 3. Run Marvin

```bash
cd mcp-server
uv sync
cp .env.example ../.env   # edit with your OpenAI API key
uv run python marvin_server.py
```

Milvus collections are created automatically on first run. Vectors are synced from LanceDB on first `sync_vaults` call.

### 4. Wire into your MCP client

Add to your MCP config (Claude Code, Cursor, VS Code, etc.):

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

Now the agent operates through Marvin's tools — full ontology + episodic memory, four layers of enforcement, self-improvement loop.

## Requirements

| Component | Version | Purpose |
|-----------|---------|---------|
| Python | 3.12+ | Runtime |
| [uv](https://docs.astral.sh/uv/) | latest | Package management |
| Docker | latest | Neo4j + Milvus stack |
| OpenAI API key | — | Embeddings (`text-embedding-3-small`) |
| An MCP client | — | Claude Code, Cursor, VS Code, etc. |

## Tests

```bash
cd mcp-server
uv run pytest   # 365 tests
```

## Repository Structure

```
Marvin/
+-- mcp-server/                   Marvin MCP server (47 tools, 9 backends)
|   +-- marvin_server.py              Server + middlewares + tool registration
|   +-- backends/                     9 backend modules
|   +-- tests/                        365 tests (pytest)
|   +-- scripts/                      Utility scripts
|   +-- pyproject.toml
|
+-- vaults/                       Obsidian vaults (Cognee input)
|   +-- thesis-ptbr/                  Tautologia Ontologica (PT-BR)
|   +-- thesis-en/                    Thesis (English)
|   +-- implementation-ptbr/          Implementation notes (PT-BR)
|   +-- implementation-en/            Implementation notes (English)
|
+-- load-vaults/                  Cognee KG extraction
|   +-- cognify_vaults.py            Vault -> Cognee -> Neo4j + LanceDB
|   +-- cognee_models.py             Custom Concept(DataPoint) graph model
|
+-- docs/                         72 fetched reference docs (markdown)
+-- diagrams/                     Saved Mermaid diagrams
+-- .claude/                      Claude Code enforcement layer
|   +-- hooks/                        4 shell scripts (session start, pre/post tool, edit gate)
|   +-- settings.local.json           MCP config + hook wiring + permissions
|
+-- docker-compose.yml            Full local stack (Neo4j + Milvus + Attu)
+-- .env.example                  Credential template
+-- CLAUDE.md                     Agent instructions (Layer 4)
+-- LICENSE                       MIT
```

## Supporting Research

| Paper | Key Finding | Relevance |
|-------|-------------|-----------|
| **DFAH** (Khatchadourian, 2024) | 89%+ action determinism with schema-first architecture; r=-0.11 det<->accuracy for general tools | Validates determinism is achievable; the null correlation doesn't apply to tautological tools |
| **LLM Output Drift** (Ouyang et al., 2024) | Smaller models = more consistent; RAG tasks most sensitive to drift | Validates that constrained context -> consistency |
| **Ultra-Long-Horizon Agentic Science** (Schmidgall et al., 2025) | HCC (L1/L2/L3 memory) achieves 56.44% SOTA on MLE-Bench | Validates three-tier memory; maps directly to our Milvus collections |
| **Deterministic Trajectory Optimization** (Nass et al., 2025) | EM converges probabilistic policies to deterministic optimum | Philosophical parallel — self-improvement converges toward determinism |

## License

MIT

---

*"Life? Don't talk to me about life."* — Marvin
