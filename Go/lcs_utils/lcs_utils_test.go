package lcs_utils

import (
	"reflect"
	"strings"
	"testing"
)

// ============================================================================
// Basic LCS Tests
// ============================================================================

func TestLCS(t *testing.T) {
	tests := []struct {
		name     string
		a        []string
		b        []string
		expected []string
	}{
		{
			name:     "Empty sequences",
			a:        []string{},
			b:        []string{},
			expected: []string{},
		},
		{
			name:     "One empty sequence",
			a:        []string{"a", "b", "c"},
			b:        []string{},
			expected: []string{},
		},
		{
			name:     "Same sequences",
			a:        []string{"a", "b", "c"},
			b:        []string{"a", "b", "c"},
			expected: []string{"a", "b", "c"},
		},
		{
			name:     "Basic LCS",
			a:        []string{"a", "b", "c", "d", "e"},
			b:        []string{"a", "c", "e"},
			expected: []string{"a", "c", "e"},
		},
		{
			name:     "Classic example",
			a:        []string{"A", "B", "C", "D", "G", "H"},
			b:        []string{"A", "E", "D", "F", "H", "R"},
			expected: []string{"A", "D", "H"},
		},
		{
			name:     "No common elements",
			a:        []string{"a", "b", "c"},
			b:        []string{"x", "y", "z"},
			expected: []string{},
		},
		{
			name:     "Reversed sequences",
			a:        []string{"a", "b", "c"},
			b:        []string{"c", "b", "a"},
			expected: []string{"a"}, // or "b" or "c", any single element is valid
		},
		{
			name:     "Longer LCS",
			a:        []string{"a", "b", "c", "d", "a", "b", "c", "d"},
			b:        []string{"a", "b", "c", "d"},
			expected: []string{"a", "b", "c", "d"},
		},
		{
			name:     "Multiple possibilities",
			a:        []string{"1", "2", "3", "4", "5"},
			b:        []string{"1", "3", "5", "7", "9"},
			expected: []string{"1", "3", "5"},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := LCS(tt.a, tt.b)
			// For reversed case, check that result is valid (any single element)
			if tt.name == "Reversed sequences" {
				if len(result) != 1 {
					t.Errorf("LCS() length = %v, want 1", len(result))
				}
				return
			}
			if !reflect.DeepEqual(result, tt.expected) {
				t.Errorf("LCS() = %v, want %v", result, tt.expected)
			}
		})
	}
}

func TestLCSLength(t *testing.T) {
	tests := []struct {
		name     string
		a        []string
		b        []string
		expected int
	}{
		{
			name:     "Empty sequences",
			a:        []string{},
			b:        []string{},
			expected: 0,
		},
		{
			name:     "Same sequences",
			a:        []string{"a", "b", "c"},
			b:        []string{"a", "b", "c"},
			expected: 3,
		},
		{
			name:     "Basic LCS",
			a:        []string{"a", "b", "c", "d", "e"},
			b:        []string{"a", "c", "e"},
			expected: 3,
		},
		{
			name:     "No common elements",
			a:        []string{"a", "b", "c"},
			b:        []string{"x", "y", "z"},
			expected: 0,
		},
		{
			name:     "Longer sequences",
			a:        []string{"a", "b", "c", "d", "e", "f", "g", "h"},
			b:        []string{"a", "c", "e", "g"},
			expected: 4,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := LCSLength(tt.a, tt.b)
			if result != tt.expected {
				t.Errorf("LCSLength() = %v, want %v", result, tt.expected)
			}
		})
	}
}

func TestLCSWithIndices(t *testing.T) {
	tests := []struct {
		name          string
		a             []string
		b             []string
		expectedLCS   []string
		expectedLen   int
		checkIndicesA []int
		checkIndicesB []int
	}{
		{
			name:        "Empty sequences",
			a:           []string{},
			b:           []string{},
			expectedLCS: []string{},
			expectedLen: 0,
		},
		{
			name:          "Basic example",
			a:             []string{"a", "b", "c", "d"},
			b:             []string{"a", "c"},
			expectedLCS:   []string{"a", "c"},
			expectedLen:   2,
			checkIndicesA: []int{0, 2},
			checkIndicesB: []int{0, 1},
		},
		{
			name:          "Same sequences",
			a:             []string{"x", "y", "z"},
			b:             []string{"x", "y", "z"},
			expectedLCS:   []string{"x", "y", "z"},
			expectedLen:   3,
			checkIndicesA: []int{0, 1, 2},
			checkIndicesB: []int{0, 1, 2},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := LCSWithIndices(tt.a, tt.b)
			if !reflect.DeepEqual(result.Subsequence, tt.expectedLCS) {
				t.Errorf("Subsequence = %v, want %v", result.Subsequence, tt.expectedLCS)
			}
			if result.Length != tt.expectedLen {
				t.Errorf("Length = %v, want %v", result.Length, tt.expectedLen)
			}
			if len(tt.checkIndicesA) > 0 && !reflect.DeepEqual(result.IndicesA, tt.checkIndicesA) {
				t.Errorf("IndicesA = %v, want %v", result.IndicesA, tt.checkIndicesA)
			}
			if len(tt.checkIndicesB) > 0 && !reflect.DeepEqual(result.IndicesB, tt.checkIndicesB) {
				t.Errorf("IndicesB = %v, want %v", result.IndicesB, tt.checkIndicesB)
			}
		})
	}
}

func TestLCSBytes(t *testing.T) {
	tests := []struct {
		name     string
		a        []byte
		b        []byte
		expected []byte
	}{
		{
			name:     "Empty",
			a:        []byte{},
			b:        []byte{},
			expected: []byte{},
		},
		{
			name:     "Basic",
			a:        []byte("abcde"),
			b:        []byte("ace"),
			expected: []byte("ace"),
		},
		{
			name:     "No common",
			a:        []byte("abc"),
			b:        []byte("xyz"),
			expected: []byte{},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := LCSBytes(tt.a, tt.b)
			if !reflect.DeepEqual(result, tt.expected) {
				t.Errorf("LCSBytes() = %v, want %v", result, tt.expected)
			}
		})
	}
}

func TestLCSString(t *testing.T) {
	tests := []struct {
		name     string
		a        string
		b        string
		expected string
	}{
		{
			name:     "Empty strings",
			a:        "",
			b:        "",
			expected: "",
		},
		{
			name:     "Basic strings",
			a:        "abcde",
			b:        "ace",
			expected: "ace",
		},
		{
			name:     "Unicode strings",
			a:        "你好世界",
			b:        "你好",
			expected: "你好",
		},
		{
			name:     "Mixed content",
			a:        "Hello, World!",
			b:        "Hlo ol!",
			expected: "Hlo ol!",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := LCSString(tt.a, tt.b)
			if result != tt.expected {
				t.Errorf("LCSString() = %v, want %v", result, tt.expected)
			}
		})
	}
}

func TestLCSStringLines(t *testing.T) {
	a := "line1\nline2\nline3\nline4"
	b := "line1\nline3\nline5"

	result := LCSStringLines(a, b)
	expected := []string{"line1", "line3"}

	if !reflect.DeepEqual(result, expected) {
		t.Errorf("LCSStringLines() = %v, want %v", result, expected)
	}
}

// ============================================================================
// LCSAll Tests
// ============================================================================

func TestLCSAll(t *testing.T) {
	tests := []struct {
		name           string
		a              []string
		b              []string
		expectedCount  int
		expectedLength int
	}{
		{
			name:           "Empty sequences",
			a:              []string{},
			b:              []string{},
			expectedCount:  1,
			expectedLength: 0,
		},
		{
			name:           "Same sequences",
			a:              []string{"a", "b", "c"},
			b:              []string{"a", "b", "c"},
			expectedCount:  1,
			expectedLength: 3,
		},
		{
			name:           "Multiple LCS",
			a:              []string{"a", "b", "c"},
			b:              []string{"a", "c", "b"},
			expectedCount:  2, // "ab" or "ac"
			expectedLength: 2,
		},
		{
			name:           "No common",
			a:              []string{"a", "b"},
			b:              []string{"x", "y"},
			expectedCount:  1,
			expectedLength: 0,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			results := LCSAll(tt.a, tt.b)
			if len(results) != tt.expectedCount {
				t.Errorf("LCSAll() count = %v, want %v", len(results), tt.expectedCount)
			}
			for _, result := range results {
				if len(result) != tt.expectedLength {
					t.Errorf("LCSAll() length = %v, want %v", len(result), tt.expectedLength)
				}
			}
		})
	}
}

// ============================================================================
// LCSOfMultiple Tests
// ============================================================================

func TestLCSOfMultiple(t *testing.T) {
	tests := []struct {
		name     string
		seqs     [][]string
		expected []string
	}{
		{
			name:     "Empty input",
			seqs:     [][]string{},
			expected: nil,
		},
		{
			name:     "Single sequence",
			seqs:     [][]string{{"a", "b", "c"}},
			expected: []string{"a", "b", "c"},
		},
		{
			name:     "Two sequences",
			seqs:     [][]string{{"a", "b", "c"}, {"a", "c"}},
			expected: []string{"a", "c"},
		},
		{
			name:     "Three sequences",
			seqs:     [][]string{{"a", "b", "c", "d"}, {"a", "c", "d"}, {"a", "d"}},
			expected: []string{"a", "d"},
		},
		{
			name:     "No common across all",
			seqs:     [][]string{{"a", "b"}, {"c", "d"}, {"e", "f"}},
			expected: nil,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := LCSOfMultiple(tt.seqs...)
			if !reflect.DeepEqual(result, tt.expected) {
				t.Errorf("LCSOfMultiple() = %v, want %v", result, tt.expected)
			}
		})
	}
}

// ============================================================================
// Diff Tests
// ============================================================================

func TestDiff(t *testing.T) {
	tests := []struct {
		name     string
		a        []string
		b        []string
		checkOps map[string]int // operation type -> count
	}{
		{
			name:     "Empty to empty",
			a:        []string{},
			b:        []string{},
			checkOps: map[string]int{"equal": 0, "insert": 0, "delete": 0},
		},
		{
			name:     "All insertions",
			a:        []string{},
			b:        []string{"a", "b", "c"},
			checkOps: map[string]int{"equal": 0, "insert": 3, "delete": 0},
		},
		{
			name:     "All deletions",
			a:        []string{"a", "b", "c"},
			b:        []string{},
			checkOps: map[string]int{"equal": 0, "insert": 0, "delete": 3},
		},
		{
			name:     "Mixed changes",
			a:        []string{"a", "b", "c", "d"},
			b:        []string{"a", "x", "c", "y"},
			checkOps: map[string]int{"equal": 2, "insert": 2, "delete": 2},
		},
		{
			name:     "Same sequences",
			a:        []string{"a", "b", "c"},
			b:        []string{"a", "b", "c"},
			checkOps: map[string]int{"equal": 3, "insert": 0, "delete": 0},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			diff := Diff(tt.a, tt.b)
			counts := map[string]int{}
			for _, op := range diff {
				counts[op.Type]++
			}
			for opType, expectedCount := range tt.checkOps {
				if counts[opType] != expectedCount {
					t.Errorf("Diff() %s count = %v, want %v", opType, counts[opType], expectedCount)
				}
			}
		})
	}
}

func TestDiffString(t *testing.T) {
	a := "line1\nline2\nline3"
	b := "line1\nlineX\nline3"

	diff := DiffString(a, b)
	counts := map[string]int{}
	for _, op := range diff {
		counts[op.Type]++
	}

	if counts["equal"] != 2 {
		t.Errorf("Expected 2 equals, got %d", counts["equal"])
	}
	if counts["insert"] != 1 {
		t.Errorf("Expected 1 insert, got %d", counts["insert"])
	}
	if counts["delete"] != 1 {
		t.Errorf("Expected 1 delete, got %d", counts["delete"])
	}
}

func TestComputeDiffStats(t *testing.T) {
	diff := []DiffResult{
		{Type: "equal", Value: "a"},
		{Type: "equal", Value: "b"},
		{Type: "insert", Value: "x"},
		{Type: "delete", Value: "c"},
	}

	stats := ComputeDiffStats(diff)

	if stats.Additions != 1 {
		t.Errorf("Additions = %v, want 1", stats.Additions)
	}
	if stats.Deletions != 1 {
		t.Errorf("Deletions = %v, want 1", stats.Deletions)
	}
	if stats.Unchanged != 2 {
		t.Errorf("Unchanged = %v, want 2", stats.Unchanged)
	}
	expectedSim := 2.0 / 4.0
	if stats.Similarity != expectedSim {
		t.Errorf("Similarity = %v, want %v", stats.Similarity, expectedSim)
	}
}

// ============================================================================
// Alignment Tests
// ============================================================================

func TestAlign(t *testing.T) {
	tests := []struct {
		name       string
		a          []string
		b          []string
		checkScore int
	}{
		{
			name:       "Empty sequences",
			a:          []string{},
			b:          []string{},
			checkScore: 0,
		},
		{
			name:       "Simple alignment",
			a:          []string{"a", "b", "c"},
			b:          []string{"a", "x", "c"},
			checkScore: 2, // LCS: "ac"
		},
		{
			name:       "Full match",
			a:          []string{"x", "y", "z"},
			b:          []string{"x", "y", "z"},
			checkScore: 3,
		},
		{
			name:       "Partial match",
			a:          []string{"1", "2", "3", "4"},
			b:          []string{"1", "3", "5"},
			checkScore: 2,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := Align(tt.a, tt.b)
			if result.Score != tt.checkScore {
				t.Errorf("Align() Score = %v, want %v", result.Score, tt.checkScore)
			}
			// Check that aligned sequences have same length
			if len(result.AlignedA) != len(result.AlignedB) {
				t.Errorf("Aligned lengths differ: %d vs %d", len(result.AlignedA), len(result.AlignedB))
			}
		})
	}
}

func TestAlignString(t *testing.T) {
	a := "ABCD"
	b := "ACBD"

	result := AlignString(a, b)

	if result.Score != 3 { // LCS: "ABD" or "ACD"
		t.Errorf("Score = %v, want 3", result.Score)
	}

	// Check that both aligned strings have same length
	if len(result.AlignedA) != len(result.AlignedB) {
		t.Errorf("Aligned lengths differ: %d vs %d", len(result.AlignedA), len(result.AlignedB))
	}
}

// ============================================================================
// SCS Tests
// ============================================================================

func TestSCS(t *testing.T) {
	tests := []struct {
		name     string
		a        []string
		b        []string
		expected []string
	}{
		{
			name:     "Empty A",
			a:        []string{},
			b:        []string{"a", "b"},
			expected: []string{"a", "b"},
		},
		{
			name:     "Empty B",
			a:        []string{"a", "b"},
			b:        []string{},
			expected: []string{"a", "b"},
		},
		{
			name:     "Same sequences",
			a:        []string{"a", "b"},
			b:        []string{"a", "b"},
			expected: []string{"a", "b"},
		},
		{
			name:     "No common",
			a:        []string{"a", "b"},
			b:        []string{"c", "d"},
			expected: []string{"a", "b", "c", "d"}, // or any interleaving
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := SCS(tt.a, tt.b)
			// For "No common" case, just check that result contains all elements
			if tt.name == "No common" {
				if len(result) != 4 {
					t.Errorf("SCS() length = %v, want 4", len(result))
				}
				return
			}
			if !reflect.DeepEqual(result, tt.expected) {
				t.Errorf("SCS() = %v, want %v", result, tt.expected)
			}
		})
	}
}

func TestSCSLength(t *testing.T) {
	tests := []struct {
		name     string
		a        []string
		b        []string
		expected int
	}{
		{
			name:     "Empty",
			a:        []string{},
			b:        []string{},
			expected: 0,
		},
		{
			name:     "Same",
			a:        []string{"a", "b"},
			b:        []string{"a", "b"},
			expected: 2,
		},
		{
			name:     "With LCS",
			a:        []string{"a", "b", "c"},
			b:        []string{"a", "c"},
			expected: 3, // 3 + 2 - 2 = 3
		},
		{
			name:     "No common",
			a:        []string{"a", "b"},
			b:        []string{"c", "d"},
			expected: 4, // 2 + 2 - 0 = 4
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := SCSLength(tt.a, tt.b)
			if result != tt.expected {
				t.Errorf("SCSLength() = %v, want %v", result, tt.expected)
			}
		})
	}
}

// ============================================================================
// Edit Distance Tests
// ============================================================================

func TestEditDistance(t *testing.T) {
	tests := []struct {
		name     string
		a        []string
		b        []string
		expected int
	}{
		{
			name:     "Empty",
			a:        []string{},
			b:        []string{},
			expected: 0,
		},
		{
			name:     "Same",
			a:        []string{"a", "b"},
			b:        []string{"a", "b"},
			expected: 0,
		},
		{
			name:     "Insert all",
			a:        []string{},
			b:        []string{"a", "b"},
			expected: 2,
		},
		{
			name:     "Delete all",
			a:        []string{"a", "b"},
			b:        []string{},
			expected: 2,
		},
		{
			name:     "Mixed",
			a:        []string{"a", "b", "c"},
			b:        []string{"a", "c"},
			expected: 1, // delete "b"
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := EditDistance(tt.a, tt.b)
			if result != tt.expected {
				t.Errorf("EditDistance() = %v, want %v", result, tt.expected)
			}
		})
	}
}

func TestEditDistanceString(t *testing.T) {
	tests := []struct {
		name     string
		a        string
		b        string
		expected int
	}{
		{
			name:     "Empty",
			a:        "",
			b:        "",
			expected: 0,
		},
		{
			name:     "Same",
			a:        "abc",
			b:        "abc",
			expected: 0,
		},
		{
			name:     "Different",
			a:        "abc",
			b:        "ac",
			expected: 1,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := EditDistanceString(tt.a, tt.b)
			if result != tt.expected {
				t.Errorf("EditDistanceString() = %v, want %v", result, tt.expected)
			}
		})
	}
}

// ============================================================================
// Similarity Tests
// ============================================================================

func TestSimilarityRatio(t *testing.T) {
	tests := []struct {
		name     string
		a        []string
		b        []string
		expected float64
	}{
		{
			name:     "Empty both",
			a:        []string{},
			b:        []string{},
			expected: 1.0,
		},
		{
			name:     "Same",
			a:        []string{"a", "b"},
			b:        []string{"a", "b"},
			expected: 1.0,
		},
		{
			name:     "No common",
			a:        []string{"a"},
			b:        []string{"b"},
			expected: 0.0,
		},
		{
			name:     "Partial",
			a:        []string{"a", "b", "c"},
			b:        []string{"a", "c"},
			expected: 0.6666666666666666, // 2/3
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := SimilarityRatio(tt.a, tt.b)
			if result != tt.expected {
				t.Errorf("SimilarityRatio() = %v, want %v", result, tt.expected)
			}
		})
	}
}

func TestSimilarityRatioString(t *testing.T) {
	tests := []struct {
		name     string
		a        string
		b        string
		expected float64
	}{
		{
			name:     "Empty",
			a:        "",
			b:        "",
			expected: 1.0,
		},
		{
			name:     "Same",
			a:        "abc",
			b:        "abc",
			expected: 1.0,
		},
		{
			name:     "Half match",
			a:        "abcd",
			b:        "abef",
			expected: 0.5,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := SimilarityRatioString(tt.a, tt.b)
			if result != tt.expected {
				t.Errorf("SimilarityRatioString() = %v, want %v", result, tt.expected)
			}
		})
	}
}

func TestJaccardSimilarity(t *testing.T) {
	tests := []struct {
		name     string
		a        []string
		b        []string
		expected float64
	}{
		{
			name:     "Empty both",
			a:        []string{},
			b:        []string{},
			expected: 1.0,
		},
		{
			name:     "Same",
			a:        []string{"a", "b"},
			b:        []string{"a", "b"},
			expected: 1.0,
		},
		{
			name:     "No common",
			a:        []string{"a"},
			b:        []string{"b"},
			expected: 0.0,
		},
		{
			name:     "Partial",
			a:        []string{"a", "b", "c"},
			b:        []string{"a", "c"},
			expected: 2.0 / 3.0, // LCS=2, Union=3
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := JaccardSimilarity(tt.a, tt.b)
			if result != tt.expected {
				t.Errorf("JaccardSimilarity() = %v, want %v", result, tt.expected)
			}
		})
	}
}

// ============================================================================
// Utility Tests
// ============================================================================

func TestIsSubsequence(t *testing.T) {
	tests := []struct {
		name     string
		a        []string
		b        []string
		expected bool
	}{
		{
			name:     "Empty A",
			a:        []string{},
			b:        []string{"a", "b"},
			expected: true,
		},
		{
			name:     "Empty B",
			a:        []string{"a"},
			b:        []string{},
			expected: false,
		},
		{
			name:     "True subsequence",
			a:        []string{"a", "c"},
			b:        []string{"a", "b", "c"},
			expected: true,
		},
		{
			name:     "Not subsequence",
			a:        []string{"c", "a"},
			b:        []string{"a", "b", "c"},
			expected: false,
		},
		{
			name:     "Same sequence",
			a:        []string{"a", "b"},
			b:        []string{"a", "b"},
			expected: true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := IsSubsequence(tt.a, tt.b)
			if result != tt.expected {
				t.Errorf("IsSubsequence() = %v, want %v", result, tt.expected)
			}
		})
	}
}

func TestIsSubsequenceString(t *testing.T) {
	tests := []struct {
		name     string
		a        string
		b        string
		expected bool
	}{
		{
			name:     "Empty A",
			a:        "",
			b:        "abc",
			expected: true,
		},
		{
			name:     "True",
			a:        "ac",
			b:        "abc",
			expected: true,
		},
		{
			name:     "False",
			a:        "ca",
			b:        "abc",
			expected: false,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := IsSubsequenceString(tt.a, tt.b)
			if result != tt.expected {
				t.Errorf("IsSubsequenceString() = %v, want %v", result, tt.expected)
			}
		})
	}
}

func TestAllSubsequences(t *testing.T) {
	seq := []string{"a", "b"}
	result := AllSubsequences(seq)

	// Should have 2^2 = 4 subsequences
	if len(result) != 4 {
		t.Errorf("AllSubsequences() count = %v, want 4", len(result))
	}

	// Check that empty subsequence is included
	hasEmpty := false
	for _, sub := range result {
		if len(sub) == 0 {
			hasEmpty = true
		}
	}
	if !hasEmpty {
		t.Error("AllSubsequences() should include empty subsequence")
	}
}

func TestCountCommonSubsequences(t *testing.T) {
	tests := []struct {
		name     string
		a        []string
		b        []string
		expected int
	}{
		{
			name:     "Empty",
			a:        []string{},
			b:        []string{},
			expected: 0, // excluding empty subsequence
		},
		{
			name:     "Same single",
			a:        []string{"a"},
			b:        []string{"a"},
			expected: 1,
		},
		{
			name:     "Same pair",
			a:        []string{"a", "b"},
			b:        []string{"a", "b"},
			expected: 3, // "a", "b", "ab"
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := CountCommonSubsequences(tt.a, tt.b)
			if result != tt.expected {
				t.Errorf("CountCommonSubsequences() = %v, want %v", result, tt.expected)
			}
		})
	}
}

func TestLCSHuntSzymanski(t *testing.T) {
	tests := []struct {
		name     string
		a        []string
		b        []string
		checkLen int
	}{
		{
			name:     "Empty",
			a:        []string{},
			b:        []string{},
			checkLen: 0,
		},
		{
			name:     "Same",
			a:        []string{"a", "b"},
			b:        []string{"a", "b"},
			checkLen: 2,
		},
		{
			name:     "Basic",
			a:        []string{"a", "b", "c", "d"},
			b:        []string{"a", "c"},
			checkLen: 2,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := LCSHuntSzymanski(tt.a, tt.b)
			if len(result) != tt.checkLen {
				t.Errorf("LCSHuntSzymanski() length = %v, want %v", len(result), tt.checkLen)
			}
		})
	}
}

// ============================================================================
// Integration Tests
// ============================================================================

func TestIntegrationFullWorkflow(t *testing.T) {
	// Test complete workflow: LCS -> Diff -> Alignment
	a := []string{"H", "e", "l", "l", "o"}
	b := []string{"H", "a", "l", "l", "o"}

	// Compute LCS
	lcs := LCS(a, b)
	if !reflect.DeepEqual(lcs, []string{"H", "l", "l", "o"}) {
		t.Errorf("LCS = %v, want [H, l, l, o]", lcs)
	}

	// Compute Diff
	diff := Diff(a, b)
	stats := ComputeDiffStats(diff)

	// Should have 4 equals, 1 insert, 1 delete
	if stats.Unchanged != 4 {
		t.Errorf("Unchanged = %v, want 4", stats.Unchanged)
	}

	// Compute Alignment
	align := Align(a, b)
	if align.Score != 4 {
		t.Errorf("Alignment Score = %v, want 4", align.Score)
	}
}

func TestIntegrationTextComparison(t *testing.T) {
	text1 := "The quick brown fox jumps"
	text2 := "The lazy brown dog jumps"

	// Get LCS of words
	words1 := strings.Split(text1, " ")
	words2 := strings.Split(text2, " ")

	lcs := LCS(words1, words2)
	expected := []string{"The", "brown", "jumps"}
	if !reflect.DeepEqual(lcs, expected) {
		t.Errorf("Word LCS = %v, want %v", lcs, expected)
	}

	// Get similarity
	sim := SimilarityRatio(words1, words2)
	expectedSim := 3.0 / 5.0
	if sim != expectedSim {
		t.Errorf("Similarity = %v, want %v", sim, expectedSim)
	}
}

func TestIntegrationCodeDiff(t *testing.T) {
	code1 := []string{
		"func main() {",
		"    fmt.Println(\"hello\")",
		"    fmt.Println(\"world\")",
		"}",
	}

	code2 := []string{
		"func main() {",
		"    fmt.Println(\"hello\")",
		"    fmt.Println(\"go\")",
		"    fmt.Println(\"lang\")",
		"}",
	}

	diff := Diff(code1, code2)
	stats := ComputeDiffStats(diff)

	// Should have changes
	if stats.Additions < 1 || stats.Deletions < 1 {
		t.Errorf("Expected changes in code diff, got additions=%d, deletions=%d", stats.Additions, stats.Deletions)
	}
}

// ============================================================================
// Edge Cases
// ============================================================================

func TestEdgeCaseLargeSequences(t *testing.T) {
	// Test with larger sequences to ensure no stack overflow
	a := make([]string, 100)
	b := make([]string, 100)

	for i := 0; i < 100; i++ {
		a[i] = string(rune('a' + i%26))
		b[i] = string(rune('a' + i%26))
	}

	lcs := LCS(a, b)
	if len(lcs) != 100 {
		t.Errorf("Large LCS length = %v, want 100", len(lcs))
	}
}

func TestEdgeCaseRepeatedElements(t *testing.T) {
	a := []string{"a", "a", "a", "a"}
	b := []string{"a", "a"}

	lcs := LCS(a, b)
	if len(lcs) != 2 {
		t.Errorf("LCS with repeats length = %v, want 2", len(lcs))
	}
}

func TestEdgeCaseUnicode(t *testing.T) {
	a := "你好世界你好"
	b := "你好你好"

	lcs := LCSString(a, b)
	// LCS should be "你好你好"
	if !strings.Contains(lcs, "你好") {
		t.Errorf("Unicode LCS = %v, should contain 你好", lcs)
	}
}

func TestEdgeCaseSpecialCharacters(t *testing.T) {
	a := []string{"!", "@", "#", "$", "%"}
	b := []string{"!", "#", "%"}

	lcs := LCS(a, b)
	expected := []string{"!", "#", "%"}
	if !reflect.DeepEqual(lcs, expected) {
		t.Errorf("Special char LCS = %v, want %v", lcs, expected)
	}
}

func TestEdgeCaseWhitespace(t *testing.T) {
	a := []string{" ", " ", " "}
	b := []string{" ", " "}

	lcs := LCS(a, b)
	if len(lcs) != 2 {
		t.Errorf("Whitespace LCS length = %v, want 2", len(lcs))
	}
}

// ============================================================================
// Benchmarks
// ============================================================================

func BenchmarkLCS(b *testing.B) {
	a := []string{"a", "b", "c", "d", "e", "f", "g", "h", "i", "j"}
	seqB := []string{"a", "c", "e", "g", "i", "k", "m", "o", "p", "q"}

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		LCS(a, seqB)
	}
}

func BenchmarkLCSLength(b *testing.B) {
	a := make([]string, 1000)
	seqB := make([]string, 1000)

	for i := 0; i < 1000; i++ {
		a[i] = string(rune('a' + i%26))
		seqB[i] = string(rune('a' + i%26))
	}

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		LCSLength(a, seqB)
	}
}

func BenchmarkDiff(b *testing.B) {
	a := []string{"l", "i", "n", "e", "1", "l", "i", "n", "e", "2"}
	seqB := []string{"l", "i", "n", "e", "X", "l", "i", "n", "e", "Y"}

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		Diff(a, seqB)
	}
}