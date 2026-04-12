# Orchestrator

Planning engine that transforms goals into tool sequences. Given a natural language goal, the orchestrator maps it to a pre-defined chain of steps that any MCP client can follow. Zero LLM in chain selection -- it's deterministic pattern matching.

---

## Why It Exists

Multi-step workflows are fragile when the agent decides the order. "Improve this code" could mean: run tests first? Improve directly? Verify tests after? The orchestrator encodes the correct sequence -- the agent executes, not invents.

This is [[Architectural Enforcement]] applied to workflows: the chain defines the space of possible actions, not the agent.

## 6 Chains

| Chain | Triggers | Steps | What it does |
|-------|----------|-------|-------------|
| `tdd_improve` | improve, refactor, tdd | 7 | tdd → write tests → green → improve_code → apply → green → issue |
| `full_improvement` | full improve, full cycle | 9 | Full TDD + improve + verify + check knowledge gaps |
| `research` | research, docs | 3 | rank_urls → filter 60+ → research_topic |
| `prompt_lifecycle` | prompt, generate prompt | 4 | generate → audit → if <7 → refine |
| `code_to_knowledge` | enrich, knowledge gap | 4 | improve_code → find gaps → retrieve → expand |
| `sync_and_audit` | sync, vault, audit | 4 | sync_vaults → audit_code → review → self_improve |

## How It Works

1. `orchestrate(goal)` receives the goal as text
2. Searches [[Milvus]] for prior art (similar past plans)
3. Pattern matches triggers against the goal
4. Returns the chain as a structured plan: list of steps with tool name, parameters, and instructions
5. The MCP client executes step-by-step

The orchestrator **plans**, it does not **execute**. It is LLM-agnostic -- any client can follow the plan.

## Tautology in the Orchestrator

Each chain is a high-level [[Tautological Tool]]: given a goal that matches a trigger, the step sequence is deterministic. There is no ambiguity about which tool to call in which order. The possibility space is reduced from "any combination of 44 tools" to "this specific sequence of N steps."

## Prior Art via Milvus

Before selecting a chain, the orchestrator searches for similar past plans in Milvus (`refine_plan`). If an existing plan is found, it is contrasted against the new goal -- tautological refinement instead of generation from scratch.

---

Related to: [[Marvin]], [[Architectural Enforcement]], [[Tautological Tool]], [[Milvus]], [[Self-Improvement Loop]]
