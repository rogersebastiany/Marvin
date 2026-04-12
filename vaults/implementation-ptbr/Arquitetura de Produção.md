# Arquitetura de Produção

O caminho da POC local para deployment AWS. A mesma [[Cadeia de Servers]], mas com autenticação, encryption, multi-tenancy, e auditoria. ~$115-125/mês.

---

## A Arquitetura

```
Internet → WAF → ALB (public subnet) → MCP Gateway (private subnet) → MCP Servers (private subnet) → S3/KMS (VPC endpoints)
                                              ↓
                                        Entra ID (JWT validation + 2FA)
```

Três zonas de confiança:
- **Public:** ALB + WAF — único componente com IP público
- **DMZ:** [[MCP Gateway]] — validação JWT, roteamento, audit logging
- **Private:** MCP servers + [[S3 como Ontologia Persistente|storage encriptado]] — zero acesso público

## Serviços AWS

**ECS Fargate (Compute):** Cada server roda num container Docker separado. Serverless — escala individual. Lambda não serve porque [[MCP]] requer conexões persistentes (SSE/[[stdio]]) e Lambda mata após 15 minutos.

**ALB (Application Load Balancer):** Front door. Termina TLS, roteia requests, suporta SSE e WebSocket para conexões persistentes do MCP, health-checks containers.

**WAF (Web Application Firewall):** Rate limiting, IP allowlisting, bloqueio de padrões de ataque. Parte da camada de [[Três Camadas de Segurança|Transporte]].

**S3 + KMS:** [[S3 como Ontologia Persistente]] — docs e diagramas encriptados. Chaves separadas por [[Tenant Isolation|tenant]].

**Secrets Manager:** API keys e chaves de encryption. Containers buscam no startup em vez de env vars. Rotação automática.

**CloudWatch Logs:** Audit de toda tool call: quem, qual tool, parâmetros, quando, qual tenant. Logs append-only — compliance-ready.

**ECR:** Registry Docker privado. Imagens nunca saem da conta. Vulnerability scanning.

**VPC + VPC Endpoints:** Rede privada. ALB em subnet pública, Fargate em subnet privada sem IPs públicos. VPC Endpoints para S3, Secrets Manager, CloudWatch — tráfego nunca toca a internet.

## O que Muda da POC

| POC | Produção |
|---|---|
| `docs/` local | [[S3 como Ontologia Persistente]] com KMS |
| [[stdio]] direto | SSE via [[MCP Gateway]] |
| Sem autenticação | JWT via Entra ID + 2FA |
| Single-user | [[Tenant Isolation]] via namespace S3 |
| Sem auditoria | CloudWatch Logs + audit middleware |
| `verify=False` | TLS validado no ALB |
| Manual deploy | IaC (Terraform/CDK) |
| `.cursor/mcp.json` local | Config apontando para ALB endpoint |

## Custo

| Serviço | Mensal |
|---|---|
| Fargate (5 tasks, 0.5 vCPU, 1GB) | ~$75 |
| ALB | ~$25 |
| WAF | ~$5 |
| S3 + KMS + Secrets + CloudWatch + ECR | ~$15-20 |
| **Total** | **~$115-125** |

## Porta de Entrada para a Tese

A [[Arquitetura de Produção]] é o que torna a tese [[Tautologia Ontológica]] viável em escala empresarial. A [[Ontologia como Código|ontologia]] fica encriptada, isolada por tenant, auditável, e acessível em O(1) via [[MCP]] sobre SSE. A "porteira aberta" do [[stdio]] se torna uma porteira com [[Três Camadas de Segurança|três camadas de segurança]] — mas o protocolo [[MCP]] é o mesmo.

---

Relaciona-se com: [[MCP Gateway]], [[Três Camadas de Segurança]], [[Tenant Isolation]], [[S3 como Ontologia Persistente]], [[Cadeia de Servers]], [[stdio]], [[FastMCP]], [[Ontologia como Código]]
