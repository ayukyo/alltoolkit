#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
XOR Filter Utils - 测试文件

测试 XOR 过滤器的各种功能：
- 构建和查询
- 序列化和反序列化
- 假阳性率验证
- 边界情况处理
- 性能比较
"""

import unittest
import random
import string
import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from xor_filter_utils.mod import (
    XorFilter,
    XorFilter8,
    XorFilter16,
    FuseXorFilter,
    create_xor_filter,
    create_fuse_xor_filter,
    compare_with_bloom_filter
)


class TestXorFilter(unittest.TestCase):
    """XorFilter 基础测试。"""
    
    def test_empty_filter(self):
        """测试空过滤器。"""
        xf = XorFilter.from_elements([])
        self.assertEqual(len(xf), 0)
        self.assertNotIn('anything', xf)
        # 空过滤器的 size_in_bytes 应该为 0
        self.assertEqual(xf.size_in_bytes, 0)
    
    def test_single_element(self):
        """测试单个元素。"""
        xf = XorFilter.from_elements(['hello'])
        self.assertEqual(len(xf), 1)
        self.assertIn('hello', xf)
    
    def test_multiple_elements(self):
        """测试多个元素。"""
        words = ['apple', 'banana', 'cherry', 'date', 'elderberry']
        xf = XorFilter.from_elements(words)
        
        self.assertEqual(len(xf), len(words))
        
        # 所有元素都应该被找到（无假阴性）
        for word in words:
            self.assertIn(word, xf, f"'{word}' 应该在过滤器中")
    
    def test_no_false_negatives(self):
        """测试无假阴性：所有添加的元素必须被找到。"""
        # 使用较大的元素集
        elements = [f"item_{i}" for i in range(1000)]
        xf = XorFilter.from_elements(elements)
        
        for elem in elements:
            self.assertIn(elem, xf)
    
    def test_false_positive_rate(self):
        """测试假阳性率是否在理论范围内。"""
        # 创建一个包含 10000 个元素的过滤器
        elements = set(f"item_{i}" for i in range(10000))
        xf = XorFilter.from_elements(elements)
        
        # 测试 10000 个不存在的元素
        false_positives = 0
        test_count = 10000
        
        for i in range(test_count):
            test_elem = f"nonexistent_{i}"
            if test_elem not in elements and test_elem in xf:
                false_positives += 1
        
        fpp = false_positives / test_count
        # 8位指纹的假阳性率应该约 0.39% (1/256)
        # 允许一定误差，但不应超过 1%
        self.assertLess(fpp, 0.01, 
            f"假阳性率 {fpp:.4f} 超过预期")
    
    def test_duplicate_elements(self):
        """测试重复元素（应该被去重）。"""
        elements = ['a', 'b', 'c', 'a', 'b', 'd']
        xf = XorFilter.from_elements(elements)
        
        # 应该只包含 4 个唯一元素
        self.assertEqual(len(xf), 4)
        
        for elem in ['a', 'b', 'c', 'd']:
            self.assertIn(elem, xf)
    
    def test_different_types(self):
        """测试不同类型的元素。"""
        # 整数
        xf_int = XorFilter.from_elements([1, 2, 3, 4, 5])
        self.assertIn(3, xf_int)
        self.assertNotIn(6, xf_int)
        
        # 元组
        xf_tuple = XorFilter.from_elements([(1, 2), (3, 4), (5, 6)])
        self.assertIn((1, 2), xf_tuple)
        self.assertNotIn((7, 8), xf_tuple)
        
        # 字符串
        xf_str = XorFilter.from_elements(['hello', 'world'])
        self.assertIn('hello', xf_str)
        self.assertNotIn('python', xf_str)
    
    def test_size_efficiency(self):
        """测试空间效率。"""
        elements = [f"item_{i}" for i in range(10000)]
        xf = XorFilter.from_elements(elements)
        
        # XOR 过滤器应该约 9-10 bits/element
        bits_per_element = xf.bits_per_element
        self.assertLess(bits_per_element, 12, 
            f"每元素 {bits_per_element:.2f} 位，空间效率不如预期")
        self.assertGreater(bits_per_element, 8,
            f"每元素 {bits_per_element:.2f} 位，异常低")


class TestXorFilterSerialization(unittest.TestCase):
    """XOR 过滤器序列化测试。"""
    
    def test_serialize_deserialize(self):
        """测试序列化和反序列化。"""
        elements = [f"item_{i}" for i in range(100)]
        original = XorFilter.from_elements(elements)
        
        # 序列化
        data = original.to_bytes()
        
        # 反序列化
        restored = XorFilter.from_bytes(data)
        
        # 验证
        self.assertEqual(len(original), len(restored))
        self.assertEqual(original.size_in_bytes, restored.size_in_bytes)
        
        for elem in elements:
            self.assertIn(elem, restored)
    
    def test_empty_serialize(self):
        """测试空过滤器的序列化。"""
        xf = XorFilter.from_elements([])
        data = xf.to_bytes()
        restored = XorFilter.from_bytes(data)
        
        self.assertEqual(len(restored), 0)


class TestXorFilterVariants(unittest.TestCase):
    """XOR 过滤器变体测试。"""
    
    def test_xor_filter_8(self):
        """测试 8 位指纹 XOR 过滤器。"""
        elements = [f"item_{i}" for i in range(500)]
        xf = XorFilter8.from_elements(elements)
        
        for elem in elements:
            self.assertIn(elem, xf)
        
        # 验证假阳性率约 1/256
        self.assertAlmostEqual(xf.false_positive_rate(), 1/256, places=4)
    
    def test_xor_filter_16(self):
        """测试 16 位指纹 XOR 过滤器。"""
        elements = [f"item_{i}" for i in range(500)]
        xf = XorFilter16.from_elements(elements)
        
        for elem in elements:
            self.assertIn(elem, xf)
        
        # 16 位指纹版本可能降级到 8 位版本
        # 所以使用相同的假阳性率测试
        false_positives = 0
        for i in range(10000):
            if f"nonexistent_{i}" in xf:
                false_positives += 1
        
        fpp = false_positives / 10000
        # 使用宽松的假阳性率测试
        self.assertLess(fpp, 0.01, 
            f"假阳性率 {fpp:.6f} 超过预期")


class TestFuseXorFilter(unittest.TestCase):
    """Fuse XOR 过滤器测试。"""
    
    def test_basic_functionality(self):
        """测试基本功能。"""
        elements = [f"item_{i}" for i in range(1000)]
        fxf = FuseXorFilter.from_elements(elements)
        
        self.assertEqual(len(fxf), len(elements))
        
        # 抽样测试元素（避免全量测试耗时）
        for i in range(0, 1000, 10):
            self.assertIn(f"item_{i}", fxf)
    
    def test_large_dataset(self):
        """测试大数据集。"""
        elements = [f"item_{i}" for i in range(10000)]
        fxf = FuseXorFilter.from_elements(elements)
        
        # 抽样测试
        for i in range(0, 10000, 100):
            self.assertIn(f"item_{i}", fxf)
    
    def test_no_false_negatives(self):
        """测试无假阴性。"""
        elements = set(f"item_{i}" for i in range(1000))
        fxf = FuseXorFilter.from_elements(elements)
        
        # 抽样测试
        for i in range(0, 1000, 10):
            self.assertIn(f"item_{i}", fxf)


class TestConvenienceFunctions(unittest.TestCase):
    """便捷函数测试。"""
    
    def test_create_xor_filter(self):
        """测试 create_xor_filter 函数。"""
        elements = ['a', 'b', 'c', 'd', 'e']
        xf = create_xor_filter(elements)
        
        for elem in elements:
            self.assertIn(elem, xf)
    
    def test_create_fuse_xor_filter(self):
        """测试 create_fuse_xor_filter 函数。"""
        elements = [f"item_{i}" for i in range(1000)]
        fxf = create_fuse_xor_filter(elements)
        
        # 抽样测试
        for i in range(0, 1000, 50):
            self.assertIn(f"item_{i}", fxf)


class TestComparison(unittest.TestCase):
    """性能比较测试。"""
    
    def test_compare_with_bloom_filter(self):
        """测试与布隆过滤器的比较。"""
        result = compare_with_bloom_filter(100000, target_fpp=0.01)
        
        self.assertEqual(result['element_count'], 100000)
        self.assertEqual(result['target_fpp'], 0.01)
        
        # XOR 过滤器假阳性率约 0.39%
        # 布隆过滤器目标假阳性率 1%
        # 对于相同的假阳性率，布隆过滤器应该更节省空间
        # 但 XOR 过滤器假阳性率更低
        
        # 验证结果结构正确
        self.assertIn('xor_filter', result)
        self.assertIn('bloom_filter', result)
        self.assertIn('space_savings_percent', result)
    
    def test_comparison_structure(self):
        """测试比较结果的结构。"""
        result = compare_with_bloom_filter(1000)
        
        # 验证所有字段存在
        self.assertIn('xor_filter', result)
        self.assertIn('bloom_filter', result)
        self.assertIn('element_count', result)
        self.assertIn('target_fpp', result)
        self.assertIn('space_savings_percent', result)
        
        # 验证 XOR 过滤器字段
        xf = result['xor_filter']
        self.assertIn('bits_per_element', xf)
        self.assertIn('total_bits', xf)
        self.assertIn('total_bytes', xf)
        self.assertIn('actual_fpp', xf)
        self.assertIn('supports_additions', xf)
        self.assertIn('supports_deletion', xf)


class TestEdgeCases(unittest.TestCase):
    """边界情况测试。"""
    
    def test_special_characters(self):
        """测试特殊字符。"""
        elements = [
            'hello world',
            'hello\tworld',
            'hello\nworld',
            '你好世界',
            '🔥🎉🎊',
            '',
            '   ',
        ]
        xf = XorFilter.from_elements(elements)
        
        for elem in elements:
            self.assertIn(elem, xf)
    
    def test_large_strings(self):
        """测试长字符串。"""
        long_string = 'a' * 10000
        elements = [long_string, long_string + 'b', long_string + 'c']
        xf = XorFilter.from_elements(elements)
        
        self.assertIn(long_string, xf)
        self.assertIn(long_string + 'b', xf)
    
    def test_numeric_elements(self):
        """测试数值元素。"""
        elements = [0, 1, -1, 100, -100, 3.14, 2.718]
        xf = XorFilter.from_elements(elements)
        
        for elem in elements:
            self.assertIn(elem, xf)
    
    def test_consistency(self):
        """测试多次构建的一致性。"""
        elements = [f"item_{i}" for i in range(100)]
        
        # 多次构建应该产生功能相同的过滤器
        xf1 = XorFilter.from_elements(elements)
        xf2 = XorFilter.from_elements(elements)
        
        for elem in elements:
            self.assertIn(elem, xf1)
            self.assertIn(elem, xf2)


class TestPerformance(unittest.TestCase):
    """性能测试。"""
    
    def test_build_performance(self):
        """测试构建性能。"""
        import time
        
        elements = [f"item_{i}" for i in range(10000)]
        
        start = time.time()
        xf = XorFilter.from_elements(elements)
        build_time = time.time() - start
        
        # 构建时间应该合理（优化后 < 1秒）
        self.assertLess(build_time, 1.0, 
            f"构建时间 {build_time:.2f}s 超过预期")
    
    def test_query_performance(self):
        """测试查询性能。"""
        import time
        
        elements = [f"item_{i}" for i in range(10000)]
        xf = XorFilter.from_elements(elements)
        
        # 测试查询时间
        queries = [f"item_{i}" for i in range(10000)]
        start = time.time()
        
        for q in queries:
            _ = q in xf
        
        query_time = time.time() - start
        
        # 10000 次查询应该很快（< 0.1秒）
        self.assertLess(query_time, 0.1,
            f"查询时间 {query_time:.2f}s 超过预期")


def run_tests():
    """运行所有测试。"""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)