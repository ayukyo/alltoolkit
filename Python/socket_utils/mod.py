#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AllToolkit - Socket Utilities Module

Comprehensive socket utilities for Python with zero external dependencies.
Provides TCP/UDP client/server helpers, connection pooling, timeout handling,
SSL/TLS support, and more.

Author: AllToolkit
License: MIT
"""

import socket
import ssl
import select
import struct
import threading
import queue
import time
import errno
from typing import Optional, Tuple, List, Dict, Any, Union, Callable
from contextlib import contextmanager
from dataclasses import dataclass, field
from enum import Enum
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# =============================================================================
# Type Aliases
# =============================================================================

SocketAddress = Tuple[str, int]
BytesLike = Union[bytes, bytearray, memoryview]


# =============================================================================
# Constants
# =============================================================================

DEFAULT_BUFFER_SIZE = 4096
DEFAULT_TIMEOUT = 30.0
MAX_CONNECTIONS = 5
DEFAULT_BACKLOG = 128


# =============================================================================
# Enums
# =============================================================================

class SocketProtocol(Enum):
    """Socket protocol types."""
    TCP = socket.SOCK_STREAM
    UDP = socket.SOCK_DGRAM
    RAW = socket.SOCK_RAW


class SocketFamily(Enum):
    """Socket address families."""
    IPv4 = socket.AF_INET
    IPv6 = socket.AF_INET6


# =============================================================================
# Data Classes
# =============================================================================

@dataclass
class SocketConfig:
    """Configuration for socket connections."""
    host: str = 'localhost'
    port: int = 8080
    timeout: float = DEFAULT_TIMEOUT
    buffer_size: int = DEFAULT_BUFFER_SIZE
    reuse_addr: bool = True
    keep_alive: bool = True
    tcp_nodelay: bool = True
    ssl_enabled: bool = False
    ssl_certfile: Optional[str] = None
    ssl_keyfile: Optional[str] = None
    ssl_ca_certs: Optional[str] = None
    ssl_check_hostname: bool = True


@dataclass
class ConnectionInfo:
    """Information about a socket connection."""
    local_addr: Optional[SocketAddress] = None
    remote_addr: Optional[SocketAddress] = None
    family: Optional[int] = None
    type: Optional[int] = None
    proto: Optional[int] = None
    connected: bool = False
    ssl: bool = False


@dataclass
class TransferStats:
    """Statistics for data transfer operations."""
    bytes_sent: int = 0
    bytes_received: int = 0
    packets_sent: int = 0
    packets_received: int = 0
    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None
    
    @property
    def duration(self) -> float:
        """Get transfer duration in seconds."""
        end = self.end_time or time.time()
        return end - self.start_time
    
    @property
    def throughput(self) -> float:
        """Get throughput in bytes/second."""
        if self.duration > 0:
            return (self.bytes_sent + self.bytes_received) / self.duration
        return 0.0


# =============================================================================
# Socket Creation Helpers
# =============================================================================

def create_socket(
    family: SocketFamily = SocketFamily.IPv4,
    protocol: SocketProtocol = SocketProtocol.TCP,
    timeout: float = DEFAULT_TIMEOUT,
    **options: Any
) -> socket.socket:
    """
    Create a configured socket with common options.
    
    Args:
        family: Address family (IPv4 or IPv6)
        protocol: Socket protocol (TCP, UDP, or RAW)
        timeout: Socket timeout in seconds
        **options: Additional socket options
        
    Returns:
        Configured socket object
        
    Example:
        >>> sock = create_socket(timeout=10.0)
        >>> sock.connect(('localhost', 8080))
    """
    sock = socket.socket(family.value, protocol.value)
    sock.settimeout(timeout)
    
    # Apply common options
    if options.get('reuse_addr', True) and protocol == SocketProtocol.TCP:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    if options.get('keep_alive', True) and protocol == SocketProtocol.TCP:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    
    if options.get('tcp_nodelay', True) and protocol == SocketProtocol.TCP:
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    
    # Set buffer sizes
    if 'send_buffer_size' in options:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, options['send_buffer_size'])
    if 'recv_buffer_size' in options:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, options['recv_buffer_size'])
    
    return sock


def create_ssl_socket(
    sock: socket.socket,
    server_hostname: Optional[str] = None,
    certfile: Optional[str] = None,
    keyfile: Optional[str] = None,
    ca_certs: Optional[str] = None,
    check_hostname: bool = True,
    ssl_version: int = ssl.PROTOCOL_TLS_CLIENT
) -> ssl.SSLSocket:
    """
    Wrap a socket with SSL/TLS.
    
    Args:
        sock: Base socket to wrap
        server_hostname: Server hostname for SNI and verification
        certfile: Client certificate file (for client auth)
        keyfile: Client key file (for client auth)
        ca_certs: CA certificates file for server verification
        check_hostname: Whether to verify server hostname
        ssl_version: SSL/TLS version to use
        
    Returns:
        SSL-wrapped socket
        
    Example:
        >>> sock = create_socket()
        >>> sock.connect(('example.com', 443))
        >>> ssl_sock = create_ssl_socket(sock, server_hostname='example.com')
    """
    context = ssl.SSLContext(ssl_version)
    
    if certfile:
        context.load_cert_chain(certfile, keyfile)
    
    if ca_certs:
        context.load_verify_locations(ca_certs)
        context.check_hostname = check_hostname
        context.verify_mode = ssl.CERT_REQUIRED
    else:
        context.check_hostname = check_hostname
        context.verify_mode = ssl.CERT_REQUIRED if check_hostname else ssl.CERT_NONE
    
    return context.wrap_socket(sock, server_hostname=server_hostname)


# =============================================================================
# TCP Client Utilities
# =============================================================================

class TCPClient:
    """TCP client with connection management."""
    
    def __init__(self, config: Optional[SocketConfig] = None):
        """
        Initialize TCP client.
        
        Args:
            config: Socket configuration
        """
        self.config = config or SocketConfig()
        self.sock: Optional[socket.socket] = None
        self.stats = TransferStats()
        self._connected = False
    
    def connect(self, host: Optional[str] = None, port: Optional[int] = None) -> 'TCPClient':
        """
        Establish TCP connection.
        
        Args:
            host: Override host
            port: Override port
            
        Returns:
            Self for chaining
            
        Raises:
            ConnectionError: If connection fails
        """
        host = host or self.config.host
        port = port or self.config.port
        
        try:
            self.sock = create_socket(
                timeout=self.config.timeout,
                reuse_addr=self.config.reuse_addr,
                keep_alive=self.config.keep_alive,
                tcp_nodelay=self.config.tcp_nodelay
            )
            
            self.sock.connect((host, port))
            
            if self.config.ssl_enabled:
                self.sock = create_ssl_socket(
                    self.sock,
                    server_hostname=host,
                    certfile=self.config.ssl_certfile,
                    keyfile=self.config.ssl_keyfile,
                    ca_certs=self.config.ssl_ca_certs,
                    check_hostname=self.config.ssl_check_hostname
                )
            
            self._connected = True
            logger.info(f"Connected to {host}:{port}")
            
        except Exception as e:
            self.close()
            raise ConnectionError(f"Failed to connect to {host}:{port}: {e}")
        
        return self
    
    def send(self, data: BytesLike) -> int:
        """
        Send data over the connection.
        
        Args:
            data: Data to send
            
        Returns:
            Number of bytes sent
            
        Raises:
            ConnectionError: If not connected
        """
        if not self._connected or not self.sock:
            raise ConnectionError("Not connected")
        
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        total_sent = 0
        while total_sent < len(data):
            sent = self.sock.send(data[total_sent:])
            if sent == 0:
                raise ConnectionError("Connection broken")
            total_sent += sent
        
        self.stats.bytes_sent += total_sent
        self.stats.packets_sent += 1
        return total_sent
    
    def recv(self, bufsize: Optional[int] = None) -> bytes:
        """
        Receive data from the connection.
        
        Args:
            bufsize: Maximum bytes to receive (uses config default if None)
            
        Returns:
            Received data
            
        Raises:
            ConnectionError: If not connected
        """
        if not self._connected or not self.sock:
            raise ConnectionError("Not connected")
        
        bufsize = bufsize or self.config.buffer_size
        data = self.sock.recv(bufsize)
        
        if data:
            self.stats.bytes_received += len(data)
            self.stats.packets_received += 1
        
        return data
    
    def recv_all(self, expected_size: int, timeout: Optional[float] = None) -> bytes:
        """
        Receive exactly the specified number of bytes.
        
        Args:
            expected_size: Number of bytes to receive
            timeout: Optional timeout override
            
        Returns:
            Received data
            
        Raises:
            ConnectionError: If connection breaks before receiving all data
        """
        if not self._connected or not self.sock:
            raise ConnectionError("Not connected")
        
        original_timeout = self.sock.gettimeout()
        if timeout is not None:
            self.sock.settimeout(timeout)
        
        try:
            data = bytearray()
            while len(data) < expected_size:
                chunk = self.sock.recv(expected_size - len(data))
                if not chunk:
                    raise ConnectionError("Connection broken")
                data.extend(chunk)
            
            self.stats.bytes_received += len(data)
            self.stats.packets_received += 1
            return bytes(data)
        finally:
            self.sock.settimeout(original_timeout)
    
    def send_recv(self, data: BytesLike, bufsize: Optional[int] = None) -> bytes:
        """
        Send data and receive response.
        
        Args:
            data: Data to send
            bufsize: Response buffer size
            
        Returns:
            Response data
        """
        self.send(data)
        return self.recv(bufsize)
    
    @property
    def connected(self) -> bool:
        """Check if connected."""
        return self._connected
    
    @property
    def connection_info(self) -> ConnectionInfo:
        """Get connection information."""
        if not self.sock:
            return ConnectionInfo()
        
        try:
            return ConnectionInfo(
                local_addr=self.sock.getsockname(),
                remote_addr=self.sock.getpeername() if self._connected else None,
                family=self.sock.family,
                type=self.sock.type,
                proto=self.sock.proto,
                connected=self._connected,
                ssl=isinstance(self.sock, ssl.SSLSocket)
            )
        except Exception:
            return ConnectionInfo()
    
    def close(self) -> None:
        """Close the connection."""
        if self.sock:
            try:
                self.sock.close()
            except Exception:
                pass
            self.sock = None
        self._connected = False
    
    def get_stats(self) -> TransferStats:
        """Get transfer statistics."""
        self.stats.end_time = time.time()
        return self.stats
    
    def __enter__(self) -> 'TCPClient':
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()


# =============================================================================
# TCP Server Utilities
# =============================================================================

class TCPServer:
    """TCP server with connection handling."""
    
    def __init__(
        self,
        host: str = '0.0.0.0',
        port: int = 8080,
        backlog: int = DEFAULT_BACKLOG,
        config: Optional[SocketConfig] = None
    ):
        """
        Initialize TCP server.
        
        Args:
            host: Host to bind to
            port: Port to bind to
            backlog: Maximum pending connections
            config: Socket configuration
        """
        self.host = host
        self.port = port
        self.backlog = backlog
        self.config = config or SocketConfig(host=host, port=port)
        self.sock: Optional[socket.socket] = None
        self._running = False
        self._clients: List[socket.socket] = []
        self._client_handler: Optional[Callable[[socket.socket, SocketAddress], None]] = None
    
    def start(self) -> 'TCPServer':
        """
        Start the server.
        
        Returns:
            Self for chaining
        """
        try:
            self.sock = create_socket(
                timeout=self.config.timeout,
                reuse_addr=self.config.reuse_addr
            )
            self.sock.bind((self.host, self.port))
            self.sock.listen(self.backlog)
            self._running = True
            logger.info(f"Server listening on {self.host}:{self.port}")
        except Exception as e:
            self.stop()
            raise RuntimeError(f"Failed to start server: {e}")
        
        return self
    
    def set_client_handler(
        self,
        handler: Callable[[socket.socket, SocketAddress], None]
    ) -> 'TCPServer':
        """
        Set handler for incoming client connections.
        
        Args:
            handler: Function to handle client connections
            
        Returns:
            Self for chaining
        """
        self._client_handler = handler
        return self
    
    def accept_one(self, timeout: Optional[float] = None) -> Tuple[socket.socket, SocketAddress]:
        """
        Accept a single connection.
        
        Args:
            timeout: Accept timeout
            
        Returns:
            Tuple of (client_socket, client_address)
        """
        if not self.sock:
            raise RuntimeError("Server not started")
        
        original_timeout = self.sock.gettimeout()
        if timeout is not None:
            self.sock.settimeout(timeout)
        
        try:
            client_sock, client_addr = self.sock.accept()
            self._clients.append(client_sock)
            logger.info(f"Client connected: {client_addr}")
            return client_sock, client_addr
        finally:
            self.sock.settimeout(original_timeout)
    
    def handle_client(
        self,
        client_sock: socket.socket,
        client_addr: SocketAddress,
        handler: Optional[Callable[[socket.socket, SocketAddress], None]] = None
    ) -> None:
        """
        Handle a client connection.
        
        Args:
            client_sock: Client socket
            client_addr: Client address
            handler: Optional handler function
        """
        handler = handler or self._client_handler
        
        if handler:
            try:
                handler(client_sock, client_addr)
            except Exception as e:
                logger.error(f"Error handling client {client_addr}: {e}")
            finally:
                self.remove_client(client_sock)
    
    def remove_client(self, client_sock: socket.socket) -> None:
        """Remove a client from the client list."""
        if client_sock in self._clients:
            self._clients.remove(client_sock)
        try:
            client_sock.close()
        except Exception:
            pass
    
    @property
    def running(self) -> bool:
        """Check if server is running."""
        return self._running
    
    @property
    def client_count(self) -> int:
        """Get number of connected clients."""
        return len(self._clients)
    
    def stop(self) -> None:
        """Stop the server."""
        self._running = False
        
        # Close all clients
        for client in self._clients[:]:
            try:
                client.close()
            except Exception:
                pass
        self._clients.clear()
        
        # Close server socket
        if self.sock:
            try:
                self.sock.close()
            except Exception:
                pass
            self.sock = None
        
        logger.info("Server stopped")
    
    def __enter__(self) -> 'TCPServer':
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.stop()


# =============================================================================
# UDP Utilities
# =============================================================================

class UDPClient:
    """UDP client for datagram communication."""
    
    def __init__(self, config: Optional[SocketConfig] = None):
        """
        Initialize UDP client.
        
        Args:
            config: Socket configuration
        """
        self.config = config or SocketConfig()
        self.sock: Optional[socket.socket] = None
        self.stats = TransferStats()
        self._bound = False
    
    def bind(self, host: Optional[str] = None, port: Optional[int] = None) -> 'UDPClient':
        """
        Bind to a local address.
        
        Args:
            host: Host to bind to (None for all interfaces)
            port: Port to bind to
            
        Returns:
            Self for chaining
        """
        host = host or '0.0.0.0'
        port = port or 0  # 0 means auto-assign
        
        self.sock = create_socket(
            protocol=SocketProtocol.UDP,
            timeout=self.config.timeout,
            reuse_addr=self.config.reuse_addr
        )
        self.sock.bind((host, port))
        self._bound = True
        logger.info(f"UDP client bound to {host}:{port}")
        return self
    
    def send_to(self, data: BytesLike, addr: SocketAddress) -> int:
        """
        Send data to a specific address.
        
        Args:
            data: Data to send
            addr: Destination address (host, port)
            
        Returns:
            Number of bytes sent
        """
        if not self.sock:
            self.sock = create_socket(protocol=SocketProtocol.UDP, timeout=self.config.timeout)
        
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        sent = self.sock.sendto(data, addr)
        self.stats.bytes_sent += sent
        self.stats.packets_sent += 1
        return sent
    
    def recv_from(self, bufsize: Optional[int] = None) -> Tuple[bytes, SocketAddress]:
        """
        Receive data from any sender.
        
        Args:
            bufsize: Maximum bytes to receive
            
        Returns:
            Tuple of (data, sender_address)
        """
        if not self.sock:
            raise RuntimeError("UDP client not bound")
        
        bufsize = bufsize or self.config.buffer_size
        data, addr = self.sock.recvfrom(bufsize)
        self.stats.bytes_received += len(data)
        self.stats.packets_received += 1
        return data, addr
    
    def send_recv(
        self,
        data: BytesLike,
        addr: SocketAddress,
        bufsize: Optional[int] = None
    ) -> Tuple[bytes, SocketAddress]:
        """
        Send data and receive response.
        
        Args:
            data: Data to send
            addr: Destination address
            bufsize: Response buffer size
            
        Returns:
            Tuple of (response_data, responder_address)
        """
        self.send_to(data, addr)
        return self.recv_from(bufsize)
    
    def broadcast(
        self,
        data: BytesLike,
        port: int,
        broadcast_addr: str = '255.255.255.255'
    ) -> int:
        """
        Send broadcast message.
        
        Args:
            data: Data to broadcast
            port: Destination port
            broadcast_addr: Broadcast address
            
        Returns:
            Number of bytes sent
        """
        if not self.sock:
            self.sock = create_socket(protocol=SocketProtocol.UDP, timeout=self.config.timeout)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        sent = self.sock.sendto(data, (broadcast_addr, port))
        self.stats.bytes_sent += sent
        self.stats.packets_sent += 1
        return sent
    
    def close(self) -> None:
        """Close the UDP socket."""
        if self.sock:
            try:
                self.sock.close()
            except Exception:
                pass
            self.sock = None
        self._bound = False
    
    def get_stats(self) -> TransferStats:
        """Get transfer statistics."""
        self.stats.end_time = time.time()
        return self.stats
    
    def __enter__(self) -> 'UDPClient':
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()


# =============================================================================
# Connection Pool
# =============================================================================

class ConnectionPool:
    """Thread-safe connection pool for TCP connections."""
    
    def __init__(
        self,
        host: str,
        port: int,
        max_connections: int = 10,
        config: Optional[SocketConfig] = None
    ):
        """
        Initialize connection pool.
        
        Args:
            host: Server host
            port: Server port
            max_connections: Maximum pooled connections
            config: Socket configuration
        """
        self.host = host
        self.port = port
        self.max_connections = max_connections
        self.config = config or SocketConfig(host=host, port=port)
        self._pool: queue.Queue = queue.Queue(maxsize=max_connections)
        self._lock = threading.Lock()
        self._created = 0
    
    def _create_connection(self) -> socket.socket:
        """Create a new connection."""
        sock = create_socket(
            timeout=self.config.timeout,
            reuse_addr=self.config.reuse_addr,
            keep_alive=self.config.keep_alive,
            tcp_nodelay=self.config.tcp_nodelay
        )
        sock.connect((self.host, self.port))
        return sock
    
    def acquire(self, timeout: Optional[float] = None) -> socket.socket:
        """
        Acquire a connection from the pool.
        
        Args:
            timeout: Acquire timeout (None for block indefinitely)
            
        Returns:
            Socket connection
            
        Raises:
            TimeoutError: If no connection available within timeout
        """
        try:
            sock = self._pool.get(timeout=timeout)
            # Verify connection is still valid
            if not self._is_valid(sock):
                sock.close()
                with self._lock:
                    self._created -= 1
                return self.acquire(timeout)
            return sock
        except queue.Empty:
            with self._lock:
                if self._created < self.max_connections:
                    self._created += 1
                    return self._create_connection()
            raise TimeoutError("No connections available")
    
    def release(self, sock: socket.socket) -> None:
        """
        Release a connection back to the pool.
        
        Args:
            sock: Socket to release
        """
        if self._is_valid(sock):
            try:
                self._pool.put_nowait(sock)
            except queue.Full:
                sock.close()
                with self._lock:
                    self._created -= 1
        else:
            sock.close()
            with self._lock:
                self._created -= 1
    
    def _is_valid(self, sock: socket.socket) -> bool:
        """Check if a socket is still valid."""
        try:
            # Check if socket is closed
            if sock.fileno() == -1:
                return False
            
            # Check for pending errors
            error = sock.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)
            return error == 0
        except Exception:
            return False
    
    @property
    def size(self) -> int:
        """Get current pool size."""
        return self._pool.qsize()
    
    @property
    def available(self) -> int:
        """Get number of available connections."""
        return self.size
    
    @property
    def in_use(self) -> int:
        """Get number of connections in use."""
        with self._lock:
            return self._created - self.size
    
    def close_all(self) -> None:
        """Close all connections in the pool."""
        while not self._pool.empty():
            try:
                sock = self._pool.get_nowait()
                sock.close()
            except queue.Empty:
                break
        with self._lock:
            self._created = 0
    
    @contextmanager
    def connection(self, timeout: Optional[float] = None):
        """
        Context manager for acquiring/releasing connections.
        
        Args:
            timeout: Acquire timeout
            
        Yields:
            Socket connection
            
        Example:
            >>> with pool.connection() as sock:
            ...     sock.send(b"data")
        """
        sock = self.acquire(timeout)
        try:
            yield sock
        finally:
            self.release(sock)
    
    def __enter__(self) -> 'ConnectionPool':
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close_all()


# =============================================================================
# Socket Helpers
# =============================================================================

def get_local_ip() -> str:
    """
    Get the local IP address.
    
    Returns:
        Local IP address as string
        
    Example:
        >>> get_local_ip()
        '192.168.1.100'
    """
    try:
        # Create a temporary socket to determine local IP
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(('8.8.8.8', 80))
        ip = sock.getsockname()[0]
        sock.close()
        return ip
    except Exception:
        return '127.0.0.1'


def get_hostname() -> str:
    """
    Get the system hostname.
    
    Returns:
        Hostname as string
    """
    return socket.gethostname()


def resolve_hostname(hostname: str) -> List[str]:
    """
    Resolve a hostname to IP addresses.
    
    Args:
        hostname: Hostname to resolve
        
    Returns:
        List of IP addresses
        
    Example:
        >>> resolve_hostname('google.com')
        ['142.250.80.46', ...]
    """
    try:
        result = socket.gethostbyname_ex(hostname)
        return result[2]
    except socket.gaierror:
        return []


def is_port_open(host: str, port: int, timeout: float = 1.0) -> bool:
    """
    Check if a port is open on a host.
    
    Args:
        host: Host to check
        port: Port number
        timeout: Connection timeout
        
    Returns:
        True if port is open
        
    Example:
        >>> is_port_open('localhost', 8080)
        True
    """
    try:
        sock = create_socket(timeout=timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except Exception:
        return False


def scan_ports(
    host: str,
    ports: List[int],
    timeout: float = 0.5
) -> Dict[int, bool]:
    """
    Scan multiple ports on a host.
    
    Args:
        host: Host to scan
        ports: List of ports to scan
        timeout: Timeout per port
        
    Returns:
        Dict mapping port -> open status
        
    Example:
        >>> scan_ports('localhost', [22, 80, 443])
        {22: True, 80: False, 443: True}
    """
    results = {}
    for port in ports:
        results[port] = is_port_open(host, port, timeout)
    return results


def wait_for_readable(
    sockets: List[socket.socket],
    timeout: float = 0.0
) -> List[socket.socket]:
    """
    Wait for sockets to become readable.
    
    Args:
        sockets: List of sockets to monitor
        timeout: Timeout in seconds (0 for non-blocking)
        
    Returns:
        List of readable sockets
        
    Example:
        >>> readable = wait_for_readable([sock1, sock2], timeout=5.0)
    """
    try:
        readable, _, _ = select.select(sockets, [], [], timeout)
        return readable
    except Exception:
        return []


def set_socket_options(
    sock: socket.socket,
    **options: Any
) -> socket.socket:
    """
    Set multiple socket options.
    
    Args:
        sock: Socket to configure
        **options: Socket options as keyword arguments
        
    Returns:
        Configured socket
        
    Example:
        >>> set_socket_options(sock, reuse_addr=True, keep_alive=True, send_buffer_size=65536)
    """
    if options.get('reuse_addr'):
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    if options.get('keep_alive'):
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    
    if options.get('tcp_nodelay'):
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    
    if 'send_buffer_size' in options:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, options['send_buffer_size'])
    
    if 'recv_buffer_size' in options:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, options['recv_buffer_size'])
    
    if 'linger' in options:
        linger_struct = struct.pack('ii', 1, options['linger'])
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, linger_struct)
    
    return sock


# =============================================================================
# Protocol Helpers
# =============================================================================

def send_length_prefixed(sock: socket.socket, data: BytesLike) -> int:
    """
    Send data with a 4-byte length prefix.
    
    Args:
        sock: Socket to send on
        data: Data to send
        
    Returns:
        Total bytes sent (including length prefix)
        
    Example:
        >>> send_length_prefixed(sock, b"hello")
        9  # 4 bytes length + 5 bytes data
    """
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    length = len(data)
    length_prefix = struct.pack('>I', length)
    
    sock.sendall(length_prefix)
    sock.sendall(data)
    
    return 4 + length


def recv_length_prefixed(sock: socket.socket) -> bytes:
    """
    Receive length-prefixed data.
    
    Args:
        sock: Socket to receive from
        
    Returns:
        Received data
        
    Raises:
        ConnectionError: If connection breaks
    """
    # Read length prefix
    length_data = sock.recv(4)
    if len(length_data) < 4:
        raise ConnectionError("Incomplete length prefix")
    
    length = struct.unpack('>I', length_data)[0]
    
    # Read data
    data = bytearray()
    while len(data) < length:
        chunk = sock.recv(length - len(data))
        if not chunk:
            raise ConnectionError("Connection broken")
        data.extend(chunk)
    
    return bytes(data)


def send_json(sock: socket.socket, data: Any) -> int:
    """
    Send JSON data with length prefix.
    
    Args:
        sock: Socket to send on
        data: Data to serialize as JSON
        
    Returns:
        Total bytes sent
    """
    import json
    json_data = json.dumps(data).encode('utf-8')
    return send_length_prefixed(sock, json_data)


def recv_json(sock: socket.socket) -> Any:
    """
    Receive JSON data with length prefix.
    
    Args:
        sock: Socket to receive from
        
    Returns:
        Deserialized JSON data
    """
    import json
    data = recv_length_prefixed(sock)
    return json.loads(data.decode('utf-8'))


# =============================================================================
# Utility Functions
# =============================================================================

def socket_to_info(sock: socket.socket) -> ConnectionInfo:
    """
    Get detailed information about a socket.
    
    Args:
        sock: Socket to inspect
        
    Returns:
        ConnectionInfo with socket details
    """
    try:
        return ConnectionInfo(
            local_addr=sock.getsockname(),
            remote_addr=sock.getpeername() if sock.type == socket.SOCK_STREAM else None,
            family=sock.family,
            type=sock.type,
            proto=sock.proto,
            connected=True,
            ssl=isinstance(sock, ssl.SSLSocket)
        )
    except Exception:
        return ConnectionInfo()


def format_socket_address(addr: SocketAddress) -> str:
    """
    Format a socket address as a string.
    
    Args:
        addr: (host, port) tuple
        
    Returns:
        Formatted string like "192.168.1.1:8080"
    """
    return f"{addr[0]}:{addr[1]}"


def parse_socket_address(addr_str: str) -> SocketAddress:
    """
    Parse a socket address string.
    
    Args:
        addr_str: String like "192.168.1.1:8080"
        
    Returns:
        (host, port) tuple
        
    Raises:
        ValueError: If format is invalid
    """
    parts = addr_str.rsplit(':', 1)
    if len(parts) != 2:
        raise ValueError(f"Invalid address format: {addr_str}")
    
    host = parts[0]
    try:
        port = int(parts[1])
    except ValueError:
        raise ValueError(f"Invalid port: {parts[1]}")
    
    return (host, port)


# =============================================================================
# Module Info
# =============================================================================

def version() -> str:
    """Get module version."""
    return "1.0.0"


def features() -> List[str]:
    """Get list of available features."""
    return [
        "TCP Client/Server",
        "UDP Client",
        "SSL/TLS Support",
        "Connection Pooling",
        "Length-Prefixed Protocol",
        "JSON over Sockets",
        "Port Scanning",
        "Socket Helpers"
    ]
