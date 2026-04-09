# Agent

[[Context]] personified with a [[ReAct]] thought loop. Receives a role and operates with [[Tool|tools]] available via [[MCP]].

---

## Definition

"The agent is the same thing, context, but it has a humanized character. It personifies an entity. You assign it the role of Senior Software Engineer, QA, PM, etc. Everything depends on how much you can enrich this agent's context."

An agent is an LLM + system prompt (role) + tools + execution loop. It is not a different program -- it is the same model operating with specialized [[Context]] and action capability.

## ReAct Loop

The agent operates in a [[ReAct]] cycle:
1. **Reason**: analyzes the task, projects the plan
2. **Act**: invokes a [[Tool]] via [[MCP]]
3. **Observe**: incorporates the result as new context
4. Repeats until the objective is achieved

## Domain AGI

With a complete [[Ontology]] of a domain (all [[Tool|tools]] mapping all knowledge), an agent achieves near-total [[Determinism]] in that domain. It is closed-domain AGI -- not universal AGI, but functional, deterministic, and replicable.

"YOU DO NOT THINK. I AM THE ONE WHO THINKS. JUST EXECUTE WHAT IS MAPPED VIA TOOL." -- This instruction transforms the agent from a probabilistic inferrer into a deterministic executor.

## Multi-Agents

Multiple agents, each with its own role and [[Tool|tools]], collaborating. The system distributes responsibilities and each agent operates within its [[Ontology]] zone.

---

Related to: [[ReAct]], [[MCP]], [[Tool]], [[Context]], [[Ontology]], [[Determinism]]
