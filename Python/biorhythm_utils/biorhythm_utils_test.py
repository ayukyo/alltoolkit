#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Biorhythm Utilities Test Module
=============================================
Comprehensive tests for biorhythm_utils module.

Tests:
    - Core calculation functions
    - Biorhythm value generation
    - Critical and peak day finding
    - Chart generation
    - Compatibility analysis
    - Batch analysis
    - Summary generation
    - Chinese zodiac integration
"""

import unittest
from datetime import date, timedelta
import math
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    # Constants
    PHYSICAL_PERIOD, EMOTIONAL_PERIOD, INTELLECTUAL_PERIOD,
    CycleType, CYCLE_CONFIGS,
    
    # Data classes
    BiorhythmValue, BiorhythmResult, CriticalDay, PeakDay,
    
    # Core functions
    calculate_days_alive,
    calculate_biorhythm,
    calculate_phase,
    calculate_days_in_cycle,
    get_biorhythm_value,
    calculate_biorhythms,
    
    # Analysis functions
    find_critical_days,
    find_peak_days,
    
    # Chart
    generate_ascii_chart,
    
    # Compatibility
    calculate_compatibility,
    
    # Batch
    analyze_date_range,
    get_best_days,
    
    # Summary
    get_daily_summary,
    generate_value_bar,
    
    # Zodiac
    get_chinese_zodiac,
    get_full_profile,
)


class TestCoreCalculations(unittest.TestCase):
    """Test core biorhythm calculation functions."""
    
    def test_calculate_days_alive(self):
        """Test days alive calculation."""
        # Same day
        self.assertEqual(
            calculate_days_alive(date(1990, 1, 1), date(1990, 1, 1)),
            0
        )
        
        # 10 days later
        self.assertEqual(
            calculate_days_alive(date(1990, 1, 1), date(1990, 1, 11)),
            10
        )
        
        # Default to today
        days = calculate_days_alive(date(1990, 1, 1))
        self.assertGreater(days, 0)
    
    def test_calculate_biorhythm(self):
        """Test biorhythm value calculation."""
        # Birth day should be 0
        self.assertAlmostEqual(calculate_biorhythm(0, 23), 0.0, places=2)
        
        # After one complete cycle, should return to 0
        self.assertAlmostEqual(calculate_biorhythm(23, 23), 0.0, places=2)
        self.assertAlmostEqual(calculate_biorhythm(28, 28), 0.0, places=2)
        self.assertAlmostEqual(calculate_biorhythm(33, 33), 0.0, places=2)
        
        # Quarter cycle should be near peak (~100)
        # Physical: 23 days, quarter = 5.75 -> peak at day 5.75
        # Day 6 is slightly past peak
        self.assertGreater(calculate_biorhythm(6, 23), 99.0)
        
        # Three-quarter cycle should be near low (~-100)
        # Physical: 23 days, 3/4 = 17.25 -> low at day 17.25
        self.assertLess(calculate_biorhythm(17, 23), -99.0)
        
        # Value range should be -100 to 100
        for period in [23, 28, 33, 38, 43, 48, 53]:
            for days in range(0, 100):
                value = calculate_biorhythm(days, period)
                self.assertGreaterEqual(value, -100)
                self.assertLessEqual(value, 100)
    
    def test_calculate_biorhythm_invalid_period(self):
        """Test biorhythm calculation with invalid period."""
        with self.assertRaises(ValueError):
            calculate_biorhythm(100, 0)
        
        with self.assertRaises(ValueError):
            calculate_biorhythm(100, -1)
    
    def test_calculate_phase(self):
        """Test phase calculation."""
        # Birth day should be phase 0
        self.assertAlmostEqual(calculate_phase(0, 23), 0.0, places=2)
        
        # After one complete cycle (day = period), we're at day 0 of next cycle
        # So phase is 0 (new cycle start)
        self.assertAlmostEqual(calculate_phase(23, 23), 0.0, places=2)
        
        # Half cycle should be phase ~180
        half_phase = calculate_phase(11, 23)
        self.assertGreater(half_phase, 170)
        self.assertLess(half_phase, 190)
        
        # Day 22 should be near phase 360 (end of cycle)
        end_phase = calculate_phase(22, 23)
        self.assertGreater(end_phase, 340)
    
    def test_calculate_days_in_cycle(self):
        """Test days in cycle calculation."""
        # Day 30 in 23-day cycle
        self.assertEqual(calculate_days_in_cycle(30, 23), 7)
        
        # Day 23 in 23-day cycle (exactly one cycle)
        self.assertEqual(calculate_days_in_cycle(23, 23), 0)
        
        # Day 0 in any cycle
        self.assertEqual(calculate_days_in_cycle(0, 23), 0)


class TestBiorhythmValue(unittest.TestCase):
    """Test BiorhythmValue generation."""
    
    def test_get_biorhythm_value(self):
        """Test complete biorhythm value generation."""
        # Birth day - critical (zero)
        value = get_biorhythm_value(CycleType.PHYSICAL, 0)
        self.assertEqual(value.cycle_type, CycleType.PHYSICAL)
        self.assertAlmostEqual(value.value, 0.0, places=2)
        self.assertTrue(value.is_critical)
        self.assertFalse(value.is_peak)
        self.assertFalse(value.is_low)
        self.assertEqual(value.state, "critical")
        
        # Peak day (near quarter cycle - day 6 for 23-day cycle is ~99.77)
        value = get_biorhythm_value(CycleType.PHYSICAL, 6)
        self.assertGreater(value.value, 99.0)
        self.assertTrue(value.is_peak)
        self.assertEqual(value.state, "high")
        
        # Low day (near three-quarter cycle - day 17 for 23-day cycle is ~-99.77)
        value = get_biorhythm_value(CycleType.PHYSICAL, 17)
        self.assertLess(value.value, -99.0)
        self.assertTrue(value.is_low)
        self.assertEqual(value.state, "low")
        
        # Normal day
        value = get_biorhythm_value(CycleType.PHYSICAL, 10)
        self.assertGreater(value.value, 0)
        self.assertLess(value.value, 100)
        self.assertFalse(value.is_critical)
        self.assertFalse(value.is_peak)
        self.assertFalse(value.is_low)
    
    def test_all_cycle_types(self):
        """Test all cycle types."""
        for cycle_type in CycleType:
            value = get_biorhythm_value(cycle_type, 100)
            self.assertEqual(value.cycle_type, cycle_type)
            config = CYCLE_CONFIGS[cycle_type]
            self.assertEqual(value.days_in_cycle, 100 % config["period"])


class TestBiorhythmResult(unittest.TestCase):
    """Test complete biorhythm calculation."""
    
    def test_calculate_biorhythms_basic(self):
        """Test basic biorhythm calculation."""
        birth = date(1990, 1, 1)
        target = date(1990, 1, 11)  # 10 days later
        
        result = calculate_biorhythms(birth, target)
        
        self.assertEqual(result.birth_date, birth)
        self.assertEqual(result.target_date, target)
        self.assertEqual(result.days_alive, 10)
        
        # Should have 3 primary cycles
        self.assertEqual(len(result.primary_cycles), 3)
        self.assertIn(CycleType.PHYSICAL, result.primary_cycles)
        self.assertIn(CycleType.EMOTIONAL, result.primary_cycles)
        self.assertIn(CycleType.INTELLECTUAL, result.primary_cycles)
        
        # Should not have secondary cycles by default
        self.assertEqual(len(result.secondary_cycles), 0)
        
        # Overall energy should be average
        avg = sum(v.value for v in result.primary_cycles.values()) / 3
        self.assertAlmostEqual(result.overall_energy, avg, places=2)
    
    def test_calculate_biorhythms_with_secondary(self):
        """Test biorhythm with secondary cycles."""
        birth = date(1990, 1, 1)
        target = date(1990, 1, 11)
        
        result = calculate_biorhythms(birth, target, include_secondary=True)
        
        # Should have 4 secondary cycles
        self.assertEqual(len(result.secondary_cycles), 4)
        self.assertIn(CycleType.INTUITIVE, result.secondary_cycles)
        self.assertIn(CycleType.AESTHETIC, result.secondary_cycles)
        self.assertIn(CycleType.AWARENESS, result.secondary_cycles)
        self.assertIn(CycleType.SPIRITUAL, result.secondary_cycles)
    
    def test_calculate_biorhythms_invalid_dates(self):
        """Test with invalid date order."""
        birth = date(1990, 1, 1)
        target = date(1989, 12, 31)
        
        with self.assertRaises(ValueError):
            calculate_biorhythms(birth, target)
    
    def test_biorhythm_result_methods(self):
        """Test BiorhythmResult helper methods."""
        birth = date(1990, 1, 1)
        target = date(1990, 1, 11)
        
        result = calculate_biorhythms(birth, target, include_secondary=True)
        
        # get_cycle should work for both primary and secondary
        phys = result.get_cycle(CycleType.PHYSICAL)
        self.assertEqual(phys.cycle_type, CycleType.PHYSICAL)
        
        intui = result.get_cycle(CycleType.INTUITIVE)
        self.assertEqual(intui.cycle_type, CycleType.INTUITIVE)
        
        # get_all_cycles should combine both
        all_cycles = result.get_all_cycles()
        self.assertEqual(len(all_cycles), 7)
        
        # get_summary should return a string
        summary = result.get_summary()
        self.assertIsInstance(summary, str)


class TestCriticalAndPeakDays(unittest.TestCase):
    """Test critical and peak day finding."""
    
    def test_find_critical_days(self):
        """Test critical day finding."""
        birth = date(1990, 1, 1)
        start = date(2024, 1, 1)
        
        critical = find_critical_days(birth, start, days=60)
        
        # Should find some critical days
        self.assertGreater(len(critical), 0)
        
        # All critical days should be within range
        for cd in critical:
            self.assertGreaterEqual(cd.date, start)
            self.assertLessEqual(cd.date, start + timedelta(days=60))
            self.assertIn(cd.cycle_type, [CycleType.PHYSICAL, CycleType.EMOTIONAL, CycleType.INTELLECTUAL])
            self.assertIn(cd.direction, ["up", "down"])
    
    def test_find_peak_days(self):
        """Test peak day finding."""
        birth = date(1990, 1, 1)
        start = date(2024, 1, 1)
        
        peaks = find_peak_days(birth, start, days=60)
        
        # Should find some peak/low days
        self.assertGreater(len(peaks), 0)
        
        # All peak days should be within range
        for pd in peaks:
            self.assertGreaterEqual(pd.date, start)
            self.assertLessEqual(pd.date, start + timedelta(days=60))
            
            if pd.is_peak:
                self.assertEqual(pd.value, 100.0)
            else:
                self.assertEqual(pd.value, -100.0)
    
    def test_find_critical_days_specific_cycle(self):
        """Test finding critical days for specific cycle."""
        birth = date(1990, 1, 1)
        start = date(2024, 1, 1)
        
        # Only physical cycle
        critical = find_critical_days(birth, start, days=60, cycle_types=[CycleType.PHYSICAL])
        
        for cd in critical:
            self.assertEqual(cd.cycle_type, CycleType.PHYSICAL)


class TestCompatibility(unittest.TestCase):
    """Test compatibility analysis."""
    
    def test_calculate_compatibility(self):
        """Test basic compatibility calculation."""
        birth1 = date(1990, 1, 1)
        birth2 = date(1992, 6, 15)
        
        compat = calculate_compatibility(birth1, birth2)
        
        # Should have all scores
        self.assertIn("physical", compat)
        self.assertIn("emotional", compat)
        self.assertIn("intellectual", compat)
        self.assertIn("overall", compat)
        self.assertIn("interpretation", compat)
        
        # Scores should be 0-100
        for key in ["physical", "emotional", "intellectual", "overall"]:
            self.assertGreaterEqual(compat[key], 0)
            self.assertLessEqual(compat[key], 100)
        
        # Interpretation should be a string
        self.assertIsInstance(compat["interpretation"], str)
    
    def test_same_birth_date(self):
        """Test compatibility with same birth date."""
        birth = date(1990, 1, 1)
        
        compat = calculate_compatibility(birth, birth)
        
        # Should have high compatibility (identical cycles)
        self.assertGreater(compat["overall"], 80)


class TestBatchAnalysis(unittest.TestCase):
    """Test batch analysis functions."""
    
    def test_analyze_date_range(self):
        """Test date range analysis."""
        birth = date(1990, 1, 1)
        start = date(2024, 1, 1)
        end = date(2024, 1, 5)
        
        results = analyze_date_range(birth, start, end)
        
        # Should have 5 results
        self.assertEqual(len(results), 5)
        
        # Each result should be valid
        for result in results:
            self.assertEqual(result.birth_date, birth)
        
        # Dates should be consecutive
        for i, result in enumerate(results):
            self.assertEqual(result.target_date, start + timedelta(days=i))
    
    def test_analyze_date_range_invalid(self):
        """Test with invalid date range."""
        birth = date(1990, 1, 1)
        start = date(2024, 1, 10)
        end = date(2024, 1, 1)  # End before start
        
        with self.assertRaises(ValueError):
            analyze_date_range(birth, start, end)
    
    def test_get_best_days(self):
        """Test finding best days."""
        birth = date(1990, 1, 1)
        start = date(2024, 1, 1)
        
        best = get_best_days(birth, start, days=60, cycle_type=CycleType.PHYSICAL, top_n=5)
        
        # Should have 5 results
        self.assertEqual(len(best), 5)
        
        # Values should be in descending order
        for i in range(len(best) - 1):
            self.assertGreaterEqual(best[i][1], best[i+1][1])
        
        # All dates should be within range
        for d, v in best:
            self.assertGreaterEqual(d, start)
            self.assertLessEqual(d, start + timedelta(days=60))


class TestChartGeneration(unittest.TestCase):
    """Test ASCII chart generation."""
    
    def test_generate_ascii_chart(self):
        """Test chart generation."""
        birth = date(1990, 1, 1)
        start = date(2024, 1, 1)
        
        chart = generate_ascii_chart(birth, start, days=30)
        
        # Should be a string
        self.assertIsInstance(chart, str)
        
        # Should contain key elements
        self.assertIn("生物节律图表", chart)
        self.assertIn("P=体力", chart)
        self.assertIn("E=情绪", chart)
        self.assertIn("I=智力", chart)
    
    def test_generate_value_bar(self):
        """Test value bar generation."""
        # Zero value
        bar = generate_value_bar(0, width=20)
        self.assertIn("│", bar)
        
        # High value
        bar = generate_value_bar(100, width=20)
        self.assertIn("▓", bar)
        
        # Low value
        bar = generate_value_bar(-100, width=20)
        self.assertIn("▓", bar)


class TestSummaryGeneration(unittest.TestCase):
    """Test summary generation."""
    
    def test_get_daily_summary(self):
        """Test daily summary generation."""
        birth = date(1990, 1, 1)
        target = date(2024, 1, 15)
        
        summary = get_daily_summary(birth, target)
        
        # Should be a string
        self.assertIsInstance(summary, str)
        
        # Should contain key elements
        self.assertIn("生物节律日报", summary)
        self.assertIn("体力", summary)
        self.assertIn("情绪", summary)
        self.assertIn("智力", summary)


class TestChineseZodiac(unittest.TestCase):
    """Test Chinese zodiac integration."""
    
    def test_get_chinese_zodiac(self):
        """Test zodiac calculation."""
        # 1990 should be Horse (庚午年)
        zodiac = get_chinese_zodiac(date(1990, 1, 1))
        self.assertEqual(zodiac["animal_cn"], "马")
        
        # 2000 should be Dragon (庚辰年)
        zodiac = get_chinese_zodiac(date(2000, 1, 1))
        self.assertEqual(zodiac["animal_cn"], "龙")
        
        # 1984 should be Rat (甲子年)
        zodiac = get_chinese_zodiac(date(1984, 1, 1))
        self.assertEqual(zodiac["animal_cn"], "鼠")
        
        # 1980 should be Monkey
        zodiac = get_chinese_zodiac(date(1980, 1, 1))
        self.assertEqual(zodiac["animal_cn"], "猴")
    
    def test_zodiac_structure(self):
        """Test zodiac result structure."""
        zodiac = get_chinese_zodiac(date(1990, 1, 1))
        
        self.assertIn("animal_cn", zodiac)
        self.assertIn("animal_en", zodiac)
        self.assertIn("earthly_branch", zodiac)
        self.assertIn("element", zodiac)
        self.assertIn("description", zodiac)


class TestFullProfile(unittest.TestCase):
    """Test full profile generation."""
    
    def test_get_full_profile(self):
        """Test complete profile generation."""
        birth = date(1990, 6, 15)
        
        profile = get_full_profile(birth)
        
        # Should have all components
        self.assertIn("birth_date", profile)
        self.assertIn("target_date", profile)
        self.assertIn("days_alive", profile)
        self.assertIn("age_years", profile)
        self.assertIn("zodiac", profile)
        self.assertIn("primary_cycles", profile)
        self.assertIn("secondary_cycles", profile)
        self.assertIn("overall_energy", profile)
        self.assertIn("upcoming_critical_days", profile)
        self.assertIn("upcoming_peak_days", profile)
        
        # Age should be reasonable
        self.assertGreater(profile["age_years"], 0)


class TestCycleConfigs(unittest.TestCase):
    """Test cycle configuration."""
    
    def test_cycle_configs_complete(self):
        """Test all cycle configs have required fields."""
        for cycle_type in CycleType:
            config = CYCLE_CONFIGS[cycle_type]
            
            self.assertIn("period", config)
            self.assertIn("name", config)
            self.assertIn("name_en", config)
            self.assertIn("description", config)
            
            # Period should be positive
            self.assertGreater(config["period"], 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)