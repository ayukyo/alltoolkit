"""
AllToolkit - Python Base64 Utilities Example

Demonstrates usage of the Base64 encoding/decoding utilities.

Run with: python base64_utils_example.py
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'base64_utils'))

from mod import Base64Utils


def example_basic_encoding():
    """Example 1: Basic encoding and decoding."""
    print("\n" + "=" * 60)
    print("Example 1: Basic Encoding and Decoding")
    print("=" * 60)
    
    # Encode a string
    original = "Hello, World!"
    encoded = Base64Utils.encode(original)
    print(f"Original: {original}")
    print(f"Encoded:  {encoded}")
    
    # Decode back
    decoded = Base64Utils.decode(encoded)
    print(f"Decoded:  {decoded}")
    print(f"Match:    {original == decoded}")


def example_binary_data():
    """Example 2: Working with binary data."""
    print("\n" + "=" * 60)
    print("Example 2: Binary Data Encoding")
    print("=" * 60)
    
    # Binary data (could be image bytes, etc.)
    binary_data = bytes([0x00, 0x01, 0x02, 0xFF, 0xFE, 0xFD])
    print(f"Binary data: {binary_data}")
    
    # Encode to Base64
    encoded = Base64Utils.encode(binary_data)
    print(f"Encoded:     {encoded}")
    
    # Decode back to bytes
    decoded = Base64Utils.decode_to_bytes(encoded)
    print(f"Decoded:     {decoded}")
    print(f"Match:       {binary_data == decoded}")


def example_urlsafe():
    """Example 3: URL-safe Base64 for URLs and filenames."""
    print("\n" + "=" * 60)
    print("Example 3: URL-safe Base64 (RFC 4648)")
    print("=" * 60)
    
    # Data that produces + and / in standard Base64
    data = "hello+world/test>data"
    
    standard = Base64Utils.encode(data)
    urlsafe = Base64Utils.encode_urlsafe(data)
    urlsafe_no_pad = Base64Utils.encode_urlsafe(data, padding=False)
    
    print(f"Original:           {data}")
    print(f"Standard Base64:    {standard}")
    print(f"URL-safe Base64:    {urlsafe}")
    print(f"URL-safe (no pad):  {urlsafe_no_pad}")
    
    # Decode URL-safe
    decoded = Base64Utils.decode_urlsafe(urlsafe)
    print(f"Decoded:            {decoded}")
    print(f"Match:              {data == decoded}")


def example_conversion():
    """Example 4: Converting between standard and URL-safe."""
    print("\n" + "=" * 60)
    print("Example 4: Converting Between Formats")
    print("=" * 60)
    
    # Standard Base64 with + and /
    standard = "aGVsbG8+/test="
    print(f"Standard Base64:    {standard}")
    
    # Convert to URL-safe
    urlsafe = Base64Utils.to_urlsafe(standard)
    print(f"URL-safe:           {urlsafe}")
    
    # Convert back to standard
    back_to_standard = Base64Utils.from_urlsafe(urlsafe)
    print(f"Back to standard:   {back_to_standard}")
    print(f"Match:              {standard == back_to_standard}")


def example_validation():
    """Example 5: Validating Base64 strings."""
    print("\n" + "=" * 60)
    print("Example 5: Base64 Validation")
    print("=" * 60)
    
    valid_strings = [
        "SGVsbG8=",
        "YWJj",
        "",
    ]
    
    invalid_strings = [
        "Invalid!!!",
        "Not@Base64#",
    ]
    
    print("Valid strings:")
    for s in valid_strings:
        result = Base64Utils.is_valid(s)
        print(f"  '{s}' -> {result}")
    
    print("\nInvalid strings:")
    for s in invalid_strings:
        result = Base64Utils.is_valid(s)
        print(f"  '{s}' -> {result}")
    
    # URL-safe validation
    print("\nURL-safe validation:")
    urlsafe_valid = "aGVsbG8-"
    urlsafe_invalid = "aGVsbG8+"
    print(f"  '{urlsafe_valid}' (urlsafe=True) -> {Base64Utils.is_valid(urlsafe_valid, urlsafe=True)}")
    print(f"  '{urlsafe_invalid}' (urlsafe=True) -> {Base64Utils.is_valid(urlsafe_invalid, urlsafe=True)}")


def example_length_calculation():
    """Example 6: Calculating encoded/decoded lengths."""
    print("\n" + "=" * 60)
    print("Example 6: Length Calculations")
    print("=" * 60)
    
    test_lengths = [1, 2, 3, 10, 100, 1000]
    
    print(f"{'Input Length':<15} {'Encoded':<10} {'Encoded (no pad)':<20}")
    print("-" * 50)
    
    for length in test_lengths:
        encoded_with_pad = Base64Utils.encoded_length(length)
        encoded_no_pad = Base64Utils.encoded_length(length, padding=False)
        print(f"{length:<15} {encoded_with_pad:<10} {encoded_no_pad:<20}")
    
    print("\nMax decoded length from Base64:")
    base64_lengths = [4, 8, 100, 136]
    for bl in base64_lengths:
        max_decoded = Base64Utils.decoded_max_length(bl)
        print(f"  Base64 length {bl} -> max {max_decoded} bytes")


def example_unicode():
    """Example 7: Unicode and multi-byte characters."""
    print("\n" + "=" * 60)
    print("Example 7: Unicode Support")
    print("=" * 60)
    
    test_strings = [
        "Hello, 世界!",
        "🎉 Emoji support 🚀",
        "日本語テキスト",
        "العربية",
    ]
    
    for original in test_strings:
        encoded = Base64Utils.encode(original)
        decoded = Base64Utils.decode(encoded)
        print(f"Original: {original}")
        print(f"Encoded:  {encoded}")
        print(f"Decoded:  {decoded}")
        print(f"Match:    {original == decoded}\n")


def example_practical_use_cases():
    """Example 8: Practical use cases."""
    print("\n" + "=" * 60)
    print("Example 8: Practical Use Cases")
    print("=" * 60)
    
    # Use case 1: Encoding data for URL parameters
    print("\n1. URL Parameter Encoding:")
    user_data = "user+name@example.com"
    url_safe = Base64Utils.encode_urlsafe(user_data, padding=False)
    print(f"   Data: {user_data}")
    print(f"   URL-safe: {url_safe}")
    
    # Use case 2: Encoding binary data for JSON
    print("\n2. Binary Data for JSON:")
    binary = bytes([0x89, 0x50, 0x4E, 0x47])  # PNG file header
    json_safe = Base64Utils.encode(binary)
    print(f"   Binary: {binary}")
    print(f"   JSON-safe: {json_safe}")
    
    # Use case 3: Simple obfuscation
    print("\n3. Simple Data Obfuscation:")
    sensitive = "secret_token_12345"
    obfuscated = Base64Utils.encode(sensitive)
    print(f"   Original:    {sensitive}")
    print(f"   Obfuscated:  {obfuscated}")
    print(f"   Deobfuscated: {Base64Utils.decode(obfuscated)}")


def example_convenience_functions():
    """Example 9: Using convenience functions."""
    print("\n" + "=" * 60)
    print("Example 9: Convenience Functions")
    print("=" * 60)
    
    # Import convenience functions directly
    from mod import encode, decode, encode_urlsafe, is_valid
    
    # Use without class prefix
    original = "Quick test"
    encoded = encode(original)
    decoded = decode(encoded)
    
    print(f"Original: {original}")
    print(f"Encoded:  {encoded}")
    print(f"Decoded:  {decoded}")
    print(f"Valid:    {is_valid(encoded)}")


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("AllToolkit - Python Base64 Utilities Examples")
    print("=" * 60)
    
    examples = [
        example_basic_encoding,
        example_binary_data,
        example_urlsafe,
        example_conversion,
        example_validation,
        example_length_calculation,
        example_unicode,
        example_practical_use_cases,
        example_convenience_functions,
    ]
    
    for example in examples:
        try:
            example()
        except Exception as e:
            print(f"\nError in {example.__name__}: {e}")
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
