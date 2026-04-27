#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Segment Tree Utils 测试文件

测试线段树工具的所有功能。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    SegmentTree,
    SegmentTreeLazy,
    SegmentTreeMin,
    SegmentTreeMax,
    SegmentTreeGCD,
    SegmentTreeXOR,
    SegmentTreeCount,
    SegmentTreeProduct,
    OperationType,
    create_segment_tree,
    range_sum,
    range_min,
    range_max,
    range_gcd,
    gcd,
    lcm,
)


def test_segment_tree_basic():
    """测试基本线段树功能"""
    print("测试基本线段树功能...")
    
    # 创建求和线段树
    data = [1, 2, 3, 4, 5]
    st = SegmentTree(data, OperationType.SUM)
    
    # 验证长度
    assert len(st) == 5
    
    # 测试区间查询
    assert st.query(0, 4) == 15
    assert st.query(1, 3) == 9
    assert st.query(2, 2) == 3
    assert st.query(0, 0) == 1
    
    # 测试获取元素
    assert st.get(0) == 1
    assert st.get(2) == 3
    assert st[4] == 5
    
    print("✓ 基本线段树功能测试通过")


def test_segment_tree_update():
    """测试线段树更新功能"""
    print("测试线段树更新功能...")
    
    st = SegmentTree([0, 0, 0, 0, 0], OperationType.SUM)
    
    # 单点更新
    st.update(0, 10)
    assert st.query(0, 0) == 10
    assert st.query(0, 4) == 10
    
    st.update(2, 5)
    assert st.query(0, 4) == 15
    assert st.query(1, 3) == 5
    
    st.update(4, 3)
    assert st.query(0, 4) == 18
    assert st.query(2, 4) == 8
    
    # 使用 __setitem__
    st[1] = 7
    assert st[1] == 7
    assert st.query(0, 4) == 25
    
    print("✓ 线段树更新功能测试通过")


def test_segment_tree_operations():
    """测试不同操作类型"""
    print("测试不同操作类型...")
    
    data = [5, 3, 7, 1, 9]
    
    # 求和
    st_sum = SegmentTree(data, OperationType.SUM)
    assert st_sum.query(0, 4) == 25
    assert st_sum.query(1, 3) == 11
    
    # 最小值
    st_min = SegmentTree(data, OperationType.MIN)
    assert st_min.query(0, 4) == 1
    assert st_min.query(0, 2) == 3
    assert st_min.query(2, 3) == 1
    
    # 最大值
    st_max = SegmentTree(data, OperationType.MAX)
    assert st_max.query(0, 4) == 9
    assert st_max.query(0, 2) == 7
    assert st_max.query(3, 4) == 9
    
    # GCD
    st_gcd = SegmentTree([12, 18, 24, 36], OperationType.GCD)
    assert st_gcd.query(0, 3) == 6
    assert st_gcd.query(0, 1) == 6
    assert st_gcd.query(1, 2) == 6
    
    # XOR
    st_xor = SegmentTree([1, 2, 3, 4, 5], OperationType.XOR)
    assert st_xor.query(0, 2) == 0  # 1 ^ 2 ^ 3 = 0
    assert st_xor.query(0, 4) == 1  # 1 ^ 2 ^ 3 ^ 4 ^ 5 = 1
    
    print("✓ 不同操作类型测试通过")


def test_segment_tree_edge_cases():
    """测试边界情况"""
    print("测试边界情况...")
    
    # 空数据
    st_empty = SegmentTree([], OperationType.SUM)
    assert len(st_empty) == 0
    
    # 单元素
    st_single = SegmentTree([100], OperationType.SUM)
    assert st_single.query(0, 0) == 100
    
    # 负数
    st_neg = SegmentTree([-1, -2, -3, -4, -5], OperationType.SUM)
    assert st_neg.query(0, 2) == -6
    st_neg.update(0, 10)
    # 更新后: [10, -2, -3, -4, -5], query(0, 2) = 10 + (-2) + (-3) = 5
    assert st_neg.query(0, 2) == 5
    
    # 浮点数
    st_float = SegmentTree([1.5, 2.5, 3.5], OperationType.SUM)
    assert st_float.query(0, 2) == 7.5
    
    print("✓ 边界情况测试通过")


def test_segment_tree_index_errors():
    """测试索引错误"""
    print("测试索引错误处理...")
    
    st = SegmentTree([1, 2, 3, 4, 5], OperationType.SUM)
    
    # 索引越界
    try:
        st.update(10, 1)
        assert False, "应该抛出 IndexError"
    except IndexError:
        pass
    
    try:
        st.get(-1)
        assert False, "应该抛出 IndexError"
    except IndexError:
        pass
    
    try:
        st.query(3, 1)  # left > right
        assert False, "应该抛出 IndexError"
    except IndexError:
        pass
    
    # 空数组查询
    st_empty = SegmentTree([], OperationType.SUM)
    try:
        st_empty.query(0, 0)
        assert False, "应该抛出 ValueError"
    except ValueError:
        pass
    
    print("✓ 索引错误处理测试通过")


def test_segment_tree_lazy():
    """测试懒标记线段树"""
    print("测试懒标记线段树...")
    
    st = SegmentTreeLazy([1, 2, 3, 4, 5])
    
    # 单点更新
    st.update(0, 10)
    assert st.query(0, 0) == 10
    assert st.query(0, 4) == 24
    
    # 区间加
    st.range_add(1, 3, 5)  # [10, 7, 8, 9, 5]
    assert st.query(1, 3) == 24  # 7 + 8 + 9
    assert st.get(1) == 7
    assert st.get(2) == 8
    assert st.get(3) == 9
    
    # 区间设值
    st.range_update(3, 4, 0)  # [10, 7, 8, 0, 0]
    assert st.query(3, 4) == 0
    assert st.query(0, 4) == 25
    assert st.get(3) == 0
    assert st.get(4) == 0
    
    # 多次区间加
    st.range_add(0, 4, 10)  # [20, 17, 18, 10, 10]
    assert st.query(0, 4) == 75
    
    # 混合操作
    st.range_update(0, 2, 5)  # [5, 5, 5, 10, 10]
    assert st.query(0, 4) == 35
    st.range_add(0, 4, 1)  # [6, 6, 6, 11, 11]
    assert st.query(0, 4) == 40
    
    print("✓ 懒标记线段树测试通过")


def test_segment_tree_min_max():
    """测试区间最值线段树"""
    print("测试区间最值线段树...")
    
    # 最小值
    st_min = SegmentTreeMin([5, 3, 7, 1, 9])
    assert st_min.query(0, 4) == 1
    assert st_min.query(0, 2) == 3
    assert st_min.query(3, 4) == 1
    
    st_min.update(3, 10)
    assert st_min.query(0, 4) == 3
    assert st_min.query(3, 4) == 9
    
    # 最大值
    st_max = SegmentTreeMax([5, 3, 7, 1, 9])
    assert st_max.query(0, 4) == 9
    assert st_max.query(0, 2) == 7
    assert st_max.query(3, 4) == 9
    
    st_max.update(2, 20)
    assert st_max.query(0, 4) == 20
    assert st_max.query(0, 2) == 20
    
    print("✓ 区间最值线段树测试通过")


def test_segment_tree_gcd_xor():
    """测试 GCD 和 XOR 线段树"""
    print("测试 GCD 和 XOR 线段树...")
    
    # GCD
    st_gcd = SegmentTreeGCD([12, 18, 24, 36, 48])
    assert st_gcd.query(0, 4) == 6
    assert st_gcd.query(0, 2) == 6
    assert st_gcd.query(2, 4) == 12
    
    st_gcd.update(2, 15)
    assert st_gcd.query(0, 4) == 3  # gcd(12,18,15,36,48) = 3
    
    # XOR
    st_xor = SegmentTreeXOR([1, 2, 3, 4, 5])
    assert st_xor.query(0, 2) == 0  # 1 ^ 2 ^ 3
    assert st_xor.query(0, 4) == 1  # 1 ^ 2 ^ 3 ^ 4 ^ 5
    assert st_xor.query(2, 4) == 3 ^ 4 ^ 5  # = 6
    
    st_xor.update(0, 0)
    assert st_xor.query(0, 4) == 0 ^ 2 ^ 3 ^ 4 ^ 5  # = 14
    
    print("✓ GCD 和 XOR 线段树测试通过")


def test_segment_tree_count():
    """测试计数线段树"""
    print("测试计数线段树...")
    
    # 统计偶数
    st_even = SegmentTreeCount([1, 2, 3, 4, 5], lambda x: x % 2 == 0)
    assert st_even.query(0, 4) == 2  # 2 和 4
    assert st_even.query(0, 2) == 1  # 只有 2
    assert st_even.query(3, 4) == 1  # 只有 4
    
    st_even.update(0, 6)  # 把 1 改为 6（偶数）
    assert st_even.query(0, 4) == 3
    
    # 统计大于某个值的元素
    st_gt3 = SegmentTreeCount([1, 2, 3, 4, 5], lambda x: x > 3)
    assert st_gt3.query(0, 4) == 2  # 4 和 5
    assert st_gt3.query(0, 2) == 0
    
    print("✓ 计数线段树测试通过")


def test_segment_tree_product():
    """测试乘积线段树"""
    print("测试乘积线段树...")
    
    # 无模数
    st_prod = SegmentTreeProduct([1, 2, 3, 4, 5])
    assert st_prod.query(0, 2) == 6  # 1 * 2 * 3
    assert st_prod.query(0, 4) == 120
    assert st_prod.query(2, 3) == 12  # 3 * 4
    
    st_prod.update(0, 2)
    assert st_prod.query(0, 4) == 240  # 2 * 2 * 3 * 4 * 5
    
    # 有模数
    st_mod = SegmentTreeProduct([1, 2, 3, 4, 5], mod=100)
    assert st_mod.query(0, 4) == 20  # 120 % 100
    
    st_mod.update(0, 10)
    assert st_mod.query(0, 4) == 0  # 10*2*3*4*5 = 1200 % 100 = 0
    
    print("✓ 乘积线段树测试通过")


def test_convenience_functions():
    """测试便捷函数"""
    print("测试便捷函数...")
    
    # create_segment_tree
    st = create_segment_tree([1, 2, 3, 4, 5])
    assert st.query(0, 4) == 15
    
    # range_sum
    queries = [(0, 2), (1, 3), (0, 4)]
    results = range_sum([1, 2, 3, 4, 5], queries)
    assert results == [6, 9, 15]
    
    # range_min
    results = range_min([5, 3, 7, 1, 9], queries)
    assert results == [3, 1, 1]
    
    # range_max
    results = range_max([5, 3, 7, 1, 9], queries)
    assert results == [7, 7, 9]
    
    # range_gcd
    results = range_gcd([12, 18, 24, 36], [(0, 1), (1, 2), (0, 3)])
    assert results == [6, 6, 6]
    
    print("✓ 便捷函数测试通过")


def test_gcd_lcm():
    """测试 GCD 和 LCM 函数"""
    print("测试 GCD 和 LCM 函数...")
    
    # GCD
    assert gcd(12, 18) == 6
    assert gcd(0, 5) == 5
    assert gcd(5, 0) == 5
    assert gcd(7, 11) == 1
    assert gcd(-12, 18) == 6
    assert gcd(12, -18) == 6
    
    # LCM
    assert lcm(12, 18) == 36
    assert lcm(7, 11) == 77
    assert lcm(0, 5) == 0
    assert lcm(5, 0) == 0
    assert lcm(-12, 18) == 36
    
    print("✓ GCD 和 LCM 函数测试通过")


def test_to_list():
    """测试转换为列表"""
    print("测试转换为列表...")
    
    st = SegmentTree([1, 2, 3, 4, 5], OperationType.SUM)
    lst = st.to_list()
    assert lst == [1, 2, 3, 4, 5]
    
    # 修改原始数据不影响副本
    st.update(0, 100)
    assert lst == [1, 2, 3, 4, 5]
    assert st.to_list() == [100, 2, 3, 4, 5]
    
    print("✓ 转换为列表测试通过")


def test_repr():
    """测试字符串表示"""
    print("测试字符串表示...")
    
    st = SegmentTree([1, 2, 3], OperationType.SUM)
    assert repr(st) == "SegmentTree([1, 2, 3], op=sum)"
    
    st_lazy = SegmentTreeLazy([1, 2, 3])
    assert repr(st_lazy) == "SegmentTreeLazy([1, 2, 3])"
    
    st_min = SegmentTreeMin([5, 3, 7])
    assert repr(st_min) == "SegmentTreeMin([5, 3, 7])"
    
    st_max = SegmentTreeMax([5, 3, 7])
    assert repr(st_max) == "SegmentTreeMax([5, 3, 7])"
    
    st_gcd = SegmentTreeGCD([12, 18])
    assert repr(st_gcd) == "SegmentTreeGCD([12, 18])"
    
    st_xor = SegmentTreeXOR([1, 2, 3])
    assert repr(st_xor) == "SegmentTreeXOR([1, 2, 3])"
    
    st_prod = SegmentTreeProduct([1, 2, 3])
    assert repr(st_prod) == "SegmentTreeProduct([1, 2, 3])"
    
    st_mod = SegmentTreeProduct([1, 2, 3], mod=10)
    assert repr(st_mod) == "SegmentTreeProduct([1, 2, 3], mod=10)"
    
    print("✓ 字符串表示测试通过")


def test_performance():
    """测试性能（大规模数据）"""
    print("测试性能...")
    
    import time
    
    # 创建大数组
    n = 100000
    data = list(range(1, n + 1))
    
    start = time.time()
    st = SegmentTree(data, OperationType.SUM)
    build_time = time.time() - start
    
    # 区间查询
    start = time.time()
    for i in range(1000):
        st.query(0, n - 1)
    query_time = time.time() - start
    
    # 单点更新
    start = time.time()
    for i in range(1000):
        st.update(i, i + 1)
    update_time = time.time() - start
    
    print(f"  构建 {n} 元素耗时: {build_time:.3f}s")
    print(f"  1000 次区间查询耗时: {query_time:.3f}s")
    print(f"  1000 次单点更新耗时: {update_time:.3f}s")
    
    # 验证结果正确
    # 1000 次更新后，索引 0-999 的值为 1-1000（与原来相同），索引 99999 的值仍为 100000
    assert st.query(n - 1, n - 1) == n
    
    # 测试懒标记线段树性能
    st_lazy = SegmentTreeLazy(data)
    
    start = time.time()
    st_lazy.range_add(0, n - 1, 10)
    range_update_time = time.time() - start
    
    print(f"  1 次区间更新耗时: {range_update_time:.3f}s")
    
    assert st_lazy.query(0, n - 1) == sum(data) + 10 * n
    
    print("✓ 性能测试通过")


def test_complex_scenario():
    """测试复杂场景"""
    print("测试复杂场景...")
    
    # 模拟动态数据统计
    st_lazy = SegmentTreeLazy([0] * 100)
    
    # 多次区间更新（注意有重叠）
    st_lazy.range_add(0, 10, 1)   # indices 0-10 加1
    st_lazy.range_add(10, 20, 2)  # indices 10-20 加2
    st_lazy.range_add(20, 30, 3)  # indices 20-30 加3
    
    # 查询统计（注意重叠部分）
    # indices 0-9: 值1, index 10: 值1+2=3
    assert st_lazy.query(0, 10) == 10 * 1 + 3  # = 13
    # index 10: 值3, indices 11-19: 值2, index 20: 值2+3=5
    assert st_lazy.query(10, 20) == 3 + 9 * 2 + 5  # = 26
    # index 20: 值5, indices 21-30: 值3
    assert st_lazy.query(20, 30) == 5 + 10 * 3  # = 35
    
    # 设置特定值
    st_lazy.range_update(50, 60, 100)
    assert st_lazy.query(50, 60) == 1100  # 100 * 11
    
    # 查询特定区间
    assert st_lazy.query(0, 30) == 10 * 1 + 3 + 9 * 2 + 5 + 10 * 3  # = 13 + 23 + 35 = 71... wait
    # Let me recalculate: 0-9: 10*1=10, 10: 3, 11-19: 9*2=18, 20: 5, 21-30: 10*3=30
    # Total: 10 + 3 + 18 + 5 + 30 = 66
    assert st_lazy.query(0, 30) == 66
    
    # 混合查询
    st_min = SegmentTreeMin([10] * 100)
    st_max = SegmentTreeMax([10] * 100)
    
    for i in range(0, 100, 10):
        st_min.update(i, i // 10)
        st_max.update(i + 5, 100 - i // 10)
    
    assert st_min.query(0, 99) == 0
    assert st_max.query(0, 99) == 100
    
    print("✓ 复杂场景测试通过")


def test_multiple_queries():
    """测试多次查询场景"""
    print("测试多次查询场景...")
    
    data = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
    st_sum = SegmentTree(data, OperationType.SUM)
    st_min = SegmentTree(data, OperationType.MIN)
    st_max = SegmentTree(data, OperationType.MAX)
    
    # 模拟多次查询
    queries = [(0, 5), (3, 8), (2, 10), (0, 10)]
    
    for left, right in queries:
        sum_val = st_sum.query(left, right)
        min_val = st_min.query(left, right)
        max_val = st_max.query(left, right)
        
        # 验证与朴素方法一致
        expected_sum = sum(data[left:right + 1])
        expected_min = min(data[left:right + 1])
        expected_max = max(data[left:right + 1])
        
        assert sum_val == expected_sum
        assert min_val == expected_min
        assert max_val == expected_max
    
    print("✓ 多次查询场景测试通过")


def run_all_tests():
    """运行所有测试"""
    print("=" * 50)
    print("Segment Tree Utils 测试套件")
    print("=" * 50)
    
    test_segment_tree_basic()
    test_segment_tree_update()
    test_segment_tree_operations()
    test_segment_tree_edge_cases()
    test_segment_tree_index_errors()
    test_segment_tree_lazy()
    test_segment_tree_min_max()
    test_segment_tree_gcd_xor()
    test_segment_tree_count()
    test_segment_tree_product()
    test_convenience_functions()
    test_gcd_lcm()
    test_to_list()
    test_repr()
    test_performance()
    test_complex_scenario()
    test_multiple_queries()
    
    print("=" * 50)
    print("所有测试通过! ✓")
    print("=" * 50)


if __name__ == "__main__":
    run_all_tests()