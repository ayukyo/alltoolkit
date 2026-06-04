#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for language_rotator.py — Language Rotator Tool Module

Tests cover:
  1. Rotation logic correctness (sequential, wrapping)
  2. Challenge card generation for all languages
  3. Config persistence (load/save/increment)
  4. Language ordering integrity
  5. Edge cases (empty/wrap-around)
"""

from __future__ import print_function

import json
import os
import shutil
import tempfile
import unittest
from datetime import datetime, timezone, timedelta
from pathlib import Path

import language_rotator


# ── Helpers ───────────────────────────────────────────────────────────────────

def make_config(idx, last_lang=None):
    return {
        "languages": ["Rust", "Go", "Swift", "Kotlin",
                      "TypeScript", "JavaScript", "Java", "C/C++"],
        "current_index": idx,
        "last_language": last_lang,
        "updated_at": "2026-06-04T00:00:00+08:00",
    }


class TestLanguageRotator(unittest.TestCase):
    """Test suite for the language rotator tool."""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.config_path = Path(self.test_dir) / "language_rotation.json"
        language_rotator.ROTATION_FILE = self.config_path

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    # ── Rotation Logic ─────────────────────────────────────────────────────────

    def test_rotate_from_rust_goes_to_go(self):
        """Current index 0 = Rust -> next should be Go (index 1)."""
        cfg = make_config(0)
        with open(self.config_path, "w") as f:
            json.dump(cfg, f)
        config = language_rotator.load_rotation()
        language_rotator.save_rotation(language_rotator.advance_rotation(config))
        with open(self.config_path) as f:
            saved = json.load(f)
        self.assertEqual(saved["current_index"], 1)
        self.assertEqual(saved["last_language"], "Rust")

    def test_rotate_wraps_after_cpp(self):
        """After C/C++ (index 7), wrap back to Rust (index 0)."""
        cfg = make_config(7)
        with open(self.config_path, "w") as f:
            json.dump(cfg, f)
        config = language_rotator.load_rotation()
        language_rotator.save_rotation(language_rotator.advance_rotation(config))
        with open(self.config_path) as f:
            saved = json.load(f)
        self.assertEqual(saved["current_index"], 0)
        self.assertEqual(saved["last_language"], "C/C++")

    def test_full_cycle_order(self):
        """All 8 languages follow the correct rotation order."""
        cfg = make_config(0)
        with open(self.config_path, "w") as f:
            json.dump(cfg, f)
        expected = ["Rust", "Go", "Swift", "Kotlin",
                    "TypeScript", "JavaScript", "Java", "C/C++"]
        for i, lang in enumerate(expected):
            config = language_rotator.load_rotation()
            self.assertEqual(config["languages"][config["current_index"]], lang)
            config = language_rotator.advance_rotation(config)
            language_rotator.save_rotation(config)

    def test_repeated_rotations(self):
        """Multiple rotations stay within bounds and wrap correctly."""
        cfg = make_config(0)
        with open(self.config_path, "w") as f:
            json.dump(cfg, f)
        for _ in range(16):  # 2 full cycles
            config = language_rotator.load_rotation()
            config = language_rotator.advance_rotation(config)
            language_rotator.save_rotation(config)
        with open(self.config_path) as f:
            saved = json.load(f)
        self.assertEqual(saved["current_index"], 0)
        self.assertEqual(saved["last_language"], "C/C++")

    # ── Challenge Card ──────────────────────────────────────────────────────────

    def test_challenge_card_has_required_fields(self):
        """Every generated card contains all required metadata fields."""
        for lang in language_rotator.LANGUAGES:
            card = language_rotator.generate_challenge_card(lang, day_seed=5)
            self.assertIn("language", card)
            self.assertIn("category", card)
            self.assertIn("hook", card)
            self.assertIn("task", card)
            self.assertIn("constraints", card)
            self.assertIn("paradigm_focus", card)
            self.assertIn("emoji", card)
            self.assertIn("day_difficulty", card)
            self.assertIn("bonus_modifier", card)
            self.assertIn("generated_at", card)
            self.assertEqual(card["language"], lang)
            self.assertIsInstance(card["constraints"], list)
            self.assertGreater(len(card["constraints"]), 0)

    def test_challenge_card_is_deterministic_per_day_seed(self):
        """Same day_seed always produces the same challenge."""
        for lang in language_rotator.LANGUAGES:
            card1 = language_rotator.generate_challenge_card(lang, day_seed=42)
            card2 = language_rotator.generate_challenge_card(lang, day_seed=42)
            self.assertEqual(card1["category"], card2["category"])
            self.assertEqual(card1["task"], card2["task"])

    def test_challenge_card_changes_across_days(self):
        """Different day_seeds produce different challenges."""
        for lang in language_rotator.LANGUAGES:
            card1 = language_rotator.generate_challenge_card(lang, day_seed=1)
            card2 = language_rotator.generate_challenge_card(lang, day_seed=2)
            # At least one field should differ across days
            different = (
                card1["category"] != card2["category"]
                or card1["day_difficulty"] != card2["day_difficulty"]
                or card1["bonus_modifier"] != card2["bonus_modifier"]
            )
            self.assertTrue(different,
                           "{}: cards should differ across days".format(lang))

    def test_all_languages_have_templates(self):
        """Every language in the rotation has at least 4 challenge templates."""
        for lang in language_rotator.LANGUAGES:
            self.assertIn(lang, language_rotator._CHALLENGE_TEMPLATES)
            self.assertGreaterEqual(
                len(language_rotator._CHALLENGE_TEMPLATES[lang]), 4)

    def test_constraints_are_nonempty(self):
        """All challenge constraints are non-empty strings."""
        seen_langs = set()
        for day_seed in range(100):
            cfg = make_config(day_seed % 8)
            with open(self.config_path, "w") as f:
                json.dump(cfg, f)
            config = language_rotator.load_rotation()
            lang = config["languages"][config["current_index"]]
            if lang in seen_langs:
                continue
            seen_langs.add(lang)
            card = language_rotator.generate_challenge_card(lang, day_seed=day_seed)
            for constraint in card["constraints"]:
                self.assertIsInstance(constraint, str)
                self.assertGreater(len(constraint.strip()), 0)

    # ── Config Persistence ─────────────────────────────────────────────────────

    def test_load_config_file_not_found(self):
        """Bootstrap config if rotation file doesn't exist."""
        # Use a fresh empty dir
        tmpdir = tempfile.mkdtemp()
        language_rotator.ROTATION_FILE = Path(tmpdir) / "does_not_exist.json"
        try:
            config = language_rotator.load_rotation()
            self.assertEqual(
                config["languages"],
                ["Rust", "Go", "Swift", "Kotlin",
                 "TypeScript", "JavaScript", "Java", "C/C++"])
            self.assertEqual(config["current_index"], 0)
        finally:
            shutil.rmtree(tmpdir)

    def test_save_rotation_updates_timestamp(self):
        """Saving config refreshes the updated_at timestamp."""
        cfg = make_config(3)
        with open(self.config_path, "w") as f:
            json.dump(cfg, f)
        config = language_rotator.load_rotation()
        language_rotator.save_rotation(config)
        with open(self.config_path) as f:
            saved = json.load(f)
        self.assertIn("updated_at", saved)
        # Should be today
        today = datetime.now(timezone(timedelta(hours=8))).date().isoformat()
        self.assertTrue(saved["updated_at"].startswith(today))

    def test_advance_rotation_updates_both_fields(self):
        """advance_rotation must update both current_index AND last_language."""
        cfg = make_config(4)
        with open(self.config_path, "w") as f:
            json.dump(cfg, f)
        config = language_rotator.load_rotation()
        config = language_rotator.advance_rotation(config)
        self.assertEqual(config["current_index"], 5)
        # index 4 = TypeScript, so last_language = TypeScript
        self.assertEqual(config["last_language"], "TypeScript")

    # ── Main rotate_and_build ─────────────────────────────────────────────────

    def test_rotate_and_build_returns_structure(self):
        """Main function returns a well-structured result dict."""
        cfg = make_config(2)
        with open(self.config_path, "w") as f:
            json.dump(cfg, f)
        result = language_rotator.rotate_and_build()
        self.assertIn("tool", result)
        self.assertIn("version", result)
        self.assertIn("selected_language", result)
        self.assertIn("challenge", result)
        self.assertIn("rotation_state", result)
        self.assertIn("config_updated", result)
        self.assertIn("rotated_at", result)
        self.assertTrue(result["config_updated"])

    def test_rotate_and_build_persists_state(self):
        """rotate_and_build must persist updated index to disk."""
        cfg = make_config(5)
        with open(self.config_path, "w") as f:
            json.dump(cfg, f)
        language_rotator.rotate_and_build()
        with open(self.config_path) as f:
            saved = json.load(f)
        self.assertEqual(saved["current_index"], 6)
        self.assertEqual(saved["last_language"], "JavaScript")

    def test_rotate_and_build_next_language_correct(self):
        """rotation_state must reflect the NEXT language correctly."""
        cfg = make_config(0)  # Rust is current
        with open(self.config_path, "w") as f:
            json.dump(cfg, f)
        result = language_rotator.rotate_and_build()
        # After Rust, next should be Go
        self.assertEqual(result["rotation_state"]["current_language"], "Go")
        self.assertEqual(result["selected_language"], "Rust")

    def test_rotation_state_cycle_progress(self):
        """Cycle position and percentage are calculated correctly."""
        cfg = make_config(3)  # Kotlin (position 4 of 8 = 50%)
        with open(self.config_path, "w") as f:
            json.dump(cfg, f)
        result = language_rotator.rotate_and_build()
        self.assertEqual(result["rotation_state"]["cycle_position"], "5/8")
        self.assertEqual(result["rotation_state"]["cycle_progress_pct"], 50.0)

    # ── Rotation Order Integrity ────────────────────────────────────────────────

    def test_languages_list_complete(self):
        """All 8 required languages are present in correct order."""
        expected = ["Rust", "Go", "Swift", "Kotlin",
                    "TypeScript", "JavaScript", "Java", "C/C++"]
        self.assertEqual(language_rotator.LANGUAGES, expected)

    def test_get_language_at_index_wraps(self):
        """get_language_at_index handles out-of-range indices correctly."""
        langs = ["Rust", "Go", "Swift"]
        self.assertEqual(language_rotator.get_language_at_index(langs, 0), "Rust")
        self.assertEqual(language_rotator.get_language_at_index(langs, 3), "Rust")
        # index 10 -> 10 % 3 = 1 -> Go
        self.assertEqual(language_rotator.get_language_at_index(langs, 10), "Go")

    # ── Summary ───────────────────────────────────────────────────────────────

    def test_build_rotation_summary(self):
        """Summary contains all expected fields with correct values."""
        cfg = make_config(2)
        with open(self.config_path, "w") as f:
            json.dump(cfg, f)
        config = language_rotator.load_rotation()
        summary = language_rotator.build_rotation_summary(config)
        self.assertIn("rotation_order", summary)
        self.assertIn("current_index", summary)
        self.assertIn("current_language", summary)
        self.assertIn("last_language", summary)
        self.assertIn("cycle_position", summary)
        self.assertIn("cycle_progress_pct", summary)
        self.assertEqual(summary["current_language"], "Swift")
        self.assertEqual(summary["cycle_position"], "3/8")


if __name__ == "__main__":
    unittest.main()