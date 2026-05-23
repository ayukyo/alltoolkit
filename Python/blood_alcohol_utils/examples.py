#!/usr/bin/env python3
"""
Blood Alcohol Content (BAC) Calculator Examples

This script demonstrates various use cases for the blood_alcohol_utils module.
"""

from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from blood_alcohol_utils.mod import (
    create_drink,
    create_drink_from_preset,
    calculate_bac,
    calculate_bac_widmark,
    calculate_bac_watson,
    quick_bac,
    drinking_session_summary,
    suggest_waiting_time,
    calculate_drinks_to_limit,
    estimate_metabolism_time,
    categorize_bac,
    get_legal_limit,
    STANDARD_DRINK_GRAMS,
    LEGAL_LIMITS,
    DRINK_PRESETS,
)


def print_separator(title: str = ""):
    """Print a visual separator."""
    if title:
        print(f"\n{'='*60}")
        print(f" {title}")
        print(f"{'='*60}")
    else:
        print(f"\n{'─'*60}")


def example_basic_bac():
    """Example 1: Basic BAC calculation."""
    print_separator("Example 1: Basic BAC Calculation")
    
    # A 70kg male drinks 2 regular beers over 1 hour
    weight = 70  # kg
    gender = "male"
    drinks = [
        create_drink_from_preset("beer_regular"),
        create_drink_from_preset("beer_regular"),
    ]
    
    result = calculate_bac(weight, gender, drinks, hours_elapsed=1, country="us")
    
    print(f"\nPerson: {weight}kg {gender}")
    print(f"Drinks: 2 regular beers (355ml, 5% ABV each)")
    print(f"Time elapsed: 1 hour")
    print(f"\nResults:")
    print(f"  BAC: {result.bac:.3f}% ({result.bac_permille:.1f}‰)")
    print(f"  Category: {result.category}")
    print(f"  Impairment: {result.impairment_level}")
    print(f"  Legal to drive (US): {'Yes ✓' if result.is_legal else 'No ✗'}")
    print(f"  Time to sober: {result.time_to_sober:.1f} hours")
    print(f"  Time to legal limit: {result.time_to_legal:.1f} hours")


def example_different_drinks():
    """Example 2: Mixed drinks calculation."""
    print_separator("Example 2: Mixed Drinks Evening")
    
    # A 65kg female has a varied night
    weight = 65
    gender = "female"
    
    drinks = [
        create_drink_from_preset("wine_red"),
        create_drink_from_preset("wine_red"),
        create_drink_from_preset("cocktail_margarita"),
        create_drink_from_preset("spirits_vodka"),
    ]
    
    result = calculate_bac(weight, gender, drinks, hours_elapsed=3, country="us")
    
    print(f"\nPerson: {weight}kg {gender}")
    print(f"Drinks over 3 hours:")
    for i, drink_name in enumerate(["Red wine", "Red wine", "Margarita", "Vodka shot"], 1):
        print(f"  {i}. {drink_name}")
    
    print(f"\nResults:")
    print(f"  BAC: {result.bac:.3f}%")
    print(f"  Category: {result.category}")
    print(f"  Legal to drive: {'Yes ✓' if result.is_legal else 'No ✗'}")
    
    if not result.is_legal:
        wait = suggest_waiting_time(result.bac, result.legal_limit)
        print(f"  Wait until legal: {wait['human']}")


def example_legal_limits_comparison():
    """Example 3: Legal limits by country."""
    print_separator("Example 3: Legal Limits Comparison")
    
    # Same person, same drinks, different countries
    weight = 70
    gender = "male"
    drinks = [create_drink_from_preset("beer_regular") for _ in range(3)]
    
    countries = ["china", "japan", "germany", "us", "uk", "sweden"]
    
    print(f"\n70kg male, 3 beers, 1 hour elapsed:")
    print(f"\n{'Country':<12} {'Limit':<8} {'Your BAC':<10} {'Legal?':<8}")
    print("─" * 45)
    
    for country in countries:
        result = calculate_bac(weight, gender, drinks, hours_elapsed=1, country=country)
        status = "✓ Yes" if result.is_legal else "✗ No"
        print(f"{country:<12} {result.legal_limit:.2f}%     {result.bac:.3f}%     {status}")


def example_drinks_to_limit():
    """Example 4: How many drinks can I have?"""
    print_separator("Example 4: Drinks to Stay Legal")
    
    scenarios = [
        (70, "male", 0.08, 2),      # US, over 2 hours
        (70, "male", 0.05, 2),      # Germany, over 2 hours
        (60, "female", 0.08, 2),    # US female
        (60, "female", 0.02, 2),    # China female
    ]
    
    print("\nMaximum drinks to stay at or below legal limit:")
    print(f"\n{'Weight':<8} {'Gender':<8} {'Limit':<8} {'Hours':<8} {'Max Drinks':<12}")
    print("─" * 50)
    
    for weight, gender, limit, hours in scenarios:
        max_drinks = calculate_drinks_to_limit(weight, gender, limit, hours)
        print(f"{weight}kg      {gender:<8} {limit:.2f}%     {hours}h       {max_drinks} beers")


def example_quick_bac():
    """Example 5: Quick BAC check."""
    print_separator("Example 5: Quick BAC Check")
    
    scenarios = [
        ("Male, 75kg, 3 beers, 2h", 75, "male", 3, 2),
        ("Female, 55kg, 2 wines, 1h", 55, "female", 2, 1),
        ("Male, 80kg, 1 vodka, 0.5h", 80, "male", 1, 0.5),
    ]
    
    print("\nQuick BAC calculations:")
    for desc, weight, gender, drinks, hours in scenarios:
        bac = quick_bac(weight, gender, drinks, "beer_regular" if "beer" in desc.lower() else 
                       ("wine_red" if "wine" in desc.lower() else "spirits_vodka"), hours)
        category, impairment = categorize_bac(bac)
        print(f"\n  {desc}")
        print(f"    BAC: {bac:.3f}%")
        print(f"    Status: {category}")


def example_session_summary():
    """Example 6: Full drinking session summary."""
    print_separator("Example 6: Drinking Session Summary")
    
    drinks = [
        create_drink_from_preset("beer_regular"),
        create_drink_from_preset("beer_regular"),
        create_drink_from_preset("wine_red"),
        create_drink_from_preset("cocktail_mojito"),
    ]
    
    summary = drinking_session_summary(72, "male", drinks, country="us")
    
    print(f"\n👤 Person: 72kg male")
    print(f"🍹 Total drinks: {summary['drink_count']}")
    print(f"🍺 Alcohol consumed: {summary['total_alcohol_grams']}g ({summary['standard_drinks']} standard drinks)")
    print(f"\n📊 Results:")
    print(f"   BAC: {summary['bac_percent']:.3f}% ({summary['bac_permille']:.1f}‰)")
    print(f"   Category: {summary['category']}")
    print(f"   Impairment: {summary['impairment']}")
    print(f"\n🚗 Legal Status ({summary['country'].upper()}):")
    print(f"   Limit: {summary['legal_limit']:.2f}%")
    print(f"   Can drive: {'✓ Yes' if summary['is_legal'] else '✗ No'}")
    print(f"\n⏱️ Time Estimates:")
    print(f"   Time to legal: {summary['time_to_legal_hours']:.1f} hours")
    print(f"   Time to sober: {summary['time_to_sober_hours']:.1f} hours")
    print(f"\n⚠️ Recommendation: {summary['recommendation']}")


def example_waiting_time():
    """Example 7: When can I drive?"""
    print_separator("Example 7: When Can I Drive?")
    
    bac_levels = [0.05, 0.08, 0.10, 0.15]
    
    print("\nTime to reach different BAC targets:")
    print(f"\n{'Current BAC':<12} {'To 0.00%':<15} {'To 0.05%':<15} {'To 0.08%':<15}")
    print("─" * 60)
    
    for bac in bac_levels:
        to_zero = suggest_waiting_time(bac, 0.0)
        to_005 = suggest_waiting_time(bac, 0.05)
        to_008 = suggest_waiting_time(bac, 0.08)
        print(f"{bac:.2f}%         {to_zero['human']:<15} {to_005['human']:<15} {to_008['human']:<15}")


def example_metabolism_time():
    """Example 8: Alcohol metabolism time."""
    print_separator("Example 8: Alcohol Metabolism Time")
    
    alcohol_amounts = [14, 28, 42, 56]  # grams of alcohol
    
    print("\nTime to fully metabolize alcohol:")
    print(f"\n{'Alcohol':<15} {'Equivalent':<20} {'Male 70kg':<15} {'Female 55kg':<15}")
    print("─" * 65)
    
    for grams in alcohol_amounts:
        std_drinks = grams / 14
        male_time = estimate_metabolism_time(grams, 70, "male")
        female_time = estimate_metabolism_time(grams, 55, "female")
        equiv = f"~{std_drinks:.0f} standard drinks"
        print(f"{grams}g            {equiv:<20} {male_time:.1f}h            {female_time:.1f}h")


def example_widmark_vs_watson():
    """Example 9: Compare Widmark and Watson formulas."""
    print_separator("Example 9: Widmark vs Watson Formula")
    
    # Same person, different formulas
    drinks = [create_drink_from_preset("beer_regular") for _ in range(3)]
    
    print("\n70kg, 175cm, 30-year-old male, 3 beers, 2 hours elapsed:")
    print(f"\n{'Formula':<15} {'BAC':<10} {'Notes':<30}")
    print("─" * 55)
    
    result_widmark = calculate_bac(70, "male", drinks, hours_elapsed=2, method="widmark")
    print(f"{'Widmark':<15} {result_widmark.bac:.3f}%     {'Uses body weight only':<30}")
    
    result_watson = calculate_bac(70, "male", drinks, hours_elapsed=2, 
                                   height_cm=175, age=30, method="watson")
    print(f"{'Watson':<15} {result_watson.bac:.3f}%     {'Uses weight, height, age':<30}")
    
    print(f"\nDifference: {abs(result_widmark.bac - result_watson.bac):.4f}%")
    print("Note: Watson formula is generally more accurate as it accounts for body water.")


def example_drink_presets():
    """Example 10: Available drink presets."""
    print_separator("Example 10: Drink Presets")
    
    print("\nAvailable drink presets:\n")
    print(f"{'Name':<25} {'Volume':<12} {'ABV':<10} {'Alcohol':<10}")
    print("─" * 60)
    
    for name, preset in sorted(DRINK_PRESETS.items()):
        volume = preset["volume_ml"]
        abv = preset["alcohol_percent"]
        alcohol_g = volume * abv * 0.789
        print(f"{name:<25} {volume}ml        {abv*100:.1f}%       {alcohol_g:.1f}g")


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("  BLOOD ALCOHOL CONTENT (BAC) CALCULATOR - EXAMPLES")
    print("=" * 60)
    
    example_basic_bac()
    example_different_drinks()
    example_legal_limits_comparison()
    example_drinks_to_limit()
    example_quick_bac()
    example_session_summary()
    example_waiting_time()
    example_metabolism_time()
    example_widmark_vs_watson()
    example_drink_presets()
    
    print_separator()
    print("\n⚠️ DISCLAIMER: These calculations are estimates only.")
    print("   Individual metabolism varies. Never rely solely on calculations.")
    print("   When in doubt, don't drive!\n")


if __name__ == "__main__":
    main()