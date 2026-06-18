#!/usr/bin/env python3
"""Tests for polyglot_echoes — echoes.py core functions."""

import json
import os
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from echoes import (
    TOOL_NAME,
    TOOL_VERSION,
    ROTATION_ORDER,
    ECHOES_DB,
    load_rotation,
    save_rotation,
    get_current_language,
    advance_rotation,
    pick_echo,
    generate_echo_report,
    format_echo_report,
    next_language,
    echoes,
)


class TestConstants(unittest.TestCase):
    def test_tool_name(self):
        self.assertEqual(TOOL_NAME, "polyglot-echoes")

    def test_tool_version(self):
        self.assertEqual(TOOL_VERSION, "1.0.0")

    def test_rotation_order(self):
        self.assertEqual(ROTATION_ORDER, [
            "Rust", "Go", "Swift", "Kotlin",
            "TypeScript", "JavaScript", "Java", "C/C++",
        ])

    def test_echoes_db_has_all_8_languages(self):
        for lang in ROTATION_ORDER:
            self.assertIn(lang, ECHOES_DB, f"{lang} missing from ECHOES_DB")

    def test_echoes_db_categories_per_language(self):
        expected_categories = {
            "BATTLE_CRY", "PHILOSOPHY", "GOTCHA",
            "COMMUNITY_SAY", "DESIGNER_VOICE", "LINGO",
        }
        for lang, categories in ECHOES_DB.items():
            self.assertEqual(set(categories.keys()), expected_categories,
                             f"{lang} categories mismatch")

    def test_echo_structure(self):
        for lang, categories in ECHOES_DB.items():
            for cat, echo_list in categories.items():
                self.assertIsInstance(echo_list, list)
                for echo in echo_list:
                    for key in ["text", "context", "meaning"]:
                        self.assertIn(key, echo, f"{lang}/{cat} missing '{key}'")


class TestNextLanguage(unittest.TestCase):
    def test_next_language_rust(self):
        self.assertEqual(next_language("Rust"), "Go")

    def test_next_language_go(self):
        self.assertEqual(next_language("Go"), "Swift")

    def test_next_language_cpp(self):
        self.assertEqual(next_language("C/C++"), "Rust")

    def test_next_language_unknown_raises(self):
        with self.assertRaises(ValueError):
            next_language("Brainfuck")


class TestPickEcho(unittest.TestCase):
    def test_pick_echo_returns_dict(self):
        result = pick_echo("Rust")
        self.assertIsInstance(result, dict)

    def test_pick_echo_has_required_fields(self):
        result = pick_echo("Go")
        for key in ["text", "context", "meaning"]:
            self.assertIn(key, result)

    def test_pick_echo_deterministic_seed(self):
        r1 = pick_echo("Swift", seed=42)
        r2 = pick_echo("Swift", seed=42)
        self.assertEqual(r1["text"], r2["text"])

    def test_pick_echo_unknown_language_returns_fallback(self):
        result = pick_echo("Brainfuck")
        self.assertIsInstance(result, dict)
        self.assertIn("text", result)

    def test_pick_echo_all_languages(self):
        for lang in ROTATION_ORDER:
            result = pick_echo(lang)
            self.assertIn("text", result)
            self.assertIn("context", result)
            self.assertIn("meaning", result)


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

    def test_get_current_language_valid(self):
        saved = self._save()
        try:
            lang = get_current_language()
            self.assertIn(lang, ROTATION_ORDER)
        finally:
            self._restore(saved)

    def test_advance_rotation_returns_int(self):
        saved = self._save()
        try:
            cfg_before = load_rotation()
            idx_before = cfg_before["current_index"]
            idx_after = advance_rotation()
            self.assertIsInstance(idx_after, int)
            cfg_after = load_rotation()
            self.assertEqual(cfg_after["current_index"], (idx_before + 1) % 8)
        finally:
            self._restore(saved)


class TestEchoReport(unittest.TestCase):
    ROTATION_FILE = str(Path(__file__).parent.parent.parent / "language_rotation.json")

    def _save(self):
        with open(self.ROTATION_FILE) as f:
            return f.read()

    def _restore(self, data):
        with open(self.ROTATION_FILE, "w") as f:
            f.write(data)

    def test_generate_echo_report_returns_dict(self):
        saved = self._save()
        try:
            report = generate_echo_report("Rust", seed=42)
            self.assertIsInstance(report, dict)
            for key in ["language", "echo", "cross_language_echoes", "timestamp"]:
                self.assertIn(key, report)
            self.assertIn("category", report["echo"])
        finally:
            self._restore(saved)

    def test_generate_echo_report_has_echo_fields(self):
        saved = self._save()
        try:
            report = generate_echo_report("Go", seed=123)
            echo = report["echo"]
            for key in ["text", "context", "meaning"]:
                self.assertIn(key, echo)
        finally:
            self._restore(saved)

    def test_generate_echo_report_deterministic_seed(self):
        saved = self._save()
        try:
            r1 = generate_echo_report("Swift", seed=999)
            r2 = generate_echo_report("Swift", seed=999)
            self.assertEqual(r1["echo"]["text"], r2["echo"]["text"])
        finally:
            self._restore(saved)

    def test_format_echo_report_returns_string(self):
        saved = self._save()
        try:
            report = generate_echo_report("Java", seed=888)
            txt = format_echo_report(report)
            self.assertIsInstance(txt, str)
            self.assertTrue(len(txt) > 0)
        finally:
            self._restore(saved)


class TestEchoesMain(unittest.TestCase):
    ROTATION_FILE = str(Path(__file__).parent.parent.parent / "language_rotation.json")

    def _save(self):
        with open(self.ROTATION_FILE) as f:
            return f.read()

    def _restore(self, data):
        with open(self.ROTATION_FILE, "w") as f:
            f.write(data)

    def test_echoes_returns_dict(self):
        saved = self._save()
        try:
            result = echoes(seed=555)
            self.assertIsInstance(result, dict)
        finally:
            self._restore(saved)

    def test_echoes_override_language(self):
        saved = self._save()
        try:
            result = echoes(seed=111, override_language="Rust")
            self.assertEqual(result["language"], "Rust")
        finally:
            self._restore(saved)


if __name__ == "__main__":
    unittest.main()
