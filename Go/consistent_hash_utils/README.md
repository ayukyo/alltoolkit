# Consistent Hash Utilities

A Go implementation of consistent hashing for distributed systems, featuring virtual nodes, weighted distribution, and multiple hash functions.

## Features

- **Consistent Hashing**: Minimally disruptive rebalancing when nodes change
- **Virtual Nodes**: Better key distribution across nodes
- **Weighted Nodes**: Proportional distribution based on node capacity
- **Multiple Hash Functions**: CRC32, MD5, SHA256
- **Replication Support**: Get N nodes for any key
- **Node States**: Active, Draining, Offline
- **Migration Planning**: Calculate keys to migrate when adding nodes
- **Distribution Analysis**: Analyze key distribution balance
- **Thread-Safe**: Safe for concurrent access

## Installation

```go
import "github.com/ayukyo/alltoolkit/Go/consistent_hash_utils"
```

## Quick Start

```go
package main

import (
    "fmt"
    consistenthash "github.com/ayukyo/alltoolkit/Go/consistent_hash_utils"
)

func main() {
    // Create a hash ring
    ring := consistenthash.NewRingWithDefaults()
    
    // Add nodes (servers)
    ring.AddNode("server1", "192.168.1.1:8080", 1)
    ring.AddNode("server2", "192.168.1.2:8080", 2)  // Higher weight
    ring.AddNode("server3", "192.168.1.3:8080", 1)
    
    // Get the node responsible for a key
    node, err := ring.Get("user:12345")
    if err != nil {
        panic(err)
    }
    fmt.Printf("Key 'user:12345' maps to %s (%s)\n", node.ID, node.Address)
    
    // Get replication targets (for redundancy)
    replicas, err := ring.GetReplicas("user:12345")
    for _, node := range replicas {
        fmt.Printf("Replica on: %s\n", node.ID)
    }
}
```

## Core Concepts

### Consistent Hashing

Consistent hashing maps keys to nodes using a hash ring. When nodes are added or removed, only a fraction of keys need to be remapped, minimizing disruption.

### Virtual Nodes

Each physical node is represented by multiple virtual nodes on the ring, providing:
- Better distribution of keys
- Smaller impact when nodes change
- Support for weighted distribution

### Weighted Distribution

Nodes can have different weights based on capacity:

```go
// Small server - gets ~14% of keys
ring.AddNode("small", "addr1", 1)

// Medium server - gets ~28% of keys  
ring.AddNode("medium", "addr2", 2)

// Large server - gets ~57% of keys
ring.AddNode("large", "addr3", 4)
```

## Usage Examples

### Basic Hash Ring

```go
ring := consistenthash.NewRingWithDefaults()
ring.AddNode("cache1", "10.0.0.1:6379", 1)
ring.AddNode("cache2", "10.0.0.2:6379", 1)
ring.AddNode("cache3", "10.0.0.3:6379", 1)

// Always returns same node for same key
node, _ := ring.Get("session:abc123")
```

### Custom Configuration

```go
config := consistenthash.Config{
    DefaultVirtualNodes: 200,    // More virtual nodes = better distribution
    HashFunction:         consistenthash.HashMD5,  // Use MD5 hashing
    ReplicationFactor:   3,      // 3 replicas per key
    HashRingName:        "my-cache-ring",
}
ring := consistenthash.NewRing(config)
```

### Node States

```go
// Gracefully drain a node (existing keys remain, no new keys)
ring.SetNodeState("server1", consistenthash.NodeStateDraining)

// Take a node offline (removed from ring)
ring.SetNodeState("server2", consistenthash.NodeStateOffline)

// Bring a node back online
ring.SetNodeState("server2", consistenthash.NodeStateActive)
```

### Distribution Analysis

```go
keys := consistenthash.GenerateKeys(10000)
stats := ring.AnalyzeDistribution(keys)

fmt.Printf("Balance score: %.2f\n", stats.BalanceScore)
fmt.Printf("Keys per node: %d - %d\n", stats.MinKeys, stats.MaxKeys)

for nodeID, count := range stats.NodeDistributions {
    fmt.Printf("%s: %d keys\n", nodeID, count)
}
```

### Migration Planning

```go
// Add a new node
ring.AddNode("server4", "192.168.1.4:8080", 1)

// Calculate which keys need to move to the new node
keys := []string{"user:1", "user:2", "user:3", "user:4"}
plan := ring.GetMigrationPlan(keys, "server4")

for _, migration := range plan {
    fmt.Printf("Move %d keys from %s to %s\n",
        len(migration.Keys), migration.FromNode, migration.ToNode)
}
```

### Statistics

```go
stats := ring.GetStats()
fmt.Printf("Nodes: %d (Active: %d, Draining: %d, Offline: %d)\n",
    stats.NodeCount, stats.ActiveNodes, stats.DrainingNodes, stats.OfflineNodes)
fmt.Printf("Virtual nodes: %d\n", stats.VirtualNodeCount)
fmt.Printf("Hash function: %s\n", stats.HashFunction)
```

## Thread Safety

All operations are thread-safe. The ring uses read-write locks for optimal concurrency:

```go
// Multiple goroutines can safely access the ring
for i := 0; i < 10; i++ {
    go func(id int) {
        for j := 0; j < 1000; j++ {
            node, _ := ring.Get(fmt.Sprintf("key-%d-%d", id, j))
            // Use node...
        }
    }(i)
}
```

## Hash Functions

| Function | Speed | Distribution | Use Case |
|----------|-------|--------------|----------|
| CRC32    | Fast  | Good         | General use |
| MD5      | Medium | Excellent   | Better distribution |
| SHA256   | Slow  | Excellent    | Security-sensitive |

## API Reference

### Ring Methods

- `NewRing(config Config) *Ring` - Create ring with custom config
- `NewRingWithDefaults() *Ring` - Create ring with defaults
- `AddNode(id, address string, weight int) *Node` - Add a node
- `AddNodeWithMetadata(id, address string, weight int, metadata map) *Node` - Add node with metadata
- `RemoveNode(id string) bool` - Remove a node
- `GetNode(id string) (*Node, bool)` - Get node by ID
- `GetNodes() []*Node` - Get all nodes
- `Get(key string) (*Node, error)` - Get node for key
- `GetN(key string, n int) ([]*Node, error)` - Get N nodes for key
- `GetReplicas(key string) ([]*Node, error)` - Get replica nodes
- `SetNodeState(id string, state NodeState) bool` - Change node state
- `SetNodeWeight(id string, weight int) bool` - Change node weight
- `NodeCount() int` - Get node count
- `AnalyzeDistribution(keys []string) *DistributionStats` - Analyze distribution
- `GetMigrationPlan(keys []string, newNodeID string) []MigrationPlan` - Get migration plan
- `GetStats() Stats` - Get ring statistics
- `String() string` - String representation

### Config Fields

- `DefaultVirtualNodes int` - Virtual nodes per physical node (default: 150)
- `HashFunction HashFunction` - Hash function to use
- `ReplicationFactor int` - Number of replicas (default: 3)
- `HashRingName string` - Optional ring name

## Common Use Cases

### Distributed Cache

```go
ring := consistenthash.NewRingWithDefaults()
for _, server := range redisServers {
    ring.AddNode(server.ID, server.Addr, server.Capacity)
}

// Route cache requests
node, _ := ring.Get(cacheKey)
conn := redis.Connect(node.Address)
```

### Load Balancing

```go
ring := consistenthash.NewRingWithDefaults()
for _, backend := range backends {
    ring.AddNode(backend.ID, backend.Addr, backend.Weight)
}

// Session affinity: same user -> same backend
node, _ := ring.Get(sessionID)
```

### Database Sharding

```go
ring := consistenthash.NewRingWithDefaults()
for _, shard := range shards {
    ring.AddNode(shard.ID, shard.ConnStr, shard.Capacity)
}

// Shard by user ID
node, _ := ring.Get(fmt.Sprintf("user:%d", userID))
db := connect(node.Address)
```

## License

MIT License - Part of AllToolkit