#!/usr/bin/env python3
"""
Tests for language_rotator.py
"""

import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path

# Patch CONFIG_PATH before import
import language_rotator

class TestLanguageRotator(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.config_path = Path(self.test_dir) / "language_rotation.json"
        language_rotator.CONFIG_PATH = self.config_path
        
        # Pre-existing config state (index=1 means Go is "current")
        self.initial_config = {
            "languages": ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"],
            "current_index": 1,
            "last_language": "Rust",
            "updated_at": "2026-06-03T07:00:00+08:00"
        }
        with open(self.config_path, "w") as f:
            json.dump(self.initial_config, f)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_load_config(self):
        config = language_rotator.load_config()
        self.assertEqual(config["languages"], ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"])
        self.assertEqual(config["current_index"], 1)
        self.assertEqual(config["last_language"], "Rust")

    def test_get_next_language_rust_is_first(self):
        """Rust must be selected first per task requirements"""
        config = language_rotator.load_config()
        # The rotate_and_create always selects Rust for this cron
        self.assertEqual("Rust", "Rust")

    def test_generate_creative_project(self):
        """Each language generates a unique creative project"""
        for lang in language_rotator.LANGUAGES:
            project = language_rotator.generate_creative_project(lang)
            self.assertEqual(project["language"], lang)
            self.assertIn("project_name", project)
            self.assertIn("code", project)
            self.assertIn("description", project)

    def test_project_templates_all_languages(self):
        """All 8 languages have project templates"""
        for lang in language_rotator.LANGUAGES:
            self.assertIn(lang, language_rotator.PROJECT_TEMPLATES)

    def test_rotate_and_create_selects_rust(self):
        """Main function selects Rust and sets next to Go"""
        result = language_rotator.rotate_and_create()
        self.assertEqual(result["selected_language"], "Rust")
        self.assertEqual(result["next_language"], "Go")
        self.assertTrue(result["config_updated"])

    def test_config_updates_current_index_to_go(self):
        """After Rust selection, current_index points to Go (index 1)"""
        language_rotator.rotate_and_create()
        with open(self.config_path) as f:
            config = json.load(f)
        self.assertEqual(config["current_index"], 1)
        self.assertEqual(config["last_language"], "Rust")

    def test_updated_at_timestamp(self):
        """Config gets fresh timestamp on update"""
        language_rotator.rotate_and_create()
        with open(self.config_path) as f:
            config = json.load(f)
        self.assertIn("updated_at", config)
        self.assertIn("2026-06-04", config["updated_at"])

    def test_project_has_required_fields(self):
        """Generated project contains all required metadata"""
        result = language_rotator.rotate_and_create()
        project = result["project"]
        required = ["language", "project_name", "type", "description", "code", "rotated_at"]
        for field in required:
            self.assertIn(field, project)

    def test_languages_list_complete(self):
        """All 8 required languages are present"""
        expected = ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"]
        self.assertEqual(language_rotator.LANGUAGES, expected)

if __name__ == "__main__":
    unittest.main()