# S3 como Ontologia Persistente

Em [[Arquitetura de Produção|produção]], o filesystem local (`docs/`, `diagrams/`) é substituído por Amazon S3 com encryption KMS. A [[Ontologia como Código|ontologia]] persiste com escala infinita, 99.999999999% de durabilidade, e encryption per-tenant.

---

## De Local para S3

| POC | Produção |
|---|---|
| `Path("docs").glob("*.md")` | `s3.list_objects(Prefix="tenant/docs/")` |
| `path.read_text()` | `s3.get_object(Key="tenant/docs/file.md")` |
| `path.write_text(md)` | `s3.put_object(Key="tenant/docs/file.md", Body=md)` |

A interface é limpa o suficiente para essa troca ser simples. O [[docs-server]] e [[web-to-docs]] substituem operações de `Path` por operações S3. As [[Primitivas MCP|tools]] — `search_docs`, `save_as_doc`, `crawl_docs` — mantêm a mesma assinatura.

## Encryption

**SSE-KMS:** Cada objeto é encriptado com uma data key única derivada de uma chave mestra no KMS. O modelo de envelope encryption garante que revogar a chave mestra torna todos os objetos ilegíveis instantaneamente.

**Chaves por tenant:** Cada [[Tenant Isolation|tenant]] tem sua própria chave KMS. Isolamento criptográfico real — não apenas lógico (prefixo) mas físico (chave diferente).

**Rotação automática:** KMS rotaciona chaves automaticamente. Objetos existentes continuam legíveis (a data key antiga está no envelope). Novos objetos usam a nova chave.

## Na Tese

A [[Ontologia como Código|ontologia]] precisa sobreviver entre sessões para que o [[Feedback Loop Determinístico]] funcione a longo prazo. Na POC, docs salvos por `crawl_docs` persistem no filesystem. Em produção, persistem no S3 — com backup, versionamento, e encryption.

O [[RAG Implícito]] se beneficia diretamente: o corpus de conhecimento acumulado não é perdido se o container reinicia. A acumulação descrita no [[Ultra-Long-Horizon Agentic Science]] requer persistência — S3 garante isso.

## Auditabilidade

Todo acesso ao S3 é logável via CloudTrail. Quem leu qual documento, quando, de qual container. Em domínios regulados, essa auditabilidade é requisito — e é parte da equação da tese (Observabilidade).

---

Relaciona-se com: [[Arquitetura de Produção]], [[Ontologia como Código]], [[Tenant Isolation]], [[Feedback Loop Determinístico]], [[RAG Implícito]], [[docs-server]], [[web-to-docs]], [[MCP Gateway]], [[Três Camadas de Segurança]]
