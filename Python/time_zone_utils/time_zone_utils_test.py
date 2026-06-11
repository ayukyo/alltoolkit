#!/usr/bin/env python3
"""Time Zone Utils Tests"""

import sys
import os
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    TIMEZONE_DATABASE,
    convert_time, convert_time_string,
    get_utc_offset, get_utc_offset_hours,
    is_dst, get_dst_info,
    list_timezones, get_timezone_info, get_common_timezones,
    find_meeting_times, time_difference_hours,
    now_in_timezone, format_for_timezone,
    parse_timezone_aware, is_same_day, add_time_in_timezone
)


def test_timezone_database():
    """Test timezone database has expected entries."""
    assert "UTC" in TIMEZONE_DATABASE
    assert "Asia/Shanghai" in TIMEZONE_DATABASE
    assert "America/New_York" in TIMEZONE_DATABASE
    assert "Europe/London" in TIMEZONE_DATABASE


def test_get_utc_offset():
    """Test UTC offset retrieval."""
    offset = get_utc_offset("Asia/Shanghai")
    assert offset == timedelta(hours=8)


def test_get_utc_offset_invalid():
    """Test invalid timezone raises error."""
    try:
        get_utc_offset("Invalid/Timezone")
        assert False, "Should raise error"
    except Exception:
        pass


def test_get_utc_offset_hours():
    """Test UTC offset in hours."""
    offset = get_utc_offset_hours("Asia/Shanghai")
    assert offset == 8.0
    
    offset_ny = get_utc_offset_hours("America/New_York")
    assert offset_ny < 0  # Negative for NY


def test_convert_time():
    """Test timezone conversion."""
    dt = datetime(2024, 6, 15, 12, 0, 0)  # Noon
    result = convert_time(dt, "UTC", "Asia/Shanghai")
    assert result.hour == 20  # Noon UTC = 8PM Shanghai


def test_convert_time_round_trip():
    """Test round-trip timezone conversion."""
    dt = datetime(2024, 6, 15, 12, 0, 0)
    shanghai = convert_time(dt, "UTC", "Asia/Shanghai")
    back = convert_time(shanghai, "Asia/Shanghai", "UTC")
    assert back.hour == dt.hour
    assert back.minute == dt.minute


def test_list_timezones():
    """Test timezone listing."""
    zones = list_timezones()
    assert len(zones) > 0
    assert "Asia/Shanghai" in zones
    assert "America/New_York" in zones


def test_list_timezones_filter():
    """Test filtering timezones."""
    zones = list_timezones(filter_str="Asia")
    assert len(zones) > 0
    assert all("Asia" in z for z in zones)


def test_is_dst():
    """Test DST detection."""
    # Summer time in NY
    summer_dt = datetime(2024, 7, 15, 12, 0, 0)
    assert is_dst("America/New_York", summer_dt) == True
    
    # Winter time in NY
    winter_dt = datetime(2024, 1, 15, 12, 0, 0)
    assert is_dst("America/New_York", winter_dt) == False


def test_is_dst_no_dst_timezone():
    """Test DST for timezone without DST."""
    dt = datetime(2024, 7, 15, 12, 0, 0)
    assert is_dst("Asia/Shanghai", dt) == False


def test_now_in_timezone():
    """Test getting current time in timezone."""
    result = now_in_timezone("Asia/Shanghai")
    assert result is not None
    assert hasattr(result, 'hour')


def test_get_timezone_info():
    """Test timezone info retrieval."""
    info = get_timezone_info("Asia/Shanghai")
    assert "name" in info
    assert "utc_offset" in info
    assert info["name"] == "Asia/Shanghai"


def test_get_common_timezones():
    """Test common timezones."""
    common = get_common_timezones()
    assert len(common) > 0


def test_time_difference_hours():
    """Test time difference calculation."""
    diff = time_difference_hours("Asia/Shanghai", "America/New_York")
    # Shanghai is UTC+8, NY is UTC-5 (summer) or UTC-5 (winter)
    # Summer: 8 - (-4) = 12 hours diff
    # The function returns a signed value
    assert abs(diff) > 0


def test_find_meeting_times():
    """Test finding meeting times."""
    times = find_meeting_times(
        ["Asia/Shanghai", "America/New_York"],
        work_start=9,
        work_end=18
    )
    assert times is not None
    assert isinstance(times, list)


def test_format_for_timezone():
    """Test timezone formatting."""
    dt = datetime(2024, 6, 15, 12, 0, 0)
    formatted = format_for_timezone(dt, "Asia/Shanghai")
    assert formatted is not None
    assert len(formatted) > 0


def test_parse_timezone_aware():
    """Test parsing timezone-aware time string."""
    result = parse_timezone_aware("2024-06-15 12:00:00", "Asia/Shanghai")
    assert result is not None


def test_is_same_day():
    """Test same day check across timezones."""
    dt1 = datetime(2024, 6, 15, 8, 0, 0)
    dt2 = datetime(2024, 6, 15, 20, 0, 0)
    # Both same calendar day
    assert is_same_day(dt1, dt2, "Asia/Shanghai") == True


def test_add_time_in_timezone():
    """Test adding time in specific timezone."""
    dt = datetime(2024, 6, 15, 12, 0, 0)
    result = add_time_in_timezone(dt, "Asia/Shanghai", hours=2)
    assert result.hour == 14


def test_get_dst_info():
    """Test DST info retrieval."""
    info = get_dst_info("America/New_York", 2024)
    assert isinstance(info, dict)


def test_utc_timezone():
    """Test UTC timezone."""
    offset = get_utc_offset("UTC")
    assert offset == timedelta(hours=0)


if __name__ == "__main__":
    import subprocess
    result = subprocess.run(["python3", "-m", "pytest", __file__, "-v"], cwd=os.path.dirname(os.path.abspath(__file__)))
    sys.exit(result.returncode)
