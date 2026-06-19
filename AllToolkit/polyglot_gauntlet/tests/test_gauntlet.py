#!/usr/bin/env python3
"""Tests for Polyglot Gauntlet."""

import json
import os
import sys
import unittest
from pathlib import Path

# Ensure the src module is importable
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from gauntlet import (
    TOOL_NAME,
    TOOL_VERSION,
    ROTATION_ORDER,
    GAUNTLET_DATA,
    load_rotation,
    save_rotation,
    get_current_language,
    advance_rotation,
    get_gauntlet,
    format_gauntlet,
)


class TestRotation(unittest.TestCase):
    ROTATION_FILE = str(Path(__file__).parent.parent.parent.parent / "language_rotation.json")

    def setUp(self):
        # Backup rotation file
        with open(self.ROTATION_FILE, "r") as f:
            self._backup = f.read()
        self._config = json.loads(self._backup)

    def tearDown(self):
        # Restore rotation file
        with open(self.ROTATION_FILE, "w") as f:
            f.write(self._backup)

    def test_rotation_file_exists_and_valid(self):
        config = load_rotation()
        self.assertIn("languages", config)
        self.assertIn("current_index", config)
        self.assertEqual(len(config["languages"]), 8)
        self.assertEqual(config["languages"], ROTATION_ORDER)

    def test_advance_rotation(self):
        config = load_rotation()
        idx_before = config["current_index"]
        lang_before = config["languages"][idx_before]
        advance_rotation(config)
        idx_after = config["current_index"]
        self.assertEqual((idx_before + 1) % 8, idx_after)
        self.assertEqual(config["languages"][idx_before], lang_before)
        # restore
        save_rotation(self._config)

    def test_get_current_language(self):
        config = load_rotation()
        lang = get_current_language(config)
        self.assertIn(lang, ROTATION_ORDER)
        idx = config["current_index"] % len(config["languages"])
        self.assertEqual(lang, config["languages"][idx])

    def test_rotation_advances_on_get_gauntlet(self):
        config = load_rotation()
        idx_before = config["current_index"]
        lang_before = config["languages"][idx_before]
        result = get_gauntlet()
        self.assertEqual(result["language"], lang_before)
        config = load_rotation()
        idx_after = config["current_index"]
        self.assertEqual((idx_before + 1) % 8, idx_after)
        self.assertEqual(config["last_language"], lang_before)

    def test_language_override_does_not_advance_rotation(self):
        config = load_rotation()
        idx_before = config["current_index"]
        result = get_gauntlet(language="Rust")
        self.assertEqual(result["language"], "Rust")
        config = load_rotation()
        idx_after = config["current_index"]
        self.assertEqual(idx_before, idx_after)

    def test_get_gauntlet_all_languages(self):
        for lang in ROTATION_ORDER:
            result = get_gauntlet(language=lang)
            self.assertEqual(result["language"], lang)
            self.assertIn("name", result)
            self.assertIn("challenge", result)
            self.assertIn("difficulty", result)
            self.assertIn("success_criteria", result)
            self.assertIn("failure_modes", result)
            self.assertIn("skills_tested", result)
            self.assertIn("mastery_quote", result)
            self.assertIn("hints", result)
            self.assertIn("starter_template", result)
            self.assertGreater(len(result["challenge"]), 20)
            self.assertGreaterEqual(len(result["success_criteria"]), 3)
            self.assertGreaterEqual(len(result["failure_modes"]), 3)

    def test_get_gauntlet_returns_next_language(self):
        config = load_rotation()
        idx = config["current_index"]
        current_lang = config["languages"][idx]
        next_lang = config["languages"][(idx + 1) % 8]
        result = get_gauntlet()
        self.assertEqual(result["next_language"], next_lang)
        self.assertNotEqual(result["language"], result["next_language"])

    def test_get_gauntlet_returns_valid_emoji(self):
        emoji_map = {
            "Rust": "🦀", "Go": "🐹", "Swift": "🦅", "Kotlin": "🟣",
            "TypeScript": "🔷", "JavaScript": "🟨", "Java": "☕", "C/C++": "⚙️"
        }
        for lang in ROTATION_ORDER:
            result = get_gauntlet(language=lang)
            self.assertEqual(result["emoji"], emoji_map[lang])

    def test_format_gauntlet_contains_all_sections(self):
        result = get_gauntlet(language="Rust")
        formatted = format_gauntlet(result)
        self.assertIn("⚔️", formatted)
        self.assertIn("Polyglot Gauntlet", formatted)
        self.assertIn("THE CHALLENGE", formatted)
        self.assertIn("SUCCESS CRITERIA", formatted)
        self.assertIn("FAILURE MODES", formatted)
        self.assertIn("SKILLS TESTED", formatted)
        self.assertIn("HINTS", formatted)
        self.assertIn("MASTERY QUOTE", formatted)
        self.assertIn("Next up", formatted)

    def test_format_gauntlet_uses_language_emoji(self):
        result = get_gauntlet(language="Rust")
        formatted = format_gauntlet(result)
        self.assertIn("🦀", formatted)
        result2 = get_gauntlet(language="Go")
        formatted2 = format_gauntlet(result2)
        self.assertIn("🐹", formatted2)

    def test_gauntlet_data_has_all_languages(self):
        for lang in ROTATION_ORDER:
            self.assertIn(lang, GAUNTLET_DATA, f"{lang} not in GAUNTLET_DATA")

    def test_gauntlet_data_structure_complete(self):
        for lang, data in GAUNTLET_DATA.items():
            required_keys = [
                "name", "challenge", "difficulty", "time_estimate",
                "skills_tested", "success_criteria", "failure_modes",
                "mastery_quote", "hints", "starter_template"
            ]
            for key in required_keys:
                self.assertIn(key, data, f"{lang} missing key '{key}'")
            self.assertGreaterEqual(len(data["skills_tested"]), 4)
            self.assertGreaterEqual(len(data["success_criteria"]), 4)
            self.assertGreaterEqual(len(data["failure_modes"]), 3)
            self.assertGreaterEqual(len(data["hints"]), 3)

    def test_tool_name_and_version(self):
        result = get_gauntlet(language="Rust")
        self.assertEqual(result["tool"], "polyglot-gauntlet")
        self.assertEqual(result["version"], "1.0.0")

    def test_hints_are_deterministic_per_language(self):
        """Same language always returns same number of hints from the pool."""
        result1 = get_gauntlet(language="Rust")
        result2 = get_gauntlet(language="Rust")
        result3 = get_gauntlet(language="Rust")
        # The number of hints and their presence should be consistent
        self.assertEqual(len(result1["hints"]), len(result2["hints"]))
        self.assertEqual(len(result2["hints"]), len(result3["hints"]))

    def test_difficulty_rating_format(self):
        for lang in ROTATION_ORDER:
            result = get_gauntlet(language=lang)
            diff = result["difficulty"]
            self.assertTrue(
                diff in ["★☆☆☆☆", "★★☆☆☆", "★★★☆☆", "★★★★☆", "★★★★★"],
                f"{lang} has invalid difficulty: {diff}"
            )

    def test_time_estimate_format(self):
        for lang in ROTATION_ORDER:
            result = get_gauntlet(language=lang)
            te = result["time_estimate"]
            self.assertTrue(
                "min" in te or "hour" in te or "h" in te or "m" in te,
                f"{lang} has unusual time estimate: {te}"
            )

    def test_starter_template_not_empty(self):
        for lang in ROTATION_ORDER:
            result = get_gauntlet(language=lang)
            self.assertGreater(
                len(result["starter_template"]), 50,
                f"{lang} starter template is too short"
            )

    def test_mastery_quote_not_empty(self):
        for lang in ROTATION_ORDER:
            result = get_gauntlet(language=lang)
            self.assertGreater(
                len(result["mastery_quote"]), 20,
                f"{lang} mastery quote too short"
            )

    def test_next_language_is_different(self):
        for lang in ROTATION_ORDER:
            result = get_gauntlet(language=lang)
            self.assertNotEqual(
                result["language"], result["next_language"],
                "next_language should differ from current"
            )

    def test_timestamp_format(self):
        result = get_gauntlet(language="Rust")
        ts = result["timestamp"]
        # Should be ISO format ending with +08:00
        self.assertIn("+08:00", ts)
        self.assertIn("T", ts)

    def test_rotation_field_in_result(self):
        result = get_gauntlet(language="Rust")
        self.assertEqual(result["rotation"], ROTATION_ORDER)


if __name__ == "__main__":
    unittest.main(verbosity=2)
