"""Tests for polyglot_correspondent."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from polyglot_correspondent.src.correspondent import (
    TOOL_NAME,
    TOOL_VERSION,
    ROTATION_ORDER,
    EPISTOLARY_DB,
    TONE_FORMAL,
    TONE_OFFICIAL,
    TONE_TERSE,
    TONE_FRIENDLY,
    TONE_FLORID,
    TONE_MONOLITHIC,
    POSTAL_DIRECT,
    POSTAL_STD,
    POSTAL_REGISTRY,
    POSTAL_VENDOR,
    advance_rotation,
    get_current_language,
    get_epistolary,
    list_facets,
    get_cross_comparison,
    generate_letter,
    generate_correspondent_report,
    format_correspondent_report,
    classify_tone,
    classify_postal_route,
    _load_rotation,
    _save_rotation,
)

LANGS = ROTATION_ORDER
ALL_FACETS = list_facets()


# ── config / rotation tests ────────────────────────────────────────────────

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


def test_get_current_language(tmp_path):
    path = str(tmp_path / "rotation.json")
    with open(path, "w") as f:
        json.dump({"languages": LANGS, "current_index": 4, "last_language": "TypeScript"}, f)

    assert get_current_language(path) == "TypeScript"


# ── database integrity tests ───────────────────────────────────────────────

def test_epistolary_db_has_all_languages():
    for lang in LANGS:
        assert lang in EPISTOLARY_DB, f"missing {lang}"


def test_epistolary_db_has_all_twelve_facets():
    for lang, record in EPISTOLARY_DB.items():
        for facet in ALL_FACETS:
            assert facet in record, f"{lang} missing facet {facet}"


def test_epistolary_facets_have_required_fields():
    required_per_facet = {
        "letterhead":   ["style", "mechanism", "idiom", "key_traits"],
        "addressing":   ["style", "mechanism", "idiom", "key_traits"],
        "salutation":   ["style", "mechanism", "idiom", "key_traits"],
        "quill":        ["style", "mechanism", "idiom", "key_traits"],
        "wax_seal":     ["style", "mechanism", "idiom", "key_traits"],
        "margin_notes": ["style", "mechanism", "idiom", "key_traits"],
        "postscript":   ["style", "mechanism", "idiom", "key_traits"],
        "valediction":  ["style", "mechanism", "idiom", "key_traits"],
        "signature":    ["style", "mechanism", "idiom", "key_traits"],
        "stationery":   ["extension", "encoding", "layout", "extra"],
        "postal_route": ["system", "manager", "mechanism", "idiom"],
        "tone":         ["register", "feel"],
    }
    for lang, record in EPISTOLARY_DB.items():
        for facet, required in required_per_facet.items():
            for field in required:
                assert field in record[facet], f"{lang}.{facet} missing {field}"


def test_all_tones_are_valid():
    valid_tones = {TONE_FORMAL, TONE_OFFICIAL, TONE_TERSE,
                   TONE_FRIENDLY, TONE_FLORID, TONE_MONOLITHIC}
    for lang, record in EPISTOLARY_DB.items():
        assert record["tone"]["register"] in valid_tones, f"{lang} has invalid tone"


def test_all_postal_routes_are_valid():
    valid_routes = {POSTAL_DIRECT, POSTAL_STD, POSTAL_REGISTRY, POSTAL_VENDOR}
    for lang, record in EPISTOLARY_DB.items():
        assert record["postal_route"]["system"] in valid_routes, f"{lang} has invalid postal route"


def test_all_facet_emojis_are_non_empty():
    for lang, record in EPISTOLARY_DB.items():
        for facet in ALL_FACETS:
            assert record[facet].get("emoji"), f"{lang}.{facet} missing emoji"


def test_key_traits_have_minimum_length():
    for lang, record in EPISTOLARY_DB.items():
        for facet in ALL_FACETS:
            traits = record[facet].get("key_traits", [])
            assert len(traits) >= 2, f"{lang}.{facet} needs >=2 key_traits"
            for t in traits:
                assert isinstance(t, str) and len(t) > 0


# ── tone + postal classification tests ────────────────────────────────────

def test_classify_tone_known():
    desc = classify_tone(TONE_FORMAL)
    assert "parchment" in desc or "courteous" in desc

    desc = classify_tone(TONE_MONOLITHIC)
    assert "stone" in desc or "chiseled" in desc or "wall" in desc


def test_classify_tone_unknown():
    desc = classify_tone("UNKNOWN_REGISTER")
    assert "unknown" in desc


def test_classify_postal_route_known():
    desc = classify_postal_route(POSTAL_REGISTRY)
    assert "registry" in desc or "central" in desc

    desc = classify_postal_route(POSTAL_VENDOR)
    assert "vendored" in desc or "system" in desc


def test_classify_postal_route_unknown():
    desc = classify_postal_route("UNKNOWN_SYSTEM")
    assert "unknown" in desc


# ── epistolary access tests ────────────────────────────────────────────────

def test_get_epistolary_returns_record():
    record = get_epistolary("Rust")
    assert record["tone"]["register"] == TONE_FORMAL


def test_get_epistolary_unknown_language():
    record = get_epistolary("COBOL")
    assert record == {}


def test_list_facets_returns_twelve():
    facets = list_facets()
    assert len(facets) == 12
    assert "letterhead" in facets
    assert "tone" in facets


def test_get_cross_comparison_has_all_languages():
    comp = get_cross_comparison("wax_seal")
    assert comp["facet"] == "wax_seal"
    for lang in LANGS:
        assert lang in comp["languages"]


def test_get_cross_comparison_for_each_facet():
    for facet in ALL_FACETS:
        comp = get_cross_comparison(facet)
        assert comp["facet"] == facet
        assert len(comp["languages"]) == len(LANGS)


# ── generate_letter tests ─────────────────────────────────────────────────

def test_generate_letter_basic():
    letter = generate_letter("Rust", seed=42)
    assert letter["language"] == "Rust"
    assert letter["tone_register"] == TONE_FORMAL
    assert "opening" in letter and len(letter["opening"]) > 0
    assert "body" in letter and len(letter["body"]) > 0
    assert "closing" in letter and len(letter["closing"]) > 0
    assert "signature_line" in letter
    assert len(letter["facets"]) == 12


def test_generate_letter_opening_matches_tone():
    for tone_register in (TONE_FORMAL, TONE_OFFICIAL, TONE_TERSE,
                          TONE_FRIENDLY, TONE_FLORID, TONE_MONOLITHIC):
        # Use a language with that tone
        lang_for_tone = {
            TONE_FORMAL: "Rust",
            TONE_OFFICIAL: "Java",
            TONE_TERSE: "JavaScript",
            TONE_FRIENDLY: "Kotlin",
            TONE_FLORID: "Swift",
            TONE_MONOLITHIC: "C/C++",
        }[tone_register]
        letter = generate_letter(lang_for_tone, seed=1)
        assert letter["tone_register"] == tone_register
        assert len(letter["opening"]) > 0
        assert len(letter["closing"]) > 0


def test_generate_letter_seed_deterministic():
    l1 = generate_letter("Swift", seed=99)
    l2 = generate_letter("Swift", seed=99)
    assert l1["opening"] == l2["opening"]
    assert l1["closing"] == l2["closing"]


def test_generate_letter_seed_changes_output():
    l1 = generate_letter("Swift", seed=1)
    l2 = generate_letter("Swift", seed=2)
    # Different seeds may or may not differ, but at least one of opening/closing should
    # change OR we accept a (very rare) collision.
    # Force test: seeds far apart.
    l3 = generate_letter("Swift", seed=100000)
    assert (l1["opening"] != l3["opening"]) or (l1["closing"] != l3["closing"])


def test_generate_letter_unknown_language():
    letter = generate_letter("Erlang")
    assert "error" in letter


def test_generate_letter_body_mentions_language():
    letter = generate_letter("Go", seed=7)
    assert "Go" in letter["body"]


def test_generate_letter_facets_have_content():
    letter = generate_letter("TypeScript", seed=11)
    for facet in letter["facets"]:
        assert facet["style"] and len(facet["style"]) > 0
        assert isinstance(facet["key_traits"], list)
        assert len(facet["key_traits"]) >= 1


def test_generate_letter_cross_comparison_complete():
    letter = generate_letter("Java", seed=13)
    cross = letter["cross_comparison"]
    for facet in ALL_FACETS:
        assert facet in cross
        for lang in LANGS:
            assert lang in cross[facet]["languages"]


# ── generate_correspondent_report tests ────────────────────────────────────

def test_generate_correspondent_report_basic(tmp_path):
    path = str(tmp_path / "rotation.json")
    with open(path, "w") as f:
        json.dump({"languages": LANGS, "current_index": 0, "last_language": "Rust"}, f)

    m = generate_correspondent_report(rotate=True, config_path=path)
    assert m["tool"] == TOOL_NAME
    assert m["version"] == TOOL_VERSION
    assert m["language"] == "Rust"
    assert m["current_index"] == 0
    assert m["new_index"] == 1
    assert m["rotated"] is True
    assert len(m["facets"]) == 12


def test_generate_correspondent_report_updates_rotation(tmp_path):
    path = str(tmp_path / "rotation.json")
    with open(path, "w") as f:
        json.dump({"languages": LANGS, "current_index": 5, "last_language": "JavaScript"}, f)

    m = generate_correspondent_report(rotate=True, config_path=path)

    with open(path) as f:
        data = json.load(f)
    assert data["current_index"] == 6
    assert data["last_language"] == "JavaScript"


def test_generate_correspondent_report_no_rotate(tmp_path):
    path = str(tmp_path / "rotation.json")
    with open(path, "w") as f:
        json.dump({"languages": LANGS, "current_index": 3, "last_language": "Kotlin"}, f)

    m = generate_correspondent_report(rotate=False, config_path=path)

    assert m["rotated"] is False
    assert m["new_index"] is None

    with open(path) as f:
        data = json.load(f)
    assert data["current_index"] == 3  # unchanged


def test_generate_correspondent_report_seed_propagated(tmp_path):
    path = str(tmp_path / "rotation.json")
    with open(path, "w") as f:
        json.dump({"languages": LANGS, "current_index": 2, "last_language": "Swift"}, f)

    m = generate_correspondent_report(rotate=False, config_path=path, seed=42)
    assert m["letter"]["opening"] is not None
    assert m["letter"]["closing"] is not None


def test_generate_correspondent_report_all_facets_present(tmp_path):
    path = str(tmp_path / "rotation.json")
    with open(path, "w") as f:
        json.dump({"languages": LANGS, "current_index": 1, "last_language": "Go"}, f)

    m = generate_correspondent_report(rotate=False, config_path=path)
    facet_names = {f["facet"] for f in m["facets"]}
    assert facet_names == set(ALL_FACETS)


def test_generate_correspondent_report_rotation_order_in_response(tmp_path):
    path = str(tmp_path / "rotation.json")
    with open(path, "w") as f:
        json.dump({"languages": LANGS, "current_index": 0, "last_language": "Rust"}, f)

    m = generate_correspondent_report(rotate=False, config_path=path)
    assert m["rotation_order"] == ROTATION_ORDER


# ── format_correspondent_report tests ──────────────────────────────────────

def test_format_correspondent_report_contains_language(tmp_path):
    path = str(tmp_path / "rotation.json")
    with open(path, "w") as f:
        json.dump({"languages": LANGS, "current_index": 0, "last_language": "Rust"}, f)

    m = generate_correspondent_report(rotate=False, config_path=path)
    output = format_correspondent_report(m)
    assert "Rust" in output
    assert "POLYGLOT CORRESPONDENT" in output


def test_format_correspondent_report_contains_letter(tmp_path):
    path = str(tmp_path / "rotation.json")
    with open(path, "w") as f:
        json.dump({"languages": LANGS, "current_index": 2, "last_language": "Swift"}, f)

    m = generate_correspondent_report(rotate=False, config_path=path)
    output = format_correspondent_report(m)
    assert "THE LETTER" in output
    assert "Swift" in output


def test_format_correspondent_report_contains_all_facet_labels(tmp_path):
    path = str(tmp_path / "rotation.json")
    with open(path, "w") as f:
        json.dump({"languages": LANGS, "current_index": 0, "last_language": "Rust"}, f)

    m = generate_correspondent_report(rotate=False, config_path=path)
    output = format_correspondent_report(m)
    for label in ("LETTERHEAD", "ADDRESSING", "SALUTATION", "QUILL", "WAX SEAL",
                  "MARGIN NOTES", "POSTSCRIPT", "VALEDICTION", "SIGNATURE",
                  "STATIONERY", "POSTAL ROUTE", "TONE"):
        assert label in output, f"missing label {label}"


def test_format_correspondent_report_contains_cross_comparison(tmp_path):
    path = str(tmp_path / "rotation.json")
    with open(path, "w") as f:
        json.dump({"languages": LANGS, "current_index": 0, "last_language": "Rust"}, f)

    m = generate_correspondent_report(rotate=False, config_path=path)
    output = format_correspondent_report(m)
    assert "CROSS-LANGUAGE COMPARISON" in output


# ── integration: full rotation cycle ──────────────────────────────────────

def test_full_rotation_cycle_wraps(tmp_path):
    path = str(tmp_path / "rotation.json")
    with open(path, "w") as f:
        json.dump({"languages": LANGS, "current_index": 7, "last_language": "C/C++"}, f)

    m = generate_correspondent_report(rotate=True, config_path=path)
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

    for _ in range(8):
        m = generate_correspondent_report(rotate=True, config_path=path)
        seen.add(m["language"])

    assert seen == set(LANGS)


def test_each_language_has_distinct_tone_or_postal():
    """Not strictly required (some share), but verify the database carries variety."""
    tones = {record["tone"]["register"] for record in EPISTOLARY_DB.values()}
    routes = {record["postal_route"]["system"] for record in EPISTOLARY_DB.values()}
    # At least 3 different tones represented
    assert len(tones) >= 3, f"only {len(tones)} tones represented"
    # At least 2 different postal routes represented
    assert len(routes) >= 2, f"only {len(routes)} postal routes represented"


def test_no_duplicate_letter_bodies_across_languages():
    """Each language's body should be unique (sanity check)."""
    bodies = set()
    for lang in LANGS:
        letter = generate_letter(lang, seed=42)
        bodies.add(letter["body"])
    assert len(bodies) == len(LANGS), "duplicate bodies across languages"


def test_c_cpp_uses_monolithic_tone():
    record = get_epistolary("C/C++")
    assert record["tone"]["register"] == TONE_MONOLITHIC


def test_swift_uses_florid_tone():
    record = get_epistolary("Swift")
    assert record["tone"]["register"] == TONE_FLORID


def test_rust_uses_formal_tone():
    record = get_epistolary("Rust")
    assert record["tone"]["register"] == TONE_FORMAL


def test_java_uses_official_tone():
    record = get_epistolary("Java")
    assert record["tone"]["register"] == TONE_OFFICIAL
