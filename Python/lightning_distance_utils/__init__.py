"""
Lightning Distance Utils

A comprehensive toolkit for calculating lightning strike distances
and providing safety recommendations.

Usage:
    from lightning_distance_utils import (
        LightningDistanceCalculator,
        quick_distance,
        quick_distance_miles,
        rule_of_thumb_distance
    )
    
    # Quick distance calculation
    distance_km = quick_distance(5.0)  # 5 seconds delay
    
    # Full calculation with safety info
    calc = LightningDistanceCalculator(temperature_celsius=20.0)
    result = calc.calculate_distance(5.0)
    print(f"Distance: {result.distance_km} km")
    print(f"Safety: {result.safety_level}")
"""

from .mod import (
    # Main calculator
    LightningDistanceCalculator,
    
    # Data classes and enums
    DistanceUnit,
    SafetyLevel,
    LightningStrike,
    
    # Convenience functions
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
    
    # Constants
    SECONDS_PER_KM,
    SECONDS_PER_MILE,
)

__version__ = "1.0.0"
__all__ = [
    "LightningDistanceCalculator",
    "DistanceUnit",
    "SafetyLevel",
    "LightningStrike",
    "quick_distance",
    "quick_distance_miles",
    "rule_of_thumb_distance",
    "estimate_thunder_arrival",
    "get_safe_shelter_time",
    "is_lightning_safe",
    "thunder_volume_estimate",
    "calculate_strike_angle",
    "flash_to_bang_kilometers",
    "flash_to_bang_miles",
    "SECONDS_PER_KM",
    "SECONDS_PER_MILE",
]