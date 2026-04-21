package heap_utils

import (
	"math/rand"
	"sort"
	"testing"
)

// ============================================================================
// MinHeap Tests
// ============================================================================

func TestMinHeapBasic(t *testing.T) {
	h := NewMinHeap[int]()
	if !h.IsEmpty() {
		t.Error("new heap should be empty")
	}
	if h.Len() != 0 {
		t.Error("new heap length should be 0")
	}

	h.Push(5)
	h.Push(3)
	h.Push(7)
	h.Push(1)

	if h.Len() != 4 {
		t.Errorf("expected length 4, got %d", h.Len())
	}

	// Peek should return minimum
	top, ok := h.Peek()
	if !ok || top != 1 {
		t.Errorf("expected peek 1, got %d, ok=%v", top, ok)
	}

	// Pop should return elements in ascending order
	expected := []int{1, 3, 5, 7}
	for i, exp := range expected {
		val := h.Pop()
		if val != exp {
			t.Errorf("pop %d: expected %d, got %d", i, exp, val)
		}
	}
}

func TestMinHeapWithInitialElements(t *testing.T) {
	h := NewMinHeap(5, 2, 8, 1, 9)
	
	top, ok := h.Peek()
	if !ok || top != 1 {
		t.Errorf("expected min 1, got %d", top)
	}

	values := h.Values()
	expected := []int{1, 2, 5, 8, 9}
	for i, v := range values {
		if v != expected[i] {
			t.Errorf("values[%d]: expected %d, got %d", i, expected[i], v)
		}
	}
}

func TestMinHeapString(t *testing.T) {
	h := NewMinHeap("banana", "apple", "cherry")
	
	top, ok := h.Peek()
	if !ok || top != "apple" {
		t.Errorf("expected 'apple', got %s", top)
	}

	vals := h.Values()
	if len(vals) != 3 || vals[0] != "apple" || vals[1] != "banana" || vals[2] != "cherry" {
		t.Errorf("unexpected values: %v", vals)
	}
}

func TestMinHeapClear(t *testing.T) {
	h := NewMinHeap(1, 2, 3)
	h.Clear()
	
	if !h.IsEmpty() {
		t.Error("heap should be empty after clear")
	}
}

func TestMinHeapToSlice(t *testing.T) {
	h := NewMinHeap(3, 1, 2)
	slice := h.ToSlice()
	
	if len(slice) != 3 {
		t.Errorf("expected length 3, got %d", len(slice))
	}
	
	// Original heap should still have elements
	if h.Len() != 3 {
		t.Error("ToSlice should not modify heap")
	}
}

// ============================================================================
// MaxHeap Tests
// ============================================================================

func TestMaxHeapBasic(t *testing.T) {
	h := NewMaxHeap[int]()
	h.Push(5)
	h.Push(3)
	h.Push(7)
	h.Push(1)

	top, ok := h.Peek()
	if !ok || top != 7 {
		t.Errorf("expected peek 7, got %d", top)
	}

	expected := []int{7, 5, 3, 1}
	for i, exp := range expected {
		val := h.Pop()
		if val != exp {
			t.Errorf("pop %d: expected %d, got %d", i, exp, val)
		}
	}
}

func TestMaxHeapWithInitialElements(t *testing.T) {
	h := NewMaxHeap(5, 2, 8, 1, 9)
	
	top, ok := h.Peek()
	if !ok || top != 9 {
		t.Errorf("expected max 9, got %d", top)
	}

	values := h.Values()
	expected := []int{9, 8, 5, 2, 1}
	for i, v := range values {
		if v != expected[i] {
			t.Errorf("values[%d]: expected %d, got %d", i, expected[i], v)
		}
	}
}

func TestMaxHeapString(t *testing.T) {
	h := NewMaxHeap("banana", "apple", "cherry")
	
	top, ok := h.Peek()
	if !ok || top != "cherry" {
		t.Errorf("expected 'cherry', got %s", top)
	}
}

// ============================================================================
// PriorityQueue Tests
// ============================================================================

type Task struct {
	Name string
}

func TestPriorityQueueHigherFirst(t *testing.T) {
	pq := NewPriorityQueue[Task](true) // higher priority first

	pq.Push(Task{Name: "low"}, 1)
	pq.Push(Task{Name: "high"}, 10)
	pq.Push(Task{Name: "medium"}, 5)

	if pq.Len() != 3 {
		t.Errorf("expected length 3, got %d", pq.Len())
	}

	// Should pop in priority order: high, medium, low
	expected := []string{"high", "medium", "low"}
	for i, exp := range expected {
		item := pq.Pop()
		if item.Value.Name != exp {
			t.Errorf("pop %d: expected %s, got %s", i, exp, item.Value.Name)
		}
	}
}

func TestPriorityQueueLowerFirst(t *testing.T) {
	pq := NewPriorityQueue[Task](false) // lower priority first

	pq.Push(Task{Name: "low"}, 1)
	pq.Push(Task{Name: "high"}, 10)
	pq.Push(Task{Name: "medium"}, 5)

	// Should pop in priority order: low, medium, high
	expected := []string{"low", "medium", "high"}
	for i, exp := range expected {
		item := pq.Pop()
		if item.Value.Name != exp {
			t.Errorf("pop %d: expected %s, got %s", i, exp, item.Value.Name)
		}
	}
}

func TestPriorityQueueUpdate(t *testing.T) {
	pq := NewPriorityQueue[string](true)

	item := pq.Push("task1", 5)
	pq.Push("task2", 10)

	// Update task1 to highest priority
	pq.Update(item, 100)

	top := pq.Pop()
	if top.Value != "task1" || top.Priority != 100 {
		t.Errorf("expected task1 with priority 100, got %s with priority %f", top.Value, top.Priority)
	}
}

func TestPriorityQueuePeek(t *testing.T) {
	pq := NewPriorityQueue[int](true)
	
	if pq.Peek() != nil {
		t.Error("peek on empty queue should return nil")
	}

	pq.Push(10, 1)
	pq.Push(20, 2)

	top := pq.Peek()
	if top == nil || top.Value != 20 {
		t.Errorf("expected peek value 20, got %v", top)
	}

	// Peek should not remove
	if pq.Len() != 2 {
		t.Error("peek should not remove element")
	}
}

func TestPriorityQueueClear(t *testing.T) {
	pq := NewPriorityQueue[int](true)
	pq.Push(1, 1)
	pq.Push(2, 2)
	pq.Clear()

	if !pq.IsEmpty() {
		t.Error("queue should be empty after clear")
	}
}

// ============================================================================
// GenericHeap Tests
// ============================================================================

type Person struct {
	Name string
	Age  int
}

func TestGenericHeap(t *testing.T) {
	// Heap ordered by age (youngest first)
	h := NewGenericHeap(func(a, b Person) bool {
		return a.Age < b.Age
	}, Person{Name: "Alice", Age: 30}, Person{Name: "Bob", Age: 25})

	h.Push(Person{Name: "Charlie", Age: 35})

	// Should pop youngest first
	p, ok := h.Peek()
	if !ok || p.Name != "Bob" {
		t.Errorf("expected Bob, got %v", p)
	}

	expected := []string{"Bob", "Alice", "Charlie"}
	for i, exp := range expected {
		p := h.Pop()
		if p.Name != exp {
			t.Errorf("pop %d: expected %s, got %s", i, exp, p.Name)
		}
	}
}

func TestGenericHeapCustomOrder(t *testing.T) {
	// Max-heap by string length
	h := NewGenericHeap(func(a, b string) bool {
		return len(a) > len(b)
	}, "a", "bb", "ccc")

	vals := []string{h.Pop(), h.Pop(), h.Pop()}
	expected := []string{"ccc", "bb", "a"}
	for i := range vals {
		if vals[i] != expected[i] {
			t.Errorf("expected %s, got %s", expected[i], vals[i])
		}
	}
}

// ============================================================================
// TopK / BottomK Tests
// ============================================================================

func TestTopK(t *testing.T) {
	data := []int{3, 1, 4, 1, 5, 9, 2, 6, 5, 3}
	top := TopK(data, 3)

	expected := []int{9, 6, 5}
	if len(top) != len(expected) {
		t.Fatalf("expected %d elements, got %d", len(expected), len(top))
	}
	for i, v := range top {
		if v != expected[i] {
			t.Errorf("top[%d]: expected %d, got %d", i, expected[i], v)
		}
	}
}

func TestTopKWithKGreaterThanN(t *testing.T) {
	data := []int{3, 1, 4}
	top := TopK(data, 5)

	if len(top) != 3 {
		t.Errorf("expected 3 elements, got %d", len(top))
	}
}

func TestTopKEmpty(t *testing.T) {
	top := TopK([]int{}, 3)
	if top != nil {
		t.Errorf("expected nil for empty input, got %v", top)
	}
}

func TestTopKZeroK(t *testing.T) {
	top := TopK([]int{1, 2, 3}, 0)
	if top != nil {
		t.Errorf("expected nil for k=0, got %v", top)
	}
}

func TestBottomK(t *testing.T) {
	data := []int{3, 1, 4, 1, 5, 9, 2, 6, 5, 3}
	bottom := BottomK(data, 3)

	expected := []int{1, 1, 2}
	if len(bottom) != len(expected) {
		t.Fatalf("expected %d elements, got %d", len(expected), len(bottom))
	}
	for i, v := range bottom {
		if v != expected[i] {
			t.Errorf("bottom[%d]: expected %d, got %d", i, expected[i], v)
		}
	}
}

func TestBottomKWithKGreaterThanN(t *testing.T) {
	data := []int{3, 1, 4}
	bottom := BottomK(data, 5)

	if len(bottom) != 3 {
		t.Errorf("expected 3 elements, got %d", len(bottom))
	}
}

// ============================================================================
// MergeKSorted Tests
// ============================================================================

func TestMergeKSorted(t *testing.T) {
	s1 := []int{1, 4, 7}
	s2 := []int{2, 5, 8}
	s3 := []int{3, 6, 9}

	merged := MergeKSorted(s1, s2, s3)
	expected := []int{1, 2, 3, 4, 5, 6, 7, 8, 9}

	if len(merged) != len(expected) {
		t.Fatalf("expected %d elements, got %d", len(expected), len(merged))
	}
	for i, v := range merged {
		if v != expected[i] {
			t.Errorf("merged[%d]: expected %d, got %d", i, expected[i], v)
		}
	}
}

func TestMergeKSortedEmpty(t *testing.T) {
	merged := MergeKSorted[int]()
	if merged != nil {
		t.Errorf("expected nil for no slices, got %v", merged)
	}
}

func TestMergeKSortedSingleSlice(t *testing.T) {
	merged := MergeKSorted([]int{1, 2, 3})
	expected := []int{1, 2, 3}
	for i, v := range merged {
		if v != expected[i] {
			t.Errorf("merged[%d]: expected %d, got %d", i, expected[i], v)
		}
	}
}

func TestMergeKSortedWithEmptySlices(t *testing.T) {
	s1 := []int{1, 3, 5}
	s2 := []int{}
	s3 := []int{2, 4}

	merged := MergeKSorted(s1, s2, s3)
	expected := []int{1, 2, 3, 4, 5}
	for i, v := range merged {
		if v != expected[i] {
			t.Errorf("merged[%d]: expected %d, got %d", i, expected[i], v)
		}
	}
}

func TestMergeKSortedStrings(t *testing.T) {
	s1 := []string{"apple", "orange"}
	s2 := []string{"banana", "pear"}

	merged := MergeKSorted(s1, s2)
	expected := []string{"apple", "banana", "orange", "pear"}
	for i, v := range merged {
		if v != expected[i] {
			t.Errorf("merged[%d]: expected %s, got %s", i, expected[i], v)
		}
	}
}

// ============================================================================
// HeapSort Tests
// ============================================================================

func TestHeapSort(t *testing.T) {
	data := []int{3, 1, 4, 1, 5, 9, 2, 6}
	sorted := HeapSort(data)

	if !sort.IntsAreSorted(sorted) {
		t.Errorf("result not sorted: %v", sorted)
	}
}

func TestHeapSortDesc(t *testing.T) {
	data := []int{3, 1, 4, 1, 5, 9, 2, 6}
	sorted := HeapSortDesc(data)

	for i := 1; i < len(sorted); i++ {
		if sorted[i-1] < sorted[i] {
			t.Errorf("result not sorted descending: %v", sorted)
			break
		}
	}
}

func TestHeapSortEmpty(t *testing.T) {
	sorted := HeapSort([]int{})
	if len(sorted) != 0 {
		t.Errorf("expected empty slice, got %v", sorted)
	}
}

func TestHeapSortSingle(t *testing.T) {
	sorted := HeapSort([]int{42})
	if len(sorted) != 1 || sorted[0] != 42 {
		t.Errorf("expected [42], got %v", sorted)
	}
}

func TestHeapSortOriginalUnmodified(t *testing.T) {
	data := []int{3, 1, 2}
	orig := make([]int, len(data))
	copy(orig, data)
	
	HeapSort(data)
	
	for i := range data {
		if data[i] != orig[i] {
			t.Error("HeapSort should not modify original slice")
			break
		}
	}
}

// ============================================================================
// NthElement Tests
// ============================================================================

func TestNthSmallest(t *testing.T) {
	data := []int{3, 1, 4, 1, 5, 9, 2, 6, 5, 3}
	
	val, ok := NthSmallest(data, 1)
	if !ok || val != 1 {
		t.Errorf("1st smallest: expected 1, got %d", val)
	}

	val, ok = NthSmallest(data, 5)
	if !ok || val != 3 {
		t.Errorf("5th smallest: expected 3, got %d", val)
	}

	val, ok = NthSmallest(data, 10)
	if !ok || val != 9 {
		t.Errorf("10th smallest: expected 9, got %d", val)
	}
}

func TestNthSmallestOutOfRange(t *testing.T) {
	data := []int{1, 2, 3}
	
	_, ok := NthSmallest(data, 0)
	if ok {
		t.Error("should return false for n=0")
	}

	_, ok = NthSmallest(data, 4)
	if ok {
		t.Error("should return false for n > len")
	}
}

func TestNthLargest(t *testing.T) {
	data := []int{3, 1, 4, 1, 5, 9, 2, 6, 5, 3}
	
	val, ok := NthLargest(data, 1)
	if !ok || val != 9 {
		t.Errorf("1st largest: expected 9, got %d", val)
	}

	val, ok = NthLargest(data, 3)
	if !ok || val != 5 {
		t.Errorf("3rd largest: expected 5, got %d", val)
	}
}

func TestMedian(t *testing.T) {
	// Odd length
	data1 := []int{3, 1, 4, 1, 5}
	med, ok := Median(data1)
	if !ok || med != 3 {
		t.Errorf("median of odd: expected 3, got %d", med)
	}

	// Even length (returns lower median)
	data2 := []int{3, 1, 4, 1}
	med, ok = Median(data2)
	if !ok || med != 1 {
		t.Errorf("median of even: expected 1, got %d", med)
	}

	// Empty
	_, ok = Median([]int{})
	if ok {
		t.Error("median of empty should return false")
	}
}

// ============================================================================
// Edge Cases and Random Tests
// ============================================================================

func TestMinHeapDuplicates(t *testing.T) {
	h := NewMinHeap(5, 5, 5, 5)
	for i := 0; i < 4; i++ {
		if h.Pop() != 5 {
			t.Error("should handle duplicates")
		}
	}
}

func TestMinHeapLargeDataset(t *testing.T) {
	const n = 10000
	
	// Generate random data
	data := make([]int, n)
	for i := range data {
		data[i] = rand.Intn(1000000)
	}

	h := NewMinHeap(data...)
	
	// Verify sorted order
	prev := -1
	for h.Len() > 0 {
		cur := h.Pop()
		if cur < prev {
			t.Error("elements not in sorted order")
			break
		}
		prev = cur
	}
}

func TestTopKRandom(t *testing.T) {
	const n = 1000
	data := make([]int, n)
	for i := range data {
		data[i] = rand.Intn(10000)
	}

	top := TopK(data, 10)
	
	// Verify top are actually the largest
	sorted := make([]int, n)
	copy(sorted, data)
	sort.Sort(sort.Reverse(sort.IntSlice(sorted)))
	
	for i := 0; i < 10; i++ {
		if top[i] != sorted[i] {
			t.Errorf("TopK mismatch at %d: expected %d, got %d", i, sorted[i], top[i])
		}
	}
}

func TestMergeKSortedStress(t *testing.T) {
	// Merge 100 sorted slices of 100 elements each
	slices := make([][]int, 100)
	for i := range slices {
		slices[i] = make([]int, 100)
		for j := range slices[i] {
			slices[i][j] = i*1000 + j
		}
	}

	merged := MergeKSorted(slices...)
	
	if len(merged) != 10000 {
		t.Fatalf("expected 10000 elements, got %d", len(merged))
	}
	
	for i := 1; i < len(merged); i++ {
		if merged[i] < merged[i-1] {
			t.Errorf("not sorted at %d: %d > %d", i, merged[i-1], merged[i])
			break
		}
	}
}

// Benchmark tests
func BenchmarkMinHeapPush(b *testing.B) {
	h := NewMinHeap[int]()
	for i := 0; i < b.N; i++ {
		h.Push(rand.Int())
	}
}

func BenchmarkMinHeapPop(b *testing.B) {
	h := NewMinHeap[int]()
	for i := 0; i < b.N; i++ {
		h.Push(rand.Int())
	}
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		h.Pop()
	}
}

func BenchmarkTopK(b *testing.B) {
	data := make([]int, 10000)
	for i := range data {
		data[i] = rand.Int()
	}
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		TopK(data, 100)
	}
}

func BenchmarkMergeKSorted(b *testing.B) {
	slices := make([][]int, 10)
	for i := range slices {
		slices[i] = make([]int, 1000)
		for j := range slices[i] {
			slices[i][j] = i*10000 + j
		}
	}
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		MergeKSorted(slices...)
	}
}