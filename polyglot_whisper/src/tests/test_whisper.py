# empty"""Tests for polyglot_whisper."""

import json
import os
import sys
import tempfile
from pathlib import Path

import pytest

sys.path.insert(0, '/home/admin/.openclaw/workspace')

from polyglot_whisper.src.cards import get_card, get_all_languages
from polyglot_whisper.src.whisper import (
    load_rotation_config,
    save_rotation_config,
    rotate_and_whisper,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def temp_config(tmp_path):
    """A minimal language_rotation.json in a temp directory."""
    config_file = tmp_path / "language_rotation.json"
    data = {
        "languages": ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"],
        "current_index": 0,
        "last_language": "Rust",
        "updated_at": "2026-06-19T01:00:00+08:00",
    }
    with open(config_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    return str(config_file)


# ---------------------------------------------------------------------------
# cards.py tests
# ---------------------------------------------------------------------------

class TestGetCard:
    def test_returns_dict_with_all_fields(self):
        card = get_card("Rust")
        assert isinstance(card, dict)
        assert set(card.keys()) == {"idiom", "proverb", "quirk", "fun_fact", "syntax_gem", "philosophy"}

    def test_all_languages_have_cards(self):
        for lang in ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"]:
            card = get_card(lang)
            assert card is not None
            assert all(card[k] for k in card)  # no empty strings

    def test_unknown_language_raises(self):
        with pytest.raises(ValueError, match="No insight card"):
            get_card("Pascal")

    def test_card_content_is_non_trivial(self):
        """Each card should have meaningful content (longer than 10 chars)."""
        for lang in get_all_languages():
            card = get_card(lang)
            for key, value in card.items():
                assert len(value) > 10, f"{lang}/{key} is too short"


class TestGetAllLanguages:
    def test_returns_all_8_languages(self):
        langs = get_all_languages()
        assert len(langs) == 8
        assert "Rust" in langs
        assert "C/C++" in langs


# ---------------------------------------------------------------------------
# whisper.py config helpers
# ---------------------------------------------------------------------------

class TestLoadRotationConfig:
    def test_loads_valid_json(self, temp_config):
        data = load_rotation_config(temp_config)
        assert "languages" in data
        assert "current_index" in data
        assert isinstance(data["languages"], list)

    def test_loads_nonexistent_file_raises(self):
        with pytest.raises(FileNotFoundError):
            load_rotation_config("/nonexistent/path.json")


class TestSaveRotationConfig:
    def test_roundtrip(self, tmp_path):
        config_path = str(tmp_path / "roundtrip.json")
        original = {
            "languages": ["A", "B"],
            "current_index": 1,
            "last_language": "B",
            "updated_at": "2026-01-01T00:00:00+00:00",
        }
        save_rotation_config(config_path, original)
        loaded = load_rotation_config(config_path)
        assert loaded == original


# ---------------------------------------------------------------------------
# Core rotation logic
# ---------------------------------------------------------------------------

class TestRotateAndWhisper:
    def test_advances_index_correctly(self, temp_config):
        """After one call, index should go from 0 → 1."""
        result = rotate_and_whisper(config_path=temp_config)
        assert result["current_index"] == 1
        assert result["previous_language"] == "Rust"
        assert result["current_language"] == "Go"

    def test_wraps_around(self, tmp_path):
        """When at last index, next should wrap to 0."""
        config_file = tmp_path / "wrap.json"
        data = {
            "languages": ["Rust", "Go"],
            "current_index": 1,
            "last_language": "Go",
            "updated_at": "2026-06-19T00:00:00+08:00",
        }
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write("\n")

        result = rotate_and_whisper(config_path=str(config_file))
        assert result["current_index"] == 0
        assert result["current_language"] == "Rust"

    def test_config_file_is_updated(self, temp_config):
        before = load_rotation_config(temp_config)
        rotate_and_whisper(config_path=temp_config)
        after = load_rotation_config(temp_config)
        assert after["current_index"] == (before["current_index"] + 1) % len(before["languages"])
        assert after["last_language"] == after["languages"][after["current_index"]]

    def test_returns_insight_card(self, temp_config):
        result = rotate_and_whisper(config_path=temp_config)
        assert result["current_language"] == "Go"
        card = result["insight_card"]
        assert card is not None
        assert "idiom" in card
        assert "proverb" in card
        assert "fun_fact" in card

    def test_full_rotation_cycle(self, tmp_path):
        """Simulate a full 8-language rotation cycle and verify index returns to 0."""
        config_file = tmp_path / "cycle.json"
        data = {
            "languages": ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"],
            "current_index": 0,
            "last_language": "Rust",
            "updated_at": "2026-06-19T00:00:00+08:00",
        }
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write("\n")

        languages = data["languages"]
        for i in range(len(languages)):
            result = rotate_and_whisper(config_path=str(config_file))
            expected_index = (i + 1) % len(languages)
            assert result["current_index"] == expected_index, (
                f"Cycle step {i}: expected index {expected_index}, "
                f"got {result['current_index']}"
            )
            assert result["current_language"] == languages[expected_index]

    def test_previous_language_is_correct(self, temp_config):
        result = rotate_and_whisper(config_path=temp_config)
        assert result["previous_language"] == "Rust"

    def test_insight_card_fields_are_all_populated(self, temp_config):
        for _ in range(8):
            result = rotate_and_whisper(config_path=temp_config)
            card = result["insight_card"]
            if card is not None:
                for field in ["idiom", "proverb", "quirk", "fun_fact", "syntax_gem", "philosophy"]:
                    assert field in card
                    assert isinstance(card[field], str)
                    assert len(card[field]) > 10


# ---------------------------------------------------------------------------
# Integration: end-to-end with real language_rotation.json
# ---------------------------------------------------------------------------

REAL_CONFIG = str(Path(__file__).parent.parent.parent.parent / "language_rotation.json")


class TestRealConfigIntegration:
    def test_rotate_and_whisper_works_with_real_config(self):
        # Backup real config
        with open(REAL_CONFIG, "r") as f:
            original = f.read()

        try:
            result = rotate_and_whisper(config_path=REAL_CONFIG)
            assert result["previous_language"] in [
                "Rust", "Go", "Swift", "Kotlin",
                "TypeScript", "JavaScript", "Java", "C/C++",
            ]
            assert result["current_language"] in [
                "Rust", "Go", "Swift", "Kotlin",
                "TypeScript", "JavaScript", "Java", "C/C++",
            ]
            assert result["insight_card"] is not None
            assert isinstance(result["insight_card"], dict)
        finally:
            # Restore original config
            with open(REAL_CONFIG, "w") as f:
                f.write(original)