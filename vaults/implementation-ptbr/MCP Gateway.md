# MCP Gateway

O componente que falta na POC: proxy autenticador que envolve os 4 servers num único endpoint SSE, com validação JWT, roteamento, e audit logging. A peça central da [[Arquitetura de Produção]].

---

## O que É

Na POC, cada server é um processo [[stdio]] independente, lançado diretamente pelo [[Agente na POC|cliente MCP]]. Sem autenticação, sem encryption, sem auditoria.

O MCP Gateway é um novo componente que:
1. **Recebe** conexões SSE (HTTP) do agente via ALB
2. **Valida** JWT emitido pelo Microsoft Entra ID
3. **Roteia** requests para o server correto (docs-server, web-to-docs, etc.)
4. **Loga** toda tool call: quem, qual tool, parâmetros, quando, qual tenant
5. **Isola** tenants via prefixos de namespace no [[S3 como Ontologia Persistente|S3]]

## De stdio para SSE

```
POC:       Agente → stdio → server.py
Produção:  Agente → HTTPS → ALB → SSE → MCP Gateway → server.py
```

O transporte muda de [[stdio]] para SSE, mas o protocolo [[MCP]] é o mesmo. Os servers não precisam ser reescritos — o Gateway faz a tradução.

## JWT e Entra ID

Microsoft Entra ID (antigo Azure AD) é o IdP corporativo. O Gateway valida em cada request:
- Token é válido e não expirou
- Issuer é o Entra ID da empresa
- Claims contêm tenant_id e scopes autorizados
- 2FA foi enforced (verificado no nível do Entra)

## Audit Logging

Cada tool call é logada no CloudWatch:

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

Logs append-only — compliance para domínios regulados (finanças, saúde, direito). É a observabilidade que faz parte da equação da tese: Spec + BDD + TDD + ADR + **Observabilidade** + [[MCP]] + [[RAG]].

## Papel na Tese

O Gateway é a [[Três Camadas de Segurança|terceira camada de segurança]] — Autenticação. Transforma a "porteira aberta" do [[MCP]] numa porteira controlada. A [[Ontologia como Código|ontologia]] continua acessível em O(1), mas apenas para usuários autenticados e autorizados.

É o componente que permite a tese funcionar em ambiente corporativo real, onde a ontologia contém informação privada, sensível, e regulada.

---

Relaciona-se com: [[Arquitetura de Produção]], [[Três Camadas de Segurança]], [[Tenant Isolation]], [[stdio]], [[MCP]], [[Cadeia de Servers]], [[Ontologia como Código]], [[S3 como Ontologia Persistente]]
