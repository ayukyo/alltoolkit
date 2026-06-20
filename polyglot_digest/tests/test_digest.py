#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for polyglot_digest module.
"""

import json
import os
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

# Add parent to path so we can import polyglot_digest
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from polyglot_digest import (
    TOOL_NAME,
    TOOL_VERSION,
    CONCEPT_BANK,
    ROTATION_FILE,
    load_rotation,
    save_rotation,
    get_concept,
    get_all_concept_keys,
    select_concept,
    build_parallel_snippet,
    digest,
)


ALL_LANGS = [
    "Rust",
    "Go",
    "Swift",
    "Kotlin",
    "TypeScript",
    "JavaScript",
    "Java",
    "C/C++",
]

EXPECTED_CONCEPT_KEYS = [
    "hello_world",
    "fn_fibonacci",
    "fn_http_get",
    "pattern_singleton",
    "fn_error_handling",
    "fn_generic_stack",
]


@pytest.fixture
def restore_rotation():
    """Snapshot and restore the rotation file."""
    snapshot = None
    if os.path.exists(ROTATION_FILE):
        with open(ROTATION_FILE, "r") as f:
            snapshot = f.read()
    yield
    if snapshot is not None:
        with open(ROTATION_FILE, "w") as f:
            f.write(snapshot)


class TestModuleMetadata:
    """Test module-level constants."""

    def test_tool_name(self):
        assert TOOL_NAME == "polyglot-digest"

    def test_tool_version(self):
        assert TOOL_VERSION == "1.0.0"

    def test_rotation_file_path(self):
        assert ROTATION_FILE.endswith("language_rotation.json")


class TestConceptBank:
    """Test CONCEPT_BANK data structure."""

    def test_all_expected_concepts_present(self):
        for key in EXPECTED_CONCEPT_KEYS:
            assert key in CONCEPT_BANK, f"Missing concept: {key}"

    def test_concept_count(self):
        assert len(CONCEPT_BANK) >= 6

    def test_each_concept_has_required_fields(self):
        for key, concept in CONCEPT_BANK.items():
            assert "title" in concept, f"{key} missing title"
            assert "description" in concept, f"{key} missing description"
            assert "tags" in concept, f"{key} missing tags"
            assert isinstance(concept["title"], str)
            assert isinstance(concept["description"], str)
            assert isinstance(concept["tags"], list)
            assert len(concept["title"]) > 0
            assert len(concept["description"]) > 0

    def test_each_concept_has_all_languages(self):
        for key, concept in CONCEPT_BANK.items():
            for lang in ALL_LANGS:
                assert lang in concept, f"{key} missing {lang}"
                assert isinstance(concept[lang], str)
                assert len(concept[lang]) > 0


class TestGetConcept:
    """Test get_concept function."""

    def test_returns_existing_concept(self):
        concept = get_concept("hello_world")
        assert concept is not None
        assert "title" in concept

    def test_returns_none_for_missing(self):
        concept = get_concept("nonexistent_concept_key")
        assert concept is None


class TestGetAllConceptKeys:
    """Test get_all_concept_keys function."""

    def test_returns_list(self):
        keys = get_all_concept_keys()
        assert isinstance(keys, list)
        assert len(keys) >= 6

    def test_contains_known_keys(self):
        keys = get_all_concept_keys()
        assert "hello_world" in keys


class TestSelectConcept:
    """Test select_concept function."""

    def test_returns_string(self):
        key = select_concept()
        assert isinstance(key, str)
        assert key in CONCEPT_BANK

    def test_forced_key_used(self):
        key = select_concept(forced_key="hello_world")
        assert key == "hello_world"

    def test_forced_invalid_key_falls_back(self):
        # Should still return something valid
        key = select_concept(forced_key="not_a_real_key")
        assert key in CONCEPT_BANK


class TestBuildParallelSnippet:
    """Test build_parallel_snippet function."""

    def test_returns_dict_for_known_concept(self):
        result = build_parallel_snippet("hello_world", ALL_LANGS)
        assert isinstance(result, dict)
        for lang in ALL_LANGS:
            assert lang in result
            assert isinstance(result[lang], str)

    def test_returns_none_for_unknown_concept(self):
        result = build_parallel_snippet("nonexistent", ALL_LANGS)
        assert result is None

    def test_partial_languages(self):
        result = build_parallel_snippet("hello_world", ["Rust", "Go"])
        assert "Rust" in result
        assert "Go" in result
        assert "Java" not in result

    def test_empty_languages_list(self):
        result = build_parallel_snippet("hello_world", [])
        assert isinstance(result, dict)
        assert len(result) == 0


class TestLoadSaveRotation:
    """Test rotation file IO."""

    def test_load_returns_dict(self, restore_rotation):
        config = load_rotation()
        assert isinstance(config, dict)

    def test_save_roundtrip(self, restore_rotation, tmp_path):
        test_file = tmp_path / "rotation.json"
        data = {"languages": ["A", "B"], "current_index": 1}
        with patch.object(
            sys.modules["polyglot_digest"], "ROTATION_FILE", str(test_file)
        ):
            save_rotation(data)
            assert test_file.exists()
            with open(test_file) as f:
                loaded = json.load(f)
            assert loaded == data


class TestDigest:
    """Test the main digest() function."""

    def test_returns_dict(self, restore_rotation):
        result = digest(concept_key="hello_world")
        assert isinstance(result, dict)

    def test_has_required_keys(self, restore_rotation):
        result = digest(concept_key="hello_world")
        expected = [
            "tool", "version", "selected_language", "next_language",
            "concept", "snippets", "rotation", "timestamp"
        ]
        for key in expected:
            assert key in result, f"Missing key: {key}"

    def test_tool_metadata(self, restore_rotation):
        result = digest(concept_key="hello_world")
        assert result["tool"] == "polyglot-digest"
        assert result["version"] == "1.0.0"

    def test_concept_key_used(self, restore_rotation):
        result = digest(concept_key="hello_world")
        assert result["concept"]["key"] == "hello_world"
        assert result["concept"]["title"] == "Hello, World!"

    def test_snippets_contain_all_languages(self, restore_rotation):
        result = digest(concept_key="hello_world")
        for lang in ALL_LANGS:
            assert lang in result["snippets"]
            assert isinstance(result["snippets"][lang], str)
            assert len(result["snippets"][lang]) > 0

    def test_language_override(self, restore_rotation):
        result = digest(language="Go", concept_key="hello_world")
        assert result["selected_language"] == "Go"

    def test_rotation_advances(self, restore_rotation):
        before = load_rotation()
        idx_before = before["current_index"]
        digest(language=before["languages"][idx_before], concept_key="hello_world")
        after = load_rotation()
        expected = (idx_before + 1) % len(after["languages"])
        assert after["current_index"] == expected

    def test_next_language_is_valid(self, restore_rotation):
        for lang in ALL_LANGS:
            result = digest(language=lang, concept_key="hello_world")
            assert result["selected_language"] == lang
            assert result["next_language"] in result["rotation"]
            sel_idx = result["rotation"].index(result["selected_language"])
            expected_next = result["rotation"][(sel_idx + 1) % len(result["rotation"])]
            assert result["next_language"] == expected_next

    def test_random_concept_selection(self, restore_rotation):
        # Just verify concept selection produces valid output
        result = digest(language="Rust")
        assert result["concept"]["key"] in CONCEPT_BANK
        assert "title" in result["concept"]
        assert "description" in result["concept"]

    def test_result_is_json_serializable(self, restore_rotation):
        result = digest(concept_key="hello_world")
        json_str = json.dumps(result, ensure_ascii=False)
        loaded = json.loads(json_str)
        assert loaded["selected_language"] == result["selected_language"]
        assert loaded["concept"]["key"] == "hello_world"

    @pytest.mark.parametrize("concept_key", EXPECTED_CONCEPT_KEYS)
    def test_digest_for_each_concept(self, concept_key, restore_rotation):
        result = digest(concept_key=concept_key, language="Rust")
        assert result["concept"]["key"] == concept_key
        assert "Rust" in result["snippets"]
        assert len(result["snippets"]["Rust"]) > 0
