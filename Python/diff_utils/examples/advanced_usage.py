#!/usr/bin/env python3
"""
diff_utils 示例：高级功能

演示格式化输出、补丁操作、合并冲突检测等高级功能。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from diff_utils.mod import (
    format_diff_unified, format_diff_context,
    format_diff_colored, format_diff_html, Colors,
    generate_patch, apply_patch,
    detect_merge_conflicts, format_conflict_markers,
    diff_statistics,
    find_similar_strings, find_longest_common_subsequence,
    highlight_differences
)


def demo_unified_diff():
    """演示 Unified Diff 格式"""
    print("=" * 60)
    print("Unified Diff 格式示例")
    print("=" * 60)
    
    old_text = """def hello():
    print("world")
    return True"""
    
    new_text = """def hello():
    print("hello")
    return False"""
    
    print(f"\n原文:\n{old_text}")
    print(f"\n新文:\n{new_text}")
    
    unified = format_diff_unified(
        old_text, new_text,
        context_lines=2,
        from_file="original.py",
        to_file="modified.py"
    )
    
    print("\nUnified Diff:")
    print(unified)


def demo_colored_diff():
    """演示彩色差异输出"""
    print("\n" + "=" * 60)
    print("彩色差异输出示例")
    print("=" * 60)
    
    old_text = """第一行
原始内容
最后一行"""
    
    new_text = """第一行
修改内容
最后一行"""
    
    print(f"\n原文:\n{old_text}")
    print(f"\n新文:\n{new_text}")
    
    colored = format_diff_colored(old_text, new_text, level="line")
    
    print("\n彩色输出 (行级):")
    print(colored)
    
    # 字符级
    old = "Hello World"
    new = "Hello Python"
    
    print(f"\n字符级差异: '{old}' -> '{new}'")
    colored_char = format_diff_colored(old, new, level="char")
    print(colored_char)


def demo_html_diff():
    """演示 HTML 输出"""
    print("\n" + "=" * 60)
    print("HTML 输出示例")
    print("=" * 60)
    
    old_text = """标题
原内容行"""
    
    new_text = """标题
新内容行"""
    
    html = format_diff_html(old_text, new_text, level="line")
    
    print("\n生成的 HTML (保存前 500 字符):")
    print(html[:500] + "...")
    
    # 可以保存到文件
    # with open("diff.html", "w") as f:
    #     f.write(html)


def demo_patch():
    """演示补丁生成与应用"""
    print("\n" + "=" * 60)
    print("补丁操作示例")
    print("=" * 60)
    
    original = """version = "1.0.0"
name = "old_name"
description = "Old description""""
    
    modified = """version = "2.0.0"
name = "new_name"
description = "New description""""
    
    print(f"\n原文:\n{original}")
    print(f"\n修改后:\n{modified}")
    
    # 生成补丁
    patch = generate_patch(original, modified)
    
    print("\n生成的补丁:")
    print(patch)
    
    # 应用补丁
    applied = apply_patch(original, patch)
    
    print("\n应用补丁后:")
    print(applied)


def demo_merge_conflicts():
    """演示合并冲突检测"""
    print("\n" + "=" * 60)
    print("合并冲突检测示例")
    print("=" * 60)
    
    base = """第一行
原始内容
第三行"""
    
    ours = """第一行
我们的修改
第三行"""
    
    theirs = """第一行
他们的修改
第三行"""
    
    print(f"\n基础版本:\n{base}")
    print(f"\n我们的版本:\n{ours}")
    print(f"\n他们的版本:\n{theirs}")
    
    conflicts = detect_merge_conflicts(base, ours, theirs)
    
    print(f"\n检测到 {len(conflicts)} 个冲突:")
    
    for i, conflict in enumerate(conflicts, 1):
        print(f"\n冲突 {i}:")
        print(f"  位置: 行 {conflict.start_line + 1} - {conflict.end_line + 1}")
        print(f"  我们的内容: {conflict.our_content}")
        print(f"  他们内容: {conflict.their_content}")
        
        markers = format_conflict_markers(conflict)
        print("\n  冲突标记:")
        for line in markers.split("\n"):
            print(f"    {line}")


def demo_similar_strings():
    """演示查找相似字符串"""
    print("\n" + "=" * 60)
    print("查找相似字符串示例")
    print("=" * 60)
    
    target = "python"
    candidates = [
        "python",
        "pyton",
        "python3",
        "pythonista",
        "programming",
        "program",
        "perl",
        "ruby",
        "java",
    ]
    
    print(f"\n目标: '{target}'")
    print(f"候选列表: {candidates}")
    
    similar = find_similar_strings(target, candidates, threshold=0.4)
    
    print(f"\n相似字符串 (阈值 0.4):")
    for string, score in similar:
        print(f"  '{string}': {score:.1%}")
    
    # 使用不同算法
    print("\n不同算法的比较:")
    for method in ["levenshtein", "jaccard", "cosine"]:
        similar = find_similar_strings(target, candidates, threshold=0.4, method=method)
        top3 = similar[:3]
        scores = [f"'{s}': {score:.0%}" for s, score in top3]
        print(f"  {method}: {', '.join(scores)}")


def demo_lcs():
    """演示最长公共子序列"""
    print("\n" + "=" * 60)
    print("最长公共子序列示例")
    print("=" * 60)
    
    pairs = [
        ("ABCDEF", "XYZABC"),
        ("programming", "programmer"),
        ("中文示例文本", "中文测试文本"),
        ("hello world", "hello there"),
    ]
    
    for s1, s2 in pairs:
        lcs = find_longest_common_subsequence(s1, s2)
        print(f"\n  '{s1}' 和 '{s2}'")
        print(f"  LCS: '{lcs}' (长度: {len(lcs)})")


def demo_highlight():
    """演示差异高亮"""
    print("\n" + "=" * 60)
    print("差异高亮示例")
    print("=" * 60)
    
    pairs = [
        ("Hello World", "Hello Python"),
        ("2023-01-01", "2024-01-01"),
        ("版本 1.0", "版本 2.0"),
    ]
    
    for old, new in pairs:
        h1, h2 = highlight_differences(old, new)
        print(f"\n  '{old}' -> '{new}'")
        print(f"  原文高亮: {h1}")
        print(f"  新文高亮: {h2}")


def demo_statistics():
    """演示差异统计"""
    print("\n" + "=" * 60)
    print("差异统计示例")
    print("=" * 60)
    
    old = """def function():
    pass
    
class OldClass:
    def method(self):
        return 1"""
    
    new = """def new_function():
    pass
    
class NewClass:
    def new_method(self):
        return 2"""
    
    stats = diff_statistics(old, new)
    
    print(f"\n原文 ({stats['old_lines']} 行)")
    print(f"新文 ({stats['new_lines']} 行)")
    
    print("\n统计信息:")
    print(f"  添加行数: {stats['additions']}")
    print(f"  删除行数: {stats['deletions']}")
    print(f"  变更总数: {stats['changes']}")
    print(f"  未变更数: {stats['unchanged']}")
    
    print("\n相似度 (不同算法):")
    print(f"  Levenshtein: {stats['similarity_levenshtein']:.1%}")
    print(f"  Jaccard: {stats['similarity_jaccard']:.1%}")
    print(f"  Cosine: {stats['similarity_cosine']:.1%}")
    
    print("\n变更行号:")
    print(f"  删除的行: {stats['deleted_line_numbers']}")
    print(f"  添加的行: {stats['added_line_numbers']}")


if __name__ == "__main__":
    demo_unified_diff()
    demo_colored_diff()
    demo_html_diff()
    demo_patch()
    demo_merge_conflicts()
    demo_similar_strings()
    demo_lcs()
    demo_highlight()
    demo_statistics()
    
    print("\n" + "=" * 60)
    print("高级功能示例演示完成!")
    print("=" * 60)