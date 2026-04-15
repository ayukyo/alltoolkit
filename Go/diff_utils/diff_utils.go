// Package diffutils provides text comparison and diff utilities.
// All functions are safe for concurrent use and handle Unicode correctly.
package diffutils

import (
	"bytes"
	"fmt"
	"strings"
	"unicode/utf8"
)

// Operation represents the type of diff operation.
type Operation int

const (
	// Equal indicates no change
	Equal Operation = iota
	// Insert indicates text was inserted
	Insert
	// Delete indicates text was deleted
	Delete
)

// Diff represents a single diff operation.
type Diff struct {
	Type Operation
	Text string
}

// Result holds the complete diff result.
type Result struct {
	Diffs  []Diff
	Stats  Stats
	LinesA int
	LinesB int
}

// Stats contains diff statistics.
type Stats struct {
	Added   int // Number of added lines/chars
	Removed int // Number of removed lines/chars
	Changed int // Number of changed lines/chars
	Equal   int // Number of unchanged lines/chars
}

// DiffLines compares two strings line by line and returns the diff.
// This is the most common diff operation, suitable for comparing files.
//
// Parameters:
//   - a: Original text (old version)
//   - b: New text (new version)
//
// Returns:
//   - Result containing diffs and statistics
//
// Example:
//
//     result := DiffLines("hello\nworld", "hello\nthere\nworld")
//     // Returns diff showing "there" was inserted
func DiffLines(a, b string) Result {
	linesA := splitLines(a)
	linesB := splitLines(b)

	// Compute LCS (Longest Common Subsequence) for lines
	lcs := computeLCS(linesA, linesB)

	diffs := make([]Diff, 0)
	stats := Stats{}

	i, j := 0, 0
	for _, l := range lcs {
		// Add deletions before this LCS match
		for i < len(linesA) && linesA[i] != l {
			diffs = append(diffs, Diff{Type: Delete, Text: linesA[i]})
			stats.Removed++
			i++
		}
		// Add insertions before this LCS match
		for j < len(linesB) && linesB[j] != l {
			diffs = append(diffs, Diff{Type: Insert, Text: linesB[j]})
			stats.Added++
			j++
		}
		// Add the matching line
		if i < len(linesA) && j < len(linesB) {
			diffs = append(diffs, Diff{Type: Equal, Text: l})
			stats.Equal++
			i++
			j++
		}
	}

	// Add remaining deletions
	for i < len(linesA) {
		diffs = append(diffs, Diff{Type: Delete, Text: linesA[i]})
		stats.Removed++
		i++
	}
	// Add remaining insertions
	for j < len(linesB) {
		diffs = append(diffs, Diff{Type: Insert, Text: linesB[j]})
		stats.Added++
		j++
	}

	return Result{
		Diffs:  diffs,
		Stats:  stats,
		LinesA: len(linesA),
		LinesB: len(linesB),
	}
}

// DiffChars compares two strings character by character.
// Useful for fine-grained text comparison.
//
// Parameters:
//   - a: Original string
//   - b: New string
//
// Returns:
//   - Slice of Diff operations
//
// Example:
//
//     diffs := DiffChars("kitten", "sitting")
//     // Shows character-level differences
func DiffChars(a, b string) []Diff {
	runesA := []rune(a)
	runesB := []rune(b)

	lcs := computeLCSRune(runesA, runesB)

	diffs := make([]Diff, 0)
	i, j := 0, 0

	for _, l := range lcs {
		// Collect deletions
		var deleted []rune
		for i < len(runesA) && runesA[i] != l {
			deleted = append(deleted, runesA[i])
			i++
		}
		if len(deleted) > 0 {
			diffs = append(diffs, Diff{Type: Delete, Text: string(deleted)})
		}

		// Collect insertions
		var inserted []rune
		for j < len(runesB) && runesB[j] != l {
			inserted = append(inserted, runesB[j])
			j++
		}
		if len(inserted) > 0 {
			diffs = append(diffs, Diff{Type: Insert, Text: string(inserted)})
		}

		// Add the matching character
		if i < len(runesA) && j < len(runesB) {
			if len(diffs) > 0 && diffs[len(diffs)-1].Type == Equal {
				diffs[len(diffs)-1].Text += string(l)
			} else {
				diffs = append(diffs, Diff{Type: Equal, Text: string(l)})
			}
			i++
			j++
		}
	}

	// Handle remaining
	if i < len(runesA) {
		diffs = append(diffs, Diff{Type: Delete, Text: string(runesA[i:])})
	}
	if j < len(runesB) {
		diffs = append(diffs, Diff{Type: Insert, Text: string(runesB[j:])})
	}

	return diffs
}

// DiffWords compares two strings word by word.
// Words are defined as sequences separated by whitespace.
//
// Parameters:
//   - a: Original text
//   - b: New text
//
// Returns:
//   - Slice of Diff operations at word level
//
// Example:
//
//     diffs := DiffWords("hello world", "hello beautiful world")
//     // Shows "beautiful" was inserted
func DiffWords(a, b string) []Diff {
	wordsA := splitWords(a)
	wordsB := splitWords(b)

	lcs := computeLCS(wordsA, wordsB)

	diffs := make([]Diff, 0)
	i, j := 0, 0

	for _, l := range lcs {
		for i < len(wordsA) && wordsA[i] != l {
			diffs = append(diffs, Diff{Type: Delete, Text: wordsA[i]})
			i++
		}
		for j < len(wordsB) && wordsB[j] != l {
			diffs = append(diffs, Diff{Type: Insert, Text: wordsB[j]})
			j++
		}
		if i < len(wordsA) && j < len(wordsB) {
			diffs = append(diffs, Diff{Type: Equal, Text: l})
			i++
			j++
		}
	}

	for i < len(wordsA) {
		diffs = append(diffs, Diff{Type: Delete, Text: wordsA[i]})
		i++
	}
	for j < len(wordsB) {
		diffs = append(diffs, Diff{Type: Insert, Text: wordsB[j]})
		j++
	}

	return diffs
}

// FormatUnified returns a unified diff format string.
// This is the classic diff format used by version control systems.
//
// Parameters:
//   - result: The diff result from DiffLines
//   - context: Number of context lines to show around changes
//   - fileA: Original filename
//   - fileB: New filename
//
// Returns:
//   - Unified diff string
//
// Example:
//
//     result := DiffLines(old, new)
//     fmt.Println(FormatUnified(result, 3, "old.txt", "new.txt"))
func FormatUnified(result Result, context int, fileA, fileB string) string {
	var buf bytes.Buffer

	// Header
	buf.WriteString(fmt.Sprintf("--- %s\n", fileA))
	buf.WriteString(fmt.Sprintf("+++ %s\n", fileB))

	// Group hunks
	hunks := extractHunks(result.Diffs, context)

	for _, hunk := range hunks {
		buf.WriteString(fmt.Sprintf("@@ -%d,%d +%d,%d @@\n",
			hunk.StartA+1, hunk.LenA,
			hunk.StartB+1, hunk.LenB))

		for _, d := range hunk.Diffs {
			switch d.Type {
			case Delete:
				buf.WriteString("-" + d.Text + "\n")
			case Insert:
				buf.WriteString("+" + d.Text + "\n")
			case Equal:
				buf.WriteString(" " + d.Text + "\n")
			}
		}
	}

	return buf.String()
}

// FormatColor returns an ANSI-colored diff string.
// Red for deletions, green for insertions, white for unchanged.
//
// Parameters:
//   - diffs: Slice of Diff operations
//
// Returns:
//   - ANSI-colored string
//
// Example:
//
//     result := DiffLines(old, new)
//     fmt.Println(FormatColor(result.Diffs))
func FormatColor(diffs []Diff) string {
	const (
		colorReset  = "\033[0m"
		colorRed    = "\033[31m"
		colorGreen  = "\033[32m"
		colorYellow = "\033[33m"
	)

	var buf bytes.Buffer
	for _, d := range diffs {
		switch d.Type {
		case Delete:
			buf.WriteString(colorRed + "-" + d.Text + colorReset + "\n")
		case Insert:
			buf.WriteString(colorGreen + "+" + d.Text + colorReset + "\n")
		case Equal:
			buf.WriteString(" " + d.Text + "\n")
		}
	}
	return buf.String()
}

// FormatHTML returns an HTML-formatted diff.
// Useful for web applications.
//
// Parameters:
//   - diffs: Slice of Diff operations
//
// Returns:
//   - HTML string with spans marking additions/deletions
//
// Example:
//
//     result := DiffLines(old, new)
//     html := FormatHTML(result.Diffs)
func FormatHTML(diffs []Diff) string {
	var buf bytes.Buffer
	buf.WriteString(`<div class="diff">`)

	for _, d := range diffs {
		escaped := htmlEscape(d.Text)
		switch d.Type {
		case Delete:
			buf.WriteString(`<del>` + escaped + "</del>\n")
		case Insert:
			buf.WriteString(`<ins>` + escaped + "</ins>\n")
		case Equal:
			buf.WriteString(`<span>` + escaped + "</span>\n")
		}
	}

	buf.WriteString(`</div>`)
	return buf.String()
}

// Similarity returns a similarity score between 0 and 1.
// 1 means identical, 0 means completely different.
//
// Parameters:
//   - a: First string
//   - b: Second string
//
// Returns:
//   - Similarity score (0.0 to 1.0)
//
// Example:
//
//     score := Similarity("hello", "hallo") // ~0.8
func Similarity(a, b string) float64 {
	if a == b {
		return 1.0
	}
	if len(a) == 0 || len(b) == 0 {
		return 0.0
	}

	// Use Levenshtein distance for similarity
	distance := levenshteinDistance(a, b)
	maxLen := max(len(a), len(b))
	return 1.0 - float64(distance)/float64(maxLen)
}

// LevenshteinDistance computes the edit distance between two strings.
// This is the minimum number of single-character edits (insert, delete, replace)
// needed to transform one string into another.
//
// Parameters:
//   - a: First string
//   - b: Second string
//
// Returns:
//   - Edit distance (non-negative integer)
//
// Example:
//
//     distance := LevenshteinDistance("kitten", "sitting") // 3
func LevenshteinDistance(a, b string) int {
	return levenshteinDistance(a, b)
}

// LCS computes the Longest Common Subsequence of two strings.
// Returns the LCS string and its length.
//
// Parameters:
//   - a: First string
//   - b: Second string
//
// Returns:
//   - LCS string and length
//
// Example:
//
//     lcs, length := LCS("ABCBDAB", "BDCABA")
//     // lcs = "BCBA" (or similar), length = 4
func LCS(a, b string) (string, int) {
	runesA := []rune(a)
	runesB := []rune(b)

	lcs := computeLCSRune(runesA, runesB)
	return string(lcs), len(lcs)
}

// ========== Helper Functions ==========

type hunk struct {
	StartA, StartB int
	LenA, LenB     int
	Diffs          []Diff
}

func extractHunks(diffs []Diff, context int) []hunk {
	if len(diffs) == 0 {
		return nil
	}

	hunks := make([]hunk, 0)
	var currentHunk *hunk
	lineA, lineB := 0, 0

	for i, d := range diffs {
		isChange := d.Type != Equal

		if isChange {
			if currentHunk == nil {
				// Start new hunk with context
				start := max(0, i-context)
				currentHunk = &hunk{
					StartA: lineA,
					StartB: lineB,
					Diffs:  make([]Diff, 0),
				}
				// Add preceding context
				for j := start; j < i; j++ {
					currentHunk.Diffs = append(currentHunk.Diffs, diffs[j])
					currentHunk.LenA++
					currentHunk.LenB++
				}
			}
			currentHunk.Diffs = append(currentHunk.Diffs, d)
			if d.Type == Delete {
				currentHunk.LenA++
			} else if d.Type == Insert {
				currentHunk.LenB++
			}
		} else if currentHunk != nil {
			// Add context after change
			currentHunk.Diffs = append(currentHunk.Diffs, d)
			currentHunk.LenA++
			currentHunk.LenB++

			// Check if we should close the hunk
			if i > 0 && diffs[i-1].Type != Equal {
				contextCount := 0
				for j := len(currentHunk.Diffs) - 1; j >= 0; j-- {
					if currentHunk.Diffs[j].Type == Equal {
						contextCount++
						if contextCount >= context {
							hunks = append(hunks, *currentHunk)
							currentHunk = nil
							break
						}
					} else {
						break
					}
				}
			}
		}

		// Update line counters
		switch d.Type {
		case Delete:
			lineA++
		case Insert:
			lineB++
		case Equal:
			lineA++
			lineB++
		}
	}

	if currentHunk != nil {
		hunks = append(hunks, *currentHunk)
	}

	return hunks
}

func splitLines(s string) []string {
	if s == "" {
		return nil
	}
	lines := strings.Split(s, "\n")
	// Remove trailing empty string if input ends with newline
	if len(lines) > 0 && lines[len(lines)-1] == "" {
		lines = lines[:len(lines)-1]
	}
	return lines
}

func splitWords(s string) []string {
	return strings.Fields(s)
}

func computeLCS(a, b []string) []string {
	m, n := len(a), len(b)
	if m == 0 || n == 0 {
		return nil
	}

	// DP table
	dp := make([][]int, m+1)
	for i := range dp {
		dp[i] = make([]int, n+1)
	}

	// Fill DP table
	for i := 1; i <= m; i++ {
		for j := 1; j <= n; j++ {
			if a[i-1] == b[j-1] {
				dp[i][j] = dp[i-1][j-1] + 1
			} else {
				dp[i][j] = max(dp[i-1][j], dp[i][j-1])
			}
		}
	}

	// Backtrack to find LCS
	lcs := make([]string, 0, dp[m][n])
	i, j := m, n
	for i > 0 && j > 0 {
		if a[i-1] == b[j-1] {
			lcs = append([]string{a[i-1]}, lcs...)
			i--
			j--
		} else if dp[i-1][j] > dp[i][j-1] {
			i--
		} else {
			j--
		}
	}

	return lcs
}

func computeLCSRune(a, b []rune) []rune {
	m, n := len(a), len(b)
	if m == 0 || n == 0 {
		return nil
	}

	dp := make([][]int, m+1)
	for i := range dp {
		dp[i] = make([]int, n+1)
	}

	for i := 1; i <= m; i++ {
		for j := 1; j <= n; j++ {
			if a[i-1] == b[j-1] {
				dp[i][j] = dp[i-1][j-1] + 1
			} else {
				dp[i][j] = max(dp[i-1][j], dp[i][j-1])
			}
		}
	}

	lcs := make([]rune, 0, dp[m][n])
	i, j := m, n
	for i > 0 && j > 0 {
		if a[i-1] == b[j-1] {
			lcs = append([]rune{a[i-1]}, lcs...)
			i--
			j--
		} else if dp[i-1][j] > dp[i][j-1] {
			i--
		} else {
			j--
		}
	}

	return lcs
}

func levenshteinDistance(a, b string) int {
	runesA := []rune(a)
	runesB := []rune(b)

	// Use UTF-8 aware length
	m, n := utf8.RuneCountInString(a), utf8.RuneCountInString(b)

	if m == 0 {
		return n
	}
	if n == 0 {
		return m
	}

	// Use two rows for space optimization
	prev := make([]int, n+1)
	curr := make([]int, n+1)

	// Initialize first row
	for j := 0; j <= n; j++ {
		prev[j] = j
	}

	// Fill DP table
	for i := 1; i <= m; i++ {
		curr[0] = i
		for j := 1; j <= n; j++ {
			if runesA[i-1] == runesB[j-1] {
				curr[j] = prev[j-1]
			} else {
				curr[j] = 1 + min(prev[j], min(curr[j-1], prev[j-1]))
			}
		}
		prev, curr = curr, prev
	}

	return prev[n]
}

func htmlEscape(s string) string {
	s = strings.ReplaceAll(s, "&", "&amp;")
	s = strings.ReplaceAll(s, "<", "&lt;")
	s = strings.ReplaceAll(s, ">", "&gt;")
	s = strings.ReplaceAll(s, "\"", "&quot;")
	s = strings.ReplaceAll(s, "'", "&#39;")
	return s
}

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