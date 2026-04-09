# mcp-memory-server

MCP server that exposes the [[Milvus]] vector database as tools for the [[Agente na POC|agent]]. It allows searching for similar memories and logging new actions.

---

## Tools

| Tool | Description |
|---|---|
| `search_tool_calls` | Searches past tool calls similar to a query |
| `search_decisions` | Searches past decisions similar to a query |
| `search_sessions` | Searches past sessions similar to a query |
| `log_tool_call` | Records a tool call (tool, params, result, context) |
| `log_decision` | Records a decision (objective, options, choice, reasoning) |
| `log_session` | Records a session summary (objective, approach, result, lessons) |

## Search Before Acting

The usage pattern: before making a decision, the agent searches [[Milvus]] for similar actions. "Have I done something like this before? Did it work? What did I learn?"

```
Agent receives objective -> search_decisions("migrate service to ECS")
    | finds similar past decision
    | "last time, using Fargate was better than EC2 because..."
Agent decides informed -> executes -> log_decision(result)
```

This is **prefetching** in HCC vocabulary ([[Acumulação Cognitiva]]): retrieving similar wisdom before starting.

## Automatic Logging

Every significant action is logged automatically:
- Tool calls: captured at execution time
- Decisions: captured when the agent chooses between alternatives
- Sessions: captured at the end of each session

The log is append-only -- memory is never erased. The agent accumulates experience monotonically.

## Difference from Implicit RAG

The [[RAG Implícito]] in the POC searches text in `docs/`. The mcp-memory-server searches **semantic experience** by vector similarity. The difference:

- `search_docs("lambda")` -> documentation about Lambda
- `search_tool_calls("deploy lambda function")` -> the last 5 times the agent deployed Lambda, with context and result

One is domain knowledge. The other is action memory.

---

Related to: [[Milvus]], [[Embedding]], [[RAG Implícito]], [[Loop de Auto-Melhoria]], [[Acumulação Cognitiva]], [[Cadeia de Servers]], [[MCP]], [[FastMCP]]
