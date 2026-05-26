#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vector Clock Example: Distributed Counter with CRDT

This example demonstrates how vector clocks can be used to implement
a conflict-free replicated data type (CRDT) - specifically, a state-based
counter (G-Counter).

Author: AllToolkit
License: MIT
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from vector_clock_utils.mod import VectorClock, merge_all


class GCounter:
    """
    Grow-only Counter (G-Counter) CRDT.
    
    A G-Counter can only be incremented, never decremented.
    Each replica maintains its own count, and the total is the sum
    of all replica counts.
    
    This uses vector clock concepts for tracking per-replica counts.
    """
    
    def __init__(self, node_id: str):
        """Initialize a G-Counter for a specific node."""
        self.node_id = node_id
        self.counts = VectorClock()  # Use VectorClock as internal state
    
    def increment(self, amount: int = 1) -> int:
        """
        Increment the counter.
        
        Args:
            amount: Amount to increment (default 1)
            
        Returns:
            The new local count
        """
        current = self.counts.get(self.node_id)
        self.counts.set(self.node_id, current + amount)
        return self.counts.get(self.node_id)
    
    def value(self) -> int:
        """Get the total counter value (sum of all replicas)."""
        return self.counts.total()
    
    def merge(self, other: 'GCounter') -> 'GCounter':
        """
        Merge with another G-Counter.
        
        This is the key CRDT operation - it combines states from different
        replicas without losing any increments.
        
        Args:
            other: Another G-Counter to merge with
            
        Returns:
            Self for chaining
        """
        self.counts.merge(other.counts)
        return self
    
    def to_dict(self) -> dict:
        """Serialize to dictionary."""
        return {
            'node_id': self.node_id,
            'counts': self.counts.to_dict()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'GCounter':
        """Deserialize from dictionary."""
        counter = cls(data['node_id'])
        counter.counts = VectorClock.from_dict(data['counts'])
        return counter
    
    def __repr__(self) -> str:
        return f"GCounter(node={self.node_id}, value={self.value()}, state={self.counts})"


class PNCounter:
    """
    Increment/Decrement Counter (PN-Counter) CRDT.
    
    A PN-Counter supports both increment and decrement by using two
    G-Counters: one for increments, one for decrements.
    """
    
    def __init__(self, node_id: str):
        """Initialize a PN-Counter for a specific node."""
        self.node_id = node_id
        self.p_counter = GCounter(node_id)  # Increments
        self.n_counter = GCounter(node_id)  # Decrements
    
    def increment(self, amount: int = 1) -> int:
        """Increment the counter."""
        self.p_counter.increment(amount)
        return self.value()
    
    def decrement(self, amount: int = 1) -> int:
        """Decrement the counter."""
        self.n_counter.increment(amount)
        return self.value()
    
    def value(self) -> int:
        """Get the current counter value."""
        return self.p_counter.value() - self.n_counter.value()
    
    def merge(self, other: 'PNCounter') -> 'PNCounter':
        """Merge with another PN-Counter."""
        self.p_counter.merge(other.p_counter)
        self.n_counter.merge(other.n_counter)
        return self
    
    def __repr__(self) -> str:
        return f"PNCounter(node={self.node_id}, value={self.value()}, +{self.p_counter.value()}, -{self.n_counter.value()})"


def simulate_replicated_counter():
    """Simulate a replicated counter scenario."""
    print("=" * 60)
    print("G-Counter (Grow-Only Counter) Simulation")
    print("=" * 60)
    
    # Create replicas on different nodes
    counter_a = GCounter('node_a')
    counter_b = GCounter('node_b')
    counter_c = GCounter('node_c')
    
    # Each node increments locally
    print("\n--- Local Increments ---")
    counter_a.increment(5)
    print(f"Node A increments by 5: {counter_a}")
    
    counter_b.increment(3)
    print(f"Node B increments by 3: {counter_b}")
    
    counter_c.increment(7)
    print(f"Node C increments by 7: {counter_c}")
    
    # Replication - merge states
    print("\n--- Replication (Merging) ---")
    print("Node A receives updates from B and C...")
    counter_a.merge(counter_b)
    counter_a.merge(counter_c)
    print(f"Node A after merge: {counter_a}")
    
    print("\nNode B receives update from A...")
    counter_b.merge(counter_a)
    print(f"Node B after merge: {counter_b}")
    
    print("\nNode C receives update from A...")
    counter_c.merge(counter_a)
    print(f"Node C after merge: {counter_c}")
    
    # More increments
    print("\n--- More Increments ---")
    counter_a.increment(2)
    print(f"Node A increments by 2: {counter_a}")
    
    counter_b.increment(4)
    print(f"Node B increments by 4: {counter_b}")
    
    # Final merge
    print("\n--- Final Merge ---")
    all_counters = [counter_a, counter_b, counter_c]
    
    # All nodes should have the same final value after full replication
    for c in all_counters:
        for other in all_counters:
            c.merge(other)
    
    print(f"Final state (all nodes identical):")
    for c in all_counters:
        print(f"  {c}")


def simulate_pn_counter():
    """Simulate a PN-Counter with increments and decrements."""
    print("\n" + "=" * 60)
    print("PN-Counter (Increment/Decrement Counter) Simulation")
    print("=" * 60)
    
    # Create replicas
    counter_a = PNCounter('node_a')
    counter_b = PNCounter('node_b')
    
    print("\n--- Operations ---")
    counter_a.increment(10)
    print(f"Node A increments by 10: {counter_a}")
    
    counter_a.decrement(3)
    print(f"Node A decrements by 3: {counter_a}")
    
    counter_b.increment(5)
    print(f"Node B increments by 5: {counter_b}")
    
    counter_b.decrement(2)
    print(f"Node B decrements by 2: {counter_b}")
    
    print("\n--- Merge ---")
    counter_a.merge(counter_b)
    counter_b.merge(counter_a)
    
    print(f"Node A after merge: {counter_a}")
    print(f"Node B after merge: {counter_b}")
    
    # Both should have the same value
    assert counter_a.value() == counter_b.value()
    print(f"\nBoth nodes converged to: {counter_a.value()}")


def main():
    """Run all simulations."""
    simulate_replicated_counter()
    simulate_pn_counter()
    
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    print("""
Vector clocks are essential for implementing CRDTs:
- G-Counter: Uses vector clock for per-replica counting
- PN-Counter: Uses two G-Counters for inc/dec operations
- Merge operation is idempotent, commutative, and associative
- No coordination needed between replicas
- Eventual consistency guaranteed
""")


if __name__ == '__main__':
    main()