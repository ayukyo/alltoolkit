"""
Unicode Character Lookup Utilities

A comprehensive Unicode character lookup and analysis toolkit.
Provides functions for:
- Character name lookup by code point or character
- Search characters by name keywords
- Character property analysis (category, script, block)
- Character encoding information (UTF-8, UTF-16, HTML entity)
- String Unicode analysis and statistics
- Character category detection (letters, digits, symbols, etc.)
- Unicode block information

Features:
- Zero external dependencies (pure Python stdlib)
- Comprehensive Unicode data coverage
- Efficient search algorithms
- Multi-language support

Reference: https://unicode.org/
"""

import unicodedata
import re
from typing import Optional, List, Dict, Set, Tuple, Union, Callable
from dataclasses import dataclass
from enum import Enum


# Unicode category constants
class UnicodeCategory(Enum):
    """Unicode general category codes."""
    # Letters
    LC = "Lc"  # Letter, capitalized (not in Unicode standard)
    LU = "Lu"  # Letter, uppercase
    LL = "Ll"  # Letter, lowercase
    LT = "Lt"  # Letter, titlecase
    LM = "Lm"  # Letter, modifier
    LO = "Lo"  # Letter, other
    
    # Marks
    MN = "Mn"  # Mark, nonspacing
    MC = "Mc"  # Mark, spacing combining
    ME = "Me"  # Mark, enclosing
    
    # Numbers
    ND = "Nd"  # Number, decimal digit
    NL = "Nl"  # Number, letter
    NO = "No"  # Number, other
    
    # Punctuation
    PC = "Pc"  # Punctuation, connector
    PD = "Pd"  # Punctuation, dash
    PS = "Ps"  # Punctuation, open
    PE = "Pe"  # Punctuation, close
    PI = "Pi"  # Punctuation, initial quote
    PF = "Pf"  # Punctuation, final quote
    PO = "Po"  # Punctuation, other
    
    # Symbols
    SM = "Sm"  # Symbol, math
    SC = "Sc"  # Symbol, currency
    SK = "Sk"  # Symbol, modifier
    SO = "So"  # Symbol, other
    
    # Separators
    ZS = "Zs"  # Separator, space
    ZL = "Zl"  # Separator, line
    ZP = "Zp"  # Separator, paragraph
    
    # Other
    CN = "Cn"  # Other, not assigned
    CC = "Cc"  # Other, control
    CF = "Cf"  # Other, format
    CS = "Cs"  # Other, surrogate
    CO = "Co"  # Other, private use


# Unicode block ranges (major blocks)
UNICODE_BLOCKS: Dict[str, Tuple[int, int]] = {
    "Basic Latin": (0x0000, 0x007F),
    "Latin-1 Supplement": (0x0080, 0x00FF),
    "Latin Extended-A": (0x0100, 0x017F),
    "Latin Extended-B": (0x0180, 0x024F),
    "IPA Extensions": (0x0250, 0x02AF),
    "Spacing Modifier Letters": (0x02B0, 0x02FF),
    "Greek and Coptic": (0x0370, 0x03FF),
    "Cyrillic": (0x0400, 0x04FF),
    "Cyrillic Supplement": (0x0500, 0x052F),
    "Armenian": (0x0530, 0x058F),
    "Hebrew": (0x0590, 0x05FF),
    "Arabic": (0x0600, 0x06FF),
    "Syriac": (0x0700, 0x074F),
    "Thaana": (0x0780, 0x07BF),
    "Devanagari": (0x0900, 0x097F),
    "Bengali": (0x0980, 0x09FF),
    "Gurmukhi": (0x0A00, 0x0A7F),
    "Gujarati": (0x0A80, 0x0AFF),
    "Oriya": (0x0B00, 0x0B7F),
    "Tamil": (0x0B80, 0x0BFF),
    "Telugu": (0x0C00, 0x0C7F),
    "Kannada": (0x0C80, 0x0CFF),
    "Malayalam": (0x0D00, 0x0D7F),
    "Sinhala": (0x0D80, 0x0DFF),
    "Thai": (0x0E00, 0x0E7F),
    "Lao": (0x0E80, 0x0EFF),
    "Tibetan": (0x0F00, 0x0FFF),
    "Georgian": (0x10A0, 0x10FF),
    "Hangul Jamo": (0x1100, 0x11FF),
    "Ethiopic": (0x1200, 0x137F),
    "Cherokee": (0x13A0, 0x13FF),
    "Unified Canadian Aboriginal Syllabics": (0x1400, 0x167F),
    "Ogham": (0x1680, 0x169F),
    "Runic": (0x16A0, 0x16FF),
    "Khmer": (0x1780, 0x17FF),
    "Mongolian": (0x1800, 0x18AF),
    "Latin Extended Additional": (0x1E00, 0x1EFF),
    "Greek Extended": (0x1F00, 0x1FFF),
    "General Punctuation": (0x2000, 0x206F),
    "Superscripts and Subscripts": (0x2070, 0x209F),
    "Currency Symbols": (0x20A0, 0x20CF),
    "Combining Diacritical Marks for Symbols": (0x20D0, 0x20FF),
    "Letterlike Symbols": (0x2100, 0x214F),
    "Number Forms": (0x2150, 0x218F),
    "Arrows": (0x2190, 0x21FF),
    "Mathematical Operators": (0x2200, 0x22FF),
    "Miscellaneous Technical": (0x2300, 0x23FF),
    "Control Pictures": (0x2400, 0x243F),
    "Optical Character Recognition": (0x2440, 0x245F),
    "Enclosed Alphanumerics": (0x2460, 0x24FF),
    "Box Drawing": (0x2500, 0x257F),
    "Block Elements": (0x2580, 0x259F),
    "Geometric Shapes": (0x25A0, 0x25FF),
    "Miscellaneous Symbols": (0x2600, 0x26FF),
    "Dingbats": (0x2700, 0x27BF),
    "Braille Patterns": (0x2800, 0x28FF),
    "CJK Radicals Supplement": (0x2E80, 0x2EFF),
    "Kangxi Radicals": (0x2F00, 0x2FDF),
    "Ideographic Description Characters": (0x2FF0, 0x2FFF),
    "CJK Symbols and Punctuation": (0x3000, 0x303F),
    "Hiragana": (0x3040, 0x309F),
    "Katakana": (0x30A0, 0x30FF),
    "Bopomofo": (0x3100, 0x312F),
    "Hangul Compatibility Jamo": (0x3130, 0x318F),
    "Bopomofo Extended": (0x31A0, 0x31BF),
    "CJK Unified Ideographs Extension A": (0x3400, 0x4DBF),
    "CJK Unified Ideographs": (0x4E00, 0x9FFF),
    "Yi Syllables": (0xA000, 0xA48F),
    "Yi Radicals": (0xA490, 0xA4CF),
    "Hangul Syllables": (0xAC00, 0xD7AF),
    "Private Use Area": (0xE000, 0xF8FF),
    "CJK Compatibility Ideographs": (0xF900, 0xFAFF),
    "Alphabetic Presentation Forms": (0xFB00, 0xFB4F),
    "Arabic Presentation Forms-A": (0xFB50, 0xFDFF),
    "Variation Selectors": (0xFE00, 0xFE0F),
    "Combining Half Marks": (0xFE20, 0xFE2F),
    "CJK Compatibility Forms": (0xFE30, 0xFE4F),
    "Small Form Variants": (0xFE50, 0xFE6F),
    "Arabic Presentation Forms-B": (0xFE70, 0xFEFF),
    "Halfwidth and Fullwidth Forms": (0xFF00, 0xFFEF),
    "Specials": (0xFFF0, 0xFFFF),
    "Linear B Syllabary": (0x10000, 0x1007F),
    "Linear B Ideograms": (0x10080, 0x100FF),
    "Aegean Numbers": (0x10100, 0x1013F),
    "Ancient Greek Numbers": (0x10140, 0x1018F),
    "Ancient Symbols": (0x10190, 0x101CF),
    "Phaistos Disc": (0x101D0, 0x101FF),
    "Lycian": (0x10280, 0x1029F),
    "Carian": (0x102A0, 0x102DF),
    "Old Italic": (0x10300, 0x1032F),
    "Gothic": (0x10330, 0x1034F),
    "Ugaritic": (0x10380, 0x1039F),
    "Old Persian": (0x103A0, 0x103DF),
    "Deseret": (0x10400, 0x1044F),
    "Shavian": (0x10450, 0x1047F),
    "Osmanya": (0x10480, 0x104AF),
    "Cypriot Syllabary": (0x10800, 0x1083F),
    "Kharoshthi": (0x10A00, 0x10A5F),
    "Tai Le": (0x1950, 0x197F),
    "New Tai Lue": (0x1980, 0x19DF),
    "Buginese": (0x1A00, 0x1A1F),
    "Glagolitic": (0x2C00, 0x2C5F),
    "Tifinagh": (0x2D30, 0x2D7F),
    "Ethiopic Extended": (0x2D80, 0x2DDF),
    "Supplementary Private Use Area-A": (0xF0000, 0xFFFFD),
    "Supplementary Private Use Area-B": (0x100000, 0x10FFFD),
}


@dataclass
class UnicodeCharInfo:
    """Detailed information about a Unicode character."""
    char: str
    code_point: int
    name: str
    category: str
    category_name: str
    block: str
    script: str
    combining: int
    bidirectional: str
    mirrored: str
    decimal_value: Optional[int]
    digit_value: Optional[int]
    numeric_value: Optional[float]
    uppercase: Optional[str]
    lowercase: Optional[str]
    titlecase: Optional[str]
    width: str
    utf8_bytes: bytes
    utf8_hex: str
    utf16_bytes: bytes
    utf16_hex: str
    html_entity_decimal: str
    html_entity_hex: str
    html_entity_named: Optional[str]
    is_printable: bool
    is_whitespace: bool
    is_control: bool
    is_letter: bool
    is_digit: bool
    is_numeric: bool
    is_punctuation: bool
    is_symbol: bool
    is_mark: bool
    is_currency: bool
    is_math: bool
    is_emoji: bool


def get_char_name(char: str) -> str:
    """
    Get the official Unicode name for a character.
    
    Args:
        char: Single character
    
    Returns:
        Unicode character name
    
    Raises:
        ValueError: If not a single character
    
    Example:
        >>> get_char_name('A')
        'LATIN CAPITAL LETTER A'
        >>> get_char_name('中')
        'CJK UNIFIED IDEOGRAPH-4E2D'
    """
    if len(char) != 1:
        raise ValueError(f"Expected single character, got {len(char)} characters")
    
    try:
        return unicodedata.name(char)
    except ValueError:
        # Handle characters without official names
        return f"<no name> U+{ord(char):04X}"


def get_char_by_name(name: str) -> Optional[str]:
    """
    Get a character by its Unicode name.
    
    Args:
        name: Unicode character name
    
    Returns:
        Character if found, None otherwise
    
    Example:
        >>> get_char_by_name('LATIN CAPITAL LETTER A')
        'A'
        >>> get_char_by_name('SNOWMAN')
        '☃'
    """
    try:
        return unicodedata.lookup(name)
    except KeyError:
        return None


def get_code_point(char: str) -> int:
    """
    Get the Unicode code point for a character.
    
    Args:
        char: Character
    
    Returns:
        Integer code point
    
    Example:
        >>> get_code_point('A')
        65
        >>> get_code_point('中')
        20013
    """
    return ord(char)


def get_char_by_code_point(code_point: int) -> str:
    """
    Get character by Unicode code point.
    
    Args:
        code_point: Integer code point
    
    Returns:
        Character
    
    Raises:
        ValueError: If code point is invalid
    
    Example:
        >>> get_char_by_code_point(65)
        'A'
        >>> get_char_by_code_point(20013)
        '中'
    """
    if code_point < 0 or code_point > 0x10FFFF:
        raise ValueError(f"Invalid code point: {code_point}")
    
    return chr(code_point)


def get_category(char: str) -> str:
    """
    Get the Unicode general category for a character.
    
    Args:
        char: Character
    
    Returns:
        Two-letter category code
    
    Example:
        >>> get_category('A')
        'Lu'  # Letter, uppercase
        >>> get_category('5')
        'Nd'  # Number, decimal digit
        >>> get_category(' ')
        'Zs'  # Separator, space
    """
    return unicodedata.category(char)


def get_category_name(category_code: str) -> str:
    """
    Get human-readable name for a Unicode category.
    
    Args:
        category_code: Two-letter category code
    
    Returns:
        Category name
    
    Example:
        >>> get_category_name('Lu')
        'Letter, uppercase'
        >>> get_category_name('Nd')
        'Number, decimal digit'
    """
    category_names = {
        'Lu': 'Letter, uppercase',
        'Ll': 'Letter, lowercase',
        'Lt': 'Letter, titlecase',
        'Lm': 'Letter, modifier',
        'Lo': 'Letter, other',
        'Mn': 'Mark, nonspacing',
        'Mc': 'Mark, spacing combining',
        'Me': 'Mark, enclosing',
        'Nd': 'Number, decimal digit',
        'Nl': 'Number, letter',
        'No': 'Number, other',
        'Pc': 'Punctuation, connector',
        'Pd': 'Punctuation, dash',
        'Ps': 'Punctuation, open',
        'Pe': 'Punctuation, close',
        'Pi': 'Punctuation, initial quote',
        'Pf': 'Punctuation, final quote',
        'Po': 'Punctuation, other',
        'Sm': 'Symbol, math',
        'Sc': 'Symbol, currency',
        'Sk': 'Symbol, modifier',
        'So': 'Symbol, other',
        'Zs': 'Separator, space',
        'Zl': 'Separator, line',
        'Zp': 'Separator, paragraph',
        'Cn': 'Other, not assigned',
        'Cc': 'Other, control',
        'Cf': 'Other, format',
        'Cs': 'Other, surrogate',
        'Co': 'Other, private use',
    }
    return category_names.get(category_code, f'Unknown category: {category_code}')


def get_block(char: str) -> str:
    """
    Get the Unicode block name for a character.
    
    Args:
        char: Character
    
    Returns:
        Block name
    
    Example:
        >>> get_block('A')
        'Basic Latin'
        >>> get_block('中')
        'CJK Unified Ideographs'
        >>> get_block('☃')
        'Miscellaneous Symbols'
    """
    code_point = ord(char)
    
    for block_name, (start, end) in UNICODE_BLOCKS.items():
        if start <= code_point <= end:
            return block_name
    
    return "Unknown Block"


def get_block_by_name(block_name: str) -> Optional[Tuple[int, int]]:
    """
    Get the code point range for a Unicode block.
    
    Args:
        block_name: Block name
    
    Returns:
        Tuple of (start, end) code points, or None
    
    Example:
        >>> get_block_by_name('Basic Latin')
        (0, 127)
    """
    return UNICODE_BLOCKS.get(block_name)


def list_block_characters(block_name: str, limit: Optional[int] = None) -> List[str]:
    """
    List characters in a Unicode block.
    
    Args:
        block_name: Block name
        limit: Maximum number of characters to return
    
    Returns:
        List of characters (skips control characters)
    
    Example:
        >>> chars = list_block_characters('Basic Latin', limit=10)
        >>> len(chars)
        10
        >>> 'A' in chars
        True
    """
    range_info = UNICODE_BLOCKS.get(block_name)
    if range_info is None:
        return []
    
    start, end = range_info
    chars = []
    
    for cp in range(start, end + 1):
        try:
            char = chr(cp)
            category = unicodedata.category(char)
            # Skip surrogates, unassigned, and control characters
            if category not in ('Cs', 'Cn', 'Cc'):
                chars.append(char)
        except ValueError:
            pass
        
        if limit and len(chars) >= limit:
            break
    
    return chars


def search_by_name(keyword: str, limit: int = 50) -> List[Dict[str, any]]:
    """
    Search for characters by name keyword.
    
    Args:
        keyword: Search keyword
        limit: Maximum results to return
    
    Returns:
        List of character info dictionaries
    
    Example:
        >>> results = search_by_name('snowman')
        >>> len(results)
        1
        >>> results[0]['char']
        '☃'
    """
    keyword = keyword.upper()
    results = []
    
    # Search in common Unicode ranges
    search_ranges = [
        (0x0000, 0xFFFF),       # BMP (Basic Multilingual Plane)
        (0x1F300, 0x1F9FF),     # Emoji range
        (0x2600, 0x27BF),       # Miscellaneous Symbols + Dingbats
    ]
    
    for start, end in search_ranges:
        for cp in range(start, end + 1):
            try:
                char = chr(cp)
                name = unicodedata.name(char, '')
                
                if keyword in name.upper():
                    results.append({
                        'char': char,
                        'code_point': cp,
                        'name': name,
                        'category': unicodedata.category(char),
                    })
                    
                    if len(results) >= limit:
                        return results
            except ValueError:
                pass
    
    return results


def search_by_category(category: str) -> List[str]:
    """
    Get all characters in a specific Unicode category.
    
    Args:
        category: Two-letter category code
    
    Returns:
        List of characters
    
    Note:
        This searches through common ranges, not all Unicode.
    
    Example:
        >>> chars = search_by_category('Sc')  # Currency symbols
        >>> '$' in chars
        True
    """
    chars = []
    
    # Search common ranges
    for cp in range(0x0000, 0xFFFF):
        try:
            char = chr(cp)
            if unicodedata.category(char) == category:
                chars.append(char)
        except ValueError:
            pass
    
    return chars


def get_full_info(char: str) -> UnicodeCharInfo:
    """
    Get comprehensive information about a character.
    
    Args:
        char: Single character
    
    Returns:
        UnicodeCharInfo dataclass with all properties
    
    Example:
        >>> info = get_full_info('A')
        >>> info.name
        'LATIN CAPITAL LETTER A'
        >>> info.category
        'Lu'
        >>> info.html_entity_decimal
        '&#65;'
    """
    if len(char) != 1:
        raise ValueError(f"Expected single character, got {len(char)} characters")
    
    code_point = ord(char)
    
    # Get basic properties
    try:
        name = unicodedata.name(char)
    except ValueError:
        name = f"<no name> U+{code_point:04X}"
    
    category = unicodedata.category(char)
    category_name = get_category_name(category)
    
    # Numeric properties
    decimal_value = None
    digit_value = None
    numeric_value = None
    
    try:
        decimal_value = unicodedata.decimal(char)
    except ValueError:
        pass
    
    try:
        digit_value = unicodedata.digit(char)
    except ValueError:
        pass
    
    try:
        numeric_value = unicodedata.numeric(char)
    except ValueError:
        pass
    
    # Case mappings (using string methods, not unicodedata)
    uppercase = None
    lowercase = None
    titlecase = None
    
    # Get uppercase if different from current
    upper_char = char.upper()
    if upper_char != char:
        uppercase = upper_char
    
    # Get lowercase if different from current
    lower_char = char.lower()
    if lower_char != char:
        lowercase = lower_char
    
    # Get titlecase if different from current
    # Note: Python's str.title() works on strings, not single chars
    # For single chars, titlecase is usually same as uppercase
    title_char = char.upper()  # Approximate titlecase as uppercase
    if title_char != char and char.islower():
        titlecase = title_char
    
    # Width estimation
    width = get_char_width(char)
    
    # Encoding info
    utf8_bytes = char.encode('utf-8')
    utf8_hex = ' '.join(f'{b:02X}' for b in utf8_bytes)
    
    utf16_bytes = char.encode('utf-16-be')
    utf16_hex = ' '.join(f'{b:02X}' for b in utf16_bytes)
    
    # HTML entities
    html_entity_decimal = f"&#{code_point};"
    html_entity_hex = f"&#x{code_point:04X};"
    html_entity_named = get_html_entity_named(char)
    
    # Character type checks
    is_printable = is_char_printable(char)
    is_whitespace = is_char_whitespace(char)
    is_control = is_char_control(char)
    is_letter = is_char_letter(char)
    is_digit = is_char_digit(char)
    is_numeric = is_char_numeric(char)
    is_punctuation = is_char_punctuation(char)
    is_symbol = is_char_symbol(char)
    is_mark = is_char_mark(char)
    is_currency = is_char_currency(char)
    is_math = is_char_math(char)
    is_emoji = is_char_emoji(char)
    
    return UnicodeCharInfo(
        char=char,
        code_point=code_point,
        name=name,
        category=category,
        category_name=category_name,
        block=get_block(char),
        script=get_script(char),
        combining=unicodedata.combining(char),
        bidirectional=unicodedata.bidirectional(char),
        mirrored=unicodedata.mirrored(char),
        decimal_value=decimal_value,
        digit_value=digit_value,
        numeric_value=numeric_value,
        uppercase=uppercase,
        lowercase=lowercase,
        titlecase=titlecase,
        width=width,
        utf8_bytes=utf8_bytes,
        utf8_hex=utf8_hex,
        utf16_bytes=utf16_bytes,
        utf16_hex=utf16_hex,
        html_entity_decimal=html_entity_decimal,
        html_entity_hex=html_entity_hex,
        html_entity_named=html_entity_named,
        is_printable=is_printable,
        is_whitespace=is_whitespace,
        is_control=is_control,
        is_letter=is_letter,
        is_digit=is_digit,
        is_numeric=is_numeric,
        is_punctuation=is_punctuation,
        is_symbol=is_symbol,
        is_mark=is_mark,
        is_currency=is_currency,
        is_math=is_math,
        is_emoji=is_emoji,
    )


def get_char_width(char: str) -> str:
    """
    Estimate the display width of a character.
    
    Args:
        char: Character
    
    Returns:
        Width category: 'narrow', 'wide', 'half', 'full', 'ambiguous'
    
    Example:
        >>> get_char_width('A')
        'narrow'
        >>> get_char_width('中')
        'wide'
    """
    category = unicodedata.category(char)
    
    # East Asian Width property (approximated)
    code_point = ord(char)
    
    # Wide characters (CJK, emoji, etc.)
    wide_ranges = [
        (0x1100, 0x115F),   # Hangul Jamo
        (0x2329, 0x232A),   # Angle brackets
        (0x2E80, 0x303E),   # CJK radicals and symbols
        (0x3040, 0xA4CF),   # CJK scripts and Yi
        (0xAC00, 0xD7A3),   # Hangul syllables
        (0xF900, 0xFAFF),   # CJK compatibility
        (0xFE10, 0xFE1F),   # Vertical forms
        (0xFE30, 0xFE6F),   # CJK compatibility forms
        (0xFF00, 0xFF60),   # Fullwidth forms
        (0xFFE0, 0xFFE6),   # Fullwidth symbols
        (0x1F300, 0x1F9FF), # Emoji
    ]
    
    for start, end in wide_ranges:
        if start <= code_point <= end:
            return 'wide'
    
    # Ambiguous width (depends on context)
    ambiguous_ranges = [
        (0x00A1, 0x00A1),   # Inverted exclamation
        (0x00A4, 0x00A4),   # Currency sign
        (0x00A7, 0x00A8),   # Section, diaeresis
        (0x00AA, 0x00AA),   # Feminine ordinal
        (0x00AD, 0x00AE),   # Soft hyphen, registered
        (0x00B0, 0x00B4),   # Degree, accents
        (0x00B6, 0x00BA),   # Paragraph, ordinals
        (0x00BC, 0x00BE),   # Fractions
        (0x00C0, 0x00C5),   # Capital accents
        (0x00C7, 0x00CF),   # Capital letters with accents
        (0x00D1, 0x00D6),   # Capital letters with accents
        (0x00D8, 0x00DD),   # Capital letters with accents
    ]
    
    for start, end in ambiguous_ranges:
        if start <= code_point <= end:
            return 'ambiguous'
    
    return 'narrow'


def get_script(char: str) -> str:
    """
    Estimate the script for a character.
    
    Args:
        char: Character
    
    Returns:
        Script name
    
    Example:
        >>> get_script('A')
        'Latin'
        >>> get_script('中')
        'CJK'
        >>> get_script('あ')
        'Hiragana'
    """
    block = get_block(char)
    
    script_map = {
        'Basic Latin': 'Latin',
        'Latin-1 Supplement': 'Latin',
        'Latin Extended-A': 'Latin',
        'Latin Extended-B': 'Latin',
        'Latin Extended Additional': 'Latin',
        'IPA Extensions': 'IPA',
        'Greek and Coptic': 'Greek',
        'Greek Extended': 'Greek',
        'Cyrillic': 'Cyrillic',
        'Cyrillic Supplement': 'Cyrillic',
        'Armenian': 'Armenian',
        'Hebrew': 'Hebrew',
        'Arabic': 'Arabic',
        'Syriac': 'Syriac',
        'Thaana': 'Thaana',
        'Devanagari': 'Devanagari',
        'Bengali': 'Bengali',
        'Gurmukhi': 'Gurmukhi',
        'Gujarati': 'Gujarati',
        'Oriya': 'Oriya',
        'Tamil': 'Tamil',
        'Telugu': 'Telugu',
        'Kannada': 'Kannada',
        'Malayalam': 'Malayalam',
        'Sinhala': 'Sinhala',
        'Thai': 'Thai',
        'Lao': 'Lao',
        'Tibetan': 'Tibetan',
        'Georgian': 'Georgian',
        'Hangul Jamo': 'Hangul',
        'Hangul Compatibility Jamo': 'Hangul',
        'Hangul Syllables': 'Hangul',
        'Ethiopic': 'Ethiopic',
        'Ethiopic Extended': 'Ethiopic',
        'Cherokee': 'Cherokee',
        'Unified Canadian Aboriginal Syllabics': 'Canadian Aboriginal',
        'Ogham': 'Ogham',
        'Runic': 'Runic',
        'Khmer': 'Khmer',
        'Mongolian': 'Mongolian',
        'Hiragana': 'Hiragana',
        'Katakana': 'Katakana',
        'Bopomofo': 'Bopomofo',
        'Bopomofo Extended': 'Bopomofo',
        'CJK Unified Ideographs': 'CJK',
        'CJK Unified Ideographs Extension A': 'CJK',
        'CJK Compatibility Ideographs': 'CJK',
        'CJK Symbols and Punctuation': 'CJK',
        'CJK Radicals Supplement': 'CJK',
        'Kangxi Radicals': 'CJK',
        'Yi Syllables': 'Yi',
        'Yi Radicals': 'Yi',
        'Braille Patterns': 'Braille',
        'Dingbats': 'Symbol',
        'Miscellaneous Symbols': 'Symbol',
        'Arrows': 'Symbol',
        'Mathematical Operators': 'Math',
        'Currency Symbols': 'Currency',
    }
    
    return script_map.get(block, 'Unknown')


def get_html_entity_named(char: str) -> Optional[str]:
    """
    Get named HTML entity for a character if one exists.
    
    Args:
        char: Character
    
    Returns:
        Named HTML entity, or None
    
    Example:
        >>> get_html_entity_named('<')
        '&lt;'
        >>> get_html_entity_named('©')
        '&copy;'
    """
    # Common named HTML entities
    named_entities = {
        '<': '&lt;',
        '>': '&gt;',
        '&': '&amp;',
        '"': '&quot;',
        "'": '&apos;',
        ' ': '&nbsp;',
        '©': '&copy;',
        '®': '&reg;',
        '™': '&trade;',
        '°': '&deg;',
        '±': '&plusmn;',
        '×': '&times;',
        '÷': '&divide;',
        '€': '&euro;',
        '£': '&pound;',
        '¥': '&yen;',
        '¢': '&cent;',
        '§': '&sect;',
        '¶': '&para;',
        '•': '&bull;',
        '…': '&hellip;',
        '—': '&mdash;',
        '–': '&ndash;',
        '«': '&laquo;',
        '»': '&raquo;',
        '†': '&dagger;',
        '‡': '&Dagger;',
        '‰': '&permil;',
        '♠': '&spades;',
        '♣': '&clubs;',
        '♥': '&hearts;',
        '♦': '&diams;',
        '←': '&larr;',
        '→': '&rarr;',
        '↑': '&uarr;',
        '↓': '&darr;',
        '↔': '&harr;',
        '⇐': '&lArr;',
        '⇒': '&rArr;',
        '⇑': '&uArr;',
        '⇓': '&dArr;',
        '⇔': '&hArr;',
        '∀': '&forall;',
        '∃': '&exist;',
        '∅': '&empty;',
        '∈': '&isin;',
        '∉': '&notin;',
        '∋': '&ni;',
        '∏': '&prod;',
        '∑': '&sum;',
        '−': '&minus;',
        '∗': '&lowast;',
        '√': '&radic;',
        '∝': '&prop;',
        '∞': '&infin;',
        '∠': '&ang;',
        '∧': '&and;',
        '∨': '&or;',
        '∩': '&cap;',
        '∪': '&cup;',
        '∫': '&int;',
        '≈': '&approx;',
        '≠': '&ne;',
        '≡': '&equiv;',
        '≤': '&le;',
        '≥': '&ge;',
        '⊂': '&sub;',
        '⊃': '&sup;',
        '⊆': '&sube;',
        '⊇': '&supe;',
        '⊕': '&oplus;',
        '⊗': '&otimes;',
        '⊥': '&perp;',
        '⋅': '&sdot;',
        'α': '&alpha;',
        'β': '&beta;',
        'γ': '&gamma;',
        'δ': '&delta;',
        'ε': '&epsilon;',
        'ζ': '&zeta;',
        'η': '&eta;',
        'θ': '&theta;',
        'ι': '&iota;',
        'κ': '&kappa;',
        'λ': '&lambda;',
        'μ': '&mu;',
        'ν': '&nu;',
        'ξ': '&xi;',
        'ο': '&omicron;',
        'π': '&pi;',
        'ρ': '&rho;',
        'σ': '&sigma;',
        'τ': '&tau;',
        'υ': '&upsilon;',
        'φ': '&phi;',
        'χ': '&chi;',
        'ψ': '&psi;',
        'ω': '&omega;',
        'Α': '&Alpha;',
        'Β': '&Beta;',
        'Γ': '&Gamma;',
        'Δ': '&Delta;',
        'Ε': '&Epsilon;',
        'Ζ': '&Zeta;',
        'Η': '&Eta;',
        'Θ': '&Theta;',
        'Ι': '&Iota;',
        'Κ': '&Kappa;',
        'Λ': '&Lambda;',
        'Μ': '&Mu;',
        'Ν': '&Nu;',
        'Ξ': '&Xi;',
        'Ο': '&Omicron;',
        'Π': '&Pi;',
        'Ρ': '&Rho;',
        'Σ': '&Sigma;',
        'Τ': '&Tau;',
        'Υ': '&Upsilon;',
        'Φ': '&Phi;',
        'Χ': '&Chi;',
        'Ψ': '&Psi;',
        'Ω': '&Omega;',
        'ƒ': '&fnof;',
        '–': '&ndash;',
        '—': '&mdash;',
        '‚': '&sbquo;',
        '„': '&bdquo;',
        '†': '&dagger;',
        '‡': '&Dagger;',
        '•': '&bull;',
        '…': '&hellip;',
        '′': '&prime;',
        '″': '&Prime;',
        'À': '&Agrave;',
        'Á': '&Aacute;',
        'Â': '&Acirc;',
        'Ã': '&Atilde;',
        'Ä': '&Auml;',
        'Å': '&Aring;',
        'Æ': '&AElig;',
        'Ç': '&Ccedil;',
        'È': '&Egrave;',
        'É': '&Eacute;',
        'Ê': '&Ecirc;',
        'Ë': '&Euml;',
        'Ì': '&Igrave;',
        'Í': '&Iacute;',
        'Î': '&Icirc;',
        'Ï': '&Iuml;',
        'Ð': '&ETH;',
        'Ñ': '&Ntilde;',
        'Ò': '&Ograve;',
        'Ó': '&Oacute;',
        'Ô': '&Ocirc;',
        'Õ': '&Otilde;',
        'Ö': '&Ouml;',
        'Ø': '&Oslash;',
        'Ù': '&Ugrave;',
        'Ú': '&Uacute;',
        'Û': '&Ucirc;',
        'Ü': '&Uuml;',
        'Ý': '&Yacute;',
        'Þ': '&THORN;',
        'ß': '&szlig;',
        'à': '&agrave;',
        'á': '&aacute;',
        'â': '&acirc;',
        'ã': '&atilde;',
        'ä': '&auml;',
        'å': '&aring;',
        'æ': '&aelig;',
        'ç': '&ccedil;',
        'è': '&egrave;',
        'é': '&eacute;',
        'ê': '&ecirc;',
        'ë': '&euml;',
        'ì': '&igrave;',
        'í': '&iacute;',
        'î': '&icirc;',
        'ï': '&iuml;',
        'ð': '&eth;',
        'ñ': '&ntilde;',
        'ò': '&ograve;',
        'ó': '&oacute;',
        'ô': '&ocirc;',
        'õ': '&otilde;',
        'ö': '&ouml;',
        'ø': '&oslash;',
        'ù': '&ugrave;',
        'ú': '&uacute;',
        'û': '&ucirc;',
        'ü': '&uuml;',
        'ý': '&yacute;',
        'þ': '&thorn;',
        'ÿ': '&yuml;',
    }
    
    return named_entities.get(char)


# Character type checking functions

# Category lookup cache for performance (lazy-initialized)
_category_cache: Dict[str, str] = {}


def _get_category(char: str) -> str:
    """Get Unicode category with local caching."""
    if char not in _category_cache:
        _category_cache[char] = unicodedata.category(char)
    return _category_cache[char]


def _make_category_checker(categories: Union[str, Tuple[str, ...], Set[str]]) -> Callable[[str], bool]:
    """
    Factory to create optimized category checker functions.
    
    Args:
        categories: Single category, tuple/set of categories to match
    
    Returns:
        Optimized checker function with category tuple for fast membership test
    """
    cat_tuple = categories if isinstance(categories, tuple) else tuple(categories)
    def checker(char: str) -> bool:
        return _get_category(char) in cat_tuple
    return checker


# Pre-built optimized checkers
is_control_category = _make_category_checker(('Cc',))
is_letter_category = _make_category_checker(('Lu', 'Ll', 'Lt', 'Lm', 'Lo'))
is_mark_category = _make_category_checker(('Mn', 'Mc', 'Me'))
is_numeric_category = _make_category_checker(('Nd', 'Nl', 'No'))
is_punctuation_category = _make_category_checker(('Pc', 'Pd', 'Ps', 'Pe', 'Pi', 'Pf', 'Po'))
is_symbol_category = _make_category_checker(('Sm', 'Sc', 'Sk', 'So'))


def is_char_printable(char: str) -> bool:
    """Check if character is printable."""
    category = _get_category(char)
    return category not in ('Cc', 'Cs', 'Cn') and char.isprintable()


def is_char_whitespace(char: str) -> bool:
    """Check if character is whitespace."""
    return char.isspace()


def is_char_control(char: str) -> bool:
    """Check if character is a control character."""
    return is_control_category(char)


def is_char_letter(char: str) -> bool:
    """Check if character is a letter."""
    return is_letter_category(char)


def is_char_digit(char: str) -> bool:
    """Check if character is a digit."""
    return _get_category(char) == 'Nd'


def is_char_numeric(char: str) -> bool:
    """Check if character is numeric (including Roman numerals, fractions, etc.)."""
    return is_numeric_category(char)


def is_char_punctuation(char: str) -> bool:
    """Check if character is punctuation."""
    return is_punctuation_category(char)


def is_char_symbol(char: str) -> bool:
    """Check if character is a symbol."""
    return is_symbol_category(char)


def is_char_mark(char: str) -> bool:
    """Check if character is a combining mark."""
    return is_mark_category(char)


def is_char_currency(char: str) -> bool:
    """Check if character is a currency symbol."""
    return _get_category(char) == 'Sc'


def is_char_math(char: str) -> bool:
    """Check if character is a math symbol."""
    return _get_category(char) == 'Sm'


def is_char_emoji(char: str) -> bool:
    """Check if character is likely an emoji."""
    code_point = ord(char)
    emoji_ranges = [
        (0x1F300, 0x1F9FF),   # Various emoji
        (0x2600, 0x27BF),     # Misc symbols + dingbats (some emoji)
        (0x1F600, 0x1F64F),   # Emoticons
        (0x1F680, 0x1F6FF),   # Transport & map
        (0x1F900, 0x1F9FF),   # Supplemental symbols
        (0x1FA00, 0x1FA6F),   # Chess symbols
        (0x1FA70, 0x1FAFF),   # Symbols and pictographs extended-A
        (0x2300, 0x23FF),     # Misc technical (some emoji)
        (0x2700, 0x27BF),     # Dingbats
        (0x1F1E6, 0x1F1FF),   # Regional indicator symbols
    ]
    return any(start <= code_point <= end for start, end in emoji_ranges)


def normalize_char(char: str, form: str = 'NFC') -> str:
    """
    Normalize a character to specified Unicode normalization form.
    
    Args:
        char: Character
        form: Normalization form ('NFC', 'NFD', 'NFKC', 'NFKD')
    
    Returns:
        Normalized character
    
    Example:
        >>> normalize_char('é', 'NFD')  # Decompose
        'e'
        >>> normalize_char('e\u0301', 'NFC')  # Compose
        'é'
    """
    return unicodedata.normalize(form, char)


def decompose_char(char: str) -> Tuple[str, List[str]]:
    """
    Decompose a character into base + combining marks.
    
    Args:
        char: Character
    
    Returns:
        Tuple of (base character, list of combining marks)
    
    Example:
        >>> decompose_char('é')
        ('e', ['\u0301'])
        >>> decompose_char('ã')
        ('a', ['\u0303'])
    """
    decomposed = unicodedata.normalize('NFD', char)
    
    base = ''
    marks = []
    
    for c in decomposed:
        if unicodedata.category(c) in ('Mn', 'Mc', 'Me'):
            marks.append(c)
        else:
            if not base:
                base = c
    
    return (base, marks)


def compose_char(base: str, marks: List[str]) -> str:
    """
    Compose a base character with combining marks.
    
    Args:
        base: Base character
        marks: List of combining marks
    
    Returns:
        Composed character
    
    Example:
        >>> compose_char('e', ['\u0301'])
        'é'
        >>> compose_char('a', ['\u0303'])
        'ã'
    """
    combined = base + ''.join(marks)
    return unicodedata.normalize('NFC', combined)


def analyze_string(s: str) -> Dict[str, any]:
    """
    Analyze a string for Unicode statistics.
    
    Args:
        s: String to analyze
    
    Returns:
        Dictionary with Unicode statistics
    
    Example:
        >>> stats = analyze_string('Hello 世界! 🌍')
        >>> stats['total_chars']
        11
        >>> stats['letter_count']
        7
        >>> stats['emoji_count']
        1
    """
    if not s:
        return {
            'total_chars': 0,
            'unique_chars': 0,
            'max_code_point': 0,
            'byte_length_utf8': 0,
            'byte_length_utf16': 0,
            'letter_count': 0,
            'digit_count': 0,
            'punctuation_count': 0,
            'symbol_count': 0,
            'whitespace_count': 0,
            'control_count': 0,
            'emoji_count': 0,
            'currency_count': 0,
            'mark_count': 0,
            'block_distribution': {},
            'script_distribution': {},
            'category_distribution': {},
            'width_distribution': {},
            'code_point_range': None,
            'has_non_ascii': False,
            'has_combining_marks': False,
            'has_emoji': False,
            'has_surrogates': False,
            'is_normalized_nfc': True,
            'is_normalized_nfd': False,
        }
    
    stats = {
        'total_chars': len(s),
        'unique_chars': len(set(s)),
        'max_code_point': max(ord(c) for c in s),
        'byte_length_utf8': len(s.encode('utf-8')),
        'byte_length_utf16': len(s.encode('utf-16-le')),
        'letter_count': 0,
        'digit_count': 0,
        'punctuation_count': 0,
        'symbol_count': 0,
        'whitespace_count': 0,
        'control_count': 0,
        'emoji_count': 0,
        'currency_count': 0,
        'mark_count': 0,
        'block_distribution': {},
        'script_distribution': {},
        'category_distribution': {},
        'width_distribution': {},
        'has_non_ascii': False,
        'has_combining_marks': False,
        'has_emoji': False,
        'has_surrogates': False,
    }
    
    for char in s:
        # Type counts
        if is_char_letter(char):
            stats['letter_count'] += 1
        if is_char_digit(char):
            stats['digit_count'] += 1
        if is_char_punctuation(char):
            stats['punctuation_count'] += 1
        if is_char_symbol(char):
            stats['symbol_count'] += 1
        if is_char_whitespace(char):
            stats['whitespace_count'] += 1
        if is_char_control(char):
            stats['control_count'] += 1
        if is_char_emoji(char):
            stats['emoji_count'] += 1
        if is_char_currency(char):
            stats['currency_count'] += 1
        if is_char_mark(char):
            stats['mark_count'] += 1
        
        # Block distribution
        block = get_block(char)
        stats['block_distribution'][block] = stats['block_distribution'].get(block, 0) + 1
        
        # Script distribution
        script = get_script(char)
        stats['script_distribution'][script] = stats['script_distribution'].get(script, 0) + 1
        
        # Category distribution
        category = unicodedata.category(char)
        stats['category_distribution'][category] = stats['category_distribution'].get(category, 0) + 1
        
        # Width distribution
        width = get_char_width(char)
        stats['width_distribution'][width] = stats['width_distribution'].get(width, 0) + 1
        
        # Flags
        if ord(char) > 127:
            stats['has_non_ascii'] = True
        if is_char_mark(char):
            stats['has_combining_marks'] = True
        if is_char_emoji(char):
            stats['has_emoji'] = True
        if unicodedata.category(char) == 'Cs':
            stats['has_surrogates'] = True
    
    # Code point range
    code_points = [ord(c) for c in s]
    if code_points:
        stats['code_point_range'] = (min(code_points), max(code_points))
    
    # Normalization status (handle Python 3.6 compatibility)
    # unicodedata.is_normalized was added in Python 3.8
    if hasattr(unicodedata, 'is_normalized'):
        stats['is_normalized_nfc'] = unicodedata.is_normalized('NFC', s)
        stats['is_normalized_nfd'] = unicodedata.is_normalized('NFD', s)
    else:
        # For Python 3.6, approximate by comparing normalized forms
        stats['is_normalized_nfc'] = (unicodedata.normalize('NFC', s) == s)
        stats['is_normalized_nfd'] = (unicodedata.normalize('NFD', s) == s)
    
    return stats


def get_string_info(s: str) -> List[Dict[str, any]]:
    """
    Get detailed information for each character in a string.
    
    Args:
        s: String
    
    Returns:
        List of character info dictionaries
    
    Example:
        >>> info = get_string_info('AB')
        >>> len(info)
        2
        >>> info[0]['name']
        'LATIN CAPITAL LETTER A'
    """
    return [
        {
            'char': char,
            'code_point': ord(char),
            'name': unicodedata.name(char, f'<unnamed> U+{ord(char):04X}'),
            'category': unicodedata.category(char),
            'block': get_block(char),
            'script': get_script(char),
            'width': get_char_width(char),
        }
        for char in s
    ]


def convert_to_html_entities(s: str, use_named: bool = True) -> str:
    """
    Convert a string to HTML entities.
    
    Args:
        s: String
        use_named: Prefer named entities where available
    
    Returns:
        String with characters replaced by HTML entities
    
    Example:
        >>> convert_to_html_entities('<>')
        '&lt;&gt;'
        >>> convert_to_html_entities('世界')
        '&#x4E16;&#x4E2D;'
    """
    result = []
    
    for char in s:
        # ASCII printable characters except special ones
        if ord(char) < 128 and char not in '<>&"\'':
            result.append(char)
            continue
        
        # Check for named entity
        if use_named:
            named = get_html_entity_named(char)
            if named:
                result.append(named)
                continue
        
        # Use numeric entity
        result.append(f'&#x{ord(char):04X};')
    
    return ''.join(result)


def convert_from_html_entities(s: str) -> str:
    """
    Convert HTML entities back to characters.
    
    Args:
        s: String with HTML entities
    
    Returns:
        String with entities replaced by characters
    
    Example:
        >>> convert_from_html_entities('&lt;&gt;')
        '<>'
        >>> convert_from_html_entities('&#x4E16;&#x4E2D;')
        '世界'
    """
    # Named entity mapping (reverse)
    named_to_char = {
        '&lt;': '<',
        '&gt;': '>',
        '&amp;': '&',
        '&quot;': '"',
        '&apos;': "'",
        '&nbsp;': '\u00A0',
        '&copy;': '©',
        '&reg;': '®',
        '&trade;': '™',
        '&deg;': '°',
        '&euro;': '€',
        '&pound;': '£',
        '&yen;': '¥',
        '&cent;': '¢',
        '&mdash;': '—',
        '&ndash;': '–',
        '&hellip;': '…',
    }
    
    # Replace named entities
    for entity, char in named_to_char.items():
        s = s.replace(entity, char)
    
    # Replace decimal entities (&#65;)
    decimal_pattern = r'&#(\d+);'
    s = re.sub(decimal_pattern, lambda m: chr(int(m.group(1))), s)
    
    # Replace hex entities (&#x41;)
    hex_pattern = r'&#x([0-9A-Fa-f]+);'
    s = re.sub(hex_pattern, lambda m: chr(int(m.group(1), 16)), s)
    
    return s


def get_unicode_version(char: str) -> Optional[str]:
    """
    Estimate the Unicode version when a character was introduced.
    
    Args:
        char: Character
    
    Returns:
        Unicode version string, or None
    
    Note:
        This is an approximation based on code point ranges.
    
    Example:
        >>> get_unicode_version('A')
        '1.0'
        >>> get_unicode_version('€')
        '2.1'
    """
    code_point = ord(char)
    
    # Approximate version ranges
    version_ranges = [
        (0x0000, 0x007F, '1.0'),      # Basic Latin
        (0x0080, 0x00FF, '1.0'),      # Latin-1 Supplement
        (0x0100, 0x017F, '1.0'),      # Latin Extended-A
        (0x0180, 0x024F, '1.0'),      # Latin Extended-B
        (0x0250, 0x02AF, '1.0'),      # IPA Extensions
        (0x20A0, 0x20CF, '2.0'),      # Currency Symbols (€ at 20AC)
        (0x1F300, 0x1F5FF, '6.0'),    # Misc Symbols and Pictographs
        (0x1F600, 0x1F64F, '6.0'),    # Emoticons
        (0x1F680, 0x1F6FF, '6.0'),    # Transport & Map
        (0x1F900, 0x1F9FF, '10.0'),   # Supplemental Symbols
        (0x1FA00, 0x1FAFF, '12.0'),   # Chess and Extended-A
    ]
    
    for start, end, version in version_ranges:
        if start <= code_point <= end:
            return version
    
    # Default to 1.0 for older characters
    if code_point <= 0xFFFF:
        return '1.0'  # BMP
    
    return None


def is_valid_unicode(s: str) -> bool:
    """
    Check if a string contains valid Unicode characters.
    
    Args:
        s: String
    
    Returns:
        True if all characters are valid
    
    Example:
        >>> is_valid_unicode('Hello')
        True
        >>> is_valid_unicode('\ud800')  # Lone surrogate
        False
    """
    try:
        s.encode('utf-8')
        # Check for surrogates
        for char in s:
            if unicodedata.category(char) == 'Cs':
                return False
        return True
    except UnicodeEncodeError:
        return False


def get_similar_chars(char: str, limit: int = 10) -> List[Dict[str, any]]:
    """
    Find characters similar to the given character (by name or shape).
    
    Args:
        char: Character
        limit: Maximum results
    
    Returns:
        List of similar characters
    
    Example:
        >>> similar = get_similar_chars('A')
        >>> len(similar)
        10
    """
    # Similar characters by category and shape
    category = unicodedata.category(char)
    
    # Characters with similar names
    try:
        name = unicodedata.name(char)
        name_keywords = name.split()[:2]  # First two words
    except ValueError:
        name_keywords = []
    
    results = []
    
    # Search in same category
    for cp in range(0x0000, 0xFFFF):
        if cp == ord(char):
            continue
        
        try:
            c = chr(cp)
            if unicodedata.category(c) == category:
                try:
                    c_name = unicodedata.name(c)
                    # Check for similar name
                    if any(kw in c_name for kw in name_keywords):
                        results.append({
                            'char': c,
                            'code_point': cp,
                            'name': c_name,
                            'similarity': 'name',
                        })
                except ValueError:
                    pass
                
                if len(results) >= limit:
                    break
        except ValueError:
            pass
    
    return results


def print_char_table(chars: List[str], width: int = 8) -> str:
    """
    Create a formatted table of characters.
    
    Args:
        chars: List of characters
        width: Number of columns
    
    Returns:
        Formatted table string
    
    Example:
        >>> print_char_table(['A', 'B', 'C'])
        'A | B | C\\n65 | 66 | 67'
    """
    if not chars:
        return ""
    
    rows = []
    
    # Character row
    char_row = []
    code_row = []
    name_row = []
    
    for i, char in enumerate(chars):
        if i > 0 and i % width == 0:
            rows.append(' | '.join(char_row))
            rows.append(' | '.join(code_row))
            rows.append(' | '.join(name_row))
            rows.append('-' * 40)
            char_row = []
            code_row = []
            name_row = []
        
        char_row.append(char)
        code_row.append(f'U+{ord(char):04X}')
        try:
            name = unicodedata.name(char, '?')
            # Truncate name for display
            if len(name) > 10:
                name = name[:10] + '...'
            name_row.append(name)
        except ValueError:
            name_row.append('?')
    
    # Remaining characters
    if char_row:
        rows.append(' | '.join(char_row))
        rows.append(' | '.join(code_row))
        rows.append(' | '.join(name_row))
    
    return '\n'.join(rows)


def escape_unicode(s: str, escape_all: bool = False) -> str:
    """
    Escape non-ASCII characters in a string.
    
    Args:
        s: String
        escape_all: Escape all characters
    
    Returns:
        Escaped string
    
    Example:
        >>> escape_unicode('Hello 世界')
        'Hello \\u4e16\\u4e2d'
        >>> escape_unicode('Hello', escape_all=True)
        '\\u0048\\u0065\\u006c\\u006c\\u006f'
    """
    result = []
    
    for char in s:
        if escape_all or ord(char) > 127:
            result.append(f'\\u{ord(char):04x}')
        else:
            result.append(char)
    
    return ''.join(result)


def unescape_unicode(s: str) -> str:
    """
    Unescape Unicode escape sequences in a string.
    
    Args:
        s: String with escape sequences
    
    Returns:
        Unescaped string
    
    Example:
        >>> unescape_unicode('Hello \\u4e16\\u4e2d')
        'Hello 世界'
    """
    # Match \\uXXXX patterns
    pattern = r'\\u([0-9A-Fa-f]{4})'
    return re.sub(pattern, lambda m: chr(int(m.group(1), 16)), s)


def get_combining_chain(char: str) -> List[str]:
    """
    Get the full chain of combining characters for a composed character.
    
    Args:
        char: Character
    
    Returns:
        List of base + combining marks
    
    Example:
        >>> get_combining_chain('é')
        ['e', '\\u0301']
    """
    base, marks = decompose_char(char)
    result = [base] if base else []
    result.extend(marks)
    return result


def strip_combining_marks(s: str) -> str:
    """
    Remove all combining marks from a string.
    
    Args:
        s: String
    
    Returns:
        String without combining marks
    
    Example:
        >>> strip_combining_marks('éàü')
        'eau'
    """
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) not in ('Mn', 'Mc', 'Me'))


def count_width(s: str) -> int:
    """
    Count the display width of a string (accounting for wide characters).
    
    Args:
        s: String
    
    Returns:
        Estimated display width
    
    Example:
        >>> count_width('Hello')
        5
        >>> count_width('你好')
        4  # Each CJK char is 2 wide
    """
    width = 0
    for char in s:
        char_width = get_char_width(char)
        if char_width == 'wide':
            width += 2
        elif char_width == 'ambiguous':
            width += 1  # Conservative estimate
        else:
            width += 1
    return width


def pad_unicode(s: str, target_width: int, pad_char: str = ' ', 
                align: str = 'left') -> str:
    """
    Pad a string to target display width (accounting for wide characters).
    
    Args:
        s: String
        target_width: Target width in display columns
        pad_char: Padding character
        align: Alignment ('left', 'right', 'center')
    
    Returns:
        Padded string
    
    Example:
        >>> pad_unicode('你好', 6)
        '你好  '
        >>> pad_unicode('你好', 6, align='center')
        ' 你好 '
    """
    current_width = count_width(s)
    
    if current_width >= target_width:
        return s
    
    pad_needed = target_width - current_width
    
    if align == 'left':
        return s + pad_char * pad_needed
    elif align == 'right':
        return pad_char * pad_needed + s
    elif align == 'center':
        left_pad = pad_needed // 2
        right_pad = pad_needed - left_pad
        return pad_char * left_pad + s + pad_char * right_pad
    
    return s


def get_unicode_plane(code_point: int) -> str:
    """
    Get the Unicode plane name for a code point.
    
    Args:
        code_point: Unicode code point
    
    Returns:
        Plane name
    
    Example:
        >>> get_unicode_plane(65)
        'Basic Multilingual Plane'
        >>> get_unicode_plane(0x1F600)
        'Supplementary Multilingual Plane'
    """
    if code_point <= 0xFFFF:
        return 'Basic Multilingual Plane (BMP)'
    elif code_point <= 0x1FFFF:
        return 'Supplementary Multilingual Plane (SMP)'
    elif code_point <= 0x2FFFF:
        return 'Supplementary Ideographic Plane (SIP)'
    elif code_point <= 0xDFFFF:
        return 'Tertiary Ideographic Plane (TIP)'
    elif code_point <= 0xEFFFF:
        return 'Supplementary Special-purpose Plane (SSP)'
    elif code_point <= 0xFFFFF:
        return 'Supplementary Private Use Area-A'
    elif code_point <= 0x10FFFF:
        return 'Supplementary Private Use Area-B'
    else:
        return 'Invalid Code Point'


def list_emojis(category: str = None, limit: int = 100) -> List[Dict[str, any]]:
    """
    List emoji characters.
    
    Args:
        category: Emoji category filter ('face', 'animal', 'food', 'activity', etc.)
        limit: Maximum results
    
    Returns:
        List of emoji info dictionaries
    
    Example:
        >>> emojis = list_emojis('face', limit=5)
        >>> len(emojis)
        5
    """
    results = []
    
    emoji_ranges = [
        (0x1F600, 0x1F64F, 'Emoticons'),
        (0x1F300, 0x1F5FF, 'Miscellaneous Symbols and Pictographs'),
        (0x1F680, 0x1F6FF, 'Transport and Map'),
        (0x1F900, 0x1F9FF, 'Supplemental Symbols and Pictographs'),
        (0x1FA00, 0x1FAFF, 'Symbols and Pictographs Extended-A'),
        (0x2600, 0x27BF, 'Miscellaneous Symbols'),
    ]
    
    category_keywords = {
        'face': ['FACE', 'EMOTICON', 'SMILE'],
        'animal': ['ANIMAL', 'DOG', 'CAT', 'BIRD', 'FISH', 'BUG'],
        'food': ['FOOD', 'DRINK', 'FRUIT', 'VEGETABLE'],
        'activity': ['SPORT', 'GAME', 'ACTIVITY'],
        'travel': ['TRANSPORT', 'CAR', 'TRAIN', 'PLANE', 'BOAT'],
        'nature': ['FLOWER', 'TREE', 'PLANT', 'WEATHER', 'SUN', 'MOON'],
        'symbol': ['SYMBOL', 'SIGN', 'ARROW'],
        'object': ['OBJECT', 'PHONE', 'COMPUTER', 'BOOK'],
    }
    
    keywords = category_keywords.get(category, []) if category else []
    
    for start, end, block_name in emoji_ranges:
        for cp in range(start, end + 1):
            try:
                char = chr(cp)
                name = unicodedata.name(char, '')
                
                # Filter by category keywords
                if keywords:
                    if not any(kw in name for kw in keywords):
                        continue
                
                results.append({
                    'char': char,
                    'code_point': cp,
                    'name': name,
                    'block': block_name,
                })
                
                if len(results) >= limit:
                    return results
            except ValueError:
                pass
    
    return results


def get_named_entity_list() -> Dict[str, str]:
    """
    Get a dictionary of named HTML entities.
    
    Returns:
        Dictionary mapping entity names to characters
    
    Example:
        >>> entities = get_named_entity_list()
        >>> entities['&lt;']
        '<'
        >>> entities['&euro;']
        '€'
    """
    return {
        '&lt;': '<',
        '&gt;': '>',
        '&amp;': '&',
        '&quot;': '"',
        '&apos;': "'",
        '&nbsp;': '\u00A0',
        '&copy;': '©',
        '&reg;': '®',
        '&trade;': '™',
        '&deg;': '°',
        '&plusmn;': '±',
        '&times;': '×',
        '&divide;': '÷',
        '&euro;': '€',
        '&pound;': '£',
        '&yen;': '¥',
        '&cent;': '¢',
        '&sect;': '§',
        '&para;': '¶',
        '&bull;': '•',
        '&hellip;': '…',
        '&mdash;': '—',
        '&ndash;': '–',
        '&laquo;': '«',
        '&raquo;': '»',
        '&larr;': '←',
        '&rarr;': '→',
        '&uarr;': '↑',
        '&darr;': '↓',
        '&harr;': '↔',
        '&infin;': '∞',
        '&alpha;': 'α',
        '&beta;': 'β',
        '&gamma;': 'γ',
        '&delta;': 'δ',
        '&pi;': 'π',
        '&sigma;': 'σ',
        '&omega;': 'ω',
        '&Alpha;': 'Α',
        '&Beta;': 'Β',
        '&Gamma;': 'Γ',
        '&Delta;': 'Δ',
        '&Pi;': 'Π',
        '&Sigma;': 'Σ',
        '&Omega;': 'Ω',
    }


def validate_code_point(code_point: int) -> bool:
    """
    Validate if a code point is a valid Unicode code point.
    
    Args:
        code_point: Integer code point
    
    Returns:
        True if valid
    
    Example:
        >>> validate_code_point(65)
        True
        >>> validate_code_point(0x11FFFF)
        False
    """
    # Valid range: 0 to 0x10FFFF
    # Exclude surrogate range: 0xD800 to 0xDFFF
    if code_point < 0 or code_point > 0x10FFFF:
        return False
    if 0xD800 <= code_point <= 0xDFFF:
        return False
    return True


def get_char_summary(char: str) -> str:
    """
    Get a human-readable summary of a character.
    
    Args:
        char: Character
    
    Returns:
        Summary string
    
    Example:
        >>> get_char_summary('A')
        'A (U+0041) LATIN CAPITAL LETTER A - Letter, uppercase [Latin]'
    """
    info = get_full_info(char)
    
    return f"{char} (U+{info.code_point:04X}) {info.name} - {info.category_name} [{info.script}]"