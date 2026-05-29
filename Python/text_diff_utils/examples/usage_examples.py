"""
text_diff_utils 使用示例

演示文本差异比较工具的各种功能。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    TextDiff, DiffType,
    diff_texts, unified_diff, similarity,
    find_common_substring, find_common_subsequences,
    highlight_diff_html, count_changes, diff_three_texts
)


def example_basic_comparison():
    """基本差异比较示例"""
    print("=" * 60)
    print("示例 1: 基本文本比较")
    print("=" * 60)
    
    original = """Hello World
This is a test document.
It has multiple lines.
Some lines are the same.
Goodbye!"""
    
    modified = """Hello World
This is a modified document.
It has multiple lines.
A new line was added here.
Some lines are the same.
See you later!"""
    
    diff = TextDiff(original, modified)
    
    print("\n--- 行级差异 ---")
    for dtype, content in diff.compare_lines():
        marker = {'equal': ' ', 'insert': '+', 'delete': '-'}[dtype.value]
        print(f"{marker} {content.rstrip()}")
    
    print(f"\n相似度: {diff.similarity():.2%}")


def example_char_level_diff():
    """字符级差异示例"""
    print("\n" + "=" * 60)
    print("示例 2: 字符级差异比较")
    print("=" * 60)
    
    old_text = "Hello, World!"
    new_text = "Hello, Python!"
    
    diff = TextDiff(old_text, new_text)
    
    print(f"\n原文: {old_text}")
    print(f"新文: {new_text}")
    print("\n字符级差异:")
    
    for dtype, content in diff.compare_chars():
        if dtype == DiffType.EQUAL:
            print(f"  相同: {repr(content)}")
        elif dtype == DiffType.DELETE:
            print(f"  删除: {repr(content)}")
        elif dtype == DiffType.INSERT:
            print(f"  插入: {repr(content)}")


def example_word_level_diff():
    """单词级差异示例"""
    print("\n" + "=" * 60)
    print("示例 3: 单词级差异比较")
    print("=" * 60)
    
    old_text = "The quick brown fox jumps over the lazy dog"
    new_text = "The fast brown cat leaps over the sleeping dog"
    
    diff = TextDiff(old_text, new_text)
    
    print(f"\n原文: {old_text}")
    print(f"新文: {new_text}")
    print("\n单词级差异:")
    
    result = []
    for dtype, content in diff.compare_words():
        if dtype == DiffType.DELETE:
            result.append(f"[-{content}-]")
        elif dtype == DiffType.INSERT:
            result.append(f"[+{content}+]")
        else:
            result.append(content)
    
    print("".join(result))


def example_unified_diff():
    """统一格式差异示例"""
    print("\n" + "=" * 60)
    print("示例 4: 统一格式差异 (类似 git diff)")
    print("=" * 60)
    
    original = """def greet(name):
    print("Hello, " + name)

def farewell(name):
    print("Goodbye, " + name)"""
    
    modified = """def greet(name, greeting="Hello"):
    print(greeting + ", " + name)

def farewell(name):
    print("See you later, " + name)

def welcome(name):
    print("Welcome, " + name)"""
    
    diff = unified_diff(original, modified, fromfile='greeting.py', tofile='greeting.py')
    print(diff)


def example_side_by_side():
    """并排格式差异示例"""
    print("\n" + "=" * 60)
    print("示例 5: 并排格式差异")
    print("=" * 60)
    
    original = """第一行
第二行
第三行
第四行"""
    
    modified = """第一行
第二行修改
新增行
第三行
第四行"""
    
    diff = TextDiff(original, modified)
    print(diff.side_by_side_text(width=30))


def example_similarity():
    """相似度计算示例"""
    print("\n" + "=" * 60)
    print("示例 6: 文本相似度计算")
    print("=" * 60)
    
    texts = [
        ("Hello World", "Hello World"),
        ("Hello World", "Hello There"),
        ("Hello World", "Hi There"),
        ("The quick brown fox", "The slow brown dog"),
        ("completely different", "totally unrelated"),
    ]
    
    print("\n文本对比较:")
    for text1, text2 in texts:
        sim = similarity(text1, text2)
        print(f"  '{text1}' vs '{text2}'")
        print(f"    相似度: {sim:.2%}\n")


def example_common_substrings():
    """公共子串查找示例"""
    print("\n" + "=" * 60)
    print("示例 7: 查找公共子串")
    print("=" * 60)
    
    text1 = "The quick brown fox jumps over the lazy dog"
    text2 = "The quick brown cat leaps over the lazy dog"
    
    # 最长公共子串
    longest = find_common_substring(text1, text2)
    print(f"\n最长公共子串: '{longest}'")
    
    # 所有公共子串
    all_common = find_common_subsequences(text1, text2, min_length=5)
    print(f"\n所有公共子串 (>=5字符):")
    for substr in all_common[:5]:  # 显示前5个
        print(f"  - '{substr}'")


def example_change_stats():
    """变更统计示例"""
    print("\n" + "=" * 60)
    print("示例 8: 变更统计")
    print("=" * 60)
    
    original = """Line one
Line two
Line three
Line four
Line five"""
    
    modified = """Line one
Line two modified
Line three
New line inserted
Line four
Line five"""
    
    # 行级统计
    stats = count_changes(original, modified, level='line')
    print("\n行级统计:")
    print(f"  新增: {stats['additions']}")
    print(f"  删除: {stats['deletions']}")
    print(f"  未变: {stats['unchanged']}")
    print(f"  总变更: {stats['total_changes']}")
    print(f"  相似度: {stats['similarity']:.2%}")
    
    # 字符级统计
    stats = count_changes(original, modified, level='char')
    print("\n字符级统计:")
    print(f"  新增: {stats['additions']}")
    print(f"  删除: {stats['deletions']}")
    print(f"  相似度: {stats['similarity']:.2%}")


def example_html_highlight():
    """HTML 高亮差异示例"""
    print("\n" + "=" * 60)
    print("示例 9: HTML 高亮差异")
    print("=" * 60)
    
    old_text = "Hello, World!"
    new_text = "Hello, Python!"
    
    html = highlight_diff_html(old_text, new_text, level='char')
    
    print(f"\n原文: {old_text}")
    print(f"新文: {new_text}")
    print(f"\nHTML 输出:")
    print(html)
    
    # 显示不同颜色
    html_custom = highlight_diff_html(
        old_text, new_text, 
        level='char',
        insert_color='#90EE90',
        delete_color='#FFB6C1'
    )
    print(f"\n自定义颜色版本:")
    print(html_custom)


def example_three_way_comparison():
    """三文本比较示例"""
    print("\n" + "=" * 60)
    print("示例 10: 三文本比较")
    print("=" * 60)
    
    original = "The quick brown fox jumps over the lazy dog"
    version_a = "The fast brown fox leaps over the lazy dog"
    version_b = "The quick brown cat jumps over the sleeping dog"
    
    result = diff_three_texts(original, version_a, version_b)
    
    print(f"\n原文: {original}")
    print(f"版本A: {version_a}")
    print(f"版本B: {version_b}")
    print("\n相似度矩阵:")
    print(f"  原文 vs 版本A: {result['text1_vs_text2']:.2%}")
    print(f"  原文 vs 版本B: {result['text1_vs_text3']:.2%}")
    print(f"  版本A vs 版本B: {result['text2_vs_text3']:.2%}")


def example_code_review():
    """代码审查差异示例"""
    print("\n" + "=" * 60)
    print("示例 11: 代码审查差异")
    print("=" * 60)
    
    old_code = """def calculate_total(items):
    total = 0
    for item in items:
        total += item.price
    return total"""

    new_code = """def calculate_total(items, discount=0):
    \"\"\"Calculate total with optional discount.\"\"\"
    total = 0
    for item in items:
        total += item.price
    if discount > 0:
        total *= (1 - discount / 100)
    return round(total, 2)"""
    
    diff = TextDiff(old_code, new_code)
    
    print("\n代码变更统计:")
    stats = diff.stats(level='line')
    print(f"  新增行: {stats.additions}")
    print(f"  删除行: {stats.deletions}")
    print(f"  未变行: {stats.unchanged}")
    print(f"  相似度: {stats.similarity:.2%}")
    
    print("\n统一格式差异:")
    print(diff.unified_diff(fromfile='original.py', tofile='modified.py'))


def example_version_control():
    """版本控制差异示例"""
    print("\n" + "=" * 60)
    print("示例 12: 版本控制差异")
    print("=" * 60)
    
    v1_0 = """# Changelog

## Version 1.0
- Initial release
- Basic functionality"""

    v1_1 = """# Changelog

## Version 1.1
- Added new feature X
- Fixed bug Y
- Improved performance

## Version 1.0
- Initial release
- Basic functionality"""

    diff = TextDiff(v1_0, v1_1)
    
    print(f"\n从 v1.0 到 v1.1 的变更:")
    print(f"  相似度: {diff.similarity():.2%}")
    print(f"  快速估计: {diff.quick_ratio():.2%}")
    
    print("\n差异详情:")
    operations = diff.get_operations()
    for op in operations:
        if op.diff_type != DiffType.EQUAL:
            print(f"  {op.diff_type.value}: 行 {op.old_start}-{op.old_end} -> 行 {op.new_start}-{op.new_end}")


if __name__ == '__main__':
    example_basic_comparison()
    example_char_level_diff()
    example_word_level_diff()
    example_unified_diff()
    example_side_by_side()
    example_similarity()
    example_common_substrings()
    example_change_stats()
    example_html_highlight()
    example_three_way_comparison()
    example_code_review()
    example_version_control()
    
    print("\n" + "=" * 60)
    print("所有示例运行完成!")
    print("=" * 60)