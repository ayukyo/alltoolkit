package combination_utils

import (
	"reflect"
	"testing"
)

// Helper to check if a slice contains a specific combination
func containsCombo[T any](combos [][]T, target []T) bool {
	for _, c := range combos {
		if reflect.DeepEqual(c, target) {
			return true
		}
	}
	return false
}

func TestCombinations(t *testing.T) {
	tests := []struct {
		name     string
		input    []int
		k        int
		expected [][]int
	}{
		{
			name:     "empty slice k=0",
			input:    []int{},
			k:        0,
			expected: [][]int{{}},
		},
		{
			name:     "empty slice k=1",
			input:    []int{},
			k:        1,
			expected: nil,
		},
		{
			name:     "single element k=0",
			input:    []int{1},
			k:        0,
			expected: [][]int{{}},
		},
		{
			name:     "single element k=1",
			input:    []int{1},
			k:        1,
			expected: [][]int{{1}},
		},
		{
			name:     "three elements k=2",
			input:    []int{1, 2, 3},
			k:        2,
			expected: [][]int{{1, 2}, {1, 3}, {2, 3}},
		},
		{
			name:     "three elements k=1",
			input:    []int{1, 2, 3},
			k:        1,
			expected: [][]int{{1}, {2}, {3}},
		},
		{
			name:     "three elements k=3",
			input:    []int{1, 2, 3},
			k:        3,
			expected: [][]int{{1, 2, 3}},
		},
		{
			name:     "four elements k=2",
			input:    []int{1, 2, 3, 4},
			k:        2,
			expected: [][]int{{1, 2}, {1, 3}, {1, 4}, {2, 3}, {2, 4}, {3, 4}},
		},
		{
			name:     "k greater than n",
			input:    []int{1, 2},
			k:        3,
			expected: nil,
		},
		{
			name:     "negative k",
			input:    []int{1, 2, 3},
			k:        -1,
			expected: nil,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := Combinations(tt.input, tt.k)
			if !reflect.DeepEqual(result, tt.expected) {
				t.Errorf("Combinations() = %v, want %v", result, tt.expected)
			}
		})
	}
}

func TestCombinationsWithStrings(t *testing.T) {
	input := []string{"a", "b", "c"}
	result := Combinations(input, 2)
	expected := [][]string{{"a", "b"}, {"a", "c"}, {"b", "c"}}

	if !reflect.DeepEqual(result, expected) {
		t.Errorf("Combinations with strings = %v, want %v", result, expected)
	}
}

func TestCombinationsChan(t *testing.T) {
	input := []int{1, 2, 3, 4}
	k := 2

	var results [][]int
	for combo := range CombinationsChan(input, k) {
		results = append(results, combo)
	}

	expected := Combinations(input, k)
	if len(results) != len(expected) {
		t.Errorf("CombinationsChan count = %d, want %d", len(results), len(expected))
	}

	// Check all expected combinations are present
	for _, exp := range expected {
		if !containsCombo(results, exp) {
			t.Errorf("Missing combination %v", exp)
		}
	}
}

func TestPermutations(t *testing.T) {
	tests := []struct {
		name     string
		input    []int
		expected [][]int
	}{
		{
			name:     "empty slice",
			input:    []int{},
			expected: [][]int{{}},
		},
		{
			name:     "single element",
			input:    []int{1},
			expected: [][]int{{1}},
		},
		{
			name:     "two elements",
			input:    []int{1, 2},
			expected: [][]int{{1, 2}, {2, 1}},
		},
		{
			name:     "three elements",
			input:    []int{1, 2, 3},
			expected: [][]int{{1, 2, 3}, {1, 3, 2}, {2, 1, 3}, {2, 3, 1}, {3, 1, 2}, {3, 2, 1}},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := Permutations(tt.input)
			if len(result) != len(tt.expected) {
				t.Errorf("Permutations count = %d, want %d", len(result), len(tt.expected))
			}

			// Check all expected permutations are present
			for _, exp := range tt.expected {
				if !containsCombo(result, exp) {
					t.Errorf("Missing permutation %v", exp)
				}
			}
		})
	}
}

func TestPermutationsChan(t *testing.T) {
	input := []int{1, 2, 3}

	var results [][]int
	for perm := range PermutationsChan(input) {
		results = append(results, perm)
	}

	expected := Permutations(input)
	if len(results) != len(expected) {
		t.Errorf("PermutationsChan count = %d, want %d", len(results), len(expected))
	}
}

func TestPermutationsK(t *testing.T) {
	tests := []struct {
		name     string
		input    []int
		k        int
		expected [][]int
	}{
		{
			name:     "k=0",
			input:    []int{1, 2, 3},
			k:        0,
			expected: [][]int{{}},
		},
		{
			name:     "k=1",
			input:    []int{1, 2, 3},
			k:        1,
			expected: [][]int{{1}, {2}, {3}},
		},
		{
			name:     "k=2 from 3 elements",
			input:    []int{1, 2, 3},
			k:        2,
			expected: [][]int{{1, 2}, {1, 3}, {2, 1}, {2, 3}, {3, 1}, {3, 2}},
		},
		{
			name:     "k greater than n",
			input:    []int{1, 2},
			k:        3,
			expected: nil,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := PermutationsK(tt.input, tt.k)
			if len(result) != len(tt.expected) {
				t.Errorf("PermutationsK count = %d, want %d", len(result), len(tt.expected))
			}

			for _, exp := range tt.expected {
				if !containsCombo(result, exp) {
					t.Errorf("Missing k-permutation %v", exp)
				}
			}
		})
	}
}

func TestCombinationsWithRepetition(t *testing.T) {
	tests := []struct {
		name     string
		input    []int
		k        int
		expected [][]int
	}{
		{
			name:     "k=0",
			input:    []int{1, 2},
			k:        0,
			expected: [][]int{{}},
		},
		{
			name:     "k=2 from 2 elements",
			input:    []int{1, 2},
			k:        2,
			expected: [][]int{{1, 1}, {1, 2}, {2, 2}},
		},
		{
			name:     "k=3 from 2 elements",
			input:    []int{1, 2},
			k:        3,
			expected: [][]int{{1, 1, 1}, {1, 1, 2}, {1, 2, 2}, {2, 2, 2}},
		},
		{
			name:     "empty slice with k>0",
			input:    []int{},
			k:        1,
			expected: nil,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := CombinationsWithRepetition(tt.input, tt.k)
			if !reflect.DeepEqual(result, tt.expected) {
				t.Errorf("CombinationsWithRepetition() = %v, want %v", result, tt.expected)
			}
		})
	}
}

func TestPowerSet(t *testing.T) {
	tests := []struct {
		name     string
		input    []int
		expected [][]int
	}{
		{
			name:     "empty slice",
			input:    []int{},
			expected: [][]int{{}},
		},
		{
			name:     "single element",
			input:    []int{1},
			expected: [][]int{{}, {1}},
		},
		{
			name:     "two elements",
			input:    []int{1, 2},
			expected: [][]int{{}, {1}, {2}, {1, 2}},
		},
		{
			name:     "three elements",
			input:    []int{1, 2, 3},
			expected: [][]int{{}, {1}, {2}, {1, 2}, {3}, {1, 3}, {2, 3}, {1, 2, 3}},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := PowerSet(tt.input)
			if len(result) != len(tt.expected) {
				t.Errorf("PowerSet count = %d, want %d", len(result), len(tt.expected))
			}

			for _, exp := range tt.expected {
				if !containsCombo(result, exp) {
					t.Errorf("Missing subset %v", exp)
				}
			}
		})
	}
}

func TestPowerSetChan(t *testing.T) {
	input := []int{1, 2, 3}

	var results [][]int
	for subset := range PowerSetChan(input) {
		results = append(results, subset)
	}

	expected := PowerSet(input)
	if len(results) != len(expected) {
		t.Errorf("PowerSetChan count = %d, want %d", len(results), len(expected))
	}
}

func TestBinomialCoefficient(t *testing.T) {
	tests := []struct {
		name      string
		n         int
		k         int
		expected  int
		expectErr bool
	}{
		{"0 choose 0", 0, 0, 1, false},
		{"5 choose 0", 5, 0, 1, false},
		{"5 choose 1", 5, 1, 5, false},
		{"5 choose 2", 5, 2, 10, false},
		{"5 choose 3", 5, 3, 10, false},
		{"5 choose 5", 5, 5, 1, false},
		{"10 choose 3", 10, 3, 120, false},
		{"20 choose 10", 20, 10, 184756, false},
		{"negative n", -1, 2, 0, true},
		{"negative k", 5, -1, 0, true},
		{"k > n", 3, 5, 0, true},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := BinomialCoefficient(tt.n, tt.k)
			if tt.expectErr {
				if err == nil {
					t.Error("Expected error, got nil")
				}
			} else {
				if err != nil {
					t.Errorf("Unexpected error: %v", err)
				}
				if result != tt.expected {
					t.Errorf("BinomialCoefficient(%d, %d) = %d, want %d", tt.n, tt.k, result, tt.expected)
				}
			}
		})
	}
}

func TestFactorial(t *testing.T) {
	tests := []struct {
		name      string
		n         int
		expected  int
		expectErr bool
	}{
		{"0!", 0, 1, false},
		{"1!", 1, 1, false},
		{"5!", 5, 120, false},
		{"10!", 10, 3628800, false},
		{"20!", 20, 2432902008176640000, false},
		{"negative", -1, 0, true},
		{"overflow", 21, 0, true},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := Factorial(tt.n)
			if tt.expectErr {
				if err == nil {
					t.Error("Expected error, got nil")
				}
			} else {
				if err != nil {
					t.Errorf("Unexpected error: %v", err)
				}
				if result != tt.expected {
					t.Errorf("Factorial(%d) = %d, want %d", tt.n, result, tt.expected)
				}
			}
		})
	}
}

func TestCountPermutations(t *testing.T) {
	tests := []struct {
		name      string
		n         int
		k         int
		expected  int
		expectErr bool
	}{
		{"P(0,0)", 0, 0, 1, false},
		{"P(5,0)", 5, 0, 1, false},
		{"P(5,1)", 5, 1, 5, false},
		{"P(5,2)", 5, 2, 20, false},
		{"P(5,5)", 5, 5, 120, false},
		{"P(10,3)", 10, 3, 720, false},
		{"negative n", -1, 2, 0, true},
		{"k > n", 3, 5, 0, true},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := CountPermutations(tt.n, tt.k)
			if tt.expectErr {
				if err == nil {
					t.Error("Expected error, got nil")
				}
			} else {
				if err != nil {
					t.Errorf("Unexpected error: %v", err)
				}
				if result != tt.expected {
					t.Errorf("CountPermutations(%d, %d) = %d, want %d", tt.n, tt.k, result, tt.expected)
				}
			}
		})
	}
}

func TestCombinationsWithRepetitionCount(t *testing.T) {
	tests := []struct {
		name     string
		n        int
		k        int
		expected int
	}{
		{"C'(2,2)", 2, 2, 3},
		{"C'(2,3)", 2, 3, 4},
		{"C'(3,2)", 3, 2, 6},
		{"C'(4,2)", 4, 2, 10},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := CombinationsWithRepetitionCount(tt.n, tt.k)
			if err != nil {
				t.Errorf("Unexpected error: %v", err)
			}
			if result != tt.expected {
				t.Errorf("CombinationsWithRepetitionCount(%d, %d) = %d, want %d", tt.n, tt.k, result, tt.expected)
			}
		})
	}
}

func TestMultiSetPermutation(t *testing.T) {
	tests := []struct {
		name     string
		input    []int
		expected int // number of unique permutations
	}{
		{"all same", []int{1, 1, 1}, 1},
		{"two pairs", []int{1, 1, 2, 2}, 6},
		{"one pair", []int{1, 1, 2}, 3},
		{"all different", []int{1, 2, 3}, 6},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := MultiSetPermutation(tt.input)
			if len(result) != tt.expected {
				t.Errorf("MultiSetPermutation count = %d, want %d", len(result), tt.expected)
			}
		})
	}
}

func TestMultiSetPermutationWithStrings(t *testing.T) {
	input := []string{"a", "a", "b"}
	result := MultiSetPermutation(input)

	expected := [][]string{{"a", "a", "b"}, {"a", "b", "a"}, {"b", "a", "a"}}
	if len(result) != len(expected) {
		t.Errorf("MultiSetPermutation count = %d, want %d", len(result), len(expected))
	}

	for _, exp := range expected {
		if !containsCombo(result, exp) {
			t.Errorf("Missing multiset permutation %v", exp)
		}
	}
}

func TestMultiSetPermutationCount(t *testing.T) {
	tests := []struct {
		name      string
		total     int
		counts    []int
		expected  int
		expectErr bool
	}{
		{"all same", 3, []int{3}, 1, false},
		{"two pairs", 4, []int{2, 2}, 6, false},
		{"aab", 3, []int{2, 1}, 3, false},
		{"sum mismatch", 3, []int{2, 2}, 0, true},
		{"negative count", 3, []int{-1, 4}, 0, true},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := MultiSetPermutationCount(tt.total, tt.counts...)
			if tt.expectErr {
				if err == nil {
					t.Error("Expected error, got nil")
				}
			} else {
				if err != nil {
					t.Errorf("Unexpected error: %v", err)
				}
				if result != tt.expected {
					t.Errorf("MultiSetPermutationCount(%d, %v) = %d, want %d", tt.total, tt.counts, result, tt.expected)
				}
			}
		})
	}
}

func TestCartesianProduct(t *testing.T) {
	tests := []struct {
		name     string
		inputs   [][]int
		expected [][]int
	}{
		{
			name:     "empty input",
			inputs:   [][]int{},
			expected: [][]int{{}},
		},
		{
			name:     "single set",
			inputs:   [][]int{{1, 2}},
			expected: [][]int{{1}, {2}},
		},
		{
			name:     "two sets",
			inputs:   [][]int{{1, 2}, {3, 4}},
			expected: [][]int{{1, 3}, {1, 4}, {2, 3}, {2, 4}},
		},
		{
			name:     "three sets",
			inputs:   [][]int{{1}, {2, 3}, {4}},
			expected: [][]int{{1, 2, 4}, {1, 3, 4}},
		},
		{
			name:     "empty set in input",
			inputs:   [][]int{{1, 2}, {}, {3}},
			expected: nil,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := CartesianProduct(tt.inputs...)
			if !reflect.DeepEqual(result, tt.expected) {
				t.Errorf("CartesianProduct() = %v, want %v", result, tt.expected)
			}
		})
	}
}

func TestCartesianProductWithStrings(t *testing.T) {
	inputs := [][]string{{"a", "b"}, {"x", "y"}}
	result := CartesianProduct(inputs...)

	expected := [][]string{{"a", "x"}, {"a", "y"}, {"b", "x"}, {"b", "y"}}
	if !reflect.DeepEqual(result, expected) {
		t.Errorf("CartesianProduct with strings = %v, want %v", result, expected)
	}
}

func TestCartesianProductCount(t *testing.T) {
	tests := []struct {
		name      string
		lengths   []int
		expected  int
		expectErr bool
	}{
		{"empty", []int{}, 1, false},
		{"single", []int{3}, 3, false},
		{"two sets", []int{2, 3}, 6, false},
		{"three sets", []int{2, 2, 2}, 8, false},
		{"zero length", []int{2, 0, 3}, 0, false},
		{"negative", []int{-1, 2}, 0, true},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := CartesianProductCount(tt.lengths...)
			if tt.expectErr {
				if err == nil {
					t.Error("Expected error, got nil")
				}
			} else {
				if err != nil {
					t.Errorf("Unexpected error: %v", err)
				}
				if result != tt.expected {
					t.Errorf("CartesianProductCount(%v) = %d, want %d", tt.lengths, result, tt.expected)
				}
			}
		})
	}
}

func TestCountPowerSet(t *testing.T) {
	tests := []struct {
		name     string
		n        int
		expected int
	}{
		{"0", 0, 1},
		{"1", 1, 2},
		{"2", 2, 4},
		{"3", 3, 8},
		{"10", 10, 1024},
		{"negative", -1, 0},
		{"overflow", 63, 0},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := CountPowerSet(tt.n)
			if result != tt.expected {
				t.Errorf("CountPowerSet(%d) = %d, want %d", tt.n, result, tt.expected)
			}
		})
	}
}

// Benchmark tests
func BenchmarkCombinations(b *testing.B) {
	input := []int{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
	for i := 0; i < b.N; i++ {
		Combinations(input, 5)
	}
}

func BenchmarkPermutations(b *testing.B) {
	input := []int{1, 2, 3, 4, 5, 6, 7}
	for i := 0; i < b.N; i++ {
		Permutations(input)
	}
}

func BenchmarkPowerSet(b *testing.B) {
	input := []int{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
	for i := 0; i < b.N; i++ {
		PowerSet(input)
	}
}

func BenchmarkBinomialCoefficient(b *testing.B) {
	for i := 0; i < b.N; i++ {
		BinomialCoefficient(20, 10)
	}
}

func BenchmarkCartesianProduct(b *testing.B) {
	s1 := []int{1, 2, 3}
	s2 := []int{4, 5, 6}
	s3 := []int{7, 8, 9}
	for i := 0; i < b.N; i++ {
		CartesianProduct(s1, s2, s3)
	}
}