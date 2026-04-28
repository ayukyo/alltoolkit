#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AllToolkit - Moon Phase Utilities Module

Comprehensive moon phase calculation utilities for Python with zero external dependencies.
Provides moon phase calculation, illumination percentage, phase names, and more.

Based on astronomical algorithms adapted for simplicity and accuracy.

Author: AllToolkit
License: MIT
"""

import math
from datetime import datetime, date, timedelta
from typing import Union, Tuple, Optional, List, Dict
from enum import Enum


# =============================================================================
# Constants
# =============================================================================

# Synodic month (average time between same moon phases) in days
SYNODIC_MONTH = 29.530588853

# Known new moon date (J2000.0 epoch reference)
# January 6, 2000, 18:14 UTC
J2000_NEW_MOON = datetime(2000, 1, 6, 18, 14, 0)

# Moon phase names
PHASE_NAMES = {
    0: "New Moon",           # 新月
    1: "Waxing Crescent",    # 蛾眉月（渐盈）
    2: "First Quarter",      # 上弦月
    3: "Waxing Gibbous",     # 盈凸月
    4: "Full Moon",          # 满月
    5: "Waning Gibbous",     # 亏凸月
    6: "Last Quarter",       # 下弦月
    7: "Waning Crescent",    # 残月（渐亏）
}

PHASE_NAMES_CN = {
    0: "新月",
    1: "蛾眉月",
    2: "上弦月",
    3: "盈凸月",
    4: "满月",
    5: "亏凸月",
    6: "下弦月",
    7: "残月",
}

# Major phase names (primary phases)
MAJOR_PHASES = {
    0: "New Moon",      # 新月
    2: "First Quarter", # 上弦月
    4: "Full Moon",     # 满月
    6: "Last Quarter",  # 下弦月
}

MAJOR_PHASES_CN = {
    0: "新月",
    2: "上弦月",
    4: "满月",
    6: "下弦月",
}


# =============================================================================
# Enums
# =============================================================================

class MoonPhase(Enum):
    """Moon phase enumeration."""
    NEW_MOON = 0
    WAXING_CRESCENT = 1
    FIRST_QUARTER = 2
    WAXING_GIBBOUS = 3
    FULL_MOON = 4
    WANING_GIBBOUS = 5
    LAST_QUARTER = 6
    WANING_CRESCENT = 7


class IlluminationLevel(Enum):
    """Illumination level categories."""
    DARK = "dark"           # 0-10%
    SLIM = "slim"           # 10-30%
    CRESCENT = "crescent"   # 30-50%
    QUARTER = "quarter"     # 45-55%
    GIBBOUS = "gibbous"     # 50-70%
    BRIGHT = "bright"       # 70-90%
    FULL = "full"           # 90-100%


# =============================================================================
# Core Functions
# =============================================================================

def get_moon_age(target_date: Union[datetime, date] = None) -> float:
    """
    Calculate the moon's age in days since the last new moon.
    
    Args:
        target_date: Target date (defaults to now)
        
    Returns:
        Moon age in days (0 to ~29.53)
        
    Example:
        >>> age = get_moon_age(date(2024, 1, 1))
        >>> print(f"Moon age: {age:.2f} days")
    """
    if target_date is None:
        target_date = datetime.now()
    elif isinstance(target_date, date) and not isinstance(target_date, datetime):
        target_date = datetime.combine(target_date, datetime.min.time())
    
    # Calculate days since reference new moon
    days_since_ref = (target_date - J2000_NEW_MOON).total_seconds() / 86400
    
    # Calculate moon age (modulo synodic month)
    moon_age = days_since_ref % SYNODIC_MONTH
    
    # Ensure positive
    if moon_age < 0:
        moon_age += SYNODIC_MONTH
    
    return moon_age


def get_illumination(target_date: Union[datetime, date] = None) -> float:
    """
    Calculate the moon's illumination percentage.
    
    Uses a simplified formula based on moon age.
    
    Args:
        target_date: Target date (defaults to now)
        
    Returns:
        Illumination percentage (0-100)
        
    Example:
        >>> illum = get_illumination()
        >>> print(f"Moon is {illum:.1f}% illuminated")
    """
    age = get_moon_age(target_date)
    
    # Moon phase angle (0 to 2π)
    phase_angle = 2 * math.pi * (age / SYNODIC_MONTH)
    
    # Illumination formula: (1 - cos(phase_angle)) / 2
    illumination = (1 - math.cos(phase_angle)) / 2 * 100
    
    return illumination


def get_phase_index(target_date: Union[datetime, date] = None) -> int:
    """
    Get the moon phase index (0-7) for a given date.
    
    Phase indices:
        0: New Moon
        1: Waxing Crescent
        2: First Quarter
        3: Waxing Gibbous
        4: Full Moon
        5: Waning Gibbous
        6: Last Quarter
        7: Waning Crescent
    
    Args:
        target_date: Target date (defaults to now)
        
    Returns:
        Phase index (0-7)
        
    Example:
        >>> idx = get_phase_index(date(2024, 1, 13))
        >>> print(get_phase_name(idx))
    """
    age = get_moon_age(target_date)
    
    # Each phase spans approximately 3.69 days (29.53 / 8)
    phase_duration = SYNODIC_MONTH / 8
    
    phase_index = int(age / phase_duration) % 8
    
    return phase_index


def get_phase_name(target_date: Union[datetime, date] = None, 
                   language: str = "en") -> str:
    """
    Get the moon phase name for a given date.
    
    Args:
        target_date: Target date (defaults to now)
        language: "en" for English, "cn" for Chinese
        
    Returns:
        Phase name string
        
    Example:
        >>> print(get_phase_name(date(2024, 1, 13)))
        'Full Moon'
        >>> print(get_phase_name(date(2024, 1, 13), "cn"))
        '满月'
    """
    phase_index = get_phase_index(target_date)
    
    if language == "cn" or language == "zh":
        return PHASE_NAMES_CN.get(phase_index, "Unknown")
    
    return PHASE_NAMES.get(phase_index, "Unknown")


def get_moon_phase(target_date: Union[datetime, date] = None) -> MoonPhase:
    """
    Get the moon phase enum for a given date.
    
    Args:
        target_date: Target date (defaults to now)
        
    Returns:
        MoonPhase enum value
        
    Example:
        >>> phase = get_moon_phase(date(2024, 1, 13))
        >>> print(phase)
        MoonPhase.FULL_MOON
    """
    phase_index = get_phase_index(target_date)
    return MoonPhase(phase_index)


def is_major_phase(target_date: Union[datetime, date] = None) -> bool:
    """
    Check if the moon is in a major phase (new, first quarter, full, last quarter).
    
    Args:
        target_date: Target date (defaults to now)
        
    Returns:
        True if major phase, False otherwise
        
    Example:
        >>> is_major_phase(date(2024, 1, 13))  # Around full moon
        True
    """
    phase_index = get_phase_index(target_date)
    return phase_index in MAJOR_PHASES


def get_next_new_moon(target_date: Union[datetime, date] = None) -> datetime:
    """
    Calculate the date of the next new moon.
    
    Args:
        target_date: Starting date (defaults to now)
        
    Returns:
        Datetime of next new moon
        
    Example:
        >>> next_nm = get_next_new_moon()
        >>> print(f"Next new moon: {next_nm.strftime('%Y-%m-%d')}")
    """
    if target_date is None:
        target_date = datetime.now()
    elif isinstance(target_date, date) and not isinstance(target_date, datetime):
        target_date = datetime.combine(target_date, datetime.min.time())
    
    age = get_moon_age(target_date)
    days_until_new = SYNODIC_MONTH - age
    
    return target_date + timedelta(days=days_until_new)


def get_next_full_moon(target_date: Union[datetime, date] = None) -> datetime:
    """
    Calculate the date of the next full moon.
    
    Args:
        target_date: Starting date (defaults to now)
        
    Returns:
        Datetime of next full moon
        
    Example:
        >>> next_fm = get_next_full_moon()
        >>> print(f"Next full moon: {next_fm.strftime('%Y-%m-%d')}")
    """
    if target_date is None:
        target_date = datetime.now()
    elif isinstance(target_date, date) and not isinstance(target_date, datetime):
        target_date = datetime.combine(target_date, datetime.min.time())
    
    age = get_moon_age(target_date)
    
    # Full moon is at half the synodic month
    full_moon_age = SYNODIC_MONTH / 2
    
    if age < full_moon_age:
        days_until_full = full_moon_age - age
    else:
        days_until_full = SYNODIC_MONTH - age + full_moon_age
    
    return target_date + timedelta(days=days_until_full)


def get_next_first_quarter(target_date: Union[datetime, date] = None) -> datetime:
    """
    Calculate the date of the next first quarter moon.
    
    Args:
        target_date: Starting date (defaults to now)
        
    Returns:
        Datetime of next first quarter
    """
    if target_date is None:
        target_date = datetime.now()
    elif isinstance(target_date, date) and not isinstance(target_date, datetime):
        target_date = datetime.combine(target_date, datetime.min.time())
    
    age = get_moon_age(target_date)
    quarter_age = SYNODIC_MONTH / 4
    
    if age < quarter_age:
        days_until = quarter_age - age
    else:
        days_until = SYNODIC_MONTH - age + quarter_age
    
    return target_date + timedelta(days=days_until)


def get_next_last_quarter(target_date: Union[datetime, date] = None) -> datetime:
    """
    Calculate the date of the next last quarter moon.
    
    Args:
        target_date: Starting date (defaults to now)
        
    Returns:
        Datetime of next last quarter
    """
    if target_date is None:
        target_date = datetime.now()
    elif isinstance(target_date, date) and not isinstance(target_date, datetime):
        target_date = datetime.combine(target_date, datetime.min.time())
    
    age = get_moon_age(target_date)
    three_quarter_age = 3 * SYNODIC_MONTH / 4
    
    if age < three_quarter_age:
        days_until = three_quarter_age - age
    else:
        days_until = SYNODIC_MONTH - age + three_quarter_age
    
    return target_date + timedelta(days=days_until)


def get_moon_phases_in_month(year: int, month: int) -> Dict[str, datetime]:
    """
    Get all major moon phases for a given month.
    
    Args:
        year: Year (e.g., 2024)
        month: Month (1-12)
        
    Returns:
        Dictionary with phase names as keys and datetime as values
        
    Example:
        >>> phases = get_moon_phases_in_month(2024, 1)
        >>> for name, dt in phases.items():
        ...     print(f"{name}: {dt.strftime('%Y-%m-%d %H:%M')}")
    """
    start_date = datetime(year, month, 1)
    
    # Find the end of the month
    if month == 12:
        end_date = datetime(year + 1, 1, 1) - timedelta(seconds=1)
    else:
        end_date = datetime(year, month + 1, 1) - timedelta(seconds=1)
    
    phases = {}
    
    # Find all new moons in the month
    next_nm = get_next_new_moon(start_date - timedelta(days=SYNODIC_MONTH))
    while next_nm <= end_date:
        if next_nm >= start_date:
            phases["New Moon"] = next_nm
        next_nm = get_next_new_moon(next_nm + timedelta(days=1))
    
    # Find all full moons in the month
    next_fm = get_next_full_moon(start_date - timedelta(days=SYNODIC_MONTH))
    while next_fm <= end_date:
        if next_fm >= start_date:
            phases["Full Moon"] = next_fm
        next_fm = get_next_full_moon(next_fm + timedelta(days=1))
    
    # Find first quarter
    next_fq = get_next_first_quarter(start_date - timedelta(days=SYNODIC_MONTH))
    while next_fq <= end_date:
        if next_fq >= start_date:
            phases["First Quarter"] = next_fq
        next_fq = get_next_first_quarter(next_fq + timedelta(days=1))
    
    # Find last quarter
    next_lq = get_next_last_quarter(start_date - timedelta(days=SYNODIC_MONTH))
    while next_lq <= end_date:
        if next_lq >= start_date:
            phases["Last Quarter"] = next_lq
        next_lq = get_next_last_quarter(next_lq + timedelta(days=1))
    
    return dict(sorted(phases.items(), key=lambda x: x[1]))


def get_moon_rise_set(target_date: Union[datetime, date] = None,
                      latitude: float = 40.7128,
                      longitude: float = -74.0060) -> Tuple[Optional[float], Optional[float]]:
    """
    Calculate approximate moonrise and moonset times.
    
    This is a simplified approximation based on the moon's phase.
    For accurate calculations, use specialized astronomical libraries.
    
    Args:
        target_date: Target date (defaults to now)
        latitude: Observer's latitude in degrees (default: NYC)
        longitude: Observer's longitude in degrees (default: NYC)
        
    Returns:
        Tuple of (moonrise_hour, moonset_hour) in 24-hour format, or (None, None)
        
    Note:
        This is a rough approximation. Actual times vary significantly
        based on the moon's position in its orbit.
        
    Example:
        >>> rise, set_time = get_moon_rise_set()
        >>> if rise and set_time:
        ...     print(f"Moonrise: {rise:.1f}h, Moonset: {set_time:.1f}h")
    """
    if target_date is None:
        target_date = datetime.now()
    elif isinstance(target_date, date) and not isinstance(target_date, datetime):
        target_date = datetime.combine(target_date, datetime.min.time())
    
    # Get moon age and phase
    age = get_moon_age(target_date)
    
    # Simplified approximation based on phase
    # New moon rises around sunrise, full moon rises around sunset
    # Each day, moonrise is about 50 minutes later
    
    # Base: new moon rises at ~6 AM
    base_rise = 6.0  # hours
    
    # Moonrise delay per day (moon rises ~50 min later each day)
    delay_per_day = 50 / 60  # hours
    
    # Calculate moonrise
    moonrise = (base_rise + (age * delay_per_day)) % 24
    
    # Moonset is approximately 12 hours after moonrise
    moonset = (moonrise + 12) % 24
    
    return moonrise, moonset


def get_lunar_eclipse_risk(target_date: Union[datetime, date] = None) -> str:
    """
    Estimate lunar eclipse visibility risk for the next full moon.
    
    This is a simplified approximation based on the moon's position
    relative to the ecliptic node. For accurate predictions, use
    specialized astronomical ephemeris data.
    
    Args:
        target_date: Target date (defaults to now)
        
    Returns:
        Risk level: "none", "low", "moderate", "high"
        
    Example:
        >>> risk = get_lunar_eclipse_risk()
        >>> print(f"Eclipse risk: {risk}")
    """
    if target_date is None:
        target_date = datetime.now()
    
    # Get the next full moon
    next_fm = get_next_full_moon(target_date)
    
    # Calculate days since reference date
    days_since_ref = (next_fm - J2000_NEW_MOON).total_seconds() / 86400
    
    # Eclipses occur when the moon is near a node
    # Nodes precess with a period of about 18.6 years (6798 days)
    node_period = 6798  # days
    
    # Eclipse season occurs every ~173 days
    eclipse_season = 173.31
    
    # Calculate position in eclipse cycle
    position = days_since_ref % eclipse_season
    
    # Eclipse is possible when position is within ~18 days of node
    distance_from_node = min(position, eclipse_season - position)
    
    if distance_from_node < 5:
        return "high"
    elif distance_from_node < 10:
        return "moderate"
    elif distance_from_node < 18:
        return "low"
    else:
        return "none"


def get_moon_info(target_date: Union[datetime, date] = None,
                  language: str = "en") -> Dict[str, any]:
    """
    Get comprehensive moon information for a given date.
    
    Args:
        target_date: Target date (defaults to now)
        language: "en" for English, "cn" for Chinese
        
    Returns:
        Dictionary containing all moon phase information
        
    Example:
        >>> info = get_moon_info()
        >>> for key, value in info.items():
        ...     print(f"{key}: {value}")
    """
    if target_date is None:
        target_date = datetime.now()
    elif isinstance(target_date, date) and not isinstance(target_date, datetime):
        target_date = datetime.combine(target_date, datetime.min.time())
    
    phase_index = get_phase_index(target_date)
    age = get_moon_age(target_date)
    illumination = get_illumination(target_date)
    
    phase_names = PHASE_NAMES_CN if language in ("cn", "zh") else PHASE_NAMES
    
    return {
        "date": target_date.strftime("%Y-%m-%d"),
        "time": target_date.strftime("%H:%M:%S"),
        "phase_index": phase_index,
        "phase_name": phase_names.get(phase_index, "Unknown"),
        "moon_age_days": round(age, 2),
        "illumination_percent": round(illumination, 1),
        "is_major_phase": is_major_phase(target_date),
        "is_waxing": phase_index < 4,
        "is_waning": phase_index > 4,
        "next_new_moon": get_next_new_moon(target_date).strftime("%Y-%m-%d"),
        "next_full_moon": get_next_full_moon(target_date).strftime("%Y-%m-%d"),
        "days_until_new_moon": round(SYNODIC_MONTH - age, 1),
        "days_until_full_moon": round(
            (SYNODIC_MONTH / 2 - age) % SYNODIC_MONTH, 1
        ),
        "synodic_month_days": round(SYNODIC_MONTH, 3),
    }


def get_moon_calendar(year: int, month: int,
                      language: str = "en") -> List[Dict[str, any]]:
    """
    Generate a moon phase calendar for a month.
    
    Args:
        year: Year (e.g., 2024)
        month: Month (1-12)
        language: "en" for English, "cn" for Chinese
        
    Returns:
        List of daily moon information
        
    Example:
        >>> calendar = get_moon_calendar(2024, 1)
        >>> for day in calendar[:7]:  # First week
        ...     print(f"{day['date']}: {day['phase_name']} ({day['illumination']:.0f}%)")
    """
    # Determine the number of days in the month
    if month == 12:
        next_month = datetime(year + 1, 1, 1)
    else:
        next_month = datetime(year, month + 1, 1)
    
    days_in_month = (next_month - datetime(year, month, 1)).days
    
    calendar = []
    for day in range(1, days_in_month + 1):
        dt = datetime(year, month, day)
        info = {
            "date": dt.strftime("%Y-%m-%d"),
            "day": day,
            "phase_index": get_phase_index(dt),
            "phase_name": get_phase_name(dt, language),
            "moon_age": round(get_moon_age(dt), 1),
            "illumination": round(get_illumination(dt), 1),
            "is_major_phase": is_major_phase(dt),
        }
        calendar.append(info)
    
    return calendar


def get_moon_emoji(target_date: Union[datetime, date] = None) -> str:
    """
    Get the emoji representation of the current moon phase.
    
    Args:
        target_date: Target date (defaults to now)
        
    Returns:
        Moon phase emoji
        
    Example:
        >>> emoji = get_moon_emoji()
        >>> print(f"Current moon: {emoji}")
    """
    phase_index = get_phase_index(target_date)
    
    emoji_map = {
        0: "🌑",  # New Moon
        1: "🌒",  # Waxing Crescent
        2: "🌓",  # First Quarter
        3: "🌔",  # Waxing Gibbous
        4: "🌕",  # Full Moon
        5: "🌖",  # Waning Gibbous
        6: "🌗",  # Last Quarter
        7: "🌘",  # Waning Crescent
    }
    
    return emoji_map.get(phase_index, "🌙")


def get_blue_moon_info(year: int) -> Dict[str, any]:
    """
    Find blue moons (second full moon in a month) for a given year.
    
    A "blue moon" is the second full moon in a calendar month.
    
    Args:
        year: Year to check
        
    Returns:
        Dictionary with blue moon information
        
    Example:
        >>> info = get_blue_moon_info(2024)
        >>> if info["has_blue_moon"]:
        ...     print(f"Blue moon in {info['blue_moon_month']}")
    """
    blue_moons = []
    
    for month in range(1, 13):
        # Get all full moons in this month
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1) - timedelta(seconds=1)
        else:
            end_date = datetime(year, month + 1, 1) - timedelta(seconds=1)
        
        # Find full moons in this month
        full_moons = []
        next_fm = get_next_full_moon(start_date - timedelta(days=SYNODIC_MONTH))
        
        while next_fm <= end_date:
            if start_date <= next_fm <= end_date:
                full_moons.append(next_fm)
            next_fm = get_next_full_moon(next_fm + timedelta(days=1))
        
        if len(full_moons) > 1:
            blue_moons.append({
                "month": month,
                "month_name": start_date.strftime("%B"),
                "first_full_moon": full_moons[0].strftime("%Y-%m-%d"),
                "blue_moon": full_moons[1].strftime("%Y-%m-%d"),
            })
    
    return {
        "year": year,
        "has_blue_moon": len(blue_moons) > 0,
        "blue_moons": blue_moons,
        "count": len(blue_moons),
    }


def calculate_moon_distance(target_date: Union[datetime, date] = None) -> float:
    """
    Calculate approximate distance from Earth to Moon.
    
    The moon's distance varies between ~356,500 km (perigee) and
    ~406,700 km (apogee) due to its elliptical orbit.
    
    Args:
        target_date: Target date (defaults to now)
        
    Returns:
        Distance in kilometers
        
    Note:
        This is a simplified approximation based on the moon's phase
        in its anomalistic month (~27.55 days).
        
    Example:
        >>> distance = calculate_moon_distance()
        >>> print(f"Moon distance: {distance:,.0f} km")
    """
    if target_date is None:
        target_date = datetime.now()
    
    # Anomalistic month (perigee to perigee) in days
    anomalistic_month = 27.55455
    
    # Reference perigee (approximate)
    # Using a known perigee date
    ref_perigee = datetime(2000, 1, 19, 0, 0, 0)
    
    # Days since reference
    days_since_ref = (target_date - ref_perigee).total_seconds() / 86400
    
    # Position in anomalistic cycle
    position = days_since_ref % anomalistic_month
    if position < 0:
        position += anomalistic_month
    
    # Perigee and apogee distances
    perigee = 356500  # km
    apogee = 406700   # km
    mean_distance = (perigee + apogee) / 2
    amplitude = (apogee - perigee) / 2
    
    # Distance varies sinusoidally
    angle = 2 * math.pi * (position / anomalistic_month)
    distance = mean_distance + amplitude * math.cos(angle)
    
    return distance


def is_super_moon(target_date: Union[datetime, date] = None) -> bool:
    """
    Check if the given date is during a super moon.
    
    A super moon occurs when a full moon coincides with the moon
    being at or near perigee (closest approach to Earth).
    
    Args:
        target_date: Target date (defaults to now)
        
    Returns:
        True if super moon, False otherwise
        
    Example:
        >>> if is_super_moon():
        ...     print("It's a super moon!")
    """
    if target_date is None:
        target_date = datetime.now()
    
    # Check if near full moon (illumination > 90%)
    illumination = get_illumination(target_date)
    if illumination < 90:
        return False
    
    # Check distance (super moon when < 360,000 km)
    distance = calculate_moon_distance(target_date)
    
    return distance < 360000


# =============================================================================
# Convenience Functions
# =============================================================================

def today() -> Dict[str, any]:
    """Get moon info for today."""
    return get_moon_info(datetime.now())


def print_moon_info(target_date: Union[datetime, date] = None) -> None:
    """
    Print formatted moon information.
    
    Args:
        target_date: Target date (defaults to now)
    """
    info = get_moon_info(target_date)
    
    print("\n" + "=" * 50)
    print("🌙 MOON INFORMATION")
    print("=" * 50)
    print(f"Date:           {info['date']}")
    print(f"Time:           {info['time']}")
    print(f"Phase:          {info['phase_name']} {get_moon_emoji(target_date)}")
    print(f"Moon Age:       {info['moon_age_days']} days")
    print(f"Illumination:   {info['illumination_percent']}%")
    print(f"Major Phase:    {'Yes' if info['is_major_phase'] else 'No'}")
    print(f"Waxing/Waning:  {'Waxing' if info['is_waxing'] else 'Waning' if info['is_waning'] else 'N/A'}")
    print("-" * 50)
    print(f"Next New Moon:  {info['next_new_moon']} ({info['days_until_new_moon']} days)")
    print(f"Next Full Moon: {info['next_full_moon']} ({info['days_until_full_moon']} days)")
    print("=" * 50 + "\n")


if __name__ == "__main__":
    # Demo
    print("\n" + "=" * 60)
    print("Moon Phase Utils - Demo")
    print("=" * 60)
    
    # Today's moon info
    print_moon_info()
    
    # Moon calendar for current month
    today = date.today()
    print(f"\n📅 Moon Calendar for {today.strftime('%B %Y')}:")
    print("-" * 40)
    
    calendar = get_moon_calendar(today.year, today.month)
    for day in calendar:
        marker = "★" if day["is_major_phase"] else " "
        print(f"{marker} {day['date']}: {day['phase_name']} {get_moon_emoji(datetime.strptime(day['date'], '%Y-%m-%d'))} ({day['illumination']:.0f}%)")
    
    # Blue moon info
    print("\n" + "-" * 40)
    blue_info = get_blue_moon_info(today.year)
    if blue_info["has_blue_moon"]:
        print(f"🔮 Blue Moons in {today.year}:")
        for bm in blue_info["blue_moons"]:
            print(f"   {bm['month_name']}: {bm['blue_moon']}")
    else:
        print(f"🔮 No blue moons in {today.year}")
    
    # Super moon check
    if is_super_moon():
        print("\n🌟 It's a SUPER MOON right now!")
    else:
        print("\n  Not currently a super moon.")
    
    # Moon distance
    distance = calculate_moon_distance()
    print(f"\n📏 Moon distance: {distance:,.0f} km")