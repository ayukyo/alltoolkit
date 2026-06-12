"""Tests for rotation integration with language_rotation.json."""

import json
import tempfile
import os
import sys
sys.path.insert(0, '/home/admin/.openclaw/workspace/AllToolkit')
from polyglot_forge.src.forge import advance_rotation, get_current_language, generate_forge_card

LANGS = ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"]


def make_temp_config(index: int = 0) -> str:
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump({
            "languages": LANGS,
            "current_index": index,
            "last_language": LANGS[index],
            "updated_at": "2026-06-12T00:00:00+08:00",
        }, f)
        return f.name


def test_advance_rotation_basic(tmp_path=None):
    path = make_temp_config(0) if tmp_path is None else tmp_path
    if tmp_path:
        path = str(tmp_path / "rotation.json")
        with open(path, "w") as f:
            json.dump({"languages": LANGS, "current_index": 0, "last_language": "Rust"}, f)

    # Work on a temp copy so we don't mutate the real file
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump({"languages": LANGS, "current_index": 2, "last_language": "Swift"}, f)
        path = f.name

    result = advance_rotation(path)
    assert result["current_index"] == 3
    assert result["last_language"] == "Kotlin"
    os.unlink(path)


def test_advance_rotation_wraps_around():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump({"languages": LANGS, "current_index": 7, "last_language": "C/C++"}, f)
        path = f.name
    try:
        result = advance_rotation(path)
        assert result["current_index"] == 0
        assert result["last_language"] == "Rust"
    finally:
        os.unlink(path)


def test_get_current_language():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump({"languages": LANGS, "current_index": 4, "last_language": "TypeScript"}, f)
        path = f.name
    try:
        lang = get_current_language(path)
        assert lang == "TypeScript"
    finally:
        os.unlink(path)


def test_generate_forge_card_updates_config():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump({"languages": LANGS, "current_index": 0, "last_language": "Rust"}, f)
        path = f.name
    try:
        result = generate_forge_card(path, seed=42)
        # After advance_rotation(0→1), current_language is Go
        assert result["current_language"] == "Go"
        assert result["pairing_language"] in [l for l in LANGS if l != "Go"]
        # Verify config was updated
        with open(path) as f:
            data = json.load(f)
        assert data["current_index"] == 1
        assert data["last_language"] == "Go"
    finally:
        os.unlink(path)


def test_generate_forge_card_pairing_never_equals_primary():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump({"languages": LANGS, "current_index": 5, "last_language": "JavaScript"}, f)
        path = f.name
    try:
        for seed in range(10):
            result = generate_forge_card(path, seed=seed)
            assert result["pairing_language"] != result["current_language"]
            # advance again to get fresh state
            with open(path, "w") as f:
                json.dump({"languages": LANGS, "current_index": 5, "last_language": "JavaScript"}, f)
    finally:
        os.unlink(path)
