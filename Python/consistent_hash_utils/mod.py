"""
AllToolkit - Python Consistent Hash Utilities

A zero-dependency, production-ready consistent hashing utility module.
Supports virtual nodes, weighted nodes, and smooth data migration.

Consistent hashing is used in distributed systems for:
- Distributed caching (Redis cluster, Memcached)
- Load balancing
- Data sharding
- Distributed storage

Author: AllToolkit
License: MIT
"""

import hashlib
import threading
from typing import (
    Dict, List, Optional, Set, Tuple, Any, 
    Callable, TypeVar, Generic, Iterator
)
from dataclasses import dataclass, field
from collections import defaultdict
import bisect


T = TypeVar('T')


def _hash_key(key: str, algorithm: str = 'md5') -> int:
    """
    Hash a string key to an integer on the hash ring.
    
    Args:
        key: String to hash
        algorithm: Hash algorithm ('md5', 'sha1', 'sha256')
    
    Returns:
        Integer hash value (0 to 2^32-1)
    """
    if algorithm == 'md5':
        h = hashlib.md5(key.encode(), usedforsecurity=False)
    elif algorithm == 'sha1':
        h = hashlib.sha1(key.encode(), usedforsecurity=False)
    elif algorithm == 'sha256':
        h = hashlib.sha256(key.encode(), usedforsecurity=False)
    else:
        raise ValueError(f"Unsupported hash algorithm: {algorithm}")
    
    # Use first 4 bytes for 32-bit hash value
    return int.from_bytes(h.digest()[:4], 'big')


@dataclass
class Node:
    """Represents a node in the consistent hash ring."""
    name: str
    weight: int = 1
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __hash__(self) -> int:
        return hash(self.name)
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Node):
            return False
        return self.name == other.name
    
    def __repr__(self) -> str:
        return f"Node({self.name!r}, weight={self.weight})"


@dataclass
class Migration:
    """Represents a data migration between nodes."""
    key: str
    source_node: Optional[str]
    target_node: str
    
    def __repr__(self) -> str:
        if self.source_node:
            return f"Migration({self.key!r}: {self.source_node} -> {self.target_node})"
        return f"Migration({self.key!r}: -> {self.target_node})"


class ConsistentHash:
    """
    Basic consistent hash ring implementation.
    
    Maps keys to nodes using consistent hashing. When nodes are added
    or removed, only a fraction of keys need to be remapped.
    
    Example:
        ring = ConsistentHash()
        ring.add_node('node1')
        ring.add_node('node2')
        
        node = ring.get_node('user:123')  # Returns 'node1' or 'node2'
    """
    
    def __init__(
        self, 
        virtual_nodes: int = 150,
        hash_algorithm: str = 'md5'
    ):
        """
        Initialize consistent hash ring.
        
        Args:
            virtual_nodes: Number of virtual nodes per physical node
            hash_algorithm: Hash algorithm ('md5', 'sha1', 'sha256')
        """
        if virtual_nodes < 1:
            raise ValueError("virtual_nodes must be at least 1")
        
        self._virtual_nodes = virtual_nodes
        self._hash_algorithm = hash_algorithm
        self._ring: Dict[int, str] = {}  # hash -> node name
        self._sorted_hashes: List[int] = []
        self._nodes: Dict[str, Node] = {}
        self._lock = threading.RLock()
    
    @property
    def virtual_nodes(self) -> int:
        """Get number of virtual nodes per physical node."""
        return self._virtual_nodes
    
    @property
    def hash_algorithm(self) -> str:
        """Get the hash algorithm used."""
        return self._hash_algorithm
    
    @property
    def node_count(self) -> int:
        """Get number of physical nodes."""
        return len(self._nodes)
    
    @property
    def nodes(self) -> List[str]:
        """Get list of node names."""
        return list(self._nodes.keys())
    
    def _get_virtual_node_keys(self, node: str, replica_index: int) -> str:
        """Generate virtual node key for hashing."""
        return f"{node}#{replica_index}"
    
    def add_node(self, name: str, weight: int = 1, metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Add a node to the hash ring.
        
        Args:
            name: Unique node identifier
            weight: Node weight (affects virtual node count)
            metadata: Optional metadata dictionary
        """
        with self._lock:
            if name in self._nodes:
                raise ValueError(f"Node {name!r} already exists")
            
            node = Node(name=name, weight=weight, metadata=metadata or {})
            self._nodes[name] = node
            
            # Create virtual nodes
            num_virtual = self._virtual_nodes * weight
            for i in range(num_virtual):
                vkey = self._get_virtual_node_keys(name, i)
                hash_val = _hash_key(vkey, self._hash_algorithm)
                self._ring[hash_val] = name
            
            self._sorted_hashes = sorted(self._ring.keys())
    
    def remove_node(self, name: str) -> None:
        """
        Remove a node from the hash ring.
        
        Args:
            name: Node identifier to remove
        """
        with self._lock:
            if name not in self._nodes:
                raise KeyError(f"Node {name!r} not found")
            
            node = self._nodes[name]
            
            # Remove virtual nodes
            num_virtual = self._virtual_nodes * node.weight
            for i in range(num_virtual):
                vkey = self._get_virtual_node_keys(name, i)
                hash_val = _hash_key(vkey, self._hash_algorithm)
                self._ring.pop(hash_val, None)
            
            del self._nodes[name]
            self._sorted_hashes = sorted(self._ring.keys())
    
    def get_node(self, key: str) -> Optional[str]:
        """
        Get the node responsible for a key.
        
        Args:
            key: Key to look up
            
        Returns:
            Node name or None if ring is empty
        """
        with self._lock:
            if not self._sorted_hashes:
                return None
            
            hash_val = _hash_key(key, self._hash_algorithm)
            
            # Find first node with hash >= key hash
            idx = bisect.bisect_left(self._sorted_hashes, hash_val)
            
            # Wrap around to first node if needed
            if idx >= len(self._sorted_hashes):
                idx = 0
            
            return self._ring[self._sorted_hashes[idx]]
    
    def get_nodes(self, key: str, count: int = 1) -> List[str]:
        """
        Get multiple nodes for a key (for replication).
        
        Args:
            key: Key to look up
            count: Number of nodes to return
            
        Returns:
            List of distinct node names
        """
        with self._lock:
            if not self._sorted_hashes or count <= 0:
                return []
            
            hash_val = _hash_key(key, self._hash_algorithm)
            idx = bisect.bisect_left(self._sorted_hashes, hash_val)
            
            result: List[str] = []
            seen: Set[str] = set()
            
            for i in range(len(self._sorted_hashes)):
                pos = (idx + i) % len(self._sorted_hashes)
                node = self._ring[self._sorted_hashes[pos]]
                
                if node not in seen:
                    seen.add(node)
                    result.append(node)
                    
                    if len(result) >= count:
                        break
            
            return result
    
    def get_node_metadata(self, name: str) -> Optional[Dict[str, Any]]:
        """Get metadata for a node."""
        with self._lock:
            node = self._nodes.get(name)
            return node.metadata.copy() if node else None
    
    def get_node_weight(self, name: str) -> int:
        """Get weight for a node."""
        with self._lock:
            node = self._nodes.get(name)
            return node.weight if node else 0
    
    def get_key_distribution(self, keys: List[str]) -> Dict[str, int]:
        """
        Get distribution of keys across nodes.
        
        Args:
            keys: List of keys to analyze
            
        Returns:
            Dictionary mapping node names to key counts
        """
        distribution: Dict[str, int] = defaultdict(int)
        
        with self._lock:
            for key in keys:
                node = self.get_node(key)
                if node:
                    distribution[node] += 1
        
        return dict(distribution)
    
    def calculate_migration(self, keys: List[str], new_nodes: List[str], removed_nodes: List[str]) -> List[Migration]:
        """
        Calculate key migrations when topology changes.
        
        Args:
            keys: List of keys to check
            new_nodes: Nodes being added
            removed_nodes: Nodes being removed
            
        Returns:
            List of Migration objects
        """
        migrations: List[Migration] = []
        
        # Create a copy of current ring state
        with self._lock:
            old_nodes = dict(self._nodes)
        
        # Create new ring
        new_ring = ConsistentHash(
            virtual_nodes=self._virtual_nodes,
            hash_algorithm=self._hash_algorithm
        )
        
        for name, node in old_nodes.items():
            if name not in removed_nodes:
                new_ring.add_node(name, node.weight, node.metadata)
        
        for name in new_nodes:
            new_ring.add_node(name)
        
        # Find migrations
        for key in keys:
            old_node = self.get_node(key)
            new_node = new_ring.get_node(key)
            
            if old_node != new_node:
                migrations.append(Migration(
                    key=key,
                    source_node=old_node,
                    target_node=new_node
                ))
        
        return migrations
    
    def get_ring_info(self) -> Dict[str, Any]:
        """Get detailed information about the ring state."""
        with self._lock:
            return {
                'node_count': len(self._nodes),
                'virtual_node_count': len(self._ring),
                'virtual_nodes_per_node': self._virtual_nodes,
                'hash_algorithm': self._hash_algorithm,
                'nodes': [
                    {
                        'name': name,
                        'weight': node.weight,
                        'metadata': node.metadata
                    }
                    for name, node in self._nodes.items()
                ]
            }
    
    def clear(self) -> None:
        """Remove all nodes from the ring."""
        with self._lock:
            self._ring.clear()
            self._sorted_hashes.clear()
            self._nodes.clear()
    
    def __contains__(self, name: str) -> bool:
        return name in self._nodes
    
    def __len__(self) -> int:
        return len(self._nodes)
    
    def __iter__(self) -> Iterator[str]:
        return iter(self._nodes.keys())


class WeightedConsistentHash(ConsistentHash):
    """
    Consistent hash ring with weighted node distribution.
    
    Nodes with higher weights receive proportionally more keys.
    Useful for heterogeneous clusters where nodes have different capacities.
    
    Example:
        ring = WeightedConsistentHash()
        ring.add_node('small-node', weight=1)
        ring.add_node('large-node', weight=3)  # Gets ~3x more keys
    """
    
    def __init__(
        self,
        virtual_nodes: int = 150,
        hash_algorithm: str = 'md5'
    ):
        super().__init__(virtual_nodes=virtual_nodes, hash_algorithm=hash_algorithm)
    
    def add_node(
        self, 
        name: str, 
        weight: int = 1, 
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Add a weighted node to the ring.
        
        Args:
            name: Unique node identifier
            weight: Node weight (higher = more keys)
            metadata: Optional metadata dictionary
        """
        if weight <= 0:
            raise ValueError("Weight must be positive")
        super().add_node(name, weight, metadata)
    
    def get_weight_distribution(self) -> Dict[str, float]:
        """Get actual weight distribution in the ring."""
        with self._lock:
            total_weight = sum(n.weight for n in self._nodes.values())
            if total_weight == 0:
                return {}
            
            return {
                name: node.weight / total_weight
                for name, node in self._nodes.items()
            }
    
    def rebalance(self, keys: List[str]) -> Dict[str, List[str]]:
        """
        Get rebalancing plan after weight changes.
        
        Args:
            keys: All keys in the system
            
        Returns:
            Dictionary mapping node names to their assigned keys
        """
        assignments: Dict[str, List[str]] = defaultdict(list)
        
        for key in keys:
            node = self.get_node(key)
            if node:
                assignments[node].append(key)
        
        return dict(assignments)


class RendezvousHash:
    """
    Rendezvous (HRW) hashing implementation.
    
    An alternative to consistent hashing that doesn't require ring maintenance.
    Each key is assigned to the node with the highest hash of (node, key).
    
    Advantages:
    - No ring maintenance overhead
    - Even distribution without virtual nodes
    - Supports weighted nodes naturally
    
    Example:
        hash = RendezvousHash()
        hash.add_node('node1', weight=2)
        hash.add_node('node2', weight=1)
        
        node = hash.get_node('user:123')
    """
    
    def __init__(self, hash_algorithm: str = 'md5'):
        """
        Initialize rendezvous hash.
        
        Args:
            hash_algorithm: Hash algorithm ('md5', 'sha1', 'sha256')
        """
        self._hash_algorithm = hash_algorithm
        self._nodes: Dict[str, Node] = {}
        self._lock = threading.RLock()
    
    @property
    def node_count(self) -> int:
        return len(self._nodes)
    
    @property
    def nodes(self) -> List[str]:
        return list(self._nodes.keys())
    
    def _compute_score(self, node: str, key: str) -> int:
        """Compute rendezvous score for a (node, key) pair."""
        combined = f"{node}:{key}"
        return _hash_key(combined, self._hash_algorithm)
    
    def add_node(
        self, 
        name: str, 
        weight: int = 1,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Add a node to the hash.
        
        Args:
            name: Unique node identifier
            weight: Node weight (affects selection probability)
            metadata: Optional metadata dictionary
        """
        if weight <= 0:
            raise ValueError("Weight must be positive")
        
        with self._lock:
            self._nodes[name] = Node(name=name, weight=weight, metadata=metadata or {})
    
    def remove_node(self, name: str) -> None:
        """
        Remove a node from the hash.
        
        Args:
            name: Node identifier to remove
        """
        with self._lock:
            if name not in self._nodes:
                raise KeyError(f"Node {name!r} not found")
            del self._nodes[name]
    
    def get_node(self, key: str) -> Optional[str]:
        """
        Get the node responsible for a key.
        
        Args:
            key: Key to look up
            
        Returns:
            Node name or None if no nodes
        """
        with self._lock:
            if not self._nodes:
                return None
            
            best_node: Optional[str] = None
            best_score = -1
            
            for name, node in self._nodes.items():
                # Apply weight: repeat hash computation for weighted nodes
                for w in range(node.weight):
                    score = self._compute_score(f"{name}#{w}", key)
                    if score > best_score:
                        best_score = score
                        best_node = name
            
            return best_node
    
    def get_nodes(self, key: str, count: int = 1) -> List[str]:
        """
        Get multiple nodes for a key (for replication).
        
        Args:
            key: Key to look up
            count: Number of nodes to return
            
        Returns:
            List of distinct node names
        """
        with self._lock:
            if not self._nodes or count <= 0:
                return []
            
            # Calculate all scores
            scores: List[Tuple[str, int]] = []
            for name, node in self._nodes.items():
                for w in range(node.weight):
                    score = self._compute_score(f"{name}#{w}", key)
                    scores.append((name, score))
            
            # Sort by score descending
            scores.sort(key=lambda x: x[1], reverse=True)
            
            # Return distinct nodes
            result: List[str] = []
            seen: Set[str] = set()
            
            for name, _ in scores:
                if name not in seen:
                    seen.add(name)
                    result.append(name)
                    if len(result) >= count:
                        break
            
            return result
    
    def clear(self) -> None:
        """Remove all nodes."""
        with self._lock:
            self._nodes.clear()
    
    def __contains__(self, name: str) -> bool:
        return name in self._nodes
    
    def __len__(self) -> int:
        return len(self._nodes)


class JumpConsistentHash:
    """
    Jump consistent hash implementation.
    
    A memory-efficient consistent hashing algorithm that uses O(1) space.
    Based on the paper "A Fast, Minimal Memory, Consistent Hash Algorithm"
    by John Lamping and Eric Veach.
    
    Advantages:
    - O(1) space complexity
    - O(1) time complexity per lookup
    - Even distribution
    - No configuration needed
    
    Limitations:
    - Only supports sequential bucket numbering (0, 1, 2, ...)
    - Adding/removing buckets causes reshuffling
    
    Example:
        hash = JumpConsistentHash(num_buckets=10)
        bucket = hash.get_bucket('user:123')  # Returns 0-9
    """
    
    def __init__(self, num_buckets: int):
        """
        Initialize jump consistent hash.
        
        Args:
            num_buckets: Number of buckets (must be positive)
        """
        if num_buckets <= 0:
            raise ValueError("num_buckets must be positive")
        
        self._num_buckets = num_buckets
        self._lock = threading.RLock()
    
    @property
    def num_buckets(self) -> int:
        return self._num_buckets
    
    def _jump_hash(self, key: int, num_buckets: int) -> int:
        """
        Jump consistent hash algorithm.
        
        Args:
            key: Integer key (usually hash of string key)
            num_buckets: Number of buckets
            
        Returns:
            Bucket index (0 to num_buckets-1)
        """
        # Constants for the algorithm
        INT64_MAX = (1 << 63) - 1
        
        b = -1
        j = 0
        
        while j < num_buckets:
            b = j
            key = ((key * 2862933555777941757) + 1) & 0xFFFFFFFFFFFFFFFF
            j = int((b + 1) * ((1 << 31) / ((key >> 33) + 1)))
        
        return b
    
    def get_bucket(self, key: str) -> int:
        """
        Get bucket for a key.
        
        Args:
            key: String key to hash
            
        Returns:
            Bucket index (0 to num_buckets-1)
        """
        hash_val = _hash_key(key, 'md5')
        return self._jump_hash(hash_val, self._num_buckets)
    
    def get_bucket_for_int(self, key: int) -> int:
        """
        Get bucket for an integer key.
        
        Args:
            key: Integer key
            
        Returns:
            Bucket index
        """
        return self._jump_hash(key, self._num_buckets)
    
    def resize(self, new_num_buckets: int) -> None:
        """
        Resize the number of buckets.
        
        Args:
            new_num_buckets: New number of buckets
        """
        if new_num_buckets <= 0:
            raise ValueError("new_num_buckets must be positive")
        
        with self._lock:
            self._num_buckets = new_num_buckets
    
    def get_distribution(self, keys: List[str]) -> Dict[int, int]:
        """
        Get distribution of keys across buckets.
        
        Args:
            keys: List of keys to analyze
            
        Returns:
            Dictionary mapping bucket indices to key counts
        """
        distribution: Dict[int, int] = defaultdict(int)
        
        for key in keys:
            bucket = self.get_bucket(key)
            distribution[bucket] += 1
        
        return dict(distribution)
    
    def __len__(self) -> int:
        return self._num_buckets


class MultiHash:
    """
    Multi-hash consistent hashing for high availability.
    
    Uses multiple hash functions to find backup nodes when the
    primary node is unavailable.
    
    Example:
        mhash = MultiHash(num_replicas=3)
        mhash.add_node('node1')
        mhash.add_node('node2')
        mhash.add_node('node3')
        
        # Get primary and backup nodes
        nodes = mhash.get_nodes_with_fallback('key', unavailable={'node1'})
    """
    
    def __init__(
        self,
        num_replicas: int = 3,
        virtual_nodes: int = 150,
        hash_algorithms: Optional[List[str]] = None
    ):
        """
        Initialize multi-hash.
        
        Args:
            num_replicas: Number of replica nodes
            virtual_nodes: Virtual nodes per physical node
            hash_algorithms: List of hash algorithms to use
        """
        self._num_replicas = num_replicas
        self._virtual_nodes = virtual_nodes
        self._hash_algorithms = hash_algorithms or ['md5', 'sha1', 'sha256']
        self._rings: List[ConsistentHash] = []
        self._nodes: Dict[str, Node] = {}
        self._lock = threading.RLock()
        
        # Create a ring for each hash algorithm
        for algo in self._hash_algorithms[:num_replicas]:
            self._rings.append(ConsistentHash(
                virtual_nodes=virtual_nodes,
                hash_algorithm=algo
            ))
    
    @property
    def node_count(self) -> int:
        return len(self._nodes)
    
    @property
    def nodes(self) -> List[str]:
        return list(self._nodes.keys())
    
    def add_node(
        self, 
        name: str, 
        weight: int = 1,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """Add a node to all hash rings."""
        with self._lock:
            if name in self._nodes:
                raise ValueError(f"Node {name!r} already exists")
            
            self._nodes[name] = Node(name=name, weight=weight, metadata=metadata or {})
            
            for ring in self._rings:
                ring.add_node(name, weight, metadata)
    
    def remove_node(self, name: str) -> None:
        """Remove a node from all hash rings."""
        with self._lock:
            if name not in self._nodes:
                raise KeyError(f"Node {name!r} not found")
            
            del self._nodes[name]
            
            for ring in self._rings:
                ring.remove_node(name)
    
    def get_primary_node(self, key: str) -> Optional[str]:
        """Get the primary node for a key."""
        with self._lock:
            if not self._rings:
                return None
            return self._rings[0].get_node(key)
    
    def get_replica_nodes(self, key: str) -> List[str]:
        """
        Get replica nodes for a key.
        
        Returns distinct nodes across all hash rings.
        Will try multiple nodes from each ring to find distinct replicas.
        """
        with self._lock:
            result: List[str] = []
            seen: Set[str] = set()
            
            # Try to get up to num_replicas distinct nodes
            for ring in self._rings:
                # Get multiple candidates from this ring
                candidates = ring.get_nodes(key, count=min(self._num_replicas, len(self._nodes)))
                for node in candidates:
                    if node and node not in seen:
                        seen.add(node)
                        result.append(node)
                        if len(result) >= self._num_replicas:
                            return result
            
            return result
    
    def get_nodes_with_fallback(
        self, 
        key: str, 
        unavailable: Optional[Set[str]] = None,
        count: int = 1
    ) -> List[str]:
        """
        Get nodes for a key, skipping unavailable ones.
        
        Args:
            key: Key to look up
            unavailable: Set of node names to skip
            count: Number of available nodes to return
            
        Returns:
            List of available node names
        """
        unavailable = unavailable or set()
        
        with self._lock:
            result: List[str] = []
            seen: Set[str] = set()
            
            # Try each ring in order
            for ring in self._rings:
                nodes = ring.get_nodes(key, count=len(self._nodes))
                for node in nodes:
                    if node not in seen and node not in unavailable:
                        seen.add(node)
                        result.append(node)
                        if len(result) >= count:
                            return result
            
            return result
    
    def clear(self) -> None:
        """Remove all nodes."""
        with self._lock:
            for ring in self._rings:
                ring.clear()
            self._nodes.clear()
    
    def __contains__(self, name: str) -> bool:
        return name in self._nodes
    
    def __len__(self) -> int:
        return len(self._nodes)


# Convenience functions

def create_ring(
    nodes: List[str],
    virtual_nodes: int = 150,
    hash_algorithm: str = 'md5'
) -> ConsistentHash:
    """
    Create a consistent hash ring with the given nodes.
    
    Args:
        nodes: List of node names
        virtual_nodes: Virtual nodes per physical node
        hash_algorithm: Hash algorithm to use
        
    Returns:
        Configured ConsistentHash instance
    """
    ring = ConsistentHash(
        virtual_nodes=virtual_nodes,
        hash_algorithm=hash_algorithm
    )
    
    for node in nodes:
        ring.add_node(node)
    
    return ring


def distribute_keys(
    keys: List[str],
    nodes: List[str],
    virtual_nodes: int = 150
) -> Dict[str, List[str]]:
    """
    Distribute keys evenly across nodes.
    
    Args:
        keys: Keys to distribute
        nodes: Available nodes
        virtual_nodes: Virtual nodes per physical node
        
    Returns:
        Dictionary mapping node names to their assigned keys
    """
    ring = create_ring(nodes, virtual_nodes)
    distribution: Dict[str, List[str]] = defaultdict(list)
    
    for key in keys:
        node = ring.get_node(key)
        if node:
            distribution[node].append(key)
    
    return dict(distribution)


def analyze_distribution(
    keys: List[str],
    nodes: List[str],
    virtual_nodes: int = 150
) -> Dict[str, Any]:
    """
    Analyze key distribution across nodes.
    
    Args:
        keys: Keys to analyze
        nodes: Available nodes
        virtual_nodes: Virtual nodes per physical node
        
    Returns:
        Distribution analysis including stats and imbalance metrics
    """
    distribution = distribute_keys(keys, nodes, virtual_nodes)
    
    counts = [len(keys) for keys in distribution.values()]
    total_keys = len(keys)
    num_nodes = len(nodes)
    
    if not counts:
        return {
            'total_keys': total_keys,
            'num_nodes': num_nodes,
            'distribution': {},
            'stats': {
                'min': 0,
                'max': 0,
                'mean': 0,
                'std_dev': 0,
            },
            'imbalance_ratio': 0,
        }
    
    mean = sum(counts) / len(counts) if counts else 0
    variance = sum((c - mean) ** 2 for c in counts) / len(counts) if counts else 0
    std_dev = variance ** 0.5
    
    min_count = min(counts) if counts else 0
    max_count = max(counts) if counts else 0
    imbalance = max_count / min_count if min_count > 0 else float('inf')
    
    return {
        'total_keys': total_keys,
        'num_nodes': num_nodes,
        'distribution': {k: len(v) for k, v in distribution.items()},
        'stats': {
            'min': min_count,
            'max': max_count,
            'mean': mean,
            'std_dev': std_dev,
        },
        'imbalance_ratio': imbalance,
    }