#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sparse Table 高级示例
===================

展示稀疏表的高级用法和实际应用场景。

作者: AllToolkit 自动化生成
日期: 2026-05-26
"""

import sys
import os
import time
import random

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    SparseTable, SparseTable2D, DisjointSparseTable,
    OperationType, batch_queries
)


def example_2d_sparse_table():
    """二维稀疏表示例"""
    print("=== 二维稀疏表示例 ===")
    
    matrix = [
        [1, 2, 3, 4, 5],
        [6, 7, 8, 9, 10],
        [11, 12, 13, 14, 15],
        [16, 17, 18, 19, 20],
        [21, 22, 23, 24, 25]
    ]
    
    st_max = SparseTable2D(matrix, OperationType.MAX)
    st_min = SparseTable2D(matrix, OperationType.MIN)
    
    print("矩阵:")
    for row in matrix:
        print(f"  {row}")
    
    print(f"\n子矩阵 [0,0] 到 [2,2] 的最大值: {st_max.query(0, 0, 2, 2)}")
    print(f"子矩阵 [0,0] 到 [2,2] 的最小值: {st_min.query(0, 0, 2, 2)}")
    print(f"子矩阵 [1,1] 到 [3,3] 的最大值: {st_max.query(1, 1, 3, 3)}")
    print(f"整个矩阵的最大值: {st_max.query(0, 0, 4, 4)}")
    print()


def example_disjoint_sparse_table():
    """不相交稀疏表示例（支持求和）"""
    print("=== 不相交稀疏表示例（支持求和）===")
    
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    st = DisjointSparseTable(data, lambda a, b: a + b, 0)
    
    print(f"数据: {data}")
    print(f"区间和 [0, 9]: {st.query(0, 9)}")
    print(f"区间和 [3, 7]: {st.query(3, 7)}")
    print(f"区间和 [0, 4]: {st.query(0, 4)}")
    print()
    
    # 乘积示例
    st_product = DisjointSparseTable(data, lambda a, b: a * b, 1)
    print(f"区间乘积 [0, 4]: {st_product.query(0, 4)}")
    print()


def example_lca_simulation():
    """模拟 LCA（最近公共祖先）问题"""
    print("=== LCA 问题模拟 ===")
    
    # 使用 RMQ 解决 LCA 问题的简化示例
    # 在实际应用中，这会配合欧拉游走使用
    
    # 假设树节点的高度序列（欧拉游走）
    euler_tour = [0, 1, 2, 1, 3, 4, 3, 1, 0]  # 节点高度
    st = SparseTable(euler_tour, OperationType.MIN)
    
    print(f"欧拉游走高度: {euler_tour}")
    
    # 查找区间 [2, 6] 的最小高度
    min_height_pos = 2
    max_height_pos = 6
    lca_height = st.query(min_height_pos, max_height_pos)
    print(f"区间 [{min_height_pos}, {max_height_pos}] 的 LCA 高度: {lca_height}")
    print()


def example_stock_analysis():
    """股票分析示例"""
    print("=== 股票价格分析示例 ===")
    
    # 模拟30天股票价格
    prices = [100, 102, 98, 105, 110, 108, 112, 115, 110, 108,
              105, 103, 107, 111, 118, 120, 115, 110, 108, 112,
              116, 119, 122, 118, 115, 112, 116, 120, 118, 125]
    
    st_min = SparseTable(prices, OperationType.MIN)
    st_max = SparseTable(prices, OperationType.MAX)
    
    print(f"30天股票价格: {prices}")
    print(f"\n分析结果:")
    print(f"  全月最低价: ${st_min.query(0, 29)}")
    print(f"  全月最高价: ${st_max.query(0, 29)}")
    
    # 分析各周
    weeks = [(0, 6), (7, 13), (14, 20), (21, 29)]
    for i, (start, end) in enumerate(weeks, 1):
        print(f"  第{i}周: 最低 ${st_min.query(start, end)}, 最高 ${st_max.query(start, end)}")
    
    # 价格波动分析
    def analyze_volatility(prices, st_min, st_max, start, end):
        low = st_min.query(start, end)
        high = st_max.query(start, end)
        return high - low
    
    print(f"\n波动幅度:")
    for i, (start, end) in enumerate(weeks, 1):
        volatility = analyze_volatility(prices, st_min, st_max, start, end)
        print(f"  第{i}周波动: ${volatility}")
    print()


def example_performance_comparison():
    """性能比较示例"""
    print("=== 性能比较示例 ===")
    
    # 生成大数据
    n = 100000
    data = [random.randint(1, 1000000) for _ in range(n)]
    queries = [(random.randint(0, n-1), None) for _ in range(10000)]
    
    # 确保左边界小于右边界
    for i in range(len(queries)):
        left = queries[i][0]
        right = random.randint(left, n-1)
        queries[i] = (left, right)
    
    # 构建稀疏表
    print(f"构建稀疏表 (n={n})...")
    start = time.time()
    st = SparseTable(data, OperationType.MIN)
    build_time = time.time() - start
    print(f"  构建时间: {build_time:.4f}s")
    
    # 稀疏表查询
    print(f"执行 {len(queries)} 次查询...")
    start = time.time()
    for left, right in queries:
        st.query(left, right)
    st_time = time.time() - start
    print(f"  稀疏表查询时间: {st_time:.4f}s")
    
    # 朴素方法对比（少量查询）
    sample_queries = queries[:100]
    print(f"执行 100 次朴素查询对比...")
    start = time.time()
    for left, right in sample_queries:
        min(data[left:right+1])
    naive_time = time.time() - start
    print(f"  朴素查询时间: {naive_time:.4f}s")
    
    print(f"\n稀疏表查询速度提升: {naive_time / st_time * 100:.1f}x")
    print()


def example_temperature_analysis():
    """温度数据分析示例"""
    print("=== 温度数据分析示例 ===")
    
    # 模拟24小时温度数据
    temps = [
        18, 17, 16, 15, 14, 14, 15, 17,  # 0-7时
        20, 23, 26, 28, 30, 31, 30, 28,  # 8-15时
        25, 23, 21, 20, 19, 18, 18, 17   # 16-23时
    ]
    
    st_min = SparseTable(temps, OperationType.MIN)
    st_max = SparseTable(temps, OperationType.MAX)
    
    print("24小时温度数据:")
    for i in range(0, 24, 6):
        print(f"  {i:02d}:00-{i+5:02d}:00: {temps[i:i+6]}")
    
    print(f"\n分析结果:")
    print(f"  全天最低温度: {st_min.query(0, 23)}°C (凌晨)")
    print(f"  全天最高温度: {st_max.query(0, 23)}°C (下午)")
    
    # 各时段分析
    periods = [
        ("凌晨 (0-5时)", 0, 5),
        ("早晨 (6-11时)", 6, 11),
        ("下午 (12-17时)", 12, 17),
        ("晚上 (18-23时)", 18, 23)
    ]
    
    print(f"\n各时段分析:")
    for name, start, end in periods:
        low = st_min.query(start, end)
        high = st_max.query(start, end)
        print(f"  {name}: 最低 {low}°C, 最高 {high}°C, 温差 {high-low}°C")
    print()


def main():
    """运行所有高级示例"""
    example_2d_sparse_table()
    example_disjoint_sparse_table()
    example_lca_simulation()
    example_stock_analysis()
    example_performance_comparison()
    example_temperature_analysis()
    
    print("所有高级示例运行完成!")


if __name__ == "__main__":
    main()