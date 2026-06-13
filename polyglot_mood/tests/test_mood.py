"""Comprehensive tests for Polyglot Mood."""

import json
import re
import tempfile
from pathlib import Path

import pytest

from polyglot_mood.src.mood import (
    LANGUAGE_MOODS,
    _load_rotation,
    _save_rotation,
    _compute_mood_shift,
    _compute_contrast,
    _build_transition_advice,
    get_mood_profile,
    get_consecutive_mood,
    MoodProfile,
    MoodSpectrum,
    VibeCheck,
    ROTATION_FILE,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def rotation_config(tmp_path):
    """Create a temporary language_rotation.json with known state."""
    config = {
        "languages": ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"],
        "current_index": 2,
        "last_language": "Swift",
        "updated_at": "2026-06-11T18:07:59.417272+00:00",
    }
    path = tmp_path / "language_rotation.json"
    path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    return str(path)


@pytest.fixture
def rotation_config_index0(tmp_path):
    """Create a config at index 0 (Rust)."""
    config = {
        "languages": ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"],
        "current_index": 0,
        "last_language": "Rust",
        "updated_at": "2026-06-12T00:00:00+00:00",
    }
    path = tmp_path / "language_rotation.json"
    path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    return str(path)


@pytest.fixture
def rotation_config_index7(tmp_path):
    """Create a config at index 7 (C/C++ — last position, for wrap-around test)."""
    config = {
        "languages": ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"],
        "current_index": 7,
        "last_language": "C/C++",
        "updated_at": "2026-06-12T00:00:00+00:00",
    }
    path = tmp_path / "language_rotation.json"
    path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    return str(path)


# ---------------------------------------------------------------------------
# Test MoodSpectrum structure
# ---------------------------------------------------------------------------

class TestMoodSpectrum:
    def test_spectrum_has_five_axes(self):
        for lang, data in LANGUAGE_MOODS.items():
            s = data["spectrum"]
            assert hasattr(s, "intensity"), f"{lang} missing intensity"
            assert hasattr(s, "warmth"), f"{lang} missing warmth"
            assert hasattr(s, "discipline"), f"{lang} missing discipline"
            assert hasattr(s, "creativity"), f"{lang} missing creativity"
            assert hasattr(s, "confidence"), f"{lang} missing confidence"

    def test_spectrum_values_in_range(self):
        for lang, data in LANGUAGE_MOODS.items():
            s = data["spectrum"]
            for axis in ["intensity", "warmth", "discipline", "creativity", "confidence"]:
                val = getattr(s, axis)
                assert 0.0 <= val <= 1.0, f"{lang}.{axis} = {val} out of range [0,1]"

    def test_all_eight_languages_defined(self):
        rotation_langs = ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"]
        for lang in rotation_langs:
            assert lang in LANGUAGE_MOODS, f"{lang} not in LANGUAGE_MOODS"


# ---------------------------------------------------------------------------
# Test MoodProfile structure
# ---------------------------------------------------------------------------

class TestMoodProfile:
    def test_all_profiles_have_required_fields(self):
        for lang, data in LANGUAGE_MOODS.items():
            assert "archetype" in data
            assert "tagline" in data
            assert "spectrum" in data
            assert "haiku" in data
            assert "coding_tips" in data
            assert "emotional_terrain" in data

    def test_haiku_has_three_lines(self):
        for lang, data in LANGUAGE_MOODS.items():
            lines = data["haiku"].split("\n")
            assert len(lines) == 3, f"{lang} haiku should have 3 lines, got {len(lines)}"

    def test_coding_tips_non_empty(self):
        for lang, data in LANGUAGE_MOODS.items():
            tips = data["coding_tips"]
            assert isinstance(tips, list)
            assert len(tips) >= 3, f"{lang} should have at least 3 coding tips"

    def test_archetype_unique(self):
        archetypes = [d["archetype"] for d in LANGUAGE_MOODS.values()]
        assert len(archetypes) == len(set(archetypes)), "All archetypes should be unique"


# ---------------------------------------------------------------------------
# Test _compute_mood_shift
# ---------------------------------------------------------------------------

class TestComputeMoodShift:
    def test_identical_spectra_returns_subtle(self):
        s = MoodSpectrum(intensity=0.5, warmth=0.5, discipline=0.5, creativity=0.5, confidence=0.5)
        shift = _compute_mood_shift(s, s)
        assert shift == "subtle emotional shift"

    def test_large_delta_reported(self):
        # Low discipline (chaos) to high discipline (order)
        from_s = MoodSpectrum(intensity=0.5, warmth=0.5, discipline=0.1, creativity=0.5, confidence=0.5)
        to_s   = MoodSpectrum(intensity=0.5, warmth=0.5, discipline=0.9, creativity=0.5, confidence=0.5)
        shift = _compute_mood_shift(from_s, to_s)
        assert "discipline" in shift
        assert "↑" in shift  # discipline went up

    def test_multiple_axes_detected(self):
        # Two axes with large deltas
        from_s = MoodSpectrum(intensity=0.1, warmth=0.1, discipline=0.1, creativity=0.1, confidence=0.1)
        to_s   = MoodSpectrum(intensity=0.9, warmth=0.9, discipline=0.9, creativity=0.9, confidence=0.9)
        shift = _compute_mood_shift(from_s, to_s)
        parts = shift.split(", ")
        # Should report multiple axes
        assert len(parts) >= 2


# ---------------------------------------------------------------------------
# Test _compute_contrast
# ---------------------------------------------------------------------------

class TestComputeContrast:
    def test_identical_spectra_zero(self):
        s = MoodSpectrum(intensity=0.5, warmth=0.5, discipline=0.5, creativity=0.5, confidence=0.5)
        assert _compute_contrast(s, s) == 0.0

    def test_maximum_contrast(self):
        s1 = MoodSpectrum(intensity=0.0, warmth=0.0, discipline=0.0, creativity=0.0, confidence=0.0)
        s2 = MoodSpectrum(intensity=1.0, warmth=1.0, discipline=1.0, creativity=1.0, confidence=1.0)
        contrast = _compute_contrast(s1, s2)
        assert contrast == 1.0

    def test_partial_contrast(self):
        s1 = MoodSpectrum(intensity=0.0, warmth=0.0, discipline=0.0, creativity=0.0, confidence=0.0)
        s2 = MoodSpectrum(intensity=0.5, warmth=0.5, discipline=0.5, creativity=0.5, confidence=0.5)
        contrast = _compute_contrast(s1, s2)
        assert 0.0 < contrast < 1.0
        assert abs(contrast - 0.5) < 0.01

    def test_rust_to_go_contrast(self):
        rust_s = LANGUAGE_MOODS["Rust"]["spectrum"]
        go_s   = LANGUAGE_MOODS["Go"]["spectrum"]
        contrast = _compute_contrast(rust_s, go_s)
        assert 0.0 < contrast < 1.0


# ---------------------------------------------------------------------------
# Test _build_transition_advice
# ---------------------------------------------------------------------------

class TestBuildTransitionAdvice:
    def test_low_contrast_gentle_advice(self):
        advice = _build_transition_advice("Rust", "Go", 0.10)
        assert "gentle" in advice.lower() or "similar" in advice.lower()

    def test_medium_contrast_embrace(self):
        advice = _build_transition_advice("JavaScript", "TypeScript", 0.25)
        assert len(advice) > 0

    def test_high_contrast_permission(self):
        advice = _build_transition_advice("JavaScript", "C/C++", 0.40)
        assert "permission" in advice.lower() or "beginner" in advice.lower()


# ---------------------------------------------------------------------------
# Test get_mood_profile (no rotation)
# ---------------------------------------------------------------------------

class TestGetMoodProfileNoRotate:
    def test_returns_correct_profile(self):
        profile = get_mood_profile("Rust", rotate=False)
        assert isinstance(profile, MoodProfile)
        assert profile.language == "Rust"
        assert profile.archetype == "The Perfectionist"

    def test_profile_fields_all_present(self):
        profile = get_mood_profile("Go", rotate=False)
        assert profile.tagline
        assert isinstance(profile.spectrum, MoodSpectrum)
        assert isinstance(profile.haiku, str)
        assert isinstance(profile.coding_tips, list)
        assert isinstance(profile.emotional_terrain, str)

    def test_unknown_language_raises(self):
        with pytest.raises(ValueError, match="Unknown language"):
            get_mood_profile("Python", rotate=False)

    def test_spectrum_values_valid(self):
        for lang in LANGUAGE_MOODS:
            profile = get_mood_profile(lang, rotate=False)
            s = profile.spectrum
            for axis in ["intensity", "warmth", "discipline", "creativity", "confidence"]:
                assert 0.0 <= getattr(s, axis) <= 1.0

    def test_haiku_three_lines(self):
        profile = get_mood_profile("Swift", rotate=False)
        lines = [l for l in profile.haiku.split("\n") if l.strip()]
        assert len(lines) == 3


# ---------------------------------------------------------------------------
# Test get_mood_profile (with rotation)
# ---------------------------------------------------------------------------

class TestGetMoodProfileWithRotate:
    def test_rotate_updates_config(self, rotation_config, monkeypatch):
        monkeypatch.setattr("polyglot_mood.src.mood.ROTATION_FILE", rotation_config)
        profile = get_mood_profile("Swift", rotate=True)
        assert profile.language == "Swift"
        with open(rotation_config, "r", encoding="utf-8") as f:
            data = json.load(f)
        # Should advance from index 2 (Swift) to index 3 (Kotlin)
        assert data["current_index"] == 3
        assert data["last_language"] == "Swift"

    def test_rotate_twice(self, rotation_config, monkeypatch):
        monkeypatch.setattr("polyglot_mood.src.mood.ROTATION_FILE", rotation_config)
        p1 = get_mood_profile("Swift", rotate=True)
        p2 = get_mood_profile("Kotlin", rotate=True)
        assert p1.language == "Swift"
        assert p2.language == "Kotlin"
        with open(rotation_config, "r", encoding="utf-8") as f:
            data = json.load(f)
        assert data["current_index"] == 4  # Kotlin → Kotlin index + 1

    def test_rotate_updates_timestamp(self, rotation_config, monkeypatch):
        monkeypatch.setattr("polyglot_mood.src.mood.ROTATION_FILE", rotation_config)
        get_mood_profile("Swift", rotate=True)
        with open(rotation_config, "r", encoding="utf-8") as f:
            data = json.load(f)
        assert "updated_at" in data


# ---------------------------------------------------------------------------
# Test get_consecutive_mood (no rotation)
# ---------------------------------------------------------------------------

class TestGetConsecutiveMoodNoRotate:
    def test_returns_pair(self, rotation_config, monkeypatch):
        monkeypatch.setattr("polyglot_mood.src.mood.ROTATION_FILE", rotation_config)
        current_mood, vibe_check = get_consecutive_mood(rotate=False)
        assert current_mood.language == "Swift"  # index 2
        assert vibe_check is None

    def test_returns_correct_next_pair(self, rotation_config_index0, monkeypatch):
        monkeypatch.setattr("polyglot_mood.src.mood.ROTATION_FILE", rotation_config_index0)
        current_mood, vibe_check = get_consecutive_mood(rotate=False)
        assert current_mood.language == "Rust"  # index 0
        assert vibe_check is None


# ---------------------------------------------------------------------------
# Test get_consecutive_mood (with rotation)
# ---------------------------------------------------------------------------

class TestGetConsecutiveMoodWithRotate:
    def test_returns_vibe_check(self, rotation_config, monkeypatch):
        monkeypatch.setattr("polyglot_mood.src.mood.ROTATION_FILE", rotation_config)
        current_mood, vibe_check = get_consecutive_mood(rotate=True)
        assert isinstance(vibe_check, VibeCheck)
        assert vibe_check.from_language == "Swift"
        assert vibe_check.to_language == "Kotlin"
        assert vibe_check.mood_shift
        assert 0.0 <= vibe_check.contrast_score <= 1.0
        assert vibe_check.advice

    def test_rotation_advances(self, rotation_config, monkeypatch):
        monkeypatch.setattr("polyglot_mood.src.mood.ROTATION_FILE", rotation_config)
        current_mood, vibe_check = get_consecutive_mood(rotate=True)
        with open(rotation_config, "r", encoding="utf-8") as f:
            data = json.load(f)
        assert data["current_index"] == 3  # Swift (2) → Kotlin (3)

    def test_wrap_around(self, rotation_config_index7, monkeypatch):
        monkeypatch.setattr("polyglot_mood.src.mood.ROTATION_FILE", rotation_config_index7)
        current_mood, vibe_check = get_consecutive_mood(rotate=True)
        assert current_mood.language == "C/C++"  # index 7
        assert vibe_check.to_language == "Rust"    # wraps to Rust
        with open(rotation_config_index7, "r", encoding="utf-8") as f:
            data = json.load(f)
        assert data["current_index"] == 0  # wrapped

    def test_vibe_check_contrast_in_range(self, rotation_config, monkeypatch):
        monkeypatch.setattr("polyglot_mood.src.mood.ROTATION_FILE", rotation_config)
        _, vibe_check = get_consecutive_mood(rotate=True)
        assert 0.0 <= vibe_check.contrast_score <= 1.0

    def test_mood_shift_contains_axis(self, rotation_config, monkeypatch):
        monkeypatch.setattr("polyglot_mood.src.mood.ROTATION_FILE", rotation_config)
        _, vibe_check = get_consecutive_mood(rotate=True)
        shift = vibe_check.mood_shift
        assert shift is not None
        assert len(shift) > 0


# ---------------------------------------------------------------------------
# Integration tests
# ---------------------------------------------------------------------------

class TestIntegration:
    def test_all_consecutive_pairs_have_vibe_checks(self, rotation_config_index0, monkeypatch):
        monkeypatch.setattr("polyglot_mood.src.mood.ROTATION_FILE", rotation_config_index0)
        languages = ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"]
        for lang in languages:
            current, vibe = get_consecutive_mood(rotate=True)
            assert current.language == lang
            assert vibe is not None
            assert vibe.from_language == lang
            assert vibe.to_language in languages

    def test_full_cycle_wrapped(self, rotation_config_index0, monkeypatch):
        monkeypatch.setattr("polyglot_mood.src.mood.ROTATION_FILE", rotation_config_index0)
        sequence = []
        for _ in range(8):
            current, _ = get_consecutive_mood(rotate=True)
            sequence.append(current.language)
        assert sequence == ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"]
        # 9th call should wrap back to Rust
        current, _ = get_consecutive_mood(rotate=True)
        assert current.language == "Rust"

    def test_spectrum_axes_unique_across_languages(self):
        """No two languages should have identical spectra."""
        seen = {}
        for lang, data in LANGUAGE_MOODS.items():
            s = data["spectrum"]
            key = tuple(sorted([
                (ax, getattr(s, ax)) for ax in ["intensity", "warmth", "discipline", "creativity", "confidence"]
            ]))
            assert key not in seen, f"Spectrum collision: {lang} matches {seen[key]}"
            seen[key] = lang

    def test_contrast_symmetry(self):
        """Contrast between A→B should equal B→A."""
        rust_s = LANGUAGE_MOODS["Rust"]["spectrum"]
        go_s   = LANGUAGE_MOODS["Go"]["spectrum"]
        ab = _compute_contrast(rust_s, go_s)
        ba = _compute_contrast(go_s, rust_s)
        assert abs(ab - ba) < 0.001

    def test_haiku_contains_language_keywords(self):
        """Haikus should contain subtle language-specific references."""
        haikus = {lang: data["haiku"] for lang, data in LANGUAGE_MOODS.items()}
        assert "borrow" in haikus["Rust"].lower() or "ownership" in haikus["Rust"].lower() or "memory" in haikus["Rust"].lower()
        assert "goroutine" in haikus["Go"].lower() or "channel" in haikus["Go"].lower() or "concurrency" in haikus["Go"].lower()
        assert "optional" in haikus["Swift"].lower() or "safety" in haikus["Swift"].lower() or "swift" in haikus["Swift"].lower()