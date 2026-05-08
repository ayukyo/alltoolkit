#!/usr/bin/env python3
"""UUIDv7 Utils Tests"""

import sys
import os
import time
import threading
from datetime import datetime, timezone, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    UUIDv7, UUIDv7Generator, UUIDv7Validator, UUIDv7Set, UUIDv7Range,
    UUIDv7Strategy, UUIDv7Components,
    generate, generate_monotonic, generate_batch, parse, is_uuidv7,
    from_timestamp, from_datetime, get_generator
)


class TestResultCollector:
    """收集测试结果"""
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def add_pass(self, name):
        self.passed += 1
        print(f"✓ {name}")
    
    def add_fail(self, name, msg):
        self.failed += 1
        self.errors.append((name, msg))
        print(f"✗ {name}: {msg}")
    
    def report(self):
        print(f"\n{'='*60}")
        print(f"UUIDv7 Utils Tests: {self.passed} passed, {self.failed} failed")
        if self.errors:
            print(f"\nFailed tests:")
            for name, msg in self.errors:
                print(f"  - {name}: {msg}")
        print(f"{'='*60}")
        return self.failed == 0


def run_tests():
    results = TestResultCollector()
    
    # Test 1: Basic UUIDv7 generation
    try:
        uuid = UUIDv7.generate()
        assert uuid.version == 7
        assert uuid.variant == 2
        assert len(str(uuid)) == 36  # Standard UUID format
        assert uuid.timestamp > 0
        results.add_pass("Basic UUIDv7 generation")
    except Exception as e:
        results.add_fail("Basic UUIDv7 generation", str(e))
    
    # Test 2: UUID string format
    try:
        uuid = UUIDv7.generate()
        s = str(uuid)
        parts = s.split('-')
        assert len(parts) == 5
        assert len(parts[0]) == 8
        assert len(parts[1]) == 4
        assert len(parts[2]) == 4
        assert len(parts[3]) == 4
        assert len(parts[4]) == 12
        results.add_pass("UUID string format")
    except Exception as e:
        results.add_fail("UUID string format", str(e))
    
    # Test 3: UUID from string
    try:
        uuid1 = UUIDv7.generate()
        uuid2 = UUIDv7(str(uuid1))
        assert uuid1 == uuid2
        assert uuid1.int == uuid2.int
        results.add_pass("UUID from string")
    except Exception as e:
        results.add_fail("UUID from string", str(e))
    
    # Test 4: UUID from int
    try:
        uuid1 = UUIDv7.generate()
        uuid2 = UUIDv7(uuid1.int)
        assert uuid1 == uuid2
        results.add_pass("UUID from int")
    except Exception as e:
        results.add_fail("UUID from int", str(e))
    
    # Test 5: UUID from bytes
    try:
        uuid1 = UUIDv7.generate()
        uuid2 = UUIDv7(uuid1.bytes)
        assert uuid1 == uuid2
        assert len(uuid1.bytes) == 16
        results.add_pass("UUID from bytes")
    except Exception as e:
        results.add_fail("UUID from bytes", str(e))
    
    # Test 6: UUID properties
    try:
        uuid = UUIDv7.generate()
        assert isinstance(uuid.hex, str)
        assert len(uuid.hex) == 32
        assert isinstance(uuid.urn, str)
        assert uuid.urn.startswith('urn:uuid:')
        assert isinstance(uuid.datetime, datetime)
        results.add_pass("UUID properties")
    except Exception as e:
        results.add_fail("UUID properties", str(e))
    
    # Test 7: Timestamp extraction
    try:
        now_ms = int(time.time() * 1000)
        uuid = UUIDv7.generate()
        # Timestamp should be close to now (within a few seconds)
        diff = abs(uuid.timestamp - now_ms)
        assert diff < 5000  # Within 5 seconds
        results.add_pass("Timestamp extraction")
    except Exception as e:
        results.add_fail("Timestamp extraction", str(e))
    
    # Test 8: UUID from timestamp
    try:
        timestamp_ms = 1712534567890
        uuid = UUIDv7.from_timestamp(timestamp_ms)
        assert uuid.timestamp == timestamp_ms
        assert uuid.version == 7
        results.add_pass("UUID from timestamp")
    except Exception as e:
        results.add_fail("UUID from timestamp", str(e))
    
    # Test 9: UUID from datetime
    try:
        dt = datetime(2024, 4, 7, 12, 42, 47, tzinfo=timezone.utc)
        uuid = UUIDv7.from_datetime(dt)
        expected_ms = int(dt.timestamp() * 1000)
        assert uuid.timestamp == expected_ms
        results.add_pass("UUID from datetime")
    except Exception as e:
        results.add_fail("UUID from datetime", str(e))
    
    # Test 10: UUID comparison
    try:
        uuid1 = UUIDv7.from_timestamp(1000)
        uuid2 = UUIDv7.from_timestamp(2000)
        assert uuid1 < uuid2
        assert uuid2 > uuid1
        assert uuid1 <= uuid2
        assert uuid2 >= uuid1
        assert uuid1 != uuid2
        results.add_pass("UUID comparison")
    except Exception as e:
        results.add_fail("UUID comparison", str(e))
    
    # Test 11: UUID equality
    try:
        uuid1 = UUIDv7.generate()
        uuid2 = UUIDv7(uuid1.int)
        assert uuid1 == uuid2
        assert uuid1 == str(uuid2)
        assert uuid1 == uuid2.int
        results.add_pass("UUID equality")
    except Exception as e:
        results.add_fail("UUID equality", str(e))
    
    # Test 12: UUID hash
    try:
        uuid1 = UUIDv7.generate()
        uuid2 = UUIDv7(uuid1.int)
        assert hash(uuid1) == hash(uuid2)
        # Can be used in set/dict
        s = {uuid1, uuid2}
        assert len(s) == 1
        results.add_pass("UUID hash")
    except Exception as e:
        results.add_fail("UUID hash", str(e))
    
    # Test 13: Monotonic generation
    try:
        gen = UUIDv7Generator()
        uuids = [gen.generate() for _ in range(100)]
        # All UUIDs should be monotonically increasing
        for i in range(1, len(uuids)):
            assert uuids[i-1] < uuids[i]
        results.add_pass("Monotonic generation")
    except Exception as e:
        results.add_fail("Monotonic generation", str(e))
    
    # Test 14: Batch generation
    try:
        uuids = generate_batch(10, monotonic=True)
        assert len(uuids) == 10
        # Check monotonic order
        for i in range(1, len(uuids)):
            assert uuids[i-1] <= uuids[i]
        results.add_pass("Batch generation")
    except Exception as e:
        results.add_fail("Batch generation", str(e))
    
    # Test 15: UUIDv7Validator - is_valid_uuid
    try:
        uuid = UUIDv7.generate()
        assert UUIDv7Validator.is_valid_uuid(str(uuid))
        assert not UUIDv7Validator.is_valid_uuid("invalid-uuid")
        assert not UUIDv7Validator.is_valid_uuid("12345")
        results.add_pass("Validator is_valid_uuid")
    except Exception as e:
        results.add_fail("Validator is_valid_uuid", str(e))
    
    # Test 16: UUIDv7Validator - is_uuidv7
    try:
        uuid = UUIDv7.generate()
        assert UUIDv7Validator.is_uuidv7(uuid)
        assert UUIDv7Validator.is_uuidv7(str(uuid))
        # Non-v7 UUID should fail
        non_v7_str = "00000000-0000-0000-0000-000000000000"
        assert not UUIDv7Validator.is_uuidv7(non_v7_str)
        results.add_pass("Validator is_uuidv7")
    except Exception as e:
        results.add_fail("Validator is_uuidv7", str(e))
    
    # Test 17: UUIDv7Validator - validate
    try:
        uuid = UUIDv7.generate()
        validated = UUIDv7Validator.validate(uuid)
        assert validated == uuid
        
        validated_str = UUIDv7Validator.validate(str(uuid))
        assert validated_str == uuid
        
        # Invalid should raise
        try:
            UUIDv7Validator.validate("invalid")
            results.add_fail("Validator validate", "Should raise for invalid")
        except ValueError:
            pass
        results.add_pass("Validator validate")
    except Exception as e:
        results.add_fail("Validator validate", str(e))
    
    # Test 18: UUIDv7Set
    try:
        uuid1 = UUIDv7.generate()
        uuid2 = UUIDv7.generate()
        uuid_set = UUIDv7Set([uuid1, uuid2])
        assert uuid1 in uuid_set
        assert uuid2 in uuid_set
        assert len(uuid_set) == 2
        
        uuid3 = UUIDv7.generate()
        uuid_set.add(uuid3)
        assert uuid3 in uuid_set
        assert len(uuid_set) == 3
        
        uuid_set.remove(uuid1)
        assert uuid1 not in uuid_set
        assert len(uuid_set) == 2
        results.add_pass("UUIDv7Set")
    except Exception as e:
        results.add_fail("UUIDv7Set", str(e))
    
    # Test 19: UUIDv7Set iteration
    try:
        uuids = [UUIDv7.generate() for _ in range(5)]
        uuid_set = UUIDv7Set(uuids)
        for uuid in uuid_set:
            assert isinstance(uuid, UUIDv7)
        
        hex_list = uuid_set.to_hex_list()
        assert len(hex_list) == 5
        assert all(len(h) == 32 for h in hex_list)
        results.add_pass("UUIDv7Set iteration")
    except Exception as e:
        results.add_fail("UUIDv7Set iteration", str(e))
    
    # Test 20: UUIDv7Range
    try:
        start = datetime(2024, 1, 1, tzinfo=timezone.utc)
        end = datetime(2024, 1, 2, tzinfo=timezone.utc)
        range_ = UUIDv7Range.from_datetime_range(start, end)
        
        uuid_in_range = UUIDv7.from_datetime(datetime(2024, 1, 1, 12, tzinfo=timezone.utc))
        uuid_out_range = UUIDv7.from_datetime(datetime(2023, 1, 1, tzinfo=timezone.utc))
        
        assert uuid_in_range in range_
        assert uuid_out_range not in range_
        results.add_pass("UUIDv7Range")
    except Exception as e:
        results.add_fail("UUIDv7Range", str(e))
    
    # Test 21: UUIDv7Range - last_hours/days
    try:
        range_hours = UUIDv7Range.last_hours(24)
        assert range_hours.duration_seconds == 24 * 3600
        
        range_days = UUIDv7Range.last_days(7)
        assert range_days.duration_seconds == 7 * 24 * 3600
        
        current_uuid = UUIDv7.generate()
        assert current_uuid in range_hours
        results.add_pass("UUIDv7Range last_hours/days")
    except Exception as e:
        results.add_fail("UUIDv7Range last_hours/days", str(e))
    
    # Test 22: Convenience functions
    try:
        uuid1 = generate()
        assert uuid1.version == 7
        
        uuid2 = generate_monotonic()
        assert uuid2.version == 7
        
        uuid3 = parse(str(uuid1))
        assert uuid3 == uuid1
        
        assert is_uuidv7(uuid1)
        
        gen = get_generator()
        assert isinstance(gen, UUIDv7Generator)
        results.add_pass("Convenience functions")
    except Exception as e:
        results.add_fail("Convenience functions", str(e))
    
    # Test 23: UUID format specifier
    try:
        uuid = UUIDv7.generate()
        assert format(uuid, 'x') == uuid.hex
        assert format(uuid, 'X') == uuid.hex.upper()
        assert format(uuid, 's') == str(uuid)
        assert format(uuid, 'n') == uuid.hex
        assert format(uuid, 'u') == uuid.urn
        results.add_pass("UUID format specifier")
    except Exception as e:
        results.add_fail("UUID format specifier", str(e))
    
    # Test 24: UUID components
    try:
        uuid = UUIDv7.generate()
        components = uuid.components
        assert isinstance(components, UUIDv7Components)
        assert components.timestamp_ms == uuid.timestamp
        assert components.version == 7
        assert components.variant == 2
        assert isinstance(components.datetime, datetime)
        results.add_pass("UUID components")
    except Exception as e:
        results.add_fail("UUID components", str(e))
    
    # Test 25: Thread-safe generator
    try:
        gen = UUIDv7Generator()
        results_list = []
        
        def generate_uuids(count):
            for _ in range(count):
                results_list.append(gen.generate())
        
        threads = [threading.Thread(target=generate_uuids, args=(50,)) for _ in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        assert len(results_list) == 200
        
        # All should be unique
        unique_ints = set(u.int for u in results_list)
        assert len(unique_ints) == 200
        
        # All should be sorted (monotonic)
        sorted_uuids = sorted(results_list)
        for i in range(1, len(sorted_uuids)):
            assert sorted_uuids[i-1] <= sorted_uuids[i]
        results.add_pass("Thread-safe generator")
    except Exception as e:
        results.add_fail("Thread-safe generator", str(e))
    
    # Test 26: Invalid UUID string
    try:
        try:
            UUIDv7("invalid-string")
            results.add_fail("Invalid UUID string", "Should raise ValueError")
        except ValueError:
            pass
        results.add_pass("Invalid UUID string")
    except Exception as e:
        results.add_fail("Invalid UUID string", str(e))
    
    # Test 27: Invalid UUID bytes
    try:
        try:
            UUIDv7(b"short")
            results.add_fail("Invalid UUID bytes", "Should raise ValueError")
        except ValueError:
            pass
        results.add_pass("Invalid UUID bytes")
    except Exception as e:
        results.add_fail("Invalid UUID bytes", str(e))
    
    # Test 28: Invalid timestamp
    try:
        try:
            UUIDv7.from_timestamp(-1)
            results.add_fail("Invalid timestamp", "Should raise ValueError")
        except ValueError:
            pass
        
        try:
            UUIDv7.from_timestamp(1 << 50)  # Too large
            results.add_fail("Invalid timestamp", "Should raise ValueError for too large")
        except ValueError:
            pass
        results.add_pass("Invalid timestamp")
    except Exception as e:
        results.add_fail("Invalid timestamp", str(e))
    
    # Test 29: Generator with node_id
    try:
        gen = UUIDv7Generator(node_id=100)
        uuid = gen.generate()
        assert uuid.version == 7
        
        try:
            UUIDv7Generator(node_id=2000)  # > 1023
            results.add_fail("Generator with node_id", "Should raise for invalid node_id")
        except ValueError:
            pass
        results.add_pass("Generator with node_id")
    except Exception as e:
        results.add_fail("Generator with node_id", str(e))
    
    # Test 30: UUID bool
    try:
        uuid = UUIDv7.generate()
        assert bool(uuid) == True
        results.add_pass("UUID bool")
    except Exception as e:
        results.add_fail("UUID bool", str(e))
    
    return results.report()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)