"""
Circadian Rhythm Utils - Tools for sleep optimization and biological rhythm analysis.

Quick Start:
    from circadian_rhythm_utils import CircadianRhythmCalculator, Chronotype
    
    # Create calculator for a "night owl"
    calc = CircadianRhythmCalculator(Chronotype.OWL)
    
    # Get best wake times for a bedtime
    windows = calc.calculate_optimal_wake_time(bedtime)
    
    # Get current alertness
    level, score = calc.get_alertness_at_time()
"""

from .circadian_rhythm import (
    # Main classes
    CircadianRhythmCalculator,
    Chronotype,
    AlertnessLevel,
    
    # Data classes
    CircadianPhase,
    SleepWindow,
    ActivityRecommendation,
    
    # Convenience functions
    get_best_wake_times,
    get_best_bedtimes,
    get_current_alertness,
    
    # Utility functions
    format_time,
    format_duration,
)

__version__ = "1.0.0"
__author__ = "AllToolkit"

__all__ = [
    "CircadianRhythmCalculator",
    "Chronotype",
    "AlertnessLevel",
    "CircadianPhase",
    "SleepWindow",
    "ActivityRecommendation",
    "get_best_wake_times",
    "get_best_bedtimes",
    "get_current_alertness",
    "format_time",
    "format_duration",
]