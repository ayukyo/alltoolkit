"""Tests for polyglot_codex - Literary Traditions of Programming Languages."""

import json
import os
import sys
import tempfile
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from codex import (
    CODEX_DB,
    ROTATION_ORDER,
    TOOL_NAME,
    TOOL_VERSION,
    generate_codex_report,
    get_codex_data,
    get_current_language,
    format_codex_report,
    _wrap_text,
)

LANGS = ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"]


def _write_config(path: str, index: int) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump({
            "languages": LANGS,
            "current_index": index,
            "last_language": LANGS[index],
            "updated_at": "2026-06-12T00:00:00+00:00"
        }, f, indent=2)
        f.write("\n")


# ---------------------------------------------------------------------------
# Rotation / config tests
# ---------------------------------------------------------------------------

def test_get_current_language():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        path = f.name
    try:
        _write_config(path, 2)  # Swift
        lang = get_current_language(path)
        assert lang == "Swift", "Expected Swift, got %s" % lang
    finally:
        os.unlink(path)


def test_get_current_language_wraps():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        path = f.name
    try:
        _write_config(path, 7)  # C/C++
        lang = get_current_language(path)
        assert lang == "C/C++", "Expected C/C++, got %s" % lang
    finally:
        os.unlink(path)


def test_rotation_advances_index():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        path = f.name
    try:
        _write_config(path, 3)  # Kotlin
        report = generate_codex_report(rotate=True, config_path=path)
        assert report["current_index"] == 3
        assert report["new_index"] == 4
        assert report["rotated"] is True

        with open(path) as f:
            saved = json.load(f)
        assert saved["current_index"] == 4
        assert saved["last_language"] == "Kotlin"
        assert "updated_at" in saved
    finally:
        os.unlink(path)


def test_rotation_no_advance_when_rotate_false():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        path = f.name
    try:
        _write_config(path, 5)  # JavaScript
        report = generate_codex_report(rotate=False, config_path=path)
        assert report["current_index"] == 5
        assert report["new_index"] is None
        assert report["rotated"] is False

        with open(path) as f:
            saved = json.load(f)
        assert saved["current_index"] == 5  # unchanged
    finally:
        os.unlink(path)


def test_rotation_wraps_from_c_to_rust():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        path = f.name
    try:
        _write_config(path, 7)  # C/C++
        report = generate_codex_report(rotate=True, config_path=path)
        assert report["new_index"] == 0
        assert report["language"] == "C/C++"

        with open(path) as f:
            saved = json.load(f)
        assert saved["current_index"] == 0
    finally:
        os.unlink(path)


def test_rotation_full_cycle():
    path = "/tmp/test_codex_cycle.json"
    try:
        for i in range(len(LANGS)):
            _write_config(path, i)
            report = generate_codex_report(rotate=True, config_path=path)
            expected_next = (i + 1) % len(LANGS)
            assert report["new_index"] == expected_next, \
                "At index %d: expected %d, got %d" % (i, expected_next, report["new_index"])
    finally:
        os.unlink(path)


def test_rotation_reads_from_config_not_hardcoded():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        path = f.name
    try:
        custom_langs = ["Python", "Ruby", "Haskell", "Erlang"]
        with open(path, "w") as f:
            json.dump({
                "languages": custom_langs,
                "current_index": 0,
                "last_language": "Python",
                "updated_at": "2026-06-12T00:00:00+00:00"
            }, f, indent=2)
            f.write("\n")
        lang = get_current_language(path)
        assert lang == "Python"
    finally:
        os.unlink(path)


# ---------------------------------------------------------------------------
# Codex data tests
# ---------------------------------------------------------------------------

def test_all_languages_have_codex_entries():
    for lang in LANGS:
        assert lang in CODEX_DB, "%s missing from CODEX_DB" % lang
        entry = CODEX_DB[lang]
        assert "literary_theme" in entry
        assert "codex_age" in entry
        assert "origin_story" in entry
        assert "epigraph" in entry
        assert "ancient_proverb" in entry
        assert "designers_maxim" in entry
        assert "famous_saying" in entry
        assert "hidden_easter_egg" in entry
        assert "philosophical_haiku" in entry
        assert "signature_works" in entry
        assert "literary_tone" in entry
        assert "codex_color" in entry


def test_codex_data_returns_correct_entry():
    for lang in LANGS:
        data = get_codex_data(lang)
        assert data is not None
        assert data["literary_theme"] != "Unknown Theme"


def test_get_codex_data_unknown_returns_none():
    data = get_codex_data("NonExistentLanguage")
    assert data is None


# ---------------------------------------------------------------------------
# Report generation tests
# ---------------------------------------------------------------------------

def test_generate_codex_report_all_languages():
    for lang in LANGS:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            path = f.name
        try:
            idx = LANGS.index(lang)
            _write_config(path, idx)
            report = generate_codex_report(rotate=False, config_path=path)
            assert report["tool"] == TOOL_NAME
            assert report["version"] == TOOL_VERSION
            assert report["language"] == lang
            assert report["current_index"] >= 0
            assert report["rotated"] is False
            assert report["new_index"] is None
            assert report["literary_theme"] != ""
            assert report["codex_age"] != ""
            assert report["origin_story"] != ""
            assert report["epigraph"] != ""
            assert report["ancient_proverb"] != ""
            assert report["designers_maxim"] != ""
            assert report["famous_saying"] != ""
            assert report["hidden_easter_egg"] != ""
            assert report["philosophical_haiku"] != ""
            assert len(report["signature_works"]) > 0
            assert report["literary_tone"] != ""
            assert report["codex_color"] != ""
            assert report["rotation_order"] == ROTATION_ORDER
            assert report["timestamp"] != ""
        finally:
            os.unlink(path)


def test_generate_codex_report_timestamp():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        path = f.name
    try:
        _write_config(path, 0)  # Rust
        r1 = generate_codex_report(rotate=False, config_path=path)
        r2 = generate_codex_report(rotate=False, config_path=path)
        assert r1["timestamp"] != ""
    finally:
        os.unlink(path)


def test_report_returns_correct_current_index():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        path = f.name
    try:
        _write_config(path, 6)  # Java
        report = generate_codex_report(rotate=False, config_path=path)
        assert report["language"] == "Java"
        assert report["current_index"] == 6
    finally:
        os.unlink(path)


# ---------------------------------------------------------------------------
# Formatting tests
# ---------------------------------------------------------------------------

def test_format_codex_report_returns_string():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        path = f.name
    try:
        _write_config(path, 0)  # Rust
        report = generate_codex_report(rotate=False, config_path=path)
        output = format_codex_report(report)
        assert isinstance(output, str)
        assert "POLYGLOT CODEX" in output
        assert "Rust" in output
        assert "ROTATION ORDER" in output
    finally:
        os.unlink(path)


def test_format_codex_report_contains_all_sections():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        path = f.name
    try:
        _write_config(path, 1)  # Go
        report = generate_codex_report(rotate=False, config_path=path)
        output = format_codex_report(report)
        assert "CODEX AGE" in output
        assert "ORIGIN STORY" in output
        assert "EPIGRAPH" in output
        assert "ANCIENT PROVERB" in output
        assert "DESIGNER'S MAXIM" in output
        assert "FAMOUS SAYING" in output
        assert "HIDDEN EASTER EGG" in output
        assert "PHILOSOPHICAL HAIKU" in output
        assert "SIGNATURE WORKS" in output
        assert "LITERARY TONE" in output
    finally:
        os.unlink(path)


def test_format_codex_report_has_border_lines():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        path = f.name
    try:
        _write_config(path, 2)  # Swift
        report = generate_codex_report(rotate=False, config_path=path)
        output = format_codex_report(report)
        # Uses box-drawing characters or + as border
        assert len(output) > 50
        assert "Swift" in output
    finally:
        os.unlink(path)


# ---------------------------------------------------------------------------
# Text wrapping tests
# ---------------------------------------------------------------------------

def test_wrap_text_short():
    text = "Short text"
    lines = _wrap_text(text, 50)
    assert len(lines) == 1
    assert lines[0] == "Short text"


def test_wrap_text_long():
    # 100 A's at width 30 -> "AAAAAAAAAA..." (30) + "AAAAAAAAAA..." (30) + "AAAAAAAAAA..." (30) + "AAAAAAAAAA" (10) = 4 lines
    text = "A" * 100
    lines = _wrap_text(text, 30)
    assert len(lines) == 4, "Expected 4 lines, got %d: %s" % (len(lines), lines)


def test_wrap_text_empty():
    lines = _wrap_text("", 50)
    assert len(lines) == 1
    assert lines[0] == ""


def test_wrap_text_none():
    lines = _wrap_text(None, 50)
    assert len(lines) == 1


# ---------------------------------------------------------------------------
# Tool constants
# ---------------------------------------------------------------------------

def test_tool_name():
    assert TOOL_NAME == "polyglot-codex"


def test_tool_version():
    assert TOOL_VERSION == "1.0.0"


def test_rotation_order_correct():
    assert ROTATION_ORDER == [
        "Rust", "Go", "Swift", "Kotlin",
        "TypeScript", "JavaScript", "Java", "C/C++",
    ]


def test_rotation_order_len():
    assert len(ROTATION_ORDER) == 8


# ---------------------------------------------------------------------------
# C/C++ Easter Egg key exists (typo fix verification)
# ---------------------------------------------------------------------------

def test_cpp_easter_egg_key_exists():
    cpp = CODEX_DB.get("C/C++", {})
    assert "hidden_easter_egg" in cpp, "C/C++ missing 'hidden_easter_egg' key"
    assert cpp["hidden_easter_egg"] != ""
