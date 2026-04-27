#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Pinyin Utilities Test Suite
=========================================
Comprehensive tests for the pinyin_utils module.

Author: AllToolkit Contributors
License: MIT
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    is_hanzi,
    get_pinyin,
    get_pinyin_with_tone,
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
    segment_chinese,
    annotate_pinyin,
    format_interlinear,
    analyze_polyphonic,
    _apply_tone,
    _remove_tone,
    _extract_tone_number,
)


def test_is_hanzi():
    """Test Chinese character detection."""
    assert is_hanzi('你') == True
    assert is_hanzi('中') == True
    assert is_hanzi('文') == True
    assert is_hanzi('字') == True
    assert is_hanzi('a') == False
    assert is_hanzi('A') == False
    assert is_hanzi('1') == False
    assert is_hanzi('@') == False
    assert is_hanzi('') == False
    assert is_hanzi('你好') == False  # More than one character
    print("✓ test_is_hanzi passed")


def test_get_pinyin():
    """Test basic pinyin retrieval."""
    # Single reading characters
    assert get_pinyin('你') == ['nǐ']
    assert get_pinyin('好') == ['hǎo', 'hào']
    assert get_pinyin('我') == ['wǒ']
    
    # Polyphonic characters
    readings = get_pinyin('长')
    assert 'cháng' in readings
    assert 'zhǎng' in readings
    
    readings = get_pinyin('行')
    assert 'xíng' in readings
    assert 'háng' in readings
    
    # Non-Chinese characters
    assert get_pinyin('a') == []
    assert get_pinyin('a', default='a') == ['a']
    
    print("✓ test_get_pinyin passed")


def test_to_pinyin_basic():
    """Test basic pinyin conversion."""
    # Simple text
    assert to_pinyin('你') == 'nǐ'
    assert to_pinyin('你好') == 'nǐ hǎo'
    
    # Different formats
    assert to_pinyin('你好', format='number') == 'ni3 hao3'
    assert to_pinyin('你好', format='plain') == 'ni hao'
    
    # Mixed text
    result = to_pinyin('Hello你好World')
    assert 'nǐ' in result
    assert 'hǎo' in result
    
    print("✓ test_to_pinyin_basic passed")


def test_to_pinyin_polyphonic():
    """Test polyphonic character handling with context."""
    # 长城 - should use 'chang' for 长
    assert 'cháng' in to_pinyin('长城')
    
    # 家长 - should use 'zhang' for 长
    assert 'zhǎng' in to_pinyin('家长')
    
    # 银行 - should use 'hang' for 行
    assert 'háng' in to_pinyin('银行')
    
    # 行走 - should use 'xing' for 行
    assert 'xíng' in to_pinyin('行走')
    
    print("✓ test_to_pinyin_polyphonic passed")


def test_to_pinyin_formats():
    """Test different output formats."""
    text = '北京'
    
    # Tone marks
    result = to_pinyin(text, format='tone')
    assert result == 'běi jīng'
    
    # Tone numbers
    result = to_pinyin(text, format='number')
    assert result == 'bei3 jing1'
    
    # Plain (no tones)
    result = to_pinyin(text, format='plain')
    assert result == 'bei jing'
    
    print("✓ test_to_pinyin_formats passed")


def test_to_pinyin_heteronym():
    """Test heteronym mode (all readings)."""
    result = to_pinyin('你好', heteronym=True)
    assert isinstance(result, list)
    assert len(result) >= 2
    assert 'nǐ' in result[0]
    
    print("✓ test_to_pinyin_heteronym passed")


def test_to_pinyin_errors():
    """Test error handling modes."""
    # Unknown character handling
    # Since our database doesn't have every character, test with rare ones
    result = to_pinyin('你', errors='default')
    assert 'nǐ' in result
    
    result = to_pinyin('你', errors='ignore')
    assert 'nǐ' in result
    
    result = to_pinyin('你', errors='replace')
    assert 'nǐ' in result
    
    print("✓ test_to_pinyin_errors passed")


def test_to_pinyin_initials():
    """Test initial extraction."""
    initials = to_pinyin_initials('你好世界')
    assert initials[0] == 'n'
    assert initials[1] == 'h'
    # '世' has 'sh' initial
    # '界' has 'j' initial
    
    print("✓ test_to_pinyin_initials passed")


def test_to_pinyin_finals():
    """Test final extraction."""
    finals = to_pinyin_finals('你好')
    assert finals[0] == 'ǐ'  # With tone
    assert finals[1] == 'ǎo'  # With tone
    
    finals_plain = to_pinyin_finals('你好', with_tone=False)
    assert finals_plain[0] == 'i'
    assert finals_plain[1] == 'ao'
    
    print("✓ test_to_pinyin_finals passed")


def test_sort_by_pinyin():
    """Test pinyin-based sorting."""
    cities = ['北京', '上海', '广州', '深圳']
    sorted_cities = sort_by_pinyin(cities)
    
    # Beijing (bei) should come before Guangzhou (guang)
    # Then Shanghai (shang), then Shenzhen (shen)
    assert sorted_cities[0] == '北京'  # b
    assert sorted_cities[1] == '广州'  # g
    assert sorted_cities[2] == '上海'  # sh (after g)
    # Shenzhen starts with 'sh' as well
    
    # Reverse sort
    reversed_cities = sort_by_pinyin(cities, reverse=True)
    assert reversed_cities[0] != sorted_cities[0]
    
    print("✓ test_sort_by_pinyin passed")


def test_contains_hanzi():
    """Test Chinese character detection in text."""
    assert contains_hanzi('你好') == True
    assert contains_hanzi('Hello 你好') == True
    assert contains_hanzi('Hello World') == False
    assert contains_hanzi('') == False
    
    print("✓ test_contains_hanzi passed")


def test_count_hanzi():
    """Test Chinese character counting."""
    assert count_hanzi('你好') == 2
    assert count_hanzi('Hello 你好 World') == 2
    assert count_hanzi('Hello World') == 0
    assert count_hanzi('') == 0
    assert count_hanzi('一二三四五六七八九十') == 10
    
    print("✓ test_count_hanzi passed")


def test_extract_hanzi():
    """Test Chinese character extraction."""
    result = extract_hanzi('Hello 你好世界 World')
    assert result == ['你', '好', '世', '界']
    
    result = extract_hanzi('Hello World')
    assert result == []
    
    print("✓ test_extract_hanzi passed")


def test_pinyin_to_ascii():
    """Test tone mark to tone number conversion."""
    assert pinyin_to_ascii('nǐ') == 'ni3'
    assert pinyin_to_ascii('hǎo') == 'hao3'
    assert pinyin_to_ascii('běi jīng') == 'bei3 jing1'
    
    print("✓ test_pinyin_to_ascii passed")


def test_ascii_to_pinyin():
    """Test tone number to tone mark conversion."""
    assert ascii_to_pinyin('ni3') == 'nǐ'
    assert ascii_to_pinyin('hao3') == 'hǎo'
    assert ascii_to_pinyin('bei3 jing1') == 'běi jīng'
    
    print("✓ test_ascii_to_pinyin passed")


def test_normalize_pinyin():
    """Test pinyin normalization."""
    assert normalize_pinyin('NV3') == 'nǚ'
    assert normalize_pinyin('zhong') == 'zhong'
    assert normalize_pinyin('ZHONG') == 'zhong'
    
    print("✓ test_normalize_pinyin passed")


def test_segment_chinese():
    """Test Chinese word segmentation."""
    result = segment_chinese('北京上海')
    assert isinstance(result, list)
    assert len(result) >= 2  # Should segment into '北京' and '上海'
    
    print("✓ test_segment_chinese passed")


def test_annotate_pinyin():
    """Test pinyin annotation."""
    result = annotate_pinyin('你好')
    assert result[0] == ('你', 'nǐ')
    assert result[1] == ('好', 'hǎo')
    
    # Mixed text
    result = annotate_pinyin('Hello你好')
    assert ('H', '') in result  # Non-Chinese
    assert ('你', 'nǐ') in result
    
    print("✓ test_annotate_pinyin passed")


def test_format_interlinear():
    """Test interlinear format."""
    result = format_interlinear('你好')
    lines = result.split('\n')
    assert len(lines) == 2
    assert 'nǐ' in lines[0]
    assert '好' in lines[1]
    
    print("✓ test_format_interlinear passed")


def test_analyze_polyphonic():
    """Test polyphonic character analysis."""
    result = analyze_polyphonic('银行行长')
    assert isinstance(result, list)
    
    # Should detect polyphonic characters
    for item in result:
        assert 'char' in item
        assert 'position' in item
        assert 'readings' in item
        assert len(item['readings']) > 1
    
    print("✓ test_analyze_polyphonic passed")


def test_tone_operations():
    """Test tone mark operations."""
    # Apply tone
    assert _apply_tone('ni', 3) == 'nǐ'
    assert _apply_tone('zhong', 1) == 'zhōng'
    assert _apply_tone('hao', 3) == 'hǎo'
    
    # Remove tone
    assert _remove_tone('nǐ') == ('ni', 3)
    assert _remove_tone('zhōng') == ('zhong', 1)
    
    # Extract tone number
    assert _extract_tone_number('zhong1') == ('zhong', 1)
    assert _extract_tone_number('ni3') == ('ni', 3)
    
    print("✓ test_tone_operations passed")


def test_numbers():
    """Test number character conversion."""
    assert to_pinyin('一二三') == 'yī èr sān'
    assert to_pinyin('一二三四五六七八九十') == 'yī èr sān sì wǔ liù qī bā jiǔ shí'
    
    print("✓ test_numbers passed")


def test_special_cases():
    """Test special polyphonic cases."""
    # 会 - meeting vs accounting
    assert 'huì' in to_pinyin('会议')  # Meeting - hui
    
    # 好 - good vs like
    assert 'hǎo' in to_pinyin('你好')
    
    # 看 - see vs guard
    assert 'kàn' in to_pinyin('看见')
    
    # 觉 - feel vs sleep
    assert 'jué' in to_pinyin('感觉')
    assert 'jiào' in to_pinyin('睡觉')
    
    print("✓ test_special_cases passed")


def test_separator():
    """Test custom separator."""
    assert to_pinyin('你好', separator=',') == 'nǐ,hǎo'
    assert to_pinyin('你好', separator='-') == 'nǐ-hǎo'
    assert to_pinyin('你好', separator='') == 'nǐhǎo'
    
    print("✓ test_separator passed")


def run_all_tests():
    """Run all test functions."""
    print("\n" + "=" * 50)
    print("Running Pinyin Utilities Tests")
    print("=" * 50 + "\n")
    
    tests = [
        test_is_hanzi,
        test_get_pinyin,
        test_to_pinyin_basic,
        test_to_pinyin_polyphonic,
        test_to_pinyin_formats,
        test_to_pinyin_heteronym,
        test_to_pinyin_errors,
        test_to_pinyin_initials,
        test_to_pinyin_finals,
        test_sort_by_pinyin,
        test_contains_hanzi,
        test_count_hanzi,
        test_extract_hanzi,
        test_pinyin_to_ascii,
        test_ascii_to_pinyin,
        test_normalize_pinyin,
        test_segment_chinese,
        test_annotate_pinyin,
        test_format_interlinear,
        test_analyze_polyphonic,
        test_tone_operations,
        test_numbers,
        test_special_cases,
        test_separator,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__} failed: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} error: {e}")
            failed += 1
    
    print("\n" + "=" * 50)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 50)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)