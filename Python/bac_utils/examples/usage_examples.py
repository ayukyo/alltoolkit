"""
BAC Calculator Utils - Usage Examples

This file demonstrates various use cases for the blood alcohol content calculator.
"""

from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    Gender, ImpairmentLevel, Drink, BACResult,
    calculate_bac, calculate_bac_from_drinks, get_impairment_level,
    time_to_sober, time_to_legal_limit, calculate_bac_result,
    estimate_alcohol_content, get_legal_limit, list_zero_tolerance_countries,
    format_bac, format_time_hours, calculate_drinks_by_bac, get_bac_warning,
    beer_bac, wine_bac, spirit_bac, LEGAL_LIMITS
)


def print_separator(title: str = ""):
    """Print a section separator."""
    print("\n" + "=" * 60)
    if title:
        print(f" {title}")
        print("=" * 60)


def example_basic_calculation():
    """Basic BAC calculation example."""
    print_separator("Example 1: Basic BAC Calculation")
    
    # A 70kg male drank 2 beers (each 500ml, 5% ABV) over 2 hours
    weight = 70  # kg
    gender = Gender.MALE
    
    # Calculate total alcohol: 2 beers × 500ml × 5% × 0.789
    alcohol_grams = 2 * estimate_alcohol_content(500, 5.0)
    
    # Calculate BAC
    bac = calculate_bac(weight, gender, alcohol_grams, hours_since_first_drink=2)
    
    print(f"\n📊 Scenario:")
    print(f"   Person: {weight}kg {gender.value}")
    print(f"   Drinks: 2 large beers (500ml each, 5% ABV)")
    print(f"   Time: 2 hours since first drink")
    print(f"   Total alcohol: {alcohol_grams:.1f}g")
    print(f"\n📈 Result:")
    print(f"   Current BAC: {format_bac(bac)}")
    
    level, description = get_impairment_level(bac)
    print(f"   Impairment: {level.value.upper()}")
    print(f"   Description: {description[:60]}...")


def example_full_result():
    """Complete BAC result with all information."""
    print_separator("Example 2: Complete BAC Result")
    
    # A 55kg female had 3 glasses of wine over 3 hours
    weight = 55
    gender = Gender.FEMALE
    
    # 3 glasses of wine (150ml each, 12% ABV)
    alcohol_grams = 3 * estimate_alcohol_content(150, 12.0)
    
    result = calculate_bac_result(
        weight_kg=weight,
        gender=gender,
        alcohol_grams=alcohol_grams,
        hours_since_first_drink=3,
        country_code="CN"  # Using China's strict limit
    )
    
    print(f"\n📊 Scenario:")
    print(f"   Person: {weight}kg {gender.value}")
    print(f"   Drinks: 3 glasses of wine (150ml each, 12% ABV)")
    print(f"   Time: 3 hours since first drink")
    
    print(f"\n📈 Complete Result:")
    print(f"   BAC: {format_bac(result.bac)}")
    print(f"   Impairment Level: {result.impairment.value}")
    print(f"   Time to Sober: {format_time_hours(result.time_to_sober)}")
    print(f"   Time to Legal Limit (China): {format_time_hours(result.time_to_drive)}")
    print(f"   Can Legally Drive: {'✅ Yes' if result.is_legal_to_drive else '❌ No'}")
    print(f"   Confidence: {result.confidence}")
    print(f"\n   Description: {result.description}")


def example_drink_tracking():
    """Track multiple drinks with timestamps."""
    print_separator("Example 3: Drink Tracking Over Time")
    
    now = datetime.now()
    weight = 75
    gender = Gender.MALE
    
    # Simulate a night out with different drinks at different times
    drinks = [
        Drink.from_beer(500, 5.0, "Beer #1", now - timedelta(hours=4)),
        Drink.from_beer(500, 5.0, "Beer #2", now - timedelta(hours=3)),
        Drink.from_wine(150, 12.0, "Wine", now - timedelta(hours=2)),
        Drink.from_spirit(45, 40.0, "Whiskey", now - timedelta(hours=1)),
        Drink.from_standard("Cocktail", units=1.5, consumed_at=now - timedelta(minutes=30)),
    ]
    
    print(f"\n📊 Scenario: Night out tracking")
    print(f"   Person: {weight}kg {gender.value}")
    print(f"\n   🍺 Drinks consumed:")
    
    total_alcohol = 0
    for drink in drinks:
        hours_ago = (now - drink.consumed_at).total_seconds() / 3600
        total_alcohol += drink.alcohol_grams
        print(f"      - {drink.name}: {drink.alcohol_grams:.1f}g alcohol ({hours_ago:.1f}h ago)")
    
    print(f"\n   Total alcohol consumed: {total_alcohol:.1f}g")
    
    # Calculate current BAC
    current_bac = calculate_bac_from_drinks(weight, gender, drinks, now)
    
    print(f"\n📈 Current Status:")
    print(f"   BAC: {format_bac(current_bac)}")
    
    level, _ = get_impairment_level(current_bac)
    print(f"   Impairment: {level.value}")
    
    # Check legal status in different countries
    print(f"\n   🚗 Legal to drive in:")
    for country in ["US", "UK", "DE", "CN", "JP"]:
        limit = get_legal_limit(country)
        is_legal = current_bac <= limit
        status = "✅" if is_legal else "❌"
        hours_to_legal = time_to_legal_limit(current_bac, country)
        if is_legal:
            print(f"      {country} (limit {format_bac(limit)}): {status}")
        else:
            print(f"      {country} (limit {format_bac(limit)}): {status} - {format_time_hours(hours_to_legal)}")


def example_beer_wine_spirit():
    """Quick calculations for common drink types."""
    print_separator("Example 4: Quick Calculations by Drink Type")
    
    weight = 70
    gender = Gender.MALE
    hours = 2
    
    print(f"\n📊 Person: {weight}kg {gender.value}, drinks consumed over {hours} hours")
    print(f"\n   🍺 Beer scenarios:")
    for beers in [1, 2, 3, 4]:
        bac = beer_bac(weight, gender, beers, hours, volume_ml=330, abv=5.0)
        legal_cn = "✅" if bac <= 0.02 else "❌"
        legal_us = "✅" if bac <= 0.08 else "❌"
        print(f"      {beers} beers: {format_bac(bac):>8}  | China: {legal_cn} | US: {legal_us}")
    
    print(f"\n   🍷 Wine scenarios:")
    for glasses in [1, 2, 3, 4]:
        bac = wine_bac(weight, gender, glasses, hours, volume_ml=150, abv=12.0)
        legal_cn = "✅" if bac <= 0.02 else "❌"
        legal_us = "✅" if bac <= 0.08 else "❌"
        print(f"      {glasses} glasses: {format_bac(bac):>8}  | China: {legal_cn} | US: {legal_us}")
    
    print(f"\n   🥃 Spirit scenarios:")
    for shots in [1, 2, 3, 4]:
        bac = spirit_bac(weight, gender, shots, hours, volume_ml=45, abv=40.0)
        legal_cn = "✅" if bac <= 0.02 else "❌"
        legal_us = "✅" if bac <= 0.08 else "❌"
        print(f"      {shots} shots: {format_bac(bac):>8}  | China: {legal_cn} | US: {legal_us}")


def example_gender_difference():
    """Show BAC difference between genders."""
    print_separator("Example 5: Gender Differences in BAC")
    
    weight = 65
    alcohol_grams = 30  # About 3 drinks
    hours = 1.5
    
    bac_male = calculate_bac(weight, Gender.MALE, alcohol_grams, hours)
    bac_female = calculate_bac(weight, Gender.FEMALE, alcohol_grams, hours)
    
    print(f"\n📊 Same person, same drinks, different biological sex:")
    print(f"   Weight: {weight}kg")
    print(f"   Alcohol: {alcohol_grams}g (about 3 standard drinks)")
    print(f"   Time: {hours} hours")
    
    print(f"\n   🚹 Male:")
    print(f"      BAC: {format_bac(bac_male)}")
    level_m, _ = get_impairment_level(bac_male)
    print(f"      Impairment: {level_m.value}")
    print(f"      Time to sober: {format_time_hours(time_to_sober(bac_male))}")
    
    print(f"\n   🚺 Female:")
    print(f"      BAC: {format_bac(bac_female)}")
    level_f, _ = get_impairment_level(bac_female)
    print(f"      Impairment: {level_f.value}")
    print(f"      Time to sober: {format_time_hours(time_to_sober(bac_female))}")
    
    diff = bac_female - bac_male
    print(f"\n   Difference: {format_bac(diff)} higher for female")
    print(f"   (Due to different alcohol distribution ratios)")


def example_legal_limits_world():
    """Legal driving limits around the world."""
    print_separator("Example 6: Legal Driving Limits Worldwide")
    
    print("\n📋 Legal BAC limits for driving by country:")
    
    # Group by limit
    by_limit = {}
    for country, limit in LEGAL_LIMITS.items():
        if limit not in by_limit:
            by_limit[limit] = []
        by_limit[limit].append(country)
    
    for limit in sorted(by_limit.keys()):
        countries = ", ".join(sorted(by_limit[limit]))
        if limit == 0.0:
            print(f"\n   ⛔ 0.00% (Zero Tolerance):")
        else:
            print(f"\n   📊 {format_bac(limit)}:")
        print(f"      {countries}")
    
    # Show zero-tolerance countries
    print(f"\n⚠️  Zero-tolerance countries: {', '.join(list_zero_tolerance_countries())}")
    print("   (Any detectable alcohol is illegal)")


def example_time_to_sober():
    """Calculate when it's safe to drive."""
    print_separator("Example 7: When Can I Drive?")
    
    # Someone had a lot to drink
    weight = 70
    gender = Gender.MALE
    alcohol_grams = 80  # About 8 drinks
    
    # Current BAC (drinks just finished)
    current_bac = calculate_bac(weight, gender, alcohol_grams, hours=0.5)
    
    print(f"\n📊 Scenario:")
    print(f"   Person: {weight}kg {gender.value}")
    print(f"   Alcohol consumed: {alcohol_grams}g (~8 standard drinks)")
    print(f"   Current BAC: {format_bac(current_bac)}")
    
    level, desc = get_impairment_level(current_bac)
    print(f"   Impairment: {level.value.upper()}")
    
    # Warnings
    warnings = get_bac_warning(current_bac)
    if warnings:
        print(f"\n   ⚠️  Warnings:")
        for w in warnings:
            print(f"      {w}")
    
    # Time calculations
    print(f"\n   ⏰ Time estimates:")
    print(f"      Until sober (0.00%): {format_time_hours(time_to_sober(current_bac))}")
    
    for country in ["CN", "DE", "US"]:
        limit = get_legal_limit(country)
        hours = time_to_legal_limit(current_bac, country)
        print(f"      Until legal in {country} ({format_bac(limit)}): {format_time_hours(hours)}")


def example_reverse_calculation():
    """How many drinks to reach a target BAC."""
    print_separator("Example 8: How Many Drinks to Reach Target BAC")
    
    print("\n⚠️  WARNING: For educational purposes only!")
    print("   Never use this to determine if you can drive safely.\n")
    
    weight = 70
    gender = Gender.MALE
    target_bac = 0.05
    
    drinks = calculate_drinks_by_bac(target_bac, weight, gender, hours=0)
    
    print(f"📊 Scenario:")
    print(f"   Person: {weight}kg {gender.value}")
    print(f"   Target BAC: {format_bac(target_bac)}")
    print(f"\n   Standard drinks needed: {drinks:.1f}")
    print(f"   (One standard drink = 10g alcohol)")
    
    print(f"\n   Equivalent to:")
    print(f"      ~{drinks:.1f} beers (330ml, 5%)")
    print(f"      ~{drinks:.1f} glasses wine (150ml, 12%)")
    print(f"      ~{drinks:.1f} shots spirits (45ml, 40%)")


def example_warning_levels():
    """Show all warning levels."""
    print_separator("Example 9: BAC Warning Levels")
    
    print("\n📋 Impairment levels and descriptions:\n")
    
    bac_levels = [
        (0.01, "Just started drinking"),
        (0.03, "Feeling relaxed"),
        (0.05, "Legal limit in many countries"),
        (0.08, "US legal limit"),
        (0.10, "Significant impairment"),
        (0.15, "Very impaired"),
        (0.20, "Severe impairment"),
        (0.25, "Dangerous level"),
        (0.30, "Life-threatening"),
        (0.40, "Potentially fatal"),
    ]
    
    for bac, scenario in bac_levels:
        level, desc = get_impairment_level(bac)
        warnings = get_bac_warning(bac)
        
        print(f"   {format_bac(bac):>8} | {level.value.upper():<18} | {scenario}")
        if warnings:
            for w in warnings[:1]:  # Show first warning only
                print(f"            └─ {w}")


def example_custom_metabolism():
    """Example with different metabolism rates."""
    print_separator("Example 10: Metabolism Rate Variations")
    
    weight = 70
    gender = Gender.MALE
    alcohol_grams = 40  # 4 drinks
    
    print(f"\n📊 Same person, different metabolism rates:")
    print(f"   Weight: {weight}kg {gender.value}")
    print(f"   Alcohol: {alcohol_grams}g")
    
    rates = [
        (0.01, "Slow metabolizer"),
        (0.015, "Average"),
        (0.02, "Fast metabolizer"),
    ]
    
    print(f"\n   After 2 hours:")
    for rate, desc in rates:
        bac = calculate_bac(weight, gender, alcohol_grams, 2, rate)
        hours_sober = time_to_sober(bac, rate)
        print(f"      {desc} ({rate}%/h): {format_bac(bac):>8} | Sober in: {format_time_hours(hours_sober)}")


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("  BLOOD ALCOHOL CONTENT (BAC) CALCULATOR - EXAMPLES")
    print("=" * 60)
    
    example_basic_calculation()
    example_full_result()
    example_drink_tracking()
    example_beer_wine_spirit()
    example_gender_difference()
    example_legal_limits_world()
    example_time_to_sober()
    example_reverse_calculation()
    example_warning_levels()
    example_custom_metabolism()
    
    print("\n" + "=" * 60)
    print("  ⚠️  DISCLAIMER")
    print("=" * 60)
    print("""
    This calculator is for EDUCATIONAL PURPOSES ONLY.
    
    - Individual responses to alcohol vary significantly
    - Many factors affect BAC: food, medication, health, tolerance
    - Never rely solely on calculations to determine sobriety
    - The only safe choice is to not drink and drive
    
    When in doubt, don't drive!
    """)


if __name__ == "__main__":
    main()