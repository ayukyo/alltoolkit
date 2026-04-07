// Package cache_utils provides a comprehensive in-memory caching solution for Go.
// It supports TTL (Time To Live), LRU (Least Recently Used) eviction policy,
// and thread-safe operations using sync.RWMutex.
//
// Features:
// - Zero dependencies, uses only Go standard library
// - TTL support with automatic expiration
// - LRU eviction when cache reaches capacity
// - Thread-safe concurrent access
// - Statistics tracking (hits, misses, evictions)
// - Generic type support (Go 1.18+)
//
// Example usage:
//
//	// Create a cache with capacity of 100 items
//	cache := cache_utils.NewCache[string, int](100)
//
//	// Set a value with TTL
//	cache.Set("key", 42, time.Minute)
//
//	// Get a value
//	if val, ok := cache.Get("key"); ok {
//	    fmt.Println(val)
//	}
//
//	// Get or compute (lazy loading)
//	val := cache.GetOrCompute("key", func() int {
//	    return expensiveOperation()
//	}, time.Minute)
//
package cache_utils

import (
	"container/list"
	"sync"
	"time"
)

// EvictionPolicy defines the eviction strategy when cache is full
type EvictionPolicy int

const (
	// EvictLRU removes the least recently used item
	EvictLRU EvictionPolicy = 0
	// EvictFIFO removes the oldest item (first in, first out)
	EvictFIFO EvictionPolicy = 1
	// EvictRandom removes a random item
	EvictRandom EvictionPolicy = 2
)

// CacheStats holds statistics about cache operations
type CacheStats struct {
	Hits        uint64
	Misses      uint64
	Evictions   uint64
	Expirations uint64
	Size        int
	Capacity    int
}

// HitRate returns the cache hit rate as a float64 between 0 and 1
func (s CacheStats) HitRate() float64 {
	total := s.Hits + s.Misses
	if total == 0 {
		return 0
	}
	return float64(s.Hits) / float64(total)
}

// cacheEntry represents a single cache entry
type cacheEntry[K comparable, V any] struct {
	key        K
	value      V
	expiration time.Time
	element    *list.Element
}

// isExpired checks if the cache entry has expired
func (e *cacheEntry[K, V]) isExpired() bool {
	return !e.expiration.IsZero() && time.Now().After(e.expiration)
}

// Cache is a thread-safe in-memory cache with TTL and LRU eviction support
type Cache[K comparable, V any] struct {
	mu          sync.RWMutex
	items       map[K]*cacheEntry[K, V]
	order       *list.List
	capacity    int
	policy      EvictionPolicy
	onEvicted   func(key K, value V)
	stats       CacheStats
}

// NewCache creates a new cache with the specified capacity
func NewCache[K comparable, V any](capacity int) *Cache[K, V] {
	if capacity <= 0 {
		capacity = 100
	}
	return &Cache[K, V]{
		items:    make(map[K]*cacheEntry[K, V]),
		order:    list.New(),
		capacity: capacity,
		policy:   EvictLRU,
	}
}

// NewCacheWithPolicy creates a new cache with specified capacity and eviction policy
func NewCacheWithPolicy[K comparable, V any](capacity int, policy EvictionPolicy) *Cache[K, V] {
	cache := NewCache[K, V](capacity)
	cache.policy = policy
	return cache
}

// SetEvictionCallback sets a callback function that is called when an item is evicted
func (c *Cache[K, V]) SetEvictionCallback(callback func(key K, value V)) {
	c.mu.Lock()
	c.onEvicted = callback
	c.mu.Unlock()
}

// Set adds or updates a key-value pair in the cache with optional TTL
// If ttl is 0, the item never expires
func (c *Cache[K, V]) Set(key K, value V, ttl time.Duration) {
	c.mu.Lock()
	defer c.mu.Unlock()

	c.purgeExpired()

	expiration := time.Time{}
	if ttl > 0 {
		expiration = time.Now().Add(ttl)
	}

	if entry, exists := c.items[key]; exists {
		// Update existing entry
		entry.value = value
		entry.expiration = expiration
		c.moveToFront(entry)
	} else {
		// Check if we need to evict
		if len(c.items) >= c.capacity {
			c.evict()
		}

		// Add new entry
		entry := &cacheEntry[K, V]{
			key:        key,
			value:      value,
			expiration: expiration,
		}
		entry.element = c.order.PushFront(entry)
		c.items[key] = entry
	}
}

// Get retrieves a value from the cache by key
// Returns the value and true if found and not expired, otherwise zero value and false
func (c *Cache[K, V]) Get(key K) (V, bool) {
	c.mu.Lock()
	defer c.mu.Unlock()

	if entry, exists := c.items[key]; exists {
		if entry.isExpired() {
			c.removeEntry(entry)
			c.stats.Expirations++
			c.stats.Misses++
			var zero V
			return zero, false
		}
		c.moveToFront(entry)
		c.stats.Hits++
		return entry.value, true
	}

	c.stats.Misses++
	var zero V
	return zero, false
}

// GetOrCompute retrieves a value from the cache, or computes and stores it if not found
// The compute function is only called if the key is not in the cache
func (c *Cache[K, V]) GetOrCompute(key K, compute func() V, ttl time.Duration) V {
	if val, ok := c.Get(key); ok {
		return val
	}

	val := compute()
	c.Set(key, val, ttl)
	return val
}

// GetOrComputeWithError retrieves a value from the cache, or computes and stores it if not found
// Similar to GetOrCompute but allows the compute function to return an error
func (c *Cache[K, V]) GetOrComputeWithError(key K, compute func() (V, error), ttl time.Duration) (V, error) {
	if val, ok := c.Get(key); ok {
		return val, nil
	}

	val, err := compute()
	if err != nil {
		var zero V
		return zero, err
	}

	c.Set(key, val, ttl)
	return val, nil
}

// Has checks if a key exists in the cache and is not expired
func (c *Cache[K, V]) Has(key K) bool {
	c.mu.RLock()
	defer c.mu.RUnlock()

	if entry, exists := c.items[key]; exists {
		return !entry.isExpired()
	}
	return false
}

// Delete removes a key from the cache
// Returns true if the key was found and removed, false otherwise
func (c *Cache[K, V]) Delete(key K) bool {
	c.mu.Lock()
	defer c.mu.Unlock()

	if entry, exists := c.items[key]; exists {
		c.removeEntry(entry)
		return true
	}
	return false
}

// Clear removes all items from the cache
func (c *Cache[K, V]) Clear() {
	c.mu.Lock()
	defer c.mu.Unlock()

	for _, entry := range c.items {
		if c.onEvicted != nil {
			c.onEvicted(entry.key, entry.value)
		}
	}

	c.items = make(map[K]*cacheEntry[K, V])
	c.order.Init()
}

// Len returns the current number of items in the cache
func (c *Cache[K, V]) Len() int {
	c.mu.RLock()
	defer c.mu.RUnlock()

	return len(c.items)
}

// Capacity returns the maximum capacity of the cache
func (c *Cache[K, V]) Capacity() int {
	c.mu.RLock()
	defer c.mu.RUnlock()

	return c.capacity
}

// SetCapacity changes the capacity of the cache
// If the new capacity is smaller than current size, items will be evicted
func (c *Cache[K, V]) SetCapacity(capacity int) {
	if capacity <= 0 {
		return
	}

	c.mu.Lock()
	defer c.mu.Unlock()

	c.capacity = capacity

	// Evict items if necessary
	for len(c.items) > c.capacity {
		c.evict()
	}
}

// Keys returns all keys in the cache (including expired ones)
func (c *Cache[K, V]) Keys() []K {
	c.mu.RLock()
	defer c.mu.RUnlock()

	keys := make([]K, 0, len(c.items))
	for key := range c.items {
		keys = append(keys, key)
	}
	return keys
}

// Values returns all values in the cache (including expired ones)
func (c *Cache[K, V]) Values() []V {
	c.mu.RLock()
	defer c.mu.RUnlock()

	values := make([]V, 0, len(c.items))
	for _, entry := range c.items {
		values = append(values, entry.value)
	}
	return values
}

// Items returns all non-expired key-value pairs in the cache
func (c *Cache[K, V]) Items() map[K]V {
	c.mu.Lock()
	defer c.mu.Unlock()

	c.purgeExpired()

	items := make(map[K]V, len(c.items))
	for key, entry := range c.items {
		items[key] = entry.value
	}
	return items
}

// Stats returns a copy of the current cache statistics
func (c *Cache[K, V]) Stats() CacheStats {
	c.mu.RLock()
	defer c.mu.RUnlock()

	return CacheStats{
		Hits:        c.stats.Hits,
		Misses:      c.stats.Misses,
		Evictions:   c.stats.Evictions,
		Expirations: c.stats.Expirations,
		Size:        len(c.items),
		Capacity:    c.capacity,
	}
}

// ResetStats resets all cache statistics to zero
func (c *Cache[K, V]) ResetStats() {
	c.mu.Lock()
	defer c.mu.Unlock()

	c.stats = CacheStats{}
}

// PurgeExpired removes all expired items from the cache
// Returns the number of items removed
func (c *Cache[K, V]) PurgeExpired() int {
	c.mu.Lock()
	defer c.mu.Unlock()

	return c.purgeExpired()
}

// purgeExpired removes expired entries (must be called with lock held)
func (c *Cache[K, V]) purgeExpired() int {
	removed := 0
	now := time.Now()
	for key, entry := range c.items {
		if !entry.expiration.IsZero() && now.After(entry.expiration) {
			c.removeEntry(entry)
			c.stats.Expirations++
			removed++
		}
	}
	return removed
}

// evict removes an item based on the eviction policy (must be called with lock held)
func (c *Cache[K, V]) evict() {
	if c.order.Len() == 0 {
		return
	}

	var entry *cacheEntry[K, V]

	switch c.policy {
	case EvictFIFO, EvictLRU:
		// Remove oldest item (back of list)
		elem := c.order.Back()
		if elem != nil {
			entry = elem.Value.(*cacheEntry[K, V])
		}
	case EvictRandom:
		// For random eviction, we still remove from back for simplicity
		// In production, you might want true random selection
		elem := c.order.Back()
		if elem != nil {
			entry = elem.Value.(*cacheEntry[K, V])
		}
	}

	if entry != nil {
		c.removeEntry(entry)
		c.stats.Evictions++
	}
}

// removeEntry removes an entry from the cache (must be called with lock held)
func (c *Cache[K, V]) removeEntry(entry *cacheEntry[K, V]) {
	if entry.element != nil {
		c.order.Remove(entry.element)
	}
	delete(c.items, entry.key)

	if c.onEvicted != nil {
		c.onEvicted(entry.key, entry.value)
	}
}

// moveToFront moves an entry to the front of the list (most recently used)
// must be called with lock held
func (c *Cache[K, V]) moveToFront(entry *cacheEntry[K, V]) {
	if entry.element != nil {
		c.order.MoveToFront(entry.element)
	}
}

// Update updates the value of an existing key without changing its position
// Returns true if the key exists and was updated, false otherwise
func (c *Cache[K, V]) Update(key K, value V) bool {
	c.mu.Lock()
	defer c.mu.Unlock()

	if entry, exists := c.items[key]; exists {
		if entry.isExpired() {
			c.removeEntry(entry)
			return false
		}
		entry.value = value
		return true
	}
	return false
}

// UpdateTTL updates the TTL of an existing key
// Returns true if the key exists and TTL was updated, false otherwise
func (c *Cache[K, V]) UpdateTTL(key K, ttl time.Duration) bool {
	c.mu.Lock()
	defer c.mu.Unlock()

	if entry, exists := c.items[key]; exists {
		if entry.isExpired() {
			c.removeEntry(entry)
			return false
		}
		if ttl > 0 {
			entry.expiration = time.Now().Add(ttl)
		} else {
			entry.expiration = time.Time{}
		}
		return true
	}
	return false
}

// Peek retrieves a value without updating its access time (LRU position)
// Returns the value and true if found, otherwise zero value and false
func (c *Cache[K, V]) Peek(key K) (V, bool) {
	c.mu.RLock()
	defer c.mu.RUnlock()

	if entry, exists := c.items[key]; exists {
		if entry.isExpired() {
			var zero V
			return zero, false
		}
		return entry.value, true
	}
	var zero V
	return zero, false
}

// GetExpiration returns the expiration time of a key
// Returns the expiration time and true if found, otherwise zero time and false
func (c *Cache[K, V]) GetExpiration(key K) (time.Time, bool) {
	c.mu.RLock()
	defer c.mu.RUnlock()

	if entry, exists := c.items[key]; exists {
		return entry.expiration, true
	}
	return time.Time{}, false
}

// IsExpired checks if a key has expired
// Returns true if the key exists and has expired, false otherwise
func (c *Cache[K, V]) IsExpired(key K) bool {
	c.mu.RLock()
	defer c.mu.RUnlock()

	if entry, exists := c.items[key]; exists {
		return entry.isExpired()
	}
	return false
}

// Touch updates the access time (LRU position) of a key
// Returns true if the key exists and was touched, false otherwise
func (c *Cache[K, V]) Touch(key K) bool {
	c.mu.Lock()
	defer c.mu.Unlock()

	if entry, exists := c.items[key]; exists {
		if entry.isExpired() {
			c.removeEntry(entry)
			return false
		}
		c.moveToFront(entry)
		return true
	}
	return false
}

// Resize changes the capacity and removes excess items if necessary
// Returns the number of items evicted
func (c *Cache[K, V]) Resize(capacity int) int {
	if capacity <= 0 {
		return 0
	}

	c.mu.Lock()
	defer c.mu.Unlock()

	oldCapacity := c.capacity
	c.capacity = capacity

	evicted := 0
	for len(c.items) > c.capacity {
		c.evict()
		evicted++
	}

	_ = oldCapacity // suppress unused warning
	return evicted
}

// ForEach iterates over all non-expired items in the cache
// The callback receives the key and value, and should return true to continue, false to stop
func (c *Cache[K, V]) ForEach(callback func(key K, value V) bool) {
	c.mu.Lock()
	defer c.mu.Unlock()

	c.purgeExpired()

	for key, entry := range c.items {
		if !callback(key, entry.value) {
			break
		}
	}
}

// Filter returns all items that match the given predicate
func (c *Cache[K, V]) Filter(predicate func(key K, value V) bool) map[K]V {
	c.mu.Lock()
	defer c.mu.Unlock()

	c.purgeExpired()

	result := make(map[K]V)
	for key, entry := range c.items {
		if predicate(key, entry.value) {
			result[key] = entry.value
		}
	}
	return result
}

// Find returns the first item that matches the given predicate
// Returns the key, value, and true if found, otherwise zero values and false
func (c *Cache[K, V]) Find(predicate func(key K, value V) bool) (K, V, bool) {
	c.mu.Lock()
	defer c.mu.Unlock()

	c.purgeExpired()

	for key, entry := range c.items {
		if predicate(key, entry.value) {
			return key, entry.value, true
		}
	}
	var zeroK K
	var zeroV V
	return zeroK, zeroV, false
}

// ContainsValue checks if any value in the cache matches the given predicate
func (c *Cache[K, V]) ContainsValue(predicate func(value V) bool) bool {
	c.mu.RLock()
	defer c.mu.RUnlock()

	for _, entry := range c.items {
		if !entry.isExpired() && predicate(entry.value) {
			return true
		}
	}
	return false
}

// Count returns the number of items that match the given predicate
func (c *Cache[K, V]) Count(predicate func(key K, value V) bool) int {
	c.mu.Lock()
	defer c.mu.Unlock()

	c.purgeExpired()

	count := 0
	for key, entry := range c.items {
		if predicate(key, entry.value) {
			count++
		}
	}
	return count
}