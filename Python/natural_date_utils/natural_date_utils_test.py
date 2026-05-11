"""
自然语言日期解析工具库 - 测试文件
Test Suite for Natural Date Parser Utilities

测试覆盖：相对日期、星期日期、月度日期、年度日期、节日、绝对日期、时间解析等
"""

import unittest
from datetime import datetime, timedelta, time
from natural_date_utils import (
    NaturalDateParser,
    ParseResult,
    DateType,
    parse,
    parse_with_info,
    is_valid,
    get_date_type,
    parse_range,
    parse_batch,
    extract_dates,
)


class TestNaturalDateParser(unittest.TestCase):
    """自然语言日期解析器测试"""
    
    def setUp(self):
        """设置测试基准时间：2024年1月15日 周一 10:30"""
        self.now = datetime(2024, 1, 15, 10, 30, 0)  # 周一
        self.parser = NaturalDateParser(now=self.now)
    
    # ==================== 相对日期测试 ====================
    
    def test_today(self):
        """测试"今天"解析"""
        result = self.parser.parse("今天")
        self.assertTrue(result.success)
        self.assertEqual(result.datetime_obj.date(), self.now.date())
        self.assertEqual(result.date_type, DateType.RELATIVE)
    
    def test_tomorrow(self):
        """测试"明天"解析"""
        result = self.parser.parse("明天")
        self.assertTrue(result.success)
        expected = self.now.date() + timedelta(days=1)
        self.assertEqual(result.datetime_obj.date(), expected)
    
    def test_yesterday(self):
        """测试"昨天"解析"""
        result = self.parser.parse("昨天")
        self.assertTrue(result.success)
        expected = self.now.date() - timedelta(days=1)
        self.assertEqual(result.datetime_obj.date(), expected)
    
    def test_day_after_tomorrow(self):
        """测试"后天"解析"""
        result = self.parser.parse("后天")
        self.assertTrue(result.success)
        expected = self.now.date() + timedelta(days=2)
        self.assertEqual(result.datetime_obj.date(), expected)
    
    def test_day_before_yesterday(self):
        """测试"前天"解析"""
        result = self.parser.parse("前天")
        self.assertTrue(result.success)
        expected = self.now.date() - timedelta(days=2)
        self.assertEqual(result.datetime_obj.date(), expected)
    
    def test_three_days_after_tomorrow(self):
        """测试"大后天"解析"""
        result = self.parser.parse("大后天")
        self.assertTrue(result.success)
        expected = self.now.date() + timedelta(days=3)
        self.assertEqual(result.datetime_obj.date(), expected)
    
    def test_three_days_before_yesterday(self):
        """测试"大前天"解析"""
        result = self.parser.parse("大前天")
        self.assertTrue(result.success)
        expected = self.now.date() - timedelta(days=3)
        self.assertEqual(result.datetime_obj.date(), expected)
    
    def test_today_with_time(self):
        """测试"今天下午3点"解析"""
        result = self.parser.parse("今天下午3点")
        self.assertTrue(result.success)
        self.assertEqual(result.datetime_obj.date(), self.now.date())
        self.assertEqual(result.datetime_obj.hour, 15)
        self.assertEqual(result.datetime_obj.minute, 0)
        self.assertTrue(result.has_time)
    
    def test_tomorrow_morning(self):
        """测试"明天早上8点"解析"""
        result = self.parser.parse("明天早上8点")
        self.assertTrue(result.success)
        expected_date = self.now.date() + timedelta(days=1)
        self.assertEqual(result.datetime_obj.date(), expected_date)
        self.assertEqual(result.datetime_obj.hour, 8)
    
    def test_yesterday_evening(self):
        """测试"昨天晚上9点"解析"""
        result = self.parser.parse("昨天晚上9点")
        self.assertTrue(result.success)
        expected_date = self.now.date() - timedelta(days=1)
        self.assertEqual(result.datetime_obj.date(), expected_date)
        self.assertEqual(result.datetime_obj.hour, 21)
    
    # ==================== 星期日期测试 ====================
    
    def test_this_week_monday(self):
        """测试"这周一"解析（当天是周一，应该返回下周一）"""
        result = self.parser.parse("这周一")
        self.assertTrue(result.success)
        # 当天是周一，"这周一"应该是下周一
        expected = self.now.date() + timedelta(days=7)
        self.assertEqual(result.datetime_obj.date(), expected)
    
    def test_next_tuesday(self):
        """测试"下周二"解析"""
        result = self.parser.parse("下周二")
        self.assertTrue(result.success)
        # 当前是周一(0)，下周二(1) = 当前周一 + 7 + 1 = 8天后
        # 即下周的周二 = 2024-01-23
        expected = self.now.date() + timedelta(days=8)
        self.assertEqual(result.datetime_obj.date(), expected)
    
    def test_last_friday(self):
        """测试"上周五"解析"""
        result = self.parser.parse("上周五")
        self.assertTrue(result.success)
        # 当前是周一(0)，上周五(4) = 当前周一 - 7 + 4 = -3天
        # 即上周的周五 = 2024-01-12
        expected = self.now.date() - timedelta(days=3)
        self.assertEqual(result.datetime_obj.date(), expected)
    
    def test_weekday_various_forms(self):
        """测试星期的各种表达形式"""
        forms = [
            ("周三", DateType.WEEKDAY),
            ("星期三", DateType.WEEKDAY),
            ("礼拜三", DateType.WEEKDAY),
        ]
        for text, expected_type in forms:
            result = self.parser.parse(text)
            self.assertTrue(result.success, f"解析失败: {text}")
            self.assertEqual(result.date_type, expected_type)
            self.assertEqual(result.datetime_obj.weekday(), 2)  # 周三
    
    def test_next_week_sunday(self):
        """测试"下周日"解析"""
        result = self.parser.parse("下周日")
        self.assertTrue(result.success)
        # 当前是周一，下周日 = 6 + 7 = 13天后
        expected = self.now.date() + timedelta(days=13)
        self.assertEqual(result.datetime_obj.date(), expected)
    
    # ==================== 月度日期测试 ====================
    
    def test_next_month(self):
        """测试"下个月"解析"""
        result = self.parser.parse("下个月")
        self.assertTrue(result.success)
        expected_month = self.now.month + 1
        if expected_month > 12:
            expected_month = 1
        self.assertEqual(result.datetime_obj.month, expected_month)
    
    def test_last_month(self):
        """测试"上个月"解析"""
        result = self.parser.parse("上个月")
        self.assertTrue(result.success)
        expected_month = self.now.month - 1
        if expected_month < 1:
            expected_month = 12
        self.assertEqual(result.datetime_obj.month, expected_month)
    
    def test_next_month_15th(self):
        """测试"下个月15号"解析"""
        result = self.parser.parse("下个月15号")
        self.assertTrue(result.success)
        self.assertEqual(result.datetime_obj.month, 2)  # 2月
        self.assertEqual(result.datetime_obj.day, 15)
    
    def test_month_end(self):
        """测试"月底"解析"""
        result = self.parser.parse("月底")
        self.assertTrue(result.success)
        # 1月有31天
        self.assertEqual(result.datetime_obj.day, 31)
        self.assertEqual(result.datetime_obj.month, 1)
    
    # ==================== 年度日期测试 ====================
    
    def test_next_year(self):
        """测试"明年"解析"""
        result = self.parser.parse("明年")
        self.assertTrue(result.success)
        self.assertEqual(result.datetime_obj.year, 2025)
    
    def test_this_year(self):
        """测试"今年"解析"""
        result = self.parser.parse("今年")
        self.assertTrue(result.success)
        self.assertEqual(result.datetime_obj.year, 2024)
    
    def test_last_year(self):
        """测试"去年"解析"""
        result = self.parser.parse("去年")
        self.assertTrue(result.success)
        self.assertEqual(result.datetime_obj.year, 2023)
    
    def test_next_year_chinese_new_year(self):
        """测试"明年春节"解析"""
        result = self.parser.parse("明年春节")  # 春节是农历，这里只测试年份
        self.assertTrue(result.success)
        self.assertEqual(result.datetime_obj.year, 2025)
    
    # ==================== 节日日期测试 ====================
    
    def test_new_year(self):
        """测试"元旦"解析"""
        result = self.parser.parse("元旦")
        self.assertTrue(result.success)
        self.assertEqual(result.datetime_obj.month, 1)
        self.assertEqual(result.datetime_obj.day, 1)
    
    def test_valentines_day(self):
        """测试"情人节"解析"""
        result = self.parser.parse("情人节")
        self.assertTrue(result.success)
        self.assertEqual(result.datetime_obj.month, 2)
        self.assertEqual(result.datetime_obj.day, 14)
    
    def test_national_day(self):
        """测试"国庆节"解析"""
        result = self.parser.parse("国庆节")
        self.assertTrue(result.success)
        self.assertEqual(result.datetime_obj.month, 10)
        self.assertEqual(result.datetime_obj.day, 1)
    
    def test_christmas(self):
        """测试"圣诞节"解析"""
        result = self.parser.parse("圣诞节")
        self.assertTrue(result.success)
        self.assertEqual(result.datetime_obj.month, 12)
        self.assertEqual(result.datetime_obj.day, 25)
    
    def test_next_year_holiday(self):
        """测试"明年元旦"解析"""
        result = self.parser.parse("明年元旦")
        self.assertTrue(result.success)
        self.assertEqual(result.datetime_obj.year, 2025)
        self.assertEqual(result.datetime_obj.month, 1)
        self.assertEqual(result.datetime_obj.day, 1)
    
    # ==================== 绝对日期测试 ====================
    
    def test_full_date(self):
        """测试完整日期"2024年5月20日"解析"""
        result = self.parser.parse("2024年5月20日")
        self.assertTrue(result.success)
        self.assertEqual(result.datetime_obj.year, 2024)
        self.assertEqual(result.datetime_obj.month, 5)
        self.assertEqual(result.datetime_obj.day, 20)
    
    def test_month_day(self):
        """测试月日"5月20日"解析"""
        result = self.parser.parse("5月20日")
        self.assertTrue(result.success)
        self.assertEqual(result.datetime_obj.month, 5)
        self.assertEqual(result.datetime_obj.day, 20)
    
    def test_full_date_with_time(self):
        """测试完整日期带时间"""
        result = self.parser.parse("2024年5月20日下午3点30分")
        self.assertTrue(result.success)
        self.assertEqual(result.datetime_obj.year, 2024)
        self.assertEqual(result.datetime_obj.month, 5)
        self.assertEqual(result.datetime_obj.day, 20)
        self.assertEqual(result.datetime_obj.hour, 15)
        self.assertEqual(result.datetime_obj.minute, 30)
    
    # ==================== 数字天数测试 ====================
    
    def test_3_days_later(self):
        """测试"3天后"解析"""
        result = self.parser.parse("3天后")
        self.assertTrue(result.success)
        expected = self.now.date() + timedelta(days=3)
        self.assertEqual(result.datetime_obj.date(), expected)
    
    def test_7_days_ago(self):
        """测试"7天前"解析"""
        result = self.parser.parse("7天前")
        self.assertTrue(result.success)
        expected = self.now.date() - timedelta(days=7)
        self.assertEqual(result.datetime_obj.date(), expected)
    
    def test_2_weeks_later(self):
        """测试"2周后"解析"""
        result = self.parser.parse("2周后")
        self.assertTrue(result.success)
        expected = self.now.date() + timedelta(weeks=2)
        self.assertEqual(result.datetime_obj.date(), expected)
    
    def test_3_months_later(self):
        """测试"3个月后"解析"""
        result = self.parser.parse("3个月后")
        self.assertTrue(result.success)
        # 1月 + 3个月 = 4月
        self.assertEqual(result.datetime_obj.month, 4)
    
    def test_1_year_later(self):
        """测试"1年后"解析"""
        result = self.parser.parse("1年后")
        self.assertTrue(result.success)
        self.assertEqual(result.datetime_obj.year, 2025)
    
    # ==================== 时间段测试 ====================
    
    def test_early_morning(self):
        """测试"凌晨"时间段"""
        result = self.parser.parse("明天凌晨")
        self.assertTrue(result.success)
        self.assertLess(result.datetime_obj.hour, 6)
    
    def test_morning(self):
        """测试"早上"时间段"""
        result = self.parser.parse("明天早上")
        self.assertTrue(result.success)
        self.assertGreaterEqual(result.datetime_obj.hour, 6)
        self.assertLess(result.datetime_obj.hour, 9)
    
    def test_afternoon(self):
        """测试"下午"时间段"""
        result = self.parser.parse("明天下午")
        self.assertTrue(result.success)
        self.assertGreaterEqual(result.datetime_obj.hour, 14)
        self.assertLess(result.datetime_obj.hour, 18)
    
    def test_evening(self):
        """测试"晚上"时间段"""
        result = self.parser.parse("明天晚上")
        self.assertTrue(result.success)
        self.assertGreaterEqual(result.datetime_obj.hour, 18)
    
    def test_late_night(self):
        """测试"深夜"时间段"""
        result = self.parser.parse("明天深夜")
        self.assertTrue(result.success)
        self.assertGreaterEqual(result.datetime_obj.hour, 22)
    
    # ==================== 日期范围测试 ====================
    
    def test_this_week(self):
        """测试"这周"解析"""
        result = self.parser.parse("这周")
        self.assertTrue(result.success)
        self.assertEqual(result.date_type, DateType.RANGE)
    
    def test_next_week(self):
        """测试"下周"解析"""
        result = self.parser.parse("下周")
        self.assertTrue(result.success)
        self.assertEqual(result.date_type, DateType.RANGE)
    
    def test_this_month(self):
        """测试"这个月"解析"""
        result = self.parser.parse("这个月")
        self.assertTrue(result.success)
        self.assertEqual(result.date_type, DateType.RANGE)
    
    # ==================== 中文数字转换测试 ====================
    
    def test_chinese_numbers(self):
        """测试中文数字转换"""
        result = self.parser.parse("三天后")
        self.assertTrue(result.success)
        expected = self.now.date() + timedelta(days=3)
        self.assertEqual(result.datetime_obj.date(), expected)
    
    def test_chinese_weekday(self):
        """测试中文星期表达"""
        result = self.parser.parse("下星期三")
        self.assertTrue(result.success)
        # 验证是周三
        self.assertEqual(result.datetime_obj.weekday(), 2)
    
    # ==================== 边界情况测试 ====================
    
    def test_invalid_input(self):
        """测试无效输入"""
        result = self.parser.parse("这是一个无效的日期")
        self.assertFalse(result.success)
        self.assertIsNone(result.datetime_obj)
    
    def test_empty_input(self):
        """测试空输入"""
        result = self.parser.parse("")
        self.assertFalse(result.success)
    
    def test_whitespace_handling(self):
        """测试空白字符处理"""
        result = self.parser.parse("  明天  ")
        self.assertTrue(result.success)
    
    # ==================== 便捷函数测试 ====================
    
    def test_parse_function(self):
        """测试 parse 便捷函数"""
        dt = parse("明天", now=self.now)
        self.assertIsNotNone(dt)
        expected = self.now.date() + timedelta(days=1)
        self.assertEqual(dt.date(), expected)
    
    def test_parse_with_info_function(self):
        """测试 parse_with_info 便捷函数"""
        result = parse_with_info("明天下午3点", now=self.now)
        self.assertTrue(result.success)
        self.assertEqual(result.datetime_obj.hour, 15)
        self.assertTrue(result.has_time)
    
    def test_is_valid_function(self):
        """测试 is_valid 便捷函数"""
        self.assertTrue(is_valid("明天", now=self.now))
        self.assertFalse(is_valid("无效日期", now=self.now))
    
    def test_get_date_type_function(self):
        """测试 get_date_type 便捷函数"""
        self.assertEqual(get_date_type("明天", now=self.now), DateType.RELATIVE)
        self.assertEqual(get_date_type("下周三", now=self.now), DateType.WEEKDAY)
        self.assertEqual(get_date_type("国庆节", now=self.now), DateType.ABSOLUTE)
    
    def test_parse_range_function(self):
        """测试 parse_range 便捷函数"""
        start, end = parse_range("这周", now=self.now)
        self.assertIsNotNone(start)
        self.assertIsNotNone(end)
        # 一周有7天
        self.assertEqual((end.date() - start.date()).days, 6)
    
    def test_parse_batch_function(self):
        """测试 parse_batch 便捷函数"""
        texts = ["今天", "明天", "后天"]
        results = parse_batch(texts, now=self.now)
        self.assertEqual(len(results), 3)
        for result in results:
            self.assertTrue(result.success)
    
    def test_extract_dates_function(self):
        """测试 extract_dates 便捷函数"""
        text = "今天要开会，明天交报告，后天放假"
        dates = extract_dates(text, now=self.now)
        self.assertGreater(len(dates), 0)
    
    # ==================== 特殊场景测试 ====================
    
    def test_cross_month(self):
        """测试跨月场景"""
        # 设置为月底
        parser = NaturalDateParser(now=datetime(2024, 1, 30, 10, 0))
        result = parser.parse("3天后")
        self.assertTrue(result.success)
        self.assertEqual(result.datetime_obj.month, 2)
    
    def test_cross_year(self):
        """测试跨年场景"""
        # 设置为年底
        parser = NaturalDateParser(now=datetime(2024, 12, 30, 10, 0))
        result = parser.parse("3天后")
        self.assertTrue(result.success)
        self.assertEqual(result.datetime_obj.year, 2025)
        self.assertEqual(result.datetime_obj.month, 1)
    
    def test_february_29(self):
        """测试闰年2月29日"""
        result = self.parser.parse("2月29日")
        # 2024年是闰年
        self.assertTrue(result.success)
        self.assertEqual(result.datetime_obj.month, 2)
        self.assertEqual(result.datetime_obj.day, 29)
    
    def test_time_with_minutes(self):
        """测试带分钟的时间"""
        result = self.parser.parse("明天15点30分")
        self.assertTrue(result.success)
        self.assertEqual(result.datetime_obj.hour, 15)
        self.assertEqual(result.datetime_obj.minute, 30)
    
    def test_time_with_colon(self):
        """测试冒号分隔的时间"""
        result = self.parser.parse("明天15:30")
        self.assertTrue(result.success)
        self.assertEqual(result.datetime_obj.hour, 15)
        self.assertEqual(result.datetime_obj.minute, 30)


class TestTimePeriodParsing(unittest.TestCase):
    """时间段解析测试"""
    
    def setUp(self):
        self.now = datetime(2024, 1, 15, 10, 30, 0)
        self.parser = NaturalDateParser(now=self.now)
    
    def test_all_time_periods(self):
        """测试所有时间段"""
        periods = [
            ("凌晨", 0, 6),
            ("早上", 6, 9),
            ("上午", 9, 12),
            ("中午", 11, 14),
            ("下午", 14, 18),
            ("傍晚", 17, 19),
            ("晚上", 18, 22),
            ("深夜", 22, 24),
        ]
        
        for period, start_h, end_h in periods:
            result = self.parser.parse(f"明天{period}")
            self.assertTrue(result.success, f"解析失败: 明天{period}")
            self.assertGreaterEqual(result.datetime_obj.hour, start_h,
                                   f"{period} 时间段错误")


class TestEdgeCases(unittest.TestCase):
    """边界情况测试"""
    
    def test_multiple_expressions(self):
        """测试多个表达混合"""
        parser = NaturalDateParser(now=datetime(2024, 1, 15, 10, 0))
        
        # 下周一下午3点
        result = parser.parse("下周一下午3点")
        self.assertTrue(result.success)
        self.assertEqual(result.datetime_obj.weekday(), 0)  # 周一
        self.assertEqual(result.datetime_obj.hour, 15)
    
    def test_specific_date_next_year(self):
        """测试已过日期默认明年"""
        parser = NaturalDateParser(now=datetime(2024, 6, 15, 10, 0))
        # 1月1日已经过了，应该是明年
        result = parser.parse("1月1日")
        self.assertTrue(result.success)
        self.assertEqual(result.datetime_obj.year, 2025)
    
    def test_chinese_number_day(self):
        """测试中文数字日期"""
        parser = NaturalDateParser(now=datetime(2024, 1, 15, 10, 0))
        result = parser.parse("十五天后")
        self.assertTrue(result.success)
        expected = parser.now.date() + timedelta(days=15)
        self.assertEqual(result.datetime_obj.date(), expected)


class TestParseResult(unittest.TestCase):
    """解析结果测试"""
    
    def test_parse_result_properties(self):
        """测试 ParseResult 属性"""
        parser = NaturalDateParser(now=datetime(2024, 1, 15, 10, 0))
        result = parser.parse("明天下午3点")
        
        self.assertTrue(result.success)
        self.assertIsNotNone(result.datetime_obj)
        self.assertEqual(result.original_text, "明天下午3点")
        self.assertEqual(result.date_type, DateType.RELATIVE)
        self.assertEqual(result.confidence, 1.0)
        self.assertTrue(result.has_time)
        self.assertIsNone(result.error_message)
    
    def test_failed_parse_result(self):
        """测试失败解析结果"""
        parser = NaturalDateParser(now=datetime(2024, 1, 15, 10, 0))
        result = parser.parse("无效日期")
        
        self.assertFalse(result.success)
        self.assertIsNone(result.datetime_obj)
        self.assertEqual(result.date_type, DateType.UNKNOWN)
        self.assertIsNotNone(result.error_message)


class TestHolidays(unittest.TestCase):
    """节日测试"""
    
    def setUp(self):
        self.parser = NaturalDateParser(now=datetime(2024, 1, 15, 10, 0))
    
    def test_all_holidays(self):
        """测试所有节日"""
        holidays = {
            "元旦": (1, 1),
            "情人节": (2, 14),
            "妇女节": (3, 8),
            "植树节": (3, 12),
            "愚人节": (4, 1),
            "劳动节": (5, 1),
            "青年节": (5, 4),
            "儿童节": (6, 1),
            "建党节": (7, 1),
            "建军节": (8, 1),
            "教师节": (9, 10),
            "国庆节": (10, 1),
            "万圣节": (10, 31),
            "光棍节": (11, 11),
            "平安夜": (12, 24),
            "圣诞节": (12, 25),
        }
        
        for holiday, (month, day) in holidays.items():
            result = self.parser.parse(holiday)
            self.assertTrue(result.success, f"解析节日失败: {holiday}")
            self.assertEqual(result.datetime_obj.month, month, f"{holiday} 月份错误")
            self.assertEqual(result.datetime_obj.day, day, f"{holiday} 日期错误")


if __name__ == "__main__":
    unittest.main()