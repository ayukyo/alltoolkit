#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - CRDT Utilities Test Suite
======================================
Comprehensive tests for Conflict-free Replicated Data Types.
"""

import unittest
import time
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from crdt_utils.mod import (
    CRDT, VectorClock, GCounter, PNCounter, 
    GSet, TwoPSet, LWWRegister, ORSet,
    LWWElementSet, CRDTMap, JSONCRDT,
    generate_node_id, crdt_hash, merge_all
)


# ============================================================================
# VectorClock Tests
# ============================================================================

class TestVectorClock(unittest.TestCase):
    """Tests for VectorClock."""
    
    def test_creation(self):
        """Test vector clock creation."""
        vc = VectorClock({'A': 1, 'B': 2})
        self.assertEqual(vc.get('A'), 1)
        self.assertEqual(vc.get('B'), 2)
        self.assertEqual(vc.get('C'), 0)  # Unknown node
    
    def test_increment(self):
        """Test incrementing a clock."""
        vc = VectorClock()
        vc = vc.increment('A')
        self.assertEqual(vc.get('A'), 1)
        vc = vc.increment('A')
        self.assertEqual(vc.get('A'), 2)
        vc = vc.increment('B')
        self.assertEqual(vc.get('B'), 1)
    
    def test_merge(self):
        """Test merging vector clocks."""
        vc1 = VectorClock({'A': 1, 'B': 2})
        vc2 = VectorClock({'A': 2, 'C': 1})
        
        merged = vc1.merge(vc2)
        self.assertEqual(merged.get('A'), 2)  # max
        self.assertEqual(merged.get('B'), 2)
        self.assertEqual(merged.get('C'), 1)
    
    def test_merge_idempotent(self):
        """Test that merge is idempotent."""
        vc = VectorClock({'A': 1, 'B': 2})
        merged = vc.merge(vc)
        self.assertEqual(merged.clocks, vc.clocks)
    
    def test_merge_commutative(self):
        """Test that merge is commutative."""
        vc1 = VectorClock({'A': 1})
        vc2 = VectorClock({'B': 2})
        
        merged1 = vc1.merge(vc2)
        merged2 = vc2.merge(vc1)
        
        self.assertEqual(merged1.clocks, merged2.clocks)
    
    def test_compare_equal(self):
        """Test comparing equal clocks."""
        vc1 = VectorClock({'A': 1})
        vc2 = VectorClock({'A': 1})
        self.assertEqual(vc1.compare(vc2), 'equal')
    
    def test_compare_before(self):
        """Test comparing clocks where one is before."""
        vc1 = VectorClock({'A': 1})
        vc2 = VectorClock({'A': 2})
        self.assertEqual(vc1.compare(vc2), 'before')
    
    def test_compare_concurrent(self):
        """Test comparing concurrent clocks."""
        vc1 = VectorClock({'A': 2, 'B': 1})
        vc2 = VectorClock({'A': 1, 'B': 2})
        self.assertEqual(vc1.compare(vc2), 'concurrent')
    
    def test_serialize(self):
        """Test serialization."""
        vc = VectorClock({'A': 1, 'B': 2})
        data = vc.to_dict()
        restored = VectorClock.from_dict(data)
        self.assertEqual(vc.clocks, restored.clocks)


# ============================================================================
# GCounter Tests
# ============================================================================

class TestGCounter(unittest.TestCase):
    """Tests for G-Counter."""
    
    def test_creation(self):
        """Test counter creation."""
        counter = GCounter(node_id='A')
        self.assertEqual(counter.value, 0)
    
    def test_increment(self):
        """Test incrementing."""
        counter = GCounter(node_id='A')
        counter = counter.increment()
        self.assertEqual(counter.value, 1)
        counter = counter.increment(5)
        self.assertEqual(counter.value, 6)
    
    def test_increment_negative_raises(self):
        """Test that negative increment raises."""
        counter = GCounter(node_id='A')
        with self.assertRaises(ValueError):
            counter.increment(-1)
    
    def test_merge(self):
        """Test merging counters."""
        counter1 = GCounter(node_id='A', counters={'A': 3, 'B': 2})
        counter2 = GCounter(node_id='B', counters={'A': 1, 'B': 5, 'C': 2})
        
        merged = counter1.merge(counter2)
        # Max of each: A=3, B=5, C=2 = 10
        self.assertEqual(merged.value, 10)
    
    def test_distributed_scenario(self):
        """Test a distributed counter scenario."""
        # Node A increments
        counter_a = GCounter(node_id='A')
        counter_a = counter_a.increment()
        counter_a = counter_a.increment()
        
        # Node B increments independently
        counter_b = GCounter(node_id='B')
        counter_b = counter_b.increment()
        
        # Merge from A's perspective
        counter_a_merged = counter_a.merge(counter_b)
        self.assertEqual(counter_a_merged.value, 3)
        
        # Merge from B's perspective
        counter_b_merged = counter_b.merge(counter_a)
        self.assertEqual(counter_b_merged.value, 3)
    
    def test_serialize(self):
        """Test serialization."""
        counter = GCounter(node_id='A')
        counter = counter.increment(5)
        
        data = counter.to_dict()
        restored = GCounter.from_dict(data)
        
        self.assertEqual(counter.value, restored.value)
        self.assertEqual(counter.node_id, restored.node_id)


# ============================================================================
# PNCounter Tests
# ============================================================================

class TestPNCounter(unittest.TestCase):
    """Tests for PN-Counter."""
    
    def test_creation(self):
        """Test counter creation."""
        counter = PNCounter(node_id='A')
        self.assertEqual(counter.value, 0)
    
    def test_increment_and_decrement(self):
        """Test increment and decrement."""
        counter = PNCounter(node_id='A')
        counter = counter.increment(5)
        self.assertEqual(counter.value, 5)
        counter = counter.decrement(2)
        self.assertEqual(counter.value, 3)
        counter = counter.decrement(5)
        self.assertEqual(counter.value, -2)  # Can be negative
    
    def test_merge(self):
        """Test merging counters."""
        counter1 = PNCounter(
            node_id='A',
            p_counters={'A': 5, 'B': 3},
            n_counters={'A': 2, 'B': 1}
        )
        counter2 = PNCounter(
            node_id='B',
            p_counters={'A': 3, 'B': 6},
            n_counters={'A': 1, 'B': 4}
        )
        
        merged = counter1.merge(counter2)
        # P: max(A:5,3=5, B:3,6=6) = 11
        # N: max(A:2,1=2, B:1,4=4) = 6
        # Value: 11 - 6 = 5
        self.assertEqual(merged.value, 5)
    
    def test_serialize(self):
        """Test serialization."""
        counter = PNCounter(node_id='A')
        counter = counter.increment(10).decrement(3)
        
        data = counter.to_dict()
        restored = PNCounter.from_dict(data)
        
        self.assertEqual(counter.value, restored.value)


# ============================================================================
# GSet Tests
# ============================================================================

class TestGSet(unittest.TestCase):
    """Tests for G-Set."""
    
    def test_creation(self):
        """Test set creation."""
        s = GSet[int]()
        self.assertEqual(len(s), 0)
    
    def test_add(self):
        """Test adding elements."""
        s = GSet[int]()
        s = s.add(1).add(2).add(3)
        
        self.assertEqual(len(s), 3)
        self.assertIn(1, s)
        self.assertIn(2, s)
        self.assertIn(3, s)
    
    def test_add_duplicate(self):
        """Test adding duplicates (should be ignored)."""
        s = GSet[int]()
        s = s.add(1).add(1).add(1)
        self.assertEqual(len(s), 1)
    
    def test_merge(self):
        """Test merging sets."""
        s1 = GSet[int]()
        s1 = s1.add(1).add(2)
        
        s2 = GSet[int]()
        s2 = s2.add(2).add(3)
        
        merged = s1.merge(s2)
        self.assertEqual(set(merged), {1, 2, 3})
    
    def test_iterator(self):
        """Test iterating over elements."""
        s = GSet[int]()
        s = s.add(1).add(2).add(3)
        
        elements = list(s)
        self.assertEqual(len(elements), 3)
    
    def test_serialize(self):
        """Test serialization."""
        s = GSet[str]()
        s = s.add('a').add('b').add('c')
        
        data = s.to_dict()
        restored = GSet.from_dict(data)
        
        self.assertEqual(s.value, restored.value)


# ============================================================================
# TwoPSet Tests
# ============================================================================

class TestTwoPSet(unittest.TestCase):
    """Tests for 2P-Set."""
    
    def test_add_and_remove(self):
        """Test add and remove."""
        s = TwoPSet[int]()
        s = s.add(1).add(2).add(3)
        self.assertEqual(len(s), 3)
        
        s = s.remove(2)
        self.assertEqual(len(s), 2)
        self.assertNotIn(2, s)
    
    def test_cannot_readd(self):
        """Test that removed elements cannot be re-added."""
        s = TwoPSet[int]()
        s = s.add(1)
        s = s.remove(1)
        s = s.add(1)  # Still in tombstone set
        
        self.assertNotIn(1, s)
    
    def test_merge(self):
        """Test merging sets."""
        s1 = TwoPSet[int]()
        s1 = s1.add(1).add(2).remove(1)
        
        s2 = TwoPSet[int]()
        s2 = s2.add(2).add(3)
        
        merged = s1.merge(s2)
        # Add set: {1, 2, 3}
        # Remove set: {1}
        # Result: {2, 3}
        self.assertEqual(set(merged), {2, 3})
    
    def test_serialize(self):
        """Test serialization."""
        s = TwoPSet[str]()
        s = s.add('x').add('y').remove('x')
        
        data = s.to_dict()
        restored = TwoPSet.from_dict(data)
        
        self.assertEqual(s.value, restored.value)


# ============================================================================
# LWWRegister Tests
# ============================================================================

class TestLWWRegister(unittest.TestCase):
    """Tests for LWW-Register."""
    
    def test_creation(self):
        """Test register creation."""
        reg = LWWRegister[str](node_id='A')
        self.assertIsNone(reg.value)
    
    def test_set_value(self):
        """Test setting values."""
        reg = LWWRegister[str](node_id='A')
        reg = reg.set('hello')
        self.assertEqual(reg.value, 'hello')
        
        reg = reg.set('world')
        self.assertEqual(reg.value, 'world')
    
    def test_merge_latest_wins(self):
        """Test that latest timestamp wins on merge."""
        reg1 = LWWRegister[str](node_id='A')
        reg1 = reg1.set('value1', timestamp=100.0)
        
        reg2 = LWWRegister[str](node_id='B')
        reg2 = reg2.set('value2', timestamp=200.0)
        
        merged = reg1.merge(reg2)
        self.assertEqual(merged.value, 'value2')  # Latest wins
    
    def test_merge_same_timestamp(self):
        """Test merge with same timestamp (first wins)."""
        reg1 = LWWRegister[str](node_id='A')
        reg1 = reg1.set('value1', timestamp=100.0)
        
        reg2 = LWWRegister[str](node_id='B')
        reg2 = reg2.set('value2', timestamp=100.0)
        
        merged = reg1.merge(reg2)
        # Same timestamp, self wins (>=)
        self.assertEqual(merged.value, 'value1')
    
    def test_serialize(self):
        """Test serialization."""
        reg = LWWRegister[int](node_id='A')
        reg = reg.set(42, timestamp=123.0)
        
        data = reg.to_dict()
        restored = LWWRegister.from_dict(data)
        
        self.assertEqual(reg.value, restored.value)
        self.assertEqual(reg.timestamp, restored.timestamp)


# ============================================================================
# ORSet Tests
# ============================================================================

class TestORSet(unittest.TestCase):
    """Tests for OR-Set."""
    
    def test_add_and_remove(self):
        """Test add and remove."""
        s = ORSet[str](node_id='A')
        s = s.add('x').add('y').add('z')
        
        self.assertEqual(len(s), 3)
        
        s = s.remove('y')
        self.assertEqual(len(s), 2)
        self.assertNotIn('y', s)
    
    def test_can_readd(self):
        """Test that removed elements CAN be re-added."""
        s = ORSet[str](node_id='A')
        s = s.add('x')
        s = s.remove('x')
        s = s.add('x')  # New unique tag
        
        self.assertIn('x', s)
    
    def test_merge(self):
        """Test merging OR-Sets."""
        s1 = ORSet[str](node_id='A')
        s1 = s1.add('a').add('b').add('c')
        
        s2 = ORSet[str](node_id='B')
        s2 = s2.add('b').add('d')
        
        merged = s1.merge(s2)
        # Union of all elements with their tags
        self.assertIn('a', merged)
        self.assertIn('b', merged)
        self.assertIn('c', merged)
        self.assertIn('d', merged)
    
    def test_merge_with_remove(self):
        """Test merging with removes."""
        s1 = ORSet[str](node_id='A')
        s1 = s1.add('x').add('y')
        
        s2 = ORSet[str](node_id='B')
        s2 = s2.add('x')
        s2 = s2.remove('x')  # Removes all tags for 'x' from s2
        
        merged = s1.merge(s2)
        # s1 still has 'x' tags, s2 doesn't
        # Merge keeps union of tags
        self.assertIn('x', merged)
        self.assertIn('y', merged)
    
    def test_serialize(self):
        """Test serialization."""
        s = ORSet[int](node_id='A')
        s = s.add(1).add(2).remove(1)
        
        data = s.to_dict()
        # Note: from_dict loses type info, but structure is preserved
        restored = ORSet.from_dict(data)
        
        self.assertEqual(len(restored), 1)


# ============================================================================
# LWWElementSet Tests
# ============================================================================

class TestLWWElementSet(unittest.TestCase):
    """Tests for LWW-Element-Set."""
    
    def test_add_and_remove(self):
        """Test add and remove."""
        s = LWWElementSet[str](node_id='A')
        s = s.add('x')
        self.assertIn('x', s)
        
        s = s.remove('x')
        self.assertNotIn('x', s)
    
    def test_readd_after_remove(self):
        """Test re-add after remove."""
        s = LWWElementSet[str](node_id='A')
        s = s.add('x', timestamp=100.0)
        s = s.remove('x', timestamp=200.0)
        self.assertNotIn('x', s)
        
        s = s.add('x', timestamp=300.0)  # Later timestamp
        self.assertIn('x', s)
    
    def test_merge(self):
        """Test merging."""
        s1 = LWWElementSet[str](node_id='A')
        s1 = s1.add('a', timestamp=100.0)
        s1 = s1.add('b', timestamp=100.0)
        
        s2 = LWWElementSet[str](node_id='B')
        s2 = s2.add('a', timestamp=50.0)  # Earlier
        s2 = s2.add('c', timestamp=100.0)
        
        merged = s1.merge(s2)
        self.assertIn('a', merged)  # Later add wins
        self.assertIn('b', merged)
        self.assertIn('c', merged)
    
    def test_serialize(self):
        """Test serialization."""
        s = LWWElementSet[str](node_id='A')
        s = s.add('test').remove('test')
        
        data = s.to_dict()
        restored = LWWElementSet.from_dict(data)
        
        self.assertEqual(s.value, restored.value)


# ============================================================================
# CRDTMap Tests
# ============================================================================

class TestCRDTMap(unittest.TestCase):
    """Tests for CRDT Map."""
    
    def test_set_and_get(self):
        """Test set and get operations."""
        m = CRDTMap[str, GCounter](node_id='A')
        
        counter = GCounter('A')
        counter = counter.increment(5)
        
        m = m.set('views', counter)
        
        retrieved = m.get('views')
        self.assertEqual(retrieved.value, 5)
    
    def test_delete(self):
        """Test delete operation."""
        m = CRDTMap[str, GCounter](node_id='A')
        
        counter = GCounter('A')
        m = m.set('counter', counter)
        self.assertIn('counter', m)
        
        m = m.delete('counter')
        self.assertNotIn('counter', m)
    
    def test_merge(self):
        """Test merging maps."""
        counter1 = GCounter('A', counters={'A': 3})
        counter2 = GCounter('B', counters={'B': 2, 'A': 1})
        
        m1 = CRDTMap[str, GCounter](node_id='A')
        m1 = m1.set('c', counter1)
        
        m2 = CRDTMap[str, GCounter](node_id='B')
        m2 = m2.set('c', counter2)
        
        merged = m1.merge(m2)
        merged_counter = merged.get('c')
        # Should have max: A=3, B=2 = 5
        self.assertEqual(merged_counter.value, 5)


# ============================================================================
# JSONCRDT Tests
# ============================================================================

class TestJSONCRDT(unittest.TestCase):
    """Tests for JSON CRDT."""
    
    def test_set_and_get(self):
        """Test set and get operations."""
        data = JSONCRDT(node_id='A')
        data = data.set('name', 'Alice')
        data = data.set('age', 30)
        
        self.assertEqual(data.get('name'), 'Alice')
        self.assertEqual(data.get('age'), 30)
    
    def test_path_operations(self):
        """Test path-based operations."""
        data = JSONCRDT(node_id='A')
        data = data.set_path(['user', 'profile', 'name'], 'Bob')
        data = data.set_path(['user', 'profile', 'email'], 'bob@example.com')
        
        self.assertEqual(data.get_path(['user', 'profile', 'name']), 'Bob')
        self.assertEqual(data.get_path(['user', 'profile', 'email']), 'bob@example.com')
    
    def test_delete(self):
        """Test delete operation."""
        data = JSONCRDT(node_id='A')
        data = data.set('key', 'value')
        self.assertIn('key', data)
        
        data = data.delete('key')
        self.assertNotIn('key', data)
    
    def test_merge(self):
        """Test merging JSON CRDTs."""
        # Create data1 with timestamp 100
        data1 = JSONCRDT(
            node_id='A',
            data={'x': 'value1'},
            timestamps={'x': 100.0}
        )
        
        # Create data2 with timestamp 200 (later)
        data2 = JSONCRDT(
            node_id='B',
            data={'x': 'value2'},
            timestamps={'x': 200.0}
        )
        
        merged = data1.merge(data2)
        self.assertEqual(merged.get('x'), 'value2')  # Later timestamp wins
    
    def test_serialize(self):
        """Test serialization."""
        data = JSONCRDT(node_id='A')
        data = data.set('key', 'value')
        
        restored = JSONCRDT.from_dict(data.to_dict())
        self.assertEqual(data.value, restored.value)
    
    def test_json_string(self):
        """Test JSON string conversion."""
        data = JSONCRDT(node_id='A')
        data = data.set('test', 123)
        
        json_str = data.to_json()
        restored = JSONCRDT.from_json(json_str)
        
        self.assertEqual(data.get('test'), restored.get('test'))


# ============================================================================
# Utility Tests
# ============================================================================

class TestUtilities(unittest.TestCase):
    """Tests for utility functions."""
    
    def test_generate_node_id(self):
        """Test node ID generation."""
        id1 = generate_node_id()
        id2 = generate_node_id()
        
        self.assertEqual(len(id1), 8)
        self.assertNotEqual(id1, id2)  # Should be unique
    
    def test_crdt_hash(self):
        """Test CRDT hashing."""
        counter = GCounter(node_id='A')
        counter = counter.increment(5)
        
        hash1 = crdt_hash(counter)
        hash2 = crdt_hash(counter)
        
        self.assertEqual(hash1, hash2)  # Same CRDT, same hash
    
    def test_merge_all(self):
        """Test merging multiple CRDTs."""
        counters = [
            GCounter('A', counters={'A': 3}),
            GCounter('B', counters={'B': 2}),
            GCounter('C', counters={'C': 1, 'A': 1}),
        ]
        
        merged = merge_all(counters)
        self.assertEqual(merged.value, 6)
    
    def test_merge_all_empty_raises(self):
        """Test that merge_all raises for empty list."""
        with self.assertRaises(ValueError):
            merge_all([])
    
    def test_merge_all_different_types_raises(self):
        """Test that merge_all raises for different types."""
        with self.assertRaises(TypeError):
            merge_all([GCounter('A'), GSet()])


# ============================================================================
# CRDT Properties Tests
# ============================================================================

class TestCRDTProperties(unittest.TestCase):
    """Tests for CRDT mathematical properties."""
    
    def test_gcounter_idempotent(self):
        """Test G-Counter merge idempotency."""
        c = GCounter('A')
        c = c.increment(5)
        
        merged = c.merge(c)
        self.assertEqual(merged.value, c.value)
    
    def test_gcounter_commutative(self):
        """Test G-Counter merge commutativity."""
        c1 = GCounter('A', counters={'A': 3, 'B': 1})
        c2 = GCounter('B', counters={'A': 1, 'B': 4})
        
        m1 = c1.merge(c2)
        m2 = c2.merge(c1)
        
        self.assertEqual(m1.value, m2.value)
        self.assertEqual(m1.counters, m2.counters)
    
    def test_gcounter_associative(self):
        """Test G-Counter merge associativity."""
        c1 = GCounter('A', counters={'A': 2})
        c2 = GCounter('B', counters={'B': 3})
        c3 = GCounter('C', counters={'C': 4})
        
        # (c1 merge c2) merge c3
        m1 = c1.merge(c2).merge(c3)
        
        # c1 merge (c2 merge c3)
        m2 = c1.merge(c2.merge(c3))
        
        self.assertEqual(m1.value, m2.value)
    
    def test_gset_idempotent(self):
        """Test G-Set merge idempotency."""
        s = GSet[int]()
        s = s.add(1).add(2)
        
        merged = s.merge(s)
        self.assertEqual(merged.value, s.value)
    
    def test_gset_commutative(self):
        """Test G-Set merge commutativity."""
        s1 = GSet[int]()
        s1 = s1.add(1).add(2)
        
        s2 = GSet[int]()
        s2 = s2.add(2).add(3)
        
        m1 = s1.merge(s2)
        m2 = s2.merge(s1)
        
        self.assertEqual(m1.value, m2.value)


# ============================================================================
# Run Tests
# ============================================================================

if __name__ == '__main__':
    unittest.main(verbosity=2)