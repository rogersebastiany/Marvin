"""
Web-to-docs backend — Fetch websites and convert to local markdown.

Not an MCP server. Used internally by mcp-marvin.
"""

import re
from pathlib import Path
from urllib.parse import urljoin, urlparse

import httpx
from bs4 import BeautifulSoup
from markdownify import markdownify

DOCS_DIR = Path(__file__).parent / "docs"


def _safe_doc_path(filename: str) -> Path | None:
    path = (DOCS_DIR / filename).resolve()
    if not str(path).startswith(str(DOCS_DIR.resolve())):
        return None
    return path


def _slugify(text: str) -> str:
    text = re.sub(r"[^\w\s-]", "", text.lower())
    return re.sub(r"[\s_]+", "-", text).strip("-")[:80]


_HEADERS = {
    "User-Agent": "Marvin/1.0 (knowledge-graph-builder; +https://github.com/rogersebastiany/Marvin)",
}


def _fetch(url: str) -> httpx.Response:
    resp = httpx.get(url, headers=_HEADERS, follow_redirects=True, timeout=30)
    resp.raise_for_status()
    return resp


def _html_to_md(html: str) -> str:
    md = markdownify(html, heading_style="ATX", strip=["img", "script", "style"])
    return re.sub(r"\n{3,}", "\n\n", md).strip()


def _fetch_and_convert(url: str) -> str:
    return _html_to_md(_fetch(url).text)


def _extract_links(html: str, base_url: str, prefix: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    links: list[str] = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith(("#", "mailto:", "javascript:")):
            continue
        absolute = urljoin(base_url, href).split("#")[0]
        if absolute.startswith(prefix) and absolute not in links:
            links.append(absolute)
    return links


def convert_url(url: str) -> str:
    """Fetch a webpage and return its content as markdown."""
    return _fetch_and_convert(url)


def save_as_doc(url: str, filename: str) -> str:
    """Fetch a webpage, convert to markdown, and save to docs/."""
    if not filename.endswith(".md"):
        filename += ".md"
    path = _safe_doc_path(filename)
    if not path:
        return f"Invalid filename '{filename}'."
    md = _fetch_and_convert(url)
    path.write_text(md)
    return f"Saved {len(md)} chars to docs/{filename}"


def batch_convert(urls: list[str]) -> str:
    """Fetch multiple webpages and save each as markdown."""
    results: list[str] = []
    for url in urls:
        try:
            md = _fetch_and_convert(url)
            title_match = re.search(r"^#\s+(.+)", md, re.MULTILINE)
            slug = _slugify(title_match.group(1) if title_match else url.split("/")[-1])
            filename = f"{slug}.md" if slug else "untitled.md"
            (DOCS_DIR / filename).write_text(md)
            results.append(f"  {url} → docs/{filename} ({len(md)} chars)")
        except Exception as e:
            results.append(f"  {url} → ERROR: {e}")
    return f"Processed {len(urls)} URL(s):\n" + "\n".join(results)


def crawl_docs(url: str, max_pages: int = 20, path_prefix: str = "") -> str:
    """Crawl a documentation site, saving each page as markdown."""
    max_pages = min(max_pages, 100)
    if not path_prefix:
        parsed = urlparse(url)
        dir_path = parsed.path.rsplit("/", 1)[0] + "/"
        path_prefix = f"{parsed.scheme}://{parsed.netloc}{dir_path}"

    visited: set[str] = set()
    queue: list[str] = [url]
    results: list[str] = []
    errors: list[str] = []

    while queue and len(visited) < max_pages:
        current = queue.pop(0)
        if current in visited:
            continue
        visited.add(current)
        try:
            resp = _fetch(current)
            html = resp.text
            md = _html_to_md(html)
            title_match = re.search(r"^#\s+(.+)", md, re.MULTILINE)
            slug = _slugify(title_match.group(1) if title_match else current.split("/")[-1])
            if not slug:
                slug = f"page-{len(visited)}"
            filename = f"{slug}.md"
            out_path = DOCS_DIR / filename
            counter = 1
            while out_path.exists():
                out_path = DOCS_DIR / f"{slug}-{counter}.md"
                counter += 1
            out_path.write_text(md)
            results.append(f"  {current} → docs/{out_path.name} ({len(md)} chars)")
            for link in _extract_links(html, current, path_prefix):
                if link not in visited:
                    queue.append(link)
        except Exception as e:
            errors.append(f"  {current} → ERROR: {e}")

    summary = f"Crawled {len(results)} page(s) (limit: {max_pages}):\n" + "\n".join(results)
    if errors:
        summary += f"\n\nErrors ({len(errors)}):\n" + "\n".join(errors)
    remaining = len([u for u in queue if u not in visited])
    if remaining:
        summary += f"\n\n{remaining} link(s) not visited (hit max_pages limit)."
    return summary
