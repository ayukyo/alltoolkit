#!/usr/bin/env python3
"""
boyer_moore_utils/boyer_moore_utils_test.py - Boyer-Moore 字符串搜索工具测试
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    # 核心搜索函数
    boyer_moore_search,
    boyer_moore_find_all,
    boyer_moore_count,
    boyer_moore_replace,
    
    # 搜索结果详情
    SearchResult,
    boyer_moore_find_with_context,
    
    # 多模式搜索
    boyer_moore_multi_search,
    boyer_moore_multi_find_first,
    
    # 性能分析
    SearchStats,
    boyer_moore_search_with_stats,
    compare_with_naive,
    
    # 便捷函数
    search,
    find_all,
    contains,
    starts_with,
    ends_with,
)


def test_basic_search():
    """测试基本搜索功能"""
    print("=== 测试基本搜索 ===")
    
    # 简单搜索
    assert boyer_moore_search("hello world", "world") == 6
    assert boyer_moore_search("hello world", "hello") == 0
    assert boyer_moore_search("hello world", "o w") == 4
    
    # 未找到
    assert boyer_moore_search("hello world", "xyz") == -1
    
    # 空模式
    assert boyer_moore_search("hello", "") == 0
    
    # 模式比文本长
    assert boyer_moore_search("hi", "hello") == -1
    
    # 重复模式
    assert boyer_moore_search("abababab", "aba") == 0
    
    print("✓ 基本搜索测试通过")


def test_case_sensitivity():
    """测试大小写敏感"""
    print("=== 测试大小写敏感 ===")
    
    # 区分大小写
    assert boyer_moore_search("Hello World", "world") == -1
    assert boyer_moore_search("Hello World", "World") == 6
    
    # 不区分大小写
    assert boyer_moore_search("Hello World", "world", case_sensitive=False) == 6
    assert boyer_moore_search("Hello World", "HELLO", case_sensitive=False) == 0
    
    # 全大写
    assert boyer_moore_search("HELLO WORLD", "hello", case_sensitive=False) == 0
    
    print("✓ 大小写敏感测试通过")


def test_find_all():
    """测试查找所有出现位置"""
    print("=== 测试查找所有位置 ===")
    
    # 多个匹配
    assert boyer_moore_find_all("hello hello hello", "hello") == [0, 6, 12]
    
    # 重叠匹配（不允许重叠）
    assert boyer_moore_find_all("abababab", "aba") == [0, 4]
    
    # 重叠匹配（允许重叠）
    assert boyer_moore_find_all("abababab", "aba", overlap=True) == [0, 2, 4]
    
    # 无匹配
    assert boyer_moore_find_all("hello world", "xyz") == []
    
    # 单个匹配
    assert boyer_moore_find_all("hello world", "world") == [6]
    
    print("✓ 查找所有位置测试通过")


def test_count():
    """测试计数功能"""
    print("=== 测试计数功能 ===")
    
    assert boyer_moore_count("hello hello hello", "hello") == 3
    assert boyer_moore_count("ababab", "aba") == 1  # 不重叠计数：aba 在位置 0
    assert boyer_moore_count("hello world", "xyz") == 0
    assert boyer_moore_count("aaaa", "aa") == 2  # 不重叠计数：aa 在位置 0 和 2
    
    # 大小写不敏感
    assert boyer_moore_count("Hello hello HELLO", "hello", case_sensitive=False) == 3
    
    print("✓ 计数功能测试通过")


def test_replace():
    """测试替换功能"""
    print("=== 测试替换功能 ===")
    
    # 全部替换
    assert boyer_moore_replace("hello world hello", "hello", "hi") == "hi world hi"
    
    # 限制替换次数
    assert boyer_moore_replace("hello world hello", "hello", "hi", count=1) == "hi world hello"
    
    # 无匹配
    assert boyer_moore_replace("hello world", "xyz", "abc") == "hello world"
    
    # 大小写不敏感
    result = boyer_moore_replace("Hello hello HELLO", "hello", "hi", case_sensitive=False)
    assert result == "hi hi hi"
    
    print("✓ 替换功能测试通过")


def test_search_result():
    """测试搜索结果对象"""
    print("=== 测试搜索结果对象 ===")
    
    # 创建搜索结果
    result = SearchResult(5, "test", "before ", " after")
    assert result.position == 5
    assert result.start == 5
    assert result.end == 9
    assert result.matched == "test"
    assert result.context_before == "before "
    assert result.context_after == " after"
    
    # 转换为字典
    d = result.to_dict()
    assert d['position'] == 5
    assert d['matched'] == "test"
    
    print("✓ 搜索结果对象测试通过")


def test_find_with_context():
    """测试带上下文的搜索"""
    print("=== 测试带上下文搜索 ===")
    
    text = "The quick brown fox jumps over the lazy dog. The fox was very quick."
    results = boyer_moore_find_with_context(text, "fox", context_len=10)
    
    assert len(results) == 2
    assert results[0].position == 16
    assert results[0].matched == "fox"
    assert results[1].position == 49
    
    # 检查上下文
    assert "brown" in results[0].context_before
    assert "jumps" in results[0].context_after
    
    print("✓ 带上下文搜索测试通过")


def test_multi_search():
    """测试多模式搜索"""
    print("=== 测试多模式搜索 ===")
    
    text = "hello world, hello universe"
    patterns = ["hello", "world", "universe"]
    
    results = boyer_moore_multi_search(text, patterns)
    
    assert results["hello"] == [0, 13]
    assert results["world"] == [6]
    assert results["universe"] == [19]
    
    # 空结果
    results2 = boyer_moore_multi_search(text, ["xyz"])
    assert results2["xyz"] == []
    
    print("✓ 多模式搜索测试通过")


def test_multi_find_first():
    """测试查找最早出现的模式"""
    print("=== 测试查找最早出现的模式 ===")
    
    # 找到最早出现的
    pattern, pos = boyer_moore_multi_find_first("hello world", ["world", "hello"])
    assert pattern == "hello"
    assert pos == 0
    
    # 部分模式存在
    pattern, pos = boyer_moore_multi_find_first("hello world", ["xyz", "hello"])
    assert pattern == "hello"
    assert pos == 0
    
    # 所有模式都不存在
    pattern, pos = boyer_moore_multi_find_first("hello world", ["xyz", "abc"])
    assert pattern is None
    assert pos == -1
    
    print("✓ 查找最早出现测试通过")


def test_search_stats():
    """测试搜索统计"""
    print("=== 测试搜索统计 ===")
    
    pos, stats = boyer_moore_search_with_stats("hello world", "world")
    
    assert pos == 6
    assert stats.algorithm == "Boyer-Moore"
    assert stats.text_length == 11
    assert stats.pattern_length == 5
    assert stats.matches == 1
    assert stats.comparisons > 0
    assert stats.execution_time_ms >= 0
    
    # 转换为字典
    d = stats.to_dict()
    assert d['algorithm'] == "Boyer-Moore"
    
    print("✓ 搜索统计测试通过")


def test_compare_with_naive():
    """测试性能对比"""
    print("=== 测试性能对比 ===")
    
    text = "The quick brown fox jumps over the lazy dog."
    pattern = "fox"
    
    results = compare_with_naive(text, pattern)
    
    assert 'boyer_moore' in results
    assert 'naive' in results
    
    bm_stats = results['boyer_moore']
    naive_stats = results['naive']
    
    # 两种算法都应该找到相同的结果
    assert bm_stats.matches == naive_stats.matches
    
    # Boyer-Moore 通常比较次数更少（对于长模式）
    print(f"  Boyer-Moore 比较次数: {bm_stats.comparisons}")
    print(f"  朴素搜索比较次数: {naive_stats.comparisons}")
    
    print("✓ 性能对比测试通过")


def test_convenience_functions():
    """测试便捷函数"""
    print("=== 测试便捷函数 ===")
    
    # search
    assert search("hello world", "world") == 6
    
    # find_all
    assert find_all("hello hello", "hello") == [0, 6]
    
    # contains
    assert contains("hello world", "world") == True
    assert contains("hello world", "xyz") == False
    
    # starts_with
    assert starts_with("hello world", "hello") == True
    assert starts_with("hello world", "world") == False
    
    # ends_with
    assert ends_with("hello world", "world") == True
    assert ends_with("hello world", "hello") == False
    
    # 大小写不敏感
    assert contains("Hello World", "world", case_sensitive=False) == True
    assert starts_with("Hello World", "hello", case_sensitive=False) == True
    assert ends_with("Hello World", "WORLD", case_sensitive=False) == True
    
    print("✓ 便捷函数测试通过")


def test_edge_cases():
    """测试边界情况"""
    print("=== 测试边界情况 ===")
    
    # 空文本
    assert boyer_moore_search("", "test") == -1
    assert boyer_moore_search("", "") == 0
    
    # 空模式
    assert boyer_moore_search("hello", "") == 0
    
    # 单字符
    assert boyer_moore_search("a", "a") == 0
    assert boyer_moore_search("a", "b") == -1
    
    # 位置限制
    assert boyer_moore_search("hello world", "hello", start=1) == -1
    assert boyer_moore_search("hello world", "world", start=5) == 6
    assert boyer_moore_search("hello world", "hello", end=4) == -1
    
    # 超出范围的位置
    assert boyer_moore_search("hi", "hello", start=10) == -1
    
    print("✓ 边界情况测试通过")


def test_long_pattern():
    """测试长模式（Boyer-Moore 优势场景）"""
    print("=== 测试长模式 ===")
    
    # 构造一个长文本和长模式
    text = "a" * 1000 + "findme" + "a" * 1000
    pattern = "findme"
    
    pos = boyer_moore_search(text, pattern)
    assert pos == 1000
    
    # 统计比较次数
    pos, stats = boyer_moore_search_with_stats(text, pattern)
    
    # Boyer-Moore 应该比朴素搜索更快
    results = compare_with_naive(text, pattern)
    print(f"  文本长度: {len(text)}")
    print(f"  Boyer-Moore 比较次数: {results['boyer_moore'].comparisons}")
    print(f"  朴素搜索比较次数: {results['naive'].comparisons}")
    
    print("✓ 长模式测试通过")


def test_chinese_text():
    """测试中文文本搜索"""
    print("=== 测试中文文本搜索 ===")
    
    text = "你好世界，欢迎使用 Boyer-Moore 算法"
    
    # 中文搜索
    assert boyer_moore_search(text, "世界") == 2
    assert boyer_moore_search(text, "算法") == 22
    assert boyer_moore_count(text, "你") == 1
    
    # 查找所有
    positions = boyer_moore_find_all("你好你好你好", "你好")
    assert positions == [0, 2, 4]
    
    print("✓ 中文文本搜索测试通过")


def test_special_characters():
    """测试特殊字符"""
    print("=== 测试特殊字符 ===")
    
    # 包含换行符
    text = "hello\nworld\nhello"
    assert boyer_moore_search(text, "world") == 6
    assert boyer_moore_count(text, "hello") == 2
    
    # 包含制表符
    text = "hello\tworld"
    assert boyer_moore_search(text, "world") == 6
    
    # 包含特殊符号
    text = "a@b#c$d%e^f"
    assert boyer_moore_search(text, "#c$") == 3
    
    print("✓ 特殊字符测试通过")


def run_all_tests():
    """运行所有测试"""
    print("=" * 50)
    print("开始运行 Boyer-Moore 字符串搜索工具测试")
    print("=" * 50)
    
    test_basic_search()
    test_case_sensitivity()
    test_find_all()
    test_count()
    test_replace()
    test_search_result()
    test_find_with_context()
    test_multi_search()
    test_multi_find_first()
    test_search_stats()
    test_compare_with_naive()
    test_convenience_functions()
    test_edge_cases()
    test_long_pattern()
    test_chinese_text()
    test_special_characters()
    
    print("=" * 50)
    print("✅ 所有测试通过！")
    print("=" * 50)


if __name__ == "__main__":
    run_all_tests()