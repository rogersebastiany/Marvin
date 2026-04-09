# Marvin

A self-improving AI agent system that proves the **Tautologia Ontológica** thesis: when an agent operates exclusively through tautological tools over a complete ontology, its behavior becomes deterministic by construction.

Named after Marvin the Paranoid Android — because when you know everything, existence is predictably depressing.

---

## The Thesis

**Tautologia Ontológica** argues that LLM non-determinism is not an intrinsic property of the model — it's a consequence of incomplete context. When:

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
Agent (Claude Code / any MCP client)
  │
  └── mcp-marvin (sole MCP server — 29 tools)
        ├── Neo4j (knowledge graph — ontology)
        │     320+ concepts, 3000+ relations
        │     Thesis + Implementation + Agent + Docs vaults
        │
        ├── Milvus (vector DB — episodic memory)
        │     tool_calls   (L1 Experience)
        │     decisions     (L2 Knowledge)
        │     sessions      (L3 Wisdom)
        │
        ├── docs/ (local markdown documentation)
        └── diagrams/ (Mermaid.js system designs)
```

The agent never talks to Neo4j, Milvus, or any backend directly. Everything goes through Marvin. This is the architectural enforcement — the agent's world is exactly the tools Marvin exposes.

### Self-Improvement Loop

```
Agent receives task
  → Marvin.retrieve() — queries Neo4j + Milvus + docs
  → Agent acts (using Marvin's tools)
  → Marvin.log_tool_call() — records action to Milvus (L1)
  → Marvin.log_decision() — records decision to Milvus (L2)
  → Agent discovers new concept relationship
  → Marvin.expand() / Marvin.link() — enriches Neo4j
  → Marvin.log_session() — session summary to Milvus (L3)
  → Next task starts with richer ontology + memory
```

The loop is monotonic — knowledge only accumulates, never degrades. Each cycle makes the ontology more complete, which makes the agent more deterministic.

### HCC Parallel (Hierarchical Cognitive Caching)

Our three Milvus collections map directly to the HCC architecture from the Ultra-Long-Horizon paper:

| Milvus Collection | HCC Layer | Granularity | What It Stores |
|---|---|---|---|
| `tool_calls` | L1 Evolving Experience | Fine | Every tool invocation with params, result, context |
| `decisions` | L2 Refined Knowledge | Medium | High-level decisions with reasoning and outcome |
| `sessions` | L3 Prior Wisdom | Coarse | Session summaries and lessons learned |

The ablation study in the paper validates this design: without L1, performance drops to 22.7%; without L3, it drops to 54.5%. All three layers are necessary.

---

## Marvin's Tools (29 total)

### Retrieval (4 tools)
| Tool | What It Does |
|---|---|
| `retrieve` | Unified search across Neo4j + Milvus + docs. One call gets everything. |
| `get_concept` | Full concept with content and all relations from the ontology |
| `traverse` | Walk N hops from a concept, return neighborhood graph |
| `why_exists` | Explain why a concept exists — all edge reasoning |

### Logging — Episodic Memory (3 tools)
| Tool | What It Does |
|---|---|
| `log_tool_call` | Record a tool invocation (L1 Experience) |
| `log_decision` | Record a decision with reasoning (L2 Knowledge) |
| `log_session` | Record a session summary (L3 Wisdom) |

### Enrichment (4 tools)
| Tool | What It Does |
|---|---|
| `expand` | Add a new concept or relation to the knowledge graph |
| `link` | Create a direct non-linear relation between two existing concepts |
| `auto_link` | Scan concept content for references to other concepts, auto-create edges |
| `ensure_bidirectional` | For every A→B edge, ensure B→A also exists |

### Evolution — Human-in-the-Loop (2 tools)
| Tool | What It Does |
|---|---|
| `propose_schema_change` | Propose a schema change (returns proposal for human review) |
| `execute_schema_change` | Apply a schema change (requires `confirmed=True` — human gate) |

### Documentation (6 tools)
| Tool | What It Does |
|---|---|
| `search_docs` | Search local markdown docs by keyword |
| `list_docs` | List all available doc files |
| `get_doc` | Read a full documentation file |
| `fetch_url` | Fetch a webpage and return as markdown |
| `save_doc` | Fetch a webpage and save as local doc |
| `crawl_docs` | Crawl a doc site, saving pages locally |

### Prompt Engineering (3 tools)
| Tool | What It Does |
|---|---|
| `generate_prompt` | Generate a structured prompt (Transformer-Driven Prompt Architect framework) |
| `refine_prompt` | Improve an existing prompt based on feedback |
| `audit_prompt` | Evaluate a prompt against the 6 mandatory sections |

### System Design — Diagrams (5 tools)
| Tool | What It Does |
|---|---|
| `generate_diagram` | Generate a Mermaid.js diagram from description |
| `judge_diagram` | Review a diagram for correctness and quality (4-dimension scoring) |
| `save_diagram` | Save a diagram to `diagrams/` |
| `list_diagrams` | List saved diagrams |
| `get_diagram` | Read a saved diagram |

### Introspection (2 tools)
| Tool | What It Does |
|---|---|
| `inspect_schemas` | Show current Neo4j + Milvus schemas |
| `stats` | Full system overview (concepts, relations, memory entries, docs, diagrams) |

---

## Neo4j Knowledge Graph

### Schema

```
(:Concept {
  name: string (unique),
  vault: "thesis" | "implementation" | "both" | "agent",
  summary: string,
  content: string,
  ghost: boolean,
  created_at: datetime,
  updated_at: datetime
})

-[:RELATES_TO {
  weight: float,
  reasoning: string,
  discovered_by: "vault_import" | "agent" | "auto_link" | "bidirectional"
}]->
```

### Vault Sources

- **Thesis vault** (`obsidian-vault-tautologia-ontologica/`) — 45 concepts covering the mathematical and theoretical foundations: Tautologia Ontológica, Determinismo, Álgebra Linear, Teoria dos Conjuntos, Espaço Amostral, Convergência, DFAH, LLM Output Drift, HCC, etc. Available in Portuguese (original) and English (`vault-thesis-en/`).

- **Implementation vault** (`vault/`) — 38 concepts covering the practical architecture: Agente na POC, Cadeia de Servers, FastMCP, Neo4j, Milvus, mcp-ontology-server, mcp-memory-server, Loop de Auto-Melhoria, Enforcement Arquitetural, etc. Available in Portuguese (original) and English (`vault-implementation-en/`).

- **Both vaults** — 3 concepts that bridge theory and implementation: Acumulação Cognitiva, Tool Tautológica, Enforcement Arquitetural.

- **Docs vault** — 210+ fetched documentation files covering Python, AWS, Kotlin, Neo4j, Milvus, Docker, MCP, Mermaid.js, SE patterns, CI/CD, OWASP, OpenTelemetry, and more.

- **Agent vault** — 20+ concepts discovered by Marvin's self-improvement loop, including Python, AWS Infrastructure, Kotlin, and cross-domain bridge concepts. Auto-classified as `agent` — distinguishable from human-authored knowledge.

### Determinism Report

The `load-vaults/determinism_report.py` script measures how close the graph is to ontological completeness:

| Metric | Score | Weight |
|---|---|---|
| Ghost Coverage (defined/referenced) | 100% | 0.20 |
| Content Coverage (has substance) | 100% | 0.15 |
| Summary Coverage (has summary) | 98%+ | 0.05 |
| Connectivity (no orphans, min 3 edges) | 82%+ | 0.20 |
| Bidirectionality (A→B and B→A) | 100% | 0.10 |
| Vault Bridging (theory↔implementation) | Improving | 0.15 |
| Tool Tautology (29 tools classified) | 90%+ | 0.15 |

Run `cd load-vaults && uv run python determinism_report.py` for current metrics.

---

## Milvus Episodic Memory

Three collections with OpenAI embeddings (`text-embedding-3-small`, 1536 dimensions), COSINE similarity, IVF_FLAT index:

### tool_calls (L1 Experience)
```
id, tool_name, parameters, result_summary, context,
session_id, timestamp, success, embedding[1536]
```

### decisions (L2 Knowledge)
```
id, objective, options_considered, chosen_option, reasoning,
outcome, session_id, timestamp, embedding[1536]
```

### sessions (L3 Wisdom)
```
id, objective, approach, result, lessons_learned, tools_used,
decision_count, tool_call_count, timestamp, embedding[1536]
```

Memory is append-only — the agent accumulates experience monotonically. Search is by semantic similarity (cosine distance in embedding space), not keyword matching.

---

## Repository Structure

```
Marvin/
├── mcp-server-poc/                  ← Marvin + all backends
│   ├── marvin_server.py             ← THE server (27 tools, 8 categories)
│   ├── ontology.py                  ← Neo4j backend
│   ├── memory.py                    ← Milvus backend
│   ├── docs_backend.py              ← Local docs search/browse
│   ├── web_to_docs_backend.py       ← Web → markdown fetcher
│   ├── prompt_engineer_backend.py   ← Prompt Architect framework
│   ├── system_design_backend.py     ← Mermaid.js diagrams
│   ├── docs/                        ← Local documentation (210+ files)
│   ├── diagrams/                    ← Saved Mermaid diagrams (3 files)
│   ├── .cursor/mcp.json             ← MCP config (only mcp-marvin)
│   ├── pyproject.toml               ← Python deps (uv)
│   ├── Dockerfile
│   └── Makefile
│
├── obsidian-vault-tautologia-ontologica/  ← Thesis vault (45 concepts, Portuguese)
│   └── obsidian-vault/
│       ├── Tautologia Ontológica.md
│       ├── Determinismo.md
│       ├── ... (45 interconnected notes)
│       └── poc docs/
│
├── vault-thesis-en/                 ← Thesis vault (English translation)
│   └── ... (45 translated notes)
│
├── vault/                           ← Implementation vault (38 concepts, Portuguese)
│   ├── Agente na POC.md
│   ├── Neo4j.md
│   ├── ... (38 interconnected notes)
│
├── vault-implementation-en/         ← Implementation vault (English translation)
│   └── ... (38 translated notes)
│
├── load-vaults/                     ← Disposable ETL scripts
│   ├── load_vaults.py               ← Vault → Neo4j loader
│   ├── query_graph.py               ← Interactive Neo4j explorer
│   ├── determinism_report.py        ← Ontological determinism metrics
│   ├── setup_milvus.py              ← Milvus collection creator
│   └── pyproject.toml
│
├── docker-compose.yml               ← Full local stack
├── CLAUDE.md                        ← Claude Code instructions
├── .gitignore
└── Untitled-2026-03-20-2209.excalidraw  ← Architecture whiteboard
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

### 2. Load vaults into Neo4j

```bash
cd load-vaults
uv sync
uv run python load_vaults.py
```

### 3. Set up Milvus collections

```bash
uv run python setup_milvus.py
```

### 4. Run Marvin

```bash
cd ../mcp-server-poc
uv sync
# Set your OpenAI key
echo "OPENAI_API_KEY=sk-..." > ../.env
# Start Marvin
uv run python marvin_server.py
```

### 5. Explore

```bash
# Query the graph
cd ../load-vaults
uv run python query_graph.py stats
uv run python query_graph.py top 10
uv run python query_graph.py concept "Tautologia Ontológica"
uv run python query_graph.py path "Determinismo" "Milvus"

# Determinism report
uv run python determinism_report.py

# Milvus status
uv run python setup_milvus.py --status
```

### 6. Wire into Claude Code

Add to your Claude Code MCP config:

```json
{
  "mcpServers": {
    "mcp-marvin": {
      "type": "stdio",
      "command": "uv",
      "args": ["run", "python", "marvin_server.py"],
      "cwd": "/path/to/Marvin/mcp-server-poc"
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
