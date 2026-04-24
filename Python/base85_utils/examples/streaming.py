"""
Base85 Streaming Encoding Examples

Demonstrates streaming encoding for large data.
"""

from mod import Base85Iterator, encode, decode

print("=== Streaming Encoding ===")

# Create iterator
iterator = Base85Iterator()

# Simulate streaming data
chunks = [b"First chunk ", b"Second chunk ", b"Third chunk ", b"Final"]

# Process each chunk
result = ""
for chunk in chunks:
    partial = iterator.update(chunk)
    if partial:
        print(f"Processed chunk: '{chunk.decode()}' -> '{partial}'")
        result += partial

# Finalize (process remaining bytes)
final = iterator.finalize()
if final:
    print(f"Finalized: '{final}'")
result += final

print(f"Full encoded: '{result}'")

# Decode and verify
full_data = b"".join(chunks)
decoded = decode(result)
print(f"Decoded: '{decoded.decode()}'")
print(f"Match: {decoded == full_data}")

print()

# Streaming with large data
print("=== Large Data Streaming ===")

import os

# Generate large data
large_data = os.urandom(10000)

# Stream in chunks of 100 bytes
iterator = Base85Iterator()
encoded_parts = []

for i in range(0, len(large_data), 100):
    chunk = large_data[i:i+100]
    partial = iterator.update(chunk)
    if partial:
        encoded_parts.append(partial)

# Finalize
final = iterator.finalize()
if final:
    encoded_parts.append(final)

full_encoded = "".join(encoded_parts)

# Compare with one-shot encoding
one_shot = encode(large_data)

print(f"Large data size: {len(large_data)} bytes")
print(f"Streaming encoded size: {len(full_encoded)} chars")
print(f"One-shot encoded size: {len(one_shot)} chars")
print(f"Results match: {full_encoded == one_shot}")
print(f"Roundtrip OK: {decode(full_encoded) == large_data}")

print()

# Different variants streaming
print("=== Streaming with Different Variants ===")

data = b"Testing streaming with different variants"

for variant in ["rfc1924", "z85", "ascii85", "btoa"]:
    iterator = Base85Iterator(variant=variant)
    result = iterator.update(data) + iterator.finalize()
    decoded = decode(result, variant=variant)
    match = decoded == data
    print(f"{variant:10s}: {len(result)} chars, roundtrip OK: {match}")