"""
Storage Unit Utils - 单元测试

运行: python -m pytest storage_unit_utils/test.py -v
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from storage_unit_utils.mod import (
    StorageUnit, UnitSystem,
    convert, to_bytes, from_bytes,
    format_size, format_bits, smart_format,
    parse_size, parse_to_bytes,
    ratio, percentage, progress_bar,
    compare, add, subtract,
    human_readable, find_largest_unit, find_smallest_unit,
    total_size, speed_format, bandwidth_format, estimate_time,
    kb, mb, gb, tb, kib, mib, gib, tib,
    DECIMAL_UNITS, BINARY_UNITS, UNIT_MAP
)

import unittest


class TestStorageUnitEnum(unittest.TestCase):
    """StorageUnit 枚举测试"""
    
    def test_decimal_units(self):
        """测试十进制单位"""
        self.assertEqual(StorageUnit.KILOBYTE.value[0], "KB")
        self.assertEqual(StorageUnit.MEGABYTE.value[0], "MB")
        self.assertEqual(StorageUnit.GIGABYTE.value[0], "GB")
        self.assertEqual(StorageUnit.TERABYTE.value[0], "TB")
    
    def test_binary_units(self):
        """测试二进制单位"""
        self.assertEqual(StorageUnit.KIBIBYTE.value[0], "KiB")
        self.assertEqual(StorageUnit.MEBIBYTE.value[0], "MiB")
        self.assertEqual(StorageUnit.GIBIBYTE.value[0], "GiB")
        self.assertEqual(StorageUnit.TEBIBYTE.value[0], "TiB")
    
    def test_unit_system(self):
        """测试单位系统"""
        self.assertEqual(StorageUnit.KILOBYTE.value[1], UnitSystem.DECIMAL)
        self.assertEqual(StorageUnit.KIBIBYTE.value[1], UnitSystem.BINARY)


class TestConvert(unittest.TestCase):
    """转换函数测试"""
    
    def test_convert_decimal(self):
        """测试十进制转换"""
        self.assertAlmostEqual(convert(1, "KB", "B"), 1000.0)
        self.assertAlmostEqual(convert(1, "MB", "KB"), 1000.0)
        self.assertAlmostEqual(convert(1, "GB", "MB"), 1000.0)
        self.assertAlmostEqual(convert(1024, "MB", "GB"), 1.024)
    
    def test_convert_binary(self):
        """测试二进制转换"""
        self.assertAlmostEqual(convert(1, "KiB", "B"), 1024.0)
        self.assertAlmostEqual(convert(1, "MiB", "KiB"), 1024.0)
        self.assertAlmostEqual(convert(1, "GiB", "MiB"), 1024.0)
        self.assertAlmostEqual(convert(1024, "MiB", "GiB"), 1.0)
    
    def test_convert_bits(self):
        """测试比特转换"""
        self.assertAlmostEqual(convert(8, "bit", "B"), 1.0)
        self.assertAlmostEqual(convert(1, "B", "bit"), 8.0)
        self.assertAlmostEqual(convert(8000, "bit", "KB"), 1.0)
    
    def test_convert_same_unit(self):
        """测试相同单位转换"""
        self.assertEqual(convert(100, "KB", "KB"), 100.0)
        self.assertEqual(convert(100, "GiB", "GiB"), 100.0)
    
    def test_convert_zero(self):
        """测试零值转换"""
        self.assertEqual(convert(0, "GB", "MB"), 0.0)
        self.assertEqual(convert(0, "GiB", "MiB"), 0.0)
    
    def test_convert_with_storage_unit(self):
        """测试使用 StorageUnit 枚举转换"""
        self.assertAlmostEqual(convert(1, StorageUnit.GIGABYTE, StorageUnit.MEGABYTE), 1000.0)
        self.assertAlmostEqual(convert(1, StorageUnit.GIBIBYTE, StorageUnit.MEBIBYTE), 1024.0)
    
    def test_convert_invalid_unit(self):
        """测试无效单位"""
        with self.assertRaises(ValueError):
            convert(1, "invalid", "MB")
        with self.assertRaises(ValueError):
            convert(1, "MB", "invalid")
    
    def test_convert_large_values(self):
        """测试大值转换"""
        self.assertAlmostEqual(convert(1, "TB", "B"), 1_000_000_000_000.0)
        self.assertAlmostEqual(convert(1, "PB", "TB"), 1000.0)
        self.assertAlmostEqual(convert(1, "TiB", "B"), 1_099_511_627_776.0)


class TestToFromBytes(unittest.TestCase):
    """to_bytes 和 from_bytes 测试"""
    
    def test_to_bytes_decimal(self):
        """测试十进制转字节"""
        self.assertEqual(to_bytes(1, "KB"), 1000)
        self.assertEqual(to_bytes(1, "MB"), 1_000_000)
        self.assertEqual(to_bytes(1, "GB"), 1_000_000_000)
        self.assertEqual(to_bytes(1, "TB"), 1_000_000_000_000)
    
    def test_to_bytes_binary(self):
        """测试二进制转字节"""
        self.assertEqual(to_bytes(1, "KiB"), 1024)
        self.assertEqual(to_bytes(1, "MiB"), 1_048_576)
        self.assertEqual(to_bytes(1, "GiB"), 1_073_741_824)
    
    def test_from_bytes_decimal(self):
        """测试字节转十进制"""
        self.assertAlmostEqual(from_bytes(1000, "KB"), 1.0)
        self.assertAlmostEqual(from_bytes(1_000_000, "MB"), 1.0)
        self.assertAlmostEqual(from_bytes(1_000_000_000, "GB"), 1.0)
    
    def test_from_bytes_binary(self):
        """测试字节转二进制"""
        self.assertAlmostEqual(from_bytes(1024, "KiB"), 1.0)
        self.assertAlmostEqual(from_bytes(1_048_576, "MiB"), 1.0)
        self.assertAlmostEqual(from_bytes(1_073_741_824, "GiB"), 1.0)
    
    def test_roundtrip(self):
        """测试往返转换"""
        original = 1024
        bytes_val = to_bytes(original, "KiB")
        result = from_bytes(bytes_val, "KiB")
        self.assertEqual(original, result)


class TestFormatSize(unittest.TestCase):
    """format_size 测试"""
    
    def test_format_zero(self):
        """测试零值格式化"""
        self.assertEqual(format_size(0), "0 B")
        self.assertEqual(format_size(0, binary=True), "0 B")
    
    def test_format_bytes(self):
        """测试字节格式化"""
        result = format_size(100)
        self.assertIn("B", result)
        result = format_size(999)
        self.assertIn("B", result)
    
    def test_format_decimal(self):
        """测试十进制格式化"""
        self.assertIn("KB", format_size(1000))
        self.assertIn("MB", format_size(1_000_000))
        self.assertIn("GB", format_size(1_000_000_000))
        self.assertIn("TB", format_size(1_000_000_000_000))
    
    def test_format_binary(self):
        """测试二进制格式化"""
        self.assertIn("KiB", format_size(1024, binary=True))
        self.assertIn("MiB", format_size(1_048_576, binary=True))
        self.assertIn("GiB", format_size(1_073_741_824, binary=True))
    
    def test_format_precision(self):
        """测试精度"""
        result = format_size(1000, precision=0)  # 1 KB
        self.assertIn("1", result)
        result = format_size(1500, precision=4)  # 1.5 KB
        self.assertIn("1.5", result)
    
    def test_format_separator(self):
        """测试分隔符"""
        self.assertIn("-", format_size(1024, separator="-"))
        self.assertIn("", format_size(1024, separator=""))


class TestFormatBits(unittest.TestCase):
    """format_bits 测试"""
    
    def test_format_bits_zero(self):
        """测试零值"""
        self.assertEqual(format_bits(0), "0 bit")
    
    def test_format_bits_small(self):
        """测试小值"""
        self.assertIn("bit", format_bits(100))
    
    def test_format_bits_large(self):
        """测试大值"""
        self.assertIn("Kbit", format_bits(1000))
        self.assertIn("Mbit", format_bits(1_000_000))
        self.assertIn("Gbit", format_bits(1_000_000_000))


class TestParseSize(unittest.TestCase):
    """parse_size 测试"""
    
    def test_parse_simple(self):
        """测试简单解析"""
        value, unit = parse_size("1GB")
        self.assertEqual(value, 1.0)
        self.assertEqual(unit, StorageUnit.GIGABYTE)
    
    def test_parse_with_space(self):
        """测试带空格解析"""
        value, unit = parse_size("1.5 KiB")
        self.assertEqual(value, 1.5)
        self.assertEqual(unit, StorageUnit.KIBIBYTE)
    
    def test_parse_no_unit(self):
        """测试无单位解析"""
        value, unit = parse_size("1024")
        self.assertEqual(value, 1024.0)
        self.assertEqual(unit, StorageUnit.BYTE)
    
    def test_parse_decimal_value(self):
        """测试小数值"""
        value, unit = parse_size("1.5GB")
        self.assertEqual(value, 1.5)
        self.assertEqual(unit, StorageUnit.GIGABYTE)
    
    def test_parse_invalid(self):
        """测试无效输入"""
        with self.assertRaises(ValueError):
            parse_size("invalid")
    
    def test_parse_to_bytes(self):
        """测试解析为字节"""
        self.assertEqual(parse_to_bytes("1KB"), 1000)
        self.assertEqual(parse_to_bytes("1KiB"), 1024)
        self.assertEqual(parse_to_bytes("1.5GB"), 1_500_000_000)
    
    def test_parse_case_insensitive(self):
        """测试大小写不敏感"""
        value1, _ = parse_size("1gb")
        value2, _ = parse_size("1GB")
        self.assertEqual(value1, value2)


class TestRatioPercentage(unittest.TestCase):
    """ratio 和 percentage 测试"""
    
    def test_ratio_basic(self):
        """测试基本比例"""
        self.assertEqual(ratio(500, 1000), 0.5)
        self.assertEqual(ratio(250, 1000), 0.25)
        self.assertEqual(ratio(100, 100), 1.0)
    
    def test_ratio_zero_total(self):
        """测试零总值"""
        self.assertEqual(ratio(100, 0), 0.0)
    
    def test_ratio_bounds(self):
        """测试边界"""
        self.assertEqual(ratio(150, 100), 1.0)  # 超过 100%
        self.assertEqual(ratio(-50, 100), 0.0)  # 负值
    
    def test_percentage_basic(self):
        """测试百分比"""
        self.assertEqual(percentage(500, 1000), "50.0%")
        self.assertEqual(percentage(250, 1000), "25.0%")
    
    def test_percentage_precision(self):
        """测试精度"""
        result = percentage(333, 1000, precision=2)
        self.assertIn("33.3", result)  # 可以是 33.3% 或 33.30%
        self.assertEqual(percentage(333, 1000, precision=0), "33%")


class TestProgressBar(unittest.TestCase):
    """progress_bar 测试"""
    
    def test_progress_basic(self):
        """测试基本进度条"""
        result = progress_bar(500, 1000, width=10)
        self.assertIn("50.0%", result)
    
    def test_progress_zero(self):
        """测试零进度"""
        result = progress_bar(0, 1000, width=10)
        self.assertIn("0.0%", result)
    
    def test_progress_full(self):
        """测试满进度"""
        result = progress_bar(1000, 1000, width=10)
        self.assertIn("100.0%", result)
    
    def test_progress_custom_chars(self):
        """测试自定义字符"""
        result = progress_bar(500, 1000, width=10, filled="#", empty="-")
        self.assertIn("#", result)
        self.assertIn("-", result)
    
    def test_progress_binary(self):
        """测试二进制单位"""
        result = progress_bar(512, 1024, binary=True)
        self.assertIn("KiB", result)


class TestCompare(unittest.TestCase):
    """compare 测试"""
    
    def test_compare_greater(self):
        """测试大于"""
        self.assertEqual(compare("1GB", "500MB"), 1)
        self.assertEqual(compare("2TB", "1TB"), 1)
    
    def test_compare_less(self):
        """测试小于"""
        self.assertEqual(compare("500MB", "1GB"), -1)
        self.assertEqual(compare("1KB", "1MB"), -1)
    
    def test_compare_equal(self):
        """测试等于"""
        self.assertEqual(compare("1000MB", "1GB"), 0)
        self.assertEqual(compare("1KiB", "1024B"), 0)
    
    def test_compare_with_units(self):
        """测试带单位比较"""
        self.assertEqual(compare(1000, 1, "MB", "GB"), 0)  # 1000MB = 1GB
        self.assertEqual(compare(2, 1, "GB", "GB"), 1)  # 2GB > 1GB


class TestAddSubtract(unittest.TestCase):
    """add 和 subtract 测试"""
    
    def test_add_basic(self):
        """测试基本加法"""
        self.assertEqual(add("1GB", "500MB"), 1_500_000_000)
        self.assertEqual(add("1KiB", "1KiB"), 2048)
    
    def test_add_multiple(self):
        """测试多值加法"""
        result = add("1GB", "500MB", "100MB")
        self.assertEqual(result, 1_600_000_000)
    
    def test_add_with_unit(self):
        """测试带单位返回"""
        result = add("1GB", "500MB", unit="MB")
        self.assertAlmostEqual(result, 1500.0)
    
    def test_subtract_basic(self):
        """测试基本减法"""
        result = subtract("2GB", "500MB")
        self.assertEqual(result, 1_500_000_000)
    
    def test_subtract_with_unit(self):
        """测试带单位返回"""
        result = subtract("2GB", "500MB", unit="MB")
        self.assertAlmostEqual(result, 1500.0)


class TestHumanReadable(unittest.TestCase):
    """human_readable 测试"""
    
    def test_short_style(self):
        """测试短格式"""
        result = human_readable(1500000000, style="short")
        self.assertIn("GB", result)
    
    def test_long_style(self):
        """测试长格式"""
        result = human_readable(1500000000, style="long")
        self.assertIn("Gigabytes", result)
    
    def test_binary_long(self):
        """测试二进制长格式"""
        result = human_readable(1024, binary=True, style="long")
        self.assertIn("Kibibyte", result)
    
    def test_zero(self):
        """测试零值"""
        self.assertEqual(human_readable(0), "0 B")
        self.assertEqual(human_readable(0, style="long"), "0 Bytes")
    
    def test_singular(self):
        """测试单数形式"""
        result = human_readable(1, style="long")
        self.assertIn("Byte", result)


class TestFindExtremes(unittest.TestCase):
    """find_largest_unit 和 find_smallest_unit 测试"""
    
    def test_find_largest(self):
        """测试找最大"""
        orig, bytes_val = find_largest_unit(["1GB", "500MB", "2TB"])
        self.assertEqual(orig, "2TB")
        self.assertEqual(bytes_val, 2_000_000_000_000)
    
    def test_find_smallest(self):
        """测试找最小"""
        orig, bytes_val = find_smallest_unit(["1GB", "500MB", "2TB"])
        self.assertEqual(orig, "500MB")
        self.assertEqual(bytes_val, 500_000_000)
    
    def test_empty_list(self):
        """测试空列表"""
        with self.assertRaises(ValueError):
            find_largest_unit([])
        with self.assertRaises(ValueError):
            find_smallest_unit([])


class TestTotalSize(unittest.TestCase):
    """total_size 测试"""
    
    def test_total_basic(self):
        """测试基本总计"""
        result = total_size("1GB", "500MB", "100MB")
        self.assertIn("GB", result)
    
    def test_total_with_unit(self):
        """测试指定单位"""
        result = total_size("1GB", "500MB", unit="MB")
        self.assertIn("MB", result)
        self.assertIn("1500", result)


class TestSpeedFormat(unittest.TestCase):
    """speed_format 测试"""
    
    def test_speed_format_basic(self):
        """测试基本速度格式化"""
        self.assertIn("KB/s", speed_format(1024))
        self.assertIn("MB/s", speed_format(1024 * 1024))
    
    def test_speed_format_binary(self):
        """测试二进制速度"""
        result = speed_format(1024, binary=True)
        self.assertIn("KiB/s", result)


class TestBandwidthFormat(unittest.TestCase):
    """bandwidth_format 测试"""
    
    def test_bandwidth_basic(self):
        """测试基本带宽格式化"""
        self.assertEqual(bandwidth_format(0), "0 bps")
        self.assertIn("Kbps", bandwidth_format(1000))
        self.assertIn("Mbps", bandwidth_format(1_000_000))
        self.assertIn("Gbps", bandwidth_format(1_000_000_000))


class TestEstimateTime(unittest.TestCase):
    """estimate_time 测试"""
    
    def test_estimate_seconds(self):
        """测试秒级估算"""
        result = estimate_time(1024, 1024)
        self.assertEqual(result, "1s")
    
    def test_estimate_minutes(self):
        """测试分钟级估算"""
        result = estimate_time(1024 * 120, 1024)  # 2 minutes
        self.assertEqual(result, "2m")
    
    def test_estimate_hours(self):
        """测试小时级估算"""
        result = estimate_time(1024 * 3600, 1024)  # 1 hour
        self.assertEqual(result, "1h")
    
    def test_estimate_days(self):
        """测试天级估算"""
        result = estimate_time(1024 * 86400, 1024)  # 1 day
        self.assertEqual(result, "1d")
    
    def test_estimate_infinite(self):
        """测试零速度"""
        result = estimate_time(1024, 0)
        self.assertEqual(result, "∞")


class TestConvenienceFunctions(unittest.TestCase):
    """便捷函数测试"""
    
    def test_kb(self):
        """测试 KB 函数"""
        self.assertEqual(kb(1), 1000)
        self.assertEqual(kb(2), 2000)
    
    def test_mb(self):
        """测试 MB 函数"""
        self.assertEqual(mb(1), 1_000_000)
        self.assertEqual(mb(2), 2_000_000)
    
    def test_gb(self):
        """测试 GB 函数"""
        self.assertEqual(gb(1), 1_000_000_000)
        self.assertEqual(gb(2), 2_000_000_000)
    
    def test_tb(self):
        """测试 TB 函数"""
        self.assertEqual(tb(1), 1_000_000_000_000)
    
    def test_kib(self):
        """测试 KiB 函数"""
        self.assertEqual(kib(1), 1024)
        self.assertEqual(kib(2), 2048)
    
    def test_mib(self):
        """测试 MiB 函数"""
        self.assertEqual(mib(1), 1_048_576)
    
    def test_gib(self):
        """测试 GiB 函数"""
        self.assertEqual(gib(1), 1_073_741_824)
    
    def test_tib(self):
        """测试 TiB 函数"""
        self.assertEqual(tib(1), 1_099_511_627_776)


class TestEdgeCases(unittest.TestCase):
    """边界情况测试"""
    
    def test_very_large_values(self):
        """测试极大值"""
        result = format_size(1e18)
        self.assertIn("EB", result)
    
    def test_negative_values(self):
        """测试负值"""
        result = format_size(-1024)
        self.assertIn("-", result)
    
    def test_float_precision(self):
        """测试浮点精度"""
        result = convert(1.5, "GB", "MB")
        self.assertAlmostEqual(result, 1500.0)
    
    def test_comma_in_input(self):
        """测试带逗号的输入"""
        value, _ = parse_size("1,000")
        self.assertEqual(value, 1000.0)


class TestUnitMap(unittest.TestCase):
    """单位映射测试"""
    
    def test_all_units_mapped(self):
        """测试所有单位都有映射"""
        for unit in StorageUnit:
            self.assertIn(unit.value[0], UNIT_MAP)


if __name__ == "__main__":
    unittest.main(verbosity=2)