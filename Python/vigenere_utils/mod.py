"""
Vigenere Cipher Utilities
=========================

A pure Python implementation of the Vigenere cipher with encryption,
decryption, and cryptanalysis features. Zero external dependencies.

The Vigenere cipher is a polyalphabetic substitution cipher that uses
a keyword to shift each letter by different amounts, making it more
secure than simple Caesar ciphers.

Features:
- Encrypt plaintext with a keyword
- Decrypt ciphertext with a keyword
- Auto-crack cipher without key (frequency analysis)
- Validate keys and text
- Support for custom alphabets

Author: AllToolkit
Date: 2026-05-27
"""

import string
from collections import Counter
from typing import Optional, Tuple, List


# Standard English letter frequencies (for cryptanalysis)
ENGLISH_FREQUENCIES = {
    'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97,
    'N': 6.75, 'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25,
    'L': 4.03, 'C': 2.78, 'U': 2.76, 'M': 2.41, 'W': 2.36,
    'F': 2.23, 'G': 2.02, 'Y': 1.97, 'P': 1.93, 'B': 1.29,
    'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15, 'Q': 0.10,
    'Z': 0.07
}

# Common English words for key detection validation
COMMON_WORDS = {
    'THE', 'BE', 'TO', 'OF', 'AND', 'A', 'IN', 'THAT', 'HAVE', 'I',
    'IT', 'FOR', 'NOT', 'ON', 'WITH', 'HE', 'AS', 'YOU', 'DO', 'AT',
    'THIS', 'BUT', 'HIS', 'BY', 'FROM', 'THEY', 'WE', 'SAY', 'HER', 'SHE',
    'OR', 'AN', 'WILL', 'MY', 'ONE', 'ALL', 'WOULD', 'THERE', 'THEIR', 'WHAT'
}


def validate_key(key: str) -> bool:
    """
    Validate that a key is suitable for Vigenere cipher.
    
    Args:
        key: The encryption key to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not key:
        return False
    
    # Key must contain at least one letter
    if not any(c.isalpha() for c in key):
        return False
    
    return True


def normalize_key(key: str) -> str:
    """
    Normalize key to uppercase letters only.
    
    Args:
        key: The original key string
        
    Returns:
        Normalized key with only uppercase letters
    """
    return ''.join(c.upper() for c in key if c.isalpha())


def encrypt(plaintext: str, key: str, preserve_case: bool = True,
           preserve_non_alpha: bool = True) -> str:
    """
    Encrypt plaintext using the Vigenere cipher.
    
    Args:
        plaintext: The text to encrypt
        key: The encryption key (keyword)
        preserve_case: Whether to maintain original letter case
        preserve_non_alpha: Whether to keep non-alphabetic characters
        
    Returns:
        The encrypted ciphertext
        
    Raises:
        ValueError: If the key is invalid
        
    Example:
        >>> encrypt("HELLO", "KEY")
        'RIJVS'
    """
    if not validate_key(key):
        raise ValueError("Key must contain at least one letter")
    
    normalized_key = normalize_key(key)
    result = []
    key_index = 0
    
    for char in plaintext:
        if char.isalpha():
            # Determine base (uppercase or lowercase)
            base = ord('A') if char.upper() == char else ord('a')
            
            # Get shift value from key
            shift = ord(normalized_key[key_index % len(normalized_key)]) - ord('A')
            
            # Apply shift
            encrypted_char = chr((ord(char.upper()) - ord('A') + shift) % 26 + ord('A'))
            
            # Preserve case if requested
            if preserve_case and char.islower():
                encrypted_char = encrypted_char.lower()
            
            result.append(encrypted_char)
            key_index += 1
        else:
            # Non-alphabetic character
            if preserve_non_alpha:
                result.append(char)
    
    return ''.join(result)


def decrypt(ciphertext: str, key: str, preserve_case: bool = True,
           preserve_non_alpha: bool = True) -> str:
    """
    Decrypt ciphertext using the Vigenere cipher.
    
    Args:
        ciphertext: The text to decrypt
        key: The decryption key (keyword)
        preserve_case: Whether to maintain original letter case
        preserve_non_alpha: Whether to keep non-alphabetic characters
        
    Returns:
        The decrypted plaintext
        
    Raises:
        ValueError: If the key is invalid
        
    Example:
        >>> decrypt("RIJVS", "KEY")
        'HELLO'
    """
    if not validate_key(key):
        raise ValueError("Key must contain at least one letter")
    
    normalized_key = normalize_key(key)
    result = []
    key_index = 0
    
    for char in ciphertext:
        if char.isalpha():
            # Determine base (uppercase or lowercase)
            base = ord('A') if char.upper() == char else ord('a')
            
            # Get shift value from key
            shift = ord(normalized_key[key_index % len(normalized_key)]) - ord('A')
            
            # Apply reverse shift
            decrypted_char = chr((ord(char.upper()) - ord('A') - shift) % 26 + ord('A'))
            
            # Preserve case if requested
            if preserve_case and char.islower():
                decrypted_char = decrypted_char.lower()
            
            result.append(decrypted_char)
            key_index += 1
        else:
            # Non-alphabetic character
            if preserve_non_alpha:
                result.append(char)
    
    return ''.join(result)


def find_key_length(ciphertext: str, max_length: int = 20) -> List[Tuple[int, float]]:
    """
    Estimate possible key lengths using the Index of Coincidence method.
    
    The Index of Coincidence (IC) measures how likely it is to draw
    two matching letters by chance. English text has IC around 0.067,
    while random text has IC around 0.038.
    
    Args:
        ciphertext: The encrypted text
        max_length: Maximum key length to test
        
    Returns:
        List of (key_length, ic_score) tuples sorted by IC descending
    """
    # Extract only letters
    letters = ''.join(c.upper() for c in ciphertext if c.isalpha())
    
    if len(letters) < 2:
        return []
    
    results = []
    
    for key_len in range(1, min(max_length + 1, len(letters))):
        total_ic = 0
        
        for i in range(key_len):
            # Get every key_len-th character starting at position i
            column = letters[i::key_len]
            
            if len(column) < 2:
                continue
            
            # Calculate IC for this column
            freq = Counter(column)
            n = len(column)
            ic = sum(f * (f - 1) for f in freq.values()) / (n * (n - 1))
            total_ic += ic
        
        avg_ic = total_ic / key_len
        results.append((key_len, avg_ic))
    
    # Sort by IC descending (higher = more likely to be English)
    results.sort(key=lambda x: x[1], reverse=True)
    
    return results


def crack_single_column(ciphertext_column: str) -> Tuple[str, float]:
    """
    Crack a single column using frequency analysis.
    
    Args:
        ciphertext_column: A column of ciphertext characters
        
    Returns:
        Tuple of (best_shift, chi_squared_score)
    """
    letters = ''.join(c.upper() for c in ciphertext_column if c.isalpha())
    
    if not letters:
        return ('A', float('inf'))
    
    best_shift = 0
    best_score = float('inf')
    
    for shift in range(26):
        # Decrypt with this shift
        decrypted = ''.join(
            chr((ord(c) - ord('A') - shift) % 26 + ord('A'))
            for c in letters
        )
        
        # Calculate chi-squared score
        freq = Counter(decrypted)
        total = len(decrypted)
        
        chi_squared = 0
        for letter in string.ascii_uppercase:
            observed = freq.get(letter, 0)
            expected = (ENGLISH_FREQUENCIES.get(letter, 0) / 100) * total
            if expected > 0:
                chi_squared += ((observed - expected) ** 2) / expected
        
        if chi_squared < best_score:
            best_score = chi_squared
            best_shift = shift
    
    return (chr(best_shift + ord('A')), best_score)


def crack(ciphertext: str, key_length: Optional[int] = None,
         max_key_length: int = 20) -> List[Tuple[str, str, float]]:
    """
    Attempt to crack the Vigenere cipher using frequency analysis.
    
    Args:
        ciphertext: The encrypted text to crack
        key_length: Known key length (if None, will be estimated)
        max_key_length: Maximum key length to try if not provided
        
    Returns:
        List of (key, plaintext, score) tuples sorted by likelihood
    """
    letters = ''.join(c.upper() for c in ciphertext if c.isalpha())
    
    if len(letters) < 10:
        return []  # Too short for reliable analysis
    
    # Estimate key length if not provided
    if key_length is None:
        key_lengths = find_key_length(letters, max_key_length)
        if not key_lengths:
            return []
        
        # Try top 3 most likely key lengths
        candidate_lengths = [kl[0] for kl in key_lengths[:3]]
    else:
        candidate_lengths = [key_length]
    
    results = []
    
    for klen in candidate_lengths:
        # Crack each column
        key_chars = []
        for i in range(klen):
            column = letters[i::klen]
            char, _ = crack_single_column(column)
            key_chars.append(char)
        
        key = ''.join(key_chars)
        
        # Decrypt and score
        plaintext = decrypt(letters, key, preserve_case=False, preserve_non_alpha=False)
        
        # Score based on English word frequency
        words = plaintext.split()
        word_score = sum(1 for w in words if w in COMMON_WORDS) / max(len(words), 1)
        
        results.append((key, plaintext, word_score))
    
    # Sort by score descending
    results.sort(key=lambda x: x[2], reverse=True)
    
    return results


def vigenere_table(key: str, size: int = 26) -> List[List[str]]:
    """
    Generate a Vigenere table (tabula recta) for visualization.
    
    Args:
        key: The keyword to highlight
        size: Size of the table (default 26 for standard alphabet)
        
    Returns:
        2D list representing the Vigenere table
    """
    alphabet = string.ascii_uppercase[:size]
    key_normalized = normalize_key(key)
    
    table = []
    for i, row_start in enumerate(alphabet):
        row = []
        for j, col in enumerate(alphabet):
            # Calculate the letter at this position
            shift = (ord(row_start) - ord('A')) % size
            letter = chr((ord(col) - ord('A') + shift) % size + ord('A'))
            
            # Highlight key letters
            key_idx = i % len(key_normalized) if key_normalized else -1
            if key_idx >= 0 and row_start == key_normalized[key_idx]:
                letter = f'[{letter}]'  # Mark key row
            
            row.append(letter)
        table.append(row)
    
    return table


def auto_decrypt(ciphertext: str) -> Tuple[Optional[str], Optional[str], List[Tuple[str, str, float]]]:
    """
    Fully automatic decryption attempt.
    
    This is a convenience function that tries to crack the cipher
    and returns the most likely result.
    
    Args:
        ciphertext: The encrypted text
        
    Returns:
        Tuple of (best_key, best_plaintext, all_candidates)
        - best_key: The most likely key (or None if cracking failed)
        - best_plaintext: The decrypted text with best key
        - all_candidates: All candidate results
    """
    candidates = crack(ciphertext)
    
    if not candidates:
        return (None, None, [])
    
    best_key, best_plaintext, _ = candidates[0]
    
    # Try to clean up the plaintext by preserving original structure
    result = []
    key_index = 0
    normalized_key = best_key
    
    for char in ciphertext:
        if char.isalpha():
            base = ord('A') if char.upper() == char else ord('a')
            shift = ord(normalized_key[key_index % len(normalized_key)]) - ord('A')
            decrypted_char = chr((ord(char.upper()) - ord('A') - shift) % 26 + ord('A'))
            
            if char.islower():
                decrypted_char = decrypted_char.lower()
            
            result.append(decrypted_char)
            key_index += 1
        else:
            result.append(char)
    
    return (best_key, ''.join(result), candidates)


# Convenience functions for quick use
def encode(text: str, key: str) -> str:
    """Alias for encrypt()."""
    return encrypt(text, key)


def decode(text: str, key: str) -> str:
    """Alias for decrypt()."""
    return decrypt(text, key)


if __name__ == "__main__":
    # Quick demo
    print("Vigenere Cipher Demo")
    print("=" * 50)
    
    plaintext = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"
    key = "SECRET"
    
    print(f"Plaintext: {plaintext}")
    print(f"Key: {key}")
    
    encrypted = encrypt(plaintext, key)
    print(f"Encrypted: {encrypted}")
    
    decrypted = decrypt(encrypted, key)
    print(f"Decrypted: {decrypted}")
    
    print("\nAttempting to crack without key...")
    candidates = crack(encrypted, key_length=len(key))
    for k, pt, score in candidates[:3]:
        print(f"Key: {k}, Score: {score:.3f}")
        print(f"Plaintext: {pt[:50]}...")