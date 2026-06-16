"""
Tests for Polyglot Odyssey
Run with: pytest tests/ -v
"""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path

import pytest

from polyglot_odyssey import (
    OdysseyState,
    format_odyssey,
    ROTATION,
    PARADIGM,
    TRANSITIONS,
    WAYPOINTS,
    STATE_FILE,
)


# ---------------------------------------------------------------------------
# Constants that must hold true
# ---------------------------------------------------------------------------

def test_rotation_order():
    """Rotation must be exactly the specified order."""
    assert ROTATION == [
        "Rust", "Go", "Swift", "Kotlin",
        "TypeScript", "JavaScript", "Java", "C/C++",
    ]


def test_all_languages_have_paradigm():
    """Every language in rotation must have paradigm metadata."""
    for lang in ROTATION:
        assert lang in PARADIGM, f"{lang} missing from PARADIGM"
        assert "tagline" in PARADIGM[lang]
        assert "superpower" in PARADIGM[lang]
        assert "motto" in PARADIGM[lang]


def test_all_languages_have_waypoints():
    """Every language in rotation must have waypoints."""
    for lang in ROTATION:
        assert lang in WAYPOINTS, f"{lang} missing from WAYPOINTS"
        assert len(WAYPOINTS[lang]) >= 2, f"{lang} needs at least 2 waypoints"


def test_transitions_cover_all_pairs():
    """Every adjacent pair in the rotation must have a transition story."""
    for i in range(len(ROTATION)):
        a = ROTATION[i]
        b = ROTATION[(i + 1) % len(ROTATION)]
        assert (a, b) in TRANSITIONS, f"Missing transition: {a} → {b}"


# ---------------------------------------------------------------------------
# OdysseyState
# ---------------------------------------------------------------------------

def test_load_bootstrap_default_state(tmp_path):
    """When the state file doesn't exist, load() bootstraps defaults."""
    state = OdysseyState.load(tmp_path / "nonexistent.json")
    assert state.languages == ROTATION
    assert state.current_index == 0
    assert state.last_language == "C/C++"
    assert state.total_legs == 0
    assert state.journey_log == []


def test_save_and_reload(tmp_path):
    """State persists correctly across save/load round-trip."""
    state1 = OdysseyState.load(tmp_path / "rotate.json")
    state1.advance()  # C/C++ → Rust
    path = tmp_path / "rotate.json"
    state1.save(path)

    state2 = OdysseyState.load(path)
    assert state2.last_language == "Rust"
    assert state2.total_legs == 1
    assert len(state2.journey_log) == 1


def test_advance_cpp_to_rust(tmp_path):
    """Bootstrap C/C++ → Rust is the first leg."""
    state = OdysseyState.load(tmp_path / "rotate.json")
    from_lang, to_lang, story, waypoints, leg = state.advance()

    assert from_lang == "C/C++"
    assert to_lang == "Rust"
    assert leg == 1
    assert len(story) > 10
    assert len(waypoints) == 2
    assert all(w in WAYPOINTS["Rust"] for w in waypoints)


def test_advance_rust_to_go(tmp_path):
    """Second leg: Rust → Go."""
    state = OdysseyState.load(tmp_path / "rotate.json")
    state.advance()  # C/C++ → Rust
    _, to_lang, _, _, _ = state.advance()  # Rust → Go

    assert to_lang == "Go"


def test_advance_wraps_around(tmp_path):
    """After 8 advances we cycle back to C/C++."""
    state = OdysseyState.load(tmp_path / "rotate.json")
    for _ in range(8):
        state.advance()
    # Now last_language should be C/C++ again
    assert state.last_language == "C/C++"
    assert state.total_legs == 8


def test_current_index_updates(tmp_path):
    """current_index advances by 1 each leg."""
    state = OdysseyState.load(tmp_path / "rotate.json")
    indices = []
    for _ in range(len(ROTATION)):
        indices.append(state.current_index)
        state.advance()
    # After each advance, index should have incremented
    assert indices == list(range(len(ROTATION)))


def test_journey_log_records_all_legs(tmp_path):
    """Every leg appends an entry to journey_log."""
    state = OdysseyState.load(tmp_path / "rotate.json")
    for i in range(5):
        state.advance()
    assert len(state.journey_log) == 5
    assert [e.leg for e in state.journey_log] == [1, 2, 3, 4, 5]


def test_journey_log_entry_fields(tmp_path):
    """Each journey log entry has all required fields."""
    state = OdysseyState.load(tmp_path / "rotate.json")
    _, _, _, waypoints, leg = state.advance()
    entry = state.journey_log[0]

    assert entry.leg == 1
    assert entry.from_lang == "C/C++"
    assert entry.to_lang == "Rust"
    assert isinstance(entry.transition_story, str)
    assert len(entry.transition_story) > 0
    assert entry.waypoints == waypoints
    assert entry.timestamp


def test_format_odyssey_output(tmp_path):
    """format_odyssey produces a non-empty string with key markers."""
    state = OdysseyState.load(tmp_path / "rotate.json")
    _, to_lang, story, waypoints, leg = state.advance()
    output = format_odyssey("C/C++", to_lang, story, waypoints, leg)

    assert "POLYGLOT ODYSSEY" in output
    assert "Leg #001" in output
    assert "From:" in output
    assert "Destination:" in output
    assert "Scenic Waypoints" in output
    assert len(output) > 200


def test_peek_does_not_advance(tmp_path):
    """Peeking (via OdysseyState directly) doesn't change state."""
    state = OdysseyState.load(tmp_path / "rotate.json")
    rotation = state.languages

    # Manually peek: get next 3 without advancing
    pos = rotation.index(state.last_language)
    peeked = [rotation[(pos + i) % len(rotation)] for i in range(1, 4)]

    assert peeked == ["Rust", "Go", "Swift"]
    assert state.last_language == "C/C++"  # unchanged


def test_language_rotation_json_is_updated(tmp_path):
    """After save, the JSON file on disk matches the state."""
    state = OdysseyState.load(tmp_path / "rotate.json")
    state.advance()
    path = tmp_path / "rotate.json"
    state.save(path)

    with open(path) as f:
        data = json.load(f)

    assert data["last_language"] == "Rust"
    assert data["current_index"] == 1
    assert data["total_legs"] == 1
    assert len(data["journey_log"]) == 1


def test_updated_at_is_iso_timestamp(tmp_path):
    """updated_at is a valid ISO 8601 timestamp."""
    from datetime import datetime, timezone

    state = OdysseyState.load(tmp_path / "rotate.json")
    state.advance()
    # Not testing exact value — just that it's parseable
    dt = datetime.fromisoformat(state.updated_at)
    assert dt.tzinfo is not None


def test_no_consecutive_repeat_languages(tmp_path):
    """No leg should have from_lang == to_lang."""
    state = OdysseyState.load(tmp_path / "rotate.json")
    for i in range(16):  # 2 full cycles
        _, to_lang, _, _, _ = state.advance()
        assert state.journey_log[-1].from_lang != to_lang
        if i > 0:
            assert state.journey_log[-1].from_lang == state.journey_log[-2].to_lang


def test_total_legs_accurate_across_cycles(tmp_path):
    """total_legs counter never resets across cycles."""
    state = OdysseyState.load(tmp_path / "rotate.json")
    for _ in range(20):
        state.advance()
    assert state.total_legs == 20
    # And every log entry has a unique sequential leg number
    legs = [e.leg for e in state.journey_log]
    assert legs == list(range(1, 21))
