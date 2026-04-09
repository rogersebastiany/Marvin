# MCP Gateway

The component missing from the POC: an authenticating proxy that wraps the 4 servers into a single SSE endpoint, with JWT validation, routing, and audit logging. The centerpiece of the [[Arquitetura de Produção]].

---

## What It Is

In the POC, each server is an independent [[stdio]] process, launched directly by the [[Agente na POC|MCP client]]. No authentication, no encryption, no auditing.

The MCP Gateway is a new component that:
1. **Receives** SSE (HTTP) connections from the agent via ALB
2. **Validates** JWT issued by Microsoft Entra ID
3. **Routes** requests to the correct server (docs-server, web-to-docs, etc.)
4. **Logs** every tool call: who, which tool, parameters, when, which tenant
5. **Isolates** tenants via namespace prefixes in [[S3 como Ontologia Persistente|S3]]

## From stdio to SSE

```
POC:        Agent -> stdio -> server.py
Production: Agent -> HTTPS -> ALB -> SSE -> MCP Gateway -> server.py
```

The transport changes from [[stdio]] to SSE, but the [[MCP]] protocol is the same. The servers do not need to be rewritten -- the Gateway handles the translation.

## JWT and Entra ID

Microsoft Entra ID (formerly Azure AD) is the corporate IdP. The Gateway validates on each request:
- Token is valid and not expired
- Issuer is the company's Entra ID
- Claims contain tenant_id and authorized scopes
- 2FA was enforced (verified at the Entra level)

## Audit Logging

Every tool call is logged to CloudWatch:

```json
{
  "timestamp": "2025-03-15T14:23:01Z",
  "tenant": "acme-corp",
  "user": "dev@acme.com",
  "server": "docs-server",
  "tool": "search_docs",
  "params": {"query": "authentication"},
  "response_size": 2048,
  "latency_ms": 45
}
```

Append-only logs -- compliance for regulated domains (finance, healthcare, law). It is the observability that is part of the thesis equation: Spec + BDD + TDD + ADR + **Observability** + [[MCP]] + [[RAG]].

## Role in the Thesis

The Gateway is the [[Três Camadas de Segurança|third security layer]] -- Authentication. It transforms the "open gate" of [[MCP]] into a controlled gate. The [[Ontologia como Código|ontology]] remains accessible in O(1), but only for authenticated and authorized users.

It is the component that allows the thesis to work in a real corporate environment, where the ontology contains private, sensitive, and regulated information.

---

Related to: [[Arquitetura de Produção]], [[Três Camadas de Segurança]], [[Tenant Isolation]], [[stdio]], [[MCP]], [[Cadeia de Servers]], [[Ontologia como Código]], [[S3 como Ontologia Persistente]]
