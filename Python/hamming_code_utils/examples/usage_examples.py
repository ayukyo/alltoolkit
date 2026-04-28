"""
Hamming Code Utilities - Usage Examples

Demonstrates practical applications of Hamming codes for error detection and correction.
"""

import sys
import os

# Handle imports whether run directly or as a module
_current_dir = os.path.dirname(os.path.abspath(__file__))
_parent_dir = os.path.dirname(_current_dir)
_mod_dir = os.path.dirname(_parent_dir)

if _parent_dir not in sys.path:
    sys.path.insert(0, _parent_dir)

# Now import from mod.py which is in the same directory as this file's parent
import mod as hamming_mod

HammingCode = hamming_mod.HammingCode
HammingStream = hamming_mod.HammingStream
hamming_distance = hamming_mod.hamming_distance
generate_hamming_table = hamming_mod.generate_hamming_table
calculate_code_rate = hamming_mod.calculate_code_rate
encode = hamming_mod.encode
decode = hamming_mod.decode


def example_1_basic_encoding():
    """Example 1: Basic Hamming(7,4) encoding."""
    print("=" * 60)
    print("Example 1: Basic Hamming(7,4) Encoding")
    print("=" * 60)
    
    hamming = HammingCode(extended=False)
    
    # Encode a 4-bit value (0-15)
    data = 10  # Binary: 1010
    code = hamming.encode(data)
    
    print(f"Original data: {data} (binary: {data:04b})")
    print(f"Encoded code:  {code:07b} (decimal: {code})")
    print()
    
    # Decode it back
    decoded, error_pos = hamming.decode(code)
    print(f"Decoded data:  {decoded} (binary: {decoded:04b})")
    print(f"Error detected: {error_pos if error_pos is not None else 'None'}")
    print()


def example_2_error_correction():
    """Example 2: Single-bit error correction."""
    print("=" * 60)
    print("Example 2: Single-Bit Error Correction")
    print("=" * 60)
    
    hamming = HammingCode(extended=False)
    
    # Original data and code
    data = 12  # Binary: 1100
    original_code = hamming.encode(data)
    
    print(f"Original data: {data} ({data:04b})")
    print(f"Original code: {original_code:07b}")
    print()
    
    # Simulate transmission error - flip bit at position 3
    error_position = 3
    corrupted_code = hamming.introduce_error(original_code, error_position)
    
    print(f"Simulated error at position {error_position}")
    print(f"Corrupted code: {corrupted_code:07b}")
    print(f"Bit difference:  {original_code:07b} -> {corrupted_code:07b}")
    print()
    
    # Detect and correct the error
    decoded_data, detected_error_pos = hamming.decode(corrupted_code)
    
    print(f"Error detected at position: {detected_error_pos}")
    print(f"Corrected data: {decoded_data} ({decoded_data:04b})")
    print(f"Correction successful: {decoded_data == data}")
    print()


def example_3_all_errors():
    """Example 3: Verify all single-bit errors are correctable."""
    print("=" * 60)
    print("Example 3: Verify All Single-Bit Errors Are Correctable")
    print("=" * 60)
    
    hamming = HammingCode(extended=False)
    
    data = 5  # Binary: 0101
    original_code = hamming.encode(data)
    
    print(f"Testing data value: {data} ({data:04b})")
    print(f"Original code: {original_code:07b}")
    print()
    print("Testing error correction at each bit position:")
    
    all_corrected = True
    for pos in range(7):
        corrupted = hamming.introduce_error(original_code, pos)
        decoded, detected_pos = hamming.decode(corrupted)
        success = (decoded == data and detected_pos == pos)
        status = "✓" if success else "✗"
        print(f"  Position {pos}: {status} (detected: {detected_pos}, corrected: {decoded == data})")
        all_corrected = all_corrected and success
    
    print()
    print(f"All errors correctable: {all_corrected}")
    print()


def example_4_extended_hamming():
    """Example 4: Extended Hamming(8,4) with overall parity."""
    print("=" * 60)
    print("Example 4: Extended Hamming(8,4) with Overall Parity")
    print("=" * 60)
    
    standard = HammingCode(extended=False)
    extended = HammingCode(extended=True)
    
    data = 7  # Binary: 0111
    
    std_code = standard.encode(data)
    ext_code = extended.encode(data)
    
    print(f"Data: {data} ({data:04b})")
    print()
    print(f"Standard Hamming(7,4): {std_code:07b}")
    print(f"Extended Hamming(8,4): {ext_code:08b}")
    print()
    
    # Check parity
    std_parity = bin(std_code).count('1')
    ext_parity = bin(ext_code).count('1')
    
    print(f"Bit count in standard: {std_parity} (may be odd or even)")
    print(f"Bit count in extended: {ext_parity} (always even)")
    print()
    
    print("Extended code includes overall parity bit for double-error detection")
    print()


def example_5_encode_table():
    """Example 5: Generate complete encoding table."""
    print("=" * 60)
    print("Example 5: Complete Hamming(7,4) Encoding Table")
    print("=" * 60)
    
    table = generate_hamming_table(extended=False)
    
    print("Data | Code (binary) | Code (decimal)")
    print("-" * 40)
    for data, code in table.items():
        print(f" {data:2d}  |    {code:07b}    |     {code:3d}")
    print()


def example_6_stream_encoding():
    """Example 6: Stream-based encoding for text."""
    print("=" * 60)
    print("Example 6: Stream-Based Encoding for Text")
    print("=" * 60)
    
    stream = HammingStream(extended=False)
    
    # Encode a text message
    message = "Hi"
    message_bytes = message.encode('utf-8')
    
    print(f"Original message: '{message}'")
    print(f"Bytes: {list(message_bytes)}")
    print()
    
    # Encode to Hamming codes
    codes = stream.encode_bytes(message_bytes)
    print(f"Hamming codes: {codes}")
    print(f"Code count: {len(codes)} (2 codes per byte)")
    print()
    
    # Decode back
    decoded_bytes, errors = stream.decode_bytes(codes)
    decoded_message = decoded_bytes.decode('utf-8')
    
    print(f"Decoded message: '{decoded_message}'")
    print(f"Errors detected: {[e for e in errors if e is not None]}")
    print()


def example_7_transmission_simulation():
    """Example 7: Simulate noisy transmission channel."""
    print("=" * 60)
    print("Example 7: Simulate Noisy Transmission Channel")
    print("=" * 60)
    
    stream = HammingStream(extended=True)  # Use extended for better detection
    
    # Original message
    message = "OK"
    message_bytes = message.encode('utf-8')
    
    print(f"Original message: '{message}'")
    print(f"Original bytes: {list(message_bytes)}")
    print()
    
    # Encode
    codes = stream.encode_bytes(message_bytes)
    print(f"Encoded codes: {codes}")
    print()
    
    # Simulate noise (flip one bit in first code)
    print("Simulating transmission noise...")
    corrupted_codes = codes.copy()
    corrupted_codes[0] ^= 0b0001000  # Flip bit at position 3
    print(f"Corrupted codes: {corrupted_codes}")
    print()
    
    # Decode with error correction
    decoded_bytes, errors = stream.decode_bytes(corrupted_codes)
    decoded_message = decoded_bytes.decode('utf-8')
    
    print(f"Decoded message: '{decoded_message}'")
    print(f"Error positions: {errors}")
    print(f"Message recovered: {decoded_message == message}")
    print()


def example_8_bit_manipulation():
    """Example 8: Bit-level operations."""
    print("=" * 60)
    print("Example 8: Bit-Level Operations")
    print("=" * 60)
    
    hamming = HammingCode(extended=False)
    
    # Work with individual bits
    data_bits = [1, 0, 1, 1]  # Binary 1011 = decimal 11
    print(f"Data bits: {data_bits}")
    
    # Encode to code bits
    code_bits = hamming.encode_bits(data_bits)
    print(f"Code bits: {code_bits}")
    print(f"Code bits format: P1 P2 D1 P4 D2 D3 D4")
    print()
    
    # Introduce error
    print("Introducing error at position 4...")
    code_bits[4] ^= 1
    print(f"Corrupted bits: {code_bits}")
    
    # Decode
    decoded_bits, error_pos = hamming.decode_bits(code_bits)
    print(f"Decoded bits: {decoded_bits}")
    print(f"Error detected at position: {error_pos}")
    print(f"Correction successful: {decoded_bits == data_bits}")
    print()


def example_9_hamming_distance():
    """Example 9: Hamming distance between codes."""
    print("=" * 60)
    print("Example 9: Hamming Distance Between Codes")
    print("=" * 60)
    
    table = generate_hamming_table(extended=False)
    codes = list(table.values())
    
    print("Minimum Hamming distance between any two valid codes:")
    
    min_distance = float('inf')
    for i, code1 in enumerate(codes):
        for j, code2 in enumerate(codes):
            if i < j:
                dist = hamming_distance(code1, code2)
                min_distance = min(min_distance, dist)
    
    print(f"Minimum distance: {min_distance}")
    print()
    print("Hamming(7,4) has minimum distance 3, which allows:")
    print("  - Detection of up to 2-bit errors")
    print("  - Correction of single-bit errors")
    print()


def example_10_efficiency():
    """Example 10: Code efficiency and overhead."""
    print("=" * 60)
    print("Example 10: Code Efficiency and Overhead")
    print("=" * 60)
    
    std_rate = calculate_code_rate(extended=False)
    ext_rate = calculate_code_rate(extended=True)
    
    print("Code Rate = Data Bits / Total Bits")
    print()
    print(f"Hamming(7,4): {std_rate:.4f} ({std_rate*100:.2f}%)")
    print(f"  - 4 data bits encoded in 7 bits")
    print(f"  - Overhead: {7-4} bits ({((7-4)/7)*100:.1f}%)")
    print()
    print(f"Hamming(8,4): {ext_rate:.4f} ({ext_rate*100:.2f}%)")
    print(f"  - 4 data bits encoded in 8 bits")
    print(f"  - Overhead: {8-4} bits ({((8-4)/8)*100:.1f}%)")
    print()
    print("Trade-off: Extended code can detect double errors")
    print()


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("HAMMING CODE UTILITIES - USAGE EXAMPLES")
    print("=" * 60 + "\n")
    
    example_1_basic_encoding()
    example_2_error_correction()
    example_3_all_errors()
    example_4_extended_hamming()
    example_5_encode_table()
    example_6_stream_encoding()
    example_7_transmission_simulation()
    example_8_bit_manipulation()
    example_9_hamming_distance()
    example_10_efficiency()
    
    print("=" * 60)
    print("All examples completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()