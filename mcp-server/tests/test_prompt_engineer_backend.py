"""
Tests for prompt_engineer_backend.py — locking current behavior as a TDD safety net.

All functions are pure string formatters — no mocking needed.
"""

import pytest


class TestSystemPrompt:
    def test_has_required_sections(self):
        from backends.prompt_engineer_backend import SYSTEM_PROMPT
        assert "ROLE & PERSPECTIVES" in SYSTEM_PROMPT
        assert "KNOWLEDGE BEYOND WEIGHTS" in SYSTEM_PROMPT
        assert "GOLDEN PATTERNS" in SYSTEM_PROMPT
        assert "EXECUTION PIPELINE" in SYSTEM_PROMPT
        assert "ATTENTION MASK" in SYSTEM_PROMPT
        assert "FINAL TASK" in SYSTEM_PROMPT

    def test_references_transformer_principles(self):
        from backends.prompt_engineer_backend import SYSTEM_PROMPT
        assert "Constant Path Length" in SYSTEM_PROMPT
        assert "Multi-Head Attention" in SYSTEM_PROMPT
        assert "Attention Masking" in SYSTEM_PROMPT


class TestBuildToolCatalog:
    def test_empty_list(self):
        from backends.prompt_engineer_backend import _build_tool_catalog
        assert _build_tool_catalog([]) == "(no tools available)"

    def test_formats_tools(self):
        from backends.prompt_engineer_backend import _build_tool_catalog
        result = _build_tool_catalog(["retrieve", "get_concept"])
        assert "- `retrieve`" in result
        assert "- `get_concept`" in result


class TestGeneratePrompt:
    def test_includes_task_and_domain(self):
        from backends.prompt_engineer_backend import generate_prompt
        result = generate_prompt("Build an API", domain="backend")
        assert "Build an API" in result
        assert "backend" in result

    def test_includes_system_prompt(self):
        from backends.prompt_engineer_backend import generate_prompt
        result = generate_prompt("Test task")
        assert "Transformer-Driven Prompt Architect" in result

    def test_includes_tool_catalog(self):
        from backends.prompt_engineer_backend import generate_prompt
        result = generate_prompt("Task", tool_catalog="- `retrieve`\n- `expand`")
        assert "retrieve" in result
        assert "expand" in result

    def test_default_domain(self):
        from backends.prompt_engineer_backend import generate_prompt
        result = generate_prompt("Task")
        assert "general" in result


class TestRefinePrompt:
    def test_includes_original_and_feedback(self):
        from backends.prompt_engineer_backend import refine_prompt
        result = refine_prompt("Original prompt", "Needs more examples")
        assert "Original prompt" in result
        assert "Needs more examples" in result

    def test_includes_system_prompt(self):
        from backends.prompt_engineer_backend import refine_prompt
        result = refine_prompt("Prompt", "Feedback")
        assert "Transformer-Driven Prompt Architect" in result

    def test_includes_tool_catalog(self):
        from backends.prompt_engineer_backend import refine_prompt
        result = refine_prompt("Prompt", "Feedback", tool_catalog="- `tdd`")
        assert "tdd" in result


class TestAuditPrompt:
    def test_includes_prompt_to_audit(self):
        from backends.prompt_engineer_backend import audit_prompt
        result = audit_prompt("My prompt to audit")
        assert "My prompt to audit" in result

    def test_includes_scoring_instructions(self):
        from backends.prompt_engineer_backend import audit_prompt
        result = audit_prompt("Prompt")
        assert "PRESENT / MISSING / WEAK" in result
        assert "score (1-10)" in result

    def test_includes_output_format(self):
        from backends.prompt_engineer_backend import audit_prompt
        result = audit_prompt("Prompt")
        assert "AUDIT REPORT" in result
        assert "SCORE" in result
        assert "REWRITTEN PROMPT" in result
