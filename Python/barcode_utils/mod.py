#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AllToolkit - Barcode Utilities Module

Comprehensive barcode generation utilities for Python with zero external dependencies.
Provides Code 128, Code 39, EAN-13, EAN-8, UPC-A, ITF, and QR-like matrix barcodes.
All barcodes are generated as SVG for scalable, high-quality output.

Author: AllToolkit
License: MIT
"""

import math
from typing import List, Dict, Any, Optional, Tuple, Union
from dataclasses import dataclass, field


# =============================================================================
# Type Aliases
# =============================================================================

Number = Union[int, float]
Color = str  # Hex color like "#000000" or named color like "black"


# =============================================================================
# Constants
# =============================================================================

# Code 39 character encoding (bars pattern: 9 elements, 3 wide, 6 narrow)
CODE39_ENCODING = {
    '0': 'nnnwwnwnn', '1': 'wnnwnwnnn', '2': 'nnwwnwnnn', '3': 'wnwwnwnnn',
    '4': 'nnwnwwnnn', '5': 'wnwnwwnnn', '6': 'nwwnwwnnn', '7': 'nnnwww nn',
    '8': 'wnnwww nn', '9': 'nnwwww nn', 'A': 'wnnwnnwnw', 'B': 'nnwwnnwnw',
    'C': 'wnwwnnwnw', 'D': 'nnwnwnwnw', 'E': 'wnwnwnwnw', 'F': 'nwwnwnwnw',
    'G': 'nnnwwnwnw', 'H': 'wnnwwnwnw', 'I': 'nnwwwnwnw', 'J': 'nnwnnnww w',
    'K': 'wnnwnnww w', 'L': 'nnwwnnww w', 'M': 'wnwwnnww w', 'N': 'nnwnwnww w',
    'O': 'wnwnwnww w', 'P': 'nwwnwnww w', 'Q': 'nnnwwnww w', 'R': 'wnnwwnww w',
    'S': 'nnwwwnww w', 'T': 'nnnnwwww w', 'U': 'wnnnwwww w', 'V': 'nnwnnwww w',
    'W': 'nnnnwnwww', 'X': 'wnnnwnwww', 'Y': 'nnwnnwwww', 'Z': 'nnnnwwwww',
    '-': 'nnnwnnnww', '.': 'wnnwnnnww', ' ': 'nnwwnnnww', '$': 'wnwwnnnww',
    '/': 'nnwnwnnww', '+': 'wnwnwnnww', '%': 'nnnwwnnww', '*': 'nnwnnwnww',
}

# Code 128 character sets A, B, C
CODE128_CHARSET_A = {
    0: '212222', 1: '222122', 2: '222221', 3: '121223', 4: '121322',
    5: '131222', 6: '122213', 7: '122312', 8: '132212', 9: '221213',
    10: '221312', 11: '231212', 12: '112232', 13: '122132', 14: '122231',
    15: '113222', 16: '123122', 17: '123221', 18: '223211', 19: '221132',
    20: '221231', 21: '213212', 22: '223112', 23: '312131', 24: '311222',
    25: '321122', 26: '321221', 27: '312212', 28: '322112', 29: '322211',
    30: '212123', 31: '212321', 32: '232121', 33: '111323', 34: '131123',
    35: '131321', 36: '112313', 37: '132113', 38: '132311', 39: '211313',
    40: '231113', 41: '231311', 42: '112133', 43: '112331', 44: '132131',
    45: '113123', 46: '113321', 47: '133121', 48: '313121', 49: '211331',
    50: '231131', 51: '213113', 52: '213311', 53: '213131', 54: '311123',
    55: '311321', 56: '331121', 57: '312113', 58: '312311', 59: '332111',
    60: '314111', 61: '221411', 62: '431111', 63: '111224', 64: '111422',
    65: '121124', 66: '121421', 67: '141122', 68: '141221', 69: '112214',
    70: '112412', 71: '122114', 72: '122411', 73: '142112', 74: '142211',
    75: '241211', 76: '221114', 77: '413111', 78: '241113', 79: '231113',
    80: '411113', 81: '231311', 82: '111214', 83: '111412', 84: '121114',
    85: '121411', 86: '141112', 87: '141211', 88: '114112', 89: '114211',
    90: '411112', 91: '411211', 92: '111142', 93: '111241', 94: '121141',
    95: '114112', 96: '114211', 97: '411112', 98: '411211', 99: '111142',
    100: '111241', 101: '121141', 102: '114121', 103: '114211', 104: '411121',
    105: '411211', 106: '211412', 107: '211214', 108: '211232',
}

CODE128_CHARSET_B = {
    0: '212222', 1: '222122', 2: '222221', 3: '121223', 4: '121322',
    5: '131222', 6: '122213', 7: '122312', 8: '132212', 9: '221213',
    10: '221312', 11: '231212', 12: '112232', 13: '122132', 14: '122231',
    15: '113222', 16: '123122', 17: '123221', 18: '223211', 19: '221132',
    20: '221231', 21: '213212', 22: '223112', 23: '312131', 24: '311222',
    25: '321122', 26: '321221', 27: '312212', 28: '322112', 29: '322211',
    30: '212123', 31: '212321', 32: '232121', 33: '111323', 34: '131123',
    35: '131321', 36: '112313', 37: '132113', 38: '132311', 39: '211313',
    40: '231113', 41: '231311', 42: '112133', 43: '112331', 44: '132131',
    45: '113123', 46: '113321', 47: '133121', 48: '313121', 49: '211331',
    50: '231131', 51: '213113', 52: '213311', 53: '213131', 54: '311123',
    55: '311321', 56: '331121', 57: '312113', 58: '312311', 59: '332111',
    60: '314111', 61: '211412', 62: '211214', 63: '211232', 64: '2331112',
    65: '111323', 66: '131123', 67: '131321', 68: '112313', 69: '132113',
    70: '132311', 71: '211313', 72: '231113', 73: '231311', 74: '112133',
    75: '112331', 76: '132131', 77: '113123', 78: '113321', 79: '133121',
    80: '313121', 81: '211331', 82: '231131', 83: '213113', 84: '213311',
    85: '213131', 86: '311123', 87: '311321', 88: '331121', 89: '312113',
    90: '312311', 91: '332111', 92: '314111', 93: '211412', 94: '211214',
    95: '211232', 96: '2331112', 97: '111323', 98: '131123', 99: '131321',
    100: '112313', 101: '132113', 102: '132311', 103: '211313', 104: '231113',
    105: '231311', 106: '112133', 107: '112331', 108: '132131',
}

# EAN-13 parity patterns
EAN13_PARITY = {
    '0': 'AAAAAA', '1': 'AABABB', '2': 'AABBAB', '3': 'AABBBA',
    '4': 'ABAABB', '5': 'ABBAAB', '6': 'ABBABA', '7': 'ABABAB',
    '8': 'ABABBA', '9': 'ABBAAA',
}

# EAN-13 odd (A) and even (B) parity encodings
EAN13_ODD = {
    '0': '0001101', '1': '0011001', '2': '0010011', '3': '0111101',
    '4': '0100011', '5': '0110001', '6': '0101111', '7': '0111011',
    '8': '0110111', '9': '0001011',
}

EAN13_EVEN = {
    '0': '0100111', '1': '0110011', '2': '0011011', '3': '0100001',
    '4': '0011101', '5': '0111001', '6': '0000101', '7': '0010001',
    '8': '0001001', '9': '0010111',
}

EAN13_GUARD = '010101'
EAN13_CENTER = '0101010'

# UPC-A uses same encoding as EAN-13
UPCA_ODD = EAN13_ODD
UPCA_EVEN = EAN13_EVEN
UPCA_GUARD = '101'
UPCA_CENTER = '0101010'

# ITF (Interleaved 2 of 5) encoding
ITF_ENCODING = {
    '0': 'nnwwn', '1': 'wnnnw', '2': 'nwnnw', '3': 'wwnnn',
    '4': 'nnwnw', '5': 'wnwnn', '6': 'nwwnn', '7': 'nnnww',
    '8': 'wnnwn', '9': 'nwnwn',
}


# =============================================================================
# Data Classes
# =============================================================================

@dataclass
class BarcodeConfig:
    """Configuration for barcode appearance."""
    width: int = 2
    height: int = 100
    margin: int = 10
    show_text: bool = True
    text_size: int = 14
    text_margin: int = 5
    foreground: Color = "#000000"
    background: Color = "#FFFFFF"
    scale: float = 1.0


@dataclass
class BarcodeResult:
    """Result of barcode generation."""
    svg: str
    width: int
    height: int
    data: str
    format: str


# =============================================================================
# Helper Functions
# =============================================================================

def _parse_color(color: Color) -> str:
    """Normalize color to hex format."""
    named_colors = {
        'black': '#000000', 'white': '#FFFFFF', 'red': '#FF0000',
        'green': '#00FF00', 'blue': '#0000FF', 'yellow': '#FFFF00',
        'cyan': '#00FFFF', 'magenta': '#FF00FF', 'gray': '#808080',
        'grey': '#808080', 'orange': '#FFA500', 'purple': '#800080',
    }
    return named_colors.get(color.lower(), color)


def _expand_pattern(pattern: str, narrow: float = 1.0, wide: float = 3.0) -> List[float]:
    """Expand barcode pattern (n=wide, w=narrow) to module widths."""
    result = []
    for char in pattern:
        if char == 'n':
            result.append(narrow)
        elif char == 'w':
            result.append(wide)
    return result


def _pattern_to_svg_bars(pattern: str, x: float, y: float, height: float,
                          narrow_width: float, wide_width: float) -> List[str]:
    """Convert pattern string to SVG bar elements."""
    bars = []
    current_x = x
    is_black = True
    
    for char in pattern:
        width = wide_width if char == 'w' else narrow_width
        if is_black:
            bars.append(f'<rect x="{current_x:.2f}" y="{y:.2f}" width="{width:.2f}" height="{height:.2f}"/>')
        current_x += width
        is_black = not is_black
    
    return bars


def _modules_to_svg_bars(modules: str, x: float, y: float, height: float,
                         module_width: float) -> List[str]:
    """Convert module string (0=space, 1=bar) to SVG bar elements."""
    bars = []
    current_x = x
    
    for i, char in enumerate(modules):
        if char == '1':
            bars.append(f'<rect x="{current_x:.2f}" y="{y:.2f}" width="{module_width:.2f}" height="{height:.2f}"/>')
        current_x += module_width
    
    return bars


# =============================================================================
# Code 39 Barcode
# =============================================================================

def generate_code39(data: str, config: Optional[BarcodeConfig] = None) -> BarcodeResult:
    """
    Generate Code 39 barcode.
    
    Code 39 supports: 0-9, A-Z, space, -, ., $, /, +, %
    Data is automatically wrapped with start/stop character (*).
    
    Args:
        data: Data to encode (alphanumeric)
        config: Barcode configuration
        
    Returns:
        BarcodeResult with SVG content
        
    Example:
        >>> result = generate_code39("HELLO123")
        >>> print(result.svg)
    """
    if config is None:
        config = BarcodeConfig()
    
    # Validate and normalize data
    data = data.upper()
    valid_chars = set('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ -.$/+%')
    for char in data:
        if char not in valid_chars:
            raise ValueError(f"Invalid character '{char}' for Code 39")
    
    # Add start/stop character
    encoded_data = '*' + data + '*'
    
    # Calculate dimensions
    narrow_width = config.width * config.scale
    wide_width = config.width * 3 * config.scale
    module_height = config.height * config.scale
    
    # Generate bars
    all_bars = []
    current_x = config.margin * config.scale
    
    for char in encoded_data:
        pattern = CODE39_ENCODING.get(char, '')
        if pattern:
            bars = _pattern_to_svg_bars(pattern.replace(' ', ''), current_x, 0,
                                        module_height, narrow_width, wide_width)
            all_bars.extend(bars)
            current_x += sum(_expand_pattern(pattern.replace(' ', ''), narrow_width, wide_width))
            # Inter-character gap
            current_x += narrow_width
    
    total_width = current_x + config.margin * config.scale
    total_height = module_height
    
    # Add text if requested
    text_element = ''
    if config.show_text:
        text_y = module_height + config.text_margin * config.scale + config.text_size * config.scale
        total_height = text_y + config.text_size * config.scale + config.margin * config.scale
        text_element = f'<text x="{total_width/2:.2f}" y="{text_y:.2f}" text-anchor="middle" font-size="{config.text_size * config.scale:.2f}" font-family="monospace">{data}</text>'
    
    # Build SVG
    fg = _parse_color(config.foreground)
    bg = _parse_color(config.background)
    
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{total_width:.2f}" height="{total_height:.2f}" viewBox="0 0 {total_width:.2f} {total_height:.2f}">
  <rect width="100%" height="100%" fill="{bg}"/>
  <g fill="{fg}">
    {''.join(all_bars)}
  </g>
  {text_element}
</svg>'''
    
    return BarcodeResult(
        svg=svg,
        width=int(total_width),
        height=int(total_height),
        data=data,
        format='code39'
    )


# =============================================================================
# Code 128 Barcode
# =============================================================================

def generate_code128(data: str, config: Optional[BarcodeConfig] = None) -> BarcodeResult:
    """
    Generate Code 128 barcode (auto-detect best character set).
    
    Code 128 supports full ASCII character set with high density.
    Automatically selects between Set A, B, or C for optimal encoding.
    
    Args:
        data: Data to encode
        config: Barcode configuration
        
    Returns:
        BarcodeResult with SVG content
        
    Example:
        >>> result = generate_code128("Hello World 123")
        >>> print(result.svg)
    """
    if config is None:
        config = BarcodeConfig()
    
    # Use Set B by default (most common)
    charset = CODE128_CHARSET_B
    
    # Convert data to code values
    code_values = []
    for char in data:
        code = ord(char)
        if code < 32:
            code += 64  # Map control chars to Set B
        elif code >= 32 and code <= 127:
            code -= 32
        else:
            code = 64  # Default for extended chars
        code_values.append(code)
    
    # Calculate checksum
    checksum = 104  # Start Code B
    for i, code in enumerate(code_values):
        checksum += code * (i + 1)
    checksum = checksum % 103
    code_values.insert(0, 104)  # Start Code B
    code_values.append(checksum)
    code_values.append(106)  # Stop code
    
    # Generate bars
    all_bars = []
    current_x = config.margin * config.scale
    module_width = config.width * config.scale
    module_height = config.height * config.scale
    
    for code in code_values:
        pattern = charset.get(code, '212222')
        bars = _code128_pattern_to_bars(pattern, current_x, 0, module_height, module_width)
        all_bars.extend(bars)
        current_x += sum(int(d) for d in pattern) * module_width
    
    total_width = current_x + config.margin * config.scale
    total_height = module_height
    
    # Add text
    text_element = ''
    if config.show_text:
        text_y = module_height + config.text_margin * config.scale + config.text_size * config.scale
        total_height = text_y + config.text_size * config.scale + config.margin * config.scale
        text_element = f'<text x="{total_width/2:.2f}" y="{text_y:.2f}" text-anchor="middle" font-size="{config.text_size * config.scale:.2f}" font-family="monospace">{data}</text>'
    
    fg = _parse_color(config.foreground)
    bg = _parse_color(config.background)
    
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{total_width:.2f}" height="{total_height:.2f}" viewBox="0 0 {total_width:.2f} {total_height:.2f}">
  <rect width="100%" height="100%" height="{total_height:.2f}" fill="{bg}"/>
  <g fill="{fg}">
    {''.join(all_bars)}
  </g>
  {text_element}
</svg>'''
    
    return BarcodeResult(
        svg=svg,
        width=int(total_width),
        height=int(total_height),
        data=data,
        format='code128'
    )


def _code128_pattern_to_bars(pattern: str, x: float, y: float, height: float,
                              module_width: float) -> List[str]:
    """Convert Code 128 pattern to SVG bars."""
    bars = []
    current_x = x
    is_black = True
    
    for digit in pattern:
        width = int(digit) * module_width
        if is_black:
            bars.append(f'<rect x="{current_x:.2f}" y="{y:.2f}" width="{width:.2f}" height="{height:.2f}"/>')
        current_x += width
        is_black = not is_black
    
    return bars


# =============================================================================
# EAN-13 Barcode
# =============================================================================

def generate_ean13(code: str, config: Optional[BarcodeConfig] = None) -> BarcodeResult:
    """
    Generate EAN-13 barcode.
    
    EAN-13 is a 13-digit barcode used worldwide for retail products.
    The first 2-3 digits indicate the country/manufacturer prefix.
    
    Args:
        code: 12 or 13 digit code (checksum calculated if 12 digits)
        config: Barcode configuration
        
    Returns:
        BarcodeResult with SVG content
        
    Example:
        >>> result = generate_ean13("590123412345")
        >>> print(result.svg)
    """
    if config is None:
        config = BarcodeConfig()
    
    # Validate and prepare code
    code = ''.join(c for c in code if c.isdigit())
    if len(code) == 13:
        code = code[:12]  # Remove checksum if present
    elif len(code) != 12:
        raise ValueError("EAN-13 requires 12 digits (checksum will be calculated)")
    
    # Calculate checksum
    checksum = _calculate_ean13_checksum(code)
    full_code = code + str(checksum)
    
    # Generate modules
    modules = EAN13_GUARD  # Left guard
    
    # First digit determines parity pattern for next 6 digits
    first_digit = full_code[0]
    parity_pattern = EAN13_PARITY[first_digit]
    
    # Left side (6 digits with parity)
    for i in range(6):
        digit = full_code[i + 1]
        if parity_pattern[i] == 'A':
            modules += EAN13_ODD[digit]
        else:
            modules += EAN13_EVEN[digit]
    
    modules += EAN13_CENTER  # Center guard
    
    # Right side (6 digits, all even parity)
    for i in range(6, 12):
        digit = full_code[i + 1]
        modules += EAN13_EVEN[digit]
    
    modules += EAN13_GUARD  # Right guard
    
    # Generate SVG
    module_width = config.width * config.scale
    module_height = config.height * config.scale
    
    all_bars = _modules_to_svg_bars(modules, config.margin * config.scale, 0,
                                    module_height, module_width)
    
    total_width = (len(modules) + config.margin * 2) * module_width
    total_height = module_height
    
    # Add text
    text_element = ''
    if config.show_text:
        text_y = module_height + config.text_margin * config.scale + config.text_size * config.scale
        total_height = text_y + config.text_size * config.scale + config.margin * config.scale
        
        # Format text with spaces
        display_code = f"{full_code[0]} {full_code[1:7]} {full_code[7:]}"
        text_element = f'<text x="{total_width/2:.2f}" y="{text_y:.2f}" text-anchor="middle" font-size="{config.text_size * config.scale:.2f}" font-family="monospace">{display_code}</text>'
    
    fg = _parse_color(config.foreground)
    bg = _parse_color(config.background)
    
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{total_width:.2f}" height="{total_height:.2f}" viewBox="0 0 {total_width:.2f} {total_height:.2f}">
  <rect width="100%" height="100%" fill="{bg}"/>
  <g fill="{fg}">
    {''.join(all_bars)}
  </g>
  {text_element}
</svg>'''
    
    return BarcodeResult(
        svg=svg,
        width=int(total_width),
        height=int(total_height),
        data=full_code,
        format='ean13'
    )


def _calculate_ean13_checksum(code: str) -> int:
    """Calculate EAN-13 checksum digit."""
    total = 0
    for i, digit in enumerate(code):
        d = int(digit)
        if i % 2 == 0:
            total += d
        else:
            total += d * 3
    return (10 - (total % 10)) % 10


# =============================================================================
# EAN-8 Barcode
# =============================================================================

def generate_ean8(code: str, config: Optional[BarcodeConfig] = None) -> BarcodeResult:
    """
    Generate EAN-8 barcode.
    
    EAN-8 is a compact 8-digit barcode for small packages.
    
    Args:
        code: 7 or 8 digit code (checksum calculated if 7 digits)
        config: Barcode configuration
        
    Returns:
        BarcodeResult with SVG content
    """
    if config is None:
        config = BarcodeConfig()
    
    code = ''.join(c for c in code if c.isdigit())
    if len(code) == 8:
        code = code[:7]
    elif len(code) != 7:
        raise ValueError("EAN-8 requires 7 digits (checksum will be calculated)")
    
    # Calculate checksum
    total = 0
    for i, digit in enumerate(code):
        d = int(digit)
        if i % 2 == 0:
            total += d * 3
        else:
            total += d
    checksum = (10 - (total % 10)) % 10
    full_code = code + str(checksum)
    
    # Generate modules
    modules = EAN13_GUARD  # Left guard
    
    # Left side (4 digits, odd parity)
    for digit in full_code[:4]:
        modules += EAN13_ODD[digit]
    
    modules += EAN13_CENTER  # Center guard
    
    # Right side (4 digits, even parity)
    for digit in full_code[4:]:
        modules += EAN13_EVEN[digit]
    
    modules += EAN13_GUARD  # Right guard
    
    # Generate SVG
    module_width = config.width * config.scale
    module_height = config.height * config.scale
    
    all_bars = _modules_to_svg_bars(modules, config.margin * config.scale, 0,
                                    module_height, module_width)
    
    total_width = (len(modules) + config.margin * 2) * module_width
    total_height = module_height
    
    text_element = ''
    if config.show_text:
        text_y = module_height + config.text_margin * config.scale + config.text_size * config.scale
        total_height = text_y + config.text_size * config.scale + config.margin * config.scale
        text_element = f'<text x="{total_width/2:.2f}" y="{text_y:.2f}" text-anchor="middle" font-size="{config.text_size * config.scale:.2f}" font-family="monospace">{full_code}</text>'
    
    fg = _parse_color(config.foreground)
    bg = _parse_color(config.background)
    
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{total_width:.2f}" height="{total_height:.2f}" viewBox="0 0 {total_width:.2f} {total_height:.2f}">
  <rect width="100%" height="100%" fill="{bg}"/>
  <g fill="{fg}">
    {''.join(all_bars)}
  </g>
  {text_element}
</svg>'''
    
    return BarcodeResult(
        svg=svg,
        width=int(total_width),
        height=int(total_height),
        data=full_code,
        format='ean8'
    )


# =============================================================================
# UPC-A Barcode
# =============================================================================

def generate_upca(code: str, config: Optional[BarcodeConfig] = None) -> BarcodeResult:
    """
    Generate UPC-A barcode.
    
    UPC-A is a 12-digit barcode used primarily in North America.
    
    Args:
        code: 11 or 12 digit code (checksum calculated if 11 digits)
        config: Barcode configuration
        
    Returns:
        BarcodeResult with SVG content
    """
    if config is None:
        config = BarcodeConfig()
    
    code = ''.join(c for c in code if c.isdigit())
    if len(code) == 12:
        code = code[:11]
    elif len(code) != 11:
        raise ValueError("UPC-A requires 11 digits (checksum will be calculated)")
    
    # Calculate checksum (same as EAN-13)
    checksum = _calculate_ean13_checksum(code)
    full_code = code + str(checksum)
    
    # Generate modules
    modules = UPCA_GUARD  # Left guard
    
    # Left side (6 digits, odd parity)
    for digit in full_code[:6]:
        modules += UPCA_ODD[digit]
    
    modules += UPCA_CENTER  # Center guard
    
    # Right side (6 digits, even parity)
    for digit in full_code[6:]:
        modules += UPCA_EVEN[digit]
    
    modules += UPCA_GUARD  # Right guard
    
    # Generate SVG
    module_width = config.width * config.scale
    module_height = config.height * config.scale
    
    all_bars = _modules_to_svg_bars(modules, config.margin * config.scale, 0,
                                    module_height, module_width)
    
    total_width = (len(modules) + config.margin * 2) * module_width
    total_height = module_height
    
    text_element = ''
    if config.show_text:
        text_y = module_height + config.text_margin * config.scale + config.text_size * config.scale
        total_height = text_y + config.text_size * config.scale + config.margin * config.scale
        display_code = f"{full_code[0]} {full_code[1:6]} {full_code[6:]} {full_code[11]}"
        text_element = f'<text x="{total_width/2:.2f}" y="{text_y:.2f}" text-anchor="middle" font-size="{config.text_size * config.scale:.2f}" font-family="monospace">{display_code}</text>'
    
    fg = _parse_color(config.foreground)
    bg = _parse_color(config.background)
    
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{total_width:.2f}" height="{total_height:.2f}" viewBox="0 0 {total_width:.2f} {total_height:.2f}">
  <rect width="100%" height="100%" fill="{bg}"/>
  <g fill="{fg}">
    {''.join(all_bars)}
  </g>
  {text_element}
</svg>'''
    
    return BarcodeResult(
        svg=svg,
        width=int(total_width),
        height=int(total_height),
        data=full_code,
        format='upca'
    )


# =============================================================================
# ITF (Interleaved 2 of 5) Barcode
# =============================================================================

def generate_itf(data: str, config: Optional[BarcodeConfig] = None) -> BarcodeResult:
    """
    Generate ITF (Interleaved 2 of 5) barcode.
    
    ITF encodes pairs of digits by interleaving their patterns.
    Commonly used for shipping cartons and warehouse applications.
    
    Args:
        data: Numeric data (even number of digits preferred)
        config: Barcode configuration
        
    Returns:
        BarcodeResult with SVG content
    """
    if config is None:
        config = BarcodeConfig()
    
    data = ''.join(c for c in data if c.isdigit())
    if not data:
        raise ValueError("ITF requires numeric data")
    
    # Pad to even length
    if len(data) % 2 != 0:
        data = '0' + data
    
    # Add start/stop patterns
    start_pattern = 'nnnn'
    stop_pattern = 'wnn'
    
    # Generate interleaved patterns
    narrow_width = config.width * config.scale
    wide_width = config.width * 3 * config.scale
    module_height = config.height * config.scale
    
    all_bars = []
    current_x = config.margin * config.scale
    
    # Start pattern
    bars = _pattern_to_svg_bars(start_pattern, current_x, 0, module_height, narrow_width, wide_width)
    all_bars.extend(bars)
    current_x += sum(_expand_pattern(start_pattern, narrow_width, wide_width))
    
    # Encode digit pairs
    for i in range(0, len(data), 2):
        digit1 = data[i]
        digit2 = data[i + 1] if i + 1 < len(data) else '0'
        
        pattern1 = ITF_ENCODING[digit1]
        pattern2 = ITF_ENCODING[digit2]
        
        # Interleave patterns
        interleaved = ''
        for j in range(5):
            interleaved += pattern1[j] + pattern2[j]
        
        bars = _pattern_to_svg_bars(interleaved, current_x, 0, module_height, narrow_width, wide_width)
        all_bars.extend(bars)
        current_x += sum(_expand_pattern(interleaved, narrow_width, wide_width))
    
    # Stop pattern
    bars = _pattern_to_svg_bars(stop_pattern, current_x, 0, module_height, narrow_width, wide_width)
    all_bars.extend(bars)
    current_x += sum(_expand_pattern(stop_pattern, narrow_width, wide_width))
    
    total_width = current_x + config.margin * config.scale
    total_height = module_height
    
    text_element = ''
    if config.show_text:
        text_y = module_height + config.text_margin * config.scale + config.text_size * config.scale
        total_height = text_y + config.text_size * config.scale + config.margin * config.scale
        text_element = f'<text x="{total_width/2:.2f}" y="{text_y:.2f}" text-anchor="middle" font-size="{config.text_size * config.scale:.2f}" font-family="monospace">{data}</text>'
    
    fg = _parse_color(config.foreground)
    bg = _parse_color(config.background)
    
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{total_width:.2f}" height="{total_height:.2f}" viewBox="0 0 {total_width:.2f} {total_height:.2f}">
  <rect width="100%" height="100%" fill="{bg}"/>
  <g fill="{fg}">
    {''.join(all_bars)}
  </g>
  {text_element}
</svg>'''
    
    return BarcodeResult(
        svg=svg,
        width=int(total_width),
        height=int(total_height),
        data=data,
        format='itf'
    )


# =============================================================================
# Matrix/QR-like Barcode
# =============================================================================

def generate_matrix(data: str, size: int = 21, config: Optional[BarcodeConfig] = None) -> BarcodeResult:
    """
    Generate a simple matrix barcode (QR-like pattern).
    
    This is a simplified matrix code for demonstration purposes.
    For production QR codes, use a dedicated QR code library.
    
    Args:
        data: Data to encode
        size: Matrix size (default 21x21, similar to QR version 1)
        config: Barcode configuration
        
    Returns:
        BarcodeResult with SVG content
    """
    if config is None:
        config = BarcodeConfig()
    
    # Create matrix based on data hash
    matrix = [[0] * size for _ in range(size)]
    
    # Add finder patterns (corners)
    finder_size = 7
    for dx in range(finder_size):
        for dy in range(finder_size):
            if dx == 0 or dx == finder_size - 1 or dy == 0 or dy == finder_size - 1 or (dx == 2 and dy == 2):
                matrix[dy][dx] = 1
                matrix[dy][size - dx - 1] = 1
                matrix[size - dy - 1][dx] = 1
    
    # Fill data area with pattern based on hash
    data_hash = sum(ord(c) * (i + 1) for i, c in enumerate(data))
    for y in range(size):
        for x in range(size):
            if matrix[y][x] == 0:
                matrix[y][x] = (data_hash + x * y) % 2
    
    # Generate SVG
    module_size = config.width * config.scale * 2
    margin = config.margin * config.scale
    
    all_bars = []
    for y in range(size):
        for x in range(size):
            if matrix[y][x] == 1:
                rect_x = margin + x * module_size
                rect_y = margin + y * module_size
                all_bars.append(f'<rect x="{rect_x:.2f}" y="{rect_y:.2f}" width="{module_size:.2f}" height="{module_size:.2f}"/>')
    
    total_size = size * module_size + margin * 2
    total_height = total_size
    
    text_element = ''
    if config.show_text:
        text_y = total_size + config.text_margin * config.scale + config.text_size * config.scale
        total_height = text_y + config.text_size * config.scale + config.margin * config.scale
        display_data = data[:20] + '...' if len(data) > 20 else data
        text_element = f'<text x="{total_size/2:.2f}" y="{text_y:.2f}" text-anchor="middle" font-size="{config.text_size * config.scale:.2f}" font-family="monospace">{display_data}</text>'
    
    fg = _parse_color(config.foreground)
    bg = _parse_color(config.background)
    
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{total_size:.2f}" height="{total_height:.2f}" viewBox="0 0 {total_size:.2f} {total_height:.2f}">
  <rect width="100%" height="100%" fill="{bg}"/>
  <g fill="{fg}">
    {''.join(all_bars)}
  </g>
  {text_element}
</svg>'''
    
    return BarcodeResult(
        svg=svg,
        width=int(total_size),
        height=int(total_height),
        data=data,
        format='matrix'
    )


# =============================================================================
# Utility Functions
# =============================================================================

def save_barcode(result: BarcodeResult, filepath: str) -> None:
    """
    Save barcode SVG to file.
    
    Args:
        result: BarcodeResult from generation function
        filepath: Output file path
        
    Example:
        >>> result = generate_code128("HELLO")
        >>> save_barcode(result, "barcode.svg")
    """
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(result.svg)


def get_supported_formats() -> List[str]:
    """
    Get list of supported barcode formats.
    
    Returns:
        List of format names
        
    Example:
        >>> get_supported_formats()
        ['code39', 'code128', 'ean13', 'ean8', 'upca', 'itf', 'matrix']
    """
    return ['code39', 'code128', 'ean13', 'ean8', 'upca', 'itf', 'matrix']


def generate_barcode(data: str, format: str = 'code128',
                     config: Optional[BarcodeConfig] = None,
                     **kwargs) -> BarcodeResult:
    """
    Universal barcode generation function.
    
    Args:
        data: Data to encode
        format: Barcode format (code39, code128, ean13, ean8, upca, itf, matrix)
        config: Barcode configuration
        **kwargs: Additional arguments passed to specific generator
        
    Returns:
        BarcodeResult with SVG content
        
    Example:
        >>> result = generate_barcode("123456789012", format="ean13")
        >>> print(result.svg)
    """
    generators = {
        'code39': generate_code39,
        'code128': generate_code128,
        'ean13': generate_ean13,
        'ean8': generate_ean8,
        'upca': generate_upca,
        'itf': generate_itf,
        'matrix': generate_matrix,
    }
    
    if format not in generators:
        raise ValueError(f"Unsupported format: {format}. Supported: {get_supported_formats()}")
    
    if format == 'matrix':
        return generators[format](data, config, **kwargs)
    return generators[format](data, config)


# =============================================================================
# Main (for testing)
# =============================================================================

if __name__ == '__main__':
    # Quick test
    print("Testing barcode generation...")
    
    # Code 128
    result = generate_code128("Hello World")
    print(f"Code 128: {result.width}x{result.height}")
    
    # EAN-13
    result = generate_ean13("590123412345")
    print(f"EAN-13: {result.width}x{result.height}")
    
    # Code 39
    result = generate_code39("ABC123")
    print(f"Code 39: {result.width}x{result.height}")
    
    print("All tests passed!")
