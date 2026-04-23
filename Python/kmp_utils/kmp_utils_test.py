#!/usr/bin/env python3
"""
kmp_utils_test.py - KMP 字符串搜索算法工具集测试

测试覆盖:
- 失败函数构建
- 单次/全部搜索
- 计数和替换
- 大小写不敏感搜索
- 批量模式匹配
- Aho-Corasick 自动机构建和搜索
- 边界检测（前缀/后缀/子串）
- 周期性字符串分析
- 边界分析
- 回文相关功能
- 高级功能

运行: python -m pytest kmp_utils_test.py -v
或直接运行: python kmp_utils_test.py
"""

import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kmp_utils.mod import (
    build_failure_function,
    build_next_array,
    search,
    search_all,
    count,
    replace,
    search_ignore_case,
    search_all_ignore_case,
    MatchResult,
    search_detailed,
    search_all_detailed,
    search_multiple_patterns,
    search_any_pattern,
    AhoCorasick,
    is_prefix,
    is_suffix,
    is_substring,
    find_smallest_period,
    is_periodic,
    get_period_unit,
    count_repetitions,
    get_borders,
    get_longest_border,
    longest_palindromic_prefix,
    longest_palindromic_suffix,
    minimum_append_for_palindrome,
    minimum_prepend_for_palindrome,
    find_all_occurrences_with_context,
    highlight_matches,
    split_by_pattern,
    search_iter,
    search_with_stats,
)


def test_build_failure_function():
    """测试失败函数构建"""
    print("\n=== 测试失败函数构建 ===")
    
    # 基本测试
    assert build_failure_function("") == []
    assert build_failure_function("A") == [0]
    assert build_failure_function("AA") == [0, 1]
    assert build_failure_function("AB") == [0, 0]
    
    # 复杂模式
    assert build_failure_function("ABABAC") == [0, 0, 1, 2, 3, 0]
    assert build_failure_function("AAAA") == [0, 1, 2, 3]
    assert build_failure_function("ABCDABCD") == [0, 0, 0, 0, 1, 2, 3, 4]
    
    # 常见模式
    assert build_failure_function("ABABCABAB") == [0, 0, 1, 2, 0, 1, 2, 3, 4]
    
    print("失败函数构建测试通过 ✓")


def test_build_next_array():
    """测试 next 数组构建"""
    print("\n=== 测试 next 数组构建 ===")
    
    assert build_next_array("") == []
    assert build_next_array("A") == [-1]
    assert build_next_array("ABABAC") == [-1, 0, 0, 1, 2, 3]
    assert build_next_array("AAAA") == [-1, 0, 1, 2]
    
    print("next 数组构建测试通过 ✓")


def test_search():
    """测试单次搜索"""
    print("\n=== 测试单次搜索 ===")
    
    # 基本搜索
    assert search("Hello World", "World") == 6
    assert search("Hello World", "Hello") == 0
    assert search("Hello World", "lo Wo") == 3
    
    # 未找到
    assert search("Hello World", "Python") == -1
    assert search("Hello", "Hello World") == -1  # 模式比文本长
    
    # 空模式
    assert search("Hello", "") == 0
    assert search("", "") == 0
    assert search("", "A") == -1
    
    # 边界情况
    assert search("AAAA", "AA") == 0
    assert search("ABCABCABC", "ABC") == 0
    assert search("ABABDABACDABABCABAB", "ABABCABAB") == 10
    
    # 指定起始位置
    assert search("ABCABC", "ABC", start=1) == 3
    assert search("ABCABC", "ABC", start=3) == 3
    assert search("ABCABC", "ABC", start=4) == -1
    
    print("单次搜索测试通过 ✓")


def test_search_all():
    """测试全部搜索"""
    print("\n=== 测试全部搜索 ===")
    
    # 基本搜索
    assert search_all("ABABABA", "ABA") == [0, 2, 4]  # ABABABA 有完整覆盖
    assert search_all("AAAA", "AA") == [0, 1, 2]
    assert search_all("ABCABCABC", "ABC") == [0, 3, 6]
    
    # 不重叠搜索
    assert search_all("ABABABA", "ABA", overlapping=False) == [0, 4]
    assert search_all("AAAA", "AA", overlapping=False) == [0, 2]
    
    # 空模式（匹配所有位置）
    assert search_all("ABC", "") == [0, 1, 2, 3]
    
    # 未找到
    assert search_all("ABC", "XYZ") == []
    
    # 边界情况
    assert search_all("A", "A") == [0]
    assert search_all("A", "AA") == []
    
    print("全部搜索测试通过 ✓")


def test_count():
    """测试计数"""
    print("\n=== 测试计数 ===")
    
    assert count("AAAA", "AA") == 3
    assert count("AAAA", "AA", overlapping=False) == 2
    assert count("ABCABCABC", "ABC") == 3
    assert count("Hello World", "l") == 3
    assert count("ABC", "XYZ") == 0
    
    print("计数测试通过 ✓")


def test_replace():
    """测试替换"""
    print("\n=== 测试替换 ===")
    
    assert replace("ABABAB", "AB", "XY") == "XYXYXY"
    assert replace("ABABAB", "AB", "XY", max_replace=2) == "XYXYAB"
    assert replace("Hello World", "World", "Python") == "Hello Python"
    assert replace("ABC", "XYZ", "123") == "ABC"  # 未找到不替换
    assert replace("", "", "X") == ""  # 空文本空模式
    
    print("替换测试通过 ✓")


def test_case_insensitive():
    """测试大小写不敏感搜索"""
    print("\n=== 测试大小写不敏感搜索 ===")
    
    assert search_ignore_case("Hello World", "WORLD") == 6
    assert search_ignore_case("Hello World", "hello") == 0
    assert search_ignore_case("Python", "PYTHON") == 0
    
    assert search_all_ignore_case("AbAbaBA", "aba") == [0, 2, 4]
    assert search_all_ignore_case("HELLO HELLO", "hello") == [0, 6]
    
    print("大小写不敏感搜索测试通过 ✓")


def test_match_result():
    """测试匹配结果对象"""
    print("\n=== 测试匹配结果对象 ===")
    
    # 详细搜索
    result = search_detailed("Hello World", "World")
    assert result is not None
    assert result.start == 6
    assert result.end == 11
    assert result.matched == "World"
    
    # 未找到
    assert search_detailed("Hello", "XYZ") is None
    
    # 上下文
    before, matched, after = result.context(2, 2)
    assert before == "o "
    assert matched == "World"
    assert after == ""
    
    # 全部详细搜索
    results = search_all_detailed("ABABAB", "ABA")
    assert len(results) == 2  # 位置 0 和 2
    assert results[0].matched == "ABA"
    assert results[0].start == 0
    assert results[1].start == 2
    
    # 等价性
    r1 = MatchResult("ABC", "AB", 0, 2)
    r2 = MatchResult("ABC", "AB", 0, 2)
    assert r1 == r2
    
    print("匹配结果对象测试通过 ✓")


def test_multiple_patterns():
    """测试批量模式匹配"""
    print("\n=== 测试批量模式匹配 ===")
    
    # 多模式搜索
    result = search_multiple_patterns("ABCDEFABC", ["ABC", "DEF", "XYZ"])
    assert result["ABC"] == [0, 6]
    assert result["DEF"] == [3]
    assert result["XYZ"] == []
    
    # 搜索任意模式
    pos, pattern = search_any_pattern("Hello World", ["World", "Hello"])
    assert pos == 0
    assert pattern == "Hello"
    
    pos, pattern = search_any_pattern("ABC", ["X", "Y", "Z"])
    assert pos == -1
    assert pattern == ""
    
    print("批量模式匹配测试通过 ✓")


def test_aho_corasick():
    """测试 Aho-Corasick 自动机"""
    print("\n=== 测试 Aho-Corasick 自动机 ===")
    
    # 基本构建和搜索
    ac = AhoCorasick(["he", "she", "his", "hers"])
    results = ac.search("ushers")
    
    # 检查结果（按结束位置排序）
    assert len(results) >= 3  # he, she, hers
    found_patterns = [p for _, p in results]
    assert "he" in found_patterns
    assert "she" in found_patterns
    assert "hers" in found_patterns
    
    # 带位置搜索
    ac2 = AhoCorasick(["AB", "BC", "ABC"])
    results2 = ac2.search_with_positions("ABCABC")
    assert len(results2) >= 4  # AB, BC, ABC, AB, BC, ABC
    
    # 检查具体位置
    for start, end, pattern in results2:
        assert pattern == "ABCABC"[start:end]
    
    # 简单模式
    ac3 = AhoCorasick(["A", "B"])
    results3 = ac3.search("ABC")
    assert len(results3) == 2  # A 和 B
    
    print("Aho-Corasick 自动机测试通过 ✓")


def test_boundary_detection():
    """测试边界检测"""
    print("\n=== 测试边界检测 ===")
    
    # 前缀检测
    assert is_prefix("Hello World", "Hello") == True
    assert is_prefix("Hello World", "World") == False
    assert is_prefix("Hello", "Hello World") == False  # 模式比文本长
    
    # 后缀检测
    assert is_suffix("Hello World", "World") == True
    assert is_suffix("Hello World", "Hello") == False
    
    # 子串检测
    assert is_substring("Hello World", "lo Wo") == True
    assert is_substring("Hello World", "xyz") == False
    
    print("边界检测测试通过 ✓")


def test_periodicity():
    """测试周期性字符串分析"""
    print("\n=== 测试周期性字符串分析 ===")
    
    # 最小周期
    assert find_smallest_period("ABCABCABC") == 3
    assert find_smallest_period("AAAA") == 1
    assert find_smallest_period("ABABAB") == 2
    assert find_smallest_period("ABCD") == 4  # 无周期
    assert find_smallest_period("") == 0
    
    # 周期性检测
    assert is_periodic("ABABAB") == True
    assert is_periodic("AAAA") == True
    assert is_periodic("ABABABC") == False
    assert is_periodic("A") == False
    
    # 周期单元
    assert get_period_unit("ABCABCABC") == "ABC"
    assert get_period_unit("AAAA") == "A"
    assert get_period_unit("ABCD") == "ABCD"
    
    # 重复次数
    assert count_repetitions("ABABAB") == 3
    assert count_repetitions("AAAA") == 4
    assert count_repetitions("ABCD") == 1
    
    print("周期性字符串分析测试通过 ✓")


def test_borders():
    """测试边界分析"""
    print("\n=== 测试边界分析 ===")
    
    # 所有边界
    borders = get_borders("ABABAB")
    assert "ABAB" in borders
    assert "AB" in borders
    assert "" in borders
    
    borders2 = get_borders("AAAA")
    assert "AAA" in borders2
    assert "AA" in borders2
    assert "A" in borders2
    
    # 无边界
    assert get_borders("ABCD") == [""]
    
    # 最长边界
    assert get_longest_border("ABABAB") == "ABAB"
    assert get_longest_border("AAAA") == "AAA"
    assert get_longest_border("ABCD") == ""
    
    print("边界分析测试通过 ✓")


def test_palindrome():
    """测试回文相关功能"""
    print("\n=== 测试回文相关功能 ===")
    
    # 最长回文前缀
    assert longest_palindromic_prefix("ABACABA") == "ABACABA"
    assert longest_palindromic_prefix("ABACABD") == "ABA"
    assert longest_palindromic_prefix("ABC") == "A"
    assert longest_palindromic_prefix("") == ""
    
    # 最长回文后缀
    assert longest_palindromic_suffix("ABACABA") == "ABACABA"
    assert longest_palindromic_suffix("ABACABD") == "D"  # 单字符回文后缀
    assert longest_palindromic_suffix("ABCABA") == "ABA"
    assert longest_palindromic_suffix("ABA") == "ABA"
    
    # 最少添加字符使成为回文
    assert minimum_append_for_palindrome("ABAC") == "ABA"  # ABAC + ABA = ABACABA
    assert minimum_append_for_palindrome("ABACABA") == ""
    assert minimum_append_for_palindrome("AACECAAA") == "CECAA"  # AACECAAA + CECAA = AACECAAACECAA
    
    assert minimum_prepend_for_palindrome("CABA") == "ABA"  # ABA + CABA = ABACABA
    assert minimum_prepend_for_palindrome("ABACABA") == ""
    
    print("回文相关功能测试通过 ✓")


def test_advanced_features():
    """测试高级功能"""
    print("\n=== 测试高级功能 ===")
    
    # 带上下文的搜索
    text = "The quick brown fox jumps"
    results = find_all_occurrences_with_context(text, "brown", 5)
    assert len(results) == 1
    assert results[0]["position"] == 10
    assert results[0]["match"] == "brown"
    assert "uick" in results[0]["before"]  # 5 chars before position 10
    assert "fox" in results[0]["after"]
    
    # 高亮匹配
    assert highlight_matches("Hello World", "World") == "Hello [[World]]"
    assert highlight_matches("ABABAB", "AB", "<b>", "</b>") == "<b>AB</b><b>AB</b><b>AB</b>"
    
    # 按模式分割
    assert split_by_pattern("A,B,C", ",") == ["A", "B", "C"]
    assert split_by_pattern("ABXABYAB", "AB") == ["", "X", "Y", ""]
    
    print("高级功能测试通过 ✓")


def test_generator():
    """测试生成器版本"""
    print("\n=== 测试生成器版本 ===")
    
    # 基本生成器
    positions = list(search_iter("ABABABA", "ABA"))  # ABABABA has 7 chars
    assert positions == [0, 2, 4]  # 完整的 ABA 匹配
    
    # 不重叠
    positions = list(search_iter("AAAA", "AA", overlapping=False))
    assert positions == [0, 2]
    
    # 空模式
    positions = list(search_iter("ABC", ""))
    assert positions == [0, 1, 2, 3]
    
    print("生成器版本测试通过 ✓")


def test_search_with_stats():
    """测试带统计的搜索"""
    print("\n=== 测试带统计的搜索 ===")
    
    stats = search_with_stats("ABABABAB", "AB")
    
    assert stats["pattern"] == "AB"
    assert stats["pattern_length"] == 2
    assert stats["text_length"] == 8
    assert stats["positions"] == [0, 2, 4, 6]
    assert stats["count"] == 4
    assert stats["build_time_seconds"] >= 0
    assert stats["search_time_seconds"] >= 0
    assert stats["failure_function"] == [0, 0]  # "AB" has no matching prefix-suffix
    
    print("带统计的搜索测试通过 ✓")


def test_edge_cases():
    """测试边界情况"""
    print("\n=== 测试边界情况 ===")
    
    # 空字符串
    assert search("", "") == 0
    assert search("", "A") == -1
    assert search_all("", "") == [0]
    assert search_all("", "A") == []
    
    # 单字符
    assert search("A", "A") == 0
    assert search("A", "B") == -1
    assert count("A", "A") == 1
    
    # 模式等于文本
    assert search("ABC", "ABC") == 0
    assert search_all("ABC", "ABC") == [0]
    
    # 重复字符
    assert search_all("AAAAAAAA", "AA") == [0, 1, 2, 3, 4, 5, 6]
    assert count("AAAAAAAA", "AA") == 7
    
    # 起始位置超出
    assert search("ABC", "A", start=10) == -1
    
    print("边界情况测试通过 ✓")


def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("KMP 字符串搜索算法工具集测试")
    print("=" * 60)
    
    try:
        test_build_failure_function()
        test_build_next_array()
        test_search()
        test_search_all()
        test_count()
        test_replace()
        test_case_insensitive()
        test_match_result()
        test_multiple_patterns()
        test_aho_corasick()
        test_boundary_detection()
        test_periodicity()
        test_borders()
        test_palindrome()
        test_advanced_features()
        test_generator()
        test_search_with_stats()
        test_edge_cases()
        
        print("\n" + "=" * 60)
        print("所有测试通过! ✓")
        print("=" * 60)
        return True
    except AssertionError as e:
        print(f"\n测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)