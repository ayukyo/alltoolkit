#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Shell Sort Utils 使用示例

演示希尔排序工具库的各种功能。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shell_sort_utils.mod import (
    shell_sort,
    shell_sort_with_trace,
    shell_sort_optimized,
    shell_sort_pair,
    is_sorted,
    benchmark_gaps,
    shellsort,
    GapSequence,
    generate_ciura_gaps,
    get_gap_sequence,
)


def example_01_basic_sort():
    """示例1: 基本排序"""
    print("=" * 50)
    print("示例1: 基本排序")
    print("=" * 50)
    
    # 基本升序排序
    numbers = [64, 34, 25, 12, 22, 11, 90]
    result = shell_sort(numbers)
    
    print(f"输入: {numbers}")
    print(f"输出: {result.data}")
    print(f"比较次数: {result.comparisons}")
    print(f"交换次数: {result.swaps}")
    print(f"使用的间隔序列: {result.gap_sequence}")
    
    # 降序排序
    result_desc = shell_sort(numbers, reverse=True)
    print(f"\n降序排序: {result_desc.data}")
    
    # 使用简写函数
    quick_sort = shellsort(numbers)
    print(f"快捷排序: {quick_sort}")


def example_02_key_function():
    """示例2: 使用键函数"""
    print("\n" + "=" * 50)
    print("示例2: 使用键函数")
    print("=" * 50)
    
    # 按字符串长度排序
    words = ["apple", "kiwi", "banana", "cherry", "fig", "watermelon"]
    result = shell_sort(words, key=len)
    print(f"单词: {words}")
    print(f"按长度排序: {result.data}")
    
    # 按绝对值排序
    numbers = [-5, 3, -1, 4, -2, 8, -7]
    result = shell_sort(numbers, key=abs)
    print(f"\n数字: {numbers}")
    print(f"按绝对值排序: {result.data}")
    
    # 排序对象列表
    class Student:
        def __init__(self, name, score):
            self.name = name
            self.score = score
        def __repr__(self):
            return f"{self.name}({self.score})"
    
    students = [
        Student("Alice", 85),
        Student("Bob", 92),
        Student("Charlie", 78),
        Student("Diana", 95),
        Student("Eve", 88)
    ]
    
    result = shell_sort(students, key=lambda s: s.score, reverse=True)
    print(f"\n按成绩降序: {result.data}")


def example_03_gap_sequences():
    """示例3: 不同间隔序列"""
    print("\n" + "=" * 50)
    print("示例3: 不同间隔序列")
    print("=" * 50)
    
    import random
    data = [random.randint(1, 100) for _ in range(50)]
    
    print(f"测试数据 (50个随机数)")
    
    # 比较不同间隔序列的性能
    results = benchmark_gaps(data)
    
    print(f"\n{'序列':<12} {'比较':>10} {'交换':>10} {'轮数':>8}")
    print("-" * 42)
    
    for seq, stats in sorted(results.items(), key=lambda x: x[1]['comparisons']):
        print(f"{seq:<12} {stats['comparisons']:>10} {stats['swaps']:>10} {stats['passes']:>8}")
    
    # 推荐使用 Ciura 序列
    print("\n💡 推荐: Ciura 序列在实践中表现最好")


def example_04_trace_visualization():
    """示例4: 排序过程可视化"""
    print("\n" + "=" * 50)
    print("示例4: 排序过程可视化")
    print("=" * 50)
    
    data = [5, 3, 1, 4, 2]
    print(f"排序 {data}")
    
    print("\n排序步骤:")
    step = 0
    for state, gap, idx in shell_sort_with_trace(data):
        step += 1
        if step <= 15:  # 显示前15步
            print(f"  步骤{step:2d}: gap={gap}, i={idx} -> {state}")
    
    print(f"\n总共 {step} 步完成排序")


def example_05_pair_sort():
    """示例5: 联合排序"""
    print("\n" + "=" * 50)
    print("示例5: 联合排序")
    print("=" * 50)
    
    # 学生成绩单
    names = ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve']
    scores = [85, 92, 78, 95, 88]
    
    print(f"姓名: {names}")
    print(f"成绩: {scores}")
    
    sorted_scores, sorted_names = shell_sort_pair(scores, names, reverse=True)
    
    print("\n按成绩降序排列:")
    for name, score in zip(sorted_names, sorted_scores):
        print(f"  {name}: {score}")


def example_06_optimized_sort():
    """示例6: 自动优化排序"""
    print("\n" + "=" * 50)
    print("示例6: 自动优化排序")
    print("=" * 50)
    
    import random
    
    # 不同规模的数据
    sizes = [30, 200, 800]
    
    for size in sizes:
        data = [random.randint(1, 1000) for _ in range(size)]
        
        result = shell_sort_optimized(data)
        print(f"\n数据量 n={size}:")
        print(f"  使用的间隔序列长度: {len(result.gap_sequence)}")
        print(f"  比较次数: {result.comparisons}")
        print(f"  交换次数: {result.swaps}")


def example_07_check_sorted():
    """示例7: 检查是否已排序"""
    print("\n" + "=" * 50)
    print("示例7: 检查是否已排序")
    print("=" * 50)
    
    # 已排序数据
    sorted_data = [1, 2, 3, 4, 5]
    print(f"{sorted_data} 是否已排序: {is_sorted(sorted_data)}")
    
    # 未排序数据
    unsorted_data = [3, 1, 4, 2]
    print(f"{unsorted_data} 是否已排序: {is_sorted(unsorted_data)}")
    
    # 降序检查
    desc_data = [5, 4, 3, 2, 1]
    print(f"{desc_data} 是否降序排序: {is_sorted(desc_data, reverse=True)}")
    
    # 带键函数检查
    abs_sorted = [-1, 2, -3, 4, 5]
    print(f"{abs_sorted} 是否按绝对值排序: {is_sorted(abs_sorted, key=abs)}")


def example_08_custom_gap_sequence():
    """示例8: 自定义间隔序列"""
    print("\n" + "=" * 50)
    print("示例8: 自定义间隔序列")
    print("=" * 50)
    
    # 查看 Ciura 序列的生成
    gaps = generate_ciura_gaps(100)
    print(f"n=100 的 Ciura 间隔序列: {gaps}")
    
    # 查看不同 n 值的序列
    for n in [10, 50, 200]:
        gaps = get_gap_sequence(n, GapSequence.CIURA)
        print(f"n={n}: {gaps}")
    
    # 比较序列生成方法
    print("\n各序列类型:")
    for seq_type in GapSequence:
        gaps = get_gap_sequence(50, seq_type)
        print(f"  {seq_type.value}: {gaps}")


def example_09_real_world_scenario():
    """示例9: 实际应用场景"""
    print("\n" + "=" * 50)
    print("示例9: 实际应用场景 - 排序商品价格")
    print("=" * 50)
    
    # 商品数据
    products = [
        ("Apple", 5.99),
        ("Banana", 3.49),
        ("Orange", 4.99),
        ("Milk", 2.99),
        ("Bread", 4.50),
        ("Cheese", 8.99),
        ("Eggs", 6.49)
    ]
    
    prices = [p[1] for p in products]
    names = [p[0] for p in products]
    
    # 按价格排序
    sorted_prices, sorted_names = shell_sort_pair(prices, names)
    
    print("商品价格从低到高:")
    for name, price in zip(sorted_names, sorted_prices):
        print(f"  {name}: ${price:.2f}")
    
    # 查找价格区间
    print("\n价格区间筛选:")
    print("低价商品 (<$4):")
    for name, price in zip(sorted_names, sorted_prices):
        if price < 4:
            print(f"  {name}: ${price:.2f}")


def run_all_examples():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("Shell Sort Utils 使用示例集")
    print("=" * 60)
    
    example_01_basic_sort()
    example_02_key_function()
    example_03_gap_sequences()
    example_04_trace_visualization()
    example_05_pair_sort()
    example_06_optimized_sort()
    example_07_check_sorted()
    example_08_custom_gap_sequence()
    example_09_real_world_scenario()
    
    print("\n" + "=" * 60)
    print("示例演示完成!")
    print("=" * 60)


if __name__ == "__main__":
    run_all_examples()