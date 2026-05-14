"""
Comprehensive tests for Jet Lag Calculator Utils.

Tests all core functionality including:
- Time difference calculations
- Severity scoring
- Recovery time estimation
- Direction handling (east vs west)
- Sleep type and age factors
- Light exposure timing
- Sleep schedule recommendations
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    JetLagCalculator,
    JetLagResult,
    TimezoneInfo,
    SleepType,
    TravelDirection,
    SleepSchedule,
    calculate_jet_lag,
    get_common_timezones,
    quick_estimate,
    analyze_route,
    POPULAR_ROUTES,
)
from datetime import time, datetime


def test_timezone_info():
    """Test TimezoneInfo creation and methods."""
    print("Testing TimezoneInfo...")
    
    # Test basic creation
    tz = TimezoneInfo(name="PST", utc_offset=-8)
    assert tz.name == "PST"
    assert tz.utc_offset == -8
    
    # Test from_utc_offset
    tz2 = TimezoneInfo.from_utc_offset(5.5)
    assert tz2.utc_offset == 5.5
    assert "5.5" in tz2.name
    
    tz3 = TimezoneInfo.from_utc_offset(-5, "EST")
    assert tz3.name == "EST"
    assert tz3.utc_offset == -5
    
    print("  ✓ TimezoneInfo tests passed")


def test_travel_direction():
    """Test travel direction enumeration."""
    print("Testing TravelDirection...")
    
    assert TravelDirection.EAST.value == "east"
    assert TravelDirection.WEST.value == "west"
    assert TravelDirection.NONE.value == "none"
    
    print("  ✓ TravelDirection tests passed")


def test_sleep_type():
    """Test sleep type enumeration."""
    print("Testing SleepType...")
    
    assert SleepType.MORNING_LARK.value == "morning_lark"
    assert SleepType.NIGHT_OWL.value == "night_owl"
    assert SleepType.INTERMEDIATE.value == "intermediate"
    
    print("  ✓ SleepType tests passed")


def test_sleep_schedule():
    """Test SleepSchedule dataclass."""
    print("Testing SleepSchedule...")
    
    schedule = SleepSchedule(
        bed_time=time(23, 0),
        wake_time=time(7, 0),
        duration=8.0
    )
    
    assert schedule.bed_time == time(23, 0)
    assert schedule.wake_time == time(7, 0)
    assert schedule.duration == 8.0
    assert "23:00" in str(schedule)
    assert "07:00" in str(schedule)
    
    print("  ✓ SleepSchedule tests passed")


def test_calculator_initialization():
    """Test JetLagCalculator initialization."""
    print("Testing JetLagCalculator initialization...")
    
    # Default initialization
    calc = JetLagCalculator()
    assert calc.age == 30
    assert calc.sleep_type == SleepType.INTERMEDIATE
    assert calc.typical_bed_time == time(23, 0)
    assert calc.typical_wake_time == time(7, 0)
    
    # Custom initialization
    calc2 = JetLagCalculator(
        age=45,
        sleep_type=SleepType.NIGHT_OWL,
        typical_bed_time=time(1, 0),
        typical_wake_time=time(9, 0)
    )
    assert calc2.age == 45
    assert calc2.sleep_type == SleepType.NIGHT_OWL
    assert calc2.typical_bed_time == time(1, 0)
    
    print("  ✓ JetLagCalculator initialization tests passed")


def test_no_time_difference():
    """Test calculation with no time difference."""
    print("Testing no time difference...")
    
    calc = JetLagCalculator()
    origin = TimezoneInfo.from_utc_offset(-5, "EST")
    dest = TimezoneInfo.from_utc_offset(-5, "EST")
    
    result = calc.calculate(origin, dest)
    
    assert result.time_difference == 0
    assert result.direction == TravelDirection.NONE
    assert result.severity_score == 0
    assert result.severity_level == "Minimal"
    assert result.estimated_recovery_days == 0
    
    print("  ✓ No time difference tests passed")


def test_small_time_difference():
    """Test calculation with small time difference (1-2 hours)."""
    print("Testing small time difference...")
    
    calc = JetLagCalculator()
    
    # 1 hour east
    origin = TimezoneInfo.from_utc_offset(-5, "EST")
    dest = TimezoneInfo.from_utc_offset(-4, "EDT")
    
    result = calc.calculate(origin, dest)
    
    assert result.time_difference == 1
    assert result.direction == TravelDirection.EAST
    assert result.severity_score < 25  # Should be mild
    assert result.estimated_recovery_days < 2
    
    print("  ✓ Small time difference tests passed")


def test_moderate_time_difference():
    """Test calculation with moderate time difference (3-6 hours)."""
    print("Testing moderate time difference...")
    
    calc = JetLagCalculator()
    
    # LA to New York (3 hours east)
    origin = TimezoneInfo.from_utc_offset(-8, "PST")
    dest = TimezoneInfo.from_utc_offset(-5, "EST")
    
    result = calc.calculate(origin, dest)
    
    assert abs(result.time_difference) == 3
    assert result.direction == TravelDirection.EAST
    assert 25 <= result.severity_score < 60  # Should be moderate
    assert result.severity_level in ["Mild", "Moderate"]
    assert result.estimated_recovery_days >= 2
    
    print("  ✓ Moderate time difference tests passed")


def test_large_time_difference():
    """Test calculation with large time difference (6+ hours)."""
    print("Testing large time difference...")
    
    calc = JetLagCalculator()
    
    # New York to London (5 hours east)
    origin = TimezoneInfo.from_utc_offset(-5, "EST")
    dest = TimezoneInfo.from_utc_offset(0, "GMT")
    
    result = calc.calculate(origin, dest)
    
    assert result.time_difference == 5
    assert result.direction == TravelDirection.EAST
    assert result.severity_score >= 30
    assert len(result.recommendations) > 3
    
    print("  ✓ Large time difference tests passed")


def test_extreme_time_difference():
    """Test calculation with extreme time difference (10+ hours)."""
    print("Testing extreme time difference...")
    
    calc = JetLagCalculator()
    
    # LA to Tokyo (17 hours east, but normalizes to 7 hours west)
    origin = TimezoneInfo.from_utc_offset(-8, "PST")
    dest = TimezoneInfo.from_utc_offset(9, "JST")
    
    result = calc.calculate(origin, dest)
    
    # Should normalize the time difference
    assert abs(result.time_difference) <= 12
    assert result.severity_score > 40
    assert result.severity_level in ["Moderate", "Severe", "Extreme"]
    assert result.estimated_recovery_days > 3
    assert len(result.recommendations) >= 5
    
    print("  ✓ Extreme time difference tests passed")


def test_east_vs_west_travel():
    """Test that eastward travel is correctly identified as more difficult."""
    print("Testing east vs west travel...")
    
    calc = JetLagCalculator()
    
    # Eastward travel (NYC to London)
    origin_east = TimezoneInfo.from_utc_offset(-5, "EST")
    dest_east = TimezoneInfo.from_utc_offset(0, "GMT")
    result_east = calc.calculate(origin_east, dest_east)
    
    # Westward travel (same distance)
    origin_west = TimezoneInfo.from_utc_offset(0, "GMT")
    dest_west = TimezoneInfo.from_utc_offset(-5, "EST")
    result_west = calc.calculate(origin_west, dest_west)
    
    assert result_east.direction == TravelDirection.EAST
    assert result_west.direction == TravelDirection.WEST
    
    # East should be more severe (harder to adjust)
    assert result_east.severity_score > result_west.severity_score
    
    # West should recover faster
    assert result_east.estimated_recovery_days > result_west.estimated_recovery_days
    
    print("  ✓ East vs west travel tests passed")


def test_age_factors():
    """Test that age affects recovery time."""
    print("Testing age factors...")
    
    origin = TimezoneInfo.from_utc_offset(-5, "EST")
    dest = TimezoneInfo.from_utc_offset(5, "IST")
    
    # Young person (recovers faster)
    calc_young = JetLagCalculator(age=20)
    result_young = calc_young.calculate(origin, dest)
    
    # Middle-aged (baseline)
    calc_middle = JetLagCalculator(age=35)
    result_middle = calc_middle.calculate(origin, dest)
    
    # Older person (recovers slower)
    calc_older = JetLagCalculator(age=65)
    result_older = calc_older.calculate(origin, dest)
    
    # Young should recover fastest
    assert result_young.estimated_recovery_days < result_middle.estimated_recovery_days
    
    # Older should recover slowest
    assert result_older.estimated_recovery_days > result_middle.estimated_recovery_days
    
    print("  ✓ Age factor tests passed")


def test_sleep_type_factors():
    """Test that sleep type affects recommendations."""
    print("Testing sleep type factors...")
    
    origin = TimezoneInfo.from_utc_offset(-5, "EST")
    dest = TimezoneInfo.from_utc_offset(2, "CEST")
    
    # Night owl going east (struggles more)
    calc_owl = JetLagCalculator(sleep_type=SleepType.NIGHT_OWL)
    result_owl = calc_owl.calculate(origin, dest)
    
    # Morning lark going west (struggles more)
    calc_lark = JetLagCalculator(sleep_type=SleepType.MORNING_LARK)
    result_lark = calc_lark.calculate(dest, origin)  # Reverse direction
    
    # Intermediate
    calc_mid = JetLagCalculator(sleep_type=SleepType.INTERMEDIATE)
    result_mid = calc_mid.calculate(origin, dest)
    
    # Night owl should have higher severity for east travel
    assert result_owl.severity_score > result_mid.severity_score
    
    print("  ✓ Sleep type factor tests passed")


def test_light_exposure_east():
    """Test light exposure recommendations for eastward travel."""
    print("Testing light exposure (eastward)...")
    
    calc = JetLagCalculator()
    origin = TimezoneInfo.from_utc_offset(-8, "PST")
    dest = TimezoneInfo.from_utc_offset(0, "GMT")
    
    result = calc.calculate(origin, dest)
    
    # For east travel, want morning light
    light_times = result.light_exposure_times
    
    assert "morning" in light_times
    assert "bright" in light_times["morning"].lower() or "light" in light_times["morning"].lower()
    
    # Should avoid bright light in evening
    assert "evening" in light_times
    
    print("  ✓ Light exposure (eastward) tests passed")


def test_light_exposure_west():
    """Test light exposure recommendations for westward travel."""
    print("Testing light exposure (westward)...")
    
    calc = JetLagCalculator()
    origin = TimezoneInfo.from_utc_offset(0, "GMT")
    dest = TimezoneInfo.from_utc_offset(-8, "PST")
    
    result = calc.calculate(origin, dest)
    
    light_times = result.light_exposure_times
    
    # For west travel, want evening light
    assert "morning" in light_times
    assert "evening" in light_times
    
    # Morning should mention avoiding bright light
    assert "avoid" in light_times["morning"].lower() or "dim" in light_times["morning"].lower()
    
    print("  ✓ Light exposure (westward) tests passed")


def test_sleep_schedule():
    """Test sleep schedule recommendations."""
    print("Testing sleep schedule recommendations...")
    
    calc = JetLagCalculator()
    origin = TimezoneInfo.from_utc_offset(-5, "EST")
    dest = TimezoneInfo.from_utc_offset(8, "CST_China")
    
    result = calc.calculate(origin, dest)
    
    schedule = result.optimal_sleep_schedule
    
    # Should have strategy
    assert "strategy" in schedule or "day_1" in schedule
    
    # For large time difference, should have multiple days
    if abs(result.time_difference) > 3:
        assert len(schedule) > 2
    
    print("  ✓ Sleep schedule tests passed")


def test_recommendations():
    """Test that recommendations are generated."""
    print("Testing recommendations...")
    
    calc = JetLagCalculator()
    origin = TimezoneInfo.from_utc_offset(-5, "EST")
    dest = TimezoneInfo.from_utc_offset(9, "JST")
    
    result = calc.calculate(origin, dest)
    
    # Should have recommendations
    assert len(result.recommendations) > 0
    
    # Recommendations should be strings
    for rec in result.recommendations:
        assert isinstance(rec, str)
        assert len(rec) > 10  # Should be meaningful text
    
    print("  ✓ Recommendations tests passed")


def test_convenience_function():
    """Test the convenience calculate_jet_lag function."""
    print("Testing convenience function...")
    
    result = calculate_jet_lag(
        origin_offset=-8,
        destination_offset=9,
        age=30,
        sleep_type="intermediate"
    )
    
    assert isinstance(result, JetLagResult)
    assert result.time_difference != 0
    assert len(result.recommendations) > 0
    
    print("  ✓ Convenience function tests passed")


def test_get_common_timezones():
    """Test common timezones dictionary."""
    print("Testing common timezones...")
    
    timezones = get_common_timezones()
    
    assert isinstance(timezones, dict)
    assert len(timezones) > 10
    
    # Check some expected timezones
    assert "UTC" in timezones
    assert timezones["UTC"] == 0
    assert "EST" in timezones
    assert "JST" in timezones
    
    print("  ✓ Common timezones tests passed")


def test_quick_estimate():
    """Test quick estimate function."""
    print("Testing quick estimate...")
    
    # No difference
    result = quick_estimate(0)
    assert result["needs_adjustment"] == False
    
    # Small difference
    result = quick_estimate(2)
    assert result["needs_adjustment"] == True
    assert result["time_difference_hours"] == 2
    assert result["estimated_recovery_days"] > 0
    
    # Large difference
    result = quick_estimate(10)
    assert result["needs_adjustment"] == True
    assert result["estimated_recovery_days"] > 5
    
    print("  ✓ Quick estimate tests passed")


def test_analyze_route():
    """Test route analysis function."""
    print("Testing route analysis...")
    
    # Test known route
    result = analyze_route("LAX", "JFK", age=30)
    
    assert result is not None
    assert "route_name" in result
    assert "time_difference" in result
    assert "direction" in result
    assert "severity" in result
    assert "recovery_days" in result
    
    # Test unknown route
    result = analyze_route("XXX", "YYY")
    assert result is None
    
    print("  ✓ Route analysis tests passed")


def test_popular_routes():
    """Test that popular routes are valid."""
    print("Testing popular routes...")
    
    assert len(POPULAR_ROUTES) > 0
    
    for route_key, route_info in POPULAR_ROUTES.items():
        assert len(route_key) == 2
        assert "origin" in route_info
        assert "dest" in route_info
        assert "name" in route_info
        
        # Should be able to calculate for each route
        result = calculate_jet_lag(route_info["origin"], route_info["dest"])
        assert isinstance(result, JetLagResult)
    
    print("  ✓ Popular routes tests passed")


def test_recovery_timeline():
    """Test recovery timeline generation."""
    print("Testing recovery timeline...")
    
    calc = JetLagCalculator()
    origin = TimezoneInfo.from_utc_offset(-5, "EST")
    dest = TimezoneInfo.from_utc_offset(9, "JST")
    
    result = calc.calculate(origin, dest)
    timeline = calc.get_recovery_timeline(result)
    
    assert len(timeline) > 0
    
    # Each day should have required fields
    for day in timeline:
        assert "day" in day
        assert "date" in day
        assert "remaining_shift_hours" in day
        assert "percent_recovered" in day
        assert "status" in day
    
    # First day should have 0% recovery
    assert timeline[0]["percent_recovered"] == 0
    
    # Last day should be fully adjusted or close
    assert timeline[-1]["status"] in ["adjusting", "fully_adjusted"]
    
    print("  ✓ Recovery timeline tests passed")


def test_recovery_timeline_with_date():
    """Test recovery timeline with specific start date."""
    print("Testing recovery timeline with date...")
    
    calc = JetLagCalculator()
    origin = TimezoneInfo.from_utc_offset(-5, "EST")
    dest = TimezoneInfo.from_utc_offset(5, "IST")
    
    result = calc.calculate(origin, dest)
    start_date = datetime(2025, 1, 15)
    
    timeline = calc.get_recovery_timeline(result, start_date)
    
    # First date should be the start date
    assert timeline[0]["date"] == "2025-01-15"
    
    # Each subsequent day should be +1
    for i, day in enumerate(timeline):
        expected_date = datetime(2025, 1, 15) + __import__('datetime').timedelta(days=i)
        assert day["date"] == expected_date.strftime("%Y-%m-%d")
    
    print("  ✓ Recovery timeline with date tests passed")


def test_normalization():
    """Test time difference normalization (e.g., 17 hours = 7 hours the other way)."""
    print("Testing time difference normalization...")
    
    calc = JetLagCalculator()
    
    # 17 hours east should normalize to 7 hours west
    origin = TimezoneInfo.from_utc_offset(-8, "PST")
    dest = TimezoneInfo.from_utc_offset(9, "JST")
    
    result = calc.calculate(origin, dest)
    
    # Should be normalized to <= 12
    assert abs(result.time_difference) <= 12
    
    print("  ✓ Normalization tests passed")


def test_severity_levels():
    """Test all severity levels are achievable."""
    print("Testing severity levels...")
    
    calc = JetLagCalculator()
    
    levels_found = set()
    
    # Test various time differences
    for hours in [0, 1, 2, 3, 4, 5, 6, 8, 10, 12]:
        origin = TimezoneInfo.from_utc_offset(0, "UTC")
        dest = TimezoneInfo.from_utc_offset(hours, f"UTC+{hours}")
        result = calc.calculate(origin, dest)
        levels_found.add(result.severity_level)
    
    # Should have found multiple levels
    assert len(levels_found) >= 2
    
    print("  ✓ Severity levels tests passed")


def test_result_dataclass():
    """Test JetLagResult dataclass structure."""
    print("Testing JetLagResult dataclass...")
    
    calc = JetLagCalculator()
    origin = TimezoneInfo.from_utc_offset(-5, "EST")
    dest = TimezoneInfo.from_utc_offset(9, "JST")
    
    result = calc.calculate(origin, dest)
    
    # Check all fields exist
    assert hasattr(result, 'time_difference')
    assert hasattr(result, 'direction')
    assert hasattr(result, 'severity_score')
    assert hasattr(result, 'severity_level')
    assert hasattr(result, 'estimated_recovery_days')
    assert hasattr(result, 'adjustment_per_day')
    assert hasattr(result, 'recommendations')
    assert hasattr(result, 'optimal_sleep_schedule')
    assert hasattr(result, 'light_exposure_times')
    assert hasattr(result, 'phase_shift_needed')
    
    print("  ✓ JetLagResult dataclass tests passed")


def run_all_tests():
    """Run all test functions."""
    print("\n" + "="*60)
    print("Jet Lag Calculator Utils - Comprehensive Test Suite")
    print("="*60 + "\n")
    
    tests = [
        test_timezone_info,
        test_travel_direction,
        test_sleep_type,
        test_sleep_schedule,
        test_calculator_initialization,
        test_no_time_difference,
        test_small_time_difference,
        test_moderate_time_difference,
        test_large_time_difference,
        test_extreme_time_difference,
        test_east_vs_west_travel,
        test_age_factors,
        test_sleep_type_factors,
        test_light_exposure_east,
        test_light_exposure_west,
        test_sleep_schedule,
        test_recommendations,
        test_convenience_function,
        test_get_common_timezones,
        test_quick_estimate,
        test_analyze_route,
        test_popular_routes,
        test_recovery_timeline,
        test_recovery_timeline_with_date,
        test_normalization,
        test_severity_levels,
        test_result_dataclass,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"  ✗ FAILED: {test.__name__}")
            print(f"    Error: {e}")
            failed += 1
        except Exception as e:
            print(f"  ✗ ERROR: {test.__name__}")
            print(f"    Error: {e}")
            failed += 1
    
    print("\n" + "="*60)
    print(f"Results: {passed} passed, {failed} failed")
    print("="*60 + "\n")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)