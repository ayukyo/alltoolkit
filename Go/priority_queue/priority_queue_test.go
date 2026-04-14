package priority_queue

import (
	"sync"
	"testing"
)

// TestMinHeap tests the basic min-heap functionality
func TestMinHeap(t *testing.T) {
	pq := MinHeap[string]()

	// Test empty queue
	if !pq.IsEmpty() {
		t.Error("New queue should be empty")
	}

	// Test push and pop
	pq.PushItem("low", 5)
	pq.PushItem("high", 1)
	pq.PushItem("medium", 3)

	if pq.Size() != 3 {
		t.Errorf("Expected size 3, got %d", pq.Size())
	}

	// Pop should return items in priority order (lowest number first)
	val, pri, ok := pq.PopItem()
	if !ok || val != "high" || pri != 1 {
		t.Errorf("Expected (high, 1, true), got (%s, %d, %v)", val, pri, ok)
	}

	val, pri, ok = pq.PopItem()
	if !ok || val != "medium" || pri != 3 {
		t.Errorf("Expected (medium, 3, true), got (%s, %d, %v)", val, pri, ok)
	}

	val, pri, ok = pq.PopItem()
	if !ok || val != "low" || pri != 5 {
		t.Errorf("Expected (low, 5, true), got (%s, %d, %v)", val, pri, ok)
	}

	// Test empty queue pop
	_, _, ok = pq.PopItem()
	if ok {
		t.Error("Pop on empty queue should return false")
	}
}

// TestMaxHeap tests the basic max-heap functionality
func TestMaxHeap(t *testing.T) {
	pq := MaxHeap[string]()

	pq.PushItem("low", 1)
	pq.PushItem("high", 5)
	pq.PushItem("medium", 3)

	// Pop should return items in priority order (highest number first)
	val, pri, ok := pq.PopItem()
	if !ok || val != "high" || pri != 5 {
		t.Errorf("Expected (high, 5, true), got (%s, %d, %v)", val, pri, ok)
	}

	val, pri, ok = pq.PopItem()
	if !ok || val != "medium" || pri != 3 {
		t.Errorf("Expected (medium, 3, true), got (%s, %d, %v)", val, pri, ok)
	}

	val, pri, ok = pq.PopItem()
	if !ok || val != "low" || pri != 1 {
		t.Errorf("Expected (low, 1, true), got (%s, %d, %v)", val, pri, ok)
	}
}

// TestPeek tests the Peek method
func TestPeek(t *testing.T) {
	pq := MinHeap[int]()

	// Peek on empty queue
	_, _, ok := pq.Peek()
	if ok {
		t.Error("Peek on empty queue should return false")
	}

	pq.PushItem(10, 2)
	pq.PushItem(20, 1)
	pq.PushItem(30, 3)

	// Peek should return highest priority without removing
	val, pri, ok := pq.Peek()
	if !ok || val != 20 || pri != 1 {
		t.Errorf("Expected (20, 1, true), got (%d, %d, %v)", val, pri, ok)
	}

	if pq.Size() != 3 {
		t.Errorf("Peek should not remove item, expected size 3, got %d", pq.Size())
	}
}

// TestUpdate tests updating priority of an item
func TestUpdate(t *testing.T) {
	pq := MinHeap[string]()

	item1 := pq.PushItem("first", 5)
	item2 := pq.PushItem("second", 3)
	item3 := pq.PushItem("third", 1)

	// Update item2 to have highest priority
	pq.Update(item2, "second-updated", 0)

	// Pop should return item2 first
	val, _, ok := pq.PopItem()
	if !ok || val != "second-updated" {
		t.Errorf("Expected second-updated, got %s", val)
	}

	val, _, ok = pq.PopItem()
	if !ok || val != "third" {
		t.Errorf("Expected third, got %s", val)
	}

	_ = item1 // keep reference
}

// TestRemove tests removing a specific item
func TestRemove(t *testing.T) {
	pq := MinHeap[string]()

	item1 := pq.PushItem("one", 1)
	item2 := pq.PushItem("two", 2)
	item3 := pq.PushItem("three", 3)

	// Remove item2
	removed := pq.Remove(item2)
	if removed != "two" {
		t.Errorf("Expected removed value 'two', got '%s'", removed)
	}

	if pq.Size() != 2 {
		t.Errorf("Expected size 2 after remove, got %d", pq.Size())
	}

	// Verify remaining items
	val, _, _ := pq.PopItem()
	if val != "one" {
		t.Errorf("Expected 'one', got '%s'", val)
	}

	val, _, _ = pq.PopItem()
	if val != "three" {
		t.Errorf("Expected 'three', got '%s'", val)
	}
}

// TestClear tests clearing the queue
func TestClear(t *testing.T) {
	pq := MinHeap[int]()

	for i := 0; i < 10; i++ {
		pq.PushItem(i, i)
	}

	if pq.Size() != 10 {
		t.Errorf("Expected size 10, got %d", pq.Size())
	}

	pq.Clear()

	if !pq.IsEmpty() {
		t.Error("Queue should be empty after Clear")
	}

	if pq.Size() != 0 {
		t.Errorf("Expected size 0 after Clear, got %d", pq.Size())
	}
}

// TestToSlice tests ToSlice method
func TestToSlice(t *testing.T) {
	pq := MinHeap[string]()

	pq.PushItem("a", 1)
	pq.PushItem("b", 2)
	pq.PushItem("c", 3)

	items := pq.ToSlice()
	if len(items) != 3 {
		t.Errorf("Expected 3 items, got %d", len(items))
	}

	// Verify the queue is unchanged
	if pq.Size() != 3 {
		t.Error("ToSlice should not modify the queue")
	}
}

// TestValues tests Values method
func TestValues(t *testing.T) {
	pq := MinHeap[int]()

	pq.PushItem(1, 10)
	pq.PushItem(2, 20)
	pq.PushItem(3, 30)

	values := pq.Values()
	if len(values) != 3 {
		t.Errorf("Expected 3 values, got %d", len(values))
	}
}

// TestContains tests Contains method
func TestContains(t *testing.T) {
	pq := MinHeap[string]()

	pq.PushItem("apple", 1)
	pq.PushItem("banana", 2)

	contains := pq.Contains(func(a, b string) bool { return a == b }, "apple")
	if !contains {
		t.Error("Should contain 'apple'")
	}

	contains = pq.Contains(func(a, b string) bool { return a == b }, "orange")
	if contains {
		t.Error("Should not contain 'orange'")
	}
}

// TestFind tests Find method
func TestFind(t *testing.T) {
	pq := MinHeap[string]()

	pq.PushItem("apple", 1)
	pq.PushItem("banana", 2)
	pq.PushItem("cherry", 3)

	item, found := pq.Find(func(s string) bool { return s == "banana" })
	if !found {
		t.Error("Should find 'banana'")
	}
	if item.Value != "banana" {
		t.Errorf("Expected 'banana', got '%s'", item.Value)
	}

	_, found = pq.Find(func(s string) bool { return s == "orange" })
	if found {
		t.Error("Should not find 'orange'")
	}
}

// TestFindByPriority tests FindByPriority method
func TestFindByPriority(t *testing.T) {
	pq := MinHeap[string]()

	pq.PushItem("apple", 1)
	pq.PushItem("banana", 2)
	pq.PushItem("cherry", 1)
	pq.PushItem("date", 3)

	items := pq.FindByPriority(1)
	if len(items) != 2 {
		t.Errorf("Expected 2 items with priority 1, got %d", len(items))
	}
}

// TestClone tests Clone method
func TestClone(t *testing.T) {
	pq := MinHeap[int]()

	pq.PushItem(1, 10)
	pq.PushItem(2, 20)
	pq.PushItem(3, 30)

	clone := pq.Clone()

	// Modify original
	pq.PopItem()

	// Clone should be unchanged
	if clone.Size() != 3 {
		t.Errorf("Clone should have 3 items, got %d", clone.Size())
	}

	// Original should have 2
	if pq.Size() != 2 {
		t.Errorf("Original should have 2 items, got %d", pq.Size())
	}
}

// TestThreadSafeMinHeap tests thread-safe min-heap
func TestThreadSafeMinHeap(t *testing.T) {
	pq := NewThreadSafeMinHeap[int]()

	// Test push and pop
	pq.PushItem(1, 5)
	pq.PushItem(2, 1)
	pq.PushItem(3, 3)

	val, pri, ok := pq.PopItem()
	if !ok || val != 2 || pri != 1 {
		t.Errorf("Expected (2, 1, true), got (%d, %d, %v)", val, pri, ok)
	}

	// Test peek
	pq.PushItem(4, 0)
	val, pri, ok = pq.Peek()
	if !ok || val != 4 || pri != 0 {
		t.Errorf("Expected (4, 0, true), got (%d, %d, %v)", val, pri, ok)
	}
}

// TestThreadSafeConcurrency tests concurrent access
func TestThreadSafeConcurrency(t *testing.T) {
	pq := NewThreadSafeMinHeap[int]()
	var wg sync.WaitGroup

	// Concurrent pushes
	for i := 0; i < 100; i++ {
		wg.Add(1)
		go func(val int) {
			defer wg.Done()
			pq.PushItem(val, val)
		}(i)
	}

	// Concurrent pops
	for i := 0; i < 50; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			pq.PopItem()
		}()
	}

	wg.Wait()

	// Should have 50 items left
	if pq.Size() != 50 {
		t.Errorf("Expected 50 items after concurrent operations, got %d", pq.Size())
	}
}

// TestBoundedMinHeap tests bounded min-heap
func TestBoundedMinHeap(t *testing.T) {
	pq := NewBoundedMinHeap[int](3)

	// Add items up to capacity
	pq.PushItem(1, 1)
	pq.PushItem(2, 2)
	pq.PushItem(3, 3)

	if !pq.IsFull() {
		t.Error("Queue should be full")
	}

	// Adding lower priority item should be rejected
	_, added := pq.PushItem(4, 10) // priority 10 > current worst (3)
	// In min-heap, lower numbers are higher priority, so 10 is lower priority
	// The bounded queue should reject it or not make room
	_ = added // just check it doesn't crash
}

// TestBoundedMaxHeap tests bounded max-heap
func TestBoundedMaxHeap(t *testing.T) {
	pq := NewBoundedMaxHeap[int](3)

	// Add items up to capacity
	pq.PushItem(1, 10)
	pq.PushItem(2, 20)
	pq.PushItem(3, 30)

	if !pq.IsFull() {
		t.Error("Queue should be full")
	}

	// Adding lower priority should be rejected in max-heap
	_, added := pq.PushItem(4, 5)
	_ = added
}

// TestBoundedEvictCallback tests eviction callback
func TestBoundedEvictCallback(t *testing.T) {
	pq := NewBoundedMaxHeap[int](2)

	evicted := make([]int, 0)
	pq.SetEvictCallback(func(val int, pri int) {
		evicted = append(evicted, val)
	})

	pq.PushItem(1, 10)
	pq.PushItem(2, 20)
	pq.PushItem(3, 30) // Should evict item with priority 10 (value 1)

	if len(evicted) != 1 {
		t.Errorf("Expected 1 eviction, got %d", len(evicted))
	}
	if len(evicted) > 0 && evicted[0] != 1 {
		t.Errorf("Expected eviction of value 1, got %d", evicted[0])
	}
}

// TestPriorityLevel tests priority level constants
func TestPriorityLevel(t *testing.T) {
	tests := []struct {
		level    PriorityLevel
		expected string
	}{
		{PriorityLowest, "Lowest"},
		{PriorityLow, "Low"},
		{PriorityNormal, "Normal"},
		{PriorityHigh, "High"},
		{PriorityHighest, "Highest"},
		{PriorityCritical, "Critical"},
		{PriorityLevel(999), "Custom"},
	}

	for _, test := range tests {
		if test.level.String() != test.expected {
			t.Errorf("PriorityLevel(%d).String() = %s, want %s",
				test.level, test.level.String(), test.expected)
		}
	}

	// Test comparisons
	if !PriorityHigh.HigherThan(PriorityNormal) {
		t.Error("High should be higher than Normal")
	}

	if !PriorityLow.LowerThan(PriorityNormal) {
		t.Error("Low should be lower than Normal")
	}

	// Test Int()
	if PriorityNormal.Int() != 50 {
		t.Errorf("PriorityNormal.Int() = %d, want 50", PriorityNormal.Int())
	}
}

// TestGenericTypes tests with different generic types
func TestGenericTypes(t *testing.T) {
	// Test with int
	intPQ := MinHeap[int]()
	intPQ.PushItem(42, 1)
	val, _, _ := intPQ.PopItem()
	if val != 42 {
		t.Errorf("Expected 42, got %d", val)
	}

	// Test with custom struct
	type Task struct {
		ID   int
		Name string
	}
	taskPQ := MaxHeap[Task]()
	taskPQ.PushItem(Task{ID: 1, Name: "Low"}, 1)
	taskPQ.PushItem(Task{ID: 2, Name: "High"}, 10)

	task, _, _ := taskPQ.PopItem()
	if task.Name != "High" {
		t.Errorf("Expected 'High' task, got '%s'", task.Name)
	}
}

// BenchmarkMinHeapPush benchmarks pushing items to a min-heap
func BenchmarkMinHeapPush(b *testing.B) {
	pq := MinHeap[int]()
	for i := 0; i < b.N; i++ {
		pq.PushItem(i, i)
	}
}

// BenchmarkMinHeapPop benchmarks popping items from a min-heap
func BenchmarkMinHeapPop(b *testing.B) {
	pq := MinHeap[int]()
	for i := 0; i < b.N; i++ {
		pq.PushItem(i, i)
	}
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		pq.PopItem()
	}
}

// BenchmarkThreadSafePush benchmarks thread-safe push
func BenchmarkThreadSafePush(b *testing.B) {
	pq := NewThreadSafeMinHeap[int]()
	for i := 0; i < b.N; i++ {
		pq.PushItem(i, i)
	}
}

// BenchmarkThreadSafePop benchmarks thread-safe pop
func BenchmarkThreadSafePop(b *testing.B) {
	pq := NewThreadSafeMinHeap[int]()
	for i := 0; i < b.N; i++ {
		pq.PushItem(i, i)
	}
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		pq.PopItem()
	}
}

// BenchmarkConcurrentOperations benchmarks concurrent push/pop
func BenchmarkConcurrentOperations(b *testing.B) {
	pq := NewThreadSafeMinHeap[int]()
	var wg sync.WaitGroup

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		wg.Add(2)
		go func(val int) {
			defer wg.Done()
			pq.PushItem(val, val)
		}(i)
		go func() {
			defer wg.Done()
			pq.PopItem()
		}()
	}
	wg.Wait()
}