// Package heap_utils provides easy-to-use heap data structures for Go.
// It wraps the standard library's container/heap interface with a simpler API.
//
// Features:
//   - MinHeap and MaxHeap with generic type support
//   - PriorityQueue with custom comparators
//   - TopK/BottomK selection algorithms
//   - Merge multiple sorted sequences
//   - Heap sort utilities
//
// Zero external dependencies - uses only Go standard library.
package heap_utils

import (
	"container/heap"
)

// ============================================================================
// Heap Interface (internal)
// ============================================================================

// heapInterface implements heap.Interface for internal use
type heapInterface[T any] struct {
	data []T
	less func(a, b T) bool
}

func (h *heapInterface[T]) Len() int           { return len(h.data) }
func (h *heapInterface[T]) Less(i, j int) bool { return h.less(h.data[i], h.data[j]) }
func (h *heapInterface[T]) Swap(i, j int)      { h.data[i], h.data[j] = h.data[j], h.data[i] }
func (h *heapInterface[T]) Push(x any)         { h.data = append(h.data, x.(T)) }
func (h *heapInterface[T]) Pop() any {
	n := len(h.data)
	item := h.data[n-1]
	h.data = h.data[:n-1]
	return item
}

// ============================================================================
// MinHeap - Minimum value at root
// ============================================================================

// MinHeap represents a min-heap where the smallest element is always at the root.
// Time complexity: Push O(log n), Pop O(log n), Peek O(1)
type MinHeap[T Ordered] struct {
	inner *heapInterface[T]
}

// NewMinHeap creates a new min-heap with optional initial elements.
func NewMinHeap[T Ordered](elements ...T) *MinHeap[T] {
	h := &MinHeap[T]{
		inner: &heapInterface[T]{
			data: make([]T, 0, len(elements)),
			less: func(a, b T) bool { return a < b },
		},
	}
	for _, e := range elements {
		h.inner.data = append(h.inner.data, e)
	}
	heap.Init(h.inner)
	return h
}

// Push adds an element to the heap. O(log n)
func (h *MinHeap[T]) Push(x T) { heap.Push(h.inner, x) }

// Pop removes and returns the minimum element. O(log n)
// Panics if heap is empty.
func (h *MinHeap[T]) Pop() T { return heap.Pop(h.inner).(T) }

// Peek returns the minimum element without removing it. O(1)
// Returns zero value and false if heap is empty.
func (h *MinHeap[T]) Peek() (T, bool) {
	if h.inner.Len() == 0 {
		var zero T
		return zero, false
	}
	return h.inner.data[0], true
}

// Len returns the number of elements in the heap.
func (h *MinHeap[T]) Len() int { return h.inner.Len() }

// IsEmpty returns true if the heap has no elements.
func (h *MinHeap[T]) IsEmpty() bool { return h.inner.Len() == 0 }

// Clear removes all elements from the heap.
func (h *MinHeap[T]) Clear() { h.inner.data = h.inner.data[:0] }

// ToSlice returns a copy of all elements in unspecified order.
func (h *MinHeap[T]) ToSlice() []T {
	result := make([]T, len(h.inner.data))
	copy(result, h.inner.data)
	return result
}

// Values returns all elements in ascending order (consumes the heap).
func (h *MinHeap[T]) Values() []T {
	result := make([]T, 0, h.inner.Len())
	for h.inner.Len() > 0 {
		result = append(result, heap.Pop(h.inner).(T))
	}
	return result
}

// ============================================================================
// MaxHeap - Maximum value at root
// ============================================================================

// MaxHeap represents a max-heap where the largest element is always at the root.
// Time complexity: Push O(log n), Pop O(log n), Peek O(1)
type MaxHeap[T Ordered] struct {
	inner *heapInterface[T]
}

// NewMaxHeap creates a new max-heap with optional initial elements.
func NewMaxHeap[T Ordered](elements ...T) *MaxHeap[T] {
	h := &MaxHeap[T]{
		inner: &heapInterface[T]{
			data: make([]T, 0, len(elements)),
			less: func(a, b T) bool { return a > b }, // reversed for max-heap
		},
	}
	for _, e := range elements {
		h.inner.data = append(h.inner.data, e)
	}
	heap.Init(h.inner)
	return h
}

// Push adds an element to the heap. O(log n)
func (h *MaxHeap[T]) Push(x T) { heap.Push(h.inner, x) }

// Pop removes and returns the maximum element. O(log n)
// Panics if heap is empty.
func (h *MaxHeap[T]) Pop() T { return heap.Pop(h.inner).(T) }

// Peek returns the maximum element without removing it. O(1)
// Returns zero value and false if heap is empty.
func (h *MaxHeap[T]) Peek() (T, bool) {
	if h.inner.Len() == 0 {
		var zero T
		return zero, false
	}
	return h.inner.data[0], true
}

// Len returns the number of elements in the heap.
func (h *MaxHeap[T]) Len() int { return h.inner.Len() }

// IsEmpty returns true if the heap has no elements.
func (h *MaxHeap[T]) IsEmpty() bool { return h.inner.Len() == 0 }

// Clear removes all elements from the heap.
func (h *MaxHeap[T]) Clear() { h.inner.data = h.inner.data[:0] }

// ToSlice returns a copy of all elements in unspecified order.
func (h *MaxHeap[T]) ToSlice() []T {
	result := make([]T, len(h.inner.data))
	copy(result, h.inner.data)
	return result
}

// Values returns all elements in descending order (consumes the heap).
func (h *MaxHeap[T]) Values() []T {
	result := make([]T, 0, h.inner.Len())
	for h.inner.Len() > 0 {
		result = append(result, heap.Pop(h.inner).(T))
	}
	return result
}

// ============================================================================
// PriorityQueue - Custom comparator support
// ============================================================================

// Item represents an item in a priority queue with an optional priority.
type Item[T any] struct {
	Value    T
	Priority float64
	Index    int // maintained by heap for update support
}

// priorityQueue implements heap.Interface for items with priorities.
type priorityQueue[T any] struct {
	data    []*Item[T]
	less    func(a, b *Item[T]) bool
	getLess func(higher bool) func(a, b *Item[T]) bool
}

func (pq *priorityQueue[T]) Len() int { return len(pq.data) }
func (pq *priorityQueue[T]) Less(i, j int) bool {
	return pq.less(pq.data[i], pq.data[j])
}
func (pq *priorityQueue[T]) Swap(i, j int) {
	pq.data[i], pq.data[j] = pq.data[j], pq.data[i]
	pq.data[i].Index = i
	pq.data[j].Index = j
}
func (pq *priorityQueue[T]) Push(x any) {
	n := len(pq.data)
	item := x.(*Item[T])
	item.Index = n
	pq.data = append(pq.data, item)
}
func (pq *priorityQueue[T]) Pop() any {
	n := len(pq.data)
	item := pq.data[n-1]
	pq.data[n-1] = nil  // avoid memory leak
	pq.data = pq.data[:n-1]
	return item
}

// PriorityQueue is a heap-based priority queue with custom priorities.
type PriorityQueue[T any] struct {
	inner *priorityQueue[T]
}

// NewPriorityQueue creates a priority queue.
// If higher is true, higher priority values come out first (max-heap behavior).
// If higher is false, lower priority values come out first (min-heap behavior).
func NewPriorityQueue[T any](higher bool) *PriorityQueue[T] {
	lessFn := func(a, b *Item[T]) bool {
		if higher {
			return a.Priority < b.Priority // for max-heap, we want larger first
		}
		return a.Priority > b.Priority // for min-heap, we want smaller first
	}
	return &PriorityQueue[T]{
		inner: &priorityQueue[T]{
			data: make([]*Item[T], 0),
			less: lessFn,
		},
	}
}

// Push adds a value with given priority to the queue. O(log n)
func (pq *PriorityQueue[T]) Push(value T, priority float64) *Item[T] {
	item := &Item[T]{Value: value, Priority: priority}
	heap.Push(pq.inner, item)
	return item
}

// Pop removes and returns the highest/lowest priority item. O(log n)
// Panics if queue is empty.
func (pq *PriorityQueue[T]) Pop() *Item[T] {
	return heap.Pop(pq.inner).(*Item[T])
}

// Peek returns the top item without removing it. O(1)
func (pq *PriorityQueue[T]) Peek() *Item[T] {
	if len(pq.inner.data) == 0 {
		return nil
	}
	return pq.inner.data[0]
}

// Update modifies the priority of an item and reorders the queue. O(log n)
func (pq *PriorityQueue[T]) Update(item *Item[T], priority float64) {
	item.Priority = priority
	heap.Fix(pq.inner, item.Index)
}

// Len returns the number of items in the queue.
func (pq *PriorityQueue[T]) Len() int { return pq.inner.Len() }

// IsEmpty returns true if the queue has no items.
func (pq *PriorityQueue[T]) IsEmpty() bool { return pq.inner.Len() == 0 }

// Clear removes all items from the queue.
func (pq *PriorityQueue[T]) Clear() { pq.inner.data = pq.inner.data[:0] }

// ============================================================================
// GenericHeap - Custom comparator for any type
// ============================================================================

// GenericHeap is a heap that works with any type using a custom comparator.
type GenericHeap[T any] struct {
	inner *heapInterface[T]
}

// NewGenericHeap creates a heap with a custom less function.
// less(a, b) should return true if a should come before b in the heap.
func NewGenericHeap[T any](less func(a, b T) bool, elements ...T) *GenericHeap[T] {
	h := &GenericHeap[T]{
		inner: &heapInterface[T]{
			data: make([]T, 0, len(elements)),
			less: less,
		},
	}
	for _, e := range elements {
		h.inner.data = append(h.inner.data, e)
	}
	heap.Init(h.inner)
	return h
}

// Push adds an element to the heap. O(log n)
func (h *GenericHeap[T]) Push(x T) { heap.Push(h.inner, x) }

// Pop removes and returns the top element. O(log n)
func (h *GenericHeap[T]) Pop() T { return heap.Pop(h.inner).(T) }

// Peek returns the top element without removing it. O(1)
func (h *GenericHeap[T]) Peek() (T, bool) {
	if h.inner.Len() == 0 {
		var zero T
		return zero, false
	}
	return h.inner.data[0], true
}

// Len returns the number of elements.
func (h *GenericHeap[T]) Len() int { return h.inner.Len() }

// IsEmpty returns true if the heap is empty.
func (h *GenericHeap[T]) IsEmpty() bool { return h.inner.Len() == 0 }

// Clear removes all elements.
func (h *GenericHeap[T]) Clear() { h.inner.data = h.inner.data[:0] }

// ============================================================================
// TopK / BottomK Selection
// ============================================================================

// TopK returns the k largest elements from a slice, sorted descending.
// Uses a min-heap internally. O(n log k) time, O(k) space.
func TopK[T Ordered](data []T, k int) []T {
	if k <= 0 || len(data) == 0 {
		return nil
	}
	if k >= len(data) {
		result := make([]T, len(data))
		copy(result, data)
		// Sort descending
		for i := 0; i < len(result); i++ {
			for j := i + 1; j < len(result); j++ {
				if result[j] > result[i] {
					result[i], result[j] = result[j], result[i]
				}
			}
		}
		return result
	}

	// Use min-heap to keep track of k largest
	h := NewMinHeap[T]()
	for _, x := range data {
		if h.Len() < k {
			h.Push(x)
		} else if top, ok := h.Peek(); ok && x > top {
			h.Pop()
			h.Push(x)
		}
	}

	// Extract and sort descending
	result := make([]T, k)
	for i := k - 1; i >= 0; i-- {
		result[i] = h.Pop()
	}
	return result
}

// BottomK returns the k smallest elements from a slice, sorted ascending.
// Uses a max-heap internally. O(n log k) time, O(k) space.
func BottomK[T Ordered](data []T, k int) []T {
	if k <= 0 || len(data) == 0 {
		return nil
	}
	if k >= len(data) {
		result := make([]T, len(data))
		copy(result, data)
		// Sort ascending
		for i := 0; i < len(result); i++ {
			for j := i + 1; j < len(result); j++ {
				if result[j] < result[i] {
					result[i], result[j] = result[j], result[i]
				}
			}
		}
		return result
	}

	// Use max-heap to keep track of k smallest
	h := NewMaxHeap[T]()
	for _, x := range data {
		if h.Len() < k {
			h.Push(x)
		} else if top, ok := h.Peek(); ok && x < top {
			h.Pop()
			h.Push(x)
		}
	}

	// Extract and sort ascending
	result := make([]T, k)
	for i := k - 1; i >= 0; i-- {
		result[i] = h.Pop()
	}
	return result
}

// ============================================================================
// MergeKSorted - Merge multiple sorted sequences
// ============================================================================

// mergeItem is an internal type for merge operations.
type mergeItem[T Ordered] struct {
	value T
	index int // source index
}

// MergeKSorted merges k sorted slices into one sorted slice.
// Uses a min-heap internally. O(n log k) time where n is total elements.
func MergeKSorted[T Ordered](slices ...[]T) []T {
	if len(slices) == 0 {
		return nil
	}

	// Use a min-heap with indices to track which slice each item comes from
	h := NewGenericHeap(func(a, b mergeItem[T]) bool {
		return a.value < b.value
	})

	// Track current position in each slice
	positions := make([]int, len(slices))
	totalLen := 0
	for i, s := range slices {
		totalLen += len(s)
		if len(s) > 0 {
			h.Push(mergeItem[T]{value: s[0], index: i})
			positions[i] = 1
		}
	}

	result := make([]T, 0, totalLen)
	for h.Len() > 0 {
		item, _ := h.Peek()
		h.Pop()
		result = append(result, item.value)
		
		// Push next item from same slice if available
		if positions[item.index] < len(slices[item.index]) {
			h.Push(mergeItem[T]{
				value: slices[item.index][positions[item.index]],
				index: item.index,
			})
			positions[item.index]++
		}
	}

	return result
}

// ============================================================================
// HeapSort - In-place heap sort
// ============================================================================

// HeapSort sorts a slice in ascending order using heap sort. O(n log n)
func HeapSort[T Ordered](data []T) []T {
	if len(data) <= 1 {
		result := make([]T, len(data))
		copy(result, data)
		return result
	}

	// Build a min-heap and extract
	h := NewMinHeap(data...)
	return h.Values()
}

// HeapSortDesc sorts a slice in descending order using heap sort. O(n log n)
func HeapSortDesc[T Ordered](data []T) []T {
	if len(data) <= 1 {
		result := make([]T, len(data))
		copy(result, data)
		return result
	}

	h := NewMaxHeap(data...)
	return h.Values()
}

// ============================================================================
// NthElement - Find nth smallest/largest
// ============================================================================

// NthSmallest finds the nth smallest element (1-indexed).
// Returns zero value and false if n is out of range.
// O(n log n) in worst case, O(n) average with quickselect.
func NthSmallest[T Ordered](data []T, n int) (T, bool) {
	if n <= 0 || n > len(data) {
		var zero T
		return zero, false
	}

	h := NewMinHeap(data...)
	for i := 1; i < n; i++ {
		h.Pop()
	}
	return h.Pop(), true
}

// NthLargest finds the nth largest element (1-indexed).
// Returns zero value and false if n is out of range.
func NthLargest[T Ordered](data []T, n int) (T, bool) {
	if n <= 0 || n > len(data) {
		var zero T
		return zero, false
	}

	h := NewMaxHeap(data...)
	for i := 1; i < n; i++ {
		h.Pop()
	}
	return h.Pop(), true
}

// Median returns the median element.
// For even-length slices, returns the lower median.
func Median[T Ordered](data []T) (T, bool) {
	n := len(data)
	if n == 0 {
		var zero T
		return zero, false
	}
	return NthSmallest(data, (n+1)/2)
}

// ============================================================================
// Ordered constraint
// ============================================================================

// Ordered is a constraint for types that can be compared with < and >.
type Ordered interface {
	~int | ~int8 | ~int16 | ~int32 | ~int64 |
		~uint | ~uint8 | ~uint16 | ~uint32 | ~uint64 | ~uintptr |
		~float32 | ~float64 |
		~string
}