# Measurable Determinism

The [[Determinism]] that can be quantified. The [[DFAH]] paper demonstrates 89-90%+ trajectory determinism when [[Context]] is structured. The POC implements the conditions for this determinism.

---

## The Evidence

The [[DFAH]] (Determinism-Faithfulness Assurance Harness) by Raffi Khatchadourian empirically proves: LLM agents with **schema-first architecture** -- typed tools, parameters with explicit types, formatted returns -- achieve 89-90% trajectory determinism.

Three formal metrics:
- **ActDet**: Do the actions (tool calls) repeat across executions?
- **SigDet**: Do the signatures (tool + exact parameters) repeat?
- **DecDet**: Do the high-level decisions repeat?

89% (ActDet) means: in 100 executions with the same input and context, 89 produce the same sequence of actions. The remaining 11% are manageable -- detectable by tests, code review, observability.

**On r = -0.11**: the DFAH reveals null correlation between determinism and accuracy in agents with generic tools. But the POC operates with [[Tautological Tool|tautological tools]] -- `search_docs` finds or returns "not found", `get_doc` returns content or error. When tools are tautological, determinism **implies** accuracy. The r = -0.11 does not apply to the POC case.

## How the POC Achieves Determinism

The POC implements exactly the **schema-first architecture** that the DFAH identifies as producing the 89%+:

**Schema-first tools:** Each [[MCP Primitives|tool]] has a precise description, typed parameters via Python type hints, formatted returns. `@mcp.tool()` from [[FastMCP]] with type hints is literally the schema-first pattern. The [[Agent in POC|agent]] does not operate in a vacuum -- it operates with [[Ontology as Code|ontology]] served via typed contracts.

**Defined tools:** The 15+ tools from the 4 servers form a complete [[Tool Catalog]]. The agent knows what it can and cannot do. Each tool description is a [[Tool as Bias|bias vector]] that constrains the [[Sample Space]].

**Implicit specs:** Each tool's docstrings are behavior specs. `"Search across all documentation files for a keyword or phrase. Returns matching lines with surrounding context and filenames."` is a spec. It is the schema-first contract.

**Structured framework:** The [[Transformer-Driven Prompt Architect]] with 6 mandatory sections ensures that every generated prompt is structured, not ad-hoc.

**Evaluation metric:** For regulated domains, the correct metric is **pass^k** (all attempts must succeed), not pass@k (at least one). The distance between pass@k and pass^k reveals the system's true variance.

## The "+" in 89%+

The [[Ultra-Long-Horizon Agentic Science]] paper shows that determinism grows with [[Cognitive Accumulation]] -- not linear context aggregation, but progressive distillation in three layers (L1 experience -> L2 knowledge -> L3 wisdom). 56.44% medal rate on MLE-Bench, SOTA.

In the POC, the [[Deterministic Feedback Loop]] implements this accumulation: each `crawl_docs` expands `docs/`, each `save_diagram` expands `diagrams/`. The corpus grows, determinism grows.

The [[Implicit RAG]] closes the cycle: knowledge persisted between sessions -> richer context in the next session -> greater determinism.

## Complement: The [[LLM Output Drift]] Paper

The same author demonstrates the inverse: without rigid context, AI varies responses even at temperature zero. Larger models (100B+, Tier 3) drift more -- only 12.5% consistency. [[Implicit RAG|RAG]] tasks are the most sensitive to drift. The search in `docs/` is exactly a RAG task -- which makes structured context even more critical.

The POC attacks drift at the root -- not by adjusting the model, but by enriching context via schema-first tools.

## Complement: [[Deterministic Trajectory Optimization]]

The same pattern in another domain: starts probabilistic, enriches with structured information, converges to deterministic. In the POC: the agent starts without docs, enriches via crawl, converges to deterministic responses.

---

Related to: [[Determinism]], [[DFAH]], [[LLM Output Drift]], [[Ultra-Long-Horizon Agentic Science]], [[Deterministic Trajectory Optimization]], [[Deterministic Feedback Loop]], [[Tool Catalog]], [[Transformer-Driven Prompt Architect]], [[Implicit RAG]], [[Drift]], [[Cognitive Accumulation]], [[FastMCP]], [[Tool as Bias]], [[Tautological Tool]]
