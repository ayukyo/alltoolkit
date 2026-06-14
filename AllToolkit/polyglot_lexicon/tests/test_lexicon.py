"""Comprehensive tests for Polyglot Lexicon — Programming Languages as Dictionary Entries."""

import json
import tempfile
import os
import sys
from pathlib import Path

# Ensure AllToolkit is on path
sys.path.insert(0, "/home/admin/.openclaw/workspace/AllToolkit")

from polyglot_lexicon.src.lexicon import (
    LEXICON_DB,
    LexiconEntry,
    get_current_language,
    generate_lexicon_card,
    format_lexicon_entry,
    load_rotation,
    save_rotation,
    TOOL_NAME,
    TOOL_VERSION,
    ROTATION_ORDER,
)

LANGS = ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"]


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

def rotation_config(tmp_path):
    """Create a temporary language_rotation.json with known state."""
    config = {
        "languages": ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"],
        "current_index": 4,
        "last_language": "Kotlin",
        "updated_at": "2026-06-15T06:00:00+08:00",
    }
    path = tmp_path / "language_rotation.json"
    path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    return str(path)


# ---------------------------------------------------------------------------
# Database tests
# ---------------------------------------------------------------------------

def test_all_8_languages_in_lexicon_db():
    for lang in LANGS:
        assert lang in LEXICON_DB, f"{lang} missing from LEXICON_DB"


def test_each_language_has_required_fields():
    required = ["part_of_speech", "pronunciation", "etymology", "definition",
                "usage_notes", "synonyms", "antonyms", "related_terms",
                "cognates", "inflection", "see_also"]
    for lang in LANGS:
        for field in required:
            assert field in LEXICON_DB[lang], f"{lang} missing '{field}'"


def test_usage_notes_format():
    for lang in LANGS:
        for usage_type, note, code in LEXICON_DB[lang]["usage_notes"]:
            assert usage_type in ("statement", "expression", "declaration"), \
                f"{lang}: invalid usage_type '{usage_type}'"
            assert len(note) > 3, f"{lang}: usage note too short"
            assert len(code) > 3, f"{lang}: usage code too short"


def test_cognates_cover_all_other_languages():
    for lang in LANGS:
        cognates = LEXICON_DB[lang]["cognates"]
        for other in LANGS:
            if other != lang:
                assert other in cognates, f"{lang} missing cognate for {other}"
                cog = cognates[other]
                assert len(cog.get("term", "")) > 0, f"{lang}/{other} missing term"
                assert len(cog.get("note", "")) > 0, f"{lang}/{other} missing note"


def test_related_terms_non_empty():
    for lang in LANGS:
        for term, desc in LEXICON_DB[lang]["related_terms"]:
            assert len(term) > 0, f"{lang}: empty related term"
            assert len(desc) > 0, f"{lang}/{term}: empty description"


def test_synonyms_antonyms_count():
    for lang in LANGS:
        assert len(LEXICON_DB[lang]["synonyms"]) >= 2, f"{lang}: < 2 synonyms"
        assert len(LEXICON_DB[lang]["antonyms"]) >= 2, f"{lang}: < 2 antonyms"


def test_inflection_and_see_also():
    for lang in LANGS:
        assert len(LEXICON_DB[lang]["inflection"]) > 5, f"{lang}: no inflection"
        assert len(LEXICON_DB[lang]["see_also"]) >= 3, f"{lang}: < 3 see_also"


def test_minimum_usage_notes():
    for lang in LANGS:
        assert len(LEXICON_DB[lang]["usage_notes"]) >= 5, \
            f"{lang}: only {len(LEXICON_DB[lang]['usage_notes'])} usage notes (need >= 5)"


def test_minimum_related_terms():
    for lang in LANGS:
        assert len(LEXICON_DB[lang]["related_terms"]) >= 3, \
            f"{lang}: only {len(LEXICON_DB[lang]['related_terms'])} related terms (need >= 3)"


# ---------------------------------------------------------------------------
# LexiconEntry class
# ---------------------------------------------------------------------------

def test_lexicon_entry_to_dict():
    for lang in LANGS:
        entry = LexiconEntry(lang, LEXICON_DB[lang])
        d = entry.to_dict()
        assert d["language"] == lang
        assert "part_of_speech" in d
        assert "etymology" in d
        assert "definition" in d
        assert "usage_notes" in d


# ---------------------------------------------------------------------------
# Rotation tests
# ---------------------------------------------------------------------------

def test_rotation_order_matches_spec():
    assert ROTATION_ORDER == [
        "Rust", "Go", "Swift", "Kotlin",
        "TypeScript", "JavaScript", "Java", "C/C++",
    ]


def test_generate_lexicon_card_structure():
    result = generate_lexicon_card()
    expected_keys = ["tool", "version", "selected_language", "entry",
                     "cognate_summary", "rotation", "next_language", "timestamp"]
    for key in expected_keys:
        assert key in result, f"Missing key: {key}"


def test_tool_name_and_version():
    result = generate_lexicon_card()
    assert result["tool"] == "polyglot-lexicon"
    assert result["version"] == "1.0.0"


def test_language_override():
    for lang in LANGS:
        result = generate_lexicon_card(language=lang)
        assert result["selected_language"] == lang


def test_cognate_summary_has_7_entries():
    for lang in LANGS:
        result = generate_lexicon_card(language=lang)
        assert len(result["cognate_summary"]) == 7, \
            f"{lang}: got {len(result['cognate_summary'])} cognates, expected 7"


def test_entry_has_all_required_fields():
    result = generate_lexicon_card()
    entry = result["entry"]
    for field in ["language", "part_of_speech", "pronunciation", "etymology",
                  "definition", "usage_notes", "synonyms", "antonyms",
                  "related_terms", "cognates", "inflection", "see_also"]:
        assert field in entry, f"entry missing '{field}'"


def test_next_language_differs_from_selected():
    for lang in LANGS:
        result = generate_lexicon_card(language=lang)
        assert result["next_language"] != result["selected_language"], \
            f"{lang}: next == selected (rotation broken)"


def test_rotation_list_complete():
    result = generate_lexicon_card()
    assert len(result["rotation"]) == 8
    assert result["rotation"] == LANGS


def test_all_languages_generate_non_empty_entries():
    for lang in LANGS:
        result = generate_lexicon_card(language=lang)
        entry = result["entry"]
        assert len(entry["etymology"]) > 10
        assert len(entry["definition"]) > 10
        assert len(entry["inflection"]) > 5
        assert len(entry["see_also"]) >= 3


# ---------------------------------------------------------------------------
# Format tests
# ---------------------------------------------------------------------------

def test_format_lexicon_entry_contains_sections():
    result = generate_lexicon_card()
    card = format_lexicon_entry(result)
    for section in ["LEXICON ENTRY", "ETYMOLOGY", "DEFINITION", "USAGE NOTES",
                    "SYNONYMS", "ANTONYMS", "RELATED TERMS", "COGNATES",
                    "Inflection", "See also"]:
        assert section in card, f"Card missing section: {section}"


def test_format_card_shows_language():
    for lang in LANGS:
        result = generate_lexicon_card(language=lang)
        card = format_lexicon_entry(result)
        assert lang in card, f"Card does not show language: {lang}"


def test_format_card_is_substantial():
    result = generate_lexicon_card()
    card = format_lexicon_entry(result)
    assert len(card) > 500, "Card is suspiciously short"


# ---------------------------------------------------------------------------
# get_current_language (no rotation advance)
# ---------------------------------------------------------------------------

def test_get_current_language_returns_valid():
    current = get_current_language()
    assert current in LANGS


if __name__ == "__main__":
    print("Running Polyglot Lexicon tests via pytest...")
    import pytest
    sys.exit(pytest.main([__file__, "-v"]))