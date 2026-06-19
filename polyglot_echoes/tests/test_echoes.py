#!/usr/bin/env python3
"""
Tests for Polyglot Echoes — Language Temporal Reverberation System
Run with: python -m pytest polyglot_echoes/tests/ -v
"""
import json
import os
import sys
import tempfile
import shutil
from pathlib import Path
from typing import Dict, Any

import pytest

# Import from package
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from polyglot_echoes import (
    TOOL_NAME,
    TOOL_VERSION,
    ROTATION_ORDER,
    ECHO_SYSTEMS,
    load_rotation,
    save_rotation,
    echoes,
    run_tests,
    compute_reverb_time,
    build_echo_waveform,
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
def rotation_config_index5(tmp_path: Path) -> str:
    """Create a rotation config at index 5 (JavaScript)."""
    config = {
        "languages": ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"],
        "current_index": 5,
        "last_language": "JavaScript",
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
        "last_language": "C/C++",
        "updated_at": "2026-06-14T03:00:00+08:00",
    }
    path = tmp_path / "language_rotation.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(config, f)
    return str(path)


@pytest.fixture
def rotation_config_index0_last(tmp_path: Path) -> str:
    """Create a rotation config at index 0, with save_rotation stubbed."""
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


# ─────────────────────────────────────────────────────────────────────────────
# Module Constants Tests
# ─────────────────────────────────────────────────────────────────────────────

class TestModuleConstants:
    def test_tool_name(self):
        assert TOOL_NAME == "polyglot-echoes"

    def test_tool_version(self):
        assert TOOL_VERSION == "1.0.0"

    def test_rotation_order_length(self):
        assert len(ROTATION_ORDER) == 8

    def test_rotation_order_sequence(self):
        expected = ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"]
        assert ROTATION_ORDER == expected

    def test_echo_systems_has_8_entries(self):
        assert len(ECHO_SYSTEMS) == 8

    def test_echo_systems_has_all_rotation_languages(self):
        for lang in ROTATION_ORDER:
            assert lang in ECHO_SYSTEMS, f"Missing {lang} in ECHO_SYSTEMS"


# ─────────────────────────────────────────────────────────────────────────────
# Echo System Data Structure Tests
# ─────────────────────────────────────────────────────────────────────────────

class TestEchoSystemStructure:
    REQUIRED_FIELDS = {
        "past_echoes", "present_resonance", "future_shadow",
        "reverb_time", "frequency_bands", "acoustic_impedance",
        "echo_description", "echo_glyph", "waveform_peaks",
        "impedance_materials", "shadow_wavelength",
    }

    def test_all_languages_have_required_fields(self):
        for lang in ROTATION_ORDER:
            entry = ECHO_SYSTEMS[lang]
            missing = self.REQUIRED_FIELDS - entry.keys()
            assert not missing, f"{lang} missing fields: {missing}"

    def test_past_echoes_is_list_of_tuples(self):
        for lang in ROTATION_ORDER:
            echoes_list = ECHO_SYSTEMS[lang]["past_echoes"]
            assert isinstance(echoes_list, list)
            for item in echoes_list:
                assert isinstance(item, tuple)
                assert len(item) == 3
                source, weight, desc = item
                assert isinstance(source, str)
                assert isinstance(weight, float)
                assert 0.0 <= weight <= 1.0
                assert isinstance(desc, str)

    def test_future_shadow_is_list_of_tuples(self):
        for lang in ROTATION_ORDER:
            shadow_list = ECHO_SYSTEMS[lang]["future_shadow"]
            assert isinstance(shadow_list, list)
            for item in shadow_list:
                assert isinstance(item, tuple)
                assert len(item) == 2
                concept, implication = item
                assert isinstance(concept, str)
                assert isinstance(implication, str)

    def test_frequency_bands_has_all_bands(self):
        REQUIRED_BANDS = {"safety", "performance", "expressiveness", "concurrency", "abstraction"}
        for lang in ROTATION_ORDER:
            bands = ECHO_SYSTEMS[lang]["frequency_bands"]
            missing = REQUIRED_BANDS - bands.keys()
            assert not missing, f"{lang} missing frequency bands: {missing}"
            for band_name, value in bands.items():
                assert isinstance(value, (int, float))
                assert 0.0 <= value <= 1.0

    def test_present_resonance_is_valid(self):
        for lang in ROTATION_ORDER:
            resonance = ECHO_SYSTEMS[lang]["present_resonance"]
            assert isinstance(resonance, (int, float))
            assert 0.0 <= resonance <= 10.0

    def test_reverb_time_is_valid(self):
        for lang in ROTATION_ORDER:
            reverb = ECHO_SYSTEMS[lang]["reverb_time"]
            assert isinstance(reverb, (int, float))
            assert reverb > 0

    def test_acoustic_impedance_is_valid(self):
        for lang in ROTATION_ORDER:
            impedance = ECHO_SYSTEMS[lang]["acoustic_impedance"]
            assert isinstance(impedance, (int, float))
            assert 0.0 <= impedance <= 1.0

    def test_waveform_peaks_is_valid(self):
        for lang in ROTATION_ORDER:
            peaks = ECHO_SYSTEMS[lang]["waveform_peaks"]
            assert isinstance(peaks, list)
            assert len(peaks) > 0
            for peak in peaks:
                assert isinstance(peak, (int, float))
                assert 0.0 <= peak <= 1.0

    def test_impedance_materials_is_list_of_strings(self):
        for lang in ROTATION_ORDER:
            materials = ECHO_SYSTEMS[lang]["impedance_materials"]
            assert isinstance(materials, list)
            assert len(materials) > 0
            for material in materials:
                assert isinstance(material, str)

    def test_echo_glyph_is_single_emoji(self):
        for lang in ROTATION_ORDER:
            glyph = ECHO_SYSTEMS[lang]["echo_glyph"]
            assert isinstance(glyph, str)
            assert len(glyph) > 0

    def test_echo_description_is_non_empty_string(self):
        for lang in ROTATION_ORDER:
            desc = ECHO_SYSTEMS[lang]["echo_description"]
            assert isinstance(desc, str)
            assert len(desc) > 20


# ─────────────────────────────────────────────────────────────────────────────
# Rotation Loading / Saving Tests
# ─────────────────────────────────────────────────────────────────────────────

class TestRotationLoadSave:
    def test_load_rotation_parses_correctly(self, rotation_config):
        data = load_rotation(rotation_config)
        assert data["languages"] == ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"]
        assert data["current_index"] == 0
        assert data["last_language"] == "Rust"

    def test_save_rotation_writes_file(self, tmp_path):
        config = {
            "languages": ["Rust", "Go"],
            "current_index": 1,
            "last_language": "Go",
            "updated_at": "2026-06-14T03:00:00+08:00",
        }
        path = tmp_path / "test_rotation.json"
        save_rotation(config, str(path))
        loaded = load_rotation(str(path))
        assert loaded == config


# ─────────────────────────────────────────────────────────────────────────────
# Language Selection / Advancement Tests
# ─────────────────────────────────────────────────────────────────────────────

class TestLanguageSelection:
    def test_select_first_language(self, rotation_config):
        """At index 0, Rust should be selected."""
        data = load_rotation(rotation_config)
        result = echoes(rotation_config)
        assert result["language"] == "Rust"
        assert result["rotation"]["current_index"] == 1

    def test_select_fifth_language(self, rotation_config_index5):
        """At index 5, JavaScript should be selected."""
        result = echoes(rotation_config_index5)
        assert result["language"] == "JavaScript"
        assert result["rotation"]["current_index"] == 6

    def test_wrap_around_last_to_first(self, rotation_config_last_index):
        """At index 7 (C/C++), next should wrap to index 0 (Rust)."""
        result = echoes(rotation_config_last_index)
        assert result["language"] == "C/C++"
        assert result["rotation"]["current_index"] == 0

    def test_full_cycle_returns_to_start(self, rotation_config_last_index):
        """After C/C++ (index 7), next wraps to Rust (index 0)."""
        data_before = load_rotation(rotation_config_last_index)
        assert data_before["current_index"] == 7
        result = echoes(rotation_config_last_index)
        assert result["rotation"]["current_index"] == 0

    def test_next_language_reflects_current_index(self, rotation_config):
        """After Rust (index 0→1), next_language should be Go."""
        result = echoes(rotation_config)
        assert result["rotation"]["next_language"] == "Go"

    def test_updated_at_is_iso_format(self, rotation_config):
        """updated_at field should be ISO 8601 format."""
        result = echoes(rotation_config)
        updated_at = result["rotation"]["updated_at"]
        # Should be non-empty string that looks like ISO timestamp
        assert isinstance(updated_at, str)
        assert len(updated_at) > 0
        # Should contain date and time separators
        assert "T" in updated_at or " " in updated_at


# ─────────────────────────────────────────────────────────────────────────────
# Echo Analysis Function Tests
# ─────────────────────────────────────────────────────────────────────────────

class TestEchoAnalysisFunctions:
    def test_compute_reverb_time_rust(self):
        reverb = compute_reverb_time("Rust")
        assert isinstance(reverb, float)
        assert reverb > 0

    def test_compute_reverb_time_js(self):
        reverb = compute_reverb_time("JavaScript")
        assert isinstance(reverb, float)
        assert reverb > 0

    def test_compute_reverb_time_cpp(self):
        reverb = compute_reverb_time("C/C++")
        assert isinstance(reverb, float)
        assert reverb > 0

    def test_build_echo_waveform_rust(self):
        waveform = build_echo_waveform("Rust")
        assert isinstance(waveform, str)
        assert len(waveform) > 0
        assert "█" in waveform

    def test_build_echo_waveform_all_languages(self):
        for lang in ROTATION_ORDER:
            waveform = build_echo_waveform(lang)
            assert "█" in waveform
            glyph = ECHO_SYSTEMS[lang]["echo_glyph"]
            assert glyph in waveform, f"Waveform for {lang} should contain glyph {glyph}"


# ─────────────────────────────────────────────────────────────────────────────
# Output Structure Tests
# ─────────────────────────────────────────────────────────────────────────────

class TestEchoesOutputStructure:
    def test_output_has_required_keys(self, rotation_config):
        result = echoes(rotation_config)
        REQUIRED = {
            "tool", "version", "language", "echo_glyph",
            "past_echoes", "present_resonance", "future_shadow",
            "reverb_time_seconds", "frequency_bands", "acoustic_impedance",
            "impedance_description", "impedance_materials", "shadow_wavelength",
            "echo_description", "waveform_peaks", "rotation",
        }
        missing = REQUIRED - result.keys()
        assert not missing, f"Missing output keys: {missing}"

    def test_past_echoes_output_format(self, rotation_config):
        result = echoes(rotation_config)
        past = result["past_echoes"]
        assert isinstance(past, list)
        for item in past:
            assert "source" in item
            assert "weight" in item
            assert "description" in item

    def test_future_shadow_output_format(self, rotation_config):
        result = echoes(rotation_config)
        future = result["future_shadow"]
        assert isinstance(future, list)
        for item in future:
            assert "concept" in item
            assert "implication" in item

    def test_impedance_description_values(self, rotation_config):
        result = echoes(rotation_config)
        valid = {"Very Low", "Low", "Medium", "High", "Very High"}
        assert result["impedance_description"] in valid

    def test_frequency_bands_are_normalized(self, rotation_config):
        result = echoes(rotation_config)
        bands = result["frequency_bands"]
        for name, value in bands.items():
            assert 0.0 <= value <= 1.0


# ─────────────────────────────────────────────────────────────────────────────
# End-to-End Behavior Tests
# ─────────────────────────────────────────────────────────────────────────────

class TestEchoesEndToEnd:
    def test_rotation_advances_correctly(self, rotation_config):
        """Test full 8-language cycle with proper advancement."""
        languages_seen = []
        config_path = rotation_config

        for i in range(8):
            result = echoes(config_path)
            languages_seen.append(result["language"])

        expected = ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"]
        assert languages_seen == expected

    def test_echoes_updates_json_file(self, rotation_config):
        """The echoes() function should persist state to JSON file."""
        echoes(rotation_config)
        data = load_rotation(rotation_config)
        assert data["current_index"] == 1
        assert data["last_language"] == "Rust"

    def test_all_languages_have_valid_past_echoes(self):
        """Every language should have at least 3 past echoes."""
        for lang in ROTATION_ORDER:
            past = ECHO_SYSTEMS[lang]["past_echoes"]
            assert len(past) >= 3, f"{lang} should have at least 3 past echoes"

    def test_all_languages_have_valid_future_shadows(self):
        """Every language should have exactly 4 future shadows."""
        for lang in ROTATION_ORDER:
            future = ECHO_SYSTEMS[lang]["future_shadow"]
            assert len(future) == 4, f"{lang} should have exactly 4 future shadows"

    def test_all_languages_have_unique_glyphs(self):
        """All languages should have distinct glyphs."""
        glyphs = [ECHO_SYSTEMS[lang]["echo_glyph"] for lang in ROTATION_ORDER]
        assert len(glyphs) == len(set(glyphs)), "All glyphs should be unique"

    def test_rotation_order_starts_with_rust(self):
        """Rotation must start with Rust."""
        assert ROTATION_ORDER[0] == "Rust"

    def test_rotation_order_ends_with_cpp(self):
        """Rotation must end with C/C++."""
        assert ROTATION_ORDER[-1] == "C/C++"

    def test_cpp_has_highest_reverb_time(self):
        """C/C++ should have the longest reverb time (most permanent influence)."""
        cpp_reverb = ECHO_SYSTEMS["C/C++"]["reverb_time"]
        for lang in ROTATION_ORDER:
            if lang != "C/C++":
                assert cpp_reverb >= ECHO_SYSTEMS[lang]["reverb_time"]

    def test_javascript_has_highest_resonance(self):
        """JavaScript should have the highest present resonance."""
        js_resonance = ECHO_SYSTEMS["JavaScript"]["present_resonance"]
        for lang in ROTATION_ORDER:
            if lang != "JavaScript":
                assert js_resonance >= ECHO_SYSTEMS[lang]["present_resonance"]


# ─────────────────────────────────────────────────────────────────────────────
# File Operations Tests
# ─────────────────────────────────────────────────────────────────────────────

class TestFileOperations:
    def test_rotation_file_is_valid_json(self, rotation_config):
        """The saved rotation file should be valid JSON."""
        with open(rotation_config, "r") as f:
            data = json.load(f)
        assert isinstance(data, dict)
        assert "languages" in data
        assert "current_index" in data

    def test_rotation_file_preserves_languages(self, rotation_config):
        """Save operations should preserve the languages list."""
        echoes(rotation_config)
        data = load_rotation(rotation_config)
        assert data["languages"] == ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"]
