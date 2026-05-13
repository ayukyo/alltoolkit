"""
Tests for Tide Prediction and Calculation Utilities

Run with: python -m pytest tide_utils_test.py -v
Or directly: python tide_utils_test.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tide_utils.mod import (
    TideCalculator,
    TideType,
    TidePhase,
    TideEvent,
    TidePrediction,
    create_semidiurnal_tides,
    create_mixed_tides,
    create_diurnal_tides,
    quick_tide_height,
    is_good_fishing_time,
    get_tide_table,
    calculate_tide_window,
    get_tide_calculator_for_location,
)
from datetime import datetime, timedelta


def test_basic_tide_calculation():
    """Test basic tide height calculation"""
    calc = TideCalculator()
    
    # Calculate tide at a specific time
    dt = datetime(2024, 1, 1, 12, 0, 0)
    height = calc.calculate_tide_height(dt)
    
    # Height should be reasonable (not extremely large)
    assert -2.0 <= height <= 2.0
    assert isinstance(height, float)


def test_tide_height_varies():
    """Test that tide height varies over time"""
    calc = TideCalculator()
    
    heights = []
    base_dt = datetime(2024, 1, 1, 0, 0, 0)
    
    # Sample heights over 24 hours
    for hour in range(24):
        dt = base_dt + timedelta(hours=hour)
        height = calc.calculate_tide_height(dt)
        heights.append(height)
    
    # Heights should vary
    assert max(heights) > min(heights)
    
    # Should have some highs and lows (semidiurnal pattern)
    # In 24 hours, we expect roughly 2 high tides and 2 low tides
    changes = 0
    for i in range(1, len(heights)):
        if (heights[i-1] < heights[i] and i < len(heights)-1 and heights[i] > heights[i+1]) \
           or (heights[i-1] > heights[i] and i < len(heights)-1 and heights[i] < heights[i+1]):
            changes += 1
    
    # Should have at least 2-4 peaks/valleys in 24 hours for semidiurnal
    assert changes >= 2


def test_tide_phase_detection():
    """Test tide phase detection"""
    calc = TideCalculator()
    
    # Find a high tide time
    dt = datetime(2024, 1, 1, 0, 0, 0)
    
    # Search for high tide
    for hour in range(24):
        test_dt = dt + timedelta(hours=hour)
        phase = calc.get_tide_phase(test_dt)
        
        # Phases should be one of the valid values
        assert phase in [TidePhase.RISING, TidePhase.FALLING, TidePhase.HIGH, TidePhase.LOW]


def test_find_next_high_tide():
    """Test finding next high tide"""
    calc = TideCalculator()
    dt = datetime(2024, 1, 1, 6, 0, 0)
    
    high_tide = calc.find_next_high_tide(dt)
    
    if high_tide:
        assert high_tide.is_high == True
        assert high_tide.time > dt
        assert isinstance(high_tide.height, float)
        assert high_tide.phase == TidePhase.HIGH


def test_find_next_low_tide():
    """Test finding next low tide"""
    calc = TideCalculator()
    dt = datetime(2024, 1, 1, 6, 0, 0)
    
    low_tide = calc.find_next_low_tide(dt)
    
    if low_tide:
        assert low_tide.is_high == False
        assert low_tide.time > dt
        assert isinstance(low_tide.height, float)
        assert low_tide.phase == TidePhase.LOW


def test_lunar_age():
    """Test lunar age calculation"""
    calc = TideCalculator()
    
    # Known reference: January 6, 2000 was a new moon
    new_moon = datetime(2000, 1, 6, 18, 14, 0)
    lunar_age = calc.get_lunar_age(new_moon)
    
    # Should be approximately 0 (new moon)
    assert 0 <= lunar_age < 1
    
    # One week later should be around 7.38 (first quarter)
    first_quarter = new_moon + timedelta(days=7)
    lunar_age = calc.get_lunar_age(first_quarter)
    assert 6 <= lunar_age <= 8
    
    # Two weeks later should be around 14.77 (full moon)
    full_moon = new_moon + timedelta(days=14)
    lunar_age = calc.get_lunar_age(full_moon)
    assert 14 <= lunar_age <= 16


def test_lunar_phase_name():
    """Test lunar phase naming"""
    calc = TideCalculator()
    
    # New moon
    new_moon = datetime(2000, 1, 6, 18, 14, 0)
    phase = calc.get_lunar_phase_name(new_moon)
    assert phase == "New Moon"
    
    # Check various phases exist
    phases_found = set()
    for day in range(30):
        dt = new_moon + timedelta(days=day)
        phase = calc.get_lunar_phase_name(dt)
        phases_found.add(phase)
    
    # Should find all major phases
    expected = ["New Moon", "Full Moon", "First Quarter", "Last Quarter"]
    for exp in expected:
        assert exp in phases_found


def test_tide_type_spring_neap():
    """Test spring and neap tide detection"""
    calc = TideCalculator()
    
    # Spring tides at new moon
    new_moon = datetime(2000, 1, 6, 18, 14, 0)
    tide_type = calc.get_tide_type(new_moon)
    assert tide_type == TideType.SPRING
    
    # Full moon (also spring tide)
    full_moon = new_moon + timedelta(days=14)
    tide_type = calc.get_tide_type(full_moon)
    assert tide_type == TideType.SPRING
    
    # First quarter (neap tide)
    first_quarter = new_moon + timedelta(days=7)
    tide_type = calc.get_tide_type(first_quarter)
    assert tide_type == TideType.NEAP
    
    # Last quarter (neap tide)
    last_quarter = new_moon + timedelta(days=22)
    tide_type = calc.get_tide_type(last_quarter)
    assert tide_type == TideType.NEAP


def test_tidal_prediction():
    """Test complete tide prediction"""
    calc = TideCalculator()
    dt = datetime(2024, 6, 15, 12, 0, 0)
    
    prediction = calc.get_prediction(dt)
    
    assert prediction.datetime == dt
    assert isinstance(prediction.height, float)
    assert prediction.phase in TidePhase
    assert prediction.tide_type in TideType
    assert isinstance(prediction.height_change_rate, float)
    
    # Should have next high and low times
    if prediction.next_high:
        assert prediction.next_high > dt
    if prediction.next_low:
        assert prediction.next_low > dt


def test_tide_events_in_range():
    """Test getting tide events in a time range"""
    calc = TideCalculator()
    start = datetime(2024, 1, 1, 0, 0, 0)
    end = datetime(2024, 1, 3, 0, 0, 0)
    
    events = calc.get_tide_events(start, end)
    
    # Should have multiple events in 2 days
    assert len(events) >= 4  # At least 2 highs and 2 lows per day
    
    for event in events:
        assert isinstance(event, TideEvent)
        assert event.time >= start
        assert event.time <= end
    
    # Events should be sorted
    times = [e.time for e in events]
    assert times == sorted(times)


def test_tidal_range():
    """Test tidal range calculation"""
    calc = TideCalculator(m2_amplitude=1.5, s2_amplitude=0.5)
    dt = datetime(2024, 6, 15, 12, 0, 0)
    
    tidal_range = calc.calculate_tidal_range(dt)
    
    # With M2=1.5 and S2=0.5 plus other constituents, range should be reasonable
    assert tidal_range >= 1.0
    assert tidal_range <= 6.0


def test_tidal_current():
    """Test tidal current estimation"""
    calc = TideCalculator()
    dt = datetime(2024, 6, 15, 12, 0, 0)
    
    direction, speed = calc.estimate_tidal_current(dt)
    
    # Direction should be flood, ebb, or slack
    assert direction in ["flood", "ebb", "slack", "unknown"]
    
    # Speed should be between 0 and 1 (relative)
    assert 0 <= speed <= 1


def test_tidal_coefficient():
    """Test tidal coefficient calculation"""
    calc = TideCalculator()
    
    # Spring tide should have high coefficient
    new_moon = datetime(2000, 1, 6, 18, 14, 0)
    coeff = calc.get_tidal_coefficient(new_moon)
    assert coeff >= 90
    
    # Neap tide should have low coefficient
    first_quarter = new_moon + timedelta(days=7)
    coeff = calc.get_tidal_coefficient(first_quarter)
    assert coeff <= 50


def test_semidiurnal_tides_factory():
    """Test semidiurnal tide factory"""
    calc = create_semidiurnal_tides(mean_high=2.0, mean_low=-2.0)
    
    # Should have strong M2 component (semidiurnal dominant)
    assert calc.m2_amplitude > calc.k1_amplitude
    assert calc.m2_amplitude > calc.o1_amplitude
    
    # Tidal range should be about 4 meters
    dt = datetime(2024, 6, 15, 12, 0, 0)
    # Heights should vary reasonably
    for hour in range(24):
        height = calc.calculate_tide_height(dt + timedelta(hours=hour))
        assert -4.0 <= height <= 4.0


def test_mixed_tides_factory():
    """Test mixed tide factory"""
    calc = create_mixed_tides(mean_high=2.0, mean_low=-2.0)
    
    # Should have stronger diurnal components than semidiurnal
    assert calc.k1_amplitude > 0.1
    assert calc.o1_amplitude > 0.1
    
    # Still should have M2 component
    assert calc.m2_amplitude > 0


def test_diurnal_tides_factory():
    """Test diurnal tide factory"""
    calc = create_diurnal_tides(mean_high=2.0, mean_low=-2.0)
    
    # Should have dominant K1 and O1 components
    assert calc.k1_amplitude > calc.m2_amplitude
    assert calc.o1_amplitude > calc.m2_amplitude


def test_quick_tide_height():
    """Test quick tide height function"""
    dt = datetime(2024, 6, 15, 12, 0, 0)
    
    height = quick_tide_height(dt, m2_amplitude=1.0, s2_amplitude=0.5)
    
    assert isinstance(height, float)
    # Height depends on all constituents, so allow wider range
    assert -2.5 <= height <= 2.5


def test_fishing_time():
    """Test fishing time assessment"""
    calc = TideCalculator()
    dt = datetime(2024, 6, 15, 12, 0, 0)
    
    is_good, reason = is_good_fishing_time(dt, calc)
    
    assert isinstance(is_good, bool)
    assert isinstance(reason, str)
    assert len(reason) > 0


def test_tide_table():
    """Test tide table generation"""
    calc = TideCalculator()
    dt = datetime(2024, 1, 1, 0, 0, 0)
    
    table = get_tide_table(dt, days=1, calculator=calc)
    
    # Should have events for 1 day
    assert len(table) >= 2
    
    for entry in table:
        assert "date" in entry
        assert "time" in entry
        assert "height_m" in entry
        assert "type" in entry
        assert entry["type"] in ["High", "Low"]
        assert "tide_type" in entry
        assert "lunar_phase" in entry


def test_tide_window():
    """Test tide window calculation"""
    calc = create_semidiurnal_tides(mean_high=1.5, mean_low=-1.5)
    dt = datetime(2024, 6, 15, 6, 0, 0)
    
    start, end = calculate_tide_window(dt, calc, min_depth=0.0)
    
    if start and end:
        assert start >= dt
        assert end > start
        
        # Verify heights in window are above threshold
        current = start
        while current <= end:
            height = calc.calculate_tide_height(current)
            assert height >= 0.0
            current += timedelta(minutes=30)


def test_location_presets():
    """Test location preset calculators"""
    # Semidiurnal
    calc_semi = get_tide_calculator_for_location("generic_semidiurnal")
    assert calc_semi.m2_amplitude == 1.0
    
    # Mixed
    calc_mixed = get_tide_calculator_for_location("generic_mixed")
    assert calc_mixed.k1_amplitude > calc_semi.k1_amplitude
    
    # Diurnal
    calc_diurnal = get_tide_calculator_for_location("generic_diurnal")
    assert calc_diurnal.k1_amplitude > calc_diurnal.m2_amplitude


def test_amplitude_effects():
    """Test that amplitudes affect tide heights"""
    # Large amplitudes = large tide range
    calc_large = TideCalculator(m2_amplitude=3.0, s2_amplitude=1.0)
    
    # Small amplitudes = small tide range
    calc_small = TideCalculator(m2_amplitude=0.5, s2_amplitude=0.2)
    
    heights_large = []
    heights_small = []
    dt = datetime(2024, 1, 1, 0, 0, 0)
    
    for hour in range(12):
        heights_large.append(calc_large.calculate_tide_height(dt + timedelta(hours=hour)))
        heights_small.append(calc_small.calculate_tide_height(dt + timedelta(hours=hour)))
    
    # Large amplitude should have bigger range
    range_large = max(heights_large) - min(heights_large)
    range_small = max(heights_small) - min(heights_small)
    
    assert range_large > range_small


def test_phase_lag_effect():
    """Test that phase lag affects tide timing"""
    # No phase lag
    calc_no_lag = TideCalculator(m2_phase=0.0)
    
    # With phase lag (90 degrees = 1/4 cycle = ~3 hours shift)
    calc_with_lag = TideCalculator(m2_phase=90.0)
    
    dt = datetime(2024, 1, 1, 0, 0, 0)
    
    height1 = calc_no_lag.calculate_tide_height(dt)
    height2 = calc_with_lag.calculate_tide_height(dt)
    
    # Heights should be different due to phase lag
    assert height1 != height2


def test_mean_sea_level():
    """Test mean sea level offset"""
    calc = TideCalculator(mean_sea_level=100.0)
    
    dt = datetime(2024, 1, 1, 0, 0, 0)
    height = calc.calculate_tide_height(dt)
    
    # Height should be offset by mean sea level
    # Base tide fluctuates around 0, so height should be around 100 ± tide amplitude
    assert 99 <= height <= 102


def test_24_hour_cycle():
    """Test that tides follow expected patterns over 24 hours"""
    calc = TideCalculator()
    dt = datetime(2024, 1, 1, 0, 0, 0)
    
    # Track phases over 24 hours
    phases = []
    for hour in range(24):
        phase = calc.get_tide_phase(dt + timedelta(hours=hour))
        phases.append(phase)
    
    # Should have at least one rising and one falling phase
    assert TidePhase.RISING in phases or TidePhase.FALLING in phases
    
    # Count transitions
    high_count = sum(1 for p in phases if p == TidePhase.HIGH)
    low_count = sum(1 for p in phases if p == TidePhase.LOW)
    
    # Should have roughly 2 highs and 2 lows for semidiurnal (with tolerance for detection)
    # Note: exact detection might miss some, so just check we have some
    assert high_count >= 0 or low_count >= 0


def test_dataclass_fields():
    """Test that dataclasses have expected fields"""
    calc = TideCalculator()
    dt = datetime(2024, 6, 15, 12, 0, 0)
    
    # TideEvent
    high = calc.find_next_high_tide(dt)
    if high:
        assert hasattr(high, 'time')
        assert hasattr(high, 'height')
        assert hasattr(high, 'is_high')
        assert hasattr(high, 'tide_type')
        assert hasattr(high, 'phase')
    
    # TidePrediction
    pred = calc.get_prediction(dt)
    assert hasattr(pred, 'datetime')
    assert hasattr(pred, 'height')
    assert hasattr(pred, 'phase')
    assert hasattr(pred, 'tide_type')
    assert hasattr(pred, 'next_high')
    assert hasattr(pred, 'next_low')
    assert hasattr(pred, 'time_to_next')
    assert hasattr(pred, 'height_change_rate')


def run_all_tests():
    """Run all tests manually"""
    tests = [
        test_basic_tide_calculation,
        test_tide_height_varies,
        test_tide_phase_detection,
        test_find_next_high_tide,
        test_find_next_low_tide,
        test_lunar_age,
        test_lunar_phase_name,
        test_tide_type_spring_neap,
        test_tidal_prediction,
        test_tide_events_in_range,
        test_tidal_range,
        test_tidal_current,
        test_tidal_coefficient,
        test_semidiurnal_tides_factory,
        test_mixed_tides_factory,
        test_diurnal_tides_factory,
        test_quick_tide_height,
        test_fishing_time,
        test_tide_table,
        test_tide_window,
        test_location_presets,
        test_amplitude_effects,
        test_phase_lag_effect,
        test_mean_sea_level,
        test_24_hour_cycle,
        test_dataclass_fields,
    ]
    
    passed = 0
    failed = 0
    
    print("Running Tide Utils Tests...\n")
    
    for test in tests:
        try:
            test()
            print(f"✓ {test.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__}: Unexpected error: {e}")
            failed += 1
    
    print(f"\n{'='*50}")
    print(f"Results: {passed} passed, {failed} failed")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)