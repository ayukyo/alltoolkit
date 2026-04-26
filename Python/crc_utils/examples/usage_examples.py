#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - CRC Utilities Usage Examples
==========================================
Demonstrates various use cases of the CRC utilities module.

Examples:
    1. Basic CRC-32 computation
    2. CRC-16 for serial communication
    3. CRC-8 for simple checksums
    4. CRC-64 for large data integrity
    5. File CRC verification
    6. Custom CRC parameters
    7. Multiple algorithm comparison
    8. Data integrity verification
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from crc_utils.mod import (
    CRC,
    crc8,
    crc16,
    crc32,
    crc64,
    file_crc,
    verify_file_crc,
    compute_checksum,
    verify_checksum,
    custom_crc,
    list_algorithms,
    get_algorithm_info,
    compute_multiple,
    reflect_bits,
)


def example_basic_crc32():
    """Example 1: Basic CRC-32 computation."""
    print("\n" + "=" * 60)
    print("Example 1: Basic CRC-32 Computation")
    print("=" * 60)
    
    # Compute CRC-32 of a string
    data = b'Hello, World!'
    
    # Using class
    crc = CRC('crc-32')
    crc.update(data)
    print(f"Data: {data}")
    print(f"CRC-32 (int): {crc.digest}")
    print(f"CRC-32 (hex): {crc.hexdigest()}")
    print(f"CRC-32 (bytes): {crc.bytesdigest().hex()}")
    
    # Using static method
    print(f"\nStatic method CRC-32: 0x{crc32(data):08X}")


def example_crc16_serial():
    """Example 2: CRC-16 for serial communication."""
    print("\n" + "=" * 60)
    print("Example 2: CRC-16 for Serial Communication")
    print("=" * 60)
    
    # CRC-16-CCITT is commonly used in serial protocols
    data = b'\x01\x02\x03\x04\x05'  # Example serial packet
    
    crc = CRC('crc-16-ccitt')
    crc.update(data)
    
    print(f"Serial data: {data.hex()}")
    print(f"CRC-16-CCITT: 0x{crc.digest:04X}")
    print(f"CRC bytes (to append): {crc.bytesdigest().hex()}")
    
    # CRC-16-MODBUS for Modbus protocol
    crc_modbus = CRC('crc-16-modbus')
    crc_modbus.update(data)
    print(f"CRC-16-MODBUS: 0x{crc_modbus.digest:04X}")


def example_crc8_simple():
    """Example 3: CRC-8 for simple checksums."""
    print("\n" + "=" * 60)
    print("Example 3: CRC-8 for Simple Checksums")
    print("=" * 60)
    
    # CRC-8 is useful for small data integrity checks
    messages = [
        b'\x00',        # Zero byte
        b'\xFF',        # Max byte
        b'\x01\x02\x03',  # Multi-byte
        b'Hello',       # ASCII text
    ]
    
    print("CRC-8 checksums:")
    for msg in messages:
        checksum = crc8(msg)
        print(f"  {msg.hex() if not msg.isalnum() else msg.decode()}: 0x{checksum:02X}")
    
    # CRC-8-MAXIM (used in Dallas/Maxim 1-Wire devices)
    crc_maxim = CRC('crc-8-maxim')
    crc_maxim.update(b'123456789')
    print(f"\nCRC-8-MAXIM of '123456789': 0x{crc_maxim.digest:02X}")


def example_crc64_large():
    """Example 4: CRC-64 for large data integrity."""
    print("\n" + "=" * 60)
    print("Example 4: CRC-64 for Large Data Integrity")
    print("=" * 60)
    
    # CRC-64 provides stronger checksum for large files
    large_data = b'A' * 10000 + b'B' * 5000
    
    crc_ecma = CRC('crc-64-ecma')
    crc_ecma.update(large_data)
    
    print(f"Data size: {len(large_data)} bytes")
    print(f"CRC-64-ECMA: 0x{crc_ecma.digest:016X}")
    
    # CRC-64-ISO
    crc_iso = CRC('crc-64-iso')
    crc_iso.update(large_data)
    print(f"CRC-64-ISO:  0x{crc_iso.digest:016X}")


def example_file_crc():
    """Example 5: File CRC verification."""
    print("\n" + "=" * 60)
    print("Example 5: File CRC Verification")
    print("=" * 60)
    
    # Create a test file
    import tempfile
    test_file = tempfile.NamedTemporaryFile(delete=False, suffix='.txt')
    test_file.write(b'This is test content for CRC verification.')
    test_file.close()
    
    # Compute file CRC
    crc_value, hex_str = file_crc(test_file.name, 'crc-32')
    print(f"File: {test_file.name}")
    print(f"CRC-32: 0x{crc_value:08X} ({hex_str})")
    
    # Also compute CRC-16
    crc16_value, crc16_hex = file_crc(test_file.name, 'crc-16-ccitt')
    print(f"CRC-16-CCITT: 0x{crc16_value:04X} ({crc16_hex})")
    
    # Verify CRC
    is_valid = verify_file_crc(test_file.name, hex_str)
    print(f"Verification result: {is_valid}")
    
    # Clean up
    import os
    os.unlink(test_file.name)
    print("Test file deleted.")


def example_custom_crc():
    """Example 6: Custom CRC parameters."""
    print("\n" + "=" * 60)
    print("Example 6: Custom CRC Parameters")
    print("=" * 60)
    
    data = b'test'
    
    # Custom CRC-16 with custom polynomial
    result1 = custom_crc(data, width=16, poly=0x1021, init=0xFFFF)
    print(f"Custom CRC-16 (CCITT init): 0x{result1:04X}")
    
    # Custom CRC-16 with different init
    result2 = custom_crc(data, width=16, poly=0x1021, init=0x0000)
    print(f"Custom CRC-16 (init=0): 0x{result2:04X}")
    
    # Custom CRC-12 (12-bit CRC, useful for some protocols)
    result3 = custom_crc(data, width=12, poly=0x80F, init=0x000)
    print(f"Custom CRC-12: 0x{result3:03X}")
    
    # Custom CRC-5 (5-bit CRC, very compact)
    result4 = custom_crc(data, width=5, poly=0x05, init=0x00)
    print(f"Custom CRC-5: 0x{result4:02X}")


def example_multiple_algorithms():
    """Example 7: Multiple algorithm comparison."""
    print("\n" + "=" * 60)
    print("Example 7: Multiple Algorithm Comparison")
    print("=" * 60)
    
    data = b'123456789'
    
    # Compare all CRC-8 variants
    print("CRC-8 variants:")
    for algo in ['crc-8', 'crc-8-maxim', 'crc-8-rohc']:
        crc = CRC(algo)
        crc.update(data)
        print(f"  {algo}: 0x{crc.digest:02X}")
    
    # Compare all CRC-16 variants
    print("\nCRC-16 variants:")
    for algo in ['crc-16-ibm', 'crc-16-maxim', 'crc-16-usb', 
                 'crc-16-ccitt', 'crc-16-ccitt-false', 'crc-16-modbus']:
        crc = CRC(algo)
        crc.update(data)
        print(f"  {algo}: 0x{crc.digest:04X}")
    
    # Compare all CRC-32 variants
    print("\nCRC-32 variants:")
    for algo in ['crc-32', 'crc-32c', 'crc-32-mpeg', 'crc-32-bzip2']:
        crc = CRC(algo)
        crc.update(data)
        print(f"  {algo}: 0x{crc.digest:08X}")
    
    # Using compute_multiple
    print("\nAll CRCs at once:")
    results = compute_multiple(['crc-8', 'crc-16-ccitt', 'crc-32', 'crc-64-ecma'], data)
    for algo, value in results.items():
        width = get_algorithm_info(algo)['width']
        print(f"  {algo}: 0x{value:0{(width // 4)}X}")


def example_data_integrity():
    """Example 8: Data integrity verification."""
    print("\n" + "=" * 60)
    print("Example 8: Data Integrity Verification")
    print("=" * 60)
    
    # Simulate data transmission with CRC check
    original_data = b'Transmitted data packet'
    
    # Compute checksum
    checksum = compute_checksum(original_data, 'crc-32')
    print(f"Original data: {original_data}")
    print(f"CRC-32 checksum: {checksum}")
    
    # Verify integrity
    is_valid = verify_checksum(original_data, checksum, 'crc-32')
    print(f"Integrity check: {is_valid}")
    
    # Simulate corrupted data
    corrupted_data = b'Transmitted data packet!'  # Added '!'
    is_valid_corrupted = verify_checksum(corrupted_data, checksum, 'crc-32')
    print(f"\nCorrupted data: {corrupted_data}")
    print(f"Integrity check (should fail): {is_valid_corrupted}")
    
    # Using CRC class verify method
    crc = CRC('crc-32')
    print(f"\nClass-based verification:")
    print(f"  Valid data: {crc.verify(original_data, checksum)}")
    print(f"  Corrupted: {crc.verify(corrupted_data, checksum)}")


def example_progressive_crc():
    """Example 9: Progressive CRC computation."""
    print("\n" + "=" * 60)
    print("Example 9: Progressive CRC Computation")
    print("=" * 60)
    
    # Process data in chunks
    chunks = [b'chunk1', b'chunk2', b'chunk3', b'chunk4']
    
    crc = CRC('crc-32')
    for i, chunk in enumerate(chunks):
        crc.update(chunk)
        print(f"Chunk {i+1}: '{chunk.decode()}' -> intermediate CRC: 0x{crc.value:08X}")
    
    print(f"Final CRC: 0x{crc.digest:08X}")
    
    # Compare with single computation
    combined = b''.join(chunks)
    single_crc = CRC.crc32(combined)
    print(f"Single computation: 0x{single_crc:08X}")
    print(f"Match: {crc.digest == single_crc}")


def example_bit_reflection():
    """Example 10: Bit reflection utilities."""
    print("\n" + "=" * 60)
    print("Example 10: Bit Reflection Utilities")
    print("=" * 60)
    
    # Reflect 8 bits
    values_8 = [0x00, 0x31, 0x55, 0xAA, 0xFF]
    print("8-bit reflection:")
    for val in values_8:
        reflected = reflect_bits(val, 8)
        print(f"  0x{val:02X} -> 0x{reflected:02X}")
    
    # Reflect 16 bits
    values_16 = [0x1234, 0xABCD, 0x5555]
    print("\n16-bit reflection:")
    for val in values_16:
        reflected = reflect_bits(val, 16)
        print(f"  0x{val:04X} -> 0x{reflected:04X}")


def example_crc_with_crc():
    """Example 11: CRC verification workflow."""
    print("\n" + "=" * 60)
    print("Example 11: CRC Verification Workflow")
    print("=" * 60)
    
    # Create a packet with CRC
    payload = b'\x01\x02\x03\x04'
    
    # Compute CRC-16 for the payload
    crc = CRC('crc-16-ccitt')
    crc.update(payload)
    crc_bytes = crc.bytesdigest()
    
    # Construct full packet (payload + CRC)
    packet = payload + crc_bytes
    print(f"Payload: {payload.hex()}")
    print(f"CRC: {crc_bytes.hex()}")
    print(f"Full packet: {packet.hex()}")
    
    # Verify received packet
    received_payload = packet[:-2]
    received_crc_bytes = packet[-2:]
    received_crc = int.from_bytes(received_crc_bytes, 'big')
    
    # Verify
    verify_crc = CRC('crc-16-ccitt')
    verify_crc.update(received_payload)
    
    print(f"\nVerification:")
    print(f"  Received payload: {received_payload.hex()}")
    print(f"  Received CRC: 0x{received_crc:04X}")
    print(f"  Computed CRC: 0x{verify_crc.digest:04X}")
    print(f"  Valid: {received_crc == verify_crc.digest}")


def example_algorithm_info():
    """Example 12: Algorithm information."""
    print("\n" + "=" * 60)
    print("Example 12: Algorithm Information")
    print("=" * 60)
    
    # List all available algorithms
    algos = list_algorithms()
    print(f"Available algorithms ({len(algos)} total):")
    for algo in algos[:10]:  # Show first 10
        print(f"  - {algo}")
    print(f"  ... and {len(algos) - 10} more")
    
    # Get detailed info
    print("\nCRC-32 details:")
    info = get_algorithm_info('crc-32')
    for key, value in info.items():
        if isinstance(value, int):
            print(f"  {key}: 0x{value:X}")
        else:
            print(f"  {key}: {value}")


def main():
    """Run all examples."""
    print("=" * 60)
    print("CRC Utilities - Usage Examples")
    print("=" * 60)
    
    examples = [
        example_basic_crc32,
        example_crc16_serial,
        example_crc8_simple,
        example_crc64_large,
        example_file_crc,
        example_custom_crc,
        example_multiple_algorithms,
        example_data_integrity,
        example_progressive_crc,
        example_bit_reflection,
        example_crc_with_crc,
        example_algorithm_info,
    ]
    
    for example in examples:
        try:
            example()
        except Exception as e:
            print(f"\nError in {example.__name__}: {e}")
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == '__main__':
    main()