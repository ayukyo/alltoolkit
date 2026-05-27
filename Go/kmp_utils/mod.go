// Package kmp_utils implements the Knuth-Morris-Pratt (KMP) string search algorithm.
// KMP is a linear-time string matching algorithm that achieves O(n+m) complexity
// by preprocessing the pattern to build a failure function (partial match table).
//
// Features:
// - Zero dependencies, uses only Go standard library
// - Build failure function (LPS array) for pattern preprocessing
// - Find first and all occurrences of pattern in text
// - Case-sensitive and case-insensitive search
// - Count occurrences and check containment
// - Replace and replace-first operations
// - Multi-pattern search support
// - Pattern validation and analysis utilities
//
// Example usage:
//
//	kmp := kmp_utils.New("pattern")
//	positions := kmp.FindAll("text with pattern here")
//	fmt.Println(positions) // [10]
//
package kmp_utils

import (
	"strings"
	"unicode/utf8"
)

// KMP represents a preprocessed pattern for KMP searching.
type KMP struct {
	pattern         string
	lps             []int // Longest Prefix Suffix array
	caseSensitive   bool
	processedPattern string
}

// New creates a new KMP searcher with the given pattern.
func New(pattern string) *KMP {
	return NewWithOptions(pattern, true)
}

// NewWithOptions creates a new KMP searcher with custom options.
func NewWithOptions(pattern string, caseSensitive bool) *KMP {
	kmp := &KMP{
		pattern:       pattern,
		caseSensitive: caseSensitive,
	}

	if !caseSensitive {
		kmp.processedPattern = strings.ToLower(pattern)
	} else {
		kmp.processedPattern = pattern
	}

	kmp.buildLPS()
	return kmp
}

// buildLPS builds the Longest Prefix Suffix array.
// lps[i] = the longest proper prefix of pattern[0..i] that is also a suffix.
func (kmp *KMP) buildLPS() {
	m := len(kmp.processedPattern)
	kmp.lps = make([]int, m)
	
	if m == 0 {
		return
	}

	length := 0 // Length of the previous longest prefix suffix
	i := 1

	for i < m {
		if kmp.processedPattern[i] == kmp.processedPattern[length] {
			length++
			kmp.lps[i] = length
			i++
		} else {
			if length != 0 {
				// Try the previous longest prefix suffix
				length = kmp.lps[length-1]
			} else {
				kmp.lps[i] = 0
				i++
			}
		}
	}
}

// preprocessText preprocesses text for case-insensitive search.
func (kmp *KMP) preprocessText(text string) string {
	if kmp.caseSensitive {
		return text
	}
	return strings.ToLower(text)
}

// Find searches for the first occurrence of the pattern in the text.
// Returns the starting position (0-indexed) or -1 if not found.
func (kmp *KMP) Find(text string) int {
	processedText := kmp.preprocessText(text)
	m := len(kmp.processedPattern)
	n := len(processedText)

	if m == 0 || n < m {
		return -1
	}

	i := 0 // Index for text
	j := 0 // Index for pattern

	for i < n {
		if processedText[i] == kmp.processedPattern[j] {
			i++
			j++
		}

		if j == m {
			return i - j // Found pattern at position i-j
		} else if i < n && processedText[i] != kmp.processedPattern[j] {
			if j != 0 {
				j = kmp.lps[j-1]
			} else {
				i++
			}
		}
	}

	return -1
}

// FindAll searches for all occurrences of the pattern in the text.
// Returns an array of starting positions (0-indexed).
func (kmp *KMP) FindAll(text string) []int {
	processedText := kmp.preprocessText(text)
	m := len(kmp.processedPattern)
	n := len(processedText)

	if m == 0 || n < m {
		return []int{}
	}

	positions := []int{}
	i := 0 // Index for text
	j := 0 // Index for pattern

	for i < n {
		if processedText[i] == kmp.processedPattern[j] {
			i++
			j++
		}

		if j == m {
			positions = append(positions, i-j)
			j = kmp.lps[j-1] // Continue searching
		} else if i < n && processedText[i] != kmp.processedPattern[j] {
			if j != 0 {
				j = kmp.lps[j-1]
			} else {
				i++
			}
		}
	}

	return positions
}

// FindLast searches for the last occurrence of the pattern.
func (kmp *KMP) FindLast(text string) int {
	positions := kmp.FindAll(text)
	if len(positions) == 0 {
		return -1
	}
	return positions[len(positions)-1]
}

// Count returns the number of occurrences of the pattern in the text.
func (kmp *KMP) Count(text string) int {
	return len(kmp.FindAll(text))
}

// Contains checks if the pattern exists in the text.
func (kmp *KMP) Contains(text string) bool {
	return kmp.Find(text) >= 0
}

// Replace replaces all occurrences of the pattern with replacement.
func (kmp *KMP) Replace(text, replacement string) string {
	positions := kmp.FindAll(text)
	if len(positions) == 0 {
		return text
	}

	m := len(kmp.pattern)
	result := text

	for i := len(positions) - 1; i >= 0; i-- {
		pos := positions[i]
		result = result[:pos] + replacement + result[pos+m:]
	}

	return result
}

// ReplaceFirst replaces the first occurrence of the pattern.
func (kmp *KMP) ReplaceFirst(text, replacement string) string {
	pos := kmp.Find(text)
	if pos < 0 {
		return text
	}

	m := len(kmp.pattern)
	return text[:pos] + replacement + text[pos+m:]
}

// GetPattern returns the search pattern.
func (kmp *KMP) GetPattern() string {
	return kmp.pattern
}

// GetPatternLength returns the pattern length.
func (kmp *KMP) GetPatternLength() int {
	return len(kmp.processedPattern)
}

// IsCaseSensitive returns whether search is case-sensitive.
func (kmp *KMP) IsCaseSensitive() bool {
	return kmp.caseSensitive
}

// GetLPS returns a copy of the LPS array for analysis.
func (kmp *KMP) GetLPS() []int {
	lps := make([]int, len(kmp.lps))
	copy(lps, kmp.lps)
	return lps
}

// Match represents a found match with position and details.
type Match struct {
	Position    int    // Starting position (0-indexed)
	Text        string // The matched substring
	EndPosition int    // Ending position (exclusive)
}

// FindMatches returns detailed match information.
func FindMatches(pattern, text string) []Match {
	kmp := New(pattern)
	positions := kmp.FindAll(text)

	matches := []Match{}
	for _, pos := range positions {
		matches = append(matches, Match{
			Position:    pos,
			Text:        text[pos : pos+len(pattern)],
			EndPosition: pos + len(pattern),
		})
	}

	return matches
}

// FindMatchesIgnoreCase returns detailed matches case-insensitively.
func FindMatchesIgnoreCase(pattern, text string) []Match {
	kmp := NewWithOptions(pattern, false)
	positions := kmp.FindAll(text)

	matches := []Match{}
	for _, pos := range positions {
		matches = append(matches, Match{
			Position:    pos,
			Text:        text[pos : pos+len(pattern)],
			EndPosition: pos + len(pattern),
		})
	}

	return matches
}

// Utility functions for direct use without creating searcher.

// Find searches for pattern in text using KMP.
func Find(pattern, text string) int {
	kmp := New(pattern)
	return kmp.Find(text)
}

// FindAll finds all occurrences of pattern in text.
func FindAll(pattern, text string) []int {
	kmp := New(pattern)
	return kmp.FindAll(text)
}

// FindIgnoreCase searches case-insensitively.
func FindIgnoreCase(pattern, text string) int {
	kmp := NewWithOptions(pattern, false)
	return kmp.Find(text)
}

// FindAllIgnoreCase finds all occurrences case-insensitively.
func FindAllIgnoreCase(pattern, text string) []int {
	kmp := NewWithOptions(pattern, false)
	return kmp.FindAll(text)
}

// Count returns number of occurrences.
func Count(pattern, text string) int {
	kmp := New(pattern)
	return kmp.Count(text)
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
	kmp := New(pattern)
	return kmp.Replace(text, replacement)
}

// ReplaceFirst replaces first occurrence.
func ReplaceFirst(pattern, text, replacement string) string {
	kmp := New(pattern)
	return kmp.ReplaceFirst(text, replacement)
}

// BuildLPS builds the LPS array for a pattern without creating a KMP object.
func BuildLPS(pattern string) []int {
	m := len(pattern)
	if m == 0 {
		return []int{}
	}

	lps := make([]int, m)
	length := 0
	i := 1

	for i < m {
		if pattern[i] == pattern[length] {
			length++
			lps[i] = length
			i++
		} else {
			if length != 0 {
				length = lps[length-1]
			} else {
				lps[i] = 0
				i++
			}
		}
	}

	return lps
}

// MultiPattern searches for multiple patterns simultaneously.
type MultiPattern struct {
	searchers []*KMP
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
	LPSCoefficient float64 // Average LPS value / length (higher = more repetitive)
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

	// Calculate LPS coefficient
	lps := BuildLPS(pattern)
	if len(lps) > 0 {
		sum := 0
		for _, v := range lps {
			sum += v
		}
		stats.LPSCoefficient = float64(sum) / float64(len(lps))
	}

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

// StreamingKMP allows searching in a streaming fashion.
type StreamingKMP struct {
	pattern string
	lps     []int
	j       int      // Current state in pattern
	matches []int    // Match positions
	pos     int      // Current position in stream
	buffer  []byte   // Buffer for match extraction
}

// NewStreamingKMP creates a new streaming KMP searcher.
func NewStreamingKMP(pattern string) *StreamingKMP {
	return &StreamingKMP{
		pattern: pattern,
		lps:     BuildLPS(pattern),
		j:       0,
		pos:     0,
		buffer:  make([]byte, 0),
	}
}

// ProcessByte processes a single byte and returns true if a match was found.
func (skmp *StreamingKMP) ProcessByte(b byte) bool {
	skmp.buffer = append(skmp.buffer, b)
	m := len(skmp.pattern)

	for skmp.j > 0 && b != skmp.pattern[skmp.j] {
		skmp.j = skmp.lps[skmp.j-1]
	}

	if b == skmp.pattern[skmp.j] {
		skmp.j++
	}

	if skmp.j == m {
		skmp.matches = append(skmp.matches, skmp.pos-m+1)
		skmp.j = skmp.lps[skmp.j-1]
		skmp.pos++
		return true
	}

	skmp.pos++
	return false
}

// ProcessBytes processes multiple bytes and returns all match positions found.
func (skmp *StreamingKMP) ProcessBytes(data []byte) []int {
	positions := []int{}
	for _, b := range data {
		if skmp.ProcessByte(b) {
			positions = append(positions, skmp.matches[len(skmp.matches)-1])
		}
	}
	return positions
}

// GetMatches returns all matches found so far.
func (skmp *StreamingKMP) GetMatches() []int {
	return skmp.matches
}

// Reset resets the streaming state.
func (skmp *StreamingKMP) Reset() {
	skmp.j = 0
	skmp.pos = 0
	skmp.matches = nil
	skmp.buffer = skmp.buffer[:0]
}

// FindOverlapping finds overlapping matches.
// Standard KMP already handles overlapping matches correctly.
func FindOverlapping(pattern, text string) []int {
	return FindAll(pattern, text)
}

// FindNonOverlapping finds non-overlapping matches.
func FindNonOverlapping(pattern, text string) []int {
	kmp := New(pattern)
	processedText := kmp.preprocessText(text)
	m := len(kmp.processedPattern)
	n := len(processedText)

	if m == 0 || n < m {
		return []int{}
	}

	positions := []int{}
	i := 0
	j := 0

	for i < n {
		if processedText[i] == kmp.processedPattern[j] {
			i++
			j++
		}

		if j == m {
			positions = append(positions, i-j)
			j = 0 // Reset to find non-overlapping
		} else if i < n && processedText[i] != kmp.processedPattern[j] {
			if j != 0 {
				j = kmp.lps[j-1]
			} else {
				i++
			}
		}
	}

	return positions
}