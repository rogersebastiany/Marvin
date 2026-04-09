# MCP na Prática: Infraestrutura, Segurança e Implementação

## O que é MCP

O MCP (Model Context Protocol) é uma maneira de ter endereçamento indireto O(1) em um contexto que não necessariamente está local no seu server. O gRPC coloca as procedures diretamente no stdin/stdout — é uma porteira aberta entre a IA e o contexto externo, via stream, não async.

Sem MCP, integrar uma ferramenta externa exige criar APIs, lidar com autenticação complexa e latência. Com MCP, você expõe o contexto (logs, DB, métricas de cloud, as tools) via gRPC. Para a IA, acessar um log no servidor de Frankfurt ou uma tabela no banco local tem o mesmo "custo" cognitivo. É O(1), como se fosse memória RAM.

A porteira é aberta, mas o terreno ao redor é cercado.

---

## Segurança: Três Camadas

O MCP em si não tem camada de segurança built-in — ele é o pipe. A segurança fica na infraestrutura ao redor, organizada em três camadas:

**Transporte** — VPN, mTLS, ou rede privada. O gRPC já suporta TLS nativamente, então o canal é encriptado. Se está tudo dentro de uma VPC na AWS, o tráfego nem sai da rede interna. CloudFront provê encriptação HTTPS em trânsito com HTTP/2 e HTTP/3.

**Acesso** — Firewall, Security Groups, IAM. Quem pode conectar no MCP server, quais tools estão expostas, quais operações são permitidas. A arquitetura de rede coloca os MCP servers em subnets privadas sem acesso direto à internet. Acesso a tools e recursos é fornecido apenas através de VPC Endpoints (PrivateLink).

**Autenticação** — Amazon Cognito provê OAuth 2.0 com authorization code grant flow para comunicação segura machine-to-machine. AWS WAF protege contra exploits web comuns e inclui rate limiting para prevenir DDoS. Microsoft Entra ID (ou outro IdP corporativo) valida JWTs em cada chamada, com 2FA enforced no nível do IdP.

---

## Arquitetura AWS para Produção

```
Internet → WAF → ALB (public subnet) → MCP Gateway (private subnet) → MCP Servers (private subnet) → S3/KMS (VPC endpoints)
                                              ↓
                                        Entra ID (JWT validation + 2FA)
```

Três zonas de confiança:

- **Public**: ALB + WAF only — único componente com IP público
- **DMZ**: MCP Gateway — validação JWT, roteamento, audit logging
- **Private**: MCP servers + storage encriptado — zero acesso público

### Serviços AWS

**ECS Fargate (Compute)** — Cada MCP server roda como um container Docker separado. Serverless, escala individual sem impactar os outros. Pay per vCPU/memory por segundo. Lambda não é viável porque MCP requer conexões persistentes (SSE/stdio) e Lambda mata funções após 15 minutos.

**ALB (Application Load Balancer)** — Front door. Termina TLS, roteia requests pro Fargate task correto, suporta SSE e WebSocket para conexões persistentes do MCP, health-checks containers.

**WAF (Web Application Firewall)** — Rate limiting, IP allowlisting (restringir a ranges do escritório), bloqueia padrões de ataque comuns, restrições geográficas.

**S3 + KMS (Storage + Encryption)** — S3 armazena documentos e diagramas. KMS encripta cada objeto com chave única via SSE-KMS. Rotação automática de chaves, auditável via CloudTrail. Chaves separadas por tenant = isolamento real.

**Secrets Manager** — API keys, senhas, chaves de encriptação. Containers buscam secrets no startup em vez de env vars. Rotação automática (ex: 30 dias), audit trail completo.

**CloudWatch Logs** — Audit de toda tool call: quem, qual tool, quais parâmetros, quando, qual tenant. Logs append-only, retenção configurável, queryable via Logs Insights.

**ECR (Container Registry)** — Registry Docker privado. Imagens nunca saem da conta. Vulnerability scanning para CVEs.

**VPC + VPC Endpoints** — VPC é a rede privada. ALB em subnet pública, Fargate tasks em subnet privada sem IPs públicos. VPC Endpoints permitem que os containers privados falem com S3, Secrets Manager e CloudWatch pela rede interna da AWS — tráfego nunca toca a internet.

### Estimativa de Custo

| Serviço | Custo Mensal |
|---------|-------------|
| Fargate (5 tasks, 0.5 vCPU, 1GB cada) | ~$75 |
| ALB | ~$25 |
| WAF | ~$5 |
| S3 | ~$1-5 |
| KMS | ~$1/key |
| Secrets Manager | ~$2 |
| CloudWatch Logs | ~$5-10 |
| ECR | ~$1 |
| **Total** | **~$115-125/mês** |

---

## Implementação: A POC

A POC consiste em 4 MCP servers em Python usando FastMCP, que se complementam numa cadeia:

**docs-server** (`server.py`) — Base de conhecimento local. Busca e navega documentação markdown em `docs/`. Em produção, backend seria S3 encriptado.

**web-to-docs** (`web_to_docs_server.py`) — Alimenta a base de conhecimento crawleando a web. Converte HTML para markdown e salva localmente. Resolve o problema de docs privadas atrás de autenticação que ferramentas padrão não alcançam.

**system-design** (`system_design_server.py`) — Gera e avalia diagramas Mermaid.js. Inclui guidelines de arquitetura e scoring de qualidade (1-10) em 4 dimensões: sintaxe, completude, clareza, boas práticas.

**prompt-engineer** (`prompt_engineer_server.py`) — Orquestrador. Auto-descobre todas as tools dos servers irmãos no startup e injeta o catálogo completo em cada prompt gerado. Framework de 6 seções mandatórias (Role, MCP Knowledge, Few-Shots, CoT, Constraints, Task).

### Cadeia de Tools

1. Agente precisa de informação → busca local (docs-server)
2. Não encontrou → busca na web e salva (web-to-docs)
3. Agora é buscável → docs-server encontra o conteúdo salvo
4. Precisa de um prompt → prompt-engineer gera prompt otimizado com catálogo completo de tools
5. Precisa de um diagrama → system-design gera/avalia diagramas Mermaid com docs como contexto

### Configuração

Todos os 4 servers são lançados via `mcp.json` (stdio, via `uv run`):

```json
{
  "mcpServers": {
    "docs-server": {
      "type": "stdio",
      "command": "uv",
      "args": ["run", "python", "server.py"]
    },
    "web-to-docs": {
      "type": "stdio",
      "command": "uv",
      "args": ["run", "python", "web_to_docs_server.py"]
    },
    "prompt-engineer": {
      "type": "stdio",
      "command": "uv",
      "args": ["run", "python", "prompt_engineer_server.py"]
    },
    "system-design": {
      "type": "stdio",
      "command": "uv",
      "args": ["run", "python", "system_design_server.py"]
    }
  }
}
```

### Pontos de Atenção para Produção

**HTTPS/TLS** — O `web_to_docs_server.py` na POC usa `verify=False` no httpx para simplificar o desenvolvimento. Em produção, isso deve ser removido e o certificado TLS deve ser validado. É um red flag de segurança em auditoria.

**Event Loop** — O `prompt_engineer_server.py` usa `asyncio.run()` dentro de um import para auto-descobrir tools. Se o event loop já estiver rodando, isso pode causar conflito. Para produção, considerar lazy loading ou approach async nativo.

**Storage** — Trocar filesystem local (`docs/`, `diagrams/`) por S3 + KMS. A interface está limpa o suficiente para essa troca ser simples — substituir `Path.read_text()` e `Path.write_text()` por um client S3.

**MCP Gateway** — Novo componente: proxy autenticador que envolve os 4 servers em um único endpoint SSE, com validação JWT e audit logging.

**Tenant Isolation** — Prefixos de namespace no S3 + RBAC escopado por tenant.

**Infrastructure-as-Code** — Terraform ou CDK para o stack AWS descrito acima.

---

## Referências

- [AWS Guidance for Deploying MCP Servers](https://aws.amazon.com/solutions/guidance/deploying-model-context-protocol-servers-on-aws/)
- [AWS MCP Servers (GitHub)](https://github.com/awslabs/mcp)
- [Scaling MCP Servers for Enterprise (AWS Blog)](https://aws.amazon.com/blogs/machine-learning/accelerating-ai-innovation-scale-mcp-servers-for-enterprise-workloads-with-amazon-bedrock/)
- Repositório da POC: disponível para consulta
