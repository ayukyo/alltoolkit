package lfu_cache_utils

import (
	"sync"
	"testing"
	"time"
)

func TestNew(t *testing.T) {
	cache := New[string, int](100)
	if cache == nil {
		t.Fatal("New returned nil")
	}
	if cache.Capacity() != 100 {
		t.Errorf("Expected capacity 100, got %d", cache.Capacity())
	}
	if cache.Size() != 0 {
		t.Errorf("Expected size 0, got %d", cache.Size())
	}
}

func TestNewWithConfig(t *testing.T) {
	cache := NewWithConfig[string, int](Config{
		Capacity: 50,
		TTL:      time.Hour,
	})
	if cache == nil {
		t.Fatal("NewWithConfig returned nil")
	}
	if cache.Capacity() != 50 {
		t.Errorf("Expected capacity 50, got %d", cache.Capacity())
	}
}

func TestNewWithZeroCapacity(t *testing.T) {
	cache := New[string, int](0)
	if cache.Capacity() != 1000 {
		t.Errorf("Expected default capacity 1000, got %d", cache.Capacity())
	}
}

func TestPutAndGet(t *testing.T) {
	cache := New[string, int](10)
	
	cache.Put("one", 1)
	cache.Put("two", 2)
	cache.Put("three", 3)
	
	if cache.Size() != 3 {
		t.Errorf("Expected size 3, got %d", cache.Size())
	}
	
	if v, ok := cache.Get("one"); !ok || v != 1 {
		t.Errorf("Expected (1, true), got (%d, %v)", v, ok)
	}
	
	if v, ok := cache.Get("two"); !ok || v != 2 {
		t.Errorf("Expected (2, true), got (%d, %v)", v, ok)
	}
	
	if v, ok := cache.Get("three"); !ok || v != 3 {
		t.Errorf("Expected (3, true), got (%d, %v)", v, ok)
	}
}

func TestGetMissing(t *testing.T) {
	cache := New[string, int](10)
	
	if v, ok := cache.Get("missing"); ok || v != 0 {
		t.Errorf("Expected (0, false), got (%d, %v)", v, ok)
	}
}

func TestUpdateExisting(t *testing.T) {
	cache := New[string, int](10)
	
	cache.Put("key", 1)
	if v, ok := cache.Get("key"); !ok || v != 1 {
		t.Errorf("Expected (1, true), got (%d, %v)", v, ok)
	}
	
	cache.Put("key", 2)
	if v, ok := cache.Get("key"); !ok || v != 2 {
		t.Errorf("Expected (2, true), got (%d, %v)", v, ok)
	}
	
	if cache.Size() != 1 {
		t.Errorf("Expected size 1, got %d", cache.Size())
	}
}

func TestEviction(t *testing.T) {
	cache := New[string, int](3)
	
	cache.Put("a", 1)
	cache.Put("b", 2)
	cache.Put("c", 3)
	
	// Access "a" twice to increase its frequency
	cache.Get("a")
	cache.Get("a")
	
	// Access "b" once
	cache.Get("b")
	
	// Add new item, should evict "c" (lowest frequency)
	cache.Put("d", 4)
	
	if cache.Contains("c") {
		t.Error("Expected 'c' to be evicted")
	}
	
	if !cache.Contains("a") {
		t.Error("Expected 'a' to still be in cache")
	}
}

func TestEvictionLRUTiebreaker(t *testing.T) {
	cache := New[string, int](3)
	
	// All items have same frequency initially
	cache.Put("a", 1)
	cache.Put("b", 2)
	cache.Put("c", 3)
	
	// Access all once (same frequency)
	cache.Get("a")
	cache.Get("b")
	cache.Get("c")
	
	// Add new item, should evict "a" (oldest among same frequency)
	cache.Put("d", 4)
	
	if cache.Contains("a") {
		t.Error("Expected 'a' to be evicted (LRU tiebreaker)")
	}
}

func TestDelete(t *testing.T) {
	cache := New[string, int](10)
	
	cache.Put("key", 1)
	if !cache.Delete("key") {
		t.Error("Expected Delete to return true")
	}
	
	if cache.Contains("key") {
		t.Error("Expected key to be deleted")
	}
	
	if cache.Delete("missing") {
		t.Error("Expected Delete of missing key to return false")
	}
}

func TestContains(t *testing.T) {
	cache := New[string, int](10)
	
	cache.Put("key", 1)
	
	if !cache.Contains("key") {
		t.Error("Expected Contains to return true")
	}
	
	if cache.Contains("missing") {
		t.Error("Expected Contains to return false for missing key")
	}
}

func TestPeek(t *testing.T) {
	cache := New[string, int](10)
	
	cache.Put("key", 1)
	cache.Get("key") // Increment frequency
	
	// Peek should not change frequency
	freq1, _ := cache.GetFrequency("key")
	cache.Peek("key")
	freq2, _ := cache.GetFrequency("key")
	
	if freq1 != freq2 {
		t.Errorf("Peek should not change frequency: %d -> %d", freq1, freq2)
	}
}

func TestKeys(t *testing.T) {
	cache := New[string, int](10)
	
	cache.Put("a", 1)
	cache.Put("b", 2)
	cache.Put("c", 3)
	
	keys := cache.Keys()
	if len(keys) != 3 {
		t.Errorf("Expected 3 keys, got %d", len(keys))
	}
	
	keyMap := make(map[string]bool)
	for _, k := range keys {
		keyMap[k] = true
	}
	
	if !keyMap["a"] || !keyMap["b"] || !keyMap["c"] {
		t.Error("Expected keys to contain a, b, c")
	}
}

func TestValues(t *testing.T) {
	cache := New[string, int](10)
	
	cache.Put("a", 1)
	cache.Put("b", 2)
	cache.Put("c", 3)
	
	values := cache.Values()
	if len(values) != 3 {
		t.Errorf("Expected 3 values, got %d", len(values))
	}
}

func TestClear(t *testing.T) {
	cache := New[string, int](10)
	
	cache.Put("a", 1)
	cache.Put("b", 2)
	cache.Put("c", 3)
	
	cache.Clear()
	
	if cache.Size() != 0 {
		t.Errorf("Expected size 0 after clear, got %d", cache.Size())
	}
	
	stats := cache.Stats()
	if stats.Hits != 0 || stats.Misses != 0 {
		t.Errorf("Expected stats to be reset after clear")
	}
}

func TestStats(t *testing.T) {
	cache := New[string, int](10)
	
	cache.Put("a", 1)
	cache.Get("a")  // hit
	cache.Get("b")  // miss
	
	stats := cache.Stats()
	
	if stats.Capacity != 10 {
		t.Errorf("Expected capacity 10, got %d", stats.Capacity)
	}
	
	if stats.Size != 1 {
		t.Errorf("Expected size 1, got %d", stats.Size)
	}
	
	if stats.Hits != 1 {
		t.Errorf("Expected 1 hit, got %d", stats.Hits)
	}
	
	if stats.Misses != 1 {
		t.Errorf("Expected 1 miss, got %d", stats.Misses)
	}
	
	if stats.HitRate != 0.5 {
		t.Errorf("Expected hit rate 0.5, got %f", stats.HitRate)
	}
}

func TestGetOrSet(t *testing.T) {
	cache := New[string, int](10)
	
	// Set new value
	v, found := cache.GetOrSet("key", 42)
	if found || v != 42 {
		t.Errorf("Expected (42, false), got (%d, %v)", v, found)
	}
	
	// Get existing value
	v, found = cache.GetOrSet("key", 100)
	if !found || v != 42 {
		t.Errorf("Expected (42, true), got (%d, %v)", v, found)
	}
}

func TestGetOrCompute(t *testing.T) {
	cache := New[string, int](10)
	computed := false
	
	// Compute new value
	v, found := cache.GetOrCompute("key", func() int {
		computed = true
		return 42
	})
	
	if found || v != 42 || !computed {
		t.Errorf("Expected (42, false, computed=true), got (%d, %v, computed=%v)", v, found, computed)
	}
	
	computed = false
	
	// Get existing value (should not compute)
	v, found = cache.GetOrCompute("key", func() int {
		computed = true
		return 100
	})
	
	if !found || v != 42 || computed {
		t.Errorf("Expected (42, true, computed=false), got (%d, %v, computed=%v)", v, found, computed)
	}
}

func TestTTL(t *testing.T) {
	cache := NewWithConfig[string, int](Config{
		Capacity: 10,
		TTL:      100 * time.Millisecond,
	})
	
	cache.Put("key", 1)
	
	// Should exist immediately
	if v, ok := cache.Get("key"); !ok || v != 1 {
		t.Errorf("Expected (1, true), got (%d, %v)", v, ok)
	}
	
	// Wait for TTL to expire
	time.Sleep(150 * time.Millisecond)
	
	// Should be expired
	if _, ok := cache.Get("key"); ok {
		t.Error("Expected key to be expired")
	}
}

func TestPutWithTTL(t *testing.T) {
	cache := New[string, int](10)
	
	cache.PutWithTTL("key", 1, 100*time.Millisecond)
	
	// Should exist immediately
	if v, ok := cache.Get("key"); !ok || v != 1 {
		t.Errorf("Expected (1, true), got (%d, %v)", v, ok)
	}
	
	// Wait for TTL to expire
	time.Sleep(150 * time.Millisecond)
	
	// Should be expired
	if _, ok := cache.Get("key"); ok {
		t.Error("Expected key to be expired")
	}
}

func TestPurgeExpired(t *testing.T) {
	cache := New[string, int](10)
	
	cache.Put("a", 1)
	cache.PutWithTTL("b", 2, 100*time.Millisecond)
	cache.PutWithTTL("c", 3, 100*time.Millisecond)
	
	// Wait for TTL to expire
	time.Sleep(150 * time.Millisecond)
	
	count := cache.PurgeExpired()
	
	if count != 2 {
		t.Errorf("Expected 2 expired items, got %d", count)
	}
	
	if cache.Size() != 1 {
		t.Errorf("Expected size 1 after purge, got %d", cache.Size())
	}
}

func TestResize(t *testing.T) {
	cache := New[string, int](10)
	
	cache.Put("a", 1)
	cache.Put("b", 2)
	cache.Put("c", 3)
	
	// Resize to smaller capacity
	cache.Resize(2)
	
	if cache.Capacity() != 2 {
		t.Errorf("Expected capacity 2, got %d", cache.Capacity())
	}
	
	// Should have evicted items
	if cache.Size() > 2 {
		t.Errorf("Expected size <= 2, got %d", cache.Size())
	}
}

func TestForEach(t *testing.T) {
	cache := New[string, int](10)
	
	cache.Put("a", 1)
	cache.Put("b", 2)
	cache.Put("c", 3)
	
	count := 0
	cache.ForEach(func(key string, value int) bool {
		count++
		return true
	})
	
	if count != 3 {
		t.Errorf("Expected 3 iterations, got %d", count)
	}
}

func TestForEachStop(t *testing.T) {
	cache := New[string, int](10)
	
	cache.Put("a", 1)
	cache.Put("b", 2)
	cache.Put("c", 3)
	
	count := 0
	cache.ForEach(func(key string, value int) bool {
		count++
		return count < 2 // Stop after 2
	})
	
	if count != 2 {
		t.Errorf("Expected 2 iterations, got %d", count)
	}
}

func TestConcurrency(t *testing.T) {
	cache := New[int, int](100)
	var wg sync.WaitGroup
	
	// Concurrent writes
	for i := 0; i < 100; i++ {
		wg.Add(1)
		go func(n int) {
			defer wg.Done()
			cache.Put(n, n*10)
		}(i)
	}
	
	// Concurrent reads
	for i := 0; i < 100; i++ {
		wg.Add(1)
		go func(n int) {
			defer wg.Done()
			cache.Get(n)
		}(i)
	}
	
	wg.Wait()
	
	stats := cache.Stats()
	if stats.Size > 100 {
		t.Errorf("Cache size should not exceed capacity: %d", stats.Size)
	}
}

func TestFrequencyTracking(t *testing.T) {
	cache := New[string, int](10)
	
	cache.Put("key", 1)
	
	// Initial frequency is 1
	if freq, ok := cache.GetFrequency("key"); !ok || freq != 1 {
		t.Errorf("Expected initial frequency 1, got %d", freq)
	}
	
	// Each Get increments frequency
	cache.Get("key")
	cache.Get("key")
	cache.Get("key")
	
	if freq, ok := cache.GetFrequency("key"); !ok || freq != 4 {
		t.Errorf("Expected frequency 4, got %d", freq)
	}
}

func TestOnEvict(t *testing.T) {
	evicted := make(map[string]int)
	cache := NewWithConfig[string, int](Config{
		Capacity: 2,
		OnEvict: func(key any, value any) {
			evicted[key.(string)] = value.(int)
		},
	})
	
	cache.Put("a", 1)
	cache.Put("b", 2)
	cache.Put("c", 3) // Should evict "a"
	
	if len(evicted) != 1 {
		t.Errorf("Expected 1 eviction, got %d", len(evicted))
	}
	
	if _, ok := evicted["a"]; !ok {
		t.Error("Expected 'a' to be evicted")
	}
}

func TestString(t *testing.T) {
	cache := New[string, int](10)
	cache.Put("a", 1)
	cache.Get("a")
	cache.Get("missing")
	
	str := cache.String()
	
	if str == "" {
		t.Error("Expected non-empty string representation")
	}
}

func TestIntKeys(t *testing.T) {
	cache := New[int, string](10)
	
	cache.Put(1, "one")
	cache.Put(2, "two")
	cache.Put(3, "three")
	
	if v, ok := cache.Get(1); !ok || v != "one" {
		t.Errorf("Expected ('one', true), got (%s, %v)", v, ok)
	}
}

func TestStructValues(t *testing.T) {
	type Item struct {
		Name  string
		Value int
	}
	
	cache := New[string, Item](10)
	
	cache.Put("item1", Item{Name: "Test", Value: 42})
	
	v, ok := cache.Get("item1")
	if !ok || v.Name != "Test" || v.Value != 42 {
		t.Errorf("Expected (Item{Name: 'Test', Value: 42}, true), got (%v, %v)", v, ok)
	}
}

func BenchmarkPut(b *testing.B) {
	cache := New[int, int](10000)
	b.ResetTimer()
	
	for i := 0; i < b.N; i++ {
		cache.Put(i%10000, i)
	}
}

func BenchmarkGet(b *testing.B) {
	cache := New[int, int](10000)
	for i := 0; i < 10000; i++ {
		cache.Put(i, i)
	}
	b.ResetTimer()
	
	for i := 0; i < b.N; i++ {
		cache.Get(i % 10000)
	}
}

func BenchmarkConcurrentGet(b *testing.B) {
	cache := New[int, int](10000)
	for i := 0; i < 10000; i++ {
		cache.Put(i, i)
	}
	b.ResetTimer()
	
	b.RunParallel(func(pb *testing.PB) {
		i := 0
		for pb.Next() {
			cache.Get(i % 10000)
			i++
		}
	})
}

func BenchmarkConcurrentPut(b *testing.B) {
	cache := New[int, int](10000)
	b.ResetTimer()
	
	b.RunParallel(func(pb *testing.PB) {
		i := 0
		for pb.Next() {
			cache.Put(i%10000, i)
			i++
		}
	})
}