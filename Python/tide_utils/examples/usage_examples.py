"""
Tide Utils - Usage Examples

This module demonstrates how to use the tide prediction and calculation
utilities for various real-world scenarios including fishing, navigation,
and coastal activities.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from tide_utils.mod import (
    TideCalculator,
    TideType,
    TidePhase,
    create_semidiurnal_tides,
    create_mixed_tides,
    create_diurnal_tides,
    quick_tide_height,
    is_good_fishing_time,
    get_tide_table,
    calculate_tide_window,
    get_tide_calculator_for_location,
)
from datetime import datetime, timedelta


def example_basic_tide_calculation():
    """Example 1: Basic tide height calculation"""
    print("\n" + "="*60)
    print("Example 1: Basic Tide Height Calculation")
    print("="*60)
    
    # Create a default tide calculator
    calc = TideCalculator()
    
    # Calculate tide height at a specific time
    dt = datetime(2024, 6, 15, 12, 0, 0)
    height = calc.calculate_tide_height(dt)
    
    print(f"\n🌊 Tide Height at {dt.strftime('%Y-%m-%d %H:%M')}")
    print(f"   Height: {height:.3f} meters")
    print(f"   Above mean sea level: {'Yes' if height > 0 else 'No'}")
    
    # Show variation over 6 hours
    print(f"\n📊 Tide heights over the next 6 hours:")
    for hour in range(7):
        test_dt = dt + timedelta(hours=hour)
        h = calc.calculate_tide_height(test_dt)
        bar = "█" * int(abs(h) * 10)
        print(f"   {test_dt.strftime('%H:%M')}: {h:+.2f}m {bar}")


def example_tide_prediction():
    """Example 2: Complete tide prediction"""
    print("\n" + "="*60)
    print("Example 2: Complete Tide Prediction")
    print("="*60)
    
    calc = TideCalculator()
    dt = datetime(2024, 6, 15, 14, 30, 0)
    
    prediction = calc.get_prediction(dt)
    
    print(f"\n📅 Tide Prediction for {prediction.datetime.strftime('%Y-%m-%d %H:%M')}")
    print(f"\n   Height: {prediction.height:.2f} meters")
    print(f"   Phase: {prediction.phase.value.upper()}")
    print(f"   Type: {prediction.tide_type.value.upper()}")
    
    if prediction.next_high:
        print(f"\n   Next High Tide: {prediction.next_high.strftime('%H:%M')}")
    if prediction.next_low:
        print(f"   Next Low Tide: {prediction.next_low.strftime('%H:%M')}")
    
    print(f"   Time to next tide: {prediction.time_to_next}")
    print(f"   Height change rate: {prediction.height_change_rate:.2f} m/hour")


def example_lunar_cycle():
    """Example 3: Lunar cycle and tide types"""
    print("\n" + "="*60)
    print("Example 3: Lunar Cycle and Tide Types")
    print("="*60)
    
    calc = TideCalculator()
    
    # Reference new moon (January 6, 2000)
    new_moon = datetime(2000, 1, 6, 18, 14, 0)
    
    print("\n🌙 Lunar Cycle Effects on Tides\n")
    print(f"{'Day':<6} {'Lunar Age':<12} {'Phase':<18} {'Tide Type':<10}")
    print("-" * 50)
    
    for day in [0, 3, 7, 10, 14, 18, 22, 26]:
        dt = new_moon + timedelta(days=day)
        lunar_age = calc.get_lunar_age(dt)
        phase = calc.get_lunar_phase_name(dt)
        tide_type = calc.get_tide_type(dt).value
        
        print(f"{day:<6} {lunar_age:<12.1f} {phase:<18} {tide_type:<10}")
    
    print("\n💡 Key Points:")
    print("   • Spring tides: Higher highs, lower lows (full/new moon)")
    print("   • Neap tides: Lower highs, higher lows (quarter moons)")
    print("   • Spring tides occur ~every 14 days")


def example_find_tide_events():
    """Example 4: Finding high and low tides"""
    print("\n" + "="*60)
    print("Example 4: Finding High and Low Tides")
    print("="*60)
    
    calc = TideCalculator()
    dt = datetime(2024, 6, 15, 8, 0, 0)
    
    print(f"\n🔍 Finding tide events after {dt.strftime('%H:%M')}\n")
    
    # Find next high tide
    high = calc.find_next_high_tide(dt)
    if high:
        print(f"   Next HIGH tide:")
        print(f"      Time: {high.time.strftime('%Y-%m-%d %H:%M')}")
        print(f"      Height: {high.height:.2f} meters")
        print(f"      Type: {high.tide_type.value}")
    
    # Find next low tide
    low = calc.find_next_low_tide(dt)
    if low:
        print(f"\n   Next LOW tide:")
        print(f"      Time: {low.time.strftime('%Y-%m-%d %H:%M')}")
        print(f"      Height: {low.height:.2f} meters")
        print(f"      Type: {low.tide_type.value}")


def example_tide_table():
    """Example 5: Generating a tide table"""
    print("\n" + "="*60)
    print("Example 5: Tide Table Generation")
    print("="*60)
    
    calc = create_semidiurnal_tides(mean_high=2.0, mean_low=-0.5)
    dt = datetime(2024, 6, 15, 0, 0, 0)
    
    print(f"\n📅 Tide Table for June 15-16, 2024\n")
    
    table = get_tide_table(dt, days=2, calculator=calc)
    
    print(f"{'Date':<12} {'Time':<8} {'Height':<10} {'Type':<8} {'Lunar':<15}")
    print("-" * 60)
    
    for entry in table:
        print(f"{entry['date']:<12} {entry['time']:<8} {entry['height_m']:>6.2f}m   "
              f"{entry['type']:<8} {entry['lunar_phase']:<15}")
    
    print(f"\n📊 Total events: {len(table)}")


def example_tidal_patterns():
    """Example 6: Different tidal patterns"""
    print("\n" + "="*60)
    print("Example 6: Different Tidal Patterns")
    print("="*60)
    
    print("\n🌊 Comparing different tidal patterns:\n")
    
    # Semidiurnal (Atlantic coast style)
    calc_semi = create_semidiurnal_tides(mean_high=2.5, mean_low=-0.5)
    
    # Mixed (Pacific coast style)
    calc_mixed = create_mixed_tides(mean_high=2.5, mean_low=-0.5)
    
    # Diurnal (Gulf of Mexico style)
    calc_diurnal = create_diurnal_tides(mean_high=2.5, mean_low=-0.5)
    
    dt = datetime(2024, 6, 15, 0, 0, 0)
    
    print(f"{'Hour':<6} {'Semidiurnal':<15} {'Mixed':<15} {'Diurnal':<15}")
    print("-" * 55)
    
    for hour in range(0, 25, 3):
        test_dt = dt + timedelta(hours=hour)
        h_semi = calc_semi.calculate_tide_height(test_dt)
        h_mixed = calc_mixed.calculate_tide_height(test_dt)
        h_diurnal = calc_diurnal.calculate_tide_height(test_dt)
        
        print(f"{hour:<6} {h_semi:>6.2f}m        {h_mixed:>6.2f}m        {h_diurnal:>6.2f}m")
    
    print("\n💡 Pattern differences:")
    print("   • Semidiurnal: Two similar highs/lows per day (Atlantic)")
    print("   • Mixed: Two highs/lows with different heights (Pacific)")
    print("   • Diurnal: One high and one low per day (some areas)")


def example_fishing_times():
    """Example 7: Best fishing times"""
    print("\n" + "="*60)
    print("Example 7: Best Fishing Times Based on Tides")
    print("="*60)
    
    calc = TideCalculator()
    dt = datetime(2024, 6, 15, 6, 0, 0)
    
    print(f"\n🎣 Fishing Time Assessment for June 15, 2024\n")
    
    for hour in [6, 8, 10, 12, 14, 16, 18, 20]:
        test_dt = dt + timedelta(hours=hour)
        is_good, reason = is_good_fishing_time(test_dt, calc)
        
        status = "✅ GOOD" if is_good else "❌ SLOW"
        print(f"   {test_dt.strftime('%H:%M')}: {status}")
        print(f"      {reason}")
    
    print("\n💡 Fishing Tips:")
    print("   • Best during moving tides (rising or falling)")
    print("   • Fish often feed near tide changes")
    print("   • Spring tides bring stronger currents and more activity")


def example_tidal_current():
    """Example 8: Tidal current estimation"""
    print("\n" + "="*60)
    print("Example 8: Tidal Current Estimation")
    print("="*60)
    
    calc = TideCalculator()
    dt = datetime(2024, 6, 15, 0, 0, 0)
    
    print("\n🌊 Tidal Current Strength Throughout the Day\n")
    
    for hour in range(0, 25, 2):
        test_dt = dt + timedelta(hours=hour)
        direction, speed = calc.estimate_tidal_current(test_dt)
        
        # Visual representation
        if direction == "slack":
            bars = "○"
        elif direction == "flood":
            bars = "→" * int(speed * 5)
        elif direction == "ebb":
            bars = "←" * int(speed * 5)
        else:
            bars = "?"
        
        print(f"   {test_dt.strftime('%H:%M')}: {direction:>6} [{speed:.2f}] {bars}")
    
    print("\n💡 Current facts:")
    print("   • Currents strongest at mid-tide")
    print("   • Slack water at high and low tide extremes")
    print("   • Flood = incoming tide, Ebb = outgoing tide")


def example_tide_window():
    """Example 9: Navigation tide window"""
    print("\n" + "="*60)
    print("Example 9: Navigation Tide Window")
    print("="*60)
    
    # Create a calculator for an area with 3m tidal range
    calc = create_semidiurnal_tides(mean_high=3.0, mean_low=-3.0)
    
    # Boat needs at least 1.5m depth to navigate
    min_depth = 1.5
    dt = datetime(2024, 6, 15, 6, 0, 0)
    
    print(f"\n⛵ Navigation Window Calculation")
    print(f"   Minimum required depth: {min_depth} meters\n")
    
    start, end = calculate_tide_window(dt, calc, min_depth)
    
    if start and end:
        duration = (end - start).total_seconds() / 3600
        print(f"   Safe navigation window:")
        print(f"      Start: {start.strftime('%H:%M')}")
        print(f"      End: {end.strftime('%H:%M')}")
        print(f"      Duration: {duration:.1f} hours")
        
        print(f"\n   Tide heights during window:")
        current = start
        while current <= end:
            height = calc.calculate_tide_height(current)
            print(f"      {current.strftime('%H:%M')}: {height:.2f}m ✓")
            current += timedelta(hours=1)
    else:
        print("   No safe navigation window found in next 24 hours")
    
    print("\n💡 Navigation tip:")
    print("   • Always check official tide tables for navigation")
    print("   • This calculation is for planning only")


def example_spring_vs_neap():
    """Example 10: Spring vs Neap tide comparison"""
    print("\n" + "="*60)
    print("Example 10: Spring vs Neap Tide Comparison")
    print("="*60)
    
    calc = TideCalculator()
    
    # New moon (spring tide)
    spring_date = datetime(2000, 1, 6, 18, 14, 0)
    
    # First quarter (neap tide)
    neap_date = spring_date + timedelta(days=7)
    
    print("\n🌊 Spring vs Neap Tide Heights\n")
    
    print("SPRING TIDE (New Moon):")
    print(f"{'Hour':<6} {'Height':<10} {'Level'}")
    for hour in range(0, 13, 2):
        dt = spring_date + timedelta(hours=hour)
        height = calc.calculate_tide_height(dt)
        level = "High" if height > 0.7 else "Low" if height < -0.7 else "Mid"
        bar = "█" * int(abs(height) * 5)
        print(f"{hour:<6} {height:>6.2f}m   {level:<4} {bar}")
    
    print("\nNEAP TIDE (First Quarter):")
    print(f"{'Hour':<6} {'Height':<10} {'Level'}")
    for hour in range(0, 13, 2):
        dt = neap_date + timedelta(hours=hour)
        height = calc.calculate_tide_height(dt)
        level = "High" if height > 0.7 else "Low" if height < -0.7 else "Mid"
        bar = "█" * int(abs(height) * 5)
        print(f"{hour:<6} {height:>6.2f}m   {level:<4} {bar}")
    
    print("\n💡 Differences:")
    print("   • Spring tides have larger tidal range")
    print("   • Neap tides have smaller tidal range")
    print("   • Difference caused by moon-sun alignment")


def example_tidal_coefficient():
    """Example 11: Tidal coefficient (French system)"""
    print("\n" + "="*60)
    print("Example 11: Tidal Coefficient System")
    print("="*60)
    
    calc = TideCalculator()
    
    print("\n📊 Tidal Coefficient Throughout Lunar Month\n")
    print(f"{'Day':<6} {'Lunar Phase':<18} {'Coefficient':<12} {'Intensity'}")
    print("-" * 55)
    
    new_moon = datetime(2000, 1, 6, 18, 14, 0)
    
    for day in range(0, 30, 2):
        dt = new_moon + timedelta(days=day)
        phase = calc.get_lunar_phase_name(dt)
        coeff = calc.get_tidal_coefficient(dt)
        
        if coeff >= 90:
            intensity = "🔴 Very Strong"
        elif coeff >= 70:
            intensity = "🟠 Strong"
        elif coeff >= 50:
            intensity = "🟡 Moderate"
        else:
            intensity = "🟢 Weak"
        
        print(f"{day:<6} {phase:<18} {coeff:<12.0f} {intensity}")
    
    print("\n💡 Coefficient meaning:")
    print("   • 95-120: Very strong spring tide")
    print("   • 70-90: Average tide")
    print("   • 45-70: Moderate tide")
    print("   • 20-45: Weak neap tide")


def example_real_time_check():
    """Example 12: Real-time tide check"""
    print("\n" + "="*60)
    print("Example 12: Real-Time Tide Check (Current Status)")
    print("="*60)
    
    calc = create_semidiurnal_tides(mean_high=1.8, mean_low=-0.3)
    
    # Simulate current time
    now = datetime(2024, 6, 15, 14, 0, 0)
    
    prediction = calc.get_prediction(now)
    
    print(f"\n📍 Current Tide Status at {now.strftime('%H:%M')}\n")
    
    print(f"   Current Height: {prediction.height:.2f} meters")
    print(f"   Current Phase: {prediction.phase.value.upper()}")
    print(f"   Tide Type: {prediction.tide_type.value.upper()}")
    
    print(f"\n   ⏰ Upcoming Events:")
    if prediction.next_high:
        high_height = calc.calculate_tide_height(prediction.next_high)
        print(f"      High Tide: {prediction.next_high.strftime('%H:%M')} "
              f"(height: {high_height:.2f}m)")
    
    if prediction.next_low:
        low_height = calc.calculate_tide_height(prediction.next_low)
        print(f"      Low Tide: {prediction.next_low.strftime('%H:%M')} "
              f"(height: {low_height:.2f}m)")
    
    print(f"\n   🌊 Rate of Change: {abs(prediction.height_change_rate):.2f} m/hour")
    
    # Direction arrow
    if prediction.phase == TidePhase.RISING:
        arrow = "↑ Rising"
    elif prediction.phase == TidePhase.FALLING:
        arrow = "↓ Falling"
    else:
        arrow = "○ Slack"
    
    print(f"   Direction: {arrow}")
    
    # Current strength
    direction, speed = calc.estimate_tidal_current(now)
    print(f"\n   💨 Tidal Current: {direction} (strength: {speed:.0%})")


def run_all_examples():
    """Run all examples"""
    print("\n" + "="*70)
    print("     🌊 TIDE PREDICTION UTILITIES - USAGE EXAMPLES 🌊")
    print("="*70)
    
    example_basic_tide_calculation()
    example_tide_prediction()
    example_lunar_cycle()
    example_find_tide_events()
    example_tide_table()
    example_tidal_patterns()
    example_fishing_times()
    example_tidal_current()
    example_tide_window()
    example_spring_vs_neap()
    example_tidal_coefficient()
    example_real_time_check()
    
    print("\n" + "="*70)
    print("     All examples completed! 🌊")
    print("="*70 + "\n")


if __name__ == "__main__":
    run_all_examples()