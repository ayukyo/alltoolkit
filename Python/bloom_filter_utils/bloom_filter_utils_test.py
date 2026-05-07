"""
Bloom Filter Utils 测试套件

测试覆盖：
- BloomFilter 基本功能
- 假阳性率验证
- 序列化/反序列化
- ScalableBloomFilter 扩展功能
- CountingBloomFilter 删除功能
- 边界条件和错误处理
"""

import unittest
import random
import string
import math
from mod import (
    BloomFilter, 
    ScalableBloomFilter, 
    CountingBloomFilter,
    BloomFilterStats,
    create_filter,
    create_scalable_filter,
    create_counting_filter
)


class TestBloomFilter(unittest.TestCase):
    """BloomFilter 基础测试"""
    
    def test_create_basic(self):
        """测试基本创建"""
        bf = BloomFilter(capacity=1000, error_rate=0.01)
        self.assertEqual(bf.capacity, 1000)
        self.assertEqual(bf.error_rate, 0.01)
        self.assertEqual(len(bf), 0)
    
    def test_create_invalid_params(self):
        """测试无效参数"""
        with self.assertRaises(ValueError):
            BloomFilter(capacity=0)
        with self.assertRaises(ValueError):
            BloomFilter(capacity=-100)
        with self.assertRaises(ValueError):
            BloomFilter(capacity=100, error_rate=0)
        with self.assertRaises(ValueError):
            BloomFilter(capacity=100, error_rate=1)
        with self.assertRaises(ValueError):
            BloomFilter(capacity=100, error_rate=-0.5)
        with self.assertRaises(ValueError):
            BloomFilter(capacity=100, hash_algorithm='invalid')
    
    def test_add_and_contains(self):
        """测试添加和包含检查"""
        bf = BloomFilter(capacity=100)
        
        # 添加元素
        bf.add("hello")
        bf.add("world")
        bf.add(123)
        bf.add(45.67)
        
        self.assertEqual(len(bf), 4)
        
        # 检查存在
        self.assertIn("hello", bf)
        self.assertIn("world", bf)
        self.assertIn(123, bf)
        self.assertIn(45.67, bf)
        
        # 检查不存在
        self.assertNotIn("unknown", bf)
        self.assertNotIn(999, bf)
    
    def test_might_contain(self):
        """测试 might_contain 方法"""
        bf = BloomFilter(capacity=100)
        bf.add("test")
        
        self.assertTrue(bf.might_contain("test"))
        self.assertFalse(bf.might_contain("absent"))
    
    def test_clear(self):
        """测试清空"""
        bf = BloomFilter(capacity=100)
        bf.add("item1")
        bf.add("item2")
        self.assertEqual(len(bf), 2)
        
        bf.clear()
        self.assertEqual(len(bf), 0)
        self.assertNotIn("item1", bf)
        self.assertNotIn("item2", bf)
    
    def test_bytes_operations(self):
        """测试字节序列化"""
        bf = BloomFilter(capacity=100, error_rate=0.05)
        items = ["alpha", "beta", "gamma", "delta"]
        for item in items:
            bf.add(item)
        
        # 序列化
        data = bf.to_bytes()
        self.assertIsInstance(data, bytes)
        self.assertGreater(len(data), 0)
        
        # 反序列化
        bf2 = BloomFilter.from_bytes(data)
        self.assertEqual(bf2.capacity, bf.capacity)
        self.assertEqual(bf2.error_rate, bf.error_rate)
        self.assertEqual(len(bf2), len(bf))
        
        # 验证元素
        for item in items:
            self.assertIn(item, bf2)
    
    def test_get_stats(self):
        """测试统计信息"""
        bf = BloomFilter(capacity=100, error_rate=0.01)
        stats = bf.get_stats()
        
        self.assertIsInstance(stats, BloomFilterStats)
        self.assertEqual(stats.capacity, 100)
        self.assertEqual(stats.error_rate, 0.01)
        self.assertEqual(stats.num_elements, 0)
        self.assertEqual(stats.fill_ratio, 0)
        self.assertEqual(stats.current_error_rate, 0)
        
        # 添加元素后检查
        for i in range(50):
            bf.add(f"item_{i}")
        
        stats = bf.get_stats()
        self.assertEqual(stats.num_elements, 50)
        self.assertGreater(stats.fill_ratio, 0)
    
    def test_hash_algorithms(self):
        """测试不同哈希算法"""
        for algo in ['md5', 'sha1', 'sha256', 'sha512']:
            bf = BloomFilter(capacity=100, hash_algorithm=algo)
            bf.add("test")
            self.assertIn("test", bf)
    
    def test_optimal_parameters(self):
        """测试最优参数计算"""
        # 验证参数在合理范围内
        bf = BloomFilter(capacity=10000, error_rate=0.01)
        
        # m ≈ -n*ln(p)/(ln(2)^2)
        expected_bits = -10000 * math.log(0.01) / (math.log(2) ** 2)
        self.assertAlmostEqual(bf.num_bits, expected_bits, delta=expected_bits * 0.1)
        
        # k ≈ m*ln(2)/n
        expected_hashes = bf.num_bits * math.log(2) / 10000
        self.assertAlmostEqual(bf.num_hashes, expected_hashes, delta=2)
    
    def test_string_representation(self):
        """测试字符串表示"""
        bf = BloomFilter(capacity=1000, error_rate=0.01)
        repr_str = repr(bf)
        
        self.assertIn("BloomFilter", repr_str)
        self.assertIn("capacity=1000", repr_str)
        self.assertIn("error_rate=0.01", repr_str)


class TestBloomFilterFalsePositiveRate(unittest.TestCase):
    """假阳性率测试"""
    
    def test_false_positive_rate(self):
        """测试假阳性率在预期范围内"""
        capacity = 10000
        error_rate = 0.01
        
        bf = BloomFilter(capacity=capacity, error_rate=error_rate)
        
        # 添加元素
        added = set()
        for i in range(capacity):
            item = f"item_{i}"
            bf.add(item)
            added.add(item)
        
        # 测试假阳性
        false_positives = 0
        test_count = 10000
        
        for i in range(capacity, capacity + test_count):
            item = f"item_{i}"
            if item in bf:
                false_positives += 1
        
        actual_rate = false_positives / test_count
        print(f"\n假阳性率测试: 预期 {error_rate}, 实际 {actual_rate:.4f}")
        
        # 实际率应接近预期，允许一定误差
        self.assertLess(actual_rate, error_rate * 3, 
                       f"假阳性率 {actual_rate} 远高于预期 {error_rate}")
    
    def test_no_false_negatives(self):
        """测试不会产生假阴性"""
        bf = BloomFilter(capacity=1000, error_rate=0.01)
        
        items = [f"test_item_{i}" for i in range(500)]
        for item in items:
            bf.add(item)
        
        # 所有添加的元素都应该存在
        for item in items:
            self.assertIn(item, bf, f"假阴性: {item} 应该存在")


class TestScalableBloomFilter(unittest.TestCase):
    """ScalableBloomFilter 测试"""
    
    def test_create_basic(self):
        """测试基本创建"""
        sbf = ScalableBloomFilter(initial_capacity=100, error_rate=0.01)
        self.assertEqual(len(sbf), 0)
    
    def test_invalid_params(self):
        """测试无效参数"""
        with self.assertRaises(ValueError):
            ScalableBloomFilter(initial_capacity=0)
        with self.assertRaises(ValueError):
            ScalableBloomFilter(initial_capacity=100, error_rate=0)
        with self.assertRaises(ValueError):
            ScalableBloomFilter(initial_capacity=100, growth_factor=1)
    
    def test_add_and_contains(self):
        """测试添加和包含检查"""
        sbf = ScalableBloomFilter(initial_capacity=10, error_rate=0.01)
        
        items = [f"item_{i}" for i in range(100)]
        for item in items:
            sbf.add(item)
        
        self.assertEqual(len(sbf), 100)
        
        for item in items:
            self.assertIn(item, sbf)
    
    def test_automatic_scaling(self):
        """测试自动扩展"""
        sbf = ScalableBloomFilter(
            initial_capacity=10, 
            error_rate=0.01,
            growth_factor=2
        )
        
        # 添加超过初始容量的元素
        for i in range(50):
            sbf.add(f"item_{i}")
        
        stats = sbf.get_stats()
        self.assertGreater(stats['num_layers'], 1, 
                          "应该创建多个层")
        self.assertEqual(stats['total_elements'], 50)
    
    def test_get_stats(self):
        """测试统计信息"""
        sbf = ScalableBloomFilter(initial_capacity=5, error_rate=0.01)
        
        for i in range(20):
            sbf.add(f"item_{i}")
        
        stats = sbf.get_stats()
        
        self.assertEqual(stats['total_elements'], 20)
        self.assertIn('num_layers', stats)
        self.assertIn('layers', stats)
        self.assertIsInstance(stats['layers'], list)


class TestCountingBloomFilter(unittest.TestCase):
    """CountingBloomFilter 测试"""
    
    def test_create_basic(self):
        """测试基本创建"""
        cbf = CountingBloomFilter(capacity=1000, error_rate=0.01)
        self.assertEqual(len(cbf), 0)
    
    def test_invalid_params(self):
        """测试无效参数"""
        with self.assertRaises(ValueError):
            CountingBloomFilter(capacity=0)
        with self.assertRaises(ValueError):
            CountingBloomFilter(capacity=100, error_rate=0)
    
    def test_add_and_contains(self):
        """测试添加和包含检查"""
        cbf = CountingBloomFilter(capacity=100)
        
        cbf.add("hello")
        cbf.add("world")
        
        self.assertIn("hello", cbf)
        self.assertIn("world", cbf)
        self.assertEqual(len(cbf), 2)
    
    def test_remove(self):
        """测试删除功能"""
        cbf = CountingBloomFilter(capacity=100)
        
        cbf.add("test")
        self.assertIn("test", cbf)
        
        # 删除
        result = cbf.remove("test")
        self.assertTrue(result)
        self.assertNotIn("test", cbf)
        self.assertEqual(len(cbf), 0)
    
    def test_remove_nonexistent(self):
        """测试删除不存在的元素"""
        cbf = CountingBloomFilter(capacity=100)
        
        result = cbf.remove("nonexistent")
        self.assertFalse(result)
    
    def test_multiple_add_remove(self):
        """测试多次添加和删除"""
        cbf = CountingBloomFilter(capacity=100)
        
        items = [f"item_{i}" for i in range(20)]
        
        # 添加所有
        for item in items:
            cbf.add(item)
        
        self.assertEqual(len(cbf), 20)
        
        # 删除一半
        for item in items[:10]:
            cbf.remove(item)
        
        self.assertEqual(len(cbf), 10)
        
        # 验证状态
        for item in items[:10]:
            self.assertNotIn(item, cbf)
        for item in items[10:]:
            self.assertIn(item, cbf)
    
    def test_counter_overflow(self):
        """测试计数器溢出保护"""
        cbf = CountingBloomFilter(capacity=10, max_count=5)
        
        # 同一元素多次添加
        for _ in range(10):
            cbf.add("test")
        
        # 计数器应该有上限
        self.assertIn("test", cbf)


class TestConvenienceFunctions(unittest.TestCase):
    """便捷函数测试"""
    
    def test_create_filter(self):
        """测试 create_filter"""
        bf = create_filter(capacity=1000, error_rate=0.01)
        self.assertIsInstance(bf, BloomFilter)
        self.assertEqual(bf.capacity, 1000)
    
    def test_create_scalable_filter(self):
        """测试 create_scalable_filter"""
        sbf = create_scalable_filter(initial_capacity=100)
        self.assertIsInstance(sbf, ScalableBloomFilter)
    
    def test_create_counting_filter(self):
        """测试 create_counting_filter"""
        cbf = create_counting_filter(capacity=100)
        self.assertIsInstance(cbf, CountingBloomFilter)


class TestEdgeCases(unittest.TestCase):
    """边界条件测试"""
    
    def test_empty_filter(self):
        """测试空过滤器"""
        bf = BloomFilter(capacity=10)
        
        self.assertNotIn("anything", bf)
        self.assertEqual(len(bf), 0)
    
    def test_single_item(self):
        """测试单个元素"""
        bf = BloomFilter(capacity=10)
        bf.add("only_one")
        
        self.assertIn("only_one", bf)
        self.assertEqual(len(bf), 1)
    
    def test_large_capacity(self):
        """测试大容量"""
        bf = BloomFilter(capacity=1000000, error_rate=0.001)
        
        # 添加少量元素验证工作正常
        for i in range(100):
            bf.add(f"item_{i}")
        
        self.assertIn("item_0", bf)
        self.assertIn("item_99", bf)
        self.assertNotIn("item_100", bf)
    
    def test_very_small_error_rate(self):
        """测试很小的错误率"""
        bf = BloomFilter(capacity=100, error_rate=0.0001)
        
        # 验证位数组更大
        self.assertGreater(bf.num_bits, 1000)
    
    def test_unicode_strings(self):
        """测试 Unicode 字符串"""
        bf = BloomFilter(capacity=100)
        
        unicode_items = [
            "你好世界",
            "こんにちは",
            "مرحبا",
            "🎉🎊🎈",
            "café résumé naïve"
        ]
        
        for item in unicode_items:
            bf.add(item)
        
        for item in unicode_items:
            self.assertIn(item, bf)
    
    def test_bytes_input(self):
        """测试字节输入"""
        bf = BloomFilter(capacity=100)
        
        bf.add(b"binary_data")
        bf.add(b"\x00\x01\x02\xff")
        
        self.assertIn(b"binary_data", bf)
        self.assertIn(b"\x00\x01\x02\xff", bf)
    
    def test_numeric_types(self):
        """测试各种数字类型"""
        bf = BloomFilter(capacity=100)
        
        items = [0, 1, -1, 3.14, -2.5, 10**100, float('inf'), float('-inf')]
        
        for item in items:
            bf.add(item)
        
        for item in items:
            self.assertIn(item, bf)
    
    def test_mixed_types(self):
        """测试混合类型"""
        bf = BloomFilter(capacity=100)
        
        items = [
            "string",
            42,
            3.14,
            True,
            None,
            (1, 2, 3),
            ["list", "item"]
        ]
        
        for item in items:
            bf.add(item)
        
        for item in items:
            self.assertIn(item, bf)


class TestPerformance(unittest.TestCase):
    """性能测试"""
    
    def test_add_performance(self):
        """测试添加性能"""
        import time
        
        bf = BloomFilter(capacity=100000, error_rate=0.01)
        
        start = time.time()
        for i in range(10000):
            bf.add(f"item_{i}")
        elapsed = time.time() - start
        
        print(f"\n添加 10000 个元素耗时: {elapsed:.4f} 秒")
        print(f"平均每个元素: {elapsed/10000*1000:.4f} 毫秒")
        
        # 应该在合理时间内完成
        self.assertLess(elapsed, 5, "添加操作太慢")
    
    def test_contains_performance(self):
        """测试查询性能"""
        import time
        
        bf = BloomFilter(capacity=100000, error_rate=0.01)
        
        for i in range(10000):
            bf.add(f"item_{i}")
        
        start = time.time()
        for i in range(10000):
            _ = f"item_{i}" in bf
        elapsed = time.time() - start
        
        print(f"\n查询 10000 次耗时: {elapsed:.4f} 秒")
        print(f"平均每次查询: {elapsed/10000*1000:.4f} 毫秒")
        
        self.assertLess(elapsed, 5, "查询操作太慢")
    
    def test_memory_efficiency(self):
        """测试内存效率"""
        import sys
        
        bf = BloomFilter(capacity=100000, error_rate=0.01)
        
        # 位数组大小
        bits = bf.num_bits
        bytes_size = (bits + 7) // 8
        
        print(f"\n位数组大小: {bits:,} bits = {bytes_size:,} bytes")
        print(f"每元素约: {bytes_size/100000:.2f} bytes")
        
        # 实际 Python 对象大小
        actual_size = sys.getsizeof(bf._bit_array) + len(bf._bit_array) * 8  # 粗略估计
        print(f"Python 估计大小: {actual_size:,} bytes")


if __name__ == "__main__":
    # 运行所有测试
    unittest.main(verbosity=2)