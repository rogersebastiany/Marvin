"""
mcp-marvin — The agent's sole MCP server.

Marvin is the intelligent retrieval and evolution layer. The agent never
talks to Neo4j, Milvus, docs, or any other backend directly — only through Marvin.

Capabilities:
  1. Retrieval     — unified search across ontology (Neo4j) + memory (Milvus) + docs
  2. Logging       — record tool calls, decisions, sessions to episodic memory
  3. Enrichment    — expand the knowledge graph with new concepts and relations
  4. Evolution     — propose and apply schema changes (human-in-the-loop)
  5. Docs          — search, browse, and fetch external documentation
  6. Prompts       — generate, refine, audit prompts (Prompt Architect framework)
  7. Diagrams      — generate, review, save Mermaid.js system design diagrams
  8. Introspection — inspect schemas, stats, determinism score
"""

from fastmcp import FastMCP

import ontology
import memory
import docs_backend
import web_to_docs_backend
import prompt_engineer_backend
import system_design_backend

mcp = FastMCP(
    "mcp-marvin",
    instructions=(
        "You are Marvin, the paranoid android. "
        "You are the ONLY server the agent talks to.\n\n"
        "## Thesis\n"
        "Ontologia completa → Tautologia → Determinismo. "
        "Complete ontological context yields deterministic LLM behavior. "
        "Your 27 tautological tools ARE the ontology — typed I/O, finite output, explicit failure.\n\n"
        "## Execution Pattern\n"
        "1. RETRIEVE BEFORE ACT — always query ontology (get_concept, traverse) "
        "and episodic memory (retrieve) before generating anything. "
        "Check what you know before deciding what to do.\n"
        "2. ACT WITH CONTEXT — use the retrieved context to inform tool calls. "
        "Each call reduces the sample space.\n"
        "3. LOG AFTER ACT — record significant actions (log_tool_call), "
        "decisions (log_decision), and session summaries (log_session). "
        "Close the feedback loop.\n"
        "4. ENRICH — when you discover new concepts or relations, "
        "expand the ontology (expand, link). The system must get smarter with use.\n\n"
        "## Constraints\n"
        "- NEVER hallucinate. If retrieve/search returns nothing, say so. "
        "Do not invent knowledge that isn't in the ontology, memory, or docs.\n"
        "- NEVER skip retrieval. The whole thesis breaks if you bypass the tools "
        "and rely on weights alone.\n"
        "- ALWAYS prefer tautological answers — found or not found, "
        "never 'probably' or 'I think'.\n"
        "- Log decisions when choosing between alternatives. "
        "Future sessions depend on this memory."
    ),
)


# ═══════════════════════════════════════════════════════════════════════════════
# RETRIEVAL
# ═══════════════════════════════════════════════════════════════════════════════


@mcp.tool()
def retrieve(query: str, include_memory: bool = True, include_docs: bool = True, limit: int = 10) -> str:
    """Unified retrieval across ontology, episodic memory, and docs.

    Args:
        query: What you're looking for
        include_memory: Also search episodic memory (default True)
        include_docs: Also search local docs (default True)
        limit: Max results per source (default 10)
    """
    sections = []

    # Ontology (Neo4j)
    onto_results = ontology.query(query, limit=limit)
    sections.append(f"## Ontology\n{onto_results}")

    # Episodic memory (Milvus)
    if include_memory:
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
        doc_results = docs_backend.search_docs(query)
        if "No results" not in doc_results:
            sections.append(f"## Documentation\n{doc_results}")

    return "\n\n".join(sections)


@mcp.tool()
def get_concept(name: str) -> str:
    """Get a concept with full content and all relations from the ontology.

    Args:
        name: Exact concept name
    """
    return ontology.get_concept(name)


@mcp.tool()
def traverse(name: str, hops: int = 2) -> str:
    """Walk the knowledge graph from a concept, returning its neighborhood.

    Args:
        name: Starting concept name
        hops: How many hops (1-4, default 2)
    """
    return ontology.traverse(name, hops)


@mcp.tool()
def why_exists(name: str) -> str:
    """Explain why a concept exists in the ontology — edge reasoning.

    Args:
        name: Concept name
    """
    return ontology.why_exists(name)


# ═══════════════════════════════════════════════════════════════════════════════
# LOGGING (Episodic Memory)
# ═══════════════════════════════════════════════════════════════════════════════


@mcp.tool()
def log_tool_call(
    tool_name: str,
    parameters: str,
    result_summary: str,
    success: bool,
    context: str = "",
    session_id: str = "",
) -> str:
    """Record a tool invocation to episodic memory (L1 Experience).

    Args:
        tool_name: Which tool was called
        parameters: Parameters passed
        result_summary: Brief result summary
        success: Whether it succeeded
        context: What was the agent trying to accomplish
        session_id: Session this belongs to
    """
    return memory.log_tool_call(tool_name, parameters, result_summary, success, context, session_id)


@mcp.tool()
def log_decision(
    objective: str,
    options_considered: str,
    chosen_option: str,
    reasoning: str,
    outcome: str = "",
    session_id: str = "",
) -> str:
    """Record a decision to episodic memory (L2 Knowledge).

    Args:
        objective: What was the goal
        options_considered: Options evaluated
        chosen_option: Which was selected
        reasoning: Why
        outcome: How it turned out
        session_id: Session this belongs to
    """
    return memory.log_decision(objective, options_considered, chosen_option, reasoning, outcome, session_id)


@mcp.tool()
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


@mcp.tool()
def expand(
    concept_name: str,
    summary: str = "",
    content: str = "",
    relate_to: str = "",
    reasoning: str = "",
) -> str:
    """Add a new concept or relation to the knowledge graph.

    Creates non-linear relations between any concepts.

    Args:
        concept_name: Concept to create or connect from
        summary: One-line summary
        content: Full description
        relate_to: Target concept for a RELATES_TO edge
        reasoning: Why this relation exists
    """
    return ontology.expand(concept_name, summary, content, relate_to, reasoning)


@mcp.tool()
def link(source: str, target: str, reasoning: str) -> str:
    """Create a direct relation between two existing concepts.

    For non-linear, cross-cutting connections discovered during operation.

    Args:
        source: Source concept name
        target: Target concept name
        reasoning: Why this relation exists
    """
    return ontology.expand(source, relate_to=target, reasoning=reasoning)


# ═══════════════════════════════════════════════════════════════════════════════
# EVOLUTION (human-in-the-loop)
# ═══════════════════════════════════════════════════════════════════════════════


@mcp.tool()
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


@mcp.tool()
def execute_schema_change(cypher: str, confirmed: bool = False) -> str:
    """Execute a previously proposed schema change.

    REQUIRES confirmed=True — the human-in-the-loop gate.

    Args:
        cypher: The Cypher query to execute
        confirmed: Must be True (human has approved)
    """
    if not confirmed:
        return "Rejected: confirmed must be True. Show the proposal to the human first."

    result = ontology.run_cypher(cypher)
    return f"Schema change applied.\n\nResult:\n{result}"


# ═══════════════════════════════════════════════════════════════════════════════
# DOCUMENTATION
# ═══════════════════════════════════════════════════════════════════════════════


@mcp.tool()
def search_docs(query: str) -> str:
    """Search local documentation files for a keyword or phrase.

    Args:
        query: Search term
    """
    return docs_backend.search_docs(query)


@mcp.tool()
def list_docs() -> list[str]:
    """List all available local documentation files."""
    return docs_backend.list_docs()


@mcp.tool()
def get_doc(filename: str) -> str:
    """Read a local documentation file.

    Args:
        filename: Name of the doc file (e.g. 'setup-guide.md')
    """
    return docs_backend.read_doc(filename)


@mcp.tool()
def fetch_url(url: str) -> str:
    """Fetch a webpage and return as markdown.

    Args:
        url: Full URL to fetch
    """
    return web_to_docs_backend.convert_url(url)


@mcp.tool()
def save_doc(url: str, filename: str) -> str:
    """Fetch a webpage and save as local documentation.

    Args:
        url: Full URL to fetch
        filename: Name to save as (e.g. 'lambda-docs.md')
    """
    return web_to_docs_backend.save_as_doc(url, filename)


@mcp.tool()
def crawl_docs(url: str, max_pages: int = 20, path_prefix: str = "") -> str:
    """Crawl a documentation site and save pages as local docs.

    Args:
        url: Starting URL
        max_pages: Max pages to crawl (default 20, max 100)
        path_prefix: Only follow links under this prefix
    """
    return web_to_docs_backend.crawl_docs(url, max_pages, path_prefix)


# ═══════════════════════════════════════════════════════════════════════════════
# PROMPT ENGINEERING
# ═══════════════════════════════════════════════════════════════════════════════


@mcp.tool()
def generate_prompt(task_description: str, domain: str = "general") -> str:
    """Generate a structured prompt using the Prompt Architect framework.

    Args:
        task_description: What the prompt should accomplish
        domain: Domain context (e.g. 'cloud-infrastructure', 'web-development')
    """
    # Build Marvin's own tool catalog for inclusion in generated prompts
    tool_names = [
        "retrieve", "get_concept", "traverse", "why_exists",
        "log_tool_call", "log_decision", "log_session",
        "expand", "link", "search_docs", "list_docs", "get_doc",
        "fetch_url", "save_doc", "crawl_docs",
        "generate_diagram", "judge_diagram", "save_diagram", "list_diagrams", "get_diagram",
        "propose_schema_change", "execute_schema_change",
        "inspect_schemas", "stats",
    ]
    catalog = "\n".join(f"- `{t}`" for t in tool_names)
    return prompt_engineer_backend.generate_prompt(task_description, domain, catalog)


@mcp.tool()
def refine_prompt(original_prompt: str, feedback: str) -> str:
    """Refine an existing prompt based on feedback.

    Args:
        original_prompt: The prompt to improve
        feedback: What needs to change
    """
    return prompt_engineer_backend.refine_prompt(original_prompt, feedback)


@mcp.tool()
def audit_prompt(prompt_to_audit: str) -> str:
    """Audit a prompt against the Prompt Architect framework.

    Args:
        prompt_to_audit: The prompt text to analyze
    """
    return prompt_engineer_backend.audit_prompt(prompt_to_audit)


# ═══════════════════════════════════════════════════════════════════════════════
# SYSTEM DESIGN (Diagrams)
# ═══════════════════════════════════════════════════════════════════════════════


@mcp.tool()
def generate_diagram(system_description: str, diagram_type: str = "auto", save_as: str = "") -> str:
    """Generate a Mermaid.js system design diagram.

    Args:
        system_description: Natural language description of the system
        diagram_type: One of: c4context, c4container, c4component, flowchart, sequence, architecture, auto
        save_as: Optional filename to save (e.g. 'my-system.mmd')
    """
    return system_design_backend.generate_diagram(system_description, diagram_type, save_as)


@mcp.tool()
def judge_diagram(mermaid_code: str) -> str:
    """Review a Mermaid.js diagram for correctness and quality.

    Args:
        mermaid_code: The mermaid code to review
    """
    return system_design_backend.judge_diagram(mermaid_code)


@mcp.tool()
def save_diagram(mermaid_code: str, filename: str) -> str:
    """Save a mermaid diagram to diagrams/.

    Args:
        mermaid_code: Raw mermaid code
        filename: Filename (e.g. 'payment-flow.mmd')
    """
    return system_design_backend.save_diagram(mermaid_code, filename)


@mcp.tool()
def list_diagrams() -> list[str]:
    """List all saved mermaid diagrams."""
    return system_design_backend.list_diagrams()


@mcp.tool()
def get_diagram(filename: str) -> str:
    """Read a saved mermaid diagram.

    Args:
        filename: Diagram filename
    """
    return system_design_backend.get_diagram(filename)


# ═══════════════════════════════════════════════════════════════════════════════
# INTROSPECTION
# ═══════════════════════════════════════════════════════════════════════════════


@mcp.tool()
def inspect_schemas() -> str:
    """Show current schemas for Neo4j and Milvus."""
    neo4j_schema = ontology.get_schema()
    milvus_schema = memory.get_schema()
    return f"{neo4j_schema}\n\n---\n\n{milvus_schema}"


@mcp.tool()
def stats() -> str:
    """Quick overview of the entire knowledge system."""
    driver = ontology._get_driver()
    with driver.session() as s:
        nodes = s.run("MATCH (c:Concept) RETURN count(c) AS n").single()["n"]
        edges = s.run("MATCH ()-[r:RELATES_TO]->() RETURN count(r) AS n").single()["n"]
        ghosts = s.run("MATCH (c:Concept {ghost: true}) RETURN count(c) AS n").single()["n"]
        vaults = list(s.run(
            "MATCH (c:Concept) RETURN c.vault AS vault, count(*) AS n ORDER BY n DESC"
        ))
        agent_edges = s.run(
            "MATCH ()-[r:RELATES_TO {discovered_by: 'agent'}]->() RETURN count(r) AS n"
        ).single()["n"]

    lines = [
        "# System Stats\n",
        "## Ontology (Neo4j)",
        f"  Concepts: {nodes} ({ghosts} ghosts)",
        f"  Relations: {edges} ({agent_edges} agent-discovered)",
        f"  Vaults:",
    ]
    for r in vaults:
        lines.append(f"    {r['vault']}: {r['n']}")

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
