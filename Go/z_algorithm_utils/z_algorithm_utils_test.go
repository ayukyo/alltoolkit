// Unit tests for Z Algorithm Utilities (Go version)

package zalgorithmutils

import (
	"testing"
)

// ============================================================================
// Z-Array Tests
// ============================================================================

func TestZArrayBasic(t *testing.T) {
	// "aabcaabxaaz" -> [0, 1, 0, 0, 3, 1, 0, 0, 2, 1, 0]
	result := ZArray("aabcaabxaaz")
	expected := []int{0, 1, 0, 0, 3, 1, 0, 0, 2, 1, 0}
	if len(result) != len(expected) {
		t.Errorf("Length mismatch: got %d, want %d", len(result), len(expected))
	}
	for i := range expected {
		if result[i] != expected[i] {
			t.Errorf("Z[%d]: got %d, want %d", i, result[i], expected[i])
		}
	}
}

func TestZArrayEmpty(t *testing.T) {
	result := ZArray("")
	if len(result) != 0 {
		t.Errorf("Empty string should return empty array, got %d elements", len(result))
	}
}

func TestZArraySingleChar(t *testing.T) {
	result := ZArray("a")
	if len(result) != 1 || result[0] != 0 {
		t.Errorf("Single char should return [0], got %v", result)
	}
}

func TestZArrayAllSame(t *testing.T) {
	// "aaaa" -> [0, 3, 2, 1]
	result := ZArray("aaaa")
	expected := []int{0, 3, 2, 1}
	for i := range expected {
		if result[i] != expected[i] {
			t.Errorf("Z[%d]: got %d, want %d", i, result[i], expected[i])
		}
	}
}

func TestZArrayNoMatches(t *testing.T) {
	result := ZArray("abcd")
	for i := 1; i < len(result); i++ {
		if result[i] != 0 {
			t.Errorf("Z[%d]: got %d, want 0", i, result[i])
		}
	}
}

func TestZArrayBytes(t *testing.T) {
	data := []byte("aabcaabxaaz")
	result := ZArrayBytes(data)
	expected := []int{0, 1, 0, 0, 3, 1, 0, 0, 2, 1, 0}
	for i := range expected {
		if result[i] != expected[i] {
			t.Errorf("Z[%d]: got %d, want %d", i, result[i], expected[i])
		}
	}
}

// ============================================================================
// Pattern Matching Tests
// ============================================================================

func TestFindAllOccurrences(t *testing.T) {
	result := FindAllOccurrences("abc", "abcabcabc")
	expected := []int{0, 3, 6}
	if len(result) != len(expected) {
		t.Errorf("Length mismatch: got %d, want %d", len(result), len(expected))
	}
	for i := range expected {
		if result[i] != expected[i] {
			t.Errorf("Position[%d]: got %d, want %d", i, result[i], expected[i])
		}
	}
}

func TestFindAllOccurrencesNotFound(t *testing.T) {
	result := FindAllOccurrences("xyz", "abcabcabc")
	if len(result) != 0 {
		t.Errorf("Should find no occurrences, got %d", len(result))
	}
}

func TestFindFirstOccurrence(t *testing.T) {
	tests := []struct {
		pattern string
		text    string
		want    int
	}{
		{"abc", "xyzabc", 3},
		{"abc", "abcabc", 0},
		{"abc", "xyz", -1},
		{"", "abc", -1},
		{"abc", "", -1},
	}

	for _, tt := range tests {
		got := FindFirstOccurrence(tt.pattern, tt.text)
		if got != tt.want {
			t.Errorf("FindFirstOccurrence(%s, %s): got %d, want %d", tt.pattern, tt.text, got, tt.want)
		}
	}
}

func TestCountOccurrences(t *testing.T) {
	tests := []struct {
		pattern string
		text    string
		want    int
	}{
		{"a", "banana", 3},
		{"ana", "banana", 2},
		{"xyz", "abcabc", 0},
	}

	for _, tt := range tests {
		got := CountOccurrences(tt.pattern, tt.text)
		if got != tt.want {
			t.Errorf("CountOccurrences(%s, %s): got %d, want %d", tt.pattern, tt.text, got, tt.want)
		}
	}
}

func TestFindMatches(t *testing.T) {
	matches := FindMatches("abc", "abcabc")
	if len(matches) != 2 {
		t.Errorf("Should find 2 matches, got %d", len(matches))
	}
	if matches[0].Index != 0 || matches[0].Length != 3 {
		t.Errorf("First match: got index=%d, length=%d, want 0, 3", matches[0].Index, matches[0].Length)
	}
	if matches[1].Index != 3 || matches[1].Length != 3 {
		t.Errorf("Second match: got index=%d, length=%d, want 3, 3", matches[1].Index, matches[1].Length)
	}
}

// ============================================================================
// Substring Analysis Tests
// ============================================================================

func TestLongestPrefixSuffix(t *testing.T) {
	tests := []struct {
		s    string
		want int
	}{
		{"ababa", 3},   // "aba"
		{"aaaa", 3},    // "aaa"
		{"abcd", 0},
		{"", 0},
	}

	for _, tt := range tests {
		got := LongestPrefixSuffix(tt.s)
		if got != tt.want {
			t.Errorf("LongestPrefixSuffix(%s): got %d, want %d", tt.s, got, tt.want)
		}
	}
}

func TestLongestRepeatedSubstring(t *testing.T) {
	substr, positions := LongestRepeatedSubstring("banana")
	if substr != "ana" {
		t.Errorf("Got substr=%s, want 'ana'", substr)
	}
	found := false
	for _, pos := range positions {
		if pos == 1 || pos == 3 {
			found = true
		}
	}
	if !found {
		t.Errorf("Positions should include 1 or 3, got %v", positions)
	}
}

func TestLongestCommonPrefix(t *testing.T) {
	tests := []struct {
		s1   string
		s2   string
		want int
	}{
		{"abcdef", "abcxyz", 3},
		{"xyz", "abc", 0},
		{"same", "same", 4},
	}

	for _, tt := range tests {
		got := LongestCommonPrefix(tt.s1, tt.s2)
		if got != tt.want {
			t.Errorf("LongestCommonPrefix(%s, %s): got %d, want %d", tt.s1, tt.s2, got, tt.want)
		}
	}
}

// ============================================================================
// Period Detection Tests
// ============================================================================

func TestFindMinimalPeriod(t *testing.T) {
	period := FindMinimalPeriod("abcabcabc")
	if period.Period != 3 {
		t.Errorf("Got period=%d, want 3", period.Period)
	}
	if !period.IsPeriodic {
		t.Errorf("Should be periodic")
	}

	period = FindMinimalPeriod("abcde")
	if period.Period != 5 {
		t.Errorf("Got period=%d, want 5", period.Period)
	}
	if period.IsPeriodic {
		t.Errorf("Should not be periodic")
	}
}

func TestIsRotation(t *testing.T) {
	tests := []struct {
		s1   string
		s2   string
		want bool
	}{
		{"abcde", "cdeab", true},
		{"abc", "abc", true},
		{"abcde", "abced", false},
		{"abc", "abcd", false},
	}

	for _, tt := range tests {
		got := IsRotation(tt.s1, tt.s2)
		if got != tt.want {
			t.Errorf("IsRotation(%s, %s): got %v, want %v", tt.s1, tt.s2, got, tt.want)
		}
	}
}

func TestFindAllRotations(t *testing.T) {
	rotations := FindAllRotations("abc")
	if len(rotations) != 3 {
		t.Errorf("Should have 3 rotations, got %d", len(rotations))
	}

	expected := []string{"abc", "bca", "cab"}
	for _, exp := range expected {
		found := false
		for _, rot := range rotations {
			if rot == exp {
				found = true
			}
		}
		if !found {
			t.Errorf("Missing rotation %s", exp)
		}
	}
}

// ============================================================================
// Compression Tests
// ============================================================================

func TestCompressString(t *testing.T) {
	pattern, count := CompressString("abcabcabc")
	if pattern != "abc" {
		t.Errorf("Got pattern=%s, want 'abc'", pattern)
	}
	if count != 3 {
		t.Errorf("Got count=%d, want 3", count)
	}

	pattern, count = CompressString("abcde")
	if pattern != "abcde" {
		t.Errorf("Got pattern=%s, want 'abcde'", pattern)
	}
	if count != 1 {
		t.Errorf("Got count=%d, want 1", count)
	}
}

func TestDecompressString(t *testing.T) {
	result := DecompressString("abc", 3)
	if result != "abcabcabc" {
		t.Errorf("Got %s, want 'abcabcabc'", result)
	}
}

// ============================================================================
// Similarity Tests
// ============================================================================

func TestSimilarityScore(t *testing.T) {
	tests := []struct {
		s1   string
		s2   string
		want float64
	}{
		{"abcdef", "abcxyz", 0.5},
		{"same", "same", 1.0},
		{"abc", "xyz", 0.0},
		{"", "", 1.0},
		{"abc", "", 0.0},
	}

	for _, tt := range tests {
		got := SimilarityScore(tt.s1, tt.s2)
		if got != tt.want {
			t.Errorf("SimilarityScore(%s, %s): got %f, want %f", tt.s1, tt.s2, got, tt.want)
		}
	}
}

func TestBatchSimilarity(t *testing.T) {
	base := "abcdef"
	strings := []string{"abcxyz", "abcdef", "xyz", ""}
	scores := BatchSimilarity(base, strings)
	if len(scores) != 4 {
		t.Errorf("Should have 4 scores, got %d", len(scores))
	}
}

// ============================================================================
// Utility Tests
// ============================================================================

func TestValidateZArray(t *testing.T) {
	s := "aabcaabxaaz"
	z := ZArray(s)
	if !ValidateZArray(s, z) {
		t.Errorf("Computed Z-array should be valid")
	}

	invalidZ := []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}
	if ValidateZArray(s, invalidZ) {
		t.Errorf("Invalid Z-array should not be valid")
	}
}

func TestVisualizeZArray(t *testing.T) {
	vis := VisualizeZArray("aaaa")
	if vis == "" {
		t.Errorf("Visualization should not be empty")
	}
	if !contains(vis, "aaaa") {
		t.Errorf("Visualization should contain the string")
	}
}

func contains(s, substr string) bool {
	for i := 0; i <= len(s)-len(substr); i++ {
		if s[i:i+len(substr)] == substr {
			return true
		}
	}
	return false
}

// ============================================================================
// Pattern Matcher Tests
// ============================================================================

func TestZPatternMatcherSingle(t *testing.T) {
	matcher := NewZPatternMatcher([]string{"abc"})
	results := matcher.Search("abcabc")
	if len(results) != 2 {
		t.Errorf("Should find 2 matches, got %d", len(results))
	}
}

func TestZPatternMatcherMultiple(t *testing.T) {
	matcher := NewZPatternMatcher([]string{"ab", "bc"})
	results := matcher.Search("abcabc")
	if len(results) != 4 {
		t.Errorf("Should find 4 matches (2 'ab' + 2 'bc'), got %d", len(results))
	}
}

func TestZPatternMatcherSearchFirst(t *testing.T) {
	matcher := NewZPatternMatcher([]string{"bc", "ab"})
	result := matcher.SearchFirst("abcabc")
	if result == nil {
		t.Errorf("Should find first match")
	}
	if result.Position != 0 {
		t.Errorf("First match should be at position 0, got %d", result.Position)
	}
}

func TestZPatternMatcherCountAll(t *testing.T) {
	matcher := NewZPatternMatcher([]string{"a", "b", "c"})
	counts := matcher.CountAll("abcabc")
	if counts["a"] != 2 {
		t.Errorf("Count for 'a' should be 2, got %d", counts["a"])
	}
}

func TestZPatternMatcherNoMatch(t *testing.T) {
	matcher := NewZPatternMatcher([]string{"xyz"})
	results := matcher.Search("abcabc")
	if len(results) != 0 {
		t.Errorf("Should find no matches, got %d", len(results))
	}
	if matcher.SearchFirst("abcabc") != nil {
		t.Errorf("Should return nil for no match")
	}
}

// ============================================================================
// Helper Function Tests
// ============================================================================

func TestContains(t *testing.T) {
	if !Contains("abc", "abcabc") {
		t.Errorf("'abcabc' should contain 'abc'")
	}
	if Contains("xyz", "abcabc") {
		t.Errorf("'abcabc' should not contain 'xyz'")
	}
}

func TestReplaceAll(t *testing.T) {
	result := ReplaceAll("abc", "xyz", "abcabcabc")
	if result != "xyzxyzxyz" {
		t.Errorf("Got %s, want 'xyzxyzxyz'", result)
	}
}

func TestSplitByPattern(t *testing.T) {
	parts := SplitByPattern(",", "a,b,c")
	if len(parts) != 3 {
		t.Errorf("Should have 3 parts, got %d", len(parts))
	}
}

// ============================================================================
// Data Types Tests
// ============================================================================

func TestZMatchString(t *testing.T) {
	m := ZMatch{Index: 2, Length: 3, Text: "abcdef"}
	substr := m.String()
	if substr != "cde" {
		t.Errorf("Got %s, want 'cde'", substr)
	}
}

func TestStringPeriodPeriodString(t *testing.T) {
	p := StringPeriod{String: "abcabc", Period: 3, IsPeriodic: true}
	period := p.PeriodString()
	if period != "abc" {
		t.Errorf("Got %s, want 'abc'", period)
	}
}