#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Capacitor Utilities Usage Examples
================================================
Comprehensive examples demonstrating capacitor_utils functionality.
"""

import sys
import os

# Add module directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    decode_capacitor_code, encode_capacitor_code,
    convert_capacitance, format_capacitance, parse_capacitance_string,
    decode_capacitor_colors,
    capacitor_energy, capacitor_charge,
    rc_time_constant, capacitor_reactance, capacitive_impedance,
    parallel_capacitance, series_capacitance, capacitor_divider_voltage,
    capacitor_charge_voltage, capacitor_discharge_voltage, time_to_charge,
    get_capacitor_series, find_nearest_standard,
    supercap_backup_time, supercap_energy_density,
    ripple_current_rating, capacitor_power_loss,
    capacitor_lifetime,
    is_valid_capacitor_code, get_capacitor_info,
)


def example_code_decoding():
    """Example: Decode various capacitor codes."""
    print("\n=== Capacitor Code Decoding ===")
    
    codes = ["104", "103", "475", "106", "1000", "4R7", "R47", "2R2", "100n", "10u"]
    
    for code in codes:
        try:
            result = decode_capacitor_code(code)
            print(f"{code:6} -> {result['capacitance_str']:12} ({result['code_type']})")
        except Exception as e:
            print(f"{code:6} -> Error: {e}")


def example_code_encoding():
    """Example: Encode capacitance values to codes."""
    print("\n=== Capacitor Code Encoding ===")
    
    values = [
        (1e-7, "3-digit"),    # 100nF
        (1e-8, "3-digit"),    # 10nF
        (4.7e-6, "3-digit"),  # 4.7uF
        (4.7e-12, "R-notation"),  # 4.7pF
        (2.2e-12, "R-notation"),  # 2.2pF
    ]
    
    for value, code_type in values:
        code = encode_capacitor_code(value, code_type)
        formatted = format_capacitance(value)
        print(f"{formatted:12} -> {code} ({code_type})")


def example_unit_conversion():
    """Example: Convert between capacitance units."""
    print("\n=== Unit Conversion ===")
    
    conversions = [
        (1, "uF", "nF"),
        (1, "uF", "pF"),
        (1000, "pF", "nF"),
        (100, "nF", "uF"),
        (1, "F", "uF"),
        (1e-6, "F", "uF"),
    ]
    
    for value, from_unit, to_unit in conversions:
        result = convert_capacitance(value, from_unit, to_unit)
        print(f"{value} {from_unit} = {result} {to_unit}")
    
    # Format examples
    print("\n=== Formatting ===")
    values = [1e-12, 1e-9, 1e-6, 1e-3, 1.0, 100e-6, 4.7e-6]
    for v in values:
        print(f"{v:.2e} F -> {format_capacitance(v)}")


def example_color_decoding():
    """Example: Decode vintage capacitor color bands."""
    print("\n=== Color Band Decoding ===")
    
    color_sets = [
        ["brown", "black", "orange"],           # 10nF
        ["brown", "black", "red", "white"],     # 1nF, 10%
        ["brown", "black", "yellow", "green", "green"],  # 100nF, 0.5%, 500V
        ["red", "red", "orange", "silver"],     # 22nF, 10%
    ]
    
    for colors in color_sets:
        result = decode_capacitor_colors(colors)
        colors_str = "-".join(colors)
        cap_str = result['capacitance_str']
        tol = result['tolerance_percent']
        volt = result['voltage_rating']
        
        info = f"{colors_str}: {cap_str}"
        if tol:
            info += f", ±{tol}%"
        if volt:
            info += f", {volt}V"
        print(info)


def example_rc_time_constant():
    """Example: Calculate RC time constants."""
    print("\n=== RC Time Constant ===")
    
    combinations = [
        (1000, 1e-6),    # 1kΩ, 1uF
        (10000, 1e-6),   # 10kΩ, 1uF
        (1000, 10e-6),   # 1kΩ, 10uF
        (470, 100e-6),   # 470Ω, 100uF
    ]
    
    for R, C in combinations:
        result = rc_time_constant(R, C)
        print(f"R={R}Ω, C={format_capacitance(C)}:")
        print(f"  τ = {result['tau_ms']:.3f} ms ({result['tau_us']:.1f} µs)")
        print(f"  5τ = {result['five_tau_seconds']*1000:.3f} ms (99.3% charged)")
        print(f"  Half-life = {result['half_life_seconds']*1000:.3f} ms")


def example_capacitive_reactance():
    """Example: Calculate capacitive reactance."""
    print("\n=== Capacitive Reactance ===")
    
    configs = [
        (1e-6, 1000),     # 1uF @ 1kHz
        (1e-6, 50),       # 1uF @ 50Hz (mains)
        (100e-6, 50),     # 100uF @ 50Hz
        (1e-4, 100000),   # 100uF @ 100kHz
    ]
    
    for C, f in configs:
        result = capacitor_reactance(C, f)
        print(f"{format_capacitance(C)} @ {f}Hz: Xc = {result['reactance_ohms']:.1f}Ω")


def example_energy_storage():
    """Example: Calculate energy stored in capacitors."""
    print("\n=== Energy Storage ===")
    
    configs = [
        (1e-6, 10),       # 1uF @ 10V
        (1000e-6, 5),     # 1000uF @ 5V
        (1e-3, 12),       # 1mF @ 12V
        (1.0, 2.7),       # 1F supercap @ 2.7V
        (100, 2.7),       # 100F supercap @ 2.7V
    ]
    
    for C, V in configs:
        result = capacitor_energy(C, V)
        energy_str = f"{result['energy_joules']:.4g} J"
        wh_str = f"{result['energy_watthours']:.4g} Wh"
        print(f"{format_capacitance(C)} @ {V}V: E = {energy_str} ({wh_str})")


def example_series_parallel():
    """Example: Series and parallel capacitor calculations."""
    print("\n=== Series and Parallel ===")
    
    # Parallel
    parallel_sets = [
        [1e-6, 1e-6, 1e-6],
        [1e-6, 2e-6, 3e-6],
        [10e-6, 20e-6],
    ]
    
    for caps in parallel_sets:
        result = parallel_capacitance(caps)
        caps_str = ", ".join([format_capacitance(c) for c in caps])
        print(f"Parallel [{caps_str}] = {format_capacitance(result)}")
    
    # Series
    series_sets = [
        [1e-6, 1e-6],
        [1e-6, 2e-6],
        [10e-6, 10e-6, 10e-6],
    ]
    
    for caps in series_sets:
        result = series_capacitance(caps)
        caps_str = ", ".join([format_capacitance(c) for c in caps])
        print(f"Series [{caps_str}] = {format_capacitance(result)}")


def example_voltage_divider():
    """Example: Capacitive voltage divider."""
    print("\n=== Capacitive Voltage Divider ===")
    
    dividers = [
        (1e-6, 1e-6, 10),    # Equal caps
        (2e-6, 1e-6, 10),    # 2:1 ratio
        (1e-6, 2e-6, 12),    # 1:2 ratio
    ]
    
    for c1, c2, vin in dividers:
        result = capacitor_divider_voltage(c1, c2, vin)
        print(f"C1={format_capacitance(c1)}, C2={format_capacitance(c2)}, Vin={vin}V:")
        print(f"  Vout = {result['vout']:.2f}V")


def example_charge_discharge():
    """Example: Capacitor charge/discharge curves."""
    print("\n=== Charge/Discharge Curves ===")
    
    C = 1e-6    # 1uF
    R = 1000    # 1kΩ
    V_target = 5  # 5V
    V_initial = 0  # Start at 0V
    
    # Charging at different times
    times = [0, 0.001, 0.002, 0.003, 0.004, 0.005]  # 0, 1τ, 2τ, 3τ, 4τ, 5τ
    
    print(f"Charging {format_capacitance(C)} through {R}Ω to {V_target}V:")
    for t in times:
        v = capacitor_charge_voltage(C, R, V_initial, V_target, t)
        percent = (v / V_target) * 100
        tau_num = t / (R * C)
        print(f"  t={t*1000:.1f}ms ({tau_num:.0f}τ): V={v:.2f}V ({percent:.1f}%)")
    
    # Discharging
    print(f"\nDischarging {format_capacitance(C)} from {V_target}V through {R}Ω:")
    for t in times:
        v = capacitor_discharge_voltage(C, R, V_target, t)
        percent = (v / V_target) * 100
        tau_num = t / (R * C)
        print(f"  t={t*1000:.1f}ms ({tau_num:.0f}τ): V={v:.2f}V ({percent:.1f}%)")


def example_e_series():
    """Example: E-series standard values."""
    print("\n=== E-Series Standard Values ===")
    
    # Show E-series values
    for series in ["E3", "E6", "E12"]:
        values = get_capacitor_series(series)
        print(f"{series}: {values}")
    
    # Find nearest standard values
    test_values = [8.5e-6, 1.1e-5, 47.5e-9, 2.3e-6]
    
    print("\nNearest standard values:")
    for value in test_values:
        result = find_nearest_standard(value, "E12")
        print(f"  {format_capacitance(value)} -> {result['nearest_str']} (error: {result['error_percent']:.1f}%)")


def example_supercap_backup():
    """Example: Supercapacitor backup time calculations."""
    print("\n=== Supercapacitor Backup ===")
    
    # Backup time examples
    configs = [
        (1.0, 5.0, 3.0, 0.001),   # 1F, 5V->3V, 1mA
        (10.0, 5.0, 3.0, 0.01),   # 10F, 5V->3V, 10mA
        (0.5, 3.3, 2.0, 0.0005),  # 0.5F, 3.3V->2V, 0.5mA
    ]
    
    for C, V_init, V_cut, I in configs:
        result = supercap_backup_time(C, V_init, V_cut, I)
        print(f"{C}F, {V_init}V->{V_cut}V, {I*1000}mA:")
        print(f"  Backup time: {result['time_seconds']:.1f}s ({result['time_minutes']:.1f}min)")
    
    # Energy density
    print("\n=== Supercap Energy Density ===")
    supercap_configs = [
        (100, 2.7, 0.05),   # 100F, 2.7V, 50g
        (1.0, 5.5, 0.01),   # 1F, 5.5V, 10g
    ]
    
    for C, V, weight in supercap_configs:
        result = supercap_energy_density(C, V, weight_kg=weight)
        print(f"{C}F @ {V}V, {weight*1000}g:")
        print(f"  Energy: {result['energy_wh']:.3f} Wh")
        print(f"  Specific energy: {result['specific_energy_wh_kg']:.2f} Wh/kg")


def example_ripple_current():
    """Example: Ripple current calculations."""
    print("\n=== Ripple Current ===")
    
    # Ripple current rating
    configs = [
        (100e-6, 100000, 0.1),   # 100uF, 100kHz, 0.1Ω ESR
        (1000e-6, 50000, 0.05),  # 1000uF, 50kHz, 0.05Ω ESR
    ]
    
    for C, f, esr in configs:
        result = ripple_current_rating(C, f, esr)
        print(f"{format_capacitance(C)} @ {f}Hz, ESR={esr}Ω:")
        print(f"  Max ripple: {result['max_ripple_current_arms']:.2f}A RMS")
        print(f"  Impedance: {result['impedance_ohms']:.3f}Ω")
    
    # Power loss
    print("\n=== Power Loss from Ripple ===")
    loss_configs = [
        (100e-6, 0.5, 100000, 0.1),
        (1000e-6, 1.0, 50000, 0.05),
    ]
    
    for C, V_rms, f, esr in loss_configs:
        result = capacitor_power_loss(C, V_rms, f, esr)
        print(f"{format_capacitance(C)}, {V_rms}V ripple @ {f}Hz, ESR={esr}Ω:")
        print(f"  Power loss: {result['power_loss_w']*1000:.2f}mW")
        print(f"  Ripple current: {result['ripple_current_arms']:.3f}A")


def example_lifetime():
    """Example: Capacitor lifetime estimation."""
    print("\n=== Lifetime Estimation ===")
    
    # Different operating conditions
    configs = [
        (2000, 105, 85, 1.0),   # Hot, full voltage
        (2000, 105, 65, 1.0),   # Cooler, full voltage
        (2000, 105, 65, 0.8),   # Cooler, reduced voltage
        (2000, 105, 45, 0.7),   # Much cooler, reduced voltage
    ]
    
    for hours, rated_temp, op_temp, v_ratio in configs:
        result = capacitor_lifetime(hours, rated_temp, op_temp, v_ratio)
        print(f"Rated {hours}h @ {rated_temp}°C, operating @ {op_temp}°C, {v_ratio*100:.0f}% voltage:")
        print(f"  Estimated: {result['estimated_hours']:.0f}h ({result['estimated_years']:.1f} years)")


def example_led_filter():
    """Example: LED power supply filter capacitor."""
    print("\n=== Practical Example: LED PSU Filter ===")
    
    # Design a filter capacitor for an LED power supply
    print("Design requirements:")
    print("  - Supply: 12V DC with 1V ripple")
    print("  - LED current: 100mA")
    print("  - Ripple frequency: 100Hz (full-wave rectified mains)")
    
    # Calculate required capacitance
    # ΔV = I * Δt / C, where Δt = 1/(2*f) for full-wave rectifier
    f = 100
    I = 0.1
    delta_V = 1.0
    delta_t = 1 / (2 * f)  # 5ms
    
    C_required = I * delta_t / delta_V
    
    print(f"\nCalculations:")
    print(f"  Δt (discharge time) = {delta_t*1000:.1f}ms")
    print(f"  C = I * Δt / ΔV = {I} * {delta_t*1000:.1f}ms / {delta_V}")
    print(f"  C required ≈ {format_capacitance(C_required)}")
    
    # Find nearest standard
    nearest = find_nearest_standard(C_required, "E12")
    print(f"  Nearest E12: {nearest['nearest_str']}")
    
    # Calculate actual ripple with chosen cap
    actual_ripple = I * delta_t / nearest['nearest']
    print(f"  Actual ripple: {actual_ripple:.2f}V")
    
    # RC time constant
    R_filter = 12 / I  # Effective resistance
    tau = rc_time_constant(R_filter, nearest['nearest'])
    print(f"  Effective load R: {R_filter:.1f}Ω")
    print(f"  Time constant: {tau['tau_ms']:.1f}ms")


def run_all_examples():
    """Run all examples."""
    print("=" * 60)
    print("CAPACITOR UTILITIES - COMPREHENSIVE EXAMPLES")
    print("=" * 60)
    
    example_code_decoding()
    example_code_encoding()
    example_unit_conversion()
    example_color_decoding()
    example_rc_time_constant()
    example_capacitive_reactance()
    example_energy_storage()
    example_series_parallel()
    example_voltage_divider()
    example_charge_discharge()
    example_e_series()
    example_supercap_backup()
    example_ripple_current()
    example_lifetime()
    example_led_filter()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    run_all_examples()