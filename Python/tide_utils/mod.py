"""
Tide Prediction and Calculation Utilities

A comprehensive toolkit for calculating tidal predictions, heights, and patterns.
Implements harmonic analysis methods for tide prediction based on astronomical
positions of the moon and sun.

Features:
- Predict high and low tides for any date
- Calculate current tide height
- Identify spring and neap tides
- Estimate tide times based on lunar phase
- Support for different tidal constituents
- Tidal current calculations
- Geographic location adjustments

All calculations are based on simplified harmonic analysis and the
equilibrium tide theory. For precise navigation, use official tide tables.
"""

import math
from typing import List, Tuple, Optional, Dict
from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timedelta


class TideType(Enum):
    """Types of tides"""
    SPRING = "spring"  # Higher high tides, lower low tides (full/new moon)
    NEAP = "neap"      # Lower high tides, higher low tides (quarter moon)
    NORMAL = "normal"  # Intermediate tides


class TidePhase(Enum):
    """Tide phase"""
    RISING = "rising"    # Incoming tide (low to high)
    FALLING = "falling"  # Outgoing tide (high to low)
    HIGH = "high"         # At high tide
    LOW = "low"           # At low tide


class TidalPattern(Enum):
    """Tidal patterns by region"""
    DIURNAL = "diurnal"        # One high and one low per day
    SEMIDIURNAL = "semidiurnal"  # Two highs and two lows per day (most common)
    MIXED = "mixed"            # Mixed pattern


@dataclass
class TideEvent:
    """Represents a tide event (high or low)"""
    time: datetime
    height: float  # in meters
    is_high: bool
    tide_type: TideType
    phase: TidePhase


@dataclass
class TidalConstituent:
    """Represents a tidal constituent for harmonic analysis"""
    name: str
    amplitude: float  # in meters
    phase: float       # in degrees
    speed: float      # in degrees per hour (angular frequency)


@dataclass
class TidePrediction:
    """Complete tide prediction for a given time"""
    datetime: datetime
    height: float  # in meters
    phase: TidePhase
    tide_type: TideType
    next_high: Optional[datetime]
    next_low: Optional[datetime]
    time_to_next: timedelta
    height_change_rate: float  # meters per hour


class TideCalculator:
    """
    Main calculator for tide predictions using harmonic analysis.
    
    Uses simplified harmonic analysis based on the major tidal constituents:
    - M2 (principal lunar semidiurnal): ~12.42 hour period
    - S2 (principal solar semidiurnal): ~12.00 hour period
    - K1 (lunar diurnal): ~23.93 hour period
    - O1 (lunar diurnal): ~25.82 hour period
    - N2 (larger lunar elliptic semidiurnal): ~12.66 hour period
    """
    
    # Tidal constituent speeds (degrees per hour)
    M2_SPEED = 28.984104    # Principal lunar semidiurnal
    S2_SPEED = 30.0         # Principal solar semidiurnal
    K1_SPEED = 15.041069    # Lunar diurnal
    O1_SPEED = 13.943035    # Lunar diurnal
    N2_SPEED = 28.439730    # Larger lunar elliptic semidiurnal
    
    # Lunar cycle period (days)
    LUNAR_CYCLE = 29.530588853
    
    # Reference epoch for tide calculations (January 1, 2000, 00:00 UTC)
    REFERENCE_EPOCH = datetime(2000, 1, 1, 0, 0, 0)
    
    def __init__(self, 
                 mean_sea_level: float = 0.0,
                 m2_amplitude: float = 1.0,
                 s2_amplitude: float = 0.5,
                 k1_amplitude: float = 0.3,
                 o1_amplitude: float = 0.2,
                 n2_amplitude: float = 0.2,
                 m2_phase: float = 0.0,
                 s2_phase: float = 0.0):
        """
        Initialize tide calculator with location-specific parameters.
        
        Args:
            mean_sea_level: Mean sea level in meters (datum)
            m2_amplitude: M2 constituent amplitude (principal lunar)
            s2_amplitude: S2 constituent amplitude (principal solar)
            k1_amplitude: K1 constituent amplitude (diurnal)
            o1_amplitude: O1 constituent amplitude (diurnal)
            n2_amplitude: N2 constituent amplitude (elliptic lunar)
            m2_phase: M2 phase lag in degrees
            s2_phase: S2 phase lag in degrees
        """
        self.mean_sea_level = mean_sea_level
        self.m2_amplitude = m2_amplitude
        self.s2_amplitude = s2_amplitude
        self.k1_amplitude = k1_amplitude
        self.o1_amplitude = o1_amplitude
        self.n2_amplitude = n2_amplitude
        self.m2_phase = m2_phase
        self.s2_phase = s2_phase
    
    def calculate_tide_height(self, dt: datetime) -> float:
        """
        Calculate tide height at a specific datetime.
        
        Uses harmonic analysis with the major tidal constituents.
        
        Args:
            dt: Datetime to calculate tide height for
            
        Returns:
            Tide height in meters relative to mean sea level
        """
        # Calculate hours since reference epoch
        hours = (dt - self.REFERENCE_EPOCH).total_seconds() / 3600
        
        # Harmonic analysis: sum of sinusoidal constituents
        height = 0.0
        
        # M2 - Principal lunar semidiurnal (most important)
        m2_angle = math.radians(self.M2_SPEED * hours + self.m2_phase)
        height += self.m2_amplitude * math.cos(m2_angle)
        
        # S2 - Principal solar semidiurnal
        s2_angle = math.radians(self.S2_SPEED * hours + self.s2_phase)
        height += self.s2_amplitude * math.cos(s2_angle)
        
        # K1 - Lunar diurnal
        k1_angle = math.radians(self.K1_SPEED * hours)
        height += self.k1_amplitude * math.cos(k1_angle)
        
        # O1 - Lunar diurnal
        o1_angle = math.radians(self.O1_SPEED * hours)
        height += self.o1_amplitude * math.cos(o1_angle)
        
        # N2 - Larger lunar elliptic semidiurnal
        n2_angle = math.radians(self.N2_SPEED * hours)
        height += self.n2_amplitude * math.cos(n2_angle)
        
        return height + self.mean_sea_level
    
    def get_tide_phase(self, dt: datetime) -> TidePhase:
        """
        Determine if tide is rising, falling, or at high/low.
        
        Args:
            dt: Datetime to check
            
        Returns:
            Current tide phase
        """
        # Check heights at slightly different times
        delta = timedelta(minutes=6)
        height_before = self.calculate_tide_height(dt - delta)
        height_now = self.calculate_tide_height(dt)
        height_after = self.calculate_tide_height(dt + delta)
        
        # Calculate rate of change
        rate_before = (height_now - height_before) / delta.total_seconds()
        rate_after = (height_after - height_now) / delta.total_seconds()
        
        # Threshold for "at high/low" (very small change)
        threshold = 0.00001
        
        if abs(rate_before) < threshold and abs(rate_after) < threshold:
            if rate_before > 0:
                return TidePhase.LOW
            else:
                return TidePhase.HIGH
        
        if height_after > height_now:
            return TidePhase.RISING
        else:
            return TidePhase.FALLING
    
    def get_tide_type(self, dt: datetime) -> TideType:
        """
        Determine if current tide is spring, neap, or normal.
        
        Spring tides occur during full and new moons.
        Neap tides occur during quarter moons.
        
        Args:
            dt: Datetime to check
            
        Returns:
            Type of tide
        """
        # Calculate lunar age (days since new moon)
        lunar_age = self.get_lunar_age(dt)
        
        # Lunar age ranges from 0 to ~29.53
        # New moon: ~0, ~29.53
        # Full moon: ~14.77
        # First quarter: ~7.38
        # Last quarter: ~22.15
        
        # Distance to nearest spring tide (new or full moon)
        dist_to_new = min(lunar_age, self.LUNAR_CYCLE - lunar_age)
        dist_to_full = abs(lunar_age - self.LUNAR_CYCLE / 2)
        dist_to_spring = min(dist_to_new, dist_to_full)
        
        # Distance to nearest neap tide (quarter moon)
        dist_to_first_quarter = abs(lunar_age - self.LUNAR_CYCLE / 4)
        dist_to_last_quarter = abs(lunar_age - 3 * self.LUNAR_CYCLE / 4)
        dist_to_neap = min(dist_to_first_quarter, dist_to_last_quarter)
        
        # Determine tide type based on proximity
        if dist_to_spring < 2:
            return TideType.SPRING
        elif dist_to_neap < 2:
            return TideType.NEAP
        else:
            return TideType.NORMAL
    
    def get_lunar_age(self, dt: datetime) -> float:
        """
        Calculate lunar age (days since new moon).
        
        Uses a simplified synodic month calculation.
        
        Args:
            dt: Datetime to calculate for
            
        Returns:
            Lunar age in days (0 to ~29.53)
        """
        # Days since reference new moon (Jan 6, 2000)
        ref_new_moon = datetime(2000, 1, 6, 18, 14, 0)
        days = (dt - ref_new_moon).total_seconds() / 86400
        
        # Calculate position in lunar cycle
        lunar_age = days % self.LUNAR_CYCLE
        return lunar_age
    
    def get_lunar_phase_name(self, dt: datetime) -> str:
        """
        Get human-readable lunar phase name.
        
        Args:
            dt: Datetime to check
            
        Returns:
            Lunar phase name
        """
        lunar_age = self.get_lunar_age(dt)
        
        if lunar_age < 1.85:
            return "New Moon"
        elif lunar_age < 7.38:
            return "Waxing Crescent"
        elif lunar_age < 9.23:
            return "First Quarter"
        elif lunar_age < 14.77:
            return "Waxing Gibbous"
        elif lunar_age < 16.61:
            return "Full Moon"
        elif lunar_age < 22.15:
            return "Waning Gibbous"
        elif lunar_age < 24.00:
            return "Last Quarter"
        else:
            return "Waning Crescent"
    
    def find_next_high_tide(self, dt: datetime, 
                           search_hours: int = 12) -> Optional[TideEvent]:
        """
        Find the next high tide after the given datetime.
        
        Args:
            dt: Starting datetime
            search_hours: Maximum hours to search ahead
            
        Returns:
            TideEvent for the next high tide, or None if not found
        """
        # Search for high tide by finding when derivative changes sign
        current = dt
        end_time = dt + timedelta(hours=search_hours)
        
        # Sample every 10 minutes
        while current < end_time:
            phase = self.get_tide_phase(current)
            if phase == TidePhase.HIGH:
                height = self.calculate_tide_height(current)
                tide_type = self.get_tide_type(current)
                return TideEvent(
                    time=current,
                    height=height,
                    is_high=True,
                    tide_type=tide_type,
                    phase=TidePhase.HIGH
                )
            current += timedelta(minutes=10)
        
        return None
    
    def find_next_low_tide(self, dt: datetime,
                          search_hours: int = 12) -> Optional[TideEvent]:
        """
        Find the next low tide after the given datetime.
        
        Args:
            dt: Starting datetime
            search_hours: Maximum hours to search ahead
            
        Returns:
            TideEvent for the next low tide, or None if not found
        """
        current = dt
        end_time = dt + timedelta(hours=search_hours)
        
        while current < end_time:
            phase = self.get_tide_phase(current)
            if phase == TidePhase.LOW:
                height = self.calculate_tide_height(current)
                tide_type = self.get_tide_type(current)
                return TideEvent(
                    time=current,
                    height=height,
                    is_high=False,
                    tide_type=tide_type,
                    phase=TidePhase.LOW
                )
            current += timedelta(minutes=10)
        
        return None
    
    def get_tide_events(self, start: datetime, end: datetime) -> List[TideEvent]:
        """
        Get all tide events (highs and lows) in a time range.
        
        Args:
            start: Start datetime
            end: End datetime
            
        Returns:
            List of TideEvent objects sorted by time
        """
        events = []
        current = start
        
        while current < end:
            phase = self.get_tide_phase(current)
            
            if phase in (TidePhase.HIGH, TidePhase.LOW):
                height = self.calculate_tide_height(current)
                tide_type = self.get_tide_type(current)
                events.append(TideEvent(
                    time=current,
                    height=height,
                    is_high=(phase == TidePhase.HIGH),
                    tide_type=tide_type,
                    phase=phase
                ))
                # Skip ahead to avoid duplicate detection
                current += timedelta(hours=4)
            else:
                current += timedelta(minutes=10)
        
        return events
    
    def get_prediction(self, dt: datetime) -> TidePrediction:
        """
        Get complete tide prediction for a specific time.
        
        Args:
            dt: Datetime to predict for
            
        Returns:
            TidePrediction with all information
        """
        height = self.calculate_tide_height(dt)
        phase = self.get_tide_phase(dt)
        tide_type = self.get_tide_type(dt)
        
        # Find next high and low tides
        next_high_event = self.find_next_high_tide(dt)
        next_low_event = self.find_next_low_tide(dt)
        
        next_high = next_high_event.time if next_high_event else None
        next_low = next_low_event.time if next_low_event else None
        
        # Calculate time to next event
        if next_high and next_low:
            if next_high < next_low:
                time_to_next = next_high - dt
            else:
                time_to_next = next_low - dt
        elif next_high:
            time_to_next = next_high - dt
        elif next_low:
            time_to_next = next_low - dt
        else:
            time_to_next = timedelta(0)
        
        # Calculate rate of height change (meters per hour)
        delta = timedelta(minutes=30)
        height_future = self.calculate_tide_height(dt + delta)
        height_change_rate = (height_future - height) / (delta.total_seconds() / 3600)
        
        return TidePrediction(
            datetime=dt,
            height=round(height, 3),
            phase=phase,
            tide_type=tide_type,
            next_high=next_high,
            next_low=next_low,
            time_to_next=time_to_next,
            height_change_rate=round(height_change_rate, 4)
        )
    
    def calculate_tidal_range(self, dt: datetime) -> float:
        """
        Calculate the tidal range (difference between high and low).
        
        Args:
            dt: Reference datetime
            
        Returns:
            Tidal range in meters
        """
        # Sample heights over a 24-hour period centered on dt
        start = dt - timedelta(hours=12)
        end = dt + timedelta(hours=12)
        
        heights = []
        current = start
        
        while current <= end:
            heights.append(self.calculate_tide_height(current))
            current += timedelta(minutes=30)
        
        if len(heights) >= 2:
            return max(heights) - min(heights)
        return 0.0
    
    def estimate_tidal_current(self, dt: datetime) -> Tuple[str, float]:
        """
        Estimate tidal current strength and direction.
        
        Currents are strongest at mid-tide and weakest at high/low slack.
        
        Args:
            dt: Datetime to estimate for
            
        Returns:
            Tuple of (direction, speed) where speed is relative (0-1)
        """
        phase = self.get_tide_phase(dt)
        prediction = self.get_prediction(dt)
        
        # Calculate tidal range
        tidal_range = self.calculate_tidal_range(dt)
        
        # Estimate current strength based on position in tidal cycle
        if phase in (TidePhase.HIGH, TidePhase.LOW):
            # Slack water - minimal current
            return ("slack", 0.0)
        
        # Calculate how far from nearest extreme
        if prediction.next_high and prediction.next_low:
            time_to_high = (prediction.next_high - dt).total_seconds()
            time_to_low = (prediction.next_low - dt).total_seconds()
            
            # Approximate time to nearest extreme
            min_time = min(time_to_high, time_to_low)
            
            # Current is strongest at mid-tide (about 3 hours from extreme)
            # Assuming 6-hour tide cycle
            mid_tide_time = 3 * 3600  # 3 hours in seconds
            
            # Calculate relative strength (0 at extremes, 1 at mid-tide)
            relative_time = abs(min_time - mid_tide_time)
            strength = 1.0 - (relative_time / mid_tide_time)
            strength = max(0.0, min(1.0, strength))
            
            # Adjust for tidal range (bigger range = stronger current)
            strength *= min(1.0, tidal_range / 2.0)
            
            if phase == TidePhase.RISING:
                return ("flood", round(strength, 2))
            else:
                return ("ebb", round(strength, 2))
        
        return ("unknown", 0.0)
    
    def get_tidal_coefficient(self, dt: datetime) -> float:
        """
        Calculate the tidal coefficient (used in French tide tables).
        
        Ranges from 20 (neap tide) to 120 (spring tide).
        Average is around 70.
        
        Args:
            dt: Datetime to calculate for
            
        Returns:
            Tidal coefficient
        """
        tide_type = self.get_tide_type(dt)
        
        # Base coefficient based on tide type
        if tide_type == TideType.SPRING:
            return 95.0
        elif tide_type == TideType.NEAP:
            return 45.0
        else:
            # Interpolate based on lunar age
            lunar_age = self.get_lunar_age(dt)
            
            # Distance to nearest spring tide
            dist_to_new = min(lunar_age, self.LUNAR_CYCLE - lunar_age)
            dist_to_full = abs(lunar_age - self.LUNAR_CYCLE / 2)
            dist_to_spring = min(dist_to_new, dist_to_full)
            
            # Distance to nearest neap tide
            dist_to_first_quarter = abs(lunar_age - self.LUNAR_CYCLE / 4)
            dist_to_last_quarter = abs(lunar_age - 3 * self.LUNAR_CYCLE / 4)
            dist_to_neap = min(dist_to_first_quarter, dist_to_last_quarter)
            
            # Interpolate coefficient
            # Spring: 95, Neap: 45
            # At midpoint between spring and neap: ~70
            if dist_to_spring < dist_to_neap:
                # Closer to spring
                return 70 + (25 * (1 - dist_to_spring / 7.38))
            else:
                # Closer to neap
                return 70 - (25 * (1 - dist_to_neap / 7.38))


def create_semidiurnal_tides(mean_high: float, mean_low: float, 
                            mean_sea_level: float = 0.0) -> TideCalculator:
    """
    Create a calculator for typical semidiurnal tides.
    
    Semidiurnal tides have two high tides and two low tides each day,
    with relatively equal heights (most common type).
    
    Args:
        mean_high: Mean high water in meters
        mean_low: Mean low water in meters
        mean_sea_level: Mean sea level datum
        
    Returns:
        Configured TideCalculator
    """
    tidal_range = mean_high - mean_low
    m2_amp = tidal_range / 2 * 0.9
    s2_amp = tidal_range / 2 * 0.3
    
    return TideCalculator(
        mean_sea_level=mean_sea_level,
        m2_amplitude=m2_amp,
        s2_amplitude=s2_amp,
        k1_amplitude=tidal_range * 0.05,
        o1_amplitude=tidal_range * 0.04,
        n2_amplitude=tidal_range * 0.15
    )


def create_mixed_tides(mean_high: float, mean_low: float,
                      mean_sea_level: float = 0.0) -> TideCalculator:
    """
    Create a calculator for mixed tides (diurnal inequality).
    
    Mixed tides have two high tides and two low tides each day,
    but with significant height differences (common on Pacific coast).
    
    Args:
        mean_high: Mean high water in meters
        mean_low: Mean low water in meters
        mean_sea_level: Mean sea level datum
        
    Returns:
        Configured TideCalculator
    """
    tidal_range = mean_high - mean_low
    m2_amp = tidal_range / 2 * 0.6
    s2_amp = tidal_range / 2 * 0.2
    k1_amp = tidal_range * 0.25
    o1_amp = tidal_range * 0.2
    
    return TideCalculator(
        mean_sea_level=mean_sea_level,
        m2_amplitude=m2_amp,
        s2_amplitude=s2_amp,
        k1_amplitude=k1_amp,
        o1_amplitude=o1_amp,
        n2_amplitude=tidal_range * 0.1
    )


def create_diurnal_tides(mean_high: float, mean_low: float,
                        mean_sea_level: float = 0.0) -> TideCalculator:
    """
    Create a calculator for diurnal tides.
    
    Diurnal tides have only one high tide and one low tide each day.
    
    Args:
        mean_high: Mean high water in meters
        mean_low: Mean low water in meters
        mean_sea_level: Mean sea level datum
        
    Returns:
        Configured TideCalculator
    """
    tidal_range = mean_high - mean_low
    
    return TideCalculator(
        mean_sea_level=mean_sea_level,
        m2_amplitude=tidal_range * 0.1,
        s2_amplitude=tidal_range * 0.05,
        k1_amplitude=tidal_range / 2 * 0.7,
        o1_amplitude=tidal_range / 2 * 0.5,
        n2_amplitude=tidal_range * 0.02
    )


def quick_tide_height(dt: datetime, 
                      m2_amplitude: float = 1.0,
                      s2_amplitude: float = 0.5) -> float:
    """
    Quick calculation of tide height using simplified M2 and S2 constituents.
    
    Args:
        dt: Datetime to calculate for
        m2_amplitude: M2 (lunar) amplitude in meters
        s2_amplitude: S2 (solar) amplitude in meters
        
    Returns:
        Tide height in meters
    """
    calc = TideCalculator(m2_amplitude=m2_amplitude, s2_amplitude=s2_amplitude)
    return calc.calculate_tide_height(dt)


def is_good_fishing_time(dt: datetime, calculator: TideCalculator) -> Tuple[bool, str]:
    """
    Determine if it's a good time for fishing based on tides.
    
    Best fishing times are typically:
    - During moving tides (rising or falling)
    - Around high or low tide
    - During spring tides
    
    Args:
        dt: Datetime to check
        calculator: TideCalculator instance
        
    Returns:
        Tuple of (is_good, reason)
    """
    prediction = calculator.get_prediction(dt)
    
    # Good during moving tides
    if prediction.phase in (TidePhase.RISING, TidePhase.FALLING):
        if prediction.tide_type == TideType.SPRING:
            return True, "Excellent - spring tide with moving water"
        return True, "Good - moving tide brings active fish"
    
    # Okay near tide extremes
    if prediction.time_to_next.total_seconds() < 1800:  # 30 minutes
        return True, "Good - fish often feed near tide changes"
    
    # Less ideal during slack water
    return False, "Slow - slack water, fish less active"


def get_tide_table(dt: datetime, days: int = 1, 
                  calculator: TideCalculator = None) -> List[Dict]:
    """
    Generate a tide table for multiple days.
    
    Args:
        dt: Starting datetime
        days: Number of days
        calculator: TideCalculator instance (creates default if None)
        
    Returns:
        List of dictionaries with tide information
    """
    if calculator is None:
        calculator = TideCalculator()
    
    table = []
    end_time = dt + timedelta(days=days)
    
    events = calculator.get_tide_events(dt, end_time)
    
    for event in events:
        table.append({
            "date": event.time.strftime("%Y-%m-%d"),
            "time": event.time.strftime("%H:%M"),
            "height_m": round(event.height, 2),
            "type": "High" if event.is_high else "Low",
            "tide_type": event.tide_type.value,
            "lunar_phase": calculator.get_lunar_phase_name(event.time)
        })
    
    return table


def calculate_tide_window(dt: datetime, 
                         calculator: TideCalculator,
                         min_depth: float = 0.0) -> Tuple[datetime, datetime]:
    """
    Calculate the next tide window when height is above minimum.
    
    Useful for determining when boats can safely navigate shallow areas.
    
    Args:
        dt: Starting datetime
        calculator: TideCalculator instance
        min_depth: Minimum required depth in meters
        
    Returns:
        Tuple of (start_time, end_time) for safe navigation window
    """
    # Search forward for window
    current = dt
    window_start = None
    window_end = None
    
    # Search up to 24 hours ahead
    for _ in range(24 * 6):  # Check every 10 minutes
        height = calculator.calculate_tide_height(current)
        
        if height >= min_depth:
            if window_start is None:
                window_start = current
            window_end = current
        else:
            if window_start is not None:
                # Window ended
                break
        
        current += timedelta(minutes=10)
    
    return (window_start, window_end)


# Common location presets (simplified parameters)
LOCATION_PRESETS = {
    "generic_semidiurnal": {
        "m2_amplitude": 1.0,
        "s2_amplitude": 0.3,
        "k1_amplitude": 0.1,
        "o1_amplitude": 0.08,
    },
    "generic_mixed": {
        "m2_amplitude": 0.6,
        "s2_amplitude": 0.2,
        "k1_amplitude": 0.25,
        "o1_amplitude": 0.2,
    },
    "generic_diurnal": {
        "m2_amplitude": 0.1,
        "s2_amplitude": 0.05,
        "k1_amplitude": 0.5,
        "o1_amplitude": 0.4,
    },
}


def get_tide_calculator_for_location(location: str = "generic_semidiurnal") -> TideCalculator:
    """
    Get a pre-configured tide calculator for a location type.
    
    Args:
        location: Location preset name
        
    Returns:
        Configured TideCalculator
    """
    preset = LOCATION_PRESETS.get(location, LOCATION_PRESETS["generic_semidiurnal"])
    return TideCalculator(**preset)