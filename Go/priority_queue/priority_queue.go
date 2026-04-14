// Package priority_queue provides a generic priority queue implementation.
// Zero external dependencies - pure Go standard library implementation.
// Supports min-heap and max-heap configurations with thread-safe options.
package priority_queue

import (
	"container/heap"
	"sync"
)

// Item represents an item in the priority queue
type Item[T any] struct {
	Value    T
	Priority int
	Index    int // Used by update method
}

// PriorityQueue implements heap.Interface and holds Items
type PriorityQueue[T any] struct {
	items    []*Item[T]
	lessFunc func(a, b int) bool
}

// Len implements heap.Interface
func (pq *PriorityQueue[T]) Len() int {
	return len(pq.items)
}

// Less implements heap.Interface
func (pq *PriorityQueue[T]) Less(i, j int) bool {
	return pq.lessFunc(pq.items[i].Priority, pq.items[j].Priority)
}

// Swap implements heap.Interface
func (pq *PriorityQueue[T]) Swap(i, j int) {
	pq.items[i], pq.items[j] = pq.items[j], pq.items[i]
	pq.items[i].Index = i
	pq.items[j].Index = j
}

// Push implements heap.Interface
func (pq *PriorityQueue[T]) Push(x interface{}) {
	n := len(pq.items)
	item := x.(*Item[T])
	item.Index = n
	pq.items = append(pq.items, item)
}

// Pop implements heap.Interface
func (pq *PriorityQueue[T]) Pop() interface{} {
	old := pq.items
	n := len(old)
	item := old[n-1]
	old[n-1] = nil  // avoid memory leak
	item.Index = -1 // for safety
	pq.items = old[0 : n-1]
	return item
}

// MinHeap creates a new min-heap priority queue (lower priority values = higher priority)
func MinHeap[T any]() *PriorityQueue[T] {
	pq := &PriorityQueue[T]{
		items: make([]*Item[T], 0),
		lessFunc: func(a, b int) bool {
			return a < b
		},
	}
	heap.Init(pq)
	return pq
}

// MaxHeap creates a new max-heap priority queue (higher priority values = higher priority)
func MaxHeap[T any]() *PriorityQueue[T] {
	pq := &PriorityQueue[T]{
		items: make([]*Item[T], 0),
		lessFunc: func(a, b int) bool {
			return a > b
		},
	}
	heap.Init(pq)
	return pq
}

// PushItem adds an item to the priority queue
func (pq *PriorityQueue[T]) PushItem(value T, priority int) *Item[T] {
	item := &Item[T]{
		Value:    value,
		Priority: priority,
	}
	heap.Push(pq, item)
	return item
}

// PopItem removes and returns the highest priority item
func (pq *PriorityQueue[T]) PopItem() (T, int, bool) {
	if pq.Len() == 0 {
		var zero T
		return zero, 0, false
	}
	item := heap.Pop(pq).(*Item[T])
	return item.Value, item.Priority, true
}

// Peek returns the highest priority item without removing it
func (pq *PriorityQueue[T]) Peek() (T, int, bool) {
	if pq.Len() == 0 {
		var zero T
		return zero, 0, false
	}
	return pq.items[0].Value, pq.items[0].Priority, true
}

// Update modifies the priority of an item in the queue
func (pq *PriorityQueue[T]) Update(item *Item[T], value T, priority int) {
	item.Value = value
	item.Priority = priority
	heap.Fix(pq, item.Index)
}

// Remove removes an item from the queue by index
func (pq *PriorityQueue[T]) Remove(item *Item[T]) T {
	heap.Remove(pq, item.Index)
	return item.Value
}

// IsEmpty returns true if the queue is empty
func (pq *PriorityQueue[T]) IsEmpty() bool {
	return pq.Len() == 0
}

// Clear removes all items from the queue
func (pq *PriorityQueue[T]) Clear() {
	pq.items = make([]*Item[T], 0)
}

// Size returns the number of items in the queue
func (pq *PriorityQueue[T]) Size() int {
	return pq.Len()
}

// ToSlice returns all items as a slice (does not modify the queue)
func (pq *PriorityQueue[T]) ToSlice() []Item[T] {
	result := make([]Item[T], len(pq.items))
	for i, item := range pq.items {
		result[i] = *item
	}
	return result
}

// Values returns all values in the queue (order not guaranteed)
func (pq *PriorityQueue[T]) Values() []T {
	result := make([]T, len(pq.items))
	for i, item := range pq.items {
		result[i] = item.Value
	}
	return result
}

// Contains checks if a value exists in the queue
func (pq *PriorityQueue[T]) Contains(equal func(T, T) bool, value T) bool {
	for _, item := range pq.items {
		if equal(item.Value, value) {
			return true
		}
	}
	return false
}

// Find returns the item matching the predicate
func (pq *PriorityQueue[T]) Find(predicate func(T) bool) (*Item[T], bool) {
	for _, item := range pq.items {
		if predicate(item.Value) {
			return item, true
		}
	}
	return nil, false
}

// FindByPriority returns all items with the given priority
func (pq *PriorityQueue[T]) FindByPriority(priority int) []*Item[T] {
	var result []*Item[T]
	for _, item := range pq.items {
		if item.Priority == priority {
			result = append(result, item)
		}
	}
	return result
}

// Clone creates a copy of the priority queue
func (pq *PriorityQueue[T]) Clone() *PriorityQueue[T] {
	newPq := &PriorityQueue[T]{
		items:    make([]*Item[T], len(pq.items)),
		lessFunc: pq.lessFunc,
	}
	for i, item := range pq.items {
		newItem := &Item[T]{
			Value:    item.Value,
			Priority: item.Priority,
			Index:    item.Index,
		}
		newPq.items[i] = newItem
	}
	heap.Init(newPq)
	return newPq
}

// ThreadSafePriorityQueue wraps PriorityQueue with mutex for concurrent access
type ThreadSafePriorityQueue[T any] struct {
	pq   *PriorityQueue[T]
	mu   sync.RWMutex
}

// NewThreadSafeMinHeap creates a thread-safe min-heap priority queue
func NewThreadSafeMinHeap[T any]() *ThreadSafePriorityQueue[T] {
	return &ThreadSafePriorityQueue[T]{
		pq: MinHeap[T](),
	}
}

// NewThreadSafeMaxHeap creates a thread-safe max-heap priority queue
func NewThreadSafeMaxHeap[T any]() *ThreadSafePriorityQueue[T] {
	return &ThreadSafePriorityQueue[T]{
		pq: MaxHeap[T](),
	}
}

// PushItem adds an item to the priority queue (thread-safe)
func (tspq *ThreadSafePriorityQueue[T]) PushItem(value T, priority int) *Item[T] {
	tspq.mu.Lock()
	defer tspq.mu.Unlock()
	return tspq.pq.PushItem(value, priority)
}

// PopItem removes and returns the highest priority item (thread-safe)
func (tspq *ThreadSafePriorityQueue[T]) PopItem() (T, int, bool) {
	tspq.mu.Lock()
	defer tspq.mu.Unlock()
	return tspq.pq.PopItem()
}

// Peek returns the highest priority item without removing it (thread-safe)
func (tspq *ThreadSafePriorityQueue[T]) Peek() (T, int, bool) {
	tspq.mu.RLock()
	defer tspq.mu.RUnlock()
	return tspq.pq.Peek()
}

// IsEmpty returns true if the queue is empty (thread-safe)
func (tspq *ThreadSafePriorityQueue[T]) IsEmpty() bool {
	tspq.mu.RLock()
	defer tspq.mu.RUnlock()
	return tspq.pq.IsEmpty()
}

// Size returns the number of items in the queue (thread-safe)
func (tspq *ThreadSafePriorityQueue[T]) Size() int {
	tspq.mu.RLock()
	defer tspq.mu.RUnlock()
	return tspq.pq.Size()
}

// Clear removes all items from the queue (thread-safe)
func (tspq *ThreadSafePriorityQueue[T]) Clear() {
	tspq.mu.Lock()
	defer tspq.mu.Unlock()
	tspq.pq.Clear()
}

// ToSlice returns all items as a slice (thread-safe)
func (tspq *ThreadSafePriorityQueue[T]) ToSlice() []Item[T] {
	tspq.mu.RLock()
	defer tspq.mu.RUnlock()
	return tspq.pq.ToSlice()
}

// Values returns all values in the queue (thread-safe)
func (tspq *ThreadSafePriorityQueue[T]) Values() []T {
	tspq.mu.RLock()
	defer tspq.mu.RUnlock()
	return tspq.pq.Values()
}

// Contains checks if a value exists in the queue (thread-safe)
func (tspq *ThreadSafePriorityQueue[T]) Contains(equal func(T, T) bool, value T) bool {
	tspq.mu.RLock()
	defer tspq.mu.RUnlock()
	return tspq.pq.Contains(equal, value)
}

// Find returns the item matching the predicate (thread-safe)
func (tspq *ThreadSafePriorityQueue[T]) Find(predicate func(T) bool) (*Item[T], bool) {
	tspq.mu.RLock()
	defer tspq.mu.RUnlock()
	return tspq.pq.Find(predicate)
}

// BoundedPriorityQueue is a priority queue with a maximum capacity
type BoundedPriorityQueue[T any] struct {
	pq       *PriorityQueue[T]
	maxSize  int
	mu       sync.RWMutex
	onEvict  func(T, int) // Callback when item is evicted
}

// NewBoundedMinHeap creates a bounded min-heap with maximum capacity
func NewBoundedMinHeap[T any](maxSize int) *BoundedPriorityQueue[T] {
	return &BoundedPriorityQueue[T]{
		pq:      MinHeap[T](),
		maxSize: maxSize,
	}
}

// NewBoundedMaxHeap creates a bounded max-heap with maximum capacity
func NewBoundedMaxHeap[T any](maxSize int) *BoundedPriorityQueue[T] {
	return &BoundedPriorityQueue[T]{
		pq:      MaxHeap[T](),
		maxSize: maxSize,
	}
}

// SetEvictCallback sets the callback for when items are evicted
func (bpq *BoundedPriorityQueue[T]) SetEvictCallback(callback func(T, int)) {
	bpq.mu.Lock()
	defer bpq.mu.Unlock()
	bpq.onEvict = callback
}

// PushItem adds an item, evicts lowest priority if at capacity
func (bpq *BoundedPriorityQueue[T]) PushItem(value T, priority int) (*Item[T], bool) {
	bpq.mu.Lock()
	defer bpq.mu.Unlock()

	// If at capacity and new item has higher priority than lowest
	if bpq.pq.Len() >= bpq.maxSize {
		// In min-heap, lowest priority is at top; in max-heap, lowest priority is at top
		// We need to check if the new item has better priority than the worst item
		peekVal, peekPri, ok := bpq.pq.Peek()
		if ok {
			// For min-heap: only add if new priority is lower (worse) than current worst
			// Actually for bounded queue, we want to keep highest priority items
			// So in min-heap (lower number = higher priority), we evict the highest number
			// In max-heap (higher number = higher priority), we evict the lowest number
			shouldEvict := false
			if bpq.pq.lessFunc(1, 2) { // min-heap: 1 < 2
				// In min-heap, we keep smaller numbers (higher priority)
				// Evict if new item has higher priority than current worst
				shouldEvict = priority < peekPri
			} else { // max-heap: 1 > 2
				// In max-heap, we keep larger numbers (higher priority)
				// Evict if new item has higher priority than current worst
				shouldEvict = priority > peekPri
			}

			if shouldEvict {
				evictedVal, evictedPri, _ := bpq.pq.PopItem()
				if bpq.onEvict != nil {
					bpq.onEvict(evictedVal, evictedPri)
				}
			} else {
				// New item has lower priority than worst, don't add
				return nil, false
			}
		}
	}

	return bpq.pq.PushItem(value, priority), true
}

// PopItem removes and returns the highest priority item
func (bpq *BoundedPriorityQueue[T]) PopItem() (T, int, bool) {
	bpq.mu.Lock()
	defer bpq.mu.Unlock()
	return bpq.pq.PopItem()
}

// Peek returns the highest priority item without removing it
func (bpq *BoundedPriorityQueue[T]) Peek() (T, int, bool) {
	bpq.mu.RLock()
	defer bpq.mu.RUnlock()
	return bpq.pq.Peek()
}

// IsEmpty returns true if the queue is empty
func (bpq *BoundedPriorityQueue[T]) IsEmpty() bool {
	bpq.mu.RLock()
	defer bpq.mu.RUnlock()
	return bpq.pq.IsEmpty()
}

// Size returns the number of items in the queue
func (bpq *BoundedPriorityQueue[T]) Size() int {
	bpq.mu.RLock()
	defer bpq.mu.RUnlock()
	return bpq.pq.Size()
}

// MaxSize returns the maximum capacity
func (bpq *BoundedPriorityQueue[T]) MaxSize() int {
	return bpq.maxSize
}

// IsFull returns true if the queue is at maximum capacity
func (bpq *BoundedPriorityQueue[T]) IsFull() bool {
	bpq.mu.RLock()
	defer bpq.mu.RUnlock()
	return bpq.pq.Size() >= bpq.maxSize
}

// Clear removes all items from the queue
func (bpq *BoundedPriorityQueue[T]) Clear() {
	bpq.mu.Lock()
	defer bpq.mu.Unlock()
	bpq.pq.Clear()
}

// PriorityLevel represents a priority level with helper methods
type PriorityLevel int

const (
	PriorityLowest  PriorityLevel = 0
	PriorityLow     PriorityLevel = 25
	PriorityNormal  PriorityLevel = 50
	PriorityHigh    PriorityLevel = 75
	PriorityHighest PriorityLevel = 100
	PriorityCritical PriorityLevel = 150
)

// String returns the string representation of a priority level
func (p PriorityLevel) String() string {
	switch p {
	case PriorityLowest:
		return "Lowest"
	case PriorityLow:
		return "Low"
	case PriorityNormal:
		return "Normal"
	case PriorityHigh:
		return "High"
	case PriorityHighest:
		return "Highest"
	case PriorityCritical:
		return "Critical"
	default:
		return "Custom"
	}
}

// Int returns the integer value of the priority level
func (p PriorityLevel) Int() int {
	return int(p)
}

// HigherThan checks if this priority is higher than another
func (p PriorityLevel) HigherThan(other PriorityLevel) bool {
	return p > other
}

// LowerThan checks if this priority is lower than another
func (p PriorityLevel) LowerThan(other PriorityLevel) bool {
	return p < other
}