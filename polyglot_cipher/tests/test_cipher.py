#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for polyglot_cipher module.
"""

import json
import os
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

# Add parent to path so we can import polyglot_cipher
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from polyglot_cipher import (
    TOOL_NAME,
    TOOL_VERSION,
    ROTATION_ORDER,
    CIPHER_MAP,
    ROTATION_FILE,
    load_rotation,
    save_rotation,
    _rust_cipher,
    _go_cipher,
    _swift_cipher,
    _kotlin_cipher,
    _typescript_cipher,
    _javascript_cipher,
    _java_cipher,
    _cpp_cipher,
    _get_next_language,
    _wrap,
    _section,
    _cipher_card,
    _generate_challenge,
    cipher,
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
        assert TOOL_NAME == "polyglot-cipher"

    def test_tool_version(self):
        assert TOOL_VERSION == "1.0.0"

    def test_rotation_order_count(self):
        assert len(ROTATION_ORDER) == 8

    def test_cipher_map_covers_all_languages(self):
        for lang in ROTATION_ORDER:
            assert lang in CIPHER_MAP, f"{lang} missing from CIPHER_MAP"

    def test_rotation_file_path(self):
        assert ROTATION_FILE.endswith("language_rotation.json")


class TestRustCipher:
    """Test Rust ROT-XOR cipher."""

    def test_rust_key(self):
        _, key = _rust_cipher("hello")
        assert key == 42

    def test_rust_changes_text(self):
        encoded, _ = _rust_cipher("hello rust")
        assert encoded != "hello rust"

    def test_rust_preserves_length(self):
        text = "hello rust"
        encoded, _ = _rust_cipher(text)
        assert len(encoded) == len(text)

    def test_rust_preserves_non_alpha(self):
        encoded, _ = _rust_cipher("hello world!")
        assert "!" in encoded
        assert " " in encoded

    def test_rust_handles_empty(self):
        encoded, _ = _rust_cipher("")
        assert encoded == ""


class TestGoCipher:
    """Test Go sliding window cipher."""

    def test_go_key(self):
        _, key = _go_cipher("hello")
        assert key == 3

    def test_go_changes_text(self):
        encoded, _ = _go_cipher("hello go")
        assert encoded != "hello go"

    def test_go_preserves_length(self):
        text = "hello go"
        encoded, _ = _go_cipher(text)
        assert len(encoded) == len(text)


class TestSwiftCipher:
    """Test Swift Unicode scalar shift."""

    def test_swift_key(self):
        _, key = _swift_cipher("hello")
        assert key == 17

    def test_swift_changes_text(self):
        encoded, _ = _swift_cipher("hello swift")
        assert encoded != "hello swift"

    def test_swift_preserves_length(self):
        text = "hello swift"
        encoded, _ = _swift_cipher(text)
        assert len(encoded) == len(text)


class TestKotlinCipher:
    """Test Kotlin null-safe Caesar."""

    def test_kotlin_key(self):
        _, key = _kotlin_cipher("hello")
        assert key == 7

    def test_kotlin_maps_space_to_null(self):
        encoded, _ = _kotlin_cipher("a b c")
        assert "null" in encoded

    def test_kotlin_changes_alpha(self):
        encoded, _ = _kotlin_cipher("abc")
        assert encoded != "abc"

    def test_kotlin_preserves_length_distribution(self):
        # Spaces become "null" (4 chars), so length increases
        text = "a a"
        encoded, _ = _kotlin_cipher(text)
        assert "null" in encoded


class TestTypeScriptCipher:
    """Test TypeScript Atbash cipher."""

    def test_typescript_key(self):
        _, key = _typescript_cipher("hello")
        assert key == 0

    def test_typescript_atbash_abc(self):
        encoded, _ = _typescript_cipher("abc")
        assert encoded == "zyx"

    def test_typescript_atbash_xyz(self):
        encoded, _ = _typescript_cipher("xyz")
        assert encoded == "cba"

    def test_typescript_atbash_inverts_preserves(self):
        text = "The quick brown fox"
        encoded, _ = _typescript_cipher(text)
        # Atbash of Atbash should equal original
        encoded_twice, _ = _typescript_cipher(encoded)
        assert encoded_twice == text

    def test_typescript_preserves_case(self):
        encoded, _ = _typescript_cipher("ABC")
        assert encoded == "ZYX"


class TestJavaScriptCipher:
    """Test JavaScript Vigenère cipher."""

    def test_javascript_key(self):
        _, key = _javascript_cipher("hello")
        # Implementation returns 0 as the key (variable) but conceptually uses "JS"
        # See _javascript_cipher for the Vigenère with "JS" key
        assert key == 0

    def test_javascript_changes_text(self):
        encoded, _ = _javascript_cipher("hello")
        assert encoded != "hello"

    def test_javascript_preserves_length(self):
        text = "hello"
        encoded, _ = _javascript_cipher(text)
        assert len(encoded) == len(text)


class TestJavaCipher:
    """Test Java classloader reverse + ROT13."""

    def test_java_key(self):
        _, key = _java_cipher("hello")
        assert key == 13

    def test_java_changes_text(self):
        encoded, _ = _java_cipher("hello java")
        assert encoded != "hello java"

    def test_java_preserves_length(self):
        text = "hello"
        encoded, _ = _java_cipher(text)
        assert len(encoded) == len(text)


class TestCppCipher:
    """Test C/C++ pointer XOR cipher."""

    def test_cpp_key(self):
        _, key = _cpp_cipher("hello")
        assert key == 0x1F

    def test_cpp_changes_text(self):
        encoded, _ = _cpp_cipher("hello")
        assert encoded != "hello"

    def test_cpp_preserves_length(self):
        text = "hello"
        encoded, _ = _cpp_cipher(text)
        assert len(encoded) == len(text)

    def test_cpp_handles_empty(self):
        encoded, _ = _cpp_cipher("")
        assert encoded == ""


class TestLoadSaveRotation:
    """Test rotation file IO."""

    def test_load_returns_dict(self, restore_rotation):
        config = load_rotation()
        assert isinstance(config, dict)
        assert "languages" in config
        assert "current_index" in config

    def test_save_roundtrip(self, restore_rotation, tmp_path):
        test_file = tmp_path / "rotation.json"
        data = {"languages": ["A", "B"], "current_index": 1}
        with patch.object(
            sys.modules["polyglot_cipher"], "ROTATION_FILE", str(test_file)
        ):
            save_rotation(data)
            assert test_file.exists()
            with open(test_file) as f:
                loaded = json.load(f)
            assert loaded == data


class TestGetNextLanguage:
    """Test _get_next_language helper."""

    def test_returns_string(self, restore_rotation):
        lang = _get_next_language()
        assert isinstance(lang, str)
        assert lang in load_rotation()["languages"]


class TestWrap:
    """Test _wrap text wrapping."""

    def test_short_text_one_line(self):
        lines = _wrap("Short text", 78)
        assert len(lines) == 1
        assert lines[0] == "Short text"

    def test_long_text_wraps(self):
        long_text = " ".join(["word"] * 50)
        lines = _wrap(long_text, 40)
        assert len(lines) > 1
        # All lines should be roughly width or shorter
        for line in lines:
            assert len(line) <= 42  # allow 2 char margin

    def test_empty_text(self):
        lines = _wrap("", 78)
        # _wrap with empty text returns empty list
        assert lines == [] or lines == [""]

    def test_single_word(self):
        lines = _wrap("Hello", 78)
        assert lines == ["Hello"]


class TestSection:
    """Test _section helper."""

    def test_returns_string(self):
        result = _section("LABEL", "Some text content")
        assert isinstance(result, str)
        assert "LABEL" in result


class TestCipherCard:
    """Test _cipher_card generation."""

    def test_contains_language(self):
        card = _cipher_card("Rust", "abc", 42, "ROT13")
        assert "Rust" in card

    def test_contains_cipher_name(self):
        card = _cipher_card("Rust", "abc", 42, "Ownership ROT-XOR")
        assert "Ownership ROT-XOR" in card


class TestGenerateChallenge:
    """Test challenge phrase generation."""

    def test_returns_string(self):
        phrase = _generate_challenge()
        assert isinstance(phrase, str)
        assert len(phrase) > 0


class TestCipherFunction:
    """Test the main cipher() function."""

    def test_returns_dict(self, restore_rotation):
        result = cipher()
        assert isinstance(result, dict)

    def test_has_required_fields(self, restore_rotation):
        result = cipher()
        for key in ["language", "cipher_name", "challenge", "encoded", "key", "cipher_card", "rotated_at"]:
            assert key in result, f"Missing key: {key}"

    def test_language_in_cipher_map(self, restore_rotation):
        result = cipher()
        assert result["language"] in CIPHER_MAP

    def test_encoded_is_string(self, restore_rotation):
        result = cipher()
        assert isinstance(result["encoded"], str)

    def test_cipher_card_is_string(self, restore_rotation):
        result = cipher()
        assert isinstance(result["cipher_card"], str)
        assert len(result["cipher_card"]) > 10

    def test_rotation_advances(self, restore_rotation):
        before = load_rotation()
        idx_before = before["current_index"]
        cipher()
        after = load_rotation()
        expected = (idx_before + 1) % len(after["languages"])
        assert after["current_index"] == expected

    def test_last_language_updated(self, restore_rotation):
        cipher()
        config = load_rotation()
        assert "last_language" in config
        assert config["last_language"] in ALL_LANGS

    def test_result_is_json_serializable(self, restore_rotation):
        result = cipher()
        json_str = json.dumps(result, ensure_ascii=False)
        loaded = json.loads(json_str)
        assert loaded["language"] == result["language"]


class TestCiphersCoverage:
    """Test that all ciphers produce valid output."""

    @pytest.mark.parametrize("lang", ALL_LANGS)
    def test_cipher_handles_alphabetic_input(self, lang):
        cipher_func = CIPHER_MAP[lang]
        text = "hello world"
        encoded, key = cipher_func(text)
        assert isinstance(encoded, str)
        assert len(encoded) >= len(text) - 1  # Allow kotlin's "null" expansion
        # Key should be non-None
        assert key is not None

    @pytest.mark.parametrize("lang", ALL_LANGS)
    def test_cipher_handles_empty(self, lang):
        cipher_func = CIPHER_MAP[lang]
        encoded, _ = cipher_func("")
        assert isinstance(encoded, str)
        # Empty in, empty-ish out
        assert encoded == "" or encoded.replace("null", "") == ""
