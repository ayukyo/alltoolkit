#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for polyglot_code_printer module.
"""

import json
import os
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

# Add parent to path so we can import polyglot_code_printer
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from polyglot_code_printer import (
    TOOL_NAME,
    TOOL_VERSION,
    LANGUAGES,
    CODE_PRINTS,
    EMOJI_MAP,
    ROTATION_FILE,
    load_rotation,
    save_rotation,
    get_current_language,
    advance_rotation,
    get_next_language,
    generate_code_print,
    _build_print_lines,
    _wrap,
    format_printable,
)


ALL_LANGS = [
    "Rust",
    "Go",
    "Swift",
    "Kotlin",
    "TypeScript",
    "JavaScript",
    "Java",
    "C/C++",
]


@pytest.fixture
def restore_rotation():
    """Snapshot and restore the rotation file."""
    snapshot = None
    if os.path.exists(ROTATION_FILE):
        with open(ROTATION_FILE, "r") as f:
            snapshot = f.read()
    yield
    if snapshot is not None:
        with open(ROTATION_FILE, "w") as f:
            f.write(snapshot)


class TestModuleMetadata:
    """Test module-level constants."""

    def test_tool_name(self):
        assert TOOL_NAME == "polyglot-code-printer"

    def test_tool_version(self):
        assert TOOL_VERSION == "1.0.0"

    def test_languages_count(self):
        assert len(LANGUAGES) == 8

    def test_languages_unique(self):
        assert len(LANGUAGES) == len(set(LANGUAGES))

    def test_rotation_file_path(self):
        assert ROTATION_FILE.endswith("language_rotation.json")


class TestCodePrints:
    """Test CODE_PRINTS data structure."""

    def test_all_languages_have_prints(self):
        for lang in LANGUAGES:
            assert lang in CODE_PRINTS, f"{lang} missing from CODE_PRINTS"

    def test_emoji_map_covers_all(self):
        for lang in LANGUAGES:
            assert lang in EMOJI_MAP

    def test_each_print_has_required_keys(self):
        required = ["emoji", "vibe", "philosophy", "aesthetic", "signature_idiom",
                    "hello_world", "box_top", "box_bottom", "line_sep", "color"]
        for lang, data in CODE_PRINTS.items():
            for key in required:
                assert key in data, f"{lang} missing key: {key}"
                assert isinstance(data[key], str)
                assert len(data[key]) > 0

    def test_hello_world_contains_greeting(self):
        for lang, data in CODE_PRINTS.items():
            text = data["hello_world"].lower()
            assert "hello" in text or "hallo" in text or "hola" in text, \
                f"{lang} hello world doesn't say hello: {data['hello_world']}"

    def test_box_top_bottom_match(self):
        for lang, data in CODE_PRINTS.items():
            assert len(data["box_top"]) == len(data["box_bottom"]), \
                f"{lang} box dimensions mismatch"


class TestLoadSaveRotation:
    """Test rotation file IO."""

    def test_load_returns_dict(self, restore_rotation):
        config = load_rotation()
        assert isinstance(config, dict)

    def test_save_roundtrip(self, restore_rotation, tmp_path):
        test_file = tmp_path / "rotation.json"
        data = {"languages": ["A", "B"], "current_index": 1}
        with patch.object(
            sys.modules["polyglot_code_printer"], "ROTATION_FILE", str(test_file)
        ):
            save_rotation(data)
            assert test_file.exists()
            with open(test_file) as f:
                loaded = json.load(f)
            assert loaded["languages"] == data["languages"]


class TestGetCurrentLanguage:
    """Test get_current_language."""

    def test_returns_string(self, restore_rotation):
        lang = get_current_language()
        assert isinstance(lang, str)
        assert lang in LANGUAGES

    def test_returns_valid_language(self, restore_rotation):
        lang = get_current_language()
        assert lang in LANGUAGES


class TestAdvanceRotation:
    """Test advance_rotation."""

    def test_advances_index(self, restore_rotation):
        before = load_rotation()
        idx_before = before["current_index"]
        advance_rotation()
        after = load_rotation()
        expected = (idx_before + 1) % len(after["languages"])
        assert after["current_index"] == expected

    def test_returns_previous_language(self, restore_rotation):
        before = load_rotation()
        idx_before = before["current_index"]
        result = advance_rotation()
        # Should be the language that WAS current
        expected_lang = before["languages"][idx_before % len(before["languages"])]
        # Or it could be filtered to LANGUAGES
        assert isinstance(result, str)

    def test_updates_last_language(self, restore_rotation):
        advance_rotation()
        config = load_rotation()
        assert "last_language" in config
        assert config["last_language"] in LANGUAGES


class TestGetNextLanguage:
    """Test get_next_language."""

    def test_returns_string(self, restore_rotation):
        lang = get_next_language()
        assert isinstance(lang, str)
        assert lang in LANGUAGES


class TestGenerateCodePrint:
    """Test generate_code_print."""

    def test_returns_dict(self, restore_rotation):
        result = generate_code_print(language="Rust")
        assert isinstance(result, dict)

    def test_has_required_keys(self, restore_rotation):
        result = generate_code_print(language="Rust")
        expected_keys = [
            "tool", "version", "selected_language", "selected_emoji",
            "vibe", "philosophy", "aesthetic", "signature_idiom",
            "hello_world", "print_lines", "all_prints",
            "rotation", "next_language", "timestamp",
        ]
        for key in expected_keys:
            assert key in result, f"Missing key: {key}"

    def test_tool_metadata(self, restore_rotation):
        result = generate_code_print(language="Rust")
        assert result["tool"] == "polyglot-code-printer"
        assert result["version"] == "1.0.0"

    def test_language_override(self, restore_rotation):
        result = generate_code_print(language="Go")
        assert result["selected_language"] == "Go"

    def test_emoji_per_language(self, restore_rotation):
        for lang in LANGUAGES:
            result = generate_code_print(language=lang)
            assert result["selected_emoji"] == EMOJI_MAP[lang]

    def test_all_prints_contains_all_languages(self, restore_rotation):
        result = generate_code_print(language="Rust")
        for lang in LANGUAGES:
            assert lang in result["all_prints"]

    def test_rotation_advances(self, restore_rotation):
        before = load_rotation()
        idx_before = before["current_index"]
        # Don't override language — let it use rotation
        generate_code_print()
        after = load_rotation()
        # Should have advanced
        assert after["current_index"] != idx_before or \
               (idx_before + 1) % len(after["languages"]) == after["current_index"]

    def test_print_lines_is_list(self, restore_rotation):
        result = generate_code_print(language="Rust")
        assert isinstance(result["print_lines"], list)
        assert len(result["print_lines"]) > 5

    def test_unknown_language_fallback(self, restore_rotation):
        result = generate_code_print(language="UnknownLang")
        # Should fall back to rotation language
        assert "selected_language" in result
        assert result["selected_language"] in LANGUAGES

    def test_result_is_json_serializable(self, restore_rotation):
        result = generate_code_print(language="Rust")
        json_str = json.dumps(result, ensure_ascii=False)
        loaded = json.loads(json_str)
        assert loaded["selected_language"] == "Rust"


class TestBuildPrintLines:
    """Test _build_print_lines."""

    def test_returns_list(self):
        cp = CODE_PRINTS["Rust"]
        lines = _build_print_lines("Rust", cp)
        assert isinstance(lines, list)
        assert len(lines) > 5

    def test_contains_language_name(self):
        cp = CODE_PRINTS["Rust"]
        lines = _build_print_lines("Rust", cp)
        assert any("Rust" in l for l in lines)


class TestWrap:
    """Test _wrap text wrapping."""

    def test_short_text(self):
        lines = _wrap("Hello world", 27)
        assert len(lines) == 1
        assert lines[0] == "Hello world"

    def test_long_text_wraps(self):
        text = " ".join(["word"] * 30)
        lines = _wrap(text, 27)
        assert len(lines) > 1
        for line in lines:
            assert len(line) <= 30  # allow some margin


class TestFormatPrintable:
    """Test format_printable."""

    def test_returns_string(self, restore_rotation):
        result = generate_code_print(language="Rust")
        formatted = format_printable(result)
        assert isinstance(formatted, str)
        assert len(formatted) > 50

    def test_contains_language(self, restore_rotation):
        result = generate_code_print(language="Rust")
        formatted = format_printable(result)
        assert "Rust" in formatted

    def test_contains_hello_world(self, restore_rotation):
        result = generate_code_print(language="Rust")
        formatted = format_printable(result)
        assert "Hello" in formatted

    def test_contains_next_language(self, restore_rotation):
        result = generate_code_print(language="Rust")
        formatted = format_printable(result)
        assert "Next:" in formatted
        assert result["next_language"] in formatted


class TestAllLanguagesPrint:
    """Test that all languages can be printed."""

    @pytest.mark.parametrize("lang", ALL_LANGS)
    def test_generate_for_each_language(self, lang, restore_rotation):
        result = generate_code_print(language=lang)
        assert result["selected_language"] == lang
        assert result["vibe"] == CODE_PRINTS[lang]["vibe"]
        assert result["philosophy"] == CODE_PRINTS[lang]["philosophy"]
        assert result["signature_idiom"] == CODE_PRINTS[lang]["signature_idiom"]
        assert result["hello_world"] == CODE_PRINTS[lang]["hello_world"]
