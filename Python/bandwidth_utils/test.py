"""
Bandwidth Utils 测试文件

测试所有核心功能。
"""

import unittest
import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    parse_size, parse_bandwidth, parse_time,
    format_time, format_bandwidth, format_size,
    calculate_transfer_time, calculate_required_bandwidth,
    estimate_download_time, compare_bandwidths,
    bandwidth_for_streaming, get_size_info, get_bandwidth_info,
    download_time, upload_time, needed_bandwidth,
    TransferResult, BandwidthInfo, SizeInfo
)


class TestParseSize(unittest.TestCase):
    """测试文件大小解析"""
    
    def test_parse_bytes(self):
        self.assertEqual(parse_size("100"), 100)
        self.assertEqual(parse_size("0"), 0)
    
    def test_parse_kb(self):
        self.assertEqual(parse_size("1 KB"), 1024)
        self.assertEqual(parse_size("2KB"), 2048)
        self.assertEqual(parse_size("1 KiB"), 1024)
    
    def test_parse_mb(self):
        self.assertEqual(parse_size("1 MB"), 1024 * 1024)
        self.assertEqual(parse_size("10 MB"), 10 * 1024 * 1024)
        self.assertEqual(parse_size("1.5 MB"), int(1.5 * 1024 * 1024))
    
    def test_parse_gb(self):
        self.assertEqual(parse_size("1 GB"), 1024 ** 3)
        self.assertEqual(parse_size("2 GB"), 2 * 1024 ** 3)
    
    def test_parse_decimal(self):
        self.assertEqual(parse_size("1.5 GB"), int(1.5 * 1024 ** 3))
        self.assertEqual(parse_size("0.5 MB"), int(0.5 * 1024 ** 2))
    
    def test_parse_with_spaces(self):
        self.assertEqual(parse_size("100 MB"), parse_size("100MB"))
        self.assertEqual(parse_size("1 GB"), parse_size("1GB"))


class TestParseBandwidth(unittest.TestCase):
    """测试带宽解析"""
    
    def test_parse_bps(self):
        self.assertEqual(parse_bandwidth("100 bps"), 100.0)
        self.assertEqual(parse_bandwidth("1000 bps"), 1000.0)
    
    def test_parse_kbps(self):
        self.assertEqual(parse_bandwidth("1 Kbps"), 1000.0)
        self.assertEqual(parse_bandwidth("100 Kbps"), 100000.0)
    
    def test_parse_mbps(self):
        self.assertEqual(parse_bandwidth("1 Mbps"), 1_000_000.0)
        self.assertEqual(parse_bandwidth("100 Mbps"), 100_000_000.0)
    
    def test_parse_gbps(self):
        self.assertEqual(parse_bandwidth("1 Gbps"), 1_000_000_000.0)
        self.assertEqual(parse_bandwidth("10 Gbps"), 10_000_000_000.0)
    
    def test_parse_bytes_per_sec(self):
        # 1 B/s = 8 bps
        self.assertEqual(parse_bandwidth("1 B/s"), 8.0)
        # 1 KB/s = 8000 bps
        self.assertEqual(parse_bandwidth("1 KB/s"), 8000.0)
        # 1 MB/s = 8,000,000 bps
        self.assertEqual(parse_bandwidth("1 MB/s"), 8_000_000.0)
    
    def test_parse_no_space(self):
        self.assertEqual(parse_bandwidth("100Mbps"), 100_000_000.0)
        self.assertEqual(parse_bandwidth("50Kbps"), 50_000.0)
    
    def test_parse_pure_number(self):
        self.assertEqual(parse_bandwidth("100"), 100.0)
        self.assertEqual(parse_bandwidth("1000"), 1000.0)


class TestParseTime(unittest.TestCase):
    """测试时间解析"""
    
    def test_parse_seconds(self):
        self.assertEqual(parse_time("30"), 30.0)
        self.assertEqual(parse_time("30s"), 30.0)
        self.assertEqual(parse_time("30 sec"), 30.0)
    
    def test_parse_minutes(self):
        self.assertEqual(parse_time("1m"), 60.0)
        self.assertEqual(parse_time("5min"), 300.0)
        self.assertEqual(parse_time("2 分钟"), 120.0)
    
    def test_parse_hours(self):
        self.assertEqual(parse_time("1h"), 3600.0)
        self.assertEqual(parse_time("2hr"), 7200.0)
        self.assertEqual(parse_time("1 小时"), 3600.0)
    
    def test_parse_days(self):
        self.assertEqual(parse_time("1d"), 86400.0)
        self.assertEqual(parse_time("2day"), 172800.0)
    
    def test_parse_combined(self):
        self.assertEqual(parse_time("1h30m"), 5400.0)
        self.assertEqual(parse_time("2h15m30s"), 8130.0)
        self.assertEqual(parse_time("1小时30分钟"), 5400.0)


class TestFormatTime(unittest.TestCase):
    """测试时间格式化"""
    
    def test_format_milliseconds(self):
        self.assertIn("ms", format_time(0.5))
    
    def test_format_seconds(self):
        self.assertEqual(format_time(30), "30s")
        self.assertEqual(format_time(45.5), "45.5s")
    
    def test_format_minutes(self):
        self.assertEqual(format_time(60), "1m")
        self.assertEqual(format_time(90), "1m 30s")
    
    def test_format_hours(self):
        self.assertEqual(format_time(3600), "1h")
        self.assertEqual(format_time(3661), "1h 1m 1s")
    
    def test_format_days(self):
        self.assertEqual(format_time(86400), "1d")
        self.assertEqual(format_time(90061), "1d 1h 1m 1s")


class TestFormatBandwidth(unittest.TestCase):
    """测试带宽格式化"""
    
    def test_format_bps(self):
        self.assertEqual(format_bandwidth(100), "100.00 bps")
    
    def test_format_kbps(self):
        self.assertEqual(format_bandwidth(5000), "5.00 Kbps")
    
    def test_format_mbps(self):
        self.assertEqual(format_bandwidth(100_000_000), "100.00 Mbps")
    
    def test_format_gbps(self):
        self.assertEqual(format_bandwidth(1_000_000_000), "1.00 Gbps")
    
    def test_format_bytes_per_sec(self):
        self.assertIn("MB/s", format_bandwidth(100_000_000, 'MB/s'))


class TestFormatSize(unittest.TestCase):
    """测试文件大小格式化"""
    
    def test_format_bytes(self):
        self.assertEqual(format_size(500), "500 B")
    
    def test_format_kb(self):
        self.assertEqual(format_size(1024), "1.00 KB")
        self.assertEqual(format_size(2048), "2.00 KB")
    
    def test_format_mb(self):
        self.assertEqual(format_size(1024 ** 2), "1.00 MB")
        self.assertEqual(format_size(10 * 1024 ** 2), "10.00 MB")
    
    def test_format_gb(self):
        self.assertEqual(format_size(1024 ** 3), "1.00 GB")


class TestCalculateTransferTime(unittest.TestCase):
    """测试传输时间计算"""
    
    def test_basic_calculation(self):
        # 1 MB = 8,388,608 bits
        # 1 Mbps = 1,000,000 bps
        # Time = 8,388,608 / 1,000,000 = 8.388608 seconds
        result = calculate_transfer_time(1024 * 1024, 1_000_000)
        self.assertAlmostEqual(result.time_seconds, 8.388608, places=2)
    
    def test_with_string_inputs(self):
        result = calculate_transfer_time("1 GB", "100 Mbps")
        self.assertGreater(result.time_seconds, 0)
        self.assertIn("s", result.time_formatted)
    
    def test_with_overhead(self):
        # 无开销
        result1 = calculate_transfer_time("100 MB", "10 Mbps", 0)
        # 5% 开销
        result2 = calculate_transfer_time("100 MB", "10 Mbps", 5)
        # 有开销的应该更慢
        self.assertGreater(result2.time_seconds, result1.time_seconds)
    
    def test_result_types(self):
        result = calculate_transfer_time("1 MB", "1 Mbps")
        self.assertIsInstance(result.time_seconds, float)
        self.assertIsInstance(result.time_formatted, str)


class TestCalculateRequiredBandwidth(unittest.TestCase):
    """测试所需带宽计算"""
    
    def test_basic_calculation(self):
        # 1 GB in 1 hour
        # 1 GB = 8,589,934,592 bits
        # 1 hour = 3600 seconds
        # Required = 8,589,934,592 / 3600 ≈ 2.38 Mbps
        info = calculate_required_bandwidth(1024 ** 3, 3600)
        self.assertAlmostEqual(info.Mbps, 2.38, places=1)
    
    def test_with_string_inputs(self):
        info = calculate_required_bandwidth("1 GB", "1h")
        self.assertGreater(info.Mbps, 0)
    
    def test_info_fields(self):
        info = calculate_required_bandwidth("1 GB", "1h")
        self.assertGreater(info.bps, 0)
        self.assertGreater(info.Kbps, 0)
        self.assertGreater(info.Mbps, 0)
        self.assertGreater(info.Gbps, 0)
        self.assertGreater(info.Bps, 0)
        self.assertGreater(info.KBps, 0)
        self.assertGreater(info.MBps, 0)


class TestEstimateDownloadTime(unittest.TestCase):
    """测试下载时间估算"""
    
    def test_returns_dict(self):
        result = estimate_download_time("1 GB", "100 Mbps")
        self.assertIsInstance(result, dict)
        self.assertIn('time_seconds', result)
        self.assertIn('time_formatted', result)
        self.assertIn('file_size_bytes', result)
        self.assertIn('bandwidth_bps', result)


class TestCompareBandwidths(unittest.TestCase):
    """测试带宽比较"""
    
    def test_compare(self):
        result = compare_bandwidths("100 Mbps", "50 Mbps", "1 Gbps")
        self.assertEqual(result['fastest'], "1 Gbps")
        self.assertEqual(result['slowest'], "50 Mbps")
    
    def test_ratio(self):
        result = compare_bandwidths("100 Mbps", "10 Mbps")
        self.assertAlmostEqual(result['ratio_fastest_to_slowest'], 10.0)
    
    def test_with_numbers(self):
        result = compare_bandwidths(100_000_000, 50_000_000)
        self.assertEqual(result['fastest_bps'], 100_000_000)


class TestBandwidthForStreaming(unittest.TestCase):
    """测试流媒体带宽建议"""
    
    def test_1080p_h264(self):
        info = bandwidth_for_streaming('1080p', 30, 'h264')
        self.assertGreater(info['recommended_bandwidth_mbps'], 0)
    
    def test_4k_av1(self):
        info = bandwidth_for_streaming('4k', 60, 'av1')
        self.assertGreater(info['recommended_bandwidth_mbps'], 0)
    
    def test_codec_efficiency(self):
        # H.265 should be more efficient than H.264
        h264 = bandwidth_for_streaming('1080p', 30, 'h264')
        h265 = bandwidth_for_streaming('1080p', 30, 'h265')
        self.assertLess(h265['estimated_bitrate_mbps'], h264['estimated_bitrate_mbps'])
    
    def test_fps_scaling(self):
        # Higher FPS should require more bandwidth
        low_fps = bandwidth_for_streaming('1080p', 30, 'h264')
        high_fps = bandwidth_for_streaming('1080p', 60, 'h264')
        self.assertLess(low_fps['estimated_bitrate_mbps'], high_fps['estimated_bitrate_mbps'])
    
    def test_invalid_resolution(self):
        with self.assertRaises(ValueError):
            bandwidth_for_streaming('invalid', 30, 'h264')


class TestConvenienceFunctions(unittest.TestCase):
    """测试便捷函数"""
    
    def test_download_time(self):
        result = download_time("1 GB", "100 Mbps")
        self.assertIsInstance(result, str)
        self.assertIn("m", result)
    
    def test_upload_time(self):
        result = upload_time("100 MB", "10 Mbps")
        self.assertIsInstance(result, str)
    
    def test_needed_bandwidth(self):
        result = needed_bandwidth("1 GB", "1h")
        self.assertIsInstance(result, str)
        self.assertIn("Mbps", result)


class TestDataClasses(unittest.TestCase):
    """测试数据类"""
    
    def test_transfer_result(self):
        result = TransferResult(
            time_seconds=60.0,
            time_formatted="1m",
            average_speed_bps=1_000_000,
            average_speed_formatted="1.00 Mbps"
        )
        self.assertEqual(result.time_seconds, 60.0)
        self.assertIn("1m", str(result))
    
    def test_bandwidth_info(self):
        info = BandwidthInfo(
            bps=100_000_000,
            Kbps=100_000,
            Mbps=100.0,
            Gbps=0.1,
            Bps=12_500_000,
            KBps=12_500,
            MBps=12.5
        )
        self.assertEqual(info.Mbps, 100.0)
        self.assertIn("100.00 Mbps", info.format_auto())
    
    def test_size_info(self):
        info = SizeInfo(
            bytes=1024**3,
            KB=1024**2,
            MB=1024,
            GB=1.0,
            TB=1/1024
        )
        self.assertEqual(info.GB, 1.0)


class TestEdgeCases(unittest.TestCase):
    """测试边界情况"""
    
    def test_zero_bandwidth(self):
        with self.assertRaises(ValueError):
            calculate_transfer_time("1 GB", 0)
        
        with self.assertRaises(ValueError):
            calculate_transfer_time("1 GB", -10)
    
    def test_zero_time(self):
        with self.assertRaises(ValueError):
            calculate_required_bandwidth("1 GB", 0)
    
    def test_very_small_values(self):
        result = calculate_transfer_time(1, 1_000_000)  # 1 byte, 1 Mbps
        self.assertGreater(result.time_seconds, 0)
    
    def test_very_large_values(self):
        result = calculate_transfer_time("1 PB", "100 Gbps")
        self.assertGreater(result.time_seconds, 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)