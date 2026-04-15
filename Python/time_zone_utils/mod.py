"""
AllToolkit - Python Time Zone Utilities

A zero-dependency, production-ready time zone conversion module.
Provides time zone conversion, offset calculation, DST detection,
timezone listing, and meeting time finder.
Built entirely with Python standard library (datetime).

Compatible with Python 3.6+. Uses fixed UTC offsets for common timezones.
For full IANA timezone support, use Python 3.9+ with zoneinfo version.

Author: AllToolkit
License: MIT
"""

from datetime import datetime, timedelta, timezone as dt_timezone
from typing import List, Tuple, Optional, Dict, Any, Union


class TimeZoneError(Exception):
    """Base exception for timezone operations."""
    pass


class InvalidTimeZoneError(TimeZoneError):
    """Raised when timezone identifier is invalid."""
    pass


class InvalidTimeError(TimeZoneError):
    """Raised when time value is invalid."""
    pass


# ============================================================================
# Timezone Database (Fixed Offsets)
# ============================================================================

# Common timezone definitions with UTC offsets
# Format: "IANA_Name": (offset_hours, offset_minutes, has_dst, dst_offset_hours)
# Note: This is a simplified implementation using fixed offsets
# For production use with full DST support, upgrade to Python 3.9+

TIMEZONE_DATABASE = {
    # UTC
    "UTC": (0, 0, False, 0),
    "Etc/UTC": (0, 0, False, 0),
    
    # Asia
    "Asia/Shanghai": (8, 0, False, 0),
    "Asia/Chongqing": (8, 0, False, 0),
    "Asia/Hong_Kong": (8, 0, False, 0),
    "Asia/Taipei": (8, 0, False, 0),
    "Asia/Singapore": (8, 0, False, 0),
    "Asia/Kuala_Lumpur": (8, 0, False, 0),
    "Asia/Tokyo": (9, 0, False, 0),
    "Asia/Seoul": (9, 0, False, 0),
    "Asia/Pyongyang": (9, 0, False, 0),
    "Asia/Bangkok": (7, 0, False, 0),
    "Asia/Ho_Chi_Minh": (7, 0, False, 0),
    "Asia/Jakarta": (7, 0, False, 0),
    "Asia/Manila": (8, 0, False, 0),
    "Asia/Kolkata": (5, 30, False, 0),  # India
    "Asia/Colombo": (5, 30, False, 0),
    "Asia/Kathmandu": (5, 45, False, 0),  # Nepal
    "Asia/Dubai": (4, 0, False, 0),
    "Asia/Muscat": (4, 0, False, 0),
    "Asia/Tehran": (3, 30, True, 4.5),  # Iran has DST
    "Asia/Riyadh": (3, 0, False, 0),
    "Asia/Jerusalem": (2, 0, True, 3),  # Israel has DST
    "Asia/Amman": (2, 0, True, 3),
    "Asia/Baghdad": (3, 0, False, 0),
    "Asia/Karachi": (5, 0, False, 0),
    "Asia/Dhaka": (6, 0, False, 0),
    "Asia/Yangon": (6, 30, False, 0),
    "Asia/Phnom_Penh": (7, 0, False, 0),
    "Asia/Vientiane": (7, 0, False, 0),
    
    # Europe
    "Europe/London": (0, 0, True, 1),  # GMT/BST
    "Europe/Dublin": (0, 0, True, 1),
    "Europe/Paris": (1, 0, True, 2),  # CET/CEST
    "Europe/Berlin": (1, 0, True, 2),
    "Europe/Rome": (1, 0, True, 2),
    "Europe/Madrid": (1, 0, True, 2),
    "Europe/Amsterdam": (1, 0, True, 2),
    "Europe/Brussels": (1, 0, True, 2),
    "Europe/Vienna": (1, 0, True, 2),
    "Europe/Stockholm": (1, 0, True, 2),
    "Europe/Oslo": (1, 0, True, 2),
    "Europe/Copenhagen": (1, 0, True, 2),
    "Europe/Warsaw": (1, 0, True, 2),
    "Europe/Prague": (1, 0, True, 2),
    "Europe/Budapest": (1, 0, True, 2),
    "Europe/Athens": (2, 0, True, 3),  # EET/EEST
    "Europe/Helsinki": (2, 0, True, 3),
    "Europe/Kiev": (2, 0, True, 3),
    "Europe/Bucharest": (2, 0, True, 3),
    "Europe/Sofia": (2, 0, True, 3),
    "Europe/Istanbul": (3, 0, False, 0),  # Turkey no longer uses DST
    "Europe/Moscow": (3, 0, False, 0),
    "Europe/Minsk": (3, 0, False, 0),
    
    # Africa
    "Africa/Cairo": (2, 0, False, 0),
    "Africa/Johannesburg": (2, 0, False, 0),
    "Africa/Lagos": (1, 0, False, 0),
    "Africa/Nairobi": (3, 0, False, 0),
    "Africa/Casablanca": (1, 0, True, 1),
    "Africa/Addis_Ababa": (3, 0, False, 0),
    
    # Americas
    "America/New_York": (-5, 0, True, -4),  # EST/EDT
    "America/Washington": (-5, 0, True, -4),
    "America/Boston": (-5, 0, True, -4),
    "America/Miami": (-5, 0, True, -4),
    "America/Atlanta": (-5, 0, True, -4),
    "America/Detroit": (-5, 0, True, -4),
    "America/Chicago": (-6, 0, True, -5),  # CST/CDT
    "America/Dallas": (-6, 0, True, -5),
    "America/Houston": (-6, 0, True, -5),
    "America/Minneapolis": (-6, 0, True, -5),
    "America/Denver": (-7, 0, True, -6),  # MST/MDT
    "America/Phoenix": (-7, 0, False, 0),  # Arizona no DST
    "America/Los_Angeles": (-8, 0, True, -7),  # PST/PDT
    "America/San_Francisco": (-8, 0, True, -7),
    "America/Seattle": (-8, 0, True, -7),
    "America/Portland": (-8, 0, True, -7),
    "America/Anchorage": (-9, 0, True, -8),
    "America/Honolulu": (-10, 0, False, 0),  # Hawaii
    "America/Toronto": (-5, 0, True, -4),
    "America/Montreal": (-5, 0, True, -4),
    "America/Vancouver": (-8, 0, True, -7),
    "America/Mexico_City": (-6, 0, True, -5),
    "America/Sao_Paulo": (-3, 0, False, 0),  # Brazil no longer uses DST
    "America/Buenos_Aires": (-3, 0, False, 0),
    "America/Santiago": (-4, 0, True, -3),
    "America/Lima": (-5, 0, False, 0),
    "America/Bogota": (-5, 0, False, 0),
    "America/Caracas": (-4, 0, False, 0),
    
    # Pacific
    "Australia/Sydney": (10, 0, True, 11),  # AEST/AEDT
    "Australia/Melbourne": (10, 0, True, 11),
    "Australia/Brisbane": (10, 0, False, 0),
    "Australia/Perth": (8, 0, False, 0),
    "Australia/Adelaide": (9, 30, True, 10.5),
    "Australia/Darwin": (9, 30, False, 0),
    "Pacific/Auckland": (12, 0, True, 13),  # NZST/NZDT
    "Pacific/Fiji": (12, 0, True, 13),
    "Pacific/Guam": (10, 0, False, 0),
    "Pacific/Port_Moresby": (10, 0, False, 0),
    "Pacific/Honolulu": (-10, 0, False, 0),
    "Pacific/Tahiti": (-10, 0, False, 0),
    "Pacific/Marquesas": (-9, -30, False, 0),  # -9:30
    "Pacific/Gambier": (-9, 0, False, 0),
    "Pacific/Pitcairn": (-8, 0, False, 0),
    "Pacific/Easter": (-6, 0, True, -5),
    "Pacific/Galapagos": (-6, 0, False, 0),
}


def _get_timezone_info(tz_name: str) -> Tuple[int, int, bool, float]:
    """
    Get timezone information from database.
    
    Returns:
        Tuple of (offset_hours, offset_minutes, has_dst, dst_offset)
    """
    if tz_name not in TIMEZONE_DATABASE:
        raise InvalidTimeZoneError(f"Unknown timezone: {tz_name}")
    return TIMEZONE_DATABASE[tz_name]


# 预定义的时区分类集合，避免每次调用时创建列表
_SOUTHERN_HEMISPHERE_TZ = frozenset([
    "Australia/Sydney", "Australia/Melbourne", "Australia/Adelaide",
    "Pacific/Auckland", "Pacific/Fiji", "America/Santiago",
])

_EUROPE_TZ = frozenset([
    "Europe/London", "Europe/Paris", "Europe/Berlin", "Europe/Rome",
    "Europe/Madrid", "Europe/Amsterdam", "Europe/Brussels",
    "Europe/Vienna", "Europe/Stockholm", "Europe/Oslo",
    "Europe/Copenhagen", "Europe/Warsaw", "Europe/Prague",
    "Europe/Budapest", "Europe/Athens", "Europe/Helsinki",
    "Europe/Kiev", "Europe/Bucharest", "Europe/Sofia",
    "Europe/Dublin",
])


def _is_dst_period(year: int, month: int, tz_name: str) -> bool:
    """
    Check if current date falls within DST period for a timezone.
    
    Simplified DST rules:
    - Northern Hemisphere: DST from second Sunday of March to first Sunday of November
    - Southern Hemisphere: DST from first Sunday of October to first Sunday of April
    - Europe: DST from last Sunday of March to last Sunday of October
    
    Note:
        优化版本：使用 frozenset 进行快速查找，
        简化 DST 检查逻辑，减少不必要的计算。
    """
    offset_hours, _, has_dst, _ = _get_timezone_info(tz_name)
    
    if not has_dst:
        return False
    
    # 使用预定义的 frozenset 进行快速查找
    if tz_name in _SOUTHERN_HEMISPHERE_TZ:
        # 南半球：10月到次年3月为 DST
        return month >= 10 or month <= 3
    
    elif tz_name in _EUROPE_TZ:
        # 欧洲：3月到10月为 DST（简化判断）
        return 4 <= month <= 9
    
    else:
        # 北半球（美国风格）：3月到11月为 DST（简化判断）
        return 4 <= month <= 10


def _create_timezone(tz_name: str, dt: Optional[datetime] = None) -> dt_timezone:
    """
    Create a timezone object for a given timezone name.
    
    Args:
        tz_name: Timezone identifier
        dt: Optional datetime for DST calculation
        
    Returns:
        timezone object
    """
    offset_hours, offset_minutes, has_dst, dst_offset = _get_timezone_info(tz_name)
    
    # Calculate effective offset
    effective_offset = offset_hours
    if has_dst and dt and _is_dst_period(dt.year, dt.month, tz_name):
        effective_offset = dst_offset
    
    total_minutes = int(effective_offset * 60) + offset_minutes
    return dt_timezone(timedelta(minutes=total_minutes), tz_name)


# ============================================================================
# Time Zone Conversion
# ============================================================================

def convert_time(dt: datetime, from_tz: str, to_tz: str) -> datetime:
    """
    Convert a datetime from one timezone to another.
    
    Args:
        dt: Datetime object (naive or aware)
        from_tz: Source timezone (e.g., 'Asia/Shanghai', 'UTC', 'America/New_York')
        to_tz: Target timezone
        
    Returns:
        Datetime in target timezone
        
    Raises:
        InvalidTimeZoneError: If timezone is invalid
    """
    try:
        from_zone = _create_timezone(from_tz, dt)
        to_zone = _create_timezone(to_tz)
    except InvalidTimeZoneError:
        raise
    except Exception as e:
        raise InvalidTimeZoneError(f"Invalid timezone: {e}")
    
    # If naive datetime, assume it's in from_tz
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=from_zone)
    else:
        # Convert to from_tz first
        dt = dt.astimezone(from_zone)
    
    return dt.astimezone(to_zone)


def convert_time_string(time_str: str, from_tz: str, to_tz: str, 
                        format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Convert a time string from one timezone to another.
    
    Args:
        time_str: Time string to convert
        from_tz: Source timezone
        to_tz: Target timezone
        format_str: Datetime format string
        
    Returns:
        Converted time string
        
    Raises:
        InvalidTimeError: If time string cannot be parsed
        InvalidTimeZoneError: If timezone is invalid
    """
    try:
        dt = datetime.strptime(time_str, format_str)
    except ValueError as e:
        raise InvalidTimeError(f"Cannot parse time string: {e}")
    
    converted = convert_time(dt, from_tz, to_tz)
    return converted.strftime(format_str)


def get_utc_offset(timezone: str, dt: Optional[datetime] = None) -> timedelta:
    """
    Get UTC offset for a timezone at a specific time.
    
    Args:
        timezone: Timezone identifier
        dt: Optional datetime (uses current time if None)
        
    Returns:
        UTC offset as timedelta
        
    Raises:
        InvalidTimeZoneError: If timezone is invalid
    """
    try:
        tz = _create_timezone(timezone, dt)
    except InvalidTimeZoneError:
        raise
    except Exception as e:
        raise InvalidTimeZoneError(f"Invalid timezone: {e}")
    
    return tz.utcoffset(None) or timedelta(0)


def get_utc_offset_hours(timezone: str, dt: Optional[datetime] = None) -> float:
    """
    Get UTC offset in hours for a timezone.
    
    Args:
        timezone: Timezone identifier
        dt: Optional datetime (uses current time if None)
        
    Returns:
        UTC offset in hours (e.g., 8.0 for UTC+8, -5.0 for UTC-5)
    """
    offset = get_utc_offset(timezone, dt)
    return offset.total_seconds() / 3600


# ============================================================================
# DST (Daylight Saving Time) Detection
# ============================================================================

def is_dst(timezone: str, dt: Optional[datetime] = None) -> bool:
    """
    Check if DST is active for a timezone at a specific time.
    
    Args:
        timezone: Timezone identifier
        dt: Optional datetime (uses current time if None)
        
    Returns:
        True if DST is active, False otherwise
        
    Raises:
        InvalidTimeZoneError: If timezone is invalid
    """
    if dt is None:
        dt = datetime.now()
    
    try:
        _, _, has_dst, _ = _get_timezone_info(timezone)
    except InvalidTimeZoneError:
        raise
    
    if not has_dst:
        return False
    
    return _is_dst_period(dt.year, dt.month, timezone)


def get_dst_info(timezone: str, year: Optional[int] = None) -> Dict[str, Any]:
    """
    Get DST information for a timezone for a specific year.
    
    Args:
        timezone: Timezone identifier
        year: Year to check (uses current year if None)
        
    Returns:
        Dictionary with DST info:
        - has_dst: Whether timezone observes DST
        - start_date: DST start date (or None)
        - end_date: DST end date (or None)
        - offset_std: Standard offset in hours
        - offset_dst: DST offset in hours (or None)
        
    Raises:
        InvalidTimeZoneError: If timezone is invalid
    """
    if year is None:
        year = datetime.now().year
    
    try:
        offset_hours, _, has_dst, dst_offset = _get_timezone_info(timezone)
    except InvalidTimeZoneError:
        raise
    
    result = {
        "has_dst": has_dst,
        "offset_std": float(offset_hours),
        "offset_dst": float(dst_offset) if has_dst else None,
        "start_date": None,
        "end_date": None,
    }
    
    if has_dst:
        # Simplified DST dates
        southern_hemisphere_tz = [
            "Australia/Sydney", "Australia/Melbourne", "Australia/Adelaide",
            "Pacific/Auckland", "Pacific/Fiji", "America/Santiago",
        ]
        
        europe_tz = [
            "Europe/London", "Europe/Paris", "Europe/Berlin", "Europe/Rome",
            "Europe/Madrid", "Europe/Amsterdam", "Europe/Brussels",
            "Europe/Vienna", "Europe/Stockholm", "Europe/Oslo",
            "Europe/Copenhagen", "Europe/Warsaw", "Europe/Prague",
            "Europe/Budapest", "Europe/Athens", "Europe/Helsinki",
            "Europe/Kiev", "Europe/Bucharest", "Europe/Sofia",
            "Europe/Dublin",
        ]
        
        def get_nth_sunday(year: int, month: int, n: int, last: bool = False) -> str:
            """Get the date string of nth Sunday of a month."""
            from datetime import date
            if last:
                if month == 12:
                    next_month = date(year + 1, 1, 1)
                else:
                    next_month = date(year, month + 1, 1)
                last_day = next_month - timedelta(days=1)
                day = last_day.day
                while True:
                    d = date(year, month, day)
                    if d.weekday() == 6:  # Sunday
                        return d.strftime("%Y-%m-%d")
                    day -= 1
            else:
                first_day = date(year, month, 1)
                first_sunday = first_day + timedelta(days=(6 - first_day.weekday()) % 7)
                target_day = first_sunday.day + (n - 1) * 7
                return date(year, month, target_day).strftime("%Y-%m-%d")
        
        if timezone in southern_hemisphere_tz:
            result["start_date"] = get_nth_sunday(year, 10, 1)
            result["end_date"] = get_nth_sunday(year, 4, 1)
        elif timezone in europe_tz:
            result["start_date"] = get_nth_sunday(year, 3, 0, last=True)
            result["end_date"] = get_nth_sunday(year, 10, 0, last=True)
        else:
            # Northern Hemisphere (US style)
            result["start_date"] = get_nth_sunday(year, 3, 2)
            result["end_date"] = get_nth_sunday(year, 11, 1)
    
    return result


# ============================================================================
# Timezone Listing and Info
# ============================================================================

def list_timezones(filter_str: Optional[str] = None) -> List[str]:
    """
    List all available timezones, optionally filtered.
    
    Args:
        filter_str: Optional filter string (case-insensitive substring match)
        
    Returns:
        List of timezone identifiers
    """
    timezones = sorted(TIMEZONE_DATABASE.keys())
    
    if filter_str:
        filter_lower = filter_str.lower()
        timezones = [tz for tz in timezones if filter_lower in tz.lower()]
    
    return timezones


def get_timezone_info(timezone: str) -> Dict[str, Any]:
    """
    Get detailed information about a timezone.
    
    Args:
        timezone: Timezone identifier
        
    Returns:
        Dictionary with timezone info:
        - name: Timezone identifier
        - current_time: Current time in timezone
        - utc_offset: Current UTC offset in hours
        - is_dst: Whether DST is currently active
        - dst_info: Full DST information for current year
        
    Raises:
        InvalidTimeZoneError: If timezone is invalid
    """
    try:
        _ = _get_timezone_info(timezone)
    except InvalidTimeZoneError:
        raise
    
    now = datetime.now()
    tz = _create_timezone(timezone, now)
    local_now = datetime.now(tz)
    current_year = now.year
    
    return {
        "name": timezone,
        "current_time": local_now.strftime("%Y-%m-%d %H:%M:%S %Z"),
        "utc_offset": get_utc_offset_hours(timezone, now),
        "is_dst": is_dst(timezone, now),
        "dst_info": get_dst_info(timezone, current_year),
    }


def get_common_timezones() -> Dict[str, str]:
    """
    Get a dictionary of common timezone identifiers by region.
    
    Returns:
        Dictionary mapping region names to timezone identifiers
    """
    return {
        "UTC": "UTC",
        "China": "Asia/Shanghai",
        "Japan": "Asia/Tokyo",
        "Korea": "Asia/Seoul",
        "Singapore": "Asia/Singapore",
        "Hong Kong": "Asia/Hong_Kong",
        "Taiwan": "Asia/Taipei",
        "India": "Asia/Kolkata",
        "Dubai": "Asia/Dubai",
        "London": "Europe/London",
        "Paris": "Europe/Paris",
        "Berlin": "Europe/Berlin",
        "Moscow": "Europe/Moscow",
        "New York": "America/New_York",
        "Los Angeles": "America/Los_Angeles",
        "Chicago": "America/Chicago",
        "Toronto": "America/Toronto",
        "Sydney": "Australia/Sydney",
        "Melbourne": "Australia/Melbourne",
        "Auckland": "Pacific/Auckland",
        "Sao Paulo": "America/Sao_Paulo",
        "Mexico City": "America/Mexico_City",
    }


# ============================================================================
# Meeting Time Finder
# ============================================================================

def find_meeting_times(timezones: List[str], 
                       work_start: int = 9, 
                       work_end: int = 18,
                       date: Optional[datetime] = None) -> List[Dict[str, Any]]:
    """
    Find suitable meeting times across multiple timezones.
    
    Args:
        timezones: List of timezone identifiers
        work_start: Start of work day (hour, 0-23)
        work_end: End of work day (hour, 0-23)
        date: Date to check (uses today if None)
        
    Returns:
        List of suitable meeting slots, each containing:
        - hour: Hour in UTC
        - times: Dictionary mapping timezone to local time string
        
    Raises:
        InvalidTimeZoneError: If any timezone is invalid
    """
    if len(timezones) < 2:
        raise TimeZoneError("Need at least 2 timezones")
    
    if date is None:
        date = datetime.now()
    
    # Try each hour of the day
    suitable_times = []
    
    for utc_hour in range(24):
        utc_dt = datetime(date.year, date.month, date.day, utc_hour, 0, 0)
        utc_tz = dt_timezone(timedelta(0), "UTC")
        utc_dt = utc_dt.replace(tzinfo=utc_tz)
        
        # Check if this time works for all timezones
        all_valid = True
        times = {}
        
        for tz_str in timezones:
            try:
                local_dt = utc_dt.astimezone(_create_timezone(tz_str, utc_dt))
                local_hour = local_dt.hour
                
                if local_hour < work_start or local_hour >= work_end:
                    all_valid = False
                    break
                
                times[tz_str] = local_dt.strftime("%H:%M")
            except Exception:
                all_valid = False
                break
        
        if all_valid:
            suitable_times.append({
                "utc_hour": utc_hour,
                "utc_time": f"{utc_hour:02d}:00",
                "times": times,
            })
    
    return suitable_times


def time_difference_hours(tz1: str, tz2: str, dt: Optional[datetime] = None) -> float:
    """
    Calculate the time difference in hours between two timezones.
    
    Args:
        tz1: First timezone
        tz2: Second timezone
        dt: Optional datetime (uses current time if None)
        
    Returns:
        Time difference in hours (tz2 - tz1)
    """
    offset1 = get_utc_offset_hours(tz1, dt)
    offset2 = get_utc_offset_hours(tz2, dt)
    return offset2 - offset1


# ============================================================================
# Utility Functions
# ============================================================================

def now_in_timezone(timezone: str) -> datetime:
    """
    Get current datetime in a specific timezone.
    
    Args:
        timezone: Timezone identifier
        
    Returns:
        Current datetime in that timezone
        
    Raises:
        InvalidTimeZoneError: If timezone is invalid
    """
    try:
        tz = _create_timezone(timezone)
    except InvalidTimeZoneError:
        raise
    except Exception as e:
        raise InvalidTimeZoneError(f"Invalid timezone: {e}")
    
    return datetime.now(tz)


def format_for_timezone(dt: datetime, timezone: str, 
                        format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Format a datetime for a specific timezone.
    
    Args:
        dt: Datetime object
        timezone: Target timezone
        format_str: Format string
        
    Returns:
        Formatted time string
        
    Raises:
        InvalidTimeZoneError: If timezone is invalid
    """
    try:
        tz = _create_timezone(timezone, dt)
    except InvalidTimeZoneError:
        raise
    except Exception as e:
        raise InvalidTimeZoneError(f"Invalid timezone: {e}")
    
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=dt_timezone(timedelta(0), "UTC"))
    
    local_dt = dt.astimezone(tz)
    return local_dt.strftime(format_str)


def parse_timezone_aware(time_str: str, timezone: str,
                         format_str: str = "%Y-%m-%d %H:%M:%S") -> datetime:
    """
    Parse a time string and make it timezone-aware.
    
    Args:
        time_str: Time string to parse
        timezone: Timezone to associate with the time
        format_str: Format string
        
    Returns:
        Timezone-aware datetime
        
    Raises:
        InvalidTimeError: If time string cannot be parsed
        InvalidTimeZoneError: If timezone is invalid
    """
    try:
        dt = datetime.strptime(time_str, format_str)
    except ValueError as e:
        raise InvalidTimeError(f"Cannot parse time string: {e}")
    
    try:
        tz = _create_timezone(timezone)
    except InvalidTimeZoneError:
        raise
    except Exception as e:
        raise InvalidTimeZoneError(f"Invalid timezone: {e}")
    
    return dt.replace(tzinfo=tz)


def is_same_day(dt1: datetime, dt2: datetime, timezone: str) -> bool:
    """
    Check if two datetimes fall on the same day in a specific timezone.
    
    Args:
        dt1: First datetime
        dt2: Second datetime
        timezone: Timezone to use for comparison
        
    Returns:
        True if same day, False otherwise
    """
    try:
        tz = _create_timezone(timezone)
    except InvalidTimeZoneError:
        raise
    except Exception as e:
        raise InvalidTimeZoneError(f"Invalid timezone: {e}")
    
    if dt1.tzinfo is None:
        dt1 = dt1.replace(tzinfo=tz)
    if dt2.tzinfo is None:
        dt2 = dt2.replace(tzinfo=tz)
    
    local1 = dt1.astimezone(tz)
    local2 = dt2.astimezone(tz)
    
    return local1.date() == local2.date()


def add_time_in_timezone(dt: datetime, timezone: str,
                         days: int = 0, hours: int = 0, 
                         minutes: int = 0, seconds: int = 0) -> datetime:
    """
    Add time to a datetime in a specific timezone.
    
    Args:
        dt: Starting datetime
        timezone: Timezone to use
        days: Days to add
        hours: Hours to add
        minutes: Minutes to add
        seconds: Seconds to add
        
    Returns:
        New datetime with added time
    """
    try:
        tz = _create_timezone(timezone, dt)
    except InvalidTimeZoneError:
        raise
    except Exception as e:
        raise InvalidTimeZoneError(f"Invalid timezone: {e}")
    
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=tz)
    
    local_dt = dt.astimezone(tz)
    delta = timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
    
    return local_dt + delta
