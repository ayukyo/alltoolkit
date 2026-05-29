package priorityqueue

import (
	"math"
	"testing"
)

// ============================================================================
// Basic Operations Tests
// ============================================================================

func TestNewPriorityQueue(t *testing.T) {
	pq := NewPriorityQueue()
	if pq == nil {
		t.Fatal("NewPriorityQueue returned nil")
	}
	if pq.Len() != 0 {
		t.Errorf("Expected empty queue, got length %d", pq.Len())
	}
	if pq.isMaxHeap {
		t.Error("NewPriorityQueue should create min-heap")
	}
}

func TestNewMaxPriorityQueue(t *testing.T) {
	pq := NewMaxPriorityQueue()
	if pq == nil {
		t.Fatal("NewMaxPriorityQueue returned nil")
	}
	if !pq.isMaxHeap {
		t.Error("NewMaxPriorityQueue should create max-heap")
	}
}

func TestEnqueueDequeue(t *testing.T) {
	pq := NewPriorityQueue()
	
	// Enqueue items with different priorities
	pq.Enqueue("low", 1.0)
	pq.Enqueue("high", 10.0)
	pq.Enqueue("medium", 5.0)
	
	if pq.Len() != 3 {
		t.Errorf("Expected length 3, got %d", pq.Len())
	}
	
	// Min-heap should return lowest priority first
	item, err := pq.Dequeue()
	if err != nil {
		t.Fatalf("Dequeue failed: %v", err)
	}
	if item.Value.(string) != "low" {
		t.Errorf("Expected 'low', got '%s'", item.Value)
	}
	if item.Priority != 1.0 {
		t.Errorf("Expected priority 1.0, got %.2f", item.Priority)
	}
	
	item, err = pq.Dequeue()
	if err != nil {
		t.Fatalf("Dequeue failed: %v", err)
	}
	if item.Value.(string) != "medium" {
		t.Errorf("Expected 'medium', got '%s'", item.Value)
	}
	
	item, err = pq.Dequeue()
	if err != nil {
		t.Fatalf("Dequeue failed: %v", err)
	}
	if item.Value.(string) != "high" {
		t.Errorf("Expected 'high', got '%s'", item.Value)
	}
}

func TestMaxHeapEnqueueDequeue(t *testing.T) {
	pq := NewMaxPriorityQueue()
	
	pq.Enqueue("low", 1.0)
	pq.Enqueue("high", 10.0)
	pq.Enqueue("medium", 5.0)
	
	// Max-heap should return highest priority first
	item, _ := pq.Dequeue()
	if item.Value.(string) != "high" {
		t.Errorf("Max-heap expected 'high', got '%s'", item.Value)
	}
	
	item, _ = pq.Dequeue()
	if item.Value.(string) != "medium" {
		t.Errorf("Max-heap expected 'medium', got '%s'", item.Value)
	}
	
	item, _ = pq.Dequeue()
	if item.Value.(string) != "low" {
		t.Errorf("Max-heap expected 'low', got '%s'", item.Value)
	}
}

func TestPeek(t *testing.T) {
	pq := NewPriorityQueue()
	
	// Peek on empty queue
	_, err := pq.Peek()
	if err != ErrQueueEmpty {
		t.Errorf("Expected ErrQueueEmpty, got %v", err)
	}
	
	pq.Enqueue("first", 1.0)
	pq.Enqueue("second", 2.0)
	
	item, err := pq.Peek()
	if err != nil {
		t.Fatalf("Peek failed: %v", err)
	}
	if item.Value.(string) != "first" {
		t.Errorf("Expected 'first', got '%s'", item.Value)
	}
	
	// Peek should not remove the item
	if pq.Len() != 2 {
		t.Errorf("Peek should not remove item, expected length 2, got %d", pq.Len())
	}
}

func TestDequeueEmptyQueue(t *testing.T) {
	pq := NewPriorityQueue()
	
	_, err := pq.Dequeue()
	if err != ErrQueueEmpty {
		t.Errorf("Expected ErrQueueEmpty, got %v", err)
	}
}

// ============================================================================
// Update Operations Tests
// ============================================================================

func TestUpdatePriority(t *testing.T) {
	pq := NewPriorityQueue()
	
	item1 := pq.Enqueue("item1", 1.0)
	pq.Enqueue("item2", 2.0)
	pq.Enqueue("item3", 3.0)
	
	// Update priority to make item1 highest
	err := pq.UpdatePriority(item1, 10.0)
	if err != nil {
		t.Fatalf("UpdatePriority failed: %v", err)
	}
	if item1.Priority != 10.0 {
		t.Errorf("Expected priority 10.0, got %.2f", item1.Priority)
	}
	
	// Now item1 should be last to dequeue (lowest priority in min-heap)
	item, _ := pq.Dequeue()
	if item.Value.(string) == "item1" {
		t.Error("item1 should not be dequeued first after priority update")
	}
}

func TestUpdatePriorityNilItem(t *testing.T) {
	pq := NewPriorityQueue()
	err := pq.UpdatePriority(nil, 10.0)
	if err != ErrNilItem {
		t.Errorf("Expected ErrNilItem, got %v", err)
	}
}

func TestRemove(t *testing.T) {
	pq := NewPriorityQueue()
	
	_ = pq.Enqueue("item1", 1.0)
	item2 := pq.Enqueue("item2", 2.0)
	_ = pq.Enqueue("item3", 3.0)
	
	// Remove item2
	err := pq.Remove(item2)
	if err != nil {
		t.Fatalf("Remove failed: %v", err)
	}
	
	if pq.Len() != 2 {
		t.Errorf("Expected length 2 after remove, got %d", pq.Len())
	}
	
	// Verify item2 is not in queue
	values := pq.Values()
	for _, v := range values {
		if v.(string) == "item2" {
			t.Error("item2 should have been removed")
		}
	}
}

// ============================================================================
// Query Operations Tests
// ============================================================================

func TestContains(t *testing.T) {
	pq := NewPriorityQueue()
	
	pq.Enqueue("a", 1.0)
	pq.Enqueue("b", 2.0)
	pq.Enqueue("c", 3.0)
	
	if !pq.Contains("a") {
		t.Error("Queue should contain 'a'")
	}
	if pq.Contains("d") {
		t.Error("Queue should not contain 'd'")
	}
}

func TestFindByValue(t *testing.T) {
	pq := NewPriorityQueue()
	
	pq.Enqueue("a", 1.0)
	pq.Enqueue("b", 2.0)
	pq.Enqueue("c", 3.0)
	
	item := pq.FindByValue("b")
	if item == nil {
		t.Fatal("Should find item 'b'")
	}
	if item.Value.(string) != "b" {
		t.Errorf("Expected 'b', got '%s'", item.Value)
	}
	if item.Priority != 2.0 {
		t.Errorf("Expected priority 2.0, got %.2f", item.Priority)
	}
	
	// Find non-existent item
	item = pq.FindByValue("d")
	if item != nil {
		t.Error("Should not find 'd'")
	}
}

func TestFindAllByPriorityRange(t *testing.T) {
	pq := NewPriorityQueue()
	
	pq.Enqueue("a", 1.0)
	pq.Enqueue("b", 2.0)
	pq.Enqueue("c", 3.0)
	pq.Enqueue("d", 4.0)
	pq.Enqueue("e", 5.0)
	
	items := pq.FindAllByPriorityRange(2.0, 4.0)
	if len(items) != 3 {
		t.Errorf("Expected 3 items in range, got %d", len(items))
	}
}

func TestSortedItems(t *testing.T) {
	pq := NewPriorityQueue()
	
	pq.Enqueue("c", 3.0)
	pq.Enqueue("a", 1.0)
	pq.Enqueue("b", 2.0)
	
	items := pq.SortedItems()
	expected := []string{"a", "b", "c"}
	
	for i, item := range items {
		if item.Value.(string) != expected[i] {
			t.Errorf("SortedItems[%d]: expected '%s', got '%s'", i, expected[i], item.Value)
		}
	}
}

// ============================================================================
// Bulk Operations Tests
// ============================================================================

func TestEnqueueBatch(t *testing.T) {
	pq := NewPriorityQueue()
	
	items := []struct {
		Value    interface{}
		Priority float64
	}{
		{"a", 3.0},
		{"b", 1.0},
		{"c", 2.0},
	}
	
	pq.EnqueueBatch(items)
	
	if pq.Len() != 3 {
		t.Errorf("Expected length 3, got %d", pq.Len())
	}
	
	// Verify order
	item, _ := pq.Dequeue()
	if item.Value.(string) != "b" {
		t.Errorf("Expected 'b', got '%s'", item.Value)
	}
}

func TestDequeueN(t *testing.T) {
	pq := NewPriorityQueue()
	
	for i := 1; i <= 5; i++ {
		pq.Enqueue(i, float64(i))
	}
	
	items, err := pq.DequeueN(3)
	if err != nil {
		t.Fatalf("DequeueN failed: %v", err)
	}
	
	if len(items) != 3 {
		t.Errorf("Expected 3 items, got %d", len(items))
	}
	
	// Verify order
	for i, item := range items {
		expected := i + 1
		if item.Value.(int) != expected {
			t.Errorf("DequeueN[%d]: expected %d, got %d", i, expected, item.Value)
		}
	}
	
	if pq.Len() != 2 {
		t.Errorf("Expected 2 remaining items, got %d", pq.Len())
	}
}

func TestDrain(t *testing.T) {
	pq := NewPriorityQueue()
	
	pq.Enqueue("a", 1.0)
	pq.Enqueue("b", 2.0)
	pq.Enqueue("c", 3.0)
	
	items := pq.Drain()
	
	if len(items) != 3 {
		t.Errorf("Expected 3 items, got %d", len(items))
	}
	
	if !pq.IsEmpty() {
		t.Error("Queue should be empty after drain")
	}
}

// ============================================================================
// Statistics Tests
// ============================================================================

func TestGetStats(t *testing.T) {
	pq := NewPriorityQueue()
	
	// Empty queue
	stats := pq.GetStats()
	if stats.Size != 0 {
		t.Errorf("Expected size 0, got %d", stats.Size)
	}
	
	// Add items
	pq.Enqueue("a", 1.0)
	pq.Enqueue("b", 2.0)
	pq.Enqueue("c", 3.0)
	
	stats = pq.GetStats()
	
	if stats.Size != 3 {
		t.Errorf("Expected size 3, got %d", stats.Size)
	}
	if stats.MinPriority != 1.0 {
		t.Errorf("Expected min priority 1.0, got %.2f", stats.MinPriority)
	}
	if stats.MaxPriority != 3.0 {
		t.Errorf("Expected max priority 3.0, got %.2f", stats.MaxPriority)
	}
	if math.Abs(stats.AvgPriority-2.0) > 0.001 {
		t.Errorf("Expected avg priority 2.0, got %.2f", stats.AvgPriority)
	}
	if stats.SumPriority != 6.0 {
		t.Errorf("Expected sum priority 6.0, got %.2f", stats.SumPriority)
	}
}

// ============================================================================
// Utility Functions Tests
// ============================================================================

func TestMerge(t *testing.T) {
	pq1 := NewPriorityQueue()
	pq1.Enqueue("a1", 1.0)
	pq1.Enqueue("a2", 3.0)
	
	pq2 := NewPriorityQueue()
	pq2.Enqueue("b1", 2.0)
	pq2.Enqueue("b2", 4.0)
	
	merged := Merge(pq1, pq2)
	
	if merged.Len() != 4 {
		t.Errorf("Expected merged length 4, got %d", merged.Len())
	}
	
	// Verify order
	expected := []float64{1.0, 2.0, 3.0, 4.0}
	for _, exp := range expected {
		item, _ := merged.Dequeue()
		if item.Priority != exp {
			t.Errorf("Expected priority %.2f, got %.2f", exp, item.Priority)
		}
	}
}

func TestClone(t *testing.T) {
	pq := NewPriorityQueue()
	pq.Enqueue("a", 1.0)
	pq.Enqueue("b", 2.0)
	
	cloned := pq.Clone()
	
	if cloned.Len() != pq.Len() {
		t.Errorf("Cloned queue should have same length")
	}
	
	// Modify original
	pq.Dequeue()
	
	// Clone should be unaffected
	if cloned.Len() == pq.Len() {
		t.Error("Clone should be independent of original")
	}
}

func TestClear(t *testing.T) {
	pq := NewPriorityQueue()
	pq.Enqueue("a", 1.0)
	pq.Enqueue("b", 2.0)
	
	pq.Clear()
	
	if !pq.IsEmpty() {
		t.Error("Queue should be empty after clear")
	}
}

// ============================================================================
// Typed Priority Queue Tests
// ============================================================================

func TestIntPriorityQueue(t *testing.T) {
	pq := NewIntPriorityQueue()
	
	pq.Enqueue(10, 1)
	pq.Enqueue(20, 3)
	pq.Enqueue(30, 2)
	
	// Min-heap: should dequeue by priority (1, 2, 3)
	val, _ := pq.Dequeue()
	if val != 10 {
		t.Errorf("Expected 10, got %d", val)
	}
	
	val, _ = pq.Dequeue()
	if val != 30 {
		t.Errorf("Expected 30, got %d", val)
	}
	
	val, _ = pq.Dequeue()
	if val != 20 {
		t.Errorf("Expected 20, got %d", val)
	}
}

func TestStringPriorityQueue(t *testing.T) {
	pq := NewStringPriorityQueue()
	
	pq.Enqueue("low", 1.0)
	pq.Enqueue("high", 3.0)
	pq.Enqueue("medium", 2.0)
	
	// Min-heap: should dequeue by priority
	val, _ := pq.Dequeue()
	if val != "low" {
		t.Errorf("Expected 'low', got '%s'", val)
	}
	
	val, _ = pq.Dequeue()
	if val != "medium" {
		t.Errorf("Expected 'medium', got '%s'", val)
	}
	
	val, _ = pq.Dequeue()
	if val != "high" {
		t.Errorf("Expected 'high', got '%s'", val)
	}
}

// ============================================================================
// Edge Cases Tests
// ============================================================================

func TestEqualPriorities(t *testing.T) {
	pq := NewPriorityQueue()
	
	pq.Enqueue("a", 1.0)
	pq.Enqueue("b", 1.0)
	pq.Enqueue("c", 1.0)
	
	// All have same priority, should still work
	for i := 0; i < 3; i++ {
		_, err := pq.Dequeue()
		if err != nil {
			t.Errorf("Dequeue %d failed: %v", i, err)
		}
	}
}

func TestNegativePriorities(t *testing.T) {
	pq := NewPriorityQueue()
	
	pq.Enqueue("a", -1.0)
	pq.Enqueue("b", 0.0)
	pq.Enqueue("c", 1.0)
	
	// Min-heap: should return negative first
	item, _ := pq.Dequeue()
	if item.Value.(string) != "a" {
		t.Errorf("Expected 'a', got '%s'", item.Value)
	}
}

func TestLargeQueue(t *testing.T) {
	pq := NewPriorityQueue()
	n := 10000
	
	for i := n; i >= 1; i-- {
		pq.Enqueue(i, float64(i))
	}
	
	if pq.Len() != n {
		t.Errorf("Expected length %d, got %d", n, pq.Len())
	}
	
	// Min-heap: should dequeue in order 1, 2, 3, ...
	for i := 1; i <= n; i++ {
		item, err := pq.Dequeue()
		if err != nil {
			t.Errorf("Dequeue %d failed: %v", i, err)
			break
		}
		if item.Value.(int) != i {
			t.Errorf("Expected %d, got %d", i, item.Value)
			break
		}
	}
}

// ============================================================================
// Benchmark Tests
// ============================================================================

func BenchmarkEnqueue(b *testing.B) {
	pq := NewPriorityQueue()
	for i := 0; i < b.N; i++ {
		pq.Enqueue(i, float64(i))
	}
}

func BenchmarkDequeue(b *testing.B) {
	pq := NewPriorityQueue()
	for i := 0; i < b.N; i++ {
		pq.Enqueue(i, float64(i))
	}
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		pq.Dequeue()
	}
}

func BenchmarkEnqueueDequeue(b *testing.B) {
	pq := NewPriorityQueue()
	for i := 0; i < b.N; i++ {
		pq.Enqueue(i, float64(i))
		pq.Dequeue()
	}
}