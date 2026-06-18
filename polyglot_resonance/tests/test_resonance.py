#!/usr/bin/env python3
"""Tests for polyglot_resonance — resonance functions."""

import importlib.util
import sys
import unittest
from pathlib import Path

# Load the module using importlib
_spec = importlib.util.spec_from_file_location(
    "polyglot_resonance",
    Path(__file__).parent.parent / "src" / "__init__.py"
)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

TOOL_NAME = _mod.TOOL_NAME
TOOL_VERSION = _mod.TOOL_VERSION
ROTATION_ORDER = _mod.ROTATION_ORDER
RESONANCE_THEMES = _mod.RESONANCE_THEMES
load_rotation = _mod.load_rotation
save_rotation = _mod.save_rotation
resonance = _mod.resonance
generate_resonance_analysis = _mod.generate_resonance_analysis
format_resonance = _mod.format_resonance


class TestConstants(unittest.TestCase):
    def test_tool_name(self):
        self.assertEqual(TOOL_NAME, "polyglot-resonance")

    def test_tool_version(self):
        self.assertEqual(TOOL_VERSION, "1.0.0")

    def test_rotation_order(self):
        self.assertEqual(ROTATION_ORDER, [
            "Rust", "Go", "Swift", "Kotlin",
            "TypeScript", "JavaScript", "Java", "C/C++",
        ])

    def test_resonance_themes_is_list(self):
        self.assertIsInstance(RESONANCE_THEMES, list)
        self.assertTrue(len(RESONANCE_THEMES) > 0)


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
        finally:
            self._restore(saved)


class TestResonanceMain(unittest.TestCase):
    ROTATION_FILE = str(Path(__file__).parent.parent.parent / "language_rotation.json")

    def _save(self):
        with open(self.ROTATION_FILE) as f:
            return f.read()

    def _restore(self, data):
        with open(self.ROTATION_FILE, "w") as f:
            f.write(data)

    def test_resonance_returns_dict(self):
        saved = self._save()
        try:
            result = resonance()
            self.assertIsInstance(result, dict)
        finally:
            self._restore(saved)

    def test_resonance_has_required_keys(self):
        saved = self._save()
        try:
            result = resonance()
            for key in ["tool", "version", "language", "theme", "language_resonance", "waveform_display", "overtones"]:
                self.assertIn(key, result)
        finally:
            self._restore(saved)

    def test_resonance_advances_rotation(self):
        saved = self._save()
        try:
            cfg_before = load_rotation()
            idx_before = cfg_before["current_index"]
            resonance()
            cfg_after = load_rotation()
            self.assertEqual(cfg_after["current_index"], (idx_before + 1) % 8)
        finally:
            self._restore(saved)


class TestGenerateResonance(unittest.TestCase):
    def test_generate_resonance_analysis_returns_dict(self):
        theme = RESONANCE_THEMES[0]
        result = generate_resonance_analysis("Rust", theme)
        self.assertIsInstance(result, dict)

    def test_generate_resonance_analysis_all_languages(self):
        theme = RESONANCE_THEMES[0]
        for lang in ROTATION_ORDER:
            result = generate_resonance_analysis(lang, theme)
            self.assertIn("language", result)
            self.assertIn("language_resonance", result)


class TestFormatResonance(unittest.TestCase):
    def test_format_resonance_returns_string(self):
        theme = RESONANCE_THEMES[0]
        result = generate_resonance_analysis("Go", theme)
        txt = format_resonance(result)
        self.assertIsInstance(txt, str)
        self.assertTrue(len(txt) > 0)


if __name__ == "__main__":
    unittest.main()
