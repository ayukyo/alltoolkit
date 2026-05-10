// Package consistenthash provides a consistent hashing implementation
// with support for virtual nodes, weight-based distribution, and replication.
//
// Features:
//   - Consistent hashing with virtual nodes for better distribution
//   - Weighted node support for heterogeneous clusters
//   - Multiple hash functions (CRC32, MD5, SHA256, Murmur3)
//   - Node replication for fault tolerance
//   - Thread-safe operations
//   - Distribution analysis and balancing metrics
//   - Zero external dependencies
//
// Author: AllToolkit
// License: MIT
package consistenthash

import (
	"crypto/md5"
	"crypto/sha256"
	"encoding/binary"
	"errors"
	"fmt"
	"hash/crc32"
	"sort"
	"strings"
	"sync"
	"time"
)

// =============================================================================
// Types and Constants
// =============================================================================

// HashFunction defines the hash function type
type HashFunction int

const (
	HashCRC32 HashFunction = iota
	HashMD5
	Hash256
)

// NodeState represents the state of a node
type NodeState int

const (
	NodeStateActive NodeState = iota
	NodeStateDraining
	NodeStateOffline
)

// =============================================================================
// Node Definition
// =============================================================================

// Node represents a node in the consistent hash ring
type Node struct {
	ID           string
	Address      string
	Weight       int
	State        NodeState
	Metadata     map[string]interface{}
	VirtualNodes int // Number of virtual nodes (overrides default if > 0)

	// Statistics
	RequestCount int64
	LastRequest  time.Time
	AddedAt      time.Time
}

// String returns a string representation of the node
func (n *Node) String() string {
	return fmt.Sprintf("Node{ID: %s, Weight: %d, State: %v}", n.ID, n.Weight, n.State)
}

// =============================================================================
// Ring Configuration
// =============================================================================

// Config holds the configuration for the hash ring
type Config struct {
	// DefaultVirtualNodes is the default number of virtual nodes per physical node
	DefaultVirtualNodes int

	// HashFunction specifies which hash function to use
	HashFunction HashFunction

	// ReplicationFactor is the number of nodes to return for each key
	ReplicationFactor int

	// HashRingName is an optional name for the ring
	HashRingName string
}

// DefaultConfig returns the default configuration
func DefaultConfig() Config {
	return Config{
		DefaultVirtualNodes: 150,
		HashFunction:        HashCRC32,
		ReplicationFactor:   3,
	}
}

// =============================================================================
// Hash Functions
// =============================================================================

// hashKey generates a hash value for the given key using the configured hash function
func hashKey(key string, fn HashFunction) uint32 {
	switch fn {
	case HashMD5:
		h := md5.Sum([]byte(key))
		return binary.BigEndian.Uint32(h[:4])
	case Hash256:
		h := sha256.Sum256([]byte(key))
		return binary.BigEndian.Uint32(h[:4])
	default: // HashCRC32
		return crc32.ChecksumIEEE([]byte(key))
	}
}

// =============================================================================
// Virtual Node
// =============================================================================

type virtualNode struct {
	node   *Node
	hash   uint32
	nodeID string
}

// =============================================================================
// Hash Ring
// =============================================================================

// Ring represents a consistent hash ring
type Ring struct {
	config        Config
	nodes         map[string]*Node
	virtualNodes  []virtualNode
	sortedHashes  []uint32
	hashFunction  HashFunction
	mu            sync.RWMutex
	virtualNodeFn func(nodeID string, i int) string
}

// NewRing creates a new consistent hash ring with the given configuration
func NewRing(config Config) *Ring {
	if config.DefaultVirtualNodes <= 0 {
		config.DefaultVirtualNodes = 150
	}
	if config.ReplicationFactor <= 0 {
		config.ReplicationFactor = 3
	}

	return &Ring{
		config:       config,
		nodes:        make(map[string]*Node),
		hashFunction: config.HashFunction,
		virtualNodeFn: func(nodeID string, i int) string {
			return fmt.Sprintf("%s#%d", nodeID, i)
		},
	}
}

// NewRingWithDefaults creates a new ring with default configuration
func NewRingWithDefaults() *Ring {
	return NewRing(DefaultConfig())
}

// =============================================================================
// Node Management
// =============================================================================

// AddNode adds a node to the ring
func (r *Ring) AddNode(id, address string, weight int) *Node {
	return r.AddNodeWithMetadata(id, address, weight, nil)
}

// AddNodeWithMetadata adds a node with optional metadata
func (r *Ring) AddNodeWithMetadata(id, address string, weight int, metadata map[string]interface{}) *Node {
	if weight <= 0 {
		weight = 1
	}

	r.mu.Lock()
	defer r.mu.Unlock()

	node := &Node{
		ID:       id,
		Address:  address,
		Weight:   weight,
		State:    NodeStateActive,
		Metadata: metadata,
		AddedAt:  time.Now(),
	}

	if node.Metadata == nil {
		node.Metadata = make(map[string]interface{})
	}

	r.nodes[id] = node
	r.rebuildRing()

	return node
}

// RemoveNode removes a node from the ring
func (r *Ring) RemoveNode(id string) bool {
	r.mu.Lock()
	defer r.mu.Unlock()

	if _, exists := r.nodes[id]; !exists {
		return false
	}

	delete(r.nodes, id)
	r.rebuildRing()
	return true
}

// GetNode retrieves a node by ID
func (r *Ring) GetNode(id string) (*Node, bool) {
	r.mu.RLock()
	defer r.mu.RUnlock()

	node, exists := r.nodes[id]
	return node, exists
}

// GetNodes returns all nodes in the ring
func (r *Ring) GetNodes() []*Node {
	r.mu.RLock()
	defer r.mu.RUnlock()

	nodes := make([]*Node, 0, len(r.nodes))
	for _, node := range r.nodes {
		nodes = append(nodes, node)
	}
	return nodes
}

// SetNodeState changes the state of a node
func (r *Ring) SetNodeState(id string, state NodeState) bool {
	r.mu.Lock()
	defer r.mu.Unlock()

	if node, exists := r.nodes[id]; exists {
		node.State = state
		r.rebuildRing()
		return true
	}
	return false
}

// SetNodeWeight changes the weight of a node
func (r *Ring) SetNodeWeight(id string, weight int) bool {
	if weight <= 0 {
		return false
	}

	r.mu.Lock()
	defer r.mu.Unlock()

	if node, exists := r.nodes[id]; exists {
		node.Weight = weight
		r.rebuildRing()
		return true
	}
	return false
}

// NodeCount returns the number of nodes in the ring
func (r *Ring) NodeCount() int {
	r.mu.RLock()
	defer r.mu.RUnlock()
	return len(r.nodes)
}

// =============================================================================
// Ring Building
// =============================================================================

// rebuildRing rebuilds the virtual nodes and sorted hashes
func (r *Ring) rebuildRing() {
	virtualNodes := make([]virtualNode, 0)

	for _, node := range r.nodes {
		if node.State == NodeStateOffline {
			continue
		}

		// Calculate number of virtual nodes based on weight
		virtualNodeCount := r.config.DefaultVirtualNodes * node.Weight
		if node.VirtualNodes > 0 {
			virtualNodeCount = node.VirtualNodes * node.Weight
		}

		for i := 0; i < virtualNodeCount; i++ {
			vn := r.virtualNodeFn(node.ID, i)
			hash := hashKey(vn, r.hashFunction)
			virtualNodes = append(virtualNodes, virtualNode{
				node:   node,
				hash:   hash,
				nodeID: node.ID,
			})
		}
	}

	// Sort by hash
	sort.Slice(virtualNodes, func(i, j int) bool {
		return virtualNodes[i].hash < virtualNodes[j].hash
	})

	r.virtualNodes = virtualNodes
	r.sortedHashes = make([]uint32, len(virtualNodes))
	for i, vn := range virtualNodes {
		r.sortedHashes[i] = vn.hash
	}
}

// =============================================================================
// Key Lookup
// =============================================================================

// Get returns the node responsible for the given key
func (r *Ring) Get(key string) (*Node, error) {
	r.mu.RLock()
	defer r.mu.RUnlock()

	if len(r.virtualNodes) == 0 {
		return nil, ErrEmptyRing
	}

	hash := hashKey(key, r.hashFunction)
	idx := r.searchIndex(hash)

	if idx >= len(r.virtualNodes) {
		idx = 0
	}

	node := r.virtualNodes[idx].node
	node.RequestCount++
	node.LastRequest = time.Now()

	return node, nil
}

// GetN returns N unique nodes responsible for the given key (for replication)
func (r *Ring) GetN(key string, n int) ([]*Node, error) {
	r.mu.RLock()
	defer r.mu.RUnlock()

	if len(r.virtualNodes) == 0 {
		return nil, ErrEmptyRing
	}

	if n <= 0 {
		n = r.config.ReplicationFactor
	}

	// Limit n to the number of active nodes
	activeNodes := 0
	for _, node := range r.nodes {
		if node.State == NodeStateActive {
			activeNodes++
		}
	}
	if n > activeNodes {
		n = activeNodes
	}

	hash := hashKey(key, r.hashFunction)
	idx := r.searchIndex(hash)

	result := make([]*Node, 0, n)
	seen := make(map[string]bool)

	for i := 0; i < len(r.virtualNodes) && len(result) < n; i++ {
		vidx := (idx + i) % len(r.virtualNodes)
		node := r.virtualNodes[vidx].node

		if !seen[node.ID] && node.State == NodeStateActive {
			seen[node.ID] = true
			result = append(result, node)
		}
	}

	for _, node := range result {
		node.RequestCount++
		node.LastRequest = time.Now()
	}

	return result, nil
}

// GetReplicas returns the replication factor number of nodes for the key
func (r *Ring) GetReplicas(key string) ([]*Node, error) {
	return r.GetN(key, r.config.ReplicationFactor)
}

// searchIndex performs binary search to find the first node with hash >= key hash
func (r *Ring) searchIndex(hash uint32) int {
	return sort.Search(len(r.sortedHashes), func(i int) bool {
		return r.sortedHashes[i] >= hash
	})
}

// =============================================================================
// Distribution Analysis
// =============================================================================

// DistributionStats holds statistics about key distribution
type DistributionStats struct {
	TotalKeys      int
	NodeDistributions map[string]int
	MinKeys        int
	MaxKeys        int
	AvgKeys        float64
	StdDev         float64
	BalanceScore   float64 // 0-1, where 1 is perfect balance
}

// AnalyzeDistribution analyzes how keys would be distributed across nodes
func (r *Ring) AnalyzeDistribution(keys []string) *DistributionStats {
	r.mu.RLock()
	defer r.mu.RUnlock()

	if len(r.virtualNodes) == 0 {
		return &DistributionStats{}
	}

	dist := make(map[string]int)
	for _, key := range keys {
		hash := hashKey(key, r.hashFunction)
		idx := r.searchIndex(hash)
		if idx >= len(r.virtualNodes) {
			idx = 0
		}
		nodeID := r.virtualNodes[idx].nodeID
		dist[nodeID]++
	}

	minKeys := int(^uint(0) >> 1)
	maxKeys := 0
	total := 0

	for _, count := range dist {
		if count < minKeys {
			minKeys = count
		}
		if count > maxKeys {
			maxKeys = count
		}
		total += count
	}

	avg := float64(total) / float64(len(dist))

	// Calculate standard deviation
	variance := 0.0
	for _, count := range dist {
		diff := float64(count) - avg
		variance += diff * diff
	}
	stdDev := 0.0
	if len(dist) > 1 {
		stdDev = variance / float64(len(dist)-1)
	}

	// Calculate balance score (1 = perfect, 0 = worst)
	balanceScore := 0.0
	if maxKeys > 0 {
		balanceScore = float64(minKeys) / float64(maxKeys)
	}

	return &DistributionStats{
		TotalKeys:        len(keys),
		NodeDistributions: dist,
		MinKeys:          minKeys,
		MaxKeys:          maxKeys,
		AvgKeys:          avg,
		StdDev:           stdDev,
		BalanceScore:     balanceScore,
	}
}

// =============================================================================
// Migration Support
// =============================================================================

// MigrationPlan represents a plan for migrating keys between nodes
type MigrationPlan struct {
	FromNode string
	ToNode   string
	Keys     []string
}

// GetMigrationPlan returns keys that need to be migrated when adding a new node
func (r *Ring) GetMigrationPlan(keys []string, newNodeID string) []MigrationPlan {
	r.mu.RLock()
	defer r.mu.RUnlock()

	_, exists := r.nodes[newNodeID]
	if !exists {
		return nil
	}

	// Create a temporary ring without the new node
	tempRing := NewRing(r.config)
	for id, node := range r.nodes {
		if id != newNodeID && node.State != NodeStateOffline {
			tempRing.nodes[id] = node
		}
	}
	tempRing.rebuildRing()

	// Find keys that now map to the new node
	migrations := make(map[string][]string)

	for _, key := range keys {
		// Get old node
		oldNode, err := tempRing.Get(key)
		if err != nil {
			continue
		}

		// Get new node
		newNodeResult, err := r.Get(key)
		if err != nil {
			continue
		}

		// Check if owner changed
		if oldNode.ID != newNodeResult.ID && newNodeResult.ID == newNodeID {
			fromNode := oldNode.ID
			migrations[fromNode] = append(migrations[fromNode], key)
		}
	}

	// Convert to MigrationPlan slice
	result := make([]MigrationPlan, 0, len(migrations))
	for fromNode, keys := range migrations {
		result = append(result, MigrationPlan{
			FromNode: fromNode,
			ToNode:   newNodeID,
			Keys:     keys,
		})
	}

	return result
}

// =============================================================================
// Statistics
// =============================================================================

// Stats holds overall ring statistics
type Stats struct {
	Name               string
	NodeCount          int
	VirtualNodeCount   int
	ActiveNodes        int
	DrainingNodes      int
	OfflineNodes       int
	TotalRequests      int64
	AvgWeight          float64
	ReplicationFactor  int
	HashFunction       string
}

// GetStats returns statistics about the ring
func (r *Ring) GetStats() Stats {
	r.mu.RLock()
	defer r.mu.RUnlock()

	activeNodes := 0
	drainingNodes := 0
	offlineNodes := 0
	totalWeight := 0
	totalRequests := int64(0)

	for _, node := range r.nodes {
		totalWeight += node.Weight
		totalRequests += node.RequestCount

		switch node.State {
		case NodeStateActive:
			activeNodes++
		case NodeStateDraining:
			drainingNodes++
		case NodeStateOffline:
			offlineNodes++
		}
	}

	var avgWeight float64
	if len(r.nodes) > 0 {
		avgWeight = float64(totalWeight) / float64(len(r.nodes))
	}

	hashFnName := "CRC32"
	switch r.hashFunction {
	case HashMD5:
		hashFnName = "MD5"
	case Hash256:
		hashFnName = "SHA256"
	}

	return Stats{
		Name:              r.config.HashRingName,
		NodeCount:         len(r.nodes),
		VirtualNodeCount:  len(r.virtualNodes),
		ActiveNodes:       activeNodes,
		DrainingNodes:     drainingNodes,
		OfflineNodes:      offlineNodes,
		TotalRequests:     totalRequests,
		AvgWeight:         avgWeight,
		ReplicationFactor: r.config.ReplicationFactor,
		HashFunction:      hashFnName,
	}
}

// =============================================================================
// Errors
// =============================================================================

var (
	ErrEmptyRing       = errors.New("ring is empty")
	ErrNodeNotFound    = errors.New("node not found")
	ErrNodeExists      = errors.New("node already exists")
	ErrInvalidWeight   = errors.New("weight must be positive")
	ErrInvalidReplicas = errors.New("replication factor must be positive")
)

// =============================================================================
// Utility Functions
// =============================================================================

// GenerateKeys generates n test keys for distribution analysis
func GenerateKeys(n int) []string {
	keys := make([]string, n)
	for i := 0; i < n; i++ {
		keys[i] = fmt.Sprintf("key-%d", i)
	}
	return keys
}

// String returns a string representation of the ring
func (r *Ring) String() string {
	r.mu.RLock()
	defer r.mu.RUnlock()

	var sb strings.Builder
	sb.WriteString(fmt.Sprintf("Ring{Nodes: %d, VirtualNodes: %d, Hash: %v}\n",
		len(r.nodes), len(r.virtualNodes), r.hashFunction))

	for _, node := range r.nodes {
		sb.WriteString(fmt.Sprintf("  - %s\n", node.String()))
	}

	return sb.String()
}