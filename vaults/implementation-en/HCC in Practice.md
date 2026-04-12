# HCC in Practice

How Hierarchical Cognitive Caching is implemented in [[Marvin]]. The most important decision: L1 (Experience) is NOT persisted. It lives only in the context window and is discarded after distillation.

---

## Why L1 Is Not Persisted

The [[Ultra-Long-Horizon Agentic Science]] paper shows all 3 layers are necessary (ablation: without L1 → 22.7%, without L3 → 54.5%). But L1 is transient by design -- tool traces, patches, terminal output. Persisting L1 causes context saturation: 200k+ tokens, the model loses coherence.

HCC keeps ~70k effective tokens by discarding L1 after distillation to L2. The agent doesn't need to remember every `git diff` -- it needs to remember "commit X fixed bug Y for reason Z" (L2).

## Three Layers

| Layer | What it stores | Persistence | Tool |
|-------|---------------|-------------|------|
| **L1 Experience** | Tool traces, patches, terminal output | Context window only | None -- lives in context |
| **L2 Knowledge** | Decisions, judgments, insights | Milvus `decisions` collection | `log_decision` |
| **L3 Wisdom** | Session summaries, strategies | Milvus `sessions` collection | `log_session` |

## Context Migration

Three operations move information between layers:

1. **Context Prefetch** (L2/L3 → context): `retrieve` or `get_memory` fetches similar decisions and sessions before acting. Injects L2/L3 as context for the current action.

2. **Context Hit** (context → L1): the agent acts, observes the result. The result becomes L1 in the context window.

3. **Context Promotion** (L1 → L2, L2 → L3): the agent distills L1 into a decision (`log_decision`) or synthesizes L2 into a session summary (`log_session`).

```
Prefetch: Milvus L2/L3 → context window
Hit:      tool result → context window (L1)
Promote:  L1 → log_decision → Milvus L2
          L2 → log_session → Milvus L3
```

## `log_decision` — Fire and Forget

`log_decision` is async fire-and-forget (daemon thread). The agent logs and continues without waiting for confirmation. This is critical to not interrupt the workflow. If Milvus is offline, the log is silently discarded -- preferable to blocking the agent.

## `log_session` — Synthesis

`log_session` is called at the end of a session. The agent synthesizes: objective, approach, result, lessons learned, tools used, decisions made. This is L3 -- transferable wisdom for future sessions.

## Validation

The design maps directly to the paper's HCC:
- Tool calls → L1 (Evolving Experience)
- Decisions → L2 (Refined Knowledge)
- Sessions → L3 (Prior Wisdom)

The difference: our L1 is not persisted in Milvus. The paper persists L1 with an eviction mechanism. We simplified: L1 is the context window, period. Distill to L2 or lose it.

---

Related to: [[Cognitive Accumulation]], [[Milvus]], [[Marvin]], [[Self-Improvement Loop]], [[Measurable Determinism]]
