"""
倒计时工具模块测试

运行方式：python test_mod.py
"""

import unittest
from datetime import datetime, timedelta
import time
import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    Countdown, CountdownError,
    create_countdown,
    countdown_from_delta,
    multi_countdown,
    format_duration,
    time_until,
    next_occurrence,
    countdown_to_next,
    CountdownTimer,
    days_until,
    hours_until,
    minutes_until
)


class TestCountdown(unittest.TestCase):
    """Countdown 类测试"""
    
    def test_create_with_string(self):
        """测试字符串创建倒计时"""
        future = datetime.now() + timedelta(days=1)
        target_str = future.strftime("%Y-%m-%d %H:%M:%S")
        cd = Countdown(target_str)
        self.assertFalse(cd.is_expired)
        self.assertTrue(cd.total_seconds > 0)
    
    def test_create_with_datetime(self):
        """测试datetime对象创建倒计时"""
        target = datetime.now() + timedelta(hours=2)
        cd = Countdown(target)
        self.assertFalse(cd.is_expired)
    
    def test_create_with_name(self):
        """测试带名称创建"""
        target = datetime.now() + timedelta(days=1)
        cd = Countdown(target, name="测试倒计时")
        self.assertEqual(cd.name, "测试倒计时")
    
    def test_invalid_date_format(self):
        """测试无效日期格式"""
        with self.assertRaises(CountdownError):
            Countdown("invalid-date")
    
    def test_past_target_raises_error(self):
        """测试过去的目标时间应报错"""
        past = datetime.now() - timedelta(days=1)
        with self.assertRaises(CountdownError):
            Countdown(past)
    
    def test_remaining(self):
        """测试剩余时间计算"""
        target = datetime.now() + timedelta(days=1, hours=2, minutes=30)
        cd = Countdown(target)
        remaining = cd.remaining
        
        self.assertIsInstance(remaining, timedelta)
        self.assertTrue(remaining > timedelta(0))
        self.assertTrue(remaining < timedelta(days=2))
    
    def test_get_components(self):
        """测试时间组件获取"""
        target = datetime.now() + timedelta(days=3, hours=5, minutes=10, seconds=30)
        cd = Countdown(target)
        days, hours, minutes, seconds = cd.get_components()
        
        # 允许1秒误差
        self.assertEqual(days, 3)
        self.assertTrue(4 <= hours <= 5)  # 允许边界误差
    
    def test_progress(self):
        """测试进度计算"""
        start = datetime.now()
        target = start + timedelta(hours=2)
        cd = Countdown(target, start=start)
        
        progress = cd.progress
        self.assertTrue(0 <= progress <= 1)
    
    def test_format_default(self):
        """测试默认格式化"""
        target = datetime.now() + timedelta(days=1, hours=2, minutes=30)
        cd = Countdown(target)
        formatted = cd.format()
        
        self.assertIn("天", formatted)
        self.assertIn("小时", formatted)
        self.assertIn("分钟", formatted)
    
    def test_format_compact(self):
        """测试紧凑格式"""
        target = datetime.now() + timedelta(days=1, hours=2)
        cd = Countdown(target)
        formatted = cd.format(style="compact")
        
        self.assertIn("d", formatted)
        self.assertIn("h", formatted)
    
    def test_format_digital(self):
        """测试数字格式"""
        target = datetime.now() + timedelta(days=1, hours=2, minutes=30, seconds=15)
        cd = Countdown(target)
        formatted = cd.format(style="digital")
        
        self.assertTrue(formatted.count(":") >= 3)
    
    def test_format_with_name(self):
        """测试带名称格式化"""
        target = datetime.now() + timedelta(days=1)
        cd = Countdown(target, name="测试")
        formatted = cd.format(include_name=True)
        
        self.assertIn("测试", formatted)
    
    def test_format_expired(self):
        """测试已过期的格式化"""
        start = datetime.now() - timedelta(days=2)
        target = datetime.now() - timedelta(days=1)
        cd = Countdown(target, start=start)
        
        formatted = cd.format()
        self.assertEqual(formatted, "已结束")
    
    def test_progress_bar(self):
        """测试进度条"""
        start = datetime.now()
        target = start + timedelta(hours=1)
        cd = Countdown(target, start=start)
        
        bar = cd.progress_bar()
        self.assertIn("[", bar)
        self.assertIn("]", bar)
        self.assertIn("%", bar)
    
    def test_progress_bar_custom_chars(self):
        """测试自定义进度条字符"""
        start = datetime.now()
        target = start + timedelta(hours=1)
        cd = Countdown(target, start=start)
        
        bar = cd.progress_bar(filled_char="#", empty_char="-")
        # 当进度很小时，可能没有填充字符
        self.assertIn("[", bar)
        self.assertIn("]", bar)
    
    def test_to_dict(self):
        """测试字典转换"""
        target = datetime.now() + timedelta(days=1)
        cd = Countdown(target, name="测试")
        result = cd.to_dict()
        
        self.assertIn("name", result)
        self.assertIn("target", result)
        self.assertIn("remaining_seconds", result)
        self.assertIn("is_expired", result)
        self.assertIn("formatted", result)
    
    def test_expired_countdown(self):
        """测试已过期的倒计时"""
        start = datetime.now() - timedelta(hours=2)
        target = datetime.now() - timedelta(hours=1)
        cd = Countdown(target, start=start)
        
        self.assertTrue(cd.is_expired)
        self.assertEqual(cd.total_seconds, 0)
        self.assertEqual(cd.progress, 1.0)


class TestCreateCountdown(unittest.TestCase):
    """create_countdown 函数测试"""
    
    def test_basic_creation(self):
        """测试基本创建"""
        target = datetime.now() + timedelta(days=1)
        cd = create_countdown(target)
        self.assertIsInstance(cd, Countdown)
    
    def test_with_all_params(self):
        """测试完整参数"""
        start = datetime.now()
        target = start + timedelta(days=1)
        cd = create_countdown(target, start=start, name="测试")
        
        self.assertEqual(cd.name, "测试")


class TestCountdownFromDelta(unittest.TestCase):
    """countdown_from_delta 函数测试"""
    
    def test_from_timedelta(self):
        """测试从timedelta创建"""
        cd = countdown_from_delta(timedelta(hours=2))
        self.assertTrue(cd.total_seconds > 0)
        self.assertTrue(cd.total_seconds <= 7200)
    
    def test_from_seconds(self):
        """测试从秒数创建"""
        cd = countdown_from_delta(3600)  # 1小时
        self.assertTrue(cd.total_seconds > 0)
        self.assertTrue(cd.total_seconds <= 3600)
    
    def test_from_float_seconds(self):
        """测试从浮点秒数创建"""
        cd = countdown_from_delta(1800.5)
        self.assertTrue(cd.total_seconds > 0)
    
    def test_with_name(self):
        """测试带名称创建"""
        cd = countdown_from_delta(3600, name="1小时倒计时")
        self.assertEqual(cd.name, "1小时倒计时")


class TestMultiCountdown(unittest.TestCase):
    """multi_countdown 函数测试"""
    
    def test_multiple_targets(self):
        """测试多个目标"""
        targets = [
            datetime.now() + timedelta(days=1),
            datetime.now() + timedelta(days=2),
            datetime.now() + timedelta(hours=1),
        ]
        results = multi_countdown(targets)
        
        self.assertEqual(len(results), 3)
        # 检查是否按剩余时间排序
        self.assertTrue(
            results[0]["remaining_seconds"] <= results[1]["remaining_seconds"]
        )
    
    def test_with_names(self):
        """测试带名称的批量倒计时"""
        targets = [
            ("任务A", datetime.now() + timedelta(hours=1)),
            ("任务B", datetime.now() + timedelta(hours=2)),
        ]
        results = multi_countdown(targets)
        
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["name"], "任务A")
        self.assertEqual(results[1]["name"], "任务B")
    
    def test_mixed_formats(self):
        """测试混合格式"""
        future = datetime.now() + timedelta(days=1)
        targets = [
            future.strftime("%Y-%m-%d"),
            ("测试", future + timedelta(days=1)),
        ]
        results = multi_countdown(targets)
        
        self.assertEqual(len(results), 2)


class TestFormatDuration(unittest.TestCase):
    """format_duration 函数测试"""
    
    def test_format_seconds(self):
        """测试格式化秒"""
        result = format_duration(45)
        self.assertIn("45", result)
        self.assertIn("秒", result)
    
    def test_format_minutes(self):
        """测试格式化分钟"""
        result = format_duration(180)  # 3分钟
        self.assertIn("3", result)
        self.assertIn("分钟", result)
    
    def test_format_hours(self):
        """测试格式化小时"""
        result = format_duration(7200)  # 2小时
        self.assertIn("2", result)
        self.assertIn("小时", result)
    
    def test_format_days(self):
        """测试格式化天"""
        result = format_duration(172800)  # 2天
        self.assertIn("2", result)
        self.assertIn("天", result)
    
    def test_format_compact(self):
        """测试紧凑格式"""
        result = format_duration(3661, style="compact")
        self.assertIn("h", result)
        self.assertIn("m", result)
        self.assertIn("s", result)
    
    def test_format_digital(self):
        """测试数字格式"""
        result = format_duration(90061, style="digital")
        self.assertEqual(result.count(":"), 3)
    
    def test_format_zero(self):
        """测试零秒"""
        result = format_duration(0)
        self.assertIn("0", result)
    
    def test_format_negative(self):
        """测试负数"""
        result = format_duration(-100)
        self.assertEqual(result, "已结束")


class TestTimeUntil(unittest.TestCase):
    """time_until 函数测试"""
    
    def test_time_until_future(self):
        """测试到未来时间"""
        future = datetime.now() + timedelta(hours=2)
        delta = time_until(future)
        
        self.assertIsInstance(delta, timedelta)
        self.assertTrue(delta > timedelta(0))
        self.assertTrue(delta < timedelta(hours=3))
    
    def test_time_until_string(self):
        """测试字符串时间"""
        future = datetime.now() + timedelta(hours=1)
        future_str = future.strftime("%Y-%m-%d %H:%M:%S")
        delta = time_until(future_str)
        
        self.assertTrue(delta > timedelta(0))


class TestNextOccurrence(unittest.TestCase):
    """next_occurrence 函数测试"""
    
    def test_next_occurrence_future(self):
        """测试未来的时间出现"""
        now = datetime.now()
        target_hour = (now.hour + 2) % 24
        time_str = f"{target_hour:02d}:00"
        
        result = next_occurrence(time_str)
        self.assertIsInstance(result, datetime)
        self.assertEqual(result.hour, target_hour)
    
    def test_next_occurrence_today(self):
        """测试今天的时间"""
        now = datetime.now()
        future_time = now + timedelta(hours=1)
        time_str = future_time.strftime("%H:%M")
        
        result = next_occurrence(time_str, reference=now)
        self.assertTrue(result > now)
    
    def test_next_occurrence_tomorrow(self):
        """测试明天的时间"""
        now = datetime.now()
        past_time = now - timedelta(hours=1)
        time_str = past_time.strftime("%H:%M")
        
        result = next_occurrence(time_str, reference=now)
        self.assertTrue(result > now)
        self.assertTrue(result.date() > now.date())


class TestCountdownToNext(unittest.TestCase):
    """countdown_to_next 函数测试"""
    
    def test_countdown_to_next(self):
        """测试到下一个时间的倒计时"""
        cd = countdown_to_next("23:59", name="午夜")
        
        self.assertEqual(cd.name, "午夜")
        self.assertFalse(cd.is_expired)


class TestCountdownTimer(unittest.TestCase):
    """CountdownTimer 类测试"""
    
    def test_elapsed(self):
        """测试已流逝时间"""
        timer = CountdownTimer()
        time.sleep(0.1)
        elapsed = timer.elapsed()
        
        self.assertIsInstance(elapsed, timedelta)
        self.assertTrue(elapsed >= timedelta(milliseconds=100))
    
    def test_elapsed_seconds(self):
        """测试已流逝秒数"""
        timer = CountdownTimer()
        time.sleep(0.1)
        elapsed = timer.elapsed_seconds()
        
        self.assertTrue(elapsed >= 0.1)
    
    def test_elapsed_formatted(self):
        """测试已流逝时间格式化"""
        timer = CountdownTimer()
        time.sleep(0.1)
        formatted = timer.elapsed_formatted()
        
        self.assertIsInstance(formatted, str)
    
    def test_pause_resume(self):
        """测试暂停和恢复"""
        timer = CountdownTimer()
        time.sleep(0.05)
        timer.pause()
        
        paused_elapsed = timer.elapsed_seconds()
        time.sleep(0.05)
        
        # 暂停期间不应增加时间
        self.assertAlmostEqual(timer.elapsed_seconds(), paused_elapsed, delta=0.01)
        
        timer.resume()
        time.sleep(0.05)
        self.assertTrue(timer.elapsed_seconds() > paused_elapsed)
    
    def test_reset(self):
        """测试重置"""
        timer = CountdownTimer()
        time.sleep(0.1)
        self.assertTrue(timer.elapsed_seconds() > 0.05)
        
        timer.reset()
        self.assertTrue(timer.elapsed_seconds() < 0.05)
    
    def test_lap(self):
        """测试计圈"""
        timer = CountdownTimer()
        time.sleep(0.05)
        
        lap1 = timer.lap()
        self.assertTrue(lap1 >= timedelta(milliseconds=50))
        
        time.sleep(0.05)
        lap2 = timer.lap()
        self.assertTrue(lap2 >= timedelta(milliseconds=50))


class TestConvenienceFunctions(unittest.TestCase):
    """便捷函数测试"""
    
    def test_days_until(self):
        """测试计算天数"""
        future = datetime.now() + timedelta(days=5, hours=1)  # 加一小时确保天数正确
        future_str = future.strftime("%Y-%m-%d")
        
        result = days_until(future_str)
        # 允许误差（可能因为当前时间的时分秒导致差1天）
        self.assertTrue(4 <= result <= 5)
    
    def test_hours_until(self):
        """测试计算小时数"""
        future = datetime.now() + timedelta(hours=25)
        future_str = future.strftime("%Y-%m-%d %H:%M:%S")
        
        result = hours_until(future_str)
        self.assertTrue(24 <= result <= 25)
    
    def test_minutes_until(self):
        """测试计算分钟数"""
        future = datetime.now() + timedelta(minutes=30)
        future_str = future.strftime("%Y-%m-%d %H:%M:%S")
        
        result = minutes_until(future_str)
        self.assertTrue(29 <= result <= 30)


class TestEdgeCases(unittest.TestCase):
    """边界情况测试"""
    
    def test_very_short_countdown(self):
        """测试非常短的倒计时"""
        cd = countdown_from_delta(0.1)  # 0.1秒
        self.assertTrue(cd.total_seconds > 0)
    
    def test_very_long_countdown(self):
        """测试很长的倒计时"""
        cd = countdown_from_delta(timedelta(days=365, hours=1))  # 加一小时确保天数正确
        days, _, _, _ = cd.get_components()
        self.assertTrue(364 <= days <= 365)  # 允许边界误差
    
    def test_unicode_name(self):
        """测试Unicode名称"""
        target = datetime.now() + timedelta(days=1)
        cd = Countdown(target, name="🎉 新年倒计时 🎊")
        
        formatted = cd.format(include_name=True)
        self.assertIn("🎉", formatted)
        self.assertIn("新年", formatted)
    
    def test_chinese_date_format(self):
        """测试中文日期格式"""
        # 注意：这里测试解析中文格式
        cd = countdown_from_delta(timedelta(days=1, hours=1))  # 确保超过1天
        # 中文格式解析需要特殊处理
        formatted = cd.format(style="chinese")
        self.assertIn("天", formatted)


def run_tests():
    """运行所有测试"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加所有测试类
    suite.addTests(loader.loadTestsFromTestCase(TestCountdown))
    suite.addTests(loader.loadTestsFromTestCase(TestCreateCountdown))
    suite.addTests(loader.loadTestsFromTestCase(TestCountdownFromDelta))
    suite.addTests(loader.loadTestsFromTestCase(TestMultiCountdown))
    suite.addTests(loader.loadTestsFromTestCase(TestFormatDuration))
    suite.addTests(loader.loadTestsFromTestCase(TestTimeUntil))
    suite.addTests(loader.loadTestsFromTestCase(TestNextOccurrence))
    suite.addTests(loader.loadTestsFromTestCase(TestCountdownToNext))
    suite.addTests(loader.loadTestsFromTestCase(TestCountdownTimer))
    suite.addTests(loader.loadTestsFromTestCase(TestConvenienceFunctions))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)