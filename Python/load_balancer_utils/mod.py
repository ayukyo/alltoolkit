#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AllToolkit - Load Balancer Utilities Module

Implementation of various load balancing algorithms for distributing workloads
across multiple servers/resources. Zero external dependencies.

Features:
- Round Robin: Simple rotation through servers
- Weighted Round Robin: Weight-based rotation
- Least Connections: Route to server with fewest active connections
- Random: Random server selection
- IP Hash: Consistent routing based on client IP
- Weighted Random: Random selection with weights
- Health checking integration
- Connection tracking
- Server statistics and monitoring
- Thread-safe operations

Author: AllToolkit
License: MIT
"""

import random
import threading
import time
import hashlib
from typing import (
    Callable, Optional, Any, Dict, List, TypeVar, Generic,
    Iterator, Tuple, Set
)
from dataclasses import dataclass, field
from enum import Enum, auto
from abc import ABC, abstractmethod
from datetime import datetime


# =============================================================================
# Type Aliases and Generics
# =============================================================================

T = TypeVar('T')


# =============================================================================
# Enums and Constants
# =============================================================================

class LoadBalancerStrategy(Enum):
    """Load balancing strategies."""
    ROUND_ROBIN = auto()
    WEIGHTED_ROUND_ROBIN = auto()
    LEAST_CONNECTIONS = auto()
    RANDOM = auto()
    WEIGHTED_RANDOM = auto()
    IP_HASH = auto()


class ServerState(Enum):
    """Server health states."""
    HEALTHY = auto()
    UNHEALTHY = auto()
    DRAINING = auto()  # Accepting no new connections


# =============================================================================
# Data Classes
# =============================================================================

@dataclass
class ServerStats:
    """Statistics for a server."""
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    active_connections: int = 0
    total_connections: int = 0
    last_request_time: Optional[float] = None
    last_failure_time: Optional[float] = None
    consecutive_failures: int = 0
    avg_response_time_ms: float = 0.0
    
    def success_rate(self) -> float:
        """Calculate success rate as percentage."""
        if self.total_requests == 0:
            return 100.0
        return (self.successful_requests / self.total_requests) * 100.0


@dataclass
class Server(Generic[T]):
    """Represents a backend server/resource."""
    id: str
    target: T
    weight: int = 1
    state: ServerState = ServerState.HEALTHY
    stats: ServerStats = field(default_factory=ServerStats)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # Health check settings
    health_check_interval: float = 30.0  # seconds
    health_check_timeout: float = 5.0
    last_health_check: Optional[float] = None
    health_check_failures: int = 0
    max_health_check_failures: int = 3


# =============================================================================
# Exceptions
# =============================================================================

class LoadBalancerError(Exception):
    """Base exception for load balancer errors."""
    pass


class NoHealthyServerError(LoadBalancerError):
    """Raised when no healthy servers are available."""
    pass


class ServerNotFoundError(LoadBalancerError):
    """Raised when a server is not found."""
    pass


class InvalidWeightError(LoadBalancerError):
    """Raised when an invalid weight is provided."""
    pass


# =============================================================================
# Health Checker
# =============================================================================

class HealthChecker(ABC):
    """Abstract base class for health checkers."""
    
    @abstractmethod
    def check(self, server: Server) -> bool:
        """
        Check if server is healthy.
        
        Args:
            server: Server to check
            
        Returns:
            True if healthy, False otherwise
        """
        pass


class DefaultHealthChecker(HealthChecker):
    """Default health checker that uses TCP connection test."""
    
    def check(self, server: Server) -> bool:
        """
        Default health check - always returns True.
        Override this by providing a custom health checker.
        """
        return server.state != ServerState.UNHEALTHY


# =============================================================================
# Load Balancer Strategies
# =============================================================================

class LoadBalancerStrategyBase(ABC, Generic[T]):
    """Abstract base class for load balancing strategies."""
    
    @abstractmethod
    def select(self, servers: List[Server[T]], key: Optional[str] = None) -> Optional[Server[T]]:
        """
        Select a server from the list.
        
        Args:
            servers: List of available servers
            key: Optional key for consistent hashing strategies
            
        Returns:
            Selected server or None if no servers available
        """
        pass
    
    @abstractmethod
    def reset(self) -> None:
        """Reset strategy state."""
        pass


class RoundRobinStrategy(LoadBalancerStrategyBase[T]):
    """Round-robin load balancing strategy."""
    
    def __init__(self):
        self._index = 0
        self._lock = threading.Lock()
    
    def select(self, servers: List[Server[T]], key: Optional[str] = None) -> Optional[Server[T]]:
        """Select next server in rotation."""
        healthy_servers = [s for s in servers if s.state == ServerState.HEALTHY]
        if not healthy_servers:
            return None
        
        with self._lock:
            server = healthy_servers[self._index % len(healthy_servers)]
            self._index += 1
            return server
    
    def reset(self) -> None:
        with self._lock:
            self._index = 0


class WeightedRoundRobinStrategy(LoadBalancerStrategyBase[T]):
    """Weighted round-robin load balancing strategy."""
    
    def __init__(self):
        self._current_index = 0
        self._current_weight = 0
        self._lock = threading.Lock()
    
    def select(self, servers: List[Server[T]], key: Optional[str] = None) -> Optional[Server[T]]:
        """Select server based on weights."""
        healthy_servers = [s for s in servers if s.state == ServerState.HEALTHY]
        if not healthy_servers:
            return None
        
        with self._lock:
            # Sort by weight descending for efficient selection
            total_weight = sum(s.weight for s in healthy_servers)
            if total_weight == 0:
                return None
            
            # Weighted round-robin using smooth algorithm
            max_weight = max(s.weight for s in healthy_servers)
            gcd_weight = self._gcd_weights(healthy_servers)
            
            while True:
                self._current_index = (self._current_index + 1) % len(healthy_servers)
                
                if self._current_index == 0:
                    self._current_weight -= gcd_weight
                    if self._current_weight <= 0:
                        self._current_weight = max_weight
                        if self._current_weight == 0:
                            return healthy_servers[0]
                
                server = healthy_servers[self._current_index]
                if server.weight >= self._current_weight:
                    return server
    
    def _gcd_weights(self, servers: List[Server[T]]) -> int:
        """Calculate GCD of all weights."""
        def gcd(a: int, b: int) -> int:
            while b:
                a, b = b, a % b
            return a
        
        result = servers[0].weight if servers else 1
        for s in servers[1:]:
            result = gcd(result, s.weight)
        return result
    
    def reset(self) -> None:
        with self._lock:
            self._current_index = 0
            self._current_weight = 0


class LeastConnectionsStrategy(LoadBalancerStrategyBase[T]):
    """Least connections load balancing strategy."""
    
    def __init__(self):
        self._lock = threading.Lock()
    
    def select(self, servers: List[Server[T]], key: Optional[str] = None) -> Optional[Server[T]]:
        """Select server with least active connections."""
        healthy_servers = [s for s in servers if s.state == ServerState.HEALTHY]
        if not healthy_servers:
            return None
        
        with self._lock:
            return min(healthy_servers, key=lambda s: s.stats.active_connections)
    
    def reset(self) -> None:
        pass


class RandomStrategy(LoadBalancerStrategyBase[T]):
    """Random load balancing strategy."""
    
    def select(self, servers: List[Server[T]], key: Optional[str] = None) -> Optional[Server[T]]:
        """Select a random server."""
        healthy_servers = [s for s in servers if s.state == ServerState.HEALTHY]
        if not healthy_servers:
            return None
        return random.choice(healthy_servers)
    
    def reset(self) -> None:
        pass


class WeightedRandomStrategy(LoadBalancerStrategyBase[T]):
    """Weighted random load balancing strategy."""
    
    def select(self, servers: List[Server[T]], key: Optional[str] = None) -> Optional[Server[T]]:
        """Select a server randomly, weighted by server weight."""
        healthy_servers = [s for s in servers if s.state == ServerState.HEALTHY]
        if not healthy_servers:
            return None
        
        total_weight = sum(s.weight for s in healthy_servers)
        if total_weight == 0:
            return None
        
        r = random.randint(1, total_weight)
        cumulative = 0
        for server in healthy_servers:
            cumulative += server.weight
            if r <= cumulative:
                return server
        
        return healthy_servers[-1]
    
    def reset(self) -> None:
        pass


class IPHashStrategy(LoadBalancerStrategyBase[T]):
    """IP hash load balancing strategy for consistent routing."""
    
    def __init__(self, replicas: int = 160):
        self._replicas = replicas
        self._ring: Dict[int, Server[T]] = {}
        self._sorted_keys: List[int] = []
        self._lock = threading.Lock()
    
    def _build_ring(self, servers: List[Server[T]]) -> None:
        """Build the hash ring."""
        self._ring.clear()
        self._sorted_keys.clear()
        
        for server in servers:
            if server.state == ServerState.HEALTHY:
                for i in range(self._replicas):
                    key = self._hash(f"{server.id}:{i}")
                    self._ring[key] = server
                    self._sorted_keys.append(key)
        
        self._sorted_keys.sort()
    
    def _hash(self, key: str) -> int:
        """Generate consistent hash for key."""
        return int(hashlib.md5(key.encode()).hexdigest(), 16)
    
    def select(self, servers: List[Server[T]], key: Optional[str] = None) -> Optional[Server[T]]:
        """Select server based on key hash."""
        healthy_servers = [s for s in servers if s.state == ServerState.HEALTHY]
        if not healthy_servers:
            return None
        
        # If no key provided, fall back to random
        if key is None:
            return random.choice(healthy_servers)
        
        with self._lock:
            self._build_ring(servers)
            
            if not self._sorted_keys:
                return None
            
            hash_key = self._hash(key)
            
            # Find first server with hash >= key hash
            for ring_key in self._sorted_keys:
                if ring_key >= hash_key:
                    return self._ring[ring_key]
            
            # Wrap around to first server
            return self._ring[self._sorted_keys[0]]
    
    def reset(self) -> None:
        with self._lock:
            self._ring.clear()
            self._sorted_keys.clear()


# =============================================================================
# Main Load Balancer Class
# =============================================================================

class LoadBalancer(Generic[T]):
    """
    Thread-safe load balancer with multiple strategies.
    
    Example:
        >>> lb = LoadBalancer(strategy=LoadBalancerStrategy.ROUND_ROBIN)
        >>> lb.add_server("server1", "192.168.1.1:8080", weight=3)
        >>> lb.add_server("server2", "192.168.1.2:8080", weight=2)
        >>> server = lb.select()
        >>> with lb.connection(server):
        ...     # Use server.target
        ...     pass
    """
    
    def __init__(
        self,
        strategy: LoadBalancerStrategy = LoadBalancerStrategy.ROUND_ROBIN,
        health_checker: Optional[HealthChecker] = None,
        health_check_interval: float = 30.0,
        enable_stats: bool = True
    ):
        """
        Initialize load balancer.
        
        Args:
            strategy: Load balancing strategy
            health_checker: Optional health checker
            health_check_interval: Seconds between health checks
            enable_stats: Whether to track statistics
        """
        self._servers: Dict[str, Server[T]] = {}
        self._strategy = self._create_strategy(strategy)
        self._strategy_enum = strategy
        self._health_checker = health_checker or DefaultHealthChecker()
        self._health_check_interval = health_check_interval
        self._enable_stats = enable_stats
        self._lock = threading.RLock()
        
        # Health check thread
        self._health_check_thread: Optional[threading.Thread] = None
        self._health_check_running = False
    
    def _create_strategy(self, strategy: LoadBalancerStrategy) -> LoadBalancerStrategyBase[T]:
        """Create strategy instance."""
        strategies = {
            LoadBalancerStrategy.ROUND_ROBIN: RoundRobinStrategy,
            LoadBalancerStrategy.WEIGHTED_ROUND_ROBIN: WeightedRoundRobinStrategy,
            LoadBalancerStrategy.LEAST_CONNECTIONS: LeastConnectionsStrategy,
            LoadBalancerStrategy.RANDOM: RandomStrategy,
            LoadBalancerStrategy.WEIGHTED_RANDOM: WeightedRandomStrategy,
            LoadBalancerStrategy.IP_HASH: IPHashStrategy,
        }
        return strategies[strategy]()
    
    # =========================================================================
    # Server Management
    # =========================================================================
    
    def add_server(
        self,
        server_id: str,
        target: T,
        weight: int = 1,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Server[T]:
        """
        Add a server to the pool.
        
        Args:
            server_id: Unique server identifier
            target: Server target (e.g., URL, address, connection)
            weight: Server weight for weighted strategies
            metadata: Optional metadata
            
        Returns:
            Added server
            
        Raises:
            InvalidWeightError: If weight is <= 0
        """
        if weight <= 0:
            raise InvalidWeightError(f"Weight must be positive, got {weight}")
        
        with self._lock:
            server = Server(
                id=server_id,
                target=target,
                weight=weight,
                metadata=metadata or {}
            )
            self._servers[server_id] = server
            return server
    
    def remove_server(self, server_id: str) -> bool:
        """
        Remove a server from the pool.
        
        Args:
            server_id: Server ID to remove
            
        Returns:
            True if removed, False if not found
        """
        with self._lock:
            if server_id in self._servers:
                del self._servers[server_id]
                return True
            return False
    
    def get_server(self, server_id: str) -> Optional[Server[T]]:
        """Get server by ID."""
        with self._lock:
            return self._servers.get(server_id)
    
    def set_server_weight(self, server_id: str, weight: int) -> bool:
        """Set server weight."""
        if weight <= 0:
            raise InvalidWeightError(f"Weight must be positive, got {weight}")
        
        with self._lock:
            if server_id in self._servers:
                self._servers[server_id].weight = weight
                return True
            return False
    
    def mark_server_healthy(self, server_id: str) -> bool:
        """Mark a server as healthy."""
        with self._lock:
            if server_id in self._servers:
                self._servers[server_id].state = ServerState.HEALTHY
                self._servers[server_id].health_check_failures = 0
                return True
            return False
    
    def mark_server_unhealthy(self, server_id: str) -> bool:
        """Mark a server as unhealthy."""
        with self._lock:
            if server_id in self._servers:
                self._servers[server_id].state = ServerState.UNHEALTHY
                return True
            return False
    
    def drain_server(self, server_id: str) -> bool:
        """Mark a server for draining (no new connections)."""
        with self._lock:
            if server_id in self._servers:
                self._servers[server_id].state = ServerState.DRAINING
                return True
            return False
    
    @property
    def servers(self) -> List[Server[T]]:
        """Get all servers."""
        with self._lock:
            return list(self._servers.values())
    
    @property
    def healthy_servers(self) -> List[Server[T]]:
        """Get healthy servers."""
        with self._lock:
            return [s for s in self._servers.values() if s.state == ServerState.HEALTHY]
    
    @property
    def server_count(self) -> int:
        """Get total server count."""
        with self._lock:
            return len(self._servers)
    
    # =========================================================================
    # Selection
    # =========================================================================
    
    def select(self, key: Optional[str] = None) -> Server[T]:
        """
        Select a server using the configured strategy.
        
        Args:
            key: Optional key for consistent hashing (IP_HASH strategy)
            
        Returns:
            Selected server
            
        Raises:
            NoHealthyServerError: If no healthy servers available
        """
        with self._lock:
            servers = list(self._servers.values())
            
        server = self._strategy.select(servers, key)
        
        if server is None:
            raise NoHealthyServerError("No healthy servers available")
        
        # Update stats
        if self._enable_stats:
            server.stats.total_requests += 1
            server.stats.last_request_time = time.time()
        
        return server
    
    def select_all(self, key: Optional[str] = None) -> Iterator[Server[T]]:
        """
        Iterate through servers in load-balanced order.
        
        Args:
            key: Optional key for consistent hashing
            
        Yields:
            Servers in load-balanced order
        """
        with self._lock:
            servers = list(self._servers.values())
        
        # Try each server once
        for _ in range(len(servers)):
            server = self._strategy.select(servers, key)
            if server:
                yield server
    
    # =========================================================================
    # Connection Tracking
    # =========================================================================
    
    def connection(self, server: Server[T]) -> 'ConnectionContext[T]':
        """
        Create a connection context manager.
        
        Usage:
            >>> server = lb.select()
            >>> with lb.connection(server):
            ...     # Make request to server.target
            ...     pass
        """
        return ConnectionContext(self, server)
    
    def _increment_connection(self, server: Server[T]) -> None:
        """Increment connection count for server."""
        if self._enable_stats:
            server.stats.active_connections += 1
            server.stats.total_connections += 1
    
    def _decrement_connection(self, server: Server[T]) -> None:
        """Decrement connection count for server."""
        if self._enable_stats:
            server.stats.active_connections = max(0, server.stats.active_connections - 1)
    
    def record_success(self, server: Server[T], response_time_ms: Optional[float] = None) -> None:
        """Record a successful request."""
        if self._enable_stats:
            server.stats.successful_requests += 1
            server.stats.consecutive_failures = 0
            if response_time_ms is not None:
                # Simple moving average
                if server.stats.avg_response_time_ms == 0:
                    server.stats.avg_response_time_ms = response_time_ms
                else:
                    server.stats.avg_response_time_ms = (
                        server.stats.avg_response_time_ms * 0.9 + response_time_ms * 0.1
                    )
    
    def record_failure(self, server: Server[T]) -> None:
        """Record a failed request."""
        if self._enable_stats:
            server.stats.failed_requests += 1
            server.stats.last_failure_time = time.time()
            server.stats.consecutive_failures += 1
    
    # =========================================================================
    # Health Checking
    # =========================================================================
    
    def start_health_checks(self) -> None:
        """Start background health check thread."""
        if self._health_check_running:
            return
        
        self._health_check_running = True
        self._health_check_thread = threading.Thread(
            target=self._health_check_loop,
            daemon=True
        )
        self._health_check_thread.start()
    
    def stop_health_checks(self) -> None:
        """Stop background health check thread."""
        self._health_check_running = False
        if self._health_check_thread:
            self._health_check_thread.join(timeout=5)
            self._health_check_thread = None
    
    def _health_check_loop(self) -> None:
        """Background health check loop."""
        while self._health_check_running:
            try:
                self.run_health_checks()
            except Exception:
                pass
            time.sleep(self._health_check_interval)
    
    def run_health_checks(self) -> Dict[str, bool]:
        """
        Run health checks on all servers.
        
        Returns:
            Dict mapping server IDs to health status
        """
        results = {}
        
        with self._lock:
            servers = list(self._servers.values())
        
        for server in servers:
            try:
                is_healthy = self._health_checker.check(server)
                results[server.id] = is_healthy
                server.last_health_check = time.time()
                
                if is_healthy:
                    server.health_check_failures = 0
                    if server.state == ServerState.UNHEALTHY:
                        server.state = ServerState.HEALTHY
                else:
                    server.health_check_failures += 1
                    if server.health_check_failures >= server.max_health_check_failures:
                        server.state = ServerState.UNHEALTHY
                        
            except Exception:
                results[server.id] = False
                server.health_check_failures += 1
        
        return results
    
    # =========================================================================
    # Statistics
    # =========================================================================
    
    def get_stats(self) -> Dict[str, Any]:
        """Get load balancer statistics."""
        with self._lock:
            servers = list(self._servers.values())
        
        total_requests = sum(s.stats.total_requests for s in servers)
        total_success = sum(s.stats.successful_requests for s in servers)
        total_failures = sum(s.stats.failed_requests for s in servers)
        total_connections = sum(s.stats.active_connections for s in servers)
        
        return {
            "strategy": self._strategy_enum.name,
            "total_servers": len(servers),
            "healthy_servers": len([s for s in servers if s.state == ServerState.HEALTHY]),
            "unhealthy_servers": len([s for s in servers if s.state == ServerState.UNHEALTHY]),
            "draining_servers": len([s for s in servers if s.state == ServerState.DRAINING]),
            "total_requests": total_requests,
            "successful_requests": total_success,
            "failed_requests": total_failures,
            "active_connections": total_connections,
            "success_rate": (total_success / total_requests * 100) if total_requests > 0 else 100,
            "servers": {
                s.id: {
                    "weight": s.weight,
                    "state": s.state.name,
                    "total_requests": s.stats.total_requests,
                    "successful_requests": s.stats.successful_requests,
                    "failed_requests": s.stats.failed_requests,
                    "active_connections": s.stats.active_connections,
                    "success_rate": s.stats.success_rate(),
                    "avg_response_time_ms": s.stats.avg_response_time_ms
                }
                for s in servers
            }
        }
    
    def reset_stats(self) -> None:
        """Reset all statistics."""
        with self._lock:
            for server in self._servers.values():
                server.stats = ServerStats()
    
    def reset(self) -> None:
        """Reset load balancer state."""
        with self._lock:
            self._strategy.reset()
            for server in self._servers.values():
                server.stats = ServerStats()


# =============================================================================
# Connection Context Manager
# =============================================================================

class ConnectionContext(Generic[T]):
    """Context manager for tracking connections."""
    
    def __init__(self, load_balancer: LoadBalancer[T], server: Server[T]):
        self._lb = load_balancer
        self._server = server
        self._start_time: Optional[float] = None
    
    def __enter__(self) -> Server[T]:
        self._lb._increment_connection(self._server)
        self._start_time = time.time()
        return self._server
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self._lb._decrement_connection(self._server)
        
        # Record success/failure
        if exc_type is None:
            response_time_ms = (time.time() - self._start_time) * 1000 if self._start_time else None
            self._lb.record_success(self._server, response_time_ms)
        else:
            self._lb.record_failure(self._server)


# =============================================================================
# Convenience Functions
# =============================================================================

def create_round_robin_balancer(servers: Optional[List[Tuple[str, T, int]]] = None) -> LoadBalancer[T]:
    """
    Create a round-robin load balancer.
    
    Args:
        servers: Optional list of (id, target, weight) tuples
        
    Returns:
        Configured load balancer
    """
    lb = LoadBalancer(strategy=LoadBalancerStrategy.ROUND_ROBIN)
    if servers:
        for server_id, target, weight in servers:
            lb.add_server(server_id, target, weight)
    return lb


def create_weighted_balancer(servers: Optional[List[Tuple[str, T, int]]] = None) -> LoadBalancer[T]:
    """
    Create a weighted round-robin load balancer.
    
    Args:
        servers: Optional list of (id, target, weight) tuples
        
    Returns:
        Configured load balancer
    """
    lb = LoadBalancer(strategy=LoadBalancerStrategy.WEIGHTED_ROUND_ROBIN)
    if servers:
        for server_id, target, weight in servers:
            lb.add_server(server_id, target, weight)
    return lb


def create_least_connections_balancer(servers: Optional[List[Tuple[str, T, int]]] = None) -> LoadBalancer[T]:
    """
    Create a least-connections load balancer.
    
    Args:
        servers: Optional list of (id, target, weight) tuples
        
    Returns:
        Configured load balancer
    """
    lb = LoadBalancer(strategy=LoadBalancerStrategy.LEAST_CONNECTIONS)
    if servers:
        for server_id, target, weight in servers:
            lb.add_server(server_id, target, weight)
    return lb


# =============================================================================
# Main (for testing)
# =============================================================================

if __name__ == "__main__":
    # Demo usage
    print("=== Load Balancer Demo ===\n")
    
    # Create load balancer with weighted round-robin
    lb = LoadBalancer(strategy=LoadBalancerStrategy.WEIGHTED_ROUND_ROBIN)
    
    # Add servers
    lb.add_server("server1", "192.168.1.1:8080", weight=3)
    lb.add_server("server2", "192.168.1.2:8080", weight=2)
    lb.add_server("server3", "192.168.1.3:8080", weight=1)
    
    print("Servers added:")
    for s in lb.servers:
        print(f"  - {s.id}: {s.target} (weight={s.weight})")
    print()
    
    # Simulate requests
    print("Simulating 10 requests:")
    selection_counts: Dict[str, int] = {}
    for i in range(10):
        server = lb.select()
        selection_counts[server.id] = selection_counts.get(server.id, 0) + 1
        print(f"  Request {i+1}: {server.id}")
    print()
    
    print("Selection counts:", selection_counts)
    print()
    
    # Show stats
    stats = lb.get_stats()
    print("Load Balancer Stats:")
    print(f"  Strategy: {stats['strategy']}")
    print(f"  Total servers: {stats['total_servers']}")
    print(f"  Healthy servers: {stats['healthy_servers']}")
    print(f"  Total requests: {stats['total_requests']}")
    
    print("\n=== Demo Complete ===")