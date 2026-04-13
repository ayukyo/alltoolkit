#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Pinyin Utilities Examples
========================================
Basic usage examples for the pinyin_utils module.

Author: AllToolkit Contributors
License: MIT
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    is_hanzi,
    get_pinyin,
    to_pinyin,
    to_pinyin_initials,
    to_pinyin_finals,
    sort_by_pinyin,
    contains_hanzi,
    count_hanzi,
    extract_hanzi,
    pinyin_to_ascii,
    ascii_to_pinyin,
    normalize_pinyin,
    annotate_pinyin,
    format_interlinear,
    analyze_polyphonic,
)


def example_basic_conversion():
    """Example: Basic pinyin conversion."""
    print("\n" + "=" * 50)
    print("Example: Basic Pinyin Conversion")
    print("=" * 50)
    
    text = "你好世界"
    print(f"Original text: {text}")
    print(f"With tone marks: {to_pinyin(text, format='tone')}")
    print(f"With tone numbers: {to_pinyin(text, format='number')}")
    print(f"Plain (no tones): {to_pinyin(text, format='plain')}")


def example_different_formats():
    """Example: Different output formats."""
    print("\n" + "=" * 50)
    print("Example: Different Output Formats")
    print("=" * 50)
    
    text = "北京上海广州"
    
    print(f"Text: {text}")
    print(f"\nFormat 'tone' (with tone marks):")
    print(f"  {to_pinyin(text, format='tone')}")
    
    print(f"\nFormat 'number' (with tone numbers):")
    print(f"  {to_pinyin(text, format='number')}")
    
    print(f"\nFormat 'plain' (no tones):")
    print(f"  {to_pinyin(text, format='plain')}")
    
    print(f"\nWith custom separator:")
    print(f"  Comma: {to_pinyin(text, separator=',')}")
    print(f"  Dash: {to_pinyin(text, separator='-')}")
    print(f"  No space: {to_pinyin(text, separator='')}")


def example_polyphonic_handling():
    """Example: Polyphonic character handling."""
    print("\n" + "=" * 50)
    print("Example: Polyphonic Character Handling")
    print("=" * 50)
    
    # 長 - chang (long) vs zhang (grow/chief)
    print("Character '长':")
    print(f"  Possible readings: {get_pinyin('长')}")
    print(f"  '长城' (Great Wall): {to_pinyin('长城')}  ← Uses 'cháng'")
    print(f"  '家长' (Parent): {to_pinyin('家长')}  ← Uses 'zhǎng'")
    print(f"  '队长' (Captain): {to_pinyin('队长')}  ← Uses 'zhǎng'")
    
    # 行 - xing (walk) vs hang (row/industry)
    print("\nCharacter '行':")
    print(f"  Possible readings: {get_pinyin('行')}")
    print(f"  '银行' (Bank): {to_pinyin('银行')}  ← Uses 'háng'")
    print(f"  '行走' (Walk): {to_pinyin('行走')}  ← Uses 'xíng'")
    print(f"  '自行车' (Bicycle): {to_pinyin('自行车')}  ← Uses 'xíng'")
    
    # 乐 - le (happy) vs yue (music)
    print("\nCharacter '乐':")
    print(f"  Possible readings: {get_pinyin('乐')}")
    print(f"  '快乐' (Happy): {to_pinyin('快乐')}  ← Uses 'lè'")
    print(f"  '音乐' (Music): {to_pinyin('音乐')}  ← Uses 'yuè'")


def example_initials_and_finals():
    """Example: Extract initials and finals."""
    print("\n" + "=" * 50)
    print("Example: Extract Initials and Finals")
    print("=" * 50)
    
    text = "你好世界"
    print(f"Text: {text}")
    
    initials = to_pinyin_initials(text)
    print(f"Initials: {initials}")
    
    finals = to_pinyin_finals(text)
    print(f"Finals (with tones): {finals}")
    
    finals_plain = to_pinyin_finals(text, with_tone=False)
    print(f"Finals (no tones): {finals_plain}")


def example_sorting():
    """Example: Sort Chinese text by pinyin."""
    print("\n" + "=" * 50)
    print("Example: Sort Chinese Text by Pinyin")
    print("=" * 50)
    
    cities = ['北京', '上海', '广州', '深圳', '杭州', '南京']
    print(f"Original list: {cities}")
    
    sorted_cities = sort_by_pinyin(cities)
    print(f"Sorted by pinyin: {sorted_cities}")
    
    # Show pinyin for each city
    for city in sorted_cities:
        print(f"  {city}: {to_pinyin(city, format='plain')}")


def example_detection():
    """Example: Detect and extract Chinese characters."""
    print("\n" + "=" * 50)
    print("Example: Detect and Extract Chinese Characters")
    print("=" * 50)
    
    mixed_text = "Hello 你好 World 世界"
    print(f"Mixed text: '{mixed_text}'")
    
    print(f"Contains Chinese: {contains_hanzi(mixed_text)}")
    print(f"Chinese character count: {count_hanzi(mixed_text)}")
    print(f"Extracted characters: {extract_hanzi(mixed_text)}")
    
    # Check individual characters
    print(f"\nCharacter checks:")
    print(f"  '你' is Chinese: {is_hanzi('你')}")
    print(f"  'H' is Chinese: {is_hanzi('H')}")


def example_tone_conversion():
    """Example: Convert between tone formats."""
    print("\n" + "=" * 50)
    print("Example: Tone Format Conversion")
    print("=" * 50)
    
    # Tone marks to numbers
    pinyin_with_tones = "nǐ hǎo shì jiè"
    print(f"Tone marks: {pinyin_with_tones}")
    print(f"To numbers: {pinyin_to_ascii(pinyin_with_tones)}")
    
    # Tone numbers to marks
    pinyin_with_numbers = "ni3 hao3 shi4 jie4"
    print(f"\nTone numbers: {pinyin_with_numbers}")
    print(f"To marks: {ascii_to_pinyin(pinyin_with_numbers)}")
    
    # Normalization
    print(f"\nNormalize 'NV3': {normalize_pinyin('NV3')}")


def example_annotation():
    """Example: Create pinyin annotations."""
    print("\n" + "=" * 50)
    print("Example: Pinyin Annotation")
    print("=" * 50)
    
    text = "你好世界"
    print(f"Text: {text}")
    
    # List of (char, pinyin) tuples
    annotations = annotate_pinyin(text)
    print(f"\nAnnotations:")
    for char, py in annotations:
        print(f"  '{char}' -> '{py}'")
    
    # Interlinear format
    print(f"\nInterlinear format:")
    print(format_interlinear(text))


def example_polyphonic_analysis():
    """Example: Analyze polyphonic characters."""
    print("\n" + "=" * 50)
    print("Example: Polyphonic Character Analysis")
    print("=" * 50)
    
    text = "银行行长参观长城"
    print(f"Text: {text}")
    
    analysis = analyze_polyphonic(text)
    print(f"\nPolyphonic characters found:")
    
    for item in analysis:
        print(f"  Position {item['position']}: '{item['char']}'")
        print(f"    Possible readings: {item['readings']}")
        if item['context']:
            print(f"    Context suggests: {item['context']}")


def example_mixed_text():
    """Example: Handle mixed Chinese and non-Chinese text."""
    print("\n" + "=" * 50)
    print("Example: Mixed Chinese and Non-Chinese Text")
    print("=" * 50)
    
    texts = [
        "Hello 你好",
        "我的email是test@example.com",
        "北京2008奥运会",
        "iPhone手机很好用",
    ]
    
    for text in texts:
        print(f"\nOriginal: {text}")
        print(f"Pinyin: {to_pinyin(text)}")


def example_numbers():
    """Example: Convert Chinese numbers."""
    print("\n" + "=" * 50)
    print("Example: Chinese Numbers")
    print("=" * 50)
    
    numbers = "一二三四五六七八九十百千万亿"
    print(f"Chinese numbers: {numbers}")
    print(f"Pinyin: {to_pinyin(numbers)}")


def example_heteronym_mode():
    """Example: Get all possible readings."""
    print("\n" + "=" * 50)
    print("Example: Heteronym Mode (All Readings)")
    print("=" * 50)
    
    text = "你好"
    print(f"Text: {text}")
    
    # Normal mode - returns string
    normal = to_pinyin(text)
    print(f"Normal mode: {normal}")
    
    # Heteronym mode - returns list of lists
    heteronym = to_pinyin(text, heteronym=True)
    print(f"Heteronym mode: {heteronym}")
    print(f"  '你' readings: {heteronym[0]}")
    print(f"  '好' readings: {heteronym[1]}")


def run_all_examples():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("   PINYIN UTILITIES - USAGE EXAMPLES")
    print("=" * 60)
    
    example_basic_conversion()
    example_different_formats()
    example_polyphonic_handling()
    example_initials_and_finals()
    example_sorting()
    example_detection()
    example_tone_conversion()
    example_annotation()
    example_polyphonic_analysis()
    example_mixed_text()
    example_numbers()
    example_heteronym_mode()
    
    print("\n" + "=" * 60)
    print("   All examples completed!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    run_all_examples()