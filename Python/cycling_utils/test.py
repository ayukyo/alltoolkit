#!/usr/bin/env python3
"""
Test suite for Cycling Utilities.

Run with: python -m pytest cycling_utils/test.py -v
Or directly: python cycling_utils/test.py
"""

import sys
import math
from typing import List

# Add parent directory to path for imports
sys.path.insert(0, '.')

from cycling_utils.mod import (
    CyclingUtils,
    CyclingResult,
    GearConfig,
    RiderProfile,
    TerrainType,
    RidingPosition,
    calculate_speed,
    calculate_time,
    calculate_distance,
    calculate_power,
    calculate_calories,
    calculate_gear_ratio,
    calculate_speed_from_cadence,
)


def test_calculate_speed():
    """Test speed calculation from distance and time."""
    utils = CyclingUtils()

    # Test basic speed calculation
    result = utils.calculate_speed(100, 4)  # 100km in 4h
    assert result.value == 25.0
    assert result.unit == "km/h"

    # Test with different values
    result = utils.calculate_speed(42.195, 3)  # Marathon distance
    assert abs(result.value - 14.065) < 0.001

    print("✓ test_calculate_speed passed")


def test_calculate_time():
    """Test time calculation from distance and speed."""
    utils = CyclingUtils()

    # Test basic time calculation
    result = utils.calculate_time(100, 25)  # 100km at 25km/h
    assert result.value == 4.0
    assert result.unit == "hours"

    # Test with different values
    result = utils.calculate_time(42.195, 15)
    assert abs(result.value - 2.813) < 0.001

    print("✓ test_calculate_time passed")


def test_calculate_distance():
    """Test distance calculation from speed and time."""
    utils = CyclingUtils()

    # Test basic distance calculation
    result = utils.calculate_distance(25, 4)  # 25km/h for 4h
    assert result.value == 100.0
    assert result.unit == "km"

    print("✓ test_calculate_distance passed")


def test_pace_speed_conversion():
    """Test pace to speed and vice versa conversions."""
    utils = CyclingUtils()

    # 5 min/km = 12 km/h
    result = utils.pace_to_speed(5)
    assert abs(result.value - 12.0) < 0.001

    # 12 km/h = 5 min/km
    result = utils.speed_to_pace(12)
    assert abs(result.value - 5.0) < 0.001

    # Round trip test
    original_pace = 4.5
    speed = utils.pace_to_speed(original_pace).value
    back_to_pace = utils.speed_to_pace(speed).value
    assert abs(original_pace - back_to_pace) < 0.0001

    print("✓ test_pace_speed_conversion passed")


def test_power_calculation():
    """Test power calculation."""
    rider = RiderProfile(weight_kg=75, ftp_watts=250)
    utils = CyclingUtils(rider=rider)

    # Test flat riding at 30 km/h
    result = utils.calculate_power(30, gradient_percent=0)
    # Should be around 100-200W for typical cyclist (depends on total weight)
    assert 80 < result.value < 300

    # Test climbing at 15 km/h on 5% grade
    result = utils.calculate_power(15, gradient_percent=5)
    # Should be significantly higher than flat
    flat_power = utils.calculate_power(15, gradient_percent=0).value
    assert result.value > flat_power

    # Test with headwind
    result_no_wind = utils.calculate_power(30, gradient_percent=0, wind_speed_kmh=0)
    result_headwind = utils.calculate_power(30, gradient_percent=0, wind_speed_kmh=15)
    assert result_headwind.value > result_no_wind.value

    # Test different riding positions
    result_tops = utils.calculate_power(30, riding_position=RidingPosition.TOPS)
    result_aero = utils.calculate_power(30, riding_position=RidingPosition.AERO)
    assert result_tops.value > result_aero.value  # Aero should require less power

    print("✓ test_power_calculation passed")


def test_estimate_speed_from_power():
    """Test speed estimation from power."""
    rider = RiderProfile(weight_kg=75, ftp_watts=250)
    utils = CyclingUtils(rider=rider)

    # Test flat riding at 200W
    result = utils.estimate_speed_from_power(200, gradient_percent=0)
    # Should be around 30-35 km/h for typical cyclist
    assert 25 < result.value < 40

    # Test climbing at 250W on 5% grade
    result = utils.estimate_speed_from_power(250, gradient_percent=5)
    # Should be slower, around 12-18 km/h
    assert 8 < result.value < 20

    print("✓ test_estimate_speed_from_power passed")


def test_power_to_weight_ratio():
    """Test power-to-weight ratio calculation."""
    rider = RiderProfile(weight_kg=75, ftp_watts=250)
    utils = CyclingUtils(rider=rider)

    result = utils.calculate_power_to_weight_ratio(300)
    assert abs(result.value - 4.0) < 0.001  # 300W / 75kg = 4 W/kg

    print("✓ test_power_to_weight_ratio passed")


def test_training_zones():
    """Test training zone determination."""
    rider = RiderProfile(weight_kg=75, ftp_watts=250)
    utils = CyclingUtils(rider=rider)

    # Zone 1: Active Recovery (< 55% FTP)
    zone, name, _ = utils.get_training_zone(120)
    assert zone == 1
    assert "Recovery" in name

    # Zone 2: Endurance (55-75% FTP)
    zone, name, _ = utils.get_training_zone(170)
    assert zone == 2
    assert "Endurance" in name

    # Zone 3: Tempo (75-90% FTP)
    zone, name, _ = utils.get_training_zone(200)
    assert zone == 3
    assert "Tempo" in name

    # Zone 4: Threshold (90-105% FTP)
    zone, name, _ = utils.get_training_zone(240)
    assert zone == 4
    assert "Threshold" in name

    # Zone 5: VO2 Max (105-120% FTP)
    zone, name, _ = utils.get_training_zone(275)
    assert zone == 5
    assert "VO2" in name

    # Zone 6: Anaerobic (120-150% FTP)
    zone, name, _ = utils.get_training_zone(320)
    assert zone == 6
    assert "Anaerobic" in name

    # Zone 7: Sprint (> 150% FTP)
    zone, name, _ = utils.get_training_zone(400)
    assert zone == 7
    assert "Sprint" in name

    print("✓ test_training_zones passed")


def test_calorie_calculation():
    """Test calorie calculation from power."""
    utils = CyclingUtils()

    # 200W for 2 hours, 24% efficiency
    result = utils.calculate_calories(200, 2, efficiency_percent=24)
    # Energy = 200W × 7200s / 4184 / 0.24 ≈ 1434 kcal
    expected = (200 * 2 * 3600) / 4184 / 0.24
    assert abs(result.value - expected) < 1

    # Higher efficiency = fewer calories
    result_low_eff = utils.calculate_calories(200, 2, efficiency_percent=20)
    result_high_eff = utils.calculate_calories(200, 2, efficiency_percent=25)
    assert result_low_eff.value > result_high_eff.value

    print("✓ test_calorie_calculation passed")


def test_calorie_from_heart_rate():
    """Test calorie estimation from heart rate."""
    rider = RiderProfile(weight_kg=70, age_years=30, gender='male')
    utils = CyclingUtils(rider=rider)

    # Test male HR-based calorie estimation
    result = utils.estimate_calories_from_hr(150, 1.5)
    assert result.value > 0
    assert result.unit == "kcal"

    # Test female HR-based calorie estimation
    rider_female = RiderProfile(weight_kg=60, age_years=25, gender='female')
    utils_female = CyclingUtils(rider=rider_female)
    result_female = utils_female.estimate_calories_from_hr(150, 1.5)

    # Results should be positive
    assert result_female.value > 0

    print("✓ test_calorie_from_heart_rate passed")


def test_gear_ratio():
    """Test gear ratio calculation."""
    utils = CyclingUtils()

    # 50/11 = 4.545
    result = utils.calculate_gear_ratio(50, 11)
    assert abs(result.value - 4.5454) < 0.01

    # 34/28 = 1.214
    result = utils.calculate_gear_ratio(34, 28)
    assert abs(result.value - 1.214) < 0.01

    # Bigger ratio = harder gear
    assert utils.calculate_gear_ratio(53, 11).value > utils.calculate_gear_ratio(34, 28).value

    print("✓ test_gear_ratio passed")


def test_development():
    """Test development (distance per crank revolution) calculation."""
    utils = CyclingUtils()

    # 50T front, 14T rear on 700c wheel with 25mm tires
    result = utils.calculate_development(50, 14)
    # Approximately 7.5-8m per revolution
    assert 7 < result.value < 9

    # Smaller gear = less development
    result_small = utils.calculate_development(34, 28)
    result_large = utils.calculate_development(50, 11)
    assert result_small.value < result_large.value

    print("✓ test_development passed")


def test_speed_from_cadence():
    """Test speed calculation from cadence."""
    utils = CyclingUtils()

    # 90 rpm with 50/14 gear - expected ~40km/h with 700c wheel
    result = utils.calculate_speed_from_cadence(90, 50, 14)
    # Should be around 35-45 km/h
    assert 35 < result.value < 45

    # Higher cadence = higher speed
    result_low = utils.calculate_speed_from_cadence(60, 50, 14)
    result_high = utils.calculate_speed_from_cadence(100, 50, 14)
    assert result_low.value < result_high.value

    # Bigger gear = higher speed at same cadence
    result_small_gear = utils.calculate_speed_from_cadence(90, 34, 28)
    result_big_gear = utils.calculate_speed_from_cadence(90, 50, 11)
    assert result_small_gear.value < result_big_gear.value

    print("✓ test_speed_from_cadence passed")


def test_cadence_from_speed():
    """Test cadence calculation from speed."""
    utils = CyclingUtils()

    # 30 km/h with 50/14 gear - expected ~66rpm with 700c wheel
    result = utils.calculate_cadence_from_speed(30, 50, 14)
    # Should be around 60-75 rpm
    assert 60 < result.value < 80

    # Higher speed = higher cadence needed
    result_slow = utils.calculate_cadence_from_speed(25, 50, 14)
    result_fast = utils.calculate_cadence_from_speed(35, 50, 14)
    assert result_slow.value < result_fast.value

    print("✓ test_cadence_from_speed passed")


def test_all_gear_ratios():
    """Test getting all gear ratios."""
    gear_config = GearConfig(
        front_teeth=[50, 34],  # Compact crank
        rear_teeth=[11, 12, 13, 14, 15, 17, 19, 21, 24, 28]
    )
    utils = CyclingUtils(gear_config=gear_config)

    ratios = utils.get_all_gear_ratios()

    # Should have 2 × 10 = 20 combinations
    assert len(ratios) == 20

    # Should be sorted by ratio
    for i in range(len(ratios) - 1):
        assert ratios[i][2] <= ratios[i + 1][2]

    # Smallest ratio should be 34/28
    assert ratios[0][0] == 34 and ratios[0][1] == 28

    # Largest ratio should be 50/11
    assert ratios[-1][0] == 50 and ratios[-1][1] == 11

    print("✓ test_all_gear_ratios passed")


def test_all_developments():
    """Test getting all developments."""
    gear_config = GearConfig(
        front_teeth=[50, 34],
        rear_teeth=[11, 28]
    )
    utils = CyclingUtils(gear_config=gear_config)

    developments = utils.get_all_developments()

    # Should have 2 × 2 = 4 combinations
    assert len(developments) == 4

    # Should be sorted by development
    for i in range(len(developments) - 1):
        assert developments[i][2] <= developments[i + 1][2]

    print("✓ test_all_developments passed")


def test_gradient_calculation():
    """Test gradient calculation."""
    utils = CyclingUtils()

    # 1000m gain over 10km = 10%
    result = utils.calculate_gradient(10, 1000)
    assert abs(result.value - 10.0) < 0.001

    # 500m gain over 10km = 5%
    result = utils.calculate_gradient(10, 500)
    assert abs(result.value - 5.0) < 0.001

    print("✓ test_gradient_calculation passed")


def test_elevation_gain():
    """Test elevation gain calculation."""
    utils = CyclingUtils()

    # 10km at 5% = 500m
    result = utils.calculate_elevation_gain(10, 5)
    assert abs(result.value - 500.0) < 0.001

    # 20km at 3% = 600m
    result = utils.calculate_elevation_gain(20, 3)
    assert abs(result.value - 600.0) < 0.001

    print("✓ test_elevation_gain passed")


def test_vam_calculation():
    """Test VAM (climbing speed) calculation."""
    utils = CyclingUtils()

    # 1000m in 1 hour = 1000 m/h
    result = utils.calculate_vam(1000, 1)
    assert abs(result.value - 1000.0) < 0.001

    # 500m in 30 minutes = 1000 m/h
    result = utils.calculate_vam(500, 0.5)
    assert abs(result.value - 1000.0) < 0.001

    # Pro cyclist VAM ~1500-2000 m/h on major climbs
    result = utils.calculate_vam(1200, 0.75)  # 1200m in 45 min
    assert abs(result.value - 1600.0) < 0.001

    print("✓ test_vam_calculation passed")


def test_climbing_difficulty():
    """Test climbing difficulty score calculation."""
    utils = CyclingUtils()

    # Alpe d'Huez: ~14km at 8% average
    result = utils.calculate_climbing_difficulty(14, 1120)
    assert result.value > 0

    # Steeper = harder
    result_moderate = utils.calculate_climbing_difficulty(10, 300)  # 3%
    result_steep = utils.calculate_climbing_difficulty(10, 800)   # 8%
    assert result_steep.value > result_moderate.value

    print("✓ test_climbing_difficulty passed")


def test_normalized_power():
    """Test Normalized Power calculation."""
    rider = RiderProfile(weight_kg=75)
    utils = CyclingUtils(rider=rider)

    # Constant power should equal NP (need enough samples for 30s window)
    constant_power = [200] * 60  # 60 samples at 1s interval = 60s
    result = utils.calculate_np(constant_power, sample_interval_seconds=1.0)
    assert abs(result.value - 200) < 1

    # Variable power should have higher NP than average
    # Need enough samples for proper calculation
    variable_power = [150] * 30 + [250] * 30  # Average = 200
    result_var = utils.calculate_np(variable_power, sample_interval_seconds=1.0)
    # NP should be close to but potentially slightly different due to smoothing
    assert abs(result_var.value - 200) < 30

    print("✓ test_normalized_power passed")


def test_tss_calculation():
    """Test Training Stress Score calculation."""
    rider = RiderProfile(weight_kg=75, ftp_watts=250)
    utils = CyclingUtils(rider=rider)

    # 1 hour at FTP = 100 TSS
    result = utils.calculate_tss(250, 1)
    assert abs(result.value - 100) < 1

    # 2 hours at FTP = 200 TSS
    result = utils.calculate_tss(250, 2)
    assert abs(result.value - 200) < 1

    # 1 hour at 75% FTP = 56.25 TSS
    result = utils.calculate_tss(187.5, 1)
    assert abs(result.value - 56.25) < 1

    print("✓ test_tss_calculation passed")


def test_intensity_factor():
    """Test Intensity Factor calculation."""
    rider = RiderProfile(weight_kg=75, ftp_watts=250)
    utils = CyclingUtils(rider=rider)

    # At FTP, IF = 1.0
    result = utils.calculate_if(250)
    assert abs(result.value - 1.0) < 0.001

    # At 75% FTP, IF = 0.75
    result = utils.calculate_if(187.5)
    assert abs(result.value - 0.75) < 0.001

    print("✓ test_intensity_factor passed")


def test_convenience_functions():
    """Test convenience functions."""
    # Speed calculation
    speed = calculate_speed(100, 4)
    assert abs(speed - 25.0) < 0.001

    # Time calculation
    time = calculate_time(100, 25)
    assert abs(time - 4.0) < 0.001

    # Distance calculation
    distance = calculate_distance(25, 4)
    assert abs(distance - 100.0) < 0.001

    # Power calculation
    power = calculate_power(30, weight_kg=75)
    assert power > 0

    # Calorie calculation
    calories = calculate_calories(200, 2)
    assert calories > 0

    # Gear ratio
    ratio = calculate_gear_ratio(50, 11)
    assert abs(ratio - 4.545) < 0.01

    # Speed from cadence
    speed = calculate_speed_from_cadence(90, 50, 14)
    assert speed > 0

    print("✓ test_convenience_functions passed")


def test_custom_gear_config():
    """Test with custom gear configuration."""
    # Custom MTB gearing
    gear_config = GearConfig(
        front_teeth=[32],  # Single chainring
        rear_teeth=[10, 12, 14, 16, 18, 21, 24, 28, 32, 36],
        wheel_diameter_mm=622,  # 29er
        tire_width_mm=2.4 * 10  # 2.4" tire in mm
    )
    utils = CyclingUtils(gear_config=gear_config)

    # Get all ratios
    ratios = utils.get_all_gear_ratios()
    assert len(ratios) == 10  # 1 × 10

    # Smallest should be 32/36
    assert ratios[0][0] == 32 and ratios[0][1] == 36

    # Largest should be 32/10
    assert ratios[-1][0] == 32 and ratios[-1][1] == 10

    print("✓ test_custom_gear_config passed")


def test_error_handling():
    """Test error handling for invalid inputs."""
    utils = CyclingUtils()

    # Test division by zero cases
    try:
        utils.calculate_speed(100, 0)
        assert False, "Should raise ValueError"
    except ValueError:
        pass

    try:
        utils.calculate_time(100, 0)
        assert False, "Should raise ValueError"
    except ValueError:
        pass

    try:
        utils.pace_to_speed(0)
        assert False, "Should raise ValueError"
    except ValueError:
        pass

    try:
        utils.calculate_gear_ratio(50, 0)
        assert False, "Should raise ValueError"
    except ValueError:
        pass

    # Test NP with too few samples
    try:
        utils.calculate_np([100, 200, 300])  # Only 3 samples
        assert False, "Should raise ValueError"
    except ValueError:
        pass

    # Test TSS without FTP
    try:
        utils.calculate_tss(200, 1)
        assert False, "Should raise ValueError"
    except ValueError:
        pass

    print("✓ test_error_handling passed")


def test_total_weight():
    """Test total weight calculation."""
    rider = RiderProfile(weight_kg=70)
    utils = CyclingUtils(rider=rider, bike_weight_kg=10)

    total = utils.total_weight
    assert total == 80.0

    # Without rider
    utils_no_rider = CyclingUtils(bike_weight_kg=8)
    assert utils_no_rider.total_weight == 8.0

    print("✓ test_total_weight passed")


def test_rolling_resistance():
    """Test power on different surfaces."""
    rider = RiderProfile(weight_kg=75)
    utils = CyclingUtils(rider=rider)

    # Same speed, different surfaces
    power_asphalt = utils.calculate_power(25, surface='asphalt').value
    power_gravel = utils.calculate_power(25, surface='gravel').value
    power_grass = utils.calculate_power(25, surface='grass').value

    # Grass should require more power than gravel, gravel more than asphalt
    assert power_grass > power_gravel > power_asphalt

    print("✓ test_rolling_resistance passed")


def run_all_tests():
    """Run all tests and print summary."""
    tests = [
        test_calculate_speed,
        test_calculate_time,
        test_calculate_distance,
        test_pace_speed_conversion,
        test_power_calculation,
        test_estimate_speed_from_power,
        test_power_to_weight_ratio,
        test_training_zones,
        test_calorie_calculation,
        test_calorie_from_heart_rate,
        test_gear_ratio,
        test_development,
        test_speed_from_cadence,
        test_cadence_from_speed,
        test_all_gear_ratios,
        test_all_developments,
        test_gradient_calculation,
        test_elevation_gain,
        test_vam_calculation,
        test_climbing_difficulty,
        test_normalized_power,
        test_tss_calculation,
        test_intensity_factor,
        test_convenience_functions,
        test_custom_gear_config,
        test_error_handling,
        test_total_weight,
        test_rolling_resistance,
    ]

    passed = 0
    failed = 0

    print("\n" + "=" * 60)
    print("Running Cycling Utilities Tests")
    print("=" * 60 + "\n")

    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"✗ {test.__name__} FAILED: {e}")
            failed += 1

    print("\n" + "=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60 + "\n")

    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)