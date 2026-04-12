#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AllToolkit - Socket Utilities Test Suite

Comprehensive tests for socket_utils module.
Run with: python socket_utils_test.py
"""

import unittest
import socket
import threading
import time
import sys
import os
from typing import Optional

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from socket_utils.mod import (
    # Socket creation
    create_socket, create_ssl_socket,
    # Config and data classes
    SocketConfig, ConnectionInfo, TransferStats,
    SocketProtocol, SocketFamily,
    # TCP utilities
    TCPClient, TCPServer,
    # UDP utilities
    UDPClient,
    # Connection pool
    ConnectionPool,
    # Helpers
    get_local_ip, get_hostname, resolve_hostname,
    is_port_open, scan_ports, wait_for_readable,
    set_socket_options,
    # Protocol helpers
    send_length_prefixed, recv_length_prefixed,
    send_json, recv_json,
    # Utilities
    socket_to_info, format_socket_address, parse_socket_address,
    version, features
)


# =============================================================================
# Test Constants
# =============================================================================

TEST_HOST = '127.0.0.1'
TEST_PORT = 18765
TEST_TIMEOUT = 5.0
BUFFER_SIZE = 1024


# =============================================================================
# Socket Creation Tests
# =============================================================================

class TestSocketCreation(unittest.TestCase):
    """Tests for socket creation functions."""
    
    def test_create_socket_default(self):
        """Test creating a default TCP socket."""
        sock = create_socket()
        self.assertIsInstance(sock, socket.socket)
        self.assertEqual(sock.type, socket.SOCK_STREAM)
        self.assertEqual(sock.family, socket.AF_INET)
        sock.close()
    
    def test_create_socket_udp(self):
        """Test creating a UDP socket."""
        sock = create_socket(protocol=SocketProtocol.UDP)
        self.assertEqual(sock.type, socket.SOCK_DGRAM)
        sock.close()
    
    def test_create_socket_ipv6(self):
        """Test creating an IPv6 socket."""
        sock = create_socket(family=SocketFamily.IPv6)
        self.assertEqual(sock.family, socket.AF_INET6)
        sock.close()
    
    def test_create_socket_timeout(self):
        """Test socket timeout setting."""
        sock = create_socket(timeout=10.0)
        self.assertEqual(sock.gettimeout(), 10.0)
        sock.close()
    
    def test_create_socket_options(self):
        """Test socket with custom options."""
        sock = create_socket(
            reuse_addr=True,
            keep_alive=True,
            tcp_nodelay=True,
            send_buffer_size=65536
        )
        
        # Verify options are set (may not be exactly as requested due to OS limits)
        self.assertTrue(sock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR))
        sock.close()


# =============================================================================
# TCP Client Tests
# =============================================================================

class TestTCPClient(unittest.TestCase):
    """Tests for TCPClient class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.server_thread: Optional[threading.Thread] = None
        self.server: Optional[TCPServer] = None
    
    def start_echo_server(self):
        """Start a simple echo server for testing."""
        def handle_client(client_sock, client_addr):
            try:
                while True:
                    data = client_sock.recv(BUFFER_SIZE)
                    if not data:
                        break
                    client_sock.sendall(data)
            except Exception:
                pass
            finally:
                client_sock.close()
        
        self.server = TCPServer(TEST_HOST, TEST_PORT, backlog=5)
        self.server.set_client_handler(handle_client)
        self.server.start()
        
        def run_server():
            while self.server and self.server.running:
                try:
                    client_sock, client_addr = self.server.accept_one(timeout=1.0)
                    threading.Thread(
                        target=handle_client,
                        args=(client_sock, client_addr),
                        daemon=True
                    ).start()
                except socket.timeout:
                    continue
                except Exception:
                    break
        
        self.server_thread = threading.Thread(target=run_server, daemon=True)
        self.server_thread.start()
        time.sleep(0.5)  # Give server time to start
    
    def tearDown(self):
        """Clean up test fixtures."""
        if self.server:
            self.server.stop()
        if self.server_thread:
            self.server_thread.join(timeout=2.0)
    
    def test_client_connect(self):
        """Test TCP client connection."""
        self.start_echo_server()
        
        client = TCPClient(SocketConfig(host=TEST_HOST, port=TEST_PORT, timeout=TEST_TIMEOUT))
        client.connect()
        
        self.assertTrue(client.connected)
        client.close()
    
    def test_client_send_recv(self):
        """Test TCP client send and receive."""
        self.start_echo_server()
        
        client = TCPClient(SocketConfig(host=TEST_HOST, port=TEST_PORT, timeout=TEST_TIMEOUT))
        client.connect()
        
        test_data = b"Hello, World!"
        client.send(test_data)
        response = client.recv(BUFFER_SIZE)
        
        self.assertEqual(response, test_data)
        client.close()
    
    def test_client_send_recv_string(self):
        """Test TCP client with string data."""
        self.start_echo_server()
        
        client = TCPClient(SocketConfig(host=TEST_HOST, port=TEST_PORT, timeout=TEST_TIMEOUT))
        client.connect()
        
        test_data = "Hello, 世界!"
        client.send(test_data)
        response = client.recv(BUFFER_SIZE).decode('utf-8')
        
        self.assertEqual(response, test_data)
        client.close()
    
    def test_client_context_manager(self):
        """Test TCP client as context manager."""
        self.start_echo_server()
        
        with TCPClient(SocketConfig(host=TEST_HOST, port=TEST_PORT, timeout=TEST_TIMEOUT)) as client:
            client.connect()
            self.assertTrue(client.connected)
        
        # Should be closed after context
        self.assertFalse(client.connected)
    
    def test_client_stats(self):
        """Test TCP client statistics."""
        self.start_echo_server()
        
        client = TCPClient(SocketConfig(host=TEST_HOST, port=TEST_PORT, timeout=TEST_TIMEOUT))
        client.connect()
        
        client.send(b"test")
        client.recv(BUFFER_SIZE)
        
        stats = client.get_stats()
        self.assertGreater(stats.bytes_sent, 0)
        self.assertGreater(stats.bytes_received, 0)
        self.assertGreater(stats.duration, 0)
        
        client.close()
    
    def test_client_connection_info(self):
        """Test TCP client connection info."""
        self.start_echo_server()
        
        client = TCPClient(SocketConfig(host=TEST_HOST, port=TEST_PORT, timeout=TEST_TIMEOUT))
        client.connect()
        
        info = client.connection_info
        self.assertTrue(info.connected)
        self.assertEqual(info.remote_addr[0], TEST_HOST)
        self.assertEqual(info.remote_addr[1], TEST_PORT)
        
        client.close()


# =============================================================================
# TCP Server Tests
# =============================================================================

class TestTCPServer(unittest.TestCase):
    """Tests for TCPServer class."""
    
    def test_server_start_stop(self):
        """Test server start and stop."""
        server = TCPServer(TEST_HOST, TEST_PORT + 1)
        server.start()
        
        self.assertTrue(server.running)
        
        server.stop()
        self.assertFalse(server.running)
    
    def test_server_context_manager(self):
        """Test server as context manager."""
        with TCPServer(TEST_HOST, TEST_PORT + 2) as server:
            self.assertTrue(server.running)
        
        self.assertFalse(server.running)
    
    def test_server_accept_client(self):
        """Test server accepting client connection."""
        server = TCPServer(TEST_HOST, TEST_PORT + 3, backlog=5)
        server.start()
        
        # Connect a client in a thread
        def connect_client():
            time.sleep(0.2)
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((TEST_HOST, TEST_PORT + 3))
            client.close()
        
        client_thread = threading.Thread(target=connect_client, daemon=True)
        client_thread.start()
        
        # Accept the connection
        client_sock, client_addr = server.accept_one(timeout=2.0)
        
        self.assertEqual(client_addr[0], TEST_HOST)
        self.assertEqual(server.client_count, 1)
        
        client_sock.close()
        server.stop()


# =============================================================================
# UDP Client Tests
# =============================================================================

class TestUDPClient(unittest.TestCase):
    """Tests for UDPClient class."""
    
    def test_udp_bind(self):
        """Test UDP client binding."""
        client = UDPClient()
        client.bind(TEST_HOST, TEST_PORT + 10)
        
        self.assertTrue(client._bound)
        client.close()
    
    def test_udp_send_recv(self):
        """Test UDP send and receive."""
        # Create two UDP clients
        sender = UDPClient(SocketConfig(timeout=TEST_TIMEOUT))
        sender.bind(TEST_HOST, TEST_PORT + 11)
        
        receiver = UDPClient(SocketConfig(timeout=TEST_TIMEOUT))
        receiver.bind(TEST_HOST, TEST_PORT + 12)
        
        # Send from sender to receiver
        test_data = b"UDP test message"
        sender.send_to(test_data, (TEST_HOST, TEST_PORT + 12))
        
        # Receive on receiver
        data, addr = receiver.recv_from(BUFFER_SIZE)
        
        self.assertEqual(data, test_data)
        self.assertEqual(addr[1], TEST_PORT + 11)
        
        sender.close()
        receiver.close()
    
    def test_udp_context_manager(self):
        """Test UDP client as context manager."""
        with UDPClient() as client:
            client.bind(TEST_HOST, TEST_PORT + 13)
            self.assertTrue(client._bound)
        
        self.assertFalse(client._bound)


# =============================================================================
# Connection Pool Tests
# =============================================================================

class TestConnectionPool(unittest.TestCase):
    """Tests for ConnectionPool class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.server_thread: Optional[threading.Thread] = None
        self.server: Optional[TCPServer] = None
    
    def start_simple_server(self):
        """Start a simple server that accepts and holds connections."""
        def handle_client(client_sock, client_addr):
            try:
                while True:
                    data = client_sock.recv(1)
                    if not data:
                        break
            except Exception:
                pass
            finally:
                client_sock.close()
        
        self.server = TCPServer(TEST_HOST, TEST_PORT + 20, backlog=10)
        self.server.set_client_handler(handle_client)
        self.server.start()
        
        def run_server():
            while self.server and self.server.running:
                try:
                    client_sock, client_addr = self.server.accept_one(timeout=1.0)
                    threading.Thread(
                        target=handle_client,
                        args=(client_sock, client_addr),
                        daemon=True
                    ).start()
                except socket.timeout:
                    continue
                except Exception:
                    break
        
        self.server_thread = threading.Thread(target=run_server, daemon=True)
        self.server_thread.start()
        time.sleep(0.5)
    
    def tearDown(self):
        """Clean up test fixtures."""
        if self.server:
            self.server.stop()
        if self.server_thread:
            self.server_thread.join(timeout=2.0)
    
    def test_pool_acquire_release(self):
        """Test pool acquire and release."""
        self.start_simple_server()
        
        pool = ConnectionPool(TEST_HOST, TEST_PORT + 20, max_connections=3)
        
        sock = pool.acquire(timeout=TEST_TIMEOUT)
        self.assertIsInstance(sock, socket.socket)
        self.assertEqual(pool.in_use, 1)
        
        pool.release(sock)
        self.assertEqual(pool.in_use, 0)
        self.assertEqual(pool.available, 1)
        
        pool.close_all()
    
    def test_pool_context_manager(self):
        """Test pool connection context manager."""
        self.start_simple_server()
        
        with ConnectionPool(TEST_HOST, TEST_PORT + 21, max_connections=2) as pool:
            with pool.connection() as sock:
                self.assertIsInstance(sock, socket.socket)
                self.assertEqual(pool.in_use, 1)
            
            self.assertEqual(pool.in_use, 0)
    
    def test_pool_max_connections(self):
        """Test pool respects max connections."""
        self.start_simple_server()
        
        pool = ConnectionPool(TEST_HOST, TEST_PORT + 22, max_connections=2)
        
        # Acquire max connections
        socks = []
        for _ in range(2):
            sock = pool.acquire(timeout=TEST_TIMEOUT)
            socks.append(sock)
        
        self.assertEqual(pool.in_use, 2)
        self.assertEqual(pool.available, 0)
        
        # Clean up
        for sock in socks:
            pool.release(sock)
        pool.close_all()


# =============================================================================
# Helper Functions Tests
# =============================================================================

class TestHelperFunctions(unittest.TestCase):
    """Tests for helper functions."""
    
    def test_get_local_ip(self):
        """Test getting local IP."""
        ip = get_local_ip()
        self.assertIsInstance(ip, str)
        # Should be a valid IP format
        parts = ip.split('.')
        self.assertEqual(len(parts), 4)
        for part in parts:
            self.assertTrue(part.isdigit())
    
    def test_get_hostname(self):
        """Test getting hostname."""
        hostname = get_hostname()
        self.assertIsInstance(hostname, str)
        self.assertGreater(len(hostname), 0)
    
    def test_resolve_hostname(self):
        """Test hostname resolution."""
        # Test localhost
        ips = resolve_hostname('localhost')
        self.assertIsInstance(ips, list)
        # Should have at least one IP (usually 127.0.0.1)
        self.assertGreater(len(ips), 0)
    
    def test_is_port_open_closed(self):
        """Test port open detection."""
        # Test a definitely closed port
        result = is_port_open(TEST_HOST, 1, timeout=0.5)
        self.assertFalse(result)
    
    def test_scan_ports(self):
        """Test port scanning."""
        results = scan_ports(TEST_HOST, [1, 2, 3], timeout=0.2)
        self.assertIsInstance(results, dict)
        self.assertEqual(len(results), 3)
        for port, is_open in results.items():
            self.assertIsInstance(is_open, bool)
    
    def test_format_socket_address(self):
        """Test address formatting."""
        addr = ('192.168.1.1', 8080)
        formatted = format_socket_address(addr)
        self.assertEqual(formatted, '192.168.1.1:8080')
    
    def test_parse_socket_address(self):
        """Test address parsing."""
        addr_str = '192.168.1.1:8080'
        parsed = parse_socket_address(addr_str)
        self.assertEqual(parsed, ('192.168.1.1', 8080))
    
    def test_parse_socket_address_invalid(self):
        """Test invalid address parsing."""
        with self.assertRaises(ValueError):
            parse_socket_address('invalid')
        
        with self.assertRaises(ValueError):
            parse_socket_address('192.168.1.1:notaport')


# =============================================================================
# Protocol Helper Tests
# =============================================================================

class TestProtocolHelpers(unittest.TestCase):
    """Tests for protocol helper functions."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.server_thread: Optional[threading.Thread] = None
        self.server: Optional[TCPServer] = None
    
    def start_echo_server(self):
        """Start echo server for protocol tests."""
        def handle_client(client_sock, client_addr):
            try:
                while True:
                    data = recv_length_prefixed(client_sock)
                    if not data:
                        break
                    send_length_prefixed(client_sock, data)
            except Exception:
                pass
            finally:
                client_sock.close()
        
        self.server = TCPServer(TEST_HOST, TEST_PORT + 30, backlog=5)
        self.server.set_client_handler(handle_client)
        self.server.start()
        
        def run_server():
            while self.server and self.server.running:
                try:
                    client_sock, client_addr = self.server.accept_one(timeout=1.0)
                    threading.Thread(
                        target=handle_client,
                        args=(client_sock, client_addr),
                        daemon=True
                    ).start()
                except socket.timeout:
                    continue
                except Exception:
                    break
        
        self.server_thread = threading.Thread(target=run_server, daemon=True)
        self.server_thread.start()
        time.sleep(0.5)
    
    def tearDown(self):
        """Clean up test fixtures."""
        if self.server:
            self.server.stop()
        if self.server_thread:
            self.server_thread.join(timeout=2.0)
    
    def test_send_recv_length_prefixed(self):
        """Test length-prefixed send/receive."""
        self.start_echo_server()
        
        sock = create_socket(timeout=TEST_TIMEOUT)
        sock.connect((TEST_HOST, TEST_PORT + 30))
        
        test_data = b"Hello, length-prefixed world!"
        send_length_prefixed(sock, test_data)
        response = recv_length_prefixed(sock)
        
        self.assertEqual(response, test_data)
        sock.close()
    
    def test_send_recv_json(self):
        """Test JSON over sockets."""
        self.start_echo_server()
        
        # Create a JSON echo handler
        def json_handler(client_sock, client_addr):
            try:
                while True:
                    data = recv_json(client_sock)
                    send_json(client_sock, data)
            except Exception:
                pass
            finally:
                client_sock.close()
        
        # Stop the old server and start JSON server
        self.server.stop()
        time.sleep(0.5)
        
        self.server = TCPServer(TEST_HOST, TEST_PORT + 31, backlog=5)
        self.server.set_client_handler(json_handler)
        self.server.start()
        
        def run_server():
            while self.server and self.server.running:
                try:
                    client_sock, client_addr = self.server.accept_one(timeout=1.0)
                    threading.Thread(
                        target=json_handler,
                        args=(client_sock, client_addr),
                        daemon=True
                    ).start()
                except socket.timeout:
                    continue
                except Exception:
                    break
        
        self.server_thread = threading.Thread(target=run_server, daemon=True)
        self.server_thread.start()
        time.sleep(0.5)
        
        sock = create_socket(timeout=TEST_TIMEOUT)
        sock.connect((TEST_HOST, TEST_PORT + 31))
        
        test_data = {"message": "Hello", "number": 42, "list": [1, 2, 3]}
        send_json(sock, test_data)
        response = recv_json(sock)
        
        self.assertEqual(response, test_data)
        sock.close()


# =============================================================================
# Data Class Tests
# =============================================================================

class TestDataClasses(unittest.TestCase):
    """Tests for data classes."""
    
    def test_socket_config_default(self):
        """Test SocketConfig defaults."""
        config = SocketConfig()
        self.assertEqual(config.host, 'localhost')
        self.assertEqual(config.port, 8080)
        self.assertEqual(config.timeout, 30.0)
        self.assertTrue(config.reuse_addr)
        self.assertTrue(config.keep_alive)
        self.assertTrue(config.tcp_nodelay)
    
    def test_socket_config_custom(self):
        """Test SocketConfig with custom values."""
        config = SocketConfig(
            host='example.com',
            port=443,
            timeout=60.0,
            ssl_enabled=True
        )
        self.assertEqual(config.host, 'example.com')
        self.assertEqual(config.port, 443)
        self.assertEqual(config.timeout, 60.0)
        self.assertTrue(config.ssl_enabled)
    
    def test_connection_info(self):
        """Test ConnectionInfo."""
        info = ConnectionInfo(
            local_addr=('127.0.0.1', 8080),
            remote_addr=('192.168.1.1', 443),
            connected=True
        )
        self.assertEqual(info.local_addr, ('127.0.0.1', 8080))
        self.assertTrue(info.connected)
    
    def test_transfer_stats(self):
        """Test TransferStats."""
        stats = TransferStats(
            bytes_sent=1000,
            bytes_received=2000,
            packets_sent=10,
            packets_received=20
        )
        
        self.assertEqual(stats.bytes_sent, 1000)
        self.assertEqual(stats.bytes_received, 2000)
        self.assertGreater(stats.duration, 0)
        self.assertGreater(stats.throughput, 0)


# =============================================================================
# Module Info Tests
# =============================================================================

class TestModuleInfo(unittest.TestCase):
    """Tests for module info functions."""
    
    def test_version(self):
        """Test version function."""
        v = version()
        self.assertIsInstance(v, str)
        # Should be semver-like
        parts = v.split('.')
        self.assertGreaterEqual(len(parts), 2)
    
    def test_features(self):
        """Test features function."""
        feats = features()
        self.assertIsInstance(feats, list)
        self.assertGreater(len(feats), 0)
        for feat in feats:
            self.assertIsInstance(feat, str)
            self.assertGreater(len(feat), 0)


# =============================================================================
# Integration Tests
# =============================================================================

class TestIntegration(unittest.TestCase):
    """Integration tests for socket utilities."""
    
    def test_full_client_server_roundtrip(self):
        """Test complete client-server communication."""
        received_messages = []
        server_ready = threading.Event()
        
        def handler(client_sock, client_addr):
            try:
                while True:
                    data = client_sock.recv(BUFFER_SIZE)
                    if not data:
                        break
                    received_messages.append(data.decode('utf-8'))
                    client_sock.sendall(b"ACK: " + data)
            except Exception:
                pass
            finally:
                client_sock.close()
        
        server = TCPServer(TEST_HOST, TEST_PORT + 40, backlog=5)
        server.set_client_handler(handler)
        server.start()
        
        def run_server():
            server_ready.set()
            while server.running:
                try:
                    client_sock, client_addr = server.accept_one(timeout=1.0)
                    threading.Thread(
                        target=handler,
                        args=(client_sock, client_addr),
                        daemon=True
                    ).start()
                except socket.timeout:
                    continue
                except Exception:
                    break
        
        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()
        server_ready.wait()
        time.sleep(0.5)
        
        try:
            # Connect and send messages
            client = TCPClient(SocketConfig(host=TEST_HOST, port=TEST_PORT + 40, timeout=TEST_TIMEOUT))
            client.connect()
            
            messages = ["Hello", "World", "Test", "123"]
            for msg in messages:
                client.send(msg)
                response = client.recv(BUFFER_SIZE).decode('utf-8')
                self.assertTrue(response.startswith("ACK: "))
            
            client.close()
            time.sleep(0.5)
            
            # Verify all messages received
            self.assertEqual(len(received_messages), len(messages))
            for i, msg in enumerate(messages):
                self.assertEqual(received_messages[i], msg)
        
        finally:
            server.stop()
            server_thread.join(timeout=2.0)


# =============================================================================
# Run Tests
# =============================================================================

if __name__ == '__main__':
    print("=" * 70)
    print("AllToolkit Socket Utils - Test Suite")
    print("=" * 70)
    print()
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestSocketCreation,
        TestTCPClient,
        TestTCPServer,
        TestUDPClient,
        TestConnectionPool,
        TestHelperFunctions,
        TestProtocolHelpers,
        TestDataClasses,
        TestModuleInfo,
        TestIntegration,
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print()
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    print("=" * 70)
    
    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)
