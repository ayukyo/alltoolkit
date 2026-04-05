"""
DateTime Utilities Test Suite
时间日期工具模块测试套件
"""

import unittest
import time
from datetime import datetime, timedelta
from mod import DateTimeUtils, now, format_datetime, parse_datetime, days_between, is_leap_year, get_age, relative_time


class TestDateTimeUtils(unittest.TestCase):
    """DateTimeUtils 测试类"""

    def test_now(self):
        """测试获取当前时间"""
        dt = DateTimeUtils.now()
        self.assertIsInstance(dt, datetime)
        # 验证时间在合理范围内（前后5秒）
        self.assertAlmostEqual(dt.timestamp(), time.time(), delta=5)

    def test_now_utc(self):
        """测试获取 UTC 时间"""
        dt = DateTimeUtils.now_utc()
        self.assertIsInstance(dt, datetime)
        self.assertIsNotNone(dt.tzinfo)

    def test_today(self):
        """测试获取今天日期"""
        today = DateTimeUtils.today()
        self.assertEqual(today.hour, 0)
        self.assertEqual(today.minute, 0)
        self.assertEqual(today.second, 0)
        self.assertEqual(today.date(), datetime.now().date())

    def test_timestamp(self):
        """测试获取时间戳"""
        ts = DateTimeUtils.timestamp()
        self.assertIsInstance(ts, float)
        self.assertAlmostEqual(ts, time.time(), delta=1)

    def test_timestamp_ms(self):
        """测试获取毫秒时间戳"""
        ts = DateTimeUtils.timestamp_ms()
        self.assertIsInstance(ts, int)
        self.assertAlmostEqual(ts / 1000, time.time(), delta=1)

    def test_timestamp_conversion(self):
        """测试时间戳转换"""
        original = datetime(2024, 3, 15, 10, 30, 0)

        # 秒级
        ts_s = DateTimeUtils.datetime_to_timestamp(original, 's')
        dt_s = DateTimeUtils.timestamp_to_datetime(ts_s, 's')
        self.assertEqual(original.replace(microsecond=0), dt_s.replace(microsecond=0))

        # 毫秒级
        ts_ms = DateTimeUtils.datetime_to_timestamp(original, 'ms')
        dt_ms = DateTimeUtils.timestamp_to_datetime(ts_ms, 'ms')
        self.assertEqual(original.replace(microsecond=0), dt_ms.replace(microsecond=0))

        # 微秒级
        ts_us = DateTimeUtils.datetime_to_timestamp(original, 'us')
        dt_us = DateTimeUtils.timestamp_to_datetime(ts_us, 'us')
        self.assertEqual(original.replace(microsecond=0), dt_us.replace(microsecond=0))

    def test_format(self):
        """测试格式化"""
        dt = datetime(2024, 3, 15, 10, 30, 0)

        # 默认格式
        result = DateTimeUtils.format(dt)
        self.assertEqual(result, "2024-03-15 10:30:00")

        # ISO 8601 格式
        result = DateTimeUtils.format(dt, DateTimeUtils.FORMAT_ISO8601)
        self.assertEqual(result, "2024-03-15T10:30:00")

        # 日期格式
        result = DateTimeUtils.format(dt, DateTimeUtils.FORMAT_DATE)
        self.assertEqual(result, "2024-03-15")

        # 中文格式
        result = DateTimeUtils.format(dt, DateTimeUtils.FORMAT_CHINESE)
        self.assertEqual(result, "2024年03月15日 10时30分00秒")

    def test_parse(self):
        """测试解析"""
        # 默认格式
        dt = DateTimeUtils.parse("2024-03-15 10:30:00")
        self.assertEqual(dt.year, 2024)
        self.assertEqual(dt.month, 3)
        self.assertEqual(dt.day, 15)
        self.assertEqual(dt.hour, 10)
        self.assertEqual(dt.minute, 30)
        self.assertEqual(dt.second, 0)

        # ISO 8601 格式
        dt = DateTimeUtils.parse("2024-03-15T10:30:00", DateTimeUtils.FORMAT_ISO8601)
        self.assertEqual(dt.year, 2024)
        self.assertEqual(dt.month, 3)
        self.assertEqual(dt.day, 15)

    def test_parse_auto(self):
        """测试自动解析"""
        # 多种格式测试
        test_cases = [
            ("2024-03-15 10:30:00", datetime(2024, 3, 15, 10, 30, 0)),
            ("2024-03-15", datetime(2024, 3, 15)),
            ("2024/03/15 10:30:00", datetime(2024, 3, 15, 10, 30, 0)),
            ("15/03/2024", datetime(2024, 3, 15)),
            ("2024-03-15T10:30:00", datetime(2024, 3, 15, 10, 30, 0)),
            ("10:30:00", datetime(1900, 1, 1, 10, 30, 0)),
        ]

        for date_str, expected in test_cases:
            result = DateTimeUtils.parse_auto(date_str)
            self.assertIsNotNone(result, f"Failed to parse: {date_str}")
            if result:
                self.assertEqual(result.replace(microsecond=0), expected.replace(microsecond=0))

        # 无效格式
        result = DateTimeUtils.parse_auto("invalid")
        self.assertIsNone(result)

    def test_add_time(self):
        """测试时间加减"""
        dt = datetime(2024, 3, 15, 10, 30, 0)

        # 加天数
        result = DateTimeUtils.add_days(dt, 5)
        self.assertEqual(result.day, 20)

        # 减天数
        result = DateTimeUtils.add_days(dt, -5)
        self.assertEqual(result.day, 10)

        # 加小时
        result = DateTimeUtils.add_hours(dt, 3)
        self.assertEqual(result.hour, 13)

        # 加分钟
        result = DateTimeUtils.add_minutes(dt, 45)
        self.assertEqual(result.minute, 15)
        self.assertEqual(result.hour, 11)

        # 加秒
        result = DateTimeUtils.add_seconds(dt, 45)
        self.assertEqual(result.second, 45)

    def test_add_months(self):
        """测试月份加减"""
        dt = datetime(2024, 3, 15, 10, 30, 0)

        # 加月份
        result = DateTimeUtils.add_months(dt, 2)
        self.assertEqual(result.month, 5)
        self.assertEqual(result.day, 15)

        # 跨年
        result = DateTimeUtils.add_months(dt, 10)
        self.assertEqual(result.year, 2025)
        self.assertEqual(result.month, 1)

        # 减月份
        result = DateTimeUtils.add_months(dt, -2)
        self.assertEqual(result.month, 1)

    def test_add_years(self):
        """测试年份加减"""
        dt = datetime(2024, 3, 15, 10, 30, 0)

        # 加年份
        result = DateTimeUtils.add_years(dt, 2)
        self.assertEqual(result.year, 2026)

        # 减年份
        result = DateTimeUtils.add_years(dt, -2)
        self.assertEqual(result.year, 2022)

        # 闰年 2月29日处理
        dt_leap = datetime(2024, 2, 29, 10, 30, 0)
        result = DateTimeUtils.add_years(dt_leap, 1)
        self.assertEqual(result.year, 2025)
        self.assertEqual(result.month, 2)

    def test_time_between(self):
        """测试时间差计算"""
        start = datetime(2024, 3, 15, 10, 0, 0)
        end = datetime(2024, 3, 17, 14, 30, 45)

        # 天数差
        days = DateTimeUtils.days_between(start, end)
        self.assertEqual(days, 2)

        # 小时差
        hours = DateTimeUtils.hours_between(start, end)
        self.assertAlmostEqual(hours, 52.5125, places=2)

        # 分钟差
        minutes = DateTimeUtils.minutes_between(start, end)
        self.assertAlmostEqual(minutes, 3150.75, places=2)

        # 秒差
        seconds = DateTimeUtils.seconds_between(start, end)
        self.assertEqual(seconds, 189045)

    def test_is_date_checks(self):
        """测试日期判断"""
        today = DateTimeUtils.today()
        yesterday = DateTimeUtils.add_days(today, -1)
        tomorrow = DateTimeUtils.add_days(today, 1)

        self.assertTrue(DateTimeUtils.is_today(today))
        self.assertTrue(DateTimeUtils.is_yesterday(yesterday))
        self.assertTrue(DateTimeUtils.is_tomorrow(tomorrow))

    def test_weekend_weekday(self):
        """测试周末/工作日判断"""
        # 2024-03-15 是星期五
        friday = datetime(2024, 3, 15)
        self.assertTrue(DateTimeUtils.is_weekday(friday))
        self.assertFalse(DateTimeUtils.is_weekend(friday))

        # 2024-03-16 是星期六
        saturday = datetime(2024, 3, 16)
        self.assertFalse(DateTimeUtils.is_weekday(saturday))
        self.assertTrue(DateTimeUtils.is_weekend(saturday))

        # 2024-03-17 是星期日
        sunday = datetime(2024, 3, 17)
        self.assertFalse(DateTimeUtils.is_weekday(sunday))
        self.assertTrue(DateTimeUtils.is_weekend(sunday))

    def test_leap_year(self):
        """测试闰年判断"""
        self.assertTrue(DateTimeUtils.is_leap_year(2024))
        self.assertTrue(DateTimeUtils.is_leap_year(2000))
        self.assertFalse(DateTimeUtils.is_leap_year(2023))
        self.assertFalse(DateTimeUtils.is_leap_year(1900))

    def test_days_in_month(self):
        """测试月份天数"""
        self.assertEqual(DateTimeUtils.days_in_month(2024, 2), 29)  # 闰年
        self.assertEqual(DateTimeUtils.days_in_month(2023, 2), 28)  # 平年
        self.assertEqual(DateTimeUtils.days_in_month(2024, 1), 31)
        self.assertEqual(DateTimeUtils.days_in_month(2024, 4), 30)

    def test_start_end_of_period(self):
        """测试周期开始/结束时间"""
        dt = datetime(2024, 3, 15, 10, 30, 0)

        # 当天开始
        start = DateTimeUtils.start_of_day(dt)
        self.assertEqual(start.hour, 0)
        self.assertEqual(start.minute, 0)
        self.assertEqual(start.second, 0)

        # 当天结束
        end = DateTimeUtils.end_of_day(dt)
        self.assertEqual(end.hour, 23)
        self.assertEqual(end.minute, 59)
        self.assertEqual(end.second, 59)

        # 当周开始（周一）
        start = DateTimeUtils.start_of_week(dt)
        self.assertEqual(start.weekday(), 0)  # Monday

        # 当周结束（周日）
        end = DateTimeUtils.end_of_week(dt)
        self.assertEqual(end.weekday(), 6)  # Sunday

        # 当月开始
        start = DateTimeUtils.start_of_month(dt)
        self.assertEqual(start.day, 1)

        # 当月结束
        end = DateTimeUtils.end_of_month(dt)
        self.assertEqual(end.day, 31)

        # 当年开始
        start = DateTimeUtils.start_of_year(dt)
        self.assertEqual(start.month, 1)
        self.assertEqual(start.day, 1)

        # 当年结束
        end = DateTimeUtils.end_of_year(dt)
        self.assertEqual(end.month, 12)
        self.assertEqual(end.day, 31)

    def test_get_age(self):
        """测试年龄计算"""
        today = datetime(2024, 3, 15)

        # 刚好过生日
        birth = datetime(2000, 3, 14)
        age = DateTimeUtils.get_age(birth, today)
        self.assertEqual(age, 24)

        # 还没过生日
        birth = datetime(2000, 3, 16)
        age = DateTimeUtils.get_age(birth, today)
        self.assertEqual(age, 23)

        # 刚好今天生日
        birth = datetime(2000, 3, 15)
        age = DateTimeUtils.get_age(birth, today)
        self.assertEqual(age, 24)

    def test_weekday_name(self):
        """测试星期名称"""
        dt = datetime(2024, 3, 15)  # Friday

        self.assertEqual(DateTimeUtils.get_weekday_name(dt, 'en'), 'Friday')
        self.assertEqual(DateTimeUtils.get_weekday_name(dt, 'cn'), '星期五')
        self.assertEqual(DateTimeUtils.get_weekday_name(dt, 'short'), 'Fri')

    def test_month_name(self):
        """测试月份名称"""
        self.assertEqual(DateTimeUtils.get_month_name(3, 'en'), 'March')
        self.assertEqual(DateTimeUtils.get_month_name(3, 'cn'), '三月')
        self.assertEqual(DateTimeUtils.get_month_name(3, 'short'), 'Mar')

    def test_relative_time(self):
        """测试相对时间"""
        now = datetime.now()

        # 刚刚
        dt = now - timedelta(seconds=30)
        self.assertEqual(DateTimeUtils.relative_time(dt, now), "刚刚")

        # 几分钟前
        dt = now - timedelta(minutes=5)
        self.assertEqual(DateTimeUtils.relative_time(dt, now), "5分钟前")

        # 几小时前
        dt = now - timedelta(hours=3)
        self.assertEqual(DateTimeUtils.relative_time(dt, now), "3小时前")

        # 昨天
        dt = now - timedelta(days=1)
        self.assertEqual(DateTimeUtils.relative_time(dt, now), "昨天")

        # 几天前
        dt = now - timedelta(days=5)
        self.assertEqual(DateTimeUtils.relative_time(dt, now), "5天前")

    def test_format_duration(self):
        """测试时长格式化"""
        # 秒
        self.assertEqual(DateTimeUtils.format_duration(45), "45秒")

        # 分钟
        self.assertEqual(DateTimeUtils.format_duration(300), "5分钟")
        self.assertEqual(DateTimeUtils.format_duration(365), "6分5秒")

        # 小时
        self.assertEqual(DateTimeUtils.format_duration(7200), "2小时")
        self.assertEqual(DateTimeUtils.format_duration(7500), "2小时5分")

        # 天
        self.assertEqual(DateTimeUtils.format_duration(172800), "2天")
        self.assertEqual(DateTimeUtils.format_duration(176400), "2天1小时")

    def test_countdown(self):
        """测试倒计时"""
        now = datetime.now()
        target = now + timedelta(days=2, hours=5, minutes=30, seconds=15)

        result = DateTimeUtils.countdown(target, now)
        self.assertEqual(result['days'], 2)
        self.assertEqual(result['hours'], 5)
        self.assertEqual(result['minutes'], 30)
        self.assertEqual(result['seconds'], 15)
        # 2天5小时30分15秒 = 2*86400 + 5*3600 + 30*60 + 15 = 192615
        self.assertEqual(result['total_seconds'], 192615)

    def test_generate_date_range(self):
        """测试日期范围生成"""
        start = datetime(2024, 3, 1)
        end = datetime(2024, 3, 5)

        dates = DateTimeUtils.generate_date_range(start, end)
        self.assertEqual(len(dates), 5)
        self.assertEqual(dates[0].day, 1)
        self.assertEqual(dates[4].day, 5)

        # 步长为2
        dates = DateTimeUtils.generate_date_range(start, end, step_days=2)
        self.assertEqual(len(dates), 3)
        self.assertEqual(dates[0].day, 1)
        self.assertEqual(dates[1].day, 3)
        self.assertEqual(dates[2].day, 5)

    def test_iso8601(self):
        """测试 ISO 8601 格式"""
        dt = datetime(2024, 3, 15, 10, 30, 0)

        # 转换为 ISO 8601
        iso = DateTimeUtils.to_iso8601(dt)
        self.assertIn("2024-03-15", iso)
        self.assertIn("10:30:00", iso)

        # 从 ISO 8601 解析
        parsed = DateTimeUtils.from_iso8601(iso)
        self.assertEqual(parsed.year, 2024)
        self.assertEqual(parsed.month, 3)
        self.assertEqual(parsed.day, 15)

    def test_convenience_functions(self):
        """测试便捷函数"""
        # now
        dt = now()
        self.assertIsInstance(dt, datetime)

        # format_datetime
        dt = datetime(2024, 3, 15, 10, 30, 0)
        result = format_datetime(dt)
        self.assertEqual(result, "2024-03-15 10:30:00")

        # parse_datetime
        dt = parse_datetime("2024-03-15 10:30:00")
        self.assertEqual(dt.year, 2024)

        # days_between
        start = datetime(2024, 3, 1)
        end = datetime(2024, 3, 10)
        self.assertEqual(days_between(start, end), 9)

        # is_leap_year
        self.assertTrue(is_leap_year(2024))
        self.assertFalse(is_leap_year(2023))

        # get_age
        birth = datetime(2000, 1, 1)
        age = get_age(birth)
        self.assertGreaterEqual(age, 24)

        # relative_time
        dt = datetime.now() - timedelta(hours=2)
        self.assertEqual(relative_time(dt), "2小时前")


class TestEdgeCases(unittest.TestCase):
    """边界情况测试"""

    def test_invalid_unit(self):
        """测试无效的时间单位"""
        with self.assertRaises(ValueError):
            DateTimeUtils.timestamp_to_datetime(1234567890, 'invalid')

        with self.assertRaises(ValueError):
            DateTimeUtils.datetime_to_timestamp(datetime.now(), 'invalid')

    def test_month_boundary(self):
        """测试月份边界"""
        # 1月31日加1个月
        dt = datetime(2024, 1, 31)
        result = DateTimeUtils.add_months(dt, 1)
        # 2月只有29天（闰年），所以应该是2月29日
        self.assertEqual(result.month, 2)
        self.assertEqual(result.day, 29)

        # 3月31日减1个月
        dt = datetime(2024, 3, 31)
        result = DateTimeUtils.add_months(dt, -1)
        self.assertEqual(result.month, 2)
        self.assertEqual(result.day, 29)

    def test_year_boundary(self):
        """测试年份边界"""
        # 12月加1个月
        dt = datetime(2024, 12, 15)
        result = DateTimeUtils.add_months(dt, 1)
        self.assertEqual(result.year, 2025)
        self.assertEqual(result.month, 1)

        # 1月减1个月
        dt = datetime(2024, 1, 15)
        result = DateTimeUtils.add_months(dt, -1)
        self.assertEqual(result.year, 2023)
        self.assertEqual(result.month, 12)

    def test_empty_date_range(self):
        """测试空日期范围"""
        start = datetime(2024, 3, 10)
        end = datetime(2024, 3, 5)
        dates = DateTimeUtils.generate_date_range(start, end)
        self.assertEqual(len(dates), 0)

    def test_single_day_range(self):
        """测试单日范围"""
        start = datetime(2024, 3, 15)
        end = datetime(2024, 3, 15)
        dates = DateTimeUtils.generate_date_range(start, end)
        self.assertEqual(len(dates), 1)
        self.assertEqual(dates[0].day, 15)


if __name__ == '__main__':
    unittest.main()
