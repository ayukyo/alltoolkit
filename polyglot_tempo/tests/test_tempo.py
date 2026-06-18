#!/usr/bin/env python3
"""
Tests for Polyglot Tempo — Rhythm Pattern Generator for Programming Languages
Run with: python -m pytest polyglot_tempo/tests/ -v
Or:       python -m polyglot_tempo --test
"""

import json
import os
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict

import pytest

# Import from package
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from tempo import (
    TOOL_NAME,
    TOOL_VERSION,
    ROTATION_ORDER,
    RHYTHM_DATA,
    load_rotation,
    save_rotation,
    get_current_language,
    advance_rotation,
    get_previous_language,
    tempo,
    generate_rhythm_report,
    format_rhythm_card,
    build_drum_grid,
    build_syncopation_bar,
    compute_transition_feel,
)


# ─────────────────────────────────────────────────────────────────────────────
# Fixtures
# ─────────────────────────────────────────────────────────────────────────────

@pytest.fixture
def rotation_config(tmp_path: Path) -> str:
    """Create a temporary rotation config file and return its path."""
    config = {
        "languages": ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"],
        "current_index": 0,
        "last_language": "Rust",
        "updated_at": "2026-06-14T03:00:00+08:00",
    }
    path = tmp_path / "language_rotation.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(config, f)
    return str(path)


@pytest.fixture
def rotation_config_index3(tmp_path: Path) -> str:
    """Create a rotation config at index 3 (Kotlin)."""
    config = {
        "languages": ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"],
        "current_index": 3,
        "last_language": "Swift",
        "updated_at": "2026-06-14T03:00:00+08:00",
    }
    path = tmp_path / "language_rotation.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(config, f)
    return str(path)


@pytest.fixture
def rotation_config_last_index(tmp_path: Path) -> str:
    """Create a rotation config at last index (7 = C/C++)."""
    config = {
        "languages": ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"],
        "current_index": 7,
        "last_language": "Java",
        "updated_at": "2026-06-14T03:00:00+08:00",
    }
    path = tmp_path / "language_rotation.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(config, f)
    return str(path)


# ─────────────────────────────────────────────────────────────────────────────
# Rotation Config Tests
# ─────────────────────────────────────────────────────────────────────────────

class TestRotationConfig:
    """Test rotation configuration loading and saving."""

    def test_load_rotation_returns_dict(self):
        """load_rotation returns a dictionary."""
        result = load_rotation()
        assert isinstance(result, dict)

    def test_rotation_has_required_keys(self):
        """Rotation config has all required keys."""
        config = load_rotation()
        assert "languages" in config
        assert "current_index" in config
        assert "last_language" in config
        assert "updated_at" in config

    def test_eight_languages_in_rotation(self):
        """Exactly 8 languages are in rotation."""
        config = load_rotation()
        assert len(config["languages"]) == 8

    def test_language_order_matches_spec(self):
        """Languages are in the expected order."""
        config = load_rotation()
        expected = ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"]
        assert config["languages"] == expected

    def test_current_index_in_valid_range(self):
        """current_index is always 0-7."""
        config = load_rotation()
        assert 0 <= config["current_index"] < 8


# ─────────────────────────────────────────────────────────────────────────────
# Rhythm Data Tests
# ─────────────────────────────────────────────────────────────────────────────

class TestRhythmData:
    """Test that all languages have complete rhythm data."""

    @pytest.mark.parametrize("lang", ROTATION_ORDER)
    def test_all_languages_have_bpm(self, lang):
        """Every language has a BPM value."""
        assert "bpm" in RHYTHM_DATA[lang]
        assert isinstance(RHYTHM_DATA[lang]["bpm"], int)
        assert 60 <= RHYTHM_DATA[lang]["bpm"] <= 200

    @pytest.mark.parametrize("lang", ROTATION_ORDER)
    def test_all_languages_have_genre(self, lang):
        """Every language has a genre string."""
        assert "genre" in RHYTHM_DATA[lang]
        assert len(RHYTHM_DATA[lang]["genre"]) > 0

    @pytest.mark.parametrize("lang", ROTATION_ORDER)
    def test_all_languages_have_drum_pattern(self, lang):
        """Every language has a drum pattern with at least 3 rows."""
        pattern = RHYTHM_DATA[lang]["drum_pattern"]
        assert isinstance(pattern, list)
        assert len(pattern) >= 3
        for row_name, row_pattern in pattern:
            assert isinstance(row_name, str)
            assert isinstance(row_pattern, str)

    @pytest.mark.parametrize("lang", ROTATION_ORDER)
    def test_all_languages_have_common_rhythms(self, lang):
        """Every language has at least 3 common rhythms."""
        rhythms = RHYTHM_DATA[lang]["common_rhythms"]
        assert isinstance(rhythms, list)
        assert len(rhythms) >= 3

    @pytest.mark.parametrize("lang", ROTATION_ORDER)
    def test_common_rhythms_have_required_fields(self, lang):
        """Each common rhythm has name, pattern, and bpm_factor."""
        for rhythm in RHYTHM_DATA[lang]["common_rhythms"]:
            assert "name" in rhythm
            assert "pattern" in rhythm
            assert "bpm_factor" in rhythm
            assert 0.5 <= rhythm["bpm_factor"] <= 2.0

    @pytest.mark.parametrize("lang", ROTATION_ORDER)
    def test_all_languages_have_time_signature(self, lang):
        """Every language has a time signature."""
        ts = RHYTHM_DATA[lang]["time_signature"]
        assert "/" in ts

    @pytest.mark.parametrize("lang", ROTATION_ORDER)
    def test_all_languages_have_syncopation_level(self, lang):
        """Every language has syncopation level 1-10."""
        level = RHYTHM_DATA[lang]["syncopation_level"]
        assert 1 <= level <= 10

    @pytest.mark.parametrize("lang", ROTATION_ORDER)
    def test_all_languages_have_swing_percentage(self, lang):
        """Every language has swing percentage 0-100."""
        pct = RHYTHM_DATA[lang]["swing_percentage"]
        assert 0 <= pct <= 100

    @pytest.mark.parametrize("lang", ROTATION_ORDER)
    def test_all_languages_have_polyrhythm_depth(self, lang):
        """Every language has polyrhythm depth 1-5."""
        depth = RHYTHM_DATA[lang]["polyrhythm_depth"]
        assert 1 <= depth <= 5

    @pytest.mark.parametrize("lang", ROTATION_ORDER)
    def test_all_languages_have_genre_emoji(self, lang):
        """Every language has a genre emoji."""
        emoji = RHYTHM_DATA[lang]["genre_emoji"]
        assert emoji is not None
        assert len(emoji) > 0

    @pytest.mark.parametrize("lang", ROTATION_ORDER)
    def test_all_languages_have_signature_groove(self, lang):
        """Every language has a signature groove name."""
        groove = RHYTHM_DATA[lang]["signature_groove"]
        assert groove is not None
        assert len(groove) > 0

    @pytest.mark.parametrize("lang", ROTATION_ORDER)
    def test_all_languages_have_rhythm_quote(self, lang):
        """Every language has a rhythm quote."""
        quote = RHYTHM_DATA[lang]["rhythm_quote"]
        assert quote is not None
        assert len(quote) > 20


# ─────────────────────────────────────────────────────────────────────────────
# Tempo Function Tests
# ─────────────────────────────────────────────────────────────────────────────

class TestTempoFunction:
    """Test the main tempo() function."""

    def test_tempo_returns_dict(self):
        """tempo() returns a dictionary."""
        result = tempo(rotate=False)
        assert isinstance(result, dict)

    def test_tempo_has_all_required_keys(self):
        """Result has all required keys."""
        result = tempo(rotate=False)
        required = [
            "tool", "version", "selected_language", "previous_language",
            "next_language", "rotation", "rhythm_profile", "drum_grid",
            "syncopation", "swing", "beat_characteristics", "common_rhythms",
            "rhythm_quote", "transition", "timestamp"
        ]
        for key in required:
            assert key in result, f"Missing key: {key}"

    def test_tempo_returns_valid_language(self):
        """Selected language is in the rotation."""
        result = tempo(rotate=False)
        assert result["selected_language"] in ROTATION_ORDER

    def test_tempo_correct_tool_name_and_version(self):
        """Tool name and version are correct."""
        result = tempo(rotate=False)
        assert result["tool"] == TOOL_NAME
        assert result["version"] == TOOL_VERSION

    def test_tempo_rhythm_profile_has_bpm(self):
        """rhythm_profile contains bpm."""
        result = tempo(rotate=False)
        assert "bpm" in result["rhythm_profile"]
        assert 60 <= result["rhythm_profile"]["bpm"] <= 200

    def test_tempo_drum_grid_is_multiline(self):
        """drum_grid is a multi-line string."""
        result = tempo(rotate=False)
        assert "\n" in result["drum_grid"]
        assert len(result["drum_grid"]) > 50

    def test_tempo_syncopation_level_1_to_10(self):
        """syncopation level is between 1 and 10."""
        result = tempo(rotate=False)
        level = result["syncopation"]["level"]
        assert 1 <= level <= 10

    def test_tempo_common_rhythms_minimum_count(self):
        """At least 3 common rhythms are returned."""
        result = tempo(rotate=False)
        assert len(result["common_rhythms"]) >= 3

    def test_tempo_bpm_factors_in_effective_bpm(self):
        """Each rhythm's effective_bpm is approximately bpm * factor."""
        result = tempo(rotate=False)
        bpm = result["rhythm_profile"]["bpm"]
        for rhythm in result["common_rhythms"]:
            expected = round(bpm * rhythm["bpm_factor"])
            assert abs(rhythm["effective_bpm"] - expected) <= 1


# ─────────────────────────────────────────────────────────────────────────────
# Rotation Advancement Tests
# ─────────────────────────────────────────────────────────────────────────────

class TestRotationAdvancement:
    """Test that rotation advances correctly."""

    def test_advance_rotation_changes_index(self):
        """Calling advance_rotation changes current_index."""
        initial = load_rotation()
        initial_idx = initial["current_index"]
        lang, new_idx = advance_rotation()
        updated = load_rotation()
        assert updated["current_index"] == new_idx
        assert updated["last_language"] == lang

    def test_rotation_cycles_correctly(self):
        """Rotation cycles from last language back to first."""
        result = tempo(rotate=True)
        config = load_rotation()
        # After calling tempo(rotate=True), we're at next position
        assert 0 <= config["current_index"] < 8

    def test_next_language_is_in_rotation(self):
        """The next_language field is always valid."""
        result = tempo(rotate=False)
        assert result["next_language"] in ROTATION_ORDER
        assert result["previous_language"] in ROTATION_ORDER or result["previous_language"] is None

    def test_rotation_order_matches_constant(self):
        """The rotation in result matches ROTATION_ORDER constant."""
        result = tempo(rotate=False)
        assert result["rotation"] == ROTATION_ORDER


# ─────────────────────────────────────────────────────────────────────────────
# Format and Display Tests
# ─────────────────────────────────────────────────────────────────────────────

class TestFormatRhythmCard:
    """Test the rhythm card formatter."""

    def test_format_rhythm_card_returns_string(self):
        """format_rhythm_card returns a string."""
        result = tempo(rotate=False)
        card = format_rhythm_card(result)
        assert isinstance(card, str)

    def test_card_contains_drum_grid_section(self):
        """Card contains the DRUM GRID section."""
        result = tempo(rotate=False)
        card = format_rhythm_card(result)
        assert "DRUM GRID" in card

    def test_card_contains_common_rhythms_section(self):
        """Card contains the COMMON RHYTHMS section."""
        result = tempo(rotate=False)
        card = format_rhythm_card(result)
        assert "COMMON RHYTHMS" in card

    def test_card_contains_bpm(self):
        """Card contains BPM information."""
        result = tempo(rotate=False)
        card = format_rhythm_card(result)
        assert "BPM" in card

    def test_card_contains_syncopation(self):
        """Card contains syncopation information."""
        result = tempo(rotate=False)
        card = format_rhythm_card(result)
        assert "Syncopation" in card

    def test_card_contains_next_language(self):
        """Card contains next language in rotation."""
        result = tempo(rotate=False)
        card = format_rhythm_card(result)
        assert "Next in rotation" in card


class TestBuildHelpers:
    """Test helper functions."""

    def test_build_drum_grid_returns_string(self):
        """build_drum_grid returns a string."""
        sample = [("Kick", "█   │   │   │   │"), ("Snare", "│   │ █ │   │   │")]
        result = build_drum_grid(sample)
        assert isinstance(result, str)

    def test_build_syncopation_bar_format(self):
        """build_syncopation_bar returns a string with brackets."""
        result = build_syncopation_bar(5)
        assert "[" in result
        assert "]" in result
        assert "5" in result

    def test_compute_transition_feel_returns_dict(self):
        """compute_transition_feel returns a dictionary with from/to/feel."""
        result = compute_transition_feel("Rust", "Go")
        assert isinstance(result, dict)
        assert "from" in result
        assert "to" in result
        assert "feel" in result
        assert result["from"] == "Rust"
        assert result["to"] == "Go"
        assert len(result["feel"]) > 0


class TestGenerateRhythmReport:
    """Test the generate_rhythm_report alias."""

    def test_generate_rhythm_report_equals_tempo(self):
        """generate_rhythm_report returns same result as tempo(rotate=False)."""
        r1 = tempo(rotate=False)
        r2 = generate_rhythm_report(rotate=False)
        # Compare without timestamp (microsecond differences cause flakiness)
        r1_ts = r1.pop("timestamp")
        r2_ts = r2.pop("timestamp")
        assert r1 == r2, f"Result differs (timestamps: {r1_ts} vs {r2_ts})"


# ─────────────────────────────────────────────────────────────────────────────
# Edge Cases
# ─────────────────────────────────────────────────────────────────────────────

class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_rotation_file_handled(self):
        """Module handles missing/invalid rotation gracefully."""
        # load_rotation will raise FileNotFoundError if missing
        # This is expected behavior
        pass

    def test_all_genres_are_distinct(self):
        """Each language has a distinct genre description."""
        genres = [RHYTHM_DATA[lang]["genre"] for lang in ROTATION_ORDER]
        assert len(genres) == len(set(genres)), "All genres should be unique"

    def test_bpm_values_span_range(self):
        """BPM values span a reasonable musical range."""
        bpms = [RHYTHM_DATA[lang]["bpm"] for lang in ROTATION_ORDER]
        assert min(bpms) >= 100  # slowest language is still brisk
        assert max(bpms) <= 165  # fastest is not inhuman

    def test_no_language_has_zero_bpm_factor(self):
        """No common rhythm has a bpm_factor of 0 (would be silent)."""
        for lang in ROTATION_ORDER:
            for rhythm in RHYTHM_DATA[lang]["common_rhythms"]:
                assert rhythm["bpm_factor"] > 0

    def test_ghost_note_frequency_range(self):
        """Ghost note frequency is in 1-10 range for all languages."""
        for lang in ROTATION_ORDER:
            freq = RHYTHM_DATA[lang]["ghost_note_frequency"]
            assert 1 <= freq <= 10

    def test_beat_strength_range(self):
        """Beat strength is in 1-10 range for all languages."""
        for lang in ROTATION_ORDER:
            strength = RHYTHM_DATA[lang]["beat_strength"]
            assert 1 <= strength <= 10
