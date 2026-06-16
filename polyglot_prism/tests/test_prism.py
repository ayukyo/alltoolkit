"""Tests for polyglot_prism — Spectral Analysis of Programming Languages."""

import json
import os
import sys
import tempfile
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from prism import (
    SPECTRAL_DB,
    ROTATION_ORDER,
    TOOL_NAME,
    TOOL_VERSION,
    generate_spectral_report,
    get_spectral_data,
    get_current_language,
    format_spectral_report,
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
        report = generate_spectral_report(rotate=True, config_path=path)
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
        report = generate_spectral_report(rotate=False, config_path=path)
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
        report = generate_spectral_report(rotate=True, config_path=path)
        assert report["new_index"] == 0
        assert report["language"] == "C/C++"

        with open(path) as f:
            saved = json.load(f)
        assert saved["current_index"] == 0
    finally:
        os.unlink(path)


def test_rotation_full_cycle():
    path = "/tmp/test_prism_cycle.json"
    try:
        for i in range(len(LANGS)):
            _write_config(path, i)
            report = generate_spectral_report(rotate=True, config_path=path)
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
# Spectral database tests
# ---------------------------------------------------------------------------

def test_all_languages_have_spectral_entries():
    for lang in LANGS:
        assert lang in SPECTRAL_DB, "%s missing from SPECTRAL_DB" % lang
        entry = SPECTRAL_DB[lang]
        assert "spectral_theme" in entry
        assert "prism_description" in entry
        assert "wavelengths" in entry
        assert "spectral_peaks" in entry
        assert "spectral_troughs" in entry
        assert "spectral_color" in entry
        assert "waveform" in entry
        assert "spectral_class" in entry


def test_all_languages_have_all_six_wavelengths():
    for lang in LANGS:
        entry = SPECTRAL_DB[lang]
        wavelengths = entry["wavelengths"]
        expected_keys = {
            "performance", "type_safety", "concurrency_model",
            "memory_model", "abstraction_level", "ecosystem_maturity"
        }
        actual_keys = set(wavelengths.keys())
        assert actual_keys == expected_keys, \
            "%s wavelengths mismatch: got %s, expected %s" % (lang, actual_keys, expected_keys)


def test_all_wavelength_scores_in_range():
    for lang in LANGS:
        entry = SPECTRAL_DB[lang]
        for key, val in entry["wavelengths"].items():
            score = val["score"]
            assert 0 <= score <= 100, \
                "%s.%s score %d out of range [0,100]" % (lang, key, score)


def test_spectral_data_returns_correct_entry():
    for lang in LANGS:
        data = get_spectral_data(lang)
        assert data is not None
        assert data["spectral_theme"] != "Unknown Theme"


def test_get_spectral_data_unknown_returns_none():
    data = get_spectral_data("NonExistentLanguage")
    assert data is None


# ---------------------------------------------------------------------------
# Report generation tests
# ---------------------------------------------------------------------------

def test_generate_spectral_report_all_languages():
    for lang in LANGS:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            path = f.name
        try:
            idx = LANGS.index(lang)
            _write_config(path, idx)
            report = generate_spectral_report(rotate=False, config_path=path)
            assert report["tool"] == TOOL_NAME
            assert report["version"] == TOOL_VERSION
            assert report["language"] == lang
            assert report["current_index"] >= 0
            assert report["rotated"] is False
            assert report["new_index"] is None
            assert report["spectral_theme"] != ""
            assert report["prism_description"] != ""
            assert len(report["wavelengths"]) == 6
            assert len(report["spectral_peaks"]) > 0
            assert len(report["spectral_troughs"]) > 0
            assert report["spectral_color"] != ""
            assert report["waveform"] != ""
            assert report["spectral_class"] != ""
            assert report["rotation_order"] == ROTATION_ORDER
            assert report["timestamp"] != ""
        finally:
            os.unlink(path)


def test_generate_spectral_report_timestamp():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        path = f.name
    try:
        _write_config(path, 0)
        r1 = generate_spectral_report(rotate=False, config_path=path)
        assert r1["timestamp"] != ""
    finally:
        os.unlink(path)


def test_report_returns_correct_current_index():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        path = f.name
    try:
        _write_config(path, 6)  # Java
        report = generate_spectral_report(rotate=False, config_path=path)
        assert report["language"] == "Java"
        assert report["current_index"] == 6
    finally:
        os.unlink(path)


# ---------------------------------------------------------------------------
# Formatting tests
# ---------------------------------------------------------------------------

def test_format_spectral_report_returns_string():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        path = f.name
    try:
        _write_config(path, 0)  # Rust
        report = generate_spectral_report(rotate=False, config_path=path)
        output = format_spectral_report(report)
        assert isinstance(output, str)
        assert "POLYGLOT PRISM" in output
        assert "Rust" in output
        assert "ROTATION ORDER" in output
    finally:
        os.unlink(path)


def test_format_spectral_report_contains_all_sections():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        path = f.name
    try:
        _write_config(path, 1)  # Go
        report = generate_spectral_report(rotate=False, config_path=path)
        output = format_spectral_report(report)
        assert "SPECTRAL DESCRIPTION" in output
        assert "WAVELENGTH INTENSITIES" in output
        assert "SPECTRAL PEAKS" in output
        assert "SPECTRAL TROUGHS" in output
        assert "WAVEFORM" in output
        assert "ROTATION ORDER" in output
    finally:
        os.unlink(path)


def test_format_spectral_report_has_border_lines():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        path = f.name
    try:
        _write_config(path, 2)  # Swift
        report = generate_spectral_report(rotate=False, config_path=path)
        output = format_spectral_report(report)
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
    assert TOOL_NAME == "polyglot-prism"


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
# C/C++ spectral entry verification
# ---------------------------------------------------------------------------

def test_cpp_spectral_entry():
    cpp = SPECTRAL_DB.get("C/C++", {})
    assert cpp["spectral_class"] == "O-Class Star (White-Blue Giant — Maximum Performance, Maximum Risk)"
    assert cpp["spectral_color"] == "⚪"
    # C/C++ should have max performance
    perf = cpp["wavelengths"]["performance"]["score"]
    assert perf == 100, "C/C++ performance should be 100, got %d" % perf


def test_rust_ownership_score_max():
    rust = SPECTRAL_DB.get("Rust", {})
    mem_score = rust["wavelengths"]["memory_model"]["score"]
    assert mem_score == 100, "Rust memory model should be 100, got %d" % mem_score


def test_javascript_ecosystem_max():
    js = SPECTRAL_DB.get("JavaScript", {})
    eco_score = js["wavelengths"]["ecosystem_maturity"]["score"]
    assert eco_score == 100, "JavaScript ecosystem should be 100, got %d" % eco_score