"""Tests for forge.py — rotation logic and alloy generation."""

import json
import tempfile
import os
import sys
sys.path.insert(0, '/home/admin/.openclaw/workspace/AllToolkit')
from polyglot_forge.src.forge import (
    METAL_PROPERTIES,
    COMPATIBILITY_MATRIX,
    FORGE_PROCESS,
    get_tier,
    compute_alloy_strength,
    select_pairing_languages,
    forge_alloy,
    advance_rotation,
    get_current_language,
    generate_forge_card,
    format_alloy_card,
    AlloyCard,
)

LANGS = ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"]


# ── config tests ─────────────────────────────────────────────────────────────

def test_all_eight_languages_have_metal_properties():
    for lang in LANGS:
        assert lang in METAL_PROPERTIES, f"{lang} missing from METAL_PROPERTIES"


def test_compatibility_matrix_has_all_languages():
    for lang in LANGS:
        assert lang in COMPATIBILITY_MATRIX
        for other in LANGS:
            if other != lang:
                assert other in COMPATIBILITY_MATRIX[lang], f"{lang} → {other} missing"


def test_get_tier_boundaries():
    assert get_tier(1.0) == "legendary"
    assert get_tier(0.85) == "legendary"
    assert get_tier(0.84) == "excellent"
    assert get_tier(0.75) == "excellent"
    assert get_tier(0.74) == "good"
    assert get_tier(0.60) == "good"
    assert get_tier(0.59) == "challenging"
    assert get_tier(0.0) == "challenging"


def test_compute_alloy_strength_returns_float():
    rust = METAL_PROPERTIES["Rust"]
    c = METAL_PROPERTIES["C/C++"]
    score = compute_alloy_strength(rust, c, 0.85)
    assert isinstance(score, float)
    assert 0.0 <= score <= 10.0


def test_compute_alloy_strength_higher_with_high_compatibility():
    rust = METAL_PROPERTIES["Rust"]
    go = METAL_PROPERTIES["Go"]
    low = compute_alloy_strength(rust, go, 0.40)
    high = compute_alloy_strength(rust, go, 0.90)
    assert high > low


def test_select_pairing_languages_never_returns_primary():
    primary = "Rust"
    secondary = select_pairing_languages(primary, LANGS, seed=42)
    assert secondary != primary
    assert secondary in LANGS


def test_select_pairing_languages_deterministic_with_seed():
    langs = ["A", "B", "C", "D"]
    r1 = select_pairing_languages("A", langs, seed=999)
    r2 = select_pairing_languages("A", langs, seed=999)
    assert r1 == r2


def test_forge_alloy_returns_alloy_card():
    card = forge_alloy("Rust", "C/C++", seed=42)
    assert isinstance(card, AlloyCard)
    assert card.primary_language == "Rust"
    assert card.secondary_language == "C/C++"
    assert card.tier in ("legendary", "excellent", "good", "challenging")
    assert 0.0 <= card.compatibility_score <= 1.0
    assert 0.0 <= card.alloy_strength <= 10.0


def test_forge_alloy_rust_cpp_is_legendary():
    card = forge_alloy("Rust", "C/C++", seed=42)
    assert card.tier == "legendary"
    assert card.compatibility_score == 0.85


def test_forge_alloy_deterministic_with_seed():
    c1 = forge_alloy("Kotlin", "Java", seed=12345)
    c2 = forge_alloy("Kotlin", "Java", seed=12345)
    assert c1 == c2


def test_format_alloy_card_contains_language_names():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump({"languages": LANGS, "current_index": 3, "last_language": "Kotlin"}, f)
        path = f.name
    try:
        result = generate_forge_card(path, seed=0)
        card = format_alloy_card(result)
        assert result["current_language"] in card
        assert result["pairing_language"] in card
    finally:
        os.unlink(path)
