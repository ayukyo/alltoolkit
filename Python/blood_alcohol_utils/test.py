"""
Tests for Blood Alcohol Content (BAC) Calculator Utils
"""

import unittest
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from blood_alcohol_utils.mod import (
    AlcoholDrink,
    BACResult,
    normalize_gender,
    create_drink,
    create_drink_from_preset,
    calculate_bac_widmark,
    calculate_bac_watson,
    calculate_total_alcohol,
    calculate_hours_elapsed,
    get_legal_limit,
    time_to_sober,
    time_to_legal,
    categorize_bac,
    calculate_bac,
    calculate_drinks_to_limit,
    estimate_metabolism_time,
    calculate_bac_at_time,
    suggest_waiting_time,
    drinking_session_summary,
    quick_bac,
    STANDARD_DRINK_GRAMS,
    LEGAL_LIMITS,
    DRINK_PRESETS,
    METABOLISM_RATE,
)


class TestNormalizeGender(unittest.TestCase):
    """Test gender normalization."""
    
    def test_male_variations(self):
        self.assertEqual(normalize_gender("male"), "male")
        self.assertEqual(normalize_gender("Male"), "male")
        self.assertEqual(normalize_gender("MALE"), "male")
        self.assertEqual(normalize_gender("m"), "male")
        self.assertEqual(normalize_gender("M"), "male")
    
    def test_female_variations(self):
        self.assertEqual(normalize_gender("female"), "female")
        self.assertEqual(normalize_gender("Female"), "female")
        self.assertEqual(normalize_gender("FEMALE"), "female")
        self.assertEqual(normalize_gender("f"), "female")
        self.assertEqual(normalize_gender("F"), "female")
    
    def test_invalid_gender(self):
        with self.assertRaises(ValueError):
            normalize_gender("other")


class TestAlcoholDrink(unittest.TestCase):
    """Test AlcoholDrink class."""
    
    def test_beer_creation(self):
        drink = AlcoholDrink("Beer", 355, 0.05)
        self.assertEqual(drink.name, "Beer")
        self.assertEqual(drink.volume_ml, 355)
        self.assertEqual(drink.alcohol_percent, 0.05)
    
    def test_alcohol_grams_calculation(self):
        # 355ml × 5% × 0.789 density ≈ 14g
        drink = AlcoholDrink("Beer", 355, 0.05)
        expected = 355 * 0.05 * 0.789
        self.assertAlmostEqual(drink.alcohol_grams, expected, places=2)
    
    def test_wine_alcohol(self):
        # 150ml × 13% × 0.789 ≈ 15.4g
        drink = AlcoholDrink("Wine", 150, 0.13)
        expected = 150 * 0.13 * 0.789
        self.assertAlmostEqual(drink.alcohol_grams, expected, places=2)
    
    def test_spirits_alcohol(self):
        # 44ml × 40% × 0.789 ≈ 13.9g
        drink = AlcoholDrink("Vodka", 44, 0.40)
        expected = 44 * 0.40 * 0.789
        self.assertAlmostEqual(drink.alcohol_grams, expected, places=2)


class TestDrinkPresets(unittest.TestCase):
    """Test drink preset functions."""
    
    def test_create_from_preset(self):
        drink = create_drink_from_preset("beer_regular")
        self.assertEqual(drink.volume_ml, 355)
        self.assertEqual(drink.alcohol_percent, 0.05)
    
    def test_create_from_preset_with_multiplier(self):
        drink = create_drink_from_preset("beer_regular", volume_multiplier=2.0)
        self.assertEqual(drink.volume_ml, 710)  # 355 * 2
    
    def test_invalid_preset(self):
        with self.assertRaises(ValueError):
            create_drink_from_preset("invalid_drink")
    
    def test_all_presets_valid(self):
        """Verify all presets have valid data."""
        for name, preset in DRINK_PRESETS.items():
            drink = create_drink_from_preset(name)
            self.assertGreater(drink.volume_ml, 0)
            self.assertGreater(drink.alcohol_percent, 0)
            self.assertLess(drink.alcohol_percent, 1)


class TestBACCalculations(unittest.TestCase):
    """Test BAC calculation functions."""
    
    def test_widmark_male(self):
        # 70kg male, 28g alcohol, 0 hours
        bac = calculate_bac_widmark(70, "male", 28, 0)
        # BAC = (28 / (70 * 0.68)) * 0.1 ≈ 0.059%
        self.assertAlmostEqual(bac, 0.059, places=2)
    
    def test_widmark_female(self):
        # 60kg female, 28g alcohol, 0 hours
        bac = calculate_bac_widmark(60, "female", 28, 0)
        # BAC = (28 / (60 * 0.55)) * 0.1 ≈ 0.085%
        self.assertAlmostEqual(bac, 0.085, places=2)
    
    def test_widmark_with_metabolism(self):
        # 70kg male, 28g alcohol, 2 hours
        bac_no_time = calculate_bac_widmark(70, "male", 28, 0)
        bac_with_time = calculate_bac_widmark(70, "male", 28, 2)
        # Should be reduced by 2 * 0.015 = 0.03%
        self.assertAlmostEqual(bac_no_time - bac_with_time, 0.03, places=2)
    
    def test_widmark_zero_alcohol(self):
        bac = calculate_bac_widmark(70, "male", 0, 0)
        self.assertEqual(bac, 0)
    
    def test_widmark_negative_result_returns_zero(self):
        # Large amount of time should result in 0, not negative
        bac = calculate_bac_widmark(70, "male", 14, 10)
        self.assertGreaterEqual(bac, 0)
    
    def test_widmark_invalid_weight(self):
        with self.assertRaises(ValueError):
            calculate_bac_widmark(0, "male", 14, 0)
        with self.assertRaises(ValueError):
            calculate_bac_widmark(-10, "male", 14, 0)
    
    def test_watson_male(self):
        # 70kg, 175cm, 30 years old, 28g alcohol
        bac = calculate_bac_watson(70, 175, "male", 30, 28, 0)
        self.assertGreater(bac, 0)
        self.assertLess(bac, 0.5)  # Reasonable range for BAC
    
    def test_watson_female(self):
        # 60kg, 165cm, 25 years old, 28g alcohol
        bac = calculate_bac_watson(60, 165, "female", 25, 28, 0)
        self.assertGreater(bac, 0)
        self.assertLess(bac, 0.5)
    
    def test_watson_invalid_inputs(self):
        with self.assertRaises(ValueError):
            calculate_bac_watson(0, 175, "male", 30, 28, 0)
        with self.assertRaises(ValueError):
            calculate_bac_watson(70, 0, "male", 30, 28, 0)


class TestLegalLimits(unittest.TestCase):
    """Test legal limit functions."""
    
    def test_get_legal_limit_us(self):
        self.assertEqual(get_legal_limit("us"), 0.08)
    
    def test_get_legal_limit_china(self):
        self.assertEqual(get_legal_limit("china"), 0.02)
    
    def test_get_legal_limit_germany(self):
        self.assertEqual(get_legal_limit("germany"), 0.05)
    
    def test_get_legal_limit_japan(self):
        self.assertEqual(get_legal_limit("japan"), 0.03)
    
    def test_invalid_country(self):
        with self.assertRaises(ValueError):
            get_legal_limit("invalid_country")


class TestTimeCalculations(unittest.TestCase):
    """Test time-related calculations."""
    
    def test_time_to_sober_zero(self):
        self.assertEqual(time_to_sober(0), 0)
    
    def test_time_to_sober(self):
        # 0.08% / 0.015 per hour ≈ 5.33 hours
        hours = time_to_sober(0.08)
        self.assertAlmostEqual(hours, 5.33, places=2)
    
    def test_time_to_legal_already_legal(self):
        hours = time_to_legal(0.03, 0.08)
        self.assertEqual(hours, 0)
    
    def test_time_to_legal(self):
        # From 0.08 to 0.05 = 0.03 / 0.015 = 2 hours
        hours = time_to_legal(0.08, 0.05)
        self.assertAlmostEqual(hours, 2.0, places=2)
    
    def test_hours_elapsed(self):
        start = datetime.now() - timedelta(hours=2.5)
        elapsed = calculate_hours_elapsed(start)
        self.assertAlmostEqual(elapsed, 2.5, places=1)
    
    def test_hours_elapsed_future(self):
        # Future time should return 0
        future = datetime.now() + timedelta(hours=2)
        elapsed = calculate_hours_elapsed(future)
        self.assertEqual(elapsed, 0)


class TestBACCategorization(unittest.TestCase):
    """Test BAC categorization."""
    
    def test_sober(self):
        category, impairment = categorize_bac(0)
        self.assertEqual(category, "Sober")
    
    def test_trace(self):
        category, _ = categorize_bac(0.01)
        self.assertEqual(category, "Trace")
    
    def test_slight(self):
        category, _ = categorize_bac(0.03)
        self.assertEqual(category, "Slight")
    
    def test_moderate(self):
        category, _ = categorize_bac(0.06)
        self.assertEqual(category, "Moderate")
    
    def test_high(self):
        category, _ = categorize_bac(0.09)
        self.assertEqual(category, "High")
    
    def test_very_high(self):
        category, _ = categorize_bac(0.12)
        self.assertEqual(category, "Very High")
    
    def test_severe(self):
        category, _ = categorize_bac(0.18)
        self.assertEqual(category, "Severe")
    
    def test_dangerous(self):
        category, _ = categorize_bac(0.25)
        self.assertEqual(category, "Dangerous")
    
    def test_life_threatening(self):
        category, _ = categorize_bac(0.35)
        self.assertEqual(category, "Life-threatening")


class TestCalculateBAC(unittest.TestCase):
    """Test comprehensive BAC calculation."""
    
    def test_basic_calculation(self):
        drinks = [create_drink_from_preset("beer_regular") for _ in range(2)]
        result = calculate_bac(70, "male", drinks, hours_elapsed=1)
        
        self.assertIsInstance(result, BACResult)
        self.assertGreater(result.bac, 0)
        self.assertEqual(result.bac_permille, result.bac * 10)
    
    def test_is_legal(self):
        drinks = [create_drink_from_preset("beer_regular")]
        result = calculate_bac(70, "male", drinks, hours_elapsed=2, country="us")
        # One beer, 2 hours later should be legal
        self.assertTrue(result.is_legal)
    
    def test_not_legal(self):
        drinks = [create_drink_from_preset("spirits_vodka") for _ in range(6)]
        result = calculate_bac(60, "female", drinks, hours_elapsed=0.5, country="us")
        self.assertFalse(result.is_legal)
    
    def test_china_stricter_limit(self):
        drinks = [create_drink_from_preset("beer_regular")]
        result_china = calculate_bac(70, "male", drinks, hours_elapsed=1, country="china")
        result_us = calculate_bac(70, "male", drinks, hours_elapsed=1, country="us")
        # China has stricter limit
        self.assertLess(result_china.legal_limit, result_us.legal_limit)


class TestDrinksToLimit(unittest.TestCase):
    """Test drinks to limit calculation."""
    
    def test_basic_calculation(self):
        drinks = calculate_drinks_to_limit(70, "male", 0.08, hours=0)
        self.assertGreater(drinks, 0)
    
    def test_female_lower_limit(self):
        male_drinks = calculate_drinks_to_limit(70, "male", 0.08, hours=0)
        female_drinks = calculate_drinks_to_limit(60, "female", 0.08, hours=0)
        # Females typically have lower tolerance
        self.assertGreater(male_drinks, female_drinks)
    
    def test_over_time_more_allowed(self):
        instant = calculate_drinks_to_limit(70, "male", 0.08, hours=0)
        over_time = calculate_drinks_to_limit(70, "male", 0.08, hours=3)
        # Drinking over more time allows more drinks
        self.assertGreater(over_time, instant)


class TestQuickBAC(unittest.TestCase):
    """Test quick BAC function."""
    
    def test_quick_calculation(self):
        bac = quick_bac(70, "male", 2, "beer_regular", hours=1)
        self.assertGreater(bac, 0)
        self.assertLess(bac, 0.5)  # Reasonable BAC range
    
    def test_no_drinks_zero_bac(self):
        bac = quick_bac(70, "male", 0, "beer_regular", hours=0)
        self.assertEqual(bac, 0)


class TestSuggestWaitingTime(unittest.TestCase):
    """Test waiting time suggestion."""
    
    def test_already_sober(self):
        result = suggest_waiting_time(0)
        self.assertEqual(result["hours"], 0)
        self.assertEqual(result["minutes"], 0)
    
    def test_waiting_time_calculation(self):
        result = suggest_waiting_time(0.08, 0.0)
        self.assertAlmostEqual(result["hours"], 0.08 / 0.015, places=2)
    
    def test_to_legal_limit(self):
        result = suggest_waiting_time(0.08, 0.05)
        self.assertAlmostEqual(result["hours"], 0.03 / 0.015, places=2)
    
    def test_human_readable_format(self):
        result = suggest_waiting_time(0.05)
        self.assertIn("h", result["human"])
        self.assertIn("m", result["human"])


class TestDrinkingSessionSummary(unittest.TestCase):
    """Test drinking session summary."""
    
    def test_summary_structure(self):
        drinks = [
            create_drink_from_preset("beer_regular"),
            create_drink_from_preset("beer_regular"),
            create_drink_from_preset("wine_red")
        ]
        summary = drinking_session_summary(70, "male", drinks)
        
        self.assertIn("bac_percent", summary)
        self.assertIn("total_alcohol_grams", summary)
        self.assertIn("standard_drinks", summary)
        self.assertIn("is_legal", summary)
        self.assertIn("time_to_sober_hours", summary)
    
    def test_recommendation_legal(self):
        drinks = [create_drink_from_preset("beer_regular")]
        summary = drinking_session_summary(70, "male", drinks, country="us")
        self.assertIn("Legal", summary["recommendation"])


class TestEstimateMetabolismTime(unittest.TestCase):
    """Test metabolism time estimation."""
    
    def test_basic_estimation(self):
        hours = estimate_metabolism_time(14, 70, "male")
        self.assertGreater(hours, 0)
    
    def test_more_alcohol_longer_time(self):
        hours_small = estimate_metabolism_time(14, 70, "male")
        hours_large = estimate_metabolism_time(28, 70, "male")
        self.assertGreater(hours_large, hours_small)


class TestConstants(unittest.TestCase):
    """Test module constants."""
    
    def test_standard_drink_grams(self):
        self.assertIn("us", STANDARD_DRINK_GRAMS)
        self.assertIn("uk", STANDARD_DRINK_GRAMS)
        self.assertEqual(STANDARD_DRINK_GRAMS["us"], 14.0)
    
    def test_legal_limits_countries(self):
        self.assertIn("us", LEGAL_LIMITS)
        self.assertIn("china", LEGAL_LIMITS)
        self.assertIn("japan", LEGAL_LIMITS)
        # China has stricter limit than US
        self.assertLess(LEGAL_LIMITS["china"], LEGAL_LIMITS["us"])
    
    def test_metabolism_rate(self):
        self.assertGreater(METABOLISM_RATE, 0)
        self.assertLess(METABOLISM_RATE, 0.1)


class TestTotalAlcohol(unittest.TestCase):
    """Test total alcohol calculation."""
    
    def test_single_drink(self):
        drink = create_drink_from_preset("beer_regular")
        total = calculate_total_alcohol([drink])
        expected = drink.alcohol_grams
        self.assertEqual(total, expected)
    
    def test_multiple_drinks(self):
        drinks = [
            create_drink_from_preset("beer_regular"),
            create_drink_from_preset("wine_red")
        ]
        total = calculate_total_alcohol(drinks)
        expected = sum(d.alcohol_grams for d in drinks)
        self.assertAlmostEqual(total, expected, places=2)


if __name__ == "__main__":
    unittest.main()