"""
Tests for Lightning Distance Calculator Utilities

Run with: python -m pytest lightning_distance_utils_test.py -v
Or directly: python lightning_distance_utils_test.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lightning_distance_utils.mod import (
    LightningDistanceCalculator,
    DistanceUnit,
    SafetyLevel,
    LightningStrike,
    quick_distance,
    quick_distance_miles,
    rule_of_thumb_distance,
    estimate_thunder_arrival,
    get_safe_shelter_time,
    is_lightning_safe,
    thunder_volume_estimate,
    calculate_strike_angle,
    flash_to_bang_kilometers,
    flash_to_bang_miles,
    SECONDS_PER_KM,
    SECONDS_PER_MILE
)


def test_basic_distance_calculation():
    """Test basic distance calculation from time delay"""
    calc = LightningDistanceCalculator(temperature_celsius=20.0)
    
    # At 20°C, speed of sound ≈ 343.42 m/s
    # 5 seconds delay = 343.42 * 5 = 1717.1 m ≈ 1.72 km
    result = calc.calculate_distance(5.0)
    
    assert result.time_delay_seconds == 5.0
    assert result.temperature_celsius == 20.0
    assert 1.7 <= result.distance_km <= 1.8
    assert 1.0 <= result.distance_miles <= 1.2
    assert result.safety_level == SafetyLevel.IMMEDIATE
    assert result.is_dangerous == True


def test_temperature_effect():
    """Test that temperature affects speed of sound and distance calculation"""
    calc_cold = LightningDistanceCalculator(temperature_celsius=0.0)
    calc_hot = LightningDistanceCalculator(temperature_celsius=40.0)
    
    result_cold = calc_cold.calculate_distance(5.0)
    result_hot = calc_hot.calculate_distance(5.0)
    
    # Sound travels faster in warmer air
    assert calc_cold.speed_of_sound < calc_hot.speed_of_sound
    assert result_cold.distance_km < result_hot.distance_km
    
    # At 0°C: ~331.3 m/s, at 40°C: ~355.54 m/s
    assert 330 <= calc_cold.speed_of_sound <= 332
    assert 354 <= calc_hot.speed_of_sound <= 357


def test_safety_levels():
    """Test safety level determination"""
    calc = LightningDistanceCalculator()
    
    # Safe: > 15 km
    result = calc.calculate_distance(50.0)  # ~17 km
    assert result.safety_level == SafetyLevel.SAFE
    
    # Caution: 10-15 km
    result = calc.calculate_distance(40.0)  # ~13.7 km
    assert result.safety_level == SafetyLevel.CAUTION
    
    # Danger: 6-10 km
    result = calc.calculate_distance(22.0)  # ~7.5 km
    assert result.safety_level == SafetyLevel.DANGER
    
    # Immediate: < 3 km
    result = calc.calculate_distance(8.0)  # ~2.7 km
    assert result.safety_level == SafetyLevel.IMMEDIATE


def test_quick_distance_functions():
    """Test convenience distance calculation functions"""
    # quick_distance returns km
    km = quick_distance(5.0, temperature=20.0)
    assert 1.7 <= km <= 1.8
    
    # quick_distance_miles returns miles
    miles = quick_distance_miles(5.0, temperature=20.0)
    assert 1.0 <= miles <= 1.2


def test_rule_of_thumb():
    """Test rule of thumb calculations"""
    result = rule_of_thumb_distance(15.0)
    
    # 15 seconds / 3 = 5 km
    assert result["rule_of_thumb_km"] == 5.0
    
    # 15 seconds / 5 = 3 miles
    assert result["rule_of_thumb_miles"] == 3.0
    
    assert "explanation" in result
    assert "time_seconds" in result


def test_estimate_thunder_arrival():
    """Test thunder arrival time estimation"""
    # 5 km away should take about 14.5 seconds
    time_seconds = estimate_thunder_arrival(5.0, temperature=20.0)
    assert 14 <= time_seconds <= 15


def test_safe_shelter_time():
    """Test safe shelter time calculation"""
    # At 40 km/h, 10 km away = 15 minutes
    minutes = get_safe_shelter_time(10.0)
    assert 14 <= minutes <= 16
    
    # 20 km away = 30 minutes
    minutes = get_safe_shelter_time(20.0)
    assert 29 <= minutes <= 31


def test_is_lightning_safe():
    """Test outdoor activity safety assessment"""
    # Immediate danger zone
    safe, msg = is_lightning_safe("swimming", 2.0)
    assert safe == False
    assert "immediately" in msg.lower()
    
    # Danger zone
    safe, msg = is_lightning_safe("hiking", 8.0)
    assert safe == False
    assert "30-30" in msg
    
    # Caution zone
    safe, msg = is_lightning_safe("sports", 12.0)
    assert safe == True
    assert "Caution" in msg
    
    # Safe zone
    safe, msg = is_lightning_safe("picnic", 20.0)
    assert safe == True
    assert "safe" in msg.lower()


def test_thunder_volume_estimate():
    """Test thunder volume estimation"""
    assert "Extremely loud" in thunder_volume_estimate(0.3)
    assert "Very loud" in thunder_volume_estimate(1.0)
    assert "Loud" in thunder_volume_estimate(3.0)
    assert "Moderate" in thunder_volume_estimate(7.0)
    assert "Faint" in thunder_volume_estimate(15.0)
    assert "Very faint" in thunder_volume_estimate(25.0)


def test_count_strikes():
    """Test multiple strike analysis"""
    calc = LightningDistanceCalculator()
    
    strikes = [20.0, 18.0, 15.0, 12.0, 10.0]  # Approaching storm
    result = calc.count_strikes(strikes)
    
    assert result["total_strikes"] == 5
    assert "average_distance_km" in result
    assert "closest_strike_km" in result
    assert "farthest_strike_km" in result
    assert result["storm_approaching"] == True
    
    # Receding storm
    strikes = [10.0, 12.0, 15.0, 18.0, 20.0]
    result = calc.count_strikes(strikes)
    assert result["storm_approaching"] == False


def test_safety_recommendation():
    """Test safety recommendation messages"""
    calc = LightningDistanceCalculator()
    
    # Safe distance
    result = calc.calculate_distance(50.0)
    msg = calc.get_safety_recommendation(result)
    assert "safe" in msg.lower()
    
    # Danger distance
    result = calc.calculate_distance(20.0)
    msg = calc.get_safety_recommendation(result)
    assert "DANGER" in msg or "seek shelter" in msg.lower()
    
    # Immediate danger
    result = calc.calculate_distance(5.0)
    msg = calc.get_safety_recommendation(result)
    assert "CRITICAL" in msg or "immediate" in msg.lower()


def test_calculate_strike_angle():
    """Test triangulation calculation"""
    # Two observers at different positions
    # Observer 1 at (0, 0), Observer 2 at (10, 0)
    # Both see lightning, with different time delays
    
    # If strike is at (5, 5):
    # Distance from Observer 1: sqrt(25 + 25) ≈ 7.07 km
    # Distance from Observer 2: sqrt(25 + 25) ≈ 7.07 km
    # Time delay ≈ 20.6 seconds each
    
    time_delays = [20.6, 20.6]
    positions = [(0.0, 0.0), (10.0, 0.0)]
    
    result = calculate_strike_angle(time_delays, positions)
    
    # Should be approximately (5, 5)
    if result:
        x, y = result
        assert 4 <= x <= 6
        assert 4 <= y <= 6


def test_calculate_strike_angle_insufficient_data():
    """Test triangulation with insufficient data"""
    # Only one observer
    result = calculate_strike_angle([5.0], [(0.0, 0.0)])
    assert result is None
    
    # Mismatched data
    result = calculate_strike_angle([5.0, 6.0], [(0.0, 0.0)])
    assert result is None


def test_flash_to_bang_convenience_functions():
    """Test simple flash-to-bang calculations"""
    # 5 seconds ≈ 1.72 km
    km = flash_to_bang_kilometers(5.0)
    assert 1.7 <= km <= 1.8
    
    # 5 seconds ≈ 1.06 miles
    miles = flash_to_bang_miles(5.0)
    assert 1.0 <= miles <= 1.2


def test_constants():
    """Test that constants are reasonable"""
    # At 20°C, sound travels ~343 m/s
    # So 1 km takes about 2.9 seconds
    assert 2.5 <= SECONDS_PER_KM <= 3.5
    
    # 1 mile = 1.609 km
    # So 1 mile takes about 4.7 seconds
    assert 4.0 <= SECONDS_PER_MILE <= 5.5


def test_set_temperature():
    """Test temperature update functionality"""
    calc = LightningDistanceCalculator(temperature_celsius=20.0)
    initial_speed = calc.speed_of_sound
    
    calc.set_temperature(40.0)
    
    assert calc.temperature_celsius == 40.0
    assert calc.speed_of_sound > initial_speed


def test_zero_delay():
    """Test zero time delay (immediate thunder)"""
    calc = LightningDistanceCalculator()
    result = calc.calculate_distance(0.0)
    
    assert result.distance_km == 0.0
    assert result.distance_miles == 0.0
    assert result.safety_level == SafetyLevel.IMMEDIATE
    assert result.is_dangerous == True


def test_large_distance():
    """Test large distance calculation"""
    calc = LightningDistanceCalculator()
    result = calc.calculate_distance(100.0)  # ~34 km
    
    assert result.distance_km > 30
    assert result.safety_level == SafetyLevel.SAFE
    assert result.is_dangerous == False


def test_dataclass_fields():
    """Test that LightningStrike dataclass has all expected fields"""
    calc = LightningDistanceCalculator()
    result = calc.calculate_distance(10.0)
    
    # Check all fields exist
    assert hasattr(result, 'distance_km')
    assert hasattr(result, 'distance_miles')
    assert hasattr(result, 'distance_meters')
    assert hasattr(result, 'distance_feet')
    assert hasattr(result, 'time_delay_seconds')
    assert hasattr(result, 'temperature_celsius')
    assert hasattr(result, 'speed_of_sound')
    assert hasattr(result, 'safety_level')
    assert hasattr(result, 'estimated_arrival_time')
    assert hasattr(result, 'is_dangerous')


def run_all_tests():
    """Run all tests manually"""
    tests = [
        test_basic_distance_calculation,
        test_temperature_effect,
        test_safety_levels,
        test_quick_distance_functions,
        test_rule_of_thumb,
        test_estimate_thunder_arrival,
        test_safe_shelter_time,
        test_is_lightning_safe,
        test_thunder_volume_estimate,
        test_count_strikes,
        test_safety_recommendation,
        test_calculate_strike_angle,
        test_calculate_strike_angle_insufficient_data,
        test_flash_to_bang_convenience_functions,
        test_constants,
        test_set_temperature,
        test_zero_delay,
        test_large_distance,
        test_dataclass_fields,
    ]
    
    passed = 0
    failed = 0
    
    print("Running Lightning Distance Utils Tests...\n")
    
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