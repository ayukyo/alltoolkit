#!/usr/bin/env python3
"""
diff_utils 示例：基础使用

演示基本的差异比较和相似度计算功能。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from diff_utils.mod import (
    diff_lines, diff_chars, diff_words,
    compute_diff_result,
    similarity_score,
    get_change_summary
)


def demo_line_diff():
    """演示行级差异比较"""
    print("=" * 60)
    print("行级差异比较示例")
    print("=" * 60)
    
    old_text = """第一行
第二行
第三行
第四行"""
    
    new_text = """第一行
修改的第二行
第三行
新增的第五行"""
    
    print(f"\n原文:\n{old_text}")
    print(f"\n新文:\n{new_text}")
    
    result = compute_diff_result(old_text, new_text, level="line")
    
    print(f"\n差异统计:")
    print(f"  - 相似度: {result.similarity:.2%}")
    print(f"  - 添加: {result.additions} 行")
    print(f"  - 删除: {result.deletions} 行")
    print(f"  - 变更: {result.changes} 行")
    print(f"  - 未变: {result.unchanged} 行")
    
    print(f"\n详细差异:")
    diff = diff_lines(old_text, new_text)
    for op_type, lines in diff:
        prefix = {
            'equal': '  ',
            'insert': '+ ',
            'delete': '- '
        }.get(op_type.value, '  ')
        for line in lines:
            print(f"{prefix}{line}")


def demo_char_diff():
    """演示字符级差异比较"""
    print("\n" + "=" * 60)
    print("字符级差异比较示例")
    print("=" * 60)
    
    old_text = "Hello, World!"
    new_text = "Hello, Python!"
    
    print(f"\n原文: {old_text}")
    print(f"新文: {new_text}")
    
    diff = diff_chars(old_text, new_text)
    
    print("\n字符差异:")
    for op_type, text in diff:
        if op_type.value == 'equal':
            print(f"  相同: '{text}'")
        elif op_type.value == 'delete':
            print(f"  删除: '{text}'")
        elif op_type.value == 'insert':
            print(f"  插入: '{text}'")


def demo_word_diff():
    """演示词级差异比较"""
    print("\n" + "=" * 60)
    print("词级差异比较示例")
    print("=" * 60)
    
    old_text = "The quick brown fox jumps over the lazy dog"
    new_text = "The slow gray cat walks under the active dog"
    
    print(f"\n原文: {old_text}")
    print(f"新文: {new_text}")
    
    diff = diff_words(old_text, new_text)
    
    print("\n词差异:")
    for op_type, words in diff:
        text = ''.join(words)
        if op_type.value == 'equal':
            print(f"  相同: '{text}'")
        elif op_type.value == 'delete':
            print(f"  删除: '{text}'")
        elif op_type.value == 'insert':
            print(f"  插入: '{text}'")


def demo_similarity():
    """演示相似度计算"""
    print("\n" + "=" * 60)
    print("相似度计算示例")
    print("=" * 60)
    
    pairs = [
        ("hello", "hallo"),
        ("kitten", "sitting"),
        ("completely different", "totally unrelated"),
        ("same text", "same text"),
        ("中文测试", "中文示例"),
    ]
    
    methods = ["levenshtein", "jaccard", "cosine", "damerau"]
    
    print(f"\n{'文本1':<25} {'文本2':<25} " + " ".join(f"{m:>10}" for m in methods))
    print("-" * 100)
    
    for s1, s2 in pairs:
        scores = [similarity_score(s1, s2, m) for m in methods]
        print(f"{s1:<25} {s2:<25} " + " ".join(f"{s:>10.1%}" for s in scores))


def demo_change_summary():
    """演示变更摘要"""
    print("\n" + "=" * 60)
    print("变更摘要示例")
    print("=" * 60)
    
    examples = [
        ("相同文本", "相同文本", "相同文本"),
        ("简单添加", "line1", "line1\nline2"),
        ("简单删除", "line1\nline2", "line1"),
        ("复杂修改", "function old() {\n  return 1;\n}", "function new() {\n  return 2;\n}"),
    ]
    
    for name, old, new in examples:
        summary = get_change_summary(old, new)
        print(f"\n{name}:")
        print(f"  原文: {old[:30]}{'...' if len(old) > 30 else ''}")
        print(f"  新文: {new[:30]}{'...' if len(new) > 30 else ''}")
        print(f"  摘要: {summary}")


if __name__ == "__main__":
    demo_line_diff()
    demo_char_diff()
    demo_word_diff()
    demo_similarity()
    demo_change_summary()
    
    print("\n" + "=" * 60)
    print("示例演示完成!")
    print("=" * 60)