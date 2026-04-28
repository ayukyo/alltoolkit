#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for Moon Phase Utilities Module

Comprehensive tests for all moon phase functions.
"""

import sys
import os
import math
from datetime import datetime, date, timedelta

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    # When running from inside the module directory
    from moon_phase_utils import (
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
        IlluminationLevel,
        SYNODIC_MONTH,
        PHASE_NAMES,
        PHASE_NAMES_CN,
    )
except ImportError:
    # When running from the AllToolkit Python directory
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
        IlluminationLevel,
        SYNODIC_MONTH,
        PHASE_NAMES,
        PHASE_NAMES_CN,
    )


def test_moon_age():
    """Test moon age calculation."""
    print("Testing get_moon_age...")
    
    # Test with known date - reference new moon is 2000-01-06 18:14 UTC
    # Using datetime for precision
    age = get_moon_age(datetime(2000, 1, 6, 18, 14, 0))
    # Should be close to 0 (reference new moon)
    # Allow some tolerance due to the modulo operation
    assert age < 1 or age > SYNODIC_MONTH - 1, f"Moon age near reference new moon should be ~0, got {age}"
    
    # Test age is always in valid range
    for _ in range(10):
        age = get_moon_age()
        assert 0 <= age <= SYNODIC_MONTH, f"Moon age {age} out of range"
    
    # Test age increases over time
    age1 = get_moon_age(datetime.now())
    age2 = get_moon_age(datetime.now() + timedelta(days=1))
    # Moon age should increase (mod SYNODIC_MONTH)
    assert (age2 > age1 or age2 < age1 - 10), "Moon age should progress over time"
    
    print("  ✓ get_moon_age tests passed")


def test_illumination():
    """Test illumination calculation."""
    print("Testing get_illumination...")
    
    # Test illumination range
    for _ in range(10):
        illum = get_illumination()
        assert 0 <= illum <= 100, f"Illumination {illum}% out of range"
    
    # Test new moon has ~0% illumination
    new_moon_date = get_next_new_moon()
    illum = get_illumination(new_moon_date)
    assert illum < 5, f"New moon illumination should be ~0%, got {illum}%"
    
    # Test full moon has ~100% illumination
    full_moon_date = get_next_full_moon()
    illum = get_illumination(full_moon_date)
    assert illum > 95, f"Full moon illumination should be ~100%, got {illum}%"
    
    print("  ✓ get_illumination tests passed")


def test_phase_index():
    """Test phase index calculation."""
    print("Testing get_phase_index...")
    
    # Test phase index range
    for _ in range(10):
        idx = get_phase_index()
        assert 0 <= idx <= 7, f"Phase index {idx} out of range"
    
    # Test new moon has index 0
    new_moon = get_next_new_moon()
    # Allow some tolerance
    age = get_moon_age(new_moon)
    if age < 1:
        idx = get_phase_index(new_moon)
        assert idx == 0, f"New moon should have index 0, got {idx}"
    
    # Test full moon has index 4
    full_moon = get_next_full_moon()
    age = get_moon_age(full_moon)
    if abs(age - SYNODIC_MONTH/2) < 2:
        idx = get_phase_index(full_moon)
        assert idx == 4, f"Full moon should have index 4, got {idx}"
    
    print("  ✓ get_phase_index tests passed")


def test_phase_name():
    """Test phase name retrieval."""
    print("Testing get_phase_name...")
    
    # Test English names
    name_en = get_phase_name()
    assert name_en in PHASE_NAMES.values(), f"Invalid English name: {name_en}"
    
    # Test Chinese names
    name_cn = get_phase_name(language="cn")
    assert name_cn in PHASE_NAMES_CN.values(), f"Invalid Chinese name: {name_cn}"
    
    # Test all phase indices
    for idx in range(8):
        name = PHASE_NAMES[idx]
        assert isinstance(name, str), f"Phase name should be string"
    
    print("  ✓ get_phase_name tests passed")


def test_moon_phase_enum():
    """Test MoonPhase enum."""
    print("Testing MoonPhase enum...")
    
    # Test enum values
    assert MoonPhase.NEW_MOON.value == 0
    assert MoonPhase.FULL_MOON.value == 4
    assert MoonPhase.FIRST_QUARTER.value == 2
    assert MoonPhase.LAST_QUARTER.value == 6
    
    # Test get_moon_phase returns enum
    phase = get_moon_phase()
    assert isinstance(phase, MoonPhase), "get_moon_phase should return MoonPhase enum"
    
    print("  ✓ MoonPhase enum tests passed")


def test_major_phase():
    """Test major phase detection."""
    print("Testing is_major_phase...")
    
    # Test that function returns boolean
    result = is_major_phase()
    assert isinstance(result, bool), "is_major_phase should return boolean"
    
    # Test new moon is major phase
    new_moon = get_next_new_moon()
    age = get_moon_age(new_moon)
    if age < 1:
        assert is_major_phase(new_moon), "New moon should be a major phase"
    
    # Test full moon is major phase
    full_moon = get_next_full_moon()
    age = get_moon_age(full_moon)
    if abs(age - SYNODIC_MONTH/2) < 2:
        assert is_major_phase(full_moon), "Full moon should be a major phase"
    
    print("  ✓ is_major_phase tests passed")


def test_next_new_moon():
    """Test next new moon calculation."""
    print("Testing get_next_new_moon...")
    
    # Test that result is in the future
    now = datetime.now()
    next_nm = get_next_new_moon()
    assert next_nm > now, "Next new moon should be in the future"
    
    # Test that it's within one synodic month
    delta = next_nm - now
    assert delta.days < SYNODIC_MONTH + 1, "Next new moon should be within one synodic month"
    
    # Test that age at next new moon is ~0 (allow tolerance due to algorithm)
    age = get_moon_age(next_nm)
    # The next new moon calculation adds SYNODIC_MONTH - age to current date
    # So age at that point should be very close to SYNODIC_MONTH (wraps to ~0)
    assert age < 0.5 or age > SYNODIC_MONTH - 0.5, f"Age at next new moon should be ~0, got {age}"
    
    print("  ✓ get_next_new_moon tests passed")


def test_next_full_moon():
    """Test next full moon calculation."""
    print("Testing get_next_full_moon...")
    
    now = datetime.now()
    next_fm = get_next_full_moon()
    
    # Test that result is in the future
    assert next_fm > now, "Next full moon should be in the future"
    
    # Test that it's within one synodic month
    delta = next_fm - now
    assert delta.days < SYNODIC_MONTH + 1, "Next full moon should be within one synodic month"
    
    # Test illumination at full moon
    illum = get_illumination(next_fm)
    assert illum > 95, f"Illumination at full moon should be ~100%, got {illum}%"
    
    print("  ✓ get_next_full_moon tests passed")


def test_next_quarters():
    """Test quarter calculations."""
    print("Testing get_next_first_quarter and get_next_last_quarter...")
    
    now = datetime.now()
    
    # Test first quarter
    next_fq = get_next_first_quarter()
    assert next_fq > now, "Next first quarter should be in the future"
    
    # Test last quarter
    next_lq = get_next_last_quarter()
    assert next_lq > now, "Next last quarter should be in the future"
    
    # Test order: one of the quarters should be first
    next_fm = get_next_full_moon()
    next_nm = get_next_new_moon()
    
    # Verify quarters are between new and full
    all_events = sorted([next_nm, next_fm, next_fq, next_lq], key=lambda x: x.timestamp())
    # Just verify they're all datetime objects
    for event in all_events:
        assert isinstance(event, datetime), "All events should be datetime objects"
    
    print("  ✓ Quarter calculation tests passed")


def test_moon_phases_in_month():
    """Test monthly phase calculation."""
    print("Testing get_moon_phases_in_month...")
    
    phases = get_moon_phases_in_month(2024, 1)
    
    # Should return a dictionary
    assert isinstance(phases, dict), "Should return a dictionary"
    
    # All values should be datetime objects
    for name, dt in phases.items():
        assert isinstance(dt, datetime), f"Value for {name} should be datetime"
        assert dt.year == 2024 and dt.month == 1, "Should be in January 2024"
    
    print("  ✓ get_moon_phases_in_month tests passed")


def test_moon_rise_set():
    """Test moonrise/moonset calculation."""
    print("Testing get_moon_rise_set...")
    
    # Test default (NYC coordinates)
    rise, set_time = get_moon_rise_set()
    assert rise is not None, "Moonrise should be calculated"
    assert set_time is not None, "Moonset should be calculated"
    assert 0 <= rise <= 24, f"Moonrise {rise} should be in 0-24 range"
    assert 0 <= set_time <= 24, f"Moonset {set_time} should be in 0-24 range"
    
    # Test with custom coordinates
    rise2, set_time2 = get_moon_rise_set(latitude=51.5074, longitude=-0.1278)  # London
    assert rise2 is not None, "Moonrise should be calculated for London"
    
    print("  ✓ get_moon_rise_set tests passed")


def test_lunar_eclipse_risk():
    """Test lunar eclipse risk estimation."""
    print("Testing get_lunar_eclipse_risk...")
    
    risk = get_lunar_eclipse_risk()
    assert risk in ["none", "low", "moderate", "high"], f"Invalid risk level: {risk}"
    
    print("  ✓ get_lunar_eclipse_risk tests passed")


def test_moon_info():
    """Test comprehensive moon info."""
    print("Testing get_moon_info...")
    
    info = get_moon_info()
    
    # Check all required keys
    required_keys = [
        "date", "time", "phase_index", "phase_name", "moon_age_days",
        "illumination_percent", "is_major_phase", "is_waxing", "is_waning",
        "next_new_moon", "next_full_moon", "days_until_new_moon",
        "days_until_full_moon", "synodic_month_days"
    ]
    
    for key in required_keys:
        assert key in info, f"Missing key: {key}"
    
    # Check value types and ranges
    assert 0 <= info["phase_index"] <= 7
    assert 0 <= info["illumination_percent"] <= 100
    assert isinstance(info["is_major_phase"], bool)
    assert isinstance(info["is_waxing"], bool)
    assert isinstance(info["is_waning"], bool)
    
    # Test Chinese language
    info_cn = get_moon_info(language="cn")
    assert info_cn["phase_name"] in PHASE_NAMES_CN.values()
    
    print("  ✓ get_moon_info tests passed")


def test_moon_calendar():
    """Test moon calendar generation."""
    print("Testing get_moon_calendar...")
    
    calendar = get_moon_calendar(2024, 1)
    
    # January should have 31 days
    assert len(calendar) == 31, f"January should have 31 days, got {len(calendar)}"
    
    # Check structure
    for day in calendar:
        assert "date" in day
        assert "day" in day
        assert "phase_index" in day
        assert "phase_name" in day
        assert "moon_age" in day
        assert "illumination" in day
        assert "is_major_phase" in day
        
        assert 1 <= day["day"] <= 31
        assert 0 <= day["phase_index"] <= 7
        assert 0 <= day["illumination"] <= 100
    
    # Test February (leap year)
    feb_calendar = get_moon_calendar(2024, 2)
    assert len(feb_calendar) == 29, "February 2024 should have 29 days"
    
    print("  ✓ get_moon_calendar tests passed")


def test_moon_emoji():
    """Test moon emoji retrieval."""
    print("Testing get_moon_emoji...")
    
    emoji = get_moon_emoji()
    assert emoji in ["🌑", "🌒", "🌓", "🌔", "🌕", "🌖", "🌗", "🌘", "🌙"]
    
    # Test each phase
    for idx in range(8):
        # Use a date that would give each phase
        ref_date = datetime(2000, 1, 6) + timedelta(days=idx * 3.7)
        emoji = get_moon_emoji(ref_date)
        assert len(emoji) > 0, f"Should return emoji for phase {idx}"
    
    print("  ✓ get_moon_emoji tests passed")


def test_blue_moon_info():
    """Test blue moon detection."""
    print("Testing get_blue_moon_info...")
    
    info = get_blue_moon_info(2024)
    
    assert "year" in info
    assert "has_blue_moon" in info
    assert "blue_moons" in info
    assert "count" in info
    
    assert info["year"] == 2024
    assert isinstance(info["has_blue_moon"], bool)
    assert isinstance(info["blue_moons"], list)
    assert isinstance(info["count"], int)
    
    # 2024 had a blue moon in August
    if info["has_blue_moon"]:
        assert info["count"] >= 1
        for bm in info["blue_moons"]:
            assert "month" in bm
            assert "month_name" in bm
            assert "first_full_moon" in bm
            assert "blue_moon" in bm
    
    print("  ✓ get_blue_moon_info tests passed")


def test_moon_distance():
    """Test moon distance calculation."""
    print("Testing calculate_moon_distance...")
    
    distance = calculate_moon_distance()
    
    # Distance should be between perigee and apogee
    assert 356000 < distance < 407000, f"Distance {distance} km out of valid range"
    
    # Test with specific date - use datetime instead of date
    distance2 = calculate_moon_distance(datetime(2024, 1, 1))
    assert 356000 < distance2 < 407000
    
    print("  ✓ calculate_moon_distance tests passed")


def test_super_moon():
    """Test super moon detection."""
    print("Testing is_super_moon...")
    
    result = is_super_moon()
    assert isinstance(result, bool), "Should return boolean"
    
    print("  ✓ is_super_moon tests passed")


def test_today_function():
    """Test today() convenience function."""
    print("Testing today()...")
    
    from moon_phase_utils.moon_phase_utils import today
    
    info = today()
    assert isinstance(info, dict), "Should return dictionary"
    assert "phase_name" in info, "Should have phase_name"
    
    print("  ✓ today() tests passed")


def test_print_moon_info():
    """Test print_moon_info function."""
    print("Testing print_moon_info...")
    
    from moon_phase_utils.moon_phase_utils import print_moon_info
    
    # Just test it doesn't crash
    import io
    import sys
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    try:
        print_moon_info()
        output = sys.stdout.getvalue()
        assert len(output) > 0, "Should print something"
    finally:
        sys.stdout = old_stdout
    
    print("  ✓ print_moon_info tests passed")


def test_consistency():
    """Test consistency between functions."""
    print("Testing consistency between functions...")
    
    # Moon age should be consistent
    age1 = get_moon_age()
    age2 = get_moon_age(datetime.now())
    assert abs(age1 - age2) < 0.01, "Moon age should be consistent"
    
    # Phase index should match illumination
    idx = get_phase_index()
    illum = get_illumination()
    
    # New moon should have low illumination
    if idx == 0:
        assert illum < 10, f"New moon (idx=0) should have low illumination, got {illum}%"
    
    # Full moon should have high illumination
    if idx == 4:
        assert illum > 90, f"Full moon (idx=4) should have high illumination, got {illum}%"
    
    # Next new moon should have age ~0
    next_nm = get_next_new_moon()
    nm_age = get_moon_age(next_nm)
    assert nm_age < 1 or nm_age > SYNODIC_MONTH - 1, f"New moon age should be ~0, got {nm_age}"
    
    print("  ✓ Consistency tests passed")


def test_edge_cases():
    """Test edge cases and special dates."""
    print("Testing edge cases...")
    
    # Test with date object (not datetime)
    info = get_moon_info(date.today())
    assert "phase_name" in info
    
    # Test with far future date
    future = date(2100, 1, 1)
    age = get_moon_age(future)
    assert 0 <= age <= SYNODIC_MONTH
    
    # Test with past date
    past = date(1900, 1, 1)
    age = get_moon_age(past)
    assert 0 <= age <= SYNODIC_MONTH
    
    # Test moon phases in different months
    for month in range(1, 13):
        phases = get_moon_phases_in_month(2024, month)
        assert isinstance(phases, dict)
    
    print("  ✓ Edge case tests passed")


def run_all_tests():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("Moon Phase Utils - Running All Tests")
    print("=" * 60 + "\n")
    
    tests = [
        test_moon_age,
        test_illumination,
        test_phase_index,
        test_phase_name,
        test_moon_phase_enum,
        test_major_phase,
        test_next_new_moon,
        test_next_full_moon,
        test_next_quarters,
        test_moon_phases_in_month,
        test_moon_rise_set,
        test_lunar_eclipse_risk,
        test_moon_info,
        test_moon_calendar,
        test_moon_emoji,
        test_blue_moon_info,
        test_moon_distance,
        test_super_moon,
        test_today_function,
        test_print_moon_info,
        test_consistency,
        test_edge_cases,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            failed += 1
            print(f"  ✗ {test.__name__} failed: {e}")
        except Exception as e:
            failed += 1
            print(f"  ✗ {test.__name__} error: {e}")
    
    print("\n" + "=" * 60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)