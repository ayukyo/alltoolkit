#!/usr/bin/env python3
"""
Tests for polyglot_wire module.
Run with: python -m pytest polyglot_wire/tests/ -v
"""
import json
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
import polyglot_wire as pw

from polyglot_wire import (
    TOOL_NAME, TOOL_VERSION, TOOL_LANGUAGES, INTEROP_PROFILES, WIRE_MATRIX,
    load_rotation, save_rotation,
    wire, format_wire_text,
    get_compatibility_bar, get_serial_format_badge,
)


class TestPolyglotWire(unittest.TestCase):
    """Test suite for Polyglot Wire."""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.rotation_file = os.path.join(self.test_dir, "language_rotation.json")
        self.original_rotation_file = pw.ROTATION_FILE

        self.test_data = {
            "languages": TOOL_LANGUAGES,
            "current_index": 0,
            "last_language": None,
            "updated_at": "2026-01-01T00:00:00+00:00",
        }
        with open(self.rotation_file, "w") as f:
            json.dump(self.test_data, f)
        pw.ROTATION_FILE = self.rotation_file

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)
        pw.ROTATION_FILE = self.original_rotation_file

    # ── Tool constants ──────────────────────────────────────────────────────────

    def test_tool_name(self):
        self.assertEqual(TOOL_NAME, "polyglot-wire")

    def test_tool_version_semver(self):
        import re
        self.assertTrue(re.match(r"\d+\.\d+\.\d+", TOOL_VERSION))

    def test_tool_languages_count(self):
        self.assertEqual(len(TOOL_LANGUAGES), 8)

    def test_tool_languages_correct(self):
        self.assertEqual(TOOL_LANGUAGES[0], "Rust")
        self.assertEqual(TOOL_LANGUAGES[7], "C/C++")

    def test_all_languages_have_interop_profiles(self):
        for lang in TOOL_LANGUAGES:
            self.assertIn(lang, INTEROP_PROFILES)

    def test_all_profiles_have_required_fields(self):
        required = ["ffi_name", "ffi_mechanism", "serialization", "ipc_schemes", "wire_score"]
        for lang in TOOL_LANGUAGES:
            for field in required:
                self.assertIn(field, INTEROP_PROFILES[lang])

    def test_all_wire_scores_in_range(self):
        for lang in TOOL_LANGUAGES:
            score = INTEROP_PROFILES[lang]["wire_score"]
            self.assertGreaterEqual(score, 1)
            self.assertLessEqual(score, 10)

    def test_wire_matrix_complete(self):
        for lang in TOOL_LANGUAGES:
            self.assertIn(lang, WIRE_MATRIX)
            for other in TOOL_LANGUAGES:
                self.assertIn(other, WIRE_MATRIX[lang])

    # ── Rotation helpers ────────────────────────────────────────────────────────

    def test_load_rotation(self):
        data = load_rotation()
        self.assertIsInstance(data, dict)
        self.assertIn("languages", data)

    def test_save_rotation_updates_file(self):
        data = load_rotation()
        data["current_index"] = 3
        save_rotation(data)
        with open(self.rotation_file) as f:
            loaded = json.load(f)
        self.assertEqual(loaded["current_index"], 3)

    def test_wire_returns_result(self):
        with open(self.rotation_file, "w") as f:
            json.dump({**self.test_data, "current_index": 0}, f)
        result = wire()
        self.assertIn("language", result)
        self.assertIn(result["language"], TOOL_LANGUAGES)

    def test_wire_advances_index(self):
        with open(self.rotation_file, "w") as f:
            json.dump({**self.test_data, "current_index": 0}, f)
        wire()
        data = load_rotation()
        self.assertEqual(data["current_index"], 1)

    def test_wire_wraps_after_last(self):
        with open(self.rotation_file, "w") as f:
            json.dump({**self.test_data, "current_index": 7}, f)
        wire()
        data = load_rotation()
        self.assertEqual(data["current_index"], 0)

    # ── Core API ───────────────────────────────────────────────────────────────

    def test_wire_structure(self):
        with open(self.rotation_file, "w") as f:
            json.dump({**self.test_data, "current_index": 0}, f)
        result = wire()
        for field in ["language", "wire_score", "compatibility_matrix",
                      "ffi_profiles", "serialization", "calling_c_example"]:
            self.assertIn(field, result, f"Missing field: {field}")

    def test_compatibility_matrix_complete(self):
        with open(self.rotation_file, "w") as f:
            json.dump({**self.test_data, "current_index": 0}, f)
        result = wire()
        matrix = result["compatibility_matrix"]
        self.assertEqual(len(matrix), 7)  # all other languages

    def test_format_wire_text_returns_string(self):
        with open(self.rotation_file, "w") as f:
            json.dump({**self.test_data, "current_index": 0}, f)
        result = wire()
        text = format_wire_text(result)
        self.assertIsInstance(text, str)
        self.assertGreater(len(text), 50)

    def test_compatibility_bar_renders(self):
        bar = get_compatibility_bar(10)
        self.assertIn("10", bar)
        bar5 = get_compatibility_bar(5)
        self.assertIn("5", bar5)

    def test_serial_format_badge(self):
        badge = get_serial_format_badge("JSON")
        self.assertIsInstance(badge, str)
        badge_unknown = get_serial_format_badge("CustomFormat")
        self.assertIsInstance(badge_unknown, str)

    def test_all_wire_scores_in_matrix_range(self):
        for lang in TOOL_LANGUAGES:
            for other in TOOL_LANGUAGES:
                score = WIRE_MATRIX[lang][other]
                self.assertGreaterEqual(score, 0)
                self.assertLessEqual(score, 10)


if __name__ == "__main__":
    unittest.main(verbosity=2)
