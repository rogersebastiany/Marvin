# mcp-memory-server

MCP server that exposes the [[Milvus]] vector database as tools for the [[Agent in POC|agent]]. It allows searching for similar memories and logging new actions.

---

## Tools

| Tool | Description |
|---|---|
In unified [[Marvin]], episodic memory is accessed via:
- `retrieve()` — unified search that internally queries `search_tool_calls`, `search_decisions`, `search_sessions` in [[Milvus]]
- `log_decision` — records a decision (objective, options, choice, reasoning)
- `log_session` — records a session summary (objective, approach, result, lessons)

The search functions (`search_*`) are internal to `memory.py` — the agent never calls them directly, only through `retrieve()`.

## Search Before Acting

The usage pattern: before making a decision, the agent calls `retrieve()` which searches [[Milvus]] for similar actions. "Have I done something like this before? Did it work? What did I learn?"

```
Agent receives objective -> retrieve("migrate service to ECS")
    | finds similar past decision (via Milvus)
    | "last time, using Fargate was better than EC2 because..."
Agent decides informed -> executes -> log_decision(result)
```

This is **prefetching** in HCC vocabulary ([[Cognitive Accumulation]]): retrieving similar wisdom before starting.

## Automatic Logging

Every significant action is logged automatically:
- Tool calls: captured at execution time
- Decisions: captured when the agent chooses between alternatives
- Sessions: captured at the end of each session

The log is append-only -- memory is never erased. The agent accumulates experience monotonically.

## Difference from Implicit RAG

The [[Implicit RAG]] in the POC searches text in `docs/`. The mcp-memory-server searches **semantic experience** by vector similarity. The difference:

- `search_docs("lambda")` -> documentation about Lambda
- `search_tool_calls("deploy lambda function")` -> the last 5 times the agent deployed Lambda, with context and result

One is domain knowledge. The other is action memory.

---

Related to: [[Milvus]], [[Embedding]], [[Implicit RAG]], [[Self-Improvement Loop]], [[Cognitive Accumulation]], [[Server Chain]], [[MCP]], [[FastMCP]]
