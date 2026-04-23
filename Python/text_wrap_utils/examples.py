#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Text Wrap Utilities - Examples

Demonstrates various use cases for text wrapping, alignment, and formatting.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    wrap_text, align_text, justify_text, wrap_and_align,
    format_paragraph, indent_text, dedent_text, center_block,
    shorten_text, fill_text, TextWrapper, Alignment, WrapMode,
    display_width, is_cjk_char, center, wrap, fill
)


def example_basic_wrapping():
    """Basic text wrapping examples."""
    print("=" * 60)
    print("Example 1: Basic Text Wrapping")
    print("=" * 60)
    
    text = """
    Python is a high-level, general-purpose programming language.
    Its design philosophy emphasizes code readability with the use of
    significant indentation. Python is dynamically-typed and garbage-collected.
    """
    
    # Remove indentation first
    text = dedent_text(text.strip())
    
    print("\nOriginal text:")
    print(text)
    
    print("\nWrapped to 40 characters:")
    print("-" * 40)
    for line in wrap_text(text, width=40):
        print(line)
    print("-" * 40)
    
    print("\nWrapped to 60 characters with indentation:")
    print("-" * 60)
    for line in wrap_text(text, width=60, initial_indent=">>> ", subsequent_indent="    "):
        print(line)
    print("-" * 60)


def example_alignment():
    """Text alignment examples."""
    print("\n" + "=" * 60)
    print("Example 2: Text Alignment")
    print("=" * 60)
    
    text = "Hello World"
    width = 40
    
    print(f"\nText: '{text}'")
    print(f"Width: {width}")
    
    print("\nLeft aligned:")
    print(align_text(text, width, Alignment.LEFT))
    
    print("\nRight aligned:")
    print(align_text(text, width, Alignment.RIGHT))
    
    print("\nCenter aligned:")
    print(align_text(text, width, Alignment.CENTER))
    
    print("\nJustified text:")
    longer_text = "This is a sample text that will be justified"
    print(justify_text(longer_text, width))


def example_paragraph_formatting():
    """Paragraph formatting examples."""
    print("\n" + "=" * 60)
    print("Example 3: Paragraph Formatting")
    print("=" * 60)
    
    text = """
    The quick brown fox jumps over the lazy dog. This classic pangram
    contains every letter of the English alphabet at least once.
    It has been used for font display samples and typing practice.
    """
    
    text = dedent_text(text.strip())
    
    print("\nJustified paragraph (width=50):")
    print("-" * 50)
    result = format_paragraph(
        text,
        width=50,
        alignment=Alignment.JUSTIFY,
        first_line_indent=4
    )
    print(result)
    print("-" * 50)
    
    print("\nLeft-aligned paragraph with hanging indent:")
    print("-" * 50)
    result = format_paragraph(
        text,
        width=50,
        alignment=Alignment.LEFT,
        hanging_indent=4
    )
    print(result)
    print("-" * 50)


def example_text_wrapper():
    """TextWrapper class example."""
    print("\n" + "=" * 60)
    print("Example 4: Using TextWrapper Class")
    print("=" * 60)
    
    text = """
    Lorem ipsum dolor sit amet, consectetur adipiscing elit.
    Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
    """
    
    text = dedent_text(text.strip())
    
    # Create a wrapper for console output
    wrapper = TextWrapper(
        width=50,
        initial_indent="> ",
        subsequent_indent="  "
    )
    
    print("\nIndented output:")
    print(wrapper.fill(text))
    
    # Create a wrapper for justified text
    justified_wrapper = TextWrapper(
        width=40,
        alignment=Alignment.JUSTIFY
    )
    
    print("\nJustified output:")
    lines = justified_wrapper.wrap_and_align(text)
    for line in lines:
        print(line)


def example_shortening():
    """Text shortening examples."""
    print("\n" + "=" * 60)
    print("Example 5: Text Shortening")
    print("=" * 60)
    
    titles = [
        "This is a very long article title that needs to be shortened for display",
        "Python Programming: A Comprehensive Guide for Beginners",
        "Machine Learning with TensorFlow and PyTorch: Practical Examples"
    ]
    
    print("\nOriginal titles shortened to 30 characters:")
    print("-" * 30)
    for title in titles:
        shortened = shorten_text(title, width=30, placeholder="...")
        print(shortened)
    
    print("\nWith custom placeholder:")
    for title in titles:
        shortened = shorten_text(title, width=25, placeholder="…")
        print(shortened)


def example_cjk_handling():
    """CJK (Chinese/Japanese/Korean) text handling examples."""
    print("\n" + "=" * 60)
    print("Example 6: CJK Text Handling")
    print("=" * 60)
    
    # Chinese text
    chinese = "这是一个中文测试文本，用于演示中文字符的换行功能。每个中文字符占用两个字符宽度。"
    
    print("\nChinese text wrapped to 30 character width:")
    print("-" * 30)
    lines = wrap_text(chinese, width=30)
    for line in lines:
        print(line)
    print("-" * 30)
    
    # Japanese text
    japanese = "これは日本語のテストテキストです。文字の幅を正しく計算して、適切に改行します。"
    
    print("\nJapanese text wrapped:")
    print("-" * 30)
    lines = wrap_text(japanese, width=30)
    for line in lines:
        print(line)
    print("-" * 30)
    
    # Mixed text
    mixed = "Hello world! 这是一个 mixed 测试文本 with 中文 and English。"
    
    print("\nMixed Chinese and English text:")
    print("-" * 30)
    lines = wrap_text(mixed, width=30)
    for line in lines:
        print(line)
    print("-" * 30)
    
    # Display width examples
    print("\nDisplay width calculations:")
    print(f"  '中文' width: {display_width('中文')} (4 cells)")
    print(f"  'hello' width: {display_width('hello')} (5 cells)")
    print(f"  'hello世界' width: {display_width('hello世界')} (9 cells)")


def example_centering():
    """Block centering examples."""
    print("\n" + "=" * 60)
    print("Example 7: Centering Blocks")
    print("=" * 60)
    
    # Center a title
    title = "Welcome to Text Wrap Utils"
    print("\nCentered title (width=50):")
    print(center_block(title, width=50))
    
    # Center a block
    block = """
    Line One
    Line Two
    Line Three
    """
    block = dedent_text(block.strip())
    
    print("\nCentered block:")
    print(center_block(block, width=40))


def example_indentation():
    """Indentation examples."""
    print("\n" + "=" * 60)
    print("Example 8: Indentation")
    print("=" * 60)
    
    code = """
def hello():
    print("Hello, World!")
    return True
"""
    code = dedent_text(code.strip())
    
    print("\nCode with extra indentation:")
    print(indent_text(code, prefix="    "))
    
    print("\nSkip first line:")
    print(indent_text(code, prefix="    ", skip_first=True))
    
    # List items
    items = ["First item", "Second item", "Third item"]
    
    print("\nList items with bullet:")
    for item in items:
        print(indent_text(item, prefix="• "))


def example_justified_text():
    """Full justification examples."""
    print("\n" + "=" * 60)
    print("Example 9: Full Justification")
    print("=" * 60)
    
    text = """
    Programming in Python is fun and productive. The language is designed
    to be easy to read and write. It supports multiple programming paradigms
    including procedural, object-oriented, and functional programming.
    """
    
    text = dedent_text(text.strip())
    
    print("\nFully justified text (newspaper style):")
    print("-" * 50)
    lines = wrap_and_align(text, width=50, alignment=Alignment.JUSTIFY)
    for line in lines:
        print(line)
    print("-" * 50)


def example_console_output():
    """Console output formatting example."""
    print("\n" + "=" * 60)
    print("Example 10: Console Output Formatting")
    print("=" * 60)
    
    # Format a console message
    title = "Application Status"
    message = """
    The application is running successfully. All systems are operational.
    Current status: Active. Last check: 2024-04-23 23:00:00
    """
    
    message = dedent_text(message.strip())
    
    # Centered title
    print("\n" + center(title, width=50))
    print("-" * 50)
    
    # Wrapped message
    for line in wrap_text(message, width=50, initial_indent="  "):
        print(line)
    
    print("-" * 50)


def run_all_examples():
    """Run all examples."""
    example_basic_wrapping()
    example_alignment()
    example_paragraph_formatting()
    example_text_wrapper()
    example_shortening()
    example_cjk_handling()
    example_centering()
    example_indentation()
    example_justified_text()
    example_console_output()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    run_all_examples()