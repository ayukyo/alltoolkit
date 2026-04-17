"""
HyperLogLog Utils 测试文件

测试所有核心功能：
- 基本添加和计数
- 精度和误差范围
- 序列化和反序列化
- 合并操作
- 集合操作（交集、Jaccard）
"""

import unittest
import tempfile
import os
import random
import string
from hyperloglog_utils import (
    HyperLogLog,
    HyperLogLogPlusPlus,
    SparseHyperLogLog,
    HyperLogLogBuilder,
    create_hll,
    from_iterable,
    merge_multiple,
    estimate_memory,
    compare_precision,
    count_leading_zeros,
    murmurhash3_x64_128,
    xxhash_64,
    sha256_hash_64,
)


class TestHashFunctions(unittest.TestCase):
    """测试哈希函数"""
    
    def test_murmurhash_basic(self):
        """测试 MurmurHash 基本功能"""
        data = b"hello world"
        hash1 = murmurhash3_x64_128(data, 0)
        hash2 = murmurhash3_x64_128(data, 0)
        
        # 相同输入应产生相同输出
        self.assertEqual(hash1, hash2)
        
        # 哈希值应该是 64 位整数
        self.assertGreater(hash1, 0)
        self.assertLess(hash1, 1 << 64)
    
    def test_xxhash_basic(self):
        """测试 XXHash 基本功能"""
        data = b"test data"
        hash1 = xxhash_64(data, 0)
        hash2 = xxhash_64(data, 0)
        
        self.assertEqual(hash1, hash2)
        self.assertGreater(hash1, 0)
    
    def test_sha256_hash_basic(self):
        """测试 SHA256 Hash 基本功能"""
        data = b"some data"
        hash1 = sha256_hash_64(data, 0)
        hash2 = sha256_hash_64(data, 0)
        
        self.assertEqual(hash1, hash2)
    
    def test_hash_distribution(self):
        """测试哈希分布"""
        hashes = set()
        for i in range(1000):
            h = murmurhash3_x64_128(f"item_{i}".encode(), 0)
            hashes.add(h)
        
        # 哈希值应该均匀分布，冲突率应该很低
        collision_rate = 1 - len(hashes) / 1000
        self.assertLess(collision_rate, 0.01)


class TestLeadingZeros(unittest.TestCase):
    """测试前导零计数"""
    
    def test_basic_cases(self):
        """测试基本情况"""
        self.assertEqual(count_leading_zeros(0, 64), 65)
        self.assertEqual(count_leading_zeros(1, 64), 64)
        self.assertEqual(count_leading_zeros(2, 64), 63)
        self.assertEqual(count_leading_zeros(4, 64), 62)
        self.assertEqual(count_leading_zeros(8, 64), 61)
        self.assertEqual(count_leading_zeros(16, 64), 60)
    
    def test_large_values(self):
        """测试大值"""
        # 最高位为 1
        val = 1 << 63
        self.assertEqual(count_leading_zeros(val, 64), 1)
        
        # 某些中间位
        val = 1 << 32
        self.assertEqual(count_leading_zeros(val, 64), 32)


class TestHyperLogLog(unittest.TestCase):
    """测试 HyperLogLog"""
    
    def test_basic_creation(self):
        """测试基本创建"""
        hll = HyperLogLog(precision=10)
        self.assertEqual(hll.precision, 10)
        self.assertEqual(hll.num_registers, 1024)
        self.assertTrue(hll.is_empty)
    
    def test_invalid_precision(self):
        """测试无效精度"""
        with self.assertRaises(ValueError):
            HyperLogLog(precision=3)
        
        with self.assertRaises(ValueError):
            HyperLogLog(precision=17)
    
    def test_invalid_hash_func(self):
        """测试无效哈希函数"""
        with self.assertRaises(ValueError):
            HyperLogLog(hash_func='invalid')
    
    def test_single_element(self):
        """测试单个元素"""
        hll = HyperLogLog(precision=10)
        hll.add("test")
        estimate = hll.count()
        self.assertGreater(estimate, 0)
        self.assertLess(estimate, 10)  # 单个元素误差很小
    
    def test_multiple_elements(self):
        """测试多个元素"""
        hll = HyperLogLog(precision=12)
        items = [f"item_{i}" for i in range(1000)]
        
        for item in items:
            hll.add(item)
        
        estimate = hll.count()
        actual = 1000
        
        # 误差应该在标准误差范围内
        error = abs(estimate - actual) / actual
        self.assertLess(error, 0.05)  # 5%误差
    
    def test_large_dataset(self):
        """测试大数据集"""
        hll = HyperLogLog(precision=14)
        
        # 添加 10000 个元素
        for i in range(10000):
            hll.add(f"user_{i}")
        
        estimate = hll.count()
        actual = 10000
        
        error = abs(estimate - actual) / actual
        self.assertLess(error, 0.02)  # 2%误差
    
    def test_duplicate_elements(self):
        """测试重复元素"""
        hll = HyperLogLog(precision=10)
        
        # 添加同一个元素多次
        for _ in range(100):
            hll.add("duplicate")
        
        estimate = hll.count()
        self.assertLess(estimate, 2)  # 应该接近 1
    
    def test_update_batch(self):
        """测试批量添加"""
        hll = HyperLogLog(precision=10)
        items = [f"batch_{i}" for i in range(100)]
        
        hll.update(items)
        estimate = hll.count()
        
        self.assertGreater(estimate, 90)
        self.assertLess(estimate, 110)
    
    def test_clear(self):
        """测试清除"""
        hll = HyperLogLog(precision=10)
        hll.add("item1")
        hll.add("item2")
        
        self.assertFalse(hll.is_empty)
        
        hll.clear()
        self.assertTrue(hll.is_empty)
        self.assertEqual(hll.count(), 0)
    
    def test_get_stats(self):
        """测试统计信息"""
        hll = HyperLogLog(precision=12)
        for i in range(100):
            hll.add(f"stat_{i}")
        
        stats = hll.get_stats()
        self.assertEqual(stats.precision, 12)
        self.assertEqual(stats.num_registers, 4096)
        self.assertGreater(stats.estimated_cardinality, 0)
    
    def test_len(self):
        """测试 len"""
        hll = HyperLogLog(precision=10)
        for i in range(50):
            hll.add(f"len_{i}")
        
        length = len(hll)
        self.assertGreater(length, 45)
        self.assertLess(length, 55)


class TestHyperLogLogSerialization(unittest.TestCase):
    """测试 HyperLogLog 序列化"""
    
    def test_to_bytes_from_bytes(self):
        """测试字节序列化"""
        hll = HyperLogLog(precision=10)
        for i in range(100):
            hll.add(f"ser_{i}")
        
        data = hll.to_bytes()
        restored = HyperLogLog.from_bytes(data)
        
        self.assertEqual(hll.precision, restored.precision)
        self.assertEqual(hll.count(), restored.count())
    
    def test_file_save_load(self):
        """测试文件保存和加载"""
        hll = HyperLogLog(precision=12)
        for i in range(200):
            hll.add(f"file_{i}")
        
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_path = f.name
        
        try:
            hll.save(temp_path)
            loaded = HyperLogLog.load(temp_path)
            
            self.assertEqual(hll.precision, loaded.precision)
            self.assertEqual(hll.count(), loaded.count())
        finally:
            os.unlink(temp_path)
    
    def test_different_hash_funcs(self):
        """测试不同哈希函数的序列化"""
        for hash_name in ['murmur', 'sha256', 'xxhash']:
            hll = HyperLogLog(precision=10, hash_func=hash_name)
            hll.add("test")
            
            data = hll.to_bytes()
            restored = HyperLogLog.from_bytes(data)
            
            self.assertEqual(restored._hash_func_name, hash_name)


class TestHyperLogLogMerge(unittest.TestCase):
    """测试 HyperLogLog 合并"""
    
    def test_basic_merge(self):
        """测试基本合并"""
        hll1 = HyperLogLog(precision=10)
        hll2 = HyperLogLog(precision=10)
        
        # 第一个添加 0-50
        for i in range(50):
            hll1.add(f"merge1_{i}")
        
        # 第二个添加 50-100
        for i in range(50, 100):
            hll2.add(f"merge2_{i}")
        
        merged = hll1.merge(hll2)
        estimate = merged.count()
        
        # 应该接近 100
        self.assertGreater(estimate, 90)
        self.assertLess(estimate, 110)
    
    def test_incompatible_merge(self):
        """测试不兼容的合并"""
        hll1 = HyperLogLog(precision=10)
        hll2 = HyperLogLog(precision=12)
        
        with self.assertRaises(ValueError):
            hll1.merge(hll2)
    
    def test_union_alias(self):
        """测试 union 别名"""
        hll1 = HyperLogLog(precision=10)
        hll2 = HyperLogLog(precision=10)
        
        hll1.add("a")
        hll2.add("b")
        
        union = hll1.union(hll2)
        self.assertGreater(len(union), 1)
    
    def test_merge_with_duplicates(self):
        """测试有重复元素的合并"""
        hll1 = HyperLogLog(precision=10)
        hll2 = HyperLogLog(precision=10)
        
        # 两个都添加相同的元素
        for i in range(50):
            hll1.add(f"dup_{i}")
            hll2.add(f"dup_{i}")
        
        merged = hll1.merge(hll2)
        estimate = merged.count()
        
        # 应该接近 50（不是 100）
        self.assertLess(estimate, 60)


class TestHyperLogLogSetOperations(unittest.TestCase):
    """测试 HyperLogLog 集合操作"""
    
    def test_intersection_cardinality(self):
        """测试交集基数估计"""
        hll1 = HyperLogLog(precision=12)
        hll2 = HyperLogLog(precision=12)
        
        # 集合 1: 0-100
        for i in range(100):
            hll1.add(f"inter_{i}")
        
        # 集合 2: 50-150（交集是 50-100）
        for i in range(50, 150):
            hll2.add(f"inter_{i}")
        
        intersection = hll1.intersection_cardinality(hll2)
        
        # 实际交集大小是 50
        self.assertGreater(intersection, 40)
        self.assertLess(intersection, 60)
    
    def test_jaccard_similarity(self):
        """测试 Jaccard 相似度"""
        hll1 = HyperLogLog(precision=12)
        hll2 = HyperLogLog(precision=12)
        
        # 相同集合
        for i in range(50):
            hll1.add(f"jac_{i}")
            hll2.add(f"jac_{i}")
        
        similarity = hll1.jaccard_similarity(hll2)
        self.assertGreater(similarity, 0.9)  # 应该接近 1
        
        # 完全不同集合
        hll3 = HyperLogLog(precision=12)
        hll4 = HyperLogLog(precision=12)
        
        for i in range(50):
            hll3.add(f"diff1_{i}")
            hll4.add(f"diff2_{i}")
        
        similarity = hll3.jaccard_similarity(hll4)
        self.assertLess(similarity, 0.1)  # 应该接近 0


class TestHyperLogLogPlusPlus(unittest.TestCase):
    """测试 HyperLogLog++"""
    
    def test_sparse_mode(self):
        """测试稀疏模式"""
        hll = HyperLogLogPlusPlus(precision=14)
        
        # 添加少量元素，应该保持稀疏模式
        for i in range(10):
            hll.add(f"sparse_{i}")
        
        self.assertTrue(hll.is_sparse)
        self.assertLess(hll.count(), 15)
    
    def test_dense_mode_conversion(self):
        """测试转换为密集模式"""
        hll = HyperLogLogPlusPlus(precision=12)
        
        # 添加足够多的元素以触发转换
        for i in range(10000):
            hll.add(f"dense_{i}")
        
        self.assertFalse(hll.is_sparse)
    
    def test_accuracy(self):
        """测试精度"""
        hll = HyperLogLogPlusPlus(precision=14)
        
        for i in range(10000):
            hll.add(f"acc_{i}")
        
        estimate = hll.count()
        error = abs(estimate - 10000) / 10000
        self.assertLess(error, 0.02)
    
    def test_serialization(self):
        """测试序列化"""
        hll = HyperLogLogPlusPlus(precision=12)
        for i in range(100):
            hll.add(f"serpp_{i}")
        
        data = hll.to_bytes()
        restored = HyperLogLogPlusPlus.from_bytes(data)
        
        self.assertEqual(hll.is_sparse, restored.is_sparse)
        self.assertEqual(hll.count(), restored.count())
    
    def test_merge(self):
        """测试合并"""
        hll1 = HyperLogLogPlusPlus(precision=12)
        hll2 = HyperLogLogPlusPlus(precision=12)
        
        for i in range(50):
            hll1.add(f"mergepp1_{i}")
        for i in range(50, 100):
            hll2.add(f"mergepp2_{i}")
        
        merged = hll1.merge(hll2)
        estimate = merged.count()
        
        self.assertGreater(estimate, 90)
    
    def test_stats(self):
        """测试统计信息"""
        hll = HyperLogLogPlusPlus(precision=12)
        for i in range(100):
            hll.add(f"statspp_{i}")
        
        stats = hll.get_stats()
        self.assertEqual(stats['precision'], 12)
        self.assertIn('is_sparse', stats)


class TestSparseHyperLogLog(unittest.TestCase):
    """测试稀疏 HyperLogLog"""
    
    def test_initial_state(self):
        """测试初始状态"""
        shll = SparseHyperLogLog(initial_precision=8, max_precision=16)
        
        self.assertEqual(shll.precision, 8)
        self.assertEqual(shll.max_precision, 16)
        self.assertFalse(shll.is_dense)
    
    def test_precision_upgrade(self):
        """测试精度升级"""
        shll = SparseHyperLogLog(initial_precision=4, max_precision=8)
        
        # 添加大量不同元素以触发升级或转换
        for i in range(1000):
            shll.add(f"upgrade_{i}")
        
        # 检查估计值是否合理
        estimate = shll.count()
        self.assertGreater(estimate, 900)
        self.assertLess(estimate, 1100)
    
    def test_dense_conversion(self):
        """测试密集模式转换"""
        shll = SparseHyperLogLog(initial_precision=4, max_precision=8, dense_threshold=100)
        
        # 添加足够多的元素以触发转换
        for i in range(200):
            shll.add(f"conv_{i}")
        
        # 应该转换为密集模式或精度已达到最大
        self.assertTrue(shll.is_dense or shll.precision == shll.max_precision)
    
    def test_small_dataset_accuracy(self):
        """测试小数据集精度"""
        shll = SparseHyperLogLog(initial_precision=8)
        
        for i in range(10):
            shll.add(f"small_{i}")
        
        # 小数据集应该很精确
        estimate = shll.count()
        self.assertLess(abs(estimate - 10), 5)
    
    def test_large_dataset_accuracy(self):
        """测试大数据集精度"""
        # 使用高精度以保证准确估计
        shll = SparseHyperLogLog(initial_precision=12, max_precision=16)
        
        for i in range(10000):
            shll.add(f"large_{i}")
        
        estimate = shll.count()
        # 应该接近 10000
        self.assertGreater(estimate, 9000)
        self.assertLess(estimate, 11000)
    
    def test_clear(self):
        """测试清除"""
        shll = SparseHyperLogLog()
        
        for i in range(100):
            shll.add(f"clear_{i}")
        
        shll.clear()
        
        self.assertEqual(shll.precision, shll._initial_precision)
        self.assertTrue(shll.is_empty)


class TestUtilityFunctions(unittest.TestCase):
    """测试工具函数"""
    
    def test_estimate_memory(self):
        """测试内存估算"""
        info = estimate_memory(10)
        
        self.assertEqual(info['precision'], 10)
        self.assertEqual(info['num_registers'], 1024)
        self.assertEqual(info['bytes'], 1024)
    
    def test_create_hll(self):
        """测试工厂函数"""
        hll = create_hll(precision=12)
        
        self.assertEqual(hll.precision, 12)
    
    def test_from_iterable(self):
        """测试从可迭代对象创建"""
        items = [f"iter_{i}" for i in range(100)]
        hll = from_iterable(items, precision=10)
        
        estimate = hll.count()
        self.assertGreater(estimate, 95)
    
    def test_merge_multiple(self):
        """测试合并多个"""
        hlls = []
        
        for i in range(4):
            hll = HyperLogLog(precision=10)
            for j in range(25):
                hll.add(f"multi_{i}_{j}")
            hlls.append(hll)
        
        merged = merge_multiple(hlls)
        estimate = merged.count()
        
        self.assertGreater(estimate, 90)
    
    def test_merge_empty_list(self):
        """测试合并空列表"""
        with self.assertRaises(ValueError):
            merge_multiple([])
    
    def test_compare_precision(self):
        """测试精度比较"""
        items = [f"comp_{i}" for i in range(500)]
        
        results = compare_precision(items, precisions=[8, 10, 12])
        
        self.assertIn(8, results)
        self.assertIn(10, results)
        self.assertIn(12, results)
        
        # 更高精度应该有更小的误差
        self.assertLess(
            results[12]['error_percent'],
            results[8]['error_percent']
        )


class TestBuilder(unittest.TestCase):
    """测试构建器"""
    
    def test_basic_build(self):
        """测试基本构建"""
        hll = HyperLogLogBuilder() \
            .precision(10) \
            .with_hash('murmur') \
            .build()
        
        self.assertEqual(hll.precision, 10)
    
    def test_build_with_items(self):
        """测试带元素的构建"""
        items = [f"build_{i}" for i in range(50)]
        
        hll = HyperLogLogBuilder() \
            .precision(10) \
            .with_items(items) \
            .build()
        
        estimate = hll.count()
        self.assertGreater(estimate, 45)


class TestEdgeCases(unittest.TestCase):
    """测试边界情况"""
    
    def test_empty_string(self):
        """测试空字符串"""
        hll = HyperLogLog(precision=10)
        hll.add("")
        
        estimate = hll.count()
        self.assertGreater(estimate, 0)
    
    def test_bytes_input(self):
        """测试字节输入"""
        hll = HyperLogLog(precision=10)
        hll.add(b"bytes_data")
        
        estimate = hll.count()
        self.assertGreater(estimate, 0)
    
    def test_numeric_input(self):
        """测试数字输入"""
        hll = HyperLogLog(precision=10)
        hll.add(12345)
        hll.add(3.14)
        
        estimate = hll.count()
        self.assertGreater(estimate, 0)
    
    def test_unicode_input(self):
        """测试 Unicode 输入"""
        hll = HyperLogLog(precision=10)
        
        unicode_strings = [
            "中文测试",
            "日本語",
            "한국어",
            "العربية",
            "תירבע",
        ]
        
        for s in unicode_strings:
            hll.add(s)
        
        estimate = hll.count()
        self.assertGreater(estimate, 4)
    
    def test_very_large_dataset(self):
        """测试大数据集"""
        hll = HyperLogLog(precision=16)
        
        # 添加 100 万模拟元素（实际只添加部分）
        for i in range(100000):
            hll.add(f"large_{i}")
        
        estimate = hll.count()
        error = abs(estimate - 100000) / 100000
        
        # precision=16 应该有很小的误差
        self.assertLess(error, 0.01)


class TestStress(unittest.TestCase):
    """压力测试"""
    
    def test_many_adds(self):
        """测试大量添加"""
        hll = HyperLogLog(precision=12)
        
        # 添加 50000 个随机字符串
        for i in range(50000):
            hll.add(''.join(random.choices(string.ascii_letters, k=10)))
        
        estimate = hll.count()
        
        # 应该接近 50000（因为是随机字符串，重复很少）
        self.assertGreater(estimate, 45000)
        self.assertLess(estimate, 55000)
    
    def test_serialization_stress(self):
        """测试序列化压力"""
        hll = HyperLogLog(precision=14)
        
        for i in range(10000):
            hll.add(f"stress_{i}")
        
        # 多次序列化和反序列化
        for _ in range(10):
            data = hll.to_bytes()
            hll = HyperLogLog.from_bytes(data)
        
        estimate = hll.count()
        self.assertGreater(estimate, 9000)


def run_tests():
    """运行所有测试"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加所有测试类
    test_classes = [
        TestHashFunctions,
        TestLeadingZeros,
        TestHyperLogLog,
        TestHyperLogLogSerialization,
        TestHyperLogLogMerge,
        TestHyperLogLogSetOperations,
        TestHyperLogLogPlusPlus,
        TestSparseHyperLogLog,
        TestUtilityFunctions,
        TestBuilder,
        TestEdgeCases,
        TestStress,
    ]
    
    for test_class in test_classes:
        suite.addTests(loader.loadTestsFromTestCase(test_class))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


if __name__ == '__main__':
    result = run_tests()
    
    # 输出总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    print(f"运行测试: {result.testsRun}")
    print(f"成功: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"失败: {len(result.failures)}")
    print(f"错误: {len(result.errors)}")
    
    if result.failures:
        print("\n失败的测试:")
        for test, traceback in result.failures:
            print(f"  - {test}")
    
    if result.errors:
        print("\n出错的测试:")
        for test, traceback in result.errors:
            print(f"  - {test}")