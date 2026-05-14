"""
Jet Lag Calculator Utils

A comprehensive utility for calculating jet lag severity, recovery time,
and providing personalized sleep schedule recommendations for travelers.

Features:
- Jet lag severity calculation based on time zone changes
- Recovery time estimation using scientifically-backed formulas
- Optimal sleep schedule recommendations
- Light exposure timing recommendations (blue light / melatonin)
- East vs West travel adjustment strategies
- Circadian rhythm phase shift calculations

Zero external dependencies - pure Python standard library.
"""

from datetime import datetime, time, timedelta
from typing import List, Tuple, Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum
import math


class TravelDirection(Enum):
    """Direction of travel affecting jet lag severity."""
    EAST = "east"  # More difficult - phase advance
    WEST = "west"  # Easier - phase delay
    NONE = "none"  # No significant time change


class SleepType(Enum):
    """Type of sleeper based on chronotype."""
    MORNING_LARK = "morning_lark"  # Early bird
    NIGHT_OWL = "night_owl"  # Late sleeper
    INTERMEDIATE = "intermediate"  # Average


@dataclass
class TimezoneInfo:
    """Information about a timezone."""
    name: str
    utc_offset: float  # Hours from UTC
    
    @classmethod
    def from_utc_offset(cls, offset: float, name: str = "") -> 'TimezoneInfo':
        """Create timezone info from UTC offset."""
        return cls(name=name or f"UTC{'+' if offset >= 0 else ''}{offset}", utc_offset=offset)


@dataclass
class JetLagResult:
    """Result of jet lag calculation."""
    time_difference: float  # Hours
    direction: TravelDirection
    severity_score: float  # 0-100
    severity_level: str  # Minimal, Mild, Moderate, Severe, Extreme
    estimated_recovery_days: float
    adjustment_per_day: float  # Hours your body adjusts per day
    recommendations: List[str]
    optimal_sleep_schedule: Dict[str, str]
    light_exposure_times: Dict[str, str]
    phase_shift_needed: float  # Hours to shift


@dataclass
class SleepSchedule:
    """A sleep schedule with bed and wake times."""
    bed_time: time
    wake_time: time
    duration: float  # Hours
    
    def __str__(self) -> str:
        return f"{self.bed_time.strftime('%H:%M')} - {self.wake_time.strftime('%H:%M')} ({self.duration:.1f}h)"


class JetLagCalculator:
    """
    Main calculator for jet lag analysis and recommendations.
    
    Uses scientifically-backed formulas for estimating jet lag severity
    and recovery time. The body typically adjusts at ~1 hour per day
    for eastward travel and ~1.5 hours per day for westward travel.
    """
    
    # Constants based on circadian rhythm research
    PHASE_ADVANCE_RATE = 0.8  # Hours per day (eastward travel)
    PHASE_DELAY_RATE = 1.2   # Hours per day (westward travel)
    
    # Age factors affecting jet lag recovery
    AGE_FACTORS = {
        (0, 25): 1.2,    # Young adults recover faster
        (25, 40): 1.0,   # Baseline
        (40, 55): 0.85,  # Slightly slower
        (55, 70): 0.7,   # Noticeably slower
        (70, 100): 0.5   # Significantly slower
    }
    
    def __init__(
        self,
        age: int = 30,
        sleep_type: SleepType = SleepType.INTERMEDIATE,
        typical_bed_time: time = time(23, 0),
        typical_wake_time: time = time(7, 0)
    ):
        """
        Initialize the jet lag calculator with personal parameters.
        
        Args:
            age: Traveler's age
            sleep_type: Chronotype (morning lark, night owl, intermediate)
            typical_bed_time: Usual bedtime at origin
            typical_wake_time: Usual wake time at origin
        """
        self.age = age
        self.sleep_type = sleep_type
        self.typical_bed_time = typical_bed_time
        self.typical_wake_time = typical_wake_time
        
    def calculate(
        self,
        origin_timezone: TimezoneInfo,
        destination_timezone: TimezoneInfo,
        travel_date: Optional[datetime] = None,
        flight_duration: Optional[float] = None
    ) -> JetLagResult:
        """
        Calculate jet lag information for a trip.
        
        Args:
            origin_timezone: Starting timezone
            destination_timezone: Destination timezone
            travel_date: Date of travel (for recommendations)
            flight_duration: Duration of flight in hours
            
        Returns:
            JetLagResult with comprehensive jet lag analysis
        """
        # Calculate time difference
        time_diff = destination_timezone.utc_offset - origin_timezone.utc_offset
        
        # Normalize to -12 to +12 range
        if time_diff > 12:
            time_diff -= 24
        elif time_diff < -12:
            time_diff += 24
            
        # Determine direction
        if abs(time_diff) < 1:
            direction = TravelDirection.NONE
        elif time_diff > 0:
            direction = TravelDirection.EAST
        else:
            direction = TravelDirection.WEST
            
        # Calculate severity score (0-100)
        severity_score = self._calculate_severity(abs(time_diff), direction)
        
        # Determine severity level
        severity_level = self._get_severity_level(severity_score)
        
        # Estimate recovery days
        recovery_days = self._estimate_recovery(abs(time_diff), direction)
        
        # Calculate adjustment per day
        if direction == TravelDirection.EAST:
            adjustment_per_day = self.PHASE_ADVANCE_RATE * self._get_age_factor()
        elif direction == TravelDirection.WEST:
            adjustment_per_day = self.PHASE_DELAY_RATE * self._get_age_factor()
        else:
            adjustment_per_day = 0
            
        # Generate recommendations
        recommendations = self._generate_recommendations(
            time_diff, direction, severity_score, flight_duration
        )
        
        # Calculate optimal sleep schedule
        sleep_schedule = self._calculate_sleep_schedule(time_diff, direction)
        
        # Calculate light exposure times
        light_times = self._calculate_light_exposure(time_diff, direction)
        
        return JetLagResult(
            time_difference=time_diff,
            direction=direction,
            severity_score=severity_score,
            severity_level=severity_level,
            estimated_recovery_days=recovery_days,
            adjustment_per_day=adjustment_per_day,
            recommendations=recommendations,
            optimal_sleep_schedule=sleep_schedule,
            light_exposure_times=light_times,
            phase_shift_needed=abs(time_diff)
        )
    
    def _calculate_severity(self, hours: float, direction: TravelDirection) -> float:
        """
        Calculate jet lag severity score (0-100).
        
        Eastward travel is generally more difficult due to phase advance
        being harder than phase delay for the circadian rhythm.
        """
        if hours < 1:
            return 0
            
        # Base severity from hours (non-linear relationship)
        # Each hour adds progressively more severity
        base_severity = min(100, (hours ** 1.3) * 5)
        
        # Direction modifier - east is harder
        if direction == TravelDirection.EAST:
            base_severity *= 1.2
        elif direction == TravelDirection.WEST:
            base_severity *= 0.9
            
        # Sleep type modifier
        if self.sleep_type == SleepType.NIGHT_OWL:
            if direction == TravelDirection.EAST:
                base_severity *= 1.15  # Owls struggle more going east
            else:
                base_severity *= 0.95
        elif self.sleep_type == SleepType.MORNING_LARK:
            if direction == TravelDirection.WEST:
                base_severity *= 1.1  # Larks struggle more going west
            else:
                base_severity *= 0.95
                
        return min(100, base_severity)
    
    def _get_severity_level(self, score: float) -> str:
        """Convert severity score to descriptive level."""
        if score < 10:
            return "Minimal"
        elif score < 25:
            return "Mild"
        elif score < 50:
            return "Moderate"
        elif score < 75:
            return "Severe"
        else:
            return "Extreme"
    
    def _get_age_factor(self) -> float:
        """Get age-based recovery factor."""
        for (min_age, max_age), factor in self.AGE_FACTORS.items():
            if min_age <= self.age < max_age:
                return factor
        return 1.0
    
    def _estimate_recovery(self, hours: float, direction: TravelDirection) -> float:
        """
        Estimate recovery time in days.
        
        Based on research showing ~1 day per time zone crossed,
        with variations for direction and individual factors.
        """
        if hours < 1:
            return 0
            
        # Base recovery: roughly 1 day per hour of time difference
        if direction == TravelDirection.EAST:
            base_days = hours / self.PHASE_ADVANCE_RATE
        elif direction == TravelDirection.WEST:
            base_days = hours / self.PHASE_DELAY_RATE
        else:
            return 0
            
        # Apply age factor
        base_days /= self._get_age_factor()
        
        # Sleep type adjustment
        if self.sleep_type == SleepType.NIGHT_OWL and direction == TravelDirection.EAST:
            base_days *= 1.1
        elif self.sleep_type == SleepType.MORNING_LARK and direction == TravelDirection.WEST:
            base_days *= 1.1
            
        return round(base_days, 1)
    
    def _generate_recommendations(
        self,
        time_diff: float,
        direction: TravelDirection,
        severity: float,
        flight_duration: Optional[float]
    ) -> List[str]:
        """Generate personalized recommendations."""
        recommendations = []
        
        abs_diff = abs(time_diff)
        
        # Pre-travel recommendations
        if abs_diff > 3:
            recommendations.append(
                f"Start adjusting your sleep schedule 3-5 days before departure, "
                f"shifting by 30-60 minutes per day {'earlier' if direction == TravelDirection.EAST else 'later'}."
            )
        
        # During flight
        if flight_duration and flight_duration > 6:
            recommendations.append(
                "Stay hydrated during the flight - dehydration worsens jet lag."
            )
            
        if abs_diff > 6:
            recommendations.append(
                "Consider a short nap (20-30 min) upon arrival, but avoid long naps."
            )
            
        # Light exposure
        if direction == TravelDirection.EAST:
            recommendations.append(
                "Seek bright light in the morning at your destination to help advance your clock."
            )
            if severity > 50:
                recommendations.append(
                    "Consider melatonin (0.5-3mg) at local bedtime for the first few nights."
                )
        elif direction == TravelDirection.WEST:
            recommendations.append(
                "Seek bright light in the evening at your destination to help delay your clock."
            )
            recommendations.append(
                "Avoid bright light in the early morning to prevent waking too early."
            )
            
        # General recommendations
        if severity > 25:
            recommendations.append(
                "Avoid heavy meals close to bedtime - eat light at destination meal times."
            )
            
        if severity > 50:
            recommendations.append(
                "Limit caffeine and alcohol - both disrupt sleep quality during adjustment."
            )
            
        recommendations.append(
            "Exercise lightly during the day, but avoid intense workouts close to bedtime."
        )
        
        if severity > 40:
            recommendations.append(
                "Plan lighter activities for the first 1-2 days at your destination."
            )
            
        return recommendations
    
    def _calculate_sleep_schedule(
        self,
        time_diff: float,
        direction: TravelDirection
    ) -> Dict[str, str]:
        """Calculate optimal sleep schedule adjustments."""
        schedule = {}
        
        if abs(time_diff) < 1:
            return {
                "note": "No significant adjustment needed",
                "bedtime": self.typical_bed_time.strftime("%H:%M"),
                "wake_time": self.typical_wake_time.strftime("%H:%M")
            }
        
        # For eastward travel, gradually go to bed earlier
        # For westward travel, gradually go to bed later
        abs_diff = abs(time_diff)
        
        # Calculate shift direction
        if direction == TravelDirection.EAST:
            shift_direction = "earlier"
            shift_minutes = min(60, int(abs_diff * 10))  # Max 60 min shift per day
        else:
            shift_direction = "later"
            shift_minutes = min(90, int(abs_diff * 15))  # Max 90 min shift per day
        
        # Day 1-3 schedule
        total_shift = shift_minutes
        
        # Calculate shifted times
        bed_delta = timedelta(minutes=total_shift if direction == TravelDirection.EAST else -total_shift)
        base_bed = datetime.combine(datetime.today(), self.typical_bed_time)
        day1_bed = (base_bed - bed_delta if direction == TravelDirection.EAST else base_bed + bed_delta).time()
        
        schedule["day_1"] = f"Bedtime: {day1_bed.strftime('%H:%M')} ({shift_direction} by {shift_minutes} min)"
        
        # Progressive shifts
        if abs_diff > 3:
            day2_shift = shift_minutes * 2
            bed_delta_2 = timedelta(minutes=day2_shift if direction == TravelDirection.EAST else -day2_shift)
            day2_bed = (base_bed - bed_delta_2 if direction == TravelDirection.EAST else base_bed + bed_delta_2).time()
            schedule["day_2"] = f"Bedtime: {day2_bed.strftime('%H:%M')} (cumulative {shift_direction} shift)"
            
        if abs_diff > 6:
            day3_shift = shift_minutes * 3
            bed_delta_3 = timedelta(minutes=day3_shift if direction == TravelDirection.EAST else -day3_shift)
            day3_bed = (base_bed - bed_delta_3 if direction == TravelDirection.EAST else base_bed + bed_delta_3).time()
            schedule["day_3"] = f"Bedtime: {day3_bed.strftime('%H:%M')} (continue adjusting)"
        
        schedule["strategy"] = f"Gradually shift bedtime {shift_direction}"
        schedule["target"] = f"Adjust to destination bedtime over {int(abs_diff)} days"
        
        return schedule
    
    def _calculate_light_exposure(self, time_diff: float, direction: TravelDirection) -> Dict[str, str]:
        """
        Calculate optimal light exposure times.
        
        Light is the primary zeitgeber (time cue) for circadian rhythms.
        Timing light exposure correctly can significantly speed adaptation.
        """
        light_times = {}
        
        if abs(time_diff) < 1:
            return {"note": "No special light timing needed"}
        
        if direction == TravelDirection.EAST:
            # For eastward travel, we want to ADVANCE our clock
            # Morning light advances the clock, evening light delays it
            light_times["morning"] = "Seek bright light (preferably sunlight) immediately after waking for 30-60 minutes"
            light_times["midday"] = "Normal indoor lighting is fine"
            light_times["evening"] = "Avoid bright light 2-3 hours before bed; use warm/dim lighting"
            light_times["peak_bright"] = "6:00 - 10:00 AM local time"
            light_times["avoid_bright"] = "8:00 PM - midnight local time"
        else:
            # For westward travel, we want to DELAY our clock
            # Evening light delays the clock, morning light advances it
            light_times["morning"] = "Avoid bright light for the first 1-2 hours after waking (wear sunglasses if needed)"
            light_times["midday"] = "Normal activity with moderate light"
            light_times["evening"] = "Seek bright light in the evening; stay active and lit until closer to bedtime"
            light_times["peak_bright"] = "6:00 - 10:00 PM local time"
            light_times["avoid_bright"] = "5:00 - 8:00 AM local time"
        
        return light_times
    
    def get_recovery_timeline(
        self,
        result: JetLagResult,
        start_date: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        """
        Generate a day-by-day recovery timeline.
        
        Args:
            result: JetLagResult from calculate()
            start_date: Starting date (defaults to today)
            
        Returns:
            List of daily recovery status dictionaries
        """
        if start_date is None:
            start_date = datetime.now()
            
        timeline = []
        recovery_days = int(result.estimated_recovery_days) + 1
        
        for day in range(recovery_days + 1):
            current_date = start_date + timedelta(days=day)
            
            # Calculate remaining phase shift
            if result.direction == TravelDirection.EAST:
                adjusted = day * self.PHASE_ADVANCE_RATE * self._get_age_factor()
            else:
                adjusted = day * self.PHASE_DELAY_RATE * self._get_age_factor()
                
            remaining = max(0, result.phase_shift_needed - adjusted)
            percent_recovered = min(100, (adjusted / result.phase_shift_needed) * 100) if result.phase_shift_needed > 0 else 100
            
            status = "fully_adjusted" if remaining < 0.5 else "adjusting"
            
            timeline.append({
                "day": day,
                "date": current_date.strftime("%Y-%m-%d"),
                "remaining_shift_hours": round(remaining, 1),
                "percent_recovered": round(percent_recovered, 1),
                "status": status
            })
            
        return timeline


def calculate_jet_lag(
    origin_offset: float,
    destination_offset: float,
    age: int = 30,
    sleep_type: str = "intermediate"
) -> JetLagResult:
    """
    Convenience function for quick jet lag calculation.
    
    Args:
        origin_offset: UTC offset of origin (e.g., -5 for EST)
        destination_offset: UTC offset of destination
        age: Traveler's age
        sleep_type: "morning_lark", "night_owl", or "intermediate"
        
    Returns:
        JetLagResult with jet lag analysis
    """
    sleep_map = {
        "morning_lark": SleepType.MORNING_LARK,
        "night_owl": SleepType.NIGHT_OWL,
        "intermediate": SleepType.INTERMEDIATE
    }
    
    calculator = JetLagCalculator(
        age=age,
        sleep_type=sleep_map.get(sleep_type.lower(), SleepType.INTERMEDIATE)
    )
    
    origin = TimezoneInfo.from_utc_offset(origin_offset)
    dest = TimezoneInfo.from_utc_offset(destination_offset)
    
    return calculator.calculate(origin, dest)


def get_common_timezones() -> Dict[str, float]:
    """
    Get a dictionary of common timezone names and their UTC offsets.
    
    Returns:
        Dict mapping timezone names to UTC offsets
    """
    return {
        "UTC": 0,
        "GMT": 0,
        "PST": -8,
        "PDT": -7,
        "MST": -7,
        "MDT": -6,
        "CST": -6,
        "CDT": -5,
        "EST": -5,
        "EDT": -4,
        "AST": -4,
        "ADT": -3,
        "BRT": -3,
        "UTC+1": 1,
        "CET": 1,
        "CEST": 2,
        "EET": 2,
        "EEST": 3,
        "MSK": 3,
        "IST": 5.5,
        "CST_China": 8,
        "JST": 9,
        "AEST": 10,
        "AEDT": 11,
        "NZST": 12,
        "NZDT": 13,
        "HST": -10,
        "AKST": -9,
        "AKDT": -8,
        "GMT+5:30": 5.5,
        "GMT+8": 8,
        "GMT+9": 9,
    }


def quick_estimate(hours_diff: float) -> Dict[str, Any]:
    """
    Quick estimation of jet lag recovery time.
    
    Args:
        hours_diff: Hours difference between origin and destination
        
    Returns:
        Dict with basic recovery estimate
    """
    hours_diff = abs(hours_diff)
    
    if hours_diff > 12:
        hours_diff = 24 - hours_diff
    
    if hours_diff < 1:
        return {
            "needs_adjustment": False,
            "message": "Minimal time difference - no adjustment needed"
        }
    
    # East travel is harder
    avg_recovery = (hours_diff / JetLagCalculator.PHASE_ADVANCE_RATE + 
                   hours_diff / JetLagCalculator.PHASE_DELAY_RATE) / 2
    
    return {
        "needs_adjustment": True,
        "time_difference_hours": hours_diff,
        "estimated_recovery_days": round(avg_recovery, 1),
        "min_recovery_days": round(hours_diff / JetLagCalculator.PHASE_DELAY_RATE, 1),
        "max_recovery_days": round(hours_diff / JetLagCalculator.PHASE_ADVANCE_RATE, 1),
        "tip": "Travel west for easier adjustment, east for more challenging adjustment"
    }


# Predefined routes for common travel corridors
POPULAR_ROUTES = {
    ("LAX", "JFK"): {"origin": -8, "dest": -5, "name": "Los Angeles to New York"},
    ("NYC", "LHR"): {"origin": -5, "dest": 0, "name": "New York to London"},
    ("LHR", "NYC"): {"origin": 0, "dest": -5, "name": "London to New York"},
    ("NYC", "TYO"): {"origin": -5, "dest": 9, "name": "New York to Tokyo"},
    ("TYO", "NYC"): {"origin": 9, "dest": -5, "name": "Tokyo to New York"},
    ("SYD", "LHR"): {"origin": 10, "dest": 0, "name": "Sydney to London"},
    ("LHR", "SYD"): {"origin": 0, "dest": 10, "name": "London to Sydney"},
    ("SFO", "HKG"): {"origin": -8, "dest": 8, "name": "San Francisco to Hong Kong"},
    ("DXB", "SYD"): {"origin": 4, "dest": 10, "name": "Dubai to Sydney"},
    ("SIN", "LAX"): {"origin": 8, "dest": -8, "name": "Singapore to Los Angeles"},
}


def analyze_route(origin_code: str, dest_code: str, age: int = 30) -> Optional[Dict[str, Any]]:
    """
    Analyze jet lag for a popular route by airport codes.
    
    Args:
        origin_code: Origin airport code (e.g., "LAX")
        dest_code: Destination airport code (e.g., "JFK")
        age: Traveler's age
        
    Returns:
        Dict with route analysis or None if route not found
    """
    route_key = (origin_code.upper(), dest_code.upper())
    
    if route_key not in POPULAR_ROUTES:
        return None
    
    route = POPULAR_ROUTES[route_key]
    result = calculate_jet_lag(route["origin"], route["dest"], age)
    
    return {
        "route_name": route["name"],
        "time_difference": result.time_difference,
        "direction": result.direction.value,
        "severity": result.severity_level,
        "recovery_days": result.estimated_recovery_days,
        "key_recommendations": result.recommendations[:3]
    }


# Export main classes and functions
__all__ = [
    'JetLagCalculator',
    'JetLagResult',
    'TimezoneInfo',
    'SleepType',
    'TravelDirection',
    'SleepSchedule',
    'calculate_jet_lag',
    'get_common_timezones',
    'quick_estimate',
    'analyze_route',
    'POPULAR_ROUTES',
]