"""
AllToolkit - Python Phone Utilities

A zero-dependency, production-ready phone number utility module.
Supports phone validation, parsing, formatting, normalization, and country detection.

Author: AllToolkit
License: MIT
"""

import re
from typing import Optional, Tuple, List, Dict, Any
from dataclasses import dataclass


@dataclass
class PhoneNumber:
    """Represents a parsed phone number."""
    country_code: str       # Country calling code (e.g., "+1", "+86")
    national_number: str    # National significant number (without country code)
    original: str           # Original phone string
    international: str      # International format (e.g., "+1 234-567-8900")
    national: str           # National format (e.g., "(234) 567-8900")
    e164: str               # E.164 format (e.g., "+12345678900")
    country: str            # ISO 3166-1 alpha-2 country code
    is_valid: bool          # Validation result
    number_type: str        # "mobile", "landline", "toll_free", "premium", "unknown"


class PhoneUtils:
    """
    Phone number utilities.
    
    Provides functions for:
    - Phone number validation (international and national formats)
    - Phone number parsing and normalization
    - Country detection from phone number
    - Number type detection (mobile, landline, toll-free, etc.)
    - Formatting (E.164, international, national)
    - Bulk phone number processing
    """

    # Country calling codes with their ISO country codes
    COUNTRY_CODES = {
        "+1": ["US", "CA"],           # USA, Canada
        "+7": ["RU", "KZ"],           # Russia, Kazakhstan
        "+20": ["EG"],                # Egypt
        "+27": ["ZA"],                # South Africa
        "+30": ["GR"],                # Greece
        "+31": ["NL"],                # Netherlands
        "+32": ["BE"],                # Belgium
        "+33": ["FR"],                # France
        "+34": ["ES"],                # Spain
        "+36": ["HU"],                # Hungary
        "+39": ["IT"],                # Italy
        "+40": ["RO"],                # Romania
        "+41": ["CH"],                # Switzerland
        "+43": ["AT"],                # Austria
        "+44": ["GB"],                # United Kingdom
        "+45": ["DK"],                # Denmark
        "+46": ["SE"],                # Sweden
        "+47": ["NO"],                # Norway
        "+48": ["PL"],                # Poland
        "+49": ["DE"],                # Germany
        "+51": ["PE"],                # Peru
        "+52": ["MX"],                # Mexico
        "+53": ["CU"],                # Cuba
        "+54": ["AR"],                # Argentina
        "+55": ["BR"],                # Brazil
        "+56": ["CL"],                # Chile
        "+57": ["CO"],                # Colombia
        "+58": ["VE"],                # Venezuela
        "+60": ["MY"],                # Malaysia
        "+61": ["AU"],                # Australia
        "+62": ["ID"],                # Indonesia
        "+63": ["PH"],                # Philippines
        "+64": ["NZ"],                # New Zealand
        "+65": ["SG"],                # Singapore
        "+66": ["TH"],                # Thailand
        "+81": ["JP"],                # Japan
        "+82": ["KR"],                # South Korea
        "+84": ["VN"],                # Vietnam
        "+86": ["CN"],                # China
        "+90": ["TR"],                # Turkey
        "+91": ["IN"],                # India
        "+92": ["PK"],                # Pakistan
        "+93": ["AF"],                # Afghanistan
        "+94": ["LK"],                # Sri Lanka
        "+95": ["MM"],                # Myanmar
        "+98": ["IR"],                # Iran
        "+212": ["MA"],               # Morocco
        "+213": ["DZ"],               # Algeria
        "+234": ["NG"],               # Nigeria
        "+254": ["KE"],               # Kenya
        "+255": ["TZ"],               # Tanzania
        "+256": ["UG"],               # Uganda
        "+260": ["ZM"],               # Zambia
        "+263": ["ZW"],               # Zimbabwe
        "+351": ["PT"],               # Portugal
        "+352": ["LU"],               # Luxembourg
        "+353": ["IE"],               # Ireland
        "+354": ["IS"],               # Iceland
        "+355": ["AL"],               # Albania
        "+356": ["MT"],               # Malta
        "+357": ["CY"],               # Cyprus
        "+358": ["FI"],               # Finland
        "+359": ["BG"],               # Bulgaria
        "+370": ["LT"],               # Lithuania
        "+371": ["LV"],               # Latvia
        "+372": ["EE"],               # Estonia
        "+373": ["MD"],               # Moldova
        "+374": ["AM"],               # Armenia
        "+375": ["BY"],               # Belarus
        "+376": ["AD"],               # Andorra
        "+377": ["MC"],               # Monaco
        "+378": ["SM"],               # San Marino
        "+380": ["UA"],               # Ukraine
        "+381": ["RS"],               # Serbia
        "+382": ["ME"],               # Montenegro
        "+383": ["XK"],               # Kosovo
        "+385": ["HR"],               # Croatia
        "+386": ["SI"],               # Slovenia
        "+387": ["BA"],               # Bosnia and Herzegovina
        "+389": ["MK"],               # North Macedonia
        "+420": ["CZ"],               # Czech Republic
        "+421": ["SK"],               # Slovakia
        "+423": ["LI"],               # Liechtenstein
        "+852": ["HK"],               # Hong Kong
        "+853": ["MO"],               # Macau
        "+855": ["KH"],               # Cambodia
        "+856": ["LA"],               # Laos
        "+880": ["BD"],               # Bangladesh
        "+886": ["TW"],               # Taiwan
        "+960": ["MV"],               # Maldives
        "+961": ["LB"],               # Lebanon
        "+962": ["JO"],               # Jordan
        "+963": ["SY"],               # Syria
        "+964": ["IQ"],               # Iraq
        "+965": ["KW"],               # Kuwait
        "+966": ["SA"],               # Saudi Arabia
        "+967": ["YE"],               # Yemen
        "+968": ["OM"],               # Oman
        "+970": ["PS"],               # Palestine
        "+971": ["AE"],               # UAE
        "+972": ["IL"],               # Israel
        "+973": ["BH"],               # Bahrain
        "+974": ["QA"],               # Qatar
        "+975": ["BT"],               # Bhutan
        "+976": ["MN"],               # Mongolia
        "+977": ["NP"],               # Nepal
        "+992": ["TJ"],               # Tajikistan
        "+993": ["TM"],               # Turkmenistan
        "+994": ["AZ"],               # Azerbaijan
        "+995": ["GE"],               # Georgia
        "+996": ["KG"],               # Kyrgyzstan
        "+998": ["UZ"],               # Uzbekistan
    }

    # Country name to ISO code mapping
    COUNTRY_NAMES = {
        "US": "United States",
        "CA": "Canada",
        "CN": "China",
        "GB": "United Kingdom",
        "DE": "Germany",
        "FR": "France",
        "JP": "Japan",
        "KR": "South Korea",
        "IN": "India",
        "AU": "Australia",
        "BR": "Brazil",
        "RU": "Russia",
        "IT": "Italy",
        "ES": "Spain",
        "MX": "Mexico",
        "ID": "Indonesia",
        "TR": "Turkey",
        "SA": "Saudi Arabia",
        "AR": "Argentina",
        "ZA": "South Africa",
    }

    # National number length ranges by country (min, max)
    NATIONAL_LENGTHS = {
        "US": (10, 10),
        "CA": (10, 10),
        "CN": (10, 11),  # 10 for 400/800 toll-free, 11 for mobile/landline
        "GB": (10, 11),
        "DE": (10, 12),
        "FR": (9, 10),
        "JP": (9, 11),
        "KR": (9, 11),
        "IN": (10, 10),
        "AU": (9, 10),
        "BR": (10, 11),
        "RU": (10, 11),
        "IT": (9, 11),
        "ES": (9, 9),
        "MX": (10, 10),
        "ID": (10, 13),
        "TR": (10, 10),
        "SA": (9, 9),
        "AR": (10, 10),
        "ZA": (9, 9),
        "SG": (8, 8),
        "MY": (9, 10),
        "TH": (9, 10),
        "VN": (9, 10),
        "PH": (10, 10),
        "NZ": (9, 10),
        "HK": (8, 8),
        "TW": (9, 10),
        "AE": (9, 9),
        "IL": (9, 9),
        "CH": (9, 9),
        "AT": (10, 13),
        "BE": (9, 9),
        "NL": (9, 9),
        "SE": (9, 11),
        "NO": (8, 8),
        "DK": (8, 8),
        "FI": (10, 10),
        "PL": (9, 9),
        "PT": (9, 9),
        "GR": (10, 10),
        "IE": (9, 9),
        "CZ": (9, 9),
        "HU": (9, 9),
        "RO": (10, 10),
        "UA": (9, 10),
    }

    # Mobile number prefixes by country
    MOBILE_PREFIXES = {
        # Note: US/Canada NANP numbers cannot be reliably classified as mobile vs landline
        # by prefix alone due to number portability. Left empty to default to landline.
        "CN": ["13", "14", "15", "16", "17", "18", "19"],
        "GB": ["7"],
        "DE": ["15", "16", "17"],
        "FR": ["6", "7"],
        "JP": ["70", "80", "90"],
        "KR": ["10"],
        "IN": ["6", "7", "8", "9"],
        "AU": ["4"],
        "BR": ["9"],
        "RU": ["9"],
        "IT": ["3"],
        "ES": ["6", "7"],
        "MX": ["1"],
        "ID": ["8"],
        "TR": ["5"],
        "SA": ["5"],
        "AR": ["9"],
        "ZA": ["6", "7", "8"],
        "SG": ["8", "9"],
        "MY": ["1"],
        "TH": ["6", "8", "9"],
        "VN": ["3", "5", "7", "8", "9"],
        "PH": ["9"],
        "NZ": ["2"],
        "HK": ["5", "6", "7", "9"],
        "TW": ["9"],
        "AE": ["5"],
        "IL": ["5"],
    }

    # Toll-free prefixes by country
    TOLL_FREE_PREFIXES = {
        "US": ["800", "833", "844", "855", "866", "877", "888"],
        "CN": ["400", "800"],
        "GB": ["800", "808"],
        "DE": ["800"],
        "FR": ["800", "805", "809"],
        "JP": ["120", "800"],
        "AU": ["1800"],
        "BR": ["0800"],
        "IN": ["1800"],
    }

    # Premium rate prefixes by country
    PREMIUM_PREFIXES = {
        "US": ["900"],
        "CN": ["96", "95"],
        "GB": ["870", "871", "872", "873", "90"],
        "DE": ["137", "138", "190"],
        "FR": ["89"],
        "AU": ["190"],
    }

    # Regex patterns for phone number extraction
    PHONE_REGEX = re.compile(
        r'(?:^|[\s\(\)\.\-+])'
        r'(\+?\d{1,3})?'
        r'[\s\.\-\(]?'
        r'(\d{2,4})'
        r'[\s\.\-\(]?'
        r'(\d{3,4})'
        r'[\s\.\-]?'
        r'(\d{4,6})'
        r'(?:$|[\s\)\.\-+])'
    )

    # Simple pattern for basic extraction
    SIMPLE_PHONE_REGEX = re.compile(
        r'\+?\d[\d\s\-\(\)\.]{6,}\d'
    )

    @classmethod
    def _clean_phone(cls, phone: str) -> str:
        """Remove all non-digit characters except leading +."""
        if not phone:
            return ""
        # Convert to string if needed
        phone_str = str(phone) if not isinstance(phone, str) else phone
        if not phone_str:
            return ""
        # Keep only digits and leading +
        cleaned = re.sub(r'[^\d+]', '', phone_str)
        # Remove any + that's not at the start
        if cleaned.startswith('+'):
            return '+' + cleaned[1:].replace('+', '')
        return cleaned.replace('+', '')

    @classmethod
    def _extract_country_code(cls, phone: str, require_explicit: bool = False) -> Tuple[Optional[str], str]:
        """
        Extract country code from phone number.
        
        Args:
            phone: Cleaned phone number string
            require_explicit: If True, only extract country code if explicitly marked with +
        
        Returns:
            Tuple of (country_code, national_number)
        """
        cleaned = cls._clean_phone(phone)
        
        if not cleaned:
            return None, ""
        
        # Check if explicitly international (starts with +)
        is_explicit = cleaned.startswith('+')
        
        # If require_explicit and not explicitly international, return as national
        if require_explicit and not is_explicit:
            return None, cleaned
        
        # Handle leading +
        if is_explicit:
            cleaned = cleaned[1:]
        
        # Try to match country codes (longest first)
        sorted_codes = sorted(cls.COUNTRY_CODES.keys(), key=len, reverse=True)
        
        for code in sorted_codes:
            code_digits = code[1:]  # Remove +
            if cleaned.startswith(code_digits):
                return code, cleaned[len(code_digits):]
        
        # No country code found, return as national number
        return None, cleaned

    @classmethod
    def _get_country_from_code(cls, country_code: str) -> Optional[str]:
        """Get primary country from country code."""
        countries = cls.COUNTRY_CODES.get(country_code, [])
        return countries[0] if countries else None

    @classmethod
    def _validate_national_number(cls, national: str, country: str) -> bool:
        """Validate national number length for a country."""
        if not national or not country:
            return False
        
        length_range = cls.NATIONAL_LENGTHS.get(country)
        if not length_range:
            # Default validation: 7-15 digits
            return 7 <= len(national) <= 15
        
        return length_range[0] <= len(national) <= length_range[1]

    @classmethod
    def _detect_number_type(cls, national: str, country: str) -> str:
        """Detect the type of phone number."""
        if not national or not country:
            return "unknown"
        
        # Check toll-free
        toll_free = cls.TOLL_FREE_PREFIXES.get(country, [])
        for prefix in toll_free:
            if national.startswith(prefix):
                return "toll_free"
        
        # Check premium
        premium = cls.PREMIUM_PREFIXES.get(country, [])
        for prefix in premium:
            if national.startswith(prefix):
                return "premium"
        
        # Check mobile
        mobile = cls.MOBILE_PREFIXES.get(country, [])
        for prefix in mobile:
            if national.startswith(prefix):
                return "mobile"
        
        # Default to landline
        return "landline"

    @classmethod
    def _format_national(cls, national: str, country: str) -> str:
        """Format national number according to country conventions."""
        if not national:
            return ""
        
        # Default formatting: group into chunks
        if country in ["US", "CA"]:
            if len(national) == 10:
                return f"({national[:3]}) {national[3:6]}-{national[6:]}"
        elif country == "CN":
            if len(national) == 11:
                return f"{national[:3]} {national[4:7]} {national[7:]}"
        elif country == "GB":
            if len(national) == 10:
                return f"{national[:4]} {national[4:6]} {national[6:]}"
            elif len(national) == 11:
                return f"{national[:5]} {national[5:6]} {national[6:]}"
        elif country == "JP":
            if len(national) == 10:
                return f"{national[:2]}-{national[2:6]}-{national[6:]}"
            elif len(national) == 11:
                return f"{national[:3]}-{national[3:4]}-{national[4:]}"
        elif country == "DE":
            # German numbers vary widely
            return f"{national[:4]} {national[4:]}"
        elif country == "FR":
            if len(national) == 9:
                return f"{national[0]} {national[1:3]} {national[3:5]} {national[5:7]} {national[7:]}"
        elif country == "AU":
            if len(national) == 9:
                return f"{national[:3]} {national[3:6]} {national[6:]}"
            elif len(national) == 10:
                return f"{national[:4]} {national[4:6]} {national[6:]}"
        
        # Default: group by 3-4 digits
        if len(national) <= 4:
            return national
        elif len(national) <= 7:
            return f"{national[:3]} {national[3:]}"
        elif len(national) <= 10:
            return f"{national[:3]} {national[3:6]} {national[6:]}"
        else:
            return f"{national[:4]} {national[4:7]} {national[7:]}"


# ============================================================================
# Public API Functions
# ============================================================================

def validate(phone: str, country: Optional[str] = None) -> bool:
    """
    Validate a phone number.
    
    Args:
        phone: Phone number string (with or without country code)
        country: Optional ISO country code to use for validation
        
    Returns:
        True if the phone number is valid, False otherwise
    """
    if not phone:
        return False
    
    cleaned = PhoneUtils._clean_phone(phone)
    if not cleaned:
        return False
    
    # If country is specified, treat as national number unless explicitly international
    if country:
        country_code, national = PhoneUtils._extract_country_code(cleaned, require_explicit=True)
        if country_code:
            # Explicitly international
            return PhoneUtils._validate_national_number(national, PhoneUtils._get_country_from_code(country_code))
        else:
            # Treat as national number for the specified country
            return PhoneUtils._validate_national_number(cleaned, country)
    
    # No country specified - only extract country code if explicitly international (+)
    country_code, national = PhoneUtils._extract_country_code(cleaned, require_explicit=True)
    
    if country_code:
        detected_country = PhoneUtils._get_country_from_code(country_code)
        return PhoneUtils._validate_national_number(national, detected_country)
    
    # No country code found - basic validation (7-15 digits)
    return 7 <= len(cleaned) <= 15


def parse(phone: str, default_country: Optional[str] = None) -> Optional[PhoneNumber]:
    """
    Parse a phone number into its components.
    
    Args:
        phone: Phone number string
        default_country: Optional ISO country code if no country code in phone
        
    Returns:
        PhoneNumber object or None if parsing fails
    """
    if not phone:
        return None
    
    cleaned = PhoneUtils._clean_phone(phone)
    if not cleaned:
        return None
    
    original = phone.strip()
    
    # If default_country specified, only extract country code if explicitly international
    if default_country:
        country_code, national = PhoneUtils._extract_country_code(cleaned, require_explicit=True)
        country = default_country
        if country_code:
            # Explicitly international - use detected country
            country = PhoneUtils._get_country_from_code(country_code)
    else:
        # No default country - detect from country code
        country_code, national = PhoneUtils._extract_country_code(cleaned)
        country = PhoneUtils._get_country_from_code(country_code) if country_code else None
    
    # Validate
    is_valid = PhoneUtils._validate_national_number(national if country_code else cleaned, country) if country else len(cleaned) >= 7
    
    if not is_valid:
        return None
    
    # Use appropriate national number
    final_national = national if country_code else cleaned
    
    # Build country code for output
    output_country_code = country_code
    if not output_country_code and country:
        # Look up country code from ISO country
        for code, countries in PhoneUtils.COUNTRY_CODES.items():
            if country in countries:
                output_country_code = code
                break
    
    # Format numbers
    if output_country_code:
        e164 = f"{output_country_code}{final_national}"
        international = f"{output_country_code} {final_national}"
    else:
        e164 = f"+{final_national}"
        international = f"+{final_national}"
    
    national_formatted = PhoneUtils._format_national(final_national, country) if country else final_national
    
    # Detect type
    number_type = PhoneUtils._detect_number_type(final_national, country) if country else "unknown"
    
    return PhoneNumber(
        country_code=output_country_code or "",
        national_number=final_national,
        original=original,
        international=international,
        national=national_formatted,
        e164=e164,
        country=country or "UNKNOWN",
        is_valid=is_valid,
        number_type=number_type
    )


def normalize(phone: str, default_country: Optional[str] = None) -> Optional[str]:
    """
    Normalize a phone number to E.164 format.
    
    Args:
        phone: Phone number string
        default_country: Optional ISO country code if no country code in phone
        
    Returns:
        E.164 formatted phone number or None if invalid
    """
    parsed = parse(phone, default_country)
    return parsed.e164 if parsed else None


def format_international(phone: str, default_country: Optional[str] = None) -> Optional[str]:
    """
    Format phone number in international format.
    
    Args:
        phone: Phone number string
        default_country: Optional ISO country code
        
    Returns:
        International formatted phone number or None if invalid
    """
    parsed = parse(phone, default_country)
    return parsed.international if parsed else None


def format_national(phone: str, default_country: Optional[str] = None) -> Optional[str]:
    """
    Format phone number in national format.
    
    Args:
        phone: Phone number string
        default_country: Optional ISO country code
        
    Returns:
        National formatted phone number or None if invalid
    """
    parsed = parse(phone, default_country)
    return parsed.national if parsed else None


def get_country_code(phone: str) -> Optional[str]:
    """
    Extract country code from phone number.
    
    Args:
        phone: Phone number string
        
    Returns:
        Country code (e.g., "+1", "+86") or None
    """
    if not phone:
        return None
    
    cleaned = PhoneUtils._clean_phone(phone)
    country_code, _ = PhoneUtils._extract_country_code(cleaned)
    return country_code


def get_country(phone: str) -> Optional[str]:
    """
    Get country from phone number.
    
    Args:
        phone: Phone number string
        
    Returns:
        ISO country code or None
    """
    if not phone:
        return None
    
    cleaned = PhoneUtils._clean_phone(phone)
    country_code, _ = PhoneUtils._extract_country_code(cleaned)
    
    if country_code:
        return PhoneUtils._get_country_from_code(country_code)
    return None


def get_country_name(country_code: str) -> Optional[str]:
    """
    Get country name from ISO code.
    
    Args:
        country_code: ISO 3166-1 alpha-2 country code
        
    Returns:
        Country name or None
    """
    return PhoneUtils.COUNTRY_NAMES.get(country_code)


def get_number_type(phone: str, default_country: Optional[str] = None) -> Optional[str]:
    """
    Detect phone number type (mobile, landline, toll-free, premium).
    
    Args:
        phone: Phone number string
        default_country: Optional ISO country code
        
    Returns:
        Number type or None if invalid
    """
    parsed = parse(phone, default_country)
    return parsed.number_type if parsed else None


def is_mobile(phone: str, default_country: Optional[str] = None) -> bool:
    """
    Check if phone number is a mobile number.
    
    Args:
        phone: Phone number string
        default_country: Optional ISO country code
        
    Returns:
        True if mobile, False otherwise
    """
    return get_number_type(phone, default_country) == "mobile"


def is_landline(phone: str, default_country: Optional[str] = None) -> bool:
    """
    Check if phone number is a landline.
    
    Args:
        phone: Phone number string
        default_country: Optional ISO country code
        
    Returns:
        True if landline, False otherwise
    """
    return get_number_type(phone, default_country) == "landline"


def is_toll_free(phone: str, default_country: Optional[str] = None) -> bool:
    """
    Check if phone number is toll-free.
    
    Args:
        phone: Phone number string
        default_country: Optional ISO country code
        
    Returns:
        True if toll-free, False otherwise
    """
    return get_number_type(phone, default_country) == "toll_free"


def extract_from_text(text: str) -> List[str]:
    """
    Extract all phone numbers from text.
    
    Args:
        text: Text to search
        
    Returns:
        List of phone number strings
    """
    if not text:
        return []
    
    matches = PhoneUtils.SIMPLE_PHONE_REGEX.findall(text)
    result = []
    
    for match in matches:
        cleaned = PhoneUtils._clean_phone(match)
        if cleaned and len(cleaned) >= 7:
            result.append(match.strip())
    
    return result


def deduplicate(phones: List[str], default_country: Optional[str] = None) -> List[str]:
    """
    Deduplicate phone numbers by E.164 format.
    
    Args:
        phones: List of phone numbers
        default_country: Optional ISO country code
        
    Returns:
        Deduplicated list preserving first occurrence
    """
    if not phones:
        return []
    
    seen = set()
    result = []
    
    for phone in phones:
        e164 = normalize(phone, default_country)
        if e164 and e164 not in seen:
            seen.add(e164)
            result.append(phone)
    
    return result


def sort_by_country(phones: List[str]) -> List[str]:
    """
    Sort phone numbers by country code.
    
    Args:
        phones: List of phone numbers
        
    Returns:
        Sorted list
    """
    if not phones:
        return []
    
    def sort_key(phone):
        code = get_country_code(phone) or "+0"
        return (code, phone)
    
    return sorted(phones, key=sort_key)


def group_by_country(phones: List[str]) -> Dict[str, List[str]]:
    """
    Group phone numbers by country.
    
    Args:
        phones: List of phone numbers
        
    Returns:
        Dictionary mapping country codes to phone lists
    """
    if not phones:
        return {}
    
    grouped: Dict[str, List[str]] = {}
    
    for phone in phones:
        country = get_country(phone) or "UNKNOWN"
        if country not in grouped:
            grouped[country] = []
        grouped[country].append(phone)
    
    return grouped


def mask(phone: str, show_last: int = 4) -> Optional[str]:
    """
    Mask phone number for display (privacy protection).
    
    Args:
        phone: Phone number string
        show_last: Number of digits to show at the end
        
    Returns:
        Masked phone number or None if invalid
    """
    parsed = parse(phone)
    if not parsed:
        return None
    
    national = parsed.national_number
    if len(national) <= show_last:
        return parsed.international
    
    masked_part = "*" * (len(national) - show_last)
    visible_part = national[-show_last:]
    
    country_code = parsed.country_code
    if country_code:
        return f"{country_code} {masked_part}{visible_part}"
    return f"{masked_part}{visible_part}"
