#!/usr/bin/env python3
"""
Tests for polyglot_flavor module.
Run with: python -m pytest polyglot_flavor/tests/ -v
"""
import json
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
import polyglot_flavor as pf

from polyglot_flavor import (
    TOOL_NAME, TOOL_VERSION, LANGUAGE_PROFILES,
    load_rotation, save_rotation,
    flavor,
)


ROTATION_ORDER = ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"]


class TestPolyglotFlavor(unittest.TestCase):
    """Test suite for Polyglot Flavor."""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.rotation_file = os.path.join(self.test_dir, "language_rotation.json")
        self.original_rotation_file = pf.ROTATION_FILE

        self.test_data = {
            "languages": ROTATION_ORDER,
            "current_index": 0,
            "last_language": None,
            "updated_at": "2026-01-01T00:00:00+00:00",
        }
        with open(self.rotation_file, "w") as f:
            json.dump(self.test_data, f)
        pf.ROTATION_FILE = self.rotation_file

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)
        pf.ROTATION_FILE = self.original_rotation_file

    # ── Tool constants ──────────────────────────────────────────────────────────

    def test_tool_name(self):
        self.assertEqual(TOOL_NAME, "polyglot-flavor")

    def test_tool_version_semver(self):
        import re
        self.assertTrue(re.match(r"\d+\.\d+\.\d+", TOOL_VERSION))

    def test_rotation_order_8_languages(self):
        self.assertEqual(len(ROTATION_ORDER), 8)

    def test_all_languages_have_profiles(self):
        for lang in ROTATION_ORDER:
            self.assertIn(lang, LANGUAGE_PROFILES)

    def test_all_profiles_have_5_dimensions(self):
        for lang, profile in LANGUAGE_PROFILES.items():
            for dim in ["body", "aroma", "acidity", "finish", "uniqueness"]:
                self.assertIn(dim, profile, f"{lang} missing '{dim}'")

    def test_all_dimensions_in_range(self):
        for lang, profile in LANGUAGE_PROFILES.items():
            for dim in ["body", "aroma", "acidity", "finish", "uniqueness"]:
                self.assertGreaterEqual(profile[dim], 1)
                self.assertLessEqual(profile[dim], 5)

    # ── Rotation helpers ────────────────────────────────────────────────────────

    def test_load_rotation(self):
        data = load_rotation()
        self.assertIsInstance(data, dict)
        self.assertIn("languages", data)
        self.assertEqual(len(data["languages"]), 8)

    def test_save_rotation_updates_file(self):
        data = load_rotation()
        data["current_index"] = 5
        save_rotation(data)
        with open(self.rotation_file) as f:
            loaded = json.load(f)
        self.assertEqual(loaded["current_index"], 5)

    def test_flavor_increments_index(self):
        with open(self.rotation_file, "w") as f:
            json.dump({**self.test_data, "current_index": 0}, f)
        pf.flavor()
        data = load_rotation()
        self.assertEqual(data["current_index"], 1)

    def test_flavor_wraps(self):
        with open(self.rotation_file, "w") as f:
            json.dump({**self.test_data, "current_index": 7}, f)
        pf.flavor()
        data = load_rotation()
        self.assertEqual(data["current_index"], 0)

    # ── Core API ───────────────────────────────────────────────────────────────

    def test_flavor_structure(self):
        with open(self.rotation_file, "w") as f:
            json.dump({**self.test_data, "current_index": 0}, f)
        result = pf.flavor()
        self.assertIn("language", result)
        self.assertIn("profile", result)
        self.assertIn("overall_score", result)

    def test_flavor_language_field(self):
        with open(self.rotation_file, "w") as f:
            json.dump({**self.test_data, "current_index": 0}, f)
        result = pf.flavor()
        self.assertIn(result["language"], ROTATION_ORDER)

    def test_flavor_unknown_language_raises(self):
        # COBOL is not in LANGUAGE_PROFILES, should raise
        with open(self.rotation_file, "w") as f:
            json.dump({**self.test_data, "languages": ["COBOL"], "current_index": 0}, f)
        with self.assertRaises(ValueError):
            pf.flavor()

    def test_all_languages_have_valid_profile(self):
        for lang in ROTATION_ORDER:
            self.assertIn(lang, LANGUAGE_PROFILES)
            profile = LANGUAGE_PROFILES[lang]
            for dim in ["body", "aroma", "acidity", "finish", "uniqueness"]:
                self.assertIn(dim, profile)


if __name__ == "__main__":
    unittest.main(verbosity=2)
