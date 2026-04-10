"""
Web-to-docs backend — Fetch websites and convert to local markdown.

Not an MCP server. Used internally by mcp-marvin.
"""

import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urljoin, urlparse

import httpx
from bs4 import BeautifulSoup
from markdownify import markdownify

MAX_WORKERS = 8

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


_NOISE_TAGS = ["nav", "header", "footer", "aside", "script", "style", "noscript", "svg", "iframe"]
_NOISE_ROLES = ["navigation", "banner", "contentinfo", "complementary", "search"]
_NOISE_CLASSES = re.compile(
    r"(sidebar|toc|table-of-contents|breadcrumb|menu|nav|navbar|footer|header|"
    r"skip-to|skipnav|pagination|cookie|banner|announcement|admonition-title|"
    r"search|modal|overlay|popup|dropdown|tab-list|tablist)",
    re.IGNORECASE,
)
_NOISE_IDS = re.compile(
    r"(sidebar|toc|nav|menu|footer|header|breadcrumb|search|skip)",
    re.IGNORECASE,
)
# Content container classes, ordered by specificity
_CONTENT_CLASSES = [
    "doc-content", "main-content", "page-content", "article-content",
    "post-content", "entry-content", "markdown-body", "rst-content",
    "documentation", "prose", "content",
]


def _is_noise_element(tag) -> bool:
    """Check if a tag looks like navigation/chrome rather than content."""
    if not tag.attrs:
        return False
    classes = " ".join(tag.get("class") or [])
    tag_id = tag.get("id") or ""
    if classes and _NOISE_CLASSES.search(classes):
        return True
    if tag_id and _NOISE_IDS.search(tag_id):
        return True
    return False


def _find_content_container(soup: BeautifulSoup):
    """Find the best content container in the document.

    Checks semantic tags first (<main>, <article>, role="main"),
    then falls back to common content-class divs.
    Returns the container tag, or <body>, or the soup itself.
    """
    # Semantic containers first
    container = soup.find("main") or soup.find("article") or soup.find(attrs={"role": "main"})
    if container and len(container.get_text(strip=True)) >= 200:
        return container

    # Fall back to content-class divs
    for cls in _CONTENT_CLASSES:
        candidate = soup.find(attrs={"class": re.compile(rf"\b{cls}\b", re.IGNORECASE)})
        if candidate and len(candidate.get_text(strip=True)) >= 200:
            return candidate

    return soup.find("body") or soup


def _strip_noise(container) -> None:
    """Remove noise elements from within a content container (in-place).

    Operates AFTER the container is isolated, so we only strip noise
    inside the content area — not globally.
    Uses decompose() for elements we want to destroy entirely,
    and unwrap() for wrapper tags we want to flatten.
    """
    # Phase 1: Remove noise by tag name
    for tag in container.find_all(_NOISE_TAGS):
        tag.decompose()

    # Phase 2: Remove noise by ARIA role
    for role in _NOISE_ROLES:
        for tag in container.find_all(attrs={"role": role}):
            tag.decompose()

    # Phase 3: Remove noise by class/id patterns
    for tag in container.find_all(["div", "section", "ul", "ol", "span", "a"]):
        if _is_noise_element(tag):
            tag.decompose()

    # Phase 4: Remove hidden elements
    for tag in container.find_all(attrs={"aria-hidden": "true"}):
        tag.decompose()
    for tag in container.find_all(attrs={"hidden": True}):
        tag.decompose()

    # Phase 5: Remove toggle buttons and labels (e.g. "Show nav", "Toggle menu")
    for tag in container.find_all("button"):
        tag.decompose()
    for tag in container.find_all("label"):
        if len(tag.get_text(strip=True)) < 30:
            tag.decompose()

    # Phase 6: Unwrap <details>/<summary> to surface collapsed content
    for tag in container.find_all("summary"):
        tag.unwrap()
    for tag in container.find_all("details"):
        tag.unwrap()

    # Phase 6: Unwrap non-semantic wrapper divs/spans (no class, no id)
    # These just add nesting noise that degrades markdown quality.
    for tag in container.find_all(["span", "div"]):
        if not tag.attrs:
            tag.unwrap()

    # Phase 7: Remove empty elements left behind by decompose()
    # An element is empty if it has no text and no meaningful children
    for tag in container.find_all(["div", "section", "p", "span", "ul", "ol"]):
        if not tag.get_text(strip=True) and not tag.find(["pre", "code", "table", "img"]):
            tag.decompose()

    # Phase 8: Consolidate adjacent text nodes after all the tree surgery
    container.smooth()


def _extract_main_content(html: str) -> str:
    """Extract main content from HTML.

    Strategy: find the content container FIRST, then strip noise within it.
    This preserves content links/elements that happen to match noise patterns
    but live outside the noise regions.
    """
    soup = BeautifulSoup(html, "html.parser")

    # Step 1: Global pre-clean — remove tags that are ALWAYS noise regardless
    # of where they appear (script, style, noscript, svg, iframe)
    for tag in soup.find_all(["script", "style", "noscript", "svg", "iframe"]):
        tag.decompose()

    # Step 2: Find the content container
    container = _find_content_container(soup)

    # Step 3: Strip noise within the container
    _strip_noise(container)

    return str(container)


def _clean_markdown(md: str) -> str:
    """Post-process markdown to remove residual noise that survives HTML extraction."""
    # Remove inline JS/CSS that leaked through
    md = re.sub(r"var\s+\w+\s*=.*?[;\n]", "", md)
    md = re.sub(r"\w+\s*\{[^}]*--[\w-]+:[^}]*\}", "", md)
    md = re.sub(r"__\w+\s*=.*?[;\n]", "", md)
    # Remove "Skip to content/main" lines
    md = re.sub(r"^\[?Skip to (main )?content\]?\(#[^)]*\)\s*$", "", md, flags=re.MULTILINE)
    # Remove search placeholders
    md = re.sub(r"^(Search|Initializing search)\.{0,3}\s*$", "", md, flags=re.MULTILINE)
    md = re.sub(r"^Search the docs\.{0,3}\s*$", "", md, flags=re.MULTILINE)
    # Remove keyboard shortcut hints (⌘K, Ctrl+K)
    md = re.sub(r"^[⌘⌃]K\s*$", "", md, flags=re.MULTILINE)
    # Remove empty markdown links []() and image refs
    md = re.sub(r"\[]\([^)]*\)", "", md)
    # Remove lines that are just UI chrome text
    md = re.sub(r"^(Navigation|Documentation|Table of contents|Show nav|Toggle.*)\s*$", "", md, flags=re.MULTILINE)
    # Remove paragraph-link-only lines (leftover nav: "* [Text](/path)")
    md = re.sub(r"^\* \[.{1,50}\]\(/[^)]*\)\s*$", "", md, flags=re.MULTILINE)
    # Collapse excessive blank lines
    md = re.sub(r"\n{3,}", "\n\n", md)
    return md.strip()


def _html_to_md(html: str) -> str:
    content = _extract_main_content(html)
    md = markdownify(content, heading_style="ATX", strip=["img", "script", "style"])
    return _clean_markdown(md)


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


# ═══════════════════════════════════════════════════════════════════════════════
# URL RANKING — Two-tier probe: HEAD metadata → full body analysis
# ═══════════════════════════════════════════════════════════════════════════════

# Content types that are never documentation
_BAD_CONTENT_TYPES = {"application/pdf", "application/zip", "application/octet-stream",
                       "image/", "video/", "audio/", "font/"}

# Meta description keywords that signal documentation content
_DOC_META_KEYWORDS = re.compile(
    r"(documentation|guide|tutorial|reference|api|usage|example|install|"
    r"quickstart|getting.started|how.to|overview|configuration|setup)",
    re.IGNORECASE,
)

# Meta description keywords that signal non-documentation
_NON_DOC_META_KEYWORDS = re.compile(
    r"(pricing|sign.up|login|register|newsletter|subscribe|contact.us|"
    r"careers|about.us|press|blog.post|news|announcement)",
    re.IGNORECASE,
)


def _tier1_head(url: str) -> dict:
    """Tier 1: HEAD request — rank by HTTP headers and URL structure.

    Near-zero cost. Returns metadata signals and a pass/fail gate.
    """
    try:
        resp = httpx.head(url, headers=_HEADERS, follow_redirects=True, timeout=15)
    except httpx.HTTPError as e:
        return {"url": url, "tier1_pass": False, "reason": f"HEAD failed: {e}"}

    headers = resp.headers
    content_type = headers.get("content-type", "").lower()
    content_length = int(headers.get("content-length", 0))
    status = resp.status_code

    # Gate: reject non-2xx
    if status >= 400:
        return {"url": url, "tier1_pass": False, "reason": f"HTTP {status}"}

    # Gate: reject non-HTML content types
    if content_type and not any(t in content_type for t in ["text/html", "application/xhtml"]):
        for bad in _BAD_CONTENT_TYPES:
            if bad in content_type:
                return {"url": url, "tier1_pass": False, "reason": f"Not HTML: {content_type}"}

    # Gate: reject tiny responses (< 2KB is almost certainly not a docs page)
    # content-length is optional, so 0 means unknown — let it pass
    if content_length > 0 and content_length < 2000:
        return {"url": url, "tier1_pass": False, "reason": f"Too small: {content_length} bytes"}

    # Score URL structure
    parsed = urlparse(url)
    path_parts = [s for s in parsed.path.split("/") if s]
    path_depth = len(path_parts)
    path_lower = parsed.path.lower()

    url_score = 0
    # Deeper paths = more likely content
    if path_depth >= 3:
        url_score += 15
    elif path_depth >= 2:
        url_score += 10
    elif path_depth >= 1:
        url_score += 5

    # Path contains doc-like segments
    doc_segments = {"docs", "guide", "tutorial", "reference", "api", "manual",
                    "handbook", "learn", "getting-started", "quickstart", "advanced"}
    if any(seg in path_lower for seg in doc_segments):
        url_score += 10

    # Path looks like an index
    if path_lower in ("/", "") or path_lower.endswith("/index"):
        url_score -= 5

    return {
        "url": url,
        "tier1_pass": True,
        "content_type": content_type,
        "content_length": content_length,
        "status": status,
        "url_depth": path_depth,
        "url_score": max(url_score, 0),
    }


def _tier2_body(url: str, html: str) -> dict:
    """Tier 2: full body analysis — structural scoring + metadata extraction.

    Only called for URLs that passed tier 1.
    """
    soup = BeautifulSoup(html, "html.parser")

    # ── Extract <head> metadata ──
    head = soup.find("head")
    meta_title = ""
    meta_desc = ""
    meta_keywords = ""
    og_type = ""
    canonical = ""

    if head:
        title_tag = head.find("title")
        meta_title = title_tag.get_text(strip=True) if title_tag else ""

        desc_tag = head.find("meta", attrs={"name": "description"})
        meta_desc = (desc_tag.get("content") or "") if desc_tag else ""

        kw_tag = head.find("meta", attrs={"name": "keywords"})
        meta_keywords = (kw_tag.get("content") or "") if kw_tag else ""

        og_tag = head.find("meta", attrs={"property": "og:type"})
        og_type = (og_tag.get("content") or "") if og_tag else ""

        canon_tag = head.find("link", attrs={"rel": "canonical"})
        canonical = (canon_tag.get("href") or "") if canon_tag else ""

    # ── Metadata score (0-20 pts) ──
    meta_score = 0

    # Description signals documentation
    combined_meta = f"{meta_title} {meta_desc} {meta_keywords}"
    if _DOC_META_KEYWORDS.search(combined_meta):
        meta_score += 10
    if _NON_DOC_META_KEYWORDS.search(combined_meta):
        meta_score -= 10

    # og:type = "article" or "documentation" is a good signal
    if og_type in ("article", "documentation", "docs"):
        meta_score += 5

    # Long description = page cares about content
    if len(meta_desc) > 80:
        meta_score += 5
    elif len(meta_desc) > 30:
        meta_score += 2

    meta_score = max(meta_score, 0)

    # ── Body structural analysis ──
    # Remove script/style for text analysis
    for tag in soup.find_all(["script", "style", "noscript"]):
        tag.decompose()

    body = soup.find("body") or soup
    full_text = body.get_text(separator=" ", strip=True)
    text_len = len(full_text)

    headings = len(body.find_all(["h1", "h2", "h3", "h4"]))
    code_blocks = len(body.find_all(["pre", "code"]))
    paragraphs = len(body.find_all("p"))
    all_links = len(body.find_all("a"))
    lists = len(body.find_all(["ul", "ol"]))
    tables = len(body.find_all("table"))
    para_text = sum(len(p.get_text(strip=True)) for p in body.find_all("p"))

    # ── Body score (0-80 pts) ──
    body_score = 0

    # Text volume (0-25 pts)
    if text_len > 5000:
        body_score += 25
    elif text_len > 2000:
        body_score += 18
    elif text_len > 800:
        body_score += 10
    elif text_len > 300:
        body_score += 5

    # Paragraph density (0-20 pts)
    if para_text > 2000:
        body_score += 20
    elif para_text > 800:
        body_score += 15
    elif para_text > 300:
        body_score += 8
    elif para_text > 100:
        body_score += 4

    # Structure (0-20 pts)
    if headings >= 3:
        body_score += 8
    elif headings >= 1:
        body_score += 4
    if code_blocks >= 2:
        body_score += 7
    elif code_blocks >= 1:
        body_score += 3
    if lists >= 2 or tables >= 1:
        body_score += 5

    # Link ratio (0-15 pts)
    if all_links > 0 and text_len > 0:
        link_text = sum(len(a.get_text(strip=True)) for a in body.find_all("a"))
        link_ratio = link_text / text_len
        if link_ratio < 0.2:
            body_score += 15
        elif link_ratio < 0.4:
            body_score += 10
        elif link_ratio < 0.6:
            body_score += 5

    total = meta_score + body_score

    if total >= 55:
        verdict = "GOOD — documentation page with substantial content"
    elif total >= 30:
        verdict = "FAIR — some content, may be thin or mixed with navigation"
    else:
        verdict = "POOR — likely an index, landing, or navigation page"

    return {
        "url": url,
        "score": min(total, 100),
        "verdict": verdict,
        "meta": {
            "title": meta_title[:120],
            "description": meta_desc[:200],
            "og_type": og_type,
            "meta_score": meta_score,
        },
        "body": {
            "text_chars": text_len,
            "paragraph_chars": para_text,
            "headings": headings,
            "code_blocks": code_blocks,
            "paragraphs": paragraphs,
            "links": all_links,
            "body_score": body_score,
        },
    }


def rank_urls(urls: list[str]) -> str:
    """Probe URLs and rank by documentation quality. Two-tier analysis:

    Tier 1 (HEAD): HTTP headers + URL structure. Filters out non-HTML, errors,
    tiny pages. Near-zero cost.

    Tier 2 (GET): Full fetch + metadata extraction (<title>, <meta description>,
    og:type) + body structural analysis (text density, headings, code blocks,
    link ratio). Only runs on tier 1 survivors.

    Use BEFORE research_topic to pick the best URLs.
    """
    if not urls:
        return "No URLs provided."

    # ── Tier 1: HEAD requests in parallel ──
    tier1_pass: list[dict] = []
    tier1_fail: list[dict] = []

    with ThreadPoolExecutor(max_workers=min(MAX_WORKERS, len(urls))) as pool:
        futures = {pool.submit(_tier1_head, url): url for url in urls}
        for future in as_completed(futures):
            result = future.result()
            if result["tier1_pass"]:
                tier1_pass.append(result)
            else:
                tier1_fail.append(result)

    if not tier1_pass:
        lines = [f"## URL Ranking — all {len(urls)} URLs failed tier 1 (HEAD)\n"]
        for r in tier1_fail:
            lines.append(f"  ✗ {r['url']} — {r['reason']}")
        return "\n".join(lines)

    # ── Tier 2: full body analysis on survivors ──
    tier2_results: list[dict] = []
    tier2_errors: list[str] = []

    def _fetch_and_score(t1: dict) -> dict:
        url = t1["url"]
        resp = _fetch(url)
        t2 = _tier2_body(url, resp.text)
        # Add tier 1 URL score to total
        t2["score"] = min(t2["score"] + t1["url_score"], 100)
        t2["url_score"] = t1["url_score"]
        t2["content_length"] = t1["content_length"]
        return t2

    with ThreadPoolExecutor(max_workers=min(MAX_WORKERS, len(tier1_pass))) as pool:
        futures = {pool.submit(_fetch_and_score, t1): t1["url"] for t1 in tier1_pass}
        for future in as_completed(futures):
            url = futures[future]
            try:
                tier2_results.append(future.result())
            except Exception as e:
                tier2_errors.append(f"  {url} → ERROR: {e}")

    # Sort by score descending
    tier2_results.sort(key=lambda r: r["score"], reverse=True)

    # ── Format output ──
    lines = [
        f"## URL Ranking ({len(tier2_results)} scored, "
        f"{len(tier1_fail)} filtered by HEAD, "
        f"{len(tier2_errors)} errors)\n"
    ]

    for i, r in enumerate(tier2_results, 1):
        m = r["meta"]
        b = r["body"]
        lines.append(
            f"{i}. **[{r['score']}/100]** {r['url']}\n"
            f"   {r['verdict']}\n"
            f"   title: {m['title'][:80] or '(none)'}\n"
            f"   meta: {m['description'][:100] or '(none)'}\n"
            f"   scores: url={r['url_score']} meta={m['meta_score']} body={b['body_score']}\n"
            f"   body: text={b['text_chars']}ch, paras={b['paragraph_chars']}ch, "
            f"headings={b['headings']}, code={b['code_blocks']}, links={b['links']}"
        )

    if tier1_fail:
        lines.append(f"\nFiltered by HEAD ({len(tier1_fail)}):")
        for r in tier1_fail:
            lines.append(f"  ✗ {r['url']} — {r['reason']}")

    if tier2_errors:
        lines.append(f"\nFetch errors ({len(tier2_errors)}):")
        lines.extend(tier2_errors)

    lines.append(
        "\n**Recommendation:** Use URLs scoring 55+ for research_topic. "
        "URLs below 30 are likely navigation/index pages — find their content subpages instead."
    )

    return "\n".join(lines)


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


def _fetch_many(urls: list[str]) -> list[dict]:
    """Fetch multiple URLs in parallel. Returns list of {url, md} or {url, error}."""
    results = []

    with ThreadPoolExecutor(max_workers=min(MAX_WORKERS, len(urls))) as pool:
        future_to_url = {pool.submit(_fetch_and_convert, url): url for url in urls}
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                results.append({"url": url, "md": future.result()})
            except Exception as e:
                results.append({"url": url, "error": str(e)})

    return results


def batch_convert(urls: list[str]) -> str:
    """Fetch multiple webpages in parallel and save each as markdown."""
    results: list[str] = []
    for item in _fetch_many(urls):
        url = item["url"]
        if "error" in item:
            results.append(f"  {url} → ERROR: {item['error']}")
            continue
        md = item["md"]
        title_match = re.search(r"^#\s+(.+)", md, re.MULTILINE)
        slug = _slugify(title_match.group(1) if title_match else url.split("/")[-1])
        filename = f"{slug}.md" if slug else "untitled.md"
        (DOCS_DIR / filename).write_text(md)
        results.append(f"  {url} → docs/{filename} ({len(md)} chars)")
    return f"Processed {len(urls)} URL(s):\n" + "\n".join(results)


def crawl_docs(url: str, max_pages: int = 20, path_prefix: str = "") -> str:
    """Crawl a documentation site, saving each page as markdown.

    Uses parallel fetching per BFS level for speed.
    """
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
        # Take a batch from the queue (up to remaining budget)
        budget = max_pages - len(visited)
        batch = []
        while queue and len(batch) < budget:
            candidate = queue.pop(0)
            if candidate not in visited:
                batch.append(candidate)
                visited.add(candidate)
        if not batch:
            break

        # Fetch batch in parallel — need raw HTML for link extraction
        def _fetch_html(u: str) -> tuple[str, str, str]:
            resp = _fetch(u)
            html = resp.text
            md = _html_to_md(html)
            return u, html, md

        with ThreadPoolExecutor(max_workers=min(MAX_WORKERS, len(batch))) as pool:
            futures = {pool.submit(_fetch_html, u): u for u in batch}
            for future in as_completed(futures):
                u = futures[future]
                try:
                    _, html, md = future.result()
                    title_match = re.search(r"^#\s+(.+)", md, re.MULTILINE)
                    slug = _slugify(title_match.group(1) if title_match else u.split("/")[-1])
                    if not slug:
                        slug = f"page-{len(results) + 1}"
                    filename = f"{slug}.md"
                    out_path = DOCS_DIR / filename
                    counter = 1
                    while out_path.exists():
                        out_path = DOCS_DIR / f"{slug}-{counter}.md"
                        counter += 1
                    out_path.write_text(md)
                    results.append(f"  {u} → docs/{out_path.name} ({len(md)} chars)")
                    for link in _extract_links(html, u, path_prefix):
                        if link not in visited:
                            queue.append(link)
                except Exception as e:
                    errors.append(f"  {u} → ERROR: {e}")

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

    # Step 1: Fetch all URLs in parallel
    fetched: list[dict] = []
    errors: list[str] = []
    thin_pages: list[str] = []

    for item in _fetch_many(urls):
        if "error" in item:
            errors.append(f"  {item['url']} → ERROR: {item['error']}")
        else:
            md = item["md"]
            title = _extract_title(md) or item["url"].split("/")[-1]
            # Check content quality — real docs pages have substantial text
            text_chars = len(re.sub(r"\[.*?\]\(.*?\)", "", md))  # strip link markup
            link_count = len(re.findall(r"\[.*?\]\(.*?\)", md))
            text_ratio = text_chars / max(len(md), 1)
            if text_chars < 500 or (link_count > 20 and text_ratio < 0.4):
                thin_pages.append(
                    f"  ⚠ {item['url']} — only {text_chars} chars of text, "
                    f"{link_count} links (likely an index page, not documentation)"
                )
            fetched.append({"url": item["url"], "title": title, "content": md})

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
    if thin_pages:
        report_lines.append(f"- ⚠ Thin pages (likely index/nav pages, not real docs): {len(thin_pages)}")
        report_lines.extend(thin_pages)
        report_lines.append(
            "- TIP: These pages are mostly navigation links. Find the actual content "
            "pages (e.g. /docs/guide, /docs/api-reference) and re-run with those URLs."
        )
    if errors:
        report_lines.append(f"- Fetch errors: {len(errors)}")
        report_lines.extend(errors)
    if comparison:
        report_lines.append(comparison)

    return "\n".join(report_lines)
