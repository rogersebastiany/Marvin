"""
Tests for cognify_vaults.py — locking current behavior as a TDD safety net.

Pure functions (build_custom_prompt, EDGE_NORMALIZE) tested directly.
Filesystem functions (collect_texts, collect_changed_texts) tested with tmp_path.
Async pipeline functions (run, run_incremental, post_process_edges) require
Cognee/Neo4j and are not tested here.
"""

import json
import pytest
from unittest.mock import patch
from pathlib import Path


# ── EDGE_NORMALIZE ──────────────────────────────────────────────────────────


class TestEdgeNormalize:
    def test_direct_lowercase_maps(self):
        from cognify_vaults import EDGE_NORMALIZE, RELATION_TYPES
        for type_name in RELATION_TYPES:
            assert EDGE_NORMALIZE[type_name.lower()] == type_name

    def test_common_cognee_defaults(self):
        from cognify_vaults import EDGE_NORMALIZE
        assert EDGE_NORMALIZE["contains"] == "COMPOSES"
        assert EDGE_NORMALIZE["is_part_of"] == "COMPOSES"
        assert EDGE_NORMALIZE["is_a"] == "EXEMPLIFIES"
        assert EDGE_NORMALIZE["depends_on"] == "REQUIRES"
        assert EDGE_NORMALIZE["uses"] == "REQUIRES"
        assert EDGE_NORMALIZE["supports"] == "ENABLES"

    def test_llm_typos_mapped(self):
        from cognify_vaults import EDGE_NORMALIZE
        assert EDGE_NORMALIZE["implementis"] == "IMPLEMENTS"
        assert EDGE_NORMALIZE["impliments"] == "IMPLEMENTS"
        assert EDGE_NORMALIZE["enebles"] == "ENABLES"
        assert EDGE_NORMALIZE["defenes"] == "DEFINES"

    def test_all_values_are_valid_relation_types(self):
        from cognify_vaults import EDGE_NORMALIZE, RELATION_TYPES
        valid = set(RELATION_TYPES.keys())
        for key, value in EDGE_NORMALIZE.items():
            assert value in valid, f"EDGE_NORMALIZE['{key}'] = '{value}' not in RELATION_TYPES"

    def test_symmetric_mappings(self):
        from cognify_vaults import EDGE_NORMALIZE
        assert EDGE_NORMALIZE["opposes"] == "CONTRADICTS"
        assert EDGE_NORMALIZE["similar_to"] == "ANALOGOUS_TO"


# ── build_custom_prompt ─────────────────────────────────────────────────────


class TestBuildCustomPrompt:
    def test_includes_extraction_rules(self):
        from cognify_vaults import build_custom_prompt
        prompt = build_custom_prompt()
        assert "knowledge graph extraction" in prompt
        assert "Concept" in prompt
        assert "relates_to" in prompt

    def test_includes_relation_types(self):
        from cognify_vaults import build_custom_prompt, RELATION_TYPES
        prompt = build_custom_prompt()
        for type_name in RELATION_TYPES:
            if type_name != "RELATES_TO":
                assert type_name.lower() in prompt

    def test_discourages_relates_to(self):
        from cognify_vaults import build_custom_prompt
        prompt = build_custom_prompt()
        assert "last resort" in prompt

    def test_mentions_symmetric_types(self):
        from cognify_vaults import build_custom_prompt
        prompt = build_custom_prompt()
        assert "Symmetric" in prompt or "symmetric" in prompt

    def test_preserves_language_instruction(self):
        from cognify_vaults import build_custom_prompt
        prompt = build_custom_prompt()
        assert "Do NOT translate" in prompt


# ── collect_texts ───────────────────────────────────────────────────────────


class TestCollectTexts:
    def test_collects_from_vaults(self, tmp_path):
        from cognify_vaults import collect_texts
        vault = tmp_path / "thesis"
        vault.mkdir()
        (vault / "concept.md").write_text("x" * 200, encoding="utf-8")
        (vault / "short.md").write_text("tiny", encoding="utf-8")

        with patch("cognify_vaults.VAULTS", {"thesis": vault}), \
             patch("cognify_vaults.DOCS_DIR", tmp_path / "nonexistent"):
            texts = collect_texts()
            assert len(texts) == 1
            assert texts[0][0] == "thesis/concept"

    def test_skips_short_files(self, tmp_path):
        from cognify_vaults import collect_texts
        vault = tmp_path / "v"
        vault.mkdir()
        (vault / "short.md").write_text("x" * 50, encoding="utf-8")

        with patch("cognify_vaults.VAULTS", {"v": vault}), \
             patch("cognify_vaults.DOCS_DIR", tmp_path / "nonexistent"):
            texts = collect_texts()
            assert len(texts) == 0

    def test_collects_docs(self, tmp_path):
        from cognify_vaults import collect_texts
        docs = tmp_path / "docs"
        docs.mkdir()
        (docs / "guide.md").write_text("y" * 300, encoding="utf-8")

        with patch("cognify_vaults.VAULTS", {}), \
             patch("cognify_vaults.DOCS_DIR", docs):
            texts = collect_texts()
            assert len(texts) == 1
            assert texts[0][0] == "docs/guide"

    def test_docs_min_length_200(self, tmp_path):
        from cognify_vaults import collect_texts
        docs = tmp_path / "docs"
        docs.mkdir()
        (docs / "short.md").write_text("y" * 150, encoding="utf-8")

        with patch("cognify_vaults.VAULTS", {}), \
             patch("cognify_vaults.DOCS_DIR", docs):
            texts = collect_texts()
            assert len(texts) == 0

    def test_skips_missing_vaults(self, tmp_path):
        from cognify_vaults import collect_texts
        with patch("cognify_vaults.VAULTS", {"missing": tmp_path / "nope"}), \
             patch("cognify_vaults.DOCS_DIR", tmp_path / "nonexistent"):
            texts = collect_texts()
            assert len(texts) == 0


# ── collect_changed_texts ───────────────────────────────────────────────────


class TestCollectChangedTexts:
    def test_collects_changed_files(self, tmp_path):
        from cognify_vaults import collect_changed_texts
        vault = tmp_path / "thesis"
        vault.mkdir()
        (vault / "changed.md").write_text("z" * 200, encoding="utf-8")

        with patch("cognify_vaults.ROOT", tmp_path), \
             patch("cognify_vaults._PATH_TO_VAULT", [(vault, "thesis")]):
            texts = collect_changed_texts(["thesis/changed.md"])
            assert len(texts) == 1
            assert texts[0][0] == "thesis/changed"

    def test_skips_non_md(self, tmp_path):
        from cognify_vaults import collect_changed_texts
        (tmp_path / "file.txt").write_text("x" * 200)

        with patch("cognify_vaults.ROOT", tmp_path):
            texts = collect_changed_texts(["file.txt"])
            assert len(texts) == 0

    def test_skips_missing_files(self, tmp_path):
        from cognify_vaults import collect_changed_texts
        with patch("cognify_vaults.ROOT", tmp_path):
            texts = collect_changed_texts(["nonexistent.md"])
            assert len(texts) == 0

    def test_skips_short_files(self, tmp_path):
        from cognify_vaults import collect_changed_texts
        (tmp_path / "short.md").write_text("tiny")

        with patch("cognify_vaults.ROOT", tmp_path):
            texts = collect_changed_texts(["short.md"])
            assert len(texts) == 0


# ── Constants ───────────────────────────────────────────────────────────────


class TestConstants:
    def test_relation_types_loaded(self):
        from cognify_vaults import RELATION_TYPES
        assert len(RELATION_TYPES) == 16
        assert "RELATES_TO" in RELATION_TYPES
        assert "IMPLEMENTS" in RELATION_TYPES

    def test_vaults_has_expected_keys(self):
        from cognify_vaults import VAULTS
        assert "thesis" in VAULTS
        assert "implementation" in VAULTS

    def test_relation_types_path(self):
        from cognify_vaults import RELATION_TYPES_PATH
        assert RELATION_TYPES_PATH.exists()
        assert RELATION_TYPES_PATH.name == "relation_types.json"
