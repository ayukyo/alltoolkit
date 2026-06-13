#!/usr/bin/env python3
"""
Tests for Polyglot Cartographer.
Run with: pytest tests/ -v
"""

import json
import os
import tempfile
from pathlib import Path

import pytest

import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from cartographer import (
    TOOL_NAME,
    TOOL_VERSION,
    ROTATION_ORDER,
    NATION_DB,
    TRADE_ROUTES,
    get_current_language,
    get_nation_data,
    get_trade_routes_for_language,
    generate_world_report,
    format_world_report,
)


# ─────────────────────────────────────────────────────────────────────────────
# Fixtures
# ─────────────────────────────────────────────────────────────────────────────

@pytest.fixture
def rotation_config():
    """A minimal rotation config for testing."""
    return {
        "languages": ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"],
        "current_index": 0,
        "last_language": "C/C++",
        "updated_at": "2026-06-14T04:00:00+08:00",
    }


@pytest.fixture
def temp_config_file(rotation_config):
    """Create a temporary config file."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False
    ) as f:
        json.dump(rotation_config, f, indent=2)
        f.write("\n")
        path = f.name
    yield path
    os.unlink(path)


# ─────────────────────────────────────────────────────────────────────────────
# Basic module tests
# ─────────────────────────────────────────────────────────────────────────────

class TestModuleConstants:
    def test_tool_name(self):
        assert TOOL_NAME == "polyglot-cartographer"

    def test_tool_version(self):
        assert TOOL_VERSION == "1.0.0"

    def test_rotation_order(self):
        assert ROTATION_ORDER == [
            "Rust", "Go", "Swift", "Kotlin",
            "TypeScript", "JavaScript", "Java", "C/C++",
        ]
        assert len(ROTATION_ORDER) == 8

    def test_nation_db_has_all_languages(self):
        for lang in ROTATION_ORDER:
            assert lang in NATION_DB, f"{lang} not in NATION_DB"

    def test_nation_db_has_required_fields(self):
        required_fields = [
            "nation_name", "terrain", "climate", "government",
            "economy", "imports", "exports", "border_policy",
            "unique_features", "cartography_symbol", "map_color",
            "diplomatic_status", "cartographer_note",
        ]
        for lang in ROTATION_ORDER:
            for field in required_fields:
                assert field in NATION_DB[lang], f"{lang} missing {field}"

    def test_trade_routes_exist(self):
        assert len(TRADE_ROUTES) > 0
        for route in TRADE_ROUTES:
            assert "from" in route
            assert "to" in route
            assert "routes" in route
            assert route["from"] in ROTATION_ORDER
            assert route["to"] in ROTATION_ORDER


# ─────────────────────────────────────────────────────────────────────────────
# get_current_language
# ─────────────────────────────────────────────────────────────────────────────

class TestGetCurrentLanguage:
    def test_returns_rust_at_index_0(self, temp_config_file):
        assert get_current_language(temp_config_file) == "Rust"

    def test_returns_go_at_index_1(self, rotation_config, temp_config_file):
        rotation_config["current_index"] = 1
        with open(temp_config_file, "w") as f:
            json.dump(rotation_config, f, indent=2)
            f.write("\n")
        assert get_current_language(temp_config_file) == "Go"

    def test_wraps_around_at_end(self, rotation_config, temp_config_file):
        rotation_config["current_index"] = 7  # C/C++
        with open(temp_config_file, "w") as f:
            json.dump(rotation_config, f, indent=2)
            f.write("\n")
        assert get_current_language(temp_config_file) == "C/C++"


# ─────────────────────────────────────────────────────────────────────────────
# get_nation_data
# ─────────────────────────────────────────────────────────────────────────────

class TestGetNationData:
    def test_returns_rust_data(self):
        data = get_nation_data("Rust")
        assert data is not None
        assert data["nation_name"] == "The Ownership Republic"
        assert data["terrain"] == "Mountain Highlands"
        assert "resource" in data["economy"].lower()

    def test_returns_js_data(self):
        data = get_nation_data("JavaScript")
        assert data is not None
        assert data["nation_name"] == "The Coastal Trade Empire"
        assert data["terrain"] == "Coastal Archipelago"

    def test_returns_none_for_unknown(self):
        assert get_nation_data("Pascal") is None


# ─────────────────────────────────────────────────────────────────────────────
# get_trade_routes_for_language
# ─────────────────────────────────────────────────────────────────────────────

class TestGetTradeRoutesForLanguage:
    def test_rust_has_trade_route_to_cpp(self):
        routes = get_trade_routes_for_language("Rust")
        partner_nations = [r["to"] if r["from"] == "Rust" else r["from"] for r in routes]
        assert "C/C++" in partner_nations

    def test_js_has_trade_route_to_typescript(self):
        routes = get_trade_routes_for_language("JavaScript")
        partner_nations = [r["to"] if r["from"] == "JavaScript" else r["from"] for r in routes]
        assert "TypeScript" in partner_nations

    def test_go_has_trade_routes(self):
        routes = get_trade_routes_for_language("Go")
        assert len(routes) >= 2

    def test_kotlin_valley_routes_to_java(self):
        routes = get_trade_routes_for_language("Kotlin")
        partner_nations = [r["to"] if r["from"] == "Kotlin" else r["from"] for r in routes]
        assert "Java" in partner_nations


# ─────────────────────────────────────────────────────────────────────────────
# generate_world_report
# ─────────────────────────────────────────────────────────────────────────────

class TestGenerateWorldReport:
    def test_returns_correct_language_at_index_0(self, temp_config_file):
        report = generate_world_report(rotate=False, config_path=temp_config_file)
        assert report["language"] == "Rust"
        assert report["current_index"] == 0
        assert report["rotated"] is False
        assert report["new_index"] is None

    def test_advances_index_when_rotate_true(self, rotation_config, temp_config_file):
        report = generate_world_report(rotate=True, config_path=temp_config_file)
        assert report["language"] == "Rust"
        assert report["new_index"] == 1
        assert report["rotated"] is True
        # Config should be updated
        with open(temp_config_file) as f:
            saved = json.load(f)
        assert saved["current_index"] == 1
        assert saved["last_language"] == "Rust"

    def test_report_contains_all_required_fields(self, temp_config_file):
        report = generate_world_report(rotate=False, config_path=temp_config_file)
        required = [
            "tool", "version", "language", "current_index", "new_index",
            "rotated", "nation_name", "terrain", "climate", "government",
            "economy", "imports", "exports", "border_policy", "unique_features",
            "cartography_symbol", "map_color", "trade_routes",
            "diplomatic_status", "cartographer_note", "world_map",
            "rotation_order", "timestamp",
        ]
        for field in required:
            assert field in report, f"Missing field: {field}"

    def test_nation_name_for_current_language(self, temp_config_file):
        report = generate_world_report(rotate=False, config_path=temp_config_file)
        assert report["nation_name"] == "The Ownership Republic"
        assert report["government"] == "Constitutional Council (Ownership Constitution)"

    def test_trade_routes_include_partners(self, temp_config_file):
        report = generate_world_report(rotate=False, config_path=temp_config_file)
        assert len(report["trade_routes"]) > 0
        partner_nations = [
            r["to"] if r["from"] == "Rust" else r["from"]
            for r in report["trade_routes"]
        ]
        assert "C/C++" in partner_nations

    def test_world_map_is_multiline_string(self, temp_config_file):
        report = generate_world_report(rotate=False, config_path=temp_config_file)
        assert isinstance(report["world_map"], str)
        assert len(report["world_map"].splitlines()) > 5

    def test_timestamp_is_iso_format(self, temp_config_file):
        report = generate_world_report(rotate=False, config_path=temp_config_file)
        assert "T" in report["timestamp"]
        assert "+" in report["timestamp"] or "Z" in report["timestamp"]

    def test_full_rotation_cycle(self, rotation_config, temp_config_file):
        """Test that rotating through all languages produces correct sequence."""
        languages_seen = []
        for i in range(8):
            report = generate_world_report(rotate=True, config_path=temp_config_file)
            languages_seen.append(report["language"])

        assert languages_seen == [
            "Rust", "Go", "Swift", "Kotlin",
            "TypeScript", "JavaScript", "Java", "C/C++",
        ]

    def test_cpp_at_end_of_rotation_wraps_to_rust(self, rotation_config, temp_config_file):
        """After C/C++ (index 7), rotation should wrap to Rust (index 0)."""
        # Set to C/C++
        rotation_config["current_index"] = 7
        with open(temp_config_file, "w") as f:
            json.dump(rotation_config, f, indent=2)
            f.write("\n")

        # Rotate once
        report = generate_world_report(rotate=True, config_path=temp_config_file)
        assert report["language"] == "C/C++"
        assert report["new_index"] == 0

        # Verify saved config wraps
        with open(temp_config_file) as f:
            saved = json.load(f)
        assert saved["current_index"] == 0


# ─────────────────────────────────────────────────────────────────────────────
# format_world_report
# ─────────────────────────────────────────────────────────────────────────────

class TestFormatWorldReport:
    def test_returns_multiline_string(self, temp_config_file):
        report = generate_world_report(rotate=False, config_path=temp_config_file)
        formatted = format_world_report(report)
        assert isinstance(formatted, str)
        assert len(formatted.splitlines()) > 10

    def test_contains_language_name(self, temp_config_file):
        report = generate_world_report(rotate=False, config_path=temp_config_file)
        formatted = format_world_report(report)
        assert "Rust" in formatted

    def test_contains_nation_name(self, temp_config_file):
        report = generate_world_report(rotate=False, config_path=temp_config_file)
        formatted = format_world_report(report)
        assert "Ownership Republic" in formatted

    def test_contains_terrain(self, temp_config_file):
        report = generate_world_report(rotate=False, config_path=temp_config_file)
        formatted = format_world_report(report)
        assert "Mountain Highlands" in formatted

    def test_contains_government(self, temp_config_file):
        report = generate_world_report(rotate=False, config_path=temp_config_file)
        formatted = format_world_report(report)
        assert "Constitutional Council" in formatted

    def test_contains_border_policy(self, temp_config_file):
        report = generate_world_report(rotate=False, config_path=temp_config_file)
        formatted = format_world_report(report)
        assert "border" in formatted.lower() or "Border" in formatted

    def test_contains_trade_routes(self, temp_config_file):
        report = generate_world_report(rotate=False, config_path=temp_config_file)
        formatted = format_world_report(report)
        assert "C/C++" in formatted

    def test_contains_diplomatic_status(self, temp_config_file):
        report = generate_world_report(rotate=False, config_path=temp_config_file)
        formatted = format_world_report(report)
        assert "Go" in formatted  # Rust-Go diplomatic status

    def test_contains_cartographer_note(self, temp_config_file):
        report = generate_world_report(rotate=False, config_path=temp_config_file)
        formatted = format_world_report(report)
        assert "borro" in formatted.lower() or "memory" in formatted.lower()

    def test_contains_rotation_order(self, temp_config_file):
        report = generate_world_report(rotate=False, config_path=temp_config_file)
        formatted = format_world_report(report)
        assert "Rust → Go → Swift" in formatted

    def test_box_drawing_characters(self, temp_config_file):
        report = generate_world_report(rotate=False, config_path=temp_config_file)
        formatted = format_world_report(report)
        assert "╔" in formatted
        assert "║" in formatted
        assert "╚" in formatted


# ─────────────────────────────────────────────────────────────────────────────
# Integration: config persistence
# ─────────────────────────────────────────────────────────────────────────────

class TestConfigPersistence:
    def test_updated_at_changes_after_rotation(self, rotation_config, temp_config_file):
        report = generate_world_report(rotate=True, config_path=temp_config_file)
        with open(temp_config_file) as f:
            saved = json.load(f)
        assert saved["updated_at"] != rotation_config["updated_at"]
        assert "T" in saved["updated_at"]

    def test_last_language_is_set(self, rotation_config, temp_config_file):
        report = generate_world_report(rotate=True, config_path=temp_config_file)
        with open(temp_config_file) as f:
            saved = json.load(f)
        assert saved["last_language"] == "Rust"

    def test_languages_list_unchanged_after_rotation(self, rotation_config, temp_config_file):
        generate_world_report(rotate=True, config_path=temp_config_file)
        with open(temp_config_file) as f:
            saved = json.load(f)
        assert saved["languages"] == rotation_config["languages"]


# ─────────────────────────────────────────────────────────────────────────────
# Edge cases
# ─────────────────────────────────────────────────────────────────────────────

class TestEdgeCases:
    def test_unknown_language_returns_none(self):
        assert get_nation_data("COBOL") is None

    def test_empty_trade_routes_language_has_empty_list(self):
        # All languages in ROTATION_ORDER should have at least some routes
        for lang in ROTATION_ORDER:
            routes = get_trade_routes_for_language(lang)
            # Every language should have at least one trade route partner
            assert len(routes) >= 1, f"{lang} has no trade routes"

    def test_all_languages_have_unique_symbols(self):
        symbols = [NATION_DB[lang]["cartography_symbol"] for lang in ROTATION_ORDER]
        assert len(symbols) == len(set(symbols)), "Duplicate cartography symbols found"

    def test_all_languages_have_unique_map_colors(self):
        colors = [NATION_DB[lang]["map_color"] for lang in ROTATION_ORDER]
        assert len(colors) == len(set(colors)), "Duplicate map colors found"

    def test_all_nations_have_imports_and_exports(self):
        for lang in ROTATION_ORDER:
            nation = NATION_DB[lang]
            assert len(nation["imports"]) > 0, f"{lang} has no imports"
            assert len(nation["exports"]) > 0, f"{lang} has no exports"