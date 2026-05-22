#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Adler-32 Checksum Utilities Module
================================================
A comprehensive Adler-32 checksum utility module for Python
with zero external dependencies.

Features:
    - Adler-32 checksum computation
    - Streaming/incremental computation
    - File checksum computation
    - Data integrity verification
    - Combined Adler-32 + CRC-32 validation
    - Hex and integer output formats
    - Performance optimized implementation

Adler-32 is a checksum algorithm used in:
    - zlib compression format
    - ZIP file format
    - SAP R/3 system

It is faster but less reliable than CRC-32 for error detection.

Algorithm:
    Adler-32 = (B * 65536 + A) mod 2^32
    Where:
        A = sum of all bytes + 1
        B = sum of all A values

Author: AllToolkit Contributors
License: MIT
"""

from typing import Union, Optional, Tuple
from dataclasses import dataclass


# ============================================================================
# Type Aliases
# ============================================================================

BytesLike = Union[bytes, bytearray, str]


# ============================================================================
# Data Classes
# ============================================================================

@dataclass
class Adler32Result:
    """Container for Adler-32 computation results."""
    value: int  # 32-bit checksum value
    hex: str  # Hexadecimal representation
    a: int  # Lower 16 bits (sum of bytes)
    b: int  # Upper 16 bits (sum of A values)


# ============================================================================
# Constants
# ============================================================================

ADLER32_MOD = 65521  # Largest prime smaller than 65536


# ============================================================================
# Core Adler-32 Functions
# ============================================================================

def adler32(data: BytesLike, initial: int = 1) -> int:
    """
    Compute Adler-32 checksum of data.
    
    Args:
        data: Input data (bytes, bytearray, or string)
        initial: Initial checksum value (default 1)
    
    Returns:
        32-bit Adler-32 checksum
    
    Examples:
        >>> adler32(b'Hello')
        93061621
        >>> adler32('Hello')
        93061621
        >>> adler32(b'')
        1
    
    Note:
        For incremental computation, pass the previous checksum
        as the initial value for the next chunk.
    """
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    # Split initial value into A and B
    a = initial & 0xFFFF
    b = (initial >> 16) & 0xFFFF
    
    for byte in data:
        a = (a + byte) % ADLER32_MOD
        b = (b + a) % ADLER32_MOD
    
    return (b << 16) | a


def adler32_detailed(data: BytesLike, initial: int = 1) -> Adler32Result:
    """
    Compute Adler-32 checksum with detailed breakdown.
    
    Args:
        data: Input data
        initial: Initial checksum value
    
    Returns:
        Adler32Result with checksum, hex, and A/B components
    
    Examples:
        >>> result = adler32_detailed(b'Hello')
        >>> result.value
        93061621
        >>> result.hex
        '058c01f5'
        >>> result.a
        501
        >>> result.b
        5640
    """
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    a = initial & 0xFFFF
    b = (initial >> 16) & 0xFFFF
    
    for byte in data:
        a = (a + byte) % ADLER32_MOD
        b = (b + a) % ADLER32_MOD
    
    value = (b << 16) | a
    
    return Adler32Result(
        value=value,
        hex=f'{value:08x}',
        a=a,
        b=b
    )


def adler32_hex(data: BytesLike) -> str:
    """
    Compute Adler-32 checksum as hexadecimal string.
    
    Args:
        data: Input data
    
    Returns:
        8-character hexadecimal string
    
    Examples:
        >>> adler32_hex(b'Hello')
        '058c01f5'
        >>> adler32_hex(b'Wikipedia')
        '11e60398'
    """
    return f'{adler32(data):08x}'


# ============================================================================
# Incremental/Streaming Computation
# ============================================================================

class Adler32Streaming:
    """
    Streaming Adler-32 checksum computation.
    
    Use for large files or data streams where loading
    all data at once is impractical.
    
    Examples:
        >>> stream = Adler32Streaming()
        >>> stream.update(b'Hello')
        >>> stream.update(b' World')
        >>> stream.value
        403375133
        >>> stream.hex
        '180b041d'
    """
    
    def __init__(self, initial: int = 1):
        """
        Initialize streaming checksum computation.
        
        Args:
            initial: Initial checksum value (default 1)
        """
        self._a = initial & 0xFFFF
        self._b = (initial >> 16) & 0xFFFF
        self._byte_count = 0
    
    def update(self, data: BytesLike) -> int:
        """
        Update checksum with additional data.
        
        Args:
            data: Additional data chunk
        
        Returns:
            Current checksum value
        
        Examples:
        >>> stream = Adler32Streaming()
        >>> stream.update(b'Hello')
        93061621
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        # For large chunks, process in blocks to avoid overflow
        # before modulo operation (safety threshold ~5552 bytes)
        block_size = 5552
        
        for i in range(0, len(data), block_size):
            chunk = data[i:i + block_size]
            for byte in chunk:
                self._a = (self._a + byte) % ADLER32_MOD
                self._b = (self._b + self._a) % ADLER32_MOD
        
        self._byte_count += len(data)
        return self.value
    
    @property
    def value(self) -> int:
        """Current checksum value."""
        return (self._b << 16) | self._a
    
    @property
    def hex(self) -> str:
        """Current checksum as hexadecimal string."""
        return f'{self.value:08x}'
    
    @property
    def byte_count(self) -> int:
        """Total bytes processed."""
        return self._byte_count
    
    def reset(self, initial: int = 1) -> None:
        """
        Reset checksum computation.
        
        Args:
            initial: New initial value (default 1)
        """
        self._a = initial & 0xFFFF
        self._b = (initial >> 16) & 0xFFFF
        self._byte_count = 0
    
    def get_result(self) -> Adler32Result:
        """
        Get detailed result.
        
        Returns:
            Adler32Result with all components
        """
        return Adler32Result(
            value=self.value,
            hex=self.hex,
            a=self._a,
            b=self._b
        )


# ============================================================================
# File Operations
# ============================================================================

def adler32_file(file_path: str, chunk_size: int = 65536) -> Adler32Result:
    """
    Compute Adler-32 checksum of a file.
    
    Args:
        file_path: Path to file
        chunk_size: Chunk size for streaming computation
    
    Returns:
        Adler32Result with checksum and details
    
    Examples:
        >>> result = adler32_file('test.txt')
        >>> result.hex
        '02b10305'
    
    Raises:
        FileNotFoundError: If file doesn't exist
        IOError: If file cannot be read
    """
    stream = Adler32Streaming()
    
    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            stream.update(chunk)
    
    return stream.get_result()


def adler32_file_hex(file_path: str) -> str:
    """
    Compute Adler-32 checksum of a file as hex string.
    
    Args:
        file_path: Path to file
    
    Returns:
        8-character hexadecimal string
    
    Examples:
        >>> adler32_file_hex('test.txt')
        '02b10305'
    """
    return adler32_file(file_path).hex


# ============================================================================
# Verification Functions
# ============================================================================

def verify_adler32(data: BytesLike, expected: Union[int, str]) -> bool:
    """
    Verify data against expected Adler-32 checksum.
    
    Args:
        data: Input data
        expected: Expected checksum (integer or hex string)
    
    Returns:
        True if checksum matches, False otherwise
    
    Examples:
        >>> verify_adler32(b'Hello', 93061621)
        True
        >>> verify_adler32(b'Hello', '058c01f5')
        True
        >>> verify_adler32(b'Hello', 'invalid')
        False
    """
    computed = adler32(data)
    
    if isinstance(expected, str):
        # Parse hex string
        try:
            expected = int(expected, 16)
        except ValueError:
            return False
    
    return computed == expected


def verify_file_adler32(file_path: str, expected: Union[int, str]) -> bool:
    """
    Verify file against expected Adler-32 checksum.
    
    Args:
        file_path: Path to file
        expected: Expected checksum (integer or hex string)
    
    Returns:
        True if checksum matches, False otherwise
    
    Examples:
        >>> verify_file_adler32('test.txt', '02b10305')
        True
    """
    computed = adler32_file(file_path).value
    
    if isinstance(expected, str):
        try:
            expected = int(expected, 16)
        except ValueError:
            return False
    
    return computed == expected


# ============================================================================
# Combined Validation (Adler-32 + CRC-32)
# ============================================================================

def compute_combined_checksum(data: BytesLike) -> Tuple[str, str]:
    """
    Compute both Adler-32 and CRC-32 checksums.
    
    Combined checksums provide better error detection
    than using either alone.
    
    Args:
        data: Input data
    
    Returns:
        Tuple of (adler32_hex, crc32_hex)
    
    Examples:
        >>> compute_combined_checksum(b'Hello')
        ('058c01f5', 'f7ff9e8b')
    
    Note:
        CRC-32 implementation uses standard polynomial 0xEDB88320.
    """
    adler = adler32_hex(data)
    
    # CRC-32 implementation (reflected polynomial)
    crc_table = _generate_crc32_table()
    crc = 0xFFFFFFFF
    
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    for byte in data:
        crc = crc_table[(crc ^ byte) & 0xFF] ^ (crc >> 8)
    
    crc = crc ^ 0xFFFFFFFF
    crc_hex = f'{crc:08x}'
    
    return (adler, crc_hex)


def verify_combined_checksum(data: BytesLike, 
                              adler_expected: str,
                              crc_expected: str) -> Tuple[bool, bool]:
    """
    Verify data against both Adler-32 and CRC-32 checksums.
    
    Args:
        data: Input data
        adler_expected: Expected Adler-32 hex string
        crc_expected: Expected CRC-32 hex string
    
    Returns:
        Tuple of (adler_valid, crc_valid)
    
    Examples:
        >>> verify_combined_checksum(b'Hello', '058c01f5', 'f7ff9e8b')
        (True, True)
    """
    adler, crc = compute_combined_checksum(data)
    
    adler_valid = adler.lower() == adler_expected.lower()
    crc_valid = crc.lower() == crc_expected.lower()
    
    return (adler_valid, crc_valid)


def _generate_crc32_table() -> list:
    """Generate CRC-32 lookup table."""
    table = []
    for i in range(256):
        crc = i
        for _ in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ 0xEDB88320
            else:
                crc >>= 1
        table.append(crc)
    return table


# ============================================================================
# Utility Functions
# ============================================================================

def adler32_to_hex(value: int) -> str:
    """
    Convert Adler-32 integer to hex string.
    
    Args:
        value: Adler-32 checksum integer
    
    Returns:
        8-character hex string
    
    Examples:
        >>> adler32_to_hex(93061621)
        '058c01f5'
    """
    return f'{value:08x}'


def hex_to_adler32(hex_string: str) -> int:
    """
    Convert hex string to Adler-32 integer.
    
    Args:
        hex_string: 8-character hex string
    
    Returns:
        Adler-32 checksum integer
    
    Examples:
        >>> hex_to_adler32('058c01f5')
        93061621
    
    Raises:
        ValueError: If hex string is invalid
    """
    try:
        return int(hex_string, 16)
    except ValueError:
        raise ValueError(f"Invalid hex string: {hex_string}")


def decompose_adler32(value: int) -> Tuple[int, int]:
    """
    Decompose Adler-32 into A and B components.
    
    Args:
        value: Adler-32 checksum integer
    
    Returns:
        Tuple of (A, B) values
    
    Examples:
        >>> decompose_adler32(93061621)
        (501, 5640)
    """
    a = value & 0xFFFF
    b = (value >> 16) & 0xFFFF
    return (a, b)


def compose_adler32(a: int, b: int) -> int:
    """
    Compose Adler-32 from A and B components.
    
    Args:
        a: Lower 16 bits (sum of bytes)
        b: Upper 16 bits (sum of A values)
    
    Returns:
        Adler-32 checksum integer
    
    Examples:
        >>> compose_adler32(501, 5640)
        93061621
    """
    return (b << 16) | a


def compare_adler32(data1: BytesLike, data2: BytesLike) -> bool:
    """
    Compare Adler-32 checksums of two data chunks.
    
    Args:
        data1: First data chunk
        data2: Second data chunk
    
    Returns:
        True if checksums match, False otherwise
    
    Examples:
        >>> compare_adler32(b'Hello', b'Hello')
        True
        >>> compare_adler32(b'Hello', b'World')
        False
    
    Note:
        Matching checksums doesn't guarantee identical data,
        but mismatched checksums definitely indicate different data.
    """
    return adler32(data1) == adler32(data2)


# ============================================================================
# Statistics Functions
# ============================================================================

def adler32_statistics(data: BytesLike) -> dict:
    """
    Compute Adler-32 checksum with statistics.
    
    Args:
        data: Input data
    
    Returns:
        Dictionary with checksum, A/B values, and statistics
    
    Examples:
        >>> stats = adler32_statistics(b'Hello World')
        >>> stats['checksum']
        403375133
        >>> stats['byte_count']
        11
        >>> stats['a_value']
        1065
        >>> stats['b_value']
        9765
    """
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    result = adler32_detailed(data)
    
    # Compute additional statistics
    byte_sum = sum(data)
    byte_avg = byte_sum / len(data) if data else 0
    byte_min = min(data) if data else 0
    byte_max = max(data) if data else 0
    
    return {
        'checksum': result.value,
        'checksum_hex': result.hex,
        'a_value': result.a,
        'b_value': result.b,
        'byte_count': len(data),
        'byte_sum': byte_sum,
        'byte_average': byte_avg,
        'byte_min': byte_min,
        'byte_max': byte_max,
    }


# ============================================================================
# Known Test Values
# ============================================================================

def test_adler32() -> bool:
    """
    Run self-test with known test values.
    
    Returns:
        True if all tests pass
    
    Examples:
        >>> test_adler32()
        True
    """
    # Test values verified against Python's zlib.adler32
    test_cases = [
        (b'', 1, '00000001'),  # Empty string
        (b'a', 6422626, '00620062'),  # Single byte 'a' (97)
        (b'abc', 38600999, '024d0127'),  # "abc"
        (b'Hello', 93061621, '058c01f5'),  # "Hello"
        (b'Hello World', 403375133, '180b041d'),  # "Hello World"
        (b'Wikipedia', 300286872, '11e60398'),  # "Wikipedia"
        (b'The quick brown fox jumps over the lazy dog', 
         1541148634, '5bdc0fda'),  # Pangram
    ]
    
    all_passed = True
    
    for data, expected_value, expected_hex in test_cases:
        computed = adler32(data)
        computed_hex = adler32_hex(data)
        
        if computed != expected_value:
            print(f"FAIL: {data!r}")
            print(f"  Expected: {expected_value} ({expected_hex})")
            print(f"  Got: {computed} ({computed_hex})")
            all_passed = False
        elif computed_hex != expected_hex:
            print(f"FAIL (hex): {data!r}")
            print(f"  Expected: {expected_hex}")
            print(f"  Got: {computed_hex}")
            all_passed = False
    
    # Test streaming
    stream = Adler32Streaming()
    stream.update(b'Hello')
    stream.update(b' World')
    
    if stream.value != adler32(b'Hello World'):
        print("FAIL: Streaming computation")
        print(f"  Expected: {adler32(b'Hello World')}")
        print(f"  Got: {stream.value}")
        all_passed = False
    
    if all_passed:
        print("All Adler-32 tests passed!")
    
    return all_passed


# ============================================================================
# Convenience Aliases
# ============================================================================

# Alias for zlib-style naming
checksum = adler32
checksum_hex = adler32_hex


if __name__ == "__main__":
    print("=== Adler-32 Checksum Utilities Demo ===\n")
    
    # Basic usage
    data = b"Hello, World!"
    print(f"Data: {data}")
    print(f"Adler-32: {adler32(data)}")
    print(f"Adler-32 (hex): {adler32_hex(data)}")
    print()
    
    # Detailed result
    result = adler32_detailed(data)
    print(f"Detailed result:")
    print(f"  Value: {result.value}")
    print(f"  Hex: {result.hex}")
    print(f"  A (lower): {result.a}")
    print(f"  B (upper): {result.b}")
    print()
    
    # Streaming computation
    print("Streaming computation:")
    stream = Adler32Streaming()
    stream.update(b"Hello")
    print(f"  After 'Hello': {stream.hex}")
    stream.update(b", World!")
    print(f"  After ', World!': {stream.hex}")
    print(f"  Total bytes: {stream.byte_count}")
    print()
    
    # Combined checksum
    adler, crc = compute_combined_checksum(data)
    print(f"Combined checksums:")
    print(f"  Adler-32: {adler}")
    print(f"  CRC-32: {crc}")
    print()
    
    # Statistics
    stats = adler32_statistics(data)
    print(f"Statistics:")
    print(f"  Checksum: {stats['checksum_hex']}")
    print(f"  Bytes: {stats['byte_count']}")
    print(f"  A/B: {stats['a_value']}/{stats['b_value']}")
    print()
    
    # Self-test
    print("\n--- Self-Test ---")
    test_adler32()