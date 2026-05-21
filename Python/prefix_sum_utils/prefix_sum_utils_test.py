#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
前缀和与差分数组工具模块测试

测试用例覆盖：
- 一维前缀和的构建和查询
- 二维前缀和的构建和查询
- 一维差分数组的更新和还原
- 二维差分数组的更新和还原
- 边界条件和异常处理
"""

import unittest
import random
from mod import (
    PrefixSum,
    PrefixSum2D,
    DifferenceArray,
    DifferenceArray2D,
    PrefixSumError,
    DifferenceArrayError,
    build_prefix_sum,
    range_sum,
    build_difference_array,
    restore_from_difference,
)


class TestPrefixSum(unittest.TestCase):
    """一维前缀和测试"""
    
    def test_basic_construction(self):
        """测试基本构建"""
        arr = [1, 2, 3, 4, 5]
        ps = PrefixSum(arr)
        
        self.assertEqual(ps.length, 5)
        self.assertEqual(ps.total(), 15)
        self.assertEqual(ps.original, arr)
        self.assertEqual(ps.prefix_array, [0, 1, 3, 6, 10, 15])
    
    def test_range_sum(self):
        """测试区间求和"""
        arr = [1, 2, 3, 4, 5]
        ps = PrefixSum(arr)
        
        self.assertEqual(ps.range_sum(0, 0), 1)
        self.assertEqual(ps.range_sum(0, 2), 6)  # 1+2+3
        self.assertEqual(ps.range_sum(1, 3), 9)  # 2+3+4
        self.assertEqual(ps.range_sum(0, 4), 15)  # 全部
        self.assertEqual(ps.range_sum(2, 2), 3)  # 单点
    
    def test_prefix_sum(self):
        """测试前缀和"""
        arr = [1, 2, 3, 4, 5]
        ps = PrefixSum(arr)
        
        self.assertEqual(ps.prefix_sum(0), 1)
        self.assertEqual(ps.prefix_sum(1), 3)  # 1+2
        self.assertEqual(ps.prefix_sum(2), 6)  # 1+2+3
        self.assertEqual(ps.prefix_sum(3), 10)  # 1+2+3+4
        self.assertEqual(ps.prefix_sum(4), 15)  # 全部
    
    def test_empty_array(self):
        """测试空数组"""
        ps = PrefixSum([])
        self.assertEqual(ps.length, 0)
        self.assertEqual(ps.total(), 0)
        self.assertEqual(ps.original, [])
        self.assertEqual(ps.prefix_array, [0])
    
    def test_negative_numbers(self):
        """测试负数"""
        arr = [1, -2, 3, -4, 5]
        ps = PrefixSum(arr)
        
        self.assertEqual(ps.range_sum(0, 2), 2)  # 1+(-2)+3
        self.assertEqual(ps.range_sum(1, 3), -3)  # -2+3+(-4)
        self.assertEqual(ps.total(), 3)
    
    def test_floats(self):
        """测试浮点数"""
        arr = [1.5, 2.5, 3.5, 4.5]
        ps = PrefixSum(arr)
        
        self.assertAlmostEqual(ps.range_sum(0, 1), 4.0)
        self.assertAlmostEqual(ps.total(), 12.0)
    
    def test_index_out_of_bounds(self):
        """测试索引越界"""
        arr = [1, 2, 3]
        ps = PrefixSum(arr)
        
        with self.assertRaises(PrefixSumError):
            ps.prefix_sum(-1)
        
        with self.assertRaises(PrefixSumError):
            ps.prefix_sum(3)
        
        with self.assertRaises(PrefixSumError):
            ps.range_sum(-1, 2)
        
        with self.assertRaises(PrefixSumError):
            ps.range_sum(0, 3)
    
    def test_invalid_range(self):
        """测试无效区间"""
        arr = [1, 2, 3]
        ps = PrefixSum(arr)
        
        with self.assertRaises(PrefixSumError):
            ps.range_sum(2, 1)  # left > right
    
    def test_getitem(self):
        """测试索引访问"""
        arr = [1, 2, 3, 4, 5]
        ps = PrefixSum(arr)
        
        self.assertEqual(ps[0], 1)
        self.assertEqual(ps[2], 3)
        self.assertEqual(ps[4], 5)
    
    def test_to_dict_and_from_dict(self):
        """测试序列化和反序列化"""
        arr = [1, 2, 3, 4, 5]
        ps1 = PrefixSum(arr)
        
        data = ps1.to_dict()
        ps2 = PrefixSum.from_dict(data)
        
        self.assertEqual(ps1.range_sum(0, 4), ps2.range_sum(0, 4))
        self.assertEqual(ps1.original, ps2.original)


class TestPrefixSum2D(unittest.TestCase):
    """二维前缀和测试"""
    
    def test_basic_construction(self):
        """测试基本构建"""
        matrix = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]
        ps2d = PrefixSum2D(matrix)
        
        self.assertEqual(ps2d.rows, 3)
        self.assertEqual(ps2d.cols, 3)
        self.assertEqual(ps2d.shape, (3, 3))
        self.assertEqual(ps2d.total(), 45)
    
    def test_region_sum(self):
        """测试区域求和"""
        matrix = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]
        ps2d = PrefixSum2D(matrix)
        
        # 左上角 2x2
        self.assertEqual(ps2d.region_sum(0, 0, 1, 1), 12)  # 1+2+4+5
        
        # 右下角 2x2
        self.assertEqual(ps2d.region_sum(1, 1, 2, 2), 28)  # 5+6+8+9
        
        # 单点
        self.assertEqual(ps2d.region_sum(1, 1, 1, 1), 5)
        
        # 第一行
        self.assertEqual(ps2d.region_sum(0, 0, 0, 2), 6)  # 1+2+3
        
        # 第一列
        self.assertEqual(ps2d.region_sum(0, 0, 2, 0), 12)  # 1+4+7
    
    def test_prefix_sum(self):
        """测试前缀和"""
        matrix = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]
        ps2d = PrefixSum2D(matrix)
        
        self.assertEqual(ps2d.prefix_sum(0, 0), 1)
        self.assertEqual(ps2d.prefix_sum(1, 1), 12)  # 1+2+4+5
        self.assertEqual(ps2d.prefix_sum(2, 2), 45)  # 全部
    
    def test_row_and_col_sum(self):
        """测试行和列求和"""
        matrix = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]
        ps2d = PrefixSum2D(matrix)
        
        # 行和
        self.assertEqual(ps2d.row_sum(0), 6)  # 1+2+3
        self.assertEqual(ps2d.row_sum(1), 15)  # 4+5+6
        self.assertEqual(ps2d.row_sum(2), 24)  # 7+8+9
        
        # 列和
        self.assertEqual(ps2d.col_sum(0), 12)  # 1+4+7
        self.assertEqual(ps2d.col_sum(1), 15)  # 2+5+8
        self.assertEqual(ps2d.col_sum(2), 18)  # 3+6+9
    
    def test_single_element(self):
        """测试单元素矩阵"""
        matrix = [[42]]
        ps2d = PrefixSum2D(matrix)
        
        self.assertEqual(ps2d.total(), 42)
        self.assertEqual(ps2d.region_sum(0, 0, 0, 0), 42)
        self.assertEqual(ps2d.row_sum(0), 42)
        self.assertEqual(ps2d.col_sum(0), 42)
    
    def test_rectangular_matrix(self):
        """测试非方阵"""
        matrix = [
            [1, 2, 3, 4],
            [5, 6, 7, 8]
        ]
        ps2d = PrefixSum2D(matrix)
        
        self.assertEqual(ps2d.shape, (2, 4))
        self.assertEqual(ps2d.total(), 36)
        self.assertEqual(ps2d.region_sum(0, 1, 1, 2), 18)  # 2+3+6+7
    
    def test_negative_numbers(self):
        """测试负数"""
        matrix = [
            [1, -2, 3],
            [-4, 5, -6],
            [7, -8, 9]
        ]
        ps2d = PrefixSum2D(matrix)
        
        self.assertEqual(ps2d.total(), 5)
        self.assertEqual(ps2d.region_sum(0, 0, 1, 1), 0)  # 1+(-2)+(-4)+5
    
    def test_floats(self):
        """测试浮点数"""
        matrix = [
            [1.5, 2.5],
            [3.5, 4.5]
        ]
        ps2d = PrefixSum2D(matrix)
        
        self.assertAlmostEqual(ps2d.total(), 12.0)
        self.assertAlmostEqual(ps2d.region_sum(0, 0, 1, 1), 12.0)
    
    def test_index_out_of_bounds(self):
        """测试索引越界"""
        matrix = [[1, 2], [3, 4]]
        ps2d = PrefixSum2D(matrix)
        
        with self.assertRaises(PrefixSumError):
            ps2d.prefix_sum(-1, 0)
        
        with self.assertRaises(PrefixSumError):
            ps2d.region_sum(0, 0, 2, 2)
    
    def test_invalid_region(self):
        """测试无效区域"""
        matrix = [[1, 2], [3, 4]]
        ps2d = PrefixSum2D(matrix)
        
        with self.assertRaises(PrefixSumError):
            ps2d.region_sum(1, 1, 0, 0)  # 左上角大于右下角
    
    def test_empty_matrix(self):
        """测试空矩阵"""
        # 空矩阵应该被允许（类似于空数组）
        ps2d = PrefixSum2D([])
        
        self.assertEqual(ps2d.rows, 0)
        self.assertEqual(ps2d.cols, 0)
        self.assertEqual(ps2d.shape, (0, 0))
        self.assertEqual(ps2d.total(), 0)
    
    def test_invalid_matrix(self):
        """测试无效矩阵"""
        # 不规则矩阵
        with self.assertRaises(PrefixSumError):
            PrefixSum2D([[1, 2], [3]])
    
    def test_getitem(self):
        """测试索引访问"""
        matrix = [[1, 2], [3, 4]]
        ps2d = PrefixSum2D(matrix)
        
        self.assertEqual(ps2d[0], [1, 2])
        self.assertEqual(ps2d[1], [3, 4])
    
    def test_to_dict_and_from_dict(self):
        """测试序列化和反序列化"""
        matrix = [[1, 2], [3, 4]]
        ps2d1 = PrefixSum2D(matrix)
        
        data = ps2d1.to_dict()
        ps2d2 = PrefixSum2D.from_dict(data)
        
        self.assertEqual(ps2d1.total(), ps2d2.total())


class TestDifferenceArray(unittest.TestCase):
    """一维差分数组测试"""
    
    def test_basic_construction(self):
        """测试基本构建"""
        arr = [1, 2, 3, 4, 5]
        da = DifferenceArray(arr)
        
        self.assertEqual(da.size, 5)
        self.assertEqual(da.to_array(), arr)
    
    def test_range_add(self):
        """测试区间加"""
        arr = [1, 2, 3, 4, 5]
        da = DifferenceArray(arr)
        
        # 区间加
        da.range_add(1, 3, 10)
        result = da.to_array()
        
        self.assertEqual(result[0], 1)  # 未改变
        self.assertEqual(result[1], 12)  # 2 + 10
        self.assertEqual(result[2], 13)  # 3 + 10
        self.assertEqual(result[3], 14)  # 4 + 10
        self.assertEqual(result[4], 5)   # 未改变
    
    def test_multiple_range_adds(self):
        """测试多次区间加"""
        arr = [1, 2, 3, 4, 5]
        da = DifferenceArray(arr)
        
        da.range_add(1, 3, 10)
        da.range_add(0, 2, 5)
        da.range_add(2, 4, 3)
        
        result = da.to_array()
        # 原始: [1, 2, 3, 4, 5]
        # +10 on [1,3]: [1, 12, 13, 14, 5]
        # +5 on [0,2]: [6, 17, 18, 14, 5]
        # +3 on [2,4]: [6, 17, 21, 17, 8]
        
        self.assertEqual(result, [6, 17, 21, 17, 8])
    
    def test_chained_operations(self):
        """测试链式操作"""
        arr = [0, 0, 0, 0, 0]
        result = (DifferenceArray(arr)
                  .range_add(0, 2, 1)
                  .range_add(2, 4, 2)
                  .point_add(3, 5)
                  .to_array())
        
        self.assertEqual(result, [1, 1, 3, 7, 2])
    
    def test_point_add(self):
        """测试单点加"""
        arr = [1, 2, 3, 4, 5]
        da = DifferenceArray(arr)
        
        da.point_add(2, 100)
        result = da.to_array()
        
        self.assertEqual(result[0], 1)
        self.assertEqual(result[1], 2)
        self.assertEqual(result[2], 103)  # 3 + 100
        self.assertEqual(result[3], 4)
        self.assertEqual(result[4], 5)
    
    def test_empty_start(self):
        """测试从指定大小开始"""
        da = DifferenceArray(size=5)
        
        self.assertEqual(da.to_array(), [0, 0, 0, 0, 0])
        
        da.range_add(0, 4, 1)
        self.assertEqual(da.to_array(), [1, 1, 1, 1, 1])
    
    def test_negative_values(self):
        """测试负数"""
        arr = [10, 20, 30, 40, 50]
        da = DifferenceArray(arr)
        
        da.range_add(1, 3, -15)
        result = da.to_array()
        
        self.assertEqual(result, [10, 5, 15, 25, 50])
    
    def test_floats(self):
        """测试浮点数"""
        arr = [1.0, 2.0, 3.0, 4.0, 5.0]
        da = DifferenceArray(arr)
        
        da.range_add(0, 2, 0.5)
        result = da.to_array()
        
        self.assertEqual(result, [1.5, 2.5, 3.5, 4.0, 5.0])
    
    def test_reset(self):
        """测试重置"""
        arr = [1, 2, 3, 4, 5]
        da = DifferenceArray(arr)
        
        da.range_add(0, 4, 100)
        da.reset()
        
        self.assertEqual(da.to_array(), [0, 0, 0, 0, 0])
        
        # 重置到新数组
        da.reset([10, 20, 30, 40, 50])
        self.assertEqual(da.to_array(), [10, 20, 30, 40, 50])
    
    def test_index_out_of_bounds(self):
        """测试索引越界"""
        arr = [1, 2, 3]
        da = DifferenceArray(arr)
        
        with self.assertRaises(DifferenceArrayError):
            da.range_add(-1, 2, 1)
        
        with self.assertRaises(DifferenceArrayError):
            da.range_add(0, 3, 1)
    
    def test_invalid_range(self):
        """测试无效区间"""
        arr = [1, 2, 3]
        da = DifferenceArray(arr)
        
        with self.assertRaises(DifferenceArrayError):
            da.range_add(2, 1, 1)  # left > right
    
    def test_get_diff(self):
        """测试获取差分数组"""
        arr = [1, 3, 6, 10, 15]
        da = DifferenceArray(arr)
        diff = da.get_diff()
        
        # 差分数组应该是 [1, 2, 3, 4, 5]
        self.assertEqual(diff, [1, 2, 3, 4, 5])
    
    def test_to_dict_and_from_dict(self):
        """测试序列化和反序列化"""
        arr = [1, 2, 3, 4, 5]
        da1 = DifferenceArray(arr)
        da1.range_add(1, 3, 10)
        
        data = da1.to_dict()
        da2 = DifferenceArray.from_dict(data)
        
        self.assertEqual(da1.to_array(), da2.to_array())


class TestDifferenceArray2D(unittest.TestCase):
    """二维差分数组测试"""
    
    def test_basic_construction(self):
        """测试基本构建"""
        matrix = [
            [1, 2],
            [3, 4]
        ]
        da2d = DifferenceArray2D(matrix)
        
        self.assertEqual(da2d.rows, 2)
        self.assertEqual(da2d.cols, 2)
        self.assertEqual(da2d.shape, (2, 2))
        self.assertEqual(da2d.to_matrix(), matrix)
    
    def test_region_add(self):
        """测试区域加"""
        da2d = DifferenceArray2D(rows=3, cols=3)
        
        # 左上角 2x2 区域加 5
        da2d.region_add(0, 0, 1, 1, 5)
        result = da2d.to_matrix()
        
        expected = [
            [5, 5, 0],
            [5, 5, 0],
            [0, 0, 0]
        ]
        self.assertEqual(result, expected)
    
    def test_overlapping_regions(self):
        """测试重叠区域"""
        da2d = DifferenceArray2D(rows=3, cols=3)
        
        # 两个重叠的区域
        da2d.region_add(0, 0, 1, 1, 5)
        da2d.region_add(1, 1, 2, 2, 10)
        result = da2d.to_matrix()
        
        expected = [
            [5, 5, 0],
            [5, 15, 10],  # 中心重叠区域 5+10=15
            [0, 10, 10]
        ]
        self.assertEqual(result, expected)
    
    def test_point_add(self):
        """测试单点加"""
        da2d = DifferenceArray2D(rows=3, cols=3)
        
        da2d.point_add(1, 1, 42)
        result = da2d.to_matrix()
        
        expected = [
            [0, 0, 0],
            [0, 42, 0],
            [0, 0, 0]
        ]
        self.assertEqual(result, expected)
    
    def test_chained_operations(self):
        """测试链式操作"""
        da2d = (DifferenceArray2D(rows=3, cols=3)
                .region_add(0, 0, 2, 2, 1)
                .region_add(1, 1, 2, 2, 2)
                .point_add(2, 2, 3))
        
        result = da2d.to_matrix()
        
        expected = [
            [1, 1, 1],
            [1, 3, 3],
            [1, 3, 6]
        ]
        self.assertEqual(result, expected)
    
    def test_from_matrix(self):
        """测试从矩阵构建"""
        matrix = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]
        da2d = DifferenceArray2D(matrix)
        
        # 不做修改，还原应该得到原矩阵
        self.assertEqual(da2d.to_matrix(), matrix)
        
        # 修改后
        da2d.region_add(0, 0, 1, 1, 10)
        result = da2d.to_matrix()
        
        expected = [
            [11, 12, 3],
            [14, 15, 6],
            [7, 8, 9]
        ]
        self.assertEqual(result, expected)
    
    def test_negative_values(self):
        """测试负数"""
        da2d = DifferenceArray2D(rows=2, cols=2)
        
        da2d.region_add(0, 0, 1, 1, 10)
        da2d.region_add(0, 0, 0, 0, -15)
        result = da2d.to_matrix()
        
        expected = [
            [-5, 10],
            [10, 10]
        ]
        self.assertEqual(result, expected)
    
    def test_floats(self):
        """测试浮点数"""
        da2d = DifferenceArray2D(rows=2, cols=2)
        
        da2d.region_add(0, 0, 1, 1, 2.5)
        result = da2d.to_matrix()
        
        expected = [
            [2.5, 2.5],
            [2.5, 2.5]
        ]
        self.assertEqual(result, expected)
    
    def test_reset(self):
        """测试重置"""
        da2d = DifferenceArray2D(rows=2, cols=2)
        
        da2d.region_add(0, 0, 1, 1, 100)
        da2d.reset()
        
        self.assertEqual(da2d.to_matrix(), [[0, 0], [0, 0]])
    
    def test_index_out_of_bounds(self):
        """测试索引越界"""
        da2d = DifferenceArray2D(rows=2, cols=2)
        
        with self.assertRaises(DifferenceArrayError):
            da2d.region_add(-1, 0, 1, 1, 1)
        
        with self.assertRaises(DifferenceArrayError):
            da2d.region_add(0, 0, 2, 2, 1)
    
    def test_invalid_region(self):
        """测试无效区域"""
        da2d = DifferenceArray2D(rows=2, cols=2)
        
        with self.assertRaises(DifferenceArrayError):
            da2d.region_add(1, 1, 0, 0, 1)  # 左上角大于右下角
    
    def test_to_dict_and_from_dict(self):
        """测试序列化和反序列化"""
        da2d1 = DifferenceArray2D(rows=2, cols=2)
        da2d1.region_add(0, 0, 1, 1, 5)
        
        data = da2d1.to_dict()
        da2d2 = DifferenceArray2D.from_dict(data)
        
        self.assertEqual(da2d1.to_matrix(), da2d2.to_matrix())


class TestConvenienceFunctions(unittest.TestCase):
    """便捷函数测试"""
    
    def test_build_prefix_sum(self):
        """测试构建前缀和数组"""
        arr = [1, 2, 3, 4, 5]
        prefix = build_prefix_sum(arr)
        
        self.assertEqual(prefix, [0, 1, 3, 6, 10, 15])
    
    def test_range_sum_function(self):
        """测试区间求和函数"""
        prefix = [0, 1, 3, 6, 10, 15]
        
        self.assertEqual(range_sum(prefix, 0, 0), 1)
        self.assertEqual(range_sum(prefix, 0, 2), 6)
        self.assertEqual(range_sum(prefix, 1, 3), 9)
        self.assertEqual(range_sum(prefix, 0, 4), 15)
    
    def test_build_difference_array(self):
        """测试构建差分数组"""
        arr = [1, 3, 6, 10, 15]
        diff = build_difference_array(arr)
        
        self.assertEqual(diff, [1, 2, 3, 4, 5])
    
    def test_restore_from_difference(self):
        """测试从差分数组还原"""
        diff = [1, 2, 3, 4, 5]
        arr = restore_from_difference(diff)
        
        self.assertEqual(arr, [1, 3, 6, 10, 15])
    
    def test_roundtrip(self):
        """测试往返转换"""
        original = [1, 2, 3, 4, 5]
        diff = build_difference_array(original)
        restored = restore_from_difference(diff)
        
        self.assertEqual(original, restored)
    
    def test_empty_array_functions(self):
        """测试空数组的便捷函数"""
        self.assertEqual(build_prefix_sum([]), [0])
        self.assertEqual(build_difference_array([]), [])
        self.assertEqual(restore_from_difference([]), [])


class TestPerformance(unittest.TestCase):
    """性能测试"""
    
    def test_large_prefix_sum(self):
        """测试大规模前缀和"""
        n = 10000
        arr = list(range(1, n + 1))
        
        ps = PrefixSum(arr)
        
        # 计算整个数组的和
        self.assertEqual(ps.total(), n * (n + 1) // 2)
        
        # 随机区间查询
        for _ in range(100):
            left = random.randint(0, n - 1)
            right = random.randint(left, n - 1)
            
            # 验证结果
            expected = sum(arr[left:right + 1])
            self.assertEqual(ps.range_sum(left, right), expected)
    
    def test_large_difference_array(self):
        """测试大规模差分数组"""
        n = 10000
        da = DifferenceArray(size=n)
        
        # 执行大量区间更新
        for _ in range(100):
            left = random.randint(0, n - 1)
            right = random.randint(left, n - 1)
            value = random.randint(-100, 100)
            da.range_add(left, right, value)
        
        # 验证可以正常还原
        result = da.to_array()
        self.assertEqual(len(result), n)
    
    def test_large_prefix_sum_2d(self):
        """测试大规模二维前缀和"""
        n, m = 100, 100
        matrix = [[i * m + j + 1 for j in range(m)] for i in range(n)]
        
        ps2d = PrefixSum2D(matrix)
        
        # 计算整个矩阵的和
        expected_total = (n * m) * (n * m + 1) // 2
        self.assertEqual(ps2d.total(), expected_total)
    
    def test_large_difference_array_2d(self):
        """测试大规模二维差分数组"""
        n, m = 100, 100
        da2d = DifferenceArray2D(rows=n, cols=m)
        
        # 执行大量区域更新
        for _ in range(50):
            r1 = random.randint(0, n - 1)
            c1 = random.randint(0, m - 1)
            r2 = random.randint(r1, n - 1)
            c2 = random.randint(c1, m - 1)
            value = random.randint(-10, 10)
            da2d.region_add(r1, c1, r2, c2, value)
        
        # 验证可以正常还原
        result = da2d.to_matrix()
        self.assertEqual(len(result), n)
        self.assertEqual(len(result[0]), m)


class TestEdgeCases(unittest.TestCase):
    """边界条件测试"""
    
    def test_single_element_prefix_sum(self):
        """测试单元素前缀和"""
        ps = PrefixSum([42])
        
        self.assertEqual(ps.length, 1)
        self.assertEqual(ps.total(), 42)
        self.assertEqual(ps.prefix_sum(0), 42)
        self.assertEqual(ps.range_sum(0, 0), 42)
    
    def test_single_element_difference_array(self):
        """测试单元素差分数组"""
        da = DifferenceArray([42])
        
        da.range_add(0, 0, 10)
        self.assertEqual(da.to_array(), [52])
    
    def test_all_same_prefix_sum(self):
        """测试全相同元素的前缀和"""
        arr = [5] * 10
        ps = PrefixSum(arr)
        
        self.assertEqual(ps.total(), 50)
        self.assertEqual(ps.range_sum(2, 7), 30)  # 6 * 5
    
    def test_all_same_difference_array(self):
        """测试全相同元素的差分数组"""
        da = DifferenceArray([5] * 10)
        
        da.range_add(0, 9, 10)
        self.assertEqual(da.to_array(), [15] * 10)


if __name__ == '__main__':
    unittest.main(verbosity=2)