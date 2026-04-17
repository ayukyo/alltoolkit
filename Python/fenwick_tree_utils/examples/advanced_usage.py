#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fenwick Tree 高级用法示例

展示区间更新、二维树状数组、最大/最小值查询等高级功能。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from fenwick_tree_utils.mod import (
    FenwickTreeRangeUpdate,
    FenwickTree2D,
    FenwickTreeMax,
    FenwickTreeMin,
    count_inversions,
    find_kth_element,
    FenwickTree,
)


def example_range_update():
    """区间更新示例"""
    print("=" * 50)
    print("区间更新树状数组示例")
    print("=" * 50)
    
    # 创建区间更新树状数组
    ft = FenwickTreeRangeUpdate(5)
    print("初始状态: [0, 0, 0, 0, 0]")
    
    # 区间更新
    print("\n执行 range_add(0, 2, 10):")
    ft.range_add(0, 2, 10)
    print(f"  当前值: [{ft.get(0)}, {ft.get(1)}, {ft.get(2)}, {ft.get(3)}, {ft.get(4)}]")
    
    print("\n执行 range_add(1, 4, 5):")
    ft.range_add(1, 4, 5)
    print(f"  当前值: [{ft.get(0)}, {ft.get(1)}, {ft.get(2)}, {ft.get(3)}, {ft.get(4)}]")
    
    # 区间和查询
    print("\n区间和查询:")
    print(f"  range_sum(0, 2) = {ft.range_sum(0, 2)}")
    print(f"  range_sum(1, 4) = {ft.range_sum(1, 4)}")
    print(f"  prefix_sum(4) = {ft.prefix_sum(4)}")
    print()


def example_2d_fenwick():
    """二维树状数组示例"""
    print("=" * 50)
    print("二维树状数组示例")
    print("=" * 50)
    
    # 创建 4x4 的二维树状数组
    ft = FenwickTree2D(4, 4)
    print("创建 4x4 二维树状数组")
    
    # 添加数据
    print("\n添加数据:")
    positions = [(0, 0), (1, 1), (2, 2), (3, 3)]
    for row, col in positions:
        value = (row + 1) * 10 + (col + 1)
        ft.add(row, col, value)
        print(f"  add({row}, {col}, {value})")
    
    # 前缀和查询
    print("\n前缀和查询:")
    for row, col in [(0, 0), (1, 1), (2, 2), (3, 3)]:
        print(f"  prefix_sum({row}, {col}) = {ft.prefix_sum(row, col)}")
    
    # 区间和查询
    print("\n区间和查询:")
    print(f"  整个矩阵 (0,0)-(3,3): {ft.range_sum(0, 0, 3, 3)}")
    print(f"  左上角 2x2 (0,0)-(1,1): {ft.range_sum(0, 0, 1, 1)}")
    print(f"  右下角 2x2 (2,2)-(3,3): {ft.range_sum(2, 2, 3, 3)}")
    print()


def example_max_min():
    """最大/最小值查询示例"""
    print("=" * 50)
    print("最大/最小值树状数组示例")
    print("=" * 50)
    
    # 最大值树状数组
    print("最大值树状数组:")
    ft_max = FenwickTreeMax(5)
    values = [3, 7, 2, 9, 5]
    for i, v in enumerate(values):
        ft_max.update(i, v)
    
    print(f"  更新值: {values}")
    print(f"  prefix_max(0) = {ft_max.prefix_max(0)}")
    print(f"  prefix_max(2) = {ft_max.prefix_max(2)}")
    print(f"  prefix_max(4) = {ft_max.prefix_max(4)}")
    
    # 更新更大的值
    print("\n  update(2, 10) (尝试将位置2更新为10):")
    success = ft_max.update(2, 10)
    print(f"    成功: {success}")
    print(f"    prefix_max(4) = {ft_max.prefix_max(4)}")
    
    # 最小值树状数组
    print("\n最小值树状数组:")
    ft_min = FenwickTreeMin(5)
    values = [8, 4, 6, 2, 10]
    for i, v in enumerate(values):
        ft_min.update(i, v)
    
    print(f"  更新值: {values}")
    print(f"  prefix_min(0) = {ft_min.prefix_min(0)}")
    print(f"  prefix_min(3) = {ft_min.prefix_min(3)}")
    print(f"  prefix_min(4) = {ft_min.prefix_min(4)}")
    print()


def example_inversion_count():
    """逆序对计数示例"""
    print("=" * 50)
    print("逆序对计数示例")
    print("=" * 50)
    
    arrays = [
        [1, 2, 3, 4, 5],
        [5, 4, 3, 2, 1],
        [2, 3, 8, 6, 1],
        [3, 1, 2, 1],
    ]
    
    for arr in arrays:
        inversions = count_inversions(arr)
        print(f"数组 {arr}: {inversions} 个逆序对")
    
    print()
    
    # 解释逆序对
    print("逆序对定义:")
    print("  对于数组 A，如果 i < j 且 A[i] > A[j]，")
    print("  则 (i, j) 构成一个逆序对。")
    print()


def example_find_kth():
    """查找第 k 小元素示例"""
    print("=" * 50)
    print("查找第 k 小元素示例")
    print("=" * 50)
    
    # 创建计数树状数组（每个位置表示该值出现的次数）
    ft = FenwickTree([0] * 10)
    
    # 添加数据: 值 2 出现 3 次，值 5 出现 2 次，值 7 出现 1 次
    ft.add(2, 3)  # 值 2 出现 3 次
    ft.add(5, 2)  # 值 5 出现 2 次
    ft.add(7, 1)  # 值 7 出现 1 次
    
    print("数据分布:")
    print(f"  值 2: {ft.get(2)} 次")
    print(f"  值 5: {ft.get(5)} 次")
    print(f"  值 7: {ft.get(7)} 次")
    print(f"  总数: {ft.prefix_sum(9)} 个")
    
    print("\n查找第 k 小:")
    # 第 1-3 小都是 2，第 4-5 小都是 5，第 6 小是 7
    for k in [1, 3, 4, 5, 6]:
        result = find_kth_element(ft, k)
        print(f"  第 {k} 小的值: {result}")
    print()


def example_real_world():
    """实际应用示例"""
    print("=" * 50)
    print("实际应用示例: 动态排名系统")
    print("=" * 50)
    
    # 模拟在线排名系统
    # 每个位置存储该分数段的人数
    max_score = 100
    ft = FenwickTree([0] * (max_score + 1))
    
    # 添加玩家分数
    scores = [85, 90, 78, 92, 88, 76, 95, 82, 90, 85]
    for score in scores:
        ft.add(score, 1)
    
    print("玩家分数分布:")
    for score in [75, 80, 85, 90, 95]:
        count = ft.get(score)
        if count > 0:
            print(f"  分数 {score}: {count} 人")
    
    print("\n统计查询:")
    # 分数 >= 90 的人数
    high_scores = ft.prefix_sum(100) - ft.prefix_sum(89)
    print(f"  分数 >= 90 的人数: {high_scores}")
    
    # 分数在 80-89 的人数
    mid_scores = ft.range_sum(80, 89)
    print(f"  分数 80-89 的人数: {mid_scores}")
    
    # 分数 < 80 的人数
    low_scores = ft.prefix_sum(79)
    print(f"  分数 < 80 的人数: {low_scores}")
    
    # 查询某个分数的排名
    print("\n排名查询:")
    for score in [95, 90, 85]:
        # 比该分数高的人数 + 1 = 排名
        higher = ft.prefix_sum(100) - ft.prefix_sum(score)
        rank = higher + 1
        print(f"  分数 {score}: 排名第 {rank}")
    
    print()


def main():
    """运行所有示例"""
    example_range_update()
    example_2d_fenwick()
    example_max_min()
    example_inversion_count()
    example_find_kth()
    example_real_world()
    
    print("=" * 50)
    print("高级示例运行完成!")
    print("=" * 50)


if __name__ == "__main__":
    main()