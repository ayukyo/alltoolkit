package text_similarity_utils

import (
	"math"
	"testing"
)

// ============================================================================
// Levenshtein Distance Tests
// ============================================================================

func TestLevenshteinDistance(t *testing.T) {
	tests := []struct {
		s1, s2   string
		expected int
	}{
		{"", "", 0},
		{"a", "", 1},
		{"", "a", 1},
		{"kitten", "sitting", 3},
		{"saturday", "sunday", 3},
		{"hello", "hello", 0},
		{"abc", "xyz", 3},
		{"", "abc", 3},
		{"abc", "", 3},
		{"北京", "南京", 1},
		{"日本語", "日本語", 0},
	}

	for _, tt := range tests {
		result := LevenshteinDistance(tt.s1, tt.s2)
		if result != tt.expected {
			t.Errorf("LevenshteinDistance(%q, %q) = %d, want %d", tt.s1, tt.s2, result, tt.expected)
		}
	}
}

func TestLevenshteinSimilarity(t *testing.T) {
	tests := []struct {
		s1, s2   string
		min, max float64
	}{
		{"hello", "hello", 1.0, 1.0},
		{"", "", 1.0, 1.0},
		{"abc", "xyz", 0.0, 0.1},
		{"kitten", "sitting", 0.5, 0.6},
	}

	for _, tt := range tests {
		result := LevenshteinSimilarity(tt.s1, tt.s2)
		if result < tt.min || result > tt.max {
			t.Errorf("LevenshteinSimilarity(%q, %q) = %v, want [%v, %v]", tt.s1, tt.s2, result, tt.min, tt.max)
		}
	}
}

// ============================================================================
// Damerau-Levenshtein Distance Tests
// ============================================================================

func TestDamerauLevenshteinDistance(t *testing.T) {
	tests := []struct {
		s1, s2   string
		expected int
	}{
		{"", "", 0},
		{"a", "", 1},
		{"", "a", 1},
		{"ca", "abc", 2},
		{"abcd", "acbd", 1}, // transposition
		{"hello", "hello", 0},
	}

	for _, tt := range tests {
		result := DamerauLevenshteinDistance(tt.s1, tt.s2)
		if result != tt.expected {
			t.Errorf("DamerauLevenshteinDistance(%q, %q) = %d, want %d", tt.s1, tt.s2, result, tt.expected)
		}
	}
}

// ============================================================================
// Jaccard Similarity Tests
// ============================================================================

func TestJaccardSimilarity(t *testing.T) {
	tests := []struct {
		s1, s2   string
		ngram    int
		expected float64
		delta    float64
	}{
		{"", "", 2, 1.0, 0.0},
		{"abc", "abc", 2, 1.0, 0.0},
		{"hello", "world", 2, 0.0, 0.1},
		{"night", "nacht", 2, 0.25, 0.1},
		{"abc", "", 2, 0.0, 0.0},
		{"", "abc", 2, 0.0, 0.0},
	}

	for _, tt := range tests {
		result := JaccardSimilarity(tt.s1, tt.s2, tt.ngram)
		if math.Abs(result-tt.expected) > tt.delta {
			t.Errorf("JaccardSimilarity(%q, %q, %d) = %v, want %v", tt.s1, tt.s2, tt.ngram, result, tt.expected)
		}
	}
}

func TestJaccardSimilarityWords(t *testing.T) {
	tests := []struct {
		s1, s2   string
		expected float64
		delta    float64
	}{
		{"", "", 1.0, 0.0},
		{"hello world", "hello world", 1.0, 0.0},
		{"hello world", "world hello", 1.0, 0.0},
		{"the quick fox", "the quick brown fox", 0.75, 0.1},
		{"apple banana", "cherry date", 0.0, 0.0},
	}

	for _, tt := range tests {
		result := JaccardSimilarityWords(tt.s1, tt.s2)
		if math.Abs(result-tt.expected) > tt.delta {
			t.Errorf("JaccardSimilarityWords(%q, %q) = %v, want %v", tt.s1, tt.s2, result, tt.expected)
		}
	}
}

// ============================================================================
// Cosine Similarity Tests
// ============================================================================

func TestCosineSimilarity(t *testing.T) {
	tests := []struct {
		s1, s2   string
		ngram    int
		min      float64
		max      float64
	}{
		{"", "", 2, 1.0, 1.0},
		{"abc", "abc", 2, 1.0, 1.0},
		{"hello", "hallo", 2, 0.5, 1.0},
		{"abc", "xyz", 2, 0.0, 0.1},
	}

	for _, tt := range tests {
		result := CosineSimilarity(tt.s1, tt.s2, tt.ngram)
		if result < tt.min || result > tt.max {
			t.Errorf("CosineSimilarity(%q, %q, %d) = %v, want [%v, %v]", tt.s1, tt.s2, tt.ngram, result, tt.min, tt.max)
		}
	}
}

// ============================================================================
// Sorensen-Dice Coefficient Tests
// ============================================================================

func TestSorensenDiceCoefficient(t *testing.T) {
	tests := []struct {
		s1, s2   string
		ngram    int
		expected float64
		delta    float64
	}{
		{"", "", 2, 1.0, 0.0},
		{"abc", "abc", 2, 1.0, 0.0},
		{"night", "nacht", 2, 0.4, 0.1},
		{"hello", "world", 2, 0.0, 0.1},
	}

	for _, tt := range tests {
		result := SorensenDiceCoefficient(tt.s1, tt.s2, tt.ngram)
		if math.Abs(result-tt.expected) > tt.delta {
			t.Errorf("SorensenDiceCoefficient(%q, %q, %d) = %v, want %v", tt.s1, tt.s2, tt.ngram, result, tt.expected)
		}
	}
}

// ============================================================================
// Hamming Distance Tests
// ============================================================================

func TestHammingDistance(t *testing.T) {
	tests := []struct {
		s1, s2   string
		expected int
	}{
		{"", "", 0},
		{"hello", "hello", 0},
		{"karolin", "kathrin", 3},
		{"1011101", "1001001", 2},
		{"abc", "xyz", 3},
		{"different", "length", -1}, // different lengths
	}

	for _, tt := range tests {
		result := HammingDistance(tt.s1, tt.s2)
		if result != tt.expected {
			t.Errorf("HammingDistance(%q, %q) = %d, want %d", tt.s1, tt.s2, result, tt.expected)
		}
	}
}

func TestHammingSimilarity(t *testing.T) {
	tests := []struct {
		s1, s2   string
		expected float64
		delta    float64
	}{
		{"", "", 1.0, 0.0},
		{"hello", "hello", 1.0, 0.0},
		{"karolin", "kathrin", 4.0/7.0, 0.01},
		{"abc", "xyz", 0.0, 0.0},
		{"different", "length", -1.0, 0.0}, // different lengths
	}

	for _, tt := range tests {
		result := HammingSimilarity(tt.s1, tt.s2)
		if math.Abs(result-tt.expected) > tt.delta {
			t.Errorf("HammingSimilarity(%q, %q) = %v, want %v", tt.s1, tt.s2, result, tt.expected)
		}
	}
}

// ============================================================================
// Jaro Similarity Tests
// ============================================================================

func TestJaroSimilarity(t *testing.T) {
	tests := []struct {
		s1, s2   string
		min      float64
		max      float64
	}{
		{"", "", 1.0, 1.0},
		{"MARTHA", "MARHTA", 0.9, 1.0},
		{"hello", "hello", 1.0, 1.0},
		{"abc", "xyz", 0.0, 0.1},
		{"DWAYNE", "DUANE", 0.7, 0.9},
	}

	for _, tt := range tests {
		result := JaroSimilarity(tt.s1, tt.s2)
		if result < tt.min || result > tt.max {
			t.Errorf("JaroSimilarity(%q, %q) = %v, want [%v, %v]", tt.s1, tt.s2, result, tt.min, tt.max)
		}
	}
}

// ============================================================================
// Jaro-Winkler Similarity Tests
// ============================================================================

func TestJaroWinklerSimilarity(t *testing.T) {
	tests := []struct {
		s1, s2   string
		min      float64
		max      float64
	}{
		{"", "", 1.0, 1.0},
		{"MARTHA", "MARHTA", 0.9, 1.0},
		{"hello", "hello", 1.0, 1.0},
		{"abc", "xyz", 0.0, 0.2},
		{"DWAYNE", "DUANE", 0.8, 1.0},
	}

	for _, tt := range tests {
		result := JaroWinklerSimilarity(tt.s1, tt.s2)
		if result < tt.min || result > tt.max {
			t.Errorf("JaroWinklerSimilarity(%q, %q) = %v, want [%v, %v]", tt.s1, tt.s2, result, tt.min, tt.max)
		}
	}

	// Jaro-Winkler should be >= Jaro for same strings
	s1, s2 := "MARTHA", "MARHTA"
	jaro := JaroSimilarity(s1, s2)
	jw := JaroWinklerSimilarity(s1, s2)
	if jw < jaro {
		t.Errorf("JaroWinklerSimilarity(%q, %q) = %v should be >= JaroSimilarity = %v", s1, s2, jw, jaro)
	}
}

// ============================================================================
// Soundex Tests
// ============================================================================

func TestSoundex(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"Robert", "R163"},
		{"Rupert", "R163"},
		{"Rubin", "R150"},
		{"Ashcraft", "A261"},
		{"Ashcroft", "A261"},
		{"Tymczak", "T522"},
		{"Pfister", "P236"},
		{"", ""},
	}

	for _, tt := range tests {
		result := Soundex(tt.input)
		if result != tt.expected {
			t.Errorf("Soundex(%q) = %q, want %q", tt.input, result, tt.expected)
		}
	}
}

func TestSoundexSimilarity(t *testing.T) {
	tests := []struct {
		s1, s2   string
		expected float64
	}{
		{"Robert", "Rupert", 1.0}, // Same Soundex
		{"Ashcraft", "Ashcroft", 1.0},
		{"hello", "world", 0.0},
	}

	for _, tt := range tests {
		result := SoundexSimilarity(tt.s1, tt.s2)
		if result != tt.expected {
			t.Errorf("SoundexSimilarity(%q, %q) = %v, want %v", tt.s1, tt.s2, result, tt.expected)
		}
	}
}

// ============================================================================
// N-Gram Similarity Tests
// ============================================================================

func TestNGramSimilarity(t *testing.T) {
	tests := []struct {
		s1, s2   string
		n        int
		min      float64
		max      float64
	}{
		{"", "", 2, 1.0, 1.0},
		{"abc", "abc", 2, 1.0, 1.0},
		{"hello", "hallo", 2, 0.5, 1.0},
		{"abc", "xyz", 2, 0.0, 0.1},
	}

	for _, tt := range tests {
		result := NGramSimilarity(tt.s1, tt.s2, tt.n)
		if result < tt.min || result > tt.max {
			t.Errorf("NGramSimilarity(%q, %q, %d) = %v, want [%v, %v]", tt.s1, tt.s2, tt.n, result, tt.min, tt.max)
		}
	}
}

// ============================================================================
// Most Similar Tests
// ============================================================================

func TestMostSimilar(t *testing.T) {
	target := "hello"
	candidates := []string{"hallo", "hello", "helo", "world", "hell"}

	tests := []struct {
		algorithm string
		wantIn    []string // Expected best match should be one of these
	}{
		{"levenshtein", []string{"hello"}},
		{"jaro", []string{"hello"}},
		{"jarowinkler", []string{"hello"}},
		{"jaccard", []string{"hello"}},
		{"cosine", []string{"hello"}},
	}

	for _, tt := range tests {
		result := MostSimilar(target, candidates, tt.algorithm, 2)
		found := false
		for _, expected := range tt.wantIn {
			if result.Text == expected {
				found = true
				break
			}
		}
		if !found {
			t.Errorf("MostSimilar(%q, candidates, %q) = %q, want one of %v", target, tt.algorithm, result.Text, tt.wantIn)
		}
		if result.Score < 0 || result.Score > 1 {
			t.Errorf("MostSimilar score %v out of range [0, 1]", result.Score)
		}
	}
}

func TestMostSimilarEmpty(t *testing.T) {
	result := MostSimilar("hello", []string{}, "levenshtein", 2)
	if result.Text != "" {
		t.Errorf("MostSimilar with empty candidates should return empty text, got %q", result.Text)
	}
}

// ============================================================================
// All Similarities Tests
// ============================================================================

func TestAllSimilarities(t *testing.T) {
	target := "apple"
	candidates := []string{"apply", "apples", "orange", "banana"}

	results := AllSimilarities(target, candidates, "levenshtein", 2)

	if len(results) != len(candidates) {
		t.Errorf("AllSimilarities returned %d results, want %d", len(results), len(candidates))
	}

	// Results should be sorted by score (descending)
	for i := 1; i < len(results); i++ {
		if results[i].Score > results[i-1].Score {
			t.Errorf("AllSimilarities results not sorted: [%d].Score=%v > [%d].Score=%v", i, results[i].Score, i-1, results[i-1].Score)
		}
	}
}

// ============================================================================
// Unicode Support Tests
// ============================================================================

func TestUnicodeSupport(t *testing.T) {
	// Chinese characters
	dist := LevenshteinDistance("北京", "南京")
	if dist != 1 {
		t.Errorf("LevenshteinDistance for Chinese: got %d, want 1", dist)
	}

	sim := LevenshteinSimilarity("你好世界", "你好中国")
	if sim < 0.5 || sim > 0.8 {
		t.Errorf("LevenshteinSimilarity for Chinese: got %v, want [0.5, 0.8]", sim)
	}

	// Japanese
	jwSim := JaroWinklerSimilarity("日本語", "日本語")
	if jwSim != 1.0 {
		t.Errorf("JaroWinklerSimilarity for identical Japanese: got %v, want 1.0", jwSim)
	}

	// Emoji
	emojiDist := LevenshteinDistance("😀😁😂", "😀😃😂")
	if emojiDist != 1 {
		t.Errorf("LevenshteinDistance for emoji: got %d, want 1", emojiDist)
	}
}

// ============================================================================
// Edge Cases Tests
// ============================================================================

func TestEdgeCases(t *testing.T) {
	// Very long strings
	longStr := strings.Repeat("a", 1000)
	longDist := LevenshteinDistance(longStr, longStr)
	if longDist != 0 {
		t.Errorf("LevenshteinDistance for identical long strings: got %d, want 0", longDist)
	}

	// Single character
	hamming := HammingDistance("a", "b")
	if hamming != 1 {
		t.Errorf("HammingDistance for single chars: got %d, want 1", hamming)
	}

	// Zero n-gram size (should default to 2)
	jaccard := JaccardSimilarity("abc", "abc", 0)
	if jaccard != 1.0 {
		t.Errorf("JaccardSimilarity with n=0: got %v, want 1.0", jaccard)
	}
}

// ============================================================================
// Benchmark Tests
// ============================================================================

func BenchmarkLevenshteinDistance(b *testing.B) {
	s1 := "kitten"
	s2 := "sitting"
	for i := 0; i < b.N; i++ {
		LevenshteinDistance(s1, s2)
	}
}

func BenchmarkJaroWinklerSimilarity(b *testing.B) {
	s1 := "MARTHA"
	s2 := "MARHTA"
	for i := 0; i < b.N; i++ {
		JaroWinklerSimilarity(s1, s2)
	}
}

func BenchmarkMostSimilar(b *testing.B) {
	target := "hello"
	candidates := []string{"hallo", "helo", "hell", "help", "held"}
	for i := 0; i < b.N; i++ {
		MostSimilar(target, candidates, "levenshtein", 2)
	}
}