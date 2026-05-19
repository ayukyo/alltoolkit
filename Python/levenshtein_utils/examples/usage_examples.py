"""
Levenshtein 工具模块使用示例
展示各种字符串相似度和模糊匹配功能
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    levenshtein_distance,
    levenshtein_distance_optimized,
    similarity_ratio,
    damerau_levenshtein_distance,
    fuzzy_search,
    fuzzy_match_one,
    edit_sequence,
    jaro_winkler_similarity,
    hamming_distance,
    longest_common_subsequence,
    longest_common_substring,
    fuzzy_replace,
    spell_check_suggestions,
    FuzzyMatcher,
    is_similar
)


def example_basic_distance():
    """基本距离计算示例"""
    print("=" * 50)
    print("1. 基本 Levenshtein 距离计算")
    print("=" * 50)
    
    pairs = [
        ("kitten", "sitting"),
        ("hello", "hallo"),
        ("python", "pytohn"),
        ("algorithm", "altruistic"),
        ("", "test"),
        ("same", "same"),
    ]
    
    for s1, s2 in pairs:
        dist = levenshtein_distance(s1, s2)
        ratio = similarity_ratio(s1, s2)
        print(f"'{s1}' → '{s2}'")
        print(f"  距离: {dist}, 相似度: {ratio:.2%}")
    
    print()


def example_optimized_distance():
    """优化版距离计算示例"""
    print("=" * 50)
    print("2. 优化版距离计算（适合长字符串）")
    print("=" * 50)
    
    # 对于长字符串，优化版更节省内存
    long_s1 = "algorithm" * 50
    long_s2 = "altruistic" * 50
    
    dist = levenshtein_distance_optimized(long_s1, long_s2)
    print(f"长字符串距离（长度 {len(long_s1)}）: {dist}")
    print()


def example_damerau_levenshtein():
    """Damerau-Levenshtein 距离示例"""
    print("=" * 50)
    print("3. Damerau-Levenshtein 距离（支持相邻交换）")
    print("=" * 50)
    
    pairs = [
        ("abcd", "acbd"),  # b 和 c 交换
        ("ca", "abc"),
        ("python", "pytohn"),  # o 和 h 交换
    ]
    
    for s1, s2 in pairs:
        standard = levenshtein_distance(s1, s2)
        damerau = damerau_levenshtein_distance(s1, s2)
        print(f"'{s1}' → '{s2}'")
        print(f"  标准 Levenshtein: {standard}")
        print(f"  Damerau-Levenshtein: {damerau}")
        if damerau < standard:
            print("  ✓ 检测到相邻字符交换！")
    print()


def example_similarity_comparison():
    """相似度比较示例"""
    print("=" * 50)
    print("4. 相似度比较")
    print("=" * 50)
    
    comparisons = [
        ("apple", "aple"),
        ("hello", "hallo"),
        ("world", "wordl"),
        ("python", "java"),
    ]
    
    for s1, s2 in comparisons:
        ratio = similarity_ratio(s1, s2)
        jw = jaro_winkler_similarity(s1, s2)
        print(f"'{s1}' vs '{s2}'")
        print(f"  标准相似度: {ratio:.2%}")
        print(f"  Jaro-Winkler: {jw:.2%}")
    print()


def example_fuzzy_search():
    """模糊搜索示例"""
    print("=" * 50)
    print("5. 模糊搜索")
    print("=" * 50)
    
    dictionary = [
        "apple", "application", "apply", "app",
        "banana", "bandana",
        "orange", "origin",
        "grape", "grapefruit"
    ]
    
    queries = ["aple", "banna", "orang", "grap"]
    
    for query in queries:
        print(f"\n搜索 '{query}':")
        results = fuzzy_search(query, dictionary, threshold=0.5, limit=5)
        for word, score in results:
            print(f"  {word}: {score:.2%}")
    print()


def example_fuzzy_match_one():
    """单个最佳匹配示例"""
    print("=" * 50)
    print("6. 单个最佳匹配")
    print("=" * 50)
    
    candidates = ["hello", "hallo", "hell", "help", "helmet"]
    
    queries = ["helo", "helo world", "xyz"]
    
    for query in queries:
        result = fuzzy_match_one(query, candidates, threshold=0.6)
        if result:
            print(f"'{query}' → '{result[0]}' (相似度: {result[1]:.2%})")
        else:
            print(f"'{query}' → 无匹配")
    print()


def example_edit_sequence():
    """编辑序列示例"""
    print("=" * 50)
    print("7. 编辑序列（将一个字符串转换为另一个的操作）")
    print("=" * 50)
    
    s1, s2 = "kitten", "sitting"
    print(f"将 '{s1}' 转换为 '{s2}':")
    
    ops = edit_sequence(s1, s2)
    for op_type, src_pos, dst_pos, char in ops:
        if op_type == 'match':
            print(f"  匹配 '{char}' @ 位置 {src_pos}")
        elif op_type == 'replace':
            print(f"  替换 @ 位置 {src_pos}: {char}")
        elif op_type == 'insert':
            print(f"  插入 '{char}' @ 位置 {dst_pos}")
        elif op_type == 'delete':
            print(f"  删除 '{char}' @ 位置 {src_pos}")
    print()


def example_jaro_winkler():
    """Jaro-Winkler 相似度示例"""
    print("=" * 50)
    print("8. Jaro-Winkler 相似度（对拼写错误更宽容）")
    print("=" * 50)
    
    pairs = [
        ("MARTHA", "MARHTA"),  # 交换
        ("DWAYNE", "DUANE"),
        ("DIXON", "DICKSONY"),
        ("crate", "trace"),
        ("crate", "crane"),  # 前缀相同
    ]
    
    for s1, s2 in pairs:
        jw = jaro_winkler_similarity(s1, s2)
        standard = similarity_ratio(s1, s2)
        print(f"'{s1}' vs '{s2}'")
        print(f"  标准: {standard:.2%}, Jaro-Winkler: {jw:.2%}")
    print()


def example_hamming_distance():
    """Hamming 距离示例"""
    print("=" * 50)
    print("9. Hamming 距离（仅限等长字符串）")
    print("=" * 50)
    
    pairs = [
        ("karolin", "kathrin"),
        ("1011101", "1001001"),
        ("AGCT", "AGGT"),
    ]
    
    for s1, s2 in pairs:
        try:
            dist = hamming_distance(s1, s2)
            print(f"'{s1}' vs '{s2}': {dist} 位不同")
        except ValueError as e:
            print(f"错误: {e}")
    print()


def example_lcs():
    """最长公共子序列/子串示例"""
    print("=" * 50)
    print("10. 最长公共子序列和子串")
    print("=" * 50)
    
    pairs = [
        ("ABCBDAB", "BDCABA"),
        ("programming", "program"),
        ("XMJYAUZ", "MZJAWXU"),
    ]
    
    for s1, s2 in pairs:
        lcs = longest_common_subsequence(s1, s2)
        lcs_str = longest_common_substring(s1, s2)
        print(f"'{s1}' vs '{s2}'")
        print(f"  最长公共子序列: '{lcs}' (长度: {len(lcs)})")
        print(f"  最长公共子串: '{lcs_str}' (长度: {len(lcs_str)})")
    print()


def example_fuzzy_replace():
    """模糊替换示例"""
    print("=" * 50)
    print("11. 模糊替换")
    print("=" * 50)
    
    text = "I have an aplpe and an appel and a appel"
    old_word = "apple"
    new_word = "orange"
    
    result, count = fuzzy_replace(text, old_word, new_word, threshold=0.6)
    
    print(f"原文本: {text}")
    print(f"模糊替换 '{old_word}' → '{new_word}':")
    print(f"结果: {result}")
    print(f"替换次数: {count}")
    print()


def example_spell_check():
    """拼写检查建议示例"""
    print("=" * 50)
    print("12. 拼写检查建议")
    print("=" * 50)
    
    dictionary = [
        "apple", "application", "apply", "approach",
        "banana", "balance",
        "orange", "origin", "original",
        "computer", "compute", "computerize"
    ]
    
    misspelled = ["aple", "aplicaton", "banan", "coputer", "oragne"]
    
    for word in misspelled:
        suggestions = spell_check_suggestions(word, dictionary, max_suggestions=3)
        print(f"'{word}' 的建议:")
        for suggestion, score in suggestions:
            print(f"  {suggestion}: {score:.2%}")
    print()


def example_fuzzy_matcher_class():
    """FuzzyMatcher 类使用示例"""
    print("=" * 50)
    print("13. FuzzyMatcher 类（支持缓存）")
    print("=" * 50)
    
    # 使用 Jaro-Winkler 作为相似度函数
    matcher = FuzzyMatcher(
        ["apple", "banana", "orange", "grape", "kiwi"],
        similarity_func=jaro_winkler_similarity
    )
    
    queries = ["aple", "banna", "orang", "grap"]
    
    print("查找最佳匹配:")
    for query in queries:
        result = matcher.find_best(query, threshold=0.7)
        if result:
            print(f"  '{query}' → '{result[0]}' ({result[1]:.2%})")
        else:
            print(f"  '{query}' → 无匹配")
    
    print("\n查找所有匹配 (阈值 0.5):")
    results = matcher.find_all("ap", threshold=0.5)
    for word, score in results:
        print(f"  {word}: {score:.2%}")
    
    print("\n动态添加候选:")
    matcher.add_candidate("apricot")
    result = matcher.find_best("apricot", threshold=0.9)
    if result:
        print(f"  'apricot' → '{result[0]}' ({result[1]:.2%})")
    
    print()


def example_chinese_text():
    """中文文本示例"""
    print("=" * 50)
    print("14. 中文文本处理")
    print("=" * 50)
    
    pairs = [
        ("北京", "背景"),  # 一字之差
        ("上海", "下海"),
        ("机器学习", "机器学习算法"),
        ("人工智能", "人能智能"),  # 两字交换
    ]
    
    for s1, s2 in pairs:
        dist = levenshtein_distance(s1, s2)
        ratio = similarity_ratio(s1, s2)
        jw = jaro_winkler_similarity(s1, s2)
        print(f"'{s1}' vs '{s2}'")
        print(f"  距离: {dist}, 标准相似度: {ratio:.2%}, Jaro-Winkler: {jw:.2%}")
    print()


def example_practical_use_cases():
    """实际应用场景示例"""
    print("=" * 50)
    print("15. 实际应用场景")
    print("=" * 50)
    
    # 场景1: 用户名匹配（防止重复注册）
    print("场景1: 防止相似用户名注册")
    existing_users = ["john_doe", "jane_doe", "admin", "administrator"]
    new_username = "john_doe2"
    
    similar = fuzzy_search(new_username, existing_users, threshold=0.7)
    if similar:
        print(f"  警告: '{new_username}' 与已有用户名相似:")
        for name, score in similar:
            print(f"    {name}: {score:.2%}")
    
    # 场景2: 搜索建议
    print("\n场景2: 搜索建议")
    products = ["iPhone 15", "iPhone 14", "iPad Pro", "MacBook Pro", "AirPods Pro"]
    query = "iphne"
    suggestions = fuzzy_search(query, products, threshold=0.5, limit=3)
    print(f"  搜索 '{query}' 的建议:")
    for product, score in suggestions:
        print(f"    {product}: {score:.2%}")
    
    # 场景3: 数据去重
    print("\n场景3: 数据去重")
    records = ["张三", "张 三", "张三三", "李四", "李 四"]
    unique = []
    for record in records:
        if not any(is_similar(record, u, threshold=0.9) for u in unique):
            unique.append(record)
        else:
            print(f"  跳过重复: '{record}'")
    print(f"  去重结果: {unique}")
    
    print()


def example_performance_comparison():
    """性能对比示例"""
    print("=" * 50)
    print("16. 性能对比（演示）")
    print("=" * 50)
    
    import time
    
    # 标准版 vs 优化版
    s1 = "algorithm" * 20  # 减少长度以加快演示
    s2 = "altruistic" * 20
    
    print(f"字符串长度: {len(s1)}")
    
    start = time.time()
    for _ in range(10):  # 减少迭代次数
        levenshtein_distance(s1, s2)
    standard_time = time.time() - start
    
    start = time.time()
    for _ in range(10):
        levenshtein_distance_optimized(s1, s2)
    optimized_time = time.time() - start
    
    print(f"标准版 10 次: {standard_time:.4f}s")
    print(f"优化版 10 次: {optimized_time:.4f}s")
    
    print()


if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("Levenshtein 工具模块 - 使用示例")
    print("=" * 50 + "\n")
    
    example_basic_distance()
    example_optimized_distance()
    example_damerau_levenshtein()
    example_similarity_comparison()
    example_fuzzy_search()
    example_fuzzy_match_one()
    example_edit_sequence()
    example_jaro_winkler()
    example_hamming_distance()
    example_lcs()
    example_fuzzy_replace()
    example_spell_check()
    example_fuzzy_matcher_class()
    example_chinese_text()
    example_practical_use_cases()
    example_performance_comparison()
    
    print("=" * 50)
    print("所有示例运行完成！")
    print("=" * 50)