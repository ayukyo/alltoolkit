package topn_utils

import (
	"math/rand"
	"reflect"
	"sort"
	"testing"
)

func TestNewTopNFinder(t *testing.T) {
	tests := []struct {
		name     string
		n        int
		expected int
	}{
		{"normal", 5, 5},
		{"zero", 0, 1},
		{"negative", -1, 1},
		{"large", 1000, 1000},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			finder := NewTopNFinder(tt.n)
			if finder.n != tt.expected {
				t.Errorf("NewTopNFinder(%d) = %d, want %d", tt.n, finder.n, tt.expected)
			}
		})
	}
}

func TestLargest(t *testing.T) {
	tests := []struct {
		name     string
		data     []int
		n        int
		expected []int
	}{
		{
			name:     "basic",
			data:     []int{1, 5, 2, 8, 3, 9, 4, 7, 6},
			n:        3,
			expected: []int{9, 8, 7},
		},
		{
			name:     "n larger than data",
			data:     []int{1, 2, 3},
			n:        5,
			expected: []int{3, 2, 1},
		},
		{
			name:     "empty data",
			data:     []int{},
			n:        3,
			expected: []int{},
		},
		{
			name:     "n equals 1",
			data:     []int{5, 2, 8, 1, 9},
			n:        1,
			expected: []int{9},
		},
		{
			name:     "duplicates",
			data:     []int{5, 5, 5, 5, 5},
			n:        3,
			expected: []int{5, 5, 5},
		},
		{
			name:     "negative numbers",
			data:     []int{-1, -5, -2, -8, -3},
			n:        2,
			expected: []int{-1, -2},
		},
		{
			name:     "mixed positive and negative",
			data:     []int{-5, 10, -2, 8, 0, -1, 9},
			n:        4,
			expected: []int{10, 9, 8, 0},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			finder := NewTopNFinder(tt.n)
			result := finder.Largest(tt.data)
			if !reflect.DeepEqual(result, tt.expected) {
				t.Errorf("Largest() = %v, want %v", result, tt.expected)
			}
		})
	}
}

func TestSmallest(t *testing.T) {
	tests := []struct {
		name     string
		data     []int
		n        int
		expected []int
	}{
		{
			name:     "basic",
			data:     []int{1, 5, 2, 8, 3, 9, 4, 7, 6},
			n:        3,
			expected: []int{1, 2, 3},
		},
		{
			name:     "n larger than data",
			data:     []int{5, 1, 3},
			n:        5,
			expected: []int{1, 3, 5},
		},
		{
			name:     "empty data",
			data:     []int{},
			n:        3,
			expected: []int{},
		},
		{
			name:     "n equals 1",
			data:     []int{5, 2, 8, 1, 9},
			n:        1,
			expected: []int{1},
		},
		{
			name:     "duplicates",
			data:     []int{3, 3, 3, 3, 3},
			n:        3,
			expected: []int{3, 3, 3},
		},
		{
			name:     "negative numbers",
			data:     []int{-1, -5, -2, -8, -3},
			n:        2,
			expected: []int{-8, -5},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			finder := NewTopNFinder(tt.n)
			result := finder.Smallest(tt.data)
			if !reflect.DeepEqual(result, tt.expected) {
				t.Errorf("Smallest() = %v, want %v", result, tt.expected)
			}
		})
	}
}

func TestLargestFloats(t *testing.T) {
	tests := []struct {
		name     string
		data     []float64
		n        int
		expected []float64
	}{
		{
			name:     "basic",
			data:     []float64{1.5, 5.2, 2.8, 8.1, 3.7},
			n:        3,
			expected: []float64{8.1, 5.2, 3.7},
		},
		{
			name:     "with negatives",
			data:     []float64{-1.5, 5.2, -2.8, 8.1, 0.0},
			n:        2,
			expected: []float64{8.1, 5.2},
		},
		{
			name:     "empty",
			data:     []float64{},
			n:        3,
			expected: []float64{},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			finder := NewTopNFinder(tt.n)
			result := finder.LargestFloats(tt.data)
			if !reflect.DeepEqual(result, tt.expected) {
				t.Errorf("LargestFloats() = %v, want %v", result, tt.expected)
			}
		})
	}
}

func TestSmallestFloats(t *testing.T) {
	tests := []struct {
		name     string
		data     []float64
		n        int
		expected []float64
	}{
		{
			name:     "basic",
			data:     []float64{1.5, 5.2, 2.8, 8.1, 3.7},
			n:        2,
			expected: []float64{1.5, 2.8},
		},
		{
			name:     "with negatives",
			data:     []float64{-1.5, 5.2, -2.8, 8.1, 0.0},
			n:        2,
			expected: []float64{-2.8, -1.5},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			finder := NewTopNFinder(tt.n)
			result := finder.SmallestFloats(tt.data)
			if !reflect.DeepEqual(result, tt.expected) {
				t.Errorf("SmallestFloats() = %v, want %v", result, tt.expected)
			}
		})
	}
}

func TestLargestStrings(t *testing.T) {
	tests := []struct {
		name     string
		data     []string
		n        int
		expected []string
	}{
		{
			name:     "basic",
			data:     []string{"apple", "banana", "cherry", "date", "elderberry"},
			n:        3,
			expected: []string{"elderberry", "date", "cherry"},
		},
		{
			name:     "n equals 1",
			data:     []string{"zebra", "ant", "mouse"},
			n:        1,
			expected: []string{"zebra"},
		},
		{
			name:     "empty",
			data:     []string{},
			n:        3,
			expected: []string{},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			finder := NewTopNFinder(tt.n)
			result := finder.LargestStrings(tt.data)
			if !reflect.DeepEqual(result, tt.expected) {
				t.Errorf("LargestStrings() = %v, want %v", result, tt.expected)
			}
		})
	}
}

func TestSmallestStrings(t *testing.T) {
	tests := []struct {
		name     string
		data     []string
		n        int
		expected []string
	}{
		{
			name:     "basic",
			data:     []string{"apple", "banana", "cherry", "date", "elderberry"},
			n:        3,
			expected: []string{"apple", "banana", "cherry"},
		},
		{
			name:     "n equals 1",
			data:     []string{"zebra", "ant", "mouse"},
			n:        1,
			expected: []string{"ant"},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			finder := NewTopNFinder(tt.n)
			result := finder.SmallestStrings(tt.data)
			if !reflect.DeepEqual(result, tt.expected) {
				t.Errorf("SmallestStrings() = %v, want %v", result, tt.expected)
			}
		})
	}
}

func TestLargestItems(t *testing.T) {
	items := []Item{
		{Value: "a", Score: 10},
		{Value: "b", Score: 30},
		{Value: "c", Score: 20},
		{Value: "d", Score: 50},
		{Value: "e", Score: 40},
	}

	finder := NewTopNFinder(3)
	result := finder.LargestItems(items)

	expected := []Item{
		{Value: "d", Score: 50},
		{Value: "e", Score: 40},
		{Value: "b", Score: 30},
	}

	if !reflect.DeepEqual(result, expected) {
		t.Errorf("LargestItems() = %v, want %v", result, expected)
	}
}

func TestSmallestItems(t *testing.T) {
	items := []Item{
		{Value: "a", Score: 10},
		{Value: "b", Score: 30},
		{Value: "c", Score: 20},
		{Value: "d", Score: 50},
		{Value: "e", Score: 40},
	}

	finder := NewTopNFinder(3)
	result := finder.SmallestItems(items)

	expected := []Item{
		{Value: "a", Score: 10},
		{Value: "c", Score: 20},
		{Value: "b", Score: 30},
	}

	if !reflect.DeepEqual(result, expected) {
		t.Errorf("SmallestItems() = %v, want %v", result, expected)
	}
}

func TestQuickSelect(t *testing.T) {
	tests := []struct {
		name     string
		data     []int
		k        int
		expected int
	}{
		{"first smallest", []int{3, 1, 4, 1, 5, 9, 2, 6}, 0, 1},
		{"second smallest", []int{3, 1, 4, 1, 5, 9, 2, 6}, 1, 1},
		{"median", []int{3, 1, 4, 1, 5, 9, 2, 6}, 4, 4},
		{"largest", []int{3, 1, 4, 1, 5, 9, 2, 6}, 7, 9},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			// Create a copy since QuickSelect modifies the slice
			data := make([]int, len(tt.data))
			copy(data, tt.data)
			result := QuickSelect(data, tt.k)
			if result != tt.expected {
				t.Errorf("QuickSelect() = %v, want %v", result, tt.expected)
			}
		})
	}
}

func TestKthSmallest(t *testing.T) {
	data := []int{3, 1, 4, 1, 5, 9, 2, 6}
	sorted := make([]int, len(data))
	copy(sorted, data)
	sort.Ints(sorted)

	for k := 1; k <= len(data); k++ {
		result := KthSmallest(data, k)
		if result != sorted[k-1] {
			t.Errorf("KthSmallest(data, %d) = %d, want %d", k, result, sorted[k-1])
		}
	}
}

func TestKthLargest(t *testing.T) {
	data := []int{3, 1, 4, 1, 5, 9, 2, 6}
	sorted := make([]int, len(data))
	copy(sorted, data)
	sort.Sort(sort.Reverse(sort.IntSlice(sorted)))

	for k := 1; k <= len(data); k++ {
		result := KthLargest(data, k)
		if result != sorted[k-1] {
			t.Errorf("KthLargest(data, %d) = %d, want %d", k, result, sorted[k-1])
		}
	}
}

func TestMedian(t *testing.T) {
	tests := []struct {
		name     string
		data     []int
		expected float64
	}{
		{"odd count", []int{1, 2, 3, 4, 5}, 3.0},
		{"even count", []int{1, 2, 3, 4}, 2.5},
		{"single element", []int{5}, 5.0},
		{"unsorted odd", []int{5, 2, 8, 1, 9}, 5.0},
		{"unsorted even", []int{3, 1, 4, 2}, 2.5},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := Median(tt.data)
			if result != tt.expected {
				t.Errorf("Median() = %v, want %v", result, tt.expected)
			}
		})
	}
}

func TestPercentile(t *testing.T) {
	data := []int{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}

	tests := []struct {
		name       string
		percentile float64
		expected   int
	}{
		{"0th percentile", 0, 1},
		{"25th percentile", 25, 3},
		{"50th percentile", 50, 5},
		{"75th percentile", 75, 8},
		{"100th percentile", 100, 10},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := Percentile(data, tt.percentile)
			if result != tt.expected {
				t.Errorf("Percentile(%v) = %d, want %d", tt.percentile, result, tt.expected)
			}
		})
	}
}

func TestTopNLargestConvenience(t *testing.T) {
	data := []int{5, 2, 8, 1, 9, 3, 7, 4, 6}
	result := TopNLargest(data, 3)
	expected := []int{9, 8, 7}

	if !reflect.DeepEqual(result, expected) {
		t.Errorf("TopNLargest() = %v, want %v", result, expected)
	}
}

func TestTopNSmallestConvenience(t *testing.T) {
	data := []int{5, 2, 8, 1, 9, 3, 7, 4, 6}
	result := TopNSmallest(data, 3)
	expected := []int{1, 2, 3}

	if !reflect.DeepEqual(result, expected) {
		t.Errorf("TopNSmallest() = %v, want %v", result, expected)
	}
}

// ========== Benchmark Tests ==========

func BenchmarkLargest(b *testing.B) {
	rand.Seed(42)
	data := make([]int, 1000000)
	for i := range data {
		data[i] = rand.Intn(1000000)
	}

	finder := NewTopNFinder(100)

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		finder.Largest(data)
	}
}

func BenchmarkSmallest(b *testing.B) {
	rand.Seed(42)
	data := make([]int, 1000000)
	for i := range data {
		data[i] = rand.Intn(1000000)
	}

	finder := NewTopNFinder(100)

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		finder.Smallest(data)
	}
}

func BenchmarkSortBasedTopN(b *testing.B) {
	rand.Seed(42)
	data := make([]int, 1000000)
	for i := range data {
		data[i] = rand.Intn(1000000)
	}

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		sorted := make([]int, len(data))
		copy(sorted, data)
		sort.Sort(sort.Reverse(sort.IntSlice(sorted)))
		_ = sorted[:100]
	}
}

func BenchmarkQuickSelect(b *testing.B) {
	rand.Seed(42)
	data := make([]int, 1000000)
	for i := range data {
		data[i] = rand.Intn(1000000)
	}

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		temp := make([]int, len(data))
		copy(temp, data)
		QuickSelect(temp, 500000)
	}
}

// ========== Edge Case Tests ==========

func TestEmptySlice(t *testing.T) {
	finder := NewTopNFinder(5)

	if result := finder.Largest([]int{}); len(result) != 0 {
		t.Errorf("Largest empty slice should return empty, got %v", result)
	}
	if result := finder.Smallest([]int{}); len(result) != 0 {
		t.Errorf("Smallest empty slice should return empty, got %v", result)
	}
	if result := finder.LargestFloats([]float64{}); len(result) != 0 {
		t.Errorf("LargestFloats empty slice should return empty, got %v", result)
	}
	if result := finder.LargestStrings([]string{}); len(result) != 0 {
		t.Errorf("LargestStrings empty slice should return empty, got %v", result)
	}
}

func TestSingleElement(t *testing.T) {
	finder := NewTopNFinder(5)

	if result := finder.Largest([]int{42}); !reflect.DeepEqual(result, []int{42}) {
		t.Errorf("Largest single element failed, got %v", result)
	}
	if result := finder.Smallest([]int{42}); !reflect.DeepEqual(result, []int{42}) {
		t.Errorf("Smallest single element failed, got %v", result)
	}
}

func TestAllSameElements(t *testing.T) {
	data := []int{5, 5, 5, 5, 5}
	finder := NewTopNFinder(3)

	result := finder.Largest(data)
	if !reflect.DeepEqual(result, []int{5, 5, 5}) {
		t.Errorf("Largest with all same elements failed, got %v", result)
	}

	result = finder.Smallest(data)
	if !reflect.DeepEqual(result, []int{5, 5, 5}) {
		t.Errorf("Smallest with all same elements failed, got %v", result)
	}
}

func TestNegativeN(t *testing.T) {
	finder := NewTopNFinder(-5)
	// Should be normalized to 1
	if finder.n != 1 {
		t.Errorf("Negative N should be normalized to 1, got %d", finder.n)
	}
}