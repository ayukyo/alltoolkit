"""
msgpack_utils Test Suite

Comprehensive tests for MessagePack serialization utilities.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from datetime import datetime, timezone
import io

from msgpack_utils.mod import (
    packb, unpackb,
    pack_stream, unpack_stream,
    StreamUnpacker,
    estimate_size,
    compare_with_json,
    is_valid_msgpack,
    Encoder, Decoder,
    MessagePackError, EncodingError, DecodingError, InsufficientData
)


class TestBasicEncoding(unittest.TestCase):
    """Test basic type encoding and decoding."""
    
    def test_nil(self):
        self.assertIsNone(unpackb(packb(None)))
    
    def test_true(self):
        self.assertTrue(unpackb(packb(True)))
    
    def test_false(self):
        self.assertFalse(unpackb(packb(False)))
    
    def test_positive_fixint(self):
        for i in [0, 1, 42, 127]:
            self.assertEqual(unpackb(packb(i)), i)
    
    def test_negative_fixint(self):
        for i in [-1, -16, -32]:
            self.assertEqual(unpackb(packb(i)), i)
    
    def test_uint8(self):
        for i in [128, 255]:
            self.assertEqual(unpackb(packb(i)), i)
    
    def test_uint16(self):
        for i in [256, 1000, 65535]:
            self.assertEqual(unpackb(packb(i)), i)
    
    def test_uint32(self):
        for i in [65536, 1000000, 4294967295]:
            self.assertEqual(unpackb(packb(i)), i)
    
    def test_uint64(self):
        for i in [4294967296, 18446744073709551615]:
            self.assertEqual(unpackb(packb(i)), i)
    
    def test_int8(self):
        for i in [-33, -128]:
            self.assertEqual(unpackb(packb(i)), i)
    
    def test_int16(self):
        for i in [-129, -1000, -32768]:
            self.assertEqual(unpackb(packb(i)), i)
    
    def test_int32(self):
        for i in [-32769, -100000, -2147483648]:
            self.assertEqual(unpackb(packb(i)), i)
    
    def test_int64(self):
        for i in [-2147483649, -9223372036854775808]:
            self.assertEqual(unpackb(packb(i)), i)
    
    def test_float(self):
        for f in [0.0, 3.14159, -2.71828, 1e-10, 1e20]:
            result = unpackb(packb(f))
            self.assertAlmostEqual(result, f, places=10)


class TestStringEncoding(unittest.TestCase):
    """Test string encoding and decoding."""
    
    def test_empty_string(self):
        s = ""
        self.assertEqual(unpackb(packb(s)), s)
    
    def test_fixstr(self):
        for s in ["a", "hello", "x" * 31]:
            self.assertEqual(unpackb(packb(s)), s)
    
    def test_str8(self):
        for s in ["x" * 32, "x" * 255]:
            self.assertEqual(unpackb(packb(s)), s)
    
    def test_str16(self):
        for s in ["x" * 256, "x" * 1000]:
            self.assertEqual(unpackb(packb(s)), s)
    
    def test_unicode(self):
        for s in ["你好", "🎉", "日本語テスト", "مرحبا"]:
            self.assertEqual(unpackb(packb(s)), s)


class TestBinaryEncoding(unittest.TestCase):
    """Test binary encoding and decoding."""
    
    def test_empty_bytes(self):
        b = b""
        self.assertEqual(unpackb(packb(b)), b)
    
    def test_bin8(self):
        b = b"\x00\x01\x02" * 10
        self.assertEqual(unpackb(packb(b)), b)
    
    def test_bin16(self):
        b = b"\xff" * 1000
        self.assertEqual(unpackb(packb(b)), b)
    
    def test_binary_data(self):
        b = bytes(range(256))
        self.assertEqual(unpackb(packb(b)), b)


class TestArrayEncoding(unittest.TestCase):
    """Test array encoding and decoding."""
    
    def test_empty_array(self):
        a = []
        self.assertEqual(unpackb(packb(a)), a)
    
    def test_fixarray(self):
        a = list(range(15))
        self.assertEqual(unpackb(packb(a)), a)
    
    def test_array16(self):
        a = list(range(100))
        self.assertEqual(unpackb(packb(a)), a)
    
    def test_mixed_types(self):
        a = [None, True, False, 42, -100, 3.14, "hello", b"bytes"]
        self.assertEqual(unpackb(packb(a)), a)
    
    def test_nested_arrays(self):
        a = [[1, 2], [3, 4], [[5, 6], [7, 8]]]
        self.assertEqual(unpackb(packb(a)), a)


class TestMapEncoding(unittest.TestCase):
    """Test map encoding and decoding."""
    
    def test_empty_map(self):
        m = {}
        self.assertEqual(unpackb(packb(m)), m)
    
    def test_fixmap(self):
        m = {f"key{i}": i for i in range(15)}
        self.assertEqual(unpackb(packb(m)), m)
    
    def test_map16(self):
        m = {f"key{i}": i for i in range(100)}
        self.assertEqual(unpackb(packb(m)), m)
    
    def test_nested_map(self):
        m = {
            "user": {
                "name": "Alice",
                "age": 30,
                "address": {
                    "city": "Tokyo",
                    "country": "Japan"
                }
            }
        }
        self.assertEqual(unpackb(packb(m)), m)
    
    def test_integer_keys(self):
        m = {1: "one", 2: "two", 100: "hundred"}
        self.assertEqual(unpackb(packb(m)), m)


class TestDatetimeEncoding(unittest.TestCase):
    """Test datetime encoding and decoding."""
    
    def test_datetime_now(self):
        dt = datetime.now(timezone.utc)
        result = unpackb(packb(dt))
        # Compare with some tolerance for floating point
        self.assertAlmostEqual(result.timestamp(), dt.timestamp(), places=6)
    
    def test_datetime_specific(self):
        dt = datetime(2024, 1, 15, 10, 30, 45, tzinfo=timezone.utc)
        result = unpackb(packb(dt))
        self.assertEqual(result.year, dt.year)
        self.assertEqual(result.month, dt.month)
        self.assertEqual(result.day, dt.day)
        self.assertEqual(result.hour, dt.hour)
        self.assertEqual(result.minute, dt.minute)
        self.assertEqual(result.second, dt.second)


class TestComplexData(unittest.TestCase):
    """Test complex data structures."""
    
    def test_complex_nested_structure(self):
        data = {
            "users": [
                {
                    "id": 1,
                    "name": "Alice",
                    "email": "alice@example.com",
                    "scores": [95, 87, 92],
                    "metadata": {
                        "created_at": datetime(2024, 1, 1, tzinfo=timezone.utc),
                        "updated_at": datetime(2024, 6, 15, tzinfo=timezone.utc),
                        "tags": ["admin", "verified"]
                    }
                },
                {
                    "id": 2,
                    "name": "Bob",
                    "email": "bob@example.com",
                    "scores": [88, 91, 85],
                    "metadata": {
                        "created_at": datetime(2024, 2, 1, tzinfo=timezone.utc),
                        "tags": ["user"]
                    }
                }
            ],
            "config": {
                "max_users": 1000,
                "features": {
                    "notifications": True,
                    "dark_mode": False,
                    "api_access": True
                }
            },
            "binary_data": b"\x00\x01\x02\x03\x04\x05"
        }
        
        packed = packb(data)
        unpacked = unpackb(packed)
        
        # Check structure
        self.assertEqual(len(unpacked["users"]), 2)
        self.assertEqual(unpacked["users"][0]["name"], "Alice")
        self.assertEqual(unpacked["users"][1]["scores"], [88, 91, 85])
        self.assertEqual(unpacked["config"]["max_users"], 1000)
        self.assertEqual(unpacked["binary_data"], b"\x00\x01\x02\x03\x04\x05")


class TestEstimateSize(unittest.TestCase):
    """Test size estimation."""
    
    def test_nil_size(self):
        self.assertEqual(estimate_size(None), 1)
    
    def test_bool_size(self):
        self.assertEqual(estimate_size(True), 1)
        self.assertEqual(estimate_size(False), 1)
    
    def test_int_sizes(self):
        self.assertEqual(estimate_size(0), 1)
        self.assertEqual(estimate_size(127), 1)
        self.assertEqual(estimate_size(128), 2)
        self.assertEqual(estimate_size(32767), 3)
        self.assertEqual(estimate_size(-1), 1)
        self.assertEqual(estimate_size(-33), 2)
    
    def test_float_size(self):
        self.assertEqual(estimate_size(3.14), 9)
    
    def test_string_sizes(self):
        self.assertEqual(estimate_size("a"), 2)  # 1 byte header + 1 char
        self.assertEqual(estimate_size("hello"), 6)  # 1 byte header + 5 chars
    
    def test_array_size(self):
        self.assertEqual(estimate_size([]), 1)  # Empty array
        self.assertEqual(estimate_size([1, 2, 3]), 4)  # 1 byte header + 3 * 1 byte
    
    def test_map_size(self):
        self.assertEqual(estimate_size({}), 1)  # Empty map
        # {"a": 1} = 1 (header) + 2 (key "a") + 1 (value 1) = 4
        self.assertEqual(estimate_size({"a": 1}), 4)
    
    def test_estimate_matches_actual(self):
        data = [1, 2, 3, "hello", {"key": "value"}]
        estimated = estimate_size(data)
        actual = len(packb(data))
        # Estimate should be exact or upper bound
        self.assertGreaterEqual(estimated, actual)


class TestCompareWithJson(unittest.TestCase):
    """Test JSON comparison."""
    
    def test_simple_object(self):
        result = compare_with_json({"name": "Alice", "age": 30})
        self.assertIn('msgpack_size', result)
        self.assertIn('json_size', result)
        self.assertIn('compression_ratio', result)
        self.assertIn('bytes_saved', result)
        self.assertIn('percent_smaller', result)
    
    def test_msgpack_more_efficient(self):
        # MessagePack should generally be smaller for binary data
        data = {
            "data": list(range(100)),
            "name": "test_data_with_many_fields",
            "active": True,
            "count": 1000
        }
        result = compare_with_json(data)
        self.assertGreater(result['bytes_saved'], 0)
    
    def test_empty_object(self):
        result = compare_with_json({})
        self.assertEqual(result['msgpack_size'], 1)
        self.assertEqual(result['json_size'], 2)  # {}


class TestIsValidMsgpack(unittest.TestCase):
    """Test validation function."""
    
    def test_valid_data(self):
        self.assertTrue(is_valid_msgpack(packb(None)))
        self.assertTrue(is_valid_msgpack(packb(42)))
        self.assertTrue(is_valid_msgpack(packb("hello")))
        self.assertTrue(is_valid_msgpack(packb([1, 2, 3])))
    
    def test_invalid_data(self):
        self.assertFalse(is_valid_msgpack(b"invalid"))
        self.assertFalse(is_valid_msgpack(b"\xc1"))  # Invalid marker
        self.assertFalse(is_valid_msgpack(b"\x92\x01"))  # Incomplete array


class TestStreaming(unittest.TestCase):
    """Test streaming API."""
    
    def test_pack_unpack_stream(self):
        data = {"key": "value", "numbers": [1, 2, 3]}
        stream = io.BytesIO()
        bytes_written = pack_stream(data, stream)
        self.assertGreater(bytes_written, 0)
        
        stream.seek(0)
        result = unpack_stream(stream)
        self.assertEqual(result, data)
    
    def test_stream_unpacker_single(self):
        data = [1, 2, 3, 4, 5]
        stream = io.BytesIO(packb(data))
        unpacker = StreamUnpacker(stream)
        results = list(unpacker)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], data)
    
    def test_stream_unpacker_multiple(self):
        stream = io.BytesIO()
        items = [
            {"id": 1, "name": "first"},
            {"id": 2, "name": "second"},
            {"id": 3, "name": "third"}
        ]
        for item in items:
            pack_stream(item, stream)
        
        stream.seek(0)
        unpacker = StreamUnpacker(stream)
        results = list(unpacker)
        self.assertEqual(len(results), 3)
        for i, result in enumerate(results):
            self.assertEqual(result, items[i])


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling."""
    
    def test_empty_types(self):
        self.assertEqual(unpackb(packb([])), [])
        self.assertEqual(unpackb(packb({})), {})
        self.assertEqual(unpackb(packb("")), "")
        self.assertEqual(unpackb(packb(b"")), b"")
    
    def test_large_string(self):
        s = "x" * 100000
        self.assertEqual(unpackb(packb(s)), s)
    
    def test_large_array(self):
        a = list(range(10000))
        self.assertEqual(unpackb(packb(a)), a)
    
    def test_large_map(self):
        m = {f"key{i}": i for i in range(1000)}
        self.assertEqual(unpackb(packb(m)), m)
    
    def test_deeply_nested(self):
        # Create deeply nested structure
        data = {"level": 0}
        current = data
        for i in range(1, 100):
            current["nested"] = {"level": i}
            current = current["nested"]
        
        result = unpackb(packb(data))
        # Verify it's still nested by traversing down
        temp = result
        for i in range(100):
            self.assertEqual(temp["level"], i)
            if "nested" in temp:
                temp = temp["nested"]
    
    def test_unicode_preservation(self):
        data = {
            "emoji": "😀🎉🚀",
            "chinese": "中文测试",
            "japanese": "日本語テスト",
            "korean": "한국어 테스트",
            "arabic": "مرحبا بالعالم",
            "mixed": "Hello 世界 🌍"
        }
        result = unpackb(packb(data))
        self.assertEqual(result, data)


class TestEncoderDecoderDirect(unittest.TestCase):
    """Test Encoder and Decoder classes directly."""
    
    def test_encoder_buffer(self):
        encoder = Encoder()
        result = encoder.encode([1, 2, 3])
        self.assertIsInstance(result, bytes)
        self.assertEqual(len(result), 4)  # 1 header + 3 values
    
    def test_decoder_position(self):
        data = packb([1, 2, 3])
        decoder = Decoder(data)
        decoder.decode()
        self.assertEqual(decoder.position, len(data))
        self.assertEqual(decoder.remaining, 0)
    
    def test_decoder_partial(self):
        # Test that decoder can handle partial decoding
        data = packb({"a": 1, "b": 2, "c": 3})
        decoder = Decoder(data)
        result = decoder.decode()
        self.assertEqual(result, {"a": 1, "b": 2, "c": 3})
    
    def test_extra_data_error(self):
        data = packb(42) + packb(43)
        with self.assertRaises(DecodingError):
            unpackb(data)  # Should fail because of extra data


class TestIntegerBoundaries(unittest.TestCase):
    """Test integer encoding boundaries."""
    
    def test_uint8_boundary(self):
        self.assertEqual(unpackb(packb(127)), 127)  # pos fixint max
        self.assertEqual(unpackb(packb(128)), 128)  # uint8 min
        self.assertEqual(unpackb(packb(255)), 255)  # uint8 max
    
    def test_uint16_boundary(self):
        self.assertEqual(unpackb(packb(256)), 256)  # uint16 min
        self.assertEqual(unpackb(packb(65535)), 65535)  # uint16 max
    
    def test_uint32_boundary(self):
        self.assertEqual(unpackb(packb(65536)), 65536)  # uint32 min
    
    def test_int8_boundary(self):
        self.assertEqual(unpackb(packb(-33)), -33)  # neg fixint min + 1
        self.assertEqual(unpackb(packb(-128)), -128)  # int8 min
    
    def test_int16_boundary(self):
        self.assertEqual(unpackb(packb(-129)), -129)  # int16 max + 1
        self.assertEqual(unpackb(packb(-32768)), -32768)  # int16 min


if __name__ == '__main__':
    unittest.main(verbosity=2)