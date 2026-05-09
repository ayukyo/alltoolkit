package memoize_utils

import (
	"sync"
	"sync/atomic"
	"testing"
	"time"
)

// ============================================================================
// Entry Tests
// ============================================================================

func TestEntry_IsExpired(t *testing.T) {
	// Entry without expiration
	entry := &Entry[string]{Value: "test"}
	if entry.IsExpired() {
		t.Error("Entry without expiration should not be expired")
	}

	// Entry with future expiration
	entry = &Entry[string]{
		Value:     "test",
		ExpiresAt: time.Now().Add(1 * time.Hour),
	}
	if entry.IsExpired() {
		t.Error("Entry with future expiration should not be expired")
	}

	// Entry with past expiration
	entry = &Entry[string]{
		Value:     "test",
		ExpiresAt: time.Now().Add(-1 * time.Second),
	}
	if !entry.IsExpired() {
		t.Error("Entry with past expiration should be expired")
	}
}

func TestEntry_Age(t *testing.T) {
	entry := &Entry[string]{
		Value:     "test",
		CreatedAt: time.Now().Add(-5 * time.Second),
	}
	age := entry.Age()
	if age < 4*time.Second || age > 6*time.Second {
		t.Errorf("Expected age around 5 seconds, got %v", age)
	}
}

func TestEntry_TTL(t *testing.T) {
	// No TTL
	entry := &Entry[string]{Value: "test"}
	ttl := entry.TTL()
	if ttl != -1 {
		t.Errorf("Expected TTL -1 for no expiration, got %v", ttl)
	}

	// With TTL
	entry = &Entry[string]{
		Value:     "test",
		ExpiresAt: time.Now().Add(30 * time.Second),
	}
	ttl = entry.TTL()
	if ttl < 28*time.Second || ttl > 32*time.Second {
		t.Errorf("Expected TTL around 30 seconds, got %v", ttl)
	}

	// Expired
	entry = &Entry[string]{
		Value:     "test",
		ExpiresAt: time.Now().Add(-1 * time.Second),
	}
	ttl = entry.TTL()
	if ttl != 0 {
		t.Errorf("Expected TTL 0 for expired entry, got %v", ttl)
	}
}

// ============================================================================
// LRU Cache Tests
// ============================================================================

func TestLRUCache_SetGet(t *testing.T) {
	cache := NewLRUCache[string, int](WithMaxSize(100))

	cache.Set("a", 1)
	cache.Set("b", 2)
	cache.Set("c", 3)

	if val, ok := cache.Get("a"); !ok || val != 1 {
		t.Errorf("Expected (1, true), got (%d, %v)", val, ok)
	}
	if val, ok := cache.Get("b"); !ok || val != 2 {
		t.Errorf("Expected (2, true), got (%d, %v)", val, ok)
	}
	if val, ok := cache.Get("c"); !ok || val != 3 {
		t.Errorf("Expected (3, true), got (%d, %v)", val, ok)
	}
}

func TestLRUCache_Eviction(t *testing.T) {
	cache := NewLRUCache[string, int](WithMaxSize(3))

	cache.Set("a", 1)
	cache.Set("b", 2)
	cache.Set("c", 3)
	cache.Set("d", 4) // Should evict "a"

	if cache.Has("a") {
		t.Error("Key 'a' should have been evicted")
	}
	if !cache.Has("b") {
		t.Error("Key 'b' should still exist")
	}
}

func TestLRUCache_LRUEvictionOrder(t *testing.T) {
	cache := NewLRUCache[string, int](WithMaxSize(3))

	cache.Set("a", 1)
	cache.Set("b", 2)
	cache.Set("c", 3)

	// Access "a" to make it recently used
	cache.Get("a")

	// Add new entry, should evict "b" (oldest)
	cache.Set("d", 4)

	if !cache.Has("a") {
		t.Error("Key 'a' should still exist (recently accessed)")
	}
	if cache.Has("b") {
		t.Error("Key 'b' should have been evicted (oldest)")
	}
	if !cache.Has("c") {
		t.Error("Key 'c' should still exist")
	}
	if !cache.Has("d") {
		t.Error("Key 'd' should exist")
	}
}

func TestLRUCache_TTL(t *testing.T) {
	cache := NewLRUCache[string, int](WithTTL(100 * time.Millisecond))

	cache.Set("a", 1)

	// Should exist immediately
	if val, ok := cache.Get("a"); !ok || val != 1 {
		t.Error("Entry should exist immediately")
	}

	// Wait for expiration
	time.Sleep(150 * time.Millisecond)

	// Should be expired now
	if _, ok := cache.Get("a"); ok {
		t.Error("Entry should be expired")
	}
}

func TestLRUCache_SetWithTTL(t *testing.T) {
	cache := NewLRUCache[string, int]()

	cache.SetWithTTL("a", 1, 100*time.Millisecond)

	// Should exist
	if val, ok := cache.Get("a"); !ok || val != 1 {
		t.Error("Entry should exist")
	}

	// Wait for expiration
	time.Sleep(150 * time.Millisecond)

	if _, ok := cache.Get("a"); ok {
		t.Error("Entry should be expired")
	}
}

func TestLRUCache_Delete(t *testing.T) {
	cache := NewLRUCache[string, int]()

	cache.Set("a", 1)
	cache.Set("b", 2)

	cache.Delete("a")

	if cache.Has("a") {
		t.Error("Key 'a' should be deleted")
	}
	if !cache.Has("b") {
		t.Error("Key 'b' should still exist")
	}
}

func TestLRUCache_Clear(t *testing.T) {
	cache := NewLRUCache[string, int]()

	cache.Set("a", 1)
	cache.Set("b", 2)
	cache.Set("c", 3)

	cache.Clear()

	if cache.Size() != 0 {
		t.Errorf("Expected size 0, got %d", cache.Size())
	}
}

func TestLRUCache_Size(t *testing.T) {
	cache := NewLRUCache[string, int]()

	if cache.Size() != 0 {
		t.Errorf("Expected size 0, got %d", cache.Size())
	}

	cache.Set("a", 1)
	cache.Set("b", 2)

	if cache.Size() != 2 {
		t.Errorf("Expected size 2, got %d", cache.Size())
	}
}

func TestLRUCache_Keys(t *testing.T) {
	cache := NewLRUCache[string, int]()

	cache.Set("a", 1)
	cache.Set("b", 2)
	cache.Set("c", 3)

	keys := cache.Keys()
	if len(keys) != 3 {
		t.Errorf("Expected 3 keys, got %d", len(keys))
	}
}

func TestLRUCache_PurgeExpired(t *testing.T) {
	cache := NewLRUCache[string, int](WithTTL(100 * time.Millisecond))

	cache.Set("a", 1)
	cache.Set("b", 2)

	time.Sleep(150 * time.Millisecond)

	count := cache.PurgeExpired()
	if count != 2 {
		t.Errorf("Expected 2 purged entries, got %d", count)
	}

	if cache.Size() != 0 {
		t.Errorf("Expected size 0 after purge, got %d", cache.Size())
	}
}

func TestLRUCache_GetOrCompute(t *testing.T) {
	cache := NewLRUCache[string, int]()
	callCount := 0

	compute := func() (int, error) {
		callCount++
		return 42, nil
	}

	// First call should compute
	val, err := cache.GetOrCompute("a", compute)
	if err != nil || val != 42 {
		t.Errorf("Expected (42, nil), got (%d, %v)", val, err)
	}
	if callCount != 1 {
		t.Errorf("Expected 1 compute call, got %d", callCount)
	}

	// Second call should use cache
	val, err = cache.GetOrCompute("a", compute)
	if err != nil || val != 42 {
		t.Errorf("Expected (42, nil), got (%d, %v)", val, err)
	}
	if callCount != 1 {
		t.Errorf("Expected 1 compute call (cached), got %d", callCount)
	}
}

func TestLRUCache_EvictionCallback(t *testing.T) {
	evicted := make([]string, 0)
	cache := NewLRUCache[string, int](
		WithMaxSize(2),
		WithEvictionCallback(func(key string, value interface{}) {
			evicted = append(evicted, key)
		}),
	)

	cache.Set("a", 1)
	cache.Set("b", 2)
	cache.Set("c", 3) // Evicts "a"

	if len(evicted) != 1 || evicted[0] != "a" {
		t.Errorf("Expected evicted ['a'], got %v", evicted)
	}
}

func TestLRUCache_Stats(t *testing.T) {
	cache := NewLRUCache[string, int](WithStats(true))

	cache.Set("a", 1)
	cache.Get("a") // Hit
	cache.Get("b") // Miss

	stats := cache.GetStats()
	if stats.Hits != 1 {
		t.Errorf("Expected 1 hit, got %d", stats.Hits)
	}
	if stats.Misses != 1 {
		t.Errorf("Expected 1 miss, got %d", stats.Misses)
	}
	expectedRate := 50.0
	if stats.HitRate != expectedRate {
		t.Errorf("Expected hit rate %.2f%%, got %.2f%%", expectedRate, stats.HitRate)
	}
}

func TestLRUCache_Concurrent(t *testing.T) {
	cache := NewLRUCache[int, int](WithMaxSize(1000))
	var wg sync.WaitGroup

	// Concurrent writes
	for i := 0; i < 100; i++ {
		wg.Add(1)
		go func(n int) {
			defer wg.Done()
			for j := 0; j < 10; j++ {
				cache.Set(n*10+j, n*10+j)
			}
		}(i)
	}

	wg.Wait()

	// Concurrent reads
	for i := 0; i < 100; i++ {
		wg.Add(1)
		go func(n int) {
			defer wg.Done()
			for j := 0; j < 10; j++ {
				cache.Get(n*10 + j)
			}
		}(i)
	}

	wg.Wait()
}

// ============================================================================
// TTL Cache Tests
// ============================================================================

func TestTTLCache_SetGet(t *testing.T) {
	cache := NewTTLCache[string, int](1 * time.Hour)

	cache.Set("a", 1)
	cache.Set("b", 2)

	if val, ok := cache.Get("a"); !ok || val != 1 {
		t.Errorf("Expected (1, true), got (%d, %v)", val, ok)
	}
	if val, ok := cache.Get("b"); !ok || val != 2 {
		t.Errorf("Expected (2, true), got (%d, %v)", val, ok)
	}
}

func TestTTLCache_Expiration(t *testing.T) {
	cache := NewTTLCache[string, int](100 * time.Millisecond)

	cache.Set("a", 1)

	// Should exist
	if _, ok := cache.Get("a"); !ok {
		t.Error("Entry should exist")
	}

	// Wait for expiration
	time.Sleep(150 * time.Millisecond)

	// Should be expired
	if _, ok := cache.Get("a"); ok {
		t.Error("Entry should be expired")
	}
}

func TestTTLCache_SetWithCustomTTL(t *testing.T) {
	cache := NewTTLCache[string, int](1 * time.Hour) // Default TTL, but override

	cache.SetWithTTL("a", 1, 100*time.Millisecond)

	time.Sleep(150 * time.Millisecond)

	if _, ok := cache.Get("a"); ok {
		t.Error("Entry should be expired")
	}
}

func TestTTLCache_Delete(t *testing.T) {
	cache := NewTTLCache[string, int](1 * time.Hour)

	cache.Set("a", 1)
	cache.Delete("a")

	if _, ok := cache.Get("a"); ok {
		t.Error("Entry should be deleted")
	}
}

func TestTTLCache_Clear(t *testing.T) {
	cache := NewTTLCache[string, int](1 * time.Hour)

	cache.Set("a", 1)
	cache.Set("b", 2)
	cache.Clear()

	if cache.Size() != 0 {
		t.Errorf("Expected size 0, got %d", cache.Size())
	}
}

func TestTTLCache_PurgeExpired(t *testing.T) {
	cache := NewTTLCache[string, int](100 * time.Millisecond)

	cache.Set("a", 1)
	cache.Set("b", 2)

	time.Sleep(150 * time.Millisecond)

	count := cache.PurgeExpired()
	if count != 2 {
		t.Errorf("Expected 2 purged entries, got %d", count)
	}
}

func TestTTLCache_Stats(t *testing.T) {
	cache := NewTTLCache[string, int](1*time.Hour, WithStats(true))

	cache.Set("a", 1)
	cache.Get("a") // Hit
	cache.Get("b") // Miss

	stats := cache.GetStats()
	if stats.Hits != 1 {
		t.Errorf("Expected 1 hit, got %d", stats.Hits)
	}
	if stats.Misses != 1 {
		t.Errorf("Expected 1 miss, got %d", stats.Misses)
	}
}

// ============================================================================
// Memoize Function Tests
// ============================================================================

func TestMemoize1(t *testing.T) {
	callCount := atomic.Int32{}
	slowFn := func(n int) int {
		callCount.Add(1)
		time.Sleep(10 * time.Millisecond)
		return n * n
	}

	memoized := Memoize1(slowFn, WithMaxSize(100))

	// First call
	result1 := memoized(5)
	if result1 != 25 {
		t.Errorf("Expected 25, got %d", result1)
	}

	// Second call should use cache
	result2 := memoized(5)
	if result2 != 25 {
		t.Errorf("Expected 25, got %d", result2)
	}

	if callCount.Load() != 1 {
		t.Errorf("Expected 1 call, got %d", callCount.Load())
	}

	// Different argument should compute again
	result3 := memoized(6)
	if result3 != 36 {
		t.Errorf("Expected 36, got %d", result3)
	}

	if callCount.Load() != 2 {
		t.Errorf("Expected 2 calls, got %d", callCount.Load())
	}
}

func TestMemoize1Err(t *testing.T) {
	callCount := 0
	fn := func(n int) (int, error) {
		callCount++
		if n < 0 {
			return 0, &testError{msg: "negative"}
		}
		return n * 2, nil
	}

	memoized := Memoize1Err(fn)

	// Valid input
	val, err := memoized(5)
	if err != nil || val != 10 {
		t.Errorf("Expected (10, nil), got (%d, %v)", val, err)
	}

	// Cached
	val, err = memoized(5)
	if err != nil || val != 10 {
		t.Errorf("Expected (10, nil), got (%d, %v)", val, err)
	}
	if callCount != 1 {
		t.Errorf("Expected 1 call, got %d", callCount)
	}

	// Error input (should not cache)
	val, err = memoized(-1)
	if err == nil {
		t.Error("Expected error for negative input")
	}
}

func TestMemoize2(t *testing.T) {
	callCount := atomic.Int32{}
	fn := func(a, b int) int {
		callCount.Add(1)
		return a + b
	}

	memoized := Memoize2(fn, WithMaxSize(100))

	result1 := memoized(2, 3)
	if result1 != 5 {
		t.Errorf("Expected 5, got %d", result1)
	}

	result2 := memoized(2, 3)
	if result2 != 5 {
		t.Errorf("Expected 5, got %d", result2)
	}

	if callCount.Load() != 1 {
		t.Errorf("Expected 1 call, got %d", callCount.Load())
	}

	// Different args
	result3 := memoized(3, 4)
	if result3 != 7 {
		t.Errorf("Expected 7, got %d", result3)
	}

	if callCount.Load() != 2 {
		t.Errorf("Expected 2 calls, got %d", callCount.Load())
	}
}

func TestMemoize2Err(t *testing.T) {
	callCount := 0
	fn := func(a, b int) (int, error) {
		callCount++
		if b == 0 {
			return 0, &testError{msg: "division by zero"}
		}
		return a / b, nil
	}

	memoized := Memoize2Err(fn)

	// Valid
	val, err := memoized(10, 2)
	if err != nil || val != 5 {
		t.Errorf("Expected (5, nil), got (%d, %v)", val, err)
	}

	// Cached
	val, err = memoized(10, 2)
	if err != nil || val != 5 {
		t.Errorf("Expected (5, nil), got (%d, %v)", val, err)
	}
	if callCount != 1 {
		t.Errorf("Expected 1 call, got %d", callCount)
	}

	// Error (not cached)
	val, err = memoized(10, 0)
	if err == nil {
		t.Error("Expected error for division by zero")
	}
	if callCount != 2 {
		t.Errorf("Expected 2 calls, got %d", callCount)
	}
}

func TestMemoize_WithTTL(t *testing.T) {
	callCount := atomic.Int32{}
	fn := func(n int) int {
		callCount.Add(1)
		return n * n
	}

	memoized := Memoize1(fn, WithTTL(100*time.Millisecond))

	// First call
	memoized(5)
	if callCount.Load() != 1 {
		t.Errorf("Expected 1 call, got %d", callCount.Load())
	}

	// Cached
	memoized(5)
	if callCount.Load() != 1 {
		t.Errorf("Expected 1 call (cached), got %d", callCount.Load())
	}

	// Wait for expiration
	time.Sleep(150 * time.Millisecond)

	// Should recompute
	memoized(5)
	if callCount.Load() != 2 {
		t.Errorf("Expected 2 calls (after expiration), got %d", callCount.Load())
	}
}

// Helper type for error testing
type testError struct {
	msg string
}

func (e *testError) Error() string {
	return e.msg
}

// ============================================================================
// Utility Function Tests
// ============================================================================

func TestExpiredEntries(t *testing.T) {
	m := map[string]*Entry[int]{
		"a": {Value: 1, ExpiresAt: time.Now().Add(1 * time.Hour)},
		"b": {Value: 2, ExpiresAt: time.Now().Add(-1 * time.Second)},
		"c": {Value: 3, ExpiresAt: time.Now().Add(1 * time.Hour)},
		"d": {Value: 4, ExpiresAt: time.Now().Add(-1 * time.Second)},
	}

	count := ExpiredEntries(m)
	if count != 2 {
		t.Errorf("Expected 2 expired entries, got %d", count)
	}
}

func TestPurgeMap(t *testing.T) {
	m := map[string]*Entry[int]{
		"a": {Value: 1, ExpiresAt: time.Now().Add(1 * time.Hour)},
		"b": {Value: 2, ExpiresAt: time.Now().Add(-1 * time.Second)},
		"c": {Value: 3, ExpiresAt: time.Now().Add(1 * time.Hour)},
	}

	count := PurgeMap(m)
	if count != 1 {
		t.Errorf("Expected 1 purged entry, got %d", count)
	}
	if len(m) != 2 {
		t.Errorf("Expected 2 remaining entries, got %d", len(m))
	}
}

// ============================================================================
// Edge Case Tests
// ============================================================================

func TestLRUCache_UpdateExisting(t *testing.T) {
	cache := NewLRUCache[string, int]()

	cache.Set("a", 1)
	cache.Set("a", 2)
	cache.Set("a", 3)

	if cache.Size() != 1 {
		t.Errorf("Expected size 1, got %d", cache.Size())
	}

	if val, ok := cache.Get("a"); !ok || val != 3 {
		t.Errorf("Expected (3, true), got (%d, %v)", val, ok)
	}
}

func TestLRUCache_MaxSizeZero(t *testing.T) {
	cache := NewLRUCache[string, int](WithMaxSize(0)) // No limit

	for i := 0; i < 100; i++ {
		cache.Set(string(rune('a'+i%26)), i)
	}

	if cache.Size() != 26 {
		t.Errorf("Expected size 26 (no eviction), got %d", cache.Size())
	}
}

func TestLRUCache_AccessCount(t *testing.T) {
	cache := NewLRUCache[string, int](WithMaxSize(10))

	cache.Set("a", 1)

	// Multiple accesses
	for i := 0; i < 5; i++ {
		cache.Get("a")
	}

	// Check internal entry
	elem := cache.items["a"]
	entry := elem.Value.(*lruEntry[string, int]).entry

	if entry.AccessCount != 6 { // 1 initial + 5 gets
		t.Errorf("Expected access count 6, got %d", entry.AccessCount)
	}
}

// Benchmark tests
func BenchmarkLRUCache_Set(b *testing.B) {
	cache := NewLRUCache[int, int](WithMaxSize(10000))
	for i := 0; i < b.N; i++ {
		cache.Set(i, i)
	}
}

func BenchmarkLRUCache_Get(b *testing.B) {
	cache := NewLRUCache[int, int](WithMaxSize(10000))
	for i := 0; i < 10000; i++ {
		cache.Set(i, i)
	}
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		cache.Get(i % 10000)
	}
}

func BenchmarkLRUCache_Concurrent(b *testing.B) {
	cache := NewLRUCache[int, int](WithMaxSize(10000))
	var wg sync.WaitGroup
	
	for i := 0; i < b.N; i++ {
		wg.Add(1)
		go func(n int) {
			defer wg.Done()
			cache.Set(n, n)
			cache.Get(n)
		}(i % 1000)
	}
	wg.Wait()
}