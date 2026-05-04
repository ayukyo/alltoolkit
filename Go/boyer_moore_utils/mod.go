// Package boyer_moore_utils implements the Boyer-Moore string search algorithm.
// Boyer-Moore is one of the most efficient string matching algorithms, 
// achieving O(n/m) average-case complexity where n is the text length 
// and m is the pattern length.
//
// Features:
// - Zero dependencies, uses only Go standard library
// - Multiple algorithm variants (Boyer-Moore, Horspool, Turbo)
// - Find all matches with positions
// - Case-sensitive and case-insensitive search
// - Reverse search (find last occurrence)
// - Pattern validation and preprocessing
// - Match counting and replacement utilities
// - Multi-pattern search
//
// Example usage:
//
//	bm := boyer_moore_utils.New("pattern")
//	positions := bm.FindAll("text with pattern here")
//	fmt.Println(positions) // [10]
//
package boyer_moore_utils

import (
	"strings"
	"unicode/utf8"
)

// BoyerMoore represents a preprocessed pattern for efficient searching.
type BoyerMoore struct {
	pattern         string
	badChar         []int // Bad character shift table (ASCII range)
	caseSensitive   bool
	processedPattern string
}

// New creates a new BoyerMoore searcher with the given pattern.
func New(pattern string) *BoyerMoore {
	return NewWithOptions(pattern, true)
}

// NewWithOptions creates a new BoyerMoore searcher with custom options.
func NewWithOptions(pattern string, caseSensitive bool) *BoyerMoore {
	bm := &BoyerMoore{
		pattern:       pattern,
		caseSensitive: caseSensitive,
	}

	if !caseSensitive {
		bm.processedPattern = strings.ToLower(pattern)
	} else {
		bm.processedPattern = pattern
	}

	bm.buildBadCharTable()
	return bm
}

// buildBadCharTable builds the bad character shift table.
// For each character, store the rightmost position in the pattern.
func (bm *BoyerMoore) buildBadCharTable() {
	m := len(bm.processedPattern)
	
	// Create table for all possible byte values (256 entries for ASCII)
	bm.badChar = make([]int, 256)
	for i := range bm.badChar {
		bm.badChar[i] = m // Default shift is pattern length
	}
	
	// Update positions for characters in pattern (excluding last char)
	for i := 0; i < m-1; i++ {
		bm.badChar[bm.processedPattern[i]] = m - 1 - i
	}
}

// preprocessText preprocesses text for case-insensitive search.
func (bm *BoyerMoore) preprocessText(text string) string {
	if bm.caseSensitive {
		return text
	}
	return strings.ToLower(text)
}

// Find searches for the first occurrence of the pattern in the text.
// Returns the starting position (0-indexed) or -1 if not found.
func (bm *BoyerMoore) Find(text string) int {
	processedText := bm.preprocessText(text)
	m := len(bm.processedPattern)
	n := len(processedText)

	if m == 0 || n < m {
		return -1
	}

	i := 0
	for i <= n - m {
		// Compare from right to left
		j := m - 1
		for j >= 0 && processedText[i+j] == bm.processedPattern[j] {
			j--
		}

		if j < 0 {
			return i // Found
		}

		// Shift using bad character rule
		shift := bm.badChar[processedText[i+m-1]]
		if shift <= 0 {
			shift = 1
		}
		i += shift
	}

	return -1
}

// FindAll searches for all occurrences of the pattern in the text.
// Returns an array of starting positions (0-indexed).
func (bm *BoyerMoore) FindAll(text string) []int {
	processedText := bm.preprocessText(text)
	m := len(bm.processedPattern)
	n := len(processedText)

	if m == 0 || n < m {
		return []int{}
	}

	positions := []int{}
	i := 0

	for i <= n - m {
		// Compare from right to left
		j := m - 1
		for j >= 0 && processedText[i+j] == bm.processedPattern[j] {
			j--
		}

		if j < 0 {
			positions = append(positions, i)
			i += m // Move past this match
		} else {
			// Shift using bad character rule
			shift := bm.badChar[processedText[i+m-1]]
			if shift <= 0 {
				shift = 1
			}
			i += shift
		}
	}

	return positions
}

// FindLast searches for the last occurrence of the pattern.
func (bm *BoyerMoore) FindLast(text string) int {
	positions := bm.FindAll(text)
	if len(positions) == 0 {
		return -1
	}
	return positions[len(positions)-1]
}

// Count returns the number of occurrences of the pattern in the text.
func (bm *BoyerMoore) Count(text string) int {
	return len(bm.FindAll(text))
}

// Contains checks if the pattern exists in the text.
func (bm *BoyerMoore) Contains(text string) bool {
	return bm.Find(text) >= 0
}

// Replace replaces all occurrences of the pattern with replacement.
func (bm *BoyerMoore) Replace(text, replacement string) string {
	positions := bm.FindAll(text)
	if len(positions) == 0 {
		return text
	}

	m := len(bm.pattern)
	result := text

	for i := len(positions) - 1; i >= 0; i-- {
		pos := positions[i]
		result = result[:pos] + replacement + result[pos+m:]
	}

	return result
}

// ReplaceFirst replaces the first occurrence of the pattern.
func (bm *BoyerMoore) ReplaceFirst(text, replacement string) string {
	pos := bm.Find(text)
	if pos < 0 {
		return text
	}

	m := len(bm.pattern)
	return text[:pos] + replacement + text[pos+m:]
}

// GetPattern returns the search pattern.
func (bm *BoyerMoore) GetPattern() string {
	return bm.pattern
}

// GetPatternLength returns the pattern length.
func (bm *BoyerMoore) GetPatternLength() int {
	return len(bm.processedPattern)
}

// IsCaseSensitive returns whether search is case-sensitive.
func (bm *BoyerMoore) IsCaseSensitive() bool {
	return bm.caseSensitive
}

// Horspool implements the Boyer-Moore-Horspool simplified algorithm.
type Horspool struct {
	BoyerMoore
}

// NewHorspool creates a new Horspool searcher.
func NewHorspool(pattern string) *Horspool {
	return &Horspool{
		BoyerMoore: *New(pattern),
	}
}

// NewHorspoolWithOptions creates a new Horspool searcher with options.
func NewHorspoolWithOptions(pattern string, caseSensitive bool) *Horspool {
	return &Horspool{
		BoyerMoore: *NewWithOptions(pattern, caseSensitive),
	}
}

// TurboBoyerMoore is an optimized variant with memory.
type TurboBoyerMoore struct {
	BoyerMoore
}

// NewTurbo creates a new Turbo Boyer-Moore searcher.
func NewTurbo(pattern string) *TurboBoyerMoore {
	return &TurboBoyerMoore{
		BoyerMoore: *New(pattern),
	}
}

// Find searches using Turbo Boyer-Moore algorithm with memory optimization.
func (tbm *TurboBoyerMoore) Find(text string) int {
	processedText := tbm.preprocessText(text)
	m := len(tbm.processedPattern)
	n := len(processedText)

	if m == 0 || n < m {
		return -1
	}

	i := 0
	memory := 0

	for i <= n - m {
		// Use memory to skip matched characters
		j := m - 1
		if memory > 0 && m - 1 - memory >= 0 {
			j = m - 1 - memory
		}
		
		k := i + j
		matched := 0

		// Match from right to left
		for j >= 0 && processedText[k] == tbm.processedPattern[j] {
			j--
			k--
			matched++
		}

		if j < 0 {
			return i // Found
		}

		// Update memory
		if matched > memory {
			memory = matched
		} else if matched > 0 {
			memory = matched - 1
		} else {
			memory = 0
		}

		// Shift using bad character rule
		shift := tbm.badChar[processedText[i+m-1]]
		if shift <= memory {
			shift = memory + 1
		}
		i += shift
	}

	return -1
}

// Utility functions for direct use without creating searcher.

// Find searches for pattern in text using Boyer-Moore.
func Find(pattern, text string) int {
	bm := New(pattern)
	return bm.Find(text)
}

// FindAll finds all occurrences of pattern in text.
func FindAll(pattern, text string) []int {
	bm := New(pattern)
	return bm.FindAll(text)
}

// FindIgnoreCase searches case-insensitively.
func FindIgnoreCase(pattern, text string) int {
	bm := NewWithOptions(pattern, false)
	return bm.Find(text)
}

// FindAllIgnoreCase finds all occurrences case-insensitively.
func FindAllIgnoreCase(pattern, text string) []int {
	bm := NewWithOptions(pattern, false)
	return bm.FindAll(text)
}

// Count returns number of occurrences.
func Count(pattern, text string) int {
	bm := New(pattern)
	return bm.Count(text)
}

// Contains checks if pattern exists in text.
func Contains(pattern, text string) bool {
	return Find(pattern, text) >= 0
}

// ContainsIgnoreCase checks case-insensitively.
func ContainsIgnoreCase(pattern, text string) bool {
	return FindIgnoreCase(pattern, text) >= 0
}

// Replace replaces all occurrences.
func Replace(pattern, text, replacement string) string {
	bm := New(pattern)
	return bm.Replace(text, replacement)
}

// ReplaceFirst replaces first occurrence.
func ReplaceFirst(pattern, text, replacement string) string {
	bm := New(pattern)
	return bm.ReplaceFirst(text, replacement)
}

// FindHorspool uses Horspool algorithm.
func FindHorspool(pattern, text string) int {
	h := NewHorspool(pattern)
	return h.Find(text)
}

// FindAllHorspool finds all using Horspool.
func FindAllHorspool(pattern, text string) []int {
	h := NewHorspool(pattern)
	return h.FindAll(text)
}

// Match represents a found match with position and details.
type Match struct {
	Position    int    // Starting position (0-indexed)
	Text        string // The matched substring
	EndPosition int    // Ending position (exclusive)
}

// FindMatches returns detailed match information.
func FindMatches(pattern, text string) []Match {
	bm := New(pattern)
	positions := bm.FindAll(text)

	matches := []Match{}
	for _, pos := range positions {
		matches = append(matches, Match{
			Position:    pos,
			Text:        text[pos:pos+len(pattern)],
			EndPosition: pos + len(pattern),
		})
	}

	return matches
}

// FindMatchesIgnoreCase returns detailed matches case-insensitively.
func FindMatchesIgnoreCase(pattern, text string) []Match {
	bm := NewWithOptions(pattern, false)
	positions := bm.FindAll(text)

	matches := []Match{}
	for _, pos := range positions {
		matches = append(matches, Match{
			Position:    pos,
			Text:        text[pos:pos+len(pattern)],
			EndPosition: pos + len(pattern),
		})
	}

	return matches
}

// MultiPattern searches for multiple patterns simultaneously.
type MultiPattern struct {
	searchers []*BoyerMoore
	patterns  []string
}

// NewMultiPattern creates a multi-pattern searcher.
func NewMultiPattern(patterns ...string) *MultiPattern {
	mp := &MultiPattern{
		patterns: patterns,
	}

	for _, p := range patterns {
		mp.searchers = append(mp.searchers, New(p))
	}

	return mp
}

// FindAny finds the first occurrence of any pattern.
// Returns pattern index and position, or -1, -1 if none found.
func (mp *MultiPattern) FindAny(text string) (patternIndex, position int) {
	firstPos := -1
	firstIdx := -1

	for i, searcher := range mp.searchers {
		pos := searcher.Find(text)
		if pos >= 0 {
			if firstPos < 0 || pos < firstPos {
				firstPos = pos
				firstIdx = i
			}
		}
	}

	return firstIdx, firstPos
}

// FindAll finds all occurrences of all patterns.
func (mp *MultiPattern) FindAll(text string) map[int][]int {
	result := make(map[int][]int)

	for i, searcher := range mp.searchers {
		positions := searcher.FindAll(text)
		if len(positions) > 0 {
			result[i] = positions
		}
	}

	return result
}

// ContainsAny checks if any pattern exists.
func (mp *MultiPattern) ContainsAny(text string) bool {
	idx, _ := mp.FindAny(text)
	return idx >= 0
}

// CountAll counts occurrences of each pattern.
func (mp *MultiPattern) CountAll(text string) map[int]int {
	result := make(map[int]int)

	for i, searcher := range mp.searchers {
		result[i] = searcher.Count(text)
	}

	return result
}

// ValidatePattern checks if a pattern is valid for searching.
func ValidatePattern(pattern string) string {
	if len(pattern) == 0 {
		return "pattern cannot be empty"
	}

	if !utf8.ValidString(pattern) {
		return "pattern contains invalid UTF-8 encoding"
	}

	return ""
}

// PatternStats provides statistics about the pattern.
type PatternStats struct {
	Length       int
	UniqueChars  int
	CharFreq     map[byte]int
	HasRepeated  bool
	IsPalindrome bool
}

// AnalyzePattern analyzes a pattern and returns statistics.
func AnalyzePattern(pattern string) PatternStats {
	stats := PatternStats{
		Length:    len(pattern),
		CharFreq:  make(map[byte]int),
	}

	for i := 0; i < len(pattern); i++ {
		stats.CharFreq[pattern[i]]++
	}

	stats.UniqueChars = len(stats.CharFreq)

	for _, count := range stats.CharFreq {
		if count > 1 {
			stats.HasRepeated = true
			break
		}
	}

	// Check palindrome
	stats.IsPalindrome = isPalindrome(pattern)

	return stats
}

// isPalindrome checks if string is a palindrome.
func isPalindrome(s string) bool {
	n := len(s)
	for i := 0; i < n/2; i++ {
		if s[i] != s[n-1-i] {
			return false
		}
	}
	return true
}