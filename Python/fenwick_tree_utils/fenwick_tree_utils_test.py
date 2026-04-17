#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fenwick Tree Utils 测试文件

测试树状数组工具的所有功能。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fenwick_tree_utils.mod import (
    FenwickTree,
    FenwickTreeRangeUpdate,
    FenwickTree2D,
    FenwickTreeMax,
    FenwickTreeMin,
    create_fenwick_tree,
    fenwick_prefix_sums,
    fenwick_range_sums,
    count_inversions,
    find_kth_element,
)


def test_fenwick_tree_basic():
    """测试基本树状数组功能"""
    print("测试基本树状数组功能...")
    
    # 创建树状数组
    data = [1, 2, 3, 4, 5]
    ft = FenwickTree(data)
    
    # 验证长度
    assert len(ft) == 5
    
    # 测试前缀和
    assert ft.prefix_sum(0) == 1
    assert ft.prefix_sum(1) == 3
    assert ft.prefix_sum(2) == 6
    assert ft.prefix_sum(3) == 10
    assert ft.prefix_sum(4) == 15
    
    # 测试区间和
    assert ft.range_sum(0, 4) == 15
    assert ft.range_sum(1, 3) == 9
    assert ft.range_sum(2, 2) == 3
    
    # 测试获取元素
    assert ft.get(0) == 1
    assert ft.get(2) == 3
    assert ft[4] == 5
    
    print("✓ 基本树状数组功能测试通过")


def test_fenwick_tree_update():
    """测试树状数组更新功能"""
    print("测试树状数组更新功能...")
    
    ft = FenwickTree([0, 0, 0, 0, 0])
    
    # 单点添加
    ft.add(0, 10)
    assert ft.prefix_sum(0) == 10
    assert ft.prefix_sum(4) == 10
    
    ft.add(2, 5)
    assert ft.prefix_sum(2) == 15
    assert ft.prefix_sum(4) == 15
    
    ft.add(4, 3)
    assert ft.prefix_sum(4) == 18
    assert ft.range_sum(2, 4) == 8
    
    # 单点设置
    ft.set(0, 20)
    assert ft.get(0) == 20
    assert ft.prefix_sum(4) == 28
    
    ft[1] = 7  # 使用 __setitem__
    assert ft[1] == 7
    
    print("✓ 树状数组更新功能测试通过")


def test_fenwick_tree_edge_cases():
    """测试边界情况"""
    print("测试边界情况...")
    
    # 空数据
    ft_empty = FenwickTree([])
    assert len(ft_empty) == 0
    
    # 单元素
    ft_single = FenwickTree([100])
    assert ft_single.prefix_sum(0) == 100
    assert ft_single.range_sum(0, 0) == 100
    
    # 负数
    ft_neg = FenwickTree([-1, -2, -3, -4, -5])
    assert ft_neg.prefix_sum(2) == -6
    ft_neg.add(0, 10)
    assert ft_neg.prefix_sum(2) == 4
    
    # 浮点数
    ft_float = FenwickTree([1.5, 2.5, 3.5])
    assert ft_float.prefix_sum(2) == 7.5
    
    # 边界索引测试
    ft = FenwickTree([1, 2, 3, 4, 5])
    assert ft.prefix_sum(-1) == 0  # 负索引返回 0
    assert ft.prefix_sum(100) == 15  # 超出范围返回总和
    
    print("✓ 边界情况测试通过")


def test_fenwick_tree_index_errors():
    """测试索引错误"""
    print("测试索引错误处理...")
    
    ft = FenwickTree([1, 2, 3, 4, 5])
    
    # 索引越界
    try:
        ft.add(10, 1)
        assert False, "应该抛出 IndexError"
    except IndexError:
        pass
    
    try:
        ft.get(-1)
        assert False, "应该抛出 IndexError"
    except IndexError:
        pass
    
    try:
        ft.range_sum(3, 1)  # left > right
        assert False, "应该抛出 IndexError"
    except IndexError:
        pass
    
    print("✓ 索引错误处理测试通过")


def test_fenwick_tree_range_update():
    """测试区间更新树状数组"""
    print("测试区间更新树状数组...")
    
    ft = FenwickTreeRangeUpdate(5)
    
    # 单点更新方式：区间更新只有一个元素
    ft.range_add(0, 0, 10)
    assert ft.get(0) == 10
    assert ft.get(1) == 0
    
    # 区间更新
    ft.range_add(0, 2, 5)  # [15, 5, 5, 0, 0]
    assert ft.get(0) == 15
    assert ft.get(1) == 5
    assert ft.get(2) == 5
    assert ft.get(3) == 0
    
    # 前缀和
    assert ft.prefix_sum(0) == 15
    assert ft.prefix_sum(2) == 25
    
    # 区间和
    assert ft.range_sum(1, 3) == 10  # 5 + 5 + 0
    
    # 多次区间更新
    ft.range_add(2, 4, 10)  # [15, 5, 15, 10, 10]
    assert ft.get(2) == 15
    assert ft.get(4) == 10
    assert ft.range_sum(0, 4) == 55
    
    print("✓ 区间更新树状数组测试通过")


def test_fenwick_tree_2d():
    """测试二维树状数组"""
    print("测试二维树状数组...")
    
    ft = FenwickTree2D(3, 3)
    
    # 验证形状
    assert ft.shape == (3, 3)
    
    # 单点更新
    ft.add(0, 0, 1)
    ft.add(1, 1, 10)
    ft.add(2, 2, 100)
    
    # 前缀和
    assert ft.prefix_sum(0, 0) == 1
    assert ft.prefix_sum(1, 1) == 11
    assert ft.prefix_sum(2, 2) == 111
    
    # 区间和
    assert ft.range_sum(0, 0, 2, 2) == 111
    assert ft.range_sum(0, 0, 1, 1) == 11
    assert ft.range_sum(1, 0, 2, 1) == 10
    
    # 获取元素
    assert ft.get(1, 1) == 10
    
    # 设置元素
    ft.set(0, 0, 5)
    assert ft.get(0, 0) == 5
    
    print("✓ 二维树状数组测试通过")


def test_fenwick_tree_max():
    """测试最大值树状数组"""
    print("测试最大值树状数组...")
    
    ft = FenwickTreeMax(5)
    
    # 更新值
    assert ft.update(0, 3) == True
    assert ft.update(2, 5) == True
    assert ft.update(4, 2) == True
    
    # 尝试减小（应该失败）
    assert ft.update(0, 2) == False
    assert ft.get(0) == 3
    
    # 前缀最大值
    assert ft.prefix_max(0) == 3
    assert ft.prefix_max(1) == 3
    assert ft.prefix_max(2) == 5
    assert ft.prefix_max(4) == 5
    
    # 更新更大的值
    assert ft.update(1, 10) == True
    assert ft.prefix_max(4) == 10
    
    print("✓ 最大值树状数组测试通过")


def test_fenwick_tree_min():
    """测试最小值树状数组"""
    print("测试最小值树状数组...")
    
    ft = FenwickTreeMin(5)
    
    # 更新值
    assert ft.update(0, 3) == True
    assert ft.update(2, 1) == True
    assert ft.update(4, 5) == True
    
    # 尝试增大（应该失败）
    assert ft.update(0, 10) == False
    assert ft.get(0) == 3
    
    # 前缀最小值
    assert ft.prefix_min(0) == 3
    assert ft.prefix_min(2) == 1
    assert ft.prefix_min(4) == 1
    
    # 更新更小的值
    assert ft.update(3, 0) == True
    assert ft.prefix_min(4) == 0
    
    print("✓ 最小值树状数组测试通过")


def test_convenience_functions():
    """测试便捷函数"""
    print("测试便捷函数...")
    
    # create_fenwick_tree
    ft = create_fenwick_tree([1, 2, 3, 4, 5])
    assert ft.prefix_sum(4) == 15
    
    # fenwick_prefix_sums
    sums = fenwick_prefix_sums([1, 2, 3, 4, 5])
    assert sums == [1, 3, 6, 10, 15]
    
    # fenwick_range_sums
    queries = [(0, 2), (1, 3), (0, 4)]
    results = fenwick_range_sums([1, 2, 3, 4, 5], queries)
    assert results == [6, 9, 15]
    
    print("✓ 便捷函数测试通过")


def test_count_inversions():
    """测试逆序对计数"""
    print("测试逆序对计数...")
    
    # 无逆序对
    assert count_inversions([1, 2, 3, 4, 5]) == 0
    
    # 完全逆序
    assert count_inversions([5, 4, 3, 2, 1]) == 10
    
    # 部分逆序
    assert count_inversions([2, 3, 8, 6, 1]) == 5
    
    # 单元素
    assert count_inversions([1]) == 0
    
    # 空数组
    assert count_inversions([]) == 0
    
    # 有重复元素
    assert count_inversions([3, 1, 2, 1]) == 4
    
    print("✓ 逆序对计数测试通过")


def test_find_kth_element():
    """测试查找第 k 小元素"""
    print("测试查找第 k 小元素...")
    
    # 创建计数树状数组
    ft = FenwickTree([0] * 5)
    ft.add(0, 1)  # 第 1 小的元素在位置 0
    ft.add(2, 1)  # 第 2 小的元素在位置 2
    ft.add(4, 1)  # 第 3 小的元素在位置 4
    
    # 查找第 k 小
    assert find_kth_element(ft, 1) == 0
    assert find_kth_element(ft, 2) == 2
    assert find_kth_element(ft, 3) == 4
    
    # 边界错误
    try:
        find_kth_element(ft, 0)
        assert False, "应该抛出 ValueError"
    except ValueError:
        pass
    
    try:
        find_kth_element(ft, 10)
        assert False, "应该抛出 ValueError"
    except ValueError:
        pass
    
    print("✓ 查找第 k 小元素测试通过")


def test_performance():
    """测试性能（大规模数据）"""
    print("测试性能...")
    
    import time
    
    # 创建大数组
    n = 100000
    data = list(range(1, n + 1))
    
    start = time.time()
    ft = FenwickTree(data)
    build_time = time.time() - start
    
    # 前缀和查询
    start = time.time()
    for i in range(1000):
        ft.prefix_sum(n - 1)
    query_time = time.time() - start
    
    # 单点更新
    start = time.time()
    for i in range(1000):
        ft.add(i, 1)
    update_time = time.time() - start
    
    print(f"  构建 {n} 元素耗时: {build_time:.3f}s")
    print(f"  1000 次前缀和查询耗时: {query_time:.3f}s")
    print(f"  1000 次单点更新耗时: {update_time:.3f}s")
    
    # 验证结果正确
    expected_sum = sum(range(1, n + 1)) + 1000  # 加上更新的值
    assert ft.prefix_sum(n - 1) == expected_sum
    
    print("✓ 性能测试通过")


def test_repr():
    """测试字符串表示"""
    print("测试字符串表示...")
    
    ft = FenwickTree([1, 2, 3])
    assert repr(ft) == "FenwickTree([1, 2, 3])"
    
    ft_range = FenwickTreeRangeUpdate(5)
    assert repr(ft_range) == "FenwickTreeRangeUpdate(size=5)"
    
    ft_2d = FenwickTree2D(3, 4)
    assert repr(ft_2d) == "FenwickTree2D(rows=3, cols=4)"
    
    ft_max = FenwickTreeMax(5)
    assert repr(ft_max) == "FenwickTreeMax(size=5)"
    
    ft_min = FenwickTreeMin(5)
    assert repr(ft_min) == "FenwickTreeMin(size=5)"
    
    print("✓ 字符串表示测试通过")


def test_to_list():
    """测试转换为列表"""
    print("测试转换为列表...")
    
    ft = FenwickTree([1, 2, 3, 4, 5])
    lst = ft.to_list()
    assert lst == [1, 2, 3, 4, 5]
    
    # 修改原始数据不影响副本
    ft.add(0, 100)
    assert lst == [1, 2, 3, 4, 5]
    assert ft.to_list() == [101, 2, 3, 4, 5]
    
    print("✓ 转换为列表测试通过")


def test_complex_scenario():
    """测试复杂场景"""
    print("测试复杂场景...")
    
    # 模拟动态数据统计
    ft = FenwickTree([0] * 100)
    
    # 添加数据
    for i in range(10):
        ft.add(i * 10, i + 1)
    
    # 查询统计
    assert ft.range_sum(0, 90) == sum(range(1, 11))
    
    # 更新数据
    ft.add(50, 5)
    assert ft.get(50) == 11  # 原值 6 + 新增 5
    
    # 查询特定区间
    assert ft.range_sum(40, 60) == 5 + 11 + 7  # 位置 40, 50, 60
    
    print("✓ 复杂场景测试通过")


def run_all_tests():
    """运行所有测试"""
    print("=" * 50)
    print("Fenwick Tree Utils 测试套件")
    print("=" * 50)
    
    test_fenwick_tree_basic()
    test_fenwick_tree_update()
    test_fenwick_tree_edge_cases()
    test_fenwick_tree_index_errors()
    test_fenwick_tree_range_update()
    test_fenwick_tree_2d()
    test_fenwick_tree_max()
    test_fenwick_tree_min()
    test_convenience_functions()
    test_count_inversions()
    test_find_kth_element()
    test_performance()
    test_repr()
    test_to_list()
    test_complex_scenario()
    
    print("=" * 50)
    print("所有测试通过! ✓")
    print("=" * 50)


if __name__ == "__main__":
    run_all_tests()