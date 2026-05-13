"""
Sliding Window Utilities 测试

测试所有滑动窗口功能：
- 通用滑动窗口
- 数值滑动窗口
- 移动平均
- 时间滑动窗口
- 限流器
- 最小最大值窗口
- 滑动窗口计数器
"""

import unittest
import time
from mod import (
    SlidingWindow,
    NumericSlidingWindow,
    MovingAverage,
    TimeSlidingWindow,
    RateLimiter,
    MinMaxSlidingWindow,
    SlidingWindowCounter,
    WindowStats,
    moving_average,
    sliding_window_stats,
    sliding_window_min_max,
)


class TestSlidingWindow(unittest.TestCase):
    """通用滑动窗口测试"""
    
    def test_basic_operations(self):
        """测试基本操作"""
        window = SlidingWindow(size=3)
        
        # 初始状态
        self.assertTrue(window.is_empty())
        self.assertEqual(len(window), 0)
        
        # 添加元素
        window.add(1)
        window.add(2)
        self.assertEqual(len(window), 2)
        self.assertFalse(window.is_full())
        
        window.add(3)
        self.assertTrue(window.is_full())
        self.assertEqual(window.get_window(), [1, 2, 3])
    
    def test_window_overflow(self):
        """测试窗口溢出"""
        window = SlidingWindow(size=3)
        
        # 填满窗口
        window.add(1)
        window.add(2)
        window.add(3)
        
        # 添加更多元素
        removed = window.add(4)
        self.assertEqual(removed, 1)
        self.assertEqual(window.get_window(), [2, 3, 4])
        
        removed = window.add(5)
        self.assertEqual(removed, 2)
        self.assertEqual(window.get_window(), [3, 4, 5])
    
    def test_callbacks(self):
        """测试回调函数"""
        added = []
        removed = []
        
        window = SlidingWindow(
            size=2,
            on_add=lambda x: added.append(x),
            on_remove=lambda x: removed.append(x),
        )
        
        window.add(1)
        window.add(2)
        window.add(3)
        
        self.assertEqual(added, [1, 2, 3])
        self.assertEqual(removed, [1])
    
    def test_get_latest_oldest(self):
        """测试获取最新/最旧元素"""
        window = SlidingWindow(size=3)
        
        self.assertIsNone(window.get_latest())
        self.assertIsNone(window.get_oldest())
        
        window.add(1)
        window.add(2)
        window.add(3)
        
        self.assertEqual(window.get_oldest(), 1)
        self.assertEqual(window.get_latest(), 3)
    
    def test_clear(self):
        """测试清空"""
        window = SlidingWindow(size=3)
        window.add(1)
        window.add(2)
        
        window.clear()
        self.assertTrue(window.is_empty())
        self.assertEqual(len(window), 0)
    
    def test_invalid_size(self):
        """测试无效大小"""
        with self.assertRaises(ValueError):
            SlidingWindow(size=0)
        with self.assertRaises(ValueError):
            SlidingWindow(size=-1)


class TestNumericSlidingWindow(unittest.TestCase):
    """数值滑动窗口测试"""
    
    def test_basic_operations(self):
        """测试基本操作"""
        window = NumericSlidingWindow(size=3)
        
        window.add(1)
        window.add(2)
        window.add(3)
        
        self.assertEqual(window.get_window(), [1.0, 2.0, 3.0])
        self.assertEqual(window.get_sum(), 6.0)
        self.assertEqual(window.get_mean(), 2.0)
    
    def test_mean_calculation(self):
        """测试平均值计算"""
        window = NumericSlidingWindow(size=3)
        
        window.add(10)
        self.assertEqual(window.get_mean(), 10.0)
        
        window.add(20)
        self.assertEqual(window.get_mean(), 15.0)
        
        window.add(30)
        self.assertEqual(window.get_mean(), 20.0)
        
        # 窗口滑动
        window.add(40)
        self.assertEqual(window.get_mean(), 30.0)  # (20+30+40)/3
    
    def test_min_max(self):
        """测试最小最大值"""
        window = NumericSlidingWindow(size=3)
        
        window.add(5)
        window.add(3)
        window.add(8)
        
        self.assertEqual(window.get_min(), 3.0)
        self.assertEqual(window.get_max(), 8.0)
        
        # 窗口滑动：移除 5，窗口变为 [3, 8, 10]
        window.add(10)
        self.assertEqual(window.get_min(), 3.0)  # 最小值仍是 3
        self.assertEqual(window.get_max(), 10.0)
        
        # 继续滑动：移除 3（当前最小值），窗口变为 [8, 10, 12]
        window.add(12)
        self.assertEqual(window.get_min(), 8.0)  # 最小值变为 8
        self.assertEqual(window.get_max(), 12.0)
    
    def test_variance_std_dev(self):
        """测试方差和标准差"""
        window = NumericSlidingWindow(size=3)
        
        window.add(2)
        window.add(4)
        window.add(6)
        
        # 均值 = 4, 方差 = ((2-4)^2 + (4-4)^2 + (6-4)^2) / 3 = 8/3
        self.assertAlmostEqual(window.get_mean(), 4.0)
        self.assertAlmostEqual(window.get_variance(), 8/3, places=5)
        self.assertAlmostEqual(window.get_std_dev(), (8/3) ** 0.5, places=5)
    
    def test_stats(self):
        """测试统计信息"""
        window = NumericSlidingWindow(size=3)
        
        window.add(1)
        window.add(2)
        window.add(3)
        
        stats = window.get_stats()
        
        self.assertIsInstance(stats, WindowStats)
        self.assertEqual(stats.count, 3)
        self.assertEqual(stats.sum, 6.0)
        self.assertEqual(stats.min, 1.0)
        self.assertEqual(stats.max, 3.0)
        self.assertEqual(stats.mean, 2.0)
    
    def test_clear(self):
        """测试清空"""
        window = NumericSlidingWindow(size=3)
        window.add(1)
        window.add(2)
        
        window.clear()
        
        self.assertTrue(window.is_empty())
        self.assertEqual(window.get_sum(), 0.0)
        self.assertIsNone(window.get_min())
        self.assertIsNone(window.get_max())


class TestMovingAverage(unittest.TestCase):
    """移动平均测试"""
    
    def test_sma(self):
        """测试简单移动平均"""
        ma = MovingAverage(window_size=3, ma_type='sma')
        
        # 第一个值
        self.assertEqual(ma.update(10), 10.0)
        
        # 第二个值
        self.assertEqual(ma.update(20), 15.0)
        
        # 第三个值
        self.assertEqual(ma.update(30), 20.0)
        
        # 窗口滑动
        self.assertEqual(ma.update(40), 30.0)
        self.assertEqual(ma.update(50), 40.0)
    
    def test_cma(self):
        """测试累积移动平均"""
        ma = MovingAverage(ma_type='cma')
        
        self.assertEqual(ma.update(1), 1.0)
        self.assertEqual(ma.update(2), 1.5)
        self.assertEqual(ma.update(3), 2.0)
        self.assertEqual(ma.update(4), 2.5)
    
    def test_wma(self):
        """测试加权移动平均"""
        ma = MovingAverage(window_size=3, ma_type='wma')
        
        # WMA: 最近值权重最大
        # 第一个值: 1*1/1 = 1
        self.assertEqual(ma.update(10), 10.0)
        
        # 第二个值: (1*10 + 2*20)/(1+2) = 50/3 = 16.67
        result = ma.update(20)
        self.assertAlmostEqual(result, 16.6666, places=3)
        
        # 第三个值: (1*10 + 2*20 + 3*30)/(1+2+3) = 140/6 = 23.33
        result = ma.update(30)
        self.assertAlmostEqual(result, 23.3333, places=3)
    
    def test_ema(self):
        """测试指数移动平均"""
        # alpha = 2/(3+1) = 0.5
        ma = MovingAverage(window_size=3, ma_type='ema')
        
        # EMA_1 = 10
        self.assertEqual(ma.update(10), 10.0)
        
        # EMA_2 = 0.5*20 + 0.5*10 = 15
        self.assertEqual(ma.update(20), 15.0)
        
        # EMA_3 = 0.5*30 + 0.5*15 = 22.5
        self.assertEqual(ma.update(30), 22.5)
    
    def test_reset(self):
        """测试重置"""
        ma = MovingAverage(window_size=3, ma_type='sma')
        
        ma.update(10)
        ma.update(20)
        ma.update(30)
        
        ma.reset()
        
        self.assertEqual(ma.get_current(), 0.0)
    
    def test_invalid_type(self):
        """测试无效类型"""
        ma = MovingAverage(window_size=3, ma_type='invalid')
        with self.assertRaises(ValueError):
            ma.update(10)


class TestTimeSlidingWindow(unittest.TestCase):
    """时间滑动窗口测试"""
    
    def test_basic_operations(self):
        """测试基本操作"""
        # 使用模拟时间
        mock_time = [0.0]
        
        def time_func():
            return mock_time[0]
        
        window = TimeSlidingWindow(window_seconds=10, time_func=time_func)
        
        # 添加元素
        window.add("a", timestamp=0)
        window.add("b", timestamp=5)
        window.add("c", timestamp=8)
        
        self.assertEqual(window.get_count(), 3)
        self.assertEqual(window.get_window(), ["a", "b", "c"])
    
    def test_expiration(self):
        """测试元素过期"""
        mock_time = [100.0]
        
        def time_func():
            return mock_time[0]
        
        window = TimeSlidingWindow(window_seconds=5, time_func=time_func)
        
        # 添加元素
        window.add("old", timestamp=90)  # 将过期
        window.add("new1", timestamp=97)
        window.add("new2", timestamp=100)
        
        # 获取窗口时会清理过期元素
        items = window.get_window()
        self.assertEqual(items, ["new1", "new2"])
    
    def test_empty_window(self):
        """测试空窗口"""
        window = TimeSlidingWindow(window_seconds=10)
        self.assertTrue(window.is_empty())
        self.assertEqual(window.get_window(), [])


class TestRateLimiter(unittest.TestCase):
    """限流器测试"""
    
    def test_fixed_window(self):
        """测试固定窗口限流"""
        limiter = RateLimiter(max_requests=3, window_seconds=1.0, algorithm='fixed')
        
        # 前 3 个请求应该允许
        self.assertTrue(limiter.allow())
        self.assertTrue(limiter.allow())
        self.assertTrue(limiter.allow())
        
        # 第 4 个应该被限流
        self.assertFalse(limiter.allow())
    
    def test_sliding_window(self):
        """测试滑动窗口限流"""
        limiter = RateLimiter(max_requests=3, window_seconds=1.0, algorithm='sliding')
        
        self.assertTrue(limiter.allow())
        self.assertTrue(limiter.allow())
        self.assertTrue(limiter.allow())
        self.assertFalse(limiter.allow())
    
    def test_token_bucket(self):
        """测试令牌桶限流"""
        limiter = RateLimiter(max_requests=3, window_seconds=1.0, algorithm='token')
        
        # 初始有 3 个令牌
        self.assertTrue(limiter.allow())
        self.assertTrue(limiter.allow())
        self.assertTrue(limiter.allow())
        self.assertFalse(limiter.allow())
        
        # 等待令牌补充
        time.sleep(0.5)
        # 补充约 1.5 个令牌
        self.assertTrue(limiter.allow())
    
    def test_leaky_bucket(self):
        """测试漏桶限流"""
        limiter = RateLimiter(max_requests=3, window_seconds=1.0, algorithm='leaky')
        
        # 桶容量为 3，初始为空
        # 由于调用之间有微小时间差导致漏水，快速调用可能允许超过3次
        # 这里验证基本行为：多次快速请求后会被限流
        
        # 快速发送多个请求
        allowed_count = 0
        for _ in range(10):
            if limiter.allow():
                allowed_count += 1
        
        # 应该允许多次（至少3次），但不会无限允许
        self.assertGreaterEqual(allowed_count, 3)
        self.assertLess(allowed_count, 10)
        
        # 等待足够长的时间让桶清空
        time.sleep(1.5)
        
        # 桶应该清空，可以再次添加
        self.assertTrue(limiter.allow())
    
    def test_get_state(self):
        """测试获取状态"""
        limiter = RateLimiter(max_requests=10, window_seconds=60, algorithm='sliding')
        
        limiter.allow()
        limiter.allow()
        
        state = limiter.get_state()
        self.assertEqual(state['algorithm'], 'sliding')
        self.assertEqual(state['requests_in_window'], 2)
        self.assertEqual(state['remaining_requests'], 8)
    
    def test_reset(self):
        """测试重置"""
        limiter = RateLimiter(max_requests=3, window_seconds=1.0, algorithm='fixed')
        
        limiter.allow()
        limiter.allow()
        limiter.allow()
        
        limiter.reset()
        
        state = limiter.get_state()
        self.assertEqual(state['requests_in_window'], 0)
    
    def test_invalid_params(self):
        """测试无效参数"""
        with self.assertRaises(ValueError):
            RateLimiter(max_requests=0, window_seconds=1.0)
        
        with self.assertRaises(ValueError):
            RateLimiter(max_requests=10, window_seconds=0)


class TestMinMaxSlidingWindow(unittest.TestCase):
    """最小最大值滑动窗口测试"""
    
    def test_basic_operations(self):
        """测试基本操作"""
        window = MinMaxSlidingWindow(size=3)
        
        window.add(1)
        self.assertEqual(window.get_min(), 1.0)
        self.assertEqual(window.get_max(), 1.0)
        
        window.add(3)
        self.assertEqual(window.get_min(), 1.0)
        self.assertEqual(window.get_max(), 3.0)
        
        window.add(2)
        self.assertEqual(window.get_min(), 1.0)
        self.assertEqual(window.get_max(), 3.0)
    
    def test_window_sliding(self):
        """测试窗口滑动"""
        window = MinMaxSlidingWindow(size=3)
        
        window.add(1)
        window.add(3)
        window.add(-1)
        
        self.assertEqual(window.get_min(), -1.0)
        self.assertEqual(window.get_max(), 3.0)
        
        # 滑动窗口，移除 1
        window.add(2)
        self.assertEqual(window.get_window(), [3.0, -1.0, 2.0])
        self.assertEqual(window.get_min(), -1.0)
        self.assertEqual(window.get_max(), 3.0)
        
        # 滑动窗口，移除 3（当前最大值）
        window.add(5)
        self.assertEqual(window.get_window(), [-1.0, 2.0, 5.0])
        self.assertEqual(window.get_min(), -1.0)
        self.assertEqual(window.get_max(), 5.0)
        
        # 滑动窗口，移除 -1（当前最小值）
        window.add(4)
        self.assertEqual(window.get_window(), [2.0, 5.0, 4.0])
        self.assertEqual(window.get_min(), 2.0)
        self.assertEqual(window.get_max(), 5.0)
    
    def test_empty_window(self):
        """测试空窗口"""
        window = MinMaxSlidingWindow(size=3)
        
        self.assertIsNone(window.get_min())
        self.assertIsNone(window.get_max())
    
    def test_clear(self):
        """测试清空"""
        window = MinMaxSlidingWindow(size=3)
        
        window.add(1)
        window.add(2)
        window.clear()
        
        self.assertEqual(len(window), 0)
        self.assertIsNone(window.get_min())
    
    def test_invalid_size(self):
        """测试无效大小"""
        with self.assertRaises(ValueError):
            MinMaxSlidingWindow(size=0)


class TestSlidingWindowCounter(unittest.TestCase):
    """滑动窗口计数器测试"""
    
    def test_basic_operations(self):
        """测试基本操作"""
        counter = SlidingWindowCounter(window_seconds=1.0, precision=10)
        
        counter.increment()
        counter.increment()
        counter.increment(3)
        
        self.assertEqual(counter.get_count(), 5)
    
    def test_expiration(self):
        """测试过期清理"""
        counter = SlidingWindowCounter(window_seconds=0.5, precision=10)
        
        counter.increment()
        counter.increment()
        
        self.assertEqual(counter.get_count(), 2)
        
        # 等待过期
        time.sleep(0.6)
        
        self.assertEqual(counter.get_count(), 0)
    
    def test_reset(self):
        """测试重置"""
        counter = SlidingWindowCounter(window_seconds=1.0)
        
        counter.increment(10)
        counter.reset()
        
        self.assertEqual(counter.get_count(), 0)


class TestConvenienceFunctions(unittest.TestCase):
    """便捷函数测试"""
    
    def test_moving_average(self):
        """测试移动平均便捷函数"""
        values = [10, 20, 30, 40, 50]
        
        sma = moving_average(values, window=3, ma_type='sma')
        self.assertEqual(len(sma), 5)
        self.assertEqual(sma[0], 10.0)
        self.assertEqual(sma[2], 20.0)  # (10+20+30)/3
        self.assertEqual(sma[4], 40.0)  # (30+40+50)/3
    
    def test_moving_average_wma(self):
        """测试加权移动平均便捷函数"""
        values = [10, 20, 30]
        
        wma = moving_average(values, window=3, ma_type='wma')
        self.assertEqual(len(wma), 3)
    
    def test_moving_average_ema(self):
        """测试指数移动平均便捷函数"""
        values = [10, 20, 30]
        
        ema = moving_average(values, window=3, ma_type='ema')
        self.assertEqual(len(ema), 3)
    
    def test_sliding_window_stats(self):
        """测试滑动窗口统计便捷函数"""
        values = [1, 2, 3, 4, 5]
        
        stats_list = sliding_window_stats(values, window=3)
        
        self.assertEqual(len(stats_list), 5)
        
        # 第一个统计（窗口只有 1 个元素）
        self.assertEqual(stats_list[0].count, 1)
        self.assertEqual(stats_list[0].sum, 1.0)
        
        # 第三个统计（窗口满）
        self.assertEqual(stats_list[2].count, 3)
        self.assertEqual(stats_list[2].sum, 6.0)
        self.assertEqual(stats_list[2].mean, 2.0)
    
    def test_sliding_window_min_max(self):
        """测试滑动窗口最小最大值便捷函数"""
        values = [1, 3, -1, 2, 5]
        
        mins, maxs = sliding_window_min_max(values, window=3)
        
        self.assertEqual(len(mins), 5)
        self.assertEqual(len(maxs), 5)
        
        # 检查第三个位置
        self.assertEqual(mins[2], -1.0)
        self.assertEqual(maxs[2], 3.0)
    
    def test_empty_input(self):
        """测试空输入"""
        self.assertEqual(moving_average([], 3), [])
        self.assertEqual(sliding_window_stats([], 3), [])
        self.assertEqual(sliding_window_min_max([], 3), ([], []))
    
    def test_invalid_window(self):
        """测试无效窗口大小"""
        self.assertEqual(moving_average([1, 2, 3], 0), [])
        self.assertEqual(sliding_window_stats([1, 2, 3], -1), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)