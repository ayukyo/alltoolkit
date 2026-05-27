#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Capacitor Utilities Module
=======================================
A comprehensive capacitor calculation and code decoding library with zero external dependencies.

Features:
    - Capacitor code decoding (3-digit, 4-digit, R-notation)
    - Capacitance unit conversion (pF, nF, uF, mF, F)
    - Capacitor energy storage calculation
    - RC time constant calculation
    - Capacitor reactance (Xc) calculation
    - Series/parallel capacitor calculations
    - Capacitor charge/discharge curves
    - EIA code decoding for SMD capacitors
    - Supercapacitor backup time estimation
    - Capacitor color band decoding (vintage capacitors)
    - Capacitor lifetime estimation
    - Standard E-series capacitance values (E3, E6, E12, E24)
    - Ripple current calculations
    - Power factor correction calculations

Author: AllToolkit Contributors
License: MIT
"""

from typing import Dict, List, Optional, Tuple, Union
from enum import Enum
import math


# ============================================================================
# Constants and Mappings
# ============================================================================

# Capacitance unit multipliers
CAPACITANCE_UNITS: Dict[str, float] = {
    "pF": 1e-12,
    "p": 1e-12,
    "nF": 1e-9,
    "n": 1e-9,
    "uF": 1e-6,
    "u": 1e-6,
    "µF": 1e-6,
    "µ": 1e-6,
    "mF": 1e-3,
    "m": 1e-3,
    "F": 1.0,
}

# Standard E-series for capacitors
E_SERIES: Dict[str, List[int]] = {
    "E3": [10, 22, 47],
    "E6": [10, 15, 22, 33, 47, 68],
    "E12": [10, 12, 15, 18, 22, 27, 33, 39, 47, 56, 68, 82],
    "E24": [10, 11, 12, 13, 15, 16, 18, 20, 22, 24, 27, 30, 
            33, 36, 39, 43, 47, 51, 56, 62, 68, 75, 82, 91],
}

# Capacitor color bands (vintage/ceramic capacitors)
COLOR_VALUES: Dict[str, int] = {
    "black": 0,
    "brown": 1,
    "red": 2,
    "orange": 3,
    "yellow": 4,
    "green": 5,
    "blue": 6,
    "violet": 7,
    "gray": 8,
    "white": 9,
}

COLOR_MULTIPLIERS: Dict[str, float] = {
    "black": 1,
    "brown": 10,
    "red": 100,
    "orange": 1000,
    "yellow": 10000,
    "green": 100000,
}

COLOR_TOLERANCES: Dict[str, Optional[float]] = {
    "black": 20.0,
    "brown": 1.0,
    "red": 2.0,
    "green": 0.5,
    "white": 10.0,
    "gold": 5.0,
    "silver": 10.0,
}

# Capacitor voltage color codes (for vintage capacitors)
COLOR_VOLTAGES: Dict[str, Optional[int]] = {
    "black": None,  # Not used for voltage
    "brown": 100,
    "red": 250,
    "orange": 300,
    "yellow": 400,
    "green": 500,
    "blue": 600,
    "violet": 700,
    "gray": 800,
    "white": 900,
}

# EIA-96 multiplier letters for SMD capacitors
EIA_MULTIPLIERS: Dict[str, int] = {
    "A": 1, "B": 10, "C": 100, "D": 1000, "E": 10000,
    "F": 100000, "Y": 1e-2, "R": 1e-3, "X": 1e-4, "S": 1e-5,
}

# Typical dielectric constants
DIELECTRIC_CONSTANTS: Dict[str, float] = {
    "ceramic": 80,
    "tantalum": 27,
    "aluminum": 8.5,
    "film": 3.0,
    "paper": 4.0,
    "mica": 7.0,
    "glass": 10.0,
    "air": 1.0,
}


# ============================================================================
# Unit Conversion Functions
# ============================================================================

def convert_capacitance(value: float, from_unit: str, to_unit: str) -> float:
    """
    Convert capacitance between different units.
    
    Args:
        value: Capacitance value to convert
        from_unit: Source unit (pF, nF, uF, mF, F)
        to_unit: Target unit (pF, nF, uF, mF, F)
    
    Returns:
        Converted capacitance value
    
    Examples:
        >>> convert_capacitance(1, "uF", "nF")
        1000.0
        >>> convert_capacitance(1000, "pF", "nF")
        1.0
    """
    from_unit = from_unit.replace("µ", "u")
    to_unit = to_unit.replace("µ", "u")
    
    if from_unit not in CAPACITANCE_UNITS:
        raise ValueError(f"Unknown unit: {from_unit}")
    if to_unit not in CAPACITANCE_UNITS:
        raise ValueError(f"Unknown unit: {to_unit}")
    
    farads = value * CAPACITANCE_UNITS[from_unit]
    return farads / CAPACITANCE_UNITS[to_unit]


def format_capacitance(capacitance_farads: float) -> str:
    """
    Format capacitance in appropriate unit with SI prefix.
    
    Args:
        capacitance_farads: Capacitance in farads
    
    Returns:
        Formatted string with appropriate unit
    
    Examples:
        >>> format_capacitance(1e-12)
        '1 pF'
        >>> format_capacitance(1e-6)
        '1 uF'
        >>> format_capacitance(0.001)
        '1 mF'
    """
    if capacitance_farads >= 1:
        return f"{capacitance_farads:.3g} F"
    elif capacitance_farads >= 1e-3:
        return f"{capacitance_farads * 1e3:.3g} mF"
    elif capacitance_farads >= 1e-6:
        return f"{capacitance_farads * 1e6:.3g} uF"
    elif capacitance_farads >= 1e-9:
        return f"{capacitance_farads * 1e9:.3g} nF"
    elif capacitance_farads >= 1e-12:
        return f"{capacitance_farads * 1e12:.3g} pF"
    else:
        return f"{capacitance_farads * 1e15:.3g} fF"


def parse_capacitance_string(cap_string: str) -> float:
    """
    Parse capacitance string to farads.
    
    Args:
        cap_string: Capacitance string (e.g., "100nF", "10uF", "1pF")
    
    Returns:
        Capacitance in farads
    
    Examples:
        >>> parse_capacitance_string("100nF")
        1e-7
        >>> parse_capacitance_string("10uF")
        1e-5
    """
    cap_string = cap_string.strip().replace("µ", "u")
    
    # Handle R notation (4R7 = 4.7pF, etc.)
    if "R" in cap_string.upper():
        parts = cap_string.upper().split("R")
        value = float(parts[0]) + float(parts[1]) / (10 ** len(parts[1]))
        # Assume pF for R notation in small caps
        return value * 1e-12
    
    # Extract number and unit
    i = 0
    while i < len(cap_string) and (cap_string[i].isdigit() or cap_string[i] in ".-"):
        i += 1
    
    value = float(cap_string[:i])
    unit = cap_string[i:].strip().lower()
    
    if unit.startswith("p"):
        return value * 1e-12
    elif unit.startswith("n"):
        return value * 1e-9
    elif unit.startswith("u") or unit.startswith("µ"):
        return value * 1e-6
    elif unit.startswith("m"):
        return value * 1e-3
    elif unit.startswith("f"):
        return value
    else:
        # Default to pF for small values, uF for larger
        if value < 1:
            return value * 1e-6  # Assume uF
        else:
            return value * 1e-12  # Assume pF


# ============================================================================
# Capacitor Code Decoding Functions
# ============================================================================

def decode_capacitor_code(code: str) -> Dict[str, Union[float, str, int]]:
    """
    Decode capacitor code to capacitance value.
    Supports 3-digit, 4-digit, and R notation codes.
    
    Args:
        code: Capacitor code string (e.g., "104", "475", "4R7", "100n")
    
    Returns:
        Dictionary with decoded values:
            - capacitance_farads: float - Capacitance in farads
            - capacitance_str: str - Formatted capacitance string
            - code_type: str - Type of code decoded
            - significant: int - Significant digits
            - multiplier: int - Multiplier exponent
    
    Examples:
        >>> decode_capacitor_code("104")["capacitance_farads"]
        1e-7
        >>> decode_capacitor_code("4R7")["capacitance_farads"]
        4.7e-12
    """
    code = code.strip().upper()
    
    # Check if it's R notation (e.g., 4R7 = 4.7pF)
    if "R" in code:
        return _decode_r_notation(code)
    
    # Check if it includes unit (e.g., 100n, 10u)
    if any(c.isalpha() for c in code):
        farads = parse_capacitance_string(code)
        return {
            "capacitance_farads": farads,
            "capacitance_str": format_capacitance(farads),
            "code_type": "unit_notation",
            "significant": None,
            "multiplier": None,
        }
    
    # Numeric code (3-digit or 4-digit)
    if not code.isdigit():
        raise ValueError(f"Invalid capacitor code: {code}")
    
    if len(code) == 3:
        return _decode_3digit(code)
    elif len(code) == 4:
        return _decode_4digit(code)
    else:
        raise ValueError(f"Invalid capacitor code length: {len(code)}")


def _decode_3digit(code: str) -> Dict[str, Union[float, str, int]]:
    """Decode 3-digit capacitor code (e.g., 104 = 10 * 10^4 pF = 100nF)."""
    significant = int(code[:2])
    multiplier = int(code[2])
    
    capacitance_pf = significant * (10 ** multiplier)
    capacitance_farads = capacitance_pf * 1e-12
    
    return {
        "capacitance_farads": capacitance_farads,
        "capacitance_str": format_capacitance(capacitance_farads),
        "code_type": "3-digit",
        "significant": significant,
        "multiplier": multiplier,
    }


def _decode_4digit(code: str) -> Dict[str, Union[float, str, int]]:
    """Decode 4-digit capacitor code (e.g., 4753 = 475 * 10^3 pF)."""
    significant = int(code[:3])
    multiplier = int(code[3])
    
    capacitance_pf = significant * (10 ** multiplier)
    capacitance_farads = capacitance_pf * 1e-12
    
    return {
        "capacitance_farads": capacitance_farads,
        "capacitance_str": format_capacitance(capacitance_farads),
        "code_type": "4-digit",
        "significant": significant,
        "multiplier": multiplier,
    }


def _decode_r_notation(code: str) -> Dict[str, Union[float, str, int]]:
    """Decode R notation capacitor code (e.g., 4R7 = 4.7pF)."""
    parts = code.split("R")
    if len(parts) != 2:
        raise ValueError(f"Invalid R notation: {code}")
    
    integer_part = parts[0] if parts[0] else "0"
    decimal_part = parts[1] if parts[1] else "0"
    
    value = float(integer_part) + float(decimal_part) / (10 ** len(decimal_part))
    capacitance_farads = value * 1e-12  # R notation typically means pF
    
    return {
        "capacitance_farads": capacitance_farads,
        "capacitance_str": format_capacitance(capacitance_farads),
        "code_type": "R-notation",
        "significant": None,
        "multiplier": None,
    }


def encode_capacitor_code(capacitance_farads: float, code_type: str = "3-digit") -> str:
    """
    Encode capacitance value to capacitor code.
    
    Args:
        capacitance_farads: Capacitance in farads
        code_type: Type of code to generate ("3-digit", "4-digit", "R-notation")
    
    Returns:
        Capacitor code string
    
    Examples:
        >>> encode_capacitor_code(1e-7)  # 100nF
        '104'
        >>> encode_capacitor_code(4.7e-12, "R-notation")  # 4.7pF
        '4R7'
    """
    capacitance_pf = capacitance_farads / 1e-12
    
    if code_type == "R-notation":
        # R notation is for values < 10pF with decimal
        if capacitance_pf < 10:
            return f"{capacitance_pf:.1f}".replace(".", "R")
        else:
            code_type = "3-digit"  # Fall back to 3-digit
    
    if code_type == "3-digit":
        if capacitance_pf < 10:
            return f"{capacitance_pf:.1f}".replace(".", "R")
        
        # Find appropriate multiplier to get significant digits in range 10-99
        multiplier = 0
        while capacitance_pf >= 100 and multiplier < 9:
            capacitance_pf /= 10
            multiplier += 1
        
        significant = int(round(capacitance_pf))
        return f"{significant:02d}{multiplier}"
    
    elif code_type == "4-digit":
        if capacitance_pf < 100:
            return f"{capacitance_pf:.2f}".replace(".", "R").ljust(4, "0")
        
        # Find appropriate multiplier to get significant digits in range 100-999
        multiplier = 0
        while capacitance_pf >= 1000 and multiplier < 9:
            capacitance_pf /= 10
            multiplier += 1
        
        significant = int(round(capacitance_pf))
        return f"{significant:03d}{multiplier}"
    
    else:
        raise ValueError(f"Unknown code type: {code_type}")


# ============================================================================
# Capacitor Color Code Decoding
# ============================================================================

def decode_capacitor_colors(colors: List[str]) -> Dict[str, Union[float, str, int, None]]:
    """
    Decode vintage/ceramic capacitor color bands to capacitance value.
    
    Color bands represent:
    - Band 1-2: Significant digits
    - Band 3: Multiplier
    - Band 4: Tolerance (optional)
    - Band 5: Voltage rating (optional)
    
    Args:
        colors: List of color names (e.g., ['brown', 'black', 'orange'])
    
    Returns:
        Dictionary with decoded values
    
    Examples:
        >>> result = decode_capacitor_colors(['brown', 'black', 'orange'])
        >>> result['capacitance_farads']
        1e-8
    """
    if len(colors) < 3:
        raise ValueError("At least 3 color bands required")
    
    colors = [c.lower() for c in colors]
    
    # Decode significant digits
    significant = 0
    for i, color in enumerate(colors[:2]):
        if color not in COLOR_VALUES:
            raise ValueError(f"Unknown color: {color}")
        significant = significant * 10 + COLOR_VALUES[color]
    
    # Decode multiplier
    multiplier_color = colors[2]
    if multiplier_color not in COLOR_MULTIPLIERS:
        raise ValueError(f"Unknown multiplier color: {multiplier_color}")
    multiplier = COLOR_MULTIPLIERS[multiplier_color]
    
    capacitance_pf = significant * multiplier
    capacitance_farads = capacitance_pf * 1e-12
    
    # Decode tolerance (optional)
    tolerance = None
    if len(colors) >= 4:
        tolerance_color = colors[3]
        tolerance = COLOR_TOLERANCES.get(tolerance_color)
    
    # Decode voltage rating (optional)
    voltage = None
    if len(colors) >= 5:
        voltage_color = colors[4]
        voltage = COLOR_VOLTAGES.get(voltage_color)
    
    return {
        "capacitance_farads": capacitance_farads,
        "capacitance_str": format_capacitance(capacitance_farads),
        "tolerance_percent": tolerance,
        "voltage_rating": voltage,
        "significant": significant,
        "multiplier": multiplier,
    }


# ============================================================================
# Electrical Calculations
# ============================================================================

def capacitor_energy(capacitance_farads: float, voltage: float) -> Dict[str, float]:
    """
    Calculate energy stored in a capacitor.
    
    E = 0.5 * C * V^2
    
    Args:
        capacitance_farads: Capacitance in farads
        voltage: Voltage in volts
    
    Returns:
        Dictionary with energy values:
            - energy_joules: Energy in joules
            - energy_watthours: Energy in watt-hours
    
    Examples:
        >>> result = capacitor_energy(1e-6, 10)  # 1uF at 10V
        >>> result['energy_joules']
        5e-05
    """
    energy_joules = 0.5 * capacitance_farads * (voltage ** 2)
    energy_watthours = energy_joules / 3600
    
    return {
        "energy_joules": energy_joules,
        "energy_watthours": energy_watthours,
    }


def capacitor_charge(capacitance_farads: float, voltage: float) -> float:
    """
    Calculate charge stored in a capacitor.
    
    Q = C * V
    
    Args:
        capacitance_farads: Capacitance in farads
        voltage: Voltage in volts
    
    Returns:
        Charge in coulombs
    
    Examples:
        >>> capacitor_charge(1e-6, 5)  # 1uF at 5V
        5e-06
    """
    return capacitance_farads * voltage


def rc_time_constant(resistance_ohms: float, capacitance_farads: float) -> Dict[str, float]:
    """
    Calculate RC time constant and related values.
    
    tau = R * C
    
    Args:
        resistance_ohms: Resistance in ohms
        capacitance_farads: Capacitance in farads
    
    Returns:
        Dictionary with time constant values:
            - tau_seconds: Time constant (tau) in seconds
            - tau_ms: Time constant in milliseconds
            - tau_us: Time constant in microseconds
            - five_tau_seconds: Time for 99.3% charge/discharge
            - half_life_seconds: Time to reach 50% charge
    
    Examples:
        >>> result = rc_time_constant(1000, 1e-6)  # 1kΩ, 1uF
        >>> result['tau_seconds']
        0.001
    """
    tau = resistance_ohms * capacitance_farads
    
    return {
        "tau_seconds": tau,
        "tau_ms": tau * 1000,
        "tau_us": tau * 1e6,
        "five_tau_seconds": tau * 5,
        "half_life_seconds": tau * math.log(2),  # Time to 50%
    }


def capacitor_reactance(capacitance_farads: float, frequency_hz: float) -> Dict[str, float]:
    """
    Calculate capacitive reactance.
    
    Xc = 1 / (2 * pi * f * C)
    
    Args:
        capacitance_farads: Capacitance in farads
        frequency_hz: Frequency in hertz
    
    Returns:
        Dictionary with reactance values:
            - reactance_ohms: Reactance in ohms
            - susceptance_siemens: Susceptance in siemens
    
    Examples:
        >>> result = capacitor_reactance(1e-6, 1000)  # 1uF at 1kHz
        >>> round(result['reactance_ohms'], 1)
        159.2
    """
    if frequency_hz == 0:
        return {
            "reactance_ohms": float('inf'),
            "susceptance_siemens": 0,
        }
    
    reactance = 1 / (2 * math.pi * frequency_hz * capacitance_farads)
    susceptance = 1 / reactance
    
    return {
        "reactance_ohms": reactance,
        "susceptance_siemens": susceptance,
    }


def capacitive_impedance(capacitance_farads: float, frequency_hz: float) -> complex:
    """
    Calculate complex impedance of a capacitor.
    
    Zc = -j / (2 * pi * f * C) = 0 - j * Xc
    
    Args:
        capacitance_farads: Capacitance in farads
        frequency_hz: Frequency in hertz
    
    Returns:
        Complex impedance
    
    Examples:
        >>> z = capacitive_impedance(1e-6, 1000)
        >>> abs(z)
        159.1549...
    """
    if frequency_hz == 0:
        return complex(0, float('-inf'))
    
    xc = 1 / (2 * math.pi * frequency_hz * capacitance_farads)
    return complex(0, -xc)


# ============================================================================
# Series and Parallel Calculations
# ============================================================================

def parallel_capacitance(capacitances: List[float]) -> float:
    """
    Calculate equivalent capacitance of capacitors in parallel.
    
    C_total = C1 + C2 + C3 + ...
    
    Args:
        capacitances: List of capacitance values in farads
    
    Returns:
        Total capacitance in farads
    
    Examples:
        >>> parallel_capacitance([1e-6, 1e-6, 1e-6])  # Three 1uF in parallel
        3e-06
    """
    return sum(capacitances)


def series_capacitance(capacitances: List[float]) -> float:
    """
    Calculate equivalent capacitance of capacitors in series.
    
    1/C_total = 1/C1 + 1/C2 + 1/C3 + ...
    
    Args:
        capacitances: List of capacitance values in farads
    
    Returns:
        Total capacitance in farads
    
    Examples:
        >>> series_capacitance([1e-6, 1e-6])  # Two 1uF in series
        5e-07
    """
    if not capacitances:
        return 0
    
    return 1 / sum(1 / c for c in capacitances if c > 0)


def capacitor_divider_voltage(
    c1: float, c2: float, vin: float
) -> Dict[str, float]:
    """
    Calculate output voltage of a capacitive voltage divider.
    
    For capacitors in series, voltage divides inversely with capacitance:
    Vout = Vin * C1 / (C1 + C2)
    
    Args:
        c1: Upper capacitor in farads
        c2: Lower capacitor in farads
        vin: Input voltage in volts
    
    Returns:
        Dictionary with voltage values:
            - vout: Output voltage
            - v1: Voltage across C1
            - v2: Voltage across C2
    
    Examples:
        >>> result = capacitor_divider_voltage(1e-6, 1e-6, 10)
        >>> result['vout']
        5.0
    """
    total_cap = c1 + c2
    v2 = vin * c1 / total_cap  # Voltage across C2 (output)
    v1 = vin * c2 / total_cap  # Voltage across C1
    
    return {
        "vout": v2,
        "v1": v1,
        "v2": v2,
    }


# ============================================================================
# Charge/Discharge Curves
# ============================================================================

def capacitor_charge_voltage(
    capacitance_farads: float,
    resistance_ohms: float,
    initial_voltage: float,
    target_voltage: float,
    time_seconds: float
) -> float:
    """
    Calculate voltage during capacitor charging.
    
    V(t) = V_target - (V_target - V_initial) * e^(-t/RC)
    
    Args:
        capacitance_farads: Capacitance in farads
        resistance_ohms: Resistance in ohms
        initial_voltage: Initial voltage on capacitor
        target_voltage: Target/charging voltage
        time_seconds: Time in seconds
    
    Returns:
        Voltage at the given time
    
    Examples:
        >>> v = capacitor_charge_voltage(1e-6, 1000, 0, 5, 0.001)  # After 1 tau
        >>> round(v, 2)
        3.16
    """
    tau = resistance_ohms * capacitance_farads
    return target_voltage - (target_voltage - initial_voltage) * math.exp(-time_seconds / tau)


def capacitor_discharge_voltage(
    capacitance_farads: float,
    resistance_ohms: float,
    initial_voltage: float,
    time_seconds: float
) -> float:
    """
    Calculate voltage during capacitor discharge.
    
    V(t) = V_initial * e^(-t/RC)
    
    Args:
        capacitance_farads: Capacitance in farads
        resistance_ohms: Resistance in ohms
        initial_voltage: Initial voltage on capacitor
        time_seconds: Time in seconds
    
    Returns:
        Voltage at the given time
    
    Examples:
        >>> v = capacitor_discharge_voltage(1e-6, 1000, 5, 0.001)  # After 1 tau
        >>> round(v, 2)
        1.84
    """
    tau = resistance_ohms * capacitance_farads
    return initial_voltage * math.exp(-time_seconds / tau)


def time_to_charge(
    capacitance_farads: float,
    resistance_ohms: float,
    target_percent: float = 99.3
) -> float:
    """
    Calculate time to charge a capacitor to a certain percentage.
    
    Args:
        capacitance_farads: Capacitance in farads
        resistance_ohms: Resistance in ohms
        target_percent: Target charge percentage (default 99.3% = 5 tau)
    
    Returns:
        Time in seconds
    
    Examples:
        >>> t = time_to_charge(1e-6, 1000, 63.2)  # Time to 1 tau (63.2%)
        >>> round(t, 6)
        0.001
    """
    if target_percent >= 100:
        target_percent = 99.999
    
    ratio = (100 - target_percent) / 100
    tau = resistance_ohms * capacitance_farads
    return -tau * math.log(ratio)


# ============================================================================
# E-Series and Standard Values
# ============================================================================

def get_capacitor_series(series: str = "E12") -> List[float]:
    """
    Get standard E-series capacitance values.
    
    Args:
        series: E-series name (E3, E6, E12, E24)
    
    Returns:
        List of standard values
    
    Examples:
        >>> get_capacitor_series("E6")
        [10, 15, 22, 33, 47, 68]
    """
    series = series.upper()
    if series not in E_SERIES:
        raise ValueError(f"Unknown E-series: {series}. Use E3, E6, E12, or E24.")
    
    return E_SERIES[series].copy()


def find_nearest_standard(
    capacitance_farads: float,
    series: str = "E12"
) -> Dict[str, Union[float, str]]:
    """
    Find nearest standard capacitance value.
    
    Args:
        capacitance_farads: Target capacitance in farads
        series: E-series to search (E3, E6, E12, E24)
    
    Returns:
        Dictionary with:
            - nearest: Nearest standard value in farads
            - nearest_str: Formatted string
            - error_percent: Percentage error from target
    
    Examples:
        >>> result = find_nearest_standard(8.5e-6, "E12")
        >>> result['nearest_str']
        '8.2 uF'
    """
    # Convert to same decade for comparison
    if capacitance_farads <= 0:
        raise ValueError("Capacitance must be positive")
    
    # Find the decade
    decade = 0
    test_value = capacitance_farads
    while test_value >= 10e-12:
        test_value /= 10
        decade += 1
    while test_value < 1e-12:
        test_value *= 10
        decade -= 1
    
    # Normalize to 1-10 pF range for comparison
    normalized = capacitance_farads / (10 ** decade * 1e-12)
    
    # Find nearest in series
    series_values = get_capacitor_series(series)
    nearest_base = min(series_values, key=lambda x: abs(x / 10 - normalized))
    
    # Find best decade
    best_error = float('inf')
    best_value = 0
    for d in range(decade - 1, decade + 2):
        for base in series_values:
            value = base * (10 ** d) * 1e-12
            error = abs(value - capacitance_farads) / capacitance_farads
            if error < best_error:
                best_error = error
                best_value = value
    
    return {
        "nearest": best_value,
        "nearest_str": format_capacitance(best_value),
        "error_percent": best_error * 100,
    }


# ============================================================================
# Supercapacitor and Backup Calculations
# ============================================================================

def supercap_backup_time(
    capacitance_farads: float,
    initial_voltage: float,
    cutoff_voltage: float,
    current_amps: float
) -> Dict[str, float]:
    """
    Calculate backup time for a supercapacitor.
    
    Uses the formula: t = C * (V_initial - V_cutoff) / I
    
    Args:
        capacitance_farads: Capacitance in farads
        initial_voltage: Initial charged voltage
        cutoff_voltage: Minimum usable voltage
        current_amps: Load current in amps
    
    Returns:
        Dictionary with:
            - time_seconds: Backup time in seconds
            - time_minutes: Backup time in minutes
            - time_hours: Backup time in hours
    
    Examples:
        >>> result = supercap_backup_time(1.0, 5.0, 3.0, 0.001)  # 1F, 5V to 3V at 1mA
        >>> result['time_seconds']
        2000.0
    """
    time_seconds = capacitance_farads * (initial_voltage - cutoff_voltage) / current_amps
    
    return {
        "time_seconds": time_seconds,
        "time_minutes": time_seconds / 60,
        "time_hours": time_seconds / 3600,
    }


def supercap_energy_density(capacitance_farads: float, voltage: float, weight_kg: float = None, volume_m3: float = None) -> Dict[str, float]:
    """
    Calculate energy density of a supercapacitor.
    
    Args:
        capacitance_farads: Capacitance in farads
        voltage: Rated voltage
        weight_kg: Weight in kilograms (optional)
        volume_m3: Volume in cubic meters (optional)
    
    Returns:
        Dictionary with energy density values
    
    Examples:
        >>> result = supercap_energy_density(100, 2.7, weight_kg=0.05)  # 100F, 2.7V, 50g
        >>> round(result['specific_energy_wh_kg'], 1)
        2.0
    """
    energy_joules = 0.5 * capacitance_farads * (voltage ** 2)
    energy_wh = energy_joules / 3600
    
    result = {
        "energy_joules": energy_joules,
        "energy_wh": energy_wh,
    }
    
    if weight_kg:
        result["specific_energy_wh_kg"] = energy_wh / weight_kg
    
    if volume_m3:
        result["energy_density_wh_m3"] = energy_wh / volume_m3
    
    return result


# ============================================================================
# Ripple Current and Power Calculations
# ============================================================================

def ripple_current_rating(
    capacitance_farads: float,
    frequency_hz: float,
    esr_ohms: float,
    max_temp_rise: float = 10.0,
    thermal_resistance: float = 20.0  # °C/W
) -> Dict[str, float]:
    """
    Calculate ripple current handling capability.
    
    Args:
        capacitance_farads: Capacitance in farads
        frequency_hz: Ripple frequency in Hz
        esr_ohms: Equivalent Series Resistance in ohms
        max_temp_rise: Maximum allowed temperature rise in °C
        thermal_resistance: Thermal resistance in °C/W
    
    Returns:
        Dictionary with ripple current ratings
    
    Examples:
        >>> result = ripple_current_rating(100e-6, 100000, 0.1)  # 100uF, 100kHz, 0.1Ω ESR
        >>> result['max_ripple_current_arms']
        0.707...
    """
    # Maximum power dissipation
    max_power = max_temp_rise / thermal_resistance
    
    # Maximum ripple current (RMS)
    max_ripple = math.sqrt(max_power / esr_ohms)
    
    # Calculate reactance at frequency
    xc = capacitor_reactance(capacitance_farads, frequency_hz)["reactance_ohms"]
    
    # Total impedance
    z = math.sqrt(esr_ohms ** 2 + xc ** 2)
    
    return {
        "max_ripple_current_arms": max_ripple,
        "max_power_dissipation_w": max_power,
        "impedance_ohms": z,
        "reactance_ohms": xc,
    }


def capacitor_power_loss(
    capacitance_farads: float,
    ripple_voltage_vrms: float,
    frequency_hz: float,
    esr_ohms: float
) -> Dict[str, float]:
    """
    Calculate power loss in a capacitor due to ripple and ESR.
    
    Args:
        capacitance_farads: Capacitance in farads
        ripple_voltage_vrms: Ripple voltage (RMS) in volts
        frequency_hz: Frequency in Hz
        esr_ohms: ESR in ohms
    
    Returns:
        Dictionary with power loss values
    
    Examples:
        >>> result = capacitor_power_loss(100e-6, 0.5, 100000, 0.1)
        >>> round(result['power_loss_w'], 4)
        0.0079
    """
    # Current through capacitor due to ripple
    xc = capacitor_reactance(capacitance_farads, frequency_hz)["reactance_ohms"]
    z = math.sqrt(esr_ohms ** 2 + xc ** 2)
    
    # RMS current
    ripple_current = ripple_voltage_vrms / z
    
    # Power loss in ESR
    power_loss = ripple_current ** 2 * esr_ohms
    
    return {
        "power_loss_w": power_loss,
        "ripple_current_arms": ripple_current,
        "impedance_ohms": z,
    }


# ============================================================================
# Capacitor Lifetime Estimation
# ============================================================================

def capacitor_lifetime(
    rated_hours: float,
    rated_temp: float,
    operating_temp: float,
    voltage_ratio: float = 1.0  # Operating voltage / Rated voltage
) -> Dict[str, float]:
    """
    Estimate capacitor lifetime based on temperature and voltage.
    
    Uses Arrhenius equation: L = L_rated * 2^((T_rated - T_op)/10) * V_factor
    
    Args:
        rated_hours: Rated lifetime at rated temperature (hours)
        rated_temp: Rated temperature in °C
        operating_temp: Operating temperature in °C
        voltage_ratio: Ratio of operating voltage to rated voltage (0-1)
    
    Returns:
        Dictionary with lifetime estimates
    
    Examples:
        >>> result = capacitor_lifetime(2000, 105, 65, 0.8)  # 2000h @ 105°C, used @ 65°C, 80% voltage
        >>> result['estimated_hours'] > 2000
        True
    """
    # Temperature factor (lifetime doubles for every 10°C decrease)
    temp_factor = 2 ** ((rated_temp - operating_temp) / 10)
    
    # Voltage factor (approximate relationship)
    voltage_factor = voltage_ratio ** 4  # Empirical approximation
    
    estimated_hours = rated_hours * temp_factor / voltage_factor
    
    return {
        "estimated_hours": estimated_hours,
        "estimated_years": estimated_hours / (365 * 24),
        "temperature_factor": temp_factor,
        "voltage_factor": 1 / voltage_factor,
    }


# ============================================================================
# Utility Functions
# ============================================================================

def is_valid_capacitor_code(code: str) -> bool:
    """
    Check if a capacitor code is valid.
    
    Args:
        code: Capacitor code string
    
    Returns:
        True if valid, False otherwise
    """
    try:
        decode_capacitor_code(code)
        return True
    except (ValueError, IndexError):
        return False


def get_capacitor_info(capacitance_farads: float) -> Dict[str, Union[float, str, bool]]:
    """
    Get information about a capacitance value.
    
    Args:
        capacitance_farads: Capacitance in farads
    
    Returns:
        Dictionary with capacitance information
    """
    return {
        "farads": capacitance_farads,
        "formatted": format_capacitance(capacitance_farads),
        "picofarads": capacitance_farads / 1e-12,
        "nanofarads": capacitance_farads / 1e-9,
        "microfarads": capacitance_farads / 1e-6,
        "millifarads": capacitance_farads / 1e-3,
        "is_standard_e3": any(
            abs(capacitance_farads - v * 10 ** math.floor(math.log10(capacitance_farads / 1e-12)) * 1e-12) < 1e-15
            for v in E_SERIES["E3"]
        ) if capacitance_farads > 0 else False,
    }


# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    # Demo usage
    print("=== Capacitor Code Decoding ===")
    print(f"104 = {decode_capacitor_code('104')['capacitance_str']}")
    print(f"475 = {decode_capacitor_code('475')['capacitance_str']}")
    print(f"4R7 = {decode_capacitor_code('4R7')['capacitance_str']}")
    print(f"100n = {decode_capacitor_code('100n')['capacitance_str']}")
    
    print("\n=== Capacitor Code Encoding ===")
    print(f"100nF = {encode_capacitor_code(100e-9)}")
    print(f"4.7pF = {encode_capacitor_code(4.7e-12, 'R-notation')}")
    
    print("\n=== Unit Conversion ===")
    print(f"1uF = {convert_capacitance(1, 'uF', 'nF')} nF")
    print(f"1000pF = {convert_capacitance(1000, 'pF', 'nF')} nF")
    
    print("\n=== RC Time Constant ===")
    result = rc_time_constant(1000, 1e-6)  # 1kΩ, 1uF
    print(f"tau = {result['tau_ms']:.3f} ms")
    print(f"5*tau = {result['five_tau_seconds'] * 1000:.3f} ms")
    
    print("\n=== Capacitive Reactance ===")
    result = capacitor_reactance(1e-6, 1000)  # 1uF at 1kHz
    print(f"Xc = {result['reactance_ohms']:.1f} Ω")
    
    print("\n=== Energy Storage ===")
    result = capacitor_energy(1000e-6, 5)  # 1000uF at 5V
    print(f"Energy = {result['energy_joules'] * 1000:.3f} mJ")
    
    print("\n=== Series/Parallel ===")
    print(f"Parallel (10uF + 20uF) = {parallel_capacitance([10e-6, 20e-6]) * 1e6:.1f} uF")
    print(f"Series (10uF + 20uF) = {series_capacitance([10e-6, 20e-6]) * 1e6:.2f} uF")
    
    print("\n=== Supercap Backup Time ===")
    result = supercap_backup_time(1.0, 5.0, 3.0, 0.001)  # 1F, 5V to 3V, 1mA
    print(f"Backup time = {result['time_minutes']:.1f} minutes")