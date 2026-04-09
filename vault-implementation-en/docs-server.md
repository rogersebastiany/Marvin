# docs-server

The [[Ontology as Code|ontology]] warehouse. `server.py` exposes the `docs/` directory as a searchable knowledge base via [[FastMCP]]. It is the server that answers "what do we know?"

---

## Implementation

```python
mcp = FastMCP("docs-server", instructions="Search and browse project documentation.")
DOCS_DIR = Path(__file__).parent / "docs"
```

Three [[MCP Primitives|tools]], one [[MCP Primitives|resource]], two [[MCP Primitives|prompts]]:

| Type | Name | Function |
|---|---|---|
| Tool | `search_docs(query)` | Keyword search across all `.md` files, returns matches with context (1 line before/after) |
| Tool | `list_docs()` | Lists all available markdown files |
| Tool | `get_doc_summary(filename)` | Returns title + first section of a doc |
| Resource | `docs://{filename}` | Complete content of a file -- O(1) access |
| Prompt | `explain_concept(topic)` | Template: search docs + explain concept |
| Prompt | `onboarding_guide()` | Template: generate onboarding guide from all docs |

## Role in the Thesis

The docs-server is the materialized [[Ontology]]. In [[Set Theory]], `docs/` contains the [[Subset]] A subset of S -- the mapped knowledge. `search_docs` is the intersection operation A intersection Q (ontology intersection query) that produces the relevant [[Programmatic Context|context]].

What is not in `docs/` is the complement S \ A -- the [[Hallucination]] zone. That is why [[web-to-docs]] exists: to expand A.

## [[Path Traversal Protection]]

```python
def _safe_path(filename: str) -> Path | None:
    path = (DOCS_DIR / filename).resolve()
    if not str(path).startswith(str(DOCS_DIR.resolve())):
        return None
    return path
```

Resolves the path and ensures it stays within `docs/`. Prevents directory traversal (`../../etc/passwd`). Every tool that accepts a filename uses `_safe_path`. It is the server's security boundary.

## In the [[Server Chain]]

The docs-server is the first server consulted. The typical flow:
1. Agent asks something -> `search_docs` -> found -> responds based on the doc
2. Agent asks something -> `search_docs` -> not found -> [[web-to-docs]] fetches and saves -> `search_docs` again -> now finds it

It is the entry and return point of the [[Deterministic Feedback Loop]].

## Production

In production, `DOCS_DIR = Path("docs")` becomes an [[S3 as Persistent Ontology|S3]] client -- `Path.read_text()` -> `s3.get_object()`. The tool interface does not change. It is the decoupling that allows scaling without rewriting.

---

Related to: [[Ontology as Code]], [[FastMCP]], [[MCP Primitives]], [[Programmatic Context]], [[Path Traversal Protection]], [[Server Chain]], [[Deterministic Feedback Loop]], [[web-to-docs]], [[Agent in POC]], [[S3 as Persistent Ontology]]
