"""
Tests for UUIDv7 Utils

Comprehensive test suite for UUIDv7 generation, validation, and utilities.
"""

import time
import threading
import sys
import os
from datetime import datetime, timezone, timedelta

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from uuidv7_utils.mod import (
    UUIDv7, UUIDv7Generator, UUIDv7Validator, UUIDv7Set, UUIDv7Range,
    UUIDv7Strategy, UUIDv7Components,
    generate, generate_monotonic, generate_batch, parse, is_uuidv7,
    from_timestamp, from_datetime
)


class TestUUIDv7Generation:
    """Tests for UUIDv7 generation"""
    
    def test_basic_generation(self):
        """Test basic UUIDv7 generation"""
        uuid = UUIDv7.generate()
        
        assert uuid.version == 7
        assert uuid.variant == 2
        assert uuid.timestamp > 0
        assert len(str(uuid)) == 36  # Standard UUID format
    
    def test_different_uuids(self):
        """Test that multiple generations produce different UUIDs"""
        uuids = [UUIDv7.generate() for _ in range(100)]
        unique_uuids = set(str(u) for u in uuids)
        assert len(unique_uuids) == 100
    
    def test_timestamp_approximation(self):
        """Test that timestamp is close to current time"""
        before = int(time.time() * 1000)
        uuid = UUIDv7.generate()
        after = int(time.time() * 1000)
        
        assert before <= uuid.timestamp <= after
    
    def test_from_timestamp(self):
        """Test creating UUIDv7 from specific timestamp"""
        timestamp_ms = 1704067200000  # 2024-01-01 00:00:00 UTC
        uuid = UUIDv7.from_timestamp(timestamp_ms)
        
        assert uuid.timestamp == timestamp_ms
        assert uuid.version == 7
    
    def test_from_datetime(self):
        """Test creating UUIDv7 from datetime"""
        dt = datetime(2024, 1, 1, 12, 30, 45, tzinfo=timezone.utc)
        uuid = UUIDv7.from_datetime(dt)
        
        # Allow small time difference due to conversion
        expected_ms = int(dt.timestamp() * 1000)
        assert abs(uuid.timestamp - expected_ms) < 1
    
    def test_parse_hex_string(self):
        """Test parsing UUID from hex string"""
        original = UUIDv7.generate()
        hex_str = original.hex
        
        parsed = UUIDv7(hex_str)
        assert parsed == original
    
    def test_parse_standard_format(self):
        """Test parsing UUID from standard format"""
        original = UUIDv7.generate()
        std_str = str(original)
        
        parsed = UUIDv7(std_str)
        assert parsed == original
    
    def test_parse_with_braces(self):
        """Test parsing UUID with braces"""
        original = UUIDv7.generate()
        braced = f'{{{str(original)}}}'
        
        parsed = UUIDv7(braced)
        assert parsed == original
    
    def test_parse_bytes(self):
        """Test parsing UUID from bytes"""
        original = UUIDv7.generate()
        uuid_bytes = original.bytes
        
        parsed = UUIDv7(uuid_bytes)
        assert parsed == original
    
    def test_invalid_parse(self):
        """Test that invalid formats raise errors"""
        try:
            UUIDv7("not-a-uuid")
            assert False, "Should have raised ValueError"
        except ValueError:
            pass
        
        # Note: UUIDv7(12345) creates a valid UUID with version 0 (not UUIDv7)
        # This is acceptable behavior - the int is valid as a UUID
        # To validate as UUIDv7, use UUIDv7Validator.is_uuidv7()
        uuid_small = UUIDv7(12345)
        assert uuid_small.version == 0  # Not a UUIDv7
        assert not UUIDv7Validator.is_uuidv7(uuid_small)


class TestUUIDv7Properties:
    """Tests for UUIDv7 properties"""
    
    def test_int_property(self):
        """Test integer representation"""
        uuid = UUIDv7.generate()
        assert isinstance(uuid.int, int)
        assert uuid.int >= 0
        assert uuid.int < (1 << 128)
    
    def test_bytes_property(self):
        """Test bytes representation"""
        uuid = UUIDv7.generate()
        assert len(uuid.bytes) == 16
    
    def test_hex_property(self):
        """Test hex string property"""
        uuid = UUIDv7.generate()
        assert len(uuid.hex) == 32
        assert all(c in '0123456789abcdef' for c in uuid.hex)
    
    def test_urn_property(self):
        """Test URN representation"""
        uuid = UUIDv7.generate()
        urn = uuid.urn
        assert urn.startswith('urn:uuid:')
        assert len(urn) == 45  # urn:uuid: + 36 chars
    
    def test_datetime_property(self):
        """Test datetime extraction"""
        dt = datetime(2024, 6, 15, 10, 30, 0, tzinfo=timezone.utc)
        uuid = UUIDv7.from_datetime(dt)
        
        extracted = uuid.datetime
        # Allow 1 second tolerance
        assert abs((extracted - dt).total_seconds()) < 1
    
    def test_components(self):
        """Test component extraction"""
        uuid = UUIDv7.generate()
        components = uuid.components
        
        assert isinstance(components, UUIDv7Components)
        assert components.timestamp_ms == uuid.timestamp
        assert components.version == 7
        assert components.variant == 2
        assert isinstance(components.datetime, datetime)


class TestUUIDv7Comparison:
    """Tests for UUIDv7 comparison operations"""
    
    def test_equality(self):
        """Test UUID equality"""
        uuid1 = UUIDv7.generate()
        uuid2 = UUIDv7(uuid1.hex)
        
        assert uuid1 == uuid2
        assert hash(uuid1) == hash(uuid2)
    
    def test_inequality(self):
        """Test UUID inequality"""
        uuid1 = UUIDv7.generate()
        uuid2 = UUIDv7.generate()
        
        assert uuid1 != uuid2
    
    def test_ordering_by_time(self):
        """Test that UUIDs are ordered by time"""
        uuids = []
        for _ in range(10):
            uuids.append(UUIDv7.generate())
            time.sleep(0.001)  # 1ms
        
        for i in range(len(uuids) - 1):
            assert uuids[i] < uuids[i+1] or uuids[i].timestamp <= uuids[i+1].timestamp
    
    def test_comparison_with_string(self):
        """Test comparison with string representation"""
        uuid = UUIDv7.generate()
        uuid_str = str(uuid)
        
        assert uuid == uuid_str
    
    def test_comparison_with_int(self):
        """Test comparison with integer representation"""
        uuid = UUIDv7.generate()
        uuid_int = uuid.int
        
        assert uuid == uuid_int


class TestUUIDv7Formatting:
    """Tests for UUIDv7 formatting"""
    
    def test_str_format(self):
        """Test string format"""
        uuid = UUIDv7.generate()
        s = str(uuid)
        
        # Check format: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        parts = s.split('-')
        assert len(parts) == 5
        assert len(parts[0]) == 8
        assert len(parts[1]) == 4
        assert len(parts[2]) == 4
        assert len(parts[3]) == 4
        assert len(parts[4]) == 12
    
    def test_repr(self):
        """Test representation"""
        uuid = UUIDv7.generate()
        r = repr(uuid)
        
        assert r.startswith("UUIDv7('")
        assert r.endswith("')")
    
    def test_format_spec(self):
        """Test format specifications"""
        uuid = UUIDv7.generate()
        
        assert format(uuid, 's') == str(uuid)
        assert format(uuid, 'x') == uuid.hex
        assert format(uuid, 'X') == uuid.hex.upper()
        assert format(uuid, 'n') == uuid.hex  # No dashes
    
    def test_bool(self):
        """Test boolean conversion"""
        uuid = UUIDv7.generate()
        assert bool(uuid) is True


class TestUUIDv7Generator:
    """Tests for UUIDv7Generator class"""
    
    def test_monotonic_generation(self):
        """Test that generator produces monotonically increasing UUIDs"""
        gen = UUIDv7Generator()
        uuids = [gen.generate() for _ in range(100)]
        
        for i in range(len(uuids) - 1):
            assert uuids[i] < uuids[i+1], f"UUIDs not monotonic at index {i}"
    
    def test_same_millisecond_ordering(self):
        """Test ordering within same millisecond"""
        gen = UUIDv7Generator()
        
        # Generate many UUIDs quickly (likely same millisecond)
        uuids = [gen.generate() for _ in range(50)]
        
        for i in range(len(uuids) - 1):
            assert uuids[i] <= uuids[i+1]
    
    def test_batch_generation(self):
        """Test batch generation"""
        gen = UUIDv7Generator()
        uuids = gen.generate_batch(10)
        
        assert len(uuids) == 10
        assert len(set(str(u) for u in uuids)) == 10  # All unique
    
    def test_node_id(self):
        """Test generator with node ID"""
        node_id = 42
        gen = UUIDv7Generator(node_id=node_id)
        uuid = gen.generate()
        
        assert uuid.version == 7
    
    def test_invalid_node_id(self):
        """Test that invalid node ID raises error"""
        try:
            UUIDv7Generator(node_id=2000)  # > 1023
            assert False, "Should have raised ValueError"
        except ValueError:
            pass
    
    def test_thread_safety(self):
        """Test thread-safe generation"""
        gen = UUIDv7Generator()
        uuids = []
        lock = threading.Lock()
        
        def generate_many():
            for _ in range(100):
                uuid = gen.generate()
                with lock:
                    uuids.append(uuid)
        
        threads = [threading.Thread(target=generate_many) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        assert len(uuids) == 1000
        assert len(set(str(u) for u in uuids)) == 1000  # All unique


class TestUUIDv7Validator:
    """Tests for UUIDv7Validator class"""
    
    def test_is_valid_uuid(self):
        """Test UUID format validation"""
        uuid = UUIDv7.generate()
        assert UUIDv7Validator.is_valid_uuid(str(uuid))
        assert not UUIDv7Validator.is_valid_uuid("not-a-uuid")
    
    def test_is_uuidv7(self):
        """Test UUIDv7 version validation"""
        uuid = UUIDv7.generate()
        assert UUIDv7Validator.is_uuidv7(uuid)
        assert UUIDv7Validator.is_uuidv7(str(uuid))
    
    def test_validate_success(self):
        """Test successful validation"""
        uuid = UUIDv7.generate()
        validated = UUIDv7Validator.validate(uuid)
        assert validated == uuid
    
    def test_validate_failure(self):
        """Test validation failure"""
        try:
            UUIDv7Validator.validate("invalid")
            assert False, "Should have raised ValueError"
        except ValueError:
            pass


class TestUUIDv7Set:
    """Tests for UUIDv7Set class"""
    
    def test_add_and_contains(self):
        """Test adding and checking membership"""
        s = UUIDv7Set()
        uuid = UUIDv7.generate()
        
        s.add(uuid)
        assert uuid in s
    
    def test_remove(self):
        """Test removing UUIDs"""
        s = UUIDv7Set()
        uuid = UUIDv7.generate()
        s.add(uuid)
        
        s.remove(uuid)
        assert uuid not in s
    
    def test_discard(self):
        """Test discarding UUIDs"""
        s = UUIDv7Set()
        uuid = UUIDv7.generate()
        
        s.discard(uuid)  # Should not raise
        s.add(uuid)
        s.discard(uuid)
        assert uuid not in s
    
    def test_len(self):
        """Test set length"""
        s = UUIDv7Set()
        uuids = [UUIDv7.generate() for _ in range(10)]
        
        for u in uuids:
            s.add(u)
        
        assert len(s) == 10
    
    def test_iteration(self):
        """Test set iteration"""
        uuids = [UUIDv7.generate() for _ in range(5)]
        s = UUIDv7Set(uuids)
        
        collected = list(s)
        assert len(collected) == 5
    
    def test_to_list(self):
        """Test conversion to list"""
        uuids = [UUIDv7.generate() for _ in range(3)]
        s = UUIDv7Set(uuids)
        
        lst = s.to_list()
        assert len(lst) == 3
        assert all(isinstance(u, UUIDv7) for u in lst)
    
    def test_to_hex_list(self):
        """Test conversion to hex list"""
        s = UUIDv7Set([UUIDv7.generate() for _ in range(3)])
        
        hex_list = s.to_hex_list()
        assert len(hex_list) == 3
        assert all(len(h) == 32 for h in hex_list)


class TestUUIDv7Range:
    """Tests for UUIDv7Range class"""
    
    def test_contains(self):
        """Test range containment"""
        start = int(time.time() * 1000) - 10000
        end = int(time.time() * 1000) + 10000
        r = UUIDv7Range(start, end)
        
        uuid = UUIDv7.generate()
        assert uuid in r
    
    def test_from_datetime_range(self):
        """Test creating range from datetimes"""
        start = datetime(2024, 1, 1, tzinfo=timezone.utc)
        end = datetime(2024, 12, 31, tzinfo=timezone.utc)
        r = UUIDv7Range.from_datetime_range(start, end)
        
        # UUID from 2024 should be in range
        uuid_2024 = UUIDv7.from_datetime(datetime(2024, 6, 1, tzinfo=timezone.utc))
        assert uuid_2024 in r
        
        # Current UUID should not be in range
        uuid_now = UUIDv7.generate()
        assert uuid_now not in r
    
    def test_from_timestamp(self):
        """Test creating range from timestamp"""
        now = int(time.time() * 1000)
        r = UUIDv7Range.from_timestamp(now, 60000)  # 1 minute
        
        assert r.duration_ms == 60000
    
    def test_last_hours(self):
        """Test range for last N hours"""
        r = UUIDv7Range.last_hours(1)
        
        assert r.duration_seconds == 3600
        
        uuid = UUIDv7.generate()
        assert uuid in r
    
    def test_last_days(self):
        """Test range for last N days"""
        r = UUIDv7Range.last_days(1)
        
        assert r.duration_seconds == 86400
        
        uuid = UUIDv7.generate()
        assert uuid in r
    
    def test_invalid_range(self):
        """Test that invalid range raises error"""
        try:
            UUIDv7Range(100, 50)  # end < start
            assert False, "Should have raised ValueError"
        except ValueError:
            pass


class TestConvenienceFunctions:
    """Tests for module-level convenience functions"""
    
    def test_generate(self):
        """Test generate function"""
        uuid = generate()
        assert isinstance(uuid, UUIDv7)
        assert uuid.version == 7
    
    def test_generate_monotonic(self):
        """Test generate_monotonic function"""
        uuids = [generate_monotonic() for _ in range(10)]
        
        for i in range(len(uuids) - 1):
            assert uuids[i] <= uuids[i+1]
    
    def test_generate_batch(self):
        """Test generate_batch function"""
        uuids = generate_batch(5)
        assert len(uuids) == 5
        
        # Monotonic batch
        uuids = generate_batch(10, monotonic=True)
        for i in range(len(uuids) - 1):
            assert uuids[i] <= uuids[i+1]
    
    def test_parse(self):
        """Test parse function"""
        original = generate()
        parsed = parse(str(original))
        
        assert parsed == original
    
    def test_is_uuidv7(self):
        """Test is_uuidv7 function"""
        uuid = generate()
        assert is_uuidv7(uuid)
        assert is_uuidv7(str(uuid))
        assert not is_uuidv7("not-a-uuid")
    
    def test_from_timestamp_func(self):
        """Test from_timestamp function"""
        ts = 1704067200000
        uuid = from_timestamp(ts)
        
        assert isinstance(uuid, UUIDv7)
        assert uuid.timestamp == ts
    
    def test_from_datetime_func(self):
        """Test from_datetime function"""
        dt = datetime(2024, 1, 1, tzinfo=timezone.utc)
        uuid = from_datetime(dt)
        
        assert isinstance(uuid, UUIDv7)
        assert abs(uuid.timestamp - int(dt.timestamp() * 1000)) < 1


class TestEdgeCases:
    """Tests for edge cases"""
    
    def test_very_old_timestamp(self):
        """Test UUID with very old timestamp"""
        # Year 1970
        ts = 0
        uuid = UUIDv7.from_timestamp(ts)
        assert uuid.timestamp == 0
    
    def test_very_new_timestamp(self):
        """Test UUID with far future timestamp"""
        # Year 5000
        ts = 100000000000000
        uuid = UUIDv7.from_timestamp(ts)
        assert uuid.timestamp == ts
    
    def test_max_random_bits(self):
        """Test with maximum random bits"""
        ts = int(time.time() * 1000)
        max_rand = (1 << 74) - 1
        uuid = UUIDv7.from_timestamp(ts, max_rand)
        
        assert uuid.timestamp == ts
    
    def test_zero_random_bits(self):
        """Test with zero random bits"""
        ts = int(time.time() * 1000)
        uuid = UUIDv7.from_timestamp(ts, 0)
        
        assert uuid.timestamp == ts
    
    def test_empty_set(self):
        """Test empty UUIDv7Set"""
        s = UUIDv7Set()
        assert len(s) == 0
        assert list(s) == []
    
    def test_set_with_duplicates(self):
        """Test set behavior with duplicate UUIDs"""
        uuid = UUIDv7.generate()
        s = UUIDv7Set([uuid, uuid, uuid])
        
        assert len(s) == 1


def run_all_tests():
    """Run all tests"""
    test_classes = [
        TestUUIDv7Generation,
        TestUUIDv7Properties,
        TestUUIDv7Comparison,
        TestUUIDv7Formatting,
        TestUUIDv7Generator,
        TestUUIDv7Validator,
        TestUUIDv7Set,
        TestUUIDv7Range,
        TestConvenienceFunctions,
        TestEdgeCases,
    ]
    
    total_tests = 0
    passed_tests = 0
    failed_tests = 0
    
    for test_class in test_classes:
        print(f"\n{'='*60}")
        print(f"Running {test_class.__name__}")
        print('='*60)
        
        instance = test_class()
        
        for method_name in dir(instance):
            if method_name.startswith('test_'):
                total_tests += 1
                try:
                    getattr(instance, method_name)()
                    print(f"  ✓ {method_name}")
                    passed_tests += 1
                except AssertionError as e:
                    print(f"  ✗ {method_name}: {e}")
                    failed_tests += 1
                except Exception as e:
                    print(f"  ✗ {method_name}: {type(e).__name__}: {e}")
                    failed_tests += 1
    
    print(f"\n{'='*60}")
    print(f"Test Results: {passed_tests}/{total_tests} passed")
    print(f"Failed: {failed_tests}")
    print('='*60)
    
    return failed_tests == 0


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)