#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Rotation Cipher Utilities Usage Examples
======================================================
Practical examples demonstrating rotation cipher functionality.

Run with: python usage_examples.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    caesar_cipher, rot13, rot5, rot47, rot18,
    vigenere_cipher, affine_cipher, atbash_cipher,
    brute_force_caesar, frequency_analysis, detect_caesar_shift,
    caesar_encrypt, caesar_decrypt, multi_rot,
    rot_all, shift_to_rot_name, is_rot13_encoded,
)


def example_basic_caesar():
    """Basic Caesar cipher examples."""
    print("\n=== Basic Caesar Cipher ===")
    
    plaintext = "Hello, World!"
    print(f"Original:  {plaintext}")
    
    # Encrypt with shift of 3
    encrypted = caesar_cipher(plaintext, 3)
    print(f"Encrypted: {encrypted}")
    
    # Decrypt (negative shift)
    decrypted = caesar_cipher(encrypted, -3)
    print(f"Decrypted: {decrypted}")
    
    # Using result objects
    result = caesar_encrypt(plaintext, 3)
    print(f"\nCipherResult:")
    print(f"  Original: {result.original}")
    print(f"  Result:   {result.result}")
    print(f"  Shift:    {result.shift}")
    print(f"  Method:   {result.method}")


def example_rot_methods():
    """ROT cipher variants examples."""
    print("\n=== ROT Cipher Variants ===")
    
    text = "Hello, World! 123"
    print(f"Original: {text}")
    
    print(f"ROT5 (digits):  {rot5(text)}")
    print(f"ROT13 (letters): {rot13(text)}")
    print(f"ROT18 (both):   {rot18(text)}")
    print(f"ROT47 (ASCII):  {rot47(text)}")
    
    # All methods at once
    print("\n--- All Methods ---")
    results = rot_all(text)
    for method, result in results.items():
        print(f"  {method}: {result}")
    
    # Self-inverse property
    print("\n--- Self-inverse Property ---")
    print(f"ROT13 twice: {rot13(rot13(text))} (same as original)")
    print(f"ROT47 twice: {rot47(rot47(text))} (same as original)")
    print(f"ROT18 twice: {rot18(rot18(text))} (same as original)")


def example_atbash():
    """Atbash cipher examples."""
    print("\n=== Atbash Cipher ===")
    
    text = "HELLO WORLD"
    print(f"Original: {text}")
    
    encrypted = atbash_cipher(text)
    print(f"Atbash:   {encrypted}")
    
    decrypted = atbash_cipher(encrypted)
    print(f"Double:   {decrypted} (self-inverse)")


def example_vigenere():
    """Vigenere cipher examples."""
    print("\n=== Vigenere Cipher ===")
    
    plaintext = "ATTACK AT DAWN"
    key = "LEMON"
    
    print(f"Original: {plaintext}")
    print(f"Key:      {key}")
    
    encrypted = vigenere_cipher(plaintext, key)
    print(f"Encrypted: {encrypted}")
    
    decrypted = vigenere_cipher(encrypted, key, decrypt=True)
    print(f"Decrypted: {decrypted}")
    
    # Different key
    print("\n--- Different Key ---")
    key2 = "SECRET"
    encrypted2 = vigenere_cipher(plaintext, key2)
    print(f"Key '{key2}': {encrypted2}")


def example_affine():
    """Affine cipher examples."""
    print("\n=== Affine Cipher ===")
    
    plaintext = "HELLO"
    a = 5  # Must be coprime with 26
    b = 8
    
    print(f"Original: {plaintext}")
    print(f"Keys:     a={a}, b={b}")
    
    encrypted = affine_cipher(plaintext, a, b)
    print(f"Encrypted: {encrypted}")
    
    decrypted = affine_cipher(encrypted, a, b, decrypt=True)
    print(f"Decrypted: {decrypted}")
    
    # Valid a values
    print("\n--- Valid 'a' Values ---")
    print("Valid 'a' values (coprime with 26): 1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25")


def example_brute_force():
    """Brute force attack examples."""
    print("\n=== Brute Force Attack ===")
    
    ciphertext = "KHOOR ZRUOG"
    print(f"Ciphertext: {ciphertext}")
    
    results = brute_force_caesar(ciphertext, top_n=5)
    
    print("\nTop 5 candidates:")
    for r in results:
        print(f"  Shift {r.shift:2d}: {r.decrypted} (score: {r.score:.1f})")
    
    # Auto-detect
    detected_shift = detect_caesar_shift(ciphertext)
    print(f"\nDetected shift: {detected_shift}")
    
    decrypted = caesar_cipher(ciphertext, -detected_shift)
    print(f"Decrypted: {decrypted}")


def example_frequency_analysis():
    """Frequency analysis examples."""
    print("\n=== Frequency Analysis ===")
    
    # English text
    text = "The quick brown fox jumps over the lazy dog"
    print(f"Text: {text}")
    
    freq = frequency_analysis(text)
    
    # Sort by frequency
    sorted_freq = sorted(freq.items(), key=lambda x: -x[1])
    print("\nLetter frequencies:")
    for letter, percentage in sorted_freq[:10]:
        print(f"  '{letter}': {percentage:.1f}%")
    
    # Compare with ciphertext
    ciphertext = caesar_cipher(text, 10)
    cipher_freq = frequency_analysis(ciphertext)
    
    print(f"\nCiphertext (shift=10): {ciphertext}")
    print("\nCiphertext frequencies:")
    sorted_cipher_freq = sorted(cipher_freq.items(), key=lambda x: -x[1])
    for letter, percentage in sorted_cipher_freq[:10]:
        print(f"  '{letter}': {percentage:.1f}%")


def example_combined_operations():
    """Combined operations examples."""
    print("\n=== Combined Operations ===")
    
    text = "Secret Message 123"
    
    # Multiple rotations
    print(f"Original: {text}")
    print(f"ROT5 + ROT13: {multi_rot(text, [5, 13])}")
    
    # ROT13 then ROT47
    step1 = rot13(text)
    step2 = rot47(step1)
    print(f"\nROT13 then ROT47:")
    print(f"  Step 1 (ROT13): {step1}")
    print(f"  Step 2 (ROT47): {step2}")
    
    # ROT name helper
    print("\n--- ROT Names ---")
    for shift in [0, 1, 3, 13, 23, 26, 39]:
        print(f"  Shift {shift}: {shift_to_rot_name(shift)}")


def example_encoding_detection():
    """ROT13 encoding detection examples."""
    print("\n=== Encoding Detection ===")
    
    texts = [
        "Hello World",
        "URYYB JBEYQ",
        "The quick brown fox",
        "Gur dhvpx oebja sbk",
    ]
    
    for text in texts:
        likely_rot13 = is_rot13_encoded(text)
        print(f"'{text}': likely ROT13? {likely_rot13}")


def example_custom_alphabet():
    """Custom alphabet examples."""
    print("\n=== Custom Alphabet ===")
    
    # Standard alphabet
    standard = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
    # Custom alphabet (keyboard order)
    keyboard = "QWERTYUIOPASDFGHJKLZXCVBNM"
    
    text = "HELLO"
    
    print(f"Original: {text}")
    print(f"Standard (shift=3): {caesar_cipher(text, 3, standard)}")
    print(f"Keyboard (shift=3): {caesar_cipher(text, 3, keyboard)}")
    
    # Alphabet with numbers
    alphanumeric = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    text2 = "ABC123"
    print(f"\n'{text2}' with alphanumeric alphabet (shift=5):")
    print(f"  Result: {caesar_cipher(text2, 5, alphanumeric)}")


def example_practical_use_cases():
    """Practical use case examples."""
    print("\n=== Practical Use Cases ===")
    
    # 1. Simple password obfuscation (NOT secure encryption!)
    print("\n1. Simple Obfuscation:")
    password = "MySecret123"
    obfuscated = rot47(password)
    print(f"   Original:    {password}")
    print(f"   Obfuscated:  {obfuscated}")
    print(f"   Restored:    {rot47(obfuscated)}")
    print("   Note: This is NOT secure encryption!")
    
    # 2. Fun encoding for puzzles
    print("\n2. Puzzle Message:")
    message = "The treasure is buried under the old oak tree"
    encoded = rot13(message)
    print(f"   Encoded: {encoded}")
    print(f"   Hint: Use ROT13 to decode")
    
    # 3. Simple text scrambling for games
    print("\n3. Game Challenge:")
    challenge = "VICTORY"
    scrambled = atbash_cipher(challenge)
    print(f"   Challenge: Decode '{scrambled}' using Atbash cipher")
    print(f"   Answer: {atbash_cipher(scrambled)}")
    
    # 4. Quick one-time encoding
    print("\n4. Quick Note Encoding:")
    note = "Meeting at 3pm"
    encoded_note = rot18(note)
    print(f"   Note:    {note}")
    print(f"   Encoded: {encoded_note}")


def main():
    """Run all examples."""
    print("=" * 60)
    print("Rotation Cipher Utilities - Usage Examples")
    print("=" * 60)
    
    example_basic_caesar()
    example_rot_methods()
    example_atbash()
    example_vigenere()
    example_affine()
    example_brute_force()
    example_frequency_analysis()
    example_combined_operations()
    example_encoding_detection()
    example_custom_alphabet()
    example_practical_use_cases()
    
    print("\n" + "=" * 60)
    print("Examples completed!")
    print("=" * 60)


if __name__ == '__main__':
    main()