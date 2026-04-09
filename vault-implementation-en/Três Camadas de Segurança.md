# Three Security Layers

The security of [[MCP]] in production, organized in three layers around the "open gate." [[MCP]] itself is a pure pipe -- security lies in the surrounding infrastructure.

---

## The Layers

**1. Transport**
The channel through which data travels. In the POC, it is local [[stdio]] (secure by design -- pipe between processes on the same OS). In [[Arquitetura de Produção|production]]:
- VPN or private network (VPC)
- mTLS between components
- TLS terminated at the ALB
- VPC Endpoints for S3/Secrets Manager/CloudWatch -- traffic never leaves the AWS network

The gate is locked at the transport level: only those on the authorized network can reach it.

**2. Access**
Who can connect and what they can do. In production:
- WAF with rate limiting (e.g., 100 req/min per IP)
- IP allowlisting (office ranges)
- Security Groups in VPC
- IAM policies per container (container A can only access secret X)
- Blocking of common attack patterns

The gate has a guard: even within the network, you can only do what is permitted.

**3. Authentication**
Who are you and how to prove it. In production:
- Microsoft Entra ID as corporate IdP
- JWT validated on each request by the [[MCP Gateway]]
- 2FA via Microsoft Authenticator enforced at Entra
- Amazon Cognito for OAuth 2.0 machine-to-machine

The gate asks for identity: even if authorized, you must prove who you are.

## In the POC

The POC has none of the 3 layers -- this is intentional by design. The goal is to demonstrate the [[Cadeia de Servers]] and the [[Feedback Loop Determinístico]], not security. The `verify=False` in [[web-to-docs]] is symptomatic: in a POC, simplifying is more valuable than securing.

## In the Thesis

"The gate is open, but the terrain around it is fenced."

[[MCP]] is O(1) by design -- instant access to [[Contexto]]. The 3 layers ensure that this instant access only happens for those who should have it. The [[Ontologia como Código|ontology]] is protected without sacrificing performance.

In regulated domains (finance, healthcare, law), these 3 layers are not optional -- they are compliance requirements. The thesis's [[Determinismo Mensurável|determinism]] is only useful if the system is auditable and secure.

---

Related to: [[MCP]], [[MCP Gateway]], [[Arquitetura de Produção]], [[stdio]], [[web-to-docs]], [[Ontologia como Código]], [[Tenant Isolation]], [[S3 como Ontologia Persistente]]
