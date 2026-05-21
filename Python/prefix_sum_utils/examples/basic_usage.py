#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
前缀和与差分数组工具模块示例

演示各种使用场景和技巧
"""

import sys
sys.path.insert(0, '..')

from mod import (
    PrefixSum,
    PrefixSum2D,
    DifferenceArray,
    DifferenceArray2D,
    build_prefix_sum,
    range_sum,
)


def example_prefix_sum():
    """一维前缀和示例"""
    print("=" * 50)
    print("一维前缀和示例")
    print("=" * 50)
    
    # 计算子数组和
    arr = [1, 4, 2, 5, 3]
    ps = PrefixSum(arr)
    
    print(f"原始数组: {arr}")
    print(f"前缀和数组: {ps.prefix_array}")
    
    # 快速计算任意区间和
    queries = [(0, 2), (1, 3), (2, 4), (0, 4)]
    for left, right in queries:
        sum_val = ps.range_sum(left, right)
        print(f"区间 [{left}, {right}] 的和: {sum_val}")
    
    print()


def example_prefix_sum_2d():
    """二维前缀和示例"""
    print("=" * 50)
    print("二维前缀和示例")
    print("=" * 50)
    
    # 图像亮度矩阵
    brightness = [
        [100, 120, 80, 90],
        [110, 130, 70, 85],
        [105, 125, 75, 88],
        [98, 118, 82, 92]
    ]
    
    ps2d = PrefixSum2D(brightness)
    
    print("亮度矩阵:")
    for row in brightness:
        print(row)
    
    # 计算区域平均亮度
    regions = [
        ((0, 0), (1, 1), "左上角"),
        ((2, 2), (3, 3), "右下角"),
        ((1, 1), (2, 2), "中心区域")
    ]
    
    for (r1, c1), (r2, c2), name in regions:
        area_sum = ps2d.region_sum(r1, c1, r2, c2)
        area_size = (r2 - r1 + 1) * (c2 - c1 + 1)
        avg = area_sum / area_size
        print(f"{name} 区域亮度: 总和={area_sum}, 平均={avg:.1f}")
    
    print()


def example_difference_array():
    """一维差分数组示例"""
    print("=" * 50)
    print("一维差分数组示例")
    print("=" * 50)
    
    # 航班预订问题
    # 有 n 个航班，初始座位数为 0
    # 处理多个预订请求
    bookings = [
        (1, 2, 10),  # 预订航班 1-2，加 10 个座位
        (0, 1, 20),  # 预订航班 0-1，加 20 个座位
        (2, 3, 15),  # 预订航班 2-3，加 15 个座位
    ]
    
    n = 4  # 航班数量
    da = DifferenceArray(size=n)
    
    print(f"航班数量: {n}")
    print("预订请求:")
    for first, last, seats in bookings:
        print(f"  航班 {first}-{last}: +{seats} 座位")
        da.range_add(first, last, seats)
    
    result = da.to_array()
    print(f"最终座位分配: {result}")
    
    print()


def example_difference_array_2d():
    """二维差分数组示例"""
    print("=" * 50)
    print("二维差分数组示例")
    print("=" * 50)
    
    # 矩形区域染色问题
    # 在一块白色画布上染色
    da2d = DifferenceArray2D(rows=5, cols=5)
    
    colors = [
        ((0, 0), (2, 2), 1, "红色"),   # 左上角染红色
        ((1, 1), (3, 3), 2, "蓝色"),   # 中间染蓝色（部分重叠）
        ((3, 3), (4, 4), 3, "绿色"),   # 右下角染绿色
    ]
    
    print("画布大小: 5x5")
    print("染色操作:")
    
    for (r1, c1), (r2, c2), value, color in colors:
        print(f"  区域 ({r1},{c1}) 到 ({r2},{c2}): {color} (值={value})")
        da2d.region_add(r1, c1, r2, c2, value)
    
    result = da2d.to_matrix()
    print("最终画布状态:")
    for row in result:
        print([int(x) if x == int(x) else x for x in row])
    
    print()


def example_moving_window_sum():
    """滑动窗口求和示例"""
    print("=" * 50)
    print("滑动窗口求和示例")
    print("=" * 50)
    
    arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    ps = PrefixSum(arr)
    window_size = 3
    
    print(f"数组: {arr}")
    print(f"窗口大小: {window_size}")
    
    window_sums = []
    for i in range(len(arr) - window_size + 1):
        window_sum = ps.range_sum(i, i + window_size - 1)
        window_sums.append(window_sum)
        print(f"窗口 [{i}, {i + window_size - 1}]: 和={window_sum}")
    
    print(f"所有窗口和: {window_sums}")
    
    print()


def example_competition_problem():
    """竞赛题目示例"""
    print("=" * 50)
    print("竞赛题目示例")
    print("=" * 50)
    
    # 问题：给一个数组，进行多次区间加操作后，输出最终数组
    arr = [0, 0, 0, 0, 0]
    operations = [
        (0, 2, 1),
        (1, 3, 2),
        (2, 4, 3),
    ]
    
    print(f"初始数组: {arr}")
    print("操作:")
    for left, right, val in operations:
        print(f"  区间 [{left}, {right}] 加 {val}")
    
    # 使用差分数组高效处理
    da = DifferenceArray(arr)
    for left, right, val in operations:
        da.range_add(left, right, val)
    
    result = da.to_array()
    print(f"最终数组: {result}")
    
    # 验证结果
    expected = [1, 3, 6, 5, 3]  # 手动计算验证
    print(f"验证: {expected}")
    print(f"结果正确: {result == expected}")
    
    print()


def example_matrix_operations():
    """矩阵批量操作示例"""
    print("=" * 50)
    print("矩阵批量操作示例")
    print("=" * 50)
    
    # 初始化一个 3x4 矩阵
    matrix = [
        [10, 20, 30, 40],
        [50, 60, 70, 80],
        [90, 100, 110, 120]
    ]
    
    da2d = DifferenceArray2D(matrix)
    
    print("原始矩阵:")
    for row in matrix:
        print(row)
    
    # 执行多个区域加操作
    print("\n操作:")
    print("  整个矩阵加 5")
    da2d.region_add(0, 0, 2, 3, 5)
    
    print("  第一行减 10")
    da2d.region_add(0, 0, 0, 3, -10)
    
    print("  最后一个元素加 100")
    da2d.point_add(2, 3, 100)
    
    result = da2d.to_matrix()
    print("\n最终矩阵:")
    for row in result:
        print(row)
    
    print()


def example_statistics():
    """统计分析示例"""
    print("=" * 50)
    print("统计分析示例")
    print("=" * 50)
    
    # 每日销售数据
    sales = [120, 150, 180, 200, 165, 190, 220]
    days = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    
    ps = PrefixSum(sales)
    
    print(f"每日销售: {sales}")
    print(f"总销售额: {ps.total()}")
    print(f"平均每日: {ps.total() / len(sales):.1f}")
    
    # 计算工作日和周末销售额
    weekday_sum = ps.range_sum(0, 4)  # 周一到周五
    weekend_sum = ps.range_sum(5, 6)  # 周六周日
    
    print(f"工作日销售: {weekday_sum} (平均 {weekday_sum/5:.1f})")
    print(f"周末销售: {weekend_sum} (平均 {weekend_sum/2:.1f})")
    
    # 计算增长率
    print("\n日增长率:")
    for i in range(1, len(sales)):
        growth = (ps.range_sum(i, i) - ps.range_sum(i-1, i-1)) / ps.range_sum(i-1, i-1) * 100
        print(f"  {days[i-1]} -> {days[i]}: {growth:.1f}%")
    
    print()


def main():
    """运行所有示例"""
    example_prefix_sum()
    example_prefix_sum_2d()
    example_difference_array()
    example_difference_array_2d()
    example_moving_window_sum()
    example_competition_problem()
    example_matrix_operations()
    example_statistics()
    
    print("所有示例完成！")


if __name__ == '__main__':
    main()