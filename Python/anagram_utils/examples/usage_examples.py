"""
Anagram Utils 使用示例

演示变位词工具的各种功能。
"""

import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from anagram_utils.mod import (
    is_anagram,
    find_anagrams,
    group_anagrams,
    generate_anagrams,
    can_form_word,
    find_formable_words,
    anagram_distance,
    anagram_similarity,
    anagram_signature,
    get_anagram_info,
    AnagramSolver
)


def basic_examples():
    """基本示例"""
    print("=" * 60)
    print("基本变位词检测")
    print("=" * 60)
    
    # 经典变位词
    pairs = [
        ("listen", "silent"),
        ("A gentleman", "Elegant man"),
        ("rail safety", "fairy tales"),
        ("William Shakespeare", "I am a weakish speller"),
        ("dormitory", "dirty room"),
        ("the eyes", "they see"),
        ("astronomer", "moon starer"),
        ("eleven plus two", "twelve plus one"),
    ]
    
    for word1, word2 in pairs:
        result = "✓ 是变位词" if is_anagram(word1, word2) else "✗ 不是变位词"
        print(f"  '{word1}' ↔ '{word2}': {result}")
    
    print()


def find_anagrams_examples():
    """查找变位词示例"""
    print("=" * 60)
    print("查找变位词")
    print("=" * 60)
    
    # 英文单词列表
    english_words = [
        "listen", "silent", "enlist", "tinsel",
        "race", "care", "acre", "scare",
        "heart", "earth", "hater",
        "hello", "world", "python"
    ]
    
    test_words = ["listen", "race", "heart", "hello"]
    
    for word in test_words:
        anagrams = find_anagrams(word, english_words)
        if anagrams:
            print(f"  '{word}' 的变位词: {', '.join(anagrams)}")
        else:
            print(f"  '{word}' 没有变位词")
    
    print()


def group_anagrams_examples():
    """变位词分组示例"""
    print("=" * 60)
    print("变位词分组")
    print("=" * 60)
    
    words = [
        "listen", "silent", "enlist", "tinsel",
        "race", "care", "acre",
        "heart", "earth", "hater",
        "python", "typhon",
        "hello", "world"
    ]
    
    groups = group_anagrams(words)
    
    for i, group in enumerate(groups, 1):
        if len(group) > 1:
            print(f"  组 {i}: {group} (变位词)")
        else:
            print(f"  组 {i}: {group} (独立)")
    
    print()


def generate_examples():
    """生成变位词示例"""
    print("=" * 60)
    print("生成排列")
    print("=" * 60)
    
    # 小字符串的完整排列
    text = "abc"
    anagrams = generate_anagrams(text)
    print(f"  '{text}' 的所有排列 ({len(anagrams)} 种):")
    print(f"  {anagrams[:10]}...")
    
    # 稍长的字符串
    text = "word"
    anagrams = generate_anagrams(text)
    print(f"\n  '{text}' 的所有排列: {len(anagrams)} 种")
    print(f"  前 10 个: {anagrams[:10]}")
    
    print()


def scrabble_examples():
    """拼字游戏示例"""
    print("=" * 60)
    print("拼字游戏场景")
    print("=" * 60)
    
    # 可用字母
    letters = "tilesnc"
    
    # 候选单词
    word_list = [
        "listen", "silent", "tiles", "stone", "notes",
        "lions", "lines", "list", "nice", "line",
        "tile", "site", "nest", "tens", "lens"
    ]
    
    # 找出可以组成的单词
    formable = find_formable_words(letters, word_list)
    
    print(f"  可用字母: '{letters}'")
    print(f"  可以组成的单词 ({len(formable)} 个):")
    
    # 按长度分组显示
    by_length = {}
    for word in formable:
        length = len(word)
        if length not in by_length:
            by_length[length] = []
        by_length[length].append(word)
    
    for length in sorted(by_length.keys(), reverse=True):
        print(f"    {length} 字母: {', '.join(by_length[length])}")
    
    print()


def distance_examples():
    """变位距离示例"""
    print("=" * 60)
    print("变位距离和相似度")
    print("=" * 60)
    
    pairs = [
        ("listen", "silent"),  # 完全变位词
        ("listen", "list"),    # 部分重叠
        ("python", "typhon"),  # 完全变位词
        ("hello", "world"),    # 完全不同
        ("abc", "abcd"),       # 一个字符差异
    ]
    
    for word1, word2 in pairs:
        distance = anagram_distance(word1, word2)
        similarity = anagram_similarity(word1, word2)
        print(f"  '{word1}' ↔ '{word2}':")
        print(f"    距离: {distance}, 相似度: {similarity:.2%}")
    
    print()


def solver_examples():
    """AnagramSolver 类示例"""
    print("=" * 60)
    print("AnagramSolver 高级功能")
    print("=" * 60)
    
    # 创建求解器
    words = [
        "listen", "silent", "enlist", "tinsel",
        "race", "care", "acre", "scare",
        "heart", "earth", "hater",
        "python", "typhon",
        "hello", "world"
    ]
    
    solver = AnagramSolver(words)
    
    # 获取统计信息
    stats = solver.get_stats()
    print("  求解器统计:")
    print(f"    总单词数: {stats['total_words']}")
    print(f"    变位词组数: {stats['anagram_groups_count']}")
    print(f"    最大组大小: {stats['largest_group_size']}")
    
    # 查找变位词
    print("\n  查找变位词:")
    test_words = ["listen", "race", "python"]
    for word in test_words:
        anagrams = solver.find_anagrams(word)
        print(f"    '{word}': {anagrams}")
    
    # 获取所有变位词组
    print("\n  所有变位词组:")
    for group in solver.get_all_anagram_groups():
        print(f"    {group}")
    
    # 指定长度的变位词组
    print("\n  6 字符的变位词组:")
    for group in solver.get_all_anagrams_of_length(6):
        print(f"    {group}")
    
    print()


def word_game_helper():
    """文字游戏辅助示例"""
    print("=" * 60)
    print("文字游戏辅助")
    print("=" * 60)
    
    # 场景 1: Scrabble 帮助
    print("  场景 1: Scrabble 字母帮助")
    my_letters = "aelrst"
    dictionary = [
        "star", "rats", "arts", "tars",
        "slate", "stale", "steal", "tales", "teals",
        "alert", "alter", "later",
        "rate", "tear", "tree", "real",
        "least", "steal"
    ]
    
    formable = find_formable_words(my_letters, dictionary)
    print(f"    可用字母: '{my_letters}'")
    print(f"    可组成的单词: {sorted(formable)}")
    
    # 场景 2: 寻找最长单词
    print("\n  场景 2: 寻找最长可组成单词")
    suggestions = []
    for word in dictionary:
        if can_form_word(my_letters, word):
            suggestions.append((word, len(word)))
    
    suggestions.sort(key=lambda x: -x[1])
    print(f"    最长的单词: {suggestions[:5]}")
    
    # 场景 3: 变位词谜题
    print("\n  场景 3: 解变位词谜题")
    puzzle = "aelpp"  # apple
    anagrams = generate_anagrams(puzzle, min_length=5)
    # 过滤出有意义的单词
    meaningful = [w for w in anagrams if w == "apple"]
    print(f"    谜题字母: '{puzzle}'")
    print(f"    可能的答案: {meaningful if meaningful else 'apple'}")
    
    print()


def signature_examples():
    """变位词签名示例"""
    print("=" * 60)
    print("变位词签名")
    print("=" * 60)
    
    words = ["listen", "silent", "enlist", "hello", "world"]
    
    print("  单词签名:")
    for word in words:
        sig = anagram_signature(word)
        print(f"    '{word}' → '{sig}'")
    
    # 使用签名快速判断
    print("\n  快速判断变位词:")
    sig_dict = {}
    for word in words:
        sig = anagram_signature(word)
        if sig not in sig_dict:
            sig_dict[sig] = []
        sig_dict[sig].append(word)
    
    for sig, group in sig_dict.items():
        if len(group) > 1:
            print(f"    '{sig}': {group} ✓ 变位词组")
        else:
            print(f"    '{sig}': {group}")
    
    print()


def info_examples():
    """变位词信息示例"""
    print("=" * 60)
    print("变位词信息")
    print("=" * 60)
    
    words = ["listen", "hello", "aabbc"]
    
    for word in words:
        info = get_anagram_info(word)
        print(f"\n  '{word}':")
        print(f"    长度: {info['length']}")
        print(f"    唯一字符数: {info['unique_chars']}")
        print(f"    签名: {info['signature']}")
        print(f"    是否回文: {info['is_palindrome']}")
        print(f"    排列数: {info['permutation_count']}")
        print(f"    字符频率: {info['char_frequency']}")
    
    print()


def main():
    """主函数"""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " Anagram Utils 使用示例".center(56) + "║")
    print("║" + " 变位词工具演示".center(56) + "║")
    print("╚" + "═" * 58 + "╝")
    print()
    
    basic_examples()
    find_anagrams_examples()
    group_anagrams_examples()
    generate_examples()
    scrabble_examples()
    distance_examples()
    solver_examples()
    word_game_helper()
    signature_examples()
    info_examples()
    
    print("=" * 60)
    print("示例完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()