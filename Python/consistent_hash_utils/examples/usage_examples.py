"""
AllToolkit - Consistent Hash Utilities Usage Examples

Examples demonstrating various consistent hashing use cases:
1. Distributed caching (Redis/Memcached cluster)
2. Load balancing
3. Data sharding
4. High availability with replicas
"""

from consistent_hash_utils.mod import (
    ConsistentHash,
    WeightedConsistentHash,
    RendezvousHash,
    JumpConsistentHash,
    MultiHash,
    create_ring,
    distribute_keys,
    analyze_distribution,
)


def example_distributed_cache():
    """
    Example: Distributed cache cluster with consistent hashing.
    
    Simulates a Redis cluster with multiple nodes, showing how keys
    are distributed and how to handle node addition/removal.
    """
    print("=" * 60)
    print("Example 1: Distributed Cache Cluster")
    print("=" * 60)
    
    # Create a cache cluster with 5 nodes
    cache_nodes = [
        ("redis-1", {"host": "192.168.1.1", "port": 6379}),
        ("redis-2", {"host": "192.168.1.2", "port": 6379}),
        ("redis-3", {"host": "192.168.1.3", "port": 6379}),
        ("redis-4", {"host": "192.168.1.4", "port": 6379}),
        ("redis-5", {"host": "192.168.1.5", "port": 6379}),
    ]
    
    ring = ConsistentHash(virtual_nodes=150)
    
    for name, metadata in cache_nodes:
        ring.add_node(name, metadata=metadata)
    
    # Distribute some cache keys
    cache_keys = [
        "user:123:profile",
        "user:456:profile",
        "session:abc123",
        "product:789",
        "cart:session:abc123",
        "config:app_settings",
        "rate_limit:user:123",
    ]
    
    print("\nCache key assignments:")
    for key in cache_keys:
        node = ring.get_node(key)
        metadata = ring.get_node_metadata(node)
        print(f"  {key} -> {node} ({metadata['host']})")
    
    # Analyze distribution with more keys
    all_keys = [f"cache:{i}" for i in range(1000)]
    distribution = ring.get_key_distribution(all_keys)
    
    print("\nKey distribution (1000 keys):")
    for node, count in sorted(distribution.items()):
        print(f"  {node}: {count} keys ({count/10:.1f}%)")
    
    # Simulate adding a new node
    print("\n--- Adding new node redis-6 ---")
    migrations = ring.calculate_migration(all_keys, ["redis-6"], [])
    ring.add_node("redis-6", metadata={"host": "192.168.1.6", "port": 6379})
    
    migrated_keys = [m.key for m in migrations]
    print(f"Keys to migrate: {len(migrated_keys)}")
    print(f"Migration ratio: {len(migrated_keys)/len(all_keys)*100:.1f}%")
    
    # Show sample migrations
    print("\nSample migrations:")
    for m in migrations[:5]:
        print(f"  {m}")
    
    # Simulate removing a node
    print("\n--- Removing node redis-3 ---")
    ring.remove_node("redis-3")
    
    new_distribution = ring.get_key_distribution(all_keys)
    print("New distribution:")
    for node, count in sorted(new_distribution.items()):
        print(f"  {node}: {count} keys")


def example_weighted_cluster():
    """
    Example: Heterogeneous cluster with weighted nodes.
    
    Shows how to handle nodes with different capacities by assigning
    weights proportional to their capacity.
    """
    print("\n" + "=" * 60)
    print("Example 2: Weighted Cluster (Heterogeneous Nodes)")
    print("=" * 60)
    
    ring = WeightedConsistentHash(virtual_nodes=100)
    
    # Add nodes with weights proportional to capacity
    # Small VM: 2GB RAM -> weight 2
    # Medium VM: 4GB RAM -> weight 4
    # Large VM: 8GB RAM -> weight 8
    ring.add_node("small-vm", weight=1, metadata={"capacity": "2GB", "cpu": 1})
    ring.add_node("medium-vm", weight=2, metadata={"capacity": "4GB", "cpu": 2})
    ring.add_node("large-vm", weight=4, metadata={"capacity": "8GB", "cpu": 4})
    
    print("\nNode weights:")
    for node in ring.nodes:
        weight = ring.get_node_weight(node)
        metadata = ring.get_node_metadata(node)
        print(f"  {node}: weight={weight}, capacity={metadata['capacity']}")
    
    # Expected distribution percentages
    expected = ring.get_weight_distribution()
    print("\nExpected distribution:")
    for node, pct in expected.items():
        print(f"  {node}: {pct*100:.1f}%")
    
    # Actual distribution
    keys = [f"key:{i}" for i in range(1000)]
    distribution = ring.get_key_distribution(keys)
    
    print("\nActual distribution (1000 keys):")
    for node, count in sorted(distribution.items()):
        actual_pct = count / len(keys)
        expected_pct = expected[node]
        print(f"  {node}: {count} keys ({actual_pct*100:.1f}%), expected {expected_pct*100:.1f}%")


def example_load_balancing():
    """
    Example: Load balancing using rendezvous hashing.
    
    Shows how to use HRW (Highest Random Weight) hashing for
    load balancing HTTP requests across servers.
    """
    print("\n" + "=" * 60)
    print("Example 3: Load Balancing with Rendezvous Hashing")
    print("=" * 60)
    
    rh = RendezvousHash()
    
    # Add load balancer backends
    backends = [
        ("web-1", {"ip": "10.0.0.1", "port": 8080}),
        ("web-2", {"ip": "10.0.0.2", "port": 8080}),
        ("web-3", {"ip": "10.0.0.3", "port": 8080}),
    ]
    
    for name, metadata in backends:
        rh.add_node(name, metadata=metadata)
    
    # Route requests based on user ID
    user_ids = ["user123", "user456", "user789", "admin", "guest"]
    
    print("\nRequest routing:")
    for user_id in user_ids:
        backend = rh.get_node(user_id)
        metadata = rh.get_node_metadata(backend)
        print(f"  {user_id} -> {backend} ({metadata['ip']}:{metadata['port']})")
    
    # Consistency check
    print("\nConsistency verification:")
    for _ in range(5):
        for user_id in user_ids[:3]:
            backend = rh.get_node(user_id)
            print(f"  {user_id} -> {backend}")
        print("  (Same mappings on repeated calls)")
    
    # Weighted load balancing
    print("\n--- Weighted load balancing ---")
    rh_weighted = RendezvousHash()
    rh_weighted.add_node("strong-server", weight=3, metadata={"capacity": "high"})
    rh_weighted.add_node("weak-server", weight=1, metadata={"capacity": "low"})
    
    requests = [f"req:{i}" for i in range(100)]
    distribution = {}
    for req in requests:
        server = rh_weighted.get_node(req)
        distribution[server] = distribution.get(server, 0) + 1
    
    print("\nRequest distribution:")
    for server, count in sorted(distribution.items()):
        print(f"  {server}: {count} requests")


def example_jump_consistent_hash():
    """
    Example: Jump consistent hash for memory-efficient sharding.
    
    Shows how to use jump consistent hash for data sharding
    with minimal memory overhead.
    """
    print("\n" + "=" * 60)
    print("Example 4: Jump Consistent Hash (Memory Efficient)")
    print("=" * 60)
    
    # Create 10 shards
    jh = JumpConsistentHash(num_buckets=10)
    
    # Shard user data
    users = ["user1", "user2", "user3", "user4", "user5"]
    
    print("\nUser shard assignments:")
    for user in users:
        shard = jh.get_bucket(user)
        print(f"  {user} -> shard-{shard}")
    
    # Analyze distribution
    all_users = [f"user:{i}" for i in range(10000)]
    distribution = jh.get_distribution(all_users)
    
    print("\nShard distribution (10000 users):")
    for shard, count in sorted(distribution.items()):
        print(f"  shard-{shard}: {count} users")
    
    # Resize shards
    print("\n--- Expanding to 20 shards ---")
    jh.resize(20)
    
    new_distribution = jh.get_distribution(all_users)
    print("New shard distribution:")
    for shard, count in sorted(new_distribution.items())[:10]:
        print(f"  shard-{shard}: {count} users")


def example_high_availability():
    """
    Example: High availability with multi-hash and replicas.
    
    Shows how to use multiple hash rings for primary/backup
    node assignment.
    """
    print("\n" + "=" * 60)
    print("Example 5: High Availability with MultiHash")
    print("=" * 60)
    
    mh = MultiHash(num_replicas=3)
    
    # Add storage nodes
    nodes = [
        ("storage-1", {"zone": "us-east-1a"}),
        ("storage-2", {"zone": "us-east-1b"}),
        ("storage-3", {"zone": "us-west-1a"}),
        ("storage-4", {"zone": "us-west-1b"}),
        ("storage-5", {"zone": "eu-west-1a"}),
    ]
    
    for name, metadata in nodes:
        mh.add_node(name, metadata=metadata)
    
    # Get primary and replicas for data
    data_keys = ["data:file1", "data:file2", "data:file3"]
    
    print("\nData replication:")
    for key in data_keys:
        primary = mh.get_primary_node(key)
        replicas = mh.get_replica_nodes(key)
        print(f"  {key}:")
        print(f"    Primary: {primary}")
        print(f"    Replicas: {replicas}")
    
    # Handle node failure
    print("\n--- storage-1 is down ---")
    unavailable = {"storage-1"}
    
    for key in data_keys:
        nodes = mh.get_nodes_with_fallback(key, unavailable=unavailable, count=2)
        print(f"  {key} -> available nodes: {nodes}")
    
    # Simulate zone failure
    print("\n--- us-east zone is down ---")
    east_nodes = {"storage-1", "storage-2"}
    
    for key in data_keys:
        nodes = mh.get_nodes_with_fallback(key, unavailable=east_nodes, count=2)
        print(f"  {key} -> west/eu nodes: {nodes}")


def example_data_migration():
    """
    Example: Planning data migration when scaling cluster.
    
    Shows how to calculate which keys need to migrate when
    adding or removing nodes.
    """
    print("\n" + "=" * 60)
    print("Example 6: Data Migration Planning")
    print("=" * 60)
    
    # Initial cluster
    ring = ConsistentHash()
    ring.add_node("server-1")
    ring.add_node("server-2")
    ring.add_node("server-3")
    
    # Existing keys
    existing_keys = [f"record:{i}" for i in range(10000)]
    
    print(f"Initial cluster: {ring.nodes}")
    
    # Migration when adding 2 new servers
    print("\n--- Scaling: Adding server-4 and server-5 ---")
    migrations = ring.calculate_migration(
        existing_keys,
        new_nodes=["server-4", "server-5"],
        removed_nodes=[]
    )
    
    # Add the new servers
    ring.add_node("server-4")
    ring.add_node("server-5")
    
    print(f"Total keys to migrate: {len(migrations)}")
    print(f"Migration percentage: {len(migrations)/len(existing_keys)*100:.1f}%")
    
    # Breakdown by destination
    dest_counts = {}
    for m in migrations:
        dest_counts[m.target_node] = dest_counts.get(m.target_node, 0) + 1
    
    print("\nKeys moving to new servers:")
    for node, count in sorted(dest_counts.items()):
        if node in ["server-4", "server-5"]:
            print(f"  {node}: {count} keys")
    
    # Migration when removing a server
    print("\n--- Downsizing: Removing server-3 ---")
    migrations = ring.calculate_migration(
        existing_keys,
        new_nodes=[],
        removed_nodes=["server-3"]
    )
    
    print(f"Total keys to migrate: {len(migrations)}")
    
    dest_counts = {}
    for m in migrations:
        dest_counts[m.target_node] = dest_counts.get(m.target_node, 0) + 1
    
    print("\nKeys redistributed from server-3:")
    for node, count in sorted(dest_counts.items()):
        print(f"  {node}: {count} keys")


def example_analyze_distribution():
    """
    Example: Analyzing key distribution quality.
    
    Shows how to use the analysis functions to check
    distribution quality and imbalance.
    """
    print("\n" + "=" * 60)
    print("Example 7: Distribution Analysis")
    print("=" * 60)
    
    keys = [f"key:{i}" for i in range(10000)]
    nodes = ["node1", "node2", "node3", "node4", "node5"]
    
    # Analyze with different virtual node counts
    for vn in [10, 50, 100, 150]:
        analysis = analyze_distribution(keys, nodes, virtual_nodes=vn)
        
        stats = analysis["stats"]
        print(f"\nVirtual nodes per node: {vn}")
        print(f"  Min keys: {stats['min']}")
        print(f"  Max keys: {stats['max']}")
        print(f"  Mean: {stats['mean']:.1f}")
        print(f"  Std dev: {stats['std_dev']:.1f}")
        print(f"  Imbalance ratio: {analysis['imbalance_ratio']:.2f}")


def main():
    """Run all examples."""
    example_distributed_cache()
    example_weighted_cluster()
    example_load_balancing()
    example_jump_consistent_hash()
    example_high_availability()
    example_data_migration()
    example_analyze_distribution()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()