#!/usr/bin/env python3
"""
usage_examples.py - KMP 字符串搜索算法工具集使用示例

示例覆盖:
- 基础字符串搜索
- 失败函数分析
- 批量模式匹配
- Aho-Corasick 多模式搜索
- 周期性字符串分析
- 回文分析
- 实际应用场景

运行: python usage_examples.py
"""

import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from kmp_utils.mod import (
    build_failure_function,
    build_next_array,
    search,
    search_all,
    count,
    replace,
    search_ignore_case,
    search_all_ignore_case,
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
    find_all_occurrences_with_context,
    highlight_matches,
    split_by_pattern,
    search_iter,
    search_with_stats,
)


def example_basic_search():
    """基础搜索示例"""
    print("\n" + "=" * 60)
    print("示例 1: 基础字符串搜索")
    print("=" * 60)
    
    text = "The quick brown fox jumps over the lazy dog"
    pattern = "brown"
    
    # 单次搜索
    pos = search(text, pattern)
    print(f"文本: '{text}'")
    print(f"模式: '{pattern}'")
    print(f"首次出现位置: {pos}")
    
    # 全部搜索
    text2 = "ABABABABABAB"
    pattern2 = "ABA"
    positions = search_all(text2, pattern2)
    print(f"\n文本: '{text2}'")
    print(f"模式: '{pattern2}'")
    print(f"所有出现位置: {positions}")
    
    # 不重叠搜索
    positions_no_overlap = search_all(text2, pattern2, overlapping=False)
    print(f"不重叠的出现位置: {positions_no_overlap}")
    
    # 计数
    cnt = count(text2, pattern2)
    print(f"匹配次数: {cnt}")
    
    # 替换
    replaced = replace(text2, pattern2, "XYZ")
    print(f"替换结果: '{replaced}'")


def example_failure_function():
    """失败函数分析示例"""
    print("\n" + "=" * 60)
    print("示例 2: 失败函数分析")
    print("=" * 60)
    
    patterns = ["ABABAC", "AAAA", "ABCDABCD", "ABCABCABC"]
    
    for pattern in patterns:
        fail = build_failure_function(pattern)
        next_arr = build_next_array(pattern)
        
        print(f"\n模式: '{pattern}'")
        print(f"失败函数: {fail}")
        print(f"next 数组: {next_arr}")
        
        # 解释失败函数
        print("解释:")
        for i, val in enumerate(fail):
            if val > 0:
                prefix = pattern[:val]
                suffix = pattern[i-val+1:i+1]
                print(f"  position {i}: pattern[{i}]='{pattern[i]}', "
                      f"最长匹配前缀='{prefix}', 长度={val}")


def example_case_insensitive():
    """大小写不敏感搜索示例"""
    print("\n" + "=" * 60)
    print("示例 3: 大小写不敏感搜索")
    print("=" * 60)
    
    text = "Python python PYTHON pYtHoN"
    pattern = "python"
    
    # 敏感搜索（只匹配小写）
    positions_sensitive = search_all(text, pattern)
    print(f"大小写敏感: {positions_sensitive}")
    
    # 不敏感搜索（匹配所有变体）
    positions_insensitive = search_all_ignore_case(text, pattern)
    print(f"大小写不敏感: {positions_insensitive}")


def example_match_details():
    """匹配详情示例"""
    print("\n" + "=" * 60)
    print("示例 4: 匹配详情")
    print("=" * 60)
    
    text = "Hello World, Welcome to Python Programming"
    pattern = "Python"
    
    # 详细搜索
    result = search_detailed(text, pattern)
    if result:
        print(f"匹配位置: {result.start} - {result.end}")
        print(f"匹配文本: '{result.matched}'")
        before, matched, after = result.context(10, 10)
        print(f"上下文: '{before}' ['{matched}] '{after}'")
    
    # 全部详细搜索
    text2 = "The cat sat on the mat with a bat"
    pattern2 = "at"
    results = search_all_detailed(text2, pattern2)
    print(f"\n文本: '{text2}'")
    print(f"模式: '{pattern2}'")
    print(f"匹配详情:")
    for r in results:
        print(f"  位置 {r.start}-{r.end}: '{r.matched}'")


def example_multiple_patterns():
    """批量模式匹配示例"""
    print("\n" + "=" * 60)
    print("示例 5: 批量模式匹配")
    print("=" * 60)
    
    text = "The quick brown fox jumps over the lazy dog"
    patterns = ["quick", "fox", "dog", "cat"]
    
    # 多模式搜索
    results = search_multiple_patterns(text, patterns)
    print(f"文本: '{text}'")
    print(f"模式列表: {patterns}")
    print("搜索结果:")
    for pattern, positions in results.items():
        if positions:
            print(f"  '{pattern}' 出现于位置: {positions}")
        else:
            print(f"  '{pattern}' 未找到")
    
    # 搜索任意模式
    pos, pattern = search_any_pattern(text, ["fox", "dog", "cat"])
    print(f"\n最早出现的模式: '{pattern}' 在位置 {pos}")


def example_aho_corasick():
    """Aho-Corasick 多模式搜索示例"""
    print("\n" + "=" * 60)
    print("示例 6: Aho-Corasick 多模式搜索")
    print("=" * 60)
    
    # 构建 Aho-Corasick 自动机
    patterns = ["he", "she", "his", "hers"]
    ac = AhoCorasick(patterns)
    
    text = "ushers"
    print(f"文本: '{text}'")
    print(f"模式列表: {patterns}")
    
    # 搜索
    results = ac.search(text)
    print("搜索结果（结束位置, 模式）:")
    for end_pos, matched_pattern in results:
        print(f"  位置 {end_pos}: '{matched_pattern}'")
    
    # 带位置信息搜索
    results_with_pos = ac.search_with_positions(text)
    print("\n详细位置:")
    for start, end, pattern in results_with_pos:
        print(f"  {start}-{end}: '{pattern}'")
    
    # 另一个示例 - 代码关键字搜索
    code = "function if else while for return break continue"
    keywords = ["if", "else", "for", "while", "function", "return"]
    ac2 = AhoCorasick(keywords)
    
    print(f"\n代码文本: '{code}'")
    print(f"关键字: {keywords}")
    results2 = ac2.search_with_positions(code)
    print("找到的关键字:")
    for start, end, keyword in sorted(results2):
        print(f"  {keyword} @ {start}-{end}")


def example_periodicity():
    """周期性字符串分析示例"""
    print("\n" + "=" * 60)
    print("示例 7: 周期性字符串分析")
    print("=" * 60)
    
    strings = ["ABCABCABC", "AAAA", "ABABAB", "ABCDABCDABCD", "ABABABC", "XYZ"]
    
    for s in strings:
        period = find_smallest_period(s)
        periodic = is_periodic(s)
        unit = get_period_unit(s)
        reps = count_repetitions(s)
        
        print(f"\n字符串: '{s}'")
        print(f"  是否周期性: {periodic}")
        print(f"  最小周期: {period}")
        print(f"  周期单元: '{unit}'")
        print(f"  重复次数: {reps}")
        
        if periodic:
            reconstructed = unit * reps
            print(f"  重构验证: '{reconstructed}' == '{s}' ✓")


def example_borders():
    """边界分析示例"""
    print("\n" + "=" * 60)
    print("示例 8: 边界分析")
    print("=" * 60)
    
    strings = ["ABABAB", "AAAA", "ABCDABCD", "ABCABC", "ABCD"]
    
    for s in strings:
        borders = get_borders(s)
        longest = get_longest_border(s)
        
        print(f"\n字符串: '{s}'")
        print(f"  所有边界: {borders}")
        print(f"  最长边界: '{longest}'")


def example_palindrome():
    """回文分析示例"""
    print("\n" + "=" * 60)
    print("示例 9: 回文分析")
    print("=" * 60)
    
    strings = ["ABACABA", "ABACABD", "ABAC", "AACECAAA"]
    
    for s in strings:
        prefix = longest_palindromic_prefix(s)
        suffix = longest_palindromic_suffix(s)
        append = minimum_append_for_palindrome(s)
        prepend = minimum_prepend_for_palindrome(s)
        
        print(f"\n字符串: '{s}'")
        print(f"  最长回文前缀: '{prefix}'")
        print(f"  最长回文后缀: '{suffix}'")
        
        if append:
            palindrome = s + append
            print(f"  尾部添加 '{append}' -> 回文 '{palindrome}'")
        else:
            print(f"  已经是回文!")
        
        if prepend:
            palindrome = prepend + s
            print(f"  开头添加 '{prepend}' -> 回文 '{palindrome}'")


def example_highlight_and_split():
    """高亮和分割示例"""
    print("\n" + "=" * 60)
    print("示例 10: 高亮和分割")
    print("=" * 60)
    
    # 高亮匹配
    text = "The quick brown fox jumps over the brown dog"
    pattern = "brown"
    
    print(f"原文: '{text}'")
    highlighted = highlight_matches(text, pattern, "**", "**")
    print(f"高亮: '{highlighted}'")
    
    html_highlighted = highlight_matches(text, pattern, "<mark>", "</mark>")
    print(f"HTML: '{html_highlighted}'")
    
    # 按模式分割
    csv = "apple,banana,orange,grape"
    parts = split_by_pattern(csv, ",")
    print(f"\nCSV: '{csv}'")
    print(f"分割: {parts}")
    
    log = "[INFO][2024][INFO][MESSAGE]"
    parts2 = split_by_pattern(log, "[INFO]")
    print(f"\n日志: '{log}'")
    print(f"分割: {parts2}")


def example_generator():
    """生成器示例"""
    print("\n" + "=" * 60)
    print("示例 11: 惰性生成器")
    print("=" * 60)
    
    # 大文本模拟
    text = "ABABABABABABABABABABABABABABABAB" * 10  # 模拟大文本
    pattern = "ABA"
    
    print(f"文本长度: {len(text)}")
    print(f"模式: '{pattern}'")
    
    # 使用生成器逐个获取匹配位置
    print("前 10 个匹配位置:")
    for i, pos in enumerate(search_iter(text, pattern)):
        if i >= 10:
            break
        print(f"  匹配 #{i+1}: 位置 {pos}")
    
    # 统计总匹配数
    total = sum(1 for _ in search_iter(text, pattern))
    print(f"总匹配数: {total}")


def example_search_stats():
    """搜索统计示例"""
    print("\n" + "=" * 60)
    print("示例 12: 搜索性能统计")
    print("=" * 60)
    
    # 模拟较长文本
    text = "The quick brown fox jumps over the lazy dog. " * 100
    pattern = "brown"
    
    stats = search_with_stats(text, pattern)
    
    print(f"文本长度: {stats['text_length']}")
    print(f"模式长度: {stats['pattern_length']}")
    print(f"匹配次数: {stats['count']}")
    print(f"匹配位置: {stats['positions'][:5]}...")  # 显示前5个
    print(f"失败函数构建时间: {stats['build_time_seconds']:.6f}s")
    print(f"搜索时间: {stats['search_time_seconds']:.6f}s")
    print(f"总时间: {stats['total_time_seconds']:.6f}s")


def example_context_search():
    """带上下文的搜索示例"""
    print("\n" + "=" * 60)
    print("示例 13: 带上下文的搜索")
    print("=" * 60)
    
    # 文本搜索场景
    article = """
    Python is a popular programming language created by Guido van Rossum.
    Python is known for its simplicity and readability. Many developers
    love Python because it allows them to write clean and maintainable code.
    Python has a rich ecosystem of libraries and frameworks.
    """
    
    keyword = "Python"
    
    print(f"搜索关键词: '{keyword}'")
    print("匹配结果:")
    
    results = find_all_occurrences_with_context(article.strip(), keyword, context_length=15)
    
    for i, result in enumerate(results, 1):
        print(f"\n  匹配 #{i}:")
        print(f"    位置: {result['position']}")
        print(f"    匹配: '{result['match']}'")
        print(f"    前文: ...'{result['before']}'")
        print(f"    后文: '{result['after']}'...")


def example_real_world():
    """实际应用场景示例"""
    print("\n" + "=" * 60)
    print("示例 14: 实际应用场景")
    print("=" * 60)
    
    # 场景 1: 日志分析
    print("\n场景 1: 日志关键字搜索")
    logs = """
    [ERROR] Connection failed at 10:30
    [INFO] Retry attempt 1
    [ERROR] Connection still failed at 10:31
    [INFO] Retry attempt 2
    [SUCCESS] Connection established at 10:32
    """
    
    error_count = count(logs, "ERROR")
    print(f"错误日志数: {error_count}")
    error_positions = search_all(logs, "ERROR")
    print(f"错误位置: {error_positions}")
    
    # 场景 2: DNA 序列分析
    print("\n场景 2: DNA 序列模式匹配")
    dna = "AGCTAGCTAGCTTAGCTAGCTAGCT"
    motif = "AGCT"
    
    positions = search_all(dna, motif)
    print(f"DNA 序列: '{dna}'")
    print(f"搜索 motif: '{motif}'")
    print(f"Motif 出现位置: {positions}")
    print(f"出现次数: {count(dna, motif)}")
    
    # 场景 3: 代码分析
    print("\n场景 3: 代码函数调用分析")
    code = "func_a(); func_b(); func_a(); func_c(); func_a();"
    
    call_count = count(code, "func_a")
    call_positions = search_all(code, "func_a")
    print(f"代码: '{code}'")
    print(f"'func_a' 调用次数: {call_count}")
    print(f"调用位置: {call_positions}")


def run_all_examples():
    """运行所有示例"""
    print("=" * 60)
    print("KMP 字符串搜索算法工具集使用示例")
    print("=" * 60)
    
    example_basic_search()
    example_failure_function()
    example_case_insensitive()
    example_match_details()
    example_multiple_patterns()
    example_aho_corasick()
    example_periodicity()
    example_borders()
    example_palindrome()
    example_highlight_and_split()
    example_generator()
    example_search_stats()
    example_context_search()
    example_real_world()
    
    print("\n" + "=" * 60)
    print("示例展示完成!")
    print("=" * 60)


if __name__ == "__main__":
    run_all_examples()