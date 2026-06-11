"""Tests for config.py."""

import json
import tempfile
import os
import sys
sys.path.insert(0, '/home/admin/.openclaw/workspace')
from polyglot_selector.src.config import load_config, save_config


def test_load_config():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump({"languages": ["A", "B"], "current_index": 1}, f)
        path = f.name
    try:
        data = load_config(path)
        assert data["languages"] == ["A", "B"]
        assert data["current_index"] == 1
    finally:
        os.unlink(path)


def test_save_config_roundtrip():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        path = f.name
    try:
        original = {"languages": ["X"], "current_index": 0, "last_language": "X"}
        save_config(path, original)
        loaded = load_config(path)
        assert loaded == original
    finally:
        os.unlink(path)


def test_save_config_pretty_format():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        path = f.name
    try:
        save_config(path, {"languages": ["A"], "current_index": 0})
        with open(path) as f:
            content = f.read()
        assert "\n" in content  # pretty-printed with newlines
        assert "  " in content  # indented
    finally:
        os.unlink(path)