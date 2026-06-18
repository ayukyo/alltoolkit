"""Tests for fugue.py — musical syntax fugue."""

import json
import tempfile
import os
import sys
sys.path.insert(0, '/home/admin/.openclaw/workspace')
from polyglot_fugue.src.fugue import (
    fugue, format_fugue, run_tests, advance_rotation,
    load_rotation, save_rotation,
    FUGUE_THEMES, ROTATION_ORDER, TOOL_NAME, TOOL_VERSION,
    _note_to_midi, render_fugue_score,
)


LANGS = ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"]


def _write_config(path: str, index: int) -> None:
    with open(path, "w") as f:
        json.dump({
            "languages": LANGS,
            "current_index": index,
            "last_language": LANGS[index],
            "updated_at": "2026-06-12T00:00:00+00:00"
        }, f, indent=2)
        f.write("\n")


def test_note_to_midi():
    assert _note_to_midi("C4") == 60
    assert _note_to_midi("A4") == 69
    assert _note_to_midi("rest") == 0
    assert _note_to_midi("G5") == 79


def test_rotation_order():
    assert ROTATION_ORDER == ["Rust", "Go", "Swift", "Kotlin",
                              "TypeScript", "JavaScript", "Java", "C/C++"]


def test_fugue_themes_count():
    assert len(FUGUE_THEMES) == 8


def test_fugue_themes_have_4_voices():
    for theme in FUGUE_THEMES:
        assert len(theme["voices"]) == 4
        assert set(theme["voices"].keys()) == {"Rust", "Go", "Swift", "Kotlin"}


def test_voice_melody_length():
    for theme in FUGUE_THEMES:
        for voice in theme["voices"].values():
            assert len(voice["melody"]) == 8


def test_render_fugue_score():
    theme = FUGUE_THEMES[0]
    score = render_fugue_score(theme["voices"])
    assert len(score) == 9
    assert all(isinstance(r, str) for r in score)


def test_fugue_returns_required_fields():
    result = fugue()
    assert "tool" in result
    assert "version" in result
    assert "language" in result
    assert "theme" in result
    assert "voices" in result
    assert "score_display" in result
    assert result["rotation_advanced"] is True
    assert "next_language" in result


def test_fugue_with_theme_id():
    result = fugue(theme_id="string_interpolation")
    assert result["theme"]["id"] == "string_interpolation"


def test_format_fugue():
    result = fugue()
    formatted = format_fugue(result)
    assert isinstance(formatted, str)
    assert formatted.startswith("╔")
    assert formatted.rstrip().endswith("╝")
    assert result["theme"]["name"] in formatted
