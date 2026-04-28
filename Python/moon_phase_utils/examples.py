#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Moon Phase Utils - Usage Examples

This file demonstrates various ways to use the moon_phase_utils module.
"""

import sys
import os
from datetime import datetime, date, timedelta

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from moon_phase_utils.moon_phase_utils import (
    get_moon_age,
    get_illumination,
    get_phase_index,
    get_phase_name,
    get_moon_phase,
    is_major_phase,
    get_next_new_moon,
    get_next_full_moon,
    get_next_first_quarter,
    get_next_last_quarter,
    get_moon_phases_in_month,
    get_moon_rise_set,
    get_lunar_eclipse_risk,
    get_moon_info,
    get_moon_calendar,
    get_moon_emoji,
    get_blue_moon_info,
    calculate_moon_distance,
    is_super_moon,
    MoonPhase,
    print_moon_info,
    today,
    SYNODIC_MONTH,
)


def example_basic_usage():
    """Basic usage examples."""
    print("\n" + "=" * 60)
    print("Example 1: Basic Usage")
    print("=" * 60)
    
    # Get today's moon info
    print("\nToday's Moon:")
    print(f"  Phase: {get_phase_name()} {get_moon_emoji()}")
    print(f"  Age: {get_moon_age():.2f} days")
    print(f"  Illumination: {get_illumination():.1f}%")
    print(f"  Major Phase: {is_major_phase()}")
    
    # Get moon info for a specific date
    specific_date = date(2024, 7, 20)
    print(f"\nMoon on {specific_date}:")
    print(f"  Phase: {get_phase_name(specific_date)} {get_moon_emoji(specific_date)}")
    print(f"  Age: {get_moon_age(specific_date):.2f} days")
    print(f"  Illumination: {get_illumination(specific_date):.1f}%")


def example_phase_enum():
    """Using MoonPhase enum."""
    print("\n" + "=" * 60)
    print("Example 2: Using MoonPhase Enum")
    print("=" * 60)
    
    phase = get_moon_phase()
    print(f"\nCurrent Phase: {phase}")
    print(f"  Name: {phase.name}")
    print(f"  Value: {phase.value}")
    
    # Compare with enum
    if phase == MoonPhase.FULL_MOON:
        print("  🌕 It's a full moon!")
    elif phase == MoonPhase.NEW_MOON:
        print("  🌑 It's a new moon!")
    else:
        print(f"  Current phase: {get_phase_name()}")


def example_chinese_names():
    """Chinese language support."""
    print("\n" + "=" * 60)
    print("Example 3: Chinese Language Support")
    print("=" * 60)
    
    print("\n月相名称 (Chinese Moon Phase Names):")
    
    # Current phase in Chinese
    print(f"\n当前月相: {get_phase_name(language='cn')} {get_moon_emoji()}")
    
    # All phases in Chinese
    print("\n所有月相:")
    for i in range(8):
        from moon_phase_utils.moon_phase_utils import PHASE_NAMES_CN
        print(f"  {i}: {PHASE_NAMES_CN[i]}")
    
    # Full info in Chinese
    info = get_moon_info(language="cn")
    print(f"\n详细信息:")
    print(f"  月相: {info['phase_name']}")
    print(f"  月龄: {info['moon_age_days']} 天")
    print(f"  照明度: {info['illumination_percent']}%")


def example_upcoming_phases():
    """Calculate upcoming moon phases."""
    print("\n" + "=" * 60)
    print("Example 4: Upcoming Moon Phases")
    print("=" * 60)
    
    print("\nUpcoming Major Phases:")
    
    next_nm = get_next_new_moon()
    next_fq = get_next_first_quarter()
    next_fm = get_next_full_moon()
    next_lq = get_next_last_quarter()
    
    today = datetime.now()
    
    events = [
        ("🌑 New Moon", next_nm),
        ("🌓 First Quarter", next_fq),
        ("🌕 Full Moon", next_fm),
        ("🌗 Last Quarter", next_lq),
    ]
    
    # Sort by date
    events.sort(key=lambda x: x[1])
    
    for name, event_date in events:
        days_until = (event_date - today).days
        print(f"  {name}: {event_date.strftime('%Y-%m-%d %H:%M')} ({days_until} days)")


def example_monthly_calendar():
    """Generate a moon phase calendar."""
    print("\n" + "=" * 60)
    print("Example 5: Monthly Moon Calendar")
    print("=" * 60)
    
    year = 2024
    month = 7  # July
    
    print(f"\nMoon Calendar for {date(year, month, 1).strftime('%B %Y')}:")
    print("-" * 40)
    
    calendar = get_moon_calendar(year, month)
    
    # Print header
    print(f"{'Day':<4} {'Phase':<18} {'Illum':<8} {'Emoji'}")
    print("-" * 40)
    
    # Print each day
    for day in calendar:
        marker = "★" if day["is_major_phase"] else " "
        print(f"{marker}{day['day']:<3} {day['phase_name']:<18} {day['illumination']:>5.0f}%  {get_moon_emoji(datetime.strptime(day['date'], '%Y-%m-%d'))}")
    
    # Major phases this month
    print("\nMajor Phases This Month:")
    phases = get_moon_phases_in_month(year, month)
    for name, dt in sorted(phases.items(), key=lambda x: x[1]):
        print(f"  {name}: {dt.strftime('%Y-%m-%d %H:%M')}")


def example_blue_moon():
    """Blue moon detection."""
    print("\n" + "=" * 60)
    print("Example 6: Blue Moon Detection")
    print("=" * 60)
    
    for year in [2024, 2025, 2026]:
        info = get_blue_moon_info(year)
        print(f"\n{year}:")
        if info["has_blue_moon"]:
            for bm in info["blue_moons"]:
                print(f"  🔮 Blue Moon in {bm['month_name']}")
                print(f"     First Full Moon: {bm['first_full_moon']}")
                print(f"     Blue Moon: {bm['blue_moon']}")
        else:
            print("  No blue moon this year")


def example_super_moon():
    """Super moon detection."""
    print("\n" + "=" * 60)
    print("Example 7: Super Moon Check")
    print("=" * 60)
    
    # Current status
    print("\nCurrent Status:")
    distance = calculate_moon_distance()
    print(f"  Moon Distance: {distance:,.0f} km")
    
    if is_super_moon():
        print("  🌟 It's a SUPER MOON!")
    else:
        print("  Not a super moon at the moment.")
    
    # Check upcoming full moons
    print("\nChecking upcoming full moons for super moon:")
    next_fm = get_next_full_moon()
    
    for i in range(3):
        check_date = next_fm + timedelta(days=i * 30)  # Check next 3 full moons
        illum = get_illumination(check_date)
        dist = calculate_moon_distance(check_date)
        is_super = dist < 360000 and illum > 90
        
        status = "🌟 SUPER MOON!" if is_super else "  Regular"
        print(f"  {check_date.strftime('%Y-%m-%d')}: {dist:,.0f} km - {status}")


def example_moon_rise_set():
    """Moonrise and moonset times."""
    print("\n" + "=" * 60)
    print("Example 8: Moonrise & Moonset Times")
    print("=" * 60)
    
    locations = [
        ("New York", 40.7128, -74.0060),
        ("London", 51.5074, -0.1278),
        ("Tokyo", 35.6762, 139.6503),
        ("Sydney", -33.8688, 151.2093),
        ("Beijing", 39.9042, 116.4074),
    ]
    
    print("\nApproximate Moonrise/Moonset Times Today:")
    print(f"{'Location':<12} {'Moonrise':<10} {'Moonset':<10}")
    print("-" * 35)
    
    for name, lat, lon in locations:
        rise, set_time = get_moon_rise_set(latitude=lat, longitude=lon)
        rise_str = f"{int(rise):02d}:{int((rise % 1) * 60):02d}"
        set_str = f"{int(set_time):02d}:{int((set_time % 1) * 60):02d}"
        print(f"{name:<12} {rise_str:<10} {set_str:<10}")


def example_eclipse_risk():
    """Lunar eclipse risk estimation."""
    print("\n" + "=" * 60)
    print("Example 9: Lunar Eclipse Risk")
    print("=" * 60)
    
    risk = get_lunar_eclipse_risk()
    risk_desc = {
        "none": "No eclipse expected soon",
        "low": "Low probability",
        "moderate": "Moderate chance",
        "high": "High probability - watch for eclipse!",
    }
    
    print(f"\nCurrent Eclipse Risk: {risk.upper()}")
    print(f"  {risk_desc[risk]}")


def example_comprehensive_info():
    """Get comprehensive moon information."""
    print("\n" + "=" * 60)
    print("Example 10: Comprehensive Moon Information")
    print("=" * 60)
    
    # Using the print function
    print_moon_info()
    
    # Or get data as dictionary
    info = get_moon_info()
    print("As dictionary:")
    for key, value in info.items():
        print(f"  {key}: {value}")


def example_moon_tracking():
    """Track moon over time."""
    print("\n" + "=" * 60)
    print("Example 11: Moon Tracking Over Time")
    print("=" * 60)
    
    print("\nMoon phase tracking for the next 30 days:")
    print(f"{'Date':<12} {'Phase':<20} {'Illum':<8} {'Emoji'}")
    print("-" * 50)
    
    today = date.today()
    for i in range(0, 30, 3):  # Every 3 days
        check_date = today + timedelta(days=i)
        phase = get_phase_name(check_date)
        illum = get_illumination(check_date)
        emoji = get_moon_emoji(check_date)
        print(f"{check_date.strftime('%Y-%m-%d'):<12} {phase:<20} {illum:>5.0f}%   {emoji}")


def example_synodic_month():
    """Synodic month information."""
    print("\n" + "=" * 60)
    print("Example 12: Synodic Month Details")
    print("=" * 60)
    
    print(f"\nSynodic Month Duration: {SYNODIC_MONTH:.6f} days")
    print(f"                       = {SYNODIC_MONTH * 24:.2f} hours")
    print(f"                       = {SYNODIC_MONTH * 24 * 60:.2f} minutes")
    
    # Calculate days until next major phase
    age = get_moon_age()
    days_until_new = SYNODIC_MONTH - age
    days_until_full = (SYNODIC_MONTH / 2 - age) % SYNODIC_MONTH
    
    print(f"\nCurrent moon age: {age:.2f} days")
    print(f"Days until new moon: {days_until_new:.2f}")
    print(f"Days until full moon: {days_until_full:.2f}")


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("🌙 Moon Phase Utils - Usage Examples")
    print("=" * 60)
    
    examples = [
        example_basic_usage,
        example_phase_enum,
        example_chinese_names,
        example_upcoming_phases,
        example_monthly_calendar,
        example_blue_moon,
        example_super_moon,
        example_moon_rise_set,
        example_eclipse_risk,
        example_comprehensive_info,
        example_moon_tracking,
        example_synodic_month,
    ]
    
    for example in examples:
        try:
            example()
        except Exception as e:
            print(f"\nError in {example.__name__}: {e}")
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()