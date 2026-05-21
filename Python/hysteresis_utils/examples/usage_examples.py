#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Hysteresis Utilities Usage Examples
=================================================
Practical examples demonstrating hysteresis utilities.

Author: AllToolkit Contributors
License: MIT
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    Hysteresis,
    SchmittTrigger,
    DeadZone,
    HysteresisFilter,
    MultiLevelHysteresis,
    HysteresisStateMachine,
    Thermostat,
    create_thermostat,
    create_alarm,
    debounce_signal,
    detect_edges_with_hysteresis,
)


def example_thermostat_control():
    """Example 1: Thermostat Control System."""
    print("\n" + "=" * 60)
    print("Example 1: Thermostat Control System")
    print("=" * 60)
    
    # Create a thermostat that:
    # - Turns heating ON when temperature drops below 18°C
    # - Turns heating OFF when temperature rises above 22°C
    thermostat = create_thermostat(heat_on=18.0, heat_off=22.0)
    
    print(f"\nThermostat Configuration:")
    print(f"  - Heat ON threshold: 18°C (turns ON when temp < 18)")
    print(f"  - Heat OFF threshold: 22°C (turns OFF when temp > 22)")
    print(f"  - Hysteresis gap: {thermostat.hysteresis_gap}°C")
    
    # Simulate temperature changes
    temperatures = [20, 19, 18, 17, 16, 18, 20, 22, 23, 21, 19, 17]
    
    print("\nTemperature Simulation:")
    print("-" * 40)
    for temp in temperatures:
        heating_state = thermostat.update(temp)
        state_str = "HEATING ON" if heating_state else "HEATING OFF"
        print(f"  Temp: {temp}°C → {state_str}")
    
    print(f"\nStatistics:")
    print(f"  - Total updates: {thermostat.stats.total_updates}")
    print(f"  - State changes: {thermostat.stats.state_changes}")
    print(f"  - Time heating ON: {thermostat.stats.time_in_high}")
    print(f"  - Time heating OFF: {thermostat.stats.time_in_low}")


def example_alarm_system():
    """Example 2: Industrial Alarm System."""
    print("\n" + "=" * 60)
    print("Example 2: Industrial Alarm System")
    print("=" * 60)
    
    # Create an alarm that:
    # - Triggers when pressure exceeds 80 PSI
    # - Resets when pressure drops below 60 PSI
    alarm = create_alarm(trigger_threshold=80.0, reset_threshold=60.0)
    
    print(f"\nAlarm Configuration:")
    print(f"  - Trigger threshold: 80 PSI")
    print(f"  - Reset threshold: 60 PSI")
    print(f"  - Hysteresis: prevents false alarms between 60-80 PSI")
    
    # Simulate pressure readings (with noise)
    pressures = [50, 55, 60, 65, 70, 75, 80, 85, 78, 72, 65, 58, 52]
    
    print("\nPressure Monitoring:")
    print("-" * 40)
    for pressure in pressures:
        alarm_state = alarm.update(pressure)
        state_str = "⚠️ ALARM ACTIVE" if alarm_state else "✓ NORMAL"
        print(f"  Pressure: {pressure} PSI → {state_str}")
    
    print(f"\nAlarm Statistics:")
    print(f"  - Triggered {alarm.stats.rising_edges} times")
    print(f"  - Reset {alarm.stats.falling_edges} times")


def example_schmitt_trigger():
    """Example 3: Schmitt Trigger for Signal Conditioning."""
    print("\n" + "=" * 60)
    print("Example 3: Schmitt Trigger for Signal Conditioning")
    print("=" * 60)
    
    # Create a Schmitt trigger for converting analog to digital
    trigger = SchmittTrigger(low_threshold=0.4, high_threshold=0.6)
    
    print("\nSchmitt Trigger Configuration:")
    print("  - Low threshold: 0.4")
    print("  - High threshold: 0.6")
    print("  - Converts noisy analog signal to clean digital output")
    
    # Simulate a noisy analog signal
    analog_signal = [0.0, 0.2, 0.4, 0.5, 0.6, 0.7, 0.55, 0.45, 0.35, 0.5, 0.65, 0.8]
    digital_output = trigger.process(analog_signal)
    
    print("\nSignal Conversion:")
    print("-" * 40)
    print("  Input → Output")
    for i, (analog, digital) in enumerate(zip(analog_signal, digital_output)):
        output_str = "HIGH (1)" if digital else "LOW (0)"
        print(f"  {analog:.2f} → {output_str}")
    
    print("\nBenefit: Noise immunity between 0.4 and 0.6 thresholds")


def example_dead_zone():
    """Example 4: Dead Zone for Noise Filtering."""
    print("\n" + "=" * 60)
    print("Example 4: Dead Zone for Noise Filtering")
    print("=" * 60)
    
    # Create a dead zone around zero for ±0.5
    dz = DeadZone(size=0.5, center=0.0)
    
    print("\nDead Zone Configuration:")
    print(f"  - Size: ±{dz.size}")
    print(f"  - Center: {dz.center}")
    print(f"  - Boundaries: [{dz.boundaries[0]}, {dz.boundaries[1]}]")
    print("  - Values in dead zone → 0")
    
    # Simulate noisy sensor readings near zero
    readings = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, -0.3, -0.6]
    
    print("\nSensor Reading Processing:")
    print("-" * 40)
    for reading in readings:
        processed = dz.process(reading)
        in_zone = dz.in_dead_zone(reading)
        status = "in dead zone" if in_zone else "outside"
        print(f"  {reading:.1f} → {processed:.1f} ({status})")


def example_multi_level_hysteresis():
    """Example 5: Multi-Level Battery Indicator."""
    print("\n" + "=" * 60)
    print("Example 5: Multi-Level Battery Indicator")
    print("=" * 60)
    
    # Create a battery level indicator with 4 levels
    # Levels: 0 (Empty), 1 (Low), 2 (Medium), 3 (Full)
    battery = MultiLevelHysteresis(
        thresholds=[20, 50, 80],  # Percentage thresholds
        hysteresis=5              # 5% hysteresis to prevent jitter
    )
    
    level_names = ["Empty", "Low", "Medium", "Full"]
    
    print("\nBattery Level Configuration:")
    print("  - Thresholds: 20%, 50%, 80%")
    print("  - Hysteresis: 5% (prevents rapid level changes)")
    print(f"  - Levels: {battery.num_levels}")
    
    # Simulate battery draining and charging
    percentages = [100, 85, 70, 55, 40, 25, 10, 30, 60, 90]
    
    print("\nBattery Level Simulation:")
    print("-" * 40)
    for pct in percentages:
        level = battery.update(pct)
        level_name = level_names[level]
        print(f"  Battery: {pct}% → Level {level} ({level_name})")
    
    print("\nApplication: Prevents display flickering between levels")


def example_state_machine():
    """Example 6: Temperature State Machine."""
    print("\n" + "=" * 60)
    print("Example 6: Temperature State Machine")
    print("=" * 60)
    
    # Create a state machine for temperature zones
    sm = HysteresisStateMachine()
    
    sm.add_state("cold", enter_below=15, exit_above=18)
    sm.add_state("comfortable", enter_above=15, enter_below=25, 
                 exit_above=28, exit_below=12)
    sm.add_state("hot", enter_above=28, exit_below=25)
    
    print("\nState Machine Configuration:")
    print("  States: cold, comfortable, hot")
    print("  - Cold: enter <15°C, exit >18°C")
    print("  - Comfortable: enter 15-25°C, exit <12°C or >28°C")
    print("  - Hot: enter >28°C, exit <25°C")
    
    # Simulate temperature changes over a day
    temps = [
        (8, 10),   # Morning - cold
        (10, 16),  # Getting warmer
        (12, 22),  # Noon - comfortable
        (14, 30),  # Afternoon - hot
        (16, 26),  # Cooling down (hysteresis keeps it hot)
        (18, 20),  # Evening - comfortable
        (20, 14),  # Night - cold
    ]
    
    print("\nDaily Temperature Cycle:")
    print("-" * 40)
    for time, temp in temps:
        state = sm.update(temp)
        print(f"  {time:02d}:00 - {temp}°C → {state}")


def example_signal_filtering():
    """Example 7: Signal Filtering with Hysteresis."""
    print("\n" + "=" * 60)
    print("Example 7: Signal Filtering with Hysteresis")
    print("=" * 60)
    
    # Create a hysteresis filter for noisy data
    filter = HysteresisFilter(threshold=2.0)
    
    print("\nFilter Configuration:")
    print("  - Threshold: 2.0 (minimum change to update output)")
    print("  - Purpose: Smooth noisy signal data")
    
    # Simulate noisy temperature readings
    noisy_signal = [20.0, 20.5, 21.0, 20.8, 21.2, 25.0, 25.5, 24.8, 25.2, 20.0]
    filtered_signal = filter.filter(noisy_signal)
    
    print("\nSignal Filtering:")
    print("-" * 40)
    print("  Raw → Filtered")
    for raw, filt in zip(noisy_signal, filtered_signal):
        changed = "changed" if raw != filt else "unchanged"
        print(f"  {raw:.1f} → {filt:.1f} ({changed})")
    
    # Count actual changes
    changes = sum(1 for i in range(1, len(filtered_signal)) 
                  if filtered_signal[i] != filtered_signal[i-1])
    print(f"\nOriginal signal changes: {len(noisy_signal)-1}")
    print(f"Filtered signal changes: {changes}")


def example_edge_detection():
    """Example 8: Edge Detection with Hysteresis."""
    print("\n" + "=" * 60)
    print("Example 8: Edge Detection with Hysteresis")
    print("=" * 60)
    
    # Simulate a noisy signal
    signal = [10, 12, 15, 18, 20, 22, 25, 23, 21, 19, 17, 15, 13, 11, 14, 18, 22, 26]
    
    # Detect edges with hysteresis (thresholds 18 and 22)
    edges = detect_edges_with_hysteresis(signal, low_threshold=18, high_threshold=22)
    
    print("\nSignal Analysis:")
    print("-" * 40)
    print(f"  Signal values: {signal}")
    
    print("\nDetected Edges:")
    print("-" * 40)
    for idx, edge_type in edges:
        value = signal[idx]
        edge_symbol = "⬆️ Rising" if edge_type == "rising" else "⬇️ Falling"
        print(f"  Index {idx} (value: {value}): {edge_symbol} edge")
    
    print("\nBenefit: Hysteresis prevents false edge detection in noise")


def example_debouncing():
    """Example 9: Signal Debouncing."""
    print("\n" + "=" * 60)
    print("Example 9: Signal Debouncing")
    print("=" * 60)
    
    # Create a noisy signal (like button clicks or sensor readings)
    noisy_values = [5.0, 5.1, 5.05, 5.08, 7.0, 7.1, 7.05, 6.9, 5.5, 5.6, 5.4]
    
    # Apply debouncing with threshold of 1.0
    debounced = debounce_signal(noisy_values, threshold=1.0)
    
    print("\nDebounce Configuration:")
    print("  - Threshold: 1.0 (minimum change to accept)")
    print("  - Purpose: Remove small fluctuations from noisy signals")
    
    print("\nSignal Debouncing:")
    print("-" * 40)
    print("  Original → Debounced")
    for orig, deb in zip(noisy_values, debounced):
        status = "accepted" if orig == deb else "filtered"
        print(f"  {orig:.2f} → {deb:.2f} ({status})")


def run_all_examples():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("AllToolkit - Hysteresis Utilities Usage Examples")
    print("=" * 60)
    
    examples = [
        example_thermostat_control,
        example_alarm_system,
        example_schmitt_trigger,
        example_dead_zone,
        example_multi_level_hysteresis,
        example_state_machine,
        example_signal_filtering,
        example_edge_detection,
        example_debouncing,
    ]
    
    for example in examples:
        try:
            example()
        except Exception as e:
            print(f"\nError in {example.__name__}: {e}")
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    run_all_examples()