"""Tests for Polyglot Metamorphosis."""

import json
import sys
import tempfile
import os
from pathlib import Path

import pytest

from metamorphosis import (
    LANGUAGE_CYCLE,
    LANGUAGE_TRAITS,
    advance_rotation,
    detect_language,
    extract_code_concepts,
    generate_metamorphic_mapping,
    get_current_language,
    load_rotation_config,
    save_rotation_config,
    transform_example,
)


# ── Fixtures ────────────────────────────────────────────────────────────────

@pytest.fixture
def rotation_config():
    """Temp config file with known state. Created fresh for each test.
    Language order: Rust(0) Go(1) Swift(2) Kotlin(3) TypeScript(4) JavaScript(5) Java(6) C/C++(7)
    """
    data = {
        "languages": ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"],
        "current_index": 3,  # Kotlin
        "last_language": "Kotlin",
        "updated_at": "2026-06-19T00:00:00+00:00",
    }
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(data, f)
        f.flush()
        yield f.name
    os.unlink(f.name)


@pytest.fixture
def rotation_config_wrap():
    """Temp config where index is at end (tests wraparound)."""
    data = {
        "languages": ["Rust", "Go", "Swift", "Kotlin", "TypeScript", "JavaScript", "Java", "C/C++"],
        "current_index": 7,
        "last_language": "C/C++",
        "updated_at": "2026-06-19T00:00:00+00:00",
    }
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(data, f)
        f.flush()
        yield f.name
    os.unlink(f.name)


# ── Rotation tests ───────────────────────────────────────────────────────────

class TestRotation:
    def test_load_rotation_config(self, rotation_config):
        data = load_rotation_config(rotation_config)
        assert data["languages"] == LANGUAGE_CYCLE
        assert data["current_index"] == 3  # Kotlin

    def test_save_rotation_config(self, rotation_config):
        data = load_rotation_config(rotation_config)
        data["current_index"] = 5
        save_rotation_config(rotation_config, data)
        reloaded = load_rotation_config(rotation_config)
        assert reloaded["current_index"] == 5

    def test_advance_rotation_increments_index(self, rotation_config):
        # At index 3 (Kotlin), advancing should go to index 4 (TypeScript)
        result = advance_rotation(rotation_config)
        assert result["previous_language"] == "Kotlin"
        assert result["current_language"] == "TypeScript"
        assert result["current_index"] == 4

    def test_advance_rotation_wraps_around(self, rotation_config_wrap):
        result = advance_rotation(rotation_config_wrap)
        assert result["previous_language"] == "C/C++"
        assert result["current_language"] == "Rust"
        assert result["current_index"] == 0

    def test_get_current_language_does_not_advance(self, rotation_config):
        # get_current_language should NOT modify state
        lang1 = get_current_language(rotation_config)
        lang2 = get_current_language(rotation_config)
        assert lang1 == lang2 == "Kotlin"  # index 3

    def test_get_current_language_matches_index(self, rotation_config):
        # Fresh config at index 3 should be Kotlin
        assert get_current_language(rotation_config) == "Kotlin"

    def test_updated_at_is_set(self, rotation_config):
        advance_rotation(rotation_config)
        data = load_rotation_config(rotation_config)
        assert "updated_at" in data
        assert "T" in data["updated_at"]


# ── Language detection ──────────────────────────────────────────────────────

class TestDetectLanguage:
    def test_detect_rust(self):
        code = "fn main() -> () { let mut x = 5; }"
        assert detect_language(code) == "Rust"

    def test_detect_go(self):
        code = "package main\n\nfunc main() { fmt.Println('hello') }"
        assert detect_language(code) == "Go"

    def test_detect_swift(self):
        code = "func greet() { guard let x = y else { return } }"
        assert detect_language(code) == "Swift"

    def test_detect_kotlin(self):
        code = "fun main() { val x = 1 }"
        assert detect_language(code) == "Kotlin"

    def test_detect_typescript(self):
        code = "interface User { name: string; }\nfunction greet(): string { return 'hi'; }"
        assert detect_language(code) == "TypeScript"

    def test_detect_javascript(self):
        code = "function greet() { console.log('hi'); }"
        assert detect_language(code) == "JavaScript"

    def test_detect_java(self):
        code = "public static void main(String[] args) { System.out.println('hi'); }"
        assert detect_language(code) == "Java"

    def test_detect_cpp(self):
        code = "#include <iostream>"
        assert detect_language(code) == "C/C++"

    def test_detect_unknown_returns_none(self):
        code = "BEGIN { puts 'hello' } END { }"
        assert detect_language(code) is None


# ── Concept extraction ──────────────────────────────────────────────────────

class TestExtractConcepts:
    def test_extract_functions(self):
        code = "fn foo() {} fn bar() {}"
        concepts = extract_code_concepts(code, "Rust")
        assert "foo" in concepts["functions"]
        assert "bar" in concepts["functions"]

    def test_extract_variables(self):
        code = "let x = 1; let y = 2;"
        concepts = extract_code_concepts(code, "Rust")
        assert "x" in concepts["variables"]
        assert "y" in concepts["variables"]

    def test_detect_loops(self):
        # for loop with parentheses pattern
        code = "for (int i = 0; i < 10; i++) { }"
        concepts = extract_code_concepts(code, "Java")
        assert concepts["loops"] is True

    def test_detect_loops_false(self):
        code = "fn foo() { }"
        concepts = extract_code_concepts(code, "Rust")
        assert concepts["loops"] is False

    def test_detect_async(self):
        code = "async fn fetch() { }"
        concepts = extract_code_concepts(code, "Rust")
        assert concepts["async"] is True

    def test_detect_error_handling(self):
        code = "fn fallible() -> Result<T, E> { }"
        concepts = extract_code_concepts(code, "Rust")
        assert concepts["error_handling"] is True


# ── Metamorphic mapping ─────────────────────────────────────────────────────

class TestMetamorphicMapping:
    def test_mapping_contains_required_keys(self):
        concepts = {"functions": ["foo"], "variables": ["x"]}
        mapping = generate_metamorphic_mapping("JavaScript", "Rust", concepts)
        assert mapping["source_language"] == "JavaScript"
        assert mapping["target_language"] == "Rust"
        assert "source_traits" in mapping
        assert "target_traits" in mapping
        assert "paradigm_shifts" in mapping
        assert "extracted_concepts" in mapping
        assert "keywords_to_learn" in mapping

    def test_keywords_to_learn_are_target_specific(self):
        mapping = generate_metamorphic_mapping("JavaScript", "Rust", {})
        rust_keywords = set(LANGUAGE_TRAITS["Rust"]["paradigm_keywords"])
        assert any(kw in rust_keywords for kw in mapping["keywords_to_learn"])

    def test_paradigm_shifts_js_to_rust(self):
        mapping = generate_metamorphic_mapping("JavaScript", "Rust", {})
        shifts = mapping["paradigm_shifts"]
        assert any("ownership" in s.lower() or "borrow" in s.lower() for s in shifts)


# ── Transform examples ──────────────────────────────────────────────────────

class TestTransformExample:
    def test_example_js_to_rust(self):
        result = transform_example("JavaScript", "Rust")
        assert "Rust" in result
        assert "//" in result

    def test_example_rust_to_js(self):
        result = transform_example("Rust", "JavaScript")
        assert "JavaScript" in result

    def test_example_go_to_kotlin(self):
        result = transform_example("Go", "Kotlin")
        assert "Kotlin" in result

    def test_example_unknown_pair(self):
        result = transform_example("Python", "Zig")
        assert "Zig" in result


# ── Language traits ──────────────────────────────────────────────────────────

class TestLanguageTraits:
    def test_all_cycle_languages_have_traits(self):
        for lang in LANGUAGE_CYCLE:
            assert lang in LANGUAGE_TRAITS
            traits = LANGUAGE_TRAITS[lang]
            assert "paradigm" in traits
            assert "syntax" in traits
            assert "paradigm_keywords" in traits
            assert len(traits["paradigm_keywords"]) >= 3

    def test_cycle_length(self):
        assert len(LANGUAGE_CYCLE) == 8
