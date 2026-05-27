#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Inductor Utilities Module Tests
============================================
Comprehensive test suite for inductor_utils module.

Run tests: python -m pytest test_mod.py -v
Or: python test_mod.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import math
from mod import (
    # Unit conversion
    convert_inductance, format_inductance, parse_inductance_string,
    
    # SMD code
    decode_smd_inductor, encode_smd_inductor,
    
    # Color codes
    decode_inductor_colors,
    
    # Electrical calculations
    inductor_energy, rl_time_constant, inductive_reactance,
    inductive_impedance, inductor_current_rise, inductor_current_fall,
    
    # Series/parallel
    series_inductance, parallel_inductance,
    
    # Q factor
    q_factor, q_factor_bandwidth,
    
    # Resonant frequency
    resonant_frequency, resonant_inductance, resonant_capacitance,
    self_resonant_frequency,
    
    # Mutual inductance
    mutual_inductance, coupling_coefficient,
    coupled_inductance_series, coupled_inductance_parallel,
    
    # Physical calculations
    air_core_inductance, toroid_inductance, turns_needed,
    
    # Standard values
    get_inductor_series, find_nearest_standard,
    
    # Utility
    is_valid_smd_code, get_inductor_info,
    inductor_saturation_current,
)


def test_unit_conversion():
    """Test inductance unit conversion."""
    # mH to µH
    assert abs(convert_inductance(1, "mH", "µH") - 1000.0) < 1e-10
    assert abs(convert_inductance(1, "mH", "uH") - 1000.0) < 1e-10
    
    # µH to nH
    assert abs(convert_inductance(1, "µH", "nH") - 1000.0) < 1e-10
    assert abs(convert_inductance(1, "uH", "nH") - 1000.0) < 1e-10
    
    # nH to µH
    assert abs(convert_inductance(1000, "nH", "µH") - 1.0) < 1e-10
    
    # H to mH
    assert abs(convert_inductance(1, "H", "mH") - 1000.0) < 1e-10
    
    # µH to H
    assert abs(convert_inductance(1e6, "µH", "H") - 1.0) < 1e-10
    
    print("✓ Unit conversion tests passed")


def test_format_inductance():
    """Test inductance formatting."""
    assert format_inductance(1) == "1 H"
    assert format_inductance(1e-3) == "1 mH"
    assert format_inductance(1e-6) == "1 µH"
    assert format_inductance(1e-9) == "1 nH"
    assert format_inductance(1e-12) == "1 pH"
    
    # Test larger values
    assert "H" in format_inductance(10)
    assert "mH" in format_inductance(10e-3)
    
    print("✓ Format inductance tests passed")


def test_parse_inductance_string():
    """Test inductance string parsing."""
    assert abs(parse_inductance_string("100nH") - 100e-9) < 1e-15
    assert abs(parse_inductance_string("10µH") - 10e-6) < 1e-15
    assert abs(parse_inductance_string("1mH") - 1e-3) < 1e-15
    assert abs(parse_inductance_string("1H") - 1.0) < 1e-15
    
    # Test µ character variations
    assert abs(parse_inductance_string("10uH") - 10e-6) < 1e-15
    
    print("✓ Parse inductance string tests passed")


def test_smd_code_decoding():
    """Test SMD inductor code decoding."""
    # 3-digit codes
    # 103 = 10 * 10^3 nH = 10000 nH = 10 µH
    result = decode_smd_inductor("103")
    assert abs(result["inductance_henries"] - 10e-6) < 1e-15
    assert result["code_type"] == "3-digit-SMD"
    
    # 470 = 47 * 10^0 nH = 47 nH = 0.047 µH (but actually should be µH based on convention)
    # Let me test with known codes
    result = decode_smd_inductor("221")  # 22 * 10^1 nH = 220 nH
    assert abs(result["inductance_henries"] - 220e-9) < 1e-15
    
    # R notation
    result = decode_smd_inductor("4R7")
    assert abs(result["inductance_henries"] - 4.7e-6) < 1e-15
    assert result["code_type"] == "R-notation"
    
    # Unit notation
    result = decode_smd_inductor("100nH")
    assert abs(result["inductance_henries"] - 100e-9) < 1e-15
    
    print("✓ SMD code decoding tests passed")


def test_smd_code_encoding():
    """Test SMD inductor code encoding."""
    # 3-digit encoding
    # 10µH should encode to 103 (10 * 10^3 nH = 10000 nH = 10 µH)
    assert encode_smd_inductor(10e-6) == "103"
    
    # 100µH = 107 (100 * 10^7 nH would be wrong, let me check)
    # Actually 100µH = 100000 nH = 100 * 10^3? No, that would be 103 = 10µH
    # 100µH = 100 * 10^6 nH? 1006?
    # Let me test actual values
    result = encode_smd_inductor(100e-6)
    # Verify by decoding
    decoded = decode_smd_inductor(result)
    assert abs(decoded["inductance_henries"] - 100e-6) < 1e-10
    
    # R notation
    assert encode_smd_inductor(4.7e-6, "R-notation") == "4R7"
    
    print("✓ SMD code encoding tests passed")


def test_color_code_decoding():
    """Test inductor color code decoding."""
    # 4-band color code
    # Brown-Black-Red = 10 * 100 µH = 1000 µH = 1 mH
    result = decode_inductor_colors(["brown", "black", "red", "gold"])
    assert abs(result["inductance_henries"] - 1e-3) < 1e-15  # 1 mH
    assert result["tolerance_percent"] == 5.0
    
    # 5-band color code
    # Brown-Black-Black-Red = 100 * 100 µH = 10000 µH = 10 mH
    result = decode_inductor_colors(["brown", "black", "black", "red", "gold"])
    assert abs(result["inductance_henries"] - 10e-3) < 1e-15  # 10 mH
    
    print("✓ Color code decoding tests passed")


def test_energy_storage():
    """Test inductor energy storage calculation."""
    # 1mH at 10A
    result = inductor_energy(1e-3, 10)
    assert result["energy_joules"] == 0.5 * 1e-3 * 100  # 0.05 J
    assert abs(result["energy_joules"] - 0.05) < 1e-10
    
    # 100µH at 5A
    result = inductor_energy(100e-6, 5)
    expected = 0.5 * 100e-6 * 25  # 0.00125 J
    assert abs(result["energy_joules"] - expected) < 1e-15
    
    print("✓ Energy storage tests passed")


def test_rl_time_constant():
    """Test RL time constant calculation."""
    # 1kΩ, 1mH: τ = L/R = 1mH/1kΩ = 1µs
    result = rl_time_constant(1000, 1e-3)
    assert abs(result["tau_seconds"] - 1e-6) < 1e-15
    assert abs(result["tau_us"] - 1.0) < 1e-10
    assert abs(result["five_tau_seconds"] - 5e-6) < 1e-15
    
    # 10Ω, 100mH: τ = 100mH/10Ω = 10ms
    result = rl_time_constant(10, 100e-3)
    assert abs(result["tau_seconds"] - 10e-3) < 1e-15
    assert abs(result["tau_ms"] - 10.0) < 1e-10
    
    print("✓ RL time constant tests passed")


def test_inductive_reactance():
    """Test inductive reactance calculation."""
    # 1mH at 1kHz
    result = inductive_reactance(1e-3, 1000)
    expected = 2 * math.pi * 1000 * 1e-3  # ~6.28 Ω
    assert abs(result["reactance_ohms"] - expected) < 0.01
    
    # 1µH at 1MHz
    result = inductive_reactance(1e-6, 1e6)
    expected = 2 * math.pi * 1e6 * 1e-6  # ~6.28 Ω
    assert abs(result["reactance_ohms"] - expected) < 0.01
    
    print("✓ Inductive reactance tests passed")


def test_inductive_impedance():
    """Test inductive impedance calculation."""
    # Pure inductance (no DCR)
    z = inductive_impedance(1e-3, 1000)
    assert z.real == 0
    assert abs(z.imag) > 0
    
    # With DCR
    z = inductive_impedance(1e-3, 1000, dc_resistance=1)
    assert z.real == 1
    assert abs(z.imag) > 0
    
    print("✓ Inductive impedance tests passed")


def test_current_rise_fall():
    """Test inductor current rise and fall."""
    # Current rise
    i = inductor_current_rise(1e-3, 1000, 0, 0.01, 1e-6)  # 1 tau
    expected = 0.01 * (1 - math.exp(-1))  # ~0.00632
    assert abs(i - expected) < 0.0001
    
    # Current fall
    i = inductor_current_fall(1e-3, 1000, 0.01, 1e-6)  # 1 tau
    expected = 0.01 * math.exp(-1)  # ~0.00368
    assert abs(i - expected) < 0.0001
    
    print("✓ Current rise/fall tests passed")


def test_series_parallel():
    """Test series and parallel inductance."""
    # Series (uncoupled)
    assert series_inductance([1e-3, 2e-3, 3e-3]) == 6e-3
    
    # Parallel (uncoupled)
    result = parallel_inductance([1e-3, 1e-3])
    assert abs(result - 0.5e-3) < 1e-15
    
    # Two equal inductors in parallel = half
    assert abs(parallel_inductance([10e-6, 10e-6]) - 5e-6) < 1e-15
    
    print("✓ Series/parallel tests passed")


def test_q_factor():
    """Test Q factor calculation."""
    # High Q inductor: 1mH, 1MHz, 0.1Ω DCR
    result = q_factor(1e-3, 1e6, 0.1)
    expected = 2 * math.pi * 1e6 * 1e-3 / 0.1  # ~6283
    assert abs(result["q_factor"] - expected) < 10
    
    # Lower Q
    result = q_factor(1e-3, 1000, 1)  # 1mH, 1kHz, 1Ω
    expected = 2 * math.pi * 1000 * 1e-3 / 1  # ~6.28
    assert abs(result["q_factor"] - expected) < 0.1
    
    print("✓ Q factor tests passed")


def test_q_factor_bandwidth():
    """Test Q factor bandwidth calculation."""
    # Q=100 at 1MHz
    result = q_factor_bandwidth(100, 1e6)
    assert result["bandwidth_hz"] == 10000  # 1MHz/100 = 10kHz
    assert result["lower_cutoff_hz"] == 9.95e5  # 1MHz - 5kHz
    assert result["upper_cutoff_hz"] == 1.005e6  # 1MHz + 5kHz
    
    print("✓ Q factor bandwidth tests passed")


def test_resonant_frequency():
    """Test resonant frequency calculations."""
    # LC resonant frequency
    freq = resonant_frequency(1e-3, 1e-6)  # 1mH, 1µF
    expected = 1 / (2 * math.pi * math.sqrt(1e-3 * 1e-6))  # ~5033 Hz
    assert abs(freq - expected) < 10
    
    # Reverse calculations
    L = resonant_inductance(1000, 1e-6)  # 1kHz, 1µF
    expected_L = 1 / (4 * math.pi ** 2 * 1e6 * 1e-6)  # ~25.33 mH
    assert abs(L - expected_L) < 1e-6
    
    C = resonant_capacitance(1000, 1e-3)  # 1kHz, 1mH
    expected_C = 1 / (4 * math.pi ** 2 * 1e6 * 1e-3)  # ~25.33 µF
    assert abs(C - expected_C) < 1e-12
    
    print("✓ Resonant frequency tests passed")


def test_self_resonant_frequency():
    """Test self-resonant frequency calculation."""
    # 1mH with 10pF parasitic
    freq = self_resonant_frequency(1e-3, 10e-12)
    expected = 1 / (2 * math.pi * math.sqrt(1e-3 * 10e-12))  # ~1.59 MHz
    assert abs(freq / 1e6 - 1.59) < 0.1
    
    print("✓ Self-resonant frequency tests passed")


def test_mutual_inductance():
    """Test mutual inductance calculations."""
    # Two 1mH inductors with k=0.9
    M = mutual_inductance(1e-3, 1e-3, 0.9)
    assert abs(M - 0.9e-3) < 1e-15
    
    # Coupling coefficient from M
    k = coupling_coefficient(1e-3, 1e-3, 0.9e-3)
    assert abs(k - 0.9) < 1e-15
    
    print("✓ Mutual inductance tests passed")


def test_coupled_inductance():
    """Test coupled inductor calculations."""
    # Series additive
    L = coupled_inductance_series(1e-3, 1e-3, 0.5e-3, "additive")
    expected = 1e-3 + 1e-3 + 2 * 0.5e-3  # 3mH
    assert abs(L - expected) < 1e-15
    
    # Series subtractive
    L = coupled_inductance_series(1e-3, 1e-3, 0.5e-3, "subtractive")
    expected = 1e-3 + 1e-3 - 2 * 0.5e-3  # 1mH
    assert abs(L - expected) < 1e-15
    
    # Parallel
    L = coupled_inductance_parallel(1e-3, 1e-3, 0.5e-3)
    # L_total = (L1*L2 - M^2) / (L1 + L2 - 2M)
    expected = (1e-6 - 0.25e-6) / (2e-3 - 1e-3)  # 0.75e-6 / 1e-3 = 0.75mH
    assert abs(L - expected) < 1e-15
    
    print("✓ Coupled inductance tests passed")


def test_air_core_inductance():
    """Test air core inductor calculation."""
    # 1cm radius, 5cm length, 100 turns
    result = air_core_inductance(0.01, 0.05, 100)
    assert result["inductance_henries"] > 0
    assert result["turns_per_meter"] == 2000
    
    # More turns = more inductance
    result2 = air_core_inductance(0.01, 0.05, 200)
    assert result2["inductance_henries"] > result["inductance_henries"]
    
    print("✓ Air core inductance tests passed")


def test_toroid_inductance():
    """Test toroid inductor calculation."""
    # Ferrite toroid: µr=2000, A=1e-4 m², l=0.05m, N=50
    result = toroid_inductance(2000, 1e-4, 0.05, 50)
    assert result["inductance_henries"] > 0
    
    # Calculate expected
    mu0 = 4 * math.pi * 1e-7
    expected = mu0 * 2000 * 2500 * 1e-4 / 0.05  # ~12.6 mH
    assert abs(result["inductance_henries"] - expected) < 1e-6
    
    print("✓ Toroid inductance tests passed")


def test_turns_needed():
    """Test turns needed calculation."""
    # Need ~14-15 turns for 1mH with given core
    turns = turns_needed(1e-3, 2000, 1e-4, 0.05)
    assert turns >= 10  # Should be reasonable
    
    print("✓ Turns needed tests passed")


def test_e_series():
    """Test E-series values."""
    # E6 values
    e6 = get_inductor_series("E6")
    assert e6 == [10, 15, 22, 33, 47, 68]
    
    # E12 values
    e12 = get_inductor_series("E12")
    assert len(e12) == 12
    
    print("✓ E-series tests passed")


def test_find_nearest_standard():
    """Test finding nearest standard value."""
    # 8.5µH should find 8.2µH in E12
    result = find_nearest_standard(8.5e-6, "E12")
    assert abs(result["nearest"] - 8.2e-6) < 1e-9 or abs(result["nearest"] - 10e-6) < 1e-9
    
    # Exact match should have zero error
    result = find_nearest_standard(10e-6, "E12")
    assert result["error_percent"] < 1
    
    print("✓ Find nearest standard tests passed")


def test_is_valid_smd_code():
    """Test SMD code validation."""
    assert is_valid_smd_code("103") == True
    assert is_valid_smd_code("4R7") == True
    assert is_valid_smd_code("100n") == True
    assert is_valid_smd_code("abc") == False  # Invalid
    assert is_valid_smd_code("") == False  # Empty
    
    print("✓ SMD code validation tests passed")


def test_get_inductor_info():
    """Test inductor info function."""
    info = get_inductor_info(1e-3)
    assert abs(info["henries"] - 1e-3) < 1e-15
    assert abs(info["millihenries"] - 1) < 1e-10
    assert abs(info["microhenries"] - 1000) < 1e-10
    assert "mH" in info["formatted"]
    
    print("✓ Inductor info tests passed")


def run_all_tests():
    """Run all test functions."""
    print("=" * 60)
    print("AllToolkit - Inductor Utilities Module Tests")
    print("=" * 60)
    print()
    
    tests = [
        test_unit_conversion,
        test_format_inductance,
        test_parse_inductance_string,
        test_smd_code_decoding,
        test_smd_code_encoding,
        test_color_code_decoding,
        test_energy_storage,
        test_rl_time_constant,
        test_inductive_reactance,
        test_inductive_impedance,
        test_current_rise_fall,
        test_series_parallel,
        test_q_factor,
        test_q_factor_bandwidth,
        test_resonant_frequency,
        test_self_resonant_frequency,
        test_mutual_inductance,
        test_coupled_inductance,
        test_air_core_inductance,
        test_toroid_inductance,
        test_turns_needed,
        test_e_series,
        test_find_nearest_standard,
        test_is_valid_smd_code,
        test_get_inductor_info,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"✗ {test.__name__} FAILED: {e}")
            failed += 1
    
    print()
    print("=" * 60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)