"""
IPv6 Encoding Examples (RFC 1924)

Demonstrates Base85 encoding for IPv6 addresses.
"""

from mod import encode_ipv6_to_base85, decode_base85_to_ipv6

print("=== IPv6 to Base85 (RFC 1924) ===")

# Common IPv6 addresses
test_addresses = [
    "::1",                                    # Loopback
    "2001:db8::1",                            # Documentation prefix
    "fe80::1",                                 # Link-local
    "2001:0db8:85a3:0000:0000:8a2e:0370:7334", # Full address
    "ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff", # All ones
]

for addr in test_addresses:
    encoded = encode_ipv6_to_base85(addr)
    decoded = decode_base85_to_ipv6(encoded)
    
    print(f"IPv6: {addr}")
    print(f"  Base85: {encoded} (20 chars)")
    print(f"  Decoded: {decoded}")
    print()

print()

# Compare lengths
print("=== Length Comparison ===")

addr = "2001:0db8:85a3:0000:0000:8a2e:0370:7334"
print(f"IPv6 address: {addr}")

# Different representations
colon_form = addr  # 39 chars
compressed_form = "2001:db8:85a3::8a2e:370:7334"  # 28 chars
base85_form = encode_ipv6_to_base85(addr)  # 20 chars

print(f"  Colon form:    {len(colon_form)} chars - '{colon_form}'")
print(f"  Compressed:    {len(compressed_form)} chars - '{compressed_form}'")
print(f"  Base85 (RFC1924): {len(base85_form)} chars - '{base85_form}'")

print()

# Practical usage
print("=== Practical IPv6 Encoding ===")

import ipaddress

# Generate some IPv6 addresses
print("Encoding network addresses:")
network = ipaddress.IPv6Network("2001:db8::/126")

for addr in network:
    encoded = encode_ipv6_to_base85(str(addr))
    decoded = decode_base85_to_ipv6(encoded)
    print(f"  {addr} -> {encoded} -> {decoded}")

print()

# Use in configuration
print("=== Configuration Example ===")

# Store IPv6 addresses in Base85 for compact config
config = {
    "gateway": encode_ipv6_to_base85("2001:db8::1"),
    "dns_primary": encode_ipv6_to_base85("2001:db8::53"),
    "dns_secondary": encode_ipv6_to_base85("2001:db8::54"),
}

print("Compact IPv6 configuration:")
for key, value in config.items():
    decoded = decode_base85_to_ipv6(value)
    print(f"  {key}: {value} ({decoded})")

print()

# Error handling
print("=== Error Handling ===")

from mod import Base85Error

try:
    encode_ipv6_to_base85("invalid-address")
except Base85Error as e:
    print(f"Invalid IPv6: {e}")

try:
    decode_base85_to_ipv6("short")  # Wrong length
except Base85Error as e:
    print(f"Wrong length: {e}")