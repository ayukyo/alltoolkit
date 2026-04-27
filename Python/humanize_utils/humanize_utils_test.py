"""
humanize_utils 测试文件
"""

import sys
import os
import unittest
import time

# Add module directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mod import (
    format_bytes, parse_size,
    format_number, format_percentage, format_with_commas,
    format_duration, format_relative_time, format_time_ago,
    format_list,
    format_phone, format_card_number, format_json, truncate_text, format_ordinal
)


class TestFormatBytes(unittest.TestCase):
    """测试字节格式化"""
    
    def test_zero_bytes(self):
        self.assertEqual(format_bytes(0), "0 B")
    
    def test_bytes(self):
        self.assertEqual(format_bytes(100), "100 B")
        self.assertEqual(format_bytes(999), "999 B")
    
    def test_kilobytes(self):
        self.assertEqual(format_bytes(1000), "1.00 KB")
        self.assertEqual(format_bytes(1500), "1.50 KB")
        self.assertEqual(format_bytes(1024), "1.02 KB")
    
    def test_megabytes(self):
        self.assertEqual(format_bytes(1000000), "1.00 MB")
        self.assertEqual(format_bytes(1500000), "1.50 MB")
    
    def test_gigabytes(self):
        self.assertEqual(format_bytes(1000000000), "1.00 GB")
    
    def test_binary_units(self):
        self.assertEqual(format_bytes(1024, binary=True), "1.00 KiB")
        self.assertEqual(format_bytes(1048576, binary=True), "1.00 MiB")
        self.assertEqual(format_bytes(1073741824, binary=True), "1.00 GiB")
    
    def test_precision(self):
        self.assertEqual(format_bytes(1500, precision=0), "2 KB")
        self.assertEqual(format_bytes(1500, precision=3), "1.500 KB")
    
    def test_no_space(self):
        self.assertEqual(format_bytes(1000, use_space=False), "1.00KB")
    
    def test_negative(self):
        self.assertEqual(format_bytes(-1000), "-1.00 KB")


class TestParseSize(unittest.TestCase):
    """测试大小解析"""
    
    def test_parse_kb(self):
        self.assertEqual(parse_size("1KB"), 1000)
        self.assertEqual(parse_size("2KB"), 2000)
    
    def test_parse_mb(self):
        self.assertEqual(parse_size("1MB"), 1000000)
        self.assertEqual(parse_size("1.5MB"), 1500000)
    
    def test_parse_binary(self):
        self.assertEqual(parse_size("1KiB"), 1024)
        self.assertEqual(parse_size("1MiB"), 1048576)
    
    def test_parse_gb(self):
        self.assertEqual(parse_size("1GB"), 1000000000)
        self.assertEqual(parse_size("2GB"), 2000000000)
    
    def test_parse_bytes(self):
        self.assertEqual(parse_size("100B"), 100)


class TestFormatNumber(unittest.TestCase):
    """测试数字格式化"""
    
    def test_small_numbers(self):
        self.assertEqual(format_number(100), "100")
        self.assertEqual(format_number(999), "999")
    
    def test_thousands(self):
        self.assertEqual(format_number(1000), "1.0K")
        self.assertEqual(format_number(1500), "1.5K")
    
    def test_millions(self):
        self.assertEqual(format_number(1000000), "1.0M")
        self.assertEqual(format_number(1500000), "1.5M")
    
    def test_billions(self):
        self.assertEqual(format_number(1000000000), "1.0B")
        self.assertEqual(format_number(1500000000), "1.5B")
    
    def test_trillions(self):
        self.assertEqual(format_number(1000000000000), "1.0T")
    
    def test_chinese_units(self):
        self.assertEqual(format_number(10000, use_chinese=True), "1.0万")
        self.assertEqual(format_number(15000, use_chinese=True), "1.5万")
        self.assertEqual(format_number(100000000, use_chinese=True), "1.0亿")
        self.assertEqual(format_number(150000000, use_chinese=True), "1.5亿")
    
    def test_precision(self):
        self.assertEqual(format_number(1500, precision=2), "1.50K")
        self.assertEqual(format_number(1500, precision=0), "2K")


class TestFormatPercentage(unittest.TestCase):
    """测试百分比格式化"""
    
    def test_decimal_input(self):
        self.assertEqual(format_percentage(0.5), "50.0%")
        self.assertEqual(format_percentage(0.256, precision=2), "25.60%")
    
    def test_percentage_input(self):
        self.assertEqual(format_percentage(50), "50.0%")
        self.assertEqual(format_percentage(75.5), "75.5%")
    
    def test_show_sign(self):
        self.assertEqual(format_percentage(0.5, show_sign=True), "+50.0%")
        self.assertEqual(format_percentage(-0.5, show_sign=True), "-50.0%")


class TestFormatWithCommas(unittest.TestCase):
    """测试千分位格式化"""
    
    def test_integers(self):
        self.assertEqual(format_with_commas(1000), "1,000")
        self.assertEqual(format_with_commas(1000000), "1,000,000")
        self.assertEqual(format_with_commas(1234567), "1,234,567")
    
    def test_negative(self):
        self.assertEqual(format_with_commas(-1000), "-1,000")
    
    def test_floats(self):
        result = format_with_commas(1234567.891, decimal_places=2)
        self.assertEqual(result, "1,234,567.89")


class TestFormatDuration(unittest.TestCase):
    """测试持续时间格式化"""
    
    def test_full_format(self):
        self.assertEqual(format_duration(3665, format_type="full"), "01:01:05")
        self.assertEqual(format_duration(0, format_type="full"), "00:00:00")
    
    def test_compact_format(self):
        self.assertEqual(format_duration(3665, format_type="compact"), "1h1m5s")
        self.assertEqual(format_duration(3600, format_type="compact"), "1h")
        self.assertEqual(format_duration(3600, format_type="compact", show_zeros=True), "1h0m0s")
        self.assertEqual(format_duration(60, format_type="compact"), "1m")
        self.assertEqual(format_duration(5, format_type="compact"), "5s")
    
    def test_text_format_english(self):
        result = format_duration(3665, format_type="text", use_chinese=False)
        self.assertEqual(result, "1 hour 1 minute 5 seconds")
    
    def test_text_format_chinese(self):
        result = format_duration(3665, format_type="text", use_chinese=True)
        self.assertEqual(result, "1小时1分钟5秒")
    
    def test_negative(self):
        self.assertEqual(format_duration(-3665, format_type="full"), "-01:01:05")


class TestFormatRelativeTime(unittest.TestCase):
    """测试相对时间格式化"""
    
    def test_seconds_ago(self):
        now = time.time()
        result = format_relative_time(now - 30, reference=now, use_chinese=True)
        self.assertEqual(result, "30秒前")
    
    def test_minutes_ago(self):
        now = time.time()
        result = format_relative_time(now - 300, reference=now, use_chinese=True)
        self.assertEqual(result, "5分钟前")
    
    def test_hours_ago(self):
        now = time.time()
        result = format_relative_time(now - 7200, reference=now, use_chinese=True)
        self.assertEqual(result, "2小时前")
    
    def test_days_ago(self):
        now = time.time()
        result = format_relative_time(now - 172800, reference=now, use_chinese=True)
        self.assertEqual(result, "2天前")
    
    def test_future(self):
        now = time.time()
        result = format_relative_time(now + 3600, reference=now, use_chinese=True)
        self.assertEqual(result, "1小时后")
    
    def test_english(self):
        now = time.time()
        result = format_relative_time(now - 3600, reference=now, use_chinese=False)
        self.assertEqual(result, "1 hour ago")


class TestFormatList(unittest.TestCase):
    """测试列表格式化"""
    
    def test_empty(self):
        self.assertEqual(format_list([]), "")
    
    def test_single_item(self):
        self.assertEqual(format_list(["a"]), "a")
    
    def test_two_items_chinese(self):
        self.assertEqual(format_list(["a", "b"]), "a 和 b")
    
    def test_three_items_chinese(self):
        self.assertEqual(format_list(["a", "b", "c"]), "a、b 和 c")
    
    def test_english_format(self):
        self.assertEqual(format_list(["a", "b"], use_chinese=False), "a and b")
        self.assertEqual(format_list(["a", "b", "c"], use_chinese=False), "a, b and c")
    
    def test_with_limit(self):
        result = format_list(["a", "b", "c", "d", "e"], limit=3)
        self.assertEqual(result, "a、b、c 等 5 项")
    
    def test_with_limit_english(self):
        result = format_list(["a", "b", "c", "d"], limit=2, use_chinese=False)
        self.assertEqual(result, "a, b and 4 more")


class TestFormatPhone(unittest.TestCase):
    """测试电话号码格式化"""
    
    def test_standard_format(self):
        self.assertEqual(format_phone("13800000000"), "138 0000 0000")
    
    def test_hyphen_format(self):
        self.assertEqual(format_phone("13800000000", format_type="hyphen"), "138-0000-0000")
    
    def test_international_format(self):
        self.assertEqual(format_phone("13800000000", format_type="international"), "+86 138 0000 0000")
    
    def test_with_country_code(self):
        result = format_phone("8613800000000", format_type="international")
        self.assertEqual(result, "+86 138 0000 0000")


class TestFormatCardNumber(unittest.TestCase):
    """测试银行卡号格式化"""
    
    def test_format(self):
        result = format_card_number("6222021234567890123")
        self.assertEqual(result, "6222 0212 3456 7890 123")
    
    def test_mask(self):
        result = format_card_number("6222021234567890123", mask=True)
        self.assertEqual(result, "6222 **** **** **** 123")


class TestTruncateText(unittest.TestCase):
    """测试文本截断"""
    
    def test_short_text(self):
        text = "短文本"
        self.assertEqual(truncate_text(text, max_length=10), text)
    
    def test_long_text(self):
        text = "这是一段很长的文本需要被截断处理"
        result = truncate_text(text, max_length=10)
        self.assertTrue(len(result) <= 10)
        self.assertTrue(result.endswith("..."))
    
    def test_custom_suffix(self):
        text = "这是一段很长的文本"
        # 使用更短的 max_length 确保截断发生
        result = truncate_text(text, max_length=8, suffix="…")
        self.assertTrue(result.endswith("…"))
        self.assertTrue(len(result) <= 8)
    
    def test_word_boundary(self):
        text = "Hello world this is a test"
        result = truncate_text(text, max_length=15, word_boundary=True)
        self.assertEqual(result, "Hello world...")


class TestFormatOrdinal(unittest.TestCase):
    """测试序数词"""
    
    def test_english(self):
        self.assertEqual(format_ordinal(1), "1st")
        self.assertEqual(format_ordinal(2), "2nd")
        self.assertEqual(format_ordinal(3), "3rd")
        self.assertEqual(format_ordinal(4), "4th")
        self.assertEqual(format_ordinal(11), "11th")
        self.assertEqual(format_ordinal(21), "21st")
        self.assertEqual(format_ordinal(22), "22nd")
        self.assertEqual(format_ordinal(23), "23rd")
    
    def test_chinese(self):
        self.assertEqual(format_ordinal(1, use_chinese=True), "第1")
        self.assertEqual(format_ordinal(100, use_chinese=True), "第100")


class TestFormatJson(unittest.TestCase):
    """测试 JSON 格式化"""
    
    def test_simple_dict(self):
        data = {"name": "张三", "age": 25}
        result = format_json(data)
        self.assertIn('"name"', result)
        self.assertIn('"age"', result)
    
    def test_with_non_ascii(self):
        data = {"name": "张三"}
        result = format_json(data, ensure_ascii=False)
        self.assertIn("张三", result)


# =============================================================================
# 边界值测试（新增）- 2026-04-17
# =============================================================================

class TestFormatBytesEdgeCases(unittest.TestCase):
    """字节格式化边界值测试"""
    
    def test_zero_precision(self):
        """测试精度为 0"""
        self.assertEqual(format_bytes(1500, precision=0), "2 KB")
    
    def test_high_precision(self):
        """测试高精度"""
        self.assertEqual(format_bytes(1500, precision=4), "1.5000 KB")
    
    def test_very_large_size(self):
        """测试极大数值"""
        # TB级别
        result = format_bytes(1000000000000)
        self.assertEqual(result, "1.00 TB")
    
    def test_negative_binary(self):
        """测试负数二进制单位"""
        self.assertEqual(format_bytes(-1024, binary=True), "-1.00 KiB")
    
    def test_float_input(self):
        """测试浮点数输入"""
        result = format_bytes(1024.5)
        self.assertIn("KB", result)


class TestParseSizeEdgeCases(unittest.TestCase):
    """大小解析边界值测试"""
    
    def test_whitespace_handling(self):
        """测试空格处理"""
        self.assertEqual(parse_size("  1KB  "), 1000)
    
    def test_lowercase_units(self):
        """测试小写单位"""
        self.assertEqual(parse_size("1kb"), 1000)
        self.assertEqual(parse_size("1mb"), 1000000)
    
    def test_with_spaces(self):
        """测试带空格的大小字符串"""
        self.assertEqual(parse_size("1 KB"), 1000)
    
    def test_large_units(self):
        """测试大单位"""
        self.assertEqual(parse_size("1TB"), 1000000000000)
        self.assertEqual(parse_size("1PB"), 1000000000000000)
    
    def test_decimal_values(self):
        """测试小数值"""
        self.assertEqual(parse_size("0.5KB"), 500)


class TestFormatNumberEdgeCases(unittest.TestCase):
    """数字格式化边界值测试"""
    
    def test_zero(self):
        """测试零"""
        self.assertEqual(format_number(0), "0")
    
    def test_negative_numbers(self):
        """测试负数"""
        self.assertEqual(format_number(-1000), "-1.0K")
        self.assertEqual(format_number(-1500000), "-1.5M")
    
    def test_chinese_trillion(self):
        """测试中文万亿单位"""
        result = format_number(1000000000000, use_chinese=True)
        self.assertEqual(result, "1.0万亿")
    
    def test_very_large_number(self):
        """测试极大数值"""
        result = format_number(1000000000000000)
        self.assertEqual(result, "1.0Q")


class TestFormatListEdgeCases(unittest.TestCase):
    """列表格式化边界值测试"""
    
    def test_many_items(self):
        """测试大量项"""
        items = [str(i) for i in range(10)]
        result = format_list(items, limit=5)
        self.assertIn("等", result)
    
    def test_custom_limit_text(self):
        """测试自定义限制文本"""
        items = ["a", "b", "c", "d"]
        result = format_list(items, limit=2, limit_text="还有 {remaining} 个")
        self.assertEqual(result, "a、b 还有 2 个")
    
    def test_all_chinese_items(self):
        """测试全中文项"""
        items = ["苹果", "香蕉", "橘子"]
        result = format_list(items)
        self.assertEqual(result, "苹果、香蕉 和 橘子")


class TestTruncateTextEdgeCases(unittest.TestCase):
    """文本截断边界值测试"""
    
    def test_empty_text(self):
        """测试空文本"""
        self.assertEqual(truncate_text("", max_length=10), "")
    
    def test_max_length_equals_text_length(self):
        """测试最大长度等于文本长度"""
        text = "测试文本"
        self.assertEqual(truncate_text(text, max_length=len(text)), text)
    
    def test_max_length_less_than_suffix(self):
        """测试最大长度小于后缀"""
        text = "测试文本"
        result = truncate_text(text, max_length=2, suffix="...")
        self.assertEqual(result, "...")
    
    def test_no_word_boundary_space(self):
        """测试无空格时的单词边界截断"""
        text = "测试文本无空格"
        result = truncate_text(text, max_length=8, word_boundary=True)
        # 无空格时，应该在指定长度截断
        self.assertTrue(len(result) <= 8)
        self.assertTrue("..." in result or len(result) == len(text))


class TestFormatDurationEdgeCases(unittest.TestCase):
    """持续时间边界值测试"""
    
    def test_zero_seconds(self):
        """测试零秒"""
        self.assertEqual(format_duration(0, format_type="compact"), "0s")
        self.assertEqual(format_duration(0, format_type="full"), "00:00:00")
    
    def test_only_seconds(self):
        """测试仅秒"""
        self.assertEqual(format_duration(30, format_type="compact"), "30s")
    
    def test_only_minutes(self):
        """测试仅分钟"""
        self.assertEqual(format_duration(60, format_type="compact"), "1m")
    
    def test_only_hours(self):
        """测试仅小时"""
        self.assertEqual(format_duration(3600, format_type="compact"), "1h")
    
    def test_very_long_duration(self):
        """测试很长持续时间"""
        result = format_duration(100000, format_type="compact")
        self.assertIn("h", result)


if __name__ == "__main__":
    unittest.main(verbosity=2)