#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AllToolkit - System Monitoring Utilities Test Suite

Comprehensive tests for monitoring_utils module.
Run with: python monitoring_utils_test.py
"""

import unittest
import sys
import os
import time
from typing import Optional

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from monitoring_utils.mod import (
    # Main monitor class
    SystemMonitor,
    # Data classes
    CPUStats, MemoryStats, DiskStats, NetworkInterfaceStats, ProcessStats,
    # Convenience functions
    get_cpu_stats, get_memory_stats, get_disk_usage, get_network_stats,
    get_process_list, get_process_info, get_top_processes, get_system_info,
    get_all_stats, get_uptime, get_hostname, get_cpu_stats_percent,
    # Module info
    version, features
)


# =============================================================================
# Test Constants
# =============================================================================

TEST_PID = 1  # Usually init/systemd, always exists


# =============================================================================
# Test Helper Classes
# =============================================================================

class TestDataClasses(unittest.TestCase):
    """Test data class functionality."""
    
    def test_cpu_stats_default(self):
        """Test CPUStats default values."""
        stats = CPUStats()
        self.assertEqual(stats.user, 0.0)
        self.assertEqual(stats.system, 0.0)
        self.assertEqual(stats.idle, 0.0)
        self.assertEqual(stats.cores, 1)
        self.assertEqual(stats.load_avg, (0.0, 0.0, 0.0))
    
    def test_cpu_stats_to_dict(self):
        """Test CPUStats to_dict method."""
        stats = CPUStats(
            user=10.0,
            system=5.0,
            idle=85.0,
            cores=4,
            load_avg=(1.5, 1.2, 0.8)
        )
        result = stats.to_dict()
        self.assertIsInstance(result, dict)
        self.assertEqual(result["user"], 10.0)
        self.assertEqual(result["cores"], 4)
        self.assertEqual(result["load_avg"], [1.5, 1.2, 0.8])
    
    def test_memory_stats_default(self):
        """Test MemoryStats default values."""
        stats = MemoryStats()
        self.assertEqual(stats.total, 0)
        self.assertEqual(stats.available, 0)
        self.assertEqual(stats.usage_percent, 0.0)
    
    def test_memory_stats_to_dict(self):
        """Test MemoryStats to_dict method."""
        stats = MemoryStats(
            total=16 * 1024**3,  # 16 GB
            available=8 * 1024**3,  # 8 GB
            used=8 * 1024**3
        )
        result = stats.to_dict()
        self.assertIsInstance(result, dict)
        self.assertEqual(result["total"], 16 * 1024**3)
    
    def test_memory_stats_properties(self):
        """Test MemoryStats property calculations."""
        stats = MemoryStats(total=16 * 1024**3)  # 16 GB
        self.assertAlmostEqual(stats.total_gb, 16.0, places=2)
    
    def test_network_interface_stats_to_dict(self):
        """Test NetworkInterfaceStats to_dict method."""
        stats = NetworkInterfaceStats(
            name="eth0",
            rx_bytes=1000000,
            tx_bytes=500000
        )
        result = stats.to_dict()
        self.assertEqual(result["name"], "eth0")
        self.assertEqual(result["rx_bytes"], 1000000)
    
    def test_process_stats_to_dict(self):
        """Test ProcessStats to_dict method."""
        stats = ProcessStats(
            pid=1234,
            name="test_process",
            cpu_percent=25.5,
            memory_percent=5.2
        )
        result = stats.to_dict()
        self.assertEqual(result["pid"], 1234)
        self.assertEqual(result["name"], "test_process")


class TestSystemMonitor(unittest.TestCase):
    """Test SystemMonitor class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.monitor = SystemMonitor()
    
    def test_init(self):
        """Test SystemMonitor initialization."""
        monitor = SystemMonitor()
        self.assertIsNotNone(monitor)
    
    def test_get_hostname(self):
        """Test getting hostname."""
        hostname = self.monitor.get_hostname()
        self.assertIsInstance(hostname, str)
        self.assertGreater(len(hostname), 0)
    
    def test_get_uptime(self):
        """Test getting uptime."""
        uptime = self.monitor.get_uptime()
        self.assertIsInstance(uptime, float)
        self.assertGreaterEqual(uptime, 0.0)
    
    def test_get_cpu_stats(self):
        """Test getting CPU statistics."""
        stats = self.monitor.get_cpu_stats()
        self.assertIsInstance(stats, CPUStats)
        self.assertGreaterEqual(stats.cores, 1)
        self.assertIsInstance(stats.load_avg, tuple)
        self.assertEqual(len(stats.load_avg), 3)
    
    def test_get_cpu_stats_percent(self):
        """Test getting CPU usage percentage."""
        stats = self.monitor.get_cpu_stats_percent(interval=0.1)
        self.assertIsInstance(stats, CPUStats)
        self.assertGreaterEqual(stats.usage_percent, 0.0)
        self.assertLessEqual(stats.usage_percent, 100.0 * stats.cores)
    
    def test_get_memory_stats(self):
        """Test getting memory statistics."""
        stats = self.monitor.get_memory_stats()
        self.assertIsInstance(stats, MemoryStats)
        self.assertGreater(stats.total, 0)
        self.assertGreaterEqual(stats.available, 0)
        self.assertGreaterEqual(stats.usage_percent, 0.0)
        self.assertLessEqual(stats.usage_percent, 100.0)
    
    def test_get_disk_usage(self):
        """Test getting disk usage."""
        usage = self.monitor.get_disk_usage("/")
        self.assertIsInstance(usage, dict)
        self.assertEqual(usage["path"], "/")
        self.assertIn("total", usage)
        self.assertIn("used", usage)
        self.assertIn("available", usage)
    
    def test_get_disk_usage_custom_path(self):
        """Test getting disk usage for custom path."""
        usage = self.monitor.get_disk_usage("/tmp")
        self.assertIsInstance(usage, dict)
        self.assertEqual(usage["path"], "/tmp")
    
    def test_get_network_stats(self):
        """Test getting network statistics."""
        stats = self.monitor.get_network_stats()
        self.assertIsInstance(stats, list)
        # Should have at least one interface (lo)
        self.assertGreater(len(stats), 0)
        for iface in stats:
            self.assertIsInstance(iface, NetworkInterfaceStats)
            self.assertIsInstance(iface.name, str)
    
    def test_get_process_list(self):
        """Test getting process list."""
        processes = self.monitor.get_process_list()
        self.assertIsInstance(processes, list)
        # Should have at least one process
        self.assertGreater(len(processes), 0)
        for proc in processes:
            self.assertIsInstance(proc, ProcessStats)
            self.assertGreater(proc.pid, 0)
    
    def test_get_process_info(self):
        """Test getting specific process info."""
        proc = self.monitor.get_process_info(TEST_PID)
        if proc:  # May return None if PID doesn't exist or no permission
            self.assertIsInstance(proc, ProcessStats)
            self.assertEqual(proc.pid, TEST_PID)
    
    def test_get_process_info_nonexistent(self):
        """Test getting info for non-existent process."""
        # Use a very high PID that likely doesn't exist
        proc = self.monitor.get_process_info(999999)
        self.assertIsNone(proc)
    
    def test_get_top_processes_cpu(self):
        """Test getting top processes by CPU."""
        processes = self.monitor.get_top_processes(5, "cpu")
        self.assertIsInstance(processes, list)
        self.assertLessEqual(len(processes), 5)
    
    def test_get_top_processes_memory(self):
        """Test getting top processes by memory."""
        processes = self.monitor.get_top_processes(5, "memory")
        self.assertIsInstance(processes, list)
        self.assertLessEqual(len(processes), 5)
    
    def test_get_system_info(self):
        """Test getting system information."""
        info = self.monitor.get_system_info()
        self.assertIsInstance(info, dict)
        self.assertIn("hostname", info)
        self.assertIn("platform", info)
        self.assertIn("cpu_count", info)
        self.assertIn("uptime", info)
        self.assertGreater(info["cpu_count"], 0)
    
    def test_get_all_stats(self):
        """Test getting all statistics."""
        stats = self.monitor.get_all_stats()
        self.assertIsInstance(stats, dict)
        self.assertIn("system", stats)
        self.assertIn("cpu", stats)
        self.assertIn("memory", stats)
        self.assertIn("disk", stats)
        self.assertIn("network", stats)
        self.assertIn("timestamp", stats)


class TestConvenienceFunctions(unittest.TestCase):
    """Test module-level convenience functions."""
    
    def test_get_cpu_stats(self):
        """Test get_cpu_stats function."""
        stats = get_cpu_stats()
        self.assertIsInstance(stats, CPUStats)
    
    def test_get_memory_stats(self):
        """Test get_memory_stats function."""
        stats = get_memory_stats()
        self.assertIsInstance(stats, MemoryStats)
        self.assertGreater(stats.total, 0)
    
    def test_get_disk_usage(self):
        """Test get_disk_usage function."""
        usage = get_disk_usage("/")
        self.assertIsInstance(usage, dict)
    
    def test_get_network_stats(self):
        """Test get_network_stats function."""
        stats = get_network_stats()
        self.assertIsInstance(stats, list)
    
    def test_get_process_list(self):
        """Test get_process_list function."""
        processes = get_process_list()
        self.assertIsInstance(processes, list)
        self.assertGreater(len(processes), 0)
    
    def test_get_process_info(self):
        """Test get_process_info function."""
        proc = get_process_info(TEST_PID)
        # May return None if no permission
        if proc:
            self.assertIsInstance(proc, ProcessStats)
    
    def test_get_top_processes(self):
        """Test get_top_processes function."""
        processes = get_top_processes(5)
        self.assertIsInstance(processes, list)
    
    def test_get_system_info(self):
        """Test get_system_info function."""
        info = get_system_info()
        self.assertIsInstance(info, dict)
    
    def test_get_all_stats(self):
        """Test get_all_stats function."""
        stats = get_all_stats()
        self.assertIsInstance(stats, dict)
    
    def test_get_uptime(self):
        """Test get_uptime function."""
        uptime = get_uptime()
        self.assertIsInstance(uptime, float)
        self.assertGreaterEqual(uptime, 0.0)
    
    def test_get_hostname(self):
        """Test get_hostname function."""
        hostname = get_hostname()
        self.assertIsInstance(hostname, str)
        self.assertGreater(len(hostname), 0)


class TestModuleInfo(unittest.TestCase):
    """Test module metadata."""
    
    def test_version(self):
        """Test version string."""
        self.assertIsInstance(version, str)
        self.assertGreater(len(version), 0)
    
    def test_features(self):
        """Test features list."""
        self.assertIsInstance(features, list)
        self.assertGreater(len(features), 0)
        for feature in features:
            self.assertIsInstance(feature, str)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.monitor = SystemMonitor()
    
    def test_disk_usage_nonexistent_path(self):
        """Test disk usage for non-existent path."""
        usage = self.monitor.get_disk_usage("/nonexistent_path_xyz123")
        self.assertIsInstance(usage, dict)
        self.assertIn("error", usage)
    
    def test_get_process_info_invalid_pid(self):
        """Test getting process info for invalid PID."""
        proc = self.monitor.get_process_info(-1)
        self.assertIsNone(proc)
    
    def test_get_top_processes_zero(self):
        """Test getting zero top processes."""
        processes = self.monitor.get_top_processes(0)
        self.assertEqual(processes, [])
    
    def test_cpu_stats_percent_short_interval(self):
        """Test CPU stats with very short interval."""
        stats = self.monitor.get_cpu_stats_percent(interval=0.01)
        self.assertIsInstance(stats, CPUStats)


class TestIntegration(unittest.TestCase):
    """Integration tests for monitoring utilities."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.monitor = SystemMonitor()
    
    def test_full_system_snapshot(self):
        """Test taking a full system snapshot."""
        stats = self.monitor.get_all_stats()
        
        # Verify all major sections exist
        self.assertIn("system", stats)
        self.assertIn("cpu", stats)
        self.assertIn("memory", stats)
        self.assertIn("disk", stats)
        self.assertIn("network", stats)
        self.assertIn("timestamp", stats)
        
        # Verify timestamp is recent
        from datetime import datetime
        # Parse ISO format timestamp (compatible with older Python)
        ts_str = stats["timestamp"].replace("Z", "+00:00")
        if "+" in ts_str:
            ts_str = ts_str.split("+")[0]
        timestamp = datetime.strptime(ts_str[:19], "%Y-%m-%dT%H:%M:%S")
        now = datetime.now()
        self.assertLess((now - timestamp).total_seconds(), 60)
    
    def test_memory_consistency(self):
        """Test memory statistics consistency."""
        mem = self.monitor.get_memory_stats()
        
        # Used + Available should approximately equal Total
        # (may not be exact due to buffers/cache)
        self.assertLessEqual(mem.used, mem.total)
        self.assertLessEqual(mem.available, mem.total)
    
    def test_cpu_load_avg_values(self):
        """Test CPU load average values are reasonable."""
        stats = self.monitor.get_cpu_stats()
        
        # Load averages should be non-negative
        for load in stats.load_avg:
            self.assertGreaterEqual(load, 0.0)
    
    def test_network_interface_data(self):
        """Test network interface data consistency."""
        interfaces = self.monitor.get_network_stats()
        
        for iface in interfaces:
            # RX/TX bytes should be non-negative
            self.assertGreaterEqual(iface.rx_bytes, 0)
            self.assertGreaterEqual(iface.tx_bytes, 0)
            # Errors/dropped should be non-negative
            self.assertGreaterEqual(iface.rx_errors, 0)
            self.assertGreaterEqual(iface.tx_errors, 0)
    
    def test_process_list_uniqueness(self):
        """Test that process list has unique PIDs."""
        processes = self.monitor.get_process_list()
        pids = [p.pid for p in processes]
        
        # All PIDs should be unique
        self.assertEqual(len(pids), len(set(pids)))


# =============================================================================
# Test Runner
# =============================================================================

if __name__ == "__main__":
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestDataClasses))
    suite.addTests(loader.loadTestsFromTestCase(TestSystemMonitor))
    suite.addTests(loader.loadTestsFromTestCase(TestConvenienceFunctions))
    suite.addTests(loader.loadTestsFromTestCase(TestModuleInfo))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Run tests with verbosity
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 60)
    print("Test Summary:")
    print(f"  Tests run: {result.testsRun}")
    print(f"  Failures: {len(result.failures)}")
    print(f"  Errors: {len(result.errors)}")
    print(f"  Skipped: {len(result.skipped)}")
    print("=" * 60)
    
    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)
