#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sparse Table 基础示例
===================

展示稀疏表的基本使用方法。

作者: AllToolkit 自动化生成
日期: 2026-05-26
"""

import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    SparseTable, OperationType, SparseTableBuilder,
    build_min_sparse_table, build_max_sparse_table,
    range_min, range_max, batch_queries
)


def example_basic_min():
    """基本最小值查询示例"""
    print("=== 最小值查询示例 ===")
    
    data = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
    st = SparseTable(data, OperationType.MIN)
    
    print(f"数据: {data}")
    print(f"整个数组最小值: {st.query(0, len(data) - 1)}")
    print(f"区间 [2, 5] 最小值: {st.query(2, 5)}")
    print(f"区间 [0, 3] 最小值: {st.query(0, 3)}")
    print()


def example_basic_max():
    """基本最大值查询示例"""
    print("=== 最大值查询示例 ===")
    
    data = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
    st = SparseTable(data, OperationType.MAX)
    
    print(f"数据: {data}")
    print(f"整个数组最大值: {st.query(0, len(data) - 1)}")
    print(f"区间 [2, 5] 最大值: {st.query(2, 5)}")
    print()


def example_gcd():
    """GCD 查询示例"""
    print("=== GCD 查询示例 ===")
    
    data = [12, 18, 24, 36, 60, 90]
    st = SparseTable(data, OperationType.GCD)
    
    print(f"数据: {data}")
    print(f"整个数组 GCD: {st.query(0, len(data) - 1)}")
    print(f"区间 [0, 2] GCD (12, 18, 24): {st.query(0, 2)}")
    print(f"区间 [2, 4] GCD (24, 36, 60): {st.query(2, 4)}")
    print()


def example_bitwise():
    """位运算示例"""
    print("=== 位运算示例 ===")
    
    # AND 运算
    data_and = [15, 7, 3, 1]
    st_and = SparseTable(data_and, OperationType.AND)
    print(f"AND 数据: {data_and}")
    print(f"区间 AND [0, 3]: {st_and.query(0, 3)}")
    
    # OR 运算
    data_or = [1, 2, 4, 8]
    st_or = SparseTable(data_or, OperationType.OR)
    print(f"OR 数据: {data_or}")
    print(f"区间 OR [0, 3]: {st_or.query(0, 3)}")
    
    # XOR 运算
    data_xor = [1, 2, 3, 4]
    st_xor = SparseTable(data_xor, OperationType.XOR)
    print(f"XOR 数据: {data_xor}")
    print(f"区间 XOR [0, 3]: {st_xor.query(0, 3)}")
    print()


def example_builder():
    """构建器模式示例"""
    print("=== 构建器模式示例 ===")
    
    st = (SparseTableBuilder()
          .with_data([5, 2, 8, 1, 9, 3])
          .for_min()
          .build())
    
    print(f"最小值: {st.query(0, 5)}")
    
    st_max = (SparseTableBuilder()
              .with_data([5, 2, 8, 1, 9, 3])
              .for_max()
              .build())
    
    print(f"最大值: {st_max.query(0, 5)}")
    print()


def example_convenience():
    """便捷函数示例"""
    print("=== 便捷函数示例 ===")
    
    data = [3, 1, 4, 1, 5, 9, 2, 6]
    
    print(f"数据: {data}")
    print(f"range_min(0, 7): {range_min(data, 0, 7)}")
    print(f"range_max(0, 7): {range_max(data, 0, 7)}")
    
    # 快速构建
    st = build_min_sparse_table(data)
    print(f"build_min_sparse_table.query(2, 5): {st.query(2, 5)}")
    print()


def example_batch():
    """批量查询示例"""
    print("=== 批量查询示例 ===")
    
    data = [3, 1, 4, 1, 5, 9, 2, 6]
    queries = [(0, 3), (2, 5), (4, 7), (1, 6)]
    
    print(f"数据: {data}")
    print(f"查询: {queries}")
    
    results_min = batch_queries(data, queries, OperationType.MIN)
    print(f"最小值结果: {results_min}")
    
    results_max = batch_queries(data, queries, OperationType.MAX)
    print(f"最大值结果: {results_max}")
    print()


def main():
    """运行所有示例"""
    example_basic_min()
    example_basic_max()
    example_gcd()
    example_bitwise()
    example_builder()
    example_convenience()
    example_batch()
    
    print("所有示例运行完成!")


if __name__ == "__main__":
    main()