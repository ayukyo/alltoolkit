"""
滑动窗口统计工具测试模块

测试所有滑动窗口数据结构和统计计算功能。
"""

import unittest
import time
import math
from mod import (
    SlidingWindowMax, SlidingWindowMin, SlidingWindowStats,
    SlidingWindowMedian, SlidingWindowPercentile, TimeWindowStats,
    SlidingWindowCounter,
    sliding_max, sliding_min, sliding_mean, sliding_sum, sliding_median
)


class TestSlidingWindowMax(unittest.TestCase):
    """测试滑动窗口最大值"""
    
    def test_basic_max(self):
        """基本最大值测试"""
        swm = SlidingWindowMax(3)
        self.assertTrue(swm.is_empty())
        
        swm.push(1)
        self.assertEqual(swm.max(), 1)
        self.assertEqual(len(swm), 1)
        
        swm.push(3)
        self.assertEqual(swm.max(), 3)
        
        swm.push(2)
        self.assertEqual(swm.max(), 3)
        self.assertTrue(swm.is_full())
        
        swm.push(5)
        self.assertEqual(swm.max(), 5)
        
        swm.push(4)
        self.assertEqual(swm.max(), 5)
        
        swm.push(1)
        self.assertEqual(swm.max(), 5)  # 窗口 [5, 4, 1]，最大值 5
    
    def test_decreasing_sequence(self):
        """递减序列测试"""
        swm = SlidingWindowMax(3)
        data = [5, 4, 3, 2, 1]
        expected = [5, 5, 5, 4, 3]
        
        for i, val in enumerate(data):
            swm.push(val)
            self.assertEqual(swm.max(), expected[i])
    
    def test_increasing_sequence(self):
        """递增序列测试"""
        swm = SlidingWindowMax(3)
        data = [1, 2, 3, 4, 5]
        expected = [1, 2, 3, 4, 5]
        
        for i, val in enumerate(data):
            swm.push(val)
            self.assertEqual(swm.max(), expected[i])
    
    def test_window_size_one(self):
        """窗口大小为1的测试"""
        swm = SlidingWindowMax(1)
        for val in [1, 5, 3, 7, 2]:
            swm.push(val)
            self.assertEqual(swm.max(), val)
    
    def test_duplicates(self):
        """重复元素测试"""
        swm = SlidingWindowMax(3)
        data = [2, 2, 2, 2, 2]
        for val in data:
            swm.push(val)
            self.assertEqual(swm.max(), 2)
    
    def test_clear(self):
        """清空测试"""
        swm = SlidingWindowMax(3)
        swm.push(1)
        swm.push(2)
        swm.push(3)
        self.assertEqual(len(swm), 3)
        
        swm.clear()
        self.assertEqual(len(swm), 0)
        self.assertTrue(swm.is_empty())
        self.assertIsNone(swm.max())
    
    def test_invalid_window_size(self):
        """无效窗口大小测试"""
        with self.assertRaises(ValueError):
            SlidingWindowMax(0)
        with self.assertRaises(ValueError):
            SlidingWindowMax(-1)
    
    def test_return_popped(self):
        """测试返回被移除的值"""
        swm = SlidingWindowMax(3)
        self.assertIsNone(swm.push(1))
        self.assertIsNone(swm.push(2))
        self.assertIsNone(swm.push(3))
        self.assertEqual(swm.push(4), 1)  # 窗口已满，返回被移除的值


class TestSlidingWindowMin(unittest.TestCase):
    """测试滑动窗口最小值"""
    
    def test_basic_min(self):
        """基本最小值测试"""
        swm = SlidingWindowMin(3)
        
        swm.push(5)
        self.assertEqual(swm.min(), 5)
        
        swm.push(3)
        self.assertEqual(swm.min(), 3)
        
        swm.push(2)
        self.assertEqual(swm.min(), 2)
        
        swm.push(4)
        self.assertEqual(swm.min(), 2)
        
        swm.push(1)
        self.assertEqual(swm.min(), 1)
    
    def test_decreasing_sequence(self):
        """递减序列测试"""
        swm = SlidingWindowMin(3)
        data = [5, 4, 3, 2, 1]
        expected = [5, 4, 3, 2, 1]
        
        for i, val in enumerate(data):
            swm.push(val)
            self.assertEqual(swm.min(), expected[i])
    
    def test_increasing_sequence(self):
        """递增序列测试"""
        swm = SlidingWindowMin(3)
        data = [1, 2, 3, 4, 5]
        expected = [1, 1, 1, 2, 3]
        
        for i, val in enumerate(data):
            swm.push(val)
            self.assertEqual(swm.min(), expected[i])


class TestSlidingWindowStats(unittest.TestCase):
    """测试滑动窗口统计"""
    
    def test_sum(self):
        """总和测试"""
        stats = SlidingWindowStats(3)
        
        stats.push(1)
        self.assertEqual(stats.sum(), 1)
        
        stats.push(2)
        self.assertEqual(stats.sum(), 3)
        
        stats.push(3)
        self.assertEqual(stats.sum(), 6)
        
        stats.push(4)
        self.assertEqual(stats.sum(), 9)  # 2+3+4
    
    def test_mean(self):
        """平均值测试"""
        stats = SlidingWindowStats(3)
        
        stats.push(1)
        self.assertEqual(stats.mean(), 1)
        
        stats.push(2)
        self.assertEqual(stats.mean(), 1.5)
        
        stats.push(3)
        self.assertEqual(stats.mean(), 2)
        
        stats.push(4)
        self.assertEqual(stats.mean(), 3)  # (2+3+4)/3
    
    def test_variance_and_std(self):
        """方差和标准差测试"""
        stats = SlidingWindowStats(3)
        
        for val in [1, 2, 3]:
            stats.push(val)
        
        # 手动计算: mean=2, variance=((1-2)^2 + (2-2)^2 + (3-2)^2) / 3 = 2/3
        self.assertAlmostEqual(stats.variance(), 2/3, places=10)
        self.assertAlmostEqual(stats.std_dev(), math.sqrt(2/3), places=10)
        
        # 样本方差
        # variance = ((1-2)^2 + (2-2)^2 + (3-2)^2) / 2 = 1
        self.assertAlmostEqual(stats.variance(population=False), 1.0, places=10)
    
    def test_min_max_range(self):
        """最小值、最大值、极差测试"""
        stats = SlidingWindowStats(3)
        
        for val in [1, 5, 3]:
            stats.push(val)
        
        self.assertEqual(stats.min(), 1)
        self.assertEqual(stats.max(), 5)
        self.assertEqual(stats.range(), 4)
    
    def test_count(self):
        """计数测试"""
        stats = SlidingWindowStats(3)
        
        self.assertEqual(stats.count(), 0)
        
        stats.push(1)
        self.assertEqual(stats.count(), 1)
        
        stats.push(2)
        self.assertEqual(stats.count(), 2)
        
        stats.push(3)
        self.assertEqual(stats.count(), 3)
        
        stats.push(4)
        self.assertEqual(stats.count(), 3)  # 窗口大小限制
    
    def test_empty_window(self):
        """空窗口测试"""
        stats = SlidingWindowStats(3)
        
        self.assertTrue(stats.is_empty())
        self.assertIsNone(stats.mean())
        self.assertIsNone(stats.variance())
        self.assertIsNone(stats.std_dev())
        self.assertIsNone(stats.min())
        self.assertIsNone(stats.max())
        self.assertIsNone(stats.range())


class TestSlidingWindowMedian(unittest.TestCase):
    """测试滑动窗口中位数"""
    
    def test_basic_median(self):
        """基本中位数测试"""
        swm = SlidingWindowMedian(3)
        
        swm.push(1)
        self.assertEqual(swm.median(), 1)
        
        swm.push(2)
        self.assertEqual(swm.median(), 1.5)
        
        swm.push(3)
        self.assertEqual(swm.median(), 2)
        
        swm.push(4)
        self.assertEqual(swm.median(), 3)
        
        swm.push(5)
        self.assertEqual(swm.median(), 4)
    
    def test_odd_window(self):
        """奇数窗口大小测试"""
        swm = SlidingWindowMedian(5)
        data = [3, 1, 4, 1, 5, 9, 2, 6]
        
        results = []
        for val in data:
            swm.push(val)
            results.append(swm.median())
        
        # 验证几个关键点
        self.assertEqual(results[0], 3)   # [3]
        self.assertEqual(results[4], 3)   # [3,1,4,1,5] sorted: [1,1,3,4,5]
        self.assertEqual(results[7], 5)   # [5,9,2,6,5] sorted: [2,5,5,6,9]
    
    def test_even_window(self):
        """偶数窗口大小测试"""
        swm = SlidingWindowMedian(4)
        data = [1, 2, 3, 4, 5, 6]
        
        results = []
        for val in data:
            swm.push(val)
            results.append(swm.median())
        
        self.assertEqual(results[3], 2.5)  # [1,2,3,4]
        self.assertEqual(results[5], 4.5)  # [3,4,5,6]
    
    def test_duplicates(self):
        """重复元素测试"""
        swm = SlidingWindowMedian(3)
        for val in [5, 5, 5, 5, 5]:
            swm.push(val)
            self.assertEqual(swm.median(), 5)


class TestSlidingWindowPercentile(unittest.TestCase):
    """测试滑动窗口百分位数"""
    
    def test_median(self):
        """中位数（P50）测试"""
        swp = SlidingWindowPercentile(5, percentile=50)
        data = [1, 2, 3, 4, 5]
        
        for val in data:
            swp.push(val)
        
        self.assertEqual(swp.percentile_value(), 3)
    
    def test_quartiles(self):
        """四分位数测试"""
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        
        # P25
        swp = SlidingWindowPercentile(10, percentile=25)
        for val in data:
            swp.push(val)
        self.assertEqual(swp.percentile_value(), 3.25)  # 线性插值
        
        # P75
        swp = SlidingWindowPercentile(10, percentile=75)
        for val in data:
            swp.push(val)
        self.assertEqual(swp.percentile_value(), 7.75)
    
    def test_percentile_0_and_100(self):
        """P0 和 P100 测试"""
        data = [1, 2, 3, 4, 5]
        
        swp = SlidingWindowPercentile(5, percentile=0)
        for val in data:
            swp.push(val)
        self.assertEqual(swp.percentile_value(), 1)
        
        swp = SlidingWindowPercentile(5, percentile=100)
        for val in data:
            swp.push(val)
        self.assertEqual(swp.percentile_value(), 5)
    
    def test_set_percentile(self):
        """动态设置百分位数测试"""
        swp = SlidingWindowPercentile(5, percentile=50)
        data = [1, 2, 3, 4, 5]
        
        for val in data:
            swp.push(val)
        
        self.assertEqual(swp.percentile_value(), 3)
        
        swp.set_percentile(75)
        self.assertEqual(swp.percentile_value(), 4)
        
        swp.set_percentile(25)
        self.assertEqual(swp.percentile_value(), 2)
    
    def test_invalid_percentile(self):
        """无效百分位数测试"""
        with self.assertRaises(ValueError):
            SlidingWindowPercentile(5, percentile=-1)
        with self.assertRaises(ValueError):
            SlidingWindowPercentile(5, percentile=101)


class TestTimeWindowStats(unittest.TestCase):
    """测试时间窗口统计"""
    
    def test_basic_time_window(self):
        """基本时间窗口测试"""
        tws = TimeWindowStats(window_seconds=10)
        now = time.time()
        
        tws.push(now - 5, 100)
        tws.push(now - 3, 200)
        tws.push(now, 300)
        
        self.assertEqual(tws.count(), 3)
        self.assertEqual(tws.sum(), 600)
        self.assertEqual(tws.mean(), 200)
    
    def test_expired_data(self):
        """过期数据测试"""
        tws = TimeWindowStats(window_seconds=5)
        now = time.time()
        
        # 添加过期数据，传入当前时间作为参考
        tws.push(now - 10, 100, current_time=now)  # 10秒前的数据，窗口5秒，会被清理
        self.assertEqual(tws.count(), 0)  # 过期数据被清理
        
        # 添加有效数据
        tws.push(now - 2, 200, current_time=now)
        tws.push(now, 300, current_time=now)
        
        self.assertEqual(tws.count(), 2)
        self.assertEqual(tws.sum(), 500)
    
    def test_rate(self):
        """速率计算测试"""
        tws = TimeWindowStats(window_seconds=10)
        now = time.time()
        
        tws.push(now - 5, 1)
        tws.push(now, 1)
        
        # 在5秒内有2个点，速率 = 1/5 = 0.2
        self.assertAlmostEqual(tws.rate(), 0.2, places=2)
    
    def test_time_span(self):
        """时间跨度测试"""
        tws = TimeWindowStats(window_seconds=10)
        now = time.time()
        
        self.assertIsNone(tws.time_span())
        
        tws.push(now, 1)
        self.assertIsNone(tws.time_span())  # 只有一个点
        
        tws.push(now + 5, 2)
        self.assertEqual(tws.time_span(), 5)
    
    def test_min_max(self):
        """最小值最大值测试"""
        tws = TimeWindowStats(window_seconds=10)
        now = time.time()
        
        self.assertIsNone(tws.min())
        self.assertIsNone(tws.max())
        
        tws.push(now, 100)
        tws.push(now + 1, 50)
        tws.push(now + 2, 150)
        
        self.assertEqual(tws.min(), 50)
        self.assertEqual(tws.max(), 150)


class TestSlidingWindowCounter(unittest.TestCase):
    """测试滑动窗口计数器"""
    
    def test_basic_count(self):
        """基本计数测试"""
        counter = SlidingWindowCounter(5)
        
        counter.push('a')
        counter.push('b')
        counter.push('a')
        counter.push('c')
        counter.push('a')
        
        self.assertEqual(counter.count('a'), 3)
        self.assertEqual(counter.count('b'), 1)
        self.assertEqual(counter.count('c'), 1)
        self.assertEqual(counter.count('d'), 0)
    
    def test_window_eviction(self):
        """窗口淘汰测试"""
        counter = SlidingWindowCounter(3)
        
        counter.push('a')
        counter.push('a')
        counter.push('a')
        self.assertEqual(counter.count('a'), 3)
        
        counter.push('b')
        self.assertEqual(counter.count('a'), 2)
        self.assertEqual(counter.count('b'), 1)
        
        counter.push('c')
        self.assertEqual(counter.count('a'), 1)
        
        counter.push('d')
        self.assertEqual(counter.count('a'), 0)
    
    def test_total_and_unique(self):
        """总数和唯一计数测试"""
        counter = SlidingWindowCounter(5)
        
        self.assertEqual(counter.total(), 0)
        self.assertEqual(counter.unique_count(), 0)
        
        counter.push('a')
        counter.push('b')
        counter.push('a')
        
        self.assertEqual(counter.total(), 3)
        self.assertEqual(counter.unique_count(), 2)
    
    def test_most_common(self):
        """最常见元素测试"""
        counter = SlidingWindowCounter(11)  # 窗口大小调整为 11，容纳所有元素
        
        for _ in range(5):
            counter.push('a')
        for _ in range(3):
            counter.push('b')
        for _ in range(2):
            counter.push('c')
        counter.push('d')
        
        most_common = counter.most_common(3)
        self.assertEqual(most_common[0], ('a', 5))
        self.assertEqual(most_common[1], ('b', 3))
        self.assertEqual(most_common[2], ('c', 2))
    
    def test_all_counts(self):
        """获取所有计数测试"""
        counter = SlidingWindowCounter(5)
        
        counter.push('a')
        counter.push('b')
        counter.push('a')
        
        counts = counter.all_counts()
        self.assertEqual(counts['a'], 2)
        self.assertEqual(counts['b'], 1)
        
        # 确保是副本
        counts['c'] = 100
        self.assertEqual(counter.count('c'), 0)


class TestConvenienceFunctions(unittest.TestCase):
    """测试便捷函数"""
    
    def test_sliding_max_function(self):
        """sliding_max 函数测试"""
        data = [1, 3, 2, 5, 4]
        result = sliding_max(data, 3)
        expected = [1, 3, 3, 5, 5]
        self.assertEqual(result, expected)
    
    def test_sliding_min_function(self):
        """sliding_min 函数测试"""
        data = [5, 3, 2, 4, 1]
        result = sliding_min(data, 3)
        expected = [5, 3, 2, 2, 1]
        self.assertEqual(result, expected)
    
    def test_sliding_mean_function(self):
        """sliding_mean 函数测试"""
        data = [1, 2, 3, 4, 5]
        result = sliding_mean(data, 3)
        expected = [1.0, 1.5, 2.0, 3.0, 4.0]
        self.assertEqual(result, expected)
    
    def test_sliding_sum_function(self):
        """sliding_sum 函数测试"""
        data = [1, 2, 3, 4, 5]
        result = sliding_sum(data, 3)
        expected = [1, 3, 6, 9, 12]
        self.assertEqual(result, expected)
    
    def test_sliding_median_function(self):
        """sliding_median 函数测试"""
        data = [1, 2, 3, 4, 5]
        result = sliding_median(data, 3)
        expected = [1, 1.5, 2, 3, 4]
        self.assertEqual(result, expected)


class TestEdgeCases(unittest.TestCase):
    """边界情况测试"""
    
    def test_single_element_window(self):
        """单元素窗口测试"""
        swm = SlidingWindowMax(1)
        self.assertEqual(swm.push(5), None)
        self.assertEqual(swm.max(), 5)
        self.assertEqual(swm.push(3), 5)
        self.assertEqual(swm.max(), 3)
    
    def test_large_window(self):
        """大窗口测试"""
        window_size = 1000
        swm = SlidingWindowMax(window_size)
        
        for i in range(window_size + 100):
            swm.push(i)
            expected_max = i
            self.assertEqual(swm.max(), expected_max)
    
    def test_negative_numbers(self):
        """负数测试"""
        swm = SlidingWindowMax(3)
        data = [-5, -3, -7, -1, -2]
        
        for val in data:
            swm.push(val)
        
        self.assertEqual(swm.max(), -1)
    
    def test_floating_point(self):
        """浮点数测试"""
        stats = SlidingWindowStats(3)
        data = [1.5, 2.5, 3.5]
        
        for val in data:
            stats.push(val)
        
        self.assertAlmostEqual(stats.mean(), 2.5)
        self.assertAlmostEqual(stats.sum(), 7.5)
    
    def test_mixed_int_float(self):
        """混合整数浮点数测试"""
        swm = SlidingWindowMax(3)
        swm.push(1)
        swm.push(2.5)
        swm.push(3)
        
        self.assertEqual(swm.max(), 3)


if __name__ == "__main__":
    unittest.main(verbosity=2)