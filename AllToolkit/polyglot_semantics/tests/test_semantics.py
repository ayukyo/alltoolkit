"""
Tests for Polyglot Semantics
"""

import json
import os
import sys
from pathlib import Path

# Ensure the package is importable
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from polyglot_semantics.src.semantics import (
    ROTATION_ORDER,
    ROTATION_FILE,
    analyze_semantics,
    format_semantic_fingerprint,
    get_current_language,
    run_tests,
    SEMANTIC_PROFILES,
)


def test_rotation_file_exists():
    assert os.path.exists(ROTATION_FILE), f"Rotation file not found: {ROTATION_FILE}"


def test_rotation_order_correct():
    """Verify the rotation order matches the specified sequence."""
    expected = ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"]
    assert ROTATION_ORDER == expected, f"Rotation order mismatch: {ROTATION_ORDER}"


def test_current_language_from_rotation():
    """get_current_language returns a valid language."""
    lang_info = get_current_language()
    assert "current_language" in lang_info
    assert lang_info["current_language"] in ROTATION_ORDER
    assert "next_language" in lang_info
    assert lang_info["next_language"] in ROTATION_ORDER


def test_rotation_index_advances():
    """The index in rotation file advances after each call."""
    with open(ROTATION_FILE, "r") as f:
        before = json.load(f)
    before_idx = before["current_index"]

    lang_info = get_current_language()

    with open(ROTATION_FILE, "r") as f:
        after = json.load(f)
    after_idx = after["current_index"]

    expected_next = (before_idx + 1) % len(before["languages"])
    assert after_idx == expected_next, (
        f"Index did not advance correctly: before={before_idx}, after={after_idx}, expected={expected_next}"
    )


def test_all_languages_have_semantic_profiles():
    """Every language in the rotation has a full semantic profile."""
    for lang in ROTATION_ORDER:
        profile = analyze_semantics(lang)
        assert "paradigm" in profile
        assert "notable_divergence" in profile
        for key in ["existence", "action", "state", "relation", "identity", "control", "abstraction"]:
            assert key in profile, f"Language {lang} missing key: {key}"
            assert "keyword" in profile[key]
            assert "semantic_difference" in profile[key]


def test_unknown_language_raises():
    """An unknown language raises ValueError."""
    try:
        analyze_semantics("NonExistentLanguage")
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "Unknown language" in str(e)


def test_fingerprint_format_valid():
    """The semantic fingerprint is well-formed."""
    lang_info = get_current_language()
    profile = analyze_semantics(lang_info["current_language"])
    fp = format_semantic_fingerprint(lang_info, profile)
    assert len(fp) > 200
    assert lang_info["current_language"] in fp
    assert "Paradigm" in fp or "paradigm" in fp.lower()


def test_fingerprint_shows_all_sections():
    """Fingerprint contains all required sections."""
    lang_info = get_current_language()
    profile = analyze_semantics(lang_info["current_language"])
    fp = format_semantic_fingerprint(lang_info, profile)
    for section in ["Existence", "Action", "State", "Relation", "Identity", "Control", "Abstraction"]:
        assert section.lower() in fp.lower(), f"Missing section: {section}"


def test_next_language_different_from_current():
    """Next language is different from current (unless there's only one)."""
    lang_info = get_current_language()
    assert lang_info["current_language"] != lang_info["next_language"]


def test_run_tests_passes():
    """run_tests() executes without raising."""
    run_tests()


if __name__ == "__main__":
    import traceback

    tests = [
        test_rotation_file_exists,
        test_rotation_order_correct,
        test_current_language_from_rotation,
        test_rotation_index_advances,
        test_all_languages_have_semantic_profiles,
        test_unknown_language_raises,
        test_fingerprint_format_valid,
        test_fingerprint_shows_all_sections,
        test_next_language_different_from_current,
        test_run_tests_passes,
    ]

    failures = []
    for test in tests:
        try:
            test()
            print(f"✅ {test.__name__}")
        except Exception as e:
            failures.append((test.__name__, str(e)))
            print(f"❌ {test.__name__}: {e}")
            traceback.print_exc()

    print(f"\n{'='*60}")
    if failures:
        print(f"FAILED: {len(failures)}/{len(tests)}")
        for name, err in failures:
            print(f"  {name}: {err}")
        sys.exit(1)
    else:
        print(f"ALL PASSED: {len(tests)}/{len(tests)}")