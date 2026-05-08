#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Steganography Utilities Examples
==============================================
Practical examples demonstrating steganography utility module usage.

Examples cover:
- Hiding messages in text using zero-width characters
- Whitespace-based hidden messages
- Case-based steganography for secure communication
- Detection and analysis of hidden content
- Real-world application scenarios
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from steganography_utils.mod import (
    # Core functions
    text_to_binary,
    binary_to_text,
    
    # Zero-width steganography
    encode_zw_steganography,
    decode_zw_steganography,
    detect_zw_steganography,
    remove_zw_steganography,
    
    # Whitespace steganography
    encode_whitespace_steganography,
    decode_whitespace_steganography,
    detect_whitespace_steganography,
    
    # Case-based steganography
    encode_case_steganography,
    decode_case_steganography,
    auto_decode_case_steganography,
    
    # Variation selector steganography
    encode_variation_selector_steganography,
    decode_variation_selector_steganography,
    
    # Analysis
    analyze_steganography,
    clean_all_steganography,
    
    # Capacity
    calculate_zw_capacity,
    calculate_case_capacity,
)


def example_binary_conversion():
    """Example: Basic binary conversion."""
    print("=" * 60)
    print("Example 1: Binary Conversion")
    print("=" * 60)
    
    # Convert text to binary
    text = "Hello"
    binary = text_to_binary(text)
    print(f"Text: '{text}'")
    print(f"Binary: '{binary}'")
    
    # Convert binary back to text
    decoded = binary_to_text(binary)
    print(f"Decoded: '{decoded}'")
    
    # Unicode support
    unicode_text = "你好"
    unicode_binary = text_to_binary(unicode_text)
    unicode_decoded = binary_to_text(unicode_binary)
    print(f"\nUnicode text: '{unicode_text}'")
    print(f"Unicode binary: '{unicode_binary}'")
    print(f"Unicode decoded: '{unicode_decoded}'")
    print()


def example_zw_steganography():
    """Example: Zero-width character steganography."""
    print("=" * 60)
    print("Example 2: Zero-Width Character Steganography")
    print("=" * 60)
    
    # Hide a secret message in cover text
    cover_text = "This is a normal message that looks innocent."
    secret_message = "Hidden secret!"
    
    print(f"Cover text: '{cover_text}'")
    print(f"Secret message: '{secret_message}'")
    
    # Encode the secret
    stego_text = encode_zw_steganography(cover_text, secret_message)
    
    print(f"\nStego text (visible): '{stego_text}'")
    print(f"Stego text length: {len(stego_text)}")
    print(f"Cover text length: {len(cover_text)}")
    print(f"Hidden characters: {len(stego_text) - len(cover_text) - 1}")
    
    # Decode the secret
    decoded_message = decode_zw_steganography(stego_text)
    print(f"\nDecoded message: '{decoded_message}'")
    
    # Detect steganography
    detected, count, hidden_msg = detect_zw_steganography(stego_text)
    print(f"Detection result:")
    print(f"  - Detected: {detected}")
    print(f"  - Hidden char count: {count}")
    print(f"  - Hidden message: '{hidden_msg}'")
    print()


def example_whitespace_steganography():
    """Example: Whitespace steganography."""
    print("=" * 60)
    print("Example 3: Whitespace Steganography")
    print("=" * 60)
    
    # Hide message using trailing whitespace
    cover_text = "This message will have hidden whitespace."
    secret_message = "Secret code"
    
    print(f"Cover text: '{cover_text}'")
    print(f"Secret message: '{secret_message}'")
    
    stego_text = encode_whitespace_steganography(cover_text, secret_message)
    
    visible_part = stego_text.split('\n')[0]
    print(f"\nStego text (with trailing whitespace):")
    print(f"  Visible part: '{visible_part}'")
    print(f"  Hidden part: spaces and tabs")
    
    # Decode
    decoded = decode_whitespace_steganography(stego_text)
    print(f"Decoded message: '{decoded}'")
    
    # Detect
    detected, ws_count, hidden_msg = detect_whitespace_steganography(stego_text)
    print(f"Detection: found={detected}, whitespace chars={ws_count}")
    print()


def example_case_steganography():
    """Example: Case-based steganography."""
    print("=" * 60)
    print("Example 4: Case-Based Steganography")
    print("=" * 60)
    
    # Need enough alphabetic characters in cover
    cover_text = "abcdefghijklmnopqrstuvwxyz"
    secret_message = "X"
    
    print(f"Cover text: '{cover_text}'")
    print(f"Secret message: '{secret_message}'")
    print(f"Capacity: {calculate_case_capacity(cover_text)} characters")
    
    # Encode
    stego_text = encode_case_steganography(cover_text, secret_message)
    
    print(f"\nStego text: '{stego_text}'")
    print("Note: Some letters are uppercase to encode the secret")
    
    # Decode with known length
    decoded = decode_case_steganography(stego_text, len(secret_message))
    print(f"Decoded message: '{decoded}'")
    
    # Auto decode
    auto_decoded = auto_decode_case_steganography(stego_text)
    print(f"Auto-decoded: '{auto_decoded}'")
    print()


def example_variation_selector():
    """Example: Variation selector steganography."""
    print("=" * 60)
    print("Example 5: Variation Selector Steganography")
    print("=" * 60)
    
    cover_text = "Hello World"
    secret_message = "Hidden"
    
    print(f"Cover text: '{cover_text}'")
    print(f"Secret message: '{secret_message}'")
    
    # Encode
    stego_text = encode_variation_selector_steganography(cover_text, secret_message)
    
    print(f"\nStego text length: {len(stego_text)}")
    print(f"Cover text length: {len(cover_text)}")
    print(f"Added variation selectors: {len(stego_text) - len(cover_text)}")
    
    # Decode
    decoded = decode_variation_selector_steganography(stego_text)
    print(f"Decoded message: '{decoded}'")
    print()


def example_analysis():
    """Example: Comprehensive steganography analysis."""
    print("=" * 60)
    print("Example 6: Steganography Analysis")
    print("=" * 60)
    
    # Create sample with zero-width steganography
    stego_zw = encode_zw_steganography("Hello", "Secret ZW")
    
    print("Analyzing text with zero-width steganography:")
    analysis = analyze_steganography(stego_zw)
    
    print(f"  Zero-width detected: {analysis['zero_width']['detected']}")
    print(f"  Hidden characters: {analysis['zero_width']['char_count']}")
    print(f"  Hidden message: '{analysis['zero_width']['message']}'")
    
    print(f"\n  Suspicious: {analysis['suspicious']}")
    print(f"  Total hidden chars: {analysis['total_hidden_chars']}")
    
    # Clean the text
    cleaned = clean_all_steganography(stego_zw)
    print(f"\nCleaned text: '{cleaned}'")
    
    # Verify it's clean
    clean_analysis = analyze_steganography(cleaned)
    print(f"Analysis after cleaning:")
    print(f"  Suspicious: {clean_analysis['suspicious']}")
    print()


def example_security_scenario():
    """Example: Security scenario - hidden communication."""
    print("=" * 60)
    print("Example 7: Security Scenario - Hidden Communication")
    print("=" * 60)
    
    # Scenario: Two parties communicating with hidden messages
    # Party A sends a message with hidden content
    public_message = "Meeting at 3pm tomorrow."
    secret_instruction = "Bring documents"
    
    # Party A encodes
    encoded_message = encode_zw_steganography(public_message, secret_instruction)
    
    print("Party A sends:")
    print(f"  Visible message: '{public_message}'")
    print(f"  Hidden instruction: '{secret_instruction}'")
    
    # Party B receives and decodes
    received_analysis = analyze_steganography(encoded_message)
    
    print("\nParty B analyzes received message:")
    print(f"  Detected hidden content: {received_analysis['suspicious']}")
    
    if received_analysis['zero_width']['detected']:
        hidden = received_analysis['zero_width']['message']
        print(f"  Extracted instruction: '{hidden}'")
    
    # Eavesdropper sees only visible content
    print("\nEavesdropper sees:")
    print(f"  '{encoded_message}'")  # Looks identical to visible text
    print("  (Hidden characters are invisible)")
    print()


def example_capacity_planning():
    """Example: Planning capacity for different methods."""
    print("=" * 60)
    print("Example 8: Capacity Planning")
    print("=" * 60)
    
    cover_length = 200
    
    print(f"Cover text length: {cover_length} characters")
    print(f"\nMaximum message capacity:")
    print(f"  Zero-width method: ~{calculate_zw_capacity(cover_length)} chars")
    print(f"  Whitespace method: ~{calculate_zw_capacity(cover_length)} chars")
    
    cover_sample = "aBcDeFgHiJkLmNoPqRsTuVwXyZ" * 10
    case_capacity = calculate_case_capacity(cover_sample)
    print(f"  Case-based method (sample): {case_capacity} chars")
    
    print("\nRecommendations:")
    print("  - Zero-width: Good for any cover text, invisible")
    print("  - Whitespace: Simple, but may be stripped by some systems")
    print("  - Case-based: Limited capacity, requires alphabetic cover")
    print()


def example_multi_layer():
    """Example: Multi-layer steganography."""
    print("=" * 60)
    print("Example 9: Multi-Layer Steganography")
    print("=" * 60)
    
    # Combine multiple methods for extra security
    cover_text = "abcdefghijklmnopqrstuvwxyz"
    
    # First layer: case-based
    secret1 = "A"
    layer1 = encode_case_steganography(cover_text, secret1)
    
    # Second layer: zero-width (added to case-modified text)
    secret2 = "Second layer"
    layer2 = encode_zw_steganography(layer1, secret2)
    
    print("Multi-layer encoding:")
    print(f"  Layer 1 (case-based): '{secret1}'")
    print(f"  Layer 2 (zero-width): '{secret2}'")
    
    # Decode both layers
    decoded2 = decode_zw_steganography(layer2)
    decoded1 = decode_case_steganography(layer2, len(secret1))
    
    print("\nDecoded:")
    print(f"  Layer 2: '{decoded2}'")
    print(f"  Layer 1: '{decoded1}'")
    print()


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("AllToolkit Steganography Utilities - Usage Examples")
    print("=" * 60 + "\n")
    
    example_binary_conversion()
    example_zw_steganography()
    example_whitespace_steganography()
    example_case_steganography()
    example_variation_selector()
    example_analysis()
    example_security_scenario()
    example_capacity_planning()
    example_multi_layer()
    
    print("=" * 60)
    print("All examples completed successfully!")
    print("=" * 60)


if __name__ == '__main__':
    main()