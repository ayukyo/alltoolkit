// Package skiplist_utils provides a thread-safe Skip List implementation.
//
// A Skip List is a probabilistic data structure that allows O(log n) average
// time complexity for search, insert, and delete operations. It's essentially
// a sorted linked list with multiple levels of "express lanes" for faster access.
//
// Features:
// - O(log n) average time for search, insert, delete
// - Sorted iteration
// - Range queries
// - Thread-safe operations
// - Zero external dependencies
package skiplist_utils

import (
	"fmt"
	"math/rand"
	"sync"
	"time"
)

const (
	// MaxLevel is the maximum number of levels in the skip list
	MaxLevel = 16
	// Probability determines the chance of a node being promoted to a higher level
	Probability = 0.5
)

// SkipList is a probabilistic sorted data structure
type SkipList[K comparable, V any] struct {
	head     *Node[K, V]
	level    int
	length   int
	mu       sync.RWMutex
	rand     *rand.Rand
	compare  func(a, b K) int
}

// Node represents an element in the skip list
type Node[K comparable, V any] struct {
	key     K
	value   V
	forward []*Node[K, V]
}

// New creates a new SkipList with a custom comparison function
func New[K comparable, V any](compare func(a, b K) int) *SkipList[K, V] {
	source := rand.NewSource(time.Now().UnixNano())
	return &SkipList[K, V]{
		head: &Node[K, V]{
			forward: make([]*Node[K, V], MaxLevel),
		},
		level:   0,
		length:  0,
		rand:    rand.New(source),
		compare: compare,
	}
}

// NewInt creates a SkipList for int keys
func NewInt[V any]() *SkipList[int, V] {
	return New[int, V](func(a, b int) int {
		if a < b {
			return -1
		} else if a > b {
			return 1
		}
		return 0
	})
}

// NewString creates a SkipList for string keys
func NewString[V any]() *SkipList[string, V] {
	return New[string, V](func(a, b string) int {
		if a < b {
			return -1
		} else if a > b {
			return 1
		}
		return 0
	})
}

// NewFloat64 creates a SkipList for float64 keys
func NewFloat64[V any]() *SkipList[float64, V] {
	return New[float64, V](func(a, b float64) int {
		if a < b {
			return -1
		} else if a > b {
			return 1
		}
		return 0
	})
}

// randomLevel generates a random level for a new node
func (sl *SkipList[K, V]) randomLevel() int {
	level := 0
	for sl.rand.Float64() < Probability && level < MaxLevel-1 {
		level++
	}
	return level
}

// Insert adds or updates a key-value pair
func (sl *SkipList[K, V]) Insert(key K, value V) {
	sl.mu.Lock()
	defer sl.mu.Unlock()

	update := make([]*Node[K, V], MaxLevel)
	current := sl.head

	// Find the position for insertion
	for i := sl.level; i >= 0; i-- {
		for current.forward[i] != nil && sl.compare(current.forward[i].key, key) < 0 {
			current = current.forward[i]
		}
		update[i] = current
	}

	current = current.forward[0]

	// Update existing key
	if current != nil && sl.compare(current.key, key) == 0 {
		current.value = value
		return
	}

	// Insert new node
	newLevel := sl.randomLevel()

	if newLevel > sl.level {
		for i := sl.level + 1; i <= newLevel; i++ {
			update[i] = sl.head
		}
		sl.level = newLevel
	}

	newNode := &Node[K, V]{
		key:     key,
		value:   value,
		forward: make([]*Node[K, V], newLevel+1),
	}

	for i := 0; i <= newLevel; i++ {
		newNode.forward[i] = update[i].forward[i]
		update[i].forward[i] = newNode
	}

	sl.length++
}

// Search finds a value by key, returns the value and whether it was found
func (sl *SkipList[K, V]) Search(key K) (V, bool) {
	sl.mu.RLock()
	defer sl.mu.RUnlock()

	current := sl.head

	for i := sl.level; i >= 0; i-- {
		for current.forward[i] != nil && sl.compare(current.forward[i].key, key) < 0 {
			current = current.forward[i]
		}
	}

	current = current.forward[0]

	if current != nil && sl.compare(current.key, key) == 0 {
		return current.value, true
	}

	var zero V
	return zero, false
}

// Delete removes a key-value pair from the skip list
func (sl *SkipList[K, V]) Delete(key K) bool {
	sl.mu.Lock()
	defer sl.mu.Unlock()

	update := make([]*Node[K, V], MaxLevel)
	current := sl.head

	for i := sl.level; i >= 0; i-- {
		for current.forward[i] != nil && sl.compare(current.forward[i].key, key) < 0 {
			current = current.forward[i]
		}
		update[i] = current
	}

	current = current.forward[0]

	if current == nil || sl.compare(current.key, key) != 0 {
		return false
	}

	for i := 0; i <= sl.level; i++ {
		if update[i].forward[i] != current {
			break
		}
		update[i].forward[i] = current.forward[i]
	}

	// Update level
	for sl.level > 0 && sl.head.forward[sl.level] == nil {
		sl.level--
	}

	sl.length--
	return true
}

// Length returns the number of elements
func (sl *SkipList[K, V]) Length() int {
	sl.mu.RLock()
	defer sl.mu.RUnlock()
	return sl.length
}

// IsEmpty checks if the skip list is empty
func (sl *SkipList[K, V]) IsEmpty() bool {
	return sl.Length() == 0
}

// Level returns the current maximum level
func (sl *SkipList[K, V]) Level() int {
	sl.mu.RLock()
	defer sl.mu.RUnlock()
	return sl.level
}

// Min returns the minimum key and its value
func (sl *SkipList[K, V]) Min() (K, V, bool) {
	sl.mu.RLock()
	defer sl.mu.RUnlock()

	if sl.head.forward[0] == nil {
		var zeroK K
		var zeroV V
		return zeroK, zeroV, false
	}

	node := sl.head.forward[0]
	return node.key, node.value, true
}

// Max returns the maximum key and its value
func (sl *SkipList[K, V]) Max() (K, V, bool) {
	sl.mu.RLock()
	defer sl.mu.RUnlock()

	if sl.head.forward[0] == nil {
		var zeroK K
		var zeroV V
		return zeroK, zeroV, false
	}

	current := sl.head
	for i := sl.level; i >= 0; i-- {
		for current.forward[i] != nil {
			current = current.forward[i]
		}
	}

	return current.key, current.value, true
}

// Range returns all key-value pairs in the range [start, end]
func (sl *SkipList[K, V]) Range(start, end K) []struct {
	Key   K
	Value V
} {
	sl.mu.RLock()
	defer sl.mu.RUnlock()

	var result []struct {
		Key   K
		Value V
	}

	current := sl.head

	// Find start position
	for i := sl.level; i >= 0; i-- {
		for current.forward[i] != nil && sl.compare(current.forward[i].key, start) < 0 {
			current = current.forward[i]
		}
	}

	current = current.forward[0]

	// Collect range
	for current != nil && sl.compare(current.key, end) <= 0 {
		result = append(result, struct {
			Key   K
			Value V
		}{Key: current.key, Value: current.value})
		current = current.forward[0]
	}

	return result
}

// RangeByPrefix returns all key-value pairs with keys starting with the given prefix (for string keys)
func (sl *SkipList[K, V]) RangeByPrefix(prefix string) []struct {
	Key   K
	Value V
} {
	sl.mu.RLock()
	defer sl.mu.RUnlock()

	var result []struct {
		Key   K
		Value V
	}

	current := sl.head

	// Find first matching key
	for i := sl.level; i >= 0; i-- {
		for current.forward[i] != nil {
			keyStr := fmt.Sprintf("%v", current.forward[i].key)
			if keyStr >= prefix {
				break
			}
			current = current.forward[i]
		}
	}

	current = current.forward[0]

	// Collect all matching keys
	for current != nil {
		keyStr := fmt.Sprintf("%v", current.key)
		if len(keyStr) < len(prefix) || keyStr[:len(prefix)] != prefix {
			break
		}
		result = append(result, struct {
			Key   K
			Value V
		}{Key: current.key, Value: current.value})
		current = current.forward[0]
	}

	return result
}

// ForEach iterates over all elements in sorted order
func (sl *SkipList[K, V]) ForEach(fn func(key K, value V) bool) {
	sl.mu.RLock()
	defer sl.mu.RUnlock()

	current := sl.head.forward[0]
	for current != nil {
		if !fn(current.key, current.value) {
			break
		}
		current = current.forward[0]
	}
}

// ToSlice returns all elements as a sorted slice
func (sl *SkipList[K, V]) ToSlice() []struct {
	Key   K
	Value V
} {
	sl.mu.RLock()
	defer sl.mu.RUnlock()

	var result []struct {
		Key   K
		Value V
	}

	current := sl.head.forward[0]
	for current != nil {
		result = append(result, struct {
			Key   K
			Value V
		}{Key: current.key, Value: current.value})
		current = current.forward[0]
	}

	return result
}

// Clear removes all elements
func (sl *SkipList[K, V]) Clear() {
	sl.mu.Lock()
	defer sl.mu.Unlock()

	sl.head = &Node[K, V]{
		forward: make([]*Node[K, V], MaxLevel),
	}
	sl.level = 0
	sl.length = 0
}

// Contains checks if a key exists
func (sl *SkipList[K, V]) Contains(key K) bool {
	_, found := sl.Search(key)
	return found
}

// GetOrInsert returns the existing value or inserts and returns the new value
func (sl *SkipList[K, V]) GetOrInsert(key K, value V) V {
	sl.mu.Lock()
	defer sl.mu.Unlock()

	// Check if exists
	update := make([]*Node[K, V], MaxLevel)
	current := sl.head

	for i := sl.level; i >= 0; i-- {
		for current.forward[i] != nil && sl.compare(current.forward[i].key, key) < 0 {
			current = current.forward[i]
		}
		update[i] = current
	}

	current = current.forward[0]

	if current != nil && sl.compare(current.key, key) == 0 {
		return current.value
	}

	// Insert new
	newLevel := sl.randomLevel()

	if newLevel > sl.level {
		for i := sl.level + 1; i <= newLevel; i++ {
			update[i] = sl.head
		}
		sl.level = newLevel
	}

	newNode := &Node[K, V]{
		key:     key,
		value:   value,
		forward: make([]*Node[K, V], newLevel+1),
	}

	for i := 0; i <= newLevel; i++ {
		newNode.forward[i] = update[i].forward[i]
		update[i].forward[i] = newNode
	}

	sl.length++
	return value
}

// Count counts elements matching a predicate
func (sl *SkipList[K, V]) Count(predicate func(key K, value V) bool) int {
	sl.mu.RLock()
	defer sl.mu.RUnlock()

	count := 0
	current := sl.head.forward[0]
	for current != nil {
		if predicate(current.key, current.value) {
			count++
		}
		current = current.forward[0]
	}
	return count
}

// FindFirst returns the first element matching a predicate
func (sl *SkipList[K, V]) FindFirst(predicate func(key K, value V) bool) (K, V, bool) {
	sl.mu.RLock()
	defer sl.mu.RUnlock()

	current := sl.head.forward[0]
	for current != nil {
		if predicate(current.key, current.value) {
			return current.key, current.value, true
		}
		current = current.forward[0]
	}

	var zeroK K
	var zeroV V
	return zeroK, zeroV, false
}

// LowerBound finds the first element >= key
func (sl *SkipList[K, V]) LowerBound(key K) (K, V, bool) {
	sl.mu.RLock()
	defer sl.mu.RUnlock()

	current := sl.head

	for i := sl.level; i >= 0; i-- {
		for current.forward[i] != nil && sl.compare(current.forward[i].key, key) < 0 {
			current = current.forward[i]
		}
	}

	current = current.forward[0]

	if current == nil {
		var zeroK K
		var zeroV V
		return zeroK, zeroV, false
	}

	return current.key, current.value, true
}

// UpperBound finds the first element > key
func (sl *SkipList[K, V]) UpperBound(key K) (K, V, bool) {
	sl.mu.RLock()
	defer sl.mu.RUnlock()

	current := sl.head

	for i := sl.level; i >= 0; i-- {
		for current.forward[i] != nil && sl.compare(current.forward[i].key, key) <= 0 {
			current = current.forward[i]
		}
	}

	current = current.forward[0]

	if current == nil {
		var zeroK K
		var zeroV V
		return zeroK, zeroV, false
	}

	return current.key, current.value, true
}

// Rank returns the 0-based rank of a key (position in sorted order)
func (sl *SkipList[K, V]) Rank(key K) (int, bool) {
	sl.mu.RLock()
	defer sl.mu.RUnlock()

	current := sl.head.forward[0]
	rank := 0

	for current != nil {
		cmp := sl.compare(current.key, key)
		if cmp == 0 {
			return rank, true
		}
		if cmp > 0 {
			break
		}
		rank++
		current = current.forward[0]
	}

	return -1, false
}

// GetByRank returns the element at the given rank
func (sl *SkipList[K, V]) GetByRank(rank int) (K, V, bool) {
	sl.mu.RLock()
	defer sl.mu.RUnlock()

	if rank < 0 || rank >= sl.length {
		var zeroK K
		var zeroV V
		return zeroK, zeroV, false
	}

	current := sl.head.forward[0]
	for i := 0; i < rank && current != nil; i++ {
		current = current.forward[0]
	}

	if current == nil {
		var zeroK K
		var zeroV V
		return zeroK, zeroV, false
	}

	return current.key, current.value, true
}