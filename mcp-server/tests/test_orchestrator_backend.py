"""
Tests for orchestrator_backend.py — locking current behavior as a TDD safety net.

Chain matching and parameter extraction are pure. orchestrate needs mocked Milvus.
"""

import pytest
from unittest.mock import patch, MagicMock


# ── CHAINS constant ──────────────────────────────────────────────────────────


class TestChains:
    def test_all_chains_present(self):
        from backends.orchestrator_backend import CHAINS
        expected = {"tdd_improve", "research", "prompt_lifecycle", "code_to_knowledge",
                    "full_improvement", "sync_and_audit", "densify"}
        assert set(CHAINS.keys()) == expected

    def test_all_chains_have_required_keys(self):
        from backends.orchestrator_backend import CHAINS
        for name, chain in CHAINS.items():
            assert "description" in chain, f"{name} missing description"
            assert "triggers" in chain, f"{name} missing triggers"
            assert "requires" in chain, f"{name} missing requires"
            assert "steps" in chain, f"{name} missing steps"
            assert len(chain["steps"]) > 0, f"{name} has no steps"

    def test_steps_have_ids(self):
        from backends.orchestrator_backend import CHAINS
        for name, chain in CHAINS.items():
            ids = [s["id"] for s in chain["steps"]]
            assert ids == sorted(ids), f"{name} step IDs not sequential"

    def test_tdd_improve_chain_structure(self):
        from backends.orchestrator_backend import CHAINS
        chain = CHAINS["tdd_improve"]
        assert chain["requires"] == ["file_path"]
        assert len(chain["steps"]) == 9
        # First step is score_applicability, last is create_issue, penultimate is scan_owasp
        assert chain["steps"][0]["tool"] == "score_applicability"
        assert chain["steps"][-1]["action"] == "create_issue"
        assert chain["steps"][-2]["tool"] == "scan_owasp"

    def test_full_improvement_chain_structure(self):
        from backends.orchestrator_backend import CHAINS
        chain = CHAINS["full_improvement"]
        assert len(chain["steps"]) == 11
        # Has score_applicability calls (step 1 and step 8)
        score_steps = [s for s in chain["steps"] if s.get("tool") == "score_applicability"]
        assert len(score_steps) == 2
        # Has scan_owasp as penultimate step
        assert chain["steps"][-2]["tool"] == "scan_owasp"


# ── _match_chains ────────────────────────────────────────────────────────────


class TestMatchChains:
    def _match(self, prompt):
        from backends.orchestrator_backend import _match_chains
        return _match_chains(prompt)

    def test_improve_triggers_tdd_improve(self):
        matches = self._match("improve memory.py")
        chain_names = [m["chain"] for m in matches]
        assert "tdd_improve" in chain_names

    def test_research_triggers(self):
        matches = self._match("research Milvus documentation")
        chain_names = [m["chain"] for m in matches]
        assert "research" in chain_names

    def test_prompt_triggers(self):
        matches = self._match("generate prompt for API design")
        chain_names = [m["chain"] for m in matches]
        assert "prompt_lifecycle" in chain_names

    def test_no_match_returns_empty(self):
        matches = self._match("xyzzy foobar nothing matches")
        assert matches == []

    def test_sorted_by_score(self):
        matches = self._match("full improve and tdd test")
        if len(matches) > 1:
            assert matches[0]["score"] >= matches[1]["score"]

    def test_multiple_chains_can_match(self):
        matches = self._match("improve and sync and audit")
        assert len(matches) >= 2

    def test_full_improvement_triggers(self):
        matches = self._match("full improvement cycle")
        chain_names = [m["chain"] for m in matches]
        assert "full_improvement" in chain_names


# ── _extract_file_path ───────────────────────────────────────────────────────


class TestExtractFilePath:
    def _extract(self, prompt):
        from backends.orchestrator_backend import _extract_file_path
        return _extract_file_path(prompt)

    def test_absolute_path(self):
        assert self._extract("improve /home/user/project/memory.py") == "/home/user/project/memory.py"

    def test_relative_path(self):
        assert self._extract("improve memory.py") == "memory.py"

    def test_nested_relative_path(self):
        # The regex captures from the first / it finds
        result = self._extract("improve src/backends/memory.py")
        assert result is not None
        assert result.endswith("memory.py")

    def test_no_path(self):
        assert self._extract("improve the code quality") is None

    def test_various_extensions(self):
        assert self._extract("check file.ts").endswith(".ts")
        assert self._extract("check file.go").endswith(".go")
        assert self._extract("check file.rs").endswith(".rs")

    def test_path_with_spaces(self):
        result = self._extract("improve /home/user/my project/file.py")
        assert result is not None
        assert result.endswith(".py")


# ── orchestrate ──────────────────────────────────────────────────────────────


class TestOrchestrate:
    @pytest.fixture(autouse=True)
    def mock_milvus(self):
        with patch("backends.orchestrator_backend._embed", return_value=[0.0] * 1536), \
             patch("backends.orchestrator_backend._search_by_vector", return_value=[]):
            yield

    def test_no_matching_chain(self):
        from backends.orchestrator_backend import orchestrate
        result = orchestrate("xyzzy foobar nothing matches here")
        assert "error" in result
        assert "available_chains" in result

    def test_matching_chain_returns_plan(self):
        from backends.orchestrator_backend import orchestrate
        result = orchestrate("improve memory.py with test safety")
        assert "chain" in result
        assert "steps" in result
        assert result["chain"] == "tdd_improve"

    def test_extracts_file_path(self):
        from backends.orchestrator_backend import orchestrate
        result = orchestrate("improve /home/user/memory.py")
        assert result["parameters"].get("file_path") == "/home/user/memory.py"

    def test_reports_missing_parameters(self):
        from backends.orchestrator_backend import orchestrate
        result = orchestrate("do some research please")
        # research chain requires urls and topic, neither in prompt
        if result.get("chain") == "research":
            assert len(result["missing_parameters"]) > 0

    def test_includes_milvus_context(self):
        from backends.orchestrator_backend import orchestrate
        result = orchestrate("improve memory.py")
        assert "milvus_context" in result

    def test_includes_alternative_chains(self):
        from backends.orchestrator_backend import orchestrate
        result = orchestrate("improve and tdd test the code")
        assert "alternative_chains" in result

    def test_full_improvement_chain(self):
        from backends.orchestrator_backend import orchestrate
        # Use multiple full_improvement triggers to outscore tdd_improve
        result = orchestrate("full cycle complete improvement on memory.py")
        assert result["chain"] == "full_improvement"
        assert len(result["steps"]) == 11

    def test_milvus_context_with_hits(self):
        from backends.orchestrator_backend import orchestrate
        hit = {"score": 0.8, "name": "Concept", "vault": "test", "summary": "A concept"}
        with patch("backends.orchestrator_backend._search_by_vector", return_value=[hit]):
            result = orchestrate("improve memory.py")
            assert len(result["milvus_context"]) > 0

    def test_milvus_context_filters_low_scores(self):
        from backends.orchestrator_backend import orchestrate
        hit = {"score": 0.1, "name": "Low", "vault": "test", "summary": "Low"}
        with patch("backends.orchestrator_backend._search_by_vector", return_value=[hit]):
            result = orchestrate("improve memory.py")
            assert len(result["milvus_context"]) == 0
