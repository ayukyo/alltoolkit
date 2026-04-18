// Package slice_utils provides comprehensive slice manipulation utilities for Go.
// Zero external dependencies - uses only Go standard library.
package slice_utils

import (
	"errors"
	"math/rand"
	"reflect"
	"sort"
)

// =============================================================================
// Basic Operations
// =============================================================================

// Contains checks if a slice contains a specific element.
func Contains[T comparable](slice []T, element T) bool {
	for _, item := range slice {
		if item == element {
			return true
		}
	}
	return false
}

// ContainsAll checks if a slice contains all specified elements.
func ContainsAll[T comparable](slice []T, elements []T) bool {
	for _, elem := range elements {
		if !Contains(slice, elem) {
			return false
		}
	}
	return true
}

// ContainsAny checks if a slice contains any of the specified elements.
func ContainsAny[T comparable](slice []T, elements []T) bool {
	for _, elem := range elements {
		if Contains(slice, elem) {
			return true
		}
	}
	return false
}

// IndexOf returns the index of the first occurrence of an element, or -1 if not found.
func IndexOf[T comparable](slice []T, element T) int {
	for i, item := range slice {
		if item == element {
			return i
		}
	}
	return -1
}

// LastIndexOf returns the index of the last occurrence of an element, or -1 if not found.
func LastIndexOf[T comparable](slice []T, element T) int {
	for i := len(slice) - 1; i >= 0; i-- {
		if slice[i] == element {
			return i
		}
	}
	return -1
}

// Count counts the occurrences of an element in a slice.
func Count[T comparable](slice []T, element T) int {
	count := 0
	for _, item := range slice {
		if item == element {
			count++
		}
	}
	return count
}

// CountBy counts elements that satisfy a predicate.
func CountBy[T any](slice []T, predicate func(T) bool) int {
	count := 0
	for _, item := range slice {
		if predicate(item) {
			count++
		}
	}
	return count
}

// =============================================================================
// Transformation Operations
// =============================================================================

// Map transforms each element using a mapper function.
func Map[T any, U any](slice []T, mapper func(T) U) []U {
	result := make([]U, len(slice))
	for i, item := range slice {
		result[i] = mapper(item)
	}
	return result
}

// Filter returns elements that satisfy a predicate.
func Filter[T any](slice []T, predicate func(T) bool) []T {
	result := make([]T, 0)
	for _, item := range slice {
		if predicate(item) {
			result = append(result, item)
		}
	}
	return result
}

// Reject returns elements that do NOT satisfy a predicate.
func Reject[T any](slice []T, predicate func(T) bool) []T {
	result := make([]T, 0)
	for _, item := range slice {
		if !predicate(item) {
			result = append(result, item)
		}
	}
	return result
}

// Reduce reduces a slice to a single value using an accumulator function.
func Reduce[T any, U any](slice []T, initial U, accumulator func(U, T) U) U {
	result := initial
	for _, item := range slice {
		result = accumulator(result, item)
	}
	return result
}

// ReduceRight reduces a slice from right to left.
func ReduceRight[T any, U any](slice []T, initial U, accumulator func(U, T) U) U {
	result := initial
	for i := len(slice) - 1; i >= 0; i-- {
		result = accumulator(result, slice[i])
	}
	return result
}

// ForEach executes a function for each element.
func ForEach[T any](slice []T, action func(T)) {
	for _, item := range slice {
		action(item)
	}
}

// ForEachWithIndex executes a function for each element with index.
func ForEachWithIndex[T any](slice []T, action func(int, T)) {
	for i, item := range slice {
		action(i, item)
	}
}

// FlatMap maps each element to a slice and flattens the result.
func FlatMap[T any, U any](slice []T, mapper func(T) []U) []U {
	result := make([]U, 0)
	for _, item := range slice {
		result = append(result, mapper(item)...)
	}
	return result
}

// =============================================================================
// Slice Manipulation
// =============================================================================

// Chunk splits a slice into chunks of specified size.
func Chunk[T any](slice []T, size int) ([][]T, error) {
	if size <= 0 {
		return nil, errors.New("chunk size must be positive")
	}
	
	chunks := make([][]T, 0, (len(slice)+size-1)/size)
	for i := 0; i < len(slice); i += size {
		end := i + size
		if end > len(slice) {
			end = len(slice)
		}
		chunks = append(chunks, slice[i:end])
	}
	return chunks, nil
}

// Flatten flattens a 2D slice into a 1D slice.
func Flatten[T any](slices [][]T) []T {
	totalLen := 0
	for _, s := range slices {
		totalLen += len(s)
	}
	result := make([]T, 0, totalLen)
	for _, s := range slices {
		result = append(result, s...)
	}
	return result
}

// Reverse reverses a slice in place.
func Reverse[T any](slice []T) {
	for i, j := 0, len(slice)-1; i < j; i, j = i+1, j-1 {
		slice[i], slice[j] = slice[j], slice[i]
	}
}

// Reversed returns a new reversed slice.
func Reversed[T any](slice []T) []T {
	result := make([]T, len(slice))
	for i, item := range slice {
		result[len(slice)-1-i] = item
	}
	return result
}

// Slice returns a portion of a slice with safe bounds.
func Slice[T any](slice []T, start, end int) []T {
	if start < 0 {
		start = 0
	}
	if end > len(slice) {
		end = len(slice)
	}
	if start >= end {
		return []T{}
	}
	return slice[start:end]
}

// Take returns the first n elements.
func Take[T any](slice []T, n int) []T {
	if n <= 0 {
		return []T{}
	}
	if n > len(slice) {
		n = len(slice)
	}
	return slice[:n]
}

// TakeWhile takes elements while predicate is true.
func TakeWhile[T any](slice []T, predicate func(T) bool) []T {
	result := make([]T, 0)
	for _, item := range slice {
		if !predicate(item) {
			break
		}
		result = append(result, item)
	}
	return result
}

// TakeLast returns the last n elements.
func TakeLast[T any](slice []T, n int) []T {
	if n <= 0 {
		return []T{}
	}
	if n > len(slice) {
		n = len(slice)
	}
	return slice[len(slice)-n:]
}

// Drop removes the first n elements.
func Drop[T any](slice []T, n int) []T {
	if n <= 0 {
		return slice
	}
	if n >= len(slice) {
		return []T{}
	}
	return slice[n:]
}

// DropWhile drops elements while predicate is true.
func DropWhile[T any](slice []T, predicate func(T) bool) []T {
	for i, item := range slice {
		if !predicate(item) {
			return slice[i:]
		}
	}
	return []T{}
}

// DropLast removes the last n elements.
func DropLast[T any](slice []T, n int) []T {
	if n <= 0 {
		return slice
	}
	if n >= len(slice) {
		return []T{}
	}
	return slice[:len(slice)-n]
}

// =============================================================================
// Set Operations
// =============================================================================

// Unique returns a slice with unique elements, preserving order.
func Unique[T comparable](slice []T) []T {
	seen := make(map[T]bool)
	result := make([]T, 0)
	for _, item := range slice {
		if !seen[item] {
			seen[item] = true
			result = append(result, item)
		}
	}
	return result
}

// UniqueBy returns a slice with unique elements based on a key function.
func UniqueBy[T any, K comparable](slice []T, keyFunc func(T) K) []T {
	seen := make(map[K]bool)
	result := make([]T, 0)
	for _, item := range slice {
		key := keyFunc(item)
		if !seen[key] {
			seen[key] = true
			result = append(result, item)
		}
	}
	return result
}

// Union returns the union of two slices.
func Union[T comparable](slice1, slice2 []T) []T {
	return Unique(append(slice1, slice2...))
}

// Intersection returns the intersection of two slices.
func Intersection[T comparable](slice1, slice2 []T) []T {
	set2 := make(map[T]bool)
	for _, item := range slice2 {
		set2[item] = true
	}
	
	result := make([]T, 0)
	seen := make(map[T]bool)
	for _, item := range slice1 {
		if set2[item] && !seen[item] {
			seen[item] = true
			result = append(result, item)
		}
	}
	return result
}

// Difference returns elements in slice1 that are not in slice2.
func Difference[T comparable](slice1, slice2 []T) []T {
	set2 := make(map[T]bool)
	for _, item := range slice2 {
		set2[item] = true
	}
	
	result := make([]T, 0)
	for _, item := range slice1 {
		if !set2[item] {
			result = append(result, item)
		}
	}
	return result
}

// SymmetricDifference returns elements in either slice but not in both.
func SymmetricDifference[T comparable](slice1, slice2 []T) []T {
	set1 := make(map[T]bool)
	set2 := make(map[T]bool)
	
	for _, item := range slice1 {
		set1[item] = true
	}
	for _, item := range slice2 {
		set2[item] = true
	}
	
	result := make([]T, 0)
	for _, item := range slice1 {
		if !set2[item] {
			result = append(result, item)
		}
	}
	for _, item := range slice2 {
		if !set1[item] {
			result = append(result, item)
		}
	}
	return result
}

// IsSubset checks if slice1 is a subset of slice2.
func IsSubset[T comparable](slice1, slice2 []T) bool {
	set2 := make(map[T]bool)
	for _, item := range slice2 {
		set2[item] = true
	}
	for _, item := range slice1 {
		if !set2[item] {
			return false
		}
	}
	return true
}

// IsSuperset checks if slice1 is a superset of slice2.
func IsSuperset[T comparable](slice1, slice2 []T) bool {
	return IsSubset(slice2, slice1)
}

// =============================================================================
// Sorting Operations
// =============================================================================

// SortBy sorts a slice by a key function.
func SortBy[T any, K ordered](slice []T, keyFunc func(T) K) {
	sort.Slice(slice, func(i, j int) bool {
		return keyFunc(slice[i]) < keyFunc(slice[j])
	})
}

// SortByDesc sorts a slice by a key function in descending order.
func SortByDesc[T any, K ordered](slice []T, keyFunc func(T) K) {
	sort.Slice(slice, func(i, j int) bool {
		return keyFunc(slice[i]) > keyFunc(slice[j])
	})
}

// SortedBy returns a new slice sorted by a key function.
func SortedBy[T any, K ordered](slice []T, keyFunc func(T) K) []T {
	result := make([]T, len(slice))
	copy(result, slice)
	SortBy(result, keyFunc)
	return result
}

// ordered is a constraint for types that can be ordered.
type ordered interface {
	~int | ~int8 | ~int16 | ~int32 | ~int64 |
		~uint | ~uint8 | ~uint16 | ~uint32 | ~uint64 | ~uintptr |
		~float32 | ~float64 | ~string
}

// Min returns the minimum element in a slice.
func Min[T ordered](slice []T) (T, error) {
	if len(slice) == 0 {
		var zero T
		return zero, errors.New("slice is empty")
	}
	min := slice[0]
	for _, item := range slice[1:] {
		if item < min {
			min = item
		}
	}
	return min, nil
}

// Max returns the maximum element in a slice.
func Max[T ordered](slice []T) (T, error) {
	if len(slice) == 0 {
		var zero T
		return zero, errors.New("slice is empty")
	}
	max := slice[0]
	for _, item := range slice[1:] {
		if item > max {
			max = item
		}
	}
	return max, nil
}

// MinBy returns the minimum element by a key function.
func MinBy[T any, K ordered](slice []T, keyFunc func(T) K) (T, error) {
	if len(slice) == 0 {
		var zero T
		return zero, errors.New("slice is empty")
	}
	minIdx := 0
	minKey := keyFunc(slice[0])
	for i, item := range slice[1:] {
		key := keyFunc(item)
		if key < minKey {
			minKey = key
			minIdx = i + 1
		}
	}
	return slice[minIdx], nil
}

// MaxBy returns the maximum element by a key function.
func MaxBy[T any, K ordered](slice []T, keyFunc func(T) K) (T, error) {
	if len(slice) == 0 {
		var zero T
		return zero, errors.New("slice is empty")
	}
	maxIdx := 0
	maxKey := keyFunc(slice[0])
	for i, item := range slice[1:] {
		key := keyFunc(item)
		if key > maxKey {
			maxKey = key
			maxIdx = i + 1
		}
	}
	return slice[maxIdx], nil
}

// =============================================================================
// Search Operations
// =============================================================================

// Find returns the first element that satisfies a predicate.
func Find[T any](slice []T, predicate func(T) bool) (T, bool) {
	for _, item := range slice {
		if predicate(item) {
			return item, true
		}
	}
	var zero T
	return zero, false
}

// FindIndex returns the index of the first element that satisfies a predicate.
func FindIndex[T any](slice []T, predicate func(T) bool) int {
	for i, item := range slice {
		if predicate(item) {
			return i
		}
	}
	return -1
}

// FindLast returns the last element that satisfies a predicate.
func FindLast[T any](slice []T, predicate func(T) bool) (T, bool) {
	for i := len(slice) - 1; i >= 0; i-- {
		if predicate(slice[i]) {
			return slice[i], true
		}
	}
	var zero T
	return zero, false
}

// FindLastIndex returns the index of the last element that satisfies a predicate.
func FindLastIndex[T any](slice []T, predicate func(T) bool) int {
	for i := len(slice) - 1; i >= 0; i-- {
		if predicate(slice[i]) {
			return i
		}
	}
	return -1
}

// FindAll returns all elements that satisfy a predicate (alias for Filter).
func FindAll[T any](slice []T, predicate func(T) bool) []T {
	return Filter(slice, predicate)
}

// Every checks if all elements satisfy a predicate.
func Every[T any](slice []T, predicate func(T) bool) bool {
	for _, item := range slice {
		if !predicate(item) {
			return false
		}
	}
	return true
}

// Some checks if any element satisfies a predicate.
func Some[T any](slice []T, predicate func(T) bool) bool {
	for _, item := range slice {
		if predicate(item) {
			return true
		}
	}
	return false
}

// None checks if no element satisfies a predicate.
func None[T any](slice []T, predicate func(T) bool) bool {
	return !Some(slice, predicate)
}

// =============================================================================
// Partition and Grouping
// =============================================================================

// Partition splits a slice into two slices based on a predicate.
func Partition[T any](slice []T, predicate func(T) bool) (matched, unmatched []T) {
	for _, item := range slice {
		if predicate(item) {
			matched = append(matched, item)
		} else {
			unmatched = append(unmatched, item)
		}
	}
	return matched, unmatched
}

// GroupBy groups elements by a key function.
func GroupBy[T any, K comparable](slice []T, keyFunc func(T) K) map[K][]T {
	result := make(map[K][]T)
	for _, item := range slice {
		key := keyFunc(item)
		result[key] = append(result[key], item)
	}
	return result
}

// GroupByToMap groups elements and transforms each group.
func GroupByToMap[T any, K comparable, V any](slice []T, keyFunc func(T) K, valueFunc func(T) V) map[K][]V {
	result := make(map[K][]V)
	for _, item := range slice {
		key := keyFunc(item)
		result[key] = append(result[key], valueFunc(item))
	}
	return result
}

// CountBy groups elements and counts occurrences of each key.
func CountByKeys[T any, K comparable](slice []T, keyFunc func(T) K) map[K]int {
	result := make(map[K]int)
	for _, item := range slice {
		key := keyFunc(item)
		result[key]++
	}
	return result
}

// =============================================================================
// Insert, Remove, Replace Operations
// =============================================================================

// Insert inserts an element at the specified index.
func Insert[T any](slice []T, index int, element T) ([]T, error) {
	if index < 0 || index > len(slice) {
		return nil, errors.New("index out of bounds")
	}
	result := make([]T, 0, len(slice)+1)
	result = append(result, slice[:index]...)
	result = append(result, element)
	result = append(result, slice[index:]...)
	return result, nil
}

// InsertAll inserts multiple elements at the specified index.
func InsertAll[T any](slice []T, index int, elements []T) ([]T, error) {
	if index < 0 || index > len(slice) {
		return nil, errors.New("index out of bounds")
	}
	result := make([]T, 0, len(slice)+len(elements))
	result = append(result, slice[:index]...)
	result = append(result, elements...)
	result = append(result, slice[index:]...)
	return result, nil
}

// Remove removes the element at the specified index.
func Remove[T any](slice []T, index int) ([]T, error) {
	if index < 0 || index >= len(slice) {
		return nil, errors.New("index out of bounds")
	}
	result := make([]T, 0, len(slice)-1)
	result = append(result, slice[:index]...)
	result = append(result, slice[index+1:]...)
	return result, nil
}

// RemoveFirst removes the first occurrence of an element.
func RemoveFirst[T comparable](slice []T, element T) []T {
	for i, item := range slice {
		if item == element {
			result := make([]T, 0, len(slice)-1)
			result = append(result, slice[:i]...)
			result = append(result, slice[i+1:]...)
			return result
		}
	}
	return slice
}

// RemoveAll removes all occurrences of an element.
func RemoveAll[T comparable](slice []T, element T) []T {
	result := make([]T, 0, len(slice))
	for _, item := range slice {
		if item != element {
			result = append(result, item)
		}
	}
	return result
}

// Replace replaces the element at the specified index.
func Replace[T any](slice []T, index int, element T) ([]T, error) {
	if index < 0 || index >= len(slice) {
		return nil, errors.New("index out of bounds")
	}
	result := make([]T, len(slice))
	copy(result, slice)
	result[index] = element
	return result, nil
}

// ReplaceAll replaces all occurrences of old element with new element.
func ReplaceAll[T comparable](slice []T, old, new T) []T {
	result := make([]T, len(slice))
	for i, item := range slice {
		if item == old {
			result[i] = new
		} else {
			result[i] = item
		}
	}
	return result
}

// =============================================================================
// Shuffling and Sampling
// =============================================================================

// Shuffle shuffles a slice in place.
func Shuffle[T any](slice []T) {
	rand.Shuffle(len(slice), func(i, j int) {
		slice[i], slice[j] = slice[j], slice[i]
	})
}

// Shuffled returns a new shuffled slice.
func Shuffled[T any](slice []T) []T {
	result := make([]T, len(slice))
	copy(result, slice)
	Shuffle(result)
	return result
}

// Sample returns n random elements from the slice.
func Sample[T any](slice []T, n int) ([]T, error) {
	if n < 0 {
		return nil, errors.New("sample size cannot be negative")
	}
	if n > len(slice) {
		return nil, errors.New("sample size cannot exceed slice length")
	}
	
	shuffled := Shuffled(slice)
	return shuffled[:n], nil
}

// RandomElement returns a random element from the slice.
func RandomElement[T any](slice []T) (T, error) {
	if len(slice) == 0 {
		var zero T
		return zero, errors.New("slice is empty")
	}
	return slice[rand.Intn(len(slice))], nil
}

// =============================================================================
// Utility Functions
// =============================================================================

// Clone returns a shallow copy of a slice.
func Clone[T any](slice []T) []T {
	result := make([]T, len(slice))
	copy(result, slice)
	return result
}

// Concat concatenates multiple slices.
func Concat[T any](slices ...[]T) []T {
	totalLen := 0
	for _, s := range slices {
		totalLen += len(s)
	}
	result := make([]T, 0, totalLen)
	for _, s := range slices {
		result = append(result, s...)
	}
	return result
}

// Repeat creates a slice with repeated elements.
func Repeat[T any](element T, count int) ([]T, error) {
	if count < 0 {
		return nil, errors.New("count cannot be negative")
	}
	result := make([]T, count)
	for i := range result {
		result[i] = element
	}
	return result, nil
}

// Range creates a slice of integers from start to end (exclusive).
func Range(start, end int) []int {
	if start >= end {
		return []int{}
	}
	result := make([]int, end-start)
	for i := range result {
		result[i] = start + i
	}
	return result
}

// RangeWithStep creates a slice of integers with a step.
func RangeWithStep(start, end, step int) ([]int, error) {
	if step == 0 {
		return nil, errors.New("step cannot be zero")
	}
	result := make([]int, 0)
	if step > 0 {
		for i := start; i < end; i += step {
			result = append(result, i)
		}
	} else {
		for i := start; i > end; i += step {
			result = append(result, i)
		}
	}
	return result, nil
}

// Fill fills a slice with a value.
func Fill[T any](slice []T, value T) {
	for i := range slice {
		slice[i] = value
	}
}

// IsEmpty checks if a slice is empty.
func IsEmpty[T any](slice []T) bool {
	return len(slice) == 0
}

// IsNotEmpty checks if a slice is not empty.
func IsNotEmpty[T any](slice []T) bool {
	return len(slice) > 0
}

// Length returns the length of a slice.
func Length[T any](slice []T) int {
	return len(slice)
}

// First returns the first element of a slice.
func First[T any](slice []T) (T, error) {
	if len(slice) == 0 {
		var zero T
		return zero, errors.New("slice is empty")
	}
	return slice[0], nil
}

// Last returns the last element of a slice.
func Last[T any](slice []T) (T, error) {
	if len(slice) == 0 {
		var zero T
		return zero, errors.New("slice is empty")
	}
	return slice[len(slice)-1], nil
}

// Second returns the second element of a slice.
func Second[T any](slice []T) (T, error) {
	if len(slice) < 2 {
		var zero T
		return zero, errors.New("slice has less than 2 elements")
	}
	return slice[1], nil
}

// Third returns the third element of a slice.
func Third[T any](slice []T) (T, error) {
	if len(slice) < 3 {
		var zero T
		return zero, errors.New("slice has less than 3 elements")
	}
	return slice[2], nil
}

// Nth returns the nth element (supports negative indices from end).
func Nth[T any](slice []T, n int) (T, error) {
	if n < 0 {
		n = len(slice) + n
	}
	if n < 0 || n >= len(slice) {
		var zero T
		return zero, errors.New("index out of bounds")
	}
	return slice[n], nil
}

// Head is an alias for First.
func Head[T any](slice []T) (T, error) {
	return First(slice)
}

// Tail returns all elements except the first.
func Tail[T any](slice []T) []T {
	if len(slice) <= 1 {
		return []T{}
	}
	return slice[1:]
}

// Init returns all elements except the last.
func Init[T any](slice []T) []T {
	if len(slice) <= 1 {
		return []T{}
	}
	return slice[:len(slice)-1]
}

// Equal checks if two slices are equal.
func Equal[T comparable](slice1, slice2 []T) bool {
	if len(slice1) != len(slice2) {
		return false
	}
	for i := range slice1 {
		if slice1[i] != slice2[i] {
			return false
		}
	}
	return true
}

// DeepEqual checks if two slices are deeply equal using reflect.DeepEqual.
func DeepEqual[T any](slice1, slice2 []T) bool {
	return reflect.DeepEqual(slice1, slice2)
}

// Sum returns the sum of all elements (for numeric types).
func Sum[T ordered](slice []T) T {
	var sum T
	for _, item := range slice {
		sum = sum + item
	}
	return sum
}

// Product returns the product of all elements (for numeric types).
func Product[T ordered](slice []T) T {
	if len(slice) == 0 {
		var zero T
		return zero
	}
	product := slice[0]
	for _, item := range slice[1:] {
		product = product * item
	}
	return product
}

// Average returns the average of numeric elements.
func Average[T float64 | float32 | int | int8 | int16 | int32 | int64 | uint | uint8 | uint16 | uint32 | uint64](slice []T) (float64, error) {
	if len(slice) == 0 {
		return 0, errors.New("slice is empty")
	}
	var sum float64
	for _, item := range slice {
		sum += float64(item)
	}
	return sum / float64(len(slice)), nil
}

// Median returns the median value of a sorted slice.
func Median[T ordered](slice []T) (T, error) {
	if len(slice) == 0 {
		var zero T
		return zero, errors.New("slice is empty")
	}
	
	sorted := SortedBy(slice, func(t T) T { return t })
	n := len(sorted)
	if n%2 == 0 {
		// For even length, return lower middle element
		return sorted[n/2-1], nil
	}
	return sorted[n/2], nil
}

// Mode returns the most frequently occurring value.
func Mode[T comparable](slice []T) (T, error) {
	if len(slice) == 0 {
		var zero T
		return zero, errors.New("slice is empty")
	}
	
	counts := make(map[T]int)
	for _, item := range slice {
		counts[item]++
	}
	
	var maxCount int
	var mode T
	for item, count := range counts {
		if count > maxCount {
			maxCount = count
			mode = item
		}
	}
	return mode, nil
}

// =============================================================================
// Zip and Unzip Operations
// =============================================================================

// Zip combines two slices into a slice of pairs.
func Zip[T, U any](slice1 []T, slice2 []U) ([]Pair[T, U], error) {
	if len(slice1) != len(slice2) {
		return nil, errors.New("slices must have equal length")
	}
	result := make([]Pair[T, U], len(slice1))
	for i := range slice1 {
		result[i] = Pair[T, U]{First: slice1[i], Second: slice2[i]}
	}
	return result, nil
}

// Unzip separates a slice of pairs into two slices.
func Unzip[T, U any](pairs []Pair[T, U]) ([]T, []U) {
	slice1 := make([]T, len(pairs))
	slice2 := make([]U, len(pairs))
	for i, p := range pairs {
		slice1[i] = p.First
		slice2[i] = p.Second
	}
	return slice1, slice2
}

// ZipWith combines two slices using a function.
func ZipWith[T, U, V any](slice1 []T, slice2 []U, f func(T, U) V) ([]V, error) {
	if len(slice1) != len(slice2) {
		return nil, errors.New("slices must have equal length")
	}
	result := make([]V, len(slice1))
	for i := range slice1 {
		result[i] = f(slice1[i], slice2[i])
	}
	return result, nil
}

// Pair represents a pair of values.
type Pair[T, U any] struct {
	First  T
	Second U
}