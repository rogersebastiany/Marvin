# stdio

O transporte da POC. Standard input/output — o pipe bidirecional entre o [[Agente na POC|agente]] e cada MCP server. A "porteira aberta" do [[MCP]] na sua forma mais simples.

---

## Como Funciona

Cada server é um processo Python que:
- **Lê** comandos JSON-RPC de stdin (o agente envia)
- **Escreve** respostas JSON-RPC em stdout (o agente recebe)

O [[FastMCP]] abstrai isso completamente. O developer não toca em stdin/stdout — apenas define tools e chama `mcp.run()`.

## Configuração

O `mcp.json` configura o cliente MCP para lançar cada server via stdio:

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

O cliente MCP spawna o processo, conecta stdin/stdout, e usa o protocolo [[MCP]] para comunicar. É a "porteira aberta" — sem autenticação, sem TLS, sem overhead. Direto no pipe.

## Por que stdio (e não HTTP)

Para desenvolvimento local, stdio é ideal:
- **Zero configuração de rede** — sem portas, sem TLS, sem firewalls
- **Latência mínima** — pipe direto entre processos, sem TCP overhead
- **Isolamento** — cada server é um processo separado, stdin/stdout exclusivo
- **Simplicidade** — `uv run python server.py` e pronto

## A Porteira Aberta

Na tese, o [[MCP]] é "a porteira aberta entre a IA e o contexto." Em stdio, a porteira é literalmente aberta — qualquer coisa no stdin é processada, qualquer coisa no stdout é consumida. Não há autenticação.

A segurança fica "no terreno ao redor" — no caso local, a segurança é o próprio OS (permissões de processo). No caso de produção ([[Arquitetura de Produção]]), a porteira é fechada com [[Três Camadas de Segurança|três camadas]] e o transporte muda para SSE via [[MCP Gateway]].

## stdio vs SSE em Produção

| Aspecto | stdio (POC) | SSE (Produção) |
|---|---|---|
| Transporte | Pipe local | HTTP + Server-Sent Events |
| Autenticação | Nenhuma | JWT via [[MCP Gateway]] |
| Multi-tenant | N/A | [[Tenant Isolation]] |
| Encryption | N/A | TLS no ALB |
| Acesso | Processo local | Rede via ALB + WAF |

A transição de stdio para SSE é a transição de POC para produção. O protocolo [[MCP]] é o mesmo — muda apenas o transporte.

---

Relaciona-se com: [[MCP]], [[FastMCP]], [[Agente na POC]], [[Arquitetura de Produção]], [[MCP Gateway]], [[Três Camadas de Segurança]], [[docs-server]], [[web-to-docs]], [[prompt-engineer]], [[system-design]]
