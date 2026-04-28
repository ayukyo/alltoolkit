#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Rotation Cipher Utilities Module
=============================================
A comprehensive rotation cipher utility module for Python with zero external dependencies.

Features:
    - Caesar cipher (arbitrary shift)
    - ROT13 (rotate by 13)
    - ROT47 (ASCII printable rotation)
    - ROT5 (digits rotation)
    - Custom alphabet rotation
    - File encryption/decryption
    - Brute force attack support
    - Frequency analysis helpers

Author: AllToolkit Contributors
License: MIT
"""

import string
from typing import Optional, Dict, List, Tuple, Callable
from dataclasses import dataclass
from functools import lru_cache


# ============================================================================
# Constants
# ============================================================================

# Standard English letter frequencies (approximate)
ENGLISH_LETTER_FREQUENCIES: Dict[str, float] = {
    'e': 12.7, 't': 9.1, 'a': 8.2, 'o': 7.5, 'i': 7.0, 'n': 6.7,
    's': 6.3, 'h': 6.1, 'r': 6.0, 'd': 4.3, 'l': 4.0, 'c': 2.8,
    'u': 2.8, 'm': 2.4, 'w': 2.4, 'f': 2.2, 'g': 2.0, 'y': 2.0,
    'p': 1.9, 'b': 1.5, 'v': 1.0, 'k': 0.8, 'j': 0.15, 'x': 0.15,
    'q': 0.10, 'z': 0.07
}

# 预定义的常见模式和异常组合（优化 _score_text 使用）
_COMMON_PATTERNS = ('the', 'and', 'ing', 'tion', 'ed', 'er', 'ly')
_UNUSUAL_COMBOS = ('qx', 'qz', 'vj', 'wz', 'zx', 'zz', 'qq')

# ASCII printable characters for ROT47
ASCII_PRINTABLE = string.printable[:-5]  # Exclude whitespace control chars
ROT47_CHARSET = '!"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~'


# ============================================================================
# Data Classes
# ============================================================================

@dataclass
class CipherResult:
    """Container for cipher operation results."""
    original: str
    result: str
    shift: int
    method: str


@dataclass
class BruteForceResult:
    """Container for brute force attack results."""
    shift: int
    decrypted: str
    score: float  # Higher is more likely English


# ============================================================================
# Core Rotation Functions
# ============================================================================

def caesar_cipher(text: str, shift: int, alphabet: Optional[str] = None) -> str:
    """
    Apply Caesar cipher rotation to text.
    
    Args:
        text: Input text to encrypt/decrypt
        shift: Number of positions to rotate (positive or negative)
        alphabet: Custom alphabet to use (default: a-z, A-Z)
    
    Returns:
        Encrypted/decrypted text
    
    Examples:
        >>> caesar_cipher('HELLO', 3)
        'KHOOR'
        >>> caesar_cipher('KHOOR', -3)
        'HELLO'
        >>> caesar_cipher('HELLO', 3, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        'KHOOR'
    """
    if alphabet is None:
        # Default: preserve case with standard alphabet
        result = []
        for char in text:
            if char.isupper():
                result.append(chr((ord(char) - ord('A') + shift) % 26 + ord('A')))
            elif char.islower():
                result.append(chr((ord(char) - ord('a') + shift) % 26 + ord('a')))
            else:
                result.append(char)
        return ''.join(result)
    else:
        # Custom alphabet
        alphabet_len = len(alphabet)
        alphabet_lower = alphabet.lower()
        result = []
        for char in text:
            if char in alphabet:
                idx = alphabet.index(char)
                result.append(alphabet[(idx + shift) % alphabet_len])
            elif char in alphabet_lower:
                idx = alphabet_lower.index(char)
                result.append(alphabet_lower[(idx + shift) % alphabet_len])
            else:
                result.append(char)
        return ''.join(result)


def rot13(text: str) -> str:
    """
    Apply ROT13 cipher (rotate by 13 positions).
    
    ROT13 is its own inverse: rot13(rot13(text)) == text
    
    Args:
        text: Input text
    
    Returns:
        ROT13 transformed text
    
    Examples:
        >>> rot13('HELLO')
        'URYYB'
        >>> rot13('URYYB')
        'HELLO'
        >>> rot13('Hello, World!')
        'Uryyb, Jbeyq!'
    """
    return caesar_cipher(text, 13)


def rot5(text: str) -> str:
    """
    Apply ROT5 cipher (rotate digits by 5 positions).
    
    ROT5 is its own inverse for digits 0-9.
    
    Args:
        text: Input text
    
    Returns:
        Text with digits rotated by 5
    
    Examples:
        >>> rot5('0123456789')
        '5678901234'
        >>> rot5('Hello 123')
        'Hello 678'
    """
    result = []
    for char in text:
        if char.isdigit():
            result.append(str((int(char) + 5) % 10))
        else:
            result.append(char)
    return ''.join(result)


def rot47(text: str) -> str:
    """
    Apply ROT47 cipher (rotate ASCII printable characters by 47).
    
    ROT47 uses the full range of ASCII printable characters (94 chars).
    It is its own inverse.
    
    Args:
        text: Input text
    
    Returns:
        ROT47 transformed text
    
    Examples:
        >>> rot47('Hello, World!')
        'w6==@ @FC@E8'
        >>> rot47('w6==@ @FC@E8')
        'Hello, World!'
    """
    result = []
    for char in text:
        ascii_val = ord(char)
        if 33 <= ascii_val <= 126:  # Printable ASCII range
            result.append(chr(33 + ((ascii_val - 33 + 47) % 94)))
        else:
            result.append(char)
    return ''.join(result)


def rot18(text: str) -> str:
    """
    Apply ROT18 cipher (combination of ROT13 + ROT5).
    
    ROT18 rotates letters by 13 and digits by 5.
    It is its own inverse.
    
    Args:
        text: Input text
    
    Returns:
        ROT18 transformed text
    
    Examples:
        >>> rot18('Hello123')
        'Uryyb678'
        >>> rot18('Uryyb678')
        'Hello123'
    """
    result = []
    for char in text:
        if char.isupper():
            result.append(chr((ord(char) - ord('A') + 13) % 26 + ord('A')))
        elif char.islower():
            result.append(chr((ord(char) - ord('a') + 13) % 26 + ord('a')))
        elif char.isdigit():
            result.append(str((int(char) + 5) % 10))
        else:
            result.append(char)
    return ''.join(result)


# ============================================================================
# Extended Cipher Functions
# ============================================================================

def vigenere_cipher(text: str, key: str, decrypt: bool = False) -> str:
    """
    Apply Vigenere cipher (polyalphabetic substitution).
    
    Args:
        text: Input text
        key: Encryption key (letters only)
        decrypt: If True, decrypt instead of encrypt
    
    Returns:
        Encrypted/decrypted text
    
    Examples:
        >>> vigenere_cipher('HELLO', 'KEY')
        'RIJVS'
        >>> vigenere_cipher('RIJVS', 'KEY', decrypt=True)
        'HELLO'
    """
    if not key:
        raise ValueError("Key cannot be empty")
    
    # Filter key to only letters and convert to uppercase
    key_clean = ''.join(c.upper() for c in key if c.isalpha())
    if not key_clean:
        raise ValueError("Key must contain at least one letter")
    
    result = []
    key_idx = 0
    
    for char in text:
        if char.isalpha():
            shift = ord(key_clean[key_idx % len(key_clean)]) - ord('A')
            if decrypt:
                shift = -shift
            
            if char.isupper():
                result.append(chr((ord(char) - ord('A') + shift) % 26 + ord('A')))
            else:
                result.append(chr((ord(char) - ord('a') + shift) % 26 + ord('a')))
            
            key_idx += 1
        else:
            result.append(char)
    
    return ''.join(result)


def affine_cipher(text: str, a: int, b: int, decrypt: bool = False) -> str:
    """
    Apply Affine cipher (E(x) = (ax + b) mod 26).
    
    Args:
        text: Input text
        a: Multiplicative key (must be coprime with 26)
        b: Additive key (shift)
        decrypt: If True, decrypt instead of encrypt
    
    Returns:
        Encrypted/decrypted text
    
    Raises:
        ValueError: If 'a' is not coprime with 26
    
    Examples:
        >>> affine_cipher('HELLO', 5, 8)
        'RCLLA'
        >>> affine_cipher('RCLLA', 5, 8, decrypt=True)
        'HELLO'
    """
    # Check if 'a' is coprime with 26
    if a % 2 == 0 or a % 13 == 0:
        raise ValueError("'a' must be coprime with 26 (no common factors)")
    
    result = []
    
    if decrypt:
        # Find modular inverse of a mod 26
        a_inv = _mod_inverse(a, 26)
    
    for char in text:
        if char.isupper():
            x = ord(char) - ord('A')
            if decrypt:
                y = (a_inv * (x - b)) % 26
            else:
                y = (a * x + b) % 26
            result.append(chr(y + ord('A')))
        elif char.islower():
            x = ord(char) - ord('a')
            if decrypt:
                y = (a_inv * (x - b)) % 26
            else:
                y = (a * x + b) % 26
            result.append(chr(y + ord('a')))
        else:
            result.append(char)
    
    return ''.join(result)


def _mod_inverse(a: int, m: int) -> int:
    """Find modular multiplicative inverse using extended Euclidean algorithm."""
    def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y
    
    gcd, x, _ = extended_gcd(a % m, m)
    if gcd != 1:
        raise ValueError("Modular inverse does not exist")
    return (x % m + m) % m


def atbash_cipher(text: str) -> str:
    """
    Apply Atbash cipher (A↔Z, B↔Y, etc.).
    
    Atbash is its own inverse.
    
    Args:
        text: Input text
    
    Returns:
        Encrypted/decrypted text
    
    Examples:
        >>> atbash_cipher('HELLO')
        'SVOOL'
        >>> atbash_cipher('SVOOL')
        'HELLO'
    """
    result = []
    for char in text:
        if char.isupper():
            result.append(chr(ord('Z') - (ord(char) - ord('A'))))
        elif char.islower():
            result.append(chr(ord('z') - (ord(char) - ord('a'))))
        else:
            result.append(char)
    return ''.join(result)


# ============================================================================
# Brute Force and Analysis
# ============================================================================

def brute_force_caesar(ciphertext: str, 
                       language: str = 'en',
                       top_n: int = 5) -> List[BruteForceResult]:
    """
    Brute force attack on Caesar cipher.
    
    Attempts all 25 possible shifts and ranks results by likelihood
    of being the plaintext language.
    
    Args:
        ciphertext: Encrypted text
        language: Language for frequency analysis ('en' for English)
        top_n: Number of top results to return
    
    Returns:
        List of BruteForceResult sorted by score (highest first)
    
    Examples:
        >>> results = brute_force_caesar('KHOOR')
        >>> results[0].decrypted
        'HELLO'
        >>> results[0].shift
        3
    """
    results = []
    
    for shift in range(1, 26):
        decrypted = caesar_cipher(ciphertext, -shift)
        score = _score_text(decrypted, language)
        results.append(BruteForceResult(
            shift=shift,
            decrypted=decrypted,
            score=score
        ))
    
    # Sort by score descending
    results.sort(key=lambda x: x.score, reverse=True)
    
    return results[:top_n]


def _score_text(text: str, language: str = 'en') -> float:
    """
    Score text based on how likely it is to be in the specified language.
    
    Uses frequency analysis of letters.
    
    Args:
        text: Text to score
        language: Language code ('en' for English)
    
    Returns:
        Score (higher = more likely)
    """
    # 优化：直接转小写，避免重复调用
    text_lower = text.lower()
    
    # 优化：使用 collections.Counter 替代手动计数
    letter_count: Dict[str, int] = {}
    total_letters = 0
    
    for char in text_lower:
        if 'a' <= char <= 'z':  # 优化：直接比较，比 isalpha() 更快
            letter_count[char] = letter_count.get(char, 0) + 1
            total_letters += 1
    
    if total_letters == 0:
        return 0.0
    
    # Calculate chi-squared-like score against expected frequencies
    # 优化：使用缓存的总字母数倒数，避免重复除法
    inv_total = 100.0 / total_letters
    score = 0.0
    for letter, expected_freq in ENGLISH_LETTER_FREQUENCIES.items():
        actual_count = letter_count.get(letter, 0)
        actual_freq = actual_count * inv_total
        # Lower difference = higher score
        score -= abs(actual_freq - expected_freq)
    
    # Bonus for common English patterns
    # 优化：使用预定义常量，避免每次创建列表
    for pattern in _COMMON_PATTERNS:
        if pattern in text_lower:
            score += 5
    
    # Penalty for unusual letter combinations
    # 优化：使用预定义常量
    for combo in _UNUSUAL_COMBOS:
        if combo in text_lower:
            score -= 10
    
    return score


def frequency_analysis(text: str) -> Dict[str, float]:
    """
    Perform frequency analysis on text.
    
    Args:
        text: Input text
    
    Returns:
        Dictionary of letter frequencies (percentage)
    
    Examples:
        >>> freq = frequency_analysis('HELLO')
        >>> round(freq['l'], 1)
        40.0
    """
    letter_count: Dict[str, int] = {}
    total_letters = 0
    
    for char in text.lower():
        if char.isalpha():
            letter_count[char] = letter_count.get(char, 0) + 1
            total_letters += 1
    
    if total_letters == 0:
        return {}
    
    frequencies = {}
    for letter, count in letter_count.items():
        frequencies[letter] = (count / total_letters) * 100
    
    return frequencies


def detect_caesar_shift(ciphertext: str, language: str = 'en') -> int:
    """
    Detect the most likely Caesar cipher shift.
    
    Uses frequency analysis to determine the shift.
    
    Args:
        ciphertext: Encrypted text
        language: Language for frequency analysis
    
    Returns:
        Most likely shift value
    
    Examples:
        >>> detect_caesar_shift('KHOOR')
        3
    """
    results = brute_force_caesar(ciphertext, language, top_n=1)
    return results[0].shift if results else 0


# ============================================================================
# Batch Operations
# ============================================================================

def caesar_encrypt(text: str, shift: int) -> CipherResult:
    """
    Encrypt text using Caesar cipher with result object.
    
    Args:
        text: Plaintext
        shift: Rotation amount
    
    Returns:
        CipherResult object
    
    Examples:
        >>> result = caesar_encrypt('HELLO', 3)
        >>> result.result
        'KHOOR'
    """
    return CipherResult(
        original=text,
        result=caesar_cipher(text, shift),
        shift=shift,
        method='caesar'
    )


def caesar_decrypt(text: str, shift: int) -> CipherResult:
    """
    Decrypt text using Caesar cipher with result object.
    
    Args:
        text: Ciphertext
        shift: Original encryption shift
    
    Returns:
        CipherResult object
    
    Examples:
        >>> result = caesar_decrypt('KHOOR', 3)
        >>> result.result
        'HELLO'
    """
    return CipherResult(
        original=text,
        result=caesar_cipher(text, -shift),
        shift=-shift,
        method='caesar'
    )


def multi_rot(text: str, rotations: List[int]) -> str:
    """
    Apply multiple ROT operations in sequence.
    
    Args:
        text: Input text
        rotations: List of rotation amounts
    
    Returns:
        Final transformed text
    
    Examples:
        >>> multi_rot('HELLO', [13, 13])  # ROT13 twice = original
        'HELLO'
        >>> multi_rot('HELLO', [5, 5, 5])
        'KHOOR'
    """
    result = text
    for rot in rotations:
        result = caesar_cipher(result, rot)
    return result


# ============================================================================
# File Operations
# ============================================================================

def encrypt_file(input_path: str, output_path: str, shift: int, 
                 method: str = 'caesar') -> int:
    """
    Encrypt a file using rotation cipher.
    
    Args:
        input_path: Path to input file
        output_path: Path to output file
        shift: Rotation amount (for Caesar) or ignored for self-inverse methods
        method: Cipher method ('caesar', 'rot13', 'rot47', 'rot5', 'rot18', 'atbash')
    
    Returns:
        Number of bytes processed
    
    Examples:
        >>> encrypt_file('plain.txt', 'cipher.txt', 3, 'caesar')
        100  # bytes processed
    """
    cipher_funcs = {
        'caesar': lambda t: caesar_cipher(t, shift),
        'rot13': rot13,
        'rot47': rot47,
        'rot5': rot5,
        'rot18': rot18,
        'atbash': atbash_cipher,
    }
    
    if method not in cipher_funcs:
        raise ValueError(f"Unknown method: {method}")
    
    cipher_func = cipher_funcs[method]
    
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    encrypted = cipher_func(content)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(encrypted)
    
    return len(content)


def decrypt_file(input_path: str, output_path: str, shift: int = 0,
                 method: str = 'caesar') -> int:
    """
    Decrypt a file using rotation cipher.
    
    Args:
        input_path: Path to input file
        output_path: Path to output file
        shift: Rotation amount (for Caesar)
        method: Cipher method
    
    Returns:
        Number of bytes processed
    
    Note:
        For self-inverse methods (rot13, rot47, rot5, rot18, atbash),
        encryption and decryption are the same operation.
    """
    if method == 'caesar':
        return encrypt_file(input_path, output_path, -shift, method)
    else:
        return encrypt_file(input_path, output_path, shift, method)


# ============================================================================
# Utility Functions
# ============================================================================

def is_rot13_encoded(text: str, threshold: float = 0.7) -> bool:
    """
    Heuristic check if text might be ROT13 encoded.
    
    Checks for unusual patterns that suggest encoding.
    
    Args:
        text: Text to check
        threshold: Confidence threshold (0-1)
    
    Returns:
        True if text might be ROT13 encoded
    
    Examples:
        >>> is_rot13_encoded('URYYB')  # ROT13 of HELLO
        True
    """
    if not text:
        return False
    
    # Count vowels
    vowel_count = sum(1 for c in text.lower() if c in 'aeiou')
    letter_count = sum(1 for c in text if c.isalpha())
    
    if letter_count == 0:
        return False
    
    vowel_ratio = vowel_count / letter_count
    
    # English text typically has ~38% vowels
    # ROT13 preserves vowels (a,e → n,r which become vowels after ROT13)
    # Check for unusual letter distributions
    
    # Check for common ROT13 patterns
    # 'n' and 'r' in encoded text often indicate vowels in original
    n_r_count = sum(1 for c in text.lower() if c in 'nr')
    
    return vowel_ratio < 0.25 or n_r_count / max(1, letter_count) > 0.2


def rot_all(text: str) -> Dict[str, str]:
    """
    Apply all standard ROT ciphers and return results.
    
    Args:
        text: Input text
    
    Returns:
        Dictionary of method name to result
    
    Examples:
        >>> results = rot_all('HELLO')
        >>> results['rot13']
        'URYYB'
        >>> results['rot47']
        'w6==@'
    """
    return {
        'rot5': rot5(text),
        'rot13': rot13(text),
        'rot18': rot18(text),
        'rot47': rot47(text),
        'atbash': atbash_cipher(text),
    }


def shift_to_rot_name(shift: int) -> str:
    """
    Convert shift amount to ROT naming convention.
    
    Args:
        shift: Shift amount (0-25 or negative)
    
    Returns:
        ROT name (e.g., 'ROT13', 'ROT3')
    
    Examples:
        >>> shift_to_rot_name(13)
        'ROT13'
        >>> shift_to_rot_name(-3)
        'ROT23'
    """
    normalized = shift % 26
    if normalized == 0:
        return 'ROT0 (no shift)'
    return f'ROT{normalized}'


if __name__ == '__main__':
    # Quick demo
    print("=== Rotation Cipher Utilities Demo ===\n")
    
    # Caesar cipher
    plaintext = "Hello, World!"
    print(f"Original: {plaintext}")
    
    encrypted = caesar_cipher(plaintext, 3)
    print(f"Caesar (shift=3): {encrypted}")
    
    decrypted = caesar_cipher(encrypted, -3)
    print(f"Decrypted: {decrypted}")
    
    # ROT13
    print(f"\nROT13: {rot13(plaintext)}")
    print(f"ROT13 double: {rot13(rot13(plaintext))}")
    
    # ROT47
    print(f"\nROT47: {rot47(plaintext)}")
    
    # ROT18
    print(f"\nROT18: {rot18('Hello 123')}")
    
    # Atbash
    print(f"\nAtbash: {atbash_cipher('HELLO')}")
    
    # Vigenere
    print(f"\nVigenere (key=KEY): {vigenere_cipher('HELLO', 'KEY')}")
    
    # Brute force
    print("\n--- Brute Force Attack ---")
    ciphertext = "KHOOR ZRUOG"
    results = brute_force_caesar(ciphertext, top_n=3)
    for r in results:
        print(f"Shift {r.shift:2d}: {r.decrypted} (score: {r.score:.2f})")
    
    # Frequency analysis
    print("\n--- Frequency Analysis ---")
    freq = frequency_analysis("THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG")
    print(f"Most common letters: {sorted(freq.items(), key=lambda x: -x[1])[:5]}")
    
    # All ROT methods
    print("\n--- All ROT Methods ---")
    all_rots = rot_all("Test123")
    for method, result in all_rots.items():
        print(f"{method}: {result}")