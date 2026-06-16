#!/usr/bin/env python3
"""
Tests for polyglot_resonator module.
Run with: python -m pytest polyglot_resonator/tests/ -v
"""
import json
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
import polyglot_resonator as pr

from polyglot_resonator import (
    TOOL_NAME, TOOL_VERSION, CONCEPT_FRAMES,
    load_rotation, save_rotation,
    get_resonance, resonator,
)


ROTATION_ORDER = ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"]


class TestPolyglotResonator(unittest.TestCase):
    """Test suite for Polyglot Resonator."""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.rotation_file = os.path.join(self.test_dir, "language_rotation.json")
        self.original_rotation_file = pr.ROTATION_FILE

        self.test_data = {
            "languages": ROTATION_ORDER,
            "current_index": 0,
            "last_language": None,
            "updated_at": "2026-01-01T00:00:00+00:00",
        }
        with open(self.rotation_file, "w") as f:
            json.dump(self.test_data, f)
        pr.ROTATION_FILE = self.rotation_file

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)
        pr.ROTATION_FILE = self.original_rotation_file

    # ── Tool constants ──────────────────────────────────────────────────────────

    def test_tool_name(self):
        self.assertEqual(TOOL_NAME, "polyglot-resonator")

    def test_tool_version_semver(self):
        import re
        self.assertTrue(re.match(r"\d+\.\d+\.\d+", TOOL_VERSION))

    def test_rotation_order_8_languages(self):
        self.assertEqual(len(ROTATION_ORDER), 8)

    def test_concept_frames_count(self):
        self.assertGreaterEqual(len(CONCEPT_FRAMES), 4)

    def test_each_concept_frame_has_required_fields(self):
        for frame in CONCEPT_FRAMES:
            self.assertIn("id", frame)
            self.assertIn("name", frame)
            self.assertIn("emoji", frame)
            self.assertIn("question", frame)
            self.assertIn("resonance", frame)

    def test_each_concept_frame_has_all_8_languages(self):
        for frame in CONCEPT_FRAMES:
            for lang in ROTATION_ORDER:
                self.assertIn(lang, frame["resonance"])

    def test_each_language_resonance_has_required_fields(self):
        for frame in CONCEPT_FRAMES:
            for lang, res in frame["resonance"].items():
                self.assertIn("stance", res)
                self.assertIn("summary", res)
                self.assertIn("key_concept", res)
                self.assertIn("philosophy", res)
                self.assertIn("idiom", res)

    # ── Rotation helpers ────────────────────────────────────────────────────────

    def test_load_rotation(self):
        data = load_rotation()
        self.assertIsInstance(data, dict)
        self.assertIn("languages", data)
        self.assertIn("current_index", data)

    def test_save_rotation_updates_file(self):
        data = load_rotation()
        data["current_index"] = 3
        save_rotation(data)
        with open(self.rotation_file) as f:
            loaded = json.load(f)
        self.assertEqual(loaded["current_index"], 3)

    def test_resonator_increments_index(self):
        with open(self.rotation_file, "w") as f:
            json.dump({**self.test_data, "current_index": 0}, f)
        pr.resonator()
        data = load_rotation()
        self.assertEqual(data["current_index"], 1)

    def test_resonator_wraps(self):
        with open(self.rotation_file, "w") as f:
            json.dump({**self.test_data, "current_index": 7}, f)
        pr.resonator()
        data = load_rotation()
        self.assertEqual(data["current_index"], 0)

    # ── Core API ───────────────────────────────────────────────────────────────

    def test_resonator_structure(self):
        with open(self.rotation_file, "w") as f:
            json.dump({**self.test_data, "current_index": 0}, f)
        result = pr.resonator()
        self.assertIn("selected_language", result)
        self.assertIn("concept_frame", result)
        self.assertIn("featured_resonance", result)
        self.assertIn("all_resonances", result)
        self.assertIn("next_language", result)

    def test_resonator_language_matches_input(self):
        with open(self.rotation_file, "w") as f:
            json.dump({**self.test_data, "current_index": 0}, f)
        result = pr.resonator()
        self.assertIn(result["selected_language"], ROTATION_ORDER)

    def test_resonator_unknown_language_raises(self):
        # COBOL is not in the rotation list, so resonator should raise
        # We test with a language not in the rotation
        with self.assertRaises((ValueError, KeyError)):
            pr.resonator(language="COBOL")

    def test_resonator_deterministic_seed(self):
        with open(self.rotation_file, "w") as f:
            json.dump({**self.test_data, "current_index": 0}, f)
        r1 = pr.resonator(language="Rust", seed=0)
        r2 = pr.resonator(language="Rust", seed=0)
        self.assertEqual(r1["concept_frame"]["id"], r2["concept_frame"]["id"])

    def test_resonator_different_seeds_different_frames(self):
        with open(self.rotation_file, "w") as f:
            json.dump({**self.test_data, "current_index": 0}, f)
        r1 = pr.resonator(seed=0)
        r2 = pr.resonator(seed=2)
        self.assertNotEqual(r1["concept_frame"]["id"], r2["concept_frame"]["id"])

    def test_get_resonance_returns_valid_data(self):
        frame = CONCEPT_FRAMES[0]
        res = get_resonance("Rust", frame)
        self.assertIn("stance", res)
        self.assertIn("summary", res)

    def test_resonator_comparison_has_all_other_languages(self):
        with open(self.rotation_file, "w") as f:
            json.dump({**self.test_data, "current_index": 0}, f)
        result = pr.resonator(language="Rust")
        # all_resonances has all 8
        self.assertEqual(len(result["all_resonances"]), 8)

    def test_all_concept_frames_resonance_complete(self):
        for frame in CONCEPT_FRAMES:
            for lang in ROTATION_ORDER:
                res = frame["resonance"][lang]
                self.assertGreater(len(res.get("stance", "")), 3)
                self.assertGreater(len(res.get("philosophy", "")), 3)


if __name__ == "__main__":
    unittest.main(verbosity=2)
