# Vault → Knowledge Graph: Full History

Every approach taken to populate Neo4j with the Tautologia Ontológica vault content, chronologically, with what we tried, what we decided, and what happened.

---

## Era 0 — The Pythonistic loader (`load-vaults/load_vaults.py`)

**Approach:** Hand-written Python regex pipeline that parses Obsidian markdown directly:

1. **Parse** — walk vault `.md` files, extract `[[wikilinks]]` and the surrounding sentence as edge context
2. **Classify** — for each `(source, target, sentence)` tuple, ask `gpt-4o-mini` to pick one of 16 relation types based on the sentence
3. **Load** — `MERGE` nodes and edges into Neo4j with vault provenance (`vault="thesis"`, `"implementation"`, `"docs"`)

**Decisions:**

- MERGE-only — agent-discovered concepts (`vault="agent"`) survive re-runs untouched
- Edge types loaded from `mcp-server/relation_types.json` as single source of truth
- Bidirectional edges enforced via `auto_link`/`ensure_bidirectional`
- Cross-language merging: EN concepts merge INTO their PT counterpart via alias mapping
- Optional classification — can run with no LLM, all edges stay as `RELATES_TO`

**What happened:** worked, was deterministic, but **hit a hard ceiling at 58.2% typed edges**. The pipeline could only find what was explicitly wikilinked. It could classify the *type* of an existing wikilink edge, but it could **never discover a relationship that wasn't already a wikilink**. Concept extraction from free prose was impossible. Result: 145 concepts, edges dominated by what the human author had bothered to wikilink.

**Verdict:** Right baseline, wrong ceiling. Needed an LLM that reads prose to *discover* concepts and relations, not just classify pre-existing ones.

---

## Era 1 — Cognee adoption (commits `cecd93c` → `db5768e`)

**Why switch:** cognee is purpose-built for LLM-driven KG extraction. It chunks documents, runs an extraction prompt over each chunk, gets back a structured JSON object describing entities + relations, deduplicates by name, MERGEs into the graph backend (Neo4j in our case). The whole thing the Pythonistic loader couldn't do is exactly what cognee is for.

**Architecture decisions:**

- Cognee 0.5.8 (dropped Milvus from core) → use **LanceDB** for cognee's internal vector needs, keep **Marvin's own Milvus** untouched
- **Neo4j as the shared graph backend** — both cognee's `Entity` nodes and Marvin's `:Concept` nodes coexist in one DB
- gpt-4o-mini for extraction (cost), text-embedding-3-small for embeddings (matches Marvin's existing model)
- Custom prompt guides the LLM toward our 16 relation type names + naming/language rules

### Attempt 1 — `OntologyGraph` custom graph_model (FAILED)

**Tried:** passed a custom `graph_model=OntologyGraph` with explicit `nodes`/`edges` lists matching our domain shape.

**What happened:** **Pydantic ValidationError inside cognee's pipeline.** The `extract_graph_from_data` task expects an *entity-centric* model (one root object with relation fields pointing at other objects), not a node-list/edge-list shape. Our `OntologyGraph` violated that contract.

**Decision:** Abandon custom graph_model. Use cognee's default `KnowledgeGraph` and post-process the output.

### Attempt 2 — Default `KnowledgeGraph` + post-processing (2026-04-10) — SUCCESS

**Tried:**

- `cognee.cognify(datasets=["tautologia"], custom_prompt=..., chunks_per_batch=5, data_per_batch=5)` with **default** `KnowledgeGraph` model
- Custom prompt nudges the LLM toward snake_case versions of our 16 type names (the schema can't enforce this — only the prompt can)
- `post_process_edges()` connects to Neo4j directly, enumerates edge types, renames snake_case → SCREAMING_CASE via `MATCH+CREATE+DELETE`
- Unmapped edge types fall back to `RELATES_TO`
- Rate limiting: `llm_rate_limit_enabled=True`, **10 req/min** under Tier 1 (200k TPM / 500 RPM)

**What happened:** Ran cleanly. **13,659 total edges**, all 16 relation types populated:

| Type | Count | Type | Count |
|---|---|---|---|
| COMPOSES | 6,019 (44%) | DEFINES | 98 |
| EXEMPLIFIES | 2,762 | REDUCES | 72 |
| RELATES_TO | 2,199 | MITIGATES | 71 |
| ENABLES | 768 | FORMALIZES | 62 |
| REQUIRES | 681 | CONTRADICTS | 57 |
| IMPLEMENTS | 327 | EVOLVES_FROM | 35 |
| EXTENDS | 296 | ANALOGOUS_TO | 34 |
| PROVES | 155 | INFERS | 23 |

**Quality issues found:**

- **Mapping gaps** — `enabled` (90 edges, should be ENABLES), `enhances` (37), `implies` (29), `enabling` (16), `components` (14), `supports` (8), `interfaces_with` (5), etc. all fell through to `RELATES_TO` instead of their semantic match
- **LLM typos** — gpt-4o-mini emitted `enebles`, `defenes`, `impliments`, `implants`, `implices`, `imples`, `defies`, `infer` (singular). ~15 edges lost
- **COMPOSES dominance** — 44% of all edges are COMPOSES. Default extraction prefers "X contains Y" / "X is part of Y" patterns. Likely over-extraction
- **`RELATES_TO` at 16%** — the prompt's "use only as last resort" instruction worked partially

**Decision:** Cognee adopted as KG engine. Custom graph_model verdict: **NO** — entity-centric assumption is hostile to nodes/edges-list shapes. Default KG + post-process is the right approach.

---

## Era 2 — This session (2026-04-11) — Path A custom Concept(DataPoint)

**Why revisit "custom graph_model" verdict:** cleaning out `mcp-server/docs/` we re-read cognee's `extract_graph_from_data.py:99-103` and noticed a specific branch: **when `graph_model is not KnowledgeGraph`, cognee bypasses the default Entity-creating flow and writes the model's class as the Neo4j label directly**. The Era 1 failure was specifically `OntologyGraph` (nodes/edges-list shape). An *entity-centric* custom DataPoint model wouldn't hit that pipeline assumption — it would *use* the entity-centric branch instead of fighting it.

**Hypothesis:** A `Concept(DataPoint)` model with 16 typed relation fields, each holding a list of nested `Concept` objects, would:

1. Land on the entity-centric branch of cognee's pipeline
2. Get its class name (`Concept`) used as the Neo4j label directly — no post-processing
3. Use Pydantic JSON schema to *constrain the LLM at extraction time* to our 16 types — no need for prompt-only nudging or post-hoc keyword mapping
4. Use deterministic `uuid5(slug(name))` IDs so the same concept across chunks resolves to a single node via MERGE

User chose **Path A** (custom Concept) over **Path B** (revert to known-working default KG + post-process), explicitly against memory's "Custom graph_model? NO" verdict, after seeing the smoke-test evidence below.

### Smoke test (`load-vaults/smoke_concept_model.py`) — PASSED

Isolated test before betting the full vault sweep on it. 4 fake unique concepts (FlibberWidget, ZorbProtocol, GlimmerEngine, WhirligigStandard) with 2 short texts about implementations, requirements, contradictions.

**Verified:**

- `:Concept` label correctly applied (no fallback to `:Entity`)
- Deterministic UUIDs: computed `uuid5(NAMESPACE_OID, slug(name))` in Python, exact match against Neo4j IDs
- Edges populated on the typed fields (IMPLEMENTS, REQUIRES, CONTRADICTS) — not just `relates_to`
- No `ValidationError` from cognee's pipeline

Path A is mechanically valid. Open question: throughput economics on Tier 1.

### Attempt 1 of Path A — 10 RPM, batch 5/5 — INSTANT 429 STORM

**Config:** `chunks_per_batch=5, data_per_batch=5, llm_rate_limit_requests=10`

**What happened:** Ran for ~3 minutes. **17 chunks completed**, then 429 error storm started. Killed.

**Diagnosis (incomplete at the time):** Custom Concept produces richer JSON than default KG (~25k tokens/req estimated). 10 RPM × 25k = 250k TPM, over the 200k ceiling.

### Attempt 2 of Path A — 5 RPM, batch 5/5 — DIES AT CHUNK ~16

**Change:** `llm_rate_limit_requests=10 → 5` with comment about Tier 1 math.

**What happened:** **16 chunks completed, 496 RateLimitError lines**, never recovered. Killed.

**Diagnosis attempt #2 (still incomplete):** Per-request token cost was higher than estimated — must be ~40k tokens/req. 5 RPM × 40k = 200k TPM = exact ceiling.

### Backup before next attempt

Before destructive operations, created two-tier Neo4j backup:

- `backups/neo4j-pre-cognee-nuke-clean.cypher` — 16MB, 3,569 statements, replayable
- `backups/neo4j-data-20260411-032054/` — 538MB raw data volume snapshot via `docker cp`

Added `backups/` to root `.gitignore`.

### Attempt 3 of Path A — 2 RPM, batch 1/1 — REAL DIAGNOSIS + SUCCESS

**Real root cause** (only diagnosed on attempt 3): cognee's `llm_rate_limit_requests` only throttles request **count**/minute. It does **NOT** cap concurrent in-flight requests within a batch. With `chunks_per_batch=5` × `data_per_batch=5`, cognee fired up to **25 parallel LLM calls on launch**. 25 × 40k = 1M tokens hitting OpenAI in second 1 → instant ceiling, infinite retry storm, zero forward progress on attempt 2.

**Config:**

- `llm_rate_limit_requests=2` (paranoid headroom)
- `chunks_per_batch=1` (no parallel chunks within a doc)
- `data_per_batch=1` (no parallel docs)

This forces strict serialization: one LLM call at a time, then wait, then next.

**Launch:** Detached `nohup uv run python cognify_vaults.py`, PIDs 2673849 + 2673861, log `/tmp/cognify-overnight.log`. Predicted 2 chunks/min × ~1100 chunks = ~9h overnight.

**Surprise during the run:** sustained throughput was actually **~14-17 chunks/min**, not 2. cognee's `llm_rate_limit_requests` appears to be a **reactive backoff** (kicks in *after* a 429), not a preemptive throttle. With no first 429 (because batch=1/1 prevented bursts), the limiter never engaged at all and cognee ran at natural API speed. Live OpenAI rate-limit headers during the run: `remaining-tokens: 199,996/200,000` — 99.998% headroom. Per-request token cost was way smaller than 40k; sustained burn was probably ~70k TPM (35% of ceiling).

**False alarm during the run:** at one check the log showed a 5h gap between events. I diagnosed an `httpx` infinite-read hang based on idle ESTABLISHED sockets to Cloudflare. **I was wrong** — the process recovered on its own and finished cleanly. Either it was a slow-but-not-stuck phase, or cognee was processing a large doc with sparse logging. Either way, no intervention needed.

### Final state (Era 2 / Path A success)

| Metric | Value |
|---|---|
| Total runtime | ~7h |
| Chunks processed | 2,175 |
| RateLimitErrors | **0** |
| `:Concept` nodes | **547** |
| Total edges | **1,844** |
| Distinct edge types | **16** (exactly our ontology, all SCREAMING_CASE) |
| Process exit | Clean |

**Edge type distribution (post `post_process_edges()`):**

| Type | Count | Type | Count |
|---|---|---|---|
| COMPOSES | 1,143 | DEFINES | 21 |
| RELATES_TO | 310 (17%) | ANALOGOUS_TO | 21 |
| REQUIRES | 93 | REDUCES | 13 |
| IMPLEMENTS | 81 | INFERS | 6 |
| EXTENDS | 38 | MITIGATES | 6 |
| ENABLES | 35 | EVOLVES_FROM | 4 |
| EXEMPLIFIES | 24 | CONTRADICTS | 1 |
| PROVES | 24 | | |
| FORMALIZES | 24 | | |

**Verification query** via `cognee.search(SearchType.GRAPH_COMPLETION)` for "What is Tautologia Ontológica?" returned a coherent PT-BR definition derived from the graph nodes — proof that the extraction worked and the graph is queryable end-to-end.

---

## Comparative scoreboard

| Run | Concepts | Edges | Typing source | RELATES_TO % | Notes |
|---|---|---|---|---|---|
| Pythonistic `load_vaults.py` | 145 | hundreds | LLM classifier on existing wikilinks | high | Couldn't discover new concepts |
| Era 1 Att. 1 — `OntologyGraph` | — | — | — | — | Pydantic ValidationError, never ran |
| Era 1 Att. 2 — default KG + post-process | ? | **13,659** | post-hoc keyword mapping | 16% | Many mapping gaps + LLM typos |
| Era 2 Att. 1 — Path A 10 RPM, 5/5 | — | — | — | — | Instant 429 storm, killed |
| Era 2 Att. 2 — Path A 5 RPM, 5/5 | — | — | — | — | 16 chunks then 496 errors, killed |
| Era 2 Att. 3 — **Path A 2 RPM, 1/1** | **547** | **1,844** | **Pydantic schema at extraction time** | **17%** | **Clean success, all 16 types native** |

**Key trade-off Era 1 vs Era 2:** Era 1 has 7.4× more edges. Era 2 has fewer but **schema-correct from second 1, no post-hoc keyword mapping, no LLM typos in the type names** (the JSON schema rejects them outright). Era 1's higher count includes many edges that *should* have been typed but landed in `RELATES_TO` due to keyword-map gaps or LLM typos. Era 2 trades volume for semantic precision.

---

## Decisions still open

1. **Keep `load_vaults.py` or wipe?** — It's the legacy Pythonistic loader. Still re-runs in `marvin_ops.py cmd_sync`. Should be disabled from CI loop.
2. **Index Cognee `:Concept` nodes into Marvin's Milvus** — Cognee writes to LanceDB (its own), Marvin's 7 collections untouched. Future merge?
3. **Re-run for missing docs?** — Era 2 covered 2,175 chunks. Total corpus is bigger; we don't know exact coverage. 547 concepts is already 3.7× the Pythonistic baseline — maybe enough.
4. **Self-audit's `relation_type_drift` check** — catches Cognee snake_case stragglers. Filter audit by `:Concept` label vs `:Entity`?
5. **Decide on `load-vaults/smoke_concept_model.py`** — keep as regression test (commit) or delete?
