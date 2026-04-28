"""
Look and Say Utils - 使用示例

展示外观数列工具的各种用法。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import LookAndSayUtils, next_term, generate, nth_term, conway_constant


def example_basic_usage():
    """基本用法示例"""
    print("=" * 60)
    print("基本用法示例")
    print("=" * 60)
    
    # 生成前10项
    print("\n外观数列前10项:")
    terms = generate(10)
    for i, term in enumerate(terms):
        print(f"  T({i}): {term}")
    
    # 计算下一项
    print("\n计算下一项:")
    print(f"  next_term('1211') = '{next_term('1211')}'")
    print(f"  next_term('111221') = '{next_term('111221')}'")
    
    # 计算第n项
    print("\n计算第n项:")
    print(f"  第5项: '{nth_term(5)}'")
    print(f"  第10项: '{nth_term(10)}'")


def example_different_seeds():
    """不同种子示例"""
    print("\n" + "=" * 60)
    print("不同种子的行为")
    print("=" * 60)
    
    seeds = ["1", "22", "3", "111111", "123", "111222333"]
    
    for seed in seeds:
        print(f"\n种子 '{seed}':")
        terms = LookAndSayUtils.generate(6, seed)
        for i, term in enumerate(terms):
            print(f"  T({i}): {term}")


def example_length_analysis():
    """长度分析示例"""
    print("\n" + "=" * 60)
    print("长度增长分析")
    print("=" * 60)
    
    # 分析前15项的长度增长
    print("\n前15项的长度和增长比:")
    growth = LookAndSayUtils.analyze_growth(15)
    print(f"{'项':>4} {'长度':>8} {'增长比':>10}")
    print("-" * 25)
    for idx, length, ratio in growth:
        print(f"{idx:>4} {length:>8} {ratio:>10.4f}")
    
    # 康威常数
    print(f"\n康威常数: {conway_constant():.15f}...")
    approx = LookAndSayUtils.conway_constant_approximation(25)
    print(f"使用25项近似: {approx:.15f}")


def example_digit_distribution():
    """数字分布分析"""
    print("\n" + "=" * 60)
    print("数字分布分析")
    print("=" * 60)
    
    # 分析不同阶段的数字分布
    stages = [10, 15, 20, 25]
    
    for n in stages:
        print(f"\n第{n}项的数字分布:")
        dist = LookAndSayUtils.digit_distribution(n)
        for digit, ratio in sorted(dist.items()):
            bar = "█" * int(ratio * 40)
            print(f"  '{digit}': {ratio:.2%} {bar}")
        
        term = nth_term(n)
        freq = LookAndSayUtils.digit_frequency(term)
        print(f"  原始计数: {freq}")


def example_run_length_encoding():
    """游程编码示例"""
    print("\n" + "=" * 60)
    print("游程编码（核心操作）")
    print("=" * 60)
    
    test_strings = ["111221", "312211", "1211", "111111111"]
    
    for s in test_strings:
        encoded = LookAndSayUtils.run_length_encoding(s)
        decoded = LookAndSayUtils.from_run_length(encoded)
        
        print(f"\n原始字符串: '{s}'")
        print(f"游程编码: {encoded}")
        print(f"解码还原: '{decoded}'")
        print(f"一致: {s == decoded}")


def example_validation():
    """有效性验证"""
    print("\n" + "=" * 60)
    print("有效性验证")
    print("=" * 60)
    
    test_cases = [
        ("1", True),
        ("11", True),
        ("21", True),
        ("1211", True),
        ("1111", False),  # 4个连续相同数字
        ("abc", False),    # 非数字
        ("", False),       # 空字符串
        ("123", True),
    ]
    
    print("\n验证各字符串是否可能是外观数列项:")
    for s, expected in test_cases:
        result = LookAndSayUtils.is_valid_look_and_say_term(s)
        status = "✓" if result == expected else "✗"
        print(f"  '{s}': {result} (预期: {expected}) {status}")


def example_reverse_step():
    """反向推导"""
    print("\n" + "=" * 60)
    print("反向推导（找到上一项）")
    print("=" * 60)
    
    test_cases = ["11", "21", "1211", "111221", "312211"]
    
    for term in test_cases:
        prev = LookAndSayUtils.reverse_step(term)
        print(f"\n当前项: '{term}'")
        print(f"可能的上一项: {prev}")
        if prev:
            # 验证
            next_from_prev = next_term(prev[0])
            print(f"验证: '{prev[0]}' → '{next_from_prev}' {'✓' if next_from_prev == term else '✗'}")


def example_length_estimation():
    """长度估算"""
    print("\n" + "=" * 60)
    print("长度估算（康威常数应用）")
    print("=" * 60)
    
    print("\n比较估算长度与实际长度:")
    print(f"{'n':>4} {'估算':>10} {'实际':>10} {'误差':>10}")
    print("-" * 40)
    
    for n in range(5, 26, 5):
        estimated = LookAndSayUtils.estimate_nth_length(n)
        actual = len(nth_term(n))
        error = abs(estimated - actual) / actual * 100
        print(f"{n:>4} {estimated:>10} {actual:>10} {error:>9.1f}%")


def example_iterator():
    """迭代器示例"""
    print("\n" + "=" * 60)
    print("使用迭代器")
    print("=" * 60)
    
    print("\n使用迭代器生成前8项:")
    it = LookAndSayUtils.iterator()
    for i in range(8):
        term = next(it)
        print(f"  T({i}): {term}")


def example_cosmological_decay():
    """宇宙学衰减示例"""
    print("\n" + "=" * 60)
    print("康威宇宙学定理演示")
    print("=" * 60)
    
    print("\n追踪特定模式在前20项中的出现:")
    decay = LookAndSayUtils.cosmological_decay(20)
    
    for pattern, occurrences in sorted(decay.items()):
        if occurrences:
            print(f"  模式 '{pattern}': 出现在项 {occurrences}")


def example_max_run():
    """最大连续长度"""
    print("\n" + "=" * 60)
    print("最大连续相同数字长度")
    print("=" * 60)
    
    print("\n前15项的最大连续长度:")
    terms = generate(15)
    for i, term in enumerate(terms):
        max_run = LookAndSayUtils.max_run_length(term)
        print(f"  T({i}): max_run={max_run}, term='{term[:30]}{'...' if len(term) > 30 else ''}'")


def example_unique_digits():
    """唯一数字计数"""
    print("\n" + "=" * 60)
    print("唯一数字数量追踪")
    print("=" * 60)
    
    counts = LookAndSayUtils.count_unique_digits(15)
    terms = generate(15)
    
    print("\n每项包含的不同数字数量:")
    for i, (count, term) in enumerate(zip(counts, terms)):
        unique = sorted(set(term))
        print(f"  T({i}): {count} 种数字 {unique}")


def main():
    """运行所有示例"""
    example_basic_usage()
    example_different_seeds()
    example_length_analysis()
    example_digit_distribution()
    example_run_length_encoding()
    example_validation()
    example_reverse_step()
    example_length_estimation()
    example_iterator()
    example_cosmological_decay()
    example_max_run()
    example_unique_digits()
    
    print("\n" + "=" * 60)
    print("示例完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()