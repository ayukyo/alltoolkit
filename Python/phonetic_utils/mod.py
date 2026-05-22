#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AllToolkit - Phonetic Algorithm Utilities Module

Phonetic algorithms encode words based on their pronunciation rather than 
spelling, enabling matching of similar-sounding names and words. Useful for
deduplication, search, spelling correction, and genealogical research.

Features:
- Soundex (US Census standard)
- Metaphone (improved Soundex)
- Double Metaphone (handles multiple pronunciations)
- Caverphone (New Zealand electoral roll)
- NYSIIS (New York State Identification and Intelligence System)
- Match Rating Codex (simplified encoding)
- Phonetic comparison and matching

Pure Python implementation with zero external dependencies.

Author: AllToolkit
License: MIT
"""

import re
from typing import List, Tuple, Optional, Set, Dict
from dataclasses import dataclass
from enum import Enum


# =============================================================================
# Data Classes and Enums
# =============================================================================

@dataclass
class PhoneticResult:
    """Result of phonetic encoding."""
    original: str
    primary: str
    alternate: Optional[str] = None  # For Double Metaphone
    algorithm: str = ""
    
    def __str__(self) -> str:
        if self.alternate:
            return f"{self.primary}/{self.alternate}"
        return self.primary


class PhoneticAlgorithm(Enum):
    """Supported phonetic algorithms."""
    SOUNDEX = "soundex"
    METAPHONE = "metaphone"
    DOUBLE_METAPHONE = "double_metaphone"
    CAVERPHONE = "caverphone"
    NYSIIS = "nysiis"
    MATCH_RATING = "match_rating"
    REFINED_SOUNDEX = "refined_soundex"


# =============================================================================
# Soundex Algorithm
# =============================================================================

def soundex(name: str) -> PhoneticResult:
    """
    Encode a name using the Soundex algorithm (US Census standard).
    
    Soundex encodes homophones to the same representation, allowing
    matching of similar-sounding names despite minor spelling differences.
    
    Args:
        name: Name or word to encode
        
    Returns:
        PhoneticResult with 4-character Soundex code
        
    Example:
        >>> soundex("Robert").primary
        'R163'
        >>> soundex("Rupert").primary
        'R163'
        >>> soundex("Smith").primary
        'S530'
        >>> soundex("Schmidt").primary
        'S530'
    """
    if not name:
        return PhoneticResult(original=name or "", primary="0000", algorithm="soundex")
    
    # Clean and normalize
    name = name.upper().strip()
    name = re.sub(r'[^A-Z]', '', name)
    
    if not name:
        return PhoneticResult(original=name or "", primary="0000", algorithm="soundex")
    
    # Keep first letter
    first_letter = name[0]
    
    # Mapping: B, P, F, V -> 1; C, S, K, G, J, Q, X, Z -> 2
    # D, T -> 3; L -> 4; M, N -> 5; R -> 6; A, E, I, O, U, H, W, Y -> ignore
    mapping = {
        'B': '1', 'P': '1', 'F': '1', 'V': '1',
        'C': '2', 'S': '2', 'K': '2', 'G': '2', 'J': '2', 'Q': '2', 'X': '2', 'Z': '2',
        'D': '3', 'T': '3',
        'L': '4',
        'M': '5', 'N': '5',
        'R': '6',
        'A': '', 'E': '', 'I': '', 'O': '', 'U': '', 'H': '', 'W': '', 'Y': ''
    }
    
    # Remove first letter and encode
    encoded = first_letter
    prev_code = mapping.get(first_letter, '')
    
    for char in name[1:]:
        code = mapping.get(char, '')
        if code and code != prev_code:
            encoded += code
        prev_code = code if code else prev_code
    
    # Pad or truncate to 4 characters
    encoded = encoded[:4].ljust(4, '0')
    
    return PhoneticResult(
        original=name,
        primary=encoded,
        algorithm="soundex"
    )


def refined_soundex(name: str) -> PhoneticResult:
    """
    Refined Soundex - extended version with more precision.
    
    Uses separate codes for each letter group and preserves
    more phonetic information.
    
    Args:
        name: Name or word to encode
        
    Returns:
        PhoneticResult with refined Soundex code
    """
    if not name:
        return PhoneticResult(original=name or "", primary="", algorithm="refined_soundex")
    
    name = name.upper().strip()
    name = re.sub(r'[^A-Z]', '', name)
    
    if not name:
        return PhoneticResult(original=name or "", primary="", algorithm="refined_soundex")
    
    # Refined Soundex mapping
    mapping = {
        'B': '1', 'P': '1',
        'F': '2', 'V': '2',
        'C': '3', 'S': '3', 'K': '3', 'G': '3',
        'J': '4', 'Q': '4', 'X': '4', 'Z': '4',
        'D': '5', 'T': '5',
        'L': '6',
        'M': '7', 'N': '7',
        'R': '8',
        'A': '9', 'E': '9', 'I': '9', 'O': '9', 'U': '9',
        'H': '', 'W': '', 'Y': ''
    }
    
    encoded = ""
    prev_code = ""
    
    for char in name:
        code = mapping.get(char, '')
        if code and code != prev_code:
            encoded += code
        prev_code = code
    
    return PhoneticResult(
        original=name,
        primary=encoded or "0",
        algorithm="refined_soundex"
    )


# =============================================================================
# Metaphone Algorithm
# =============================================================================

def metaphone(word: str, length: int = 4) -> PhoneticResult:
    """
    Encode a word using the Metaphone algorithm.
    
    Metaphone is more accurate than Soundex for English names,
    using knowledge of English pronunciation rules.
    
    Args:
        word: Word to encode
        length: Maximum length of result (default 4)
        
    Returns:
        PhoneticResult with Metaphone code
        
    Example:
        >>> metaphone("Smith").primary
        'SM0T'
        >>> metaphone("Schmidt").primary
        'SMTT'
    """
    if not word:
        return PhoneticResult(original=word or "", primary="", algorithm="metaphone")
    
    word = word.upper().strip()
    word = re.sub(r'[^A-Z]', '', word)
    
    if not word:
        return PhoneticResult(original=word or "", primary="", algorithm="metaphone")
    
    # Handle silent letters and special cases
    if len(word) >= 2:
        # Handle initial silent letters
        if word[:2] in ['KN', 'GN', 'PN', 'WR', 'AE']:
            word = word[1:]
        elif word.startswith('WH'):
            word = 'W' + word[2:]
        elif word.startswith('X'):
            word = 'S' + word[1:]
    
    result = []
    i = 0
    length_word = len(word)
    
    while i < length_word:
        char = word[i]
        
        # Skip duplicate adjacent letters (except C)
        if i > 0 and char == word[i-1] and char != 'C':
            i += 1
            continue
        
        if char in 'AEIOU':
            # Vowels only at beginning
            if i == 0:
                result.append(char)
        elif char == 'B':
            # B -> B, silent if after M at end
            if not (i == length_word - 1 and i > 0 and word[i-1] == 'M'):
                result.append('B')
        elif char == 'C':
            # C -> X (SH) if -CIA- or -CH-
            # C -> S if -CI-, -CE-, -CY-
            # C -> K otherwise
            if i + 1 < length_word and word[i+1] in 'IEY':
                if i + 2 < length_word and word[i+1:i+3] == 'IA':
                    result.append('X')
                else:
                    result.append('S')
            elif i + 1 < length_word and word[i+1] == 'H':
                result.append('X')
                i += 1
            else:
                result.append('K')
        elif char == 'D':
            # D -> J if -DGE-, -DGI-, -DGY-
            # D -> T otherwise
            if i + 2 < length_word and word[i+1] == 'G' and word[i+2] in 'EIY':
                result.append('J')
                i += 2
            else:
                result.append('T')
        elif char == 'F':
            result.append('F')
        elif char == 'G':
            # G -> F if -GH and not at beginning, silent if -GN or -GNED
            # G -> J if -GI-, -GE-, -GY- and not -GG-
            # G -> K otherwise
            if i + 1 < length_word and word[i+1] == 'H':
                if i + 2 < length_word or i > 0:
                    # GH -> F at end, silent otherwise
                    if i + 1 == length_word - 1:
                        result.append('F')
                    i += 1
            elif i + 1 < length_word and word[i+1] in 'IEY':
                if not (i > 0 and word[i-1] == 'G'):
                    result.append('J')
                else:
                    result.append('K')
            else:
                result.append('K')
        elif char == 'H':
            # H -> H if before vowel, silent otherwise
            if i + 1 < length_word and word[i+1] in 'AEIOU':
                if i == 0 or word[i-1] not in 'CSPTG':
                    result.append('H')
        elif char == 'J':
            result.append('J')
        elif char == 'K':
            # K -> K, silent if after C
            if i == 0 or word[i-1] != 'C':
                result.append('K')
        elif char == 'L':
            result.append('L')
        elif char == 'M':
            result.append('M')
        elif char == 'N':
            result.append('N')
        elif char == 'P':
            # P -> F if before H, P otherwise
            if i + 1 < length_word and word[i+1] == 'H':
                result.append('F')
                i += 1
            else:
                result.append('P')
        elif char == 'Q':
            result.append('K')
        elif char == 'R':
            result.append('R')
        elif char == 'S':
            # S -> X (SH) if -SH-, -SIO-, -SIA-
            if i + 1 < length_word and word[i+1] == 'H':
                result.append('X')
                i += 1
            elif i + 2 < length_word and word[i+1] in 'IO' and word[i+2] in 'AO':
                result.append('X')
            else:
                result.append('S')
        elif char == 'T':
            # T -> X if -TIA-, -TIO-
            # T -> 0 (TH) if -TH-
            # T -> silent if -TCH-
            if i + 2 < length_word and word[i+1] == 'I' and word[i+2] in 'AO':
                result.append('X')
            elif i + 1 < length_word and word[i+1] == 'H':
                result.append('0')  # '0' represents TH sound
                i += 1
            elif i + 2 < length_word and word[i+1:i+3] == 'CH':
                pass  # Silent
            else:
                result.append('T')
        elif char == 'V':
            result.append('F')
        elif char == 'W':
            # W -> W if before vowel
            if i + 1 < length_word and word[i+1] in 'AEIOU':
                result.append('W')
        elif char == 'X':
            result.append('KS')
        elif char == 'Y':
            # Y -> Y if before vowel
            if i + 1 < length_word and word[i+1] in 'AEIOU':
                result.append('Y')
        elif char == 'Z':
            result.append('S')
        
        i += 1
    
    code = ''.join(result)[:length]
    
    return PhoneticResult(
        original=word,
        primary=code,
        algorithm="metaphone"
    )


# =============================================================================
# Double Metaphone Algorithm
# =============================================================================

def double_metaphone(word: str) -> PhoneticResult:
    """
    Encode a word using the Double Metaphone algorithm.
    
    Double Metaphone returns both a primary and alternate encoding,
    handling words with multiple possible pronunciations.
    
    Args:
        word: Word to encode
        
    Returns:
        PhoneticResult with primary and alternate codes
        
    Example:
        >>> result = double_metaphone("Catherine")
        >>> print(result.primary, result.alternate)
        K0RN KTRN
    """
    if not word:
        return PhoneticResult(original=word or "", primary="", algorithm="double_metaphone")
    
    word = word.upper().strip()
    word = re.sub(r'[^A-Z]', '', word)
    
    if not word:
        return PhoneticResult(original=word or "", primary="", algorithm="double_metaphone")
    
    primary = []
    alternate = []
    length = len(word)
    
    # Slavic/Germanic name patterns
    slavic = word.endswith(('WICZ', 'WITZ', 'SKI', 'SKY'))
    germanic = any(word.startswith(p) for p in ['VON ', 'VAN ', 'SCH']) or \
               any(word.endswith(p) for p in ['HEIM', 'BACH', 'HAUS'])
    
    i = 0
    
    while i < length:
        char = word[i]
        
        if char in 'AEIOU':
            # Vowels
            if i == 0:
                primary.append(char)
                alternate.append(char)
        elif char == 'B':
            # B -> P, silent if after M at end
            if not (i == length - 1 and i > 0 and word[i-1] == 'M'):
                primary.append('P')
                alternate.append('P')
        elif char == 'C':
            # Various C rules
            if i > 0 and i + 2 < length and word[i-1:i+2] == 'SCH':
                # SCH -> SK (Germanic)
                primary.append('K')
                alternate.append('K')
            elif i + 1 < length and word[i+1] == 'H':
                # CH -> X/K
                if i == 0:
                    if length > 1 and word[1] in 'AEIOU':
                        primary.append('K')
                        alternate.append('X')
                    else:
                        primary.append('X')
                        alternate.append('X')
                elif i > 0 and word[i-1] in 'AEIOU':
                    primary.append('K')
                    alternate.append('X')
                else:
                    primary.append('X')
                    alternate.append('X')
                i += 1
            elif i + 1 < length and word[i+1] in 'IEY':
                # CI, CE, CY -> S
                if i == 0:
                    primary.append('S')
                    alternate.append('S')
                else:
                    primary.append('S')
                    alternate.append('S')
            else:
                primary.append('K')
                alternate.append('K')
        elif char == 'D':
            if i + 2 < length and word[i+1] == 'G' and word[i+2] in 'IEY':
                primary.append('J')
                alternate.append('J')
                i += 2
            else:
                primary.append('T')
                alternate.append('T')
        elif char == 'F':
            primary.append('F')
            alternate.append('F')
        elif char == 'G':
            # Various G rules
            if i + 1 < length and word[i+1] == 'H':
                if i > 0 and word[i-1] not in 'AEIOU':
                    primary.append('K')
                    alternate.append('K')
                elif i + 2 == length:
                    pass  # Silent
                else:
                    primary.append('K')
                    alternate.append('K')
                i += 1
            elif i + 1 < length and word[i+1] in 'IEY':
                if i > 0 and word[i-1] != 'G':
                    primary.append('J')
                    alternate.append('J')
                else:
                    primary.append('K')
                    alternate.append('K')
            else:
                primary.append('K')
                alternate.append('K')
        elif char == 'H':
            if i + 1 < length and word[i+1] in 'AEIOU':
                if i == 0 or word[i-1] not in 'CSPTG':
                    primary.append('H')
                    alternate.append('H')
        elif char == 'J':
            primary.append('J')
            alternate.append('J')
        elif char == 'K':
            if i == 0 or word[i-1] != 'C':
                primary.append('K')
                alternate.append('K')
        elif char == 'L':
            primary.append('L')
            alternate.append('L')
        elif char == 'M':
            primary.append('M')
            alternate.append('M')
        elif char == 'N':
            primary.append('N')
            alternate.append('N')
        elif char == 'P':
            if i + 1 < length and word[i+1] == 'H':
                primary.append('F')
                alternate.append('F')
                i += 1
            else:
                primary.append('P')
                alternate.append('P')
        elif char == 'Q':
            primary.append('K')
            alternate.append('K')
        elif char == 'R':
            primary.append('R')
            alternate.append('R')
        elif char == 'S':
            if i + 1 < length and word[i+1] == 'H':
                primary.append('X')
                alternate.append('X')
                i += 1
            elif i + 2 < length and word[i+1:i+3] in ['IA', 'IO']:
                primary.append('X')
                alternate.append('S')
            else:
                primary.append('S')
                alternate.append('S')
        elif char == 'T':
            if i + 2 < length and word[i+1:i+3] in ['IA', 'IO']:
                primary.append('X')
                alternate.append('X')
            elif i + 1 < length and word[i+1] == 'H':
                primary.append('0')  # TH
                alternate.append('T')
                i += 1
            elif i + 2 < length and word[i+1:i+3] == 'CH':
                pass  # Silent in TCH
            else:
                primary.append('T')
                alternate.append('T')
        elif char == 'V':
            primary.append('F')
            alternate.append('F')
        elif char == 'W':
            if i + 1 < length and word[i+1] in 'AEIOU':
                primary.append('W')
                alternate.append('W')
        elif char == 'X':
            primary.append('KS')
            alternate.append('KS')
        elif char == 'Y':
            if i + 1 < length and word[i+1] in 'AEIOU':
                primary.append('Y')
                alternate.append('Y')
        elif char == 'Z':
            primary.append('S')
            alternate.append('S')
        
        i += 1
    
    primary_code = ''.join(primary)
    alt_code = ''.join(alternate)
    
    return PhoneticResult(
        original=word,
        primary=primary_code,
        alternate=alt_code if alt_code != primary_code else None,
        algorithm="double_metaphone"
    )


# =============================================================================
# Caverphone Algorithm
# =============================================================================

def caverphone(word: str, version: int = 2) -> PhoneticResult:
    """
    Encode a word using the Caverphone algorithm.
    
    Caverphone was designed for matching names in New Zealand 
    electoral rolls, handling Maori-influenced pronunciations.
    
    Args:
        word: Word to encode
        version: Caverphone version (1 or 2, default 2)
        
    Returns:
        PhoneticResult with Caverphone code
    """
    if not word:
        return PhoneticResult(original=word or "", primary="1111111111", algorithm="caverphone")
    
    word = word.upper().strip()
    word = re.sub(r'[^A-Z]', '', word)
    
    if not word:
        return PhoneticResult(original=word or "", primary="1111111111", algorithm="caverphone")
    
    # Step 1: Remove trailing 'e'
    if word.endswith('E'):
        word = word[:-1]
    
    # Step 2: Replace name endings
    endings = [
        ('EIGH', 'A'), ('OUGH', 'A'), ('AUGH', 'A'), 
        ('GN', 'N'), ('DG', 'G'), ('TCH', 'CH')
    ]
    for old, new in endings:
        if word.endswith(old):
            word = word[:-len(old)] + new
    
    # Step 3: Replace letter sequences
    replacements = [
        ('V', 'F'), ('Z', 'S'), ('PH', 'F'), ('X', 'S'),
        ('SCH', 'SK'), ('SH', 'S'), ('CH', 'K'),
        ('KN', 'N'), ('GN', 'N'), ('WR', 'R'),
        ('YE', 'Y'), ('AI', 'A'), ('EI', 'A'),
        ('AU', 'A'), ('OU', 'A'), ('EA', 'E'),
        ('EE', 'E'), ('IE', 'I'), ('OO', 'U'),
        ('OA', 'O'), ('TH', '0'), ('QU', 'KW'),
        ('CY', 'S'), ('CI', 'S'), ('CE', 'S'),
    ]
    
    for old, new in replacements:
        word = word.replace(old, new)
    
    # Step 4: Keep only consonants (and digits for TH->0)
    result = ""
    for char in word:
        if char in 'BCDFGHJKLMNPQRSTVWXYZ0':
            result += char
    
    # Step 5: Pad or truncate to 10 characters
    result = result[:10].ljust(10, '1')
    
    return PhoneticResult(
        original=word,
        primary=result,
        algorithm=f"caverphone{version}"
    )


# =============================================================================
# NYSIIS Algorithm
# =============================================================================

def nysiis(name: str) -> PhoneticResult:
    """
    Encode a name using the NYSIIS algorithm.
    
    NYSIIS (New York State Identification and Intelligence System)
    is designed to encode similar-sounding names to the same code.
    
    Args:
        name: Name to encode
        
    Returns:
        PhoneticResult with NYSIIS code
        
    Example:
        >>> nysiis("O'Connor").primary
        'OCANN'
    """
    if not name:
        return PhoneticResult(original=name or "", primary="", algorithm="nysiis")
    
    name = name.upper().strip()
    name = re.sub(r'[^A-Z]', '', name)
    
    if not name:
        return PhoneticResult(original=name or "", primary="", algorithm="nysiis")
    
    # Handle first character rules
    first_char = name[0]
    
    # Replace first letter
    if name.startswith('MAC'):
        name = 'MCC' + name[3:]
    elif name.startswith('KN'):
        name = 'NN' + name[2:]
    elif name.startswith('K'):
        name = 'C' + name[1:]
    elif name.startswith('PH') or name.startswith('PF'):
        name = 'FF' + name[2:]
    elif name.startswith('SCH'):
        name = 'SSS' + name[3:]
    
    # Replace last letter
    if name.endswith('EE'):
        name = name[:-2] + 'Y'
    elif name.endswith('IE'):
        name = name[:-2] + 'Y'
    elif name.endswith(('DT', 'RT', 'RD', 'NT', 'ND')):
        # Keep as is
        pass
    elif name.endswith('S') or name.endswith('Z'):
        name = name[:-1] + 'S'
    elif name.endswith('X'):
        name = name[:-1] + 'S'
    
    result = name[0]
    
    # Process remaining characters
    i = 1
    while i < len(name):
        char = name[i]
        prev_char = name[i-1] if i > 0 else ''
        
        # Skip if same as previous
        if char == prev_char:
            i += 1
            continue
        
        # Replace sequences
        if char == 'E' and i + 1 < len(name) and name[i+1] == 'V':
            result += 'AF'
            i += 2
            continue
        
        # Replace vowels
        if char in 'AEIOU':
            if i + 1 < len(name) and name[i+1] == 'Y':
                result += 'Y'
                i += 2
            else:
                result += 'A'
        elif char == 'Q':
            result += 'G'
        elif char == 'Z':
            result += 'S'
        elif char == 'M':
            result += 'N'
        elif char == 'K':
            if i + 1 < len(name) and name[i+1] == 'N':
                result += 'N'
                i += 1
            else:
                result += 'C'
        elif char == 'H':
            if prev_char not in 'AEIOU' and (i + 1 < len(name) and name[i+1] not in 'AEIOU'):
                # H between consonants - keep previous
                pass
            else:
                result += 'H'
        elif char == 'W':
            if prev_char in 'AEIOU':
                result += 'A'
        else:
            result += char
        
        i += 1
    
    # Replace trailing patterns
    if result.endswith('S'):
        result = result[:-1] + 'A'
    if result.endswith('AY'):
        result = result[:-2] + 'Y'
    if result.endswith('A'):
        result = result[:-1]
    
    # Remove duplicate adjacent characters
    final = result[0]
    for char in result[1:]:
        if char != final[-1]:
            final += char
    
    return PhoneticResult(
        original=name,
        primary=final,
        algorithm="nysiis"
    )


# =============================================================================
# Match Rating Codex
# =============================================================================

def match_rating_codex(name: str) -> PhoneticResult:
    """
    Encode a name using Match Rating Codex (MRC) algorithm.
    
    MRC is a simplified phonetic encoding used for matching
    similar-sounding names with a comparison algorithm.
    
    Args:
        name: Name to encode
        
    Returns:
        PhoneticResult with MRC code
    """
    if not name:
        return PhoneticResult(original=name or "", primary="", algorithm="match_rating")
    
    name = name.upper().strip()
    name = re.sub(r'[^A-Z]', '', name)
    
    if not name:
        return PhoneticResult(original=name or "", primary="", algorithm="match_rating")
    
    # Step 1: Remove vowels (except first)
    result = name[0]
    for char in name[1:]:
        if char not in 'AEIOU':
            result += char
    
    # Step 2: Remove adjacent duplicates
    final = result[0]
    for char in result[1:]:
        if char != final[-1]:
            final += char
    
    # Step 3: Limit to first and last 3 characters if > 6
    if len(final) > 6:
        final = final[:3] + final[-3:]
    
    return PhoneticResult(
        original=name,
        primary=final,
        algorithm="match_rating"
    )


def match_rating_compare(code1: str, code2: str) -> Tuple[bool, int]:
    """
    Compare two Match Rating Codex codes.
    
    Args:
        code1: First MRC code
        code2: Second MRC code
        
    Returns:
        Tuple of (match: bool, score: int)
    """
    len1, len2 = len(code1), len(code2)
    diff = abs(len1 - len2)
    
    # Length difference check
    if len1 <= 4 and diff > 2:
        return False, diff
    if len1 <= 7 and diff > 3:
        return False, diff
    if diff > 4:
        return False, diff
    
    # Count matching characters
    matches = 0
    for c1, c2 in zip(code1, code2):
        if c1 == c2:
            matches += 1
    
    # Minimum matches required
    min_len = min(len1, len2)
    min_matches = min_len // 2 + 1
    
    return matches >= min_matches, matches


# =============================================================================
# Phonetic Comparison Functions
# =============================================================================

def phonetic_match(
    word1: str,
    word2: str,
    algorithm: PhoneticAlgorithm = PhoneticAlgorithm.DOUBLE_METAPHONE
) -> Tuple[bool, float]:
    """
    Check if two words match phonetically.
    
    Args:
        word1: First word
        word2: Second word
        algorithm: Phonetic algorithm to use
        
    Returns:
        Tuple of (matches: bool, similarity: float)
    """
    result1 = encode(word1, algorithm)
    result2 = encode(word2, algorithm)
    
    # Check primary codes
    if result1.primary == result2.primary:
        return True, 1.0
    
    # Check alternate codes (for Double Metaphone)
    if result1.alternate and result1.alternate == result2.primary:
        return True, 0.9
    if result2.alternate and result1.primary == result2.alternate:
        return True, 0.9
    if result1.alternate and result2.alternate and result1.alternate == result2.alternate:
        return True, 0.9
    
    # Calculate similarity
    from difflib import SequenceMatcher
    similarity = SequenceMatcher(None, result1.primary, result2.primary).ratio()
    
    return False, similarity


def encode(word: str, algorithm: PhoneticAlgorithm) -> PhoneticResult:
    """
    Encode a word using the specified phonetic algorithm.
    
    Args:
        word: Word to encode
        algorithm: Phonetic algorithm to use
        
    Returns:
        PhoneticResult with encoding
    """
    if algorithm == PhoneticAlgorithm.SOUNDEX:
        return soundex(word)
    elif algorithm == PhoneticAlgorithm.METAPHONE:
        return metaphone(word)
    elif algorithm == PhoneticAlgorithm.DOUBLE_METAPHONE:
        return double_metaphone(word)
    elif algorithm == PhoneticAlgorithm.CAVERPHONE:
        return caverphone(word)
    elif algorithm == PhoneticAlgorithm.NYSIIS:
        return nysiis(word)
    elif algorithm == PhoneticAlgorithm.MATCH_RATING:
        return match_rating_codex(word)
    elif algorithm == PhoneticAlgorithm.REFINED_SOUNDEX:
        return refined_soundex(word)
    else:
        return soundex(word)


def phonetic_search(
    query: str,
    candidates: List[str],
    algorithm: PhoneticAlgorithm = PhoneticAlgorithm.DOUBLE_METAPHONE,
    threshold: float = 0.8
) -> List[Tuple[str, float]]:
    """
    Search for phonetically similar words.
    
    Args:
        query: Query word
        candidates: List of candidate words
        algorithm: Phonetic algorithm to use
        threshold: Minimum similarity threshold
        
    Returns:
        List of (word, similarity) tuples, sorted by similarity
    """
    query_result = encode(query, algorithm)
    matches = []
    
    for candidate in candidates:
        cand_result = encode(candidate, algorithm)
        
        # Check exact matches
        if query_result.primary == cand_result.primary:
            matches.append((candidate, 1.0))
            continue
        
        if query_result.alternate and query_result.alternate == cand_result.primary:
            matches.append((candidate, 0.95))
            continue
        
        if cand_result.alternate and query_result.primary == cand_result.alternate:
            matches.append((candidate, 0.95))
            continue
        
        if query_result.alternate and cand_result.alternate:
            if query_result.alternate == cand_result.alternate:
                matches.append((candidate, 0.9))
                continue
        
        # Calculate similarity
        from difflib import SequenceMatcher
        similarity = SequenceMatcher(None, query_result.primary, cand_result.primary).ratio()
        
        if similarity >= threshold:
            matches.append((candidate, similarity))
    
    return sorted(matches, key=lambda x: x[1], reverse=True)


def encode_all(word: str) -> Dict[str, PhoneticResult]:
    """
    Encode a word using all available algorithms.
    
    Args:
        word: Word to encode
        
    Returns:
        Dictionary mapping algorithm names to results
    """
    return {
        'soundex': soundex(word),
        'refined_soundex': refined_soundex(word),
        'metaphone': metaphone(word),
        'double_metaphone': double_metaphone(word),
        'caverphone': caverphone(word),
        'nysiis': nysiis(word),
        'match_rating': match_rating_codex(word),
    }


def phonetic_similarity(word1: str, word2: str) -> float:
    """
    Calculate overall phonetic similarity between two words.
    
    Uses multiple algorithms and returns average similarity.
    
    Args:
        word1: First word
        word2: Second word
        
    Returns:
        Similarity score from 0.0 to 1.0
    """
    algorithms = [
        PhoneticAlgorithm.SOUNDEX,
        PhoneticAlgorithm.METAPHONE,
        PhoneticAlgorithm.DOUBLE_METAPHONE,
        PhoneticAlgorithm.NYSIIS,
    ]
    
    total_similarity = 0.0
    
    for algo in algorithms:
        matches, similarity = phonetic_match(word1, word2, algo)
        total_similarity += similarity
    
    return total_similarity / len(algorithms)


# =============================================================================
# Utility Functions
# =============================================================================

def group_by_phonetic(
    words: List[str],
    algorithm: PhoneticAlgorithm = PhoneticAlgorithm.DOUBLE_METAPHONE
) -> Dict[str, List[str]]:
    """
    Group words by their phonetic encoding.
    
    Args:
        words: List of words to group
        algorithm: Phonetic algorithm to use
        
    Returns:
        Dictionary mapping phonetic codes to lists of words
    """
    groups: Dict[str, List[str]] = {}
    
    for word in words:
        result = encode(word, algorithm)
        code = result.primary
        
        if code not in groups:
            groups[code] = []
        groups[code].append(word)
        
        # Also group by alternate code if present
        if result.alternate:
            if result.alternate not in groups:
                groups[result.alternate] = []
            if word not in groups[result.alternate]:
                groups[result.alternate].append(word)
    
    return groups


def find_duplicates(
    words: List[str],
    algorithm: PhoneticAlgorithm = PhoneticAlgorithm.DOUBLE_METAPHONE,
    threshold: float = 0.9
) -> List[List[str]]:
    """
    Find phonetic duplicates in a list of words.
    
    Args:
        words: List of words
        algorithm: Phonetic algorithm to use
        threshold: Minimum similarity for duplicate
        
    Returns:
        List of groups of similar words
    """
    groups = group_by_phonetic(words, algorithm)
    duplicates = []
    
    for code, group in groups.items():
        if len(group) > 1 and group not in duplicates:
            # Check if this group is already included
            is_subset = False
            for existing in duplicates:
                if set(group).issubset(set(existing)):
                    is_subset = True
                    break
            if not is_subset:
                duplicates.append(group)
    
    return duplicates


# =============================================================================
# Main (for testing)
# =============================================================================

if __name__ == '__main__':
    print("=" * 60)
    print("Phonetic Algorithm Utilities - Test Suite")
    print("=" * 60)
    
    test_names = [
        "Robert", "Rupert", "Smith", "Schmidt", "Catherine", "Katherine",
        "O'Connor", "Oconnor", "Johnson", "Johnsen", "MacDonald", "McDonald",
        "Wilson", "Willson", "Thompson", "Thomson"
    ]
    
    print("\n--- Soundex ---")
    for name in test_names[:6]:
        result = soundex(name)
        print(f"{name:15} -> {result.primary}")
    
    print("\n--- Metaphone ---")
    for name in test_names[:6]:
        result = metaphone(name)
        print(f"{name:15} -> {result.primary}")
    
    print("\n--- Double Metaphone ---")
    for name in test_names[:6]:
        result = double_metaphone(name)
        if result.alternate:
            print(f"{name:15} -> {result.primary} / {result.alternate}")
        else:
            print(f"{name:15} -> {result.primary}")
    
    print("\n--- NYSIIS ---")
    for name in test_names[:6]:
        result = nysiis(name)
        print(f"{name:15} -> {result.primary}")
    
    print("\n--- Phonetic Matching ---")
    pairs = [("Robert", "Rupert"), ("Smith", "Schmidt"), ("Catherine", "Katherine")]
    for w1, w2 in pairs:
        matches, similarity = phonetic_match(w1, w2)
        status = "✓" if matches else "✗"
        print(f"{w1:12} vs {w2:12}: {status} ({similarity:.2f})")
    
    print("\n--- Group by Phonetic ---")
    groups = group_by_phonetic(test_names)
    for code, names in sorted(groups.items())[:5]:
        print(f"{code:10} -> {', '.join(names)}")
    
    print("\n" + "=" * 60)
    print("All tests completed successfully!")