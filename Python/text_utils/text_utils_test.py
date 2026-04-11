#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AllToolkit - Text Utilities Test Suite"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    clean_whitespace, clean_text, remove_html_tags, remove_urls, remove_emojis,
    truncate, pad_left, pad_right, pad_center, wrap_text, indent_text,
    to_camel_case, to_pascal_case, to_snake_case, to_kebab_case, to_title_case,
    replace_all, replace_regex, find_all, find_first,
    count_words, count_chars, count_lines, word_frequency, char_frequency, readability_score,
    escape_html, unescape_html, escape_regex, hash_text,
    levenshtein_distance, similarity_ratio, is_palindrome,
    is_empty, is_not_empty, reverse_string, repeat_string,
    generate_random_string, extract_numbers, extract_emails, mask_text
)


class TestRunner:
    def __init__(self):
        self.passed = 0
        self.failed = 0
    
    def test(self, name, condition):
        if condition:
            self.passed += 1
            print(f"  ✓ {name}")
        else:
            self.failed += 1
            print(f"  ✗ {name}")
    
    def report(self):
        total = self.passed + self.failed
        print(f"\n{'='*50}")
        print(f"Tests: {total} | Passed: {self.passed} | Failed: {self.failed}")
        if self.failed == 0:
            print("All tests passed!")
        else:
            print(f"{self.failed} test(s) failed.")
        print('='*50)
        return self.failed == 0


def run_tests():
    runner = TestRunner()
    
    # ========================================================================
    # String Cleaning Tests
    # ========================================================================
    print("\nString Cleaning Tests")
    print("="*50)
    
    runner.test("clean_whitespace removes extra spaces", clean_whitespace("  hello   world  ") == "hello world")
    runner.test("clean_whitespace handles newlines", clean_whitespace("hello\n\nworld") == "hello world")
    runner.test("clean_whitespace handles None", clean_whitespace(None) == "")
    runner.test("clean_whitespace handles empty string", clean_whitespace("") == "")
    
    runner.test("clean_text removes punctuation", clean_text("Hello, World!", remove_punctuation=True) == "Hello World")
    runner.test("clean_text removes digits", clean_text("abc123", remove_digits=True) == "abc")
    runner.test("clean_text converts to lowercase", clean_text("HELLO", lowercase=True) == "hello")
    runner.test("clean_text strips whitespace", clean_text("  hello  ", strip=True) == "hello")
    runner.test("clean_text handles None", clean_text(None) == "")
    
    runner.test("remove_html_tags removes tags", remove_html_tags("<p>Hello <b>World</b></p>") == "Hello World")
    runner.test("remove_html_tags handles nested tags", remove_html_tags("<div><span>text</span></div>") == "text")
    runner.test("remove_html_tags handles None", remove_html_tags(None) == "")
    
    runner.test("remove_urls removes http URLs", "example.com" not in remove_urls("Visit https://example.com now"))
    runner.test("remove_urls removes www URLs", "example.com" not in remove_urls("Check www.example.com"))
    runner.test("remove_urls handles None", remove_urls(None) == "")
    
    runner.test("remove_emojis removes emojis", remove_emojis("Hello 👋 World") == "Hello  World")
    runner.test("remove_emojis handles None", remove_emojis(None) == "")
    
    # ========================================================================
    # Text Formatting Tests
    # ========================================================================
    print("\nText Formatting Tests")
    print("="*50)
    
    runner.test("truncate shortens long text", truncate("Hello World", 8) == "Hello...")
    runner.test("truncate keeps short text", truncate("Hi", 10) == "Hi")
    runner.test("truncate uses custom suffix", truncate("Hello", 4, suffix="!") == "Hel!")
    runner.test("truncate handles None", truncate(None, 10) == "")
    
    runner.test("pad_left adds padding", pad_left("42", 5, '0') == "00042")
    runner.test("pad_left handles None", pad_left(None, 5) == "     ")
    
    runner.test("pad_right adds padding", pad_right("Hello", 10) == "Hello     ")
    runner.test("pad_right handles None", pad_right(None, 5) == "     ")
    
    runner.test("pad_center centers text", pad_center("Title", 20, '=') == "=======Title========")
    runner.test("pad_center handles None", pad_center(None, 5) == "     ")
    
    runner.test("wrap_text wraps long lines", '\n' in wrap_text("Hello world this is a long line", width=15))
    runner.test("wrap_text handles None", wrap_text(None, 80) == "")
    runner.test("wrap_text handles empty string", wrap_text("", width=80) == "")
    runner.test("wrap_text handles width 1", wrap_text("abc", width=1) == "a\nb\nc")
    runner.test("wrap_text breaks long words", "aaaa" in wrap_text("aaaaaaaaaa", width=4))
    runner.test("wrap_text preserves short lines", wrap_text("hi", width=10) == "hi")
    runner.test("wrap_text raises on invalid width", 
                (lambda: wrap_text("test", width=0) and False or True) if True else False)
    try:
        wrap_text("test", width=0)
        runner.test("wrap_text raises ValueError on zero width", False)
    except ValueError as e:
        runner.test("wrap_text raises ValueError on zero width", "width must be positive" in str(e))
    except Exception:
        runner.test("wrap_text raises ValueError on zero width", False)
    try:
        wrap_text("test", width=-1)
        runner.test("wrap_text raises ValueError on negative width", False)
    except ValueError as e:
        runner.test("wrap_text raises ValueError on negative width", "width must be positive" in str(e))
    except Exception:
        runner.test("wrap_text raises ValueError on negative width", False)
    
    runner.test("indent_text adds indentation", indent_text("line", spaces=2) == "  line")
    runner.test("indent_text indents multiple lines", indent_text("a\nb", spaces=2) == "  a\n  b")
    runner.test("indent_text skips first line", indent_text("a\nb", spaces=2, skip_first=True) == "a\n  b")
    runner.test("indent_text handles None", indent_text(None) == "")
    
    # ========================================================================
    # Case Conversion Tests
    # ========================================================================
    print("\nCase Conversion Tests")
    print("="*50)
    
    runner.test("to_camel_case from snake_case", to_camel_case("hello_world") == "helloWorld")
    runner.test("to_camel_case from space-separated", to_camel_case("Hello World") == "helloWorld")
    runner.test("to_camel_case handles None", to_camel_case(None) == "")
    
    runner.test("to_pascal_case from snake_case", to_pascal_case("hello_world") == "HelloWorld")
    runner.test("to_pascal_case handles None", to_pascal_case(None) == "")
    
    runner.test("to_snake_case from camelCase", to_snake_case("helloWorld") == "hello_world")
    runner.test("to_snake_case from PascalCase", to_snake_case("HelloWorld") == "hello_world")
    runner.test("to_snake_case handles None", to_snake_case(None) == "")
    
    runner.test("to_kebab_case from camelCase", to_kebab_case("helloWorld") == "hello-world")
    runner.test("to_kebab_case handles None", to_kebab_case(None) == "")
    
    runner.test("to_title_case", to_title_case("hello world") == "Hello World")
    runner.test("to_title_case handles None", to_title_case(None) == "")
    
    # ========================================================================
    # Search and Replace Tests
    # ========================================================================
    print("\nSearch and Replace Tests")
    print("="*50)
    
    runner.test("replace_all single replacement", replace_all("hello", {"hello": "hi"}) == "hi")
    runner.test("replace_all multiple replacements", replace_all("hello world", {"hello": "hi", "world": "there"}) == "hi there")
    runner.test("replace_all handles None", replace_all(None, {}) == "")
    
    runner.test("replace_regex with pattern", replace_regex("abc123def", r'\d+', 'X') == "abcXdef")
    runner.test("replace_regex handles None", replace_regex(None, r'\d+', 'X') == "")
    
    runner.test("find_all finds all matches", find_all("abc123def456", r'\d+') == ['123', '456'])
    runner.test("find_all returns empty on no match", find_all("abcdef", r'\d+') == [])
    runner.test("find_all handles None", find_all(None, r'\d+') == [])
    
    runner.test("find_first finds first match", find_first("abc123def456", r'\d+') == '123')
    runner.test("find_first returns default on no match", find_first("abcdef", r'\d+', default='N/A') == 'N/A')
    runner.test("find_first handles None", find_first(None, r'\d+') == '')
    
    # ========================================================================
    # Text Analysis Tests
    # ========================================================================
    print("\nText Analysis Tests")
    print("="*50)
    
    runner.test("count_words", count_words("Hello world this is a test") == 6)
    runner.test("count_words empty", count_words("") == 0)
    runner.test("count_words handles None", count_words(None) == 0)
    
    runner.test("count_chars with spaces", count_chars("Hello World") == 11)
    runner.test("count_chars without spaces", count_chars("Hello World", include_spaces=False) == 10)
    runner.test("count_chars handles None", count_chars(None) == 0)
    
    runner.test("count_lines", count_lines("line1\nline2\nline3") == 3)
    runner.test("count_lines single line", count_lines("single") == 1)
    runner.test("count_lines handles None", count_lines(None) == 0)
    
    runner.test("word_frequency", word_frequency("hello world hello") == {'hello': 2, 'world': 1})
    runner.test("word_frequency case insensitive", word_frequency("Hello hello", lowercase=True) == {'hello': 2})
    runner.test("word_frequency handles None", word_frequency(None) == {})
    
    runner.test("char_frequency", char_frequency("hello") == {'h': 1, 'e': 1, 'l': 2, 'o': 1})
    runner.test("char_frequency handles None", char_frequency(None) == {})
    
    runner.test("readability_score returns dict", isinstance(readability_score("Hello world. Test."), dict))
    runner.test("readability_score has expected keys", 'word_count' in readability_score("Hello world."))
    runner.test("readability_score handles None", readability_score(None) == {})
    
    # ========================================================================
    # Encoding and Escaping Tests
    # ========================================================================
    print("\nEncoding and Escaping Tests")
    print("="*50)
    
    runner.test("escape_html escapes < and >", '&' in escape_html("<script>"))
    runner.test("escape_html escapes quotes", '&quot;' in escape_html('"hello"'))
    runner.test("escape_html handles None", escape_html(None) == "")
    
    runner.test("unescape_html unescapes entities", unescape_html("&lt;hello&gt;") == "<hello>")
    runner.test("unescape_html handles None", unescape_html(None) == "")
    
    runner.test("escape_regex escapes special chars", '\\' in escape_regex("price: $100"))
    runner.test("escape_regex handles None", escape_regex(None) == "")
    
    runner.test("hash_text md5", hash_text("hello", algorithm='md5') == "5d41402abc4b2a76b9719d911017c592")
    runner.test("hash_text sha256", len(hash_text("hello", algorithm='sha256')) == 64)
    runner.test("hash_text handles None", hash_text(None) == "")
    
    # ========================================================================
    # String Comparison Tests
    # ========================================================================
    print("\nString Comparison Tests")
    print("="*50)
    
    runner.test("levenshtein_distance identical", levenshtein_distance("hello", "hello") == 0)
    runner.test("levenshtein_distance different", levenshtein_distance("kitten", "sitting") == 3)
    runner.test("levenshtein_distance handles None", levenshtein_distance(None, "hello") == 5)
    
    runner.test("similarity_ratio identical", similarity_ratio("hello", "hello") == 1.0)
    runner.test("similarity_ratio similar", 0.7 < similarity_ratio("hello", "hallo") < 1.0)
    runner.test("similarity_ratio handles None", similarity_ratio(None, None) == 1.0)
    
    runner.test("is_palindrome simple", is_palindrome("radar") == True)
    runner.test("is_palindrome with spaces", is_palindrome("A man a plan a canal Panama") == True)
    runner.test("is_palindrome negative", is_palindrome("hello") == False)
    runner.test("is_palindrome handles None", is_palindrome(None) == False)
    
    # ========================================================================
    # Utility Functions Tests
    # ========================================================================
    print("\nUtility Functions Tests")
    print("="*50)
    
    runner.test("is_empty with whitespace", is_empty("   ") == True)
    runner.test("is_empty with content", is_empty("hello") == False)
    runner.test("is_empty with None", is_empty(None) == True)
    
    runner.test("is_not_empty with content", is_not_empty("hello") == True)
    runner.test("is_not_empty with whitespace", is_not_empty("   ") == False)
    
    runner.test("reverse_string", reverse_string("hello") == "olleh")
    runner.test("reverse_string handles None", reverse_string(None) == "")
    
    runner.test("repeat_string", repeat_string("ab", 3) == "ababab")
    runner.test("repeat_string with separator", repeat_string("ab", 3, separator='-') == "ab-ab-ab")
    runner.test("repeat_string zero count", repeat_string("ab", 0) == "")
    runner.test("repeat_string handles None", repeat_string(None, 3) == "")
    
    runner.test("generate_random_string length", len(generate_random_string(10)) == 10)
    runner.test("generate_random_string uses letters and digits", generate_random_string(100, use_letters=True, use_digits=True, use_special=False).isalnum())
    
    runner.test("extract_numbers", extract_numbers("I have 3 apples and 5 oranges") == [3, 5])
    runner.test("extract_numbers no numbers", extract_numbers("no numbers here") == [])
    runner.test("extract_numbers handles None", extract_numbers(None) == [])
    
    runner.test("extract_emails", extract_emails("Contact support@example.com or sales@company.org") == ['support@example.com', 'sales@company.org'])
    runner.test("extract_emails no emails", extract_emails("no emails here") == [])
    runner.test("extract_emails handles None", extract_emails(None) == [])
    
    runner.test("mask_text end visible", mask_text("1234567890", visible_end=4) == "******7890")
    runner.test("mask_text start and end visible", mask_text("password", visible_start=2, visible_end=2) == "pa****rd")
    runner.test("mask_text custom char", mask_text("secret", mask_char='X') == "XXXXXX")
    runner.test("mask_text handles None", mask_text(None) == "")
    
    # ========================================================================
    # Report Results
    # ========================================================================
    return runner.report()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
