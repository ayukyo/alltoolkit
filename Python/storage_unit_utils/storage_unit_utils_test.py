#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for storage_unit_utils"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    convert, to_bytes, from_bytes, format_size, format_bits,
    parse_size, parse_to_bytes, smart_format, ratio, percentage,
    progress_bar, compare, add, subtract, human_readable,
    find_largest_unit, find_smallest_unit, total_size,
    speed_format, bandwidth_format, estimate_time,
    kb, mb, gb, tb, kib, mib, gib, tib,
    StorageUnit, UnitSystem
)

import unittest


class TestConvert(unittest.TestCase):
    def test_convert_kb_to_mb(self):
        self.assertAlmostEqual(convert(1024, "KB", "MB"), 1.024, places=3)

    def test_convert_gb_to_mb(self):
        self.assertAlmostEqual(convert(1, "GB", "MB"), 1000, places=3)

    def test_convert_kib_to_mib(self):
        self.assertAlmostEqual(convert(1024, "KiB", "MiB"), 1.0, places=3)

    def test_convert_bit_to_byte(self):
        self.assertEqual(convert(8, "bit", "B"), 1.0)

    def test_convert_invalid_unit_raises(self):
        with self.assertRaises(ValueError):
            convert(1, "invalid", "GB")


class TestToBytes(unittest.TestCase):
    def test_kb_to_bytes(self):
        self.assertEqual(to_bytes(1, "KB"), 1000)

    def test_kib_to_bytes(self):
        self.assertEqual(to_bytes(1, "KiB"), 1024)

    def test_gb_to_bytes(self):
        self.assertEqual(to_bytes(1.5, "GB"), 1500000000)


class TestFromBytes(unittest.TestCase):
    def test_bytes_to_kb(self):
        self.assertAlmostEqual(from_bytes(1024, "KB"), 1.024, places=3)

    def test_bytes_to_kib(self):
        self.assertEqual(from_bytes(1024, "KiB"), 1.0)


class TestFormatSize(unittest.TestCase):
    def test_format_zero(self):
        self.assertEqual(format_size(0), "0 B")

    def test_format_bytes(self):
        self.assertEqual(format_size(500), "500.00 B")

    def test_format_kb(self):
        self.assertEqual(format_size(1024), "1.02 KB")

    def test_format_binary(self):
        self.assertEqual(format_size(1024, binary=True), "1.00 KiB")

    def test_format_gb(self):
        self.assertIn("GB", format_size(1500000000))


class TestParseSize(unittest.TestCase):
    def test_parse_gb(self):
        value, unit = parse_size("1GB")
        self.assertEqual(value, 1.0)
        self.assertEqual(unit, StorageUnit.GIGABYTE)

    def test_parse_with_space(self):
        value, unit = parse_size("1.5 KiB")
        self.assertEqual(value, 1.5)
        self.assertEqual(unit, StorageUnit.KIBIBYTE)

    def test_parse_no_unit(self):
        value, unit = parse_size("1024")
        self.assertEqual(value, 1024.0)
        self.assertEqual(unit, StorageUnit.BYTE)

    def test_parse_invalid(self):
        with self.assertRaises(ValueError):
            parse_size("invalid")


class TestSmartFormat(unittest.TestCase):
    def test_small_value(self):
        self.assertEqual(smart_format(500), "500.00 B")

    def test_large_value(self):
        result = smart_format(1500000000)
        self.assertIn("GB", result)


class TestRatio(unittest.TestCase):
    def test_ratio_normal(self):
        self.assertEqual(ratio(500, 1000), 0.5)

    def test_ratio_zero_total(self):
        self.assertEqual(ratio(500, 0), 0.0)

    def test_ratio_overflow(self):
        self.assertEqual(ratio(2000, 1000), 1.0)


class TestPercentage(unittest.TestCase):
    def test_percentage_normal(self):
        self.assertEqual(percentage(500, 1000), "50.0%")

    def test_percentage_precision(self):
        self.assertEqual(percentage(256, 1024, precision=2), "25.00%")


class TestProgressBar(unittest.TestCase):
    def test_progress_bar_half(self):
        result = progress_bar(500, 1000, width=10)
        self.assertIn("50.0%", result)

    def test_progress_bar_binary(self):
        result = progress_bar(512, 1024, binary=True, width=10)
        self.assertIn("50.0%", result)


class TestCompare(unittest.TestCase):
    def test_compare_gb_vs_mb(self):
        self.assertEqual(compare("1GB", "500MB"), 1)

    def test_compare_equal(self):
        # 1024 KiB = 1 MiB
        self.assertEqual(compare(1024, 1, "KiB", "MiB"), 0)

    def test_compare_less(self):
        self.assertEqual(compare("500MB", "1GB"), -1)


class TestAddSubtract(unittest.TestCase):
    def test_add_sizes(self):
        self.assertEqual(add("1GB", "500MB"), 1500000000)

    def test_add_with_unit(self):
        result = add("1GB", "500MB", unit="MB")
        self.assertAlmostEqual(result, 1500.0, places=1)

    def test_subtract_sizes(self):
        self.assertEqual(subtract("2GB", "500MB"), 1500000000)


class TestHumanReadable(unittest.TestCase):
    def test_short_style(self):
        self.assertEqual(human_readable(1500000000, style="short"), "1.50 GB")

    def test_long_style(self):
        self.assertIn("Gigabyte", human_readable(1500000000, style="long"))


class TestFindLargestSmallest(unittest.TestCase):
    def test_find_largest(self):
        result, bytes_val = find_largest_unit(["1GB", "500MB", "2TB"])
        self.assertEqual(result, "2TB")

    def test_find_smallest(self):
        result, bytes_val = find_smallest_unit(["1GB", "500MB", "2TB"])
        self.assertEqual(result, "500MB")


class TestTotalSize(unittest.TestCase):
    def test_total_size(self):
        result = total_size("1GB", "500MB", "100MB")
        self.assertIn("GB", result)


class TestSpeedFormat(unittest.TestCase):
    def test_speed_format(self):
        result = speed_format(1024 * 1024)
        self.assertTrue("MB/s" in result or "MiB/s" in result)


class TestBandwidthFormat(unittest.TestCase):
    def test_bandwidth_mbps(self):
        result = bandwidth_format(1000000)
        self.assertIn("Mbps", result)

    def test_bandwidth_gbps(self):
        result = bandwidth_format(1000000000)
        self.assertIn("Gbps", result)


class TestEstimateTime(unittest.TestCase):
    def test_estimate_time_minutes(self):
        result = estimate_time(1024 * 1024 * 100, 1024 * 1024)
        self.assertIn("m", result)

    def test_estimate_time_infinity(self):
        self.assertEqual(estimate_time(100, 0), "∞")


class TestConvenienceFunctions(unittest.TestCase):
    def test_kb(self):
        self.assertEqual(kb(1), 1000)

    def test_mb(self):
        self.assertEqual(mb(1), 1000000)

    def test_gb(self):
        self.assertEqual(gb(1), 1000000000)

    def test_kib(self):
        self.assertEqual(kib(1), 1024)

    def test_mib(self):
        self.assertEqual(mib(1), 1048576)

    def test_gib(self):
        self.assertEqual(gib(1), 1073741824)


if __name__ == "__main__":
    unittest.main()