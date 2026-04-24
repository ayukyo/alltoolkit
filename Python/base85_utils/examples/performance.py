"""
Base85 Performance Examples

Demonstrates performance characteristics and benchmarks.
"""

from mod import encode, decode, compare_with_base64
import time
import os

print("=== Encoding Performance ===")

# Test different sizes
sizes = [100, 1000, 10000, 100000]
iterations = 100

for size in sizes:
    data = os.urandom(size)
    
    # Measure encoding
    start = time.time()
    for _ in range(iterations):
        encoded = encode(data)
    encode_time = time.time() - start
    
    # Measure decoding
    start = time.time()
    for _ in range(iterations):
        decoded = decode(encoded)
    decode_time = time.time() - start
    
    throughput_encode = (size * iterations) / encode_time / 1024  # KB/s
    throughput_decode = (size * iterations) / decode_time / 1024
    
    print(f"Size {size:6d} bytes:")
    print(f"  Encode: {encode_time:.4f}s ({throughput_encode:.1f} KB/s)")
    print(f"  Decode: {decode_time:.4f}s ({throughput_decode:.1f} KB/s)")

print()

# Compare with Base64
print("=== Efficiency vs Base64 ===")

data_sizes = [10, 100, 1000, 10000]

for size in data_sizes:
    data = os.urandom(size)
    comparison = compare_with_base64(data)
    
    print(f"Size {size} bytes:")
    print(f"  Base85: {comparison['base85_size']} chars ({comparison['base85_overhead']:.1%} overhead)")
    print(f"  Base64: {comparison['base64_size']} chars ({comparison['base64_overhead']:.1%} overhead)")
    print(f"  Base85 efficiency: {comparison['base85_efficiency']:.2f}x")
    print()

print()

# Detailed comparison for large data
print("=== Large Data Comparison ===")

large_data = bytes(range(256)) * 100  # 25.6 KB
comparison = compare_with_base64(large_data)

print(f"Original: {comparison['original_size']} bytes")
print(f"Base85 encoded: {comparison['base85_size']} chars")
print(f"Base64 encoded: {comparison['base64_size']} chars")
print(f"Base85 saves: {comparison['base64_size'] - comparison['base85_size']} chars")
print(f"Savings percentage: {(1 - comparison['base85_size']/comparison['base64_size'])*100:.1f}%")

print()

# Memory efficiency
print("=== Streaming vs One-Shot for Large Data ===")

large_data = os.urandom(1000000)  # 1 MB

# One-shot encoding
start = time.time()
one_shot_encoded = encode(large_data)
one_shot_time = time.time() - start

# Streaming encoding
from mod import Base85Iterator

iterator = Base85Iterator()
stream_encoded_parts = []

start = time.time()
for i in range(0, len(large_data), 4096):
    chunk = large_data[i:i+4096]
    partial = iterator.update(chunk)
    stream_encoded_parts.append(partial)
stream_encoded_parts.append(iterator.finalize())
stream_encoded = "".join(stream_encoded_parts)
stream_time = time.time() - start

print(f"1 MB data:")
print(f"  One-shot time: {one_shot_time:.4f}s")
print(f"  Streaming time: {stream_time:.4f}s")
print(f"  Results match: {one_shot_encoded == stream_encoded}")

print()

# Different variants performance
print("=== Variant Performance Comparison ===")

data = os.urandom(10000)
variants = ["rfc1924", "z85", "ascii85", "btoa"]
iterations = 100

for variant in variants:
    start = time.time()
    for _ in range(iterations):
        encoded = encode(data, variant=variant)
    encode_time = time.time() - start
    
    start = time.time()
    for _ in range(iterations):
        decoded = decode(encoded, variant=variant)
    decode_time = time.time() - start
    
    print(f"{variant:10s}: encode {encode_time:.4f}s, decode {decode_time:.4f}s")