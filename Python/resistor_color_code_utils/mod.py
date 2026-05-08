#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Resistor Color Code Utilities Module
==================================================
A comprehensive resistor color code calculator for Python with zero external dependencies.

Features:
    - Convert color bands to resistance value (3, 4, 5, 6 bands)
    - Convert resistance value to color bands
    - Support for tolerance bands (gold, silver, etc.)
    - Temperature coefficient calculation (6-band resistors)
    - SMD resistor code decoding (EIA-96, 3-digit, 4-digit)
    - Resistance value formatting with SI prefixes
    - Standard E-series values (E6, E12, E24, E48, E96, E192)
    - Nearest standard value finder

Author: AllToolkit Contributors
License: MIT
"""

from typing import Dict, List, Optional, Tuple, Union
from enum import Enum


# ============================================================================
# Color Band Definitions
# ============================================================================

class Color(Enum):
    """Resistor color band enumeration."""
    BLACK = "black"
    BROWN = "brown"
    RED = "red"
    ORANGE = "orange"
    YELLOW = "yellow"
    GREEN = "green"
    BLUE = "blue"
    VIOLET = "violet"
    GRAY = "gray"
    WHITE = "white"
    GOLD = "gold"
    SILVER = "silver"
    NONE = "none"  # No tolerance band (20% tolerance)


# Color to value mapping for significant figures
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

# Color to multiplier mapping
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

# Color to tolerance mapping (percentage)
COLOR_TOLERANCES: Dict[str, Optional[float]] = {
    "brown": 1.0,
    "red": 2.0,
    "green": 0.5,
    "blue": 0.25,
    "violet": 0.1,
    "gray": 0.05,
    "gold": 5.0,
    "silver": 10.0,
    "none": 20.0,
}

# Color to temperature coefficient mapping (ppm/°C) for 6-band resistors
COLOR_TEMPCO: Dict[str, Optional[int]] = {
    "black": 250,
    "brown": 100,
    "red": 50,
    "orange": 15,
    "yellow": 25,
    "green": 20,
    "blue": 10,
    "violet": 5,
    "gray": 1,
}

# Reverse mappings for value to color conversion
VALUE_COLORS: Dict[int, str] = {v: k for k, v in COLOR_VALUES.items()}
MULTIPLIER_COLORS: Dict[float, str] = {
    1e-2: "silver",
    1e-1: "gold",
    1: "black",
    10: "brown",
    100: "red",
    1000: "orange",
    10000: "yellow",
    100000: "green",
    1000000: "blue",
    10000000: "violet",
}
TOLERANCE_COLORS: Dict[float, str] = {v: k for k, v in COLOR_TOLERANCES.items() if v is not None}
TEMPCO_COLORS: Dict[int, str] = {v: k for k, v in COLOR_TEMPCO.items() if v is not None}

# Standard E-series values
E_SERIES: Dict[str, List[int]] = {
    "E6": [10, 15, 22, 33, 47, 68],
    "E12": [10, 12, 15, 18, 22, 27, 33, 39, 47, 56, 68, 82],
    "E24": [10, 11, 12, 13, 15, 16, 18, 20, 22, 24, 27, 30, 33, 36, 39, 43, 47, 51, 56, 62, 68, 75, 82, 91],
}

# E96 series values (for more precise resistors)
E96_VALUES: List[int] = [
    100, 102, 105, 107, 110, 113, 115, 118, 121, 124, 127, 130, 133, 137, 140, 143,
    147, 150, 154, 158, 162, 165, 169, 174, 178, 182, 187, 191, 196, 200, 205, 210,
    215, 221, 226, 232, 237, 243, 249, 255, 261, 267, 274, 280, 287, 294, 301, 309,
    316, 324, 332, 340, 348, 357, 365, 374, 383, 392, 402, 412, 422, 432, 442, 453,
    464, 475, 487, 499, 511, 523, 536, 549, 562, 576, 590, 604, 619, 634, 649, 665,
    681, 698, 715, 732, 750, 768, 787, 806, 825, 845, 866, 887, 909, 931, 953, 976
]

E192_VALUES: List[int] = [
    100, 101, 102, 104, 105, 106, 107, 109, 110, 111, 113, 114, 115, 117, 118, 120,
    121, 123, 124, 126, 127, 129, 130, 132, 133, 135, 137, 138, 140, 142, 143, 145,
    147, 149, 150, 152, 154, 156, 158, 160, 162, 164, 165, 167, 169, 172, 174, 176,
    178, 180, 182, 184, 187, 189, 191, 193, 196, 198, 200, 203, 205, 208, 210, 213,
    215, 218, 221, 223, 226, 229, 232, 234, 237, 240, 243, 246, 249, 252, 255, 258,
    261, 264, 267, 271, 274, 277, 280, 284, 287, 291, 294, 298, 301, 305, 309, 312,
    316, 320, 324, 328, 332, 336, 340, 344, 348, 352, 357, 361, 365, 370, 374, 379,
    383, 388, 392, 397, 402, 407, 412, 417, 422, 427, 432, 437, 442, 448, 453, 459,
    464, 470, 475, 481, 487, 493, 499, 505, 511, 517, 523, 530, 536, 542, 549, 556,
    562, 569, 576, 583, 590, 597, 604, 612, 619, 626, 634, 642, 649, 657, 665, 673,
    681, 690, 698, 706, 715, 723, 732, 741, 750, 759, 768, 777, 787, 796, 806, 816,
    825, 835, 845, 856, 866, 876, 887, 898, 909, 920, 931, 942, 953, 965, 976, 988
]

# SMD resistor code mappings
SMD_3DIGIT_MIN = 1.0
SMD_3DIGIT_MAX = 9.9e9  # 9.9 GΩ
SMD_4DIGIT_MIN = 1.0
SMD_4DIGIT_MAX = 99.9e9  # 99.9 GΩ

# EIA-96 SMD resistor codes (for 1% tolerance resistors)
EIA96_CODES: Dict[str, int] = {}
for i, val in enumerate(E96_VALUES):
    code = chr(65 + i // 10) + str(i % 10)  # A0, A1, ... B0, B1, etc.
    if i < 10:
        code = chr(65 + i // 10) + str(i % 10)  # A0-A9
    elif i < 20:
        code = chr(65 + i // 10) + str(i % 10)  # B0-B9
    else:
        code = chr(65 + i // 10) + str(i % 10)


def _build_eia96_codes() -> Dict[str, int]:
    """Build EIA-96 SMD resistor code lookup table."""
    codes = {}
    letters = "CDFGHJKLMNPQRSTUVWXYP"  # EIA-96 multiplier letters
    for i, val in enumerate(E96_VALUES):
        # Generate code: first letter + digit
        letter = letters[i // 10] if i // 10 < len(letters) else letters[-1]
        digit = i % 10
        codes[f"{letter}{digit}"] = val
    return codes


EIA96_LOOKUP = _build_eia96_codes()


# ============================================================================
# Utility Functions
# ============================================================================

def _normalize_color(color: str) -> str:
    """Normalize color name to lowercase."""
    return color.lower().strip()


def _format_resistance(ohms: float, precision: int = 2) -> str:
    """
    Format resistance value with appropriate SI prefix.
    
    Args:
        ohms: Resistance in ohms
        precision: Decimal precision
    
    Returns:
        Formatted string like "4.7 kΩ" or "220 Ω"
    """
    if ohms >= 1e9:
        return f"{ohms / 1e9:.{precision}g} GΩ"
    elif ohms >= 1e6:
        return f"{ohms / 1e6:.{precision}g} MΩ"
    elif ohms >= 1e3:
        return f"{ohms / 1e3:.{precision}g} kΩ"
    elif ohms >= 1:
        return f"{ohms:.{precision}g} Ω"
    elif ohms >= 1e-3:
        return f"{ohms * 1e3:.{precision}g} mΩ"
    elif ohms >= 1e-6:
        return f"{ohms * 1e6:.{precision}g} μΩ"
    else:
        return f"{ohms:.{precision}g} Ω"


def _parse_resistance_string(value: str) -> float:
    """
    Parse a resistance string to ohms.
    
    Args:
        value: String like "4.7k", "220R", "1M5", "100Ω"
    
    Returns:
        Resistance in ohms
    """
    value = value.strip().upper().replace(" ", "").replace("Ω", "R").replace("OHM", "R")
    
    # Handle multiplier suffixes
    multipliers = {
        "R": 1,
        "K": 1e3,
        "M": 1e6,
        "G": 1e9,
        "T": 1e12,
    }
    
    for suffix, mult in multipliers.items():
        if suffix in value:
            parts = value.split(suffix)
            if len(parts) == 2:
                # Handle formats like "4K7", "1M5"
                if parts[1]:
                    num = float(parts[0] + "." + parts[1])
                else:
                    num = float(parts[0])
                return num * mult
            elif len(parts) == 1:
                return float(parts[0]) * mult
    
    # No suffix, assume ohms
    return float(value)


# ============================================================================
# Color Band Decoding
# ============================================================================

def decode_3band(colors: List[str]) -> Dict[str, Union[float, str]]:
    """
    Decode a 3-band resistor (2 significant figures + multiplier).
    No tolerance band means 20% tolerance.
    
    Args:
        colors: List of 3 color names
    
    Returns:
        Dictionary with 'resistance', 'resistance_str', 'tolerance', 'colors'
    
    Example:
        >>> decode_3band(['brown', 'black', 'red'])
        {'resistance': 1000.0, 'resistance_str': '1 kΩ', 'tolerance': 20.0, ...}
    """
    if len(colors) != 3:
        raise ValueError("3-band resistor requires exactly 3 colors")
    
    colors = [_normalize_color(c) for c in colors]
    
    # Validate colors
    for c in colors[:2]:
        if c not in COLOR_VALUES:
            raise ValueError(f"Invalid significant figure color: {c}")
    if colors[2] not in COLOR_MULTIPLIERS:
        raise ValueError(f"Invalid multiplier color: {colors[2]}")
    
    # Calculate resistance
    sig1 = COLOR_VALUES[colors[0]]
    sig2 = COLOR_VALUES[colors[1]]
    multiplier = COLOR_MULTIPLIERS[colors[2]]
    
    resistance = (sig1 * 10 + sig2) * multiplier
    
    return {
        "resistance": resistance,
        "resistance_str": _format_resistance(resistance),
        "tolerance": 20.0,  # Default for 3-band
        "tolerance_str": "±20%",
        "colors": colors,
        "bands": 3,
    }


def decode_4band(colors: List[str]) -> Dict[str, Union[float, str, None]]:
    """
    Decode a 4-band resistor (2 significant figures + multiplier + tolerance).
    
    Args:
        colors: List of 4 color names
    
    Returns:
        Dictionary with 'resistance', 'resistance_str', 'tolerance', 'colors'
    
    Example:
        >>> decode_4band(['brown', 'black', 'red', 'gold'])
        {'resistance': 1000.0, 'resistance_str': '1 kΩ', 'tolerance': 5.0, ...}
    """
    if len(colors) != 4:
        raise ValueError("4-band resistor requires exactly 4 colors")
    
    colors = [_normalize_color(c) for c in colors]
    
    # Validate colors
    for c in colors[:2]:
        if c not in COLOR_VALUES:
            raise ValueError(f"Invalid significant figure color: {c}")
    if colors[2] not in COLOR_MULTIPLIERS:
        raise ValueError(f"Invalid multiplier color: {colors[2]}")
    if colors[3] not in COLOR_TOLERANCES:
        raise ValueError(f"Invalid tolerance color: {colors[3]}")
    
    # Calculate resistance
    sig1 = COLOR_VALUES[colors[0]]
    sig2 = COLOR_VALUES[colors[1]]
    multiplier = COLOR_MULTIPLIERS[colors[2]]
    tolerance = COLOR_TOLERANCES[colors[3]]
    
    resistance = (sig1 * 10 + sig2) * multiplier
    
    return {
        "resistance": resistance,
        "resistance_str": _format_resistance(resistance),
        "tolerance": tolerance,
        "tolerance_str": f"±{tolerance}%",
        "colors": colors,
        "bands": 4,
        "tempco": None,
    }


def decode_5band(colors: List[str]) -> Dict[str, Union[float, str, None]]:
    """
    Decode a 5-band resistor (3 significant figures + multiplier + tolerance).
    
    Args:
        colors: List of 5 color names
    
    Returns:
        Dictionary with 'resistance', 'resistance_str', 'tolerance', 'colors'
    
    Example:
        >>> decode_5band(['brown', 'black', 'black', 'red', 'gold'])
        {'resistance': 10000.0, 'resistance_str': '10 kΩ', 'tolerance': 5.0, ...}
    """
    if len(colors) != 5:
        raise ValueError("5-band resistor requires exactly 5 colors")
    
    colors = [_normalize_color(c) for c in colors]
    
    # Validate colors
    for c in colors[:3]:
        if c not in COLOR_VALUES:
            raise ValueError(f"Invalid significant figure color: {c}")
    if colors[3] not in COLOR_MULTIPLIERS:
        raise ValueError(f"Invalid multiplier color: {colors[3]}")
    if colors[4] not in COLOR_TOLERANCES:
        raise ValueError(f"Invalid tolerance color: {colors[4]}")
    
    # Calculate resistance
    sig1 = COLOR_VALUES[colors[0]]
    sig2 = COLOR_VALUES[colors[1]]
    sig3 = COLOR_VALUES[colors[2]]
    multiplier = COLOR_MULTIPLIERS[colors[3]]
    tolerance = COLOR_TOLERANCES[colors[4]]
    
    resistance = (sig1 * 100 + sig2 * 10 + sig3) * multiplier
    
    return {
        "resistance": resistance,
        "resistance_str": _format_resistance(resistance),
        "tolerance": tolerance,
        "tolerance_str": f"±{tolerance}%",
        "colors": colors,
        "bands": 5,
        "tempco": None,
    }


def decode_6band(colors: List[str]) -> Dict[str, Union[float, str, int, None]]:
    """
    Decode a 6-band resistor (3 significant figures + multiplier + tolerance + tempco).
    
    Args:
        colors: List of 6 color names
    
    Returns:
        Dictionary with 'resistance', 'resistance_str', 'tolerance', 'tempco', 'colors'
    
    Example:
        >>> decode_6band(['brown', 'black', 'black', 'red', 'gold', 'brown'])
        {'resistance': 10000.0, 'resistance_str': '10 kΩ', 'tolerance': 5.0, 'tempco': 100, ...}
    """
    if len(colors) != 6:
        raise ValueError("6-band resistor requires exactly 6 colors")
    
    colors = [_normalize_color(c) for c in colors]
    
    # Validate colors
    for c in colors[:3]:
        if c not in COLOR_VALUES:
            raise ValueError(f"Invalid significant figure color: {c}")
    if colors[3] not in COLOR_MULTIPLIERS:
        raise ValueError(f"Invalid multiplier color: {colors[3]}")
    if colors[4] not in COLOR_TOLERANCES:
        raise ValueError(f"Invalid tolerance color: {colors[4]}")
    if colors[5] not in COLOR_TEMPCO:
        raise ValueError(f"Invalid temperature coefficient color: {colors[5]}")
    
    # Calculate resistance
    sig1 = COLOR_VALUES[colors[0]]
    sig2 = COLOR_VALUES[colors[1]]
    sig3 = COLOR_VALUES[colors[2]]
    multiplier = COLOR_MULTIPLIERS[colors[3]]
    tolerance = COLOR_TOLERANCES[colors[4]]
    tempco = COLOR_TEMPCO[colors[5]]
    
    resistance = (sig1 * 100 + sig2 * 10 + sig3) * multiplier
    
    return {
        "resistance": resistance,
        "resistance_str": _format_resistance(resistance),
        "tolerance": tolerance,
        "tolerance_str": f"±{tolerance}%",
        "tempco": tempco,
        "tempco_str": f"{tempco} ppm/°C",
        "colors": colors,
        "bands": 6,
    }


def decode_resistor(colors: List[str]) -> Dict[str, Union[float, str, int, None]]:
    """
    Automatically detect and decode a resistor based on number of color bands.
    
    Args:
        colors: List of color names (3-6 bands)
    
    Returns:
        Decoded resistor information
    
    Example:
        >>> decode_resistor(['red', 'violet', 'yellow', 'gold'])
        {'resistance': 270000.0, 'resistance_str': '270 kΩ', ...}
    """
    num_bands = len(colors)
    
    if num_bands == 3:
        return decode_3band(colors)
    elif num_bands == 4:
        return decode_4band(colors)
    elif num_bands == 5:
        return decode_5band(colors)
    elif num_bands == 6:
        return decode_6band(colors)
    else:
        raise ValueError(f"Invalid number of bands: {num_bands}. Must be 3, 4, 5, or 6.")


# ============================================================================
# Resistance to Color Band Encoding
# ============================================================================

def encode_4band(resistance: float, tolerance: float = 5.0) -> Dict[str, Union[List[str], float, str]]:
    """
    Encode a resistance value to 4-band color code.
    
    Args:
        resistance: Resistance in ohms
        tolerance: Tolerance percentage (0.05, 0.1, 0.25, 0.5, 1, 2, 5, 10, 20)
    
    Returns:
        Dictionary with 'colors', 'resistance', 'resistance_str', 'tolerance'
    
    Example:
        >>> encode_4band(4700, 5)
        {'colors': ['yellow', 'violet', 'red', 'gold'], ...}
    """
    if tolerance not in TOLERANCE_COLORS:
        # Find nearest available tolerance
        available = sorted(TOLERANCE_COLORS.keys())
        nearest = min(available, key=lambda x: abs(x - tolerance))
        tolerance = nearest
    
    # Find multiplier and significant figures
    if resistance == 0:
        return {
            "colors": ["black", "black", "black", TOLERANCE_COLORS[tolerance]],
            "resistance": 0,
            "resistance_str": "0 Ω",
            "tolerance": tolerance,
            "tolerance_str": f"±{tolerance}%",
        }
    
    # Get significant figures
    resistance_abs = abs(resistance)
    
    # Find appropriate multiplier
    multiplier = 1
    while resistance_abs >= 100:
        resistance_abs /= 10
        multiplier *= 10
    while resistance_abs < 10:
        resistance_abs *= 10
        multiplier /= 10
    
    sig_val = int(round(resistance_abs))
    
    # Handle edge cases
    if sig_val >= 100:
        sig_val //= 10
        multiplier *= 10
    if sig_val < 10:
        sig_val = int(round(resistance_abs * 10))
        multiplier /= 10
    
    sig1 = sig_val // 10
    sig2 = sig_val % 10
    
    # Find multiplier color
    mult_color = None
    for mult, color in sorted(MULTIPLIER_COLORS.items(), key=lambda x: x[0]):
        if abs(mult - multiplier) < 1e-10 * max(abs(mult), 1):
            mult_color = color
            break
    
    # Try to find closest multiplier
    if mult_color is None:
        # Find nearest multiplier
        closest_mult = min(MULTIPLIER_COLORS.keys(), key=lambda x: abs(x - multiplier))
        mult_color = MULTIPLIER_COLORS[closest_mult]
        # Recalculate sig figures for this multiplier
        actual_mult = closest_mult
        resistance_abs = abs(resistance) / actual_mult
        sig_val = int(round(resistance_abs))
        if sig_val >= 100:
            sig_val = sig_val // 10
        if sig_val < 10:
            sig_val = max(10, sig_val * 10)
        sig1 = sig_val // 10
        sig2 = sig_val % 10
    
    colors = [
        VALUE_COLORS.get(sig1, "black"),
        VALUE_COLORS.get(sig2, "black"),
        mult_color,
        TOLERANCE_COLORS[tolerance],
    ]
    
    return {
        "colors": colors,
        "resistance": resistance,
        "resistance_str": _format_resistance(resistance),
        "tolerance": tolerance,
        "tolerance_str": f"±{tolerance}%",
    }


def encode_5band(resistance: float, tolerance: float = 1.0) -> Dict[str, Union[List[str], float, str]]:
    """
    Encode a resistance value to 5-band color code.
    
    Args:
        resistance: Resistance in ohms
        tolerance: Tolerance percentage (0.05, 0.1, 0.25, 0.5, 1, 2, 5, 10)
    
    Returns:
        Dictionary with 'colors', 'resistance', 'resistance_str', 'tolerance'
    
    Example:
        >>> encode_5band(4700, 1)
        {'colors': ['yellow', 'violet', 'black', 'brown', 'brown'], ...}
    """
    if tolerance not in TOLERANCE_COLORS:
        available = sorted(TOLERANCE_COLORS.keys())
        nearest = min(available, key=lambda x: abs(x - tolerance))
        tolerance = nearest
    
    if resistance == 0:
        return {
            "colors": ["black", "black", "black", "black", TOLERANCE_COLORS[tolerance]],
            "resistance": 0,
            "resistance_str": "0 Ω",
            "tolerance": tolerance,
            "tolerance_str": f"±{tolerance}%",
        }
    
    # Get significant figures (3 digits)
    resistance_abs = abs(resistance)
    
    # Find appropriate multiplier
    multiplier = 1
    while resistance_abs >= 1000:
        resistance_abs /= 10
        multiplier *= 10
    while resistance_abs < 100:
        resistance_abs *= 10
        multiplier /= 10
    
    sig_val = int(round(resistance_abs))
    
    # Handle edge cases
    if sig_val >= 1000:
        sig_val //= 10
        multiplier *= 10
    if sig_val < 100:
        sig_val = max(100, int(round(abs(resistance) / multiplier * 100)))
    
    sig1 = sig_val // 100
    sig2 = (sig_val // 10) % 10
    sig3 = sig_val % 10
    
    # Find multiplier color
    mult_color = None
    for mult, color in sorted(MULTIPLIER_COLORS.items(), key=lambda x: x[0]):
        if abs(mult - multiplier) < 1e-10 * max(abs(mult), 1):
            mult_color = color
            break
    
    if mult_color is None:
        closest_mult = min(MULTIPLIER_COLORS.keys(), key=lambda x: abs(x - multiplier))
        mult_color = MULTIPLIER_COLORS[closest_mult]
    
    colors = [
        VALUE_COLORS.get(sig1, "black"),
        VALUE_COLORS.get(sig2, "black"),
        VALUE_COLORS.get(sig3, "black"),
        mult_color,
        TOLERANCE_COLORS[tolerance],
    ]
    
    return {
        "colors": colors,
        "resistance": resistance,
        "resistance_str": _format_resistance(resistance),
        "tolerance": tolerance,
        "tolerance_str": f"±{tolerance}%",
    }


def encode_6band(resistance: float, tolerance: float = 1.0, tempco: int = 100) -> Dict[str, Union[List[str], float, str, int]]:
    """
    Encode a resistance value to 6-band color code (with temperature coefficient).
    
    Args:
        resistance: Resistance in ohms
        tolerance: Tolerance percentage (0.05, 0.1, 0.25, 0.5, 1, 2, 5, 10)
        tempco: Temperature coefficient in ppm/°C (1, 5, 10, 15, 20, 25, 50, 100, 250)
    
    Returns:
        Dictionary with 'colors', 'resistance', 'tolerance', 'tempco'
    
    Example:
        >>> encode_6band(4700, 1, 100)
        {'colors': ['yellow', 'violet', 'black', 'brown', 'brown', 'brown'], ...}
    """
    # Get 5-band encoding first
    result = encode_5band(resistance, tolerance)
    
    # Find tempco color
    if tempco not in TEMPCO_COLORS:
        available = sorted(TEMPCO_COLORS.keys())
        nearest = min(available, key=lambda x: abs(x - tempco))
        tempco = nearest
    
    result["colors"].append(TEMPCO_COLORS[tempco])
    result["tempco"] = tempco
    result["tempco_str"] = f"{tempco} ppm/°C"
    result["bands"] = 6
    
    return result


# ============================================================================
# SMD Resistor Codes
# ============================================================================

def decode_smd(code: str) -> Dict[str, Union[float, str]]:
    """
    Decode an SMD resistor code to resistance value.
    
    Supports:
        - 3-digit codes (e.g., "103" = 10kΩ)
        - 4-digit codes (e.g., "1002" = 10kΩ)
        - EIA-96 codes (e.g., "01C" = 10kΩ)
        - "R" notation (e.g., "4R7" = 4.7Ω)
    
    Args:
        code: SMD resistor code string
    
    Returns:
        Dictionary with 'resistance', 'resistance_str', 'code', 'type'
    
    Example:
        >>> decode_smd("103")
        {'resistance': 10000.0, 'resistance_str': '10 kΩ', 'code': '103', 'type': '3-digit'}
        >>> decode_smd("4R7")
        {'resistance': 4.7, 'resistance_str': '4.7 Ω', 'code': '4R7', 'type': 'R-notation'}
    """
    code = code.strip().upper()
    
    if not code:
        raise ValueError("Empty SMD code")
    
    # Check for R notation (e.g., "4R7", "R47", "47R")
    if "R" in code:
        parts = code.split("R")
        if len(parts) == 2:
            if parts[0] and parts[1]:
                resistance = float(parts[0] + "." + parts[1])
            elif parts[0]:
                resistance = float(parts[0])
            else:
                resistance = float("0." + parts[1])
            return {
                "resistance": resistance,
                "resistance_str": _format_resistance(resistance),
                "code": code,
                "type": "R-notation",
            }
    
    # Check for EIA-96 code (letter + digit)
    if len(code) == 2 and code[0].isalpha() and code[1].isdigit():
        if code in EIA96_LOOKUP:
            base_value = EIA96_LOOKUP[code]
            # EIA-96 codes are base values, need to apply multiplier
            # Actually EIA-96 uses the code differently - the letter is multiplier
            # Let's use a simpler lookup
            # Standard EIA-96: first 2 chars are code, third char is multiplier
            raise ValueError(f"Invalid EIA-96 code: {code}. Need 3-character code like '01C'.")
    
    if len(code) == 3 and code[0].isdigit() and code[1].isdigit() and code[2].isalpha():
        # EIA-96 format: 2 digits + 1 letter
        digit_part = code[:2]
        letter = code[2]
        
        # Get base value from digit code
        digit_code = int(digit_part)
        if 1 <= digit_code <= 96:
            base_value = E96_VALUES[digit_code - 1]
        else:
            raise ValueError(f"Invalid EIA-96 digit code: {digit_part}")
        
        # Multiplier from letter
        letter_multipliers = {
            "A": 1, "B": 10, "C": 100, "D": 1000, "E": 10000,
            "F": 100000, "X": 0.1, "Y": 0.01, "Z": 0.001,
        }
        
        if letter not in letter_multipliers:
            raise ValueError(f"Invalid EIA-96 multiplier letter: {letter}")
        
        multiplier = letter_multipliers[letter]
        resistance = base_value * multiplier
        
        return {
            "resistance": resistance,
            "resistance_str": _format_resistance(resistance),
            "code": code,
            "type": "EIA-96",
        }
    
    # 3-digit code
    if len(code) == 3 and code.isdigit():
        sig = int(code[:2])
        multiplier = int(code[2])
        resistance = sig * (10 ** multiplier)
        return {
            "resistance": resistance,
            "resistance_str": _format_resistance(resistance),
            "code": code,
            "type": "3-digit",
        }
    
    # 4-digit code
    if len(code) == 4 and code.isdigit():
        sig = int(code[:3])
        multiplier = int(code[3])
        resistance = sig * (10 ** multiplier)
        return {
            "resistance": resistance,
            "resistance_str": _format_resistance(resistance),
            "code": code,
            "type": "4-digit",
        }
    
    raise ValueError(f"Invalid SMD code format: {code}")


def encode_smd(resistance: float, code_type: str = "auto") -> Dict[str, Union[str, float]]:
    """
    Encode a resistance value to SMD code.
    
    Args:
        resistance: Resistance in ohms
        code_type: '3-digit', '4-digit', 'auto'
    
    Returns:
        Dictionary with 'code', 'resistance', 'resistance_str', 'type'
    
    Example:
        >>> encode_smd(10000)
        {'code': '103', 'resistance': 10000.0, 'type': '3-digit'}
        >>> encode_smd(4.7)
        {'code': '4R7', 'resistance': 4.7, 'type': 'R-notation'}
    """
    resistance_abs = abs(resistance)
    
    if code_type == "auto":
        # Choose best format
        if resistance_abs < 1:
            # Use R notation for small values
            return encode_smd_r_notation(resistance)
        elif resistance_abs < 100 and resistance_abs == int(resistance_abs):
            # Integer under 100, no code needed
            return {
                "code": str(int(resistance_abs)),
                "resistance": resistance,
                "resistance_str": _format_resistance(resistance),
                "type": "direct",
            }
        elif resistance_abs >= 10 and resistance_abs < 100 and resistance_abs == int(resistance_abs):
            return {
                "code": str(int(resistance_abs)),
                "resistance": resistance,
                "resistance_str": _format_resistance(resistance),
                "type": "direct",
            }
        else:
            # Try 3-digit first
            result = encode_smd_3digit(resistance)
            if result:
                return result
            # Fall back to 4-digit
            result = encode_smd_4digit(resistance)
            if result:
                return result
            # Fall back to R notation
            return encode_smd_r_notation(resistance)
    
    elif code_type == "3-digit":
        result = encode_smd_3digit(resistance)
        if result:
            return result
        raise ValueError(f"Cannot encode {resistance} as 3-digit SMD code")
    
    elif code_type == "4-digit":
        result = encode_smd_4digit(resistance)
        if result:
            return result
        raise ValueError(f"Cannot encode {resistance} as 4-digit SMD code")
    
    else:
        raise ValueError(f"Unknown code type: {code_type}")


def encode_smd_3digit(resistance: float) -> Optional[Dict[str, Union[str, float]]]:
    """Encode resistance to 3-digit SMD code if possible."""
    resistance_abs = abs(resistance)
    
    # Check if 2 significant figures work
    if resistance_abs < 10:
        return None
    
    # Find multiplier
    multiplier = 0
    val = resistance_abs
    while val >= 100:
        val /= 10
        multiplier += 1
    while val < 10:
        val *= 10
        multiplier -= 1
    
    sig = int(round(val))
    if sig >= 100 or sig < 10:
        return None
    
    code = f"{sig}{multiplier}"
    
    return {
        "code": code,
        "resistance": resistance,
        "resistance_str": _format_resistance(resistance),
        "type": "3-digit",
    }


def encode_smd_4digit(resistance: float) -> Optional[Dict[str, Union[str, float]]]:
    """Encode resistance to 4-digit SMD code if possible."""
    resistance_abs = abs(resistance)
    
    if resistance_abs < 1:
        return None
    
    # Find multiplier
    multiplier = 0
    val = resistance_abs
    while val >= 1000:
        val /= 10
        multiplier += 1
    while val < 100:
        val *= 10
        multiplier -= 1
    
    sig = int(round(val))
    if sig >= 1000 or sig < 100:
        return None
    
    code = f"{sig}{multiplier}"
    
    return {
        "code": code,
        "resistance": resistance,
        "resistance_str": _format_resistance(resistance),
        "type": "4-digit",
    }


def encode_smd_r_notation(resistance: float) -> Dict[str, Union[str, float]]:
    """Encode resistance to R notation SMD code."""
    resistance_abs = abs(resistance)
    
    if resistance_abs >= 100:
        # Too large for R notation alone
        val = resistance_abs / 1000
        if val == int(val):
            return {
                "code": f"{int(val)}K",
                "resistance": resistance,
                "resistance_str": _format_resistance(resistance),
                "type": "K-notation",
            }
        else:
            return {
                "code": f"{val:.3g}K".replace(".", "K"),
                "resistance": resistance,
                "resistance_str": _format_resistance(resistance),
                "type": "K-notation",
            }
    
    if resistance_abs >= 10:
        return {
            "code": str(int(resistance_abs)),
            "resistance": resistance,
            "resistance_str": _format_resistance(resistance),
            "type": "direct",
        }
    
    # R notation
    val_str = f"{resistance_abs:.2g}"
    if "." in val_str:
        return {
            "code": val_str.replace(".", "R"),
            "resistance": resistance,
            "resistance_str": _format_resistance(resistance),
            "type": "R-notation",
        }
    else:
        return {
            "code": f"{val_str}R",
            "resistance": resistance,
            "resistance_str": _format_resistance(resistance),
            "type": "R-notation",
        }


# ============================================================================
# Standard E-Series Values
# ============================================================================

def get_e_series(series: str) -> List[float]:
    """
    Get standard E-series values.
    
    Args:
        series: Series name ('E6', 'E12', 'E24', 'E96', 'E192')
    
    Returns:
        List of standard values
    
    Example:
        >>> get_e_series('E12')
        [10, 12, 15, 18, 22, 27, 33, 39, 47, 56, 68, 82]
    """
    series = series.upper()
    if series == "E6":
        return E_SERIES["E6"][:]
    elif series == "E12":
        return E_SERIES["E12"][:]
    elif series == "E24":
        return E_SERIES["E24"][:]
    elif series == "E96":
        return E96_VALUES[:]
    elif series == "E192":
        return E192_VALUES[:]
    else:
        raise ValueError(f"Unknown E-series: {series}. Use E6, E12, E24, E96, or E192.")


def find_nearest_standard(value: float, series: str = "E24") -> Dict[str, Union[float, str, List[float]]]:
    """
    Find the nearest standard resistor value in an E-series.
    
    Args:
        value: Desired resistance value in ohms
        series: E-series to search ('E6', 'E12', 'E24', 'E96', 'E192')
    
    Returns:
        Dictionary with 'nearest', 'error_percent', 'candidates'
    
    Example:
        >>> find_nearest_standard(4700, 'E12')
        {'nearest': 4700.0, 'error_percent': 0.0, ...}
        >>> find_nearest_standard(5000, 'E12')
        {'nearest': 4700.0, 'error_percent': 6.0, ...}
    """
    series_values = get_e_series(series)
    
    # Find the decade
    if value <= 0:
        raise ValueError("Value must be positive")
    
    decade = 0
    val = value
    while val >= 100:
        val /= 10
        decade += 1
    while val < 10:
        val *= 10
        decade -= 1
    
    # Generate candidates for nearby decades
    candidates = []
    for d in [decade - 1, decade, decade + 1]:
        mult = 10 ** d
        for sv in series_values:
            candidates.append(sv * mult / 10)  # Adjust for base value being 10-99
    
    # Find nearest
    nearest = min(candidates, key=lambda x: abs(x - value))
    error_percent = abs(nearest - value) / value * 100
    
    # Get all candidates within 10%
    nearby = sorted([c for c in candidates if abs(c - value) / value * 100 <= 10],
                   key=lambda x: abs(x - value))
    
    return {
        "nearest": nearest,
        "nearest_str": _format_resistance(nearest),
        "error_percent": round(error_percent, 2),
        "candidates": nearby[:5],
        "series": series,
    }


def is_standard_value(value: float, series: str = "E24", tolerance: float = 1.0) -> bool:
    """
    Check if a value is a standard E-series value within tolerance.
    
    Args:
        value: Resistance value in ohms
        series: E-series to check against
        tolerance: Allowed deviation percentage
    
    Returns:
        True if value is standard within tolerance
    
    Example:
        >>> is_standard_value(4700, 'E12')
        True
        >>> is_standard_value(4800, 'E12')
        False
    """
    series_values = get_e_series(series)
    
    # Find the decade
    decade = 0
    val = value
    while val >= 100:
        val /= 10
        decade += 1
    while val < 10:
        val *= 10
        decade -= 1
    
    # Check all decades within a range
    for d in [decade - 1, decade, decade + 1]:
        mult = 10 ** d
        for sv in series_values:
            standard = sv * mult / 10
            if abs(standard - value) / value * 100 <= tolerance:
                return True
    
    return False


# ============================================================================
# Parallel and Series Resistance
# ============================================================================

def parallel_resistance(resistances: List[float]) -> float:
    """
    Calculate equivalent resistance of resistors in parallel.
    
    Args:
        resistances: List of resistance values in ohms
    
    Returns:
        Equivalent resistance in ohms
    
    Example:
        >>> parallel_resistance([100, 100])
        50.0
        >>> parallel_resistance([1000, 2000])
        666.66...
    """
    if not resistances:
        raise ValueError("Empty resistance list")
    
    # Filter out zero resistances (short circuit)
    non_zero = [r for r in resistances if r > 0]
    
    if not non_zero:
        return 0.0  # All zero = short circuit
    
    # Check for zeros
    if any(r == 0 for r in resistances):
        return 0.0  # Any zero = short circuit
    
    # Calculate parallel resistance
    reciprocal_sum = sum(1 / r for r in non_zero)
    return 1 / reciprocal_sum


def series_resistance(resistances: List[float]) -> float:
    """
    Calculate equivalent resistance of resistors in series.
    
    Args:
        resistances: List of resistance values in ohms
    
    Returns:
        Equivalent resistance in ohms
    
    Example:
        >>> series_resistance([100, 200])
        300.0
    """
    if not resistances:
        raise ValueError("Empty resistance list")
    
    return sum(resistances)


def voltage_divider(r1: float, r2: float, vin: float) -> float:
    """
    Calculate output voltage of a voltage divider.
    
    Args:
        r1: Upper resistor (between Vin and Vout) in ohms
        r2: Lower resistor (between Vout and GND) in ohms
        vin: Input voltage in volts
    
    Returns:
        Output voltage in volts
    
    Example:
        >>> voltage_divider(10000, 10000, 5)
        2.5
    """
    if r1 + r2 == 0:
        raise ValueError("Total resistance cannot be zero")
    
    return vin * r2 / (r1 + r2)


def led_resistor(supply_voltage: float, led_voltage: float, led_current: float) -> float:
    """
    Calculate the required resistor for an LED circuit.
    
    Args:
        supply_voltage: Supply voltage in volts
        led_voltage: LED forward voltage in volts
        led_current: Desired LED current in amperes
    
    Returns:
        Required resistor value in ohms
    
    Example:
        >>> led_resistor(5, 2, 0.02)  # 5V supply, 2V LED, 20mA
        150.0
    """
    if led_current <= 0:
        raise ValueError("LED current must be positive")
    
    voltage_drop = supply_voltage - led_voltage
    if voltage_drop <= 0:
        raise ValueError("Supply voltage must be greater than LED voltage")
    
    return voltage_drop / led_current


# ============================================================================
# Color Band Validation
# ============================================================================

def is_valid_color(color: str) -> bool:
    """Check if a color name is valid for resistor color codes."""
    return _normalize_color(color) in COLOR_VALUES or \
           _normalize_color(color) in COLOR_MULTIPLIERS or \
           _normalize_color(color) in COLOR_TOLERANCES or \
           _normalize_color(color) in COLOR_TEMPCO or \
           _normalize_color(color) == "none"


def get_color_info(color: str) -> Dict[str, Union[int, float, str, None]]:
    """
    Get information about a resistor color.
    
    Args:
        color: Color name
    
    Returns:
        Dictionary with 'value', 'multiplier', 'tolerance', 'tempco'
    
    Example:
        >>> get_color_info('red')
        {'value': 2, 'multiplier': 100, 'tolerance': 2.0, 'tempco': 50}
    """
    color = _normalize_color(color)
    
    return {
        "color": color,
        "value": COLOR_VALUES.get(color),
        "multiplier": COLOR_MULTIPLIERS.get(color),
        "tolerance": COLOR_TOLERANCES.get(color),
        "tempco": COLOR_TEMPCO.get(color),
    }


# ============================================================================
# Module Exports
# ============================================================================

__all__ = [
    # Enums and constants
    'Color',
    'COLOR_VALUES',
    'COLOR_MULTIPLIERS',
    'COLOR_TOLERANCES',
    'COLOR_TEMPCO',
    'E_SERIES',
    'E96_VALUES',
    'E192_VALUES',
    
    # Decoding functions
    'decode_3band',
    'decode_4band',
    'decode_5band',
    'decode_6band',
    'decode_resistor',
    
    # Encoding functions
    'encode_4band',
    'encode_5band',
    'encode_6band',
    
    # SMD functions
    'decode_smd',
    'encode_smd',
    
    # E-series functions
    'get_e_series',
    'find_nearest_standard',
    'is_standard_value',
    
    # Circuit calculations
    'parallel_resistance',
    'series_resistance',
    'voltage_divider',
    'led_resistor',
    
    # Utilities
    'is_valid_color',
    'get_color_info',
    '_format_resistance',
    '_parse_resistance_string',
]


if __name__ == '__main__':
    # Quick demo
    print("AllToolkit Resistor Color Code Utils Demo")
    print("=" * 50)
    
    # Decode 4-band resistor
    colors = ['red', 'violet', 'yellow', 'gold']
    result = decode_4band(colors)
    print(f"\nDecode {colors}:")
    print(f"  Resistance: {result['resistance_str']} (±{result['tolerance']}%)")
    
    # Encode resistance
    result = encode_4band(4700, 5)
    print(f"\nEncode 4.7kΩ ±5%:")
    print(f"  Colors: {' - '.join(result['colors'])}")
    
    # SMD codes
    print(f"\nSMD Code '103': {decode_smd('103')['resistance_str']}")
    print(f"SMD Code '4R7': {decode_smd('4R7')['resistance_str']}")
    
    # Find nearest standard
    nearest = find_nearest_standard(5000, 'E12')
    print(f"\nNearest E12 to 5000Ω: {nearest['nearest_str']} ({nearest['error_percent']}% error)")
    
    # LED resistor
    r = led_resistor(5, 2, 0.02)
    print(f"\nLED resistor (5V, 2V LED, 20mA): {r:.1f}Ω")
    
    # Parallel resistance
    print(f"\nParallel 100Ω + 100Ω: {parallel_resistance([100, 100])}Ω")
    print(f"Series 100Ω + 200Ω: {series_resistance([100, 200])}Ω")
    
    print("\nFor full documentation, see README.md")