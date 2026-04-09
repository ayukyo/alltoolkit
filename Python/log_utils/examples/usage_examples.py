#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit Log Utils - Usage Examples
=======================================
Demonstrates common use cases for the log utilities module.
"""

import sys
import os
from datetime import datetime, timedelta

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from mod import (
    LogLevel, LogEntry,
    parse_log_level, parse_timestamp, parse_apache_log, parse_syslog,
    parse_json_log, parse_log_line,
    filter_by_level, filter_by_time_range, filter_by_pattern, filter_by_source,
    count_by_level, count_by_hour, get_error_summary, calculate_error_rate,
    detect_anomalies, format_log_entry, to_json_lines, to_csv,
    search_logs, extract_field,
    generate_sample_log, tail_log
)


def print_section(title):
    """Print a section header."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)


def example_parsing():
    """Example: Log Parsing"""
    print_section("Log Parsing Examples")
    
    # Generic log parsing
    print("\n1. Generic Log Parsing:")
    line = "2024-01-15 10:30:45 ERROR Database connection failed"
    entry = parse_log_line(line)
    print(f"   Input:  {line}")
    print(f"   Level:  {entry.level.name}")
    print(f"   Time:   {entry.timestamp}")
    print(f"   Message: {entry.message}")
    
    # Apache log parsing
    print("\n2. Apache Log Parsing:")
    apache_line = '127.0.0.1 - frank [10/Oct/2000:13:55:36 -0700] "GET /apache_pb.gif HTTP/1.0" 200 2326 "http://www.example.com/" "Mozilla/4.08"'
    parsed = parse_apache_log(apache_line)
    print(f"   IP:      {parsed['ip']}")
    print(f"   User:    {parsed['user']}")
    print(f"   Method:  {parsed['method']}")
    print(f"   Path:    {parsed['path']}")
    print(f"   Status:  {parsed['status']}")
    print(f"   Size:    {parsed['size']} bytes")
    
    # Syslog parsing
    print("\n3. Syslog Parsing:")
    syslog_line = '<13>Jan 15 10:30:45 myhost myapp[1234]: System started'
    parsed = parse_syslog(syslog_line)
    print(f"   Priority: {parsed['priority']}")
    print(f"   Hostname: {parsed['hostname']}")
    print(f"   Tag:      {parsed['tag']}")
    print(f"   PID:      {parsed['pid']}")
    print(f"   Message:  {parsed['message']}")
    
    # JSON log parsing
    print("\n4. JSON Log Parsing:")
    json_line = '{"timestamp": "2024-01-15T10:30:45", "level": "WARN", "message": "High memory usage", "service": "api"}'
    parsed = parse_json_log(json_line)
    print(f"   Level:   {parsed['level']}")
    print(f"   Message: {parsed['message']}")
    print(f"   Service: {parsed['service']}")


def example_filtering():
    """Example: Log Filtering"""
    print_section("Log Filtering Examples")
    
    # Generate sample logs
    logs = generate_sample_log(count=20)
    parsed = [parse_log_line(line) for line in logs]
    
    # Filter by level
    print("\n1. Filter by Level (WARNING and above):")
    filtered = filter_by_level(parsed, LogLevel.WARN)
    print(f"   Original: {len(parsed)} logs")
    print(f"   Filtered: {len(filtered)} logs")
    for log in filtered[:3]:
        print(f"   - {log.level.name}: {log.message[:40]}...")
    
    # Filter by pattern
    print("\n2. Filter by Pattern (containing 'error' or 'failed'):")
    filtered = filter_by_pattern(parsed, r'(error|failed)', case_sensitive=False)
    print(f"   Found: {len(filtered)} logs")
    for log in filtered[:3]:
        print(f"   - {log.message[:50]}...")
    
    # Filter by time range
    print("\n3. Filter by Time Range (last 10 minutes):")
    now = datetime.now()
    filtered = filter_by_time_range(parsed, start_time=now - timedelta(minutes=10))
    print(f"   Found: {len(filtered)} logs in last 10 minutes")


def example_analysis():
    """Example: Log Analysis"""
    print_section("Log Analysis Examples")
    
    # Generate sample logs
    logs = generate_sample_log(count=100)
    parsed = [parse_log_line(line) for line in logs]
    
    # Count by level
    print("\n1. Count by Level:")
    counts = count_by_level(parsed)
    for level, count in sorted(counts.items()):
        bar = '█' * (count // 2)
        print(f"   {level:10} {count:3} {bar}")
    
    # Count by hour
    print("\n2. Count by Hour:")
    hourly = count_by_hour(parsed)
    for hour in sorted(hourly.keys()):
        count = hourly[hour]
        bar = '█' * (count // 2)
        print(f"   {hour:02d}:00  {count:3} {bar}")
    
    # Error rate
    print("\n3. Error Rate:")
    error_rate = calculate_error_rate(parsed)
    print(f"   Error Rate: {error_rate:.2%}")
    
    # Top errors
    print("\n4. Top Error Messages:")
    top_errors = get_error_summary(parsed, top_n=5)
    for i, (msg, count) in enumerate(top_errors, 1):
        print(f"   {i}. ({count}x) {msg[:50]}...")


def example_search():
    """Example: Log Search"""
    print_section("Log Search Examples")
    
    # Generate sample logs
    logs = generate_sample_log(count=50)
    parsed = [parse_log_line(line) for line in logs]
    
    # Simple search
    print("\n1. Simple Search ('Database'):")
    results = search_logs(parsed, 'Database')
    print(f"   Found: {len(results)} logs")
    for log in results[:3]:
        print(f"   - {log.message}")
    
    # Wildcard search
    print("\n2. Wildcard Search ('Request * completed'):")
    results = search_logs(parsed, 'Request * completed')
    print(f"   Found: {len(results)} logs")
    for log in results[:3]:
        print(f"   - {log.message}")
    
    # Extract field
    print("\n3. Extract Levels:")
    levels = extract_field(parsed, 'level')
    print(f"   First 10 levels: {[l.name for l in levels[:10]]}")


def example_formatting():
    """Example: Log Formatting"""
    print_section("Log Formatting Examples")
    
    # Create sample entries
    entries = [
        LogEntry(
            timestamp=datetime(2024, 1, 15, 10, 30, 0),
            level=LogLevel.ERROR,
            message="Database connection failed",
            source="db_service"
        ),
        LogEntry(
            timestamp=datetime(2024, 1, 15, 10, 31, 0),
            level=LogLevel.INFO,
            message="Retrying connection...",
            source="db_service"
        ),
        LogEntry(
            timestamp=datetime(2024, 1, 15, 10, 32, 0),
            level=LogLevel.INFO,
            message="Connection established",
            source="db_service"
        ),
    ]
    
    # Custom format
    print("\n1. Custom Format:")
    for entry in entries:
        formatted = format_log_entry(entry, '[%(timestamp)s] %(level)s %(source)s: %(message)s')
        print(f"   {formatted}")
    
    # JSON Lines
    print("\n2. JSON Lines Format:")
    jsonl = to_json_lines(entries)
    for line in jsonl.split('\n')[:2]:
        print(f"   {line[:80]}...")
    
    # CSV Format
    print("\n3. CSV Format:")
    csv_data = to_csv(entries, columns=['timestamp', 'level', 'source', 'message'])
    for line in csv_data.split('\n'):
        print(f"   {line}")


def example_anomaly_detection():
    """Example: Anomaly Detection"""
    print_section("Anomaly Detection Examples")
    
    # Create logs with anomaly spike
    base = datetime.now() - timedelta(hours=1)
    logs = []
    
    # Normal: 2 logs per minute for 30 minutes
    for i in range(30):
        for j in range(2):
            logs.append(LogEntry(
                timestamp=base + timedelta(minutes=i, seconds=j*10),
                level=LogLevel.INFO,
                message="Normal operation"
            ))
    
    # Anomaly: 50 logs in one minute
    for i in range(50):
        logs.append(LogEntry(
            timestamp=base + timedelta(minutes=35, seconds=i),
            level=LogLevel.ERROR,
            message="Spike event"
        ))
    
    # Detect anomalies
    anomalies = detect_anomalies(logs, threshold_multiplier=2.0)
    
    print(f"\n   Total logs: {len(logs)}")
    print(f"   Anomalies detected: {len(anomalies)}")
    for anomaly in anomalies:
        print(f"   - { anomaly.strftime('%Y-%m-%d %H:%M:%S') }")


def example_real_world():
    """Example: Real-world Scenarios"""
    print_section("Real-world Scenarios")
    
    # Scenario 1: Log health check
    print("\n1. Log Health Check:")
    logs = generate_sample_log(count=200)
    parsed = [parse_log_line(line) for line in logs]
    
    error_rate = calculate_error_rate(parsed)
    level_counts = count_by_level(parsed)
    
    print(f"   Total Logs: {len(parsed)}")
    print(f"   Error Rate: {error_rate:.2%}")
    print(f"   Status: {'⚠️ WARNING' if error_rate > 0.05 else '✅ HEALTHY'}")
    
    # Scenario 2: Service log summary
    print("\n2. Service Log Summary:")
    logs_with_source = [
        LogEntry(level=LogLevel.INFO, message="Request processed", source="api"),
        LogEntry(level=LogLevel.ERROR, message="DB timeout", source="db"),
        LogEntry(level=LogLevel.INFO, message="Cache hit", source="cache"),
        LogEntry(level=LogLevel.ERROR, message="Auth failed", source="api"),
        LogEntry(level=LogLevel.WARN, message="Slow query", source="db"),
    ]
    
    by_source = {}
    for log in logs_with_source:
        if log.source not in by_source:
            by_source[log.source] = {'total': 0, 'errors': 0}
        by_source[log.source]['total'] += 1
        if log.level.value >= LogLevel.ERROR.value:
            by_source[log.source]['errors'] += 1
    
    for source, stats in by_source.items():
        print(f"   {source}: {stats['total']} total, {stats['errors']} errors")


def main():
    """Run all examples."""
    print("=" * 60)
    print("  AllToolkit Log Utils - Usage Examples")
    print("=" * 60)
    
    example_parsing()
    example_filtering()
    example_analysis()
    example_search()
    example_formatting()
    example_anomaly_detection()
    example_real_world()
    
    print("\n" + "=" * 60)
    print("  Examples completed!")
    print("=" * 60)


if __name__ == '__main__':
    main()
