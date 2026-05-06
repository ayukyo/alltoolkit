"""
UUIDv7 Utils - Usage Examples

This file demonstrates various use cases for UUIDv7 in real-world scenarios.
"""

import time
import sys
import os
from datetime import datetime, timezone, timedelta

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from uuidv7_utils.mod import (
    UUIDv7, UUIDv7Generator, UUIDv7Validator, UUIDv7Set, UUIDv7Range,
    generate, generate_monotonic, generate_batch, parse, is_uuidv7,
    from_timestamp, from_datetime
)


def example_basic_generation():
    """Basic UUIDv7 generation"""
    print("=" * 60)
    print("Basic UUIDv7 Generation")
    print("=" * 60)
    
    # Generate a new UUIDv7
    uuid = UUIDv7.generate()
    print(f"UUIDv7: {uuid}")
    print(f"Version: {uuid.version}")
    print(f"Timestamp: {uuid.timestamp}")
    print(f"Datetime: {uuid.datetime}")
    print(f"Hex: {uuid.hex}")
    print(f"URN: {uuid.urn}")
    print(f"Bytes length: {len(uuid.bytes)}")
    
    # Using convenience function
    uuid2 = generate()
    print(f"\nUsing generate(): {uuid2}")


def example_monotonic_generation():
    """Monotonically increasing UUIDv7 generation"""
    print("\n" + "=" * 60)
    print("Monotonic Generation")
    print("=" * 60)
    
    gen = UUIDv7Generator()
    
    # Generate 5 UUIDs
    uuids = [gen.generate() for _ in range(5)]
    
    for i, uuid in enumerate(uuids):
        print(f"{i+1}. {uuid} (ts: {uuid.timestamp})")
    
    # Verify ordering
    is_ordered = all(uuids[i] < uuids[i+1] for i in range(len(uuids)-1))
    print(f"\nMonotonically ordered: {is_ordered}")


def example_batch_generation():
    """Batch generation for efficiency"""
    print("\n" + "=" * 60)
    print("Batch Generation")
    print("=" * 60)
    
    # Generate 100 UUIDs at once
    uuids = generate_batch(10, monotonic=True)
    
    print(f"Generated {len(uuids)} UUIDs:")
    for i, uuid in enumerate(uuids[:5]):
        print(f"  {i+1}. {uuid}")
    print(f"  ... and {len(uuids) - 5} more")


def example_from_timestamp():
    """Creating UUIDv7 from specific timestamps"""
    print("\n" + "=" * 60)
    print("Creating UUIDs from Timestamps")
    print("=" * 60)
    
    # New Year 2024
    new_year = datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    uuid_new_year = UUIDv7.from_datetime(new_year)
    print(f"New Year 2024: {uuid_new_year}")
    print(f"  DateTime: {uuid_new_year.datetime}")
    
    # Unix epoch
    epoch = 0
    uuid_epoch = UUIDv7.from_timestamp(epoch)
    print(f"\nUnix Epoch: {uuid_epoch}")
    print(f"  DateTime: {uuid_epoch.datetime}")
    
    # Current time
    now_ms = int(time.time() * 1000)
    uuid_now = UUIDv7.from_timestamp(now_ms)
    print(f"\nNow: {uuid_now}")
    print(f"  DateTime: {uuid_now.datetime}")


def example_parsing():
    """Parsing UUID strings and bytes"""
    print("\n" + "=" * 60)
    print("Parsing UUIDs")
    print("=" * 60)
    
    original = UUIDv7.generate()
    print(f"Original: {original}")
    
    # Parse from string
    from_string = UUIDv7(str(original))
    print(f"From string: {from_string}")
    print(f"Equal: {from_string == original}")
    
    # Parse from hex
    from_hex = UUIDv7(original.hex)
    print(f"\nFrom hex: {from_hex}")
    print(f"Equal: {from_hex == original}")
    
    # Parse from bytes
    from_bytes = UUIDv7(original.bytes)
    print(f"\nFrom bytes: {from_bytes}")
    print(f"Equal: {from_bytes == original}")
    
    # Parse from integer
    from_int = UUIDv7(original.int)
    print(f"\nFrom integer: {from_int}")
    print(f"Equal: {from_int == original}")


def example_validation():
    """Validating UUIDs"""
    print("\n" + "=" * 60)
    print("UUID Validation")
    print("=" * 60)
    
    valid_uuid = str(UUIDv7.generate())
    invalid_uuid = "not-a-valid-uuid"
    
    print(f"'{valid_uuid}' is valid UUIDv7: {is_uuidv7(valid_uuid)}")
    print(f"'{invalid_uuid}' is valid UUIDv7: {is_uuidv7(invalid_uuid)}")
    
    # Using validator class
    try:
        validated = UUIDv7Validator.validate(valid_uuid)
        print(f"\nValidated: {validated}")
    except ValueError as e:
        print(f"Validation failed: {e}")
    
    try:
        UUIDv7Validator.validate(invalid_uuid)
    except ValueError as e:
        print(f"\nValidation failed for invalid: {e}")


def example_comparison():
    """Comparing UUIDs"""
    print("\n" + "=" * 60)
    print("UUID Comparison")
    print("=" * 60)
    
    uuid1 = UUIDv7.generate()
    time.sleep(0.002)  # 2ms
    uuid2 = UUIDv7.generate()
    
    print(f"UUID1: {uuid1}")
    print(f"UUID2: {uuid2}")
    print(f"\nuuid1 < uuid2: {uuid1 < uuid2}")
    print(f"uuid1 == uuid2: {uuid1 == uuid2}")
    print(f"uuid1 <= uuid2: {uuid1 <= uuid2}")
    
    # Same UUID comparison
    uuid_copy = UUIDv7(uuid1.hex)
    print(f"\nuuid1 == uuid_copy: {uuid1 == uuid_copy}")
    print(f"uuid1 is uuid_copy: {uuid1 is uuid_copy}")
    
    # Comparison with string
    print(f"\nuuid1 == str(uuid1): {uuid1 == str(uuid1)}")


def example_uuid_set():
    """Using UUIDv7Set for collection operations"""
    print("\n" + "=" * 60)
    print("UUIDv7Set Collection")
    print("=" * 60)
    
    # Create a set with some UUIDs
    uuids = [UUIDv7.generate() for _ in range(5)]
    uuid_set = UUIDv7Set(uuids)
    
    print(f"Set size: {len(uuid_set)}")
    
    # Check membership
    print(f"\nFirst UUID in set: {uuids[0] in uuid_set}")
    
    # Add new UUID
    new_uuid = UUIDv7.generate()
    uuid_set.add(new_uuid)
    print(f"Added new UUID: {new_uuid}")
    print(f"New UUID in set: {new_uuid in uuid_set}")
    
    # Remove UUID
    uuid_set.remove(uuids[0])
    print(f"\nRemoved first UUID")
    print(f"First UUID in set: {uuids[0] in uuid_set}")
    
    # Convert to list
    hex_list = uuid_set.to_hex_list()
    print(f"\nHex list: {hex_list[:2]}...")


def example_time_range():
    """Time-based UUID filtering"""
    print("\n" + "=" * 60)
    print("Time-Based UUID Filtering")
    print("=" * 60)
    
    # Create a range for last 24 hours
    range_24h = UUIDv7Range.last_hours(24)
    print(f"Last 24 hours range: {range_24h}")
    print(f"  Start: {range_24h.start_datetime()}")
    print(f"  End: {range_24h.end_datetime()}")
    
    # Check if current UUID is in range
    current_uuid = UUIDv7.generate()
    print(f"\nCurrent UUID in last 24h: {current_uuid in range_24h}")
    
    # Create a specific date range
    start = datetime(2024, 1, 1, tzinfo=timezone.utc)
    end = datetime(2024, 12, 31, tzinfo=timezone.utc)
    year_2024 = UUIDv7Range.from_datetime_range(start, end)
    print(f"\n2024 year range: {year_2024}")
    
    # UUID from 2024
    uuid_2024 = UUIDv7.from_datetime(datetime(2024, 6, 15, tzinfo=timezone.utc))
    print(f"2024 UUID in 2024 range: {uuid_2024 in year_2024}")
    print(f"Current UUID in 2024 range: {current_uuid in year_2024}")
    
    # Last 7 days
    range_7d = UUIDv7Range.last_days(7)
    print(f"\nLast 7 days: {range_7d}")
    print(f"Duration: {range_7d.duration_seconds / 3600} hours")


def example_database_use_case():
    """Database primary key use case"""
    print("\n" + "=" * 60)
    print("Database Primary Key Use Case")
    print("=" * 60)
    
    gen = UUIDv7Generator()
    
    # Simulate inserting records
    records = []
    for i in range(5):
        record = {
            'id': gen.generate(),
            'name': f'User {i+1}',
            'created_at': datetime.now(timezone.utc)
        }
        records.append(record)
    
    print("Generated IDs for user records:")
    for record in records:
        print(f"  {record['id']} - {record['name']} @ {record['id'].datetime}")
    
    # IDs are naturally ordered by time
    ids = [r['id'] for r in records]
    print(f"\nIDs are time-ordered: {ids == sorted(ids)}")
    print("This means: ")
    print("  - Database indexes are more efficient")
    print("  - Range queries by time are fast")
    print("  - Natural clustering by creation time")


def example_distributed_system():
    """Distributed system use case with node IDs"""
    print("\n" + "=" * 60)
    print("Distributed System Use Case")
    print("=" * 60)
    
    # Simulate multiple nodes
    nodes = {
        'node-1': UUIDv7Generator(node_id=1),
        'node-2': UUIDv7Generator(node_id=2),
        'node-3': UUIDv7Generator(node_id=3),
    }
    
    # Each node generates IDs
    for node_name, generator in nodes.items():
        uuid = generator.generate()
        print(f"{node_name}: {uuid}")
        print(f"  Timestamp: {uuid.timestamp}")
        print(f"  Created: {uuid.datetime}")


def example_time_based_queries():
    """Time-based query filtering"""
    print("\n" + "=" * 60)
    print("Time-Based Query Filtering")
    print("=" * 60)
    
    # Generate IDs over time
    ids = []
    for i in range(10):
        ids.append(UUIDv7.generate())
        time.sleep(0.001)  # 1ms delay
    
    # Query: Find IDs created in last 5ms
    range_5ms = UUIDv7Range.from_timestamp(
        int(time.time() * 1000) - 5,
        5
    )
    
    matching = [uid for uid in ids if uid in range_5ms]
    print(f"Total IDs: {len(ids)}")
    print(f"IDs in last 5ms: {len(matching)}")
    
    # Query: Find IDs before a specific time
    cutoff = ids[5].timestamp
    before = [uid for uid in ids if uid.timestamp < cutoff]
    print(f"\nIDs before index 5: {len(before)}")
    
    # Sort by creation time
    sorted_ids = sorted(ids)
    print(f"\nIDs sorted by time: {sorted_ids == ids}")


def example_thread_safety():
    """Thread-safe generation"""
    print("\n" + "=" * 60)
    print("Thread-Safe Generation")
    print("=" * 60)
    
    import threading
    
    gen = UUIDv7Generator()
    all_ids = []
    lock = threading.Lock()
    
    def generate_ids():
        for _ in range(100):
            uid = gen.generate()
            with lock:
                all_ids.append(uid)
    
    threads = [threading.Thread(target=generate_ids) for _ in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    
    print(f"Generated {len(all_ids)} IDs from 5 threads")
    print(f"All unique: {len(set(str(u) for u in all_ids)) == len(all_ids)}")
    print(f"All ordered: {all_ids == sorted(all_ids)}")


def run_all_examples():
    """Run all examples"""
    example_basic_generation()
    example_monotonic_generation()
    example_batch_generation()
    example_from_timestamp()
    example_parsing()
    example_validation()
    example_comparison()
    example_uuid_set()
    example_time_range()
    example_database_use_case()
    example_distributed_system()
    example_time_based_queries()
    example_thread_safety()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    run_all_examples()