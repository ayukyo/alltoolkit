"""
Tests for Blood Alcohol Content (BAC) Calculator Utils

Comprehensive tests covering all functionality.
"""

import unittest
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bac_utils.mod import (
    Gender, ImpairmentLevel, Drink, BACResult,
    calculate_bac, calculate_bac_from_drinks, get_impairment_level,
    time_to_sober, time_to_legal_limit, calculate_bac_result,
    estimate_alcohol_content, get_legal_limit, list_zero_tolerance_countries,
    format_bac, format_time_hours, calculate_drinks_by_bac, get_bac_warning,
    beer_bac, wine_bac, spirit_bac,
    LEGAL_LIMITS, METABOLISM_RATE_AVG, WIDMARK_MALE, WIDMARK_FEMALE
)


class TestDrinkClass(unittest.TestCase):
    """Test Drink dataclass and factory methods."""
    
    def test_from_standard(self):
        """Test creating a drink from standard units."""
        drink = Drink.from_standard("Beer", units=2.0)
        self.assertEqual(drink.name, "Beer")
        self.assertEqual(drink.alcohol_grams, 20.0)
        self.assertIsNone(drink.consumed_at)
    
    def test_from_beer(self):
        """Test creating a drink from beer specifications."""
        drink = Drink.from_beer(500, abv=5.0)
        # 500ml * 0.05 * 0.789 = 19.725g
        self.assertAlmostEqual(drink.alcohol_grams, 19.725, places=2)
    
    def test_from_wine(self):
        """Test creating a drink from wine specifications."""
        drink = Drink.from_wine(150, abv=12.0)
        # 150ml * 0.12 * 0.789 = 14.202g
        self.assertAlmostEqual(drink.alcohol_grams, 14.202, places=2)
    
    def test_from_spirit(self):
        """Test creating a drink from spirit specifications."""
        drink = Drink.from_spirit(45, abv=40.0)
        # 45ml * 0.40 * 0.789 = 14.202g
        self.assertAlmostEqual(drink.alcohol_grams, 14.202, places=2)
    
    def test_with_timestamp(self):
        """Test creating a drink with timestamp."""
        now = datetime.now()
        drink = Drink.from_standard("Wine", units=1.5, consumed_at=now)
        self.assertEqual(drink.consumed_at, now)


class TestBACCalculation(unittest.TestCase):
    """Test BAC calculation functions."""
    
    def test_calculate_bac_male(self):
        """Test BAC calculation for male."""
        # 70kg male, 30g alcohol, 1 hour
        bac = calculate_bac(70, Gender.MALE, 30, 1)
        # Should be positive but reduced by metabolism
        self.assertGreater(bac, 0)
        self.assertLess(bac, 1.0)  # Shouldn't be impossibly high
    
    def test_calculate_bac_female(self):
        """Test BAC calculation for female (higher BAC than male same weight)."""
        # Same parameters, different gender
        bac_male = calculate_bac(70, Gender.MALE, 30, 1)
        bac_female = calculate_bac(70, Gender.FEMALE, 30, 1)
        # Female should have higher BAC due to lower widmark factor
        self.assertGreater(bac_female, bac_male)
    
    def test_calculate_bac_zero_alcohol(self):
        """Test BAC with no alcohol consumed."""
        bac = calculate_bac(70, Gender.MALE, 0, 1)
        self.assertEqual(bac, 0.0)
    
    def test_calculate_bac_zero_time(self):
        """Test BAC with no time passed."""
        bac = calculate_bac(70, Gender.MALE, 30, 0)
        self.assertGreater(bac, 0)
    
    def test_calculate_bac_long_time(self):
        """Test BAC after long time (should be near zero)."""
        # 30g alcohol, 24 hours later
        bac = calculate_bac(70, Gender.MALE, 30, 24)
        self.assertAlmostEqual(bac, 0.0, places=2)
    
    def test_calculate_bac_negative_hours(self):
        """Test BAC with negative hours returns 0."""
        bac = calculate_bac(70, Gender.MALE, 30, -1)
        self.assertEqual(bac, 0.0)
    
    def test_calculate_bac_zero_weight(self):
        """Test BAC with zero weight returns 0."""
        bac = calculate_bac(0, Gender.MALE, 30, 1)
        self.assertEqual(bac, 0.0)
    
    def test_calculate_bac_metabolism_rate(self):
        """Test that different metabolism rates affect BAC."""
        bac_slow = calculate_bac(70, Gender.MALE, 30, 2, metabolism_rate=0.01)
        bac_fast = calculate_bac(70, Gender.MALE, 30, 2, metabolism_rate=0.02)
        # Faster metabolism should result in lower BAC
        self.assertGreater(bac_slow, bac_fast)


class TestBACFromDrinks(unittest.TestCase):
    """Test BAC calculation from list of drinks."""
    
    def test_single_drink(self):
        """Test BAC from single drink."""
        now = datetime.now()
        drinks = [Drink.from_beer(500, 5.0, "Beer", now - timedelta(hours=1))]
        bac = calculate_bac_from_drinks(70, Gender.MALE, drinks, now)
        self.assertGreater(bac, 0)
    
    def test_multiple_drinks(self):
        """Test BAC from multiple drinks."""
        now = datetime.now()
        drinks = [
            Drink.from_beer(500, 5.0, "Beer", now - timedelta(hours=2)),
            Drink.from_wine(150, 12.0, "Wine", now - timedelta(hours=1)),
        ]
        bac = calculate_bac_from_drinks(70, Gender.MALE, drinks, now)
        self.assertGreater(bac, 0)
    
    def test_drinks_without_timestamp(self):
        """Test drinks consumed just now (no timestamp)."""
        drinks = [Drink.from_standard("Beer", units=2)]
        bac = calculate_bac_from_drinks(70, Gender.MALE, drinks)
        self.assertGreater(bac, 0)
    
    def test_future_drink(self):
        """Test that future drinks don't affect current BAC."""
        now = datetime.now()
        drinks = [Drink.from_standard("Beer", units=2, consumed_at=now + timedelta(hours=1))]
        bac = calculate_bac_from_drinks(70, Gender.MALE, drinks, now)
        self.assertEqual(bac, 0.0)


class TestImpairmentLevel(unittest.TestCase):
    """Test impairment level determination."""
    
    def test_sober(self):
        """Test sober level."""
        level, desc = get_impairment_level(0.01)
        self.assertEqual(level, ImpairmentLevel.SOBER)
    
    def test_mild(self):
        """Test mild impairment."""
        level, desc = get_impairment_level(0.03)
        self.assertEqual(level, ImpairmentLevel.MILD)
    
    def test_moderate(self):
        """Test moderate impairment."""
        level, desc = get_impairment_level(0.07)
        self.assertEqual(level, ImpairmentLevel.MODERATE)
    
    def test_significant(self):
        """Test significant impairment."""
        level, desc = get_impairment_level(0.12)
        self.assertEqual(level, ImpairmentLevel.SIGNIFICANT)
    
    def test_severe(self):
        """Test severe impairment."""
        level, desc = get_impairment_level(0.18)
        self.assertEqual(level, ImpairmentLevel.SEVERE)
    
    def test_dangerous(self):
        """Test dangerous level."""
        level, desc = get_impairment_level(0.25)
        self.assertEqual(level, ImpairmentLevel.DANGEROUS)
    
    def test_life_threatening(self):
        """Test life-threatening level."""
        level, desc = get_impairment_level(0.35)
        self.assertEqual(level, ImpairmentLevel.LIFE_THREATENING)
    
    def test_description_not_empty(self):
        """Test that descriptions are provided."""
        for bac in [0.01, 0.03, 0.07, 0.12, 0.18, 0.25, 0.35]:
            level, desc = get_impairment_level(bac)
            self.assertTrue(len(desc) > 0)


class TestTimeToSober(unittest.TestCase):
    """Test time-to-sober calculations."""
    
    def test_zero_bac(self):
        """Test zero BAC returns 0 hours."""
        hours = time_to_sober(0.0)
        self.assertEqual(hours, 0.0)
    
    def test_typical_bac(self):
        """Test typical BAC level."""
        hours = time_to_sober(0.08)
        # At 0.015/hour, should be about 5.33 hours
        self.assertGreater(hours, 5)
        self.assertLess(hours, 6)
    
    def test_high_bac(self):
        """Test high BAC takes longer."""
        hours_low = time_to_sober(0.10)
        hours_high = time_to_sober(0.20)
        self.assertGreater(hours_high, hours_low)
    
    def test_custom_metabolism(self):
        """Test custom metabolism rate."""
        hours_slow = time_to_sober(0.08, metabolism_rate=0.01)
        hours_fast = time_to_sober(0.08, metabolism_rate=0.02)
        self.assertGreater(hours_slow, hours_fast)


class TestLegalLimits(unittest.TestCase):
    """Test legal limit functions."""
    
    def test_us_limit(self):
        """Test US legal limit."""
        limit = get_legal_limit("US")
        self.assertEqual(limit, 0.08)
    
    def test_china_limit(self):
        """Test China legal limit."""
        limit = get_legal_limit("CN")
        self.assertEqual(limit, 0.02)
    
    def test_germany_limit(self):
        """Test Germany legal limit."""
        limit = get_legal_limit("DE")
        self.assertEqual(limit, 0.05)
    
    def test_unknown_country(self):
        """Test unknown country defaults to US limit."""
        limit = get_legal_limit("XX")
        self.assertEqual(limit, 0.08)
    
    def test_case_insensitive(self):
        """Test country code is case insensitive."""
        limit_lower = get_legal_limit("us")
        limit_upper = get_legal_limit("US")
        self.assertEqual(limit_lower, limit_upper)
    
    def test_zero_tolerance_countries(self):
        """Test zero tolerance country list."""
        zero_countries = list_zero_tolerance_countries()
        self.assertIn("BR", zero_countries)  # Brazil
        self.assertIn("CZ", zero_countries)  # Czech Republic
        self.assertIn("HU", zero_countries)  # Hungary
    
    def test_time_to_legal_limit(self):
        """Test time to legal limit calculation."""
        # At 0.08 with US limit (0.08), should be 0
        hours = time_to_legal_limit(0.08, "US")
        self.assertEqual(hours, 0.0)
        
        # At 0.10 with US limit, should be positive
        hours = time_to_legal_limit(0.10, "US")
        self.assertGreater(hours, 0)
        
        # At 0.04 with China limit (0.02), should be positive
        hours = time_to_legal_limit(0.04, "CN")
        self.assertGreater(hours, 0)


class TestBACResult(unittest.TestCase):
    """Test BACResult dataclass."""
    
    def test_full_result(self):
        """Test complete result calculation."""
        result = calculate_bac_result(70, Gender.MALE, 30, 1, "US")
        
        self.assertGreater(result.bac, 0)
        self.assertIn(result.impairment, ImpairmentLevel)
        self.assertTrue(len(result.description) > 0)
        self.assertGreaterEqual(result.time_to_sober, 0)
        self.assertGreaterEqual(result.time_to_drive, 0)
        self.assertIsInstance(result.is_legal_to_drive, bool)
        self.assertTrue(len(result.confidence) > 0)
    
    def test_legal_to_drive(self):
        """Test legal driving determination."""
        # Small amount, should be legal
        result = calculate_bac_result(70, Gender.MALE, 5, 3, "US")
        self.assertTrue(result.is_legal_to_drive)
        
        # Large amount, should be illegal
        result = calculate_bac_result(70, Gender.MALE, 100, 0.5, "US")
        self.assertFalse(result.is_legal_to_drive)


class TestHelperFunctions(unittest.TestCase):
    """Test helper functions."""
    
    def test_estimate_alcohol_content(self):
        """Test alcohol content estimation."""
        # 500ml beer at 5% ABV
        grams = estimate_alcohol_content(500, 5.0)
        # 500 * 0.05 * 0.789 = 19.725
        self.assertAlmostEqual(grams, 19.725, places=2)
    
    def test_format_bac(self):
        """Test BAC formatting."""
        self.assertEqual(format_bac(0.08), "0.080%")
        self.assertEqual(format_bac(0.0), "0.000%")
        self.assertEqual(format_bac(0.12345), "0.123%")
    
    def test_format_time_hours(self):
        """Test time formatting."""
        self.assertEqual(format_time_hours(0), "Now")
        self.assertEqual(format_time_hours(0.5), "30 minutes")
        self.assertEqual(format_time_hours(1), "1 hour")
        self.assertEqual(format_time_hours(2), "2 hours")
        self.assertEqual(format_time_hours(1.5), "1 hour 30 min")
        self.assertEqual(format_time_hours(2.25), "2 hours 15 min")
    
    def test_calculate_drinks_by_bac(self):
        """Test reverse calculation - drinks needed for target BAC."""
        # Should return a reasonable number of drinks
        drinks = calculate_drinks_by_bac(0.05, 70, Gender.MALE, 0)
        self.assertGreater(drinks, 0)
        
        # Heavier person needs MORE drinks for same BAC (not fewer)
        # BAC = Alcohol / (Weight × r) × 100 → heavier needs more alcohol
        drinks_light = calculate_drinks_by_bac(0.05, 60, Gender.MALE, 0)
        drinks_heavy = calculate_drinks_by_bac(0.05, 80, Gender.MALE, 0)
        self.assertGreater(drinks_heavy, drinks_light)  # Fixed: heavier needs more
    
    def test_get_bac_warning(self):
        """Test warning messages."""
        warnings = get_bac_warning(0.01)
        self.assertEqual(len(warnings), 0)  # No warnings for very low BAC
        
        warnings = get_bac_warning(0.06)
        self.assertGreater(len(warnings), 0)  # Should have warnings
        
        warnings = get_bac_warning(0.35)
        self.assertGreater(len(warnings), 0)  # Should have severe warnings


class TestConvenienceFunctions(unittest.TestCase):
    """Test convenience functions for common scenarios."""
    
    def test_beer_bac(self):
        """Test beer BAC calculation."""
        bac = beer_bac(70, Gender.MALE, 2, 2)
        self.assertGreater(bac, 0)
    
    def test_wine_bac(self):
        """Test wine BAC calculation."""
        bac = wine_bac(60, Gender.FEMALE, 2, 2)
        self.assertGreater(bac, 0)
    
    def test_spirit_bac(self):
        """Test spirit BAC calculation."""
        bac = spirit_bac(80, Gender.MALE, 3, 1)
        self.assertGreater(bac, 0)
    
    def test_different_volumes(self):
        """Test different beer volumes."""
        bac_small = beer_bac(70, Gender.MALE, 2, 2, volume_ml=330)
        bac_large = beer_bac(70, Gender.MALE, 2, 2, volume_ml=500)
        self.assertGreater(bac_large, bac_small)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""
    
    def test_very_high_bac(self):
        """Test very high BAC (life-threatening)."""
        bac = calculate_bac(50, Gender.FEMALE, 200, 0.5)
        level, _ = get_impairment_level(bac)
        self.assertEqual(level, ImpairmentLevel.LIFE_THREATENING)
    
    def test_exact_boundary_values(self):
        """Test exact boundary values for impairment levels."""
        # Just below threshold
        level, _ = get_impairment_level(0.019)
        self.assertEqual(level, ImpairmentLevel.SOBER)
        
        level, _ = get_impairment_level(0.02)
        self.assertEqual(level, ImpairmentLevel.MILD)
        
        level, _ = get_impairment_level(0.049)
        self.assertEqual(level, ImpairmentLevel.MILD)
        
        level, _ = get_impairment_level(0.05)
        self.assertEqual(level, ImpairmentLevel.MODERATE)
    
    def test_very_small_amounts(self):
        """Test very small alcohol amounts."""
        bac = calculate_bac(100, Gender.MALE, 1, 0.1)
        # Should be very small but positive
        self.assertGreaterEqual(bac, 0)
    
    def test_multiple_countries_legal_limits(self):
        """Test legal limit comparison across countries."""
        bac = 0.05
        
        # Should be legal in UK
        hours_uk = time_to_legal_limit(bac, "UK")
        self.assertEqual(hours_uk, 0.0)
        
        # Should NOT be legal in China
        hours_cn = time_to_legal_limit(bac, "CN")
        self.assertGreater(hours_cn, 0)
        
        # Should NOT be legal in zero-tolerance countries
        hours_br = time_to_legal_limit(bac, "BR")
        self.assertGreater(hours_br, 0)


class TestLegalLimitsData(unittest.TestCase):
    """Test the legal limits data."""
    
    def test_all_limits_positive(self):
        """Test all legal limits are non-negative."""
        for country, limit in LEGAL_LIMITS.items():
            self.assertGreaterEqual(limit, 0, f"{country} has negative limit")
            self.assertLessEqual(limit, 0.5, f"{country} has suspiciously high limit")
    
    def test_common_countries_exist(self):
        """Test that common countries are in the data."""
        common = ["US", "UK", "DE", "FR", "JP", "CN", "AU", "CA"]
        for country in common:
            self.assertIn(country, LEGAL_LIMITS)


if __name__ == "__main__":
    unittest.main(verbosity=2)