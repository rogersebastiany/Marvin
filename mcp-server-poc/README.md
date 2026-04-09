# MCP Server POC — AI-Powered Development Toolkit

A proof-of-concept showcasing how Cursor IDE (enterprise) can boost developer productivity through built-in features, marketplace MCP servers, and custom MCP servers for company-specific needs.

## The Three Levels of Cursor Productivity

### Level 1: Built-in Features (Zero Code)

These are available out of the box to every developer on the team.

**`@docs` — Documentation Indexing**
Add any public documentation URL in Settings → Docs and Cursor indexes it automatically. Any developer can reference it with `@docs` in chat. Shareable with the team. Replaces the need for a custom docs server for public documentation.

**`.cursor/rules/` — Project Rules**
Markdown files in `.cursor/rules/` that instruct the AI how to behave in your project. Enforce coding standards, architecture decisions, security policies. Version-controlled, auto-attached by directory. Example: "all API endpoints must validate JWT", "use repository pattern for data access".

**`@codebase` / `@file` / `@folder` — Context References**
Point the AI at exactly the right context. `@codebase how does authentication work` searches your entire repo — no copy-pasting into ChatGPT.

**Composer — Multi-file Agent**
The agent creates/edits multiple files in one go: "add a new API endpoint with tests, migration, and docs" — scaffolds everything following your project rules.

**Cmd+K — Inline Edit**
Select code, describe the change in natural language. Ideal for refactoring: "convert to async/await", "add error handling", "make this generic".

**Tab Autocomplete**
Context-aware across the whole project — knows your types, patterns, and conventions. The daily driver that saves ~30 min/day per developer.

### Level 2: MCP Marketplace (Browse & Install)

Pre-built MCP servers from the Cursor marketplace. Every developer should browse and pick what fits their workflow:

- **Database** — query, migrate, inspect schemas from chat
- **Jira / Linear** — create tickets, update status from the IDE
- **Sentry** — pull error context into debugging sessions
- **Monitoring** — pull logs, metrics, alerts into agent context
- **Figma** — reference designs while building UI
- **GitHub** — PR reviews, issue management, CI status

### Level 3: Custom MCP Servers (This Repo)

For company-specific needs that marketplace servers don't cover — especially **private documentation behind authentication** and **domain-specific tooling**.

Cursor's `@docs` only indexes public URLs. If your company has internal wikis, private APIs, or architecture docs behind SSO, you need a custom solution. That's what this repo demonstrates.

## Custom MCP Servers

### When Do You Need Custom MCP?

| Need | Built-in Solution | Custom MCP Needed? |
|------|------------------|-------------------|
| Index public docs (AWS, React, etc.) | `@docs` — just paste the URL | No |
| Enforce coding standards | `.cursor/rules/` | No |
| Search private/internal docs behind auth | Nothing built-in | **Yes** |
| Generate system design diagrams | Nothing built-in | **Yes** |
| Structured prompt engineering framework | Rules cover basic cases | **Yes** (for advanced audit/scoring) |
| Crawl & save docs for offline use | Nothing built-in | **Yes** |

### Server Reference

#### 1. Docs Server (`server.py`)
Search and browse local markdown documentation. In production, this backs onto encrypted S3 storage for private company docs.

| Type | Name | Description |
|------|------|-------------|
| Tool | `search_docs(query)` | Keyword search across all docs with context |
| Tool | `list_docs()` | List available documentation files |
| Tool | `get_doc_summary(filename)` | First section/summary of a doc |
| Resource | `docs://{filename}` | Full contents of a doc file |
| Prompt | `explain_concept(topic)` | Search docs and explain a concept |
| Prompt | `onboarding_guide()` | Generate a getting-started guide |

#### 2. Web-to-Docs (`web_to_docs_server.py`)
Fetch websites, convert to markdown, and save locally for the docs server to search.

| Type | Name | Description |
|------|------|-------------|
| Tool | `convert_url(url)` | Fetch a page and return as markdown |
| Tool | `save_as_doc(url, filename)` | Fetch, convert, and save to `docs/` |
| Tool | `batch_convert(urls)` | Fetch multiple URLs, auto-name files |
| Tool | `crawl_docs(url, max_pages, path_prefix)` | Crawl a docs site (follow links, max 100 pages) |
| Prompt | `research_and_answer(question)` | Search local, fetch from web if needed, answer |
| Prompt | `fetch_project_docs(technology)` | Build a local docs library for a technology |

#### 3. Prompt Engineer (`prompt_engineer_server.py`)
Generate, refine, and audit prompts using the Transformer-Driven Prompt Architect framework. Auto-discovers all tools from sibling servers at startup and injects the full catalog into every generated prompt.

| Type | Name | Description |
|------|------|-------------|
| Tool | `list_mcp_tools()` | List all tools available across all MCP servers |
| Tool | `generate_prompt(task, domain)` | Generate a structured prompt (6 mandatory sections, auto-includes tool catalog) |
| Tool | `refine_prompt(original, feedback)` | Improve a prompt based on feedback |
| Tool | `audit_prompt(prompt)` | Score 1-10 and identify gaps |
| Prompt | `architect_prompt(task)` | Quick trigger to generate a production prompt |
| Prompt | `improve_my_prompt()` | Audit + refine workflow |

#### 4. System Design (`system_design_server.py`)
Generate and review system design diagrams using Mermaid.js.

| Type | Name | Description |
|------|------|-------------|
| Tool | `generate_diagram(description, type, save_as)` | Generate a mermaid diagram from a description |
| Tool | `judge_diagram(mermaid_code)` | Review and score a diagram (syntax, completeness, clarity, best practices) |
| Tool | `save_diagram(mermaid_code, filename)` | Save a `.mmd` file to `diagrams/` |
| Tool | `list_diagrams()` | List saved diagrams |
| Tool | `get_diagram(filename)` | Read a saved diagram |
| Resource | `diagrams://{filename}` | Read a diagram as a resource |
| Prompt | `design_system(description)` | End-to-end: generate diagram + explain decisions + save |
| Prompt | `review_architecture(filename)` | Load a diagram, judge it, improve if score < 7 |

### How They Chain Together

1. **Agent needs info** → searches local docs (docs-server)
2. **Not found locally** → fetches from the web and saves (web-to-docs)
3. **Now searchable** → docs-server can search the newly saved content
4. **Needs a prompt** → prompt-engineer generates an optimized prompt
5. **Needs a diagram** → system-design generates/reviews mermaid diagrams using docs as context

## Quick Start

```bash
uv sync
```

All 4 servers are auto-launched by Cursor via `.cursor/mcp.json` — no manual start needed.

For global availability across all Cursor projects, copy the config to `~/.cursor/mcp.json` (with absolute paths — see the file for the format).

## Docker

```bash
docker build -t mcp-docs-server .
docker run -i --rm mcp-docs-server
```

## Presentation Demo Script

### Act 1: Built-in Power (2 min)
1. Show `.cursor/rules/` — "every dev gets these standards automatically"
2. Show `@docs` — add a public docs URL, reference it in chat
3. Show `@codebase` — "how does authentication work in this project?"

### Act 2: Marketplace (1 min)
4. Browse MCP marketplace — show Jira, database, Sentry integrations
5. "Every dev should pick the tools that fit their workflow"

### Act 3: Custom MCP for Our Needs (5 min)
6. **"What docs are available?"** → `list_docs`
7. **"Search the docs for authentication"** → `search_docs`
8. **"Fetch the FastAPI docs"** → `crawl_docs` → saves to `docs/` → searchable
9. **"Design a payment system"** → `generate_diagram` → mermaid output
10. **"Review this architecture diagram"** → `judge_diagram` → scored feedback
11. **"Create a prompt for a code reviewer"** → `generate_prompt` → structured prompt

### Act 4: The Vision (2 min)
12. **Full chain**: "How does AWS Lambda work?" → search local → not found → crawl AWS docs → search again → answer with citations → generate architecture diagram
13. Show the cloud deployment plan — "this is how we'd run it with private docs behind Entra ID"

## Cloud Deployment (Production)

Architecture diagrams available in `diagrams/secure-mcp-platform.mmd` and `diagrams/aws-deployment.mmd`.

### AWS Services

#### ECS Fargate (Compute)
Where the code runs. Serverless containers — you provide Docker images, AWS manages the underlying infrastructure. Each MCP server runs as a separate **task** (container). You pay per vCPU/memory per second, only while running. Lambda is not viable because MCP requires persistent connections (SSE/stdio) and Lambda kills functions after 15 minutes.

#### ALB (Application Load Balancer)
The front door and only component with a public IP. Terminates TLS (HTTPS cert lives here), routes requests to the right Fargate task, supports SSE and WebSocket for MCP's persistent connections, and health-checks containers to stop sending traffic to unhealthy ones.

#### WAF (Web Application Firewall)
Sits in front of the ALB and filters traffic before it reaches your code. Handles rate limiting (e.g., max 100 req/min per IP), IP allowlisting (restrict to company IP ranges), blocks common attack patterns, and supports geographic restrictions.

#### S3 + KMS (Storage + Encryption)
**S3** stores documents and diagrams — infinite capacity, 99.999999999% durability. **KMS** (Key Management Service) encrypts every object with a unique data key via SSE-KMS. Keys can be rotated automatically, access is auditable via CloudTrail, and separate keys per tenant provide hard isolation. Revoking a key instantly makes all data under it unreadable.

#### Secrets Manager
Stores API keys, database passwords, and encryption keys. Containers fetch secrets at startup instead of using env vars or config files. Supports automatic rotation (e.g., every 30 days), full audit trail of access, and fine-grained IAM policies (container A can only read secret X).

#### CloudWatch Logs (Audit)
Where the MCP Gateway logs every tool call: who, which tool, what parameters, when, which tenant. Logs are append-only (individual entries can't be deleted), configurable retention (e.g., 1 year), queryable via Logs Insights, and exportable to S3 or a SIEM for compliance.

#### ECR (Elastic Container Registry)
Private Docker registry inside your AWS account. MCP server images are pushed here and pulled by ECS Fargate. Images never leave your account. Supports vulnerability scanning for known CVEs.

#### VPC + VPC Endpoints (Networking)
**VPC** is the private network. The ALB sits in a public subnet (internet-facing), while all Fargate tasks run in a private subnet with no public IPs and no internet access. **VPC Endpoints** let the private containers talk to S3, Secrets Manager, and CloudWatch over AWS's internal network — traffic never touches the internet.

#### Microsoft Entra ID (Authentication)
Your company's existing identity provider (not an AWS service). The MCP Gateway validates JWT tokens issued by Entra ID on every call. 2FA via Microsoft Authenticator is enforced at the Entra level — the platform just verifies the token is valid and not expired.

### Security Architecture

```
Internet → WAF → ALB (public subnet) → MCP Gateway (private subnet) → MCP Servers (private subnet) → S3/KMS (VPC endpoints)
                                              ↓
                                        Entra ID (JWT validation + 2FA)
```

Three trust zones:
- **Public**: ALB + WAF only
- **DMZ**: MCP Gateway (JWT validation, routing, audit logging)
- **Private**: MCP servers + encrypted storage (zero public access)

### Cost Estimate

| Service | Monthly Cost |
|---------|-------------|
| Fargate (5 tasks, 0.5 vCPU, 1GB each) | ~$75 |
| ALB | ~$25 + $0.008/LCU-hour |
| WAF | ~$5 + $0.60/million requests |
| S3 | ~$1-5 (depends on doc volume) |
| KMS | ~$1/key/month |
| Secrets Manager | ~$2 |
| CloudWatch Logs | ~$5-10 |
| ECR | ~$1 |
| **Total** | **~$115-125/month** |

### What Needs to Change from POC

1. **MCP Gateway** — new authenticating proxy that wraps all 4 servers behind a single SSE endpoint
2. **Storage backend** — swap local `docs/` for S3 client with KMS encryption
3. **Tenant isolation** — namespace prefixes in S3 + scoped RBAC per tenant
4. **Audit middleware** — log every tool call through the gateway
5. **Infrastructure-as-code** — Terraform or CDK for the AWS stack above
