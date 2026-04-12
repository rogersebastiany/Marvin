# HTML to Markdown

The conversion pipeline in [[web-to-docs]] that transforms web pages into searchable documentation. `httpx` + `BeautifulSoup` + `markdownify` -> `.md` file in `docs/`.

---

## The Pipeline

```
URL -> httpx.get(url, verify=False) -> HTML
  -> markdownify(html, heading_style="ATX", strip=["img", "script", "style"]) -> Raw Markdown
  -> regex cleanup (collapse 3+ newlines into 2) -> Clean Markdown
  -> Path.write_text() -> docs/{slug}.md
```

## Components

**httpx:** Asynchronous HTTP client. `follow_redirects=True`, `timeout=30`. The `verify=False` disables TLS validation -- caveat for [[Production Architecture|production]].

**BeautifulSoup:** HTML parser used by `crawl_docs` to extract links (`<a href="...">`) and build the BFS crawling queue. Filters by same-prefix to avoid leaving the site.

**markdownify:** Converts HTML to Markdown with ATX headings (`#`, `##`). Strips `img`, `script`, `style` -- removes noise, keeps textual content.

## Auto-Naming

`crawl_docs` and `batch_convert` derive filenames automatically:

```python
def _slugify(text: str) -> str:
    text = re.sub(r"[^\w\s-]", "", text.lower())
    return re.sub(r"[\s_]+", "-", text).strip("-")[:80]
```

Extracts the title from the first `# heading` in the markdown, slugifies it, and saves as `{slug}.md`. If the file already exists, adds a counter: `{slug}-1.md`, `{slug}-2.md`.

## Role in the Thesis

The pipeline is the mechanism for **building [[Ontology as Code|ontology]]**. The web contains knowledge, but in a format not searchable by the [[docs-server]]. The pipeline converts it to markdown -- a format that `search_docs` can index.

Each converted page expands the [[Subset]] A subset of S. The complement S \ A ([[Hallucination]] zone) shrinks. It is the [[Deterministic Feedback Loop]] materialized: web -> markdown -> searchable -> more [[Programmatic Context|context]] -> more [[Measurable Determinism|determinism]].

## Limitations

- `verify=False` -- no TLS validation
- No authentication -- cannot fetch docs behind SSO/login
- No rate limiting -- may overload sites
- Keyword search, not semantic -- [[Implicit RAG]], not full RAG
- No content deduplication -- crawl may save similar pages

In [[Production Architecture|production]], these limitations are resolved: validated TLS, auth via headers, rate limiting, and potentially semantic search with [[Embedding|embeddings]].

---

Related to: [[web-to-docs]], [[Ontology as Code]], [[Deterministic Feedback Loop]], [[Implicit RAG]], [[docs-server]], [[Production Architecture]], [[Programmatic Context]]
