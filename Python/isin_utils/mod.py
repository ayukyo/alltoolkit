"""
ISIN Utilities - International Securities Identification Number Utilities

A comprehensive toolkit for working with ISIN (International Securities 
Identification Numbers). ISIN is a 12-character alphanumeric code that 
uniquely identifies securities worldwide.

Features:
- Validate ISIN codes (Luhn mod 10 algorithm)
- Parse ISIN components (country code, NSIN, check digit)
- Generate random ISINs for testing
- Extract ISINs from text
- Zero external dependencies

Reference: ISO 6166
"""

import re
from typing import Optional, Tuple, List, Dict
from dataclasses import dataclass
from enum import Enum


class ISINValidationError(Exception):
    """Exception raised for ISIN validation errors."""
    pass


@dataclass
class ISINInfo:
    """Parsed ISIN information."""
    original: str
    cleaned: str
    is_valid: bool
    country_code: str
    nsin: str
    check_digit: str
    message: str
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "original": self.original,
            "cleaned": self.cleaned,
            "is_valid": self.is_valid,
            "country_code": self.country_code,
            "nsin": self.nsin,
            "check_digit": self.check_digit,
            "message": self.message
        }


# Country code to country name mapping (partial, common ones)
COUNTRY_CODES = {
    "US": "United States",
    "GB": "United Kingdom",
    "DE": "Germany",
    "FR": "France",
    "JP": "Japan",
    "CN": "China",
    "HK": "Hong Kong",
    "SG": "Singapore",
    "AU": "Australia",
    "CA": "Canada",
    "CH": "Switzerland",
    "NL": "Netherlands",
    "SE": "Sweden",
    "IT": "Italy",
    "ES": "Spain",
    "IN": "India",
    "KR": "South Korea",
    "TW": "Taiwan",
    "BR": "Brazil",
    "MX": "Mexico",
    "RU": "Russia",
    "ZA": "South Africa",
    "AE": "United Arab Emirates",
    "SA": "Saudi Arabia",
    "IL": "Israel",
    "IE": "Ireland",
    "BE": "Belgium",
    "AT": "Austria",
    "PT": "Portugal",
    "NO": "Norway",
    "DK": "Denmark",
    "FI": "Finland",
    "PL": "Poland",
    "TR": "Turkey",
    "ID": "Indonesia",
    "MY": "Malaysia",
    "TH": "Thailand",
    "PH": "Philippines",
    "VN": "Vietnam",
    "NZ": "New Zealand",
    "LU": "Luxembourg",
    "CZ": "Czech Republic",
    "GR": "Greece",
    "HU": "Hungary",
    "AR": "Argentina",
    "CL": "Chile",
    "CO": "Colombia",
    "PE": "Peru",
    "EG": "Egypt",
    "NG": "Nigeria",
    "KE": "Kenya",
    "MA": "Morocco",
    "PK": "Pakistan",
    "BD": "Bangladesh",
}


def _clean_isin(isin: str) -> str:
    """Clean ISIN string by removing whitespace and converting to uppercase."""
    if not isin:
        return ""
    return re.sub(r'[\s\-\.]', '', str(isin)).upper()


def _char_to_value(char: str) -> int:
    """Convert a character to its numeric value for Luhn check.
    
    Digits 0-9 remain as their values.
    Letters A-Z are 10-35.
    """
    if char.isdigit():
        return int(char)
    elif char.isalpha():
        return ord(char) - ord('A') + 10
    return 0


def _luhn_mod10_check(digits: str) -> int:
    """Calculate Luhn mod 10 check digit for ISIN.
    
    Used for ISIN validation. The algorithm:
    1. Convert all letters to numbers (A=10, B=11, ..., Z=35)
    2. Expand each number to separate digits (e.g., 28 -> 2, 8)
    3. Based on the length of expanded digits:
       - If length is odd: double all digits at even positions from the left (0, 2, 4...)
       - If length is even: double all digits at odd positions from the left (1, 3, 5...)
    4. If doubling results in >9, subtract 9
    5. Sum all digits
    6. Check digit = (10 - (sum mod 10)) mod 10
    
    Args:
        digits: 11-character ISIN without check digit
    """
    # Convert all characters to their numeric values
    # and expand into a sequence of single digits
    expanded_digits = []
    for c in digits:
        val = _char_to_value(c)
        if val >= 10:
            # Expand multi-digit numbers (e.g., 28 -> 2, 8)
            expanded_digits.append(val // 10)
            expanded_digits.append(val % 10)
        else:
            expanded_digits.append(val)
    
    # Determine doubling positions based on length
    # If length is odd: double even positions from left (0, 2, 4...)
    # If length is even: double odd positions from left (1, 3, 5...)
    n = len(expanded_digits)
    double_even_positions = (n % 2 == 1)  # odd length -> double even positions
    
    total = 0
    for i, digit in enumerate(expanded_digits):
        # Determine if this position should be doubled
        should_double = (i % 2 == 0) if double_even_positions else (i % 2 == 1)
        
        if should_double:
            digit *= 2
            if digit > 9:
                digit -= 9
        
        total += digit
    
    return (10 - (total % 10)) % 10


def calculate_check_digit(isin: str) -> str:
    """Calculate the check digit for an ISIN (without the check digit).
    
    Args:
        isin: An 11-character ISIN without check digit, or 12-character
              ISIN (check digit will be ignored).
    
    Returns:
        The calculated check digit as a string.
    
    Raises:
        ISINValidationError: If the input is invalid.
    """
    cleaned = _clean_isin(isin)
    
    if len(cleaned) < 11:
        raise ISINValidationError(f"ISIN must have at least 11 characters, got {len(cleaned)}")
    
    # Take first 11 characters
    base = cleaned[:11]
    
    # Validate format
    if not base[:2].isalpha():
        raise ISINValidationError("First two characters must be letters (country code)")
    
    for char in base:
        if not char.isalnum():
            raise ISINValidationError(f"Invalid character: {char}")
    
    return str(_luhn_mod10_check(base))


def is_valid_isin(isin: str) -> bool:
    """Check if an ISIN is valid.
    
    Args:
        isin: The ISIN string to validate.
    
    Returns:
        True if valid, False otherwise.
    """
    try:
        info = validate_isin(isin)
        return info.is_valid
    except:
        return False


def validate_isin(isin: str) -> ISINInfo:
    """Validate an ISIN and return detailed information.
    
    Args:
        isin: The ISIN string to validate.
    
    Returns:
        ISINInfo object with validation results.
    """
    original = isin
    cleaned = _clean_isin(isin)
    
    # Check length
    if len(cleaned) != 12:
        return ISINInfo(
            original=original,
            cleaned=cleaned,
            is_valid=False,
            country_code="",
            nsin="",
            check_digit="",
            message=f"ISIN must be 12 characters, got {len(cleaned)}"
        )
    
    # Check country code (first 2 characters must be letters)
    country_code = cleaned[:2]
    if not country_code.isalpha():
        return ISINInfo(
            original=original,
            cleaned=cleaned,
            is_valid=False,
            country_code="",
            nsin="",
            check_digit="",
            message="First two characters must be letters (country code)"
        )
    
    # Check that all characters are alphanumeric
    if not cleaned.isalnum():
        return ISINInfo(
            original=original,
            cleaned=cleaned,
            is_valid=False,
            country_code=country_code,
            nsin="",
            check_digit="",
            message="ISIN must contain only alphanumeric characters"
        )
    
    # Parse components
    nsin = cleaned[2:11]
    check_digit = cleaned[11]
    
    # Validate check digit
    expected_check = calculate_check_digit(cleaned[:11])
    if check_digit != expected_check:
        return ISINInfo(
            original=original,
            cleaned=cleaned,
            is_valid=False,
            country_code=country_code,
            nsin=nsin,
            check_digit=check_digit,
            message=f"Invalid check digit: expected {expected_check}, got {check_digit}"
        )
    
    return ISINInfo(
        original=original,
        cleaned=cleaned,
        is_valid=True,
        country_code=country_code,
        nsin=nsin,
        check_digit=check_digit,
        message="Valid ISIN"
    )


def parse_isin(isin: str) -> ISINInfo:
    """Parse an ISIN and return its components.
    
    Args:
        isin: The ISIN string to parse.
    
    Returns:
        ISINInfo object with parsed components.
    """
    return validate_isin(isin)


def get_isin_info(isin: str) -> Dict:
    """Get detailed information about an ISIN.
    
    Args:
        isin: The ISIN string.
    
    Returns:
        Dictionary with ISIN information including country name.
    """
    info = validate_isin(isin)
    result = info.to_dict()
    
    # Add country name if available
    result["country_name"] = COUNTRY_CODES.get(info.country_code, "Unknown")
    
    return result


def format_isin(isin: str, separator: str = " ") -> str:
    """Format an ISIN with separator.
    
    Args:
        isin: The ISIN string.
        separator: Separator character (default: space).
    
    Returns:
        Formatted ISIN string.
    
    Example:
        >>> format_isin("US0378331005")
        "US 037833100 5"
    """
    cleaned = _clean_isin(isin)
    
    if len(cleaned) != 12:
        return cleaned
    
    return f"{cleaned[:2]}{separator}{cleaned[2:11]}{separator}{cleaned[11]}"


def generate_isin(country_code: str = "US", nsin: Optional[str] = None, 
                  seed: Optional[int] = None) -> str:
    """Generate a valid ISIN.
    
    Args:
        country_code: 2-letter country code (default: "US").
        nsin: 9-character NSIN. If None, generates random NSIN.
        seed: Random seed for reproducible generation.
    
    Returns:
        A valid ISIN string.
    
    Example:
        >>> generate_isin("US")
        "US0378331005"
        
        >>> generate_isin("US", "037833100")
        "US0378331005"
    """
    import random
    
    if seed is not None:
        random.seed(seed)
    
    # Validate country code
    country_code = country_code.upper()
    if len(country_code) != 2 or not country_code.isalpha():
        raise ISINValidationError("Country code must be 2 letters")
    
    # Generate or validate NSIN
    if nsin is None:
        # Generate random 9-character alphanumeric NSIN
        chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        nsin = "".join(random.choice(chars) for _ in range(9))
    else:
        nsin = _clean_isin(nsin)
        if len(nsin) != 9:
            raise ISINValidationError("NSIN must be 9 characters")
    
    # Build base ISIN
    base = country_code + nsin
    
    # Calculate check digit
    check_digit = calculate_check_digit(base)
    
    return base + check_digit


def generate_random_isin(seed: Optional[int] = None) -> str:
    """Generate a random valid ISIN.
    
    Args:
        seed: Random seed for reproducible generation.
    
    Returns:
        A random valid ISIN string.
    """
    import random
    
    if seed is not None:
        random.seed(seed)
    
    # Random country code from common ones
    countries = list(COUNTRY_CODES.keys())
    country_code = random.choice(countries)
    
    return generate_isin(country_code, seed=seed)


def extract_isin(text: str) -> Optional[str]:
    """Extract the first valid ISIN from text.
    
    Args:
        text: Text to search for ISIN.
    
    Returns:
        First valid ISIN found, or None.
    """
    isins = extract_all_isin(text)
    return isins[0] if isins else None


def extract_all_isin(text: str) -> List[str]:
    """Extract all valid ISINs from text.
    
    Args:
        text: Text to search for ISINs.
    
    Returns:
        List of valid ISINs found.
    """
    # Pattern to match potential ISINs (2 letters + 9 alphanumeric + 1 digit)
    pattern = r'\b([A-Z]{2}[A-Z0-9]{9}[0-9])\b'
    
    potential_isins = re.findall(pattern, text.upper())
    
    # Validate each potential ISIN
    valid_isins = []
    for isin in potential_isins:
        info = validate_isin(isin)
        if info.is_valid:
            valid_isins.append(info.cleaned)
    
    return valid_isins


def compare_isin(isin1: str, isin2: str) -> bool:
    """Compare two ISINs for equality (ignoring formatting).
    
    Args:
        isin1: First ISIN.
        isin2: Second ISIN.
    
    Returns:
        True if ISINs are equivalent.
    """
    cleaned1 = _clean_isin(isin1)
    cleaned2 = _clean_isin(isin2)
    return cleaned1 == cleaned2


def isin_to_cusip(isin: str) -> Optional[str]:
    """Extract CUSIP from US ISIN.
    
    CUSIP is a 9-character identifier used for US and Canadian securities.
    For US ISINs, the NSIN is the CUSIP.
    
    Args:
        isin: An ISIN string (US or CA only).
    
    Returns:
        CUSIP code if ISIN is US or CA, None otherwise.
    """
    info = validate_isin(isin)
    
    if not info.is_valid:
        return None
    
    if info.country_code in ("US", "CA"):
        return info.nsin
    
    return None


def cusip_to_isin(cusip: str, country_code: str = "US") -> str:
    """Convert CUSIP to ISIN.
    
    Args:
        cusip: 9-character CUSIP code.
        country_code: Country code (default: "US").
    
    Returns:
        Valid ISIN string.
    """
    cusip = _clean_isin(cusip)
    
    if len(cusip) != 9:
        raise ISINValidationError(f"CUSIP must be 9 characters, got {len(cusip)}")
    
    return generate_isin(country_code, cusip)


def sedol_to_isin(sedol: str, country_code: str = "GB") -> str:
    """Convert SEDOL to ISIN.
    
    SEDOL is a 7-character security identifier for UK securities.
    
    Args:
        sedol: 7-character SEDOL code.
        country_code: Country code (default: "GB").
    
    Returns:
        Valid ISIN string.
    
    Note:
        SEDOL needs to be padded to 9 characters for ISIN.
    """
    sedol = _clean_isin(sedol)
    
    if len(sedol) != 7:
        raise ISINValidationError(f"SEDOL must be 7 characters, got {len(sedol)}")
    
    # Pad SEDOL to 9 characters with leading zeros
    nsin = sedol.zfill(9)
    
    return generate_isin(country_code, nsin)


# Common ISINs for testing
EXAMPLE_ISINS = {
    "APPLE": "US0378331005",
    "MICROSOFT": "US5949181045",
    "GOOGLE": "US02079K1079",
    "AMAZON": "US0231351067",
    "TESLA": "US88160R1014",
    "NETFLIX": "US64110L1061",
    "FACEBOOK": "US30303M1027",
    "NVIDIA": "US67066G1040",
    "BERKSHIRE": "US0846707026",
    "JOHNSON_JOHNSON": "US4781601046",
    "VISA": "US92826C8394",
    "MCDONALDS": "US5801351017",
    "COCA_COLA": "US1912161007",
    "DISNEY": "US2546871060",
    "INTEL": "US4581401001",
    "SAMSUNG": "KR7005930003",
    "TOYOTA": "JP3633400001",
    "SONY": "JP3435000009",
    "TENCENT": "KYG875721634",
    "ALIBABA": "KYG0201G1013",
}


def get_example_isin(name: str) -> Optional[str]:
    """Get an example ISIN by company name.
    
    Args:
        name: Company name (e.g., "APPLE", "MICROSOFT").
    
    Returns:
        Example ISIN or None if not found.
    """
    return EXAMPLE_ISINS.get(name.upper())


def list_example_isins() -> Dict[str, str]:
    """Get all example ISINs.
    
    Returns:
        Dictionary of company names to ISINs.
    """
    return EXAMPLE_ISINS.copy()


# Convenience aliases
validate = validate_isin
is_valid = is_valid_isin
parse = parse_isin
generate = generate_isin