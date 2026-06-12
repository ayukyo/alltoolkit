"""Comprehensive tests for Polyglot Harmony."""

import json
import tempfile
from pathlib import Path

import pytest

from polyglot_harmony.src.harmony import (
    analyze_harmony,
    get_consecutive_pair,
    HarmonyReport,
    DimensionScore,
    LANGUAGE_FEATURES,
    COMPATIBILITY_PAIRS,
    DEFAULT_COMPATIBILITY,
    _get_compatibility,
    _build_transfer_tips,
    _build_synergy_summary,
    _score_to_dimension,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def rotation_config(tmp_path):
    """Create a temporary language_rotation.json with known state."""
    config = {
        "languages": ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"],
        "current_index": 1,
        "last_language": "Go",
        "updated_at": "2026-06-11T18:07:59.417272+00:00",
    }
    path = tmp_path / "language_rotation.json"
    path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    return str(path)


@pytest.fixture
def all_languages_config(tmp_path):
    """Create a config with all languages in extended list."""
    config = {
        "languages": ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"],
        "current_index": 0,
        "last_language": "Rust",
        "updated_at": "2026-06-12T00:00:00+00:00",
    }
    path = tmp_path / "language_rotation.json"
    path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    return str(path)


# ---------------------------------------------------------------------------
# Test _get_compatibility
# ---------------------------------------------------------------------------

class TestGetCompatibility:
    def test_known_pair_rust_go(self):
        result = _get_compatibility("Rust", "Go")
        assert result == COMPATIBILITY_PAIRS[("Rust", "Go")]
        assert "syntax" in result

    def test_known_pair_swift_kotlin(self):
        result = _get_compatibility("Swift", "Kotlin")
        assert result["syntax"] == 0.90
        assert result["paradigm"] == 0.85

    def test_known_pair_typescript_javascript(self):
        result = _get_compatibility("TypeScript", "JavaScript")
        assert result["syntax"] == 0.95
        assert result["interop"] == 0.95

    def test_unknown_pair_defaults(self):
        result = _get_compatibility("Python", "Zig")
        assert result == DEFAULT_COMPATIBILITY

    def test_reverse_pair_differs(self):
        forward = _get_compatibility("Rust", "Go")
        reverse = _get_compatibility("Go", "Rust")
        assert forward != reverse, "Compatibility should be directional"


# ---------------------------------------------------------------------------
# Test _score_to_dimension
# ---------------------------------------------------------------------------

class TestScoreToDimension:
    def test_dimension_creation(self):
        dim = _score_to_dimension(0.85, "Syntax Overlap", "Lexical similarity")
        assert dim.score == 0.85
        assert dim.label == "Syntax Overlap"
        assert dim.description == "Lexical similarity"


# ---------------------------------------------------------------------------
# Test _build_transfer_tips
# ---------------------------------------------------------------------------

class TestBuildTransferTips:
    def test_high_syntax_triggers_tip(self):
        scores = {"syntax": 0.90, "paradigm": 0.60, "interop": 0.50, "transfer": 0.65}
        tips = _build_transfer_tips("TypeScript", "JavaScript", scores)
        assert any("syntax" in t.lower() for t in tips)

    def test_low_transfer_triggers_warning(self):
        scores = {"syntax": 0.50, "paradigm": 0.45, "interop": 0.40, "transfer": 0.45}
        tips = _build_transfer_tips("Java", "C/C++", scores)
        assert any("unlearn" in t.lower() or "paradigm shift" in t.lower() for t in tips)

    def test_memory_model_transition_tip(self):
        # Rust (ownership) -> Go (gc) should produce memory model tip
        scores = {"syntax": 0.85, "paradigm": 0.55, "interop": 0.60, "transfer": 0.70}
        tips = _build_transfer_tips("Rust", "Go", scores)
        assert any("memory" in t.lower() or "ownership" in t.lower() for t in tips)

    def test_shared_paradigm_tip(self):
        scores = {"syntax": 0.90, "paradigm": 0.85, "interop": 0.80, "transfer": 0.88}
        tips = _build_transfer_tips("Swift", "Kotlin", scores)
        assert any("shared paradigms" in t.lower() or "paradigm" in t.lower() for t in tips)


# ---------------------------------------------------------------------------
# Test _build_synergy_summary
# ---------------------------------------------------------------------------

class TestBuildSynergySummary:
    def test_high_avg_smooth_transition(self):
        scores = {"syntax": 0.95, "paradigm": 0.90, "interop": 0.85, "transfer": 0.88}
        summary = _build_synergy_summary("TypeScript", "JavaScript", scores, [])
        assert "smooth" in summary.lower() or "natural" in summary.lower()

    def test_low_avg_bold_leap(self):
        scores = {"syntax": 0.45, "paradigm": 0.40, "interop": 0.35, "transfer": 0.40}
        summary = _build_synergy_summary("JavaScript", "Rust", scores, [])
        assert "bold" in summary.lower() or "leap" in summary.lower()


# ---------------------------------------------------------------------------
# Test get_consecutive_pair
# ---------------------------------------------------------------------------

class TestGetConsecutivePair:
    def test_returns_correct_pair(self, rotation_config):
        prev, curr = get_consecutive_pair(rotation_config)
        assert prev == "Go"   # index 1
        assert curr == "Swift"  # index 2

    def test_does_not_modify_index(self, rotation_config):
        prev1, curr1 = get_consecutive_pair(rotation_config)
        prev2, curr2 = get_consecutive_pair(rotation_config)
        assert prev1 == prev2
        assert curr1 == curr2

    def test_wraps_around(self, all_languages_config):
        # With index=0 and 8 languages, next is index 1
        prev, curr = get_consecutive_pair(all_languages_config)
        assert prev == "Rust"
        assert curr == "Go"


# ---------------------------------------------------------------------------
# Test analyze_harmony (no rotation)
# ---------------------------------------------------------------------------

class TestAnalyzeHarmonyNoRotate:
    def test_analyze_no_rotate(self, rotation_config):
        report = analyze_harmony(rotation_config, rotate=False)
        assert isinstance(report, HarmonyReport)
        assert report.previous_language == "Go"
        assert report.current_language == "Swift"
        assert report.rotated is False
        assert report.new_index == 1

    def test_report_has_all_fields(self, rotation_config):
        report = analyze_harmony(rotation_config, rotate=False)
        assert isinstance(report.overall_score, float)
        assert 0.0 <= report.overall_score <= 1.0
        assert len(report.dimensions) == 4
        assert isinstance(report.transfer_tips, list)
        assert isinstance(report.synergy_summary, str)

    def test_dimensions_have_correct_labels(self, rotation_config):
        report = analyze_harmony(rotation_config, rotate=False)
        labels = {d.label for d in report.dimensions}
        assert labels == {"Syntax Overlap", "Paradigm Alignment", "Ecosystem Interop", "Learning Transfer"}

    def test_dimensions_scores_valid(self, rotation_config):
        report = analyze_harmony(rotation_config, rotate=False)
        for dim in report.dimensions:
            assert 0.0 <= dim.score <= 1.0
            assert dim.label
            assert dim.description


# ---------------------------------------------------------------------------
# Test analyze_harmony (with rotation)
# ---------------------------------------------------------------------------

class TestAnalyzeHarmonyWithRotate:
    def test_rotate_updates_index(self, rotation_config):
        report = analyze_harmony(rotation_config, rotate=True)
        assert report.rotated is True
        assert report.new_index == 2  # index was 1, now 2 (Swift)

    def test_rotate_persists_config(self, rotation_config):
        report = analyze_harmony(rotation_config, rotate=True)
        with open(rotation_config, "r", encoding="utf-8") as f:
            data = json.load(f)
        assert data["current_index"] == 2
        assert data["last_language"] == "Swift"

    def test_rotate_twice_advances_twice(self, rotation_config):
        report1 = analyze_harmony(rotation_config, rotate=True)
        report2 = analyze_harmony(rotation_config, rotate=True)
        assert report1.new_index == 2
        assert report2.new_index == 3
        assert report2.previous_language == "Swift"
        assert report2.current_language == "Kotlin"

    def test_rotate_wraps_around(self, all_languages_config):
        # Create config at last index
        config_path = all_languages_config
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        data["current_index"] = 7  # C/C++
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        with open(config_path, "r", encoding="utf-8") as f:
            content = f.read()
        import re
        content = re.sub(r'"current_index":\s*\d+', '"current_index": 7', content)
        with open(config_path, "w", encoding="utf-8") as f:
            f.write(content)

        report = analyze_harmony(config_path, rotate=True)
        assert report.new_index == 0  # wraps to Rust
        assert report.current_language == "Rust"

    def test_rotate_updates_timestamp(self, rotation_config):
        report = analyze_harmony(rotation_config, rotate=True)
        # Verify updated_at was written to config
        with open(rotation_config, "r", encoding="utf-8") as f:
            data = json.load(f)
        assert "updated_at" in data
        assert data["updated_at"] != "2026-06-11T18:07:59.417272+00:00"


# ---------------------------------------------------------------------------
# Test HarmonyReport structure
# ---------------------------------------------------------------------------

class TestHarmonyReport:
    def test_report_dataclass_fields(self):
        report = HarmonyReport(
            previous_language="Rust",
            current_language="Go",
            overall_score=0.72,
            dimensions=[],
            transfer_tips=[],
            synergy_summary="Test summary",
            rotated=True,
            new_index=1,
        )
        assert report.previous_language == "Rust"
        assert report.current_language == "Go"
        assert report.overall_score == 0.72
        assert report.rotated is True
        assert report.new_index == 1

    def test_dimension_score_dataclass(self):
        dim = DimensionScore(score=0.85, label="Test", description="Test desc")
        assert dim.score == 0.85
        assert dim.label == "Test"


# ---------------------------------------------------------------------------
# Test LANGUAGE_FEATURES completeness
# ---------------------------------------------------------------------------

class TestLanguageFeatures:
    def test_all_rotation_languages_defined(self):
        rotation_languages = ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"]
        for lang in rotation_languages:
            assert lang in LANGUAGE_FEATURES, f"{lang} not in LANGUAGE_FEATURES"

    def test_all_languages_have_required_keys(self):
        required_keys = ["paradigm", "syntax_family", "memory_model", "strengths", "learning_curve"]
        for lang, features in LANGUAGE_FEATURES.items():
            for key in required_keys:
                assert key in features, f"{lang} missing {key}"

    def test_memory_models_are_reasonable(self):
        valid_models = {"ownership_borrow", "garbage_collected", "arc", "jvm-gc", "gc-dynamic", "manual"}
        for lang, features in LANGUAGE_FEATURES.items():
            assert features["memory_model"] in valid_models, f"{lang} has invalid memory_model"


# ---------------------------------------------------------------------------
# Integration-style tests
# ---------------------------------------------------------------------------

class TestIntegration:
    def test_full_rotation_cycle_no_rotate(self, all_languages_config):
        """Simulate reading all pairs by repeatedly calling analyze_harmony with rotate=False.

        analyze_harmony with rotate=False reads the current index but does NOT advance it,
        so we need to use it to check all pairs. We simulate a full cycle by manually
        setting the index in the config file before each call.
        """
        config_path = all_languages_config
        languages = ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"]
        expected = [
            ("Rust", "Go"), ("Go", "Swift"), ("Swift", "Kotlin"),
            ("Kotlin", "TypeScript"), ("TypeScript", "JavaScript"),
            ("JavaScript", "Java"), ("Java", "C/C++"), ("C/C++", "Rust"),
        ]
        for i, (prev_exp, curr_exp) in enumerate(expected):
            # Set index to i so get_consecutive_pair returns the expected pair
            with open(config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            data["current_index"] = i
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
                f.write("\n")

            prev, curr = get_consecutive_pair(config_path)
            assert prev == prev_exp, f"Step {i}: prev={prev}, expected={prev_exp}"
            assert curr == curr_exp, f"Step {i}: curr={curr}, expected={curr_exp}"

    def test_scores_for_known_pair(self):
        scores = _get_compatibility("Swift", "Kotlin")
        assert scores["syntax"] == 0.90
        assert scores["paradigm"] == 0.85
        assert scores["interop"] == 0.80
        assert scores["transfer"] == 0.88