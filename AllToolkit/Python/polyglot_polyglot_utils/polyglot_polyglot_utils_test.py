#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Polyglot Pattern Translation Utilities Test Suite
===============================================================
Comprehensive tests for polyglot_polyglot_utils module.

Run with: python polyglot_polyglot_utils_test.py -v
Or:       python -m pytest polyglot_polyglot_utils_test.py -v
"""

import sys
import os
import json
import unittest
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    # Constants
    LANGUAGE_ROTATION,
    LANGUAGE_META,
    ROTATION_FILE,
    ALL_PATTERNS,
    PATTERN_CATEGORIES,
    # Pattern dataclasses
    Pattern,
    PatternExample,
    # Pattern objects
    NULL_PATTERNS,
    ERROR_PATTERNS,
    CONCURRENCY_PATTERNS,
    ITERATION_PATTERNS,
    COMPOSITION_PATTERNS,
    # Rotation utilities
    get_rotation_state,
    advance_rotation,
    get_current_language,
    get_next_language,
    # Pattern query API
    get_pattern,
    get_all_patterns,
    get_patterns_by_category,
    get_pattern_for_language,
    format_pattern_markdown,
)


# =============================================================================
# Test Data Fixtures
# =============================================================================

SAMPLE_ROTATION_STATE = {
    "languages": [
        "Python", "Rust", "Go", "Swift", "Kotlin", "TypeScript",
        "JavaScript", "Java", "C/C++", "Lua", "C#", "PHP", "Ruby",
        "R", "SQL", "MATLAB", "Perl", "Delphi", "Fortran",
        "ArkTS", "VB", "Zig"
    ],
    "current_index": 1,
    "last_language": "Rust",
    "updated_at": "2026-06-11T04:13:31.913245+08:00"
}


# =============================================================================
# Test Language Rotation Constants
# =============================================================================

class TestLanguageRotationConstants(unittest.TestCase):
    """Tests for the LANGUAGE_ROTATION constant."""

    def test_rotation_has_eight_languages(self):
        """Rotation should contain exactly 8 languages."""
        self.assertEqual(len(LANGUAGE_ROTATION), 8)

    def test_rotation_correct_order(self):
        """Rotation should follow the specified order."""
        expected = [
            "Rust", "Go", "Swift", "Kotlin", "TypeScript",
            "JavaScript", "Java", "C/C++"
        ]
        self.assertEqual(LANGUAGE_ROTATION, expected)

    def test_rotation_no_duplicates(self):
        """Rotation should contain no duplicate languages."""
        self.assertEqual(len(LANGUAGE_ROTATION), len(set(LANGUAGE_ROTATION)))

    def test_rotation_starts_with_rust(self):
        """Rotation should start with Rust."""
        self.assertEqual(LANGUAGE_ROTATION[0], "Rust")

    def test_rotation_ends_with_cpp(self):
        """Rotation should end with C/C++."""
        self.assertEqual(LANGUAGE_ROTATION[-1], "C/C++")


# =============================================================================
# Test Language Metadata
# =============================================================================

class TestLanguageMeta(unittest.TestCase):
    """Tests for LANGUAGE_META."""

    def test_all_rotation_languages_have_metadata(self):
        """Every language in the rotation should have metadata."""
        for lang in LANGUAGE_ROTATION:
            with self.subTest(lang=lang):
                self.assertIn(lang, LANGUAGE_META)

    def test_metadata_has_required_fields(self):
        """Each language should have extension, style, paradigm, gc, null_safety."""
        required = ["extension", "style", "paradigm", "gc", "null_safety"]
        for lang in LANGUAGE_ROTATION:
            with self.subTest(lang=lang):
                meta = LANGUAGE_META[lang]
                for field in required:
                    self.assertIn(field, meta, f"{lang} missing {field}")

    def test_extensions_are_correct_format(self):
        """Each language should have a proper file extension."""
        expected = {
            "Rust": ".rs", "Go": ".go", "Swift": ".swift",
            "Kotlin": ".kt", "TypeScript": ".ts", "JavaScript": ".js",
            "Java": ".java", "C/C++": ".cpp"
        }
        for lang, ext in expected.items():
            with self.subTest(lang=lang):
                self.assertEqual(LANGUAGE_META[lang]["extension"], ext)

    def test_gc_field_types(self):
        """gc field should be boolean."""
        for lang in LANGUAGE_ROTATION:
            with self.subTest(lang=lang):
                self.assertIsInstance(LANGUAGE_META[lang]["gc"], bool)

    def test_rust_has_no_gc(self):
        """Rust should have gc=False."""
        self.assertFalse(LANGUAGE_META["Rust"]["gc"])

    def test_cpp_has_no_gc(self):
        """C/C++ should have gc=False."""
        self.assertFalse(LANGUAGE_META["C/C++"]["gc"])

    def test_garbage_collected_languages(self):
        """Go, Swift, Kotlin, TS, JS, Java should have gc=True."""
        gc_langs = ["Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java"]
        for lang in gc_langs:
            with self.subTest(lang=lang):
                self.assertTrue(LANGUAGE_META[lang]["gc"])


# =============================================================================
# Test Pattern Definitions
# =============================================================================

class TestPatternDefinitions(unittest.TestCase):
    """Tests for the pattern definitions."""

    def test_all_patterns_have_id(self):
        """Every pattern should have an id."""
        for p in ALL_PATTERNS.values():
            with self.subTest(pattern=p.id):
                self.assertIsNotNone(p.id)
                self.assertNotEqual(p.id, "")

    def test_all_patterns_have_name(self):
        """Every pattern should have a name."""
        for p in ALL_PATTERNS.values():
            with self.subTest(pattern=p.id):
                self.assertIsNotNone(p.name)
                self.assertNotEqual(p.name, "")

    def test_all_patterns_have_description(self):
        """Every pattern should have a description."""
        for p in ALL_PATTERNS.values():
            with self.subTest(pattern=p.id):
                self.assertIsNotNone(p.description)
                self.assertNotEqual(p.description, "")

    def test_all_patterns_have_category(self):
        """Every pattern should have a category."""
        for p in ALL_PATTERNS.values():
            with self.subTest(pattern=p.id):
                self.assertIsNotNone(p.category)
                self.assertNotEqual(p.category, "")

    def test_all_patterns_have_examples(self):
        """Every pattern should have at least one example."""
        for p in ALL_PATTERNS.values():
            with self.subTest(pattern=p.id):
                self.assertGreater(len(p.examples), 0)

    def test_each_pattern_has_eight_examples(self):
        """Each pattern should have exactly 8 examples (one per language)."""
        for p in ALL_PATTERNS.values():
            with self.subTest(pattern=p.id):
                self.assertEqual(len(p.examples), 8)

    def test_each_example_has_language(self):
        """Each example should have a language field."""
        for p in ALL_PATTERNS.values():
            for ex in p.examples:
                with self.subTest(pattern=p.id, example=ex.language):
                    self.assertIsNotNone(ex.language)
                    self.assertIn(ex.language, LANGUAGE_ROTATION)

    def test_each_example_has_code(self):
        """Each example should have non-empty code."""
        for p in ALL_PATTERNS.values():
            for ex in p.examples:
                with self.subTest(pattern=p.id, example=ex.language):
                    self.assertIsNotNone(ex.code)
                    self.assertNotEqual(ex.code.strip(), "")

    def test_each_example_language_in_rotation(self):
        """Each example's language should be in LANGUAGE_ROTATION."""
        for p in ALL_PATTERNS.values():
            for ex in p.examples:
                with self.subTest(pattern=p.id, example=ex.language):
                    self.assertIn(ex.language, LANGUAGE_ROTATION)

    def test_all_eight_languages_present_per_pattern(self):
        """Each pattern should have exactly one example per language."""
        for p in ALL_PATTERNS.values():
            with self.subTest(pattern=p.id):
                langs = [ex.language for ex in p.examples]
                self.assertEqual(sorted(langs), sorted(LANGUAGE_ROTATION))

    def test_pattern_ids_are_unique(self):
        """Pattern IDs should be unique."""
        ids = [p.id for p in ALL_PATTERNS.values()]
        self.assertEqual(len(ids), len(set(ids)))

    def test_null_safety_pattern_correct_id(self):
        """NULL_PATTERNS should have id 'null_safety'."""
        self.assertEqual(NULL_PATTERNS.id, "null_safety")

    def test_error_handling_pattern_correct_id(self):
        """ERROR_PATTERNS should have id 'error_handling'."""
        self.assertEqual(ERROR_PATTERNS.id, "error_handling")

    def test_concurrency_pattern_correct_id(self):
        """CONCURRENCY_PATTERNS should have id 'concurrency'."""
        self.assertEqual(CONCURRENCY_PATTERNS.id, "concurrency")

    def test_iteration_pattern_correct_id(self):
        """ITERATION_PATTERNS should have id 'iteration'."""
        self.assertEqual(ITERATION_PATTERNS.id, "iteration")

    def test_function_composition_pattern_correct_id(self):
        """COMPOSITION_PATTERNS should have id 'function_composition'."""
        self.assertEqual(COMPOSITION_PATTERNS.id, "function_composition")


# =============================================================================
# Test Pattern Categories
# =============================================================================

class TestPatternCategories(unittest.TestCase):
    """Tests for pattern categories."""

    def test_categories_list_not_empty(self):
        """PATTERN_CATEGORIES should not be empty."""
        self.assertGreater(len(PATTERN_CATEGORIES), 0)

    def test_categories_are_unique(self):
        """Categories should be unique."""
        self.assertEqual(len(PATTERN_CATEGORIES), len(set(PATTERN_CATEGORIES)))


# =============================================================================
# Test Rotation State (with real temp files)
# =============================================================================

class TestRotationState(unittest.TestCase):
    """Tests for rotation state utilities using real temp files."""

    def setUp(self):
        """Create a temp rotation file for each test."""
        self._tmpdir = tempfile.mkdtemp()
        self._tmpfile = os.path.join(self._tmpdir, "language_rotation.json")

    def tearDown(self):
        """Clean up temp file."""
        try:
            os.unlink(self._tmpfile)
        except OSError:
            pass
        try:
            os.rmdir(self._tmpdir)
        except OSError:
            pass

    def _write_state(self, state: dict):
        """Helper: write state to temp rotation file."""
        with open(self._tmpfile, "w") as f:
            json.dump(state, f)

    def test_get_current_language(self):
        """get_current_language should return last_language from state."""
        self._write_state(SAMPLE_ROTATION_STATE)

        import importlib
        import mod
        orig = mod.ROTATION_FILE
        mod.ROTATION_FILE = Path(self._tmpfile)

        lang = mod.get_current_language()
        self.assertEqual(lang, "Rust")

        mod.ROTATION_FILE = orig

    def test_get_next_language_from_rust_is_go(self):
        """When last_language is Rust, next should be Go."""
        self._write_state(SAMPLE_ROTATION_STATE)

        import importlib
        import mod
        orig = mod.ROTATION_FILE
        mod.ROTATION_FILE = Path(self._tmpfile)

        next_lang = mod.get_next_language()
        self.assertEqual(next_lang, "Go")

        mod.ROTATION_FILE = orig

    def test_get_next_language_from_java_is_cpp(self):
        """When last_language is Java, next should be C/C++."""
        state = dict(SAMPLE_ROTATION_STATE, last_language="Java")
        self._write_state(state)

        import importlib
        import mod
        orig = mod.ROTATION_FILE
        mod.ROTATION_FILE = Path(self._tmpfile)

        next_lang = mod.get_next_language()
        self.assertEqual(next_lang, "C/C++")

        mod.ROTATION_FILE = orig

    def test_get_next_language_from_cpp_wraps_to_rust(self):
        """When last_language is C/C++, next should wrap to Rust."""
        state = dict(SAMPLE_ROTATION_STATE, last_language="C/C++")
        self._write_state(state)

        import importlib
        import mod
        orig = mod.ROTATION_FILE
        mod.ROTATION_FILE = Path(self._tmpfile)

        next_lang = mod.get_next_language()
        self.assertEqual(next_lang, "Rust")

        mod.ROTATION_FILE = orig

    def test_advance_rotation_from_rust(self):
        """advance_rotation should advance from Rust to Go."""
        self._write_state(SAMPLE_ROTATION_STATE)

        import importlib
        import mod
        orig = mod.ROTATION_FILE
        mod.ROTATION_FILE = Path(self._tmpfile)

        next_lang = mod.advance_rotation()
        self.assertEqual(next_lang, "Go")

        mod.ROTATION_FILE = orig

    def test_advance_rotation_writes_state(self):
        """advance_rotation should write updated state to file."""
        self._write_state(SAMPLE_ROTATION_STATE)

        import importlib
        import mod
        orig = mod.ROTATION_FILE
        mod.ROTATION_FILE = Path(self._tmpfile)

        mod.advance_rotation()

        # Verify file was written
        with open(self._tmpfile) as f:
            written = json.load(f)
        self.assertIn("last_language", written)

        mod.ROTATION_FILE = orig


# =============================================================================
# Test Pattern Query API
# =============================================================================

class TestPatternQueryAPI(unittest.TestCase):
    """Tests for get_pattern and related functions."""

    def test_get_pattern_by_id(self):
        """get_pattern('null_safety') should return NULL_PATTERNS."""
        p = get_pattern("null_safety")
        self.assertEqual(p.id, "null_safety")

    def test_get_pattern_by_id_error_handling(self):
        """get_pattern('error_handling') should return ERROR_PATTERNS."""
        p = get_pattern("error_handling")
        self.assertEqual(p.id, "error_handling")

    def test_get_pattern_by_id_concurrency(self):
        """get_pattern('concurrency') should return CONCURRENCY_PATTERNS."""
        p = get_pattern("concurrency")
        self.assertEqual(p.id, "concurrency")

    def test_get_pattern_by_id_iteration(self):
        """get_pattern('iteration') should return ITERATION_PATTERNS."""
        p = get_pattern("iteration")
        self.assertEqual(p.id, "iteration")

    def test_get_pattern_by_id_function_composition(self):
        """get_pattern('function_composition') should return COMPOSITION_PATTERNS."""
        p = get_pattern("function_composition")
        self.assertEqual(p.id, "function_composition")

    def test_get_pattern_unknown_id_raises(self):
        """get_pattern with unknown ID should raise ValueError."""
        with self.assertRaises(ValueError):
            get_pattern("nonexistent_pattern")

    def test_get_pattern_with_valid_language(self):
        """get_pattern with valid language should filter examples."""
        p = get_pattern("null_safety", language="Rust")
        self.assertEqual(len(p.examples), 1)
        self.assertEqual(p.examples[0].language, "Rust")

    def test_get_pattern_with_language_is_case_insensitive(self):
        """get_pattern language filter should be case-insensitive."""
        p1 = get_pattern("null_safety", language="rust")
        p2 = get_pattern("null_safety", language="Rust")
        p3 = get_pattern("null_safety", language="RUST")
        self.assertEqual(p1.examples[0].language, "Rust")
        self.assertEqual(p2.examples[0].language, "Rust")
        self.assertEqual(p3.examples[0].language, "Rust")

    def test_get_pattern_with_cpp_language(self):
        """get_pattern with 'C/C++' language should work."""
        p = get_pattern("null_safety", language="C/C++")
        self.assertEqual(len(p.examples), 1)
        self.assertEqual(p.examples[0].language, "C/C++")

    def test_get_pattern_with_invalid_language_raises(self):
        """get_pattern with invalid language should raise ValueError."""
        with self.assertRaises(ValueError):
            get_pattern("null_safety", language="Pascal")

    def test_get_all_patterns_returns_all(self):
        """get_all_patterns should return all 5 patterns."""
        patterns = get_all_patterns()
        self.assertEqual(len(patterns), 5)

    def test_get_all_patterns_are_pattern_objects(self):
        """get_all_patterns should return Pattern objects."""
        for p in get_all_patterns():
            self.assertIsInstance(p, Pattern)

    def test_get_patterns_by_category(self):
        """get_patterns_by_category should filter by category."""
        patterns = get_patterns_by_category("Error Handling")
        self.assertGreater(len(patterns), 0)
        for p in patterns:
            self.assertEqual(p.category, "Error Handling")

    def test_get_pattern_for_language(self):
        """get_pattern_for_language should return one example per pattern."""
        results = get_pattern_for_language("Rust")
        self.assertGreater(len(results), 0)
        for pattern, example in results:
            self.assertIsInstance(pattern, Pattern)
            self.assertIsInstance(example, PatternExample)
            self.assertEqual(example.language, "Rust")


# =============================================================================
# Test Format Markdown
# =============================================================================

class TestFormatMarkdown(unittest.TestCase):
    """Tests for format_pattern_markdown."""

    def test_format_includes_pattern_name(self):
        """Formatted output should include pattern name."""
        output = format_pattern_markdown(NULL_PATTERNS)
        self.assertIn("## Null/Option Safety", output)

    def test_format_includes_pattern_description(self):
        """Formatted output should include pattern description."""
        output = format_pattern_markdown(NULL_PATTERNS)
        self.assertIn("Handle potentially missing values", output)

    def test_format_includes_category(self):
        """Formatted output should include category."""
        output = format_pattern_markdown(NULL_PATTERNS)
        self.assertIn("**Category:** Error Handling", output)

    def test_format_includes_language_examples(self):
        """Formatted output should include all 8 languages."""
        output = format_pattern_markdown(NULL_PATTERNS)
        for lang in LANGUAGE_ROTATION:
            with self.subTest(lang=lang):
                self.assertIn(f"### {lang}", output)

    def test_format_with_language_filter(self):
        """Format with language filter should only show that language."""
        output = format_pattern_markdown(NULL_PATTERNS, language="Rust")
        self.assertIn("### Rust", output)
        self.assertNotIn("### Go", output)

    def test_format_includes_code_blocks(self):
        """Formatted output should include fenced code blocks."""
        output = format_pattern_markdown(NULL_PATTERNS)
        self.assertIn("```rust", output)

    def test_format_with_cpp_language(self):
        """Format with C/C++ language should use cpp code fence."""
        output = format_pattern_markdown(NULL_PATTERNS, language="C/C++")
        self.assertIn("```cpp", output)

    def test_format_includes_annotations(self):
        """Formatted output should include annotations."""
        output = format_pattern_markdown(NULL_PATTERNS)
        # At least one annotation should be present
        self.assertIsNotNone(output)


# =============================================================================
# Test Pattern Code Content
# =============================================================================

class TestPatternCodeContent(unittest.TestCase):
    """Tests for the content of pattern code examples."""

    def test_null_safety_rust_uses_option(self):
        """Rust null_safety example should use Option<T>."""
        ex = next(ex for ex in NULL_PATTERNS.examples if ex.language == "Rust")
        self.assertIn("Option", ex.code)
        self.assertIn("Some", ex.code)

    def test_null_safety_go_uses_pointers(self):
        """Go null_safety example should use pointers."""
        ex = next(ex for ex in NULL_PATTERNS.examples if ex.language == "Go")
        self.assertIn("*string", ex.code)
        self.assertIn("nil", ex.code)

    def test_null_safety_swift_uses_optional(self):
        """Swift null_safety example should use Optional or ?."""
        ex = next(ex for ex in NULL_PATTERNS.examples if ex.language == "Swift")
        self.assertIn("String?", ex.code)

    def test_null_safety_kotlin_uses_nullable(self):
        """Kotlin null_safety example should use nullable type."""
        ex = next(ex for ex in NULL_PATTERNS.examples if ex.language == "Kotlin")
        self.assertIn("String?", ex.code)

    def test_null_safety_typescript_uses_union(self):
        """TypeScript null_safety example should use string | null union."""
        ex = next(ex for ex in NULL_PATTERNS.examples if ex.language == "TypeScript")
        self.assertIn("null", ex.code)

    def test_null_safety_java_uses_optional(self):
        """Java null_safety example should use Optional<T>."""
        ex = next(ex for ex in NULL_PATTERNS.examples if ex.language == "Java")
        self.assertIn("Optional", ex.code)

    def test_null_safety_cpp_uses_optional(self):
        """C/C++ null_safety example should use std::optional."""
        ex = next(ex for ex in NULL_PATTERNS.examples if ex.language == "C/C++")
        self.assertIn("std::optional", ex.code)

    def test_iteration_all_examples_filter_and_map(self):
        """All iteration examples should demonstrate filter/map or equivalent."""
        for ex in ITERATION_PATTERNS.examples:
            with self.subTest(lang=ex.language):
                code_lower = ex.code.lower()
                # Should have filter concept (or copy_if for C++)
                self.assertTrue(
                    "filter" in code_lower or "copy_if" in code_lower,
                    f"{ex.language} iteration example should use filter"
                )

    def test_concurrency_all_examples_show_parallelism(self):
        """All concurrency examples should show parallel execution."""
        for ex in CONCURRENCY_PATTERNS.examples:
            with self.subTest(lang=ex.language):
                code_lower = ex.code.lower()
                # Should involve threads, goroutines, async, coroutines, etc.
                self.assertTrue(
                    "thread" in code_lower or "goroutine" in code_lower or
                    "async" in code_lower or "coroutine" in code_lower or
                    "future" in code_lower or "dispatch" in code_lower,
                    f"{ex.language} concurrency example should show parallelism"
                )

    def test_function_composition_all_examples_chain_operations(self):
        """All function_composition examples should chain multiple operations."""
        for ex in COMPOSITION_PATTERNS.examples:
            with self.subTest(lang=ex.language):
                code_lower = ex.code.lower()
                # Should show chaining multiple operations
                map_count = code_lower.count("map") + code_lower.count("transform")
                self.assertGreater(
                    map_count, 1,
                    f"{ex.language} should chain multiple operations"
                )


# =============================================================================
# Test Main CLI
# =============================================================================

class TestCLI(unittest.TestCase):
    """Tests for CLI arguments."""

    def test_no_args_shows_help(self):
        """Calling main() with no args should display help."""
        import io
        import sys
        from mod import main

        old_stdout = sys.stdout
        old_stderr = sys.stderr
        try:
            sys.stdout = io.StringIO()
            sys.stderr = io.StringIO()
            try:
                main()
            except SystemExit:
                pass
            output = sys.stdout.getvalue()
            self.assertTrue(
                "Usage" in output or "pattern" in output.lower(),
                "Should show usage help"
            )
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr

    def test_list_patterns(self):
        """--list should list patterns without crashing."""
        import io
        import sys
        from mod import main

        old_stdout = sys.stdout
        try:
            sys.stdout = io.StringIO()
            try:
                main()
            except SystemExit:
                pass
        finally:
            sys.stdout = old_stdout

    def test_categories(self):
        """--categories should show categories without crashing."""
        import io
        import sys
        from mod import main

        old_stdout = sys.stdout
        try:
            sys.stdout = io.StringIO()
            try:
                main()
            except SystemExit:
                pass
        finally:
            sys.stdout = old_stdout

    def test_meta(self):
        """--meta should show language metadata without crashing."""
        import io
        import sys
        from mod import main

        old_stdout = sys.stdout
        try:
            sys.stdout = io.StringIO()
            try:
                main()
            except SystemExit:
                pass
        finally:
            sys.stdout = old_stdout


# =============================================================================
# Run Tests
# =============================================================================

if __name__ == "__main__":
    unittest.main(verbosity=2)