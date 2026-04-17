#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fenwick Tree 基本用法示例

展示树状数组的基本操作。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from fenwick_tree_utils.mod import FenwickTree, create_fenwick_tree


def example_basic_operations():
    """基本操作示例"""
    print("=" * 50)
    print("基本操作示例")
    print("=" * 50)
    
    # 创建树状数组
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    ft = FenwickTree(data)
    
    print(f"原始数据: {ft.to_list()}")
    print()
    
    # 前缀和查询
    print("前缀和查询:")
    for i in range(len(ft)):
        print(f"  prefix_sum({i}) = {ft.prefix_sum(i)}")
    print()
    
    # 区间和查询
    print("区间和查询:")
    queries = [(0, 4), (3, 7), (5, 9)]
    for left, right in queries:
        print(f"  range_sum({left}, {right}) = {ft.range_sum(left, right)}")
    print()
    
    # 单点更新
    print("单点更新:")
    print(f"  更新前: ft[2] = {ft[2]}")
    ft.add(2, 5)  # 第3个元素加5
    print(f"  add(2, 5) 后: ft[2] = {ft[2]}")
    print(f"  更新后的前缀和(2) = {ft.prefix_sum(2)}")
    print()


def example_dynamic_updates():
    """动态更新示例"""
    print("=" * 50)
    print("动态更新示例")
    print("=" * 50)
    
    # 创建空树状数组
    ft = FenwickTree(size=10)
    print(f"初始状态: {ft.to_list()}")
    
    # 逐步添加数据
    print("\n逐步添加数据:")
    for i in range(10):
        ft.add(i, i + 1)
        print(f"  add({i}, {i+1})")
    
    print(f"\n添加后状态: {ft.to_list()}")
    print(f"总和: {ft.prefix_sum(9)}")
    
    # 动态修改
    print("\n动态修改:")
    ft.set(5, 100)  # 设置第6个元素为100
    print(f"  set(5, 100)")
    print(f"  当前状态: {ft.to_list()}")
    print(f"  新的总和: {ft.prefix_sum(9)}")
    print()


def example_statistics():
    """统计应用示例"""
    print("=" * 50)
    print("统计应用示例")
    print("=" * 50)
    
    # 模拟分数统计
    scores = [85, 90, 78, 92, 88, 76, 95, 82]
    ft = FenwickTree(scores)
    
    print(f"学生分数: {scores}")
    print()
    
    # 计算累计分数
    cumulative = [ft.prefix_sum(i) for i in range(len(scores))]
    print(f"累计分数: {cumulative}")
    
    # 计算区间平均分
    print("\n区间平均分:")
    for start, end in [(0, 2), (3, 5), (0, 7)]:
        total = ft.range_sum(start, end)
        avg = total / (end - start + 1)
        print(f"  学生 {start}-{end}: 总分={total}, 平均={avg:.2f}")
    print()


def example_convenience_functions():
    """便捷函数示例"""
    print("=" * 50)
    print("便捷函数示例")
    print("=" * 50)
    
    from fenwick_tree_utils.mod import fenwick_prefix_sums, fenwick_range_sums
    
    data = [10, 20, 30, 40, 50]
    
    # 计算所有前缀和
    sums = fenwick_prefix_sums(data)
    print(f"数据: {data}")
    print(f"前缀和: {sums}")
    
    # 批量计算区间和
    queries = [(0, 1), (2, 4), (0, 4)]
    results = fenwick_range_sums(data, queries)
    print(f"\n查询: {queries}")
    print(f"结果: {results}")
    print()


def main():
    """运行所有示例"""
    example_basic_operations()
    example_dynamic_updates()
    example_statistics()
    example_convenience_functions()
    
    print("=" * 50)
    print("示例运行完成!")
    print("=" * 50)


if __name__ == "__main__":
    main()