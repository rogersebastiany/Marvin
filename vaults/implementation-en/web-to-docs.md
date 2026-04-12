# web-to-docs

The [[Ontology as Code|ontology]] builder. `web_to_docs_server.py` fetches web pages, converts [[HTML to Markdown]], and saves to `docs/` for the [[docs-server]] to search. Solves the problem of private docs behind authentication.

---

## Implementation

```python
mcp = FastMCP("web-to-docs", instructions="Fetch websites and convert them to markdown documentation.")
```

Four [[MCP Primitives|tools]], two [[MCP Primitives|prompts]]:

| Type | Name | Function |
|---|---|---|
| Tool | `convert_url(url)` | Fetches page, returns markdown (without saving) |
| Tool | `save_as_doc(url, filename)` | Fetches, converts, saves to `docs/` |
| Tool | `batch_convert(urls)` | Fetches multiple URLs, auto-names, saves |
| Tool | `crawl_docs(url, max_pages, path_prefix)` | Crawls docs site following internal links (max 100 pages) |
| Prompt | `research_and_answer(question)` | Template: local search -> web search -> save -> respond |
| Prompt | `fetch_project_docs(technology)` | Template: build local library for a technology |

## Conversion Pipeline

The [[HTML to Markdown|conversion]] follows the pipeline:

```
URL -> httpx.get() -> HTML -> BeautifulSoup (parse) -> markdownify (convert) -> regex cleanup -> .md in docs/
```

`crawl_docs` adds: same-prefix link extraction, BFS queue, deduplication, and auto-naming via title slug.

## Role in the Thesis

web-to-docs is the mechanism that **expands** the [[Ontology as Code|ontology]]. If [[docs-server]] is the warehouse, web-to-docs is the supplier.

In [[Set Theory]]: web-to-docs expands the [[Subset]] A subset of S. Each `crawl_docs` adds elements to A. The complement S \ A ([[Hallucination]] zone) shrinks.

It is the component that closes the [[Deterministic Feedback Loop]]: "not found locally -> search the web -> save -> now searchable."

## Caveat: verify=False

```python
def _fetch(url: str) -> httpx.Response:
    resp = httpx.get(url, follow_redirects=True, timeout=30, verify=False)
```

`verify=False` disables TLS certificate validation. Acceptable in the POC to simplify development. In production, it must be removed -- it is a security red flag in audits. It is part of the changes needed for the [[Production Architecture]].

## In the [[Server Chain]]

web-to-docs is the second server in the chain -- activated when [[docs-server]] does not find results. It feeds docs-server with new knowledge. The `research_and_answer` prompt orchestrates exactly this chain: local search -> web -> save -> local search -> respond.

---

Related to: [[Ontology as Code]], [[docs-server]], [[HTML to Markdown]], [[FastMCP]], [[MCP Primitives]], [[Deterministic Feedback Loop]], [[Server Chain]], [[Path Traversal Protection]], [[Production Architecture]], [[Agent in POC]]
