#!/usr/bin/env python3
"""Tests for polyglot_vessel — vessel.py core functions."""

import json
import os
import sys
import unittest
from pathlib import Path

# Ensure the module is importable
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from vessel import (
    TOOL_NAME,
    TOOL_VERSION,
    ROTATION_ORDER,
    VESSEL_DATA,
    load_rotation,
    save_rotation,
    advance_rotation,
    get_current_language,
    _pressure_label,
    _density_label,
    _volatility_label,
    _buoyancy_label,
    _make_bar,
    _overall_vessel_score,
    generate_vessel_report,
    format_vessel_report,
)


class TestConstants(unittest.TestCase):
    def test_tool_name(self):
        self.assertEqual(TOOL_NAME, "polyglot-vessel")

    def test_tool_version(self):
        self.assertEqual(TOOL_VERSION, "1.0.0")

    def test_rotation_order(self):
        self.assertEqual(ROTATION_ORDER, [
            "Rust", "Go", "Swift", "Kotlin",
            "TypeScript", "JavaScript", "Java", "C/C++",
        ])

    def test_vessel_data_has_all_8_languages(self):
        for lang in ROTATION_ORDER:
            self.assertIn(lang, VESSEL_DATA, f"{lang} missing from VESSEL_DATA")

    def test_vessel_data_structure(self):
        required_keys = [
            "core_essence", "pressure_rating", "density", "volatility",
            "buoyancy", "pour_temperature", "distillation_notes",
            "appearance", "odour", "flame_test", "shelf_life",
            "compatible_with", "vessel_shape",
        ]
        for lang, data in VESSEL_DATA.items():
            for key in required_keys:
                self.assertIn(key, data, f"{lang} missing '{key}'")


class TestLabelHelpers(unittest.TestCase):
    def test_pressure_label_returns_string(self):
        for val in [1.0, 3.5, 5.5, 7.5, 9.5]:
            label = _pressure_label(val)
            self.assertIsInstance(label, str)
            self.assertTrue(len(label) > 0)

    def test_density_label_returns_string(self):
        for val in [3.0, 5.5, 8.5]:
            label = _density_label(val)
            self.assertIsInstance(label, str)
            self.assertTrue(len(label) > 0)

    def test_volatility_label_returns_string(self):
        for val in [2.0, 5.0, 8.5]:
            label = _volatility_label(val)
            self.assertIsInstance(label, str)
            self.assertTrue(len(label) > 0)

    def test_buoyancy_label_returns_string(self):
        for val in [2.0, 5.5, 9.0]:
            label = _buoyancy_label(val)
            self.assertIsInstance(label, str)
            self.assertTrue(len(label) > 0)

    def test_make_bar_length(self):
        for width in [10, 20, 40]:
            bar = _make_bar(5.0, width=width)
            # Bar is [ + width chars + ] so total width+2
            self.assertEqual(len(bar), width + 2)

    def test_make_bar_format(self):
        bar = _make_bar(5.0, width=20)
        self.assertTrue(bar.startswith("["))
        self.assertTrue(bar.endswith("]"))

    def test_overall_vessel_score_returns_dict(self):
        score = _overall_vessel_score(5.0, 5.0, 5.0, 5.0)
        self.assertIsInstance(score, dict)
        self.assertIn("overall_score", score)


class TestRotation(unittest.TestCase):
    ROTATION_FILE = str(Path(__file__).parent.parent.parent / "language_rotation.json")

    def _save(self):
        with open(self.ROTATION_FILE) as f:
            return f.read()

    def _restore(self, data):
        with open(self.ROTATION_FILE, "w") as f:
            f.write(data)

    def test_load_rotation_returns_dict(self):
        saved = self._save()
        try:
            cfg = load_rotation()
            self.assertIsInstance(cfg, dict)
            self.assertIn("languages", cfg)
            self.assertIn("current_index", cfg)
        finally:
            self._restore(saved)

    def test_get_current_language_returns_valid_language(self):
        saved = self._save()
        try:
            lang = get_current_language()
            self.assertIn(lang, ROTATION_ORDER)
        finally:
            self._restore(saved)

    def test_advance_rotation_returns_tuple(self):
        saved = self._save()
        try:
            result = advance_rotation()
            self.assertIsInstance(result, tuple)
            self.assertEqual(len(result), 3)
            lang, idx, next_lang = result
            self.assertIn(lang, ROTATION_ORDER)
            self.assertIsInstance(idx, int)
            self.assertIn(next_lang, ROTATION_ORDER)
        finally:
            self._restore(saved)


class TestVesselReport(unittest.TestCase):
    ROTATION_FILE = str(Path(__file__).parent.parent.parent / "language_rotation.json")

    def _save(self):
        with open(self.ROTATION_FILE) as f:
            return f.read()

    def _restore(self, data):
        with open(self.ROTATION_FILE, "w") as f:
            f.write(data)

    def test_generate_vessel_report_returns_dict(self):
        saved = self._save()
        try:
            report = generate_vessel_report(seed=42)
            self.assertIsInstance(report, dict)
            self.assertIn("language", report)
            self.assertIn("vessel_certificate", report)
            self.assertIn("overall_assessment", report)
        finally:
            self._restore(saved)

    def test_generate_vessel_report_language_matches_vessel_data(self):
        saved = self._save()
        try:
            report = generate_vessel_report(seed=99)
            self.assertIn(report["language"], VESSEL_DATA)
        finally:
            self._restore(saved)

    def test_format_vessel_report_returns_string(self):
        saved = self._save()
        try:
            report = generate_vessel_report(seed=777)
            txt = format_vessel_report(report)
            self.assertIsInstance(txt, str)
            self.assertIn(report["language"], txt)
        finally:
            self._restore(saved)


if __name__ == "__main__":
    unittest.main()
