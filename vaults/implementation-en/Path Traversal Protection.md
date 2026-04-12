# Path Traversal Protection

The `_safe_path()` function present in all servers that accept filenames. It resolves the path and ensures it stays within the allowed directory (`docs/` or `diagrams/`). Security boundary against directory traversal.

---

## Implementation

```python
def _safe_path(filename: str) -> Path | None:
    path = (DOCS_DIR / filename).resolve()
    if not str(path).startswith(str(DOCS_DIR.resolve())):
        return None
    return path
```

The pattern repeats in each server:
- [[docs-server]]: `_safe_path()` confines to `docs/`
- [[web-to-docs]]: `_safe_doc_path()` confines to `docs/`
- [[system-design]]: `_safe_diagram_path()` confines to `diagrams/`

## What It Prevents

Without the protection, an input like `../../etc/passwd` would resolve outside the allowed directory. The `.resolve()` canonicalizes the path (resolves `..`), and the `startswith` check verifies the result is within the expected directory.

If the check fails, it returns `None`. The tools check and return an error: `"Document '{filename}' not found."` -- instead of accessing arbitrary files.

## In the Thesis

Path Traversal Protection is a [[Decision Boundary]] implemented in code. Inside `docs/` = safe zone (the [[Subset]] A). Outside `docs/` = forbidden zone (complement S \ A).

It is the same principle as [[Anti-Hallucination]]: confining the system to the mapped domain and rejecting everything outside. In the thesis, the model is confined to the [[Sample Space]] defined by the [[Context]]. In the code, files are confined to the directory defined by the protection.

## Preview of [[Tenant Isolation]]

In [[Production Architecture|production]], `_safe_path()` evolves into per-tenant isolation: instead of confining to `docs/`, it confines to `tenant-a/docs/`. The principle is the same -- different scale.

---

Related to: [[docs-server]], [[web-to-docs]], [[system-design]], [[Anti-Hallucination]], [[Tenant Isolation]], [[Production Architecture]], [[Decision Boundary]]
