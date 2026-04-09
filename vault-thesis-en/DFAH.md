# DFAH

Determinism-Faithfulness Assurance Harness. Paper by Raffi Khatchadourian (City University of New York) that measures [[Determinismo]] and faithfulness of tool-using LLM agents, revealing that determinism and accuracy are independent dimensions.

---

## Reference

**Replayable Financial Agents: A Determinism-Faithfulness Assurance Harness for Tool-Using LLM Agents**
Raffi Khatchadourian -- City University of New York
https://arxiv.org/abs/2601.15322

## Contribution

The paper introduces a "replayable" harness -- it records agent trajectories (sequences of tool calls) and re-executes them to measure divergence. With structured [[Contexto]] (typed schemas, specs, defined tools), trajectory determinism rises to 89-90%+.

It is the central empirical proof of the [[Ontological Tautology]] thesis: [[Ontologia]] (structured context) -> [[Tautologia]] (predictable result) -> [[Determinismo]] (89%+).

## Three Formal Metrics

The paper defines three levels of determinism, each measuring a different granularity:

- **ActDet** (Action Determinism): Are the actions (tool calls) the same across executions?
- **SigDet** (Signature Determinism): Are the signatures (which tool + which parameters) the same?
- **DecDet** (Decision Determinism): Are the high-level decisions the same?

SigDet is the strictest -- it requires identical parameters. DecDet is the most relaxed -- it allows implementation variation as long as the strategy is the same. The 89%+ refers to ActDet under schema-first conditions.

## pass^k vs pass@k

Two evaluation metrics with opposite implications:

- **pass@k** (optimistic): at least 1 of k attempts succeeds. Useful for exploration.
- **pass^k** (conservative): all k attempts succeed. Required for reproducibility.

The gap between pass@k and pass^k reveals the true variance. A system with pass@5 = 95% but pass^5 = 40% looks good but is unstable. For regulated domains (finance, healthcare, law), pass^k is the metric that matters.

## The Provocative Finding: Determinism is not Accuracy

The correlation between determinism and accuracy is **null (r = -0.11)**. Small models (7-20B parameters) achieve 100% determinism at T=0.0, but low accuracy. Frontier models show moderate determinism with variable accuracy.

**However**: this null correlation applies to agents with generic tools -- tools whose output is ambiguous or open-ended. When tools are [[Tool Tautológica|tautological]] (complete I/O contract, finite output, explicit failure), determinism **implies** accuracy. If the tool can only return the correct answer or "I don't know," a deterministic system is deterministically correct.

The [[Ontological Tautology]] thesis operates in this restricted universe: tautological tools served via [[MCP]]. The r = -0.11 measures the general case; the thesis operates in the specific case where the correlation is positive by construction.

## Schema-First Architecture

What produces the 89%+ is specifically **schema-first architecture**: typed tool definitions, parameters with explicit types, formatted returns. It is not generic "context." It is structured [[Contexto]] with contracts.

In practice: `@mcp.tool()` with type hints from [[FastMCP]] is literally this pattern. Each POC tool with typed parameters and precise docstrings implements schema-first.

## Failure Modes

Stress tests reveal that determinism **degrades** under:
- Tool failures (timeout, API errors)
- Ambiguous schemas (vague descriptions, untyped parameters)
- Overloaded context (too many tools, contradictory information)

The 89% is not unconditional -- it requires maintaining schema and [[Contexto]] quality.

## Implication

89-90% determinism means that 11% indeterminism is manageable. In a software engineering context, this is acceptable -- errors can be detected by tests, code review, and observability.

The paper [[Ultra-Long-Horizon Agentic Science]] shows that the number can grow with [[Acumulação Cognitiva]] -- sustaining the "+".

---

Related to: [[Determinismo]], [[Ontologia]], [[Tautologia]], [[LLM Output Drift]], [[Ultra-Long-Horizon Agentic Science]], [[Contexto]], [[Ontological Tautology]], [[Acumulação Cognitiva]], [[FastMCP]], [[Tool Tautológica]]
