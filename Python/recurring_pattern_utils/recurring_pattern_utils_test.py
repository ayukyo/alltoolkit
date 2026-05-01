"""
周期性模式工具测试模块

测试 parse_natural_language, parse_cron, get_next_occurrence 等功能
"""

import unittest
from datetime import datetime, date, timedelta
import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from recurring_pattern_utils.mod import (
    RecurringPattern, PatternType, Weekday,
    parse_natural_language, parse_cron,
    get_next_occurrence, get_previous_occurrence,
    get_occurrences_in_range, validate_pattern,
    pattern_to_description, get_nth_weekday_of_month,
    calculate_next_n_occurrences, humanize_timedelta,
    parse, next_occurrence, is_match
)


class TestParseNaturalLanguage(unittest.TestCase):
    """测试自然语言解析"""
    
    def test_daily_patterns(self):
        """测试每日模式"""
        # 每天
        pattern = parse_natural_language("每天")
        self.assertEqual(pattern.pattern_type, PatternType.DAILY)
        self.assertEqual(pattern.hour, 0)
        self.assertEqual(pattern.minute, 0)
        
        # daily
        pattern = parse_natural_language("daily")
        self.assertEqual(pattern.pattern_type, PatternType.DAILY)
        
        # 每天上午9点
        pattern = parse_natural_language("每天上午9点")
        self.assertEqual(pattern.pattern_type, PatternType.DAILY)
        self.assertEqual(pattern.hour, 9)
        self.assertEqual(pattern.minute, 0)
        
        # 每天下午3点30分
        pattern = parse_natural_language("每天下午3点30分")
        self.assertEqual(pattern.hour, 15)
        self.assertEqual(pattern.minute, 30)
        
        # 每3天
        pattern = parse_natural_language("每3天")
        self.assertEqual(pattern.pattern_type, PatternType.DAILY)
        self.assertEqual(pattern.interval, 3)
    
    def test_weekly_patterns(self):
        """测试每周模式"""
        # 每周一
        pattern = parse_natural_language("每周一")
        self.assertEqual(pattern.pattern_type, PatternType.WEEKLY)
        self.assertIn(Weekday.MONDAY, pattern.weekdays)
        
        # 每周一三五
        pattern = parse_natural_language("每周一三五")
        self.assertEqual(pattern.pattern_type, PatternType.WEEKLY)
        self.assertIn(Weekday.MONDAY, pattern.weekdays)
        self.assertIn(Weekday.WEDNESDAY, pattern.weekdays)
        self.assertIn(Weekday.FRIDAY, pattern.weekdays)
        
        # weekly on monday
        pattern = parse_natural_language("weekly on monday")
        self.assertEqual(pattern.pattern_type, PatternType.WEEKLY)
        self.assertIn(Weekday.MONDAY, pattern.weekdays)
    
    def test_workday_weekend_patterns(self):
        """测试工作日和周末模式"""
        # 工作日
        pattern = parse_natural_language("工作日")
        self.assertEqual(pattern.pattern_type, PatternType.WEEKLY)
        self.assertEqual(len(pattern.weekdays), 5)
        self.assertIn(Weekday.MONDAY, pattern.weekdays)
        self.assertIn(Weekday.FRIDAY, pattern.weekdays)
        self.assertNotIn(Weekday.SATURDAY, pattern.weekdays)
        
        # 周末
        pattern = parse_natural_language("周末")
        self.assertEqual(pattern.pattern_type, PatternType.WEEKLY)
        self.assertEqual(len(pattern.weekdays), 2)
        self.assertIn(Weekday.SATURDAY, pattern.weekdays)
        self.assertIn(Weekday.SUNDAY, pattern.weekdays)
    
    def test_monthly_patterns(self):
        """测试每月模式"""
        # 每月1号
        pattern = parse_natural_language("每月1号")
        self.assertEqual(pattern.pattern_type, PatternType.MONTHLY)
        self.assertIn(1, pattern.days_of_month)
        
        # 每月15号
        pattern = parse_natural_language("每月15号")
        self.assertIn(15, pattern.days_of_month)
        
        # monthly on 15
        pattern = parse_natural_language("monthly on 15")
        self.assertEqual(pattern.pattern_type, PatternType.MONTHLY)
        self.assertIn(15, pattern.days_of_month)
    
    def test_nth_weekday_of_month(self):
        """测试每月第 n 个周几模式"""
        # 每月第二个周二
        pattern = parse_natural_language("每月第二个周二")
        self.assertEqual(pattern.pattern_type, PatternType.MONTHLY)
        self.assertIsNotNone(pattern.nth_weekday)
        nth, wd = pattern.nth_weekday
        self.assertEqual(nth, 2)
        self.assertEqual(wd, Weekday.TUESDAY)
        
        # 每月最后一个周五
        pattern = parse_natural_language("每月最后一个周五")
        nth, wd = pattern.nth_weekday
        self.assertEqual(nth, -1)
        self.assertEqual(wd, Weekday.FRIDAY)
    
    def test_interval_patterns(self):
        """测试间隔模式"""
        # every 3 days
        pattern = parse_natural_language("every 3 days")
        self.assertEqual(pattern.pattern_type, PatternType.DAILY)
        self.assertEqual(pattern.interval, 3)
        
        # every 2 weeks
        pattern = parse_natural_language("every 2 weeks")
        self.assertEqual(pattern.pattern_type, PatternType.WEEKLY)
        self.assertEqual(pattern.interval, 2)
    
    def test_time_parsing(self):
        """测试时间解析"""
        # 9:30 格式
        pattern = parse_natural_language("每天9:30")
        self.assertEqual(pattern.hour, 9)
        self.assertEqual(pattern.minute, 30)
        
        # 14:00:00 格式
        pattern = parse_natural_language("每天14:00:00")
        self.assertEqual(pattern.hour, 14)
        self.assertEqual(pattern.minute, 0)
        self.assertEqual(pattern.second, 0)
    
    def test_yearly_patterns(self):
        """测试每年模式"""
        pattern = parse_natural_language("每年")
        self.assertEqual(pattern.pattern_type, PatternType.YEARLY)
        
        pattern = parse_natural_language("yearly")
        self.assertEqual(pattern.pattern_type, PatternType.YEARLY)


class TestParseCron(unittest.TestCase):
    """测试 cron 表达式解析"""
    
    def test_daily_cron(self):
        """测试每日 cron"""
        pattern = parse_cron("0 9 * * *")
        self.assertEqual(pattern.hour, 9)
        self.assertEqual(pattern.minute, 0)
    
    def test_weekly_cron(self):
        """测试每周 cron"""
        # 周一到周五 14:30
        pattern = parse_cron("30 14 * * 1-5")
        self.assertEqual(pattern.hour, 14)
        self.assertEqual(pattern.minute, 30)
        # cron 1-5 表示周一到周五
        self.assertIn(Weekday.MONDAY, pattern.weekdays)
        self.assertIn(Weekday.FRIDAY, pattern.weekdays)
    
    def test_monthly_cron(self):
        """测试每月 cron"""
        pattern = parse_cron("0 0 1 * *")
        self.assertEqual(pattern.pattern_type, PatternType.MONTHLY)
        self.assertIn(1, pattern.days_of_month)
    
    def test_specific_weekdays_cron(self):
        """测试特定周几 cron"""
        # 每周一三五 12:00
        pattern = parse_cron("0 12 * * 1,3,5")
        self.assertIn(Weekday.MONDAY, pattern.weekdays)
        self.assertIn(Weekday.WEDNESDAY, pattern.weekdays)
        self.assertIn(Weekday.FRIDAY, pattern.weekdays)
    
    def test_cron_with_step(self):
        """测试步进 cron"""
        # 每 15 分钟
        pattern = parse_cron("*/15 * * * *")
        self.assertEqual(pattern.minute, 0)  # 取最小值
    
    def test_invalid_cron(self):
        """测试无效 cron"""
        with self.assertRaises(ValueError):
            parse_cron("0 9 * *")  # 字段不够
        
        with self.assertRaises(ValueError):
            parse_cron("60 9 * * *")  # 分钟超出范围


class TestNextOccurrence(unittest.TestCase):
    """测试下一个触发时间计算"""
    
    def test_daily_next(self):
        """测试每日下一个触发"""
        pattern = parse_natural_language("每天9:00")
        from_time = datetime(2024, 1, 15, 8, 30)
        next_time = get_next_occurrence(pattern, from_time)
        
        self.assertIsNotNone(next_time)
        self.assertEqual(next_time.hour, 9)
        self.assertEqual(next_time.minute, 0)
        # 同一天 9:00 还没到，应该返回当天 9:00
        self.assertEqual(next_time.day, 15)
    
    def test_daily_next_tomorrow(self):
        """测试每日下一个触发 (第二天)"""
        pattern = parse_natural_language("每天9:00")
        from_time = datetime(2024, 1, 15, 10, 0)
        next_time = get_next_occurrence(pattern, from_time)
        
        self.assertIsNotNone(next_time)
        self.assertEqual(next_time.day, 16)
        self.assertEqual(next_time.hour, 9)
    
    def test_weekly_next(self):
        """测试每周下一个触发"""
        # 假设今天是周六，找下周一
        pattern = parse_natural_language("每周一")
        from_time = datetime(2024, 1, 13, 10, 0)  # 2024-01-13 是周六
        next_time = get_next_occurrence(pattern, from_time)
        
        self.assertIsNotNone(next_time)
        self.assertEqual(next_time.weekday(), 0)  # 周一
        self.assertTrue(next_time > from_time)
    
    def test_monthly_next(self):
        """测试每月下一个触发"""
        pattern = parse_natural_language("每月15号")
        from_time = datetime(2024, 1, 10, 0, 0)
        next_time = get_next_occurrence(pattern, from_time)
        
        self.assertIsNotNone(next_time)
        # 下一个 15 号是 1月15日
        self.assertEqual(next_time.month, 1)
        self.assertEqual(next_time.day, 15)
    
    def test_with_end_date(self):
        """测试有结束日期的情况"""
        pattern = parse_natural_language("每天")
        pattern.end_date = date(2024, 1, 20)
        
        from_time = datetime(2024, 1, 20, 1, 0)
        next_time = get_next_occurrence(pattern, from_time)
        
        self.assertIsNone(next_time)  # 已超过结束日期


class TestPreviousOccurrence(unittest.TestCase):
    """测试上一个触发时间计算"""
    
    def test_daily_previous(self):
        """测试每日上一个触发"""
        pattern = parse_natural_language("每天9:00")
        # 当时间是 10:30 时，上一个 9:00 是当天 9:00（因为已经过了）
        from_time = datetime(2024, 1, 15, 10, 30)
        prev_time = get_previous_occurrence(pattern, from_time)
        
        self.assertIsNotNone(prev_time)
        # 当天的 9:00 已经过了，应该返回当天的 9:00
        self.assertEqual(prev_time.day, 15)
        self.assertEqual(prev_time.hour, 9)
    
    def test_weekly_previous(self):
        """测试每周上一个触发"""
        pattern = parse_natural_language("每周一")
        from_time = datetime(2024, 1, 15, 10, 0)  # 2024-01-15 是周一
        prev_time = get_previous_occurrence(pattern, from_time)
        
        self.assertIsNotNone(prev_time)
        self.assertEqual(prev_time.weekday(), 0)  # 周一
        self.assertTrue(prev_time < from_time)


class TestOccurrencesInRange(unittest.TestCase):
    """测试时间范围内的触发时间"""
    
    def test_daily_in_range(self):
        """测试每日在范围内"""
        pattern = parse_natural_language("每天9:00")
        start = datetime(2024, 1, 10, 0, 0)
        end = datetime(2024, 1, 15, 23, 59)  # 包含15日
        
        occurrences = get_occurrences_in_range(pattern, start, end)
        
        self.assertEqual(len(occurrences), 6)  # 10, 11, 12, 13, 14, 15日
        for occ in occurrences:
            self.assertEqual(occ.hour, 9)
            self.assertEqual(occ.minute, 0)
    
    def test_weekly_in_range(self):
        """测试每周在范围内"""
        pattern = parse_natural_language("每周一")
        start = datetime(2024, 1, 1, 0, 0)
        end = datetime(2024, 1, 31, 23, 59)
        
        occurrences = get_occurrences_in_range(pattern, start, end)
        
        for occ in occurrences:
            self.assertEqual(occ.weekday(), 0)


class TestValidatePattern(unittest.TestCase):
    """测试模式验证"""
    
    def test_valid_patterns(self):
        """测试有效模式"""
        valid, _ = validate_pattern("每天")
        self.assertTrue(valid)
        
        valid, _ = validate_pattern("每周一三五")
        self.assertTrue(valid)
        
        valid, _ = validate_pattern("0 9 * * *")
        self.assertTrue(valid)
    
    def test_invalid_patterns(self):
        """测试无效模式"""
        valid, _ = validate_pattern("无效模式")
        self.assertFalse(valid)


class TestPatternToDescription(unittest.TestCase):
    """测试模式描述转换"""
    
    def test_daily_description(self):
        """测试每日描述"""
        pattern = parse_natural_language("每天9:30")
        desc = pattern_to_description(pattern)
        self.assertIn("每天", desc)
        self.assertIn("09:30", desc)
    
    def test_weekly_description(self):
        """测试每周描述"""
        pattern = parse_natural_language("每周一三五")
        desc = pattern_to_description(pattern)
        self.assertIn("每周", desc)
    
    def test_monthly_description(self):
        """测试每月描述"""
        pattern = parse_natural_language("每月15号")
        desc = pattern_to_description(pattern)
        self.assertIn("每月", desc)
        self.assertIn("15", desc)


class TestGetNthWeekdayOfMonth(unittest.TestCase):
    """测试获取每月第 n 个周几"""
    
    def test_first_monday(self):
        """测试第一个周一"""
        # 2024年1月第一个周一是1月1日
        result = get_nth_weekday_of_month(2024, 1, 1, Weekday.MONDAY)
        self.assertEqual(result, date(2024, 1, 1))
    
    def test_second_tuesday(self):
        """测试第二个周二"""
        # 2024年1月第二个周二是1月9日
        result = get_nth_weekday_of_month(2024, 1, 2, Weekday.TUESDAY)
        self.assertEqual(result, date(2024, 1, 9))
    
    def test_last_friday(self):
        """测试最后一个周五"""
        # 2024年1月最后一个周五是1月26日
        result = get_nth_weekday_of_month(2024, 1, -1, Weekday.FRIDAY)
        self.assertEqual(result, date(2024, 1, 26))
    
    def test_nonexistent_nth(self):
        """测试不存在的第 n 个"""
        # 2024年2月没有第5个周一
        result = get_nth_weekday_of_month(2024, 2, 5, Weekday.MONDAY)
        self.assertIsNone(result)


class TestCalculateNextNOccurrences(unittest.TestCase):
    """测试计算接下来 n 个触发时间"""
    
    def test_next_n_daily(self):
        """测试每日接下来 n 个"""
        pattern = parse_natural_language("每天9:00")
        from_time = datetime(2024, 1, 15, 10, 0)
        
        occurrences = calculate_next_n_occurrences(pattern, from_time, 5)
        
        self.assertEqual(len(occurrences), 5)
        for i, occ in enumerate(occurrences):
            self.assertEqual(occ.day, 16 + i)
            self.assertEqual(occ.hour, 9)


class TestHumanizeTimedelta(unittest.TestCase):
    """测试时间差人性化"""
    
    def test_seconds(self):
        """测试秒"""
        dt = datetime(2024, 1, 15, 10, 0, 30)
        from_time = datetime(2024, 1, 15, 10, 0, 0)
        result = humanize_timedelta(dt, from_time)
        self.assertEqual(result, "30 秒后")
    
    def test_minutes(self):
        """测试分钟"""
        dt = datetime(2024, 1, 15, 10, 15, 0)
        from_time = datetime(2024, 1, 15, 10, 0, 0)
        result = humanize_timedelta(dt, from_time)
        self.assertEqual(result, "15 分钟后")
    
    def test_hours(self):
        """测试小时"""
        dt = datetime(2024, 1, 15, 12, 0, 0)
        from_time = datetime(2024, 1, 15, 10, 0, 0)
        result = humanize_timedelta(dt, from_time)
        self.assertEqual(result, "2 小时后")
    
    def test_days(self):
        """测试天"""
        dt = datetime(2024, 1, 17, 10, 0, 0)
        from_time = datetime(2024, 1, 15, 10, 0, 0)
        result = humanize_timedelta(dt, from_time)
        self.assertEqual(result, "2 天后")


class TestConvenienceFunctions(unittest.TestCase):
    """测试便捷函数"""
    
    def test_parse_auto_detect(self):
        """测试自动检测模式类型"""
        # 自然语言
        pattern = parse("每天")
        self.assertEqual(pattern.pattern_type, PatternType.DAILY)
        
        # cron
        pattern = parse("0 9 * * *")
        self.assertEqual(pattern.hour, 9)
    
    def test_next_occurrence_convenience(self):
        """测试便捷函数获取下一个触发时间"""
        result = next_occurrence("每天9:00", datetime(2024, 1, 15, 8, 0))
        self.assertIsNotNone(result)
        self.assertEqual(result.hour, 9)
    
    def test_is_match(self):
        """测试匹配检查"""
        dt = datetime(2024, 1, 15, 9, 0)  # 周一 9:00
        
        self.assertTrue(is_match("每天9:00", dt))
        # "每周一" 默认时间是 0:00，所以 9:00 不匹配时间部分
        # 改为检查 0:00 的时间
        dt_midnight = datetime(2024, 1, 15, 0, 0)  # 周一 0:00
        self.assertTrue(is_match("每周一", dt_midnight))
        self.assertFalse(is_match("每周二", dt_midnight))


class TestRecurringPatternMatch(unittest.TestCase):
    """测试 RecurringPattern.matches 方法"""
    
    def test_daily_match(self):
        """测试每日匹配"""
        pattern = RecurringPattern(
            pattern_type=PatternType.DAILY,
            hour=9, minute=0
        )
        
        self.assertTrue(pattern.matches(datetime(2024, 1, 15, 9, 0)))
        self.assertFalse(pattern.matches(datetime(2024, 1, 15, 10, 0)))
    
    def test_weekly_match(self):
        """测试每周匹配"""
        pattern = RecurringPattern(
            pattern_type=PatternType.WEEKLY,
            weekdays={Weekday.MONDAY, Weekday.WEDNESDAY},
            hour=9, minute=0
        )
        
        self.assertTrue(pattern.matches(datetime(2024, 1, 15, 9, 0)))  # 周一
        self.assertTrue(pattern.matches(datetime(2024, 1, 17, 9, 0)))  # 周三
        self.assertFalse(pattern.matches(datetime(2024, 1, 16, 9, 0)))  # 周二
    
    def test_date_range(self):
        """测试日期范围限制"""
        pattern = RecurringPattern(
            pattern_type=PatternType.DAILY,
            hour=9, minute=0,
            start_date=date(2024, 1, 10),
            end_date=date(2024, 1, 20)
        )
        
        self.assertFalse(pattern.matches(datetime(2024, 1, 5, 9, 0)))
        self.assertTrue(pattern.matches(datetime(2024, 1, 15, 9, 0)))
        self.assertFalse(pattern.matches(datetime(2024, 1, 25, 9, 0)))


if __name__ == '__main__':
    unittest.main(verbosity=2)