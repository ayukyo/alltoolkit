#!/usr/bin/env python3
"""
ULID Utils - Usage Examples

This file demonstrates various use cases for the ULID utilities.

ULID (Universally Unique Lexicographically Sortable Identifier) is:
- 128 bits total (26 characters in Base32)
- 48 bits timestamp (milliseconds since Unix epoch)
- 80 bits randomness
- Lexicographically sortable
- URL-safe
- Case-insensitive
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime, timezone, timedelta
import uuid

# Import the module
from mod import (
    ULID, ULIDError, generate, parse, is_valid, monotonic,
    from_datetime, from_uuid, from_hex, from_int,
    generate_batch, generate_monotonic_batch, compare, min_ulid, max_ulid,
    extract_timestamps
)


def example_basic_generation():
    """Example 1: Basic ULID generation"""
    print("=" * 60)
    print("Example 1: Basic ULID Generation")
    print("=" * 60)
    
    # Generate a new ULID
    ulid = ULID.generate()
    print(f"Generated ULID: {ulid}")
    print(f"String representation: {str(ulid)}")
    print(f"Length: {len(str(ulid))} characters")
    print()
    
    # Module-level shortcut
    ulid2 = generate()
    print(f"Using shortcut: {ulid2}")
    print()


def example_timestamp_extraction():
    """Example 2: Extract timestamp information"""
    print("=" * 60)
    print("Example 2: Timestamp Extraction")
    print("=" * 60)
    
    ulid = ULID.generate()
    print(f"ULID: {ulid}")
    print(f"Timestamp (ms): {ulid.timestamp_ms()}")
    print(f"Timestamp (s): {ulid.timestamp()}")
    print(f"Datetime (UTC): {ulid.datetime()}")
    print(f"Datetime (ISO): {ulid.datetime().isoformat()}")
    print()
    
    # Randomness component
    print(f"Randomness (hex): {ulid.randomness().hex()}")
    print(f"Randomness (bytes): {list(ulid.randomness())}")
    print()


def example_parsing_and_validation():
    """Example 3: Parse and validate ULIDs"""
    print("=" * 60)
    print("Example 3: Parsing and Validation")
    print("=" * 60)
    
    # Parse from string
    ulid_str = '01ARZ3NDEKTSV4RRFFQ69G5FAV'
    ulid = ULID.parse(ulid_str)
    print(f"Parsed ULID: {ulid}")
    print(f"Timestamp: {ulid.datetime()}")
    print()
    
    # Validation
    print(f"Is valid: {is_valid('01ARZ3NDEKTSV4RRFFQ69G5FAV')}")
    print(f"Is valid (invalid): {is_valid('INVALID_ULID!!!')}")
    print(f"Is valid (wrong length): {is_valid('01ARZ3')}")
    print()
    
    # Case-insensitive
    lower = ulid_str.lower()
    parsed = parse(lower)
    print(f"Lowercase input: {lower}")
    print(f"Parsed result: {parsed}")
    print()


def example_datetime_creation():
    """Example 4: Create ULID from datetime"""
    print("=" * 60)
    print("Example 4: Create ULID from Datetime")
    print("=" * 60)
    
    # Specific datetime
    dt = datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    ulid = ULID.from_datetime(dt)
    print(f"Input datetime: {dt}")
    print(f"Generated ULID: {ulid}")
    print(f"Extracted datetime: {ulid.datetime()}")
    print()
    
    # Current time with specific timezone
    now_utc = datetime.now(timezone.utc)
    ulid_now = from_datetime(now_utc)
    print(f"Current UTC: {now_utc}")
    print(f"ULID: {ulid_now}")
    print()


def example_type_conversions():
    """Example 5: Type conversions"""
    print("=" * 60)
    print("Example 5: Type Conversions")
    print("=" * 60)
    
    ulid = ULID.generate()
    print(f"ULID: {ulid}")
    print()
    
    # To various formats
    print(f"Hex: {ulid.hex()}")
    print(f"Int: {ulid.to_int()}")
    print(f"Bytes: {ulid.bytes().hex()}")
    print(f"UUID: {ulid.to_uuid()}")
    print()
    
    # From various formats
    hex_ulid = from_hex('01706d60a1e24840890c2759b22a3f68')
    print(f"From hex: {hex_ulid}")
    
    int_ulid = from_int(123456789012345678901234567890)
    print(f"From int: {int_ulid}")
    
    uuid_obj = uuid.uuid4()
    uuid_ulid = from_uuid(uuid_obj)
    print(f"From UUID: {uuid_ulid}")
    print()


def example_comparison():
    """Example 6: Compare ULIDs"""
    print("=" * 60)
    print("Example 6: ULID Comparison")
    print("=" * 60)
    
    # Generate two ULIDs with a small delay
    ulid1 = ULID.generate()
    import time
    time.sleep(0.002)  # 2ms delay
    ulid2 = ULID.generate()
    
    print(f"ULID 1: {ulid1}")
    print(f"ULID 2: {ulid2}")
    print()
    
    # Comparison
    print(f"ulid1 < ulid2: {ulid1 < ulid2}")
    print(f"ulid1 == ulid2: {ulid1 == ulid2}")
    print(f"ulid1 > ulid2: {ulid1 > ulid2}")
    print()
    
    # Compare function
    print(f"compare(ulid1, ulid2): {compare(ulid1, ulid2)}")
    print(f"compare(ulid2, ulid1): {compare(ulid2, ulid1)}")
    print(f"compare(ulid1, ulid1): {compare(ulid1, ulid1)}")
    print()
    
    # Sorting
    ulids = [ulid2, ulid1]
    sorted_ulids = sorted(ulids)
    print(f"Sorted ULIDs: {[str(u)[:13] + '...' for u in sorted_ulids]}")
    print()


def example_monotonic():
    """Example 7: Monotonic ULID generation"""
    print("=" * 60)
    print("Example 7: Monotonic ULID Generation")
    print("=" * 60)
    
    print("Generating 5 monotonic ULIDs (guaranteed to be sorted):")
    last = None
    for i in range(5):
        current = ULID.monotonic(last)
        print(f"  {i+1}. {current}")
        if last:
            print(f"     > previous: {current > last}")
        last = current
    print()
    
    # Using batch function
    print("Batch monotonic generation:")
    batch = generate_monotonic_batch(5)
    for i, u in enumerate(batch):
        print(f"  {i+1}. {u}")
    print()


def example_batch_operations():
    """Example 8: Batch operations"""
    print("=" * 60)
    print("Example 8: Batch Operations")
    print("=" * 60)
    
    # Generate batch
    ulids = generate_batch(5)
    print(f"Generated {len(ulids)} ULIDs:")
    for u in ulids:
        print(f"  {u}")
    print()
    
    # Find min/max
    print(f"Min ULID: {min_ulid(ulids)}")
    print(f"Max ULID: {max_ulid(ulids)}")
    print()
    
    # Extract timestamps
    print("Timestamps extracted:")
    for u, ts in extract_timestamps(ulids):
        print(f"  {u[:13]}... -> {ts} ms")
    print()


def example_database_use_case():
    """Example 9: Database use case simulation"""
    print("=" * 60)
    print("Example 9: Database Use Case Simulation")
    print("=" * 60)
    
    # Simulate database records with ULID as primary key
    records = []
    
    print("Inserting records with ULID primary keys:")
    for i in range(3):
        record = {
            'id': str(ULID.generate()),
            'data': f'Record {i+1}',
            'created_at': datetime.now(timezone.utc)
        }
        records.append(record)
        print(f"  Inserted: {record['id'][:13]}... -> {record['data']}")
    
    print()
    print("Records sorted by ID (automatically sorted by creation time):")
    for r in sorted(records, key=lambda x: x['id']):
        print(f"  {r['id']} -> {r['data']}")
    print()


def example_sorting_by_time():
    """Example 10: Sorting ULIDs by time"""
    print("=" * 60)
    print("Example 10: Sorting ULIDs by Time")
    print("=" * 60)
    
    # Create ULIDs from different dates
    dates = [
        datetime(2024, 1, 1, tzinfo=timezone.utc),
        datetime(2024, 6, 15, tzinfo=timezone.utc),
        datetime(2023, 12, 31, tzinfo=timezone.utc),
        datetime(2024, 3, 1, tzinfo=timezone.utc),
    ]
    
    ulids = [from_datetime(d) for d in dates]
    
    print("ULIDs (unsorted):")
    for u, d in zip(ulids, dates):
        print(f"  {u} -> {d.date()}")
    print()
    
    # Sort ULIDs (they sort lexicographically == chronologically)
    sorted_ulids = sorted(ulids)
    
    print("ULIDs (sorted lexicographically):")
    for u in sorted_ulids:
        print(f"  {u} -> {u.datetime().date()}")
    print()


def example_url_safe():
    """Example 11: URL-safe identifiers"""
    print("=" * 60)
    print("Example 11: URL-Safe Identifiers")
    print("=" * 60)
    
    # ULIDs are URL-safe (no special characters)
    ulid = ULID.generate()
    print(f"ULID: {ulid}")
    
    # Can be safely used in URLs
    url = f"https://example.com/resource/{ulid}"
    print(f"URL: {url}")
    
    # No encoding needed
    import urllib.parse
    encoded = urllib.parse.quote(str(ulid))
    print(f"URL encoded: {encoded}")
    print(f"Same as original: {encoded == str(ulid)}")
    print()


def example_copy_and_hash():
    """Example 12: Copy and hash"""
    print("=" * 60)
    print("Example 12: Copy and Hash")
    print("=" * 60)
    
    original = ULID.generate()
    print(f"Original: {original}")
    
    # Copy by passing to constructor
    copy = ULID(original)
    print(f"Copy: {copy}")
    print(f"Equal: {original == copy}")
    print()
    
    # Hash for use in dicts/sets
    print(f"Hash of original: {hash(original)}")
    print(f"Hash of copy: {hash(copy)}")
    print(f"Same hash: {hash(original) == hash(copy)}")
    
    # Use in set
    ulid_set = {original, copy}
    print(f"Set size (should be 1): {len(ulid_set)}")
    print()


if __name__ == '__main__':
    print("\n" + "#" * 60)
    print("# ULID Utils - Complete Usage Examples")
    print("#" * 60 + "\n")
    
    example_basic_generation()
    example_timestamp_extraction()
    example_parsing_and_validation()
    example_datetime_creation()
    example_type_conversions()
    example_comparison()
    example_monotonic()
    example_batch_operations()
    example_database_use_case()
    example_sorting_by_time()
    example_url_safe()
    example_copy_and_hash()
    
    print("#" * 60)
    print("# All examples completed!")
    print("#" * 60)