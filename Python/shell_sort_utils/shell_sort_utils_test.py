#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Shell Sort Utils 测试文件

测试希尔排序工具库的各个功能。
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
    generate_shell_gaps,
    generate_knuth_gaps,
    generate_hibbard_gaps,
    generate_sedgewick_gaps,
    generate_ciura_gaps,
    generate_tokuda_gaps,
    generate_pratt_gaps,
    get_gap_sequence,
    SortResult,
)


def test_gap_sequences():
    """测试间隔序列生成"""
    print("=" * 50)
    print("测试间隔序列生成")
    print("=" * 50)
    
    n = 100
    
    print(f"\n数据长度 n = {n}")
    
    shell_gaps = generate_shell_gaps(n)
    print(f"Shell 序列: {shell_gaps}")
    
    knuth_gaps = generate_knuth_gaps(n)
    print(f"Knuth 序列: {knuth_gaps}")
    
    hibbard_gaps = generate_hibbard_gaps(n)
    print(f"Hibbard 序列: {hibbard_gaps}")
    
    sedgewick_gaps = generate_sedgewick_gaps(n)
    print(f"Sedgewick 序列: {sedgewick_gaps}")
    
    ciura_gaps = generate_ciura_gaps(n)
    print(f"Ciura 序列: {ciura_gaps}")
    
    tokuda_gaps = generate_tokuda_gaps(n)
    print(f"Tokuda 序列: {tokuda_gaps}")
    
    pratt_gaps = generate_pratt_gaps(n)
    print(f"Pratt 序列: {pratt_gaps[:10]}... (共 {len(pratt_gaps)} 个)")
    
    # 测试 get_gap_sequence
    print("\n通过 get_gap_sequence 获取:")
    for seq in GapSequence:
        gaps = get_gap_sequence(n, seq)
        print(f"  {seq.value}: {gaps[:5]}{'...' if len(gaps) > 5 else ''}")
    
    print("\n✓ 间隔序列生成测试通过")


def test_basic_shell_sort():
    """测试基本希尔排序"""
    print("\n" + "=" * 50)
    print("测试基本希尔排序")
    print("=" * 50)
    
    # 测试数据
    test_cases = [
        [64, 34, 25, 12, 22, 11, 90],
        [5, 2, 9, 1, 5, 6],
        [1, 2, 3, 4, 5],  # 已排序
        [5, 4, 3, 2, 1],  # 反向排序
        [42],             # 单元素
        [],               # 空列表
        [3, 3, 3, 3, 3],  # 全相同
    ]
    
    for data in test_cases:
        result = shell_sort(data)
        print(f"\n输入: {data}")
        print(f"输出: {result.data}")
        print(f"比较次数: {result.comparisons}, 交换次数: {result.swaps}")
        print(f"扫描轮数: {result.passes}")
        
        # 验证排序正确
        expected = sorted(data)
        assert result.data == expected, f"排序结果不正确: {result.data} != {expected}"
    
    print("\n✓ 基本希尔排序测试通过")


def test_reverse_sort():
    """测试降序排序"""
    print("\n" + "=" * 50)
    print("测试降序排序")
    print("=" * 50)
    
    data = [64, 34, 25, 12, 22, 11, 90]
    result = shell_sort(data, reverse=True)
    
    print(f"输入: {data}")
    print(f"降序输出: {result.data}")
    
    expected = sorted(data, reverse=True)
    assert result.data == expected, f"降序排序不正确"
    
    print("\n✓ 降序排序测试通过")


def test_key_function():
    """测试键函数"""
    print("\n" + "=" * 50)
    print("测试键函数")
    print("=" * 50)
    
    # 按绝对值排序
    data = [-5, 3, -1, 4, -2]
    result = shell_sort(data, key=abs)
    print(f"按绝对值排序: {data} -> {result.data}")
    assert result.data == [-1, -2, 3, 4, -5]
    
    # 按字符串长度排序
    words = ["apple", "kiwi", "banana", "cherry", "fig"]
    result = shell_sort(words, key=len)
    print(f"按长度排序: {words} -> {result.data}")
    assert result.data == ["fig", "kiwi", "apple", "banana", "cherry"]
    
    # 按对象属性排序
    class Person:
        def __init__(self, name, age):
            self.name = name
            self.age = age
        def __repr__(self):
            return f"{self.name}({self.age})"
    
    people = [Person("Alice", 30), Person("Bob", 25), Person("Charlie", 35)]
    result = shell_sort(people, key=lambda p: p.age)
    print(f"按年龄排序: {result.data}")
    
    print("\n✓ 键函数测试通过")


def test_inplace_sort():
    """测试原地排序"""
    print("\n" + "=" * 50)
    print("测试原地排序")
    print("=" * 50)
    
    data = [5, 3, 1, 4, 2]
    original_data = data.copy()
    
    # 非原地排序（默认）
    result1 = shell_sort(data)
    print(f"非原地排序: 原数据 {data} 不变, 结果 {result1.data}")
    assert data == original_data
    
    # 原地排序
    result2 = shell_sort(data, inplace=True)
    print(f"原地排序: 原数据 {data} 已改变")
    assert data == result2.data
    assert data == [1, 2, 3, 4, 5]
    
    print("\n✓ 原地排序测试通过")


def test_gap_sequence_comparison():
    """测试不同间隔序列的比较"""
    print("\n" + "=" * 50)
    print("测试不同间隔序列性能比较")
    print("=" * 50)
    
    # 随机生成测试数据
    import random
    data = [random.randint(1, 1000) for _ in range(100)]
    
    print(f"数据长度: {len(data)}")
    
    results = {}
    for seq in GapSequence:
        result = shell_sort(data.copy(), seq)
        results[seq.value] = {
            'comparisons': result.comparisons,
            'swaps': result.swaps,
            'passes': result.passes
        }
        
        # 验证排序正确
        assert result.data == sorted(data), f"{seq.value} 序列排序不正确"
    
    print("\n性能统计:")
    print(f"{'序列':<12} {'比较':>10} {'交换':>10} {'轮数':>8}")
    print("-" * 40)
    for seq, stats in results.items():
        print(f"{seq:<12} {stats['comparisons']:>10} {stats['swaps']:>10} {stats['passes']:>8}")
    
    print("\n✓ 间隔序列比较测试通过")


def test_shell_sort_with_trace():
    """测试带跟踪的希尔排序"""
    print("\n" + "=" * 50)
    print("测试带跟踪的希尔排序")
    print("=" * 50)
    
    data = [5, 3, 1, 4, 2]
    print(f"初始数据: {data}")
    
    step_count = 0
    for state, gap, idx in shell_sort_with_trace(data):
        step_count += 1
        if step_count <= 10:  # 只显示前10步
            print(f"步骤 {step_count}: gap={gap}, i={idx}, state={state}")
    
    print(f"总步骤数: {step_count}")
    
    # 验证最终结果正确
    final_state = list(shell_sort_with_trace(data))[-1][0]
    assert final_state == sorted(data)
    
    print("\n✓ 带跟踪排序测试通过")


def test_shell_sort_optimized():
    """测试优化的希尔排序"""
    print("\n" + "=" * 50)
    print("测试优化的希尔排序")
    print("=" * 50)
    
    import random
    
    # 小数据量
    small_data = [random.randint(1, 50) for _ in range(30)]
    result = shell_sort_optimized(small_data)
    print(f"小数据量 (n=30): {len(result.gap_sequence)} 个间隔")
    assert result.data == sorted(small_data)
    
    # 中等数据量
    medium_data = [random.randint(1, 500) for _ in range(500)]
    result = shell_sort_optimized(medium_data)
    print(f"中等数据量 (n=500): {len(result.gap_sequence)} 个间隔")
    assert result.data == sorted(medium_data)
    
    # 已部分有序数据
    partially_sorted = list(range(100))
    # 添加少量逆序
    for _ in range(5):
        i, j = random.randint(0, 99), random.randint(0, 99)
        partially_sorted[i], partially_sorted[j] = partially_sorted[j], partially_sorted[i]
    
    result = shell_sort_optimized(partially_sorted)
    print(f"部分有序数据: 排序完成")
    assert result.data == sorted(partially_sorted)
    
    print("\n✓ 优化排序测试通过")


def test_shell_sort_pair():
    """测试联合排序"""
    print("\n" + "=" * 50)
    print("测试联合排序")
    print("=" * 50)
    
    names = ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve']
    scores = [85, 92, 78, 88, 95]
    
    print(f"姓名: {names}")
    print(f"分数: {scores}")
    
    sorted_scores, sorted_names = shell_sort_pair(scores, names)
    print(f"按分数排序后:")
    print(f"  分数: {sorted_scores}")
    print(f"  姓名: {sorted_names}")
    
    # 验证对应关系保持
    for i in range(len(names)):
        idx = names.index(sorted_names[i])
        assert scores[idx] == sorted_scores[i]
    
    # 降序排序
    sorted_scores_desc, sorted_names_desc = shell_sort_pair(scores, names, reverse=True)
    print(f"\n降序排序:")
    print(f"  分数: {sorted_scores_desc}")
    print(f"  姓名: {sorted_names_desc}")
    
    assert sorted_scores_desc == sorted(scores, reverse=True)
    
    print("\n✓ 联合排序测试通过")


def test_is_sorted():
    """测试排序检查函数"""
    print("\n" + "=" * 50)
    print("测试排序检查函数")
    print("=" * 50)
    
    # 已排序
    assert is_sorted([1, 2, 3, 4, 5]) == True
    assert is_sorted([1, 1, 2, 2, 3]) == True
    print("已升序排序: ✓")
    
    # 未排序
    assert is_sorted([3, 1, 2, 4]) == False
    assert is_sorted([1, 3, 2]) == False
    print("未排序: ✓")
    
    # 降序检查
    assert is_sorted([5, 4, 3, 2, 1], reverse=True) == True
    assert is_sorted([5, 3, 4, 2, 1], reverse=True) == False
    print("降序排序检查: ✓")
    
    # 带键函数
    assert is_sorted([-1, 2, -3, 4], key=abs) == True
    assert is_sorted([-3, 2, -1, 4], key=abs) == False
    print("键函数排序检查: ✓")
    
    # 边界情况
    assert is_sorted([]) == True
    assert is_sorted([42]) == True
    print("边界情况: ✓")
    
    print("\n✓ 排序检查测试通过")


def test_benchmark_gaps():
    """测试间隔序列性能基准测试"""
    print("\n" + "=" * 50)
    print("测试间隔序列性能基准测试")
    print("=" * 50)
    
    import random
    data = [random.randint(1, 100) for _ in range(50)]
    
    results = benchmark_gaps(data)
    
    print(f"数据长度: {len(data)}")
    print("\n各序列性能:")
    print(f"{'序列':<12} {'比较':>8} {'交换':>8} {'轮数':>6}")
    print("-" * 36)
    
    for seq_name, stats in results.items():
        print(f"{seq_name:<12} {stats['comparisons']:>8} {stats['swaps']:>8} {stats['passes']:>6}")
    
    # 找出最佳序列
    best = min(results.items(), key=lambda x: x[1]['comparisons'])
    print(f"\n最佳序列 (最少比较): {best[0]} ({best[1]['comparisons']} 次比较)")
    
    print("\n✓ 性能基准测试通过")


def test_aliases():
    """测试便捷函数别名"""
    print("\n" + "=" * 50)
    print("测试便捷函数别名")
    print("=" * 50)
    
    data = [5, 3, 1, 4, 2]
    
    result1 = shellsort(data)
    print(f"shellsort: {result1}")
    
    result2 = shellsort(data, reverse=True)
    print(f"shellsort (降序): {result2}")
    
    assert result1 == sorted(data)
    assert result2 == sorted(data, reverse=True)
    
    print("\n✓ 别名函数测试通过")


def test_large_data():
    """测试大数据量排序"""
    print("\n" + "=" * 50)
    print("测试大数据量排序")
    print("=" * 50)
    
    import random
    import time
    
    sizes = [100, 500, 1000]
    
    for size in sizes:
        data = [random.randint(1, 10000) for _ in range(size)]
        
        start = time.time()
        result = shell_sort(data, GapSequence.CIURA)
        elapsed = time.time() - start
        
        print(f"n={size}: {elapsed:.4f}s, 比较={result.comparisons}, 交换={result.swaps}")
        
        assert result.data == sorted(data)
    
    print("\n✓ 大数据量测试通过")


def run_all_tests():
    """运行所有测试"""
    print("\n" + "=" * 60)
    print("Shell Sort Utils 测试套件")
    print("=" * 60)
    
    test_gap_sequences()
    test_basic_shell_sort()
    test_reverse_sort()
    test_key_function()
    test_inplace_sort()
    test_gap_sequence_comparison()
    test_shell_sort_with_trace()
    test_shell_sort_optimized()
    test_shell_sort_pair()
    test_is_sorted()
    test_benchmark_gaps()
    test_aliases()
    test_large_data()
    
    print("\n" + "=" * 60)
    print("✓ 所有测试通过!")
    print("=" * 60)


if __name__ == "__main__":
    run_all_tests()