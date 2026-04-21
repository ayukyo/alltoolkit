#!/usr/bin/env python3
"""
boyer_moore_utils/examples/usage_examples.py - Boyer-Moore 字符串搜索使用示例

Boyer-Moore 算法是一种高效的字符串匹配算法，通过预处理模式串，
利用"坏字符规则"和"好后缀规则"跳过不必要的比较，实现高效的文本搜索。

特点：
- 平均时间复杂度 O(n/m)，其中 n 是文本长度，m 是模式长度
- 最坏时间复杂度 O(n+m)
- 模式越长，跳过越多，效率越高
- 适合长文本、长模式的高效搜索
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    boyer_moore_search,
    boyer_moore_find_all,
    boyer_moore_count,
    boyer_moore_replace,
    boyer_moore_find_with_context,
    boyer_moore_multi_search,
    boyer_moore_multi_find_first,
    boyer_moore_search_with_stats,
    compare_with_naive,
    search,
    find_all,
    contains,
    starts_with,
    ends_with,
    SearchResult,
    SearchStats,
)


def example_1_basic_search():
    """示例1: 基本搜索"""
    print("=" * 60)
    print("示例1: 基本搜索")
    print("=" * 60)
    
    text = "The quick brown fox jumps over the lazy dog."
    
    # 搜索单词
    pos = boyer_moore_search(text, "fox")
    print(f"文本: {text}")
    print(f"搜索 'fox': 位置 {pos}")
    print(f"匹配内容: '{text[pos:pos+3]}'")
    
    # 搜索不存在的单词
    pos = boyer_moore_search(text, "cat")
    print(f"搜索 'cat': 位置 {pos} (未找到)")
    
    # 使用便捷函数
    print(f"\n使用 contains() 检查是否存在:")
    print(f"  contains(text, 'fox'): {contains(text, 'fox')}")
    print(f"  contains(text, 'cat'): {contains(text, 'cat')}")
    
    print()


def example_2_case_sensitivity():
    """示例2: 大小写处理"""
    print("=" * 60)
    print("示例2: 大小写处理")
    print("=" * 60)
    
    text = "Hello World, HELLO world"
    
    # 区分大小写
    print(f"文本: {text}")
    print(f"区分大小写搜索 'hello': {boyer_moore_search(text, 'hello')}")
    print(f"区分大小写搜索 'Hello': {boyer_moore_search(text, 'Hello')}")
    
    # 不区分大小写
    print(f"不区分大小写搜索 'hello': {boyer_moore_search(text, 'hello', case_sensitive=False)}")
    
    # 查找所有出现（不区分大小写）
    positions = boyer_moore_find_all(text, "hello", case_sensitive=False)
    print(f"'hello' 所有出现位置（不区分大小写）: {positions}")
    
    print()


def example_3_find_all():
    """示例3: 查找所有匹配位置"""
    print("=" * 60)
    print("示例3: 查找所有匹配位置")
    print("=" * 60)
    
    text = "ababababab"
    
    # 不允许重叠
    positions = boyer_moore_find_all(text, "aba", overlap=False)
    print(f"文本: {text}")
    print(f"搜索 'aba'（不重叠）: {positions}")
    print(f"出现次数: {len(positions)}")
    
    # 允许重叠
    positions_overlap = boyer_moore_find_all(text, "aba", overlap=True)
    print(f"搜索 'aba'（允许重叠）: {positions_overlap}")
    print(f"出现次数: {len(positions_overlap)}")
    
    # 使用计数函数
    count = boyer_moore_count(text, "aba")
    print(f"使用 count() 计数: {count}")
    
    print()


def example_4_replace():
    """示例4: 替换文本"""
    print("=" * 60)
    print("示例4: 替换文本")
    print("=" * 60)
    
    text = "hello world, hello universe, hello galaxy"
    
    # 全部替换
    result = boyer_moore_replace(text, "hello", "hi")
    print(f"原文: {text}")
    print(f"全部替换 'hello' -> 'hi': {result}")
    
    # 限制替换次数
    result = boyer_moore_replace(text, "hello", "hi", count=2)
    print(f"替换前2次: {result}")
    
    # 大小写不敏感替换
    text_mixed = "Hello hello HELLO"
    result = boyer_moore_replace(text_mixed, "hello", "hi", case_sensitive=False)
    print(f"\n原文: {text_mixed}")
    print(f"不区分大小写替换: {result}")
    
    print()


def example_5_context_search():
    """示例5: 带上下文的搜索"""
    print("=" * 60)
    print("示例5: 带上下文的搜索")
    print("=" * 60)
    
    text = """
    Python 是一种广泛使用的高级编程语言，由 Guido van Rossum 于 1991 年创建。
    Python 的设计哲学强调代码的可读性和简洁性，它的语法允许程序员用更少的代码行表达概念。
    Python 支持多种编程范式，包括面向对象、命令式、函数式和过程式编程。
    """
    
    # 搜索并获取上下文
    results = boyer_moore_find_with_context(text, "Python", context_len=15)
    
    print(f"搜索 'Python'，显示上下文（前后各15字符）:\n")
    for i, result in enumerate(results, 1):
        print(f"  [{i}] 位置 {result.position}:")
        print(f"      ...{result.context_before}[{result.matched}]{result.context_after}...")
        print()
    
    print()


def example_6_multi_pattern():
    """示例6: 多模式搜索"""
    print("=" * 60)
    print("示例6: 多模式搜索")
    print("=" * 60)
    
    text = "The quick brown fox jumps over the lazy dog. The fox was very quick."
    patterns = ["fox", "quick", "dog", "cat"]
    
    # 搜索多个模式
    results = boyer_moore_multi_search(text, patterns)
    
    print(f"文本: {text}")
    print(f"搜索模式: {patterns}")
    print(f"\n搜索结果:")
    for pattern, positions in results.items():
        if positions:
            print(f"  '{pattern}': 位置 {positions}")
        else:
            print(f"  '{pattern}': 未找到")
    
    # 找最早出现的模式
    first_pattern, first_pos = boyer_moore_multi_find_first(text, patterns)
    print(f"\n最早出现的模式: '{first_pattern}' 在位置 {first_pos}")
    
    print()


def example_7_prefix_suffix():
    """示例7: 前缀和后缀检查"""
    print("=" * 60)
    print("示例7: 前缀和后缀检查")
    print("=" * 60)
    
    text = "Hello, World!"
    
    print(f"文本: '{text}'")
    print(f"starts_with(text, 'Hello'): {starts_with(text, 'Hello')}")
    print(f"starts_with(text, 'World'): {starts_with(text, 'World')}")
    print(f"ends_with(text, 'World!'): {ends_with(text, 'World!')}")
    print(f"ends_with(text, 'Hello'): {ends_with(text, 'Hello')}")
    
    # 大小写不敏感
    print(f"\n大小写不敏感:")
    print(f"starts_with(text, 'hello', case_sensitive=False): {starts_with(text, 'hello', case_sensitive=False)}")
    print(f"ends_with(text, 'world!', case_sensitive=False): {ends_with(text, 'world!', case_sensitive=False)}")
    
    print()


def example_8_performance_comparison():
    """示例8: 性能对比"""
    print("=" * 60)
    print("示例8: 性能对比（Boyer-Moore vs 朴素搜索）")
    print("=" * 60)
    
    # 构造长文本
    text = "a" * 10000 + "findme" + "a" * 10000
    pattern = "findme"
    
    print(f"文本长度: {len(text)}")
    print(f"模式: '{pattern}'")
    
    # 性能对比
    results = compare_with_naive(text, pattern)
    
    bm = results['boyer_moore']
    naive = results['naive']
    
    print(f"\nBoyer-Moore:")
    print(f"  比较次数: {bm.comparisons}")
    print(f"  跳过次数: {bm.skips}")
    print(f"  执行时间: {bm.execution_time_ms:.4f} ms")
    print(f"  效率: {bm.efficiency:.2%}")
    
    print(f"\n朴素搜索:")
    print(f"  比较次数: {naive.comparisons}")
    print(f"  执行时间: {naive.execution_time_ms:.4f} ms")
    
    # 计算提升
    comparison_reduction = (1 - bm.comparisons / naive.comparisons) * 100 if naive.comparisons > 0 else 0
    print(f"\n比较次数减少: {comparison_reduction:.1f}%")
    
    print()


def example_9_search_statistics():
    """示例9: 搜索统计信息"""
    print("=" * 60)
    print("示例9: 搜索统计信息")
    print("=" * 60)
    
    text = "The Boyer-Moore algorithm is efficient for string searching."
    pattern = "algorithm"
    
    # 获取详细统计
    pos, stats = boyer_moore_search_with_stats(text, pattern)
    
    print(f"文本: {text}")
    print(f"模式: '{pattern}'")
    print(f"\n搜索统计:")
    print(f"  算法: {stats.algorithm}")
    print(f"  文本长度: {stats.text_length}")
    print(f"  模式长度: {stats.pattern_length}")
    print(f"  找到位置: {pos}")
    print(f"  比较次数: {stats.comparisons}")
    print(f"  跳过次数: {stats.skips}")
    print(f"  匹配次数: {stats.matches}")
    print(f"  执行时间: {stats.execution_time_ms:.4f} ms")
    
    # 转换为字典
    stats_dict = stats.to_dict()
    print(f"\n统计信息字典: {stats_dict}")
    
    print()


def example_10_practical_use_cases():
    """示例10: 实际应用场景"""
    print("=" * 60)
    print("示例10: 实际应用场景")
    print("=" * 60)
    
    # 场景1: 日志分析
    log_data = """
    [2024-01-15 10:30:15] INFO: Server started on port 8080
    [2024-01-15 10:30:16] ERROR: Connection failed to database
    [2024-01-15 10:30:17] INFO: Retrying connection...
    [2024-01-15 10:30:18] ERROR: Timeout waiting for response
    [2024-01-15 10:30:19] INFO: Connection restored
    """
    
    print("场景1: 日志分析 - 查找所有错误")
    error_positions = boyer_moore_find_all(log_data, "ERROR")
    print(f"发现 {len(error_positions)} 个错误")
    for pos in error_positions:
        line_start = log_data.rfind('\n', 0, pos) + 1
        line_end = log_data.find('\n', pos)
        print(f"  {log_data[line_start:line_end].strip()}")
    
    # 场景2: 代码搜索
    code = '''
def calculate_sum(a, b):
    return a + b

def calculate_difference(a, b):
    return a - b

def calculate_product(a, b):
    return a * b
'''
    
    print("\n场景2: 代码搜索 - 查找所有函数定义")
    func_positions = boyer_moore_find_all(code, "def ")
    print(f"发现 {len(func_positions)} 个函数定义")
    for pos in func_positions:
        line_end = code.find('\n', pos)
        print(f"  {code[pos:line_end].strip()}")
    
    # 场景3: 敏感词过滤
    text = "这是一段包含敏感词的文本，需要进行敏感词过滤处理。"
    sensitive_words = ["敏感词", "过滤"]
    
    print("\n场景3: 敏感词检测")
    results = boyer_moore_multi_search(text, sensitive_words)
    for word, positions in results.items():
        if positions:
            print(f"  发现敏感词 '{word}' 在位置 {positions}")
    
    # 场景4: 数据验证
    email = "user@example.com"
    
    print("\n场景4: 数据验证 - 检查邮箱格式元素")
    print(f"邮箱: {email}")
    print(f"  包含 '@': {contains(email, '@')}")
    print(f"  包含 '.': {contains(email, '.')}")
    print(f"  以 '.com' 结尾: {ends_with(email, '.com')}")
    
    print()


def example_11_chinese_text():
    """示例11: 中文文本搜索"""
    print("=" * 60)
    print("示例11: 中文文本搜索")
    print("=" * 60)
    
    text = """
    人工智能（Artificial Intelligence，简称AI）是计算机科学的一个分支，
    旨在研究和开发能够模拟、延伸和扩展人类智能的理论、方法、技术及应用系统。
    人工智能的研究包括机器学习、深度学习、自然语言处理等多个领域。
    """
    
    # 搜索中文词汇
    pattern = "人工智能"
    positions = boyer_moore_find_all(text, pattern)
    
    print(f"搜索 '{pattern}':")
    print(f"  出现位置: {positions}")
    print(f"  出现次数: {len(positions)}")
    
    # 带上下文的搜索
    results = boyer_moore_find_with_context(text, "智能", context_len=10)
    print(f"\n搜索 '智能' 带上下文:")
    for r in results:
        print(f"  ...{r.context_before}[{r.matched}]{r.context_after}...")
    
    # 替换
    replaced = boyer_moore_replace(text, "人工智能", "AI")
    print(f"\n替换后:\n{replaced}")
    
    print()


def example_12_long_text_performance():
    """示例12: 长文本性能测试"""
    print("=" * 60)
    print("示例12: 长文本性能测试")
    print("=" * 60)
    
    # 生成一个长文本
    import random
    random.seed(42)
    
    # 创建一个大约 100KB 的文本
    words = ["apple", "banana", "cherry", "date", "elderberry", 
             "fig", "grape", "honeydew", "kiwi", "lemon"]
    
    # 生成文本并在末尾放置目标
    text_parts = [random.choice(words) + " " for _ in range(10000)]
    text = "".join(text_parts) + "TARGET_WORD " + "".join(text_parts[:100])
    
    pattern = "TARGET_WORD"
    
    print(f"文本长度: {len(text)} 字符")
    print(f"搜索模式: '{pattern}'")
    
    # 使用 Boyer-Moore 搜索
    pos, stats = boyer_moore_search_with_stats(text, pattern)
    
    print(f"\n搜索结果:")
    print(f"  找到位置: {pos}")
    print(f"  比较次数: {stats.comparisons}")
    print(f"  跳过次数: {stats.skips}")
    print(f"  效率: {stats.efficiency:.2%}")
    print(f"  执行时间: {stats.execution_time_ms:.4f} ms")
    
    # 与朴素搜索对比
    print("\n与朴素搜索对比:")
    comparison = compare_with_naive(text, pattern)
    print(f"  Boyer-Moore 比较次数: {comparison['boyer_moore'].comparisons}")
    print(f"  朴素搜索比较次数: {comparison['naive'].comparisons}")
    
    reduction = (1 - comparison['boyer_moore'].comparisons / comparison['naive'].comparisons) * 100
    print(f"  比较次数减少: {reduction:.1f}%")
    
    print()


def run_all_examples():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("Boyer-Moore 字符串搜索工具使用示例")
    print("=" * 60 + "\n")
    
    example_1_basic_search()
    example_2_case_sensitivity()
    example_3_find_all()
    example_4_replace()
    example_5_context_search()
    example_6_multi_pattern()
    example_7_prefix_suffix()
    example_8_performance_comparison()
    example_9_search_statistics()
    example_10_practical_use_cases()
    example_11_chinese_text()
    example_12_long_text_performance()
    
    print("\n" + "=" * 60)
    print("所有示例运行完成！")
    print("=" * 60)


if __name__ == "__main__":
    run_all_examples()