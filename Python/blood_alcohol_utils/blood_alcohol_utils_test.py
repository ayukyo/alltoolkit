#!/usr/bin/env python3
"""Blood Alcohol Utils Tests"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    create_drink, create_drink_from_preset,
    calculate_bac_widmark, calculate_bac_watson,
    calculate_total_alcohol, calculate_hours_elapsed,
    get_legal_limit, time_to_sober, time_to_legal,
    categorize_bac, calculate_bac,
    calculate_drinks_to_limit, estimate_metabolism_time,
    quick_bac, drinking_session_summary,
    normalize_gender, AlcoholDrink, BACResult,
    STANDARD_DRINK_GRAMS, LEGAL_LIMITS, DRINK_PRESETS
)


class TestOutcomeCollector:
    """收集测试结果"""
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def add_pass(self, name):
        self.passed += 1
        print(f"✓ {name}")
    
    def add_fail(self, name, msg):
        self.failed += 1
        self.errors.append((name, msg))
        print(f"✗ {name}: {msg}")
    
    def report(self):
        print(f"\n{'='*60}")
        print(f"Blood Alcohol Utils Tests: {self.passed} passed, {self.failed} failed")
        if self.errors:
            print(f"\nFailed tests:")
            for name, msg in self.errors:
                print(f"  - {name}: {msg}")
        print(f"{'='*60}")
        return self.failed == 0


def run_tests():
    results = TestOutcomeCollector()
    
    # Test 1: Normalize gender
    try:
        assert normalize_gender("male") == "male"
        assert normalize_gender("m") == "male"
        assert normalize_gender("female") == "female"
        assert normalize_gender("f") == "female"
        results.add_pass("Normalize gender")
    except Exception as e:
        results.add_fail("Normalize gender", str(e))
    
    # Test 2: Create drink
    try:
        drink = create_drink("Beer", 355, 0.05)
        assert drink.name == "Beer"
        assert drink.volume_ml == 355
        assert drink.alcohol_percent == 0.05
        assert abs(drink.alcohol_grams - 14.0) < 0.1  # 355 * 0.05 * 0.789
        results.add_pass("Create drink")
    except Exception as e:
        results.add_fail("Create drink", str(e))
    
    # Test 3: Create drink from preset
    try:
        beer = create_drink_from_preset("beer_regular")
        assert beer.volume_ml == 355
        assert beer.alcohol_percent == 0.05
        
        wine = create_drink_from_preset("wine_red")
        assert wine.volume_ml == 150
        assert wine.alcohol_percent == 0.13
        results.add_pass("Create drink from preset")
    except Exception as e:
        results.add_fail("Create drink from preset", str(e))
    
    # Test 4: Calculate total alcohol
    try:
        drinks = [
            create_drink("Beer", 355, 0.05),
            create_drink("Wine", 150, 0.12)
        ]
        total = calculate_total_alcohol(drinks)
        expected = 355 * 0.05 * 0.789 + 150 * 0.12 * 0.789
        assert abs(total - expected) < 0.1
        results.add_pass("Calculate total alcohol")
    except Exception as e:
        results.add_fail("Calculate total alcohol", str(e))
    
    # Test 5: BAC Widmark - male
    try:
        bac = calculate_bac_widmark(70, "male", 28, 0)
        # 28g / (70kg * 0.68) * 0.1 ≈ 0.0588
        assert 0.05 < bac < 0.07
        results.add_pass("BAC Widmark male")
    except Exception as e:
        results.add_fail("BAC Widmark male", str(e))
    
    # Test 6: BAC Widmark - female
    try:
        bac = calculate_bac_widmark(60, "female", 28, 0)
        # 28g / (60kg * 0.55) * 0.1 ≈ 0.0848
        assert 0.07 < bac < 0.10
        results.add_pass("BAC Widmark female")
    except Exception as e:
        results.add_fail("BAC Widmark female", str(e))
    
    # Test 7: BAC Widmark - with hours elapsed
    try:
        bac_no_time = calculate_bac_widmark(70, "male", 28, 0)
        bac_with_time = calculate_bac_widmark(70, "male", 28, 2)
        # Should decrease by metabolism rate
        assert bac_with_time < bac_no_time
        assert bac_with_time >= 0
        results.add_pass("BAC Widmark with time")
    except Exception as e:
        results.add_fail("BAC Widmark with time", str(e))
    
    # Test 8: BAC Watson
    try:
        bac = calculate_bac_watson(70, 175, "male", 30, 28, 0)
        # Similar to Widmark but considers body water
        assert 0.05 < bac < 0.10
        results.add_pass("BAC Watson")
    except Exception as e:
        results.add_fail("BAC Watson", str(e))
    
    # Test 9: Get legal limit
    try:
        assert get_legal_limit("china") == 0.02
        assert get_legal_limit("us") == 0.08
        assert get_legal_limit("japan") == 0.03
        assert get_legal_limit("germany") == 0.05
        results.add_pass("Get legal limit")
    except Exception as e:
        results.add_fail("Get legal limit", str(e))
    
    # Test 10: Time to sober
    try:
        hours = time_to_sober(0.08)
        # 0.08 / 0.015 ≈ 5.33 hours
        assert 5 < hours < 6
        results.add_pass("Time to sober")
    except Exception as e:
        results.add_fail("Time to sober", str(e))
    
    # Test 11: Time to legal
    try:
        hours = time_to_legal(0.08, 0.05)
        # (0.08 - 0.05) / 0.015 = 2 hours
        assert hours == 2.0
        results.add_pass("Time to legal")
    except Exception as e:
        results.add_fail("Time to legal", str(e))
    
    # Test 12: Time to legal - already legal
    try:
        hours = time_to_legal(0.03, 0.05)
        assert hours == 0
        results.add_pass("Time to legal already legal")
    except Exception as e:
        results.add_fail("Time to legal already legal", str(e))
    
    # Test 13: Categorize BAC - sober
    try:
        cat, imp = categorize_bac(0)
        assert cat == "Sober"
        assert imp == "No impairment"
        results.add_pass("Categorize BAC sober")
    except Exception as e:
        results.add_fail("Categorize BAC sober", str(e))
    
    # Test 14: Categorize BAC - slight
    try:
        cat, imp = categorize_bac(0.03)
        assert cat == "Slight"
        results.add_pass("Categorize BAC slight")
    except Exception as e:
        results.add_fail("Categorize BAC slight", str(e))
    
    # Test 15: Categorize BAC - high
    try:
        cat, imp = categorize_bac(0.09)
        assert cat == "High"
        results.add_pass("Categorize BAC high")
    except Exception as e:
        results.add_fail("Categorize BAC high", str(e))
    
    # Test 16: Categorize BAC - dangerous
    try:
        cat, imp = categorize_bac(0.25)
        assert cat == "Dangerous"
        results.add_pass("Categorize BAC dangerous")
    except Exception as e:
        results.add_fail("Categorize BAC dangerous", str(e))
    
    # Test 17: Calculate BAC full
    try:
        drinks = [create_drink_from_preset("beer_regular")]
        result = calculate_bac(70, "male", drinks, hours_elapsed=1)
        assert isinstance(result, BACResult)
        assert result.bac >= 0
        assert isinstance(result.is_legal, bool)
        assert result.time_to_sober >= 0
        results.add_pass("Calculate BAC full")
    except Exception as e:
        results.add_fail("Calculate BAC full", str(e))
    
    # Test 18: Quick BAC
    try:
        bac = quick_bac(70, "male", 2, "beer_regular", 1)
        assert bac >= 0
        # 2 beers: ~28g alcohol, after 1 hour
        assert bac < 0.1
        results.add_pass("Quick BAC")
    except Exception as e:
        results.add_fail("Quick BAC", str(e))
    
    # Test 19: Drinking session summary
    try:
        drinks = [create_drink_from_preset("beer_regular") for _ in range(3)]
        summary = drinking_session_summary(70, "male", drinks)
        assert 'bac_percent' in summary
        assert 'is_legal' in summary
        assert 'total_alcohol_grams' in summary
        assert summary['drink_count'] == 3
        results.add_pass("Drinking session summary")
    except Exception as e:
        results.add_fail("Drinking session summary", str(e))
    
    # Test 20: Standard drink grams
    try:
        assert STANDARD_DRINK_GRAMS["us"] == 14.0
        assert STANDARD_DRINK_GRAMS["uk"] == 8.0
        assert STANDARD_DRINK_GRAMS["au"] == 10.0
        results.add_pass("Standard drink grams")
    except Exception as e:
        results.add_fail("Standard drink grams", str(e))
    
    # Test 21: Legal limits dict
    try:
        assert len(LEGAL_LIMITS) >= 10
        assert "china" in LEGAL_LIMITS
        assert "us" in LEGAL_LIMITS
        results.add_pass("Legal limits dict")
    except Exception as e:
        results.add_fail("Legal limits dict", str(e))
    
    # Test 22: Drink presets
    try:
        assert len(DRINK_PRESETS) >= 10
        assert "beer_regular" in DRINK_PRESETS
        assert "wine_red" in DRINK_PRESETS
        results.add_pass("Drink presets")
    except Exception as e:
        results.add_fail("Drink presets", str(e))
    
    # Test 23: Estimate metabolism time
    try:
        hours = estimate_metabolism_time(14, 70, "male")
        # One standard drink, should metabolize in ~1 hour
        assert 0.5 < hours < 2
        results.add_pass("Estimate metabolism time")
    except Exception as e:
        results.add_fail("Estimate metabolism time", str(e))
    
    # Test 24: Calculate drinks to limit
    try:
        max_drinks = calculate_drinks_to_limit(70, "male", 0.05, 2)
        assert max_drinks >= 1
        assert isinstance(max_drinks, int)
        results.add_pass("Calculate drinks to limit")
    except Exception as e:
        results.add_fail("Calculate drinks to limit", str(e))
    
    # Test 25: AlcoholDrink properties
    try:
        drink = AlcoholDrink("Test", 100, 0.10)
        assert drink.name == "Test"
        assert abs(drink.alcohol_grams - 7.89) < 0.1
        results.add_pass("AlcoholDrink properties")
    except Exception as e:
        results.add_fail("AlcoholDrink properties", str(e))
    
    # Test 26: Invalid gender
    try:
        normalize_gender("invalid")
        results.add_fail("Invalid gender", "Should raise ValueError")
    except ValueError:
        results.add_pass("Invalid gender")
    except Exception as e:
        results.add_fail("Invalid gender", str(e))
    
    # Test 27: Invalid country
    try:
        get_legal_limit("invalid_country")
        results.add_fail("Invalid country", "Should raise ValueError")
    except ValueError:
        results.add_pass("Invalid country")
    except Exception as e:
        results.add_fail("Invalid country", str(e))
    
    # Test 28: Invalid preset
    try:
        create_drink_from_preset("invalid_preset")
        results.add_fail("Invalid preset", "Should raise ValueError")
    except ValueError:
        results.add_pass("Invalid preset")
    except Exception as e:
        results.add_fail("Invalid preset", str(e))
    
    # Test 29: Zero BAC time to sober
    try:
        hours = time_to_sober(0)
        assert hours == 0
        results.add_pass("Zero BAC time to sober")
    except Exception as e:
        results.add_fail("Zero BAC time to sober", str(e))
    
    # Test 30: Negative BAC handling
    try:
        bac = calculate_bac_widmark(70, "male", 1, 100)  # Very long time
        assert bac == 0  # Should clamp to 0
        results.add_pass("Negative BAC handling")
    except Exception as e:
        results.add_fail("Negative BAC handling", str(e))
    
    return results.report()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)