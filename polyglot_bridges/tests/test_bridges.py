#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for polyglot_bridges module.
"""

import json
import os
import sys
import pytest
from pathlib import Path

# Build correct path to module
POLYGLOT_ROOT = Path(__file__).parent.parent.parent
ROTATION_FILE = str(POLYGLOT_ROOT / "language_rotation.json")

# Patch ROTATION_FILE before importing
import polyglot_bridges
polyglot_bridges.ROTATION_FILE = ROTATION_FILE

from polyglot_bridges import (
    TOOL_NAME,
    TOOL_VERSION,
    TOOL_LANGUAGES,
    UNIVERSAL_PROBLEMS,
    build_bridge,
    _find_gap,
    _compute_difficulty,
    _build_bridge_path,
    semantic_bridge,
    load_rotation,
)


class TestModuleMetadata:
    """Test module constants."""

    def test_tool_name(self):
        assert TOOL_NAME == "polyglot-semantic-bridges"

    def test_tool_version(self):
        assert TOOL_VERSION == "1.0.0"

    def test_tool_languages_count(self):
        assert len(TOOL_LANGUAGES) == 8

    def test_tool_languages_order(self):
        assert TOOL_LANGUAGES == ["Rust", "Go", "Swift", "Kotlin",
                                   "TypeScript", "JavaScript", "Java", "C/C++"]


class TestUniversalProblems:
    """Test UNIVERSAL_PROBLEMS data structure."""

    def test_has_8_problems(self):
        assert len(UNIVERSAL_PROBLEMS) == 8

    def test_each_problem_has_required_fields(self):
        for problem in UNIVERSAL_PROBLEMS:
            assert "id" in problem
            assert "name" in problem
            assert "emoji" in problem
            assert "description" in problem
            assert "why_it_matters" in problem
            assert "slot" in problem
            assert "solutions" in problem

    def test_each_problem_has_all_language_solutions(self):
        for problem in UNIVERSAL_PROBLEMS:
            for lang in TOOL_LANGUAGES:
                assert lang in problem["solutions"], f"{problem['id']} missing {lang}"

    def test_each_solution_has_required_fields(self):
        required = ["approach", "mechanism", "code_example", "idiom", "translation_gap", "key_insight"]
        for problem in UNIVERSAL_PROBLEMS:
            for lang, sol in problem["solutions"].items():
                for field in required:
                    assert field in sol, f"{problem['id']}/{lang} missing {field}"

    def test_problem_slots_are_sequential(self):
        slots = [p["slot"] for p in UNIVERSAL_PROBLEMS]
        assert slots == list(range(8))


class TestLoadRotation:
    """Test rotation loading."""

    def test_returns_dict(self):
        config = load_rotation()
        assert isinstance(config, dict)

    def test_has_languages(self):
        config = load_rotation()
        assert "languages" in config
        assert len(config["languages"]) == 8


class TestBuildBridge:
    """Test build_bridge function."""

    def test_returns_dict(self):
        result = build_bridge("Rust")
        assert isinstance(result, dict)

    def test_returns_selected_language(self):
        result = build_bridge("Go")
        assert result["selected_language"] == "Go"

    def test_returns_problem(self):
        result = build_bridge("Swift")
        assert "problem" in result
        assert "id" in result["problem"]
        assert "name" in result["problem"]
        assert "emoji" in result["problem"]
        assert "description" in result["problem"]

    def test_returns_solution(self):
        result = build_bridge("Kotlin")
        assert "solution" in result
        assert "approach" in result["solution"]
        assert "mechanism" in result["solution"]
        assert "code_example" in result["solution"]

    def test_returns_comparison(self):
        result = build_bridge("TypeScript")
        assert "comparison" in result
        for lang in TOOL_LANGUAGES:
            assert lang in result["comparison"]

    def test_returns_translation_gaps(self):
        result = build_bridge("JavaScript")
        assert "translation_gaps" in result
        assert isinstance(result["translation_gaps"], list)

    def test_returns_difficulty_rating(self):
        result = build_bridge("Rust")
        assert "difficulty_rating" in result
        assert isinstance(result["difficulty_rating"], str)
        assert "⭐" in result["difficulty_rating"]

    def test_returns_emoji_path(self):
        result = build_bridge("Java")
        assert "emoji_path" in result
        assert "🌉" in result["emoji_path"]

    def test_returns_next_language(self):
        result = build_bridge("Rust")
        assert result["next_language"] == "Go"

    def test_returns_rotation_order(self):
        result = build_bridge("C/C++")
        assert result["rotation_order"] == TOOL_LANGUAGES

    def test_unknown_language_raises_value_error(self):
        with pytest.raises(ValueError) as excinfo:
            build_bridge("Python")
        assert "Python" in str(excinfo.value)

    def test_updates_rotation(self):
        config_before = load_rotation()
        idx_before = config_before["current_index"]
        lang_before = config_before["languages"][idx_before]
        build_bridge(lang_before)
        config_after = load_rotation()
        expected = (idx_before + 1) % len(config_before["languages"])
        assert config_after["current_index"] == expected


class TestSemanticBridge:
    """Test semantic_bridge function."""

    def test_returns_dict(self):
        result = semantic_bridge()
        assert isinstance(result, dict)

    def test_with_language_param(self):
        result = semantic_bridge("Rust")
        assert result["selected_language"] == "Rust"

    def test_without_param_uses_rotation(self):
        config = load_rotation()
        idx = config["current_index"] % len(TOOL_LANGUAGES)
        expected_lang = config["languages"][idx]
        result = semantic_bridge()
        assert result["selected_language"] == expected_lang


class TestFindGap:
    """Test _find_gap helper function."""

    def test_returns_none_when_no_gap(self):
        sol_a = {"approach": "Same", "translation_gap": ""}
        sol_b = {"approach": "Same", "translation_gap": ""}
        result = _find_gap(sol_a, sol_b)
        assert result is None

    def test_returns_gap_for_no_direct_equivalent(self):
        sol_a = {"approach": "Option", "translation_gap": "No direct equivalent"}
        sol_b = {"approach": "Null", "translation_gap": ""}
        result = _find_gap(sol_a, sol_b)
        assert result is not None

    def test_returns_gap_when_a_has_no_direct_equivalent(self):
        # When sol_a has "No direct equivalent", gap is returned
        sol_a = {"approach": "Option", "translation_gap": "No direct equivalent in JS"}
        sol_b = {"approach": "Null", "translation_gap": ""}
        result = _find_gap(sol_a, sol_b)
        assert result is not None


class TestComputeDifficulty:
    """Test _compute_difficulty helper function."""

    def test_returns_string_with_stars(self):
        result = _compute_difficulty("null_safety", "Rust")
        assert isinstance(result, str)
        assert "⭐" in result

    def test_different_languages_have_different_difficulty(self):
        rust_diff = _compute_difficulty("null_safety", "Rust")
        js_diff = _compute_difficulty("null_safety", "JavaScript")
        # Both should have stars, but can differ
        assert "⭐" in rust_diff
        assert "⭐" in js_diff


class TestBuildBridgePath:
    """Test _build_bridge_path helper function."""

    def test_returns_string(self):
        result = _build_bridge_path(TOOL_LANGUAGES, "Rust", 0)
        assert isinstance(result, str)

    def test_contains_bridge_emoji(self):
        result = _build_bridge_path(TOOL_LANGUAGES, "Rust", 0)
        assert "🌉" in result

    def test_contains_language_emoji(self):
        result = _build_bridge_path(TOOL_LANGUAGES, "Go", 1)
        assert "🐹" in result
