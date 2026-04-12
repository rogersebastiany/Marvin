"""
Tests for ops_backend.py — locking current behavior as a TDD safety net.

Pure functions (compute_diff, _count_drift, _is_mcp_tool_decorator, _extract_set_or_list)
tested directly. extract_code_structure tested with real source files.
sync/audit/self_improve tested with mocked externals.
"""

import ast
import json
import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path


# ── _get_lancedb_path ───────────────────────────────────────────────────────


class TestGetLancedbPath:
    def test_returns_none_when_path_missing(self):
        from backends.ops_backend import _get_lancedb_path
        with patch("os.getenv", return_value="/nonexistent/lancedb"):
            result = _get_lancedb_path()
            assert result is None

    def test_returns_path_when_exists(self, tmp_path):
        from backends.ops_backend import _get_lancedb_path
        lance_dir = tmp_path / "test.lancedb"
        lance_dir.mkdir()
        with patch("os.getenv", return_value=str(lance_dir)):
            result = _get_lancedb_path()
            assert result == str(lance_dir)

    def test_relative_path_joined_to_repo_root(self, tmp_path):
        from backends.ops_backend import _get_lancedb_path
        with patch("os.getenv", return_value="data/cognee.lancedb"), \
             patch("backends.ops_backend.REPO_ROOT", tmp_path):
            (tmp_path / "data" / "cognee.lancedb").mkdir(parents=True)
            result = _get_lancedb_path()
            assert result == str(tmp_path / "data" / "cognee.lancedb")


# ── _is_mcp_tool_decorator ─────────────────────────────────────────────────


class TestIsMcpToolDecorator:
    def _check(self, decorator_source):
        from backends.ops_backend import _is_mcp_tool_decorator
        tree = ast.parse(f"@{decorator_source}\ndef f(): pass")
        return _is_mcp_tool_decorator(tree.body[0].decorator_list[0])

    def test_simple_mcp_tool(self):
        assert self._check("mcp.tool()") is True

    def test_mcp_tool_no_call(self):
        assert self._check("mcp.tool") is True

    def test_other_decorator(self):
        assert self._check("pytest.fixture()") is False

    def test_property_decorator(self):
        from backends.ops_backend import _is_mcp_tool_decorator
        tree = ast.parse("@property\ndef f(): pass")
        assert _is_mcp_tool_decorator(tree.body[0].decorator_list[0]) is False


# ── _extract_set_or_list ────────────────────────────────────────────────────


class TestExtractSetOrList:
    def _extract(self, source):
        from backends.ops_backend import _extract_set_or_list
        tree = ast.parse(f"x = {source}")
        return _extract_set_or_list(tree.body[0].value)

    def test_list_of_strings(self):
        result = self._extract('["b", "a", "c"]')
        assert result == ["a", "b", "c"]

    def test_set_of_strings(self):
        result = self._extract('{"z", "a"}')
        assert result == ["a", "z"]

    def test_empty_list(self):
        assert self._extract("[]") == []

    def test_non_string_elements_ignored(self):
        result = self._extract('[1, "a", 2]')
        assert result == ["a"]

    def test_set_call_wrapper(self):
        # set(["a", "b"]) — Call wrapping a List
        result = self._extract('set(["b", "a"])')
        assert result == ["a", "b"]


# ── compute_diff ────────────────────────────────────────────────────────────


class TestComputeDiff:
    def _diff(self, code=None, kg=None):
        from backends.ops_backend import compute_diff
        if code is None:
            code = {
                "tools": ["retrieve", "expand"],
                "constants": {
                    "MARVIN_TOOLS": ["retrieve", "expand"],
                    "MILVUS_TOOLS": ["retrieve"],
                    "OVERVIEW_TOOLS": [],
                    "NEO4J_READ_TOOLS": [],
                    "WRITE_TOOLS": ["expand"],
                },
                "backends": {},
                "middleware": [],
                "imports": {},
            }
        if kg is None:
            kg = {
                "marvin_concept": {"content": "Exposes 2 tools."},
                "marvin_relations": [
                    {"rel_type": "REQUIRES", "target": "Neo4j"},
                    {"rel_type": "REQUIRES", "target": "Milvus"},
                ],
                "relation_types_in_kg": [("REQUIRES", 10), ("RELATES_TO", 5)],
                "total_concepts": 100,
                "total_relations": 200,
            }
        return compute_diff(code, kg)

    def test_no_drift(self):
        diff = self._diff()
        assert diff["tool_count_mismatch"] is None
        assert diff["canonical_list_drift"] is None

    def test_tool_count_mismatch(self):
        kg = {
            "marvin_concept": {"content": "Exposes 99 tools."},
            "marvin_relations": [],
            "relation_types_in_kg": [],
            "total_concepts": 0,
            "total_relations": 0,
        }
        diff = self._diff(kg=kg)
        assert diff["tool_count_mismatch"] is not None
        assert diff["tool_count_mismatch"]["kg_claims"] == 99
        assert diff["tool_count_mismatch"]["code_has"] == 2

    def test_canonical_list_drift(self):
        code = {
            "tools": ["retrieve", "expand"],
            "constants": {
                "MARVIN_TOOLS": ["retrieve", "expand", "ghost_tool"],
                "MILVUS_TOOLS": ["retrieve"],
                "OVERVIEW_TOOLS": [],
                "NEO4J_READ_TOOLS": [],
                "WRITE_TOOLS": ["expand"],
            },
            "backends": {},
            "middleware": [],
            "imports": {},
        }
        diff = self._diff(code=code)
        assert diff["canonical_list_drift"] is not None
        assert "ghost_tool" in diff["canonical_list_drift"]["in_list_not_decorated"]

    def test_concept_gaps(self):
        kg = {
            "marvin_concept": {"content": ""},
            "marvin_relations": [],  # No relations at all
            "relation_types_in_kg": [],
            "total_concepts": 0,
            "total_relations": 0,
        }
        diff = self._diff(kg=kg)
        assert len(diff["concept_gaps"]) > 0
        expected_concepts = {"Neo4j", "Milvus", "docs-server", "web-to-docs",
                             "prompt-engineer", "system-design"}
        gap_concepts = {g["expected_concept"] for g in diff["concept_gaps"]}
        assert gap_concepts == expected_concepts

    def test_middleware_gaps(self):
        code = {
            "tools": ["retrieve", "expand", "unclassified_tool"],
            "constants": {
                "MARVIN_TOOLS": ["retrieve", "expand", "unclassified_tool"],
                "MILVUS_TOOLS": ["retrieve"],
                "OVERVIEW_TOOLS": [],
                "NEO4J_READ_TOOLS": [],
                "WRITE_TOOLS": ["expand"],
            },
            "backends": {},
            "middleware": [],
            "imports": {},
        }
        diff = self._diff(code=code)
        assert "unclassified_tool" in diff["middleware_gaps"]

    def test_no_marvin_concept(self):
        kg = {
            "marvin_concept": None,
            "marvin_relations": [],
            "relation_types_in_kg": [],
            "total_concepts": 0,
            "total_relations": 0,
        }
        diff = self._diff(kg=kg)
        assert diff["tool_count_mismatch"] is None


# ── _count_drift ────────────────────────────────────────────────────────────


class TestCountDrift:
    def test_zero_drift(self):
        from backends.ops_backend import _count_drift
        diff = {
            "tool_count_mismatch": None,
            "canonical_list_drift": None,
            "relation_type_drift": None,
            "concept_gaps": [],
            "middleware_gaps": [],
        }
        assert _count_drift(diff) == 0

    def test_counts_tool_mismatch(self):
        from backends.ops_backend import _count_drift
        diff = {
            "tool_count_mismatch": {"kg_claims": 10, "code_has": 8},
            "canonical_list_drift": None,
            "relation_type_drift": None,
            "concept_gaps": [],
        }
        assert _count_drift(diff) == 1

    def test_counts_canonical_drift(self):
        from backends.ops_backend import _count_drift
        diff = {
            "tool_count_mismatch": None,
            "canonical_list_drift": {
                "in_list_not_decorated": ["a", "b"],
                "decorated_not_in_list": ["c"],
            },
            "relation_type_drift": None,
            "concept_gaps": [],
        }
        assert _count_drift(diff) == 3

    def test_counts_concept_gaps(self):
        from backends.ops_backend import _count_drift
        diff = {
            "tool_count_mismatch": None,
            "canonical_list_drift": None,
            "relation_type_drift": None,
            "concept_gaps": [{"module": "a"}, {"module": "b"}],
        }
        assert _count_drift(diff) == 2

    def test_counts_relation_type_drift(self):
        from backends.ops_backend import _count_drift
        diff = {
            "tool_count_mismatch": None,
            "canonical_list_drift": None,
            "relation_type_drift": {
                "defined_not_used": ["X"],
                "used_not_defined": ["Y", "Z"],
            },
            "concept_gaps": [],
        }
        assert _count_drift(diff) == 3

    def test_combined(self):
        from backends.ops_backend import _count_drift
        diff = {
            "tool_count_mismatch": {"kg_claims": 10, "code_has": 8},
            "canonical_list_drift": {
                "in_list_not_decorated": ["a"],
                "decorated_not_in_list": [],
            },
            "relation_type_drift": {
                "defined_not_used": ["X"],
                "used_not_defined": [],
            },
            "concept_gaps": [{"module": "x"}],
        }
        assert _count_drift(diff) == 4  # 1 + 1 + 1 + 1


# ── extract_code_structure ──────────────────────────────────────────────────


class TestExtractCodeStructure:
    def test_returns_expected_keys(self):
        from backends.ops_backend import extract_code_structure
        result = extract_code_structure()
        assert "tools" in result
        assert "backends" in result
        assert "constants" in result
        assert "middleware" in result
        assert "imports" in result

    def test_finds_tools_in_marvin_server(self):
        from backends.ops_backend import extract_code_structure
        result = extract_code_structure()
        assert len(result["tools"]) > 0

    def test_finds_backends(self):
        from backends.ops_backend import extract_code_structure
        result = extract_code_structure()
        assert "ontology" in result["backends"]
        assert "memory" in result["backends"]
        assert "ops_backend" in result["backends"]

    def test_finds_marvin_tools_constant(self):
        from backends.ops_backend import extract_code_structure
        result = extract_code_structure()
        assert "MARVIN_TOOLS" in result["constants"]
        assert len(result["constants"]["MARVIN_TOOLS"]) > 0

    def test_finds_imports(self):
        from backends.ops_backend import extract_code_structure
        result = extract_code_structure()
        assert "ops_backend" in result["imports"]


# ── Constants ───────────────────────────────────────────────────────────────


class TestConstants:
    def test_source_files(self):
        from backends.ops_backend import SOURCE_FILES
        assert "marvin_server.py" in SOURCE_FILES
        assert "backends/ops_backend.py" in SOURCE_FILES
        assert len(SOURCE_FILES) == 10

    def test_backend_concept_map(self):
        from backends.ops_backend import BACKEND_CONCEPT_MAP
        assert "ontology" in BACKEND_CONCEPT_MAP
        assert "memory" in BACKEND_CONCEPT_MAP
        assert BACKEND_CONCEPT_MAP["ontology"] == ("Neo4j", "REQUIRES")
        assert BACKEND_CONCEPT_MAP["memory"] == ("Milvus", "REQUIRES")

    def test_repo_root_and_mcp_server(self):
        from backends.ops_backend import REPO_ROOT, MCP_SERVER
        assert REPO_ROOT.exists()
        assert MCP_SERVER.exists()
        assert (MCP_SERVER / "backends" / "ops_backend.py").exists()


# ── sync ────────────────────────────────────────────────────────────────────


class TestSync:
    def test_skip_cognify(self):
        from backends.ops_backend import sync
        from backends import memory
        with patch.object(memory, "ensure_collections"), \
             patch("backends.ops_backend._sync_lance_concepts_to_milvus", return_value=10), \
             patch("backends.ops_backend._sync_lance_doc_chunks_to_milvus", return_value=20):
            result = sync(skip_cognify=True)
            assert result["cognify_mode"] == "skipped"
            assert result["concepts"] == 10
            assert result["doc_chunks"] == 20
            assert "elapsed_s" in result

    def test_empty_changed_files(self):
        from backends.ops_backend import sync
        from backends import memory
        with patch.object(memory, "ensure_collections"), \
             patch("backends.ops_backend._sync_lance_concepts_to_milvus", return_value=5), \
             patch("backends.ops_backend._sync_lance_doc_chunks_to_milvus", return_value=3):
            result = sync(changed_files=[])
            assert result["cognify_mode"] == "skipped (no changed files)"

    def test_incremental_cognify(self):
        from backends.ops_backend import sync
        from backends import memory
        mock_cognify = MagicMock()
        with patch.object(memory, "ensure_collections"), \
             patch.dict("sys.modules", {"cognify_vaults": mock_cognify}), \
             patch("backends.ops_backend._sync_lance_concepts_to_milvus", return_value=5), \
             patch("backends.ops_backend._sync_lance_doc_chunks_to_milvus", return_value=3), \
             patch("asyncio.run"):
            result = sync(changed_files=["a.md", "b.md"])
            assert "incremental (2 files)" in result["cognify_mode"]


# ── audit ───────────────────────────────────────────────────────────────────


class TestAudit:
    def test_returns_expected_structure(self):
        from backends.ops_backend import audit
        mock_kg = {
            "marvin_concept": {"content": ""},
            "marvin_relations": [],
            "relation_types_in_kg": [],
            "total_concepts": 100,
            "total_relations": 200,
        }
        with patch("backends.ops_backend.extract_kg_claims", return_value=mock_kg):
            result = audit()
            assert "drift_points" in result
            assert "findings" in result
            assert "code_summary" in result
            assert "kg_summary" in result
            assert "elapsed_s" in result
            assert isinstance(result["drift_points"], int)
            assert isinstance(result["findings"], list)


# ── self_improve ────────────────────────────────────────────────────────────


class TestSelfImprove:
    def test_no_drift_returns_early(self):
        from backends.ops_backend import self_improve
        mock_code = {
            "tools": ["retrieve", "expand"],
            "constants": {
                "MARVIN_TOOLS": ["retrieve", "expand"],
                "MILVUS_TOOLS": ["retrieve"],
                "OVERVIEW_TOOLS": [],
                "NEO4J_READ_TOOLS": [],
                "WRITE_TOOLS": ["expand"],
            },
            "backends": {},
            "middleware": [],
            "imports": {},
        }
        # Include all relation types from relation_types.json so no drift
        mock_kg = {
            "marvin_concept": {"content": "Exposes 2 tools."},
            "marvin_relations": [
                {"rel_type": "REQUIRES", "target": "Neo4j"},
                {"rel_type": "REQUIRES", "target": "Milvus"},
                {"rel_type": "COMPOSES", "target": "docs-server"},
                {"rel_type": "COMPOSES", "target": "web-to-docs"},
                {"rel_type": "COMPOSES", "target": "prompt-engineer"},
                {"rel_type": "COMPOSES", "target": "system-design"},
            ],
            "relation_types_in_kg": [
                ("RELATES_TO", 1), ("IMPLEMENTS", 1), ("PROVES", 1),
                ("REQUIRES", 1), ("EXTENDS", 1), ("CONTRADICTS", 1),
                ("ENABLES", 1), ("EXEMPLIFIES", 1), ("COMPOSES", 1),
                ("EVOLVES_FROM", 1), ("INFERS", 1), ("FORMALIZES", 1),
                ("DEFINES", 1), ("ANALOGOUS_TO", 1), ("REDUCES", 1),
                ("MITIGATES", 1),
            ],
            "total_concepts": 100,
            "total_relations": 200,
        }
        from backends import ontology, memory
        with patch("backends.ops_backend.extract_code_structure", return_value=mock_code), \
             patch("backends.ops_backend.extract_kg_claims", return_value=mock_kg), \
             patch.object(ontology, "expand"), \
             patch.object(memory, "log_decision"):
            result = self_improve()
            assert result["drift_before"] == 0
            assert result["fixes"] == 0
            assert "No drift" in result["actions"]

    def test_fixes_concept_gaps(self):
        from backends.ops_backend import self_improve
        from backends import ontology, memory
        mock_kg = {
            "marvin_concept": {"content": ""},
            "marvin_relations": [],  # no relations → all gaps
            "relation_types_in_kg": [],
            "total_concepts": 100,
            "total_relations": 200,
        }
        with patch("backends.ops_backend.extract_kg_claims", return_value=mock_kg), \
             patch.object(ontology, "expand") as mock_expand, \
             patch.object(memory, "log_decision"), \
             patch("backends.ops_backend._sync_lance_concepts_to_milvus", return_value=0):
            result = self_improve()
            assert result["drift_before"] > 0
            assert result["fixes"] > 0
            assert mock_expand.called
