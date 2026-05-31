package lfu_cache_utils

import (
	"fmt"
	"sync"
	"testing"
	"time"
)

func TestNew(t *testing.T) {
	cache := New(3)
	if cache.capacity != 3 {
		t.Errorf("expected capacity 3, got %d", cache.capacity)
	}
	if cache.Len() != 0 {
		t.Errorf("expected empty cache, got %d items", cache.Len())
	}
}

func TestNewZeroCapacity(t *testing.T) {
	cache := New(0)
	if cache.capacity != 128 {
		t.Errorf("expected default capacity 128, got %d", cache.capacity)
	}
}

func TestSetGet(t *testing.T) {
	cache := New(3)

	cache.Set("a", 1)
	cache.Set("b", 2)
	cache.Set("c", 3)

	v, ok := cache.Get("a")
	if !ok || v != 1 {
		t.Errorf("expected Get(a)=1, got %v, ok=%v", v, ok)
	}

	v, ok = cache.Get("b")
	if !ok || v != 2 {
		t.Errorf("expected Get(b)=2, got %v, ok=%v", v, ok)
	}

	v, ok = cache.Get("c")
	if !ok || v != 3 {
		t.Errorf("expected Get(c)=3, got %v, ok=%v", v, ok)
	}
}

func TestGetNonExistent(t *testing.T) {
	cache := New(3)

	v, ok := cache.Get("nonexistent")
	if ok || v != nil {
		t.Errorf("expected nil, ok=false, got %v, ok=%v", v, ok)
	}
}

func TestEviction(t *testing.T) {
	cache := New(3)

	cache.Set("a", 1)
	cache.Set("b", 2)
	cache.Set("c", 3)

	// "a" accessed once
	cache.Get("a")

	// Add "d", should evict "b" (least frequently used)
	cache.Set("d", 4)

	_, aExists := cache.Get("a")
	_, bExists := cache.Get("b")
	_, cExists := cache.Get("c")
	_, dExists := cache.Get("d")

	if !aExists {
		t.Error("'a' should still exist after eviction")
	}
	if bExists {
		t.Error("'b' should have been evicted")
	}
	if !cExists {
		t.Error("'c' should still exist after eviction")
	}
	if !dExists {
		t.Error("'d' should exist")
	}
}

func TestFrequencyIncrement(t *testing.T) {
	cache := New(3)

	cache.Set("a", 1)
	cache.Set("b", 2)

	cache.Get("a")
	cache.Get("a")
	cache.Get("b")

	// "a" accessed 3 times (1 set + 2 get), "b" accessed 2 times
	freqA, _ := cache.Frequency("a")
	freqB, _ := cache.Frequency("b")

	if freqA != 3 {
		t.Errorf("expected freq(a)=3, got %d", freqA)
	}
	if freqB != 2 {
		t.Errorf("expected freq(b)=2, got %d", freqB)
	}
}

func TestDelete(t *testing.T) {
	cache := New(3)

	cache.Set("a", 1)
	cache.Set("b", 2)

	deleted := cache.Delete("a")
	if !deleted {
		t.Error("expected Delete(a) to return true")
	}

	_, ok := cache.Get("a")
	if ok {
		t.Error("'a' should not exist after deletion")
	}

	v, ok := cache.Get("b")
	if !ok || v != 2 {
		t.Errorf("expected Get(b)=2, got %v, ok=%v", v, ok)
	}
}

func TestDeleteNonExistent(t *testing.T) {
	cache := New(3)

	deleted := cache.Delete("nonexistent")
	if deleted {
		t.Error("expected Delete(nonexistent) to return false")
	}
}

func TestClear(t *testing.T) {
	cache := New(3)

	cache.Set("a", 1)
	cache.Set("b", 2)
	cache.Set("c", 3)

	cache.Clear()

	if cache.Len() != 0 {
		t.Errorf("expected empty cache, got %d items", cache.Len())
	}

	_, ok := cache.Get("a")
	if ok {
		t.Error("'a' should not exist after Clear()")
	}
}

func TestContains(t *testing.T) {
	cache := New(3)

	cache.Set("a", 1)

	if !cache.Contains("a") {
		t.Error("'a' should be contained")
	}

	if cache.Contains("b") {
		t.Error("'b' should not be contained")
	}
}

func TestTTL(t *testing.T) {
	cache := NewWithTTL(3, 50*time.Millisecond)

	cache.Set("a", 1)

	if !cache.Contains("a") {
		t.Error("'a' should be contained immediately")
	}

	time.Sleep(60 * time.Millisecond)

	if cache.Contains("a") {
		t.Error("'a' should have expired")
	}
}

func TestSetWithTTL(t *testing.T) {
	cache := New(3)

	cache.SetWithTTL("a", 1, 50*time.Millisecond)
	cache.SetWithTTL("b", 2, 100*time.Millisecond)

	time.Sleep(60 * time.Millisecond)

	if cache.Contains("a") {
		t.Error("'a' should have expired")
	}

	if !cache.Contains("b") {
		t.Error("'b' should still be valid")
	}
}

func TestEvictCallback(t *testing.T) {
	evicted := make(map[string]interface{})
	callback := func(key string, value interface{}) {
		evicted[key] = value
	}

	cache := NewWithEvict(2, callback)

	cache.Set("a", 1)
	cache.Set("b", 2)
	cache.Set("c", 3) // should evict "a"

	if len(evicted) != 1 {
		t.Errorf("expected 1 eviction, got %d", len(evicted))
	}

	if evicted["a"] != 1 {
		t.Errorf("expected evicted[a]=1, got %v", evicted["a"])
	}
}

func TestCleanup(t *testing.T) {
	cache := New(3)

	cache.SetWithTTL("a", 1, 30*time.Millisecond)
	cache.SetWithTTL("b", 2, 60*time.Millisecond)
	cache.Set("c", 3)

	time.Sleep(40 * time.Millisecond)

	removed := cache.Cleanup()

	if removed != 1 {
		t.Errorf("expected 1 cleanup, got %d", removed)
	}

	if cache.Len() != 2 {
		t.Errorf("expected 2 items, got %d", cache.Len())
	}
}

func TestKeys(t *testing.T) {
	cache := New(3)

	cache.Set("a", 1)
	cache.Set("b", 2)
	cache.Set("c", 3)

	keys := cache.Keys()

	if len(keys) != 3 {
		t.Errorf("expected 3 keys, got %d", len(keys))
	}

	keyMap := make(map[string]bool)
	for _, k := range keys {
		keyMap[k] = true
	}

	for _, k := range []string{"a", "b", "c"} {
		if !keyMap[k] {
			t.Errorf("expected key %q to be in keys", k)
		}
	}
}

func TestStats(t *testing.T) {
	cache := New(3)

	cache.Set("a", 1)
	cache.Set("b", 2)
	cache.Get("a")
	cache.Get("a")
	cache.Get("b")

	stats := cache.Stats()

	if stats["capacity"] != 3 {
		t.Errorf("expected capacity=3, got %v", stats["capacity"])
	}

	if stats["size"] != 2 {
		t.Errorf("expected size=2, got %v", stats["size"])
	}
}

func TestResize(t *testing.T) {
	cache := New(5)

	for i := 0; i < 5; i++ {
		cache.Set(fmt.Sprintf("key%d", i), i)
	}

	cache.Resize(2)

	if cache.Len() != 2 {
		t.Errorf("expected 2 items, got %d", cache.Len())
	}
}

func TestUpdate(t *testing.T) {
	cache := New(3)

	cache.Set("a", 1)
	cache.Set("a", 100)

	v, ok := cache.Get("a")
	if !ok || v != 100 {
		t.Errorf("expected Get(a)=100, got %v, ok=%v", v, ok)
	}
}

func TestTouch(t *testing.T) {
	cache := New(3)

	cache.Set("a", 1)
	cache.Get("a")
	cache.Get("a")

	freqBefore, _ := cache.Frequency("a")
	cache.Touch("a")
	freqAfter, _ := cache.Frequency("a")

	if freqAfter <= freqBefore {
		t.Errorf("expected frequency to increase after Touch, before=%d, after=%d", freqBefore, freqAfter)
	}
}

func TestGetMulti(t *testing.T) {
	cache := New(3)

	cache.Set("a", 1)
	cache.Set("b", 2)
	cache.Set("c", 3)

	results := cache.GetMulti([]string{"a", "b", "nonexistent"})

	if len(results) != 2 {
		t.Errorf("expected 2 results, got %d", len(results))
	}

	if results["a"] != 1 {
		t.Errorf("expected results[a]=1, got %v", results["a"])
	}

	if results["b"] != 2 {
		t.Errorf("expected results[b]=2, got %v", results["b"])
	}
}

func TestSetMulti(t *testing.T) {
	cache := New(3)

	items := map[string]interface{}{
		"x": 1,
		"y": 2,
		"z": 3,
	}

	cache.SetMulti(items)

	if cache.Len() != 3 {
		t.Errorf("expected 3 items, got %d", cache.Len())
	}
}

func TestConcurrency(t *testing.T) {
	cache := New(1000)

	var wg sync.WaitGroup
	wg.Add(4)

	go func() {
		defer wg.Done()
		for i := 0; i < 250; i++ {
			cache.Set(fmt.Sprintf("key%d", i), i)
		}
	}()

	go func() {
		defer wg.Done()
		for i := 250; i < 500; i++ {
			cache.Set(fmt.Sprintf("key%d", i), i)
		}
	}()

	go func() {
		defer wg.Done()
		for i := 0; i < 250; i++ {
			cache.Get(fmt.Sprintf("key%d", i))
		}
	}()

	go func() {
		defer wg.Done()
		for i := 250; i < 500; i++ {
			cache.Get(fmt.Sprintf("key%d", i))
		}
	}()

	wg.Wait()

	if cache.Len() > 1000 {
		t.Errorf("cache size exceeds capacity: %d", cache.Len())
	}
}

func TestString(t *testing.T) {
	cache := New(10)
	cache.Set("a", 1)

	str := cache.String()
	if str == "" {
		t.Error("expected non-empty string representation")
	}
}
