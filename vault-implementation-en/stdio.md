# stdio

The POC's transport. Standard input/output -- the bidirectional pipe between the [[Agente na POC|agent]] and each MCP server. The "open gate" of [[MCP]] in its simplest form.

---

## How It Works

Each server is a Python process that:
- **Reads** JSON-RPC commands from stdin (the agent sends)
- **Writes** JSON-RPC responses to stdout (the agent receives)

[[FastMCP]] abstracts this completely. The developer does not touch stdin/stdout -- just defines tools and calls `mcp.run()`.

## Configuration

The `mcp.json` configures the MCP client to launch each server via stdio:

```json
{
  "mcpServers": {
    "docs-server": {
      "type": "stdio",
      "command": "uv",
      "args": ["run", "python", "server.py"]
    }
  }
}
```

The MCP client spawns the process, connects stdin/stdout, and uses the [[MCP]] protocol to communicate. It is the "open gate" -- no authentication, no TLS, no overhead. Straight to the pipe.

## Why stdio (and not HTTP)

For local development, stdio is ideal:
- **Zero network configuration** -- no ports, no TLS, no firewalls
- **Minimal latency** -- direct pipe between processes, no TCP overhead
- **Isolation** -- each server is a separate process, exclusive stdin/stdout
- **Simplicity** -- `uv run python server.py` and done

## The Open Gate

In the thesis, [[MCP]] is "the open gate between AI and context." In stdio, the gate is literally open -- anything on stdin is processed, anything on stdout is consumed. There is no authentication.

Security lies "in the terrain around" -- in the local case, security is the OS itself (process permissions). In the production case ([[Arquitetura de Produção]]), the gate is closed with [[Três Camadas de Segurança|three layers]] and the transport changes to SSE via [[MCP Gateway]].

## stdio vs SSE in Production

| Aspect | stdio (POC) | SSE (Production) |
|---|---|---|
| Transport | Local pipe | HTTP + Server-Sent Events |
| Authentication | None | JWT via [[MCP Gateway]] |
| Multi-tenant | N/A | [[Tenant Isolation]] |
| Encryption | N/A | TLS on ALB |
| Access | Local process | Network via ALB + WAF |

The transition from stdio to SSE is the transition from POC to production. The [[MCP]] protocol is the same -- only the transport changes.

---

Related to: [[MCP]], [[FastMCP]], [[Agente na POC]], [[Arquitetura de Produção]], [[MCP Gateway]], [[Três Camadas de Segurança]], [[docs-server]], [[web-to-docs]], [[prompt-engineer]], [[system-design]]
