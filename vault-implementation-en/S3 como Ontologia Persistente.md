# S3 as Persistent Ontology

In [[Arquitetura de Produção|production]], the local filesystem (`docs/`, `diagrams/`) is replaced by Amazon S3 with KMS encryption. The [[Ontologia como Código|ontology]] persists with infinite scale, 99.999999999% durability, and per-tenant encryption.

---

## From Local to S3

| POC | Production |
|---|---|
| `Path("docs").glob("*.md")` | `s3.list_objects(Prefix="tenant/docs/")` |
| `path.read_text()` | `s3.get_object(Key="tenant/docs/file.md")` |
| `path.write_text(md)` | `s3.put_object(Key="tenant/docs/file.md", Body=md)` |

The interface is clean enough for this swap to be simple. The [[docs-server]] and [[web-to-docs]] replace `Path` operations with S3 operations. The [[Primitivas MCP|tools]] -- `search_docs`, `save_as_doc`, `crawl_docs` -- keep the same signature.

## Encryption

**SSE-KMS:** Each object is encrypted with a unique data key derived from a master key in KMS. The envelope encryption model ensures that revoking the master key makes all objects instantly unreadable.

**Keys per tenant:** Each [[Tenant Isolation|tenant]] has its own KMS key. Real cryptographic isolation -- not just logical (prefix) but physical (different key).

**Automatic rotation:** KMS rotates keys automatically. Existing objects remain readable (the old data key is in the envelope). New objects use the new key.

## In the Thesis

The [[Ontologia como Código|ontology]] needs to survive between sessions for the [[Feedback Loop Determinístico]] to work long-term. In the POC, docs saved by `crawl_docs` persist on the filesystem. In production, they persist in S3 -- with backup, versioning, and encryption.

The [[RAG Implícito]] benefits directly: the accumulated knowledge corpus is not lost if the container restarts. The accumulation described in [[Ultra-Long-Horizon Agentic Science]] requires persistence -- S3 guarantees this.

## Auditability

All S3 access is loggable via CloudTrail. Who read which document, when, from which container. In regulated domains, this auditability is a requirement -- and is part of the thesis equation (Observability).

---

Related to: [[Arquitetura de Produção]], [[Ontologia como Código]], [[Tenant Isolation]], [[Feedback Loop Determinístico]], [[RAG Implícito]], [[docs-server]], [[web-to-docs]], [[MCP Gateway]], [[Três Camadas de Segurança]]
