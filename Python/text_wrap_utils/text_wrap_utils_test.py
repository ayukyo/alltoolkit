#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Suite for Text Wrap Utilities Module

Comprehensive tests for text wrapping, alignment, and formatting functions.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    # Enums
    Alignment, WrapMode,
    # Character utilities
    is_cjk_char, is_wide_char, display_width, strip_ansi, display_width_ansi,
    # Core wrapping functions
    wrap_text, _split_words, _break_word, _truncate_to_width,
    # Alignment functions
    align_text, justify_text,
    # High-level formatting
    wrap_and_align, format_paragraph, dedent_text, indent_text,
    center_block, fill_text, shorten_text, split_lines_aware,
    # Utility class
    TextWrapper,
    # Convenience functions
    wrap, fill, center, left_align, right_align, justify, shorten
)


def test_is_cjk_char():
    """Test CJK character detection."""
    print("Testing is_cjk_char...")
    
    # Chinese characters
    assert is_cjk_char('中') == True
    assert is_cjk_char('文') == True
    
    # Japanese Hiragana
    assert is_cjk_char('あ') == True
    assert is_cjk_char('ん') == True
    
    # Japanese Katakana
    assert is_cjk_char('ア') == True
    assert is_cjk_char('ン') == True
    
    # Korean Hangul
    assert is_cjk_char('한') == True
    assert is_cjk_char('글') == True
    
    # ASCII characters
    assert is_cjk_char('a') == False
    assert is_cjk_char('Z') == False
    assert is_cjk_char('0') == False
    assert is_cjk_char(' ') == False
    
    print("  ✓ is_cjk_char tests passed")


def test_is_wide_char():
    """Test wide character detection."""
    print("Testing is_wide_char...")
    
    # CJK characters are wide
    assert is_wide_char('中') == True
    assert is_wide_char('あ') == True
    assert is_wide_char('한') == True
    
    # ASCII characters are not wide
    assert is_wide_char('a') == False
    assert is_wide_char('Z') == False
    assert is_wide_char(' ') == False
    
    print("  ✓ is_wide_char tests passed")


def test_display_width():
    """Test display width calculation."""
    print("Testing display_width...")
    
    # ASCII
    assert display_width("hello") == 5
    assert display_width("hello world") == 11
    
    # CJK characters (each is 2 cells wide)
    assert display_width("中文") == 4
    assert display_width("日本語") == 6
    
    # Mixed
    assert display_width("hello世界") == 9  # 5 + 4
    
    # Tab (4 cells by default)
    assert display_width("\t") == 4
    
    # Empty
    assert display_width("") == 0
    
    print("  ✓ display_width tests passed")


def test_strip_ansi():
    """Test ANSI code stripping."""
    print("Testing strip_ansi...")
    
    # No ANSI codes
    assert strip_ansi("hello") == "hello"
    
    # With ANSI codes
    text_with_ansi = "\x1b[31mred text\x1b[0m"
    assert strip_ansi(text_with_ansi) == "red text"
    
    # Multiple codes
    text_multiple = "\x1b[1;31mBold Red\x1b[0m \x1b[32mGreen\x1b[0m"
    assert strip_ansi(text_multiple) == "Bold Red Green"
    
    print("  ✓ strip_ansi tests passed")


def test_wrap_text():
    """Test text wrapping."""
    print("Testing wrap_text...")
    
    # Basic wrapping
    text = "This is a simple test of the text wrapping functionality."
    lines = wrap_text(text, width=20)
    
    for line in lines:
        assert display_width(line) <= 20, f"Line too wide: {line}"
    
    # Empty text
    assert wrap_text("") == []
    
    # Short text (no wrapping needed)
    short = "Hello"
    lines = wrap_text(short, width=80)
    assert len(lines) == 1
    assert lines[0] == "Hello"
    
    # Text with indentation
    text = "This is a test with indentation applied."
    lines = wrap_text(text, width=20, initial_indent="> ", subsequent_indent="  ")
    assert lines[0].startswith("> ")
    if len(lines) > 1:
        assert lines[1].startswith("  ")
    
    print("  ✓ wrap_text tests passed")


def test_wrap_text_cjk():
    """Test CJK text wrapping."""
    print("Testing wrap_text with CJK...")
    
    # Chinese text
    text = "这是一个测试文本用于演示中文字符的换行功能。"
    lines = wrap_text(text, width=20)
    
    for line in lines:
        assert display_width(line) <= 20, f"Line too wide: {line}"
    
    # Mixed text
    mixed = "Hello world 这是一个 mixed 测试文本。"
    lines = wrap_text(mixed, width=20)
    
    for line in lines:
        assert display_width(line) <= 20, f"Line too wide: {line}"
    
    print("  ✓ CJK wrap_text tests passed")


def test_align_text():
    """Test text alignment."""
    print("Testing align_text...")
    
    text = "Hello"
    width = 20
    
    # Left alignment
    left = align_text(text, width, Alignment.LEFT)
    assert left == "Hello" + " " * 15
    
    # Right alignment
    right = align_text(text, width, Alignment.RIGHT)
    assert right == " " * 15 + "Hello"
    
    # Center alignment
    centered = align_text(text, width, Alignment.CENTER)
    assert centered == " " * 7 + "Hello" + " " * 8
    
    # Text wider than width
    long_text = "This is a very long text that exceeds the width"
    aligned = align_text(long_text, 10, Alignment.LEFT)
    assert aligned == long_text  # Should return unchanged
    
    print("  ✓ align_text tests passed")


def test_justify_text():
    """Test text justification."""
    print("Testing justify_text...")
    
    # Short text (no justification needed)
    short = "Hello"
    justified = justify_text(short, 10)
    assert display_width(justified) <= 10
    
    # Multiple words
    text = "Hello world test"
    justified = justify_text(text, 30)
    assert display_width(justified) == 30
    # Should have spaces distributed
    assert " " in justified
    
    # Single word
    single = "Hello"
    justified = justify_text(single, 20)
    assert display_width(justified) <= 20
    
    print("  ✓ justify_text tests passed")


def test_wrap_and_align():
    """Test combined wrap and align."""
    print("Testing wrap_and_align...")
    
    text = "This is a sample text for testing the wrap and align functionality of the module."
    
    # Left alignment
    lines = wrap_and_align(text, width=30, alignment=Alignment.LEFT)
    assert len(lines) > 0
    for line in lines:
        assert display_width(line) <= 30
    
    # Center alignment
    lines = wrap_and_align(text, width=30, alignment=Alignment.CENTER)
    for line in lines:
        assert display_width(line) <= 30
    
    # Right alignment
    lines = wrap_and_align(text, width=30, alignment=Alignment.RIGHT)
    for line in lines:
        assert display_width(line) <= 30
    
    # Justify
    lines = wrap_and_align(text, width=30, alignment=Alignment.JUSTIFY)
    for line in lines:
        assert display_width(line) <= 30
    
    print("  ✓ wrap_and_align tests passed")


def test_format_paragraph():
    """Test paragraph formatting."""
    print("Testing format_paragraph...")
    
    text = "This is a test paragraph that will be formatted with specific settings for indentation and line spacing. It should wrap correctly and maintain the proper alignment."
    
    # Basic paragraph
    result = format_paragraph(text, width=40)
    lines = result.split('\n')
    assert len(lines) > 1
    for line in lines:
        assert display_width(line) <= 40
    
    # With indentation (when not justified)
    result = format_paragraph(text, width=40, alignment=Alignment.LEFT, first_line_indent=4)
    assert result.startswith("    ")  # First line indented
    
    # With hanging indent (when not justified)
    result = format_paragraph(text, width=40, alignment=Alignment.LEFT, hanging_indent=4)
    lines = result.split('\n')
    if len(lines) > 1:
        assert lines[1].startswith("    ")
    
    print("  ✓ format_paragraph tests passed")


def test_dedent_text():
    """Test text dedentation."""
    print("Testing dedent_text...")
    
    # Common indentation
    text = """
        First line
        Second line
        Third line
    """
    dedented = dedent_text(text)
    assert "    " not in dedented or dedented.strip().startswith("First")
    
    # Already dedented
    text = "No indentation"
    dedented = dedent_text(text)
    assert dedented == text
    
    print("  ✓ dedent_text tests passed")


def test_indent_text():
    """Test text indentation."""
    print("Testing indent_text...")
    
    text = "First line\nSecond line\nThird line"
    
    # Basic indentation
    indented = indent_text(text, prefix="  ")
    lines = indented.split('\n')
    assert lines[0] == "  First line"
    assert lines[1] == "  Second line"
    assert lines[2] == "  Third line"
    
    # Skip empty lines
    text_with_empty = "First line\n\nThird line"
    indented = indent_text(text_with_empty, prefix="  ", skip_empty=True)
    lines = indented.split('\n')
    assert lines[0] == "  First line"
    assert lines[1] == ""  # Empty line not indented
    assert lines[2] == "  Third line"
    
    # Skip first line
    indented = indent_text(text, prefix="  ", skip_first=True)
    lines = indented.split('\n')
    assert lines[0] == "First line"  # Not indented
    assert lines[1] == "  Second line"  # Indented
    
    print("  ✓ indent_text tests passed")


def test_center_block():
    """Test block centering."""
    print("Testing center_block...")
    
    text = "Hello\nWorld"
    centered = center_block(text, width=20)
    lines = centered.split('\n')
    
    # Both lines should be centered
    assert lines[0].startswith(" " * 7)  # (20 - 5) // 2
    assert lines[1].startswith(" " * 7)
    
    print("  ✓ center_block tests passed")


def test_fill_text():
    """Test text filling."""
    print("Testing fill_text...")
    
    text = "This is a test paragraph.\n\nThis is a second paragraph."
    
    # Preserve paragraphs
    filled = fill_text(text, width=40, preserve_paragraphs=True)
    assert "\n\n" in filled
    
    # No paragraph preservation
    filled = fill_text(text, width=40, preserve_paragraphs=False)
    # Should have no double newlines
    
    print("  ✓ fill_text tests passed")


def test_shorten_text():
    """Test text shortening."""
    print("Testing shorten_text...")
    
    text = "This is a long text that needs to be shortened to fit within a specific width."
    
    # Basic shortening
    shortened = shorten_text(text, width=20)
    assert display_width(shortened) <= 20
    assert shortened.endswith("...")
    
    # Text already short enough
    short = "Hello"
    shortened = shorten_text(short, width=20)
    assert shortened == short
    
    # Custom placeholder
    shortened = shorten_text(text, width=20, placeholder="…")
    assert shortened.endswith("…")
    
    print("  ✓ shorten_text tests passed")


def test_split_lines_aware():
    """Test line-aware splitting."""
    print("Testing split_lines_aware...")
    
    # Text with existing line breaks
    text = "Short line\nThis is a longer line that will need to be wrapped because it exceeds the width."
    
    lines = split_lines_aware(text, width=20)
    
    # First line should be preserved
    assert "Short line" in lines[0]
    
    # Long line should be wrapped
    for line in lines:
        assert display_width(line) <= 20, f"Line too wide: {line}"
    
    print("  ✓ split_lines_aware tests passed")


def test_text_wrapper_class():
    """Test TextWrapper class."""
    print("Testing TextWrapper class...")
    
    text = "This is a test of the TextWrapper class functionality with various settings applied."
    
    # Basic usage
    wrapper = TextWrapper(width=30)
    lines = wrapper.wrap(text)
    assert len(lines) > 0
    for line in lines:
        assert display_width(line) <= 30
    
    # Fill method
    filled = wrapper.fill(text)
    assert "\n" in filled
    
    # With alignment
    wrapper = TextWrapper(width=30, alignment=Alignment.CENTER)
    lines = wrapper.wrap_and_align(text)
    for line in lines:
        assert display_width(line) <= 30
    
    print("  ✓ TextWrapper class tests passed")


def test_convenience_functions():
    """Test convenience functions."""
    print("Testing convenience functions...")
    
    text = "This is a sample text for testing convenience functions."
    
    # wrap
    lines = wrap(text, width=20)
    assert len(lines) > 0
    
    # fill
    filled = fill(text, width=20)
    assert "\n" in filled
    
    # center
    centered = center(text[:10], width=30)
    assert centered.startswith(" ")
    
    # left_align
    left = left_align(text[:10], width=30)
    assert left.endswith(" ")
    
    # right_align
    right = right_align(text[:10], width=30)
    assert right.startswith(" ")
    
    # justify
    justified = justify(text[:30], width=50)
    assert display_width(justified) == 50
    
    # shorten
    short = shorten(text, width=20)
    assert len(short) <= 20
    
    print("  ✓ convenience functions tests passed")


def test_edge_cases():
    """Test edge cases."""
    print("Testing edge cases...")
    
    # Empty string
    assert wrap_text("") == []
    assert align_text("", 10) == " " * 10
    assert justify_text("", 10) == " " * 10  # Returns padded spaces
    
    # Single character
    assert wrap_text("a", width=10) == ["a"]
    assert align_text("a", 5) == "a    "
    
    # Very long word
    long_word = "supercalifragilisticexpialidocious"
    lines = wrap_text(long_word, width=10, break_long_words=True)
    for line in lines:
        assert display_width(line) <= 10
    
    # Whitespace only
    assert wrap_text("   ") == []
    
    # Unicode edge cases
    unicode_text = "🎉🎊🎈🎁🎂"
    lines = wrap_text(unicode_text, width=10)
    assert len(lines) > 0
    
    print("  ✓ edge case tests passed")


def test_break_word():
    """Test word breaking."""
    print("Testing _break_word...")
    
    # Short word (no breaking needed)
    parts = _break_word("hello", 10)
    assert parts == ["hello"]
    
    # Long word
    parts = _break_word("supercalifragilisticexpialidocious", 10)
    for part in parts:
        assert display_width(part) <= 10
    
    # CJK breaking
    parts = _break_word("中文测试文字", 4)
    for part in parts:
        assert display_width(part) <= 4
    
    print("  ✓ _break_word tests passed")


def test_truncate_to_width():
    """Test text truncation."""
    print("Testing _truncate_to_width...")
    
    # ASCII
    truncated = _truncate_to_width("hello world", 5)
    assert truncated == "hello"
    
    # CJK
    truncated = _truncate_to_width("中文测试文字", 4)
    assert truncated == "中文"
    
    # Mixed
    truncated = _truncate_to_width("hello中文", 7)
    assert display_width(truncated) <= 7
    
    print("  ✓ _truncate_to_width tests passed")


def run_all_tests():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("Running Text Wrap Utilities Tests")
    print("=" * 60 + "\n")
    
    # Character utilities
    test_is_cjk_char()
    test_is_wide_char()
    test_display_width()
    test_strip_ansi()
    
    # Core functions
    test_wrap_text()
    test_wrap_text_cjk()
    test_break_word()
    test_truncate_to_width()
    
    # Alignment
    test_align_text()
    test_justify_text()
    
    # High-level formatting
    test_wrap_and_align()
    test_format_paragraph()
    test_dedent_text()
    test_indent_text()
    test_center_block()
    test_fill_text()
    test_shorten_text()
    test_split_lines_aware()
    
    # Utility class
    test_text_wrapper_class()
    
    # Convenience functions
    test_convenience_functions()
    
    # Edge cases
    test_edge_cases()
    
    print("\n" + "=" * 60)
    print("All tests passed! ✓")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    run_all_tests()