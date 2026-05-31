#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Wavelet Tree Utils 使用示例

作者: AllToolkit
日期: 2026-06-01
"""

import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    WaveletTree,
    WaveletTreeCompact,
    create_wavelet_tree,
    wavelet_rank,
    wavelet_quantile,
    wavelet_range_count,
)


def example_basic():
    """基本使用示例"""
    print("=" * 50)
    print("基本使用示例")
    print("=" * 50)
    
    # 创建小波树
    data = [1, 2, 1, 3, 2, 1, 4, 2]
    wt = WaveletTree(data, min_val=1, max_val=4)
    
    print(f"数据: {data}")
    print(f"小波树: {wt}")
    print(f"大小: {wt.size}")
    print()
    
    # 统计元素出现次数
    print("元素出现次数:")
    for val in range(1, 5):
        count = wt.rank(val, 0, len(data) - 1)
        print(f"  值 {val}: {count} 次")
    print()
    
    # 获取第 k 小的值
    print("第 k 小的值:")
    for k in range(1, 9):
        val = wt.quantize(0, len(data) - 1, k)
        print(f"  第 {k} 小的值: {val}")
    print()


def example_string_indexing():
    """字符串索引示例"""
    print("=" * 50)
    print("字符串索引示例")
    print("=" * 50)
    
    # 将字符串转换为 ASCII 码
    text = "abracadabra"
    data = [ord(c) for c in text]
    
    print(f"文本: {text}")
    print(f"ASCII 码: {data}")
    print()
    
    min_val = min(data)
    max_val = max(data)
    wt = WaveletTree(data, min_val=min_val, max_val=max_val)
    
    # 统计字符出现次数
    print("字符出现次数:")
    for c in set(text):
        val = ord(c)
        count = wt.rank(val, 0, len(data) - 1)
        print(f"  字符 '{c}': {count} 次")
    print()


def example_range_queries():
    """范围查询示例"""
    print("=" * 50)
    print("范围查询示例")
    print("=" * 50)
    
    # 模拟日志数据：[错误级别(1-5), 时间戳, ...]
    logs = [
        1, 3, 2, 4, 1, 5, 2, 3, 1, 4,
        2, 1, 3, 4, 5, 1, 2, 3, 4, 2
    ]
    
    wt = create_wavelet_tree(logs)
    
    print(f"日志数据 (前10条): {logs[:10]}...")
    print()
    
    # 范围频率查询
    print("范围频率查询:")
    count_1_2 = wt.range_count(0, 9, 1, 2)
    count_3_5 = wt.range_count(0, 9, 3, 5)
    print(f"  [0, 9] 区间内，错误级别 1-2 的日志数: {count_1_2}")
    print(f"  [0, 9] 区间内，错误级别 3-5 的日志数: {count_3_5}")
    print()
    
    # 分位数查询
    print("分位数查询:")
    median = wt.quantile(0, 9, 5)
    print(f"  [0, 9] 区间内，中位数错误级别: {median}")
    print()


def example_compact_version():
    """紧凑版小波树示例"""
    print("=" * 50)
    print("紧凑版小波树示例")
    print("=" * 50)
    
    data = [1, 2, 1, 3, 2, 1, 4, 2]
    wt = WaveletTreeCompact(data, min_val=1, max_val=4)
    
    print(f"数据: {data}")
    print(f"紧凑版小波树: {wt}")
    print()
    
    # 统计元素出现次数
    print("元素出现次数:")
    for val in range(1, 5):
        count = wt.rank(val, 0, len(data) - 1)
        print(f"  值 {val}: {count} 次")
    print()


def example_dna_sequence():
    """DNA 序列分析示例"""
    print("=" * 50)
    print("DNA 序列分析示例")
    print("=" * 50)
    
    # DNA 碱基编码：A=0, C=1, G=2, T=3
    dna_text = "ACGTACGTACGT"
    dna_map = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
    data = [dna_map[c] for c in dna_text]
    
    print(f"DNA 序列: {dna_text}")
    print(f"编码: {data}")
    print()
    
    wt = create_wavelet_tree(data)
    
    # 统计各碱基出现次数
    reverse_map = {0: 'A', 1: 'C', 2: 'G', 3: 'T'}
    print("碱基出现次数:")
    for val in range(4):
        count = wt.rank(val, 0, len(data) - 1)
        print(f"  碱基 '{reverse_map[val]}': {count} 次")
    print()


def example_streaming_stats():
    """流式统计示例"""
    print("=" * 50)
    print("流式统计示例（模拟实时数据）")
    print("=" * 50)
    
    # 模拟传感器数据（温度值 15-35）
    import random
    random.seed(42)
    
    sensor_data = [random.randint(15, 35) for _ in range(20)]
    wt = create_wavelet_tree(sensor_data)
    
    print(f"传感器数据: {sensor_data}")
    print()
    
    # 实时统计
    print("统计分析:")
    print(f"  温度范围 20-25 的数据点: {wt.range_count(0, 19, 20, 25)}")
    print(f"  温度范围 30-35 的数据点: {wt.range_count(0, 19, 30, 35)}")
    print(f"  中位数温度: {wt.quantile(0, 19, 10)}")
    print()


def example_api_usage():
    """API 使用示例"""
    print("=" * 50)
    print("API 使用示例")
    print("=" * 50)
    
    data = [5, 2, 8, 1, 9, 3, 7, 4, 6, 10]
    wt = create_wavelet_tree(data)
    
    print(f"数据: {data}")
    print()
    
    # 使用便捷函数
    print("使用便捷函数:")
    print(f"  wavelet_rank: 值为 5 的数量 = {wavelet_rank(wt, 5, 0, 9)}")
    print(f"  wavelet_quantile: 第 5 小的值 = {wavelet_quantile(wt, 0, 9, 5)}")
    print(f"  wavelet_range_count: [3,7] 范围的数量 = {wavelet_range_count(wt, 0, 9, 3, 7)}")
    print()


def main():
    """运行所有示例"""
    example_basic()
    example_string_indexing()
    example_range_queries()
    example_compact_version()
    example_dna_sequence()
    example_streaming_stats()
    example_api_usage()


if __name__ == "__main__":
    main()