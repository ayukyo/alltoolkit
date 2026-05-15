"""
Cron Utils 测试套件

测试所有核心功能：
- 表达式解析
- 下次运行时间计算
- 验证功能
- 描述生成
- 特殊表达式
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import unittest
from datetime import datetime, timedelta
from mod import (
    CronExpression,
    CronParseError,
    parse,
    get_next_run,
    get_next_runs,
    validate,
    to_description,
    EVERY_MINUTE,
    EVERY_HOUR,
    EVERY_DAY,
    EVERY_5_MINUTES,
    WEEKDAYS_9AM,
)


class TestCronParsing(unittest.TestCase):
    """测试 Cron 表达式解析"""
    
    def test_parse_standard_5_fields(self):
        """测试标准5字段格式"""
        cron = parse("0 9 * * 1-5")
        self.assertEqual(cron.fields['minute'], {0})
        self.assertEqual(cron.fields['hour'], {9})
        self.assertEqual(cron.fields['day'], set(range(1, 32)))
        self.assertEqual(cron.fields['month'], set(range(1, 13)))
        self.assertEqual(cron.fields['weekday'], {1, 2, 3, 4, 5})
    
    def test_parse_extended_6_fields(self):
        """测试扩展6字段格式"""
        cron = parse("30 0 9 * * *")
        self.assertTrue(cron.has_seconds)
        self.assertEqual(cron.fields['second'], {30})
        self.assertEqual(cron.fields['minute'], {0})
        self.assertEqual(cron.fields['hour'], {9})
    
    def test_parse_asterisk(self):
        """测试通配符"""
        cron = parse("* * * * *")
        self.assertEqual(cron.fields['minute'], set(range(60)))
        self.assertEqual(cron.fields['hour'], set(range(24)))
    
    def test_parse_step(self):
        """测试步长表达式"""
        cron = parse("*/15 * * * *")
        self.assertEqual(cron.fields['minute'], {0, 15, 30, 45})
    
    def test_parse_range(self):
        """测试范围表达式"""
        cron = parse("0 9-17 * * *")
        self.assertEqual(cron.fields['hour'], set(range(9, 18)))
    
    def test_parse_range_with_step(self):
        """测试范围+步长表达式"""
        cron = parse("0-30/10 * * * *")
        self.assertEqual(cron.fields['minute'], {0, 10, 20, 30})
    
    def test_parse_list(self):
        """测试列表表达式"""
        cron = parse("0,30 9,12,18 * * *")
        self.assertEqual(cron.fields['minute'], {0, 30})
        self.assertEqual(cron.fields['hour'], {9, 12, 18})
    
    def test_parse_month_names(self):
        """测试月份名称"""
        cron = parse("0 0 1 jan,feb,mar *")
        self.assertEqual(cron.fields['month'], {1, 2, 3})
    
    def test_parse_weekday_names(self):
        """测试星期名称"""
        cron = parse("0 9 * * mon-fri")
        self.assertEqual(cron.fields['weekday'], {1, 2, 3, 4, 5})
    
    def test_parse_special_yearly(self):
        """测试 @yearly 特殊表达式"""
        cron = parse("@yearly")
        self.assertEqual(cron.fields['minute'], {0})
        self.assertEqual(cron.fields['hour'], {0})
        self.assertEqual(cron.fields['day'], {1})
        self.assertEqual(cron.fields['month'], {1})
    
    def test_parse_special_monthly(self):
        """测试 @monthly 特殊表达式"""
        cron = parse("@monthly")
        self.assertEqual(cron.fields['day'], {1})
        self.assertEqual(cron.fields['hour'], {0})
        self.assertEqual(cron.fields['minute'], {0})
    
    def test_parse_special_hourly(self):
        """测试 @hourly 特殊表达式"""
        cron = parse("@hourly")
        self.assertEqual(cron.fields['minute'], {0})
        self.assertEqual(cron.fields['hour'], set(range(24)))
    
    def test_parse_invalid_fields_count(self):
        """测试无效字段数量"""
        with self.assertRaises(CronParseError):
            parse("* * *")
        with self.assertRaises(CronParseError):
            parse("* * * * * * *")
    
    def test_parse_invalid_range(self):
        """测试无效范围"""
        with self.assertRaises(CronParseError):
            parse("60 * * * *")  # 分钟超出范围
        with self.assertRaises(CronParseError):
            parse("0 25 * * *")  # 小时超出范围
    
    def test_parse_invalid_special(self):
        """测试无效特殊表达式"""
        with self.assertRaises(CronParseError):
            parse("@invalid")


class TestNextRunCalculation(unittest.TestCase):
    """测试下次运行时间计算"""
    
    def test_next_run_every_minute(self):
        """测试每分钟的下次运行"""
        cron = parse(EVERY_MINUTE)
        now = datetime(2024, 1, 15, 10, 30, 45)
        next_run = cron.get_next_run(now)
        
        self.assertIsNotNone(next_run)
        # 应该是下一分钟
        self.assertEqual(next_run.minute, 31)
        self.assertEqual(next_run.second, 0)
    
    def test_next_run_every_5_minutes(self):
        """测试每5分钟的下次运行"""
        cron = parse(EVERY_5_MINUTES)
        now = datetime(2024, 1, 15, 10, 32, 0)
        next_run = cron.get_next_run(now)
        
        self.assertIsNotNone(next_run)
        # 应该是35分钟
        self.assertEqual(next_run.minute, 35)
    
    def test_next_run_specific_hour(self):
        """测试特定小时的下次运行"""
        cron = parse("0 9 * * *")  # 每天9点
        now = datetime(2024, 1, 15, 10, 0, 0)  # 上午10点
        next_run = cron.get_next_run(now)
        
        self.assertIsNotNone(next_run)
        # 应该是第二天9点
        self.assertEqual(next_run.day, 16)
        self.assertEqual(next_run.hour, 9)
        self.assertEqual(next_run.minute, 0)
    
    def test_next_run_weekday(self):
        """测试工作日的下次运行"""
        cron = parse(WEEKDAYS_9AM)
        # 周五
        now = datetime(2024, 1, 12, 10, 0, 0)  # 2024-01-12 是周五
        next_run = cron.get_next_run(now)
        
        self.assertIsNotNone(next_run)
        # 应该是下周一
        self.assertEqual(next_run.weekday(), 0)  # Monday
        self.assertEqual(next_run.hour, 9)
    
    def test_next_run_month_specific_day(self):
        """测试每月特定日期"""
        cron = parse("0 0 15 * *")  # 每月15号
        now = datetime(2024, 1, 10, 0, 0, 0)
        next_run = cron.get_next_run(now)
        
        self.assertIsNotNone(next_run)
        self.assertEqual(next_run.day, 15)
    
    def test_next_runs_multiple(self):
        """测试获取多次运行时间"""
        cron = parse("0 * * * *")  # 每小时
        now = datetime(2024, 1, 15, 10, 0, 0)
        runs = cron.get_next_runs(5, now)
        
        self.assertEqual(len(runs), 5)
        # 检查每小时递增
        for i, run in enumerate(runs):
            self.assertEqual(run.hour, (11 + i) % 24)
    
    def test_next_run_with_seconds(self):
        """测试6字段格式的下次运行"""
        cron = parse("*/10 * * * * *")  # 每10秒
        now = datetime(2024, 1, 15, 10, 30, 45)
        next_run = cron.get_next_run(now)
        
        self.assertIsNotNone(next_run)
        # 应该是下一分钟的50秒
        self.assertEqual(next_run.second, 50)


class TestValidation(unittest.TestCase):
    """测试验证功能"""
    
    def test_validate_valid(self):
        """测试有效表达式验证"""
        valid, err = validate("0 9 * * 1-5")
        self.assertTrue(valid)
        self.assertIsNone(err)
    
    def test_validate_invalid(self):
        """测试无效表达式验证"""
        valid, err = validate("invalid")
        self.assertFalse(valid)
        self.assertIsNotNone(err)
    
    def test_validate_empty(self):
        """测试空表达式验证"""
        valid, err = validate("")
        self.assertFalse(valid)
        self.assertIsNotNone(err)


class TestDescription(unittest.TestCase):
    """测试描述生成"""
    
    def test_description_zh(self):
        """测试中文描述"""
        desc = to_description("*/5 * * * *", lang='zh')
        self.assertIn('分钟', desc)
    
    def test_description_en(self):
        """测试英文描述"""
        desc = to_description("*/5 * * * *", lang='en')
        self.assertIn('minute', desc.lower())
    
    def test_description_invalid(self):
        """测试无效表达式描述"""
        desc = to_description("invalid", lang='zh')
        self.assertIn('无效', desc)


class TestEdgeCases(unittest.TestCase):
    """测试边缘情况"""
    
    def test_leap_year(self):
        """测试闰年2月29日"""
        cron = parse("0 0 29 2 *")  # 2月29日
        now = datetime(2023, 1, 1, 0, 0, 0)
        next_run = cron.get_next_run(now, max_iterations=100000)
        
        # 应该能找到下一个闰年的2月29日
        if next_run:
            self.assertEqual(next_run.month, 2)
            self.assertEqual(next_run.day, 29)
    
    def test_midnight(self):
        """测试午夜时间"""
        cron = parse("0 0 * * *")
        now = datetime(2024, 1, 15, 23, 59, 0)
        next_run = cron.get_next_run(now)
        
        self.assertIsNotNone(next_run)
        self.assertEqual(next_run.hour, 0)
        self.assertEqual(next_run.minute, 0)
    
    def test_new_year(self):
        """测试新年"""
        cron = parse("0 0 1 1 *")  # 每年1月1日
        now = datetime(2024, 12, 31, 23, 0, 0)
        next_run = cron.get_next_run(now)
        
        self.assertIsNotNone(next_run)
        self.assertEqual(next_run.year, 2025)
        self.assertEqual(next_run.month, 1)
        self.assertEqual(next_run.day, 1)


class TestConvenienceFunctions(unittest.TestCase):
    """测试便捷函数"""
    
    def test_get_next_run_function(self):
        """测试 get_next_run 便捷函数"""
        next_run = get_next_run("0 9 * * *")
        self.assertIsNotNone(next_run)
        self.assertIsInstance(next_run, datetime)
    
    def test_get_next_runs_function(self):
        """测试 get_next_runs 便捷函数"""
        runs = get_next_runs("0 * * * *", count=3)
        self.assertEqual(len(runs), 3)
        self.assertIsInstance(runs[0], datetime)
    
    def test_parse_function(self):
        """测试 parse 便捷函数"""
        cron = parse("* * * * *")
        self.assertIsInstance(cron, CronExpression)


if __name__ == "__main__":
    unittest.main(verbosity=2)