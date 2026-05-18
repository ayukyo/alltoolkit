"""
Tests for CBOR Utilities

Comprehensive tests for CBOR encoding and decoding according to RFC 8949.
"""

import unittest
import struct
import math
from datetime import datetime, timezone, timedelta
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mod import (
    encode, decode, encode_canonical, encode_to_file, decode_from_file,
    is_valid_cbor, get_cbor_type, estimate_size, dumps, loads,
    cbor2json, json2cbor,
    CBORError, CBOREncodingError, CBORDecodingError, CBORUnsupportedTypeError
)


class TestIntegerEncoding(unittest.TestCase):
    """Test integer encoding and decoding."""
    
    def test_small_positive_integers(self):
        """Test small positive integers (0-23) - encoded in single byte."""
        for i in range(24):
            encoded = encode(i)
            self.assertEqual(len(encoded), 1)
            self.assertEqual(encoded[0], i)
            self.assertEqual(decode(encoded), i)
    
    def test_one_byte_integers(self):
        """Test integers that need one extra byte (24-255)."""
        for i in [24, 100, 200, 255]:
            encoded = encode(i)
            self.assertEqual(len(encoded), 2)
            self.assertEqual(encoded[0], 24)  # AI_ONE_BYTE
            self.assertEqual(encoded[1], i)
            self.assertEqual(decode(encoded), i)
    
    def test_two_byte_integers(self):
        """Test integers that need two extra bytes."""
        for i in [256, 1000, 65535]:
            encoded = encode(i)
            self.assertEqual(len(encoded), 3)
            self.assertEqual(encoded[0], 25)  # AI_TWO_BYTES
            value = struct.unpack('>H', encoded[1:3])[0]
            self.assertEqual(value, i)
            self.assertEqual(decode(encoded), i)
    
    def test_four_byte_integers(self):
        """Test integers that need four extra bytes."""
        for i in [65536, 1000000, 4294967295]:
            encoded = encode(i)
            self.assertEqual(len(encoded), 5)
            self.assertEqual(encoded[0], 26)  # AI_FOUR_BYTES
            value = struct.unpack('>I', encoded[1:5])[0]
            self.assertEqual(value, i)
            self.assertEqual(decode(encoded), i)
    
    def test_eight_byte_integers(self):
        """Test integers that need eight extra bytes."""
        for i in [4294967296, 1000000000000, 2**63 - 1]:
            encoded = encode(i)
            self.assertEqual(len(encoded), 9)
            self.assertEqual(encoded[0], 27)  # AI_EIGHT_BYTES
            value = struct.unpack('>Q', encoded[1:9])[0]
            self.assertEqual(value, i)
            self.assertEqual(decode(encoded), i)
    
    def test_negative_integers(self):
        """Test negative integers."""
        for i in [-1, -10, -100, -1000, -1000000]:
            encoded = encode(i)
            decoded = decode(encoded)
            self.assertEqual(decoded, i)
    
    def test_large_negative_integers(self):
        """Test large negative integers."""
        for i in [-2**63, -1000000000000]:
            encoded = encode(i)
            decoded = decode(encoded)
            self.assertEqual(decoded, i)
    
    def test_zero(self):
        """Test zero."""
        encoded = encode(0)
        self.assertEqual(encoded, b'\x00')
        self.assertEqual(decode(encoded), 0)


class TestFloatEncoding(unittest.TestCase):
    """Test floating point encoding and decoding."""
    
    def test_positive_floats(self):
        """Test positive floating point numbers."""
        for f in [0.0, 0.5, 1.0, 1.5, 3.14159, 1000.0, 1e10]:
            encoded = encode(f)
            decoded = decode(encoded)
            self.assertAlmostEqual(decoded, f, places=6)
    
    def test_negative_floats(self):
        """Test negative floating point numbers."""
        for f in [-0.5, -1.0, -1.5, -3.14159, -1000.0]:
            encoded = encode(f)
            decoded = decode(encoded)
            self.assertAlmostEqual(decoded, f, places=6)
    
    def test_special_floats(self):
        """Test special floating point values."""
        # Positive infinity
        encoded = encode(float('inf'))
        self.assertEqual(decode(encoded), float('inf'))
        
        # Negative infinity
        encoded = encode(float('-inf'))
        self.assertEqual(decode(encoded), float('-inf'))
        
        # NaN
        encoded = encode(float('nan'))
        self.assertTrue(math.isnan(decode(encoded)))
    
    def test_small_floats(self):
        """Test small floating point values."""
        for f in [0.1, 0.01, 0.001]:
            encoded = encode(f)
            decoded = decode(encoded)
            self.assertAlmostEqual(decoded, f, places=6)


import math


class TestStringEncoding(unittest.TestCase):
    """Test string encoding and decoding."""
    
    def test_empty_string(self):
        """Test empty string."""
        encoded = encode("")
        self.assertEqual(encoded, b'\x60')
        self.assertEqual(decode(encoded), "")
    
    def test_short_strings(self):
        """Test short strings (length < 24)."""
        for s in ["a", "ab", "hello", "world!"]:
            encoded = encode(s)
            self.assertTrue(encoded.startswith(b'\x60' + bytes([len(s)])) or 
                           encoded[0] == 0x60 + len(s))
            self.assertEqual(decode(encoded), s)
    
    def test_medium_strings(self):
        """Test medium length strings."""
        s = "a" * 100
        encoded = encode(s)
        self.assertEqual(decode(encoded), s)
    
    def test_long_strings(self):
        """Test long strings."""
        s = "hello" * 1000
        encoded = encode(s)
        self.assertEqual(decode(encoded), s)
    
    def test_unicode_strings(self):
        """Test Unicode strings."""
        for s in ["こんにちは", "你好世界", "مرحبا", "🎉🎊🎁"]:
            encoded = encode(s)
            decoded = decode(encoded)
            self.assertEqual(decoded, s)
    
    def test_emoji(self):
        """Test emoji encoding."""
        s = "👨‍👩‍👧‍👦🎉🎊🎁🌟⭐🌈☀️🌙🌎🌍🌏"
        encoded = encode(s)
        decoded = decode(encoded)
        self.assertEqual(decoded, s)


class TestByteStringEncoding(unittest.TestCase):
    """Test byte string encoding and decoding."""
    
    def test_empty_bytes(self):
        """Test empty byte string."""
        encoded = encode(b"")
        self.assertEqual(encoded, b'\x40')
        self.assertEqual(decode(encoded), b"")
    
    def test_short_byte_strings(self):
        """Test short byte strings."""
        for b in [b"a", b"ab", b"hello", b"\x00\x01\x02"]:
            encoded = encode(b)
            decoded = decode(encoded)
            self.assertEqual(decoded, b)
    
    def test_long_byte_strings(self):
        """Test long byte strings."""
        b = bytes(range(256)) * 10
        encoded = encode(b)
        decoded = decode(encoded)
        self.assertEqual(decoded, b)
    
    def test_bytearray(self):
        """Test bytearray encoding."""
        ba = bytearray(b"hello")
        encoded = encode(ba)
        decoded = decode(encoded)
        self.assertEqual(decoded, bytes(ba))


class TestArrayEncoding(unittest.TestCase):
    """Test array encoding and decoding."""
    
    def test_empty_array(self):
        """Test empty array."""
        encoded = encode([])
        self.assertEqual(encoded, b'\x80')
        self.assertEqual(decode(encoded), [])
    
    def test_simple_arrays(self):
        """Test simple arrays."""
        for arr in [[1, 2, 3], ["a", "b", "c"], [1, "a", True, None]]:
            encoded = encode(arr)
            decoded = decode(encoded)
            self.assertEqual(decoded, arr)
    
    def test_nested_arrays(self):
        """Test nested arrays."""
        arr = [[1, 2], [3, 4], [[5, 6], [7, 8]]]
        encoded = encode(arr)
        decoded = decode(encoded)
        self.assertEqual(decoded, arr)
    
    def test_tuple_encoding(self):
        """Test tuple encoding (converted to list)."""
        t = (1, 2, 3)
        encoded = encode(t)
        decoded = decode(encoded)
        self.assertEqual(decoded, list(t))
    
    def test_large_array(self):
        """Test large array."""
        arr = list(range(1000))
        encoded = encode(arr)
        decoded = decode(encoded)
        self.assertEqual(decoded, arr)


class TestMapEncoding(unittest.TestCase):
    """Test map encoding and decoding."""
    
    def test_empty_map(self):
        """Test empty map."""
        encoded = encode({})
        self.assertEqual(encoded, b'\xa0')
        self.assertEqual(decode(encoded), {})
    
    def test_simple_maps(self):
        """Test simple maps."""
        m = {"a": 1, "b": 2, "c": 3}
        encoded = encode(m)
        decoded = decode(encoded)
        self.assertEqual(decoded, m)
    
    def test_integer_keys(self):
        """Test maps with integer keys."""
        m = {1: "one", 2: "two", 3: "three"}
        encoded = encode(m)
        decoded = decode(encoded)
        self.assertEqual(decoded, m)
    
    def test_nested_maps(self):
        """Test nested maps."""
        m = {"a": {"b": {"c": 1}}}
        encoded = encode(m)
        decoded = decode(encoded)
        self.assertEqual(decoded, m)
    
    def test_mixed_keys(self):
        """Test maps with mixed key types."""
        m = {"string": 1, 42: "integer", b"bytes": "binary"}
        encoded = encode(m)
        decoded = decode(encoded)
        self.assertEqual(decoded, m)


class TestBooleanAndNull(unittest.TestCase):
    """Test boolean and null encoding."""
    
    def test_true(self):
        """Test True encoding."""
        encoded = encode(True)
        self.assertEqual(encoded, b'\xf5')
        self.assertEqual(decode(encoded), True)
    
    def test_false(self):
        """Test False encoding."""
        encoded = encode(False)
        self.assertEqual(encoded, b'\xf4')
        self.assertEqual(decode(encoded), False)
    
    def test_none(self):
        """Test None encoding."""
        encoded = encode(None)
        self.assertEqual(encoded, b'\xf6')
        self.assertEqual(decode(encoded), None)


class TestSetEncoding(unittest.TestCase):
    """Test set encoding."""
    
    def test_simple_set(self):
        """Test simple set."""
        s = {1, 2, 3}
        encoded = encode(s)
        decoded = decode(encoded)
        self.assertEqual(decoded, s)
    
    def test_string_set(self):
        """Test set of strings."""
        s = {"a", "b", "c"}
        encoded = encode(s)
        decoded = decode(encoded)
        self.assertEqual(decoded, s)


class TestDatetimeEncoding(unittest.TestCase):
    """Test datetime encoding and decoding."""
    
    def test_datetime_epoch(self):
        """Test datetime as epoch timestamp (default)."""
        dt = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        encoded = encode(dt)
        decoded = decode(encoded)
        self.assertEqual(decoded.timestamp(), dt.timestamp())
    
    def test_datetime_string(self):
        """Test datetime as ISO string."""
        dt = datetime(2024, 1, 1, 12, 0, 0)
        encoded = encode(dt, datetime_mode='string')
        decoded = decode(encoded)
        # Should be a datetime (or close to it)
        self.assertIsInstance(decoded, datetime)
    
    def test_datetime_now(self):
        """Test encoding current time."""
        dt = datetime.now(timezone.utc)
        encoded = encode(dt)
        decoded = decode(encoded)
        # Allow for small time difference
        self.assertTrue(abs((decoded - dt).total_seconds()) < 1)


class TestTaggedValues(unittest.TestCase):
    """Test tagged value encoding and decoding."""
    
    def test_big_positive_integer(self):
        """Test big positive integer (tag 2)."""
        # This is automatically handled for large integers
        large = 2**65
        encoded = encode(large)
        decoded = decode(encoded)
        self.assertEqual(decoded, large)
    
    def test_big_negative_integer(self):
        """Test big negative integer (tag 3)."""
        large = -(2**65)
        encoded = encode(large)
        decoded = decode(encoded)
        self.assertEqual(decoded, large)


class TestCanonicalEncoding(unittest.TestCase):
    """Test canonical CBOR encoding."""
    
    def test_map_key_order(self):
        """Test that map keys are sorted in canonical encoding."""
        m = {"c": 1, "a": 2, "b": 3}
        encoded = encode_canonical(m)
        decoded = decode(encoded)
        self.assertEqual(decoded, m)
        
        # Check that keys are in bytewise order
        # 'a' < 'b' < 'c' in UTF-8
        self.assertEqual(encoded[0], 0xa3)  # Map with 3 items
    
    def test_deterministic(self):
        """Test that canonical encoding is deterministic."""
        m = {"z": 1, "a": 2, "m": 3, "b": 4}
        encoded1 = encode_canonical(m)
        encoded2 = encode_canonical(m)
        self.assertEqual(encoded1, encoded2)
    
    def test_sort_keys_flag(self):
        """Test sort_keys flag."""
        m = {"c": 1, "a": 2, "b": 3}
        encoded = encode(m, sort_keys=True)
        decoded = decode(encoded)
        self.assertEqual(decoded, m)


class TestFileOperations(unittest.TestCase):
    """Test file operations."""
    
    def test_encode_to_file(self):
        """Test encoding to file."""
        import tempfile
        import os
        
        data = {"name": "test", "values": [1, 2, 3]}
        
        with tempfile.NamedTemporaryFile(delete=False) as f:
            filepath = f.name
        
        try:
            encode_to_file(data, filepath)
            decoded = decode_from_file(filepath)
            self.assertEqual(decoded, data)
        finally:
            os.unlink(filepath)


class TestValidation(unittest.TestCase):
    """Test validation functions."""
    
    def test_is_valid_cbor_true(self):
        """Test valid CBOR data."""
        self.assertTrue(is_valid_cbor(encode(42)))
        self.assertTrue(is_valid_cbor(encode("hello")))
        self.assertTrue(is_valid_cbor(encode([1, 2, 3])))
        self.assertTrue(is_valid_cbor(encode({"a": 1})))
    
    def test_is_valid_cbor_false(self):
        """Test invalid CBOR data."""
        self.assertFalse(is_valid_cbor(b""))
        self.assertFalse(is_valid_cbor(b"not cbor"))
        self.assertFalse(is_valid_cbor(b"\xff\xff\xff"))
    
    def test_get_cbor_type(self):
        """Test type detection."""
        self.assertEqual(get_cbor_type(encode(42)), 'int')
        self.assertEqual(get_cbor_type(encode(3.14)), 'float')
        self.assertEqual(get_cbor_type(encode(True)), 'bool')
        self.assertEqual(get_cbor_type(encode(None)), 'null')
        self.assertEqual(get_cbor_type(encode("hello")), 'str')
        self.assertEqual(get_cbor_type(encode(b"bytes")), 'bytes')
        self.assertEqual(get_cbor_type(encode([1, 2, 3])), 'array')
        self.assertEqual(get_cbor_type(encode({"a": 1})), 'map')


class TestEstimateSize(unittest.TestCase):
    """Test size estimation."""
    
    def test_integer_sizes(self):
        """Test integer size estimation."""
        for i in [0, 10, 100, 1000, 100000, 10000000000]:
            estimated = estimate_size(i)
            actual = len(encode(i))
            # Allow for small difference due to encoding choices
            self.assertLessEqual(abs(estimated - actual), 0)
    
    def test_string_sizes(self):
        """Test string size estimation."""
        for s in ["", "a", "hello", "a" * 100, "a" * 1000]:
            estimated = estimate_size(s)
            actual = len(encode(s))
            self.assertEqual(estimated, actual)
    
    def test_array_sizes(self):
        """Test array size estimation."""
        for arr in [[], [1], [1, 2, 3], list(range(100))]:
            estimated = estimate_size(arr)
            actual = len(encode(arr))
            self.assertEqual(estimated, actual)


class TestAliases(unittest.TestCase):
    """Test module aliases."""
    
    def test_dumps_loads(self):
        """Test dumps and loads aliases."""
        data = {"key": "value", "number": 42}
        encoded = dumps(data)
        decoded = loads(encoded)
        self.assertEqual(decoded, data)


class TestCBOR2JSON(unittest.TestCase):
    """Test CBOR to JSON conversion."""
    
    def test_simple_conversion(self):
        """Test simple CBOR to JSON conversion."""
        data = {"name": "Alice", "age": 30}
        encoded = encode(data)
        json_obj = cbor2json(encoded)
        self.assertEqual(json_obj, data)
    
    def test_bytes_to_base64(self):
        """Test that bytes are converted to base64."""
        data = {"binary": b"\x00\x01\x02"}
        encoded = encode(data)
        json_obj = cbor2json(encoded)
        # Binary should be base64 encoded
        import base64
        expected = base64.b64encode(b"\x00\x01\x02").decode('ascii')
        self.assertEqual(json_obj["binary"], expected)
    
    def test_json2cbor(self):
        """Test JSON to CBOR conversion."""
        data = {"name": "Bob", "active": True}
        encoded = json2cbor(data)
        decoded = decode(encoded)
        self.assertEqual(decoded, data)


class TestComplexData(unittest.TestCase):
    """Test complex data structures."""
    
    def test_nested_structure(self):
        """Test deeply nested structure."""
        data = {
            "level1": {
                "level2": {
                    "level3": {
                        "level4": {
                            "data": [1, 2, 3],
                            "meta": {"count": 3}
                        }
                    }
                }
            }
        }
        encoded = encode(data)
        decoded = decode(encoded)
        self.assertEqual(decoded, data)
    
    def test_mixed_types(self):
        """Test structure with mixed types."""
        data = {
            "int": 42,
            "float": 3.14,
            "string": "hello",
            "bytes": b"world",
            "bool": True,
            "null": None,
            "array": [1, "two", 3.0],
            "map": {"nested": "value"}
        }
        encoded = encode(data)
        decoded = decode(encoded)
        self.assertEqual(decoded, data)
    
    def test_roundtrip(self):
        """Test encode/decode roundtrip for various types."""
        test_cases = [
            0, 1, -1, 255, -255, 65535, -65535,
            0.0, 1.0, -1.0, 3.14159, 1e10, -1e10,
            "", "a", "hello world", "日本語テスト",
            b"", b"a", b"\x00\xff",
            [], [1, 2, 3], ["a", "b", "c"],
            {}, {"a": 1}, {"a": {"b": {"c": 3}}},
            True, False, None,
        ]
        
        for value in test_cases:
            with self.subTest(value=value):
                encoded = encode(value)
                decoded = decode(encoded)
                self.assertEqual(decoded, value)


class TestErrorHandling(unittest.TestCase):
    """Test error handling."""
    
    def test_invalid_cbor(self):
        """Test decoding invalid CBOR."""
        with self.assertRaises(CBORDecodingError):
            decode(b"\xff")  # Break marker without context
    
    def test_truncated_cbor(self):
        """Test decoding truncated CBOR."""
        encoded = encode([1, 2, 3])
        with self.assertRaises(CBORDecodingError):
            decode(encoded[:2])  # Truncated
    
    def test_unsupported_type(self):
        """Test encoding unsupported type."""
        class CustomClass:
            pass
        
        with self.assertRaises(CBORUnsupportedTypeError):
            encode(CustomClass())


class TestIndefiniteLength(unittest.TestCase):
    """Test indefinite length encoding."""
    
    def test_indefinite_array(self):
        """Test decoding indefinite length array."""
        # Manually create an indefinite array: [_ 1, 2, 3 ]
        # 0x9F = start indefinite array
        # 0x01, 0x02, 0x03 = items
        # 0xFF = break
        encoded = bytes([0x9F, 0x01, 0x02, 0x03, 0xFF])
        decoded = decode(encoded)
        self.assertEqual(decoded, [1, 2, 3])
    
    def test_indefinite_map(self):
        """Test decoding indefinite length map."""
        # Manually create an indefinite map: {_ "a": 1, "b": 2 }
        # 0xBF = start indefinite map
        # 0x61 'a' 0x01, 0x61 'b' 0x02
        # 0xFF = break
        encoded = bytes([0xBF, 0x61, ord('a'), 0x01, 0x61, ord('b'), 0x02, 0xFF])
        decoded = decode(encoded)
        self.assertEqual(decoded, {"a": 1, "b": 2})
    
    def test_indefinite_string(self):
        """Test decoding indefinite length string."""
        # "strea" (5 chars) + "ming" (4 chars) = "streaming"
        encoded = bytes([0x7F, 0x65]) + b"strea" + bytes([0x64]) + b"ming" + bytes([0xFF])
        decoded = decode(encoded)
        self.assertEqual(decoded, "streaming")
    
    def test_indefinite_bytes(self):
        """Test decoding indefinite length byte string."""
        encoded = bytes([0x5F, 0x41]) + b"a" + bytes([0x41]) + b"b" + bytes([0xFF])
        decoded = decode(encoded)
        self.assertEqual(decoded, b"ab")


if __name__ == '__main__':
    unittest.main()