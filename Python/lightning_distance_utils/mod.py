"""
Lightning Distance Calculator Utilities

A comprehensive toolkit for calculating lightning strike distances based on
the time delay between seeing lightning and hearing thunder. Includes safety
warnings and educational information about lightning.

Features:
- Calculate distance from lightning based on time delay
- Temperature-adjusted speed of sound calculations
- Metric and imperial unit support
- Safety warnings and recommendations
- Flash-to-bang method implementation
- Lightning strike location estimation
"""

import math
from typing import Tuple, Optional, List, Dict
from dataclasses import dataclass
from enum import Enum


class DistanceUnit(Enum):
    """Distance measurement units"""
    KILOMETERS = "km"
    MILES = "mi"
    METERS = "m"
    FEET = "ft"


class SafetyLevel(Enum):
    """Lightning safety levels"""
    SAFE = "safe"
    CAUTION = "caution"
    DANGER = "danger"
    IMMEDIATE = "immediate"


@dataclass
class LightningStrike:
    """Represents a lightning strike calculation result"""
    distance_km: float
    distance_miles: float
    distance_meters: float
    distance_feet: float
    time_delay_seconds: float
    temperature_celsius: float
    speed_of_sound: float
    safety_level: SafetyLevel
    estimated_arrival_time: Optional[float]  # seconds until thunder arrives
    is_dangerous: bool


class LightningDistanceCalculator:
    """
    Calculator for lightning strike distances using the flash-to-bang method.
    
    The flash-to-bang method uses the time difference between seeing lightning
    and hearing thunder to estimate distance. Since light travels almost
    instantly (~300,000 km/s) compared to sound (~343 m/s at 20°C), we can
    calculate the distance based on sound travel time.
    """
    
    # Physical constants
    SPEED_OF_LIGHT = 299792458  # m/s (for reference, we assume instant)
    BASE_SPEED_OF_SOUND = 331.3  # m/s at 0°C
    
    # Safety thresholds (in km)
    SAFE_DISTANCE = 15.0  # Beyond this is considered safe
    CAUTION_DISTANCE = 10.0  # Start being cautious
    DANGER_DISTANCE = 6.0  # Seek shelter immediately
    IMMEDIATE_DANGER = 3.0  # Extremely close, high risk
    
    def __init__(self, temperature_celsius: float = 20.0):
        """
        Initialize calculator with ambient temperature.
        
        Args:
            temperature_celsius: Ambient temperature in Celsius (affects sound speed)
        """
        self.temperature_celsius = temperature_celsius
        self._speed_of_sound = self._calculate_speed_of_sound(temperature_celsius)
    
    def _calculate_speed_of_sound(self, temp_celsius: float) -> float:
        """
        Calculate speed of sound based on temperature.
        
        Formula: v = 331.3 + (0.606 × T) m/s
        Where T is temperature in Celsius.
        
        Args:
            temp_celsius: Temperature in Celsius
            
        Returns:
            Speed of sound in m/s
        """
        return self.BASE_SPEED_OF_SOUND + (0.606 * temp_celsius)
    
    @property
    def speed_of_sound(self) -> float:
        """Get current speed of sound in m/s"""
        return self._speed_of_sound
    
    def set_temperature(self, temp_celsius: float) -> None:
        """Update temperature and recalculate speed of sound"""
        self.temperature_celsius = temp_celsius
        self._speed_of_sound = self._calculate_speed_of_sound(temp_celsius)
    
    def calculate_distance(self, time_delay_seconds: float) -> LightningStrike:
        """
        Calculate lightning strike distance from flash-to-bang time delay.
        
        Args:
            time_delay_seconds: Time between seeing lightning and hearing thunder
            
        Returns:
            LightningStrike with distance calculations and safety info
        """
        # Distance = speed × time
        distance_meters = self._speed_of_sound * time_delay_seconds
        distance_km = distance_meters / 1000
        distance_miles = distance_km * 0.621371
        distance_feet = distance_meters * 3.28084
        
        # Determine safety level
        safety_level = self._get_safety_level(distance_km)
        is_dangerous = distance_km <= self.DANGER_DISTANCE
        
        # For very close strikes, estimate when thunder arrived
        estimated_arrival = None if distance_km > 0.1 else time_delay_seconds
        
        return LightningStrike(
            distance_km=round(distance_km, 2),
            distance_miles=round(distance_miles, 2),
            distance_meters=round(distance_meters, 1),
            distance_feet=round(distance_feet, 1),
            time_delay_seconds=time_delay_seconds,
            temperature_celsius=self.temperature_celsius,
            speed_of_sound=round(self._speed_of_sound, 2),
            safety_level=safety_level,
            estimated_arrival_time=estimated_arrival,
            is_dangerous=is_dangerous
        )
    
    def _get_safety_level(self, distance_km: float) -> SafetyLevel:
        """Determine safety level based on distance"""
        if distance_km > self.SAFE_DISTANCE:
            return SafetyLevel.SAFE
        elif distance_km > self.CAUTION_DISTANCE:
            return SafetyLevel.CAUTION
        elif distance_km > self.IMMEDIATE_DANGER:
            return SafetyLevel.DANGER
        else:
            return SafetyLevel.IMMEDIATE
    
    def get_safety_recommendation(self, strike: LightningStrike) -> str:
        """
        Get safety recommendation based on lightning strike distance.
        
        Args:
            strike: LightningStrike calculation result
            
        Returns:
            Safety recommendation string
        """
        recommendations = {
            SafetyLevel.SAFE: (
                f"The lightning is approximately {strike.distance_km} km away. "
                "While you're relatively safe, continue monitoring the storm. "
                "Stay indoors if possible."
            ),
            SafetyLevel.CAUTION: (
                f"⚠️ The lightning is about {strike.distance_km} km away. "
                "Stay alert and be prepared to seek shelter. "
                "Avoid open areas, tall trees, and water bodies."
            ),
            SafetyLevel.DANGER: (
                f"⚡ DANGER: The lightning is only {strike.distance_km} km away! "
                "Seek shelter IMMEDIATELY! Go indoors or inside a hard-topped vehicle. "
                "Stay away from windows, plumbing, and electrical equipment."
            ),
            SafetyLevel.IMMEDIATE: (
                f"🔴 CRITICAL: Lightning is extremely close ({strike.distance_km} km)! "
                "You may be in immediate danger! If no shelter is available: "
                "Crouch low with feet together, minimize contact with ground, "
                "DO NOT lie flat, and cover your ears!"
            )
        }
        return recommendations[strike.safety_level]
    
    def count_strikes(self, strikes: List[float]) -> Dict:
        """
        Analyze multiple lightning strikes to track storm movement.
        
        Args:
            strikes: List of time delays (in seconds) for consecutive strikes
            
        Returns:
            Dictionary with storm analysis
        """
        if not strikes:
            return {"error": "No strikes provided"}
        
        calculated = [self.calculate_distance(t) for t in strikes]
        distances_km = [s.distance_km for s in calculated]
        
        avg_distance = sum(distances_km) / len(distances_km)
        min_distance = min(distances_km)
        max_distance = max(distances_km)
        
        # Determine if storm is approaching or receding
        approaching = False
        if len(strikes) >= 2:
            recent = distances_km[-min(3, len(distances_km)):]
            older = distances_km[:max(1, len(distances_km) - 3)]
            if recent and older:
                recent_avg = sum(recent) / len(recent)
                older_avg = sum(older) / len(older)
                approaching = recent_avg < older_avg
        
        return {
            "total_strikes": len(strikes),
            "average_distance_km": round(avg_distance, 2),
            "closest_strike_km": min_distance,
            "farthest_strike_km": max_distance,
            "storm_approaching": approaching,
            "safety_level": self._get_safety_level(min_distance).value,
            "strikes": calculated
        }


def quick_distance(time_delay_seconds: float, temperature: float = 20.0) -> float:
    """
    Quick calculation of lightning distance in kilometers.
    
    Args:
        time_delay_seconds: Time between flash and thunder
        temperature: Ambient temperature in Celsius (default 20°C)
        
    Returns:
        Distance in kilometers
    """
    calc = LightningDistanceCalculator(temperature)
    return calc.calculate_distance(time_delay_seconds).distance_km


def quick_distance_miles(time_delay_seconds: float, temperature: float = 20.0) -> float:
    """
    Quick calculation of lightning distance in miles.
    
    Args:
        time_delay_seconds: Time between flash and thunder
        temperature: Ambient temperature in Celsius (default 20°C)
        
    Returns:
        Distance in miles
    """
    calc = LightningDistanceCalculator(temperature)
    return calc.calculate_distance(time_delay_seconds).distance_miles


def rule_of_thumb_distance(time_delay_seconds: float) -> dict:
    """
    Calculate distance using the common rule of thumb methods.
    
    The "5-second rule": Every 5 seconds = approximately 1 mile
    The "3-second rule": Every 3 seconds = approximately 1 kilometer
    
    Args:
        time_delay_seconds: Time between flash and thunder
        
    Returns:
        Dictionary with rule-of-thumb calculations
    """
    km_approx = time_delay_seconds / 3  # 3 seconds ≈ 1 km
    miles_approx = time_delay_seconds / 5  # 5 seconds ≈ 1 mile
    
    return {
        "time_seconds": time_delay_seconds,
        "rule_of_thumb_km": round(km_approx, 1),
        "rule_of_thumb_miles": round(miles_approx, 1),
        "explanation": (
            "Rule of thumb: Count seconds between flash and thunder. "
            "Divide by 3 for kilometers, or divide by 5 for miles."
        )
    }


def estimate_thunder_arrival(distance_km: float, temperature: float = 20.0) -> float:
    """
    Estimate how long until thunder is heard from a lightning strike.
    
    Args:
        distance_km: Distance to lightning strike in kilometers
        temperature: Ambient temperature in Celsius
        
    Returns:
        Time in seconds until thunder is audible
    """
    calc = LightningDistanceCalculator(temperature)
    speed_of_sound_km_s = calc.speed_of_sound / 1000
    return distance_km / speed_of_sound_km_s


def get_safe_shelter_time(distance_km: float) -> float:
    """
    Calculate time available to reach shelter before storm arrives.
    
    Assumes storm moves at approximately 40 km/h (typical thunderstorm speed).
    
    Args:
        distance_km: Current distance to storm
        
    Returns:
        Estimated minutes before storm is overhead
    """
    storm_speed_kmh = 40  # Typical thunderstorm speed
    time_hours = distance_km / storm_speed_kmh
    return time_hours * 60  # Convert to minutes


def is_lightning_safe(outdoor_activity: str, distance_km: float) -> Tuple[bool, str]:
    """
    Determine if it's safe to continue outdoor activities.
    
    Args:
        outdoor_activity: Type of activity (swimming, hiking, sports, etc.)
        distance_km: Distance to nearest lightning strike
        
    Returns:
        Tuple of (is_safe, recommendation)
    """
    # 30-30 Rule: Seek shelter if time between flash and thunder < 30 seconds
    # Wait 30 minutes after last thunder before resuming activities
    
    if distance_km <= 6:
        return False, "Seek shelter immediately - lightning is within danger zone!"
    
    if distance_km <= 10:
        return False, (
            f"Unsafe for {outdoor_activity}. Lightning is {distance_km} km away. "
            "Follow the 30-30 rule: seek shelter and wait 30 minutes after last thunder."
        )
    
    if distance_km <= 15:
        return True, (
            f"Caution advised for {outdoor_activity}. Lightning is {distance_km} km away. "
            "Be prepared to seek shelter. Monitor the storm closely."
        )
    
    return True, f"Relatively safe for {outdoor_activity}. Lightning is {distance_km} km away."


def thunder_volume_estimate(distance_km: float) -> str:
    """
    Estimate how loud thunder will be at a given distance.
    
    Args:
        distance_km: Distance to lightning strike
        
    Returns:
        Description of expected thunder volume
    """
    if distance_km < 0.5:
        return "Extremely loud - may cause hearing damage, sounds like explosion"
    elif distance_km < 2:
        return "Very loud - can be startling, window-rattling boom"
    elif distance_km < 5:
        return "Loud - clear rumble, easily heard indoors"
    elif distance_km < 10:
        return "Moderate - distinct rumble, may need to be outdoors to hear clearly"
    elif distance_km < 20:
        return "Faint - distant rumble, may be mistaken for other sounds"
    else:
        return "Very faint or inaudible - too far to hear clearly"


def calculate_strike_angle(time_delays: List[float], 
                          observer_positions: List[Tuple[float, float]]) -> Optional[Tuple[float, float]]:
    """
    Calculate approximate lightning strike position using triangulation.
    
    Requires at least 2 observers at different positions with timing data.
    This is a simplified calculation and assumes flat terrain.
    
    Args:
        time_delays: List of flash-to-bang times from each observer
        observer_positions: List of (x, y) coordinates for each observer in km
        
    Returns:
        Approximate (x, y) position of lightning strike in km, or None if insufficient data
    """
    if len(time_delays) < 2 or len(observer_positions) < 2:
        return None
    
    if len(time_delays) != len(observer_positions):
        return None
    
    # Calculate distance from each observer
    calc = LightningDistanceCalculator()
    distances = [calc.calculate_distance(t).distance_km for t in time_delays]
    
    # Simple triangulation using first two observers
    x1, y1 = observer_positions[0]
    x2, y2 = observer_positions[1]
    d1, d2 = distances[0], distances[1]
    
    # Distance between observers
    dx = x2 - x1
    dy = y2 - y1
    d = math.sqrt(dx*dx + dy*dy)
    
    if d == 0 or d > (d1 + d2):
        return None  # Invalid geometry
    
    # Calculate intersection point (simplified 2D)
    a = (d1*d1 - d2*d2 + d*d) / (2*d)
    
    if d1*d1 < a*a:
        return None  # No real solution
    
    h = math.sqrt(max(0, d1*d1 - a*a))
    
    # Intersection point
    px = x1 + a * dx/d + h * (-dy)/d
    py = y1 + a * dy/d + h * dx/d
    
    return (round(px, 2), round(py, 2))


# Convenience constants
SECONDS_PER_KM = 2.9  # Approximately (at 20°C)
SECONDS_PER_MILE = 4.7  # Approximately (at 20°C)


def flash_to_bang_kilometers(seconds: float) -> float:
    """
    Simple flash-to-bang distance in kilometers.
    
    Divides seconds by ~2.9 (based on speed of sound at 20°C).
    
    Args:
        seconds: Time between lightning flash and thunder
        
    Returns:
        Distance in kilometers
    """
    return round(seconds / SECONDS_PER_KM, 1)


def flash_to_bang_miles(seconds: float) -> float:
    """
    Simple flash-to-bang distance in miles.
    
    Divides seconds by ~4.7 (based on speed of sound at 20°C).
    
    Args:
        seconds: Time between lightning flash and thunder
        
    Returns:
        Distance in miles
    """
    return round(seconds / SECONDS_PER_MILE, 1)