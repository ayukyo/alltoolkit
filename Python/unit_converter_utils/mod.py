#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Unit Converter Utilities Module
=============================================
A comprehensive unit conversion utility module for Python with zero external dependencies.

Features:
    - Length/Distance conversions (m, km, cm, mm, inch, foot, yard, mile, nautical mile)
    - Weight/Mass conversions (kg, g, mg, lb, oz, ton, metric ton)
    - Temperature conversions (Celsius, Fahrenheit, Kelvin)
    - Volume conversions (L, mL, gallon, quart, pint, cup, fluid oz)
    - Area conversions (m², km², cm², ft², in², acre, hectare)
    - Speed/Velocity conversions (m/s, km/h, mph, knot, ft/s)
    - Time conversions (s, min, h, day, week, month, year)
    - Data storage conversions (B, KB, MB, GB, TB, PB, bit, Kibit, Mibit)
    - Pressure conversions (Pa, bar, atm, psi, mmHg, Torr)
    - Energy conversions (J, kJ, cal, kcal, Wh, kWh, BTU, eV)
    - Power conversions (W, kW, MW, hp, BTU/h)
    - Batch conversions and unit validation

Author: AllToolkit Contributors
License: MIT
"""

from typing import Any, Dict, List, Optional, Tuple, Union
from enum import Enum


# ============================================================================
# Type Aliases
# ============================================================================

Number = Union[int, float]
ConversionResult = Tuple[float, str]


# ============================================================================
# Enums for Unit Categories
# ============================================================================

class LengthUnit(Enum):
    """Length/Distance units."""
    METER = "m"
    KILOMETER = "km"
    CENTIMETER = "cm"
    MILLIMETER = "mm"
    MICROMETER = "μm"
    NANOMETER = "nm"
    INCH = "in"
    FOOT = "ft"
    YARD = "yd"
    MILE = "mi"
    NAUTICAL_MILE = "nmi"


class WeightUnit(Enum):
    """Weight/Mass units."""
    KILOGRAM = "kg"
    GRAM = "g"
    MILLIGRAM = "mg"
    MICROGRAM = "μg"
    POUND = "lb"
    OUNCE = "oz"
    TON = "ton"  # Short ton (US)
    METRIC_TON = "t"
    STONE = "st"


class TemperatureUnit(Enum):
    """Temperature units."""
    CELSIUS = "°C"
    FAHRENHEIT = "°F"
    KELVIN = "K"


class VolumeUnit(Enum):
    """Volume units."""
    LITER = "L"
    MILLILITER = "mL"
    GALLON_US = "gal"
    QUART_US = "qt"
    PINT_US = "pt"
    CUP_US = "cup"
    FLUID_OUNCE_US = "fl oz"
    TABLESPOON = "tbsp"
    TEASPOON = "tsp"
    CUBIC_METER = "m³"
    CUBIC_CENTIMETER = "cm³"
    CUBIC_INCH = "in³"
    CUBIC_FOOT = "ft³"


class AreaUnit(Enum):
    """Area units."""
    SQUARE_METER = "m²"
    SQUARE_KILOMETER = "km²"
    SQUARE_CENTIMETER = "cm²"
    SQUARE_MILLIMETER = "mm²"
    SQUARE_FOOT = "ft²"
    SQUARE_INCH = "in²"
    SQUARE_YARD = "yd²"
    ACRE = "acre"
    HECTARE = "ha"


class SpeedUnit(Enum):
    """Speed/Velocity units."""
    METER_PER_SECOND = "m/s"
    KILOMETER_PER_HOUR = "km/h"
    MILE_PER_HOUR = "mph"
    KNOT = "kn"
    FOOT_PER_SECOND = "ft/s"


class TimeUnit(Enum):
    """Time units."""
    SECOND = "s"
    MILLISECOND = "ms"
    MICROSECOND = "μs"
    NANOSECOND = "ns"
    MINUTE = "min"
    HOUR = "h"
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    YEAR = "year"


class DataUnit(Enum):
    """Data storage units."""
    BIT = "bit"
    BYTE = "B"
    KILOBYTE = "KB"
    MEGABYTE = "MB"
    GIGABYTE = "GB"
    TERABYTE = "TB"
    PETABYTE = "PB"
    KIBIBYTE = "KiB"
    MEBIBYTE = "MiB"
    GIBIBYTE = "GiB"
    TEBIBYTE = "TiB"
    PEBIBYTE = "PiB"
    KIBIBIT = "Kibit"
    MEBIBIT = "Mibit"
    GIBIBIT = "Gibit"


class PressureUnit(Enum):
    """Pressure units."""
    PASCAL = "Pa"
    KILOPASCAL = "kPa"
    BAR = "bar"
    ATMOSPHERE = "atm"
    PSI = "psi"
    MMHG = "mmHg"
    TORR = "Torr"


class EnergyUnit(Enum):
    """Energy units."""
    JOULE = "J"
    KILOJOULE = "kJ"
    CALORIE = "cal"
    KILOCALORIE = "kcal"
    WATT_HOUR = "Wh"
    KILOWATT_HOUR = "kWh"
    BTU = "BTU"
    ELECTRON_VOLT = "eV"


class PowerUnit(Enum):
    """Power units."""
    WATT = "W"
    KILOWATT = "kW"
    MEGAWATT = "MW"
    HORSEPOWER = "hp"
    BTU_PER_HOUR = "BTU/h"


# ============================================================================
# Conversion Factors (to base unit)
# ============================================================================

# Length: base unit = meter
LENGTH_TO_METER: Dict[str, float] = {
    "m": 1.0,
    "km": 1000.0,
    "cm": 0.01,
    "mm": 0.001,
    "μm": 1e-6,
    "nm": 1e-9,
    "in": 0.0254,
    "ft": 0.3048,
    "yd": 0.9144,
    "mi": 1609.344,
    "nmi": 1852.0,
}

# Weight: base unit = kilogram
WEIGHT_TO_KG: Dict[str, float] = {
    "kg": 1.0,
    "g": 0.001,
    "mg": 1e-6,
    "μg": 1e-9,
    "lb": 0.45359237,
    "oz": 0.028349523125,
    "ton": 907.18474,  # Short ton
    "t": 1000.0,  # Metric ton
    "st": 6.35029318,  # Stone
}

# Volume: base unit = liter
VOLUME_TO_LITER: Dict[str, float] = {
    "L": 1.0,
    "mL": 0.001,
    "gal": 3.785411784,
    "qt": 0.946352946,
    "pt": 0.473176473,
    "cup": 0.2365882365,
    "fl oz": 0.0295735295625,
    "tbsp": 0.01478676478125,
    "tsp": 0.00492892159375,
    "m³": 1000.0,
    "cm³": 0.001,
    "in³": 0.016387064,
    "ft³": 28.316846592,
}

# Area: base unit = square meter
AREA_TO_SQM: Dict[str, float] = {
    "m²": 1.0,
    "km²": 1e6,
    "cm²": 0.0001,
    "mm²": 1e-6,
    "ft²": 0.09290304,
    "in²": 0.00064516,
    "yd²": 0.83612736,
    "acre": 4046.8564224,
    "ha": 10000.0,
}

# Speed: base unit = meter per second
SPEED_TO_MPS: Dict[str, float] = {
    "m/s": 1.0,
    "km/h": 0.2777777777777778,  # 1/3.6
    "mph": 0.44704,
    "kn": 0.5144444444444444,
    "ft/s": 0.3048,
}

# Time: base unit = second
TIME_TO_SECOND: Dict[str, float] = {
    "s": 1.0,
    "ms": 0.001,
    "μs": 1e-6,
    "ns": 1e-9,
    "min": 60.0,
    "h": 3600.0,
    "day": 86400.0,
    "week": 604800.0,
    "month": 2629746.0,  # Average month (30.44 days)
    "year": 31556952.0,  # Julian year
}

# Data: base unit = byte
DATA_TO_BYTE: Dict[str, float] = {
    "bit": 0.125,
    "B": 1.0,
    "KB": 1000.0,
    "MB": 1e6,
    "GB": 1e9,
    "TB": 1e12,
    "PB": 1e15,
    "KiB": 1024.0,
    "MiB": 1048576.0,
    "GiB": 1073741824.0,
    "TiB": 1099511627776.0,
    "PiB": 1125899906842624.0,
    "Kibit": 128.0,
    "Mibit": 131072.0,
    "Gibit": 134217728.0,
}

# Pressure: base unit = Pascal
PRESSURE_TO_PA: Dict[str, float] = {
    "Pa": 1.0,
    "kPa": 1000.0,
    "bar": 100000.0,
    "atm": 101325.0,
    "psi": 6894.757293168,
    "mmHg": 133.322387415,
    "Torr": 133.322368421,
}

# Energy: base unit = Joule
ENERGY_TO_JOULE: Dict[str, float] = {
    "J": 1.0,
    "kJ": 1000.0,
    "cal": 4.184,
    "kcal": 4184.0,
    "Wh": 3600.0,
    "kWh": 3600000.0,
    "BTU": 1055.05585262,
    "eV": 1.602176634e-19,
}

# Power: base unit = Watt
POWER_TO_WATT: Dict[str, float] = {
    "W": 1.0,
    "kW": 1000.0,
    "MW": 1e6,
    "hp": 745.6998715822702,
    "BTU/h": 0.2930710701722222,
}


# ============================================================================
# Utility Functions
# ============================================================================

def _to_float(value: Any) -> float:
    """Convert value to float safely."""
    try:
        return float(value)
    except (TypeError, ValueError):
        raise ValueError(f"Cannot convert '{value}' to a number")


def _validate_positive(value: float, name: str = "Value") -> None:
    """Validate that a value is positive (for units that require it)."""
    if value < 0:
        raise ValueError(f"{name} cannot be negative: {value}")


def _validate_non_negative(value: float, name: str = "Value") -> None:
    """Validate that a value is non-negative."""
    if value < 0:
        raise ValueError(f"{name} cannot be negative: {value}")


def _get_unit_symbol(unit: Union[str, Enum]) -> str:
    """Get the symbol for a unit."""
    if isinstance(unit, Enum):
        return unit.value
    return str(unit)


def _find_unit_key(unit: str, mapping: Dict[str, float]) -> str:
    """Find the key for a unit in a mapping (case-insensitive)."""
    unit_lower = unit.lower()
    for key in mapping:
        if key.lower() == unit_lower:
            return key
    raise ValueError(f"Unknown unit: {unit}. Valid units: {list(mapping.keys())}")


# ============================================================================
# Length Conversions
# ============================================================================

def convert_length(value: Number, from_unit: str, to_unit: str) -> float:
    """
    Convert length/distance between units.
    
    Args:
        value: The value to convert
        from_unit: Source unit (e.g., 'm', 'km', 'ft', 'in')
        to_unit: Target unit
    
    Returns:
        Converted value
    
    Example:
        >>> convert_length(1, 'km', 'm')
        1000.0
        >>> convert_length(1, 'mile', 'km')
        1.609344
        >>> convert_length(100, 'cm', 'in')
        39.37007874015748
    """
    value = _to_float(value)
    from_key = _find_unit_key(from_unit, LENGTH_TO_METER)
    to_key = _find_unit_key(to_unit, LENGTH_TO_METER)
    
    # Convert to meters, then to target unit
    meters = value * LENGTH_TO_METER[from_key]
    return meters / LENGTH_TO_METER[to_key]


def meters_to_feet(meters: Number) -> float:
    """Convert meters to feet."""
    return convert_length(meters, 'm', 'ft')


def feet_to_meters(feet: Number) -> float:
    """Convert feet to meters."""
    return convert_length(feet, 'ft', 'm')


def kilometers_to_miles(km: Number) -> float:
    """Convert kilometers to miles."""
    return convert_length(km, 'km', 'mi')


def miles_to_kilometers(miles: Number) -> float:
    """Convert miles to kilometers."""
    return convert_length(miles, 'mi', 'km')


def inches_to_centimeters(inches: Number) -> float:
    """Convert inches to centimeters."""
    return convert_length(inches, 'in', 'cm')


def centimeters_to_inches(cm: Number) -> float:
    """Convert centimeters to inches."""
    return convert_length(cm, 'cm', 'in')


# ============================================================================
# Weight Conversions
# ============================================================================

def convert_weight(value: Number, from_unit: str, to_unit: str) -> float:
    """
    Convert weight/mass between units.
    
    Args:
        value: The value to convert
        from_unit: Source unit (e.g., 'kg', 'lb', 'oz', 'g')
        to_unit: Target unit
    
    Returns:
        Converted value
    
    Example:
        >>> convert_weight(1, 'kg', 'lb')
        2.2046226218487757
        >>> convert_weight(16, 'oz', 'lb')
        1.0
        >>> convert_weight(1, 'ton', 'kg')
        907.18474
    """
    value = _to_float(value)
    _validate_non_negative(value, "Weight")
    
    from_key = _find_unit_key(from_unit, WEIGHT_TO_KG)
    to_key = _find_unit_key(to_unit, WEIGHT_TO_KG)
    
    # Convert to kg, then to target unit
    kg = value * WEIGHT_TO_KG[from_key]
    return kg / WEIGHT_TO_KG[to_key]


def kg_to_pounds(kg: Number) -> float:
    """Convert kilograms to pounds."""
    return convert_weight(kg, 'kg', 'lb')


def pounds_to_kg(pounds: Number) -> float:
    """Convert pounds to kilograms."""
    return convert_weight(pounds, 'lb', 'kg')


def grams_to_ounces(grams: Number) -> float:
    """Convert grams to ounces."""
    return convert_weight(grams, 'g', 'oz')


def ounces_to_grams(ounces: Number) -> float:
    """Convert ounces to grams."""
    return convert_weight(ounces, 'oz', 'g')


# ============================================================================
# Temperature Conversions
# ============================================================================

def convert_temperature(value: Number, from_unit: str, to_unit: str) -> float:
    """
    Convert temperature between units.
    
    Args:
        value: The value to convert
        from_unit: Source unit ('C', 'F', 'K', '°C', '°F')
        to_unit: Target unit
    
    Returns:
        Converted value
    
    Example:
        >>> convert_temperature(0, 'C', 'F')
        32.0
        >>> convert_temperature(100, 'C', 'F')
        212.0
        >>> convert_temperature(32, 'F', 'C')
        0.0
        >>> convert_temperature(0, 'C', 'K')
        273.15
    """
    value = _to_float(value)
    from_unit = from_unit.replace('°', '').upper()
    to_unit = to_unit.replace('°', '').upper()
    
    # Normalize unit names
    if from_unit in ('CELSIUS', 'C'):
        from_unit = 'C'
    elif from_unit in ('FAHRENHEIT', 'F'):
        from_unit = 'F'
    elif from_unit in ('KELVIN', 'K'):
        from_unit = 'K'
    else:
        raise ValueError(f"Unknown temperature unit: {from_unit}. Use 'C', 'F', or 'K'")
    
    if to_unit in ('CELSIUS', 'C'):
        to_unit = 'C'
    elif to_unit in ('FAHRENHEIT', 'F'):
        to_unit = 'F'
    elif to_unit in ('KELVIN', 'K'):
        to_unit = 'K'
    else:
        raise ValueError(f"Unknown temperature unit: {to_unit}. Use 'C', 'F', or 'K'")
    
    # Validate absolute zero
    if from_unit == 'C' and value < -273.15:
        raise ValueError("Temperature below absolute zero")
    if from_unit == 'F' and value < -459.67:
        raise ValueError("Temperature below absolute zero")
    if from_unit == 'K' and value < 0:
        raise ValueError("Temperature below absolute zero")
    
    # Convert to Celsius first
    if from_unit == 'C':
        celsius = value
    elif from_unit == 'F':
        celsius = (value - 32) * 5 / 9
    else:  # Kelvin
        celsius = value - 273.15
    
    # Convert from Celsius to target
    if to_unit == 'C':
        return celsius
    elif to_unit == 'F':
        return celsius * 9 / 5 + 32
    else:  # Kelvin
        return celsius + 273.15


def celsius_to_fahrenheit(celsius: Number) -> float:
    """Convert Celsius to Fahrenheit."""
    return convert_temperature(celsius, 'C', 'F')


def fahrenheit_to_celsius(fahrenheit: Number) -> float:
    """Convert Fahrenheit to Celsius."""
    return convert_temperature(fahrenheit, 'F', 'C')


def celsius_to_kelvin(celsius: Number) -> float:
    """Convert Celsius to Kelvin."""
    return convert_temperature(celsius, 'C', 'K')


def kelvin_to_celsius(kelvin: Number) -> float:
    """Convert Kelvin to Celsius."""
    return convert_temperature(kelvin, 'K', 'C')


def fahrenheit_to_kelvin(fahrenheit: Number) -> float:
    """Convert Fahrenheit to Kelvin."""
    return convert_temperature(fahrenheit, 'F', 'K')


def kelvin_to_fahrenheit(kelvin: Number) -> float:
    """Convert Kelvin to Fahrenheit."""
    return convert_temperature(kelvin, 'K', 'F')


# ============================================================================
# Volume Conversions
# ============================================================================

def convert_volume(value: Number, from_unit: str, to_unit: str) -> float:
    """
    Convert volume between units.
    
    Args:
        value: The value to convert
        from_unit: Source unit (e.g., 'L', 'mL', 'gal', 'cup')
        to_unit: Target unit
    
    Returns:
        Converted value
    
    Example:
        >>> convert_volume(1, 'L', 'mL')
        1000.0
        >>> convert_volume(1, 'gal', 'L')
        3.785411784
        >>> convert_volume(4, 'cup', 'L')
        0.946352946
    """
    value = _to_float(value)
    _validate_non_negative(value, "Volume")
    
    from_key = _find_unit_key(from_unit, VOLUME_TO_LITER)
    to_key = _find_unit_key(to_unit, VOLUME_TO_LITER)
    
    # Convert to liters, then to target unit
    liters = value * VOLUME_TO_LITER[from_key]
    return liters / VOLUME_TO_LITER[to_key]


def liters_to_gallons(liters: Number) -> float:
    """Convert liters to gallons (US)."""
    return convert_volume(liters, 'L', 'gal')


def gallons_to_liters(gallons: Number) -> float:
    """Convert gallons (US) to liters."""
    return convert_volume(gallons, 'gal', 'L')


def milliliters_to_fluid_ounces(ml: Number) -> float:
    """Convert milliliters to fluid ounces (US)."""
    return convert_volume(ml, 'mL', 'fl oz')


def fluid_ounces_to_milliliters(fl_oz: Number) -> float:
    """Convert fluid ounces (US) to milliliters."""
    return convert_volume(fl_oz, 'fl oz', 'mL')


# ============================================================================
# Area Conversions
# ============================================================================

def convert_area(value: Number, from_unit: str, to_unit: str) -> float:
    """
    Convert area between units.
    
    Args:
        value: The value to convert
        from_unit: Source unit (e.g., 'm²', 'ft²', 'acre', 'ha')
        to_unit: Target unit
    
    Returns:
        Converted value
    
    Example:
        >>> convert_area(1, 'ha', 'm²')
        10000.0
        >>> convert_area(1, 'acre', 'm²')
        4046.8564224
        >>> convert_area(100, 'm²', 'ft²')
        1076.3910416709722
    """
    value = _to_float(value)
    _validate_non_negative(value, "Area")
    
    from_key = _find_unit_key(from_unit, AREA_TO_SQM)
    to_key = _find_unit_key(to_unit, AREA_TO_SQM)
    
    # Convert to square meters, then to target unit
    sqm = value * AREA_TO_SQM[from_key]
    return sqm / AREA_TO_SQM[to_key]


def square_meters_to_square_feet(sq_m: Number) -> float:
    """Convert square meters to square feet."""
    return convert_area(sq_m, 'm²', 'ft²')


def square_feet_to_square_meters(sq_ft: Number) -> float:
    """Convert square feet to square meters."""
    return convert_area(sq_ft, 'ft²', 'm²')


def acres_to_hectares(acres: Number) -> float:
    """Convert acres to hectares."""
    return convert_area(acres, 'acre', 'ha')


def hectares_to_acres(hectares: Number) -> float:
    """Convert hectares to acres."""
    return convert_area(hectares, 'ha', 'acre')


# ============================================================================
# Speed Conversions
# ============================================================================

def convert_speed(value: Number, from_unit: str, to_unit: str) -> float:
    """
    Convert speed/velocity between units.
    
    Args:
        value: The value to convert
        from_unit: Source unit (e.g., 'km/h', 'mph', 'm/s', 'kn')
        to_unit: Target unit
    
    Returns:
        Converted value
    
    Example:
        >>> convert_speed(100, 'km/h', 'mph')
        62.137119223733395
        >>> convert_speed(1, 'm/s', 'km/h')
        3.6
        >>> convert_speed(1, 'knot', 'km/h')
        1.8519999999999998
    """
    value = _to_float(value)
    _validate_non_negative(value, "Speed")
    
    from_key = _find_unit_key(from_unit, SPEED_TO_MPS)
    to_key = _find_unit_key(to_unit, SPEED_TO_MPS)
    
    # Convert to m/s, then to target unit
    mps = value * SPEED_TO_MPS[from_key]
    return mps / SPEED_TO_MPS[to_key]


def kmh_to_mph(kmh: Number) -> float:
    """Convert km/h to mph."""
    return convert_speed(kmh, 'km/h', 'mph')


def mph_to_kmh(mph: Number) -> float:
    """Convert mph to km/h."""
    return convert_speed(mph, 'mph', 'km/h')


def ms_to_kmh(ms: Number) -> float:
    """Convert m/s to km/h."""
    return convert_speed(ms, 'm/s', 'km/h')


def knots_to_kmh(knots: Number) -> float:
    """Convert knots to km/h."""
    return convert_speed(knots, 'kn', 'km/h')


# ============================================================================
# Time Conversions
# ============================================================================

def convert_time(value: Number, from_unit: str, to_unit: str) -> float:
    """
    Convert time between units.
    
    Args:
        value: The value to convert
        from_unit: Source unit (e.g., 's', 'min', 'h', 'day', 'week')
        to_unit: Target unit
    
    Returns:
        Converted value
    
    Example:
        >>> convert_time(1, 'h', 'min')
        60.0
        >>> convert_time(1, 'day', 'h')
        24.0
        >>> convert_time(60, 's', 'min')
        1.0
    """
    value = _to_float(value)
    _validate_non_negative(value, "Time")
    
    from_key = _find_unit_key(from_unit, TIME_TO_SECOND)
    to_key = _find_unit_key(to_unit, TIME_TO_SECOND)
    
    # Convert to seconds, then to target unit
    seconds = value * TIME_TO_SECOND[from_key]
    return seconds / TIME_TO_SECOND[to_key]


def hours_to_minutes(hours: Number) -> float:
    """Convert hours to minutes."""
    return convert_time(hours, 'h', 'min')


def minutes_to_seconds(minutes: Number) -> float:
    """Convert minutes to seconds."""
    return convert_time(minutes, 'min', 's')


def days_to_hours(days: Number) -> float:
    """Convert days to hours."""
    return convert_time(days, 'day', 'h')


def weeks_to_days(weeks: Number) -> float:
    """Convert weeks to days."""
    return convert_time(weeks, 'week', 'day')


def years_to_days(years: Number) -> float:
    """Convert years to days."""
    return convert_time(years, 'year', 'day')


# ============================================================================
# Data Storage Conversions
# ============================================================================

def convert_data(value: Number, from_unit: str, to_unit: str) -> float:
    """
    Convert data storage between units.
    
    Args:
        value: The value to convert
        from_unit: Source unit (e.g., 'GB', 'MB', 'GiB', 'TB')
        to_unit: Target unit
    
    Returns:
        Converted value
    
    Example:
        >>> convert_data(1, 'GB', 'MB')
        1000.0
        >>> convert_data(1, 'GiB', 'MiB')
        1024.0
        >>> convert_data(1, 'TB', 'GB')
        1000.0
    """
    value = _to_float(value)
    _validate_non_negative(value, "Data")
    
    from_key = _find_unit_key(from_unit, DATA_TO_BYTE)
    to_key = _find_unit_key(to_unit, DATA_TO_BYTE)
    
    # Convert to bytes, then to target unit
    bytes_val = value * DATA_TO_BYTE[from_key]
    return bytes_val / DATA_TO_BYTE[to_key]


def gb_to_mb(gb: Number) -> float:
    """Convert gigabytes to megabytes (decimal)."""
    return convert_data(gb, 'GB', 'MB')


def gib_to_mib(gib: Number) -> float:
    """Convert gibibytes to mebibytes (binary)."""
    return convert_data(gib, 'GiB', 'MiB')


def tb_to_gb(tb: Number) -> float:
    """Convert terabytes to gigabytes (decimal)."""
    return convert_data(tb, 'TB', 'GB')


def bytes_to_bits(bytes_val: Number) -> float:
    """Convert bytes to bits."""
    return convert_data(bytes_val, 'B', 'bit')


def bits_to_bytes(bits: Number) -> float:
    """Convert bits to bytes."""
    return convert_data(bits, 'bit', 'B')


# ============================================================================
# Pressure Conversions
# ============================================================================

def convert_pressure(value: Number, from_unit: str, to_unit: str) -> float:
    """
    Convert pressure between units.
    
    Args:
        value: The value to convert
        from_unit: Source unit (e.g., 'Pa', 'bar', 'atm', 'psi')
        to_unit: Target unit
    
    Returns:
        Converted value
    
    Example:
        >>> convert_pressure(1, 'atm', 'Pa')
        101325.0
        >>> convert_pressure(1, 'bar', 'psi')
        14.50377377304066
        >>> convert_pressure(760, 'mmHg', 'atm')
        0.9999998462107669
    """
    value = _to_float(value)
    _validate_non_negative(value, "Pressure")
    
    from_key = _find_unit_key(from_unit, PRESSURE_TO_PA)
    to_key = _find_unit_key(to_unit, PRESSURE_TO_PA)
    
    # Convert to Pascal, then to target unit
    pa = value * PRESSURE_TO_PA[from_key]
    return pa / PRESSURE_TO_PA[to_key]


def atm_to_pascal(atm: Number) -> float:
    """Convert atmospheres to Pascal."""
    return convert_pressure(atm, 'atm', 'Pa')


def psi_to_bar(psi: Number) -> float:
    """Convert PSI to bar."""
    return convert_pressure(psi, 'psi', 'bar')


def bar_to_psi(bar: Number) -> float:
    """Convert bar to PSI."""
    return convert_pressure(bar, 'bar', 'psi')


# ============================================================================
# Energy Conversions
# ============================================================================

def convert_energy(value: Number, from_unit: str, to_unit: str) -> float:
    """
    Convert energy between units.
    
    Args:
        value: The value to convert
        from_unit: Source unit (e.g., 'J', 'kJ', 'cal', 'kWh')
        to_unit: Target unit
    
    Returns:
        Converted value
    
    Example:
        >>> convert_energy(1, 'kJ', 'J')
        1000.0
        >>> convert_energy(1, 'kcal', 'kJ')
        4.184
        >>> convert_energy(1, 'kWh', 'J')
        3600000.0
    """
    value = _to_float(value)
    _validate_non_negative(value, "Energy")
    
    from_key = _find_unit_key(from_unit, ENERGY_TO_JOULE)
    to_key = _find_unit_key(to_unit, ENERGY_TO_JOULE)
    
    # Convert to Joules, then to target unit
    joules = value * ENERGY_TO_JOULE[from_key]
    return joules / ENERGY_TO_JOULE[to_key]


def kwh_to_joules(kwh: Number) -> float:
    """Convert kilowatt-hours to Joules."""
    return convert_energy(kwh, 'kWh', 'J')


def calories_to_joules(cal: Number) -> float:
    """Convert calories to Joules."""
    return convert_energy(cal, 'cal', 'J')


def btu_to_kwh(btu: Number) -> float:
    """Convert BTU to kilowatt-hours."""
    return convert_energy(btu, 'BTU', 'kWh')


# ============================================================================
# Power Conversions
# ============================================================================

def convert_power(value: Number, from_unit: str, to_unit: str) -> float:
    """
    Convert power between units.
    
    Args:
        value: The value to convert
        from_unit: Source unit (e.g., 'W', 'kW', 'hp')
        to_unit: Target unit
    
    Returns:
        Converted value
    
    Example:
        >>> convert_power(1, 'kW', 'W')
        1000.0
        >>> convert_power(1, 'hp', 'kW')
        0.7456998715822702
        >>> convert_power(1000, 'W', 'kW')
        1.0
    """
    value = _to_float(value)
    _validate_non_negative(value, "Power")
    
    from_key = _find_unit_key(from_unit, POWER_TO_WATT)
    to_key = _find_unit_key(to_unit, POWER_TO_WATT)
    
    # Convert to Watts, then to target unit
    watts = value * POWER_TO_WATT[from_key]
    return watts / POWER_TO_WATT[to_key]


def hp_to_kw(hp: Number) -> float:
    """Convert horsepower to kilowatts."""
    return convert_power(hp, 'hp', 'kW')


def kw_to_hp(kw: Number) -> float:
    """Convert kilowatts to horsepower."""
    return convert_power(kw, 'kW', 'hp')


def mw_to_kw(mw: Number) -> float:
    """Convert megawatts to kilowatts."""
    return convert_power(mw, 'MW', 'kW')


# ============================================================================
# Batch Conversions
# ============================================================================

def batch_convert_length(values: List[Number], from_unit: str, to_unit: str) -> List[float]:
    """
    Convert multiple length values.
    
    Args:
        values: List of values to convert
        from_unit: Source unit
        to_unit: Target unit
    
    Returns:
        List of converted values
    
    Example:
        >>> batch_convert_length([1, 2, 3], 'km', 'm')
        [1000.0, 2000.0, 3000.0]
    """
    return [convert_length(v, from_unit, to_unit) for v in values]


def batch_convert_weight(values: List[Number], from_unit: str, to_unit: str) -> List[float]:
    """Convert multiple weight values."""
    return [convert_weight(v, from_unit, to_unit) for v in values]


def batch_convert_temperature(values: List[Number], from_unit: str, to_unit: str) -> List[float]:
    """Convert multiple temperature values."""
    return [convert_temperature(v, from_unit, to_unit) for v in values]


# ============================================================================
# Unit Information
# ============================================================================

def get_available_units(category: str) -> List[str]:
    """
    Get list of available units for a category.
    
    Args:
        category: Category name ('length', 'weight', 'temperature', 'volume',
                  'area', 'speed', 'time', 'data', 'pressure', 'energy', 'power')
    
    Returns:
        List of unit symbols
    
    Example:
        >>> 'm' in get_available_units('length')
        True
        >>> 'kg' in get_available_units('weight')
        True
    """
    category = category.lower()
    mapping = {
        'length': LENGTH_TO_METER,
        'weight': WEIGHT_TO_KG,
        'temperature': {'C': 1, 'F': 1, 'K': 1},  # Special handling
        'volume': VOLUME_TO_LITER,
        'area': AREA_TO_SQM,
        'speed': SPEED_TO_MPS,
        'time': TIME_TO_SECOND,
        'data': DATA_TO_BYTE,
        'pressure': PRESSURE_TO_PA,
        'energy': ENERGY_TO_JOULE,
        'power': POWER_TO_WATT,
    }
    
    if category not in mapping:
        raise ValueError(f"Unknown category: {category}. Valid: {list(mapping.keys())}")
    
    return list(mapping[category].keys())


def get_unit_info(unit: str) -> Optional[Dict[str, Any]]:
    """
    Get information about a specific unit.
    
    Args:
        unit: Unit symbol
    
    Returns:
        Dict with 'category', 'symbol', 'name' or None if not found
    
    Example:
        >>> info = get_unit_info('km')
        >>> info['category']
        'length'
    """
    unit_info = {
        'm': ('length', 'Meter'),
        'km': ('length', 'Kilometer'),
        'cm': ('length', 'Centimeter'),
        'mm': ('length', 'Millimeter'),
        'in': ('length', 'Inch'),
        'ft': ('length', 'Foot'),
        'yd': ('length', 'Yard'),
        'mi': ('length', 'Mile'),
        'kg': ('weight', 'Kilogram'),
        'g': ('weight', 'Gram'),
        'lb': ('weight', 'Pound'),
        'oz': ('weight', 'Ounce'),
        'L': ('volume', 'Liter'),
        'mL': ('volume', 'Milliliter'),
        'gal': ('volume', 'Gallon'),
        '°C': ('temperature', 'Celsius'),
        '°F': ('temperature', 'Fahrenheit'),
        'K': ('temperature', 'Kelvin'),
    }
    
    if unit in unit_info:
        category, name = unit_info[unit]
        return {'category': category, 'symbol': unit, 'name': name}
    return None


# ============================================================================
# Convenience Functions
# ============================================================================

def convert(value: Number, from_unit: str, to_unit: str) -> float:
    """
    Universal conversion function (auto-detects category).
    
    Args:
        value: The value to convert
        from_unit: Source unit
        to_unit: Target unit
    
    Returns:
        Converted value
    
    Example:
        >>> convert(100, 'C', 'F')  # Temperature
        212.0
        >>> convert(1, 'km', 'mi')  # Length
        0.6213711922373339
    """
    # Try each category
    converters = [
        (LENGTH_TO_METER, convert_length),
        (WEIGHT_TO_KG, convert_weight),
        (VOLUME_TO_LITER, convert_volume),
        (AREA_TO_SQM, convert_area),
        (SPEED_TO_MPS, convert_speed),
        (TIME_TO_SECOND, convert_time),
        (DATA_TO_BYTE, convert_data),
        (PRESSURE_TO_PA, convert_pressure),
        (ENERGY_TO_JOULE, convert_energy),
        (POWER_TO_WATT, convert_power),
    ]
    
    for mapping, converter in converters:
        try:
            _find_unit_key(from_unit, mapping)
            _find_unit_key(to_unit, mapping)
            return converter(value, from_unit, to_unit)
        except ValueError:
            continue
    
    # Try temperature as last resort (special handling)
    try:
        return convert_temperature(value, from_unit, to_unit)
    except ValueError:
        pass
    
    raise ValueError(f"Cannot convert between '{from_unit}' and '{to_unit}'. "
                     f"Units may be from different categories or invalid.")


def format_conversion(value: Number, from_unit: str, to_unit: str, 
                      precision: int = 4) -> str:
    """
    Convert and format result as a string.
    
    Args:
        value: The value to convert
        from_unit: Source unit
        to_unit: Target unit
        precision: Decimal places
    
    Returns:
        Formatted string like "100.0000 m"
    
    Example:
        >>> format_conversion(1, 'km', 'm')
        '1000.0000 m'
        >>> format_conversion(1, 'mile', 'km', precision=2)
        '1.61 km'
    """
    result = convert(value, from_unit, to_unit)
    return f"{result:.{precision}f} {to_unit}"


# ============================================================================
# Module Exports
# ============================================================================

__all__ = [
    # Enums
    'LengthUnit', 'WeightUnit', 'TemperatureUnit', 'VolumeUnit',
    'AreaUnit', 'SpeedUnit', 'TimeUnit', 'DataUnit', 'PressureUnit',
    'EnergyUnit', 'PowerUnit',
    
    # Type aliases
    'Number', 'ConversionResult', 'Point2D', 'Point3D',
    
    # Main conversion functions
    'convert_length', 'convert_weight', 'convert_temperature',
    'convert_volume', 'convert_area', 'convert_speed',
    'convert_time', 'convert_data', 'convert_pressure',
    'convert_energy', 'convert_power',
    
    # Convenience functions
    'convert', 'format_conversion',
    
    # Length shortcuts
    'meters_to_feet', 'feet_to_meters', 'kilometers_to_miles',
    'miles_to_kilometers', 'inches_to_centimeters', 'centimeters_to_inches',
    
    # Weight shortcuts
    'kg_to_pounds', 'pounds_to_kg', 'grams_to_ounces', 'ounces_to_grams',
    
    # Temperature shortcuts
    'celsius_to_fahrenheit', 'fahrenheit_to_celsius', 'celsius_to_kelvin',
    'kelvin_to_celsius', 'fahrenheit_to_kelvin', 'kelvin_to_fahrenheit',
    
    # Volume shortcuts
    'liters_to_gallons', 'gallons_to_liters',
    'milliliters_to_fluid_ounces', 'fluid_ounces_to_milliliters',
    
    # Area shortcuts
    'square_meters_to_square_feet', 'square_feet_to_square_meters',
    'acres_to_hectares', 'hectares_to_acres',
    
    # Speed shortcuts
    'kmh_to_mph', 'mph_to_kmh', 'ms_to_kmh', 'knots_to_kmh',
    
    # Time shortcuts
    'hours_to_minutes', 'minutes_to_seconds', 'days_to_hours',
    'weeks_to_days', 'years_to_days',
    
    # Data shortcuts
    'gb_to_mb', 'gib_to_mib', 'tb_to_gb', 'bytes_to_bits', 'bits_to_bytes',
    
    # Pressure shortcuts
    'atm_to_pascal', 'psi_to_bar', 'bar_to_psi',
    
    # Energy shortcuts
    'kwh_to_joules', 'calories_to_joules', 'btu_to_kwh',
    
    # Power shortcuts
    'hp_to_kw', 'kw_to_hp', 'mw_to_kw',
    
    # Batch conversions
    'batch_convert_length', 'batch_convert_weight', 'batch_convert_temperature',
    
    # Unit info
    'get_available_units', 'get_unit_info',
]


if __name__ == '__main__':
    # Quick demo
    print("AllToolkit - Unit Converter Utils Demo")
    print("=" * 50)
    
    print("\nLength:")
    print(f"  1 km = {convert_length(1, 'km', 'mi'):.4f} mi")
    print(f"  100 m = {convert_length(100, 'm', 'ft'):.4f} ft")
    
    print("\nWeight:")
    print(f"  1 kg = {convert_weight(1, 'kg', 'lb'):.4f} lb")
    print(f"  16 oz = {convert_weight(16, 'oz', 'g'):.4f} g")
    
    print("\nTemperature:")
    print(f"  0°C = {convert_temperature(0, 'C', 'F'):.1f}°F")
    print(f"  100°C = {convert_temperature(100, 'C', 'F'):.1f}°F")
    print(f"  32°F = {convert_temperature(32, 'F', 'C'):.1f}°C")
    
    print("\nVolume:")
    print(f"  1 gal = {convert_volume(1, 'gal', 'L'):.4f} L")
    print(f"  1 L = {convert_volume(1, 'L', 'cup'):.4f} cups")
    
    print("\nData:")
    print(f"  1 GB = {convert_data(1, 'GB', 'MB'):.0f} MB")
    print(f"  1 GiB = {convert_data(1, 'GiB', 'MiB'):.0f} MiB")
    
    print("\nSpeed:")
    print(f"  100 km/h = {convert_speed(100, 'km/h', 'mph'):.2f} mph")
    print(f"  60 mph = {convert_speed(60, 'mph', 'km/h'):.2f} km/h")
