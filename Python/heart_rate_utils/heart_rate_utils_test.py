#!/usr/bin/env python3
"""Heart Rate Utils Tests"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    HeartRateZone, MaxHrFormula, HeartRateRange, ZoneInfo, HeartRateResult,
    HeartRateUtils,
    calculate_max_hr, get_zones, get_fat_burning_hr, get_current_zone,
    estimate_calories
)


def test_calculate_max_hr_standard():
    """Test standard max HR formula (220 - age)."""
    hr = calculate_max_hr(30, "standard")
    assert hr == 190


def test_calculate_max_hr_tanaka():
    """Test Tanaka formula."""
    hr = calculate_max_hr(30, "tanaka")
    assert hr == 187


def test_calculate_max_hr_gellish():
    """Test Gellish formula."""
    hr = calculate_max_hr(30, "gellish")
    assert hr == 186  # Gellish: 207 - 0.7*30 = 186


def test_calculate_max_hr_invalid_age():
    """Test invalid age raises error."""
    try:
        calculate_max_hr(0)
        assert False, "Should raise ValueError"
    except ValueError:
        pass
    
    try:
        calculate_max_hr(121)
        assert False, "Should raise ValueError"
    except ValueError:
        pass


def test_get_zones():
    """Test zone calculation via convenience function."""
    zones = get_zones(age=30)
    assert "Zone 1" in zones["zones"]


def test_get_zones_with_resting():
    """Test zones with resting HR (Karvonen)."""
    zones = get_zones(age=30, resting_hr=60, use_karvonen=True)
    assert "Zone 1" in zones["zones"]


def test_zone_contains():
    """Test zone membership."""
    hr_range = HeartRateRange(120, 140)
    assert 130 in hr_range
    assert 100 not in hr_range
    assert 150 not in hr_range


def test_zone_to_dict():
    """Test zone dict conversion."""
    hr_range = HeartRateRange(120, 140)
    d = hr_range.to_dict()
    assert d["min"] == 120
    assert d["max"] == 140


def test_zone_info_to_dict():
    """Test ZoneInfo dict conversion."""
    hr_range = HeartRateRange(120, 140)
    zone_info = ZoneInfo(
        zone=HeartRateZone.ZONE_1,
        name="Recovery",
        description="Light intensity",
        hr_range=hr_range,
        percentage_range=(50, 60),
        benefits=["Recovery", "Endurance"],
        duration_minutes=(20, 60)
    )
    d = zone_info.to_dict()
    assert "zone" in d
    assert "name" in d
    assert "hr_range" in d
    assert "benefits" in d


def test_get_fat_burning_hr():
    """Test fat burning zone calculation."""
    zone = get_fat_burning_hr(30)
    assert zone is not None
    assert "hr_range" in zone
    assert "min" in zone["hr_range"]
    assert "max" in zone["hr_range"]


def test_get_current_zone():
    """Test current zone detection."""
    zone = get_current_zone(hr=130, age=30)
    assert zone is not None
    assert "zone" in zone


def test_estimate_calories():
    """Test calorie estimation."""
    calories = estimate_calories(hr=120, duration_min=30, weight_kg=70, age=30)
    assert calories > 0
    assert isinstance(calories, (int, float))


def test_max_hr_with_all_formulas():
    """Test all max HR formulas give reasonable values."""
    age = 40
    results = []
    for formula in ["standard", "tanaka", "gellish", "arena", "inbar"]:
        hr = calculate_max_hr(age, formula)
        results.append(hr)
        assert 120 <= hr <= 220  # Reasonable range
    
    # Different formulas should give different results
    assert len(set(results)) > 1


def test_heart_rate_result_to_dict():
    """Test HeartRateResult dict conversion."""
    result = get_zones(age=30)
    
    assert "max_hr" in result
    assert "zones" in result
    assert result["max_hr"] > 0


def test_zones_keys():
    """Test all 5 zones are present."""
    result = get_zones(age=30)
    zones = result["zones"]
    
    assert len(zones) == 5
    assert "Zone 1" in zones
    assert "Zone 5" in zones


def test_zone_ordering():
    """Test zones are in correct order (low to high)."""
    result = get_zones(age=30)
    zones = result["zones"]
    
    prev_max = 0
    for key in ["Zone 1", "Zone 2", "Zone 3", "Zone 4", "Zone 5"]:
        zone = zones[key]
        hr_range = zone["hr_range"]
        assert hr_range["min"] >= prev_max
        prev_max = hr_range["max"]


def test_max_hr_class_method():
    """Test HeartRateUtils.calculate_max_hr."""
    hr = HeartRateUtils.calculate_max_hr(30)
    assert hr > 0
    assert hr == 187  # Tanaka: 208 - 0.7*30 = 187


if __name__ == "__main__":
    import subprocess
    result = subprocess.run(["python3", "-m", "pytest", __file__, "-v"], cwd=os.path.dirname(os.path.abspath(__file__)))
    sys.exit(result.returncode)
