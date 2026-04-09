# Três Camadas de Segurança

A segurança do [[MCP]] em produção, organizada em três camadas ao redor da "porteira aberta." O [[MCP]] em si é pipe puro — a segurança fica na infraestrutura ao redor.

---

## As Camadas

**1. Transporte**
O canal por onde trafegam os dados. Na POC, é [[stdio]] local (seguro por design — pipe entre processos do mesmo OS). Em [[Arquitetura de Produção|produção]]:
- VPN ou rede privada (VPC)
- mTLS entre componentes
- TLS terminado no ALB
- VPC Endpoints para S3/Secrets Manager/CloudWatch — tráfego nunca sai da rede AWS

A porteira está trancada no transporte: só chega quem está na rede autorizada.

**2. Acesso**
Quem pode conectar e o que pode fazer. Em produção:
- WAF com rate limiting (ex: 100 req/min por IP)
- IP allowlisting (ranges do escritório)
- Security Groups no VPC
- IAM policies por container (container A só acessa secret X)
- Bloqueio de padrões de ataque comuns

A porteira tem um guarda: mesmo dentro da rede, só faz o que é permitido.

**3. Autenticação**
Quem é você e como provar. Em produção:
- Microsoft Entra ID como IdP corporativo
- JWT validado em cada request pelo [[MCP Gateway]]
- 2FA via Microsoft Authenticator enforced no Entra
- Amazon Cognito para OAuth 2.0 machine-to-machine

A porteira pede identidade: mesmo autorizado, precisa provar quem é.

## Na POC

A POC não tem nenhuma das 3 camadas — é design intencional. O objetivo é demonstrar a [[Cadeia de Servers]] e o [[Feedback Loop Determinístico]], não a segurança. O `verify=False` no [[web-to-docs]] é sintomático: em POC, simplificar é mais valioso que securizar.

## Na Tese

"A porteira é aberta, mas o terreno ao redor é cercado."

O [[MCP]] é O(1) por design — acesso instantâneo ao [[Contexto]]. As 3 camadas garantem que esse acesso instantâneo só acontece para quem deve. A [[Ontologia como Código|ontologia]] fica protegida sem sacrificar performance.

Em domínios regulados (finanças, saúde, direito), essas 3 camadas não são opcionais — são requisito de compliance. O [[Determinismo Mensurável|determinismo]] da tese só é útil se o sistema é auditável e seguro.

---

Relaciona-se com: [[MCP]], [[MCP Gateway]], [[Arquitetura de Produção]], [[stdio]], [[web-to-docs]], [[Ontologia como Código]], [[Tenant Isolation]], [[S3 como Ontologia Persistente]]
