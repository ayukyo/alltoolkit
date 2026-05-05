package wordle_utils

import (
	"strings"
	"testing"
)

// Helper function to create test solver
func newTestSolver() *WordleSolver {
	return NewWordleSolver(DefaultWordList(), 5)
}

// TestNewWordleSolver tests solver initialization
func TestNewWordleSolver(t *testing.T) {
	words := []string{"apple", "bread", "crane", "dream", "eager", "flame"}
	solver := NewWordleSolver(words, 5)

	if solver.wordLength != 5 {
		t.Errorf("Expected wordLength 5, got %d", solver.wordLength)
	}

	if len(solver.possibleWords) != 6 {
		t.Errorf("Expected 6 possible words, got %d", len(solver.possibleWords))
	}

	if len(solver.wordList) != 6 {
		t.Errorf("Expected 6 words in wordList, got %d", len(solver.wordList))
	}
}

// TestNewWordleSolverFiltersByLength tests that solver filters words by length
func TestNewWordleSolverFiltersByLength(t *testing.T) {
	words := []string{"apple", "pie", "crane", "hi", "dream", "testing"}
	solver := NewWordleSolver(words, 5)

	if len(solver.wordList) != 3 {
		t.Errorf("Expected 3 words (5-letter only), got %d", len(solver.wordList))
	}
}

// TestCheckGuess tests the CheckGuess function
func TestCheckGuess(t *testing.T) {
	tests := []struct {
		name     string
		guess    string
		target   string
		expected []Feedback
	}{
		{
			name:     "all correct",
			guess:    "apple",
			target:   "apple",
			expected: []Feedback{Correct, Correct, Correct, Correct, Correct},
		},
		{
			name:     "all absent",
			guess:    "xyzzy",
			target:   "apple",
			expected: []Feedback{Absent, Absent, Absent, Absent, Absent},
		},
		{
			name:     "mix of correct and absent",
			guess:    "apric",
			target:   "apple",
			expected: []Feedback{Correct, Correct, Absent, Absent, Absent},
		},
		{
			name:     "all present different positions",
			guess:    "leapp",
			target:   "apple",
			expected: []Feedback{Present, Present, Present, Present, Present},
		},
		{
			name:     "double letter in target",
			guess:    "speed",
			target:   "eerie",
			expected: []Feedback{Absent, Absent, Present, Present, Absent},
		},
		{
			name:     "case insensitive",
			guess:    "APPLE",
			target:   "apple",
			expected: []Feedback{Correct, Correct, Correct, Correct, Correct},
		},
		{
			name:     "one correct others absent",
			guess:    "crane",
			target:   "cloud",
			expected: []Feedback{Correct, Absent, Absent, Absent, Absent},
		},
		{
			name:     "one correct from multiple",
			guess:    "eerie",
			target:   "peppy",
			expected: []Feedback{Absent, Correct, Absent, Absent, Absent},
		},
		{
			name:     "one correct two present",
			guess:    "llama",
			target:   "label",
			expected: []Feedback{Correct, Present, Present, Absent, Absent},
		},
		{
			name:     "one correct one present",
			guess:    "apple",
			target:   "peppy",
			expected: []Feedback{Absent, Present, Correct, Absent, Present},
		},
		{
			name:     "two present first two",
			guess:    "eerie",
			target:   "speed",
			expected: []Feedback{Present, Present, Absent, Absent, Absent},
		},
		{
			name:     "one present one correct",
			guess:    "speed",
			target:   "peppy",
			expected: []Feedback{Absent, Present, Present, Absent, Absent},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := CheckGuess(tt.guess, tt.target)
			if len(result) != len(tt.expected) {
				t.Errorf("Expected %d feedback items, got %d", len(tt.expected), len(result))
				return
			}
			for i, f := range result {
				if f != tt.expected[i] {
					t.Errorf("Position %d: expected %v, got %v", i, tt.expected[i], f)
				}
			}
		})
	}
}

// TestCheckGuessDifferentLengths tests CheckGuess with mismatched lengths
func TestCheckGuessDifferentLengths(t *testing.T) {
	result := CheckGuess("app", "apple")
	if result != nil {
		t.Errorf("Expected nil for mismatched lengths, got %v", result)
	}
}

// TestFilterWords tests word filtering based on feedback
func TestFilterWords(t *testing.T) {
	solver := newTestSolver()

	// Guess "crane" and get all correct for "crane"
	filtered := solver.FilterWords("crane", []Feedback{Correct, Correct, Correct, Correct, Correct})

	if len(filtered) != 1 {
		t.Errorf("Expected 1 word after exact match, got %d", len(filtered))
	}
	if len(filtered) > 0 && filtered[0] != "crane" {
		t.Errorf("Expected 'crane', got '%s'", filtered[0])
	}
}

// TestFilterWordsWithPresent tests filtering with present letters
func TestFilterWordsWithPresent(t *testing.T) {
	words := []string{"apple", "apply", "aloft", "brake", "crane"}
	solver := NewWordleSolver(words, 5)

	// 'a' is present but not at position 0
	filtered := solver.FilterWords("alert", []Feedback{Present, Absent, Absent, Absent, Absent})

	for _, word := range filtered {
		if word[0] == 'a' {
			t.Errorf("Word '%s' should not have 'a' at position 0", word)
		}
		if !strings.ContainsRune(word, 'a') {
			t.Errorf("Word '%s' should contain 'a'", word)
		}
	}
}

// TestFilterWordsWithAbsent tests filtering with absent letters
func TestFilterWordsWithAbsent(t *testing.T) {
	words := []string{"apple", "bread", "crane", "dream", "flame"}
	solver := NewWordleSolver(words, 5)

	// 'z' is absent - no words contain 'z' so all should remain
	filtered := solver.FilterWords("zzzzz", []Feedback{Absent, Absent, Absent, Absent, Absent})

	// All words should remain since none contain 'z'
	if len(filtered) != len(words) {
		t.Errorf("Expected %d words (none contain 'z'), got %d", len(words), len(filtered))
	}
}

// TestFilterWordsWithRealAbsent tests filtering when letter actually exists in some words
func TestFilterWordsWithRealAbsent(t *testing.T) {
	words := []string{"apple", "bread", "crane", "dream", "flame"}
	solver := NewWordleSolver(words, 5)

	// 'p' is absent - only "apple" contains 'p'
	filtered := solver.FilterWords("ppppp", []Feedback{Absent, Absent, Absent, Absent, Absent})

	// Should filter out "apple"
	if len(filtered) != 4 {
		t.Errorf("Expected 4 words (apple removed), got %d", len(filtered))
	}

	for _, word := range filtered {
		if word == "apple" {
			t.Error("'apple' should have been filtered out")
		}
	}
}

// TestLetterFrequency tests letter frequency calculation
func TestLetterFrequency(t *testing.T) {
	words := []string{"apple", "bread", "crane"}
	solver := NewWordleSolver(words, 5)

	freq := solver.LetterFrequency()

	// 'a' appears in all 3 words
	if freq['a'] == 0 {
		t.Error("Expected non-zero frequency for 'a'")
	}

	// 'z' does not appear
	if freq['z'] != 0 {
		t.Error("Expected zero frequency for 'z'")
	}
}

// TestPositionFrequency tests position frequency calculation
func TestPositionFrequency(t *testing.T) {
	words := []string{"apple", "apric", "alone"}
	solver := NewWordleSolver(words, 5)

	posFreq := solver.PositionFrequency()

	// 'a' should have high frequency at position 0
	if posFreq[0]['a'] == 0 {
		t.Error("Expected 'a' to have non-zero frequency at position 0")
	}
}

// TestScoreWord tests word scoring
func TestScoreWord(t *testing.T) {
	solver := newTestSolver()

	score := solver.ScoreWord("crane")
	if score <= 0 {
		t.Errorf("Expected positive score for 'crane', got %f", score)
	}
}

// TestSuggestGuess tests guess suggestion
func TestSuggestGuess(t *testing.T) {
	solver := newTestSolver()

	guess := solver.SuggestGuess()
	if guess == "" {
		t.Error("Expected non-empty guess suggestion")
	}

	if len(guess) != 5 {
		t.Errorf("Expected 5-letter word, got '%s' (length %d)", guess, len(guess))
	}
}

// TestSuggestGuessFromAll tests suggestion from entire word list
func TestSuggestGuessFromAll(t *testing.T) {
	solver := newTestSolver()

	// Filter to reduce possibilities
	solver.FilterWords("arise", []Feedback{Absent, Present, Absent, Present, Absent})

	guess := solver.SuggestGuessFromAll()
	if guess == "" {
		t.Error("Expected non-empty guess from all words")
	}
}

// TestTopSuggestions tests top N suggestions
func TestTopSuggestions(t *testing.T) {
	solver := newTestSolver()

	suggestions := solver.TopSuggestions(5)
	if len(suggestions) != 5 {
		t.Errorf("Expected 5 suggestions, got %d", len(suggestions))
	}

	// Check all suggestions are valid 5-letter words
	for _, word := range suggestions {
		if len(word) != 5 {
			t.Errorf("Invalid suggestion '%s' (length %d)", word, len(word))
		}
	}
}

// TestTopSuggestionsMoreThanAvailable tests requesting more suggestions than available
func TestTopSuggestionsMoreThanAvailable(t *testing.T) {
	words := []string{"apple", "bread"}
	solver := NewWordleSolver(words, 5)

	suggestions := solver.TopSuggestions(10)
	if len(suggestions) != 2 {
		t.Errorf("Expected 2 suggestions (only 2 available), got %d", len(suggestions))
	}
}

// TestFeedbackToString tests feedback to string conversion
func TestFeedbackToString(t *testing.T) {
	tests := []struct {
		feedback []Feedback
		expected string
	}{
		{
			feedback: []Feedback{Correct, Present, Absent},
			expected: "🟩🟨⬜",
		},
		{
			feedback: []Feedback{Correct, Correct, Correct, Correct, Correct},
			expected: "🟩🟩🟩🟩🟩",
		},
		{
			feedback: []Feedback{Absent, Absent, Absent},
			expected: "⬜⬜⬜",
		},
	}

	for _, tt := range tests {
		result := FeedbackToString(tt.feedback)
		if result != tt.expected {
			t.Errorf("Expected '%s', got '%s'", tt.expected, result)
		}
	}
}

// TestFeedbackFromString tests string to feedback conversion
func TestFeedbackFromString(t *testing.T) {
	tests := []struct {
		input    string
		expected []Feedback
	}{
		{
			input:    "GYX",
			expected: []Feedback{Correct, Present, Absent},
		},
		{
			input:    "ggggg",
			expected: []Feedback{Correct, Correct, Correct, Correct, Correct},
		},
		{
			input:    "?????",
			expected: []Feedback{Absent, Absent, Absent, Absent, Absent},
		},
		{
			input:    "GyXgY",
			expected: []Feedback{Correct, Present, Absent, Correct, Present},
		},
	}

	for _, tt := range tests {
		result := FeedbackFromString(tt.input)
		for i, f := range result {
			if f != tt.expected[i] {
				t.Errorf("Position %d: expected %v, got %v", i, tt.expected[i], f)
			}
		}
	}
}

// TestIsWinningFeedback tests winning feedback detection
func TestIsWinningFeedback(t *testing.T) {
	if !IsWinningFeedback([]Feedback{Correct, Correct, Correct, Correct, Correct}) {
		t.Error("Expected all correct to be winning")
	}

	if IsWinningFeedback([]Feedback{Correct, Present, Correct, Correct, Correct}) {
		t.Error("Expected not winning with present")
	}

	if IsWinningFeedback([]Feedback{Absent, Absent, Absent}) {
		t.Error("Expected not winning with absent")
	}
}

// TestCommonLetters tests common letter extraction
func TestCommonLetters(t *testing.T) {
	solver := newTestSolver()

	common := solver.CommonLetters(5)
	if len(common) > 5 {
		t.Errorf("Expected at most 5 letters, got %d", len(common))
	}

	// Common letters should be non-empty for a good word list
	if len(common) == 0 {
		t.Error("Expected some common letters")
	}
}

// TestWordsContaining tests finding words with a specific letter
func TestWordsContaining(t *testing.T) {
	solver := newTestSolver()

	words := solver.WordsContaining('a')
	for _, word := range words {
		if !strings.ContainsRune(word, 'a') {
			t.Errorf("Word '%s' does not contain 'a'", word)
		}
	}
}

// TestWordsWithPattern tests pattern matching
func TestWordsWithPattern(t *testing.T) {
	solver := newTestSolver()

	words := solver.WordsWithPattern("a____")
	for _, word := range words {
		if word[0] != 'a' {
			t.Errorf("Word '%s' does not match pattern 'a____'", word)
		}
	}
}

// TestWordsWithPatternPartial tests partial pattern matching
func TestWordsWithPatternPartial(t *testing.T) {
	solver := newTestSolver()

	words := solver.WordsWithPattern("_pp__")
	for _, word := range words {
		if word[1] != 'p' || word[2] != 'p' {
			t.Errorf("Word '%s' does not match pattern '_pp__'", word)
		}
	}
}

// TestStatistics tests statistics output
func TestStatistics(t *testing.T) {
	solver := newTestSolver()

	stats := solver.Statistics()

	if stats["word_length"] != 5 {
		t.Errorf("Expected word_length 5, got %v", stats["word_length"])
	}

	if stats["guesses_made"] != 0 {
		t.Errorf("Expected 0 guesses_made, got %v", stats["guesses_made"])
	}

	totalWords, ok := stats["total_words"].(int)
	if !ok || totalWords <= 0 {
		t.Errorf("Expected positive total_words, got %v", stats["total_words"])
	}
}

// TestReset tests solver reset
func TestReset(t *testing.T) {
	solver := newTestSolver()

	originalCount := len(solver.possibleWords)

	// Make a guess
	solver.FilterWords("crane", []Feedback{Absent, Absent, Absent, Absent, Absent})
	filteredCount := len(solver.possibleWords)

	// Reset
	solver.Reset()

	if len(solver.possibleWords) != originalCount {
		t.Errorf("Expected %d possible words after reset, got %d", originalCount, len(solver.possibleWords))
	}

	if len(solver.guessHistory) != 0 {
		t.Error("Expected guess history to be cleared")
	}

	// Verify filtering actually happened
	if filteredCount >= originalCount {
		t.Error("Filtering should have reduced possibilities")
	}
}

// TestMultipleFilters tests multiple consecutive filters
func TestMultipleFilters(t *testing.T) {
	solver := newTestSolver()

	// First guess
	solver.FilterWords("arise", []Feedback{Absent, Present, Absent, Present, Absent})
	count1 := len(solver.possibleWords)

	// Second guess
	solver.FilterWords("crane", []Feedback{Absent, Correct, Present, Absent, Absent})
	count2 := len(solver.possibleWords)

	// Should be reducing possibilities
	if count2 > count1 {
		t.Errorf("Expected reducing possibilities: %d -> %d", count1, count2)
	}
}

// TestEmptyWordList tests handling empty word list
func TestEmptyWordList(t *testing.T) {
	solver := NewWordleSolver([]string{}, 5)

	guess := solver.SuggestGuess()
	if guess != "" {
		t.Errorf("Expected empty guess for empty word list, got '%s'", guess)
	}

	freq := solver.LetterFrequency()
	if len(freq) != 0 {
		t.Error("Expected empty frequency map for empty word list")
	}
}

// TestNoPossibleWords tests handling when all words are filtered out
func TestNoPossibleWords(t *testing.T) {
	words := []string{"apple"}
	solver := NewWordleSolver(words, 5)

	// Filter with contradictory feedback
	solver.FilterWords("zzzzz", []Feedback{Correct, Correct, Correct, Correct, Correct})

	// Should have no possible words
	if len(solver.possibleWords) != 0 {
		t.Errorf("Expected 0 possible words, got %d", len(solver.possibleWords))
	}

	guess := solver.SuggestGuess()
	if guess != "" {
		t.Errorf("Expected empty guess, got '%s'", guess)
	}
}

// TestDoubleLetterFeedback tests correct handling of double letters
func TestDoubleLetterFeedback(t *testing.T) {
	tests := []struct {
		name     string
		guess    string
		target   string
		expected []Feedback
	}{
		{
			name:     "double letter one correct one present",
			guess:    "llama",
			target:   "label",
			expected: []Feedback{Correct, Present, Present, Absent, Absent},
		},
		{
			name:     "double letter in guess single in target",
			guess:    "apple",
			target:   "peppy",
			expected: []Feedback{Absent, Present, Correct, Absent, Present},
		},
		{
			name:     "triple letter in guess",
			guess:    "eerie",
			target:   "speed",
			expected: []Feedback{Present, Present, Absent, Absent, Absent},
		},
		{
			name:     "single letter correct double in target",
			guess:    "speed",
			target:   "peppy",
			expected: []Feedback{Absent, Present, Present, Absent, Absent},
		},
		{
			name:     "double e in target",
			guess:    "speed",
			target:   "eerie",
			expected: []Feedback{Absent, Absent, Present, Present, Absent},
		},
		{
			name:     "triple e in guess",
			guess:    "eerie",
			target:   "peppy",
			expected: []Feedback{Absent, Correct, Absent, Absent, Absent},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := CheckGuess(tt.guess, tt.target)
			for i, f := range result {
				if f != tt.expected[i] {
					t.Errorf("Position %d: expected %v, got %v", i, tt.expected[i], f)
				}
			}
		})
	}
}

// TestDefaultWordList tests the default word list
func TestDefaultWordList(t *testing.T) {
	words := DefaultWordList()

	if len(words) == 0 {
		t.Fatal("Default word list is empty")
	}

	// All words should be 5 letters
	for _, word := range words {
		if len(word) != 5 {
			t.Errorf("Word '%s' is not 5 letters", word)
		}
	}

	// All words should be lowercase
	for _, word := range words {
		if word != strings.ToLower(word) {
			t.Errorf("Word '%s' is not lowercase", word)
		}
	}
}

// TestGetPossibleWords tests getting current possible words
func TestGetPossibleWords(t *testing.T) {
	solver := newTestSolver()

	words := solver.GetPossibleWords()
	if len(words) == 0 {
		t.Error("Expected non-empty possible words")
	}

	// Make a guess
	solver.FilterWords("arise", []Feedback{Absent, Absent, Absent, Absent, Absent})

	// Should have different set now
	newWords := solver.GetPossibleWords()
	if len(newWords) >= len(words) {
		t.Error("Expected reduced word list after filtering")
	}
}

// TestBoundaryConditions tests edge cases
func TestBoundaryConditions(t *testing.T) {
	t.Run("empty pattern", func(t *testing.T) {
		solver := newTestSolver()
		words := solver.WordsWithPattern("")
		// Empty pattern matches nothing
		if len(words) != 0 {
			t.Errorf("Expected 0 words for empty pattern, got %d", len(words))
		}
	})

	t.Run("single word list", func(t *testing.T) {
		solver := NewWordleSolver([]string{"apple"}, 5)
		guess := solver.SuggestGuess()
		if guess != "apple" {
			t.Errorf("Expected 'apple', got '%s'", guess)
		}
	})

	t.Run("all same letter", func(t *testing.T) {
		words := []string{"aaaaa", "bbbbb", "ccccc"}
		solver := NewWordleSolver(words, 5)

		common := solver.CommonLetters(10)
		// Should only return letters that exist
		if len(common) > 3 {
			t.Errorf("Expected at most 3 common letters, got %d", len(common))
		}
	})
}

// TestMatchesFeedback tests the internal matching logic
func TestMatchesFeedback(t *testing.T) {
	tests := []struct {
		name      string
		candidate string
		guess     string
		feedback  []Feedback
		expected  bool
	}{
		{
			name:      "exact match",
			candidate: "apple",
			guess:     "apple",
			feedback:  []Feedback{Correct, Correct, Correct, Correct, Correct},
			expected:  true,
		},
		{
			name:      "absent letter filters correctly",
			candidate: "bread",
			guess:     "zippy",
			feedback:  []Feedback{Absent, Absent, Absent, Absent, Absent},
			expected:  true, // 'z', 'i', 'p', 'y' not in 'bread'
		},
		{
			name:      "absent letter filters out candidate",
			candidate: "alone",
			guess:     "apple",
			feedback:  []Feedback{Absent, Present, Absent, Absent, Absent},
			expected:  false, // 'a' is Absent but 'alone' has 'a'
		},
		{
			name:      "present at same position fails",
			candidate: "apple",
			guess:     "arise",
			feedback:  []Feedback{Absent, Present, Absent, Absent, Absent},
			expected:  false, // 'r' is at position 1 in both, but should be Present (wrong position)
		},
		{
			name:      "correct position match",
			candidate: "crane",
			guess:     "cloud",
			feedback:  []Feedback{Correct, Absent, Absent, Absent, Absent},
			expected:  true, // 'c' is at position 0 in both
		},
		{
			name:      "correct position mismatch",
			candidate: "arise",
			guess:     "cloud",
			feedback:  []Feedback{Correct, Absent, Absent, Absent, Absent},
			expected:  false, // 'c' is not at position 0 in 'arise'
		},
		{
			name:      "present without letter fails",
			candidate: "bread",
			guess:     "apple",
			feedback:  []Feedback{Absent, Present, Absent, Absent, Absent},
			expected:  false, // 'p' is Present but 'bread' has no 'p'
		},
		{
			name:      "present with letter but absent filters",
			candidate: "crane",
			guess:     "apple",
			feedback:  []Feedback{Absent, Present, Absent, Absent, Absent},
			expected:  false, // 'p' is Present, but 'a' is Absent and 'crane' has 'a'
		},
		{
			name:      "present matches with custom word",
			candidate: "pkunk",
			guess:     "apple",
			feedback:  []Feedback{Absent, Present, Absent, Absent, Absent},
			expected:  true, // 'p' is Present at pos 1, 'pkunk' has 'p' at pos 0, no 'a','l','e'
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			solver := NewWordleSolver([]string{tt.candidate}, 5)
			result := solver.matchesFeedback(tt.candidate, tt.guess, tt.feedback)
			if result != tt.expected {
				t.Errorf("Expected %v, got %v", tt.expected, result)
			}
		})
	}
}