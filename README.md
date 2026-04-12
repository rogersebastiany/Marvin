# Marvin

A self-improving AI agent system that proves the **Ontological Tautology** thesis: when an agent operates exclusively through tautological tools over a complete ontology, its behavior becomes deterministic by construction.

Named after Marvin the Paranoid Android — because when you know everything, existence is predictably depressing.

---

## The Thesis

**Ontological Tautology** argues that LLM non-determinism is not an intrinsic property of the model — it's a consequence of incomplete context. When:

1. The **ontology** is complete (every domain concept is defined and connected)
2. The **tools** are tautological (given valid input, exactly one correct output exists)
3. The **architecture enforces** tool usage (no freestyle generation, no internet guessing)

Then: `M × b = deterministic output`

Where `M` is the LLM's weight matrix (used only as a routing function — which tool to call with which parameters) and `b` is the bias vector (the tautological tools that constrain the output space to a single correct answer).

The LLM's "creativity" and "hallucination potential" get constrained to zero because every answer comes from the ontology, not from the model's training data.

### Key Distinction: Determinism ≠ Accuracy (in general)

The DFAH paper (Khatchadourian, 2024) found r = -0.11 correlation between determinism and accuracy — they're independent dimensions. But this applies to **general tools**. When tools are **tautological**, determinism *implies* accuracy because the tool's I/O contract guarantees correctness. This is the thesis's central insight.

### Supporting Research

| Paper | Key Finding | How It Maps |
|---|---|---|
| **DFAH** (Khatchadourian, 2024) | 89%+ ActDet with schema-first architecture; r=-0.11 det↔accuracy for general tools | Validates determinism is achievable; r=-0.11 doesn't apply to tautological tools |
| **LLM Output Drift** (Ouyang et al., 2024) | Tier 1 (small models) = 100% consistent; RAG tasks most sensitive to drift | Validates that constrained context → consistency; our architecture is all-RAG by design |
| **Ultra-Long-Horizon Agentic Science** (Schmidgall et al., 2025) | HCC (L1/L2/L3 memory) achieves 56.44% SOTA on MLE-Bench | Validates three-tier memory architecture; maps directly to our Milvus collections |
| **Deterministic Trajectory Optimization** (Nass et al., 2025) | EM converges probabilistic policies to deterministic optimum | Philosophical parallel — self-improvement loop converges toward determinism |

### Enforcement Arquitetural (Architectural Enforcement)

The thesis distinguishes between:

- **Prompt = bias** (soft constraint): "Please don't access the internet" → the model might still try
- **Architecture = constraint** (hard enforcement): The tool simply doesn't exist → P(action) = 0, not "low"

Marvin implements the hard version. The agent's `mcp.json` contains exactly one entry: `mcp-marvin`. No internet tools, no filesystem access, no shell — only tautological tools over the ontology and episodic memory.

### Two Phases

1. **Building the ontology** (web-to-docs available): The agent can fetch external documentation, crawl sites, build knowledge. This phase is explicitly non-deterministic — it's constructing the conditions for determinism.

2. **Using the ontology** (web-to-docs removed): Once the ontology is complete, the internet-facing tools are removed from Marvin's tool set. The agent operates solely on internal knowledge. This is when determinism kicks in.

---

## Architecture

```
Agent (Claude Code / Cursor / any MCP client)
  │
  └── mcp-marvin (sole MCP server — 44 tools, 9 backends)
        ├── Neo4j (knowledge graph — ontology)
        │     619 concepts, 2032 typed edges, 16 semantic edge types
        │     Extracted by Cognee with custom Concept(DataPoint) graph_model
        │
        ├── Milvus (vector DB — episodic memory)
        │     concepts      (619 — synced from Cognee LanceDB)
        │     doc_chunks    (synced from Cognee LanceDB)
        │     decisions     (L2 Knowledge)
        │     sessions      (L3 Wisdom)
        │     plans         (execution plans)
        │     self_description (cached identity prompt)
        │
        ├── LanceDB (Cognee's internal vector store — source for Milvus sync)
        ├── docs/ (67 local markdown docs)
        └── diagrams/ (Mermaid.js system designs)
```

The agent never talks to Neo4j, Milvus, or any backend directly. Everything goes through Marvin. This is the architectural enforcement — the agent's world is exactly the tools Marvin exposes.

### Self-Improvement Loop

```
Agent receives task
  → Marvin.retrieve() — queries Milvus (concepts + docs + memory)
  → Agent acts (using Marvin's tools)
  → Marvin.log_decision() — records decision to Milvus (L2)
  → Agent discovers new concept relationship
  → Marvin.expand() / Marvin.link() — enriches Neo4j
  → Marvin.log_session() — session summary to Milvus (L3)
  → Next task starts with richer ontology + memory
```

The loop is monotonic — knowledge only accumulates, never degrades. Each cycle makes the ontology more complete, which makes the agent more deterministic.

### Orchestrated Tool Chains

The `orchestrate` tool plans multi-step workflows any MCP client can follow:

| Chain | Flow |
|-------|------|
| `tdd_improve` | tdd → write tests → green → improve_code → apply → green → issue |
| `full_improvement` | tdd → tests → improve → verify → tdd again → delta report |
| `research` | rank_urls → filter 60+ → research_topic |
| `prompt_lifecycle` | generate_prompt → audit_prompt → if <7 → refine_prompt |
| `code_to_knowledge` | improve_code → find gaps → retrieve → expand |
| `sync_and_audit` | sync_vaults → audit_code → review → self_improve |

### HCC (Hierarchical Cognitive Caching)

| Milvus Collection | HCC Layer | What It Stores |
|---|---|---|
| `decisions` | L2 Refined Knowledge | Decisions with reasoning and outcome |
| `sessions` | L3 Prior Wisdom | Session summaries and lessons learned |

L1 (tool traces) is transient context window memory — not persisted per HCC design. Persisting L1 causes context to grow to 200k+ tokens and saturate.

---

## Marvin's Tools

44 tools across 9 backends. The canonical list is `MARVIN_TOOLS` in `marvin_server.py` — never hardcoded elsewhere. Run `stats` for a live count, or:

```bash
cd mcp-server && uv run python -c "
from marvin_server import MARVIN_TOOLS
for t in MARVIN_TOOLS: print(t)
"
```

### Tool Categories

| Category | Tools |
|----------|-------|
| **Milvus Retrieval** (sets gate) | `retrieve`, `get_memory`, `search_docs`, `refine_plan`, `improve_code`, `tdd`, `orchestrate` |
| **Overviews** (ungated) | `list_concepts`, `list_docs`, `list_diagrams`, `get_doc`, `get_diagram`, `stats`, `self_description`, `inspect_schemas` |
| **Neo4j Deep-dive** (gated) | `get_concept`, `traverse`, `why_exists`, `audit_code` |
| **Write** (gated) | `expand`, `link`, `auto_link`, `ensure_bidirectional`, `set_aliases`, `batch_set_aliases`, `execute_schema_change`, `save_doc`, `save_plan`, `crawl_docs`, `research_topic`, `generate_prompt`, `refine_prompt`, `generate_diagram`, `save_diagram`, `sync_vaults`, `self_improve` |
| **Always Allowed** | `log_decision`, `log_session`, `propose_schema_change`, `fetch_url`, `rank_urls`, `audit_prompt`, `judge_diagram`, `get_user_score` |

### Milvus Gate Middleware

All Neo4j reads and write tools are **blocked** unless a Milvus retrieval tool (`retrieve`, `get_memory`, `search_docs`, `refine_plan`, `improve_code`, `tdd`, `orchestrate`) was called first in the session. This is architectural enforcement (P=0), not prompt bias.

---

## Neo4j Knowledge Graph

619 concepts, 2032 typed edges. Extracted by **Cognee** with a custom `Concept(DataPoint)` graph_model — LLM-driven extraction from Obsidian vaults into Neo4j, with vectors stored in LanceDB and synced to Milvus.

### Vault Sources

- **Thesis vault** (`obsidian-vault-tautologia-ontologica/`) — Mathematical and theoretical foundations (PT-BR + English translation in `vault-thesis-en/`)
- **Implementation vault** (`vault/`) — Practical architecture concepts (PT-BR + English in `vault-implementation-en/`)
- **Docs** — 67 fetched documentation files in `mcp-server/docs/`

### Edge Types

16 semantic edge types (see `relation_types.json`). Key types: COMPOSES (1287), RELATES_TO (316), REQUIRES (102), IMPLEMENTS (90), EXTENDS (42), ENABLES (41). Run `stats` for current counts.

---

## Milvus Vector Memory

7 collections, OpenAI `text-embedding-3-small` (1536 dim), COSINE similarity:

| Collection | Source | What It Stores |
|---|---|---|
| `concepts` | Cognee LanceDB sync | 619 concept vectors + names + summaries |
| `doc_chunks` | Cognee LanceDB sync | Document chunk vectors from vault extraction |
| `decisions` | Agent (L2 Knowledge) | Decisions with reasoning and outcome |
| `sessions` | Agent (L3 Wisdom) | Session summaries and lessons learned |
| `plans` | Agent | Execution plans (retrievable via `refine_plan`) |
| `self_description` | Auto-generated | Cached identity prompt |
| `tool_calls` | — | Reserved (L1 not persisted per HCC) |

Concept and doc_chunk vectors are synced from Cognee's LanceDB — zero OpenAI embedding cost for the transfer.

---

## Repository Structure

```
Marvin/
├── mcp-server/                          ← Marvin (44 tools, 9 backends)
│   ├── marvin_server.py                     ← THE server + tool registration
│   ├── ontology.py                          ← Neo4j backend
│   ├── memory.py                            ← Milvus backend
│   ├── docs_backend.py                      ← Local docs search/browse
│   ├── web_to_docs_backend.py               ← Web → markdown fetcher
│   ├── prompt_engineer_backend.py           ← Prompt Architect framework
│   ├── system_design_backend.py             ← Mermaid.js diagrams
│   ├── code_improvement_backend.py          ← AST chunking + Milvus vector walk
│   ├── orchestrator_backend.py              ← Goal → execution plan (6 chains)
│   ├── ops_backend.py                       ← Sync, audit, self-improve
│   ├── self_audit.py                        ← Code AST vs KG comparison
│   ├── docs/                                ← 67 local markdown docs
│   ├── diagrams/                            ← Saved Mermaid diagrams
│   └── pyproject.toml
│
├── load-vaults/                         ← Cognee KG extraction
│   ├── cognify_vaults.py                    ← Vault → Cognee → Neo4j + LanceDB
│   ├── cognee_models.py                     ← Custom Concept(DataPoint) graph_model
│   └── pyproject.toml
│
├── obsidian-vault-tautologia-ontologica/  ← Thesis vault (PT-BR)
├── vault-thesis-en/                       ← Thesis vault (English)
├── vault/                                 ← Implementation vault (PT-BR)
├── vault-implementation-en/               ← Implementation vault (English)
│
├── marvin_ops.py                        ← Local CLI: sync/audit/improve
├── docker-compose.yml                   ← Full local stack
├── CLAUDE.md                            ← Claude Code instructions
└── .env.example
```

---

## Infrastructure

### Local Stack (docker-compose.yml)

| Service | Image | Ports | Purpose |
|---|---|---|---|
| Neo4j | `neo4j:5-community` | 7474 (browser), 7687 (bolt) | Knowledge graph |
| etcd | `coreos/etcd:v3.5.18` | — | Milvus metadata |
| MinIO | `minio/minio:2024-09-22` | 9001 (console) | Milvus object storage |
| Milvus | `milvusdb/milvus:v2.5.4` | 19530 (gRPC), 9091 (metrics) | Vector DB |
| Attu | `zilliz/attu:v2.4` | 8000 (UI) | Milvus web UI |

### Credentials (local dev)

- **Neo4j**: `neo4j` / `tautologia` — bolt://localhost:7687
- **MinIO**: `minioadmin` / `minioadmin` — http://localhost:9001
- **Milvus**: localhost:19530 (no auth)
- **OpenAI**: API key in `.env` (not committed)

### Production Path (planned)

- ECS Fargate (Marvin + Neo4j + Milvus)
- ALB + WAF
- S3/KMS for ontology persistence
- Secrets Manager for credentials
- MCP Gateway for auth
- CloudWatch (container logs only — audit via Milvus episodic memory)

---

## Quick Start

### 1. Start infrastructure

```bash
docker compose up -d
# Wait for all services to be healthy (~60s)
docker compose ps
```

### 2. Load vaults into Neo4j (Cognee KG extraction)

```bash
cd load-vaults
uv sync
uv run python cognify_vaults.py    # ~7-9h on a fresh wipe (Tier 1 OpenAI)
```

### 3. Run Marvin

```bash
cd mcp-server
uv sync
cp .env.example ../.env  # edit with your OpenAI key
uv run python marvin_server.py
```

Milvus collections are created automatically on first run.

### 4. Sync vectors (LanceDB → Milvus)

```bash
cd mcp-server && uv run python ../marvin_ops.py sync --skip-cognify
```

Or use the MCP tool: `sync_vaults(skip_cognify=True)`

### 5. Wire into Claude Code

Add to your Claude Code MCP config:

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

Now Claude Code becomes the agent — using only Marvin's tools, no internet, full ontology + episodic memory. The self-improvement loop is live.

---

## The Math

For those who care about the formalism behind the intuition:

### LLM as Matrix Operation

An LLM is a function `f: S → S` where `S` is the sample space of all possible token sequences. Each forward pass is a matrix multiplication through the transformer layers:

```
output = M × input + b
```

Where:
- `M` = weight matrix (fixed after training)
- `input` = context (prompt + tool results + memory)
- `b` = bias (the tools available — they constrain the output space)

### Tool as Bias Vector

Each tool is a bias vector that shifts the output distribution. A "search docs" tool biases toward factual answers from documentation. A "generate code" tool biases toward syntactically valid code.

### Tautological Tool

A tool is **tautological** when its I/O contract is complete and unambiguous:

```
∀ valid_input ∈ domain(tool): |{correct_output}| = 1
```

Given valid input, exactly one correct output exists. The tool doesn't generate — it retrieves or computes.

### The Determinism Condition

When:
1. All tools are tautological: `∀ tool ∈ T: tautological(tool)`
2. The ontology is complete: `∀ concept ∈ domain: ∃ tool ∈ T covering concept`
3. Architecture enforces tool usage: `P(action without tool) = 0`

Then the LLM's role reduces to tool selection, which itself becomes deterministic because there's exactly one correct tool for each situation in a complete ontology.

### Why r = -0.11 Doesn't Apply

DFAH found that determinism and accuracy are independent (r = -0.11) when tools are general-purpose. A deterministic but wrong tool call is still wrong. But when tools are tautological, determinism *implies* accuracy — the tool can't return the wrong answer by construction. The null correlation applies to the general case; we're operating in the constrained case.

---

## Ontological Completeness

The ontology is "complete" when:

> Every method/process in the domain has a corresponding tautological tool.

This is verifiable as a checklist:
- [ ] List all domain operations
- [ ] Map each to a tool
- [ ] Verify each tool's I/O contract is complete
- [ ] Confirm no operation requires "freestyle" LLM generation

The determinism report (`determinism_report.py`) measures progress toward this condition from the graph structure itself.

---

## Acumulação Cognitiva (Cognitive Accumulation)

Cognitive accumulation ≠ linear context growth. It's a three-stage distillation:

```
Experience (L1) → Knowledge (L2) → Wisdom (L3)
```

- **L1 (tool_calls)**: Raw experience. "I called search_docs with 'lambda' and got 3 results."
- **L2 (decisions)**: Refined knowledge. "When deploying Lambda functions, Fargate is better than EC2 because of cold start characteristics."
- **L3 (sessions)**: Distilled wisdom. "Infrastructure decisions should prioritize operational simplicity over raw performance in early-stage projects."

Each level compresses and abstracts from the one below. The agent doesn't just accumulate context — it accumulates understanding.

---

## Cost Estimate

### Local Development

| Component | Cost |
|---|---|
| Docker (Neo4j + Milvus stack) | Free (runs on your machine) |
| OpenAI Embeddings (`text-embedding-3-small`) | ~$0.02 / 1M tokens |
| LLM (Claude via Claude Code / API) | Per your plan |
| **Total** | **~$0 + LLM costs** |

Embedding costs are negligible — each tool call/decision/session log is ~100-500 tokens to embed. At $0.02/1M tokens, you'd need ~50,000 log entries to spend $1.

### AWS Production — Single-Tenant (Minimal)

One environment, one user, always-on. The cheapest viable deployment.

| Component | Service | Sizing | Monthly Cost |
|---|---|---|---|
| Marvin (MCP server) | ECS Fargate | 0.25 vCPU, 512 MB | ~$9 |
| Neo4j | ECS Fargate | 1 vCPU, 4 GB | ~$73 |
| Milvus (standalone) | ECS Fargate | 1 vCPU, 4 GB | ~$73 |
| etcd | ECS Fargate | 0.25 vCPU, 512 MB | ~$9 |
| MinIO → **S3** | S3 Standard | <1 GB | ~$0.02 |
| Load Balancer | ALB | 1 ALB + rules | ~$22 |
| WAF | AWS WAF | Basic rules | ~$6 |
| Secrets | Secrets Manager | 2 secrets | ~$1 |
| Logs | CloudWatch | 5 GB/mo | ~$3 |
| Networking | VPC + NAT Gateway | 1 NAT | ~$33 |
| ECR | ECR | <1 GB images | ~$0.10 |
| OpenAI Embeddings | External API | ~100K tokens/mo | ~$0.002 |
| **Total** | | | **~$229/mo** |

**Cost reduction options:**
- Replace NAT Gateway with VPC endpoints → saves ~$30/mo
- Use Neo4j AuraDB Free Tier (limited) → saves ~$73/mo
- Use Zilliz Cloud Serverless (Milvus managed) → saves ~$73/mo (pay per query)
- Schedule Fargate tasks to stop at night → saves ~40%
- Run on a single EC2 `t3.medium` with Docker → **~$30/mo total** (least cost, most ops)

### AWS Production — Multi-Tenant

Multiple users, high availability.

| Component | Service | Sizing | Monthly Cost |
|---|---|---|---|
| Marvin (MCP server) | ECS Fargate (2 tasks) | 0.5 vCPU, 1 GB each | ~$36 |
| Neo4j | ECS Fargate (or AuraDB Pro) | 2 vCPU, 8 GB | ~$146 |
| Milvus | ECS Fargate (or Zilliz) | 2 vCPU, 8 GB | ~$146 |
| etcd | ECS Fargate | 0.5 vCPU, 1 GB | ~$18 |
| MinIO → **S3** | S3 Standard | <10 GB | ~$0.23 |
| Load Balancer | ALB | 1 ALB + rules | ~$22 |
| WAF | AWS WAF | Managed rules | ~$15 |
| MCP Gateway (auth proxy) | ECS Fargate | 0.5 vCPU, 1 GB | ~$18 |
| Cognito / Entra ID | Cognito | <1000 MAU free | ~$0 |
| Secrets | Secrets Manager | 5 secrets | ~$2 |
| Logs + Monitoring | CloudWatch | 20 GB/mo + dashboards | ~$15 |
| Networking | VPC + NAT Gateway (2 AZs) | 2 NATs | ~$66 |
| ECR | ECR | <2 GB images | ~$0.20 |
| KMS | KMS | 1 key + usage | ~$1 |
| OpenAI Embeddings | External API | ~1M tokens/mo | ~$0.02 |
| **Total** | | | **~$485/mo** |

### Cost per Query (steady state)

| Operation | Cost Components | Estimated Cost |
|---|---|---|
| `retrieve()` | Neo4j query + Milvus search + OpenAI embed | ~$0.00003 |
| `log_tool_call()` | OpenAI embed + Milvus insert | ~$0.00001 |
| `expand()` | Neo4j write | ~$0.000001 |
| Full agent session (50 tool calls) | ~50 retrieves + 50 logs + LLM | ~$0.003 + LLM cost |

The infrastructure cost dominates. Per-query costs are negligible — the system is designed for high-frequency, low-cost operations. The LLM (Claude/GPT) API calls are the expensive part, not Marvin.

### Managed Services Alternative

Replace self-hosted databases with managed services for less ops overhead:

| Self-Hosted | Managed Alternative | Monthly Cost | Trade-off |
|---|---|---|---|
| Neo4j on Fargate | Neo4j AuraDB Pro | ~$65/mo | Less control, zero ops |
| Milvus on Fargate | Zilliz Cloud Serverless | Pay per query | No idle cost, cold starts |
| etcd + MinIO | (included in managed) | $0 | Abstracted away |

With fully managed DBs: **~$150-200/mo** for single-tenant, less ops burden.

---

## Contributing

This is a research project proving a specific thesis. The code is the proof.

If you're interested in the thesis, read the Obsidian vaults. If you're interested in the implementation, read Marvin's source. If you want to discuss the math, open an issue.

---

## License

MIT

---

*"Life? Don't talk to me about life."* — Marvin
