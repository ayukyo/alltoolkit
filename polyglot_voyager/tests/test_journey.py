"""Tests for Polyglot Voyager journey module."""

import json
import os
import sys
import tempfile
from pathlib import Path

import pytest

sys.path.insert(0, '/home/admin/.openclaw/workspace/AllToolkit')

from polyglot_voyager.src.journey import (
    advance_and_log,
    get_journey_snapshot,
    get_polyglot_map,
    _emoji_stamp,
    _load_journey_log,
    _save_journey_log,
    DEFAULT_ROTATION_CONFIG,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_rotation_file(path: str, languages: list, current_index: int) -> None:
    data = {
        "languages": languages,
        "current_index": current_index,
        "last_language": languages[current_index],
        "updated_at": "2026-06-19T07:21:00+08:00",
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f)


def make_journey_log(path: str, total: int = 0, visited: list = None, journey: list = None) -> None:
    data = {
        "total_visits": total,
        "languages_visited": visited or [],
        "journey": journey or [],
    }
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f)


# ---------------------------------------------------------------------------
# Tests — _emoji_stamp
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("language,expected", [
    ("Rust", "🦀"),
    ("Go", "🐹"),
    ("Swift", "🦅"),
    ("Kotlin", "🧃"),
    ("TypeScript", "📘"),
    ("JavaScript", "📒"),
    ("Java", "☕"),
    ("C/C++", "⚙️"),
    ("Zig", "🔮"),
])
def test_emoji_stamp_returns_correct_emoji(language, expected):
    assert _emoji_stamp(language) == expected


# ---------------------------------------------------------------------------
# Tests — get_journey_snapshot
# ---------------------------------------------------------------------------

def test_snapshot_returns_current_language(tmp_path):
    config = tmp_path / "rotation.json"
    make_rotation_file(str(config), ["Rust", "Go", "Swift"], 0)

    result = get_journey_snapshot(config_path=str(config))

    assert result["current_language"] == "Rust"
    assert result["current_index"] == 0
    assert result["total_languages"] == 3


def test_snapshot_does_not_modify_index(tmp_path):
    config = tmp_path / "rotation.json"
    make_rotation_file(str(config), ["Rust", "Go", "Swift"], 1)

    get_journey_snapshot(config_path=str(config))
    result2 = get_journey_snapshot(config_path=str(config))

    assert result2["current_index"] == 1


# ---------------------------------------------------------------------------
# Tests — advance_and_log
# ---------------------------------------------------------------------------

def test_advance_rotates_to_next_language(tmp_path):
    config = tmp_path / "rotation.json"
    journey_log = tmp_path / "journey.json"
    make_rotation_file(str(config), ["Rust", "Go", "Swift", "Kotlin"], 1)
    make_journey_log(str(journey_log))

    result = advance_and_log(
        config_path=str(config),
        journey_log_path=str(journey_log),
    )

    assert result["previous_language"] == "Go"
    assert result["current_language"] == "Swift"
    assert result["current_index"] == 2


def test_advance_circular_rotation_wraps(tmp_path):
    config = tmp_path / "rotation.json"
    journey_log = tmp_path / "journey.json"
    make_rotation_file(str(config), ["Rust", "Go"], 1)  # last index
    make_journey_log(str(journey_log))

    result = advance_and_log(
        config_path=str(config),
        journey_log_path=str(journey_log),
    )

    assert result["current_language"] == "Rust"
    assert result["current_index"] == 0


def test_advance_updates_rotation_json(tmp_path):
    config = tmp_path / "rotation.json"
    journey_log = tmp_path / "journey.json"
    make_rotation_file(str(config), ["Rust", "Go"], 0)
    make_journey_log(str(journey_log))

    advance_and_log(config_path=str(config), journey_log_path=str(journey_log))

    with open(config, "r") as f:
        data = json.load(f)
    assert data["current_index"] == 1
    assert data["last_language"] == "Go"


def test_advance_appends_to_journey_log(tmp_path):
    config = tmp_path / "rotation.json"
    journey_log = tmp_path / "journey.json"
    make_rotation_file(str(config), ["Rust", "Go", "Swift"], 0)
    make_journey_log(str(journey_log))

    result1 = advance_and_log(config_path=str(config), journey_log_path=str(journey_log))
    result2 = advance_and_log(config_path=str(config), journey_log_path=str(journey_log))

    assert result1["current_language"] == "Go"
    assert result2["current_language"] == "Swift"
    assert result1["total_visits"] == 1
    assert result2["total_visits"] == 2


def test_advance_tracks_unique_languages_visited(tmp_path):
    config = tmp_path / "rotation.json"
    journey_log = tmp_path / "journey.json"
    make_rotation_file(str(config), ["Rust", "Go", "Rust"], 0)
    make_journey_log(str(journey_log))

    r1 = advance_and_log(config_path=str(config), journey_log_path=str(journey_log))
    r2 = advance_and_log(config_path=str(config), journey_log_path=str(journey_log))
    r3 = advance_and_log(config_path=str(config), journey_log_path=str(journey_log))

    # Rotation: index 0→Rust, 1→Go, 2→Rust(wrap), 0→Rust
    assert r1["current_language"] == "Go"
    assert r2["current_language"] == "Rust"
    assert r3["current_language"] == "Rust"  # wrapped back to index 0

    assert r1["languages_visited"] == ["Go"]
    assert r2["languages_visited"] == ["Go", "Rust"]
    assert r3["languages_visited"] == ["Go", "Rust"]


def test_advance_returns_passport_stamps(tmp_path):
    config = tmp_path / "rotation.json"
    journey_log = tmp_path / "journey.json"
    make_rotation_file(str(config), ["Rust", "Go", "Swift"], 0)
    make_journey_log(str(journey_log))

    result = advance_and_log(config_path=str(config), journey_log_path=str(journey_log))

    assert result["current_language"] == "Go"
    assert result["passport_stamps"] == ["🐹"]


def test_advance_returns_recent_journey(tmp_path):
    config = tmp_path / "rotation.json"
    journey_log = tmp_path / "journey.json"
    make_rotation_file(str(config), ["Rust", "Go", "Swift"], 0)
    make_journey_log(str(journey_log))

    advance_and_log(config_path=str(config), journey_log_path=str(journey_log))
    result = advance_and_log(config_path=str(config), journey_log_path=str(journey_log))

    assert len(result["journey"]) == 2
    assert result["journey"][-1]["language"] == "Swift"


# ---------------------------------------------------------------------------
# Tests — get_polyglot_map
# ---------------------------------------------------------------------------

def test_map_shows_visited_and_unvisited(tmp_path):
    journey_log = tmp_path / "journey.json"
    make_journey_log(str(journey_log), total=3, visited=["Rust", "Go"], journey=[
        {"language": "Rust", "stamp": "🦀"},
        {"language": "Go", "stamp": "🐹"},
        {"language": "Rust", "stamp": "🦀"},
    ])

    result = get_polyglot_map(journey_log_path=str(journey_log))

    assert result["visited"] == ["Rust", "Go"]
    assert "Swift" in result["not_yet_visited"]
    assert result["total_visits"] == 3
    assert result["map_legend"]["visited"] == "🌍"


def test_map_with_no_visits(tmp_path):
    journey_log = tmp_path / "journey.json"
    make_journey_log(str(journey_log))

    result = get_polyglot_map(journey_log_path=str(journey_log))

    assert result["visited"] == []
    assert len(result["not_yet_visited"]) == 8
    assert result["total_visits"] == 0


# ---------------------------------------------------------------------------
# Integration-like tests with real workspace rotation
# ---------------------------------------------------------------------------

def test_rotation_sequence_full_cycle(tmp_path):
    """Verify full cycle: Rust→Go→Swift→Kotlin→TS→JS→Java→C/C++→Rust."""
    config = tmp_path / "rotation.json"
    journey_log = tmp_path / "journey.json"
    languages = ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"]
    make_rotation_file(str(config), languages, 0)
    make_journey_log(str(journey_log))

    expected = ["Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++", "Rust"]

    for expected_lang in expected:
        result = advance_and_log(config_path=str(config), journey_log_path=str(journey_log))
        assert result["current_language"] == expected_lang, \
            f"Expected {expected_lang}, got {result['current_language']}"


def test_index_cycles_correctly(tmp_path):
    """Index should cycle 0→1→2→3→4→5→6→7→0→1..."""
    config = tmp_path / "rotation.json"
    journey_log = tmp_path / "journey.json"
    make_rotation_file(str(config), ["A", "B", "C"], 0)
    make_journey_log(str(journey_log))

    indices = []
    for _ in range(6):
        result = advance_and_log(config_path=str(config), journey_log_path=str(journey_log))
        indices.append(result["current_index"])

    assert indices == [1, 2, 0, 1, 2, 0]
