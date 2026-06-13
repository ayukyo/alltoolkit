"""Comprehensive tests for Polyglot Craft — Language Crafting Recipes."""

import json
import tempfile
from pathlib import Path

import pytest

from polyglot_craft.src.craft import (
    get_current_language,
    advance_rotation,
    generate_craft_card,
    format_craft_card,
    _load_rotation,
    _save_rotation,
    CRAFT_DB,
    ROTATION_ORDER,
    TOOL_NAME,
    TOOL_VERSION,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def rotation_config(tmp_path):
    """Create a temporary language_rotation.json with known state."""
    config = {
        "languages": ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"],
        "current_index": 2,
        "last_language": "Swift",
        "updated_at": "2026-06-12T07:00:00+08:00",
    }
    path = tmp_path / "language_rotation.json"
    path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    return str(path)


@pytest.fixture
def rotation_config_full(tmp_path):
    """Create a temporary language_rotation.json with all 8 languages at index 0."""
    config = {
        "languages": ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"],
        "current_index": 0,
        "last_language": "C/C++",
        "updated_at": "2026-06-12T00:00:00+08:00",
    }
    path = tmp_path / "language_rotation.json"
    path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    return str(path)


@pytest.fixture
def rotation_config_edge(tmp_path):
    """Create a temporary language_rotation.json at last index (C/C++ = 7)."""
    config = {
        "languages": ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"],
        "current_index": 7,
        "last_language": "Java",
        "updated_at": "2026-06-12T00:00:00+08:00",
    }
    path = tmp_path / "language_rotation.json"
    path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    return str(path)


# ---------------------------------------------------------------------------
# Module constants
# ---------------------------------------------------------------------------

def test_tool_name():
    assert TOOL_NAME == "polyglot-craft"
    assert TOOL_VERSION == "1.0.0"


def test_rotation_order_length():
    assert len(ROTATION_ORDER) == 8
    assert len(set(ROTATION_ORDER)) == 8


def test_rotation_order_contains_expected():
    expected = {"Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"}
    assert set(ROTATION_ORDER) == expected


def test_all_languages_have_craft_entries():
    for lang in ROTATION_ORDER:
        assert lang in CRAFT_DB, f"{lang} missing from CRAFT_DB"
        entry = CRAFT_DB[lang]
        assert "mental_model" in entry
        assert "emoji" in entry
        assert "signature_patterns" in entry
        assert len(entry["signature_patterns"]) == 3
        assert "blind_spots" in entry
        assert len(entry["blind_spots"]) == 3
        assert "micro_exercises" in entry
        assert len(entry["micro_exercises"]) == 3


def test_signature_patterns_have_required_fields():
    for lang, entry in CRAFT_DB.items():
        for pat in entry["signature_patterns"]:
            assert "name" in pat
            assert "pattern" in pat
            assert "why" in pat


def test_blind_spots_have_required_fields():
    for lang, entry in CRAFT_DB.items():
        for spot in entry["blind_spots"]:
            assert "from" in spot
            assert "issue" in spot


def test_micro_exercises_have_required_fields():
    for lang, entry in CRAFT_DB.items():
        for ex in entry["micro_exercises"]:
            assert "title" in ex
            assert "snippet" in ex
            assert "concept" in ex


# ---------------------------------------------------------------------------
# Rotation mechanics
# ---------------------------------------------------------------------------

def test_get_current_language_at_known_index(rotation_config):
    assert get_current_language(rotation_config) == "Swift"


def test_advance_rotation_moves_index_forward(rotation_config):
    old_lang = advance_rotation(rotation_config)
    assert old_lang == "Swift"
    data = _load_rotation(rotation_config)
    assert data["current_index"] == 3
    assert data["last_language"] == "Swift"


def test_advance_rotation_wraps_at_end(rotation_config_edge):
    """When at last index (7 = C/C++), advance should wrap to 0 (Rust)."""
    old_lang = advance_rotation(rotation_config_edge)
    assert old_lang == "C/C++"
    data = _load_rotation(rotation_config_edge)
    assert data["current_index"] == 0


def test_full_rotation_cycle(rotation_config_full):
    """All 8 languages should be visited in order before cycling back."""
    visited = []
    for i in range(8):
        lang = get_current_language(rotation_config_full)
        visited.append(lang)
        advance_rotation(rotation_config_full)
    assert visited == ROTATION_ORDER
    # After 8 advances, we're back at index 0
    data = _load_rotation(rotation_config_full)
    assert data["current_index"] == 0


def test_generate_craft_card_does_not_rotate_by_default(rotation_config_full):
    card = generate_craft_card(rotate=False, config_path=rotation_config_full)
    assert card["rotated"] is False
    data = _load_rotation(rotation_config_full)
    assert data["current_index"] == 0


def test_generate_craft_card_rotates_by_default(rotation_config_full):
    card = generate_craft_card(rotate=True, config_path=rotation_config_full)
    assert card["rotated"] is True
    assert card["language"] == "Rust"
    assert card["new_index"] == 1
    data = _load_rotation(rotation_config_full)
    assert data["current_index"] == 1


def test_generate_craft_card_has_required_fields(rotation_config_full):
    card = generate_craft_card(rotate=False, config_path=rotation_config_full)
    assert card["tool"] == TOOL_NAME
    assert card["version"] == TOOL_VERSION
    assert card["language"] == "Rust"
    assert card["current_index"] == 0
    assert "mental_model" in card
    assert "emoji" in card
    assert "signature_patterns" in card
    assert len(card["signature_patterns"]) == 3
    assert "blind_spots" in card
    assert len(card["blind_spots"]) == 3
    assert "micro_exercises" in card
    assert len(card["micro_exercises"]) == 3
    assert "rotation_order" in card
    assert "timestamp" in card


def test_craft_card_language_matches_rotation(rotation_config):
    """Craft card language should match what get_current_language returns."""
    expected_lang = get_current_language(rotation_config)
    card = generate_craft_card(rotate=False, config_path=rotation_config)
    assert card["language"] == expected_lang


# ---------------------------------------------------------------------------
# Formatting
# ---------------------------------------------------------------------------

def test_format_craft_card_returns_string(rotation_config_full):
    card = generate_craft_card(rotate=False, config_path=rotation_config_full)
    output = format_craft_card(card)
    assert isinstance(output, str)
    assert len(output) > 0


def test_format_craft_card_contains_language(rotation_config_full):
    card = generate_craft_card(rotate=False, config_path=rotation_config_full)
    output = format_craft_card(card)
    assert "Rust" in output


def test_format_craft_card_contains_signature_patterns_header(rotation_config_full):
    card = generate_craft_card(rotate=False, config_path=rotation_config_full)
    output = format_craft_card(card)
    assert "SIGNATURE PATTERNS" in output


def test_format_craft_card_contains_blind_spots_header(rotation_config_full):
    card = generate_craft_card(rotate=False, config_path=rotation_config_full)
    output = format_craft_card(card)
    assert "BLIND SPOTS" in output


def test_format_craft_card_contains_micro_exercises_header(rotation_config_full):
    card = generate_craft_card(rotate=False, config_path=rotation_config_full)
    output = format_craft_card(card)
    assert "MICRO-EXERCISES" in output


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_all_eight_languages_produce_valid_cards(tmp_path):
    """Every language in the rotation should produce a valid craft card."""
    for i, lang in enumerate(ROTATION_ORDER):
        config = {
            "languages": list(ROTATION_ORDER),
            "current_index": i,
            "last_language": ROTATION_ORDER[(i - 1) % 8],
            "updated_at": "2026-06-12T00:00:00+08:00",
        }
        path = tmp_path / f"rotation_{i}.json"
        path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
        card = generate_craft_card(rotate=False, config_path=str(path))
        assert card["language"] == lang
        assert card["current_index"] == i
        assert len(card["signature_patterns"]) == 3
        assert len(card["blind_spots"]) == 3
        assert len(card["micro_exercises"]) == 3
        assert card["mental_model"] != "?"


def test_updated_at_changes_after_advance(rotation_config_full):
    data_before = _load_rotation(rotation_config_full)
    old_updated = data_before["updated_at"]
    advance_rotation(rotation_config_full)
    data_after = _load_rotation(rotation_config_full)
    assert data_after["updated_at"] != old_updated


def test_last_language_records_previous_language(rotation_config_full):
    old_lang = get_current_language(rotation_config_full)
    advance_rotation(rotation_config_full)
    data = _load_rotation(rotation_config_full)
    assert data["last_language"] == old_lang
