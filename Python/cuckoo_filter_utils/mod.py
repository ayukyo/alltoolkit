"""
Cuckoo Filter - A probabilistic data structure for testing set membership.

Cuckoo filters are similar to Bloom filters but offer:
- Support for deletion (unlike Bloom filters)
- Better space efficiency
- Lower false positive rates for the same memory usage
- Constant time operations (O(1) average)

Reference: "Cuckoo Filter: Practically Better Than Bloom" by Fan et al.
"""

import random
import json
import math
from typing import List, Optional, Dict, Any, Tuple

__version__ = "1.0.0"

DEFAULT_BUCKET_SIZE = 4
DEFAULT_MAX_KICKS = 500
DEFAULT_FINGERPRINT_SIZE = 1


class CuckooFilter:
    """
    A Cuckoo filter data structure for approximate set membership queries.
    
    Supports insertion, lookup, and deletion with configurable false positive rate.
    """
    
    def __init__(self, capacity: int, bucket_size: int = DEFAULT_BUCKET_SIZE,
                 max_kicks: int = DEFAULT_MAX_KICKS, fp_rate: float = 0.01):
        """
        Initialize a Cuckoo filter.
        
        Args:
            capacity: Expected number of items to store
            bucket_size: Number of fingerprints per bucket (default: 4)
            max_kicks: Maximum displacement attempts (default: 500)
            fp_rate: Target false positive rate (default: 0.01)
        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if bucket_size <= 0:
            raise ValueError("Bucket size must be positive")
        if max_kicks <= 0:
            raise ValueError("Max kicks must be positive")
        if fp_rate <= 0 or fp_rate >= 1:
            raise ValueError("False positive rate must be between 0 and 1")
        
        self._bucket_size = bucket_size
        self._max_kicks = max_kicks
        
        # Calculate fingerprint size
        # f >= log2(1/epsilon) + log2(2b)
        fp_bits = int(math.ceil(math.log2(1 / fp_rate) + math.log2(2 * bucket_size)))
        self._fp_size = max((fp_bits + 7) // 8, DEFAULT_FINGERPRINT_SIZE)
        
        # Calculate number of buckets (for ~95% load factor)
        num_buckets = capacity // bucket_size
        if num_buckets < 1:
            num_buckets = 1
        # Round up to power of 2 for better hash distribution
        self._num_buckets = self._next_power_of_two(num_buckets)
        
        # Initialize buckets (list of empty fingerprints)
        self._buckets: List[List[Optional[int]]] = [
            [None for _ in range(bucket_size)] for _ in range(self._num_buckets)
        ]
        
        self._count = 0
        self._capacity = self._num_buckets * bucket_size
    
    @property
    def count(self) -> int:
        """Number of items currently stored."""
        return self._count
    
    @property
    def capacity(self) -> int:
        """Total capacity of the filter."""
        return self._capacity
    
    @property
    def load_factor(self) -> float:
        """Load factor (fraction of slots used)."""
        return self._count / self._capacity if self._capacity > 0 else 0
    
    def _next_power_of_two(self, n: int) -> int:
        """Return the smallest power of 2 >= n."""
        if n <= 0:
            return 1
        n -= 1
        n |= n >> 1
        n |= n >> 2
        n |= n >> 4
        n |= n >> 8
        n |= n >> 16
        n |= n >> 32
        return n + 1
    
    def _hash_data(self, data: bytes) -> int:
        """Compute FNV-1a hash of data."""
        h = 14695981039346656037  # FNV offset basis
        for b in data:
            h ^= b
            h *= 1099511628211  # FNV prime
        return h
    
    def _fingerprint(self, data: bytes) -> int:
        """Generate a fingerprint for data."""
        h = self._hash_data(data)
        fp = h & ((1 << (self._fp_size * 8)) - 1)  # Truncate to fp_size bytes
        # Ensure fingerprint is never 0 (empty slot marker)
        if fp == 0:
            fp = 1
        return fp
    
    def _hash1(self, data: bytes) -> int:
        """Compute primary hash index."""
        h = self._hash_data(data)
        return h % self._num_buckets
    
    def _alt_index(self, index: int, fp: int) -> int:
        """Compute alternate bucket index."""
        # Use fingerprint to compute alternate position
        fp_bytes = fp.to_bytes(self._fp_size, 'little', signed=False)
        h = self._hash_data(fp_bytes)
        return (index ^ h) % self._num_buckets
    
    def _insert_fp(self, bucket_idx: int, fp: int) -> bool:
        """Try to insert fingerprint into bucket."""
        bucket = self._buckets[bucket_idx]
        for i in range(self._bucket_size):
            if bucket[i] is None:
                bucket[i] = fp
                return True
        return False
    
    def _contains_fp(self, bucket_idx: int, fp: int) -> bool:
        """Check if fingerprint exists in bucket."""
        bucket = self._buckets[bucket_idx]
        return fp in bucket
    
    def _delete_fp(self, bucket_idx: int, fp: int) -> bool:
        """Remove fingerprint from bucket."""
        bucket = self._buckets[bucket_idx]
        for i in range(self._bucket_size):
            if bucket[i] == fp:
                bucket[i] = None
                return True
        return False
    
    def _relocate_and_insert(self, i1: int, i2: int, fp: int) -> bool:
        """Attempt to relocate entries and insert."""
        indices = [i1, i2]
        idx = random.choice(indices)
        
        for _ in range(self._max_kicks):
            bucket = self._buckets[idx]
            
            # Choose random entry to kick
            entry_idx = random.randint(0, self._bucket_size - 1)
            
            # Swap fingerprints
            old_fp = bucket[entry_idx]
            bucket[entry_idx] = fp
            fp = old_fp
            
            # Find alternate index for kicked fingerprint
            idx = self._alt_index(idx, fp)
            
            # Try to insert kicked fingerprint
            if self._insert_fp(idx, fp):
                self._count += 1
                return True
        
        # Failed after max kicks
        return False
    
    def insert(self, data: bytes) -> bool:
        """
        Insert an item into the filter.
        
        Args:
            data: Item to insert as bytes
        
        Returns:
            True if inserted, False if filter is too full
        
        Example:
            >>> cf = CuckooFilter(10000)
            >>> cf.insert(b"hello")
            True
        """
        fp = self._fingerprint(data)
        i1 = self._hash1(data)
        i2 = self._alt_index(i1, fp)
        
        # Try to insert into either bucket
        if self._insert_fp(i1, fp):
            self._count += 1
            return True
        if self._insert_fp(i2, fp):
            self._count += 1
            return True
        
        # Need to relocate entries
        return self._relocate_and_insert(i1, i2, fp)
    
    def insert_string(self, s: str) -> bool:
        """
        Insert a string into the filter.
        
        Args:
            s: String to insert
        
        Returns:
            True if inserted, False if filter is too full
        
        Example:
            >>> cf = CuckooFilter(10000)
            >>> cf.insert_string("world")
            True
        """
        return self.insert(s.encode('utf-8'))
    
    def contains(self, data: bytes) -> bool:
        """
        Check if an item might be in the filter.
        
        Args:
            data: Item to check as bytes
        
        Returns:
            True if item might be present (may be false positive)
            False if item is definitely not present
        
        Example:
            >>> cf = CuckooFilter(10000)
            >>> cf.insert(b"hello")
            True
            >>> cf.contains(b"hello")
            True
            >>> cf.contains(b"world")  # Might be False or True (FP)
            False
        """
        fp = self._fingerprint(data)
        i1 = self._hash1(data)
        i2 = self._alt_index(i1, fp)
        
        return self._contains_fp(i1, fp) or self._contains_fp(i2, fp)
    
    def contains_string(self, s: str) -> bool:
        """
        Check if a string might be in the filter.
        
        Args:
            s: String to check
        
        Returns:
            True if string might be present, False if definitely not
        """
        return self.contains(s.encode('utf-8'))
    
    def delete(self, data: bytes) -> bool:
        """
        Remove an item from the filter.
        
        Args:
            data: Item to remove as bytes
        
        Returns:
            True if item was found and removed, False if not found
        
        Note:
            Only delete items you know were inserted. Deleting non-existent
            items may cause false negatives for other items.
        
        Example:
            >>> cf = CuckooFilter(10000)
            >>> cf.insert(b"hello")
            True
            >>> cf.delete(b"hello")
            True
            >>> cf.contains(b"hello")
            False
        """
        fp = self._fingerprint(data)
        i1 = self._hash1(data)
        i2 = self._alt_index(i1, fp)
        
        if self._delete_fp(i1, fp):
            self._count -= 1
            return True
        if self._delete_fp(i2, fp):
            self._count -= 1
            return True
        return False
    
    def delete_string(self, s: str) -> bool:
        """
        Remove a string from the filter.
        
        Args:
            s: String to remove
        
        Returns:
            True if string was found and removed, False if not found
        """
        return self.delete(s.encode('utf-8'))
    
    def bulk_insert(self, items: List[bytes]) -> Tuple[int, bool]:
        """
        Insert multiple items at once.
        
        Args:
            items: List of items to insert
        
        Returns:
            Tuple of (number inserted, whether any failed)
        
        Example:
            >>> cf = CuckooFilter(10000)
            >>> items = [b"a", b"b", b"c"]
            >>> cf.bulk_insert(items)
            (3, False)
        """
        inserted = 0
        for item in items:
            if not self.insert(item):
                return inserted, True
            inserted += 1
        return inserted, False
    
    def bulk_insert_strings(self, items: List[str]) -> Tuple[int, bool]:
        """
        Insert multiple strings at once.
        
        Args:
            items: List of strings to insert
        
        Returns:
            Tuple of (number inserted, whether any failed)
        """
        inserted = 0
        for item in items:
            if not self.insert_string(item):
                return inserted, True
            inserted += 1
        return inserted, False
    
    def reset(self) -> None:
        """
        Clear all items from the filter.
        
        Example:
            >>> cf = CuckooFilter(10000)
            >>> cf.insert_string("test")
            True
            >>> cf.reset()
            >>> cf.count
            0
        """
        for bucket in self._buckets:
            for i in range(len(bucket)):
                bucket[i] = None
        self._count = 0
    
    def stats(self) -> Dict[str, Any]:
        """
        Get statistics about the filter.
        
        Returns:
            Dictionary with:
            - capacity: Total capacity
            - count: Number of items
            - load_factor: Fraction of slots used (0-1)
            - bucket_size: Entries per bucket
            - fingerprint_size: Size of fingerprints in bytes
            - expected_fp_rate: Expected false positive rate
            - memory_bytes: Approximate memory usage
        
        Example:
            >>> cf = CuckooFilter(10000)
            >>> cf.insert_string("test")
            True
            >>> stats = cf.stats()
            >>> stats['count']
            1
        """
        # Calculate expected FP rate: P = 1 - (1 - 1/2^f)^2b
        fp_bits = self._fp_size * 8
        prob_not_match = (1 - 1 / (2 ** fp_bits)) ** (2 * self._bucket_size)
        expected_fp = 1 - prob_not_match
        
        memory_bytes = self._num_buckets * self._bucket_size * self._fp_size
        
        return {
            'capacity': self._capacity,
            'count': self._count,
            'load_factor': self.load_factor,
            'bucket_size': self._bucket_size,
            'fingerprint_size': self._fp_size,
            'expected_fp_rate': expected_fp,
            'memory_bytes': memory_bytes,
        }
    
    def to_json(self) -> str:
        """
        Serialize filter to JSON string.
        
        Returns:
            JSON representation of the filter
        
        Example:
            >>> cf = CuckooFilter(10000)
            >>> cf.insert_string("test")
            True
            >>> data = cf.to_json()
            >>> len(data) > 0
            True
        """
        # Convert None to -1 for JSON serialization
        buckets_serialized = []
        for bucket in self._buckets:
            bucket_serialized = [fp if fp is not None else -1 for fp in bucket]
            buckets_serialized.append(bucket_serialized)
        
        data = {
            'buckets': buckets_serialized,
            'bucket_size': self._bucket_size,
            'fp_size': self._fp_size,
            'max_kicks': self._max_kicks,
            'num_buckets': self._num_buckets,
            'count': self._count,
            'capacity': self._capacity,
        }
        return json.dumps(data)
    
    @classmethod
    def from_json(cls, data: str) -> 'CuckooFilter':
        """
        Deserialize filter from JSON string.
        
        Args:
            data: JSON string representation
        
        Returns:
            New CuckooFilter instance
        
        Example:
            >>> cf1 = CuckooFilter(10000)
            >>> cf1.insert_string("test")
            True
            >>> data = cf1.to_json()
            >>> cf2 = CuckooFilter.from_json(data)
            >>> cf2.contains_string("test")
            True
        """
        obj = json.loads(data)
        
        # Create a minimal filter, then restore state
        cf = cls.__new__(cls)
        cf._bucket_size = obj['bucket_size']
        cf._fp_size = obj['fp_size']
        cf._max_kicks = obj['max_kicks']
        cf._num_buckets = obj['num_buckets']
        cf._count = obj['count']
        cf._capacity = obj['capacity']
        
        # Convert -1 back to None
        cf._buckets = []
        for bucket_serialized in obj['buckets']:
            bucket = [fp if fp != -1 else None for fp in bucket_serialized]
            cf._buckets.append(bucket)
        
        return cf
    
    def clone(self) -> 'CuckooFilter':
        """
        Create a deep copy of the filter.
        
        Returns:
            New CuckooFilter with same state
        
        Example:
            >>> cf1 = CuckooFilter(10000)
            >>> cf1.insert_string("test")
            True
            >>> cf2 = cf1.clone()
            >>> cf2.contains_string("test")
            True
        """
        return self.from_json(self.to_json())
    
    def __repr__(self) -> str:
        stats = self.stats()
        return f"CuckooFilter(count={stats['count']}, capacity={stats['capacity']}, " \
               f"load_factor={stats['load_factor']:.2%}, fp_rate={stats['expected_fp_rate']:.4%})"
    
    def __len__(self) -> int:
        return self._count
    
    def __contains__(self, item: bytes) -> bool:
        return self.contains(item)


def create_optimal_filter(expected_items: int, fp_rate: float = 0.01) -> CuckooFilter:
    """
    Create a Cuckoo filter optimized for given parameters.
    
    Args:
        expected_items: Expected number of items to store
        fp_rate: Desired false positive rate
    
    Returns:
        Optimized CuckooFilter instance
    
    Example:
        >>> cf = create_optimal_filter(100000, 0.001)
        >>> cf.capacity > 100000
        True
    """
    return CuckooFilter(expected_items, fp_rate=fp_rate)


def calculate_false_positive_rate(fp_bits: int, bucket_size: int) -> float:
    """
    Calculate the theoretical false positive rate.
    
    Args:
        fp_bits: Fingerprint size in bits
        bucket_size: Number of entries per bucket
    
    Returns:
        False positive rate as fraction
    
    Example:
        >>> rate = calculate_false_positive_rate(8, 4)
        >>> rate > 0
        True
    """
    prob_not_match = (1 - 1 / (2 ** fp_bits)) ** (2 * bucket_size)
    return 1 - prob_not_match