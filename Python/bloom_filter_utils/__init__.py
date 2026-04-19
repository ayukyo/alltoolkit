"""
布隆过滤器工具集 (Bloom Filter Utils)

高效的 probabilistic 数据结构，用于元素存在性检测。

主要组件：
- BloomFilter: 标准布隆过滤器
- CountingBloomFilter: 计数布隆过滤器（支持删除）
- ScalableBloomFilter: 可扩展布隆过滤器（自动扩容）
- DeletableBloomFilter: 可删除布隆过滤器（精确删除）
- BloomFilterBuilder: 流畅 API 构建器

便捷函数：
- create_bloom_filter: 快速创建
- create_optimal_bloom_filter: 最优参数创建
- optimal_num_bits: 计算最优位数组大小
- optimal_num_hashes: 计算最优哈希函数数量
- estimate_false_positive_rate: 估算假阳性率

使用示例：
    from bloom_filter_utils import BloomFilter
    
    bf = BloomFilter(capacity=10000, error_rate=0.01)
    bf.add("hello")
    print("hello" in bf)  # True
    print("world" in bf)  # False
"""

from .bloom_filter import (
    BloomFilter,
    CountingBloomFilter,
    ScalableBloomFilter,
    DeletableBloomFilter,
    BloomFilterBuilder,
    BloomFilterStats,
    optimal_num_bits,
    optimal_num_hashes,
    estimate_false_positive_rate,
    create_bloom_filter,
    create_optimal_bloom_filter,
)

__all__ = [
    "BloomFilter",
    "CountingBloomFilter",
    "ScalableBloomFilter",
    "DeletableBloomFilter",
    "BloomFilterBuilder",
    "BloomFilterStats",
    "optimal_num_bits",
    "optimal_num_hashes",
    "estimate_false_positive_rate",
    "create_bloom_filter",
    "create_optimal_bloom_filter",
]

__version__ = "1.0.0"
__author__ = "AllToolkit"