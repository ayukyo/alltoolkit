// Package z_algorithm_utils provides Z-algorithm implementations for efficient
// string matching and pattern searching. Zero-dependency, production-ready.
//
// The Z-algorithm computes an array Z where Z[i] is the length of the longest
// substring starting at position i that matches the prefix of the string.
// This allows O(n) pattern matching when combined with sentinel concatenation.
//
// Author: AllToolkit
// License: MIT

package zalgorithmutils

import (
	"bytes"
	"fmt"
	"strings"
)

// ============================================================================
// Core Types
// ============================================================================

// ZMatch represents a match found using Z-algorithm.
type ZMatch struct {
	Index  int
	Length int
	Text   string
}

// String contains the matched substring.
func (m ZMatch) String() string {
	if m.Index >= 0 && m.Index+m.Length <= len(m.Text) {
		return m.Text[m.Index : m.Index+m.Length]
	}
	return ""
}

// StringPeriod represents the period information of a string.
type StringPeriod struct {
	String     string
	Period     int
	IsPeriodic bool
}

// PeriodString returns the repeating unit.
func (p StringPeriod) PeriodString() string {
	if p.Period > 0 && p.Period <= len(p.String) {
		return p.String[:p.Period]
	}
	return ""
}

// ProbabilityDistribution represents a probability distribution.
type ProbabilityDistribution struct {
	Outcomes  map[int]float64
	Mean      float64
	Variance  float64
	StdDev    float64
	MinValue  int
	MaxValue  int
}

// ============================================================================
// Core Z-Algorithm
// ============================================================================

// ZArray computes the Z-array for a string.
// Z[i] is the length of the longest substring starting from i
// that is also a prefix of the string.
//
// Time complexity: O(n)
// Space complexity: O(n)
func ZArray(s string) []int {
	n := len(s)
	if n == 0 {
		return []int{}
	}

	z := make([]int, n)
	l, r := 0, 0 // [l, r] is the rightmost Z-box

	for i := 1; i < n; i++ {
		if i <= r {
			// i is within current Z-box
			z[i] = min(r-i+1, z[i-l])
		}

		// Try to extend the Z-box
		whileLoop := true
		for whileLoop && i+z[i] < n && s[z[i]] == s[i+z[i]] {
			z[i]++
			if i+z[i]-1 > r {
				l, r = i, i+z[i]-1
			}
		}
	}

	return z
}

// ZArrayBytes computes the Z-array for a byte slice.
func ZArrayBytes(data []byte) []int {
	n := len(data)
	if n == 0 {
		return []int{}
	}

	z := make([]int, n)
	l, r := 0, 0

	for i := 1; i < n; i++ {
		if i <= r {
			z[i] = min(r-i+1, z[i-l])
		}

		for i+z[i] < n && data[z[i]] == data[i+z[i]] {
			z[i]++
			if i+z[i]-1 > r {
				l, r = i, i+z[i]-1
			}
		}
	}

	return z
}

// ZArrayWithSentinel computes Z-array for pattern+sentinel+text concatenation.
func ZArrayWithSentinel(pattern, text, sentinel string) []int {
	combined := pattern + sentinel + text
	return ZArray(combined)
}

// ============================================================================
// Pattern Matching
// ============================================================================

// FindAllOccurrences finds all occurrences of pattern in text.
// Time complexity: O(n + m)
func FindAllOccurrences(pattern, text string) []int {
	if pattern == "" || text == "" {
		return []int{}
	}

	m, n := len(pattern), len(text)
	if m > n {
		return []int{}
	}

	// Build Z-array for pattern$text
	combined := pattern + "$" + text
	z := ZArray(combined)

	// Find all positions where Z[i] >= m
	positions := []int{}
	for i := m + 1; i < len(z); i++ {
		if z[i] >= m {
			positions = append(positions, i-m-1)
		}
	}

	return positions
}

// FindFirstOccurrence finds the first occurrence of pattern in text.
func FindFirstOccurrence(pattern, text string) int {
	if pattern == "" || text == "" {
		return -1
	}

	m, n := len(pattern), len(text)
	if m > n {
		return -1
	}

	combined := pattern + "$" + text
	z := ZArray(combined)

	for i := m + 1; i < len(z); i++ {
		if z[i] >= m {
			return i - m - 1
		}
	}

	return -1
}

// CountOccurrences counts the number of occurrences of pattern in text.
func CountOccurrences(pattern, text string) int {
	return len(FindAllOccurrences(pattern, text))
}

// FindMatches finds all matches with details.
func FindMatches(pattern, text string) []ZMatch {
	positions := FindAllOccurrences(pattern, text)
	matches := make([]ZMatch, len(positions))
	for i, pos := range positions {
		matches[i] = ZMatch{
			Index:  pos,
			Length: len(pattern),
			Text:   text,
		}
	}
	return matches
}

// ============================================================================
// Substring Analysis
// ============================================================================

// LongestPrefixSuffix finds the length of the longest proper prefix that is also a suffix.
func LongestPrefixSuffix(s string) int {
	if s == "" {
		return 0
	}

	z := ZArray(s)
	n := len(s)

	maxLPS := 0
	for i := 1; i < n; i++ {
		if i+z[i] == n {
			maxLPS = max(maxLPS, z[i])
		}
	}

	return maxLPS
}

// LongestRepeatedSubstring finds the longest substring that appears at least twice.
func LongestRepeatedSubstring(s string) (string, []int) {
	if s == "" {
		return "", []int{}
	}

	n := len(s)
	z := ZArray(s)

	maxLen := 0
	positions := []int{}

	for i := 1; i < n; i++ {
		if z[i] > maxLen {
			maxLen = z[i]
			positions = []int{i}
		} else if z[i] == maxLen && maxLen > 0 {
			positions = append(positions, i)
		}
	}

	// Check for longer substrings not starting at 0
	for length := n / 2; length > maxLen; length-- {
		for start := 0; start <= n-length; start++ {
			substr := s[start : start+length]
			found := FindAllOccurrences(substr, s)
			if len(found) >= 2 {
				return substr, found
			}
		}
	}

	if maxLen == 0 {
		return "", []int{}
	}

	return s[:maxLen], positions
}

// LongestCommonPrefix finds the length of the longest common prefix of two strings.
func LongestCommonPrefix(s1, s2 string) int {
	combined := s1 + "$" + s2
	z := ZArray(combined)

	pos := len(s1) + 1
	if pos < len(z) {
		return z[pos]
	}
	return 0
}

// ============================================================================
// Period Detection
// ============================================================================

// FindMinimalPeriod finds the minimal period of a string.
func FindMinimalPeriod(s string) StringPeriod {
	if s == "" {
		return StringPeriod{String: s, Period: 0, IsPeriodic: false}
	}

	n := len(s)

	// Check all possible periods
	for p := 1; p <= n/2; p++ {
		if n%p != 0 {
			continue
		}

		// Verify period p
		valid := true
		for i := p; i < n; i++ {
			if s[i] != s[i%p] {
				valid = false
				break
			}
		}

		if valid {
			return StringPeriod{String: s, Period: p, IsPeriodic: true}
		}
	}

	// Using Z-array approach for more general case
	z := ZArray(s)

	for p := 1; p <= n; p++ {
		if p < n && p+z[p] >= n {
			valid := true
			for i := p; i < n; i++ {
				if s[i] != s[i-p] {
					valid = false
					break
				}
			}
			if valid {
				return StringPeriod{String: s, Period: p, IsPeriodic: p < n}
			}
		}
	}

	return StringPeriod{String: s, Period: n, IsPeriodic: false}
}

// IsRotation checks if s2 is a rotation of s1.
func IsRotation(s1, s2 string) bool {
	if len(s1) != len(s2) {
		return false
	}

	if s1 == "" {
		return true
	}

	// s2 is rotation of s1 iff s2 is substring of s1 + s1
	return len(FindAllOccurrences(s2, s1+s1)) > 0
}

// FindAllRotations finds all unique rotations of a string.
func FindAllRotations(s string) []string {
	if s == "" {
		return []string{""}
	}

	n := len(s)
	rotations := make([]string, n)
	for i := 0; i < n; i++ {
		rotations[i] = s[i:] + s[:i]
	}

	// Remove duplicates while preserving order
	seen := make(map[string]bool)
	unique := []string{}
	for _, rot := range rotations {
		if !seen[rot] {
			seen[rot] = true
			unique = append(unique, rot)
		}
	}

	return unique
}

// ============================================================================
// Compression
// ============================================================================

// CompressString finds the smallest repeating unit.
func CompressString(s string) (string, int) {
	if s == "" {
		return "", 1
	}

	period := FindMinimalPeriod(s)

	if period.IsPeriodic {
		return period.PeriodString(), len(s) / period.Period
	}

	return s, 1
}

// DecompressString decompresses a string pattern.
func DecompressString(pattern string, count int) string {
	result := ""
	for i := 0; i < count; i++ {
		result += pattern
	}
	return result
}

// ============================================================================
// Similarity
// ============================================================================

// SimilarityScore calculates a similarity score based on longest common prefix.
func SimilarityScore(s1, s2 string) float64 {
	if s1 == "" && s2 == "" {
		return 1.0
	}
	if s1 == "" || s2 == "" {
		return 0.0
	}

	lcp := LongestCommonPrefix(s1, s2)
	maxLen := max(len(s1), len(s2))

	return float64(lcp) / float64(maxLen)
}

// BatchSimilarity calculates similarity scores for multiple strings.
func BatchSimilarity(base string, strings []string) []float64 {
	if base == "" {
		results := make([]float64, len(strings))
		for i, s := range strings {
			if s == "" {
				results[i] = 1.0
			} else {
				results[i] = 0.0
			}
		}
		return results
	}

	maxLen := len(base)
	for _, s := range strings {
		maxLen = max(maxLen, len(s))
	}

	results := make([]float64, len(strings))
	for i, s := range strings {
		if s == "" {
			results[i] = 0.0
		} else {
			lcp := LongestCommonPrefix(base, s)
			results[i] = float64(lcp) / float64(maxLen)
		}
	}

	return results
}

// ============================================================================
// Utility Functions
// ============================================================================

// VisualizeZArray creates a visual representation of the Z-array.
func VisualizeZArray(s string) string {
	z := ZArray(s)
	var lines []string

	lines = append(lines, fmt.Sprintf("String: %s", s))

	// Index line
	indexLine := "Index:  "
	for i := 0; i < len(s); i++ {
		indexLine += fmt.Sprintf("%2d ", i)
	}
	lines = append(lines, indexLine)

	// Char line
	charLine := "Char:   "
	for _, c := range s {
		charLine += fmt.Sprintf("%2s ", string(c))
	}
	lines = append(lines, charLine)

	// Z line
	zLine := "Z:      "
	for _, v := range z {
		zLine += fmt.Sprintf("%2d ", v)
	}
	lines = append(lines, zLine)

	return strings.Join(lines, "\n")
}

// ValidateZArray validates that a Z-array is correct for a given string.
func ValidateZArray(s string, z []int) bool {
	if len(s) != len(z) {
		return false
	}

	computed := ZArray(s)
	for i := range z {
		if z[i] != computed[i] {
			return false
		}
	}

	return true
}

// ============================================================================
// Pattern Matcher Class
// ============================================================================

// ZPatternMatcher is an efficient multi-pattern matcher using Z-algorithm.
type ZPatternMatcher struct {
	patterns []string
	zArrays  [][]int
}

// NewZPatternMatcher creates a new pattern matcher.
func NewZPatternMatcher(patterns []string) *ZPatternMatcher {
	zArrays := make([][]int, len(patterns))
	for i, p := range patterns {
		zArrays[i] = ZArray(p)
	}
	return &ZPatternMatcher{
		patterns: patterns,
		zArrays:  zArrays,
	}
}

// Search searches for all patterns in text.
func (m *ZPatternMatcher) Search(text string) []struct {
	PatternIndex int
	Position     int
	Pattern      string
} {
	var results []struct {
		PatternIndex int
		Position     int
		Pattern      string
	}

	for i, pattern := range m.patterns {
		positions := FindAllOccurrences(pattern, text)
		for _, pos := range positions {
			results = append(results, struct {
				PatternIndex int
				Position     int
				Pattern      string
			}{
				PatternIndex: i,
				Position:     pos,
				Pattern:      pattern,
			})
		}
	}

	return results
}

// SearchFirst finds the first occurrence of any pattern.
func (m *ZPatternMatcher) SearchFirst(text string) *struct {
	PatternIndex int
	Position     int
	Pattern      string
} {
	firstPos := len(text)
	firstPatternIdx := -1

	for i, pattern := range m.patterns {
		pos := FindFirstOccurrence(pattern, text)
		if pos != -1 && pos < firstPos {
			firstPos = pos
			firstPatternIdx = i
		}
	}

	if firstPatternIdx >= 0 {
		return &struct {
			PatternIndex int
			Position     int
			Pattern      string
		}{
			PatternIndex: firstPatternIdx,
			Position:     firstPos,
			Pattern:      m.patterns[firstPatternIdx],
		}
	}
	return nil
}

// CountAll counts occurrences of each pattern.
func (m *ZPatternMatcher) CountAll(text string) map[string]int {
	counts := make(map[string]int)
	for _, pattern := range m.patterns {
		counts[pattern] = CountOccurrences(pattern, text)
	}
	return counts
}

// ============================================================================
// Helper Functions
// ============================================================================

func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}

func max(a, b int) int {
	if a > b {
		return a
	}
	return b
}

// Contains checks if a string contains another string using Z-algorithm.
func Contains(pattern, text string) bool {
	return FindFirstOccurrence(pattern, text) != -1
}

// HasPrefixAny checks if text starts with any of the patterns.
func HasPrefixAny(text string, patterns []string) bool {
	for _, pattern := range patterns {
		if strings.HasPrefix(text, pattern) {
			return true
		}
	}
	return false
}

// HasSuffixAny checks if text ends with any of the patterns.
func HasSuffixAny(text string, patterns []string) bool {
	for _, pattern := range patterns {
		if strings.HasSuffix(text, pattern) {
			return true
		}
	}
	return false
}

// ReplaceAll replaces all occurrences of pattern with replacement.
func ReplaceAll(pattern, replacement, text string) string {
	positions := FindAllOccurrences(pattern, text)
	if len(positions) == 0 {
		return text
	}

	// Build result using bytes.Buffer for efficiency
	var result bytes.Buffer
	lastPos := 0
	m := len(pattern)

	for _, pos := range positions {
		result.WriteString(text[lastPos:pos])
		result.WriteString(replacement)
		lastPos = pos + m
	}
	result.WriteString(text[lastPos:])

	return result.String()
}

// SplitByPattern splits text by pattern occurrences.
func SplitByPattern(pattern, text string) []string {
	if pattern == "" {
		return []string{text}
	}

	positions := FindAllOccurrences(pattern, text)
	if len(positions) == 0 {
		return []string{text}
	}

	var parts []string
	lastPos := 0
	m := len(pattern)

	for _, pos := range positions {
		parts = append(parts, text[lastPos:pos])
		lastPos = pos + m
	}
	parts = append(parts, text[lastPos:])

	return parts
}