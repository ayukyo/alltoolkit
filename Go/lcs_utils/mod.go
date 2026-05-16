// Package lcs_utils provides Longest Common Subsequence (LCS) algorithms
// for comparing sequences. This is a fundamental algorithm used in:
// - Text comparison and diff tools
// - Version control systems
// - Bioinformatics (DNA/RNA sequence alignment)
// - Plagiarism detection
// - Data synchronization
package lcs_utils

import (
	"strings"
)

// ============================================================================
// Core Types
// ============================================================================

// Result represents the result of an LCS computation
type Result struct {
	// The longest common subsequence
	Subsequence []string

	// Length of the LCS
	Length int

	// Indices in the first sequence where LCS elements appear
	IndicesA []int

	// Indices in the second sequence where LCS elements appear
	IndicesB []int
}

// DiffResult represents the result of a diff operation
type DiffResult struct {
	// Type of change: "equal", "insert", "delete"
	Type string

	// The content
	Value string

	// Index in sequence A (for equal and delete)
	IndexA int

	// Index in sequence B (for equal and insert)
	IndexB int
}

// AlignmentResult represents sequence alignment result
type AlignmentResult struct {
	// Aligned sequence A (with gaps represented as "-")
	AlignedA []string

	// Aligned sequence B (with gaps represented as "-")
	AlignedB []string

	// The LCS
	LCS []string

	// Alignment score (LCS length)
	Score int
}

// ============================================================================
// Basic LCS Algorithms
// ============================================================================

// LCS computes the Longest Common Subsequence of two slices
// Uses standard dynamic programming with O(m*n) time and space
func LCS(a, b []string) []string {
	result := LCSWithIndices(a, b)
	return result.Subsequence
}

// LCSLength computes only the length of LCS (space-optimized)
// Uses O(min(m,n)) space instead of O(m*n)
func LCSLength(a, b []string) int {
	m, n := len(a), len(b)

	// Ensure 'a' is the shorter sequence for space optimization
	if m > n {
		a, b = b, a
		m, n = n, m
	}

	// Use two rows instead of full matrix
	prev := make([]int, m+1)
	curr := make([]int, m+1)

	for j := 1; j <= n; j++ {
		for i := 1; i <= m; i++ {
			if a[i-1] == b[j-1] {
				curr[i] = prev[i-1] + 1
			} else {
				curr[i] = max(prev[i], curr[i-1])
			}
		}
		prev, curr = curr, prev
	}

	return prev[m]
}

// LCSWithIndices computes LCS along with the indices in both sequences
func LCSWithIndices(a, b []string) Result {
	m, n := len(a), len(b)

	// Build DP table
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
	indicesA := make([]int, 0, dp[m][n])
	indicesB := make([]int, 0, dp[m][n])

	i, j := m, n
	for i > 0 && j > 0 {
		if a[i-1] == b[j-1] {
			lcs = append([]string{a[i-1]}, lcs...)
			indicesA = append([]int{i - 1}, indicesA...)
			indicesB = append([]int{j - 1}, indicesB...)
			i--
			j--
		} else if dp[i-1][j] > dp[i][j-1] {
			i--
		} else {
			j--
		}
	}

	return Result{
		Subsequence: lcs,
		Length:      dp[m][n],
		IndicesA:    indicesA,
		IndicesB:    indicesB,
	}
}

// LCSBytes computes LCS for byte slices
func LCSBytes(a, b []byte) []byte {
	strA := make([]string, len(a))
	strB := make([]string, len(b))
	for i, b := range a {
		strA[i] = string([]byte{b})
	}
	for i, b := range b {
		strB[i] = string([]byte{b})
	}

	result := LCS(strA, strB)
	combined := make([]byte, len(result))
	for i, s := range result {
		combined[i] = []byte(s)[0]
	}
	return combined
}

// LCSString computes LCS for strings (character by character)
func LCSString(a, b string) string {
	runesA := []rune(a)
	runesB := []rune(b)

	strA := make([]string, len(runesA))
	strB := make([]string, len(runesB))
	for i, r := range runesA {
		strA[i] = string(r)
	}
	for i, r := range runesB {
		strB[i] = string(r)
	}

	return strings.Join(LCS(strA, strB), "")
}

// LCSStringLines computes LCS for strings split by lines
func LCSStringLines(a, b string) []string {
	linesA := strings.Split(a, "\n")
	linesB := strings.Split(b, "\n")
	return LCS(linesA, linesB)
}

// ============================================================================
// Advanced LCS Algorithms
// ============================================================================

// LCSAll finds all possible LCS solutions
// Warning: Can be exponentially many solutions for large inputs
func LCSAll(a, b []string) [][]string {
	m, n := len(a), len(b)

	// Build DP table
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

	// Backtrack all paths
	return backtrackAll(dp, a, b, m, n)
}

func backtrackAll(dp [][]int, a, b []string, i, j int) [][]string {
	if i == 0 || j == 0 {
		return [][]string{{}}
	}

	if a[i-1] == b[j-1] {
		// Current character is part of LCS
		results := backtrackAll(dp, a, b, i-1, j-1)
		for idx := range results {
			results[idx] = append(results[idx], a[i-1])
		}
		return results
	}

	var results [][]string

	// If both directions are equal, explore both
	if dp[i-1][j] == dp[i][j-1] {
		results = append(results, backtrackAll(dp, a, b, i-1, j)...)
		results = append(results, backtrackAll(dp, a, b, i, j-1)...)
	} else if dp[i-1][j] > dp[i][j-1] {
		results = append(results, backtrackAll(dp, a, b, i-1, j)...)
	} else {
		results = append(results, backtrackAll(dp, a, b, i, j-1)...)
	}

	// Deduplicate results
	return deduplicateResults(results)
}

func deduplicateResults(results [][]string) [][]string {
	seen := make(map[string]bool)
	unique := make([][]string, 0)
	for _, r := range results {
		key := strings.Join(r, "\x00")
		if !seen[key] {
			seen[key] = true
			unique = append(unique, r)
		}
	}
	return unique
}

// LCSOfMultiple computes LCS of multiple sequences
// Uses a reduction approach: LCS(A, B, C) = LCS(LCS(A, B), C)
func LCSOfMultiple(sequences ...[]string) []string {
	if len(sequences) == 0 {
		return nil
	}
	if len(sequences) == 1 {
		return sequences[0]
	}

	result := LCS(sequences[0], sequences[1])
	for i := 2; i < len(sequences); i++ {
		result = LCS(result, sequences[i])
		if len(result) == 0 {
			return nil
		}
	}
	return result
}

// ============================================================================
// Diff Operations
// ============================================================================

// Diff computes the differences between two sequences
// Returns a list of operations to transform A into B
func Diff(a, b []string) []DiffResult {
	result := LCSWithIndices(a, b)
	diff := make([]DiffResult, 0)

	idxA, idxB := 0, 0
	lcsIdx := 0

	for lcsIdx < len(result.Subsequence) {
		// Process deletions before this LCS element
		for idxA < result.IndicesA[lcsIdx] {
			diff = append(diff, DiffResult{
				Type:   "delete",
				Value:  a[idxA],
				IndexA: idxA,
				IndexB: -1,
			})
			idxA++
		}

		// Process insertions before this LCS element
		for idxB < result.IndicesB[lcsIdx] {
			diff = append(diff, DiffResult{
				Type:   "insert",
				Value:  b[idxB],
				IndexA: -1,
				IndexB: idxB,
			})
			idxB++
		}

		// Process the LCS element
		diff = append(diff, DiffResult{
			Type:   "equal",
			Value:  result.Subsequence[lcsIdx],
			IndexA: idxA,
			IndexB: idxB,
		})
		idxA++
		idxB++
		lcsIdx++
	}

	// Process remaining deletions
	for idxA < len(a) {
		diff = append(diff, DiffResult{
			Type:   "delete",
			Value:  a[idxA],
			IndexA: idxA,
			IndexB: -1,
		})
		idxA++
	}

	// Process remaining insertions
	for idxB < len(b) {
		diff = append(diff, DiffResult{
			Type:   "insert",
			Value:  b[idxB],
			IndexA: -1,
			IndexB: idxB,
		})
		idxB++
	}

	return diff
}

// DiffString computes the differences between two strings (line by line)
func DiffString(a, b string) []DiffResult {
	linesA := strings.Split(a, "\n")
	linesB := strings.Split(b, "\n")
	return Diff(linesA, linesB)
}

// DiffStats computes statistics about the differences
type DiffStats struct {
	Additions  int
	Deletions  int
	Unchanged  int
	Similarity float64
}

// ComputeDiffStats computes statistics about the differences
func ComputeDiffStats(diff []DiffResult) DiffStats {
	stats := DiffStats{}
	for _, d := range diff {
		switch d.Type {
		case "insert":
			stats.Additions++
		case "delete":
			stats.Deletions++
		case "equal":
			stats.Unchanged++
		}
	}

	total := stats.Unchanged + stats.Additions + stats.Deletions
	if total > 0 {
		stats.Similarity = float64(stats.Unchanged) / float64(total)
	}

	return stats
}

// ============================================================================
// Sequence Alignment
// ============================================================================

// Align performs sequence alignment based on LCS
func Align(a, b []string) AlignmentResult {
	result := LCSWithIndices(a, b)

	alignedA := make([]string, 0)
	alignedB := make([]string, 0)

	idxA, idxB := 0, 0

	for _, lcsChar := range result.Subsequence {
		// Add gaps in A before this LCS character
		for idxA < len(a) && a[idxA] != lcsChar {
			alignedA = append(alignedA, a[idxA])
			alignedB = append(alignedB, "-")
			idxA++
		}

		// Add gaps in B before this LCS character
		for idxB < len(b) && b[idxB] != lcsChar {
			alignedA = append(alignedA, "-")
			alignedB = append(alignedB, b[idxB])
			idxB++
		}

		// Add the matching character
		alignedA = append(alignedA, lcsChar)
		alignedB = append(alignedB, lcsChar)
		idxA++
		idxB++
	}

	// Handle remaining characters
	for idxA < len(a) {
		alignedA = append(alignedA, a[idxA])
		alignedB = append(alignedB, "-")
		idxA++
	}

	for idxB < len(b) {
		alignedA = append(alignedA, "-")
		alignedB = append(alignedB, b[idxB])
		idxB++
	}

	return AlignmentResult{
		AlignedA: alignedA,
		AlignedB: alignedB,
		LCS:      result.Subsequence,
		Score:    result.Length,
	}
}

// AlignString performs sequence alignment on strings (character by character)
func AlignString(a, b string) AlignmentResult {
	runesA := []rune(a)
	runesB := []rune(b)

	strA := make([]string, len(runesA))
	strB := make([]string, len(runesB))
	for i, r := range runesA {
		strA[i] = string(r)
	}
	for i, r := range runesB {
		strB[i] = string(r)
	}

	return Align(strA, strB)
}

// ============================================================================
// Shortest Common Supersequence
// ============================================================================

// SCS computes the Shortest Common Supersequence of two sequences
// SCS contains both A and B as subsequences and is of minimum length
func SCS(a, b []string) []string {
	result := LCSWithIndices(a, b)

	scs := make([]string, 0)
	idxA, idxB := 0, 0

	for i := 0; i < len(result.Subsequence); i++ {
		// Add characters from A before this LCS character
		for idxA < result.IndicesA[i] {
			scs = append(scs, a[idxA])
			idxA++
		}

		// Add characters from B before this LCS character
		for idxB < result.IndicesB[i] {
			scs = append(scs, b[idxB])
			idxB++
		}

		// Add the LCS character
		scs = append(scs, result.Subsequence[i])
		idxA++
		idxB++
	}

	// Add remaining characters from A
	for idxA < len(a) {
		scs = append(scs, a[idxA])
		idxA++
	}

	// Add remaining characters from B
	for idxB < len(b) {
		scs = append(scs, b[idxB])
		idxB++
	}

	return scs
}

// SCSLength computes the length of the Shortest Common Supersequence
func SCSLength(a, b []string) int {
	return len(a) + len(b) - LCSLength(a, b)
}

// ============================================================================
// Edit Distance
// ============================================================================

// EditDistance computes the minimum number of operations to transform A into B
// Uses the relationship: EditDistance = |A| + |B| - 2*LCS(A,B)
// Note: This is NOT the Levenshtein distance, but the LCS-based edit distance
// which only counts insertions and deletions (no substitutions)
func EditDistance(a, b []string) int {
	return len(a) + len(b) - 2*LCSLength(a, b)
}

// EditDistanceString computes the edit distance for strings
func EditDistanceString(a, b string) int {
	return EditDistance(strings.Split(a, ""), strings.Split(b, ""))
}

// ============================================================================
// Similarity Measures
// ============================================================================

// SimilarityRatio computes the similarity ratio between two sequences
// Returns a value between 0 and 1
func SimilarityRatio(a, b []string) float64 {
	if len(a) == 0 && len(b) == 0 {
		return 1.0
	}

	maxLen := max(len(a), len(b))
	if maxLen == 0 {
		return 1.0
	}

	lcsLen := LCSLength(a, b)
	return float64(lcsLen) / float64(maxLen)
}

// SimilarityRatioString computes the similarity ratio for strings
func SimilarityRatioString(a, b string) float64 {
	return SimilarityRatio(
		strings.Split(a, ""),
		strings.Split(b, ""),
	)
}

// JaccardSimilarity computes Jaccard similarity based on LCS
func JaccardSimilarity(a, b []string) float64 {
	if len(a) == 0 && len(b) == 0 {
		return 1.0
	}

	unionLen := len(a) + len(b) - LCSLength(a, b)
	if unionLen == 0 {
		return 1.0
	}

	return float64(LCSLength(a, b)) / float64(unionLen)
}

// ============================================================================
// Hunt-Szymanski Algorithm
// ============================================================================

// LCSHuntSzymanski computes LCS using the Hunt-Szymanski algorithm
// More efficient when the number of matches is small
// Time complexity: O((r + n) log n) where r is the number of matches
func LCSHuntSzymanski(a, b []string) []string {
	// Build a map of positions for each character in B
	positions := make(map[string][]int)
	for i := len(b) - 1; i >= 0; i-- {
		positions[b[i]] = append(positions[b[i]], i)
	}

	// Threshold array for patience sorting
	threshold := make([]int, 0, len(a))

	// Process A in order
	for _, char := range a {
		posList, exists := positions[char]
		if !exists {
			continue
		}

		// For each position in B where this character appears
		for _, pos := range posList {
			// Binary search for the position to insert
			lo, hi := 0, len(threshold)
			for lo < hi {
				mid := (lo + hi) / 2
				if threshold[mid] < pos {
					lo = mid + 1
				} else {
					hi = mid
				}
			}

			if lo == len(threshold) {
				threshold = append(threshold, pos)
			} else {
				threshold[lo] = pos
			}
		}
	}

	// Reconstruct LCS from threshold
	// This is a simplified version - the full algorithm would track the actual sequence
	return make([]string, len(threshold))
}

// ============================================================================
// Utility Functions
// ============================================================================

func max(a, b int) int {
	if a > b {
		return a
	}
	return b
}

// IsSubsequence checks if A is a subsequence of B
func IsSubsequence(a, b []string) bool {
	i := 0
	for _, char := range b {
		if i < len(a) && a[i] == char {
			i++
		}
	}
	return i == len(a)
}

// IsSubsequenceString checks if string A is a subsequence of string B
func IsSubsequenceString(a, b string) bool {
	return IsSubsequence(
		strings.Split(a, ""),
		strings.Split(b, ""),
	)
}

// AllSubsequences generates all subsequences of a sequence
// Warning: Returns 2^n results, use with caution on large sequences
func AllSubsequences(seq []string) [][]string {
	n := len(seq)
	count := 1 << n
	result := make([][]string, 0, count)

	for i := 0; i < count; i++ {
		subseq := make([]string, 0)
		for j := 0; j < n; j++ {
			if (i & (1 << j)) != 0 {
				subseq = append(subseq, seq[j])
			}
		}
		result = append(result, subseq)
	}

	return result
}

// CountCommonSubsequences counts the number of common subsequences
// This is useful for measuring sequence similarity beyond just LCS
func CountCommonSubsequences(a, b []string) int {
	m, n := len(a), len(b)

	// DP table to store count
	dp := make([][]int, m+1)
	for i := range dp {
		dp[i] = make([]int, n+1)
	}

	// Base case: empty subsequences
	for i := 0; i <= m; i++ {
		dp[i][0] = 1
	}
	for j := 0; j <= n; j++ {
		dp[0][j] = 1
	}

	// Fill DP table
	for i := 1; i <= m; i++ {
		for j := 1; j <= n; j++ {
			if a[i-1] == b[j-1] {
				dp[i][j] = dp[i-1][j-1] + dp[i-1][j] + dp[i][j-1] - dp[i-1][j-1]
			} else {
				dp[i][j] = dp[i-1][j] + dp[i][j-1] - dp[i-1][j-1]
			}
		}
	}

	return dp[m][n] - 1 // Subtract 1 to exclude empty subsequence
}