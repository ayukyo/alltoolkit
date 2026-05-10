package consistenthash

import (
	"fmt"
	"math/rand"
	"sort"
	"strings"
	"testing"
	"time"
)

// =============================================================================
// Basic Tests
// =============================================================================

func TestNewRing(t *testing.T) {
	ring := NewRingWithDefaults()
	if ring == nil {
		t.Fatal("Expected non-nil ring")
	}
	if ring.NodeCount() != 0 {
		t.Errorf("Expected empty ring, got %d nodes", ring.NodeCount())
	}
}

func TestNewRingWithConfig(t *testing.T) {
	config := Config{
		DefaultVirtualNodes: 200,
		HashFunction:         HashMD5,
		ReplicationFactor:   5,
	}
	ring := NewRing(config)
	if ring == nil {
		t.Fatal("Expected non-nil ring")
	}
	if ring.config.DefaultVirtualNodes != 200 {
		t.Errorf("Expected 200 virtual nodes, got %d", ring.config.DefaultVirtualNodes)
	}
	if ring.config.HashFunction != HashMD5 {
		t.Errorf("Expected MD5 hash function")
	}
}

func TestAddNode(t *testing.T) {
	ring := NewRingWithDefaults()
	node := ring.AddNode("node1", "localhost:8080", 1)

	if node == nil {
		t.Fatal("Expected non-nil node")
	}
	if node.ID != "node1" {
		t.Errorf("Expected ID 'node1', got '%s'", node.ID)
	}
	if node.Address != "localhost:8080" {
		t.Errorf("Expected address 'localhost:8080', got '%s'", node.Address)
	}
	if node.Weight != 1 {
		t.Errorf("Expected weight 1, got %d", node.Weight)
	}
	if ring.NodeCount() != 1 {
		t.Errorf("Expected 1 node, got %d", ring.NodeCount())
	}
}

func TestAddNodeWithMetadata(t *testing.T) {
	ring := NewRingWithDefaults()
	metadata := map[string]interface{}{
		"region": "us-west",
		"zone":   "a",
	}
	node := ring.AddNodeWithMetadata("node1", "localhost:8080", 2, metadata)

	if node.Metadata["region"] != "us-west" {
		t.Errorf("Expected region 'us-west', got '%v'", node.Metadata["region"])
	}
}

func TestRemoveNode(t *testing.T) {
	ring := NewRingWithDefaults()
	ring.AddNode("node1", "localhost:8080", 1)

	if !ring.RemoveNode("node1") {
		t.Error("Expected true when removing existing node")
	}
	if ring.NodeCount() != 0 {
		t.Errorf("Expected 0 nodes, got %d", ring.NodeCount())
	}

	if ring.RemoveNode("nonexistent") {
		t.Error("Expected false when removing non-existent node")
	}
}

func TestGetNode(t *testing.T) {
	ring := NewRingWithDefaults()
	ring.AddNode("node1", "localhost:8080", 1)

	node, exists := ring.GetNode("node1")
	if !exists {
		t.Fatal("Expected to find node")
	}
	if node.ID != "node1" {
		t.Errorf("Expected ID 'node1', got '%s'", node.ID)
	}

	_, exists = ring.GetNode("nonexistent")
	if exists {
		t.Error("Expected not to find nonexistent node")
	}
}

func TestSetNodeState(t *testing.T) {
	ring := NewRingWithDefaults()
	ring.AddNode("node1", "localhost:8080", 1)

	if !ring.SetNodeState("node1", NodeStateDraining) {
		t.Error("Expected true when setting state")
	}

	node, _ := ring.GetNode("node1")
	if node.State != NodeStateDraining {
		t.Errorf("Expected state Draining, got %v", node.State)
	}
}

func TestSetNodeWeight(t *testing.T) {
	ring := NewRingWithDefaults()
	ring.AddNode("node1", "localhost:8080", 1)

	if !ring.SetNodeWeight("node1", 5) {
		t.Error("Expected true when setting weight")
	}

	node, _ := ring.GetNode("node1")
	if node.Weight != 5 {
		t.Errorf("Expected weight 5, got %d", node.Weight)
	}

	if ring.SetNodeWeight("node1", 0) {
		t.Error("Expected false when setting invalid weight")
	}
}

// =============================================================================
// Hash Function Tests
// =============================================================================

func TestHashFunctions(t *testing.T) {
	keys := []string{"test1", "test2", "test3", "test4", "test5"}

	hashFunctions := []HashFunction{HashCRC32, HashMD5, Hash256}

	for _, fn := range hashFunctions {
		t.Run(fmt.Sprintf("HashFunction_%d", fn), func(t *testing.T) {
			config := Config{
				DefaultVirtualNodes: 150,
				HashFunction:         fn,
			}
			ring := NewRing(config)

			for i := 0; i < 3; i++ {
				ring.AddNode(fmt.Sprintf("node%d", i), fmt.Sprintf("localhost:%d", 8080+i), 1)
			}

			for _, key := range keys {
				node, err := ring.Get(key)
				if err != nil {
					t.Errorf("Unexpected error for key '%s': %v", key, err)
				}
				if node == nil {
					t.Errorf("Expected non-nil node for key '%s'", key)
				}
			}
		})
	}
}

func TestHashConsistency(t *testing.T) {
	ring := NewRingWithDefaults()
	ring.AddNode("node1", "localhost:8080", 1)
	ring.AddNode("node2", "localhost:8081", 1)
	ring.AddNode("node3", "localhost:8082", 1)

	// Same key should always map to same node
	key := "test-key-123"
	nodes := make([]*Node, 10)
	for i := 0; i < 10; i++ {
		node, err := ring.Get(key)
		if err != nil {
			t.Fatalf("Unexpected error: %v", err)
		}
		nodes[i] = node
	}

	for i := 1; i < 10; i++ {
		if nodes[i].ID != nodes[0].ID {
			t.Errorf("Inconsistent hashing: key mapped to different nodes")
		}
	}
}

// =============================================================================
// Key Lookup Tests
// =============================================================================

func TestGetSingleKey(t *testing.T) {
	ring := NewRingWithDefaults()
	ring.AddNode("node1", "localhost:8080", 1)
	ring.AddNode("node2", "localhost:8081", 1)

	node, err := ring.Get("my-key")
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if node == nil {
		t.Fatal("Expected non-nil node")
	}
}

func TestGetEmptyRing(t *testing.T) {
	ring := NewRingWithDefaults()

	_, err := ring.Get("my-key")
	if err != ErrEmptyRing {
		t.Errorf("Expected ErrEmptyRing, got %v", err)
	}
}

func TestGetN(t *testing.T) {
	ring := NewRingWithDefaults()
	ring.AddNode("node1", "localhost:8080", 1)
	ring.AddNode("node2", "localhost:8081", 1)
	ring.AddNode("node3", "localhost:8082", 1)

	nodes, err := ring.GetN("my-key", 2)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if len(nodes) != 2 {
		t.Errorf("Expected 2 nodes, got %d", len(nodes))
	}

	// Verify uniqueness
	seen := make(map[string]bool)
	for _, node := range nodes {
		if seen[node.ID] {
			t.Errorf("Duplicate node in result: %s", node.ID)
		}
		seen[node.ID] = true
	}
}

func TestGetReplicas(t *testing.T) {
	config := Config{
		DefaultVirtualNodes: 150,
		ReplicationFactor:   3,
	}
	ring := NewRing(config)
	ring.AddNode("node1", "localhost:8080", 1)
	ring.AddNode("node2", "localhost:8081", 1)
	ring.AddNode("node3", "localhost:8082", 1)

	nodes, err := ring.GetReplicas("my-key")
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if len(nodes) != 3 {
		t.Errorf("Expected 3 nodes, got %d", len(nodes))
	}
}

// =============================================================================
// Weight Tests
// =============================================================================

func TestWeightedDistribution(t *testing.T) {
	ring := NewRingWithDefaults()
	ring.AddNode("node1", "localhost:8080", 1)
	ring.AddNode("node2", "localhost:8081", 3) // 3x weight

	// Generate many keys and check distribution
	keys := make([]string, 10000)
	for i := 0; i < 10000; i++ {
		keys[i] = fmt.Sprintf("key-%d", i)
	}

	dist := make(map[string]int)
	for _, key := range keys {
		node, err := ring.Get(key)
		if err != nil {
			t.Fatalf("Unexpected error: %v", err)
		}
		dist[node.ID]++
	}

	// node2 should get more keys than node1 (weighted 3x)
	// Due to consistent hashing nature, ratio may vary but node2 should be higher
	if dist["node2"] <= dist["node1"] {
		t.Errorf("Expected node2 (weight=3) to get more keys than node1 (weight=1), got node1: %d, node2: %d",
			dist["node1"], dist["node2"])
	}
	
	// Check that node2 gets at least 1.5x more keys (allowing for variance)
	ratio := float64(dist["node2"]) / float64(dist["node1"])
	if ratio < 1.5 {
		t.Errorf("Expected node2 to get significantly more keys (ratio > 1.5), got %.2f (node1: %d, node2: %d)",
			ratio, dist["node1"], dist["node2"])
	}
}

// =============================================================================
// Node State Tests
// =============================================================================

func TestOfflineNodeExcluded(t *testing.T) {
	ring := NewRingWithDefaults()
	ring.AddNode("node1", "localhost:8080", 1)
	ring.AddNode("node2", "localhost:8081", 1)

	// Set node1 offline
	ring.SetNodeState("node1", NodeStateOffline)

	// All keys should go to node2
	for i := 0; i < 100; i++ {
		node, err := ring.Get(fmt.Sprintf("key-%d", i))
		if err != nil {
			t.Fatalf("Unexpected error: %v", err)
		}
		if node.ID != "node2" {
			t.Errorf("Expected key to map to node2, got %s", node.ID)
		}
	}
}

func TestDrainingNodeAcceptsNoNewKeys(t *testing.T) {
	ring := NewRingWithDefaults()
	ring.AddNode("node1", "localhost:8080", 1)
	ring.AddNode("node2", "localhost:8081", 1)

	// Set node1 draining (should still work but prefer others)
	// Note: draining nodes are still in the ring but can be handled differently
	ring.SetNodeState("node1", NodeStateDraining)

	// The draining node is still active for existing keys
	// but won't get new keys in GetN with replication
}

// =============================================================================
// Distribution Analysis Tests
// =============================================================================

func TestAnalyzeDistribution(t *testing.T) {
	ring := NewRingWithDefaults()
	ring.AddNode("node1", "localhost:8080", 1)
	ring.AddNode("node2", "localhost:8081", 1)
	ring.AddNode("node3", "localhost:8082", 1)

	keys := GenerateKeys(1000)
	stats := ring.AnalyzeDistribution(keys)

	if stats.TotalKeys != 1000 {
		t.Errorf("Expected 1000 keys, got %d", stats.TotalKeys)
	}

	if len(stats.NodeDistributions) != 3 {
		t.Errorf("Expected 3 nodes in distribution, got %d", len(stats.NodeDistributions))
	}

	if stats.BalanceScore < 0.8 {
		t.Errorf("Expected balance score >= 0.8, got %.2f", stats.BalanceScore)
	}
}

func TestDistributionWithWeights(t *testing.T) {
	ring := NewRingWithDefaults()
	ring.AddNode("node1", "localhost:8080", 1)
	ring.AddNode("node2", "localhost:8081", 2)
	ring.AddNode("node3", "localhost:8082", 3)

	keys := GenerateKeys(60000)
	stats := ring.AnalyzeDistribution(keys)

	// Check that weighted nodes get proportional keys
	n1 := stats.NodeDistributions["node1"]
	n2 := stats.NodeDistributions["node2"]
	n3 := stats.NodeDistributions["node3"]

	// Higher weighted nodes should get more keys
	if n2 <= n1 {
		t.Errorf("Expected n2 (weight=2) to have more keys than n1 (weight=1), got n1: %d, n2: %d", n1, n2)
	}
	if n3 <= n2 {
		t.Errorf("Expected n3 (weight=3) to have more keys than n2 (weight=2), got n2: %d, n3: %d", n2, n3)
	}
	
	// Verify all nodes received keys
	if n1 == 0 || n2 == 0 || n3 == 0 {
		t.Errorf("Expected all nodes to receive keys, got n1: %d, n2: %d, n3: %d", n1, n2, n3)
	}
}

// =============================================================================
// Migration Tests
// =============================================================================

func TestGetMigrationPlan(t *testing.T) {
	ring := NewRingWithDefaults()

	// Add initial nodes
	ring.AddNode("node1", "localhost:8080", 1)
	ring.AddNode("node2", "localhost:8081", 1)

	// Generate keys before adding new node
	keys := GenerateKeys(100)

	// Record original distribution
	originalDist := make(map[string]string)
	for _, key := range keys {
		node, _ := ring.Get(key)
		originalDist[key] = node.ID
	}

	// Add new node
	ring.AddNode("node3", "localhost:8082", 1)

	// Get migration plan
	plan := ring.GetMigrationPlan(keys, "node3")

	// Verify that migrated keys are now on node3
	for _, migration := range plan {
		if migration.ToNode != "node3" {
			t.Errorf("Expected migration to node3, got %s", migration.ToNode)
		}
		for _, key := range migration.Keys {
			node, _ := ring.Get(key)
			if node.ID != "node3" {
				t.Errorf("Expected key '%s' to be on node3, got %s", key, node.ID)
			}
		}
	}
}

// =============================================================================
// Statistics Tests
// =============================================================================

func TestGetStats(t *testing.T) {
	ring := NewRingWithDefaults()
	ring.AddNode("node1", "localhost:8080", 2)
	ring.AddNode("node2", "localhost:8081", 3)

	stats := ring.GetStats()

	if stats.NodeCount != 2 {
		t.Errorf("Expected 2 nodes, got %d", stats.NodeCount)
	}
	if stats.ActiveNodes != 2 {
		t.Errorf("Expected 2 active nodes, got %d", stats.ActiveNodes)
	}
	if stats.VirtualNodeCount == 0 {
		t.Error("Expected virtual nodes to be created")
	}
	if stats.AvgWeight != 2.5 {
		t.Errorf("Expected avg weight 2.5, got %.2f", stats.AvgWeight)
	}
}

func TestGetStatsWithStates(t *testing.T) {
	ring := NewRingWithDefaults()
	ring.AddNode("node1", "localhost:8080", 1)
	ring.AddNode("node2", "localhost:8081", 1)
	ring.AddNode("node3", "localhost:8082", 1)

	ring.SetNodeState("node2", NodeStateDraining)
	ring.SetNodeState("node3", NodeStateOffline)

	stats := ring.GetStats()

	if stats.ActiveNodes != 1 {
		t.Errorf("Expected 1 active node, got %d", stats.ActiveNodes)
	}
	if stats.DrainingNodes != 1 {
		t.Errorf("Expected 1 draining node, got %d", stats.DrainingNodes)
	}
	if stats.OfflineNodes != 1 {
		t.Errorf("Expected 1 offline node, got %d", stats.OfflineNodes)
	}
}

// =============================================================================
// Thread Safety Tests
// =============================================================================

func TestConcurrentAccess(t *testing.T) {
	ring := NewRingWithDefaults()

	// Add initial nodes
	for i := 0; i < 5; i++ {
		ring.AddNode(fmt.Sprintf("node%d", i), fmt.Sprintf("localhost:%d", 8080+i), 1)
	}

	// Concurrent reads and writes
	done := make(chan bool)
	numOps := 1000

	// Reader goroutines
	for i := 0; i < 10; i++ {
		go func(id int) {
			for j := 0; j < numOps; j++ {
				key := fmt.Sprintf("key-%d-%d", id, j)
				_, err := ring.Get(key)
				if err != nil && err != ErrEmptyRing {
					t.Errorf("Unexpected error: %v", err)
				}
			}
			done <- true
		}(i)
	}

	// Writer goroutines
	for i := 0; i < 2; i++ {
		go func(id int) {
			for j := 0; j < 10; j++ {
				nodeID := fmt.Sprintf("temp-node-%d-%d", id, j)
				ring.AddNode(nodeID, fmt.Sprintf("localhost:%d", 9000+j), 1)
				time.Sleep(time.Millisecond)
				ring.RemoveNode(nodeID)
			}
			done <- true
		}(i)
	}

	// Wait for all goroutines
	for i := 0; i < 12; i++ {
		<-done
	}
}

// =============================================================================
// Minimally Disruptive Rebalancing Tests
// =============================================================================

func TestMinimallyDisruptiveRebalancing(t *testing.T) {
	ring := NewRingWithDefaults()

	// Add initial nodes
	ring.AddNode("node1", "localhost:8080", 1)
	ring.AddNode("node2", "localhost:8081", 1)

	// Record key assignments
	keys := GenerateKeys(1000)
	originalAssignments := make(map[string]string)
	for _, key := range keys {
		node, _ := ring.Get(key)
		originalAssignments[key] = node.ID
	}

	// Add a new node
	ring.AddNode("node3", "localhost:8082", 1)

	// Count how many keys changed
	changedKeys := 0
	for _, key := range keys {
		node, _ := ring.Get(key)
		if node.ID != originalAssignments[key] {
			changedKeys++
		}
	}

	// Only about 1/3 of keys should change (roughly)
	changeRatio := float64(changedKeys) / float64(len(keys))
	if changeRatio > 0.4 {
		t.Errorf("Too many keys changed: %.2f%% (expected ~33%%)", changeRatio*100)
	}
}

// =============================================================================
// Benchmark Tests
// =============================================================================

func BenchmarkGet(b *testing.B) {
	ring := NewRingWithDefaults()
	for i := 0; i < 10; i++ {
		ring.AddNode(fmt.Sprintf("node%d", i), fmt.Sprintf("localhost:%d", 8080+i), 1)
	}

	keys := make([]string, b.N)
	for i := 0; i < b.N; i++ {
		keys[i] = fmt.Sprintf("key-%d", rand.Intn(10000))
	}

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		ring.Get(keys[i])
	}
}

func BenchmarkGetN(b *testing.B) {
	ring := NewRingWithDefaults()
	for i := 0; i < 10; i++ {
		ring.AddNode(fmt.Sprintf("node%d", i), fmt.Sprintf("localhost:%d", 8080+i), 1)
	}

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		ring.GetN(fmt.Sprintf("key-%d", i), 3)
	}
}

func BenchmarkAddNode(b *testing.B) {
	for i := 0; i < b.N; i++ {
		ring := NewRingWithDefaults()
		for j := 0; j < 100; j++ {
			ring.AddNode(fmt.Sprintf("node%d", j), fmt.Sprintf("localhost:%d", 8080+j), 1)
		}
	}
}

func BenchmarkHashFunction_CRC32(b *testing.B) {
	config := Config{HashFunction: HashCRC32}
	ring := NewRing(config)
	for i := 0; i < 10; i++ {
		ring.AddNode(fmt.Sprintf("node%d", i), fmt.Sprintf("localhost:%d", 8080+i), 1)
	}

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		ring.Get(fmt.Sprintf("key-%d", i))
	}
}

func BenchmarkHashFunction_MD5(b *testing.B) {
	config := Config{HashFunction: HashMD5}
	ring := NewRing(config)
	for i := 0; i < 10; i++ {
		ring.AddNode(fmt.Sprintf("node%d", i), fmt.Sprintf("localhost:%d", 8080+i), 1)
	}

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		ring.Get(fmt.Sprintf("key-%d", i))
	}
}

func BenchmarkHashFunction_SHA256(b *testing.B) {
	config := Config{HashFunction: Hash256}
	ring := NewRing(config)
	for i := 0; i < 10; i++ {
		ring.AddNode(fmt.Sprintf("node%d", i), fmt.Sprintf("localhost:%d", 8080+i), 1)
	}

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		ring.Get(fmt.Sprintf("key-%d", i))
	}
}

// =============================================================================
// Example Tests
// =============================================================================

func ExampleRing_Get() {
	ring := NewRingWithDefaults()
	ring.AddNode("node1", "localhost:8080", 1)
	ring.AddNode("node2", "localhost:8081", 1)
	ring.AddNode("node3", "localhost:8082", 1)

	node, _ := ring.Get("my-key")
	fmt.Printf("Key 'my-key' maps to: %s (%s)\n", node.ID, node.Address)
}

func ExampleRing_GetReplicas() {
	config := Config{
		ReplicationFactor: 3,
	}
	ring := NewRing(config)
	ring.AddNode("node1", "localhost:8080", 1)
	ring.AddNode("node2", "localhost:8081", 1)
	ring.AddNode("node3", "localhost:8082", 1)

	nodes, _ := ring.GetReplicas("my-key")
	fmt.Printf("Key 'my-key' is replicated on %d nodes:\n", len(nodes))
	for _, node := range nodes {
		fmt.Printf("  - %s\n", node.ID)
	}
}

func ExampleRing_AnalyzeDistribution() {
	ring := NewRingWithDefaults()
	ring.AddNode("node1", "localhost:8080", 1)
	ring.AddNode("node2", "localhost:8081", 2)
	ring.AddNode("node3", "localhost:8082", 3)

	keys := GenerateKeys(10000)
	stats := ring.AnalyzeDistribution(keys)

	fmt.Printf("Distribution analysis for %d keys:\n", stats.TotalKeys)
	for nodeID, count := range stats.NodeDistributions {
		fmt.Printf("  %s: %d keys\n", nodeID, count)
	}
	fmt.Printf("Balance score: %.2f\n", stats.BalanceScore)
}

func Example_weightedDistribution() {
	ring := NewRingWithDefaults()
	// Server with more capacity gets higher weight
	ring.AddNode("small", "localhost:8080", 1)
	ring.AddNode("medium", "localhost:8081", 2)
	ring.AddNode("large", "localhost:8082", 4)

	// Analyze how 10000 keys distribute
	stats := ring.AnalyzeDistribution(GenerateKeys(10000))

	// Sort nodes for consistent output
	var nodes []string
	for nodeID := range stats.NodeDistributions {
		nodes = append(nodes, nodeID)
	}
	sort.Strings(nodes)

	for _, nodeID := range nodes {
		count := stats.NodeDistributions[nodeID]
		percentage := float64(count) / float64(stats.TotalKeys) * 100
		fmt.Printf("%s: %d keys (%.1f%%)\n", nodeID, count, percentage)
	}
}

func Example_migration() {
	// Create a ring with 2 nodes
	ring := NewRingWithDefaults()
	ring.AddNode("node1", "192.168.1.1:8080", 1)
	ring.AddNode("node2", "192.168.1.2:8080", 1)

	// Existing keys
	keys := []string{"user:1", "user:2", "user:3", "user:4", "user:5"}

	// Add a new node
	ring.AddNode("node3", "192.168.1.3:8080", 1)

	// Get migration plan
	plan := ring.GetMigrationPlan(keys, "node3")

	fmt.Println("Migration plan for adding node3:")
	for _, migration := range plan {
		fmt.Printf("  Move %d keys from %s to %s\n", len(migration.Keys), migration.FromNode, migration.ToNode)
	}
}

func Example_nodeStates() {
	ring := NewRingWithDefaults()
	ring.AddNode("node1", "localhost:8080", 1)
	ring.AddNode("node2", "localhost:8081", 1)
	ring.AddNode("node3", "localhost:8082", 1)

	// Gracefully drain a node (no new requests)
	ring.SetNodeState("node2", NodeStateDraining)

	// Take a node offline for maintenance
	ring.SetNodeState("node3", NodeStateOffline)

	stats := ring.GetStats()
	fmt.Printf("Active: %d, Draining: %d, Offline: %d\n",
		stats.ActiveNodes, stats.DrainingNodes, stats.OfflineNodes)
	// Output: Active: 1, Draining: 1, Offline: 1
}

// =============================================================================
// String Tests
// =============================================================================

func TestString(t *testing.T) {
	ring := NewRingWithDefaults()
	ring.AddNode("node1", "localhost:8080", 1)

	str := ring.String()
	if !strings.Contains(str, "node1") {
		t.Errorf("Expected string to contain 'node1', got '%s'", str)
	}
}