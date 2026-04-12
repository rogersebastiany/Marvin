"""
Tests for web_to_docs_backend.py — locking current behavior as a TDD safety net.

Pure functions (slugify, HTML processing, markdown cleaning) tested directly.
HTTP functions mocked via httpx.
"""

import pytest
from unittest.mock import MagicMock, patch
from bs4 import BeautifulSoup


# ── _slugify ─────────────────────────────────────────────────────────────────


class TestSlugify:
    def _slug(self, text):
        from web_to_docs_backend import _slugify
        return _slugify(text)

    def test_basic(self):
        assert self._slug("Hello World") == "hello-world"

    def test_special_chars_removed(self):
        assert self._slug("Test! @#$% 123") == "test-123"

    def test_max_length_80(self):
        result = self._slug("a" * 200)
        assert len(result) <= 80

    def test_leading_trailing_hyphens_stripped(self):
        result = self._slug("---hello---")
        assert not result.startswith("-")
        assert not result.endswith("-")

    def test_empty_string(self):
        assert self._slug("") == ""

    def test_underscores_become_hyphens(self):
        assert self._slug("foo_bar_baz") == "foo-bar-baz"


# ── _safe_doc_path ───────────────────────────────────────────────────────────


class TestSafeDocPath:
    def test_valid_path(self):
        from web_to_docs_backend import _safe_doc_path
        result = _safe_doc_path("test.md")
        assert result is not None

    def test_traversal_blocked(self):
        from web_to_docs_backend import _safe_doc_path
        result = _safe_doc_path("../../etc/passwd")
        assert result is None


# ── _is_noise_element ────────────────────────────────────────────────────────


class TestIsNoiseElement:
    def _check(self, html):
        from web_to_docs_backend import _is_noise_element
        soup = BeautifulSoup(html, "html.parser")
        return _is_noise_element(soup.find())

    def test_sidebar_class_is_noise(self):
        assert self._check('<div class="sidebar">content</div>') is True

    def test_nav_id_is_noise(self):
        assert self._check('<div id="nav-menu">content</div>') is True

    def test_content_div_not_noise(self):
        assert self._check('<div class="main-content">content</div>') is False

    def test_no_attrs_not_noise(self):
        assert self._check('<div>plain</div>') is False

    def test_toc_class_is_noise(self):
        assert self._check('<div class="table-of-contents">toc</div>') is True


# ── _find_content_container ─────────────────────────────────────────────────���


class TestFindContentContainer:
    def _find(self, html):
        from web_to_docs_backend import _find_content_container
        soup = BeautifulSoup(html, "html.parser")
        return _find_content_container(soup)

    def test_finds_main_tag(self):
        html = "<html><body><main>" + "x" * 300 + "</main></body></html>"
        result = self._find(html)
        assert result.name == "main"

    def test_finds_article_tag(self):
        html = "<html><body><article>" + "x" * 300 + "</article></body></html>"
        result = self._find(html)
        assert result.name == "article"

    def test_falls_back_to_content_class(self):
        html = '<html><body><div class="doc-content">' + "x" * 300 + "</div></body></html>"
        result = self._find(html)
        assert "doc-content" in (result.get("class") or [])

    def test_falls_back_to_body(self):
        html = "<html><body><div>" + "x" * 300 + "</div></body></html>"
        result = self._find(html)
        assert result.name == "body"

    def test_ignores_small_main(self):
        html = "<html><body><main>tiny</main><div>" + "x" * 300 + "</div></body></html>"
        result = self._find(html)
        # main has < 200 chars, so falls back to body
        assert result.name == "body"


# ── _extract_main_content ────────────────────────────────────────────────────


class TestExtractMainContent:
    def _extract(self, html):
        from web_to_docs_backend import _extract_main_content
        return _extract_main_content(html)

    def test_removes_script_tags(self):
        html = "<body><main>" + "x" * 300 + "<script>alert(1)</script></main></body>"
        result = self._extract(html)
        assert "alert" not in result

    def test_removes_style_tags(self):
        html = "<body><main>" + "x" * 300 + "<style>.foo{}</style></main></body>"
        result = self._extract(html)
        assert ".foo" not in result

    def test_preserves_content(self):
        html = "<body><main><p>" + "Real content " * 30 + "</p></main></body>"
        result = self._extract(html)
        assert "Real content" in result


# ── _clean_markdown ──────────────────────────────────────────────────────────


class TestCleanMarkdown:
    def _clean(self, md):
        from web_to_docs_backend import _clean_markdown
        return _clean_markdown(md)

    def test_removes_skip_to_content(self):
        md = "[Skip to content](#main)\nHello"
        result = self._clean(md)
        assert "Skip to content" not in result
        assert "Hello" in result

    def test_removes_search_placeholder(self):
        md = "Search...\nActual content"
        result = self._clean(md)
        assert "Search..." not in result

    def test_removes_empty_links(self):
        md = "Before [](http://example.com) After"
        result = self._clean(md)
        assert "[](" not in result

    def test_collapses_blank_lines(self):
        md = "Line 1\n\n\n\n\nLine 2"
        result = self._clean(md)
        assert "\n\n\n" not in result
        assert "Line 1" in result
        assert "Line 2" in result

    def test_removes_navigation_text(self):
        md = "Navigation\nActual content"
        result = self._clean(md)
        assert result.strip() == "Actual content"


# ── _extract_links ───────────────────────────────────────────────────────────


class TestExtractLinks:
    def _links(self, html, base, prefix):
        from web_to_docs_backend import _extract_links
        return _extract_links(html, base, prefix)

    def test_extracts_matching_links(self):
        html = '<a href="/docs/guide">Guide</a><a href="/other">Other</a>'
        result = self._links(html, "http://example.com/docs/", "http://example.com/docs/")
        assert "http://example.com/docs/guide" in result
        assert "http://example.com/other" not in result

    def test_skips_anchors_and_mailto(self):
        html = '<a href="#section">Anchor</a><a href="mailto:x@x.com">Email</a>'
        result = self._links(html, "http://example.com/", "http://example.com/")
        assert len(result) == 0

    def test_deduplicates(self):
        html = '<a href="/page">A</a><a href="/page">B</a>'
        result = self._links(html, "http://example.com/", "http://example.com/")
        assert len(result) == 1

    def test_strips_fragments(self):
        html = '<a href="/page#section">Link</a>'
        result = self._links(html, "http://example.com/", "http://example.com/")
        assert result[0] == "http://example.com/page"


# ── _extract_title ───────────────────────────────────────────────────────────


class TestExtractTitle:
    def _title(self, md):
        from web_to_docs_backend import _extract_title
        return _extract_title(md)

    def test_extracts_h1(self):
        assert self._title("# Hello World\nContent") == "Hello World"

    def test_no_h1(self):
        assert self._title("No heading here") == ""

    def test_strips_whitespace(self):
        assert self._title("#  Spaced  ") == "Spaced"


# ── _tier2_body ──────────────────────────────────────────────────────────────


class TestTier2Body:
    def _score(self, html, url="http://example.com/docs/guide"):
        from web_to_docs_backend import _tier2_body
        return _tier2_body(url, html)

    def test_good_doc_page(self):
        html = (
            "<html><head><title>API Guide</title>"
            '<meta name="description" content="Complete API reference documentation guide">'
            "</head><body>"
            "<h1>API Guide</h1>" +
            "<p>" + "Paragraph content " * 50 + "</p>" * 5 +
            "<h2>Section 1</h2><p>" + "More content " * 30 + "</p>"
            "<h2>Section 2</h2><pre><code>example code</code></pre>"
            "<h2>Section 3</h2><p>" + "Even more " * 30 + "</p>"
            "</body></html>"
        )
        result = self._score(html)
        assert result["score"] >= 50
        assert "GOOD" in result["verdict"] or "FAIR" in result["verdict"]

    def test_thin_page_low_score(self):
        html = "<html><body><p>Small</p></body></html>"
        result = self._score(html)
        assert result["score"] < 30

    def test_returns_expected_structure(self):
        html = "<html><head><title>Test</title></head><body><p>Content</p></body></html>"
        result = self._score(html)
        assert "url" in result
        assert "score" in result
        assert "verdict" in result
        assert "meta" in result
        assert "body" in result
        assert "title" in result["meta"]


# ── convert_url ──────────────────────────────────────────────────────────────


class TestConvertUrl:
    def test_fetches_and_converts(self):
        from web_to_docs_backend import convert_url
        with patch("web_to_docs_backend._fetch_and_convert", return_value="# Test\nContent"):
            result = convert_url("http://example.com")
            assert "Test" in result


# ── save_as_doc ──────────────────────────────────────────────────────────────


class TestSaveAsDoc:
    def test_adds_md_extension(self, tmp_path):
        from web_to_docs_backend import save_as_doc
        with patch("web_to_docs_backend.DOCS_DIR", tmp_path), \
             patch("web_to_docs_backend._fetch_and_convert", return_value="# Test"):
            result = save_as_doc("http://example.com", "myfile")
            assert "myfile.md" in result
            assert (tmp_path / "myfile.md").exists()

    def test_invalid_filename(self):
        from web_to_docs_backend import save_as_doc
        with patch("web_to_docs_backend._fetch_and_convert", return_value="# Test"), \
             patch("web_to_docs_backend._safe_doc_path", return_value=None):
            result = save_as_doc("http://example.com", "../../evil")
            assert "Invalid" in result


# ── research_topic ───────────────────────────────────────────────────────────


class TestResearchTopic:
    def test_no_urls(self):
        from web_to_docs_backend import research_topic
        assert research_topic([], "Test") == "No URLs provided."

    def test_all_urls_fail(self):
        from web_to_docs_backend import research_topic
        with patch("web_to_docs_backend._fetch_many", return_value=[
            {"url": "http://fail.com", "error": "timeout"}
        ]):
            result = research_topic(["http://fail.com"], "Test")
            assert "All URLs failed" in result

    def test_successful_research(self, tmp_path):
        from web_to_docs_backend import research_topic
        with patch("web_to_docs_backend.DOCS_DIR", tmp_path), \
             patch("web_to_docs_backend._fetch_many", return_value=[
                 {"url": "http://a.com", "md": "# Page A\nContent A " * 30},
                 {"url": "http://b.com", "md": "# Page B\nContent B " * 30},
             ]):
            result = research_topic(["http://a.com", "http://b.com"], "My Topic")
            assert "Research complete" in result
            assert "Sources fetched: 2/2" in result
            # File should be saved
            assert (tmp_path / "my-topic.md").exists()


# ── Constants ────────────────────────────────────────────────────────────────


class TestConstants:
    def test_max_workers(self):
        from web_to_docs_backend import MAX_WORKERS
        assert MAX_WORKERS == 8

    def test_headers_has_user_agent(self):
        from web_to_docs_backend import _HEADERS
        assert "User-Agent" in _HEADERS
        assert "Marvin" in _HEADERS["User-Agent"]

    def test_noise_tags(self):
        from web_to_docs_backend import _NOISE_TAGS
        assert "nav" in _NOISE_TAGS
        assert "script" in _NOISE_TAGS

    def test_content_classes(self):
        from web_to_docs_backend import _CONTENT_CLASSES
        assert "doc-content" in _CONTENT_CLASSES
        assert "markdown-body" in _CONTENT_CLASSES
