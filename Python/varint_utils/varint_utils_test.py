"""
Unit tests for varint_utils module.

Tests all encoding/decoding functions, edge cases, and streaming support.
"""

import unittest
from mod import (
    # Exceptions
    VarintError, VarintOverflowError, VarintDecodeError,
    # Unsigned
    encode_unsigned, decode_unsigned, encode_unsigned_batch, decode_unsigned_batch,
    # ZigZag
    zigzag_encode, zigzag_decode,
    # Signed
    encode_signed, decode_signed, encode_signed_batch, decode_signed_batch,
    # Streaming
    VarintWriter, VarintReader,
    # Size utilities
    size_unsigned, size_signed, estimate_size_unsigned, estimate_size_signed, compare_efficiency,
    # Protocol Buffers style
    encode_int32, decode_int32, encode_int64, decode_int64,
    encode_uint32, decode_uint32, encode_uint64, decode_uint64,
    # General purpose
    encode_varint, decode_varint,
    # Constants
    MAX_UINT64, MAX_INT64, MIN_INT64,
)


class TestUnsignedVarint(unittest.TestCase):
    """Test unsigned varint encoding and decoding."""
    
    def test_encode_zero(self):
        """Test encoding zero."""
        self.assertEqual(encode_unsigned(0), b'\x00')
    
    def test_encode_small_values(self):
        """Test encoding values that fit in one byte."""
        self.assertEqual(encode_unsigned(1), b'\x01')
        self.assertEqual(encode_unsigned(127), b'\x7f')
        self.assertEqual(encode_unsigned(42), b'\x2a')
    
    def test_encode_two_byte_values(self):
        """Test encoding values that need two bytes."""
        self.assertEqual(encode_unsigned(128), b'\x80\x01')
        self.assertEqual(encode_unsigned(300), b'\xac\x02')
        self.assertEqual(encode_unsigned(16383), b'\xff\x7f')
    
    def test_encode_three_byte_values(self):
        """Test encoding values that need three bytes."""
        self.assertEqual(encode_unsigned(16384), b'\x80\x80\x01')
        self.assertEqual(encode_unsigned(2097151), b'\xff\xff\x7f')
    
    def test_encode_large_values(self):
        """Test encoding large values."""
        # 32-bit max
        max_uint32 = (1 << 32) - 1
        result = encode_unsigned(max_uint32)
        self.assertEqual(len(result), 5)
        
        # 64-bit max
        result = encode_unsigned(MAX_UINT64)
        self.assertEqual(len(result), 10)
    
    def test_decode_zero(self):
        """Test decoding zero."""
        value, consumed = decode_unsigned(b'\x00')
        self.assertEqual(value, 0)
        self.assertEqual(consumed, 1)
    
    def test_decode_small_values(self):
        """Test decoding values that fit in one byte."""
        value, consumed = decode_unsigned(b'\x01')
        self.assertEqual(value, 1)
        self.assertEqual(consumed, 1)
        
        value, consumed = decode_unsigned(b'\x7f')
        self.assertEqual(value, 127)
        self.assertEqual(consumed, 1)
    
    def test_decode_two_byte_values(self):
        """Test decoding values that need two bytes."""
        value, consumed = decode_unsigned(b'\x80\x01')
        self.assertEqual(value, 128)
        self.assertEqual(consumed, 2)
        
        value, consumed = decode_unsigned(b'\xac\x02')
        self.assertEqual(value, 300)
        self.assertEqual(consumed, 2)
    
    def test_roundtrip(self):
        """Test encode/decode roundtrip for various values."""
        test_values = [
            0, 1, 127, 128, 255, 256, 16383, 16384,
            65535, 65536, 2097151, 2097152,
            (1 << 31) - 1, (1 << 31), MAX_UINT64
        ]
        
        for value in test_values:
            with self.subTest(value=value):
                encoded = encode_unsigned(value)
                decoded, consumed = decode_unsigned(encoded)
                self.assertEqual(decoded, value)
                self.assertEqual(consumed, len(encoded))
    
    def test_encode_negative_raises(self):
        """Test that encoding negative values raises error."""
        with self.assertRaises(VarintError):
            encode_unsigned(-1)
    
    def test_encode_overflow_raises(self):
        """Test that encoding values > max raises error."""
        with self.assertRaises(VarintError):
            encode_unsigned(MAX_UINT64 + 1)
    
    def test_decode_empty_raises(self):
        """Test that decoding empty data raises error."""
        with self.assertRaises(VarintDecodeError):
            decode_unsigned(b'')
    
    def test_decode_incomplete_raises(self):
        """Test that decoding incomplete data raises error."""
        with self.assertRaises(VarintDecodeError):
            decode_unsigned(b'\x80')  # Missing continuation byte
    
    def test_decode_with_offset(self):
        """Test decoding with offset."""
        data = b'\xff\xac\x02\xff'
        value, consumed = decode_unsigned(data, offset=1)
        self.assertEqual(value, 300)
        self.assertEqual(consumed, 2)


class TestUnsignedBatch(unittest.TestCase):
    """Test batch encoding and decoding of unsigned varints."""
    
    def test_encode_decode_batch(self):
        """Test batch encode/decode roundtrip."""
        values = [0, 1, 127, 128, 300, 16384, (1 << 20)]
        encoded = encode_unsigned_batch(values)
        decoded = decode_unsigned_batch(encoded)
        self.assertEqual(decoded, values)
    
    def test_decode_batch_with_count(self):
        """Test decoding specific number of values."""
        encoded = encode_unsigned_batch([1, 2, 3, 4, 5])
        decoded = decode_unsigned_batch(encoded, count=3)
        self.assertEqual(decoded, [1, 2, 3])
    
    def test_decode_batch_count_mismatch_raises(self):
        """Test that mismatched count raises error."""
        encoded = encode_unsigned_batch([1, 2, 3])
        with self.assertRaises(VarintDecodeError):
            decode_unsigned_batch(encoded, count=5)


class TestZigZag(unittest.TestCase):
    """Test ZigZag encoding and decoding."""
    
    def test_zero(self):
        """Test ZigZag encoding of zero."""
        self.assertEqual(zigzag_encode(0), 0)
        self.assertEqual(zigzag_decode(0), 0)
    
    def test_positive_values(self):
        """Test ZigZag encoding of positive values."""
        self.assertEqual(zigzag_encode(1), 2)
        self.assertEqual(zigzag_encode(2), 4)
        self.assertEqual(zigzag_encode(3), 6)
        self.assertEqual(zigzag_encode(42), 84)
    
    def test_negative_values(self):
        """Test ZigZag encoding of negative values."""
        self.assertEqual(zigzag_encode(-1), 1)
        self.assertEqual(zigzag_encode(-2), 3)
        self.assertEqual(zigzag_encode(-3), 5)
        self.assertEqual(zigzag_encode(-42), 83)
    
    def test_roundtrip(self):
        """Test ZigZag encode/decode roundtrip."""
        test_values = [0, 1, -1, 2, -2, 42, -42, 1000, -1000,
                      MAX_INT64, MIN_INT64]
        
        for value in test_values:
            with self.subTest(value=value):
                encoded = zigzag_encode(value)
                decoded = zigzag_decode(encoded)
                self.assertEqual(decoded, value)
    
    def test_small_values_produce_small_outputs(self):
        """Test that small absolute values produce small encoded values."""
        # This is the key property of ZigZag encoding
        small_positive = zigzag_encode(10)
        small_negative = zigzag_encode(-10)
        
        # Both should be relatively small
        self.assertLess(small_positive, 100)
        self.assertLess(small_negative, 100)


class TestSignedVarint(unittest.TestCase):
    """Test signed varint encoding and decoding."""
    
    def test_encode_zero(self):
        """Test encoding zero."""
        self.assertEqual(encode_signed(0), b'\x00')
    
    def test_encode_positive(self):
        """Test encoding positive values."""
        self.assertEqual(encode_signed(1), b'\x02')  # zigzag(1) = 2
        self.assertEqual(encode_signed(63), b'\x7e')  # zigzag(63) = 126
    
    def test_encode_negative(self):
        """Test encoding negative values."""
        self.assertEqual(encode_signed(-1), b'\x01')  # zigzag(-1) = 1
        self.assertEqual(encode_signed(-2), b'\x03')  # zigzag(-2) = 3
        self.assertEqual(encode_signed(-64), b'\x7f')  # zigzag(-64) = 127
    
    def test_decode_zero(self):
        """Test decoding zero."""
        value, consumed = decode_signed(b'\x00')
        self.assertEqual(value, 0)
        self.assertEqual(consumed, 1)
    
    def test_decode_positive(self):
        """Test decoding positive values."""
        value, consumed = decode_signed(b'\x02')
        self.assertEqual(value, 1)
        
        value, consumed = decode_signed(b'\x7e')
        self.assertEqual(value, 63)
    
    def test_decode_negative(self):
        """Test decoding negative values."""
        value, consumed = decode_signed(b'\x01')
        self.assertEqual(value, -1)
        
        value, consumed = decode_signed(b'\x03')
        self.assertEqual(value, -2)
    
    def test_roundtrip(self):
        """Test encode/decode roundtrip for signed values."""
        test_values = [
            0, 1, -1, 2, -2, 63, -64, 64, -65,
            1000, -1000, 1000000, -1000000,
            MAX_INT64, MIN_INT64
        ]
        
        for value in test_values:
            with self.subTest(value=value):
                encoded = encode_signed(value)
                decoded, consumed = decode_signed(encoded)
                self.assertEqual(decoded, value)
                self.assertEqual(consumed, len(encoded))
    
    def test_encode_out_of_range_raises(self):
        """Test that encoding out-of-range values raises error."""
        with self.assertRaises(VarintError):
            encode_signed(MAX_INT64 + 1)
        with self.assertRaises(VarintError):
            encode_signed(MIN_INT64 - 1)


class TestSignedBatch(unittest.TestCase):
    """Test batch encoding and decoding of signed varints."""
    
    def test_encode_decode_batch(self):
        """Test batch encode/decode roundtrip."""
        values = [0, 1, -1, 100, -100, 10000, -10000]
        encoded = encode_signed_batch(values)
        decoded = decode_signed_batch(encoded)
        self.assertEqual(decoded, values)
    
    def test_decode_batch_with_count(self):
        """Test decoding specific number of signed values."""
        encoded = encode_signed_batch([1, -1, 2, -2, 3])
        decoded = decode_signed_batch(encoded, count=3)
        self.assertEqual(decoded, [1, -1, 2])


class TestVarintWriter(unittest.TestCase):
    """Test VarintWriter streaming class."""
    
    def test_write_unsigned(self):
        """Test writing unsigned values."""
        writer = VarintWriter()
        writer.write_unsigned(1).write_unsigned(300)
        data = writer.get_bytes()
        
        self.assertEqual(data, b'\x01\xac\x02')
    
    def test_write_signed(self):
        """Test writing signed values."""
        writer = VarintWriter()
        writer.write_signed(0).write_signed(-1).write_signed(1)
        data = writer.get_bytes()
        
        self.assertEqual(data, b'\x00\x01\x02')
    
    def test_write_batch(self):
        """Test writing batches of values."""
        writer = VarintWriter()
        writer.write_unsigned_batch([1, 2, 3])
        writer.write_signed_batch([-1, -2, -3])
        data = writer.get_bytes()
        
        self.assertEqual(data, b'\x01\x02\x03\x01\x03\x05')
    
    def test_len(self):
        """Test length method."""
        writer = VarintWriter()
        self.assertEqual(len(writer), 0)
        writer.write_unsigned(300)
        self.assertEqual(len(writer), 2)
    
    def test_clear(self):
        """Test clear method."""
        writer = VarintWriter()
        writer.write_unsigned(1).write_unsigned(2)
        self.assertEqual(len(writer), 2)
        writer.clear()
        self.assertEqual(len(writer), 0)


class TestVarintReader(unittest.TestCase):
    """Test VarintReader streaming class."""
    
    def test_read_unsigned(self):
        """Test reading unsigned values."""
        data = encode_unsigned_batch([1, 300, 128])
        reader = VarintReader(data)
        
        self.assertEqual(reader.read_unsigned(), 1)
        self.assertEqual(reader.read_unsigned(), 300)
        self.assertEqual(reader.read_unsigned(), 128)
    
    def test_read_signed(self):
        """Test reading signed values."""
        data = encode_signed_batch([0, -1, 1, -2])
        reader = VarintReader(data)
        
        self.assertEqual(reader.read_signed(), 0)
        self.assertEqual(reader.read_signed(), -1)
        self.assertEqual(reader.read_signed(), 1)
        self.assertEqual(reader.read_signed(), -2)
    
    def test_has_more(self):
        """Test has_more method."""
        data = encode_unsigned(1)
        reader = VarintReader(data)
        
        self.assertTrue(reader.has_more())
        reader.read_unsigned()
        self.assertFalse(reader.has_more())
    
    def test_read_unsigned_all(self):
        """Test iterating over all unsigned values."""
        data = encode_unsigned_batch([1, 2, 3, 4, 5])
        reader = VarintReader(data)
        
        values = list(reader.read_unsigned_all())
        self.assertEqual(values, [1, 2, 3, 4, 5])
    
    def test_read_signed_all(self):
        """Test iterating over all signed values."""
        data = encode_signed_batch([0, -1, 1, -2, 2])
        reader = VarintReader(data)
        
        values = list(reader.read_signed_all())
        self.assertEqual(values, [0, -1, 1, -2, 2])
    
    def test_bytes_read_remaining(self):
        """Test bytes tracking."""
        data = encode_unsigned_batch([1, 300])
        reader = VarintReader(data)
        
        self.assertEqual(reader.bytes_read(), 0)
        self.assertEqual(reader.bytes_remaining(), 3)
        
        reader.read_unsigned()  # 1 byte
        self.assertEqual(reader.bytes_read(), 1)
        self.assertEqual(reader.bytes_remaining(), 2)
        
        reader.read_unsigned()  # 2 bytes
        self.assertEqual(reader.bytes_read(), 3)
        self.assertEqual(reader.bytes_remaining(), 0)
    
    def test_reset(self):
        """Test reset method."""
        data = encode_unsigned_batch([1, 2])
        reader = VarintReader(data)
        
        reader.read_unsigned()
        reader.read_unsigned()
        self.assertFalse(reader.has_more())
        
        reader.reset()
        self.assertTrue(reader.has_more())
        self.assertEqual(reader.read_unsigned(), 1)
    
    def test_read_empty_raises(self):
        """Test that reading empty raises error."""
        reader = VarintReader(b'')
        
        with self.assertRaises(VarintDecodeError):
            reader.read_unsigned()


class TestSizeUtilities(unittest.TestCase):
    """Test size calculation utilities."""
    
    def test_size_unsigned(self):
        """Test unsigned size calculation."""
        self.assertEqual(size_unsigned(0), 1)
        self.assertEqual(size_unsigned(1), 1)
        self.assertEqual(size_unsigned(127), 1)
        self.assertEqual(size_unsigned(128), 2)
        self.assertEqual(size_unsigned(16383), 2)
        self.assertEqual(size_unsigned(16384), 3)
        self.assertEqual(size_unsigned(2097151), 3)
        self.assertEqual(size_unsigned(2097152), 4)
    
    def test_size_unsigned_matches_encoding(self):
        """Test that size calculation matches actual encoding size."""
        test_values = [0, 1, 127, 128, 16383, 16384, 2097151, 2097152,
                      (1 << 31), MAX_UINT64]
        
        for value in test_values:
            with self.subTest(value=value):
                self.assertEqual(size_unsigned(value), len(encode_unsigned(value)))
    
    def test_size_signed(self):
        """Test signed size calculation."""
        self.assertEqual(size_signed(0), 1)
        self.assertEqual(size_signed(1), 1)
        self.assertEqual(size_signed(-1), 1)
        self.assertEqual(size_signed(63), 1)
        self.assertEqual(size_signed(-64), 1)
        self.assertEqual(size_signed(64), 2)
        self.assertEqual(size_signed(-65), 2)
    
    def test_size_signed_matches_encoding(self):
        """Test that signed size calculation matches actual encoding size."""
        test_values = [0, 1, -1, 63, -64, 64, -65, 1000, -1000,
                      MAX_INT64, MIN_INT64]
        
        for value in test_values:
            with self.subTest(value=value):
                self.assertEqual(size_signed(value), len(encode_signed(value)))
    
    def test_size_unsigned_negative_raises(self):
        """Test that negative values raise error for unsigned size."""
        with self.assertRaises(VarintError):
            size_unsigned(-1)
    
    def test_estimate_size_unsigned(self):
        """Test estimating total size for multiple unsigned values."""
        values = [0, 127, 128, 16384]
        total = estimate_size_unsigned(values)
        self.assertEqual(total, 1 + 1 + 2 + 3)
    
    def test_estimate_size_signed(self):
        """Test estimating total size for multiple signed values."""
        values = [0, 1, -1, 64, -65]
        total = estimate_size_signed(values)
        self.assertEqual(total, 1 + 1 + 1 + 2 + 2)
    
    def test_compare_efficiency(self):
        """Test efficiency comparison."""
        # Small values - varint should be much smaller
        small_values = [1, 2, 3, 4, 5]
        result = compare_efficiency(small_values)
        
        self.assertEqual(result['value_count'], 5)
        self.assertEqual(result['varint_size'], 5)  # 1 byte each
        self.assertEqual(result['fixed_size'], 40)  # 5 * 8 bytes
        self.assertEqual(result['bytes_saved'], 35)
        self.assertAlmostEqual(result['compression_ratio'], 5/40)
        self.assertEqual(result['avg_varint_size'], 1)
        
        # Large values - varint will be larger
        large_values = [MAX_INT64, MAX_INT64, MAX_INT64]
        result = compare_efficiency(large_values)
        
        # Each large value takes 10 bytes in varint vs 8 in fixed
        self.assertEqual(result['varint_size'], 30)  # 3 * 10 bytes
        self.assertEqual(result['fixed_size'], 24)  # 3 * 8 bytes
        self.assertEqual(result['bytes_saved'], -6)  # varint is bigger


class TestProtocolBuffersStyle(unittest.TestCase):
    """Test Protocol Buffers style encoding functions."""
    
    def test_int32_roundtrip(self):
        """Test int32 encode/decode roundtrip."""
        test_values = [
            0, 1, -1, 2147483647, -2147483648,  # Max and min int32
            100, -100, 1000, -1000
        ]
        
        for value in test_values:
            with self.subTest(value=value):
                encoded = encode_int32(value)
                decoded, consumed = decode_int32(encoded)
                self.assertEqual(decoded, value)
                self.assertEqual(consumed, len(encoded))
    
    def test_int32_out_of_range_raises(self):
        """Test that int32 encoding out of range raises error."""
        with self.assertRaises(VarintError):
            encode_int32(2147483648)  # Max int32 + 1
        with self.assertRaises(VarintError):
            encode_int32(-2147483649)  # Min int32 - 1
    
    def test_int64_roundtrip(self):
        """Test int64 encode/decode roundtrip."""
        test_values = [
            0, 1, -1, 
            2147483647, -2147483648,
            MAX_INT64, MIN_INT64
        ]
        
        for value in test_values:
            with self.subTest(value=value):
                encoded = encode_int64(value)
                decoded, consumed = decode_int64(encoded)
                self.assertEqual(decoded, value)
    
    def test_uint32_roundtrip(self):
        """Test uint32 encode/decode roundtrip."""
        test_values = [0, 1, 127, 128, 255, 256, 65535, 4294967295]
        
        for value in test_values:
            with self.subTest(value=value):
                encoded = encode_uint32(value)
                decoded, consumed = decode_uint32(encoded)
                self.assertEqual(decoded, value)
    
    def test_uint32_out_of_range_raises(self):
        """Test that uint32 encoding out of range raises error."""
        with self.assertRaises(VarintError):
            encode_uint32(4294967296)  # Max uint32 + 1
    
    def test_uint64_roundtrip(self):
        """Test uint64 encode/decode roundtrip."""
        test_values = [0, 1, (1 << 32), (1 << 63), MAX_UINT64]
        
        for value in test_values:
            with self.subTest(value=value):
                encoded = encode_uint64(value)
                decoded, consumed = decode_uint64(encoded)
                self.assertEqual(decoded, value)


class TestGeneralPurpose(unittest.TestCase):
    """Test general-purpose encode_varint/decode_varint functions."""
    
    def test_unsigned_mode(self):
        """Test general-purpose unsigned encoding."""
        encoded = encode_varint(300)
        self.assertEqual(encoded, b'\xac\x02')
        
        decoded, consumed = decode_varint(encoded)
        self.assertEqual(decoded, 300)
    
    def test_signed_mode(self):
        """Test general-purpose signed encoding."""
        encoded = encode_varint(-1, signed=True)
        self.assertEqual(encoded, b'\x01')
        
        decoded, consumed = decode_varint(encoded, signed=True)
        self.assertEqual(decoded, -1)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""
    
    def test_max_uint64_roundtrip(self):
        """Test encoding/decoding maximum uint64 value."""
        encoded = encode_unsigned(MAX_UINT64)
        decoded, consumed = decode_unsigned(encoded)
        self.assertEqual(decoded, MAX_UINT64)
        self.assertEqual(consumed, 10)
    
    def test_max_int64_roundtrip(self):
        """Test encoding/decoding maximum int64 value."""
        encoded = encode_signed(MAX_INT64)
        decoded, consumed = decode_signed(encoded)
        self.assertEqual(decoded, MAX_INT64)
    
    def test_min_int64_roundtrip(self):
        """Test encoding/decoding minimum int64 value."""
        encoded = encode_signed(MIN_INT64)
        decoded, consumed = decode_signed(encoded)
        self.assertEqual(decoded, MIN_INT64)
    
    def test_empty_batch(self):
        """Test encoding/decoding empty batches."""
        self.assertEqual(encode_unsigned_batch([]), b'')
        self.assertEqual(decode_unsigned_batch(b''), [])
        
        self.assertEqual(encode_signed_batch([]), b'')
        self.assertEqual(decode_signed_batch(b''), [])
    
    def test_writer_reader_integration(self):
        """Test VarintWriter and VarintReader integration."""
        writer = VarintWriter()
        
        # Write various values
        writer.write_unsigned(0)
        writer.write_unsigned(1)
        writer.write_unsigned(127)
        writer.write_unsigned(128)
        writer.write_unsigned(300)
        writer.write_signed(-1)
        writer.write_signed(1)
        writer.write_signed(-42)
        
        data = writer.get_bytes()
        reader = VarintReader(data)
        
        # Read values back
        self.assertEqual(reader.read_unsigned(), 0)
        self.assertEqual(reader.read_unsigned(), 1)
        self.assertEqual(reader.read_unsigned(), 127)
        self.assertEqual(reader.read_unsigned(), 128)
        self.assertEqual(reader.read_unsigned(), 300)
        self.assertEqual(reader.read_signed(), -1)
        self.assertEqual(reader.read_signed(), 1)
        self.assertEqual(reader.read_signed(), -42)
        
        self.assertFalse(reader.has_more())


if __name__ == '__main__':
    unittest.main(verbosity=2)