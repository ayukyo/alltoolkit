// Package deque_utils provides a generic double-ended queue (deque) implementation
// with comprehensive operations for efficient insertion and removal at both ends.
// 
// A deque (pronounced "deck") is a linear collection that supports element
// insertion and removal at both ends. It's more versatile than a stack or queue
// and is used in many algorithms including:
// - Sliding window algorithms
// - BFS and graph algorithms
// - Palindrome checking
// - Expression evaluation
// - Task scheduling
package deque_utils

import (
	"errors"
	"fmt"
	"strings"
)

// ============================================================================
// Core Types
// ============================================================================

// ErrEmptyDeque is returned when attempting to access an element from an empty deque
var ErrEmptyDeque = errors.New("deque is empty")

// ErrIndexOutOfRange is returned when the index is out of valid range
var ErrIndexOutOfRange = errors.New("index out of range")

// Deque is a generic double-ended queue implementation
type Deque[T any] struct {
	data []T
}

// NewDeque creates a new empty deque
func NewDeque[T any]() *Deque[T] {
	return &Deque[T]{
		data: make([]T, 0),
	}
}

// NewDequeWithCapacity creates a new deque with initial capacity
func NewDequeWithCapacity[T any](capacity int) *Deque[T] {
	return &Deque[T]{
		data: make([]T, 0, capacity),
	}
}

// NewDequeFromSlice creates a deque from an existing slice
func NewDequeFromSlice[T any](items []T) *Deque[T] {
	data := make([]T, len(items))
	copy(data, items)
	return &Deque[T]{data: data}
}

// ============================================================================
// Basic Operations
// ============================================================================

// PushFront adds an element to the front of the deque
func (d *Deque[T]) PushFront(item T) {
	d.data = append([]T{item}, d.data...)
}

// PushBack adds an element to the back of the deque
func (d *Deque[T]) PushBack(item T) {
	d.data = append(d.data, item)
}

// PopFront removes and returns the element at the front of the deque
// Returns ErrEmptyDeque if the deque is empty
func (d *Deque[T]) PopFront() (T, error) {
	var zero T
	if len(d.data) == 0 {
		return zero, ErrEmptyDeque
	}
	item := d.data[0]
	d.data = d.data[1:]
	return item, nil
}

// PopBack removes and returns the element at the back of the deque
// Returns ErrEmptyDeque if the deque is empty
func (d *Deque[T]) PopBack() (T, error) {
	var zero T
	if len(d.data) == 0 {
		return zero, ErrEmptyDeque
	}
	item := d.data[len(d.data)-1]
	d.data = d.data[:len(d.data)-1]
	return item, nil
}

// Front returns the element at the front without removing it
// Returns ErrEmptyDeque if the deque is empty
func (d *Deque[T]) Front() (T, error) {
	var zero T
	if len(d.data) == 0 {
		return zero, ErrEmptyDeque
	}
	return d.data[0], nil
}

// Back returns the element at the back without removing it
// Returns ErrEmptyDeque if the deque is empty
func (d *Deque[T]) Back() (T, error) {
	var zero T
	if len(d.data) == 0 {
		return zero, ErrEmptyDeque
	}
	return d.data[len(d.data)-1], nil
}

// ============================================================================
// Collection Properties
// ============================================================================

// Len returns the number of elements in the deque
func (d *Deque[T]) Len() int {
	return len(d.data)
}

// IsEmpty returns true if the deque contains no elements
func (d *Deque[T]) IsEmpty() bool {
	return len(d.data) == 0
}

// Clear removes all elements from the deque
func (d *Deque[T]) Clear() {
	d.data = make([]T, 0)
}

// Cap returns the current capacity of the deque
func (d *Deque[T]) Cap() int {
	return cap(d.data)
}

// ============================================================================
// Random Access
// ============================================================================

// Get returns the element at the specified index
// Returns ErrIndexOutOfRange if index is out of range
func (d *Deque[T]) Get(index int) (T, error) {
	var zero T
	if index < 0 || index >= len(d.data) {
		return zero, ErrIndexOutOfRange
	}
	return d.data[index], nil
}

// Set sets the element at the specified index
// Returns ErrIndexOutOfRange if index is out of range
func (d *Deque[T]) Set(index int, item T) error {
	if index < 0 || index >= len(d.data) {
		return ErrIndexOutOfRange
	}
	d.data[index] = item
	return nil
}

// ============================================================================
// Bulk Operations
// ============================================================================

// PushFrontAll adds all elements from a slice to the front of the deque
// Elements are added in order, so the first element of the slice
// will be at the very front after this operation
func (d *Deque[T]) PushFrontAll(items []T) {
	if len(items) == 0 {
		return
	}
	newData := make([]T, 0, len(items)+len(d.data))
	newData = append(newData, items...)
	newData = append(newData, d.data...)
	d.data = newData
}

// PushBackAll adds all elements from a slice to the back of the deque
func (d *Deque[T]) PushBackAll(items []T) {
	d.data = append(d.data, items...)
}

// PopFrontN removes and returns n elements from the front
// Returns an error if n > Len()
func (d *Deque[T]) PopFrontN(n int) ([]T, error) {
	if n > len(d.data) {
		return nil, fmt.Errorf("cannot pop %d elements from deque of size %d", n, len(d.data))
	}
	if n <= 0 {
		return []T{}, nil
	}
	result := make([]T, n)
	copy(result, d.data[:n])
	d.data = d.data[n:]
	return result, nil
}

// PopBackN removes and returns n elements from the back
// Returns an error if n > Len()
func (d *Deque[T]) PopBackN(n int) ([]T, error) {
	if n > len(d.data) {
		return nil, fmt.Errorf("cannot pop %d elements from deque of size %d", n, len(d.data))
	}
	if n <= 0 {
		return []T{}, nil
	}
	start := len(d.data) - n
	result := make([]T, n)
	copy(result, d.data[start:])
	d.data = d.data[:start]
	return result, nil
}

// ============================================================================
// Search Operations
// ============================================================================

// Contains returns true if the deque contains an element that equals the target
func (d *Deque[T]) Contains(target T, equals func(a, b T) bool) bool {
	for _, item := range d.data {
		if equals(item, target) {
			return true
		}
	}
	return false
}

// IndexOf returns the first index of the target element, or -1 if not found
func (d *Deque[T]) IndexOf(target T, equals func(a, b T) bool) int {
	for i, item := range d.data {
		if equals(item, target) {
			return i
		}
	}
	return -1
}

// LastIndexOf returns the last index of the target element, or -1 if not found
func (d *Deque[T]) LastIndexOf(target T, equals func(a, b T) bool) int {
	for i := len(d.data) - 1; i >= 0; i-- {
		if equals(d.data[i], target) {
			return i
		}
	}
	return -1
}

// Find returns the first element that matches the predicate, or an error if none found
func (d *Deque[T]) Find(predicate func(T) bool) (T, error) {
	for _, item := range d.data {
		if predicate(item) {
			return item, nil
		}
	}
	var zero T
	return zero, errors.New("no element matches predicate")
}

// FindAll returns all elements that match the predicate
func (d *Deque[T]) FindAll(predicate func(T) bool) []T {
	result := make([]T, 0)
	for _, item := range d.data {
		if predicate(item) {
			result = append(result, item)
		}
	}
	return result
}

// Count returns the number of elements that match the predicate
func (d *Deque[T]) Count(predicate func(T) bool) int {
	count := 0
	for _, item := range d.data {
		if predicate(item) {
			count++
		}
	}
	return count
}

// ============================================================================
// Modification Operations
// ============================================================================

// InsertAt inserts an element at the specified index
// Returns ErrIndexOutOfRange if index is out of valid range [0, Len()]
func (d *Deque[T]) InsertAt(index int, item T) error {
	if index < 0 || index > len(d.data) {
		return ErrIndexOutOfRange
	}
	if index == 0 {
		d.PushFront(item)
		return nil
	}
	if index == len(d.data) {
		d.PushBack(item)
		return nil
	}
	d.data = append(d.data[:index], append([]T{item}, d.data[index:]...)...)
	return nil
}

// RemoveAt removes the element at the specified index
// Returns ErrIndexOutOfRange if index is out of range
func (d *Deque[T]) RemoveAt(index int) (T, error) {
	var zero T
	if index < 0 || index >= len(d.data) {
		return zero, ErrIndexOutOfRange
	}
	item := d.data[index]
	d.data = append(d.data[:index], d.data[index+1:]...)
	return item, nil
}

// Remove removes the first element that matches the predicate
// Returns true if an element was removed
func (d *Deque[T]) Remove(predicate func(T) bool) bool {
	for i, item := range d.data {
		if predicate(item) {
			d.data = append(d.data[:i], d.data[i+1:]...)
			return true
		}
	}
	return false
}

// RemoveAll removes all elements that match the predicate
// Returns the number of elements removed
func (d *Deque[T]) RemoveAll(predicate func(T) bool) int {
	count := 0
	newData := make([]T, 0, len(d.data))
	for _, item := range d.data {
		if !predicate(item) {
			newData = append(newData, item)
		} else {
			count++
		}
	}
	d.data = newData
	return count
}

// ============================================================================
// Transformation Operations
// ============================================================================

// Map applies a function to each element and returns a new deque
func Map[T, U any](d *Deque[T], transform func(T) U) *Deque[U] {
	result := NewDequeWithCapacity[U](d.Len())
	for _, item := range d.data {
		result.PushBack(transform(item))
	}
	return result
}

// Filter returns a new deque containing only elements that match the predicate
func (d *Deque[T]) Filter(predicate func(T) bool) *Deque[T] {
	result := NewDeque[T]()
	for _, item := range d.data {
		if predicate(item) {
			result.PushBack(item)
		}
	}
	return result
}

// Reduce reduces the deque to a single value using the accumulator function
func Reduce[T, U any](d *Deque[T], initial U, accumulator func(U, T) U) U {
	result := initial
	for _, item := range d.data {
		result = accumulator(result, item)
	}
	return result
}

// ForEach applies a function to each element
func (d *Deque[T]) ForEach(action func(T)) {
	for _, item := range d.data {
		action(item)
	}
}

// Reverse reverses the deque in place
func (d *Deque[T]) Reverse() {
	for i, j := 0, len(d.data)-1; i < j; i, j = i+1, j-1 {
		d.data[i], d.data[j] = d.data[j], d.data[i]
	}
}

// Reversed returns a new deque with elements in reverse order
func (d *Deque[T]) Reversed() *Deque[T] {
	result := NewDequeWithCapacity[T](d.Len())
	for i := len(d.data) - 1; i >= 0; i-- {
		result.PushBack(d.data[i])
	}
	return result
}

// RotateLeft rotates the deque to the left by n positions
func (d *Deque[T]) RotateLeft(n int) {
	if d.Len() == 0 {
		return
	}
	n = n % d.Len()
	if n < 0 {
		n += d.Len()
	}
	if n == 0 {
		return
	}
	d.data = append(d.data[n:], d.data[:n]...)
}

// RotateRight rotates the deque to the right by n positions
func (d *Deque[T]) RotateRight(n int) {
	d.RotateLeft(-n)
}

// ============================================================================
// Slice Operations
// ============================================================================

// ToSlice returns a copy of the deque as a slice
func (d *Deque[T]) ToSlice() []T {
	result := make([]T, len(d.data))
	copy(result, d.data)
	return result
}

// SubDeque returns a new deque with elements from start to end (exclusive)
func (d *Deque[T]) SubDeque(start, end int) (*Deque[T], error) {
	if start < 0 || end > len(d.data) || start > end {
		return nil, ErrIndexOutOfRange
	}
	return NewDequeFromSlice(d.data[start:end]), nil
}

// Take returns a new deque with the first n elements
func (d *Deque[T]) Take(n int) *Deque[T] {
	if n <= 0 {
		return NewDeque[T]()
	}
	if n >= len(d.data) {
		return NewDequeFromSlice(d.ToSlice())
	}
	return NewDequeFromSlice(d.data[:n])
}

// TakeLast returns a new deque with the last n elements
func (d *Deque[T]) TakeLast(n int) *Deque[T] {
	if n <= 0 {
		return NewDeque[T]()
	}
	if n >= len(d.data) {
		return NewDequeFromSlice(d.ToSlice())
	}
	return NewDequeFromSlice(d.data[len(d.data)-n:])
}

// Skip returns a new deque skipping the first n elements
func (d *Deque[T]) Skip(n int) *Deque[T] {
	if n <= 0 {
		return NewDequeFromSlice(d.ToSlice())
	}
	if n >= len(d.data) {
		return NewDeque[T]()
	}
	return NewDequeFromSlice(d.data[n:])
}

// ============================================================================
// Comparison Operations
// ============================================================================

// Equal returns true if both deques have the same elements in the same order
func (d *Deque[T]) Equal(other *Deque[T], equals func(a, b T) bool) bool {
	if d.Len() != other.Len() {
		return false
	}
	for i := 0; i < d.Len(); i++ {
		if !equals(d.data[i], other.data[i]) {
			return false
		}
	}
	return true
}

// ============================================================================
// Conversion Operations
// ============================================================================

// String returns a string representation of the deque
func (d *Deque[T]) String() string {
	var sb strings.Builder
	sb.WriteString("Deque[")
	for i, item := range d.data {
		if i > 0 {
			sb.WriteString(", ")
		}
		sb.WriteString(fmt.Sprintf("%v", item))
	}
	sb.WriteString("]")
	return sb.String()
}

// ============================================================================
// Utility Functions
// ============================================================================

// Clone returns a shallow copy of the deque
func (d *Deque[T]) Clone() *Deque[T] {
	return NewDequeFromSlice(d.ToSlice())
}

// Append appends another deque to the end of this deque
func (d *Deque[T]) Append(other *Deque[T]) {
	d.data = append(d.data, other.data...)
}

// Prepend prepends another deque to the front of this deque
func (d *Deque[T]) Prepend(other *Deque[T]) {
	newData := make([]T, 0, len(other.data)+len(d.data))
	newData = append(newData, other.data...)
	newData = append(newData, d.data...)
	d.data = newData
}

// Swap swaps two elements at the given indices
func (d *Deque[T]) Swap(i, j int) error {
	if i < 0 || i >= len(d.data) || j < 0 || j >= len(d.data) {
		return ErrIndexOutOfRange
	}
	d.data[i], d.data[j] = d.data[j], d.data[i]
	return nil
}

// ============================================================================
// Special Operations for Common Use Cases
// ============================================================================

// PushFrontIfEmpty adds an element to the front only if the deque is empty
// Returns true if the element was added
func (d *Deque[T]) PushFrontIfEmpty(item T) bool {
	if d.IsEmpty() {
		d.PushFront(item)
		return true
	}
	return false
}

// PushBackIfEmpty adds an element to the back only if the deque is empty
// Returns true if the element was added
func (d *Deque[T]) PushBackIfEmpty(item T) bool {
	if d.IsEmpty() {
		d.PushBack(item)
		return true
	}
	return false
}

// PopFrontOrDefault removes and returns the front element, or returns the default if empty
func (d *Deque[T]) PopFrontOrDefault(defaultValue T) T {
	if d.IsEmpty() {
		return defaultValue
	}
	item, _ := d.PopFront()
	return item
}

// PopBackOrDefault removes and returns the back element, or returns the default if empty
func (d *Deque[T]) PopBackOrDefault(defaultValue T) T {
	if d.IsEmpty() {
		return defaultValue
	}
	item, _ := d.PopBack()
	return item
}

// FrontOrDefault returns the front element, or returns the default if empty
func (d *Deque[T]) FrontOrDefault(defaultValue T) T {
	if d.IsEmpty() {
		return defaultValue
	}
	item, _ := d.Front()
	return item
}

// BackOrDefault returns the back element, or returns the default if empty
func (d *Deque[T]) BackOrDefault(defaultValue T) T {
	if d.IsEmpty() {
		return defaultValue
	}
	item, _ := d.Back()
	return item
}

// EnsureCapacity ensures the deque has at least the specified capacity
func (d *Deque[T]) EnsureCapacity(capacity int) {
	if cap(d.data) < capacity {
		newData := make([]T, len(d.data), capacity)
		copy(newData, d.data)
		d.data = newData
	}
}

// TrimExcess reduces capacity to match size
func (d *Deque[T]) TrimExcess() {
	if len(d.data) < cap(d.data) {
		newData := make([]T, len(d.data))
		copy(newData, d.data)
		d.data = newData
	}
}

// ============================================================================
// Order Statistics
// ============================================================================

// Min returns the minimum element according to the less function
func (d *Deque[T]) Min(less func(a, b T) bool) (T, error) {
	var zero T
	if d.IsEmpty() {
		return zero, ErrEmptyDeque
	}
	min := d.data[0]
	for i := 1; i < len(d.data); i++ {
		if less(d.data[i], min) {
			min = d.data[i]
		}
	}
	return min, nil
}

// Max returns the maximum element according to the less function
func (d *Deque[T]) Max(less func(a, b T) bool) (T, error) {
	var zero T
	if d.IsEmpty() {
		return zero, ErrEmptyDeque
	}
	max := d.data[0]
	for i := 1; i < len(d.data); i++ {
		if less(max, d.data[i]) {
			max = d.data[i]
		}
	}
	return max, nil
}

// All returns true if all elements match the predicate
func (d *Deque[T]) All(predicate func(T) bool) bool {
	for _, item := range d.data {
		if !predicate(item) {
			return false
		}
	}
	return true
}

// Any returns true if any element matches the predicate
func (d *Deque[T]) Any(predicate func(T) bool) bool {
	for _, item := range d.data {
		if predicate(item) {
			return true
		}
	}
	return false
}

// First returns the first element that matches the predicate, or an error
func (d *Deque[T]) First(predicate func(T) bool) (T, error) {
	for _, item := range d.data {
		if predicate(item) {
			return item, nil
		}
	}
	var zero T
	return zero, errors.New("no element matches predicate")
}

// Last returns the last element that matches the predicate, or an error
func (d *Deque[T]) Last(predicate func(T) bool) (T, error) {
	for i := len(d.data) - 1; i >= 0; i-- {
		if predicate(d.data[i]) {
			return d.data[i], nil
		}
	}
	var zero T
	return zero, errors.New("no element matches predicate")
}

// ============================================================================
// Iterator
// ============================================================================

// Iterator returns a channel that yields elements from front to back
func (d *Deque[T]) Iterator() <-chan T {
	ch := make(chan T)
	go func() {
		defer close(ch)
		for _, item := range d.data {
			ch <- item
		}
	}()
	return ch
}

// ReverseIterator returns a channel that yields elements from back to front
func (d *Deque[T]) ReverseIterator() <-chan T {
	ch := make(chan T)
	go func() {
		defer close(ch)
		for i := len(d.data) - 1; i >= 0; i-- {
			ch <- d.data[i]
		}
	}()
	return ch
}