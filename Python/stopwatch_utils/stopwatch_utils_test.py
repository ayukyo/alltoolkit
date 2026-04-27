"""
StopWatch Utils 测试文件

测试秒表计时工具的所有核心功能。
"""

import sys
import os
import time
import threading
import unittest

# Add module directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mod import (
    StopWatch,
    LapTimer,
    Timer,
    PerformanceTimer,
    StopwatchContext,
    timed,
    measure_time,
    countdown
)


class TestStopWatch(unittest.TestCase):
    """StopWatch 类测试"""
    
    def test_basic_start_stop(self):
        """测试基本启动和暂停"""
        sw = StopWatch()
        self.assertFalse(sw.is_running)
        
        sw.start()
        self.assertTrue(sw.is_running)
        
        time.sleep(0.1)
        elapsed = sw.elapsed()
        self.assertGreater(elapsed, 0.09)
        self.assertLess(elapsed, 0.2)
        
        sw.pause()
        self.assertTrue(sw.is_paused)
        elapsed_paused = sw.elapsed()
        
        time.sleep(0.1)
        # 暂停后时间不应增加
        self.assertAlmostEqual(elapsed_paused, sw.elapsed(), places=3)
    
    def test_reset(self):
        """测试重置"""
        sw = StopWatch(auto_start=True)
        time.sleep(0.1)
        self.assertGreater(sw.elapsed(), 0.05)
        
        sw.reset()
        self.assertFalse(sw.is_running)
        self.assertEqual(sw.elapsed(), 0.0)
    
    def test_pause_resume(self):
        """测试暂停和恢复"""
        sw = StopWatch()
        sw.start()
        time.sleep(0.1)
        sw.pause()
        
        paused_elapsed = sw.elapsed()
        time.sleep(0.1)
        
        sw.resume()
        time.sleep(0.1)
        
        final_elapsed = sw.elapsed()
        # 恢复后时间应该增加
        self.assertGreater(final_elapsed, paused_elapsed)
    
    def test_elapsed_units(self):
        """测试不同时间单位"""
        sw = StopWatch(auto_start=True)
        time.sleep(0.1)
        
        seconds = sw.elapsed('seconds')
        milliseconds = sw.elapsed('milliseconds')
        microseconds = sw.elapsed('microseconds')
        
        # 验证单位转换关系（允许一定误差）
        self.assertAlmostEqual(seconds * 1000, milliseconds, places=0)
        self.assertAlmostEqual(seconds * 1000000, microseconds, places=-1)  # 允许更大的误差范围
    
    def test_elapsed_str(self):
        """测试格式化时间字符串"""
        sw = StopWatch()
        
        # 测试微秒级
        sw.start()
        time.sleep(0.0005)  # 500 微秒
        result = sw.elapsed_str()
        self.assertIn('μs', result)
        sw.reset()
        
        # 测试毫秒级
        sw.start()
        time.sleep(0.05)  # 50 毫秒
        result = sw.elapsed_str()
        self.assertIn('ms', result)
        sw.reset()
        
        # 测试秒级
        sw.start()
        time.sleep(0.5)
        result = sw.elapsed_str()
        self.assertIn('s', result)
    
    def test_context_manager(self):
        """测试上下文管理器"""
        with StopWatch() as sw:
            self.assertTrue(sw.is_running)
            time.sleep(0.1)
        
        self.assertTrue(sw.is_paused)
        self.assertGreater(sw.elapsed(), 0.09)
    
    def test_chain_calls(self):
        """测试链式调用"""
        sw = StopWatch().start()
        time.sleep(0.05)
        sw.pause().resume().reset()
        self.assertEqual(sw.elapsed(), 0.0)


class TestLapTimer(unittest.TestCase):
    """LapTimer 类测试"""
    
    def test_lap_recording(self):
        """测试圈记录"""
        timer = LapTimer(auto_start=True)
        time.sleep(0.1)
        lap1 = timer.lap("第一圈")
        
        self.assertEqual(lap1.lap_number, 1)
        self.assertEqual(lap1.label, "第一圈")
        self.assertGreater(lap1.lap_time, 0.09)
        
        time.sleep(0.05)
        lap2 = timer.lap("第二圈")
        
        self.assertEqual(lap2.lap_number, 2)
        self.assertLess(lap2.lap_time, lap1.lap_time)  # 第二圈更快
    
    def test_get_laps(self):
        """测试获取所有圈记录"""
        timer = LapTimer(auto_start=True)
        for _ in range(3):
            time.sleep(0.03)
            timer.lap()
        
        laps = timer.get_laps()
        self.assertEqual(len(laps), 3)
    
    def test_fastest_slowest_lap(self):
        """测试最快和最慢圈"""
        timer = LapTimer(auto_start=True)
        
        # 创建不同的圈时间
        time.sleep(0.1)  # 慢圈
        timer.lap("慢圈")
        
        time.sleep(0.02)  # 快圈
        timer.lap("快圈")
        
        time.sleep(0.05)  # 中等圈
        timer.lap("中等圈")
        
        fastest = timer.get_fastest_lap()
        slowest = timer.get_slowest_lap()
        
        self.assertEqual(fastest.label, "快圈")
        self.assertEqual(slowest.label, "慢圈")
    
    def test_average_lap(self):
        """测试平均圈用时"""
        timer = LapTimer(auto_start=True)
        
        for _ in range(3):
            time.sleep(0.05)
            timer.lap()
        
        avg = timer.get_average_lap()
        self.assertGreater(avg, 0.04)
        self.assertLess(avg, 0.1)
    
    def test_reset_clears_laps(self):
        """测试重置清除圈记录"""
        timer = LapTimer(auto_start=True)
        timer.lap()
        timer.lap()
        
        timer.reset()
        
        self.assertEqual(len(timer.get_laps()), 0)
    
    def test_summary(self):
        """测试摘要输出"""
        timer = LapTimer(auto_start=True)
        time.sleep(0.05)
        timer.lap("测试圈")
        
        summary = timer.summary()
        self.assertIn("总计时间", summary)
        self.assertIn("圈数: 1", summary)
        self.assertIn("测试圈", summary)


class TestTimer(unittest.TestCase):
    """Timer 类测试"""
    
    def test_countdown(self):
        """测试倒计时"""
        result = []
        
        def on_complete():
            result.append("completed")
        
        timer = Timer(0.5, callback=on_complete, auto_start=True)
        self.assertTrue(timer.is_running)
        
        time.sleep(0.6)
        
        self.assertEqual(result, ["completed"])
        self.assertFalse(timer.is_running)
    
    def test_cancel(self):
        """测试取消倒计时"""
        result = []
        
        def on_complete():
            result.append("should not happen")
        
        timer = Timer(1.0, callback=on_complete, auto_start=True)
        timer.cancel()
        
        time.sleep(1.1)
        
        self.assertEqual(result, [])  # 回调不应执行
    
    def test_pause_resume(self):
        """测试暂停和恢复"""
        result = []
        
        def on_complete():
            result.append("completed")
        
        timer = Timer(0.3, callback=on_complete)
        timer.start()
        time.sleep(0.1)
        timer.pause()
        
        remaining = timer.remaining()
        self.assertLess(remaining, 0.25)
        self.assertGreater(remaining, 0.1)
        
        time.sleep(0.3)  # 暂停期间，倒计时不应完成
        self.assertEqual(result, [])
        
        timer.resume()
        time.sleep(0.25)
        self.assertEqual(result, ["completed"])
    
    def test_remaining(self):
        """测试剩余时间"""
        timer = Timer(2.0, auto_start=True)
        
        time.sleep(0.5)
        remaining = timer.remaining()
        self.assertLess(remaining, 1.6)
        self.assertGreater(remaining, 1.4)


class TestPerformanceTimer(unittest.TestCase):
    """PerformanceTimer 类测试"""
    
    def test_single_measurement(self):
        """测试单次测量"""
        perf = PerformanceTimer("测试")
        
        with perf:
            time.sleep(0.1)
        
        self.assertEqual(perf.count(), 1)
        self.assertGreater(perf.elapsed(), 0.09)
    
    def test_multiple_measurements(self):
        """测试多次测量"""
        perf = PerformanceTimer("测试")
        
        for _ in range(5):
            with perf.measure():
                time.sleep(0.02)
        
        self.assertEqual(perf.count(), 5)
        self.assertGreater(perf.average(), 0.01)
    
    def test_statistics(self):
        """测试统计数据"""
        perf = PerformanceTimer("测试")
        
        for sleep_time in [0.02, 0.05, 0.03]:
            with perf.measure():
                time.sleep(sleep_time)
        
        stats = perf.statistics()
        
        self.assertEqual(stats['name'], "测试")
        self.assertEqual(stats['count'], 3)
        self.assertGreater(stats['min'], 0.01)
        self.assertGreater(stats['max'], 0.04)
        self.assertGreater(stats['average'], 0.02)
    
    def test_context_manager(self):
        """测试上下文管理器"""
        with PerformanceTimer("测试") as perf:
            time.sleep(0.05)
        
        self.assertEqual(perf.count(), 1)
    
    def test_summary(self):
        """测试摘要输出"""
        perf = PerformanceTimer("性能测试")
        with perf.measure():
            time.sleep(0.01)
        
        summary = perf.summary()
        self.assertIn("性能测试", summary)
        self.assertIn("测量次数: 1", summary)


class TestDecorators(unittest.TestCase):
    """装饰器测试"""
    
    def test_timed_decorator(self):
        """测试计时装饰器"""
        @timed("测试函数", print_result=False)
        def slow_function():
            time.sleep(0.1)
            return "result"
        
        result = slow_function()
        self.assertEqual(result, "result")
    
    def test_timed_decorator_default_name(self):
        """测试默认函数名"""
        @timed(print_result=False)
        def my_function():
            return 42
        
        result = my_function()
        self.assertEqual(result, 42)


class TestConvenienceFunctions(unittest.TestCase):
    """便捷函数测试"""
    
    def test_measure_time(self):
        """测试测量函数时间"""
        def slow_func(x):
            time.sleep(0.1)
            return x * 2
        
        result, elapsed = measure_time(slow_func, 5)
        
        self.assertEqual(result, 10)
        self.assertGreater(elapsed, 0.09)
    
    def test_countdown(self):
        """测试倒计时函数"""
        results = []
        
        countdown(3, callback=lambda s: results.append(s), interval=0.1)
        
        self.assertEqual(results, [3, 2, 1])


class TestStopwatchContext(unittest.TestCase):
    """StopwatchContext 测试"""
    
    def test_basic_usage(self):
        """测试基本用法"""
        with StopwatchContext("测试操作", print_result=False):
            time.sleep(0.05)
        # 不应抛出异常
    
    def test_without_name(self):
        """测试无名称"""
        with StopwatchContext(print_result=False):
            time.sleep(0.01)


if __name__ == '__main__':
    unittest.main(verbosity=2)