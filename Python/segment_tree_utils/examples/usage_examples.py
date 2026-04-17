#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Segment Tree Utils 使用示例

展示线段树工具库的各种用法。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from segment_tree_utils.mod import (
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
)


def example_basic_usage():
    """基本使用示例"""
    print("\n" + "=" * 50)
    print("基本使用示例")
    print("=" * 50)
    
    # 创建求和线段树
    data = [1, 3, 5, 7, 9, 11]
    st = SegmentTree(data, OperationType.SUM)
    
    print(f"数据: {data}")
    print(f"整个数组之和: {st.query(0, 5)}")
    print(f"区间 [1, 3] 之和: {st.query(1, 3)}")
    print(f"区间 [2, 4] 之和: {st.query(2, 4)}")
    
    # 更新元素
    st.update(0, 10)
    print(f"\n更新索引 0 为 10 后:")
    print(f"整个数组之和: {st.query(0, 5)}")
    print(f"当前数组: {st.to_list()}")


def example_min_max():
    """区间最值示例"""
    print("\n" + "=" * 50)
    print("区间最值示例")
    print("=" * 50)
    
    data = [3, 1, 4, 1, 5, 9, 2, 6]
    print(f"数据: {data}")
    
    # 最小值线段树
    st_min = SegmentTreeMin(data)
    print(f"区间 [0, 7] 最小值: {st_min.query(0, 7)}")
    print(f"区间 [0, 3] 最小值: {st_min.query(0, 3)}")
    print(f"区间 [4, 7] 最小值: {st_min.query(4, 7)}")
    
    # 最大值线段树
    st_max = SegmentTreeMax(data)
    print(f"\n区间 [0, 7] 最大值: {st_max.query(0, 7)}")
    print(f"区间 [0, 3] 最大值: {st_max.query(0, 3)}")
    print(f"区间 [4, 7] 最大值: {st_max.query(4, 7)}")
    
    # 更新后查询
    st_min.update(4, 0)  # 将最大值改为最小值
    print(f"\n更新索引 4 为 0 后:")
    print(f"区间 [0, 7] 最小值: {st_min.query(0, 7)}")


def example_lazy_propagation():
    """懒标记（区间更新）示例"""
    print("\n" + "=" * 50)
    print("懒标记（区间更新）示例")
    print("=" * 50)
    
    data = [1, 2, 3, 4, 5, 6, 7, 8]
    st = SegmentTreeLazy(data)
    print(f"初始数据: {data}")
    print(f"初始总和: {st.query(0, 7)}")
    
    # 区间加
    st.range_add(0, 3, 10)  # 前4个元素各加10
    print(f"\n区间 [0, 3] 各加 10 后:")
    print(f"数组: {st.to_list()}")
    print(f"总和: {st.query(0, 7)}")
    
    # 区间设值
    st.range_update(4, 7, 0)  # 后4个元素设为0
    print(f"\n区间 [4, 7] 设为 0 后:")
    print(f"数组: {st.to_list()}")
    print(f"总和: {st.query(0, 7)}")
    
    # 再次区间加
    st.range_add(0, 7, 5)  # 所有元素各加5
    print(f"\n整个数组各加 5 后:")
    print(f"数组: {st.to_list()}")
    print(f"总和: {st.query(0, 7)}")


def example_gcd_xor():
    """GCD 和 XOR 示例"""
    print("\n" + "=" * 50)
    print("GCD 和 XOR 示例")
    print("=" * 50)
    
    # GCD 示例
    data = [24, 36, 48, 60, 72]
    st_gcd = SegmentTreeGCD(data)
    print(f"数据: {data}")
    print(f"区间 [0, 4] GCD: {st_gcd.query(0, 4)}")
    print(f"区间 [0, 2] GCD: {st_gcd.query(0, 2)}")
    print(f"区间 [2, 4] GCD: {st_gcd.query(2, 4)}")
    
    # XOR 示例
    data_xor = [1, 2, 3, 4, 5, 6, 7]
    st_xor = SegmentTreeXOR(data_xor)
    print(f"\n数据: {data_xor}")
    print(f"区间 [0, 6] XOR: {st_xor.query(0, 6)}")
    print(f"区间 [0, 2] XOR: {st_xor.query(0, 2)} (1^2^3=0)")
    print(f"区间 [3, 6] XOR: {st_xor.query(3, 6)}")


def example_count():
    """计数线段树示例"""
    print("\n" + "=" * 50)
    print("计数线段树示例")
    print("=" * 50)
    
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    # 统计偶数个数
    st_even = SegmentTreeCount(data, lambda x: x % 2 == 0)
    print(f"数据: {data}")
    print(f"区间 [0, 9] 偶数个数: {st_even.query(0, 9)}")
    print(f"区间 [0, 4] 偶数个数: {st_even.query(0, 4)}")
    
    # 统计大于5的元素个数
    st_gt5 = SegmentTreeCount(data, lambda x: x > 5)
    print(f"\n区间 [0, 9] 大于5的元素个数: {st_gt5.query(0, 9)}")
    print(f"区间 [0, 5] 大于5的元素个数: {st_gt5.query(0, 5)}")
    
    # 统计能被3整除的元素个数
    st_div3 = SegmentTreeCount(data, lambda x: x % 3 == 0)
    print(f"\n区间 [0, 9] 能被3整除的元素个数: {st_div3.query(0, 9)}")


def example_product():
    """乘积线段树示例"""
    print("\n" + "=" * 50)
    print("乘积线段树示例")
    print("=" * 50)
    
    # 无模数
    data = [1, 2, 3, 4, 5]
    st = SegmentTreeProduct(data)
    print(f"数据: {data}")
    print(f"区间 [0, 4] 乘积: {st.query(0, 4)}")
    print(f"区间 [0, 2] 乘积: {st.query(0, 2)}")
    
    # 有模数（用于大数计算）
    st_mod = SegmentTreeProduct(data, mod=100)
    print(f"\n使用模数 100:")
    print(f"区间 [0, 4] 乘积: {st_mod.query(0, 4)}")
    
    # 大数示例
    large_data = [10, 20, 30, 40, 50]
    st_large = SegmentTreeProduct(large_data, mod=1000000)
    print(f"\n大数数据: {large_data}")
    print(f"区间 [0, 4] 乘积 (mod 1000000): {st_large.query(0, 4)}")


def example_convenience_functions():
    """便捷函数示例"""
    print("\n" + "=" * 50)
    print("便捷函数示例")
    print("=" * 50)
    
    data = [3, 1, 4, 1, 5, 9, 2, 6]
    queries = [(0, 3), (2, 5), (4, 7)]
    
    print(f"数据: {data}")
    print(f"查询: {queries}")
    
    # 批量求和
    sums = range_sum(data, queries)
    print(f"\n批量求和结果: {sums}")
    
    # 批量最小值
    mins = range_min(data, queries)
    print(f"批量最小值结果: {mins}")
    
    # 批量最大值
    maxs = range_max(data, queries)
    print(f"批量最大值结果: {maxs}")
    
    # 批量 GCD
    gcd_data = [12, 18, 24, 36, 48]
    gcd_queries = [(0, 2), (1, 4), (0, 4)]
    gcds = range_gcd(gcd_data, gcd_queries)
    print(f"\nGCD 数据: {gcd_data}")
    print(f"批量 GCD 结果: {gcds}")


def example_dynamic_statistics():
    """动态统计示例"""
    print("\n" + "=" * 50)
    print("动态统计示例 - 模拟实时数据")
    print("=" * 50)
    
    # 模拟温度数据
    temperatures = [20, 22, 25, 28, 30, 28, 25, 22]
    st_sum = SegmentTree(temperatures, OperationType.SUM)
    st_min = SegmentTreeMin(temperatures)
    st_max = SegmentTreeMax(temperatures)
    
    print(f"温度数据: {temperatures}")
    print(f"平均温度: {st_sum.query(0, 7) / len(temperatures):.2f}")
    print(f"最低温度: {st_min.query(0, 7)}")
    print(f"最高温度: {st_max.query(0, 7)}")
    print(f"温度范围: {st_max.query(0, 7) - st_min.query(0, 7)}")
    
    # 模拟温度更新
    print("\n温度更新: 索引 0 升高到 25，索引 4 升高到 35")
    st_sum.update(0, 25)
    st_min.update(0, 25)
    st_max.update(0, 25)
    st_sum.update(4, 35)
    st_max.update(4, 35)
    
    print(f"更新后平均温度: {st_sum.query(0, 7) / len(temperatures):.2f}")
    print(f"更新后最低温度: {st_min.query(0, 7)}")
    print(f"更新后最高温度: {st_max.query(0, 7)}")


def example_array_manipulation():
    """数组批量操作示例"""
    print("\n" + "=" * 50)
    print("数组批量操作示例")
    print("=" * 50)
    
    # 使用懒标记线段树进行批量操作
    st = SegmentTreeLazy([0] * 10)
    
    print("初始数组: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]")
    
    # 批量设置
    st.range_update(0, 4, 1)   # 前5个设为1
    st.range_update(5, 9, 2)   # 后5个设为2
    print(f"批量设值后: {st.to_list()}")
    print(f"总和: {st.query(0, 9)}")
    
    # 批量加值
    st.range_add(0, 9, 5)      # 全部加5
    print(f"全部加5后: {st.to_list()}")
    print(f"总和: {st.query(0, 9)}")
    
    # 局部调整
    st.range_add(2, 6, 3)      # 中间部分再加3
    print(f"中间再加3后: {st.to_list()}")
    print(f"总和: {st.query(0, 9)}")


def example_competitive_programming():
    """竞赛编程示例"""
    print("\n" + "=" * 50)
    print("竞赛编程示例 - 常见问题")
    print("=" * 50)
    
    # 问题1: 区间求和 + 单点更新
    print("问题1: 区间求和 + 单点更新")
    arr = [5, 3, 7, 1, 9, 11, 8, 6]
    st = SegmentTree(arr, OperationType.SUM)
    
    print(f"数组: {arr}")
    
    # 查询区间和
    print(f"查询 [2, 5]: {st.query(2, 5)}")
    
    # 更新单点
    st.update(3, 10)
    print(f"更新位置3为10后，查询 [2, 5]: {st.query(2, 5)}")
    
    # 问题2: 区间最小值 + 区间最大值同时查询
    print("\n问题2: 同时查询区间最小值和最大值")
    arr2 = [10, 5, 20, 8, 15, 25, 12]
    st_min = SegmentTreeMin(arr2)
    st_max = SegmentTreeMax(arr2)
    
    for i in range(0, len(arr2), 2):
        end = min(i + 2, len(arr2) - 1)
        print(f"区间 [{i}, {end}]: min={st_min.query(i, end)}, max={st_max.query(i, end)}")
    
    # 问题3: 区间GCD
    print("\n问题3: 区间GCD")
    arr3 = [48, 36, 60, 72, 96]
    st_gcd = SegmentTreeGCD(arr3)
    print(f"数组: {arr3}")
    print(f"整个数组GCD: {st_gcd.query(0, 4)}")
    print(f"前半部分GCD: {st_gcd.query(0, 2)}")


def main():
    """运行所有示例"""
    print("=" * 50)
    print("Segment Tree Utils 使用示例")
    print("=" * 50)
    
    example_basic_usage()
    example_min_max()
    example_lazy_propagation()
    example_gcd_xor()
    example_count()
    example_product()
    example_convenience_functions()
    example_dynamic_statistics()
    example_array_manipulation()
    example_competitive_programming()
    
    print("\n" + "=" * 50)
    print("所有示例运行完成!")
    print("=" * 50)


if __name__ == "__main__":
    main()