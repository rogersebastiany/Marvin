# Production Architecture

The path from the local POC to AWS deployment. The same [[Server Chain]], but with authentication, encryption, multi-tenancy, and auditing. ~$115-125/month.

---

## The Architecture

```
Internet -> WAF -> ALB (public subnet) -> MCP Gateway (private subnet) -> MCP Servers (private subnet) -> S3/KMS (VPC endpoints)
                                              |
                                        Entra ID (JWT validation + 2FA)
```

Three trust zones:
- **Public:** ALB + WAF -- the only component with a public IP
- **DMZ:** [[MCP Gateway]] -- JWT validation, routing, audit logging
- **Private:** MCP servers + [[S3 as Persistent Ontology|encrypted storage]] -- zero public access

## AWS Services

**ECS Fargate (Compute):** Each server runs in a separate Docker container. Serverless -- scales individually. Lambda is not suitable because [[MCP]] requires persistent connections (SSE/[[stdio]]) and Lambda kills after 15 minutes.

**ALB (Application Load Balancer):** Front door. Terminates TLS, routes requests, supports SSE and WebSocket for persistent MCP connections, health-checks containers.

**WAF (Web Application Firewall):** Rate limiting, IP allowlisting, attack pattern blocking. Part of the [[Three Security Layers|Transport]] layer.

**S3 + KMS:** [[S3 as Persistent Ontology]] -- encrypted docs and diagrams. Separate keys per [[Tenant Isolation|tenant]].

**Secrets Manager:** API keys and encryption keys. Containers fetch at startup instead of env vars. Automatic rotation.

**CloudWatch Logs:** Audit of every tool call: who, which tool, parameters, when, which tenant. Append-only logs -- compliance-ready.

**ECR:** Private Docker registry. Images never leave the account. Vulnerability scanning.

**VPC + VPC Endpoints:** Private network. ALB in public subnet, Fargate in private subnet with no public IPs. VPC Endpoints for S3, Secrets Manager, CloudWatch -- traffic never touches the internet.

## What Changes from the POC

| POC | Production |
|---|---|
| Local `docs/` | [[S3 as Persistent Ontology]] with KMS |
| Direct [[stdio]] | SSE via [[MCP Gateway]] |
| No authentication | JWT via Entra ID + 2FA |
| Single-user | [[Tenant Isolation]] via S3 namespace |
| No auditing | CloudWatch Logs + audit middleware |
| `verify=False` | Validated TLS on ALB |
| Manual deploy | IaC (Terraform/CDK) |
| Local `.cursor/mcp.json` | Config pointing to ALB endpoint |

## Cost

| Service | Monthly |
|---|---|
| Fargate (5 tasks, 0.5 vCPU, 1GB) | ~$75 |
| ALB | ~$25 |
| WAF | ~$5 |
| S3 + KMS + Secrets + CloudWatch + ECR | ~$15-20 |
| **Total** | **~$115-125** |

## Gateway to the Thesis

The [[Production Architecture]] is what makes the [[Ontological Tautology]] thesis viable at enterprise scale. The [[Ontology as Code|ontology]] is encrypted, isolated per tenant, auditable, and accessible in O(1) via [[MCP]] over SSE. The "open gate" of [[stdio]] becomes a gate with [[Three Security Layers|three security layers]] -- but the [[MCP]] protocol is the same.

---

Related to: [[MCP Gateway]], [[Three Security Layers]], [[Tenant Isolation]], [[S3 as Persistent Ontology]], [[Server Chain]], [[stdio]], [[FastMCP]], [[Ontology as Code]]
