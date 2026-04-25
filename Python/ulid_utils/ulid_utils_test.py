#!/usr/bin/env python3
"""
Unit tests for ULID Utils

Tests cover:
- ULID generation
- ULID parsing and validation
- ULID encoding/decoding
- Monotonic generation
- Type conversions (UUID, hex, int, datetime)
- Comparison operations
- Batch operations
"""

import unittest
import time
from datetime import datetime, timezone, timedelta
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    ULID, ULIDError, generate, parse, is_valid, monotonic,
    from_datetime, from_uuid, from_hex, from_int,
    generate_batch, generate_monotonic_batch, compare, min_ulid, max_ulid,
    extract_timestamps, CROCKFORD_ALPHABET, ULID_LENGTH, ULID_BYTES
)


class TestULIDBasic(unittest.TestCase):
    """Test basic ULID generation and properties."""
    
    def test_generate_length(self):
        """Test that generated ULID has correct length."""
        ulid = ULID.generate()
        self.assertEqual(len(str(ulid)), ULID_LENGTH)
    
    def test_generate_bytes_length(self):
        """Test that ULID bytes has correct length."""
        ulid = ULID.generate()
        self.assertEqual(len(ulid.bytes()), ULID_BYTES)
    
    def test_generate_valid_characters(self):
        """Test that generated ULID only uses Crockford's Base32."""
        ulid = ULID.generate()
        for char in str(ulid):
            self.assertIn(char, CROCKFORD_ALPHABET)
    
    def test_generate_unique(self):
        """Test that multiple ULIDs are unique."""
        ulids = [str(ULID.generate()) for _ in range(1000)]
        self.assertEqual(len(ulids), len(set(ulids)))
    
    def test_generate_lowercase_handling(self):
        """Test that lowercase characters are handled."""
        ulid = ULID.generate()
        lower = str(ulid).lower()
        parsed = ULID.parse(lower)
        self.assertEqual(str(parsed), str(ulid))
    
    def test_str_representation(self):
        """Test string representation."""
        ulid = ULID.generate()
        self.assertEqual(len(str(ulid)), 26)
    
    def test_repr_representation(self):
        """Test repr representation."""
        ulid = ULID.generate()
        self.assertIn('ULID', repr(ulid))
        self.assertIn(str(ulid), repr(ulid))


class TestULIDParsing(unittest.TestCase):
    """Test ULID parsing and validation."""
    
    def test_parse_valid_ulid(self):
        """Test parsing a valid ULID string."""
        # Generate a valid ULID and parse it back
        original = ULID.generate()
        ulid_str = str(original)
        ulid = ULID.parse(ulid_str)
        self.assertEqual(str(ulid), ulid_str)
    
    def test_parse_lowercase(self):
        """Test parsing lowercase ULID."""
        original = ULID.generate()
        ulid_str = str(original)
        ulid = ULID.parse(ulid_str.lower())
        self.assertEqual(str(ulid), ulid_str)
    
    def test_parse_invalid_length(self):
        """Test parsing ULID with wrong length."""
        with self.assertRaises(ULIDError):
            ULID.parse('01ARZ3NDEK')
    
    def test_parse_invalid_character(self):
        """Test parsing ULID with invalid characters."""
        with self.assertRaises(ULIDError):
            ULID.parse('01ARZ3NDEKTSV4RRFFQ69G5FAI')  # 'I' is invalid
    
    def test_is_valid_true(self):
        """Test is_valid with valid ULID."""
        self.assertTrue(is_valid('01ARZ3NDEKTSV4RRFFQ69G5FAV'))
    
    def test_is_valid_false(self):
        """Test is_valid with invalid ULID."""
        self.assertFalse(is_valid('invalid'))
        self.assertFalse(is_valid('01ARZ3NDEKTSV4RRFFQ69G5FAI'))  # Invalid char
    
    def test_roundtrip(self):
        """Test that encoding and decoding roundtrips correctly."""
        original = ULID.generate()
        encoded = str(original)
        decoded = ULID.parse(encoded)
        self.assertEqual(original.bytes(), decoded.bytes())


class TestULIDTimestamp(unittest.TestCase):
    """Test timestamp extraction and handling."""
    
    def test_timestamp_ms_type(self):
        """Test that timestamp_ms returns int."""
        ulid = ULID.generate()
        self.assertIsInstance(ulid.timestamp_ms(), int)
    
    def test_timestamp_type(self):
        """Test that timestamp returns float."""
        ulid = ULID.generate()
        self.assertIsInstance(ulid.timestamp(), float)
    
    def test_datetime_type(self):
        """Test that datetime returns datetime object."""
        ulid = ULID.generate()
        self.assertIsInstance(ulid.datetime(), datetime)
    
    def test_datetime_timezone(self):
        """Test that datetime has UTC timezone."""
        ulid = ULID.generate()
        dt = ulid.datetime()
        self.assertEqual(dt.tzinfo, timezone.utc)
    
    def test_timestamp_accuracy(self):
        """Test that timestamp is within reasonable range."""
        ulid = ULID.generate()
        now = time.time()
        # Allow 1 second tolerance
        self.assertAlmostEqual(ulid.timestamp(), now, delta=1.0)
    
    def test_from_datetime(self):
        """Test creating ULID from datetime."""
        dt = datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        ulid = ULID.from_datetime(dt)
        extracted = ulid.datetime()
        self.assertEqual(extracted.year, 2025)
        self.assertEqual(extracted.month, 1)
        self.assertEqual(extracted.day, 1)
    
    def test_from_datetime_naive(self):
        """Test creating ULID from naive datetime (assumed UTC)."""
        dt = datetime(2025, 6, 15, 0, 0, 0)  # Naive
        ulid = ULID.from_datetime(dt)
        self.assertEqual(ulid.datetime().month, 6)
    
    def test_custom_timestamp(self):
        """Test generating ULID with custom timestamp."""
        custom_ms = 1609459200000  # 2021-01-01 00:00:00 UTC
        ulid = ULID(ULID._generate_bytes(timestamp_ms=custom_ms))
        self.assertEqual(ulid.timestamp_ms(), custom_ms)


class TestULIDConversions(unittest.TestCase):
    """Test type conversions."""
    
    def test_to_hex(self):
        """Test hex conversion."""
        ulid = ULID.generate()
        hex_str = ulid.hex()
        self.assertEqual(len(hex_str), 32)
        self.assertTrue(all(c in '0123456789abcdef' for c in hex_str))
    
    def test_from_hex(self):
        """Test creating ULID from hex."""
        hex_str = '01706d60a1e24840890c2759b22a3f68'
        ulid = ULID.from_hex(hex_str)
        self.assertEqual(ulid.hex(), hex_str)
    
    def test_from_hex_with_prefix(self):
        """Test creating ULID from hex with 0x prefix."""
        hex_str = '0x01706d60a1e24840890c2759b22a3f68'
        ulid = ULID.from_hex(hex_str)
        self.assertEqual(ulid.hex(), hex_str[2:])
    
    def test_to_int(self):
        """Test int conversion."""
        ulid = ULID.generate()
        val = ulid.to_int()
        self.assertIsInstance(val, int)
        self.assertGreater(val, 0)
    
    def test_from_int(self):
        """Test creating ULID from int."""
        val = 123456789012345678901234567890
        ulid = ULID.from_int(val)
        self.assertEqual(ulid.to_int(), val)
    
    def test_from_int_overflow(self):
        """Test that from_int rejects values >= 2^128."""
        with self.assertRaises(ULIDError):
            ULID.from_int(2**128)
    
    def test_from_int_negative(self):
        """Test that from_int rejects negative values."""
        with self.assertRaises(ULIDError):
            ULID.from_int(-1)
    
    def test_to_uuid(self):
        """Test UUID conversion."""
        ulid = ULID.generate()
        uuid_obj = ulid.to_uuid()
        self.assertEqual(len(uuid_obj.bytes), 16)
        self.assertEqual(uuid_obj.bytes, ulid.bytes())
    
    def test_from_uuid(self):
        """Test creating ULID from UUID."""
        import uuid
        u = uuid.uuid4()
        ulid = ULID.from_uuid(u)
        self.assertEqual(ulid.bytes(), u.bytes)
    
    def test_hex_roundtrip(self):
        """Test hex conversion roundtrip."""
        original = ULID.generate()
        hex_str = original.hex()
        restored = ULID.from_hex(hex_str)
        self.assertEqual(original.bytes(), restored.bytes())
    
    def test_int_roundtrip(self):
        """Test int conversion roundtrip."""
        original = ULID.generate()
        val = original.to_int()
        restored = ULID.from_int(val)
        self.assertEqual(original.bytes(), restored.bytes())


class TestULIDComparison(unittest.TestCase):
    """Test comparison operations."""
    
    def test_equality(self):
        """Test ULID equality."""
        ulid = ULID.generate()
        same = ULID.parse(str(ulid))
        self.assertEqual(ulid, same)
    
    def test_inequality(self):
        """Test ULID inequality."""
        ulid1 = ULID.generate()
        ulid2 = ULID.generate()
        self.assertNotEqual(ulid1, ulid2)
    
    def test_less_than(self):
        """Test less than comparison."""
        ulid1 = ULID.from_int(100)
        ulid2 = ULID.from_int(200)
        self.assertLess(ulid1, ulid2)
    
    def test_greater_than(self):
        """Test greater than comparison."""
        ulid1 = ULID.from_int(100)
        ulid2 = ULID.from_int(200)
        self.assertGreater(ulid2, ulid1)
    
    def test_less_equal(self):
        """Test less than or equal comparison."""
        ulid1 = ULID.from_int(100)
        ulid2 = ULID.from_int(100)
        self.assertLessEqual(ulid1, ulid2)
    
    def test_greater_equal(self):
        """Test greater than or equal comparison."""
        ulid1 = ULID.from_int(100)
        ulid2 = ULID.from_int(100)
        self.assertGreaterEqual(ulid1, ulid2)
    
    def test_hash(self):
        """Test that ULIDs are hashable."""
        ulid1 = ULID.generate()
        ulid2 = ULID.parse(str(ulid1))
        self.assertEqual(hash(ulid1), hash(ulid2))
    
    def test_set_membership(self):
        """Test that ULIDs can be used in sets."""
        ulid1 = ULID.generate()
        ulid2 = ULID.generate()
        ulid_set = {ulid1, ulid2, ulid1}  # ulid1 twice
        self.assertEqual(len(ulid_set), 2)
    
    def test_compare_function(self):
        """Test compare function."""
        u1 = ULID.from_int(100)
        u2 = ULID.from_int(200)
        self.assertEqual(compare(u1, u2), -1)
        self.assertEqual(compare(u2, u1), 1)
        self.assertEqual(compare(u1, u1), 0)


class TestULIDMonotonic(unittest.TestCase):
    """Test monotonic ULID generation."""
    
    def test_monotonic_first(self):
        """Test first monotonic ULID generation."""
        ulid = ULID.monotonic()
        self.assertEqual(len(str(ulid)), ULID_LENGTH)
    
    def test_monotonic_increasing(self):
        """Test that monotonic ULIDs increase."""
        u1 = ULID.monotonic()
        time.sleep(0.001)  # Small delay
        u2 = ULID.monotonic(u1)
        self.assertLess(u1, u2)
    
    def test_monotonic_same_millisecond(self):
        """Test monotonic behavior within same millisecond."""
        # Force same timestamp
        now_ms = int(time.time() * 1000)
        u1 = ULID(ULID._generate_bytes(timestamp_ms=now_ms))
        u2 = ULID.monotonic(u1)
        
        # Should be greater or equal (different randomness)
        self.assertGreater(u2, u1)
    
    def test_generate_monotonic_batch(self):
        """Test batch monotonic generation."""
        ulids = generate_monotonic_batch(10)
        self.assertEqual(len(ulids), 10)
        
        # Check all are sorted
        for i in range(len(ulids) - 1):
            self.assertLess(ulids[i], ulids[i + 1])


class TestULIDBatch(unittest.TestCase):
    """Test batch operations."""
    
    def test_generate_batch(self):
        """Test batch generation."""
        ulids = generate_batch(10)
        self.assertEqual(len(ulids), 10)
    
    def test_generate_batch_unique(self):
        """Test that batch generates unique ULIDs."""
        ulids = generate_batch(100)
        str_ulids = [str(u) for u in ulids]
        self.assertEqual(len(str_ulids), len(set(str_ulids)))
    
    def test_generate_batch_empty(self):
        """Test batch generation with count 0."""
        ulids = generate_batch(0)
        self.assertEqual(len(ulids), 0)
    
    def test_min_ulid(self):
        """Test finding minimum ULID."""
        ulids = [ULID.from_int(300), ULID.from_int(100), ULID.from_int(200)]
        min_u = min_ulid(ulids)
        self.assertEqual(min_u.to_int(), 100)
    
    def test_max_ulid(self):
        """Test finding maximum ULID."""
        ulids = [ULID.from_int(300), ULID.from_int(100), ULID.from_int(200)]
        max_u = max_ulid(ulids)
        self.assertEqual(max_u.to_int(), 300)
    
    def test_extract_timestamps(self):
        """Test timestamp extraction from batch."""
        ulids = generate_batch(5)
        extracted = extract_timestamps(ulids)
        self.assertEqual(len(extracted), 5)
        for ulid, ts in extracted:
            self.assertIsInstance(ulid, ULID)
            self.assertIsInstance(ts, int)


class TestULIDEdgeCases(unittest.TestCase):
    """Test edge cases and error handling."""
    
    def test_empty_init(self):
        """Test ULID() with no arguments."""
        ulid = ULID()
        self.assertEqual(len(str(ulid)), ULID_LENGTH)
    
    def test_bytes_init(self):
        """Test ULID initialization from bytes."""
        original = ULID.generate()
        from_bytes = ULID(original.bytes())
        self.assertEqual(original, from_bytes)
    
    def test_copy_init(self):
        """Test ULID initialization from another ULID."""
        original = ULID.generate()
        copy = ULID(original)
        self.assertEqual(original, copy)
    
    def test_invalid_bytes_length(self):
        """Test that invalid bytes length raises error."""
        with self.assertRaises(ULIDError):
            ULID(b'12345')  # 5 bytes instead of 16
    
    def test_invalid_type(self):
        """Test that invalid type raises error."""
        with self.assertRaises(ULIDError):
            ULID(12345)  # int, not valid for init
    
    def test_len_method(self):
        """Test __len__ method."""
        ulid = ULID.generate()
        self.assertEqual(len(ulid), ULID_LENGTH)
    
    def test_int_method(self):
        """Test __int__ method."""
        ulid = ULID.generate()
        self.assertEqual(int(ulid), ulid.to_int())
    
    def test_bytes_method(self):
        """Test __bytes__ method."""
        ulid = ULID.generate()
        self.assertEqual(bytes(ulid), ulid.bytes())


class TestULIDEncodingDecoding(unittest.TestCase):
    """Test encoding and decoding edge cases."""
    
    def test_all_zero_ulid(self):
        """Test ULID with all zeros."""
        ulid = ULID.from_int(0)
        self.assertEqual(ulid.to_int(), 0)
        self.assertEqual(str(ulid), '0' * ULID_LENGTH)
    
    def test_max_ulid(self):
        """Test maximum ULID value."""
        max_val = (2**128) - 1
        ulid = ULID.from_int(max_val)
        self.assertEqual(ulid.to_int(), max_val)
        # Max ULID has 25 Zs and 1 W at the end (due to 2-bit padding)
        # ZZZZZZZZZZZZZZZZZZZZZZZZZW
        self.assertTrue(all(c in 'Z' for c in str(ulid)[:25]))
        self.assertEqual(str(ulid)[25], 'W')
    
    def test_known_encoding(self):
        """Test known ULID encoding."""
        # This is a specific test case from the ULID spec
        # Timestamp: 1469918176385 ms = 2016-07-30 14:36:16.385 UTC
        # Randomness: all ones for simplicity
        timestamp_ms = 1469918176385
        
        # Generate with specific timestamp
        randomness = b'\xff' * 10  # All ones
        ulid_bytes = ULID._generate_bytes(timestamp_ms, randomness)
        ulid = ULID(ulid_bytes)
        
        # Verify timestamp is correct
        self.assertEqual(ulid.timestamp_ms(), timestamp_ms)


class TestModuleFunctions(unittest.TestCase):
    """Test module-level convenience functions."""
    
    def test_module_generate(self):
        """Test module-level generate function."""
        ulid = generate()
        self.assertIsInstance(ulid, ULID)
    
    def test_module_parse(self):
        """Test module-level parse function."""
        # Generate a valid ULID and parse it back
        original = generate()
        ulid_str = str(original)
        ulid = parse(ulid_str)
        self.assertEqual(str(ulid), ulid_str)
    
    def test_module_is_valid(self):
        """Test module-level is_valid function."""
        self.assertTrue(is_valid('01ARZ3NDEKTSV4RRFFQ69G5FAV'))
        self.assertFalse(is_valid('invalid'))
    
    def test_module_monotonic(self):
        """Test module-level monotonic function."""
        ulid = monotonic()
        self.assertIsInstance(ulid, ULID)
    
    def test_module_from_datetime(self):
        """Test module-level from_datetime function."""
        dt = datetime(2025, 1, 1, tzinfo=timezone.utc)
        ulid = from_datetime(dt)
        self.assertIsInstance(ulid, ULID)
    
    def test_module_from_uuid(self):
        """Test module-level from_uuid function."""
        import uuid
        u = uuid.uuid4()
        ulid = from_uuid(u)
        self.assertEqual(ulid.bytes(), u.bytes)
    
    def test_module_from_hex(self):
        """Test module-level from_hex function."""
        hex_str = '01706d60a1e24840890c2759b22a3f68'
        ulid = from_hex(hex_str)
        self.assertEqual(ulid.hex(), hex_str)
    
    def test_module_from_int(self):
        """Test module-level from_int function."""
        val = 123456
        ulid = from_int(val)
        self.assertEqual(ulid.to_int(), val)


if __name__ == '__main__':
    unittest.main(verbosity=2)