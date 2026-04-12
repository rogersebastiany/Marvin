# Path Traversal Protection

Função `_safe_path()` presente em todos os servers que aceitam filenames. Resolve o path e garante que fica dentro do diretório permitido (`docs/` ou `diagrams/`). Fronteira de segurança contra directory traversal.

---

## Implementação

```python
def _safe_path(filename: str) -> Path | None:
    path = (DOCS_DIR / filename).resolve()
    if not str(path).startswith(str(DOCS_DIR.resolve())):
        return None
    return path
```

O pattern se repete em cada server:
- [[docs-server]]: `_safe_path()` confina a `docs/`
- [[web-to-docs]]: `_safe_doc_path()` confina a `docs/`
- [[system-design]]: `_safe_diagram_path()` confina a `diagrams/`

## O que Previne

Sem a proteção, um input como `../../etc/passwd` seria resolvido para fora do diretório permitido. O `.resolve()` canonicaliza o path (resolve `..`), e o `startswith` verifica se o resultado está dentro do diretório esperado.

Se a verificação falha, retorna `None`. As tools checam e retornam erro: `"Document '{filename}' not found."` — em vez de acessar arquivos arbitrários.

## Na Tese

Path Traversal Protection é uma [[Decision Boundary]] implementada em código. Dentro de `docs/` = zona segura (o [[Subconjunto]] A). Fora de `docs/` = zona proibida (complemento S \ A).

É o mesmo princípio da [[Anti-Alucinação]]: confinar o sistema ao domínio mapeado e rejeitar tudo que está fora. Na tese, o modelo é confinado ao [[Espaço Amostral]] definido pelo [[Contexto]]. No código, os arquivos são confinados ao diretório definido pela proteção.

## Preview de [[Tenant Isolation]]

Em [[Arquitetura de Produção|produção]], o `_safe_path()` evolui para isolamento por tenant: em vez de confinar a `docs/`, confina a `tenant-a/docs/`. O princípio é o mesmo — escala diferente.

---

Relaciona-se com: [[docs-server]], [[web-to-docs]], [[system-design]], [[Anti-Alucinação]], [[Tenant Isolation]], [[Arquitetura de Produção]], [[Decision Boundary]]
