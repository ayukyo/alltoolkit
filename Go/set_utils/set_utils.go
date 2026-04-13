// Package set_utils provides generic set operations for Go.
// It offers efficient implementations for union, intersection, difference,
// and other common set operations using Go generics (Go 1.18+).
package set_utils

import (
	"fmt"
	"sort"
)

// Set represents a generic set of comparable elements.
type Set[T comparable] struct {
	elements map[T]struct{}
}

// NewSet creates a new empty set.
func NewSet[T comparable]() *Set[T] {
	return &Set[T]{
		elements: make(map[T]struct{}),
	}
}

// NewSetFromSlice creates a new set from a slice, removing duplicates.
func NewSetFromSlice[T comparable](items []T) *Set[T] {
	s := NewSet[T]()
	for _, item := range items {
		s.Add(item)
	}
	return s
}

// Add adds an element to the set. Returns true if the element was added, false if it already existed.
func (s *Set[T]) Add(item T) bool {
	if _, exists := s.elements[item]; exists {
		return false
	}
	s.elements[item] = struct{}{}
	return true
}

// Remove removes an element from the set. Returns true if the element was removed, false if it didn't exist.
func (s *Set[T]) Remove(item T) bool {
	if _, exists := s.elements[item]; !exists {
		return false
	}
	delete(s.elements, item)
	return true
}

// Contains checks if an element exists in the set.
func (s *Set[T]) Contains(item T) bool {
	_, exists := s.elements[item]
	return exists
}

// Size returns the number of elements in the set.
func (s *Set[T]) Size() int {
	return len(s.elements)
}

// IsEmpty checks if the set is empty.
func (s *Set[T]) IsEmpty() bool {
	return len(s.elements) == 0
}

// Clear removes all elements from the set.
func (s *Set[T]) Clear() {
	s.elements = make(map[T]struct{})
}

// ToSlice returns all elements as a slice.
func (s *Set[T]) ToSlice() []T {
	result := make([]T, 0, len(s.elements))
	for item := range s.elements {
		result = append(result, item)
	}
	return result
}

// ToSortedSlice returns all elements as a sorted slice.
// Elements must satisfy constraints.Ordered.
func ToSortedSlice[T constraintsOrdered](s *Set[T]) []T {
	result := s.ToSlice()
	sort.Slice(result, func(i, j int) bool {
		return result[i] < result[j]
	})
	return result
}

// constraintsOrdered is a constraint for types that can be ordered.
type constraintsOrdered interface {
	~int | ~int8 | ~int16 | ~int32 | ~int64 |
		~uint | ~uint8 | ~uint16 | ~uint32 | ~uint64 | ~uintptr |
		~float32 | ~float64 |
		~string
}

// Union returns a new set containing all elements from both sets.
func Union[T comparable](s1, s2 *Set[T]) *Set[T] {
	result := NewSet[T]()
	for item := range s1.elements {
		result.Add(item)
	}
	for item := range s2.elements {
		result.Add(item)
	}
	return result
}

// Intersection returns a new set containing elements that exist in both sets.
func Intersection[T comparable](s1, s2 *Set[T]) *Set[T] {
	result := NewSet[T]()
	// Iterate over the smaller set for efficiency
	if s1.Size() > s2.Size() {
		s1, s2 = s2, s1
	}
	for item := range s1.elements {
		if s2.Contains(item) {
			result.Add(item)
		}
	}
	return result
}

// Difference returns a new set containing elements in s1 that are not in s2.
func Difference[T comparable](s1, s2 *Set[T]) *Set[T] {
	result := NewSet[T]()
	for item := range s1.elements {
		if !s2.Contains(item) {
			result.Add(item)
		}
	}
	return result
}

// SymmetricDifference returns a new set containing elements that are in either set but not in both.
func SymmetricDifference[T comparable](s1, s2 *Set[T]) *Set[T] {
	result := NewSet[T]()
	for item := range s1.elements {
		if !s2.Contains(item) {
			result.Add(item)
		}
	}
	for item := range s2.elements {
		if !s1.Contains(item) {
			result.Add(item)
		}
	}
	return result
}

// IsSubset checks if s1 is a subset of s2.
func IsSubset[T comparable](s1, s2 *Set[T]) bool {
	if s1.Size() > s2.Size() {
		return false
	}
	for item := range s1.elements {
		if !s2.Contains(item) {
			return false
		}
	}
	return true
}

// IsSuperset checks if s1 is a superset of s2.
func IsSuperset[T comparable](s1, s2 *Set[T]) bool {
	return IsSubset(s2, s1)
}

// IsProperSubset checks if s1 is a proper subset of s2 (subset but not equal).
func IsProperSubset[T comparable](s1, s2 *Set[T]) bool {
	return s1.Size() < s2.Size() && IsSubset(s1, s2)
}

// IsProperSuperset checks if s1 is a proper superset of s2.
func IsProperSuperset[T comparable](s1, s2 *Set[T]) bool {
	return IsProperSubset(s2, s1)
}

// Equals checks if two sets contain exactly the same elements.
func Equals[T comparable](s1, s2 *Set[T]) bool {
	if s1.Size() != s2.Size() {
		return false
	}
	for item := range s1.elements {
		if !s2.Contains(item) {
			return false
		}
	}
	return true
}

// AreDisjoint checks if two sets have no elements in common.
func AreDisjoint[T comparable](s1, s2 *Set[T]) bool {
	// Iterate over the smaller set for efficiency
	if s1.Size() > s2.Size() {
		s1, s2 = s2, s1
	}
	for item := range s1.elements {
		if s2.Contains(item) {
			return false
		}
	}
	return true
}

// Clone returns a shallow copy of the set.
func (s *Set[T]) Clone() *Set[T] {
	result := NewSet[T]()
	for item := range s.elements {
		result.Add(item)
	}
	return result
}

// Each iterates over all elements in the set, calling the provided function.
func (s *Set[T]) Each(fn func(T)) {
	for item := range s.elements {
		fn(item)
	}
}

// Filter returns a new set containing only elements that satisfy the predicate.
func (s *Set[T]) Filter(predicate func(T) bool) *Set[T] {
	result := NewSet[T]()
	for item := range s.elements {
		if predicate(item) {
			result.Add(item)
		}
	}
	return result
}

// Map transforms each element using the provided function and returns a new set.
func Map[T comparable, U comparable](s *Set[T], transform func(T) U) *Set[U] {
	result := NewSet[U]()
	for item := range s.elements {
		result.Add(transform(item))
	}
	return result
}

// Any returns true if any element satisfies the predicate.
func (s *Set[T]) Any(predicate func(T) bool) bool {
	for item := range s.elements {
		if predicate(item) {
			return true
		}
	}
	return false
}

// All returns true if all elements satisfy the predicate.
func (s *Set[T]) All(predicate func(T) bool) bool {
	for item := range s.elements {
		if !predicate(item) {
			return false
		}
	}
	return true
}

// String returns a string representation of the set.
func (s *Set[T]) String() string {
	return fmt.Sprintf("%v", s.ToSlice())
}

// ============================================================================
// Utility Functions (non-method versions for functional style)
// ============================================================================

// UniqueSlice removes duplicates from a slice and returns a new slice.
func UniqueSlice[T comparable](items []T) []T {
	return NewSetFromSlice(items).ToSlice()
}

// UniqueSliceInPlace removes duplicates from a slice in place.
func UniqueSliceInPlace[T comparable](items *[]T) {
	seen := make(map[T]struct{})
	result := (*items)[:0]
	for _, item := range *items {
		if _, exists := seen[item]; !exists {
			seen[item] = struct{}{}
			result = append(result, item)
		}
	}
	*items = result
}

// SliceContains checks if a slice contains an element.
func SliceContains[T comparable](items []T, item T) bool {
	for _, i := range items {
		if i == item {
			return true
		}
	}
	return false
}

// SliceUnion returns the union of multiple slices as a single slice with no duplicates.
func SliceUnion[T comparable](slices ...[]T) []T {
	result := NewSet[T]()
	for _, slice := range slices {
		for _, item := range slice {
			result.Add(item)
		}
	}
	return result.ToSlice()
}

// SliceIntersection returns the intersection of multiple slices as a single slice.
func SliceIntersection[T comparable](slices ...[]T) []T {
	if len(slices) == 0 {
		return []T{}
	}
	if len(slices) == 1 {
		return UniqueSlice(slices[0])
	}

	result := NewSetFromSlice(slices[0])
	for _, slice := range slices[1:] {
		other := NewSetFromSlice(slice)
		result = Intersection(result, other)
	}
	return result.ToSlice()
}

// SliceDifference returns elements in the first slice that are not in the second slice.
func SliceDifference[T comparable](s1, s2 []T) []T {
	set1 := NewSetFromSlice(s1)
	set2 := NewSetFromSlice(s2)
	return Difference(set1, set2).ToSlice()
}

// SliceSymmetricDifference returns elements that are in exactly one of the slices.
func SliceSymmetricDifference[T comparable](s1, s2 []T) []T {
	set1 := NewSetFromSlice(s1)
	set2 := NewSetFromSlice(s2)
	return SymmetricDifference(set1, set2).ToSlice()
}

// CountBy counts occurrences of each unique element in a slice.
func CountBy[T comparable](items []T) map[T]int {
	result := make(map[T]int)
	for _, item := range items {
		result[item]++
	}
	return result
}

// MostFrequent returns the most frequently occurring element(s) in a slice.
// Returns all elements that have the maximum frequency.
func MostFrequent[T comparable](items []T) []T {
	if len(items) == 0 {
		return []T{}
	}

	counts := CountBy(items)
	maxCount := 0
	for _, count := range counts {
		if count > maxCount {
			maxCount = count
		}
	}

	result := []T{}
	for item, count := range counts {
		if count == maxCount {
			result = append(result, item)
		}
	}
	return result
}

// LeastFrequent returns the least frequently occurring element(s) in a slice.
// Returns all elements that have the minimum frequency.
func LeastFrequent[T comparable](items []T) []T {
	if len(items) == 0 {
		return []T{}
	}

	counts := CountBy(items)
	minCount := len(items) + 1
	for _, count := range counts {
		if count < minCount {
			minCount = count
		}
	}

	result := []T{}
	for item, count := range counts {
		if count == minCount {
			result = append(result, item)
		}
	}
	return result
}