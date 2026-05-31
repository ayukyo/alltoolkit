package lfu_cache_utils

/*
LFU Cache Utilities
===================
A Least Frequently Used (LFU) cache implementation in pure Go.
Zero external dependencies.

Features:
- O(1) get and set operations
- Frequency-based eviction
- Automatic frequency tracking
- Capacity management
- Custom TTL support
- Thread-safe operations
- Multiple frequency tiers
*/

import (
	"container/list"
	"fmt"
	"sync"
	"time"
)

// CacheEntry represents a cached item with metadata
type CacheEntry struct {
	Key       string
	Value     interface{}
	Frequency int
	CreatedAt time.Time
	ExpiresAt *time.Time
}

// LFUCache is a thread-safe Least Frequently Used cache
type LFUCache struct {
	mu       sync.RWMutex
	capacity int
	ttl      time.Duration
	items    map[string]*list.Element
	freqList *list.List // list of *CacheEntry, ordered by frequency
	onEvict  func(key string, value interface{})
}

// cacheItem wraps CacheEntry for list storage
type cacheItem struct {
	entry *CacheEntry
}

// New creates a new LFU cache with the given capacity
func New(capacity int) *LFUCache {
	if capacity <= 0 {
		capacity = 128
	}
	return &LFUCache{
		capacity: capacity,
		items:    make(map[string]*list.Element),
		freqList: list.New(),
	}
}

// NewWithTTL creates a new LFU cache with TTL support
func NewWithTTL(capacity int, ttl time.Duration) *LFUCache {
	cache := New(capacity)
	cache.ttl = ttl
	return cache
}

// NewWithEvict creates a new LFU cache with eviction callback
func NewWithEvict(capacity int, onEvict func(key string, value interface{})) *LFUCache {
	cache := New(capacity)
	cache.onEvict = onEvict
	return cache
}

// Get retrieves an item from the cache
func (c *LFUCache) Get(key string) (interface{}, bool) {
	c.mu.Lock()
	defer c.mu.Unlock()

	elem, exists := c.items[key]
	if !exists {
		return nil, false
	}

	item := elem.Value.(*cacheItem)
	entry := item.entry

	// Check expiration
	if entry.ExpiresAt != nil && time.Now().After(*entry.ExpiresAt) {
		c.remove(key, elem)
		return nil, false
	}

	// Increment frequency
	c.incrementFreq(elem)
	return entry.Value, true
}

// Set adds or updates an item in the cache
func (c *LFUCache) Set(key string, value interface{}) {
	c.mu.Lock()
	defer c.mu.Unlock()

	c.setInternal(key, value)
}

func (c *LFUCache) setInternal(key string, value interface{}) {
	var expiresAt *time.Time
	if c.ttl > 0 {
		t := time.Now().Add(c.ttl)
		expiresAt = &t
	}

	entry := &CacheEntry{
		Key:       key,
		Value:     value,
		Frequency: 1,
		CreatedAt: time.Now(),
		ExpiresAt: expiresAt,
	}

	// Check if key exists
	if elem, exists := c.items[key]; exists {
		oldItem := elem.Value.(*cacheItem)
		if c.onEvict != nil {
			c.onEvict(key, oldItem.entry.Value)
		}
		c.remove(key, elem)
	}

	// Evict if at capacity
	if c.capacity > 0 && len(c.items) >= c.capacity {
		c.evictLFU()
	}

	// Add new entry
	item := &cacheItem{entry: entry}
	elem := c.freqList.PushFront(item)
	c.items[key] = elem
}

// SetWithTTL sets an item with custom TTL
func (c *LFUCache) SetWithTTL(key string, value interface{}, ttl time.Duration) {
	c.mu.Lock()
	defer c.mu.Unlock()

	t := time.Now().Add(ttl)
	entry := &CacheEntry{
		Key:       key,
		Value:     value,
		Frequency: 1,
		CreatedAt: time.Now(),
		ExpiresAt: &t,
	}

	if elem, exists := c.items[key]; exists {
		oldItem := elem.Value.(*cacheItem)
		if c.onEvict != nil {
			c.onEvict(key, oldItem.entry.Value)
		}
		c.remove(key, elem)
	}

	if c.capacity > 0 && len(c.items) >= c.capacity {
		c.evictLFU()
	}

	item := &cacheItem{entry: entry}
	elem := c.freqList.PushFront(item)
	c.items[key] = elem
}

// Delete removes an item from the cache
func (c *LFUCache) Delete(key string) bool {
	c.mu.Lock()
	defer c.mu.Unlock()

	elem, exists := c.items[key]
	if !exists {
		return false
	}

	c.remove(key, elem)
	return true
}

// Contains checks if a key exists and is not expired
func (c *LFUCache) Contains(key string) bool {
	c.mu.RLock()
	defer c.mu.RUnlock()

	elem, exists := c.items[key]
	if !exists {
		return false
	}

	item := elem.Value.(*cacheItem)
	entry := item.entry

	if entry.ExpiresAt != nil && time.Now().After(*entry.ExpiresAt) {
		return false
	}

	return true
}

// Clear removes all items from the cache
func (c *LFUCache) Clear() {
	c.mu.Lock()
	defer c.mu.Unlock()

	if c.onEvict != nil {
		for key, elem := range c.items {
			item := elem.Value.(*cacheItem)
			c.onEvict(key, item.entry.Value)
		}
	}

	c.items = make(map[string]*list.Element)
	c.freqList.Init()
}

// Len returns the number of items in the cache
func (c *LFUCache) Len() int {
	c.mu.RLock()
	defer c.mu.RUnlock()
	return len(c.items)
}

// Keys returns all keys in the cache
func (c *LFUCache) Keys() []string {
	c.mu.RLock()
	defer c.mu.RUnlock()

	keys := make([]string, 0, len(c.items))
	now := time.Now()

	for key, elem := range c.items {
		item := elem.Value.(*cacheItem)
		entry := item.entry

		// Skip expired entries
		if entry.ExpiresAt != nil && now.After(*entry.ExpiresAt) {
			continue
		}
		keys = append(keys, key)
	}

	return keys
}

// Stats returns cache statistics
func (c *LFUCache) Stats() map[string]interface{} {
	c.mu.RLock()
	defer c.mu.RUnlock()

	stats := map[string]interface{}{
		"capacity": c.capacity,
		"size":     len(c.items),
		"ttl":      c.ttl.String(),
	}

	// Count items by frequency
	freqCounts := make(map[int]int)
	var minFreq, maxFreq int = 0, 0

	for _, elem := range c.items {
		item := elem.Value.(*cacheItem)
		freq := item.entry.Frequency
		freqCounts[freq]++
		if freq > maxFreq {
			maxFreq = freq
		}
		if minFreq == 0 || freq < minFreq {
			minFreq = freq
		}
	}

	if len(freqCounts) > 0 {
		stats["min_frequency"] = minFreq
		stats["max_frequency"] = maxFreq
		stats["frequency_distribution"] = freqCounts
	}

	return stats
}

// incrementFreq moves an item to a higher frequency tier
func (c *LFUCache) incrementFreq(elem *list.Element) {
	item := elem.Value.(*cacheItem)
	entry := item.entry
	entry.Frequency++

	// Move to front of list (higher frequency = closer to front)
	c.freqList.MoveToFront(elem)
}

// remove removes an item from the cache
func (c *LFUCache) remove(key string, elem *list.Element) {
	c.freqList.Remove(elem)
	delete(c.items, key)
}

// evictLFU removes the least frequently used item
func (c *LFUCache) evictLFU() {
	// Back of the list has lowest frequency
	elem := c.freqList.Back()
	if elem == nil {
		return
	}

	item := elem.Value.(*cacheItem)
	entry := item.entry

	if c.onEvict != nil {
		c.onEvict(entry.Key, entry.Value)
	}

	c.remove(entry.Key, elem)
}

// Cleanup removes expired entries
func (c *LFUCache) Cleanup() int {
	c.mu.Lock()
	defer c.mu.Unlock()

	now := time.Now()
	removed := 0

	var toRemove []*list.Element
	for key, elem := range c.items {
		item := elem.Value.(*cacheItem)
		entry := item.entry

		if entry.ExpiresAt != nil && now.After(*entry.ExpiresAt) {
			toRemove = append(toRemove, elem)
			if c.onEvict != nil {
				c.onEvict(key, entry.Value)
			}
		}
	}

	for _, elem := range toRemove {
		item := elem.Value.(*cacheItem)
		c.remove(item.entry.Key, elem)
		removed++
	}

	return removed
}

// Frequency returns the access frequency of a key
func (c *LFUCache) Frequency(key string) (int, bool) {
	c.mu.RLock()
	defer c.mu.RUnlock()

	elem, exists := c.items[key]
	if !exists {
		return 0, false
	}

	item := elem.Value.(*cacheItem)
	return item.entry.Frequency, true
}

// Resize changes the cache capacity
func (c *LFUCache) Resize(capacity int) {
	c.mu.Lock()
	defer c.mu.Unlock()

	c.capacity = capacity

	for c.capacity > 0 && len(c.items) > c.capacity {
		c.evictLFU()
	}
}

// GetMulti retrieves multiple items from the cache
func (c *LFUCache) GetMulti(keys []string) map[string]interface{} {
	c.mu.RLock()
	defer c.mu.RUnlock()

	results := make(map[string]interface{})
	now := time.Now()

	for _, key := range keys {
		elem, exists := c.items[key]
		if !exists {
			continue
		}

		item := elem.Value.(*cacheItem)
		entry := item.entry

		if entry.ExpiresAt != nil && now.After(*entry.ExpiresAt) {
			continue
		}

		results[key] = entry.Value
	}

	return results
}

// SetMulti sets multiple items in the cache
func (c *LFUCache) SetMulti(items map[string]interface{}) {
	c.mu.Lock()
	defer c.mu.Unlock()

	for key, value := range items {
		c.setInternal(key, value)
	}
}

// Update updates an existing entry's value without changing its frequency
func (c *LFUCache) Update(key string, value interface{}) bool {
	c.mu.Lock()
	defer c.mu.Unlock()

	elem, exists := c.items[key]
	if !exists {
		return false
	}

	item := elem.Value.(*cacheItem)
	item.entry.Value = value
	return true
}

// Touch updates an entry's access time without changing its value
func (c *LFUCache) Touch(key string) bool {
	c.mu.Lock()
	defer c.mu.Unlock()

	elem, exists := c.items[key]
	if !exists {
		return false
	}

	item := elem.Value.(*cacheItem)
	item.entry.CreatedAt = time.Now()
	c.incrementFreq(elem)
	return true
}

// String returns a string representation of the cache
func (c *LFUCache) String() string {
	c.mu.RLock()
	defer c.mu.RUnlock()

	return fmt.Sprintf("LFUCache(capacity=%d, size=%d, ttl=%v)", 
		c.capacity, len(c.items), c.ttl)
}
