#!/usr/bin/env python3
"""Tests for polyglot_pantheon — pantheon.py core functions."""

import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pantheon import (
    TOOL_NAME,
    TOOL_VERSION,
    ROTATION_ORDER,
    LANGUAGE_DEITIES,
    load_rotation,
    save_rotation,
    build_divinity_bar,
    build_domain_web,
    pantheon,
)


class TestConstants(unittest.TestCase):
    def test_tool_name(self):
        self.assertEqual(TOOL_NAME, "polyglot-pantheon")

    def test_tool_version(self):
        self.assertEqual(TOOL_VERSION, "1.0.0")

    def test_rotation_order(self):
        self.assertEqual(ROTATION_ORDER, [
            "Rust", "Go", "Swift", "Kotlin",
            "TypeScript", "JavaScript", "Java", "C/C++",
        ])

    def test_language_deities_all_8(self):
        for lang in ROTATION_ORDER:
            self.assertIn(lang, LANGUAGE_DEITIES, f"{lang} missing")

    def test_deity_structure(self):
        required_fields = [
            "divine_name", "domain", "portfolio", "mythology",
            "sacred_text", "divine_rank", "blessing", "power_level",
            "divine_relationships", "prophecy",
        ]
        for lang, deity in LANGUAGE_DEITIES.items():
            for field in required_fields:
                self.assertIn(field, deity, f"{lang} missing '{field}'")


class TestBuildHelpers(unittest.TestCase):
    def test_build_divinity_bar_string(self):
        bar = build_divinity_bar(75, 100)
        self.assertIsInstance(bar, str)
        self.assertTrue(len(bar) > 0)

    def test_build_divinity_bar_zero(self):
        bar = build_divinity_bar(0, 100)
        self.assertIsInstance(bar, str)

    def test_build_divinity_bar_max(self):
        bar = build_divinity_bar(100, 100)
        self.assertIsInstance(bar, str)

    def test_build_domain_web_returns_string(self):
        deity = LANGUAGE_DEITIES.get("Rust", {})
        web = build_domain_web(deity)
        self.assertIsInstance(web, str)

    def test_build_domain_web_all_languages(self):
        for lang, deity in LANGUAGE_DEITIES.items():
            web = build_domain_web(deity)
            self.assertIsInstance(web, str)


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
        finally:
            self._restore(saved)


class TestPantheonMain(unittest.TestCase):
    ROTATION_FILE = str(Path(__file__).parent.parent.parent / "language_rotation.json")

    def _save(self):
        with open(self.ROTATION_FILE) as f:
            return f.read()

    def _restore(self, data):
        with open(self.ROTATION_FILE, "w") as f:
            f.write(data)

    def test_pantheon_returns_dict(self):
        saved = self._save()
        try:
            result = pantheon()
            self.assertIsInstance(result, dict)
        finally:
            self._restore(saved)

    def test_pantheon_has_required_keys(self):
        saved = self._save()
        try:
            result = pantheon()
            required = [
                "tool", "version", "language", "divine_name", "domain",
                "divine_rank", "portfolio", "domain_web", "mythology",
                "sacred_text", "blessing", "worship_practice",
                "divine_relationships", "prophecy", "power_level",
                "divinity_bar", "next_language", "timestamp",
            ]
            for key in required:
                self.assertIn(key, result, f"Missing key: {key}")
        finally:
            self._restore(saved)

    def test_pantheon_language_in_deities(self):
        saved = self._save()
        try:
            result = pantheon()
            self.assertIn(result["language"], LANGUAGE_DEITIES)
        finally:
            self._restore(saved)

    def test_pantheon_advances_rotation(self):
        saved = self._save()
        try:
            cfg_before = load_rotation()
            idx_before = cfg_before["current_index"]
            result = pantheon()
            cfg_after = load_rotation()
            idx_after = cfg_after["current_index"]
            self.assertEqual(idx_after, (idx_before + 1) % 8)
        finally:
            self._restore(saved)

    def test_pantheon_sets_last_language(self):
        saved = self._save()
        try:
            result = pantheon()
            cfg = load_rotation()
            self.assertEqual(cfg.get("last_language"), result["language"])
        finally:
            self._restore(saved)


if __name__ == "__main__":
    unittest.main()
