# Tenant Isolation

Data isolation between clients/teams in the [[Production Architecture]]. Each tenant operates with its own [[Ontology as Code|ontology]] -- documents, diagrams, and history isolated.

---

## Mechanism

**Namespace prefixes in S3:**
```
s3://mcp-docs-bucket/
  |- tenant-a/docs/architecture.md
  |- tenant-a/diagrams/payment-flow.mmd
  |- tenant-b/docs/architecture.md     <- different from tenant-a
  +- tenant-b/diagrams/infra.mmd
```

The [[MCP Gateway]] injects the `tenant_id` (extracted from the JWT) into every access to [[S3 as Persistent Ontology|S3]]. The [[docs-server]] does not "know" it is multi-tenant -- the Gateway ensures that `DOCS_DIR` points to the correct prefix.

**KMS keys per tenant:**
Each tenant has its own encryption key in KMS. Revoking a tenant's key makes all their data instantly unreadable -- without needing to delete objects. Hard isolation.

**Scoped RBAC:**
IAM policies that ensure tenant A's container can only access objects with the `tenant-a/` prefix. Even if the code tries to access `tenant-b/`, IAM blocks it.

## Ontology per Tenant

In the thesis, "the universal ontology does not exist -- nobody has mapped everything that exists across all domains. But the per-domain ontology is buildable."

Tenant Isolation materializes this: each tenant builds its own [[Ontology as Code|ontology]]. The finance team has docs about compliance and regulation. The infra team has docs about AWS and Terraform. Each operates in its own [[Subset]] of the [[Sample Space]] -- without interference.

## In the POC

The POC is single-tenant by design -- `DOCS_DIR = Path(__file__).parent / "docs"` points to a fixed directory. The change to multi-tenant is swapping `Path` for an S3 client with a dynamic prefix. The [[MCP Primitives|tool]] interface does not change -- `search_docs(query)` stays the same, but searches within the tenant's prefix.

## [[Path Traversal Protection]] as Preview

The POC's `_safe_path()` already implements a primitive form of isolation: it ensures access stays within `docs/` or `diagrams/`. In production, Tenant Isolation scales this concept: it ensures access stays within the tenant's namespace.

---

Related to: [[Production Architecture]], [[MCP Gateway]], [[S3 as Persistent Ontology]], [[Ontology as Code]], [[Three Security Layers]], [[Path Traversal Protection]], [[docs-server]]
