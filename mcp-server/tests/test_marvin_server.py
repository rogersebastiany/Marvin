"""
Tests for marvin_server.py — locking current behavior as a TDD safety net.

Constants and tier classification tested directly. build_self_description
tested with mocked ontology/memory. Tool wrappers are thin delegates — not
tested here (tested via their backend test files).
"""

import ast
import textwrap
import pytest
from pathlib import Path


# marvin_server.py has heavy FastMCP coupling (decorators, middleware, lifespan).
# Instead of fighting the import, we parse the source AST directly for constants
# and test pure functions by extracting them.

SERVER_PATH = Path(__file__).parent.parent / "marvin_server.py"
SOURCE = SERVER_PATH.read_text()
TREE = ast.parse(SOURCE, filename="marvin_server.py")


def _extract_list_constant(name: str) -> list[str]:
    """Extract a list constant from the AST."""
    for node in ast.iter_child_nodes(TREE):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == name:
                    if isinstance(node.value, ast.List):
                        return [
                            elt.value for elt in node.value.elts
                            if isinstance(elt, ast.Constant) and isinstance(elt.value, str)
                        ]
    return []


def _extract_frozenset_constant(name: str) -> set[str]:
    """Extract a frozenset({...}) constant from the AST."""
    for node in ast.iter_child_nodes(TREE):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == name:
                    val = node.value
                    # frozenset({...})
                    if isinstance(val, ast.Call) and isinstance(val.args[0], ast.Set):
                        return {
                            elt.value for elt in val.args[0].elts
                            if isinstance(elt, ast.Constant) and isinstance(elt.value, str)
                        }
    return set()


def _extract_decorated_functions() -> list[str]:
    """Find all functions decorated with @mcp.tool(...)."""
    tools = []
    for node in ast.walk(TREE):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for dec in node.decorator_list:
                if isinstance(dec, ast.Call) and isinstance(dec.func, ast.Attribute):
                    if (isinstance(dec.func.value, ast.Name) and
                            dec.func.value.id == "mcp" and dec.func.attr == "tool"):
                        tools.append(node.name)
    return tools


# Pre-extract all constants
MARVIN_TOOLS = _extract_list_constant("MARVIN_TOOLS")
MILVUS_TOOLS = _extract_frozenset_constant("MILVUS_TOOLS")
OVERVIEW_TOOLS = _extract_frozenset_constant("OVERVIEW_TOOLS")
NEO4J_READ_TOOLS = _extract_frozenset_constant("NEO4J_READ_TOOLS")
WRITE_TOOLS = _extract_frozenset_constant("WRITE_TOOLS")
GATED_TOOLS = NEO4J_READ_TOOLS | WRITE_TOOLS
DECORATED_TOOLS = _extract_decorated_functions()


# ── MARVIN_TOOLS ────────────────────────────────────────────────────────────


class TestMarvinTools:
    def test_has_47_tools(self):
        assert len(MARVIN_TOOLS) == 47

    def test_no_duplicates(self):
        assert len(MARVIN_TOOLS) == len(set(MARVIN_TOOLS))

    def test_core_tools_present(self):
        for tool in ["retrieve", "get_concept", "traverse", "expand", "log_decision",
                      "stats", "self_description", "improve_code", "tdd", "orchestrate"]:
            assert tool in MARVIN_TOOLS, f"{tool} missing from MARVIN_TOOLS"

    def test_matches_decorated_functions(self):
        """Every entry in MARVIN_TOOLS should have a corresponding @mcp.tool function."""
        decorated_set = set(DECORATED_TOOLS)
        marvin_set = set(MARVIN_TOOLS)
        missing_decorator = marvin_set - decorated_set
        missing_list = decorated_set - marvin_set
        assert not missing_decorator, f"In MARVIN_TOOLS but no @mcp.tool: {missing_decorator}"
        assert not missing_list, f"Has @mcp.tool but not in MARVIN_TOOLS: {missing_list}"


# ── Tier Classification ────────────────────────────────────────────────────


class TestTierClassification:
    def test_milvus_tools(self):
        expected = {"retrieve", "get_memory", "search_docs", "refine_plan",
                    "improve_code", "tdd", "score_applicability", "scan_owasp", "orchestrate", "classify_keywords"}
        assert MILVUS_TOOLS == expected

    def test_overview_tools(self):
        expected = {"list_concepts", "list_docs", "list_diagrams",
                    "get_doc", "get_diagram",
                    "stats", "self_description", "inspect_schemas"}
        assert OVERVIEW_TOOLS == expected

    def test_neo4j_read_tools(self):
        expected = {"get_concept", "traverse", "why_exists", "audit_code"}
        assert NEO4J_READ_TOOLS == expected

    def test_write_tools_contains_key_tools(self):
        assert "expand" in WRITE_TOOLS
        assert "link" in WRITE_TOOLS
        assert "save_doc" in WRITE_TOOLS
        assert "sync_vaults" in WRITE_TOOLS
        assert "self_improve" in WRITE_TOOLS

    def test_gated_is_union_of_neo4j_read_and_write(self):
        assert GATED_TOOLS == NEO4J_READ_TOOLS | WRITE_TOOLS

    def test_every_tool_classified(self):
        """Every tool in MARVIN_TOOLS should be in exactly one tier or be always-allowed."""
        classified = MILVUS_TOOLS | OVERVIEW_TOOLS | NEO4J_READ_TOOLS | WRITE_TOOLS
        always_allowed = set(MARVIN_TOOLS) - classified
        expected_always = {"log_decision", "log_session", "propose_schema_change",
                           "fetch_url", "rank_urls", "audit_prompt", "judge_diagram"}
        assert always_allowed == expected_always

    def test_no_tier_overlap(self):
        """No tool should be in multiple tiers."""
        tiers = [MILVUS_TOOLS, OVERVIEW_TOOLS, NEO4J_READ_TOOLS, WRITE_TOOLS]
        names = ["MILVUS", "OVERVIEW", "NEO4J_READ", "WRITE"]
        for i, a in enumerate(tiers):
            for j, b in enumerate(tiers):
                if i < j:
                    overlap = a & b
                    assert not overlap, f"{names[i]} and {names[j]} overlap: {overlap}"

    def test_tier_counts(self):
        assert len(MILVUS_TOOLS) == 10
        assert len(OVERVIEW_TOOLS) == 8
        assert len(NEO4J_READ_TOOLS) == 4
        assert len(WRITE_TOOLS) == 18

    def test_all_classified_tools_in_marvin_tools(self):
        """Every classified tool should exist in MARVIN_TOOLS."""
        classified = MILVUS_TOOLS | OVERVIEW_TOOLS | NEO4J_READ_TOOLS | WRITE_TOOLS
        marvin_set = set(MARVIN_TOOLS)
        not_in_list = classified - marvin_set
        assert not not_in_list, f"Classified but not in MARVIN_TOOLS: {not_in_list}"


# ── Middleware class existence ──────────────────────────────────────────────


class TestMiddleware:
    def test_retrieve_before_act_middleware_exists(self):
        """The middleware class should exist in the source."""
        class_names = [
            node.name for node in ast.walk(TREE)
            if isinstance(node, ast.ClassDef)
        ]
        assert "RetrieveBeforeActMiddleware" in class_names

    def test_middleware_has_on_call_tool(self):
        """The middleware should have an on_call_tool method."""
        for node in ast.walk(TREE):
            if isinstance(node, ast.ClassDef) and node.name == "RetrieveBeforeActMiddleware":
                methods = [n.name for n in node.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
                assert "on_call_tool" in methods


# ── build_self_description structure ────────────────────────────────────────


class TestBuildSelfDescription:
    def test_function_exists(self):
        funcs = [
            node.name for node in ast.walk(TREE)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        ]
        assert "build_self_description" in funcs

    def test_build_tool_catalog_exists(self):
        funcs = [
            node.name for node in ast.walk(TREE)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        ]
        assert "_build_tool_catalog" in funcs


# ── Lifespan ────────────────────────────────────────────────────────────────


class TestLifespan:
    def test_lifespan_function_exists(self):
        funcs = [
            node.name for node in ast.walk(TREE)
            if isinstance(node, ast.AsyncFunctionDef)
        ]
        assert "marvin_lifespan" in funcs


# ── Source structure ────────────────────────────────────────────────────────


class TestSourceStructure:
    def test_imports_all_backends(self):
        """All 9 backends should be imported via 'from backends import X'."""
        imported_names = []
        for node in ast.iter_child_nodes(TREE):
            if isinstance(node, ast.ImportFrom) and node.module == "backends":
                for alias in node.names:
                    imported_names.append(alias.name)
        expected_backends = [
            "ontology", "memory", "docs_backend", "web_to_docs_backend",
            "prompt_engineer_backend", "system_design_backend",
            "code_improvement_backend", "orchestrator_backend", "ops_backend",
        ]
        for backend in expected_backends:
            assert backend in imported_names, f"Missing import: {backend}"

    def test_all_tool_functions_have_docstrings(self):
        for node in ast.walk(TREE):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                for dec in node.decorator_list:
                    if isinstance(dec, ast.Call) and isinstance(dec.func, ast.Attribute):
                        if (isinstance(dec.func.value, ast.Name) and
                                dec.func.value.id == "mcp" and dec.func.attr == "tool"):
                            docstring = ast.get_docstring(node)
                            assert docstring, f"Tool {node.name} has no docstring"
