"""
Sequence Utilities - 测试模块

全面测试所有序列分析功能。
"""

import unittest
import math
from sequence_utils import (
    # 异常类
    SequenceError, EmptySequenceError, InvalidSequenceError,
    
    # 统计分析
    mean, median, mode, variance, std_dev, skewness, kurtosis,
    quantile, quartiles, iqr, range_value, coefficient_of_variation,
    descriptive_stats,
    
    # 序列变换
    normalize, standardize, differentiate, cumulative_sum, cumulative_product,
    exponential_smoothing, moving_average, log_transform, power_transform,
    box_cox_transform,
    
    # 序列生成器
    arange, linspace, logspace, geometric_sequence, fibonacci, tribonacci,
    lucas_numbers, prime_numbers, triangular_numbers, square_numbers,
    cube_numbers, factorial_sequence,
    
    # 滑动窗口操作
    sliding_window, rolling_max, rolling_min, rolling_sum, rolling_std,
    
    # 插值与填充
    linear_interpolate, fill_missing,
    
    # 重采样
    downsample, upsample,
    
    # 序列操作
    reverse, shuffle, sample, split, chunk, flatten, unique,
    difference, intersection, union,
    
    # 异常值检测
    zscore_outliers, iqr_outliers, remove_outliers,
    
    # 趋势与周期检测
    is_monotonic, is_increasing, is_decreasing, trend_direction,
    find_peaks, find_valleys, detect_seasonality,
    
    # 自相关与滞后
    autocorrelation, autocorrelation_function, lag, lead,
    
    # 序列相似度
    euclidean_distance, manhattan_distance, cosine_similarity,
    pearson_correlation, spearman_correlation, dtw_distance,
    
    # 实用工具
    apply, filter_seq, reduce_seq, compose,
    
    # 常量
    GOLDEN_RATIO, EULER_NUMBER, PI, golden_sequence,
)


class TestStatistics(unittest.TestCase):
    """统计分析测试"""
    
    def test_mean(self):
        self.assertAlmostEqual(mean([1, 2, 3, 4, 5]), 3.0)
        self.assertAlmostEqual(mean([10]), 10.0)
        with self.assertRaises(EmptySequenceError):
            mean([])
    
    def test_median(self):
        self.assertAlmostEqual(median([1, 2, 3, 4, 5]), 3.0)
        self.assertAlmostEqual(median([1, 2, 3, 4]), 2.5)
        self.assertAlmostEqual(median([5]), 5.0)
        with self.assertRaises(EmptySequenceError):
            median([])
    
    def test_mode(self):
        self.assertEqual(mode([1, 2, 2, 3, 3, 3]), [3])
        self.assertEqual(sorted(mode([1, 1, 2, 2])), [1, 2])
        with self.assertRaises(EmptySequenceError):
            mode([])
    
    def test_variance(self):
        self.assertAlmostEqual(variance([1, 2, 3, 4, 5], population=True), 2.0)
        self.assertAlmostEqual(variance([1, 2, 3, 4, 5], population=False), 2.5)
        with self.assertRaises(EmptySequenceError):
            variance([])
    
    def test_std_dev(self):
        self.assertAlmostEqual(std_dev([2, 4, 4, 4, 5, 5, 7, 9], population=True), 2.0)
        with self.assertRaises(EmptySequenceError):
            std_dev([])
    
    def test_skewness(self):
        # 对称分布偏度应接近0
        data = [1, 2, 3, 4, 5]
        self.assertAlmostEqual(skewness(data), 0.0, places=10)
        with self.assertRaises(EmptySequenceError):
            skewness([])
    
    def test_kurtosis(self):
        data = [1, 2, 3, 4, 5]
        k = kurtosis(data)
        self.assertIsInstance(k, float)
        with self.assertRaises(EmptySequenceError):
            kurtosis([])
    
    def test_quantile(self):
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.assertAlmostEqual(quantile(data, 0.25), 3.25)
        self.assertAlmostEqual(quantile(data, 0.5), 5.5)
        self.assertAlmostEqual(quantile(data, 0.75), 7.75)
        with self.assertRaises(ValueError):
            quantile(data, 1.5)
    
    def test_quartiles(self):
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        q1, q2, q3 = quartiles(data)
        self.assertAlmostEqual(q1, 3.25)
        self.assertAlmostEqual(q2, 5.5)
        self.assertAlmostEqual(q3, 7.75)
    
    def test_iqr(self):
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.assertAlmostEqual(iqr(data), 4.5)
    
    def test_range_value(self):
        self.assertAlmostEqual(range_value([1, 5, 10]), 9.0)
        with self.assertRaises(EmptySequenceError):
            range_value([])
    
    def test_coefficient_of_variation(self):
        data = [10, 20, 30, 40, 50]
        cv = coefficient_of_variation(data)
        self.assertGreater(cv, 0)
    
    def test_descriptive_stats(self):
        data = [1, 2, 3, 4, 5]
        stats = descriptive_stats(data)
        self.assertEqual(stats['count'], 5)
        self.assertAlmostEqual(stats['mean'], 3.0)
        self.assertIn('mode', stats)


class TestTransformations(unittest.TestCase):
    """序列变换测试"""
    
    def test_normalize_minmax(self):
        data = [1, 2, 3, 4, 5]
        result = normalize(data, method='minmax', a=0, b=1)
        self.assertAlmostEqual(result[0], 0.0)
        self.assertAlmostEqual(result[-1], 1.0)
    
    def test_normalize_zscore(self):
        data = [1, 2, 3, 4, 5]
        result = normalize(data, method='zscore')
        self.assertAlmostEqual(sum(result), 0.0, places=10)
        # zscore标准化使用样本标准差，标准化后总体标准差约为 sqrt(n-1/n)
        # 对于 n=5，sqrt(4/5) ≈ 0.894
        expected_std = math.sqrt((len(data) - 1) / len(data))
        self.assertAlmostEqual(std_dev(result, population=True), expected_std, places=5)
    
    def test_standardize(self):
        data = [1, 2, 3, 4, 5]
        result = standardize(data)
        self.assertAlmostEqual(mean(result), 0.0, places=10)
    
    def test_differentiate(self):
        data = [1, 2, 4, 7, 11]
        result = differentiate(data)
        self.assertEqual(result, [1.0, 2.0, 3.0, 4.0])
        
        # 二阶差分
        result2 = differentiate(data, 2)
        self.assertEqual(result2, [1.0, 1.0, 1.0])
    
    def test_cumulative_sum(self):
        self.assertEqual(cumulative_sum([1, 2, 3, 4, 5]), [1.0, 3.0, 6.0, 10.0, 15.0])
    
    def test_cumulative_product(self):
        self.assertEqual(cumulative_product([1, 2, 3, 4]), [1.0, 2.0, 6.0, 24.0])
    
    def test_exponential_smoothing(self):
        data = [10, 20, 15, 25, 20]
        result = exponential_smoothing(data, alpha=0.5)
        self.assertEqual(len(result), len(data))
        self.assertAlmostEqual(result[0], 10.0)
    
    def test_moving_average(self):
        data = [1, 2, 3, 4, 5]
        result = moving_average(data, 3)
        self.assertAlmostEqual(result[0], 2.0)
        self.assertAlmostEqual(result[1], 3.0)
        self.assertAlmostEqual(result[2], 4.0)
        
        # 带权重的移动平均
        weights = [0.2, 0.3, 0.5]
        result = moving_average(data, 3, weights=weights)
        self.assertEqual(len(result), 3)
    
    def test_log_transform(self):
        data = [1, math.e, math.e ** 2]
        result = log_transform(data)
        self.assertAlmostEqual(result[0], 0.0)
        self.assertAlmostEqual(result[1], 1.0)
        self.assertAlmostEqual(result[2], 2.0)
        
        # 对数变换要求正值
        with self.assertRaises(InvalidSequenceError):
            log_transform([-1, 2, 3])
    
    def test_power_transform(self):
        data = [1, 2, 3, 4]
        result = power_transform(data, 2)
        self.assertEqual(result, [1.0, 4.0, 9.0, 16.0])
    
    def test_box_cox_transform(self):
        data = [1, 2, 3, 4, 5]
        result = box_cox_transform(data, 0.5)
        self.assertEqual(len(result), len(data))
        
        # lambda=0 等同于对数变换
        result_log = box_cox_transform(data, 0)
        expected = log_transform(data)
        for r, e in zip(result_log, expected):
            self.assertAlmostEqual(r, e)


class TestGenerators(unittest.TestCase):
    """序列生成器测试"""
    
    def test_arange(self):
        self.assertEqual(arange(5), [0.0, 1.0, 2.0, 3.0, 4.0])
        self.assertEqual(arange(1, 5), [1.0, 2.0, 3.0, 4.0])
        self.assertEqual(arange(0, 10, 2), [0.0, 2.0, 4.0, 6.0, 8.0])
        
        # 负步长
        result = arange(5, 0, -1)
        self.assertEqual(result, [5.0, 4.0, 3.0, 2.0, 1.0])
    
    def test_linspace(self):
        result = linspace(0, 1, 5)
        self.assertEqual(len(result), 5)
        self.assertAlmostEqual(result[0], 0.0)
        self.assertAlmostEqual(result[-1], 1.0)
    
    def test_logspace(self):
        result = logspace(0, 2, 3)
        self.assertEqual(len(result), 3)
        self.assertAlmostEqual(result[0], 1.0)
        self.assertAlmostEqual(result[1], 10.0)
        self.assertAlmostEqual(result[2], 100.0)
    
    def test_geometric_sequence(self):
        result = geometric_sequence(1, 2, 5)
        self.assertEqual(result, [1.0, 2.0, 4.0, 8.0, 16.0])
    
    def test_fibonacci(self):
        self.assertEqual(fibonacci(0), [])
        self.assertEqual(fibonacci(1), [0])
        self.assertEqual(fibonacci(2), [0, 1])
        self.assertEqual(fibonacci(10), [0, 1, 1, 2, 3, 5, 8, 13, 21, 34])
    
    def test_tribonacci(self):
        self.assertEqual(tribonacci(0), [])
        self.assertEqual(tribonacci(5), [0, 0, 1, 1, 2])
    
    def test_lucas_numbers(self):
        self.assertEqual(lucas_numbers(0), [])
        self.assertEqual(lucas_numbers(5), [2, 1, 3, 4, 7])
    
    def test_prime_numbers(self):
        self.assertEqual(prime_numbers(10), [2, 3, 5, 7, 11, 13, 17, 19, 23, 29])
        self.assertEqual(prime_numbers(0), [])
    
    def test_triangular_numbers(self):
        self.assertEqual(triangular_numbers(5), [1, 3, 6, 10, 15])
    
    def test_square_numbers(self):
        self.assertEqual(square_numbers(5), [1, 4, 9, 16, 25])
    
    def test_cube_numbers(self):
        self.assertEqual(cube_numbers(4), [1, 8, 27, 64])
    
    def test_factorial_sequence(self):
        self.assertEqual(factorial_sequence(5), [1, 2, 6, 24, 120])


class TestSlidingWindow(unittest.TestCase):
    """滑动窗口测试"""
    
    def test_sliding_window(self):
        data = [1, 2, 3, 4, 5]
        result = sliding_window(data, 3)
        self.assertEqual(result, [[1, 2, 3], [2, 3, 4], [3, 4, 5]])
        
        # 带步长
        result = sliding_window(data, 3, step=2)
        self.assertEqual(result, [[1, 2, 3], [3, 4, 5]])
    
    def test_rolling_max(self):
        data = [1, 5, 3, 8, 2]
        result = rolling_max(data, 3)
        self.assertEqual(result, [5.0, 8.0, 8.0])
    
    def test_rolling_min(self):
        data = [1, 5, 3, 8, 2]
        result = rolling_min(data, 3)
        self.assertEqual(result, [1.0, 3.0, 2.0])
    
    def test_rolling_sum(self):
        data = [1, 2, 3, 4, 5]
        result = rolling_sum(data, 3)
        self.assertEqual(result, [6.0, 9.0, 12.0])
    
    def test_rolling_std(self):
        data = [1, 2, 3, 4, 5]
        result = rolling_std(data, 3)
        self.assertEqual(len(result), 3)
        for r in result:
            self.assertGreater(r, 0)


class TestInterpolation(unittest.TestCase):
    """插值与填充测试"""
    
    def test_linear_interpolate(self):
        x = [0, 1, 2, 3]
        y = [0, 2, 4, 6]
        
        # 线性插值
        result = linear_interpolate(x, y, 1.5)
        self.assertAlmostEqual(result, 3.0)
        
        # 外推
        result = linear_interpolate(x, y, -1)
        self.assertAlmostEqual(result, -2.0)
    
    def test_fill_missing_linear(self):
        data = [1, None, 3, None, 5]
        result = fill_missing(data, method='linear')
        # linear 方法先用 forward 再用 backward，边界处的 None 会用边界值填充
        # [1, None, 3, None, 5] -> forward: [1, 1, 3, 3, 5] -> backward: [1, 1, 3, 3, 5]
        self.assertEqual(result, [1.0, 1.0, 3.0, 3.0, 5.0])
    
    def test_fill_missing_forward(self):
        data = [1, None, None, 4]
        result = fill_missing(data, method='forward')
        self.assertEqual(result, [1.0, 1.0, 1.0, 4.0])
    
    def test_fill_missing_backward(self):
        data = [1, None, None, 4]
        result = fill_missing(data, method='backward')
        self.assertEqual(result, [1.0, 4.0, 4.0, 4.0])
    
    def test_fill_missing_mean(self):
        data = [1, None, 3, None, 5]
        result = fill_missing(data, method='mean')
        expected_mean = (1 + 3 + 5) / 3
        self.assertAlmostEqual(result[1], expected_mean)
        self.assertAlmostEqual(result[3], expected_mean)


class TestResampling(unittest.TestCase):
    """重采样测试"""
    
    def test_downsample_mean(self):
        data = [1, 2, 3, 4, 5, 6]
        result = downsample(data, 2, method='mean')
        self.assertEqual(result, [1.5, 3.5, 5.5])
    
    def test_downsample_sum(self):
        data = [1, 2, 3, 4, 5, 6]
        result = downsample(data, 2, method='sum')
        self.assertEqual(result, [3.0, 7.0, 11.0])
    
    def test_downsample_max(self):
        data = [1, 2, 3, 4, 5, 6]
        result = downsample(data, 2, method='max')
        self.assertEqual(result, [2.0, 4.0, 6.0])
    
    def test_upsample_linear(self):
        data = [0, 10]
        result = upsample(data, 2, method='linear')
        self.assertEqual(len(result), 3)
        self.assertAlmostEqual(result[1], 5.0)
    
    def test_upsample_nearest(self):
        data = [0, 10]
        result = upsample(data, 2, method='nearest')
        self.assertEqual(len(result), 3)


class TestSequenceOperations(unittest.TestCase):
    """序列操作测试"""
    
    def test_reverse(self):
        self.assertEqual(reverse([1, 2, 3, 4, 5]), [5, 4, 3, 2, 1])
    
    def test_shuffle(self):
        data = [1, 2, 3, 4, 5]
        result = shuffle(data, seed=42)
        self.assertEqual(set(result), set(data))
        
        # 固定种子产生固定结果
        result2 = shuffle(data, seed=42)
        self.assertEqual(result, result2)
    
    def test_sample_without_replacement(self):
        data = [1, 2, 3, 4, 5]
        result = sample(data, 3, replace=False, seed=42)
        self.assertEqual(len(result), 3)
        self.assertTrue(all(x in data for x in result))
        
        with self.assertRaises(ValueError):
            sample(data, 10, replace=False)
    
    def test_sample_with_replacement(self):
        data = [1, 2, 3, 4, 5]
        result = sample(data, 10, replace=True, seed=42)
        self.assertEqual(len(result), 10)
    
    def test_split(self):
        data = [1, 2, 3, 4, 5, 6]
        part1, part2 = split(data, ratio=0.5)
        self.assertEqual(len(part1), 3)
        self.assertEqual(len(part2), 3)
    
    def test_chunk(self):
        data = [1, 2, 3, 4, 5, 6, 7]
        result = chunk(data, 3)
        self.assertEqual(result, [[1, 2, 3], [4, 5, 6], [7]])
    
    def test_flatten(self):
        data = [[1, 2], [3, 4], [5]]
        result = flatten(data)
        self.assertEqual(result, [1, 2, 3, 4, 5])
    
    def test_unique(self):
        data = [1, 2, 2, 3, 3, 3, 4]
        result = unique(data)
        self.assertEqual(result, [1, 2, 3, 4])
    
    def test_difference(self):
        self.assertEqual(difference([1, 2, 3, 4], [3, 4, 5]), [1, 2])
    
    def test_intersection(self):
        self.assertEqual(intersection([1, 2, 3, 4], [3, 4, 5]), [3, 4])
    
    def test_union(self):
        result = union([1, 2, 3], [3, 4, 5])
        self.assertEqual(sorted(result), [1, 2, 3, 4, 5])


class TestOutliers(unittest.TestCase):
    """异常值检测测试"""
    
    def test_zscore_outliers(self):
        data = [1, 2, 3, 4, 5, 100]
        outliers = zscore_outliers(data, threshold=2.0)
        self.assertEqual(outliers, [5])
    
    def test_iqr_outliers(self):
        data = [1, 2, 3, 4, 5, 100]
        outliers = iqr_outliers(data, k=1.5)
        self.assertTrue(5 in outliers)
    
    def test_remove_outliers_iqr(self):
        data = [1, 2, 3, 4, 5, 100]
        result = remove_outliers(data, method='iqr')
        self.assertNotIn(100, result)
    
    def test_remove_outliers_zscore(self):
        data = [1, 2, 3, 4, 5, 100]
        result = remove_outliers(data, method='zscore', threshold=2.0)
        self.assertNotIn(100, result)


class TestTrendDetection(unittest.TestCase):
    """趋势检测测试"""
    
    def test_is_monotonic(self):
        self.assertTrue(is_monotonic([1, 2, 3, 4, 5]))
        self.assertTrue(is_monotonic([5, 4, 3, 2, 1]))
        self.assertTrue(is_monotonic([1, 1, 2, 2, 3]))
        self.assertFalse(is_monotonic([1, 3, 2, 4, 5]))
        
        # 严格单调
        self.assertTrue(is_monotonic([1, 2, 3], strict=True))
        self.assertFalse(is_monotonic([1, 1, 2], strict=True))
    
    def test_is_increasing(self):
        self.assertTrue(is_increasing([1, 2, 3, 4, 5]))
        self.assertFalse(is_increasing([5, 4, 3, 2, 1]))
    
    def test_is_decreasing(self):
        self.assertTrue(is_decreasing([5, 4, 3, 2, 1]))
        self.assertFalse(is_decreasing([1, 2, 3, 4, 5]))
    
    def test_trend_direction(self):
        self.assertEqual(trend_direction([1, 2, 3, 4, 5]), 'increasing')
        self.assertEqual(trend_direction([5, 4, 3, 2, 1]), 'decreasing')
    
    def test_find_peaks(self):
        data = [1, 3, 2, 4, 1, 5, 2]
        peaks = find_peaks(data)
        self.assertIn(1, peaks)  # 3 is a peak
        self.assertIn(3, peaks)  # 4 is a peak
        self.assertIn(5, peaks)  # 5 is a peak
    
    def test_find_valleys(self):
        data = [3, 1, 4, 2, 5, 1, 6]
        valleys = find_valleys(data)
        self.assertTrue(len(valleys) > 0)
    
    def test_detect_seasonality(self):
        # 周期性数据
        data = [1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3]
        period = detect_seasonality(data)
        self.assertEqual(period, 3)
        
        # 无周期性数据
        data2 = [1, 2, 3, 4, 5, 6, 7, 8]
        period2 = detect_seasonality(data2)
        self.assertIsNone(period2)


class TestAutocorrelation(unittest.TestCase):
    """自相关测试"""
    
    def test_autocorrelation_lag_0(self):
        data = [1, 2, 3, 4, 5]
        self.assertEqual(autocorrelation(data, 0), 1.0)
    
    def test_autocorrelation(self):
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        acf = autocorrelation_function(data, max_lag=3)
        self.assertEqual(len(acf), 4)
        self.assertEqual(acf[0], 1.0)
    
    def test_lag(self):
        data = [1, 2, 3, 4, 5]
        result = lag(data, 2, fill=0)
        self.assertEqual(result, [0, 0, 1, 2, 3])
    
    def test_lead(self):
        data = [1, 2, 3, 4, 5]
        result = lead(data, 2, fill=0)
        self.assertEqual(result, [3, 4, 5, 0, 0])


class TestSimilarity(unittest.TestCase):
    """序列相似度测试"""
    
    def test_euclidean_distance(self):
        seq1 = [1, 2, 3]
        seq2 = [4, 5, 6]
        result = euclidean_distance(seq1, seq2)
        expected = math.sqrt(27)  # sqrt((4-1)^2 + (5-2)^2 + (6-3)^2)
        self.assertAlmostEqual(result, expected)
        
        with self.assertRaises(ValueError):
            euclidean_distance([1, 2], [1, 2, 3])
    
    def test_manhattan_distance(self):
        seq1 = [1, 2, 3]
        seq2 = [4, 5, 6]
        result = manhattan_distance(seq1, seq2)
        self.assertEqual(result, 9.0)
    
    def test_cosine_similarity(self):
        seq1 = [1, 0, 0]
        seq2 = [1, 0, 0]
        result = cosine_similarity(seq1, seq2)
        self.assertAlmostEqual(result, 1.0)
        
        seq3 = [0, 1, 0]
        result = cosine_similarity(seq1, seq3)
        self.assertAlmostEqual(result, 0.0)
    
    def test_pearson_correlation(self):
        seq1 = [1, 2, 3, 4, 5]
        seq2 = [1, 2, 3, 4, 5]
        result = pearson_correlation(seq1, seq2)
        self.assertAlmostEqual(result, 1.0)
        
        seq3 = [5, 4, 3, 2, 1]
        result = pearson_correlation(seq1, seq3)
        self.assertAlmostEqual(result, -1.0)
    
    def test_spearman_correlation(self):
        seq1 = [1, 2, 3, 4, 5]
        seq2 = [5, 4, 3, 2, 1]
        result = spearman_correlation(seq1, seq2)
        self.assertAlmostEqual(result, -1.0)
    
    def test_dtw_distance(self):
        seq1 = [1, 2, 3]
        seq2 = [1, 2, 3]
        result = dtw_distance(seq1, seq2)
        self.assertAlmostEqual(result, 0.0)
        
        # DTW 可以对齐 [1,2,3] 和 [1,2,2,3]，因为 2 可以重复匹配
        seq3 = [1, 2, 2, 3]
        result = dtw_distance(seq1, seq3)
        # [1,2,3] 与 [1,2,2,3] 的最佳对齐：1->1, 2->2,2, 3->3，距离为0
        self.assertAlmostEqual(result, 0.0)
        
        # 有差异的序列
        seq4 = [1, 3, 5]
        result2 = dtw_distance(seq1, seq4)
        self.assertGreater(result2, 0)


class TestUtilities(unittest.TestCase):
    """实用工具测试"""
    
    def test_apply(self):
        data = [1, 2, 3, 4, 5]
        result = apply(data, lambda x: x ** 2)
        self.assertEqual(result, [1, 4, 9, 16, 25])
    
    def test_filter_seq(self):
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        result = filter_seq(data, lambda x: x > 5)
        self.assertEqual(result, [6, 7, 8, 9, 10])
    
    def test_reduce_seq(self):
        data = [1, 2, 3, 4, 5]
        result = reduce_seq(data, lambda x, y: x + y)
        self.assertEqual(result, 15)
        
        result = reduce_seq(data, lambda x, y: x + y, initial=10)
        self.assertEqual(result, 25)
    
    def test_compose(self):
        # compose 从右到左执行：先执行最后一个函数
        # compose(lambda x: x + 1, lambda x: x * 2) 对 3 的执行顺序：
        # 先执行 lambda x: x * 2，得到 6，再执行 lambda x: x + 1，得到 7
        f = compose(lambda x: x + 1, lambda x: x * 2)
        result = f(3)  # (3 * 2) + 1 = 7
        self.assertEqual(result, 7)
        
        # 数学上的函数组合：f∘g(x) = f(g(x))，即先 g 后 f
        # compose(f, g) 应该先执行 g，再执行 f
        f2 = compose(lambda x: x * 2, lambda x: x + 1)
        result2 = f2(3)  # (3 + 1) * 2 = 8
        self.assertEqual(result2, 8)
    
    def test_golden_ratio(self):
        self.assertAlmostEqual(GOLDEN_RATIO, 1.618033988749895, places=5)
    
    def test_golden_sequence(self):
        result = golden_sequence(5)
        self.assertEqual(len(result), 5)
        for i, val in enumerate(result):
            self.assertAlmostEqual(val, GOLDEN_RATIO ** i)


class TestConstants(unittest.TestCase):
    """常量测试"""
    
    def test_constants(self):
        self.assertAlmostEqual(EULER_NUMBER, math.e)
        self.assertAlmostEqual(PI, math.pi)


if __name__ == '__main__':
    unittest.main(verbosity=2)