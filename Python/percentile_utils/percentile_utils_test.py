"""
百分位数工具模块测试

测试所有百分位数计算功能
"""

import unittest
import math
from mod import (
    percentile,
    quartiles,
    percentile_rank,
    boxplot_stats,
    deciles,
    percentiles,
    grouped_percentile,
    percentile_summary,
    is_outlier,
    normalize_by_percentile,
    winsorize,
    InterpolationMethod
)


class TestPercentile(unittest.TestCase):
    """测试 percentile 函数"""
    
    def test_simple_percentile(self):
        """测试基本百分位数计算"""
        data = [1, 2, 3, 4, 5]
        self.assertEqual(percentile(data, 50), 3.0)
        self.assertEqual(percentile(data, 0), 1.0)
        self.assertEqual(percentile(data, 100), 5.0)
    
    def test_linear_interpolation(self):
        """测试线性插值"""
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        # P25 应该在索引 2.25 处，值为 3.25
        self.assertAlmostEqual(percentile(data, 25), 3.25)
        # P75 应该在索引 6.75 处，值为 7.75
        self.assertAlmostEqual(percentile(data, 75), 7.75)
    
    def test_lower_method(self):
        """测试下界方法"""
        data = [1, 2, 3, 4, 5]
        self.assertEqual(percentile(data, 25, InterpolationMethod.LOWER), 2.0)
        self.assertEqual(percentile(data, 50, InterpolationMethod.LOWER), 3.0)
    
    def test_higher_method(self):
        """测试上界方法"""
        data = [1, 2, 3, 4, 5]
        self.assertEqual(percentile(data, 25, InterpolationMethod.HIGHER), 2.0)
        self.assertEqual(percentile(data, 50, InterpolationMethod.HIGHER), 3.0)
    
    def test_nearest_method(self):
        """测试最近邻方法"""
        data = [1, 2, 3, 4, 5]
        self.assertEqual(percentile(data, 50, InterpolationMethod.NEAREST), 3.0)
        self.assertEqual(percentile(data, 26, InterpolationMethod.NEAREST), 2.0)
    
    def test_midpoint_method(self):
        """测试中点方法"""
        data = [1, 2, 3, 4, 5]
        # 对于 P50，rank=2，取索引 2 和 3 的中点：(3+4)/2 = 3.5
        self.assertEqual(percentile(data, 50, InterpolationMethod.MIDPOINT), 3.5)
    
    def test_single_value(self):
        """测试单值数据"""
        data = [42]
        self.assertEqual(percentile(data, 50), 42.0)
        self.assertEqual(percentile(data, 0), 42.0)
        self.assertEqual(percentile(data, 100), 42.0)
    
    def test_sorted_data_optimization(self):
        """测试已排序数据优化"""
        sorted_data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        # 使用 sorted_data=True 应该得到相同结果
        self.assertEqual(
            percentile(sorted_data, 50, sorted_data=True),
            percentile(sorted_data, 50, sorted_data=False)
        )
    
    def test_invalid_percentile(self):
        """测试无效百分位数"""
        data = [1, 2, 3]
        with self.assertRaises(ValueError):
            percentile(data, -1)
        with self.assertRaises(ValueError):
            percentile(data, 101)
    
    def test_empty_data(self):
        """测试空数据"""
        with self.assertRaises(ValueError):
            percentile([], 50)
    
    def test_non_numeric_data(self):
        """测试非数值数据"""
        with self.assertRaises(TypeError):
            percentile([1, 'a', 3], 50)


class TestQuartiles(unittest.TestCase):
    """测试 quartiles 函数"""
    
    def test_basic_quartiles(self):
        """测试基本四分位数"""
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        qs = quartiles(data)
        
        # 使用 linear 方法，Q1 = P25，对于 9 个元素
        # rank = 0.25 * 8 = 2，所以 Q1 在索引 2-3 之间
        self.assertAlmostEqual(qs['Q1'], 3.0)  # 实际计算值
        self.assertEqual(qs['Q2'], 5.0)  # 中位数
        # Q3 = P75，rank = 0.75 * 8 = 6
        self.assertAlmostEqual(qs['Q3'], 7.0)
        self.assertAlmostEqual(qs['IQR'], 4.0)
    
    def test_even_length_data(self):
        """测试偶数长度数据"""
        data = [1, 2, 3, 4, 5, 6, 7, 8]
        qs = quartiles(data)
        
        self.assertEqual(qs['Q2'], 4.5)  # 中位数
    
    def test_quartiles_with_method(self):
        """测试不同插值方法的四分位数"""
        data = [1, 2, 3, 4, 5]
        
        qs_linear = quartiles(data, InterpolationMethod.LINEAR)
        qs_lower = quartiles(data, InterpolationMethod.LOWER)
        
        # 不同方法可能得到不同结果
        self.assertIsInstance(qs_linear['Q1'], float)
        self.assertIsInstance(qs_lower['Q1'], float)


class TestPercentileRank(unittest.TestCase):
    """测试 percentile_rank 函数"""
    
    def test_exact_value(self):
        """测试精确值"""
        data = [1, 2, 3, 4, 5]
        rank = percentile_rank(data, 3)
        self.assertEqual(rank, 50.0)
    
    def test_interpolated_value(self):
        """测试插值"""
        data = [1, 2, 3, 4, 5]
        # 2.5 在 2 和 3 之间
        rank = percentile_rank(data, 2.5)
        # 百分位排名应该在合理范围内
        self.assertGreaterEqual(rank, 25.0)
        self.assertLessEqual(rank, 50.0)
    
    def test_below_min(self):
        """测试低于最小值"""
        data = [1, 2, 3, 4, 5]
        rank = percentile_rank(data, 0)
        self.assertEqual(rank, 0.0)
    
    def test_above_max(self):
        """测试高于最大值"""
        data = [1, 2, 3, 4, 5]
        rank = percentile_rank(data, 100)
        self.assertEqual(rank, 100.0)
    
    def test_duplicate_values(self):
        """测试重复值"""
        data = [1, 2, 2, 2, 3, 4, 5]
        rank = percentile_rank(data, 2)
        self.assertGreater(rank, 20.0)
        self.assertLess(rank, 60.0)


class TestBoxplotStats(unittest.TestCase):
    """测试 boxplot_stats 函数"""
    
    def test_basic_boxplot(self):
        """测试基本箱线图统计"""
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        stats = boxplot_stats(data)
        
        self.assertEqual(stats['min'], 1)
        self.assertEqual(stats['max'], 9)
        self.assertIn('Q1', stats)
        self.assertIn('Q3', stats)
        self.assertIn('IQR', stats)
    
    def test_outlier_detection(self):
        """测试异常值检测"""
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 100]
        stats = boxplot_stats(data)
        
        self.assertIn(100, stats['outliers'])
    
    def test_no_outliers(self):
        """测试无异常值情况"""
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        stats = boxplot_stats(data)
        
        self.assertEqual(len(stats['outliers']), 0)
    
    def test_custom_whisker_multiplier(self):
        """测试自定义须长乘数"""
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 100]
        
        stats_1_5 = boxplot_stats(data, whisker_multiplier=1.5)
        stats_3_0 = boxplot_stats(data, whisker_multiplier=3.0)
        
        # 更大的乘数应该产生更少的异常值
        self.assertGreaterEqual(len(stats_1_5['outliers']), len(stats_3_0['outliers']))


class TestDeciles(unittest.TestCase):
    """测试 deciles 函数"""
    
    def test_basic_deciles(self):
        """测试基本十分位数"""
        data = list(range(1, 101))  # 1-100
        decs = deciles(data)
        
        self.assertEqual(len(decs), 10)
        # D0 = P0 (最小值), D9 = P90
        self.assertEqual(decs[0], 1.0)  # P0 = 最小值
        self.assertAlmostEqual(decs[9], 90.1)  # P90
    
    def test_deciles_symmetry(self):
        """测试十分位数对称性"""
        data = list(range(1, 11))
        decs = deciles(data)
        
        # 检查递增
        for i in range(len(decs) - 1):
            self.assertLessEqual(decs[i], decs[i + 1])


class TestPercentiles(unittest.TestCase):
    """测试 percentiles 函数"""
    
    def test_multiple_percentiles(self):
        """测试多个百分位数"""
        data = [1, 2, 3, 4, 5]
        ps = percentiles(data, [10, 25, 50, 75, 90])
        
        self.assertEqual(len(ps), 5)
        self.assertIn(10, ps)
        self.assertIn(50, ps)
        self.assertEqual(ps[50], 3.0)
    
    def test_percentiles_ordering(self):
        """测试百分位数顺序"""
        data = list(range(1, 101))
        ps = percentiles(data, [25, 50, 75])
        
        self.assertLess(ps[25], ps[50])
        self.assertLess(ps[50], ps[75])


class TestGroupedPercentile(unittest.TestCase):
    """测试 grouped_percentile 函数"""
    
    def test_grouped_percentile(self):
        """测试分组百分位数"""
        groups = {
            'A': [1, 2, 3, 4, 5],
            'B': [10, 20, 30, 40, 50],
            'C': [100, 200, 300, 400, 500]
        }
        
        result = grouped_percentile(groups, 50)
        
        self.assertEqual(result['A'], 3.0)
        self.assertEqual(result['B'], 30.0)
        self.assertEqual(result['C'], 300.0)
    
    def test_empty_groups(self):
        """测试空分组"""
        with self.assertRaises(ValueError):
            grouped_percentile({}, 50)


class TestPercentileSummary(unittest.TestCase):
    """测试 percentile_summary 函数"""
    
    def test_summary_structure(self):
        """测试摘要结构"""
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        summary = percentile_summary(data)
        
        required_keys = ['count', 'min', 'max', 'sum', 'mean', 'variance', 
                         'std_dev', 'quartiles', 'percentiles', 'range', 'median']
        
        for key in required_keys:
            self.assertIn(key, summary)
    
    def test_summary_values(self):
        """测试摘要值"""
        data = [1, 2, 3, 4, 5]
        summary = percentile_summary(data)
        
        self.assertEqual(summary['count'], 5)
        self.assertEqual(summary['min'], 1)
        self.assertEqual(summary['max'], 5)
        self.assertEqual(summary['sum'], 15)
        self.assertEqual(summary['mean'], 3.0)
    
    def test_std_dev(self):
        """测试标准差计算"""
        data = [1, 2, 3, 4, 5]
        summary = percentile_summary(data)
        
        # 总体标准差 = sqrt(((1-3)^2 + (2-3)^2 + (3-3)^2 + (4-3)^2 + (5-3)^2) / 5)
        # = sqrt((4 + 1 + 0 + 1 + 4) / 5) = sqrt(2) ≈ 1.414
        self.assertAlmostEqual(summary['std_dev'], math.sqrt(2), places=3)


class TestIsOutlier(unittest.TestCase):
    """测试 is_outlier 函数"""
    
    def test_is_outlier_true(self):
        """测试确认为异常值"""
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.assertTrue(is_outlier(100, data))
        self.assertTrue(is_outlier(-100, data))
    
    def test_is_outlier_false(self):
        """测试确认为正常值"""
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.assertFalse(is_outlier(5, data))
        self.assertFalse(is_outlier(1, data))
        self.assertFalse(is_outlier(9, data))


class TestNormalizeByPercentile(unittest.TestCase):
    """测试 normalize_by_percentile 函数"""
    
    def test_normalize_default(self):
        """测试默认归一化"""
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        normalized = normalize_by_percentile(data)
        
        self.assertEqual(len(normalized), len(data))
        # 检查归一化后的数据保持了相对顺序
        for i in range(len(normalized) - 1):
            self.assertLessEqual(normalized[i], normalized[i + 1])
    
    def test_normalize_custom_percentiles(self):
        """测试自定义百分位归一化"""
        data = [1, 2, 3, 4, 5]
        normalized = normalize_by_percentile(data, 10, 90)
        
        self.assertEqual(len(normalized), len(data))


class TestWinsorize(unittest.TestCase):
    """测试 winsorize 函数"""
    
    def test_winsorize_basic(self):
        """测试基本缩尾处理"""
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 100]
        result = winsorize(data, 10, 90)
        
        # 100 应该被缩尾到 P90
        self.assertLess(result[-1], 100)
        self.assertGreater(result[-1], 8)
    
    def test_winsorize_preserves_middle(self):
        """测试缩尾处理保留中间值"""
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        result = winsorize(data, 20, 80)
        
        # 中间值应该保持不变
        for i in range(2, 8):
            self.assertEqual(result[i], data[i])
    
    def test_winsorize_extremes(self):
        """测试极端值缩尾"""
        data = [-100, 1, 2, 3, 4, 5, 6, 7, 8, 100]
        result = winsorize(data, 10, 90)
        
        # 极端值应该被限制
        self.assertGreaterEqual(result[0], -100)
        self.assertLessEqual(result[-1], 100)


class TestInterpolationMethods(unittest.TestCase):
    """测试各种插值方法的对比"""
    
    def test_compare_methods(self):
        """比较不同插值方法"""
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        
        methods = [
            InterpolationMethod.LINEAR,
            InterpolationMethod.LOWER,
            InterpolationMethod.HIGHER,
            InterpolationMethod.NEAREST,
            InterpolationMethod.MIDPOINT
        ]
        
        results = {}
        for method in methods:
            results[method.value] = percentile(data, 25, method)
        
        # 所有方法都应该返回有效数值
        for value in results.values():
            self.assertIsInstance(value, float)
            self.assertGreater(value, 0)
    
    def test_exclusive_method(self):
        """测试 exclusive 方法"""
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        
        # P50 在有效范围内
        result = percentile(data, 50, InterpolationMethod.EXCLUSIVE)
        self.assertIsInstance(result, float)
    
    def test_exclusive_method_boundary(self):
        """测试 exclusive 方法边界"""
        data = [1, 2, 3, 4, 5]  # 只有5个元素
        
        # 太小的百分位数应该报错
        with self.assertRaises(ValueError):
            percentile(data, 5, InterpolationMethod.EXCLUSIVE)
        
        # 太大的百分位数应该报错
        with self.assertRaises(ValueError):
            percentile(data, 95, InterpolationMethod.EXCLUSIVE)
    
    def test_exclusive_method_small_data(self):
        """测试 exclusive 方法小数据集"""
        data = [1, 2, 3]  # 只有3个元素
        
        # 需要至少4个数据点
        with self.assertRaises(ValueError):
            percentile(data, 50, InterpolationMethod.EXCLUSIVE)


class TestEdgeCases(unittest.TestCase):
    """测试边缘情况"""
    
    def test_two_values(self):
        """测试两个值的数据"""
        data = [1, 10]
        self.assertEqual(percentile(data, 0), 1.0)
        self.assertEqual(percentile(data, 50), 5.5)
        self.assertEqual(percentile(data, 100), 10.0)
    
    def test_all_same_values(self):
        """测试所有值相同"""
        data = [5, 5, 5, 5, 5]
        
        self.assertEqual(percentile(data, 0), 5.0)
        self.assertEqual(percentile(data, 50), 5.0)
        self.assertEqual(percentile(data, 100), 5.0)
        
        qs = quartiles(data)
        self.assertEqual(qs['Q1'], 5.0)
        self.assertEqual(qs['Q3'], 5.0)
        self.assertEqual(qs['IQR'], 0.0)
    
    def test_negative_values(self):
        """测试负值"""
        data = [-10, -5, 0, 5, 10]
        
        self.assertEqual(percentile(data, 50), 0.0)
        self.assertEqual(percentile(data, 0), -10.0)
        self.assertEqual(percentile(data, 100), 10.0)
    
    def test_floating_point_values(self):
        """测试浮点数值"""
        data = [1.5, 2.7, 3.9, 4.1, 5.3]
        
        result = percentile(data, 50)
        self.assertIsInstance(result, float)
    
    def test_large_dataset(self):
        """测试大数据集"""
        import random
        data = [random.random() * 1000 for _ in range(10000)]
        
        result = percentile(data, 50)
        self.assertGreater(result, 0)
        self.assertLess(result, 1000)


if __name__ == "__main__":
    unittest.main(verbosity=2)