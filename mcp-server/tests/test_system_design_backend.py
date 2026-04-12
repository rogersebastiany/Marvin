"""
Tests for system_design_backend.py — locking current behavior as a TDD safety net.

Filesystem functions tested with tmp_path. String formatters tested directly.
"""

import pytest
from unittest.mock import patch
from pathlib import Path


# ── _safe_diagram_path ───────────────────────────────────────────────────────


class TestSafeDiagramPath:
    def test_valid_path(self):
        from backends.system_design_backend import _safe_diagram_path
        result = _safe_diagram_path("test.mmd")
        assert result is not None

    def test_traversal_blocked(self):
        from backends.system_design_backend import _safe_diagram_path
        result = _safe_diagram_path("../../etc/passwd")
        assert result is None


# ── generate_diagram ─────────────────────────────────────────────────────────


class TestGenerateDiagram:
    def test_includes_description(self):
        from backends.system_design_backend import generate_diagram
        result = generate_diagram("A microservices system")
        assert "A microservices system" in result

    def test_includes_guidelines(self):
        from backends.system_design_backend import generate_diagram
        result = generate_diagram("System")
        assert "Diagram Type Selection" in result
        assert "Best Practices" in result

    def test_auto_type_no_forced_keyword(self):
        from backends.system_design_backend import generate_diagram
        result = generate_diagram("System", diagram_type="auto")
        assert "You MUST use" not in result

    def test_specific_type_forces_keyword(self):
        from backends.system_design_backend import generate_diagram
        result = generate_diagram("System", diagram_type="c4context")
        assert "You MUST use `C4Context`" in result

    def test_sequence_type(self):
        from backends.system_design_backend import generate_diagram
        result = generate_diagram("System", diagram_type="sequence")
        assert "sequenceDiagram" in result

    def test_save_as_instruction(self):
        from backends.system_design_backend import generate_diagram
        result = generate_diagram("System", save_as="my-diagram.mmd")
        assert "save_diagram" in result
        assert "my-diagram.mmd" in result

    def test_unknown_type_passes_through(self):
        from backends.system_design_backend import generate_diagram
        result = generate_diagram("System", diagram_type="gantt")
        assert "gantt" in result


# ── judge_diagram ────────────────────────────────────────────────────────────


class TestJudgeDiagram:
    def test_includes_code(self):
        from backends.system_design_backend import judge_diagram
        result = judge_diagram("graph TD\n  A-->B")
        assert "graph TD" in result
        assert "A-->B" in result

    def test_includes_review_criteria(self):
        from backends.system_design_backend import judge_diagram
        result = judge_diagram("graph TD")
        assert "Syntax Correctness" in result
        assert "Completeness" in result
        assert "Clarity" in result
        assert "Best Practices" in result

    def test_includes_mermaid_block(self):
        from backends.system_design_backend import judge_diagram
        result = judge_diagram("graph TD")
        assert "```mermaid" in result


# ── save_diagram ─────────────────────────────────────────────────────────────


class TestSaveDiagram:
    def test_saves_to_file(self, tmp_path):
        from backends.system_design_backend import save_diagram
        with patch("backends.system_design_backend.DIAGRAMS_DIR", tmp_path):
            result = save_diagram("graph TD\n  A-->B", "test")
            assert "test.mmd" in result
            assert (tmp_path / "test.mmd").exists()
            assert (tmp_path / "test.mmd").read_text() == "graph TD\n  A-->B"

    def test_adds_extension(self, tmp_path):
        from backends.system_design_backend import save_diagram
        with patch("backends.system_design_backend.DIAGRAMS_DIR", tmp_path):
            result = save_diagram("code", "mydiag")
            assert "mydiag.mmd" in result

    def test_keeps_extension(self, tmp_path):
        from backends.system_design_backend import save_diagram
        with patch("backends.system_design_backend.DIAGRAMS_DIR", tmp_path):
            result = save_diagram("code", "mydiag.mmd")
            assert "mydiag.mmd" in result

    def test_invalid_path(self):
        from backends.system_design_backend import save_diagram
        with patch("backends.system_design_backend._safe_diagram_path", return_value=None):
            result = save_diagram("code", "../../evil")
            assert "Invalid" in result


# ── list_diagrams ────────────────────────────────────────────────────────────


class TestListDiagrams:
    def test_lists_mmd_files(self, tmp_path):
        (tmp_path / "a.mmd").write_text("graph")
        (tmp_path / "b.mmd").write_text("graph")
        (tmp_path / "c.txt").write_text("not a diagram")
        with patch("backends.system_design_backend.DIAGRAMS_DIR", tmp_path):
            from backends.system_design_backend import list_diagrams
            result = list_diagrams()
            assert "a.mmd" in result
            assert "b.mmd" in result
            assert "c.txt" not in result

    def test_sorted(self, tmp_path):
        (tmp_path / "z.mmd").write_text("g")
        (tmp_path / "a.mmd").write_text("g")
        with patch("backends.system_design_backend.DIAGRAMS_DIR", tmp_path):
            from backends.system_design_backend import list_diagrams
            result = list_diagrams()
            assert result == sorted(result)


# ── get_diagram ──────────────────────────────────────────────────────────────


class TestGetDiagram:
    def test_reads_file(self, tmp_path):
        (tmp_path / "test.mmd").write_text("graph TD\n  A-->B")
        with patch("backends.system_design_backend.DIAGRAMS_DIR", tmp_path):
            from backends.system_design_backend import get_diagram
            result = get_diagram("test.mmd")
            assert "graph TD" in result

    def test_not_found(self, tmp_path):
        with patch("backends.system_design_backend.DIAGRAMS_DIR", tmp_path):
            from backends.system_design_backend import get_diagram
            result = get_diagram("missing.mmd")
            assert "not found" in result

    def test_traversal_blocked(self):
        from backends.system_design_backend import get_diagram
        with patch("backends.system_design_backend._safe_diagram_path", return_value=None):
            result = get_diagram("../../etc/passwd")
            assert "not found" in result


# ── Constants ────────────────────────────────────────────────────────────────


class TestConstants:
    def test_diagram_guidelines_has_types(self):
        from backends.system_design_backend import DIAGRAM_GUIDELINES
        assert "C4Context" in DIAGRAM_GUIDELINES
        assert "Flowchart" in DIAGRAM_GUIDELINES
        assert "Sequence Diagram" in DIAGRAM_GUIDELINES

    def test_type_map_in_generate(self):
        from backends.system_design_backend import generate_diagram
        types = ["c4context", "c4container", "c4component", "flowchart", "sequence", "architecture"]
        for t in types:
            result = generate_diagram("Test", diagram_type=t)
            assert "You MUST use" in result
