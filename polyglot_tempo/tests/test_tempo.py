#!/usr/bin/env python3
"""
Tests for Polyglot Tempo — Rhythm Pattern Generator
"""

import json
import os
import tempfile
from pathlib import Path
from typing import Dict, Any

import pytest

# Import from package
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from tempo import (
    TOOL_NAME,
    TOOL_VERSION,
    ROTATION_ORDER,
    RHYTHM_DB,
    get_current_language,
    get_tempo_for_language,
    generate_tempo_map,
    format_tempo_card,
    _compute_next_index,
)


# ─────────────────────────────────────────────────────────────────────────────
# Fixtures
# ─────────────────────────────────────────────────────────────────────────────

@pytest.fixture
def rotation_config(tmp_path: Path) -> str:
    """Create a temporary rotation config file and return its path."""
    config = {
        "languages": ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"],
        "current_index": 1,
        "last_language": "Go",
        "updated_at": "2026-06-14T03:00:00+08:00",
    }
    path = tmp_path / "language_rotation.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(config, f)
    return str(path)


@pytest.fixture
def rotation_config_index0(tmp_path: Path) -> str:
    """Create a rotation config with index=0."""
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


# ─────────────────────────────────────────────────────────────────────────────
# Module Constants Tests
# ─────────────────────────────────────────────────────────────────────────────

class TestModuleConstants:
    def test_tool_name(self):
        assert TOOL_NAME == "polyglot-tempo"
        assert "tempo" in TOOL_NAME

    def test_tool_version(self):
        assert TOOL_VERSION == "1.0.0"

    def test_rotation_order_length(self):
        assert len(ROTATION_ORDER) == 8

    def test_rotation_order_sequence(self):
        expected = ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"]
        assert ROTATION_ORDER == expected

    def test_rhythm_db_has_all_rotation_languages(self):
        for lang in ROTATION_ORDER:
            assert lang in RHYTHM_DB, f"Missing {lang} in RHYTHM_DB"

    def test_rhythm_db_entry_structure(self):
        required_keys = {
            "bpm", "time_signature", "groove_tag", "feel",
            "primary_pattern", "pattern_desc", "beat_notation",
            "fill_pattern", "fill_desc", "percussion_emoji",
            "cadence", "rhythm_quote", "tempo_desc", "ascii_notation",
            "kick", "snare", "hihat", "crash", "swing_factor",
        }
        for lang in ROTATION_ORDER:
            entry = RHYTHM_DB[lang]
            missing = required_keys - entry.keys()
            assert not missing, f"{lang} missing keys: {missing}"

    def test_bpm_ranges(self):
        for lang, data in RHYTHM_DB.items():
            assert 60 <= data["bpm"] <= 200, f"{lang} BPM out of range: {data['bpm']}"

    def test_swing_factor_ranges(self):
        for lang, data in RHYTHM_DB.items():
            assert 0.0 <= data["swing_factor"] <= 1.0, f"{lang} swing_factor out of range: {data['swing_factor']}"


# ─────────────────────────────────────────────────────────────────────────────
# Compute Next Index Tests
# ─────────────────────────────────────────────────────────────────────────────

class TestComputeNextIndex:
    def test_advance_normal(self):
        languages = ["Rust", "Go", "Swift"]
        assert _compute_next_index(0, languages) == 1
        assert _compute_next_index(1, languages) == 2

    def test_advance_wraps(self):
        languages = ["Rust", "Go", "Swift"]
        assert _compute_next_index(2, languages) == 0

    def test_advance_empty(self):
        languages = []
        # Edge case: empty list, should not crash
        result = _compute_next_index(0, languages)
        assert result == 0

    def test_advance_single_element(self):
        languages = ["Rust"]
        assert _compute_next_index(0, languages) == 0


# ─────────────────────────────────────────────────────────────────────────────
# Get Current Language Tests
# ─────────────────────────────────────────────────────────────────────────────

class TestGetCurrentLanguage:
    def test_returns_language_at_index(self, rotation_config):
        lang = get_current_language(rotation_config)
        assert lang == "Go"  # current_index = 1

    def test_returns_rust_at_index0(self, rotation_config_index0):
        lang = get_current_language(rotation_config_index0)
        assert lang == "Rust"

    def test_returns_cpp_at_last_index(self, rotation_config_last_index):
        lang = get_current_language(rotation_config_last_index)
        assert lang == "C/C++"


# ─────────────────────────────────────────────────────────────────────────────
# Get Tempo For Language Tests
# ─────────────────────────────────────────────────────────────────────────────

class TestGetTempoForLanguage:
    def test_returns_data_for_known_language(self):
        result = get_tempo_for_language("Rust")
        assert result is not None
        assert result["bpm"] == 120
        assert result["groove_tag"] == "Staccato Precision Metal"

    def test_returns_none_for_unknown_language(self):
        result = get_tempo_for_language("Python")
        assert result is None

    def test_all_rotation_languages_have_tempo_data(self):
        for lang in ROTATION_ORDER:
            result = get_tempo_for_language(lang)
            assert result is not None, f"Missing tempo data for {lang}"


# ─────────────────────────────────────────────────────────────────────────────
# Generate Tempo Map Tests
# ─────────────────────────────────────────────────────────────────────────────

class TestGenerateTempoMap:
    def test_returns_language_data(self, rotation_config):
        result = generate_tempo_map(rotate=False, config_path=rotation_config)
        assert result["current_language"] == "Go"
        assert result["current_index"] == 1
        assert result["bpm"] == 130
        assert result["groove_tag"] == "Clean 4/4 Funk"
        assert result["rotated"] is False
        assert result["new_index"] is None

    def test_rotation_advances_index(self, rotation_config):
        result = generate_tempo_map(rotate=True, config_path=rotation_config)
        assert result["current_language"] == "Go"
        assert result["rotated"] is True
        assert result["new_index"] == 2

    def test_rotation_persists_to_file(self, rotation_config):
        generate_tempo_map(rotate=True, config_path=rotation_config)
        with open(rotation_config, "r") as f:
            data = json.load(f)
        assert data["current_index"] == 2
        assert data["last_language"] == "Go"
        assert "updated_at" in data

    def test_rotation_wraps_at_end(self, rotation_config_last_index):
        result = generate_tempo_map(rotate=True, config_path=rotation_config_last_index)
        assert result["current_language"] == "C/C++"
        assert result["new_index"] == 0  # wraps back to Rust

    def test_rotation_file_wrapped(self, rotation_config_last_index):
        generate_tempo_map(rotate=True, config_path=rotation_config_last_index)
        with open(rotation_config_last_index, "r") as f:
            data = json.load(f)
        assert data["current_index"] == 0
        assert data["last_language"] == "C/C++"

    def test_unknown_language_returns_fallback(self, tmp_path: Path):
        config = {
            "languages": ["Python"],
            "current_index": 0,
            "last_language": "Python",
            "updated_at": "2026-06-14T03:00:00+08:00",
        }
        path = tmp_path / "lang.json"
        with open(path, "w") as f:
            json.dump(config, f)
        result = generate_tempo_map(rotate=False, config_path=str(path))
        assert result["current_language"] == "Python"
        assert result["bpm"] == 0
        assert result["groove_tag"] == "Unknown Groove"


# ─────────────────────────────────────────────────────────────────────────────
# Format Tempo Card Tests
# ─────────────────────────────────────────────────────────────────────────────

class TestFormatTempoCard:
    def test_formats_without_error(self, rotation_config):
        data = generate_tempo_map(rotate=False, config_path=rotation_config)
        card = format_tempo_card(data)
        assert isinstance(card, str)
        assert "POLYGLOT TEMPO" in card
        assert data["current_language"] in card

    def test_card_contains_key_fields(self, rotation_config):
        data = generate_tempo_map(rotate=False, config_path=rotation_config)
        card = format_tempo_card(data)
        assert "Groove Tag" in card
        assert "BPM" in card
        assert "PRIMARY RHYTHM" in card
        assert "FILL PATTERN" in card
        assert "PERCUSSION SEMANTICS" in card
        assert "CADENCE" in card

    def test_card_shows_rust_staccato(self):
        # Force Rust by using a config with index 0
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({
                "languages": ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"],
                "current_index": 0,
                "last_language": "Rust",
                "updated_at": "2026-06-14T03:00:00+08:00",
            }, f)
            path = f.name
        try:
            data = generate_tempo_map(rotate=False, config_path=path)
            card = format_tempo_card(data)
            assert "Staccato Precision Metal" in card
            assert "120" in card
        finally:
            os.unlink(path)

    def test_card_shows_cpp_death_metal(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({
                "languages": ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"],
                "current_index": 7,
                "last_language": "C/C++",
                "updated_at": "2026-06-14T03:00:00+08:00",
            }, f)
            path = f.name
        try:
            data = generate_tempo_map(rotate=False, config_path=path)
            card = format_tempo_card(data)
            assert "Death Metal Precision" in card
            assert "150" in card
        finally:
            os.unlink(path)


# ─────────────────────────────────────────────────────────────────────────────
# Round-Robin Sequence Tests
# ─────────────────────────────────────────────────────────────────────────────

class TestRoundRobinSequence:
    def test_full_rotation_sequence(self, tmp_path: Path):
        """Test that all 8 languages are visited in correct order over a full cycle."""
        config = {
            "languages": ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"],
            "current_index": 0,
            "last_language": "Rust",
            "updated_at": "2026-06-14T03:00:00+08:00",
        }
        path = tmp_path / "lang.json"
        with open(path, "w") as f:
            json.dump(config, f)

        visited = []
        for i in range(8):
            result = generate_tempo_map(rotate=True, config_path=str(path))
            visited.append(result["current_language"])

        expected = ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"]
        assert visited == expected

    def test_index_wraps_after_full_cycle(self, tmp_path: Path):
        """Test that index wraps back to 0 after a full 8-step cycle."""
        config = {
            "languages": ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"],
            "current_index": 0,
            "last_language": "Rust",
            "updated_at": "2026-06-14T03:00:00+08:00",
        }
        path = tmp_path / "lang.json"
        with open(path, "w") as f:
            json.dump(config, f)

        # Run 8 rotations
        for _ in range(8):
            generate_tempo_map(rotate=True, config_path=str(path))

        with open(path, "r") as f:
            data = json.load(f)
        assert data["current_index"] == 0


# ─────────────────────────────────────────────────────────────────────────────
# BPM / Groove Characteristics Tests
# ─────────────────────────────────────────────────────────────────────────────

class TestBPMGrooveCharacteristics:
    def test_rust_is_slowest_bpm(self):
        rust_bpm = RHYTHM_DB["Rust"]["bpm"]
        cpp_bpm = RHYTHM_DB["C/C++"]["bpm"]
        ts_bpm = RHYTHM_DB["TypeScript"]["bpm"]
        assert rust_bpm < cpp_bpm  # Rust = 120, C/C++ = 150

    def test_cpp_is_fastest_bpm(self):
        bpms = {lang: data["bpm"] for lang, data in RHYTHM_DB.items()}
        fastest = max(bpms, key=bpms.get)
        assert fastest == "C/C++"

    def test_go_is_most_straight_no_swing(self):
        go_swing = RHYTHM_DB["Go"]["swing_factor"]
        js_swing = RHYTHM_DB["JavaScript"]["swing_factor"]
        assert go_swing < js_swing

    def test_js_has_highest_swing(self):
        bpms = {lang: data["swing_factor"] for lang, data in RHYTHM_DB.items()}
        most_swing = max(bpms, key=bpms.get)
        assert most_swing == "JavaScript"

    def test_all_have_distinct_groove_tags(self):
        tags = [data["groove_tag"] for data in RHYTHM_DB.values()]
        assert len(tags) == len(set(tags)), "Groove tags must all be unique"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])