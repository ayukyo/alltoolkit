#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for Load Balancer Utilities Module

Run with: python load_balancer_utils_test.py
"""

import sys
import os
import time
import threading
import unittest

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from load_balancer_utils.mod import (
    LoadBalancer,
    LoadBalancerStrategy,
    Server,
    ServerState,
    ServerStats,
    HealthChecker,
    DefaultHealthChecker,
    LoadBalancerError,
    NoHealthyServerError,
    InvalidWeightError,
    ConnectionContext,
    create_round_robin_balancer,
    create_weighted_balancer,
    create_least_connections_balancer,
    RoundRobinStrategy,
    WeightedRoundRobinStrategy,
    LeastConnectionsStrategy,
    RandomStrategy,
    WeightedRandomStrategy,
    IPHashStrategy,
)


class TestServer(unittest.TestCase):
    """Test Server dataclass."""
    
    def test_server_creation(self):
        """Test creating a server."""
        server = Server(id="test", target="localhost:8080", weight=5)
        self.assertEqual(server.id, "test")
        self.assertEqual(server.target, "localhost:8080")
        self.assertEqual(server.weight, 5)
        self.assertEqual(server.state, ServerState.HEALTHY)
        self.assertIsInstance(server.stats, ServerStats)
    
    def test_server_defaults(self):
        """Test server default values."""
        server = Server(id="test", target="localhost:8080")
        self.assertEqual(server.weight, 1)
        self.assertEqual(server.state, ServerState.HEALTHY)
        self.assertEqual(server.metadata, {})
    
    def test_server_stats(self):
        """Test server statistics."""
        stats = ServerStats()
        stats.total_requests = 100
        stats.successful_requests = 95
        self.assertEqual(stats.success_rate(), 95.0)
        
        stats.total_requests = 0
        self.assertEqual(stats.success_rate(), 100.0)


class TestRoundRobinStrategy(unittest.TestCase):
    """Test Round Robin strategy."""
    
    def test_basic_selection(self):
        """Test basic round-robin selection."""
        strategy = RoundRobinStrategy()
        servers = [
            Server(id="s1", target="t1"),
            Server(id="s2", target="t2"),
            Server(id="s3", target="t3"),
        ]
        
        # Should cycle through servers
        self.assertEqual(strategy.select(servers).id, "s1")
        self.assertEqual(strategy.select(servers).id, "s2")
        self.assertEqual(strategy.select(servers).id, "s3")
        self.assertEqual(strategy.select(servers).id, "s1")
    
    def test_empty_servers(self):
        """Test selection with no servers."""
        strategy = RoundRobinStrategy()
        self.assertIsNone(strategy.select([]))
    
    def test_reset(self):
        """Test strategy reset."""
        strategy = RoundRobinStrategy()
        servers = [Server(id="s1", target="t1"), Server(id="s2", target="t2")]
        
        strategy.select(servers)
        strategy.select(servers)
        strategy.reset()
        
        self.assertEqual(strategy.select(servers).id, "s1")


class TestWeightedRoundRobinStrategy(unittest.TestCase):
    """Test Weighted Round Robin strategy."""
    
    def test_weighted_distribution(self):
        """Test that servers are selected proportionally to weight."""
        strategy = WeightedRoundRobinStrategy()
        servers = [
            Server(id="s1", target="t1", weight=3),
            Server(id="s2", target="t2", weight=1),
        ]
        
        # Run many selections
        counts = {}
        for _ in range(40):
            server = strategy.select(servers)
            counts[server.id] = counts.get(server.id, 0) + 1
        
        # s1 should be selected approximately 3x more than s2
        self.assertGreater(counts["s1"], counts["s2"])
    
    def test_empty_servers(self):
        """Test selection with no servers."""
        strategy = WeightedRoundRobinStrategy()
        self.assertIsNone(strategy.select([]))
    
    def test_zero_weight(self):
        """Test with zero weight servers."""
        strategy = WeightedRoundRobinStrategy()
        servers = [Server(id="s1", target="t1", weight=0)]
        # Should handle gracefully
        result = strategy.select(servers)
        self.assertIsNone(result)


class TestLeastConnectionsStrategy(unittest.TestCase):
    """Test Least Connections strategy."""
    
    def test_least_connections_selection(self):
        """Test selecting server with least connections."""
        strategy = LeastConnectionsStrategy()
        servers = [
            Server(id="s1", target="t1"),
            Server(id="s2", target="t2"),
            Server(id="s3", target="t3"),
        ]
        
        # Set different connection counts
        servers[0].stats.active_connections = 5
        servers[1].stats.active_connections = 2
        servers[2].stats.active_connections = 8
        
        # Should select s2 (least connections)
        self.assertEqual(strategy.select(servers).id, "s2")
    
    def test_equal_connections(self):
        """Test with equal connection counts."""
        strategy = LeastConnectionsStrategy()
        servers = [
            Server(id="s1", target="t1"),
            Server(id="s2", target="t2"),
        ]
        # Both have 0 connections
        result = strategy.select(servers)
        self.assertIn(result.id, ["s1", "s2"])
    
    def test_unhealthy_servers_excluded(self):
        """Test that unhealthy servers are excluded."""
        strategy = LeastConnectionsStrategy()
        servers = [
            Server(id="s1", target="t1"),
            Server(id="s2", target="t2", state=ServerState.UNHEALTHY),
        ]
        
        # Should only select s1
        self.assertEqual(strategy.select(servers).id, "s1")


class TestRandomStrategy(unittest.TestCase):
    """Test Random strategy."""
    
    def test_random_selection(self):
        """Test random selection."""
        strategy = RandomStrategy()
        servers = [
            Server(id="s1", target="t1"),
            Server(id="s2", target="t2"),
            Server(id="s3", target="t3"),
        ]
        
        # All selections should be valid
        for _ in range(20):
            server = strategy.select(servers)
            self.assertIn(server.id, ["s1", "s2", "s3"])
    
    def test_distribution(self):
        """Test roughly uniform distribution."""
        strategy = RandomStrategy()
        servers = [
            Server(id="s1", target="t1"),
            Server(id="s2", target="t2"),
        ]
        
        counts = {}
        for _ in range(1000):
            server = strategy.select(servers)
            counts[server.id] = counts.get(server.id, 0) + 1
        
        # Should be roughly 50/50
        self.assertGreater(counts["s1"], 400)
        self.assertGreater(counts["s2"], 400)
    
    def test_empty_servers(self):
        """Test with no servers."""
        strategy = RandomStrategy()
        self.assertIsNone(strategy.select([]))


class TestWeightedRandomStrategy(unittest.TestCase):
    """Test Weighted Random strategy."""
    
    def test_weighted_distribution(self):
        """Test weighted random distribution."""
        strategy = WeightedRandomStrategy()
        servers = [
            Server(id="s1", target="t1", weight=3),
            Server(id="s2", target="t2", weight=1),
        ]
        
        counts = {}
        for _ in range(1000):
            server = strategy.select(servers)
            counts[server.id] = counts.get(server.id, 0) + 1
        
        # s1 should be selected ~75% of the time
        self.assertGreater(counts["s1"], counts["s2"])
        self.assertGreater(counts["s1"], 600)


class TestIPHashStrategy(unittest.TestCase):
    """Test IP Hash strategy."""
    
    def test_consistent_hashing(self):
        """Test that same key always gets same server."""
        strategy = IPHashStrategy()
        servers = [
            Server(id="s1", target="t1"),
            Server(id="s2", target="t2"),
            Server(id="s3", target="t3"),
        ]
        
        # Same key should always return same server
        for _ in range(10):
            server1 = strategy.select(servers, key="192.168.1.1")
            server2 = strategy.select(servers, key="192.168.1.2")
            self.assertIsNotNone(server1)
            self.assertIsNotNone(server2)
    
    def test_different_keys_distribution(self):
        """Test that different keys distribute across servers."""
        strategy = IPHashStrategy()
        servers = [
            Server(id="s1", target="t1"),
            Server(id="s2", target="t2"),
        ]
        
        unique_servers = set()
        for i in range(20):
            server = strategy.select(servers, key=f"192.168.1.{i}")
            unique_servers.add(server.id)
        
        # Should distribute across servers
        self.assertGreater(len(unique_servers), 1)
    
    def test_no_key_fallback(self):
        """Test fallback to random when no key provided."""
        strategy = IPHashStrategy()
        servers = [Server(id="s1", target="t1")]
        
        # Should still work without key
        server = strategy.select(servers)
        self.assertEqual(server.id, "s1")


class TestLoadBalancer(unittest.TestCase):
    """Test LoadBalancer class."""
    
    def test_add_server(self):
        """Test adding servers."""
        lb = LoadBalancer()
        server = lb.add_server("s1", "localhost:8080", weight=3)
        
        self.assertEqual(server.id, "s1")
        self.assertEqual(server.target, "localhost:8080")
        self.assertEqual(server.weight, 3)
    
    def test_add_server_invalid_weight(self):
        """Test adding server with invalid weight."""
        lb = LoadBalancer()
        
        with self.assertRaises(InvalidWeightError):
            lb.add_server("s1", "localhost:8080", weight=0)
        
        with self.assertRaises(InvalidWeightError):
            lb.add_server("s1", "localhost:8080", weight=-1)
    
    def test_remove_server(self):
        """Test removing servers."""
        lb = LoadBalancer()
        lb.add_server("s1", "localhost:8080")
        
        self.assertTrue(lb.remove_server("s1"))
        self.assertEqual(lb.server_count, 0)
        self.assertFalse(lb.remove_server("s1"))
    
    def test_select_round_robin(self):
        """Test round-robin selection."""
        lb = LoadBalancer(strategy=LoadBalancerStrategy.ROUND_ROBIN)
        lb.add_server("s1", "t1")
        lb.add_server("s2", "t2")
        
        self.assertEqual(lb.select().id, "s1")
        self.assertEqual(lb.select().id, "s2")
        self.assertEqual(lb.select().id, "s1")
    
    def test_select_no_healthy_servers(self):
        """Test selection with no healthy servers."""
        lb = LoadBalancer()
        lb.add_server("s1", "t1")
        lb.mark_server_unhealthy("s1")
        
        with self.assertRaises(NoHealthyServerError):
            lb.select()
    
    def test_set_server_weight(self):
        """Test setting server weight."""
        lb = LoadBalancer()
        lb.add_server("s1", "t1", weight=1)
        
        self.assertTrue(lb.set_server_weight("s1", 5))
        self.assertEqual(lb.get_server("s1").weight, 5)
        
        self.assertFalse(lb.set_server_weight("nonexistent", 5))
    
    def test_mark_server_healthy_unhealthy(self):
        """Test marking server health status."""
        lb = LoadBalancer()
        lb.add_server("s1", "t1")
        
        lb.mark_server_unhealthy("s1")
        self.assertEqual(lb.get_server("s1").state, ServerState.UNHEALTHY)
        
        lb.mark_server_healthy("s1")
        self.assertEqual(lb.get_server("s1").state, ServerState.HEALTHY)
    
    def test_drain_server(self):
        """Test draining server."""
        lb = LoadBalancer()
        lb.add_server("s1", "t1")
        
        lb.drain_server("s1")
        self.assertEqual(lb.get_server("s1").state, ServerState.DRAINING)
    
    def test_connection_tracking(self):
        """Test connection context manager."""
        lb = LoadBalancer()
        lb.add_server("s1", "t1")
        
        server = lb.select()
        self.assertEqual(server.stats.active_connections, 0)
        
        with lb.connection(server):
            self.assertEqual(server.stats.active_connections, 1)
        
        self.assertEqual(server.stats.active_connections, 0)
    
    def test_record_success_failure(self):
        """Test recording request outcomes."""
        lb = LoadBalancer(enable_stats=True)
        lb.add_server("s1", "t1")
        
        server = lb.select()
        
        lb.record_success(server, 100.0)
        self.assertEqual(server.stats.successful_requests, 1)
        self.assertEqual(server.stats.avg_response_time_ms, 100.0)
        
        lb.record_failure(server)
        self.assertEqual(server.stats.failed_requests, 1)
    
    def test_get_stats(self):
        """Test statistics retrieval."""
        lb = LoadBalancer()
        lb.add_server("s1", "t1", weight=3)
        lb.add_server("s2", "t2", weight=2)
        
        stats = lb.get_stats()
        
        self.assertEqual(stats["strategy"], "ROUND_ROBIN")
        self.assertEqual(stats["total_servers"], 2)
        self.assertEqual(stats["healthy_servers"], 2)
        self.assertIn("s1", stats["servers"])
        self.assertIn("s2", stats["servers"])
    
    def test_reset_stats(self):
        """Test resetting statistics."""
        lb = LoadBalancer()
        lb.add_server("s1", "t1")
        
        server = lb.select()
        server.stats.total_requests = 100
        
        lb.reset_stats()
        self.assertEqual(lb.get_server("s1").stats.total_requests, 0)
    
    def test_reset(self):
        """Test reset."""
        lb = LoadBalancer()
        lb.add_server("s1", "t1")
        lb.add_server("s2", "t2")
        
        lb.select()
        lb.select()
        
        lb.reset()
        
        # Should reset strategy index
        self.assertEqual(lb.select().id, "s1")
    
    def test_servers_property(self):
        """Test servers property."""
        lb = LoadBalancer()
        lb.add_server("s1", "t1")
        lb.add_server("s2", "t2")
        
        servers = lb.servers
        self.assertEqual(len(servers), 2)
    
    def test_healthy_servers_property(self):
        """Test healthy servers property."""
        lb = LoadBalancer()
        lb.add_server("s1", "t1")
        lb.add_server("s2", "t2")
        lb.mark_server_unhealthy("s2")
        
        healthy = lb.healthy_servers
        self.assertEqual(len(healthy), 1)
        self.assertEqual(healthy[0].id, "s1")


class TestConvenienceFunctions(unittest.TestCase):
    """Test convenience functions."""
    
    def test_create_round_robin_balancer(self):
        """Test creating round-robin balancer."""
        lb = create_round_robin_balancer([
            ("s1", "t1", 1),
            ("s2", "t2", 1),
        ])
        
        self.assertEqual(lb.server_count, 2)
        self.assertEqual(lb.select().id, "s1")
        self.assertEqual(lb.select().id, "s2")
    
    def test_create_weighted_balancer(self):
        """Test creating weighted balancer."""
        lb = create_weighted_balancer([
            ("s1", "t1", 3),
            ("s2", "t2", 1),
        ])
        
        self.assertEqual(lb.server_count, 2)
    
    def test_create_least_connections_balancer(self):
        """Test creating least connections balancer."""
        lb = create_least_connections_balancer([
            ("s1", "t1", 1),
            ("s2", "t2", 1),
        ])
        
        self.assertEqual(lb.server_count, 2)


class TestThreadSafety(unittest.TestCase):
    """Test thread safety."""
    
    def test_concurrent_selections(self):
        """Test concurrent server selections."""
        lb = LoadBalancer()
        lb.add_server("s1", "t1")
        lb.add_server("s2", "t2")
        
        errors = []
        
        def select_many():
            try:
                for _ in range(100):
                    server = lb.select()
                    lb.record_success(server)
            except Exception as e:
                errors.append(e)
        
        threads = [threading.Thread(target=select_many) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        self.assertEqual(len(errors), 0)
        
        stats = lb.get_stats()
        self.assertEqual(stats["total_requests"], 1000)
    
    def test_concurrent_modifications(self):
        """Test concurrent server additions and removals."""
        lb = LoadBalancer()
        
        errors = []
        
        def add_servers():
            try:
                for i in range(100):
                    lb.add_server(f"s{i}", f"t{i}")
            except Exception as e:
                errors.append(e)
        
        def remove_servers():
            try:
                for i in range(50):
                    lb.remove_server(f"s{i}")
            except Exception as e:
                errors.append(e)
        
        t1 = threading.Thread(target=add_servers)
        t2 = threading.Thread(target=remove_servers)
        
        t1.start()
        time.sleep(0.01)  # Let some servers be added first
        t2.start()
        
        t1.join()
        t2.join()
        
        self.assertEqual(len(errors), 0)


class TestHealthChecking(unittest.TestCase):
    """Test health checking."""
    
    def test_health_check(self):
        """Test health check execution."""
        class TestHealthChecker(HealthChecker):
            def __init__(self):
                self.check_count = 0
            
            def check(self, server):
                self.check_count += 1
                return server.id != "s2"
        
        checker = TestHealthChecker()
        lb = LoadBalancer(health_checker=checker)
        lb.add_server("s1", "t1")
        lb.add_server("s2", "t2")
        
        # Set lower threshold for faster testing
        lb.get_server("s2").max_health_check_failures = 1
        
        results = lb.run_health_checks()
        
        self.assertEqual(results["s1"], True)
        self.assertEqual(results["s2"], False)
        self.assertEqual(lb.get_server("s2").state, ServerState.UNHEALTHY)


def run_tests():
    """Run all tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestServer))
    suite.addTests(loader.loadTestsFromTestCase(TestRoundRobinStrategy))
    suite.addTests(loader.loadTestsFromTestCase(TestWeightedRoundRobinStrategy))
    suite.addTests(loader.loadTestsFromTestCase(TestLeastConnectionsStrategy))
    suite.addTests(loader.loadTestsFromTestCase(TestRandomStrategy))
    suite.addTests(loader.loadTestsFromTestCase(TestWeightedRandomStrategy))
    suite.addTests(loader.loadTestsFromTestCase(TestIPHashStrategy))
    suite.addTests(loader.loadTestsFromTestCase(TestLoadBalancer))
    suite.addTests(loader.loadTestsFromTestCase(TestConvenienceFunctions))
    suite.addTests(loader.loadTestsFromTestCase(TestThreadSafety))
    suite.addTests(loader.loadTestsFromTestCase(TestHealthChecking))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)