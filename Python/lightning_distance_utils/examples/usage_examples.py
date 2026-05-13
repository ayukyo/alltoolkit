"""
Lightning Distance Utils - Usage Examples

This module demonstrates how to use the lightning distance calculator
for various real-world scenarios.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from lightning_distance_utils.mod import (
    LightningDistanceCalculator,
    quick_distance,
    quick_distance_miles,
    rule_of_thumb_distance,
    estimate_thunder_arrival,
    get_safe_shelter_time,
    is_lightning_safe,
    thunder_volume_estimate,
    calculate_strike_angle,
    flash_to_bang_kilometers,
    flash_to_bang_miles,
    SafetyLevel
)


def example_basic_calculation():
    """Example 1: Basic lightning distance calculation"""
    print("\n" + "="*60)
    print("Example 1: Basic Lightning Distance Calculation")
    print("="*60)
    
    # Create calculator with default temperature (20°C)
    calc = LightningDistanceCalculator()
    
    # You saw lightning and counted 5 seconds until thunder
    time_delay = 5.0  # seconds
    result = calc.calculate_distance(time_delay)
    
    print(f"\n⚡ Lightning Strike Analysis")
    print(f"   Time delay: {result.time_delay_seconds} seconds")
    print(f"   Temperature: {result.temperature_celsius}°C")
    print(f"   Speed of sound: {result.speed_of_sound} m/s")
    print(f"\n📍 Distance:")
    print(f"   {result.distance_km} km ({result.distance_miles} miles)")
    print(f"   {result.distance_meters} meters ({result.distance_feet} feet)")
    print(f"\n⚠️ Safety Level: {result.safety_level.value.upper()}")
    print(f"   Dangerous: {'Yes' if result.is_dangerous else 'No'}")
    print(f"\n💡 Recommendation:")
    print(f"   {calc.get_safety_recommendation(result)}")


def example_temperature_effect():
    """Example 2: Temperature effect on distance calculation"""
    print("\n" + "="*60)
    print("Example 2: Temperature Effect on Distance")
    print("="*60)
    
    temperatures = [-10, 0, 10, 20, 30, 40]
    time_delay = 10.0  # seconds
    
    print(f"\nSame flash-to-bang time ({time_delay}s) at different temperatures:\n")
    print(f"{'Temp (°C)':<12} {'Speed (m/s)':<15} {'Distance (km)':<15} {'Difference'}")
    print("-" * 60)
    
    base_distance = None
    for temp in temperatures:
        calc = LightningDistanceCalculator(temp)
        result = calc.calculate_distance(time_delay)
        
        if base_distance is None:
            diff = "-"
            base_distance = result.distance_km
        else:
            diff = f"+{result.distance_km - base_distance:.2f} km"
        
        print(f"{temp:<12} {calc.speed_of_sound:<15.2f} {result.distance_km:<15.2f} {diff}")
    
    print("\n💡 Sound travels faster in warmer air, so the same time delay")
    print("   indicates a slightly greater distance at higher temperatures.")


def example_quick_calculations():
    """Example 3: Quick convenience functions"""
    print("\n" + "="*60)
    print("Example 3: Quick Convenience Functions")
    print("="*60)
    
    time_delays = [3, 5, 10, 15, 20, 30]
    
    print("\n⚡ Quick Distance Reference Table")
    print(f"\n{'Seconds':<10} {'Kilometers':<15} {'Miles':<15} {'Safety'}")
    print("-" * 55)
    
    for seconds in time_delays:
        km = quick_distance(seconds)
        miles = quick_distance_miles(seconds)
        
        if km < 3:
            safety = "🔴 IMMEDIATE"
        elif km < 6:
            safety = "🟠 DANGER"
        elif km < 10:
            safety = "🟡 CAUTION"
        elif km < 15:
            safety = "🟡 WATCH"
        else:
            safety = "🟢 SAFE"
        
        print(f"{seconds:<10} {km:<15.1f} {miles:<15.1f} {safety}")


def example_rule_of_thumb():
    """Example 4: Rule of thumb method"""
    print("\n" + "="*60)
    print("Example 4: Rule of Thumb Method")
    print("="*60)
    
    result = rule_of_thumb_distance(15.0)
    
    print(f"\n📊 For {result['time_seconds']} seconds delay:")
    print(f"   Rule of thumb distance: ~{result['rule_of_thumb_km']} km")
    print(f"   Rule of thumb distance: ~{result['rule_of_thumb_miles']} miles")
    print(f"\n💡 {result['explanation']}")
    
    print("\n🎯 Memory Aid:")
    print("   • Count seconds between flash and thunder")
    print("   • ÷ 3 = distance in kilometers")
    print("   • ÷ 5 = distance in miles")


def example_safety_assessment():
    """Example 5: Outdoor activity safety assessment"""
    print("\n" + "="*60)
    print("Example 5: Outdoor Activity Safety Assessment")
    print("="*60)
    
    activities = ["swimming", "hiking", "golf", "picnic", "sports"]
    distances = [2, 5, 8, 12, 18]
    
    print("\n🏃 Is it safe to continue outdoor activities?\n")
    
    for activity, distance in zip(activities, distances):
        is_safe, message = is_lightning_safe(activity, distance)
        status = "✅ SAFE" if is_safe else "❌ UNSAFE"
        print(f"\n{activity.upper()} at {distance} km:")
        print(f"   Status: {status}")
        print(f"   {message}")


def example_thunder_volume():
    """Example 6: Thunder volume estimation"""
    print("\n" + "="*60)
    print("Example 6: Thunder Volume Estimation")
    print("="*60)
    
    distances = [0.5, 1, 3, 5, 10, 15, 25]
    
    print("\n🔊 Expected thunder volume at different distances:\n")
    
    for dist in distances:
        volume = thunder_volume_estimate(dist)
        print(f"   {dist} km away: {volume}")


def example_storm_tracking():
    """Example 7: Storm tracking with multiple strikes"""
    print("\n" + "="*60)
    print("Example 7: Storm Tracking with Multiple Strikes")
    print("="*60)
    
    calc = LightningDistanceCalculator()
    
    print("\n📡 Tracking a storm over time:")
    print("   (Recording flash-to-bang times for consecutive strikes)\n")
    
    # Approaching storm
    approaching_strikes = [25, 22, 20, 18, 15, 12]
    
    print("Storm APPROACHING:")
    for i, delay in enumerate(approaching_strikes, 1):
        result = calc.calculate_distance(delay)
        print(f"   Strike {i}: {delay}s delay → {result.distance_km} km")
    
    analysis = calc.count_strikes(approaching_strikes)
    print(f"\n📊 Analysis:")
    print(f"   Total strikes: {analysis['total_strikes']}")
    print(f"   Average distance: {analysis['average_distance_km']} km")
    print(f"   Closest strike: {analysis['closest_strike_km']} km")
    print(f"   Storm approaching: {analysis['storm_approaching']}")
    print(f"   Safety level: {analysis['safety_level']}")
    
    # Receding storm
    print("\n" + "-"*40)
    print("Storm RECEEDING:")
    receding_strikes = [12, 15, 18, 22, 25, 30]
    
    for i, delay in enumerate(receding_strikes, 1):
        result = calc.calculate_distance(delay)
        print(f"   Strike {i}: {delay}s delay → {result.distance_km} km")
    
    analysis = calc.count_strikes(receding_strikes)
    print(f"\n📊 Analysis:")
    print(f"   Storm approaching: {analysis['storm_approaching']}")


def example_shelter_time():
    """Example 8: Time to seek shelter"""
    print("\n" + "="*60)
    print("Example 8: Time to Seek Shelter")
    print("="*60)
    
    distances = [5, 10, 15, 20, 30]
    
    print("\n⏱️ Estimated time to reach shelter before storm arrives:")
    print("   (Assuming typical thunderstorm speed of 40 km/h)\n")
    
    for dist in distances:
        minutes = get_safe_shelter_time(dist)
        thunder_time = estimate_thunder_arrival(dist)
        
        print(f"   Storm {dist} km away:")
        print(f"      Time to find shelter: ~{minutes:.0f} minutes")
        print(f"      Thunder arrival: {thunder_time:.1f} seconds after lightning")


def example_triangulation():
    """Example 9: Lightning strike location triangulation"""
    print("\n" + "="*60)
    print("Example 9: Lightning Strike Triangulation")
    print("="*60)
    
    print("\n📍 Using multiple observers to locate lightning strike:")
    print("   Observer 1: Position (0, 0), heard thunder after 17 seconds")
    print("   Observer 2: Position (10, 0), heard thunder after 17 seconds")
    
    time_delays = [17.0, 17.0]
    positions = [(0.0, 0.0), (10.0, 0.0)]
    
    result = calculate_strike_angle(time_delays, positions)
    
    if result:
        print(f"\n   Estimated strike location: ({result[0]} km, {result[1]} km)")
    else:
        print("\n   Could not calculate position (insufficient or invalid data)")


def example_30_30_rule():
    """Example 10: The 30-30 Rule"""
    print("\n" + "="*60)
    print("Example 10: The 30-30 Rule for Lightning Safety")
    print("="*60)
    
    print("""
    ┌─────────────────────────────────────────────────────────────┐
    │                    THE 30-30 RULE                          │
    ├─────────────────────────────────────────────────────────────┤
    │  SEEK SHELTER if:                                          │
    │    • Time between flash and thunder < 30 seconds           │
    │    • (Lightning is within ~10 km)                          │
    │                                                             │
    │  RESUME ACTIVITIES:                                        │
    │    • Wait 30 minutes after the LAST thunder                │
    │    • Even if rain has stopped                               │
    │                                                             │
    │  WHY? Lightning can strike 15+ km from the storm!         │
    └─────────────────────────────────────────────────────────────┘
    """)
    
    calc = LightningDistanceCalculator()
    
    # Demonstrate the 30-second threshold
    result = calc.calculate_distance(30.0)
    print(f"30 seconds delay = {result.distance_km} km away")
    
    if result.distance_km < 10:
        print("✓ Within danger zone - SEEK SHELTER!")
    
    print("\n💡 Key Facts:")
    print("   • Lightning can strike up to 15 km from a storm")
    print("   • 'Bolts from the blue' can occur in clear skies")
    print("   • When thunder roars, go indoors!")


def run_all_examples():
    """Run all examples"""
    print("\n" + "="*70)
    print("     ⚡ LIGHTNING DISTANCE CALCULATOR - USAGE EXAMPLES ⚡")
    print("="*70)
    
    example_basic_calculation()
    example_temperature_effect()
    example_quick_calculations()
    example_rule_of_thumb()
    example_safety_assessment()
    example_thunder_volume()
    example_storm_tracking()
    example_shelter_time()
    example_triangulation()
    example_30_30_rule()
    
    print("\n" + "="*70)
    print("     All examples completed! ⚡")
    print("="*70 + "\n")


if __name__ == "__main__":
    run_all_examples()