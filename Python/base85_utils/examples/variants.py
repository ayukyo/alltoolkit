"""
Base85 Variants Examples

Demonstrates different Base85 encoding variants.
"""

from mod import (
    encode, decode,
    encode_ascii85, decode_ascii85,
    encode_z85, decode_z85,
    get_charset,
)

# Compare all variants
print("=== Comparing All Variants ===")

data = b"Hello, World!"

for variant in ["rfc1924", "z85", "ascii85", "btoa"]:
    encoded = encode(data, variant=variant)
    decoded = decode(encoded, variant=variant)
    print(f"{variant:10s}: {encoded} -> {decoded}")

print()

# Ascii85 features
print("=== Ascii85 (Adobe/PDF/Git) ===")

# Basic Ascii85 encoding
data = b"Hello"
encoded = encode_ascii85(data)
print(f"Basic: '{data}' -> '{encoded}'")

# With frame delimiters
encoded_framed = encode_ascii85(data, frame=True)
print(f"Framed: '{data}' -> '{encoded_framed}'")

# Zero block abbreviation
data_with_zeros = b"\x00\x00\x00\x00Hello\x00\x00\x00\x00"
encoded_zeros = encode_ascii85(data_with_zeros)
print(f"Zero blocks: encoded as 'z' -> '{encoded_zeros}'")

# Decoding handles both framed and unframed
print(f"Decoded (unframed): {decode_ascii85(encoded)}")
print(f"Decoded (framed): {decode_ascii85(encoded_framed)}")

print()

# Z85 features (ZeroMQ)
print("=== Z85 (ZeroMQ) ===")

# Z85 uses printable characters only
charset = get_charset("z85")
print(f"Z85 charset: {charset[:20]}... (85 chars, all printable)")

# Perfect for configuration files
data = b"Config data"
encoded = encode_z85(data)
print(f"'{data}' -> '{encoded}'")

# ZeroMQ CURVE key encoding (32 bytes -> 40 chars)
print("\nZeroMQ CURVE key example:")
import os
key = os.urandom(32)
z85_key = encode_z85(key)
print(f"32-byte key -> {len(z85_key)} chars: {z85_key}")
decoded_key = decode_z85(z85_key)
print(f"Roundtrip OK: {key == decoded_key}")

print()

# Character set comparison
print("=== Character Set Comparison ===")

variants = ["rfc1924", "z85", "ascii85", "btoa"]
for v in variants:
    charset = get_charset(v)
    printable = all(c.isprintable() for c in charset)
    safe_for_json = all(c not in '"\\' for c in charset)
    print(f"{v:10s}: Printable={printable}, JSON-safe={safe_for_json}")