#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - VIN (Vehicle Identification Number) Decoder Utilities
==================================================================
A comprehensive VIN decoder module with zero external dependencies.

Features:
    - VIN validation (check digit verification)
    - WMI (World Manufacturer Identifier) decoding
    - Model year decoding
    - Country of origin identification
    - Region identification
    - Manufacturer lookup
    - Full VIN information extraction
    - VIN generation for testing

The VIN is a 17-character code that uniquely identifies a motor vehicle.
Standard: ISO 3779 / ISO 3780

Author: AllToolkit Contributors
License: MIT
"""

import re
import datetime
from typing import Dict, List, Optional, Tuple, NamedTuple
from enum import Enum


# =============================================================================
# Constants
# =============================================================================

# VIN cannot contain I, O, Q (easily confused with 1, 0)
VIN_PATTERN = re.compile(r'^[A-HJ-NPR-Z0-9]{17}$')

# Transliteration values for check digit calculation
# A=1, B=2, ..., H=8 (no I), J=1, K=2, ..., R=9 (no O, Q)
TRANSLITERATION = {
    'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8,
    'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'P': 7, 'R': 9,
    'S': 2, 'T': 3, 'U': 4, 'V': 5, 'W': 6, 'X': 7, 'Y': 8, 'Z': 9,
    '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9
}

# Position weights for check digit (positions 1-17, position 9 is check digit with weight 0)
POSITION_WEIGHTS = [8, 7, 6, 5, 4, 3, 2, 10, 0, 9, 8, 7, 6, 5, 4, 3, 2]

# Model year codes - maps code to base year (1980-2009 cycle)
# Note: Same codes repeat for 2010-2039 cycle
YEAR_CODE_BASE = {
    'A': 1980, 'B': 1981, 'C': 1982, 'D': 1983, 'E': 1984, 'F': 1985,
    'G': 1986, 'H': 1987, 'J': 1988, 'K': 1989, 'L': 1990, 'M': 1991,
    'N': 1992, 'P': 1993, 'R': 1994, 'S': 1995, 'T': 1996, 'V': 1997,
    'W': 1998, 'X': 1999, 'Y': 2000,
    '1': 2001, '2': 2002, '3': 2003, '4': 2004, '5': 2005,
    '6': 2006, '7': 2007, '8': 2008, '9': 2009,
}

# Reverse mapping: year to code (for generation)
YEAR_TO_CODE = {}
for code, year in YEAR_CODE_BASE.items():
    YEAR_TO_CODE[year] = code
    # Also add second cycle years (2010-2039)
    YEAR_TO_CODE[year + 30] = code


# Country/Region codes by first character
REGION_CODES = {
    'A': 'Africa',
    'B': 'Africa',
    'C': 'Africa',
    'D': 'Africa',
    'E': 'Europe',
    'F': 'Europe',
    'G': 'Europe',
    'H': 'Europe',
    'J': 'Asia',
    'K': 'Asia',
    'L': 'Asia',
    'M': 'Asia',
    'N': 'Asia',
    'P': 'Asia',
    'R': 'Asia',
    'S': 'Europe',
    'T': 'Europe',
    'U': 'Europe',
    'V': 'Europe',
    'W': 'Europe',
    'X': 'Europe',
    'Y': 'Europe',
    'Z': 'Europe',
    '1': 'North America',
    '2': 'North America',
    '3': 'North America',
    '4': 'North America',
    '5': 'North America',
    '6': 'Oceania',
    '7': 'Oceania',
    '8': 'South America',
    '9': 'South America',
}


# WMI (World Manufacturer Identifier) database
# Format: WMI prefix -> (Manufacturer, Country)
WMI_DATABASE = {
    # United States
    '1A': ('Audi', 'USA'),
    '1B': ('BMW', 'USA'),
    '1C': ('Chrysler', 'USA'),
    '1D': ('Daimler', 'USA'),
    '1F': ('Ford', 'USA'),
    '1G': ('General Motors', 'USA'),
    '1H': ('Honda', 'USA'),
    '1J': ('Jeep', 'USA'),
    '1L': ('Lincoln', 'USA'),
    '1M': ('Mercury', 'USA'),
    '1N': ('Nissan', 'USA'),
    '1P': ('Porsche', 'USA'),
    '1R': ('Rolls-Royce', 'USA'),
    '1S': ('Subaru', 'USA'),
    '1T': ('Toyota', 'USA'),
    '1V': ('Volkswagen', 'USA'),
    '1W': ('Willys', 'USA'),
    '1X': ('Kenworth', 'USA'),
    '1Y': ('Mazda', 'USA'),
    '1Z': ('Ford', 'USA'),
    
    # Canada
    '2A': ('Audi', 'Canada'),
    '2B': ('BMW', 'Canada'),
    '2C': ('Chrysler', 'Canada'),
    '2F': ('Ford', 'Canada'),
    '2G': ('General Motors', 'Canada'),
    '2H': ('Honda', 'Canada'),
    '2M': ('Mazda', 'Canada'),
    '2P': ('Porsche', 'Canada'),
    '2T': ('Toyota', 'Canada'),
    '2V': ('Volkswagen', 'Canada'),
    
    # Mexico
    '3A': ('Audi', 'Mexico'),
    '3B': ('BMW', 'Mexico'),
    '3C': ('Chrysler', 'Mexico'),
    '3D': ('Daimler', 'Mexico'),
    '3F': ('Ford', 'Mexico'),
    '3G': ('General Motors', 'Mexico'),
    '3H': ('Honda', 'Mexico'),
    '3N': ('Nissan', 'Mexico'),
    '3P': ('Porsche', 'Mexico'),
    '3T': ('Toyota', 'Mexico'),
    '3V': ('Volkswagen', 'Mexico'),
    '3W': ('Volkswagen', 'Mexico'),
    '3X': ('Volkswagen', 'Mexico'),
    
    # Germany
    'WA': ('Audi', 'Germany'),
    'WB': ('BMW', 'Germany'),
    'WD': ('Daimler', 'Germany'),
    'WF': ('Ford', 'Germany'),
    'WG': ('Opel', 'Germany'),
    'WH': ('Audi', 'Germany'),
    'WK': ('Porsche', 'Germany'),
    'WL': ('Opel', 'Germany'),
    'WM': ('Mercedes-Benz', 'Germany'),
    'WN': ('Volkswagen', 'Germany'),
    'WP': ('Porsche', 'Germany'),
    'WR': ('Audi', 'Germany'),
    'WS': ('Audi', 'Germany'),
    'WT': ('Audi', 'Germany'),
    'WU': ('Audi', 'Germany'),
    'WV': ('Volkswagen', 'Germany'),
    'WW': ('Volkswagen', 'Germany'),
    'WX': ('Porsche', 'Germany'),
    'WY': ('Porsche', 'Germany'),
    'W0': ('Mercedes-Benz', 'Germany'),
    
    # Japan
    'JA': ('Isuzu', 'Japan'),
    'JB': ('Isuzu', 'Japan'),
    'JC': ('Isuzu', 'Japan'),
    'JD': ('Isuzu', 'Japan'),
    'JE': ('Isuzu', 'Japan'),
    'JF': ('Fuji Heavy Industries', 'Japan'),  # Subaru
    'JG': ('Fuji Heavy Industries', 'Japan'),  # Subaru
    'JH': ('Honda', 'Japan'),
    'JJ': ('Isuzu', 'Japan'),
    'JK': ('Kawasaki', 'Japan'),
    'JL': ('Mitsubishi', 'Japan'),
    'JM': ('Mazda', 'Japan'),
    'JN': ('Nissan', 'Japan'),
    'JP': ('Suzuki', 'Japan'),
    'JR': ('Kawasaki', 'Japan'),
    'JS': ('Suzuki', 'Japan'),
    'JT': ('Toyota', 'Japan'),
    'JU': ('Yamaha', 'Japan'),
    'JV': ('Suzuki', 'Japan'),
    'JW': ('Yamaha', 'Japan'),
    'JX': ('Yamaha', 'Japan'),
    'JY': ('Yamaha', 'Japan'),
    'JZ': ('Mazda', 'Japan'),
    'J0': ('Daihatsu', 'Japan'),
    'J1': ('Honda', 'Japan'),
    'J2': ('Kawasaki', 'Japan'),
    'J3': ('Kawasaki', 'Japan'),
    'J4': ('Kawasaki', 'Japan'),
    'J5': ('Kawasaki', 'Japan'),
    'J6': ('Kawasaki', 'Japan'),
    'J7': ('Mitsubishi', 'Japan'),
    'J8': ('Mitsubishi', 'Japan'),
    
    # South Korea
    'KL': ('Daewoo', 'South Korea'),
    'KM': ('Hyundai', 'South Korea'),
    'KN': ('Kia', 'South Korea'),
    'KP': ('SsangYong', 'South Korea'),
    'KR': ('Renault Samsung', 'South Korea'),
    'KT': ('Renault Samsung', 'South Korea'),
    
    # China (L prefix)
    'LA': ('Honda', 'China'),
    'LB': ('GM', 'China'),
    'LC': ('Toyota', 'China'),
    'LD': ('Volkswagen', 'China'),
    'LE': ('Volkswagen', 'China'),
    'LF': ('Ford', 'China'),
    'LG': ('GM', 'China'),
    'LH': ('Honda', 'China'),
    'LJ': ('Jeep', 'China'),
    'LK': ('BMW', 'China'),
    'LL': ('Mercedes-Benz', 'China'),
    'LM': ('Nissan', 'China'),
    'LN': ('Hyundai', 'China'),
    'LP': ('Peugeot', 'China'),
    'LR': ('Toyota', 'China'),
    'LS': ('Volvo', 'China'),
    'LT': ('Tesla', 'China'),
    
    # UK
    'SA': ('Aston Martin', 'UK'),
    'SB': ('Bentley', 'UK'),
    'SC': ('Lotus', 'UK'),
    'SD': ('Jaguar', 'UK'),
    'SE': ('McLaren', 'UK'),
    'SF': ('Mini', 'UK'),
    'SG': ('Rolls-Royce', 'UK'),
    'SH': ('Honda', 'UK'),
    'SJ': ('MG', 'UK'),
    'SK': ('Nissan', 'UK'),
    'SL': ('Jaguar', 'UK'),
    'SM': ('MINI', 'UK'),
    'SN': ('Toyota', 'UK'),
    
    # France
    'VA': ('Renault', 'France'),
    'VB': ('Renault', 'France'),
    'VF': ('Renault', 'France'),
    'VG': ('Citroën', 'France'),
    'VH': ('Peugeot', 'France'),
    'VJ': ('Renault', 'France'),
    'VK': ('Peugeot', 'France'),
    'VL': ('Renault', 'France'),
    'VM': ('Citroën', 'France'),
    'VN': ('Renault', 'France'),
    'VP': ('Peugeot', 'France'),
    'VR': ('Renault', 'France'),
    'VS': ('Citroën', 'France'),
    'VT': ('Bugatti', 'France'),
    'VU': ('Renault', 'France'),
    'VV': ('Volvo', 'France'),
    'VX': ('Peugeot', 'France'),
    'VY': ('Citroën', 'France'),
    
    # Italy
    'ZA': ('Fiat', 'Italy'),
    'ZB': ('Fiat', 'Italy'),
    'ZC': ('Lancia', 'Italy'),
    'ZD': ('Fiat', 'Italy'),
    'ZE': ('Ferrari', 'Italy'),
    'ZF': ('Ferrari', 'Italy'),
    'ZG': ('Ferrari', 'Italy'),
    'ZH': ('Fiat', 'Italy'),
    'ZJ': ('Fiat', 'Italy'),
    'ZK': ('Lamborghini', 'Italy'),
    'ZL': ('Lancia', 'Italy'),
    'ZM': ('Maserati', 'Italy'),
    'ZN': ('Fiat', 'Italy'),
    'ZP': ('Piaggio', 'Italy'),
    'ZR': ('Alfa Romeo', 'Italy'),
    'ZS': ('Ferrari', 'Italy'),
    'ZT': ('Fiat', 'Italy'),
    'ZU': ('Fiat', 'Italy'),
    'ZV': ('Fiat', 'Italy'),
    'ZW': ('Fiat', 'Italy'),
    'ZX': ('Lancia', 'Italy'),
    'ZY': ('Alfa Romeo', 'Italy'),
    'ZZ': ('Fiat', 'Italy'),
    
    # Sweden
    'YS': ('Scania', 'Sweden'),
    'YV': ('Volvo', 'Sweden'),
    'YK': ('Saab', 'Sweden'),
    'YL': ('Volvo', 'Sweden'),
    'YM': ('Volvo', 'Sweden'),
    'YN': ('Saab', 'Sweden'),
    'YP': ('Saab', 'Sweden'),
    'YR': ('Volvo', 'Sweden'),
    'YT': ('Volvo', 'Sweden'),
    'YU': ('Volvo', 'Sweden'),
    'YW': ('Volvo', 'Sweden'),
    'YX': ('Volvo', 'Sweden'),
    'Y1': ('Volvo', 'Sweden'),
    'Y2': ('Volvo', 'Sweden'),
    'Y3': ('Volvo', 'Sweden'),
    'Y4': ('Volvo', 'Sweden'),
    
    # Australia
    '6A': ('Audi', 'Australia'),
    '6F': ('Ford', 'Australia'),
    '6G': ('GM', 'Australia'),
    '6H': ('Honda', 'Australia'),
    '6M': ('Mitsubishi', 'Australia'),
    '6N': ('Nissan', 'Australia'),
    '6T': ('Toyota', 'Australia'),
    
    # Brazil
    '9A': ('Audi', 'Brazil'),
    '9B': ('BMW', 'Brazil'),
    '9C': ('Chrysler', 'Brazil'),
    '9F': ('Ford', 'Brazil'),
    '9G': ('GM', 'Brazil'),
    '9H': ('Honda', 'Brazil'),
    '9K': ('Kia', 'Brazil'),
    '9M': ('Mercedes-Benz', 'Brazil'),
    '9N': ('Nissan', 'Brazil'),
    '9T': ('Toyota', 'Brazil'),
    '9V': ('Volkswagen', 'Brazil'),
    '9W': ('Volkswagen', 'Brazil'),
    '9X': ('Hyundai', 'Brazil'),
    
    # India
    'MA': ('Maruti Suzuki', 'India'),
    'MB': ('Tata Motors', 'India'),
    'MC': ('Mahindra', 'India'),
    'MD': ('Mahindra', 'India'),
    'ME': ('Ford', 'India'),
    'MF': ('Honda', 'India'),
    'MH': ('Hyundai', 'India'),
    'MK': ('Kia', 'India'),
    'ML': ('MG', 'India'),
    'MM': ('Mercedes-Benz', 'India'),
    'MN': ('Nissan', 'India'),
    'MP': ('Volkswagen', 'India'),
    'MR': ('Renault', 'India'),
    'MT': ('Toyota', 'India'),
    'MY': ('Kia', 'India'),
}


# =============================================================================
# Data Classes
# =============================================================================

class VINInfo(NamedTuple):
    """VIN decoding result."""
    vin: str
    valid: bool
    check_digit: str
    check_digit_valid: bool
    wmi: str
    vds: str
    vis: str
    manufacturer: Optional[str]
    country: Optional[str]
    region: str
    model_year: Optional[int]
    model_years: List[int]
    plant_code: str
    sequential_number: str


class VINValidationResult(NamedTuple):
    """VIN validation result."""
    valid: bool
    errors: List[str]
    warnings: List[str]


# =============================================================================
# Validation Functions
# =============================================================================

def validate_vin_format(vin: str) -> VINValidationResult:
    """
    Validate VIN format (length, allowed characters).
    
    Args:
        vin: VIN string to validate
    
    Returns:
        VINValidationResult with valid status, errors, and warnings
    
    Example:
        >>> result = validate_vin_format("1HGBH41JXMN109186")
        >>> result.valid
        True
    """
    errors = []
    warnings = []
    
    if not vin:
        errors.append("VIN is empty")
        return VINValidationResult(False, errors, warnings)
    
    # Check length
    if len(vin) != 17:
        errors.append(f"VIN must be exactly 17 characters, got {len(vin)}")
        return VINValidationResult(False, errors, warnings)
    
    vin = vin.upper()
    
    # Check for invalid characters (I, O, Q are not allowed)
    invalid_chars = set()
    for char in vin:
        if char not in TRANSLITERATION:
            invalid_chars.add(char)
    
    if invalid_chars:
        errors.append(f"VIN contains invalid characters: {', '.join(sorted(invalid_chars))}")
    
    return VINValidationResult(len(errors) == 0, errors, warnings)


def calculate_check_digit(vin: str) -> str:
    """
    Calculate the check digit (position 9) for a VIN.
    
    Args:
        vin: VIN string (17 characters)
    
    Returns:
        Check digit character ('0'-'9' or 'X')
    
    Example:
        >>> calculate_check_digit("1HGBH41JXMN109186")
        'X'
    """
    if len(vin) != 17:
        # Need all 17 characters for calculation
        raise ValueError(f"VIN must be 17 characters for check digit calculation, got {len(vin)}")
    
    vin = vin.upper()
    
    # Calculate weighted sum using all positions except position 9 (index 8)
    total = 0
    for i in range(17):
        if i == 8:  # Skip check digit position
            continue
        transliterated = TRANSLITERATION.get(vin[i], 0)
        total += transliterated * POSITION_WEIGHTS[i]
    
    # Check digit is the sum mod 11
    remainder = total % 11
    
    return 'X' if remainder == 10 else str(remainder)


def validate_check_digit(vin: str) -> bool:
    """
    Validate the check digit in a VIN.
    
    Args:
        vin: Complete 17-character VIN
    
    Returns:
        True if check digit is valid
    
    Example:
        >>> validate_check_digit("1HGBH41JXMN109186")
        True  # With correct check digit
    """
    if len(vin) != 17:
        return False
    
    try:
        calculated = calculate_check_digit(vin)
        actual = vin[8].upper()
        return calculated == actual
    except:
        return False


def validate_vin(vin: str) -> VINValidationResult:
    """
    Full VIN validation including format and check digit.
    
    Args:
        vin: VIN string to validate
    
    Returns:
        VINValidationResult with valid status, errors, and warnings
    
    Example:
        >>> result = validate_vin("1HGBH41JXMN109186")
        >>> print(result.valid, result.errors)
    """
    result = validate_vin_format(vin)
    errors = list(result.errors)
    warnings = list(result.warnings)
    
    if not result.valid:
        return VINValidationResult(False, errors, warnings)
    
    # Check digit validation
    if not validate_check_digit(vin):
        try:
            calculated = calculate_check_digit(vin)
            errors.append(f"Invalid check digit: expected '{calculated}', got '{vin[8]}'")
        except:
            errors.append("Cannot validate check digit")
    
    return VINValidationResult(len(errors) == 0, errors, warnings)


# =============================================================================
# Decoding Functions
# =============================================================================

def get_region(vin: str) -> str:
    """
    Get the region from a VIN.
    
    Args:
        vin: VIN string
    
    Returns:
        Region name
    
    Example:
        >>> get_region("1HGBH41JXMN109186")
        'North America'
    """
    if not vin:
        return "Unknown"
    
    first_char = vin[0].upper()
    return REGION_CODES.get(first_char, "Unknown")


def get_country(vin: str) -> Optional[str]:
    """
    Get the country from a VIN using WMI database.
    
    Args:
        vin: VIN string
    
    Returns:
        Country name or None
    
    Example:
        >>> get_country("1HGBH41JXMN109186")
        'USA'
    """
    if len(vin) < 2:
        return None
    
    wmi2 = vin[:2].upper()
    
    # Check WMI database
    if wmi2 in WMI_DATABASE:
        return WMI_DATABASE[wmi2][1]
    
    return None


def get_manufacturer(vin: str) -> Optional[str]:
    """
    Get the manufacturer from a VIN using WMI database.
    
    Args:
        vin: VIN string
    
    Returns:
        Manufacturer name or None
    
    Example:
        >>> get_manufacturer("1HGBH41JXMN109186")
        'Honda'
    """
    if len(vin) < 2:
        return None
    
    wmi2 = vin[:2].upper()
    
    # Check WMI database
    if wmi2 in WMI_DATABASE:
        return WMI_DATABASE[wmi2][0]
    
    return None


def get_model_year(vin: str) -> Optional[int]:
    """
    Get the model year from a VIN.
    
    Note: VIN year codes repeat every 30 years. This function returns
    the most likely year based on current date.
    
    Args:
        vin: VIN string
    
    Returns:
        Model year or None
    
    Example:
        >>> get_model_year("1HGBH41JXMN109186")  # 'X' = 1999 or 2029
        1999  # or 2029 depending on current date
    """
    if len(vin) < 10:
        return None
    
    year_code = vin[9].upper()
    
    if year_code not in YEAR_CODE_BASE:
        return None
    
    base_year = YEAR_CODE_BASE[year_code]
    current_year = datetime.datetime.now().year
    
    # Determine which cycle is most likely
    # If base_year is 1980-2009, check if next cycle is more likely
    if base_year < 2010:
        if base_year + 30 <= current_year + 10:
            return base_year + 30
        else:
            return base_year
    else:
        return base_year


def get_possible_years(vin: str) -> List[int]:
    """
    Get all possible model years from a VIN (handles 30-year cycle).
    
    Args:
        vin: VIN string
    
    Returns:
        List of possible years
    
    Example:
        >>> get_possible_years("1HGBH41JXMN109186")  # 'X' year code
        [1999, 2029]
    """
    if len(vin) < 10:
        return []
    
    year_code = vin[9].upper()
    
    if year_code not in YEAR_CODE_BASE:
        return []
    
    base_year = YEAR_CODE_BASE[year_code]
    
    # Return both possible years in the 30-year cycle
    return [base_year, base_year + 30]


def decode_wmi(wmi: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Decode a WMI (World Manufacturer Identifier) code.
    
    Args:
        wmi: 2-3 character WMI code
    
    Returns:
        Tuple of (manufacturer, country) or (None, None) if unknown
    
    Example:
        >>> decode_wmi("1HG")
        ('Honda', 'USA')
    """
    wmi = wmi.upper()
    
    # Try 2-character code
    if len(wmi) >= 2 and wmi[:2] in WMI_DATABASE:
        return WMI_DATABASE[wmi[:2]]
    
    return (None, None)


def decode_vin(vin: str) -> VINInfo:
    """
    Fully decode a VIN and return all available information.
    
    VIN Structure:
    - Positions 1-3: WMI (3 chars)
    - Positions 4-8: VDS (5 chars)
    - Position 9: Check digit (1 char)
    - Position 10: Year code (1 char)
    - Position 11: Plant code (1 char)
    - Positions 12-17: Sequential number (6 chars)
    
    Args:
        vin: VIN string
    
    Returns:
        VINInfo named tuple with all decoded information
    
    Example:
        >>> info = decode_vin("1HGBH41JXMN109186")
        >>> print(info.manufacturer, info.country, info.region)
    """
    vin = vin.upper()
    
    # Handle partial VIN
    if len(vin) < 17:
        return VINInfo(
            vin=vin,
            valid=False,
            check_digit='',
            check_digit_valid=False,
            wmi=vin[:3] if len(vin) >= 3 else '',
            vds=vin[3:8] if len(vin) > 3 else '',
            vis='',
            manufacturer=get_manufacturer(vin),
            country=get_country(vin),
            region=get_region(vin),
            model_year=None,
            model_years=[],
            plant_code='',
            sequential_number=''
        )
    
    # Validate
    validation = validate_vin(vin)
    check_valid = validate_check_digit(vin)
    
    # Extract components (correct VIN structure)
    wmi = vin[:3]          # Positions 1-3
    vds = vin[3:8]         # Positions 4-8 (5 chars)
    vis = vin[9:17]        # Positions 10-17 (VIS includes year, plant, sequential)
    plant_code = vin[10]   # Position 11
    sequential_number = vin[11:17]  # Positions 12-17
    
    # Decode components
    manufacturer = get_manufacturer(vin)
    country = get_country(vin)
    region = get_region(vin)
    model_year = get_model_year(vin)
    possible_years = get_possible_years(vin)
    
    return VINInfo(
        vin=vin,
        valid=validation.valid,
        check_digit=vin[8],
        check_digit_valid=check_valid,
        wmi=wmi,
        vds=vds,
        vis=vis,
        manufacturer=manufacturer,
        country=country,
        region=region,
        model_year=model_year,
        model_years=possible_years,
        plant_code=plant_code,
        sequential_number=sequential_number
    )


# =============================================================================
# Generation Functions
# =============================================================================

def generate_vin(
    wmi: str = "1HG",
    vds: str = None,
    model_year: int = None,
    plant_code: str = "M",
    sequential: str = None
) -> str:
    """
    Generate a valid VIN for testing purposes.
    
    VIN Structure:
    - Positions 1-3: WMI (3 chars)
    - Positions 4-8: VDS (5 chars)
    - Position 9: Check digit (1 char)
    - Position 10: Year code (1 char)
    - Position 11: Plant code (1 char)
    - Positions 12-17: Sequential number (6 chars)
    
    Args:
        wmi: World Manufacturer Identifier (2-3 chars)
        vds: Vehicle Descriptor Section (5 chars, optional, random if None)
        model_year: Model year (optional, current year if None)
        plant_code: Plant code (1 char)
        sequential: Sequential number (6 chars, optional, random if None)
    
    Returns:
        Valid 17-character VIN
    
    Example:
        >>> vin = generate_vin("1HG", model_year=2020)
        >>> len(vin)
        17
    """
    import random
    
    chars = "ABCDEFGHJKLMNPRSTUVWXYZ0123456789"  # Valid VIN chars (no I, O, Q)
    
    # Validate/pad WMI (2-3 chars)
    wmi = wmi.upper()[:3]
    if len(wmi) < 3:
        wmi = wmi + ''.join(random.choice(chars) for _ in range(3 - len(wmi)))
    
    # Generate random VDS if not provided (5 chars for positions 4-8)
    if vds is None:
        vds = ''.join(random.choice(chars) for _ in range(5))
    else:
        vds = vds.upper()[:5]
        if len(vds) < 5:
            vds = vds + ''.join(random.choice(chars) for _ in range(5 - len(vds)))
    
    # Determine model year and code
    if model_year is None:
        model_year = datetime.datetime.now().year
    
    # Get year code
    year_code = YEAR_TO_CODE.get(model_year)
    if year_code is None:
        # Use closest valid year
        valid_years = sorted(YEAR_TO_CODE.keys())
        closest = min(valid_years, key=lambda y: abs(y - model_year))
        year_code = YEAR_TO_CODE[closest]
    
    # Plant code
    plant_code = (plant_code or 'A').upper()[:1]
    if plant_code in 'IOQ':
        plant_code = 'A'  # Invalid chars
    
    # Generate sequential number
    if sequential is None:
        sequential = ''.join(random.choice(chars) for _ in range(6))
    else:
        sequential = str(sequential).upper()[:6]
        if len(sequential) < 6:
            sequential = sequential + ''.join(random.choice(chars) for _ in range(6 - len(sequential)))
    
    # Build VIN with placeholder for check digit
    # Structure: WMI(3) + VDS(5) + CheckDigitPlaceholder(1) + YearCode(1) + Plant(1) + Sequential(6) = 17
    vin_partial = wmi + vds + 'X' + year_code + plant_code + sequential
    
    # Calculate check digit
    check_digit = calculate_check_digit(vin_partial)
    
    # Replace placeholder at position 9 (index 8)
    vin = vin_partial[:8] + check_digit + vin_partial[9:]
    
    return vin


def format_vin(vin: str, separator: str = ' ') -> str:
    """
    Format a VIN with separators for readability.
    
    Args:
        vin: VIN string
        separator: Separator character (default: space)
    
    Returns:
        Formatted VIN (e.g., "1HG BH41 JX MN109186")
    
    Example:
        >>> format_vin("1HGBH41JXMN109186", "-")
        '1HG-BH41JX-MN109186'
    """
    if len(vin) != 17:
        return vin
    
    # Split: WMI (3) + VDS (6) + VIS (8) = 17
    return separator.join([vin[:3], vin[3:9], vin[9:17]])


# =============================================================================
# Utility Functions
# =============================================================================

def extract_vin_from_text(text: str) -> List[str]:
    """
    Extract potential VINs from text.
    
    Args:
        text: Text to search for VINs
    
    Returns:
        List of potential VIN strings found
    
    Example:
        >>> extract_vin_from_text("My car VIN is 1HGBH41JXMN109186")
        ['1HGBH41JXMN109186']
    """
    # Find all 17-character alphanumeric sequences (no I, O, Q)
    potential_vins = re.findall(r'[A-HJ-NPR-Z0-9]{17}', text.upper())
    
    # Filter to format-valid VINs
    valid_vins = []
    for vin in potential_vins:
        result = validate_vin_format(vin)
        if result.valid:
            valid_vins.append(vin)
    
    return valid_vins


def compare_vins(vin1: str, vin2: str) -> Dict[str, bool]:
    """
    Compare two VINs and identify similarities.
    
    Args:
        vin1: First VIN
        vin2: Second VIN
    
    Returns:
        Dictionary of comparison results
    
    Example:
        >>> compare_vins("1HGBH41JXMN109186", "1HGBH41JXMN109187")
        {'same_wmi': True, 'same_vds': True, ...}
    """
    vin1 = vin1.upper()
    vin2 = vin2.upper()
    
    info1 = decode_vin(vin1)
    info2 = decode_vin(vin2)
    
    return {
        'same_wmi': vin1[:3] == vin2[:3] if len(vin1) >= 3 and len(vin2) >= 3 else False,
        'same_vds': vin1[3:9] == vin2[3:9] if len(vin1) >= 9 and len(vin2) >= 9 else False,
        'same_vis': vin1[9:17] == vin2[9:17] if len(vin1) >= 17 and len(vin2) >= 17 else False,
        'same_manufacturer': info1.manufacturer == info2.manufacturer,
        'same_country': info1.country == info2.country,
        'same_region': info1.region == info2.region,
        'same_year': vin1[9] == vin2[9] if len(vin1) >= 10 and len(vin2) >= 10 else False,
        'same_plant': vin1[10] == vin2[10] if len(vin1) >= 11 and len(vin2) >= 11 else False,
        'consecutive': False,  # Would need numeric comparison
    }


def get_year_code(year: int) -> str:
    """
    Get the VIN year code for a given year.
    
    Args:
        year: Model year (1980-2039)
    
    Returns:
        Year code character
    
    Example:
        >>> get_year_code(2020)
        'L'
    """
    code = YEAR_TO_CODE.get(year)
    if code is None:
        raise ValueError(f"Year {year} out of valid range (1980-2039)")
    return code


# =============================================================================
# Main Demo
# =============================================================================

if __name__ == "__main__":
    print("VIN Decoder Utilities Demo")
    print("=" * 60)
    
    # Example VINs
    example_vins = [
        generate_vin("1HG", model_year=2020),
        generate_vin("JH", model_year=2020),
        generate_vin("WB", model_year=2020),
        generate_vin("JT", model_year=2020),
        generate_vin("YV", model_year=2020),
    ]
    
    for vin in example_vins:
        print(f"\nVIN: {vin}")
        print(f"Formatted: {format_vin(vin, '-')}")
        
        validation = validate_vin(vin)
        print(f"Valid: {validation.valid}")
        
        info = decode_vin(vin)
        print(f"WMI: {info.wmi}")
        print(f"Manufacturer: {info.manufacturer}")
        print(f"Country: {info.country}")
        print(f"Region: {info.region}")
        print(f"Model Year: {info.model_year} (possible: {info.model_years})")
        print(f"Check Digit: {info.check_digit} (valid: {info.check_digit_valid})")
    
    print("\n" + "=" * 60)
    print("\nExtracting VINs from text:")
    text = f"Found VINs: {example_vins[0]}, {example_vins[1]}"
    found = extract_vin_from_text(text)
    print(f"  Found: {found}")