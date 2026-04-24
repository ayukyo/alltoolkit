# Consistent Hash

A high-performance consistent hashing implementation in Rust with zero external dependencies.

## Features

- **Zero Dependencies**: Pure Rust implementation with no external crates
- **Virtual Nodes**: Better distribution with configurable virtual nodes per physical node
- **Minimal Rebalancing**: Only ~1/N keys move when adding/removing nodes
- **Weighted Nodes**: Support for nodes with different capacities
- **Thread-Safe**: `Arc<RwLock>` based thread-safe operations
- **Replication Support**: Get N nodes for a key (useful for data replication)
- **MurmurHash3**: High-quality hash distribution using MurmurHash3-like algorithm

## Installation

Add to your `Cargo.toml`:

```toml
[dependencies]
consistent_hash = { path = "./consistent_hash" }
```

## Quick Start

```rust
use consistent_hash::ConsistentHash;

fn main() {
    // Create a hash ring
    let mut ring = ConsistentHash::<&str>::new();
    
    // Add nodes with virtual nodes for better distribution
    ring.add_node("server1", 150);
    ring.add_node("server2", 150);
    ring.add_node("server3", 150);
    
    // Route a key to a node
    let node = ring.get("user:12345").unwrap();
    println!("Key maps to: {}", node);
    
    // Get multiple nodes for replication
    let replicas = ring.get_n("user:12345", 2);
    println!("Replica nodes: {:?}", replicas);
}
```

## Usage

### Basic Operations

```rust
use consistent_hash::ConsistentHash;

let mut ring = ConsistentHash::new();

// Add nodes
ring.add("server1");                      // Default 150 virtual nodes
ring.add_node("server2", 200);            // Custom virtual nodes

// Remove nodes
ring.remove(&"server1");

// Get node for key
let node = ring.get("some-key");

// Check membership
if ring.contains(&"server2") {
    println!("Server2 is in the ring");
}

// Get ring statistics
let stats = ring.stats();
println!("Nodes: {}, Virtual nodes: {}", stats.node_count, stats.virtual_node_count);
```

### Weighted Nodes

Nodes with different capacities can be weighted:

```rust
let mut ring = ConsistentHash::new();

// Server with 3x capacity gets 3x more virtual nodes
ring.add_weighted("powerful-server", 3.0);
ring.add_weighted("normal-server", 1.0);
ring.add_weighted("small-server", 0.5);
```

### Replication

Get multiple nodes for data replication:

```rust
let mut ring = ConsistentHash::new();
ring.add("primary");
ring.add("replica1");
ring.add("replica2");

// Get 2 nodes for replication
let nodes = ring.get_n("user:123", 2);
// Returns primary node and first replica
```

### Custom Configuration

```rust
use consistent_hash::{ConsistentHash, RingConfig};

let config = RingConfig {
    virtual_nodes: 200,
    weighted: true,
};

let mut ring = ConsistentHash::with_config(config);
```

## Algorithm

Consistent hashing maps both nodes and keys to a circular hash space (ring). 

1. **Node Placement**: Each physical node is hashed to multiple positions on the ring via virtual nodes
2. **Key Routing**: Keys are hashed and assigned to the nearest node clockwise on the ring
3. **Minimal Rebalancing**: When a node is added/removed, only keys that map to that node's region are affected

### Why Virtual Nodes?

Without virtual nodes, uneven distribution can occur. With 150+ virtual nodes per physical node, the key distribution becomes statistically uniform.

## Thread Safety

The implementation uses `Arc<RwLock>` internally, allowing safe concurrent access:

```rust
use std::sync::Arc;
use std::thread;

let ring = Arc::new(ConsistentHash::<&str>::new());
// Add nodes...

let handles: Vec<_> = (0..4)
    .map(|_| {
        let ring = Arc::clone(&ring);
        thread::spawn(move || {
            ring.get("key")  // Safe concurrent access
        })
    })
    .collect();
```

## Performance

- **Insert**: O(V log V) where V = virtual nodes
- **Lookup**: O(log V) 
- **Memory**: O(V)

Typical performance with 150 virtual nodes per server:
- 3 nodes, 450 virtual nodes: ~100ns lookup
- 100 nodes, 15000 virtual nodes: ~150ns lookup

## Use Cases

- **Load Balancing**: Distribute requests across servers
- **Distributed Caching**: Memcached/Redis cluster sharding
- **Database Sharding**: Route users to database shards
- **CDN**: Route content to edge servers
- **Distributed Storage**: Consistent data placement

## API Reference

### `ConsistentHash<T>`

| Method | Description |
|--------|-------------|
| `new()` | Create ring with defaults (150 virtual nodes) |
| `with_virtual_nodes(n)` | Create with custom virtual nodes |
| `add(identifier)` | Add node with default virtual nodes |
| `add_node(id, vnodes)` | Add node with custom virtual nodes |
| `add_weighted(id, weight)` | Add node with weight factor |
| `remove(identifier)` | Remove a node, returns true if existed |
| `get(key)` | Get node for string key |
| `get_by_key(key)` | Get node for hashable key |
| `get_n(key, n)` | Get N nodes for replication |
| `contains(id)` | Check if node exists |
| `clear()` | Remove all nodes |
| `nodes()` | Get all node identifiers |
| `node_count()` | Number of physical nodes |
| `virtual_node_count()` | Number of virtual nodes |
| `stats()` | Get ring statistics |
| `distribution_balance(keys)` | Measure key distribution balance |

## License

MIT