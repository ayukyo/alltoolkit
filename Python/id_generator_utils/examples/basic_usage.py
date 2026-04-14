#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ID Generator Utilities - Basic Usage Examples

This example demonstrates the basic usage of all ID generators.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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


def main():
    print("=" * 60)
    print("ID Generator Utilities - Examples")
    print("=" * 60)
    print()
    
    # Snowflake ID
    print("1. Snowflake ID Generator")
    print("-" * 40)
    gen = SnowflakeGenerator(worker_id=1, datacenter_id=1)
    
    print("Generating 5 Snowflake IDs:")
    for i in range(5):
        snowflake_id = gen.generate()
        parsed = SnowflakeGenerator.parse(snowflake_id)
        print(f"  ID: {snowflake_id}")
        print(f"    Time: {parsed['datetime']}")
        print(f"    Worker: {parsed['worker_id']}, DC: {parsed['datacenter_id']}, Seq: {parsed['sequence']}")
    print()
    
    # ULID
    print("2. ULID Generator")
    print("-" * 40)
    print("Generating 5 ULIDs:")
    for i in range(5):
        ulid = ULID.generate()
        ts = ULID.get_timestamp(ulid)
        print(f"  {ulid} (time: {ts.isoformat()})")
    print()
    
    # NanoID
    print("3. NanoID Generator")
    print("-" * 40)
    print(f"  Default (21 chars):     {NanoID.generate()}")
    print(f"  Custom length (10):     {NanoID.generate(length=10)}")
    print(f"  Numeric (16):           {NanoID.numeric(16)}")
    print(f"  Lowercase (12):         {NanoID.lowercase(12)}")
    print(f"  No lookalikes (20):     {NanoID.no_lookalikes(20)}")
    print(f"  URL-safe (15):          {NanoID.url_safe(15)}")
    print()
    
    # ObjectId
    print("4. ObjectId Generator (MongoDB-style)")
    print("-" * 40)
    print("Generating 3 ObjectIds:")
    for i in range(3):
        oid = ObjectId.generate()
        ts = ObjectId.get_timestamp(oid)
        print(f"  {oid} (time: {ts.isoformat()})")
    print()
    
    # Convenience functions
    print("5. Convenience Functions")
    print("-" * 40)
    print(f"  short_id():             {short_id()}")
    print(f"  short_id(12):           {short_id(12)}")
    print(f"  timestamp_id('ORD'):    {timestamp_id('ORD')}")
    print(f"  prefixed_uuid('USER'):  {prefixed_uuid('USER')}")
    print(f"  ksuid():                {ksuid()}")
    print(f"  cuid2():                {cuid2()}")
    print(f"  tsid('INV'):            {tsid('INV')}")
    print()
    
    # Sequential ID Generator
    print("6. Sequential ID Generator")
    print("-" * 40)
    order_gen = sequential_id('ORD', padding=8)
    print("  Order ID Generator (padding=8):")
    for i in range(5):
        print(f"    {order_gen()}")
    print()
    
    # UUID variants
    print("7. UUID Variants")
    print("-" * 40)
    print(f"  UUID4 string:   {uuid4_str()}")
    print(f"  UUID4 hex:      {uuid4_hex()}")
    print(f"  UUID7 string:   {uuid7_str()}")
    print()
    
    # ID Analysis
    print("8. ID Analysis")
    print("-" * 40)
    
    ulid = ULID.generate()
    oid = ObjectId.generate()
    numeric = '1234567890'
    
    print(f"  ULID analysis:")
    result = analyze_id(ulid)
    print(f"    Type: {result['type']}")
    if 'timestamp' in result['properties']:
        print(f"    Time: {result['properties']['timestamp']}")
    
    print(f"  ObjectId analysis:")
    result = analyze_id(oid)
    print(f"    Type: {result['type']}")
    
    print(f"  Numeric analysis:")
    result = analyze_id(numeric)
    print(f"    Type: {result['type']}, Value: {result['properties']['value']}")
    print()
    
    print("=" * 60)
    print("Examples completed!")
    print("=" * 60)


if __name__ == '__main__':
    main()