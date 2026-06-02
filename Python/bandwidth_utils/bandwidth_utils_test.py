#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Bandwidth Utilities Tests

Tests for the bandwidth_utils module.
"""

import pytest
from mod import (
    parse_size,
    parse_bandwidth,
    parse_time,
    calculate_transfer_time,
    calculate_required_bandwidth,
    format_time,
    format_bandwidth,
    format_size,
    get_size_info,
    get_bandwidth_info,
    estimate_download_time,
    compare_bandwidths,
    bandwidth_for_streaming,
    download_time,
    needed_bandwidth,
    TransferResult,
    BandwidthInfo,
    SizeInfo,
    SIZE_UNITS,
    BITRATE_UNITS,
    BYTERATE_UNITS,
    TIME_UNITS,
)


class TestParseSize:
    """Tests for parse_size function."""

    def test_parse_bytes(self):
        """Test parsing bytes."""
        assert parse_size('100 B') == 100
        assert parse_size('100B') == 100

    def test_parse_kilobytes(self):
        """Test parsing kilobytes."""
        assert parse_size('1 KB') == 1024
        assert parse_size('1KB') == 1024
        assert parse_size('1 KiB') == 1024

    def test_parse_megabytes(self):
        """Test parsing megabytes."""
        assert parse_size('1 MB') == 1048576
        assert parse_size('1.5 MB') == 1572864

    def test_parse_gigabytes(self):
        """Test parsing gigabytes."""
        assert parse_size('1 GB') == 1073741824
        assert parse_size('2 GB') == 2147483648

    def test_parse_pure_number(self):
        """Test parsing pure number (assumes bytes)."""
        assert parse_size('100') == 100

    def test_parse_invalid(self):
        """Test parsing invalid format raises ValueError."""
        with pytest.raises(ValueError):
            parse_size('invalid')


class TestParseBandwidth:
    """Tests for parse_bandwidth function."""

    def test_parse_bps(self):
        """Test parsing bps."""
        assert parse_bandwidth('100 bps') == 100.0

    def test_parse_kilobits(self):
        """Test parsing Kbps."""
        assert parse_bandwidth('100 Kbps') == 100000.0

    def test_parse_megabits(self):
        """Test parsing Mbps."""
        assert parse_bandwidth('100 Mbps') == 100000000.0

    def test_parse_gigabits(self):
        """Test parsing Gbps."""
        assert parse_bandwidth('1 Gbps') == 1000000000.0

    def test_parse_bytes_per_second(self):
        """Test parsing bytes per second."""
        result = parse_bandwidth('10 MB/s')
        assert result == 80000000.0  # 10 MB/s = 80 Mbps

    def test_parse_bytes_no_space(self):
        """Test parsing bandwidth without space."""
        assert parse_bandwidth('100Mbps') == 100000000.0

    def test_parse_pure_number(self):
        """Test parsing pure number (assumes bps)."""
        assert parse_bandwidth('100000') == 100000.0


class TestParseTime:
    """Tests for parse_time function."""

    def test_parse_seconds(self):
        """Test parsing seconds."""
        assert parse_time('30s') == 30.0
        assert parse_time('30') == 30.0

    def test_parse_minutes(self):
        """Test parsing minutes."""
        assert parse_time('5m') == 300.0
        assert parse_time('5min') == 300.0

    def test_parse_hours(self):
        """Test parsing hours."""
        assert parse_time('2h') == 7200.0
        assert parse_time('1 hour') == 3600.0

    def test_parse_days(self):
        """Test parsing days."""
        assert parse_time('1d') == 86400.0
        assert parse_time('1 day') == 86400.0

    def test_parse_combined(self):
        """Test parsing combined time units."""
        assert parse_time('1h30m') == 5400.0
        assert parse_time('1h 30m') == 5400.0

    def test_parse_invalid(self):
        """Test parsing invalid format raises ValueError."""
        with pytest.raises(ValueError):
            parse_time('invalid')


class TestCalculateTransferTime:
    """Tests for calculate_transfer_time function."""

    def test_basic_calculation(self):
        """Test basic transfer time calculation."""
        result = calculate_transfer_time('1 GB', '100 Mbps')
        assert isinstance(result, TransferResult)
        assert result.time_seconds > 0
        assert result.time_formatted != ''

    def test_with_overhead(self):
        """Test calculation with protocol overhead."""
        result_no_overhead = calculate_transfer_time('1 GB', '100 Mbps', 0)
        result_with_overhead = calculate_transfer_time('1 GB', '100 Mbps', 10)
        assert result_with_overhead.time_seconds > result_no_overhead.time_seconds

    def test_string_inputs(self):
        """Test with string inputs."""
        result = calculate_transfer_time('100 MB', '10 Mbps')
        assert result.time_seconds > 0

    def test_numeric_inputs(self):
        """Test with numeric inputs."""
        result = calculate_transfer_time(104857600, 10000000.0)
        assert result.time_seconds > 0


class TestCalculateRequiredBandwidth:
    """Tests for calculate_required_bandwidth function."""

    def test_basic_calculation(self):
        """Test basic bandwidth calculation."""
        info = calculate_required_bandwidth('1 GB', '1h')
        assert isinstance(info, BandwidthInfo)
        assert info.bps > 0
        assert info.Mbps > 0

    def test_bandwidth_info_format_auto(self):
        """Test format_auto method."""
        info = calculate_required_bandwidth('1 GB', '1h')
        formatted = info.format_auto()
        assert isinstance(formatted, str)
        assert 'bps' in formatted.lower() or 'B/s' in formatted

    def test_with_string_time(self):
        """Test with string time limit."""
        info = calculate_required_bandwidth('4.7 GB', '1h')
        assert info.Mbps > 0


class TestFormatTime:
    """Tests for format_time function."""

    def test_format_seconds(self):
        """Test formatting seconds."""
        assert 's' in format_time(45.5)

    def test_format_minutes_seconds(self):
        """Test formatting minutes and seconds."""
        result = format_time(90)
        assert 'm' in result
        assert 's' in result

    def test_format_hours_minutes_seconds(self):
        """Test formatting hours, minutes, and seconds."""
        result = format_time(3661)
        assert 'h' in result
        assert 'm' in result
        assert 's' in result

    def test_format_negative(self):
        """Test formatting negative time."""
        result = format_time(-100)
        assert '-' in result

    def test_format_small_value(self):
        """Test formatting small time value."""
        result = format_time(0.5)
        assert 'ms' in result


class TestFormatBandwidth:
    """Tests for format_bandwidth function."""

    def test_format_auto_kbps(self):
        """Test auto-formatting low bandwidth."""
        result = format_bandwidth(50000)
        assert 'Kbps' in result or 'kbps' in result.lower()

    def test_format_auto_mbps(self):
        """Test auto-formatting medium bandwidth."""
        result = format_bandwidth(100000000)
        assert 'Mbps' in result or 'mbps' in result.lower()

    def test_format_auto_gbps(self):
        """Test auto-formatting high bandwidth."""
        result = format_bandwidth(1000000000)
        assert 'Gbps' in result or 'gbps' in result.lower()

    def test_format_specific_unit(self):
        """Test formatting with specific unit."""
        result = format_bandwidth(100000000, 'MB/s')
        assert 'MB/s' in result


class TestFormatSize:
    """Tests for format_size function."""

    def test_format_bytes(self):
        """Test formatting bytes."""
        assert 'B' in format_size(100)

    def test_format_kilobytes(self):
        """Test formatting kilobytes."""
        result = format_size(2048)
        assert 'KB' in result

    def test_format_megabytes(self):
        """Test formatting megabytes."""
        result = format_size(10485760)
        assert 'MB' in result

    def test_format_gigabytes(self):
        """Test formatting gigabytes."""
        result = format_size(10737418240)
        assert 'GB' in result


class TestGetSizeInfo:
    """Tests for get_size_info function."""

    def test_size_info_structure(self):
        """Test SizeInfo structure."""
        info = get_size_info(1536000000)
        assert isinstance(info, SizeInfo)
        assert info.bytes == 1536000000
        assert info.KB > 0
        assert info.MB > 0
        assert info.GB > 0

    def test_size_info_conversion(self):
        """Test size info conversion values."""
        info = get_size_info(1024)
        assert info.KB == 1.0


class TestGetBandwidthInfo:
    """Tests for get_bandwidth_info function."""

    def test_bandwidth_info_structure(self):
        """Test BandwidthInfo structure."""
        info = get_bandwidth_info(100000000)
        assert isinstance(info, BandwidthInfo)
        assert info.bps == 100000000
        assert info.Kbps == 100000
        assert info.Mbps == 100

    def test_bandwidth_info_conversion(self):
        """Test bandwidth info conversion."""
        info = get_bandwidth_info(1000000)
        assert info.Kbps == 1000.0


class TestEstimateDownloadTime:
    """Tests for estimate_download_time function."""

    def test_returns_dict(self):
        """Test that result is a dictionary."""
        result = estimate_download_time('1 GB', '100 Mbps')
        assert isinstance(result, dict)
        assert 'time_formatted' in result
        assert 'bandwidth_formatted' in result

    def test_includes_overhead(self):
        """Test that overhead is included in result."""
        result = estimate_download_time('1 GB', '100 Mbps', protocol_overhead=5.0)
        assert result['protocol_overhead_percent'] == 5.0


class TestCompareBandwidths:
    """Tests for compare_bandwidths function."""

    def test_compare_returns_dict(self):
        """Test that result is a dictionary."""
        result = compare_bandwidths('100 Mbps', '50 Mbps')
        assert isinstance(result, dict)
        assert 'fastest' in result
        assert 'slowest' in result

    def test_fastest_is_fastest(self):
        """Test that fastest is correctly identified."""
        result = compare_bandwidths('100 Mbps', '50 Mbps', '1 Gbps')
        assert '1 Gbps' == result['fastest']

    def test_ratio_calculation(self):
        """Test that ratio is calculated."""
        result = compare_bandwidths('100 Mbps', '50 Mbps')
        assert result['ratio_fastest_to_slowest'] == 2.0


class TestBandwidthForStreaming:
    """Tests for bandwidth_for_streaming function."""

    def test_1080p_h264(self):
        """Test 1080p H.264 bandwidth estimation."""
        result = bandwidth_for_streaming('1080p', 30, 'h264')
        assert 'recommended' in result
        assert 'Mbps' in result['recommended']

    def test_4k_av1(self):
        """Test 4K AV1 bandwidth estimation."""
        result = bandwidth_for_streaming('4k', 60, 'av1')
        assert 'estimated_bitrate_mbps' in result
        assert result['estimated_bitrate_mbps'] > 0

    def test_invalid_resolution(self):
        """Test invalid resolution raises ValueError."""
        with pytest.raises(ValueError):
            bandwidth_for_streaming('invalid', 30, 'h264')


class TestQuickFunctions:
    """Tests for quick convenience functions."""

    def test_download_time(self):
        """Test download_time function."""
        result = download_time('1 GB', '100 Mbps')
        assert isinstance(result, str)
        assert 's' in result or 'm' in result or 'h' in result

    def test_needed_bandwidth(self):
        """Test needed_bandwidth function."""
        result = needed_bandwidth('1 GB', '1h')
        assert isinstance(result, str)


class TestEdgeCases:
    """Tests for edge cases."""

    def test_zero_bandwidth_error(self):
        """Test that zero bandwidth raises ValueError."""
        with pytest.raises(ValueError):
            calculate_transfer_time('1 GB', 0)

    def test_zero_time_error(self):
        """Test that zero time raises ValueError."""
        with pytest.raises(ValueError):
            calculate_required_bandwidth('1 GB', '0s')

    def test_empty_string_bandwidth(self):
        """Test parsing empty string bandwidth."""
        with pytest.raises(ValueError):
            parse_bandwidth('')

    def test_empty_string_size(self):
        """Test parsing empty string size."""
        with pytest.raises(ValueError):
            parse_size('')


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
