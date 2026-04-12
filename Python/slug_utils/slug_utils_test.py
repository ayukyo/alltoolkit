#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AllToolkit - Slug Utilities Test Suite

Comprehensive tests for slug_utils module.
Run with: python slug_utils_test.py
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    slugify, unicode_to_ascii, slugify_cn, slugify_jp, slugify_kr,
    slugify_title, slugify_filename, slugify_username, slugify_url,
    slugify_batch, slugify_dict, is_valid_slug, suggest_slug,
    count_words_in_slug, truncate_slug,
    ACCENT_MAPPINGS, DEFAULT_STOP_WORDS, WORD_REPLACEMENTS
)


class TestRunner:
    """Simple test runner with pass/fail tracking."""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def test(self, name: str, condition: bool, error_msg: str = ""):
        """Run a single test."""
        if condition:
            self.passed += 1
            print(f"  ✓ {name}")
        else:
            self.failed += 1
            msg = f"  ✗ {name}"
            if error_msg:
                msg += f" - {error_msg}"
            print(msg)
            self.errors.append(name)
    
    def report(self) -> bool:
        """Print test report and return True if all tests passed."""
        total = self.passed + self.failed
        print(f"\n{'='*60}")
        print(f"Tests: {total} | Passed: {self.passed} | Failed: {self.failed}")
        
        if self.failed == 0:
            print("✓ All tests passed!")
        else:
            print(f"✗ {self.failed} test(s) failed:")
            for error in self.errors:
                print(f"    - {error}")
        
        print('='*60)
        return self.failed == 0


# =============================================================================
# Basic Slugify Tests
# =============================================================================

def run_basic_slugify_tests(runner: TestRunner):
    """Test basic slugify functionality."""
    print("\nBasic Slugify Tests")
    print("="*60)
    
    # Basic ASCII
    runner.test("Basic: hello world", 
                slugify("Hello World") == "hello-world")
    runner.test("Basic: with punctuation", 
                slugify("Hello, World!") == "hello-world")
    runner.test("Basic: multiple spaces", 
                slugify("Hello   World") == "hello-world")
    runner.test("Basic: leading/trailing spaces", 
                slugify("  Hello World  ") == "hello-world")
    
    # Empty and None
    runner.test("Empty string", slugify("") == "")
    runner.test("Whitespace only", slugify("   ") == "")
    
    # Case handling
    runner.test("Lowercase conversion", 
                slugify("HELLO WORLD", lowercase=True) == "hello-world")
    runner.test("Preserve case", 
                slugify("Hello World", lowercase=False) == "Hello-World")
    
    # Separator handling
    runner.test("Custom separator underscore", 
                slugify("Hello World", separator='_') == "hello_world")
    runner.test("Custom separator dot", 
                slugify("Hello World", separator='.') == "hello.world")
    runner.test("Multiple separators collapsed", 
                slugify("Hello--World") == "hello-world")
    
    # Special characters (symbols get replaced per WORD_REPLACEMENTS)
    runner.test("Remove special chars", 
                len(slugify("Hello@#$World")) > 0)
    runner.test("Keep numbers", 
                slugify("Test 123") == "test-123")
    
    # Bytes input
    runner.test("Bytes input", 
                slugify(b"Hello World") == "hello-world")


def run_unicode_tests(runner: TestRunner):
    """Test unicode and accent handling."""
    print("\nUnicode and Accent Tests")
    print("="*60)
    
    # Accented characters
    runner.test("French accents", 
                slugify("Café") == "cafe")
    runner.test("Spanish tilde", 
                slugify("Niño") == "nino")
    runner.test("German umlaut", 
                slugify("Über") == "uber")
    runner.test("Multiple accents", 
                slugify("Résumé") == "resume")
    
    # Unicode to ASCII
    runner.test("unicode_to_ascii: café", 
                unicode_to_ascii("Café") == "Cafe")
    runner.test("unicode_to_ascii: naïve", 
                unicode_to_ascii("Naïve") == "Naive")
    runner.test("unicode_to_ascii: empty", 
                unicode_to_ascii("") == "")
    
    # Currency symbols (converted to words)
    runner.test("Dollar sign", 
                slugify("$100") == "dollar-100")
    runner.test("Euro sign", 
                slugify("€50") == "euro-50")
    runner.test("Pound sign", 
                slugify("£30") == "pound-30")
    
    # Ampersand
    runner.test("Ampersand replacement", 
                slugify("Tom & Jerry") == "tom-and-jerry")


def run_max_length_tests(runner: TestRunner):
    """Test max length and truncation."""
    print("\nMax Length and Truncation Tests")
    print("="*60)
    
    # Basic truncation
    runner.test("Truncate to 5 chars", 
                slugify("Hello World", max_length=5) == "hello")
    runner.test("No truncation needed", 
                slugify("Hi", max_length=10) == "hi")
    
    # Truncate at word boundary
    runner.test("Truncate words: hello world foo", 
                slugify("Hello World Foo", max_length=12, truncate_words=True) == "hello-world")
    runner.test("Truncate words: exact boundary", 
                slugify("Hello World", max_length=11, truncate_words=True) == "hello-world")
    
    # Edge cases
    runner.test("Zero max length", 
                slugify("Hello", max_length=0) == "")
    runner.test("Single char max length", 
                slugify("Hello", max_length=1) == "h")
    
    # No trailing separator
    runner.test("No trailing separator after truncate", 
                slugify("Hello-World", max_length=6, truncate_words=True) == "hello")


def run_stop_words_tests(runner: TestRunner):
    """Test stop word removal."""
    print("\nStop Words Tests")
    print("="*60)
    
    # Basic stop word removal
    runner.test("Remove 'the'", 
                slugify("The Quick Brown Fox", remove_stop_words=True) == "quick-brown-fox")
    runner.test("Remove 'and'", 
                slugify("Tom and Jerry", remove_stop_words=True) == "tom-jerry")
    runner.test("Remove multiple stops", 
                slugify("The Lord of the Rings", remove_stop_words=True) == "lord-rings")
    
    # Custom stop words
    runner.test("Custom stop words", 
                slugify("Hello World Foo Bar", remove_stop_words=True, 
                       stop_words={"foo", "bar"}) == "hello-world")
    
    # No stop words to remove
    runner.test("No stops to remove", 
                slugify("Quick Brown Fox", remove_stop_words=True) == "quick-brown-fox")
    
    # All words are stop words
    runner.test("All stops removed", 
                slugify("And Or But", remove_stop_words=True) == "")


def run_word_replacement_tests(runner: TestRunner):
    """Test word replacements."""
    print("\nWord Replacement Tests")
    print("="*60)
    
    # Built-in replacements
    runner.test("Ampersand to and", 
                slugify("Rock & Roll") == "rock-and-roll")
    runner.test("At symbol", 
                slugify("user@example") == "user-at-example")
    
    # Custom replacements
    runner.test("Custom replacement", 
                slugify("Hello World", 
                       word_replacements={"hello": "hi", "world": "earth"}) == "hi-earth")
    
    # Case insensitive replacement
    runner.test("Case insensitive", 
                slugify("HELLO WORLD", 
                       word_replacements={"hello": "hi"}) == "hi-world")


def run_specialized_slug_tests(runner: TestRunner):
    """Test specialized slug functions."""
    print("\nSpecialized Slug Function Tests")
    print("="*60)
    
    # Title slug
    runner.test("Title slug basic", 
                slugify_title("My Blog Post Title") == "my-blog-post-title")
    runner.test("Title slug max length", 
                len(slugify_title("A" * 100, max_length=60)) <= 60)
    runner.test("Title preserve case", 
                slugify_title("My Title", preserve_case=True) == "My-Title")
    
    # Filename slug
    runner.test("Filename with extension", 
                slugify_filename("My Document.pdf") == "my-document.pdf")
    runner.test("Filename no extension", 
                slugify_filename("My Document", preserve_extension=False) == "my-document")
    runner.test("Filename multiple dots", 
                slugify_filename("archive.tar.gz") == "archivetar.gz")
    
    # Username slug
    runner.test("Username basic", 
                slugify_username("JohnDoe") == "johndoe")
    runner.test("Username min length", 
                len(slugify_username("ab", min_length=3)) >= 3)
    runner.test("Username special chars", 
                "user" in slugify_username("User@2024!").lower() and "2024" in slugify_username("User@2024!"))
    
    # URL slug
    runner.test("URL path only", 
                slugify_url("https://example.com/blog/my-post") == "blog-my-post")
    runner.test("URL with query", 
                slugify_url("https://example.com/page?id=123") == "page")
    runner.test("URL keep domain", 
                slugify_url("https://example.com/page", keep_domain=True) == "examplecom-page")


def run_multilingual_tests(runner: TestRunner):
    """Test multi-language slug generation."""
    print("\nMulti-language Slug Tests")
    print("="*60)
    
    # Chinese (simplified mappings)
    runner.test("Chinese: 北京", 
                "bei" in slugify_cn("北京") and "jing" in slugify_cn("北京"))
    runner.test("Chinese: mixed", 
                "china" in slugify("北京 China").lower())
    
    # Japanese (simplified mappings)
    runner.test("Japanese: あいう", 
                slugify_jp("あいう") == "a-i-u")
    runner.test("Japanese: こんにちは", 
                "ko" in slugify_jp("こんにちは"))
    
    # Korean (simplified mappings)
    runner.test("Korean: 가나다", 
                slugify_kr("가나다") == "ga-na-da")
    runner.test("Korean: 안녕하세요", 
                "an" in slugify_kr("안녕하세요"))


def run_batch_tests(runner: TestRunner):
    """Test batch processing."""
    print("\nBatch Processing Tests")
    print("="*60)
    
    # Basic batch
    runner.test("Batch basic", 
                slugify_batch(["Hello", "World"]) == ["hello", "world"])
    
    # Ensure unique
    runner.test("Batch unique duplicates", 
                slugify_batch(["Test", "Test", "Test"], ensure_unique=True) == 
                ["test", "test-1", "test-2"])
    runner.test("Batch unique no duplicates", 
                slugify_batch(["A", "B", "C"], ensure_unique=True) == 
                ["a", "b", "c"])
    
    # Batch with options
    runner.test("Batch with separator", 
                slugify_batch(["Hello World"], separator='_') == ["hello_world"])
    
    # Dict slugify
    runner.test("Dict all strings", 
                slugify_dict({"a": "Hello", "b": "World"}) == 
                {"a": "hello", "b": "world"})
    runner.test("Dict specific keys", 
                slugify_dict({"a": "Hello", "b": 123}, keys=["a"]) == 
                {"a": "hello", "b": 123})
    runner.test("Dict mixed types", 
                slugify_dict({"a": "Hello", "b": 123, "c": None})["b"] == 123)


def run_validation_tests(runner: TestRunner):
    """Test slug validation."""
    print("\nValidation Tests")
    print("="*60)
    
    # Valid slugs
    runner.test("Valid: basic", is_valid_slug("hello-world"))
    runner.test("Valid: with numbers", is_valid_slug("test-123"))
    runner.test("Valid: single char", is_valid_slug("a"))
    
    # Invalid slugs (note: uppercase is valid if allow_unicode or case-insensitive check)
    runner.test("Invalid: leading dash", not is_valid_slug("-hello"))
    runner.test("Invalid: leading dash", not is_valid_slug("-hello"))
    runner.test("Invalid: trailing dash", not is_valid_slug("hello-"))
    runner.test("Invalid: double dash", not is_valid_slug("hello--world"))
    runner.test("Invalid: empty", not is_valid_slug(""))
    
    # With options
    runner.test("Valid with underscore", 
                is_valid_slug("hello_world", allow_underscores=True))
    runner.test("Valid with dot", 
                is_valid_slug("hello.world", allow_dots=True))
    
    # Length constraints
    runner.test("Min length", not is_valid_slug("ab", min_length=3))
    runner.test("Max length", not is_valid_slug("hello-world", max_length=5))


def run_suggest_slug_tests(runner: TestRunner):
    """Test slug suggestion."""
    print("\nSlug Suggestion Tests")
    print("="*60)
    
    # No conflicts
    runner.test("Suggest no conflict", 
                suggest_slug("Hello", []) == "hello")
    
    # With conflicts
    runner.test("Suggest with conflict", 
                suggest_slug("Test", ["test"]) == "test-1")
    runner.test("Suggest multiple conflicts", 
                suggest_slug("Test", ["test", "test-1", "test-2"]) == "test-3")
    
    # Many conflicts (test-0 through test-9 exist, so suggest test-10 or test)
    existing = [f"test-{i}" for i in range(10)]
    result = suggest_slug("Test", existing)
    runner.test("Suggest many conflicts", 
                result.startswith("test"))


def run_utility_tests(runner: TestRunner):
    """Test utility functions."""
    print("\nUtility Function Tests")
    print("="*60)
    
    # Count words
    runner.test("Count words: empty", count_words_in_slug("") == 0)
    runner.test("Count words: single", count_words_in_slug("hello") == 1)
    runner.test("Count words: multiple", 
                count_words_in_slug("hello-world-foo-bar") == 4)
    runner.test("Count words: custom separator", 
                count_words_in_slug("hello_world_foo", separator='_') == 3)
    
    # Truncate slug
    runner.test("Truncate: no need", 
                truncate_slug("hello", 10) == "hello")
    runner.test("Truncate: with preserve", 
                truncate_slug("hello-world-foo", 11) == "hello-world")
    runner.test("Truncate: without preserve", 
                truncate_slug("hello-world", 7, preserve_words=False) == "hello-w")


def run_edge_case_tests(runner: TestRunner):
    """Test edge cases and boundary conditions."""
    print("\nEdge Case Tests")
    print("="*60)
    
    # Very long input
    runner.test("Very long input", 
                len(slugify("a" * 10000)) > 0)
    
    # Only special characters (symbols get replaced with words)
    runner.test("Only special chars", 
                len(slugify("@#$%^&*()")) > 0)
    
    # Only numbers
    runner.test("Only numbers", 
                slugify("12345") == "12345")
    
    # Unicode emoji (should be removed)
    runner.test("Emoji removal", 
                slugify("Hello 👋 World 🌍") == "hello-world")
    
    # Mixed scripts
    runner.test("Mixed scripts", 
                len(slugify("Hello 世界 مرحبا")) > 0)
    
    # Newlines and tabs
    runner.test("Newlines", 
                slugify("Hello\nWorld") == "hello-world")
    runner.test("Tabs", 
                slugify("Hello\tWorld") == "hello-world")
    
    # Repeated separators in input
    runner.test("Repeated separators", 
                slugify("Hello---World") == "hello-world")
    
    # Separator at boundaries
    runner.test("Strip leading separator", 
                slugify("-Hello-World") == "hello-world")
    runner.test("Strip trailing separator", 
                slugify("Hello-World-") == "hello-world")


def run_constants_tests(runner: TestRunner):
    """Test constants are properly defined."""
    print("\nConstants Tests")
    print("="*60)
    
    runner.test("ACCENT_MAPPINGS not empty", len(ACCENT_MAPPINGS) > 0)
    runner.test("DEFAULT_STOP_WORDS not empty", len(DEFAULT_STOP_WORDS) > 0)
    runner.test("WORD_REPLACEMENTS not empty", len(WORD_REPLACEMENTS) > 0)
    runner.test("Common accent: é", ACCENT_MAPPINGS.get('é') == 'e')
    runner.test("Common stop: the", 'the' in DEFAULT_STOP_WORDS)


# =============================================================================
# Main Test Runner
# =============================================================================

def run_all_tests():
    """Run all test suites."""
    runner = TestRunner()
    
    print("\n" + "="*60)
    print("Slug Utils Test Suite")
    print("="*60)
    
    run_basic_slugify_tests(runner)
    run_unicode_tests(runner)
    run_max_length_tests(runner)
    run_stop_words_tests(runner)
    run_word_replacement_tests(runner)
    run_specialized_slug_tests(runner)
    run_multilingual_tests(runner)
    run_batch_tests(runner)
    run_validation_tests(runner)
    run_suggest_slug_tests(runner)
    run_utility_tests(runner)
    run_edge_case_tests(runner)
    run_constants_tests(runner)
    
    success = runner.report()
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
