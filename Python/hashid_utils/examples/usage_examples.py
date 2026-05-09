#!/usr/bin/env python3
"""
Usage examples for hashid_utils module.

Demonstrates:
- Basic encoding/decoding
- Custom salt and alphabet
- Minimum length padding
- Multiple numbers
- Pre-configured classes
- Real-world use cases
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hashid_utils.mod import (
    HashID,
    encode_id,
    decode_id,
    encode_ids,
    decode_ids,
    is_valid_hashid,
    estimate_length,
    YouTubeHashID,
    ShortHashID,
)


def example_basic_encoding():
    """Basic encode and decode operations."""
    print("\n" + "="*60)
    print("Example 1: Basic Encoding/Decoding")
    print("="*60)
    
    # Create a HashID instance
    h = HashID()
    
    # Encode a number
    encoded = h.encode(12345)
    print(f"Encoded 12345: {encoded}")
    
    # Decode back to number
    decoded = h.decode(encoded)
    print(f"Decoded '{encoded}': {decoded}")
    
    # Single number methods
    encoded_single = h.encode_single(67890)
    decoded_single = h.decode_single(encoded_single)
    print(f"\nSingle encode/decode:")
    print(f"  Encoded 67890: {encoded_single}")
    print(f"  Decoded: {decoded_single}")


def example_custom_salt():
    """Using custom salt for unique encoding."""
    print("\n" + "="*60)
    print("Example 2: Custom Salt")
    print("="*60)
    
    # Each app should use its own salt
    app1 = HashID(salt="my awesome app secret")
    app2 = HashID(salt="another app secret")
    
    number = 999
    
    # Same number, different salts = different hashes
    hash1 = app1.encode(number)
    hash2 = app2.encode(number)
    
    print(f"Number: {number}")
    print(f"App 1 hash: {hash1}")
    print(f"App 2 hash: {hash2}")
    print(f"Different? {hash1 != hash2}")
    
    # Each can decode its own hash
    print(f"\nApp 1 decodes its hash: {app1.decode(hash1)}")
    print(f"App 2 decodes its hash: {app2.decode(hash2)}")
    
    # Wrong salt gives different result
    wrong = app2.decode(hash1)
    print(f"\nApp 2 decodes App 1's hash: {wrong} (different!)")


def example_min_length():
    """Minimum length padding."""
    print("\n" + "="*60)
    print("Example 3: Minimum Length Padding")
    print("="*60)
    
    # Without min_length
    h1 = HashID()
    short_hash = h1.encode(1)
    print(f"Without min_length, encode(1): '{short_hash}' (length: {len(short_hash)})")
    
    # With min_length
    h2 = HashID(min_length=8)
    padded_hash = h2.encode(1)
    print(f"With min_length=8, encode(1): '{padded_hash}' (length: {len(padded_hash)})")
    
    # Different min_lengths
    for min_len in [4, 6, 8, 10, 12]:
        h = HashID(min_length=min_len)
        encoded = h.encode(42)
        print(f"min_length={min_len:2d}: '{encoded}' (actual: {len(encoded)})")


def example_multiple_numbers():
    """Encoding multiple numbers at once."""
    print("\n" + "="*60)
    print("Example 4: Multiple Numbers")
    print("="*60)
    
    h = HashID(salt="multi-number demo")
    
    # Encode multiple IDs together
    user_id = 12345
    post_id = 67890
    comment_id = 11111
    
    encoded = h.encode(user_id, post_id, comment_id)
    print(f"Encoding: user_id={user_id}, post_id={post_id}, comment_id={comment_id}")
    print(f"Combined hash: {encoded}")
    
    # Decode back to list
    decoded = h.decode(encoded)
    print(f"Decoded: {decoded}")
    
    # Use in URL
    url = f"https://example.com/comments/{encoded}"
    print(f"\nURL example: {url}")


def example_custom_alphabet():
    """Custom alphabet for specific needs."""
    print("\n" + "="*60)
    print("Example 5: Custom Alphabet")
    print("="*60)
    
    # Hexadecimal only (for systems that prefer lowercase hex)
    h_hex = HashID(alphabet="0123456789abcdef")
    encoded = h_hex.encode(12345)
    print(f"Hex alphabet: {encoded}")
    
    # Lowercase only (case-insensitive systems)
    h_lower = HashID(alphabet="abcdefghijklmnopqrstuvwxyz")
    encoded = h_lower.encode(12345)
    print(f"Lowercase only: {encoded}")
    
    # Numbers only (for numeric-only fields)
    h_nums = HashID(alphabet="0123456789")
    encoded = h_nums.encode(12345)
    print(f"Numbers only: {encoded}")
    
    # Custom business-friendly alphabet
    business_alphabet = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"  # No I, O, 1, 0 (confusing)
    h_biz = HashID(alphabet=business_alphabet)
    encoded = h_biz.encode(12345)
    print(f"Business-friendly: {encoded}")


def example_preconfigured():
    """Using pre-configured classes."""
    print("\n" + "="*60)
    print("Example 6: Pre-configured Classes")
    print("="*60)
    
    # YouTube-style IDs (11 characters minimum)
    yt = YouTubeHashID(salt="my video site")
    video_id = yt.encode(123456789)
    print(f"YouTube-style ID: {video_id} (length: {len(video_id)})")
    
    # Short IDs (4 characters minimum)
    short = ShortHashID(salt="my short url")
    short_id = short.encode(123)
    print(f"Short ID: {short_id} (length: {len(short_id)})")


def example_convenience_functions():
    """Using convenience functions."""
    print("\n" + "="*60)
    print("Example 7: Convenience Functions")
    print("="*60)
    
    # Quick single ID encode/decode
    encoded = encode_id(999, salt="my app")
    print(f"encode_id(999): {encoded}")
    
    decoded = decode_id(encoded, salt="my app")
    print(f"decode_id('{encoded}'): {decoded}")
    
    # Quick multi-ID encode/decode
    encoded = encode_ids(1, 2, 3, salt="my app")
    print(f"\nencode_ids(1, 2, 3): {encoded}")
    
    decoded = decode_ids(encoded, salt="my app")
    print(f"decode_ids('{encoded}'): {decoded}")
    
    # Validation
    print(f"\nis_valid_hashid('{encoded}'): {is_valid_hashid(encoded)}")
    print(f"is_valid_hashid('invalid@id'): {is_valid_hashid('invalid@id')}")


def example_real_world_use_cases():
    """Real-world use cases."""
    print("\n" + "="*60)
    print("Example 8: Real-World Use Cases")
    print("="*60)
    
    # 1. URL shortening
    print("\n1. URL Shortening Service")
    h = HashID(salt="url shortener", min_length=6)
    
    database_id = 1234567
    short_code = h.encode(database_id)
    print(f"   Database ID: {database_id}")
    print(f"   Short URL: https://short.url/{short_code}")
    
    # 2. User-facing IDs
    print("\n2. User-facing IDs (hide database IDs)")
    h = HashID(salt="my app", min_length=8)
    
    user_id = 1  # Don't want users to see ID=1
    order_id = 42
    
    user_hash = h.encode(user_id)
    order_hash = h.encode(order_id)
    
    print(f"   User ID: {user_id} → Public: {user_hash}")
    print(f"   Order ID: {order_id} → Public: {order_hash}")
    
    # 3. Combined resource IDs
    print("\n3. Combined Resource IDs")
    h = HashID(salt="resource ids", min_length=10)
    
    user_id = 123
    post_id = 456
    comment_id = 789
    
    combined = h.encode(user_id, post_id, comment_id)
    print(f"   User: {user_id}, Post: {post_id}, Comment: {comment_id}")
    print(f"   Combined: {combined}")
    print(f"   Decoded: {h.decode(combined)}")
    
    # 4. Order confirmation codes
    print("\n4. Order Confirmation Codes")
    h = HashID(salt="order codes", min_length=12)
    
    order_num = 1000001
    confirmation = h.encode(order_num)
    print(f"   Order #{order_num}")
    print(f"   Confirmation: {confirmation}")
    
    # 5. API key generation
    print("\n5. API Key Generation")
    h = HashID(salt="api keys", min_length=32)
    
    user_id = 999
    timestamp = 1609459200  # 2021-01-01
    api_key = h.encode(user_id, timestamp)
    print(f"   User: {user_id}, Timestamp: {timestamp}")
    print(f"   API Key: {api_key}")


def example_length_estimation():
    """Length estimation for planning."""
    print("\n" + "="*60)
    print("Example 9: Length Estimation")
    print("="*60)
    
    print("Estimated hash length for numbers:")
    for num in [10, 100, 1000, 10000, 100000, 1000000, 10000000]:
        est = estimate_length(num)
        print(f"  {num:>10,}: {est} characters")
    
    print("\nWith hex alphabet (16 chars):")
    for num in [10, 100, 1000, 10000, 100000, 1000000]:
        est = estimate_length(num, alphabet_length=16)
        print(f"  {num:>10,}: {est} characters")


def example_deterministic():
    """Demonstrating deterministic encoding."""
    print("\n" + "="*60)
    print("Example 10: Deterministic Encoding")
    print("="*60)
    
    h = HashID(salt="consistent")
    
    # Same input always produces same output
    print("Same input, multiple calls:")
    for i in range(5):
        encoded = h.encode(12345)
        print(f"  Call {i+1}: {encoded}")
    
    print("\nThis allows:")
    print("  - Predictable IDs for caching")
    print("  - ID generation without database storage")
    print("  - Reproducible hashes across services")


def main():
    """Run all examples."""
    print("="*60)
    print("HashID Utils - Usage Examples")
    print("="*60)
    
    example_basic_encoding()
    example_custom_salt()
    example_min_length()
    example_multiple_numbers()
    example_custom_alphabet()
    example_preconfigured()
    example_convenience_functions()
    example_real_world_use_cases()
    example_length_estimation()
    example_deterministic()
    
    print("\n" + "="*60)
    print("Examples completed!")
    print("="*60)


if __name__ == "__main__":
    main()