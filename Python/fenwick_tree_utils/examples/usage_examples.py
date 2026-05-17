#!/usr/bin/env python3
"""
Fenwick Tree Utils 使用示例

展示如何使用各种树状数组功能。
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import mod


def example_basic():
    """基础树状数组示例"""
    print("\n=== 基础树状数组示例 ===")
    
    # 从数组创建
    data = [1, 2, 3, 4, 5, 6, 7, 8]
    tree = mod.FenwickTree(data)
    
    print(f"原始数据: {data}")
    print(f"总和: {tree.total}")
    
    # 前缀求和
    print(f"前缀和 [0..3]: {tree.prefix_sum(3)}")  # 1+2+3+4 = 10
    print(f"前缀和 [0..7]: {tree.prefix_sum(7)}")  # 全部 = 36
    
    # 区间求和
    print(f"区间和 [2..5]: {tree.range_sum(2, 5)}")  # 3+4+5+6 = 18
    
    # 单点更新
    tree.update(2, 10)  # 第 2 个元素增加 10
    print(f"更新索引 2 (+10) 后的值: {tree.get_value(2)}")  # 13
    print(f"更新后的区间和 [2..5]: {tree.range_sum(2, 5)}")  # 13+4+5+6 = 28
    
    # 设置值
    tree.set_value(0, 100)
    print(f"设置索引 0 为 100 后的总和: {tree.total}")


def example_diff():
    """差分数组变体示例"""
    print("\n=== 差分数组变体示例 ===")
    
    # 创建差分树状数组
    tree = mod.FenwickTreeDiff(size=5)
    
    print("初始数组: [0, 0, 0, 0, 0]")
    
    # 区间更新
    tree.range_update(1, 3, 5)  # [1, 3] 增加 5
    print(f"区间更新 [1..3] += 5")
    
    # 查询各点
    for i in range(5):
        print(f"  query({i}) = {tree.query(i)}")
    
    # 再更新
    tree.range_update(2, 4, 3)
    print(f"区间更新 [2..4] += 3")
    
    for i in range(5):
        print(f"  query({i}) = {tree.query(i)}")


def example_range():
    """区间更新区间查询示例"""
    print("\n=== 区间更新区间查询示例 ===")
    
    tree = mod.FenwickTreeRange(size=6)
    
    print("初始数组: [0, 0, 0, 0, 0, 0]")
    
    # 区间更新
    tree.range_update(1, 4, 10)
    print(f"区间更新 [1..4] += 10")
    print(f"区间查询 [0..5]: {tree.range_query(0, 5)}")  # 40
    
    # 再次更新
    tree.range_update(2, 5, 5)
    print(f"区间更新 [2..5] += 5")
    print(f"区间查询 [2..4]: {tree.range_query(2, 4)}")  # 10+5 + 10+5 + 10+5 = 45
    
    # 验证各部分
    print("验证:")
    print(f"  [0..1]: {tree.range_query(0, 1)}")   # 10
    print(f"  [1..4]: {tree.range_query(1, 4)}")   # 60
    print(f"  [2..5]: {tree.range_query(2, 5)}")   # 65


def example_2d():
    """二维树状数组示例"""
    print("\n=== 二维树状数组示例 ===")
    
    # 创建矩阵
    matrix = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12]
    ]
    
    tree = mod.FenwickTree2D(matrix)
    
    print(f"矩阵:")
    for row in matrix:
        print(f"  {row}")
    
    print(f"\n总和: {tree.total}")
    
    # 矩形区域求和
    print(f"矩形 [0,0] 到 [1,1]: {tree.range_sum(0, 0, 1, 1)}")  # 1+2+5+6 = 14
    print(f"矩形 [1,1] 到 [2,2]: {tree.range_sum(1, 1, 2, 2)}")  # 6+7+10+11 = 34
    
    # 单点更新
    tree.update(1, 1, 100)
    print(f"\n更新 (1,1) += 100")
    print(f"矩形 [1,1] 到 [2,2]: {tree.range_sum(1, 1, 2, 2)}")  # 106+7+110+11 = 234


def example_min():
    """RMQ 树状数组示例"""
    print("\n=== RMQ 树状数组示例 ===")
    
    # 最小值树
    data = [5, 3, 7, 2, 8, 1, 9]
    min_tree = mod.FenwickTreeMin(data)
    
    print(f"数据: {data}")
    print(f"前缀最小值查询:")
    for i in range(len(data)):
        print(f"  min[0..{i}] = {min_tree.query(i)}")
    
    # 最大值树
    max_tree = mod.FenwickTreeMin(data, comparator=max)
    print(f"\n前缀最大值查询:")
    for i in range(len(data)):
        print(f"  max[0..{i}] = {max_tree.query(i)}")
    
    # 更新
    min_tree.update(0, 0)
    print(f"\n更新索引 0 为 0 后的 min[0..4]: {min_tree.query(4)}")


def example_kth():
    """第 k 小查找示例"""
    print("\n=== 第 k 小查找示例 ===")
    
    # 使用频数数组（例如统计排序后的位置）
    tree = mod.FenwickTree(size=10)
    
    # 添加一些元素
    positions = [2, 2, 2, 5, 5, 7, 7, 7, 7]
    for pos in positions:
        tree.update(pos, 1)
    
    print(f"频数分布:")
    for i in range(10):
        print(f"  位置 {i}: {tree.get_value(i)}")
    
    print(f"\n查找第 k 小:")
    for k in [1, 3, 4, 6, 9]:
        pos = tree.find_kth(k)
        print(f"  第 {k} 小的位置: {pos}")


def example_convenience():
    """便捷函数示例"""
    print("\n=== 便捷函数示例 ===")
    
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    # 快速前缀求和
    print(f"数据: {data}")
    print(f"prefix_sum(data, 4): {mod.prefix_sum(data, 4)}")  # 1+2+3+4+5 = 15
    
    # 快速区间求和
    print(f"range_sum(data, 3, 7): {mod.range_sum(data, 3, 7)}")  # 4+5+6+7+8 = 30
    
    # 创建不同类型
    print(f"\n创建不同类型的树状数组:")
    tree_std = mod.create_fenwick_tree(data, 'standard')
    tree_diff = mod.create_fenwick_tree(data, 'diff')
    tree_min = mod.create_fenwick_tree(data, 'min')
    
    print(f"  standard: {tree_std}")
    print(f"  diff: {tree_diff}")
    print(f"  min: {tree_min}")


def example_practical():
    """实际应用示例"""
    print("\n=== 实际应用示例 ===")
    
    # 场景：维护动态数组，支持快速查询
    print("场景: 动态数组求和")
    
    data = [i * i for i in range(1, 11)]  # 1, 4, 9, 16, 25, 36, 49, 64, 81, 100
    tree = mod.FenwickTree(data)
    
    print(f"平方数: {data}")
    print(f"总和: {tree.total}")
    
    # 更新操作
    tree.update(4, 50)  # 第 5 个元素增加 50
    print(f"更新索引 4 (+50) 后的总和: {tree.total}")
    
    # 区间查询
    print(f"区间 [3..6] 的和: {tree.range_sum(3, 6)}")


def main():
    """运行所有示例"""
    print("=" * 60)
    print("Fenwick Tree Utils 使用示例")
    print("=" * 60)
    
    example_basic()
    example_diff()
    example_range()
    example_2d()
    example_min()
    example_kth()
    example_convenience()
    example_practical()
    
    print("\n" + "=" * 60)
    print("示例运行完成！")
    print("=" * 60)


if __name__ == '__main__':
    main()