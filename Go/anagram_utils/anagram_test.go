package anagram_utils

import (
	"reflect"
	"sort"
	"testing"
)

func TestIsAnagram(t *testing.T) {
	tests := []struct {
		name     string
		s1       string
		s2       string
		expected bool
	}{
		{"simple anagram", "listen", "silent", true},
		{"different lengths", "hello", "hi", false},
		{"same word", "test", "test", true},
		{"case insensitive", "Listen", "Silent", true},
		{"with spaces", "dormitory", "dirty room", true},
		{"with punctuation", "eleven plus two", "twelve plus one", true},
		{"not anagram", "hello", "world", false},
		{"empty strings", "", "", true},
		{"single char", "a", "a", true},
		{"unicode", "café", "face", false}, // café has 'c','a','f','é' but face has 'f','a','c','e' - different letters
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := IsAnagram(tt.s1, tt.s2)
			if result != tt.expected {
				t.Errorf("IsAnagram(%q, %q) = %v, want %v", tt.s1, tt.s2, result, tt.expected)
			}
		})
	}
}

func TestIsAnagramStrict(t *testing.T) {
	tests := []struct {
		name     string
		s1       string
		s2       string
		expected bool
	}{
		{"exact match", "abc", "cba", true},
		{"case sensitive", "Abc", "cba", false},
		{"with spaces", "a b c", "cba", false},
		{"same case", "TEST", "ESTT", true},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := IsAnagramStrict(tt.s1, tt.s2)
			if result != tt.expected {
				t.Errorf("IsAnagramStrict(%q, %q) = %v, want %v", tt.s1, tt.s2, result, tt.expected)
			}
		})
	}
}

func TestGetSignature(t *testing.T) {
	tests := []struct {
		name     string
		input    string
		expected string
	}{
		{"simple", "cab", "abc"},
		{"uppercase", "CAB", "abc"},
		{"mixed", "bAc", "abc"},
		{"with numbers", "a1b2c3", "abc"},
		{"empty", "", ""},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := GetSignature(tt.input)
			if result != tt.expected {
				t.Errorf("GetSignature(%q) = %q, want %q", tt.input, result, tt.expected)
			}
		})
	}
}

func TestFindAnagrams(t *testing.T) {
	wordList := []string{"listen", "silent", "enlist", "inlets", "hello", "world", "tinsel"}

	tests := []struct {
		name     string
		word     string
		expected []string
	}{
		{"listen anagrams", "listen", []string{"silent", "enlist", "inlets", "tinsel"}},
		{"no anagrams", "hello", nil},
		{"case insensitive", "SILENT", []string{"listen", "enlist", "inlets", "tinsel"}},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := FindAnagrams(tt.word, wordList)
			sort.Strings(result)
			if tt.expected != nil {
				sort.Strings(tt.expected)
			}
			// Handle nil vs empty slice comparison
			if len(result) == 0 && len(tt.expected) == 0 {
				return // Both empty, test passes
			}
			if !reflect.DeepEqual(result, tt.expected) {
				t.Errorf("FindAnagrams(%q) = %v, want %v", tt.word, result, tt.expected)
			}
		})
	}
}

func TestGroupAnagrams(t *testing.T) {
	words := []string{"listen", "silent", "hello", "world", "enlist", "act", "cat", "tac"}
	groups := GroupAnagrams(words)

	// Check that anagrams are grouped together
	listenSig := GetSignature("listen")
	if len(groups[listenSig]) != 3 {
		t.Errorf("Expected 3 anagrams for 'listen', got %d", len(groups[listenSig]))
	}

	actSig := GetSignature("act")
	if len(groups[actSig]) != 3 {
		t.Errorf("Expected 3 anagrams for 'act', got %d", len(groups[actSig]))
	}
}

func TestGenerateAnagrams(t *testing.T) {
	tests := []struct {
		name         string
		input        string
		minExpected  int
		exactMatches []string
	}{
		{"two letters", "ab", 2, []string{"ab", "ba"}},
		{"three letters", "abc", 6, []string{"abc", "acb", "bac", "bca", "cab", "cba"}},
		{"with duplicates", "aa", 1, []string{"aa"}},
		{"empty", "", 0, nil},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := GenerateAnagrams(tt.input)
			if len(result) < tt.minExpected {
				t.Errorf("GenerateAnagrams(%q) returned %d results, want at least %d",
					tt.input, len(result), tt.minExpected)
			}
			for _, match := range tt.exactMatches {
				found := false
				for _, r := range result {
					if r == match {
						found = true
						break
					}
				}
				if !found {
					t.Errorf("GenerateAnagrams(%q) missing %q", tt.input, match)
				}
			}
		})
	}
}

func TestGenerateAnagramsLimit(t *testing.T) {
	// Test that limit works
	result := GenerateAnagramsLimit("abcde", 10)
	if len(result) > 10 {
		t.Errorf("GenerateAnagramsLimit returned %d results, expected at most 10", len(result))
	}

	// Test with small limit
	result = GenerateAnagramsLimit("abc", 5)
	if len(result) > 5 {
		t.Errorf("GenerateAnagramsLimit returned %d results, expected at most 5", len(result))
	}

	// Test with zero limit
	result = GenerateAnagramsLimit("abc", 0)
	if len(result) != 0 {
		t.Errorf("GenerateAnagramsLimit with limit 0 returned %d results", len(result))
	}
}

func TestCountAnagrams(t *testing.T) {
	tests := []struct {
		name     string
		input    string
		expected int
	}{
		{"unique letters", "abc", 6},          // 3! = 6
		{"two same letters", "aab", 3},        // 3!/2! = 3
		{"all same letters", "aaa", 1},       // 3!/3! = 1
		{"single letter", "a", 1},             // 1! = 1
		{"empty", "", 0},                      // 0
		{"four unique", "abcd", 24},           // 4! = 24
		{"two pairs", "aabb", 6},              // 4!/(2!*2!) = 6
		{"one triple", "aaab", 4},             // 4!/3! = 4
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := CountAnagrams(tt.input)
			if result != tt.expected {
				t.Errorf("CountAnagrams(%q) = %d, want %d", tt.input, result, tt.expected)
			}
		})
	}
}

func TestIsValidAnagram(t *testing.T) {
	tests := []struct {
		name     string
		source   string
		candidate string
		expected bool
	}{
		{"valid anagram", "listen", "silent", true},
		{"same word", "test", "test", false},
		{"same word different case", "Test", "TEST", false},
		{"not anagram", "hello", "world", false},
		{"valid with spaces", "dormitory", "dirty room", true},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := IsValidAnagram(tt.source, tt.candidate)
			if result != tt.expected {
				t.Errorf("IsValidAnagram(%q, %q) = %v, want %v",
					tt.source, tt.candidate, result, tt.expected)
			}
		})
	}
}

func TestGetLetterFrequency(t *testing.T) {
	tests := []struct {
		name     string
		input    string
		expected map[rune]int
	}{
		{"simple", "hello", map[rune]int{'h': 1, 'e': 1, 'l': 2, 'o': 1}},
		{"with duplicates", "aabbcc", map[rune]int{'a': 2, 'b': 2, 'c': 2}},
		{"mixed case", "AaBb", map[rune]int{'a': 2, 'b': 2}},
		{"empty", "", map[rune]int{}},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := GetLetterFrequency(tt.input)
			if !reflect.DeepEqual(result, tt.expected) {
				t.Errorf("GetLetterFrequency(%q) = %v, want %v", tt.input, result, tt.expected)
			}
		})
	}
}

func TestHasSameLetters(t *testing.T) {
	tests := []struct {
		name     string
		s1       string
		s2       string
		expected bool
	}{
		{"same letters", "abc", "cba", true},
		{"different letters", "abc", "abd", false},
		{"different counts", "aabc", "abc", false},
		{"with spaces", "a b c", "abc", true},
		{"case insensitive", "ABC", "abc", true},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := HasSameLetters(tt.s1, tt.s2)
			if result != tt.expected {
				t.Errorf("HasSameLetters(%q, %q) = %v, want %v",
					tt.s1, tt.s2, result, tt.expected)
			}
		})
	}
}

func TestRemoveLetter(t *testing.T) {
	tests := []struct {
		name     string
		input    string
		letter   rune
		expected string
	}{
		{"remove first", "hello", 'h', "ello"},
		{"remove middle", "hello", 'l', "helo"},
		{"remove last", "hello", 'o', "hell"},
		{"letter not found", "hello", 'z', "hello"},
		{"case insensitive", "Hello", 'h', "ello"},
		{"empty string", "", 'a', ""},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := RemoveLetter(tt.input, tt.letter)
			if result != tt.expected {
				t.Errorf("RemoveLetter(%q, %q) = %q, want %q",
					tt.input, tt.letter, result, tt.expected)
			}
		})
	}
}

func TestCanFormWord(t *testing.T) {
	tests := []struct {
		name            string
		availableLetters string
		word            string
		expected        bool
	}{
		{"can form", "abcdef", "bed", true},
		{"cannot form - missing letter", "abcdef", "bedg", false},
		{"cannot form - not enough letters", "abc", "aabb", false},
		{"exact match", "abc", "abc", true},
		{"with extra", "aabbcc", "abc", true},
		{"empty word", "abc", "", true},
		{"empty available", "", "a", false},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := CanFormWord(tt.availableLetters, tt.word)
			if result != tt.expected {
				t.Errorf("CanFormWord(%q, %q) = %v, want %v",
					tt.availableLetters, tt.word, result, tt.expected)
			}
		})
	}
}

func TestFindPossibleWords(t *testing.T) {
	wordList := []string{"cat", "act", "tac", "bat", "tab", "cab", "dog"}
	available := "tacb"

	result := FindPossibleWords(available, wordList)
	expected := []string{"cat", "act", "tac", "bat", "tab", "cab"}

	sort.Strings(result)
	sort.Strings(expected)

	if !reflect.DeepEqual(result, expected) {
		t.Errorf("FindPossibleWords(%q, ...) = %v, want %v", available, result, expected)
	}
}

func TestLongestAnagram(t *testing.T) {
	wordList := []string{"a", "at", "act", "cat", "tact", "tactic"}
	available := "cttacti"

	result := LongestAnagram(available, wordList)
	if len(result) < 5 { // Should find at least "tactic" (6 letters)
		t.Errorf("LongestAnagram returned %q (len %d), expected longer word", result, len(result))
	}
}

func TestScrabbleScore(t *testing.T) {
	tests := []struct {
		name     string
		word     string
		expected int
	}{
		{"simple", "cat", 5},        // c(3) + a(1) + t(1) = 5
		{"high value", "quiz", 22},  // q(10) + u(1) + i(1) + z(10) = 22
		{"all ones", "aeiou", 5},    // all 1s
		{"empty", "", 0},
		{"case insensitive", "QUIZ", 22},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := ScrabbleScore(tt.word)
			if result != tt.expected {
				t.Errorf("ScrabbleScore(%q) = %d, want %d", tt.word, result, tt.expected)
			}
		})
	}
}

func TestHighestScoringWord(t *testing.T) {
	wordList := []string{"cat", "dog", "quiz", "act", "zip"}
	available := "quizactopg"

	result := HighestScoringWord(available, wordList)
	// "quiz" = 22, "zip" = 14, "dog" = 5, "cat" = 5, "act" = 5
	if result != "quiz" {
		t.Errorf("HighestScoringWord returned %q, want 'quiz'", result)
	}
}

func TestNormalize(t *testing.T) {
	tests := []struct {
		name     string
		input    string
		expected string
	}{
		{"lowercase", "HELLO", "hello"},
		{"remove numbers", "he11o", "heo"},
		{"remove punctuation", "h.e.l.l.o", "hello"},
		{"remove spaces", "h e l l o", "hello"},
		{"mixed", "HeLLo 123 World!", "helloworld"},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := normalize(tt.input)
			if result != tt.expected {
				t.Errorf("normalize(%q) = %q, want %q", tt.input, result, tt.expected)
			}
		})
	}
}

func TestSortString(t *testing.T) {
	tests := []struct {
		name     string
		input    string
		expected string
	}{
		{"simple", "cba", "abc"},
		{"already sorted", "abc", "abc"},
		{"duplicates", "cbaa", "aabc"},
		{"empty", "", ""},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := sortString(tt.input)
			if result != tt.expected {
				t.Errorf("sortString(%q) = %q, want %q", tt.input, result, tt.expected)
			}
		})
	}
}

func TestFactorial(t *testing.T) {
	tests := []struct {
		n        int
		expected int
	}{
		{0, 1},
		{1, 1},
		{2, 2},
		{3, 6},
		{4, 24},
		{5, 120},
		{10, 3628800},
	}

	for _, tt := range tests {
		result := factorial(tt.n)
		if result != tt.expected {
			t.Errorf("factorial(%d) = %d, want %d", tt.n, result, tt.expected)
		}
	}
}

// Benchmark tests
func BenchmarkIsAnagram(b *testing.B) {
	for i := 0; i < b.N; i++ {
		IsAnagram("dormitory", "dirty room")
	}
}

func BenchmarkGenerateAnagrams(b *testing.B) {
	for i := 0; i < b.N; i++ {
		GenerateAnagrams("abcdefg")
	}
}

func BenchmarkGroupAnagrams(b *testing.B) {
	words := []string{"listen", "silent", "hello", "world", "enlist", "act", "cat"}
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		GroupAnagrams(words)
	}
}

func BenchmarkFindAnagrams(b *testing.B) {
	wordList := []string{"listen", "silent", "enlist", "inlets", "hello", "world", "tinsel"}
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		FindAnagrams("listen", wordList)
	}
}