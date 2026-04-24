"""
Base85 Basic Usage Examples

Demonstrates basic encoding and decoding operations.
"""

from mod import encode, decode, is_valid

# Basic encoding
print("=== Basic Encoding ===")

data = b"Hello, World!"
encoded = encode(data)
print(f"Original: {data}")
print(f"Encoded:  {encoded}")
print(f"Decoded:  {decode(encoded)}")

print()

# String encoding (auto-converts to UTF-8 bytes)
print("=== String Encoding ===")

text = "你好世界 Hello World"
encoded = encode(text)
decoded = decode(encoded).decode("utf-8")
print(f"Original: {text}")
print(f"Encoded:  {encoded}")
print(f"Decoded:  {decoded}")

print()

# Validation
print("=== Validation ===")

encoded = encode(b"Test data")
print(f"Is '{encoded}' valid? {is_valid(encoded)}")
print(f"Is 'invalid!!!' valid? {is_valid('invalid!!!')}")

print()

# Size estimation
print("=== Size Estimation ===")

from mod import estimate_encoded_size, estimate_decoded_size

original_size = 100
encoded_size = estimate_encoded_size(original_size)
decoded_size = estimate_decoded_size(encoded_size)

print(f"Original size: {original_size} bytes")
print(f"Estimated encoded size: {encoded_size} characters")
print(f"Estimated decoded size: {decoded_size} bytes")

print()

# Comparison with Base64
print("=== Comparison with Base64 ===")

from mod import compare_with_base64

data = bytes(range(256)) * 10  # 2560 bytes
comparison = compare_with_base64(data)

print(f"Original size: {comparison['original_size']} bytes")
print(f"Base85 size: {comparison['base85_size']} chars ({comparison['base85_overhead']:.1%} overhead)")
print(f"Base64 size: {comparison['base64_size']} chars ({comparison['base64_overhead']:.1%} overhead)")
print(f"Base85 efficiency: {comparison['base85_efficiency']:.2f}x relative to Base64")

print()

# Different data sizes
print("=== Encoding Various Sizes ===")

for size in [1, 2, 3, 4, 5, 8, 16, 32]:
    data = bytes(range(size))
    encoded = encode(data)
    decoded = decode(encoded)
    print(f"{size} bytes -> {len(encoded)} chars -> {len(decoded)} bytes (roundtrip OK: {data == decoded})")