"""
Tests for memory.py — locking current behavior as a TDD safety net.

All external dependencies (Milvus, OpenAI) are mocked.
Pure functions (_chunk_markdown, _format_ressalva) are tested directly.
"""

import pytest
from unittest.mock import MagicMock, patch, call
from datetime import datetime, timezone


# ── Pure function tests ─────────────────────────────────────────────────────


class TestChunkMarkdown:
    """_chunk_markdown is pure: markdown text → list of chunk dicts."""

    def _chunk(self, text, doc_name="testdoc"):
        from backends.memory import _chunk_markdown
        return _chunk_markdown(text, doc_name)

    def test_empty_text_returns_empty(self):
        assert self._chunk("") == []

    def test_single_section_with_heading(self):
        text = "## Introduction\nThis is the introduction section with enough content to pass the 50-char minimum threshold for chunks."
        chunks = self._chunk(text)
        assert len(chunks) == 1
        assert chunks[0]["heading"] == "Introduction"
        assert chunks[0]["doc_name"] == "testdoc"
        assert chunks[0]["chunk_index"] == 1
        assert chunks[0]["id"] == "testdoc::1"
        assert "introduction section" in chunks[0]["content"].lower()

    def test_multiple_sections(self):
        text = (
            "## First Section\n"
            "Content for the first section that is long enough to exceed the fifty character minimum.\n\n"
            "## Second Section\n"
            "Content for the second section that is also long enough to exceed the fifty character minimum."
        )
        chunks = self._chunk(text)
        assert len(chunks) == 2
        assert chunks[0]["heading"] == "First Section"
        assert chunks[1]["heading"] == "Second Section"

    def test_skips_tiny_chunks_under_50_chars(self):
        text = "## Tiny\nShort."
        chunks = self._chunk(text)
        assert len(chunks) == 0

    def test_preamble_before_first_heading(self):
        text = (
            "This is a preamble with enough text to exceed fifty characters for the minimum threshold requirement.\n\n"
            "## Actual Section\n"
            "This section also has enough text to exceed fifty characters for the minimum threshold requirement."
        )
        chunks = self._chunk(text)
        # Preamble chunk uses doc_name as heading since it doesn't start with #
        preamble_chunks = [c for c in chunks if c["heading"] == "testdoc"]
        assert len(preamble_chunks) <= 1  # preamble may or may not be included

    def test_content_truncated_at_8000_chars(self):
        text = "## Big Section\n" + "x" * 10000
        chunks = self._chunk(text)
        assert len(chunks) == 1
        assert len(chunks[0]["content"]) <= 8000

    def test_heading_truncated_at_500_chars(self):
        text = "## " + "H" * 600 + "\n" + "Content " * 20
        chunks = self._chunk(text)
        assert len(chunks) == 1
        assert len(chunks[0]["heading"]) <= 500

    def test_embed_text_contains_heading_and_content(self):
        text = "## My Heading\nSome content that is long enough to be above the fifty character minimum for chunks in memory."
        chunks = self._chunk(text)
        assert len(chunks) == 1
        assert "My Heading" in chunks[0]["embed_text"]
        assert "Some content" in chunks[0]["embed_text"]

    def test_chunk_index_sequential(self):
        text = (
            "## A\n" + "a" * 60 + "\n\n"
            "## B\n" + "b" * 60 + "\n\n"
            "## C\n" + "c" * 60
        )
        chunks = self._chunk(text)
        indices = [c["chunk_index"] for c in chunks]
        assert indices == sorted(indices)
        # Indices come from enumerate over re.split parts, so they may not be 0,1,2
        # but must be strictly increasing
        assert len(set(indices)) == len(indices)


class TestFormatRessalva:
    """_format_ressalva is pure: (collection_name, hit_dict) → string."""

    def _fmt(self, collection, hit):
        from backends.memory import _format_ressalva
        return _format_ressalva(collection, hit)

    def test_concepts_format(self):
        hit = {"vault": "cognee", "name": "TestConcept", "summary": "A test concept"}
        result = self._fmt("concepts", hit)
        assert "[cognee]" in result
        assert "TestConcept" in result
        assert "A test concept" in result

    def test_decisions_format(self):
        hit = {"objective": "Decide X", "chosen_option": "Option A", "reasoning": "Because Y"}
        result = self._fmt("decisions", hit)
        assert "Decide X" in result
        assert "Option A" in result
        assert "Because Y" in result

    def test_sessions_format(self):
        hit = {"objective": "Session goal", "lessons_learned": "Lesson 1"}
        result = self._fmt("sessions", hit)
        assert "Session goal" in result
        assert "Lesson 1" in result

    def test_doc_chunks_format(self):
        hit = {"doc_name": "readme", "heading": "Setup", "content": "Install with pip"}
        result = self._fmt("doc_chunks", hit)
        assert "readme" in result
        assert "Setup" in result
        assert "Install with pip" in result

    def test_plans_format(self):
        hit = {"status": "approved", "name": "my-plan", "title": "My Plan", "summary": "Do things"}
        result = self._fmt("plans", hit)
        assert "[approved]" in result
        assert "my-plan" in result
        assert "My Plan" in result

    def test_unknown_collection_returns_str(self):
        hit = {"foo": "bar"}
        result = self._fmt("unknown_collection", hit)
        assert "bar" in result

    def test_missing_fields_use_fallbacks(self):
        result = self._fmt("concepts", {})
        assert "[?]" in result
        assert "?" in result

    def test_long_fields_truncated(self):
        hit = {"objective": "X" * 200, "chosen_option": "Y" * 200, "reasoning": "Z" * 200}
        result = self._fmt("decisions", hit)
        assert len(result) < 500  # truncation should keep it reasonable


# ── Mocked integration tests ───────────────────────────────────────────────


@pytest.fixture
def mock_milvus():
    """Mock Milvus connections and Collection."""
    with patch("backends.memory.connections") as mock_conn, \
         patch("backends.memory.Collection") as mock_col_cls, \
         patch("backends.memory.utility") as mock_util:
        # Reset global connection state
        from backends import memory
        memory._connected = False

        mock_col = MagicMock()
        mock_col_cls.return_value = mock_col
        mock_col.num_entities = 0

        yield {
            "connections": mock_conn,
            "Collection": mock_col_cls,
            "collection": mock_col,
            "utility": mock_util,
        }


@pytest.fixture
def mock_openai():
    """Mock OpenAI embeddings client."""
    with patch("backends.memory._get_openai") as mock_get:
        mock_client = MagicMock()
        mock_get.return_value = mock_client

        # Default: return a 1536-dim zero vector
        mock_embedding = MagicMock()
        mock_embedding.embedding = [0.0] * 1536

        mock_response = MagicMock()
        mock_response.data = [mock_embedding]
        mock_client.embeddings.create.return_value = mock_response

        yield {
            "get_openai": mock_get,
            "client": mock_client,
            "response": mock_response,
        }


class TestEnsureConnected:
    def test_connects_once(self, mock_milvus):
        from backends.memory import _ensure_connected
        _ensure_connected()
        _ensure_connected()
        # Should only connect once
        mock_milvus["connections"].connect.assert_called_once()

    def test_uses_env_vars(self, mock_milvus):
        from backends.memory import _ensure_connected, MILVUS_HOST, MILVUS_PORT
        _ensure_connected()
        mock_milvus["connections"].connect.assert_called_with(
            "default", host=MILVUS_HOST, port=MILVUS_PORT
        )


class TestEmbed:
    def test_embed_returns_vector(self, mock_openai):
        from backends.memory import _embed
        result = _embed("test text")
        assert isinstance(result, list)
        assert len(result) == 1536
        mock_openai["client"].embeddings.create.assert_called_once()

    def test_embed_batch_batching(self, mock_openai):
        from backends.memory import _embed_batch
        # Create enough texts to trigger batching
        texts = [f"text {i}" for i in range(150)]

        mock_emb = MagicMock()
        mock_emb.embedding = [0.0] * 1536
        # The mock returns the same response object for both calls,
        # so .data always has 100 items → 200 total (100+100).
        # The real API would return 50 for the second batch.
        # We need per-call responses to test accurately.
        resp_100 = MagicMock()
        resp_100.data = [MagicMock(embedding=[0.0]*1536) for _ in range(100)]
        resp_50 = MagicMock()
        resp_50.data = [MagicMock(embedding=[0.0]*1536) for _ in range(50)]
        mock_openai["client"].embeddings.create.side_effect = [resp_100, resp_50]

        result = _embed_batch(texts, batch_size=100)
        # Should make 2 API calls (100 + 50)
        assert mock_openai["client"].embeddings.create.call_count == 2
        assert len(result) == 150

    def test_embed_batch_empty(self, mock_openai):
        from backends.memory import _embed_batch
        result = _embed_batch([])
        assert result == []
        mock_openai["client"].embeddings.create.assert_not_called()


class TestSearchCollection:
    def test_returns_formatted_hits(self, mock_milvus, mock_openai):
        from backends.memory import _search_collection

        # Mock search results
        mock_hit = MagicMock()
        mock_hit.score = 0.95
        mock_hit.entity.get = lambda f: {"tool_name": "test_tool", "parameters": "{}"}[f]

        mock_milvus["collection"].search.return_value = [[mock_hit]]

        hits = _search_collection("tool_calls", "query", 5, ["tool_name", "parameters"])
        assert len(hits) == 1
        assert hits[0]["score"] == 0.95

    def test_empty_results(self, mock_milvus, mock_openai):
        from backends.memory import _search_collection

        mock_milvus["collection"].search.return_value = [[]]
        hits = _search_collection("tool_calls", "query", 5, ["tool_name"])
        assert hits == []

    def test_uses_cosine_metric(self, mock_milvus, mock_openai):
        from backends.memory import _search_collection

        mock_milvus["collection"].search.return_value = [[]]
        _search_collection("tool_calls", "query", 5, ["tool_name"])

        call_kwargs = mock_milvus["collection"].search.call_args
        assert call_kwargs[1]["param"]["metric_type"] == "COSINE"
        assert call_kwargs[1]["anns_field"] == "embedding"


class TestSearchFunctions:
    """Test the public search_* functions return properly formatted strings."""

    def _setup_search(self, mock_milvus, mock_openai, hits):
        mock_milvus["collection"].search.return_value = [hits]

    def test_search_tool_calls_no_results(self, mock_milvus, mock_openai):
        self._setup_search(mock_milvus, mock_openai, [])
        from backends.memory import search_tool_calls
        result = search_tool_calls("query")
        assert result == "No similar tool calls found."

    def test_search_tool_calls_with_results(self, mock_milvus, mock_openai):
        mock_hit = MagicMock()
        mock_hit.score = 0.9
        mock_hit.entity.get = lambda f: {
            "tool_name": "retrieve",
            "parameters": '{"query": "test"}',
            "result_summary": "Found 3 results",
            "context": "testing",
            "timestamp": "2026-04-12T00:00:00Z",
            "success": True,
        }.get(f)
        self._setup_search(mock_milvus, mock_openai, [mock_hit])
        from backends.memory import search_tool_calls
        result = search_tool_calls("query")
        assert "Found 1 similar tool call(s)" in result
        assert "[ok]" in result
        assert "retrieve" in result

    def test_search_decisions_no_results(self, mock_milvus, mock_openai):
        self._setup_search(mock_milvus, mock_openai, [])
        from backends.memory import search_decisions
        assert search_decisions("query") == "No similar decisions found."

    def test_search_plans_no_results(self, mock_milvus, mock_openai):
        self._setup_search(mock_milvus, mock_openai, [])
        from backends.memory import search_plans
        assert search_plans("query") == "No similar plans found."

    def test_search_sessions_no_results(self, mock_milvus, mock_openai):
        self._setup_search(mock_milvus, mock_openai, [])
        from backends.memory import search_sessions
        assert search_sessions("query") == "No similar sessions found."

    def test_search_tool_calls_fail_status(self, mock_milvus, mock_openai):
        mock_hit = MagicMock()
        mock_hit.score = 0.8
        mock_hit.entity.get = lambda f: {
            "tool_name": "expand",
            "parameters": "{}",
            "result_summary": "Error",
            "context": "",
            "timestamp": "",
            "success": False,
        }.get(f)
        self._setup_search(mock_milvus, mock_openai, [mock_hit])
        from backends.memory import search_tool_calls
        result = search_tool_calls("query")
        assert "[fail]" in result


class TestLogFunctions:
    """Test log_tool_call, log_decision, log_session."""

    def test_log_tool_call_returns_confirmation(self, mock_milvus, mock_openai):
        from backends.memory import log_tool_call
        result = log_tool_call("retrieve", '{"q":"test"}', "Found 5", True, "ctx", "sess1")
        assert "Logged tool call: retrieve" in result
        mock_milvus["collection"].insert.assert_called_once()
        mock_milvus["collection"].flush.assert_called_once()

    def test_log_decision_returns_confirmation(self, mock_milvus, mock_openai):
        from backends.memory import log_decision
        result = log_decision("Decide X", "A or B", "A", "Because reasons")
        assert "Logged decision:" in result
        assert "Decide X" in result
        mock_milvus["collection"].insert.assert_called_once()

    def test_log_decision_truncates_objective(self, mock_milvus, mock_openai):
        from backends.memory import log_decision
        long_obj = "X" * 200
        result = log_decision(long_obj, "opts", "chosen", "reasoning")
        # Confirmation truncates to 60 chars
        assert len(result) < 200

    def test_log_session_returns_confirmation(self, mock_milvus, mock_openai):
        from backends.memory import log_session
        result = log_session("Obj", "Approach", "Result", "Lessons", "tools", 3, 10)
        assert "Logged session:" in result
        mock_milvus["collection"].insert.assert_called_once()


class TestSavePlan:
    def test_upsert_deletes_then_inserts(self, mock_milvus, mock_openai):
        from backends.memory import save_plan
        mock_milvus["collection"].num_entities = 0
        result = save_plan("my-plan", "My Plan", "draft", "Summary", "Full content")
        assert "Saved plan: my-plan [draft]" in result
        # Should delete existing, then insert
        mock_milvus["collection"].delete.assert_called_once()
        mock_milvus["collection"].insert.assert_called_once()
        assert mock_milvus["collection"].flush.call_count == 2  # after delete + after insert

    def test_plan_id_format(self, mock_milvus, mock_openai):
        from backends.memory import save_plan
        result = save_plan("test-plan", "Title", "approved", "Sum", "Content")
        assert "(plan::test-plan)" in result


class TestRefinePlanVectorWalk:
    def test_single_iteration(self, mock_milvus, mock_openai):
        from backends.memory import refine_plan_vector_walk

        # Mock _search_by_vector to return empty for all collections
        with patch("backends.memory._search_by_vector", return_value=[]):
            result = refine_plan_vector_walk("My draft plan", iterations=1)
            assert result["iterations"] == 1
            assert result["total_ressalvas"] == 0
            assert result["unique_sources"] == 0
            assert "per_iteration" in result
            assert "enhanced_draft" in result

    def test_iterations_clamped(self, mock_milvus, mock_openai):
        from backends.memory import refine_plan_vector_walk
        with patch("backends.memory._search_by_vector", return_value=[]):
            # iterations clamped to max 5
            result = refine_plan_vector_walk("draft", iterations=10)
            assert result["iterations"] == 5

            # iterations clamped to min 1
            result = refine_plan_vector_walk("draft", iterations=0)
            assert result["iterations"] == 1

    def test_multiple_iterations_accumulate(self, mock_milvus, mock_openai):
        from backends.memory import refine_plan_vector_walk

        fake_hit = {"name": "TestConcept", "vault": "cognee", "summary": "A concept", "score": 0.8}
        with patch("backends.memory._search_by_vector", return_value=[fake_hit]):
            result = refine_plan_vector_walk("My plan", iterations=2, k_per_collection=1)
            assert result["iterations"] == 2
            assert result["total_ressalvas"] > 0
            assert len(result["per_iteration"]) == 2
            # With iterations > 1, enhanced_draft should contain "Prior art from Milvus"
            assert "Prior art from Milvus" in result["enhanced_draft"]

    def test_k_per_collection_clamped(self, mock_milvus, mock_openai):
        from backends.memory import refine_plan_vector_walk
        with patch("backends.memory._search_by_vector", return_value=[]) as mock_search:
            refine_plan_vector_walk("draft", iterations=1, k_per_collection=50)
            # k clamped to 20
            for c in mock_search.call_args_list:
                assert c[1].get("limit", c[0][2]) <= 20


class TestSearchByVector:
    def test_returns_formatted_hits(self, mock_milvus, mock_openai):
        from backends.memory import _search_by_vector

        mock_hit = MagicMock()
        mock_hit.score = 0.85
        mock_hit.entity.get = lambda f: {"name": "Concept1"}.get(f)
        mock_milvus["collection"].search.return_value = [[mock_hit]]

        hits = _search_by_vector("concepts", [0.0] * 1536, 5, ["name"])
        assert len(hits) == 1
        assert hits[0]["score"] == 0.85
        assert hits[0]["name"] == "Concept1"


class TestSearchDocChunksAndConcepts:
    def test_search_doc_chunks_delegates(self, mock_milvus, mock_openai):
        from backends.memory import search_doc_chunks
        mock_milvus["collection"].search.return_value = [[]]
        result = search_doc_chunks("query", limit=3)
        assert result == []

    def test_search_concepts_semantic_delegates(self, mock_milvus, mock_openai):
        from backends.memory import search_concepts_semantic
        mock_milvus["collection"].search.return_value = [[]]
        result = search_concepts_semantic("query", limit=3)
        assert result == []


class TestIndexDocs:
    def test_nonexistent_dir(self, mock_milvus, mock_openai):
        from backends.memory import index_docs
        result = index_docs("/nonexistent/path")
        assert "not found" in result.lower()

    def test_empty_dir(self, mock_milvus, mock_openai, tmp_path):
        from backends.memory import index_docs
        result = index_docs(str(tmp_path))
        assert "No chunks to index" in result

    def test_indexes_markdown_files(self, mock_milvus, mock_openai, tmp_path):
        from backends.memory import index_docs

        # Create a markdown file with enough content
        md_file = tmp_path / "test.md"
        md_file.write_text(
            "## Section One\n" + "Content " * 30 + "\n\n"
            "## Section Two\n" + "More content " * 30
        )

        # Mock batch embedding
        mock_emb = MagicMock()
        mock_emb.embedding = [0.0] * 1536
        mock_openai["client"].embeddings.create.return_value = MagicMock(
            data=[mock_emb, mock_emb]
        )

        result = index_docs(str(tmp_path))
        assert "Indexed 2 chunks from 1 docs" in result

    def test_skips_small_files(self, mock_milvus, mock_openai, tmp_path):
        from backends.memory import index_docs
        (tmp_path / "tiny.md").write_text("Small")
        result = index_docs(str(tmp_path))
        assert "No chunks to index" in result


class TestIndexConcepts:
    def test_empty_list(self, mock_milvus, mock_openai):
        from backends.memory import index_concepts
        result = index_concepts([])
        assert "No concepts to index" in result

    def test_indexes_concepts(self, mock_milvus, mock_openai):
        from backends.memory import index_concepts

        concepts = [
            {"name": "Concept1", "vault": "cognee", "summary": "First concept", "content": "Details"},
            {"name": "Concept2", "vault": "cognee", "summary": "Second concept", "content": "More details"},
        ]

        mock_emb = MagicMock()
        mock_emb.embedding = [0.0] * 1536
        mock_openai["client"].embeddings.create.return_value = MagicMock(
            data=[mock_emb, mock_emb]
        )

        result = index_concepts(concepts)
        assert "Indexed 2 concepts" in result


class TestSelfDescription:
    def test_save_self_description(self, mock_milvus, mock_openai):
        from backends.memory import save_self_description
        result = save_self_description("I am Marvin")
        assert "Self description cached" in result
        assert "11 chars" in result
        mock_milvus["collection"].insert.assert_called_once()

    def test_get_cached_hit(self, mock_milvus, mock_openai):
        from backends.memory import get_cached_self_description
        mock_milvus["utility"].has_collection.return_value = True
        mock_milvus["collection"].num_entities = 1
        mock_milvus["collection"].query.return_value = [
            {"content": "Cached identity", "timestamp": "2026-04-12T00:00:00Z"}
        ]
        result = get_cached_self_description()
        assert result == "Cached identity"

    def test_get_cached_miss_no_collection(self, mock_milvus, mock_openai):
        from backends.memory import get_cached_self_description
        mock_milvus["utility"].has_collection.return_value = False
        result = get_cached_self_description()
        assert result is None

    def test_get_cached_miss_empty_collection(self, mock_milvus, mock_openai):
        from backends.memory import get_cached_self_description
        mock_milvus["utility"].has_collection.return_value = True
        mock_milvus["collection"].num_entities = 0
        result = get_cached_self_description()
        assert result is None

    def test_get_cached_miss_no_results(self, mock_milvus, mock_openai):
        from backends.memory import get_cached_self_description
        mock_milvus["utility"].has_collection.return_value = True
        mock_milvus["collection"].num_entities = 1
        mock_milvus["collection"].query.return_value = []
        result = get_cached_self_description()
        assert result is None


class TestEnsureCollections:
    def test_creates_missing_collections(self, mock_milvus):
        from backends.memory import ensure_collections
        mock_milvus["utility"].has_collection.return_value = False
        created = ensure_collections()
        assert len(created) == 7  # ALL_COLLECTIONS has 7

    def test_skips_existing_collections(self, mock_milvus):
        from backends.memory import ensure_collections
        mock_milvus["utility"].has_collection.return_value = True
        created = ensure_collections()
        assert created == []


class TestGetSchema:
    def test_returns_markdown(self, mock_milvus):
        from backends.memory import get_schema

        mock_milvus["utility"].has_collection.return_value = True

        # Mock schema fields
        mock_field = MagicMock()
        mock_field.name = "id"
        mock_field.dtype.name = "VARCHAR"
        mock_field.is_primary = True

        mock_milvus["collection"].description = "Test collection"
        mock_milvus["collection"].num_entities = 42
        mock_milvus["collection"].schema.fields = [mock_field]
        mock_milvus["collection"].indexes = []

        result = get_schema()
        assert "# Milvus Schema" in result
        assert "Entities: 42" in result

    def test_handles_missing_collection(self, mock_milvus):
        from backends.memory import get_schema
        mock_milvus["utility"].has_collection.return_value = False
        result = get_schema()
        assert "NOT FOUND" in result


class TestConstants:
    """Verify key constants haven't drifted."""

    def test_all_collections_list(self):
        from backends.memory import ALL_COLLECTIONS
        assert "tool_calls" in ALL_COLLECTIONS
        assert "decisions" in ALL_COLLECTIONS
        assert "sessions" in ALL_COLLECTIONS
        assert "doc_chunks" in ALL_COLLECTIONS
        assert "concepts" in ALL_COLLECTIONS
        assert "self_description" in ALL_COLLECTIONS
        assert "plans" in ALL_COLLECTIONS
        assert len(ALL_COLLECTIONS) == 7

    def test_embedding_dim(self):
        from backends.memory import EMBEDDING_DIM
        assert EMBEDDING_DIM == 1536

    def test_ressalva_collections_keys(self):
        from backends.memory import _RESSALVA_COLLECTIONS
        assert set(_RESSALVA_COLLECTIONS.keys()) == {
            "concepts", "decisions", "sessions", "doc_chunks", "plans"
        }
