"""
Tests for docs_backend.py — locking current behavior as a TDD safety net.

Pure filesystem functions tested with tmp_path. Milvus search path mocked.
"""

import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path


@pytest.fixture
def docs_dir(tmp_path):
    """Create a temporary docs directory with test files."""
    docs = tmp_path / "docs"
    docs.mkdir()

    (docs / "python-basics.md").write_text(
        "# Python Basics\n\nPython is a programming language.\n\n"
        "## Variables\n\nVariables store values.\n\n"
        "## Functions\n\nFunctions encapsulate logic.\n"
    )
    (docs / "neo4j-guide.md").write_text(
        "# Neo4j Guide\n\nNeo4j is a graph database.\n\n"
        "## Cypher\n\nCypher is the query language.\n"
    )

    with patch("backends.docs_backend.DOCS_DIR", docs):
        yield docs


# ── _safe_path ───────────────────────────────────────────────────────────────


class TestSafePath:
    def test_valid_filename(self, docs_dir):
        from backends.docs_backend import _safe_path
        with patch("backends.docs_backend.DOCS_DIR", docs_dir):
            result = _safe_path("python-basics.md")
            assert result is not None
            assert result.name == "python-basics.md"

    def test_path_traversal_blocked(self, docs_dir):
        from backends.docs_backend import _safe_path
        with patch("backends.docs_backend.DOCS_DIR", docs_dir):
            result = _safe_path("../../etc/passwd")
            assert result is None

    def test_nonexistent_file_returns_path(self, docs_dir):
        from backends.docs_backend import _safe_path
        with patch("backends.docs_backend.DOCS_DIR", docs_dir):
            result = _safe_path("nonexistent.md")
            # _safe_path returns the path even if file doesn't exist
            # (caller checks .is_file())
            assert result is not None


# ── search_docs ──────────────────────────────────────────────────────────────


class TestSearchDocs:
    def test_empty_query(self, docs_dir):
        from backends.docs_backend import search_docs
        result = search_docs("")
        assert "non-empty" in result

    def test_whitespace_query(self, docs_dir):
        from backends.docs_backend import search_docs
        result = search_docs("   ")
        assert "non-empty" in result

    def test_milvus_primary_path(self, docs_dir):
        from backends.docs_backend import search_docs
        from backends import memory
        with patch.object(memory, "search_doc_chunks", return_value=[
            {"doc_name": "test", "heading": "Section", "content": "Some content", "score": 0.9}
        ]):
            result = search_docs("test query")
            assert "Found 1 result(s)" in result
            assert "score=0.900" in result

    def test_keyword_fallback_when_milvus_empty(self, docs_dir):
        from backends.docs_backend import search_docs
        from backends import memory
        with patch.object(memory, "search_doc_chunks", return_value=[]):
            result = search_docs("Python")
            assert "keyword fallback" in result
            assert "python-basics.md" in result

    def test_keyword_fallback_when_milvus_down(self, docs_dir):
        from backends.docs_backend import search_docs
        from backends import memory
        with patch.object(memory, "search_doc_chunks", side_effect=Exception("down")):
            result = search_docs("graph database")
            assert "keyword fallback" in result
            assert "neo4j-guide.md" in result

    def test_no_results(self, docs_dir):
        from backends.docs_backend import search_docs
        from backends import memory
        with patch.object(memory, "search_doc_chunks", return_value=[]):
            result = search_docs("zzzznonexistent")
            assert "No results found" in result


# ── list_docs ────────────────────────────────────────────────────────────────


class TestListDocs:
    def test_lists_markdown_files(self, docs_dir):
        from backends.docs_backend import list_docs
        result = list_docs()
        assert isinstance(result, list)
        assert "python-basics.md" in result
        assert "neo4j-guide.md" in result

    def test_sorted(self, docs_dir):
        from backends.docs_backend import list_docs
        result = list_docs()
        assert result == sorted(result)


# ── get_doc_summary ──────────────────────────────────────────────────────────


class TestGetDocSummary:
    def test_returns_first_section(self, docs_dir):
        from backends.docs_backend import get_doc_summary
        result = get_doc_summary("python-basics.md")
        assert "Python Basics" in result
        assert "Variables" in result
        # Should not include the third section
        assert "Functions" not in result

    def test_not_found(self, docs_dir):
        from backends.docs_backend import get_doc_summary
        result = get_doc_summary("nonexistent.md")
        assert "not found" in result

    def test_path_traversal(self, docs_dir):
        from backends.docs_backend import get_doc_summary
        result = get_doc_summary("../../etc/passwd")
        assert "not found" in result


# ── read_doc ─────────────────────────────────────────────────────────────────


class TestReadDoc:
    def test_reads_full_file(self, docs_dir):
        from backends.docs_backend import read_doc
        result = read_doc("python-basics.md")
        assert "Python Basics" in result
        assert "Variables" in result
        assert "Functions" in result

    def test_not_found(self, docs_dir):
        from backends.docs_backend import read_doc
        result = read_doc("missing.md")
        assert "not found" in result

    def test_path_traversal(self, docs_dir):
        from backends.docs_backend import read_doc
        result = read_doc("../../etc/passwd")
        assert "not found" in result
