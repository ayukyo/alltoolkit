"""
Suffix Tree Utils 使用示例

演示后缀树的各种应用场景
"""

import sys
import os

# Add the module directory to the path
module_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, module_dir)

from mod import (
    SuffixTree, GeneralizedSuffixTree,
    find_all_occurrences,
    longest_repeated_substring,
    longest_common_substring,
    count_occurrences,
    build_suffix_array
)


def example_basic_search():
    """基本搜索示例"""
    print("=" * 50)
    print("示例 1: 基本模式搜索")
    print("=" * 50)
    
    text = "banana"
    st = SuffixTree(text)
    
    print(f"文本: {text}")
    print()
    
    # 搜索各种模式
    patterns = ["ban", "ana", "na", "xyz", ""]
    for pattern in patterns:
        positions = st.search(pattern)
        print(f"搜索 '{pattern}': {positions}")
    
    print()
    # 使用便捷函数
    print(f"find_all_occurrences('banana', 'ana'): {find_all_occurrences('banana', 'ana')}")


def example_count_and_contains():
    """计数和包含检查示例"""
    print("\n" + "=" * 50)
    print("示例 2: 计数和包含检查")
    print("=" * 50)
    
    text = "the quick brown fox jumps over the lazy dog"
    st = SuffixTree(text)
    
    print(f"文本: {text}")
    print()
    
    # 包含检查
    words = ["quick", "fox", "cat", "the"]
    print("包含检查:")
    for word in words:
        print(f"  包含 '{word}': {st.contains(word)}")
    
    print()
    # 计数
    patterns = ["the", "o", " ", "x"]
    print("出现次数:")
    for p in patterns:
        print(f"  '{p}' 出现 {st.count_occurrences(p)} 次")


def example_longest_repeated():
    """最长重复子串示例"""
    print("\n" + "=" * 50)
    print("示例 3: 最长重复子串")
    print("=" * 50)
    
    texts = [
        "banana",
        "mississippi",
        "abcdefg",  # 无重复
        "abcabcabc",
        "aaaaaa",
    ]
    
    for text in texts:
        st = SuffixTree(text)
        lrs = st.longest_repeated_substring()
        print(f"文本: '{text}' -> 最长重复子串: '{lrs}'")
    
    # 使用便捷函数
    print(f"\nlongest_repeated_substring('programming'): '{longest_repeated_substring('programming')}'")


def example_all_repeated():
    """所有重复子串示例"""
    print("\n" + "=" * 50)
    print("示例 4: 所有重复子串")
    print("=" * 50)
    
    text = "ababab"
    st = SuffixTree(text)
    
    print(f"文本: {text}")
    print()
    
    # 获取所有重复子串
    repeated = st.all_repeated_substrings(min_length=2)
    print(f"所有重复子串 (长度 >= 2):")
    for s in repeated:
        print(f"  '{s}' (长度: {len(s)})")
    
    print()
    # 按长度筛选
    repeated_long = st.all_repeated_substrings(min_length=3)
    print(f"所有重复子串 (长度 >= 3): {repeated_long}")


def example_longest_common_substring():
    """最长公共子串示例"""
    print("\n" + "=" * 50)
    print("示例 5: 最长公共子串")
    print("=" * 50)
    
    pairs = [
        ("hello world", "world peace"),
        ("programming", "programmer"),
        ("abcdefg", "xyz"),  # 无公共子串
        ("The quick brown fox", "The lazy dog"),
    ]
    
    for text1, text2 in pairs:
        gst = GeneralizedSuffixTree([text1, text2])
        lcs = gst.longest_common_substring()
        print(f"'{text1}' 与 '{text2}'")
        print(f"  最长公共子串: '{lcs}'")
        print()


def example_multiple_strings():
    """多字符串公共子串示例"""
    print("\n" + "=" * 50)
    print("示例 6: 多字符串公共子串")
    print("=" * 50)
    
    strings = [
        "information",
        "transform",
        "platform"
    ]
    
    print("字符串列表:")
    for i, s in enumerate(strings, 1):
        print(f"  {i}. {s}")
    
    gst = GeneralizedSuffixTree(strings)
    lcs = gst.longest_common_substring()
    
    print(f"\n所有字符串的最长公共子串: '{lcs}'")
    
    # 获取所有公共子串
    all_common = gst.all_common_substrings(min_length=2)
    print(f"\n所有公共子串 (长度 >= 2):")
    for s in all_common[:5]:  # 只显示前5个
        print(f"  '{s}'")


def example_palindrome():
    """回文检测示例"""
    print("\n" + "=" * 50)
    print("示例 7: 最长回文子串")
    print("=" * 50)
    
    texts = [
        "babad",
        "cbbd",
        "racecar",
        "abcba",
    ]
    
    for text in texts:
        st = SuffixTree(text)
        lps = st.longest_palindromic_substring()
        print(f"'{text}' 的最长回文子串: '{lps}'")


def example_suffix_array():
    """后缀数组示例"""
    print("\n" + "=" * 50)
    print("示例 8: 后缀数组")
    print("=" * 50)
    
    text = "banana"
    sa = build_suffix_array(text)
    
    print(f"文本: {text}")
    print(f"\n后缀数组 (排序后的后缀起始位置):")
    print(f"索引: {sa}")
    
    print(f"\n排序后的所有后缀:")
    for i, pos in enumerate(sa):
        print(f"  {i}: suffix[{pos}] = '{text[pos:]}'")


def example_practical_application():
    """实际应用示例"""
    print("\n" + "=" * 50)
    print("示例 9: 实际应用 - DNA 序列分析")
    print("=" * 50)
    
    # 模拟 DNA 序列
    dna1 = "ATCGATCGATCGATCG"
    dna2 = "GATCGATCGATCGATT"
    
    print("DNA 序列 1:", dna1)
    print("DNA 序列 2:", dna2)
    print()
    
    # 查找重复片段
    st1 = SuffixTree(dna1)
    print(f"序列 1 最长重复片段: '{st1.longest_repeated_substring()}'")
    
    # 查找共同片段
    gst = GeneralizedSuffixTree([dna1, dna2])
    print(f"共同最长片段: '{gst.longest_common_substring()}'")
    
    # 查找特定模式
    pattern = "ATCG"
    positions = st1.search(pattern)
    print(f"'{pattern}' 在序列 1 中出现的位置: {positions}")


def example_text_similarity():
    """文本相似度示例"""
    print("\n" + "=" * 50)
    print("示例 10: 文本相似度计算")
    print("=" * 50)
    
    def similarity(text1: str, text2: str) -> float:
        """基于最长公共子串的相似度"""
        if not text1 or not text2:
            return 0.0
        
        gst = GeneralizedSuffixTree([text1, text2])
        lcs = gst.longest_common_substring()
        return len(lcs) / max(len(text1), len(text2))
    
    pairs = [
        ("hello world", "hello there"),
        ("programming is fun", "programming is great"),
        ("completely different", "totally unrelated"),
    ]
    
    for text1, text2 in pairs:
        sim = similarity(text1, text2)
        print(f"相似度: {sim:.2%}")
        print(f"  '{text1}'")
        print(f"  '{text2}'")
        print()


def example_pattern_matching_benchmark():
    """模式匹配性能对比"""
    print("\n" + "=" * 50)
    print("示例 11: 模式匹配对比")
    print("=" * 50)
    
    import time
    
    text = "abcdefghij" * 100
    pattern = "cdefghij"
    
    # 后缀树搜索
    st = SuffixTree(text)
    
    # 预热
    st.search(pattern)
    
    # 后缀树搜索计时
    start = time.time()
    for _ in range(1000):
        st.search(pattern)
    suffix_tree_time = time.time() - start
    
    # Python 内置 find 计时
    start = time.time()
    for _ in range(1000):
        text.find(pattern)
    builtin_time = time.time() - start
    
    print(f"文本长度: {len(text)}")
    print(f"模式: '{pattern}'")
    print(f"\n1000 次搜索:")
    print(f"  后缀树: {suffix_tree_time:.4f}s")
    print(f"  Python 内置: {builtin_time:.4f}s")
    print(f"\n注意: 后缀树适合多次搜索同一文本的场景")


if __name__ == "__main__":
    example_basic_search()
    example_count_and_contains()
    example_longest_repeated()
    example_all_repeated()
    example_longest_common_substring()
    example_multiple_strings()
    example_palindrome()
    example_suffix_array()
    example_practical_application()
    example_text_similarity()
    example_pattern_matching_benchmark()
    
    print("\n" + "=" * 50)
    print("所有示例完成!")
    print("=" * 50)