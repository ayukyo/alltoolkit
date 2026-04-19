// Package ring_buffer_utils provides circular buffer (ring buffer) implementations.
//
// Ring buffers are fixed-size buffers that overwrite the oldest data when full.
// They are useful for:
//   - Fixed-size queues
//   - Rolling window statistics
//   - Event buffering
//   - Data stream processing
//
// Features:
//   - Zero external dependencies
//   - Generic type support (Go 1.18+)
//   - Thread-safe option
//   - Statistical operations for numeric buffers
package ring_buffer_utils

import (
	"errors"
	"math"
	"sync"
)

// Common errors
var (
	ErrBufferEmpty   = errors.New("buffer is empty")
	ErrBufferFull    = errors.New("buffer is full")
	ErrInvalidIndex  = errors.New("index out of range")
	ErrInvalidSize   = errors.New("invalid size: must be positive")
	ErrInsufficientData = errors.New("insufficient data for operation")
)

// RingBuffer is a generic circular buffer implementation.
// When the buffer is full, new elements overwrite the oldest ones.
type RingBuffer[T any] struct {
	data     []T
	head     int // write position
	count    int
	capacity int
	mu       sync.RWMutex
	threadSafe bool
}

// NewRingBuffer creates a new ring buffer with the specified capacity.
func NewRingBuffer[T any](capacity int) *RingBuffer[T] {
	if capacity <= 0 {
		panic(ErrInvalidSize)
	}
	return &RingBuffer[T]{
		data:     make([]T, capacity),
		head:     0,
		count:    0,
		capacity: capacity,
	}
}

// NewThreadSafeRingBuffer creates a thread-safe ring buffer.
func NewThreadSafeRingBuffer[T any](capacity int) *RingBuffer[T] {
	rb := NewRingBuffer[T](capacity)
	rb.threadSafe = true
	return rb
}

// Push adds an element to the buffer, overwriting the oldest if full.
// Returns the overwritten element (if any) and whether an element was overwritten.
func (rb *RingBuffer[T]) Push(item T) (T, bool) {
	if rb.threadSafe {
		rb.mu.Lock()
		defer rb.mu.Unlock()
	}
	
	var zero T
	var overwritten T
	wasOverwritten := false
	
	if rb.count == rb.capacity {
		// Get the element that will be overwritten
		oldestIdx := (rb.head - rb.count + rb.capacity) % rb.capacity
		overwritten = rb.data[oldestIdx]
		wasOverwritten = true
	}
	
	rb.data[rb.head] = item
	rb.head = (rb.head + 1) % rb.capacity
	
	if rb.count < rb.capacity {
		rb.count++
	}
	
	return overwritten, wasOverwritten
}

// Pop removes and returns the newest element.
// Returns ErrBufferEmpty if the buffer is empty.
func (rb *RingBuffer[T]) Pop() (T, error) {
	if rb.threadSafe {
		rb.mu.Lock()
		defer rb.mu.Unlock()
	}
	
	var zero T
	if rb.count == 0 {
		return zero, ErrBufferEmpty
	}
	
	rb.head = (rb.head - 1 + rb.capacity) % rb.capacity
	item := rb.data[rb.head]
	rb.data[rb.head] = zero // clear reference
	rb.count--
	
	return item, nil
}

// PopLeft removes and returns the oldest element.
// Returns ErrBufferEmpty if the buffer is empty.
func (rb *RingBuffer[T]) PopLeft() (T, error) {
	if rb.threadSafe {
		rb.mu.Lock()
		defer rb.mu.Unlock()
	}
	
	var zero T
	if rb.count == 0 {
		return zero, ErrBufferEmpty
	}
	
	oldestIdx := (rb.head - rb.count + rb.capacity) % rb.capacity
	item := rb.data[oldestIdx]
	rb.data[oldestIdx] = zero // clear reference
	rb.count--
	
	return item, nil
}

// Peek returns the newest element without removing it.
func (rb *RingBuffer[T]) Peek() (T, error) {
	if rb.threadSafe {
		rb.mu.RLock()
		defer rb.mu.RUnlock()
	}
	
	var zero T
	if rb.count == 0 {
		return zero, ErrBufferEmpty
	}
	
	newestIdx := (rb.head - 1 + rb.capacity) % rb.capacity
	return rb.data[newestIdx], nil
}

// PeekLeft returns the oldest element without removing it.
func (rb *RingBuffer[T]) PeekLeft() (T, error) {
	if rb.threadSafe {
		rb.mu.RLock()
		defer rb.mu.RUnlock()
	}
	
	var zero T
	if rb.count == 0 {
		return zero, ErrBufferEmpty
	}
	
	oldestIdx := (rb.head - rb.count + rb.capacity) % rb.capacity
	return rb.data[oldestIdx], nil
}

// Get returns the element at the specified index (0 = oldest).
func (rb *RingBuffer[T]) Get(index int) (T, error) {
	if rb.threadSafe {
		rb.mu.RLock()
		defer rb.mu.RUnlock()
	}
	
	var zero T
	if index < 0 || index >= rb.count {
		return zero, ErrInvalidIndex
	}
	
	actualIdx := (rb.head - rb.count + index + rb.capacity) % rb.capacity
	return rb.data[actualIdx], nil
}

// Set sets the element at the specified index.
func (rb *RingBuffer[T]) Set(index int, item T) error {
	if rb.threadSafe {
		rb.mu.Lock()
		defer rb.mu.Unlock()
	}
	
	if index < 0 || index >= rb.count {
		return ErrInvalidIndex
	}
	
	actualIdx := (rb.head - rb.count + index + rb.capacity) % rb.capacity
	rb.data[actualIdx] = item
	return nil
}

// Len returns the current number of elements.
func (rb *RingBuffer[T]) Len() int {
	if rb.threadSafe {
		rb.mu.RLock()
		defer rb.mu.RUnlock()
	}
	return rb.count
}

// Cap returns the buffer capacity.
func (rb *RingBuffer[T]) Cap() int {
	return rb.capacity
}

// IsFull returns true if the buffer is full.
func (rb *RingBuffer[T]) IsFull() bool {
	if rb.threadSafe {
		rb.mu.RLock()
		defer rb.mu.RUnlock()
	}
	return rb.count == rb.capacity
}

// IsEmpty returns true if the buffer is empty.
func (rb *RingBuffer[T]) IsEmpty() bool {
	if rb.threadSafe {
		rb.mu.RLock()
		defer rb.mu.RUnlock()
	}
	return rb.count == 0
}

// Clear removes all elements from the buffer.
func (rb *RingBuffer[T]) Clear() {
	if rb.threadSafe {
		rb.mu.Lock()
		defer rb.mu.Unlock()
	}
	
	var zero T
	for i := range rb.data {
		rb.data[i] = zero
	}
	rb.head = 0
	rb.count = 0
}

// ToSlice returns all elements as a slice (oldest first).
func (rb *RingBuffer[T]) ToSlice() []T {
	if rb.threadSafe {
		rb.mu.RLock()
		defer rb.mu.RUnlock()
	}
	
	if rb.count == 0 {
		return []T{}
	}
	
	result := make([]T, rb.count)
	startIdx := (rb.head - rb.count + rb.capacity) % rb.capacity
	for i := 0; i < rb.count; i++ {
		result[i] = rb.data[(startIdx+i)%rb.capacity]
	}
	return result
}

// Extend adds multiple elements to the buffer.
func (rb *RingBuffer[T]) Extend(items []T) {
	for _, item := range items {
		rb.Push(item)
	}
}

// ForEach iterates over all elements (oldest first).
func (rb *RingBuffer[T]) ForEach(fn func(T) bool) {
	if rb.threadSafe {
		rb.mu.RLock()
		defer rb.mu.RUnlock()
	}
	
	if rb.count == 0 {
		return
	}
	
	startIdx := (rb.head - rb.count + rb.capacity) % rb.capacity
	for i := 0; i < rb.count; i++ {
		if !fn(rb.data[(startIdx+i)%rb.capacity]) {
			break
		}
	}
}

// Contains checks if an element exists in the buffer.
func (rb *RingBuffer[T]) Contains(item T, equal func(T, T) bool) bool {
	if rb.threadSafe {
		rb.mu.RLock()
		defer rb.mu.RUnlock()
	}
	
	found := false
	rb.forEachInternal(func(v T) bool {
		if equal(v, item) {
			found = true
			return false
		}
		return true
	})
	return found
}

// Reverse returns a reversed copy of the buffer (newest first).
func (rb *RingBuffer[T]) Reverse() []T {
	slice := rb.ToSlice()
	for i, j := 0, len(slice)-1; i < j; i, j = i+1, j-1 {
		slice[i], slice[j] = slice[j], slice[i]
	}
	return slice
}

// Copy creates a new buffer with the same content.
func (rb *RingBuffer[T]) Copy() *RingBuffer[T] {
	if rb.threadSafe {
		rb.mu.RLock()
		defer rb.mu.RUnlock()
	}
	
	newBuffer := NewRingBuffer[T](rb.capacity)
	newBuffer.threadSafe = rb.threadSafe
	newBuffer.count = rb.count
	newBuffer.head = rb.head
	copy(newBuffer.data, rb.data)
	return newBuffer
}

// internal iterator without locks
func (rb *RingBuffer[T]) forEachInternal(fn func(T) bool) {
	if rb.count == 0 {
		return
	}
	
	startIdx := (rb.head - rb.count + rb.capacity) % rb.capacity
	for i := 0; i < rb.count; i++ {
		if !fn(rb.data[(startIdx+i)%rb.capacity]) {
			break
		}
	}
}

// NumericRingBuffer is a ring buffer for numeric types with statistical operations.
type NumericRingBuffer struct {
	*RingBuffer[float64]
	sum    float64
	sumSq  float64
	min    float64
	max    float64
	hasMinMax bool
}

// NewNumericRingBuffer creates a numeric ring buffer with statistical capabilities.
func NewNumericRingBuffer(capacity int) *NumericRingBuffer {
	return &NumericRingBuffer{
		RingBuffer: NewRingBuffer[float64](capacity),
	}
}

// NewThreadSafeNumericRingBuffer creates a thread-safe numeric ring buffer.
func NewThreadSafeNumericRingBuffer(capacity int) *NumericRingBuffer {
	rb := NewNumericRingBuffer(capacity)
	rb.threadSafe = true
	return rb
}

// Push adds a value and updates statistics.
func (nrb *NumericRingBuffer) Push(value float64) (float64, bool) {
	if nrb.threadSafe {
		nrb.mu.Lock()
		defer nrb.mu.Unlock()
	}
	
	var overwritten float64
	wasOverwritten := false
	
	// If buffer is full, subtract the overwritten value
	if nrb.count == nrb.capacity {
		oldestIdx := (nrb.head - nrb.count + nrb.capacity) % nrb.capacity
		overwritten = nrb.data[oldestIdx]
		wasOverwritten = true
		nrb.sum -= overwritten
		nrb.sumSq -= overwritten * overwritten
	}
	
	nrb.data[nrb.head] = value
	nrb.head = (nrb.head + 1) % nrb.capacity
	
	if nrb.count < nrb.capacity {
		nrb.count++
	}
	
	nrb.sum += value
	nrb.sumSq += value * value
	
	// Update min/max
	if !nrb.hasMinMax {
		nrb.min = value
		nrb.max = value
		nrb.hasMinMax = true
	} else {
		if value < nrb.min {
			nrb.min = value
		}
		if value > nrb.max {
			nrb.max = value
		}
	}
	
	return overwritten, wasOverwritten
}

// Clear resets the buffer and statistics.
func (nrb *NumericRingBuffer) Clear() {
	if nrb.threadSafe {
		nrb.mu.Lock()
		defer nrb.mu.Unlock()
	}
	
	for i := range nrb.data {
		nrb.data[i] = 0
	}
	nrb.head = 0
	nrb.count = 0
	nrb.sum = 0
	nrb.sumSq = 0
	nrb.hasMinMax = false
}

// Mean returns the arithmetic mean.
func (nrb *NumericRingBuffer) Mean() (float64, error) {
	if nrb.threadSafe {
		nrb.mu.RLock()
		defer nrb.mu.RUnlock()
	}
	
	if nrb.count == 0 {
		return 0, ErrBufferEmpty
	}
	return nrb.sum / float64(nrb.count), nil
}

// Sum returns the sum of all elements.
func (nrb *NumericRingBuffer) Sum() float64 {
	if nrb.threadSafe {
		nrb.mu.RLock()
		defer nrb.mu.RUnlock()
	}
	return nrb.sum
}

// Variance returns the sample variance.
func (nrb *NumericRingBuffer) Variance() (float64, error) {
	if nrb.threadSafe {
		nrb.mu.RLock()
		defer nrb.mu.RUnlock()
	}
	
	if nrb.count < 2 {
		return 0, ErrInsufficientData
	}
	
	mean := nrb.sum / float64(nrb.count)
	return (nrb.sumSq - float64(nrb.count)*mean*mean) / float64(nrb.count-1), nil
}

// StdDev returns the sample standard deviation.
func (nrb *NumericRingBuffer) StdDev() (float64, error) {
	variance, err := nrb.Variance()
	if err != nil {
		return 0, err
	}
	return math.Sqrt(variance), nil
}

// Min returns the minimum value.
func (nrb *NumericRingBuffer) Min() (float64, error) {
	if nrb.threadSafe {
		nrb.mu.RLock()
		defer nrb.mu.RUnlock()
	}
	
	if !nrb.hasMinMax {
		return 0, ErrBufferEmpty
	}
	return nrb.min, nil
}

// Max returns the maximum value.
func (nrb *NumericRingBuffer) Max() (float64, error) {
	if nrb.threadSafe {
		nrb.mu.RLock()
		defer nrb.mu.RUnlock()
	}
	
	if !nrb.hasMinMax {
		return 0, ErrBufferEmpty
	}
	return nrb.max, nil
}

// Range returns the difference between max and min.
func (nrb *NumericRingBuffer) Range() (float64, error) {
	min, err := nrb.Min()
	if err != nil {
		return 0, err
	}
	max, err := nrb.Max()
	if err != nil {
		return 0, err
	}
	return max - min, nil
}

// MovingAverage computes moving average with the specified window size.
func (nrb *NumericRingBuffer) MovingAverage(window int) ([]float64, error) {
	if nrb.threadSafe {
		nrb.mu.RLock()
		defer nrb.mu.RUnlock()
	}
	
	if window > nrb.count {
		return nil, ErrInsufficientData
	}
	if window <= 0 {
		return nil, ErrInvalidSize
	}
	
	data := nrb.ToSlice()
	result := make([]float64, 0, len(data)-window+1)
	
	for i := 0; i <= len(data)-window; i++ {
		sum := 0.0
		for j := 0; j < window; j++ {
			sum += data[i+j]
		}
		result = append(result, sum/float64(window))
	}
	
	return result, nil
}

// Median returns the median of all elements.
func (nrb *NumericRingBuffer) Median() (float64, error) {
	if nrb.threadSafe {
		nrb.mu.RLock()
		defer nrb.mu.RUnlock()
	}
	
	if nrb.count == 0 {
		return 0, ErrBufferEmpty
	}
	
	data := nrb.ToSlice()
	sorted := make([]float64, len(data))
	copy(sorted, data)
	
	// Simple insertion sort for median
	for i := 1; i < len(sorted); i++ {
		for j := i; j > 0 && sorted[j] < sorted[j-1]; j-- {
			sorted[j], sorted[j-1] = sorted[j-1], sorted[j]
		}
	}
	
	mid := len(sorted) / 2
	if len(sorted)%2 == 0 {
		return (sorted[mid-1] + sorted[mid]) / 2, nil
	}
	return sorted[mid], nil
}

// Percentile returns the value at the given percentile (0-100).
func (nrb *NumericRingBuffer) Percentile(p float64) (float64, error) {
	if nrb.threadSafe {
		nrb.mu.RLock()
		defer nrb.mu.RUnlock()
	}
	
	if nrb.count == 0 {
		return 0, ErrBufferEmpty
	}
	if p < 0 || p > 100 {
		return 0, errors.New("percentile must be between 0 and 100")
	}
	
	data := nrb.ToSlice()
	sorted := make([]float64, len(data))
	copy(sorted, data)
	
	// Sort
	for i := 1; i < len(sorted); i++ {
		for j := i; j > 0 && sorted[j] < sorted[j-1]; j-- {
			sorted[j], sorted[j-1] = sorted[j-1], sorted[j]
		}
	}
	
	if p == 100 {
		return sorted[len(sorted)-1], nil
	}
	
	index := (p / 100) * float64(len(sorted)-1)
	lower := int(index)
	upper := lower + 1
	
	if upper >= len(sorted) {
		return sorted[lower], nil
	}
	
	frac := index - float64(lower)
	return sorted[lower] + frac*(sorted[upper]-sorted[lower]), nil
}

// SlidingWindow creates a sliding window iterator.
func SlidingWindow[T any](data []T, windowSize int) [][]T {
	if windowSize <= 0 || len(data) < windowSize {
		return nil
	}
	
	result := make([][]T, 0, len(data)-windowSize+1)
	for i := 0; i <= len(data)-windowSize; i++ {
		window := make([]T, windowSize)
		copy(window, data[i:i+windowSize])
		result = append(result, window)
	}
	return result
}

// Batch processes data in fixed-size batches.
func Batch[T any, R any](data []T, batchSize int, processor func([]T) R) []R {
	if batchSize <= 0 {
		return nil
	}
	
	results := make([]R, 0, (len(data)+batchSize-1)/batchSize)
	for i := 0; i < len(data); i += batchSize {
		end := i + batchSize
		if end > len(data) {
			end = len(data)
		}
		results = append(results, processor(data[i:end]))
	}
	return results
}