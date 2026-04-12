# Tenant Isolation

Isolamento de dados entre clientes/equipes na [[Arquitetura de Produção]]. Cada tenant opera com sua própria [[Ontologia como Código|ontologia]] — documentos, diagramas, e histórico isolados.

---

## Mecanismo

**Namespace prefixes no S3:**
```
s3://mcp-docs-bucket/
  ├── tenant-a/docs/architecture.md
  ├── tenant-a/diagrams/payment-flow.mmd
  ├── tenant-b/docs/architecture.md     ← diferente do tenant-a
  └── tenant-b/diagrams/infra.mmd
```

O [[MCP Gateway]] injeta o `tenant_id` (extraído do JWT) em todo acesso ao [[S3 como Ontologia Persistente|S3]]. O [[docs-server]] não "sabe" que é multi-tenant — o Gateway garante que `DOCS_DIR` aponta para o prefixo correto.

**KMS keys por tenant:**
Cada tenant tem sua própria chave de encryption no KMS. Revogar a chave de um tenant torna todos os seus dados instantaneamente ilegíveis — sem precisar deletar objetos. Hard isolation.

**RBAC escopado:**
IAM policies que garantem que o container do tenant A só acessa objetos com prefixo `tenant-a/`. Mesmo que o código tente acessar `tenant-b/`, o IAM bloqueia.

## Ontologia por Tenant

Na tese, "a ontologia universal não existe — ninguém mapeou tudo que existe em todos os domínios. Mas a ontologia por domínio é construível."

O Tenant Isolation materializa isso: cada tenant constrói sua própria [[Ontologia como Código|ontologia]]. O time de finanças tem docs sobre compliance e regulação. O time de infra tem docs sobre AWS e Terraform. Cada um opera no seu [[Subconjunto]] do [[Espaço Amostral]] — sem interferência.

## Na POC

A POC é single-tenant por design — `DOCS_DIR = Path(__file__).parent / "docs"` aponta para um diretório fixo. A mudança para multi-tenant é trocar `Path` por S3 client com prefixo dinâmico. A interface das [[Primitivas MCP|tools]] não muda — `search_docs(query)` continua igual, mas busca no prefixo do tenant.

## [[Path Traversal Protection]] como Preview

O `_safe_path()` da POC já implementa uma forma primitiva de isolamento: garante que o acesso fica dentro de `docs/` ou `diagrams/`. Em produção, o Tenant Isolation escala esse conceito: garante que o acesso fica dentro do namespace do tenant.

---

Relaciona-se com: [[Arquitetura de Produção]], [[MCP Gateway]], [[S3 como Ontologia Persistente]], [[Ontologia como Código]], [[Três Camadas de Segurança]], [[Path Traversal Protection]], [[docs-server]]
