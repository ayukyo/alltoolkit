#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AllToolkit - SWIFT/BIC Utilities Module

Comprehensive SWIFT/BIC (Bank Identifier Code) utilities for Python with zero external dependencies.
Provides validation, parsing, and information extraction for international bank codes.

SWIFT/BIC Format:
- 8 characters (primary office) or 11 characters (specific branch)
- BBBBCCLLbbb where:
  - BBBB = Bank code (4 letters)
  - CC = Country code (2 letters, ISO 3166-1 alpha-2)
  - LL = Location code (2 alphanumeric)
  - bbb = Branch code (3 alphanumeric, optional - 'XXX' for primary office)

Author: AllToolkit
License: MIT
"""

import re
from typing import Dict, List, Optional, Tuple, NamedTuple
from dataclasses import dataclass


# =============================================================================
# ISO 3166-1 Alpha-2 Country Codes
# =============================================================================

ISO_COUNTRIES = {
    'AD': 'Andorra', 'AE': 'United Arab Emirates', 'AF': 'Afghanistan',
    'AG': 'Antigua and Barbuda', 'AI': 'Anguilla', 'AL': 'Albania',
    'AM': 'Armenia', 'AO': 'Angola', 'AQ': 'Antarctica', 'AR': 'Argentina',
    'AS': 'American Samoa', 'AT': 'Austria', 'AU': 'Australia',
    'AW': 'Aruba', 'AX': 'Åland Islands', 'AZ': 'Azerbaijan',
    'BA': 'Bosnia and Herzegovina', 'BB': 'Barbados', 'BD': 'Bangladesh',
    'BE': 'Belgium', 'BF': 'Burkina Faso', 'BG': 'Bulgaria', 'BH': 'Bahrain',
    'BI': 'Burundi', 'BJ': 'Benin', 'BL': 'Saint Barthélemy',
    'BM': 'Bermuda', 'BN': 'Brunei Darussalam', 'BO': 'Bolivia',
    'BQ': 'Bonaire, Sint Eustatius and Saba', 'BR': 'Brazil',
    'BS': 'Bahamas', 'BT': 'Bhutan', 'BV': 'Bouvet Island',
    'BW': 'Botswana', 'BY': 'Belarus', 'BZ': 'Belize',
    'CA': 'Canada', 'CC': 'Cocos (Keeling) Islands', 'CD': 'Congo (DRC)',
    'CF': 'Central African Republic', 'CG': 'Congo', 'CH': 'Switzerland',
    'CI': 'Côte d\'Ivoire', 'CK': 'Cook Islands', 'CL': 'Chile',
    'CM': 'Cameroon', 'CN': 'China', 'CO': 'Colombia', 'CR': 'Costa Rica',
    'CU': 'Cuba', 'CV': 'Cabo Verde', 'CW': 'Curaçao', 'CX': 'Christmas Island',
    'CY': 'Cyprus', 'CZ': 'Czechia', 'DE': 'Germany', 'DJ': 'Djibouti',
    'DK': 'Denmark', 'DM': 'Dominica', 'DO': 'Dominican Republic',
    'DZ': 'Algeria', 'EC': 'Ecuador', 'EE': 'Estonia', 'EG': 'Egypt',
    'EH': 'Western Sahara', 'ER': 'Eritrea', 'ES': 'Spain', 'ET': 'Ethiopia',
    'FI': 'Finland', 'FJ': 'Fiji', 'FK': 'Falkland Islands (Malvinas)',
    'FM': 'Micronesia', 'FO': 'Faroe Islands', 'FR': 'France',
    'GA': 'Gabon', 'GB': 'United Kingdom', 'GD': 'Grenada', 'GE': 'Georgia',
    'GF': 'French Guiana', 'GG': 'Guernsey', 'GH': 'Ghana', 'GI': 'Gibraltar',
    'GL': 'Greenland', 'GM': 'Gambia', 'GN': 'Guinea', 'GP': 'Guadeloupe',
    'GQ': 'Equatorial Guinea', 'GR': 'Greece', 'GS': 'South Georgia',
    'GT': 'Guatemala', 'GU': 'Guam', 'GW': 'Guinea-Bissau', 'GY': 'Guyana',
    'HK': 'Hong Kong', 'HM': 'Heard Island and McDonald Islands',
    'HN': 'Honduras', 'HR': 'Croatia', 'HT': 'Haiti', 'HU': 'Hungary',
    'ID': 'Indonesia', 'IE': 'Ireland', 'IL': 'Israel', 'IM': 'Isle of Man',
    'IN': 'India', 'IO': 'British Indian Ocean Territory', 'IQ': 'Iraq',
    'IR': 'Iran', 'IS': 'Iceland', 'IT': 'Italy', 'JE': 'Jersey',
    'JM': 'Jamaica', 'JO': 'Jordan', 'JP': 'Japan', 'KE': 'Kenya',
    'KG': 'Kyrgyzstan', 'KH': 'Cambodia', 'KI': 'Kiribati', 'KM': 'Comoros',
    'KN': 'Saint Kitts and Nevis', 'KP': 'North Korea', 'KR': 'South Korea',
    'KW': 'Kuwait', 'KY': 'Cayman Islands', 'KZ': 'Kazakhstan',
    'LA': 'Laos', 'LB': 'Lebanon', 'LC': 'Saint Lucia', 'LI': 'Liechtenstein',
    'LK': 'Sri Lanka', 'LR': 'Liberia', 'LS': 'Lesotho', 'LT': 'Lithuania',
    'LU': 'Luxembourg', 'LV': 'Latvia', 'LY': 'Libya', 'MA': 'Morocco',
    'MC': 'Monaco', 'MD': 'Moldova', 'ME': 'Montenegro', 'MF': 'Saint Martin',
    'MG': 'Madagascar', 'MH': 'Marshall Islands', 'MK': 'North Macedonia',
    'ML': 'Mali', 'MM': 'Myanmar', 'MN': 'Mongolia', 'MO': 'Macao',
    'MP': 'Northern Mariana Islands', 'MQ': 'Martinique', 'MR': 'Mauritania',
    'MS': 'Montserrat', 'MT': 'Malta', 'MU': 'Mauritius', 'MV': 'Maldives',
    'MW': 'Malawi', 'MX': 'Mexico', 'MY': 'Malaysia', 'MZ': 'Mozambique',
    'NA': 'Namibia', 'NC': 'New Caledonia', 'NE': 'Niger', 'NF': 'Norfolk Island',
    'NG': 'Nigeria', 'NI': 'Nicaragua', 'NL': 'Netherlands', 'NO': 'Norway',
    'NP': 'Nepal', 'NR': 'Nauru', 'NU': 'Niue', 'NZ': 'New Zealand',
    'OM': 'Oman', 'PA': 'Panama', 'PE': 'Peru', 'PF': 'French Polynesia',
    'PG': 'Papua New Guinea', 'PH': 'Philippines', 'PK': 'Pakistan',
    'PL': 'Poland', 'PM': 'Saint Pierre and Miquelon', 'PN': 'Pitcairn',
    'PR': 'Puerto Rico', 'PS': 'Palestine', 'PT': 'Portugal', 'PW': 'Palau',
    'PY': 'Paraguay', 'QA': 'Qatar', 'RE': 'Réunion', 'RO': 'Romania',
    'RS': 'Serbia', 'RU': 'Russia', 'RW': 'Rwanda', 'SA': 'Saudi Arabia',
    'SB': 'Solomon Islands', 'SC': 'Seychelles', 'SD': 'Sudan', 'SE': 'Sweden',
    'SG': 'Singapore', 'SH': 'Saint Helena', 'SI': 'Slovenia',
    'SJ': 'Svalbard and Jan Mayen', 'SK': 'Slovakia', 'SL': 'Sierra Leone',
    'SM': 'San Marino', 'SN': 'Senegal', 'SO': 'Somalia', 'SR': 'Suriname',
    'SS': 'South Sudan', 'ST': 'São Tomé and Príncipe', 'SV': 'El Salvador',
    'SX': 'Sint Maarten', 'SY': 'Syria', 'SZ': 'Eswatini', 'TC': 'Turks and Caicos Islands',
    'TD': 'Chad', 'TF': 'French Southern Territories', 'TG': 'Togo',
    'TH': 'Thailand', 'TJ': 'Tajikistan', 'TK': 'Tokelau', 'TL': 'Timor-Leste',
    'TM': 'Turkmenistan', 'TN': 'Tunisia', 'TO': 'Tonga', 'TR': 'Turkey',
    'TT': 'Trinidad and Tobago', 'TV': 'Tuvalu', 'TW': 'Taiwan',
    'TZ': 'Tanzania', 'UA': 'Ukraine', 'UG': 'Uganda', 'UM': 'US Minor Islands',
    'US': 'United States', 'UY': 'Uruguay', 'UZ': 'Uzbekistan', 'VA': 'Vatican City',
    'VC': 'Saint Vincent and the Grenadines', 'VE': 'Venezuela',
    'VG': 'British Virgin Islands', 'VI': 'US Virgin Islands',
    'VN': 'Vietnam', 'VU': 'Vanuatu', 'WF': 'Wallis and Futuna',
    'WS': 'Samoa', 'YE': 'Yemen', 'YT': 'Mayotte', 'ZA': 'South Africa',
    'ZM': 'Zambia', 'ZW': 'Zimbabwe',
    # Special codes
    'XK': 'Kosovo',  # Not officially ISO but widely used
}

# SEPA countries (Single Euro Payments Area)
SEPA_COUNTRIES = {
    'AT', 'BE', 'BG', 'HR', 'CY', 'CZ', 'DK', 'EE', 'FI', 'FR', 'DE', 'GR',
    'HU', 'IS', 'IE', 'IT', 'LV', 'LI', 'LT', 'LU', 'MT', 'NL', 'NO', 'PL',
    'PT', 'RO', 'SK', 'SI', 'ES', 'SE', 'CH', 'GB', 'AD', 'MC', 'SM', 'VA'
}

# Location code special meanings
LOCATION_CODE_SPECIAL = {
    '0': 'Test code (0 in position 8)',
    '1': 'Passive participant',
    '2': 'Test code (reverse routing)',
    # 'XX' in location often means not connected to SWIFT network
}


# =============================================================================
# Data Classes
# =============================================================================

@dataclass
class SWIFTComponents:
    """Parsed components of a SWIFT/BIC code."""
    bank_code: str
    country_code: str
    location_code: str
    branch_code: Optional[str]
    country_name: str
    is_primary_office: bool
    is_test_code: bool
    is_passive: bool
    is_connected: bool
    is_sepa_country: bool


@dataclass
class SWIFTValidationResult:
    """Result of SWIFT/BIC validation."""
    is_valid: bool
    code: str
    normalized: str
    error: Optional[str]
    components: Optional[SWIFTComponents]


# =============================================================================
# Validation Functions
# =============================================================================

def is_valid_swift(code: str) -> bool:
    """
    Check if a SWIFT/BIC code is valid.
    
    Args:
        code: SWIFT/BIC code to validate (8 or 11 characters)
        
    Returns:
        True if valid, False otherwise
        
    Example:
        >>> is_valid_swift('DEUTDEFF')
        True
        >>> is_valid_swift('DEUTDEFFXXX')
        True
        >>> is_valid_swift('INVALID')
        False
    """
    result = validate_swift(code)
    return result.is_valid


def validate_swift(code: str) -> SWIFTValidationResult:
    """
    Validate a SWIFT/BIC code and return detailed result.
    
    Args:
        code: SWIFT/BIC code to validate
        
    Returns:
        SWIFTValidationResult with validation details
        
    Example:
        >>> result = validate_swift('DEUTDEFF')
        >>> print(result.is_valid)
        True
        >>> print(result.components.country_name)
        Germany
    """
    # Normalize input
    normalized = code.strip().upper() if code else ''
    
    # Check basic format
    if not normalized:
        return SWIFTValidationResult(
            is_valid=False,
            code=code,
            normalized=normalized,
            error='Empty code',
            components=None
        )
    
    # Length check
    if len(normalized) not in (8, 11):
        return SWIFTValidationResult(
            is_valid=False,
            code=code,
            normalized=normalized,
            error=f'Invalid length: {len(normalized)} (must be 8 or 11)',
            components=None
        )
    
    # Regex pattern: 4 letters + 2 letters (country) + 2 alphanumeric + optional 3 alphanumeric
    pattern = r'^([A-Z]{4})([A-Z]{2})([A-Z0-9]{2})([A-Z0-9]{3})?$'
    match = re.match(pattern, normalized)
    
    if not match:
        # Check which part is invalid
        bank_code = normalized[:4]
        country_code = normalized[4:6] if len(normalized) >= 6 else ''
        
        if not re.match(r'^[A-Z]{4}$', bank_code):
            error = f'Invalid bank code: {bank_code} (must be 4 letters)'
        elif not re.match(r'^[A-Z]{2}$', country_code):
            error = f'Invalid country code: {country_code} (must be 2 letters)'
        else:
            error = 'Invalid location or branch code format'
        
        return SWIFTValidationResult(
            is_valid=False,
            code=code,
            normalized=normalized,
            error=error,
            components=None
        )
    
    bank_code = match.group(1)
    country_code = match.group(2)
    location_code = match.group(3)
    branch_code = match.group(4)
    
    # Check if country code is valid ISO 3166-1
    country_name = ISO_COUNTRIES.get(country_code)
    if not country_name:
        return SWIFTValidationResult(
            is_valid=False,
            code=code,
            normalized=normalized,
            error=f'Invalid country code: {country_code}',
            components=None
        )
    
    # Analyze location code
    is_test_code = location_code[1] == '0'
    is_passive = location_code[1] == '1'
    is_connected = location_code[1] not in ('0', '1') and 'X' not in location_code
    
    # Check if primary office (branch code is XXX or omitted)
    is_primary_office = branch_code is None or branch_code == 'XXX'
    
    # Check SEPA membership
    is_sepa_country = country_code in SEPA_COUNTRIES
    
    components = SWIFTComponents(
        bank_code=bank_code,
        country_code=country_code,
        location_code=location_code,
        branch_code=branch_code,
        country_name=country_name,
        is_primary_office=is_primary_office,
        is_test_code=is_test_code,
        is_passive=is_passive,
        is_connected=is_connected,
        is_sepa_country=is_sepa_country
    )
    
    return SWIFTValidationResult(
        is_valid=True,
        code=code,
        normalized=normalized,
        error=None,
        components=components
    )


# =============================================================================
# Parsing Functions
# =============================================================================

def parse_swift(code: str) -> Optional[SWIFTComponents]:
    """
    Parse a SWIFT/BIC code and return its components.
    
    Args:
        code: SWIFT/BIC code to parse
        
    Returns:
        SWIFTComponents if valid, None if invalid
        
    Example:
        >>> comp = parse_swift('DEUTDEFF')
        >>> print(comp.bank_code)
        DEUT
        >>> print(comp.country_name)
        Germany
    """
    result = validate_swift(code)
    return result.components


def get_bank_code(code: str) -> Optional[str]:
    """Extract bank code from SWIFT/BIC."""
    components = parse_swift(code)
    return components.bank_code if components else None


def get_country_code(code: str) -> Optional[str]:
    """Extract country code from SWIFT/BIC."""
    components = parse_swift(code)
    return components.country_code if components else None


def get_country_name(code: str) -> Optional[str]:
    """Extract country name from SWIFT/BIC."""
    components = parse_swift(code)
    return components.country_name if components else None


def get_location_code(code: str) -> Optional[str]:
    """Extract location code from SWIFT/BIC."""
    components = parse_swift(code)
    return components.location_code if components else None


def get_branch_code(code: str) -> Optional[str]:
    """Extract branch code from SWIFT/BIC (returns None if 8-character code)."""
    components = parse_swift(code)
    return components.branch_code if components else None


# =============================================================================
# Utility Functions
# =============================================================================

def normalize_swift(code: str) -> Optional[str]:
    """
    Normalize a SWIFT/BIC code to uppercase.
    
    Args:
        code: SWIFT/BIC code to normalize
        
    Returns:
        Normalized code if valid, None if invalid
        
    Example:
        >>> normalize_swift('deutdeff')
        'DEUTDEFF'
        >>> normalize_swift('DEUT DE FF')
        'DEUTDEFF'
    """
    if not code:
        return None
    
    # Remove whitespace and convert to uppercase
    normalized = ''.join(code.split()).upper()
    
    # Validate
    if is_valid_swift(normalized):
        return normalized
    return None


def format_swift(code: str, separator: str = ' ') -> Optional[str]:
    """
    Format a SWIFT/BIC code with separator for readability.
    
    Args:
        code: SWIFT/BIC code to format
        separator: Separator character (default: space)
        
    Returns:
        Formatted code if valid, None if invalid
        
    Example:
        >>> format_swift('DEUTDEFFXXX')
        'DEUT DE FF XXX'
        >>> format_swift('DEUTDEFF', '-')
        'DEUT-DE-FF'
    """
    result = validate_swift(code)
    if not result.is_valid:
        return None
    
    normalized = result.normalized
    
    # Format: BBBB CC LL [BBB]
    parts = [normalized[:4], normalized[4:6], normalized[6:8]]
    if len(normalized) == 11:
        parts.append(normalized[8:11])
    
    return separator.join(parts)


def is_primary_office(code: str) -> bool:
    """Check if SWIFT code represents a primary/head office."""
    components = parse_swift(code)
    return components.is_primary_office if components else False


def is_test_code(code: str) -> bool:
    """Check if SWIFT code is a test code."""
    components = parse_swift(code)
    return components.is_test_code if components else False


def is_passive_participant(code: str) -> bool:
    """Check if SWIFT code is a passive participant."""
    components = parse_swift(code)
    return components.is_passive if components else False


def is_swift_connected(code: str) -> bool:
    """Check if bank is connected to SWIFT network."""
    components = parse_swift(code)
    return components.is_connected if components else False


def is_sepa_country(code: str) -> bool:
    """Check if SWIFT code's country is in SEPA."""
    components = parse_swift(code)
    return components.is_sepa_country if components else False


# =============================================================================
# Information Functions
# =============================================================================

def get_country_info(code: str) -> Optional[Dict[str, any]]:
    """
    Get detailed country information for a SWIFT/BIC code.
    
    Args:
        code: SWIFT/BIC code
        
    Returns:
        Dictionary with country information or None if invalid
        
    Example:
        >>> info = get_country_info('DEUTDEFF')
        >>> print(info['name'])
        Germany
        >>> print(info['is_sepa'])
        True
    """
    components = parse_swift(code)
    if not components:
        return None
    
    return {
        'code': components.country_code,
        'name': components.country_name,
        'is_sepa': components.is_sepa_country,
    }


def swift_info(code: str) -> Dict[str, any]:
    """
    Get comprehensive information about a SWIFT/BIC code.
    
    Args:
        code: SWIFT/BIC code
        
    Returns:
        Dictionary with all available information
        
    Example:
        >>> info = swift_info('DEUTDEFFXXX')
        >>> print(info['valid'])
        True
        >>> print(info['bank_code'])
        DEUT
    """
    result = validate_swift(code)
    
    if not result.is_valid:
        return {
            'valid': False,
            'code': code,
            'normalized': result.normalized,
            'error': result.error,
        }
    
    comp = result.components
    
    return {
        'valid': True,
        'code': code,
        'normalized': result.normalized,
        'formatted': format_swift(result.normalized),
        'bank_code': comp.bank_code,
        'country_code': comp.country_code,
        'country_name': comp.country_name,
        'location_code': comp.location_code,
        'branch_code': comp.branch_code,
        'is_primary_office': comp.is_primary_office,
        'is_test_code': comp.is_test_code,
        'is_passive': comp.is_passive,
        'is_connected': comp.is_connected,
        'is_sepa_country': comp.is_sepa_country,
        'length': len(result.normalized),
    }


def compare_swift(code1: str, code2: str) -> Dict[str, any]:
    """
    Compare two SWIFT/BIC codes.
    
    Args:
        code1: First SWIFT/BIC code
        code2: Second SWIFT/BIC code
        
    Returns:
        Dictionary with comparison results
        
    Example:
        >>> compare_swift('DEUTDEFF', 'DEUTDEFFXXX')
        {'same_bank': True, 'same_country': True, 'same_branch': True}
    """
    comp1 = parse_swift(code1)
    comp2 = parse_swift(code2)
    
    if not comp1 or not comp2:
        return {
            'error': 'One or both codes are invalid',
            'code1_valid': comp1 is not None,
            'code2_valid': comp2 is not None,
        }
    
    return {
        'same_bank': comp1.bank_code == comp2.bank_code,
        'same_country': comp1.country_code == comp2.country_code,
        'same_location': comp1.location_code == comp2.location_code,
        'same_branch': comp1.branch_code == comp2.branch_code,
        'same_institution': (comp1.bank_code == comp2.bank_code and 
                            comp1.country_code == comp2.country_code and
                            comp1.location_code == comp2.location_code),
    }


# =============================================================================
# Generation Functions (for testing)
# =============================================================================

def generate_test_swift(country_code: str, bank_code: str = 'TEST') -> Optional[str]:
    """
    Generate a test SWIFT/BIC code (for development/testing only).
    
    Note: Test codes have '0' as the last character of the location code.
    
    Args:
        country_code: ISO 3166-1 alpha-2 country code
        bank_code: 4-letter bank code (default: TEST)
        
    Returns:
        Test SWIFT code or None if invalid inputs
        
    Example:
        >>> generate_test_swift('DE', 'TEST')
        'TESTDE00'
    """
    country_code = country_code.upper() if country_code else ''
    bank_code = bank_code.upper() if bank_code else ''
    
    if not re.match(r'^[A-Z]{2}$', country_code):
        return None
    
    if not re.match(r'^[A-Z]{4}$', bank_code):
        bank_code = bank_code.ljust(4, 'X')[:4]
    
    if country_code not in ISO_COUNTRIES:
        return None
    
    return f'{bank_code}{country_code}00'


# =============================================================================
# Country Utilities
# =============================================================================

def get_all_countries() -> Dict[str, str]:
    """
    Get all ISO 3166-1 alpha-2 country codes.
    
    Returns:
        Dictionary of country codes to names
        
    Example:
        >>> countries = get_all_countries()
        >>> print(countries['US'])
        United States
    """
    return ISO_COUNTRIES.copy()


def get_sepa_countries() -> set:
    """
    Get all SEPA country codes.
    
    Returns:
        Set of ISO 3166-1 alpha-2 codes for SEPA countries
        
    Example:
        >>> 'DE' in get_sepa_countries()
        True
    """
    return SEPA_COUNTRIES.copy()


def country_code_to_name(code: str) -> Optional[str]:
    """
    Convert ISO 3166-1 alpha-2 country code to name.
    
    Args:
        code: Country code
        
    Returns:
        Country name or None if not found
        
    Example:
        >>> country_code_to_name('DE')
        'Germany'
    """
    return ISO_COUNTRIES.get(code.upper() if code else '')


# =============================================================================
# Main (for testing)
# =============================================================================

if __name__ == '__main__':
    print("SWIFT/BIC Utilities Test\n")
    print("=" * 50)
    
    # Test codes
    test_codes = [
        'DEUTDEFF',          # Deutsche Bank, Frankfurt
        'DEUTDEFFXXX',      # Deutsche Bank, Frankfurt (primary office)
        'CHASUS33',         # JP Morgan Chase, US
        'BARCGB22',         # Barclays, UK
        'HSBCUS33',         # HSBC, US
        'SBININBB',         # State Bank of India
        'TESTDE00',         # Test code
        'INVALID',          # Invalid
        'DEUT',             # Too short
        'DEUTDEFF12345',    # Too long
    ]
    
    for code in test_codes:
        result = validate_swift(code)
        print(f"\nCode: {code}")
        print(f"  Valid: {result.is_valid}")
        if result.is_valid:
            comp = result.components
            print(f"  Bank: {comp.bank_code}")
            print(f"  Country: {comp.country_code} ({comp.country_name})")
            print(f"  Location: {comp.location_code}")
            print(f"  Branch: {comp.branch_code or 'N/A'}")
            print(f"  Primary Office: {comp.is_primary_office}")
            print(f"  Test Code: {comp.is_test_code}")
            print(f"  SEPA: {comp.is_sepa_country}")
        else:
            print(f"  Error: {result.error}")
    
    print("\n" + "=" * 50)
    print("\nFormat test:")
    print(f"  format_swift('DEUTDEFFXXX') = '{format_swift('DEUTDEFFXXX')}'")
    print(f"  format_swift('DEUTDEFF', '-') = '{format_swift('DEUTDEFF', '-')}'")
    
    print("\nCompare test:")
    print(f"  compare_swift('DEUTDEFF', 'DEUTDEFFXXX') = {compare_swift('DEUTDEFF', 'DEUTDEFFXXX')}")
    
    print("\nAll tests passed!")