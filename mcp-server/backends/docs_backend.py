"""
Docs backend — Python library for searching/browsing local markdown docs.

Not an MCP server. Used internally by mcp-marvin.
Uses Pathlib for all filesystem operations with path traversal protection.
Semantic search via Milvus IVF_FLAT index with keyword fallback.
"""

import logging
from pathlib import Path

log = logging.getLogger(__name__)

DOCS_DIR = Path(__file__).parent.parent.parent / "docs"


def _safe_path(filename: str) -> Path | None:
    """Resolve filename and ensure it stays inside DOCS_DIR."""
    path = (DOCS_DIR / filename).resolve()
    if not str(path).startswith(str(DOCS_DIR.resolve())):
        return None
    return path


def search_docs(query: str) -> str:
    """Semantic search over docs via Milvus. Keyword fallback if Milvus is down."""
    if not query.strip():
        return "Please provide a non-empty search query."

    # Primary: semantic search via Milvus
    try:
        from . import memory
        hits = memory.search_doc_chunks(query, limit=5)
        if hits:
            parts = [f"Found {len(hits)} result(s) for '{query}':\n"]
            for h in hits:
                parts.append(
                    f"**{h.get('doc_name', '?')}.md** — {h.get('heading', '')} "
                    f"(score={h['score']:.3f}):\n```\n{h.get('content', '')[:500]}\n```"
                )
            return "\n\n".join(parts)
    except Exception:
        pass

    # Fallback: keyword grep (Milvus down or empty)
    query_lower = query.lower()
    results: list[str] = []

    for doc in sorted(DOCS_DIR.glob("*.md")):
        lines = doc.read_text().splitlines()
        for i, line in enumerate(lines):
            if query_lower in line.lower():
                start = max(0, i - 1)
                end = min(len(lines), i + 2)
                snippet = "\n".join(lines[start:end])
                results.append(f"**{doc.name}** (line {i + 1}):\n```\n{snippet}\n```")

    if results:
        log.info("search_docs keyword fallback: %d matches for '%s'", len(results), query[:60])
        return f"Found {len(results)} match(es) (keyword fallback):\n\n" + "\n\n".join(results)

    return f"No results found for '{query}'."


def list_docs() -> list[str]:
    """List all available documentation files."""
    return [doc.name for doc in sorted(DOCS_DIR.glob("*.md"))]


def get_doc_summary(filename: str) -> str:
    """Return the first section of a documentation file."""
    path = _safe_path(filename)
    if not path or not path.is_file():
        return f"Document '{filename}' not found."

    text = path.read_text()
    sections = text.split("\n## ")
    summary = sections[0] if len(sections) <= 1 else sections[0] + "\n## " + sections[1]
    return summary.strip()


def read_doc(filename: str) -> str:
    """Read the full contents of a documentation file."""
    path = _safe_path(filename)
    if not path or not path.is_file():
        return f"Document '{filename}' not found."
    return path.read_text()
