"""
Rebuild all raw docs through the improved extraction pipeline.

Extracts the canonical source URL from each doc file, re-fetches through
the improved _html_to_md pipeline, and overwrites the file.

Usage:
    uv run python rebuild_docs.py          # dry run (shows what would change)
    uv run python rebuild_docs.py --apply  # actually re-fetch and overwrite
"""

import re
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

from backends.web_to_docs_backend import _fetch_and_convert, _slugify

DOCS_DIR = Path(__file__).parent.parent.parent / "docs"

# Map filename patterns to their canonical URL sources
# Format: (filename_pattern, url_template)
# {slug} is replaced with the part after the prefix
KNOWN_SOURCES = {
    "kotlin-": "https://kotlinlang.org/docs/{slug}.html",
    "kotlinx-coroutines-": "https://github.com/Kotlin/kotlinx.coroutines",
    "python-": "https://docs.python.org/3/library/{slug}.html",
    "terraform-aws-": "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/{slug}",
    "neo4j-": "https://neo4j.com/docs/",
    "milvus-": "https://milvus.io/docs/",
    "httpx-": "https://www.python-httpx.org/{slug}/",
    "fastmcp-": "https://gofastmcp.com/",
    "aws-": "https://docs.aws.amazon.com/",
    "docker-": "https://docs.docker.com/",
    "mermaid-": "https://mermaid.js.org/syntax/",
    "prometheus-": "https://prometheus.io/docs/",
    "opentelemetry-": "https://opentelemetry.io/docs/",
    "owasp-": "https://cheatsheetseries.owasp.org/",
    "github-actions-": "https://docs.github.com/en/actions/",
    "design-patterns-": "https://refactoring.guru/design-patterns/",
    "git-": "https://git-scm.com/docs/",
}


def _extract_source_url(filepath: Path) -> str | None:
    """Try to extract the canonical source URL from a doc file."""
    content = filepath.read_text(errors="replace")

    fname = filepath.stem  # e.g. "kotlin-coroutines-basics"

    # Strategy 1: Look for canonical/og:url in raw HTML remnants
    # Many docs still have the JSON-LD or meta tags embedded
    for pattern in [
        r'"url"\s*:\s*"(https?://[^"]+)"',
        r'href="(https?://[^"]+)"[^>]*rel="canonical"',
        r'content="(https?://[^"]+)"[^>]*property="og:url"',
    ]:
        match = re.search(pattern, content)
        if match:
            url = match.group(1)
            # Filter out generic/non-specific URLs
            if len(url) > 30 and not url.endswith(('.png', '.jpg', '.css', '.js')):
                return url

    # Strategy 2: Look for known URL patterns in the content
    url_patterns = {
        "kotlin": r'https://kotlinlang\.org/docs/[a-z0-9-]+\.html',
        "python": r'https://docs\.python\.org/3/library/[a-z0-9_]+\.html',
        "aws": r'https://docs\.aws\.amazon\.com/[^\s"<>)\]]+\.html',
        "terraform": r'https://registry\.terraform\.io/providers/hashicorp/aws/latest/docs/resources/[a-z0-9_]+',
        "httpx": r'https://www\.python-httpx\.org/[a-z0-9-/]+',
        "mermaid": r'https://mermaid\.js\.org/syntax/[a-z0-9-]+',
        "neo4j": r'https://neo4j\.com/docs/[^\s"<>)\]]+',
        "milvus": r'https://milvus\.io/docs/[^\s"<>)\]]+',
        "docker": r'https://docs\.docker\.com/[^\s"<>)\]]+',
        "prometheus": r'https://prometheus\.io/docs/[^\s"<>)\]]+',
        "opentelemetry": r'https://opentelemetry\.io/docs/[^\s"<>)\]]+',
        "owasp": r'https://cheatsheetseries\.owasp\.org/[^\s"<>)\]]+',
        "github-actions": r'https://docs\.github\.com/en/actions/[^\s"<>)\]]+',
        "design-patterns": r'https://refactoring\.guru/design-patterns/[a-z-]+',
        "fastmcp": r'https://gofastmcp\.com/[^\s"<>)\]]+',
        "grafana": r'https://grafana\.com/docs/[^\s"<>)\]]+',
        "argocd": r'https://argo-cd\.readthedocs\.io/[^\s"<>)\]]+',
    }

    for prefix, pattern in url_patterns.items():
        if fname.startswith(prefix) or prefix in fname:
            match = re.search(pattern, content)
            if match:
                url = match.group(0).rstrip(')')
                return url

    # Strategy 3: Known URL mappings by filename
    for prefix, template in KNOWN_SOURCES.items():
        if fname.startswith(prefix.rstrip('-')):
            slug = fname[len(prefix.rstrip('-'))+1:] if '-' in prefix else fname
            if '{slug}' in template:
                return template.format(slug=slug)

    return None


def rebuild_doc(filepath: Path, apply: bool = False) -> dict:
    """Re-fetch a single doc through the improved pipeline."""
    url = _extract_source_url(filepath)
    if not url:
        return {"file": filepath.name, "status": "SKIP", "reason": "no source URL found"}

    old_size = filepath.stat().st_size

    if not apply:
        return {"file": filepath.name, "status": "WOULD_REBUILD", "url": url, "old_size": old_size}

    try:
        new_content = _fetch_and_convert(url)
        new_size = len(new_content)

        # Sanity check: don't overwrite with tiny/empty content
        if new_size < 200:
            return {"file": filepath.name, "status": "SKIP", "reason": f"new content too small ({new_size} chars)", "url": url}

        filepath.write_text(new_content)
        return {
            "file": filepath.name,
            "status": "REBUILT",
            "url": url,
            "old_size": old_size,
            "new_size": new_size,
            "delta": new_size - old_size,
        }
    except Exception as e:
        return {"file": filepath.name, "status": "ERROR", "url": url, "error": str(e)}


def main():
    apply = "--apply" in sys.argv

    # Get all non-consolidated docs
    docs = sorted([
        f for f in DOCS_DIR.glob("*.md")
        if "consolidated" not in f.name
    ])

    print(f"{'REBUILDING' if apply else 'DRY RUN'}: {len(docs)} docs\n")

    results = {"REBUILT": [], "WOULD_REBUILD": [], "SKIP": [], "ERROR": []}

    if apply:
        # Parallel fetch with progress
        with ThreadPoolExecutor(max_workers=4) as pool:
            futures = {pool.submit(rebuild_doc, f, True): f for f in docs}
            for i, future in enumerate(as_completed(futures), 1):
                result = future.result()
                results[result["status"]].append(result)
                status = result["status"]
                print(f"[{i}/{len(docs)}] {status}: {result['file']}", end="")
                if status == "REBUILT":
                    print(f" ({result['old_size']} → {result['new_size']}, Δ{result['delta']:+d})")
                elif status == "ERROR":
                    print(f" — {result['error'][:80]}")
                else:
                    print(f" — {result.get('reason', '')}")
    else:
        for f in docs:
            result = rebuild_doc(f, False)
            results[result["status"]].append(result)
            if result["status"] == "WOULD_REBUILD":
                print(f"  ✓ {result['file']} ← {result['url']}")
            else:
                print(f"  ✗ {result['file']} — {result.get('reason', '?')}")

    # Summary
    print(f"\n{'='*60}")
    print(f"Summary:")
    for status, items in results.items():
        if items:
            print(f"  {status}: {len(items)}")


if __name__ == "__main__":
    main()
