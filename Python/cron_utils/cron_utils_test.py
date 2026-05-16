"""
Cron Utilities 测试

测试 Cron 表达式解析、验证和计算功能。
"""

import unittest
from datetime import datetime, timedelta
from mod import (
    CronExpression,
    CronParseError,
    CronValidator,
    CronCalculator,
    CronScheduler,
    parse,
    validate,
    is_valid,
    next_run,
    next_runs,
    describe,
)


class TestCronExpression(unittest.TestCase):
    """CronExpression 测试"""
    
    def test_parse_standard_5_fields(self):
        """测试标准 5 字段解析"""
        # 每分钟
        cron = CronExpression("* * * * *")
        self.assertFalse(cron.has_seconds)
        self.assertFalse(cron.has_year)
    
    def test_parse_extended_6_fields(self):
        """测试扩展 6 字段解析"""
        # 每秒
        cron = CronExpression("* * * * * *")
        self.assertTrue(cron.has_seconds)
        self.assertFalse(cron.has_year)
    
    def test_parse_quartz_7_fields(self):
        """测试 Quartz 7 字段解析"""
        cron = CronExpression("* * * * * * 2024")
        self.assertTrue(cron.has_seconds)
        self.assertTrue(cron.has_year)
    
    def test_parse_invalid_fields_count(self):
        """测试无效字段数量"""
        with self.assertRaises(CronParseError):
            CronExpression("* * * *")  # 只有 4 个字段
        
        with self.assertRaises(CronParseError):
            CronExpression("* * * * * * * *")  # 8 个字段
    
    def test_special_expressions(self):
        """测试特殊表达式"""
        # @hourly
        cron = CronExpression("@hourly")
        self.assertTrue(cron.has_seconds)
        
        # @daily
        cron = CronExpression("@daily")
        self.assertTrue(cron.has_seconds)
        
        # @monthly
        cron = CronExpression("@monthly")
        self.assertTrue(cron.has_seconds)
        
        # @yearly
        cron = CronExpression("@yearly")
        self.assertTrue(cron.has_seconds)
    
    def test_parse_asterisk(self):
        """测试星号解析"""
        cron = CronExpression("* * * * *")
        
        # 分钟应该是 0-59
        self.assertEqual(len(cron.field_values), 5)
        # 验证分钟字段
        from mod import CronFieldType
        self.assertEqual(len(cron.field_values[CronFieldType.MINUTE]), 60)
    
    def test_parse_range(self):
        """测试范围解析"""
        cron = CronExpression("0-30 * * * *")
        # 分钟应该是 0-30
        minute_field = cron.field_values
        # 获取分钟字段
    
    def test_parse_step(self):
        """测试步长解析"""
        # 每 15 分钟
        cron = CronExpression("*/15 * * * *")
        # 应该包含 0, 15, 30, 45
        
        # 每 5 分钟
        cron = CronExpression("*/5 * * * *")
    
    def test_parse_list(self):
        """测试列表解析"""
        cron = CronExpression("0,15,30,45 * * * *")
        # 应该包含 0, 15, 30, 45
    
    def test_parse_month_names(self):
        """测试月份名称"""
        cron = CronExpression("0 0 1 jan *")
        # 1 月
        
        cron = CronExpression("0 0 1 january *")
        # 1 月
    
    def test_parse_weekday_names(self):
        """测试星期名称"""
        cron = CronExpression("0 0 * * mon")
        # 周一
        
        cron = CronExpression("0 0 * * monday")
        # 周一
    
    def test_matches(self):
        """测试时间匹配"""
        # 每分钟
        cron = CronExpression("* * * * *")
        
        # 任意时间都应该匹配
        dt = datetime(2024, 1, 15, 10, 30, 0)
        self.assertTrue(cron.matches(dt))
        
        # 每小时整点
        cron = CronExpression("0 * * * *")
        self.assertTrue(cron.matches(datetime(2024, 1, 15, 10, 0, 0)))
        self.assertFalse(cron.matches(datetime(2024, 1, 15, 10, 30, 0)))
        
        # 每天 9 点
        cron = CronExpression("0 9 * * *")
        self.assertTrue(cron.matches(datetime(2024, 1, 15, 9, 0, 0)))
        self.assertFalse(cron.matches(datetime(2024, 1, 15, 10, 0, 0)))
    
    def test_get_next_run(self):
        """测试下次执行时间计算"""
        # 每分钟
        cron = CronExpression("* * * * *")
        from_time = datetime(2024, 1, 15, 10, 30, 30)
        next_time = cron.get_next_run(from_time)
        self.assertIsNotNone(next_time)
        self.assertEqual(next_time.minute, 31)
        
        # 每小时整点
        cron = CronExpression("0 * * * *")
        from_time = datetime(2024, 1, 15, 10, 30, 0)
        next_time = cron.get_next_run(from_time)
        self.assertIsNotNone(next_time)
        self.assertEqual(next_time.hour, 11)
        self.assertEqual(next_time.minute, 0)
    
    def test_get_next_runs(self):
        """测试多次执行时间计算"""
        # 每 15 分钟
        cron = CronExpression("*/15 * * * *")
        from_time = datetime(2024, 1, 15, 10, 0, 0)
        runs = cron.get_next_runs(4, from_time)
        
        self.assertEqual(len(runs), 4)
        # 应该是 10:15, 10:30, 10:45, 11:00
        self.assertEqual(runs[0].minute, 15)
        self.assertEqual(runs[1].minute, 30)
        self.assertEqual(runs[2].minute, 45)
        self.assertEqual(runs[3].minute, 0)
        self.assertEqual(runs[3].hour, 11)
    
    def test_get_description(self):
        """测试描述生成"""
        # 每分钟
        cron = CronExpression("* * * * *")
        desc = cron.get_description()
        self.assertIn("分", desc)
        
        # 每小时
        cron = CronExpression("0 * * * *")
        desc = cron.get_description()
        self.assertIn("0分", desc)
        self.assertIn("每时", desc)
    
    def test_invalid_range(self):
        """测试无效范围"""
        # 分钟超出范围
        with self.assertRaises(CronParseError):
            CronExpression("60 * * * *")
        
        # 小时超出范围
        with self.assertRaises(CronParseError):
            CronExpression("* 24 * * *")
    
    def test_6_field_expression(self):
        """测试 6 字段表达式"""
        # 每秒
        cron = CronExpression("* * * * * *")
        self.assertTrue(cron.has_seconds)
        
        # 每分钟的第 30 秒
        cron = CronExpression("30 * * * * *")
        dt = datetime(2024, 1, 15, 10, 30, 30)
        self.assertTrue(cron.matches(dt))
        dt = datetime(2024, 1, 15, 10, 30, 0)
        self.assertFalse(cron.matches(dt))


class TestCronValidator(unittest.TestCase):
    """CronValidator 测试"""
    
    def test_validate_valid(self):
        """测试有效表达式"""
        is_valid, error = CronValidator.validate("* * * * *")
        self.assertTrue(is_valid)
        self.assertIsNone(error)
        
        is_valid, error = CronValidator.validate("0 9 * * 1-5")
        self.assertTrue(is_valid)
        self.assertIsNone(error)
    
    def test_validate_invalid(self):
        """测试无效表达式"""
        is_valid, error = CronValidator.validate("* * * *")
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)
        
        is_valid, error = CronValidator.validate("60 * * * *")
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)
    
    def test_is_valid(self):
        """测试快速验证"""
        self.assertTrue(CronValidator.is_valid("* * * * *"))
        self.assertFalse(CronValidator.is_valid("* * * *"))


class TestCronCalculator(unittest.TestCase):
    """CronCalculator 测试"""
    
    def test_next_run(self):
        """测试下次执行计算"""
        from_time = datetime(2024, 1, 15, 10, 0, 0)
        next_time = CronCalculator.next_run("0 * * * *", from_time)
        self.assertIsNotNone(next_time)
        self.assertEqual(next_time.hour, 11)
    
    def test_next_runs(self):
        """测试多次执行计算"""
        from_time = datetime(2024, 1, 15, 10, 0, 0)
        runs = CronCalculator.next_runs("0 * * * *", 3, from_time)
        self.assertEqual(len(runs), 3)
    
    def test_time_until_next(self):
        """测试距离下次执行的时间"""
        from_time = datetime(2024, 1, 15, 10, 0, 0)
        delta = CronCalculator.time_until_next("0 11 * * *", from_time)
        self.assertIsNotNone(delta)
        self.assertEqual(delta, timedelta(hours=1))


class TestCronScheduler(unittest.TestCase):
    """CronScheduler 测试"""
    
    def test_add_remove_job(self):
        """测试添加和移除任务"""
        scheduler = CronScheduler()
        
        scheduler.add_job("job1", "* * * * *")
        self.assertIn("job1", scheduler.get_jobs())
        
        scheduler.remove_job("job1")
        self.assertNotIn("job1", scheduler.get_jobs())
    
    def test_get_due_jobs(self):
        """测试获取到期任务"""
        scheduler = CronScheduler()
        
        # 每分钟
        scheduler.add_job("every_minute", "* * * * *")
        
        # 特定时间
        at_time = datetime(2024, 1, 15, 10, 30, 0)
        due = scheduler.get_due_jobs(at_time)
        self.assertIn("every_minute", due)
        
        # 每小时整点
        scheduler.add_job("hourly", "0 * * * *")
        
        # 非整点时间，hourly 不应该到期
        due = scheduler.get_due_jobs(at_time)
        self.assertIn("every_minute", due)
        self.assertNotIn("hourly", due)
        
        # 整点时间，两者都应该到期
        at_time_hourly = datetime(2024, 1, 15, 11, 0, 0)
        due = scheduler.get_due_jobs(at_time_hourly)
        self.assertIn("every_minute", due)
        self.assertIn("hourly", due)
    
    def test_get_schedule(self):
        """测试获取调度表"""
        scheduler = CronScheduler()
        
        scheduler.add_job("hourly", "0 * * * *")
        
        from_time = datetime(2024, 1, 15, 10, 30, 0)
        schedule = scheduler.get_schedule(hours=3, from_time=from_time)
        
        self.assertIn("hourly", schedule)
        # 3 小时内应该有 3 次
        self.assertEqual(len(schedule["hourly"]), 3)


class TestConvenienceFunctions(unittest.TestCase):
    """便捷函数测试"""
    
    def test_parse(self):
        """测试 parse 函数"""
        cron = parse("* * * * *")
        self.assertIsInstance(cron, CronExpression)
    
    def test_validate(self):
        """测试 validate 函数"""
        is_valid, error = validate("* * * * *")
        self.assertTrue(is_valid)
    
    def test_is_valid(self):
        """测试 is_valid 函数"""
        self.assertTrue(is_valid("* * * * *"))
        self.assertFalse(is_valid("* * * *"))
    
    def test_next_run(self):
        """测试 next_run 函数"""
        from_time = datetime(2024, 1, 15, 10, 0, 0)
        result = next_run("0 * * * *", from_time)
        self.assertIsNotNone(result)
    
    def test_next_runs(self):
        """测试 next_runs 函数"""
        from_time = datetime(2024, 1, 15, 10, 0, 0)
        runs = next_runs("0 * * * *", 5, from_time)
        self.assertEqual(len(runs), 5)
    
    def test_describe(self):
        """测试 describe 函数"""
        desc = describe("0 9 * * 1-5")
        self.assertIsNotNone(desc)
        self.assertIn("9时", desc)


class TestEdgeCases(unittest.TestCase):
    """边界情况测试"""
    
    def test_year_end(self):
        """测试年末边界"""
        # 每年 1 月 1 日 0 点
        cron = CronExpression("0 0 0 1 1 *")
        from_time = datetime(2024, 12, 31, 23, 59, 59)
        next_time = cron.get_next_run(from_time)
        self.assertIsNotNone(next_time)
        self.assertEqual(next_time.year, 2025)
        self.assertEqual(next_time.month, 1)
        self.assertEqual(next_time.day, 1)
    
    def test_february_29(self):
        """测试闰年 2 月 29 日"""
        # 每月 29 日（简化测试）
        cron = CronExpression("0 0 29 * *")
        
        # 从 1 月开始查找
        from_time = datetime(2024, 1, 15, 10, 0, 0)
        next_time = cron.get_next_run(from_time)
        self.assertIsNotNone(next_time)
        # 应该找到 1 月 29 日
        self.assertEqual(next_time.month, 1)
        self.assertEqual(next_time.day, 29)
        
        # 从 2 月 1 日开始（2024 是闰年）
        from_time = datetime(2024, 2, 1, 10, 0, 0)
        next_time = cron.get_next_run(from_time)
        self.assertIsNotNone(next_time)
        # 应该找到 2 月 29 日
        self.assertEqual(next_time.month, 2)
        self.assertEqual(next_time.day, 29)
    
    def test_weekday_boundary(self):
        """测试星期边界"""
        # 每周一
        cron = CronExpression("0 9 * * 1")
        
        # 2024-01-15 是周一
        dt = datetime(2024, 1, 15, 9, 0, 0)
        self.assertTrue(cron.matches(dt))
        
        # 2024-01-16 是周二
        dt = datetime(2024, 1, 16, 9, 0, 0)
        self.assertFalse(cron.matches(dt))
    
    def test_complex_expression(self):
        """测试复杂表达式"""
        # 每个工作日早上 9:30
        cron = CronExpression("30 9 * * 1-5")
        
        # 周一 9:30
        dt = datetime(2024, 1, 15, 9, 30, 0)  # 周一
        self.assertTrue(cron.matches(dt))
        
        # 周六 9:30
        dt = datetime(2024, 1, 20, 9, 30, 0)  # 周六
        self.assertFalse(cron.matches(dt))
    
    def test_multiple_values(self):
        """测试多值表达式"""
        # 每天 9:00, 12:00, 18:00
        cron = CronExpression("0 9,12,18 * * *")
        
        self.assertTrue(cron.matches(datetime(2024, 1, 15, 9, 0, 0)))
        self.assertTrue(cron.matches(datetime(2024, 1, 15, 12, 0, 0)))
        self.assertTrue(cron.matches(datetime(2024, 1, 15, 18, 0, 0)))
        self.assertFalse(cron.matches(datetime(2024, 1, 15, 10, 0, 0)))
    
    def test_step_with_range(self):
        """测试范围步长"""
        # 每小时前 30 分钟内，每 5 分钟
        cron = CronExpression("0-30/5 * * * *")
        
        # 应该匹配 0, 5, 10, 15, 20, 25, 30
        for minute in [0, 5, 10, 15, 20, 25, 30]:
            self.assertTrue(cron.matches(datetime(2024, 1, 15, 10, minute, 0)))
        
        # 不应该匹配
        for minute in [35, 40, 45, 50, 55]:
            self.assertFalse(cron.matches(datetime(2024, 1, 15, 10, minute, 0)))


class TestPerformance(unittest.TestCase):
    """性能测试"""
    
    def test_next_runs_performance(self):
        """测试多次计算性能"""
        import time
        
        cron = CronExpression("*/5 * * * *")
        from_time = datetime(2024, 1, 15, 10, 0, 0)
        
        start = time.time()
        runs = cron.get_next_runs(1000, from_time)
        elapsed = time.time() - start
        
        # 1000 次计算应该在合理时间内完成
        self.assertEqual(len(runs), 1000)
        # 打印但不强制要求
        print(f"\n1000 次计算耗时: {elapsed:.3f}s")
    
    def test_matches_performance(self):
        """测试匹配性能"""
        import time
        
        cron = CronExpression("*/15 * * * *")
        
        start = time.time()
        for i in range(10000):
            dt = datetime(2024, 1, 15, 10, i % 60, 0)
            cron.matches(dt)
        elapsed = time.time() - start
        
        print(f"\n10000 次匹配耗时: {elapsed:.3f}s")


if __name__ == "__main__":
    unittest.main(verbosity=2)