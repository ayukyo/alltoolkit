"""
AllToolkit - Python Time Zone Utils Examples

Practical usage examples for time_zone_utils module.
Demonstrates common scenarios and best practices.

Compatible with Python 3.6+
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime, timedelta, timezone as dt_timezone

from mod import (
    convert_time, convert_time_string,
    get_utc_offset_hours, is_dst, get_dst_info,
    list_timezones, get_timezone_info, get_common_timezones,
    find_meeting_times, time_difference_hours,
    now_in_timezone, format_for_timezone, parse_timezone_aware,
    is_same_day, add_time_in_timezone,
)


def example_basic_conversion():
    """Example 1: Basic timezone conversion"""
    print("=" * 60)
    print("Example 1: Basic Timezone Conversion")
    print("=" * 60)
    
    # Convert datetime object
    shanghai_time = datetime(2026, 4, 10, 16, 0, 0)
    utc_time = convert_time(shanghai_time, "Asia/Shanghai", "UTC")
    ny_time = convert_time(shanghai_time, "Asia/Shanghai", "America/New_York")
    
    print("")
    print("Shanghai: {}".format(shanghai_time.strftime('%Y-%m-%d %H:%M:%S')))
    print("UTC:      {}".format(utc_time.strftime('%Y-%m-%d %H:%M:%S')))
    print("New York: {}".format(ny_time.strftime('%Y-%m-%d %H:%M:%S')))
    
    # Convert time string
    time_str = "2026-04-10 16:00:00"
    converted = convert_time_string(time_str, "Asia/Shanghai", "Europe/London")
    print("")
    print("Shanghai {} = London {}".format(time_str, converted))


def example_dst_detection():
    """Example 2: DST detection"""
    print("")
    print("=" * 60)
    print("Example 2: DST Detection")
    print("=" * 60)
    
    cities = [
        ("Asia/Shanghai", "Shanghai"),
        ("America/New_York", "New York"),
        ("Europe/London", "London"),
        ("Australia/Sydney", "Sydney"),
    ]
    
    dates = [
        (datetime(2026, 1, 15), "Jan 15 (Northern Winter)"),
        (datetime(2026, 7, 15), "Jul 15 (Northern Summer)"),
    ]
    
    for tz, name in cities:
        print("")
        print("{} ({}):".format(name, tz))
        for dt, date_name in dates:
            dst = is_dst(tz, dt)
            offset = get_utc_offset_hours(tz, dt)
            print("  {}: DST={}, UTC offset={:+.1f}".format(date_name, dst, offset))


def example_meeting_finder():
    """Example 3: Meeting time finder"""
    print("")
    print("=" * 60)
    print("Example 3: Meeting Time Finder")
    print("=" * 60)
    
    # Scenario 1: China and Europe teams
    print("")
    print("Scenario 1: Shanghai - London team meeting")
    times = find_meeting_times(
        ["Asia/Shanghai", "Europe/London"],
        work_start=9, work_end=18,
        date=datetime(2026, 4, 10)
    )
    
    if times:
        print("Found {} suitable time slots:".format(len(times)))
        for i, slot in enumerate(times[:5], 1):  # Show first 5
            print("")
            print("  Option {}: UTC {}".format(i, slot['utc_time']))
            for tz, local_time in slot['times'].items():
                print("    {}: {}".format(tz, local_time))
    else:
        print("  No suitable time slots")
    
    # Scenario 2: Global team (more challenging)
    print("")
    print("Scenario 2: Shanghai - London - New York global meeting")
    times = find_meeting_times(
        ["Asia/Shanghai", "Europe/London", "America/New_York"],
        work_start=9, work_end=17,  # Narrower window
        date=datetime(2026, 4, 10)
    )
    
    if times:
        print("Found {} suitable time slots:".format(len(times)))
        for slot in times:
            print("")
            print("  UTC {}:".format(slot['utc_time']))
            for tz, local_time in slot['times'].items():
                print("    {}: {}".format(tz, local_time))
    else:
        print("  No overlap for all three timezones during work hours")
        print("  Consider:")
        print("  - Someone attending outside work hours")
        print("  - Using recorded meetings or async communication")
        print("  - Rotating meeting times")


def example_world_clock():
    """Example 4: World clock"""
    print("")
    print("=" * 60)
    print("Example 4: World Clock")
    print("=" * 60)
    
    common = get_common_timezones()
    
    # Select major cities
    cities = {
        "Shanghai": common["China"],
        "Tokyo": common["Japan"],
        "London": common["London"],
        "Paris": common["Paris"],
        "New York": common["New York"],
        "Los Angeles": common["Los Angeles"],
        "Sydney": common["Sydney"],
    }
    
    print("")
    print("Current time around the world:")
    print("-" * 50)
    
    utc_now = datetime.now(dt_timezone(timedelta(0)))
    print("UTC Base: {}".format(utc_now.strftime('%Y-%m-%d %H:%M:%S')))
    print("-" * 50)
    
    for city, tz in cities.items():
        local_time = now_in_timezone(tz)
        offset = get_utc_offset_hours(tz)
        dst_marker = " [DST]" if is_dst(tz) else ""
        print("{:>10}: {} (UTC{:+.0f}){}".format(
            city, local_time.strftime('%H:%M:%S'), offset, dst_marker))


def example_time_calculations():
    """Example 5: Time calculations"""
    print("")
    print("=" * 60)
    print("Example 5: Time Calculations")
    print("=" * 60)
    
    # Scenario: Flight time calculation
    print("")
    print("Flight time calculation: Shanghai -> New York")
    departure = datetime(2026, 4, 10, 12, 0, 0)  # Noon departure
    flight_duration = 14  # hours
    
    # Calculate arrival time (Shanghai timezone)
    arrival_sh = add_time_in_timezone(departure, "Asia/Shanghai", hours=flight_duration)
    
    # Convert to New York local time
    arrival_ny = convert_time(arrival_sh, "Asia/Shanghai", "America/New_York")
    
    print("Departure: Shanghai {}".format(departure.strftime('%Y-%m-%d %H:%M')))
    print("Duration:  {} hours".format(flight_duration))
    print("Arrival:   New York {}".format(arrival_ny.strftime('%Y-%m-%d %H:%M')))
    
    # Scenario: Project deadline
    print("")
    print("Project deadline calculation")
    start_date = datetime(2026, 4, 10, 9, 0, 0)
    
    # Add work days (simplified: just add calendar days)
    work_days = 10
    deadline = add_time_in_timezone(start_date, "Asia/Shanghai", days=work_days)
    
    print("Start:     {}".format(start_date.strftime('%Y-%m-%d %H:%M')))
    print("Work days: {}".format(work_days))
    print("Deadline:  {}".format(deadline.strftime('%Y-%m-%d %H:%M')))


def example_timezone_info():
    """Example 6: Timezone info query"""
    print("")
    print("=" * 60)
    print("Example 6: Timezone Info Query")
    print("=" * 60)
    
    # Query specific timezone
    tz = "Asia/Shanghai"
    info = get_timezone_info(tz)
    
    print("")
    print("{}:".format(info['name']))
    print("  Current time: {}".format(info['current_time']))
    print("  UTC offset:   {:+.1f} hours".format(info['utc_offset']))
    print("  DST active:   {}".format('Yes' if info['is_dst'] else 'No'))
    
    # DST details
    dst_info = info['dst_info']
    print("")
    print("  DST Details:")
    print("  - Has DST:       {}".format('Yes' if dst_info['has_dst'] else 'No'))
    if dst_info['has_dst']:
        print("  - Standard offset: {:+.1f}".format(dst_info['offset_std']))
        print("  - DST offset:      {:+.1f}".format(dst_info['offset_dst']))
        print("  - Start date:      {}".format(dst_info['start_date']))
        print("  - End date:        {}".format(dst_info['end_date']))
    
    # List all timezone count
    all_timezones = list_timezones()
    print("")
    print("IANA timezone database has {} timezones".format(len(all_timezones)))
    
    # Filter Asia timezones
    asia_timezones = list_timezones("Asia/")
    print("Asia timezones: {}".format(len(asia_timezones)))


def example_special_timezones():
    """Example 7: Special timezones"""
    print("")
    print("=" * 60)
    print("Example 7: Special Timezones (Non-hour offsets)")
    print("=" * 60)
    
    special_tzs = [
        ("Asia/Kolkata", "India", 5.5),       # UTC+5:30
        ("Asia/Kathmandu", "Nepal", 5.75),    # UTC+5:45
        ("Pacific/Marquesas", "Marquesas", -9.5),  # UTC-9:30
    ]
    
    print("")
    print("Timezones with non-hour offsets:")
    for tz, name, expected_offset in special_tzs:
        offset = get_utc_offset_hours(tz)
        status = "[OK]" if abs(offset - expected_offset) < 0.01 else "[FAIL]"
        print("  {} {}: UTC{:+.2f}".format(status, name, offset))


def example_practical_scenarios():
    """Example 8: Practical scenarios"""
    print("")
    print("=" * 60)
    print("Example 8: Practical Scenarios")
    print("=" * 60)
    
    # Scenario 1: Check if in quiet hours
    print("")
    print("Scenario 1: Check if user is in quiet hours")
    
    def is_quiet_hours(user_tz, quiet_start=22, quiet_end=8):
        now = now_in_timezone(user_tz)
        hour = now.hour
        return hour >= quiet_start or hour < quiet_end
    
    user_tz = "Asia/Shanghai"
    if is_quiet_hours(user_tz):
        print("  User ({}) is in quiet hours, defer notification".format(user_tz))
    else:
        print("  User ({}) can receive notifications".format(user_tz))
    
    # Scenario 2: Log time normalization
    print("")
    print("Scenario 2: Normalize log times to UTC")
    
    log_entries = [
        ("2026-04-10 16:00:00", "Asia/Shanghai", "Shanghai Server"),
        ("2026-04-10 09:00:00", "Europe/London", "London Server"),
        ("2026-04-10 04:00:00", "America/New_York", "New York Server"),
    ]
    
    print("  Original -> UTC:")
    for time_str, tz, server in log_entries:
        dt = parse_timezone_aware(time_str, tz)
        utc_time = format_for_timezone(dt, "UTC")
        print("  {}: {} -> {}".format(server, time_str, utc_time))
    
    # Scenario 3: Cross-timezone birthday reminder
    print("")
    print("Scenario 3: Cross-timezone birthday reminder")
    
    friend_tz = "America/New_York"
    birthday = datetime(2026, 4, 15, 0, 0, 0)  # Friend's local April 15 midnight
    
    # Convert to my timezone
    my_tz = "Asia/Shanghai"
    birthday_sh = convert_time(birthday, friend_tz, my_tz)
    
    print("  Friend timezone: {}".format(friend_tz))
    print("  Birthday date:   {}".format(birthday.strftime('%Y-%m-%d')))
    print("  My timezone:     {}".format(my_tz))
    print("  My local time:   {}".format(birthday_sh.strftime('%Y-%m-%d %H:%M')))
    print("  Reminder: Send wishes before {}".format(birthday_sh.strftime('%m-%d %H:%M')))


def run_all_examples():
    """Run all examples"""
    print("")
    print("*" * 60)
    print("AllToolkit - Time Zone Utils Examples")
    print("*" * 60)
    
    example_basic_conversion()
    example_dst_detection()
    example_meeting_finder()
    example_world_clock()
    example_time_calculations()
    example_timezone_info()
    example_special_timezones()
    example_practical_scenarios()
    
    print("")
    print("=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    run_all_examples()
