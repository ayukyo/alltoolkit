// Package lfu_cache_utils implements a thread-safe LFU (Least Frequently Used) cache
// with O(1) time complexity for Get and Put operations.
//
// LFU cache evicts the least frequently accessed items when the cache is full.
// When multiple items have the same frequency, the least recently used among them
// is evicted (LFU with LRU tiebreaker).
package lfu_cache_utils

import (
	"container/list"
	"encoding/json"
	"fmt"
	"sync"
	"time"
)

// LFUCache represents a thread-safe LFU cache
type LFUCache[K comparable, V any] struct {
	mu sync.RWMutex

	capacity int
	minFreq  int

	// key -> cache entry
	entries map[K]*cacheEntry[K, V]

	// freq -> doubly linked list of entries with that frequency
	freqLists map[int]*list.List

	// key -> element in the freq list (for O(1) removal)
	freqNodes map[K]*list.Element

	// Statistics
	hits      int64
	misses    int64
	evictions int64

	// Optional TTL support
	ttl time.Duration

	// Callback when an item is evicted
	onEvict func(key K, value V)
}

// cacheEntry stores the value and its frequency
type cacheEntry[K comparable, V any] struct {
	key       K
	value     V
	frequency int
	expiry    time.Time
	hasExpiry bool
}

// Stats holds cache statistics
type Stats struct {
	Capacity  int     `json:"capacity"`
	Size      int     `json:"size"`
	Hits      int64   `json:"hits"`
	Misses    int64   `json:"misses"`
	Evictions int64   `json:"evictions"`
	HitRate   float64 `json:"hit_rate"`
	MinFreq   int     `json:"min_freq"`
	MaxFreq   int     `json:"max_freq"`
	TTL       string  `json:"ttl,omitempty"`
}

// Config holds configuration options for the LFU cache
type Config struct {
	Capacity int
	TTL      time.Duration
	// OnEvict is called when an item is evicted (typed callback should be set after creation)
	OnEvict  func(key any, value any)
}

// entryJSON is used for JSON serialization
type entryJSON struct {
	Key       any `json:"key"`
	Value     any `json:"value"`
	Frequency int `json:"frequency"`
}

// New creates a new LFU cache with the specified capacity
func New[K comparable, V any](capacity int) *LFUCache[K, V] {
	return NewWithConfig[K, V](Config{Capacity: capacity})
}

// NewWithConfig creates a new LFU cache with custom configuration
func NewWithConfig[K comparable, V any](config Config) *LFUCache[K, V] {
	if config.Capacity <= 0 {
		config.Capacity = 1000
	}

	// Convert the generic callback to typed callback
	var typedOnEvict func(K, V)
	if config.OnEvict != nil {
		typedOnEvict = func(key K, value V) {
			config.OnEvict(key, value)
		}
	}

	return &LFUCache[K, V]{
		capacity:  config.Capacity,
		entries:  make(map[K]*cacheEntry[K, V]),
		freqLists: make(map[int]*list.List),
		freqNodes: make(map[K]*list.Element),
		ttl:       config.TTL,
		onEvict:   typedOnEvict,
	}
}

// Get retrieves a value from the cache
// Returns the value and true if found, zero value and false otherwise
func (c *LFUCache[K, V]) Get(key K) (V, bool) {
	c.mu.Lock()
	defer c.mu.Unlock()

	entry, exists := c.entries[key]
	if !exists {
		c.misses++
		var zero V
		return zero, false
	}

	// Check TTL
	if entry.hasExpiry && time.Now().After(entry.expiry) {
		c.removeEntry(key)
		c.misses++
		var zero V
		return zero, false
	}

	// Increment frequency
	c.incrementFrequency(key)

	c.hits++
	return entry.value, true
}

// Put adds or updates a value in the cache
func (c *LFUCache[K, V]) Put(key K, value V) {
	c.mu.Lock()
	defer c.mu.Unlock()

	// Check if key already exists
	if entry, exists := c.entries[key]; exists {
		entry.value = value
		if c.ttl > 0 {
			entry.expiry = time.Now().Add(c.ttl)
			entry.hasExpiry = true
		}
		c.incrementFrequency(key)
		return
	}

	// Evict if at capacity
	if len(c.entries) >= c.capacity {
		c.evict()
	}

	// Create new entry
	entry := &cacheEntry[K, V]{
		key:       key,
		value:     value,
		frequency: 1,
	}
	if c.ttl > 0 {
		entry.expiry = time.Now().Add(c.ttl)
		entry.hasExpiry = true
	}

	// Add to entries
	c.entries[key] = entry

	// Add to frequency list
	c.addToFreqList(key, 1)

	// Update min frequency
	c.minFreq = 1
}

// PutWithTTL adds a value with a custom TTL
func (c *LFUCache[K, V]) PutWithTTL(key K, value V, ttl time.Duration) {
	c.mu.Lock()
	defer c.mu.Unlock()

	// Check if key already exists
	if entry, exists := c.entries[key]; exists {
		entry.value = value
		entry.expiry = time.Now().Add(ttl)
		entry.hasExpiry = true
		c.incrementFrequency(key)
		return
	}

	// Evict if at capacity
	if len(c.entries) >= c.capacity {
		c.evict()
	}

	// Create new entry
	entry := &cacheEntry[K, V]{
		key:       key,
		value:     value,
		frequency: 1,
		expiry:    time.Now().Add(ttl),
		hasExpiry: true,
	}

	// Add to entries
	c.entries[key] = entry

	// Add to frequency list
	c.addToFreqList(key, 1)

	// Update min frequency
	c.minFreq = 1
}

// Delete removes a key from the cache
func (c *LFUCache[K, V]) Delete(key K) bool {
	c.mu.Lock()
	defer c.mu.Unlock()

	if _, exists := c.entries[key]; !exists {
		return false
	}

	c.removeEntry(key)
	return true
}

// Contains checks if a key exists in the cache without updating its frequency
func (c *LFUCache[K, V]) Contains(key K) bool {
	c.mu.RLock()
	defer c.mu.RUnlock()

	entry, exists := c.entries[key]
	if !exists {
		return false
	}

	// Check TTL
	if entry.hasExpiry && time.Now().After(entry.expiry) {
		return false
	}

	return true
}

// Peek retrieves a value without updating its frequency
func (c *LFUCache[K, V]) Peek(key K) (V, bool) {
	c.mu.RLock()
	defer c.mu.RUnlock()

	entry, exists := c.entries[key]
	if !exists {
		var zero V
		return zero, false
	}

	// Check TTL
	if entry.hasExpiry && time.Now().After(entry.expiry) {
		var zero V
		return zero, false
	}

	return entry.value, true
}

// Size returns the number of items in the cache
func (c *LFUCache[K, V]) Size() int {
	c.mu.RLock()
	defer c.mu.RUnlock()
	return len(c.entries)
}

// Capacity returns the maximum capacity of the cache
func (c *LFUCache[K, V]) Capacity() int {
	return c.capacity
}

// Clear removes all items from the cache
func (c *LFUCache[K, V]) Clear() {
	c.mu.Lock()
	defer c.mu.Unlock()

	c.entries = make(map[K]*cacheEntry[K, V])
	c.freqLists = make(map[int]*list.List)
	c.freqNodes = make(map[K]*list.Element)
	c.minFreq = 0
	c.hits = 0
	c.misses = 0
	c.evictions = 0
}

// Stats returns cache statistics
func (c *LFUCache[K, V]) Stats() Stats {
	c.mu.RLock()
	defer c.mu.RUnlock()

	total := c.hits + c.misses
	hitRate := float64(0)
	if total > 0 {
		hitRate = float64(c.hits) / float64(total)
	}

	maxFreq := 0
	for freq := range c.freqLists {
		if freq > maxFreq {
			maxFreq = freq
		}
	}

	ttlStr := ""
	if c.ttl > 0 {
		ttlStr = c.ttl.String()
	}

	return Stats{
		Capacity:  c.capacity,
		Size:      len(c.entries),
		Hits:      c.hits,
		Misses:    c.misses,
		Evictions: c.evictions,
		HitRate:   hitRate,
		MinFreq:   c.minFreq,
		MaxFreq:   maxFreq,
		TTL:       ttlStr,
	}
}

// Keys returns all keys in the cache
func (c *LFUCache[K, V]) Keys() []K {
	c.mu.RLock()
	defer c.mu.RUnlock()

	keys := make([]K, 0, len(c.entries))
	for key, entry := range c.entries {
		if !entry.hasExpiry || !time.Now().After(entry.expiry) {
			keys = append(keys, key)
		}
	}
	return keys
}

// Values returns all values in the cache
func (c *LFUCache[K, V]) Values() []V {
	c.mu.RLock()
	defer c.mu.RUnlock()

	values := make([]V, 0, len(c.entries))
	for _, entry := range c.entries {
		if !entry.hasExpiry || !time.Now().After(entry.expiry) {
			values = append(values, entry.value)
		}
	}
	return values
}

// ForEach iterates over all entries in the cache
func (c *LFUCache[K, V]) ForEach(fn func(key K, value V) bool) {
	c.mu.RLock()
	defer c.mu.RUnlock()

	for key, entry := range c.entries {
		if !entry.hasExpiry || !time.Now().After(entry.expiry) {
			if !fn(key, entry.value) {
				break
			}
		}
	}
}

// GetFrequency returns the access frequency of a key
func (c *LFUCache[K, V]) GetFrequency(key K) (int, bool) {
	c.mu.RLock()
	defer c.mu.RUnlock()

	entry, exists := c.entries[key]
	if !exists {
		return 0, false
	}
	return entry.frequency, true
}

// PurgeExpired removes all expired entries from the cache
func (c *LFUCache[K, V]) PurgeExpired() int {
	c.mu.Lock()
	defer c.mu.Unlock()

	count := 0
	now := time.Now()
	for key, entry := range c.entries {
		if entry.hasExpiry && now.After(entry.expiry) {
			c.removeEntry(key)
			count++
		}
	}
	return count
}

// Resize changes the capacity of the cache
// If new capacity is smaller, evicts items as needed
func (c *LFUCache[K, V]) Resize(newCapacity int) {
	c.mu.Lock()
	defer c.mu.Unlock()

	if newCapacity <= 0 {
		newCapacity = 1
	}

	c.capacity = newCapacity

	// Evict if necessary
	for len(c.entries) > c.capacity {
		c.evict()
	}
}

// incrementFrequency increases the frequency of a key and updates its position
func (c *LFUCache[K, V]) incrementFrequency(key K) {
	entry := c.entries[key]
	oldFreq := entry.frequency

	// Remove from old frequency list
	c.removeFromFreqList(key, oldFreq)

	// Increment frequency
	entry.frequency++
	newFreq := entry.frequency

	// Add to new frequency list
	c.addToFreqList(key, newFreq)

	// Update minFreq if needed
	if oldFreq == c.minFreq {
		if list, exists := c.freqLists[oldFreq]; !exists || list.Len() == 0 {
			c.minFreq = newFreq
		}
	}
}

// addToFreqList adds a key to a frequency list
func (c *LFUCache[K, V]) addToFreqList(key K, freq int) {
	if _, exists := c.freqLists[freq]; !exists {
		c.freqLists[freq] = list.New()
	}
	c.freqNodes[key] = c.freqLists[freq].PushBack(key)
}

// removeFromFreqList removes a key from a frequency list
func (c *LFUCache[K, V]) removeFromFreqList(key K, freq int) {
	if elem, exists := c.freqNodes[key]; exists {
		if list, ok := c.freqLists[freq]; ok {
			list.Remove(elem)
			if list.Len() == 0 {
				delete(c.freqLists, freq)
			}
		}
		delete(c.freqNodes, key)
	}
}

// removeEntry removes an entry completely from the cache
func (c *LFUCache[K, V]) removeEntry(key K) {
	entry, exists := c.entries[key]
	if !exists {
		return
	}

	// Remove from frequency list
	c.removeFromFreqList(key, entry.frequency)

	// Remove from entries
	delete(c.entries, key)

	// Call eviction callback
	if c.onEvict != nil {
		c.onEvict(key, entry.value)
	}
}

// evict removes the least frequently used item (with LRU tiebreaker)
func (c *LFUCache[K, V]) evict() {
	// Get the minimum frequency list
	freqList, exists := c.freqLists[c.minFreq]
	if !exists || freqList.Len() == 0 {
		// Find new minimum frequency
		c.updateMinFreq()
		if c.minFreq == 0 {
			return
		}
		freqList = c.freqLists[c.minFreq]
	}

	// Remove the oldest item from the minimum frequency list (LRU tiebreaker)
	if elem := freqList.Front(); elem != nil {
		key := elem.Value.(K)
		c.removeEntry(key)
		c.evictions++
	}
}

// updateMinFreq finds the minimum frequency with items
func (c *LFUCache[K, V]) updateMinFreq() {
	c.minFreq = 0
	for freq, list := range c.freqLists {
		if list.Len() > 0 {
			if c.minFreq == 0 || freq < c.minFreq {
				c.minFreq = freq
			}
		}
	}
}

// Export exports the cache contents for serialization
func (c *LFUCache[K, V]) Export() ([]entryJSON, error) {
	c.mu.RLock()
	defer c.mu.RUnlock()

	entries := make([]entryJSON, 0, len(c.entries))
	for key, entry := range c.entries {
		entries = append(entries, entryJSON{
			Key:       key,
			Value:     entry.value,
			Frequency: entry.frequency,
		})
	}
	return entries, nil
}

// ToJSON exports the cache as a JSON string
func (c *LFUCache[K, V]) ToJSON() (string, error) {
	entries, err := c.Export()
	if err != nil {
		return "", err
	}

	data, err := json.Marshal(entries)
	if err != nil {
		return "", err
	}
	return string(data), nil
}

// String returns a string representation of the cache stats
func (c *LFUCache[K, V]) String() string {
	stats := c.Stats()
	return fmt.Sprintf("LFUCache{capacity=%d, size=%d, hits=%d, misses=%d, hitRate=%.2f%%, evictions=%d}",
		stats.Capacity, stats.Size, stats.Hits, stats.Misses, stats.HitRate*100, stats.Evictions)
}

// GetOrSet retrieves a value if it exists, otherwise sets and returns the provided value
func (c *LFUCache[K, V]) GetOrSet(key K, value V) (V, bool) {
	c.mu.Lock()
	defer c.mu.Unlock()

	// Check if exists
	if entry, exists := c.entries[key]; exists {
		if !entry.hasExpiry || !time.Now().After(entry.expiry) {
			c.incrementFrequency(key)
			c.hits++
			return entry.value, true
		}
	}

	// Not found, add it
	c.misses++

	// Evict if at capacity
	if len(c.entries) >= c.capacity {
		c.evict()
	}

	// Create new entry
	entry := &cacheEntry[K, V]{
		key:       key,
		value:     value,
		frequency: 1,
	}
	if c.ttl > 0 {
		entry.expiry = time.Now().Add(c.ttl)
		entry.hasExpiry = true
	}

	c.entries[key] = entry
	c.addToFreqList(key, 1)
	c.minFreq = 1

	return value, false
}

// GetOrCompute retrieves a value if it exists, otherwise computes and stores it
func (c *LFUCache[K, V]) GetOrCompute(key K, compute func() V) (V, bool) {
	c.mu.Lock()
	defer c.mu.Unlock()

	// Check if exists
	if entry, exists := c.entries[key]; exists {
		if !entry.hasExpiry || !time.Now().After(entry.expiry) {
			c.incrementFrequency(key)
			c.hits++
			return entry.value, true
		}
	}

	// Not found, compute it
	c.misses++
	value := compute()

	// Evict if at capacity
	if len(c.entries) >= c.capacity {
		c.evict()
	}

	// Create new entry
	entry := &cacheEntry[K, V]{
		key:       key,
		value:     value,
		frequency: 1,
	}
	if c.ttl > 0 {
		entry.expiry = time.Now().Add(c.ttl)
		entry.hasExpiry = true
	}

	c.entries[key] = entry
	c.addToFreqList(key, 1)
	c.minFreq = 1

	return value, false
}