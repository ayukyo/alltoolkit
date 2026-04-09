#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Log Utilities Module
====================================
A comprehensive log processing utility module for Python with zero external dependencies.

Features:
    - Log parsing (multiple formats: Apache, Nginx, Syslog, JSON, custom)
    - Log level management and filtering
    - Log formatting and transformation
    - Log analysis (statistics, aggregation, patterns)
    - Log rotation helpers
    - Log search and extraction
    - Timestamp parsing and normalization

Author: AllToolkit Contributors
License: MIT
"""

import re
import json
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Union, Callable, Tuple, Iterator
from collections import Counter, defaultdict
from enum import Enum
import os


# ============================================================================
# Log Level Enum
# ============================================================================

class LogLevel(Enum):
    """Standard log levels with numeric values."""
    TRACE = 0
    DEBUG = 10
    INFO = 20
    WARN = 30
    WARNING = 30
    ERROR = 40
    CRITICAL = 50
    FATAL = 60
    
    @classmethod
    def from_string(cls, level_str: str) -> 'LogLevel':
        """Parse log level from string."""
        if level_str is None:
            return cls.INFO
        level_upper = level_str.upper().strip()
        # Handle common variations
        level_map = {
            'TRACE': cls.TRACE,
            'DBG': cls.DEBUG,
            'DEBUG': cls.DEBUG,
            'INF': cls.INFO,
            'INFO': cls.INFO,
            'WRN': cls.WARN,
            'WARN': cls.WARN,
            'WARNING': cls.WARNING,
            'ERR': cls.ERROR,
            'ERROR': cls.ERROR,
            'CRT': cls.CRITICAL,
            'CRIT': cls.CRITICAL,
            'CRITICAL': cls.CRITICAL,
            'FATAL': cls.FATAL,
            'EMERG': cls.FATAL,
            'EMERGENCY': cls.FATAL,
        }
        return level_map.get(level_upper, cls.INFO)
    
    @classmethod
    def from_numeric(cls, level_num: int) -> 'LogLevel':
        """Parse log level from numeric value."""
        if level_num <= 0:
            return cls.TRACE
        elif level_num <= 10:
            return cls.DEBUG
        elif level_num <= 20:
            return cls.INFO
        elif level_num <= 30:
            return cls.WARN
        elif level_num <= 40:
            return cls.ERROR
        elif level_num <= 50:
            return cls.CRITICAL
        else:
            return cls.FATAL


# ============================================================================
# Log Entry Data Class
# ============================================================================

class LogEntry:
    """Represents a parsed log entry."""
    
    def __init__(self, 
                 timestamp: Optional[datetime] = None,
                 level: LogLevel = LogLevel.INFO,
                 message: str = "",
                 source: str = "",
                 extra: Optional[Dict[str, Any]] = None):
        self.timestamp = timestamp
        self.level = level
        self.message = message
        self.source = source
        self.extra = extra or {}
    
    def __repr__(self) -> str:
        ts = self.timestamp.strftime('%Y-%m-%d %H:%M:%S') if self.timestamp else 'N/A'
        return f"LogEntry({ts}, {self.level.name}, {self.message[:30]}...)"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'level': self.level.name,
            'message': self.message,
            'source': self.source,
            'extra': self.extra
        }
    
    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict())


# ============================================================================
# Log Parsing Functions
# ============================================================================

def parse_log_level(line: str) -> LogLevel:
    """
    Extract and parse log level from a log line.
    
    Args:
        line: A log line
    
    Returns:
        LogLevel enum value
    
    Example:
        >>> parse_log_level("2024-01-15 10:30:00 ERROR Database connection failed")
        LogLevel.ERROR
    """
    if not line:
        return LogLevel.INFO
    
    # Common log level patterns
    patterns = [
        r'\b(TRACE|DEBUG|INFO|WARN|WARNING|ERROR|CRITICAL|FATAL)\b',
        r'\[(TRACE|DEBUG|INFO|WARN|WARNING|ERROR|CRITICAL|FATAL)\]',
        r'\b(DBG|INF|WRN|ERR|CRT)\b',
        r'\b(level[=:]?\s*)(\d+)\b',  # Numeric levels
    ]
    
    for pattern in patterns:
        match = re.search(pattern, line, re.IGNORECASE)
        if match:
            level_str = match.group(1) if match.lastindex == 1 else match.group(2)
            if level_str.isdigit():
                return LogLevel.from_numeric(int(level_str))
            return LogLevel.from_string(level_str)
    
    return LogLevel.INFO


def parse_timestamp(line: str, 
                    formats: Optional[List[str]] = None) -> Optional[datetime]:
    """
    Extract and parse timestamp from a log line.
    
    Args:
        line: A log line
        formats: List of datetime formats to try (default: common formats)
    
    Returns:
        datetime object or None if not found
    
    Example:
        >>> parse_timestamp("2024-01-15 10:30:00 INFO Starting service")
        datetime(2024, 1, 15, 10, 30, 0)
    """
    if not line:
        return None
    
    default_formats = [
        '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%dT%H:%M:%S',
        '%Y-%m-%dT%H:%M:%SZ',
        '%Y-%m-%dT%H:%M:%S.%f',
        '%Y-%m-%dT%H:%M:%S.%fZ',
        '%d/%b/%Y:%H:%M:%S',  # Apache format
        '%b %d %H:%M:%S',     # Syslog format
        '%Y/%m/%d %H:%M:%S',
        '%d-%m-%Y %H:%M:%S',
        '%m/%d/%Y %H:%M:%S',
        '%Y-%m-%d %H:%M:%S.%f',
    ]
    
    formats = formats or default_formats
    
    # Common timestamp patterns to extract
    patterns = [
        r'(\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(?:\.\d+)?Z?)',
        r'(\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2})',
        r'(\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})',
        r'(\d{4}/\d{2}/\d{2}\s+\d{2}:\d{2}:\d{2})',
        r'(\d{2}-\d{2}-\d{4}\s+\d{2}:\d{2}:\d{2})',
        r'(\d{2}/\d{2}/\d{4}\s+\d{2}:\d{2}:\d{2})',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, line)
        if match:
            ts_str = match.group(1)
            for fmt in formats:
                try:
                    # Handle year-less syslog format
                    if fmt == '%b %d %H:%M:%S':
                        ts_str_with_year = f"{datetime.now().year} {ts_str}"
                        return datetime.strptime(ts_str_with_year, '%Y %b %d %H:%M:%S')
                    return datetime.strptime(ts_str, fmt)
                except ValueError:
                    continue
    
    return None


def parse_apache_log(line: str) -> Optional[Dict[str, Any]]:
    """
    Parse Apache Combined Log Format.
    
    Format: %h %l %u %t "%r" %>s %b "%{Referer}i" "%{User-Agent}i"
    
    Args:
        line: Apache log line
    
    Returns:
        Dictionary with parsed fields or None
    
    Example:
        >>> line = '127.0.0.1 - frank [10/Oct/2000:13:55:36 -0700] "GET /apache_pb.gif HTTP/1.0" 200 2326 "http://www.example.com/start.html" "Mozilla/4.08"'
        >>> parse_apache_log(line)
        {'ip': '127.0.0.1', 'user': 'frank', 'timestamp': ..., 'method': 'GET', ...}
    """
    if not line:
        return None
    
    # Apache Combined Log Format regex
    pattern = r'^(\S+)\s+(\S+)\s+(\S+)\s+\[([^\]]+)\]\s+"([^"]*)"?\s+(\d{3})\s+(\S+)(?:\s+"([^"]*)")?(?:\s+"([^"]*)")?'
    
    match = re.match(pattern, line)
    if not match:
        return None
    
    groups = match.groups()
    request_parts = groups[4].split() if groups[4] else []
    
    return {
        'ip': groups[0],
        'ident': groups[1] if groups[1] != '-' else None,
        'user': groups[2] if groups[2] != '-' else None,
        'timestamp': parse_timestamp(groups[3], ['%d/%b/%Y:%H:%M:%S %z', '%d/%b/%Y:%H:%M:%S']),
        'request': groups[4],
        'method': request_parts[0] if request_parts else None,
        'path': request_parts[1] if len(request_parts) > 1 else None,
        'protocol': request_parts[2] if len(request_parts) > 2 else None,
        'status': int(groups[5]) if groups[5] else None,
        'size': int(groups[6]) if groups[6] != '-' else 0,
        'referer': groups[7] if groups[7] and groups[7] != '-' else None,
        'user_agent': groups[8] if groups[8] else None,
    }


def parse_nginx_log(line: str) -> Optional[Dict[str, Any]]:
    """
    Parse Nginx log format (similar to Apache).
    
    Args:
        line: Nginx log line
    
    Returns:
        Dictionary with parsed fields or None
    """
    return parse_apache_log(line)  # Similar format


def parse_syslog(line: str) -> Optional[Dict[str, Any]]:
    """
    Parse Syslog format (RFC 3164).
    
    Format: <PRI>TIMESTAMP HOSTNAME TAG: MSG
    
    Args:
        line: Syslog line
    
    Returns:
        Dictionary with parsed fields or None
    """
    if not line:
        return None
    
    # Syslog pattern
    pattern = r'^(?:<(\d+)>)?(\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})\s+(\S+)\s+(\S+?)(?:\[(\d+)\])?:\s*(.*)$'
    
    match = re.match(pattern, line)
    if not match:
        return None
    
    groups = match.groups()
    priority = int(groups[0]) if groups[0] else None
    
    return {
        'priority': priority,
        'facility': (priority >> 3) if priority else None,
        'severity': (priority & 7) if priority else None,
        'timestamp': parse_timestamp(groups[1]),
        'hostname': groups[2],
        'tag': groups[3],
        'pid': int(groups[4]) if groups[4] else None,
        'message': groups[5],
    }


def parse_json_log(line: str) -> Optional[Dict[str, Any]]:
    """
    Parse JSON-formatted log line.
    
    Args:
        line: JSON log line
    
    Returns:
        Parsed dictionary or None
    """
    if not line:
        return None
    
    try:
        return json.loads(line.strip())
    except json.JSONDecodeError:
        return None


def parse_log_line(line: str, 
                   log_type: str = 'auto') -> Optional[Union[Dict[str, Any], LogEntry]]:
    """
    Parse a log line (auto-detect or specified format).
    
    Args:
        line: Log line to parse
        log_type: 'auto', 'apache', 'nginx', 'syslog', 'json', 'generic'
    
    Returns:
        Parsed log entry or None
    """
    if not line or not line.strip():
        return None
    
    if log_type == 'auto':
        # Auto-detect format
        stripped = line.strip()
        if stripped.startswith('{') and stripped.endswith('}'):
            log_type = 'json'
        elif re.match(r'^\d+\.\d+\.\d+\.\d+\s', line):
            log_type = 'apache'
        elif re.match(r'^<\d+>', line):
            log_type = 'syslog'
        elif re.match(r'^\w{3}\s+\d+\s+\d+:\d+:\d+', line):
            log_type = 'syslog'
        else:
            log_type = 'generic'
    
    if log_type == 'json':
        return parse_json_log(line)
    elif log_type == 'apache':
        return parse_apache_log(line)
    elif log_type == 'nginx':
        return parse_nginx_log(line)
    elif log_type == 'syslog':
        return parse_syslog(line)
    else:
        # Generic log parsing
        timestamp = parse_timestamp(line)
        level = parse_log_level(line)
        
        # Extract message (remove timestamp and level)
        message = line.strip()
        for pattern in [
            r'^\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(?:\.\d+)?Z?\s*',
            r'^\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}\s*',
            r'^(TRACE|DEBUG|INFO|WARN|WARNING|ERROR|CRITICAL|FATAL)\s*',
        ]:
            message = re.sub(pattern, '', message, flags=re.IGNORECASE)
        
        return LogEntry(
            timestamp=timestamp,
            level=level,
            message=message.strip()
        )


# ============================================================================
# Log Filtering Functions
# ============================================================================

def filter_by_level(logs: List[Union[str, Dict, LogEntry]], 
                    min_level: Union[str, LogLevel, int] = 'INFO') -> List:
    """
    Filter logs by minimum log level.
    
    Args:
        logs: List of log lines, dicts, or LogEntry objects
        min_level: Minimum level to include ('INFO', LogLevel.INFO, or 20)
    
    Returns:
        Filtered list of logs
    
    Example:
        >>> logs = ["DEBUG test", "INFO test", "ERROR test"]
        >>> filter_by_level(logs, 'INFO')
        ['INFO test', 'ERROR test']
    """
    if isinstance(min_level, str):
        min_level = LogLevel.from_string(min_level)
    elif isinstance(min_level, int):
        min_level = LogLevel.from_numeric(min_level)
    
    result = []
    for log in logs:
        if isinstance(log, LogEntry):
            log_level = log.level
        elif isinstance(log, dict):
            log_level = LogLevel.from_string(log.get('level', 'INFO'))
        else:
            log_level = parse_log_level(str(log))
        
        if log_level.value >= min_level.value:
            result.append(log)
    
    return result


def filter_by_time_range(logs: List[Union[str, Dict, LogEntry]],
                         start_time: Optional[datetime] = None,
                         end_time: Optional[datetime] = None) -> List:
    """
    Filter logs by time range.
    
    Args:
        logs: List of log entries
        start_time: Start of time range (inclusive)
        end_time: End of time range (inclusive)
    
    Returns:
        Filtered list of logs
    """
    result = []
    for log in logs:
        timestamp = None
        if isinstance(log, LogEntry):
            timestamp = log.timestamp
        elif isinstance(log, dict):
            if 'timestamp' in log:
                ts = log['timestamp']
                if isinstance(ts, datetime):
                    timestamp = ts
                elif isinstance(ts, str):
                    timestamp = parse_timestamp(ts)
        else:
            timestamp = parse_timestamp(str(log))
        
        if timestamp is None:
            continue
        
        if start_time and timestamp < start_time:
            continue
        if end_time and timestamp > end_time:
            continue
        
        result.append(log)
    
    return result


def filter_by_pattern(logs: List[Union[str, Dict, LogEntry]], 
                      pattern: str,
                      case_sensitive: bool = False) -> List:
    """
    Filter logs by regex pattern.
    
    Args:
        logs: List of log entries
        pattern: Regex pattern to match
        case_sensitive: Whether matching is case-sensitive
    
    Returns:
        Filtered list of logs
    """
    flags = 0 if case_sensitive else re.IGNORECASE
    regex = re.compile(pattern, flags)
    
    result = []
    for log in logs:
        text = str(log)
        if isinstance(log, dict):
            text = json.dumps(log)
        elif isinstance(log, LogEntry):
            text = log.message
        
        if regex.search(text):
            result.append(log)
    
    return result


def filter_by_source(logs: List[Union[str, Dict, LogEntry]], 
                     sources: Union[str, List[str]]) -> List:
    """
    Filter logs by source/tag.
    
    Args:
        logs: List of log entries
        sources: Source name or list of source names
    
    Returns:
        Filtered list of logs
    """
    if isinstance(sources, str):
        sources = [sources]
    
    sources_lower = [s.lower() for s in sources]
    
    result = []
    for log in logs:
        source = None
        if isinstance(log, LogEntry):
            source = log.source
        elif isinstance(log, dict):
            source = log.get('source') or log.get('tag') or log.get('logger')
        
        if source and source.lower() in sources_lower:
            result.append(log)
    
    return result


# ============================================================================
# Log Analysis Functions
# ============================================================================

def count_by_level(logs: List[Union[str, Dict, LogEntry]]) -> Dict[str, int]:
    """
    Count logs by level.
    
    Args:
        logs: List of log entries
    
    Returns:
        Dictionary mapping level names to counts
    """
    counter = Counter()
    for log in logs:
        if isinstance(log, LogEntry):
            level = log.level.name
        elif isinstance(log, dict):
            level = log.get('level', 'UNKNOWN')
        else:
            level = parse_log_level(str(log)).name
        counter[level] += 1
    
    return dict(counter)


def count_by_hour(logs: List[Union[str, Dict, LogEntry]]) -> Dict[int, int]:
    """
    Count logs by hour of day.
    
    Args:
        logs: List of log entries
    
    Returns:
        Dictionary mapping hour (0-23) to counts
    """
    counter = Counter()
    for log in logs:
        timestamp = None
        if isinstance(log, LogEntry):
            timestamp = log.timestamp
        elif isinstance(log, dict):
            ts = log.get('timestamp')
            if isinstance(ts, datetime):
                timestamp = ts
            elif isinstance(ts, str):
                timestamp = parse_timestamp(ts)
        else:
            timestamp = parse_timestamp(str(log))
        
        if timestamp:
            counter[timestamp.hour] += 1
    
    return dict(counter)


def get_error_summary(logs: List[Union[str, Dict, LogEntry]], 
                      top_n: int = 10) -> List[Tuple[str, int]]:
    """
    Get summary of most common error messages.
    
    Args:
        logs: List of log entries
        top_n: Number of top errors to return
    
    Returns:
        List of (message, count) tuples
    """
    error_logs = filter_by_level(logs, LogLevel.ERROR)
    
    counter = Counter()
    for log in error_logs:
        if isinstance(log, LogEntry):
            msg = log.message[:100]  # Truncate long messages
        elif isinstance(log, dict):
            msg = log.get('message', str(log))[:100]
        else:
            msg = str(log)[:100]
        counter[msg] += 1
    
    return counter.most_common(top_n)


def calculate_error_rate(logs: List[Union[str, Dict, LogEntry]]) -> float:
    """
    Calculate error rate (errors / total logs).
    
    Args:
        logs: List of log entries
    
    Returns:
        Error rate as a float (0.0 to 1.0)
    """
    if not logs:
        return 0.0
    
    error_count = len(filter_by_level(logs, LogLevel.ERROR))
    return error_count / len(logs)


def detect_anomalies(logs: List[Union[str, Dict, LogEntry]],
                     window_size: int = 60,
                     threshold_multiplier: float = 3.0) -> List[datetime]:
    """
    Detect anomaly spikes in log volume.
    
    Args:
        logs: List of log entries with timestamps
        window_size: Window size in minutes
        threshold_multiplier: Standard deviations above mean to flag as anomaly
    
    Returns:
        List of anomaly timestamps
    """
    # Group logs by minute
    minute_counts = defaultdict(int)
    for log in logs:
        timestamp = None
        if isinstance(log, LogEntry):
            timestamp = log.timestamp
        elif isinstance(log, dict):
            ts = log.get('timestamp')
            if isinstance(ts, datetime):
                timestamp = ts
        else:
            timestamp = parse_timestamp(str(log))
        
        if timestamp:
            minute_key = timestamp.replace(second=0, microsecond=0)
            minute_counts[minute_key] += 1
    
    if not minute_counts:
        return []
    
    counts = list(minute_counts.values())
    mean_count = sum(counts) / len(counts)
    variance = sum((c - mean_count) ** 2 for c in counts) / len(counts)
    std_dev = variance ** 0.5
    
    threshold = mean_count + (threshold_multiplier * std_dev)
    
    anomalies = []
    for minute, count in minute_counts.items():
        if count > threshold:
            anomalies.append(minute)
    
    return sorted(anomalies)


# ============================================================================
# Log Formatting Functions
# ============================================================================

def format_log_entry(entry: LogEntry, 
                     format_str: str = '%(timestamp)s %(level)s %(message)s') -> str:
    """
    Format a log entry using a format string.
    
    Args:
        entry: LogEntry object
        format_str: Format string with placeholders
    
    Returns:
        Formatted log string
    
    Placeholders:
        %(timestamp)s - Timestamp
        %(level)s - Log level
        %(message)s - Message
        %(source)s - Source
    """
    replacements = {
        'timestamp': entry.timestamp.strftime('%Y-%m-%d %H:%M:%S') if entry.timestamp else 'N/A',
        'level': entry.level.name,
        'message': entry.message,
        'source': entry.source,
    }
    
    result = format_str
    for key, value in replacements.items():
        result = result.replace(f'%({key})s', value)
    
    return result


def to_json_lines(logs: List[Union[Dict, LogEntry]]) -> str:
    """
    Convert logs to JSON Lines format.
    
    Args:
        logs: List of log entries
    
    Returns:
        JSON Lines string
    """
    lines = []
    for log in logs:
        if isinstance(log, LogEntry):
            lines.append(log.to_json())
        elif isinstance(log, dict):
            lines.append(json.dumps(log))
        else:
            lines.append(json.dumps({'message': str(log)}))
    
    return '\n'.join(lines)


def to_csv(logs: List[Union[Dict, LogEntry]], 
           columns: Optional[List[str]] = None) -> str:
    """
    Convert logs to CSV format.
    
    Args:
        logs: List of log entries
        columns: Column names to include
    
    Returns:
        CSV string
    """
    if not logs:
        return ''
    
    default_columns = ['timestamp', 'level', 'message', 'source']
    columns = columns or default_columns
    
    lines = []
    # Header
    lines.append(','.join(columns))
    
    # Data rows
    for log in logs:
        row = []
        for col in columns:
            if isinstance(log, LogEntry):
                value = getattr(log, col, '')
                if col == 'timestamp' and value:
                    value = value.strftime('%Y-%m-%d %H:%M:%S')
                elif col == 'level':
                    value = value.name
            elif isinstance(log, dict):
                value = log.get(col, '')
                if isinstance(value, datetime):
                    value = value.strftime('%Y-%m-%d %H:%M:%S')
            else:
                value = str(log)
            
            # Escape CSV special characters
            value = str(value).replace('"', '""')
            if ',' in value or '"' in value or '\n' in value:
                value = f'"{value}"'
            row.append(value)
        
        lines.append(','.join(row))
    
    return '\n'.join(lines)


# ============================================================================
# Log Search Functions
# ============================================================================

def search_logs(logs: List[Union[str, Dict, LogEntry]],
                query: str,
                fields: Optional[List[str]] = None,
                case_sensitive: bool = False) -> List:
    """
    Search logs for a query string.
    
    Args:
        logs: List of log entries
        query: Search query
        fields: Fields to search (default: all)
        case_sensitive: Case-sensitive search
    
    Returns:
        Matching logs
    """
    flags = 0 if case_sensitive else re.IGNORECASE
    
    # Escape special regex characters in query
    escaped_query = re.escape(query)
    # Allow wildcard matching
    escaped_query = escaped_query.replace(r'\*', '.*')
    pattern = re.compile(escaped_query, flags)
    
    result = []
    for log in logs:
        text_to_search = ''
        
        if isinstance(log, LogEntry):
            if fields is None:
                text_to_search = f"{log.message} {log.source}"
            else:
                for field in fields:
                    text_to_search += f" {getattr(log, field, '')}"
        elif isinstance(log, dict):
            if fields is None:
                text_to_search = json.dumps(log)
            else:
                for field in fields:
                    text_to_search += f" {log.get(field, '')}"
        else:
            text_to_search = str(log)
        
        if pattern.search(text_to_search):
            result.append(log)
    
    return result


def extract_field(logs: List[Union[Dict, LogEntry]], 
                  field: str) -> List[Any]:
    """
    Extract a specific field from logs.
    
    Args:
        logs: List of log entries
        field: Field name to extract
    
    Returns:
        List of field values
    """
    result = []
    for log in logs:
        if isinstance(log, dict):
            if field in log:
                result.append(log[field])
        elif isinstance(log, LogEntry):
            if field == 'timestamp':
                result.append(log.timestamp)
            elif field == 'level':
                result.append(log.level)
            elif field == 'message':
                result.append(log.message)
            elif field == 'source':
                result.append(log.source)
            elif field in log.extra:
                result.append(log.extra[field])
    
    return result


# ============================================================================
# Log Rotation Helpers
# ============================================================================

def get_log_files(directory: str, 
                  prefix: str = '', 
                  suffix: str = '.log') -> List[str]:
    """
    Get list of log files in a directory.
    
    Args:
        directory: Directory path
        prefix: Filename prefix filter
        suffix: Filename suffix filter
    
    Returns:
        List of log file paths
    """
    if not os.path.isdir(directory):
        return []
    
    log_files = []
    for filename in os.listdir(directory):
        if filename.startswith(prefix) and filename.endswith(suffix):
            log_files.append(os.path.join(directory, filename))
    
    return sorted(log_files)


def get_file_size(filepath: str) -> int:
    """
    Get file size in bytes.
    
    Args:
        filepath: File path
    
    Returns:
        File size in bytes
    """
    try:
        return os.path.getsize(filepath)
    except OSError:
        return 0


def get_file_age_days(filepath: str) -> float:
    """
    Get file age in days.
    
    Args:
        filepath: File path
    
    Returns:
        File age in days
    """
    try:
        mtime = os.path.getmtime(filepath)
        age_seconds = datetime.now().timestamp() - mtime
        return age_seconds / (24 * 60 * 60)
    except OSError:
        return 0


def find_rotation_candidates(directory: str,
                             max_size_mb: float = 100,
                             max_age_days: int = 30,
                             prefix: str = '',
                             suffix: str = '.log') -> List[Dict[str, Any]]:
    """
    Find log files that are candidates for rotation.
    
    Args:
        directory: Directory to scan
        max_size_mb: Maximum file size in MB
        max_age_days: Maximum file age in days
        prefix: Filename prefix
        suffix: Filename suffix
    
    Returns:
        List of candidate files with metadata
    """
    candidates = []
    max_size_bytes = max_size_mb * 1024 * 1024
    
    log_files = get_log_files(directory, prefix, suffix)
    
    for filepath in log_files:
        size = get_file_size(filepath)
        age = get_file_age_days(filepath)
        
        needs_rotation = size > max_size_bytes or age > max_age_days
        
        if needs_rotation:
            candidates.append({
                'path': filepath,
                'size_bytes': size,
                'size_mb': size / (1024 * 1024),
                'age_days': age,
                'reason': [] if not needs_rotation else (
                    ['size'] if size > max_size_bytes else []
                ) + (['age'] if age > max_age_days else [])
            })
    
    return candidates


# ============================================================================
# Utility Functions
# ============================================================================

def tail_log(filepath: str, lines: int = 10) -> List[str]:
    """
    Read the last N lines of a log file (efficient for large files).
    
    Args:
        filepath: Log file path
        lines: Number of lines to read
    
    Returns:
        List of last N lines
    """
    if not os.path.isfile(filepath):
        return []
    
    with open(filepath, 'rb') as f:
        # Go to end of file
        f.seek(0, 2)
        file_size = f.tell()
        
        if file_size == 0:
            return []
        
        # Read backwards
        buffer_size = 4096
        buffer = b''
        lines_found = 0
        
        while lines_found <= lines and file_size > 0:
            read_size = min(buffer_size, file_size)
            f.seek(file_size - read_size)
            buffer = f.read(read_size) + buffer
            lines_found = buffer.count(b'\n')
            file_size -= read_size
        
        # Split and return last N lines
        all_lines = buffer.decode('utf-8', errors='ignore').splitlines()
        return all_lines[-lines:] if len(all_lines) > lines else all_lines


def merge_log_files(filepaths: List[str], 
                    output_path: Optional[str] = None,
                    sort_by_time: bool = True) -> Union[str, List[str]]:
    """
    Merge multiple log files.
    
    Args:
        filepaths: List of log file paths
        output_path: Output file path (optional, returns string if None)
        sort_by_time: Sort merged logs by timestamp
    
    Returns:
        Merged log content (string or written to file)
    """
    all_lines = []
    
    for filepath in filepaths:
        if os.path.isfile(filepath):
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                all_lines.extend(f.readlines())
    
    if sort_by_time:
        # Try to sort by extracted timestamp
        def get_timestamp(line):
            ts = parse_timestamp(line)
            return ts if ts else datetime.min
        
        all_lines.sort(key=get_timestamp)
    
    merged = ''.join(all_lines)
    
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(merged)
        return output_path
    
    return merged


def generate_sample_log(count: int = 100,
                        start_level: LogLevel = LogLevel.DEBUG) -> List[str]:
    """
    Generate sample log entries for testing.
    
    Args:
        count: Number of log entries to generate
        start_level: Minimum log level
    
    Returns:
        List of sample log lines
    """
    import random
    
    levels = [lvl for lvl in LogLevel if lvl.value >= start_level.value]
    messages = [
        "Application started successfully",
        "Processing request from user",
        "Database connection established",
        "Cache miss for key",
        "Request completed in {ms}ms",
        "Warning: High memory usage detected",
        "Error: Failed to connect to service",
        "Debug: Variable state dump",
        "Info: Configuration loaded",
        "Critical: System shutdown initiated",
    ]
    
    logs = []
    base_time = datetime.now() - timedelta(hours=1)
    
    for i in range(count):
        level = random.choice(levels)
        message = random.choice(messages).format(ms=random.randint(10, 5000))
        timestamp = base_time + timedelta(seconds=i * 30)
        
        log_line = f"{timestamp.strftime('%Y-%m-%d %H:%M:%S')} {level.name} {message}"
        logs.append(log_line)
    
    return logs


# ============================================================================
# Module Constants
# ============================================================================

__version__ = '1.0.0'
__all__ = [
    # Classes
    'LogLevel',
    'LogEntry',
    # Parsing
    'parse_log_level',
    'parse_timestamp',
    'parse_apache_log',
    'parse_nginx_log',
    'parse_syslog',
    'parse_json_log',
    'parse_log_line',
    # Filtering
    'filter_by_level',
    'filter_by_time_range',
    'filter_by_pattern',
    'filter_by_source',
    # Analysis
    'count_by_level',
    'count_by_hour',
    'get_error_summary',
    'calculate_error_rate',
    'detect_anomalies',
    # Formatting
    'format_log_entry',
    'to_json_lines',
    'to_csv',
    # Search
    'search_logs',
    'extract_field',
    # Rotation
    'get_log_files',
    'get_file_size',
    'get_file_age_days',
    'find_rotation_candidates',
    # Utilities
    'tail_log',
    'merge_log_files',
    'generate_sample_log',
]
