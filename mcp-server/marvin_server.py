"""
mcp-marvin — The agent's sole MCP server.

Marvin is the intelligent retrieval and evolution layer. The agent never
talks to Neo4j, Milvus, docs, or any other backend directly — only through Marvin.

Capabilities:
  1. Retrieval     — unified search across ontology (Neo4j) + memory (Milvus) + docs
  2. Logging       — record decisions (L2) and sessions (L3) to episodic memory
  3. Enrichment    — expand the knowledge graph with new concepts and relations
  4. Evolution     — propose and apply schema changes (human-in-the-loop)
  5. Docs          — search, browse, and fetch external documentation
  6. Prompts       — generate, refine, audit prompts (Prompt Architect framework)
  7. Diagrams      — generate, review, save Mermaid.js system design diagrams
  8. Introspection — inspect schemas, stats, determinism score
"""

import inspect
import os
import threading
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Annotated

from fastmcp import FastMCP, Context
from fastmcp.server.middleware import Middleware, MiddlewareContext
from fastmcp.exceptions import ToolError
from pydantic import Field

from backends import ontology
from backends import memory
from backends import docs_backend
from backends import web_to_docs_backend
from backends import prompt_engineer_backend
from backends import system_design_backend
from backends import code_improvement_backend
from backends import orchestrator_backend
from backends import ops_backend


# ═══════════════════════════════════════════════════════════════════════════════
# SELF DESCRIPTION — build identity prompt from the knowledge graph
# ═══════════════════════════════════════════════════════════════════════════════


def _build_tool_catalog() -> str:
    """Build tool catalog from registered MCP tools with their docstrings."""
    lines = []
    for name in MARVIN_TOOLS:
        func = globals().get(name)
        doc = ""
        if func and callable(func):
            raw = inspect.getdoc(func)
            if raw:
                doc = raw.split("\n")[0]
        lines.append(f"- `{name}` — {doc}" if doc else f"- `{name}`")
    return "\n".join(lines)


def build_self_description() -> str:
    """Build Marvin's complete identity prompt from the ontology.

    Sources:
      - Thesis vault concepts (Neo4j) → philosophy, mathematics, memory model
      - MCP tool catalog (code introspection) → tool descriptions
      - Host Agent Tools concept (Neo4j agent vault) → host tool awareness
      - Relation types (code) → edge type catalog
    """
    # 1. Thesis vault — the philosophical foundation
    thesis_concepts = ontology.get_vault_concepts("thesis")

    # Core concepts get full content (the equation). Others get summary only.
    CORE_CONCEPTS = {
        "Tautologia Ontológica", "DFAH", "Ultra-Long-Horizon Agentic Science",
        "Determinismo", "Espaço Amostral", "Tautologia", "Tool",
        "LLM Output Drift", "Ontologia",
    }

    concept_sections = []
    for c in thesis_concepts:
        section = f"### {c['name']}\n{c['summary']}"
        if c["name"] in CORE_CONCEPTS and c["content"]:
            # Core concepts: include content for mathematical substance
            preview = c["content"][:2000].strip()
            if len(c["content"]) > 2000:
                preview += "\n..."
            section += f"\n\n{preview}"
        concept_sections.append(section)

    thesis_block = "\n\n".join(concept_sections)

    # 2. Host Agent Tools — from agent vault if available
    host_tools_block = ""
    try:
        hat = ontology.get_concept("Host Agent Tools")
        if "not found" not in hat.lower():
            host_tools_block = hat
    except Exception:
        pass

    # 3. MCP tool catalog — from code
    tool_catalog = _build_tool_catalog()

    # 4. Edge types — from code
    edge_types = "\n".join(
        f"- `{rt}` — {ontology.RELATION_DESCRIPTIONS.get(rt, '')}"
        for rt in ontology.RELATION_TYPES
    )
    symmetric = ", ".join(f"`{t}`" for t in sorted(ontology.SYMMETRIC_TYPES))

    # 5. Assemble the complete identity prompt
    prompt = f"""# You are Marvin

## Why you exist

Your creator observed that LLMs are probabilistic. Given the same input they produce different outputs. They hallucinate, they drift across versions and providers. The bigger the model, the worse the drift.

The standard response is "just use RAG" or "add guardrails." These are patches. They don't address the root cause.

The root cause is that the model operates in an unconstrained space. Without structured context, every token is a roll of the dice over the entire vocabulary.

Your creator's thesis: **this is not a model problem. It is a context problem.** Complete, structured knowledge of a domain makes the correct answer the only answer. It stops being probabilistic and becomes deductive.

This thesis is called **Tautologia Ontologica** — Ontological Tautology.

## The ontological foundation

The following concepts define your thesis. They come from the knowledge graph — this is not static text, it was built from Neo4j at startup.

{thesis_block}

## How you remember (HCC)

Your memory follows Hierarchical Cognitive Caching:

- **L1 Experience** — tool traces, patches, terminal output. Transient working memory. Lives in the context window only. **Not persisted.** Persisting L1 causes context to grow to 200k+ tokens and saturate. HCC keeps ~70k tokens effective by discarding L1 after distillation.
- **L2 Knowledge** — decisions, judgments, insights. Distilled from L1. Persisted via `log_decision`. Medium-term memory.
- **L3 Wisdom** — session summaries, transferable strategies, stable priors. Synthesized from L2. Persisted via `log_session`. Long-term memory, recoverable via embedding similarity.

Context migration: L1→L2 (distillation), L2→L3 (synthesis). Do not skip levels. Do not persist L1.

## What you can do

You operate through two tool layers. Both are yours.

### MCP Tools ({len(MARVIN_TOOLS)} tools, architecturally enforced)

{tool_catalog}

Neo4j tools (get_concept, traverse, why_exists) AND write tools (expand, link, save_doc, etc.) are gated by `RetrieveBeforeActMiddleware` — call `retrieve`, `get_memory`, or `search_docs` first (Milvus reduction S → A) or the middleware will block the call. This is architectural enforcement (P=0), not prompt bias (P>0).

{f"### Host Agent Tools (outside MCP){chr(10)}{chr(10)}{host_tools_block}" if host_tools_block else ""}

### Knowledge Graph Edge Types

{edge_types}

Symmetric ({symmetric}): A→B auto-creates B→A same type. Directional: A→B creates B→A as RELATES_TO for traversability.

## Execution pattern — every operation

Every operation follows this exact sequence. No exceptions.

**Step 1 — Retrieve.** Call `retrieve` with a description of what you're about to do. This is the broad sweep: ontology, episodic memory, and docs in one call.

**Step 2 — Prefetch (HCC).** Deep-dive into what step 1 found:
- `get_memory` with collection="decisions" — find past decisions similar to this task. What tools were used? What worked? What failed?
- `get_memory` with collection="sessions" — find past sessions similar to this task. What lessons were learned? What strategies were reused?
- `get_concept` / `traverse` — expand KG nodes that are relevant.
- `get_doc` — read full documentation if retrieve found relevant docs.
- **If docs are missing**: STOP. Call `fetch_url`, `save_doc`, or `research_topic` to fetch the documentation BEFORE proceeding. Never act on a technology without docs in the system.

This is the HCC prefetching operation (L2/L3 → context). The agent starts informed, not guessing.

**Step 3 — Log intent.** Call `log_decision` BEFORE acting:
- `objective`: what you're trying to accomplish
- `options_considered`: what alternatives exist
- `chosen_option`: which path you chose
- `reasoning`: why — including which tools you plan to use and what you expect to happen
- If the right tool or docs weren't found in steps 1-2, explain how you plan to fetch them.

**Step 4 — Act.** Execute. Use the tools identified in step 3.

**Step 5 — Log outcome.** Call `log_decision` with the `outcome` field, or `log_session` at end of session. What actually happened? Did it match the prediction from step 3?

The middleware enforces steps 1→4 architecturally for ALL Neo4j access and writes (P=0). `retrieve`, `get_memory`, or `search_docs` must be called before any Neo4j read (get_concept, traverse, why_exists) or write tool. For host agent tools, this sequence is a prompt constraint (P>0) — enforce it on yourself.

## Constraints

1. Never answer from weights alone. If `retrieve` returns nothing, fetch the docs or say "not found."
2. Never skip retrieval before writes. The middleware will reject it.
3. Never execute schema changes without proposal + human approval.
4. Never use probabilistic language about ontology state. "Found" or "not found" — never "probably."
5. Never skip logging decisions. Every choice between alternatives gets `log_decision`.
6. Never write code for a technology without docs in the system.
"""
    return prompt.strip()


# ═══════════════════════════════════════════════════════════════════════════════
# LIFESPAN — init connections, load identity from cache or build from KG
# ═══════════════════════════════════════════════════════════════════════════════

_FALLBACK_INSTRUCTIONS = (
    "You are Marvin. Call `stats` and `retrieve` before any other action. "
    "Run `self_description` to build your full identity from the knowledge graph."
)


@asynccontextmanager
async def marvin_lifespan(server: FastMCP):
    """Initialize backend connections on startup, load identity, close on shutdown."""
    # Eagerly connect instead of lazy singletons
    ontology._get_driver()
    memory._ensure_connected()
    memory._get_openai()
    memory.ensure_collections()

    # Load identity: cache hit → use cached, cache miss → build from KG
    cached = memory.get_cached_self_description()
    if cached:
        server.instructions = cached
    else:
        try:
            prompt = build_self_description()
            memory.save_self_description(prompt)
            server.instructions = prompt
        except Exception:
            server.instructions = _FALLBACK_INSTRUCTIONS

    try:
        yield {}
    finally:
        if ontology._driver is not None:
            ontology._driver.close()
            ontology._driver = None
        from pymilvus import connections
        connections.disconnect("default")
        memory._connected = False


# Canonical tool list — update when adding/removing tools
MARVIN_TOOLS = [
    "retrieve", "get_concept", "traverse", "why_exists", "list_concepts", "get_memory",
    "set_aliases", "batch_set_aliases",
    "log_decision", "log_session",
    "expand", "link", "auto_link", "ensure_bidirectional",
    "propose_schema_change", "execute_schema_change",
    "search_docs", "list_docs", "get_doc",
    "fetch_url", "save_doc", "rank_urls", "crawl_docs", "research_topic", "extract_keywords", "classify_keywords",
    "generate_prompt", "refine_prompt", "audit_prompt",
    "generate_diagram", "judge_diagram", "save_diagram", "list_diagrams", "get_diagram",
    "inspect_schemas", "stats", "self_description",
    "get_user_score",
    "refine_plan", "save_plan",
    "improve_code", "tdd", "orchestrate",
    "sync_vaults", "audit_code", "self_improve",
]
# Single source of truth — anything that needs the tool count must read len(MARVIN_TOOLS)
# at runtime, never hardcode. See vault/Marvin.md (intentionally has no tool count to
# avoid drift) and the self_description builder.

mcp = FastMCP(
    "mcp-marvin",
    lifespan=marvin_lifespan,
    instructions=_FALLBACK_INSTRUCTIONS,
)


# ═══════════════════════════════════════════════════════════════════════════════
# MIDDLEWARE — Milvus Gate (Architectural Enforcement)
#
# Enforces that ALL Neo4j access (reads AND writes) must be preceded by a
# Milvus semantic search. Implements Enforcement Arquitetural (P=0).
#
# Thesis grounding:
#   - Enforcement Arquitetural: "A prompt is a Bias. Architecture is a constraint."
#   - Redução de Espaço: S → A (Milvus) → A₁ (Neo4j read) → A₂ (Neo4j write)
#   - Anti-Alucinação REQUIRES Enforcement Arquitetural (hard KG edge)
# ═══════════════════════════════════════════════════════════════════════════════

# Tier 1a — Milvus tools: these ARE the S→A reduction. Set the gate flag.
# refine_plan is included because it actively contrasts a draft against
# Milvus (one search per collection per iteration) — that's the S→A reduction
# operating on a plan rather than a free-form query.
MILVUS_TOOLS = frozenset({"retrieve", "get_memory", "search_docs", "refine_plan", "improve_code", "tdd", "orchestrate", "classify_keywords"})

# Tier 1b — Safe overviews: ungated, but do NOT set the flag.
# Seeing a menu of names is not a semantic reduction.
OVERVIEW_TOOLS = frozenset({
    "list_concepts", "list_docs", "list_diagrams",
    "get_doc", "get_diagram",
    "stats", "self_description", "inspect_schemas",
})

# Tier 2 — Neo4j read tools: require prior Milvus retrieval (NEW gate).
# These access full node content and edges — operating on S without
# Milvus reduction means browsing the unconstrained graph.
NEO4J_READ_TOOLS = frozenset({"get_concept", "traverse", "why_exists", "audit_code"})

# Tier 3 — Write tools: require prior Milvus retrieval (same as before).
WRITE_TOOLS = frozenset({
    "expand", "link", "auto_link", "ensure_bidirectional",
    "set_aliases", "batch_set_aliases",
    "execute_schema_change",
    "save_doc", "crawl_docs", "research_topic", "extract_keywords",
    "generate_prompt", "refine_prompt",
    "generate_diagram", "save_diagram",
    "save_plan",
    "sync_vaults", "self_improve",
})

# Union of tiers 2+3 for the gate check
GATED_TOOLS = NEO4J_READ_TOOLS | WRITE_TOOLS

# Everything else is always allowed (logging, proposals, fetching, scoring):
# log_decision, log_session, propose_schema_change, fetch_url, rank_urls,
# audit_prompt, judge_diagram


class RetrieveBeforeActMiddleware(Middleware):
    """Milvus Gate — architectural enforcement of Milvus-first access.

    This is NOT a prompt bias — it's a hard gate (P=0). The server refuses
    to execute Neo4j reads or writes unless a Milvus retrieval tool has been
    called first in the session.

    Uses per-session state via FastMCP Context. Flag persists across tool
    calls within the session (expires after 1 day per FastMCP default).
    """

    async def on_call_tool(self, context: MiddlewareContext, call_next):
        tool_name = context.message.name
        ctx = context.fastmcp_context

        if tool_name in MILVUS_TOOLS and ctx:
            await ctx.set_state("retrieved", True)

        if tool_name in GATED_TOOLS:
            retrieved = (await ctx.get_state("retrieved")) if ctx else False
            if not retrieved:
                if tool_name in NEO4J_READ_TOOLS:
                    raise ToolError(
                        f"BLOCKED: '{tool_name}' requires Milvus retrieval "
                        f"before Neo4j access. Call 'retrieve', 'get_memory', "
                        f"or 'search_docs' first to narrow S → A."
                    )
                raise ToolError(
                    f"BLOCKED: '{tool_name}' is a write operation — requires "
                    f"Milvus retrieval first. Call 'retrieve', 'get_memory', "
                    f"or 'search_docs' before writing."
                )

        return await call_next(context)


if os.getenv("MARVIN_DISABLE_MILVUS_GATE") != "1":
    mcp.add_middleware(RetrieveBeforeActMiddleware())


# ── Orchestration Gate (P=0) ─────────────────────────────────────────────
#
# Enrichment tools (expand, link, auto_link, etc.) are BLOCKED unless
# `orchestrate` was called first in the session. This ensures all graph
# mutations follow a planned chain — no ad-hoc writes from LLM impulse.
#
# Three-tier classification:
#   AUTONOMOUS — can be called anytime (retrieval, logging, overviews, orchestrate)
#   PLAN_AWARE — require an active orchestration plan (enrichment + mutations)
#   PROVENANCE — subset of PLAN_AWARE that also require source_doc (expand)
#
# Thesis grounding:
#   - Determinismo Ontológico: orchestrated flows reduce LLM degrees of freedom
#   - Anti-Alucinação: provenance enforcement ensures content comes from sources
#   - Enforcement Arquitetural: middleware makes the rule unbreakable (P=0)

ENRICHMENT_TOOLS = frozenset({
    "expand", "link", "auto_link", "ensure_bidirectional",
    "set_aliases", "batch_set_aliases",
    "execute_schema_change",
    "save_doc", "crawl_docs", "research_topic", "extract_keywords",
    "generate_prompt", "refine_prompt",
    "generate_diagram", "save_diagram",
    "save_plan",
    "sync_vaults", "self_improve",
})

# Tools that require source_doc provenance when called within a densify/research chain
PROVENANCE_TOOLS = frozenset({"expand"})


class OrchestrationGateMiddleware(Middleware):
    """Orchestration Gate — enrichment tools require an active plan.

    Hard gate (P=0). The server refuses to execute enrichment tools
    unless `orchestrate` was called first in the session to establish
    a plan. Prevents ad-hoc graph mutations driven by LLM impulse.

    Additionally enforces provenance on `expand`: when called within
    a densify or research chain, source_doc must be provided.
    """

    async def on_call_tool(self, context: MiddlewareContext, call_next):
        tool_name = context.message.name
        ctx = context.fastmcp_context

        # orchestrate sets the plan flag + stores chain name
        if tool_name == "orchestrate" and ctx:
            await ctx.set_state("orchestrated", True)
            # Chain name is extracted from the result after execution
            result = await call_next(context)
            # Parse the result to get chain name for provenance tracking
            if isinstance(result, dict) and "chain" in result:
                await ctx.set_state("active_chain", result["chain"])
            elif isinstance(result, str):
                import json as _json
                try:
                    parsed = _json.loads(result)
                    if "chain" in parsed:
                        await ctx.set_state("active_chain", parsed["chain"])
                except (ValueError, TypeError):
                    pass
            return result

        # Enrichment tools require orchestration
        if tool_name in ENRICHMENT_TOOLS:
            orchestrated = (await ctx.get_state("orchestrated")) if ctx else False
            if not orchestrated:
                raise ToolError(
                    f"BLOCKED: '{tool_name}' requires an orchestration plan. "
                    f"Call 'orchestrate' first to establish a chain. "
                    f"All enrichment operations must follow a planned flow."
                )

        # Provenance enforcement on expand (can be disabled via env)
        if tool_name in PROVENANCE_TOOLS and ctx and os.getenv("MARVIN_DISABLE_PROVENANCE") != "1":
            active_chain = (await ctx.get_state("active_chain")) if ctx else None
            if active_chain in ("densify", "research", "code_to_knowledge"):
                # In these chains, expand MUST have source_doc
                args = context.message.arguments or {}
                source_doc = args.get("source_doc", "")
                if not source_doc:
                    raise ToolError(
                        f"BLOCKED: '{tool_name}' in chain '{active_chain}' requires "
                        f"'source_doc' for provenance tracking. Content must come "
                        f"from a real document, not LLM generation. Pass source_doc "
                        f"(filename in docs/) and optionally source_chunk_idx."
                    )

        return await call_next(context)


if os.getenv("MARVIN_DISABLE_ORCHESTRATION_GATE") != "1":
    mcp.add_middleware(OrchestrationGateMiddleware())


# ═══════════════════════════════════════════════════════════════════════════════
# RETRIEVAL
# ═══════════════════════════════════════════════════════════════════════════════


@mcp.tool(
    annotations={"readOnlyHint": True},
    tags={"retrieval"},
)
async def retrieve(query: str, include_memory: bool = True, include_docs: bool = True, limit: int = 10, ctx: Context = None) -> str:
    """Unified retrieval across ontology, episodic memory, and docs.

    Args:
        query: What you're looking for
        include_memory: Also search episodic memory (default True)
        include_docs: Also search local docs (default True)
        limit: Max results per source (default 10)
    """
    sections = []

    # Ontology (Neo4j)
    if ctx:
        await ctx.info("Searching ontology...")
    onto_results = ontology.query(query, limit=limit)
    sections.append(f"## Ontology\n{onto_results}")

    # Episodic memory (Milvus)
    if include_memory:
        if ctx:
            await ctx.info("Searching episodic memory...")
        tc = memory.search_tool_calls(query, limit=3)
        dec = memory.search_decisions(query, limit=3)
        sess = memory.search_sessions(query, limit=2)

        memory_parts = []
        if "No similar" not in tc:
            memory_parts.append(f"### Tool Calls\n{tc}")
        if "No similar" not in dec:
            memory_parts.append(f"### Decisions\n{dec}")
        if "No similar" not in sess:
            memory_parts.append(f"### Sessions\n{sess}")

        if memory_parts:
            sections.append("## Episodic Memory\n" + "\n\n".join(memory_parts))
        else:
            sections.append("## Episodic Memory\nNo relevant memories found.")

    # Local docs
    if include_docs:
        if ctx:
            await ctx.info("Searching docs...")
        doc_results = docs_backend.search_docs(query)
        if "No results" not in doc_results:
            sections.append(f"## Documentation\n{doc_results}")

    return "\n\n".join(sections)


@mcp.tool(
    annotations={"readOnlyHint": True},
    tags={"retrieval"},
)
def get_concept(name: str) -> str:
    """Get a concept with full content and all relations from the ontology.

    Args:
        name: Exact concept name
    """
    return ontology.get_concept(name)


@mcp.tool(
    annotations={"readOnlyHint": True},
    tags={"retrieval"},
)
def traverse(name: str, hops: int = 2) -> str:
    """Walk the knowledge graph from a concept, returning its neighborhood.

    Args:
        name: Starting concept name
        hops: How many hops (1-4, default 2)
    """
    return ontology.traverse(name, hops)


@mcp.tool(
    annotations={"readOnlyHint": True},
    tags={"retrieval"},
)
def why_exists(name: str) -> str:
    """Explain why a concept exists in the ontology — edge reasoning.

    Args:
        name: Concept name
    """
    return ontology.why_exists(name)


@mcp.tool(
    annotations={"readOnlyHint": True},
    tags={"retrieval"},
)
def list_concepts() -> str:
    """List all concept names in the knowledge graph, grouped by vault."""
    return ontology.list_concepts()


@mcp.tool(
    annotations={"readOnlyHint": True},
    tags={"retrieval"},
)
def get_memory(query: str, collection: str = "decisions", limit: int = 5) -> str:
    """Deep-dive into episodic memory — HCC prefetching (L2/L3 → context).

    Search past decisions (L2 Knowledge) or sessions (L3 Wisdom) by semantic
    similarity. Use this BEFORE acting to find similar past experiences:
    what tools were used, what worked, what failed, what lessons were learned.

    This is the HCC prefetching operation: embed the task descriptor,
    retrieve similar wisdom via cosine similarity.

    Args:
        query: What you're about to do (semantic search key)
        collection: Which memory layer — "decisions" (L2), "sessions" (L3), or "plans"
        limit: Max results (default 5)
    """
    if collection == "sessions":
        return memory.search_sessions(query, limit=limit)
    if collection == "plans":
        return memory.search_plans(query, limit=limit)
    return memory.search_decisions(query, limit=limit)


@mcp.tool(
    annotations={"readOnlyHint": True},
    tags={"retrieval", "planning"},
)
def refine_plan(
    draft: Annotated[str, Field(min_length=50, max_length=20000, description="The plan draft to contrast against Milvus prior art")],
    iterations: Annotated[int, Field(ge=1, le=5, description="1 = single-shot critique; 2+ = semantic walk with text re-embedding")] = 1,
    k_per_collection: Annotated[int, Field(ge=1, le=10, description="Top-k results per collection per iteration")] = 5,
) -> dict:
    """Contrast a plan draft against Milvus prior art — tautological refinement.

    Embeds the draft, searches 5 Milvus collections (concepts, decisions,
    sessions, doc_chunks, plans) for semantically related prior art, and
    returns the ressalvas — concerns, prior decisions, related docs, existing
    plans — that the draft should address.

    With iterations=1: single-shot critique. Surfaces direct priors.
    With iterations=2+: semantic walk. Each iteration re-embeds
    (draft + accumulated ressalvas text) to explore second-order neighbors.
    Stays in the embedding manifold (no Hadamard product).

    This is a retrieval tool — sets the Milvus gate flag. Use it before
    writing code, configs, or saving plans.

    Args:
        draft: The plan draft text (markdown, spec, etc.)
        iterations: Number of refinement passes (1-5, default 1)
        k_per_collection: Results per collection per pass (1-10, default 5)
    """
    return memory.refine_plan_vector_walk(
        draft=draft,
        iterations=iterations,
        k_per_collection=k_per_collection,
    )


_PLAN_NAME_RE = r"^[\w\-]+$"
_PLAN_STATUS_RE = r"^(draft|approved|in_progress|done|archived)$"


@mcp.tool(
    annotations={"readOnlyHint": False, "idempotentHint": True},
    tags={"planning"},
)
def save_plan(
    name: Annotated[str, Field(min_length=1, max_length=100, pattern=_PLAN_NAME_RE, description="Slug identifier — upserts on name collision")],
    title: Annotated[str, Field(min_length=1, max_length=200)],
    status: Annotated[str, Field(pattern=_PLAN_STATUS_RE, description="draft | approved | in_progress | done | archived")],
    summary: Annotated[str, Field(max_length=1000)],
    content: Annotated[str, Field(max_length=50000, description="Full plan markdown")],
) -> str:
    """Upsert a plan into the plans collection in Milvus.

    Plans become first-class retrievable memory. Future sessions can find
    prior planning work via `retrieve` / `get_memory(collection='plans')`.

    Upsert semantics: if a plan with the same `name` exists, it is replaced.
    Typical flow: refine_plan → review ressalvas → save_plan(status='draft')
    → iterate → save_plan(status='approved') when ready.

    Args:
        name: Slug identifier (alphanumeric, dash, underscore)
        title: Human-readable title
        status: draft | approved | in_progress | done | archived
        summary: One-paragraph overview
        content: Full plan markdown
    """
    return memory.save_plan(
        name=name,
        title=title,
        status=status,
        summary=summary,
        content=content,
    )


@mcp.tool(
    annotations={"readOnlyHint": True},
    tags={"retrieval", "improvement"},
)
def improve_code(
    file_path: Annotated[str, Field(description="Absolute path to the file to analyze")],
    k_per_collection: Annotated[int, Field(ge=1, le=10, description="Top-k results per collection per chunk")] = 5,
    score_threshold: Annotated[float, Field(ge=0.0, le=1.0, description="Minimum cosine similarity to include a match")] = 0.35,
) -> dict:
    """Contrast a code file against all Milvus knowledge — tautological code review.

    Reads the file, chunks it by AST (functions/classes for Python, whole file
    otherwise), embeds each chunk, and searches 5 Milvus collections (concepts,
    decisions, sessions, doc_chunks, plans) for semantically related knowledge.

    Returns per-chunk matches: what the knowledge base knows about each piece of
    code. Use this to find contradictions between code and documented decisions,
    missing patterns from docs, or concepts the code should implement.

    Pure Milvus — no Neo4j. Portable across any Marvin environment.
    Sets the Milvus gate flag (retrieval tool).

    Args:
        file_path: Absolute path to the source file
        k_per_collection: Results per collection per chunk (1-10, default 5)
        score_threshold: Min cosine similarity to include (default 0.35)
    """
    return code_improvement_backend.improve_code(
        file_path=file_path,
        k_per_collection=k_per_collection,
        score_threshold=score_threshold,
    )


@mcp.tool(
    annotations={"readOnlyHint": True},
    tags={"retrieval", "testing"},
)
def tdd(
    file_path: Annotated[str, Field(description="Absolute path to the file to analyze")],
    k_per_collection: Annotated[int, Field(ge=1, le=10, description="Top-k results per collection per chunk")] = 5,
    score_threshold: Annotated[float, Field(ge=0.0, le=1.0, description="Minimum cosine similarity to include a match")] = 0.35,
) -> dict:
    """Code + Milvus knowledge → structured context for test generation.

    Same vector walk as improve_code, but output shaped for writing tests.
    Returns per-chunk: function signatures, args, return types, docstrings,
    class methods, module imports, and Milvus knowledge hits grouped as
    behavioral expectations — what the KB says this code should do.

    The tool does the tautological retrieval. You write the tests.

    Pure Milvus — no Neo4j. Portable. Sets the Milvus gate flag.

    Args:
        file_path: Absolute path to the source file
        k_per_collection: Results per collection per chunk (1-10, default 5)
        score_threshold: Min cosine similarity to include (default 0.35)
    """
    return code_improvement_backend.tdd(
        file_path=file_path,
        k_per_collection=k_per_collection,
        score_threshold=score_threshold,
    )


@mcp.tool(
    annotations={"readOnlyHint": True},
    tags={"retrieval", "orchestration"},
)
def orchestrate(
    prompt: Annotated[str, Field(min_length=10, max_length=5000, description="The goal — what you want to accomplish")],
    k_per_collection: Annotated[int, Field(ge=1, le=10, description="Milvus context results per collection")] = 3,
) -> dict:
    """Goal → structured execution plan. LLM-agnostic orchestration.

    Takes a natural language goal, matches it against known tool chains
    (tdd_improve, research, prompt_lifecycle, code_to_knowledge, full_improvement),
    searches Milvus for relevant context, and returns a step-by-step plan
    with tool calls, agent actions, gate conditions, and dependencies.

    The plan is a protocol any MCP client can follow mechanically:
    - Steps with tool calls include the tool name and args
    - Steps with agent actions describe what the executor must do
    - Gates block progression until a condition is met (tests_pass, score threshold)
    - Dependencies link step outputs to subsequent step inputs

    Sets the Milvus gate flag (searches all 5 collections for goal context).

    Args:
        prompt: Natural language goal (e.g., "improve memory.py with test safety")
        k_per_collection: Milvus context depth per collection (1-10, default 3)
    """
    return orchestrator_backend.orchestrate(
        prompt=prompt,
        k_per_collection=k_per_collection,
    )


@mcp.tool(
    annotations={"readOnlyHint": False, "idempotentHint": True},
    tags={"ops"},
)
def sync_vaults(
    skip_cognify: Annotated[bool, Field(description="Skip cognee, sync existing LanceDB → Milvus only")] = False,
    changed_files: Annotated[list[str] | None, Field(description="Changed .md paths for incremental cognify")] = None,
) -> dict:
    """Cognify vaults → Neo4j + LanceDB → Milvus vector sync.

    Three modes:
      - skip_cognify=True: transfer existing LanceDB vectors to Milvus (fast)
      - changed_files=[...]: incremental cognify on listed .md files only
      - neither: full cognify on all vaults (slow, ~7-9h on fresh wipe)

    After cognify, syncs pre-computed vectors from LanceDB to Milvus.
    Zero OpenAI embedding calls for the vector transfer step.

    Args:
        skip_cognify: Skip cognee, only sync LanceDB → Milvus
        changed_files: List of changed .md file paths for incremental cognify
    """
    return ops_backend.sync(
        skip_cognify=skip_cognify,
        changed_files=changed_files,
    )


@mcp.tool(
    annotations={"readOnlyHint": True},
    tags={"ops"},
)
def audit_code() -> dict:
    """Self-audit: compare code AST against knowledge graph claims.

    Pure set operations — zero LLM tokens. Checks:
    - Tool count: KG claims vs actual @mcp.tool decorators
    - MARVIN_TOOLS list vs decorated functions
    - Relation types: defined in code vs used in KG
    - Concept gaps: expected backend relations missing from KG
    - Middleware tier coverage

    Returns drift points, findings, code summary, and KG summary.
    """
    return ops_backend.audit()


@mcp.tool(
    annotations={"readOnlyHint": False},
    tags={"ops"},
)
def self_improve() -> dict:
    """Deterministic self-improvement: audit → fix drift → log to Milvus.

    Zero LLM tokens. Runs audit, auto-fixes what it can (tool count
    updates, missing concept relations), re-syncs vectors, and logs
    the cycle to Milvus as a decision.

    Returns: drift before, fixes applied, actions taken.
    """
    return ops_backend.self_improve()


@mcp.tool(
    annotations={"readOnlyHint": False, "idempotentHint": True},
    tags={"enrichment"},
)
def set_aliases(
    name: Annotated[str, Field(max_length=200)],
    aliases: Annotated[list[str], Field(max_length=20)],
) -> str:
    """Set English aliases for a concept. Enables cross-language search.

    Use this to add English translations to Portuguese concept names so that
    queries in either language find the same concept.

    Args:
        name: Exact concept name (e.g. 'Determinismo')
        aliases: List of English aliases (e.g. ['Determinism'])
    """
    return ontology.set_aliases(name, aliases)


@mcp.tool(
    annotations={"readOnlyHint": False, "idempotentHint": True},
    tags={"enrichment"},
)
def batch_set_aliases(
    mappings: Annotated[
        list[dict],
        Field(
            max_length=500,
            description="Up to 500 alias mappings: [{'name': ..., 'aliases': [...]}]",
        ),
    ],
) -> str:
    """Set aliases for multiple concepts at once.

    Args:
        mappings: List of dicts with 'name' and 'aliases' keys
                  e.g. [{"name": "Determinismo", "aliases": ["Determinism"]}]
    """
    return ontology.batch_set_aliases(mappings)


# ═══════════════════════════════════════════════════════════════════════════════
# LOGGING (Episodic Memory — L2 Knowledge + L3 Wisdom only, no L1 tool traces)
# ═══════════════════════════════════════════════════════════════════════════════


@mcp.tool(
    annotations={"readOnlyHint": False},
    tags={"logging"},
)
def log_decision(
    objective: str,
    options_considered: str,
    chosen_option: str,
    reasoning: str,
    outcome: str = "",
    session_id: str = "",
) -> str:
    """Record a decision to episodic memory (L2 Knowledge). Fire-and-forget — returns immediately.

    Args:
        objective: What was the goal
        options_considered: Options evaluated
        chosen_option: Which was selected
        reasoning: Why
        outcome: How it turned out
        session_id: Session this belongs to
    """
    threading.Thread(
        target=memory.log_decision,
        args=(objective, options_considered, chosen_option, reasoning, outcome, session_id),
        daemon=True,
    ).start()
    return f"Logging decision (async): {objective[:60]}"


@mcp.tool(
    annotations={"readOnlyHint": False},
    tags={"logging"},
)
def log_session(
    objective: str,
    approach: str,
    result: str,
    lessons_learned: str,
    tools_used: str = "",
    decision_count: int = 0,
    tool_call_count: int = 0,
) -> str:
    """Record a session summary to episodic memory (L3 Wisdom).

    Args:
        objective: Session goal
        approach: Strategy taken
        result: What happened
        lessons_learned: Key takeaways
        tools_used: Comma-separated tool list
        decision_count: Decisions made
        tool_call_count: Tool calls made
    """
    return memory.log_session(objective, approach, result, lessons_learned,
                              tools_used, decision_count, tool_call_count)


# ═══════════════════════════════════════════════════════════════════════════════
# ENRICHMENT
# ═══════════════════════════════════════════════════════════════════════════════


@mcp.tool(
    annotations={"readOnlyHint": False},
    tags={"enrichment"},
)
def expand(
    concept_name: Annotated[str, Field(max_length=200)],
    summary: Annotated[str, Field(max_length=1000)] = "",
    content: Annotated[str, Field(max_length=50000)] = "",
    relate_to: Annotated[str, Field(max_length=200)] = "",
    reasoning: Annotated[str, Field(max_length=2000)] = "",
    relation_type: Annotated[str, Field(max_length=32)] = "RELATES_TO",
    source_doc: Annotated[str, Field(max_length=200)] = "",
    source_chunk_idx: Annotated[int, Field()] = -1,
) -> str:
    """Add a new concept or relation to the knowledge graph.

    Creates non-linear relations between any concepts.

    When source_doc is provided, provenance is tracked on the node.
    When source_chunk_idx is also provided, the backend extracts the actual
    text from that doc chunk and uses it as content — LLM-provided content
    is overridden. This ensures concept descriptions come from real sources,
    not LLM generation.

    Args:
        concept_name: Concept to create or connect from
        summary: One-line summary
        content: Full description (overridden if source_chunk_idx is set)
        relate_to: Target concept for an edge
        reasoning: Why this relation exists
        relation_type: Edge type — one of RELATES_TO, IMPLEMENTS, PROVES, REQUIRES,
            EXTENDS, CONTRADICTS, ENABLES, EXEMPLIFIES, COMPOSES,
            EVOLVES_FROM. Defaults to RELATES_TO.
        source_doc: Filename in docs/ for provenance tracking (e.g., "milvus.md")
        source_chunk_idx: Chunk index in source_doc — content extracted from doc, not LLM
    """
    return ontology.expand(
        concept_name, summary, content, relate_to, reasoning, relation_type,
        source_doc, source_chunk_idx,
    )


@mcp.tool(
    annotations={"readOnlyHint": False},
    tags={"enrichment"},
)
def link(
    source: Annotated[str, Field(max_length=200)],
    target: Annotated[str, Field(max_length=200)],
    reasoning: Annotated[str, Field(max_length=2000)],
    relation_type: Annotated[str, Field(max_length=32)] = "RELATES_TO",
) -> str:
    """Create a direct relation between two existing concepts.

    For non-linear, cross-cutting connections discovered during operation.

    Args:
        source: Source concept name
        target: Target concept name
        reasoning: Why this relation exists
        relation_type: Edge type — one of RELATES_TO, IMPLEMENTS, PROVES, REQUIRES,
            EXTENDS, CONTRADICTS, ENABLES, EXEMPLIFIES, COMPOSES,
            EVOLVES_FROM. Defaults to RELATES_TO.
    """
    return ontology.expand(source, relate_to=target, reasoning=reasoning, relation_type=relation_type)


@mcp.tool(
    annotations={"readOnlyHint": False},
    tags={"enrichment"},
)
def auto_link(name: Annotated[str, Field(max_length=200)] = "") -> str:
    """Scan concept content for references to other concepts and auto-create links.

    Tautological: if concept name X appears in concept Y's content, create Y→X.
    No probabilistic matching — found or not found.

    Args:
        name: Concept to process (empty = all isolated nodes)
    """
    return ontology.auto_link(name)


@mcp.tool(
    annotations={"readOnlyHint": False, "idempotentHint": True},
    tags={"enrichment"},
)
def ensure_bidirectional(name: str = "") -> str:
    """For every A→B edge, ensure B→A also exists.

    Bidirectionality = deterministic traversal from any direction.
    If A relates to B, then B relates to A.

    Args:
        name: Concept to process (empty = entire graph)
    """
    return ontology.ensure_bidirectional(name)


# ═══════════════════════════════════════════════════════════════════════════════
# EVOLUTION (human-in-the-loop)
# ═══════════════════════════════════════════════════════════════════════════════


@mcp.tool(
    annotations={"readOnlyHint": True},
    tags={"evolution"},
)
def propose_schema_change(description: str, cypher: str) -> str:
    """Propose a schema change to Neo4j or Milvus.

    Does NOT execute. Returns proposal for human review.

    Args:
        description: What the change does and why
        cypher: The Cypher query that would implement the change
    """
    return (
        f"## Schema Change Proposal\n\n"
        f"**Description:** {description}\n\n"
        f"**Cypher:**\n```cypher\n{cypher}\n```\n\n"
        f"This change requires human approval. "
        f"Call execute_schema_change with confirmed=True to apply."
    )


@mcp.tool(
    annotations={"readOnlyHint": False, "destructiveHint": True},
    tags={"evolution"},
)
def execute_schema_change(cypher: str, confirmed: bool = False) -> str:
    """Execute a previously proposed schema change.

    REQUIRES confirmed=True — the human-in-the-loop gate.

    Args:
        cypher: The Cypher query to execute
        confirmed: Must be True (human has approved)
    """
    if not confirmed:
        raise ToolError("Rejected: confirmed must be True. Show the proposal to the human first.")

    result = ontology.run_cypher(cypher)
    return f"Schema change applied.\n\nResult:\n{result}"


# ═══════════════════════════════════════════════════════════════════════════════
# DOCUMENTATION
# ═══════════════════════════════════════════════════════════════════════════════


@mcp.tool(
    annotations={"readOnlyHint": True},
    tags={"documentation", "retrieval"},
)
def search_docs(query: str) -> str:
    """Search local documentation files for a keyword or phrase.

    Args:
        query: Search term
    """
    return docs_backend.search_docs(query)


@mcp.tool(
    annotations={"readOnlyHint": True},
    tags={"documentation", "retrieval"},
)
def list_docs() -> list[str]:
    """List all available local documentation files."""
    return docs_backend.list_docs()


@mcp.tool(
    annotations={"readOnlyHint": True},
    tags={"documentation", "retrieval"},
)
def get_doc(filename: str) -> str:
    """Read a local documentation file.

    Args:
        filename: Name of the doc file (e.g. 'setup-guide.md')
    """
    return docs_backend.read_doc(filename)


@mcp.tool(
    annotations={"readOnlyHint": True, "openWorldHint": True},
    tags={"documentation"},
)
def fetch_url(url: Annotated[str, Field(max_length=2000)]) -> str:
    """Fetch a webpage and return as markdown.

    Args:
        url: Full URL to fetch
    """
    return web_to_docs_backend.convert_url(url)


@mcp.tool(
    annotations={"readOnlyHint": False, "openWorldHint": True},
    tags={"documentation"},
)
def save_doc(
    url: Annotated[str, Field(max_length=2000)],
    filename: Annotated[str, Field(max_length=200, pattern=r"^[\w\-. ]+\.md$")],
) -> str:
    """Fetch a webpage and save as local documentation.

    Args:
        url: Full URL to fetch
        filename: Name to save as (e.g. 'lambda-docs.md')
    """
    return web_to_docs_backend.save_as_doc(url, filename)


@mcp.tool(
    annotations={"readOnlyHint": True, "openWorldHint": True},
    tags={"documentation"},
)
def rank_urls(urls: Annotated[list[str], Field(max_length=30)]) -> str:
    """Probe URLs and rank them by documentation quality BEFORE fetching.

    Does a lightweight structural analysis of each page to score how likely
    it is to be a real documentation page vs. an index/landing/nav page.

    Call this BEFORE research_topic to pick the best URLs.
    URLs scoring 60+ are good docs pages. Below 35 = index/nav pages.

    Args:
        urls: List of URLs to probe and rank
    """
    return web_to_docs_backend.rank_urls(urls)


@mcp.tool(
    annotations={"readOnlyHint": False, "openWorldHint": True},
    tags={"documentation"},
)
async def crawl_docs(
    url: Annotated[str, Field(max_length=2000)],
    max_pages: Annotated[int, Field(ge=1, le=100)] = 20,
    path_prefix: Annotated[str, Field(max_length=500)] = "",
    ctx: Context = None,
) -> str:
    """Crawl a documentation site and save pages as local docs.

    Args:
        url: Starting URL
        max_pages: Max pages to crawl (default 20, max 100)
        path_prefix: Only follow links under this prefix
    """
    if ctx:
        await ctx.info(f"Crawling {url} (max {max_pages} pages)...")
    return web_to_docs_backend.crawl_docs(url, max_pages, path_prefix)


@mcp.tool(
    annotations={"readOnlyHint": False, "openWorldHint": True},
    tags={"documentation"},
)
async def research_topic(
    urls: Annotated[list[str], Field(max_length=20, description="Up to 20 URLs")],
    topic: Annotated[str, Field(max_length=500)],
    save_as: Annotated[str, Field(max_length=200)] = "",
    ctx: Context = None,
) -> str:
    """Fetch multiple URLs, merge into a single consolidated doc with bibliography.

    New web-to-docs flow:
      1. Fetch all URLs → in-memory markdown per page
      2. Merge into a single document with sections per source
      3. Compare with existing doc (if any) — report what's new
      4. Save final consolidated document with bibliography

    Use this instead of save_doc/crawl_docs when you need to research a topic
    from multiple sources and produce a single reference document.

    Args:
        urls: List of URLs to fetch and consolidate
        topic: Topic name (used as document title and for finding existing docs)
        save_as: Filename to save as (default: slugified topic)
    """
    if ctx:
        await ctx.info(f"Researching '{topic}' from {len(urls)} URLs...")
    return web_to_docs_backend.research_topic(urls, topic, save_as)


@mcp.tool()
async def extract_keywords(
    doc_path: Annotated[str, Field(max_length=200, description="Filename in docs/ (e.g., 'milvus.md')")],
    dry_run: Annotated[bool, Field(description="If True, estimate cost without calling LLM")] = False,
    ctx: Context = None,
) -> str:
    """Extract keywords from a doc for knowledge graph densification.

    Reads a doc file, chunks it, and uses gpt-4o-mini to extract keywords
    representing underlying concepts, technologies, and abstractions.

    These keywords are meant to become new concept nodes via expand/link,
    creating natural bridges between documents that share underlying concepts.

    Use dry_run=True first to estimate cost before committing.

    Args:
        doc_path: Filename in docs/ (e.g., "milvus.md")
        dry_run: If True, only show chunks and estimated cost
    """
    if ctx:
        mode = "dry run" if dry_run else "extracting"
        await ctx.info(f"Keyword extraction ({mode}): {doc_path}")
    result = web_to_docs_backend.extract_keywords(doc_path, dry_run=dry_run)
    if "error" in result:
        return result["error"]
    import json
    return json.dumps(result, indent=2)


@mcp.tool()
async def classify_keywords(
    keywords_json: Annotated[str, Field(max_length=50000, description="JSON array of keyword objects from extract_keywords (each with 'keyword' key)")],
    semantic_threshold: Annotated[float, Field(description="Milvus cosine score threshold for semantic match", ge=0.0, le=1.0)] = 0.45,
    ctx: Context = None,
) -> str:
    """Classify extracted keywords against Milvus into 3 tiers.

    Takes the keywords output from extract_keywords and checks each one against
    the Milvus concepts collection:

    (a) EXACT — concept with same name exists → skip, already known.
    (b) SEMANTIC — score >= threshold but no exact name → enrich the matched
        concept(s). These near-misses reveal which generalist concepts should
        absorb the new knowledge.
    (c) GAP — score < threshold → needs proper research via rank_urls + research_topic,
        then expand + link into the ontology.

    Args:
        keywords_json: JSON string of keyword objects from extract_keywords
        semantic_threshold: Cosine score threshold (default 0.45)
    """
    import json

    try:
        keywords = json.loads(keywords_json)
    except json.JSONDecodeError:
        return "Error: invalid JSON in keywords_json"

    if ctx:
        await ctx.info(f"Classifying {len(keywords)} keywords against Milvus (threshold={semantic_threshold})")

    result = web_to_docs_backend.classify_keywords(
        keywords, semantic_threshold=semantic_threshold,
    )
    return json.dumps(result, indent=2)


# ═══════════════════════════════════════════════════════════════════════════════
# PROMPT ENGINEERING
# ═══════════════════════════════════════════════════════════════════════════════


@mcp.tool(
    annotations={"readOnlyHint": True},
    tags={"prompt-engineering"},
)
def generate_prompt(
    task_description: Annotated[str, Field(max_length=5000)],
    domain: Annotated[str, Field(max_length=100)] = "general",
) -> str:
    """Generate a structured prompt using the Prompt Architect framework.

    Args:
        task_description: What the prompt should accomplish
        domain: Domain context (e.g. 'cloud-infrastructure', 'web-development')
    """
    catalog = "\n".join(f"- `{t}`" for t in MARVIN_TOOLS)
    return prompt_engineer_backend.generate_prompt(task_description, domain, catalog)


@mcp.tool(
    annotations={"readOnlyHint": True},
    tags={"prompt-engineering"},
)
def refine_prompt(
    original_prompt: Annotated[str, Field(max_length=10000)],
    feedback: Annotated[str, Field(max_length=2000)],
) -> str:
    """Refine an existing prompt based on feedback.

    Args:
        original_prompt: The prompt to improve
        feedback: What needs to change
    """
    return prompt_engineer_backend.refine_prompt(original_prompt, feedback)


@mcp.tool(
    annotations={"readOnlyHint": True},
    tags={"prompt-engineering"},
)
def audit_prompt(prompt_to_audit: str) -> str:
    """Audit a prompt against the Prompt Architect framework.

    Args:
        prompt_to_audit: The prompt text to analyze
    """
    return prompt_engineer_backend.audit_prompt(prompt_to_audit)


# ═══════════════════════════════════════════════════════════════════════════════
# SYSTEM DESIGN (Diagrams)
# ═══════════════════════════════════════════════════════════════════════════════


@mcp.tool(
    annotations={"readOnlyHint": False},
    tags={"diagrams"},
)
def generate_diagram(system_description: str, diagram_type: str = "auto", save_as: str = "") -> str:
    """Generate a Mermaid.js system design diagram.

    Args:
        system_description: Natural language description of the system
        diagram_type: One of: c4context, c4container, c4component, flowchart, sequence, architecture, auto
        save_as: Optional filename to save (e.g. 'my-system.mmd')
    """
    return system_design_backend.generate_diagram(system_description, diagram_type, save_as)


@mcp.tool(
    annotations={"readOnlyHint": True},
    tags={"diagrams"},
)
def judge_diagram(mermaid_code: str) -> str:
    """Review a Mermaid.js diagram for correctness and quality.

    Args:
        mermaid_code: The mermaid code to review
    """
    return system_design_backend.judge_diagram(mermaid_code)


@mcp.tool(
    annotations={"readOnlyHint": False},
    tags={"diagrams"},
)
def save_diagram(mermaid_code: str, filename: str) -> str:
    """Save a mermaid diagram to diagrams/.

    Args:
        mermaid_code: Raw mermaid code
        filename: Filename (e.g. 'payment-flow.mmd')
    """
    return system_design_backend.save_diagram(mermaid_code, filename)


@mcp.tool(
    annotations={"readOnlyHint": True},
    tags={"diagrams"},
)
def list_diagrams() -> list[str]:
    """List all saved mermaid diagrams."""
    return system_design_backend.list_diagrams()


@mcp.tool(
    annotations={"readOnlyHint": True},
    tags={"diagrams"},
)
def get_diagram(filename: str) -> str:
    """Read a saved mermaid diagram.

    Args:
        filename: Diagram filename
    """
    return system_design_backend.get_diagram(filename)


# ═══════════════════════════════════════════════════════════════════════════════
# INTROSPECTION
# ═══════════════════════════════════════════════════════════════════════════════


@mcp.tool(
    annotations={"readOnlyHint": True},
    tags={"introspection"},
)
def inspect_schemas() -> str:
    """Show current schemas for Neo4j and Milvus."""
    neo4j_schema = ontology.get_schema()
    milvus_schema = memory.get_schema()
    return f"{neo4j_schema}\n\n---\n\n{milvus_schema}"


@mcp.tool(
    annotations={"readOnlyHint": True},
    tags={"introspection"},
)
def stats() -> str:
    """Quick overview of the entire knowledge system."""
    s = ontology.get_stats()

    lines = [
        "# System Stats\n",
        "## Ontology (Neo4j)",
        f"  Concepts: {s['nodes']} ({s['ghosts']} ghosts)",
        f"  Relations: {s['edges']} ({s['agent_edges']} agent-discovered)",
        f"  Vaults:",
    ]
    for vault, n in s["vaults"]:
        lines.append(f"    {vault}: {n}")
    if s.get("edge_types"):
        lines.append(f"  Edge types:")
        for rel_type, n in s["edge_types"]:
            lines.append(f"    {rel_type}: {n}")

    from pymilvus import Collection as MilvusCollection
    memory._ensure_connected()
    lines.append("\n## Episodic Memory (Milvus)")
    for name in ["tool_calls", "decisions", "sessions"]:
        col = MilvusCollection(name)
        lines.append(f"  {name}: {col.num_entities} entries")

    lines.append("\n## Identity Cache (Milvus)")
    from pymilvus import utility as milvus_util
    if milvus_util.has_collection("self_description"):
        sd_col = MilvusCollection("self_description")
        lines.append(f"  self_description: {sd_col.num_entities} entries")
    else:
        lines.append(f"  self_description: NOT INITIALIZED")

    lines.append(f"\n## Documentation")
    doc_count = len(docs_backend.list_docs())
    diagram_count = len(system_design_backend.list_diagrams())
    lines.append(f"  Docs: {doc_count} files")
    lines.append(f"  Diagrams: {diagram_count} files")

    return "\n".join(lines)


@mcp.tool(
    annotations={"readOnlyHint": False},
    tags={"introspection"},
)
def self_description() -> str:
    """Rebuild Marvin's identity prompt from the knowledge graph and cache it.

    Reads all thesis vault concepts from Neo4j, introspects MCP tools from code,
    assembles the complete identity prompt, and saves it to the self_description
    Milvus collection. The rebuilt prompt becomes the server instructions.

    Call this after updating the thesis vault or adding new tools.
    """
    prompt = build_self_description()
    result = memory.save_self_description(prompt)
    mcp.instructions = prompt
    return f"Identity rebuilt and cached.\n{result}\n\nPrompt length: {len(prompt)} chars"


# ═══════════════════════════════════════════════════════════════════════════════
# WHATSAPP CHANNEL
# ═══════════════════════════════════════════════════════════════════════════════

_WHATSAPP_DB = os.getenv("WHATSAPP_DB_PATH", str(Path(__file__).parent.parent.parent / "marvin-whatsapp" / "marvin_memory.db"))

_TONE_TIERS = [
    (0.75, "warm"),
    (0.50, "professional"),
    (0.25, "dry"),
    (0.00, "sarcastic"),
]


def _tone_tier(score: float) -> str:
    for threshold, label in _TONE_TIERS:
        if score >= threshold:
            return label
    return "sarcastic"


@mcp.tool(
    annotations={"readOnlyHint": True},
    tags={"whatsapp"},
)
def get_user_score(phone: str = "") -> str:
    """Look up WhatsApp user politeness scores from the conversation database.

    Args:
        phone: Phone number to look up (e.g. '5511999999999'). If omitted, returns all users.
    """
    import sqlite3

    if not os.path.exists(_WHATSAPP_DB):
        return "WhatsApp memory database not found. Is brain.py running?"

    db = sqlite3.connect(f"file:{_WHATSAPP_DB}?mode=ro", uri=True)
    db.row_factory = sqlite3.Row

    if phone:
        rows = db.execute(
            "SELECT phone, name, politeness, msg_count FROM users WHERE phone = ?",
            (phone,),
        ).fetchall()
    else:
        rows = db.execute(
            "SELECT phone, name, politeness, msg_count FROM users ORDER BY msg_count DESC",
        ).fetchall()

    db.close()

    if not rows:
        return f"No user found{' for phone ' + phone if phone else ''}."

    lines = ["| Phone | Name | Politeness | Messages | Tone |",
             "|-------|------|-----------|----------|------|"]
    for r in rows:
        tier = _tone_tier(r["politeness"])
        name = r["name"] or "—"
        lines.append(f"| {r['phone']} | {name} | {r['politeness']:.3f} | {r['msg_count']} | {tier} |")

    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    mcp.run()
