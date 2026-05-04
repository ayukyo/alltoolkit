package boyer_moore_utils

import (
	"testing"
)

func TestBasicFind(t *testing.T) {
	tests := []struct {
		pattern string
		text    string
		expect  int
	}{
		{"hello", "hello world", 0},
		{"world", "hello world", 6},
		{"abc", "ababababc", 6},
		{"xyz", "hello world", -1},
		{"", "hello", -1},
		{"hello", "", -1},
		{"a", "aaaaa", 0},
		{"aa", "aaaaa", 0},
		{"aaa", "aaaaa", 0},
	}

	for _, test := range tests {
		result := Find(test.pattern, test.text)
		if result != test.expect {
			t.Errorf("Find(%q, %q) = %d, expected %d", test.pattern, test.text, result, test.expect)
		}
	}
}

func TestFindAll(t *testing.T) {
	tests := []struct {
		pattern string
		text    string
		expect  []int
	}{
		{"ab", "abababab", []int{0, 2, 4, 6}},
		{"a", "aaaaa", []int{0, 1, 2, 3, 4}},
		{"xyz", "hello world", []int{}},
		{"test", "testtesttest", []int{0, 4, 8}},
		// Note: "aa" in "aaaaa" finds non-overlapping matches
		// Boyer-Moore shifts by pattern length after finding match
		{"aa", "aaaaa", []int{0, 2}}, // Non-overlapping
	}

	for _, test := range tests {
		result := FindAll(test.pattern, test.text)
		if !equalIntSlice(result, test.expect) {
			t.Errorf("FindAll(%q, %q) = %v, expected %v", test.pattern, test.text, result, test.expect)
		}
	}
}

func TestFindIgnoreCase(t *testing.T) {
	tests := []struct {
		pattern string
		text    string
		expect  int
	}{
		{"HELLO", "hello world", 0},
		{"Hello", "HELLO WORLD", 0},
		{"ABC", "abcabc", 0},
		{"XYZ", "hello world", -1},
	}

	for _, test := range tests {
		result := FindIgnoreCase(test.pattern, test.text)
		if result != test.expect {
			t.Errorf("FindIgnoreCase(%q, %q) = %d, expected %d", test.pattern, test.text, result, test.expect)
		}
	}
}

func TestFindAllIgnoreCase(t *testing.T) {
	tests := []struct {
		pattern string
		text    string
		expect  []int
	}{
		{"AB", "aBAbab", []int{0, 2, 4}},
		{"TEST", "testTESTTest", []int{0, 4, 8}},
	}

	for _, test := range tests {
		result := FindAllIgnoreCase(test.pattern, test.text)
		if !equalIntSlice(result, test.expect) {
			t.Errorf("FindAllIgnoreCase(%q, %q) = %v, expected %v", test.pattern, test.text, result, test.expect)
		}
	}
}

func TestCount(t *testing.T) {
	tests := []struct {
		pattern string
		text    string
		expect  int
	}{
		{"ab", "abababab", 4},
		{"a", "aaaaa", 5},
		{"xyz", "hello world", 0},
		{"test", "testtesttest", 3},
	}

	for _, test := range tests {
		result := Count(test.pattern, test.text)
		if result != test.expect {
			t.Errorf("Count(%q, %q) = %d, expected %d", test.pattern, test.text, result, test.expect)
		}
	}
}

func TestContains(t *testing.T) {
	tests := []struct {
		pattern string
		text    string
		expect  bool
	}{
		{"hello", "hello world", true},
		{"xyz", "hello world", false},
		{"world", "hello world", true},
	}

	for _, test := range tests {
		result := Contains(test.pattern, test.text)
		if result != test.expect {
			t.Errorf("Contains(%q, %q) = %v, expected %v", test.pattern, test.text, result, test.expect)
		}
	}
}

func TestReplace(t *testing.T) {
	tests := []struct {
		pattern     string
		text        string
		replacement string
		expect      string
	}{
		{"ab", "ababab", "xy", "xyxyxy"},
		{"hello", "hello world", "hi", "hi world"},
		{"xyz", "hello world", "abc", "hello world"},
		{"a", "aaa", "b", "bbb"},
	}

	for _, test := range tests {
		result := Replace(test.pattern, test.text, test.replacement)
		if result != test.expect {
			t.Errorf("Replace(%q, %q, %q) = %q, expected %q", test.pattern, test.text, test.replacement, result, test.expect)
		}
	}
}

func TestReplaceFirst(t *testing.T) {
	tests := []struct {
		pattern     string
		text        string
		replacement string
		expect      string
	}{
		{"ab", "ababab", "xy", "xyabab"},
		{"hello", "hello hello", "hi", "hi hello"},
		{"xyz", "hello world", "abc", "hello world"},
	}

	for _, test := range tests {
		result := ReplaceFirst(test.pattern, test.text, test.replacement)
		if result != test.expect {
			t.Errorf("ReplaceFirst(%q, %q, %q) = %q, expected %q", test.pattern, test.text, test.replacement, result, test.expect)
		}
	}
}

func TestBoyerMooreStruct(t *testing.T) {
	bm := New("pattern")
	
	if bm.GetPattern() != "pattern" {
		t.Errorf("GetPattern() = %q, expected %q", bm.GetPattern(), "pattern")
	}
	
	if bm.GetPatternLength() != 7 {
		t.Errorf("GetPatternLength() = %d, expected 7", bm.GetPatternLength())
	}
	
	if !bm.IsCaseSensitive() {
		t.Errorf("IsCaseSensitive() = false, expected true")
	}
	
	// Test case-insensitive
	bm2 := NewWithOptions("pattern", false)
	if bm2.IsCaseSensitive() {
		t.Errorf("IsCaseSensitive() = true, expected false")
	}
}

func TestFindLast(t *testing.T) {
	bm := New("ab")
	
	tests := []struct {
		text   string
		expect int
	}{
		{"ababab", 4},
		{"ab", 0},
		{"xyz", -1},
	}

	for _, test := range tests {
		result := bm.FindLast(test.text)
		if result != test.expect {
			t.Errorf("FindLast(%q) = %d, expected %d", test.text, result, test.expect)
		}
	}
}

func TestHorspool(t *testing.T) {
	tests := []struct {
		pattern string
		text    string
		expect  int
	}{
		{"hello", "hello world", 0},
		{"world", "hello world", 6},
		{"abc", "ababababc", 6},
		{"xyz", "hello world", -1},
	}

	for _, test := range tests {
		result := FindHorspool(test.pattern, test.text)
		if result != test.expect {
			t.Errorf("FindHorspool(%q, %q) = %d, expected %d", test.pattern, test.text, result, test.expect)
		}
	}
}

func TestHorspoolFindAll(t *testing.T) {
	h := NewHorspool("ab")
	result := h.FindAll("abababab")
	expect := []int{0, 2, 4, 6}
	
	if !equalIntSlice(result, expect) {
		t.Errorf("Horspool.FindAll() = %v, expected %v", result, expect)
	}
}

func TestTurboBoyerMoore(t *testing.T) {
	tbm := NewTurbo("pattern")
	
	tests := []struct {
		text   string
		expect int
	}{
		{"find the pattern here", 9},
		{"pattern", 0},
		{"no match here", -1},
	}

	for _, test := range tests {
		result := tbm.Find(test.text)
		if result != test.expect {
			t.Errorf("Turbo.Find(%q) = %d, expected %d", test.text, result, test.expect)
		}
	}
}

func TestFindMatches(t *testing.T) {
	matches := FindMatches("ab", "ababab")
	
	if len(matches) != 3 {
		t.Errorf("FindMatches returned %d matches, expected 3", len(matches))
	}
	
	// Check first match
	if matches[0].Position != 0 {
		t.Errorf("First match position = %d, expected 0", matches[0].Position)
	}
	
	if matches[0].Text != "ab" {
		t.Errorf("First match text = %q, expected %q", matches[0].Text, "ab")
	}
	
	if matches[0].EndPosition != 2 {
		t.Errorf("First match end position = %d, expected 2", matches[0].EndPosition)
	}
}

func TestMultiPattern(t *testing.T) {
	mp := NewMultiPattern("hello", "world", "test")
	
	// FindAny
	idx, pos := mp.FindAny("hello world")
	if idx != 0 || pos != 0 {
		t.Errorf("FindAny() = (%d, %d), expected (0, 0)", idx, pos)
	}
	
	// ContainsAny
	if !mp.ContainsAny("hello world") {
		t.Errorf("ContainsAny() = false, expected true")
	}
	
	if mp.ContainsAny("xyz") {
		t.Errorf("ContainsAny() = true for xyz, expected false")
	}
	
	// FindAll
	all := mp.FindAll("hello world hello")
	if len(all[0]) != 2 {
		t.Errorf("FindAll pattern 0 count = %d, expected 2", len(all[0]))
	}
}

func TestValidatePattern(t *testing.T) {
	if ValidatePattern("") != "pattern cannot be empty" {
		t.Errorf("ValidatePattern empty should fail")
	}
	
	if ValidatePattern("hello") != "" {
		t.Errorf("ValidatePattern('hello') should be valid")
	}
}

func TestAnalyzePattern(t *testing.T) {
	stats := AnalyzePattern("abba")
	
	if stats.Length != 4 {
		t.Errorf("Length = %d, expected 4", stats.Length)
	}
	
	if stats.UniqueChars != 2 {
		t.Errorf("UniqueChars = %d, expected 2", stats.UniqueChars)
	}
	
	if !stats.HasRepeated {
		t.Errorf("HasRepeated = false, expected true")
	}
	
	if !stats.IsPalindrome {
		t.Errorf("IsPalindrome = false, expected true for 'abba'")
	}
}

func TestPalindrome(t *testing.T) {
	palindromes := []string{"aba", "abba", "abcba", "a", ""}
	nonPalindromes := []string{"ab", "abc", "abcd"}
	
	for _, s := range palindromes {
		if !isPalindrome(s) {
			t.Errorf("%q should be palindrome", s)
		}
	}
	
	for _, s := range nonPalindromes {
		if isPalindrome(s) {
			t.Errorf("%q should not be palindrome", s)
		}
	}
}

func TestEdgeCases(t *testing.T) {
	// Empty pattern
	bm := New("")
	if bm.Find("text") != -1 {
		t.Errorf("Empty pattern should return -1")
	}
	
	// Empty text
	bm = New("pattern")
	if bm.Find("") != -1 {
		t.Errorf("Empty text should return -1")
	}
	
	// Pattern longer than text
	bm = New("longpattern")
	if bm.Find("short") != -1 {
		t.Errorf("Pattern longer than text should return -1")
	}
	
	// Single character
	bm = New("a")
	if bm.Find("abc") != 0 {
		t.Errorf("Single char find failed")
	}
}

func TestRepeatedPattern(t *testing.T) {
	// Pattern with repeated characters - non-overlapping matches
	bm := New("aa")
	
	result := bm.FindAll("aaaaa")
	// Boyer-Moore finds non-overlapping matches
	expect := []int{0, 2}
	
	if !equalIntSlice(result, expect) {
		t.Errorf("FindAll('aa', 'aaaaa') = %v, expected %v (non-overlapping)", result, expect)
	}
}

func TestChineseCharacters(t *testing.T) {
	bm := New("你好")
	
	text := "你好世界你好"
	result := bm.FindAll(text)
	
	if len(result) != 2 {
		t.Errorf("FindAll Chinese = %d matches, expected 2", len(result))
	}
	
	if result[0] != 0 {
		t.Errorf("First Chinese match position = %d, expected 0", result[0])
	}
}

func TestSpecialCharacters(t *testing.T) {
	tests := []struct {
		pattern string
		text    string
		expect  int
	}{
		{"$100", "Price is $100", 9},
		{"C++", "I love C++ programming", 7},
		{"@user", "Hello @user", 6},
		{"#tag", "This is #tag", 8},
	}

	for _, test := range tests {
		result := Find(test.pattern, test.text)
		if result != test.expect {
			t.Errorf("Find(%q, %q) = %d, expected %d", test.pattern, test.text, result, test.expect)
		}
	}
}

// Helper function
func equalIntSlice(a, b []int) bool {
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

// Benchmark tests
func BenchmarkFind(b *testing.B) {
	text := "This is a long text with many words and we need to find pattern somewhere in the middle pattern here"
	pattern := "pattern"
	
	for i := 0; i < b.N; i++ {
		Find(pattern, text)
	}
}

func BenchmarkFindAll(b *testing.B) {
	text := "abababababababababababababababab"
	pattern := "ab"
	
	for i := 0; i < b.N; i++ {
		FindAll(pattern, text)
	}
}

func BenchmarkHorspool(b *testing.B) {
	text := "This is a long text with many words and we need to find pattern somewhere in the middle pattern here"
	pattern := "pattern"
	
	for i := 0; i < b.N; i++ {
		FindHorspool(pattern, text)
	}
}

func BenchmarkTurbo(b *testing.B) {
	text := "This is a long text with many words and we need to find pattern somewhere in the middle pattern here"
	tbm := NewTurbo("pattern")
	
	for i := 0; i < b.N; i++ {
		tbm.Find(text)
	}
}