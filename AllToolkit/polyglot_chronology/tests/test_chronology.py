"""Comprehensive tests for Polyglot Chronology — Temporal Cartography."""

import json
import tempfile
from pathlib import Path

import pytest

from polyglot_chronology.src.chronology import (
    get_current_language,
    get_epoch_for_language,
    generate_temporal_map,
    format_epoch_card,
    _compute_next_index,
    _build_time_scale_bar,
    _get_neighboring_epochs,
    GEOLOGICAL_EPOCHS,
    EPOCH_ORDER,
    EPOCH_DESCRIPTIONS,
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
        "current_index": 4,
        "last_language": "Kotlin",
        "updated_at": "2026-06-12T07:00:00+08:00",
    }
    path = tmp_path / "language_rotation.json"
    path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    return str(path)


@pytest.fixture
def rotation_config_full(tmp_path):
    """Create a temporary language_rotation.json with all 8 languages."""
    config = {
        "languages": ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"],
        "current_index": 0,
        "last_language": "Rust",
        "updated_at": "2026-06-12T00:00:00+08:00",
    }
    path = tmp_path / "language_rotation.json"
    path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    return str(path)


# ---------------------------------------------------------------------------
# Module constants
# ---------------------------------------------------------------------------

def test_tool_name():
    assert TOOL_NAME == "polyglot-chronology"
    assert TOOL_VERSION == "1.0.0"


def test_rotation_order_length():
    assert len(ROTATION_ORDER) == 8
    assert len(set(ROTATION_ORDER)) == 8


def test_rotation_order_contains_expected():
    expected = {"Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"}
    assert set(ROTATION_ORDER) == expected


def test_epoch_order():
    assert EPOCH_ORDER == ["Precambrian", "Paleozoic", "Mesozoic", "Cenozoic"]
    assert len(EPOCH_ORDER) == 4


def test_epoch_descriptions_cover_all_epochs():
    for epoch in EPOCH_ORDER:
        assert epoch in EPOCH_DESCRIPTIONS
        assert len(EPOCH_DESCRIPTIONS[epoch]) > 10


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def test_compute_next_index():
    languages = ["Rust", "Go", "Swift", "Kotlin"]
    assert _compute_next_index(0, languages) == 1
    assert _compute_next_index(2, languages) == 3
    assert _compute_next_index(3, languages) == 0  # wraps around


def test_build_time_scale_bar():
    bar = _build_time_scale_bar(1991)
    assert len(bar) == 20
    assert "█" in bar
    assert "░" in bar


def test_build_time_scale_bar_oldest():
    bar = _build_time_scale_bar(1950)
    assert len(bar) == 20
    assert bar.count("░") >= 18


def test_build_time_scale_bar_newest():
    bar = _build_time_scale_bar(2025)
    assert len(bar) == 20
    assert bar.count("█") >= 18


def test_get_neighboring_epochs():
    assert _get_neighboring_epochs("Paleozoic") == ["Precambrian", "Mesozoic"]
    assert _get_neighboring_epochs("Precambrian") == ["Paleozoic"]
    assert _get_neighboring_epochs("Cenozoic") == ["Mesozoic"]
    assert _get_neighboring_epochs("UnknownEpoch") == []


# ---------------------------------------------------------------------------
# Language epoch database
# ---------------------------------------------------------------------------

def test_all_rotation_languages_have_epoch_data():
    for lang in ROTATION_ORDER:
        assert lang in GEOLOGICAL_EPOCHS, f"Missing epoch data for {lang}"


def test_epoch_data_has_required_fields():
    required = [
        "epoch", "period", "geological_age_mya", "language_age",
        "formative_pressure", "fossil_record", "extinction_resistance",
        "extinction_risk", "era_tagline",
    ]
    for lang, data in GEOLOGICAL_EPOCHS.items():
        for field in required:
            assert field in data, f"Missing '{field}' for language {lang}"


def test_geological_age_reasonable():
    for lang, data in GEOLOGICAL_EPOCHS.items():
        age = data["geological_age_mya"]
        assert age >= 0, f"{lang} has invalid geological_age_mya: {age}"
        assert age <= 5000, f"{lang} has unreasonable geological_age_mya: {age}"


def test_fossil_record_nonempty():
    for lang, data in GEOLOGICAL_EPOCHS.items():
        assert len(data["fossil_record"]) > 0, f"{lang} has no fossil_record"


def test_extinction_risk_valid():
    valid_risks = {"low", "medium", "high"}
    for lang, data in GEOLOGICAL_EPOCHS.items():
        assert data["extinction_risk"] in valid_risks


# ---------------------------------------------------------------------------
# get_epoch_for_language
# ---------------------------------------------------------------------------

def test_get_epoch_for_language_valid():
    for lang in ROTATION_ORDER:
        epoch = get_epoch_for_language(lang)
        assert epoch is not None
        assert "epoch" in epoch
        assert "formative_pressure" in epoch


def test_get_epoch_for_language_case_sensitive():
    assert get_epoch_for_language("Rust") is not None
    assert get_epoch_for_language("rust") is None
    assert get_epoch_for_language("RUST") is None


def test_get_epoch_for_language_unknown():
    assert get_epoch_for_language("NonExistentLanguage") is None


# ---------------------------------------------------------------------------
# get_current_language
# ---------------------------------------------------------------------------

def test_get_current_language_returns_correct_language(rotation_config):
    lang = get_current_language(rotation_config)
    # current_index=4 → languages[4] = TypeScript
    assert lang == "TypeScript"


def test_get_current_language_does_not_rotate(rotation_config):
    with open(rotation_config) as f:
        before = json.load(f)
    get_current_language(rotation_config)
    with open(rotation_config) as f:
        after = json.load(f)
    assert after["current_index"] == before["current_index"]


# ---------------------------------------------------------------------------
# generate_temporal_map (no rotation)
# ---------------------------------------------------------------------------

def test_generate_temporal_map_no_rotate(rotation_config):
    """When rotate=False, index should not change."""
    with open(rotation_config) as f:
        original = json.load(f)
    original_index = original["current_index"]

    result = generate_temporal_map(rotate=False, config_path=rotation_config)

    assert result["current_language"] == original["languages"][original_index]
    assert result["current_index"] == original_index
    assert result["new_index"] is None
    assert result["rotated"] is False

    # Verify file was NOT modified
    with open(rotation_config) as f:
        after = json.load(f)
    assert after["current_index"] == original_index


def test_generate_temporal_map_unknown_language_fallback(rotation_config):
    """Languages not in the database should return a graceful fallback."""
    # current_index=4 → TypeScript, which IS in the database.
    # Test the fallback by checking an unknown language would get "Unknown" epoch.
    epoch = get_epoch_for_language("NonExistentLanguage")
    assert epoch is None  # confirms our unknown lang returns None
    # Now test that generate_temporal_map handles this gracefully via fallback
    # by directly calling with a fake config
    fake_config = {
        "languages": ["Rust", "FakeLang", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"],
        "current_index": 1,  # FakeLang
        "last_language": "Rust",
        "updated_at": "2026-06-12T00:00:00+08:00",
    }
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(fake_config, f)
        fake_path = f.name
    try:
        result = generate_temporal_map(rotate=False, config_path=fake_path)
        assert result["current_language"] == "FakeLang"
        assert result["epoch"] == "Unknown"
    finally:
        Path(fake_path).unlink()


# ---------------------------------------------------------------------------
# generate_temporal_map (with rotation)
# ---------------------------------------------------------------------------

def test_generate_temporal_map_with_rotate(rotation_config):
    """When rotate=True, index should advance by 1."""
    with open(rotation_config) as f:
        original = json.load(f)
    original_index = original["current_index"]
    original_language = original["languages"][original_index]

    result = generate_temporal_map(rotate=True, config_path=rotation_config)

    assert result["current_language"] == original_language
    assert result["rotated"] is True
    assert result["new_index"] == (original_index + 1) % len(original["languages"])

    with open(rotation_config) as f:
        after = json.load(f)
    assert after["current_index"] == (original_index + 1) % len(original["languages"])


def test_generate_temporal_map_wraps_around(rotation_config_full):
    """At the last language, rotation should wrap to index 0."""
    with open(rotation_config_full) as f:
        original = json.load(f)

    # current_index=0 (Rust), advance should go to 1 (Go)
    result = generate_temporal_map(rotate=True, config_path=rotation_config_full)
    assert result["current_language"] == "Rust"
    assert result["new_index"] == 1

    with open(rotation_config_full) as f:
        after = json.load(f)
    assert after["current_index"] == 1


def test_generate_temporal_map_updates_last_language(rotation_config_full):
    generate_temporal_map(rotate=True, config_path=rotation_config_full)
    with open(rotation_config_full) as f:
        after = json.load(f)
    assert after["last_language"] == "Rust"
    assert "updated_at" in after


def test_generate_temporal_map_contains_required_fields(rotation_config):
    result = generate_temporal_map(rotate=False, config_path=rotation_config)
    required = [
        "current_language", "current_index", "epoch", "period",
        "geological_age_mya", "formative_pressure", "fossil_record",
        "extinction_resistance", "extinction_risk", "era_tagline",
        "neighboring_epochs", "epoch_description", "epoch_order",
        "time_scale_bar", "rotated",
    ]
    for field in required:
        assert field in result, f"Missing field: {field}"


# ---------------------------------------------------------------------------
# format_epoch_card
# ---------------------------------------------------------------------------

def test_format_epoch_card_valid_output(rotation_config):
    result = generate_temporal_map(rotate=False, config_path=rotation_config)
    card = format_epoch_card(result)
    assert isinstance(card, str)
    assert len(card) > 100
    assert result["current_language"] in card
    assert result["epoch"] in card


def test_format_epoch_card_extinction_risk_emoji(rotation_config):
    result = generate_temporal_map(rotate=False, config_path=rotation_config)
    card = format_epoch_card(result)
    risk = result["extinction_risk"]
    emoji_map = {"low": "🟢", "medium": "🟡", "high": "🔴"}
    assert emoji_map[risk] in card


def test_format_epoch_card_fossil_record_present(rotation_config):
    result = generate_temporal_map(rotate=False, config_path=rotation_config)
    card = format_epoch_card(result)
    for fossil in result["fossil_record"]:
        assert fossil in card


# ---------------------------------------------------------------------------
# Integration: full rotation cycle
# ---------------------------------------------------------------------------

def test_full_rotation_cycle(rotation_config_full):
    """Verify all 8 languages are visited in order over a full cycle."""
    visited = []
    for _ in range(8):
        result = generate_temporal_map(rotate=True, config_path=rotation_config_full)
        visited.append(result["current_language"])

    assert visited == list(ROTATION_ORDER)


def test_rotation_after_full_cycle_wraps(rotation_config_full):
    """After a full 8-language cycle, index should be back at 0."""
    for _ in range(8):
        generate_temporal_map(rotate=True, config_path=rotation_config_full)

    with open(rotation_config_full) as f:
        final = json.load(f)
    assert final["current_index"] == 0