"""
IMEI Utilities - Validate, parse, and generate IMEI numbers

IMEI (International Mobile Equipment Identity) is a unique identifier
for mobile devices. This module provides utilities for:
- Validating IMEI numbers using Luhn algorithm
- Parsing IMEI structure (TAC, SNR, Check Digit)
- Calculating check digits
- Generating random IMEI for testing

IMEI Structure (15 digits):
- TAC (Type Allocation Code): First 8 digits
- SNR (Serial Number): Next 6 digits
- CD (Check Digit): Last 1 digit

Example: 49-015420-323751-8
    TAC: 49015420
    SNR: 323751
    CD: 8

Author: AllToolkit
Date: 2026-04-24
"""

import random
from typing import Optional, Dict, Tuple


def luhn_checksum(number: str) -> int:
    """
    Calculate Luhn checksum for a number string.
    
    The Luhn algorithm is used to validate various identification numbers
    including IMEI, credit cards, etc.
    
    Args:
        number: String of digits (without check digit)
    
    Returns:
        Checksum value (0-9)
    
    Example:
        >>> luhn_checksum("49015420323751")
        2
    """
    total = 0
    # Process from right to left
    for i, digit in enumerate(reversed(number)):
        d = int(digit)
        # Double every second digit (from right, so odd positions from left)
        if i % 2 == 0:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    return total % 10


def calculate_check_digit(imei14: str) -> int:
    """
    Calculate the check digit for a 14-digit IMEI body.
    
    Args:
        imei14: First 14 digits of IMEI (without check digit)
    
    Returns:
        Check digit (0-9)
    
    Raises:
        ValueError: If imei14 is not 14 digits
    
    Example:
        >>> calculate_check_digit("49015420323751")
        8
    """
    if not imei14.isdigit():
        raise ValueError("IMEI must contain only digits")
    if len(imei14) != 14:
        raise ValueError(f"IMEI body must be 14 digits, got {len(imei14)}")
    
    checksum = luhn_checksum(imei14)
    return (10 - checksum) % 10


def validate(imei: str) -> bool:
    """
    Validate an IMEI number.
    
    Validates using Luhn algorithm and checks format.
    Accepts IMEI with or without separators.
    
    Args:
        imei: IMEI number (15 digits, optionally with separators)
    
    Returns:
        True if valid, False otherwise
    
    Example:
        >>> validate("490154203237518")
        True
        >>> validate("49-015420-323751-8")
        True
        >>> validate("490154203237519")
        False
    """
    # Remove separators
    clean_imei = ''.join(c for c in imei if c.isdigit())
    
    if len(clean_imei) != 15:
        return False
    
    if not clean_imei.isdigit():
        return False
    
    # Verify check digit
    imei14 = clean_imei[:14]
    expected_cd = calculate_check_digit(imei14)
    actual_cd = int(clean_imei[14])
    
    return expected_cd == actual_cd


def parse(imei: str) -> Dict[str, str]:
    """
    Parse an IMEI number and return its components.
    
    Args:
        imei: IMEI number (15 digits, optionally with separators)
    
    Returns:
        Dictionary with keys:
        - tac: Type Allocation Code (8 digits)
        - snr: Serial Number (6 digits)
        - cd: Check Digit (1 digit)
        - valid: Whether the IMEI is valid
    
    Raises:
        ValueError: If IMEI format is invalid
    
    Example:
        >>> parse("490154203237518")
        {'tac': '49015420', 'snr': '323751', 'cd': '8', 'valid': True}
    """
    # Remove separators
    clean_imei = ''.join(c for c in imei if c.isdigit())
    
    if len(clean_imei) != 15:
        raise ValueError(f"IMEI must be 15 digits, got {len(clean_imei)}")
    
    if not clean_imei.isdigit():
        raise ValueError("IMEI must contain only digits")
    
    return {
        'tac': clean_imei[:8],
        'snr': clean_imei[8:14],
        'cd': clean_imei[14],
        'valid': validate(clean_imei)
    }


def format_imei(imei: str, style: str = 'standard') -> str:
    """
    Format an IMEI number in different styles.
    
    Args:
        imei: IMEI number (15 digits, optionally with separators)
        style: Format style ('standard', 'compact', 'dashed')
            - standard: AA-BBBBBB-CCCCCC-D (e.g., 35-209900-176148-8)
            - compact: AABBBBBBCCCCCCD (no separators)
            - dashed: AA-BBBBBB-CCCCCC-D
            - spaced: AA BBBBBB CCCCCC D
    
    Returns:
        Formatted IMEI string
    
    Raises:
        ValueError: If IMEI is invalid or style is unknown
    
    Example:
        >>> format_imei("490154203237518", "standard")
        '49-015420-323751-8'
        >>> format_imei("490154203237518", "spaced")
        '49 015420 323751 8'
    """
    # Remove separators
    clean_imei = ''.join(c for c in imei if c.isdigit())
    
    if len(clean_imei) != 15:
        raise ValueError(f"IMEI must be 15 digits, got {len(clean_imei)}")
    
    tac = clean_imei[:8]
    snr = clean_imei[8:14]
    cd = clean_imei[14]
    
    if style == 'compact':
        return clean_imei
    elif style in ('standard', 'dashed'):
        return f"{tac[:2]}-{tac[2:8]}-{snr}-{cd}"
    elif style == 'spaced':
        return f"{tac[:2]} {tac[2:8]} {snr} {cd}"
    else:
        raise ValueError(f"Unknown style: {style}")


def generate_random(tac: Optional[str] = None) -> str:
    """
    Generate a random valid IMEI number.
    
    Useful for testing purposes. Generated IMEI will pass Luhn validation.
    
    Args:
        tac: Optional 8-digit TAC (Type Allocation Code).
             If not provided, a random TAC will be generated.
    
    Returns:
        15-digit valid IMEI number
    
    Raises:
        ValueError: If TAC is provided but not 8 digits
    
    Example:
        >>> imei = generate_random()
        >>> validate(imei)
        True
        >>> imei = generate_random("35209900")
        >>> imei.startswith("35209900")
        True
    """
    if tac is None:
        # Generate random TAC (8 digits)
        tac = ''.join(str(random.randint(0, 9)) for _ in range(8))
    else:
        if not tac.isdigit() or len(tac) != 8:
            raise ValueError("TAC must be 8 digits")
    
    # Generate random SNR (6 digits)
    snr = ''.join(str(random.randint(0, 9)) for _ in range(6))
    
    # Calculate check digit
    imei14 = tac + snr
    cd = calculate_check_digit(imei14)
    
    return imei14 + str(cd)


def generate_batch(count: int, tac: Optional[str] = None) -> list:
    """
    Generate multiple random valid IMEI numbers.
    
    Args:
        count: Number of IMEI numbers to generate
        tac: Optional 8-digit TAC for all generated IMEIs
    
    Returns:
        List of valid IMEI numbers
    
    Example:
        >>> imeis = generate_batch(5)
        >>> len(imeis)
        5
        >>> all(validate(imei) for imei in imeis)
        True
    """
    return [generate_random(tac) for _ in range(count)]


def get_tac_info(tac: str) -> Dict[str, str]:
    """
    Get basic information about a TAC (Type Allocation Code).
    
    Note: This is a simplified lookup. Real TAC databases are much larger
    and require external data sources.
    
    Args:
        tac: 8-digit TAC code
    
    Returns:
        Dictionary with TAC information:
        - tac: The TAC code
        - reporting_body_identifier: First 2 digits
        - type: 'standard' or 'unknown'
    
    Example:
        >>> info = get_tac_info("49015420")
        >>> info['reporting_body_identifier']
        '49'
    """
    if not tac.isdigit() or len(tac) != 8:
        raise ValueError("TAC must be 8 digits")
    
    # Reporting Body Identifier (first 2 digits)
    # Common values:
    # 01, 10: DECT devices
    # 35: GSM devices
    # 44: UK devices
    # 45: Denmark
    # etc.
    rbi = tac[:2]
    
    # Simplified classification
    tac_type = 'unknown'
    if rbi == '35':
        tac_type = 'gsm_standard'
    elif rbi in ('01', '10'):
        tac_type = 'dect_device'
    elif rbi == '44':
        tac_type = 'uk_device'
    
    return {
        'tac': tac,
        'reporting_body_identifier': rbi,
        'type': tac_type
    }


def compare_imei(imei1: str, imei2: str) -> Dict[str, any]:
    """
    Compare two IMEI numbers and return comparison result.
    
    Args:
        imei1: First IMEI number
        imei2: Second IMEI number
    
    Returns:
        Dictionary with comparison results:
        - match: Whether IMEIs are identical
        - same_tac: Whether TAC codes match
        - same_snr: Whether serial numbers match
        - valid1: Whether imei1 is valid
        - valid2: Whether imei2 is valid
    
    Example:
        >>> compare_imei("490154203237518", "490154203237519")
        {'match': False, 'same_tac': True, 'same_snr': True, ...}
    """
    clean1 = ''.join(c for c in imei1 if c.isdigit())
    clean2 = ''.join(c for c in imei2 if c.isdigit())
    
    if len(clean1) != 15 or len(clean2) != 15:
        return {
            'match': False,
            'same_tac': False,
            'same_snr': False,
            'valid1': False,
            'valid2': False,
            'error': 'Invalid IMEI format'
        }
    
    tac1, tac2 = clean1[:8], clean2[:8]
    snr1, snr2 = clean1[8:14], clean2[8:14]
    
    return {
        'match': clean1 == clean2,
        'same_tac': tac1 == tac2,
        'same_snr': snr1 == snr2,
        'valid1': validate(clean1),
        'valid2': validate(clean2)
    }


def extract_digits(text: str) -> list:
    """
    Extract potential IMEI numbers from text.
    
    Finds sequences of 15 digits that could be IMEI numbers.
    
    Args:
        text: Text to search for IMEI numbers
    
    Returns:
        List of potential IMEI numbers found (validated)
    
    Example:
        >>> extract_digits("Device IMEI: 490154203237518 and 123456789012345")
        ['490154203237518']
    """
    import re
    
    # Find all sequences of 15 digits
    pattern = r'\d{15}'
    matches = re.findall(pattern, text)
    
    # Filter to only valid IMEIs
    valid_imeis = [m for m in matches if validate(m)]
    
    return valid_imeis


class IMEIValidator:
    """
    Class-based IMEI validator for repeated validations.
    
    Provides a fluent interface for IMEI validation and manipulation.
    
    Example:
        >>> validator = IMEIValidator("490154203237518")
        >>> validator.is_valid
        True
        >>> validator.tac
        '49015420'
    """
    
    def __init__(self, imei: str):
        """
        Initialize validator with an IMEI number.
        
        Args:
            imei: IMEI number to validate
        """
        self._raw = imei
        self._clean = ''.join(c for c in imei if c.isdigit())
        self._parsed = None
        
        if len(self._clean) == 15:
            try:
                self._parsed = parse(self._clean)
            except ValueError:
                pass
    
    @property
    def is_valid(self) -> bool:
        """Check if IMEI is valid."""
        return self._parsed is not None and self._parsed['valid']
    
    @property
    def tac(self) -> Optional[str]:
        """Get TAC (Type Allocation Code)."""
        return self._parsed['tac'] if self._parsed else None
    
    @property
    def snr(self) -> Optional[str]:
        """Get SNR (Serial Number)."""
        return self._parsed['snr'] if self._parsed else None
    
    @property
    def check_digit(self) -> Optional[str]:
        """Get check digit."""
        return self._parsed['cd'] if self._parsed else None
    
    def format(self, style: str = 'standard') -> str:
        """Format the IMEI in the specified style."""
        if not self._parsed:
            raise ValueError("Cannot format invalid IMEI")
        return format_imei(self._clean, style)
    
    def __repr__(self) -> str:
        status = "valid" if self.is_valid else "invalid"
        return f"IMEIValidator({self._clean}, {status})"
    
    def __str__(self) -> str:
        return self._clean if self._clean else self._raw


if __name__ == "__main__":
    # Demo
    print("=" * 50)
    print("IMEI Utilities Demo")
    print("=" * 50)
    
    # Validate
    test_imei = "490154203237518"
    print(f"\nValidating {test_imei}: {validate(test_imei)}")
    
    # Parse
    parsed = parse(test_imei)
    print(f"Parsed: TAC={parsed['tac']}, SNR={parsed['snr']}, CD={parsed['cd']}")
    
    # Format
    print(f"Standard format: {format_imei(test_imei, 'standard')}")
    print(f"Compact format: {format_imei(test_imei, 'compact')}")
    
    # Generate
    random_imei = generate_random()
    print(f"\nGenerated random IMEI: {random_imei}")
    print(f"Valid: {validate(random_imei)}")
    
    # Class-based
    validator = IMEIValidator(test_imei)
    print(f"\nClass-based validator: {validator}")
    print(f"Is valid: {validator.is_valid}")
    print(f"TAC: {validator.tac}")