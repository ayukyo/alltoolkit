"""Tests for selector.py — rotation logic."""

import json
import tempfile
import os
import sys
sys.path.insert(0, '/home/admin/.openclaw/workspace')
from polyglot_selector.src.selector import select_next_language


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


def test_rotation_basic():
    """Starting at index 7 (C/C++), next should be index 0 (Rust)."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        path = f.name
    try:
        _write_config(path, 7)
        result = select_next_language(path, seed=0)
        assert result["previous_language"] == "C/C++"
        assert result["current_language"] == "Rust"
        assert result["current_index"] == 0
    finally:
        os.unlink(path)


def test_rotation_middle():
    """Starting at index 3 (Kotlin), next should be index 4 (TypeScript)."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        path = f.name
    try:
        _write_config(path, 3)
        result = select_next_language(path, seed=0)
        assert result["current_language"] == "TypeScript"
        assert result["current_index"] == 4
    finally:
        os.unlink(path)


def test_rotation_wraps_around():
    """Cycle through all 8 languages starting from index 0."""
    path = "/tmp/test_rotation_wrap.json"
    try:
        for i in range(len(LANGS)):
            _write_config(path, i)
            result = select_next_language(path, seed=0)
            expected_next = (i + 1) % len(LANGS)
            assert result["current_index"] == expected_next, \
                f"At index {i}, expected {expected_next}, got {result['current_index']}"
    finally:
        os.unlink(path)


def test_config_updated_after_rotation():
    """Verify language_rotation.json is actually updated on disk."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        path = f.name
    try:
        _write_config(path, 5)
        result = select_next_language(path, seed=0)
        assert result["current_index"] == 6

        # Reload from disk
        with open(path) as f:
            saved = json.load(f)
        assert saved["current_index"] == 6
        assert saved["last_language"] == "Java"
    finally:
        os.unlink(path)


def test_challenge_included_in_result():
    """Result must contain a Challenge namedtuple."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        path = f.name
    try:
        _write_config(path, 0)
        result = select_next_language(path, seed=42)
        assert "challenge" in result
        assert result["challenge"].language == "Go"
    finally:
        os.unlink(path)


def test_no_hardcoded_languages():
    """The selector must read languages from config, not from code."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        path = f.name
    try:
        custom_langs = ["Python", "Ruby", "Haskell"]
        with open(path, "w") as f:
            json.dump({
                "languages": custom_langs,
                "current_index": 0,
                "last_language": "Python",
                "updated_at": "2026-06-12T00:00:00+00:00"
            }, f, indent=2)
            f.write("\n")
        result = select_next_language(path, seed=0)
        assert result["current_language"] == "Ruby"
        assert result["current_index"] == 1
        assert result["challenge"] is None  # Ruby not in LANGUAGE_FEATURES
    finally:
        os.unlink(path)