package skiplist_utils

import (
	"math/rand"
	"sort"
	"sync"
	"testing"
	"time"
)

func TestNewInt(t *testing.T) {
	sl := NewInt[string]()
	if sl == nil {
		t.Fatal("NewInt returned nil")
	}
	if sl.Length() != 0 {
		t.Errorf("Expected empty list, got length %d", sl.Length())
	}
	if !sl.IsEmpty() {
		t.Error("Expected IsEmpty to be true")
	}
}

func TestNewString(t *testing.T) {
	sl := NewString[int]()
	if sl == nil {
		t.Fatal("NewString returned nil")
	}
}

func TestInsertAndSearch(t *testing.T) {
	sl := NewInt[string]()

	sl.Insert(1, "one")
	sl.Insert(2, "two")
	sl.Insert(3, "three")

	if sl.Length() != 3 {
		t.Errorf("Expected length 3, got %d", sl.Length())
	}

	val, found := sl.Search(2)
	if !found {
		t.Error("Expected to find key 2")
	}
	if val != "two" {
		t.Errorf("Expected 'two', got '%s'", val)
	}

	_, found = sl.Search(99)
	if found {
		t.Error("Should not find key 99")
	}
}

func TestUpdate(t *testing.T) {
	sl := NewInt[string]()

	sl.Insert(1, "one")
	sl.Insert(1, "ONE")

	if sl.Length() != 1 {
		t.Errorf("Expected length 1 after update, got %d", sl.Length())
	}

	val, found := sl.Search(1)
	if !found {
		t.Error("Expected to find key 1")
	}
	if val != "ONE" {
		t.Errorf("Expected 'ONE', got '%s'", val)
	}
}

func TestDelete(t *testing.T) {
	sl := NewInt[string]()

	sl.Insert(1, "one")
	sl.Insert(2, "two")
	sl.Insert(3, "three")

	if !sl.Delete(2) {
		t.Error("Expected Delete to return true")
	}

	if sl.Length() != 2 {
		t.Errorf("Expected length 2, got %d", sl.Length())
	}

	_, found := sl.Search(2)
	if found {
		t.Error("Should not find deleted key")
	}

	if sl.Delete(99) {
		t.Error("Delete of non-existent key should return false")
	}
}

func TestMin(t *testing.T) {
	sl := NewInt[string]()

	_, _, found := sl.Min()
	if found {
		t.Error("Min on empty list should return false")
	}

	sl.Insert(5, "five")
	sl.Insert(2, "two")
	sl.Insert(8, "eight")
	sl.Insert(1, "one")

	key, val, found := sl.Min()
	if !found {
		t.Fatal("Expected to find min")
	}
	if key != 1 {
		t.Errorf("Expected min key 1, got %d", key)
	}
	if val != "one" {
		t.Errorf("Expected 'one', got '%s'", val)
	}
}

func TestMax(t *testing.T) {
	sl := NewInt[string]()

	_, _, found := sl.Max()
	if found {
		t.Error("Max on empty list should return false")
	}

	sl.Insert(5, "five")
	sl.Insert(2, "two")
	sl.Insert(8, "eight")
	sl.Insert(1, "one")

	key, val, found := sl.Max()
	if !found {
		t.Fatal("Expected to find max")
	}
	if key != 8 {
		t.Errorf("Expected max key 8, got %d", key)
	}
	if val != "eight" {
		t.Errorf("Expected 'eight', got '%s'", val)
	}
}

func TestRange(t *testing.T) {
	sl := NewInt[string]()

	for i := 0; i < 20; i++ {
		sl.Insert(i, string(rune('a'+i)))
	}

	results := sl.Range(5, 10)

	if len(results) != 6 {
		t.Errorf("Expected 6 results, got %d", len(results))
	}

	for i, r := range results {
		expectedKey := 5 + i
		if r.Key != expectedKey {
			t.Errorf("Expected key %d, got %d", expectedKey, r.Key)
		}
	}
}

func TestToSlice(t *testing.T) {
	sl := NewInt[string]()

	keys := []int{3, 1, 4, 1, 5, 9, 2, 6}
	for _, k := range keys {
		sl.Insert(k, string(rune('0'+k)))
	}

	slice := sl.ToSlice()

	// Check sorted order
	for i := 1; i < len(slice); i++ {
		if slice[i].Key <= slice[i-1].Key {
			t.Errorf("Slice not sorted: %d should be after %d", slice[i].Key, slice[i-1].Key)
		}
	}
}

func TestContains(t *testing.T) {
	sl := NewInt[string]()

	sl.Insert(1, "one")
	sl.Insert(2, "two")

	if !sl.Contains(1) {
		t.Error("Should contain 1")
	}
	if !sl.Contains(2) {
		t.Error("Should contain 2")
	}
	if sl.Contains(3) {
		t.Error("Should not contain 3")
	}
}

func TestGetOrInsert(t *testing.T) {
	sl := NewInt[string]()

	val := sl.GetOrInsert(1, "one")
	if val != "one" {
		t.Errorf("Expected 'one', got '%s'", val)
	}

	val = sl.GetOrInsert(1, "ONE")
	if val != "one" {
		t.Errorf("Expected existing 'one', got '%s'", val)
	}
}

func TestCount(t *testing.T) {
	sl := NewInt[int]()

	for i := 0; i < 10; i++ {
		sl.Insert(i, i*10)
	}

	count := sl.Count(func(key int, value int) bool {
		return key%2 == 0
	})

	if count != 5 {
		t.Errorf("Expected 5 even keys, got %d", count)
	}
}

func TestFindFirst(t *testing.T) {
	sl := NewInt[string]()

	sl.Insert(1, "apple")
	sl.Insert(2, "banana")
	sl.Insert(3, "cherry")

	_, val, found := sl.FindFirst(func(key int, value string) bool {
		return len(value) > 5
	})

	if !found {
		t.Error("Expected to find element")
	}
	if val != "banana" {
		t.Errorf("Expected 'banana', got '%s'", val)
	}
}

func TestLowerBound(t *testing.T) {
	sl := NewInt[string]()

	sl.Insert(1, "one")
	sl.Insert(3, "three")
	sl.Insert(5, "five")

	key, val, found := sl.LowerBound(2)
	if !found {
		t.Fatal("Expected to find element")
	}
	if key != 3 {
		t.Errorf("Expected key 3, got %d", key)
	}
	if val != "three" {
		t.Errorf("Expected 'three', got '%s'", val)
	}

	key, val, found = sl.LowerBound(3)
	if !found {
		t.Fatal("Expected to find element")
	}
	if key != 3 {
		t.Errorf("Expected key 3, got %d", key)
	}
}

func TestUpperBound(t *testing.T) {
	sl := NewInt[string]()

	sl.Insert(1, "one")
	sl.Insert(3, "three")
	sl.Insert(5, "five")

	key, val, found := sl.UpperBound(3)
	if !found {
		t.Fatal("Expected to find element")
	}
	if key != 5 {
		t.Errorf("Expected key 5, got %d", key)
	}
	if val != "five" {
		t.Errorf("Expected 'five', got '%s'", val)
	}
}

func TestRank(t *testing.T) {
	sl := NewInt[string]()

	sl.Insert(10, "ten")
	sl.Insert(20, "twenty")
	sl.Insert(30, "thirty")

	rank, found := sl.Rank(10)
	if !found {
		t.Fatal("Expected to find key 10")
	}
	if rank != 0 {
		t.Errorf("Expected rank 0, got %d", rank)
	}

	rank, found = sl.Rank(20)
	if !found {
		t.Fatal("Expected to find key 20")
	}
	if rank != 1 {
		t.Errorf("Expected rank 1, got %d", rank)
	}

	rank, found = sl.Rank(30)
	if !found {
		t.Fatal("Expected to find key 30")
	}
	if rank != 2 {
		t.Errorf("Expected rank 2, got %d", rank)
	}

	_, found = sl.Rank(99)
	if found {
		t.Error("Should not find rank for non-existent key")
	}
}

func TestGetByRank(t *testing.T) {
	sl := NewInt[string]()

	sl.Insert(10, "ten")
	sl.Insert(20, "twenty")
	sl.Insert(30, "thirty")

	key, val, found := sl.GetByRank(0)
	if !found {
		t.Fatal("Expected to find element at rank 0")
	}
	if key != 10 || val != "ten" {
		t.Errorf("Expected (10, ten), got (%d, %s)", key, val)
	}

	key, val, found = sl.GetByRank(2)
	if !found {
		t.Fatal("Expected to find element at rank 2")
	}
	if key != 30 || val != "thirty" {
		t.Errorf("Expected (30, thirty), got (%d, %s)", key, val)
	}

	_, _, found = sl.GetByRank(-1)
	if found {
		t.Error("Should not find element at negative rank")
	}

	_, _, found = sl.GetByRank(100)
	if found {
		t.Error("Should not find element at rank > length")
	}
}

func TestClear(t *testing.T) {
	sl := NewInt[string]()

	sl.Insert(1, "one")
	sl.Insert(2, "two")
	sl.Insert(3, "three")

	sl.Clear()

	if sl.Length() != 0 {
		t.Errorf("Expected length 0 after clear, got %d", sl.Length())
	}

	if !sl.IsEmpty() {
		t.Error("Expected IsEmpty after clear")
	}
}

func TestForEach(t *testing.T) {
	sl := NewInt[int]()

	for i := 0; i < 5; i++ {
		sl.Insert(i, i*10)
	}

	var keys []int
	sl.ForEach(func(key int, value int) bool {
		keys = append(keys, key)
		return true
	})

	if len(keys) != 5 {
		t.Errorf("Expected 5 keys, got %d", len(keys))
	}

	// Check sorted order
	if !sort.IntsAreSorted(keys) {
		t.Error("Keys should be in sorted order")
	}
}

func TestForEachEarlyStop(t *testing.T) {
	sl := NewInt[int]()

	for i := 0; i < 10; i++ {
		sl.Insert(i, i*10)
	}

	var count int
	sl.ForEach(func(key int, value int) bool {
		count++
		return key < 4 // Stop after key 4
	})

	if count != 5 {
		t.Errorf("Expected 5 iterations, got %d", count)
	}
}

func TestStringKeys(t *testing.T) {
	sl := NewString[int]()

	sl.Insert("banana", 1)
	sl.Insert("apple", 2)
	sl.Insert("cherry", 3)

	if sl.Length() != 3 {
		t.Errorf("Expected length 3, got %d", sl.Length())
	}

	val, found := sl.Search("apple")
	if !found {
		t.Error("Expected to find 'apple'")
	}
	if val != 2 {
		t.Errorf("Expected 2, got %d", val)
	}

	// Check sorted order
	slice := sl.ToSlice()
	if slice[0].Key != "apple" {
		t.Errorf("Expected first key 'apple', got '%s'", slice[0].Key)
	}
	if slice[2].Key != "cherry" {
		t.Errorf("Expected last key 'cherry', got '%s'", slice[2].Key)
	}
}

func TestFloat64Keys(t *testing.T) {
	sl := NewFloat64[string]()

	sl.Insert(1.5, "one point five")
	sl.Insert(2.5, "two point five")
	sl.Insert(0.5, "zero point five")

	if sl.Length() != 3 {
		t.Errorf("Expected length 3, got %d", sl.Length())
	}

	key, _, found := sl.Min()
	if !found {
		t.Fatal("Expected to find min")
	}
	if key != 0.5 {
		t.Errorf("Expected min key 0.5, got %f", key)
	}
}

func TestConcurrentInsert(t *testing.T) {
	sl := NewInt[int]()
	var wg sync.WaitGroup

	for i := 0; i < 100; i++ {
		wg.Add(1)
		go func(val int) {
			defer wg.Done()
			sl.Insert(val, val*10)
		}(i)
	}

	wg.Wait()

	if sl.Length() != 100 {
		t.Errorf("Expected length 100, got %d", sl.Length())
	}

	// Verify all values
	for i := 0; i < 100; i++ {
		val, found := sl.Search(i)
		if !found {
			t.Errorf("Expected to find key %d", i)
		}
		if val != i*10 {
			t.Errorf("Expected value %d, got %d", i*10, val)
		}
	}
}

func TestConcurrentReadWrite(t *testing.T) {
	sl := NewInt[int]()
	var wg sync.WaitGroup

	// Initial data
	for i := 0; i < 50; i++ {
		sl.Insert(i, i)
	}

	// Concurrent reads and writes
	for i := 0; i < 100; i++ {
		wg.Add(2)

		go func(val int) {
			defer wg.Done()
			sl.Insert(val, val)
		}(i + 100)

		go func(val int) {
			defer wg.Done()
			sl.Search(val % 50)
		}(i)
	}

	wg.Wait()

	// Verify consistency
	slice := sl.ToSlice()
	for i := 1; i < len(slice); i++ {
		if slice[i].Key <= slice[i-1].Key {
			t.Error("Concurrent operations broke sorted order")
			break
		}
	}
}

func TestLargeDataset(t *testing.T) {
	sl := NewInt[int]()

	// Insert 10000 random keys
	r := rand.New(rand.NewSource(42))
	keys := r.Perm(10000)

	for _, k := range keys {
		sl.Insert(k, k*100)
	}

	if sl.Length() != 10000 {
		t.Errorf("Expected length 10000, got %d", sl.Length())
	}

	// Verify all keys
	for _, k := range keys {
		val, found := sl.Search(k)
		if !found {
			t.Errorf("Expected to find key %d", k)
			continue
		}
		if val != k*100 {
			t.Errorf("Expected value %d, got %d", k*100, val)
		}
	}

	// Verify sorted order
	slice := sl.ToSlice()
	for i := 1; i < len(slice); i++ {
		if slice[i].Key <= slice[i-1].Key {
			t.Error("Slice not in sorted order")
			break
		}
	}
}

func TestRandomOperations(t *testing.T) {
	sl := NewInt[int]()
	reference := make(map[int]int)

	r := rand.New(rand.NewSource(time.Now().UnixNano()))

	for i := 0; i < 1000; i++ {
		op := r.Intn(3)
		key := r.Intn(100)

		switch op {
		case 0: // Insert
			value := r.Intn(1000)
			sl.Insert(key, value)
			reference[key] = value
		case 1: // Search
			val, found := sl.Search(key)
			refVal, refFound := reference[key]
			if found != refFound {
				t.Errorf("Search mismatch for key %d: skip list found=%v, map found=%v", key, found, refFound)
			}
			if found && val != refVal {
				t.Errorf("Value mismatch for key %d: got %d, expected %d", key, val, refVal)
			}
		case 2: // Delete
			deleted := sl.Delete(key)
			_, exists := reference[key]
			if deleted != exists {
				t.Errorf("Delete mismatch for key %d: skip list deleted=%v, map exists=%v", key, deleted, exists)
			}
			delete(reference, key)
		}
	}
}

func TestLevel(t *testing.T) {
	sl := NewInt[string]()

	// Level should be 0 for empty list
	if sl.Level() != 0 {
		t.Errorf("Expected level 0 for empty list, got %d", sl.Level())
	}

	// Insert many elements to increase level
	for i := 0; i < 1000; i++ {
		sl.Insert(i, string(rune('a'+i%26)))
	}

	// Level should have increased (probabilistically)
	// We don't assert exact value since it's random
	t.Logf("Level after 1000 inserts: %d", sl.Level())
}

func BenchmarkInsert(b *testing.B) {
	sl := NewInt[int]()
	for i := 0; i < b.N; i++ {
		sl.Insert(i, i*10)
	}
}

func BenchmarkSearch(b *testing.B) {
	sl := NewInt[int]()
	for i := 0; i < 10000; i++ {
		sl.Insert(i, i*10)
	}
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		sl.Search(i % 10000)
	}
}

func BenchmarkDelete(b *testing.B) {
	sl := NewInt[int]()
	for i := 0; i < b.N; i++ {
		sl.Insert(i, i*10)
	}
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		sl.Delete(i)
	}
}

func BenchmarkRange(b *testing.B) {
	sl := NewInt[int]()
	for i := 0; i < 10000; i++ {
		sl.Insert(i, i)
	}
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		sl.Range(1000, 2000)
	}
}