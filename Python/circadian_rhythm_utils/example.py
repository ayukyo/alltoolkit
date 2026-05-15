#!/usr/bin/env python3
"""
Example usage of Circadian Rhythm Utils.

This demonstrates how to use the library for:
1. Finding optimal wake times
2. Finding optimal bedtimes
3. Checking current alertness
4. Getting activity recommendations
5. Managing jet lag
6. Sleep debt analysis
"""

from datetime import datetime, time, timedelta
from circadian_rhythm import (
    CircadianRhythmCalculator,
    Chronotype,
    get_best_wake_times,
    get_best_bedtimes,
    get_current_alertness,
    format_duration,
)


def main():
    print("=" * 60)
    print("Circadian Rhythm Utils - Examples")
    print("=" * 60)
    
    # ========================================
    # Example 1: Find Optimal Wake Times
    # ========================================
    print("\n📅 Example 1: Find Optimal Wake Times")
    print("-" * 40)
    
    bedtime = datetime(2026, 5, 15, 23, 0)  # Going to bed at 11 PM
    print(f"Bedtime: {bedtime.strftime('%I:%M %p')}")
    print("\nRecommended wake times:")
    
    wake_options = get_best_wake_times(bedtime, Chronotype.INTERMEDIATE)
    for i, option in enumerate(wake_options, 1):
        print(f"  {i}. {option['wake_time']} - {option['duration']} sleep "
              f"(Quality: {option['quality']}%, {option['rem_cycles']} REM cycles)")
    
    # ========================================
    # Example 2: Find Optimal Bedtimes
    # ========================================
    print("\n\n📅 Example 2: Find Optimal Bedtimes")
    print("-" * 40)
    
    wake_time = datetime(2026, 5, 16, 7, 0)  # Need to wake up at 7 AM
    print(f"Target wake time: {wake_time.strftime('%I:%M %p')}")
    print("\nRecommended bedtimes:")
    
    bed_options = get_best_bedtimes(wake_time, Chronotype.INTERMEDIATE)
    for i, option in enumerate(bed_options, 1):
        print(f"  {i}. {option['bedtime']} - {option['duration']} sleep "
              f"(Quality: {option['quality']}%, {option['rem_cycles']} REM cycles)")
    
    # ========================================
    # Example 3: Current Alertness Level
    # ========================================
    print("\n\n⚡ Example 3: Current Alertness Level")
    print("-" * 40)
    
    alertness = get_current_alertness(Chronotype.INTERMEDIATE)
    print(f"Alertness Level: {alertness['alertness_level']}")
    print(f"Alertness Score: {alertness['alertness_score']}/100")
    print(f"Current Phase: {alertness['current_phase']}")
    print(f"Description: {alertness['phase_description']}")
    
    # ========================================
    # Example 4: Activity Recommendations
    # ========================================
    print("\n\n🏃 Example 4: Daily Activity Recommendations")
    print("-" * 40)
    
    calc = CircadianRhythmCalculator(Chronotype.INTERMEDIATE)
    recommendations = calc.get_activity_recommendations()
    
    print("Optimal schedule for today:\n")
    for rec in recommendations[:6]:  # Show first 6
        time_str = rec.time.strftime("%I:%M %p")
        print(f"  {time_str} - {rec.activity}")
        print(f"           {rec.reason}")
    
    # ========================================
    # Example 5: Chronotype Analysis
    # ========================================
    print("\n\n🦉 Example 5: Chronotype Analysis")
    print("-" * 40)
    
    # Compare different chronotypes at different times
    test_time = datetime(2026, 5, 15, 7, 0)  # 7 AM
    
    print(f"Alertness at {test_time.strftime('%I:%M %p')}:\n")
    
    for chronotype in Chronotype:
        calc_type = CircadianRhythmCalculator(chronotype)
        level, score = calc_type.get_alertness_at_time(test_time)
        phase = calc_type.get_current_phase(test_time)
        
        print(f"  {chronotype.value:15} - Score: {score:5.1f}/100, "
              f"Phase: {phase.name}")
    
    # ========================================
    # Example 6: Sleep Debt Impact
    # ========================================
    print("\n\n😴 Example 6: Sleep Debt Impact Analysis")
    print("-" * 40)
    
    hours_slept_options = [8, 7, 6, 5, 4]
    
    print("Impact of last night's sleep on today's performance:\n")
    
    for hours in hours_slept_options:
        impact = calc.get_sleep_debt_impact(hours)
        print(f"  {hours} hours sleep:")
        print(f"      Cognitive: {impact['cognitive_performance']:.0f}%  |  "
              f"Reaction: {impact['reaction_time']:.0f}%  |  "
              f"Overall: {impact['overall']:.0f}%")
    
    # ========================================
    # Example 7: Jet Lag Recovery
    # ========================================
    print("\n\n✈️ Example 7: Jet Lag Recovery")
    print("-" * 40)
    
    # Flying from LA to Tokyo (8 hours eastward)
    jet_lag = calc.get_jet_lag_recovery(8)
    
    print(f"Crossing {jet_lag['timezones_crossed']} time zones ({jet_lag['direction']})")
    print(f"Estimated recovery: {jet_lag['estimated_recovery_days']} days\n")
    print("Recommendations:")
    for rec in jet_lag['recommendations'][:4]:
        print(f"  • {rec}")
    
    # ========================================
    # Example 8: Nap Recommendation
    # ========================================
    print("\n\n💤 Example 8: Nap Recommendation")
    print("-" * 40)
    
    # After 6 hours of being awake, feeling tired
    nap_rec = calc.get_nap_recommendation(hours_since_sleep=6, current_energy=3)
    
    if nap_rec['should_nap']:
        print(f"Recommended nap duration: {nap_rec['optimal_duration']} minutes")
        print(f"Timing: {nap_rec['timing']}")
        print("\nBenefits:")
        for benefit in nap_rec['benefits']:
            print(f"  • {benefit}")
    else:
        print("Nap not recommended right now.")
        print(nap_rec['timing'])
    
    # ========================================
    # Example 9: Melatonin Schedule
    # ========================================
    print("\n\n🌙 Example 9: Melatonin Production Schedule")
    print("-" * 40)
    
    melatonin = calc.get_melatonin_schedule()
    
    print("Natural melatonin rhythm:\n")
    print(f"  Production starts:  {melatonin['production_start'][0].strftime('%I:%M %p')}")
    print(f"  Peak production:     {melatonin['peak_production'][0].strftime('%I:%M %p')}")
    print(f"  Decline begins:      {melatonin['decline_phase'][0].strftime('%I:%M %p')}")
    
    # ========================================
    # Example 10: Daily Alertness Curve
    # ========================================
    print("\n\n📈 Example 10: 24-Hour Alertness Curve")
    print("-" * 40)
    
    curve = calc.get_daily_alertness_curve()
    
    # Show key points
    print("Alertness throughout the day:\n")
    
    # Find peak and trough
    peak = max(curve, key=lambda x: x[1])
    trough = min(curve, key=lambda x: x[1])
    
    print(f"  Peak alertness:  {peak[0].strftime('%I:%M %p')} ({peak[1]:.1f}/100)")
    print(f"  Lowest alertness: {trough[0].strftime('%I:%M %p')} ({trough[1]:.1f}/100)")
    
    # Show hourly samples
    print("\n  Hourly breakdown:")
    for hour in range(24):
        t = curve[hour * 2]  # Every hour (30 min intervals)
        bar = "█" * int(t[1] / 10)
        print(f"    {t[0].strftime('%I %p'):>4}: {bar} {t[1]:.0f}")
    
    print("\n" + "=" * 60)
    print("Circadian Rhythm Utils Demo Complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()