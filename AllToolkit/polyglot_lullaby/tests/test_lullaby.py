#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for polyglot_lullaby module.
"""

import json
import os
import sys
from pathlib import Path

import pytest

# Resolve the real workspace language_rotation.json (one level above AllToolkit)
POLYGLOT_ROOT = Path(__file__).parent.parent.parent.parent  # workspace
ROTATION_FILE = str(POLYGLOT_ROOT / "language_rotation.json")

# Patch ROTATION_FILE before importing
import polyglot_lullaby
polyglot_lullaby.ROTATION_FILE = ROTATION_FILE

from polyglot_lullaby import (
    TOOL_NAME,
    TOOL_VERSION,
    LANGUAGE_KEY,
    VERSE_LIBRARY,
    REFRAINS,
    BENEDICTIONS,
    compose_lullaby,
    detect_anxieties,
    load_rotation,
    save_rotation,
    pick_language,
    advance_rotation,
    run_tests,
)


ROTATION_ORDER = ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"]


@pytest.fixture
def rotation_snapshot():
    """Snapshot the real rotation file before each rotation-mutating test, restore after."""
    p = Path(ROTATION_FILE)
    original = p.read_text(encoding="utf-8") if p.exists() else None
    yield p
    if original is not None:
        p.write_text(original, encoding="utf-8")
    elif p.exists():
        p.unlink()


class TestModuleMetadata:
    def test_tool_name(self):
        assert TOOL_NAME == "polyglot-lullaby"

    def test_tool_version(self):
        assert TOOL_VERSION == "1.0.0"

    def test_verse_library_8_languages(self):
        assert set(VERSE_LIBRARY.keys()) == set(ROTATION_ORDER)
        for lang, verses in VERSE_LIBRARY.items():
            assert len(verses) >= 1, f"{lang} has no verses"
            for v in verses:
                assert isinstance(v, tuple) and len(v) == 2
                assert v[0] and v[1]

    def test_language_key_8_languages(self):
        assert set(LANGUAGE_KEY.keys()) == set(ROTATION_ORDER)
        for lang, meta in LANGUAGE_KEY.items():
            assert "key" in meta and "motif" in meta and "tempo" in meta


class TestDetectAnxieties:
    def test_empty_snippet_returns_at_least_one_verse(self):
        for lang in ROTATION_ORDER:
            out = detect_anxieties("", lang)
            assert len(out) >= 1

    def test_rust_async_keyword(self):
        verses = detect_anxieties("let handle = tokio::spawn(async move { ... });", "Rust")
        assert any("async" in v[0].lower() for v in verses)

    def test_go_channel_keyword(self):
        verses = detect_anxieties("ch := make(chan int); close(ch);", "Go")
        assert any("chan" in v[0].lower() for v in verses)

    def test_swift_force_unwrap(self):
        verses = detect_anxieties("let x = foo!.bar", "Swift")
        assert any("force" in v[0].lower() for v in verses)

    def test_javascript_async(self):
        verses = detect_anxieties("async function fetchData() { await fetch() }", "JavaScript")
        assert isinstance(verses, list)


class TestComposeLullaby:
    def test_compose_for_each_language(self):
        for lang in ROTATION_ORDER:
            out = compose_lullaby(lang)
            assert out["language"] == lang
            assert out["key"]
            assert out["motif"]
            assert out["tempo"]
            assert out["refrain"] in REFRAINS
            assert out["benediction"] in BENEDICTIONS
            assert out["stanzas"]
            assert "composed_at" in out
            assert "digest" in out
            assert len(out["digest"]) == 8

    def test_digest_is_deterministic(self):
        a = compose_lullaby("Rust", "let x = 1;")
        b = compose_lullaby("Rust", "let x = 1;")
        assert a["digest"] == b["digest"]
        assert a["stanzas"] == b["stanzas"]

    def test_different_languages_different_key(self):
        keys = {compose_lullaby(l)["key"] for l in ROTATION_ORDER}
        # at least 4 distinct keys among 8 languages
        assert len(keys) >= 4


class TestRotation:
    def test_load_rotation_has_8_languages(self):
        cfg = load_rotation()
        assert set(cfg["languages"]) == set(ROTATION_ORDER)
        assert 0 <= cfg["current_index"] < len(cfg["languages"])

    def test_pick_language_current(self):
        cfg = load_rotation()
        assert pick_language(cfg) == cfg["languages"][cfg["current_index"]]

    def test_pick_language_explicit(self):
        cfg = load_rotation()
        assert pick_language(cfg, explicit="Go") == "Go"

    def test_advance_rotation_wraps(self, rotation_snapshot):
        cfg = load_rotation()
        before = cfg["current_index"]
        advance_rotation(cfg)
        assert cfg["current_index"] == (before + 1) % len(cfg["languages"])
        assert "updated_at" in cfg

    def test_run_tests_clean(self):
        # run_tests() returns a list of failure strings; should be empty.
        result = run_tests()
        assert result == [], f"self-tests failed: {result}"
