// Package wordle_utils provides utilities for Wordle game analysis and solving.
// Includes word filtering, letter frequency analysis, and optimal guess suggestions.
package wordle_utils

import (
	"sort"
	"strings"
	"unicode"
)

// Feedback represents the result of a guess against the target word.
type Feedback int

const (
	Absent  Feedback = iota // Letter not in word (gray)
	Present                 // Letter in word but wrong position (yellow)
	Correct                 // Letter in correct position (green)
)

// GuessResult represents the feedback for a single guess.
type GuessResult struct {
	Word     string
	Feedback []Feedback // Length matches word length
}

// WordleSolver provides utilities for solving Wordle puzzles.
type WordleSolver struct {
	wordList     []string
	wordLength   int
	possibleWords []string
	guessHistory []GuessResult
}

// NewWordleSolver creates a new solver with the given word list.
func NewWordleSolver(wordList []string, wordLength int) *WordleSolver {
	filtered := make([]string, 0)
	for _, word := range wordList {
		if len(word) == wordLength {
			filtered = append(filtered, strings.ToLower(word))
		}
	}
	return &WordleSolver{
		wordList:      filtered,
		wordLength:    wordLength,
		possibleWords: filtered,
		guessHistory:  make([]GuessResult, 0),
	}
}

// FilterWords filters the possible words based on guess feedback.
func (ws *WordleSolver) FilterWords(guess string, feedback []Feedback) []string {
	ws.guessHistory = append(ws.guessHistory, GuessResult{
		Word:     strings.ToLower(guess),
		Feedback: feedback,
	})

	filtered := make([]string, 0)
	for _, word := range ws.possibleWords {
		if ws.matchesFeedback(word, strings.ToLower(guess), feedback) {
			filtered = append(filtered, word)
		}
	}
	ws.possibleWords = filtered
	return filtered
}

// matchesFeedback checks if a candidate word matches the feedback pattern.
func (ws *WordleSolver) matchesFeedback(candidate, guess string, feedback []Feedback) bool {
	if len(candidate) != len(guess) || len(feedback) != len(guess) {
		return false
	}

	// Count letters that are Present but not Correct
	lettersInWord := make(map[rune]int)
	lettersCorrect := make(map[rune]int)

	for i, f := range feedback {
		letter := rune(guess[i])
		if f == Correct {
			lettersCorrect[letter]++
		}
	}

	for i, f := range feedback {
		letter := rune(guess[i])
		if f == Present {
			lettersInWord[letter]++
		}
	}

	// Check each position
	for i, f := range feedback {
		candidateLetter := rune(candidate[i])
		guessLetter := rune(guess[i])

		switch f {
		case Correct:
			if candidateLetter != guessLetter {
				return false
			}
		case Present:
			if candidateLetter == guessLetter {
				return false // Letter is in wrong position, can't be here
			}
		case Absent:
			// Letter should not appear in word, unless it appears elsewhere as Correct/Present
			countInCandidate := strings.Count(candidate, string(guessLetter))
			required := lettersCorrect[guessLetter] + lettersInWord[guessLetter]
			if countInCandidate > required {
				return false
			}
		}
	}

	// Check that all Present letters appear somewhere
	for letter, count := range lettersInWord {
		candidateCount := strings.Count(candidate, string(letter))
		correctCount := lettersCorrect[letter]
		if candidateCount < count+correctCount {
			return false
		}
	}

	return true
}

// GetPossibleWords returns the current list of possible words.
func (ws *WordleSolver) GetPossibleWords() []string {
	return ws.possibleWords
}

// Reset clears all guess history and resets possible words.
func (ws *WordleSolver) Reset() {
	ws.possibleWords = ws.wordList
	ws.guessHistory = make([]GuessResult, 0)
}

// LetterFrequency calculates letter frequency across all possible words.
func (ws *WordleSolver) LetterFrequency() map[rune]float64 {
	freq := make(map[rune]int)
	total := 0

	for _, word := range ws.possibleWords {
		seen := make(map[rune]bool)
		for _, letter := range word {
			if !seen[letter] {
				freq[letter]++
				seen[letter] = true
				total++
			}
		}
	}

	result := make(map[rune]float64)
	for letter, count := range freq {
		result[letter] = float64(count) / float64(total)
	}
	return result
}

// PositionFrequency calculates letter frequency at each position.
func (ws *WordleSolver) PositionFrequency() []map[rune]float64 {
	result := make([]map[rune]float64, ws.wordLength)
	for i := range result {
		result[i] = make(map[rune]float64)
	}

	if len(ws.possibleWords) == 0 {
		return result
	}

	for _, word := range ws.possibleWords {
		for i, letter := range word {
			result[i][letter]++
		}
	}

	for i := range result {
		for letter := range result[i] {
			result[i][letter] = result[i][letter] / float64(len(ws.possibleWords))
		}
	}

	return result
}

// ScoreWord scores a word based on letter frequency and position.
func (ws *WordleSolver) ScoreWord(word string) float64 {
	freq := ws.LetterFrequency()
	posFreq := ws.PositionFrequency()

	score := 0.0
	seen := make(map[rune]bool)

	for i, letter := range word {
		// Bonus for unique letters
		if !seen[letter] {
			score += freq[letter] * 10
			seen[letter] = true
		}
		// Bonus for position frequency
		if i < len(posFreq) {
			score += posFreq[i][letter] * 5
		}
	}

	return score
}

// SuggestGuess suggests the best guess based on scoring.
func (ws *WordleSolver) SuggestGuess() string {
	if len(ws.possibleWords) == 0 {
		return ""
	}

	bestWord := ws.possibleWords[0]
	bestScore := ws.ScoreWord(bestWord)

	for _, word := range ws.possibleWords[1:] {
		score := ws.ScoreWord(word)
		if score > bestScore {
			bestScore = score
			bestWord = word
		}
	}

	return bestWord
}

// SuggestGuessFromAll suggests best guess from entire word list (not just possible).
func (ws *WordleSolver) SuggestGuessFromAll() string {
	bestWord := ws.wordList[0]
	bestScore := ws.ScoreWord(bestWord)

	for _, word := range ws.wordList[1:] {
		score := ws.ScoreWord(word)
		if score > bestScore {
			bestScore = score
			bestWord = word
		}
	}

	return bestWord
}

// TopSuggestions returns the top N suggested guesses.
func (ws *WordleSolver) TopSuggestions(n int) []string {
	type wordScore struct {
		word  string
		score float64
	}

	scores := make([]wordScore, 0, len(ws.possibleWords))
	for _, word := range ws.possibleWords {
		scores = append(scores, wordScore{word, ws.ScoreWord(word)})
	}

	sort.Slice(scores, func(i, j int) bool {
		return scores[i].score > scores[j].score
	})

	result := make([]string, 0, n)
	for i := 0; i < n && i < len(scores); i++ {
		result = append(result, scores[i].word)
	}
	return result
}

// CheckGuess validates a guess against a target word and returns feedback.
func CheckGuess(guess, target string) []Feedback {
	guess = strings.ToLower(guess)
	target = strings.ToLower(target)

	if len(guess) != len(target) {
		return nil
	}

	feedback := make([]Feedback, len(guess))
	targetLetters := make(map[rune]int)

	// Count letters in target
	for _, letter := range target {
		targetLetters[letter]++
	}

	// First pass: mark correct
	for i, letter := range guess {
		if letter == rune(target[i]) {
			feedback[i] = Correct
			targetLetters[letter]--
		}
	}

	// Second pass: mark present or absent
	for i, letter := range guess {
		if feedback[i] == Correct {
			continue
		}
		if targetLetters[letter] > 0 {
			feedback[i] = Present
			targetLetters[letter]--
		} else {
			feedback[i] = Absent
		}
	}

	return feedback
}

// FeedbackToString converts feedback to a readable string.
func FeedbackToString(feedback []Feedback) string {
	var sb strings.Builder
	for _, f := range feedback {
		switch f {
		case Correct:
			sb.WriteString("🟩")
		case Present:
			sb.WriteString("🟨")
		case Absent:
			sb.WriteString("⬜")
		}
	}
	return sb.String()
}

// FeedbackFromString parses a feedback string into Feedback slice.
// Format: G/g = green (correct), Y/y = yellow (present), X/x/? = gray (absent)
func FeedbackFromString(s string) []Feedback {
	feedback := make([]Feedback, 0)
	for _, c := range s {
		switch unicode.ToUpper(c) {
		case 'G':
			feedback = append(feedback, Correct)
		case 'Y':
			feedback = append(feedback, Present)
		default:
			feedback = append(feedback, Absent)
		}
	}
	return feedback
}

// IsWinningFeedback checks if all feedback is Correct.
func IsWinningFeedback(feedback []Feedback) bool {
	for _, f := range feedback {
		if f != Correct {
			return false
		}
	}
	return true
}

// CommonLetters returns the most common letters in possible words.
func (ws *WordleSolver) CommonLetters(n int) []rune {
	freq := ws.LetterFrequency()

	type letterFreq struct {
		letter rune
		freq   float64
	}

	letters := make([]letterFreq, 0, 26)
	for r := 'a'; r <= 'z'; r++ {
		letters = append(letters, letterFreq{r, freq[r]})
	}

	sort.Slice(letters, func(i, j int) bool {
		return letters[i].freq > letters[j].freq
	})

	result := make([]rune, 0, n)
	for i := 0; i < n && i < len(letters); i++ {
		if letters[i].freq > 0 {
			result = append(result, letters[i].letter)
		}
	}
	return result
}

// WordsContaining returns all possible words containing the given letter.
func (ws *WordleSolver) WordsContaining(letter rune) []string {
	result := make([]string, 0)
	for _, word := range ws.possibleWords {
		if strings.ContainsRune(word, letter) {
			result = append(result, word)
		}
	}
	return result
}

// WordsWithPattern returns words matching a pattern (use '_' for unknown).
func (ws *WordleSolver) WordsWithPattern(pattern string) []string {
	result := make([]string, 0)
	pattern = strings.ToLower(pattern)

	for _, word := range ws.possibleWords {
		if matchesPattern(word, pattern) {
			result = append(result, word)
		}
	}
	return result
}

func matchesPattern(word, pattern string) bool {
	if len(word) != len(pattern) {
		return false
	}
	for i, c := range pattern {
		if c != '_' && c != rune(word[i]) {
			return false
		}
	}
	return true
}

// Statistics returns solver statistics.
func (ws *WordleSolver) Statistics() map[string]interface{} {
	return map[string]interface{}{
		"total_words":      len(ws.wordList),
		"possible_words":   len(ws.possibleWords),
		"word_length":      ws.wordLength,
		"guesses_made":     len(ws.guessHistory),
		"remaining_words":  len(ws.possibleWords),
		"top_letters":      ws.CommonLetters(5),
		"best_guess":       ws.SuggestGuess(),
	}
}

// DefaultWordList returns a sample 5-letter word list for testing.
func DefaultWordList() []string {
	return []string{
		"about", "above", "abuse", "actor", "acute", "admit", "adopt", "adult",
		"after", "again", "agent", "agree", "ahead", "alarm", "album", "alert",
		"alike", "alive", "allow", "alone", "along", "alter", "among", "anger",
		"angle", "angry", "apart", "apple", "apply", "arena", "argue", "arise",
		"array", "aside", "asset", "avoid", "award", "aware", "badly", "baker",
		"bases", "basic", "basis", "beach", "began", "begin", "begun", "being",
		"below", "bench", "billy", "birth", "black", "blame", "blind", "block",
		"blood", "board", "boost", "booth", "bound", "brain", "brand", "bread",
		"break", "breed", "brief", "bring", "broad", "broke", "brown", "build",
		"built", "buyer", "cable", "carry", "catch", "cause", "chain", "chair",
		"chart", "chase", "cheap", "check", "chest", "chief", "child", "china",
		"chose", "civil", "claim", "class", "clean", "clear", "click", "clock",
		"close", "coach", "coast", "could", "count", "court", "cover", "craft",
		"crash", "cream", "crime", "cross", "crowd", "crown", "curve", "cycle",
		"daily", "dance", "dated", "dealt", "death", "debut", "delay", "depth",
		"doing", "doubt", "dozen", "draft", "drama", "drank", "drawn", "dream",
		"dress", "drink", "drive", "drove", "dying", "early", "earth", "eight",
		"elite", "empty", "enemy", "enjoy", "enter", "entry", "equal", "error",
		"event", "every", "exact", "exist", "extra", "faith", "false", "fault",
		"fiber", "field", "fifth", "fifty", "fight", "final", "first", "fixed",
		"flash", "fleet", "floor", "fluid", "focus", "force", "forth", "found",
		"frame", "frank", "fraud", "fresh", "front", "fruit", "fully", "funny",
		"giant", "given", "glass", "globe", "going", "grace", "grade", "grand",
		"grant", "grass", "great", "green", "gross", "group", "grown", "guard",
		"guess", "guest", "guide", "happy", "harry", "heart", "heavy", "hence",
		"horse", "hotel", "house", "human", "ideal", "image", "index", "inner",
		"input", "issue", "japan", "joint", "judge", "juice", "known", "label",
		"large", "laser", "later", "laugh", "layer", "learn", "lease", "least",
		"leave", "legal", "level", "light", "limit", "links", "lives", "local",
		"logic", "loose", "lower", "lucky", "lunch", "lying", "magic", "major",
		"maker", "march", "match", "maybe", "mayor", "meant", "media", "metal",
		"might", "minor", "minus", "mixed", "model", "money", "month", "moral",
		"motor", "mount", "mouse", "mouth", "movie", "music", "needs", "never",
		"newly", "night", "noise", "north", "noted", "novel", "nurse", "occur",
		"ocean", "offer", "often", "order", "other", "ought", "outer", "owner",
		"paint", "panel", "paper", "party", "peace", "phase", "phone", "photo",
		"piece", "pilot", "pitch", "place", "plain", "plane", "plant", "plate",
		"point", "pound", "power", "press", "price", "pride", "prime", "print",
		"prior", "prize", "proof", "proud", "prove", "queen", "quick", "quiet",
		"quite", "radio", "raise", "range", "rapid", "ratio", "reach", "ready",
		"refer", "right", "rival", "river", "roman", "rough", "round", "route",
		"royal", "rural", "saint", "sales", "scale", "scene", "scope", "score",
		"sense", "serve", "seven", "shall", "shape", "share", "sharp", "sheet",
		"shelf", "shell", "shift", "shirt", "shock", "shoot", "short", "shown",
		"sight", "since", "sized", "skill", "sleep", "slide", "small", "smart",
		"smile", "smoke", "solid", "solve", "sorry", "sound", "south", "space",
		"spare", "speak", "speed", "spend", "spent", "split", "spoke", "sport",
		"staff", "stage", "stake", "stand", "start", "state", "steam", "steel",
		"steep", "stick", "still", "stock", "stone", "stood", "store", "storm",
		"story", "strip", "stuck", "study", "stuff", "style", "sugar", "suite",
		"super", "sweet", "swing", "taken", "taste", "teach", "teeth", "thank",
		"theft", "their", "theme", "there", "these", "thick", "thing", "think",
		"third", "those", "three", "threw", "throw", "tight", "tired", "title",
		"today", "token", "topic", "total", "touch", "tough", "tower", "track",
		"trade", "trail", "train", "trash", "treat", "trend", "trial", "tribe",
		"trick", "tried", "truck", "truly", "trust", "truth", "twice", "under",
		"undue", "union", "unity", "until", "upper", "upset", "urban", "usage",
		"usual", "valid", "value", "video", "virus", "visit", "vital", "vocal",
		"voice", "waste", "watch", "water", "waved", "wheel", "where", "which",
		"while", "white", "whole", "whose", "width", "woman", "works", "world",
		"worry", "worse", "worst", "worth", "would", "wound", "write", "wrong",
		"wrote", "yield", "young", "youth", "crane", "crate", "slate", "stare",
		"blame", "flame", "shame", "share", "snare", "spare", "scare", "apple",
		"fable", "maple", "rifle", "title", "uncle", "aisle", "table", "gable",
		"haste", "paste", "waste", "ghost", "cloud", "train", "lucky", "bread",
		"peppy", "label", "speed", "eerie", "later", "angle", "alone", "aloft",
		"brake", "alert", "arise", "speed", "dream", "flame", "grape", "house",
		"juice", "cloud", "world", "smart", "great", "about", "pound", "found",
	}
}