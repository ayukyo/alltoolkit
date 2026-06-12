"""Tests for polyglot_signal."""

import json
import tempfile
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from polyglot_signal.src.signal import (
    TOOL_NAME,
    TOOL_VERSION,
    ROTATION_ORDER,
    SIGNAL_DB,
    advance_rotation,
    get_current_language,
    get_signal_map,
    get_signal_comparison,
    generate_signal_report,
    format_signal_report,
    classify_signal_strength,
    _load_rotation,
    _save_rotation,
)

LANGS = ROTATION_ORDER


# ── config tests ─────────────────────────────────────────────────────────────

def test_load_rotation(tmp_path):
    path = str(tmp_path / "rotation.json")
    with open(path, "w") as f:
        json.dump({"languages": LANGS, "current_index": 3, "last_language": "Kotlin"}, f)
    data = _load_rotation(path)
    assert data["languages"] == LANGS
    assert data["current_index"] == 3


def test_save_rotation_roundtrip(tmp_path):
    path = str(tmp_path / "rotation.json")
    original = {"languages": LANGS, "current_index": 5, "last_language": "JavaScript"}
    _save_rotation(original, path)
    loaded = _load_rotation(path)
    assert loaded == original


def test_advance_rotation_basic(tmp_path):
    path = str(tmp_path / "rotation.json")
    with open(path, "w") as f:
        json.dump({"languages": LANGS, "current_index": 2, "last_language": "Swift"}, f)

    result = advance_rotation(path)
    assert result == "Swift"

    with open(path) as f:
        data = json.load(f)
    assert data["current_index"] == 3
    assert data["last_language"] == "Swift"


def test_advance_rotation_wraps_around(tmp_path):
    path = str(tmp_path / "rotation.json")
    with open(path, "w") as f:
        json.dump({"languages": LANGS, "current_index": 7, "last_language": "C/C++"}, f)

    result = advance_rotation(path)
    assert result == "C/C++"

    with open(path) as f:
        data = json.load(f)
    assert data["current_index"] == 0
    assert data["last_language"] == "C/C++"


def test_get_current_language(tmp_path):
    path = str(tmp_path / "rotation.json")
    with open(path, "w") as f:
        json.dump({"languages": LANGS, "current_index": 4, "last_language": "TypeScript"}, f)

    lang = get_current_language(path)
    assert lang == "TypeScript"


# ── signal map tests ──────────────────────────────────────────────────────────

def test_signal_db_has_all_languages():
    for lang in LANGS:
        assert lang in SIGNAL_DB, f"{lang} missing from SIGNAL_DB"


def test_signal_db_has_all_five_categories():
    CATS = ("error", "absence", "warning", "success", "async")
    for lang in LANGS:
        for cat in CATS:
            assert cat in SIGNAL_DB[lang], f"{lang}/{cat} missing"


def test_signal_db_categories_have_required_fields():
    REQUIRED = ("signal", "mechanism", "idiom", "key_traits", "signal_tag", "emoji")
    for lang in LANGS:
        for cat, data in SIGNAL_DB[lang].items():
            for field in REQUIRED:
                assert field in data, f"{lang}/{cat} missing '{field}'"


def test_all_signal_tags_are_valid():
    VALID_TAGS = {"PROVEN", "NOMINAL", "ADAPTED", "RUNTIME"}
    for lang in LANGS:
        for cat, data in SIGNAL_DB[lang].items():
            tag = data.get("signal_tag")
            assert tag in VALID_TAGS, f"{lang}/{cat} has invalid tag {tag!r}"


def test_all_language_emojis_are_non_empty():
    for lang in LANGS:
        for cat, data in SIGNAL_DB[lang].items():
            emoji = data.get("emoji", "")
            assert len(emoji) > 0, f"{lang}/{cat} has empty emoji"


# ── signal strength classification ──────────────────────────────────────────

def test_classify_signal_strength():
    assert "compile-time" in classify_signal_strength("PROVEN")
    assert "compile-time" in classify_signal_strength("NOMINAL")
    assert "runtime" in classify_signal_strength("RUNTIME")
    assert "hybrid" in classify_signal_strength("ADAPTED")


# ── get_signal_map tests ─────────────────────────────────────────────────────

def test_get_signal_map_returns_five_categories():
    for lang in LANGS:
        m = get_signal_map(lang)
        assert len(m) == 5
        for cat in ("error", "absence", "warning", "success", "async"):
            assert cat in m


def test_get_signal_map_unknown_language_returns_empty():
    m = get_signal_map("NonExistentLang")
    assert m == {}


# ── get_signal_comparison tests ──────────────────────────────────────────────

def test_get_signal_comparison_has_all_categories():
    for lang in LANGS:
        comp = get_signal_comparison(lang)
        for cat in ("error", "absence", "warning", "success", "async"):
            assert cat in comp


def test_get_signal_comparison_source_language_is_correct():
    for lang in LANGS:
        comp = get_signal_comparison(lang)
        for cat, row in comp.items():
            assert row["source_language"] == lang


def test_get_signal_comparison_includes_all_other_languages():
    for lang in LANGS:
        comp = get_signal_comparison(lang)
        for cat, row in comp.items():
            for other in LANGS:
                if other != lang:
                    assert other in row, f"{lang}/{cat} missing {other}"


# ── generate_signal_report tests ─────────────────────────────────────────────

def test_generate_signal_report_basic(tmp_path):
    path = str(tmp_path / "rotation.json")
    with open(path, "w") as f:
        json.dump({"languages": LANGS, "current_index": 0, "last_language": "Rust"}, f)

    m = generate_signal_report(rotate=True, config_path=path)

    assert m["tool"] == TOOL_NAME
    assert m["version"] == TOOL_VERSION
    assert m["language"] == "Rust"
    assert m["current_index"] == 0
    assert m["new_index"] == 1
    assert m["rotated"] is True
    assert len(m["signal_categories"]) == 5


def test_generate_signal_report_updates_rotation(tmp_path):
    path = str(tmp_path / "rotation.json")
    with open(path, "w") as f:
        json.dump({"languages": LANGS, "current_index": 5, "last_language": "JavaScript"}, f)

    m = generate_signal_report(rotate=True, config_path=path)

    with open(path) as f:
        data = json.load(f)
    assert data["current_index"] == 6
    assert data["last_language"] == "JavaScript"


def test_generate_signal_report_no_rotate(tmp_path):
    path = str(tmp_path / "rotation.json")
    with open(path, "w") as f:
        json.dump({"languages": LANGS, "current_index": 3, "last_language": "Kotlin"}, f)

    m = generate_signal_report(rotate=False, config_path=path)

    assert m["rotated"] is False
    assert m["new_index"] is None

    with open(path) as f:
        data = json.load(f)
    assert data["current_index"] == 3  # unchanged


def test_generate_signal_report_all_categories_present(tmp_path):
    path = str(tmp_path / "rotation.json")
    with open(path, "w") as f:
        json.dump({"languages": LANGS, "current_index": 1, "last_language": "Go"}, f)

    m = generate_signal_report(rotate=False, config_path=path)

    cats = m["signal_categories"]
    cat_names = {c["category"] for c in cats}
    assert cat_names == {"error", "absence", "warning", "success", "async"}


def test_generate_signal_report_cross_language_comparison(tmp_path):
    path = str(tmp_path / "rotation.json")
    with open(path, "w") as f:
        json.dump({"languages": LANGS, "current_index": 0, "last_language": "Rust"}, f)

    m = generate_signal_report(rotate=False, config_path=path)

    comp = m["cross_language_comparison"]
    assert "error" in comp
    assert "absence" in comp
    for other in LANGS:
        if other != "Rust":
            assert other in comp["error"]


def test_generate_signal_report_rotation_order_in_response(tmp_path):
    path = str(tmp_path / "rotation.json")
    with open(path, "w") as f:
        json.dump({"languages": LANGS, "current_index": 0, "last_language": "Rust"}, f)

    m = generate_signal_report(rotate=False, config_path=path)
    assert m["rotation_order"] == ROTATION_ORDER


# ── format_signal_report tests ────────────────────────────────────────────────

def test_format_signal_report_contains_language(tmp_path):
    path = str(tmp_path / "rotation.json")
    with open(path, "w") as f:
        json.dump({"languages": LANGS, "current_index": 0, "last_language": "Rust"}, f)

    m = generate_signal_report(rotate=False, config_path=path)
    output = format_signal_report(m)
    assert "Rust" in output
    assert "SIGNAL TAXONOMY" in output


def test_format_signal_report_contains_all_categories(tmp_path):
    path = str(tmp_path / "rotation.json")
    with open(path, "w") as f:
        json.dump({"languages": LANGS, "current_index": 0, "last_language": "Rust"}, f)

    m = generate_signal_report(rotate=False, config_path=path)
    output = format_signal_report(m)
    for cat in ("ERROR", "ABSENCE", "WARNING", "SUCCESS", "ASYNC"):
        assert cat in output


# ── integration: full rotation cycle ───────────────────────────────────────

def test_full_rotation_cycle_wraps(tmp_path):
    path = str(tmp_path / "rotation.json")
    with open(path, "w") as f:
        json.dump({"languages": LANGS, "current_index": 7, "last_language": "C/C++"}, f)

    # Advance from last language
    m = generate_signal_report(rotate=True, config_path=path)
    assert m["language"] == "C/C++"
    assert m["new_index"] == 0

    with open(path) as f:
        data = json.load(f)
    assert data["current_index"] == 0
    assert data["last_language"] == "C/C++"


def test_all_eight_languages_covered_in_cycle(tmp_path):
    path = str(tmp_path / "rotation.json")
    seen = set()
    with open(path, "w") as f:
        json.dump({"languages": LANGS, "current_index": 0, "last_language": "Rust"}, f)

    for i in range(8):
        m = generate_signal_report(rotate=True, config_path=path)
        seen.add(m["language"])

    assert seen == set(LANGS)


def test_signal_categories_have_non_empty_key_traits(tmp_path):
    path = str(tmp_path / "rotation.json")
    with open(path, "w") as f:
        json.dump({"languages": LANGS, "current_index": 0, "last_language": "Rust"}, f)

    m = generate_signal_report(rotate=False, config_path=path)
    for cat in m["signal_categories"]:
        assert len(cat["key_traits"]) >= 2, f"{cat['category']} needs more key_traits"
        assert len(cat["mechanism"]) > 5
        assert len(cat["idiom"]) > 5