"""
AllToolkit - Python UUID Utilities Test Suite

Comprehensive test suite for UUID generation and manipulation utilities.
Run with: python uuid_utils_test.py

Tests cover:
- UUID generation (v1, v3, v4, v5)
- UUID validation and parsing
- UUID conversion (string, bytes, int)
- UUID comparison and sorting
- Timestamp and node extraction (v1)
- Batch generation
- Nil UUID handling
- Custom hash-based UUID generation
"""

import sys
import os
from datetime import datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    UUIDUtils,
    generate_v1, generate_v3, generate_v4, generate_v5,
    parse, is_valid, is_valid_fast, get_version, get_variant,
    to_string, to_bytes, from_bytes, to_int, from_int,
    compare, equal, sort, get_timestamp, get_node,
    generate_batch, nil, is_nil, hash_to_uuid
)
import uuid


def test_generate_v1():
    """Test UUID v1 generation."""
    u = UUIDUtils.generate_v1()
    assert isinstance(u, uuid.UUID)
    assert u.version == 1
    assert u.variant == uuid.RFC_4122
    print("✓ test_generate_v1 passed")


def test_generate_v3():
    """Test UUID v3 generation (MD5 namespace-based)."""
    # Test with namespace object
    u1 = UUIDUtils.generate_v3(UUIDUtils.NAMESPACE_DNS, 'example.com')
    assert isinstance(u1, uuid.UUID)
    assert u1.version == 3
    
    # Test determinism - same input produces same output
    u2 = UUIDUtils.generate_v3(UUIDUtils.NAMESPACE_DNS, 'example.com')
    assert u1 == u2
    
    # Test with string namespace
    u3 = UUIDUtils.generate_v3('dns', 'example.com')
    assert u1 == u3
    
    # Different name produces different UUID
    u4 = UUIDUtils.generate_v3(UUIDUtils.NAMESPACE_DNS, 'different.com')
    assert u1 != u4
    
    # Different namespace produces different UUID
    u5 = UUIDUtils.generate_v3(UUIDUtils.NAMESPACE_URL, 'example.com')
    assert u1 != u5
    
    print("✓ test_generate_v3 passed")


def test_generate_v4():
    """Test UUID v4 generation (random)."""
    u = UUIDUtils.generate_v4()
    assert isinstance(u, uuid.UUID)
    assert u.version == 4
    assert u.variant == uuid.RFC_4122
    
    # Two v4 UUIDs should be different (extremely high probability)
    u2 = UUIDUtils.generate_v4()
    assert u != u2
    
    print("✓ test_generate_v4 passed")


def test_generate_v5():
    """Test UUID v5 generation (SHA-1 namespace-based)."""
    # Test with namespace object
    u1 = UUIDUtils.generate_v5(UUIDUtils.NAMESPACE_DNS, 'example.com')
    assert isinstance(u1, uuid.UUID)
    assert u1.version == 5
    
    # Test determinism
    u2 = UUIDUtils.generate_v5(UUIDUtils.NAMESPACE_DNS, 'example.com')
    assert u1 == u2
    
    # v3 and v5 produce different UUIDs for same input
    u3 = UUIDUtils.generate_v3(UUIDUtils.NAMESPACE_DNS, 'example.com')
    assert u1 != u3
    
    print("✓ test_generate_v5 passed")


def test_parse():
    """Test UUID parsing from various formats."""
    # Standard format
    u1 = UUIDUtils.parse('123e4567-e89b-12d3-a456-426614174000')
    assert str(u1) == '123e4567-e89b-12d3-a456-426614174000'
    
    # Braced format
    u2 = UUIDUtils.parse('{123e4567-e89b-12d3-a456-426614174000}')
    assert str(u2) == '123e4567-e89b-12d3-a456-426614174000'
    
    # URN format
    u3 = UUIDUtils.parse('urn:uuid:123e4567-e89b-12d3-a456-426614174000')
    assert str(u3) == '123e4567-e89b-12d3-a456-426614174000'
    
    # No hyphens
    u4 = UUIDUtils.parse('123e4567e89b12d3a456426614174000')
    assert str(u4) == '123e4567-e89b-12d3-a456-426614174000'
    
    # Uppercase
    u5 = UUIDUtils.parse('123E4567-E89B-12D3-A456-426614174000')
    assert str(u5) == '123e4567-e89b-12d3-a456-426614174000'
    
    print("✓ test_parse passed")


def test_is_valid():
    """Test UUID validation."""
    # Valid UUIDs
    assert UUIDUtils.is_valid('123e4567-e89b-12d3-a456-426614174000')
    assert UUIDUtils.is_valid('{123e4567-e89b-12d3-a456-426614174000}')
    assert UUIDUtils.is_valid('urn:uuid:123e4567-e89b-12d3-a456-426614174000')
    assert UUIDUtils.is_valid('123e4567e89b12d3a456426614174000')
    assert UUIDUtils.is_valid('00000000-0000-0000-0000-000000000000')
    assert UUIDUtils.is_valid('ffffffff-ffff-ffff-ffff-ffffffffffff')
    
    # Invalid UUIDs
    assert not UUIDUtils.is_valid('not-a-uuid')
    assert not UUIDUtils.is_valid('')
    assert not UUIDUtils.is_valid('123e4567-e89b-12d3-a456-42661417400')  # Too short
    assert not UUIDUtils.is_valid('123e4567-e89b-12d3-a456-4266141740000')  # Too long
    assert not UUIDUtils.is_valid('123e4567-e89b-12d3-a456-42661417400g')  # Invalid char
    assert not UUIDUtils.is_valid(None)
    
    print("✓ test_is_valid passed")


def test_is_valid_fast():
    """Test fast UUID validation using regex."""
    # Valid UUIDs
    assert UUIDUtils.is_valid_fast('123e4567-e89b-12d3-a456-426614174000')
    assert UUIDUtils.is_valid_fast('{123e4567-e89b-12d3-a456-426614174000}')
    assert UUIDUtils.is_valid_fast('urn:uuid:123e4567-e89b-12d3-a456-426614174000')
    assert UUIDUtils.is_valid_fast('123e4567e89b12d3a456426614174000')
    
    # Invalid UUIDs
    assert not UUIDUtils.is_valid_fast('not-a-uuid')
    assert not UUIDUtils.is_valid_fast('')
    assert not UUIDUtils.is_valid_fast('123e4567-e89b-12d3-a456-42661417400g')
    assert not UUIDUtils.is_valid_fast(None)
    
    print("✓ test_is_valid_fast passed")


def test_get_version():
    """Test UUID version detection."""
    u1 = UUIDUtils.generate_v1()
    assert UUIDUtils.get_version(u1) == 1
    
    u3 = UUIDUtils.generate_v3(UUIDUtils.NAMESPACE_DNS, 'test')
    assert UUIDUtils.get_version(u3) == 3
    
    u4 = UUIDUtils.generate_v4()
    assert UUIDUtils.get_version(u4) == 4
    
    u5 = UUIDUtils.generate_v5(UUIDUtils.NAMESPACE_DNS, 'test')
    assert UUIDUtils.get_version(u5) == 5
    
    # Test with string input
    assert UUIDUtils.get_version('123e4567-e89b-12d3-a456-426614174000') == 1
    
    print("✓ test_get_version passed")


def test_get_variant():
    """Test UUID variant detection."""
    u = UUIDUtils.generate_v4()
    variant = UUIDUtils.get_variant(u)
    assert variant == 'RFC 4122'
    
    print("✓ test_get_variant passed")


def test_to_string():
    """Test UUID string conversion formats."""
    u = uuid.UUID('123e4567-e89b-12d3-a456-426614174000')
    
    assert UUIDUtils.to_string(u, 'standard') == '123e4567-e89b-12d3-a456-426614174000'
    assert UUIDUtils.to_string(u, 'braced') == '{123e4567-e89b-12d3-a456-426614174000}'
    assert UUIDUtils.to_string(u, 'urn') == 'urn:uuid:123e4567-e89b-12d3-a456-426614174000'
    assert UUIDUtils.to_string(u, 'no-hyphen') == '123e4567e89b12d3a456426614174000'
    assert UUIDUtils.to_string(u, 'upper') == '123E4567-E89B-12D3-A456-426614174000'
    
    # Test invalid format
    try:
        UUIDUtils.to_string(u, 'invalid')
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
    
    print("✓ test_to_string passed")


def test_to_bytes_and_from_bytes():
    """Test UUID bytes conversion."""
    u = uuid.UUID('123e4567-e89b-12d3-a456-426614174000')
    
    # Convert to bytes
    b = UUIDUtils.to_bytes(u)
    assert len(b) == 16
    
    # Convert back
    u2 = UUIDUtils.from_bytes(b)
    assert u == u2
    
    print("✓ test_to_bytes_and_from_bytes passed")


def test_to_int_and_from_int():
    """Test UUID integer conversion."""
    u = uuid.UUID('123e4567-e89b-12d3-a456-426614174000')
    
    # Convert to int
    i = UUIDUtils.to_int(u)
    assert isinstance(i, int)
    assert i > 0
    
    # Convert back
    u2 = UUIDUtils.from_int(i)
    assert u == u2
    
    # Test nil UUID
    nil_uuid = UUIDUtils.nil()
    assert UUIDUtils.to_int(nil_uuid) == 0
    assert UUIDUtils.from_int(0) == nil_uuid
    
    print("✓ test_to_int_and_from_int passed")


def test_compare():
    """Test UUID comparison."""
    u1 = uuid.UUID('123e4567-e89b-12d3-a456-426614174000')
    u2 = uuid.UUID('123e4567-e89b-12d3-a456-426614174001')
    u3 = uuid.UUID('123e4567-e89b-12d3-a456-426614174000')
    
    assert UUIDUtils.compare(u1, u2) == -1
    assert UUIDUtils.compare(u2, u1) == 1
    assert UUIDUtils.compare(u1, u3) == 0
    
    # Test with string inputs
    assert UUIDUtils.compare(u1, '123e4567-e89b-12d3-a456-426614174001') == -1
    
    print("✓ test_compare passed")


def test_equal():
    """Test UUID equality check."""
    u1 = uuid.UUID('123e4567-e89b-12d3-a456-426614174000')
    
    assert UUIDUtils.equal(u1, '123e4567-e89b-12d3-a456-426614174000')
    assert UUIDUtils.equal(u1, u1)
    assert not UUIDUtils.equal(u1, '123e4567-e89b-12d3-a456-426614174001')
    
    # Test case insensitivity
    assert UUIDUtils.equal(u1, '123E4567-E89B-12D3-A456-426614174000')
    
    print("✓ test_equal passed")


def test_sort():
    """Test UUID sorting."""
    uuids = [
        '123e4567-e89b-12d3-a456-426614174002',
        '123e4567-e89b-12d3-a456-426614174000',
        '123e4567-e89b-12d3-a456-426614174001',
    ]
    
    sorted_uuids = UUIDUtils.sort(uuids)
    assert str(sorted_uuids[0]) == '123e4567-e89b-12d3-a456-426614174000'
    assert str(sorted_uuids[1]) == '123e4567-e89b-12d3-a456-426614174001'
    assert str(sorted_uuids[2]) == '123e4567-e89b-12d3-a456-426614174002'
    
    # Test reverse sort
    sorted_reverse = UUIDUtils.sort(uuids, reverse=True)
    assert str(sorted_reverse[0]) == '123e4567-e89b-12d3-a456-426614174002'
    
    print("✓ test_sort passed")


def test_get_timestamp():
    """Test timestamp extraction from UUID v1."""
    u = UUIDUtils.generate_v1()
    ts = UUIDUtils.get_timestamp(u)
    
    assert ts is not None
    assert isinstance(ts, datetime)
    
    # Test with v4 UUID (should return None)
    u4 = UUIDUtils.generate_v4()
    assert UUIDUtils.get_timestamp(u4) is None
    
    # Test with string input
    ts2 = UUIDUtils.get_timestamp(str(u))
    assert ts2 is not None
    
    print("✓ test_get_timestamp passed")


def test_get_node():
    """Test node extraction from UUID v1."""
    u = UUIDUtils.generate_v1()
    node = UUIDUtils.get_node(u)
    
    assert node is not None
    assert isinstance(node, int)
    assert node >= 0
    
    # Test with v4 UUID (should return None)
    u4 = UUIDUtils.generate_v4()
    assert UUIDUtils.get_node(u4) is None
    
    print("✓ test_get_node passed")


def test_generate_batch():
    """Test batch UUID generation."""
    # Generate batch of v4 UUIDs
    uuids_v4 = UUIDUtils.generate_batch(10, version=4)
    assert len(uuids_v4) == 10
    assert all(u.version == 4 for u in uuids_v4)
    # All should be unique
    assert len(set(uuids_v4)) == 10
    
    # Generate batch of v1 UUIDs
    uuids_v1 = UUIDUtils.generate_batch(5, version=1)
    assert len(uuids_v1) == 5
    assert all(u.version == 1 for u in uuids_v1)
    
    # Test invalid version
    try:
        UUIDUtils.generate_batch(5, version=3)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
    
    try:
        UUIDUtils.generate_batch(5, version=99)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
    
    print("✓ test_generate_batch passed")


def test_nil():
    """Test nil UUID."""
    nil_uuid = UUIDUtils.nil()
    assert str(nil_uuid) == '00000000-0000-0000-0000-000000000000'
    assert nil_uuid.int == 0
    
    assert UUIDUtils.is_nil(nil_uuid)
    assert UUIDUtils.is_nil('00000000-0000-0000-0000-000000000000')
    assert not UUIDUtils.is_nil(UUIDUtils.generate_v4())
    
    print("✓ test_nil passed")


def test_hash_to_uuid():
    """Test hash-based UUID generation."""
    # Test determinism
    u1 = UUIDUtils.hash_to_uuid('my-custom-seed')
    u2 = UUIDUtils.hash_to_uuid('my-custom-seed')
    assert u1 == u2
    
    # Different inputs produce different UUIDs
    u3 = UUIDUtils.hash_to_uuid('different-seed')
    assert u1 != u3
    
    # Test different algorithms
    u_md5 = UUIDUtils.hash_to_uuid('test', 'md5')
    u_sha1 = UUIDUtils.hash_to_uuid('test', 'sha1')
    u_sha256 = UUIDUtils.hash_to_uuid('test', 'sha256')
    u_sha512 = UUIDUtils.hash_to_uuid('test', 'sha512')
    
    assert u_md5 != u_sha1
    assert u_sha1 != u_sha256
    assert u_sha256 != u_sha512
    
    # All should be valid UUIDs
    assert all(u.version == 5 for u in [u_md5, u_sha1, u_sha256, u_sha512])
    
    # Test with bytes input
    u_bytes = UUIDUtils.hash_to_uuid(b'test-bytes')
    assert isinstance(u_bytes, uuid.UUID)
    
    # Test invalid algorithm
    try:
        UUIDUtils.hash_to_uuid('test', 'invalid')
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
    
    print("✓ test_hash_to_uuid passed")


def test_convenience_functions():
    """Test convenience functions for direct import."""
    # Test generation functions
    u1 = generate_v1()
    assert u1.version == 1
    
    u3 = generate_v3('dns', 'test.com')
    assert u3.version == 3
    
    u4 = generate_v4()
    assert u4.version == 4
    
    u5 = generate_v5('dns', 'test.com')
    assert u5.version == 5
    
    # Test parse and validation
    assert is_valid('123e4567-e89b-12d3-a456-426614174000')
    assert not is_valid('invalid')
    
    # Test nil
    assert is_nil(nil())
    
    print("✓ test_convenience_functions passed")


def test_namespace_constants():
    """Test predefined namespace constants."""
    assert str(UUIDUtils.NAMESPACE_DNS) == '6ba7b810-9dad-11d1-80b4-00c04fd430c8'
    assert str(UUIDUtils.NAMESPACE_URL) == '6ba7b811-9dad-11d1-80b4-00c04fd430c8'
    assert str(UUIDUtils.NAMESPACE_OID) == '6ba7b812-9dad-11d1-80b4-00c04fd430c8'
    assert str(UUIDUtils.NAMESPACE_X500) == '6ba7b814-9dad-11d1-80b4-00c04fd430c8'
    
    print("✓ test_namespace_constants passed")


def test_edge_cases():
    """Test edge cases and boundary conditions."""
    # Empty string validation
    assert not UUIDUtils.is_valid('')
    assert not UUIDUtils.is_valid_fast('')
    
    # None handling
    assert not UUIDUtils.is_valid(None)
    assert not UUIDUtils.is_valid_fast(None)
    
    # Maximum UUID
    max_uuid = uuid.UUID('ffffffff-ffff-ffff-ffff-ffffffffffff')
    assert UUIDUtils.is_valid(str(max_uuid))
    
    # Mixed case
    mixed_case = '123E4567-E89b-12D3-a456-426614174000'
    assert UUIDUtils.is_valid(mixed_case)
    
    print("✓ test_edge_cases passed")


def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("AllToolkit - UUID Utilities Test Suite")
    print("=" * 60)
    print()
    
    test_generate_v1()
    test_generate_v3()
    test_generate_v4()
    test_generate_v5()
    test_parse()
    test_is_valid()
    test_is_valid_fast()
    test_get_version()
    test_get_variant()
    test_to_string()
    test_to_bytes_and_from_bytes()
    test_to_int_and_from_int()
    test_compare()
    test_equal()
    test_sort()
    test_get_timestamp()
    test_get_node()
    test_generate_batch()
    test_nil()
    test_hash_to_uuid()
    test_convenience_functions()
    test_namespace_constants()
    test_edge_cases()
    
    print()
    print("=" * 60)
    print("All tests passed! ✓")
    print("=" * 60)


if __name__ == '__main__':
    run_all_tests()
