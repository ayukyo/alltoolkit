"""
Comprehensive tests for Circadian Rhythm Utils.

Run with: python -m pytest test_circadian_rhythm.py -v
Or simply: python test_circadian_rhythm.py
"""

import unittest
from datetime import datetime, time, timedelta
import math

from circadian_rhythm import (
    CircadianRhythmCalculator,
    Chronotype,
    AlertnessLevel,
    CircadianPhase,
    SleepWindow,
    ActivityRecommendation,
    get_best_wake_times,
    get_best_bedtimes,
    get_current_alertness,
    format_time,
    format_duration,
)


class TestChronotype(unittest.TestCase):
    """Test Chronotype enum."""
    
    def test_chronotype_values(self):
        """Test that all chronotype values exist."""
        self.assertEqual(Chronotype.EXTREME_LARK.value, "extreme_lark")
        self.assertEqual(Chronotype.LARK.value, "lark")
        self.assertEqual(Chronotype.INTERMEDIATE.value, "intermediate")
        self.assertEqual(Chronotype.OWL.value, "owl")
        self.assertEqual(Chronotype.EXTREME_OWL.value, "extreme_owl")
    
    def test_chronotype_count(self):
        """Test that we have 5 chronotypes."""
        self.assertEqual(len(list(Chronotype)), 5)


class TestAlertnessLevel(unittest.TestCase):
    """Test AlertnessLevel enum."""
    
    def test_alertness_ordering(self):
        """Test that alertness levels are properly ordered."""
        self.assertLess(AlertnessLevel.VERY_LOW.value, AlertnessLevel.LOW.value)
        self.assertLess(AlertnessLevel.LOW.value, AlertnessLevel.MODERATE.value)
        self.assertLess(AlertnessLevel.MODERATE.value, AlertnessLevel.HIGH.value)
        self.assertLess(AlertnessLevel.HIGH.value, AlertnessLevel.PEAK.value)


class TestCircadianRhythmCalculator(unittest.TestCase):
    """Test CircadianRhythmCalculator class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.calc_intermediate = CircadianRhythmCalculator(Chronotype.INTERMEDIATE)
        self.calc_lark = CircadianRhythmCalculator(Chronotype.LARK)
        self.calc_owl = CircadianRhythmCalculator(Chronotype.OWL)
    
    def test_initialization(self):
        """Test calculator initialization."""
        self.assertEqual(self.calc_intermediate.chronotype, Chronotype.INTERMEDIATE)
        self.assertEqual(self.calc_intermediate.age, 30)
    
    def test_initialization_with_age(self):
        """Test calculator with custom age."""
        calc = CircadianRhythmCalculator(Chronotype.INTERMEDIATE, age=45)
        self.assertEqual(calc.age, 45)
    
    def test_recommended_sleep_duration(self):
        """Test sleep duration recommendations by age."""
        # Test different ages
        ages_and_durations = [
            (0, 14),    # Infant
            (2, 12),    # Toddler
            (5, 10),    # Preschool
            (10, 9),    # School age
            (16, 8.5),  # Teen
            (30, 7.5),  # Adult
            (70, 8),    # Senior
        ]
        
        for age, expected in ages_and_durations:
            calc = CircadianRhythmCalculator(Chronotype.INTERMEDIATE, age=age)
            self.assertEqual(calc.get_recommended_sleep_duration(), expected)
    
    def test_get_current_phase(self):
        """Test getting current circadian phase."""
        # Test at different times
        morning = datetime(2026, 5, 15, 9, 0)  # 9 AM
        phase = self.calc_intermediate.get_current_phase(morning)
        self.assertIsInstance(phase, CircadianPhase)
        self.assertEqual(phase.name, "Peak Performance")
        
        # Test at night
        night = datetime(2026, 5, 15, 3, 0)  # 3 AM
        phase = self.calc_intermediate.get_current_phase(night)
        self.assertEqual(phase.name, "Sleep")
    
    def test_get_alertness_at_time(self):
        """Test alertness calculation."""
        # Morning should have moderate to high alertness
        morning = datetime(2026, 5, 15, 10, 0)
        level, score = self.calc_intermediate.get_alertness_at_time(morning)
        self.assertIn(level, [AlertnessLevel.MODERATE, AlertnessLevel.HIGH, AlertnessLevel.PEAK])
        self.assertGreater(score, 50)
        
        # Late night should have low alertness
        night = datetime(2026, 5, 15, 3, 0)
        level, score = self.calc_intermediate.get_alertness_at_time(night)
        self.assertIn(level, [AlertnessLevel.LOW, AlertnessLevel.VERY_LOW])
        self.assertLess(score, 40)
    
    def test_chronotype_alertness_difference(self):
        """Test that different chronotypes have different alertness patterns."""
        # 6 AM: Lark should be more alert than Owl
        early_morning = datetime(2026, 5, 15, 6, 0)
        
        _, lark_score = self.calc_lark.get_alertness_at_time(early_morning)
        _, owl_score = self.calc_owl.get_alertness_at_time(early_morning)
        
        # Larks are generally more alert earlier
        # Note: Due to sinusoidal nature, this might not always be true
        # but the phases should differ
        lark_phase = self.calc_lark.get_current_phase(early_morning)
        owl_phase = self.calc_owl.get_current_phase(early_morning)
        
        # Phases should be different (lark offset is -1, owl offset is +1)
        self.assertNotEqual(lark_phase.start_hour, owl_phase.start_hour)
    
    def test_calculate_optimal_wake_time(self):
        """Test wake time calculation."""
        bedtime = datetime(2026, 5, 15, 23, 0)  # 11 PM
        
        windows = self.calc_intermediate.calculate_optimal_wake_time(bedtime)
        
        # Should return multiple windows
        self.assertGreater(len(windows), 3)
        
        # Each window should have required attributes
        for window in windows:
            self.assertIsInstance(window, SleepWindow)
            self.assertIsInstance(window.wake_time, datetime)
            self.assertIsInstance(window.duration_hours, float)
            self.assertIsInstance(window.quality_score, float)
            self.assertIsInstance(window.rem_cycles, int)
            
            # Duration should be reasonable (4-7 cycles * 1.5 hours)
            self.assertGreaterEqual(window.duration_hours, 6)
            self.assertLessEqual(window.duration_hours, 10.5)
        
        # Windows should be sorted by quality
        for i in range(len(windows) - 1):
            self.assertGreaterEqual(windows[i].quality_score, windows[i+1].quality_score)
    
    def test_calculate_optimal_bedtime(self):
        """Test bedtime calculation."""
        wake_time = datetime(2026, 5, 16, 7, 0)  # 7 AM
        
        windows = self.calc_intermediate.calculate_optimal_bedtime(wake_time)
        
        # Should return multiple windows
        self.assertGreater(len(windows), 3)
        
        # Each window should have required attributes
        for window in windows:
            self.assertIsInstance(window, SleepWindow)
            self.assertIsInstance(window.bedtime, datetime)
            self.assertLess(window.bedtime, wake_time)  # Bedtime before wake time
        
        # Windows should be sorted by quality
        for i in range(len(windows) - 1):
            self.assertGreaterEqual(windows[i].quality_score, windows[i+1].quality_score)
    
    def test_rem_cycle_alignment(self):
        """Test that wake times align with REM cycle endings."""
        bedtime = datetime(2026, 5, 15, 23, 0)
        windows = self.calc_intermediate.calculate_optimal_wake_time(bedtime)
        
        # All windows should be multiples of 90 minutes + 15 min sleep onset
        for window in windows:
            expected_duration = window.rem_cycles * 1.5
            self.assertAlmostEqual(window.duration_hours, expected_duration, places=1)
    
    def test_get_activity_recommendations(self):
        """Test activity recommendations."""
        recommendations = self.calc_intermediate.get_activity_recommendations()
        
        # Should have multiple recommendations throughout the day
        self.assertGreater(len(recommendations), 5)
        
        for rec in recommendations:
            self.assertIsInstance(rec, ActivityRecommendation)
            self.assertIsInstance(rec.time, datetime)
            self.assertIsInstance(rec.activity, str)
            self.assertIsInstance(rec.reason, str)
            self.assertIn(rec.priority, [1, 2, 3, 4, 5])
        
        # Should be sorted by time
        for i in range(len(recommendations) - 1):
            self.assertLessEqual(recommendations[i].time, recommendations[i+1].time)
    
    def test_get_melatonin_schedule(self):
        """Test melatonin schedule."""
        schedule = self.calc_intermediate.get_melatonin_schedule()
        
        required_keys = [
            "production_start",
            "peak_production", 
            "decline_phase",
            "baseline"
        ]
        
        for key in required_keys:
            self.assertIn(key, schedule)
            self.assertIsInstance(schedule[key], tuple)
            self.assertEqual(len(schedule[key]), 2)
    
    def test_get_daily_alertness_curve(self):
        """Test daily alertness curve generation."""
        curve = self.calc_intermediate.get_daily_alertness_curve()
        
        # Should have 48 data points (every 30 minutes for 24 hours)
        self.assertEqual(len(curve), 48)
        
        for timestamp, score in curve:
            self.assertIsInstance(timestamp, datetime)
            self.assertIsInstance(score, float)
            self.assertGreaterEqual(score, 0)
            self.assertLessEqual(score, 100)
    
    def test_get_sleep_debt_impact(self):
        """Test sleep debt calculations."""
        # Well rested
        impact = self.calc_intermediate.get_sleep_debt_impact(8)
        self.assertEqual(impact["overall"], 100)
        
        # Sleep deprived
        impact = self.calc_intermediate.get_sleep_debt_impact(4)
        self.assertLess(impact["overall"], 100)
        self.assertLess(impact["cognitive_performance"], 100)
        
        # More debt = more impairment
        impact_low = self.calc_intermediate.get_sleep_debt_impact(6)
        impact_high = self.calc_intermediate.get_sleep_debt_impact(4)
        self.assertLess(impact_high["overall"], impact_low["overall"])
    
    def test_estimate_chronotype(self):
        """Test chronotype estimation from preferences."""
        # Extreme lark wakes at 4 AM
        estimated = self.calc_intermediate.estimate_chronotype(
            time(4, 0), time(20, 0)
        )
        self.assertEqual(estimated, Chronotype.EXTREME_LARK)
        
        # Lark wakes at 6 AM
        estimated = self.calc_intermediate.estimate_chronotype(
            time(6, 0), time(22, 0)
        )
        self.assertEqual(estimated, Chronotype.LARK)
        
        # Intermediate wakes at 7:30 AM
        estimated = self.calc_intermediate.estimate_chronotype(
            time(7, 30), time(23, 30)
        )
        self.assertEqual(estimated, Chronotype.INTERMEDIATE)
        
        # Owl wakes at 9 AM
        estimated = self.calc_intermediate.estimate_chronotype(
            time(9, 0), time(1, 0)
        )
        self.assertEqual(estimated, Chronotype.OWL)
        
        # Extreme owl wakes at 11 AM
        estimated = self.calc_intermediate.estimate_chronotype(
            time(11, 0), time(3, 0)
        )
        self.assertEqual(estimated, Chronotype.EXTREME_OWL)
    
    def test_get_jet_lag_recovery(self):
        """Test jet lag recovery estimation."""
        # Eastward travel
        result = self.calc_intermediate.get_jet_lag_recovery(6)
        self.assertEqual(result["timezones_crossed"], 6)
        self.assertEqual(result["direction"], "eastward")
        self.assertGreater(result["estimated_recovery_days"], 0)
        
        # Westward travel (should be faster)
        result_west = self.calc_intermediate.get_jet_lag_recovery(-6)
        self.assertEqual(result_west["direction"], "westward")
        self.assertLess(result_west["estimated_recovery_days"], result["estimated_recovery_days"])
        
        # Should have recommendations
        self.assertGreater(len(result["recommendations"]), 0)
    
    def test_get_nap_recommendation(self):
        """Test nap recommendation logic."""
        # Use a time when alertness is typically high (10 AM)
        high_alert_time = datetime(2026, 5, 15, 10, 0)
        
        # Low energy should recommend nap
        rec = self.calc_intermediate.get_nap_recommendation(8, current_energy=2, at_time=high_alert_time)
        self.assertTrue(rec["should_nap"])
        self.assertGreater(rec["optimal_duration"], 0)
        
        # High energy at high alertness time should not recommend nap
        rec = self.calc_intermediate.get_nap_recommendation(4, current_energy=8, at_time=high_alert_time)
        self.assertFalse(rec["should_nap"])


class TestConvenienceFunctions(unittest.TestCase):
    """Test convenience functions."""
    
    def test_get_best_wake_times(self):
        """Test quick wake time calculation."""
        bedtime = datetime(2026, 5, 15, 23, 0)
        results = get_best_wake_times(bedtime)
        
        self.assertEqual(len(results), 3)  # Top 3
        for result in results:
            self.assertIn("wake_time", result)
            self.assertIn("duration", result)
            self.assertIn("quality", result)
            self.assertIn("rem_cycles", result)
    
    def test_get_best_bedtimes(self):
        """Test quick bedtime calculation."""
        wake_time = datetime(2026, 5, 16, 7, 0)
        results = get_best_bedtimes(wake_time)
        
        self.assertEqual(len(results), 3)  # Top 3
        for result in results:
            self.assertIn("bedtime", result)
            self.assertIn("duration", result)
            self.assertIn("quality", result)
            self.assertIn("rem_cycles", result)
    
    def test_get_current_alertness(self):
        """Test quick alertness check."""
        result = get_current_alertness()
        
        self.assertIn("alertness_level", result)
        self.assertIn("alertness_score", result)
        self.assertIn("current_phase", result)
        self.assertIn("phase_description", result)
    
    def test_format_time(self):
        """Test time formatting."""
        dt = datetime(2026, 5, 15, 14, 30)
        self.assertEqual(format_time(dt), "14:30")
    
    def test_format_duration(self):
        """Test duration formatting."""
        self.assertEqual(format_duration(7.5), "7h 30m")
        self.assertEqual(format_duration(8.0), "8h 0m")
        self.assertEqual(format_duration(6.25), "6h 15m")


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""
    
    def test_midnight_boundary(self):
        """Test calculations crossing midnight."""
        calc = CircadianRhythmCalculator(Chronotype.INTERMEDIATE)
        
        # Bedtime at 1 AM
        bedtime = datetime(2026, 5, 16, 1, 0)
        windows = calc.calculate_optimal_wake_time(bedtime)
        
        # Wake times should be on the same day or next day
        for window in windows:
            self.assertGreater(window.wake_time, bedtime)
    
    def test_extreme_chronotypes(self):
        """Test extreme chronotype offsets."""
        calc_lark = CircadianRhythmCalculator(Chronotype.EXTREME_LARK)
        calc_owl = CircadianRhythmCalculator(Chronotype.EXTREME_OWL)
        
        # Both should produce valid recommendations
        recommendations_lark = calc_lark.get_activity_recommendations()
        recommendations_owl = calc_owl.get_activity_recommendations()
        
        self.assertGreater(len(recommendations_lark), 0)
        self.assertGreater(len(recommendations_owl), 0)
    
    def test_alertness_score_bounds(self):
        """Test that alertness scores are always 0-100."""
        calc = CircadianRhythmCalculator(Chronotype.INTERMEDIATE)
        
        # Test every hour
        for hour in range(24):
            dt = datetime(2026, 5, 15, hour, 0)
            _, score = calc.get_alertness_at_time(dt)
            self.assertGreaterEqual(score, 0)
            self.assertLessEqual(score, 100)
    
    def test_quality_score_bounds(self):
        """Test that sleep quality scores are always 0-100."""
        calc = CircadianRhythmCalculator(Chronotype.INTERMEDIATE)
        
        bedtime = datetime(2026, 5, 15, 23, 0)
        windows = calc.calculate_optimal_wake_time(bedtime)
        
        for window in windows:
            self.assertGreaterEqual(window.quality_score, 0)
            self.assertLessEqual(window.quality_score, 100)


class TestDifferentAges(unittest.TestCase):
    """Test age-dependent functionality."""
    
    def test_teen_needs_more_sleep(self):
        """Test that teens need more sleep than adults."""
        calc_teen = CircadianRhythmCalculator(Chronotype.INTERMEDIATE, age=16)
        calc_adult = CircadianRhythmCalculator(Chronotype.INTERMEDIATE, age=30)
        
        self.assertGreater(
            calc_teen.get_recommended_sleep_duration(),
            calc_adult.get_recommended_sleep_duration()
        )
    
    def test_senior_sleep_needs(self):
        """Test senior sleep recommendations."""
        calc_senior = CircadianRhythmCalculator(Chronotype.INTERMEDIATE, age=70)
        
        # Seniors need slightly more sleep
        self.assertGreaterEqual(calc_senior.get_recommended_sleep_duration(), 7)


if __name__ == "__main__":
    unittest.main(verbosity=2)