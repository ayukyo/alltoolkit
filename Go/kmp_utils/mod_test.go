package kmp_utils

import (
	"testing"
)

// TestNew tests the creation of KMP searcher
func TestNew(t *testing.T) {
	kmp := New("pattern")
	if kmp == nil {
		t.Fatal("Expected non-nil KMP instance")
	}
	if kmp.GetPattern() != "pattern" {
		t.Errorf("Expected pattern 'pattern', got '%s'", kmp.GetPattern())
	}
	if kmp.GetPatternLength() != 7 {
		t.Errorf("Expected pattern length 7, got %d", kmp.GetPatternLength())
	}
	if !kmp.IsCaseSensitive() {
		t.Error("Expected case-sensitive by default")
	}
}

// TestNewWithOptions tests case-insensitive search
func TestNewWithOptions(t *testing.T) {
	kmp := NewWithOptions("PATTERN", false)
	if kmp.IsCaseSensitive() {
		t.Error("Expected case-insensitive")
	}
}

// TestBuildLPS tests the LPS array construction
func TestBuildLPS(t *testing.T) {
	tests := []struct {
		pattern  string
		expected []int
	}{
		{"ABABCABAB", []int{0, 0, 1, 2, 0, 1, 2, 3, 4}},
		{"AAAA", []int{0, 1, 2, 3}},
		{"ABCDE", []int{0, 0, 0, 0, 0}},
		{"AABAACAABAA", []int{0, 1, 0, 1, 2, 0, 1, 2, 3, 4, 5}},
		{"AAACAAAAAC", []int{0, 1, 2, 0, 1, 2, 3, 3, 3, 4}}, // Corrected: AAACAAAAAC
		{"ABABABAB", []int{0, 0, 1, 2, 3, 4, 5, 6}},
		{"", []int{}},
		{"A", []int{0}},
	}

	for _, tt := range tests {
		lps := BuildLPS(tt.pattern)
		if !equalSlices(lps, tt.expected) {
			t.Errorf("BuildLPS(%q) = %v, expected %v", tt.pattern, lps, tt.expected)
		}
	}
}

// TestFind tests finding first occurrence
func TestFind(t *testing.T) {
	tests := []struct {
		pattern  string
		text     string
		expected int
	}{
		{"ABABCABAB", "ABABDABACDABABCABAB", 10},
		{"ABAB", "ABABABAB", 0},
		{"ABCD", "ABC ABCDAB ABCDABCDABDE", 4},
		{"AAAA", "AAAAAAAA", 0},
		{"ABCD", "ABABABAB", -1},
		{"", "text", -1},
		{"pattern", "", -1},
		{"abc", "xyzabcxyz", 3},
		{"test", "testing test tested", 0}, // "testing" starts with "test"
		{" test", "testing test tested", 7}, // Search for " test" with leading space
	}

	for _, tt := range tests {
		pos := Find(tt.pattern, tt.text)
		if pos != tt.expected {
			t.Errorf("Find(%q, %q) = %d, expected %d", tt.pattern, tt.text, pos, tt.expected)
		}
	}
}

// TestFindAll tests finding all occurrences
func TestFindAll(t *testing.T) {
	tests := []struct {
		pattern  string
		text     string
		expected []int
	}{
		{"ABAB", "ABABABAB", []int{0, 2, 4}},
		{"AA", "AAAAAA", []int{0, 1, 2, 3, 4}},
		{"AB", "ABABABAB", []int{0, 2, 4, 6}},
		{"XYZ", "ABCXYZXYZXYZ", []int{3, 6, 9}},
		{"ABCD", "ABABABAB", []int{}},
		{"", "text", []int{}},
		{"test", "testtest", []int{0, 4}},
	}

	for _, tt := range tests {
		positions := FindAll(tt.pattern, tt.text)
		if !equalSlices(positions, tt.expected) {
			t.Errorf("FindAll(%q, %q) = %v, expected %v", tt.pattern, tt.text, positions, tt.expected)
		}
	}
}

// TestFindIgnoreCase tests case-insensitive search
func TestFindIgnoreCase(t *testing.T) {
	tests := []struct {
		pattern  string
		text     string
		expected int
	}{
		{"PATTERN", "text with Pattern here", 10},
		{"ABC", "aBcAbC", 0},
		{" TEST", "testing TeSt case", 7}, // Search for " test" with leading space
		{"XYZ", "xyzXYZxyz", 0},
	}

	for _, tt := range tests {
		pos := FindIgnoreCase(tt.pattern, tt.text)
		if pos != tt.expected {
			t.Errorf("FindIgnoreCase(%q, %q) = %d, expected %d", tt.pattern, tt.text, pos, tt.expected)
		}
	}
}

// TestFindAllIgnoreCase tests case-insensitive find all
func TestFindAllIgnoreCase(t *testing.T) {
	tests := []struct {
		pattern  string
		text     string
		expected []int
	}{
		{"AB", "aBABabAB", []int{0, 2, 4, 6}},
		{"TEST", "TestTESTtest", []int{0, 4, 8}},
		{"AA", "AaaAAaA", []int{0, 1, 2, 3, 4, 5}}, // Overlapping matches for "aa" case-insensitive
	}

	for _, tt := range tests {
		positions := FindAllIgnoreCase(tt.pattern, tt.text)
		if !equalSlices(positions, tt.expected) {
			t.Errorf("FindAllIgnoreCase(%q, %q) = %v, expected %v", tt.pattern, tt.text, positions, tt.expected)
		}
	}
}

// TestCount tests counting occurrences
func TestCount(t *testing.T) {
	tests := []struct {
		pattern  string
		text     string
		expected int
	}{
		{"AB", "ABABABAB", 4},
		{"AA", "AAAAAA", 5},
		{"X", "XXXXX", 5},
		{"ABCD", "ABABABAB", 0},
		{"", "text", 0},
		{"test", "testtesttest", 3},
	}

	for _, tt := range tests {
		count := Count(tt.pattern, tt.text)
		if count != tt.expected {
			t.Errorf("Count(%q, %q) = %d, expected %d", tt.pattern, tt.text, count, tt.expected)
		}
	}
}

// TestContains tests containment check
func TestContains(t *testing.T) {
	tests := []struct {
		pattern  string
		text     string
		expected bool
	}{
		{"AB", "ABABABAB", true},
		{"XYZ", "ABABABAB", false},
		{"test", "testing", true},
		{"", "text", false},
		{"pattern", "", false},
	}

	for _, tt := range tests {
		result := Contains(tt.pattern, tt.text)
		if result != tt.expected {
			t.Errorf("Contains(%q, %q) = %v, expected %v", tt.pattern, tt.text, result, tt.expected)
		}
	}
}

// TestReplace tests replacement functionality
func TestReplace(t *testing.T) {
	tests := []struct {
		pattern     string
		text        string
		replacement string
		expected    string
	}{
		{"AB", "ABABABAB", "XY", "XYXYXYXY"},
		{"XX", "AAAAAA", "B", "AAAAAA"},    // No match
		{"test", "testtest", "exam", "examexam"},
		{"XYZ", "ABCABC", "123", "ABCABC"},
	}

	for _, tt := range tests {
		result := Replace(tt.pattern, tt.text, tt.replacement)
		if result != tt.expected {
			t.Errorf("Replace(%q, %q, %q) = %q, expected %q", tt.pattern, tt.text, tt.replacement, result, tt.expected)
		}
	}
}

// TestReplaceFirst tests single replacement
func TestReplaceFirst(t *testing.T) {
	tests := []struct {
		pattern     string
		text        string
		replacement string
		expected    string
	}{
		{"AB", "ABABABAB", "XY", "XYABABAB"},
		{"XX", "AAAAAA", "B", "AAAAAA"},   // No match
		{"test", "testtest", "exam", "examtest"},
		{"XYZ", "ABCABC", "123", "ABCABC"},
	}

	for _, tt := range tests {
		result := ReplaceFirst(tt.pattern, tt.text, tt.replacement)
		if result != tt.expected {
			t.Errorf("ReplaceFirst(%q, %q, %q) = %q, expected %q", tt.pattern, tt.text, tt.replacement, result, tt.expected)
		}
	}
}

// TestFindLast tests finding last occurrence
func TestFindLast(t *testing.T) {
	tests := []struct {
		pattern  string
		text     string
		expected int
	}{
		{"AB", "ABABABAB", 6},
		{"AA", "AAAAAA", 4},
		{"test", "testtesttest", 8},
		{"XYZ", "ABCABC", -1},
	}

	for _, tt := range tests {
		kmp := New(tt.pattern)
		pos := kmp.FindLast(tt.text)
		if pos != tt.expected {
			t.Errorf("FindLast(%q, %q) = %d, expected %d", tt.pattern, tt.text, pos, tt.expected)
		}
	}
}

// TestFindMatches tests detailed match information
func TestFindMatches(t *testing.T) {
	matches := FindMatches("AB", "ABABAB")
	expected := []Match{
		{Position: 0, Text: "AB", EndPosition: 2},
		{Position: 2, Text: "AB", EndPosition: 4},
		{Position: 4, Text: "AB", EndPosition: 6},
	}

	if len(matches) != len(expected) {
		t.Fatalf("Expected %d matches, got %d", len(expected), len(matches))
	}

	for i, m := range matches {
		if m.Position != expected[i].Position {
			t.Errorf("Match %d: expected position %d, got %d", i, expected[i].Position, m.Position)
		}
		if m.Text != expected[i].Text {
			t.Errorf("Match %d: expected text %q, got %q", i, expected[i].Text, m.Text)
		}
		if m.EndPosition != expected[i].EndPosition {
			t.Errorf("Match %d: expected end position %d, got %d", i, expected[i].EndPosition, m.EndPosition)
		}
	}
}

// TestMultiPattern tests multi-pattern search
func TestMultiPattern(t *testing.T) {
	mp := NewMultiPattern("cat", "dog", "bird")
	text := "I have a cat and a dog, but no bird"

	// Test FindAny
	idx, pos := mp.FindAny(text)
	if idx < 0 || idx > 2 {
		t.Errorf("FindAny returned invalid index %d", idx)
	}
	if pos < 0 {
		t.Error("FindAny should find at least one pattern")
	}

	// Test ContainsAny
	if !mp.ContainsAny(text) {
		t.Error("ContainsAny should return true")
	}

	// Test FindAll
	all := mp.FindAll(text)
	if len(all) != 3 {
		t.Errorf("Expected 3 patterns with matches, got %d", len(all))
	}

	// Test CountAll
	counts := mp.CountAll(text)
	for i, count := range counts {
		if count != 1 {
			t.Errorf("Pattern %d: expected count 1, got %d", i, count)
		}
	}
}

// TestValidatePattern tests pattern validation
func TestValidatePattern(t *testing.T) {
	tests := []struct {
		pattern  string
		expected string
	}{
		{"valid", ""},
		{"", "pattern cannot be empty"},
		{"\xff\xfe\xfd", "pattern contains invalid UTF-8 encoding"},
	}

	for _, tt := range tests {
		err := ValidatePattern(tt.pattern)
		if err != tt.expected {
			t.Errorf("ValidatePattern(%q) = %q, expected %q", tt.pattern, err, tt.expected)
		}
	}
}

// TestAnalyzePattern tests pattern analysis
func TestAnalyzePattern(t *testing.T) {
	stats := AnalyzePattern("ABABABAB")
	if stats.Length != 8 {
		t.Errorf("Expected length 8, got %d", stats.Length)
	}
	if stats.UniqueChars != 2 {
		t.Errorf("Expected 2 unique chars, got %d", stats.UniqueChars)
	}
	if !stats.HasRepeated {
		t.Error("Expected HasRepeated to be true")
	}
	// ABABABAB reversed is BABABABA, not the same
	if stats.IsPalindrome {
		t.Error("Expected IsPalindrome to be false for ABABABAB")
	}

	stats2 := AnalyzePattern("ABCDE")
	if stats2.HasRepeated {
		t.Error("Expected HasRepeated to be false for ABCDE")
	}
	if stats2.IsPalindrome {
		t.Error("Expected IsPalindrome to be false for ABCDE")
	}

	// Test actual palindrome
	stats3 := AnalyzePattern("ABBA")
	if !stats3.IsPalindrome {
		t.Error("Expected IsPalindrome to be true for ABBA")
	}
}

// TestStreamingKMP tests streaming search
func TestStreamingKMP(t *testing.T) {
	skmp := NewStreamingKMP("ABC")
	data := []byte("XYZABCXYZ")

	positions := skmp.ProcessBytes(data)
	if len(positions) != 1 || positions[0] != 3 {
		t.Errorf("Expected position [3], got %v", positions)
	}

	// Test reset
	skmp.Reset()
	if len(skmp.GetMatches()) != 0 {
		t.Error("Expected no matches after reset")
	}
}

// TestFindOverlapping tests overlapping matches
func TestFindOverlapping(t *testing.T) {
	tests := []struct {
		pattern  string
		text     string
		expected []int
	}{
		{"AA", "AAAA", []int{0, 1, 2}},
		{"ABAB", "ABABABAB", []int{0, 2, 4}},
		{"ABA", "ABABA", []int{0, 2}},
	}

	for _, tt := range tests {
		positions := FindOverlapping(tt.pattern, tt.text)
		if !equalSlices(positions, tt.expected) {
			t.Errorf("FindOverlapping(%q, %q) = %v, expected %v", tt.pattern, tt.text, positions, tt.expected)
		}
	}
}

// TestFindNonOverlapping tests non-overlapping matches
func TestFindNonOverlapping(t *testing.T) {
	tests := []struct {
		pattern  string
		text     string
		expected []int
	}{
		{"AA", "AAAA", []int{0, 2}},
		{"ABAB", "ABABABAB", []int{0, 4}},
		{"ABA", "ABABA", []int{0}},
	}

	for _, tt := range tests {
		positions := FindNonOverlapping(tt.pattern, tt.text)
		if !equalSlices(positions, tt.expected) {
			t.Errorf("FindNonOverlapping(%q, %q) = %v, expected %v", tt.pattern, tt.text, positions, tt.expected)
		}
	}
}

// TestGetLPS tests LPS array retrieval
func TestGetLPS(t *testing.T) {
	kmp := New("ABABCABAB")
	lps := kmp.GetLPS()
	expected := []int{0, 0, 1, 2, 0, 1, 2, 3, 4}

	if !equalSlices(lps, expected) {
		t.Errorf("GetLPS() = %v, expected %v", lps, expected)
	}

	// Verify it's a copy
	lps[0] = 999
	newLPS := kmp.GetLPS()
	if newLPS[0] == 999 {
		t.Error("GetLPS should return a copy")
	}
}

// BenchmarkFind benchmarks the Find operation
func BenchmarkFind(b *testing.B) {
	text := "This is a sample text with a pattern to find. Pattern pattern pattern."
	pattern := "pattern"

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		Find(pattern, text)
	}
}

// BenchmarkFindAll benchmarks the FindAll operation
func BenchmarkFindAll(b *testing.B) {
	text := "ABABABABABABABABABABABABABABABABABABABABABABABABABABABABABABABAB"
	pattern := "ABAB"

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		FindAll(pattern, text)
	}
}

// BenchmarkBuildLPS benchmarks the LPS array construction
func BenchmarkBuildLPS(b *testing.B) {
	pattern := "ABABCABABABABCABAB"

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		BuildLPS(pattern)
	}
}

// BenchmarkStreamingKMP benchmarks streaming search
func BenchmarkStreamingKMP(b *testing.B) {
	pattern := "pattern"
	text := []byte("This is a long text that contains a pattern somewhere in the middle of the string.")
	skmp := NewStreamingKMP(pattern)

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		skmp.Reset()
		skmp.ProcessBytes(text)
	}
}

// Helper function to compare int slices
func equalSlices(a, b []int) bool {
	if len(a) != len(b) {
		return false
	}
	for i := range a {
		if a[i] != b[i] {
			return false
		}
	}
	return true
}