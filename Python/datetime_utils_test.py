"""
datetime_utils_test.py - 日期时间工具模块测试
"""

import unittest
from datetime import datetime, date, timedelta
import sys
sys.path.insert(0, '.')

from datetime_utils import (
    format_datetime, parse_datetime, parse_natural_time,
    get_timezone, convert_timezone, now_in_timezone,
    add_months, add_years, date_diff, age,
    workdays_between, add_workdays, is_workday,
    date_range, get_month_range, get_week_range,
    timestamp_to_datetime, datetime_to_timestamp,
    is_leap_year, days_in_month, quarter, week_of_year,
    humanize_delta, format_duration,
    now, today, yesterday, tomorrow,
)


class TestFormatParse(unittest.TestCase):
    """测试格式化和解析"""
    
    def test_format_datetime_default(self):
        """测试默认格式化"""
        result = format_datetime(datetime(2026, 4, 27, 12, 30, 45))
        self.assertEqual(result, '2026-04-27 12:30:45')
    
    def test_format_datetime_cn(self):
        """测试中文格式"""
        result = format_datetime(datetime(2026, 4, 27, 12, 30, 45), fmt='cn_datetime')
        self.assertEqual(result, '2026年04月27日 12时30分45秒')
    
    def test_format_datetime_custom(self):
        """测试自定义格式"""
        result = format_datetime(datetime(2026, 4, 27), fmt='%Y/%m/%d')
        self.assertEqual(result, '2026/04/27')
    
    def test_format_date_only(self):
        """测试只有日期"""
        result = format_datetime(date(2026, 4, 27), fmt='iso')
        self.assertEqual(result, '2026-04-27')
    
    def test_parse_datetime_iso(self):
        """测试 ISO 格式解析"""
        result = parse_datetime('2026-04-27')
        self.assertEqual(result, datetime(2026, 4, 27, 0, 0))
    
    def test_parse_datetime_iso_datetime(self):
        """测试 ISO 日期时间解析"""
        result = parse_datetime('2026-04-27 12:30:45')
        self.assertEqual(result, datetime(2026, 4, 27, 12, 30, 45))
    
    def test_parse_datetime_cn(self):
        """测试中文日期解析"""
        result = parse_datetime('2026年04月27日', fmt='cn_date')
        self.assertEqual(result, datetime(2026, 4, 27, 0, 0))
    
    def test_parse_datetime_auto(self):
        """测试自动格式检测"""
        result = parse_datetime('2026/04/27')
        self.assertEqual(result, datetime(2026, 4, 27, 0, 0))
    
    def test_parse_datetime_invalid(self):
        """测试无效日期"""
        with self.assertRaises(ValueError):
            parse_datetime('invalid date')
    
    def test_parse_natural_time_tomorrow(self):
        """测试解析'明天'"""
        base = datetime(2026, 4, 27, 12, 0)
        result = parse_natural_time('明天', base)
        self.assertEqual(result, datetime(2026, 4, 28, 0, 0))
    
    def test_parse_natural_time_yesterday(self):
        """测试解析'昨天'"""
        base = datetime(2026, 4, 27, 12, 0)
        result = parse_natural_time('昨天', base)
        self.assertEqual(result, datetime(2026, 4, 26, 0, 0))
    
    def test_parse_natural_time_days_later(self):
        """测试解析'N天后'"""
        base = datetime(2026, 4, 27, 12, 0)
        result = parse_natural_time('3天后', base)
        self.assertEqual(result, datetime(2026, 4, 30, 12, 0))
    
    def test_parse_natural_time_hours_ago(self):
        """测试解析'N小时前'"""
        base = datetime(2026, 4, 27, 12, 0)
        result = parse_natural_time('2小时前', base)
        self.assertEqual(result, datetime(2026, 4, 27, 10, 0))


class TestTimezone(unittest.TestCase):
    """测试时区功能"""
    
    def test_get_timezone_utc(self):
        """测试获取 UTC 时区"""
        tz = get_timezone('UTC')
        self.assertIsNotNone(tz)
    
    def test_get_timezone_shanghai(self):
        """测试获取上海时区"""
        tz = get_timezone('Asia/Shanghai')
        # 如果 zoneinfo 可用，应该返回时区对象
        if tz:
            self.assertEqual(tz.key, 'Asia/Shanghai')
    
    def test_convert_timezone(self):
        """测试时区转换"""
        try:
            from zoneinfo import ZoneInfo
            dt = datetime(2026, 4, 27, 12, 0, tzinfo=ZoneInfo('UTC'))
            result = convert_timezone(dt, 'Asia/Shanghai')
            # 上海是 UTC+8
            self.assertEqual(result.hour, 20)
        except ImportError:
            # zoneinfo 不可用，跳过此测试
            self.skipTest("zoneinfo not available")
    
    def test_now_in_timezone(self):
        """测试获取指定时区当前时间"""
        result = now_in_timezone('UTC')
        self.assertIsNotNone(result)
        self.assertIsNotNone(result.tzinfo)


class TestDateCalculation(unittest.TestCase):
    """测试日期计算"""
    
    def test_add_months_normal(self):
        """测试正常月份加减"""
        dt = datetime(2026, 3, 15)
        result = add_months(dt, 2)
        self.assertEqual(result, datetime(2026, 5, 15))
    
    def test_add_months_overflow(self):
        """测试月份溢出"""
        dt = datetime(2026, 1, 31)
        result = add_months(dt, 1)
        self.assertEqual(result, datetime(2026, 2, 28))
    
    def test_add_months_negative(self):
        """测试月份减法"""
        dt = datetime(2026, 3, 15)
        result = add_months(dt, -2)
        self.assertEqual(result, datetime(2026, 1, 15))
    
    def test_add_years_normal(self):
        """测试年份加减"""
        dt = datetime(2026, 4, 27)
        result = add_years(dt, 1)
        self.assertEqual(result, datetime(2027, 4, 27))
    
    def test_add_years_leap_year(self):
        """测试闰年处理"""
        dt = datetime(2024, 2, 29)
        result = add_years(dt, 1)
        self.assertEqual(result, datetime(2025, 2, 28))
    
    def test_date_diff_days(self):
        """测试日期差计算"""
        result = date_diff('2026-01-01', '2026-01-11')
        self.assertEqual(result['days'], 10)
    
    def test_date_diff_weeks(self):
        """测试周数差"""
        result = date_diff('2026-01-01', '2026-01-22')
        self.assertEqual(result['weeks'], 3)
    
    def test_age(self):
        """测试年龄计算"""
        result = age('1990-05-15', reference=date(2026, 4, 27))
        self.assertEqual(result['years'], 35)
        self.assertEqual(result['months'], 11)
    
    def test_age_next_birthday(self):
        """测试下次生日"""
        result = age('1990-12-25', reference=date(2026, 4, 27))
        self.assertEqual(result['next_birthday'], '2026-12-25')


class TestWorkdays(unittest.TestCase):
    """测试工作日计算"""
    
    def test_workdays_between_week(self):
        """测试一周内的工作日"""
        result = workdays_between('2026-04-20', '2026-04-26')  # 周一到周日
        self.assertEqual(result, 5)  # 5 个工作日
    
    def test_workdays_with_holidays(self):
        """测试含节假日的工作日"""
        holidays = ['2026-04-20']  # 周一放假
        result = workdays_between('2026-04-20', '2026-04-24', holidays=holidays)
        self.assertEqual(result, 4)  # 周二到周五，共4个工作日
    
    def test_add_workdays(self):
        """测试增加工作日"""
        result = add_workdays('2026-04-24', 3)  # 周五 + 3 工作日
        # 周五 -> 周一(27), 周二(28), 周三(29)
        self.assertEqual(result, date(2026, 4, 29))
    
    def test_add_workdays_negative(self):
        """测试减少工作日"""
        result = add_workdays('2026-04-27', -2)  # 周日 - 2 工作日 = 周三
        self.assertEqual(result, date(2026, 4, 23))
    
    def test_is_workday_weekday(self):
        """测试工作日判断 - 工作日"""
        self.assertTrue(is_workday('2026-04-27'))  # 周一
    
    def test_is_workday_weekend(self):
        """测试工作日判断 - 周末"""
        self.assertFalse(is_workday('2026-04-25'))  # 周六
        self.assertFalse(is_workday('2026-04-26'))  # 周日
    
    def test_is_workday_holiday(self):
        """测试工作日判断 - 节假日"""
        holidays = ['2026-04-27']
        self.assertFalse(is_workday('2026-04-27', holidays=holidays))


class TestDateRange(unittest.TestCase):
    """测试日期范围"""
    
    def test_date_range(self):
        """测试日期范围生成"""
        result = date_range('2026-04-25', '2026-04-28')
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0], date(2026, 4, 25))
        self.assertEqual(result[-1], date(2026, 4, 28))
    
    def test_date_range_reverse(self):
        """测试反向日期范围"""
        result = date_range('2026-04-28', '2026-04-25')
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0], date(2026, 4, 28))
    
    def test_date_range_with_step(self):
        """测试带步长的日期范围"""
        result = date_range('2026-04-25', '2026-04-30', step=timedelta(days=2))
        self.assertEqual(len(result), 3)
    
    def test_get_month_range(self):
        """测试月份范围"""
        start, end = get_month_range(2026, 2)
        self.assertEqual(start, date(2026, 2, 1))
        self.assertEqual(end, date(2026, 2, 28))
    
    def test_get_month_range_leap_year(self):
        """测试闰年二月"""
        start, end = get_month_range(2024, 2)
        self.assertEqual(end.day, 29)
    
    def test_get_week_range(self):
        """测试周范围"""
        start, end = get_week_range('2026-04-28')  # 周二
        # 2026-04-27 是周一
        self.assertEqual(start, date(2026, 4, 27))
        self.assertEqual(end, date(2026, 5, 3))


class TestTimestamp(unittest.TestCase):
    """测试时间戳操作"""
    
    def test_timestamp_to_datetime(self):
        """测试时间戳转日期"""
        result = timestamp_to_datetime(1745678400)
        self.assertIsInstance(result, datetime)
    
    def test_datetime_to_timestamp(self):
        """测试日期转时间戳"""
        dt = datetime(2025, 4, 26, 16, 0)
        result = datetime_to_timestamp(dt)
        self.assertIsInstance(result, int)
    
    def test_timestamp_ms(self):
        """测试毫秒时间戳"""
        ts = 1745678400000  # 毫秒
        result = timestamp_to_datetime(ts, ms=True)
        self.assertIsInstance(result, datetime)


class TestUtilities(unittest.TestCase):
    """测试工具函数"""
    
    def test_is_leap_year(self):
        """测试闰年判断"""
        self.assertTrue(is_leap_year(2024))
        self.assertFalse(is_leap_year(2025))
        self.assertFalse(is_leap_year(2026))
    
    def test_days_in_month(self):
        """测试月份天数"""
        self.assertEqual(days_in_month(2026, 1), 31)
        self.assertEqual(days_in_month(2026, 2), 28)
        self.assertEqual(days_in_month(2024, 2), 29)
        self.assertEqual(days_in_month(2026, 4), 30)
    
    def test_quarter(self):
        """测试季度"""
        self.assertEqual(quarter('2026-01-15'), 1)
        self.assertEqual(quarter('2026-04-27'), 2)
        self.assertEqual(quarter('2026-07-01'), 3)
        self.assertEqual(quarter('2026-10-15'), 4)
    
    def test_week_of_year(self):
        """测试周数"""
        year, week = week_of_year('2026-04-27')
        self.assertEqual(year, 2026)
        self.assertEqual(week, 18)  # 2026-04-27 是第18周
    
    def test_humanize_delta(self):
        """测试人性化时间差"""
        self.assertEqual(humanize_delta(3661), '1小时1分钟')
        self.assertEqual(humanize_delta(timedelta(days=2, hours=3)), '2天3小时')
        self.assertEqual(humanize_delta(65), '1分钟5秒')
    
    def test_format_duration(self):
        """测试时长格式化"""
        self.assertEqual(format_duration(3665), '1:01:05')
        self.assertEqual(format_duration(65), '1:05')
        self.assertEqual(format_duration(3600), '1:00:00')


class TestShortcuts(unittest.TestCase):
    """测试快捷函数"""
    
    def test_now(self):
        """测试 now 函数"""
        result = now()
        self.assertIsInstance(result, str)
        self.assertIn('2026', result)  # 当前年份
    
    def test_today(self):
        """测试 today 函数"""
        result = today()
        self.assertIsInstance(result, str)
    
    def test_yesterday(self):
        """测试 yesterday 函数"""
        result = yesterday()
        self.assertIsInstance(result, str)
    
    def test_tomorrow(self):
        """测试 tomorrow 函数"""
        result = tomorrow()
        self.assertIsInstance(result, str)


if __name__ == '__main__':
    unittest.main(verbosity=2)