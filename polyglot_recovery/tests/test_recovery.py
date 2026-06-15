"""Tests for polyglot_recovery."""

import json
import tempfile
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from polyglot_recovery.src.recovery import (
    TOOL_NAME,
    TOOL_VERSION,
    ROTATION_ORDER,
    RECOVERY_DB,
    advance_rotation,
    get_current_language,
    get_recovery_map,
    get_recovery_comparison,
    generate_recovery_report,
    format_recovery_report,
    classify_resilience_tag,
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


# ── recovery DB tests ──────────────────────────────────────────────────────────

def test_recovery_db_has_all_languages():
    for lang in LANGS:
        assert lang in RECOVERY_DB, f"{lang} missing from RECOVERY_DB"


def test_recovery_db_has_all_five_dimensions():
    DIMS = ("model", "retry", "degrade", "circuit", "resurrect")
    for lang in LANGS:
        for dim in DIMS:
            assert dim in RECOVERY_DB[lang], f"{lang}/{dim} missing"


def test_recovery_db_dimensions_have_required_fields():
    REQUIRED = ("strategy", "mechanism", "idiom", "key_traits", "resilience_tag", "emoji")
    for lang in LANGS:
        for dim, data in RECOVERY_DB[lang].items():
            for field in REQUIRED:
                assert field in data, f"{lang}/{dim} missing '{field}'"


def test_all_resilience_tags_are_valid():
    VALID_TAGS = {"PROVEN", "NOMINAL", "ADAPTED", "BUILTIN", "MANUAL", "RUNTIME"}
    for lang in LANGS:
        for dim, data in RECOVERY_DB[lang].items():
            tag = data.get("resilience_tag")
            assert tag in VALID_TAGS, f"{lang}/{dim} has invalid tag {tag!r}"


def test_all_language_emojis_are_non_empty():
    for lang in LANGS:
        for dim, data in RECOVERY_DB[lang].items():
            emoji = data.get("emoji", "")
            assert len(emoji) > 0, f"{lang}/{dim} has empty emoji"


# ── resilience classification ────────────────────────────────────────────────

def test_classify_resilience_tag():
    assert "compile-time" in classify_resilience_tag("PROVEN")
    assert "compile-time" in classify_resilience_tag("NOMINAL")
    assert "runtime" in classify_resilience_tag("RUNTIME")
    assert "ecosystem" in classify_resilience_tag("BUILTIN")
    assert "manual" in classify_resilience_tag("MANUAL")
    assert "ecosystem" in classify_resilience_tag("ADAPTED")


# ── get_recovery_map tests ──────────────────────────────────────────────────

def test_get_recovery_map_returns_five_dimensions():
    for lang in LANGS:
        m = get_recovery_map(lang)
        assert len(m) == 5
        for dim in ("model", "retry", "degrade", "circuit", "resurrect"):
            assert dim in m


def test_get_recovery_map_unknown_language_returns_empty():
    m = get_recovery_map("NonExistentLang")
    assert m == {}


# ── get_recovery_comparison tests ─────────────────────────────────────────

def test_get_recovery_comparison_has_all_dimensions():
    for lang in LANGS:
        comp = get_recovery_comparison(lang)
        for dim in ("model", "retry", "degrade", "circuit", "resurrect"):
            assert dim in comp


def test_get_recovery_comparison_source_language_is_correct():
    for lang in LANGS:
        comp = get_recovery_comparison(lang)
        for dim, row in comp.items():
            assert row["source_language"] == lang


def test_get_recovery_comparison_includes_all_other_languages():
    for lang in LANGS:
        comp = get_recovery_comparison(lang)
        for dim, row in comp.items():
            for other in LANGS:
                if other != lang:
                    assert other in row, f"{lang}/{dim} missing {other}"


# ── generate_recovery_report tests ─────────────────────────────────────────

def test_generate_recovery_report_basic(tmp_path):
    path = str(tmp_path / "rotation.json")
    with open(path, "w") as f:
        json.dump({"languages": LANGS, "current_index": 0, "last_language": "Rust"}, f)

    m = generate_recovery_report(rotate=True, config_path=path)

    assert m["tool"] == TOOL_NAME
    assert m["version"] == TOOL_VERSION
    assert m["language"] == "Rust"
    assert m["current_index"] == 0
    assert m["new_index"] == 1
    assert m["rotated"] is True
    assert len(m["recovery_dimensions"]) == 5


def test_generate_recovery_report_updates_rotation(tmp_path):
    path = str(tmp_path / "rotation.json")
    with open(path, "w") as f:
        json.dump({"languages": LANGS, "current_index": 5, "last_language": "JavaScript"}, f)

    m = generate_recovery_report(rotate=True, config_path=path)

    with open(path) as f:
        data = json.load(f)
    assert data["current_index"] == 6
    assert data["last_language"] == "JavaScript"


def test_generate_recovery_report_no_rotate(tmp_path):
    path = str(tmp_path / "rotation.json")
    with open(path, "w") as f:
        json.dump({"languages": LANGS, "current_index": 3, "last_language": "Kotlin"}, f)

    m = generate_recovery_report(rotate=False, config_path=path)

    assert m["rotated"] is False
    assert m["new_index"] is None

    with open(path) as f:
        data = json.load(f)
    assert data["current_index"] == 3  # unchanged


def test_generate_recovery_report_all_dimensions_present(tmp_path):
    path = str(tmp_path / "rotation.json")
    with open(path, "w") as f:
        json.dump({"languages": LANGS, "current_index": 1, "last_language": "Go"}, f)

    m = generate_recovery_report(rotate=False, config_path=path)

    dims = m["recovery_dimensions"]
    dim_names = {d["dimension"] for d in dims}
    assert dim_names == {"model", "retry", "degrade", "circuit", "resurrect"}


def test_generate_recovery_report_cross_language_comparison(tmp_path):
    path = str(tmp_path / "rotation.json")
    with open(path, "w") as f:
        json.dump({"languages": LANGS, "current_index": 0, "last_language": "Rust"}, f)

    m = generate_recovery_report(rotate=False, config_path=path)

    comp = m["cross_language_comparison"]
    assert "model" in comp
    assert "retry" in comp
    for other in LANGS:
        if other != "Rust":
            assert other in comp["model"]


def test_generate_recovery_report_rotation_order_in_response(tmp_path):
    path = str(tmp_path / "rotation.json")
    with open(path, "w") as f:
        json.dump({"languages": LANGS, "current_index": 0, "last_language": "Rust"}, f)

    m = generate_recovery_report(rotate=False, config_path=path)
    assert m["rotation_order"] == ROTATION_ORDER


# ── format_recovery_report tests ───────────────────────────────────────────

def test_format_recovery_report_contains_language(tmp_path):
    path = str(tmp_path / "rotation.json")
    with open(path, "w") as f:
        json.dump({"languages": LANGS, "current_index": 0, "last_language": "Rust"}, f)

    m = generate_recovery_report(rotate=False, config_path=path)
    output = format_recovery_report(m)
    assert "Rust" in output
    assert "RECOVERY DIMENSIONS" in output


def test_format_recovery_report_contains_all_dimensions(tmp_path):
    path = str(tmp_path / "rotation.json")
    with open(path, "w") as f:
        json.dump({"languages": LANGS, "current_index": 0, "last_language": "Rust"}, f)

    m = generate_recovery_report(rotate=False, config_path=path)
    output = format_recovery_report(m)
    for label in ("RECOVERY MODEL", "RETRY MECHANISM", "GRACEFUL DEGRADATION",
                  "CIRCUIT BREAKER", "RESURRECTION"):
        assert label in output


# ── integration: full rotation cycle ─────────────────────────────────────

def test_full_rotation_cycle_wraps(tmp_path):
    path = str(tmp_path / "rotation.json")
    with open(path, "w") as f:
        json.dump({"languages": LANGS, "current_index": 7, "last_language": "C/C++"}, f)

    # Advance from last language
    m = generate_recovery_report(rotate=True, config_path=path)
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
        m = generate_recovery_report(rotate=True, config_path=path)
        seen.add(m["language"])

    assert seen == set(LANGS)


def test_recovery_dimensions_have_non_empty_key_traits(tmp_path):
    path = str(tmp_path / "rotation.json")
    with open(path, "w") as f:
        json.dump({"languages": LANGS, "current_index": 0, "last_language": "Rust"}, f)

    m = generate_recovery_report(rotate=False, config_path=path)
    for dim in m["recovery_dimensions"]:
        assert len(dim["key_traits"]) >= 2, f"{dim['dimension']} needs more key_traits"
        assert len(dim["mechanism"]) > 5
        assert len(dim["idiom"]) > 5


def test_recovery_db_all_dimensions_have_non_empty_fields(tmp_path):
    REQUIRED = ("strategy", "mechanism", "idiom")
    for lang in LANGS:
        for dim, data in RECOVERY_DB[lang].items():
            for field in REQUIRED:
                val = data.get(field, "")
                assert len(val) > 5, f"{lang}/{dim}/{field} too short"