package trie_utils

import (
	"sort"
	"testing"
)

// ============================================================================
// Trie Creation Tests
// ============================================================================

func TestNewTrie(t *testing.T) {
	trie := NewTrie()
	if trie == nil {
		t.Fatal("NewTrie returned nil")
	}
	if trie.Size() != 0 {
		t.Errorf("New trie should be empty, got size %d", trie.Size())
	}
	if !trie.IsEmpty() {
		t.Error("New trie should report as empty")
	}
	if !trie.caseSensitive {
		t.Error("NewTrie should be case-sensitive by default")
	}
}

func TestNewTrieCaseInsensitive(t *testing.T) {
	trie := NewTrieCaseInsensitive()
	if trie == nil {
		t.Fatal("NewTrieCaseInsensitive returned nil")
	}
	if trie.caseSensitive {
		t.Error("NewTrieCaseInsensitive should be case-insensitive")
	}
}

// ============================================================================
// Insert Tests
// ============================================================================

func TestInsert(t *testing.T) {
	trie := NewTrie()

	// Insert new word
	if !trie.Insert("hello") {
		t.Error("Insert of new word should return true")
	}
	if trie.Size() != 1 {
		t.Errorf("Expected size 1, got %d", trie.Size())
	}

	// Insert same word again
	if trie.Insert("hello") {
		t.Error("Insert of existing word should return false")
	}
	if trie.Size() != 1 {
		t.Errorf("Size should still be 1, got %d", trie.Size())
	}

	// Insert empty string
	if trie.Insert("") {
		t.Error("Insert of empty string should return false")
	}
}

func TestInsertCaseSensitive(t *testing.T) {
	trie := NewTrie()

	trie.Insert("hello")
	trie.Insert("Hello")
	trie.Insert("HELLO")

	if trie.Size() != 3 {
		t.Errorf("Expected 3 distinct words (case-sensitive), got %d", trie.Size())
	}

	if !trie.Search("hello") || !trie.Search("Hello") || !trie.Search("HELLO") {
		t.Error("All case variations should exist")
	}
}

func TestInsertCaseInsensitive(t *testing.T) {
	trie := NewTrieCaseInsensitive()

	trie.Insert("hello")
	trie.Insert("Hello")
	trie.Insert("HELLO")

	if trie.Size() != 1 {
		t.Errorf("Expected 1 word (case-insensitive), got %d", trie.Size())
	}

	if !trie.Search("hello") || !trie.Search("Hello") || !trie.Search("HELLO") {
		t.Error("All case variations should match")
	}
}

func TestInsertBatch(t *testing.T) {
	trie := NewTrie()
	words := []string{"apple", "app", "application", "apply", "banana"}

	inserted := trie.InsertBatch(words)
	if inserted != 5 {
		t.Errorf("Expected 5 insertions, got %d", inserted)
	}

	// Insert duplicates
	inserted = trie.InsertBatch(words)
	if inserted != 0 {
		t.Errorf("Expected 0 new insertions, got %d", inserted)
	}
}

// ============================================================================
// Search Tests
// ============================================================================

func TestSearch(t *testing.T) {
	trie := NewTrie()
	words := []string{"apple", "app", "application", "banana"}

	for _, w := range words {
		trie.Insert(w)
	}

	for _, w := range words {
		if !trie.Search(w) {
			t.Errorf("Should find word: %s", w)
		}
	}

	// Non-existent words
	if trie.Search("ap") {
		t.Error("'ap' should not exist as a word")
	}
	if trie.Search("applex") {
		t.Error("'applex' should not exist")
	}
	if trie.Search("") {
		t.Error("Empty string should not exist")
	}
}

func TestGetCount(t *testing.T) {
	trie := NewTrie()

	trie.Insert("hello")
	trie.Insert("hello")
	trie.Insert("hello")

	if count := trie.GetCount("hello"); count != 3 {
		t.Errorf("Expected count 3, got %d", count)
	}

	if count := trie.GetCount("world"); count != 0 {
		t.Errorf("Expected count 0 for non-existent word, got %d", count)
	}
}

// ============================================================================
// Prefix Tests
// ============================================================================

func TestStartsWith(t *testing.T) {
	trie := NewTrie()
	trie.InsertBatch([]string{"apple", "app", "application", "banana"})

	tests := []struct {
		prefix   string
		expected bool
	}{
		{"app", true},
		{"apple", true},
		{"ban", true},
		{"orange", false},
		{"x", false},
		{"", true}, // Empty prefix matches all
	}

	for _, tt := range tests {
		t.Run(tt.prefix, func(t *testing.T) {
			if result := trie.StartsWith(tt.prefix); result != tt.expected {
				t.Errorf("StartsWith(%q) = %v, want %v", tt.prefix, result, tt.expected)
			}
		})
	}
}

func TestLongestCommonPrefix(t *testing.T) {
	tests := []struct {
		name     string
		words    []string
		expected string
	}{
		{"common prefix", []string{"apple", "app", "application"}, "app"},
		{"no common prefix", []string{"cat", "dog", "bird"}, ""},
		{"single word", []string{"hello"}, "hello"},
		{"empty trie", []string{}, ""},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			trie := NewTrie()
			trie.InsertBatch(tt.words)

			if result := trie.LongestCommonPrefix(); result != tt.expected {
				t.Errorf("LongestCommonPrefix() = %q, want %q", result, tt.expected)
			}
		})
	}
}

func TestLongestPrefixOf(t *testing.T) {
	trie := NewTrie()
	trie.InsertBatch([]string{"app", "apple", "application"})

	tests := []struct {
		word     string
		expected string
	}{
		{"applepie", "apple"},
		{"application", "application"},
		{"appetite", "app"},
		{"banana", ""},
		{"", ""},
	}

	for _, tt := range tests {
		t.Run(tt.word, func(t *testing.T) {
			if result := trie.LongestPrefixOf(tt.word); result != tt.expected {
				t.Errorf("LongestPrefixOf(%q) = %q, want %q", tt.word, result, tt.expected)
			}
		})
	}
}

func TestCountPrefix(t *testing.T) {
	trie := NewTrie()
	trie.InsertBatch([]string{"apple", "app", "application", "apply", "banana"})

	tests := []struct {
		prefix   string
		expected int
	}{
		{"app", 4},
		{"apple", 1},
		{"ban", 1},
		{"xyz", 0},
		{"", 5},
	}

	for _, tt := range tests {
		t.Run(tt.prefix, func(t *testing.T) {
			if result := trie.CountPrefix(tt.prefix); result != tt.expected {
				t.Errorf("CountPrefix(%q) = %d, want %d", tt.prefix, result, tt.expected)
			}
		})
	}
}

// ============================================================================
// Delete Tests
// ============================================================================

func TestDelete(t *testing.T) {
	trie := NewTrie()
	trie.InsertBatch([]string{"apple", "app", "application"})

	// Delete existing word
	if !trie.Delete("app") {
		t.Error("Delete of existing word should return true")
	}
	if trie.Search("app") {
		t.Error("'app' should not exist after deletion")
	}
	if trie.Size() != 2 {
		t.Errorf("Size should be 2, got %d", trie.Size())
	}

	// Other words should still exist
	if !trie.Search("apple") || !trie.Search("application") {
		t.Error("'apple' and 'application' should still exist")
	}

	// Delete non-existent word
	if trie.Delete("xyz") {
		t.Error("Delete of non-existent word should return false")
	}

	// Delete empty string
	if trie.Delete("") {
		t.Error("Delete of empty string should return false")
	}
}

func TestDeleteCleanup(t *testing.T) {
	trie := NewTrie()
	trie.Insert("apple")
	trie.Insert("app")

	// Delete 'apple' should not delete 'app'
	trie.Delete("apple")
	if !trie.Search("app") {
		t.Error("'app' should still exist after deleting 'apple'")
	}
	if trie.StartsWith("appl") {
		t.Error("'appl' prefix should not exist after deleting 'apple'")
	}
}

// ============================================================================
// AutoComplete Tests
// ============================================================================

func TestAutoComplete(t *testing.T) {
	trie := NewTrie()
	trie.InsertBatch([]string{"apple", "app", "application", "apply", "banana", "band"})

	tests := []struct {
		name     string
		prefix   string
		expected []string
	}{
		{"app prefix", "app", []string{"app", "apple", "application", "apply"}},
		{"ban prefix", "ban", []string{"banana", "band"}},
		{"no matches", "xyz", []string{}},
		{"empty prefix", "", []string{"app", "apple", "application", "apply", "banana", "band"}},
		{"exact match", "apple", []string{"apple"}},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := trie.AutoComplete(tt.prefix)
			sort.Strings(tt.expected)
			if !equalSlices(result, tt.expected) {
				t.Errorf("AutoComplete(%q) = %v, want %v", tt.prefix, result, tt.expected)
			}
		})
	}
}

func TestAutoCompleteN(t *testing.T) {
	trie := NewTrie()
	trie.InsertBatch([]string{"apple", "app", "application", "apply"})

	result := trie.AutoCompleteN("app", 2)
	if len(result) != 2 {
		t.Errorf("Expected 2 results, got %d", len(result))
	}
}

func TestAutoCompleteByFrequency(t *testing.T) {
	trie := NewTrie()
	
	// Insert with different frequencies
	trie.Insert("apple")
	trie.Insert("apple")
	trie.Insert("apple")
	trie.Insert("app")
	trie.Insert("app")
	trie.Insert("application")

	result := trie.AutoCompleteByFrequency("app", 10)
	
	// 'apple' should be first (count=3), then 'app' (count=2), then 'application' (count=1)
	if len(result) < 3 {
		t.Fatalf("Expected at least 3 results, got %d", len(result))
	}
	if result[0] != "apple" {
		t.Errorf("Expected 'apple' first, got %q", result[0])
	}
	if result[1] != "app" {
		t.Errorf("Expected 'app' second, got %q", result[1])
	}
}

// ============================================================================
// Pattern Matching Tests
// ============================================================================

func TestMatchPattern(t *testing.T) {
	trie := NewTrie()
	trie.InsertBatch([]string{"cat", "bat", "rat", "car", "bar", "cart", "cats"})

	tests := []struct {
		name     string
		pattern  string
		expected []string
	}{
		{"single wildcard", "?at", []string{"bat", "cat", "rat"}},
		{"prefix wildcard", "c??", []string{"car", "cat"}},
		{"suffix wildcard", "ca?", []string{"car", "cat"}},
		{"star prefix", "*", []string{"bar", "bat", "car", "cart", "cat", "cats", "rat"}},
		{"star middle", "c*t", []string{"cat", "cart", "cats"}},
		{"no match", "z??", []string{}},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := trie.MatchPattern(tt.pattern)
			sort.Strings(tt.expected)
			if !equalSlices(result, tt.expected) {
				t.Errorf("MatchPattern(%q) = %v, want %v", tt.pattern, result, tt.expected)
			}
		})
	}
}

// ============================================================================
// Fuzzy Search Tests
// ============================================================================

func TestFuzzySearch(t *testing.T) {
	trie := NewTrie()
	trie.InsertBatch([]string{"hello", "help", "held", "helmet", "world", "word"})

	tests := []struct {
		name     string
		word     string
		distance int
	}{
		{"exact match", "hello", 0},
		{"one edit", "helio", 1},
		{"two edits", "hallo", 2},
		{"three edits", "hella", 1},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			results := trie.FuzzySearch(tt.word, tt.distance)
			// Verify all results are within the specified distance
			for _, r := range results {
				d := levenshteinDistance(tt.word, r)
				if d > tt.distance {
					t.Errorf("FuzzySearch returned %q with distance %d, max allowed %d", r, d, tt.distance)
				}
			}
		})
	}
}

// ============================================================================
// Statistics Tests
// ============================================================================

func TestGetStats(t *testing.T) {
	trie := NewTrie()
	trie.InsertBatch([]string{"a", "ab", "abc", "abcd"})

	stats := trie.GetStats()

	if stats.TotalWords != 4 {
		t.Errorf("Expected 4 words, got %d", stats.TotalWords)
	}
	if stats.TotalNodes < 4 {
		t.Errorf("Expected at least 4 nodes, got %d", stats.TotalNodes)
	}
	if stats.MaxDepth != 4 {
		t.Errorf("Expected max depth 4, got %d", stats.MaxDepth)
	}
}

func TestGetStatsEmpty(t *testing.T) {
	trie := NewTrie()
	stats := trie.GetStats()

	if stats.TotalWords != 0 {
		t.Errorf("Expected 0 words, got %d", stats.TotalWords)
	}
}

// ============================================================================
// Clear Tests
// ============================================================================

func TestClear(t *testing.T) {
	trie := NewTrie()
	trie.InsertBatch([]string{"apple", "banana", "cherry"})

	trie.Clear()

	if trie.Size() != 0 {
		t.Errorf("Size should be 0 after clear, got %d", trie.Size())
	}
	if !trie.IsEmpty() {
		t.Error("Trie should be empty after clear")
	}
	if trie.Search("apple") {
		t.Error("Should not find words after clear")
	}
}

// ============================================================================
// GetAllWords Tests
// ============================================================================

func TestGetAllWords(t *testing.T) {
	trie := NewTrie()
	words := []string{"delta", "alpha", "charlie", "bravo"}
	trie.InsertBatch(words)

	result := trie.GetAllWords()
	expected := []string{"alpha", "bravo", "charlie", "delta"}

	if !equalSlices(result, expected) {
		t.Errorf("GetAllWords() = %v, want %v", result, expected)
	}
}

// ============================================================================
// Helper Functions
// ============================================================================

func equalSlices(a, b []string) bool {
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

// ============================================================================
// Benchmarks
// ============================================================================

func BenchmarkInsert(b *testing.B) {
	trie := NewTrie()
	for i := 0; i < b.N; i++ {
		trie.Insert("benchmark_word")
		trie.Clear()
	}
}

func BenchmarkSearch(b *testing.B) {
	trie := NewTrie()
	trie.Insert("benchmark_word")
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		trie.Search("benchmark_word")
	}
}

func BenchmarkAutoComplete(b *testing.B) {
	trie := NewTrie()
	words := []string{"apple", "app", "application", "apply", "aptitude", "append"}
	trie.InsertBatch(words)
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		trie.AutoComplete("app")
	}
}

func BenchmarkFuzzySearch(b *testing.B) {
	trie := NewTrie()
	// Insert a larger set of words
	for i := 0; i < 1000; i++ {
		trie.Insert(generateWord(i))
	}
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		trie.FuzzySearch("test", 2)
	}
}

func generateWord(n int) string {
	const letters = "abcdefghijklmnopqrstuvwxyz"
	word := ""
	for i := 0; i < 5; i++ {
		word += string(letters[(n+i)%26])
	}
	return word
}