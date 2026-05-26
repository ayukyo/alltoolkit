"""
Vector Clock Utilities - 向量时钟工具

A comprehensive toolkit for working with vector clocks in distributed systems.
Zero external dependencies - pure Python implementation.

Vector clocks are a data structure used for capturing causality relationships
between events in distributed systems. They enable:
- Partial ordering of events
- Conflict detection
- Causal consistency
- Distributed snapshot algorithms

Features:
- VectorClock class with full comparison operations
- Event ordering (happens-before, concurrent, equal)
- Increment, merge, and compare operations
- Dotted version vectors for finer-grained tracking
- Serialization/deserialization (JSON, dict)
- Process ID management
- Conflict detection utilities

Author: AllToolkit
License: MIT
"""

from typing import Dict, List, Optional, Set, Tuple, Union, Any
from dataclasses import dataclass, field
from copy import deepcopy
import json


class VectorClock:
    """
    Vector Clock implementation for distributed systems.
    
    A vector clock is a vector of counters, one per process/node.
    Each process increments its own counter when an event occurs,
    and updates its vector to the element-wise maximum when receiving messages.
    
    Example:
        >>> vc1 = VectorClock({'A': 1, 'B': 0, 'C': 0})
        >>> vc2 = VectorClock({'A': 1, 'B': 2, 'C': 0})
        >>> vc1.happens_before(vc2)
        True
        >>> vc2.happens_before(vc1)
        False
    """
    
    def __init__(self, clock: Optional[Dict[str, int]] = None):
        """
        Initialize a vector clock.
        
        Args:
            clock: Optional initial clock state as a dict of process_id -> counter
        """
        self._clock: Dict[str, int] = dict(clock) if clock else {}
    
    @property
    def clock(self) -> Dict[str, int]:
        """Return a copy of the internal clock dictionary."""
        return dict(self._clock)
    
    def get(self, process_id: str) -> int:
        """
        Get the counter value for a process.
        
        Args:
            process_id: The process identifier
            
        Returns:
            Counter value (0 if process not in clock)
        """
        return self._clock.get(process_id, 0)
    
    def set(self, process_id: str, value: int) -> None:
        """
        Set the counter value for a process.
        
        Args:
            process_id: The process identifier
            value: The counter value to set
            
        Raises:
            ValueError: If value is negative
        """
        if value < 0:
            raise ValueError("Vector clock values must be non-negative")
        self._clock[process_id] = value
    
    def increment(self, process_id: str) -> 'VectorClock':
        """
        Increment the counter for a process (local event).
        
        Args:
            process_id: The process performing the event
            
        Returns:
            Self for chaining
        """
        self._clock[process_id] = self._clock.get(process_id, 0) + 1
        return self
    
    def merge(self, other: 'VectorClock') -> 'VectorClock':
        """
        Merge with another vector clock (receive message).
        
        This creates a new vector clock that is the element-wise maximum
        of both clocks, then increments the local process counter.
        
        Args:
            other: The other vector clock to merge with
            
        Returns:
            Self for chaining
        """
        for process_id, value in other._clock.items():
            self._clock[process_id] = max(self._clock.get(process_id, 0), value)
        return self
    
    def merge_new(self, other: 'VectorClock') -> 'VectorClock':
        """
        Create a new merged vector clock without modifying self.
        
        Args:
            other: The other vector clock to merge with
            
        Returns:
            New merged VectorClock
        """
        result = VectorClock(self._clock)
        result.merge(other)
        return result
    
    def happens_before(self, other: 'VectorClock') -> bool:
        """
        Check if this clock happens-before another (causality).
        
        A happens-before B if:
        - For all processes i: A[i] <= B[i]
        - There exists at least one process j: A[j] < B[j]
        
        Args:
            other: The other vector clock to compare with
            
        Returns:
            True if this clock happens-before other
        """
        at_least_one_less = False
        all_less_or_equal = True
        
        all_processes = set(self._clock.keys()) | set(other._clock.keys())
        
        for process_id in all_processes:
            self_val = self._clock.get(process_id, 0)
            other_val = other._clock.get(process_id, 0)
            
            if self_val > other_val:
                all_less_or_equal = False
                break
            elif self_val < other_val:
                at_least_one_less = True
        
        return all_less_or_equal and at_least_one_less
    
    def happens_after(self, other: 'VectorClock') -> bool:
        """
        Check if this clock happens-after another.
        
        Args:
            other: The other vector clock to compare with
            
        Returns:
            True if other happens-before this
        """
        return other.happens_before(self)
    
    def concurrent_with(self, other: 'VectorClock') -> bool:
        """
        Check if two events are concurrent (no causal relationship).
        
        Two events are concurrent if neither happens-before the other.
        
        Args:
            other: The other vector clock to compare with
            
        Returns:
            True if the events are concurrent
        """
        return not self.happens_before(other) and not other.happens_before(self) and self != other
    
    def __eq__(self, other: object) -> bool:
        """Check equality of vector clocks."""
        if not isinstance(other, VectorClock):
            return False
        return self._clock == other._clock
    
    def __lt__(self, other: 'VectorClock') -> bool:
        """Less than operator (happens-before)."""
        return self.happens_before(other)
    
    def __le__(self, other: 'VectorClock') -> bool:
        """Less than or equal operator."""
        return self == other or self < other
    
    def __gt__(self, other: 'VectorClock') -> bool:
        """Greater than operator (happens-after)."""
        return self.happens_after(other)
    
    def __ge__(self, other: 'VectorClock') -> bool:
        """Greater than or equal operator."""
        return self == other or self > other
    
    def __repr__(self) -> str:
        """String representation."""
        return f"VectorClock({self._clock})"
    
    def __str__(self) -> str:
        """Human-readable string representation."""
        if not self._clock:
            return "VC:{}"
        items = sorted(self._clock.items())
        return f"VC:{{{', '.join(f'{k}:{v}' for k, v in items)}}}"
    
    def __hash__(self) -> int:
        """Hash for use in sets and dicts."""
        return hash(tuple(sorted(self._clock.items())))
    
    def copy(self) -> 'VectorClock':
        """Create a deep copy of this vector clock."""
        return VectorClock(deepcopy(self._clock))
    
    def to_dict(self) -> Dict[str, int]:
        """Convert to dictionary."""
        return dict(self._clock)
    
    @classmethod
    def from_dict(cls, data: Dict[str, int]) -> 'VectorClock':
        """Create from dictionary."""
        return cls(data)
    
    def to_json(self) -> str:
        """Serialize to JSON string."""
        return json.dumps(self._clock)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'VectorClock':
        """Deserialize from JSON string."""
        return cls(json.loads(json_str))
    
    def processes(self) -> Set[str]:
        """Get the set of process IDs in this clock."""
        return set(self._clock.keys())
    
    def max_value(self) -> int:
        """Get the maximum counter value across all processes."""
        return max(self._clock.values()) if self._clock else 0
    
    def min_value(self) -> int:
        """Get the minimum counter value across all processes."""
        return min(self._clock.values()) if self._clock else 0
    
    def total(self) -> int:
        """Get the sum of all counter values."""
        return sum(self._clock.values())
    
    def is_empty(self) -> bool:
        """Check if the clock is empty (no events)."""
        return not self._clock or all(v == 0 for v in self._clock.values())
    
    def reset(self) -> 'VectorClock':
        """Reset all counters to zero."""
        self._clock = {k: 0 for k in self._clock}
        return self
    
    def clear(self) -> 'VectorClock':
        """Clear all process entries."""
        self._clock = {}
        return self
    
    def add_process(self, process_id: str, initial_value: int = 0) -> 'VectorClock':
        """
        Add a new process to the clock.
        
        Args:
            process_id: The new process identifier
            initial_value: Initial counter value (default 0)
            
        Returns:
            Self for chaining
        """
        if process_id not in self._clock:
            self._clock[process_id] = initial_value
        return self
    
    def remove_process(self, process_id: str) -> 'VectorClock':
        """
        Remove a process from the clock.
        
        Args:
            process_id: The process identifier to remove
            
        Returns:
            Self for chaining
        """
        self._clock.pop(process_id, None)
        return self


@dataclass
class DottedVersionVector:
    """
    Dotted Version Vector for finer-grained causality tracking.
    
    Unlike regular vector clocks, dotted version vectors can track
    causality of individual operations within a process, making them
    useful for conflict-free replicated data types (CRDTs) and
    distributed databases.
    
    Structure:
        - dot: (process_id, counter) - the unique identifier of this event
        - vector: the version vector tracking causality
    
    Example:
        >>> dvv = DottedVersionVector('A')
        >>> dvv.increment()  # Event at A
        DottedVersionVector(dot=('A', 1), vector={'A': 1})
    """
    
    process_id: str
    dot: Tuple[str, int] = field(default_factory=lambda: ('', 0))
    vector: Dict[str, int] = field(default_factory=dict)
    
    def __post_init__(self):
        """Initialize the dotted version vector."""
        if not self.vector:
            self.vector = {}
        if self.dot == ('', 0):
            self.dot = (self.process_id, 0)
    
    def increment(self) -> 'DottedVersionVector':
        """
        Increment and create a new dot for this process.
        
        Returns:
            Self for chaining
        """
        current = self.vector.get(self.process_id, 0) + 1
        self.vector[self.process_id] = current
        self.dot = (self.process_id, current)
        return self
    
    def merge(self, other: 'DottedVersionVector') -> 'DottedVersionVector':
        """
        Merge with another dotted version vector.
        
        Args:
            other: The other DVV to merge with
            
        Returns:
            Self for chaining
        """
        # Merge the vectors
        for pid, counter in other.vector.items():
            self.vector[pid] = max(self.vector.get(pid, 0), counter)
        
        # Update dot if needed
        if other.dot[1] > self.vector.get(other.dot[0], 0):
            self.vector[other.dot[0]] = other.dot[1]
            self.dot = other.dot
        
        return self
    
    def contains(self, dot: Tuple[str, int]) -> bool:
        """
        Check if a dot is contained in this version vector.
        
        Args:
            dot: (process_id, counter) tuple
            
        Returns:
            True if the dot is contained
        """
        process_id, counter = dot
        return self.vector.get(process_id, 0) >= counter
    
    def dominates(self, other: 'DottedVersionVector') -> bool:
        """
        Check if this DVV dominates another.
        
        Args:
            other: The other DVV to compare with
            
        Returns:
            True if this dominates other
        """
        for pid, counter in other.vector.items():
            if self.vector.get(pid, 0) < counter:
                return False
        return True
    
    def concurrent_with(self, other: 'DottedVersionVector') -> bool:
        """
        Check if two DVVs are concurrent.
        
        Args:
            other: The other DVV to compare with
            
        Returns:
            True if concurrent (neither dominates)
        """
        return not self.dominates(other) and not other.dominates(self)
    
    def to_vector_clock(self) -> VectorClock:
        """Convert to a regular VectorClock."""
        return VectorClock(dict(self.vector))
    
    @classmethod
    def from_vector_clock(cls, vc: VectorClock, process_id: str) -> 'DottedVersionVector':
        """Create from a VectorClock."""
        return cls(process_id=process_id, vector=dict(vc.clock))
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'process_id': self.process_id,
            'dot': list(self.dot),
            'vector': dict(self.vector)
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DottedVersionVector':
        """Create from dictionary."""
        return cls(
            process_id=data['process_id'],
            dot=tuple(data['dot']),
            vector=data['vector']
        )
    
    def __repr__(self) -> str:
        """String representation."""
        return f"DottedVersionVector(dot={self.dot}, vector={self.vector})"


def compare_events(clock1: VectorClock, clock2: VectorClock) -> str:
    """
    Compare two events and return their relationship.
    
    Args:
        clock1: First event's vector clock
        clock2: Second event's vector clock
        
    Returns:
        One of: 'before', 'after', 'concurrent', 'equal'
    
    Example:
        >>> vc1 = VectorClock({'A': 1})
        >>> vc2 = VectorClock({'A': 2})
        >>> compare_events(vc1, vc2)
        'before'
    """
    if clock1 == clock2:
        return 'equal'
    elif clock1.happens_before(clock2):
        return 'before'
    elif clock1.happens_after(clock2):
        return 'after'
    else:
        return 'concurrent'


def find_concurrent_events(clocks: List[VectorClock]) -> List[Tuple[int, int]]:
    """
    Find all pairs of concurrent events in a list.
    
    Args:
        clocks: List of vector clocks
        
    Returns:
        List of (i, j) tuples indicating concurrent pairs
    
    Example:
        >>> vc1 = VectorClock({'A': 1, 'B': 0})
        >>> vc2 = VectorClock({'A': 0, 'B': 1})
        >>> find_concurrent_events([vc1, vc2])
        [(0, 1)]
    """
    concurrent_pairs = []
    n = len(clocks)
    
    for i in range(n):
        for j in range(i + 1, n):
            if clocks[i].concurrent_with(clocks[j]):
                concurrent_pairs.append((i, j))
    
    return concurrent_pairs


def sort_by_causality(clocks: List[VectorClock]) -> List[int]:
    """
    Topologically sort events by causality.
    
    Returns indices in an order that respects happens-before relationships.
    Note: Concurrent events can appear in any order relative to each other.
    
    Args:
        clocks: List of vector clocks
        
    Returns:
        List of indices in causal order
    
    Example:
        >>> vc1 = VectorClock({'A': 1})
        >>> vc2 = VectorClock({'A': 2})
        >>> vc3 = VectorClock({'A': 1, 'B': 1})
        >>> sort_by_causality([vc1, vc2, vc3])
        [0, 1, 2]  # or [0, 2, 1] - both are valid
    """
    from functools import cmp_to_key
    
    def compare(a: VectorClock, b: VectorClock) -> int:
        if a.happens_before(b):
            return -1
        elif a.happens_after(b):
            return 1
        else:
            return 0
    
    indexed = list(enumerate(clocks))
    indexed.sort(key=lambda x: cmp_to_key(compare)(x[1]))
    
    return [i for i, _ in indexed]


def merge_all(clocks: List[VectorClock]) -> VectorClock:
    """
    Merge multiple vector clocks into one.
    
    Args:
        clocks: List of vector clocks to merge
        
    Returns:
        New VectorClock that is the element-wise maximum
    
    Example:
        >>> vc1 = VectorClock({'A': 2, 'B': 1})
        >>> vc2 = VectorClock({'A': 1, 'C': 3})
        >>> merge_all([vc1, vc2])
        VectorClock({'A': 2, 'B': 1, 'C': 3})
    """
    if not clocks:
        return VectorClock()
    
    result = clocks[0].copy()
    for clock in clocks[1:]:
        result.merge(clock)
    
    return result


def detect_conflicts(
    updates: List[Tuple[str, VectorClock]]
) -> List[Tuple[str, str]]:
    """
    Detect conflicting updates in a distributed system.
    
    Two updates conflict if their vector clocks are concurrent.
    
    Args:
        updates: List of (update_id, vector_clock) tuples
        
    Returns:
        List of (update_id1, update_id2) tuples indicating conflicts
    
    Example:
        >>> vc1 = VectorClock({'A': 1, 'B': 0})
        >>> vc2 = VectorClock({'A': 0, 'B': 1})
        >>> detect_conflicts([('u1', vc1), ('u2', vc2)])
        [('u1', 'u2')]
    """
    conflicts = []
    n = len(updates)
    
    for i in range(n):
        for j in range(i + 1, n):
            id1, clock1 = updates[i]
            id2, clock2 = updates[j]
            if clock1.concurrent_with(clock2):
                conflicts.append((id1, id2))
    
    return conflicts


class VectorClockHistory:
    """
    Track the history of events with vector clocks.
    
    Useful for debugging and visualization of distributed systems.
    """
    
    def __init__(self):
        """Initialize an empty history."""
        self._events: List[Tuple[str, VectorClock, Optional[str]]] = []
    
    def record(self, event_id: str, clock: VectorClock, description: str = None) -> None:
        """
        Record an event in the history.
        
        Args:
            event_id: Unique identifier for the event
            clock: The vector clock at this event
            description: Optional description
        """
        self._events.append((event_id, clock.copy(), description))
    
    def get_event(self, event_id: str) -> Optional[Tuple[VectorClock, Optional[str]]]:
        """
        Get an event by its ID.
        
        Args:
            event_id: The event identifier
            
        Returns:
            Tuple of (clock, description) or None
        """
        for eid, clock, desc in self._events:
            if eid == event_id:
                return (clock, desc)
        return None
    
    def get_causal_chain(self, event_id: str) -> List[Tuple[str, VectorClock, Optional[str]]]:
        """
        Get all events that causally precede a given event.
        
        Args:
            event_id: The event identifier
            
        Returns:
            List of (event_id, clock, description) tuples in causal order
        """
        target = self.get_event(event_id)
        if not target:
            return []
        
        target_clock, _ = target
        chain = []
        
        for eid, clock, desc in self._events:
            if clock.happens_before(target_clock):
                chain.append((eid, clock.copy(), desc))
        
        # Sort by causality
        chain.sort(key=lambda x: (x[1].total(), str(x[1])))
        
        return chain
    
    def get_all_events(self) -> List[Tuple[str, VectorClock, Optional[str]]]:
        """Get all recorded events."""
        return [(eid, clk.copy(), desc) for eid, clk, desc in self._events]
    
    def clear(self) -> None:
        """Clear the history."""
        self._events = []
    
    def __len__(self) -> int:
        """Return the number of recorded events."""
        return len(self._events)
    
    def __repr__(self) -> str:
        """String representation."""
        return f"VectorClockHistory({len(self._events)} events)"


# =============================================================================
# Convenience Functions
# =============================================================================

def create_clock(*process_ids: str) -> VectorClock:
    """
    Create a vector clock initialized with zeros for given process IDs.
    
    Args:
        *process_ids: Variable number of process identifiers
        
    Returns:
        New VectorClock with all counters set to 0
    
    Example:
        >>> create_clock('A', 'B', 'C')
        VectorClock({'A': 0, 'B': 0, 'C': 0})
    """
    return VectorClock({pid: 0 for pid in process_ids})


def increment_and_merge(clock: VectorClock, process_id: str, other: VectorClock) -> VectorClock:
    """
    Simulate receiving a message: merge with other clock and increment local.
    
    This is a common pattern in distributed systems:
    1. Merge with the received vector clock
    2. Increment the local counter
    
    Args:
        clock: The local vector clock
        process_id: The local process ID
        other: The received vector clock
        
    Returns:
        New VectorClock after merge and increment
    
    Example:
        >>> local = VectorClock({'A': 1, 'B': 0})
        >>> received = VectorClock({'A': 0, 'B': 2})
        >>> increment_and_merge(local, 'A', received)
        VectorClock({'A': 2, 'B': 2})
    """
    result = clock.copy()
    result.merge(other)
    result.increment(process_id)
    return result


def is_ancestor(ancestor: VectorClock, descendant: VectorClock) -> bool:
    """
    Check if one clock is a direct or indirect ancestor of another.
    
    This is equivalent to happens-before but more intuitive for some use cases.
    
    Args:
        ancestor: The potential ancestor clock
        descendant: The potential descendant clock
        
    Returns:
        True if ancestor happens-before descendant
    
    Example:
        >>> vc1 = VectorClock({'A': 1})
        >>> vc2 = VectorClock({'A': 2})
        >>> is_ancestor(vc1, vc2)
        True
    """
    return ancestor.happens_before(descendant)


def is_descendant(descendant: VectorClock, ancestor: VectorClock) -> bool:
    """
    Check if one clock is a direct or indirect descendant of another.
    
    Args:
        descendant: The potential descendant clock
        ancestor: The potential ancestor clock
        
    Returns:
        True if descendant happens-after ancestor
    """
    return descendant.happens_after(ancestor)