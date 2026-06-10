#!/usr/bin/env python3
"""
Tests for polyglot_translation module.
Run with: python -m pytest test_polyglot_translation.py -v
Or directly: python test_polyglot_translation.py
"""

import json
import os
import random
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

# Ensure module is importable (run from parent so module resolves)
sys.path.insert(0, str(Path(__file__).parent.parent))
import polyglot_translation as pt

from polyglot_translation import (
    ROTATION_ORDER,
    CULTURAL_DB,
    get_current_language,
    advance_rotation,
    pick_expression,
    generate_card,
    format_card,
    next_language,
    run,
    TOOL_NAME,
    TOOL_VERSION,
    TRANSLATION_RATING,
)


class TestPolyglotTranslation(unittest.TestCase):
    """Test suite for Polyglot Translation."""

    def setUp(self):
        """Create a temporary rotation file for isolated testing."""
        self.test_dir = tempfile.mkdtemp()
        self.rotation_file = os.path.join(self.test_dir, "language_rotation.json")
        self.original_rotation_file = pt.ROTATION_FILE

        # Write a clean rotation file
        self.test_data = {
            "languages": ROTATION_ORDER,
            "current_index": 0,
            "last_language": None,
            "updated_at": "2026-01-01T00:00:00+00:00",
        }
        with open(self.rotation_file, "w") as f:
            json.dump(self.test_data, f)

    def tearDown(self):
        """Clean up temporary directory."""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    # ── Rotation file helpers ──────────────────────────────────────────────────

    def test_rotation_file_exists_and_valid_json(self):
        """The rotation file should be valid JSON with required keys."""
        with open(self.rotation_file, "r") as f:
            data = json.load(f)
        self.assertIn("languages", data)
        self.assertIn("current_index", data)
        self.assertIn("last_language", data)
        self.assertIn("updated_at", data)

    def test_rotation_languages_match_tool_constants(self):
        """languages list in rotation file must match ROTATION_ORDER."""
        with open(self.rotation_file, "r") as f:
            data = json.load(f)
        self.assertEqual(data["languages"], ROTATION_ORDER)

    # ── get_current_language ─────────────────────────────────────────────────────

    def test_get_current_language_index_0(self):
        """At index 0, should return Rust."""
        result = get_current_language(self.rotation_file)
        self.assertEqual(result, "Rust")

    def test_get_current_language_index_1(self):
        """At index 1, should return Go."""
        with open(self.rotation_file, "w") as f:
            json.dump({**self.test_data, "current_index": 1}, f)
        result = get_current_language(self.rotation_file)
        self.assertEqual(result, "Go")

    def test_get_current_language_wraps_correctly(self):
        """Index 8 should wrap to index 0 (Rust)."""
        with open(self.rotation_file, "w") as f:
            json.dump({**self.test_data, "current_index": 8}, f)
        result = get_current_language(self.rotation_file)
        self.assertEqual(result, "Rust")

    def test_get_current_language_last_language_field(self):
        """Should read from whatever index is stored, regardless of last_language."""
        with open(self.rotation_file, "w") as f:
            json.dump({**self.test_data, "current_index": 3, "last_language": "Rust"}, f)
        result = get_current_language(self.rotation_file)
        self.assertEqual(result, "Kotlin")

    # ── advance_rotation ─────────────────────────────────────────────────────────

    def test_advance_rotation_returns_old_index(self):
        """advance_rotation returns the old index before advancing."""
        result = advance_rotation(self.rotation_file)
        self.assertEqual(result, 0)

    def test_advance_rotation_updates_current_index(self):
        """advance_rotation should increment current_index by 1."""
        advance_rotation(self.rotation_file)
        with open(self.rotation_file, "r") as f:
            data = json.load(f)
        self.assertEqual(data["current_index"], 1)

    def test_advance_rotation_wraps_after_last(self):
        """After 8 advances (index 7 → 0), should wrap correctly."""
        for i in range(8):
            advance_rotation(self.rotation_file)
        with open(self.rotation_file, "r") as f:
            data = json.load(f)
        self.assertEqual(data["current_index"], 0)

    def test_advance_rotation_updates_last_language(self):
        """advance_rotation should set last_language to the previous current language."""
        advance_rotation(self.rotation_file)
        with open(self.rotation_file, "r") as f:
            data = json.load(f)
        self.assertEqual(data["last_language"], "Rust")

    def test_advance_rotation_updates_timestamp(self):
        """advance_rotation should update updated_at to current UTC time."""
        old_data = {**self.test_data}
        advance_rotation(self.rotation_file)
        with open(self.rotation_file, "r") as f:
            data = json.load(f)
        self.assertNotEqual(data["updated_at"], old_data["updated_at"])

    # ── next_language ───────────────────────────────────────────────────────────

    def test_next_language_rust(self):
        """next_language('Rust') → 'Go'."""
        self.assertEqual(next_language("Rust"), "Go")

    def test_next_language_go(self):
        """next_language('Go') → 'Swift'."""
        self.assertEqual(next_language("Go"), "Swift")

    def test_next_language_cpp(self):
        """next_language('C/C++') → 'Rust' (wraps)."""
        self.assertEqual(next_language("C/C++"), "Rust")

    def test_next_language_kotlin(self):
        """next_language('Kotlin') → 'TypeScript'."""
        self.assertEqual(next_language("Kotlin"), "TypeScript")

    # ── pick_expression ─────────────────────────────────────────────────────────

    def test_pick_expression_returns_rust_expressions(self):
        """pick_expression('Rust') should return an expression with Rust cultural data."""
        expr = pick_expression("Rust")
        self.assertIn("text", expr)
        self.assertIn("context", expr)
        self.assertIn("culture", expr)
        self.assertIn("category", expr)

    def test_pick_expression_unknown_language_returns_fallback(self):
        """pick_expression for unknown language returns a fallback message."""
        expr = pick_expression("COBOL")
        self.assertIn("No cultural data", expr["text"])

    def test_pick_expression_all_categories_covered(self):
        """For each language, all five categories should exist."""
        for lang in ROTATION_ORDER:
            expr = pick_expression(lang)
            self.assertIn(expr["category"], ["idiom", "mantra", "war_story", "maxim", "meme"])

    def test_pick_expression_is_deterministic_per_run(self):
        """Calling pick_expression multiple times should give consistent category structure."""
        for lang in ROTATION_ORDER:
            expr = pick_expression(lang)
            self.assertIsInstance(expr["text"], str)
            self.assertTrue(len(expr["text"]) > 0)
            self.assertIsInstance(expr["context"], str)
            self.assertIsInstance(expr["culture"], str)

    # ── generate_card ───────────────────────────────────────────────────────────

    def test_generate_card_structure(self):
        """generate_card should return a dict with language, expression, translations."""
        card = generate_card("Rust")
        self.assertIn("language", card)
        self.assertIn("expression", card)
        self.assertIn("translations", card)
        self.assertIn("generated_at", card)

    def test_generate_card_language_matches_input(self):
        """generate_card('Rust') should have language='Rust'."""
        card = generate_card("Rust")
        self.assertEqual(card["language"], "Rust")

    def test_generate_card_translations_has_7_entries(self):
        """generate_card should produce 7 translation entries (all other languages)."""
        card = generate_card("Rust")
        self.assertEqual(len(card["translations"]), 7)
        languages = [t["target_language"] for t in card["translations"]]
        for lang in ROTATION_ORDER:
            if lang != "Rust":
                self.assertIn(lang, languages)

    def test_generate_card_source_not_in_translations(self):
        """generate_card should NOT include the source language in translations."""
        card = generate_card("Go")
        targets = [t["target_language"] for t in card["translations"]]
        self.assertNotIn("Go", targets)

    def test_generate_card_all_translations_have_rating(self):
        """Each translation entry should have a 'rating' field."""
        card = generate_card("Rust")
        for t in card["translations"]:
            self.assertIn("rating", t)
            self.assertIn(t["rating"], ["direct", "near", "adapted", "untranslatable"])

    def test_generate_card_generated_at_is_iso_format(self):
        """generated_at should be a valid ISO timestamp string."""
        card = generate_card("Rust")
        ts = card["generated_at"]
        self.assertIsInstance(ts, str)
        # Format: 2026-01-01T00:00:00+00:00 or similar ISO-8601
        self.assertIn("T", ts)
        self.assertTrue(ts.endswith("+00:00") or "Z" in ts or "+" in ts or "-" in ts.split("T")[1])

    # ── format_card ─────────────────────────────────────────────────────────────

    def test_format_card_returns_string(self):
        """format_card should return a string."""
        card = generate_card("Rust")
        result = format_card(card)
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)

    def test_format_card_contains_language(self):
        """format_card output should contain the language name."""
        card = generate_card("Rust")
        result = format_card(card)
        self.assertIn("Rust", result)

    def test_format_card_contains_expression_text(self):
        """format_card output should contain the expression text."""
        card = generate_card("Rust")
        result = format_card(card)
        expr_text = card["expression"]["text"]
        self.assertIn(expr_text, result)

    def test_format_card_contains_translation_targets(self):
        """format_card output should list all translation target languages."""
        card = generate_card("Rust")
        result = format_card(card)
        for t in card["translations"]:
            self.assertIn(t["target_language"], result)

    def test_format_card_contains_rating_symbols(self):
        """format_card output should contain translation rating symbols."""
        card = generate_card("Rust")
        result = format_card(card)
        # Should contain at least one of the rating symbols
        symbols = ["✅", "⚡", "🔧", "❌"]
        self.assertTrue(any(s in result for s in symbols))

    def test_format_card_contains_next_language(self):
        """format_card output should show the next language in rotation."""
        card = generate_card("Rust")
        result = format_card(card)
        self.assertIn("Go", result)  # Rust's next is Go

    # ── run ────────────────────────────────────────────────────────────────────────

    def test_run_returns_string(self):
        """run() should return a non-empty string."""
        result = run()
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)

    def test_run_advances_rotation(self):
        """run() should advance the rotation index by 1."""
        # Set index to 2 (Swift)
        with open(self.rotation_file, "w") as f:
            json.dump({**self.test_data, "current_index": 2}, f)
        # Monkey-patch ROTATION_FILE for this test
        old_file = pt.ROTATION_FILE
        pt.ROTATION_FILE = self.rotation_file

        old_lang = pt.get_current_language()
        pt.run()
        new_lang = pt.get_current_language()

        pt.ROTATION_FILE = old_file
        # After run(), index should advance from 2 to 3 (Kotlin)
        self.assertEqual(new_lang, "Kotlin")
        self.assertNotEqual(old_lang, new_lang)

    # ── Tool constants ───────────────────────────────────────────────────────────

    def test_tool_name_is_polyglot_translation(self):
        """TOOL_NAME should be 'polyglot-translation'."""
        self.assertEqual(TOOL_NAME, "polyglot-translation")

    def test_tool_version_is_semver_format(self):
        """TOOL_VERSION should be in semver format."""
        import re
        self.assertTrue(re.match(r"\d+\.\d+\.\d+", TOOL_VERSION))

    def test_rotation_order_has_8_languages(self):
        """ROTATION_ORDER should have exactly 8 languages."""
        self.assertEqual(len(ROTATION_ORDER), 8)

    def test_rotation_order_matches_specified_sequence(self):
        """ROTATION_ORDER should match the specified sequence."""
        self.assertEqual(
            ROTATION_ORDER,
            ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"],
        )

    def test_cultural_db_has_all_languages(self):
        """CULTURAL_DB should have entries for all 8 rotation languages."""
        for lang in ROTATION_ORDER:
            self.assertIn(lang, CULTURAL_DB)

    def test_cultural_db_each_language_has_all_categories(self):
        """Each language in CULTURAL_DB should have all 5 categories."""
        expected_categories = {"idiom", "mantra", "war_story", "maxim", "meme"}
        for lang in ROTATION_ORDER:
            categories = set(CULTURAL_DB[lang].keys())
            self.assertEqual(categories, expected_categories)

    def test_cultural_db_each_expression_has_required_fields(self):
        """Every expression in CULTURAL_DB should have text, context, culture."""
        for lang in ROTATION_ORDER:
            for category, expressions in CULTURAL_DB[lang].items():
                for expr in expressions:
                    self.assertIn("text", expr)
                    self.assertIn("context", expr)
                    self.assertIn("culture", expr)

    def test_translation_rating_has_all_keys(self):
        """TRANSLATION_RATING should have direct, near, adapted, untranslatable."""
        self.assertEqual(
            set(TRANSLATION_RATING.keys()),
            {"direct", "near", "adapted", "untranslatable"},
        )


class TestRotationSequence(unittest.TestCase):
    """Test that the rotation sequence matches spec: Rust → Go → Swift → Kotlin → TypeScript → JavaScript → Java → C/C++ → Rust (loop)."""

    def test_rotation_sequence_order(self):
        """Verify exact rotation order."""
        self.assertEqual(ROTATION_ORDER[0], "Rust")
        self.assertEqual(ROTATION_ORDER[1], "Go")
        self.assertEqual(ROTATION_ORDER[2], "Swift")
        self.assertEqual(ROTATION_ORDER[3], "Kotlin")
        self.assertEqual(ROTATION_ORDER[4], "TypeScript")
        self.assertEqual(ROTATION_ORDER[5], "JavaScript")
        self.assertEqual(ROTATION_ORDER[6], "Java")
        self.assertEqual(ROTATION_ORDER[7], "C/C++")

    def test_next_language_sequence_matches_rotation(self):
        """next_language should match the rotation order."""
        for i, lang in enumerate(ROTATION_ORDER):
            expected_next = ROTATION_ORDER[(i + 1) % len(ROTATION_ORDER)]
            self.assertEqual(next_language(lang), expected_next)


if __name__ == "__main__":
    unittest.main(verbosity=2)