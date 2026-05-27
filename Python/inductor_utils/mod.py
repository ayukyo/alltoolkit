#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Inductor Utilities Module
======================================
A comprehensive inductor calculation and code decoding library with zero external dependencies.

Features:
    - Inductance unit conversion (H, mH, µH, nH, pH)
    - Inductor color code decoding (4-band and 5-band)
    - SMD inductor code decoding (3-digit, 4-digit, R-notation)
    - Inductor energy storage calculation
    - RL time constant calculation
    - Inductive reactance (XL) calculation
    - Series/parallel inductor calculations
    - Q factor calculation
    - Self-resonant frequency (SRF) calculation
    - Resonant frequency calculation (LC circuits)
    - Inductor impedance calculation
    - Standard E-series inductance values (E3, E6, E12, E24)
    - Mutual inductance calculation
    - Coupled inductor calculations
    - Toroid inductor calculation
    - Air core inductor calculation
    - Ferrite core inductor estimation

Author: AllToolkit Contributors
License: MIT
"""

from typing import Dict, List, Optional, Tuple, Union
from enum import Enum
import math


# ============================================================================
# Constants and Mappings
# ============================================================================

# Inductance unit multipliers
INDUCTANCE_UNITS: Dict[str, float] = {
    "H": 1.0,
    "mH": 1e-3,
    "µH": 1e-6,
    "uH": 1e-6,
    "u": 1e-6,
    "µ": 1e-6,
    "nH": 1e-9,
    "n": 1e-9,
    "pH": 1e-12,
    "p": 1e-12,
}

# Standard E-series for inductors
E_SERIES: Dict[str, List[int]] = {
    "E3": [10, 22, 47],
    "E6": [10, 15, 22, 33, 47, 68],
    "E12": [10, 12, 15, 18, 22, 27, 33, 39, 47, 56, 68, 82],
    "E24": [10, 11, 12, 13, 15, 16, 18, 20, 22, 24, 27, 30,
            33, 36, 39, 43, 47, 51, 56, 62, 68, 75, 82, 91],
}

# Inductor color bands (similar to resistor color codes)
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
    "blue": 1000000,
    "violet": 10000000,
    "gold": 0.1,
    "silver": 0.01,
}

COLOR_TOLERANCES: Dict[str, Optional[float]] = {
    "black": 20.0,
    "brown": 1.0,
    "red": 2.0,
    "orange": 3.0,
    "yellow": 4.0,
    "green": 0.5,
    "blue": 0.25,
    "violet": 0.1,
    "gray": 0.05,
    "white": None,
    "gold": 5.0,
    "silver": 10.0,
    "none": 20.0,
}

# SMD inductor code multipliers (similar to capacitors)
SMD_MULTIPLIERS: Dict[str, int] = {
    "R": 1,
    "K": 1000,
    "M": 1000000,
}


# ============================================================================
# Unit Conversion Functions
# ============================================================================

def convert_inductance(value: float, from_unit: str, to_unit: str) -> float:
    """
    Convert inductance between different units.
    
    Args:
        value: Inductance value to convert
        from_unit: Source unit (H, mH, µH, nH, pH)
        to_unit: Target unit (H, mH, µH, nH, pH)
    
    Returns:
        Converted inductance value
    
    Examples:
        >>> convert_inductance(1, "mH", "µH")
        1000.0
        >>> convert_inductance(1000, "nH", "µH")
        1.0
    """
    from_unit = from_unit.replace("µ", "u").replace("uH", "uH")
    to_unit = to_unit.replace("µ", "u").replace("uH", "uH")
    
    # Normalize unit names
    unit_map = {
        "h": "H", "henry": "H", "henries": "H",
        "mh": "mH", "millihenry": "mH", "millihenries": "mH",
        "uh": "µH", "microhenry": "µH", "microhenries": "µH",
        "nh": "nH", "nanohenry": "nH", "nanohenries": "nH",
        "ph": "pH", "picohenry": "pH", "picohenries": "pH",
    }
    
    from_unit = unit_map.get(from_unit.lower(), from_unit)
    to_unit = unit_map.get(to_unit.lower(), to_unit)
    
    if from_unit not in INDUCTANCE_UNITS:
        raise ValueError(f"Unknown unit: {from_unit}")
    if to_unit not in INDUCTANCE_UNITS:
        raise ValueError(f"Unknown unit: {to_unit}")
    
    henries = value * INDUCTANCE_UNITS[from_unit]
    return henries / INDUCTANCE_UNITS[to_unit]


def format_inductance(inductance_henries: float) -> str:
    """
    Format inductance in appropriate unit with SI prefix.
    
    Args:
        inductance_henries: Inductance in henries
    
    Returns:
        Formatted string with appropriate unit
    
    Examples:
        >>> format_inductance(1e-6)
        '1 µH'
        >>> format_inductance(1e-3)
        '1 mH'
        >>> format_inductance(1e-9)
        '1 nH'
    """
    if inductance_henries >= 1:
        return f"{inductance_henries:.3g} H"
    elif inductance_henries >= 1e-3:
        return f"{inductance_henries * 1e3:.3g} mH"
    elif inductance_henries >= 1e-6:
        return f"{inductance_henries * 1e6:.3g} µH"
    elif inductance_henries >= 1e-9:
        return f"{inductance_henries * 1e9:.3g} nH"
    elif inductance_henries >= 1e-12:
        return f"{inductance_henries * 1e12:.3g} pH"
    else:
        return f"{inductance_henries * 1e15:.3g} fH"


def parse_inductance_string(ind_string: str) -> float:
    """
    Parse inductance string to henries.
    
    Args:
        ind_string: Inductance string (e.g., "100nH", "10µH", "1mH")
    
    Returns:
        Inductance in henries
    
    Examples:
        >>> parse_inductance_string("100nH")
        1e-7
        >>> parse_inductance_string("10µH")
        1e-5
    """
    ind_string = ind_string.strip().replace("µ", "u").replace("uH", "uH")
    
    # Handle R notation (e.g., 4R7 = 4.7µH)
    if "R" in ind_string.upper():
        parts = ind_string.upper().split("R")
        value = float(parts[0]) + float(parts[1]) / (10 ** len(parts[1]))
        # Assume µH for R notation
        return value * 1e-6
    
    # Extract number and unit
    i = 0
    while i < len(ind_string) and (ind_string[i].isdigit() or ind_string[i] in ".-"):
        i += 1
    
    value = float(ind_string[:i])
    unit = ind_string[i:].strip().lower()
    
    if unit.startswith("p"):
        return value * 1e-12
    elif unit.startswith("n"):
        return value * 1e-9
    elif unit.startswith("u") or unit.startswith("µ") or unit.startswith("mi"):
        return value * 1e-6
    elif unit.startswith("m"):
        return value * 1e-3
    elif unit.startswith("h") or unit.startswith("he"):
        return value
    else:
        # Default to µH for small values, mH for larger
        if value < 0.1:
            return value * 1e-6  # Assume µH
        elif value < 1000:
            return value * 1e-6  # Assume µH
        else:
            return value * 1e-9  # Assume nH


# ============================================================================
# Inductor Code Decoding Functions
# ============================================================================

def decode_smd_inductor(code: str) -> Dict[str, Union[float, str, int, None]]:
    """
    Decode SMD inductor code to inductance value.
    Supports 3-digit, 4-digit, and R notation codes.
    
    Args:
        code: SMD inductor code string (e.g., "103", "4R7", "100n")
    
    Returns:
        Dictionary with decoded values:
            - inductance_henries: float - Inductance in henries
            - inductance_str: str - Formatted inductance string
            - code_type: str - Type of code decoded
            - significant: int - Significant digits (or None)
            - multiplier: int - Multiplier exponent (or None)
    
    Examples:
        >>> decode_smd_inductor("103")["inductance_henries"]
        1e-5
        >>> decode_smd_inductor("4R7")["inductance_henries"]
        4.7e-06
    """
    code = code.strip().upper()
    
    # Check if it includes unit (e.g., 100n, 10u)
    if any(c.isalpha() and c != "R" for c in code):
        henries = parse_inductance_string(code)
        return {
            "inductance_henries": henries,
            "inductance_str": format_inductance(henries),
            "code_type": "unit_notation",
            "significant": None,
            "multiplier": None,
        }
    
    # Check if it's R notation (e.g., 4R7 = 4.7µH)
    if "R" in code:
        return _decode_r_notation_inductor(code)
    
    # Numeric code (3-digit or 4-digit)
    if not code.isdigit():
        raise ValueError(f"Invalid inductor code: {code}")
    
    if len(code) == 3:
        return _decode_3digit_smd(code)
    elif len(code) == 4:
        return _decode_4digit_smd(code)
    else:
        raise ValueError(f"Invalid inductor code length: {len(code)}")


def _decode_3digit_smd(code: str) -> Dict[str, Union[float, str, int]]:
    """Decode 3-digit SMD inductor code (e.g., 103 = 10 * 10^3 nH = 10µH)."""
    significant = int(code[:2])
    multiplier = int(code[2])
    
    inductance_nh = significant * (10 ** multiplier)
    inductance_henries = inductance_nh * 1e-9
    
    return {
        "inductance_henries": inductance_henries,
        "inductance_str": format_inductance(inductance_henries),
        "code_type": "3-digit-SMD",
        "significant": significant,
        "multiplier": multiplier,
    }


def _decode_4digit_smd(code: str) -> Dict[str, Union[float, str, int]]:
    """Decode 4-digit SMD inductor code (e.g., 1002 = 100 * 10^2 nH = 10µH)."""
    significant = int(code[:3])
    multiplier = int(code[3])
    
    inductance_nh = significant * (10 ** multiplier)
    inductance_henries = inductance_nh * 1e-9
    
    return {
        "inductance_henries": inductance_henries,
        "inductance_str": format_inductance(inductance_henries),
        "code_type": "4-digit-SMD",
        "significant": significant,
        "multiplier": multiplier,
    }


def _decode_r_notation_inductor(code: str) -> Dict[str, Union[float, str, int, None]]:
    """Decode R notation inductor code (e.g., 4R7 = 4.7µH)."""
    parts = code.split("R")
    if len(parts) != 2:
        raise ValueError(f"Invalid R notation: {code}")
    
    integer_part = parts[0] if parts[0] else "0"
    decimal_part = parts[1] if parts[1] else "0"
    
    value = float(integer_part) + float(decimal_part) / (10 ** len(decimal_part))
    inductance_henries = value * 1e-6  # R notation typically means µH
    
    return {
        "inductance_henries": inductance_henries,
        "inductance_str": format_inductance(inductance_henries),
        "code_type": "R-notation",
        "significant": None,
        "multiplier": None,
    }


def encode_smd_inductor(inductance_henries: float, code_type: str = "3-digit") -> str:
    """
    Encode inductance value to SMD inductor code.
    
    Args:
        inductance_henries: Inductance in henries
        code_type: Type of code to generate ("3-digit", "4-digit", "R-notation")
    
    Returns:
        SMD inductor code string
    
    Examples:
        >>> encode_smd_inductor(10e-6)  # 10µH
        '103'
        >>> encode_smd_inductor(4.7e-6, "R-notation")  # 4.7µH
        '4R7'
    """
    inductance_nh = inductance_henries / 1e-9
    
    if code_type == "R-notation":
        # R notation is for values < 10µH with decimal
        inductance_uh = inductance_henries / 1e-6
        if inductance_uh < 10:
            return f"{inductance_uh:.1f}".replace(".", "R")
        else:
            code_type = "3-digit"  # Fall back to 3-digit
    
    if code_type == "3-digit":
        if inductance_nh < 10:
            return f"{inductance_nh:.1f}".replace(".", "R")
        
        # Find appropriate multiplier to get significant digits in range 10-99
        multiplier = 0
        while inductance_nh >= 100 and multiplier < 9:
            inductance_nh /= 10
            multiplier += 1
        
        significant = int(round(inductance_nh))
        return f"{significant:02d}{multiplier}"
    
    elif code_type == "4-digit":
        if inductance_nh < 100:
            return f"{inductance_nh:.2f}".replace(".", "R").ljust(4, "0")
        
        # Find appropriate multiplier to get significant digits in range 100-999
        multiplier = 0
        while inductance_nh >= 1000 and multiplier < 9:
            inductance_nh /= 10
            multiplier += 1
        
        significant = int(round(inductance_nh))
        return f"{significant:03d}{multiplier}"
    
    else:
        raise ValueError(f"Unknown code type: {code_type}")


# ============================================================================
# Inductor Color Code Decoding
# ============================================================================

def decode_inductor_colors(colors: List[str]) -> Dict[str, Union[float, str, int, None]]:
    """
    Decode inductor color bands to inductance value.
    
    Color bands represent (4-band):
    - Band 1-2: Significant digits
    - Band 3: Multiplier
    - Band 4: Tolerance (optional)
    
    Or (5-band):
    - Band 1-3: Significant digits
    - Band 4: Multiplier
    - Band 5: Tolerance (optional)
    
    Args:
        colors: List of color names (e.g., ['brown', 'black', 'red', 'gold'])
    
    Returns:
        Dictionary with decoded values
    
    Examples:
        >>> result = decode_inductor_colors(['brown', 'black', 'red', 'gold'])
        >>> result['inductance_henries']
        1e-06
    """
    if len(colors) < 3:
        raise ValueError("At least 3 color bands required")
    
    colors = [c.lower() for c in colors]
    
    if len(colors) == 4 or len(colors) == 5:
        # 4-band or 5-band (with tolerance)
        if len(colors) == 4:
            return _decode_4band_inductor(colors)
        else:
            return _decode_5band_inductor(colors)
    else:
        raise ValueError(f"Unsupported number of color bands: {len(colors)}")


def _decode_4band_inductor(colors: List[str]) -> Dict[str, Union[float, str, int, None]]:
    """Decode 4-band inductor color code."""
    # Decode significant digits (first 2 bands)
    significant = 0
    for i, color in enumerate(colors[:2]):
        if color not in COLOR_VALUES:
            raise ValueError(f"Unknown color: {color}")
        significant = significant * 10 + COLOR_VALUES[color]
    
    # Decode multiplier (3rd band)
    multiplier_color = colors[2]
    if multiplier_color not in COLOR_MULTIPLIERS:
        raise ValueError(f"Unknown multiplier color: {multiplier_color}")
    multiplier = COLOR_MULTIPLIERS[multiplier_color]
    
    inductance_uh = significant * multiplier
    inductance_henries = inductance_uh * 1e-6
    
    # Decode tolerance (4th band)
    tolerance = None
    if len(colors) >= 4:
        tolerance_color = colors[3]
        tolerance = COLOR_TOLERANCES.get(tolerance_color)
    
    return {
        "inductance_henries": inductance_henries,
        "inductance_str": format_inductance(inductance_henries),
        "tolerance_percent": tolerance,
        "significant": significant,
        "multiplier": multiplier,
        "code_type": "4-band-color",
    }


def _decode_5band_inductor(colors: List[str]) -> Dict[str, Union[float, str, int, None]]:
    """Decode 5-band inductor color code."""
    # Decode significant digits (first 3 bands)
    significant = 0
    for i, color in enumerate(colors[:3]):
        if color not in COLOR_VALUES:
            raise ValueError(f"Unknown color: {color}")
        significant = significant * 10 + COLOR_VALUES[color]
    
    # Decode multiplier (4th band)
    multiplier_color = colors[3]
    if multiplier_color not in COLOR_MULTIPLIERS:
        raise ValueError(f"Unknown multiplier color: {multiplier_color}")
    multiplier = COLOR_MULTIPLIERS[multiplier_color]
    
    inductance_uh = significant * multiplier
    inductance_henries = inductance_uh * 1e-6
    
    # Decode tolerance (5th band)
    tolerance = None
    if len(colors) >= 5:
        tolerance_color = colors[4]
        tolerance = COLOR_TOLERANCES.get(tolerance_color)
    
    return {
        "inductance_henries": inductance_henries,
        "inductance_str": format_inductance(inductance_henries),
        "tolerance_percent": tolerance,
        "significant": significant,
        "multiplier": multiplier,
        "code_type": "5-band-color",
    }


# ============================================================================
# Electrical Calculations
# ============================================================================

def inductor_energy(inductance_henries: float, current_amps: float) -> Dict[str, float]:
    """
    Calculate energy stored in an inductor.
    
    E = 0.5 * L * I^2
    
    Args:
        inductance_henries: Inductance in henries
        current_amps: Current in amperes
    
    Returns:
        Dictionary with energy values:
            - energy_joules: Energy in joules
            - energy_watthours: Energy in watt-hours
    
    Examples:
        >>> result = inductor_energy(1e-3, 10)  # 1mH at 10A
        >>> result['energy_joules']
        0.05
    """
    energy_joules = 0.5 * inductance_henries * (current_amps ** 2)
    energy_watthours = energy_joules / 3600
    
    return {
        "energy_joules": energy_joules,
        "energy_watthours": energy_watthours,
    }


def rl_time_constant(resistance_ohms: float, inductance_henries: float) -> Dict[str, float]:
    """
    Calculate RL time constant and related values.
    
    tau = L / R
    
    Args:
        resistance_ohms: Resistance in ohms
        inductance_henries: Inductance in henries
    
    Returns:
        Dictionary with time constant values:
            - tau_seconds: Time constant (tau) in seconds
            - tau_ms: Time constant in milliseconds
            - tau_us: Time constant in microseconds
            - five_tau_seconds: Time for 99.3% rise/fall
            - half_life_seconds: Time to reach 50%
    
    Examples:
        >>> result = rl_time_constant(1000, 1e-3)  # 1kΩ, 1mH
        >>> result['tau_us']
        1.0
    """
    tau = inductance_henries / resistance_ohms
    
    return {
        "tau_seconds": tau,
        "tau_ms": tau * 1000,
        "tau_us": tau * 1e6,
        "five_tau_seconds": tau * 5,
        "half_life_seconds": tau * math.log(2),
    }


def inductive_reactance(inductance_henries: float, frequency_hz: float) -> Dict[str, float]:
    """
    Calculate inductive reactance.
    
    XL = 2 * pi * f * L
    
    Args:
        inductance_henries: Inductance in henries
        frequency_hz: Frequency in hertz
    
    Returns:
        Dictionary with reactance values:
            - reactance_ohms: Reactance in ohms
            - susceptance_siemens: Susceptance in siemens
    
    Examples:
        >>> result = inductive_reactance(1e-3, 1000)  # 1mH at 1kHz
        >>> round(result['reactance_ohms'], 1)
        6.3
    """
    reactance = 2 * math.pi * frequency_hz * inductance_henries
    susceptance = 1 / reactance if reactance > 0 else float('inf')
    
    return {
        "reactance_ohms": reactance,
        "susceptance_siemens": susceptance,
    }


def inductive_impedance(inductance_henries: float, frequency_hz: float, dc_resistance: float = 0) -> complex:
    """
    Calculate complex impedance of an inductor.
    
    ZL = R + j * XL = R + j * 2 * pi * f * L
    
    Args:
        inductance_henries: Inductance in henries
        frequency_hz: Frequency in hertz
        dc_resistance: DC resistance (DCR) in ohms (default 0)
    
    Returns:
        Complex impedance
    
    Examples:
        >>> z = inductive_impedance(1e-3, 1000)
        >>> abs(z)
        6.2831...
    """
    xl = 2 * math.pi * frequency_hz * inductance_henries
    return complex(dc_resistance, xl)


def inductor_current_rise(
    inductance_henries: float,
    resistance_ohms: float,
    initial_current: float,
    target_current: float,
    time_seconds: float
) -> float:
    """
    Calculate current during inductor energizing.
    
    I(t) = I_target - (I_target - I_initial) * e^(-t*R/L)
    
    Args:
        inductance_henries: Inductance in henries
        resistance_ohms: Resistance in ohms
        initial_current: Initial current through inductor
        target_current: Target/final current (V/R)
        time_seconds: Time in seconds
    
    Returns:
        Current at the given time
    
    Examples:
        >>> i = inductor_current_rise(1e-3, 1000, 0, 0.01, 1e-6)  # After 1 tau
        >>> round(i * 1000, 2)  # mA
        6.32
    """
    tau = inductance_henries / resistance_ohms
    return target_current - (target_current - initial_current) * math.exp(-time_seconds / tau)


def inductor_current_fall(
    inductance_henries: float,
    resistance_ohms: float,
    initial_current: float,
    time_seconds: float
) -> float:
    """
    Calculate current during inductor de-energizing.
    
    I(t) = I_initial * e^(-t*R/L)
    
    Args:
        inductance_henries: Inductance in henries
        resistance_ohms: Resistance in ohms
        initial_current: Initial current through inductor
        time_seconds: Time in seconds
    
    Returns:
        Current at the given time
    
    Examples:
        >>> i = inductor_current_fall(1e-3, 1000, 0.01, 1e-6)  # After 1 tau
        >>> round(i * 1000, 2)  # mA
        3.68
    """
    tau = inductance_henries / resistance_ohms
    return initial_current * math.exp(-time_seconds / tau)


# ============================================================================
# Series and Parallel Calculations
# ============================================================================

def series_inductance(inductances: List[float], coupling_coefficients: List[float] = None) -> float:
    """
    Calculate equivalent inductance of inductors in series.
    
    For uncoupled inductors: L_total = L1 + L2 + L3 + ...
    For coupled inductors: L_total = L1 + L2 + 2*M (where M is mutual inductance)
    
    Args:
        inductances: List of inductance values in henries
        coupling_coefficients: List of coupling coefficients (optional, for mutual inductance)
    
    Returns:
        Total inductance in henries
    
    Examples:
        >>> series_inductance([1e-3, 2e-3, 3e-3])  # Three inductors in series
        0.006
    """
    if not inductances:
        return 0
    
    if coupling_coefficients is None:
        return sum(inductances)
    
    # With mutual inductance
    total = sum(inductances)
    for i in range(len(inductances) - 1):
        for j in range(i + 1, len(inductances)):
            k = coupling_coefficients[i] if i < len(coupling_coefficients) else 0
            m = k * math.sqrt(inductances[i] * inductances[j])
            total += 2 * m  # Add mutual inductance (assuming additive)
    
    return total


def parallel_inductance(inductances: List[float], coupling_coefficients: List[float] = None) -> float:
    """
    Calculate equivalent inductance of inductors in parallel.
    
    For uncoupled inductors: 1/L_total = 1/L1 + 1/L2 + 1/L3 + ...
    
    Args:
        inductances: List of inductance values in henries
        coupling_coefficients: List of coupling coefficients (optional)
    
    Returns:
        Total inductance in henries
    
    Examples:
        >>> parallel_inductance([1e-3, 1e-3])  # Two 1mH inductors in parallel
        0.0005
    """
    if not inductances:
        return 0
    
    if coupling_coefficients is None:
        return 1 / sum(1 / L for L in inductances if L > 0)
    
    # Simplified parallel calculation without mutual inductance
    return 1 / sum(1 / L for L in inductances if L > 0)


# ============================================================================
# Q Factor and Quality Calculations
# ============================================================================

def q_factor(
    inductance_henries: float,
    frequency_hz: float,
    dc_resistance: float,
    ac_resistance: float = 0
) -> Dict[str, float]:
    """
    Calculate inductor Q factor (quality factor).
    
    Q = XL / R = 2 * pi * f * L / R
    
    Args:
        inductance_henries: Inductance in henries
        frequency_hz: Frequency in hertz
        dc_resistance: DC resistance (DCR) in ohms
        ac_resistance: Additional AC resistance (skin effect, proximity effect) in ohms
    
    Returns:
        Dictionary with Q factor values:
            - q_factor: Quality factor
            - reactance_ohms: Inductive reactance
            - total_resistance_ohms: Total resistance
    
    Examples:
        >>> result = q_factor(1e-3, 1000000, 0.1)  # 1mH, 1MHz, 0.1Ω DCR
        >>> round(result['q_factor'], 1)
        6283.2
    """
    xl = 2 * math.pi * frequency_hz * inductance_henries
    total_resistance = dc_resistance + ac_resistance
    
    q = xl / total_resistance if total_resistance > 0 else float('inf')
    
    return {
        "q_factor": q,
        "reactance_ohms": xl,
        "total_resistance_ohms": total_resistance,
    }


def q_factor_bandwidth(q: float, center_frequency_hz: float) -> Dict[str, float]:
    """
    Calculate bandwidth from Q factor.
    
    BW = f0 / Q
    
    Args:
        q: Quality factor
        center_frequency_hz: Center/resonant frequency in hertz
    
    Returns:
        Dictionary with bandwidth values:
            - bandwidth_hz: -3dB bandwidth in hertz
            - lower_cutoff_hz: Lower -3dB frequency
            - upper_cutoff_hz: Upper -3dB frequency
    
    Examples:
        >>> result = q_factor_bandwidth(100, 1e6)  # Q=100 at 1MHz
        >>> result['bandwidth_hz']
        10000.0
    """
    bandwidth = center_frequency_hz / q
    lower = center_frequency_hz - bandwidth / 2
    upper = center_frequency_hz + bandwidth / 2
    
    return {
        "bandwidth_hz": bandwidth,
        "lower_cutoff_hz": lower,
        "upper_cutoff_hz": upper,
    }


# ============================================================================
# Resonant Frequency Calculations
# ============================================================================

def resonant_frequency(inductance_henries: float, capacitance_farads: float) -> float:
    """
    Calculate resonant frequency of LC circuit.
    
    f = 1 / (2 * pi * sqrt(L * C))
    
    Args:
        inductance_henries: Inductance in henries
        capacitance_farads: Capacitance in farads
    
    Returns:
        Resonant frequency in hertz
    
    Examples:
        >>> freq = resonant_frequency(1e-3, 1e-6)  # 1mH, 1µF
        >>> round(freq)
        5033.0
    """
    return 1 / (2 * math.pi * math.sqrt(inductance_henries * capacitance_farads))


def resonant_inductance(frequency_hz: float, capacitance_farads: float) -> float:
    """
    Calculate inductance needed for resonance at given frequency.
    
    L = 1 / (4 * pi^2 * f^2 * C)
    
    Args:
        frequency_hz: Desired resonant frequency in hertz
        capacitance_farads: Capacitance in farads
    
    Returns:
        Required inductance in henries
    
    Examples:
        >>> L = resonant_inductance(1000, 1e-6)  # 1kHz, 1µF
        >>> format_inductance(L)
        '25.33 mH'
    """
    return 1 / (4 * math.pi ** 2 * frequency_hz ** 2 * capacitance_farads)


def resonant_capacitance(frequency_hz: float, inductance_henries: float) -> float:
    """
    Calculate capacitance needed for resonance at given frequency.
    
    C = 1 / (4 * pi^2 * f^2 * L)
    
    Args:
        frequency_hz: Desired resonant frequency in hertz
        inductance_henries: Inductance in henries
    
    Returns:
        Required capacitance in farads
    
    Examples:
        >>> C = resonant_capacitance(1000, 1e-3)  # 1kHz, 1mH
        >>> C * 1e6  # µF
        25.33...
    """
    return 1 / (4 * math.pi ** 2 * frequency_hz ** 2 * inductance_henries)


# ============================================================================
# Self-Resonant Frequency (SRF)
# ============================================================================

def self_resonant_frequency(inductance_henries: float, parasitic_capacitance_farads: float) -> float:
    """
    Calculate self-resonant frequency of an inductor.
    
    The self-resonant frequency occurs when the inductor's inductance resonates
    with its parasitic capacitance.
    
    f_srf = 1 / (2 * pi * sqrt(L * C_parasitic))
    
    Args:
        inductance_henries: Inductance in henries
        parasitic_capacitance_farads: Parasitic capacitance in farads
    
    Returns:
        Self-resonant frequency in hertz
    
    Examples:
        >>> f = self_resonant_frequency(1e-3, 10e-12)  # 1mH with 10pF parasitic
        >>> round(f / 1e6, 2)  # MHz
        1.59
    """
    return 1 / (2 * math.pi * math.sqrt(inductance_henries * parasitic_capacitance_farads))


# ============================================================================
# Mutual Inductance and Coupling
# ============================================================================

def mutual_inductance(
    inductance1_henries: float,
    inductance2_henries: float,
    coupling_coefficient: float
) -> float:
    """
    Calculate mutual inductance between two coupled inductors.
    
    M = k * sqrt(L1 * L2)
    
    Args:
        inductance1_henries: First inductance in henries
        inductance2_henries: Second inductance in henries
        coupling_coefficient: Coupling coefficient (0 to 1)
    
    Returns:
        Mutual inductance in henries
    
    Examples:
        >>> M = mutual_inductance(1e-3, 1e-3, 0.9)  # Two 1mH inductors, k=0.9
        >>> M * 1e3  # mH
        0.9
    """
    return coupling_coefficient * math.sqrt(inductance1_henries * inductance2_henries)


def coupling_coefficient(
    inductance1_henries: float,
    inductance2_henries: float,
    mutual_inductance_henries: float
) -> float:
    """
    Calculate coupling coefficient from mutual inductance.
    
    k = M / sqrt(L1 * L2)
    
    Args:
        inductance1_henries: First inductance in henries
        inductance2_henries: Second inductance in henries
        mutual_inductance_henries: Mutual inductance in henries
    
    Returns:
        Coupling coefficient (0 to 1)
    
    Examples:
        >>> k = coupling_coefficient(1e-3, 1e-3, 0.9e-3)
        >>> k
        0.9
    """
    return mutual_inductance_henries / math.sqrt(inductance1_henries * inductance2_henries)


def coupled_inductance_series(
    inductance1_henries: float,
    inductance2_henries: float,
    mutual_inductance_henries: float,
    phase: str = "additive"
) -> float:
    """
    Calculate total inductance of coupled inductors in series.
    
    L_total = L1 + L2 ± 2M
    
    Args:
        inductance1_henries: First inductance in henries
        inductance2_henries: Second inductance in henries
        mutual_inductance_henries: Mutual inductance in henries
        phase: "additive" (same direction) or "subtractive" (opposite)
    
    Returns:
        Total inductance in henries
    
    Examples:
        >>> L = coupled_inductance_series(1e-3, 1e-3, 0.5e-3, "additive")
        >>> L * 1e3  # mH
        3.0
    """
    if phase == "additive":
        return inductance1_henries + inductance2_henries + 2 * mutual_inductance_henries
    else:
        return inductance1_henries + inductance2_henries - 2 * mutual_inductance_henries


def coupled_inductance_parallel(
    inductance1_henries: float,
    inductance2_henries: float,
    mutual_inductance_henries: float
) -> float:
    """
    Calculate total inductance of coupled inductors in parallel.
    
    L_total = (L1 * L2 - M^2) / (L1 + L2 - 2M)
    
    Args:
        inductance1_henries: First inductance in henries
        inductance2_henries: Second inductance in henries
        mutual_inductance_henries: Mutual inductance in henries
    
    Returns:
        Total inductance in henries
    
    Examples:
        >>> L = coupled_inductance_parallel(1e-3, 1e-3, 0.5e-3)
        >>> L * 1e3  # mH
        0.5
    """
    numerator = inductance1_henries * inductance2_henries - mutual_inductance_henries ** 2
    denominator = inductance1_henries + inductance2_henries - 2 * mutual_inductance_henries
    
    if abs(denominator) < 1e-15:
        return float('inf')
    
    return numerator / denominator


# ============================================================================
# Physical Inductor Calculations
# ============================================================================

def air_core_inductance(
    coil_radius_meters: float,
    coil_length_meters: float,
    number_of_turns: int,
    wire_diameter_meters: float = None
) -> Dict[str, float]:
    """
    Calculate inductance of a single-layer air core solenoid coil.
    
    L = (mu0 * N^2 * A) / l
    
    Where mu0 = 4 * pi * 10^-7 H/m (permeability of free space)
    
    Args:
        coil_radius_meters: Coil radius in meters
        coil_length_meters: Coil length in meters
        number_of_turns: Number of turns
        wire_diameter_meters: Wire diameter in meters (optional, for correction)
    
    Returns:
        Dictionary with:
            - inductance_henries: Inductance in henries
            - inductance_str: Formatted inductance string
            - turns_per_meter: Turns per meter
    
    Examples:
        >>> result = air_core_inductance(0.01, 0.05, 100)  # 1cm radius, 5cm length, 100 turns
        >>> result['inductance_str']
        '198 µH'
    """
    mu0 = 4 * math.pi * 1e-7  # Permeability of free space
    
    # Cross-sectional area
    area = math.pi * coil_radius_meters ** 2
    
    # Basic inductance formula for solenoid
    inductance = (mu0 * number_of_turns ** 2 * area) / coil_length_meters
    
    # Apply Wheeler's formula correction for more accuracy
    # L = (N^2 * r^2) / (9 * r + 10 * l) (in µH, r and l in inches)
    # Convert to meters, apply correction
    radius_inches = coil_radius_meters / 0.0254
    length_inches = coil_length_meters / 0.0254
    wheeler_inductance_uh = (number_of_turns ** 2 * radius_inches ** 2) / (9 * radius_inches + 10 * length_inches)
    wheeler_inductance = wheeler_inductance_uh * 1e-6
    
    # Use average of both methods for better accuracy
    inductance = (inductance + wheeler_inductance) / 2
    
    turns_per_meter = number_of_turns / coil_length_meters
    
    return {
        "inductance_henries": inductance,
        "inductance_str": format_inductance(inductance),
        "turns_per_meter": turns_per_meter,
    }


def toroid_inductance(
    core_permeability: float,
    core_cross_section_m2: float,
    magnetic_path_length_m: float,
    number_of_turns: int
) -> Dict[str, float]:
    """
    Calculate inductance of a toroidal inductor.
    
    L = (mu0 * mur * N^2 * A) / l_magnetic
    
    Args:
        core_permeability: Relative permeability of the core material
        core_cross_section_m2: Core cross-sectional area in square meters
        magnetic_path_length_m: Magnetic path length in meters
        number_of_turns: Number of turns
    
    Returns:
        Dictionary with inductance values
    
    Examples:
        >>> result = toroid_inductance(2000, 1e-4, 0.05, 50)  # Ferrite toroid
        >>> result['inductance_str']
        '12.6 mH'
    """
    mu0 = 4 * math.pi * 1e-7  # Permeability of free space
    
    inductance = (mu0 * core_permeability * number_of_turns ** 2 * core_cross_section_m2) / magnetic_path_length_m
    
    return {
        "inductance_henries": inductance,
        "inductance_str": format_inductance(inductance),
        "effective_permeability": core_permeability,
    }


def turns_needed(
    target_inductance_henries: float,
    core_permeability: float,
    core_cross_section_m2: float,
    magnetic_path_length_m: float
) -> int:
    """
    Calculate number of turns needed for target inductance on a toroid core.
    
    N = sqrt(L * l_magnetic / (mu0 * mur * A))
    
    Args:
        target_inductance_henries: Target inductance in henries
        core_permeability: Relative permeability of the core material
        core_cross_section_m2: Core cross-sectional area in square meters
        magnetic_path_length_m: Magnetic path length in meters
    
    Returns:
        Number of turns needed (rounded up)
    
    Examples:
        >>> turns_needed(1e-3, 2000, 1e-4, 0.05)  # 1mH target
        15
    """
    mu0 = 4 * math.pi * 1e-7
    
    turns_squared = (target_inductance_henries * magnetic_path_length_m) / (mu0 * core_permeability * core_cross_section_m2)
    
    return math.ceil(math.sqrt(turns_squared))


# ============================================================================
# E-Series and Standard Values
# ============================================================================

def get_inductor_series(series: str = "E12") -> List[float]:
    """
    Get standard E-series inductance values.
    
    Args:
        series: E-series name (E3, E6, E12, E24)
    
    Returns:
        List of standard values
    
    Examples:
        >>> get_inductor_series("E6")
        [10, 15, 22, 33, 47, 68]
    """
    series = series.upper()
    if series not in E_SERIES:
        raise ValueError(f"Unknown E-series: {series}. Use E3, E6, E12, or E24.")
    
    return E_SERIES[series].copy()


def find_nearest_standard(
    inductance_henries: float,
    series: str = "E12"
) -> Dict[str, Union[float, str]]:
    """
    Find nearest standard inductance value.
    
    Args:
        inductance_henries: Target inductance in henries
        series: E-series to search (E3, E6, E12, E24)
    
    Returns:
        Dictionary with:
            - nearest: Nearest standard value in henries
            - nearest_str: Formatted string
            - error_percent: Percentage error from target
    
    Examples:
        >>> result = find_nearest_standard(8.5e-6, "E12")  # 8.5µH
        >>> result['nearest_str']
        '8.2 µH'
    """
    if inductance_henries <= 0:
        raise ValueError("Inductance must be positive")
    
    # Find the decade
    decade = 0
    test_value = inductance_henries
    while test_value >= 10e-6:
        test_value /= 10
        decade += 1
    while test_value < 1e-6:
        test_value *= 10
        decade -= 1
    
    # Normalize to 1-10 µH range for comparison
    normalized = inductance_henries / (10 ** decade * 1e-6)
    
    # Find nearest in series
    series_values = get_inductor_series(series)
    nearest_base = min(series_values, key=lambda x: abs(x / 10 - normalized))
    
    # Find best decade
    best_error = float('inf')
    best_value = 0
    for d in range(decade - 1, decade + 2):
        for base in series_values:
            value = base * (10 ** d) * 1e-6
            error = abs(value - inductance_henries) / inductance_henries
            if error < best_error:
                best_error = error
                best_value = value
    
    return {
        "nearest": best_value,
        "nearest_str": format_inductance(best_value),
        "error_percent": best_error * 100,
    }


# ============================================================================
# Utility Functions
# ============================================================================

def is_valid_smd_code(code: str) -> bool:
    """
    Check if an SMD inductor code is valid.
    
    Args:
        code: SMD inductor code string
    
    Returns:
        True if valid, False otherwise
    """
    try:
        decode_smd_inductor(code)
        return True
    except (ValueError, IndexError):
        return False


def get_inductor_info(inductance_henries: float) -> Dict[str, Union[float, str, bool]]:
    """
    Get information about an inductance value.
    
    Args:
        inductance_henries: Inductance in henries
    
    Returns:
        Dictionary with inductance information
    """
    return {
        "henries": inductance_henries,
        "formatted": format_inductance(inductance_henries),
        "nanohenries": inductance_henries / 1e-9,
        "microhenries": inductance_henries / 1e-6,
        "millihenries": inductance_henries / 1e-3,
        "is_standard_e3": any(
            abs(inductance_henries - v * 10 ** math.floor(math.log10(inductance_henries / 1e-6)) * 1e-6) < 1e-15
            for v in E_SERIES["E3"]
        ) if inductance_henries > 0 else False,
    }


def inductor_saturation_current(
    inductance_henries: float,
    core_cross_section_m2: float,
    magnetic_path_length_m: float,
    number_of_turns: int,
    saturation_flux_density_tesla: float
) -> float:
    """
    Calculate saturation current for an inductor.
    
    I_sat = (B_sat * l_magnetic) / (mu0 * mur * N)
    
    For air core, mur = 1.
    
    Args:
        inductance_henries: Inductance in henries
        core_cross_section_m2: Core cross-sectional area in m²
        magnetic_path_length_m: Magnetic path length in meters
        number_of_turns: Number of turns
        saturation_flux_density_tesla: Saturation flux density in Tesla
    
    Returns:
        Saturation current in amperes
    """
    mu0 = 4 * math.pi * 1e-7
    
    # Calculate effective permeability from inductance
    mur = (inductance_henries * magnetic_path_length_m) / (mu0 * number_of_turns ** 2 * core_cross_section_m2)
    
    # Saturation current
    i_sat = (saturation_flux_density_tesla * magnetic_path_length_m) / (mu0 * mur * number_of_turns)
    
    return i_sat


# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    # Demo usage
    print("=== SMD Inductor Code Decoding ===")
    print(f"103 = {decode_smd_inductor('103')['inductance_str']}")
    print(f"4R7 = {decode_smd_inductor('4R7')['inductance_str']}")
    print(f"100n = {decode_smd_inductor('100n')['inductance_str']}")
    
    print("\n=== SMD Inductor Code Encoding ===")
    print(f"10µH = {encode_smd_inductor(10e-6)}")
    print(f"4.7µH = {encode_smd_inductor(4.7e-6, 'R-notation')}")
    
    print("\n=== Unit Conversion ===")
    print(f"1mH = {convert_inductance(1, 'mH', 'µH')} µH")
    print(f"1000nH = {convert_inductance(1000, 'nH', 'µH')} µH")
    
    print("\n=== RL Time Constant ===")
    result = rl_time_constant(1000, 1e-3)  # 1kΩ, 1mH
    print(f"τ = {result['tau_us']:.3f} µs")
    print(f"5τ = {result['five_tau_seconds'] * 1e6:.3f} µs")
    
    print("\n=== Inductive Reactance ===")
    result = inductive_reactance(1e-3, 1000)  # 1mH at 1kHz
    print(f"XL = {result['reactance_ohms']:.2f} Ω")
    
    print("\n=== Energy Storage ===")
    result = inductor_energy(1e-3, 10)  # 1mH at 10A
    print(f"Energy = {result['energy_joules'] * 1000:.3f} mJ")
    
    print("\n=== Q Factor ===")
    result = q_factor(1e-3, 1000000, 0.1)  # 1mH, 1MHz, 0.1Ω
    print(f"Q = {result['q_factor']:.1f}")
    
    print("\n=== Resonant Frequency ===")
    freq = resonant_frequency(1e-3, 1e-6)  # 1mH, 1µF
    print(f"f0 = {freq:.1f} Hz")
    
    print("\n=== Series/Parallel ===")
    print(f"Series (10µH + 20µH) = {series_inductance([10e-6, 20e-6]) * 1e6:.1f} µH")
    print(f"Parallel (10µH + 20µH) = {parallel_inductance([10e-6, 20e-6]) * 1e6:.2f} µH")
    
    print("\n=== Air Core Inductor ===")
    result = air_core_inductance(0.01, 0.05, 100)  # 1cm radius, 5cm length, 100 turns
    print(f"L = {result['inductance_str']}")
    
    print("\n=== Toroid Inductor ===")
    result = toroid_inductance(2000, 1e-4, 0.05, 50)
    print(f"L = {result['inductance_str']}")