"""Tests for challenges.py."""

import pytest
import sys
sys.path.insert(0, '/home/admin/.openclaw/workspace')
from polyglot_selector.src.challenges import (
    generate_challenge,
    LANGUAGE_FEATURES,
    CHALLENGE_TYPES,
    Challenge,
)


SUPPORTED_LANGUAGES = list(LANGUAGE_FEATURES.keys())


def test_generate_challenge_returns_challenge_namedtuple():
    ch = generate_challenge("Rust", seed=42)
    assert isinstance(ch, Challenge)
    assert ch.language == "Rust"
    assert ch.challenge_type in [t[0] for t in CHALLENGE_TYPES]
    assert ch.feature in LANGUAGE_FEATURES["Rust"]


def test_generate_challenge_deterministic_with_same_seed():
    ch1 = generate_challenge("Go", seed=123)
    ch2 = generate_challenge("Go", seed=123)
    assert ch1 == ch2


def test_generate_challenge_all_languages_supported():
    for lang in SUPPORTED_LANGUAGES:
        ch = generate_challenge(lang, seed=0)
        assert ch.language == lang
        assert ch.feature in LANGUAGE_FEATURES[lang]


def test_generate_challenge_unknown_language_raises():
    with pytest.raises(ValueError, match="Unsupported language"):
        generate_challenge("Brainfuck")


def test_all_languages_have_five_features():
    for lang, features in LANGUAGE_FEATURES.items():
        assert len(features) == 5, f"{lang} should have exactly 5 features"