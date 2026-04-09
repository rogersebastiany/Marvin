# Architectural Enforcement

Behavioral constraints on the [[Agente]] must be imposed by architecture (which [[Tool|tools]] exist), not by prompts (which tools it "should" use). If the tool does not exist, the action is impossible. It is not "please don't do this" -- it is "cannot do this."

---

## Prompt vs Architecture

A prompt is a [[Bias]] -- it shifts probability, it does not eliminate it. "Do not access the internet" in the system prompt is a probabilistic constraint. The model may interpret creatively, ignore under pressure, or override when it "thinks" it is helping.

Architecture is an **absolute** constraint. If there is no web access tool in the [[MCP]] config, the probability of a web action is zero -- there are no web [[Vetor|vectors]] in the agent's [[Espaço Amostral]]. The absence of a tool is itself a reduction of S.

```
Prompt: "do not access the internet" -> bias -> P(web) ~ low, but > 0
Architecture: no web tool -> P(web) = 0
```

## Two Phases of the Ontology

The practical consequence: the agent operates in two phases with different toolsets.

**Phase 1 -- Building the [[Ontologia]]**
The agent has `web-to-docs` (crawl, save, batch). It accesses the internet to search, convert, and save knowledge. The ontology is incomplete -- web access is necessary to complete it.

**Phase 2 -- Using the [[Ontologia]]**
`web-to-docs` is removed from the config. The agent operates exclusively with [[Tool Tautológica|tautological tools]] over already-mapped knowledge. If `search_docs` returns "not found," the agent reports that it is incapable -- it does not invent, does not search the web.

The transition from Phase 1 to Phase 2 is the moment when the ontology becomes complete: every method in the domain has a corresponding tautological tool.

## The Thesis Eating Itself

The agent's action space IS the agent's [[Ontologia]]. The available tools define what the agent can do, just as the domain's ontology defines what the domain contains.

Removing a tool = removing a possibility = reducing S. Adding a tool = expanding the action space = expanding the ontology.

The [[Ontological Tautology]] applies recursively: the agent's ontology (its tools) must itself be tautological. Every available tool must be [[Tool Tautológica|tautological]]. No unnecessary tool should exist.

The ontologically tautological agent has **exactly** the tools it needs -- no more, no less.

---

Related to: [[Tool]], [[Tool Tautológica]], [[Agente]], [[MCP]], [[Ontologia]], [[Bias]], [[Espaço Amostral]], [[Ontological Tautology]]
