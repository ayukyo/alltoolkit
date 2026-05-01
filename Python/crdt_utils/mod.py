#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - CRDT (Conflict-free Replicated Data Types) Utilities Module
=========================================================================
A comprehensive CRDT implementation for distributed systems.
Zero external dependencies - pure Python implementation.

Features:
    - G-Counter (Grow-only Counter)
    - PN-Counter (Positive-Negative Counter)
    - G-Set (Grow-only Set)
    - 2P-Set (Two-Phase Set)
    - LWW-Register (Last-Writer-Wins Register)
    - OR-Set (Observed-Remove Set)
    - Vector Clock
    - LWW-Element-Set
    - CRDT Map (Conflict-free Map)

CRDTs are used in:
    - Distributed databases (Redis CRDB, Riak, Cassandra)
    - Collaborative editing (Google Docs-style)
    - Distributed counters and sets
    - Offline-first applications
    - Multi-master replication systems

Author: AllToolkit Contributors
License: MIT
"""

from typing import (
    Dict, Set, List, Tuple, Optional, Any, 
    Generic, TypeVar, Iterator, Callable,
    Mapping, MutableMapping
)
from dataclasses import dataclass, field
from copy import deepcopy
from abc import ABC, abstractmethod
import time
import hashlib
import json

# ============================================================================
# Type Variables
# ============================================================================

T = TypeVar('T')
K = TypeVar('K')
V = TypeVar('V')


# ============================================================================
# Abstract Base Class
# ============================================================================

class CRDT(ABC):
    """Abstract base class for all CRDTs."""
    
    @abstractmethod
    def merge(self, other: 'CRDT') -> 'CRDT':
        """
        Merge with another CRDT of the same type.
        
        The merge operation must be:
        - Commutative: merge(a, b) == merge(b, a)
        - Associative: merge(merge(a, b), c) == merge(a, merge(b, c))
        - Idempotent: merge(a, a) == a
        """
        pass
    
    @abstractmethod
    def clone(self) -> 'CRDT':
        """Create a deep copy of this CRDT."""
        pass
    
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        pass
    
    @classmethod
    @abstractmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CRDT':
        """Deserialize from dictionary."""
        pass
    
    def equals(self, other: 'CRDT') -> bool:
        """Check equality with another CRDT."""
        return self.to_dict() == other.to_dict()
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, CRDT):
            return self.equals(other)
        return False


# ============================================================================
# Vector Clock
# ============================================================================

@dataclass
class VectorClock(CRDT):
    """
    Vector Clock for tracking causality in distributed systems.
    
    A vector clock maintains a counter for each node/process,
    allowing partial ordering of events across distributed systems.
    
    Example:
        >>> vc1 = VectorClock({'A': 1, 'B': 2})
        >>> vc2 = VectorClock({'A': 2, 'C': 1})
        >>> vc1.merge(vc2)
        VectorClock({'A': 2, 'B': 2, 'C': 1})
    """
    
    clocks: Dict[str, int] = field(default_factory=dict)
    
    def increment(self, node_id: str) -> 'VectorClock':
        """
        Increment the counter for a node.
        
        Args:
            node_id: Node identifier
            
        Returns:
            New vector clock with incremented value
        """
        new_clocks = dict(self.clocks)
        new_clocks[node_id] = new_clocks.get(node_id, 0) + 1
        return VectorClock(new_clocks)
    
    def get(self, node_id: str) -> int:
        """Get the counter value for a node."""
        return self.clocks.get(node_id, 0)
    
    def merge(self, other: 'CRDT') -> 'VectorClock':
        """
        Merge with another vector clock.
        Takes the maximum value for each node.
        """
        if not isinstance(other, VectorClock):
            raise TypeError(f"Cannot merge VectorClock with {type(other)}")
        
        all_nodes = set(self.clocks.keys()) | set(other.clocks.keys())
        merged = {
            node: max(self.get(node), other.get(node))
            for node in all_nodes
        }
        return VectorClock(merged)
    
    def compare(self, other: 'VectorClock') -> str:
        """
        Compare two vector clocks.
        
        Returns:
            'before': self happens before other
            'after': self happens after other
            'concurrent': self and other are concurrent (no causal relationship)
            'equal': self and other are equal
        """
        if self.clocks == other.clocks:
            return 'equal'
        
        all_nodes = set(self.clocks.keys()) | set(other.clocks.keys())
        
        self_less = False
        other_less = False
        
        for node in all_nodes:
            self_val = self.get(node)
            other_val = other.get(node)
            
            if self_val < other_val:
                self_less = True
            elif self_val > other_val:
                other_less = True
        
        if self_less and not other_less:
            return 'before'
        if other_less and not self_less:
            return 'after'
        return 'concurrent'
    
    def happens_before(self, other: 'VectorClock') -> bool:
        """Check if this clock happens before another."""
        return self.compare(other) == 'before'
    
    def concurrent_with(self, other: 'VectorClock') -> bool:
        """Check if this clock is concurrent with another."""
        return self.compare(other) == 'concurrent'
    
    def clone(self) -> 'VectorClock':
        return VectorClock(dict(self.clocks))
    
    def to_dict(self) -> Dict[str, Any]:
        return {'clocks': dict(self.clocks)}
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'VectorClock':
        return cls(dict(data.get('clocks', {})))
    
    def __repr__(self) -> str:
        return f"VectorClock({self.clocks})"
    
    def __hash__(self) -> int:
        return hash(tuple(sorted(self.clocks.items())))


# ============================================================================
# G-Counter (Grow-only Counter)
# ============================================================================

@dataclass
class GCounter(CRDT):
    """
    Grow-only Counter (G-Counter).
    
    A counter that can only be incremented. Each node maintains its own
    counter, and the total is the sum of all node counters.
    
    Properties:
        - Can only increment (never decrement)
        - Eventually consistent across all nodes
        - Monotonically increasing
    
    Example:
        >>> counter = GCounter(node_id='A')
        >>> counter.increment()
        >>> counter.increment()
        >>> counter.value
        2
    """
    
    node_id: str
    counters: Dict[str, int] = field(default_factory=dict)
    
    def __post_init__(self):
        if self.node_id not in self.counters:
            self.counters[self.node_id] = 0
    
    @property
    def value(self) -> int:
        """Get the total counter value."""
        return sum(self.counters.values())
    
    def increment(self, amount: int = 1) -> 'GCounter':
        """
        Increment the counter.
        
        Args:
            amount: Amount to increment (must be positive)
            
        Returns:
            New counter with incremented value
        """
        if amount < 0:
            raise ValueError("G-Counter can only increment, not decrement")
        
        new_counters = dict(self.counters)
        new_counters[self.node_id] = new_counters.get(self.node_id, 0) + amount
        return GCounter(self.node_id, new_counters)
    
    def merge(self, other: 'CRDT') -> 'GCounter':
        """Merge with another G-Counter by taking max of each counter."""
        if not isinstance(other, GCounter):
            raise TypeError(f"Cannot merge GCounter with {type(other)}")
        
        all_nodes = set(self.counters.keys()) | set(other.counters.keys())
        merged = {
            node: max(self.counters.get(node, 0), other.counters.get(node, 0))
            for node in all_nodes
        }
        return GCounter(self.node_id, merged)
    
    def clone(self) -> 'GCounter':
        return GCounter(self.node_id, dict(self.counters))
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'node_id': self.node_id,
            'counters': dict(self.counters)
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'GCounter':
        return cls(
            node_id=data['node_id'],
            counters=dict(data.get('counters', {}))
        )
    
    def __repr__(self) -> str:
        return f"GCounter(value={self.value}, node={self.node_id})"


# ============================================================================
# PN-Counter (Positive-Negative Counter)
# ============================================================================

@dataclass
class PNCounter(CRDT):
    """
    Positive-Negative Counter (PN-Counter).
    
    A counter that supports both increment and decrement operations.
    Implemented using two G-Counters (one for increments, one for decrements).
    
    Properties:
        - Supports increment and decrement
        - Eventually consistent
        - May have negative values
    
    Example:
        >>> counter = PNCounter(node_id='A')
        >>> counter.increment(5)
        >>> counter.decrement(2)
        >>> counter.value
        3
    """
    
    node_id: str
    p_counters: Dict[str, int] = field(default_factory=dict)  # increments
    n_counters: Dict[str, int] = field(default_factory=dict)  # decrements
    
    def __post_init__(self):
        if self.node_id not in self.p_counters:
            self.p_counters[self.node_id] = 0
        if self.node_id not in self.n_counters:
            self.n_counters[self.node_id] = 0
    
    @property
    def value(self) -> int:
        """Get the total counter value (increments - decrements)."""
        return sum(self.p_counters.values()) - sum(self.n_counters.values())
    
    def increment(self, amount: int = 1) -> 'PNCounter':
        """Increment the counter."""
        if amount < 0:
            raise ValueError("Amount must be non-negative")
        
        new_p = dict(self.p_counters)
        new_p[self.node_id] = new_p.get(self.node_id, 0) + amount
        return PNCounter(self.node_id, new_p, dict(self.n_counters))
    
    def decrement(self, amount: int = 1) -> 'PNCounter':
        """Decrement the counter."""
        if amount < 0:
            raise ValueError("Amount must be non-negative")
        
        new_n = dict(self.n_counters)
        new_n[self.node_id] = new_n.get(self.node_id, 0) + amount
        return PNCounter(self.node_id, dict(self.p_counters), new_n)
    
    def merge(self, other: 'CRDT') -> 'PNCounter':
        """Merge with another PN-Counter."""
        if not isinstance(other, PNCounter):
            raise TypeError(f"Cannot merge PNCounter with {type(other)}")
        
        all_nodes = set(self.p_counters.keys()) | set(other.p_counters.keys())
        
        merged_p = {
            node: max(self.p_counters.get(node, 0), other.p_counters.get(node, 0))
            for node in all_nodes
        }
        merged_n = {
            node: max(self.n_counters.get(node, 0), other.n_counters.get(node, 0))
            for node in all_nodes
        }
        
        return PNCounter(self.node_id, merged_p, merged_n)
    
    def clone(self) -> 'PNCounter':
        return PNCounter(
            self.node_id,
            dict(self.p_counters),
            dict(self.n_counters)
        )
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'node_id': self.node_id,
            'p_counters': dict(self.p_counters),
            'n_counters': dict(self.n_counters)
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PNCounter':
        return cls(
            node_id=data['node_id'],
            p_counters=dict(data.get('p_counters', {})),
            n_counters=dict(data.get('n_counters', {}))
        )
    
    def __repr__(self) -> str:
        return f"PNCounter(value={self.value}, node={self.node_id})"


# ============================================================================
# G-Set (Grow-only Set)
# ============================================================================

class GSet(Generic[T], CRDT):
    """
    Grow-only Set (G-Set).
    
    A set that only supports add operations. Elements can never be removed.
    
    Properties:
        - Can only add elements (no removal)
        - Set union for merge
        - Eventually consistent
    
    Example:
        >>> s = GSet[int]()
        >>> s = s.add(1).add(2).add(3)
        >>> 2 in s
        True
        >>> s.value
        {1, 2, 3}
    """
    
    def __init__(self, elements: Optional[Set[T]] = None):
        self._elements: Set[T] = set(elements) if elements else set()
    
    @property
    def value(self) -> Set[T]:
        """Get the set of elements."""
        return set(self._elements)
    
    def add(self, element: T) -> 'GSet[T]':
        """Add an element to the set."""
        new_elements = set(self._elements)
        new_elements.add(element)
        return GSet(new_elements)
    
    def __contains__(self, element: T) -> bool:
        return element in self._elements
    
    def __len__(self) -> int:
        return len(self._elements)
    
    def __iter__(self) -> Iterator[T]:
        return iter(self._elements)
    
    def merge(self, other: 'CRDT') -> 'GSet[T]':
        """Merge with another G-Set using set union."""
        if not isinstance(other, GSet):
            raise TypeError(f"Cannot merge GSet with {type(other)}")
        return GSet(self._elements | other._elements)
    
    def clone(self) -> 'GSet[T]':
        return GSet(set(self._elements))
    
    def to_dict(self) -> Dict[str, Any]:
        return {'elements': list(self._elements)}
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'GSet[T]':
        return cls(set(data.get('elements', [])))
    
    def __repr__(self) -> str:
        return f"GSet({self._elements})"
    
    def __hash__(self) -> int:
        return hash(frozenset(self._elements))


# ============================================================================
# 2P-Set (Two-Phase Set)
# ============================================================================

class TwoPSet(Generic[T], CRDT):
    """
    Two-Phase Set (2P-Set).
    
    A set that supports both add and remove operations using two G-Sets.
    Once an element is removed, it cannot be re-added.
    
    Properties:
        - Supports add and remove
        - Removed elements cannot be re-added
        - Uses add set and remove set (tombstones)
    
    Example:
        >>> s = TwoPSet[int]()
        >>> s = s.add(1).add(2).remove(1)
        >>> 1 in s
        False
        >>> 2 in s
        True
    """
    
    def __init__(
        self,
        add_set: Optional[Set[T]] = None,
        remove_set: Optional[Set[T]] = None
    ):
        self._add_set: Set[T] = set(add_set) if add_set else set()
        self._remove_set: Set[T] = set(remove_set) if remove_set else set()
    
    @property
    def value(self) -> Set[T]:
        """Get the set of elements (add_set - remove_set)."""
        return self._add_set - self._remove_set
    
    def add(self, element: T) -> 'TwoPSet[T]':
        """Add an element to the set."""
        new_add = set(self._add_set)
        new_add.add(element)
        return TwoPSet(new_add, set(self._remove_set))
    
    def remove(self, element: T) -> 'TwoPSet[T]':
        """Remove an element from the set (adds to tombstone set)."""
        new_remove = set(self._remove_set)
        new_remove.add(element)
        return TwoPSet(set(self._add_set), new_remove)
    
    def __contains__(self, element: T) -> bool:
        return element in self._add_set and element not in self._remove_set
    
    def __len__(self) -> int:
        return len(self.value)
    
    def __iter__(self) -> Iterator[T]:
        return iter(self.value)
    
    def merge(self, other: 'CRDT') -> 'TwoPSet[T]':
        """Merge with another 2P-Set."""
        if not isinstance(other, TwoPSet):
            raise TypeError(f"Cannot merge TwoPSet with {type(other)}")
        
        return TwoPSet(
            self._add_set | other._add_set,
            self._remove_set | other._remove_set
        )
    
    def clone(self) -> 'TwoPSet[T]':
        return TwoPSet(set(self._add_set), set(self._remove_set))
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'add_set': list(self._add_set),
            'remove_set': list(self._remove_set)
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TwoPSet[T]':
        return cls(
            add_set=set(data.get('add_set', [])),
            remove_set=set(data.get('remove_set', []))
        )
    
    def __repr__(self) -> str:
        return f"TwoPSet(value={self.value}, removed={self._remove_set})"


# ============================================================================
# LWW-Register (Last-Writer-Wins Register)
# ============================================================================

@dataclass
class LWWRegister(Generic[T], CRDT):
    """
    Last-Writer-Wins Register (LWW-Register).
    
    A register that stores a single value with a timestamp.
    On conflict, the value with the latest timestamp wins.
    
    Properties:
        - Stores a single value
        - Timestamp-based conflict resolution
        - Supports arbitrary values
    
    Example:
        >>> reg = LWWRegister[str](node_id='A')
        >>> reg = reg.set('hello')
        >>> reg = reg.set('world')
        >>> reg.value
        'world'
    """
    
    node_id: str
    value: Optional[T] = None
    timestamp: float = 0.0
    
    def set(self, value: T, timestamp: Optional[float] = None) -> 'LWWRegister[T]':
        """
        Set a new value.
        
        Args:
            value: The value to set
            timestamp: Optional timestamp (defaults to current time)
            
        Returns:
            New register with updated value
        """
        ts = timestamp if timestamp is not None else time.time()
        return LWWRegister(self.node_id, value, ts)
    
    def merge(self, other: 'CRDT') -> 'LWWRegister[T]':
        """Merge with another LWW-Register (latest timestamp wins)."""
        if not isinstance(other, LWWRegister):
            raise TypeError(f"Cannot merge LWWRegister with {type(other)}")
        
        if self.timestamp >= other.timestamp:
            return LWWRegister(self.node_id, self.value, self.timestamp)
        return LWWRegister(self.node_id, other.value, other.timestamp)
    
    def clone(self) -> 'LWWRegister[T]':
        return LWWRegister(self.node_id, self.value, self.timestamp)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'node_id': self.node_id,
            'value': self.value,
            'timestamp': self.timestamp
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'LWWRegister[T]':
        return cls(
            node_id=data['node_id'],
            value=data.get('value'),
            timestamp=data.get('timestamp', 0.0)
        )
    
    def __repr__(self) -> str:
        return f"LWWRegister(value={self.value!r}, ts={self.timestamp})"


# ============================================================================
# OR-Set (Observed-Remove Set)
# ============================================================================

class ORSet(Generic[T], CRDT):
    """
    Observed-Remove Set (OR-Set).
    
    A set that supports both add and remove operations.
    Each element is tagged with a unique identifier, allowing re-addition
    after removal.
    
    Properties:
        - Supports add and remove
        - Elements can be re-added after removal
        - Uses unique tags for each add operation
    
    Example:
        >>> s = ORSet[str](node_id='A')
        >>> s = s.add('x').add('y').remove('x').add('x')
        >>> 'x' in s
        True
    """
    
    def __init__(
        self,
        node_id: str,
        elements: Optional[Dict[T, Set[str]]] = None
    ):
        self.node_id = node_id
        # elements: {element: set of unique tags}
        self._elements: Dict[T, Set[str]] = {}
        if elements:
            for elem, tags in elements.items():
                self._elements[elem] = set(tags)
    
    def _generate_tag(self) -> str:
        """Generate a unique tag for an element."""
        return f"{self.node_id}:{time.time()}:{hash(time.time()) % 10000}"
    
    @property
    def value(self) -> Set[T]:
        """Get the set of elements."""
        return set(self._elements.keys())
    
    def add(self, element: T) -> 'ORSet[T]':
        """Add an element with a unique tag."""
        new_elements = {k: set(v) for k, v in self._elements.items()}
        if element not in new_elements:
            new_elements[element] = set()
        new_elements[element].add(self._generate_tag())
        return ORSet(self.node_id, new_elements)
    
    def remove(self, element: T) -> 'ORSet[T]':
        """Remove an element (removes all tags for this element)."""
        new_elements = {k: set(v) for k, v in self._elements.items()}
        if element in new_elements:
            del new_elements[element]
        return ORSet(self.node_id, new_elements)
    
    def __contains__(self, element: T) -> bool:
        return element in self._elements
    
    def __len__(self) -> int:
        return len(self._elements)
    
    def __iter__(self) -> Iterator[T]:
        return iter(self._elements)
    
    def merge(self, other: 'CRDT') -> 'ORSet[T]':
        """
        Merge with another OR-Set.
        
        Union of tags for each element.
        """
        if not isinstance(other, ORSet):
            raise TypeError(f"Cannot merge ORSet with {type(other)}")
        
        merged: Dict[T, Set[str]] = {}
        
        # Add all elements from self
        for elem, tags in self._elements.items():
            merged[elem] = set(tags)
        
        # Add all elements from other
        for elem, tags in other._elements.items():
            if elem in merged:
                merged[elem] |= tags
            else:
                merged[elem] = set(tags)
        
        return ORSet(self.node_id, merged)
    
    def clone(self) -> 'ORSet[T]':
        return ORSet(
            self.node_id,
            {k: set(v) for k, v in self._elements.items()}
        )
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'node_id': self.node_id,
            'elements': {str(k): list(v) for k, v in self._elements.items()}
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ORSet[T]':
        elements = {}
        for k, v in data.get('elements', {}).items():
            elements[k] = set(v)
        return cls(node_id=data['node_id'], elements=elements)
    
    def __repr__(self) -> str:
        return f"ORSet({self.value}, node={self.node_id})"


# ============================================================================
# LWW-Element-Set
# ============================================================================

class LWWElementSet(Generic[T], CRDT):
    """
    Last-Writer-Wins Element Set.
    
    A set that uses timestamps for both add and remove operations.
    When merging, the operation with the latest timestamp wins.
    
    Properties:
        - Supports add and remove with timestamps
        - Can re-add elements after removal
        - Timestamp-based conflict resolution
    
    Example:
        >>> s = LWWElementSet[str](node_id='A')
        >>> s = s.add('x')
        >>> s = s.remove('x')
        >>> 'x' in s
        False
    """
    
    def __init__(
        self,
        node_id: str,
        add_set: Optional[Dict[T, float]] = None,
        remove_set: Optional[Dict[T, float]] = None
    ):
        self.node_id = node_id
        self._add_set: Dict[T, float] = dict(add_set) if add_set else {}
        self._remove_set: Dict[T, float] = dict(remove_set) if remove_set else {}
    
    @property
    def value(self) -> Set[T]:
        """Get the set of elements (added but not removed)."""
        result = set()
        for elem, add_time in self._add_set.items():
            remove_time = self._remove_set.get(elem, 0)
            if add_time > remove_time:
                result.add(elem)
        return result
    
    def add(self, element: T, timestamp: Optional[float] = None) -> 'LWWElementSet[T]':
        """Add an element."""
        ts = timestamp if timestamp is not None else time.time()
        new_add = dict(self._add_set)
        new_add[element] = ts
        return LWWElementSet(self.node_id, new_add, dict(self._remove_set))
    
    def remove(self, element: T, timestamp: Optional[float] = None) -> 'LWWElementSet[T]':
        """Remove an element."""
        ts = timestamp if timestamp is not None else time.time()
        new_remove = dict(self._remove_set)
        new_remove[element] = ts
        return LWWElementSet(self.node_id, dict(self._add_set), new_remove)
    
    def __contains__(self, element: T) -> bool:
        add_time = self._add_set.get(element, 0)
        remove_time = self._remove_set.get(element, 0)
        return add_time > remove_time
    
    def __len__(self) -> int:
        return len(self.value)
    
    def __iter__(self) -> Iterator[T]:
        return iter(self.value)
    
    def merge(self, other: 'CRDT') -> 'LWWElementSet[T]':
        """Merge with another LWW-Element-Set."""
        if not isinstance(other, LWWElementSet):
            raise TypeError(f"Cannot merge LWWElementSet with {type(other)}")
        
        # Merge add sets - take latest timestamp
        new_add = dict(self._add_set)
        for elem, ts in other._add_set.items():
            if elem not in new_add or ts > new_add[elem]:
                new_add[elem] = ts
        
        # Merge remove sets - take latest timestamp
        new_remove = dict(self._remove_set)
        for elem, ts in other._remove_set.items():
            if elem not in new_remove or ts > new_remove[elem]:
                new_remove[elem] = ts
        
        return LWWElementSet(self.node_id, new_add, new_remove)
    
    def clone(self) -> 'LWWElementSet[T]':
        return LWWElementSet(
            self.node_id,
            dict(self._add_set),
            dict(self._remove_set)
        )
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'node_id': self.node_id,
            'add_set': {str(k): v for k, v in self._add_set.items()},
            'remove_set': {str(k): v for k, v in self._remove_set.items()}
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'LWWElementSet[T]':
        return cls(
            node_id=data['node_id'],
            add_set=data.get('add_set', {}),
            remove_set=data.get('remove_set', {})
        )
    
    def __repr__(self) -> str:
        return f"LWWElementSet({self.value}, node={self.node_id})"


# ============================================================================
# CRDT Map
# ============================================================================

class CRDTMap(Generic[K, V], CRDT):
    """
    Conflict-free Replicated Data Type Map.
    
    A map/dictionary that supports CRDT values. Each key maps to a CRDT
    value, and conflicts are resolved by merging the values.
    
    Properties:
        - Key-value store with CRDT values
        - Supports add, update, remove operations
        - Merge by combining entries
    
    Example:
        >>> m = CRDTMap[str, GCounter](node_id='A')
        >>> counter = GCounter('A')
        >>> counter = counter.increment()
        >>> m = m.set('views', counter)
        >>> m.get('views').value
        1
    """
    
    def __init__(
        self,
        node_id: str,
        entries: Optional[Dict[K, CRDT]] = None
    ):
        self.node_id = node_id
        self._entries: Dict[K, CRDT] = dict(entries) if entries else {}
    
    def get(self, key: K) -> Optional[CRDT]:
        """Get the value for a key."""
        return self._entries.get(key)
    
    def set(self, key: K, value: CRDT) -> 'CRDTMap[K, V]':
        """Set a value for a key."""
        new_entries = dict(self._entries)
        new_entries[key] = value
        return CRDTMap(self.node_id, new_entries)
    
    def delete(self, key: K) -> 'CRDTMap[K, V]':
        """Delete a key from the map."""
        new_entries = dict(self._entries)
        if key in new_entries:
            del new_entries[key]
        return CRDTMap(self.node_id, new_entries)
    
    def __contains__(self, key: K) -> bool:
        return key in self._entries
    
    def __len__(self) -> int:
        return len(self._entries)
    
    def __iter__(self) -> Iterator[K]:
        return iter(self._entries)
    
    def keys(self) -> Set[K]:
        """Get all keys."""
        return set(self._entries.keys())
    
    def values(self) -> List[CRDT]:
        """Get all values."""
        return list(self._entries.values())
    
    def items(self) -> Iterator[Tuple[K, CRDT]]:
        """Get all key-value pairs."""
        return iter(self._entries.items())
    
    def merge(self, other: 'CRDT') -> 'CRDTMap[K, V]':
        """Merge with another CRDT Map."""
        if not isinstance(other, CRDTMap):
            raise TypeError(f"Cannot merge CRDTMap with {type(other)}")
        
        merged = dict(self._entries)
        
        for key, value in other._entries.items():
            if key in merged:
                merged[key] = merged[key].merge(value)
            else:
                merged[key] = value.clone()
        
        return CRDTMap(self.node_id, merged)
    
    def clone(self) -> 'CRDTMap[K, V]':
        return CRDTMap(
            self.node_id,
            {k: v.clone() for k, v in self._entries.items()}
        )
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'node_id': self.node_id,
            'entries': {str(k): v.to_dict() for k, v in self._entries.items()}
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CRDTMap[K, V]':
        # Note: This requires knowing the CRDT types for values
        return cls(node_id=data['node_id'], entries={})
    
    def __repr__(self) -> str:
        return f"CRDTMap(keys={set(self._entries.keys())}, node={self.node_id})"


# ============================================================================
# JSON CRDT (JSON-compatible CRDT)
# ============================================================================

class JSONCRDT(CRDT):
    """
    JSON-compatible CRDT that can store nested JSON-like data.
    
    Supports:
        - Strings (LWW-Register)
        - Numbers (PN-Counter or LWW-Register)
        - Booleans (LWW-Register)
        - Null
        - Arrays (OR-Set based)
        - Objects (CRDT-Map based)
    
    Example:
        >>> data = JSONCRDT(node_id='A')
        >>> data = data.set_path(['user', 'name'], 'Alice')
        >>> data = data.set_path(['user', 'age'], 30)
        >>> data.get_path(['user', 'name'])
        'Alice'
    """
    
    def __init__(
        self,
        node_id: str,
        data: Optional[Dict[str, Any]] = None,
        timestamps: Optional[Dict[str, float]] = None
    ):
        self.node_id = node_id
        self._data: Dict[str, Any] = dict(data) if data else {}
        self._timestamps: Dict[str, float] = dict(timestamps) if timestamps else {}
    
    def _path_to_key(self, path: List[str]) -> str:
        """Convert path list to string key."""
        return '.'.join(str(p) for p in path)
    
    def get(self, key: str) -> Any:
        """Get a value by key."""
        return self._data.get(key)
    
    def get_path(self, path: List[str]) -> Any:
        """Get a value by path."""
        key = self._path_to_key(path)
        return self._data.get(key)
    
    def set(self, key: str, value: Any) -> 'JSONCRDT':
        """Set a value by key."""
        new_data = dict(self._data)
        new_timestamps = dict(self._timestamps)
        
        new_data[key] = deepcopy(value)
        new_timestamps[key] = time.time()
        
        return JSONCRDT(self.node_id, new_data, new_timestamps)
    
    def set_path(self, path: List[str], value: Any) -> 'JSONCRDT':
        """Set a value by path."""
        return self.set(self._path_to_key(path), value)
    
    def delete(self, key: str) -> 'JSONCRDT':
        """Delete a key."""
        new_data = dict(self._data)
        new_timestamps = dict(self._timestamps)
        
        if key in new_data:
            del new_data[key]
            del new_timestamps[key]
        
        return JSONCRDT(self.node_id, new_data, new_timestamps)
    
    def delete_path(self, path: List[str]) -> 'JSONCRDT':
        """Delete by path."""
        return self.delete(self._path_to_key(path))
    
    @property
    def value(self) -> Dict[str, Any]:
        """Get all data."""
        return dict(self._data)
    
    def __contains__(self, key: str) -> bool:
        return key in self._data
    
    def __len__(self) -> int:
        return len(self._data)
    
    def merge(self, other: 'CRDT') -> 'JSONCRDT':
        """Merge with another JSONCRDT (LWW semantics for each key)."""
        if not isinstance(other, JSONCRDT):
            raise TypeError(f"Cannot merge JSONCRDT with {type(other)}")
        
        merged_data = dict(self._data)
        merged_timestamps = dict(self._timestamps)
        
        for key, value in other._data.items():
            other_ts = other._timestamps.get(key, 0)
            self_ts = self._timestamps.get(key, 0)
            
            if other_ts > self_ts:
                merged_data[key] = deepcopy(value)
                merged_timestamps[key] = other_ts
        
        return JSONCRDT(self.node_id, merged_data, merged_timestamps)
    
    def clone(self) -> 'JSONCRDT':
        return JSONCRDT(
            self.node_id,
            deepcopy(self._data),
            dict(self._timestamps)
        )
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'node_id': self.node_id,
            'data': deepcopy(self._data),
            'timestamps': dict(self._timestamps)
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'JSONCRDT':
        return cls(
            node_id=data['node_id'],
            data=data.get('data'),
            timestamps=data.get('timestamps')
        )
    
    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict())
    
    @classmethod
    def from_json(cls, json_str: str) -> 'JSONCRDT':
        """Create from JSON string."""
        return cls.from_dict(json.loads(json_str))
    
    def __repr__(self) -> str:
        return f"JSONCRDT(keys={len(self._data)}, node={self.node_id})"


# ============================================================================
# Utility Functions
# ============================================================================

def generate_node_id() -> str:
    """
    Generate a unique node ID.
    
    Returns:
        Unique node identifier string
    """
    import random
    import string
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choices(chars, k=8))


def crdt_hash(crdt: CRDT) -> str:
    """
    Generate a hash of a CRDT for comparison.
    
    Args:
        crdt: CRDT instance
        
    Returns:
        SHA-256 hash string
    """
    data = json.dumps(crdt.to_dict(), sort_keys=True)
    return hashlib.sha256(data.encode()).hexdigest()


def merge_all(crdts: List[CRDT]) -> CRDT:
    """
    Merge multiple CRDTs of the same type.
    
    Args:
        crdts: List of CRDTs to merge
        
    Returns:
        Merged CRDT
        
    Raises:
        ValueError: If list is empty
        TypeError: If CRDTs are not of the same type
    """
    if not crdts:
        raise ValueError("Cannot merge empty list of CRDTs")
    
    result = crdts[0].clone()
    for crdt in crdts[1:]:
        result = result.merge(crdt)
    
    return result


# ============================================================================
# Exports
# ============================================================================

__all__ = [
    # Base
    'CRDT',
    # Data Structures
    'VectorClock',
    'GCounter',
    'PNCounter',
    'GSet',
    'TwoPSet',
    'LWWRegister',
    'ORSet',
    'LWWElementSet',
    'CRDTMap',
    'JSONCRDT',
    # Utilities
    'generate_node_id',
    'crdt_hash',
    'merge_all',
]