#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for polyglot_tempo module.
"""

import json
import os
import sys
import pytest
from pathlib import Path

# Build correct path to module and rotation file
POLYGLOT_ROOT = Path(__file__).parent.parent      # polyglot_tempo/
WORKSPACE_ROOT = POLYGLOT_ROOT.parent             # AllToolkit/
ROTATION_FILE = str(WORKSPACE_ROOT / "language_rotation.json")

# Add src/ to sys.path so tempo module can be found
import sys
sys.path.insert(0, str(POLYGLOT_ROOT / "src"))

# Patch the rotation file path in tempo module before import
import tempo as tempo_module
tempo_module._ROTATION_FILE = ROTATION_FILE

from tempo import (
    TOOL_NAME,
    TOOL_VERSION,
    LANGUAGE_RHYTHMS,
    LANGUAGE_NOTE_VALUES,
    GENRE_DESCRIPTIONS,
    TEMPO_TIER_LABELS,
    get_tempo_profile,
    generate_beat_pattern,
    get_language_genre,
    get_tempo_tier,
    analyze_tempo,
    format_tempo_report,
    load_rotation,
    compute_next_language,
)

ROTATION_ORDER = ["Rust", "Go", "Swift", "Kotlin",
                  "TypeScript", "JavaScript", "Java", "C/C++"]


class TestModuleMetadata:
    """Test module constants."""

    def test_tool_name(self):
        assert TOOL_NAME == "polyglot-tempo"

    def test_tool_version(self):
        assert TOOL_VERSION == "1.0.0"


class TestLanguageRhythmsData:
    """Test LANGUAGE_RHYTHMS data completeness."""

    def test_all_8_languages_have_rhythms(self):
        for lang in ROTATION_ORDER:
            assert lang in LANGUAGE_RHYTHMS, f"{lang} missing from LANGUAGE_RHYTHMS"

    def test_each_language_has_required_fields(self):
        required_fields = {
            "bpm_range", "time_signature", "character", "feel",
            "signature_note", "syncopation", "groove_factor",
            "rhythm_tags", "composer_equivalent", "mood_keywords",
        }
        for lang in ROTATION_ORDER:
            fields = set(LANGUAGE_RHYTHMS[lang].keys())
            missing = required_fields - fields
            assert not missing, f"{lang} missing fields: {missing}"

    def test_bpm_ranges_are_valid(self):
        for lang in ROTATION_ORDER:
            lo, hi = LANGUAGE_RHYTHMS[lang]["bpm_range"]
            assert 40 <= lo <= 200, f"{lang} bpm_range low {lo} out of range"
            assert lo <= hi, f"{lang} bpm_range {lo}-{hi} invalid"
            assert lo <= hi <= 200, f"{lang} bpm_range high {hi} out of range"

    def test_syncopation_and_groove_in_range(self):
        for lang in ROTATION_ORDER:
            data = LANGUAGE_RHYTHMS[lang]
            assert 0 <= data["syncopation"] <= 1, f"{lang} syncopation out of [0,1]"
            assert 0 <= data["groove_factor"] <= 1, f"{lang} groove_factor out of [0,1]"


class TestTempoTierClassification:
    """Test get_tempo_tier function."""

    def test_prestissimo(self):
        assert get_tempo_tier(155) == "prestissimo"
        assert get_tempo_tier(151) == "prestissimo"

    def test_presto(self):
        assert get_tempo_tier(150) == "presto"
        assert get_tempo_tier(135) == "presto"

    def test_allegro(self):
        assert get_tempo_tier(134) == "allegro"
        assert get_tempo_tier(110) == "allegro"

    def test_andante(self):
        assert get_tempo_tier(109) == "andante"
        assert get_tempo_tier(85) == "andante"

    def test_adagio(self):
        assert get_tempo_tier(84) == "adagio"
        assert get_tempo_tier(60) == "adagio"


class TestGetTempoProfile:
    """Test get_tempo_profile function."""

    def test_returns_dict(self):
        result = get_tempo_profile("Rust")
        assert isinstance(result, dict)

    def test_returns_bpm_in_range(self):
        for lang in ROTATION_ORDER:
            profile = get_tempo_profile(lang)
            assert "bpm" in profile
            lo, hi = profile["bpm_range"]
            assert lo <= profile["bpm"] <= hi

    def test_returns_tempo_tier(self):
        for lang in ROTATION_ORDER:
            profile = get_tempo_profile(lang)
            assert "tempo_tier" in profile
            assert profile["tempo_tier"] in TEMPO_TIER_LABELS

    def test_returns_genre_description(self):
        for lang in ROTATION_ORDER:
            profile = get_tempo_profile(lang)
            assert "genre_description" in profile
            assert isinstance(profile["genre_description"], str)
            assert len(profile["genre_description"]) > 0

    def test_invalid_language_raises(self):
        with pytest.raises(ValueError) as excinfo:
            get_tempo_profile("Haskell")
        assert "Haskell" in str(excinfo.value)


class TestGenerateBeatPattern:
    """Test generate_beat_pattern function."""

    def test_returns_list(self):
        result = generate_beat_pattern("Rust", bars=4)
        assert isinstance(result, list)

    def test_returns_correct_number_of_bars(self):
        for bars in [1, 2, 4, 8]:
            result = generate_beat_pattern("Rust", bars=bars)
            assert len(result) == bars

    def test_each_bar_has_four_beats(self):
        for lang in ROTATION_ORDER:
            pattern = generate_beat_pattern(lang, bars=4)
            for bar in pattern:
                beats = [b.strip() for b in bar.split("  ") if b.strip()]
                assert len(beats) == 4, f"{lang} bar has {len(beats)} beats, expected 4"

    def test_beat_symbols_are_valid(self):
        valid_symbols = {"●", "○", "◑", "░"}
        for lang in ROTATION_ORDER:
            pattern = generate_beat_pattern(lang, bars=4)
            for bar in pattern:
                for beat in bar.split("  "):
                    beat = beat.strip()
                    if beat:
                        assert beat in valid_symbols, f"{lang}: invalid beat symbol {beat}"

    def test_first_beat_is_always_strong(self):
        for lang in ROTATION_ORDER:
            pattern = generate_beat_pattern(lang, bars=4)
            for bar in pattern:
                beats = bar.split("  ")
                assert beats[0].strip() == "●", f"{lang}: first beat not ●"

    def test_invalid_language_raises(self):
        with pytest.raises(ValueError):
            generate_beat_pattern("Scala")


class TestGetLanguageGenre:
    """Test get_language_genre function."""

    def test_returns_string(self):
        result = get_language_genre("Rust")
        assert isinstance(result, str)

    def test_genre_in_descriptions(self):
        for lang in ROTATION_ORDER:
            genre = get_language_genre(lang)
            assert genre in GENRE_DESCRIPTIONS, f"{lang} genre '{genre}' not in GENRE_DESCRIPTIONS"


class TestAnalyzeTempo:
    """Test analyze_tempo function (main entry point)."""

    def test_returns_dict(self):
        result = analyze_tempo("Rust")
        assert isinstance(result, dict)

    def test_returns_language(self):
        result = analyze_tempo("Rust")
        assert result["language"] == "Rust"

    def test_returns_tempo_profile(self):
        result = analyze_tempo("Rust")
        assert "tempo_profile" in result
        assert isinstance(result["tempo_profile"], dict)

    def test_returns_beat_pattern(self):
        result = analyze_tempo("Rust")
        assert "beat_pattern" in result
        assert isinstance(result["beat_pattern"], list)
        assert len(result["beat_pattern"]) == 4

    def test_returns_next_language(self):
        result = analyze_tempo("Rust")
        assert "next_language" in result
        assert result["next_language"] == "Go"

    def test_returns_rotation_position(self):
        result = analyze_tempo("Go")
        assert "rotation_position" in result
        assert result["rotation_position"] == 1

    def test_invalid_language_raises(self):
        with pytest.raises(ValueError) as excinfo:
            analyze_tempo("Zig")
        assert "Zig" in str(excinfo.value)

    def test_updates_rotation_state(self):
        config_before = load_rotation()
        idx_before = config_before["current_index"]
        lang_before = config_before["languages"][idx_before]
        analyze_tempo(lang_before)
        config_after = load_rotation()
        expected = (idx_before + 1) % len(config_before["languages"])
        assert config_after["current_index"] == expected


class TestFormatTempoReport:
    """Test format_tempo_report function."""

    def test_returns_string(self):
        analysis = analyze_tempo("Rust")
        report = format_tempo_report(analysis)
        assert isinstance(report, str)

    def test_report_contains_language(self):
        analysis = analyze_tempo("Swift")
        report = format_tempo_report(analysis)
        assert "Swift" in report

    def test_report_contains_bpm(self):
        analysis = analyze_tempo("Kotlin")
        report = format_tempo_report(analysis)
        assert "BPM:" in report

    def test_report_contains_next_language(self):
        analysis = analyze_tempo("Java")
        report = format_tempo_report(analysis)
        assert "C/C++" in report

    def test_report_contains_beat_pattern(self):
        analysis = analyze_tempo("TypeScript")
        report = format_tempo_report(analysis)
        assert "Beat Pattern" in report


class TestRotationIntegrity:
    """Test rotation file integrity."""

    def test_rotation_file_exists(self):
        assert os.path.exists(ROTATION_FILE)

    def test_rotation_has_8_languages(self):
        config = load_rotation()
        assert len(config["languages"]) == 8

    def test_rust_is_first(self):
        config = load_rotation()
        assert config["languages"][0] == "Rust"

    def test_cpp_is_last(self):
        config = load_rotation()
        assert config["languages"][-1] == "C/C++"

    def test_current_index_in_range(self):
        config = load_rotation()
        assert 0 <= config["current_index"] < len(config["languages"])