package set_utils

import (
	"sort"
	"testing"
)

// Helper function to check if two slices contain the same elements (order-independent)
func slicesEqual[T comparable](a, b []T) bool {
	if len(a) != len(b) {
		return false
	}
	aSet := NewSetFromSlice(a)
	bSet := NewSetFromSlice(b)
	return Equals(aSet, bSet)
}

// Helper to sort a slice for comparison
func sortSlice[T constraintsOrdered](s []T) []T {
	result := make([]T, len(s))
	copy(result, s)
	sort.Slice(result, func(i, j int) bool {
		return result[i] < result[j]
	})
	return result
}

// ============================================================================
// Set Creation Tests
// ============================================================================

func TestNewSet(t *testing.T) {
	s := NewSet[int]()
	if s == nil {
		t.Fatal("NewSet returned nil")
	}
	if s.Size() != 0 {
		t.Errorf("New set should be empty, got size %d", s.Size())
	}
	if !s.IsEmpty() {
		t.Error("New set should report as empty")
	}
}

func TestNewSetFromSlice(t *testing.T) {
	tests := []struct {
		name     string
		input    []int
		expected int
	}{
		{"empty slice", []int{}, 0},
		{"no duplicates", []int{1, 2, 3}, 3},
		{"with duplicates", []int{1, 2, 2, 3, 3, 3}, 3},
		{"all same", []int{1, 1, 1, 1}, 1},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			s := NewSetFromSlice(tt.input)
			if s.Size() != tt.expected {
				t.Errorf("expected size %d, got %d", tt.expected, s.Size())
			}
		})
	}
}

// ============================================================================
// Add/Remove/Contains Tests
// ============================================================================

func TestAdd(t *testing.T) {
	s := NewSet[string]()

	// Add new element
	if !s.Add("a") {
		t.Error("Add of new element should return true")
	}
	if s.Size() != 1 {
		t.Errorf("expected size 1, got %d", s.Size())
	}
	if !s.Contains("a") {
		t.Error("set should contain 'a'")
	}

	// Add duplicate
	if s.Add("a") {
		t.Error("Add of existing element should return false")
	}
	if s.Size() != 1 {
		t.Errorf("size should still be 1, got %d", s.Size())
	}
}

func TestRemove(t *testing.T) {
	s := NewSet[int]()
	s.Add(1)
	s.Add(2)

	// Remove existing
	if !s.Remove(1) {
		t.Error("Remove of existing element should return true")
	}
	if s.Contains(1) {
		t.Error("set should not contain removed element")
	}

	// Remove non-existing
	if s.Remove(99) {
		t.Error("Remove of non-existing element should return false")
	}
}

func TestContains(t *testing.T) {
	s := NewSet[int]()
	s.Add(1)
	s.Add(2)
	s.Add(3)

	tests := []struct {
		item     int
		expected bool
	}{
		{1, true},
		{2, true},
		{3, true},
		{4, false},
		{0, false},
		{-1, false},
	}

	for _, tt := range tests {
		t.Run("", func(t *testing.T) {
			if s.Contains(tt.item) != tt.expected {
				t.Errorf("Contains(%d) = %v, want %v", tt.item, !tt.expected, tt.expected)
			}
		})
	}
}

// ============================================================================
// Set Operations Tests
// ============================================================================

func TestUnion(t *testing.T) {
	tests := []struct {
		name     string
		s1       []int
		s2       []int
		expected []int
	}{
		{"both empty", []int{}, []int{}, []int{}},
		{"one empty", []int{1, 2}, []int{}, []int{1, 2}},
		{"no overlap", []int{1, 2}, []int{3, 4}, []int{1, 2, 3, 4}},
		{"partial overlap", []int{1, 2, 3}, []int{2, 3, 4}, []int{1, 2, 3, 4}},
		{"full overlap", []int{1, 2}, []int{1, 2}, []int{1, 2}},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			s1 := NewSetFromSlice(tt.s1)
			s2 := NewSetFromSlice(tt.s2)
			result := Union(s1, s2)

			if !slicesEqual(result.ToSlice(), tt.expected) {
				t.Errorf("Union = %v, want %v", result.ToSlice(), tt.expected)
			}
		})
	}
}

func TestIntersection(t *testing.T) {
	tests := []struct {
		name     string
		s1       []int
		s2       []int
		expected []int
	}{
		{"both empty", []int{}, []int{}, []int{}},
		{"one empty", []int{1, 2}, []int{}, []int{}},
		{"no overlap", []int{1, 2}, []int{3, 4}, []int{}},
		{"partial overlap", []int{1, 2, 3}, []int{2, 3, 4}, []int{2, 3}},
		{"full overlap", []int{1, 2}, []int{1, 2}, []int{1, 2}},
		{"subset", []int{1, 2}, []int{1, 2, 3, 4}, []int{1, 2}},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			s1 := NewSetFromSlice(tt.s1)
			s2 := NewSetFromSlice(tt.s2)
			result := Intersection(s1, s2)

			if !slicesEqual(result.ToSlice(), tt.expected) {
				t.Errorf("Intersection = %v, want %v", result.ToSlice(), tt.expected)
			}
		})
	}
}

func TestDifference(t *testing.T) {
	tests := []struct {
		name     string
		s1       []int
		s2       []int
		expected []int
	}{
		{"both empty", []int{}, []int{}, []int{}},
		{"first empty", []int{}, []int{1, 2}, []int{}},
		{"second empty", []int{1, 2}, []int{}, []int{1, 2}},
		{"no overlap", []int{1, 2}, []int{3, 4}, []int{1, 2}},
		{"partial overlap", []int{1, 2, 3}, []int{2, 3, 4}, []int{1}},
		{"full overlap", []int{1, 2}, []int{1, 2}, []int{}},
		{"subset", []int{1, 2}, []int{1, 2, 3, 4}, []int{}},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			s1 := NewSetFromSlice(tt.s1)
			s2 := NewSetFromSlice(tt.s2)
			result := Difference(s1, s2)

			if !slicesEqual(result.ToSlice(), tt.expected) {
				t.Errorf("Difference = %v, want %v", result.ToSlice(), tt.expected)
			}
		})
	}
}

func TestSymmetricDifference(t *testing.T) {
	tests := []struct {
		name     string
		s1       []int
		s2       []int
		expected []int
	}{
		{"both empty", []int{}, []int{}, []int{}},
		{"one empty", []int{1, 2}, []int{}, []int{1, 2}},
		{"no overlap", []int{1, 2}, []int{3, 4}, []int{1, 2, 3, 4}},
		{"partial overlap", []int{1, 2, 3}, []int{2, 3, 4}, []int{1, 4}},
		{"full overlap", []int{1, 2}, []int{1, 2}, []int{}},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			s1 := NewSetFromSlice(tt.s1)
			s2 := NewSetFromSlice(tt.s2)
			result := SymmetricDifference(s1, s2)

			if !slicesEqual(result.ToSlice(), tt.expected) {
				t.Errorf("SymmetricDifference = %v, want %v", result.ToSlice(), tt.expected)
			}
		})
	}
}

// ============================================================================
// Subset/Superset Tests
// ============================================================================

func TestIsSubset(t *testing.T) {
	tests := []struct {
		name     string
		s1       []int
		s2       []int
		expected bool
	}{
		{"both empty", []int{}, []int{}, true},
		{"empty is subset of any", []int{}, []int{1, 2}, true},
		{"proper subset", []int{1, 2}, []int{1, 2, 3}, true},
		{"equal sets", []int{1, 2}, []int{1, 2}, true},
		{"not a subset", []int{1, 2, 3}, []int{1, 2}, false},
		{"disjoint sets", []int{1, 2}, []int{3, 4}, false},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			s1 := NewSetFromSlice(tt.s1)
			s2 := NewSetFromSlice(tt.s2)
			result := IsSubset(s1, s2)

			if result != tt.expected {
				t.Errorf("IsSubset = %v, want %v", result, tt.expected)
			}
		})
	}
}

func TestIsProperSubset(t *testing.T) {
	tests := []struct {
		name     string
		s1       []int
		s2       []int
		expected bool
	}{
		{"equal sets", []int{1, 2}, []int{1, 2}, false},
		{"proper subset", []int{1, 2}, []int{1, 2, 3}, true},
		{"not a subset", []int{1, 2, 3}, []int{1, 2}, false},
		{"empty is proper subset", []int{}, []int{1}, true},
		{"both empty", []int{}, []int{}, false},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			s1 := NewSetFromSlice(tt.s1)
			s2 := NewSetFromSlice(tt.s2)
			result := IsProperSubset(s1, s2)

			if result != tt.expected {
				t.Errorf("IsProperSubset = %v, want %v", result, tt.expected)
			}
		})
	}
}

func TestAreDisjoint(t *testing.T) {
	tests := []struct {
		name     string
		s1       []int
		s2       []int
		expected bool
	}{
		{"both empty", []int{}, []int{}, true},
		{"one empty", []int{1, 2}, []int{}, true},
		{"disjoint", []int{1, 2}, []int{3, 4}, true},
		{"not disjoint", []int{1, 2}, []int{2, 3}, false},
		{"full overlap", []int{1, 2}, []int{1, 2}, false},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			s1 := NewSetFromSlice(tt.s1)
			s2 := NewSetFromSlice(tt.s2)
			result := AreDisjoint(s1, s2)

			if result != tt.expected {
				t.Errorf("AreDisjoint = %v, want %v", result, tt.expected)
			}
		})
	}
}

// ============================================================================
// Functional Operations Tests
// ============================================================================

func TestFilter(t *testing.T) {
	s := NewSetFromSlice([]int{1, 2, 3, 4, 5, 6})
	result := s.Filter(func(n int) bool {
		return n%2 == 0
	})

	expected := []int{2, 4, 6}
	if !slicesEqual(result.ToSlice(), expected) {
		t.Errorf("Filter = %v, want %v", result.ToSlice(), expected)
	}

	// Original set should be unchanged
	if s.Size() != 6 {
		t.Errorf("Original set modified, size = %d", s.Size())
	}
}

func TestMap(t *testing.T) {
	s := NewSetFromSlice([]int{1, 2, 3})
	result := Map(s, func(n int) string {
		return string(rune('a' + n - 1))
	})

	expected := []string{"a", "b", "c"}
	if !slicesEqual(result.ToSlice(), expected) {
		t.Errorf("Map = %v, want %v", result.ToSlice(), expected)
	}
}

func TestAny(t *testing.T) {
	s := NewSetFromSlice([]int{2, 4, 6, 8})

	if !s.Any(func(n int) bool { return n > 5 }) {
		t.Error("Any should return true when at least one element matches")
	}

	if s.Any(func(n int) bool { return n > 10 }) {
		t.Error("Any should return false when no elements match")
	}
}

func TestAll(t *testing.T) {
	s := NewSetFromSlice([]int{2, 4, 6, 8})

	if !s.All(func(n int) bool { return n%2 == 0 }) {
		t.Error("All should return true when all elements match")
	}

	if s.All(func(n int) bool { return n < 5 }) {
		t.Error("All should return false when not all elements match")
	}
}

// ============================================================================
// Utility Functions Tests
// ============================================================================

func TestUniqueSlice(t *testing.T) {
	tests := []struct {
		name     string
		input    []int
		expected []int
	}{
		{"empty", []int{}, []int{}},
		{"no duplicates", []int{1, 2, 3}, []int{1, 2, 3}},
		{"with duplicates", []int{1, 2, 2, 3, 3, 3}, []int{1, 2, 3}},
		{"all same", []int{1, 1, 1, 1}, []int{1}},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := UniqueSlice(tt.input)
			if !slicesEqual(result, tt.expected) {
				t.Errorf("UniqueSlice = %v, want %v", result, tt.expected)
			}
		})
	}
}

func TestUniqueSliceInPlace(t *testing.T) {
	input := []int{1, 2, 2, 3, 3, 3}
	UniqueSliceInPlace(&input)

	if len(input) != 3 {
		t.Errorf("expected length 3, got %d", len(input))
	}

	// Check no duplicates
	seen := make(map[int]bool)
	for _, v := range input {
		if seen[v] {
			t.Errorf("duplicate found: %d", v)
		}
		seen[v] = true
	}
}

func TestSliceContains(t *testing.T) {
	slice := []int{1, 2, 3, 4, 5}

	if !SliceContains(slice, 3) {
		t.Error("SliceContains should return true for existing element")
	}

	if SliceContains(slice, 99) {
		t.Error("SliceContains should return false for non-existing element")
	}
}

func TestSliceUnion(t *testing.T) {
	result := SliceUnion([]int{1, 2}, []int{2, 3}, []int{3, 4})
	expected := []int{1, 2, 3, 4}

	if !slicesEqual(result, expected) {
		t.Errorf("SliceUnion = %v, want %v", result, expected)
	}
}

func TestSliceIntersection(t *testing.T) {
	tests := []struct {
		name     string
		slices   [][]int
		expected []int
	}{
		{"two slices", [][]int{{1, 2, 3}, {2, 3, 4}}, []int{2, 3}},
		{"three slices", [][]int{{1, 2, 3}, {2, 3, 4}, {2, 3, 5}}, []int{2, 3}},
		{"no common", [][]int{{1, 2}, {3, 4}}, []int{}},
		{"empty", [][]int{}, []int{}},
		{"single", [][]int{{1, 2, 3}}, []int{1, 2, 3}},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := SliceIntersection(tt.slices...)
			if !slicesEqual(result, tt.expected) {
				t.Errorf("SliceIntersection = %v, want %v", result, tt.expected)
			}
		})
	}
}

func TestCountBy(t *testing.T) {
	result := CountBy([]string{"a", "b", "a", "c", "a", "b"})

	expected := map[string]int{"a": 3, "b": 2, "c": 1}

	for k, v := range expected {
		if result[k] != v {
			t.Errorf("CountBy[%s] = %d, want %d", k, result[k], v)
		}
	}
}

func TestMostFrequent(t *testing.T) {
	tests := []struct {
		name     string
		input    []int
		expected []int // Elements with max frequency
	}{
		{"single most", []int{1, 2, 2, 3}, []int{2}},
		{"multiple most", []int{1, 1, 2, 2, 3}, []int{1, 2}},
		{"empty", []int{}, []int{}},
		{"all same freq", []int{1, 2, 3}, []int{1, 2, 3}},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := MostFrequent(tt.input)
			if !slicesEqual(result, tt.expected) {
				t.Errorf("MostFrequent = %v, want %v", result, tt.expected)
			}
		})
	}
}

func TestLeastFrequent(t *testing.T) {
	tests := []struct {
		name     string
		input    []int
		expected []int
	}{
		{"single least", []int{1, 1, 2, 3}, []int{2, 3}},
		{"empty", []int{}, []int{}},
		{"all same freq", []int{1, 2, 3}, []int{1, 2, 3}},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := LeastFrequent(tt.input)
			if !slicesEqual(result, tt.expected) {
				t.Errorf("LeastFrequent = %v, want %v", result, tt.expected)
			}
		})
	}
}

// ============================================================================
// String Tests
// ============================================================================

func TestStringSet(t *testing.T) {
	s := NewSet[string]()
	s.Add("hello")
	s.Add("world")

	if s.Size() != 2 {
		t.Errorf("expected size 2, got %d", s.Size())
	}

	if !s.Contains("hello") {
		t.Error("set should contain 'hello'")
	}
}

// ============================================================================
// Clone Tests
// ============================================================================

func TestClone(t *testing.T) {
	original := NewSetFromSlice([]int{1, 2, 3})
	clone := original.Clone()

	// Clone should have same elements
	if !Equals(original, clone) {
		t.Error("clone should equal original")
	}

	// Modifying clone should not affect original
	clone.Add(4)
	if original.Contains(4) {
		t.Error("original should not be affected by clone modification")
	}
}

// ============================================================================
// Clear Tests
// ============================================================================

func TestClear(t *testing.T) {
	s := NewSetFromSlice([]int{1, 2, 3})
	s.Clear()

	if s.Size() != 0 {
		t.Errorf("expected size 0 after clear, got %d", s.Size())
	}

	if !s.IsEmpty() {
		t.Error("set should be empty after clear")
	}
}

// ============================================================================
// Sorted Slice Tests
// ============================================================================

func TestToSortedSlice(t *testing.T) {
	s := NewSetFromSlice([]int{3, 1, 4, 1, 5, 9, 2, 6})
	result := ToSortedSlice(s)

	expected := []int{1, 2, 3, 4, 5, 6, 9}
	if len(result) != len(expected) {
		t.Errorf("expected length %d, got %d", len(expected), len(result))
	}

	for i := range expected {
		if result[i] != expected[i] {
			t.Errorf("ToSortedSlice[%d] = %d, want %d", i, result[i], expected[i])
		}
	}
}

// ============================================================================
// Edge Cases and Stress Tests
// ============================================================================

func TestLargeSet(t *testing.T) {
	s := NewSet[int]()
	largeSize := 10000

	// Add many elements
	for i := 0; i < largeSize; i++ {
		s.Add(i)
	}

	if s.Size() != largeSize {
		t.Errorf("expected size %d, got %d", largeSize, s.Size())
	}

	// Test contains
	for i := 0; i < largeSize; i++ {
		if !s.Contains(i) {
			t.Errorf("set should contain %d", i)
		}
	}

	// Test remove half
	for i := 0; i < largeSize/2; i++ {
		s.Remove(i)
	}

	if s.Size() != largeSize/2 {
		t.Errorf("expected size %d after removal, got %d", largeSize/2, s.Size())
	}
}

func TestStringType(t *testing.T) {
	s := NewSetFromSlice([]string{"apple", "banana", "cherry", "banana", "apple"})

	if s.Size() != 3 {
		t.Errorf("expected size 3, got %d", s.Size())
	}

	// Test operations
	s2 := NewSetFromSlice([]string{"banana", "date"})
	union := Union(s, s2)

	if union.Size() != 4 {
		t.Errorf("union should have 4 elements, got %d", union.Size())
	}
}

// Benchmark tests
func BenchmarkAdd(b *testing.B) {
	s := NewSet[int]()
	for i := 0; i < b.N; i++ {
		s.Add(i)
	}
}

func BenchmarkContains(b *testing.B) {
	s := NewSet[int]()
	for i := 0; i < 10000; i++ {
		s.Add(i)
	}
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		s.Contains(i % 10000)
	}
}

func BenchmarkUnion(b *testing.B) {
	s1 := NewSet[int]()
	s2 := NewSet[int]()
	for i := 0; i < 1000; i++ {
		s1.Add(i)
		s2.Add(i + 500)
	}
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		Union(s1, s2)
	}
}