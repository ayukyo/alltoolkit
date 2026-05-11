"""
Tests for KSUID Utilities

Run: python Python/ksuid_utils/ksuid_utils_test.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    generate, generate_bytes, parse, validate, extract_timestamp,
    extract_datetime, compare, sort, sort_descending, generate_range,
    generate_batch, from_datetime, to_datetime, get_time_range,
    is_sorted, batch_parse, generate_monotonic, format_ksuid, analyze,
    humanize_age, get_epoch_info, encode_base62, decode_base62,
    KSUID_STRING_LENGTH, KSUID_BYTES_LENGTH, KSUID_EPOCH
)

from datetime import datetime, timezone, timedelta


class ResultCollector:
    """Collect test results"""
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.tests = []
    
    def test(self, name: str, condition: bool, details: str = ""):
        if condition:
            self.passed += 1
            self.tests.append(f"✅ {name}")
        else:
            self.failed += 1
            self.tests.append(f"❌ {name}" + (f" - {details}" if details else ""))
    
    def summary(self):
        print(f"\n{'='*60}")
        print(f"KSUID Utils Test Results: {self.passed} passed, {self.failed} failed")
        print(f"{'='*60}")
        for t in self.tests:
            print(t)
        return self.failed == 0


def test_constants():
    """Test KSUID constants"""
    r = ResultCollector()
    
    r.test("String length is 27", KSUID_STRING_LENGTH == 27)
    r.test("Bytes length is 20", KSUID_BYTES_LENGTH == 20)
    r.test("Epoch is 1400000000", KSUID_EPOCH == 1400000000)
    
    return r


def test_base62():
    """Test Base62 encoding and decoding"""
    r = ResultCollector()
    
    # Encode/decode roundtrip
    test_bytes = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13'
    encoded = encode_base62(test_bytes)
    decoded = decode_base62(encoded)
    r.test("Base62 roundtrip", decoded == test_bytes)
    
    # All zeros
    zeros = b'\x00' * 20
    encoded = encode_base62(zeros)
    decoded = decode_base62(encoded)
    r.test("Base62 zeros roundtrip", decoded == zeros)
    
    # Invalid character
    try:
        decode_base62('aWgEPTl1tmebfsQzFP4qxw980!')
        r.test("Base62 invalid char", False)
    except ValueError:
        r.test("Base62 invalid char", True)
    
    return r


def test_generate():
    """Test KSUID generation"""
    r = ResultCollector()
    
    # Generate basic KSUID
    ksuid = generate()
    r.test("Generate length", len(ksuid) == KSUID_STRING_LENGTH)
    r.test("Generate valid", validate(ksuid))
    
    # Generate with specific timestamp
    timestamp = 1640995200  # 2022-01-01 00:00:00 UTC
    ksuid = generate(timestamp=timestamp)
    r.test("Generate with timestamp valid", validate(ksuid))
    r.test("Generate with timestamp matches", extract_timestamp(ksuid) == timestamp)
    
    # Generate bytes
    ksuid_bytes = generate_bytes()
    r.test("Generate bytes length", len(ksuid_bytes) == KSUID_BYTES_LENGTH)
    
    # Bytes to string roundtrip
    encoded = encode_base62(ksuid_bytes)
    r.test("Bytes to string length", len(encoded) == KSUID_STRING_LENGTH)
    
    return r


def test_parse():
    """Test KSUID parsing"""
    r = ResultCollector()
    
    # Parse valid KSUID
    ksuid = generate(timestamp=1640995200)
    result = parse(ksuid)
    
    r.test("Parse valid KSUID", result['valid'])
    r.test("Parse timestamp correct", result['timestamp'] == 1640995200)
    r.test("Parse has payload", result['payload'] is not None)
    r.test("Parse has datetime", result['datetime'] is not None)
    
    # Parse invalid KSUID (wrong length)
    result = parse("too_short")
    r.test("Parse invalid length", not result['valid'])
    r.test("Parse invalid length has error", 'error' in result)
    
    # Parse invalid KSUID (invalid characters)
    result = parse("aWgEPTl1tmebfsQzFP4qxw98!")
    r.test("Parse invalid chars", not result['valid'])
    
    return r


def test_validate():
    """Test KSUID validation"""
    r = ResultCollector()
    
    # Valid KSUID
    ksuid = generate()
    r.test("Validate generated KSUID", validate(ksuid))
    
    # Invalid KSUIDs
    r.test("Validate empty string", not validate(""))
    r.test("Validate wrong length", not validate("abc"))
    r.test("Validate invalid chars", not validate("aWgEPTl1tmebfsQzFP4qxw98!"))
    
    return r


def test_extract():
    """Test timestamp and datetime extraction"""
    r = ResultCollector()
    
    # Known timestamp
    timestamp = 1640995200  # 2022-01-01 00:00:00 UTC
    ksuid = generate(timestamp=timestamp)
    
    r.test("Extract timestamp", extract_timestamp(ksuid) == timestamp)
    
    dt = extract_datetime(ksuid)
    r.test("Extract datetime year", dt.year == 2022)
    r.test("Extract datetime month", dt.month == 1)
    r.test("Extract datetime day", dt.day == 1)
    
    # Invalid KSUID
    r.test("Extract timestamp invalid", extract_timestamp("invalid") is None)
    r.test("Extract datetime invalid", extract_datetime("invalid") is None)
    
    return r


def test_compare():
    """Test KSUID comparison"""
    r = ResultCollector()
    
    # Generate two KSUIDs with different timestamps
    ksuid1 = generate(timestamp=1640995200)
    ksuid2 = generate(timestamp=1640995201)
    
    result = compare(ksuid1, ksuid2)
    
    r.test("Compare older", result['ksuid1_older'])
    r.test("Compare time diff", result['time_diff_seconds'] == 1)
    r.test("Compare same payload", not result['same_payload'])  # Different random
    
    # Same timestamp KSUIDs
    ksuid3 = generate(timestamp=1640995200)
    ksuid4 = generate(timestamp=1640995200)
    
    result = compare(ksuid3, ksuid4)
    r.test("Compare same time", result['same_time'])
    
    # Invalid comparison
    result = compare("invalid", ksuid1)
    r.test("Compare with invalid", 'error' in result)
    
    return r


def test_sort():
    """Test KSUID sorting"""
    r = ResultCollector()
    
    # Generate KSUIDs in random order
    ksuids = [
        generate(timestamp=1640995203),
        generate(timestamp=1640995200),
        generate(timestamp=1640995202),
        generate(timestamp=1640995201),
    ]
    
    sorted_ascending = sort(ksuids)
    sorted_descending = sort_descending(ksuids)
    
    # Check ascending order
    timestamps_asc = [extract_timestamp(k) for k in sorted_ascending]
    r.test("Sort ascending", timestamps_asc == sorted(timestamps_asc))
    
    # Check descending order
    timestamps_desc = [extract_timestamp(k) for k in sorted_descending]
    r.test("Sort descending", timestamps_desc == sorted(timestamps_desc, reverse=True))
    
    return r


def test_generate_range():
    """Test KSUID range generation"""
    r = ResultCollector()
    
    # Generate range
    ksuids = generate_range(1640995200, 1640995205)
    
    r.test("Range generation count", len(ksuids) == 5)
    r.test("Range all valid", all(validate(k) for k in ksuids))
    
    # Check timestamps
    timestamps = [extract_timestamp(k) for k in ksuids]
    expected = list(range(1640995200, 1640995205))
    r.test("Range timestamps correct", timestamps == expected)
    
    # Invalid range (start >= end)
    try:
        generate_range(1640995205, 1640995200)
        r.test("Range validation", False)
    except ValueError:
        r.test("Range validation", True)
    
    return r


def test_generate_batch():
    """Test batch generation"""
    r = ResultCollector()
    
    ksuids = generate_batch(10)
    
    r.test("Batch count", len(ksuids) == 10)
    r.test("Batch all valid", all(validate(k) for k in ksuids))
    r.test("Batch all unique", len(set(ksuids)) == 10)
    
    return r


def test_datetime_conversion():
    """Test datetime conversion"""
    r = ResultCollector()
    
    # From datetime
    dt = datetime(2022, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    ksuid = from_datetime(dt)
    
    r.test("From datetime valid", validate(ksuid))
    r.test("From datetime timestamp", extract_timestamp(ksuid) == int(dt.timestamp()))
    
    # To datetime
    dt_back = to_datetime(ksuid)
    r.test("To datetime year", dt_back.year == 2022)
    r.test("To datetime UTC", dt_back.tzinfo == timezone.utc)
    
    return r


def test_time_range():
    """Test time range extraction"""
    r = ResultCollector()
    
    ksuids = [
        generate(timestamp=1640995200),
        generate(timestamp=1640995205),
        generate(timestamp=1640995203),
    ]
    
    time_range = get_time_range(ksuids)
    
    r.test("Time range min", time_range[0] == 1640995200)
    r.test("Time range max", time_range[1] == 1640995205)
    
    # Empty list
    empty_range = get_time_range([])
    r.test("Time range empty", empty_range is None)
    
    return r


def test_is_sorted():
    """Test sorted check"""
    r = ResultCollector()
    
    # Sorted list
    sorted_ksuids = [
        generate(timestamp=1640995200),
        generate(timestamp=1640995201),
        generate(timestamp=1640995202),
    ]
    r.test("Is sorted - sorted", is_sorted(sorted_ksuids))
    
    # Unsorted list
    unsorted_ksuids = [
        generate(timestamp=1640995202),
        generate(timestamp=1640995200),
        generate(timestamp=1640995201),
    ]
    r.test("Is sorted - unsorted", not is_sorted(unsorted_ksuids))
    
    # With invalid
    mixed = [generate(), "invalid"]
    r.test("Is sorted - with invalid", not is_sorted(mixed))
    
    return r


def test_batch_parse():
    """Test batch parsing"""
    r = ResultCollector()
    
    ksuids = [
        generate(timestamp=1640995200),
        generate(timestamp=1640995201),
        "invalid_ksuid",
    ]
    
    result = batch_parse(ksuids)
    
    r.test("Batch parse valid count", result['valid_count'] == 2)
    r.test("Batch parse invalid count", result['invalid_count'] == 1)
    r.test("Batch parse total", result['total'] == 3)
    r.test("Batch parse has time range", result['time_range'] is not None)
    
    return r


def test_monotonic():
    """Test monotonic generation"""
    r = ResultCollector()
    
    # Generate monotonic sequence
    k1 = generate_monotonic()
    k2 = generate_monotonic(k1)
    k3 = generate_monotonic(k2)
    
    r.test("Monotonic all valid", validate(k1) and validate(k2) and validate(k3))
    
    # Check ordering
    result = compare(k1, k2)
    r.test("Monotonic k1 older than k2", result['ksuid1_older'] or result['same_time'])
    
    result = compare(k2, k3)
    r.test("Monotonic k2 older than k3", result['ksuid1_older'] or result['same_time'])
    
    return r


def test_format():
    """Test KSUID formatting"""
    r = ResultCollector()
    
    ksuid = generate()
    
    # Default format
    formatted = format_ksuid(ksuid, "default")
    r.test("Format default", formatted == ksuid)
    
    # Grouped format
    formatted = format_ksuid(ksuid, "grouped")
    r.test("Format grouped has dash", '-' in formatted)
    r.test("Format grouped length", len(formatted.replace('-', '')) == KSUID_STRING_LENGTH)
    
    # With time format
    formatted = format_ksuid(ksuid, "with_time")
    r.test("Format with time contains UTC", 'UTC' in formatted)
    
    return r


def test_analyze():
    """Test KSUID analysis"""
    r = ResultCollector()
    
    ksuid = generate(timestamp=1640995200)
    result = analyze(ksuid)
    
    r.test("Analyze valid", result['valid'])
    r.test("Analyze has timestamp", result['timestamp'] == 1640995200)
    r.test("Analyze has year", result['year'] == 2022)
    r.test("Analyze has age", result['age_seconds'] >= 0)
    r.test("Analyze has human age", 'age_human' in result)
    
    # Invalid KSUID
    result = analyze("invalid")
    r.test("Analyze invalid", not result['valid'])
    
    return r


def test_humanize_age():
    """Test humanize age function"""
    r = ResultCollector()
    
    r.test("Humanize 30 seconds", humanize_age(30) == "30 seconds")
    r.test("Humanize 1 minute", humanize_age(60) == "1 minute")
    r.test("Humanize 5 minutes", humanize_age(300) == "5 minutes")
    r.test("Humanize 1 hour", humanize_age(3600) == "1 hour")
    r.test("Humanize 2 hours", humanize_age(7200) == "2 hours")
    r.test("Humanize 1 day", humanize_age(86400) == "1 day")
    r.test("Humanize 30 days", humanize_age(2592000) == "1 month")
    r.test("Humanize 365 days", humanize_age(31536000) == "1 year")
    
    return r


def test_epoch_info():
    """Test epoch information"""
    r = ResultCollector()
    
    info = get_epoch_info()
    
    r.test("Epoch info has epoch", info['epoch'] == KSUID_EPOCH)
    r.test("Epoch info has datetime", 'datetime' in info)
    r.test("Epoch info has description", 'description' in info)
    r.test("Epoch info has max timestamp", 'max_timestamp' in info)
    
    return r


def test_edge_cases():
    """Test edge cases"""
    r = ResultCollector()
    
    # Epoch boundary KSUID
    epoch_ksuid = generate(timestamp=KSUID_EPOCH)
    result = parse(epoch_ksuid)
    r.test("Epoch KSUID valid", result['valid'])
    r.test("Epoch KSUID timestamp", result['ksuid_timestamp'] == 0)
    
    # Large timestamp
    large_timestamp = KSUID_EPOCH + 100000000  # ~3 years after epoch
    large_ksuid = generate(timestamp=large_timestamp)
    r.test("Large timestamp KSUID valid", validate(large_ksuid))
    
    # Timestamp too early (before epoch)
    try:
        generate(timestamp=KSUID_EPOCH - 1)
        r.test("Timestamp before epoch", False)
    except ValueError:
        r.test("Timestamp before epoch", True)
    
    # All zeros payload (valid but unlikely)
    zero_payload = b'\x00' * 16
    ksuid_bytes = b'\x00\x00\x00\x00' + zero_payload
    ksuid_str = encode_base62(ksuid_bytes)
    r.test("Zero payload KSUID valid", validate(ksuid_str))
    
    return r


def main():
    """Run all tests"""
    all_results = []
    
    print("Testing KSUID Utilities...")
    print("=" * 60)
    
    test_functions = [
        test_constants,
        test_base62,
        test_generate,
        test_parse,
        test_validate,
        test_extract,
        test_compare,
        test_sort,
        test_generate_range,
        test_generate_batch,
        test_datetime_conversion,
        test_time_range,
        test_is_sorted,
        test_batch_parse,
        test_monotonic,
        test_format,
        test_analyze,
        test_humanize_age,
        test_epoch_info,
        test_edge_cases,
    ]
    
    for test_func in test_functions:
        print(f"\nRunning {test_func.__name__}...")
        result = test_func()
        all_results.append(result)
    
    # Combine all results
    combined = ResultCollector()
    for r in all_results:
        combined.passed += r.passed
        combined.failed += r.failed
        combined.tests.extend(r.tests)
    
    return combined.summary()


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)