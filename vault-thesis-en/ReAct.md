# ReAct

Thought loop of the [[Agent]]: Reason -> Act -> Observe. Repeats until the objective is achieved.

---

## Definition

ReAct (Reasoning + Acting) is a paradigm where the model alternates between reasoning (thinking about what to do) and acting (executing a [[Tool]]). After each action, the model observes the result and incorporates it as new [[Context]].

## The Cycle

1. **Reason**: navigates the [[Sample Space]] and projects -- "to ensure this, I need the spec"
2. **Act**: calls a [[Tool]]/[[MCP]] to fetch data
3. **Observe**: receives the result as new [[Context]] and restarts the cycle

Each cycle enriches the context. It is the Deterministic Feedback Loop in action -- each iteration brings the [[Agent]] closer to [[Determinism]].

## Relationship with the Thesis

ReAct is the practical mechanism of [[Ontological Tautology]]. At each cycle, the agent accumulates more [[Context]] (reason -> observation), reduces the [[Sample Space]], and approaches the [[Tautology|tautological]] answer.

With [[RAG]] in the loop, the agent also queries past decisions -- accumulation of structured knowledge as described in the paper [[Ultra-Long-Horizon Agentic Science]].

---

Related to: [[Agent]], [[Tool]], [[MCP]], [[Context]], [[Sample Space]], [[Determinism]], [[RAG]], [[Ultra-Long-Horizon Agentic Science]]
