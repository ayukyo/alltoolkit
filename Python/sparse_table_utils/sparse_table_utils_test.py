#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sparse Table Utils 测试套件
===========================

全面测试稀疏表工具库的所有功能。

作者: AllToolkit 自动化生成
日期: 2026-05-26
"""

import sys
import os
import unittest
import random
import math

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    SparseTable, SparseTable2D, PrefixSumTable,
    SparseTableBuilder, OperationType, RangeInfo,
    build_min_sparse_table, build_max_sparse_table, build_gcd_sparse_table,
    range_min, range_max, range_gcd, batch_queries,
    _gcd, _lcm, _bit_length
)


class TestUtilityFunctions(unittest.TestCase):
    """测试工具函数"""
    
    def test_gcd(self):
        """测试 GCD 计算"""
        self.assertEqual(_gcd(12, 18), 6)
        self.assertEqual(_gcd(17, 13), 1)
        self.assertEqual(_gcd(100, 25), 25)
        self.assertEqual(_gcd(0, 5), 5)
        self.assertEqual(_gcd(5, 0), 5)
        self.assertEqual(_gcd(-12, 18), 6)
        self.assertEqual(_gcd(12, -18), 6)
        self.assertEqual(_gcd(-12, -18), 6)
    
    def test_lcm(self):
        """测试 LCM 计算"""
        self.assertEqual(_lcm(12, 18), 36)
        self.assertEqual(_lcm(4, 5), 20)
        self.assertEqual(_lcm(7, 13), 91)
        self.assertEqual(_lcm(0, 5), 0)
        self.assertEqual(_lcm(5, 0), 0)
        self.assertEqual(_lcm(-12, 18), 36)
    
    def test_bit_length(self):
        """测试二进制位数计算"""
        self.assertEqual(_bit_length(0), 0)
        self.assertEqual(_bit_length(1), 1)
        self.assertEqual(_bit_length(2), 2)
        self.assertEqual(_bit_length(3), 2)
        self.assertEqual(_bit_length(4), 3)
        self.assertEqual(_bit_length(7), 3)
        self.assertEqual(_bit_length(8), 4)
        self.assertEqual(_bit_length(15), 4)
        self.assertEqual(_bit_length(16), 5)


class TestSparseTableMin(unittest.TestCase):
    """测试稀疏表最小值功能"""
    
    def setUp(self):
        """测试前准备"""
        self.data = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
        self.st = SparseTable(self.data, OperationType.MIN)
    
    def test_basic_query(self):
        """测试基本查询"""
        self.assertEqual(self.st.query(0, 10), 1)
        self.assertEqual(self.st.query(0, 3), 1)
        self.assertEqual(self.st.query(4, 6), 2)  # min(5, 9, 2) = 2
        self.assertEqual(self.st.query(6, 6), 2)
    
    def test_single_element(self):
        """测试单元素查询"""
        for i in range(len(self.data)):
            self.assertEqual(self.st.query(i, i), self.data[i])
    
    def test_entire_range(self):
        """测试整个范围查询"""
        self.assertEqual(self.st.query(0, len(self.data) - 1), min(self.data))
    
    def test_range_min_method(self):
        """测试 range_min 便捷方法"""
        self.assertEqual(self.st.range_min(0, 3), 1)
        self.assertEqual(self.st.range_min(4, 8), 2)
    
    def test_invalid_range(self):
        """测试无效范围"""
        with self.assertRaises(ValueError):
            self.st.query(-1, 5)
        with self.assertRaises(ValueError):
            self.st.query(5, 3)  # left > right
    
    def test_empty_data(self):
        """测试空数据"""
        st = SparseTable([], OperationType.MIN)
        self.assertEqual(len(st), 0)
        with self.assertRaises(ValueError):
            st.query(0, 0)
    
    def test_len(self):
        """测试长度"""
        self.assertEqual(len(self.st), len(self.data))
    
    def test_getitem(self):
        """测试索引访问"""
        for i, v in enumerate(self.data):
            self.assertEqual(self.st[i], v)
    
    def test_data_property(self):
        """测试数据属性"""
        self.assertEqual(self.st.data, self.data)
        # 确保是副本
        self.st.data[0] = 100
        self.assertEqual(self.st._data[0], 3)
    
    def test_op_type_property(self):
        """测试操作类型属性"""
        self.assertEqual(self.st.op_type, OperationType.MIN)


class TestSparseTableMax(unittest.TestCase):
    """测试稀疏表最大值功能"""
    
    def setUp(self):
        self.data = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
        self.st = SparseTable(self.data, OperationType.MAX)
    
    def test_basic_query(self):
        """测试基本查询"""
        self.assertEqual(self.st.query(0, 10), 9)
        self.assertEqual(self.st.query(0, 3), 4)
        self.assertEqual(self.st.query(4, 6), 9)
        self.assertEqual(self.st.query(6, 8), 6)
    
    def test_range_max_method(self):
        """测试 range_max 便捷方法"""
        self.assertEqual(self.st.range_max(0, 10), 9)
    
    def test_range_max_wrong_type(self):
        """测试错误类型调用"""
        st_min = SparseTable(self.data, OperationType.MIN)
        with self.assertRaises(ValueError):
            st_min.range_max(0, 5)


class TestSparseTableGCD(unittest.TestCase):
    """测试稀疏表 GCD 功能"""
    
    def setUp(self):
        self.data = [12, 18, 24, 36, 60, 90]
        self.st = SparseTable(self.data, OperationType.GCD)
    
    def test_basic_query(self):
        """测试基本 GCD 查询"""
        self.assertEqual(self.st.query(0, 5), 6)
        self.assertEqual(self.st.query(0, 2), 6)  # gcd(12, 18, 24) = 6
        self.assertEqual(self.st.query(2, 4), 12)  # gcd(24, 36, 60) = 12
    
    def test_single_element(self):
        """测试单元素 GCD"""
        for i, v in enumerate(self.data):
            self.assertEqual(self.st.query(i, i), v)
    
    def test_range_gcd_method(self):
        """测试 range_gcd 便捷方法"""
        self.assertEqual(self.st.range_gcd(0, 5), 6)


class TestSparseTableLCM(unittest.TestCase):
    """测试稀疏表 LCM 功能"""
    
    def setUp(self):
        self.data = [2, 3, 4, 5]
        self.st = SparseTable(self.data, OperationType.LCM)
    
    def test_basic_query(self):
        """测试基本 LCM 查询"""
        self.assertEqual(self.st.query(0, 3), 60)  # lcm(2,3,4,5) = 60
        self.assertEqual(self.st.query(0, 1), 6)   # lcm(2,3) = 6
        self.assertEqual(self.st.query(2, 3), 20)   # lcm(4,5) = 20


class TestSparseTableBitwise(unittest.TestCase):
    """测试稀疏表位运算功能"""
    
    def test_and_operation(self):
        """测试 AND 运算"""
        data = [15, 7, 3, 1]
        st = SparseTable(data, OperationType.AND)
        self.assertEqual(st.query(0, 3), 15 & 7 & 3 & 1)
        self.assertEqual(st.query(0, 1), 15 & 7)
    
    def test_or_operation(self):
        """测试 OR 运算"""
        data = [1, 2, 4, 8]
        st = SparseTable(data, OperationType.OR)
        self.assertEqual(st.query(0, 3), 15)  # 1 | 2 | 4 | 8 = 15


class TestSparseTableLargeData(unittest.TestCase):
    """测试大数据量"""
    
    def test_large_random(self):
        """测试大规模随机数据"""
        n = 10000
        data = [random.randint(1, 1000000) for _ in range(n)]
        st = SparseTable(data, OperationType.MIN)
        
        # 随机测试 100 个查询
        for _ in range(100):
            left = random.randint(0, n - 1)
            right = random.randint(left, n - 1)
            expected = min(data[left:right + 1])
            self.assertEqual(st.query(left, right), expected)
    
    def test_large_max(self):
        """测试大规模最大值查询"""
        n = 5000
        data = [random.randint(1, 1000000) for _ in range(n)]
        st = SparseTable(data, OperationType.MAX)
        
        for _ in range(50):
            left = random.randint(0, n - 1)
            right = random.randint(left, n - 1)
            expected = max(data[left:right + 1])
            self.assertEqual(st.query(left, right), expected)


class TestSparseTable2D(unittest.TestCase):
    """测试二维稀疏表"""
    
    def setUp(self):
        self.matrix = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 16]
        ]
        self.st_min = SparseTable2D(self.matrix, OperationType.MIN)
        self.st_max = SparseTable2D(self.matrix, OperationType.MAX)
    
    def test_basic_min_query(self):
        """测试基本最小值查询"""
        self.assertEqual(self.st_min.query(0, 0, 3, 3), 1)
        self.assertEqual(self.st_min.query(0, 0, 1, 1), 1)
        self.assertEqual(self.st_min.query(2, 2, 3, 3), 11)
    
    def test_basic_max_query(self):
        """测试基本最大值查询"""
        self.assertEqual(self.st_max.query(0, 0, 3, 3), 16)
        self.assertEqual(self.st_max.query(0, 0, 1, 1), 6)
        self.assertEqual(self.st_max.query(1, 1, 2, 2), 11)
    
    def test_single_element(self):
        """测试单元素查询"""
        for r in range(4):
            for c in range(4):
                self.assertEqual(self.st_min.query(r, c, r, c), self.matrix[r][c])
                self.assertEqual(self.st_max.query(r, c, r, c), self.matrix[r][c])
    
    def test_properties(self):
        """测试属性"""
        self.assertEqual(self.st_min.rows, 4)
        self.assertEqual(self.st_min.cols, 4)
    
    def test_empty_matrix(self):
        """测试空矩阵"""
        st = SparseTable2D([], OperationType.MIN)
        self.assertEqual(st.rows, 0)
        self.assertEqual(st.cols, 0)
    
    def test_invalid_range(self):
        """测试无效范围"""
        with self.assertRaises(ValueError):
            self.st_min.query(-1, 0, 2, 2)
        with self.assertRaises(ValueError):
            self.st_min.query(0, 0, 5, 2)


class TestPrefixSumTable(unittest.TestCase):
    """测试前缀和表"""
    
    def test_sum_operation(self):
        """测试求和操作"""
        data = [1, 2, 3, 4, 5]
        st = PrefixSumTable(data, lambda a, b: a + b, 0, lambda a, b: a - b)
        
        self.assertEqual(st.query(0, 4), 15)
        self.assertEqual(st.query(1, 3), 9)  # 2 + 3 + 4 = 9
        self.assertEqual(st.query(2, 2), 3)
    
    def test_product_operation(self):
        """测试乘积操作"""
        data = [1, 2, 3, 4, 5]
        # 乘积没有简单的逆操作
        st = PrefixSumTable(data, lambda a, b: a * b, 1)
        
        self.assertEqual(st.query(0, 4), 120)
        self.assertEqual(st.query(1, 3), 24)  # 2 * 3 * 4 = 24
    
    def test_xor_operation(self):
        """测试 XOR 操作"""
        data = [1, 2, 3, 4]
        # XOR 的逆操作是 XOR 本身
        st = PrefixSumTable(data, lambda a, b: a ^ b, 0, lambda a, b: a ^ b)
        self.assertEqual(st.query(0, 3), 1 ^ 2 ^ 3 ^ 4)  # = 4
    
    def test_single_element(self):
        """测试单元素"""
        data = [42]
        st = PrefixSumTable(data, lambda a, b: a + b, 0, lambda a, b: a - b)
        self.assertEqual(st.query(0, 0), 42)
    
    def test_empty_data(self):
        """测试空数据"""
        st = PrefixSumTable([], lambda a, b: a + b, 0)
        self.assertEqual(len(st), 0)
        with self.assertRaises(ValueError):
            st.query(0, 0)
    
    def test_large_sum(self):
        """测试大规模求和"""
        n = 100
        data = list(range(1, n + 1))
        st = PrefixSumTable(data, lambda a, b: a + b, 0, lambda a, b: a - b)
        
        expected = sum(data)
        self.assertEqual(st.query(0, n - 1), expected)
        
        # 随机测试
        for _ in range(20):
            left = random.randint(0, n - 1)
            right = random.randint(left, n - 1)
            expected = sum(data[left:right + 1])
            self.assertEqual(st.query(left, right), expected)
    
    def test_prefix_query(self):
        """测试前缀查询"""
        data = [1, 2, 3, 4, 5]
        st = PrefixSumTable(data, lambda a, b: a + b, 0)
        
        self.assertEqual(st.prefix_query(0), 1)
        self.assertEqual(st.prefix_query(2), 6)
        self.assertEqual(st.prefix_query(4), 15)


class TestSparseTableBuilder(unittest.TestCase):
    """测试构建器模式"""
    
    def test_builder_min(self):
        """测试构建最小值表"""
        st = (SparseTableBuilder()
              .with_data([5, 2, 8, 1, 9, 3])
              .for_min()
              .build())
        self.assertEqual(st.query(0, 5), 1)
    
    def test_builder_max(self):
        """测试构建最大值表"""
        st = (SparseTableBuilder()
              .with_data([5, 2, 8, 1, 9, 3])
              .for_max()
              .build())
        self.assertEqual(st.query(0, 5), 9)
    
    def test_builder_gcd(self):
        """测试构建 GCD 表"""
        st = (SparseTableBuilder()
              .with_data([12, 18, 24, 36])
              .for_gcd()
              .build())
        self.assertEqual(st.query(0, 3), 6)
    
    def test_builder_lcm(self):
        """测试构建 LCM 表"""
        st = (SparseTableBuilder()
              .with_data([2, 3, 4, 5])
              .for_lcm()
              .build())
        self.assertEqual(st.query(0, 3), 60)


class TestConvenienceFunctions(unittest.TestCase):
    """测试便捷函数"""
    
    def test_build_min_sparse_table(self):
        """测试构建最小值表"""
        st = build_min_sparse_table([3, 1, 4, 1, 5])
        self.assertEqual(st.query(0, 4), 1)
    
    def test_build_max_sparse_table(self):
        """测试构建最大值表"""
        st = build_max_sparse_table([3, 1, 4, 1, 5])
        self.assertEqual(st.query(0, 4), 5)
    
    def test_build_gcd_sparse_table(self):
        """测试构建 GCD 表"""
        st = build_gcd_sparse_table([12, 18, 24])
        self.assertEqual(st.query(0, 2), 6)
    
    def test_range_min(self):
        """测试一次性最小值查询"""
        self.assertEqual(range_min([3, 1, 4, 1, 5], 0, 4), 1)
        self.assertEqual(range_min([5, 4, 3, 2, 1], 0, 4), 1)
    
    def test_range_max(self):
        """测试一次性最大值查询"""
        self.assertEqual(range_max([3, 1, 4, 1, 5], 0, 4), 5)
        self.assertEqual(range_max([1, 2, 3, 4, 5], 0, 4), 5)
    
    def test_range_gcd(self):
        """测试一次性 GCD 查询"""
        self.assertEqual(range_gcd([12, 18, 24], 0, 2), 6)
    
    def test_batch_queries(self):
        """测试批量查询"""
        data = [3, 1, 4, 1, 5, 9, 2, 6]
        queries = [(0, 3), (2, 5), (4, 7)]
        results = batch_queries(data, queries, OperationType.MIN)
        self.assertEqual(results, [1, 1, 2])


class TestSerialization(unittest.TestCase):
    """测试序列化"""
    
    def test_to_dict(self):
        """测试转换为字典"""
        st = SparseTable([3, 1, 4, 1, 5], OperationType.MIN)
        d = st.to_dict()
        
        self.assertEqual(d['data'], [3, 1, 4, 1, 5])
        self.assertEqual(d['op_type'], 'min')
        self.assertEqual(d['n'], 5)
    
    def test_from_dict(self):
        """测试从字典创建"""
        d = {
            'data': [3, 1, 4, 1, 5],
            'op_type': 'min',
            'n': 5
        }
        st = SparseTable.from_dict(d)
        self.assertEqual(st.query(0, 4), 1)
        self.assertEqual(st.op_type, OperationType.MIN)


class TestEdgeCases(unittest.TestCase):
    """测试边界情况"""
    
    def test_two_elements(self):
        """测试两个元素"""
        st = SparseTable([5, 3], OperationType.MIN)
        self.assertEqual(st.query(0, 1), 3)
        self.assertEqual(st.query(0, 0), 5)
        self.assertEqual(st.query(1, 1), 3)
    
    def test_all_same(self):
        """测试所有元素相同"""
        data = [5] * 100
        st = SparseTable(data, OperationType.MIN)
        for _ in range(10):
            left = random.randint(0, 99)
            right = random.randint(left, 99)
            self.assertEqual(st.query(left, right), 5)
    
    def test_negative_numbers(self):
        """测试负数"""
        data = [-3, -1, -4, -1, -5, -9]
        st_min = SparseTable(data, OperationType.MIN)
        st_max = SparseTable(data, OperationType.MAX)
        
        self.assertEqual(st_min.query(0, 5), -9)
        self.assertEqual(st_max.query(0, 5), -1)
    
    def test_mixed_positive_negative(self):
        """测试正负混合"""
        data = [-5, 3, -2, 8, -1]
        st_min = SparseTable(data, OperationType.MIN)
        st_max = SparseTable(data, OperationType.MAX)
        
        self.assertEqual(st_min.query(0, 4), -5)
        self.assertEqual(st_max.query(0, 4), 8)
    
    def test_large_values(self):
        """测试大数值"""
        data = [10**15, 2 * 10**15, 3 * 10**15]
        st = SparseTable(data, OperationType.MIN)
        self.assertEqual(st.query(0, 2), 10**15)


class TestCorrectnessAgainstNaive(unittest.TestCase):
    """对比朴素算法的正确性测试"""
    
    def test_random_correctness(self):
        """随机正确性测试"""
        for _ in range(10):
            n = random.randint(10, 100)
            data = [random.randint(-1000, 1000) for _ in range(n)]
            
            # 测试最小值
            st_min = SparseTable(data, OperationType.MIN)
            for _ in range(20):
                left = random.randint(0, n - 1)
                right = random.randint(left, n - 1)
                expected = min(data[left:right + 1])
                self.assertEqual(st_min.query(left, right), expected)
            
            # 测试最大值
            st_max = SparseTable(data, OperationType.MAX)
            for _ in range(20):
                left = random.randint(0, n - 1)
                right = random.randint(left, n - 1)
                expected = max(data[left:right + 1])
                self.assertEqual(st_max.query(left, right), expected)
            
            # 测试 GCD
            positive_data = [abs(x) or 1 for x in data]  # 确保 GCD 数据为正
            st_gcd = SparseTable(positive_data, OperationType.GCD)
            for _ in range(20):
                left = random.randint(0, n - 1)
                right = random.randint(left, n - 1)
                expected = positive_data[left]
                for i in range(left + 1, right + 1):
                    expected = math.gcd(expected, positive_data[i])
                self.assertEqual(st_gcd.query(left, right), expected)


def run_tests():
    """运行所有测试"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加所有测试类
    test_classes = [
        TestUtilityFunctions,
        TestSparseTableMin,
        TestSparseTableMax,
        TestSparseTableGCD,
        TestSparseTableLCM,
        TestSparseTableBitwise,
        TestSparseTableLargeData,
        TestSparseTable2D,
        TestPrefixSumTable,
        TestSparseTableBuilder,
        TestConvenienceFunctions,
        TestSerialization,
        TestEdgeCases,
        TestCorrectnessAgainstNaive,
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


if __name__ == "__main__":
    result = run_tests()
    sys.exit(0 if result.wasSuccessful() else 1)