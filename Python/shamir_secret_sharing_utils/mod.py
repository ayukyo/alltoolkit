#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Shamir's Secret Sharing Utilities Module
======================================================
A comprehensive Shamir's Secret Sharing (SSS) implementation with zero external dependencies.

Shamir's Secret Sharing is a cryptographic algorithm that divides a secret into n shares,
where any k or more shares can reconstruct the original secret, but fewer than k shares
reveal no information about the secret.

Features:
    - Split secrets into shares with configurable threshold
    - Reconstruct secrets from shares
    - Support for arbitrary secret sizes
    - Secure random polynomial generation
    - Verification and validation utilities
    - Share encoding/decoding utilities
    - Support for both text and binary secrets

Security:
    - Uses cryptographically secure random number generation
    - Operates over finite fields (GF(2^8) for bytes, or custom prime fields)
    - Information-theoretic security (k-1 shares reveal zero information)

Author: AllToolkit Contributors
License: MIT
"""

import secrets
import struct
from typing import List, Tuple, Optional, Union, Dict, Any
from dataclasses import dataclass
import hashlib


# Large primes for field arithmetic
PRIME_128 = 2**128 - 159
PRIME_256 = 2**256 - 189
PRIME_512 = 2**512 - 569
PRIME_1024 = 2**1024 - 1057

# Default prime (512-bit for better compatibility with long strings)
DEFAULT_PRIME = PRIME_512


def _select_prime(secret_int: int) -> int:
    """Select appropriate prime based on secret size."""
    if secret_int < PRIME_128:
        return PRIME_128
    elif secret_int < PRIME_256:
        return PRIME_256
    elif secret_int < PRIME_512:
        return PRIME_512
    elif secret_int < PRIME_1024:
        return PRIME_1024
    else:
        raise ValueError("Secret too large. Maximum supported size is 1024 bits.")


@dataclass
class Share:
    """Represents a single share in Shamir's Secret Sharing."""
    x: int  # x-coordinate (share index)
    y: int  # y-coordinate (share value)
    prime: int  # The prime used for field arithmetic
    threshold: int  # Minimum shares needed to reconstruct
    
    def encode(self) -> str:
        """Encode share to a portable string format."""
        # Format: base16(threshold):base16(x):base16(y):base16(prime)[:8]
        prime_short = self.prime
        return f"{self.threshold:x}:{self.x:x}:{self.y:x}:{prime_short:x}"
    
    @classmethod
    def decode(cls, encoded: str) -> 'Share':
        """Decode a share from string format."""
        parts = encoded.split(':')
        if len(parts) != 4:
            raise ValueError("Invalid share format")
        threshold = int(parts[0], 16)
        x = int(parts[1], 16)
        y = int(parts[2], 16)
        prime = int(parts[3], 16)
        return cls(x=x, y=y, prime=prime, threshold=threshold)
    
    def __repr__(self) -> str:
        return f"Share(x={self.x}, y=..., threshold={self.threshold})"


@dataclass
class ShareSet:
    """A collection of shares for a single secret."""
    shares: List[Share]
    secret_hash: Optional[str] = None  # SHA-256 hash for verification
    
    def encode(self) -> str:
        """Encode all shares to a portable string."""
        lines = []
        if self.secret_hash:
            lines.append(f"# hash:{self.secret_hash}")
        for share in self.shares:
            lines.append(share.encode())
        return "\n".join(lines)
    
    @classmethod
    def decode(cls, encoded: str) -> 'ShareSet':
        """Decode a share set from string format."""
        lines = encoded.strip().split('\n')
        shares = []
        secret_hash = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if line.startswith('# hash:'):
                secret_hash = line[7:]
            else:
                shares.append(Share.decode(line))
        
        return cls(shares=shares, secret_hash=secret_hash)


def _mod_inverse(a: int, prime: int) -> int:
    """
    Calculate modular multiplicative inverse using extended Euclidean algorithm.
    Returns x such that (a * x) % prime == 1
    """
    if a < 0:
        a = a % prime
    
    def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y
    
    gcd, x, _ = extended_gcd(a % prime, prime)
    if gcd != 1:
        raise ValueError("Modular inverse does not exist")
    return (x % prime + prime) % prime


def _evaluate_polynomial(coefficients: List[int], x: int, prime: int) -> int:
    """Evaluate polynomial at point x using Horner's method."""
    result = 0
    for coeff in reversed(coefficients):
        result = (result * x + coeff) % prime
    return result


def _lagrange_interpolation(shares: List[Tuple[int, int]], prime: int) -> int:
    """
    Reconstruct the secret using Lagrange interpolation.
    shares: list of (x, y) tuples
    Returns the secret (f(0))
    """
    secret = 0
    n = len(shares)
    
    for i in range(n):
        xi, yi = shares[i]
        
        # Calculate Lagrange basis polynomial at x=0
        numerator = 1
        denominator = 1
        
        for j in range(n):
            if i != j:
                xj = shares[j][0]
                numerator = (numerator * (-xj)) % prime
                denominator = (denominator * (xi - xj)) % prime
        
        # Compute the Lagrange coefficient
        lagrange_coeff = (numerator * _mod_inverse(denominator, prime)) % prime
        
        # Add the contribution from this share
        secret = (secret + yi * lagrange_coeff) % prime
    
    return secret


def split_secret(
    secret: Union[int, bytes, str],
    threshold: int,
    num_shares: int,
    prime: Optional[int] = None,
    include_hash: bool = True
) -> ShareSet:
    """
    Split a secret into shares using Shamir's Secret Sharing.
    
    Args:
        secret: The secret to split (integer, bytes, or string)
        threshold: Minimum number of shares needed to reconstruct (k)
        num_shares: Total number of shares to generate (n)
        prime: Prime for field arithmetic (auto-selected if None)
        include_hash: Include SHA-256 hash for verification
    
    Returns:
        ShareSet containing all shares
    
    Raises:
        ValueError: If parameters are invalid
    
    Example:
        >>> shares = split_secret(b"my secret", k=3, n=5)
        >>> len(shares.shares)
        5
    """
    # Validate parameters
    if threshold < 2:
        raise ValueError("Threshold must be at least 2")
    if num_shares < threshold:
        raise ValueError("Number of shares must be >= threshold")
    if threshold > 255:
        raise ValueError("Threshold cannot exceed 255")
    if num_shares > 255:
        raise ValueError("Number of shares cannot exceed 255")
    
    # Convert secret to integer
    if isinstance(secret, str):
        secret_bytes = secret.encode('utf-8')
    elif isinstance(secret, int):
        if secret < 0:
            raise ValueError("Secret integer must be non-negative")
        secret_bytes = secret.to_bytes((secret.bit_length() + 7) // 8 or 1, 'big')
    else:
        secret_bytes = secret
    
    # Select appropriate prime based on secret size
    secret_int = int.from_bytes(secret_bytes, 'big')
    if prime is None:
        prime = _select_prime(secret_int)
    elif secret_int >= prime:
        raise ValueError("Secret too large for the provided prime. Use a larger prime.")
    
    # Generate random polynomial coefficients
    # f(x) = secret + a1*x + a2*x^2 + ... + a_{k-1}*x^{k-1}
    coefficients = [secret_int]
    for _ in range(threshold - 1):
        coeff = secrets.randbelow(prime - 1) + 1
        coefficients.append(coeff)
    
    # Generate shares by evaluating polynomial at distinct points
    shares = []
    used_x = set()
    
    for _ in range(num_shares):
        # Find unused x-coordinate
        while True:
            x = secrets.randbelow(prime - 1) + 1
            if x not in used_x:
                used_x.add(x)
                break
        
        y = _evaluate_polynomial(coefficients, x, prime)
        shares.append(Share(x=x, y=y, prime=prime, threshold=threshold))
    
    # Calculate hash for verification
    secret_hash = None
    if include_hash:
        secret_hash = hashlib.sha256(secret_bytes).hexdigest()
    
    return ShareSet(shares=shares, secret_hash=secret_hash)


def reconstruct_secret(shares: Union[List[Share], ShareSet]) -> int:
    """
    Reconstruct the secret from shares.
    
    Args:
        shares: List of Share objects or a ShareSet
    
    Returns:
        The reconstructed secret as an integer
    
    Raises:
        ValueError: If shares are invalid or insufficient
    
    Example:
        >>> shares = split_secret(b"my secret", k=3, n=5)
        >>> secret = reconstruct_secret(shares.shares[:3])
    """
    if isinstance(shares, ShareSet):
        shares = shares.shares
    
    if not shares:
        raise ValueError("No shares provided")
    
    # Check threshold
    threshold = shares[0].threshold
    prime = shares[0].prime
    
    if len(shares) < threshold:
        raise ValueError(f"Need at least {threshold} shares, got {len(shares)}")
    
    # Validate shares
    for share in shares:
        if share.threshold != threshold:
            raise ValueError("All shares must have the same threshold")
        if share.prime != prime:
            raise ValueError("All shares must use the same prime")
        if share.x < 0 or share.x >= prime:
            raise ValueError("Share x-coordinate out of range")
    
    # Take only the shares we need
    shares_to_use = shares[:threshold]
    
    # Reconstruct using Lagrange interpolation
    points = [(s.x, s.y) for s in shares_to_use]
    secret = _lagrange_interpolation(points, prime)
    
    return secret


def reconstruct_secret_bytes(
    shares: Union[List[Share], ShareSet],
    expected_length: Optional[int] = None
) -> bytes:
    """
    Reconstruct the secret as bytes.
    
    Args:
        shares: List of Share objects or a ShareSet
        expected_length: Expected byte length of the secret
    
    Returns:
        The reconstructed secret as bytes
    """
    secret_int = reconstruct_secret(shares)
    
    if expected_length:
        byte_length = expected_length
    else:
        byte_length = (secret_int.bit_length() + 7) // 8 or 1
    
    return secret_int.to_bytes(byte_length, 'big')


def reconstruct_secret_string(shares: Union[List[Share], ShareSet]) -> str:
    """
    Reconstruct the secret as a UTF-8 string.
    
    Args:
        shares: List of Share objects or a ShareSet
    
    Returns:
        The reconstructed secret as a string
    """
    return reconstruct_secret_bytes(shares).decode('utf-8')


def verify_secret_hash(shares: ShareSet, secret: Union[bytes, str]) -> bool:
    """
    Verify that the reconstructed secret matches the stored hash.
    
    Args:
        shares: ShareSet with a stored hash
        secret: The reconstructed secret (bytes or string)
    
    Returns:
        True if the hash matches, False otherwise
    """
    if not shares.secret_hash:
        raise ValueError("ShareSet has no stored hash")
    
    if isinstance(secret, str):
        secret_bytes = secret.encode('utf-8')
    else:
        secret_bytes = secret
    
    computed_hash = hashlib.sha256(secret_bytes).hexdigest()
    return computed_hash == shares.secret_hash


class ShamirSecretSharing:
    """
    High-level Shamir's Secret Sharing class for easy use.
    
    Example:
        >>> sss = ShamirSecretSharing(threshold=3, num_shares=5)
        >>> shares = sss.split(b"my secret key")
        >>> secret = sss.reconstruct(shares[:3])
    """
    
    def __init__(
        self,
        threshold: int,
        num_shares: int,
        prime: Optional[int] = None
    ):
        """
        Initialize Shamir's Secret Sharing.
        
        Args:
            threshold: Minimum shares needed to reconstruct
            num_shares: Total number of shares to generate
            prime: Prime for field arithmetic (auto-selected if None)
        """
        if threshold < 2:
            raise ValueError("Threshold must be at least 2")
        if num_shares < threshold:
            raise ValueError("Number of shares must be >= threshold")
        
        self.threshold = threshold
        self.num_shares = num_shares
        self.prime = prime or DEFAULT_PRIME
    
    def split(
        self,
        secret: Union[int, bytes, str],
        include_hash: bool = True
    ) -> ShareSet:
        """Split a secret into shares."""
        return split_secret(
            secret=secret,
            threshold=self.threshold,
            num_shares=self.num_shares,
            prime=self.prime,
            include_hash=include_hash
        )
    
    def reconstruct(self, shares: List[Share]) -> int:
        """Reconstruct the secret from shares."""
        return reconstruct_secret(shares)
    
    def reconstruct_bytes(
        self,
        shares: List[Share],
        expected_length: Optional[int] = None
    ) -> bytes:
        """Reconstruct the secret as bytes."""
        return reconstruct_secret_bytes(shares, expected_length)
    
    def reconstruct_string(self, shares: List[Share]) -> str:
        """Reconstruct the secret as a string."""
        return reconstruct_secret_string(shares)


def split_string(
    secret: str,
    threshold: int,
    num_shares: int,
    prime: Optional[int] = None
) -> ShareSet:
    """
    Convenience function to split a string secret.
    
    Args:
        secret: The string to split
        threshold: Minimum shares needed
        num_shares: Total shares to generate
        prime: Optional prime for field arithmetic
    
    Returns:
        ShareSet with encoded shares
    """
    return split_secret(
        secret=secret.encode('utf-8'),
        threshold=threshold,
        num_shares=num_shares,
        prime=prime
    )


def split_int(
    secret: int,
    threshold: int,
    num_shares: int,
    prime: Optional[int] = None
) -> ShareSet:
    """
    Convenience function to split an integer secret.
    
    Args:
        secret: The integer to split
        threshold: Minimum shares needed
        num_shares: Total shares to generate
        prime: Optional prime for field arithmetic
    
    Returns:
        ShareSet with encoded shares
    """
    return split_secret(
        secret=secret,
        threshold=threshold,
        num_shares=num_shares,
        prime=prime
    )


def split_bytes(
    secret: bytes,
    threshold: int,
    num_shares: int,
    prime: Optional[int] = None
) -> ShareSet:
    """
    Convenience function to split a bytes secret.
    
    Args:
        secret: The bytes to split
        threshold: Minimum shares needed
        num_shares: Total shares to generate
        prime: Optional prime for field arithmetic
    
    Returns:
        ShareSet with encoded shares
    """
    return split_secret(
        secret=secret,
        threshold=threshold,
        num_shares=num_shares,
        prime=prime
    )


# GF(2^8) implementation for byte-level sharing
# This allows sharing individual bytes independently for arbitrary-length data

# Generator for GF(2^8) - using x^8 + x^4 + x^3 + x^2 + 1 (0x11D)
GF256_GENERATOR = 0x11D

# Precompute logarithm and exponentiation tables for GF(2^8)
_GF256_EXP = [0] * 512
_GF256_LOG = [0] * 256

def _init_gf256_tables():
    """Initialize GF(2^8) logarithm and exponentiation tables."""
    x = 1
    for i in range(255):
        _GF256_EXP[i] = x
        _GF256_LOG[x] = i
        x <<= 1
        if x & 0x100:
            x ^= GF256_GENERATOR
    # Extend exponent table for easy multiplication
    for i in range(255, 512):
        _GF256_EXP[i] = _GF256_EXP[i - 255]


# Initialize tables
_init_gf256_tables()


def _gf256_mul(a: int, b: int) -> int:
    """Multiply two elements in GF(2^8)."""
    if a == 0 or b == 0:
        return 0
    return _GF256_EXP[_GF256_LOG[a] + _GF256_LOG[b]]


def _gf256_inv(a: int) -> int:
    """Compute multiplicative inverse in GF(2^8)."""
    if a == 0:
        raise ValueError("Cannot invert zero")
    return _GF256_EXP[255 - _GF256_LOG[a]]


def _gf256_evaluate_polynomial(coeffs: List[int], x: int) -> int:
    """Evaluate polynomial in GF(2^8) at point x."""
    result = 0
    for coeff in reversed(coeffs):
        result = _gf256_mul(result, x) ^ coeff
    return result


def _gf256_lagrange_interpolation(points: List[Tuple[int, int]]) -> int:
    """
    Reconstruct the secret in GF(2^8) using Lagrange interpolation.
    Returns f(0).
    """
    secret = 0
    n = len(points)
    
    for i in range(n):
        xi, yi = points[i]
        basis = 1
        
        for j in range(n):
            if i != j:
                xj = points[j][0]
                # Lagrange basis: (0 - xj) / (xi - xj) = xj / (xi ^ xj) in GF(2^8)
                numerator = xj
                denominator = xi ^ xj
                basis = _gf256_mul(basis, _gf256_mul(numerator, _gf256_inv(denominator)))
        
        secret ^= _gf256_mul(yi, basis)
    
    return secret


def split_bytes_gf256(
    data: bytes,
    threshold: int,
    num_shares: int
) -> List[bytes]:
    """
    Split arbitrary-length bytes into shares using GF(2^8).
    Each byte is processed independently.
    
    Args:
        data: The bytes to split
        threshold: Minimum shares needed to reconstruct
        num_shares: Total shares to generate
    
    Returns:
        List of share bytes (each share is same length as data + 1 byte for x)
    """
    if threshold < 2:
        raise ValueError("Threshold must be at least 2")
    if num_shares < threshold:
        raise ValueError("Number of shares must be >= threshold")
    if threshold > 255 or num_shares > 255:
        raise ValueError("Threshold and num_shares cannot exceed 255 in GF(2^8)")
    
    # Generate x-coordinates (1 to num_shares)
    # Using sequential x-values for simplicity
    x_values = list(range(1, num_shares + 1))
    
    # Initialize shares with x-coordinate
    shares = [bytes([x]) for x in x_values]
    
    # Process each byte independently
    for byte in data:
        # Generate random polynomial coefficients in GF(2^8)
        # f(x) = secret + a1*x + a2*x^2 + ... + a_{k-1}*x^{k-1}
        coeffs = [byte]
        for _ in range(threshold - 1):
            coeffs.append(secrets.randbelow(256))
        
        # Evaluate polynomial at each x-coordinate
        for i, x in enumerate(x_values):
            y = _gf256_evaluate_polynomial(coeffs, x)
            shares[i] += bytes([y])
    
    return shares


def reconstruct_bytes_gf256(shares: List[bytes]) -> bytes:
    """
    Reconstruct bytes from GF(2^8) shares.
    
    Args:
        shares: List of share bytes (first byte is x-coordinate)
    
    Returns:
        Reconstructed data bytes
    """
    if not shares:
        raise ValueError("No shares provided")
    
    # Extract x-coordinates and validate lengths
    x_values = []
    share_data = []
    data_len = len(shares[0]) - 1
    
    for share in shares:
        if len(share) - 1 != data_len:
            raise ValueError("All shares must have the same length")
        x_values.append(share[0])
        share_data.append(share[1:])
    
    # Reconstruct each byte
    result = bytearray()
    for i in range(data_len):
        points = [(x_values[j], share_data[j][i]) for j in range(len(shares))]
        byte = _gf256_lagrange_interpolation(points)
        result.append(byte)
    
    return bytes(result)


# Utility functions for share management

def encode_shares_compact(shares: List[Share]) -> str:
    """
    Encode shares to a compact single-line format.
    
    Args:
        shares: List of Share objects
    
    Returns:
        Compact encoded string
    """
    if not shares:
        return ""
    
    parts = []
    for share in shares:
        parts.append(f"{share.x}.{share.y}.{share.prime}.{share.threshold}")
    
    return "|".join(parts)


def decode_shares_compact(encoded: str) -> List[Share]:
    """
    Decode shares from compact format.
    
    Args:
        encoded: Compact encoded string
    
    Returns:
        List of Share objects
    """
    if not encoded:
        return []
    
    shares = []
    for part in encoded.split("|"):
        x, y, prime, threshold = part.split(".")
        shares.append(Share(
            x=int(x),
            y=int(y),
            prime=int(prime),
            threshold=int(threshold)
        ))
    
    return shares


def get_share_info(share: Share) -> Dict[str, Any]:
    """
    Get information about a share.
    
    Args:
        share: A Share object
    
    Returns:
        Dictionary with share information
    """
    return {
        "x_coordinate": share.x,
        "threshold": share.threshold,
        "prime_bits": share.prime.bit_length(),
        "is_valid": 0 < share.x < share.prime and 0 <= share.y < share.prime
    }


def validate_share_set(shares: List[Share]) -> Tuple[bool, Optional[str]]:
    """
    Validate a set of shares for consistency.
    
    Args:
        shares: List of Share objects
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not shares:
        return False, "No shares provided"
    
    threshold = shares[0].threshold
    prime = shares[0].prime
    
    if len(shares) < threshold:
        return False, f"Insufficient shares: need {threshold}, have {len(shares)}"
    
    x_values = set()
    for i, share in enumerate(shares):
        if share.threshold != threshold:
            return False, f"Share {i} has inconsistent threshold"
        if share.prime != prime:
            return False, f"Share {i} has inconsistent prime"
        if share.x in x_values:
            return False, f"Duplicate x-coordinate: {share.x}"
        x_values.add(share.x)
    
    return True, None


# Demonstrative function for testing
def demo():
    """Run a demonstration of Shamir's Secret Sharing."""
    print("=" * 60)
    print("Shamir's Secret Sharing Demo")
    print("=" * 60)
    
    # Example 1: String secret
    secret = "My top secret password!"
    print(f"\nOriginal secret: {secret}")
    
    # Split into 5 shares, need 3 to reconstruct
    shares = split_string(secret, threshold=3, num_shares=5)
    print(f"\nGenerated {len(shares.shares)} shares (need 3 to reconstruct):")
    
    for i, share in enumerate(shares.shares):
        print(f"  Share {i+1}: {share.encode()[:50]}...")
    
    # Reconstruct with just 3 shares
    reconstructed = reconstruct_secret_string(shares.shares[:3])
    print(f"\nReconstructed with 3 shares: {reconstructed}")
    print(f"Match: {reconstructed == secret}")
    
    # Verify hash
    print(f"\nHash verification: {verify_secret_hash(shares, reconstructed)}")
    
    # Example 2: Binary secret using GF(2^8)
    print("\n" + "=" * 60)
    print("GF(2^8) Binary Secret Demo")
    print("=" * 60)
    
    binary_secret = b"\x01\x02\x03\x04\x05\x06\x07\x08"
    print(f"\nOriginal binary: {binary_secret.hex()}")
    
    gf_shares = split_bytes_gf256(binary_secret, threshold=3, num_shares=5)
    print(f"\nGenerated {len(gf_shares)} GF(2^8) shares:")
    
    for i, share in enumerate(gf_shares):
        print(f"  Share {i+1}: {share.hex()}")
    
    # Reconstruct with 3 shares
    reconstructed_binary = reconstruct_bytes_gf256(gf_shares[:3])
    print(f"\nReconstructed: {reconstructed_binary.hex()}")
    print(f"Match: {reconstructed_binary == binary_secret}")


if __name__ == "__main__":
    demo()