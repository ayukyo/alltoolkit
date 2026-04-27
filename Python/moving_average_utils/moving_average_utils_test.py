"""
Moving Average Utils 单元测试
"""

import sys
import os
import unittest
import math

# Add module directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mod import (
    simple_moving_average,
    exponential_moving_average,
    weighted_moving_average,
    cumulative_moving_average,
    triangular_moving_average,
    hull_moving_average,
    kaufman_adaptive_moving_average,
    volume_weighted_moving_average,
    moving_average_convergence_divergence,
    average_true_range,
    bollinger_bands,
    rolling_statistics,
    MovingAverage,
)


class TestSimpleMovingAverage(unittest.TestCase):
    """简单移动平均测试"""
    
    def test_basic(self):
        """基础测试"""
        data = [1, 2, 3, 4, 5]
        result = simple_moving_average(data, 3)
        self.assertEqual(result[:2], [None, None])
        self.assertEqual(result[2], 2.0)
        self.assertEqual(result[3], 3.0)
        self.assertEqual(result[4], 4.0)
    
    def test_window_equals_length(self):
        """窗口等于数据长度"""
        data = [1, 2, 3, 4, 5]
        result = simple_moving_average(data, 5)
        self.assertEqual(result[:4], [None, None, None, None])
        self.assertEqual(result[4], 3.0)
    
    def test_window_greater_than_length(self):
        """窗口大于数据长度"""
        data = [1, 2, 3]
        result = simple_moving_average(data, 5)
        self.assertEqual(result, [None, None, None])
    
    def test_single_element(self):
        """单元素"""
        data = [5]
        result = simple_moving_average(data, 1)
        self.assertEqual(result, [5.0])
    
    def test_invalid_window(self):
        """无效窗口"""
        with self.assertRaises(ValueError):
            simple_moving_average([1, 2, 3], 0)
        with self.assertRaises(ValueError):
            simple_moving_average([1, 2, 3], -1)
    
    def test_empty_data(self):
        """空数据"""
        result = simple_moving_average([], 3)
        self.assertEqual(result, [])


class TestExponentialMovingAverage(unittest.TestCase):
    """指数移动平均测试"""
    
    def test_basic(self):
        """基础测试"""
        data = [1, 2, 3, 4, 5]
        result = exponential_moving_average(data, 3)
        self.assertEqual(result[:2], [None, None])
        # 第一个EMA是SMA
        self.assertEqual(result[2], 2.0)
        # 后续值递减权重
        self.assertIsNotNone(result[3])
        self.assertIsNotNone(result[4])
    
    def test_custom_smoothing(self):
        """自定义平滑因子"""
        data = [1, 2, 3, 4, 5]
        result = exponential_moving_average(data, 3, smoothing=0.5)
        self.assertEqual(result[:2], [None, None])
        self.assertEqual(result[2], 2.0)
        # smoothing=0.5 时：EMA = 0.5 * 新值 + 0.5 * 旧EMA
        self.assertAlmostEqual(result[3], 0.5 * 4 + 0.5 * 2)
    
    def test_window_one(self):
        """窗口为1"""
        data = [1, 2, 3, 4, 5]
        result = exponential_moving_average(data, 1)
        # 窗口1时，EMA应该等于当前值
        self.assertEqual(result, data)


class TestWeightedMovingAverage(unittest.TestCase):
    """加权移动平均测试"""
    
    def test_basic(self):
        """基础测试"""
        data = [1, 2, 3, 4, 5]
        result = weighted_moving_average(data, 3)
        self.assertEqual(result[:2], [None, None])
        # 1*1 + 2*2 + 3*3 / (1+2+3) = 14/6 ≈ 2.333
        self.assertAlmostEqual(result[2], 14/6, places=5)
        # 2*1 + 3*2 + 4*3 / 6 = 20/6 ≈ 3.333
        self.assertAlmostEqual(result[3], 20/6, places=5)
    
    def test_window_one(self):
        """窗口为1"""
        data = [1, 2, 3]
        result = weighted_moving_average(data, 1)
        self.assertEqual(result, [1.0, 2.0, 3.0])


class TestCumulativeMovingAverage(unittest.TestCase):
    """累积移动平均测试"""
    
    def test_basic(self):
        """基础测试"""
        data = [1, 2, 3, 4, 5]
        result = cumulative_moving_average(data)
        self.assertEqual(result[0], 1.0)
        self.assertEqual(result[1], 1.5)
        self.assertEqual(result[2], 2.0)
        self.assertEqual(result[3], 2.5)
        self.assertEqual(result[4], 3.0)
    
    def test_empty(self):
        """空数据"""
        result = cumulative_moving_average([])
        self.assertEqual(result, [])


class TestTriangularMovingAverage(unittest.TestCase):
    """三角移动平均测试"""
    
    def test_basic(self):
        """基础测试"""
        data = [1, 2, 3, 4, 5, 6, 7]
        result = triangular_moving_average(data, 3)
        # TMA是SMA的SMA
        self.assertIsNotNone(result)


class TestHullMovingAverage(unittest.TestCase):
    """Hull移动平均测试"""
    
    def test_basic(self):
        """基础测试"""
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        result = hull_moving_average(data, 5)
        self.assertIsNotNone(result)
        # 检查前面有None
        self.assertTrue(any(v is None for v in result))


class TestKaufmanAdaptiveMovingAverage(unittest.TestCase):
    """KAMA测试"""
    
    def test_basic(self):
        """基础测试"""
        data = list(range(1, 21))
        result = kaufman_adaptive_moving_average(data, 10)
        self.assertIsNotNone(result)
        # 前面应该有None
        self.assertTrue(result[9] is None)
        self.assertTrue(result[10] is not None)
    
    def test_trending_data(self):
        """趋势数据"""
        # 强趋势数据
        data = list(range(1, 31))
        result = kaufman_adaptive_moving_average(data, 5)
        # KAMA应该快速跟随趋势
        self.assertTrue(any(v is not None for v in result))


class TestVolumeWeightedMovingAverage(unittest.TestCase):
    """成交量加权移动平均测试"""
    
    def test_basic(self):
        """基础测试"""
        prices = [10, 11, 12, 13, 14]
        volumes = [100, 200, 150, 300, 250]
        result = volume_weighted_moving_average(prices, volumes, 3)
        
        self.assertEqual(result[:2], [None, None])
        # 第三个值：(10*100 + 11*200 + 12*150) / (100+200+150)
        expected = (10*100 + 11*200 + 12*150) / 450
        self.assertAlmostEqual(result[2], expected, places=5)
    
    def test_length_mismatch(self):
        """价格和成交量长度不一致"""
        with self.assertRaises(ValueError):
            volume_weighted_moving_average([1, 2, 3], [100, 200], 2)


class TestMACD(unittest.TestCase):
    """MACD测试"""
    
    def test_basic(self):
        """基础测试"""
        data = list(range(1, 50))
        macd_line, signal_line, histogram = moving_average_convergence_divergence(
            data, fast_period=12, slow_period=26, signal_period=9
        )
        
        # 检查长度
        self.assertEqual(len(macd_line), len(data))
        self.assertEqual(len(signal_line), len(data))
        self.assertEqual(len(histogram), len(data))
        
        # 前面应该有None（slow_period-1 = 25个None）
        self.assertEqual(macd_line[:25], [None] * 25)
        # 第26个（索引25）应该有值（EMA slow开始计算）
        self.assertIsNotNone(macd_line[25])
    
    def test_invalid_periods(self):
        """无效周期"""
        with self.assertRaises(ValueError):
            moving_average_convergence_divergence([1, 2, 3], fast_period=0)
        with self.assertRaises(ValueError):
            moving_average_convergence_divergence([1, 2, 3], fast_period=26, slow_period=12)


class TestAverageTrueRange(unittest.TestCase):
    """ATR测试"""
    
    def test_basic(self):
        """基础测试"""
        highs = [15, 17, 16, 18, 20, 22, 21, 23, 24, 25]
        lows = [10, 12, 11, 13, 15, 17, 16, 18, 19, 20]
        closes = [14, 15, 14, 17, 18, 20, 19, 21, 22, 23]
        
        result = average_true_range(highs, lows, closes, window=3)
        
        self.assertEqual(len(result), len(highs))
        # ATR需要window-1个前置None，从window-1索引开始有值
        self.assertIsNone(result[1])  # 前2个是None
        self.assertIsNotNone(result[2])  # 第3个开始有值
    
    def test_length_mismatch(self):
        """长度不一致"""
        with self.assertRaises(ValueError):
            average_true_range([1, 2], [1, 2, 3], [1, 2], 2)


class TestBollingerBands(unittest.TestCase):
    """布林带测试"""
    
    def test_basic(self):
        """基础测试"""
        data = list(range(1, 31))
        upper, middle, lower = bollinger_bands(data, window=5, num_std=2.0)
        
        # 检查长度
        self.assertEqual(len(upper), len(data))
        self.assertEqual(len(middle), len(data))
        self.assertEqual(len(lower), len(data))
        
        # 检查中间轨道是SMA
        sma = simple_moving_average(data, 5)
        self.assertEqual(middle, sma)
        
        # 检查上轨 > 中轨 > 下轨
        for i in range(4, len(data)):
            if upper[i] is not None:
                self.assertGreater(upper[i], middle[i])
                self.assertGreater(middle[i], lower[i])
    
    def test_invalid_params(self):
        """无效参数"""
        with self.assertRaises(ValueError):
            bollinger_bands([1, 2, 3], window=0)
        with self.assertRaises(ValueError):
            bollinger_bands([1, 2, 3], window=3, num_std=-1)


class TestRollingStatistics(unittest.TestCase):
    """滚动统计量测试"""
    
    def test_basic(self):
        """基础测试"""
        data = [1, 2, 3, 4, 5]
        stats = rolling_statistics(data, 3, ['mean', 'std', 'min', 'max'])
        
        # 检查所有统计量都有
        self.assertIn('mean', stats)
        self.assertIn('std', stats)
        self.assertIn('min', stats)
        self.assertIn('max', stats)
        
        # 检查值
        self.assertEqual(stats['mean'][:2], [None, None])
        self.assertEqual(stats['mean'][2], 2.0)
        self.assertEqual(stats['min'][2], 1)
        self.assertEqual(stats['max'][2], 3)
    
    def test_all_stats(self):
        """所有统计量"""
        data = [1, 2, 3, 4, 5]
        all_stats = ['mean', 'std', 'var', 'min', 'max', 'sum', 'median']
        stats = rolling_statistics(data, 3, all_stats)
        
        for s in all_stats:
            self.assertIn(s, stats)
        
        # 检查中位数
        self.assertEqual(stats['median'][2], 2.0)  # [1,2,3] median=2
        self.assertEqual(stats['median'][3], 3.0)  # [2,3,4] median=3
    
    def test_invalid_stat(self):
        """无效统计量"""
        with self.assertRaises(ValueError):
            rolling_statistics([1, 2, 3], 2, ['invalid_stat'])


class TestMovingAverageClass(unittest.TestCase):
    """MovingAverage类测试"""
    
    def test_sma(self):
        """SMA类接口"""
        ma = MovingAverage(window=3, method='sma')
        
        self.assertIsNone(ma.update(1))
        self.assertIsNone(ma.update(2))
        self.assertEqual(ma.update(3), 2.0)
        self.assertEqual(ma.update(4), 3.0)
    
    def test_ema(self):
        """EMA类接口"""
        ma = MovingAverage(window=3, method='ema')
        
        self.assertIsNone(ma.update(1))
        self.assertIsNone(ma.update(2))
        self.assertEqual(ma.update(3), 2.0)
        self.assertIsNotNone(ma.update(4))
    
    def test_invalid_method(self):
        """无效方法"""
        with self.assertRaises(ValueError):
            MovingAverage(window=3, method='invalid')
    
    def test_reset(self):
        """重置"""
        ma = MovingAverage(window=3, method='sma')
        ma.update(1)
        ma.update(2)
        ma.update(3)
        
        self.assertEqual(len(ma.data), 3)
        ma.reset()
        self.assertEqual(len(ma.data), 0)
    
    def test_compute(self):
        """批量计算"""
        ma = MovingAverage(window=3, method='sma')
        data = [1, 2, 3, 4, 5]
        
        result = ma.compute(data)
        self.assertEqual(result[:2], [None, None])
        self.assertEqual(result[2], 2.0)
    
    def test_current(self):
        """当前值"""
        ma = MovingAverage(window=3, method='sma')
        ma.update(1)
        ma.update(2)
        
        self.assertIsNone(ma.current)
        ma.update(3)
        self.assertEqual(ma.current, 2.0)


if __name__ == "__main__":
    unittest.main()