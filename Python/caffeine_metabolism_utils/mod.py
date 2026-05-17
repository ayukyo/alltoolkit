"""
Caffeine Metabolism Utils - Track caffeine levels in the body over time.

This module provides tools to calculate caffeine metabolism, track consumption,
and estimate when caffeine levels will reach safe levels for sleep.

Key features:
- Calculate current caffeine levels using half-life decay
- Track multiple caffeine sources over time
- Estimate sleep-safe time based on caffeine thresholds
- Support for different beverages and their typical caffeine content

Physics model:
- Caffeine follows first-order kinetics
- Average half-life: 5-6 hours (varies by individual)
- Peak absorption: 30-60 minutes after consumption
"""

from datetime import datetime, timedelta
from typing import List, Optional, Dict, Tuple
import math


# Common beverages and their typical caffeine content (mg)
BEVERAGE_DATABASE = {
    # Coffee
    "espresso_single": 63,
    "espresso_double": 125,
    "drip_coffee_small": 95,
    "drip_coffee_medium": 165,
    "drip_coffee_large": 330,
    "cold_brew_small": 200,
    "cold_brew_medium": 300,
    "cold_brew_large": 400,
    "latte_small": 63,
    "latte_medium": 95,
    "latte_large": 125,
    "cappuccino": 63,
    "americano_small": 75,
    "americano_medium": 150,
    "americano_large": 225,
    
    # Tea
    "black_tea": 47,
    "green_tea": 28,
    "white_tea": 25,
    "oolong_tea": 38,
    "matcha": 70,
    "chai_tea": 47,
    "iced_tea": 47,
    
    # Energy drinks
    "red_bull_small": 80,
    "red_bull_large": 111,
    "monster_small": 160,
    "monster_large": 240,
    "rockstar": 160,
    "bang_energy": 300,
    "celcius": 200,
    "prime_energy": 200,
    
    # Soda
    "coke_can": 34,
    "coke_bottle": 57,
    "pepsi_can": 38,
    "pepsi_bottle": 63,
    "mountain_dew_can": 54,
    "mountain_dew_bottle": 90,
    "dr_pepper_can": 41,
    
    # Other
    "dark_chocolate_bar": 23,
    "milk_chocolate_bar": 9,
    "energy_shot": 215,
    "pre_workout": 300,
    "excedrin": 130,
    "midol": 60,
    "no_doze": 200,
}


class CaffeineEntry:
    """Represents a single caffeine consumption event."""
    
    def __init__(
        self,
        amount_mg: float,
        timestamp: datetime,
        source: str = "custom",
        absorption_delay_minutes: int = 45
    ):
        """
        Initialize a caffeine entry.
        
        Args:
            amount_mg: Amount of caffeine in milligrams
            timestamp: When the caffeine was consumed
            source: Name or type of beverage (for tracking)
            absorption_delay_minutes: Time to peak absorption (default 45 min)
        """
        self.amount_mg = amount_mg
        self.timestamp = timestamp
        self.source = source
        self.absorption_delay_minutes = absorption_delay_minutes
    
    def to_dict(self) -> dict:
        """Convert entry to dictionary."""
        return {
            "amount_mg": self.amount_mg,
            "timestamp": self.timestamp.isoformat(),
            "source": self.source,
            "absorption_delay_minutes": self.absorption_delay_minutes
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "CaffeineEntry":
        """Create entry from dictionary."""
        # Parse ISO format timestamp (compatible with Python 3.6)
        ts_str = data["timestamp"]
        # Handle both 'YYYY-MM-DDTHH:MM:SS' and 'YYYY-MM-DDTHH:MM:SS.mmmmmm'
        if '.' in ts_str:
            timestamp = datetime.strptime(ts_str, "%Y-%m-%dT%H:%M:%S.%f")
        else:
            timestamp = datetime.strptime(ts_str, "%Y-%m-%dT%H:%M:%S")
        
        return cls(
            amount_mg=data["amount_mg"],
            timestamp=timestamp,
            source=data.get("source", "custom"),
            absorption_delay_minutes=data.get("absorption_delay_minutes", 45)
        )


class CaffeineMetabolismTracker:
    """
    Track caffeine consumption and metabolism over time.
    
    Uses pharmacokinetic modeling to estimate current caffeine levels
    based on consumption history and individual metabolism parameters.
    """
    
    # Default half-life in hours (average for adults)
    DEFAULT_HALF_LIFE = 5.0
    
    # Recommended maximum daily intake (FDA)
    MAX_DAILY_RECOMMENDED_MG = 400
    
    # Threshold for minimal effect on sleep (mg)
    SLEEP_SAFE_THRESHOLD_MG = 25
    
    def __init__(
        self,
        half_life_hours: float = DEFAULT_HALF_LIFE,
        sleep_safe_threshold_mg: float = SLEEP_SAFE_THRESHOLD_MG
    ):
        """
        Initialize the tracker.
        
        Args:
            half_life_hours: Caffeine half-life in hours (default 5, range 3-7)
            sleep_safe_threshold_mg: Level below which sleep is minimally affected
        """
        if half_life_hours <= 0:
            raise ValueError("Half-life must be positive")
        if sleep_safe_threshold_mg <= 0:
            raise ValueError("Sleep threshold must be positive")
        
        self.half_life_hours = half_life_hours
        self.sleep_safe_threshold_mg = sleep_safe_threshold_mg
        self.entries: List[CaffeineEntry] = []
    
    def _calculate_decay_constant(self) -> float:
        """Calculate the elimination rate constant (k) from half-life."""
        # k = ln(2) / half_life
        return math.log(2) / self.half_life_hours
    
    def consume(
        self,
        amount_mg: float,
        timestamp: Optional[datetime] = None,
        source: str = "custom",
        absorption_delay_minutes: int = 45
    ) -> CaffeineEntry:
        """
        Log a caffeine consumption event.
        
        Args:
            amount_mg: Amount of caffeine consumed (mg)
            timestamp: When consumed (defaults to now)
            source: Beverage name or identifier
            absorption_delay_minutes: Time to peak absorption
            
        Returns:
            The created CaffeineEntry
        """
        if amount_mg <= 0:
            raise ValueError("Amount must be positive")
        
        if timestamp is None:
            timestamp = datetime.now()
        
        entry = CaffeineEntry(
            amount_mg=amount_mg,
            timestamp=timestamp,
            source=source,
            absorption_delay_minutes=absorption_delay_minutes
        )
        self.entries.append(entry)
        return entry
    
    def consume_beverage(
        self,
        beverage_key: str,
        timestamp: Optional[datetime] = None,
        custom_amount_mg: Optional[float] = None
    ) -> CaffeineEntry:
        """
        Consume a predefined beverage.
        
        Args:
            beverage_key: Key from BEVERAGE_DATABASE (e.g., "drip_coffee_medium")
            timestamp: When consumed (defaults to now)
            custom_amount_mg: Override the database amount
            
        Returns:
            The created CaffeineEntry
        """
        if beverage_key not in BEVERAGE_DATABASE:
            raise ValueError(f"Unknown beverage: {beverage_key}. "
                           f"Available: {list(BEVERAGE_DATABASE.keys())}")
        
        amount = custom_amount_mg if custom_amount_mg else BEVERAGE_DATABASE[beverage_key]
        return self.consume(amount, timestamp, source=beverage_key)
    
    def get_current_level(self, at_time: Optional[datetime] = None) -> float:
        """
        Calculate current total caffeine level in the body.
        
        Args:
            at_time: Time to calculate for (defaults to now)
            
        Returns:
            Total caffeine level in mg
        """
        if at_time is None:
            at_time = datetime.now()
        
        total = 0.0
        k = self._calculate_decay_constant()
        
        for entry in self.entries:
            # Time since consumption in hours
            hours_since = (at_time - entry.timestamp).total_seconds() / 3600
            
            if hours_since < 0:
                # Future entry, skip
                continue
            
            # Absorption phase (0 to absorption_delay)
            absorption_hours = entry.absorption_delay_minutes / 60
            
            if hours_since < absorption_hours:
                # Linear absorption to peak
                absorption_fraction = hours_since / absorption_hours
                effective_amount = entry.amount_mg * absorption_fraction
            else:
                # Elimination phase (exponential decay)
                effective_hours = hours_since - absorption_hours
                effective_amount = entry.amount_mg * math.exp(-k * effective_hours)
            
            total += effective_amount
        
        return total
    
    def get_level_at(self, target_time: datetime) -> float:
        """Calculate caffeine level at a specific time."""
        return self.get_current_level(target_time)
    
    def get_level_history(
        self,
        start_time: datetime,
        end_time: datetime,
        interval_minutes: int = 30
    ) -> List[Dict]:
        """
        Get caffeine level history over a time range.
        
        Args:
            start_time: Start of range
            end_time: End of range
            interval_minutes: Sampling interval
            
        Returns:
            List of dicts with timestamp and level_mg
        """
        history = []
        current = start_time
        
        while current <= end_time:
            level = self.get_level_at(current)
            history.append({
                "timestamp": current.isoformat(),
                "level_mg": round(level, 2)
            })
            current += timedelta(minutes=interval_minutes)
        
        return history
    
    def time_until_threshold(
        self,
        threshold_mg: Optional[float] = None,
        from_time: Optional[datetime] = None
    ) -> Optional[timedelta]:
        """
        Calculate time until caffeine level drops below threshold.
        
        Args:
            threshold_mg: Target threshold (defaults to sleep_safe_threshold)
            from_time: Starting time (defaults to now)
            
        Returns:
            Time delta until threshold is reached, or None if already below
        """
        if threshold_mg is None:
            threshold_mg = self.sleep_safe_threshold_mg
        
        if from_time is None:
            from_time = datetime.now()
        
        current_level = self.get_level_at(from_time)
        
        if current_level <= threshold_mg:
            return None  # Already below threshold
        
        # Binary search for the time
        k = self._calculate_decay_constant()
        total_amount = sum(e.amount_mg for e in self.entries 
                         if e.timestamp <= from_time)
        
        # Simplified: assume all caffeine decays from peak at the same time
        # For more accuracy, would need to track each entry separately
        # This approximation works well for single-source calculations
        
        # Use Newton-Raphson or simple iteration
        max_hours = 24  # Max search time
        test_time = from_time
        
        for hours in [i * 0.25 for i in range(1, int(max_hours * 4) + 1)]:
            test_time = from_time + timedelta(hours=hours)
            level = self.get_level_at(test_time)
            if level <= threshold_mg:
                return timedelta(hours=hours)
        
        return timedelta(hours=max_hours)
    
    def get_sleep_recommendation(
        self,
        target_bedtime: Optional[datetime] = None,
        from_time: Optional[datetime] = None
    ) -> Dict:
        """
        Get recommendation for sleep timing based on caffeine levels.
        
        Args:
            target_bedtime: Desired bedtime (defaults to 10 PM today)
            from_time: Current/reference time (defaults to now)
            
        Returns:
            Dict with sleep recommendations
        """
        if from_time is None:
            from_time = datetime.now()
        
        if target_bedtime is None:
            # Default to 10 PM
            target_bedtime = from_time.replace(hour=22, minute=0, second=0, microsecond=0)
            if target_bedtime < from_time:
                target_bedtime += timedelta(days=1)
        
        current_level = self.get_level_at(from_time)
        bedtime_level = self.get_level_at(target_bedtime)
        
        time_to_safe = self.time_until_threshold(
            self.sleep_safe_threshold_mg, from_time
        )
        
        safe_bedtime = target_bedtime >= from_time + (time_to_safe or timedelta(0))
        
        return {
            "current_level_mg": round(current_level, 2),
            "bedtime_level_mg": round(bedtime_level, 2),
            "is_safe_to_sleep": bedtime_level <= self.sleep_safe_threshold_mg,
            "sleep_safe_threshold_mg": self.sleep_safe_threshold_mg,
            "time_until_safe": str(time_to_safe) if time_to_safe else "Already safe",
            "recommended_bedtime": (from_time + time_to_safe).isoformat() if time_to_safe else from_time.isoformat(),
            "target_bedtime": target_bedtime.isoformat(),
            "safe_bedtime_achieved": safe_bedtime
        }
    
    def get_daily_total(
        self,
        date: Optional[datetime] = None
    ) -> Tuple[float, List[CaffeineEntry]]:
        """
        Get total caffeine consumed on a specific date.
        
        Args:
            date: Date to check (defaults to today)
            
        Returns:
            Tuple of (total_mg, list of entries)
        """
        if date is None:
            date = datetime.now()
        
        day_start = date.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start + timedelta(days=1)
        
        day_entries = [
            e for e in self.entries
            if day_start <= e.timestamp < day_end
        ]
        
        total = sum(e.amount_mg for e in day_entries)
        return total, day_entries
    
    def get_status(self, at_time: Optional[datetime] = None) -> Dict:
        """
        Get comprehensive status report.
        
        Args:
            at_time: Time for calculation (defaults to now)
            
        Returns:
            Dict with all status information
        """
        if at_time is None:
            at_time = datetime.now()
        
        daily_total, daily_entries = self.get_daily_total(at_time)
        current_level = self.get_current_level(at_time)
        time_to_safe = self.time_until_threshold(from_time=at_time)
        
        return {
            "current_level_mg": round(current_level, 2),
            "daily_total_mg": round(daily_total, 2),
            "daily_entries_count": len(daily_entries),
            "max_daily_recommended_mg": self.MAX_DAILY_RECOMMENDED_MG,
            "within_daily_limit": daily_total <= self.MAX_DAILY_RECOMMENDED_MG,
            "sleep_safe_threshold_mg": self.sleep_safe_threshold_mg,
            "time_until_safe": str(time_to_safe) if time_to_safe else "Already safe",
            "half_life_hours": self.half_life_hours,
            "total_entries": len(self.entries)
        }
    
    def clear_old_entries(self, older_than_hours: int = 48) -> int:
        """
        Remove entries older than specified hours.
        
        Args:
            older_than_hours: Threshold age in hours
            
        Returns:
            Number of entries removed
        """
        cutoff = datetime.now() - timedelta(hours=older_than_hours)
        original_count = len(self.entries)
        self.entries = [e for e in self.entries if e.timestamp > cutoff]
        return original_count - len(self.entries)
    
    def export_data(self) -> List[dict]:
        """Export all entries as list of dicts."""
        return [e.to_dict() for e in self.entries]
    
    def import_data(self, data: List[dict]) -> int:
        """
        Import entries from list of dicts.
        
        Args:
            data: List of entry dicts
            
        Returns:
            Number of entries imported
        """
        count = 0
        for entry_data in data:
            try:
                entry = CaffeineEntry.from_dict(entry_data)
                self.entries.append(entry)
                count += 1
            except (KeyError, ValueError):
                continue
        return count
    
    @staticmethod
    def get_beverage_list() -> Dict[str, int]:
        """Get all available predefined beverages."""
        return BEVERAGE_DATABASE.copy()
    
    @staticmethod
    def search_beverages(query: str) -> Dict[str, int]:
        """
        Search for beverages matching a query.
        
        Args:
            query: Search string
            
        Returns:
            Dict of matching beverages and their caffeine content
        """
        query_lower = query.lower()
        return {
            k: v for k, v in BEVERAGE_DATABASE.items()
            if query_lower in k.lower()
        }


def calculate_caffeine_decay(
    initial_mg: float,
    hours: float,
    half_life_hours: float = 5.0
) -> float:
    """
    Simple function to calculate caffeine after hours of decay.
    
    Args:
        initial_mg: Starting caffeine amount
        hours: Hours elapsed
        half_life_hours: Caffeine half-life
        
    Returns:
        Remaining caffeine in mg
    """
    k = math.log(2) / half_life_hours
    return initial_mg * math.exp(-k * hours)


def calculate_half_life_from_data(
    initial_mg: float,
    remaining_mg: float,
    hours_elapsed: float
) -> float:
    """
    Calculate individual half-life from observed data.
    
    Args:
        initial_mg: Initial caffeine amount
        remaining_mg: Measured remaining amount
        hours_elapsed: Time passed
        
    Returns:
        Estimated half-life in hours
    """
    if remaining_mg <= 0 or remaining_mg >= initial_mg or hours_elapsed <= 0:
        raise ValueError("Invalid data for half-life calculation")
    
    # remaining = initial * e^(-k*t)
    # ln(remaining/initial) = -k*t
    # k = -ln(remaining/initial) / t
    # half_life = ln(2) / k
    
    k = -math.log(remaining_mg / initial_mg) / hours_elapsed
    return math.log(2) / k


def estimate_caffeine_sensitivity(
    sleep_quality_after_coffee: str,
    hours_between_coffee_and_bed: float
) -> Dict[str, any]:
    """
    Estimate caffeine sensitivity based on reported effects.
    
    Args:
        sleep_quality_after_coffee: "poor", "moderate", or "good"
        hours_between_coffee_and_bed: Hours between last coffee and bedtime
        
    Returns:
        Dict with sensitivity assessment
    """
    sensitivity_map = {
        "poor": {
            "estimated_half_life": 7.0,
            "sensitivity": "high",
            "recommendation": "Avoid caffeine 8+ hours before bed"
        },
        "moderate": {
            "estimated_half_life": 5.5,
            "sensitivity": "moderate",
            "recommendation": "Avoid caffeine 6+ hours before bed"
        },
        "good": {
            "estimated_half_life": 4.0,
            "sensitivity": "low",
            "recommendation": "Avoid caffeine 4+ hours before bed"
        }
    }
    
    result = sensitivity_map.get(sleep_quality_after_coffee.lower(), {
        "estimated_half_life": 5.0,
        "sensitivity": "unknown",
        "recommendation": "Monitor your response to caffeine"
    })
    
    result["hours_before_bed"] = hours_between_coffee_and_bed
    result["input_sleep_quality"] = sleep_quality_after_coffee
    
    return result


def caffeine_equivalent(
    amount_mg: float,
    as_beverage: str = "drip_coffee_medium"
) -> Dict[str, any]:
    """
    Express a caffeine amount in terms of a reference beverage.
    
    Args:
        amount_mg: Caffeine amount in mg
        as_beverage: Reference beverage key
        
    Returns:
        Dict with equivalent information
    """
    if as_beverage not in BEVERAGE_DATABASE:
        as_beverage = "drip_coffee_medium"
    
    ref_amount = BEVERAGE_DATABASE[as_beverage]
    equivalents = amount_mg / ref_amount
    
    # Find closest beverages
    sorted_beverages = sorted(
        BEVERAGE_DATABASE.items(),
        key=lambda x: abs(x[1] - amount_mg)
    )[:5]
    
    return {
        "input_mg": amount_mg,
        "reference_beverage": as_beverage,
        "reference_caffeine_mg": ref_amount,
        "equivalent_units": round(equivalents, 2),
        "closest_beverages": [
            {"name": k, "caffeine_mg": v, "difference_mg": abs(v - amount_mg)}
            for k, v in sorted_beverages
        ]
    }