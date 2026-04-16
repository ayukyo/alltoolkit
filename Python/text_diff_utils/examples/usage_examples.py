#!/usr/bin/env python3
"""
文本差异比较工具集使用示例
Text Diff Utilities Usage Examples
"""

import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    diff_lines, diff_words, diff_chars,
    unified_diff, context_diff, html_diff, inline_diff,
    similarity_ratio, levenshtein_distance, normalized_levenshtein,
    lcs, lcs_length, create_patch, apply_patch,
    get_diff_summary, text_diff_summary, TextDiffer,
    batch_diff, find_duplicate_blocks, DiffType
)


def print_section(title):
    """打印分节标题"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def example_basic_diff():
    """基础差异比较示例"""
    print_section("基础差异比较")
    
    old_text = """第一行：这是原始内容
第二行：保持不变
第三行：将被删除
第四行：也会被修改"""
    
    new_text = """第一行：这是原始内容
第二行：保持不变
第四行：已经被修改了
第五行：这是新增的行"""
    
    print("原始文本:")
    print(old_text)
    print("\n新文本:")
    print(new_text)
    
    # 按行比较
    result = diff_lines(old_text, new_text)
    
    print("\n差异统计:")
    stats = result.stats
    print(f"  新增行数: {stats['added']}")
    print(f"  删除行数: {stats['deleted']}")
    print(f"  替换行数: {stats['replaced']}")
    print(f"  未变行数: {stats['unchanged']}")
    print(f"  总变更数: {stats['total_changes']}")
    
    print("\n变更操作:")
    for op in result.get_changes():
        if op.type == DiffType.INSERT:
            print(f"  + INSERT [{op.new_start}:{op.new_end}]: {op.new_content[:40]}")
        elif op.type == DiffType.DELETE:
            print(f"  - DELETE [{op.old_start}:{op.old_end}]: {op.old_content[:40]}")
        else:
            print(f"  ~ REPLACE [{op.old_start}:{op.old_end}]: {op.old_content[:30]} -> {op.new_content[:30]}")


def example_unified_diff():
    """统一差异格式示例"""
    print_section("统一差异格式 (Unified Diff)")
    
    old_code = """def hello():
    print("Hello, World!")
    return True

def goodbye():
    print("Goodbye!")
    return False"""
    
    new_code = """def hello():
    print("Hello, Python!")
    return True

def greet(name):
    print(f"Hello, {name}!")
    return True

def goodbye():
    print("Goodbye, World!")
    return False"""
    
    diff = unified_diff(old_code, new_code, "original.py", "modified.py", n=2)
    
    print("统一差异格式输出:")
    print(diff)


def example_html_diff():
    """HTML 差异示例"""
    print_section("HTML 差异格式")
    
    old_text = "这是原始的第一行\n这是原始的第二行\n这是原始的第三行"
    new_text = "这是修改后的第一行\n这是原始的第二行\n这是新增的第四行"
    
    html = html_diff(old_text, new_text, "原文件.txt", "新文件.txt")
    
    # 保存到文件
    output_path = os.path.join(os.path.dirname(__file__), "diff_output.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"HTML 差异已保存到: {output_path}")
    print("\nHTML 预览（前 500 字符）:")
    print(html[:500] + "...")


def example_similarity():
    """相似度计算示例"""
    print_section("相似度计算")
    
    text_pairs = [
        ("hello world", "hello there"),
        ("The quick brown fox", "The slow brown dog"),
        ("完全相同的文本", "完全相同的文本"),
        ("abc", "xyz"),
        ("这是一个测试", "这是另一个测试"),
    ]
    
    print(f"{'文本 1':<25} {'文本 2':<25} {'相似度':<10} {'编辑距离':<10} {'归一化距离':<10}")
    print("-" * 80)
    
    for text1, text2 in text_pairs:
        sim = similarity_ratio(text1, text2)
        lev = levenshtein_distance(text1, text2)
        norm_lev = normalized_levenshtein(text1, text2)
        print(f"{text1[:22]:<25} {text2[:22]:<25} {sim:<10.2%} {lev:<10} {norm_lev:<10.2%}")


def example_lcs():
    """最长公共子序列示例"""
    print_section("最长公共子序列")
    
    pairs = [
        ("ABCDGH", "AEDFHR"),
        ("AGGTAB", "GXTXAYB"),
        ("hello world", "hello there"),
        ("这是一个测试文本", "这是另一个测试"),
    ]
    
    for s1, s2 in pairs:
        lcs_str = lcs(s1, s2)
        lcs_len = lcs_length(s1, s2)
        print(f"\n字符串 1: {s1}")
        print(f"字符串 2: {s2}")
        print(f"LCS: '{lcs_str}' (长度: {lcs_len})")


def example_word_char_diff():
    """单词和字符级差异示例"""
    print_section("单词级差异")
    
    old = "The quick brown fox jumps over the lazy dog"
    new = "The slow brown dog jumps over the lazy cat"
    
    print(f"原文本: {old}")
    print(f"新文本: {new}")
    print("\n单词级差异:")
    
    result = diff_words(old, new)
    output = []
    for word, diff_type in result:
        if diff_type == DiffType.INSERT:
            output.append(f"+{word}+")
        elif diff_type == DiffType.DELETE:
            output.append(f"-{word}-")
        else:
            output.append(word)
    
    print(" ".join(output))
    
    print_section("字符级差异")
    
    old = "kitten"
    new = "sitting"
    
    print(f"原文本: {old}")
    print(f"新文本: {new}")
    print("\n字符级差异:")
    
    result = diff_chars(old, new)
    output = []
    for char, diff_type in result:
        if diff_type == DiffType.INSERT:
            output.append(f"[+{char}]")
        elif diff_type == DiffType.DELETE:
            output.append(f"[-{char}]")
        else:
            output.append(char)
    
    print("".join(output))


def example_text_differ_class():
    """TextDiffer 类使用示例"""
    print_section("TextDiffer 类")
    
    # 创建比较器
    differ = TextDiffer(ignore_whitespace=True, ignore_case=False)
    
    old = "Hello World"
    new = "hello world"
    
    print(f"原文本: '{old}'")
    print(f"新文本: '{new}'")
    
    # 不忽略大小写时有差异
    result1 = differ.diff(old, new)
    print(f"\n忽略空白但不忽略大小写: has_changes={result1.has_changes()}")
    
    # 忽略大小写时无差异
    differ2 = TextDiffer(ignore_whitespace=True, ignore_case=True)
    result2 = differ2.diff(old, new)
    print(f"忽略空白和大小写: has_changes={result2.has_changes()}")
    
    # 计算相似度
    similarity = differ.similarity(old, new)
    print(f"\n相似度: {similarity:.2%}")


def example_patch():
    """补丁功能示例"""
    print_section("补丁功能")
    
    original = """def calculate(a, b):
    return a + b

def process():
    pass"""
    
    modified = """def calculate(a, b):
    return a + b

def process():
    print("Processing...")
    return True

def new_function():
    return "I'm new!" """
    
    print("原始代码:")
    print(original)
    print("\n修改后代码:")
    print(modified)
    
    # 创建补丁
    patch = create_patch(original, modified, "original.py", "modified.py")
    
    print("\n生成的补丁:")
    print(patch)
    
    # 保存补丁到文件
    patch_path = os.path.join(os.path.dirname(__file__), "changes.patch")
    with open(patch_path, "w", encoding="utf-8") as f:
        f.write(patch)
    
    print(f"\n补丁已保存到: {patch_path}")


def example_batch_diff():
    """批量差异比较示例"""
    print_section("批量差异比较")
    
    texts = [
        ("version 1.0", "version 2.0"),
        ("hello", "hallo"),
        ("same content", "same content"),
        ("delete this", ""),
        ("", "add this"),
    ]
    
    print(f"{'文本 1':<20} {'文本 2':<20} {'相似度':<10} {'有变化':<10}")
    print("-" * 60)
    
    results = batch_diff(texts)
    
    for (old, new), result in zip(texts, results):
        sim = similarity_ratio(old, new)
        print(f"{old[:17]:<20} {new[:17]:<20} {sim:<10.2%} {result.has_changes():<10}")


def example_summary():
    """差异摘要示例"""
    print_section("差异摘要")
    
    old = """第一章：开始
这是故事的开头。
主角出现了。

第二章：冒险
主角开始冒险。
遇到了挑战。

第三章：结局
故事结束了。"""
    
    new = """第一章：开始
这是故事的重新开始。
主角出现了。

第二章：冒险
主角开始大冒险。
遇到了新的挑战。
找到了宝藏。

第三章：结局
故事有了新的结局。
还有一个彩蛋。"""
    
    print("原始文本:")
    print(old[:100] + "...\n")
    
    print("新文本:")
    print(new[:100] + "...\n")
    
    # 获取详细摘要
    summary = get_diff_summary(old, new)
    
    print("详细摘要:")
    for key, value in summary.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.2%}")
        else:
            print(f"  {key}: {value}")
    
    # 获取人类可读摘要
    human_summary = text_diff_summary(old, new)
    print(f"\n人类可读摘要: {human_summary}")


def example_inline_diff():
    """内联差异示例"""
    print_section("内联差异格式")
    
    old = """apple
banana
cherry
date"""
    
    new = """apple
blueberry
cherry
elderberry"""
    
    diff = inline_diff(old, new, prefix_add="➕ ", prefix_del="➖ ", prefix_eq="   ")
    
    print("内联差异输出:")
    print(diff)


def main():
    """运行所有示例"""
    print("=" * 60)
    print("  文本差异比较工具集 - 使用示例")
    print("  Text Diff Utilities - Usage Examples")
    print("=" * 60)
    
    example_basic_diff()
    example_unified_diff()
    example_html_diff()
    example_similarity()
    example_lcs()
    example_word_char_diff()
    example_text_differ_class()
    example_patch()
    example_batch_diff()
    example_summary()
    example_inline_diff()
    
    print("\n" + "=" * 60)
    print("  所有示例运行完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()