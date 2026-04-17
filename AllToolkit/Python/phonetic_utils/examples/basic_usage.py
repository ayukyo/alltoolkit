"""
Phonetic Utils 示例 - 基本用法

展示如何使用语音编码工具进行姓名匹配。

Author: AllToolkit
License: MIT
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from phonetic_utils.mod import (
    soundex, metaphone, double_metaphone, nysiis,
    caverphone, match_rating, lein,
    phonetic_similarity, match_names, get_all_encodings,
    batch_encode, group_by_phonetic, find_duplicates,
    PhoneticEncoder
)


def demo_basic_encoding():
    """基本编码演示"""
    print("\n=== 基本编码演示 ===")
    
    name = "Smith"
    
    print(f"\n姓名: {name}")
    print(f"  Soundex:      {soundex(name)}")
    print(f"  Metaphone:    {metaphone(name)}")
    print(f"  NYSIIS:       {nysiis(name)}")
    print(f"  Caverphone:   {caverphone(name)}")
    print(f"  Match Rating: {match_rating(name)}")
    print(f"  Lein:         {lein(name)}")
    
    # Double Metaphone 返回两个编码
    primary, alternate = double_metaphone(name)
    print(f"  Double Metaphone: {primary} / {alternate}")


def demo_all_encodings():
    """所有编码对比"""
    print("\n=== 所有编码对比 ===")
    
    names = ["Smith", "Schmidt", "Smyth", "Johnson", "Williams", "Brown"]
    
    print(f"\n{'姓名':<12} {'Soundex':<8} {'Metaphone':<8} {'NYSIIS':<8}")
    print("-" * 40)
    
    for name in names:
        print(f"{name:<12} {soundex(name):<8} {metaphone(name):<8} {nysiis(name):<8}")


def demo_similarity():
    """相似度计算演示"""
    print("\n=== 相似度计算演示 ===")
    
    pairs = [
        ("Smith", "Schmidt"),
        ("Smith", "Smyth"),
        ("Johnson", "Johnston"),
        ("Williams", "Wilson"),
        ("Brown", "Braun"),
        ("John", "Jane"),
    ]
    
    print(f"\n{'姓名1':<10} {'姓名2':<10} {'Soundex':<8} {'Metaphone':<10}")
    print("-" * 40)
    
    for name1, name2 in pairs:
        sim1 = phonetic_similarity(name1, name2, 'soundex')
        sim2 = phonetic_similarity(name1, name2, 'metaphone')
        print(f"{name1:<10} {name2:<10} {sim1:.2f}     {sim2:.2f}")


def demo_name_matching():
    """姓名匹配演示"""
    print("\n=== 姓名匹配演示 ===")
    
    target = "Smith"
    candidates = [
        "Smith", "Schmidt", "Smyth", "Smithson",
        "Johnson", "Williams", "Brown", "Jones"
    ]
    
    print(f"\n目标姓名: {target}")
    print(f"候选列表: {', '.join(candidates)}")
    
    # 使用 Soundex 匹配
    matches = match_names(target, candidates, 'soundex', threshold=0.8)
    
    print(f"\n匹配结果 (Soundex, threshold=0.8):")
    for name, score in matches:
        print(f"  {name}: {score:.2f}")
    
    # 使用 Metaphone 匹配
    matches2 = match_names(target, candidates, 'metaphone', threshold=0.5)
    
    print(f"\n匹配结果 (Metaphone, threshold=0.5):")
    for name, score in matches2:
        print(f"  {name}: {score:.2f}")


def demo_duplicate_detection():
    """重复检测演示"""
    print("\n=== 重复检测演示 ===")
    
    names = [
        "Smith", "Schmidt", "Smyth",
        "Johnson", "Johnston", "Johns",
        "Williams", "Wilson",
        "Brown", "Braun",
        "Taylor"
    ]
    
    print(f"\n输入姓名: {', '.join(names)}")
    
    # 查找可能的重复
    duplicates = find_duplicates(names, 'soundex', threshold=0.8)
    
    print(f"\n可能的重复组:")
    for group in duplicates:
        print(f"  {group}")


def demo_grouping():
    """分组演示"""
    print("\n=== 分组演示 ===")
    
    names = [
        "Smith", "Schmidt", "Johnson", "Johnston",
        "Williams", "Brown", "Braun"
    ]
    
    print(f"\n输入姓名: {', '.join(names)}")
    
    # 按 Soundex 分组
    groups = group_by_phonetic(names, 'soundex')
    
    print(f"\nSoundex 分组结果:")
    for code, group_names in groups.items():
        print(f"  {code}: {group_names}")


def demo_batch_encoding():
    """批量编码演示"""
    print("\n=== 批量编码演示 ===")
    
    names = ["Smith", "Johnson", "Williams", "Brown", "Jones"]
    
    print(f"\n输入姓名: {', '.join(names)}")
    
    # 批量 Soundex 编码
    codes = batch_encode(names, 'soundex')
    
    print(f"\n批量 Soundex 编码:")
    for name, code in codes.items():
        print(f"  {name}: {code}")


def demo_encoder_class():
    """编码器类演示"""
    print("\n=== PhoneticEncoder 类演示 ===")
    
    # 创建编码器
    encoder = PhoneticEncoder('soundex', 4)
    
    print(f"\n编码器配置: {encoder}")
    
    # 编码单个姓名
    name = "Smith"
    code = encoder.encode(name)
    print(f"\n编码 '{name}': {code}")
    
    # 批量编码
    names = ["Smith", "Johnson", "Williams"]
    codes = encoder.batch_encode(names)
    print(f"\n批量编码: {codes}")
    
    # 相似度计算
    sim = encoder.similarity("Smith", "Schmidt")
    print(f"\n相似度 (Smith vs Schmidt): {sim:.2f}")
    
    # 匹配
    matches = encoder.match("Smith", ["Schmidt", "Johnson", "Smyth"])
    print(f"\n匹配结果:")
    for name, score in matches:
        print(f"  {name}: {score:.2f}")


def demo_real_world():
    """实际应用场景演示"""
    print("\n=== 实际应用场景 ===")
    
    # 场景1: 数据去重
    print("\n场景1: 数据去重")
    customer_names = [
        "John Smith", "J. Smith", "Smith, John",
        "Jane Johnson", "J. Johnson", "Johnson, Jane",
        "Robert Williams"
    ]
    
    # 提取姓氏
    surnames = [name.split()[-1] for name in customer_names]
    
    duplicates = find_duplicates(surnames, 'soundex', threshold=0.8)
    print(f"  可能重复的姓氏:")
    for group in duplicates:
        print(f"    {group}")
    
    # 场景2: 搜索优化
    print("\n场景2: 搜索优化")
    search_query = "Smth"  # 用户输入可能有拼写错误
    database_names = ["Smith", "Johnson", "Williams", "Brown", "Smyth"]
    
    matches = match_names(search_query, database_names, 'metaphone', threshold=0.5)
    print(f"  搜索 '{search_query}' 的结果:")
    for name, score in matches:
        print(f"    {name}: {score:.2f}")
    
    # 场景3: 族谱研究
    print("\n场景3: 族谱研究")
    historical_names = ["Müller", "Mueller", "Miller"]
    all_codes = get_all_encodings("Müller")
    print(f"  'Müller' 的所有编码:")
    for algo, code in all_codes.items():
        print(f"    {algo}: {code}")


def main():
    """运行所有演示"""
    print("\n" + "=" * 60)
    print("Phonetic Utils 示例")
    print("=" * 60)
    
    demo_basic_encoding()
    demo_all_encodings()
    demo_similarity()
    demo_name_matching()
    demo_duplicate_detection()
    demo_grouping()
    demo_batch_encoding()
    demo_encoder_class()
    demo_real_world()
    
    print("\n" + "=" * 60)
    print("演示完成!")
    print("=" * 60 + "\n")


if __name__ == '__main__':
    main()