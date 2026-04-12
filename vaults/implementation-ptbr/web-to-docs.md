# web-to-docs

O construtor de [[Ontologia como Código|ontologia]]. `web_to_docs_server.py` busca páginas web, converte [[HTML para Markdown]], e salva em `docs/` para o [[docs-server]] pesquisar. Resolve o problema de docs privadas atrás de autenticação.

---

## Implementação

```python
mcp = FastMCP("web-to-docs", instructions="Fetch websites and convert them to markdown documentation.")
```

Quatro [[Primitivas MCP|tools]], dois [[Primitivas MCP|prompts]]:

| Tipo | Nome | Função |
|---|---|---|
| Tool | `convert_url(url)` | Busca página, retorna markdown (sem salvar) |
| Tool | `save_as_doc(url, filename)` | Busca, converte, salva em `docs/` |
| Tool | `batch_convert(urls)` | Busca múltiplas URLs, auto-nomeia, salva |
| Tool | `crawl_docs(url, max_pages, path_prefix)` | Crawlea site de docs seguindo links internos (max 100 páginas) |
| Prompt | `research_and_answer(question)` | Template: busca local → busca web → salva → responde |
| Prompt | `fetch_project_docs(technology)` | Template: constrói biblioteca local de uma tecnologia |

## Pipeline de Conversão

A [[HTML para Markdown|conversão]] segue o pipeline:

```
URL → httpx.get() → HTML → BeautifulSoup (parse) → markdownify (convert) → regex cleanup → .md em docs/
```

O `crawl_docs` adiciona: extração de links same-prefix, fila BFS, deduplicação, e auto-nomeação via slug do título.

## Papel na Tese

O web-to-docs é o mecanismo que **expande** a [[Ontologia como Código|ontologia]]. Se o [[docs-server]] é o armazém, o web-to-docs é o fornecedor.

Na [[Teoria dos Conjuntos]]: o web-to-docs expande o [[Subconjunto]] A ⊂ S. Cada `crawl_docs` adiciona elementos a A. O complemento S \ A (zona de [[Alucinação]]) diminui.

É o componente que fecha o [[Feedback Loop Determinístico]]: "não encontrou localmente → busca na web → salva → agora é buscável."

## Caveat: verify=False

```python
def _fetch(url: str) -> httpx.Response:
    resp = httpx.get(url, follow_redirects=True, timeout=30, verify=False)
```

`verify=False` desabilita validação de certificado TLS. Aceitável na POC para simplificar desenvolvimento. Em produção, deve ser removido — é red flag de segurança em auditoria. Faz parte das mudanças necessárias para a [[Arquitetura de Produção]].

## Na [[Cadeia de Servers]]

O web-to-docs é o segundo server na cadeia — ativado quando o [[docs-server]] não encontra. Alimenta o docs-server com conhecimento novo. O prompt `research_and_answer` orquestra exatamente essa cadeia: busca local → web → salva → busca local → responde.

---

Relaciona-se com: [[Ontologia como Código]], [[docs-server]], [[HTML para Markdown]], [[FastMCP]], [[Primitivas MCP]], [[Feedback Loop Determinístico]], [[Cadeia de Servers]], [[Path Traversal Protection]], [[Arquitetura de Produção]], [[Agente na POC]]
