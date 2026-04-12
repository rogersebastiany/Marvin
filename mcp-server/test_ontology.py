"""
Tests for ontology.py — locking current behavior as a TDD safety net.

All Neo4j interactions are mocked. Tests verify output formatting,
branching logic, and constant integrity.
"""

import pytest
from unittest.mock import MagicMock, patch, PropertyMock


# ── Helpers ──────────────────────────────────────────────────────────────────


def _make_record(data: dict):
    """Create a mock Neo4j record."""
    rec = MagicMock()
    rec.__getitem__ = lambda self, k: data[k]
    rec.keys = lambda: list(data.keys())
    rec.get = lambda k, default=None: data.get(k, default)
    return rec


def _make_node(props: dict):
    """Create a mock Neo4j node."""
    node = MagicMock()
    node.__getitem__ = lambda self, k: props[k]
    node.get = lambda k, default=None: props.get(k, default)
    return node


@pytest.fixture
def mock_neo4j():
    """Mock Neo4j driver and session."""
    with patch("ontology._get_driver") as mock_get:
        mock_driver = MagicMock()
        mock_get.return_value = mock_driver
        mock_session = MagicMock()
        mock_driver.session.return_value.__enter__ = MagicMock(return_value=mock_session)
        mock_driver.session.return_value.__exit__ = MagicMock(return_value=False)

        yield {
            "driver": mock_driver,
            "session": mock_session,
        }


# ── Constants ────────────────────────────────────────────────────────────────


class TestConstants:
    def test_relation_types_count(self):
        from ontology import RELATION_TYPES
        assert len(RELATION_TYPES) == 16

    def test_symmetric_types(self):
        from ontology import SYMMETRIC_TYPES
        assert "RELATES_TO" in SYMMETRIC_TYPES
        assert "CONTRADICTS" in SYMMETRIC_TYPES
        assert "ANALOGOUS_TO" in SYMMETRIC_TYPES
        # Directional types should NOT be symmetric
        assert "IMPLEMENTS" not in SYMMETRIC_TYPES
        assert "REQUIRES" not in SYMMETRIC_TYPES

    def test_relation_descriptions_complete(self):
        from ontology import RELATION_TYPES, RELATION_DESCRIPTIONS
        for rt in RELATION_TYPES:
            assert rt in RELATION_DESCRIPTIONS
            assert len(RELATION_DESCRIPTIONS[rt]) > 0

    def test_any_rel_fragment(self):
        from ontology import _ANY_REL, RELATION_TYPES
        for rt in RELATION_TYPES:
            assert rt in _ANY_REL


# ── _get_driver ──────────────────────────────────────────────────────────────


class TestGetDriver:
    def test_creates_driver_once(self):
        import ontology
        ontology._driver = None
        with patch("ontology.GraphDatabase.driver") as mock_gd:
            mock_gd.return_value = MagicMock()
            d1 = ontology._get_driver()
            d2 = ontology._get_driver()
            mock_gd.assert_called_once()
            assert d1 is d2
        ontology._driver = None


# ── query ────────────────────────────────────────────────────────────────────


class TestQuery:
    def test_milvus_primary_path(self, mock_neo4j):
        from ontology import query
        with patch.dict("sys.modules", {"memory": MagicMock()}) as _, \
             patch("memory.search_concepts_semantic") as _mock_search:
            import memory as mock_mem_mod
            mock_mem = mock_mem_mod
            mock_mem.search_concepts_semantic.return_value = [
                {"name": "TestConcept", "vault": "cognee", "summary": "A concept", "score": 0.85}
            ]
            result = query("test")
            assert "Found 1 concept(s)" in result
            assert "[cognee]" in result
            assert "TestConcept" in result
            assert "score=0.850" in result

    def test_milvus_empty_falls_through_to_neo4j(self, mock_neo4j):
        from ontology import query
        with patch.dict("sys.modules", {"memory": MagicMock()}) as _, \
             patch("memory.search_concepts_semantic") as _mock_search:
            import memory as mock_mem_mod
            mock_mem = mock_mem_mod
            mock_mem.search_concepts_semantic.return_value = []
            # Neo4j fallback returns results
            mock_neo4j["session"].run.return_value = [
                _make_record({"name": "Fallback", "vault": "test", "summary": "sum", "ghost": False, "aliases": None})
            ]
            result = query("test")
            assert "keyword fallback" in result
            assert "Fallback" in result

    def test_milvus_exception_falls_to_neo4j(self, mock_neo4j):
        from ontology import query
        with patch.dict("sys.modules", {"memory": MagicMock()}) as _, \
             patch("memory.search_concepts_semantic") as _mock_search:
            import memory as mock_mem_mod
            mock_mem = mock_mem_mod
            mock_mem.search_concepts_semantic.side_effect = Exception("Milvus down")
            mock_neo4j["session"].run.return_value = []
            result = query("test")
            assert "No concepts found" in result

    def test_no_results_anywhere(self, mock_neo4j):
        from ontology import query
        with patch.dict("sys.modules", {"memory": MagicMock()}) as _, \
             patch("memory.search_concepts_semantic") as _mock_search:
            import memory as mock_mem_mod
            mock_mem = mock_mem_mod
            mock_mem.search_concepts_semantic.return_value = []
            mock_neo4j["session"].run.return_value = []
            result = query("nonexistent")
            assert "No concepts found" in result
            assert "nonexistent" in result

    def test_ghost_and_aliases_in_fallback(self, mock_neo4j):
        from ontology import query
        with patch.dict("sys.modules", {"memory": MagicMock()}) as _, \
             patch("memory.search_concepts_semantic") as _mock_search:
            import memory as mock_mem_mod
            mock_mem = mock_mem_mod
            mock_mem.search_concepts_semantic.return_value = []
            mock_neo4j["session"].run.return_value = [
                _make_record({
                    "name": "Ghost", "vault": "test", "summary": "",
                    "ghost": True, "aliases": ["Fantasma"]
                })
            ]
            result = query("ghost")
            assert "(ghost)" in result
            assert "Fantasma" in result


# ── set_aliases ──────────────────────────────────────────────────────────────


class TestSetAliases:
    def test_concept_not_found(self, mock_neo4j):
        from ontology import set_aliases
        mock_neo4j["session"].run.return_value.single.return_value = None
        result = set_aliases("Missing", ["alias1"])
        assert "not found" in result

    def test_success(self, mock_neo4j):
        from ontology import set_aliases
        # First call (check existence) returns a node
        mock_neo4j["session"].run.return_value.single.return_value = {"c": {}}
        result = set_aliases("MyConc", ["eng1", "eng2"])
        assert "Set aliases" in result
        assert "eng1" in result
        assert "eng2" in result


# ── batch_set_aliases ────────────────────────────────────────────────────────


class TestBatchSetAliases:
    def test_mixed_results(self, mock_neo4j):
        from ontology import batch_set_aliases
        # Alternate: found, not found
        mock_neo4j["session"].run.return_value.single.side_effect = [
            {"c": {}}, None
        ]
        mappings = [
            {"name": "Found", "aliases": ["a"]},
            {"name": "NotFound", "aliases": ["b"]},
        ]
        result = batch_set_aliases(mappings)
        assert "Processed 2" in result
        assert "'Found'" in result
        assert "'NotFound' not found" in result


# ── get_concept ──────────────────────────────────────────────────────────────


class TestGetConcept:
    def test_not_found_with_suggestions(self, mock_neo4j):
        from ontology import get_concept
        # First call: concept not found
        mock_neo4j["session"].run.return_value.single.return_value = None
        # Second call: suggestions
        mock_neo4j["session"].run.return_value = [
            _make_record({"c.name": "Similar"}),
        ]
        # Override: first .single() returns None, second .run() returns suggestions
        call_count = [0]
        def run_side_effect(*args, **kwargs):
            call_count[0] += 1
            result = MagicMock()
            if call_count[0] == 1:
                result.single.return_value = None
                return result
            else:
                # Return list of name records
                rec = MagicMock()
                rec.__getitem__ = lambda s, i: "SimilarConcept"
                return [rec]
        mock_neo4j["session"].run.side_effect = run_side_effect
        result = get_concept("Missing")
        assert "not found" in result

    def test_not_found_no_suggestions(self, mock_neo4j):
        from ontology import get_concept
        call_count = [0]
        def run_side_effect(*args, **kwargs):
            call_count[0] += 1
            result = MagicMock()
            if call_count[0] == 1:
                result.single.return_value = None
                return result
            return []
        mock_neo4j["session"].run.side_effect = run_side_effect
        result = get_concept("Missing")
        assert "not found" in result

    def test_found_with_content_and_links(self, mock_neo4j):
        from ontology import get_concept
        node = _make_node({
            "name": "TestConcept", "vault": "cognee", "ghost": False,
            "summary": "A test", "content": "Some content here"
        })
        call_count = [0]
        def run_side_effect(*args, **kwargs):
            call_count[0] += 1
            if call_count[0] == 1:
                result = MagicMock()
                result.single.return_value = {"c": node}
                return result
            elif call_count[0] == 2:
                return [_make_record({
                    "target": "Other", "rel_type": "RELATES_TO",
                    "reasoning": "test", "weight": 1.0, "by": "agent"
                })]
            else:
                return []
        mock_neo4j["session"].run.side_effect = run_side_effect
        result = get_concept("TestConcept")
        assert "# TestConcept" in result
        assert "Vault: cognee" in result
        assert "Some content here" in result
        assert "Links to (1)" in result
        assert "RELATES_TO" in result


# ── traverse ─────────────────────────────────────────────────────────────────


class TestTraverse:
    def test_not_found(self, mock_neo4j):
        from ontology import traverse
        mock_neo4j["session"].run.return_value.single.return_value = None
        result = traverse("Missing")
        assert "not found" in result

    def test_hops_clamped(self, mock_neo4j):
        from ontology import traverse
        call_count = [0]
        def run_side_effect(*args, **kwargs):
            call_count[0] += 1
            if call_count[0] == 1:
                result = MagicMock()
                result.single.return_value = {"c": {}}
                return result
            return []
        mock_neo4j["session"].run.side_effect = run_side_effect
        result = traverse("A", hops=0)
        assert "no connections" in result

    def test_results_grouped_by_hop(self, mock_neo4j):
        from ontology import traverse
        call_count = [0]
        def run_side_effect(*args, **kwargs):
            call_count[0] += 1
            if call_count[0] == 1:
                result = MagicMock()
                result.single.return_value = {"c": {}}
                return result
            return [
                _make_record({"name": "B", "vault": "cognee", "ghost": False, "distance": 1}),
                _make_record({"name": "C", "vault": "cognee", "ghost": False, "distance": 2}),
            ]
        mock_neo4j["session"].run.side_effect = run_side_effect
        result = traverse("A", hops=2)
        assert "Neighborhood of 'A'" in result
        assert "Hop 1" in result
        assert "Hop 2" in result
        assert "B" in result
        assert "C" in result


# ── why_exists ───────────────────────────────────────────────────────────────


class TestWhyExists:
    def test_not_found(self, mock_neo4j):
        from ontology import why_exists
        mock_neo4j["session"].run.return_value.single.return_value = None
        result = why_exists("Missing")
        assert "not found" in result

    def test_ghost_concept(self, mock_neo4j):
        from ontology import why_exists
        node = _make_node({
            "name": "Ghost", "vault": "ghost", "ghost": True,
            "summary": "", "content": ""
        })
        call_count = [0]
        def run_side_effect(*args, **kwargs):
            call_count[0] += 1
            if call_count[0] == 1:
                result = MagicMock()
                result.single.return_value = {"c": node}
                return result
            return []
        mock_neo4j["session"].run.side_effect = run_side_effect
        result = why_exists("Ghost")
        assert "ghost node" in result

    def test_with_edges(self, mock_neo4j):
        from ontology import why_exists
        node = _make_node({
            "name": "A", "vault": "cognee", "ghost": False,
            "summary": "concept", "content": ""
        })
        call_count = [0]
        def run_side_effect(*args, **kwargs):
            call_count[0] += 1
            if call_count[0] == 1:
                result = MagicMock()
                result.single.return_value = {"c": node}
                return result
            return [_make_record({
                "other": "B", "rel_type": "REQUIRES",
                "reasoning": "A needs B", "by": "agent",
                "weight": 1.0, "dir": "→"
            })]
        mock_neo4j["session"].run.side_effect = run_side_effect
        result = why_exists("A")
        assert "Relations (1)" in result
        assert "REQUIRES" in result
        assert "A needs B" in result


# ── expand ───────────────────────────────────────────────────────────────────


class TestExpand:
    def test_create_new_concept(self, mock_neo4j):
        from ontology import expand
        mock_neo4j["session"].run.return_value.single.return_value = None
        result = expand("NewConcept", summary="A new one")
        assert "Created concept 'NewConcept'" in result
        assert "vault: agent" in result

    def test_update_existing_concept(self, mock_neo4j):
        from ontology import expand
        mock_neo4j["session"].run.return_value.single.return_value = {"c": {}}
        result = expand("Existing", summary="Updated")
        assert "Updated concept 'Existing'" in result

    def test_existing_no_changes(self, mock_neo4j):
        from ontology import expand
        mock_neo4j["session"].run.return_value.single.return_value = {"c": {}}
        result = expand("Existing")
        assert "already exists" in result

    def test_create_with_relation(self, mock_neo4j):
        from ontology import expand
        # First .single() = None (concept doesn't exist)
        # Then .single() = None (target doesn't exist → ghost)
        mock_neo4j["session"].run.return_value.single.return_value = None
        result = expand("A", relate_to="B", relation_type="REQUIRES", reasoning="A needs B")
        assert "Created concept 'A'" in result
        assert "REQUIRES" in result

    def test_invalid_relation_type_defaults(self, mock_neo4j):
        from ontology import expand
        mock_neo4j["session"].run.return_value.single.return_value = None
        result = expand("A", relate_to="B", relation_type="INVALID")
        assert "RELATES_TO" in result


# ── auto_link ────────────────────────────────────────────────────────────────


class TestAutoLink:
    def test_concept_not_found(self, mock_neo4j):
        from ontology import auto_link
        call_count = [0]
        def run_side_effect(*args, **kwargs):
            call_count[0] += 1
            if call_count[0] == 1:
                return [_make_record({"name": "A"}), _make_record({"name": "B"})]
            return []
        mock_neo4j["session"].run.side_effect = run_side_effect
        result = auto_link("Missing")
        assert "not found" in result

    def test_no_isolated_concepts(self, mock_neo4j):
        from ontology import auto_link
        call_count = [0]
        def run_side_effect(*args, **kwargs):
            call_count[0] += 1
            if call_count[0] == 1:
                return [_make_record({"name": "A"})]
            return []
        mock_neo4j["session"].run.side_effect = run_side_effect
        result = auto_link()
        assert "No isolated concepts" in result


# ── ensure_bidirectional ─────────────────────────────────────────────────────


class TestEnsureBidirectional:
    def test_concept_not_found(self, mock_neo4j):
        from ontology import ensure_bidirectional
        mock_neo4j["session"].run.return_value.single.return_value = None
        result = ensure_bidirectional("Missing")
        assert "not found" in result

    def test_already_bidirectional(self, mock_neo4j):
        from ontology import ensure_bidirectional
        call_count = [0]
        def run_side_effect(*args, **kwargs):
            call_count[0] += 1
            if call_count[0] == 1:
                result = MagicMock()
                result.single.return_value = {"c": {}}
                return result
            return []
        mock_neo4j["session"].run.side_effect = run_side_effect
        result = ensure_bidirectional("A")
        assert "already bidirectional" in result

    def test_all_bidirectional_no_name(self, mock_neo4j):
        from ontology import ensure_bidirectional
        mock_neo4j["session"].run.return_value = []
        result = ensure_bidirectional()
        assert "already bidirectional" in result


# ── run_cypher ───────────────────────────────────────────────────────────────


class TestRunCypher:
    def test_no_results(self, mock_neo4j):
        from ontology import run_cypher
        mock_neo4j["session"].run.return_value = []
        result = run_cypher("MATCH (n) RETURN n LIMIT 0")
        assert "(no results)" in result

    def test_with_results(self, mock_neo4j):
        from ontology import run_cypher
        rec = _make_record({"name": "A", "count": 5})
        mock_neo4j["session"].run.return_value = [rec]
        result = run_cypher("MATCH (n) RETURN n.name AS name")
        assert "name=A" in result
        assert "count=5" in result


# ── get_vault_concepts ───────────────────────────────────────────────────────


class TestGetVaultConcepts:
    def test_returns_list(self, mock_neo4j):
        from ontology import get_vault_concepts
        mock_neo4j["session"].run.return_value = [
            _make_record({
                "name": "A", "summary": "Sum A", "content": "Content A",
                "rels": [{"target": "B", "type": "RELATES_TO"}]
            })
        ]
        result = get_vault_concepts("cognee")
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]["name"] == "A"
        assert len(result[0]["relations"]) == 1

    def test_filters_none_rels(self, mock_neo4j):
        from ontology import get_vault_concepts
        mock_neo4j["session"].run.return_value = [
            _make_record({"name": "A", "summary": "", "content": "", "rels": [None, None]})
        ]
        result = get_vault_concepts("test")
        assert result[0]["relations"] == []


# ── list_concepts ────────────────────────────────────────────────────────────


class TestListConcepts:
    def test_empty_graph(self, mock_neo4j):
        from ontology import list_concepts
        mock_neo4j["session"].run.return_value = []
        result = list_concepts()
        assert "No concepts" in result

    def test_grouped_by_vault(self, mock_neo4j):
        from ontology import list_concepts
        mock_neo4j["session"].run.return_value = [
            _make_record({"name": "A", "vault": "cognee"}),
            _make_record({"name": "B", "vault": "cognee"}),
            _make_record({"name": "C", "vault": "agent"}),
        ]
        result = list_concepts()
        assert "3 concepts" in result
        assert "[cognee]" in result
        assert "[agent]" in result


# ── get_stats ────────────────────────────────────────────────────────────────


class TestGetStats:
    def test_returns_dict_structure(self, mock_neo4j):
        from ontology import get_stats
        call_count = [0]
        def run_side_effect(*args, **kwargs):
            call_count[0] += 1
            result = MagicMock()
            if call_count[0] in (1, 2, 3, 5):
                # nodes, edges, ghosts, agent_edges
                result.single.return_value = {"n": 10}
                return result
            elif call_count[0] == 4:
                # vaults
                return [_make_record({"vault": "cognee", "n": 8})]
            else:
                # edge_types
                return [_make_record({"rel_type": "RELATES_TO", "n": 5})]
        mock_neo4j["session"].run.side_effect = run_side_effect
        result = get_stats()
        assert isinstance(result, dict)
        assert "nodes" in result
        assert "edges" in result
        assert "ghosts" in result
        assert "vaults" in result
        assert "agent_edges" in result
        assert "edge_types" in result


# ── get_schema ───────────────────────────────────────────────────────────────


class TestGetSchema:
    def test_returns_markdown(self, mock_neo4j):
        from ontology import get_schema
        call_count = [0]
        def run_side_effect(*args, **kwargs):
            call_count[0] += 1
            if call_count[0] == 1:
                # labels
                rec = MagicMock()
                rec.__getitem__ = lambda s, i: "Concept"
                return [rec]
            elif call_count[0] == 2:
                # rel_types
                rec = MagicMock()
                rec.__getitem__ = lambda s, i: "RELATES_TO"
                return [rec]
            elif call_count[0] == 3:
                # constraints
                return [_make_record({
                    "name": "c1", "type": "UNIQUENESS",
                    "labelsOrTypes": ["Concept"], "properties": ["name"]
                })]
            else:
                # indexes
                return [_make_record({
                    "name": "idx1", "type": "RANGE",
                    "labelsOrTypes": ["Concept"], "properties": ["name"]
                })]
        mock_neo4j["session"].run.side_effect = run_side_effect
        result = get_schema()
        assert "# Neo4j Schema" in result
        assert "Labels" in result
        assert "Relationship Types" in result
        assert "Constraints" in result
        assert "Indexes" in result
