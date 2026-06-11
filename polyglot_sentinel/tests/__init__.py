"""Tests for sentinel.py."""

import json
import tempfile
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from polyglot_sentinel.src.sentinel import (
    get_current_language,
    advance_rotation,
    generate_sentinel_report,
    LANGUAGE_PROFILES,
    ROTATION_ORDER,
    SentinelReport,
    Signal,
)

# Shared language list matching language_rotation.json
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


def test_get_current_language():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        path = f.name
    try:
        _write_config(path, 2)  # Swift
        lang = get_current_language(path)
        assert lang == "Swift", f"Expected Swift, got {lang}"
    finally:
        os.unlink(path)


def test_advance_rotation_wraps():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        path = f.name
    try:
        _write_config(path, 7)  # C/C++
        new_lang, new_idx = advance_rotation(path)
        assert new_lang == "Rust", f"Expected Rust after C/C++, got {new_lang}"
        assert new_idx == 0, f"Expected index 0, got {new_idx}"
    finally:
        os.unlink(path)


def test_advance_rotation_middle():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        path = f.name
    try:
        _write_config(path, 4)  # TypeScript
        new_lang, new_idx = advance_rotation(path)
        assert new_lang == "JavaScript", f"Expected JavaScript, got {new_lang}"
        assert new_idx == 5, f"Expected index 5, got {new_idx}"
    finally:
        os.unlink(path)


def test_advance_rotation_updates_config():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        path = f.name
    try:
        _write_config(path, 3)  # Kotlin
        advance_rotation(path)

        with open(path) as f:
            saved = json.load(f)
        assert saved["current_index"] == 4
        assert saved["last_language"] == "TypeScript"
        assert "updated_at" in saved
    finally:
        os.unlink(path)


def test_generate_sentinel_report_all_languages():
    for lang in LANGS:
        report = generate_sentinel_report(lang, seed=42)
        assert isinstance(report, SentinelReport)
        assert report.current_language == lang
        assert lang in LANGUAGE_PROFILES, f"{lang} not in LANGUAGE_PROFILES"
        assert 1 <= report.threat_level <= 5
        assert 0.0 <= report.stability_score <= 1.0
        assert 0.0 <= report.opportunity_index <= 1.0
        assert 0.0 <= report.signal_risk <= 1.0
        assert len(report.signals) > 0
        assert report.generated_at != ""


def test_generate_sentinel_report_deterministic():
    r1 = generate_sentinel_report("Rust", seed=99)
    r2 = generate_sentinel_report("Rust", seed=99)
    assert r1.current_language == r2.current_language
    assert r1.threat_category == r2.threat_category
    assert r1.stability_score == r2.stability_score


def test_signal_types():
    for lang in LANGS:
        report = generate_sentinel_report(lang, seed=0)
        for sig in report.signals:
            assert isinstance(sig, Signal)
            assert sig.type in ("Low moon", "Convergence front", "Echo", "Aurora", "Static", "Stable")
            assert sig.severity in ("low", "medium", "high")
            assert sig.description != ""


def test_threat_categories():
    for lang in LANGS:
        report = generate_sentinel_report(lang)
        assert report.threat_category in ("EXTINCTION", "VULNERABLE", "STABLE", "RISING", "DOMINANT")


def test_rotation_reads_from_config_not_hardcoded():
    """Verify the sentinel reads language list from config, not from code."""
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
        # Sentinel should read from config, not ROTATION_ORDER
        # But get_current_language uses ROTATION_ORDER hardcoded...
        # So it will read from config path which has Python at index 0
        # The sentinel reads from the actual file, which has Python
        lang = get_current_language(path)
        assert lang == "Python"
    finally:
        os.unlink(path)