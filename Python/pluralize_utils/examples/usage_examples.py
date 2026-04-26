"""
pluralize_utils 使用示例

演示英文单词单复数转换的各种用法。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from pluralize_utils.mod import (
    singular_to_plural,
    plural_to_singular,
    is_plural,
    get_plural_form,
    batch_pluralize,
    batch_singularize,
    get_article,
    format_count,
)


def print_section(title: str):
    """打印章节标题"""
    print(f"\n{'=' * 50}")
    print(f"  {title}")
    print('=' * 50)


def example_basic_conversion():
    """基本转换示例"""
    print_section("基本转换")
    
    # 单数转复数
    words = ['cat', 'dog', 'box', 'city', 'knife', 'child', 'man', 'person']
    print("\n单数 → 复数:")
    for word in words:
        plural = singular_to_plural(word)
        print(f"  {word:15} → {plural}")
    
    # 复数转单数
    plurals = ['cats', 'dogs', 'boxes', 'cities', 'knives', 'children', 'men', 'people']
    print("\n复数 → 单数:")
    for word in plurals:
        singular = plural_to_singular(word)
        print(f"  {word:15} → {singular}")


def example_irregular_nouns():
    """不规则变化名词示例"""
    print_section("不规则变化名词")
    
    irregular_words = [
        ('man', 'men'),
        ('woman', 'women'),
        ('child', 'children'),
        ('person', 'people'),
        ('foot', 'feet'),
        ('tooth', 'teeth'),
        ('goose', 'geese'),
        ('mouse', 'mice'),
        ('ox', 'oxen'),
        ('sheep', 'sheep'),  # 单复数同形
        ('deer', 'deer'),    # 单复数同形
    ]
    
    print("\n不规则变化:")
    for singular, expected_plural in irregular_words:
        result = singular_to_plural(singular)
        status = "✓" if result == expected_plural else "✗"
        print(f"  {status} {singular:15} → {result:15} (期望: {expected_plural})")


def example_latin_greek():
    """拉丁/希腊源词示例"""
    print_section("拉丁/希腊源词")
    
    latin_words = [
        ('analysis', 'analyses'),
        ('basis', 'bases'),
        ('crisis', 'crises'),
        ('phenomenon', 'phenomena'),
        ('criterion', 'criteria'),
        ('datum', 'data'),
        ('medium', 'media'),
        ('curriculum', 'curricula'),
        ('focus', 'foci'),
        ('fungus', 'fungi'),
        ('nucleus', 'nuclei'),
        ('stimulus', 'stimuli'),
        ('index', 'indices'),
        ('matrix', 'matrices'),
        ('appendix', 'appendices'),
    ]
    
    print("\n拉丁/希腊源词复数:")
    for singular, expected_plural in latin_words:
        result = singular_to_plural(singular)
        status = "✓" if result == expected_plural else "✗"
        print(f"  {status} {singular:15} → {result:15} (期望: {expected_plural})")


def example_is_plural():
    """判断复数示例"""
    print_section("判断是否为复数")
    
    test_words = [
        'cat', 'cats',
        'box', 'boxes',
        'city', 'cities',
        'man', 'men',
        'child', 'children',
        'sheep', 'fish',
        'news', 'politics',
        'data', 'media',
    ]
    
    print("\n判断复数:")
    for word in test_words:
        result = is_plural(word)
        print(f"  {word:15} → {'是复数' if result else '单数'}")


def example_with_count():
    """根据数量转换示例"""
    print_section("根据数量转换")
    
    word = 'cat'
    counts = [0, 1, 2, 5, 10, 100]
    
    print(f"\n单词: {word}")
    for count in counts:
        form = get_plural_form(word, count)
        print(f"  {count:3} → {form}")
    
    print(f"\n单词: box")
    for count in counts:
        form = get_plural_form('box', count)
        print(f"  {count:3} → {form}")


def example_batch_operations():
    """批量操作示例"""
    print_section("批量操作")
    
    words = ['cat', 'dog', 'box', 'city', 'knife', 'child', 'man', 'woman']
    
    # 批量转复数
    plurals = batch_pluralize(words)
    print("\n批量转复数:")
    print(f"  输入: {words}")
    print(f"  输出: {plurals}")
    
    # 批量转单数
    singulars = batch_singularize(plurals)
    print("\n批量转单数:")
    print(f"  输入: {plurals}")
    print(f"  输出: {singulars}")


def example_format_count():
    """格式化数量示例"""
    print_section("格式化数量")
    
    examples = [
        ('cat', 1),
        ('cat', 2),
        ('apple', 1),
        ('apple', 3),
        ('box', 5),
        ('child', 10),
        ('person', 100),
    ]
    
    print("\n格式化结果:")
    for word, count in examples:
        result = format_count(word, count)
        print(f"  {word:10} × {count:3} → {result}")


def example_case_preservation():
    """大小写保持示例"""
    print_section("大小写保持")
    
    words = ['Cat', 'CAT', 'Dog', 'DOG', 'Child', 'CHILD']
    
    print("\n转换时保持大小写:")
    for word in words:
        plural = singular_to_plural(word)
        singular = plural_to_singular(plural)
        print(f"  {word:10} → {plural:12} → {singular:10}")


def example_sentence_building():
    """构建句子示例"""
    print_section("实际应用：构建句子")
    
    # 构建描述数量的句子
    items = [
        ('apple', 5),
        ('orange', 1),
        ('banana', 12),
        ('child', 3),
        ('man', 2),
        ('woman', 4),
        ('box', 1),
        ('knife', 6),
    ]
    
    print("\n构建句子:")
    for word, count in items:
        formatted = format_count(word, count)
        print(f"  I have {formatted}.")
    
    # 智能判断
    print("\n智能判断并转换:")
    sentences = [
        "I have 1 cat.",
        "I have 2 dog.",
        "She has 5 box.",
        "They have 10 child.",
    ]
    
    for sentence in sentences:
        # 提取数量和单词
        import re
        match = re.match(r'(.*?)(\d+)\s+(\w+)(\..*)', sentence)
        if match:
            prefix, count, word, suffix = match.groups()
            count = int(count)
            formatted = format_count(word, count)
            new_sentence = f"{prefix}{formatted}{suffix}"
            print(f"  {sentence:25} → {new_sentence}")


def example_comprehensive():
    """综合示例"""
    print_section("综合示例")
    
    print("\n1. 常用单词转换:")
    common_words = ['book', 'pen', 'car', 'house', 'tree', 'computer', 'phone', 'table']
    for word in common_words:
        plural = singular_to_plural(word)
        print(f"   {word:12} → {plural}")
    
    print("\n2. 特殊结尾单词:")
    special_words = [
        ('bus', 'buses'),
        ('quiz', 'quizzes'),
        ('church', 'churches'),
        ('brush', 'brushes'),
        ('baby', 'babies'),
        ('toy', 'toys'),
        ('potato', 'potatoes'),
        ('photo', 'photos'),
    ]
    for singular, expected in special_words:
        result = singular_to_plural(singular)
        status = "✓" if result == expected else "✗"
        print(f"   {status} {singular:12} → {result:12}")
    
    print("\n3. 不可数名词:")
    uncountable = ['sheep', 'deer', 'fish', 'information', 'news', 'water']
    for word in uncountable:
        plural = singular_to_plural(word)
        print(f"   {word:15} → {plural} (保持不变)")


def main():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("  pluralize_utils - 英文单词单复数转换工具")
    print("=" * 60)
    
    example_basic_conversion()
    example_irregular_nouns()
    example_latin_greek()
    example_is_plural()
    example_with_count()
    example_batch_operations()
    example_format_count()
    example_case_preservation()
    example_sentence_building()
    example_comprehensive()
    
    print("\n" + "=" * 60)
    print("  示例完成！")
    print("=" * 60 + "\n")


if __name__ == '__main__':
    main()