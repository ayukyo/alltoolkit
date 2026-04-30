"""
Bloom Filter Utils 测试套件

测试覆盖：
- 哈希函数
- BitArray 基础操作
- 标准 BloomFilter
- 可扩展 ScalableBloomFilter
- 计数 CountingBloomFilter
- 序列化/反序列化
- 边界情况
"""

import unittest
import tempfile
import os
import math
import sys
from typing import List

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入被测试模块
from bloom_filter_utils.bloom_filter_utils import (
    murmurhash3_x86_32,
    fnv_hash_32,
    djb2_hash,
    sha256_hash,
    HASH_FUNCTIONS,
    optimal_size,
    false_positive_rate,
    BitArray,
    BloomFilter,
    BloomFilterStats,
    ScalableBloomFilter,
    ScalableBloomFilterConfig,
    CountingBloomFilter,
    create_optimal_filter,
    from_iterable,
    estimate_memory_usage,
    compare_hash_functions,
    BloomFilterBuilder,
)


# ============================================================================
# 哈希函数测试
# ============================================================================

class TestHashFunctions(unittest.TestCase):
    """测试哈希函数实现"""
    
    def test_murmurhash_deterministic(self):
        """测试 MurmurHash 确定性"""
        data = b"hello world"
        h1 = murmurhash3_x86_32(data)
        h2 = murmurhash3_x86_32(data)
        self.assertEqual(h1, h2)
    
    def test_murmurhash_different_inputs(self):
        """测试不同输入产生不同哈希"""
        h1 = murmurhash3_x86_32(b"hello")
        h2 = murmurhash3_x86_32(b"world")
        self.assertNotEqual(h1, h2)
    
    def test_murmurhash_seed_effect(self):
        """测试种子影响哈希结果"""
        data = b"test data"
        h1 = murmurhash3_x86_32(data, seed=0)
        h2 = murmurhash3_x86_32(data, seed=1)
        self.assertNotEqual(h1, h2)
    
    def test_murmurhash_empty_input(self):
        """测试空输入"""
        h = murmurhash3_x86_32(b"")
        self.assertIsInstance(h, int)
        self.assertGreaterEqual(h, 0)
    
    def test_fnv_hash_deterministic(self):
        """测试 FNV 哈希确定性"""
        data = b"hello world"
        h1 = fnv_hash_32(data)
        h2 = fnv_hash_32(data)
        self.assertEqual(h1, h2)
    
    def test_fnv_hash_different_inputs(self):
        """测试 FNV 不同输入"""
        h1 = fnv_hash_32(b"a")
        h2 = fnv_hash_32(b"b")
        self.assertNotEqual(h1, h2)
    
    def test_djb2_hash_deterministic(self):
        """测试 DJB2 哈希确定性"""
        data = b"hello world"
        h1 = djb2_hash(data)
        h2 = djb2_hash(data)
        self.assertEqual(h1, h2)
    
    def test_sha256_hash_deterministic(self):
        """测试 SHA256 哈希确定性"""
        data = b"hello world"
        h1 = sha256_hash(data)
        h2 = sha256_hash(data)
        self.assertEqual(h1, h2)
    
    def test_hash_functions_registry(self):
        """测试哈希函数注册表"""
        self.assertIn('murmur', HASH_FUNCTIONS)
        self.assertIn('fnv', HASH_FUNCTIONS)
        self.assertIn('djb2', HASH_FUNCTIONS)
        self.assertIn('sha256', HASH_FUNCTIONS)
        self.assertEqual(len(HASH_FUNCTIONS), 4)
    
    def test_hash_distribution(self):
        """测试哈希分布均匀性（简单检查）"""
        # 生成多个哈希值，检查是否分布合理
        hashes = set()
        for i in range(1000):
            h = murmurhash3_x86_32(f"item_{i}".encode())
            hashes.add(h)
        
        # 1000 个不同输入应该产生大量不同的哈希值
        self.assertGreater(len(hashes), 990)
    
    def test_hash_32bit_range(self):
        """测试哈希值在 32 位范围内"""
        for name, func in HASH_FUNCTIONS.items():
            for data in [b"", b"a", b"hello", b"x" * 1000]:
                h = func(data)
                self.assertGreaterEqual(h, 0)
                self.assertLess(h, 2**32, f"{name} hash out of 32-bit range")


# ============================================================================
# 工具函数测试
# ============================================================================

class TestUtilityFunctions(unittest.TestCase):
    """测试工具函数"""
    
    def test_optimal_size_basic(self):
        """测试最优大小计算"""
        m, k = optimal_size(1000, 0.01)
        self.assertGreater(m, 0)
        self.assertGreater(k, 0)
    
    def test_optimal_size_larger_n(self):
        """测试更大的元素数量"""
        m1, k1 = optimal_size(1000, 0.01)
        m2, k2 = optimal_size(10000, 0.01)
        self.assertGreater(m2, m1)
    
    def test_optimal_size_smaller_fp(self):
        """测试更小的假阳性率需要更多空间"""
        m1, k1 = optimal_size(1000, 0.1)
        m2, k2 = optimal_size(1000, 0.001)
        self.assertGreater(m2, m1)
        self.assertGreater(k2, k1)
    
    def test_optimal_size_invalid_n(self):
        """测试无效的元素数量"""
        with self.assertRaises(ValueError):
            optimal_size(0, 0.01)
        with self.assertRaises(ValueError):
            optimal_size(-1, 0.01)
    
    def test_optimal_size_invalid_fp(self):
        """测试无效的假阳性率"""
        with self.assertRaises(ValueError):
            optimal_size(1000, 0)
        with self.assertRaises(ValueError):
            optimal_size(1000, 1)
        with self.assertRaises(ValueError):
            optimal_size(1000, -0.01)
        with self.assertRaises(ValueError):
            optimal_size(1000, 1.01)
    
    def test_false_positive_rate(self):
        """测试假阳性率计算"""
        # 空 filter 应该有 0 假阳性率
        fp = false_positive_rate(0, 1000, 5)
        self.assertEqual(fp, 0)
        
        # 正常情况
        fp = false_positive_rate(100, 1000, 5)
        self.assertGreater(fp, 0)
        self.assertLess(fp, 1)
    
    def test_estimate_memory_usage(self):
        """测试内存使用估算"""
        result = estimate_memory_usage(1000000, 0.01)
        
        self.assertIn('bits_needed', result)
        self.assertIn('bytes_needed', result)
        self.assertIn('kilobytes', result)
        self.assertIn('megabytes', result)
        self.assertIn('hash_functions', result)
        self.assertIn('bits_per_element', result)
        
        self.assertGreater(result['bits_needed'], 0)
        self.assertGreater(result['bytes_needed'], 0)


# ============================================================================
# BitArray 测试
# ============================================================================

class TestBitArray(unittest.TestCase):
    """测试 BitArray 实现"""
    
    def test_init(self):
        """测试初始化"""
        ba = BitArray(100)
        self.assertEqual(len(ba), 100)
    
    def test_init_zero_size(self):
        """测试零大小初始化"""
        ba = BitArray(0)
        self.assertEqual(len(ba), 0)
    
    def test_init_negative_size(self):
        """测试负大小初始化"""
        with self.assertRaises(ValueError):
            BitArray(-1)
    
    def test_set_and_get(self):
        """测试设置和获取"""
        ba = BitArray(100)
        
        # 初始全为 0
        self.assertFalse(ba[0])
        self.assertFalse(ba[50])
        self.assertFalse(ba[99])
        
        # 设置位
        ba[0] = True
        ba[50] = True
        ba[99] = True
        
        self.assertTrue(ba[0])
        self.assertTrue(ba[50])
        self.assertTrue(ba[99])
        self.assertFalse(ba[1])
        self.assertFalse(ba[49])
    
    def test_set_clear_toggle(self):
        """测试 set/clear/toggle 方法"""
        ba = BitArray(10)
        
        ba.set(5)
        self.assertTrue(ba[5])
        
        ba.clear(5)
        self.assertFalse(ba[5])
        
        result = ba.toggle(5)
        self.assertTrue(result)
        self.assertTrue(ba[5])
        
        result = ba.toggle(5)
        self.assertFalse(result)
        self.assertFalse(ba[5])
    
    def test_index_bounds(self):
        """测试索引边界"""
        ba = BitArray(10)
        
        with self.assertRaises(IndexError):
            _ = ba[-1]
        
        with self.assertRaises(IndexError):
            _ = ba[10]
        
        with self.assertRaises(IndexError):
            ba[-1] = True
        
        with self.assertRaises(IndexError):
            ba[10] = True
    
    def test_count_set_bits(self):
        """测试位数统计"""
        ba = BitArray(100)
        self.assertEqual(ba.count_set_bits(), 0)
        
        ba.set(0)
        ba.set(10)
        ba.set(50)
        ba.set(99)
        self.assertEqual(ba.count_set_bits(), 4)
    
    def test_clear_all(self):
        """测试清除所有位"""
        ba = BitArray(100)
        for i in range(0, 100, 2):
            ba.set(i)
        
        self.assertGreater(ba.count_set_bits(), 0)
        ba.clear_all()
        self.assertEqual(ba.count_set_bits(), 0)
    
    def test_set_all(self):
        """测试设置所有位"""
        ba = BitArray(100)
        ba.set_all()
        self.assertEqual(ba.count_set_bits(), 100)
    
    def test_to_bytes_and_from_bytes(self):
        """测试序列化和反序列化"""
        ba = BitArray(100)
        ba.set(0)
        ba.set(50)
        ba.set(99)
        
        data = ba.to_bytes()
        self.assertIsInstance(data, bytes)
        
        ba2 = BitArray.from_bytes(data, 100)
        self.assertTrue(ba2[0])
        self.assertTrue(ba2[50])
        self.assertTrue(ba2[99])
        self.assertFalse(ba2[1])
    
    def test_large_size(self):
        """测试大尺寸"""
        ba = BitArray(100000)
        ba.set(0)
        ba.set(99999)
        self.assertTrue(ba[0])
        self.assertTrue(ba[99999])
        self.assertEqual(ba.count_set_bits(), 2)


# ============================================================================
# BloomFilter 测试
# ============================================================================

class TestBloomFilter(unittest.TestCase):
    """测试标准布隆过滤器"""
    
    def test_init_default(self):
        """测试默认初始化"""
        bf = BloomFilter()
        self.assertGreater(bf.size, 0)
        self.assertGreater(bf.hash_count, 0)
        self.assertTrue(bf.is_empty)
    
    def test_init_custom_params(self):
        """测试自定义参数初始化"""
        bf = BloomFilter(expected_elements=1000, false_positive_rate=0.001)
        self.assertGreater(bf.size, 0)
        self.assertGreater(bf.hash_count, 0)
    
    def test_init_invalid_params(self):
        """测试无效参数"""
        with self.assertRaises(ValueError):
            BloomFilter(expected_elements=0)
        
        with self.assertRaises(ValueError):
            BloomFilter(expected_elements=-1)
        
        with self.assertRaises(ValueError):
            BloomFilter(false_positive_rate=0)
        
        with self.assertRaises(ValueError):
            BloomFilter(false_positive_rate=1)
        
        with self.assertRaises(ValueError):
            BloomFilter(hash_func='unknown')
    
    def test_add_and_contains(self):
        """测试添加和查询"""
        bf = BloomFilter(expected_elements=100, false_positive_rate=0.01)
        
        bf.add("hello")
        bf.add("world")
        
        self.assertIn("hello", bf)
        self.assertIn("world", bf)
        self.assertNotIn("foo", bf)
    
    def test_add_bytes(self):
        """测试添加字节"""
        bf = BloomFilter()
        
        bf.add(b"bytes_data")
        self.assertIn(b"bytes_data", bf)
    
    def test_add_numbers(self):
        """测试添加数字"""
        bf = BloomFilter()
        
        bf.add(42)
        bf.add(3.14)
        
        self.assertIn(42, bf)
        self.assertIn(3.14, bf)
    
    def test_might_contain(self):
        """测试 might_contain 方法"""
        bf = BloomFilter()
        bf.add("test")
        
        self.assertTrue(bf.might_contain("test"))
        self.assertFalse(bf.might_contain("nonexistent"))
    
    def test_len(self):
        """测试长度"""
        bf = BloomFilter()
        self.assertEqual(len(bf), 0)
        
        bf.add("a")
        self.assertEqual(len(bf), 1)
        
        bf.add("b")
        self.assertEqual(len(bf), 2)
    
    def test_clear(self):
        """测试清除"""
        bf = BloomFilter()
        bf.add("a")
        bf.add("b")
        
        self.assertEqual(len(bf), 2)
        bf.clear()
        self.assertEqual(len(bf), 0)
        self.assertNotIn("a", bf)
        self.assertNotIn("b", bf)
    
    def test_update(self):
        """测试批量添加"""
        bf = BloomFilter()
        items = ["a", "b", "c", "d", "e"]
        
        bf.update(items)
        
        self.assertEqual(len(bf), 5)
        for item in items:
            self.assertIn(item, bf)
    
    def test_update_chain(self):
        """测试链式调用"""
        bf = BloomFilter()
        result = bf.update(["a", "b"]).update(["c", "d"])
        
        self.assertIs(result, bf)
        self.assertEqual(len(bf), 4)
    
    def test_false_positive_rate(self):
        """测试假阳性率（统计测试）"""
        bf = BloomFilter(expected_elements=1000, false_positive_rate=0.01)
        
        # 添加 1000 个元素
        for i in range(1000):
            bf.add(f"item_{i}")
        
        # 测试不在集合中的元素
        false_positives = 0
        total_tests = 10000
        
        for i in range(1000, 1000 + total_tests):
            if f"item_{i}" in bf:
                false_positives += 1
        
        actual_fp_rate = false_positives / total_tests
        
        # 假阳性率应该在设计值的合理范围内（允许一些偏差）
        self.assertLess(actual_fp_rate, 0.05)  # 应该小于 5%
    
    def test_no_false_negatives(self):
        """测试无假阴性"""
        bf = BloomFilter(expected_elements=100, false_positive_rate=0.01)
        
        items = [f"item_{i}" for i in range(100)]
        for item in items:
            bf.add(item)
        
        # 所有添加的元素必须存在
        for item in items:
            self.assertIn(item, bf)
    
    def test_get_stats(self):
        """测试统计信息"""
        bf = BloomFilter()
        for i in range(100):
            bf.add(f"item_{i}")
        
        stats = bf.get_stats()
        
        self.assertIsInstance(stats, BloomFilterStats)
        self.assertEqual(stats.size, bf.size)
        self.assertEqual(stats.hash_count, bf.hash_count)
        self.assertEqual(stats.elements_added, 100)
        self.assertGreater(stats.set_bits, 0)
        self.assertGreater(stats.fill_ratio, 0)
        self.assertGreater(stats.estimated_fp_rate, 0)
        
        # 测试字典转换
        stats_dict = stats.to_dict()
        self.assertIn('size', stats_dict)
        self.assertIn('elements_added', stats_dict)
    
    def test_union(self):
        """测试并集操作"""
        bf1 = BloomFilter(expected_elements=100, false_positive_rate=0.01, hash_func='murmur')
        bf2 = BloomFilter(expected_elements=100, false_positive_rate=0.01, hash_func='murmur')
        
        bf1.add("a")
        bf1.add("b")
        
        bf2.add("b")
        bf2.add("c")
        
        union = bf1.union(bf2)
        
        self.assertIn("a", union)
        self.assertIn("b", union)
        self.assertIn("c", union)
    
    def test_union_incompatible(self):
        """测试不兼容过滤器的并集"""
        bf1 = BloomFilter(expected_elements=100, false_positive_rate=0.01)
        bf2 = BloomFilter(expected_elements=200, false_positive_rate=0.01)
        
        with self.assertRaises(ValueError):
            bf1.union(bf2)
    
    def test_intersect(self):
        """测试交集操作"""
        bf1 = BloomFilter(expected_elements=100, false_positive_rate=0.01, hash_func='murmur')
        bf2 = BloomFilter(expected_elements=100, false_positive_rate=0.01, hash_func='murmur')
        
        bf1.add("a")
        bf1.add("b")
        
        bf2.add("b")
        bf2.add("c")
        
        intersection = bf1.intersect(bf2)
        
        # 交集应该包含 "b"（两个都有的）
        self.assertIn("b", intersection)
    
    def test_serialization(self):
        """测试序列化和反序列化"""
        bf = BloomFilter(expected_elements=100, false_positive_rate=0.01)
        for i in range(50):
            bf.add(f"item_{i}")
        
        # 序列化
        data = bf.to_bytes()
        self.assertIsInstance(data, bytes)
        
        # 反序列化
        bf2 = BloomFilter.from_bytes(data)
        
        self.assertEqual(bf.size, bf2.size)
        self.assertEqual(bf.hash_count, bf2.hash_count)
        self.assertEqual(len(bf), len(bf2))
        
        # 验证所有元素都在
        for i in range(50):
            self.assertIn(f"item_{i}", bf2)
    
    def test_save_and_load(self):
        """测试文件保存和加载"""
        bf = BloomFilter(expected_elements=100, false_positive_rate=0.01)
        for i in range(50):
            bf.add(f"item_{i}")
        
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_path = f.name
        
        try:
            bf.save(temp_path)
            bf2 = BloomFilter.load(temp_path)
            
            self.assertEqual(bf.size, bf2.size)
            self.assertEqual(len(bf), len(bf2))
            
            for i in range(50):
                self.assertIn(f"item_{i}", bf2)
        finally:
            os.unlink(temp_path)
    
    def test_different_hash_functions(self):
        """测试不同哈希函数"""
        for hash_name in ['murmur', 'fnv', 'djb2', 'sha256']:
            bf = BloomFilter(hash_func=hash_name)
            bf.add("test")
            self.assertIn("test", bf)
    
    def test_equality(self):
        """测试相等性"""
        bf1 = BloomFilter(expected_elements=100, false_positive_rate=0.01)
        bf2 = BloomFilter(expected_elements=100, false_positive_rate=0.01)
        
        bf1.add("a")
        bf2.add("a")
        
        self.assertEqual(bf1, bf2)
        
        bf2.add("b")
        self.assertNotEqual(bf1, bf2)
    
    def test_repr(self):
        """测试字符串表示"""
        bf = BloomFilter()
        repr_str = repr(bf)
        self.assertIn("BloomFilter", repr_str)
        self.assertIn("size=", repr_str)
        self.assertIn("hash_count=", repr_str)


# ============================================================================
# ScalableBloomFilter 测试
# ============================================================================

class TestScalableBloomFilter(unittest.TestCase):
    """测试可扩展布隆过滤器"""
    
    def test_init_default(self):
        """测试默认初始化"""
        sbf = ScalableBloomFilter()
        self.assertEqual(sbf.filter_count, 1)
        self.assertTrue(sbf.is_empty)
    
    def test_init_custom_config(self):
        """测试自定义配置"""
        config = ScalableBloomFilterConfig(
            initial_capacity=100,
            false_positive_rate=0.001,
            growth_factor=3.0,
        )
        sbf = ScalableBloomFilter(config=config)
        self.assertEqual(sbf.filter_count, 1)
    
    def test_add_and_contains(self):
        """测试添加和查询"""
        sbf = ScalableBloomFilter()
        
        sbf.add("hello")
        sbf.add("world")
        
        self.assertIn("hello", sbf)
        self.assertIn("world", sbf)
        self.assertNotIn("foo", sbf)
    
    def test_automatic_expansion(self):
        """测试自动扩容"""
        config = ScalableBloomFilterConfig(
            initial_capacity=10,
            growth_factor=2.0,
        )
        sbf = ScalableBloomFilter(config=config)
        
        # 添加超过初始容量的元素
        for i in range(100):
            sbf.add(f"item_{i}")
        
        # 应该有多个内部过滤器
        self.assertGreater(sbf.filter_count, 1)
        
        # 所有元素应该可查询
        for i in range(100):
            self.assertIn(f"item_{i}", sbf)
    
    def test_len(self):
        """测试长度"""
        sbf = ScalableBloomFilter(initial_capacity=10)
        
        for i in range(50):
            sbf.add(f"item_{i}")
        
        self.assertEqual(len(sbf), 50)
    
    def test_clear(self):
        """测试清除"""
        sbf = ScalableBloomFilter()
        sbf.add("a")
        sbf.add("b")
        
        sbf.clear()
        
        self.assertEqual(len(sbf), 0)
        self.assertNotIn("a", sbf)
        self.assertNotIn("b", sbf)
    
    def test_get_stats(self):
        """测试统计信息"""
        sbf = ScalableBloomFilter(initial_capacity=10)
        
        for i in range(100):
            sbf.add(f"item_{i}")
        
        stats = sbf.get_stats()
        
        self.assertIn('filter_count', stats)
        self.assertIn('total_elements', stats)
        self.assertIn('total_size_bits', stats)
        self.assertIn('estimated_fp_rate', stats)
        self.assertIn('filters', stats)
        
        self.assertGreater(stats['filter_count'], 1)
        self.assertEqual(stats['total_elements'], 100)
    
    def test_serialization(self):
        """测试序列化和反序列化"""
        sbf = ScalableBloomFilter(initial_capacity=10)
        
        for i in range(100):
            sbf.add(f"item_{i}")
        
        data = sbf.to_bytes()
        self.assertIsInstance(data, bytes)
        
        sbf2 = ScalableBloomFilter.from_bytes(data)
        
        self.assertEqual(sbf.filter_count, sbf2.filter_count)
        self.assertEqual(len(sbf), len(sbf2))
        
        for i in range(100):
            self.assertIn(f"item_{i}", sbf2)
    
    def test_save_and_load(self):
        """测试文件保存和加载"""
        sbf = ScalableBloomFilter(initial_capacity=10)
        
        for i in range(50):
            sbf.add(f"item_{i}")
        
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_path = f.name
        
        try:
            sbf.save(temp_path)
            sbf2 = ScalableBloomFilter.load(temp_path)
            
            self.assertEqual(len(sbf), len(sbf2))
            
            for i in range(50):
                self.assertIn(f"item_{i}", sbf2)
        finally:
            os.unlink(temp_path)
    
    def test_max_filters_limit(self):
        """测试最大过滤器数量限制"""
        config = ScalableBloomFilterConfig(
            initial_capacity=1,
            growth_factor=1.1,
            max_filters=3,
        )
        sbf = ScalableBloomFilter(config=config)
        
        # 尝试添加很多元素，超过容量
        for i in range(100):
            sbf.add(f"item_{i}")
        
        # 过滤器数量应该不超过限制
        self.assertLessEqual(sbf.filter_count, 3)
    
    def test_no_false_negatives(self):
        """测试无假阴性（即使扩容后）"""
        sbf = ScalableBloomFilter(initial_capacity=10)
        
        items = [f"item_{i}" for i in range(200)]
        for item in items:
            sbf.add(item)
        
        # 所有添加的元素必须存在
        for item in items:
            self.assertIn(item, sbf)
    
    def test_repr(self):
        """测试字符串表示"""
        sbf = ScalableBloomFilter()
        repr_str = repr(sbf)
        self.assertIn("ScalableBloomFilter", repr_str)


# ============================================================================
# CountingBloomFilter 测试
# ============================================================================

class TestCountingBloomFilter(unittest.TestCase):
    """测试计数布隆过滤器"""
    
    def test_init_default(self):
        """测试默认初始化"""
        cbf = CountingBloomFilter()
        self.assertGreater(cbf.size, 0)
        self.assertGreater(cbf.hash_count, 0)
        self.assertTrue(cbf.is_empty)
    
    def test_add_and_contains(self):
        """测试添加和查询"""
        cbf = CountingBloomFilter()
        
        cbf.add("hello")
        cbf.add("world")
        
        self.assertIn("hello", cbf)
        self.assertIn("world", cbf)
        self.assertNotIn("foo", cbf)
    
    def test_remove(self):
        """测试删除"""
        cbf = CountingBloomFilter()
        
        cbf.add("hello")
        self.assertIn("hello", cbf)
        
        result = cbf.remove("hello")
        self.assertTrue(result)
        self.assertNotIn("hello", cbf)
    
    def test_remove_nonexistent(self):
        """测试删除不存在的元素"""
        cbf = CountingBloomFilter()
        
        result = cbf.remove("nonexistent")
        self.assertFalse(result)
    
    def test_multiple_add_and_remove(self):
        """测试多次添加和删除"""
        cbf = CountingBloomFilter()
        
        # 添加相同元素多次
        cbf.add("hello")
        cbf.add("hello")
        cbf.add("hello")
        
        self.assertEqual(cbf.count("hello"), 3)
        
        # 删除一次
        cbf.remove("hello")
        self.assertEqual(cbf.count("hello"), 2)
        self.assertIn("hello", cbf)
        
        # 再删除一次
        cbf.remove("hello")
        self.assertEqual(cbf.count("hello"), 1)
        self.assertIn("hello", cbf)
        
        # 删除最后一次
        cbf.remove("hello")
        self.assertEqual(cbf.count("hello"), 0)
        self.assertNotIn("hello", cbf)
    
    def test_counter_overflow(self):
        """测试计数器溢出"""
        # 使用 4 位计数器（最大值 15）
        cbf = CountingBloomFilter(counter_bits=4)
        
        # 添加同一个元素多次
        for _ in range(20):
            result = cbf.add("test")
            if not result:
                # 溢出后添加失败
                break
        
        # 计数应该被限制在最大值
        self.assertLessEqual(cbf.count("test"), 15)
    
    def test_counter_bits(self):
        """测试不同计数器位数"""
        for bits in [4, 8, 16]:
            cbf = CountingBloomFilter(counter_bits=bits)
            self.assertEqual(cbf._counter_bits, bits)
            self.assertEqual(cbf._max_count, (1 << bits) - 1)
    
    def test_invalid_counter_bits(self):
        """测试无效的计数器位数"""
        with self.assertRaises(ValueError):
            CountingBloomFilter(counter_bits=5)
        
        with self.assertRaises(ValueError):
            CountingBloomFilter(counter_bits=32)
    
    def test_len(self):
        """测试长度"""
        cbf = CountingBloomFilter()
        self.assertEqual(len(cbf), 0)
        
        cbf.add("a")
        self.assertEqual(len(cbf), 1)
        
        cbf.add("a")  # 重复添加
        self.assertEqual(len(cbf), 2)
        
        cbf.remove("a")
        self.assertEqual(len(cbf), 1)
    
    def test_clear(self):
        """测试清除"""
        cbf = CountingBloomFilter()
        cbf.add("a")
        cbf.add("b")
        
        cbf.clear()
        
        self.assertEqual(len(cbf), 0)
        self.assertNotIn("a", cbf)
        self.assertNotIn("b", cbf)
    
    def test_get_stats(self):
        """测试统计信息"""
        cbf = CountingBloomFilter()
        for i in range(50):
            cbf.add(f"item_{i}")
        
        stats = cbf.get_stats()
        
        self.assertIn('size', stats)
        self.assertIn('hash_count', stats)
        self.assertIn('elements_added', stats)
        self.assertIn('non_zero_counters', stats)
        self.assertIn('fill_ratio', stats)
        self.assertIn('counter_bits', stats)
    
    def test_serialization(self):
        """测试序列化和反序列化"""
        cbf = CountingBloomFilter(counter_bits=8)
        for i in range(50):
            cbf.add(f"item_{i}")
        
        data = cbf.to_bytes()
        self.assertIsInstance(data, bytes)
        
        cbf2 = CountingBloomFilter.from_bytes(data)
        
        self.assertEqual(cbf.size, cbf2.size)
        self.assertEqual(len(cbf), len(cbf2))
        
        for i in range(50):
            self.assertIn(f"item_{i}", cbf2)
    
    def test_serialization_4bit(self):
        """测试 4 位计数器序列化"""
        cbf = CountingBloomFilter(counter_bits=4)
        for i in range(50):
            cbf.add(f"item_{i}")
        
        data = cbf.to_bytes()
        cbf2 = CountingBloomFilter.from_bytes(data)
        
        for i in range(50):
            self.assertIn(f"item_{i}", cbf2)
    
    def test_serialization_16bit(self):
        """测试 16 位计数器序列化"""
        cbf = CountingBloomFilter(counter_bits=16)
        for i in range(50):
            cbf.add(f"item_{i}")
        
        data = cbf.to_bytes()
        cbf2 = CountingBloomFilter.from_bytes(data)
        
        for i in range(50):
            self.assertIn(f"item_{i}", cbf2)
    
    def test_save_and_load(self):
        """测试文件保存和加载"""
        cbf = CountingBloomFilter()
        for i in range(50):
            cbf.add(f"item_{i}")
        
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_path = f.name
        
        try:
            cbf.save(temp_path)
            cbf2 = CountingBloomFilter.load(temp_path)
            
            self.assertEqual(len(cbf), len(cbf2))
            
            for i in range(50):
                self.assertIn(f"item_{i}", cbf2)
        finally:
            os.unlink(temp_path)
    
    def test_repr(self):
        """测试字符串表示"""
        cbf = CountingBloomFilter()
        repr_str = repr(cbf)
        self.assertIn("CountingBloomFilter", repr_str)


# ============================================================================
# 工厂函数和构建器测试
# ============================================================================

class TestFactoryFunctions(unittest.TestCase):
    """测试工厂函数"""
    
    def test_create_optimal_filter(self):
        """测试创建最优过滤器"""
        bf = create_optimal_filter(1000, 0.01)
        
        self.assertIsInstance(bf, BloomFilter)
        self.assertGreater(bf.size, 0)
    
    def test_from_iterable_list(self):
        """测试从列表创建"""
        items = ["a", "b", "c", "d", "e"]
        bf = from_iterable(items)
        
        for item in items:
            self.assertIn(item, bf)
    
    def test_from_iterable_set(self):
        """测试从集合创建"""
        items = {"a", "b", "c", "d", "e"}
        bf = from_iterable(items)
        
        for item in items:
            self.assertIn(item, bf)
    
    def test_compare_hash_functions(self):
        """测试哈希函数比较"""
        items = [f"item_{i}" for i in range(100)]
        # 查询中包含一些不在集合中的元素
        queries = [f"item_{i}" for i in range(150)]
        
        results = compare_hash_functions(items, queries, 100)
        
        self.assertIn('murmur', results)
        self.assertIn('fnv', results)
        self.assertIn('djb2', results)
        self.assertIn('sha256', results)
        
        for name, data in results.items():
            self.assertIn('add_time_ms', data)
            self.assertIn('query_time_ms', data)
            self.assertIn('actual_fp_rate', data)


class TestBloomFilterBuilder(unittest.TestCase):
    """测试构建器模式"""
    
    def test_basic_build(self):
        """测试基本构建"""
        bf = BloomFilterBuilder().build()
        self.assertIsInstance(bf, BloomFilter)
    
    def test_fluent_api(self):
        """测试流畅 API"""
        bf = (BloomFilterBuilder()
              .expected_elements(1000)
              .false_positive_rate(0.001)
              .with_hash('murmur')
              .build())
        
        self.assertIsInstance(bf, BloomFilter)
    
    def test_with_items(self):
        """测试带初始元素"""
        items = ["a", "b", "c"]
        bf = (BloomFilterBuilder()
              .with_items(items)
              .build())
        
        for item in items:
            self.assertIn(item, bf)
    
    def test_auto_resize_with_items(self):
        """测试自动调整大小"""
        items = [f"item_{i}" for i in range(100)]
        bf = (BloomFilterBuilder()
              .expected_elements(10)  # 设置比实际小
              .with_items(items)  # 应该自动调整
              .build())
        
        # 所有元素应该在
        for item in items:
            self.assertIn(item, bf)


# ============================================================================
# 边界情况测试
# ============================================================================

class TestEdgeCases(unittest.TestCase):
    """测试边界情况"""
    
    def test_empty_filter(self):
        """测试空过滤器"""
        bf = BloomFilter()
        
        # 空过滤器不应该包含任何元素
        self.assertNotIn("anything", bf)
        self.assertNotIn("", bf)
        self.assertNotIn(0, bf)
    
    def test_single_element(self):
        """测试单个元素"""
        bf = BloomFilter()
        bf.add("only_one")
        
        self.assertIn("only_one", bf)
        self.assertEqual(len(bf), 1)
    
    def test_large_elements(self):
        """测试大量元素"""
        bf = BloomFilter(expected_elements=10000, false_positive_rate=0.01)
        
        for i in range(10000):
            bf.add(f"item_{i}")
        
        # 随机检查一些元素
        for i in range(0, 10000, 100):
            self.assertIn(f"item_{i}", bf)
    
    def test_unicode_strings(self):
        """测试 Unicode 字符串"""
        bf = BloomFilter()
        
        items = ["你好", "世界", "🌍", "🎉", "тест", "テスト"]
        for item in items:
            bf.add(item)
        
        for item in items:
            self.assertIn(item, bf)
    
    def test_special_characters(self):
        """测试特殊字符"""
        bf = BloomFilter()
        
        items = ["hello\tworld", "line\nbreak", "tab\there", "quote\"test"]
        for item in items:
            bf.add(item)
        
        for item in items:
            self.assertIn(item, bf)
    
    def test_empty_string(self):
        """测试空字符串"""
        bf = BloomFilter()
        bf.add("")
        
        self.assertIn("", bf)
        self.assertEqual(len(bf), 1)
    
    def test_very_long_string(self):
        """测试很长字符串"""
        bf = BloomFilter()
        long_string = "x" * 10000
        
        bf.add(long_string)
        self.assertIn(long_string, bf)
    
    def test_very_low_fp_rate(self):
        """测试非常低的假阳性率"""
        bf = BloomFilter(expected_elements=100, false_positive_rate=0.0001)
        
        for i in range(100):
            bf.add(f"item_{i}")
        
        for i in range(100):
            self.assertIn(f"item_{i}", bf)
    
    def test_bitarray_edge_cases(self):
        """测试 BitArray 边界情况"""
        # 测试跨越字节边界的位
        ba = BitArray(16)
        ba[7] = True
        ba[8] = True
        self.assertTrue(ba[7])
        self.assertTrue(ba[8])
        
        # 测试最后一位
        ba = BitArray(100)
        ba[99] = True
        self.assertTrue(ba[99])
        self.assertFalse(ba[98])


# ============================================================================
# 性能测试
# ============================================================================

class TestPerformance(unittest.TestCase):
    """性能测试"""
    
    def test_large_scale_add(self):
        """测试大规模添加性能"""
        import time
        
        bf = BloomFilter(expected_elements=100000, false_positive_rate=0.01)
        
        start = time.perf_counter()
        for i in range(100000):
            bf.add(f"item_{i}")
        elapsed = time.perf_counter() - start
        
        # 应该在合理时间内完成（< 5 秒）
        self.assertLess(elapsed, 5.0)
    
    def test_large_scale_query(self):
        """测试大规模查询性能"""
        import time
        
        bf = BloomFilter(expected_elements=100000, false_positive_rate=0.01)
        for i in range(100000):
            bf.add(f"item_{i}")
        
        start = time.perf_counter()
        for i in range(100000):
            _ = f"item_{i}" in bf
        elapsed = time.perf_counter() - start
        
        # 应该在合理时间内完成（< 5 秒）
        self.assertLess(elapsed, 5.0)
    
    def test_memory_efficiency(self):
        """测试内存效率"""
        # 100 万元素，1% 假阳性率
        stats = estimate_memory_usage(1000000, 0.01)
        
        # 应该使用约 1.2 MB（理论值）
        self.assertLess(stats['megabytes'], 2.0)


if __name__ == '__main__':
    unittest.main(verbosity=2)