#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vector Clock Example: Distributed Key-Value Store

This example demonstrates how vector clocks can be used to track
versions and detect conflicts in a distributed key-value store.

Author: AllToolkit
License: MIT
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from vector_clock_utils.mod import VectorClock, detect_conflicts, merge_all


class DistributedValue:
    """A value with associated vector clock for conflict detection."""
    
    def __init__(self, value, clock: VectorClock):
        self.value = value
        self.clock = clock
    
    def __repr__(self):
        return f"DistributedValue(value={self.value!r}, clock={self.clock})"


class DistributedKVStore:
    """
    A simple distributed key-value store using vector clocks.
    
    Supports:
    - Multiple replicas
    - Conflict detection
    - Last-writer-wins resolution
    - Merge of concurrent updates
    """
    
    def __init__(self, node_id: str):
        """Initialize a replica."""
        self.node_id = node_id
        self.data: dict = {}  # key -> DistributedValue
        self.clock = VectorClock()  # Local vector clock
    
    def put(self, key: str, value) -> DistributedValue:
        """
        Store a value with version tracking.
        
        Args:
            key: The key to store
            value: The value to store
            
        Returns:
            The stored DistributedValue
        """
        # Increment local clock
        self.clock.increment(self.node_id)
        
        # Create versioned value
        dv = DistributedValue(value, self.clock.copy())
        self.data[key] = dv
        
        print(f"[{self.node_id}] PUT {key}={value!r} at {self.clock}")
        return dv
    
    def get(self, key: str) -> DistributedValue:
        """Get a value by key."""
        return self.data.get(key)
    
    def sync_from(self, other: 'DistributedKVStore'):
        """
        Synchronize data from another replica.
        
        This merges clocks and detects conflicts.
        """
        print(f"\n[{self.node_id}] Syncing from {other.node_id}...")
        
        # Update local clock
        self.clock.merge(other.clock)
        
        # Merge data
        for key, other_value in other.data.items():
            if key not in self.data:
                # Key doesn't exist locally, just copy
                self.data[key] = DistributedValue(
                    other_value.value,
                    other_value.clock.copy()
                )
                print(f"  [{self.node_id}] Added {key}={other_value.value!r}")
            else:
                local_value = self.data[key]
                
                if local_value.clock.happens_before(other_value.clock):
                    # Remote is newer
                    self.data[key] = DistributedValue(
                        other_value.value,
                        other_value.clock.copy()
                    )
                    print(f"  [{self.node_id}] Updated {key} to {other_value.value!r}")
                elif other_value.clock.happens_before(local_value.clock):
                    # Local is newer, keep local
                    print(f"  [{self.node_id}] Keeping local {key}={local_value.value!r}")
                elif local_value.clock.concurrent_with(other_value.clock):
                    # Conflict! Need to resolve
                    print(f"  [{self.node_id}] CONFLICT on {key}!")
                    print(f"    Local:  {local_value.value!r} at {local_value.clock}")
                    print(f"    Remote: {other_value.value!r} at {other_value.clock}")
                    
                    # Resolve using last-writer-wins (higher node_id wins)
                    if self.node_id > other.node_id:
                        self.data[key] = DistributedValue(
                            other_value.value,
                            other_value.clock.copy()
                        )
                        print(f"    Resolved to remote (LWW: {other.node_id})")
                    else:
                        print(f"    Resolved to local (LWW: {self.node_id})")
        
        print(f"[{self.node_id}] Clock now: {self.clock}")


def main():
    """Demonstrate a distributed key-value store scenario."""
    print("=" * 60)
    print("Distributed Key-Value Store with Vector Clocks")
    print("=" * 60)
    
    # Create three replicas
    replica_a = DistributedKVStore('A')
    replica_b = DistributedKVStore('B')
    replica_c = DistributedKVStore('C')
    
    # Initialize clocks with all nodes
    for replica in [replica_a, replica_b, replica_c]:
        for node in ['A', 'B', 'C']:
            replica.clock.add_process(node, 0)
    
    # Replica A writes a value
    print("\n--- Phase 1: Initial Write ---")
    replica_a.put('user:1', {'name': 'Alice', 'age': 30})
    
    # Sync A -> B
    print("\n--- Phase 2: Sync A -> B ---")
    replica_b.sync_from(replica_a)
    
    # Concurrent updates on A and B
    print("\n--- Phase 3: Concurrent Updates ---")
    replica_a.put('user:1', {'name': 'Alice', 'age': 31})  # A updates age
    replica_b.put('user:1', {'name': 'Alice Smith', 'age': 30})  # B updates name
    
    # Now A syncs with B - conflict!
    print("\n--- Phase 4: Conflict Detection ---")
    replica_a.sync_from(replica_b)
    
    # C syncs from A (which now has merged state)
    print("\n--- Phase 5: Third Replica Sync ---")
    for node in ['A', 'B', 'C']:
        replica_c.clock.add_process(node, 0)
    replica_c.sync_from(replica_a)
    
    print("\n--- Final State ---")
    print(f"Replica A: {replica_a.data}")
    print(f"Replica B: {replica_b.data}")
    print(f"Replica C: {replica_c.data}")


if __name__ == '__main__':
    main()