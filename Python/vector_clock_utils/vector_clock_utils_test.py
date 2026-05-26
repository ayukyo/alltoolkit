#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vector Clock Utilities - Test Suite

Comprehensive tests for vector clock operations.

Author: AllToolkit
License: MIT
"""

import sys
import os
import pytest

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from vector_clock_utils.mod import (
    VectorClock, DottedVersionVector, VectorClockHistory,
    compare_events, find_concurrent_events, sort_by_causality,
    merge_all, detect_conflicts, create_clock, increment_and_merge,
    is_ancestor, is_descendant
)


class TestVectorClockBasic:
    """Basic vector clock operations."""
    
    def test_create_empty(self):
        """Test creating an empty vector clock."""
        vc = VectorClock()
        assert vc.clock == {}
        assert vc.is_empty()
    
    def test_create_with_values(self):
        """Test creating a vector clock with initial values."""
        vc = VectorClock({'A': 1, 'B': 2, 'C': 3})
        assert vc.get('A') == 1
        assert vc.get('B') == 2
        assert vc.get('C') == 3
    
    def test_get_nonexistent(self):
        """Test getting value for non-existent process."""
        vc = VectorClock({'A': 1})
        assert vc.get('B') == 0  # Default is 0
    
    def test_set_value(self):
        """Test setting a value."""
        vc = VectorClock()
        vc.set('A', 5)
        assert vc.get('A') == 5
    
    def test_set_negative_raises(self):
        """Test that setting negative values raises error."""
        vc = VectorClock()
        with pytest.raises(ValueError):
            vc.set('A', -1)
    
    def test_increment(self):
        """Test incrementing a process counter."""
        vc = VectorClock({'A': 5})
        vc.increment('A')
        assert vc.get('A') == 6
        
        # Increment non-existent process
        vc.increment('B')
        assert vc.get('B') == 1
    
    def test_merge(self):
        """Test merging two vector clocks."""
        vc1 = VectorClock({'A': 2, 'B': 1})
        vc2 = VectorClock({'A': 1, 'B': 3, 'C': 2})
        
        vc1.merge(vc2)
        
        assert vc1.get('A') == 2  # max(2, 1) = 2
        assert vc1.get('B') == 3  # max(1, 3) = 3
        assert vc1.get('C') == 2  # new process


class TestVectorClockComparison:
    """Vector clock comparison operations."""
    
    def test_equal(self):
        """Test equality."""
        vc1 = VectorClock({'A': 1, 'B': 2})
        vc2 = VectorClock({'A': 1, 'B': 2})
        
        assert vc1 == vc2
        assert vc1 <= vc2
        assert vc1 >= vc2
    
    def test_not_equal(self):
        """Test inequality."""
        vc1 = VectorClock({'A': 1})
        vc2 = VectorClock({'A': 2})
        
        assert vc1 != vc2
    
    def test_happens_before(self):
        """Test happens-before relationship."""
        vc1 = VectorClock({'A': 1, 'B': 0})
        vc2 = VectorClock({'A': 1, 'B': 2})
        
        assert vc1.happens_before(vc2)
        assert not vc2.happens_before(vc1)
        assert vc1 < vc2
    
    def test_happens_after(self):
        """Test happens-after relationship."""
        vc1 = VectorClock({'A': 1})
        vc2 = VectorClock({'A': 2})
        
        assert vc2.happens_after(vc1)
        assert vc2 > vc1
    
    def test_concurrent(self):
        """Test concurrent events."""
        vc1 = VectorClock({'A': 1, 'B': 0})
        vc2 = VectorClock({'A': 0, 'B': 1})
        
        assert vc1.concurrent_with(vc2)
        assert vc2.concurrent_with(vc1)
    
    def test_concurrent_with_difference(self):
        """Test concurrent events with overlapping processes."""
        vc1 = VectorClock({'A': 2, 'B': 1})
        vc2 = VectorClock({'A': 1, 'B': 2})
        
        # A[2,1] and B[1,2] are concurrent because A[2]>B[1] but A[1]<B[2]
        assert vc1.concurrent_with(vc2)
    
    def test_not_concurrent_when_related(self):
        """Test that related events are not concurrent."""
        vc1 = VectorClock({'A': 1})
        vc2 = VectorClock({'A': 2})
        
        assert not vc1.concurrent_with(vc2)


class TestVectorClockUtilities:
    """Utility functions for vector clocks."""
    
    def test_copy(self):
        """Test copying a vector clock."""
        vc1 = VectorClock({'A': 1, 'B': 2})
        vc2 = vc1.copy()
        
        # Modify original
        vc1.increment('A')
        
        # Copy should be independent
        assert vc2.get('A') == 1
        assert vc1.get('A') == 2
    
    def test_to_dict(self):
        """Test conversion to dictionary."""
        vc = VectorClock({'A': 1, 'B': 2})
        d = vc.to_dict()
        
        assert d == {'A': 1, 'B': 2}
    
    def test_from_dict(self):
        """Test creation from dictionary."""
        vc = VectorClock.from_dict({'A': 1, 'B': 2})
        
        assert vc.get('A') == 1
        assert vc.get('B') == 2
    
    def test_json_serialization(self):
        """Test JSON serialization/deserialization."""
        vc1 = VectorClock({'A': 1, 'B': 2})
        json_str = vc1.to_json()
        
        vc2 = VectorClock.from_json(json_str)
        
        assert vc1 == vc2
    
    def test_processes(self):
        """Test getting process IDs."""
        vc = VectorClock({'A': 1, 'B': 2, 'C': 3})
        
        assert vc.processes() == {'A', 'B', 'C'}
    
    def test_total(self):
        """Test getting total of all counters."""
        vc = VectorClock({'A': 1, 'B': 2, 'C': 3})
        
        assert vc.total() == 6
    
    def test_max_min_values(self):
        """Test max and min values."""
        vc = VectorClock({'A': 1, 'B': 5, 'C': 3})
        
        assert vc.max_value() == 5
        assert vc.min_value() == 1
    
    def test_add_remove_process(self):
        """Test adding and removing processes."""
        vc = VectorClock({'A': 1})
        
        vc.add_process('B', 5)
        assert vc.get('B') == 5
        
        # Adding existing process doesn't change value
        vc.add_process('A', 10)
        assert vc.get('A') == 1  # Unchanged
        
        vc.remove_process('B')
        assert vc.get('B') == 0
    
    def test_reset(self):
        """Test resetting counters."""
        vc = VectorClock({'A': 5, 'B': 3})
        vc.reset()
        
        assert vc.get('A') == 0
        assert vc.get('B') == 0


class TestDottedVersionVector:
    """Dotted version vector tests."""
    
    def test_create(self):
        """Test creating a dotted version vector."""
        dvv = DottedVersionVector('A')
        assert dvv.process_id == 'A'
        assert dvv.dot == ('A', 0)
    
    def test_increment(self):
        """Test incrementing a dotted version vector."""
        dvv = DottedVersionVector('A')
        dvv.increment()
        
        assert dvv.dot == ('A', 1)
        assert dvv.vector == {'A': 1}
        
        dvv.increment()
        assert dvv.dot == ('A', 2)
        assert dvv.vector == {'A': 2}
    
    def test_merge(self):
        """Test merging dotted version vectors."""
        dvv1 = DottedVersionVector('A')
        dvv1.increment()  # A:1
        
        dvv2 = DottedVersionVector('B')
        dvv2.increment()  # B:1
        
        dvv1.merge(dvv2)
        
        assert dvv1.vector.get('B') == 1
    
    def test_contains(self):
        """Test dot containment."""
        dvv = DottedVersionVector('A')
        dvv.increment()  # A:1
        
        assert dvv.contains(('A', 1))
        assert not dvv.contains(('A', 2))
        assert not dvv.contains(('B', 1))
    
    def test_dominates(self):
        """Test domination relationship."""
        dvv1 = DottedVersionVector('A')
        dvv1.increment()
        
        dvv2 = DottedVersionVector('A')
        dvv2.increment()
        dvv2.increment()
        
        assert dvv2.dominates(dvv1)
        assert not dvv1.dominates(dvv2)
    
    def test_to_vector_clock(self):
        """Test conversion to vector clock."""
        dvv = DottedVersionVector('A')
        dvv.increment()
        dvv.vector['B'] = 3  # Directly modify the vector dict
        
        vc = dvv.to_vector_clock()
        
        assert isinstance(vc, VectorClock)
        assert vc.get('A') == 1
        assert vc.get('B') == 3


class TestHelperFunctions:
    """Test helper functions."""
    
    def test_compare_events(self):
        """Test event comparison."""
        vc1 = VectorClock({'A': 1})
        vc2 = VectorClock({'A': 2})
        vc3 = VectorClock({'B': 1})
        
        assert compare_events(vc1, vc2) == 'before'
        assert compare_events(vc2, vc1) == 'after'
        assert compare_events(vc1, vc3) == 'concurrent'
        assert compare_events(vc1, vc1) == 'equal'
    
    def test_find_concurrent_events(self):
        """Test finding concurrent event pairs."""
        vc1 = VectorClock({'A': 1, 'B': 0})  # Event 1
        vc2 = VectorClock({'A': 0, 'B': 1})  # Event 2 (concurrent with 1)
        vc3 = VectorClock({'A': 2, 'B': 1})  # Event 3 (after both)
        
        pairs = find_concurrent_events([vc1, vc2, vc3])
        
        assert (0, 1) in pairs  # vc1 and vc2 are concurrent
    
    def test_sort_by_causality(self):
        """Test causal sorting."""
        vc1 = VectorClock({'A': 1})  # First
        vc2 = VectorClock({'A': 2})  # After vc1
        vc3 = VectorClock({'A': 3})  # After vc2
        
        indices = sort_by_causality([vc3, vc1, vc2])
        
        # Should be sorted in causal order
        assert indices[0] == 1  # vc1
        assert indices[1] == 2  # vc2
        assert indices[2] == 0  # vc3
    
    def test_merge_all(self):
        """Test merging multiple vector clocks."""
        vc1 = VectorClock({'A': 2, 'B': 1})
        vc2 = VectorClock({'A': 1, 'C': 3})
        vc3 = VectorClock({'B': 2, 'C': 1})
        
        merged = merge_all([vc1, vc2, vc3])
        
        assert merged.get('A') == 2
        assert merged.get('B') == 2
        assert merged.get('C') == 3
    
    def test_merge_all_empty(self):
        """Test merging empty list."""
        merged = merge_all([])
        
        assert merged.is_empty()
    
    def test_detect_conflicts(self):
        """Test conflict detection."""
        vc1 = VectorClock({'A': 1, 'B': 0})
        vc2 = VectorClock({'A': 0, 'B': 1})
        vc3 = VectorClock({'A': 1, 'B': 1})  # After both
        
        conflicts = detect_conflicts([
            ('u1', vc1),
            ('u2', vc2),
            ('u3', vc3)
        ])
        
        # u1 and u2 are concurrent (conflict)
        assert ('u1', 'u2') in conflicts
        # u3 doesn't conflict with u1 or u2 (it's after both)
    
    def test_create_clock(self):
        """Test clock creation helper."""
        vc = create_clock('A', 'B', 'C')
        
        assert vc.get('A') == 0
        assert vc.get('B') == 0
        assert vc.get('C') == 0
        assert len(vc.processes()) == 3
    
    def test_increment_and_merge(self):
        """Test increment and merge helper."""
        local = VectorClock({'A': 1, 'B': 0})
        received = VectorClock({'A': 0, 'B': 2})
        
        result = increment_and_merge(local, 'A', received)
        
        assert result.get('A') == 2  # max(1, 0) + 1 = 2
        assert result.get('B') == 2  # max(0, 2) = 2
    
    def test_is_ancestor(self):
        """Test ancestor check."""
        vc1 = VectorClock({'A': 1})
        vc2 = VectorClock({'A': 2})
        
        assert is_ancestor(vc1, vc2)
        assert not is_ancestor(vc2, vc1)
    
    def test_is_descendant(self):
        """Test descendant check."""
        vc1 = VectorClock({'A': 1})
        vc2 = VectorClock({'A': 2})
        
        assert is_descendant(vc2, vc1)
        assert not is_descendant(vc1, vc2)


class TestVectorClockHistory:
    """Test vector clock history tracking."""
    
    def test_record_and_retrieve(self):
        """Test recording and retrieving events."""
        history = VectorClockHistory()
        
        vc = VectorClock({'A': 1})
        history.record('e1', vc, 'First event')
        
        result = history.get_event('e1')
        
        assert result is not None
        clock, desc = result
        assert clock.get('A') == 1
        assert desc == 'First event'
    
    def test_get_nonexistent_event(self):
        """Test getting non-existent event."""
        history = VectorClockHistory()
        
        result = history.get_event('nonexistent')
        
        assert result is None
    
    def test_get_causal_chain(self):
        """Test getting causal chain."""
        history = VectorClockHistory()
        
        vc1 = VectorClock({'A': 1})
        vc2 = VectorClock({'A': 2})
        vc3 = VectorClock({'A': 3})
        
        history.record('e1', vc1, 'First')
        history.record('e2', vc2, 'Second')
        history.record('e3', vc3, 'Third')
        
        chain = history.get_causal_chain('e3')
        
        assert len(chain) == 2  # e1 and e2 precede e3
    
    def test_clear(self):
        """Test clearing history."""
        history = VectorClockHistory()
        
        history.record('e1', VectorClock({'A': 1}))
        assert len(history) == 1
        
        history.clear()
        assert len(history) == 0


class TestDistributedSystemScenario:
    """Test realistic distributed system scenarios."""
    
    def test_three_node_broadcast(self):
        """Test a three-node broadcast scenario."""
        # Three nodes: A, B, C
        vc_a = VectorClock({'A': 0, 'B': 0, 'C': 0})
        vc_b = VectorClock({'A': 0, 'B': 0, 'C': 0})
        vc_c = VectorClock({'A': 0, 'B': 0, 'C': 0})
        
        # Node A has local event
        vc_a.increment('A')  # A: [1,0,0]
        assert vc_a.get('A') == 1
        
        # Node A sends to B
        vc_b.merge(vc_a)
        vc_b.increment('B')  # B: [1,1,0]
        
        assert vc_a.happens_before(vc_b)
        
        # Node B broadcasts to C
        vc_c.merge(vc_b)
        vc_c.increment('C')  # C: [1,1,1]
        
        assert vc_b.happens_before(vc_c)
        assert vc_a.happens_before(vc_c)
    
    def test_concurrent_updates(self):
        """Test detecting concurrent updates."""
        # Two concurrent updates
        vc1 = VectorClock({'A': 1, 'B': 0})
        vc2 = VectorClock({'A': 0, 'B': 1})
        
        assert vc1.concurrent_with(vc2)
        
        # Merge resolves to a common state
        merged = merge_all([vc1, vc2])
        
        assert merged.get('A') == 1
        assert merged.get('B') == 1
    
    def test_version_vector_evolution(self):
        """Test version vector evolution in a distributed database."""
        # Simulate a distributed key-value store
        
        # Initial state
        replicas = {
            'R1': VectorClock({'R1': 0, 'R2': 0, 'R3': 0}),
            'R2': VectorClock({'R1': 0, 'R2': 0, 'R3': 0}),
            'R3': VectorClock({'R1': 0, 'R2': 0, 'R3': 0}),
        }
        
        # R1 receives write, increments its counter
        replicas['R1'].increment('R1')  # Write at R1
        
        # R1 replicates to R2
        replicas['R2'].merge(replicas['R1'])
        replicas['R2'].increment('R2')  # Acknowledge
        
        # R2 replicates to R3
        replicas['R3'].merge(replicas['R2'])
        replicas['R3'].increment('R3')  # Acknowledge
        
        # Check causality
        assert replicas['R1'].happens_before(replicas['R2'])
        assert replicas['R2'].happens_before(replicas['R3'])
        assert replicas['R1'].happens_before(replicas['R3'])


class TestEdgeCases:
    """Test edge cases and boundary conditions."""
    
    def test_empty_clock_operations(self):
        """Test operations on empty clocks."""
        vc = VectorClock()
        
        assert vc.is_empty()
        assert vc.total() == 0
        assert vc.max_value() == 0
        assert vc.min_value() == 0
    
    def test_merge_with_empty(self):
        """Test merging with empty clock."""
        vc1 = VectorClock({'A': 5})
        vc2 = VectorClock()
        
        vc1.merge(vc2)
        
        assert vc1.get('A') == 5
    
    def test_hash_consistency(self):
        """Test hash consistency."""
        vc1 = VectorClock({'A': 1, 'B': 2})
        vc2 = VectorClock({'A': 1, 'B': 2})
        
        assert hash(vc1) == hash(vc2)
        
        # Can use in sets
        clock_set = {vc1, vc2}
        assert len(clock_set) == 1
    
    def test_string_representations(self):
        """Test string representations."""
        vc = VectorClock({'A': 1, 'B': 2})
        
        assert 'VectorClock' in repr(vc)
        assert 'A:1' in str(vc) or 'A: 1' in str(vc)
    
    def test_large_values(self):
        """Test with large counter values."""
        vc = VectorClock({'A': 1000000, 'B': 999999999})
        
        assert vc.get('A') == 1000000
        assert vc.get('B') == 999999999
        assert vc.total() == 1000999999
    
    def test_many_processes(self):
        """Test with many processes."""
        processes = {f'P{i}': i for i in range(100)}
        vc = VectorClock(processes)
        
        assert len(vc.processes()) == 100
        assert vc.total() == sum(range(100))


if __name__ == '__main__':
    pytest.main([__file__, '-v'])