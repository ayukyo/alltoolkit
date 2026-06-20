#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pytest wrapper for polyglot_cathedral self-tests.

The module ships its own test runner via `python -m polyglot_cathedral --test`.
This file wraps it as a pytest-compatible test case for CI / discovery.
"""

import sys
import subprocess
from pathlib import Path

# Ensure parent (AllToolkit/) is on sys.path so `import polyglot_cathedral` works
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


def test_polyglot_cathedral_self_tests_pass():
    from polyglot_cathedral import run_tests
    failures = run_tests()
    assert not failures, f"polyglot_cathedral self-tests failed: {failures}"


def test_polyglot_cathedral_cli_help():
    """Smoke-test the CLI help path."""
    result = subprocess.run(
        [sys.executable, "-m", "polyglot_cathedral", "--help"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        universal_newlines=True,
        cwd=str(Path(__file__).parent.parent.parent),
    )
    assert result.returncode == 0
    assert "polyglot-cathedral" in result.stdout


def test_polyglot_cathedral_current_matches_rotation():
    """Current language helper must agree with the JSON file."""
    from polyglot_cathedral import get_current_language, load_rotation

    rot = load_rotation()
    langs = rot["languages"]
    expected = langs[rot["current_index"] % len(langs)]
    assert get_current_language() == expected


def test_polyglot_cathedral_report_for_each_language():
    """All eight rotation languages must produce a non-error report."""
    from polyglot_cathedral import cathedral_report, load_rotation

    rot = load_rotation()
    for lang in rot["languages"]:
        rep = cathedral_report(language=lang, snippet="", advance=False)
        assert "error" not in rep, f"error for {lang}: {rep}"
        assert rep["language"] == lang
        assert "cathedral" in rep
        assert "floor_plan" in rep
        assert "structure" in rep
        assert "bell_tower" in rep
        assert "ornament" in rep
        assert "gargoyles" in rep
        assert "architects" in rep
        assert "visitors" in rep
        assert "ascii_art" in rep


def test_polyglot_cathedral_compare_symmetry():
    """side_by_side_naves must be symmetric for unique elements."""
    from polyglot_cathedral import side_by_side_naves

    a = side_by_side_naves("Rust", "Go")
    b = side_by_side_naves("Go", "Rust")
    assert a["shared_transepts"] == b["shared_transepts"]
    assert a["unique_to_a"] == b["unique_to_b"]
    assert a["unique_to_b"] == b["unique_to_a"]


def test_polyglot_cathedral_snippet_homing_detects_rust():
    """A Rust-looking snippet must rank Rust at the top."""
    from polyglot_cathedral import cathedral_report

    snippet = (
        "fn main() {\n"
        "    let mut v: Vec<i32> = Vec::new();\n"
        "    let r: Result<i32, ()> = Ok(1);\n"
        "    println!(\"{:?}\", r.unwrap());\n"
        "}\n"
    )
    rep = cathedral_report(language="Rust", snippet=snippet, advance=False)
    matches = rep["snippet_homing"]["top_matches"]
    assert matches, "no matches found for Rust snippet"
    top_lang, top_score = matches[0]["language"], matches[0]["score"]
    assert top_lang == "Rust", f"expected Rust on top, got {top_lang}"
    assert top_score >= 2


def test_polyglot_cathedral_unknown_language_returns_error():
    """Asking for an unknown language must return a structured error."""
    from polyglot_cathedral import cathedral_report

    rep = cathedral_report(language="Elvish", advance=False)
    assert "error" in rep
    assert "Elvish" in rep["error"]