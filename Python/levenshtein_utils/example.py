#!/usr/bin/env python3
"""
Levenshtein Distance Utils 示例脚本
展示各种使用场景
"""

from mod import (
    levenshtein_distance,
    similarity,
    find_closest,
    find_all_closest,
    edit_sequence,
    apply_edits,
    damerau_levenshtein_distance,
    hamming_distance,
    ratio
)


def demo_spell_checker():
    """演示拼写检查器"""
    print("=" * 60)
    print("示例 1: 拼写检查器")
    print("=" * 60)
    
    dictionary = [
        "apple", "application", "applet", "appeal",
        "banana", "berry", "blueberry",
        "orange", "organic", "origin"
    ]
    
    # 选择距离明显最近的示例
    misspelled_words = ["banan", "orang", "berrie", "organik"]
    
    for word in misspelled_words:
        closest = find_closest(word, dictionary, return_distance=True)
        suggestions = find_all_closest(word, dictionary, top_n=3, threshold=0.5)
        
        print(f"\n输入: '{word}'")
        print(f"  最佳匹配: '{closest[0]}' (距离: {closest[1]})")
        print(f"  建议列表:")
        for suggestion, sim in suggestions:
            print(f"    - '{suggestion}' (相似度: {sim:.1%})")


def demo_fuzzy_search():
    """演示模糊搜索"""
    print("\n" + "=" * 60)
    print("示例 2: 模糊搜索")
    print("=" * 60)
    
    products = [
        "iPhone 15 Pro Max",
        "iPhone 15 Pro",
        "iPhone 15",
        "iPhone 14 Pro",
        "Samsung Galaxy S24",
        "Samsung Galaxy S23",
        "Google Pixel 8",
        "Google Pixel 8 Pro"
    ]
    
    queries = ["iphone pro", "samsng galxy", "pixl 8"]
    
    for query in queries:
        print(f"\n搜索: '{query}'")
        matches = find_all_closest(query, products, top_n=3, threshold=0.3)
        
        if matches:
            for i, (product, sim) in enumerate(matches, 1):
                print(f"  {i}. {product} ({sim:.1%})")
        else:
            print("  未找到匹配")


def demo_dna_sequence():
    """演示 DNA 序列比对"""
    print("\n" + "=" * 60)
    print("示例 3: DNA 序列比对")
    print("=" * 60)
    
    sequences = [
        ("AGCTAGCTAG", "AGCTAGGTAG"),
        ("ATCGATCGAT", "ATCGATCG"),
        ("GCTAGCTAGC", "GCTATCTAGC")
    ]
    
    for seq1, seq2 in sequences:
        dist = levenshtein_distance(seq1, seq2)
        sim = similarity(seq1, seq2)
        
        print(f"\n序列 1: {seq1}")
        print(f"序列 2: {seq2}")
        print(f"  编辑距离: {dist}")
        print(f"  相似度: {sim:.2%}")
        
        # 获取编辑操作
        _, ops = edit_sequence(seq1, seq2)
        mutations = [op for op, _ in ops if op != "equal"]
        print(f"  变异数: {len(mutations)}")


def demo_typo_correction():
    """演示自动纠错"""
    print("\n" + "=" * 60)
    print("示例 4: 自动纠错建议")
    print("=" * 60)
    
    correct_words = [
        "accommodate", "occurrence", "separate", "definitely",
        "necessary", "occasionally", "questionnaire", "mischievous"
    ]
    
    user_inputs = [
        "accomodate", "occurance", "seperate", "definately",
        "neccessary", "occassionally", "questionaire", "mischievious"
    ]
    
    print("\n常见拼写错误纠正:")
    for wrong, correct in zip(user_inputs, correct_words):
        dist = levenshtein_distance(wrong, correct)
        sim = similarity(wrong, correct)
        closest = find_closest(wrong, correct_words)
        
        print(f"\n  错误: '{wrong}'")
        print(f"  正确: '{correct}'")
        print(f"  建议: '{closest}' (正确: {'✓' if closest == correct else '✗'})")
        print(f"  距离: {dist}, 相似度: {sim:.1%}")


def demo_string_diff():
    """演示字符串差异可视化"""
    print("\n" + "=" * 60)
    print("示例 5: 字符串差异可视化")
    print("=" * 60)
    
    pairs = [
        ("kitten", "sitting"),
        ("Saturday", "Sunday"),
        ("algorithm", "logarithm")
    ]
    
    for s1, s2 in pairs:
        print(f"\n'{s1}' -> '{s2}'")
        dist, ops = edit_sequence(s1, s2)
        print(f"编辑距离: {dist}")
        
        print("操作步骤:")
        for op, data in ops:
            if op == "equal":
                i, j, length = data
                print(f"  ✓ 保持: '{s1[i:i+length]}'")
            elif op == "replace":
                i, char = data
                print(f"  ✗ 替换: 位置 {i} '{s1[i]}' -> '{char}'")
            elif op == "insert":
                i, char = data
                print(f"  + 插入: 位置 {i} '{char}'")
            elif op == "delete":
                i, length = data
                print(f"  - 删除: 位置 {i} '{s1[i:i+length]}'")


def demo_distance_comparison():
    """演示不同距离度量对比"""
    print("\n" + "=" * 60)
    print("示例 6: 不同距离度量对比")
    print("=" * 60)
    
    pairs = [
        ("abcd", "acbd"),
        ("ca", "abc"),
        ("kitten", "sitting"),
        ("book", "back")
    ]
    
    print("\n对比 Levenshtein 和 Damerau-Levenshtein:")
    print(f"{'字符串对':<25} {'L距离':<8} {'DL距离':<8} {'说明'}")
    print("-" * 60)
    
    for s1, s2 in pairs:
        l_dist = levenshtein_distance(s1, s2)
        dl_dist = damerau_levenshtein_distance(s1, s2)
        
        if dl_dist < l_dist:
            note = "相邻交换优势"
        else:
            note = "相同"
        
        print(f"{s1} -> {s2:<15} {l_dist:<8} {dl_dist:<8} {note}")


def demo_hamming_distance():
    """演示汉明距离应用"""
    print("\n" + "=" * 60)
    print("示例 7: 汉明距离 - 错误检测")
    print("=" * 60)
    
    # 模拟数据传输
    original = "1011010110"
    received = "1010010110"
    
    print(f"\n原始数据: {original}")
    print(f"接收数据: {received}")
    
    h_dist = hamming_distance(original, received)
    print(f"汉明距离: {h_dist} 位不同")
    
    # 找出错误位置
    errors = [i for i, (a, b) in enumerate(zip(original, received)) if a != b]
    print(f"错误位置: {errors}")


def demo_fuzzywuzzy_compatibility():
    """演示与 fuzzywuzzy 库的兼容性"""
    print("\n" + "=" * 60)
    print("示例 8: FuzzyWuzzy 兼容比率")
    print("=" * 60)
    
    pairs = [
        ("hello world", "hello"),
        ("fuzzy string matching", "fuzzy matching"),
        ("Levenshtein distance", "Levenstein distance"),
        ("completely different", "totally unrelated")
    ]
    
    print(f"\n{'字符串 1':<30} {'字符串 2':<25} {'比率'}")
    print("-" * 80)
    
    for s1, s2 in pairs:
        r = ratio(s1, s2)
        sim = similarity(s1, s2)
        print(f"{s1:<30} {s2:<25} {r:.1f}% ({sim:.1%})")


if __name__ == "__main__":
    demo_spell_checker()
    demo_fuzzy_search()
    demo_dna_sequence()
    demo_typo_correction()
    demo_string_diff()
    demo_distance_comparison()
    demo_hamming_distance()
    demo_fuzzywuzzy_compatibility()
    
    print("\n" + "=" * 60)
    print("演示完成!")
    print("=" * 60)