#!/usr/bin/env python3
"""
Tests for Polyglot Chef — Kitchen Brigade Tribute to Programming Languages
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

from chef import (
    TOOL_NAME,
    TOOL_VERSION,
    ROTATION_ORDER,
    KITCHEN_DB,
    get_current_language,
    get_station_for_language,
    generate_station_report,
    format_station_card,
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
        assert TOOL_NAME == "polyglot-chef"
        assert "chef" in TOOL_NAME

    def test_tool_version(self):
        assert TOOL_VERSION == "1.0.0"

    def test_rotation_order_length(self):
        assert len(ROTATION_ORDER) == 8

    def test_rotation_order_sequence(self):
        expected = ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"]
        assert ROTATION_ORDER == expected

    def test_kitchen_db_has_all_rotation_languages(self):
        for lang in ROTATION_ORDER:
            assert lang in KITCHEN_DB, f"Missing {lang} in KITCHEN_DB"

    def test_kitchen_db_entry_structure(self):
        required_keys = {
            "station", "brigade_role", "cooking_philosophy", "technique",
            "signature_dish", "mise_en_place", "service_rhythm",
            "plating_philosophy", "kitchen_tools", "chef_quote",
            "service_note", "plating_style", "station_emoji",
            "prep_style", "execution_tag",
        }
        for lang in ROTATION_ORDER:
            entry = KITCHEN_DB[lang]
            missing = required_keys - entry.keys()
            assert not missing, f"{lang} missing keys: {missing}"

    def test_all_kitchen_tools_are_nonempty_lists(self):
        for lang in ROTATION_ORDER:
            entry = KITCHEN_DB[lang]
            assert isinstance(entry["kitchen_tools"], list)
            assert len(entry["kitchen_tools"]) > 0

    def test_all_mise_en_place_are_nonempty_lists(self):
        for lang in ROTATION_ORDER:
            entry = KITCHEN_DB[lang]
            assert isinstance(entry["mise_en_place"], list)
            assert len(entry["mise_en_place"]) > 0

    def test_all_stations_are_unique(self):
        stations = [data["station"] for data in KITCHEN_DB.values()]
        assert len(stations) == len(set(stations)), "Stations must all be unique"

    def test_all_execution_tags_are_unique(self):
        tags = [data["execution_tag"] for data in KITCHEN_DB.values()]
        assert len(tags) == len(set(tags)), "Execution tags must all be unique"

    def test_all_plating_styles_are_unique(self):
        styles = [data["plating_style"] for data in KITCHEN_DB.values()]
        assert len(styles) == len(set(styles)), "Plating styles must all be unique"


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
# Get Station For Language Tests
# ─────────────────────────────────────────────────────────────────────────────

class TestGetStationForLanguage:
    def test_returns_data_for_known_language(self):
        result = get_station_for_language("Rust")
        assert result is not None
        assert result["station"] == "Sautoir Station (Sauté Chef)"
        assert result["execution_tag"] == "Proof-first cooking"

    def test_returns_none_for_unknown_language(self):
        result = get_station_for_language("Python")
        assert result is None

    def test_all_rotation_languages_have_station_data(self):
        for lang in ROTATION_ORDER:
            result = get_station_for_language(lang)
            assert result is not None, f"Missing station data for {lang}"


# ─────────────────────────────────────────────────────────────────────────────
# Generate Station Report Tests
# ─────────────────────────────────────────────────────────────────────────────

class TestGenerateStationReport:
    def test_returns_language_data(self, rotation_config):
        result = generate_station_report(rotate=False, config_path=rotation_config)
        assert result["current_language"] == "Go"
        assert result["current_index"] == 1
        assert result["station"] == "Rôtisseur Station (Roast Chef)"
        assert result["rotated"] is False
        assert result["new_index"] is None

    def test_rotation_advances_index(self, rotation_config):
        result = generate_station_report(rotate=True, config_path=rotation_config)
        assert result["current_language"] == "Go"
        assert result["rotated"] is True
        assert result["new_index"] == 2

    def test_rotation_persists_to_file(self, rotation_config):
        generate_station_report(rotate=True, config_path=rotation_config)
        with open(rotation_config, "r") as f:
            data = json.load(f)
        assert data["current_index"] == 2
        assert data["last_language"] == "Go"
        assert "updated_at" in data

    def test_rotation_wraps_at_end(self, rotation_config_last_index):
        result = generate_station_report(rotate=True, config_path=rotation_config_last_index)
        assert result["current_language"] == "C/C++"
        assert result["new_index"] == 0  # wraps back to Rust

    def test_rotation_file_wrapped(self, rotation_config_last_index):
        generate_station_report(rotate=True, config_path=rotation_config_last_index)
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
        result = generate_station_report(rotate=False, config_path=str(path))
        assert result["current_language"] == "Python"
        assert result["station"] == "Unknown Station"


# ─────────────────────────────────────────────────────────────────────────────
# Format Station Card Tests
# ─────────────────────────────────────────────────────────────────────────────

class TestFormatStationCard:
    def test_formats_without_error(self, rotation_config):
        data = generate_station_report(rotate=False, config_path=rotation_config)
        card = format_station_card(data)
        assert isinstance(card, str)
        assert "POLYGLOT CHEF" in card
        assert data["current_language"] in card

    def test_card_contains_key_fields(self, rotation_config):
        data = generate_station_report(rotate=False, config_path=rotation_config)
        card = format_station_card(data)
        assert "Station" in card
        assert "COOKING PHILOSOPHY" in card
        assert "SIGNATURE DISH" in card
        assert "SERVICE RHYTHM" in card
        assert "PLATING PHILOSOPHY" in card
        assert "KITCHEN TOOLS" in card
        assert "CHEF'S PHILOSOPHY" in card

    def test_card_shows_rust_sautoir(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({
                "languages": ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"],
                "current_index": 0,
                "last_language": "Rust",
                "updated_at": "2026-06-14T03:00:00+08:00",
            }, f)
            path = f.name
        try:
            data = generate_station_report(rotate=False, config_path=path)
            card = format_station_card(data)
            assert "Sautoir Station" in card
            assert "Proof-first cooking" in card
        finally:
            os.unlink(path)

    def test_card_shows_cpp_raw_fire(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({
                "languages": ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"],
                "current_index": 7,
                "last_language": "C/C++",
                "updated_at": "2026-06-14T03:00:00+08:00",
            }, f)
            path = f.name
        try:
            data = generate_station_report(rotate=False, config_path=path)
            card = format_station_card(data)
            assert "Raw Provisions" in card
            assert "Manual-memory cooking" in card
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
            result = generate_station_report(rotate=True, config_path=str(path))
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
            generate_station_report(rotate=True, config_path=str(path))

        with open(path, "r") as f:
            data = json.load(f)
        assert data["current_index"] == 0


# ─────────────────────────────────────────────────────────────────────────────
# Station Characteristics Tests
# ─────────────────────────────────────────────────────────────────────────────

class TestStationCharacteristics:
    def test_rust_is_sautoir_station(self):
        entry = KITCHEN_DB["Rust"]
        assert "Sautoir" in entry["station"]
        assert entry["prep_style"] == "Mise en place perfectionist"

    def test_go_is_rotisseur_station(self):
        entry = KITCHEN_DB["Go"]
        assert "Rôtisseur" in entry["station"]
        assert entry["prep_style"] == "Minimal mise, fast fire"

    def test_swift_is_entremetier_station(self):
        entry = KITCHEN_DB["Swift"]
        assert "Entremetier" in entry["station"]

    def test_kotlin_is_garde_manger_station(self):
        entry = KITCHEN_DB["Kotlin"]
        assert "Garde Manager" in entry["station"]

    def test_typescript_is_cdp_station(self):
        entry = KITCHEN_DB["TypeScript"]
        assert "Type Saucer" in entry["station"]

    def test_javascript_is_improv_station(self):
        entry = KITCHEN_DB["JavaScript"]
        assert "Improv" in entry["station"]
        assert entry["execution_tag"] == "Event-loop cooking"

    def test_java_is_charcutier_station(self):
        entry = KITCHEN_DB["Java"]
        assert "Charcutier" in entry["station"]

    def test_cpp_is_raw_provisions_station(self):
        entry = KITCHEN_DB["C/C++"]
        assert "Raw Provisions" in entry["station"]
        assert entry["execution_tag"] == "Manual-memory cooking"

    def test_all_plating_styles_are_different(self):
        styles = [data["plating_style"] for data in KITCHEN_DB.values()]
        assert len(styles) == len(set(styles))

    def test_all_station_emojis_are_nonempty(self):
        for lang, data in KITCHEN_DB.items():
            assert data["station_emoji"], f"{lang} missing station_emoji"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])