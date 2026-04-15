package diffutils

import (
	"strings"
	"testing"
)

// ========== DiffLines Tests ==========

func TestDiffLinesIdentical(t *testing.T) {
	a := "hello\nworld"
	result := DiffLines(a, a)

	if len(result.Diffs) != 2 {
		t.Errorf("Expected 2 diffs for identical strings, got %d", len(result.Diffs))
	}

	if result.Stats.Added != 0 || result.Stats.Removed != 0 {
		t.Errorf("Expected no changes for identical strings, got +added/-removed: %d/%d",
			result.Stats.Added, result.Stats.Removed)
	}

	for i, d := range result.Diffs {
		if d.Type != Equal {
			t.Errorf("Diff %d: expected Equal, got %v", i, d.Type)
		}
	}
}

func TestDiffLinesEmpty(t *testing.T) {
	result := DiffLines("", "")

	if len(result.Diffs) != 0 {
		t.Errorf("Expected 0 diffs for empty strings, got %d", len(result.Diffs))
	}
}

func TestDiffLinesInsertion(t *testing.T) {
	a := "line1\nline3"
	b := "line1\nline2\nline3"

	result := DiffLines(a, b)

	if result.Stats.Added != 1 {
		t.Errorf("Expected 1 addition, got %d", result.Stats.Added)
	}

	// Verify the inserted line is "line2"
	foundInsert := false
	for _, d := range result.Diffs {
		if d.Type == Insert && d.Text == "line2" {
			foundInsert = true
			break
		}
	}
	if !foundInsert {
		t.Error("Expected to find 'line2' as insertion")
	}
}

func TestDiffLinesDeletion(t *testing.T) {
	a := "line1\nline2\nline3"
	b := "line1\nline3"

	result := DiffLines(a, b)

	if result.Stats.Removed != 1 {
		t.Errorf("Expected 1 removal, got %d", result.Stats.Removed)
	}
}

func TestDiffLinesModification(t *testing.T) {
	a := "hello\nworld"
	b := "hello\ngo"

	result := DiffLines(a, b)

	if result.Stats.Removed != 1 || result.Stats.Added != 1 {
		t.Errorf("Expected 1 removal and 1 addition, got %d removed, %d added",
			result.Stats.Removed, result.Stats.Added)
	}
}

func TestDiffLinesUnicode(t *testing.T) {
	a := "你好\n世界"
	b := "你好\n世界！"

	result := DiffLines(a, b)

	if result.Stats.Removed != 1 || result.Stats.Added != 1 {
		t.Errorf("Expected modification for Unicode, got %d removed, %d added",
			result.Stats.Removed, result.Stats.Added)
	}
}

func TestDiffLinesMultipleChanges(t *testing.T) {
	a := "line1\nline2\nline3\nline4"
	b := "line0\nline1\nline3\nline5"

	result := DiffLines(a, b)

	if result.Stats.Added != 2 {
		t.Errorf("Expected 2 additions, got %d", result.Stats.Added)
	}
	if result.Stats.Removed != 2 {
		t.Errorf("Expected 2 removals, got %d", result.Stats.Removed)
	}
}

// ========== DiffChars Tests ==========

func TestDiffCharsIdentical(t *testing.T) {
	diffs := DiffChars("hello", "hello")

	for i, d := range diffs {
		if d.Type != Equal {
			t.Errorf("Diff %d: expected Equal, got %v", i, d.Type)
		}
	}
}

func TestDiffCharsInsert(t *testing.T) {
	diffs := DiffChars("ac", "abc")

	foundInsert := false
	for _, d := range diffs {
		if d.Type == Insert && d.Text == "b" {
			foundInsert = true
			break
		}
	}
	if !foundInsert {
		t.Error("Expected to find 'b' as insertion")
	}
}

func TestDiffCharsDelete(t *testing.T) {
	diffs := DiffChars("abc", "ac")

	foundDelete := false
	for _, d := range diffs {
		if d.Type == Delete && d.Text == "b" {
			foundDelete = true
			break
		}
	}
	if !foundDelete {
		t.Error("Expected to find 'b' as deletion")
	}
}

func TestDiffCharsReplace(t *testing.T) {
	diffs := DiffChars("cat", "bat")

	if len(diffs) < 2 {
		t.Error("Expected at least 2 diffs for replacement")
	}

	// First character should show deletion and insertion
	if diffs[0].Type != Delete || diffs[0].Text != "c" {
		t.Errorf("Expected first diff to be deletion of 'c', got %v '%s'", diffs[0].Type, diffs[0].Text)
	}
}

func TestDiffCharsUnicode(t *testing.T) {
	diffs := DiffChars("你好", "你坏")

	if len(diffs) == 0 {
		t.Error("Expected non-empty diff result")
	}

	// Should detect character change
	foundChange := false
	for _, d := range diffs {
		if d.Type != Equal {
			foundChange = true
			break
		}
	}
	if !foundChange {
		t.Error("Expected to detect Unicode character change")
	}
}

// ========== DiffWords Tests ==========

func TestDiffWordsIdentical(t *testing.T) {
	diffs := DiffWords("hello world", "hello world")

	for i, d := range diffs {
		if d.Type != Equal {
			t.Errorf("Diff %d: expected Equal, got %v", i, d.Type)
		}
	}
}

func TestDiffWordsInsert(t *testing.T) {
	diffs := DiffWords("hello world", "hello beautiful world")

	foundInsert := false
	for _, d := range diffs {
		if d.Type == Insert && d.Text == "beautiful" {
			foundInsert = true
			break
		}
	}
	if !foundInsert {
		t.Error("Expected to find 'beautiful' as insertion")
	}
}

func TestDiffWordsDelete(t *testing.T) {
	diffs := DiffWords("the quick brown fox", "the fox")

	if len(diffs) < 2 {
		t.Error("Expected multiple diffs for word deletion")
	}
}

// ========== LevenshteinDistance Tests ==========

func TestLevenshteinDistanceIdentical(t *testing.T) {
	d := LevenshteinDistance("hello", "hello")
	if d != 0 {
		t.Errorf("Expected distance 0 for identical strings, got %d", d)
	}
}

func TestLevenshteinDistanceEmpty(t *testing.T) {
	d := LevenshteinDistance("", "hello")
	if d != 5 {
		t.Errorf("Expected distance 5 for empty->hello, got %d", d)
	}

	d = LevenshteinDistance("hello", "")
	if d != 5 {
		t.Errorf("Expected distance 5 for hello->empty, got %d", d)
	}
}

func TestLevenshteinDistanceKittenSitting(t *testing.T) {
	// Classic example
	d := LevenshteinDistance("kitten", "sitting")
	if d != 3 {
		t.Errorf("Expected distance 3 for kitten->sitting, got %d", d)
	}
}

func TestLevenshteinDistanceSubstitution(t *testing.T) {
	d := LevenshteinDistance("cat", "bat")
	if d != 1 {
		t.Errorf("Expected distance 1 for cat->bat, got %d", d)
	}
}

func TestLevenshteinDistanceUnicode(t *testing.T) {
	d := LevenshteinDistance("你好", "你坏")
	if d != 1 {
		t.Errorf("Expected distance 1 for Unicode substitution, got %d", d)
	}
}

// ========== Similarity Tests ==========

func TestSimilarityIdentical(t *testing.T) {
	s := Similarity("hello", "hello")
	if s != 1.0 {
		t.Errorf("Expected similarity 1.0 for identical strings, got %f", s)
	}
}

func TestSimilarityEmpty(t *testing.T) {
	s := Similarity("", "hello")
	if s != 0.0 {
		t.Errorf("Expected similarity 0.0 for empty string, got %f", s)
	}
}

func TestSimilarityPartial(t *testing.T) {
	s := Similarity("hello", "hallo")
	// One character different out of 5
	expected := 0.8
	if s < expected-0.01 || s > expected+0.01 {
		t.Errorf("Expected similarity ~%f, got %f", expected, s)
	}
}

func TestSimilarityCompletelyDifferent(t *testing.T) {
	s := Similarity("abc", "xyz")
	// All different
	if s > 0.5 {
		t.Errorf("Expected low similarity for completely different strings, got %f", s)
	}
}

// ========== LCS Tests ==========

func TestLCSIdentical(t *testing.T) {
	lcs, length := LCS("ABC", "ABC")
	if lcs != "ABC" {
		t.Errorf("Expected LCS 'ABC', got '%s'", lcs)
	}
	if length != 3 {
		t.Errorf("Expected length 3, got %d", length)
	}
}

func TestLCSEmpty(t *testing.T) {
	lcs, length := LCS("", "ABC")
	if length != 0 {
		t.Errorf("Expected length 0 for empty string, got %d", length)
	}
	if lcs != "" {
		t.Errorf("Expected empty LCS, got '%s'", lcs)
	}
}

func TestLCSClassic(t *testing.T) {
	lcs, length := LCS("ABCBDAB", "BDCABA")
	// Possible LCS: "BCBA" or "BDAB" with length 4
	if length != 4 {
		t.Errorf("Expected LCS length 4, got %d (lcs: '%s')", length, lcs)
	}
}

func TestLCSUnicode(t *testing.T) {
	lcs, length := LCS("你好世界", "你好中国")
	if length < 2 {
		t.Errorf("Expected LCS length >= 2, got %d (lcs: '%s')", length, lcs)
	}
	if !strings.Contains(lcs, "你好") {
		t.Errorf("Expected LCS to contain '你好', got '%s'", lcs)
	}
}

// ========== FormatUnified Tests ==========

func TestFormatUnifiedNoChanges(t *testing.T) {
	result := DiffLines("line1\nline2", "line1\nline2")
	uni := FormatUnified(result, 3, "a.txt", "b.txt")

	if !strings.Contains(uni, "--- a.txt") || !strings.Contains(uni, "+++ b.txt") {
		t.Error("Expected unified diff headers")
	}
}

func TestFormatUnifiedWithChanges(t *testing.T) {
	result := DiffLines("line1\nline2", "line1\nmodified")
	uni := FormatUnified(result, 3, "a.txt", "b.txt")

	if !strings.Contains(uni, "--- a.txt") {
		t.Error("Expected --- header")
	}
	if !strings.Contains(uni, "+++ b.txt") {
		t.Error("Expected +++ header")
	}
	if !strings.Contains(uni, "@@") {
		t.Error("Expected hunk header @@")
	}
}

// ========== FormatColor Tests ==========

func TestFormatColor(t *testing.T) {
	diffs := []Diff{
		{Type: Equal, Text: "same"},
		{Type: Delete, Text: "old"},
		{Type: Insert, Text: "new"},
	}
	result := FormatColor(diffs)

	if !strings.Contains(result, "same") {
		t.Error("Expected 'same' in output")
	}
	if !strings.Contains(result, "old") {
		t.Error("Expected 'old' in output")
	}
	if !strings.Contains(result, "new") {
		t.Error("Expected 'new' in output")
	}
	// Should contain ANSI codes
	if !strings.Contains(result, "\033[") {
		t.Error("Expected ANSI color codes in output")
	}
}

// ========== FormatHTML Tests ==========

func TestFormatHTML(t *testing.T) {
	diffs := []Diff{
		{Type: Equal, Text: "same"},
		{Type: Delete, Text: "old"},
		{Type: Insert, Text: "new"},
	}
	result := FormatHTML(diffs)

	if !strings.Contains(result, "<div") {
		t.Error("Expected div wrapper")
	}
	if !strings.Contains(result, "<del>old</del>") {
		t.Error("Expected <del> tag for deletion")
	}
	if !strings.Contains(result, "<ins>new</ins>") {
		t.Error("Expected <ins> tag for insertion")
	}
	if !strings.Contains(result, "<span>same</span>") {
		t.Error("Expected <span> tag for equal text")
	}
}

func TestFormatHTMLEscape(t *testing.T) {
	diffs := []Diff{
		{Type: Equal, Text: "<script>alert('xss')</script>"},
	}
	result := FormatHTML(diffs)

	if strings.Contains(result, "<script>") {
		t.Error("HTML should be escaped")
	}
	if !strings.Contains(result, "&lt;script&gt;") {
		t.Error("Expected escaped HTML entities")
	}
}

// ========== Edge Cases ==========

func TestDiffLinesTrailingNewline(t *testing.T) {
	a := "line1\nline2"
	b := "line1\nline2\n"

	result := DiffLines(a, b)

	// Trailing newline should result in an insertion
	if result.Stats.Added != 1 {
		t.Errorf("Expected 1 addition for trailing newline, got %d", result.Stats.Added)
	}
}

func TestDiffCharsEmoji(t *testing.T) {
	// Test with multi-byte Unicode characters
	diffs := DiffChars("hello 👋 world", "hello 🌍 world")

	foundDelete := false
	foundInsert := false
	for _, d := range diffs {
		if d.Type == Delete && strings.Contains(d.Text, "👋") {
			foundDelete = true
		}
		if d.Type == Insert && strings.Contains(d.Text, "🌍") {
			foundInsert = true
		}
	}

	if !foundDelete || !foundInsert {
		t.Error("Expected emoji substitution to be detected")
	}
}

func TestLargeDiff(t *testing.T) {
	// Test with larger inputs
	var a, b strings.Builder
	for i := 0; i < 1000; i++ {
		a.WriteString("line\n")
		if i%2 == 0 {
			b.WriteString("line\n")
		} else {
			b.WriteString("modified\n")
		}
	}

	result := DiffLines(a.String(), b.String())

	if result.Stats.Removed != 500 || result.Stats.Added != 500 {
		t.Errorf("Expected 500 modifications, got %d removed, %d added",
			result.Stats.Removed, result.Stats.Added)
	}
}

// ========== Benchmark ==========

func BenchmarkDiffLines(b *testing.B) {
	a := strings.Repeat("line\n", 1000)
	c := strings.Repeat("line\n", 1000)
	for i := 0; i < b.N; i++ {
		DiffLines(a, c)
	}
}

func BenchmarkLevenshteinDistance(b *testing.B) {
	a := strings.Repeat("a", 1000)
	c := strings.Repeat("b", 1000)
	for i := 0; i < b.N; i++ {
		LevenshteinDistance(a, c)
	}
}

func BenchmarkDiffChars(b *testing.B) {
	a := strings.Repeat("hello", 100)
	c := strings.Repeat("world", 100)
	for i := 0; i < b.N; i++ {
		DiffChars(a, c)
	}
}