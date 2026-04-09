# web-to-docs

The [[Ontologia como Código|ontology]] builder. `web_to_docs_server.py` fetches web pages, converts [[HTML para Markdown]], and saves to `docs/` for the [[docs-server]] to search. Solves the problem of private docs behind authentication.

---

## Implementation

```python
mcp = FastMCP("web-to-docs", instructions="Fetch websites and convert them to markdown documentation.")
```

Four [[Primitivas MCP|tools]], two [[Primitivas MCP|prompts]]:

| Type | Name | Function |
|---|---|---|
| Tool | `convert_url(url)` | Fetches page, returns markdown (without saving) |
| Tool | `save_as_doc(url, filename)` | Fetches, converts, saves to `docs/` |
| Tool | `batch_convert(urls)` | Fetches multiple URLs, auto-names, saves |
| Tool | `crawl_docs(url, max_pages, path_prefix)` | Crawls docs site following internal links (max 100 pages) |
| Prompt | `research_and_answer(question)` | Template: local search -> web search -> save -> respond |
| Prompt | `fetch_project_docs(technology)` | Template: build local library for a technology |

## Conversion Pipeline

The [[HTML para Markdown|conversion]] follows the pipeline:

```
URL -> httpx.get() -> HTML -> BeautifulSoup (parse) -> markdownify (convert) -> regex cleanup -> .md in docs/
```

`crawl_docs` adds: same-prefix link extraction, BFS queue, deduplication, and auto-naming via title slug.

## Role in the Thesis

web-to-docs is the mechanism that **expands** the [[Ontologia como Código|ontology]]. If [[docs-server]] is the warehouse, web-to-docs is the supplier.

In [[Teoria dos Conjuntos]]: web-to-docs expands the [[Subconjunto]] A subset of S. Each `crawl_docs` adds elements to A. The complement S \ A ([[Alucinação]] zone) shrinks.

It is the component that closes the [[Feedback Loop Determinístico]]: "not found locally -> search the web -> save -> now searchable."

## Caveat: verify=False

```python
def _fetch(url: str) -> httpx.Response:
    resp = httpx.get(url, follow_redirects=True, timeout=30, verify=False)
```

`verify=False` disables TLS certificate validation. Acceptable in the POC to simplify development. In production, it must be removed -- it is a security red flag in audits. It is part of the changes needed for the [[Arquitetura de Produção]].

## In the [[Cadeia de Servers]]

web-to-docs is the second server in the chain -- activated when [[docs-server]] does not find results. It feeds docs-server with new knowledge. The `research_and_answer` prompt orchestrates exactly this chain: local search -> web -> save -> local search -> respond.

---

Related to: [[Ontologia como Código]], [[docs-server]], [[HTML para Markdown]], [[FastMCP]], [[Primitivas MCP]], [[Feedback Loop Determinístico]], [[Cadeia de Servers]], [[Path Traversal Protection]], [[Arquitetura de Produção]], [[Agente na POC]]
