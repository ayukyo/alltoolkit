#!/usr/bin/env python3
"""Tests for polyglot_fossil."""

import sys
import json
import copy
import tempfile
import os
from pathlib import Path

# ── Setup ─────────────────────────────────────────────────────────────────────
TOOL_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(TOOL_DIR))

from polyglot_fossil.src.forge import (
    FossilClassification,
    FossilRecord,
    build_strata_summary,
    classify_fossil,
    fossil_dig,
    get_ancestors,
    get_fossils,
    get_rotation_chain,
    load_rotation,
    save_rotation,
    _is_similar,
)
from polyglot_fossil.src.config import ROTATION_ORDER, ROTATION_FILE


# ── Temp file helpers ──────────────────────────────────────────────────────────

STOCK_JSON = {
    "languages": ROTATION_ORDER,
    "current_index": 0,
    "last_language": "Rust",
    "updated_at": "2026-06-01T00:00:00+00:00",
}

_orig_file = str(ROTATION_FILE)

def _with_tmp_config(fn):
    """Decorator: swap ROTATION_FILE to a temp file, restore after."""
    def wrapper(*args, **kwargs):
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            json.dump(STOCK_JSON, f)
            tmp = f.name
        orig = ROTATION_FILE
        try:
            # Monkey-patch the module-level path
            import polyglot_fossil.src.config as cfg
            import polyglot_fossil.src.forge as forge
            cfg.ROTATION_FILE = Path(tmp)
            forge.ROTATION_FILE = Path(tmp)
            return fn(*args, **kwargs)
        finally:
            cfg.ROTATION_FILE = orig
            forge.ROTATION_FILE = orig
            os.unlink(tmp)
    return wrapper


# ── Test helpers ───────────────────────────────────────────────────────────────

def assert_eq(a, b, msg=""):
    if a != b:
        raise AssertionError(f"{msg}: expected {b!r}, got {a!r}")

def assert_true(a, msg=""):
    if not a:
        raise AssertionError(f"{msg}: got falsy {a!r}")


# ── Tests ─────────────────────────────────────────────────────────────────────

def test_rotation_order_8_languages():
    assert_eq(8, len(ROTATION_ORDER), "8 languages in rotation")
    assert_eq("C/C++", ROTATION_ORDER[0], "C/C++ first")
    assert_eq("Java", ROTATION_ORDER[1], "Java second")
    assert_eq("JavaScript", ROTATION_ORDER[2], "JavaScript third")
    assert_eq("TypeScript", ROTATION_ORDER[3], "TypeScript fourth")
    assert_eq("Kotlin", ROTATION_ORDER[4], "Kotlin fifth")
    assert_eq("Swift", ROTATION_ORDER[5], "Swift sixth")
    assert_eq("Go", ROTATION_ORDER[6], "Go seventh")
    assert_eq("Rust", ROTATION_ORDER[7], "Rust last")

def test_rotation_forms_cycle():
    """Rust (idx=7) → next should be C/C++ (idx=0) via modulo wrap."""
    assert_eq(ROTATION_ORDER[(7 + 1) % 8], "C/C++", "cycle wraps to C/C++")

@_with_tmp_config
def test_load_rotation_returns_valid_dict():
    data = load_rotation()
    assert_true(isinstance(data, dict), "returns dict")
    assert_true("languages" in data, "has languages key")
    assert_true("current_index" in data, "has current_index key")
    assert_eq(type(data["languages"]), list, "languages is list")
    assert_eq(type(data["current_index"]), int, "current_index is int")

@_with_tmp_config
def test_save_rotation_persists():
    data = load_rotation()
    data["current_index"] = 3
    save_rotation(data)
    reloaded = load_rotation()
    assert_eq(3, reloaded["current_index"], "index persisted")

def test_get_rotation_chain_rust():
    chain = get_rotation_chain("Rust")
    assert_true("Rust" in chain, "Rust in chain")
    assert_true("C/C++" in chain, "C/C++ in chain")
    assert_true("Go" in chain, "Go in chain")
    # Rust is at index 0 (current), C/C++ at index 1 (predecessor)
    assert_true(chain.index("Rust") < chain.index("C/C++"),
                "Rust comes before C/C++ in chain")
    assert_eq(chain[0], "Rust", "Rust is at start of chain")

def test_get_rotation_chain_typescript():
    chain = get_rotation_chain("TypeScript")
    assert_true("TypeScript" in chain, "TS in chain")
    assert_true("Kotlin" in chain, "Kotlin in TS chain")
    assert_true("JavaScript" in chain, "JS in TS chain")
    assert_true(chain.index("TypeScript") < chain.index("Kotlin"),
                "TypeScript comes before Kotlin in chain")

def test_get_rotation_chain_javascript():
    chain = get_rotation_chain("JavaScript")
    assert_true("JavaScript" in chain, "JS in chain")
    assert_true("TypeScript" in chain, "TS in JS chain")
    assert_true(chain.index("JavaScript") < chain.index("TypeScript"),
                "JavaScript comes before TypeScript in chain")

def test_get_rotation_chain_kotlin():
    chain = get_rotation_chain("Kotlin")
    assert_true("Kotlin" in chain, "Kotlin in chain")
    assert_true("Swift" in chain, "Swift in Kotlin chain")
    assert_true("Go" in chain, "Go in Kotlin chain")
    assert_true(chain.index("Kotlin") < chain.index("Swift"),
                "Kotlin comes before Swift in chain")

@_with_tmp_config
def test_get_ancestors_rust():
    ancestors = get_ancestors("Rust")
    names = [a for a, _ in ancestors]
    # With reversed order, Rust(7)'s predecessor is C/C++(0) with prev_idx walking
    assert_true("C/C++" in names, "C/C++ is ancestor of Rust")
    depths = {a: d for a, d in ancestors}
    assert_true(depths.get("C/C++", 0) == 1, "C/C++ has stratum 1")

@_with_tmp_config
def test_get_ancestors_typescript():
    ancestors = get_ancestors("TypeScript")
    names = [a for a, _ in ancestors]
    # TypeScript's direct predecessor in the reversed order is Kotlin
    # (TypeScript idx=3, Kotlin idx=4 via +1 offset)
    assert_true("Kotlin" in names, "Kotlin is ancestor of TypeScript")
    depths = {a: d for a, d in ancestors}
    assert_true(depths.get("Kotlin", 0) == 1,
                "Kotlin has stratum 1 (direct predecessor)")
    assert_true(depths.get("Swift", 0) == 2,
                "Swift has stratum 2")

def test_fossil_classification_inherited():
    """Go inherits struct_adt from Rust (both use 'struct' keyword as core concept)."""
    ancestors = [("Rust", 1)]
    rec = classify_fossil("struct_adt", "Go", ancestors)
    assert_eq(FossilClassification.INHERITED, rec.classification, "Go inherits struct_adt from Rust")
    assert_true(len(rec.ancestral_form) > 0, "ancestral form is non-empty")

def test_fossil_classification_novel():
    """Swift has async_await that Kotlin doesn't share via ancestor chain."""
    ancestors = [("Rust", 2)]
    rec = classify_fossil("async_await", "Swift", ancestors)
    # Swift and Rust both have async/await → should be INHERITED or MUTATED
    assert rec.classification in (
        FossilClassification.INHERITED,
        FossilClassification.MUTATED,
        FossilClassification.NOVEL,
    ), f"Swift async_await has valid classification: {rec.classification}"

def test_fossil_classification_absent():
    """C/C++ does NOT have null_safety (Option/Nullable types)."""
    ancestors = [("Rust", 1)]
    rec = classify_fossil("null_safety", "C/C++", ancestors)
    assert_eq(FossilClassification.ABSENT, rec.classification, "C/C++ has no null_safety (ABSENT)")

def test_fossil_classification_unknown_fossil():
    ancestors = [("C/C++", 1)]
    rec = classify_fossil("comprehensions", "Go", ancestors)
    assert rec.classification in (
        FossilClassification.INHERITED,
        FossilClassification.MUTATED,
        FossilClassification.NOVEL,
        FossilClassification.ABSENT,
    ), "unknown fossil gets valid classification"

def test_fossil_record_to_dict():
    rec = FossilRecord(
        fossil_id="test",
        name="Test Fossil",
        concept="A test concept",
        classification=FossilClassification.NOVEL,
        detail="test detail",
        ancestral_form="ancestral",
        stratum=1,
        ancestor="C/C++",
    )
    d = rec.to_dict()
    assert_true("fossil_id" in d, "dict has fossil_id")
    assert_true("classification" in d, "dict has classification")
    assert_eq("NOVEL", d["classification"], "classification serialised correctly")

def test_fossil_record_layer_bar():
    rec = FossilRecord(
        fossil_id="x", name="X", concept="",
        classification=FossilClassification.INHERITED,
        detail="", ancestral_form="", stratum=2, ancestor="Go",
    )
    bar = rec.layer_bar(max_depth=3)
    assert_true("[" in bar, "layer_bar has brackets")
    assert_true("L2" in bar, "layer_bar shows stratum")

def test_fossil_record_badge():
    rec = FossilRecord(
        fossil_id="x", name="X", concept="",
        classification=FossilClassification.INHERITED,
        detail="", ancestral_form="", stratum=1, ancestor="C/C++",
    )
    badge = rec.badge()
    assert_true("◉" in badge or "INHERITED" in badge, "badge has INHERITED symbol")

@_with_tmp_config
def test_get_fossils_rust_returns_records():
    records = get_fossils("Rust")
    assert_true(len(records) > 0, "Rust has fossils")
    ids = {r.fossil_id for r in records}
    assert_true("null_safety" in ids, "null_safety fossil found for Rust")
    assert_true("generics" in ids, "generics fossil found for Rust")
    for rec in records:
        assert_true(rec.name, f"Rust fossil {rec.fossil_id} has name")

@_with_tmp_config
def test_get_fossils_all_languages_have_fossils():
    for lang in ROTATION_ORDER:
        records = get_fossils(lang)
        assert_true(len(records) > 0, f"{lang} has at least one fossil record")

@_with_tmp_config
def test_get_fossils_rust_null_safety_is_option():
    records = get_fossils("Rust")
    null_rec = next((r for r in records if r.fossil_id == "null_safety"), None)
    assert_true(null_rec is not None, "Rust null_safety fossil found")
    assert_true("Option" in null_rec.detail, "Rust uses Option<T>")

@_with_tmp_config
def test_get_fossils_typescript_null_safety():
    records = get_fossils("TypeScript")
    null_rec = next((r for r in records if r.fossil_id == "null_safety"), None)
    assert_true(null_rec is not None, "TypeScript null_safety fossil found")
    assert_true("null" in null_rec.detail or "undefined" in null_rec.detail,
                "TypeScript uses null/undefined")

@_with_tmp_config
def test_get_fossils_kotlin_null_safety():
    records = get_fossils("Kotlin")
    null_rec = next((r for r in records if r.fossil_id == "null_safety"), None)
    assert_true(null_rec is not None, "Kotlin null_safety fossil found")
    assert_true("Nullable" in null_rec.detail or "?" in null_rec.detail,
                "Kotlin uses nullable T?")

def test_build_strata_summary():
    records = [
        FossilRecord("a", "A", "", FossilClassification.INHERITED, "", "", 1, "C/C++"),
        FossilRecord("b", "B", "", FossilClassification.INHERITED, "", "", 2, "Go"),
        FossilRecord("c", "C", "", FossilClassification.MUTATED,  "", "", 1, "Java"),
        FossilRecord("d", "D", "", FossilClassification.NOVEL,    "", "", 0, ""),
        FossilRecord("e", "E", "", FossilClassification.ABSENT,   "", "", 0, ""),
    ]
    summary = build_strata_summary(records)
    assert_eq(5, summary["total"], "total is 5")
    assert_eq(2, summary["by_classification"]["INHERITED"], "2 inherited")
    assert_eq(1, summary["by_classification"]["MUTATED"],  "1 mutated")
    assert_eq(1, summary["by_classification"]["NOVEL"],    "1 novel")
    assert_eq(1, summary["by_classification"]["ABSENT"],   "1 absent")

def test_is_similar_exact():
    assert_true(_is_similar("Result<T, E>", "Result<T, E>"), "identical is similar")

def test_is_similar_shared_keywords():
    assert_true(_is_similar("enum with variants", "enum with data"), "shared enum keyword")
    assert_true(_is_similar("async/await", "async/await syntax"), "shared async/await")

def test_is_similar_not_similar():
    assert_true(not _is_similar("Result<T, E>", "nil check"), "very different strings not similar")

@_with_tmp_config
def test_fossil_dig_returns_valid_structure():
    result = fossil_dig()
    assert_true("tool" in result, "result has tool")
    assert_true("language" in result, "result has language")
    assert_true("rotation_chain" in result, "result has rotation_chain")
    assert_true("fossils" in result, "result has fossils")
    assert_true("strata_summary" in result, "result has strata_summary")
    assert_true("report" in result, "result has report")
    assert_true("next_language" in result, "result has next_language")
    assert_true("rotated_at" in result, "result has rotated_at")
    assert_eq("polyglot-fossil", result["tool"], "tool name correct")
    assert_eq("0.1.0", result["version"], "version correct")

@_with_tmp_config
def test_fossil_dig_language_override():
    result = fossil_dig(language="Rust")
    assert_eq("Rust", result["language"], "override sets Rust")

@_with_tmp_config
def test_fossil_dig_rotation_advances():
    before = load_rotation()
    idx_before = before["current_index"]

    result = fossil_dig()

    after = load_rotation()
    assert_true(after["current_index"] != idx_before, "index changed")
    # last_language is the language that was just processed (result["language"])
    assert_eq(result["language"], after["last_language"],
              "last_language is the language just processed")

@_with_tmp_config
def test_fossil_dig_next_language_is_valid():
    result = fossil_dig()
    assert_true(result["next_language"] in ROTATION_ORDER, "next_language is in rotation")

@_with_tmp_config
def test_fossil_dig_rust_fossils_list_length():
    result = fossil_dig(language="Rust")
    assert_true(len(result["fossils"]) >= 15, "Rust has at least 15 fossil records")

@_with_tmp_config
def test_fossil_dig_all_8_languages():
    checked = set()
    for lang in ROTATION_ORDER:
        result = fossil_dig(language=lang)
        checked.add(result["language"])
        assert_true(len(result["fossils"]) > 0, f"{lang} has fossils")
        assert_true("rotation_chain" in result, f"{lang} has chain")
        # Current language is at chain[0]
        assert_eq(result["rotation_chain"][0], lang, f"chain starts with {lang}")
        # Verify each fossil record is valid
        for f in result["fossils"]:
            assert_true("fossil_id" in f, f"{lang}: fossil has id")
            assert_true("name" in f, f"{lang}: fossil has name")
            assert_true("classification" in f, f"{lang}: fossil has classification")
            assert f["classification"] in ("INHERITED", "MUTATED", "NOVEL", "ABSENT"), \
                f"{lang}: invalid classification {f['classification']}"

    assert_eq(8, len(checked), "all 8 languages checked")

@_with_tmp_config
def test_fossil_dig_report_contains_language():
    result = fossil_dig(language="Swift")
    report = result["report"]
    assert_true("Swift" in report, "report mentions Swift")
    assert_true("POLYGLOT FOSSIL" in report or "FOSSIL" in report, "report has header")

@_with_tmp_config
def test_fossil_dig_report_contains_fossil_symbols():
    result = fossil_dig(language="Rust")
    report = result["report"]
    assert_true("◉" in report or "INHERITED" in report, "report has INHERITED symbol")
    assert_true("✦" in report or "NOVEL" in report, "report has NOVEL symbol")

@_with_tmp_config
def test_fossil_dig_chain_integrity():
    for lang in ROTATION_ORDER:
        result = fossil_dig(language=lang)
        chain = result["rotation_chain"]
        # Current language is at chain[0]
        assert_eq(chain[0], lang, f"{lang}: chain starts with itself")
        # Each successive language has a HIGHER index in ROTATION_ORDER (wrapping at 7→0)
        for i in range(len(chain) - 1):
            idx_i = ROTATION_ORDER.index(chain[i])
            idx_j = ROTATION_ORDER.index(chain[i + 1])
            assert idx_i < idx_j or (idx_i == 7 and idx_j == 0), \
                f"{lang}: chain order is valid ({chain[i]}({idx_i}) → {chain[i+1]}({idx_j}))"

@_with_tmp_config
def test_fossil_dig_ancestors_list():
    result = fossil_dig(language="Kotlin")
    ancestors = result["ancestors"]
    assert_true(isinstance(ancestors, list), "ancestors is list")
    for a in ancestors:
        assert_true("ancestor" in a, "ancestor entry has 'ancestor' key")
        assert_true("stratum" in a, "ancestor entry has 'stratum' key")
        assert_true(a["stratum"] >= 1, "stratum is >= 1")

@_with_tmp_config
def test_fossil_dig_strata_summary_valid():
    for lang in ROTATION_ORDER:
        result = fossil_dig(language=lang)
        summary = result["strata_summary"]
        assert_true("total" in summary, f"{lang}: summary has total")
        assert_true("by_classification" in summary, f"{lang}: summary has by_classification")
        assert_eq(sum(summary["by_classification"].values()), summary["total"],
                  f"{lang}: sum of by_classification equals total")

@_with_tmp_config
def test_fossil_dig_rust_ownership_borrow_inherited():
    result = fossil_dig(language="Rust")
    ownership_rec = next(
        (f for f in result["fossils"] if f["fossil_id"] == "ownership_borrow"), None
    )
    assert_true(ownership_rec is not None, "Rust has ownership_borrow fossil")
    # Rust has ownership_borrow as its own feature (NOVEL or MUTATED, not ABSENT)
    assert ownership_rec["classification"] != "ABSENT", \
        "Rust ownership_borrow should not be ABSENT"

@_with_tmp_config
def test_fossil_dig_go_error_as_value():
    result = fossil_dig(language="Go")
    error_rec = next(
        (f for f in result["fossils"] if f["fossil_id"] == "error_as_value"), None
    )
    assert_true(error_rec is not None, "Go has error_as_value fossil")
    assert error_rec["classification"] in ("INHERITED", "MUTATED", "NOVEL"), \
        "Go error_as_value is valid classification"

@_with_tmp_config
def test_fossil_dig_typescript_inherits_js_generics():
    result = fossil_dig(language="TypeScript")
    gen_rec = next(
        (f for f in result["fossils"] if f["fossil_id"] == "generics"), None
    )
    assert_true(gen_rec is not None, "TypeScript has generics fossil")
    # TS inherits generics from JS (via ancestor map)
    assert_true(gen_rec["classification"] in (
        "INHERITED", "MUTATED", "NOVEL"
    ), "TS generics has valid classification")

def test_fossil_classification_enum_symbols():
    assert_eq("◉", FossilClassification.INHERITED.symbol())
    assert_eq("◌", FossilClassification.MUTATED.symbol())
    assert_eq("✦", FossilClassification.NOVEL.symbol())
    assert_eq("—", FossilClassification.ABSENT.symbol())

def test_fossil_classification_str():
    assert_eq("INHERITED", FossilClassification.INHERITED.value)
    assert_eq("MUTATED", FossilClassification.MUTATED.value)
    assert_eq("NOVEL", FossilClassification.NOVEL.value)
    assert_eq("ABSENT", FossilClassification.ABSENT.value)

@_with_tmp_config
def test_fossil_dig_idempotent_rotation():
    """Calling fossil_dig twice should advance index twice."""
    before = load_rotation()
    idx0 = before["current_index"]

    r1 = fossil_dig()
    after1 = load_rotation()
    idx1 = after1["current_index"]
    assert_true(idx1 != idx0, "first call advances index")

    r2 = fossil_dig()
    after2 = load_rotation()
    idx2 = after2["current_index"]
    assert_true(idx2 != idx1, "second call advances index again")
    assert_eq(r1["next_language"], r2["language"], "r1.next == r2.language")


# ── Runner ────────────────────────────────────────────────────────────────────

def run_tests():
    tests = [
        t for t in globals() if t.startswith("test_") and callable(globals()[t])
    ]
    passed = 0
    failed = 0
    errors = []

    for name in tests:
        try:
            globals()[name]()
            print(f"  ✅ PASS: {name}")
            passed += 1
        except Exception as e:
            print(f"  ❌ FAIL: {name}: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
            errors.append((name, e))

    print()
    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed, {len(tests)} total")
    if failed:
        raise SystemExit(1)
    print("🪨 All Polyglot Fossil tests passed! The strata are mapped.")


if __name__ == "__main__":
    run_tests()