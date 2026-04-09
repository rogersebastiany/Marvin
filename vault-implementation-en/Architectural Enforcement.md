# Architectural Enforcement

Behavioral constraints on the [[Agent in POC|agent]] must be imposed by the architecture (which tools are in the MCP config), not by the prompt. If the tool does not exist, the action is impossible by construction.

---

## The Prompt Problem

A prompt is a [[Tool as Bias|bias]] -- it shifts probability, it does not eliminate it. "Do not access the internet" is a soft constraint. The model operates in probabilistic space -- it can ignore, reinterpret, or override the instruction.

Architecture is an absolute constraint. If `web-to-docs` is not in `mcp.json`, the [[Agent in POC|agent]] has no web access vectors in the [[Sample Space]]. The probability of a web action is zero -- not low, zero.

## Two Phases in the POC

**Phase 1 -- Ontology Construction**

```json
{
  "mcpServers": {
    "docs-server": { ... },
    "web-to-docs": { ... },
    "prompt-engineer": { ... },
    "system-design": { ... }
  }
}
```

The agent has `web-to-docs`. It can crawl, save, expand `docs/`. The [[Ontology as Code|ontology]] is incomplete -- web access is necessary to build it. It is the [[Deterministic Feedback Loop]] in action: not found -> searched the web -> saved -> now finds it.

**Phase 2 -- Ontology Usage**

```json
{
  "mcpServers": {
    "docs-server": { ... },
    "prompt-engineer": { ... },
    "system-design": { ... },
    "mcp-ontology-server": { ... },
    "mcp-memory-server": { ... }
  }
}
```

`web-to-docs` removed. [[mcp-ontology-server]] and [[mcp-memory-server]] added. The agent operates exclusively on mapped knowledge -- [[Neo4j]] for ontology, [[Milvus]] for memory, `docs/` for text. If `search_docs` returns "not found", the agent reports that it is incapable. It does not invent, it does not search the web.

The transition is the moment when the ontology becomes complete: every method in the domain has a corresponding [[Tautological Tool]].

## In Production

The [[MCP Gateway]] can enforce phases via configuration:
- Phase 1: gateway routes to `web-to-docs` + `docs-server`
- Phase 2: gateway blocks `web-to-docs`, routes to ontology + memory servers
- Audit log records any attempt to access a blocked tool

The enforcement is at the infrastructure level, not at the prompt level.

## The Ontologically Tautological Agent

The agent's action space IS the agent's ontology. The available tools define what it can do. Remove tool = reduce S. Add tool = expand S.

The [[Ontological Tautology — Thesis and Proof|thesis]] applies recursively: the agent's ontology (its tools) must itself be tautological. Every available tool must be [[Tautological Tool|tautological]]. No unnecessary tool should exist. The agent has **exactly** the tools it needs -- no more, no less.

---

Related to: [[Tautological Tool]], [[Tool as Bias]], [[Agent in POC]], [[Server Chain]], [[MCP Gateway]], [[Deterministic Feedback Loop]], [[Ontology as Code]], [[Neo4j]], [[Milvus]], [[mcp-ontology-server]], [[mcp-memory-server]], [[Ontological Tautology — Thesis and Proof]]
