"""
AllToolkit - Bencode Utilities Tests

Comprehensive test suite for bencode encoding/decoding.

Author: AllToolkit
License: MIT
"""

import unittest
import tempfile
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    Bencoder, BencodeError, BencodeEncodeError, BencodeDecodeError, BencodeTypeError,
    encode, decode, decode_to_str_dict, encode_to_file, decode_file,
    decode_file_to_str_dict, bencode_size, validate_bencode, is_bencodable,
    bencode_checksum, bencode_equal
)


class TestBencodeIntegers(unittest.TestCase):
    """Test integer encoding and decoding."""
    
    def test_encode_zero(self):
        self.assertEqual(encode(0), b"i0e")
    
    def test_encode_positive(self):
        self.assertEqual(encode(42), b"i42e")
        self.assertEqual(encode(123456789), b"i123456789e")
    
    def test_encode_negative(self):
        self.assertEqual(encode(-1), b"i-1e")
        self.assertEqual(encode(-42), b"i-42e")
        self.assertEqual(encode(-999999), b"i-999999e")
    
    def test_decode_zero(self):
        self.assertEqual(decode(b"i0e"), 0)
    
    def test_decode_positive(self):
        self.assertEqual(decode(b"i42e"), 42)
        self.assertEqual(decode(b"i123456789e"), 123456789)
    
    def test_decode_negative(self):
        self.assertEqual(decode(b"i-1e"), -1)
        self.assertEqual(decode(b"i-42e"), -42)
    
    def test_decode_invalid_leading_zeros(self):
        with self.assertRaises(BencodeDecodeError):
            decode(b"i042e")
    
    def test_decode_invalid_negative_zero(self):
        with self.assertRaises(BencodeDecodeError):
            decode(b"i-0e")
    
    def test_bool_not_int(self):
        # Booleans should not be treated as integers
        with self.assertRaises(BencodeTypeError):
            encode(True)
        with self.assertRaises(BencodeTypeError):
            encode(False)


class TestBencodeStrings(unittest.TestCase):
    """Test string/bytes encoding and decoding."""
    
    def test_encode_empty_string(self):
        self.assertEqual(encode(""), b"0:")
    
    def test_encode_string(self):
        self.assertEqual(encode("spam"), b"4:spam")
        self.assertEqual(encode("hello"), b"5:hello")
    
    def test_encode_bytes(self):
        self.assertEqual(encode(b"spam"), b"4:spam")
        self.assertEqual(encode(b""), b"0:")
    
    def test_encode_unicode(self):
        # UTF-8 encoding
        # "你好" is 6 bytes in UTF-8
        self.assertEqual(encode("你好"), b"6:\xe4\xbd\xa0\xe5\xa5\xbd")
    
    def test_decode_empty_string(self):
        self.assertEqual(decode(b"0:"), b"")
    
    def test_decode_string(self):
        self.assertEqual(decode(b"4:spam"), b"spam")
        self.assertEqual(decode(b"5:hello"), b"hello")
    
    def test_decode_binary(self):
        # Binary data that's not valid UTF-8
        data = b"\x00\x01\x02\xff"
        self.assertEqual(decode(b"4:" + data), data)
    
    def test_decode_unicode(self):
        encoded = b"6:\xe4\xbd\xa0\xe5\xa5\xbd"  # 你好 in UTF-8
        result = decode(encoded)
        self.assertEqual(result.decode('utf-8'), "你好")


class TestBencodeLists(unittest.TestCase):
    """Test list encoding and decoding."""
    
    def test_encode_empty_list(self):
        self.assertEqual(encode([]), b"le")
    
    def test_encode_list_of_integers(self):
        self.assertEqual(encode([1, 2, 3]), b"li1ei2ei3ee")
    
    def test_encode_list_of_strings(self):
        self.assertEqual(encode(["spam", "eggs"]), b"l4:spam4:eggse")
    
    def test_encode_mixed_list(self):
        self.assertEqual(encode(["spam", 42]), b"l4:spami42ee")
    
    def test_encode_nested_list(self):
        self.assertEqual(encode([[1, 2], [3, 4]]), b"lli1ei2eeli3ei4eee")
    
    def test_decode_empty_list(self):
        self.assertEqual(decode(b"le"), [])
    
    def test_decode_list_of_integers(self):
        self.assertEqual(decode(b"li1ei2ei3ee"), [1, 2, 3])
    
    def test_decode_list_of_strings(self):
        self.assertEqual(decode(b"l4:spam4:eggse"), [b"spam", b"eggs"])
    
    def test_decode_mixed_list(self):
        self.assertEqual(decode(b"l4:spami42ee"), [b"spam", 42])
    
    def test_decode_nested_list(self):
        self.assertEqual(decode(b"lli1ei2eeli3ei4eee"), [[1, 2], [3, 4]])


class TestBencodeDicts(unittest.TestCase):
    """Test dictionary encoding and decoding."""
    
    def test_encode_empty_dict(self):
        self.assertEqual(encode({}), b"de")
    
    def test_encode_simple_dict(self):
        # Keys are sorted lexicographically
        self.assertEqual(encode({"spam": "eggs"}), b"d4:spam4:eggse")
    
    def test_encode_dict_sorted_keys(self):
        # Keys should be sorted
        result = encode({"z": 1, "a": 2})
        self.assertEqual(result, b"d1:ai2e1:zi1ee")
    
    def test_encode_dict_bytes_keys(self):
        self.assertEqual(encode({b"spam": b"eggs"}), b"d4:spam4:eggse")
    
    def test_encode_nested_dict(self):
        result = encode({"outer": {"inner": 42}})
        self.assertEqual(result, b"d5:outerd5:inneri42eee")
    
    def test_decode_empty_dict(self):
        self.assertEqual(decode(b"de"), {})
    
    def test_decode_simple_dict(self):
        self.assertEqual(decode(b"d4:spam4:eggse"), {b"spam": b"eggs"})
    
    def test_decode_dict_sorted_keys(self):
        result = decode(b"d1:ai2e1:zi1ee")
        self.assertEqual(result, {b"a": 2, b"z": 1})
    
    def test_decode_nested_dict(self):
        result = decode(b"d5:outerd5:inneri42eee")
        self.assertEqual(result, {b"outer": {b"inner": 42}})
    
    def test_decode_unsorted_keys_error(self):
        # Keys must be sorted
        with self.assertRaises(BencodeDecodeError):
            decode(b"d1:zi1e1:ai2ee")  # z before a


class TestComplexStructures(unittest.TestCase):
    """Test complex nested structures."""
    
    def test_torrent_like_structure(self):
        """Test a structure similar to a torrent file."""
        data = {
            "announce": "http://tracker.example.com/announce",
            "info": {
                "name": "test.torrent",
                "piece length": 16384,
                "length": 12345678,
                "pieces": b"\x00" * 20  # 20-byte SHA1 hash
            },
            "creation date": 1234567890,
            "comment": "Test torrent"
        }
        
        encoded = encode(data)
        decoded = decode(encoded)
        
        # Verify structure
        self.assertEqual(decoded[b"announce"], b"http://tracker.example.com/announce")
        self.assertEqual(decoded[b"creation date"], 1234567890)
        self.assertEqual(decoded[b"comment"], b"Test torrent")
        
        info = decoded[b"info"]
        self.assertEqual(info[b"name"], b"test.torrent")
        self.assertEqual(info[b"piece length"], 16384)
        self.assertEqual(info[b"length"], 12345678)
    
    def test_deeply_nested(self):
        """Test deeply nested structures."""
        data = {"a": {"b": {"c": {"d": {"e": 42}}}}}
        encoded = encode(data)
        decoded = decode(encoded)
        
        self.assertEqual(decoded[b"a"][b"b"][b"c"][b"d"][b"e"], 42)
    
    def test_list_of_dicts(self):
        """Test list containing dictionaries."""
        data = [{"id": 1}, {"id": 2}]
        encoded = encode(data)
        decoded = decode(encoded)
        
        self.assertEqual(decoded[0][b"id"], 1)
        self.assertEqual(decoded[1][b"id"], 2)


class TestDecodeToStrDict(unittest.TestCase):
    """Test decode_to_str_dict function."""
    
    def test_simple_dict(self):
        data = encode({"foo": "bar", "num": 42})
        result = decode_to_str_dict(data)
        self.assertEqual(result["foo"], b"bar")
        self.assertEqual(result["num"], 42)
    
    def test_nested_dict(self):
        data = encode({"outer": {"inner": "value"}})
        result = decode_to_str_dict(data)
        self.assertEqual(result, {"outer": {"inner": b"value"}})
    
    def test_list_in_dict(self):
        data = encode({"items": [1, 2, 3]})
        result = decode_to_str_dict(data)
        self.assertEqual(result, {"items": [1, 2, 3]})


class TestFileIO(unittest.TestCase):
    """Test file I/O operations."""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_encode_to_file_and_decode(self):
        data = {"name": "test", "value": 42, "items": [1, 2, 3]}
        filepath = os.path.join(self.temp_dir, "test.bencode")
        
        encode_to_file(data, filepath)
        result = decode_file(filepath)
        
        self.assertEqual(result[b"name"], b"test")
        self.assertEqual(result[b"value"], 42)
        self.assertEqual(result[b"items"], [1, 2, 3])
    
    def test_decode_file_to_str_dict(self):
        data = {"name": "test", "value": 42}
        filepath = os.path.join(self.temp_dir, "test.bencode")
        
        encode_to_file(data, filepath)
        result = decode_file_to_str_dict(filepath)
        
        self.assertEqual(result["name"], b"test")
        self.assertEqual(result["value"], 42)


class TestUtilityFunctions(unittest.TestCase):
    """Test utility functions."""
    
    def test_bencode_size_int(self):
        self.assertEqual(bencode_size(42), 4)  # i42e
        self.assertEqual(bencode_size(0), 3)   # i0e
        self.assertEqual(bencode_size(-1), 4)  # i-1e
    
    def test_bencode_size_string(self):
        self.assertEqual(bencode_size("spam"), 6)  # 4:spam
        self.assertEqual(bencode_size(""), 2)       # 0:
    
    def test_bencode_size_list(self):
        self.assertEqual(bencode_size([]), 2)              # le
        self.assertEqual(bencode_size([1, 2, 3]), 11)  # li1ei2ei3ee (l + i1e + i2e + i3e + e)
    
    def test_bencode_size_dict(self):
        self.assertEqual(bencode_size({}), 2)  # de
        self.assertEqual(bencode_size({"a": 1}), 8)  # d1:ai1ee
    
    def test_validate_bencode_valid(self):
        is_valid, error = validate_bencode(b"i42e")
        self.assertTrue(is_valid)
        self.assertIsNone(error)
    
    def test_validate_bencode_invalid(self):
        is_valid, error = validate_bencode(b"invalid")
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)
    
    def test_is_bencodable_int(self):
        self.assertTrue(is_bencodable(42))
        self.assertTrue(is_bencodable(-1))
    
    def test_is_bencodable_string(self):
        self.assertTrue(is_bencodable("hello"))
        self.assertTrue(is_bencodable(b"bytes"))
    
    def test_is_bencodable_list(self):
        self.assertTrue(is_bencodable([1, 2, 3]))
        self.assertTrue(is_bencodable(["a", "b"]))
    
    def test_is_bencodable_dict(self):
        self.assertTrue(is_bencodable({"a": 1}))
        self.assertTrue(is_bencodable({b"a": b"b"}))
    
    def test_is_not_bencodable(self):
        self.assertFalse(is_bencodable(3.14))  # float
        self.assertFalse(is_bencodable(None))
        self.assertFalse(is_bencodable(set()))
        self.assertFalse(is_bencodable(object()))
    
    def test_bencode_checksum(self):
        data1 = {"a": 1}
        data2 = {"a": 1}
        data3 = {"a": 2}
        
        self.assertEqual(bencode_checksum(data1), bencode_checksum(data2))
        self.assertNotEqual(bencode_checksum(data1), bencode_checksum(data3))
    
    def test_bencode_equal_same(self):
        self.assertTrue(bencode_equal({"a": 1}, {"a": 1}))
        self.assertTrue(bencode_equal([1, 2], [1, 2]))
    
    def test_bencode_equal_different(self):
        self.assertFalse(bencode_equal({"a": 1}, {"a": 2}))
        self.assertFalse(bencode_equal([1, 2], [2, 1]))
    
    def test_bencode_equal_str_bytes_key(self):
        # String keys are encoded as bytes, so they should be equal
        self.assertTrue(bencode_equal({"a": 1}, {b"a": 1}))


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling."""
    
    def test_empty_structures(self):
        self.assertEqual(encode([]), b"le")
        self.assertEqual(encode({}), b"de")
        self.assertEqual(decode(b"le"), [])
        self.assertEqual(decode(b"de"), {})
    
    def test_large_integer(self):
        large = 10**18
        encoded = encode(large)
        decoded = decode(encoded)
        self.assertEqual(decoded, large)
    
    def test_negative_large_integer(self):
        large = -(10**18)
        encoded = encode(large)
        decoded = decode(encoded)
        self.assertEqual(decoded, large)
    
    def test_long_string(self):
        s = "a" * 10000
        encoded = encode(s)
        decoded = decode(encoded)
        self.assertEqual(decoded, s.encode('utf-8'))
    
    def test_deeply_nested_list(self):
        data = [[[[[[[42]]]]]]]
        encoded = encode(data)
        decoded = decode(encoded)
        self.assertEqual(decoded, data)
    
    def test_deeply_nested_dict(self):
        data = {"a": {"b": {"c": {"d": {"e": {"f": {"g": 42}}}}}}}
        encoded = encode(data)
        decoded = decode(encoded)
        self.assertEqual(decoded[b"a"][b"b"][b"c"][b"d"][b"e"][b"f"][b"g"], 42)
    
    def test_invalid_type_float(self):
        with self.assertRaises(BencodeTypeError):
            encode(3.14)
    
    def test_invalid_type_none(self):
        with self.assertRaises(BencodeTypeError):
            encode(None)
    
    def test_invalid_type_set(self):
        with self.assertRaises(BencodeTypeError):
            encode({1, 2, 3})
    
    def test_invalid_dict_key_int(self):
        with self.assertRaises(BencodeTypeError):
            encode({1: "value"})
    
    def test_decode_truncated_int(self):
        with self.assertRaises(BencodeDecodeError):
            decode(b"i42")
    
    def test_decode_truncated_string(self):
        with self.assertRaises(BencodeDecodeError):
            decode(b"4:spa")
    
    def test_decode_truncated_list(self):
        with self.assertRaises(BencodeDecodeError):
            decode(b"li42e")
    
    def test_decode_truncated_dict(self):
        with self.assertRaises(BencodeDecodeError):
            decode(b"d3:foo")
    
    def test_decode_extra_data(self):
        with self.assertRaises(BencodeDecodeError):
            decode(b"i42eextra")


class TestBencoderClass(unittest.TestCase):
    """Test Bencoder class methods."""
    
    def test_custom_encoding(self):
        encoder = Bencoder(encoding='latin-1')
        data = "café"
        encoded = encoder.encode(data)
        decoded = encoder.decode(encoded)
        self.assertEqual(decoded, data.encode('latin-1'))
    
    def test_parse_torrent_info_single_file(self):
        """Test parsing a single-file torrent structure."""
        encoder = Bencoder()
        
        # Create a minimal torrent-like structure
        torrent_data = {
            "announce": "http://tracker.example.com/announce",
            "info": {
                "name": "test.txt",
                "piece length": 16384,
                "length": 1024,
                "pieces": b"\x00" * 20
            },
            "creation date": 1234567890
        }
        
        # Write to temp file
        with tempfile.NamedTemporaryFile(mode='wb', suffix='.torrent', delete=False) as f:
            f.write(encoder.encode(torrent_data))
            filepath = f.name
        
        try:
            info = encoder.parse_torrent_info(filepath)
            self.assertEqual(info['announce'], "http://tracker.example.com/announce")
            self.assertEqual(info['info']['name'], "test.txt")
            self.assertEqual(info['info']['piece_length'], 16384)
            self.assertEqual(info['info']['length'], 1024)
            self.assertEqual(info['creation_date'], 1234567890)
        finally:
            os.unlink(filepath)
    
    def test_get_torrent_files_single(self):
        """Test getting files from single-file torrent."""
        encoder = Bencoder()
        
        torrent_data = {
            "info": {
                "name": "test.txt",
                "piece length": 16384,
                "length": 1024,
                "pieces": b"\x00" * 20
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='wb', suffix='.torrent', delete=False) as f:
            f.write(encoder.encode(torrent_data))
            filepath = f.name
        
        try:
            files = encoder.get_torrent_files(filepath)
            self.assertEqual(len(files), 1)
            self.assertEqual(files[0]['path'], 'test.txt')
            self.assertEqual(files[0]['size'], 1024)
        finally:
            os.unlink(filepath)
    
    def test_get_torrent_total_size(self):
        """Test getting total size of torrent."""
        encoder = Bencoder()
        
        torrent_data = {
            "info": {
                "name": "test",
                "piece length": 16384,
                "files": [
                    {"path": ["file1.txt"], "length": 1024},
                    {"path": ["file2.txt"], "length": 2048}
                ],
                "pieces": b"\x00" * 20
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='wb', suffix='.torrent', delete=False) as f:
            f.write(encoder.encode(torrent_data))
            filepath = f.name
        
        try:
            total = encoder.get_torrent_total_size(filepath)
            self.assertEqual(total, 3072)
        finally:
            os.unlink(filepath)


class TestRoundTrip(unittest.TestCase):
    """Test round-trip encoding/decoding."""
    
    def test_roundtrip_integers(self):
        values = [0, 1, -1, 42, -42, 123456789, -123456789]
        for v in values:
            with self.subTest(value=v):
                self.assertEqual(decode(encode(v)), v)
    
    def test_roundtrip_strings(self):
        values = ["", "a", "hello", "hello world", "你好世界"]
        for v in values:
            with self.subTest(value=v):
                # Strings are decoded as bytes
                self.assertEqual(decode(encode(v)), v.encode('utf-8'))
    
    def test_roundtrip_lists(self):
        values = [
            [],
            [1],
            [1, 2, 3],
            [],  # skip string list since strings become bytes
            [1, 2, 3],
            [[1, 2], [3, 4]],
            [[[[1]]]]
        ]
        for v in values:
            with self.subTest(value=v):
                self.assertEqual(decode(encode(v)), v)
    
    def test_roundtrip_lists_with_strings(self):
        """Test lists with strings - they decode as bytes."""
        values = ["a", "b", "c"]
        encoded = encode(values)
        decoded = decode(encoded)
        # Strings decode as bytes
        self.assertEqual(decoded, [b"a", b"b", b"c"])
    
    def test_roundtrip_dicts(self):
        values = [
            {},
            {"a": 1},
            {"a": 1, "b": 2},
            {"outer": {"inner": 42}},
            {"list": [1, 2, 3], "num": 42}
        ]
        for v in values:
            with self.subTest(value=v):
                encoded = encode(v)
                decoded = decode(encoded)
                # Keys become bytes after decoding
                expected = {k.encode('utf-8'): v2 for k, v2 in v.items()}
                # Recursively convert nested dict keys
                def convert_keys(d):
                    result = {}
                    for k, v in d.items():
                        if isinstance(k, bytes):
                            k = k.decode('utf-8')
                        if isinstance(v, dict):
                            v = {k2.encode('utf-8') if isinstance(k2, str) else k2: v2 for k2, v2 in v.items()}
                        result[k.encode('utf-8') if isinstance(k, str) else k] = v
                    return result
                self.assertEqual(decoded, convert_keys(expected))


if __name__ == "__main__":
    unittest.main(verbosity=2)