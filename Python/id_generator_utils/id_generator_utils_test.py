#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AllToolkit - ID Generator Utilities Tests

Comprehensive tests for all ID generation functions.
"""

import time
import threading
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    SnowflakeGenerator,
    ULID,
    NanoID,
    ObjectId,
    short_id,
    timestamp_id,
    sequential_id,
    prefixed_uuid,
    ksuid,
    cuid2,
    tsid,
    analyze_id,
    uuid4_str,
    uuid4_hex,
    uuid7_str,
)


def test_snowflake_generator():
    """Test Snowflake ID generator."""
    print("Testing SnowflakeGenerator...")
    
    # Test basic generation
    gen = SnowflakeGenerator(worker_id=1, datacenter_id=1)
    id1 = gen.generate()
    id2 = gen.generate()
    
    assert isinstance(id1, int), "ID should be integer"
    assert id2 > id1, "IDs should be monotonically increasing"
    
    # Test ID parsing
    parsed = SnowflakeGenerator.parse(id1)
    assert 'timestamp' in parsed
    assert 'worker_id' in parsed
    assert 'datacenter_id' in parsed
    assert 'sequence' in parsed
    assert parsed['worker_id'] == 1
    assert parsed['datacenter_id'] == 1
    
    # Test batch generation
    ids = gen.generate_batch(100)
    assert len(ids) == 100
    assert len(set(ids)) == 100, "All IDs should be unique"
    
    # Test ordering
    for i in range(len(ids) - 1):
        assert ids[i] < ids[i + 1], "IDs should be ordered"
    
    # Test invalid worker_id
    try:
        SnowflakeGenerator(worker_id=100)
        assert False, "Should raise ValueError"
    except ValueError:
        pass
    
    print("✓ SnowflakeGenerator tests passed")


def test_ulid():
    """Test ULID generator."""
    print("Testing ULID...")
    
    # Test basic generation
    ulid1 = ULID.generate()
    ulid2 = ULID.generate()
    
    assert len(ulid1) == 26, "ULID should be 26 characters"
    assert len(ulid2) == 26, "ULID should be 26 characters"
    
    # Test characters are valid
    valid_chars = set('0123456789ABCDEFGHJKMNPQRSTVWXYZ')
    assert all(c in valid_chars for c in ulid1.upper()), "ULID should use valid characters"
    
    # Test timestamp extraction
    ts = ULID.get_timestamp(ulid1)
    now = time.time()
    assert abs(ts.timestamp() - now) < 1, "Timestamp should be close to now"
    
    # Test ordering
    time.sleep(0.001)  # Small delay
    ulid3 = ULID.generate()
    assert ulid3 > ulid1, "ULIDs should be sortable"
    
    # Test comparison
    assert ULID.compare(ulid1, ulid1) == 0
    assert ULID.compare(ulid1, ulid3) == -1
    assert ULID.compare(ulid3, ulid1) == 1
    
    print("✓ ULID tests passed")


def test_nanoid():
    """Test NanoID generator."""
    print("Testing NanoID...")
    
    # Test basic generation
    id1 = NanoID.generate()
    assert len(id1) == 21, "Default NanoID should be 21 characters"
    
    # Test custom length
    id2 = NanoID.generate(length=10)
    assert len(id2) == 10, "Custom length should work"
    
    # Test custom alphabet
    numeric_id = NanoID.generate(alphabet='0123456789')
    assert numeric_id.isdigit(), "Numeric alphabet should produce numeric ID"
    
    # Test numeric method
    num_id = NanoID.numeric(16)
    assert len(num_id) == 16
    assert num_id.isdigit()
    
    # Test lowercase method
    lower_id = NanoID.lowercase(12)
    assert len(lower_id) == 12
    assert lower_id.islower() or lower_id.isdigit()
    
    # Test no_lookalikes method
    safe_id = NanoID.no_lookalikes(20)
    assert len(safe_id) == 20
    lookalikes = set('l1IO0')
    assert not any(c in lookalikes for c in safe_id), "Should not contain lookalikes"
    
    # Test url_safe method
    url_id = NanoID.url_safe(15)
    assert len(url_id) == 15
    
    # Test uniqueness
    ids = set(NanoID.generate() for _ in range(1000))
    assert len(ids) == 1000, "All IDs should be unique"
    
    print("✓ NanoID tests passed")


def test_objectid():
    """Test ObjectId generator."""
    print("Testing ObjectId...")
    
    # Test basic generation
    oid1 = ObjectId.generate()
    oid2 = ObjectId.generate()
    
    assert len(oid1) == 24, "ObjectId should be 24 characters"
    assert ObjectId.is_valid(oid1), "Generated ID should be valid"
    
    # Test uniqueness
    ids = set(ObjectId.generate() for _ in range(1000))
    assert len(ids) == 1000, "All ObjectIds should be unique"
    
    # Test timestamp extraction
    ts = ObjectId.get_timestamp(oid1)
    now = time.time()
    assert abs(ts.timestamp() - now) < 2, "Timestamp should be close to now"
    
    # Test validation
    assert ObjectId.is_valid('507f1f77bcf86cd799439011')
    assert not ObjectId.is_valid('invalid')
    assert not ObjectId.is_valid('507f1f77bcf86cd79943901')  # Too short
    
    print("✓ ObjectId tests passed")


def test_short_id():
    """Test short_id function."""
    print("Testing short_id...")
    
    id1 = short_id(8)
    assert len(id1) == 8
    
    id2 = short_id(16)
    assert len(id2) == 16
    
    # Test custom alphabet
    hex_id = short_id(12, alphabet='0123456789abcdef')
    assert len(hex_id) == 12
    
    print("✓ short_id tests passed")


def test_timestamp_id():
    """Test timestamp_id function."""
    print("Testing timestamp_id...")
    
    id1 = timestamp_id()
    assert len(id1) > 14  # At least timestamp + random
    
    id2 = timestamp_id(prefix='ORD')
    assert id2.startswith('ORD')
    
    id3 = timestamp_id(prefix='USER', suffix='_END')
    assert id3.startswith('USER')
    assert id3.endswith('_END')
    
    print("✓ timestamp_id tests passed")


def test_sequential_id():
    """Test sequential_id function."""
    print("Testing sequential_id...")
    
    gen = sequential_id('ITEM', padding=6)
    
    id1 = gen()
    id2 = gen()
    id3 = gen()
    
    assert id1 == 'ITEM000001'
    assert id2 == 'ITEM000002'
    assert id3 == 'ITEM000003'
    
    # Test without padding
    gen2 = sequential_id('ID')
    assert gen2() == 'ID1'
    assert gen2() == 'ID2'
    
    print("✓ sequential_id tests passed")


def test_prefixed_uuid():
    """Test prefixed_uuid function."""
    print("Testing prefixed_uuid...")
    
    id1 = prefixed_uuid('USER')
    assert id1.startswith('USER_')
    assert len(id1) == 41  # USER_ + UUID
    
    id2 = prefixed_uuid('ORDER', separator=':')
    assert id2.startswith('ORDER:')
    
    print("✓ prefixed_uuid tests passed")


def test_ksuid():
    """Test ksuid function."""
    print("Testing ksuid...")
    
    id1 = ksuid()
    assert isinstance(id1, str)
    assert len(id1) > 20
    
    # Test uniqueness
    ids = set(ksuid() for _ in range(100))
    assert len(ids) == 100, "All KSUIDs should be unique"
    
    print("✓ ksuid tests passed")


def test_cuid2():
    """Test cuid2 function."""
    print("Testing cuid2...")
    
    id1 = cuid2()
    assert isinstance(id1, str)
    assert len(id1) == 24
    
    id2 = cuid2(length=32)
    assert len(id2) == 32
    
    # Test uniqueness
    ids = set(cuid2() for _ in range(1000))
    assert len(ids) == 1000, "All CUID2s should be unique"
    
    print("✓ cuid2 tests passed")


def test_tsid():
    """Test tsid function."""
    print("Testing tsid...")
    
    id1 = tsid('ORD')
    assert id1.startswith('ORD')
    
    id2 = tsid()
    assert isinstance(id2, str)
    
    # Test uniqueness
    ids = set(tsid() for _ in range(100))
    assert len(ids) == 100, "All TSIDs should be unique"
    
    print("✓ tsid tests passed")


def test_analyze_id():
    """Test analyze_id function."""
    print("Testing analyze_id...")
    
    # Test ObjectId analysis
    oid = ObjectId.generate()
    result = analyze_id(oid)
    assert result['type'] == 'objectid'
    
    # Test ULID analysis
    ulid = ULID.generate()
    result = analyze_id(ulid)
    assert result['type'] == 'ulid'
    
    # Test numeric analysis
    result = analyze_id('12345678')
    assert result['type'] == 'numeric'
    
    # Test prefixed analysis
    result = analyze_id('USER_abc123')
    assert result['type'] == 'prefixed'
    assert result['properties']['prefix'] == 'USER'
    
    print("✓ analyze_id tests passed")


def test_uuid_functions():
    """Test UUID functions."""
    print("Testing UUID functions...")
    
    # Test uuid4_str
    id1 = uuid4_str()
    assert len(id1) == 36
    assert '-' in id1
    
    # Test uuid4_hex
    id2 = uuid4_hex()
    assert len(id2) == 32
    assert '-' not in id2
    
    # Test uuid7_str
    id3 = uuid7_str()
    assert len(id3) == 36
    assert '-' in id3
    
    # Test uniqueness
    ids = set(uuid4_str() for _ in range(100))
    assert len(ids) == 100
    
    print("✓ UUID functions tests passed")


def test_thread_safety():
    """Test thread safety of generators."""
    print("Testing thread safety...")
    
    # Test SnowflakeGenerator thread safety
    gen = SnowflakeGenerator(worker_id=1)
    ids = []
    
    def generate_ids():
        for _ in range(100):
            ids.append(gen.generate())
    
    threads = [threading.Thread(target=generate_ids) for _ in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    
    assert len(ids) == 1000, "Should generate 1000 IDs"
    assert len(set(ids)) == 1000, "All IDs should be unique"
    
    # Test ULID thread safety
    ulids = []
    
    def generate_ulids():
        for _ in range(100):
            ulids.append(ULID.generate())
    
    threads = [threading.Thread(target=generate_ulids) for _ in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    
    assert len(set(ulids)) == 1000, "All ULIDs should be unique"
    
    # Test ObjectId thread safety
    oids = []
    
    def generate_oids():
        for _ in range(100):
            oids.append(ObjectId.generate())
    
    threads = [threading.Thread(target=generate_oids) for _ in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    
    assert len(set(oids)) == 1000, "All ObjectIds should be unique"
    
    print("✓ Thread safety tests passed")


def test_performance():
    """Test generation performance."""
    print("Testing performance...")
    
    # SnowflakeGenerator performance
    gen = SnowflakeGenerator(worker_id=1)
    start = time.time()
    for _ in range(10000):
        gen.generate()
    elapsed = time.time() - start
    print(f"  SnowflakeGenerator: 10000 IDs in {elapsed:.3f}s ({10000/elapsed:.0f} IDs/s)")
    
    # ULID performance
    start = time.time()
    for _ in range(10000):
        ULID.generate()
    elapsed = time.time() - start
    print(f"  ULID: 10000 IDs in {elapsed:.3f}s ({10000/elapsed:.0f} IDs/s)")
    
    # NanoID performance
    start = time.time()
    for _ in range(10000):
        NanoID.generate()
    elapsed = time.time() - start
    print(f"  NanoID: 10000 IDs in {elapsed:.3f}s ({10000/elapsed:.0f} IDs/s)")
    
    # ObjectId performance
    start = time.time()
    for _ in range(10000):
        ObjectId.generate()
    elapsed = time.time() - start
    print(f"  ObjectId: 10000 IDs in {elapsed:.3f}s ({10000/elapsed:.0f} IDs/s)")
    
    print("✓ Performance tests passed")


def main():
    """Run all tests."""
    print("=" * 60)
    print("ID Generator Utilities - Comprehensive Test Suite")
    print("=" * 60)
    print()
    
    test_snowflake_generator()
    test_ulid()
    test_nanoid()
    test_objectid()
    test_short_id()
    test_timestamp_id()
    test_sequential_id()
    test_prefixed_uuid()
    test_ksuid()
    test_cuid2()
    test_tsid()
    test_analyze_id()
    test_uuid_functions()
    test_thread_safety()
    test_performance()
    
    print()
    print("=" * 60)
    print("✓ All tests passed!")
    print("=" * 60)


if __name__ == '__main__':
    main()