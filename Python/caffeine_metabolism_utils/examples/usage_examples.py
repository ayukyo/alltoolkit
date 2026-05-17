"""
Caffeine Metabolism Utils - Usage Examples

This module demonstrates practical usage of the caffeine metabolism tracking tools.
"""

from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    CaffeineMetabolismTracker,
    calculate_caffeine_decay,
    calculate_half_life_from_data,
    estimate_caffeine_sensitivity,
    caffeine_equivalent,
    BEVERAGE_DATABASE
)


def example_basic_tracking():
    """Basic caffeine tracking throughout the day."""
    print("\n=== Basic Daily Tracking ===\n")
    
    tracker = CaffeineMetabolismTracker()
    now = datetime.now()
    
    # Morning coffee at 7 AM
    morning = now.replace(hour=7, minute=0, second=0, microsecond=0)
    tracker.consume_beverage("drip_coffee_medium", timestamp=morning)
    print(f"7:00 AM - Consumed drip coffee (medium): 165mg")
    
    # Second coffee at 10 AM
    ten_am = now.replace(hour=10, minute=0, second=0, microsecond=0)
    tracker.consume_beverage("espresso_double", timestamp=ten_am)
    print(f"10:00 AM - Consumed double espresso: 125mg")
    
    # Afternoon tea at 2 PM
    two_pm = now.replace(hour=14, minute=0, second=0, microsecond=0)
    tracker.consume_beverage("green_tea", timestamp=two_pm)
    print(f"2:00 PM - Consumed green tea: 28mg")
    
    # Check current status
    status = tracker.get_status()
    print(f"\nDaily Status:")
    print(f"  Total caffeine today: {status['daily_total_mg']}mg")
    print(f"  Within daily limit (400mg): {status['within_daily_limit']}")
    print(f"  Total entries: {status['total_entries']}")


def example_sleep_timing():
    """Calculate optimal sleep timing based on caffeine."""
    print("\n=== Sleep Timing Calculator ===\n")
    
    # Person with slower metabolism
    tracker = CaffeineMetabolismTracker(
        half_life_hours=6.0,  # Slower than average
        sleep_safe_threshold_mg=20
    )
    
    now = datetime.now()
    
    # Late afternoon coffee
    late_coffee = now.replace(hour=15, minute=30)
    tracker.consume_beverage("cold_brew_medium", timestamp=late_coffee)
    print(f"3:30 PM - Cold brew (medium): 300mg")
    
    # Check if safe to sleep at 10 PM
    ten_pm = now.replace(hour=22, minute=0)
    rec = tracker.get_sleep_recommendation(target_bedtime=ten_pm, from_time=late_coffee)
    
    print(f"\nBedtime Analysis (10 PM target):")
    print(f"  Caffeine at bedtime: {rec['bedtime_level_mg']}mg")
    print(f"  Safe to sleep: {'Yes ✓' if rec['is_safe_to_sleep'] else 'No ✗'}")
    print(f"  Time until safe: {rec['time_until_safe']}")
    print(f"  Recommended bedtime: {rec['recommended_bedtime']}")


def example_level_over_time():
    """Track caffeine level over the day."""
    print("\n=== Caffeine Level Timeline ===\n")
    
    tracker = CaffeineMetabolismTracker(half_life_hours=5.0)
    base = datetime.now().replace(hour=6, minute=0, second=0, microsecond=0)
    
    # Morning coffee
    tracker.consume(200, timestamp=base + timedelta(hours=1), source="morning_coffee")
    print("7:00 AM - Morning coffee: 200mg")
    
    # Check levels throughout the day
    times = [
        ("7:00 AM (immediate)", base + timedelta(hours=1)),
        ("8:00 AM (1hr after)", base + timedelta(hours=2)),
        ("12:00 PM (5hr after)", base + timedelta(hours=6)),
        ("5:00 PM (10hr after)", base + timedelta(hours=11)),
        ("10:00 PM (15hr after)", base + timedelta(hours=16)),
    ]
    
    print("\nCaffeine Levels:")
    for label, time in times:
        level = tracker.get_level_at(time)
        print(f"  {label}: {level:.1f}mg")


def example_multiple_beverages():
    """Track multiple beverage types."""
    print("\n=== Multiple Beverage Types ===\n")
    
    tracker = CaffeineMetabolismTracker()
    now = datetime.now()
    
    # List some interesting beverages
    beverages = [
        ("espresso_single", "Espresso (single)"),
        ("drip_coffee_medium", "Drip Coffee (medium)"),
        ("cold_brew_medium", "Cold Brew (medium)"),
        ("matcha", "Matcha"),
        ("red_bull_small", "Red Bull (small)"),
        ("monster_small", "Monster Energy"),
        ("coke_can", "Coca-Cola (can)"),
    ]
    
    print("Caffeine Content Comparison:")
    for key, name in beverages:
        mg = BEVERAGE_DATABASE[key]
        print(f"  {name}: {mg}mg")


def example_sensitivity_analysis():
    """Analyze caffeine sensitivity."""
    print("\n=== Caffeine Sensitivity Analysis ===\n")
    
    scenarios = [
        ("poor", 4, "Coffee at 6 PM, bed at 10 PM - couldn't sleep"),
        ("moderate", 6, "Coffee at 2 PM, bed at 8 PM - some difficulty"),
        ("good", 2, "Coffee at 8 PM, bed at 10 PM - slept fine"),
    ]
    
    for sleep_quality, hours, description in scenarios:
        result = estimate_caffeine_sensitivity(sleep_quality, hours)
        print(f"Scenario: {description}")
        print(f"  Sensitivity: {result['sensitivity']}")
        print(f"  Estimated half-life: {result['estimated_half_life']} hours")
        print(f"  Recommendation: {result['recommendation']}")
        print()


def example_caffeine_equivalents():
    """Calculate caffeine equivalents."""
    print("\n=== Caffeine Equivalents ===\n")
    
    amounts = [50, 100, 200, 300, 400]
    
    for mg in amounts:
        equiv = caffeine_equivalent(mg, "espresso_single")
        print(f"{mg}mg caffeine = {equiv['equivalent_units']} espressos")
        
        # Show closest beverage
        closest = equiv['closest_beverages'][0]
        print(f"  Closest match: {closest['name']} ({closest['caffeine_mg']}mg)")


def example_custom_metabolism():
    """Example with custom metabolism parameters."""
    print("\n=== Custom Metabolism Parameters ===\n")
    
    # Person who knows their half-life is longer (maybe on oral contraceptives)
    tracker = CaffeineMetabolismTracker(
        half_life_hours=7.0,  # Extended half-life
        sleep_safe_threshold_mg=15  # More sensitive to caffeine
    )
    
    now = datetime.now()
    tracker.consume_beverage("latte_medium", timestamp=now)
    print(f"Consumed latte (medium): 95mg")
    print(f"Your metabolism: {tracker.half_life_hours}hr half-life")
    print(f"Your safe threshold: {tracker.sleep_safe_threshold_mg}mg")
    
    time_safe = tracker.time_until_threshold()
    print(f"Time until safe to sleep: {time_safe}")


def example_decay_calculation():
    """Simple decay calculation examples."""
    print("\n=== Caffeine Decay Calculations ===\n")
    
    initial = 200  # mg
    
    print(f"Starting with {initial}mg of caffeine:")
    for hours in [0, 1, 2, 5, 10, 15, 20]:
        remaining = calculate_caffeine_decay(initial, hours, 5.0)
        print(f"  After {hours:2d} hours: {remaining:.1f}mg remaining")


def example_half_life_estimation():
    """Calculate personal half-life from observations."""
    print("\n=== Personal Half-Life Estimation ===\n")
    
    # If you measured your caffeine levels (e.g., through a blood test or app)
    initial = 150  # mg
    after_6_hours = 68  # mg
    
    try:
        half_life = calculate_half_life_from_data(initial, after_6_hours, 6)
        print(f"If {initial}mg drops to {after_6_hours}mg after 6 hours:")
        print(f"  Your estimated half-life: {half_life:.1f} hours")
        
        # Interpret
        if half_life < 4:
            interpretation = "Fast metabolizer - caffeine clears quickly"
        elif half_life < 6:
            interpretation = "Normal metabolism"
        else:
            interpretation = "Slow metabolizer - caffeine stays in system longer"
        print(f"  Interpretation: {interpretation}")
    except ValueError as e:
        print(f"Error: {e}")


def example_daily_limit_monitoring():
    """Monitor daily caffeine against recommended limits."""
    print("\n=== Daily Limit Monitoring ===\n")
    
    tracker = CaffeineMetabolismTracker()
    now = datetime.now()
    
    drinks = [
        (7, "drip_coffee_large"),
        (10, "espresso_double"),
        (14, "coke_can"),
        (16, "green_tea"),
    ]
    
    total = 0
    for hour, beverage in drinks:
        mg = BEVERAGE_DATABASE[beverage]
        total += mg
        time = now.replace(hour=hour, minute=0, second=0, microsecond=0)
        tracker.consume_beverage(beverage, timestamp=time)
        print(f"{hour}:00 - {beverage}: {mg}mg (running total: {total}mg)")
    
    status = tracker.get_status()
    print(f"\nDaily Summary:")
    print(f"  Total caffeine: {status['daily_total_mg']}mg")
    print(f"  FDA recommended max: {status['max_daily_recommended_mg']}mg")
    
    percentage = (status['daily_total_mg'] / status['max_daily_recommended_mg']) * 100
    print(f"  Daily limit usage: {percentage:.0f}%")
    print(f"  Within limits: {'Yes ✓' if status['within_daily_limit'] else 'No ✗'}")


def example_export_import():
    """Save and restore caffeine log."""
    print("\n=== Data Export/Import ===\n")
    
    # Create tracker with some data
    tracker1 = CaffeineMetabolismTracker()
    now = datetime.now()
    
    tracker1.consume_beverage("drip_coffee_medium", timestamp=now - timedelta(hours=5))
    tracker1.consume_beverage("espresso_single", timestamp=now - timedelta(hours=2))
    
    # Export
    data = tracker1.export_data()
    print(f"Exported {len(data)} entries")
    
    # Import into new tracker
    tracker2 = CaffeineMetabolismTracker()
    imported = tracker2.import_data(data)
    print(f"Imported {imported} entries")
    
    # Verify
    print(f"Tracker 1 current level: {tracker1.get_current_level():.1f}mg")
    print(f"Tracker 2 current level: {tracker2.get_current_level():.1f}mg")


def main():
    """Run all examples."""
    print("=" * 60)
    print("Caffeine Metabolism Utils - Usage Examples")
    print("=" * 60)
    
    example_basic_tracking()
    example_sleep_timing()
    example_level_over_time()
    example_multiple_beverages()
    example_sensitivity_analysis()
    example_caffeine_equivalents()
    example_custom_metabolism()
    example_decay_calculation()
    example_half_life_estimation()
    example_daily_limit_monitoring()
    example_export_import()
    
    print("\n" + "=" * 60)
    print("Examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()