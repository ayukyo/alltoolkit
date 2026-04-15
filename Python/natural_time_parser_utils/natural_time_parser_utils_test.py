"""
Natural Time Parser Utilities - 单元测试

测试自然语言时间解析功能。

Author: AllToolkit
"""

import unittest
from datetime import datetime, timedelta
from Python.natural_time_parser_utils.mod import (
    NaturalTimeParser,
    DurationParser,
    TimeExpressionExtractor,
    RelativeTimeFormatter,
    ParseError,
    parse_time,
    parse_duration,
    format_duration,
    extract_times,
    relative_time,
    when,
    how_long,
)


class TestNaturalTimeParser(unittest.TestCase):
    """测试自然语言时间解析器"""
    
    def setUp(self):
        """设置测试环境"""
        self.reference = datetime(2026, 4, 16, 7, 0, 0)  # 2026年4月16日 7:00
        self.parser = NaturalTimeParser(self.reference)
    
    def test_relative_time_english(self):
        """测试英文相对时间"""
        # 分钟
        result = self.parser.parse("in 5 minutes")
        expected = self.reference + timedelta(minutes=5)
        self.assertEqual(result, expected)
        
        # 小时
        result = self.parser.parse("in 2 hours")
        expected = self.reference + timedelta(hours=2)
        self.assertEqual(result, expected)
        
        # 天
        result = self.parser.parse("in 3 days")
        expected = self.reference + timedelta(days=3)
        self.assertEqual(result, expected)
        
        # 周
        result = self.parser.parse("in 1 week")
        expected = self.reference + timedelta(weeks=1)
        self.assertEqual(result, expected)
    
    def test_relative_time_chinese(self):
        """测试中文相对时间"""
        # 分钟后
        result = self.parser.parse("5分钟后")
        expected = self.reference + timedelta(minutes=5)
        self.assertEqual(result, expected)
        
        # 小时后
        result = self.parser.parse("2小时后")
        expected = self.reference + timedelta(hours=2)
        self.assertEqual(result, expected)
        
        # 天后
        result = self.parser.parse("3天后")
        expected = self.reference + timedelta(days=3)
        self.assertEqual(result, expected)
        
        # 半小时后
        result = self.parser.parse("半小时后")
        expected = self.reference + timedelta(minutes=30)
        self.assertEqual(result, expected)
    
    def test_absolute_time_english(self):
        """测试英文绝对时间"""
        # today
        result = self.parser.parse("today")
        expected = datetime(2026, 4, 16, 0, 0, 0)
        self.assertEqual(result, expected)
        
        # tomorrow
        result = self.parser.parse("tomorrow")
        expected = datetime(2026, 4, 17, 0, 0, 0)
        self.assertEqual(result, expected)
        
        # yesterday
        result = self.parser.parse("yesterday")
        expected = datetime(2026, 4, 15, 0, 0, 0)
        self.assertEqual(result, expected)
    
    def test_absolute_time_chinese(self):
        """测试中文绝对时间"""
        # 今天
        result = self.parser.parse("今天")
        expected = datetime(2026, 4, 16, 0, 0, 0)
        self.assertEqual(result, expected)
        
        # 明天
        result = self.parser.parse("明天")
        expected = datetime(2026, 4, 17, 0, 0, 0)
        self.assertEqual(result, expected)
        
        # 后天
        result = self.parser.parse("后天")
        expected = datetime(2026, 4, 18, 0, 0, 0)
        self.assertEqual(result, expected)
    
    def test_weekday_english(self):
        """测试英文星期"""
        # next monday (2026-04-16 是周四)
        result = self.parser.parse("next monday")
        expected = datetime(2026, 4, 20, 0, 0, 0)  # 下周一
        self.assertEqual(result, expected)
        
        # next friday
        result = self.parser.parse("next friday")
        expected = datetime(2026, 4, 17, 0, 0, 0)  # 明天是周五
        self.assertEqual(result, expected)
    
    def test_weekday_chinese(self):
        """测试中文星期"""
        # 周一
        result = self.parser.parse("周一")
        expected = datetime(2026, 4, 20, 0, 0, 0)  # 下周一
        self.assertEqual(result, expected)
        
        # 下周三
        result = self.parser.parse("下周三")
        expected = datetime(2026, 4, 22, 0, 0, 0)
        self.assertEqual(result, expected)
        
        # 上周五
        result = self.parser.parse("上周五")
        expected = datetime(2026, 4, 10, 0, 0, 0)
        self.assertEqual(result, expected)
    
    def test_time_only_english(self):
        """测试英文纯时间"""
        # at 3pm
        result = self.parser.parse("at 3pm")
        expected = self.reference.replace(hour=15, minute=0)
        self.assertEqual(result, expected)
        
        # at 9am
        result = self.parser.parse("at 9am")
        expected = self.reference.replace(hour=9, minute=0)
        self.assertEqual(result, expected)
        
        # at 15:30
        result = self.parser.parse("at 15:30")
        expected = self.reference.replace(hour=15, minute=30)
        self.assertEqual(result, expected)
    
    def test_time_only_chinese(self):
        """测试中文纯时间"""
        # 3点
        result = self.parser.parse("3点")
        expected = self.reference.replace(hour=3, minute=0)
        self.assertEqual(result, expected)
        
        # 下午3点
        result = self.parser.parse("下午3点")
        expected = self.reference.replace(hour=15, minute=0)
        self.assertEqual(result, expected)
        
        # 8点半
        result = self.parser.parse("8点半")
        expected = self.reference.replace(hour=8, minute=30)
        self.assertEqual(result, expected)
        
        # 晚上8点
        result = self.parser.parse("晚上8点")
        expected = self.reference.replace(hour=20, minute=0)
        self.assertEqual(result, expected)
    
    def test_combined_expression(self):
        """测试组合表达式"""
        # tomorrow at 3pm
        result = self.parser.parse("tomorrow at 3pm")
        expected = datetime(2026, 4, 17, 15, 0, 0)
        self.assertEqual(result, expected)
        
        # 明天下午3点
        result = self.parser.parse("明天下午3点")
        expected = datetime(2026, 4, 17, 15, 0, 0)
        self.assertEqual(result, expected)
        
        # 下周一早上9点
        result = self.parser.parse("下周一早上9点")
        expected = datetime(2026, 4, 20, 9, 0, 0)
        self.assertEqual(result, expected)
    
    def test_parse_error(self):
        """测试解析错误"""
        with self.assertRaises(ParseError):
            self.parser.parse("")
        
        with self.assertRaises(ParseError):
            self.parser.parse("invalid time expression")
    
    def test_convenience_function(self):
        """测试便捷函数"""
        result = parse_time("in 10 minutes", self.reference)
        expected = self.reference + timedelta(minutes=10)
        self.assertEqual(result, expected)
        
        result = when("明天", self.reference)
        expected = datetime(2026, 4, 17, 0, 0, 0)
        self.assertEqual(result, expected)


class TestDurationParser(unittest.TestCase):
    """测试时长解析器"""
    
    def test_parse_english_duration(self):
        """测试英文时长"""
        # 2h 30m
        result = DurationParser.parse("2h 30m")
        expected = timedelta(hours=2, minutes=30)
        self.assertEqual(result, expected)
        
        # 90 seconds
        result = DurationParser.parse("90 seconds")
        expected = timedelta(seconds=90)
        self.assertEqual(result, expected)
        
        # 1 day
        result = DurationParser.parse("1 day")
        expected = timedelta(days=1)
        self.assertEqual(result, expected)
    
    def test_parse_chinese_duration(self):
        """测试中文时长"""
        # 2小时30分钟
        result = DurationParser.parse("2小时30分钟")
        expected = timedelta(hours=2, minutes=30)
        self.assertEqual(result, expected)
        
        # 90秒
        result = DurationParser.parse("90秒")
        expected = timedelta(seconds=90)
        self.assertEqual(result, expected)
        
        # 半小时
        result = DurationParser.parse("半小时")
        expected = timedelta(minutes=30)
        self.assertEqual(result, expected)
    
    def test_parse_colon_format(self):
        """测试冒号格式"""
        # 1:30:00
        result = DurationParser.parse("1:30:00")
        expected = timedelta(hours=1, minutes=30)
        self.assertEqual(result, expected)
        
        # 2:30
        result = DurationParser.parse("2:30")
        expected = timedelta(hours=2, minutes=30)
        self.assertEqual(result, expected)
    
    def test_format_duration(self):
        """测试时长格式化"""
        # 中文
        duration = timedelta(hours=2, minutes=30, seconds=15)
        result = format_duration(duration, 'cn')
        self.assertIn('2', result)
        self.assertIn('小时', result)
        self.assertIn('30', result)
        self.assertIn('分钟', result)
        
        # 英文
        result = format_duration(duration, 'en')
        self.assertIn('2', result)
        self.assertIn('hour', result)
        self.assertIn('30', result)
        self.assertIn('minute', result)
    
    def test_convenience_function(self):
        """测试便捷函数"""
        result = how_long("1小时")
        expected = timedelta(hours=1)
        self.assertEqual(result, expected)


class TestTimeExpressionExtractor(unittest.TestCase):
    """测试时间表达式提取器"""
    
    def test_extract_english(self):
        """测试英文时间提取"""
        text = "Let's meet tomorrow at 3pm for 2 hours"
        results = extract_times(text)
        
        self.assertTrue(len(results) >= 2)
        
        # 应该提取到 tomorrow
        found_tomorrow = any('tomorrow' in r['match'].lower() for r in results)
        self.assertTrue(found_tomorrow)
    
    def test_extract_chinese(self):
        """测试中文时间提取"""
        text = "明天下午3点开会，预计持续2小时"
        results = extract_times(text)
        
        self.assertTrue(len(results) >= 1)
        
        # 应该提取到时间表达式
        has_time = any('明天' in r['match'] or '下午' in r['match'] or '3点' in r['match'] for r in results)
        self.assertTrue(has_time)


class TestRelativeTimeFormatter(unittest.TestCase):
    """测试相对时间格式化器"""
    
    def test_format_past_time_cn(self):
        """测试过去时间格式化（中文）"""
        now = datetime(2026, 4, 16, 7, 0, 0)
        
        # 刚刚
        result = relative_time(now - timedelta(seconds=5), now, 'cn')
        self.assertEqual(result, "刚刚")
        
        # X分钟前
        result = relative_time(now - timedelta(minutes=30), now, 'cn')
        self.assertIn('30', result)
        self.assertIn('分钟前', result)
        
        # X小时前
        result = relative_time(now - timedelta(hours=3), now, 'cn')
        self.assertIn('3', result)
        self.assertIn('小时前', result)
        
        # 昨天
        result = relative_time(now - timedelta(days=1), now, 'cn')
        self.assertEqual(result, "昨天")
        
        # X天前
        result = relative_time(now - timedelta(days=5), now, 'cn')
        self.assertIn('5', result)
        self.assertIn('天前', result)
    
    def test_format_future_time_cn(self):
        """测试未来时间格式化（中文）"""
        now = datetime(2026, 4, 16, 7, 0, 0)
        
        # X分钟后
        result = relative_time(now + timedelta(minutes=30), now, 'cn')
        self.assertIn('30', result)
        self.assertIn('分钟后', result)
        
        # 明天
        result = relative_time(now + timedelta(days=1), now, 'cn')
        self.assertEqual(result, "明天")
    
    def test_format_past_time_en(self):
        """测试过去时间格式化（英文）"""
        now = datetime(2026, 4, 16, 7, 0, 0)
        
        # just now
        result = relative_time(now - timedelta(seconds=5), now, 'en')
        self.assertEqual(result, "just now")
        
        # X minutes ago
        result = relative_time(now - timedelta(minutes=30), now, 'en')
        self.assertIn('30', result)
        self.assertIn('minutes ago', result)
        
        # yesterday
        result = relative_time(now - timedelta(days=1), now, 'en')
        self.assertEqual(result, "yesterday")


class TestIntegration(unittest.TestCase):
    """集成测试"""
    
    def test_full_workflow(self):
        """测试完整工作流程"""
        reference = datetime(2026, 4, 16, 7, 0, 0)
        
        # 解析时间表达式
        meeting_time = parse_time("明天下午3点", reference)
        self.assertEqual(meeting_time, datetime(2026, 4, 17, 15, 0, 0))
        
        # 解析时长
        duration = parse_duration("2小时")
        self.assertEqual(duration, timedelta(hours=2))
        
        # 计算结束时间
        end_time = meeting_time + duration
        self.assertEqual(end_time, datetime(2026, 4, 17, 17, 0, 0))
        
        # 格式化相对时间
        now = datetime(2026, 4, 16, 10, 0, 0)
        rel_str = relative_time(meeting_time, now, 'cn')
        self.assertIn('明天', rel_str)


if __name__ == '__main__':
    unittest.main()