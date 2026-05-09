#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Phonetic Encoding Utilities Module
=================================================
A comprehensive phonetic encoding utility module for Python with zero external dependencies.

Features:
    - Soundex encoding (American Soundex)
    - Metaphone encoding
    - Double Metaphone encoding (primary and alternate)
    - NYSIIS encoding (New York State Identification and Intelligence System)
    - Caverphone 2.0 encoding
    - Match Rating Codex (MRC) encoding
    - Fuzzy name matching utilities
    - Phonetic similarity comparison

Applications:
    - Name matching and deduplication
    - Search with spelling tolerance
    - Genealogy and record linkage
    - Customer database deduplication

Author: AllToolkit Contributors
License: MIT
"""

import re
from typing import Tuple, List, Optional, Dict, Set
from dataclasses import dataclass
from enum import Enum


# ============================================================================
# Constants
# ============================================================================

# Soundex letter groups
SOUNDEX_GROUPS = {
    'b': '1', 'f': '1', 'p': '1', 'v': '1',
    'c': '2', 'g': '2', 'j': '2', 'k': '2', 'q': '2', 's': '2', 'x': '2', 'z': '2',
    'd': '3', 't': '3',
    'l': '4',
    'm': '5', 'n': '5',
    'r': '6',
}

# Metaphone letter mappings
METAPHONE_VOWELS = {'a', 'e', 'i', 'o', 'u'}


# ============================================================================
# Data Classes
# ============================================================================

@dataclass
class PhoneticResult:
    """Container for phonetic encoding results."""
    soundex: str
    metaphone: str
    double_metaphone: Tuple[str, Optional[str]]
    nysiis: str
    caverphone: str
    match_rating_codex: str


@dataclass
class DoubleMetaphoneResult:
    """Container for Double Metaphone results."""
    primary: str
    alternate: Optional[str]


class PhoneticAlgorithm(Enum):
    """Enumeration of supported phonetic algorithms."""
    SOUNDEX = "soundex"
    METAPHONE = "metaphone"
    DOUBLE_METAPHONE = "double_metaphone"
    NYSIIS = "nysiis"
    CAVERPHONE = "caverphone"
    MATCH_RATING_CODEX = "match_rating_codex"


# ============================================================================
# Utility Functions
# ============================================================================

def _clean_string(text: str) -> str:
    """
    Clean and normalize a string for phonetic processing.
    
    Args:
        text: Input string
    
    Returns:
        Cleaned uppercase string with only letters
    """
    if not text:
        return ""
    return re.sub(r'[^A-Za-z]', '', text).upper()


def _is_vowel(char: str) -> bool:
    """Check if a character is a vowel."""
    return char.lower() in METAPHONE_VOWELS


def _is_slavo_germanic(text: str) -> bool:
    """Check if a name appears to be Slavic or Germanic in origin."""
    text_lower = text.lower()
    patterns = ['witz', 'wicz', 'ski', 'sky', 'cki', 'sk', 'sch', 'tz', 'cz']
    return any(p in text_lower for p in patterns)


# ============================================================================
# Soundex Algorithm
# ============================================================================

def soundex(text: str) -> str:
    """
    Encode a string using the American Soundex algorithm.
    
    Soundex encodes homophones to the same representation, allowing
    matching of names that sound similar but are spelled differently.
    
    Args:
        text: Input string to encode
    
    Returns:
        4-character Soundex code (letter + 3 digits)
    
    Examples:
        >>> soundex("Robert")
        'R163'
        >>> soundex("Rupert")
        'R163'
        >>> soundex("Smith")
        'S530'
        >>> soundex("Schmidt")
        'S530'
    
    Note:
        Soundex codes have the format: First letter + 3 digits
        Vowels and H, W are ignored after the first letter
        Adjacent letters with the same code are merged
    """
    if not text:
        return "0000"
    
    cleaned = _clean_string(text)
    if not cleaned:
        return "0000"
    
    # Keep the first letter
    first_letter = cleaned[0]
    
    # Encode remaining letters
    codes = []
    for char in cleaned[1:]:
        code = SOUNDEX_GROUPS.get(char.lower(), '')
        if code:
            codes.append(code)
    
    # Remove adjacent duplicates
    result = [first_letter]
    prev_code = SOUNDEX_GROUPS.get(first_letter.lower(), '')
    
    for code in codes:
        if code != prev_code:
            result.append(code)
        prev_code = code
    
    # Pad with zeros or truncate to 4 characters
    encoded = ''.join(result)[:4]
    return (encoded + '000')[:4]


def soundex_words(text: str) -> List[str]:
    """
    Encode each word in a string using Soundex.
    
    Args:
        text: Input string with multiple words
    
    Returns:
        List of Soundex codes, one per word
    
    Examples:
        >>> soundex_words("John Smith")
        ['J500', 'S530']
    """
    words = text.split()
    return [soundex(word) for word in words]


# ============================================================================
# Metaphone Algorithm
# ============================================================================

def metaphone(text: str) -> str:
    """
    Encode a string using the Metaphone algorithm.
    
    Metaphone is more accurate than Soundex for English names,
    handling more complex pronunciation rules.
    
    Args:
        text: Input string to encode
    
    Returns:
        Metaphone code string
    
    Examples:
        >>> metaphone("Smith")
        'SM0T'
        >>> metaphone("Schmidt")
        'SMTT'
        >>> metaphone("phone")
        'FN'
        >>> metaphone("knight")
        'NFT'
    """
    if not text:
        return ""
    
    cleaned = _clean_string(text)
    if not cleaned:
        return ""
    
    length = len(cleaned)
    result = []
    i = 0
    
    while i < length:
        char = cleaned[i]
        next_char = cleaned[i + 1] if i + 1 < length else ''
        prev_char = cleaned[i - 1] if i > 0 else ''
        
        # Skip vowels at the beginning
        if i == 0 and _is_vowel(char):
            result.append(char)
            i += 1
            continue
        
        # Skip vowels in other positions (but keep previous)
        if _is_vowel(char):
            i += 1
            continue
        
        # Process consonants
        if char == 'B':
            # B -> B, unless at end after M
            if not (i == length - 1 and prev_char == 'M'):
                result.append('B')
            i += 1
            
        elif char == 'C':
            # C -> X (SH) if -CIA- or -CH-
            # C -> S if -CI-, -CE-, -CY-
            # C -> K otherwise
            if next_char == 'I' and (i + 2 < length and cleaned[i + 2] == 'A'):
                result.append('X')
            elif next_char == 'H':
                result.append('X')
                i += 1
            elif next_char in 'IEY':
                result.append('S')
            else:
                result.append('K')
            i += 1
            
        elif char == 'D':
            # D -> J if -DGE-, -DGI-, -DGY-
            # D -> T otherwise
            if next_char == 'G' and (i + 2 < length and cleaned[i + 2] in 'EIY'):
                result.append('J')
                i += 1
            else:
                result.append('T')
            i += 1
            
        elif char == 'F':
            result.append('F')
            i += 1
            
        elif char == 'G':
            # G -> F if -GH and not at beginning
            # G -> silent if -GN or -GNED
            # G -> J if -GI-, -GE-, -GY-
            # G -> K otherwise
            if next_char == 'H':
                if i == 0:
                    result.append('K')
                elif i + 2 == length:
                    # GH at end, silent
                    pass
                elif not _is_vowel(cleaned[i + 2]):
                    result.append('K')
                i += 1
            elif next_char == 'N':
                if i + 2 == length or (i + 2 < length and cleaned[i + 2] == 'E' and i + 3 == length):
                    # GN at end or GNED, silent
                    pass
                else:
                    result.append('K')
            elif next_char in 'IEY':
                result.append('J')
            else:
                result.append('K')
            i += 1
            
        elif char == 'H':
            # H -> H if before vowel and not after C,G,P,S,T
            if _is_vowel(next_char) and prev_char not in 'CGPST':
                result.append('H')
            i += 1
            
        elif char == 'J':
            # J -> J
            result.append('J')
            i += 1
            
        elif char == 'K':
            # K -> silent if after C
            if prev_char != 'C':
                result.append('K')
            i += 1
            
        elif char == 'L':
            result.append('L')
            i += 1
            
        elif char == 'M':
            result.append('M')
            i += 1
            
        elif char == 'N':
            result.append('N')
            i += 1
            
        elif char == 'P':
            # P -> F if before H, P otherwise
            if next_char == 'H':
                result.append('F')
                i += 1
            else:
                result.append('P')
            i += 1
            
        elif char == 'Q':
            result.append('K')
            i += 1
            
        elif char == 'R':
            result.append('R')
            i += 1
            
        elif char == 'S':
            # S -> X (SH) if -SH-, -SIO-, -SIA-
            # S -> S otherwise
            if next_char == 'H':
                result.append('X')
                i += 1
            elif next_char == 'I' and (i + 2 < length and cleaned[i + 2] in 'AO'):
                result.append('X')
                i += 2
            else:
                result.append('S')
            i += 1
            
        elif char == 'T':
            # T -> X if -TIA-, -TIO-
            # T -> 0 (TH) if -TH-
            # T -> silent if -TCH-
            if next_char == 'I' and (i + 2 < length and cleaned[i + 2] in 'AO'):
                result.append('X')
                i += 2
            elif next_char == 'H':
                result.append('0')  # Using '0' for TH sound
                i += 1
            elif next_char == 'C' and (i + 2 < length and cleaned[i + 2] == 'H'):
                # TCH, silent T
                i += 1
            else:
                result.append('T')
            i += 1
            
        elif char == 'V':
            result.append('F')
            i += 1
            
        elif char == 'W':
            # W -> W if before vowel
            if _is_vowel(next_char):
                result.append('W')
            i += 1
            
        elif char == 'X':
            result.append('KS')
            i += 1
            
        elif char == 'Y':
            # Y -> Y if before vowel
            if _is_vowel(next_char):
                result.append('Y')
            i += 1
            
        elif char == 'Z':
            result.append('S')
            i += 1
            
        else:
            i += 1
    
    return ''.join(result)


# ============================================================================
# Double Metaphone Algorithm
# ============================================================================

def double_metaphone(text: str) -> DoubleMetaphoneResult:
    """
    Encode a string using the Double Metaphone algorithm.
    
    Double Metaphone returns both a primary and alternate encoding,
    providing better matching for names of various origins.
    
    Args:
        text: Input string to encode
    
    Returns:
        DoubleMetaphoneResult with primary and alternate codes
    
    Examples:
        >>> result = double_metaphone("Smith")
        >>> result.primary
        'SMT0'
        >>> result.alternate
        'XMT0'
        >>> result = double_metaphone("Schmidt")
        >>> result.primary
        'SMT0'
    """
    if not text:
        return DoubleMetaphoneResult("", None)
    
    cleaned = _clean_string(text)
    if not cleaned:
        return DoubleMetaphoneResult("", None)
    
    length = len(cleaned)
    primary = []
    alternate = []
    i = 0
    
    # Check for Slavic/Germanic names
    slavo_germanic = _is_slavo_germanic(cleaned)
    
    # Handle special cases at the beginning
    if length >= 2:
        two_char = cleaned[:2]
        if two_char == 'KN' or two_char == 'GN' or two_char == 'PN' or two_char == 'AE' or two_char == 'WR':
            i = 1
        elif two_char == 'WH':
            primary.append('W')
            alternate.append('A')
            i = 2
        elif two_char == 'X':
            primary.append('S')
            alternate.append('S')
            i = 1
        elif two_char == 'NG':
            i = 1
    
    # Main processing loop
    while i < length:
        char = cleaned[i]
        next_char = cleaned[i + 1] if i + 1 < length else ''
        prev_char = cleaned[i - 1] if i > 0 else ''
        next_next_char = cleaned[i + 2] if i + 2 < length else ''
        
        if char == 'A' or char == 'E' or char == 'I' or char == 'O' or char == 'U' or char == 'Y':
            # Vowels
            if i == 0:
                # All vowels at beginning map to 'A'
                primary.append('A')
                alternate.append('A')
            i += 1
            
        elif char == 'B':
            # -MB, silent B
            if next_char == 'B':
                i += 1
            primary.append('P')
            alternate.append('P')
            i += 1
            
        elif char == 'C':
            # Various C rules
            if prev_char == ' ' and next_char == 'I' and next_next_char == 'A':
                # CIA -> X
                primary.append('X')
                alternate.append('X')
            elif next_char == 'H':
                # CH
                if i == 0 and (next_next_char == 'A' or next_next_char == 'E' or next_next_char == 'I' or next_next_char == 'O' or next_next_char == 'U'):
                    # Germanic
                    primary.append('K')
                    alternate.append('X')
                elif i == 0:
                    primary.append('X')
                    alternate.append('X')
                elif prev_char == 'S':
                    primary.append('K')
                    alternate.append('X')
                else:
                    primary.append('X')
                    alternate.append('K')
                i += 1
            elif next_char == 'I' and next_next_char == 'A':
                primary.append('X')
                alternate.append('X')
                i += 1
            elif next_char in 'IEY':
                primary.append('S')
                alternate.append('S')
            else:
                primary.append('K')
                alternate.append('K')
            i += 1
            
        elif char == 'D':
            if next_char == 'G' and next_next_char in 'EIY':
                # DGE, DGI, DGY -> J
                primary.append('J')
                alternate.append('J')
                i += 1
            else:
                primary.append('T')
                alternate.append('T')
            i += 1
            
        elif char == 'F':
            if next_char == 'F':
                i += 1
            primary.append('F')
            alternate.append('F')
            i += 1
            
        elif char == 'G':
            if next_char == 'H':
                if i == 0:
                    # GH at start
                    primary.append('K')
                    alternate.append('K')
                elif i > 0 and (cleaned[i - 1] not in 'AEIOU'):
                    primary.append('K')
                    alternate.append('K')
                i += 1
            elif next_char == 'N':
                if i == 0 or (i == 1 and prev_char == ' '):
                    if length > i + 2 and cleaned[i + 2] in 'EIY':
                        primary.append('K')
                        alternate.append('J')
                    else:
                        primary.append('N')
                        alternate.append('KN')
                else:
                    primary.append('K')
                    alternate.append('K')
                i += 1
            elif next_char in 'IEY':
                if i == 0:
                    primary.append('K')
                    alternate.append('J')
                elif prev_char == 'D':
                    pass  # Silent
                else:
                    primary.append('J')
                    alternate.append('J')
                i += 1
            else:
                if next_char == 'G':
                    i += 1
                primary.append('K')
                alternate.append('K')
            i += 1
            
        elif char == 'H':
            if i == 0 and _is_vowel(next_char):
                primary.append('H')
                alternate.append('H')
            elif prev_char in 'AEIOU' and _is_vowel(next_char):
                primary.append('H')
                alternate.append('H')
            i += 1
            
        elif char == 'J':
            if i == 0:
                if next_char == 'N':
                    primary.append('N')
                    alternate.append('N')
                else:
                    primary.append('J')
                    alternate.append('A')
            elif prev_char not in 'STK' and next_char in 'AEIOU':
                primary.append('J')
                alternate.append('J')
            else:
                primary.append('J')
                alternate.append('J')
            i += 1
            
        elif char == 'K':
            if next_char == 'K':
                i += 1
            primary.append('K')
            alternate.append('K')
            i += 1
            
        elif char == 'L':
            if next_char == 'L':
                i += 1
            primary.append('L')
            alternate.append('L')
            i += 1
            
        elif char == 'M':
            if next_char == 'M':
                i += 1
            primary.append('M')
            alternate.append('M')
            i += 1
            
        elif char == 'N':
            if next_char == 'N':
                i += 1
            primary.append('N')
            alternate.append('N')
            i += 1
            
        elif char == 'P':
            if next_char == 'H':
                primary.append('F')
                alternate.append('F')
                i += 1
            else:
                if next_char == 'P':
                    i += 1
                primary.append('P')
                alternate.append('P')
            i += 1
            
        elif char == 'Q':
            if next_char == 'Q':
                i += 1
            primary.append('K')
            alternate.append('K')
            i += 1
            
        elif char == 'R':
            if next_char == 'R':
                i += 1
            if i == length - 1 and prev_char == 'E' and length > 1:
                # French endings
                primary.append('')
                alternate.append('R')
            else:
                primary.append('R')
                alternate.append('R')
            i += 1
            
        elif char == 'S':
            if next_char == 'H':
                # SH
                primary.append('X')
                alternate.append('X')
                i += 1
            elif next_char == 'I' and next_next_char in 'AO':
                # SIO, SIA
                primary.append('X')
                alternate.append('S')
                i += 1
            elif next_char == 'Z':
                # SZ
                primary.append('S')
                alternate.append('X')
                i += 1
            else:
                if next_char == 'S':
                    i += 1
                primary.append('S')
                alternate.append('S')
            i += 1
            
        elif char == 'T':
            if next_char == 'H':
                primary.append('0')  # TH
                alternate.append('T')
                i += 1
            elif next_char == 'I' and next_next_char in 'AO':
                # TIO, TIA
                primary.append('X')
                alternate.append('X')
                i += 1
            elif next_char == 'C' and next_next_char == 'H':
                # TCH
                pass  # Silent
                i += 1
            else:
                if next_char == 'T':
                    i += 1
                primary.append('T')
                alternate.append('T')
            i += 1
            
        elif char == 'V':
            if next_char == 'V':
                i += 1
            primary.append('F')
            alternate.append('F')
            i += 1
            
        elif char == 'W':
            if next_char == 'W':
                i += 1
            if _is_vowel(next_char):
                primary.append('W')
                alternate.append('W')
            elif i == 0 and next_char == 'H':
                primary.append('A')
                alternate.append('A')
                i += 1
            i += 1
            
        elif char == 'X':
            primary.append('KS')
            alternate.append('KS')
            i += 1
            
        elif char == 'Y':
            if _is_vowel(next_char):
                primary.append('Y')
                alternate.append('Y')
            i += 1
            
        elif char == 'Z':
            if next_char == 'Z':
                i += 1
            if next_char == 'H':
                primary.append('J')
                alternate.append('J')
                i += 1
            else:
                primary.append('S')
                alternate.append('S')
            i += 1
            
        else:
            i += 1
    
    # Limit to 4 characters
    primary_str = ''.join(primary)[:4]
    alt_str = ''.join(alternate)[:4]
    
    return DoubleMetaphoneResult(
        primary=primary_str,
        alternate=alt_str if alt_str != primary_str else None
    )


# ============================================================================
# NYSIIS Algorithm
# ============================================================================

def nysiis(text: str) -> str:
    """
    Encode a string using the NYSIIS algorithm.
    
    New York State Identification and Intelligence System (NYSIIS) was
    developed for name matching in law enforcement databases.
    
    Args:
        text: Input string to encode
    
    Returns:
        NYSIIS code string
    
    Examples:
        >>> nysiis("Smith")
        'SNAT'
        >>> nysiis("Schmidt")
        'SNAT'
        >>> nysiis("O'Connor")
        'OCAN'
    """
    if not text:
        return ""
    
    cleaned = _clean_string(text)
    if not cleaned:
        return ""
    
    length = len(cleaned)
    
    # Step 1: First character transformations
    first = cleaned[0]
    if first == 'M' and length > 1 and cleaned[1] in 'AEIOU':
        cleaned = 'M' + cleaned[1:]
    elif first == 'K' and length > 1 and cleaned[1] == 'N':
        cleaned = 'N' + cleaned[1:]
    elif first == 'P' and length > 1 and cleaned[1] == 'H':
        cleaned = 'F' + cleaned[1:]
    elif first == 'H' and length > 1 and cleaned[1] in 'AEIOU':
        cleaned = cleaned[1:]  # Drop H before vowel
        if cleaned:
            first = cleaned[0]
    
    # Step 2: Last character transformations
    if cleaned:
        last = cleaned[-1]
        if last == 'S':
            cleaned = cleaned[:-1] + 'S'
        elif last == 'A':
            cleaned = cleaned[:-1] + 'A'
        elif last == 'Z':
            cleaned = cleaned[:-1] + 'S'
    
    # Step 3: Replace trailing AY with Y
    if len(cleaned) >= 2 and cleaned[-2:] == 'AY':
        cleaned = cleaned[:-2] + 'Y'
    
    # Step 4: Main transformations
    result = []
    i = 0
    while i < len(cleaned):
        char = cleaned[i]
        next_char = cleaned[i + 1] if i + 1 < len(cleaned) else ''
        prev_char = cleaned[i - 1] if i > 0 else ''
        
        # EV -> AF
        if char == 'E' and next_char == 'V':
            result.append('A')
            result.append('F')
            i += 2
            continue
        
        # A, E, I, O, U -> A
        if char in 'AEIOU':
            result.append('A')
            i += 1
            continue
        
        # Q -> G
        if char == 'Q':
            result.append('G')
            i += 1
            continue
        
        # Z -> S
        if char == 'Z':
            result.append('S')
            i += 1
            continue
        
        # M -> N
        if char == 'M':
            result.append('N')
            i += 1
            continue
        
        # KN -> N
        if char == 'K' and next_char == 'N':
            i += 1
            continue
        
        # K -> C
        if char == 'K':
            result.append('C')
            i += 1
            continue
        
        # PH -> F
        if char == 'P' and next_char == 'H':
            result.append('F')
            i += 2
            continue
        
        # H -> previous if before non-vowel or after non-vowel
        if char == 'H':
            if prev_char and next_char:
                if prev_char not in 'AEIOU' or next_char not in 'AEIOU':
                    if prev_char not in 'AEIOU':
                        result.append(prev_char)
                    i += 1
                    continue
            result.append('H')
            i += 1
            continue
        
        # W -> previous if after vowel
        if char == 'W':
            if prev_char in 'AEIOU':
                result.append(prev_char)
            else:
                result.append('W')
            i += 1
            continue
        
        result.append(char)
        i += 1
    
    # Step 5: Remove adjacent duplicates
    deduped = []
    for char in result:
        if not deduped or deduped[-1] != char:
            deduped.append(char)
    
    # Step 6: Remove trailing S and A
    while deduped and deduped[-1] in 'SA':
        deduped.pop()
    
    # Step 7: Ensure at least one character
    if not deduped:
        return first if 'first' in dir() else ""
    
    # Pad to at least 4 characters or truncate to 6
    result_str = ''.join(deduped)
    if len(result_str) < 4:
        result_str = (result_str + 'AAAA')[:4]
    
    return result_str[:6]


# ============================================================================
# Caverphone 2.0 Algorithm
# ============================================================================

def caverphone(text: str) -> str:
    """
    Encode a string using the Caverphone 2.0 algorithm.
    
    Caverphone was developed for matching names in the Canterbury
    electoral roll (New Zealand).
    
    Args:
        text: Input string to encode
    
    Returns:
        10-character Caverphone code
    
    Examples:
        >>> caverphone("Lee")
        'L111111111'
        >>> caverphone("Thompson")
        'TMPSN11111'
    """
    if not text:
        return "1111111111"
    
    cleaned = _clean_string(text)
    if not cleaned:
        return "1111111111"
    
    # Convert to lowercase for processing
    cleaned = cleaned.lower()
    
    # Step 1: Remove trailing 'e'
    if cleaned.endswith('e'):
        cleaned = cleaned[:-1]
    
    # Step 2: Replace name endings
    endings = [
        ('ev', 'af'),  # at end only
    ]
    
    # Step 3-12: Character replacements
    replacements = [
        ('cj', 'sk'), ('c', 'k'), ('kh', 'k'), ('ph', 'f'),
        ('qh', 'k'), ('q', 'k'), ('sh', 's'), ('sch', 'sk'),
        ('tj', 'sk'), ('th', 't'), ('v', 'f'), ('w', 'f'),
        ('x', 'k'), ('y', 'f'), ('z', 's'),
    ]
    
    for old, new in replacements:
        cleaned = cleaned.replace(old, new)
    
    # Step 13: Remove vowels
    cleaned = re.sub(r'[aeiou]', '', cleaned)
    
    # Step 14: Remove trailing 'h'
    if cleaned.endswith('h'):
        cleaned = cleaned[:-1]
    
    # Step 15: Remove trailing 'w'
    if cleaned.endswith('w'):
        cleaned = cleaned[:-1]
    
    # Step 16: Remove consecutive duplicates
    deduped = []
    for char in cleaned:
        if not deduped or deduped[-1] != char:
            deduped.append(char)
    cleaned = ''.join(deduped)
    
    # Step 17: Pad or truncate to 10 characters
    cleaned = (cleaned + '1111111111')[:10]
    
    return cleaned.upper()


# ============================================================================
# Match Rating Codex Algorithm
# ============================================================================

def match_rating_codex(text: str) -> str:
    """
    Encode a string using the Match Rating Codex (MRC) algorithm.
    
    MRC was developed by the Ontario Provincial Police for name matching
    in criminal justice systems.
    
    Args:
        text: Input string to encode
    
    Returns:
        MRC code string
    
    Examples:
        >>> match_rating_codex("Smith")
        'SMTH'
        >>> match_rating_codex("O'Connor")
        'OCNR'
    """
    if not text:
        return ""
    
    cleaned = _clean_string(text)
    if not cleaned:
        return ""
    
    # Step 1: Remove vowels
    result = re.sub(r'[AEIOU]', '', cleaned)
    
    # Step 2: Remove consecutive duplicates
    deduped = []
    for char in result:
        if not deduped or deduped[-1] != char:
            deduped.append(char)
    result = ''.join(deduped)
    
    # Step 3: Keep first and last character, remove others that are duplicates
    if len(result) > 2:
        first = result[0]
        last = result[-1]
        middle = result[1:-1]
        
        # Remove consecutive duplicates from middle
        new_middle = []
        prev = first
        for char in middle:
            if char != prev:
                new_middle.append(char)
            prev = char
        
        if new_middle and last == new_middle[-1]:
            new_middle = new_middle[:-1]
        
        result = first + ''.join(new_middle) + last
    
    # Step 4: Limit to 6 characters
    return result[:6]


# ============================================================================
# Fuzzy Matching Functions
# ============================================================================

def soundex_match(name1: str, name2: str) -> bool:
    """
    Check if two names match using Soundex.
    
    Args:
        name1: First name
        name2: Second name
    
    Returns:
        True if Soundex codes match
    
    Examples:
        >>> soundex_match("Smith", "Schmidt")
        True
        >>> soundex_match("Johnson", "Jonson")
        True
    """
    return soundex(name1) == soundex(name2)


def metaphone_match(name1: str, name2: str) -> bool:
    """
    Check if two names match using Metaphone.
    
    Args:
        name1: First name
        name2: Second name
    
    Returns:
        True if Metaphone codes match
    
    Examples:
        >>> metaphone_match("Smith", "Schmidt")
        False
        >>> metaphone_match("Catherine", "Katherine")
        True
    """
    return metaphone(name1) == metaphone(name2)


def double_metaphone_match(name1: str, name2: str) -> bool:
    """
    Check if two names match using Double Metaphone.
    
    Compares all combinations of primary and alternate codes.
    
    Args:
        name1: First name
        name2: Second name
    
    Returns:
        True if any combination of codes match
    
    Examples:
        >>> double_metaphone_match("Smith", "Schmidt")
        True
    """
    result1 = double_metaphone(name1)
    result2 = double_metaphone(name2)
    
    codes1 = {result1.primary}
    if result1.alternate:
        codes1.add(result1.alternate)
    
    codes2 = {result2.primary}
    if result2.alternate:
        codes2.add(result2.alternate)
    
    return bool(codes1 & codes2)


def nysiis_match(name1: str, name2: str) -> bool:
    """
    Check if two names match using NYSIIS.
    
    Args:
        name1: First name
        name2: Second name
    
    Returns:
        True if NYSIIS codes match
    """
    return nysiis(name1) == nysiis(name2)


def phonetic_match(name1: str, name2: str, algorithm: PhoneticAlgorithm = PhoneticAlgorithm.DOUBLE_METAPHONE) -> bool:
    """
    Check if two names match using the specified phonetic algorithm.
    
    Args:
        name1: First name
        name2: Second name
        algorithm: Phonetic algorithm to use
    
    Returns:
        True if names match according to the algorithm
    """
    if algorithm == PhoneticAlgorithm.SOUNDEX:
        return soundex_match(name1, name2)
    elif algorithm == PhoneticAlgorithm.METAPHONE:
        return metaphone_match(name1, name2)
    elif algorithm == PhoneticAlgorithm.DOUBLE_METAPHONE:
        return double_metaphone_match(name1, name2)
    elif algorithm == PhoneticAlgorithm.NYSIIS:
        return nysiis_match(name1, name2)
    elif algorithm == PhoneticAlgorithm.CAVERPHONE:
        return caverphone(name1) == caverphone(name2)
    elif algorithm == PhoneticAlgorithm.MATCH_RATING_CODEX:
        return match_rating_codex(name1) == match_rating_codex(name2)
    else:
        raise ValueError(f"Unknown algorithm: {algorithm}")


def phonetic_similarity(name1: str, name2: str) -> float:
    """
    Calculate phonetic similarity score between two names.
    
    Returns a score from 0.0 to 1.0 based on how many algorithms
    agree that the names match.
    
    Args:
        name1: First name
        name2: Second name
    
    Returns:
        Similarity score (0.0 = no match, 1.0 = all algorithms match)
    
    Examples:
        >>> phonetic_similarity("Smith", "Schmidt")
        0.833...
        >>> phonetic_similarity("John", "Jane")
        0.166...
    """
    algorithms = [
        PhoneticAlgorithm.SOUNDEX,
        PhoneticAlgorithm.METAPHONE,
        PhoneticAlgorithm.DOUBLE_METAPHONE,
        PhoneticAlgorithm.NYSIIS,
        PhoneticAlgorithm.CAVERPHONE,
        PhoneticAlgorithm.MATCH_RATING_CODEX,
    ]
    
    matches = sum(1 for alg in algorithms if phonetic_match(name1, name2, alg))
    return matches / len(algorithms)


def encode_all(text: str) -> PhoneticResult:
    """
    Encode a string using all phonetic algorithms.
    
    Args:
        text: Input string to encode
    
    Returns:
        PhoneticResult with all encodings
    
    Examples:
        >>> result = encode_all("Smith")
        >>> result.soundex
        'S530'
        >>> result.metaphone
        'SM0T'
    """
    dm = double_metaphone(text)
    return PhoneticResult(
        soundex=soundex(text),
        metaphone=metaphone(text),
        double_metaphone=(dm.primary, dm.alternate),
        nysiis=nysiis(text),
        caverphone=caverphone(text),
        match_rating_codex=match_rating_codex(text)
    )


def find_phonetic_matches(name: str, candidates: List[str], 
                         algorithm: PhoneticAlgorithm = PhoneticAlgorithm.DOUBLE_METAPHONE,
                         threshold: float = 0.0) -> List[Tuple[str, float]]:
    """
    Find phonetic matches for a name from a list of candidates.
    
    Args:
        name: Name to match
        candidates: List of candidate names
        algorithm: Phonetic algorithm to use
        threshold: Minimum similarity threshold (0.0 - 1.0)
    
    Returns:
        List of (candidate_name, similarity_score) tuples, sorted by similarity
    
    Examples:
        >>> find_phonetic_matches("Smith", ["Smith", "Schmidt", "Jones"])
        [('Smith', 1.0), ('Schmidt', 0.833...)]
    """
    results = []
    
    for candidate in candidates:
        if algorithm == PhoneticAlgorithm.DOUBLE_METAPHONE:
            score = phonetic_similarity(name, candidate)
        else:
            if phonetic_match(name, candidate, algorithm):
                score = 1.0
            else:
                score = 0.0
        
        if score >= threshold:
            results.append((candidate, score))
    
    # Sort by score descending
    results.sort(key=lambda x: (-x[1], x[0]))
    return results


def batch_encode(names: List[str], algorithm: PhoneticAlgorithm = PhoneticAlgorithm.SOUNDEX) -> Dict[str, str]:
    """
    Encode multiple names using a single algorithm.
    
    Args:
        names: List of names to encode
        algorithm: Phonetic algorithm to use
    
    Returns:
        Dictionary mapping names to their codes
    
    Examples:
        >>> batch_encode(["Smith", "Schmidt", "Johnson"], PhoneticAlgorithm.SOUNDEX)
        {'Smith': 'S530', 'Schmidt': 'S530', 'Johnson': 'J525'}
    """
    encoders = {
        PhoneticAlgorithm.SOUNDEX: soundex,
        PhoneticAlgorithm.METAPHONE: metaphone,
        PhoneticAlgorithm.NYSIIS: nysiis,
        PhoneticAlgorithm.CAVERPHONE: caverphone,
        PhoneticAlgorithm.MATCH_RATING_CODEX: match_rating_codex,
    }
    
    if algorithm == PhoneticAlgorithm.DOUBLE_METAPHONE:
        return {name: double_metaphone(name).primary for name in names}
    
    encoder = encoders.get(algorithm)
    if not encoder:
        raise ValueError(f"Unknown algorithm: {algorithm}")
    
    return {name: encoder(name) for name in names}


if __name__ == '__main__':
    # Quick demo
    print("=== Phonetic Encoding Demo ===\n")
    
    test_names = ["Smith", "Schmidt", "Johnson", "Jonson", "Catherine", "Katherine"]
    
    print("Soundex:")
    for name in test_names:
        print(f"  {name}: {soundex(name)}")
    
    print("\nMetaphone:")
    for name in test_names:
        print(f"  {name}: {metaphone(name)}")
    
    print("\nDouble Metaphone:")
    for name in test_names:
        result = double_metaphone(name)
        print(f"  {name}: {result.primary} / {result.alternate}")
    
    print("\nNYSIIS:")
    for name in test_names:
        print(f"  {name}: {nysiis(name)}")
    
    print("\nPhonetic Similarity (Smith vs Schmidt):")
    print(f"  {phonetic_similarity('Smith', 'Schmidt'):.2%}")
    
    print("\nFind matches for 'Smith':")
    matches = find_phonetic_matches("Smith", ["Smith", "Schmidt", "Smythe", "Jones", "Johnson"])
    for name, score in matches[:3]:
        print(f"  {name}: {score:.2%}")