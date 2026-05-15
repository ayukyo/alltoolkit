"""
Circadian Rhythm Utils - A utility for calculating optimal sleep/wake times,
biological rhythms, and energy patterns throughout the day.

Zero external dependencies - uses only Python standard library.
"""

from datetime import datetime, timedelta, time
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass
from enum import Enum
import math


class Chronotype(Enum):
    """Sleep chronotype classification."""
    EXTREME_LARK = "extreme_lark"      # Very early riser (4-5 AM)
    LARK = "lark"                       # Early riser (6-7 AM)
    INTERMEDIATE = "intermediate"       # Average (7-8 AM)
    OWL = "owl"                         # Late riser (8-9 AM)
    EXTREME_OWL = "extreme_owl"        # Very late riser (10+ AM)


class AlertnessLevel(Enum):
    """Energy/alertness levels throughout the day."""
    VERY_LOW = 1
    LOW = 2
    MODERATE = 3
    HIGH = 4
    PEAK = 5


@dataclass
class CircadianPhase:
    """Represents a phase in the circadian cycle."""
    name: str
    start_hour: float
    end_hour: float
    description: str
    alertness: AlertnessLevel


@dataclass
class SleepWindow:
    """Represents an optimal sleep window."""
    bedtime: datetime
    wake_time: datetime
    duration_hours: float
    quality_score: float  # 0-100
    rem_cycles: int


@dataclass
class ActivityRecommendation:
    """Activity recommendation for a specific time."""
    time: datetime
    activity: str
    reason: str
    priority: int  # 1-5, 5 being highest


class CircadianRhythmCalculator:
    """
    Main calculator for circadian rhythm analysis.
    
    Based on established circadian science principles:
    - Core body temperature rhythm
    - Melatonin production cycles
    - Sleep architecture (90-min REM cycles)
    - Chronotype variations
    """
    
    # Base circadian rhythm phases (for intermediate chronotype)
    BASE_PHASES = [
        CircadianPhase("Sleep", 0, 6, "Deep sleep period", AlertnessLevel.VERY_LOW),
        CircadianPhase("Wake Transition", 6, 7, "Melatonin decreasing, cortisol rising", AlertnessLevel.LOW),
        CircadianPhase("Morning Alert", 7, 9, "Peak morning alertness", AlertnessLevel.HIGH),
        CircadianPhase("Peak Performance", 9, 12, "Best cognitive performance window", AlertnessLevel.PEAK),
        CircadianPhase("Post-Lunch Dip", 12, 14, "Natural energy dip after lunch", AlertnessLevel.LOW),
        CircadianPhase("Afternoon Recovery", 14, 17, "Gradual energy recovery", AlertnessLevel.MODERATE),
        CircadianPhase("Evening Peak", 17, 20, "Second alertness peak", AlertnessLevel.HIGH),
        CircadianPhase("Wind Down", 20, 22, "Melatonin production begins", AlertnessLevel.MODERATE),
        CircadianPhase("Pre-Sleep", 22, 24, "Sleep pressure building", AlertnessLevel.LOW),
    ]
    
    # Chronotype hour offsets from base phases
    CHRONOTYPE_OFFSETS = {
        Chronotype.EXTREME_LARK: -2,
        Chronotype.LARK: -1,
        Chronotype.INTERMEDIATE: 0,
        Chronotype.OWL: 1,
        Chronotype.EXTREME_OWL: 2,
    }
    
    REM_CYCLE_DURATION = 1.5  # hours (90 minutes)
    
    def __init__(self, chronotype: Chronotype = Chronotype.INTERMEDIATE, age: int = 30):
        """
        Initialize the calculator.
        
        Args:
            chronotype: The person's sleep chronotype
            age: Age affects sleep duration needs and rhythm flexibility
        """
        self.chronotype = chronotype
        self.age = age
        self._phases = self._adjust_phases_for_chronotype()
    
    def _adjust_phases_for_chronotype(self) -> List[CircadianPhase]:
        """Adjust base phases based on chronotype."""
        offset = self.CHRONOTYPE_OFFSETS[self.chronotype]
        adjusted = []
        
        for phase in self.BASE_PHASES:
            new_start = (phase.start_hour + offset) % 24
            new_end = (phase.end_hour + offset) % 24
            adjusted.append(CircadianPhase(
                name=phase.name,
                start_hour=new_start,
                end_hour=new_end,
                description=phase.description,
                alertness=phase.alertness
            ))
        
        return adjusted
    
    def get_recommended_sleep_duration(self) -> float:
        """
        Get recommended sleep duration based on age.
        
        Returns:
            Recommended hours of sleep per night.
        """
        if self.age < 1:
            return 14
        elif self.age < 3:
            return 12
        elif self.age < 6:
            return 10
        elif self.age < 13:
            return 9
        elif self.age < 18:
            return 8.5
        elif self.age < 65:
            return 7.5
        else:
            return 8
    
    def get_current_phase(self, at_time: Optional[datetime] = None) -> CircadianPhase:
        """
        Get the current circadian phase.
        
        Args:
            at_time: Time to check (defaults to now)
            
        Returns:
            Current circadian phase.
        """
        if at_time is None:
            at_time = datetime.now()
        
        hour = at_time.hour + at_time.minute / 60
        
        for phase in self._phases:
            if phase.start_hour <= phase.end_hour:
                if phase.start_hour <= hour < phase.end_hour:
                    return phase
            else:  # Phase spans midnight
                if hour >= phase.start_hour or hour < phase.end_hour:
                    return phase
        
        return self._phases[0]  # Default to first phase
    
    def get_alertness_at_time(self, at_time: Optional[datetime] = None) -> Tuple[AlertnessLevel, float]:
        """
        Calculate alertness level at a specific time.
        
        Uses a sinusoidal model based on core body temperature rhythm.
        
        Args:
            at_time: Time to check (defaults to now)
            
        Returns:
            Tuple of (AlertnessLevel, raw_score 0-100)
        """
        if at_time is None:
            at_time = datetime.now()
        
        hour = at_time.hour + at_time.minute / 60
        
        # Adjust for chronotype offset
        offset = self.CHRONOTYPE_OFFSETS[self.chronotype]
        adjusted_hour = (hour - offset) % 24
        
        # Circadian alertness model (sinusoidal)
        # Peak at ~10 AM (after morning cortisol surge)
        # Trough at ~3 AM (deepest sleep)
        # Peak around 6 PM (evening alertness)
        
        # Primary circadian component
        primary = 50 + 25 * math.sin(2 * math.pi * (adjusted_hour - 6) / 24)
        
        # Secondary evening peak
        evening_bonus = 10 * math.sin(2 * math.pi * (adjusted_hour - 16) / 12)
        evening_bonus = max(0, evening_bonus)
        
        # Sleep pressure component (builds throughout wake period)
        sleep_pressure = 0
        if 6 <= adjusted_hour <= 22:  # Awake hours
            sleep_pressure = -5 * math.sin(2 * math.pi * (adjusted_hour - 6) / 16)
        
        raw_score = primary + evening_bonus + sleep_pressure
        raw_score = max(0, min(100, raw_score))
        
        if raw_score >= 85:
            level = AlertnessLevel.PEAK
        elif raw_score >= 70:
            level = AlertnessLevel.HIGH
        elif raw_score >= 50:
            level = AlertnessLevel.MODERATE
        elif raw_score >= 30:
            level = AlertnessLevel.LOW
        else:
            level = AlertnessLevel.VERY_LOW
        
        return level, raw_score
    
    def calculate_optimal_wake_time(self, bedtime: datetime) -> List[SleepWindow]:
        """
        Calculate optimal wake times for a given bedtime.
        
        Based on 90-minute REM cycles. Waking at the end of a cycle
        results in feeling more refreshed.
        
        Args:
            bedtime: The time you go to bed
            
        Returns:
            List of possible wake windows, sorted by quality score.
        """
        windows = []
        sleep_duration = self.get_recommended_sleep_duration()
        
        # Allow 15 minutes to fall asleep
        actual_sleep_start = bedtime + timedelta(minutes=15)
        
        # Generate windows for 4-7 REM cycles
        for cycles in range(4, 8):
            duration_hours = cycles * self.REM_CYCLE_DURATION
            wake_time = actual_sleep_start + timedelta(hours=duration_hours)
            
            # Quality scoring based on multiple factors
            quality = self._calculate_sleep_quality(bedtime, wake_time, duration_hours)
            
            windows.append(SleepWindow(
                bedtime=bedtime,
                wake_time=wake_time,
                duration_hours=duration_hours,
                quality_score=quality,
                rem_cycles=cycles
            ))
        
        return sorted(windows, key=lambda w: w.quality_score, reverse=True)
    
    def calculate_optimal_bedtime(self, wake_time: datetime) -> List[SleepWindow]:
        """
        Calculate optimal bedtimes for a target wake time.
        
        Works backwards from wake time to find bedtimes that align
        with REM cycle endings.
        
        Args:
            wake_time: Target wake time
            
        Returns:
            List of possible sleep windows, sorted by quality score.
        """
        windows = []
        
        # Generate windows for 4-7 REM cycles
        for cycles in range(4, 8):
            duration_hours = cycles * self.REM_CYCLE_DURATION
            # Add 15 minutes for falling asleep
            bedtime = wake_time - timedelta(hours=duration_hours, minutes=15)
            
            quality = self._calculate_sleep_quality(bedtime, wake_time, duration_hours)
            
            windows.append(SleepWindow(
                bedtime=bedtime,
                wake_time=wake_time,
                duration_hours=duration_hours,
                quality_score=quality,
                rem_cycles=cycles
            ))
        
        return sorted(windows, key=lambda w: w.quality_score, reverse=True)
    
    def _calculate_sleep_quality(self, bedtime: datetime, wake_time: datetime, 
                                  duration_hours: float) -> float:
        """
        Calculate sleep quality score for a window.
        
        Factors:
        - Duration (optimal range)
        - Bedtime alignment with circadian rhythm
        - Wake time alertness
        """
        score = 50  # Base score
        
        # Duration bonus (optimal is 7-9 hours for adults)
        recommended = self.get_recommended_sleep_duration()
        duration_diff = abs(duration_hours - recommended)
        if duration_diff <= 0.5:
            score += 20
        elif duration_diff <= 1:
            score += 15
        elif duration_diff <= 1.5:
            score += 10
        elif duration_diff <= 2:
            score += 5
        
        # Bedtime alignment (circadian preferred times)
        bed_hour = bedtime.hour + bedtime.minute / 60
        offset = self.CHRONOTYPE_OFFSETS[self.chronotype]
        optimal_bed_start = 22 - offset  # 10 PM for intermediate
        optimal_bed_end = 24 - offset    # 12 AM for intermediate
        
        if optimal_bed_start <= bed_hour < optimal_bed_end or bed_hour >= optimal_bed_start:
            score += 15
        elif bed_hour >= optimal_bed_start - 1 or bed_hour < (optimal_bed_end + 2) % 24:
            score += 10
        else:
            score -= 5
        
        # Wake time alertness
        _, wake_alertness = self.get_alertness_at_time(wake_time)
        score += (wake_alertness - 50) * 0.3
        
        return max(0, min(100, score))
    
    def get_activity_recommendations(self, date: Optional[datetime] = None) -> List[ActivityRecommendation]:
        """
        Get activity recommendations for a day.
        
        Args:
            date: The date to generate recommendations for (defaults to today)
            
        Returns:
            List of activity recommendations throughout the day.
        """
        if date is None:
            date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        recommendations = []
        offset = self.CHRONOTYPE_OFFSETS[self.chronotype]
        
        # Morning exercise
        rec_time = date + timedelta(hours=7 - offset)
        recommendations.append(ActivityRecommendation(
            time=rec_time,
            activity="Light Exercise",
            reason="Cortisol levels rising, good for cardio and flexibility",
            priority=4
        ))
        
        # Deep work session 1
        rec_time = date + timedelta(hours=9 - offset)
        recommendations.append(ActivityRecommendation(
            time=rec_time,
            activity="Deep Work",
            reason="Peak cognitive performance window",
            priority=5
        ))
        
        # Creative work
        rec_time = date + timedelta(hours=11 - offset)
        recommendations.append(ActivityRecommendation(
            time=rec_time,
            activity="Creative Work",
            reason="High alertness, good for brainstorming",
            priority=4
        ))
        
        # Lunch break
        rec_time = date + timedelta(hours=12.5 - offset)
        recommendations.append(ActivityRecommendation(
            time=rec_time,
            activity="Lunch Break",
            reason="Natural energy dip approaching",
            priority=3
        ))
        
        # Power nap window
        rec_time = date + timedelta(hours=13.5 - offset)
        recommendations.append(ActivityRecommendation(
            time=rec_time,
            activity="Power Nap (10-20 min)",
            reason="Post-lunch dip, ideal nap window",
            priority=3
        ))
        
        # Administrative tasks
        rec_time = date + timedelta(hours=14.5 - offset)
        recommendations.append(ActivityRecommendation(
            time=rec_time,
            activity="Administrative Tasks",
            reason="Energy recovering, good for routine work",
            priority=3
        ))
        
        # Physical exercise
        rec_time = date + timedelta(hours=17 - offset)
        recommendations.append(ActivityRecommendation(
            time=rec_time,
            activity="Intense Exercise",
            reason="Peak physical performance, body temp high",
            priority=5
        ))
        
        # Social activities
        rec_time = date + timedelta(hours=19 - offset)
        recommendations.append(ActivityRecommendation(
            time=rec_time,
            activity="Social Activities",
            reason="Evening alertness peak, good mood",
            priority=4
        ))
        
        # Wind down
        rec_time = date + timedelta(hours=21 - offset)
        recommendations.append(ActivityRecommendation(
            time=rec_time,
            activity="Wind Down",
            reason="Melatonin production beginning",
            priority=4
        ))
        
        # Sleep preparation
        rec_time = date + timedelta(hours=22 - offset)
        recommendations.append(ActivityRecommendation(
            time=rec_time,
            activity="Sleep Preparation",
            reason="Blue light reduction, relax activities",
            priority=5
        ))
        
        return sorted(recommendations, key=lambda r: r.time)
    
    def get_melatonin_schedule(self, date: Optional[datetime] = None) -> Dict[str, Tuple[datetime, datetime]]:
        """
        Get the melatonin production schedule.
        
        Args:
            date: The date to calculate for (defaults to today)
            
        Returns:
            Dictionary with melatonin phase times.
        """
        if date is None:
            date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        offset = self.CHRONOTYPE_OFFSETS[self.chronotype]
        
        # Melatonin rise starts ~2 hours before natural bedtime
        rise_start = date + timedelta(hours=20 - offset)
        peak_start = date + timedelta(hours=22 - offset)
        
        # Melatonin drops ~2 hours after wake time
        decline_start = date + timedelta(hours=8 - offset)
        baseline_start = date + timedelta(hours=10 - offset)
        
        return {
            "production_start": (rise_start, peak_start),
            "peak_production": (peak_start, decline_start),
            "decline_phase": (decline_start, baseline_start),
            "baseline": (baseline_start, rise_start + timedelta(days=1))
        }
    
    def get_daily_alertness_curve(self, date: Optional[datetime] = None) -> List[Tuple[datetime, float]]:
        """
        Generate a 24-hour alertness curve.
        
        Args:
            date: The date to start from (defaults to today)
            
        Returns:
            List of (datetime, alertness_score) tuples for every 30 minutes.
        """
        if date is None:
            date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        curve = []
        for minutes in range(0, 24 * 60, 30):  # Every 30 minutes
            t = date + timedelta(minutes=minutes)
            _, score = self.get_alertness_at_time(t)
            curve.append((t, score))
        
        return curve
    
    def get_sleep_debt_impact(self, hours_slept: float) -> Dict[str, float]:
        """
        Calculate the impact of sleep debt on various functions.
        
        Args:
            hours_slept: Hours slept the previous night
            
        Returns:
            Dictionary of impairment percentages for various functions.
        """
        recommended = self.get_recommended_sleep_duration()
        debt = recommended - hours_slept
        
        if debt <= 0:
            return {
                "cognitive_performance": 100,
                "reaction_time": 100,
                "memory_consolidation": 100,
                "emotional_regulation": 100,
                "immune_function": 100,
                "metabolic_efficiency": 100,
                "overall": 100
            }
        
        # Impairment increases non-linearly with sleep debt
        debt_factor = min(debt / recommended, 0.5)  # Cap at 50% debt
        
        return {
            "cognitive_performance": 100 - (debt_factor * 80),
            "reaction_time": 100 - (debt_factor * 60),
            "memory_consolidation": 100 - (debt_factor * 70),
            "emotional_regulation": 100 - (debt_factor * 50),
            "immune_function": 100 - (debt_factor * 40),
            "metabolic_efficiency": 100 - (debt_factor * 45),
            "overall": 100 - (debt_factor * 55)
        }
    
    def estimate_chronotype(self, preferred_wake_time: time, 
                           preferred_bedtime: time) -> Chronotype:
        """
        Estimate chronotype from sleep preferences.
        
        Args:
            preferred_wake_time: Natural wake time preference
            preferred_bedtime: Natural bedtime preference
            
        Returns:
            Estimated chronotype.
        """
        wake_hour = preferred_wake_time.hour + preferred_wake_time.minute / 60
        
        if wake_hour < 5:
            return Chronotype.EXTREME_LARK
        elif wake_hour < 7:
            return Chronotype.LARK
        elif wake_hour < 8.5:
            return Chronotype.INTERMEDIATE
        elif wake_hour < 10:
            return Chronotype.OWL
        else:
            return Chronotype.EXTREME_OWL
    
    def get_jet_lag_recovery(self, timezone_shift: int) -> Dict[str, any]:
        """
        Estimate jet lag recovery time and recommendations.
        
        Args:
            timezone_shift: Number of time zones crossed (positive = eastward)
            
        Returns:
            Dictionary with recovery estimates and recommendations.
        """
        # Rule of thumb: 1 day per time zone crossed (roughly)
        # Eastward travel is harder than westward
        
        abs_shift = abs(timezone_shift)
        
        if timezone_shift > 0:  # Eastward
            days_to_recover = abs_shift * 0.8  # ~80% of time zones
        else:  # Westward
            days_to_recover = abs_shift * 0.6  # ~60% of time zones
        
        return {
            "timezones_crossed": timezone_shift,
            "direction": "eastward" if timezone_shift > 0 else "westward",
            "estimated_recovery_days": round(days_to_recover, 1),
            "recommendations": [
                f"Adjust sleep schedule by 1 hour per day towards destination time",
                "Get morning sunlight exposure (helps reset circadian clock)",
                "Stay hydrated and avoid alcohol",
                "Consider melatonin supplements (0.5-3mg) at destination bedtime",
                "Avoid heavy meals close to destination bedtime",
                f"Full adjustment expected in {round(days_to_recover)} days"
            ]
        }
    
    def get_nap_recommendation(self, hours_since_sleep: float, 
                               current_energy: int = 5,
                               at_time: Optional[datetime] = None) -> Dict[str, any]:
        """
        Get personalized nap recommendation.
        
        Args:
            hours_since_sleep: Hours since waking up
            current_energy: Current energy level (1-10)
            at_time: Time to evaluate (defaults to now)
            
        Returns:
            Nap recommendation details.
        """
        _, alertness = self.get_alertness_at_time(at_time)
        
        recommendation = {
            "should_nap": False,
            "optimal_duration": 0,
            "timing": None,
            "benefits": [],
            "warnings": []
        }
        
        if current_energy < 4 or alertness < 40:
            recommendation["should_nap"] = True
            recommendation["optimal_duration"] = 20  # Power nap
            recommendation["timing"] = "Now"
            recommendation["benefits"] = [
                "Restore alertness",
                "Improve mood",
                "Enhance cognitive function"
            ]
            recommendation["warnings"] = [
                "Avoid napping after 3 PM (may affect nighttime sleep)",
                "Keep under 30 minutes to avoid sleep inertia"
            ]
        elif hours_since_sleep > 8 and current_energy < 6:
            recommendation["should_nap"] = True
            recommendation["optimal_duration"] = 10
            recommendation["timing"] = "Within the next hour"
            recommendation["benefits"] = [
                "Brief restorative rest",
                "Maintain performance"
            ]
        else:
            recommendation["should_nap"] = False
            recommendation["timing"] = "Not recommended now"
            recommendation["warnings"] = [
                "Current energy levels are adequate",
                "Unnecessary napping may disrupt nighttime sleep"
            ]
        
        return recommendation


def format_time(dt: datetime) -> str:
    """Format datetime as HH:MM."""
    return dt.strftime("%H:%M")


def format_duration(hours: float) -> str:
    """Format duration as 'Xh Ym'."""
    h = int(hours)
    m = int((hours - h) * 60)
    return f"{h}h {m}m"


# Convenience functions for quick usage

def get_best_wake_times(bedtime: datetime, chronotype: Chronotype = Chronotype.INTERMEDIATE) -> List[Dict]:
    """
    Quick function to get best wake times.
    
    Args:
        bedtime: When you go to bed
        chronotype: Your sleep chronotype
        
    Returns:
        List of wake time options with quality scores.
    """
    calc = CircadianRhythmCalculator(chronotype)
    windows = calc.calculate_optimal_wake_time(bedtime)
    
    return [
        {
            "wake_time": format_time(w.wake_time),
            "duration": format_duration(w.duration_hours),
            "quality": round(w.quality_score, 1),
            "rem_cycles": w.rem_cycles
        }
        for w in windows[:3]  # Top 3
    ]


def get_best_bedtimes(wake_time: datetime, chronotype: Chronotype = Chronotype.INTERMEDIATE) -> List[Dict]:
    """
    Quick function to get best bedtimes for a target wake time.
    
    Args:
        wake_time: When you want to wake up
        chronotype: Your sleep chronotype
        
    Returns:
        List of bedtime options with quality scores.
    """
    calc = CircadianRhythmCalculator(chronotype)
    windows = calc.calculate_optimal_bedtime(wake_time)
    
    return [
        {
            "bedtime": format_time(w.bedtime),
            "duration": format_duration(w.duration_hours),
            "quality": round(w.quality_score, 1),
            "rem_cycles": w.rem_cycles
        }
        for w in windows[:3]  # Top 3
    ]


def get_current_alertness(chronotype: Chronotype = Chronotype.INTERMEDIATE) -> Dict:
    """
    Quick function to get current alertness level.
    
    Args:
        chronotype: Your sleep chronotype
        
    Returns:
        Current alertness information.
    """
    calc = CircadianRhythmCalculator(chronotype)
    level, score = calc.get_alertness_at_time()
    phase = calc.get_current_phase()
    
    return {
        "alertness_level": level.name,
        "alertness_score": round(score, 1),
        "current_phase": phase.name,
        "phase_description": phase.description
    }