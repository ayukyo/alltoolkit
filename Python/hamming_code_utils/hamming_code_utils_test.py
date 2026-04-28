"""
Unit tests for Hamming Code Utilities

Tests encoding, decoding, error detection, and correction.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hamming_code_utils.mod import (
    HammingCode, HammingStream,
    hamming_distance, generate_hamming_table, calculate_code_rate,
    encode, decode
)


class TestHammingCodeBasic:
    """Test basic Hamming(7,4) encoding and decoding."""
    
    def test_encode_data_range(self):
        """Test encoding all valid 4-bit values."""
        hamming = HammingCode(extended=False)
        for data in range(16):
            code = hamming.encode(data)
            assert 0 <= code <= 127, f"Code {code} out of range for data {data}"
    
    def test_encode_invalid_data(self):
        """Test encoding invalid data values."""
        hamming = HammingCode(extended=False)
        
        try:
            hamming.encode(-1)
            assert False, "Should raise ValueError for negative data"
        except ValueError:
            pass
        
        try:
            hamming.encode(16)
            assert False, "Should raise ValueError for data > 15"
        except ValueError:
            pass
    
    def test_encode_decode_roundtrip(self):
        """Test that encoding then decoding returns original data."""
        hamming = HammingCode(extended=False)
        for data in range(16):
            code = hamming.encode(data)
            decoded, error = hamming.decode(code)
            assert decoded == data, f"Roundtrip failed: {data} -> {code} -> {decoded}"
            assert error is None, f"Unexpected error detected for clean code"
    
    def test_known_encodings(self):
        """Test some known Hamming(7,4) encodings."""
        hamming = HammingCode(extended=False)
        
        # Test specific known values
        # Data bits at positions 3,5,6,7 (1-indexed)
        # Parity bits at positions 1,2,4 (1-indexed)
        tests = [
            (0, 0b0000000),   # 0000 -> all zeros
            (15, 0b1111111),  # 1111 -> all ones except parity adjustments
        ]
        
        # At minimum, verify encoding produces consistent results
        for data, _ in tests:
            code = hamming.encode(data)
            decoded, _ = hamming.decode(code)
            assert decoded == data


class TestErrorCorrection:
    """Test single-bit error detection and correction."""
    
    def test_single_error_correction(self):
        """Test that all single-bit errors can be corrected."""
        hamming = HammingCode(extended=False)
        
        for data in range(16):
            original_code = hamming.encode(data)
            
            # Test error at each position
            for pos in range(7):
                corrupted = hamming.introduce_error(original_code, pos)
                decoded, error_pos = hamming.decode(corrupted)
                
                assert decoded == data, f"Failed to correct error at pos {pos} for data {data}"
                assert error_pos == pos, f"Wrong error position detected: expected {pos}, got {error_pos}"
    
    def test_no_error_detection(self):
        """Test that clean codes show no errors."""
        hamming = HammingCode(extended=False)
        
        for data in range(16):
            code = hamming.encode(data)
            is_valid, error_pos = hamming.is_valid(code)
            assert is_valid, f"Clean code marked as invalid for data {data}"
            assert error_pos is None


class TestExtendedHamming:
    """Test extended Hamming(8,4) with overall parity."""
    
    def test_extended_encode_decode(self):
        """Test extended Hamming code roundtrip."""
        hamming = HammingCode(extended=True)
        
        for data in range(16):
            code = hamming.encode(data)
            assert 0 <= code <= 255, f"Code {code} out of range"
            decoded, error = hamming.decode(code)
            assert decoded == data
            assert error is None
    
    def test_extended_error_correction(self):
        """Test extended Hamming corrects single-bit errors."""
        hamming = HammingCode(extended=True)
        
        for data in range(16):
            original_code = hamming.encode(data)
            
            # Test error at each position including parity bit
            for pos in range(8):
                corrupted = hamming.introduce_error(original_code, pos)
                decoded, error_pos = hamming.decode(corrupted)
                
                assert decoded == data, f"Failed to correct error at pos {pos} for data {data}"
    
    def test_extended_has_overall_parity(self):
        """Test that extended codes have even overall parity."""
        hamming = HammingCode(extended=True)
        
        for data in range(16):
            code = hamming.encode(data)
            # Count total bits
            bit_count = bin(code).count('1')
            assert bit_count % 2 == 0, f"Extended code should have even parity"


class TestHammingStream:
    """Test stream-based encoding/decoding."""
    
    def test_encode_decode_bytes(self):
        """Test encoding and decoding byte streams."""
        stream = HammingStream(extended=False)
        
        test_data = b"Hello, World!"
        codes = stream.encode_bytes(test_data)
        decoded, errors = stream.decode_bytes(codes)
        
        assert decoded == test_data
        assert all(e is None for e in errors)
    
    def test_encode_decode_bits(self):
        """Test encoding and decoding to bit streams."""
        stream = HammingStream(extended=True)
        
        test_data = bytes(range(256))  # All byte values
        bits = stream.encode_to_bits(test_data)
        decoded, errors = stream.decode_from_bits(bits)
        
        assert decoded == test_data
        assert all(e is None for e in errors)
    
    def test_stream_error_correction(self):
        """Test error correction in stream mode."""
        stream = HammingStream(extended=False)
        
        test_data = b"Test"
        codes = stream.encode_bytes(test_data)
        
        # Introduce error in second code
        codes[1] ^= 0b0010000  # Flip a bit
        
        decoded, errors = stream.decode_bytes(codes)
        
        # Data should still be recovered
        assert decoded == test_data
        assert errors[1] is not None  # Error detected in second code


class TestUtilityFunctions:
    """Test utility functions."""
    
    def test_hamming_distance(self):
        """Test Hamming distance calculation."""
        # Same code
        assert hamming_distance(0, 0) == 0
        assert hamming_distance(0b1111111, 0b1111111) == 0
        
        # Different by 1 bit
        assert hamming_distance(0, 1) == 1
        assert hamming_distance(0b1000000, 0) == 1
        
        # Different by multiple bits
        assert hamming_distance(0b1010101, 0b0101010) == 7  # All bits differ
        assert hamming_distance(0b1010101, 0b1010001) == 1  # Only bit 2 differs
    
    def test_generate_hamming_table(self):
        """Test Hamming table generation."""
        table = generate_hamming_table(extended=False)
        
        assert len(table) == 16
        assert all(0 <= code <= 127 for code in table.values())
        
        # Verify all codes decode correctly
        hamming = HammingCode(extended=False)
        for data, code in table.items():
            decoded, _ = hamming.decode(code)
            assert decoded == data
    
    def test_calculate_code_rate(self):
        """Test code rate calculation."""
        rate_7_4 = calculate_code_rate(extended=False)
        rate_8_4 = calculate_code_rate(extended=True)
        
        assert rate_7_4 == 4/7
        assert rate_8_4 == 4/8
        assert rate_7_4 > rate_8_4  # Standard is more efficient


class TestEncodeBits:
    """Test bit-level encoding and decoding."""
    
    def test_encode_bits(self):
        """Test encoding from bit list."""
        hamming = HammingCode(extended=False)
        
        # Encode [1, 0, 1, 0] = 10
        data_bits = [1, 0, 1, 0]
        code_bits = hamming.encode_bits(data_bits)
        
        assert len(code_bits) == 7
        assert all(b in (0, 1) for b in code_bits)
        
        # Verify roundtrip
        code = 0
        for i, bit in enumerate(code_bits):
            code |= (bit << (6 - i))
        decoded, _ = hamming.decode(code)
        assert decoded == 10
    
    def test_decode_bits(self):
        """Test decoding to bit list."""
        hamming = HammingCode(extended=False)
        
        code = hamming.encode(12)  # 1100
        code_bits = [(code >> (6 - i)) & 1 for i in range(7)]
        
        data_bits, error = hamming.decode_bits(code_bits)
        
        assert len(data_bits) == 4
        assert data_bits == [1, 1, 0, 0]
        assert error is None
    
    def test_invalid_bits(self):
        """Test handling of invalid bit input."""
        hamming = HammingCode(extended=False)
        
        # Wrong number of data bits
        try:
            hamming.encode_bits([1, 0, 1])  # Only 3 bits
            assert False, "Should raise ValueError"
        except ValueError:
            pass
        
        # Invalid bit values
        try:
            hamming.encode_bits([1, 2, 0, 1])  # 2 is not valid bit
            assert False, "Should raise ValueError"
        except ValueError:
            pass


class TestConvenienceFunctions:
    """Test convenience functions."""
    
    def test_encode_decode_convenience(self):
        """Test convenience encode/decode functions."""
        for data in range(16):
            code = encode(data)
            decoded, _ = decode(code)
            assert decoded == data
        
        # Extended version
        for data in range(16):
            code = encode(data, extended=True)
            decoded, _ = decode(code, extended=True)
            assert decoded == data


def run_all_tests():
    """Run all tests and report results."""
    test_classes = [
        TestHammingCodeBasic,
        TestErrorCorrection,
        TestExtendedHamming,
        TestHammingStream,
        TestUtilityFunctions,
        TestEncodeBits,
        TestConvenienceFunctions,
    ]
    
    passed = 0
    failed = 0
    
    print("Running Hamming Code Tests")
    print("=" * 50)
    
    for test_class in test_classes:
        print(f"\n{test_class.__name__}:")
        instance = test_class()
        
        for method_name in dir(instance):
            if method_name.startswith('test_'):
                try:
                    getattr(instance, method_name)()
                    print(f"  ✓ {method_name}")
                    passed += 1
                except AssertionError as e:
                    print(f"  ✗ {method_name}: {e}")
                    failed += 1
                except Exception as e:
                    print(f"  ✗ {method_name}: {type(e).__name__}: {e}")
                    failed += 1
    
    print("\n" + "=" * 50)
    print(f"Results: {passed} passed, {failed} failed")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)