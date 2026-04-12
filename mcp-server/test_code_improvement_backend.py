"""
Tests for code_improvement_backend.py — locking current behavior as a TDD safety net.

AST functions tested directly. improve_code/tdd tested with mocked Milvus.
"""

import pytest
from unittest.mock import patch, MagicMock
import ast
import textwrap


# ── _unparse_annotation ──────────────────────────────────────────────────────


class TestUnparseAnnotation:
    def _unparse(self, node):
        from code_improvement_backend import _unparse_annotation
        return _unparse_annotation(node)

    def test_none_returns_none(self):
        assert self._unparse(None) is None

    def test_simple_name(self):
        tree = ast.parse("x: int")
        ann = tree.body[0].annotation
        assert self._unparse(ann) == "int"

    def test_complex_annotation(self):
        # Parse a subscript like list[str]
        tree = ast.parse("x: list[str] = []")
        ann = tree.body[0].annotation
        result = self._unparse(ann)
        assert result == "list[str]"


# ── _extract_signature ───────────────────────────────────────────────────────


class TestExtractSignature:
    def _sig(self, func_source):
        from code_improvement_backend import _extract_signature
        tree = ast.parse(textwrap.dedent(func_source))
        func = tree.body[0]
        return _extract_signature(func)

    def test_no_args(self):
        sig = self._sig("def foo(): pass")
        assert sig["args"] == []
        assert sig["return_type"] is None
        assert sig["is_async"] is False
        assert sig["decorators"] == []

    def test_args_with_annotations(self):
        sig = self._sig("def foo(x: int, y: str) -> bool: pass")
        assert len(sig["args"]) == 2
        assert sig["args"][0]["name"] == "x"
        assert sig["args"][0]["annotation"] == "int"
        assert sig["return_type"] == "bool"

    def test_default_values(self):
        sig = self._sig("def foo(x: int = 5, y: str = 'hello'): pass")
        assert sig["args"][0]["default"] == "5"
        assert sig["args"][1]["default"] == "'hello'"

    def test_async_function(self):
        sig = self._sig("async def foo(): pass")
        assert sig["is_async"] is True

    def test_decorators(self):
        sig = self._sig("@property\ndef foo(self): pass")
        assert "property" in sig["decorators"]


# ── _extract_class_methods ───────────────────────────────────────────────────


class TestExtractClassMethods:
    def test_extracts_methods(self):
        from code_improvement_backend import _extract_class_methods
        source = textwrap.dedent("""\
        class Foo:
            def bar(self):
                '''Bar method.'''
                pass
            def baz(self, x: int) -> str:
                pass
        """)
        tree = ast.parse(source)
        cls = tree.body[0]
        lines = source.splitlines(keepends=True)
        methods = _extract_class_methods(cls, lines)
        assert len(methods) == 2
        assert methods[0]["name"] == "bar"
        assert methods[0]["docstring"] == "Bar method."
        assert methods[1]["name"] == "baz"

    def test_no_methods(self):
        from code_improvement_backend import _extract_class_methods
        source = "class Empty:\n    x = 1\n"
        tree = ast.parse(source)
        cls = tree.body[0]
        lines = source.splitlines(keepends=True)
        methods = _extract_class_methods(cls, lines)
        assert methods == []


# ── _chunk_code_by_ast ───────────────────────────────────────────────────────


class TestChunkCodeByAst:
    def _chunk(self, source, path="test.py"):
        from code_improvement_backend import _chunk_code_by_ast
        return _chunk_code_by_ast(source, path)

    def test_non_python_returns_whole_file(self):
        chunks = self._chunk("some content", "file.js")
        assert len(chunks) == 1
        assert chunks[0]["kind"] == "file"

    def test_syntax_error_returns_whole_file(self):
        chunks = self._chunk("def broken(:\n  pass", "bad.py")
        assert len(chunks) == 1
        assert chunks[0]["kind"] == "file"

    def test_functions_and_classes(self):
        source = textwrap.dedent("""\
        def foo():
            pass

        class Bar:
            def method(self):
                pass

        def baz():
            pass
        """)
        chunks = self._chunk(source)
        assert len(chunks) == 3
        assert chunks[0]["name"] == "foo"
        assert chunks[0]["kind"] == "function"
        assert chunks[1]["name"] == "Bar"
        assert chunks[1]["kind"] == "class"
        assert chunks[2]["name"] == "baz"

    def test_includes_docstring(self):
        source = 'def foo():\n    """Docstring."""\n    pass\n'
        chunks = self._chunk(source)
        assert chunks[0]["docstring"] == "Docstring."

    def test_function_has_signature(self):
        source = "def foo(x: int) -> str:\n    pass\n"
        chunks = self._chunk(source)
        assert "signature" in chunks[0]
        assert chunks[0]["signature"]["return_type"] == "str"

    def test_class_has_methods(self):
        source = textwrap.dedent("""\
        class Foo:
            def bar(self):
                pass
        """)
        chunks = self._chunk(source)
        assert "methods" in chunks[0]
        assert len(chunks[0]["methods"]) == 1

    def test_no_functions_returns_whole_file(self):
        source = "x = 1\ny = 2\n"
        chunks = self._chunk(source)
        assert len(chunks) == 1
        assert chunks[0]["kind"] == "file"


# ── _extract_imports ─────────────────────────────────────────────────────────


class TestExtractImports:
    def _imports(self, source):
        from code_improvement_backend import _extract_imports
        return _extract_imports(source)

    def test_import_and_from(self):
        source = "import os\nfrom pathlib import Path\n"
        result = self._imports(source)
        assert "import os" in result
        assert "from pathlib import Path" in result

    def test_no_imports(self):
        assert self._imports("x = 1") == []

    def test_syntax_error(self):
        assert self._imports("def broken(:") == []


# ── improve_code ─────────────────────────────────────────────────────────────


class TestImproveCode:
    def test_file_not_found(self):
        from code_improvement_backend import improve_code
        with patch("code_improvement_backend._embed_batch"):
            result = improve_code("/nonexistent/file.py")
            assert "error" in result

    def test_empty_file(self, tmp_path):
        from code_improvement_backend import improve_code
        f = tmp_path / "empty.py"
        f.write_text("")
        with patch("code_improvement_backend._embed_batch"):
            result = improve_code(str(f))
            assert "error" in result

    def test_returns_expected_structure(self, tmp_path):
        from code_improvement_backend import improve_code
        f = tmp_path / "sample.py"
        f.write_text("def foo():\n    pass\n")

        with patch("code_improvement_backend._embed_batch", return_value=[[0.0] * 1536]), \
             patch("code_improvement_backend._search_by_vector", return_value=[]):
            result = improve_code(str(f))
            assert "file" in result
            assert "chunks" in result
            assert "total_matches" in result
            assert "unique_sources" in result
            assert len(result["chunks"]) == 1
            assert result["chunks"][0]["name"] == "foo"

    def test_filters_by_score_threshold(self, tmp_path):
        from code_improvement_backend import improve_code
        f = tmp_path / "sample.py"
        f.write_text("def foo():\n    pass\n")

        low_hit = {"score": 0.1, "name": "low", "vault": "test", "summary": "low"}
        high_hit = {"score": 0.9, "name": "high", "vault": "test", "summary": "high"}

        with patch("code_improvement_backend._embed_batch", return_value=[[0.0] * 1536]), \
             patch("code_improvement_backend._search_by_vector", return_value=[low_hit, high_hit]):
            result = improve_code(str(f), score_threshold=0.5)
            # Only high_hit should pass
            matches = result["chunks"][0]["matches"]
            assert all(m["score"] >= 0.5 for m in matches)


# ── tdd ──────────────────────────────────────────────────────────────────────


class TestTdd:
    def test_file_not_found(self):
        from code_improvement_backend import tdd
        with patch("code_improvement_backend._embed_batch"):
            result = tdd("/nonexistent/file.py")
            assert "error" in result

    def test_returns_expected_structure(self, tmp_path):
        from code_improvement_backend import tdd
        f = tmp_path / "sample.py"
        f.write_text("import os\n\ndef foo(x: int) -> str:\n    '''Do stuff.'''\n    pass\n")

        with patch("code_improvement_backend._embed_batch", return_value=[[0.0] * 1536]), \
             patch("code_improvement_backend._search_by_vector", return_value=[]):
            result = tdd(str(f))
            assert result["module_name"] == "sample"
            assert "import os" in result["imports"]
            assert len(result["testable_units"]) == 1
            unit = result["testable_units"][0]
            assert unit["name"] == "foo"
            assert unit["docstring"] == "Do stuff."
            assert unit["signature"]["return_type"] == "str"
            assert "knowledge" in unit

    def test_k_per_collection_clamped(self, tmp_path):
        from code_improvement_backend import tdd
        f = tmp_path / "sample.py"
        f.write_text("def foo(): pass\n")

        with patch("code_improvement_backend._embed_batch", return_value=[[0.0] * 1536]), \
             patch("code_improvement_backend._search_by_vector", return_value=[]) as mock_search:
            tdd(str(f), k_per_collection=50)
            for call in mock_search.call_args_list:
                assert call[0][2] <= 20  # limit arg
