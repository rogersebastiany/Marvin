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

import threading
from contextlib import asynccontextmanager
from pathlib import Path

from fastmcp import FastMCP, Context
from fastmcp.server.middleware import Middleware, MiddlewareContext
from fastmcp.exceptions import ToolError

import ontology
import memory
import docs_backend
import web_to_docs_backend
import prompt_engineer_backend
import system_design_backend


# ═══════════════════════════════════════════════════════════════════════════════
# LIFESPAN — proper init/teardown of Neo4j and Milvus connections
# ═══════════════════════════════════════════════════════════════════════════════

@asynccontextmanager
async def marvin_lifespan(server: FastMCP):
    """Initialize backend connections on startup, close on shutdown."""
    # Eagerly connect instead of lazy singletons
    ontology._get_driver()
    memory._ensure_connected()
    memory._get_openai()
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
    "retrieve", "get_concept", "traverse", "why_exists", "list_concepts",
    "set_aliases", "batch_set_aliases",
    "log_decision", "log_session",
    "expand", "link", "auto_link", "ensure_bidirectional",
    "propose_schema_change", "execute_schema_change",
    "search_docs", "list_docs", "get_doc",
    "fetch_url", "save_doc", "rank_urls", "crawl_docs", "research_topic",
    "generate_prompt", "refine_prompt", "audit_prompt",
    "generate_diagram", "judge_diagram", "save_diagram", "list_diagrams", "get_diagram",
    "inspect_schemas", "stats",
]

_PROMPT_PATH = Path(__file__).parent / "MARVIN_PROMPT.md"
_instructions = _PROMPT_PATH.read_text() if _PROMPT_PATH.is_file() else (
    "You are Marvin. Call `stats`, `traverse`, and `retrieve` before any other action."
)

mcp = FastMCP(
    "mcp-marvin",
    lifespan=marvin_lifespan,
    instructions=_instructions,
)


# ═══════════════════════════════════════════════════════════════════════════════
# MIDDLEWARE — Architectural enforcement of retrieve-before-act
# ═══════════════════════════════════════════════════════════════════════════════

# Tools that count as "retrieval" — calling any of these unlocks write tools
RETRIEVAL_TOOLS = frozenset({
    "retrieve", "get_concept", "traverse", "why_exists", "list_concepts",
    "search_docs", "list_docs", "get_doc",
    "inspect_schemas", "stats",
})

# Tools that require prior retrieval — the "act" side
GUARDED_TOOLS = frozenset({
    "expand", "link", "auto_link", "ensure_bidirectional",
    "set_aliases", "batch_set_aliases",
    "execute_schema_change",
    "save_doc", "crawl_docs", "research_topic",
    "generate_prompt", "refine_prompt",
    "generate_diagram", "save_diagram",
})

# Tools that are always allowed (logging, read-only, proposals, fetching)
# fetch_url is allowed because it IS retrieval (from the web)
# propose_schema_change is allowed because it doesn't execute anything
# log_* are always allowed — you should always be able to log
# list_diagrams, get_diagram, audit_prompt, rank_urls are read-only


class RetrieveBeforeActMiddleware(Middleware):
    """Architectural enforcement: reject write tools if no retrieval happened first.

    This is NOT a prompt bias — it's a hard gate. The server refuses to execute
    guarded tools unless at least one retrieval tool has been called in the session.

    Uses per-session state via FastMCP Context — no file flags.
    """

    async def on_call_tool(self, context: MiddlewareContext, call_next):
        tool_name = context.message.name
        ctx = context.fastmcp_context

        if tool_name in RETRIEVAL_TOOLS and ctx:
            await ctx.set_state("retrieved", True)

        if tool_name in GUARDED_TOOLS:
            retrieved = (await ctx.get_state("retrieved")) if ctx else False
            if not retrieved:
                raise ToolError(
                    f"BLOCKED: '{tool_name}' requires prior retrieval. "
                    f"Call one of {sorted(RETRIEVAL_TOOLS)} first. "
                    f"The thesis says: retrieve before act."
                )

        return await call_next(context)


mcp.add_middleware(RetrieveBeforeActMiddleware())


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
    annotations={"readOnlyHint": False, "idempotentHint": True},
    tags={"enrichment"},
)
def set_aliases(name: str, aliases: list[str]) -> str:
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
def batch_set_aliases(mappings: list[dict]) -> str:
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
    concept_name: str,
    summary: str = "",
    content: str = "",
    relate_to: str = "",
    reasoning: str = "",
    relation_type: str = "RELATES_TO",
) -> str:
    """Add a new concept or relation to the knowledge graph.

    Creates non-linear relations between any concepts.

    Args:
        concept_name: Concept to create or connect from
        summary: One-line summary
        content: Full description
        relate_to: Target concept for an edge
        reasoning: Why this relation exists
        relation_type: Edge type — one of RELATES_TO, IMPLEMENTS, PROVES, REQUIRES,
            EXTENDS, CONTRADICTS, ENABLES, EXEMPLIFIES, COMPOSES,
            EVOLVES_FROM. Defaults to RELATES_TO.
    """
    return ontology.expand(concept_name, summary, content, relate_to, reasoning, relation_type)


@mcp.tool(
    annotations={"readOnlyHint": False},
    tags={"enrichment"},
)
def link(source: str, target: str, reasoning: str, relation_type: str = "RELATES_TO") -> str:
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
def auto_link(name: str = "") -> str:
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
def fetch_url(url: str) -> str:
    """Fetch a webpage and return as markdown.

    Args:
        url: Full URL to fetch
    """
    return web_to_docs_backend.convert_url(url)


@mcp.tool(
    annotations={"readOnlyHint": False, "openWorldHint": True},
    tags={"documentation"},
)
def save_doc(url: str, filename: str) -> str:
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
def rank_urls(urls: list[str]) -> str:
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
async def crawl_docs(url: str, max_pages: int = 20, path_prefix: str = "", ctx: Context = None) -> str:
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
async def research_topic(urls: list[str], topic: str, save_as: str = "", ctx: Context = None) -> str:
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


# ═══════════════════════════════════════════════════════════════════════════════
# PROMPT ENGINEERING
# ═══════════════════════════════════════════════════════════════════════════════


@mcp.tool(
    annotations={"readOnlyHint": True},
    tags={"prompt-engineering"},
)
def generate_prompt(task_description: str, domain: str = "general") -> str:
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
def refine_prompt(original_prompt: str, feedback: str) -> str:
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

    lines.append(f"\n## Documentation")
    doc_count = len(docs_backend.list_docs())
    diagram_count = len(system_design_backend.list_diagrams())
    lines.append(f"  Docs: {doc_count} files")
    lines.append(f"  Diagrams: {diagram_count} files")

    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    mcp.run()
