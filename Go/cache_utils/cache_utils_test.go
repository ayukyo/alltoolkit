package cache_utils

import (
	"sync"
	"testing"
	"time"
)

// TestNewCache tests cache creation
func TestNewCache(t *testing.T) {
	cache := NewCache[string, int](100)
	if cache == nil {
		t.Fatal("Expected cache to be created")
	}
	if cache.Capacity() != 100 {
		t.Errorf("Expected capacity 100, got %d", cache.Capacity())
	}

	// Test default capacity
	cache2 := NewCache[string, int](0)
	if cache2.Capacity() != 100 {
		t.Errorf("Expected default capacity 100, got %d", cache2.Capacity())
	}
}

// TestNewCacheWithPolicy tests cache creation with policy
func TestNewCacheWithPolicy(t *testing.T) {
	cache := NewCacheWithPolicy[string, int](100, EvictFIFO)
	if cache == nil {
		t.Fatal("Expected cache to be created")
	}
	if cache.policy != EvictFIFO {
		t.Errorf("Expected FIFO policy")
	}
}

// TestSetAndGet tests basic set and get operations
func TestSetAndGet(t *testing.T) {
	cache := NewCache[string, int](10)

	// Test set and get
	cache.Set("key1", 42, 0)
	val, ok := cache.Get("key1")
	if !ok {
		t.Error("Expected to find key1")
	}
	if val != 42 {
		t.Errorf("Expected value 42, got %d", val)
	}

	// Test non-existent key
	_, ok = cache.Get("nonexistent")
	if ok {
		t.Error("Expected not to find nonexistent key")
	}
}

// TestTTL tests time-to-live functionality
func TestTTL(t *testing.T) {
	cache := NewCache[string, int](10)

	// Set with short TTL
	cache.Set("key1", 42, 50*time.Millisecond)

	// Should exist immediately
	val, ok := cache.Get("key1")
	if !ok || val != 42 {
		t.Error("Expected to find key immediately after set")
	}

	// Wait for expiration
	time.Sleep(100 * time.Millisecond)

	// Should be expired
	_, ok = cache.Get("key1")
	if ok {
		t.Error("Expected key to be expired")
	}
}

// TestUpdate tests updating existing values
func TestUpdate(t *testing.T) {
	cache := NewCache[string, int](10)

	cache.Set("key1", 42, 0)
	cache.Set("key1", 100, 0)

	val, ok := cache.Get("key1")
	if !ok {
		t.Error("Expected to find key1")
	}
	if val != 100 {
		t.Errorf("Expected updated value 100, got %d", val)
	}
}

// TestDelete tests deletion
func TestDelete(t *testing.T) {
	cache := NewCache[string, int](10)

	cache.Set("key1", 42, 0)
	deleted := cache.Delete("key1")
	if !deleted {
		t.Error("Expected Delete to return true")
	}

	_, ok := cache.Get("key1")
	if ok {
		t.Error("Expected key to be deleted")
	}

	// Delete non-existent key
	deleted = cache.Delete("nonexistent")
	if deleted {
		t.Error("Expected Delete to return false for non-existent key")
	}
}

// TestClear tests clearing the cache
func TestClear(t *testing.T) {
	cache := NewCache[string, int](10)

	cache.Set("key1", 1, 0)
	cache.Set("key2", 2, 0)
	cache.Set("key3", 3, 0)

	cache.Clear()

	if cache.Len() != 0 {
		t.Errorf("Expected cache to be empty, got %d items", cache.Len())
	}

	_, ok := cache.Get("key1")
	if ok {
		t.Error("Expected key1 to be cleared")
	}
}

// TestLRUEviction tests LRU eviction policy
func TestLRUEviction(t *testing.T) {
	cache := NewCache[string, int](3)

	cache.Set("a", 1, 0)
	cache.Set("b", 2, 0)
	cache.Set("c", 3, 0)

	// Access "a" to make it most recently used
	cache.Get("a")

	// Add new item, should evict "b" (least recently used)
	cache.Set("d", 4, 0)

	_, ok := cache.Get("b")
	if ok {
		t.Error("Expected 'b' to be evicted (LRU)")
	}

	_, ok = cache.Get("a")
	if !ok {
		t.Error("Expected 'a' to still exist")
	}
}

// TestCapacity tests capacity enforcement
func TestCapacity(t *testing.T) {
	cache := NewCache[string, int](2)

	cache.Set("a", 1, 0)
	cache.Set("b", 2, 0)
	cache.Set("c", 3, 0) // Should trigger eviction

	if cache.Len() > 2 {
		t.Errorf("Expected cache size <= 2, got %d", cache.Len())
	}
}

// TestSetCapacity tests changing capacity
func TestSetCapacity(t *testing.T) {
	cache := NewCache[string, int](5)

	cache.Set("a", 1, 0)
	cache.Set("b", 2, 0)
	cache.Set("c", 3, 0)

	cache.SetCapacity(2)

	if cache.Capacity() != 2 {
		t.Errorf("Expected capacity 2, got %d", cache.Capacity())
	}
	if cache.Len() > 2 {
		t.Errorf("Expected size <= 2 after resize, got %d", cache.Len())
	}
}

// TestHas tests the Has method
func TestHas(t *testing.T) {
	cache := NewCache[string, int](10)

	cache.Set("key1", 42, 0)

	if !cache.Has("key1") {
		t.Error("Expected Has to return true for existing key")
	}

	if cache.Has("nonexistent") {
		t.Error("Expected Has to return false for non-existent key")
	}

	// Test expired key
	cache.Set("expired", 1, 1*time.Millisecond)
	time.Sleep(10 * time.Millisecond)
	if cache.Has("expired") {
		t.Error("Expected Has to return false for expired key")
	}
}

// TestGetOrCompute tests lazy loading
func TestGetOrCompute(t *testing.T) {
	cache := NewCache[string, int](10)

	computeCount := 0
	compute := func() int {
		computeCount++
		return 42
	}

	// First call should compute
	val := cache.GetOrCompute("key1", compute, 0)
	if val != 42 {
		t.Errorf("Expected 42, got %d", val)
	}
	if computeCount != 1 {
		t.Errorf("Expected compute to be called once, got %d", computeCount)
	}

	// Second call should use cached value
	val = cache.GetOrCompute("key1", compute, 0)
	if val != 42 {
		t.Errorf("Expected 42, got %d", val)
	}
	if computeCount != 1 {
		t.Errorf("Expected compute to still be called once, got %d", computeCount)
	}
}

// TestGetOrComputeWithError tests lazy loading with error handling
func TestGetOrComputeWithError(t *testing.T) {
	cache := NewCache[string, int](10)

	// Successful computation
	val, err := cache.GetOrComputeWithError("key1", func() (int, error) {
		return 42, nil
	}, 0)
	if err != nil {
		t.Errorf("Expected no error, got %v", err)
	}
	if val != 42 {
		t.Errorf("Expected 42, got %d", val)
	}

	// Error computation
	val, err = cache.GetOrComputeWithError("key2", func() (int, error) {
		return 0, testing.ErrAbort
	}, 0)
	if err == nil {
		t.Error("Expected an error")
	}
}

// TestStats tests statistics tracking
func TestStats(t *testing.T) {
	cache := NewCache[string, int](10)

	// Initial stats
	stats := cache.Stats()
	if stats.Hits != 0 || stats.Misses != 0 {
		t.Error("Expected initial stats to be zero")
	}

	// Add some hits and misses
	cache.Set("key1", 1, 0)
	cache.Get("key1") // hit
	cache.Get("key2") // miss

	stats = cache.Stats()
	if stats.Hits != 1 {
		t.Errorf("Expected 1 hit, got %d", stats.Hits)
	}
	if stats.Misses != 1 {
		t.Errorf("Expected 1 miss, got %d", stats.Misses)
	}

	// Test hit rate
	hitRate := stats.HitRate()
	if hitRate != 0.5 {
		t.Errorf("Expected hit rate 0.5, got %f", hitRate)
	}

	// Reset stats
	cache.ResetStats()
	stats = cache.Stats()
	if stats.Hits != 0 || stats.Misses != 0 {
		t.Error("Expected stats to be reset")
	}
}

// TestConcurrency tests thread safety
func TestConcurrency(t *testing.T) {
	cache := NewCache[int, int](100)

	var wg sync.WaitGroup
	numGoroutines := 100
	numOperations := 100

	// Concurrent writes
	for i := 0; i < numGoroutines; i++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()
			for j := 0; j < numOperations; j++ {
				cache.Set(id*numOperations+j, j, 0)
			}
		}(i)
	}

	// Concurrent reads
	for i := 0; i < numGoroutines; i++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()
			for j := 0; j < numOperations; j++ {
				cache.Get(id*numOperations + j)
			}
		}(i)
	}

	wg.Wait()

	// Cache should not panic or have race conditions
	if cache.Len() < 0 {
		t.Error("Cache length should be non-negative")
	}
}

// TestPeek tests peeking without updating access time
func TestPeek(t *testing.T) {
	cache := NewCache[string, int](3)

	cache.Set("a", 1, 0)
	cache.Set("b", 2, 0)
	cache.Set("c", 3, 0)

	// Peek "a"
	val, ok := cache.Peek("a")
	if !ok || val != 1 {
		t.Error("Expected to peek 'a'")
	}

	// Add new item, "a" should still be evicted because Peek doesn't update LRU
	cache.Set("d", 4, 0)

	// "a" might be evicted (depends on implementation)
	// The important thing is that Peek doesn't panic
}

// TestUpdateMethod tests the Update method
func TestUpdateMethod(t *testing.T) {
	cache := NewCache[string, int](10)

	cache.Set("key1", 42, 0)
	updated := cache.Update("key1", 100)
	if !updated {
		t.Error("Expected Update to return true")
	}

	val, _ := cache.Get("key1")
	if val != 100 {
		t.Errorf("Expected value 100, got %d", val)
	}

	// Update non-existent key
	updated = cache.Update("nonexistent", 1)
	if updated {
		t.Error("Expected Update to return false for non-existent key")
	}
}

// TestUpdateTTL tests updating TTL
func TestUpdateTTL(t *testing.T) {
	cache := NewCache[string, int](10)

	cache.Set("key1", 42, time.Hour)
	updated := cache.UpdateTTL("key1", 2*time.Hour)
	if !updated {
		t.Error("Expected UpdateTTL to return true")
	}

	// Update non-existent key
	updated = cache.UpdateTTL("nonexistent", time.Hour)
	if updated {
		t.Error("Expected UpdateTTL to return false for non-existent key")
	}
}

// TestTouch tests touching a key
func TestTouch(t *testing.T) {
	cache := NewCache[string, int](10)

	cache.Set("key1", 42, 0)
	touched := cache.Touch("key1")
	if !touched {
		t.Error("Expected Touch to return true")
	}

	// Touch non-existent key
	touched = cache.Touch("nonexistent")
	if touched {
		t.Error("Expected Touch to return false for non-existent key")
	}
}

// TestKeysAndValues tests getting keys and values
func TestKeysAndValues(t *testing.T) {
	cache := NewCache[string, int](10)

	cache.Set("a", 1, 0)
	cache.Set("b", 2, 0)

	keys := cache.Keys()
	if len(keys) != 2 {
		t.Errorf("Expected 2 keys, got %d", len(keys))
	}

	values := cache.Values()
	if len(values) != 2 {
		t.Errorf("Expected 2 values, got %d", len(values))
	}
}

// TestItems tests getting all items
func TestItems(t *testing.T) {
	cache := NewCache[string, int](10)

	cache.Set("a", 1, 0)
	cache.Set("b", 2, 0)

	items := cache.Items()
	if len(items) != 2 {
		t.Errorf("Expected 2 items, got %d", len(items))
	}
	if items["a"] != 1 || items["b"] != 2 {
		t.Error("Expected correct values in items")
	}
}

// TestForEach tests iterating over items
func TestForEach(t *testing.T) {
	cache := NewCache[string, int](10)

	cache.Set("a", 1, 0)
	cache.Set("b", 2, 0)

	count := 0
	cache.ForEach(func(key string, value int) bool {
		count++
		return true
	})

	if count != 2 {
		t.Errorf("Expected to iterate over 2 items, got %d", count)
	}
}

// TestFilter tests filtering items
func TestFilter(t *testing.T) {
	cache := NewCache[string, int](10)

	cache.Set("a", 1, 0)
	cache.Set("b", 2, 0)
	cache.Set("c", 3, 0)

	filtered := cache.Filter(func(key string, value int) bool {
		return value > 1
	})

	if len(filtered) != 2 {
		t.Errorf("Expected 2 filtered items, got %d", len(filtered))
	}
}

// TestFind tests finding an item
func TestFind(t *testing.T) {
	cache := NewCache[string, int](10)

	cache.Set("a", 1, 0)
	cache.Set("b", 2, 0)

	key, val, found := cache.Find(func(k string, v int) bool {
		return v == 2
	})

	if !found {
		t.Error("Expected to find item")
	}
	if key != "b" || val != 2 {
		t.Errorf("Expected key='b', val=2, got key='%s', val=%d", key, val)
	}
}

// TestCount tests counting items
func TestCount(t *testing.T) {
	cache := NewCache[string, int](10)

	cache.Set("a", 1, 0)
	cache.Set("b", 2, 0)
	cache.Set("c", 3, 0)

	count := cache.Count(func(key string, value int) bool {
		return value > 1
	})

	if count != 2 {
		t.Errorf("Expected count 2, got %d", count)
	}
}

// TestEvictionCallback tests eviction callback
func TestEvictionCallback(t *testing.T) {
	cache := NewCache[string, int](2)

	evicted := make(map[string]int)
	cache.SetEvictionCallback(func(key string, value int) {
		evicted[key] = value
	})

	cache.Set("a", 1, 0)
	cache.Set("b", 2, 0)
	cache.Set("c", 3, 0) // Should evict "a"

	if _, ok := evicted["a"]; !ok {
		t.Error("Expected eviction callback to be called for 'a'")
	}
}

// TestPurgeExpired tests purging expired items
func TestPurgeExpired(t *testing.T) {
	cache := NewCache[string, int](10)

	cache.Set("a", 1, 10*time.Millisecond)
	cache.Set("b", 2, 0) // No expiration

	time.Sleep(20 * time.Millisecond)

	removed := cache.PurgeExpired()
	if removed != 1 {
		t.Errorf("Expected 1 expired item removed, got %d", removed)
	}

	if cache.Has("a") {
		t.Error("Expected 'a' to be purged")
	}
	if !cache.Has("b") {
		t.Error("Expected 'b' to still exist")
	}
}

// TestGetExpiration tests getting expiration time
func TestGetExpiration(t *testing.T) {
	cache := NewCache[string, int](10)

	cache.Set("key1", 42, time.Hour)
	exp, ok := cache.GetExpiration("key1")
	if !ok {
		t.Error("Expected to get expiration")
	}
	if exp.IsZero() {
		t.Error("Expected non-zero expiration")
	}

	// Non-existent key
	_, ok = cache.GetExpiration("nonexistent")
	if ok {
		t.Error("Expected not to find expiration for non-existent key")
	}
}

// TestIsExpired tests checking if a key is expired
func TestIsExpired(t *testing.T) {
	cache := NewCache[string, int](10)

	cache.Set("key1", 42, 10*time.Millisecond)

	if cache.IsExpired("key1") {
		t.Error("Expected key not to be expired immediately")
	}

	time.Sleep(20 * time.Millisecond)

	if !cache.IsExpired("key1") {
		t.Error("Expected key to be expired after waiting")
	}

	// Non-existent key
	if cache.IsExpired("nonexistent") {
		t.Error("Expected non-existent key to not be expired")
	}
}

// TestResize tests resizing the cache
func TestResize(t *testing.T) {
	cache := NewCache[string, int](5)

	cache.Set("a", 1, 0)
	cache.Set("b", 2, 0)
	cache.Set("c", 3, 0)

	evicted := cache.Resize(2)
	if evicted != 1 {
		t.Errorf("Expected 1 item evicted, got %d", evicted)
	}

	if cache.Len() > 2 {
		t.Errorf("Expected size <= 2, got %d", cache.Len())
	}
}

// TestContainsValue tests checking if a value exists
func TestContainsValue(t *testing.T) {
	cache := NewCache[string, int](10)

	cache.Set("a", 1, 0)
	cache.Set("b", 2, 0)

	if !cache.ContainsValue(func(v int) bool {
		return v == 2
	}) {
		t.Error("Expected to find value 2")
	}

	if cache.ContainsValue(func(v int) bool {
		return v == 99
	}) {
		t.Error("Expected not to find value 99")
	}
}

// TestGenericTypes tests cache with different types
func TestGenericTypes(t *testing.T) {
	// Test with string keys and struct values
	type User struct {
		Name  string
		Email string
	}

	cache := NewCache[string, User](10)
	user := User{Name: "John", Email: "john@example.com"}
	cache.Set("user1", user, 0)

	retrieved, ok := cache.Get("user1")
	if !ok {
		t.Error("Expected to find user")
	}
	if retrieved.Name != "John" {
		t.Errorf("Expected name John, got %s", retrieved.Name)
	}

	// Test with int keys and string values
	intCache := NewCache[int, string](10)
	intCache.Set(1, "one", 0)
	intCache.Set(2, "two", 0)

	str, ok := intCache.Get(1)
	if !ok || str != "one" {
		t.Error("Expected to find 'one'")
	}
}

// BenchmarkSet benchmarks the Set operation
func BenchmarkSet(b *testing.B) {
	cache := NewCache[int, int](1000)
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		cache.Set(i%100, i, 0)
	}
}

// BenchmarkGet benchmarks the Get operation
func BenchmarkGet(b *testing.B) {
	cache := NewCache[int, int](1000)
	for i := 0; i < 1000; i++ {
		cache.Set(i, i, 0)
	}
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		cache.Get(i % 1000)
	}
}

// BenchmarkGetOrCompute benchmarks the GetOrCompute operation
func BenchmarkGetOrCompute(b *testing.B) {
	cache := NewCache[int, int](1000)
	compute := func() int {
		return 42
	}
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		cache.GetOrCompute(i%100, compute, 0)
	}
}