#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for polyglot_anomaly module.
"""

import json
import os
import sys
import tempfile
import pytest
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from anomaly import (
    TOOL_NAME,
    TOOL_VERSION,
    ANOMALY_DATA,
    ROTATION_ORDER,
    load_rotation,
    save_rotation,
    get_current_language,
    advance_rotation,
    detect_anomalies,
    format_anomaly_report,
)


ROTATION_FILE = str(Path(__file__).parent.parent.parent / "language_rotation.json")


class TestModuleMetadata:
    """Test module constants."""

    def test_tool_name(self):
        assert TOOL_NAME == "polyglot-anomaly"

    def test_tool_version(self):
        assert TOOL_VERSION == "1.0.0"


class TestAnomalyData:
    """Test ANOMALY_DATA structure."""

    def test_all_8_languages_have_data(self):
        for lang in ROTATION_ORDER:
            assert lang in ANOMALY_DATA, f"{lang} missing from ANOMALY_DATA"

    def test_each_language_has_required_keys(self):
        for lang, data in ANOMALY_DATA.items():
            assert "emoji" in data
            assert "anomalies" in data
            assert "paradoxes" in data
            assert "delightful_contradictions" in data

    def test_each_anomaly_has_required_fields(self):
        for lang, data in ANOMALY_DATA.items():
            for anomaly in data["anomalies"]:
                assert "id" in anomaly
                assert "name" in anomaly
                assert "severity" in anomaly
                assert "description" in anomaly
                assert "paradox" in anomaly
                assert "workaround" in anomaly
                assert "example_code" in anomaly

    def test_anomaly_severity_values(self):
        valid_severities = {"critical", "high", "medium", "low"}
        for lang, data in ANOMALY_DATA.items():
            for anomaly in data["anomalies"]:
                assert anomaly["severity"] in valid_severities, \
                    f"{lang}/{anomaly['id']} has invalid severity: {anomaly['severity']}"

    def test_each_paradox_has_required_fields(self):
        for lang, data in ANOMALY_DATA.items():
            for paradox in data["paradoxes"]:
                assert "quote" in paradox
                assert "explanation" in paradox

    def test_delightful_contradictions_are_strings(self):
        for lang, data in ANOMALY_DATA.items():
            for contradiction in data["delightful_contradictions"]:
                assert isinstance(contradiction, str)


class TestRotationFunctions:
    """Test rotation load/save functions."""

    def test_load_rotation_returns_dict(self):
        config = load_rotation()
        assert isinstance(config, dict)

    def test_rotation_has_languages_list(self):
        config = load_rotation()
        assert "languages" in config
        assert isinstance(config["languages"], list)
        assert len(config["languages"]) == 8

    def test_rotation_has_current_index(self):
        config = load_rotation()
        assert "current_index" in config
        assert isinstance(config["current_index"], int)

    def test_rust_is_first_language(self):
        config = load_rotation()
        assert config["languages"][0] == "Rust"


class TestGetCurrentLanguage:
    """Test get_current_language function."""

    def test_returns_language_from_rotation(self):
        lang = get_current_language()
        assert lang in ROTATION_ORDER


class TestAdvanceRotation:
    """Test advance_rotation function."""

    def test_returns_current_language(self):
        config_before = load_rotation()
        idx_before = config_before["current_index"]
        lang = advance_rotation()
        assert lang == config_before["languages"][idx_before]

    def test_advances_current_index(self):
        config_before = load_rotation()
        idx_before = config_before["current_index"]
        advance_rotation()
        config_after = load_rotation()
        expected = (idx_before + 1) % len(config_before["languages"])
        assert config_after["current_index"] == expected

    def test_sets_last_language(self):
        config_before = load_rotation()
        idx_before = config_before["current_index"]
        lang = advance_rotation()
        config_after = load_rotation()
        assert config_after.get("last_language") == lang


class TestDetectAnomalies:
    """Test detect_anomalies function."""

    def test_detects_anomalies_for_specific_language(self):
        result = detect_anomalies("Rust")
        assert result["language"] == "Rust"
        assert "anomaly_count" in result
        assert "anomalies" in result
        assert result["anomaly_count"] == len(result["anomalies"])

    def test_detects_anomalies_returns_severity_breakdown(self):
        result = detect_anomalies("Rust")
        assert "severity_breakdown" in result
        assert isinstance(result["severity_breakdown"], dict)
        assert "critical" in result["severity_breakdown"]
        assert "high" in result["severity_breakdown"]
        assert "medium" in result["severity_breakdown"]
        assert "low" in result["severity_breakdown"]

    def test_detects_anomalies_returns_paradoxes(self):
        result = detect_anomalies("Go")
        assert "paradoxes" in result
        assert isinstance(result["paradoxes"], list)

    def test_detects_anomalies_returns_delightful_contradictions(self):
        result = detect_anomalies("Swift")
        assert "delightful_contradictions" in result
        assert isinstance(result["delightful_contradictions"], list)

    def test_detects_anomalies_returns_next_language(self):
        result = detect_anomalies("Kotlin")
        assert "next_language" in result
        assert result["next_language"] in ROTATION_ORDER

    def test_detects_anomalies_with_language_override_does_not_advance_rotation(self):
        config_before = load_rotation()
        idx_before = config_before["current_index"]
        detect_anomalies("Rust")
        config_after = load_rotation()
        assert config_after["current_index"] == idx_before

    def test_unknown_language_raises_value_error(self):
        with pytest.raises(ValueError) as excinfo:
            detect_anomalies("Brainfuck")
        assert "Brainfuck" in str(excinfo.value)

    def test_returns_emoji(self):
        result = detect_anomalies("Rust")
        assert "emoji" in result
        assert isinstance(result["emoji"], str)

    def test_returns_tool_info(self):
        result = detect_anomalies("Java")
        assert result["tool"] == TOOL_NAME
        assert result["version"] == TOOL_VERSION

    def test_returns_rotation_position(self):
        result = detect_anomalies("TypeScript")
        assert "rotation_position" in result
        assert isinstance(result["rotation_position"], int)

    def test_returns_timestamp(self):
        result = detect_anomalies("JavaScript")
        assert "timestamp" in result


class TestFormatAnomalyReport:
    """Test format_anomaly_report function."""

    def test_returns_string(self):
        result = detect_anomalies("Rust")
        report = format_anomaly_report(result)
        assert isinstance(report, str)

    def test_report_contains_language_name(self):
        result = detect_anomalies("Go")
        report = format_anomaly_report(result)
        assert "Go" in report

    def test_report_contains_anomaly_count(self):
        result = detect_anomalies("C/C++")
        report = format_anomaly_report(result)
        assert str(result["anomaly_count"]) in report

    def test_report_contains_next_language(self):
        result = detect_anomalies("Kotlin")
        report = format_anomaly_report(result)
        assert result["next_language"] in report

    def test_report_contains_severity_breakdown(self):
        result = detect_anomalies("Swift")
        report = format_anomaly_report(result)
        # Should contain severity counts
        assert "CRITICAL" in report or "critical" in report.lower()

    def test_empty_report_does_not_crash(self):
        # Create minimal report
        minimal = {
            "emoji": "🦀",
            "language": "Rust",
            "tool": TOOL_NAME,
            "version": TOOL_VERSION,
            "anomaly_count": 0,
            "severity_breakdown": {"critical": 0, "high": 0, "medium": 0, "low": 0},
            "anomalies": [],
            "paradoxes": [],
            "delightful_contradictions": [],
            "next_language": "Go",
        }
        report = format_anomaly_report(minimal)
        assert isinstance(report, str)
