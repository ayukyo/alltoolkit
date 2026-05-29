// Package priority_queue_utils provides a generic priority queue implementation
// with various utility functions. Zero dependencies, uses only Go standard library.
//
// Author: AllToolkit
// Version: 1.0.0
package priorityqueue

import (
	"container/heap"
	"errors"
	"fmt"
	"sort"
)

// ============================================================================
// Errors
// ============================================================================

var (
	ErrQueueEmpty      = errors.New("priority queue is empty")
	ErrItemNotFound    = errors.New("item not found in queue")
	ErrInvalidPriority = errors.New("invalid priority value")
	ErrNilItem         = errors.New("item cannot be nil")
)

// ============================================================================
// Item - Queue Item
// ============================================================================

// Item represents an element in the priority queue
type Item struct {
	Value    interface{} // The value stored in the item
	Priority float64     // The priority of the item (higher = more important)
	Index    int         // Index in the heap (maintained by heap.Interface methods)
}

// NewItem creates a new priority queue item
func NewItem(value interface{}, priority float64) *Item {
	return &Item{
		Value:    value,
		Priority: priority,
		Index:    -1,
	}
}

// String returns a string representation of the item
func (item *Item) String() string {
	return fmt.Sprintf("Item{Value: %v, Priority: %.2f, Index: %d}",
		item.Value, item.Priority, item.Index)
}

// ============================================================================
// Priority Queue (Min-Heap by default)
// ============================================================================

// PriorityQueue implements heap.Interface and holds Items
type PriorityQueue struct {
	items    []*Item
	isMaxHeap bool // true for max-heap, false for min-heap
}

// NewPriorityQueue creates a new min-heap priority queue
func NewPriorityQueue() *PriorityQueue {
	pq := &PriorityQueue{
		items:    make([]*Item, 0),
		isMaxHeap: false,
	}
	heap.Init(pq)
	return pq
}

// NewMaxPriorityQueue creates a new max-heap priority queue
func NewMaxPriorityQueue() *PriorityQueue {
	pq := &PriorityQueue{
		items:    make([]*Item, 0),
		isMaxHeap: true,
	}
	heap.Init(pq)
	return pq
}

// NewPriorityQueueWithCapacity creates a priority queue with pre-allocated capacity
func NewPriorityQueueWithCapacity(capacity int, isMaxHeap bool) *PriorityQueue {
	pq := &PriorityQueue{
		items:    make([]*Item, 0, capacity),
		isMaxHeap: isMaxHeap,
	}
	heap.Init(pq)
	return pq
}

// Len implements heap.Interface
func (pq *PriorityQueue) Len() int {
	return len(pq.items)
}

// Less implements heap.Interface
// For min-heap: items with lower priority come first
// For max-heap: items with higher priority come first
func (pq *PriorityQueue) Less(i, j int) bool {
	if pq.isMaxHeap {
		return pq.items[i].Priority > pq.items[j].Priority
	}
	return pq.items[i].Priority < pq.items[j].Priority
}

// Swap implements heap.Interface
func (pq *PriorityQueue) Swap(i, j int) {
	pq.items[i], pq.items[j] = pq.items[j], pq.items[i]
	pq.items[i].Index = i
	pq.items[j].Index = j
}

// Push implements heap.Interface
func (pq *PriorityQueue) Push(x interface{}) {
	n := len(pq.items)
	item := x.(*Item)
	item.Index = n
	pq.items = append(pq.items, item)
}

// Pop implements heap.Interface
func (pq *PriorityQueue) Pop() interface{} {
	old := pq.items
	n := len(old)
	item := old[n-1]
	old[n-1] = nil  // avoid memory leak
	item.Index = -1 // for safety
	pq.items = old[0 : n-1]
	return item
}

// ============================================================================
// Core Operations
// ============================================================================

// Enqueue adds an item to the priority queue
func (pq *PriorityQueue) Enqueue(value interface{}, priority float64) *Item {
	item := NewItem(value, priority)
	heap.Push(pq, item)
	return item
}

// Dequeue removes and returns the highest priority item (or lowest for min-heap)
func (pq *PriorityQueue) Dequeue() (*Item, error) {
	if pq.Len() == 0 {
		return nil, ErrQueueEmpty
	}
	return heap.Pop(pq).(*Item), nil
}

// Peek returns the highest priority item without removing it
func (pq *PriorityQueue) Peek() (*Item, error) {
	if pq.Len() == 0 {
		return nil, ErrQueueEmpty
	}
	return pq.items[0], nil
}

// Size returns the number of items in the queue
func (pq *PriorityQueue) Size() int {
	return pq.Len()
}

// IsEmpty returns true if the queue is empty
func (pq *PriorityQueue) IsEmpty() bool {
	return pq.Len() == 0
}

// Clear removes all items from the queue
func (pq *PriorityQueue) Clear() {
	pq.items = make([]*Item, 0)
}

// IsMaxHeap returns true if this is a max-heap
func (pq *PriorityQueue) IsMaxHeap() bool {
	return pq.isMaxHeap
}

// ============================================================================
// Update Operations
// ============================================================================

// UpdatePriority changes the priority of an item and reorders the queue
func (pq *PriorityQueue) UpdatePriority(item *Item, priority float64) error {
	if item == nil {
		return ErrNilItem
	}
	if item.Index < 0 || item.Index >= pq.Len() {
		return ErrItemNotFound
	}
	item.Priority = priority
	heap.Fix(pq, item.Index)
	return nil
}

// UpdateValue changes the value of an item
func (pq *PriorityQueue) UpdateValue(item *Item, value interface{}) error {
	if item == nil {
		return ErrNilItem
	}
	if item.Index < 0 || item.Index >= pq.Len() {
		return ErrItemNotFound
	}
	item.Value = value
	return nil
}

// Remove removes a specific item from the queue
func (pq *PriorityQueue) Remove(item *Item) error {
	if item == nil {
		return ErrNilItem
	}
	if item.Index < 0 || item.Index >= pq.Len() {
		return ErrItemNotFound
	}
	heap.Remove(pq, item.Index)
	return nil
}

// RemoveByIndex removes an item by its index
func (pq *PriorityQueue) RemoveByIndex(index int) (*Item, error) {
	if index < 0 || index >= pq.Len() {
		return nil, ErrItemNotFound
	}
	return heap.Remove(pq, index).(*Item), nil
}

// ============================================================================
// Query Operations
// ============================================================================

// Items returns a copy of all items in the queue (unordered)
func (pq *PriorityQueue) Items() []*Item {
	items := make([]*Item, len(pq.items))
	copy(items, pq.items)
	return items
}

// SortedItems returns all items sorted by priority
func (pq *PriorityQueue) SortedItems() []*Item {
	items := pq.Items()
	sort.Slice(items, func(i, j int) bool {
		if pq.isMaxHeap {
			return items[i].Priority > items[j].Priority
		}
		return items[i].Priority < items[j].Priority
	})
	return items
}

// Values returns all values in the queue (unordered)
func (pq *PriorityQueue) Values() []interface{} {
	values := make([]interface{}, len(pq.items))
	for i, item := range pq.items {
		values[i] = item.Value
	}
	return values
}

// Priorities returns all priorities in the queue (unordered)
func (pq *PriorityQueue) Priorities() []float64 {
	priorities := make([]float64, len(pq.items))
	for i, item := range pq.items {
		priorities[i] = item.Priority
	}
	return priorities
}

// Contains checks if an item with the given value exists
func (pq *PriorityQueue) Contains(value interface{}) bool {
	for _, item := range pq.items {
		if item.Value == value {
			return true
		}
	}
	return false
}

// FindByValue finds an item by its value
func (pq *PriorityQueue) FindByValue(value interface{}) *Item {
	for _, item := range pq.items {
		if item.Value == value {
			return item
		}
	}
	return nil
}

// FindAllByValue finds all items with the given value
func (pq *PriorityQueue) FindAllByValue(value interface{}) []*Item {
	var result []*Item
	for _, item := range pq.items {
		if item.Value == value {
			result = append(result, item)
		}
	}
	return result
}

// FindByPriority finds an item by its priority
func (pq *PriorityQueue) FindByPriority(priority float64) *Item {
	for _, item := range pq.items {
		if item.Priority == priority {
			return item
		}
	}
	return nil
}

// FindAllByPriorityRange finds all items within a priority range
func (pq *PriorityQueue) FindAllByPriorityRange(min, max float64) []*Item {
	var result []*Item
	for _, item := range pq.items {
		if item.Priority >= min && item.Priority <= max {
			result = append(result, item)
		}
	}
	return result
}

// ============================================================================
// Bulk Operations
// ============================================================================

// EnqueueBatch adds multiple items at once
func (pq *PriorityQueue) EnqueueBatch(items []struct {
	Value    interface{}
	Priority float64
}) []*Item {
	result := make([]*Item, len(items))
	for i, item := range items {
		result[i] = pq.Enqueue(item.Value, item.Priority)
	}
	return result
}

// DequeueN removes and returns the top N items
func (pq *PriorityQueue) DequeueN(n int) ([]*Item, error) {
	if n <= 0 {
		return nil, nil
	}
	if n > pq.Len() {
		n = pq.Len()
	}
	
	result := make([]*Item, n)
	for i := 0; i < n; i++ {
		item, err := pq.Dequeue()
		if err != nil {
			return result[:i], err
		}
		result[i] = item
	}
	return result, nil
}

// Drain removes and returns all items
func (pq *PriorityQueue) Drain() []*Item {
	items, _ := pq.DequeueN(pq.Len())
	return items
}

// ============================================================================
// Statistics
// ============================================================================

// Stats returns statistics about the queue
type Stats struct {
	Size       int
	MinPriority float64
	MaxPriority float64
	AvgPriority float64
	SumPriority  float64
	IsMaxHeap   bool
}

// GetStats returns statistics about the queue
func (pq *PriorityQueue) GetStats() Stats {
	if pq.Len() == 0 {
		return Stats{Size: 0, IsMaxHeap: pq.isMaxHeap}
	}

	min := pq.items[0].Priority
	max := pq.items[0].Priority
	sum := 0.0

	for _, item := range pq.items {
		if item.Priority < min {
			min = item.Priority
		}
		if item.Priority > max {
			max = item.Priority
		}
		sum += item.Priority
	}

	return Stats{
		Size:        pq.Len(),
		MinPriority: min,
		MaxPriority: max,
		AvgPriority: sum / float64(pq.Len()),
		SumPriority: sum,
		IsMaxHeap:   pq.isMaxHeap,
	}
}

// ============================================================================
// Utility Functions
// ============================================================================

// Merge merges two priority queues into a new one
func Merge(pq1, pq2 *PriorityQueue) *PriorityQueue {
	isMaxHeap := pq1.isMaxHeap
	result := NewPriorityQueueWithCapacity(pq1.Len()+pq2.Len(), isMaxHeap)
	
	for _, item := range pq1.items {
		result.Enqueue(item.Value, item.Priority)
	}
	for _, item := range pq2.items {
		result.Enqueue(item.Value, item.Priority)
	}
	
	return result
}

// MergeInPlace merges another queue into this one
func (pq *PriorityQueue) MergeInPlace(other *PriorityQueue) {
	for _, item := range other.items {
		pq.Enqueue(item.Value, item.Priority)
	}
}

// Clone creates a deep copy of the priority queue
func (pq *PriorityQueue) Clone() *PriorityQueue {
	newPQ := NewPriorityQueueWithCapacity(pq.Len(), pq.isMaxHeap)
	for _, item := range pq.items {
		newPQ.Enqueue(item.Value, item.Priority)
	}
	return newPQ
}

// Reverse creates a new queue with inverted priorities
func (pq *PriorityQueue) Reverse() *PriorityQueue {
	newPQ := NewPriorityQueueWithCapacity(pq.Len(), !pq.isMaxHeap)
	for _, item := range pq.items {
		// Invert the priority to reverse the order
		newPQ.Enqueue(item.Value, -item.Priority)
	}
	return newPQ
}

// ============================================================================
// Typed Priority Queue (for common types)
// ============================================================================

// IntPriorityQueue is a specialized priority queue for integers
type IntPriorityQueue struct {
	*PriorityQueue
}

// NewIntPriorityQueue creates a new integer priority queue
func NewIntPriorityQueue() *IntPriorityQueue {
	return &IntPriorityQueue{NewPriorityQueue()}
}

// Enqueue adds an integer with priority
func (pq *IntPriorityQueue) Enqueue(value, priority int) {
	pq.PriorityQueue.Enqueue(value, float64(priority))
}

// Dequeue removes and returns the top integer
func (pq *IntPriorityQueue) Dequeue() (int, error) {
	item, err := pq.PriorityQueue.Dequeue()
	if err != nil {
		return 0, err
	}
	return item.Value.(int), nil
}

// Peek returns the top integer without removing it
func (pq *IntPriorityQueue) Peek() (int, error) {
	item, err := pq.PriorityQueue.Peek()
	if err != nil {
		return 0, err
	}
	return item.Value.(int), nil
}

// StringPriorityQueue is a specialized priority queue for strings
type StringPriorityQueue struct {
	*PriorityQueue
}

// NewStringPriorityQueue creates a new string priority queue
func NewStringPriorityQueue() *StringPriorityQueue {
	return &StringPriorityQueue{NewPriorityQueue()}
}

// Enqueue adds a string with priority
func (pq *StringPriorityQueue) Enqueue(value string, priority float64) {
	pq.PriorityQueue.Enqueue(value, priority)
}

// Dequeue removes and returns the top string
func (pq *StringPriorityQueue) Dequeue() (string, error) {
	item, err := pq.PriorityQueue.Dequeue()
	if err != nil {
		return "", err
	}
	return item.Value.(string), nil
}

// Peek returns the top string without removing it
func (pq *StringPriorityQueue) Peek() (string, error) {
	item, err := pq.PriorityQueue.Peek()
	if err != nil {
		return "", err
	}
	return item.Value.(string), nil
}

// ============================================================================
// String Representation
// ============================================================================

// String returns a string representation of the queue
func (pq *PriorityQueue) String() string {
	heapType := "min-heap"
	if pq.isMaxHeap {
		heapType = "max-heap"
	}
	return fmt.Sprintf("PriorityQueue{%s, size: %d}", heapType, pq.Len())
}

// DebugString returns a detailed string representation for debugging
func (pq *PriorityQueue) DebugString() string {
	if pq.Len() == 0 {
		return "PriorityQueue{empty}"
	}
	
	result := fmt.Sprintf("PriorityQueue{%s, items:\n", map[bool]string{true: "max-heap", false: "min-heap"}[pq.isMaxHeap])
	for _, item := range pq.SortedItems() {
		result += fmt.Sprintf("  %v (priority: %.2f)\n", item.Value, item.Priority)
	}
	result += "}"
	return result
}