"""
Vigenere Cipher Utilities - Usage Examples
=========================================

This file demonstrates various use cases for the Vigenere cipher utilities.

Author: AllToolkit
Date: 2026-05-27
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from vigenere_utils.mod import (
    encrypt, decrypt, encode, decode,
    find_key_length, crack, auto_decrypt,
    vigenere_table, validate_key, normalize_key
)


def example_1_basic_encryption():
    """Example 1: Basic encryption and decryption."""
    print("\n" + "=" * 60)
    print("Example 1: Basic Encryption and Decryption")
    print("=" * 60)
    
    plaintext = "HELLO WORLD"
    key = "SECRET"
    
    print(f"\nOriginal: {plaintext}")
    print(f"Key: {key}")
    
    # Encrypt
    ciphertext = encrypt(plaintext, key)
    print(f"Encrypted: {ciphertext}")
    
    # Decrypt
    decrypted = decrypt(ciphertext, key)
    print(f"Decrypted: {decrypted}")
    
    # Verify
    print(f"✓ Round-trip successful: {plaintext == decrypted}")


def example_2_case_preservation():
    """Example 2: Case preservation options."""
    print("\n" + "=" * 60)
    print("Example 2: Case Preservation")
    print("=" * 60)
    
    plaintext = "Hello World"
    key = "KEY"
    
    # With case preservation (default)
    encrypted1 = encrypt(plaintext, key, preserve_case=True)
    print(f"\nPreserve case ON:  '{plaintext}' -> '{encrypted1}'")
    
    # Without case preservation
    encrypted2 = encrypt(plaintext, key, preserve_case=False)
    print(f"Preserve case OFF: '{plaintext}' -> '{encrypted2}'")


def example_3_special_characters():
    """Example 3: Handling special characters and numbers."""
    print("\n" + "=" * 60)
    print("Example 3: Special Characters and Numbers")
    print("=" * 60)
    
    plaintext = "Meet me at 3:00 PM! Don't be late."
    key = "SECURE"
    
    print(f"\nOriginal: {plaintext}")
    
    # Preserve non-alphabetic characters (default)
    encrypted = encrypt(plaintext, key, preserve_non_alpha=True)
    print(f"Encrypted: {encrypted}")
    
    decrypted = decrypt(encrypted, key)
    print(f"Decrypted: {decrypted}")
    
    # Remove non-alphabetic characters
    encrypted_clean = encrypt(plaintext, key, preserve_non_alpha=False)
    print(f"\nWithout special chars: {encrypted_clean}")


def example_4_historical_cipher():
    """Example 4: Historical Vigenere cipher example."""
    print("\n" + "=" * 60)
    print("Example 4: Historical Example")
    print("=" * 60)
    
    # Famous historical example
    plaintext = "ATTACKATDAWN"
    key = "LEMON"
    
    print(f"\nHistorical example:")
    print(f"Plaintext: {plaintext}")
    print(f"Key: {key}")
    
    ciphertext = encrypt(plaintext, key)
    print(f"Ciphertext: {ciphertext}")
    print(f"Expected:  LXFOPVEFRNHR")
    print(f"✓ Matches expected: {ciphertext == 'LXFOPVEFRNHR'}")


def example_5_key_length_detection():
    """Example 5: Detecting key length from ciphertext."""
    print("\n" + "=" * 60)
    print("Example 5: Key Length Detection")
    print("=" * 60)
    
    plaintext = (
        "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG "
        "AND THE RAIN IN SPAIN FALLS MAINLY ON THE PLAIN"
    )
    key = "CRYPTOGRAPHY"
    actual_key_length = len(key)
    
    ciphertext = encrypt(plaintext, key)
    print(f"\nEncrypted a long message with key '{key}' (length: {actual_key_length})")
    
    # Detect key length
    results = find_key_length(ciphertext, max_length=15)
    
    print("\nTop 5 most likely key lengths:")
    print("Length | IC Score")
    print("-" * 25)
    for length, score in results[:5]:
        marker = " <-- Actual" if length == actual_key_length else ""
        print(f"  {length:2d}   | {score:.6f}{marker}")


def example_6_cracking_cipher():
    """Example 6: Cracking a Vigenere cipher without the key."""
    print("\n" + "=" * 60)
    print("Example 6: Cracking Without the Key")
    print("=" * 60)
    
    plaintext = (
        "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG "
        "THIS IS A SECRET MESSAGE THAT WE WANT TO HIDE"
    )
    key = "SECRET"
    key_length = len(key)
    
    ciphertext = encrypt(plaintext, key)
    print(f"\nOriginal plaintext: {plaintext[:50]}...")
    print(f"Key (unknown to cracker): {key}")
    print(f"Ciphertext: {ciphertext[:50]}...")
    
    # Attempt to crack
    print("\nCracking...")
    candidates = crack(ciphertext, key_length=key_length)
    
    print("\nTop candidates:")
    print("Key     | Score  | Plaintext preview")
    print("-" * 60)
    for cand_key, cand_plaintext, score in candidates[:5]:
        print(f"{cand_key:7s} | {score:.3f}  | {cand_plaintext[:40]}...")
    
    # Check if we found the right key
    correct = any(k == key for k, _, _ in candidates)
    print(f"\n✓ Found correct key: {correct}")


def example_7_automatic_decryption():
    """Example 7: Fully automatic decryption."""
    print("\n" + "=" * 60)
    print("Example 7: Automatic Decryption")
    print("=" * 60)
    
    # A longer text works better for automatic cracking
    plaintext = (
        "IT WAS THE BEST OF TIMES IT WAS THE WORST OF TIMES "
        "IT WAS THE AGE OF WISDOM IT WAS THE AGE OF FOOLISHNESS "
        "IT WAS THE EPOCH OF BELIEF IT WAS THE EPOCH OF INCREDULITY"
    )
    key = "DICKENS"
    
    ciphertext = encrypt(plaintext, key)
    print(f"\nOriginal: {plaintext[:60]}...")
    print(f"Key: {key}")
    print(f"Ciphertext: {ciphertext[:60]}...")
    
    # Auto decrypt
    found_key, decrypted, all_candidates = auto_decrypt(ciphertext)
    
    print(f"\nAuto-detected key: {found_key}")
    print(f"Decrypted text: {decrypted[:60]}...")
    print(f"✓ Correct decryption: {decrypted.replace(' ', '') == plaintext.replace(' ', '')}")


def example_8_vigenere_table():
    """Example 8: Viewing the Vigenere table (Tabula Recta)."""
    print("\n" + "=" * 60)
    print("Example 8: Vigenere Table (Tabula Recta)")
    print("=" * 60)
    
    key = "KEY"
    print(f"\nGenerating Vigenere table with key '{key}' highlighted...")
    
    table = vigenere_table(key)
    
    # Print header
    print("\n    ", end="")
    for col in range(10):  # Show first 10 columns for brevity
        print(f" {chr(ord('A') + col)}  ", end="")
    print()
    print("   " + "-" * 34)
    
    # Print rows (first 10 for brevity)
    for i, row in enumerate(table[:10]):
        letter = chr(ord('A') + i)
        print(f" {letter} |", end="")
        for j, cell in enumerate(row[:10]):
            # Check if this is a key row
            key_idx = i % len(key) if key else -1
            if key_idx >= 0 and chr(ord('A') + i) == normalize_key(key)[key_idx]:
                print(f" {cell}", end="")
            else:
                print(f" {cell} ", end="")
        print()


def example_9_key_validation():
    """Example 9: Key validation and normalization."""
    print("\n" + "=" * 60)
    print("Example 9: Key Validation and Normalization")
    print("=" * 60)
    
    test_keys = [
        ("SECRET", "Valid simple key"),
        ("MySecretKey123", "Valid key with numbers"),
        ("K-E-Y!", "Valid key with symbols (normalized)"),
        ("12345", "Invalid - numbers only"),
        ("!@#$%", "Invalid - symbols only"),
        ("", "Invalid - empty"),
    ]
    
    print("\nKey Validation Results:")
    print("-" * 50)
    for key, description in test_keys:
        is_valid = validate_key(key)
        normalized = normalize_key(key) if is_valid else "N/A"
        status = "✓" if is_valid else "✗"
        print(f"{status} {key:15s} -> {normalized:15s} ({description})")


def example_10_convenience_aliases():
    """Example 10: Using convenience aliases."""
    print("\n" + "=" * 60)
    print("Example 10: Convenience Aliases")
    print("=" * 60)
    
    # encode/decode are aliases for encrypt/decrypt
    plaintext = "SECRET MESSAGE"
    key = "KEY"
    
    # Using encode/decode aliases
    encoded = encode(plaintext, key)
    decoded = decode(encoded, key)
    
    print(f"\nUsing encode/decode aliases:")
    print(f"encode('{plaintext}', '{key}') = {encoded}")
    print(f"decode('{encoded}', '{key}') = {decoded}")


def main():
    """Run all examples."""
    print("=" * 60)
    print("VIGENERE CIPHER UTILITIES - USAGE EXAMPLES")
    print("=" * 60)
    
    example_1_basic_encryption()
    example_2_case_preservation()
    example_3_special_characters()
    example_4_historical_cipher()
    example_5_key_length_detection()
    example_6_cracking_cipher()
    example_7_automatic_decryption()
    example_8_vigenere_table()
    example_9_key_validation()
    example_10_convenience_aliases()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()