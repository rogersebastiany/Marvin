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


# ═══════════════════════════════════════════════════════════════════════════════
# RESEARCH FLOW — Fetch → Merge in-memory → Compare with existing → Save final
# ═══════════════════════════════════════════════════════════════════════════════


def _extract_title(md: str) -> str:
    """Extract the first H1 title from markdown, or return empty string."""
    match = re.search(r"^#\s+(.+)", md, re.MULTILINE)
    return match.group(1).strip() if match else ""


def _existing_doc_content(topic_slug: str) -> str | None:
    """Return existing doc content if a file matching the slug exists."""
    path = DOCS_DIR / f"{topic_slug}.md"
    if path.is_file():
        return path.read_text()
    return None


def research_topic(urls: list[str], topic: str, save_as: str = "") -> str:
    """Fetch multiple URLs into memory, merge, compare with existing docs, save final.

    New web-to-docs flow:
      1. Fetch all URLs → in-memory markdown per page
      2. Merge into a single document with sections per source
      3. Compare with existing doc (if any) — report what's new
      4. Save final consolidated document with bibliography

    Args:
        urls: List of URLs to fetch and consolidate
        topic: Topic name (used as document title and for finding existing docs)
        save_as: Filename to save as (default: slugified topic)

    Returns:
        The consolidated document content and a save report.
    """
    if not urls:
        return "No URLs provided."

    # Step 1: Fetch all URLs into memory
    fetched: list[dict] = []
    errors: list[str] = []

    for url in urls:
        try:
            md = _fetch_and_convert(url)
            title = _extract_title(md) or url.split("/")[-1]
            fetched.append({"url": url, "title": title, "content": md})
        except Exception as e:
            errors.append(f"  {url} → ERROR: {e}")

    if not fetched:
        error_report = "\n".join(errors)
        return f"All URLs failed:\n{error_report}"

    # Step 2: Merge into single document with sections
    sections: list[str] = [f"# {topic}\n"]

    for i, page in enumerate(fetched, 1):
        # Strip the page's own H1 to avoid duplicate titles
        content = re.sub(r"^#\s+.+\n*", "", page["content"], count=1).strip()
        sections.append(f"## {i}. {page['title']}\n\n{content}")

    # Bibliography
    bib_lines = [f"## Bibliography\n"]
    for i, page in enumerate(fetched, 1):
        bib_lines.append(f"{i}. [{page['title']}]({page['url']})")
    sections.append("\n".join(bib_lines))

    consolidated = "\n\n---\n\n".join(sections)

    # Step 3: Compare with existing doc
    slug = save_as.replace(".md", "") if save_as else _slugify(topic)
    existing = _existing_doc_content(slug)
    comparison = ""

    if existing:
        existing_len = len(existing)
        new_len = len(consolidated)
        existing_lines = set(existing.splitlines())
        new_lines = set(consolidated.splitlines())
        added = len(new_lines - existing_lines)
        removed = len(existing_lines - new_lines)
        comparison = (
            f"\n\n## Comparison with existing doc\n"
            f"- Existing: {existing_len:,} chars\n"
            f"- New: {new_len:,} chars\n"
            f"- Lines added: {added}\n"
            f"- Lines removed: {removed}\n"
        )

    # Step 4: Save final document
    filename = f"{slug}.md" if not slug.endswith(".md") else slug
    path = _safe_doc_path(filename)
    if not path:
        return f"Invalid filename '{filename}'."

    path.write_text(consolidated)

    # Report
    report_lines = [
        f"## Research complete: {topic}",
        f"- Sources fetched: {len(fetched)}/{len(urls)}",
        f"- Final document: docs/{filename} ({len(consolidated):,} chars)",
    ]
    if errors:
        report_lines.append(f"- Fetch errors: {len(errors)}")
        report_lines.extend(errors)
    if comparison:
        report_lines.append(comparison)

    return "\n".join(report_lines)
