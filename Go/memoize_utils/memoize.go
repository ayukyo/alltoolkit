// Package memoize_utils provides function memoization utilities with TTL, LRU eviction,
// and thread-safe caching capabilities.
//
// Features:
//   - Generic memoization for any function signature
//   - TTL (Time-To-Live) support for cache expiration
//   - LRU (Least Recently Used) eviction policy
//   - Thread-safe operations
//   - Memory statistics and cache management
//   - Zero external dependencies
package memoize_utils

import (
	"container/list"
	"sync"
	"time"
)

// ============================================================================
// Core Types
// ============================================================================

// Entry represents a cached value with metadata
type Entry[V any] struct {
	Value      V
	CreatedAt  time.Time
	ExpiresAt  time.Time
	AccessAt   time.Time
	AccessCount int64
	Key        string
}

// IsExpired checks if the entry has expired
func (e *Entry[V]) IsExpired() bool {
	if e.ExpiresAt.IsZero() {
		return false
	}
	return time.Now().After(e.ExpiresAt)
}

// Age returns the age of the entry
func (e *Entry[V]) Age() time.Duration {
	return time.Since(e.CreatedAt)
}

// TTL returns the remaining time to live
func (e *Entry[V]) TTL() time.Duration {
	if e.ExpiresAt.IsZero() {
		return -1 // No expiration
	}
	ttl := time.Until(e.ExpiresAt)
	if ttl < 0 {
		return 0
	}
	return ttl
}

// ============================================================================
// Cache Options
// ============================================================================

// Option configures the cache behavior
type Option func(*options)

type options struct {
	maxSize    int
	ttl        time.Duration
	onEvict    func(key string, value interface{})
	stats      bool
}

// WithMaxSize sets the maximum cache size (enables LRU eviction)
func WithMaxSize(size int) Option {
	return func(o *options) {
		o.maxSize = size
	}
}

// WithTTL sets the default TTL for cache entries
func WithTTL(ttl time.Duration) Option {
	return func(o *options) {
		o.ttl = ttl
	}
}

// WithEvictionCallback sets a callback for when entries are evicted
func WithEvictionCallback(callback func(key string, value interface{})) Option {
	return func(o *options) {
		o.onEvict = callback
	}
}

// WithStats enables statistics tracking
func WithStats(enabled bool) Option {
	return func(o *options) {
		o.stats = enabled
	}
}

// ============================================================================
// LRU Cache
// ============================================================================

// LRUCache implements a thread-safe LRU cache with TTL support
type LRUCache[K comparable, V any] struct {
	mu         sync.RWMutex
	items      map[K]*list.Element
	evictList  *list.List
	maxSize    int
	ttl        time.Duration
	onEvict    func(key string, value interface{})
	stats      *CacheStats
}

type lruEntry[K comparable, V any] struct {
	key   K
	entry *Entry[V]
}

// NewLRUCache creates a new LRU cache
func NewLRUCache[K comparable, V any](opts ...Option) *LRUCache[K, V] {
	o := &options{
		maxSize: 1000,
	}
	for _, opt := range opts {
		opt(o)
	}

	cache := &LRUCache[K, V]{
		items:     make(map[K]*list.Element),
		evictList: list.New(),
		maxSize:   o.maxSize,
		ttl:       o.ttl,
		onEvict:   o.onEvict,
	}
	if o.stats {
		cache.stats = &CacheStats{}
	}
	return cache
}

// Set adds a value to the cache
func (c *LRUCache[K, V]) Set(key K, value V) {
	c.SetWithTTL(key, value, c.ttl)
}

// SetWithTTL adds a value to the cache with a specific TTL
func (c *LRUCache[K, V]) SetWithTTL(key K, value V, ttl time.Duration) {
	c.mu.Lock()
	defer c.mu.Unlock()

	// Check if key exists
	if elem, ok := c.items[key]; ok {
		c.evictList.MoveToFront(elem)
		ent := elem.Value.(*lruEntry[K, V])
		ent.entry.Value = value
		ent.entry.CreatedAt = time.Now()
		ent.entry.AccessAt = time.Now()
		ent.entry.AccessCount++
		if ttl > 0 {
			ent.entry.ExpiresAt = time.Now().Add(ttl)
		}
		return
	}

	// Create new entry
	now := time.Now()
	entry := &Entry[V]{
		Value:       value,
		CreatedAt:   now,
		AccessAt:    now,
		AccessCount: 1,
	}
	if ttl > 0 {
		entry.ExpiresAt = now.Add(ttl)
	}

	// Add to cache
	elem := c.evictList.PushFront(&lruEntry[K, V]{key: key, entry: entry})
	c.items[key] = elem

	// Evict if necessary
	if c.maxSize > 0 && c.evictList.Len() > c.maxSize {
		c.evict()
	}
}

// Get retrieves a value from the cache
func (c *LRUCache[K, V]) Get(key K) (V, bool) {
	c.mu.Lock()
	defer c.mu.Unlock()

	elem, ok := c.items[key]
	if !ok {
		if c.stats != nil {
			c.stats.Misses++
		}
		var zero V
		return zero, false
	}

	ent := elem.Value.(*lruEntry[K, V])
	
	// Check expiration
	if ent.entry.IsExpired() {
		c.deleteElement(elem)
		if c.stats != nil {
			c.stats.Misses++
		}
		var zero V
		return zero, false
	}

	// Update access info
	c.evictList.MoveToFront(elem)
	ent.entry.AccessAt = time.Now()
	ent.entry.AccessCount++
	
	if c.stats != nil {
		c.stats.Hits++
	}
	
	return ent.entry.Value, true
}

// GetOrCompute retrieves a value or computes and caches it
func (c *LRUCache[K, V]) GetOrCompute(key K, compute func() (V, error)) (V, error) {
	// Try to get from cache
	if val, ok := c.Get(key); ok {
		return val, nil
	}

	// Compute value
	val, err := compute()
	if err != nil {
		var zero V
		return zero, err
	}

	// Cache it
	c.Set(key, val)
	return val, nil
}

// Delete removes a key from the cache
func (c *LRUCache[K, V]) Delete(key K) {
	c.mu.Lock()
	defer c.mu.Unlock()

	if elem, ok := c.items[key]; ok {
		c.deleteElement(elem)
	}
}

// Clear clears all entries from the cache
func (c *LRUCache[K, V]) Clear() {
	c.mu.Lock()
	defer c.mu.Unlock()

	for _, elem := range c.items {
		if c.onEvict != nil {
			ent := elem.Value.(*lruEntry[K, V])
			c.onEvict(any(ent.key).(string), ent.entry.Value)
		}
	}
	c.items = make(map[K]*list.Element)
	c.evictList.Init()
}

// Has checks if a key exists and is not expired
func (c *LRUCache[K, V]) Has(key K) bool {
	c.mu.RLock()
	defer c.mu.RUnlock()

	elem, ok := c.items[key]
	if !ok {
		return false
	}
	ent := elem.Value.(*lruEntry[K, V])
	return !ent.entry.IsExpired()
}

// Size returns the number of entries in the cache
func (c *LRUCache[K, V]) Size() int {
	c.mu.RLock()
	defer c.mu.RUnlock()
	return len(c.items)
}

// Keys returns all keys in the cache
func (c *LRUCache[K, V]) Keys() []K {
	c.mu.RLock()
	defer c.mu.RUnlock()

	keys := make([]K, 0, len(c.items))
	for _, elem := range c.items {
		keys = append(keys, elem.Value.(*lruEntry[K, V]).key)
	}
	return keys
}

// PurgeExpired removes all expired entries
func (c *LRUCache[K, V]) PurgeExpired() int {
	c.mu.Lock()
	defer c.mu.Unlock()

	count := 0
	for key, elem := range c.items {
		ent := elem.Value.(*lruEntry[K, V])
		if ent.entry.IsExpired() {
			c.deleteElement(elem)
			delete(c.items, key)
			count++
		}
	}
	return count
}

// GetStats returns cache statistics
func (c *LRUCache[K, V]) GetStats() CacheStats {
	if c.stats == nil {
		return CacheStats{}
	}
	c.mu.RLock()
	defer c.mu.RUnlock()
	
	stats := *c.stats
	stats.Size = len(c.items)
	stats.MaxSize = c.maxSize
	if stats.Hits+stats.Misses > 0 {
		stats.HitRate = float64(stats.Hits) / float64(stats.Hits+stats.Misses) * 100
	}
	return stats
}

// evict removes the oldest entry
func (c *LRUCache[K, V]) evict() {
	elem := c.evictList.Back()
	if elem != nil {
		c.deleteElement(elem)
	}
}

// deleteElement removes an element from the cache
func (c *LRUCache[K, V]) deleteElement(elem *list.Element) {
	ent := elem.Value.(*lruEntry[K, V])
	delete(c.items, ent.key)
	c.evictList.Remove(elem)
	
	if c.onEvict != nil {
		c.onEvict(any(ent.key).(string), ent.entry.Value)
	}
}

// ============================================================================
// Cache Statistics
// ============================================================================

// CacheStats holds cache statistics
type CacheStats struct {
	Hits     int64
	Misses   int64
	Size     int
	MaxSize  int
	HitRate  float64
}

// ============================================================================
// Memoize Functions
// ============================================================================

// Memoize wraps a function with memoization (single argument)
func Memoize1[K comparable, V any](fn func(K) V, opts ...Option) func(K) V {
	cache := NewLRUCache[K, V](opts...)
	return func(key K) V {
		if val, ok := cache.Get(key); ok {
			return val
		}
		val := fn(key)
		cache.Set(key, val)
		return val
	}
}

// Memoize1Err wraps a function with memoization that can return an error
func Memoize1Err[K comparable, V any](fn func(K) (V, error), opts ...Option) func(K) (V, error) {
	cache := NewLRUCache[K, V](opts...)
	return func(key K) (V, error) {
		if val, ok := cache.Get(key); ok {
			return val, nil
		}
		val, err := fn(key)
		if err != nil {
			var zero V
			return zero, err
		}
		cache.Set(key, val)
		return val, nil
	}
}

// Memoize2 wraps a function with memoization (two arguments)
func Memoize2[K1, K2 comparable, V any](fn func(K1, K2) V, opts ...Option) func(K1, K2) V {
	type key struct {
		k1 K1
		k2 K2
	}
	cache := NewLRUCache[key, V](opts...)
	return func(k1 K1, k2 K2) V {
		k := key{k1: k1, k2: k2}
		if val, ok := cache.Get(k); ok {
			return val
		}
		val := fn(k1, k2)
		cache.Set(k, val)
		return val
	}
}

// Memoize2Err wraps a function with memoization that can return an error
func Memoize2Err[K1, K2 comparable, V any](fn func(K1, K2) (V, error), opts ...Option) func(K1, K2) (V, error) {
	type key struct {
		k1 K1
		k2 K2
	}
	cache := NewLRUCache[key, V](opts...)
	return func(k1 K1, k2 K2) (V, error) {
		k := key{k1: k1, k2: k2}
		if val, ok := cache.Get(k); ok {
			return val, nil
		}
		val, err := fn(k1, k2)
		if err != nil {
			var zero V
			return zero, err
		}
		cache.Set(k, val)
		return val, nil
	}
}

// ============================================================================
// TTL Cache (Simpler alternative without LRU)
// ============================================================================

// TTLCache is a simple TTL cache without LRU eviction
type TTLCache[K comparable, V any] struct {
	mu      sync.RWMutex
	items   map[K]*Entry[V]
	ttl     time.Duration
	onEvict func(key string, value interface{})
	stats   *CacheStats
}

// NewTTLCache creates a new TTL-only cache
func NewTTLCache[K comparable, V any](ttl time.Duration, opts ...Option) *TTLCache[K, V] {
	o := &options{
		ttl: ttl,
	}
	for _, opt := range opts {
		opt(o)
	}

	cache := &TTLCache[K, V]{
		items: make(map[K]*Entry[V]),
		ttl:   ttl,
		onEvict: o.onEvict,
	}
	if o.stats {
		cache.stats = &CacheStats{}
	}
	return cache
}

// Set adds a value to the cache
func (c *TTLCache[K, V]) Set(key K, value V) {
	c.mu.Lock()
	defer c.mu.Unlock()

	now := time.Now()
	entry := &Entry[V]{
		Value:       value,
		CreatedAt:   now,
		AccessAt:    now,
		AccessCount: 1,
	}
	if c.ttl > 0 {
		entry.ExpiresAt = now.Add(c.ttl)
	}
	c.items[key] = entry
}

// SetWithTTL adds a value with a custom TTL
func (c *TTLCache[K, V]) SetWithTTL(key K, value V, ttl time.Duration) {
	c.mu.Lock()
	defer c.mu.Unlock()

	now := time.Now()
	entry := &Entry[V]{
		Value:       value,
		CreatedAt:   now,
		AccessAt:    now,
		AccessCount: 1,
	}
	if ttl > 0 {
		entry.ExpiresAt = now.Add(ttl)
	}
	c.items[key] = entry
}

// Get retrieves a value from the cache
func (c *TTLCache[K, V]) Get(key K) (V, bool) {
	c.mu.Lock()
	defer c.mu.Unlock()

	entry, ok := c.items[key]
	if !ok {
		if c.stats != nil {
			c.stats.Misses++
		}
		var zero V
		return zero, false
	}

	if entry.IsExpired() {
		delete(c.items, key)
		if c.stats != nil {
			c.stats.Misses++
		}
		var zero V
		return zero, false
	}

	entry.AccessAt = time.Now()
	entry.AccessCount++
	if c.stats != nil {
		c.stats.Hits++
	}
	return entry.Value, true
}

// Delete removes a key from the cache
func (c *TTLCache[K, V]) Delete(key K) {
	c.mu.Lock()
	defer c.mu.Unlock()
	
	if entry, ok := c.items[key]; ok {
		if c.onEvict != nil {
			c.onEvict(any(key).(string), entry.Value)
		}
		delete(c.items, key)
	}
}

// Clear clears all entries
func (c *TTLCache[K, V]) Clear() {
	c.mu.Lock()
	defer c.mu.Unlock()
	c.items = make(map[K]*Entry[V])
}

// Size returns the cache size
func (c *TTLCache[K, V]) Size() int {
	c.mu.RLock()
	defer c.mu.RUnlock()
	return len(c.items)
}

// PurgeExpired removes all expired entries
func (c *TTLCache[K, V]) PurgeExpired() int {
	c.mu.Lock()
	defer c.mu.Unlock()

	count := 0
	for key, entry := range c.items {
		if entry.IsExpired() {
			if c.onEvict != nil {
				c.onEvict(any(key).(string), entry.Value)
			}
			delete(c.items, key)
			count++
		}
	}
	return count
}

// GetStats returns cache statistics
func (c *TTLCache[K, V]) GetStats() CacheStats {
	if c.stats == nil {
		return CacheStats{}
	}
	c.mu.RLock()
	defer c.mu.RUnlock()
	
	stats := *c.stats
	stats.Size = len(c.items)
	if stats.Hits+stats.Misses > 0 {
		stats.HitRate = float64(stats.Hits) / float64(stats.Hits+stats.Misses) * 100
	}
	return stats
}

// ============================================================================
// Utility Functions
// ============================================================================

// ExpiredEntries returns a count of expired entries in a map with TTL entries
func ExpiredEntries[K comparable, V any](m map[K]*Entry[V]) int {
	count := 0
	for _, entry := range m {
		if entry.IsExpired() {
			count++
		}
	}
	return count
}

// PurgeMap removes expired entries from a map
func PurgeMap[K comparable, V any](m map[K]*Entry[V]) int {
	count := 0
	for key, entry := range m {
		if entry.IsExpired() {
			delete(m, key)
			count++
		}
	}
	return count
}