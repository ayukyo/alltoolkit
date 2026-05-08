#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Steganography Utilities Module
============================================
A comprehensive steganography utility module for Python with zero external dependencies.

Features:
    - Zero-width character steganography (hide data in text using invisible Unicode)
    - Whitespace steganography (encode data using spaces and tabs)
    - Case-based steganography (hide data using letter case variations)
    - Unicode variation selector steganography
    - Support for encoding and decoding hidden messages
    - Detection and analysis of steganographic content

Author: AllToolkit Contributors
License: MIT
"""

from typing import Tuple, List, Optional
import re


# ============================================================================
# Constants
# ============================================================================

# Zero-width Unicode characters for steganography
ZERO_WIDTH_SPACE = '\u200B'          # Zero-width space
ZERO_WIDTH_NON_JOINER = '\u200C'    # Zero-width non-joiner
ZERO_WIDTH_JOINER = '\u200D'         # Zero-width joiner
LEFT_TO_RIGHT_MARK = '\u200E'        # Left-to-right mark
RIGHT_TO_LEFT_MARK = '\u200F'        # Right-to-left mark

# Binary encoding using zero-width characters
ZW_BINARY_MAP = {
    '0': ZERO_WIDTH_SPACE,
    '1': ZERO_WIDTH_NON_JOINER,
}

ZW_BINARY_REVERSE = {
    ZERO_WIDTH_SPACE: '0',
    ZERO_WIDTH_NON_JOINER: '1',
}

# Whitespace encoding
WS_SPACE = ' '                       # Regular space
WS_TAB = '\t'                        # Tab character

# Whitespace binary mapping
WS_BINARY_MAP = {
    '0': WS_SPACE,
    '1': WS_TAB,
}

WS_BINARY_REVERSE = {
    WS_SPACE: '0',
    WS_TAB: '1',
}

# Unicode variation selectors for steganography (VS1-VS16)
VARIATION_SELECTORS = [chr(0xFE00 + i) for i in range(16)]


# ============================================================================
# Utility Functions
# ============================================================================

def text_to_binary(text: str, encoding: str = 'utf-8') -> str:
    """
    Convert text to binary string representation.
    
    Args:
        text: Text to convert
        encoding: Character encoding (default: utf-8)
    
    Returns:
        Binary string representation
    
    Examples:
        >>> text_to_binary('AB')
        '0100000101000010'
        >>> text_to_binary('Hi')
        '0100100001101001'
    """
    byte_data = text.encode(encoding)
    return ''.join(format(byte, '08b') for byte in byte_data)


def binary_to_text(binary: str, encoding: str = 'utf-8') -> str:
    """
    Convert binary string to text.
    
    Args:
        binary: Binary string representation
        encoding: Character encoding (default: utf-8)
    
    Returns:
        Decoded text
    
    Raises:
        ValueError: If binary string is invalid
    
    Examples:
        >>> binary_to_text('0100000101000010')
        'AB'
        >>> binary_to_text('0100100001101001')
        'Hi'
    """
    if len(binary) % 8 != 0:
        raise ValueError(f"Binary string length must be multiple of 8, got {len(binary)}")
    
    # Pad with leading zeros if needed (shouldn't happen with proper input)
    if binary:
        byte_list = [binary[i:i+8] for i in range(0, len(binary), 8)]
        try:
            byte_data = bytes(int(b, 2) for b in byte_list)
            return byte_data.decode(encoding)
        except (ValueError, UnicodeDecodeError) as e:
            raise ValueError(f"Failed to decode binary: {e}")
    return ''


def _extract_zero_width_chars(text: str) -> str:
    """
    Extract all zero-width characters from text.
    
    Args:
        text: Text to extract from
    
    Returns:
        String of zero-width characters only
    """
    return ''.join(c for c in text if c in ZW_BINARY_REVERSE)


def _extract_variation_selectors(text: str) -> str:
    """
    Extract all variation selector characters from text.
    
    Args:
        text: Text to extract from
    
    Returns:
        String of variation selector characters only
    """
    return ''.join(c for c in text if c in VARIATION_SELECTORS)


# ============================================================================
# Zero-Width Character Steganography
# ============================================================================

def encode_zw_steganography(cover_text: str, secret_message: str, 
                           encoding: str = 'utf-8') -> str:
    """
    Hide a secret message inside cover text using zero-width characters.
    
    The secret message is converted to binary, then each binary digit
    is encoded as a zero-width character:
    - '0' -> Zero-width space (U+200B)
    - '1' -> Zero-width non-joiner (U+200C)
    
    The hidden characters are appended after the cover text, appearing
    as an invisible suffix.
    
    Args:
        cover_text: Visible cover text
        secret_message: Message to hide
        encoding: Character encoding for the secret (default: utf-8)
    
    Returns:
        Cover text with hidden message (invisible to naked eye)
    
    Examples:
        >>> result = encode_zw_steganography('Hello World', 'Hi')
        >>> len(result) > len('Hello World')
        True
        >>> decode_zw_steganography(result)
        'Hi'
    """
    # Convert secret message to binary
    binary_data = text_to_binary(secret_message, encoding)
    
    # Encode binary as zero-width characters
    hidden_chars = ''.join(ZW_BINARY_MAP[b] for b in binary_data)
    
    # Add a marker at the end (zero-width joiner) to mark message end
    hidden_chars += ZERO_WIDTH_JOINER
    
    return cover_text + hidden_chars


def decode_zw_steganography(stego_text: str, encoding: str = 'utf-8') -> str:
    """
    Extract hidden message from steganographic text.
    
    Args:
        stego_text: Text with hidden message
        encoding: Character encoding (default: utf-8)
    
    Returns:
        Hidden message, or empty string if none found
    
    Examples:
        >>> stego = encode_zw_steganography('Hello', 'Secret')
        >>> decode_zw_steganography(stego)
        'Secret'
        >>> decode_zw_steganography('No hidden message')
        ''
    """
    # Extract zero-width characters
    zw_chars = _extract_zero_width_chars(stego_text)
    
    # Find the end marker (zero-width joiner)
    end_marker_pos = stego_text.find(ZERO_WIDTH_JOINER)
    
    if end_marker_pos == -1:
        # No end marker found, try to decode all zero-width chars
        if not zw_chars:
            return ''
        binary_data = ''.join(ZW_BINARY_REVERSE.get(c, '') for c in zw_chars)
    else:
        # Extract only the encoded part (before the end marker)
        stego_part = stego_text[:end_marker_pos]
        zw_chars = _extract_zero_width_chars(stego_part)
        if not zw_chars:
            return ''
        binary_data = ''.join(ZW_BINARY_REVERSE.get(c, '') for c in zw_chars)
    
    if not binary_data:
        return ''
    
    # Convert binary to text
    try:
        return binary_to_text(binary_data, encoding)
    except ValueError:
        return ''


def detect_zw_steganography(text: str) -> Tuple[bool, int, Optional[str]]:
    """
    Detect if text contains zero-width steganography.
    
    Args:
        text: Text to analyze
    
    Returns:
        Tuple of (detected: bool, char_count: int, hidden_message: Optional[str])
    
    Examples:
        >>> stego = encode_zw_steganography('Hello', 'Secret')
        >>> detected, count, msg = detect_zw_steganography(stego)
        >>> detected
        True
        >>> msg
        'Secret'
    """
    zw_chars = _extract_zero_width_chars(text)
    char_count = len(zw_chars)
    
    if char_count == 0:
        return False, 0, None
    
    # Check for end marker
    has_marker = ZERO_WIDTH_JOINER in text
    
    if has_marker:
        try:
            hidden = decode_zw_steganography(text)
            return True, char_count, hidden
        except Exception:
            return True, char_count, None
    
    return True, char_count, None


def remove_zw_steganography(text: str) -> str:
    """
    Remove all zero-width steganography characters from text.
    
    Args:
        text: Text with potential hidden content
    
    Returns:
        Cleaned text without zero-width characters
    
    Examples:
        >>> stego = encode_zw_steganography('Hello', 'Secret')
        >>> clean = remove_zw_steganography(stego)
        >>> clean
        'Hello'
    """
    # Remove all zero-width characters
    return ''.join(c for c in text if c not in ZW_BINARY_REVERSE and c != ZERO_WIDTH_JOINER)


# ============================================================================
# Whitespace Steganography
# ============================================================================

# Whitespace end marker: sequence that signals message end
WS_END_MARKER = '\n\n'


def encode_whitespace_steganography(cover_text: str, secret_message: str,
                                   encoding: str = 'utf-8') -> str:
    """
    Hide a secret message using trailing whitespace.
    
    Each bit of the secret is encoded as:
    - '0' -> Space character
    - '1' -> Tab character
    
    A double newline marker is added to indicate message boundaries.
    
    Args:
        cover_text: Visible cover text
        secret_message: Message to hide
        encoding: Character encoding (default: utf-8)
    
    Returns:
        Cover text with trailing whitespace containing hidden message
    
    Examples:
        >>> result = encode_whitespace_steganography('Hello', 'Hi')
        >>> decode_whitespace_steganography(result)
        'Hi'
    """
    # Convert secret message to binary
    binary_data = text_to_binary(secret_message, encoding)
    
    # Encode binary as whitespace
    hidden_whitespace = ''.join(WS_BINARY_MAP[b] for b in binary_data)
    
    # Add double newline as end marker
    return cover_text + hidden_whitespace + WS_END_MARKER


def decode_whitespace_steganography(stego_text: str, encoding: str = 'utf-8') -> str:
    """
    Extract hidden message from whitespace steganography.
    
    Args:
        stego_text: Text with hidden whitespace message
        encoding: Character encoding (default: utf-8)
    
    Returns:
        Hidden message, or empty string if none found
    
    Examples:
        >>> stego = encode_whitespace_steganography('Hello', 'Secret')
        >>> decode_whitespace_steganography(stego)
        'Secret'
    """
    # Find the end marker position
    end_marker_pos = stego_text.find(WS_END_MARKER)
    
    if end_marker_pos == -1:
        return ''
    
    # Extract the encoded whitespace (between cover text and end marker)
    encoded_part = stego_text[:end_marker_pos]
    
    # Find where the cover text ends - look for the start of pure whitespace
    # The encoded whitespace should be at the end of the string before the marker
    
    # Collect all whitespace characters from the end
    whitespace_chars = []
    for i in range(len(encoded_part) - 1, -1, -1):
        char = encoded_part[i]
        if char in (WS_SPACE, WS_TAB):
            whitespace_chars.append(char)
        else:
            break
    
    if not whitespace_chars:
        return ''
    
    # Reverse to get correct order
    whitespace_chars = whitespace_chars[::-1]
    
    # Convert whitespace to binary
    binary_data = ''.join(WS_BINARY_REVERSE.get(c, '') for c in whitespace_chars)
    
    if not binary_data:
        return ''
    
    # Convert binary to text
    try:
        return binary_to_text(binary_data, encoding)
    except ValueError:
        return ''


def detect_whitespace_steganography(text: str) -> Tuple[bool, int, Optional[str]]:
    """
    Detect if text contains whitespace steganography.
    
    Args:
        text: Text to analyze
    
    Returns:
        Tuple of (detected: bool, ws_count: int, hidden_message: Optional[str])
    
    Examples:
        >>> stego = encode_whitespace_steganography('Hello', 'Secret')
        >>> detected, count, msg = detect_whitespace_steganography(stego)
        >>> detected
        True
    """
    # Check for end marker
    if WS_END_MARKER not in text:
        return False, 0, None
    
    end_marker_pos = text.find(WS_END_MARKER)
    
    # Extract the encoded whitespace
    encoded_part = text[:end_marker_pos]
    
    # Count trailing whitespace characters
    ws_count = 0
    for i in range(len(encoded_part) - 1, -1, -1):
        if encoded_part[i] in (WS_SPACE, WS_TAB):
            ws_count += 1
        else:
            break
    
    if ws_count == 0:
        return False, 0, None
    
    # Try to decode
    try:
        hidden = decode_whitespace_steganography(text)
        if hidden:
            return True, ws_count, hidden
    except Exception:
        pass
    
    return True, ws_count, None


def remove_whitespace_steganography(text: str) -> str:
    """
    Remove trailing whitespace steganography from text.
    
    Args:
        text: Text with potential whitespace steganography
    
    Returns:
        Cleaned text without hidden whitespace
    
    Examples:
        >>> stego = encode_whitespace_steganography('Hello', 'Secret')
        >>> clean = remove_whitespace_steganography(stego)
        >>> clean
        'Hello'
    """
    # Find the end marker
    end_marker_pos = text.find(WS_END_MARKER)
    
    if end_marker_pos == -1:
        # No marker, return text stripped of trailing whitespace
        return text.rstrip()
    
    # Get the cover text part (before encoded whitespace)
    cover_part = text[:end_marker_pos]
    
    # Remove trailing whitespace from cover
    cover_text = cover_part.rstrip()
    
    return cover_text


# ============================================================================
# Case-Based Steganography
# ============================================================================

def encode_case_steganography(cover_text: str, secret_message: str,
                              encoding: str = 'utf-8') -> str:
    """
    Hide a secret message using letter case variations.
    
    The secret message is encoded by modifying the case of alphabetic
    characters in the cover text:
    - Lowercase -> bit 0
    - Uppercase -> bit 1
    
    Args:
        cover_text: Cover text (must have enough alphabetic characters)
        secret_message: Message to hide
        encoding: Character encoding (default: utf-8)
    
    Returns:
        Cover text with modified case containing hidden message
    
    Raises:
        ValueError: If cover text doesn't have enough alphabetic characters
    
    Examples:
        >>> result = encode_case_steganography('hello world', 'A')
        >>> len(result) == len('hello world')
        True
    """
    # Convert secret message to binary
    binary_data = text_to_binary(secret_message, encoding)
    
    # Count alphabetic characters in cover text
    alpha_chars = [i for i, c in enumerate(cover_text) if c.isalpha()]
    
    if len(alpha_chars) < len(binary_data):
        raise ValueError(
            f"Cover text needs at least {len(binary_data)} alphabetic characters, "
            f"but has only {len(alpha_chars)}"
        )
    
    # Build result with case modifications
    result = list(cover_text)
    for i, bit in enumerate(binary_data):
        idx = alpha_chars[i]
        char = cover_text[idx]
        if bit == '1':
            result[idx] = char.upper()
        else:
            result[idx] = char.lower()
    
    return ''.join(result)


def decode_case_steganography(stego_text: str, message_length: int,
                              encoding: str = 'utf-8') -> str:
    """
    Extract hidden message from case-based steganography.
    
    Args:
        stego_text: Text with hidden case message
        message_length: Expected length of the decoded message in characters
        encoding: Character encoding (default: utf-8)
    
    Returns:
        Hidden message
    
    Examples:
        >>> stego = encode_case_steganography('hello world', 'Hi')
        >>> decode_case_steganography(stego, 2)
        'Hi'
    """
    # Extract bits from case
    bits = []
    for char in stego_text:
        if char.isalpha():
            bits.append('1' if char.isupper() else '0')
    
    # Need enough bits for the message (8 bits per character)
    required_bits = message_length * 8
    
    if len(bits) < required_bits:
        raise ValueError(
            f"Need {required_bits} bits for {message_length} characters, "
            f"but only found {len(bits)} alphabetic characters"
        )
    
    binary_data = ''.join(bits[:required_bits])
    
    return binary_to_text(binary_data, encoding)


def auto_decode_case_steganography(stego_text: str, encoding: str = 'utf-8') -> str:
    """
    Attempt to automatically decode case-based steganography.
    
    This function tries different message lengths and validates the output.
    Best used when the message structure is unknown.
    
    Args:
        stego_text: Text with potential hidden message
        encoding: Character encoding (default: utf-8)
    
    Returns:
        Most likely hidden message, or empty string if none detected
    
    Examples:
        >>> stego = encode_case_steganography('abcdefghij', 'X')
        >>> auto_decode_case_steganography(stego)
        'X'
    """
    alpha_count = sum(1 for c in stego_text if c.isalpha())
    
    if alpha_count < 8:
        return ''
    
    # Try different message lengths (from 1 up to max possible)
    max_chars = alpha_count // 8
    
    for length in range(1, min(max_chars + 1, 100)):  # Limit to reasonable lengths
        try:
            result = decode_case_steganography(stego_text, length, encoding)
            # Check if result contains printable characters
            if result and all(c.isprintable() or c.isspace() for c in result):
                return result
        except (ValueError, UnicodeDecodeError):
            continue
    
    return ''


# ============================================================================
# Variation Selector Steganography
# ============================================================================

def encode_variation_selector_steganography(cover_text: str, secret_message: str,
                                           encoding: str = 'utf-8') -> str:
    """
    Hide a secret message using Unicode variation selectors.
    
    Each nibble (4 bits) of the secret is encoded as a variation selector
    (U+FE00 to U+FE0F), which are invisible characters that typically
    modify preceding glyphs.
    
    Args:
        cover_text: Cover text
        secret_message: Message to hide
        encoding: Character encoding (default: utf-8)
    
    Returns:
        Cover text with variation selectors inserted
    
    Examples:
        >>> result = encode_variation_selector_steganography('Hello', 'Hi')
        >>> len(result) > len('Hello')
        True
        >>> decode_variation_selector_steganography(result)
        'Hi'
    """
    # Convert secret message to binary
    binary_data = text_to_binary(secret_message, encoding)
    
    # Pad to multiple of 4 bits (nibbles)
    while len(binary_data) % 4 != 0:
        binary_data += '0'
    
    # Split into nibbles and convert to variation selectors
    vs_chars = []
    for i in range(0, len(binary_data), 4):
        nibble = binary_data[i:i+4]
        vs_index = int(nibble, 2)
        vs_chars.append(VARIATION_SELECTORS[vs_index])
    
    # Add end marker (use all 1s pattern - variation selector 15)
    vs_chars.append(VARIATION_SELECTORS[15])
    vs_chars.append(VARIATION_SELECTORS[15])
    
    # Insert after each character of cover text
    result = []
    for i, char in enumerate(cover_text):
        result.append(char)
        if i < len(vs_chars):
            result.append(vs_chars[i])
    
    # Add remaining variation selectors at the end
    if len(vs_chars) > len(cover_text):
        result.extend(vs_chars[len(cover_text):])
    
    return ''.join(result)


def decode_variation_selector_steganography(stego_text: str,
                                           encoding: str = 'utf-8') -> str:
    """
    Extract hidden message from variation selector steganography.
    
    Args:
        stego_text: Text with hidden variation selectors
        encoding: Character encoding (default: utf-8)
    
    Returns:
        Hidden message, or empty string if none found
    
    Examples:
        >>> stego = encode_variation_selector_steganography('Hello', 'Secret')
        >>> decode_variation_selector_steganography(stego)
        'Secret'
    """
    # Extract variation selectors
    vs_chars = _extract_variation_selectors(stego_text)
    
    if len(vs_chars) < 2:
        return ''
    
    # Find end marker (two consecutive VS15)
    end_marker = VARIATION_SELECTORS[15] + VARIATION_SELECTORS[15]
    end_pos = vs_chars.find(end_marker)
    
    if end_pos == -1:
        return ''
    
    # Extract data before end marker
    data_vs = vs_chars[:end_pos]
    
    if not data_vs:
        return ''
    
    # Convert variation selectors to nibbles
    binary_data = ''
    for vs in data_vs:
        nibble_index = VARIATION_SELECTORS.index(vs)
        binary_data += format(nibble_index, '04b')
    
    # Convert binary to text
    try:
        return binary_to_text(binary_data, encoding)
    except ValueError:
        return ''


# ============================================================================
# Detection and Analysis
# ============================================================================

def analyze_steganography(text: str) -> dict:
    """
    Analyze text for potential steganographic content.
    
    Performs comprehensive analysis for various steganography methods.
    
    Args:
        text: Text to analyze
    
    Returns:
        Dictionary with analysis results
    
    Examples:
        >>> stego = encode_zw_steganography('Hello', 'Secret')
        >>> result = analyze_steganography(stego)
        >>> result['zero_width']['detected']
        True
    """
    results = {
        'zero_width': {
            'detected': False,
            'char_count': 0,
            'message': None,
        },
        'whitespace': {
            'detected': False,
            'ws_count': 0,
            'message': None,
        },
        'variation_selectors': {
            'detected': False,
            'char_count': 0,
            'message': None,
        },
        'suspicious': False,
        'total_hidden_chars': 0,
    }
    
    # Check zero-width steganography
    zw_detected, zw_count, zw_msg = detect_zw_steganography(text)
    results['zero_width']['detected'] = zw_detected
    results['zero_width']['char_count'] = zw_count
    results['zero_width']['message'] = zw_msg
    
    # Check whitespace steganography
    ws_detected, ws_count, ws_msg = detect_whitespace_steganography(text)
    results['whitespace']['detected'] = ws_detected
    results['whitespace']['ws_count'] = ws_count
    results['whitespace']['message'] = ws_msg
    
    # Check variation selectors
    vs_chars = _extract_variation_selectors(text)
    vs_count = len(vs_chars)
    if vs_count > 0:
        results['variation_selectors']['detected'] = True
        results['variation_selectors']['char_count'] = vs_count
        results['variation_selectors']['message'] = decode_variation_selector_steganography(text)
    
    # Calculate totals
    results['total_hidden_chars'] = zw_count + ws_count + vs_count
    results['suspicious'] = (
        zw_detected or ws_detected or vs_count > len(text) * 0.1
    )
    
    return results


def clean_all_steganography(text: str) -> str:
    """
    Remove all known steganographic content from text.
    
    Args:
        text: Text to clean
    
    Returns:
        Cleaned text without hidden content
    
    Examples:
        >>> stego = encode_zw_steganography('Hello', 'Secret')
        >>> clean = clean_all_steganography(stego)
        >>> clean
        'Hello'
    """
    # Remove zero-width characters
    result = remove_zw_steganography(text)
    
    # Remove variation selectors
    result = ''.join(c for c in result if c not in VARIATION_SELECTORS)
    
    # Remove trailing whitespace steganography
    result = remove_whitespace_steganography(result)
    
    return result


# ============================================================================
# Capacity Calculation
# ============================================================================

def calculate_zw_capacity(cover_text_length: int, encoding: str = 'utf-8') -> int:
    """
    Calculate maximum message length that can be hidden using zero-width method.
    
    Args:
        cover_text_length: Length of cover text
        encoding: Character encoding (default: utf-8)
    
    Returns:
        Maximum characters that can be hidden
    
    Examples:
        >>> calculate_zw_capacity(100)
        12
    """
    # Each character needs 8 bits + 1 end marker
    # Zero-width chars are appended, so capacity is theoretically unlimited
    # But practical limit is based on output size
    # For typical use, allow roughly 12% of cover text length
    return max(0, cover_text_length // 8)


def calculate_whitespace_capacity(cover_text_length: int, encoding: str = 'utf-8') -> int:
    """
    Calculate maximum message length for whitespace steganography.
    
    Args:
        cover_text_length: Length of cover text
        encoding: Character encoding (default: utf-8)
    
    Returns:
        Maximum characters that can be hidden
    
    Examples:
        >>> calculate_whitespace_capacity(100)
        12
    """
    # Same as zero-width, appended to end
    return max(0, cover_text_length // 8)


def calculate_case_capacity(cover_text: str, encoding: str = 'utf-8') -> int:
    """
    Calculate maximum message length for case-based steganography.
    
    Args:
        cover_text: Cover text (to count alphabetic characters)
        encoding: Character encoding (default: utf-8)
    
    Returns:
        Maximum characters that can be hidden
    
    Examples:
        >>> calculate_case_capacity('Hello World')
        1
        >>> calculate_case_capacity('abcdefghijklmnopqrstuvwxyz')
        3
    """
    alpha_count = sum(1 for c in cover_text if c.isalpha())
    return alpha_count // 8


# ============================================================================
# Main
# ============================================================================

if __name__ == '__main__':
    print("=== Zero-Width Steganography ===")
    cover = "Hello, World!"
    secret = "Hi"
    
    stego = encode_zw_steganography(cover, secret)
    print(f"Cover text: {repr(cover)}")
    print(f"Secret message: {secret}")
    print(f"Stego text (visible): {repr(stego)}")
    print(f"Stego text length: {len(stego)} (cover: {len(cover)})")
    
    decoded = decode_zw_steganography(stego)
    print(f"Decoded message: {decoded}")
    
    detected, count, msg = detect_zw_steganography(stego)
    print(f"Detection: found={detected}, chars={count}, message={msg}")
    
    print("\n=== Whitespace Steganography ===")
    stego_ws = encode_whitespace_steganography(cover, secret)
    print(f"Stego text: {repr(stego_ws)}")
    print(f"Decoded: {decode_whitespace_steganography(stego_ws)}")
    
    print("\n=== Case-Based Steganography ===")
    cover_case = "abcdefghij" * 2
    secret_case = "X"
    stego_case = encode_case_steganography(cover_case, secret_case)
    print(f"Cover: {cover_case}")
    print(f"Stego: {stego_case}")
    print(f"Decoded: {decode_case_steganography(stego_case, len(secret_case))}")
    
    print("\n=== Variation Selector Steganography ===")
    stego_vs = encode_variation_selector_steganography(cover, secret)
    print(f"Stego text length: {len(stego_vs)}")
    print(f"Decoded: {decode_variation_selector_steganography(stego_vs)}")
    
    print("\n=== Analysis ===")
    analysis = analyze_steganography(stego)
    print(f"Analysis: {analysis}")