#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for polyglot_pulse module.
"""

import json
import os
import sys
import pytest
from pathlib import Path

# Build correct path to module
POLYGLOT_ROOT = Path(__file__).parent.parent.parent
ROTATION_FILE = str(POLYGLOT_ROOT / "language_rotation.json")

# Patch ROTATION_FILE before importing
import polyglot_pulse
polyglot_pulse.ROTATION_FILE = ROTATION_FILE

from polyglot_pulse import (
    TOOL_NAME,
    TOOL_VERSION,
    LANGUAGE_METRICS,
    calculate_pulse_score,
    get_vital_signs,
    assess_health_conditions,
    generate_diagnosis,
    measure_pulse,
    load_rotation,
)


ROTATION_ORDER = ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"]


class TestModuleMetadata:
    """Test module constants."""

    def test_tool_name(self):
        assert TOOL_NAME == "polyglot-pulse"

    def test_tool_version(self):
        assert TOOL_VERSION == "1.0.0"


class TestLanguageMetrics:
    """Test LANGUAGE_METRICS data."""

    def test_all_8_languages_have_metrics(self):
        for lang in ROTATION_ORDER:
            assert lang in LANGUAGE_METRICS, f"{lang} missing metrics"

    def test_each_language_has_all_required_metrics(self):
        required = {"energy", "memory_integrity", "concurrency_pulse",
                    "type_safety", "learning_curve", "community_growth"}
        for lang, metrics in LANGUAGE_METRICS.items():
            assert required.issubset(metrics.keys()), f"{lang} missing metrics"

    def test_metric_values_in_range(self):
        for lang, metrics in LANGUAGE_METRICS.items():
            for key, value in metrics.items():
                assert 0 <= value <= 100, f"{lang}.{key}={value} out of range"


class TestCalculatePulseScore:
    """Test calculate_pulse_score function."""

    def test_returns_float(self):
        result = calculate_pulse_score(LANGUAGE_METRICS["Rust"])
        assert isinstance(result, (int, float))

    def test_rust_has_high_score(self):
        score = calculate_pulse_score(LANGUAGE_METRICS["Rust"])
        assert score >= 80

    def test_js_has_high_energy_but_low_memory(self):
        metrics = LANGUAGE_METRICS["JavaScript"]
        assert metrics["energy"] >= 90
        assert metrics["memory_integrity"] < 80

    def test_score_respects_weights(self):
        # Pure 100s should give 100
        all_100 = {k: 100 for k in LANGUAGE_METRICS["Rust"].keys()}
        score = calculate_pulse_score(all_100)
        assert score == 100.0

    def test_score_with_zeros(self):
        all_0 = {k: 0 for k in LANGUAGE_METRICS["Rust"].keys()}
        score = calculate_pulse_score(all_0)
        assert score == 0.0


class TestGetVitalSigns:
    """Test get_vital_signs function."""

    def test_returns_dict(self):
        result = get_vital_signs("Rust")
        assert isinstance(result, dict)

    def test_returns_all_required_keys(self):
        result = get_vital_signs("Rust")
        expected = ["energy", "memory_integrity", "concurrency_pulse",
                    "type_safety", "learning_curve", "community_growth"]
        for key in expected:
            assert key in result

    def test_values_in_valid_range(self):
        for lang in ROTATION_ORDER:
            vitals = get_vital_signs(lang)
            for key, value in vitals.items():
                assert 1 <= value <= 100, f"{lang}.{key}={value}"

    def test_deterministic_for_same_language(self):
        # Same language should give same base values
        v1 = get_vital_signs("Rust")
        v2 = get_vital_signs("Rust")
        assert v1.keys() == v2.keys()


class TestAssessHealthConditions:
    """Test assess_health_conditions function."""

    def test_returns_list(self):
        conditions = assess_health_conditions(LANGUAGE_METRICS["Rust"])
        assert isinstance(conditions, list)

    def test_rust_gets_ironclad_memory(self):
        conditions = assess_health_conditions(LANGUAGE_METRICS["Rust"])
        assert "🛡️ Ironclad Memory" in conditions

    def test_cpp_gets_loose_types(self):
        # C/C++ has type_safety=60, which is < 70
        conditions = assess_health_conditions(LANGUAGE_METRICS["C/C++"])
        assert "🤷 Loose Types" in conditions

    def test_empty_conditions_for_balanced_language(self):
        balanced = {k: 75 for k in LANGUAGE_METRICS["Rust"].keys()}
        conditions = assess_health_conditions(balanced)
        assert isinstance(conditions, list)


class TestGenerateDiagnosis:
    """Test generate_diagnosis function."""

    def test_returns_string(self):
        diag = generate_diagnosis("Rust", 90)
        assert isinstance(diag, str)

    def test_high_score_peak_condition(self):
        diag = generate_diagnosis("Rust", 95)
        assert "🌟" in diag or "peak" in diag.lower()

    def test_low_score_needs_attention(self):
        diag = generate_diagnosis("C/C++", 60)
        assert isinstance(diag, str)
        assert len(diag) > 0


class TestMeasurePulse:
    """Test measure_pulse function."""

    def test_returns_dict(self):
        result = measure_pulse("Rust")
        assert isinstance(result, dict)

    def test_returns_language(self):
        result = measure_pulse("Rust")
        assert result["language"] == "Rust"

    def test_returns_vital_signs(self):
        result = measure_pulse("Go")
        assert "vital_signs" in result
        assert isinstance(result["vital_signs"], dict)

    def test_returns_pulse_score(self):
        result = measure_pulse("Swift")
        assert "pulse_score" in result
        assert 0 <= result["pulse_score"] <= 100

    def test_returns_diagnosis(self):
        result = measure_pulse("Kotlin")
        assert "diagnosis" in result
        assert isinstance(result["diagnosis"], str)

    def test_returns_health_conditions(self):
        result = measure_pulse("TypeScript")
        assert "health_conditions" in result
        assert isinstance(result["health_conditions"], list)

    def test_returns_next_language(self):
        result = measure_pulse("Rust")
        assert "next_language" in result
        assert result["next_language"] == "Go"

    def test_returns_rotation_position(self):
        result = measure_pulse("Java")
        assert "rotation_position" in result
        assert isinstance(result["rotation_position"], int)

    def test_returns_timestamp(self):
        result = measure_pulse("JavaScript")
        assert "timestamp" in result

    def test_invalid_language_raises_value_error(self):
        with pytest.raises(ValueError) as excinfo:
            measure_pulse("Python")
        assert "Python" in str(excinfo.value)

    def test_updates_rotation_state(self):
        config_before = load_rotation()
        idx_before = config_before["current_index"]
        lang_before = config_before["languages"][idx_before]
        measure_pulse(lang_before)
        config_after = load_rotation()
        expected = (idx_before + 1) % len(config_before["languages"])
        assert config_after["current_index"] == expected


class TestRotationIntegrity:
    """Test rotation file integrity."""

    def test_rotation_file_exists(self):
        assert os.path.exists(ROTATION_FILE)

    def test_rotation_has_8_languages(self):
        config = load_rotation()
        assert len(config["languages"]) == 8

    def test_rust_is_first(self):
        config = load_rotation()
        assert config["languages"][0] == "Rust"

    def test_cpp_is_last(self):
        config = load_rotation()
        assert config["languages"][-1] == "C/C++"
