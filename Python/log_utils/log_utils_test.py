#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Log Utils Test Suite
====================================
Comprehensive test suite for the log utilities module.

Run with: python3 log_utils_test.py
"""

import sys
import os
import json
from datetime import datetime, timedelta

# Add parent directory to path for imports
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(parent_dir, 'log_utils'))

from mod import (
    LogLevel, LogEntry,
    parse_log_level, parse_timestamp, parse_apache_log, parse_nginx_log,
    parse_syslog, parse_json_log, parse_log_line,
    filter_by_level, filter_by_time_range, filter_by_pattern, filter_by_source,
    count_by_level, count_by_hour, get_error_summary, calculate_error_rate,
    detect_anomalies, format_log_entry, to_json_lines, to_csv,
    search_logs, extract_field, get_log_files, get_file_size, get_file_age_days,
    find_rotation_candidates, tail_log, merge_log_files, generate_sample_log
)


# ============================================================================
# Test Framework
# ============================================================================

class TestResult:
    """Simple test result tracker."""
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def record(self, name: str, passed: bool, error: str = None):
        if passed:
            self.passed += 1
        else:
            self.failed += 1
            self.errors.append((name, error))
    
    def summary(self) -> str:
        total = self.passed + self.failed
        return f"Tests: {total} | Passed: {self.passed} | Failed: {self.failed}"
    
    def is_success(self) -> bool:
        return self.failed == 0


result = TestResult()


def test(name: str, condition: bool, error_msg: str = None):
    """Record a test result."""
    if not condition:
        error_msg = error_msg or f"Expected True, got False"
        result.record(name, False, error_msg)
        print(f"  ❌ {name}: {error_msg}")
    else:
        result.record(name, True)
        print(f"  ✅ {name}")


def test_eq(name: str, actual, expected, error_msg: str = None):
    """Test equality."""
    if actual != expected:
        error_msg = error_msg or f"Expected {expected!r}, got {actual!r}"
        result.record(name, False, error_msg)
        print(f"  ❌ {name}: {error_msg}")
    else:
        result.record(name, True)
        print(f"  ✅ {name}")


# ============================================================================
# LogLevel Tests
# ============================================================================

def test_log_level_enum():
    """Test LogLevel enum."""
    print("\n[LogLevel Enum Tests]")
    
    test_eq("LogLevel.DEBUG.value", LogLevel.DEBUG.value, 10)
    test_eq("LogLevel.INFO.value", LogLevel.INFO.value, 20)
    test_eq("LogLevel.ERROR.value", LogLevel.ERROR.value, 40)
    test_eq("LogLevel.CRITICAL.value", LogLevel.CRITICAL.value, 50)


def test_log_level_from_string():
    """Test LogLevel.from_string()."""
    print("\n[LogLevel from_string Tests]")
    
    test_eq("from_string('DEBUG')", LogLevel.from_string('DEBUG'), LogLevel.DEBUG)
    test_eq("from_string('info')", LogLevel.from_string('info'), LogLevel.INFO)
    test_eq("from_string('ERROR')", LogLevel.from_string('ERROR'), LogLevel.ERROR)
    test_eq("from_string('warn')", LogLevel.from_string('warn'), LogLevel.WARN)
    test_eq("from_string('CRITICAL')", LogLevel.from_string('CRITICAL'), LogLevel.CRITICAL)
    test_eq("from_string('FATAL')", LogLevel.from_string('FATAL'), LogLevel.FATAL)
    test_eq("from_string('UNKNOWN')", LogLevel.from_string('UNKNOWN'), LogLevel.INFO)
    test_eq("from_string(None)", LogLevel.from_string(None), LogLevel.INFO)
    test_eq("from_string('DBG')", LogLevel.from_string('DBG'), LogLevel.DEBUG)
    test_eq("from_string('ERR')", LogLevel.from_string('ERR'), LogLevel.ERROR)


def test_log_level_from_numeric():
    """Test LogLevel.from_numeric()."""
    print("\n[LogLevel from_numeric Tests]")
    
    test_eq("from_numeric(5)", LogLevel.from_numeric(5), LogLevel.DEBUG)
    test_eq("from_numeric(15)", LogLevel.from_numeric(15), LogLevel.INFO)
    test_eq("from_numeric(25)", LogLevel.from_numeric(25), LogLevel.WARN)
    test_eq("from_numeric(40)", LogLevel.from_numeric(40), LogLevel.ERROR)
    test_eq("from_numeric(50)", LogLevel.from_numeric(50), LogLevel.CRITICAL)
    test_eq("from_numeric(100)", LogLevel.from_numeric(100), LogLevel.FATAL)


# ============================================================================
# LogEntry Tests
# ============================================================================

def test_log_entry_class():
    """Test LogEntry class."""
    print("\n[LogEntry Class Tests]")
    
    entry = LogEntry(
        timestamp=datetime(2024, 1, 15, 10, 30, 0),
        level=LogLevel.ERROR,
        message="Test error message",
        source="test_module",
        extra={'key': 'value'}
    )
    
    test_eq("LogEntry.timestamp", entry.timestamp, datetime(2024, 1, 15, 10, 30, 0))
    test_eq("LogEntry.level", entry.level, LogLevel.ERROR)
    test_eq("LogEntry.message", entry.message, "Test error message")
    test_eq("LogEntry.source", entry.source, "test_module")
    test_eq("LogEntry.extra['key']", entry.extra['key'], 'value')
    
    # Test to_dict
    d = entry.to_dict()
    test("LogEntry.to_dict() has keys", 
         set(d.keys()) == {'timestamp', 'level', 'message', 'source', 'extra'})
    
    # Test to_json
    j = entry.to_json()
    parsed = json.loads(j)
    test("LogEntry.to_json() is valid JSON", parsed['level'] == 'ERROR')
    
    # Test repr
    repr_str = repr(entry)
    test("LogEntry.__repr__() contains level", 'ERROR' in repr_str)


# ============================================================================
# Log Parsing Tests
# ============================================================================

def test_parse_log_level():
    """Test parse_log_level()."""
    print("\n[parse_log_level Tests]")
    
    test_eq("parse_log_level('ERROR msg')", 
            parse_log_level('2024-01-15 10:30:00 ERROR Database failed'), 
            LogLevel.ERROR)
    test_eq("parse_log_level('INFO msg')", 
            parse_log_level('INFO Application started'), 
            LogLevel.INFO)
    test_eq("parse_log_level('[DEBUG] msg')", 
            parse_log_level('[DEBUG] Variable dump'), 
            LogLevel.DEBUG)
    test_eq("parse_log_level('WARNING msg')", 
            parse_log_level('WARNING: High memory'), 
            LogLevel.WARNING)
    test_eq("parse_log_level('CRITICAL msg')", 
            parse_log_level('CRITICAL System failure'), 
            LogLevel.CRITICAL)
    test_eq("parse_log_level('no level')", 
            parse_log_level('Just a message'), 
            LogLevel.INFO)
    test_eq("parse_log_level('')", parse_log_level(''), LogLevel.INFO)
    test_eq("parse_log_level(None)", parse_log_level(None), LogLevel.INFO)


def test_parse_timestamp():
    """Test parse_timestamp()."""
    print("\n[parse_timestamp Tests]")
    
    # ISO format
    ts = parse_timestamp('2024-01-15 10:30:45 INFO msg')
    test("parse_timestamp ISO format", 
         ts and ts.year == 2024 and ts.month == 1 and ts.day == 15)
    
    # ISO with T
    ts = parse_timestamp('2024-01-15T10:30:45 INFO msg')
    test("parse_timestamp ISO with T", 
         ts and ts.hour == 10 and ts.minute == 30)
    
    # Apache format
    ts = parse_timestamp('15/Jan/2024:10:30:45 +0000 GET /path')
    test("parse_timestamp Apache format", ts is not None)
    
    # Syslog format
    ts = parse_timestamp('Jan 15 10:30:45 hostname tag: message')
    test("parse_timestamp Syslog format", ts is not None)
    
    # No timestamp
    ts = parse_timestamp('Just a message with no timestamp')
    test("parse_timestamp no timestamp", ts is None)
    
    # Empty
    ts = parse_timestamp('')
    test("parse_timestamp empty", ts is None)


def test_parse_apache_log():
    """Test parse_apache_log()."""
    print("\n[parse_apache_log Tests]")
    
    line = '127.0.0.1 - frank [10/Oct/2000:13:55:36 -0700] "GET /apache_pb.gif HTTP/1.0" 200 2326 "http://www.example.com/start.html" "Mozilla/4.08"'
    parsed = parse_apache_log(line)
    
    test("parse_apache_log returns dict", parsed is not None)
    test_eq("parse_apache_log ip", parsed['ip'], '127.0.0.1')
    test_eq("parse_apache_log user", parsed['user'], 'frank')
    test_eq("parse_apache_log method", parsed['method'], 'GET')
    test_eq("parse_apache_log path", parsed['path'], '/apache_pb.gif')
    test_eq("parse_apache_log status", parsed['status'], 200)
    test_eq("parse_apache_log size", parsed['size'], 2326)
    test("parse_apache_log has timestamp", parsed['timestamp'] is not None)
    
    # Invalid line
    parsed = parse_apache_log('invalid log line')
    test("parse_apache_log invalid returns None", parsed is None)


def test_parse_syslog():
    """Test parse_syslog()."""
    print("\n[parse_syslog Tests]")
    
    line = '<13>Jan 15 10:30:45 myhost myapp[1234]: Test message'
    parsed = parse_syslog(line)
    
    test("parse_syslog returns dict", parsed is not None)
    test_eq("parse_syslog priority", parsed['priority'], 13)
    test_eq("parse_syslog hostname", parsed['hostname'], 'myhost')
    test_eq("parse_syslog tag", parsed['tag'], 'myapp')
    test_eq("parse_syslog pid", parsed['pid'], 1234)
    test_eq("parse_syslog message", parsed['message'], 'Test message')
    
    # Without priority
    line2 = 'Jan 15 10:30:45 myhost myapp: Test message'
    parsed2 = parse_syslog(line2)
    test("parse_syslog without priority", parsed2 is not None)


def test_parse_json_log():
    """Test parse_json_log()."""
    print("\n[parse_json_log Tests]")
    
    line = '{"timestamp": "2024-01-15T10:30:45", "level": "ERROR", "message": "Test"}'
    parsed = parse_json_log(line)
    
    test("parse_json_log returns dict", parsed is not None)
    test_eq("parse_json_log level", parsed['level'], 'ERROR')
    test_eq("parse_json_log message", parsed['message'], 'Test')
    
    # Invalid JSON
    parsed = parse_json_log('not json')
    test("parse_json_log invalid returns None", parsed is None)


def test_parse_log_line_auto():
    """Test parse_log_line with auto-detection."""
    print("\n[parse_log_line auto-detection Tests]")
    
    # JSON
    result = parse_log_line('{"level": "INFO", "message": "test"}', 'auto')
    test("parse_log_line detects JSON", isinstance(result, dict))
    
    # Apache
    line = '192.168.1.1 - - [15/Jan/2024:10:30:45 +0000] "GET / HTTP/1.1" 200 1234'
    result = parse_log_line(line, 'auto')
    test("parse_log_line detects Apache", isinstance(result, dict) and 'ip' in result)
    
    # Generic
    result = parse_log_line('2024-01-15 10:30:45 ERROR Test message', 'auto')
    test("parse_log_line generic returns LogEntry", isinstance(result, LogEntry))


# ============================================================================
# Log Filtering Tests
# ============================================================================

def test_filter_by_level():
    """Test filter_by_level()."""
    print("\n[filter_by_level Tests]")
    
    logs = [
        LogEntry(level=LogLevel.DEBUG, message="Debug msg"),
        LogEntry(level=LogLevel.INFO, message="Info msg"),
        LogEntry(level=LogLevel.WARN, message="Warn msg"),
        LogEntry(level=LogLevel.ERROR, message="Error msg"),
    ]
    
    # Filter INFO and above
    filtered = filter_by_level(logs, 'INFO')
    test_eq("filter_by_level INFO count", len(filtered), 3)
    test("filter_by_level excludes DEBUG", 
         all(e.level.value >= LogLevel.INFO.value for e in filtered))
    
    # Filter ERROR and above
    filtered = filter_by_level(logs, LogLevel.ERROR)
    test_eq("filter_by_level ERROR count", len(filtered), 1)
    
    # Filter with numeric level
    filtered = filter_by_level(logs, 40)
    test_eq("filter_by_level numeric count", len(filtered), 1)
    
    # Empty logs
    filtered = filter_by_level([], 'INFO')
    test_eq("filter_by_level empty", len(filtered), 0)


def test_filter_by_pattern():
    """Test filter_by_pattern()."""
    print("\n[filter_by_pattern Tests]")
    
    logs = [
        LogEntry(message="Database connection established"),
        LogEntry(message="Database query failed"),
        LogEntry(message="Cache miss"),
        LogEntry(message="Request completed"),
    ]
    
    # Pattern match
    filtered = filter_by_pattern(logs, r'Database')
    test_eq("filter_by_pattern Database count", len(filtered), 2)
    
    # Case insensitive
    filtered = filter_by_pattern(logs, r'database', case_sensitive=False)
    test_eq("filter_by_pattern case insensitive", len(filtered), 2)
    
    # Case sensitive
    filtered = filter_by_pattern(logs, r'database', case_sensitive=True)
    test_eq("filter_by_pattern case sensitive", len(filtered), 0)
    
    # Regex pattern
    filtered = filter_by_pattern(logs, r'(failed|error)', case_sensitive=False)
    test_eq("filter_by_pattern regex", len(filtered), 1)


def test_filter_by_time_range():
    """Test filter_by_time_range()."""
    print("\n[filter_by_time_range Tests]")
    
    base = datetime(2024, 1, 15, 12, 0, 0)
    logs = [
        LogEntry(timestamp=base - timedelta(hours=2), message="Old"),
        LogEntry(timestamp=base - timedelta(hours=1), message="Recent"),
        LogEntry(timestamp=base, message="Now"),
        LogEntry(timestamp=base + timedelta(hours=1), message="Future"),
    ]
    
    # Time range
    filtered = filter_by_time_range(logs, 
                                    start_time=base - timedelta(minutes=30),
                                    end_time=base + timedelta(minutes=30))
    test_eq("filter_by_time_range count", len(filtered), 1)
    test_eq("filter_by_time_range message", filtered[0].message, "Now")
    
    # Only start time
    filtered = filter_by_time_range(logs, start_time=base)
    test_eq("filter_by_time_range start only", len(filtered), 2)


def test_filter_by_source():
    """Test filter_by_source()."""
    print("\n[filter_by_source Tests]")
    
    logs = [
        LogEntry(source="auth", message="Login"),
        LogEntry(source="database", message="Query"),
        LogEntry(source="auth", message="Logout"),
        LogEntry(source="cache", message="Miss"),
    ]
    
    filtered = filter_by_source(logs, 'auth')
    test_eq("filter_by_source single", len(filtered), 2)
    
    filtered = filter_by_source(logs, ['auth', 'cache'])
    test_eq("filter_by_source multiple", len(filtered), 3)


# ============================================================================
# Log Analysis Tests
# ============================================================================

def test_count_by_level():
    """Test count_by_level()."""
    print("\n[count_by_level Tests]")
    
    logs = [
        LogEntry(level=LogLevel.DEBUG, message="d1"),
        LogEntry(level=LogLevel.DEBUG, message="d2"),
        LogEntry(level=LogLevel.INFO, message="i1"),
        LogEntry(level=LogLevel.ERROR, message="e1"),
        LogEntry(level=LogLevel.ERROR, message="e2"),
        LogEntry(level=LogLevel.ERROR, message="e3"),
    ]
    
    counts = count_by_level(logs)
    test_eq("count_by_level DEBUG", counts.get('DEBUG', 0), 2)
    test_eq("count_by_level INFO", counts.get('INFO', 0), 1)
    test_eq("count_by_level ERROR", counts.get('ERROR', 0), 3)


def test_count_by_hour():
    """Test count_by_hour()."""
    print("\n[count_by_hour Tests]")
    
    logs = [
        LogEntry(timestamp=datetime(2024, 1, 15, 10, 0, 0), message="h10"),
        LogEntry(timestamp=datetime(2024, 1, 15, 10, 30, 0), message="h10"),
        LogEntry(timestamp=datetime(2024, 1, 15, 11, 0, 0), message="h11"),
        LogEntry(timestamp=datetime(2024, 1, 15, 14, 0, 0), message="h14"),
    ]
    
    counts = count_by_hour(logs)
    test_eq("count_by_hour 10", counts.get(10, 0), 2)
    test_eq("count_by_hour 11", counts.get(11, 0), 1)
    test_eq("count_by_hour 14", counts.get(14, 0), 1)


def test_get_error_summary():
    """Test get_error_summary()."""
    print("\n[get_error_summary Tests]")
    
    logs = [
        LogEntry(level=LogLevel.ERROR, message="Connection failed"),
        LogEntry(level=LogLevel.ERROR, message="Connection failed"),
        LogEntry(level=LogLevel.ERROR, message="Connection failed"),
        LogEntry(level=LogLevel.ERROR, message="Timeout error"),
        LogEntry(level=LogLevel.ERROR, message="Timeout error"),
        LogEntry(level=LogLevel.INFO, message="Success"),
    ]
    
    summary = get_error_summary(logs, top_n=2)
    test_eq("get_error_summary top count", len(summary), 2)
    test_eq("get_error_summary top message", summary[0][0], "Connection failed")
    test_eq("get_error_summary top count value", summary[0][1], 3)


def test_calculate_error_rate():
    """Test calculate_error_rate()."""
    print("\n[calculate_error_rate Tests]")
    
    logs = [
        LogEntry(level=LogLevel.INFO, message="i1"),
        LogEntry(level=LogLevel.INFO, message="i2"),
        LogEntry(level=LogLevel.ERROR, message="e1"),
        LogEntry(level=LogLevel.ERROR, message="e2"),
    ]
    
    rate = calculate_error_rate(logs)
    test_eq("calculate_error_rate", rate, 0.5)
    
    # Empty
    rate = calculate_error_rate([])
    test_eq("calculate_error_rate empty", rate, 0.0)


def test_detect_anomalies():
    """Test detect_anomalies()."""
    print("\n[detect_anomalies Tests]")
    
    base = datetime(2024, 1, 15, 12, 0, 0)
    # Normal: 1 log per minute for 10 minutes
    # Anomaly: 20 logs in one minute
    logs = []
    for i in range(10):
        logs.append(LogEntry(timestamp=base + timedelta(minutes=i), message="normal"))
    
    # Add anomaly spike
    for i in range(20):
        logs.append(LogEntry(timestamp=base + timedelta(minutes=15), message="spike"))
    
    anomalies = detect_anomalies(logs, window_size=60, threshold_multiplier=2.0)
    test("detect_anomalies finds spike", len(anomalies) > 0)


# ============================================================================
# Log Formatting Tests
# ============================================================================

def test_format_log_entry():
    """Test format_log_entry()."""
    print("\n[format_log_entry Tests]")
    
    entry = LogEntry(
        timestamp=datetime(2024, 1, 15, 10, 30, 45),
        level=LogLevel.ERROR,
        message="Test message",
        source="test"
    )
    
    formatted = format_log_entry(entry, '%(timestamp)s %(level)s %(message)s')
    test("format_log_entry contains timestamp", '2024-01-15 10:30:45' in formatted)
    test("format_log_entry contains level", 'ERROR' in formatted)
    test("format_log_entry contains message", 'Test message' in formatted)


def test_to_json_lines():
    """Test to_json_lines()."""
    print("\n[to_json_lines Tests]")
    
    logs = [
        LogEntry(level=LogLevel.INFO, message="msg1"),
        LogEntry(level=LogLevel.ERROR, message="msg2"),
    ]
    
    jsonl = to_json_lines(logs)
    lines = jsonl.split('\n')
    test_eq("to_json_lines line count", len(lines), 2)
    
    # Verify valid JSON
    parsed = json.loads(lines[0])
    test_eq("to_json_lines valid JSON level", parsed['level'], 'INFO')


def test_to_csv():
    """Test to_csv()."""
    print("\n[to_csv Tests]")
    
    logs = [
        LogEntry(timestamp=datetime(2024, 1, 15, 10, 0, 0), level=LogLevel.INFO, message="msg1", source="s1"),
        LogEntry(timestamp=datetime(2024, 1, 15, 11, 0, 0), level=LogLevel.ERROR, message="msg2", source="s2"),
    ]
    
    csv_str = to_csv(logs)
    lines = csv_str.split('\n')
    test("to_csv has header", 'timestamp' in lines[0])
    test_eq("to_csv data rows", len(lines), 3)  # header + 2 data rows


# ============================================================================
# Log Search Tests
# ============================================================================

def test_search_logs():
    """Test search_logs()."""
    print("\n[search_logs Tests]")
    
    logs = [
        LogEntry(message="Database connection established"),
        LogEntry(message="Database query failed"),
        LogEntry(message="Cache hit"),
        LogEntry(message="Request from user admin"),
    ]
    
    # Simple search
    results = search_logs(logs, 'Database')
    test_eq("search_logs Database", len(results), 2)
    
    # Wildcard search
    results = search_logs(logs, 'user *')
    test_eq("search_logs wildcard", len(results), 1)
    
    # Case insensitive
    results = search_logs(logs, 'database', case_sensitive=False)
    test_eq("search_logs case insensitive", len(results), 2)


def test_extract_field():
    """Test extract_field()."""
    print("\n[extract_field Tests]")
    
    logs = [
        LogEntry(level=LogLevel.INFO, message="m1", source="s1"),
        LogEntry(level=LogLevel.ERROR, message="m2", source="s2"),
        LogEntry(level=LogLevel.WARN, message="m3", source="s3"),
    ]
    
    levels = extract_field(logs, 'level')
    test_eq("extract_field level count", len(levels), 3)
    test_eq("extract_field first level", levels[0], LogLevel.INFO)
    
    messages = extract_field(logs, 'message')
    test_eq("extract_field messages", messages, ['m1', 'm2', 'm3'])


# ============================================================================
# Log Rotation Tests
# ============================================================================

def test_get_log_files():
    """Test get_log_files()."""
    print("\n[get_log_files Tests]")
    
    # Test with current directory (should find mod.py)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    files = get_log_files(current_dir, prefix='', suffix='.py')
    test("get_log_files finds files", len(files) > 0, f"Found {len(files)} files in {current_dir}")
    
    # Test with .log suffix (should find none in this dir)
    log_files = get_log_files(current_dir, suffix='.log')
    test("get_log_files .log suffix ok", isinstance(log_files, list))
    
    # Non-existent directory
    files = get_log_files('/nonexistent/path')
    test_eq("get_log_files nonexistent", len(files), 0)


def test_generate_sample_log():
    """Test generate_sample_log()."""
    print("\n[generate_sample_log Tests]")
    
    logs = generate_sample_log(count=50, start_level=LogLevel.INFO)
    test_eq("generate_sample_log count", len(logs), 50)
    
    # Verify format
    test("generate_sample_log has timestamp", 
         all('202' in log for log in logs))
    test("generate_sample_log has level", 
         any('INFO' in log or 'ERROR' in log or 'WARN' in log for log in logs))


# ============================================================================
# Integration Tests
# ============================================================================

def test_full_pipeline():
    """Test full log processing pipeline."""
    print("\n[Full Pipeline Integration Test]")
    
    # Generate sample logs
    logs = generate_sample_log(count=100)
    
    # Parse logs
    parsed = [parse_log_line(log) for log in logs]
    test("parse all generated logs", all(p is not None for p in parsed))
    
    # Filter by level
    filtered = filter_by_level(parsed, LogLevel.WARN)
    test("filter reduces count", len(filtered) <= len(parsed))
    
    # Count by level
    counts = count_by_level(filtered)
    test("count_by_level returns dict", isinstance(counts, dict))
    
    # Search
    results = search_logs(filtered, 'error', case_sensitive=False)
    test("search returns list", isinstance(results, list))
    
    # Format to JSON
    jsonl = to_json_lines([l for l in filtered if isinstance(l, LogEntry)])
    test("to_json_lines produces output", len(jsonl) > 0)


# ============================================================================
# Main Test Runner
# ============================================================================

def run_all_tests():
    """Run all test suites."""
    print("=" * 60)
    print("  AllToolkit Log Utils - Test Suite")
    print("=" * 60)
    
    # LogLevel tests
    test_log_level_enum()
    test_log_level_from_string()
    test_log_level_from_numeric()
    
    # LogEntry tests
    test_log_entry_class()
    
    # Parsing tests
    test_parse_log_level()
    test_parse_timestamp()
    test_parse_apache_log()
    test_parse_syslog()
    test_parse_json_log()
    test_parse_log_line_auto()
    
    # Filtering tests
    test_filter_by_level()
    test_filter_by_pattern()
    test_filter_by_time_range()
    test_filter_by_source()
    
    # Analysis tests
    test_count_by_level()
    test_count_by_hour()
    test_get_error_summary()
    test_calculate_error_rate()
    test_detect_anomalies()
    
    # Formatting tests
    test_format_log_entry()
    test_to_json_lines()
    test_to_csv()
    
    # Search tests
    test_search_logs()
    test_extract_field()
    
    # Rotation tests
    test_get_log_files()
    test_generate_sample_log()
    
    # Integration tests
    test_full_pipeline()
    
    # Summary
    print("\n" + "=" * 60)
    print(f"  {result.summary()}")
    print("=" * 60)
    
    if result.errors:
        print("\nFailed tests:")
        for name, error in result.errors:
            print(f"  - {name}: {error}")
    
    return result.is_success()


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
