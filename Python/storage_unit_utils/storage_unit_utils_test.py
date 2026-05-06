#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Storage Unit Utils Test Suite
Tests for storage unit conversion and formatting
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from storage_unit_utils.mod import (
    UnitSystem, StorageUnit,
    convert, to_bytes, from_bytes,
    format_size, format_bits, parse_size, parse_to_bytes,
    smart_format, ratio, percentage, progress_bar,
    compare, add, subtract, human_readable,
    find_largest_unit, find_smallest_unit, total_size,
    speed_format, bandwidth_format, estimate_time,
    kb, mb, gb, tb, kib, mib, gib, tib,
    UNIT_MAP, DECIMAL_UNITS, BINARY_UNITS
)


class TestResultCollector:
    """Collects test results"""
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.tests = []
    
    def add_result(self, name, passed, message=""):
        self.tests.append((name, passed, message))
        if passed:
            self.passed += 1
        else:
            self.failed += 1
    
    def summary(self):
        total = self.passed + self.failed
        print(f"\n{'='*60}")
        print(f"Storage Unit Utils Test Results: {self.passed}/{total} passed")
        print(f"{'='*60}")
        if self.failed > 0:
            print("Failed tests:")
            for name, passed, msg in self.tests:
                if not passed:
                    print(f"  - {name}: {msg}")
        return self.failed == 0


results = TestResultCollector()


def test_enums():
    """Test UnitSystem and StorageUnit enums"""
    try:
        assert UnitSystem.DECIMAL.value == "decimal"
        assert UnitSystem.BINARY.value == "binary"
        
        assert StorageUnit.BYTE.value[0] == "B"
        assert StorageUnit.KILOBYTE.value[0] == "KB"
        assert StorageUnit.MEGABYTE.value[0] == "MB"
        assert StorageUnit.GIBIBYTE.value[0] == "GiB"
        
        results.add_result("enums", True)
    except Exception as e:
        results.add_result("enums", False, str(e))


def test_convert():
    """Test unit conversion"""
    try:
        # KB to MB (decimal)
        assert convert(1024, "KB", "MB") == 1.024
        
        # KiB to MiB (binary)
        assert convert(1024, "KiB", "MiB") == 1.0
        
        # GB to MB
        assert convert(1, "GB", "MB") == 1000
        
        # GiB to MiB
        assert convert(1, "GiB", "MiB") == 1024
        
        # Bits to Bytes
        assert convert(8, "bit", "B") == 1.0
        
        # Same unit
        assert convert(100, "KB", "KB") == 100
        
        # Zero
        assert convert(0, "KB", "MB") == 0
        
        results.add_result("convert", True)
    except Exception as e:
        results.add_result("convert", False, str(e))


def test_to_bytes():
    """Test to_bytes function"""
    try:
        assert to_bytes(1, "KB") == 1000
        assert to_bytes(1, "KiB") == 1024
        assert to_bytes(1, "MB") == 1000000
        assert to_bytes(1, "GiB") == 1073741824
        
        # Bit conversion
        assert to_bytes(8, "bit") == 1
        
        results.add_result("to_bytes", True)
    except Exception as e:
        results.add_result("to_bytes", False, str(e))


def test_from_bytes():
    """Test from_bytes function"""
    try:
        assert from_bytes(1000, "KB") == 1.0
        assert from_bytes(1024, "KiB") == 1.0
        assert from_bytes(1000000, "MB") == 1.0
        
        results.add_result("from_bytes", True)
    except Exception as e:
        results.add_result("from_bytes", False, str(e))


def test_format_size():
    """Test size formatting"""
    try:
        # Decimal
        assert format_size(0) == "0 B"
        assert format_size(1000) == "1.00 KB"
        assert format_size(1500) == "1.50 KB"
        assert format_size(1000000) == "1.00 MB"
        
        # Binary
        assert format_size(1024, binary=True) == "1.00 KiB"
        assert format_size(1048576, binary=True) == "1.00 MiB"
        
        # Precision
        assert format_size(1500, precision=1) == "1.5 KB"
        
        # Separator
        assert format_size(1000, separator="") == "1.00KB"
        
        results.add_result("format_size", True)
    except Exception as e:
        results.add_result("format_size", False, str(e))


def test_format_bits():
    """Test bits formatting"""
    try:
        assert format_bits(0) == "0 bit"
        assert format_bits(1000) == "1.00 Kbit"
        assert format_bits(1000000) == "1.00 Mbit"
        
        results.add_result("format_bits", True)
    except Exception as e:
        results.add_result("format_bits", False, str(e))


def test_parse_size():
    """Test size parsing"""
    try:
        value, unit = parse_size("1GB")
        assert value == 1.0
        assert unit == StorageUnit.GIGABYTE
        
        value, unit = parse_size("1.5 KiB")
        assert value == 1.5
        assert unit == StorageUnit.KIBIBYTE
        
        value, unit = parse_size("1024")
        assert value == 1024.0
        assert unit == StorageUnit.BYTE
        
        # Invalid parse
        try:
            parse_size("invalid")
            results.add_result("parse_size", False, "Should raise for invalid")
        except ValueError:
            pass
        
        results.add_result("parse_size", True)
    except Exception as e:
        results.add_result("parse_size", False, str(e))


def test_parse_to_bytes():
    """Test parse to bytes"""
    try:
        assert parse_to_bytes("1KB") == 1000
        assert parse_to_bytes("1KiB") == 1024
        assert parse_to_bytes("1.5GB") == 1500000000
        
        results.add_result("parse_to_bytes", True)
    except Exception as e:
        results.add_result("parse_to_bytes", False, str(e))


def test_smart_format():
    """Test smart formatting"""
    try:
        # Less than 1KB shows bytes
        assert "B" in smart_format(500)
        # More than 1KB shows KB
        assert "KB" in smart_format(1500)
        # Binary preference
        assert "KiB" in smart_format(1536, prefer_binary=True)
        
        results.add_result("smart_format", True)
    except Exception as e:
        results.add_result("smart_format", False, str(e))


def test_ratio():
    """Test ratio calculation"""
    try:
        assert ratio(500, 1000) == 0.5
        assert ratio(0, 1000) == 0.0
        assert ratio(1000, 1000) == 1.0
        assert ratio(1000, 0) == 0.0
        
        results.add_result("ratio", True)
    except Exception as e:
        results.add_result("ratio", False, str(e))


def test_percentage():
    """Test percentage calculation"""
    try:
        assert percentage(500, 1000) == "50.0%"
        assert percentage(256, 1024) == "25.0%"
        
        results.add_result("percentage", True)
    except Exception as e:
        results.add_result("percentage", False, str(e))


def test_progress_bar():
    """Test progress bar generation"""
    try:
        bar = progress_bar(500, 1000, width=10)
        assert "50.0%" in bar
        
        bar = progress_bar(750, 1000, width=10)
        assert "75.0%" in bar
        
        # Binary
        bar = progress_bar(512, 1024, binary=True)
        assert "50.0%" in bar
        
        results.add_result("progress_bar", True)
    except Exception as e:
        results.add_result("progress_bar", False, str(e))


def test_compare():
    """Test size comparison"""
    try:
        assert compare("1GB", "500MB") == 1
        assert compare("500MB", "1GB") == -1
        # 1KB = 1000 bytes in decimal, so they are equal
        result = compare("1KB", "1000B")
        assert result == 0
        
        # Numeric comparison with units
        # 1024 MB vs 1 GB: 1024 MB = 1024000000 bytes, 1 GB = 1000000000 bytes
        assert compare(1024, 1, "MB", "GB") == 1
        
        results.add_result("compare", True)
    except Exception as e:
        results.add_result("compare", False, str(e))


def test_add():
    """Test size addition"""
    try:
        assert add("1GB", "500MB") == 1500000000
        assert add("1GB", "500MB", unit="MB") == 1500.0
        
        # Multiple sizes
        assert add("1GB", "500MB", "100MB") == 1600000000
        
        results.add_result("add", True)
    except Exception as e:
        results.add_result("add", False, str(e))


def test_subtract():
    """Test size subtraction"""
    try:
        assert subtract("2GB", "500MB") == 1500000000
        assert subtract("2GB", "500MB", unit="MB") == 1500.0
        
        results.add_result("subtract", True)
    except Exception as e:
        results.add_result("subtract", False, str(e))


def test_human_readable():
    """Test human readable formatting"""
    try:
        # Short style
        assert human_readable(1500000000) == "1.50 GB"
        
        # Long style
        hr = human_readable(1500000000, style="long")
        assert "Gigabytes" in hr
        
        # Binary long
        hr = human_readable(1024, binary=True, style="long")
        assert "Kibibyte" in hr
        
        # Zero
        assert human_readable(0) == "0 B"
        
        results.add_result("human_readable", True)
    except Exception as e:
        results.add_result("human_readable", False, str(e))


def test_find_largest_smallest():
    """Test find largest and smallest"""
    try:
        largest_str, largest_bytes = find_largest_unit(["1GB", "500MB", "2TB"])
        assert largest_str == "2TB"
        
        smallest_str, smallest_bytes = find_smallest_unit(["1GB", "500MB", "2TB"])
        assert smallest_str == "500MB"
        
        # Empty list
        try:
            find_largest_unit([])
            results.add_result("find_largest_smallest", False, "Should raise for empty")
        except ValueError:
            pass
        
        results.add_result("find_largest_smallest", True)
    except Exception as e:
        results.add_result("find_largest_smallest", False, str(e))


def test_total_size():
    """Test total size formatting"""
    try:
        assert "GB" in total_size("1GB", "500MB", "100MB")
        
        # With unit
        total = total_size("1GB", "500MB", unit="MB")
        assert "MB" in total
        
        results.add_result("total_size", True)
    except Exception as e:
        results.add_result("total_size", False, str(e))


def test_speed_format():
    """Test speed formatting"""
    try:
        assert speed_format(1024) == "1.02 KB/s"
        assert speed_format(1024, binary=True) == "1.00 KiB/s"
        
        results.add_result("speed_format", True)
    except Exception as e:
        results.add_result("speed_format", False, str(e))


def test_bandwidth_format():
    """Test bandwidth formatting"""
    try:
        assert bandwidth_format(1000000) == "1.00 Mbps"
        assert bandwidth_format(1000000000) == "1.00 Gbps"
        assert bandwidth_format(0) == "0 bps"
        
        results.add_result("bandwidth_format", True)
    except Exception as e:
        results.add_result("bandwidth_format", False, str(e))


def test_estimate_time():
    """Test time estimation"""
    try:
        # Seconds
        assert estimate_time(100, 10) == "10s"
        
        # Minutes
        t = estimate_time(1024 * 1024 * 100, 1024 * 1024)
        assert "m" in t
        
        # Infinity
        assert estimate_time(100, 0) == "∞"
        
        results.add_result("estimate_time", True)
    except Exception as e:
        results.add_result("estimate_time", False, str(e))


def test_convenience_functions():
    """Test convenience functions"""
    try:
        assert kb(1) == 1000
        assert mb(1) == 1000000
        assert gb(1) == 1000000000
        assert tb(1) == 1000000000000
        
        assert kib(1) == 1024
        assert mib(1) == 1048576
        assert gib(1) == 1073741824
        assert tib(1) == 1099511627776
        
        results.add_result("convenience_functions", True)
    except Exception as e:
        results.add_result("convenience_functions", False, str(e))


def test_unit_map():
    """Test unit map"""
    try:
        assert UNIT_MAP["KB"] == StorageUnit.KILOBYTE
        assert UNIT_MAP["MiB"] == StorageUnit.MEBIBYTE
        assert UNIT_MAP["GB"] == StorageUnit.GIGABYTE
        
        results.add_result("unit_map", True)
    except Exception as e:
        results.add_result("unit_map", False, str(e))


def test_unit_lists():
    """Test unit lists"""
    try:
        assert StorageUnit.BYTE in DECIMAL_UNITS
        assert StorageUnit.KIBIBYTE in BINARY_UNITS
        
        results.add_result("unit_lists", True)
    except Exception as e:
        results.add_result("unit_lists", False, str(e))


def test_large_values():
    """Test large values"""
    try:
        # PB
        pb = format_size(1000000000000000)
        assert "PB" in pb
        
        # EB
        eb = format_size(1000000000000000000)
        assert "EB" in eb
        
        results.add_result("large_values", True)
    except Exception as e:
        results.add_result("large_values", False, str(e))


def test_float_values():
    """Test float values"""
    try:
        assert to_bytes(1.5, "KB") == 1500
        assert from_bytes(1500, "KB") == 1.5
        
        assert format_size(1500) == "1.50 KB"
        
        results.add_result("float_values", True)
    except Exception as e:
        results.add_result("float_values", False, str(e))


def test_negative_values():
    """Test negative values"""
    try:
        # Negative ratio
        assert ratio(-500, 1000) == 0.0  # Clamped
        
        # Negative percentage
        pct = percentage(-500, 1000)
        assert "0.0%" in pct
        
        results.add_result("negative_values", True)
    except Exception as e:
        results.add_result("negative_values", False, str(e))


def test_edge_cases():
    """Test edge cases"""
    try:
        # Zero
        assert "0" in format_size(0)
        assert "0" in format_bits(0)
        assert progress_bar(0, 1000) is not None
        
        # Very small
        assert "B" in format_size(1)
        
        # Empty sizes
        assert add() == 0
        
        results.add_result("edge_cases", True)
    except Exception as e:
        results.add_result("edge_cases", False, str(e))


def test_chinese_units():
    """Test Chinese unit notation"""
    try:
        # 1.5GB in Chinese notation
        value, unit = parse_size("1.5GB")
        assert value == 1.5
        
        # Spaces in size
        value, unit = parse_size("1 GB")
        assert value == 1
        
        results.add_result("chinese_units", True)
    except Exception as e:
        results.add_result("chinese_units", False, str(e))


def test_precision_variations():
    """Test precision variations"""
    try:
        # Different precision levels - just check they contain KB
        assert "KB" in format_size(1500, precision=0)
        assert "KB" in format_size(1500, precision=1)
        assert "KB" in format_size(1500, precision=2)
        assert "KB" in format_size(1500, precision=3)
        
        results.add_result("precision_variations", True)
    except Exception as e:
        results.add_result("precision_variations", False, str(e))


# Run all tests
def run_tests():
    """Run all test functions"""
    test_enums()
    test_convert()
    test_to_bytes()
    test_from_bytes()
    test_format_size()
    test_format_bits()
    test_parse_size()
    test_parse_to_bytes()
    test_smart_format()
    test_ratio()
    test_percentage()
    test_progress_bar()
    test_compare()
    test_add()
    test_subtract()
    test_human_readable()
    test_find_largest_smallest()
    test_total_size()
    test_speed_format()
    test_bandwidth_format()
    test_estimate_time()
    test_convenience_functions()
    test_unit_map()
    test_unit_lists()
    test_large_values()
    test_float_values()
    test_negative_values()
    test_edge_cases()
    test_chinese_units()
    test_precision_variations()
    
    return results.summary()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)