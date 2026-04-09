# docs-server

O armazém de [[Ontologia como Código|ontologia]]. `server.py` expõe o diretório `docs/` como base de conhecimento pesquisável via [[FastMCP]]. É o server que responde "o que sabemos?"

---

## Implementação

```python
mcp = FastMCP("docs-server", instructions="Search and browse project documentation.")
DOCS_DIR = Path(__file__).parent / "docs"
```

Três [[Primitivas MCP|tools]], um [[Primitivas MCP|resource]], dois [[Primitivas MCP|prompts]]:

| Tipo | Nome | Função |
|---|---|---|
| Tool | `search_docs(query)` | Busca keyword em todos os `.md`, retorna matches com contexto (1 linha antes/depois) |
| Tool | `list_docs()` | Lista todos os arquivos markdown disponíveis |
| Tool | `get_doc_summary(filename)` | Retorna título + primeira seção de um doc |
| Resource | `docs://{filename}` | Conteúdo completo de um arquivo — acesso O(1) |
| Prompt | `explain_concept(topic)` | Template: busca docs + explica conceito |
| Prompt | `onboarding_guide()` | Template: gera guia de onboarding a partir de todos os docs |

## Papel na Tese

O docs-server é a [[Ontologia]] materializada. Na [[Teoria dos Conjuntos]], `docs/` contém o [[Subconjunto]] A ⊂ S — o conhecimento mapeado. `search_docs` é a operação de interseção A ∩ Q (ontologia ∩ query) que produz o [[Contexto Programático|contexto]] relevante.

O que não está em `docs/` é o complemento S \ A — zona de [[Alucinação]]. Por isso o [[web-to-docs]] existe: para expandir A.

## [[Path Traversal Protection]]

```python
def _safe_path(filename: str) -> Path | None:
    path = (DOCS_DIR / filename).resolve()
    if not str(path).startswith(str(DOCS_DIR.resolve())):
        return None
    return path
```

Resolve o path e garante que fica dentro de `docs/`. Previne directory traversal (`../../etc/passwd`). Cada tool que aceita filename usa `_safe_path`. É a fronteira de segurança do server.

## Na [[Cadeia de Servers]]

O docs-server é o primeiro server consultado. O fluxo típico:
1. Agente pergunta algo → `search_docs` → encontra → responde com base no doc
2. Agente pergunta algo → `search_docs` → não encontra → [[web-to-docs]] busca e salva → `search_docs` de novo → agora encontra

É o ponto de entrada e retorno do [[Feedback Loop Determinístico]].

## Produção

Em produção, `DOCS_DIR = Path("docs")` vira um client [[S3 como Ontologia Persistente|S3]] — `Path.read_text()` → `s3.get_object()`. A interface das tools não muda. É o desacoplamento que permite escalar sem reescrever.

---

Relaciona-se com: [[Ontologia como Código]], [[FastMCP]], [[Primitivas MCP]], [[Contexto Programático]], [[Path Traversal Protection]], [[Cadeia de Servers]], [[Feedback Loop Determinístico]], [[web-to-docs]], [[Agente na POC]], [[S3 como Ontologia Persistente]]
