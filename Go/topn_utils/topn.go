// Package topn_utils provides efficient Top-N selection algorithms
// for finding the top N largest or smallest elements from a collection.
package topn_utils

import (
	"container/heap"
	"sort"
)

// TopNFinder finds the top N elements from a collection efficiently.
// Uses min-heap for finding largest elements and max-heap for smallest.
type TopNFinder struct {
	n int
}

// NewTopNFinder creates a new TopNFinder for finding top N elements.
func NewTopNFinder(n int) *TopNFinder {
	if n <= 0 {
		n = 1
	}
	return &TopNFinder{n: n}
}

// ========== Min Heap for Top N Largest ==========

type minHeap struct {
	data []int
}

func (h *minHeap) Len() int           { return len(h.data) }
func (h *minHeap) Less(i, j int) bool { return h.data[i] < h.data[j] }
func (h *minHeap) Swap(i, j int)      { h.data[i], h.data[j] = h.data[j], h.data[i] }

func (h *minHeap) Push(x interface{}) {
	h.data = append(h.data, x.(int))
}

func (h *minHeap) Pop() interface{} {
	old := h.data
	n := len(old)
	x := old[n-1]
	h.data = old[0 : n-1]
	return x
}

// ========== Max Heap for Top N Smallest ==========

type maxHeap struct {
	data []int
}

func (h *maxHeap) Len() int           { return len(h.data) }
func (h *maxHeap) Less(i, j int) bool { return h.data[i] > h.data[j] }
func (h *maxHeap) Swap(i, j int)      { h.data[i], h.data[j] = h.data[j], h.data[i] }

func (h *maxHeap) Push(x interface{}) {
	h.data = append(h.data, x.(int))
}

func (h *maxHeap) Pop() interface{} {
	old := h.data
	n := len(old)
	x := old[n-1]
	h.data = old[0 : n-1]
	return x
}

// ========== Int Operations ==========

// Largest finds the top N largest integers from a slice.
// Returns sorted in descending order.
// Time: O(n log k), Space: O(k) where k is N
func (t *TopNFinder) Largest(data []int) []int {
	if len(data) == 0 || t.n <= 0 {
		return []int{}
	}

	n := min(t.n, len(data))

	// Use min-heap to track N largest elements
	h := &minHeap{data: make([]int, 0, n)}
	heap.Init(h)

	for _, v := range data {
		if h.Len() < n {
			heap.Push(h, v)
		} else if v > h.data[0] {
			heap.Pop(h)
			heap.Push(h, v)
		}
	}

	// Extract and sort in descending order
	result := make([]int, h.Len())
	for i := len(result) - 1; i >= 0; i-- {
		result[i] = heap.Pop(h).(int)
	}

	return result
}

// Smallest finds the top N smallest integers from a slice.
// Returns sorted in ascending order.
// Time: O(n log k), Space: O(k) where k is N
func (t *TopNFinder) Smallest(data []int) []int {
	if len(data) == 0 || t.n <= 0 {
		return []int{}
	}

	n := min(t.n, len(data))

	// Use max-heap to track N smallest elements
	h := &maxHeap{data: make([]int, 0, n)}
	heap.Init(h)

	for _, v := range data {
		if h.Len() < n {
			heap.Push(h, v)
		} else if v < h.data[0] {
			heap.Pop(h)
			heap.Push(h, v)
		}
	}

	// Extract and sort in ascending order
	result := make([]int, h.Len())
	for i := len(result) - 1; i >= 0; i-- {
		result[i] = heap.Pop(h).(int)
	}

	return result
}

// ========== Float64 Operations ==========

type minHeapFloat struct {
	data []float64
}

func (h *minHeapFloat) Len() int           { return len(h.data) }
func (h *minHeapFloat) Less(i, j int) bool { return h.data[i] < h.data[j] }
func (h *minHeapFloat) Swap(i, j int)      { h.data[i], h.data[j] = h.data[j], h.data[i] }

func (h *minHeapFloat) Push(x interface{}) {
	h.data = append(h.data, x.(float64))
}

func (h *minHeapFloat) Pop() interface{} {
	old := h.data
	n := len(old)
	x := old[n-1]
	h.data = old[0 : n-1]
	return x
}

type maxHeapFloat struct {
	data []float64
}

func (h *maxHeapFloat) Len() int           { return len(h.data) }
func (h *maxHeapFloat) Less(i, j int) bool { return h.data[i] > h.data[j] }
func (h *maxHeapFloat) Swap(i, j int)      { h.data[i], h.data[j] = h.data[j], h.data[i] }

func (h *maxHeapFloat) Push(x interface{}) {
	h.data = append(h.data, x.(float64))
}

func (h *maxHeapFloat) Pop() interface{} {
	old := h.data
	n := len(old)
	x := old[n-1]
	h.data = old[0 : n-1]
	return x
}

// LargestFloats finds the top N largest float64 values from a slice.
func (t *TopNFinder) LargestFloats(data []float64) []float64 {
	if len(data) == 0 || t.n <= 0 {
		return []float64{}
	}

	n := min(t.n, len(data))
	h := &minHeapFloat{data: make([]float64, 0, n)}
	heap.Init(h)

	for _, v := range data {
		if h.Len() < n {
			heap.Push(h, v)
		} else if v > h.data[0] {
			heap.Pop(h)
			heap.Push(h, v)
		}
	}

	result := make([]float64, h.Len())
	for i := len(result) - 1; i >= 0; i-- {
		result[i] = heap.Pop(h).(float64)
	}

	return result
}

// SmallestFloats finds the top N smallest float64 values from a slice.
func (t *TopNFinder) SmallestFloats(data []float64) []float64 {
	if len(data) == 0 || t.n <= 0 {
		return []float64{}
	}

	n := min(t.n, len(data))
	h := &maxHeapFloat{data: make([]float64, 0, n)}
	heap.Init(h)

	for _, v := range data {
		if h.Len() < n {
			heap.Push(h, v)
		} else if v < h.data[0] {
			heap.Pop(h)
			heap.Push(h, v)
		}
	}

	result := make([]float64, h.Len())
	for i := len(result) - 1; i >= 0; i-- {
		result[i] = heap.Pop(h).(float64)
	}

	return result
}

// ========== String Operations ==========

type minHeapString struct {
	data []string
}

func (h *minHeapString) Len() int           { return len(h.data) }
func (h *minHeapString) Less(i, j int) bool { return h.data[i] < h.data[j] }
func (h *minHeapString) Swap(i, j int)      { h.data[i], h.data[j] = h.data[j], h.data[i] }

func (h *minHeapString) Push(x interface{}) {
	h.data = append(h.data, x.(string))
}

func (h *minHeapString) Pop() interface{} {
	old := h.data
	n := len(old)
	x := old[n-1]
	h.data = old[0 : n-1]
	return x
}

type maxHeapString struct {
	data []string
}

func (h *maxHeapString) Len() int           { return len(h.data) }
func (h *maxHeapString) Less(i, j int) bool { return h.data[i] > h.data[j] }
func (h *maxHeapString) Swap(i, j int)      { h.data[i], h.data[j] = h.data[j], h.data[i] }

func (h *maxHeapString) Push(x interface{}) {
	h.data = append(h.data, x.(string))
}

func (h *maxHeapString) Pop() interface{} {
	old := h.data
	n := len(old)
	x := old[n-1]
	h.data = old[0 : n-1]
	return x
}

// LargestStrings finds the top N largest strings (lexicographically) from a slice.
func (t *TopNFinder) LargestStrings(data []string) []string {
	if len(data) == 0 || t.n <= 0 {
		return []string{}
	}

	n := min(t.n, len(data))
	h := &minHeapString{data: make([]string, 0, n)}
	heap.Init(h)

	for _, v := range data {
		if h.Len() < n {
			heap.Push(h, v)
		} else if v > h.data[0] {
			heap.Pop(h)
			heap.Push(h, v)
		}
	}

	result := make([]string, h.Len())
	for i := len(result) - 1; i >= 0; i-- {
		result[i] = heap.Pop(h).(string)
	}

	return result
}

// SmallestStrings finds the top N smallest strings (lexicographically) from a slice.
func (t *TopNFinder) SmallestStrings(data []string) []string {
	if len(data) == 0 || t.n <= 0 {
		return []string{}
	}

	n := min(t.n, len(data))
	h := &maxHeapString{data: make([]string, 0, n)}
	heap.Init(h)

	for _, v := range data {
		if h.Len() < n {
			heap.Push(h, v)
		} else if v < h.data[0] {
			heap.Pop(h)
			heap.Push(h, v)
		}
	}

	result := make([]string, h.Len())
	for i := len(result) - 1; i >= 0; i-- {
		result[i] = heap.Pop(h).(string)
	}

	return result
}

// ========== Generic Operations with Custom Comparator ==========

// Item represents an item with a value and comparable score
type Item struct {
	Value interface{}
	Score float64
}

type minHeapItem struct {
	data []Item
}

func (h *minHeapItem) Len() int           { return len(h.data) }
func (h *minHeapItem) Less(i, j int) bool { return h.data[i].Score < h.data[j].Score }
func (h *minHeapItem) Swap(i, j int)      { h.data[i], h.data[j] = h.data[j], h.data[i] }

func (h *minHeapItem) Push(x interface{}) {
	h.data = append(h.data, x.(Item))
}

func (h *minHeapItem) Pop() interface{} {
	old := h.data
	n := len(old)
	x := old[n-1]
	h.data = old[0 : n-1]
	return x
}

type maxHeapItem struct {
	data []Item
}

func (h *maxHeapItem) Len() int           { return len(h.data) }
func (h *maxHeapItem) Less(i, j int) bool { return h.data[i].Score > h.data[j].Score }
func (h *maxHeapItem) Swap(i, j int)      { h.data[i], h.data[j] = h.data[j], h.data[i] }

func (h *maxHeapItem) Push(x interface{}) {
	h.data = append(h.data, x.(Item))
}

func (h *maxHeapItem) Pop() interface{} {
	old := h.data
	n := len(old)
	x := old[n-1]
	h.data = old[0 : n-1]
	return x
}

// LargestItems finds the top N items with highest scores.
func (t *TopNFinder) LargestItems(items []Item) []Item {
	if len(items) == 0 || t.n <= 0 {
		return []Item{}
	}

	n := min(t.n, len(items))
	h := &minHeapItem{data: make([]Item, 0, n)}
	heap.Init(h)

	for _, v := range items {
		if h.Len() < n {
			heap.Push(h, v)
		} else if v.Score > h.data[0].Score {
			heap.Pop(h)
			heap.Push(h, v)
		}
	}

	result := make([]Item, h.Len())
	for i := len(result) - 1; i >= 0; i-- {
		result[i] = heap.Pop(h).(Item)
	}

	return result
}

// SmallestItems finds the top N items with lowest scores.
func (t *TopNFinder) SmallestItems(items []Item) []Item {
	if len(items) == 0 || t.n <= 0 {
		return []Item{}
	}

	n := min(t.n, len(items))
	h := &maxHeapItem{data: make([]Item, 0, n)}
	heap.Init(h)

	for _, v := range items {
		if h.Len() < n {
			heap.Push(h, v)
		} else if v.Score < h.data[0].Score {
			heap.Pop(h)
			heap.Push(h, v)
		}
	}

	result := make([]Item, h.Len())
	for i := len(result) - 1; i >= 0; i-- {
		result[i] = heap.Pop(h).(Item)
	}

	return result
}

// ========== Utility Functions ==========

// QuickSelect uses quickselect algorithm to find the k-th smallest element.
// Average O(n), worst O(n²)
func QuickSelect(data []int, k int) int {
	if len(data) == 0 || k < 0 || k >= len(data) {
		return 0
	}
	return quickSelectHelper(data, 0, len(data)-1, k)
}

func quickSelectHelper(data []int, left, right, k int) int {
	if left == right {
		return data[left]
	}

	pivotIndex := partition(data, left, right)

	if k == pivotIndex {
		return data[k]
	} else if k < pivotIndex {
		return quickSelectHelper(data, left, pivotIndex-1, k)
	}
	return quickSelectHelper(data, pivotIndex+1, right, k)
}

func partition(data []int, left, right int) int {
	pivot := data[right]
	i := left

	for j := left; j < right; j++ {
		if data[j] <= pivot {
			data[i], data[j] = data[j], data[i]
			i++
		}
	}
	data[i], data[right] = data[right], data[i]
	return i
}

// KthSmallest finds the k-th smallest element (1-indexed).
func KthSmallest(data []int, k int) int {
	if k < 1 || k > len(data) {
		return 0
	}
	return QuickSelect(data, k-1)
}

// KthLargest finds the k-th largest element (1-indexed).
func KthLargest(data []int, k int) int {
	if k < 1 || k > len(data) {
		return 0
	}
	return QuickSelect(data, len(data)-k)
}

// Median finds the median value of a slice.
func Median(data []int) float64 {
	n := len(data)
	if n == 0 {
		return 0
	}

	// Create a copy to avoid modifying original
	sorted := make([]int, n)
	copy(sorted, data)
	sort.Ints(sorted)

	if n%2 == 1 {
		return float64(sorted[n/2])
	}
	return float64(sorted[n/2-1]+sorted[n/2]) / 2
}

// Percentile finds the value at the given percentile (0-100).
func Percentile(data []int, percentile float64) int {
	n := len(data)
	if n == 0 || percentile < 0 || percentile > 100 {
		return 0
	}

	sorted := make([]int, n)
	copy(sorted, data)
	sort.Ints(sorted)

	index := int(float64(n-1) * percentile / 100)
	return sorted[index]
}

// ========== Convenience Functions ==========

// TopNLargest is a convenience function to find top N largest integers.
func TopNLargest(data []int, n int) []int {
	finder := NewTopNFinder(n)
	return finder.Largest(data)
}

// TopNSmallest is a convenience function to find top N smallest integers.
func TopNSmallest(data []int, n int) []int {
	finder := NewTopNFinder(n)
	return finder.Smallest(data)
}