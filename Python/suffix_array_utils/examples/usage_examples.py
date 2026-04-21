"""
Suffix Array Utils 使用示例

演示后缀数组工具的各种应用场景。
"""

import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    SuffixArray,
    SuffixArrayAdvanced,
    build_suffix_array,
    build_lcp_array,
    find_all_occurrences,
    longest_repeated_substring,
    longest_common_substring,
    count_distinct_substrings,
    pattern_exists,
)


def example_basic_usage():
    """基本用法示例"""
    print("=" * 60)
    print("1. 基本用法 - 构建后缀数组")
    print("=" * 60)
    
    text = "banana"
    sa = SuffixArray(text)
    
    print(f"文本: '{text}'")
    print(f"后缀数组: {sa.suffix_array}")
    print(f"LCP数组: {sa.lcp_array}")
    print()
    print("排序后的所有后缀:")
    for i, pos in enumerate(sa.suffix_array):
        print(f"  排名 {i}: 位置 {pos} -> '{text[pos:]}'")
    print()


def example_pattern_search():
    """模式匹配示例"""
    print("=" * 60)
    print("2. 模式匹配 - 查找子串位置")
    print("=" * 60)
    
    text = "abracadabra"
    sa = SuffixArray(text)
    
    print(f"文本: '{text}'")
    print()
    
    patterns = ["abra", "cad", "ra", "xyz"]
    for pattern in patterns:
        positions = sa.search(pattern)
        count = len(positions)
        if count > 0:
            print(f"模式 '{pattern}' 出现 {count} 次，位置: {positions}")
        else:
            print(f"模式 '{pattern}' 未找到")
    print()


def example_longest_repeated_substring():
    """最长重复子串示例"""
    print("=" * 60)
    print("3. 最长重复子串")
    print("=" * 60)
    
    texts = [
        "banana",
        "mississippi",
        "abcdefgh",
        "abcabcabc"
    ]
    
    for text in texts:
        sa = SuffixArray(text)
        substring, positions = sa.longest_repeated_substring()
        
        if substring:
            print(f"文本: '{text}'")
            print(f"  最长重复子串: '{substring}'")
            print(f"  出现位置: {positions}")
        else:
            print(f"文本: '{text}'")
            print(f"  无重复子串")
    print()


def example_longest_common_substring():
    """最长公共子串示例"""
    print("=" * 60)
    print("4. 最长公共子串")
    print("=" * 60)
    
    pairs = [
        ("programming", "grammatical"),
        ("abcdefg", "xyzabc"),
        ("hello world", "world peace"),
        ("nothing", "common")
    ]
    
    for text1, text2 in pairs:
        substring, positions = longest_common_substring(text1, text2)
        
        if substring:
            print(f"文本1: '{text1}'")
            print(f"文本2: '{text2}'")
            print(f"  最长公共子串: '{substring}'")
            print(f"  位置: text1[{positions[0]}], text2[{positions[1]}]")
        else:
            print(f"文本1: '{text1}', 文本2: '{text2}'")
            print(f"  无公共子串")
    print()


def example_distinct_substrings():
    """不同子串数量示例"""
    print("=" * 60)
    print("5. 统计不同子串数量")
    print("=" * 60)
    
    texts = ["aab", "abc", "aaaa", "abcd"]
    
    for text in texts:
        count = count_distinct_substrings(text)
        total = len(text) * (len(text) + 1) // 2
        print(f"文本: '{text}'")
        print(f"  总子串数: {total}")
        print(f"  不同子串数: {count}")
        print(f"  重复子串数: {total - count}")
    print()


def example_kth_substring():
    """第k小子串示例"""
    print("=" * 60)
    print("6. 按字典序找第k小的子串")
    print("=" * 60)
    
    text = "banana"
    sa = SuffixArray(text)
    
    print(f"文本: '{text}'")
    print(f"所有子串按字典序排序:")
    
    # 显示前几个
    all_substrings = []
    for i in range(len(text)):
        for j in range(i + 1, len(text) + 1):
            all_substrings.append(text[i:j])
    
    sorted_substrings = sorted(set(all_substrings))
    for i, sub in enumerate(sorted_substrings, 1):
        kth = sa.kth_substring(i)
        match = "✓" if kth == sub else "✗"
        if i <= 10:
            print(f"  第{i}小: '{kth}' {match}")
    
    print(f"  ... 共 {len(sorted_substrings)} 个不同子串")
    print()


def example_repeated_substrings():
    """所有重复子串示例"""
    print("=" * 60)
    print("7. 找出所有重复子串")
    print("=" * 60)
    
    text = "abcabcabc"
    sa = SuffixArray(text)
    
    print(f"文本: '{text}'")
    print("所有重复子串 (长度 >= 2):")
    
    repeats = sa.all_repeated_substrings(min_length=2)
    for substring, positions in repeats:
        print(f"  '{substring}': {len(positions)} 次, 位置: {positions}")
    print()


def example_convenience_functions():
    """便捷函数示例"""
    print("=" * 60)
    print("8. 便捷函数 - 一行代码完成任务")
    print("=" * 60)
    
    text = "the quick brown fox jumps over the lazy dog"
    
    # 快速查找
    positions = find_all_occurrences(text, "the")
    print(f"查找 'the' 在 '{text[:30]}...' 中: {positions}")
    
    # 快速检查
    exists = pattern_exists(text, "fox")
    print(f"'fox' 存在: {exists}")
    
    exists = pattern_exists(text, "cat")
    print(f"'cat' 存在: {exists}")
    
    # 快速构建
    sa_arr = build_suffix_array("banana")
    print(f"后缀数组: {sa_arr}")
    
    lcp_arr = build_lcp_array("banana")
    print(f"LCP数组: {lcp_arr}")
    print()


def example_advanced_usage():
    """高级用法示例"""
    print("=" * 60)
    print("9. 高级功能 - 两个后缀的LCP")
    print("=" * 60)
    
    text = "abracadabra"
    sa = SuffixArrayAdvanced(text)
    
    print(f"文本: '{text}'")
    
    # 计算不同后缀的LCP
    pairs = [(0, 3), (0, 7), (3, 5)]
    for i, j in pairs:
        suffix_i = text[i:]
        suffix_j = text[j:]
        lcp = sa.lcp_between_suffixes(i, j)
        print(f"后缀 '{suffix_i}' 和 '{suffix_j}' 的LCP: {lcp}")
    print()


def example_text_analysis():
    """文本分析示例"""
    print("=" * 60)
    print("10. 文本分析应用")
    print("=" * 60)
    
    # DNA序列分析
    dna = "GATATATAGAT"
    sa = SuffixArray(dna)
    
    print(f"DNA序列: '{dna}'")
    
    # 查找特定模式
    pattern = "ATA"
    positions = sa.search(pattern)
    print(f"模式 '{pattern}' 出现位置: {positions}")
    
    # 最长重复序列
    repeat, pos = sa.longest_repeated_substring()
    print(f"最长重复片段: '{repeat}'")
    
    # 子串多样性
    distinct = sa.distinct_substrings_count()
    print(f"不同子串数量: {distinct}")
    print()


def example_performance():
    """性能测试示例"""
    print("=" * 60)
    print("11. 性能测试")
    print("=" * 60)
    
    import time
    
    # 创建长文本
    text = "abcdefghij" * 1000
    
    print(f"文本长度: {len(text)}")
    
    # 构建时间
    start = time.time()
    sa = SuffixArray(text)
    build_time = time.time() - start
    print(f"构建时间: {build_time:.4f} 秒")
    
    # 查询时间
    start = time.time()
    for _ in range(100):
        sa.search("abcdefghij")
    search_time = time.time() - start
    print(f"100次查询时间: {search_time:.4f} 秒")
    
    # 最长重复子串
    start = time.time()
    substring, _ = sa.longest_repeated_substring()
    lcp_time = time.time() - start
    print(f"最长重复子串查找时间: {lcp_time:.4f} 秒")
    print(f"最长重复子串: '{substring[:50]}...' (长度 {len(substring)})")
    print()


def main():
    """运行所有示例"""
    example_basic_usage()
    example_pattern_search()
    example_longest_repeated_substring()
    example_longest_common_substring()
    example_distinct_substrings()
    example_kth_substring()
    example_repeated_substrings()
    example_convenience_functions()
    example_advanced_usage()
    example_text_analysis()
    example_performance()
    
    print("=" * 60)
    print("所有示例运行完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()