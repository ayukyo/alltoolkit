"""
ISBN (International Standard Book Number) Utilities

Complete ISBN-10 and ISBN-13 utilities with zero external dependencies.
Supports validation, parsing, formatting, and conversion between formats.

ISBN-10: 10-digit format (used until 2007)
  - Format: X-XXXXX-XXX-X (group-publisher-title-check)
  - Check digit: 0-9 or X (Roman numeral 10)
  
ISBN-13: 13-digit format (current standard since 2007)
  - Format: XXX-X-XXXX-XXXX-X (prefix-group-publisher-title-check)
  - Prefix: 978 or 979 (GS1 prefix for Bookland)
  - Check digit: 0-9
"""

import re
from typing import Optional, Dict, List, Tuple


# ISBN-10 check digit weights
ISBN10_WEIGHTS = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]

# ISBN-13 check digit weights
ISBN13_WEIGHTS = [1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1]

# GS1 prefixes for ISBN-13
ISBN_PREFIXES = ['978', '979']


def clean(isbn: str) -> str:
    """
    Remove non-numeric characters from ISBN (preserves X check digit).
    
    Args:
        isbn: ISBN string (may contain hyphens, spaces, etc.)
    
    Returns:
        Cleaned ISBN string
    
    Example:
        >>> clean('978-0-306-40615-7')
        '9780306406157'
        >>> clean('0 306 40615 2')
        '0306406152'
    """
    # Keep only digits and X (for ISBN-10 check digit)
    return ''.join(c for c in isbn.upper() if c.isdigit() or c == 'X')


def validate(isbn: str) -> bool:
    """
    Validate an ISBN (accepts both ISBN-10 and ISBN-13).
    
    Args:
        isbn: ISBN string
    
    Returns:
        True if valid, False otherwise
    
    Example:
        >>> validate('978-0-306-40615-7')
        True
        >>> validate('0-306-40615-2')
        True
        >>> validate('invalid')
        False
    """
    cleaned = clean(isbn)
    
    if len(cleaned) == 10:
        return validate_isbn10(cleaned)
    elif len(cleaned) == 13:
        return validate_isbn13(cleaned)
    
    return False


def validate_isbn10(isbn: str) -> bool:
    """
    Validate an ISBN-10.
    
    Args:
        isbn: ISBN-10 string
    
    Returns:
        True if valid, False otherwise
    
    Example:
        >>> validate_isbn10('0306406152')
        True
        >>> validate_isbn10('030640615X')
        False
    """
    cleaned = clean(isbn)
    
    if len(cleaned) != 10:
        return False
    
    # Calculate check digit
    try:
        total = 0
        for i, char in enumerate(cleaned):
            if char == 'X':
                value = 10
            else:
                value = int(char)
            total += value * ISBN10_WEIGHTS[i]
        
        return total % 11 == 0
    except (ValueError, IndexError):
        return False


def validate_isbn13(isbn: str) -> bool:
    """
    Validate an ISBN-13.
    
    Args:
        isbn: ISBN-13 string
    
    Returns:
        True if valid, False otherwise
    
    Example:
        >>> validate_isbn13('9780306406157')
        True
        >>> validate_isbn13('9790306406156')
        True
    """
    cleaned = clean(isbn)
    
    if len(cleaned) != 13:
        return False
    
    # Calculate check digit
    try:
        total = sum(int(cleaned[i]) * ISBN13_WEIGHTS[i] for i in range(13))
        return total % 10 == 0
    except (ValueError, IndexError):
        return False


def calculate_check_digit_isbn10(isbn: str) -> str:
    """
    Calculate check digit for ISBN-10.
    
    Args:
        isbn: ISBN-10 string (9 digits, with or without check digit)
    
    Returns:
        Check digit (0-9 or X)
    
    Example:
        >>> calculate_check_digit_isbn10('030640615')
        '2'
        >>> calculate_check_digit_isbn10('080442957')
        'X'
    """
    cleaned = clean(isbn)[:9]
    
    if len(cleaned) != 9:
        raise ValueError("ISBN-10 requires 9 digits for check digit calculation")
    
    total = sum(int(cleaned[i]) * ISBN10_WEIGHTS[i] for i in range(9))
    remainder = total % 11
    check = (11 - remainder) % 11
    
    return 'X' if check == 10 else str(check)


def calculate_check_digit_isbn13(isbn: str) -> str:
    """
    Calculate check digit for ISBN-13.
    
    Args:
        isbn: ISBN-13 string (12 digits, with or without check digit)
    
    Returns:
        Check digit (0-9)
    
    Example:
        >>> calculate_check_digit_isbn13('978030640615')
        '7'
    """
    cleaned = clean(isbn)[:12]
    
    if len(cleaned) != 12:
        raise ValueError("ISBN-13 requires 12 digits for check digit calculation")
    
    total = sum(int(cleaned[i]) * ISBN13_WEIGHTS[i] for i in range(12))
    check = (10 - (total % 10)) % 10
    
    return str(check)


def isbn10_to_isbn13(isbn: str) -> str:
    """
    Convert ISBN-10 to ISBN-13.
    
    Args:
        isbn: ISBN-10 string
    
    Returns:
        ISBN-13 string
    
    Raises:
        ValueError: If ISBN-10 is invalid
    
    Example:
        >>> isbn10_to_isbn13('0306406152')
        '9780306406157'
    """
    cleaned = clean(isbn)
    
    if len(cleaned) != 10:
        raise ValueError("Invalid ISBN-10 length")
    
    if not validate_isbn10(cleaned):
        raise ValueError("Invalid ISBN-10 check digit")
    
    # Add 978 prefix and calculate new check digit
    isbn13_base = '978' + cleaned[:9]
    check_digit = calculate_check_digit_isbn13(isbn13_base)
    
    return isbn13_base + check_digit


def isbn13_to_isbn10(isbn: str) -> Optional[str]:
    """
    Convert ISBN-13 to ISBN-10.
    
    Only works for ISBN-13s with 978 prefix (legacy ISBN-10s).
    ISBN-13s with 979 prefix cannot be converted to ISBN-10.
    
    Args:
        isbn: ISBN-13 string
    
    Returns:
        ISBN-10 string, or None if not convertible
    
    Example:
        >>> isbn13_to_isbn10('9780306406157')
        '0306406152'
        >>> isbn13_to_isbn10('9790306406156')
        None
    """
    cleaned = clean(isbn)
    
    if len(cleaned) != 13:
        raise ValueError("Invalid ISBN-13 length")
    
    if not validate_isbn13(cleaned):
        raise ValueError("Invalid ISBN-13 check digit")
    
    # Check if convertible (must have 978 prefix)
    if not cleaned.startswith('978'):
        return None
    
    # Remove 978 prefix and calculate new check digit
    isbn10_base = cleaned[3:12]
    check_digit = calculate_check_digit_isbn10(isbn10_base)
    
    return isbn10_base + check_digit


def parse(isbn: str) -> Dict[str, any]:
    """
    Parse an ISBN and extract all components.
    
    Args:
        isbn: ISBN string (ISBN-10 or ISBN-13)
    
    Returns:
        Dictionary with parsed components
    
    Example:
        >>> parse('978-0-306-40615-7')
        {'valid': True, 'type': 'ISBN-13', 'prefix': '978', ...}
    """
    cleaned = clean(isbn)
    
    result = {
        'original': isbn.strip(),
        'cleaned': cleaned,
        'valid': False,
        'type': None,
        'prefix': None,
        'group': None,
        'publisher': None,
        'title': None,
        'check_digit': None,
        'isbn10': None,
        'isbn13': None
    }
    
    if len(cleaned) == 10:
        result['type'] = 'ISBN-10'
        result['valid'] = validate_isbn10(cleaned)
        
        if result['valid']:
            result['check_digit'] = cleaned[9]
            result['isbn10'] = cleaned
            result['isbn13'] = isbn10_to_isbn13(cleaned)
            
    elif len(cleaned) == 13:
        result['type'] = 'ISBN-13'
        result['valid'] = validate_isbn13(cleaned)
        
        if result['valid']:
            result['prefix'] = cleaned[:3]
            result['check_digit'] = cleaned[12]
            result['isbn13'] = cleaned
            result['isbn10'] = isbn13_to_isbn10(cleaned)
    else:
        return result
    
    return result


def format(isbn: str, style: str = "hyphenated") -> str:
    """
    Format an ISBN string.
    
    Args:
        isbn: ISBN string
        style: Formatting style
            - 'clean': Just digits (and X)
            - 'hyphenated': With hyphens (X-XXXXX-XXX-X or XXX-X-XXXX-XXXX-X)
            - 'spaced': With spaces
            - 'both': With hyphens and spaces
    
    Returns:
        Formatted ISBN string
    
    Example:
        >>> format('0306406152', 'hyphenated')
        '0-306-40615-2'
        >>> format('9780306406157', 'hyphenated')
        '978-0-306-40615-7'
    """
    cleaned = clean(isbn)
    
    if style == "clean":
        return cleaned
    
    if len(cleaned) == 10:
        # ISBN-10 format: X-XXXXX-XXX-X
        if style == "hyphenated":
            return f"{cleaned[0]}-{cleaned[1:6]}-{cleaned[6:9]}-{cleaned[9]}"
        elif style == "spaced":
            return f"{cleaned[0]} {cleaned[1:6]} {cleaned[6:9]} {cleaned[9]}"
        elif style == "both":
            return f"{cleaned[0]}- {cleaned[1:6]} - {cleaned[6:9]} - {cleaned[9]}"
    
    elif len(cleaned) == 13:
        # ISBN-13 format: XXX-X-XXXX-XXXX-X
        if style == "hyphenated":
            return f"{cleaned[:3]}-{cleaned[3]}-{cleaned[4:8]}-{cleaned[8:12]}-{cleaned[12]}"
        elif style == "spaced":
            return f"{cleaned[:3]} {cleaned[3]} {cleaned[4:8]} {cleaned[8:12]} {cleaned[12]}"
        elif style == "both":
            return f"{cleaned[:3]}- {cleaned[3]} - {cleaned[4:8]} - {cleaned[8:12]} - {cleaned[12]}"
    
    return cleaned


def get_type(isbn: str) -> Optional[str]:
    """
    Get the type of an ISBN.
    
    Args:
        isbn: ISBN string
    
    Returns:
        'ISBN-10', 'ISBN-13', or None if invalid
    
    Example:
        >>> get_type('0306406152')
        'ISBN-10'
        >>> get_type('9780306406157')
        'ISBN-13'
    """
    cleaned = clean(isbn)
    
    if len(cleaned) == 10:
        return 'ISBN-10' if validate_isbn10(cleaned) else None
    elif len(cleaned) == 13:
        return 'ISBN-13' if validate_isbn13(cleaned) else None
    
    return None


def is_isbn10(isbn: str) -> bool:
    """
    Check if an ISBN is a valid ISBN-10.
    
    Args:
        isbn: ISBN string
    
    Returns:
        True if valid ISBN-10
    
    Example:
        >>> is_isbn10('0306406152')
        True
    """
    cleaned = clean(isbn)
    return len(cleaned) == 10 and validate_isbn10(cleaned)


def is_isbn13(isbn: str) -> bool:
    """
    Check if an ISBN is a valid ISBN-13.
    
    Args:
        isbn: ISBN string
    
    Returns:
        True if valid ISBN-13
    
    Example:
        >>> is_isbn13('9780306406157')
        True
    """
    cleaned = clean(isbn)
    return len(cleaned) == 13 and validate_isbn13(cleaned)


def generate_isbn13(prefix: str = '978', group: str = '0', 
                    publisher: str = None, title: str = None) -> str:
    """
    Generate a valid ISBN-13 with random or specified components.
    
    Note: This generates syntactically valid ISBNs for testing purposes only.
    Real ISBNs must be registered with the ISBN Agency.
    
    Args:
        prefix: GS1 prefix (978 or 979)
        group: Group identifier (language/country)
        publisher: Publisher code (random if None)
        title: Title code (random if None)
    
    Returns:
        Valid ISBN-13 string
    
    Example:
        >>> isbn = generate_isbn13()
        >>> validate(isbn)
        True
    """
    if prefix not in ISBN_PREFIXES:
        raise ValueError(f"Prefix must be '978' or '979', got '{prefix}'")
    
    # Generate random publisher and title codes if not provided
    if publisher is None:
        publisher = ''.join(str(__import__('random').randint(0, 9)) for _ in range(4))
    
    if title is None:
        title = ''.join(str(__import__('random').randint(0, 9)) for _ in range(4))
    
    # Build ISBN-13 base (12 digits)
    base = prefix + group + publisher + title
    
    # Pad or truncate to 12 digits
    if len(base) < 12:
        base = base + '0' * (12 - len(base))
    else:
        base = base[:12]
    
    # Calculate check digit
    check_digit = calculate_check_digit_isbn13(base)
    
    return base + check_digit


def generate_isbn10(group: str = '0', publisher: str = None, title: str = None) -> str:
    """
    Generate a valid ISBN-10 with random or specified components.
    
    Note: This generates syntactically valid ISBNs for testing purposes only.
    Real ISBNs must be registered with the ISBN Agency.
    
    Args:
        group: Group identifier (language/country)
        publisher: Publisher code (random if None)
        title: Title code (random if None)
    
    Returns:
        Valid ISBN-10 string
    
    Example:
        >>> isbn = generate_isbn10()
        >>> validate(isbn)
        True
    """
    # Generate random publisher and title codes if not provided
    if publisher is None:
        publisher = ''.join(str(__import__('random').randint(0, 9)) for _ in range(4))
    
    if title is None:
        title = ''.join(str(__import__('random').randint(0, 9)) for _ in range(3))
    
    # Build ISBN-10 base (9 digits)
    base = group + publisher + title
    
    # Pad or truncate to 9 digits
    if len(base) < 9:
        base = base + '0' * (9 - len(base))
    else:
        base = base[:9]
    
    # Calculate check digit
    check_digit = calculate_check_digit_isbn10(base)
    
    return base + check_digit


def batch_validate(isbns: List[str]) -> Dict[str, any]:
    """
    Validate multiple ISBNs at once.
    
    Args:
        isbns: List of ISBN strings
    
    Returns:
        Dictionary with validation results
    
    Example:
        >>> result = batch_validate(['0306406152', '9780306406157', 'invalid'])
        >>> result['valid_count']
        2
    """
    results = {
        'valid_count': 0,
        'invalid_count': 0,
        'isbn10_count': 0,
        'isbn13_count': 0,
        'details': []
    }
    
    for isbn in isbns:
        parsed = parse(isbn)
        
        detail = {
            'original': isbn.strip(),
            'cleaned': parsed['cleaned'],
            'valid': parsed['valid'],
            'type': parsed['type'],
            'isbn10': parsed['isbn10'],
            'isbn13': parsed['isbn13']
        }
        
        results['details'].append(detail)
        
        if parsed['valid']:
            results['valid_count'] += 1
            if parsed['type'] == 'ISBN-10':
                results['isbn10_count'] += 1
            else:
                results['isbn13_count'] += 1
        else:
            results['invalid_count'] += 1
    
    results['total'] = len(isbns)
    
    return results


def normalize(isbn: str, target: str = "isbn13") -> Optional[str]:
    """
    Normalize an ISBN to a specific format.
    
    Args:
        isbn: ISBN string
        target: Target format ('isbn10', 'isbn13', or 'clean')
    
    Returns:
        Normalized ISBN string, or None if not possible
    
    Example:
        >>> normalize('0306406152', 'isbn13')
        '9780306406157'
        >>> normalize('9780306406157', 'isbn10')
        '0306406152'
    """
    parsed = parse(isbn)
    
    if not parsed['valid']:
        return None
    
    if target == 'clean':
        return parsed['cleaned']
    elif target == 'isbn13':
        return parsed['isbn13']
    elif target == 'isbn10':
        return parsed['isbn10']
    
    return None


def find_isbns(text: str) -> List[str]:
    """
    Find all ISBNs in a text string.
    
    Args:
        text: Text to search for ISBNs
    
    Returns:
        List of valid ISBNs found
    
    Example:
        >>> find_isbns('Book ISBN: 978-0-306-40615-7 and 0-306-40615-2')
        ['978-0-306-40615-7', '0-306-40615-2']
    """
    # Match patterns that look like ISBNs with hyphens
    # Flexible pattern that captures most ISBN formats
    pattern = r'\d[\d\-\s]{8,15}[\dXx]'
    
    potential_isbns = re.findall(pattern, text)
    
    # Validate each potential ISBN
    valid_isbns = []
    for potential in potential_isbns:
        # Clean and check length
        cleaned = clean(potential)
        # If cleaned version is valid, use it
        if len(cleaned) == 10 and validate_isbn10(cleaned):
            valid_isbns.append(potential.strip())
        elif len(cleaned) == 13 and validate_isbn13(cleaned):
            valid_isbns.append(potential.strip())
        # For partially matched ISBNs, try extending
        elif len(cleaned) < 10:
            # Try to find continuation in text
            idx = text.find(potential)
            if idx >= 0:
                end_idx = idx + len(potential)
                # Try extending by a few characters
                for ext_len in range(1, 5):
                    extended = text[idx:end_idx + ext_len]
                    ext_cleaned = clean(extended)
                    if len(ext_cleaned) == 10 and validate_isbn10(ext_cleaned):
                        valid_isbns.append(extended.strip())
                        break
                    elif len(ext_cleaned) == 13 and validate_isbn13(ext_cleaned):
                        valid_isbns.append(extended.strip())
                        break
    
    return valid_isbns


def compare(isbn1: str, isbn2: str) -> Dict[str, any]:
    """
    Compare two ISBNs.
    
    Args:
        isbn1: First ISBN
        isbn2: Second ISBN
    
    Returns:
        Dictionary with comparison results
    
    Example:
        >>> compare('0306406152', '9780306406157')
        {'same_book': True, 'isbn1_type': 'ISBN-10', ...}
    """
    parsed1 = parse(isbn1)
    parsed2 = parse(isbn2)
    
    result = {
        'isbn1_valid': parsed1['valid'],
        'isbn2_valid': parsed2['valid'],
        'isbn1_type': parsed1['type'],
        'isbn2_type': parsed2['type'],
        'same_book': False,
        'same_isbn': False
    }
    
    if not parsed1['valid'] or not parsed2['valid']:
        return result
    
    # Check if they represent the same book (same ISBN-13)
    if parsed1['isbn13'] and parsed2['isbn13']:
        result['same_book'] = parsed1['isbn13'] == parsed2['isbn13']
    
    # Check if they're exactly the same ISBN
    result['same_isbn'] = parsed1['cleaned'] == parsed2['cleaned']
    
    result['isbn1_isbn10'] = parsed1['isbn10']
    result['isbn1_isbn13'] = parsed1['isbn13']
    result['isbn2_isbn10'] = parsed2['isbn10']
    result['isbn2_isbn13'] = parsed2['isbn13']
    
    return result


def get_group_name(group_code: str) -> Optional[str]:
    """
    Get the group name for a group code.
    
    This is a simplified mapping for common groups.
    For complete data, use the official ISBN Range File.
    
    Args:
        group_code: Group identifier (single digit or code)
    
    Returns:
        Group name or None
    
    Example:
        >>> get_group_name('0')
        'English'
        >>> get_group_name('7')
        'China'
    """
    # Simplified group mapping (common groups)
    groups = {
        '0': 'English (UK/US)',
        '1': 'English (UK/US)',
        '2': 'French',
        '3': 'German',
        '4': 'Japanese',
        '5': 'Russian',
        '7': 'China',
        '80': 'Czech Republic',
        '82': 'Norwegian',
        '83': 'Polish',
        '84': 'Spanish',
        '85': 'Brazilian Portuguese',
        '87': 'Danish',
        '88': 'Italian',
        '89': 'Korean',
        '90': 'Dutch',
        '91': 'Swedish',
        '92': 'International',
        '93': 'India',
        '94': 'Dutch (Netherlands)',
        '952': 'Finnish',
        '977': 'Egypt',
        '978': 'ISBN-13 Prefix',
        '979': 'ISBN-13 Prefix',
    }
    
    # Try exact match first
    if group_code in groups:
        return groups[group_code]
    
    # Try prefix match for multi-digit codes
    for code, name in sorted(groups.items(), key=lambda x: -len(x[0])):
        if group_code.startswith(code):
            return name
    
    return None


def analyze(isbn: str) -> Dict[str, any]:
    """
    Perform comprehensive analysis of an ISBN.
    
    Args:
        isbn: ISBN string
    
    Returns:
        Dictionary with full analysis
    
    Example:
        >>> analyze('978-0-306-40615-7')
        {'valid': True, 'type': 'ISBN-13', ...}
    """
    parsed = parse(isbn)
    
    result = {
        'valid': parsed['valid'],
        'original': parsed['original'],
        'cleaned': parsed['cleaned'],
        'type': parsed['type'],
        'check_digit': parsed['check_digit'],
        'isbn10': parsed['isbn10'],
        'isbn13': parsed['isbn13'],
        'formats': {},
        'group': None,
        'group_name': None
    }
    
    if parsed['valid']:
        # Generate all formats
        result['formats'] = {
            'clean': format(isbn, 'clean'),
            'hyphenated': format(isbn, 'hyphenated'),
            'spaced': format(isbn, 'spaced')
        }
        
        # Extract group code (simplified)
        cleaned = parsed['cleaned']
        if parsed['type'] == 'ISBN-10':
            group_code = cleaned[0]
        else:
            group_code = cleaned[3]  # Skip prefix
        
        result['group'] = group_code
        result['group_name'] = get_group_name(group_code)
    
    return result


def repair(isbn: str) -> Optional[str]:
    """
    Attempt to repair a malformed ISBN.
    
    Common fixes:
    - Remove extra characters
    - Fix transposed check digit
    - Add missing check digit
    
    Args:
        isbn: Possibly malformed ISBN string
    
    Returns:
        Repaired ISBN, or None if unrepairable
    
    Example:
        >>> repair('030640615')  # Missing check digit
        '0306406152'
    """
    cleaned = clean(isbn)
    
    # Already valid
    if len(cleaned) in [10, 13] and validate(cleaned):
        return cleaned
    
    # Missing check digit
    if len(cleaned) == 9:
        # Try to add ISBN-10 check digit
        try:
            check = calculate_check_digit_isbn10(cleaned)
            return cleaned + check
        except ValueError:
            pass
    
    if len(cleaned) == 12:
        # Try to add ISBN-13 check digit
        try:
            check = calculate_check_digit_isbn13(cleaned)
            return cleaned + check
        except ValueError:
            pass
    
    # Extra digit at end (try removing and recalculating)
    if len(cleaned) == 11:
        # Could be ISBN-10 with extra digit
        try:
            base = cleaned[:9]
            check = calculate_check_digit_isbn10(base)
            candidate = base + check
            if validate_isbn10(candidate):
                return candidate
        except ValueError:
            pass
    
    if len(cleaned) == 14:
        # Could be ISBN-13 with extra digit
        try:
            base = cleaned[:12]
            check = calculate_check_digit_isbn13(base)
            candidate = base + check
            if validate_isbn13(candidate):
                return candidate
        except ValueError:
            pass
    
    return None