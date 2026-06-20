#!/usr/bin/env python3
"""Tests for polyglot_reef module."""

import json
import os
import sys
import tempfile
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from reef import (
    TOOL_NAME,
    TOOL_VERSION,
    LANGUAGE_SPECIES,
    NICHE_DESCRIPTIONS,
    ROLE_DESCRIPTIONS,
    REEF_CONDITIONS,
    analyze_species,
    get_ecosystem_report,
    format_reef_report,
    load_rotation,
    save_rotation,
    compute_next_index,
)


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def make_temp_config(languages=None, current_index=0):
    """Create a temp rotation config and return its path."""
    data = {
        "languages": languages or ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"],
        "current_index": current_index,
        "last_language": None,
        "updated_at": "2026-06-19T00:00:00+08:00",
    }
    fd, path = tempfile.mkstemp(suffix=".json")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    return path


# ─────────────────────────────────────────────────────────────────────────────
# Tests: compute_next_index
# ─────────────────────────────────────────────────────────────────────────────

class TestComputeNextIndex:
    def test_basic_increment(self):
        assert compute_next_index(0, ["A", "B", "C"]) == 1
        assert compute_next_index(1, ["A", "B", "C"]) == 2
        assert compute_next_index(2, ["A", "B", "C"]) == 0  # wraps

    def test_wrap_around(self):
        assert compute_next_index(7, ["A", "B", "C", "D", "E", "F", "G", "H"]) == 0

    def test_single_element(self):
        assert compute_next_index(0, ["Only"]) == 0


# ─────────────────────────────────────────────────────────────────────────────
# Tests: Rotation file I/O
# ─────────────────────────────────────────────────────────────────────────────

class TestRotationIO:
    def test_save_and_load(self):
        path = make_temp_config()
        try:
            data = {"languages": ["X", "Y"], "current_index": 1, "last_language": "X", "updated_at": "2026-06-19T00:00:00+08:00"}
            save_rotation(data, path)
            loaded = load_rotation(path)
            assert loaded["languages"] == ["X", "Y"]
            assert loaded["current_index"] == 1
            assert loaded["last_language"] == "X"
        finally:
            os.unlink(path)

    def test_load_rotation_returns_dict(self):
        path = make_temp_config(languages=["Rust", "Go"], current_index=1)
        try:
            result = load_rotation(path)
            assert isinstance(result, dict)
            assert "languages" in result
            assert "current_index" in result
        finally:
            os.unlink(path)


# ─────────────────────────────────────────────────────────────────────────────
# Tests: analyze_species
# ─────────────────────────────────────────────────────────────────────────────

class TestAnalyzeSpecies:
    def test_known_language_returns_data(self):
        for lang in ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"]:
            result = analyze_species(lang)
            assert result is not None, f"analyze_species returned None for {lang}"
            assert result["language"] == lang
            assert "scientific_name" in result
            assert "niche" in result
            assert "traits" in result
            assert "trait_bars" in result
            assert "reef_impact" in result
            assert "fun_fact" in result
            assert "conservation_status" in result

    def test_unknown_language_returns_none(self):
        assert analyze_species("Brainfuck") is None
        assert analyze_species("COBOL") is None
        assert analyze_species("") is None

    def test_all_languages_have_all_trait_keys(self):
        expected_traits = {"safety", "speed", "ergonomics", "concurrency", "type_safety"}
        for lang, data in LANGUAGE_SPECIES.items():
            assert set(data["traits"].keys()) == expected_traits, f"{lang} missing traits"

    def test_trait_values_in_range(self):
        for lang, data in LANGUAGE_SPECIES.items():
            for trait, value in data["traits"].items():
                assert 0 <= value <= 10, f"{lang}.{trait} = {value} out of range [0,10]"

    def test_trait_bars_are_correct_length(self):
        for lang in LANGUAGE_SPECIES:
            result = analyze_species(lang)
            for trait, bar in result["trait_bars"].items():
                assert len(bar) == 10, f"{lang}.{trait} bar length = {len(bar)}, expected 10"

    def test_role_types_are_valid(self):
        valid_roles = {"keystone", "apex", "indicator", "invasive", "stable"}
        for lang in LANGUAGE_SPECIES:
            result = analyze_species(lang)
            assert result["role_type"] in valid_roles, f"{lang} has invalid role_type {result['role_type']}"


# ─────────────────────────────────────────────────────────────────────────────
# Tests: get_ecosystem_report
# ─────────────────────────────────────────────────────────────────────────────

class TestEcosystemReport:
    def test_report_contains_required_keys(self):
        path = make_temp_config(current_index=0)
        try:
            report = get_ecosystem_report(rotate=False, config_path=path)
            required = {
                "tool_name", "tool_version", "current_language", "current_index",
                "rotated", "species", "reef_health", "reef_conditions",
                "niche_descriptions", "role_descriptions",
            }
            assert required.issubset(report.keys()), f"Missing keys: {required - report.keys()}"
        finally:
            os.unlink(path)

    def test_report_without_rotate_does_not_change_index(self):
        path = make_temp_config(languages=["Rust", "Go"], current_index=1)
        try:
            get_ecosystem_report(rotate=False, config_path=path)
            data = load_rotation(path)
            assert data["current_index"] == 1
        finally:
            os.unlink(path)

    def test_report_with_rotate_updates_index(self):
        path = make_temp_config(languages=["Rust", "Go", "Swift"], current_index=0)
        try:
            report = get_ecosystem_report(rotate=True, config_path=path)
            data = load_rotation(path)
            assert data["current_index"] == 1
            assert data["last_language"] == "Rust"
            assert report["rotated"] is True
            assert report["new_index"] == 1
        finally:
            os.unlink(path)

    def test_report_wraps_at_end_of_list(self):
        path = make_temp_config(languages=["A", "B", "C"], current_index=2)
        try:
            report = get_ecosystem_report(rotate=True, config_path=path)
            data = load_rotation(path)
            assert data["current_index"] == 0
            assert report["new_index"] == 0
        finally:
            os.unlink(path)

    def test_species_analysis_in_report(self):
        path = make_temp_config(languages=["Rust", "Go"], current_index=0)
        try:
            report = get_ecosystem_report(rotate=False, config_path=path)
            assert report["current_language"] == "Rust"
            species = report["species"]
            assert species["language"] == "Rust"
            assert "avg_fitness" in species
            assert "niche_breadth" in species
        finally:
            os.unlink(path)

    def test_reef_health_in_report(self):
        path = make_temp_config()
        try:
            report = get_ecosystem_report(rotate=False, config_path=path)
            health = report["reef_health"]
            assert "score" in health
            assert "label" in health
            assert "emoji" in health
            assert 0 <= health["score"] <= 100
        finally:
            os.unlink(path)

    def test_reef_conditions_in_report(self):
        path = make_temp_config()
        try:
            report = get_ecosystem_report(rotate=False, config_path=path)
            assert isinstance(report["reef_conditions"], list)
            assert all("name" in c for c in report["reef_conditions"])
        finally:
            os.unlink(path)


# ─────────────────────────────────────────────────────────────────────────────
# Tests: format_reef_report
# ─────────────────────────────────────────────────────────────────────────────

class TestFormatReefReport:
    def test_formats_without_error(self):
        path = make_temp_config(current_index=0)
        try:
            report = get_ecosystem_report(rotate=False, config_path=path)
            card = format_reef_report(report)
            assert isinstance(card, str)
            assert len(card) > 0
            assert "POLYGLOT REEF" in card
            assert report["current_language"] in card
        finally:
            os.unlink(path)

    def test_formatted_card_contains_species_info(self):
        path = make_temp_config(languages=["Rust"], current_index=0)
        try:
            report = get_ecosystem_report(rotate=False, config_path=path)
            card = format_reef_report(report)
            assert "Rust" in card
            assert "TRAIT PROFILE" in card
            assert "REEF HEALTH" in card
            assert "FUN FACT" in card
        finally:
            os.unlink(path)


# ─────────────────────────────────────────────────────────────────────────────
# Tests: full rotation cycle
# ─────────────────────────────────────────────────────────────────────────────

class TestFullRotationCycle:
    def test_full_cycle_through_all_languages(self):
        """Simulate a full rotation cycle to verify index management."""
        languages = ["Rust", "Go", "Swift"]
        path = make_temp_config(languages=languages, current_index=0)
        try:
            seen = {}
            for i in range(len(languages) + 2):
                report = get_ecosystem_report(rotate=True, config_path=path)
                lang = report["current_language"]
                seen[lang] = seen.get(lang, 0) + 1
                data = load_rotation(path)
                # After i iterations, should be at index (i+1) % 3
                assert data["current_index"] == (i + 1) % len(languages), \
                    f"i={i}: expected {(i+1)%3}, got {data['current_index']}"

            # After 5 iterations over 3 languages: Rust=2, Go=2, Swift=1
            assert seen == {"Rust": 2, "Go": 2, "Swift": 1}
        finally:
            os.unlink(path)

    def test_no_duplicate_consecutive_languages(self):
        """Verify no language repeats consecutively in rotation."""
        languages = ["Rust", "Go", "Swift", "Kotlin", "TypeScript",
                      "JavaScript", "Java", "C/C++"]
        path = make_temp_config(languages=languages, current_index=0)
        try:
            last_lang = None
            for _ in range(24):
                report = get_ecosystem_report(rotate=True, config_path=path)
                lang = report["current_language"]
                assert lang != last_lang, f"Duplicate consecutive: {lang}"
                last_lang = lang
        finally:
            os.unlink(path)


# ─────────────────────────────────────────────────────────────────────────────
# Tests: Module-level constants
# ─────────────────────────────────────────────────────────────────────────────

class TestModuleConstants:
    def test_tool_name_and_version(self):
        assert TOOL_NAME == "polyglot-reef"
        assert TOOL_VERSION == "1.0.0"

    def test_all_8_languages_in_species_db(self):
        expected = {"Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"}
        assert set(LANGUAGE_SPECIES.keys()) == expected

    def test_niche_descriptions_populated(self):
        expected_niches = {"Systems", "Web", "Mobile", "Cloud", "Enterprise", "Data", "Embedded"}
        assert set(NICHE_DESCRIPTIONS.keys()) == expected_niches

    def test_role_descriptions_populated(self):
        expected_roles = {"keystone", "apex", "indicator", "invasive", "stable"}
        assert set(ROLE_DESCRIPTIONS.keys()) == expected_roles

    def test_reef_conditions_not_empty(self):
        assert len(REEF_CONDITIONS) > 0
        assert all("name" in c and "description" in c for c in REEF_CONDITIONS)
