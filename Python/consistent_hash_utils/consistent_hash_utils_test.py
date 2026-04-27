"""
Tests for Consistent Hash Utilities

Comprehensive test suite for consistent hashing implementations.
"""

import unittest
import threading
import time
from collections import Counter
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    ConsistentHash,
    WeightedConsistentHash,
    RendezvousHash,
    JumpConsistentHash,
    MultiHash,
    Node,
    Migration,
    create_ring,
    distribute_keys,
    analyze_distribution,
    _hash_key,
)


class TestHashKey(unittest.TestCase):
    """Test the internal hash key function."""
    
    def test_md5_hash(self):
        """Test MD5 hashing."""
        h1 = _hash_key("test", "md5")
        h2 = _hash_key("test", "md5")
        self.assertEqual(h1, h2)
        self.assertIsInstance(h1, int)
        self.assertGreaterEqual(h1, 0)
        self.assertLess(h1, 2**32)
    
    def test_sha1_hash(self):
        """Test SHA1 hashing."""
        h1 = _hash_key("test", "sha1")
        h2 = _hash_key("test", "sha1")
        self.assertEqual(h1, h2)
    
    def test_sha256_hash(self):
        """Test SHA256 hashing."""
        h1 = _hash_key("test", "sha256")
        h2 = _hash_key("test", "sha256")
        self.assertEqual(h1, h2)
    
    def test_different_keys_different_hashes(self):
        """Test that different keys produce different hashes."""
        h1 = _hash_key("key1", "md5")
        h2 = _hash_key("key2", "md5")
        self.assertNotEqual(h1, h2)
    
    def test_invalid_algorithm(self):
        """Test invalid hash algorithm raises error."""
        with self.assertRaises(ValueError):
            _hash_key("test", "invalid")


class TestNode(unittest.TestCase):
    """Test Node dataclass."""
    
    def test_node_creation(self):
        """Test node creation."""
        node = Node(name="node1", weight=2, metadata={"host": "localhost"})
        self.assertEqual(node.name, "node1")
        self.assertEqual(node.weight, 2)
        self.assertEqual(node.metadata, {"host": "localhost"})
    
    def test_node_equality(self):
        """Test node equality based on name."""
        node1 = Node(name="node1")
        node2 = Node(name="node1")
        node3 = Node(name="node2")
        
        self.assertEqual(node1, node2)
        self.assertNotEqual(node1, node3)
    
    def test_node_hash(self):
        """Test node is hashable."""
        node = Node(name="node1")
        nodes_set = {node}
        self.assertIn(node, nodes_set)


class TestMigration(unittest.TestCase):
    """Test Migration dataclass."""
    
    def test_migration_creation(self):
        """Test migration creation."""
        m = Migration(key="key1", source_node="node1", target_node="node2")
        self.assertEqual(m.key, "key1")
        self.assertEqual(m.source_node, "node1")
        self.assertEqual(m.target_node, "node2")
    
    def test_migration_repr(self):
        """Test migration string representation."""
        m1 = Migration(key="key1", source_node="node1", target_node="node2")
        self.assertIn("node1", repr(m1))
        self.assertIn("node2", repr(m1))
        
        m2 = Migration(key="key1", source_node=None, target_node="node2")
        self.assertIn("-> node2", repr(m2))


class TestConsistentHash(unittest.TestCase):
    """Test ConsistentHash class."""
    
    def test_empty_ring(self):
        """Test empty ring returns None."""
        ring = ConsistentHash()
        self.assertIsNone(ring.get_node("key"))
        self.assertEqual(ring.node_count, 0)
        self.assertEqual(len(ring), 0)
    
    def test_single_node(self):
        """Test ring with single node."""
        ring = ConsistentHash()
        ring.add_node("node1")
        
        self.assertEqual(ring.node_count, 1)
        self.assertEqual(ring.get_node("key1"), "node1")
        self.assertEqual(ring.get_node("key2"), "node1")
        self.assertEqual(ring.get_node("key3"), "node1")
    
    def test_multiple_nodes(self):
        """Test ring with multiple nodes."""
        ring = ConsistentHash()
        ring.add_node("node1")
        ring.add_node("node2")
        ring.add_node("node3")
        
        self.assertEqual(ring.node_count, 3)
        self.assertIn("node1", ring.nodes)
        self.assertIn("node2", ring.nodes)
        self.assertIn("node3", ring.nodes)
    
    def test_consistent_mapping(self):
        """Test that same key always maps to same node."""
        ring = ConsistentHash()
        ring.add_node("node1")
        ring.add_node("node2")
        
        for _ in range(100):
            self.assertEqual(ring.get_node("key1"), ring.get_node("key1"))
    
    def test_remove_node(self):
        """Test removing a node."""
        ring = ConsistentHash()
        ring.add_node("node1")
        ring.add_node("node2")
        
        # Store some mappings
        key1_node = ring.get_node("key1")
        
        # Remove one node
        ring.remove_node("node1")
        
        self.assertEqual(ring.node_count, 1)
        self.assertNotIn("node1", ring)
        
        # All keys should now map to node2
        self.assertEqual(ring.get_node("key1"), "node2")
        self.assertEqual(ring.get_node("key2"), "node2")
    
    def test_remove_nonexistent_node(self):
        """Test removing non-existent node raises error."""
        ring = ConsistentHash()
        with self.assertRaises(KeyError):
            ring.remove_node("nonexistent")
    
    def test_add_duplicate_node(self):
        """Test adding duplicate node raises error."""
        ring = ConsistentHash()
        ring.add_node("node1")
        with self.assertRaises(ValueError):
            ring.add_node("node1")
    
    def test_get_nodes_replication(self):
        """Test getting multiple nodes for replication."""
        ring = ConsistentHash()
        ring.add_node("node1")
        ring.add_node("node2")
        ring.add_node("node3")
        
        nodes = ring.get_nodes("key1", count=2)
        self.assertEqual(len(nodes), 2)
        self.assertNotEqual(nodes[0], nodes[1])
    
    def test_get_nodes_more_than_available(self):
        """Test getting more nodes than available."""
        ring = ConsistentHash()
        ring.add_node("node1")
        ring.add_node("node2")
        
        nodes = ring.get_nodes("key1", count=5)
        self.assertEqual(len(nodes), 2)
    
    def test_get_nodes_empty_ring(self):
        """Test getting nodes from empty ring."""
        ring = ConsistentHash()
        nodes = ring.get_nodes("key1", count=2)
        self.assertEqual(len(nodes), 0)
    
    def test_distribution(self):
        """Test key distribution is reasonably even."""
        ring = ConsistentHash(virtual_nodes=100)
        ring.add_node("node1")
        ring.add_node("node2")
        ring.add_node("node3")
        
        keys = [f"key{i}" for i in range(1000)]
        distribution = ring.get_key_distribution(keys)
        
        # Each node should have roughly 1/3 of keys
        for node, count in distribution.items():
            self.assertGreater(count, 200)  # At least 20%
            self.assertLess(count, 500)  # At most 50%
    
    def test_node_metadata(self):
        """Test node metadata."""
        ring = ConsistentHash()
        ring.add_node("node1", metadata={"host": "192.168.1.1", "port": 6379})
        
        metadata = ring.get_node_metadata("node1")
        self.assertEqual(metadata["host"], "192.168.1.1")
        self.assertEqual(metadata["port"], 6379)
    
    def test_node_weight(self):
        """Test node weight."""
        ring = ConsistentHash()
        ring.add_node("node1", weight=3)
        
        self.assertEqual(ring.get_node_weight("node1"), 3)
    
    def test_ring_info(self):
        """Test ring info."""
        ring = ConsistentHash(virtual_nodes=100)
        ring.add_node("node1")
        ring.add_node("node2", weight=2)
        
        info = ring.get_ring_info()
        self.assertEqual(info["node_count"], 2)
        self.assertEqual(info["virtual_node_count"], 300)  # 100 + 100*2
        self.assertEqual(info["virtual_nodes_per_node"], 100)
    
    def test_clear(self):
        """Test clearing the ring."""
        ring = ConsistentHash()
        ring.add_node("node1")
        ring.add_node("node2")
        
        ring.clear()
        
        self.assertEqual(ring.node_count, 0)
        self.assertIsNone(ring.get_node("key"))
    
    def test_thread_safety(self):
        """Test thread safety."""
        ring = ConsistentHash()
        
        def add_nodes():
            for i in range(100):
                try:
                    ring.add_node(f"node{threading.current_thread().name}{i}")
                except ValueError:
                    pass
        
        threads = [threading.Thread(target=add_nodes, name=str(i)) for i in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        # Ring should have nodes
        self.assertGreater(ring.node_count, 0)
    
    def test_calculate_migration(self):
        """Test migration calculation."""
        ring = ConsistentHash()
        ring.add_node("node1")
        ring.add_node("node2")
        
        keys = [f"key{i}" for i in range(100)]
        migrations = ring.calculate_migration(keys, ["node3"], [])
        
        # Some keys should migrate to the new node
        migrated_to_node3 = [m for m in migrations if m.target_node == "node3"]
        self.assertGreater(len(migrated_to_node3), 0)
    
    def test_iteration(self):
        """Test iterating over nodes."""
        ring = ConsistentHash()
        ring.add_node("node1")
        ring.add_node("node2")
        ring.add_node("node3")
        
        nodes = list(ring)
        self.assertEqual(len(nodes), 3)
        self.assertIn("node1", nodes)
    
    def test_contains(self):
        """Test node membership."""
        ring = ConsistentHash()
        ring.add_node("node1")
        
        self.assertIn("node1", ring)
        self.assertNotIn("node2", ring)


class TestWeightedConsistentHash(unittest.TestCase):
    """Test WeightedConsistentHash class."""
    
    def test_weight_affects_distribution(self):
        """Test that higher weight means more keys."""
        ring = WeightedConsistentHash(virtual_nodes=100)
        ring.add_node("small", weight=1)
        ring.add_node("large", weight=3)
        
        keys = [f"key{i}" for i in range(1000)]
        distribution = ring.get_key_distribution(keys)
        
        # Large node should have roughly 3x more keys
        ratio = distribution["large"] / distribution["small"]
        self.assertGreater(ratio, 2)
        self.assertLess(ratio, 4)
    
    def test_zero_weight_raises(self):
        """Test that zero weight raises error."""
        ring = WeightedConsistentHash()
        with self.assertRaises(ValueError):
            ring.add_node("node1", weight=0)
    
    def test_negative_weight_raises(self):
        """Test that negative weight raises error."""
        ring = WeightedConsistentHash()
        with self.assertRaises(ValueError):
            ring.add_node("node1", weight=-1)
    
    def test_weight_distribution(self):
        """Test weight distribution calculation."""
        ring = WeightedConsistentHash()
        ring.add_node("node1", weight=1)
        ring.add_node("node2", weight=3)
        
        dist = ring.get_weight_distribution()
        self.assertAlmostEqual(dist["node1"], 0.25, places=2)
        self.assertAlmostEqual(dist["node2"], 0.75, places=2)
    
    def test_rebalance(self):
        """Test rebalancing."""
        ring = WeightedConsistentHash()
        ring.add_node("node1")
        ring.add_node("node2")
        
        keys = [f"key{i}" for i in range(100)]
        assignments = ring.rebalance(keys)
        
        total_assigned = sum(len(v) for v in assignments.values())
        self.assertEqual(total_assigned, 100)


class TestRendezvousHash(unittest.TestCase):
    """Test RendezvousHash class."""
    
    def test_empty(self):
        """Test empty hash returns None."""
        rh = RendezvousHash()
        self.assertIsNone(rh.get_node("key"))
        self.assertEqual(rh.node_count, 0)
    
    def test_single_node(self):
        """Test single node always returns that node."""
        rh = RendezvousHash()
        rh.add_node("node1")
        
        self.assertEqual(rh.get_node("key1"), "node1")
        self.assertEqual(rh.get_node("key2"), "node1")
    
    def test_multiple_nodes(self):
        """Test multiple nodes distribution."""
        rh = RendezvousHash()
        rh.add_node("node1")
        rh.add_node("node2")
        rh.add_node("node3")
        
        keys = [f"key{i}" for i in range(300)]
        distribution = Counter(rh.get_node(k) for k in keys)
        
        # Each node should get roughly 1/3 of keys
        for node in ["node1", "node2", "node3"]:
            self.assertGreater(distribution[node], 50)
    
    def test_consistent(self):
        """Test consistency."""
        rh = RendezvousHash()
        rh.add_node("node1")
        rh.add_node("node2")
        
        for _ in range(10):
            self.assertEqual(rh.get_node("key1"), rh.get_node("key1"))
    
    def test_weighted(self):
        """Test weighted nodes."""
        rh = RendezvousHash()
        rh.add_node("small", weight=1)
        rh.add_node("large", weight=3)
        
        keys = [f"key{i}" for i in range(1000)]
        distribution = Counter(rh.get_node(k) for k in keys)
        
        # Large should get roughly 3x more
        ratio = distribution["large"] / distribution["small"]
        self.assertGreater(ratio, 2)
    
    def test_remove_node(self):
        """Test removing a node."""
        rh = RendezvousHash()
        rh.add_node("node1")
        rh.add_node("node2")
        
        key1_node = rh.get_node("key1")
        rh.remove_node("node1")
        
        self.assertEqual(rh.node_count, 1)
        self.assertNotIn("node1", rh)
    
    def test_get_nodes_multiple(self):
        """Test getting multiple nodes."""
        rh = RendezvousHash()
        rh.add_node("node1")
        rh.add_node("node2")
        rh.add_node("node3")
        
        nodes = rh.get_nodes("key1", count=2)
        self.assertEqual(len(nodes), 2)
        self.assertNotEqual(nodes[0], nodes[1])
    
    def test_clear(self):
        """Test clearing all nodes."""
        rh = RendezvousHash()
        rh.add_node("node1")
        rh.add_node("node2")
        
        rh.clear()
        
        self.assertEqual(rh.node_count, 0)
        self.assertIsNone(rh.get_node("key"))


class TestJumpConsistentHash(unittest.TestCase):
    """Test JumpConsistentHash class."""
    
    def test_bucket_range(self):
        """Test bucket is always in valid range."""
        jh = JumpConsistentHash(num_buckets=10)
        
        for i in range(1000):
            bucket = jh.get_bucket(f"key{i}")
            self.assertGreaterEqual(bucket, 0)
            self.assertLess(bucket, 10)
    
    def test_consistency(self):
        """Test same key always gets same bucket."""
        jh = JumpConsistentHash(num_buckets=10)
        
        for _ in range(100):
            self.assertEqual(jh.get_bucket("key1"), jh.get_bucket("key1"))
    
    def test_distribution(self):
        """Test even distribution."""
        jh = JumpConsistentHash(num_buckets=10)
        
        keys = [f"key{i}" for i in range(10000)]
        distribution = jh.get_distribution(keys)
        
        # Each bucket should have roughly 1000 keys
        for bucket, count in distribution.items():
            self.assertGreater(count, 500)
            self.assertLess(count, 1500)
    
    def test_resize(self):
        """Test resizing buckets."""
        jh = JumpConsistentHash(num_buckets=5)
        old_bucket = jh.get_bucket("key1")
        
        jh.resize(10)
        self.assertEqual(jh.num_buckets, 10)
    
    def test_invalid_num_buckets(self):
        """Test invalid num_buckets raises error."""
        with self.assertRaises(ValueError):
            JumpConsistentHash(num_buckets=0)
        
        with self.assertRaises(ValueError):
            JumpConsistentHash(num_buckets=-1)
    
    def test_int_key(self):
        """Test integer key."""
        jh = JumpConsistentHash(num_buckets=10)
        
        bucket = jh.get_bucket_for_int(12345)
        self.assertGreaterEqual(bucket, 0)
        self.assertLess(bucket, 10)
    
    def test_len(self):
        """Test length returns num_buckets."""
        jh = JumpConsistentHash(num_buckets=10)
        self.assertEqual(len(jh), 10)


class TestMultiHash(unittest.TestCase):
    """Test MultiHash class."""
    
    def test_empty(self):
        """Test empty multi-hash."""
        mh = MultiHash()
        self.assertEqual(mh.node_count, 0)
    
    def test_single_node(self):
        """Test single node."""
        mh = MultiHash()
        mh.add_node("node1")
        
        self.assertEqual(mh.get_primary_node("key"), "node1")
        self.assertEqual(mh.get_replica_nodes("key"), ["node1"])
    
    def test_multiple_nodes_replication(self):
        """Test multiple nodes with replication."""
        mh = MultiHash(num_replicas=3)
        mh.add_node("node1")
        mh.add_node("node2")
        mh.add_node("node3")
        
        replicas = mh.get_replica_nodes("key1")
        self.assertEqual(len(replicas), 3)
        
        # All replicas should be different
        self.assertEqual(len(set(replicas)), 3)
    
    def test_fallback(self):
        """Test fallback with unavailable nodes."""
        mh = MultiHash(num_replicas=3)
        mh.add_node("node1")
        mh.add_node("node2")
        mh.add_node("node3")
        
        # Get nodes with node1 unavailable
        nodes = mh.get_nodes_with_fallback("key1", unavailable={"node1"}, count=2)
        
        # Should return nodes that aren't node1
        for node in nodes:
            self.assertNotEqual(node, "node1")
    
    def test_remove_node(self):
        """Test removing a node."""
        mh = MultiHash()
        mh.add_node("node1")
        mh.add_node("node2")
        
        mh.remove_node("node1")
        
        self.assertEqual(mh.node_count, 1)
        self.assertNotIn("node1", mh)
    
    def test_clear(self):
        """Test clearing all nodes."""
        mh = MultiHash()
        mh.add_node("node1")
        mh.add_node("node2")
        
        mh.clear()
        
        self.assertEqual(mh.node_count, 0)


class TestConvenienceFunctions(unittest.TestCase):
    """Test convenience functions."""
    
    def test_create_ring(self):
        """Test create_ring function."""
        ring = create_ring(["node1", "node2", "node3"])
        
        self.assertEqual(ring.node_count, 3)
        self.assertIsNotNone(ring.get_node("key"))
    
    def test_distribute_keys(self):
        """Test distribute_keys function."""
        keys = [f"key{i}" for i in range(100)]
        distribution = distribute_keys(keys, ["node1", "node2", "node3"])
        
        total = sum(len(v) for v in distribution.values())
        self.assertEqual(total, 100)
    
    def test_analyze_distribution(self):
        """Test analyze_distribution function."""
        keys = [f"key{i}" for i in range(1000)]
        analysis = analyze_distribution(keys, ["node1", "node2", "node3"])
        
        self.assertEqual(analysis["total_keys"], 1000)
        self.assertEqual(analysis["num_nodes"], 3)
        self.assertIn("distribution", analysis)
        self.assertIn("stats", analysis)
        self.assertIn("imbalance_ratio", analysis)
        
        # Check stats
        stats = analysis["stats"]
        self.assertIn("min", stats)
        self.assertIn("max", stats)
        self.assertIn("mean", stats)
        self.assertIn("std_dev", stats)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling."""
    
    def test_invalid_virtual_nodes(self):
        """Test invalid virtual_nodes raises error."""
        with self.assertRaises(ValueError):
            ConsistentHash(virtual_nodes=0)
        
        with self.assertRaises(ValueError):
            ConsistentHash(virtual_nodes=-1)
    
    def test_large_key(self):
        """Test with very large key."""
        ring = ConsistentHash()
        ring.add_node("node1")
        
        large_key = "x" * 10000
        self.assertEqual(ring.get_node(large_key), "node1")
    
    def test_unicode_key(self):
        """Test with unicode key."""
        ring = ConsistentHash()
        ring.add_node("node1")
        ring.add_node("node2")
        
        node = ring.get_node("测试键")
        self.assertIn(node, ["node1", "node2"])
    
    def test_special_characters_in_node_name(self):
        """Test special characters in node name."""
        ring = ConsistentHash()
        ring.add_node("node-1_test.example.com:8080")
        
        self.assertEqual(ring.node_count, 1)
        self.assertIsNotNone(ring.get_node("key"))


class TestPerformance(unittest.TestCase):
    """Performance tests."""
    
    def test_large_ring_performance(self):
        """Test performance with many nodes."""
        ring = ConsistentHash(virtual_nodes=100)
        
        # Add 100 nodes
        start = time.time()
        for i in range(100):
            ring.add_node(f"node{i}")
        add_time = time.time() - start
        
        self.assertLess(add_time, 5.0)  # Should be fast
        
        # Lookups
        start = time.time()
        for i in range(10000):
            ring.get_node(f"key{i}")
        lookup_time = time.time() - start
        
        self.assertLess(lookup_time, 2.0)  # Should be fast
    
    def test_jump_hash_performance(self):
        """Test jump hash performance."""
        jh = JumpConsistentHash(num_buckets=1000)
        
        start = time.time()
        for i in range(100000):
            jh.get_bucket(f"key{i}")
        elapsed = time.time() - start
        
        self.assertLess(elapsed, 1.0)  # Very fast


if __name__ == "__main__":
    unittest.main(verbosity=2)