"""
AllToolkit - Python Emoji Utilities Test Suite

Comprehensive test suite for emoji_utils module.
Covers normal scenarios, edge cases, and error conditions.

Run: python emoji_utils_test.py
"""

import sys
import os
from typing import Any

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from emoji_utils.mod import (
    EmojiUtils,
    EmojiCategory,
    EmojiInfo,
    EmojiAnalysis,
    extract_emojis,
    count_emojis,
    get_unique_emojis,
    get_emoji_counts,
    remove_emojis,
    replace_emojis,
    has_emoji,
    is_emoji,
    analyze,
    to_unicode_escape,
    from_unicode_escape,
    strip_skin_tone,
    emoji_to_text,
    text_to_emoji,
    filter_by_category,
    get_emoji_positions,
    reverse,
)


class TestResult:
    """Simple test result tracker."""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def add_pass(self, name: str):
        self.passed += 1
        print(f"  ✓ {name}")
    
    def add_fail(self, name: str, expected: Any, actual: Any):
        self.failed += 1
        self.errors.append((name, expected, actual))
        print(f"  ✗ {name}")
        print(f"    Expected: {expected}")
        print(f"    Actual: {actual}")
    
    def summary(self):
        total = self.passed + self.failed
        print(f"\n{'='*60}")
        print(f"Test Results: {self.passed}/{total} passed")
        if self.failed > 0:
            print(f"Failed: {self.failed}")
            print(f"\nFailures:")
            for name, expected, actual in self.errors:
                print(f"  - {name}: expected {expected}, got {actual}")
        else:
            print("All tests passed! ✓")
        print(f"{'='*60}")
        return self.failed == 0


def run_tests():
    """Run all tests."""
    result = TestResult()
    utils = EmojiUtils()
    
    print("=" * 60)
    print("Emoji Utils Test Suite")
    print("=" * 60)
    
    # ===== Extraction Tests =====
    print("\n[1] Extraction Tests")
    print("-" * 40)
    
    # Test basic extraction
    test_name = "extract_basic"
    text = "Hello 👋 World 🌍!"
    expected = ['👋', '🌍']
    actual = utils.extract_emojis(text)
    if actual == expected:
        result.add_pass(test_name)
    else:
        result.add_fail(test_name, expected, actual)
    
    # Test empty string
    test_name = "extract_empty"
    expected = []
    actual = utils.extract_emojis("")
    if actual == expected:
        result.add_pass(test_name)
    else:
        result.add_fail(test_name, expected, actual)
    
    # Test no emojis
    test_name = "extract_no_emoji"
    text = "Hello World!"
    expected = []
    actual = utils.extract_emojis(text)
    if actual == expected:
        result.add_pass(test_name)
    else:
        result.add_fail(test_name, expected, actual)
    
    # Test multiple same emojis
    test_name = "extract_multiple_same"
    text = "😀😃😄😀😃"
    expected = ['😀', '😃', '😄', '😀', '😃']
    actual = utils.extract_emojis(text)
    if actual == expected:
        result.add_pass(test_name)
    else:
        result.add_fail(test_name, expected, actual)
    
    # Test complex emoji (flag)
    test_name = "extract_flag_emoji"
    text = "🇺🇸"
    actual = utils.extract_emojis(text)
    if len(actual) > 0 and '🇺' in text:
        result.add_pass(test_name)
    else:
        result.add_fail(test_name, "flag emoji detected", actual)
    
    # Test skin tone emoji
    test_name = "extract_skin_tone"
    text = "👋🏽"
    actual = utils.extract_emojis(text)
    if len(actual) > 0:
        result.add_pass(test_name)
    else:
        result.add_fail(test_name, "skin tone emoji detected", actual)
    
    # ===== Counting Tests =====
    print("\n[2] Counting Tests")
    print("-" * 40)
    
    # Test basic count
    test_name = "count_basic"
    text = "😀😃😄"
    expected = 3
    actual = utils.count_emojis(text)
    if actual == expected:
        result.add_pass(test_name)
    else:
        result.add_fail(test_name, expected, actual)
    
    # Test count empty
    test_name = "count_empty"
    expected = 0
    actual = utils.count_emojis("")
    if actual == expected:
        result.add_pass(test_name)
    else:
        result.add_fail(test_name, expected, actual)
    
    # Test unique emojis
    test_name = "unique_emojis"
    text = "😀😃😀😄😃"
    expected = {'😀', '😃', '😄'}
    actual = utils.get_unique_emojis(text)
    if actual == expected:
        result.add_pass(test_name)
    else:
        result.add_fail(test_name, expected, actual)
    
    # Test emoji counts
    test_name = "emoji_counts"
    text = "😀😃😀"
    expected = {'😀': 2, '😃': 1}
    actual = utils.get_emoji_counts(text)
    if actual == expected:
        result.add_pass(test_name)
    else:
        result.add_fail(test_name, expected, actual)
    
    # ===== Removal Tests =====
    print("\n[3] Removal Tests")
    print("-" * 40)
    
    # Test remove emojis
    test_name = "remove_emojis"
    text = "Hello 👋 World 🌍!"
    expected = "Hello World!"
    actual = utils.remove_emojis(text)
    if actual == expected:
        result.add_pass(test_name)
    else:
        result.add_fail(test_name, expected, actual)
    
    # Test remove all emojis
    test_name = "remove_all_emoji"
    text = "😀😃😄"
    expected = ""
    actual = utils.remove_emojis(text)
    if actual == expected:
        result.add_pass(test_name)
    else:
        result.add_fail(test_name, expected, actual)
    
    # Test replace emojis
    test_name = "replace_emojis"
    text = "Hello 👋"
    replacement = "[emoji]"
    expected = "Hello [emoji]"
    actual = utils.replace_emojis(text, replacement)
    if actual == expected:
        result.add_pass(test_name)
    else:
        result.add_fail(test_name, expected, actual)
    
    # ===== Detection Tests =====
    print("\n[4] Detection Tests")
    print("-" * 40)
    
    # Test has emoji - true
    test_name = "has_emoji_true"
    text = "Hello 👋"
    expected = True
    actual = utils.has_emoji(text)
    if actual == expected:
        result.add_pass(test_name)
    else:
        result.add_fail(test_name, expected, actual)
    
    # Test has emoji - false
    test_name = "has_emoji_false"
    text = "Hello"
    expected = False
    actual = utils.has_emoji(text)
    if actual == expected:
        result.add_pass(test_name)
    else:
        result.add_fail(test_name, expected, actual)
    
    # Test is emoji - true
    test_name = "is_emoji_true"
    expected = True
    actual = utils.is_emoji("😀")
    if actual == expected:
        result.add_pass(test_name)
    else:
        result.add_fail(test_name, expected, actual)
    
    # Test is emoji - false
    test_name = "is_emoji_false"
    expected = False
    actual = utils.is_emoji("Hello")
    if actual == expected:
        result.add_pass(test_name)
    else:
        result.add_fail(test_name, expected, actual)
    
    # Test is emoji - empty
    test_name = "is_emoji_empty"
    expected = False
    actual = utils.is_emoji("")
    if actual == expected:
        result.add_pass(test_name)
    else:
        result.add_fail(test_name, expected, actual)
    
    # ===== Unicode Conversion Tests =====
    print("\n[5] Unicode Conversion Tests")
    print("-" * 40)
    
    # Test to unicode escape
    test_name = "to_unicode_escape"
    emoji = "😀"
    expected = "U+1F600"
    actual = utils.to_unicode_escape(emoji)
    if "U+1F600" in actual:
        result.add_pass(test_name)
    else:
        result.add_fail(test_name, expected, actual)
    
    # Test from unicode escape
    test_name = "from_unicode_escape"
    unicode_str = "U+1F600"
    expected = "😀"
    actual = utils.from_unicode_escape(unicode_str)
    if actual == expected:
        result.add_pass(test_name)
    else:
        result.add_fail(test_name, expected, actual)
    
    # Test round trip
    test_name = "unicode_round_trip"
    emoji = "🌍"
    unicode_str = utils.to_unicode_escape(emoji)
    actual = utils.from_unicode_escape(unicode_str)
    if actual == emoji:
        result.add_pass(test_name)
    else:
        result.add_fail(test_name, emoji, actual)
    
    # ===== Skin Tone Tests =====
    print("\n[6] Skin Tone Tests")
    print("-" * 40)
    
    # Test strip skin tone
    test_name = "strip_skin_tone"
    emoji = "👋🏽"
    expected = "👋"
    actual = utils.strip_skin_tone(emoji)
    if actual == expected:
        result.add_pass(test_name)
    else:
        result.add_fail(test_name, expected, actual)
    
    # Test get skin tone variants
    test_name = "get_skin_tone_variants"
    emoji = "👋"
    variants = utils.get_skin_tone_variants(emoji)
    if len(variants) > 0 and 'medium' in variants:
        result.add_pass(test_name)
    else:
        result.add_fail(test_name, "variants with medium tone", variants)
    
    # ===== Text Conversion Tests =====
    print("\n[7] Text Conversion Tests")
    print("-" * 40)
    
    # Test emoji to text
    test_name = "emoji_to_text"
    emoji = "😀"
    actual = utils.emoji_to_text(emoji)
    if 'face' in actual.lower() or 'grin' in actual.lower():
        result.add_pass(test_name)
    else:
        result.add_fail(test_name, "description with face/grin", actual)
    
    # Test emoji to shortcode
    test_name = "emoji_to_shortcode"
    emoji = "😀"
    actual = utils.emoji_to_text(emoji, use_shortcodes=True)
    if actual.startswith(':') and actual.endswith(':'):
        result.add_pass(test_name)
    else:
        result.add_fail(test_name, "shortcode format :...:", actual)
    
    # Test text to emoji
    test_name = "text_to_emoji"
    text = "smile"
    expected = "😀"
    actual = utils.text_to_emoji(text)
    if actual == expected:
        result.add_pass(test_name)
    else:
        result.add_fail(test_name, expected, actual)
    
    # Test text to emoji - shortcode
    test_name = "shortcode_to_emoji"
    text = ":heart:"
    expected = "❤️"
    actual = utils.text_to_emoji(text)
    if actual == expected:
        result.add_pass(test_name)
    else:
        result.add_fail(test_name, expected, actual)
    
    # ===== Analysis Tests =====
    print("\n[8] Analysis Tests")
    print("-" * 40)
    
    # Test basic analysis
    test_name = "analyze_basic"
    text = "Hello 👋 World 🌍! 👋"
    analysis = utils.analyze(text)
    if analysis.total_emojis == 3 and analysis.unique_emojis == 2:
        result.add_pass(test_name)
    else:
        result.add_fail(test_name, "total=3, unique=2", 
                       f"total={analysis.total_emojis}, unique={analysis.unique_emojis}")
    
    # Test analysis categories
    test_name = "analyze_categories"
    text = "😀🐕🍎"
    analysis = utils.analyze(text)
    if len(analysis.categories) > 0:
        result.add_pass(test_name)
    else:
        result.add_fail(test_name, "categories detected", analysis.categories)
    
    # Test analysis density
    test_name = "analyze_density"
    text = "😀"
    analysis = utils.analyze(text)
    if analysis.emoji_density == 100.0:
        result.add_pass(test_name)
    else:
        result.add_fail(test_name, 100.0, analysis.emoji_density)
    
    # Test analysis to_dict
    test_name = "analysis_to_dict"
    text = "😀👋"
    analysis = utils.analyze(text)
    result_dict = analysis.to_dict()
    if 'total_emojis' in result_dict and 'emojis' in result_dict:
        result.add_pass(test_name)
    else:
        result.add_fail(test_name, "dict with required keys", result_dict.keys())
    
    # ===== Category Filter Tests =====
    print("\n[9] Category Filter Tests")
    print("-" * 40)
    
    # Test filter by category - smiley
    test_name = "filter_smiley"
    text = "😀🐕🍎"
    actual = utils.filter_by_category(text, EmojiCategory.SMILEY)
    if '😀' in actual:
        result.add_pass(test_name)
    else:
        result.add_fail(test_name, "smiley emoji filtered", actual)
    
    # Test filter by category - no match
    test_name = "filter_no_match"
    text = "🐕🍎"
    actual = utils.filter_by_category(text, EmojiCategory.SMILEY)
    if len(actual) == 0:
        result.add_pass(test_name)
    else:
        result.add_fail(test_name, "empty list", actual)
    
    # ===== Position Tests =====
    print("\n[10] Position Tests")
    print("-" * 40)
    
    # Test get positions
    test_name = "get_positions"
    text = "Hi 👋"
    positions = utils.get_emoji_positions(text)
    if len(positions) == 1 and positions[0][2] == '👋':
        result.add_pass(test_name)
    else:
        result.add_fail(test_name, "one position with 👋", positions)
    
    # Test get positions - multiple
    test_name = "get_positions_multiple"
    text = "😀😃😄"
    positions = utils.get_emoji_positions(text)
    if len(positions) == 3:
        result.add_pass(test_name)
    else:
        result.add_fail(test_name, "three positions", len(positions))
    
    # ===== Reverse Tests =====
    print("\n[11] Reverse Tests")
    print("-" * 40)
    
    # Test reverse with emoji
    test_name = "reverse_emoji"
    text = "Hi 👋"
    actual = utils.reverse(text)
    # Emoji should stay intact, text reversed
    if '👋' in actual and 'iH' in actual:
        result.add_pass(test_name)
    else:
        result.add_fail(test_name, "👋 and iH in result", actual)
    
    # Test reverse empty
    test_name = "reverse_empty"
    expected = ""
    actual = utils.reverse("")
    if actual == expected:
        result.add_pass(test_name)
    else:
        result.add_fail(test_name, expected, actual)
    
    # Test reverse no emoji
    test_name = "reverse_no_emoji"
    text = "Hello"
    expected = "olleH"
    actual = utils.reverse(text)
    if actual == expected:
        result.add_pass(test_name)
    else:
        result.add_fail(test_name, expected, actual)
    
    # ===== Edge Cases =====
    print("\n[12] Edge Cases")
    print("-" * 40)
    
    # Test None handling (should return empty list for defensive programming)
    test_name = "handle_none"
    try:
        actual = utils.extract_emojis(None)
        if actual == []:
            result.add_pass(test_name)
        else:
            result.add_fail(test_name, "empty list", actual)
    except (TypeError, AttributeError):
        # Also acceptable to raise an exception
        result.add_pass(test_name)
    
    # Test very long text
    test_name = "long_text"
    text = "😀" * 1000
    count = utils.count_emojis(text)
    if count == 1000:
        result.add_pass(test_name)
    else:
        result.add_fail(test_name, 1000, count)
    
    # Test mixed scripts
    test_name = "mixed_scripts"
    text = "Hello 你好 👋 مرحبا 🌍"
    emojis = utils.extract_emojis(text)
    if len(emojis) >= 2:
        result.add_pass(test_name)
    else:
        result.add_fail(test_name, "2+ emojis", len(emojis))
    
    # Test emoji at boundaries
    test_name = "emoji_boundaries"
    text = "👋Hello🌍"
    emojis = utils.extract_emojis(text)
    if len(emojis) == 2:
        result.add_pass(test_name)
    else:
        result.add_fail(test_name, 2, len(emojis))
    
    # ===== EmojiInfo Tests =====
    print("\n[13] EmojiInfo Tests")
    print("-" * 40)
    
    # Test get emoji info
    test_name = "get_emoji_info"
    emoji = "😀"
    info = utils.get_emoji_info(emoji)
    if info and info.char == emoji:
        result.add_pass(test_name)
    else:
        result.add_fail(test_name, "valid EmojiInfo", info)
    
    # Test emoji info to_dict
    test_name = "emoji_info_to_dict"
    emoji = "🌍"
    info = utils.get_emoji_info(emoji)
    if info:
        result_dict = info.to_dict()
        if 'char' in result_dict and 'unicode' in result_dict:
            result.add_pass(test_name)
        else:
            result.add_fail(test_name, "dict with char/unicode", result_dict.keys())
    else:
        result.add_fail(test_name, "valid info", None)
    
    # Test non-emoji info
    test_name = "non_emoji_info"
    info = utils.get_emoji_info("A")
    if info is None:
        result.add_pass(test_name)
    else:
        result.add_fail(test_name, None, info)
    
    # ===== Module-level Functions =====
    print("\n[14] Module-level Functions")
    print("-" * 40)
    
    # Test module extract
    test_name = "module_extract"
    text = "Hello 👋"
    expected = ['👋']
    actual = extract_emojis(text)
    if actual == expected:
        result.add_pass(test_name)
    else:
        result.add_fail(test_name, expected, actual)
    
    # Test module count
    test_name = "module_count"
    text = "😀😃"
    expected = 2
    actual = count_emojis(text)
    if actual == expected:
        result.add_pass(test_name)
    else:
        result.add_fail(test_name, expected, actual)
    
    # Test module has_emoji
    test_name = "module_has_emoji"
    text = "Hello 🌍"
    expected = True
    actual = has_emoji(text)
    if actual == expected:
        result.add_pass(test_name)
    else:
        result.add_fail(test_name, expected, actual)
    
    # Test module analyze
    test_name = "module_analyze"
    text = "😀👋"
    analysis = analyze(text)
    if isinstance(analysis, EmojiAnalysis):
        result.add_pass(test_name)
    else:
        result.add_fail(test_name, "EmojiAnalysis instance", type(analysis))
    
    # Print summary
    result.summary()
    return result.summary()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
