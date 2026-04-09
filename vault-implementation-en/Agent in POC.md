# Agent in the POC

Any [[MCP]] client that consumes the 4 POC servers. It can be an IDE (Cursor, VS Code, JetBrains), Claude Code, or any agent with MCP support. It operates via [[ReAct in POC|ReAct]] with the [[MCP Primitives|tools]] available through [[stdio]].

---

## Configuration

The servers are configured via `mcp.json` (standard MCP format):

```json
{
  "mcpServers": {
    "docs-server": { "type": "stdio", "command": "uv", "args": ["run", "python", "server.py"] },
    "web-to-docs": { "type": "stdio", "command": "uv", "args": ["run", "python", "web_to_docs_server.py"] },
    "prompt-engineer": { "type": "stdio", "command": "uv", "args": ["run", "python", "prompt_engineer_server.py"] },
    "system-design": { "type": "stdio", "command": "uv", "args": ["run", "python", "system_design_server.py"] }
  }
}
```

The MCP client spawns the 4 processes. Each server becomes available as a source of [[MCP Primitives|tools, resources, and prompts]]. No manual startup required.

## The Agent as Personified Context

In the thesis, [[Agent]] is "[[Context]] personified with a [[ReAct]] loop." Any MCP client is exactly that:

- **Context:** system prompt + codebase + MCP tools + project rules
- **Persona:** defined by the system prompt (Senior Engineer, QA, PM, etc.)
- **ReAct loop:** reasons (plans), acts (invokes tools), observes (incorporates results)
- **[[Tool|Tools]]:** the 15+ tools from the 4 servers, accessible via [[MCP]]

The agent does not "know" the domain ontology. It "accesses" the ontology via [[docs-server]], "expands" it via [[web-to-docs]], "optimizes" delivery via [[prompt-engineer]], and "visualizes" via [[system-design]].

## The Agent Cycle in the POC

```
User asks "how does Lambda work?"
    |
Agent reasons: "I'll search the docs"
    | Act
search_docs("lambda") -> "No results found"
    | Observe
Agent reasons: "no local docs, I'll search the web"
    | Act
crawl_docs("https://docs.aws.amazon.com/lambda/...") -> "Crawled 15 pages"
    | Observe
Agent reasons: "now I have docs, I'll search again"
    | Act
search_docs("lambda") -> matches in 8 files
    | Observe
Agent reasons: "I have enough information to answer"
    |
Response based on verified docs
```

Each reason->act->observe cycle is a step in the [[Deterministic Feedback Loop]]. Each tool call is [[Space Reduction in Practice|space reduction]].

## Tool Agnosticism

The [[MCP]] protocol is standardized. Any client implementing the protocol can consume the 4 servers. The `mcp.json` config is portable across tools. The [[Ontology as Code|ontology]] served does not depend on which agent consumes it -- the same [[Server Chain]] works with any MCP client.

This reinforces the thesis: [[Measurable Determinism|determinism]] comes from the [[Programmatic Context|context]] (the served ontology), not from the agent. Swap the agent, keep the tools -- determinism is preserved.

## Architectural Enforcement

What the agent can do is defined by the list of tools in the MCP config -- not by the prompt. If `web-to-docs` is not in `mcp.json`, the agent cannot access the internet. It is not "please don't" -- it is "cannot." Constraints must be [[Architectural Enforcement|architectural]], not textual. See [[Architectural Enforcement]].

---

Related to: [[Agent]], [[ReAct in POC]], [[stdio]], [[MCP Primitives]], [[Server Chain]], [[Deterministic Feedback Loop]], [[Space Reduction in Practice]], [[Ontology as Code]], [[Measurable Determinism]], [[docs-server]], [[web-to-docs]], [[prompt-engineer]], [[system-design]], [[mcp-ontology-server]], [[mcp-memory-server]], [[Self-Improvement Loop]], [[Architectural Enforcement]]
