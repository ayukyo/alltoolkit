// Package text_similarity_utils provides text similarity calculation algorithms
// with zero external dependencies.
//
// Supported algorithms:
//   - Levenshtein Distance
//   - Damerau-Levenshtein Distance
//   - Jaccard Similarity
//   - Cosine Similarity
//   - Sorensen-Dice Coefficient
//   - Hamming Distance
//   - Jaro Similarity
//   - Jaro-Winkler Similarity
//   - Soundex Comparison
//   - N-Gram Similarity
package text_similarity_utils

import (
	"math"
	"sort"
	"strings"
	"unicode"
)

// ============================================================================
// Levenshtein Distance
// ============================================================================

// LevenshteinDistance calculates the minimum number of single-character edits
// (insertions, deletions, substitutions) required to change one string into another.
func LevenshteinDistance(s1, s2 string) int {
	if s1 == s2 {
		return 0
	}
	if len(s1) == 0 {
		return len(s2)
	}
	if len(s2) == 0 {
		return len(s1)
	}

	r1, r2 := []rune(s1), []rune(s2)
	len1, len2 := len(r1), len(r2)

	// Use two rows to optimize memory
	prev := make([]int, len2+1)
	curr := make([]int, len2+1)

	for j := 0; j <= len2; j++ {
		prev[j] = j
	}

	for i := 1; i <= len1; i++ {
		curr[0] = i
		for j := 1; j <= len2; j++ {
			cost := 1
			if r1[i-1] == r2[j-1] {
				cost = 0
			}
			curr[j] = min(
				prev[j]+1,      // deletion
				curr[j-1]+1,    // insertion
				prev[j-1]+cost, // substitution
			)
		}
		prev, curr = curr, prev
	}

	return prev[len2]
}

// LevenshteinSimilarity returns a normalized similarity score between 0 and 1.
func LevenshteinSimilarity(s1, s2 string) float64 {
	if s1 == s2 {
		return 1.0
	}
	maxLen := max(len([]rune(s1)), len([]rune(s2)))
	if maxLen == 0 {
		return 1.0
	}
	distance := LevenshteinDistance(s1, s2)
	return 1.0 - float64(distance)/float64(maxLen)
}

// ============================================================================
// Damerau-Levenshtein Distance
// ============================================================================

// DamerauLevenshteinDistance calculates the minimum number of edits including
// adjacent transpositions (swap of two adjacent characters).
func DamerauLevenshteinDistance(s1, s2 string) int {
	if s1 == s2 {
		return 0
	}
	if len(s1) == 0 {
		return len(s2)
	}
	if len(s2) == 0 {
		return len(s1)
	}

	r1, r2 := []rune(s1), []rune(s2)
	len1, len2 := len(r1), len(r2)

	matrix := make([][]int, len1+1)
	for i := range matrix {
		matrix[i] = make([]int, len2+1)
	}

	for i := 0; i <= len1; i++ {
		matrix[i][0] = i
	}
	for j := 0; j <= len2; j++ {
		matrix[0][j] = j
	}

	for i := 1; i <= len1; i++ {
		for j := 1; j <= len2; j++ {
			cost := 1
			if r1[i-1] == r2[j-1] {
				cost = 0
			}

			matrix[i][j] = min(
				matrix[i-1][j]+1,    // deletion
				matrix[i][j-1]+1,    // insertion
				matrix[i-1][j-1]+cost, // substitution
			)

			// Transposition
			if i > 1 && j > 1 && r1[i-1] == r2[j-2] && r1[i-2] == r2[j-1] {
				matrix[i][j] = min(matrix[i][j], matrix[i-2][j-2]+cost)
			}
		}
	}

	return matrix[len1][len2]
}

// ============================================================================
// Jaccard Similarity
// ============================================================================

// JaccardSimilarity calculates the Jaccard similarity coefficient using n-grams.
// Returns a value between 0 and 1.
func JaccardSimilarity(s1, s2 string, ngramSize int) float64 {
	if s1 == s2 {
		return 1.0
	}
	if len(s1) == 0 || len(s2) == 0 {
		return 0.0
	}

	set1 := getNgramSet(s1, ngramSize)
	set2 := getNgramSet(s2, ngramSize)

	if len(set1) == 0 && len(set2) == 0 {
		return 1.0
	}

	intersection := 0
	for gram := range set1 {
		if set2[gram] {
			intersection++
		}
	}

	union := len(set1) + len(set2) - intersection
	if union == 0 {
		return 0.0
	}

	return float64(intersection) / float64(union)
}

// JaccardSimilarityWords calculates Jaccard similarity using word sets.
func JaccardSimilarityWords(s1, s2 string) float64 {
	words1 := getWordSet(s1)
	words2 := getWordSet(s2)

	if len(words1) == 0 && len(words2) == 0 {
		return 1.0
	}

	intersection := 0
	for word := range words1 {
		if words2[word] {
			intersection++
		}
	}

	union := len(words1) + len(words2) - intersection
	if union == 0 {
		return 0.0
	}

	return float64(intersection) / float64(union)
}

// ============================================================================
// Cosine Similarity
// ============================================================================

// CosineSimilarity calculates the cosine similarity between two strings
// using n-gram frequency vectors.
func CosineSimilarity(s1, s2 string, ngramSize int) float64 {
	if s1 == s2 {
		return 1.0
	}
	if len(s1) == 0 || len(s2) == 0 {
		return 0.0
	}

	vec1 := getNgramFreq(s1, ngramSize)
	vec2 := getNgramFreq(s2, ngramSize)

	dotProduct := 0.0
	for gram, count1 := range vec1 {
		if count2, exists := vec2[gram]; exists {
			dotProduct += float64(count1 * count2)
		}
	}

	magnitude1 := 0.0
	for _, count := range vec1 {
		magnitude1 += float64(count * count)
	}

	magnitude2 := 0.0
	for _, count := range vec2 {
		magnitude2 += float64(count * count)
	}

	if magnitude1 == 0 || magnitude2 == 0 {
		return 0.0
	}

	return dotProduct / (math.Sqrt(magnitude1) * math.Sqrt(magnitude2))
}

// ============================================================================
// Sorensen-Dice Coefficient
// ============================================================================

// SorensenDiceCoefficient calculates the Sørensen–Dice coefficient using n-grams.
// Returns a value between 0 and 1.
func SorensenDiceCoefficient(s1, s2 string, ngramSize int) float64 {
	if s1 == s2 {
		return 1.0
	}
	if len(s1) == 0 || len(s2) == 0 {
		return 0.0
	}

	set1 := getNgramSet(s1, ngramSize)
	set2 := getNgramSet(s2, ngramSize)

	if len(set1) == 0 && len(set2) == 0 {
		return 1.0
	}

	intersection := 0
	for gram := range set1 {
		if set2[gram] {
			intersection++
		}
	}

	totalSize := len(set1) + len(set2)
	if totalSize == 0 {
		return 0.0
	}

	return 2.0 * float64(intersection) / float64(totalSize)
}

// ============================================================================
// Hamming Distance
// ============================================================================

// HammingDistance calculates the Hamming distance between two strings.
// Both strings must be of equal length.
// Returns -1 if strings have different lengths.
func HammingDistance(s1, s2 string) int {
	if len(s1) != len(s2) {
		return -1
	}

	r1, r2 := []rune(s1), []rune(s2)
	if len(r1) != len(r2) {
		return -1 // Different rune lengths
	}

	distance := 0
	for i := range r1 {
		if r1[i] != r2[i] {
			distance++
		}
	}
	return distance
}

// HammingSimilarity returns normalized similarity (0-1) for equal-length strings.
// Returns -1 if strings have different lengths.
func HammingSimilarity(s1, s2 string) float64 {
	if len(s1) != len(s2) {
		return -1
	}

	r1, r2 := []rune(s1), []rune(s2)
	if len(r1) != len(r2) {
		return -1
	}

	if len(r1) == 0 {
		return 1.0
	}

	distance := HammingDistance(s1, s2)
	if distance < 0 {
		return -1
	}
	return 1.0 - float64(distance)/float64(len(r1))
}

// ============================================================================
// Jaro Similarity
// ============================================================================

// JaroSimilarity calculates the Jaro similarity between two strings.
// Returns a value between 0 and 1.
func JaroSimilarity(s1, s2 string) float64 {
	if s1 == s2 {
		return 1.0
	}

	r1, r2 := []rune(s1), []rune(s2)
	len1, len2 := len(r1), len(r2)

	if len1 == 0 && len2 == 0 {
		return 1.0
	}
	if len1 == 0 || len2 == 0 {
		return 0.0
	}

	matchDistance := max(len1, len2)/2 - 1
	if matchDistance < 0 {
		matchDistance = 0
	}

	matched1 := make([]bool, len1)
	matched2 := make([]bool, len2)

	matches := 0
	transpositions := 0

	for i := 0; i < len1; i++ {
		start := max(0, i-matchDistance)
		end := min(i+matchDistance+1, len2)

		for j := start; j < end; j++ {
			if matched2[j] || r1[i] != r2[j] {
				continue
			}
			matched1[i] = true
			matched2[j] = true
			matches++
			break
		}
	}

	if matches == 0 {
		return 0.0
	}

	k := 0
	for i := 0; i < len1; i++ {
		if !matched1[i] {
			continue
		}
		for !matched2[k] {
			k++
		}
		if r1[i] != r2[k] {
			transpositions++
		}
		k++
	}

	return (float64(matches)/float64(len1) +
		float64(matches)/float64(len2) +
		float64(matches-transpositions)/float64(matches)) / 3.0
}

// ============================================================================
// Jaro-Winkler Similarity
// ============================================================================

// JaroWinklerSimilarity calculates the Jaro-Winkler similarity.
// Gives extra weight to strings that match from the beginning.
// Returns a value between 0 and 1.
func JaroWinklerSimilarity(s1, s2 string) float64 {
	jaro := JaroSimilarity(s1, s2)

	if jaro < 0.7 {
		return jaro
	}

	r1, r2 := []rune(s1), []rune(s2)
	minLen := min(len(r1), len(r2))
	if minLen > 4 {
		minLen = 4
	}

	prefix := 0
	for i := 0; i < minLen; i++ {
		if r1[i] == r2[i] {
			prefix++
		} else {
			break
		}
	}

	return jaro + float64(prefix)*0.1*(1.0-jaro)
}

// ============================================================================
// Soundex
// ============================================================================

// Soundex returns the Soundex code for a string.
func Soundex(s string) string {
	if len(s) == 0 {
		return ""
	}

	r := []rune(strings.ToUpper(s))
	result := make([]rune, 1, 4)
	result[0] = r[0]

	// Soundex mapping
	soundexMap := map[rune]rune{
		'B': '1', 'F': '1', 'P': '1', 'V': '1',
		'C': '2', 'G': '2', 'J': '2', 'K': '2', 'Q': '2', 'S': '2', 'X': '2', 'Z': '2',
		'D': '3', 'T': '3',
		'L': '4',
		'M': '5', 'N': '5',
		'R': '6',
	}

	prevCode, ok := soundexMap[r[0]]
	if !ok {
		prevCode = '0'
	}

	for i := 1; i < len(r) && len(result) < 4; i++ {
		if !unicode.IsLetter(r[i]) {
			continue
		}
		code, exists := soundexMap[unicode.ToUpper(r[i])]
		if exists && code != prevCode {
			result = append(result, code)
		}
		if exists {
			prevCode = code
		}
	}

	// Pad with zeros
	for len(result) < 4 {
		result = append(result, '0')
	}

	return string(result)
}

// SoundexSimilarity compares two strings using Soundex encoding.
// Returns 1 if Soundex codes match, 0 otherwise.
func SoundexSimilarity(s1, s2 string) float64 {
	code1 := Soundex(s1)
	code2 := Soundex(s2)

	if code1 == code2 {
		return 1.0
	}
	return 0.0
}

// ============================================================================
// N-Gram Similarity
// ============================================================================

// NGramSimilarity calculates similarity using overlapping n-grams.
func NGramSimilarity(s1, s2 string, n int) float64 {
	if s1 == s2 {
		return 1.0
	}
	if len(s1) == 0 || len(s2) == 0 {
		return 0.0
	}

	set1 := getNgramSet(s1, n)
	set2 := getNgramSet(s2, n)

	if len(set1) == 0 || len(set2) == 0 {
		return 0.0
	}

	intersection := 0
	for gram := range set1 {
		if set2[gram] {
			intersection++
		}
	}

	maxSize := max(len(set1), len(set2))
	return float64(intersection) / float64(maxSize)
}

// ============================================================================
// Most Similar (Best Match)
// ============================================================================

// SimilarityResult represents a similarity comparison result.
type SimilarityResult struct {
	Text       string
	Score      float64
	Algorithm  string
}

// MostSimilar returns the most similar string from candidates using specified algorithm.
// Supported algorithms: "levenshtein", "jaro", "jarowinkler", "jaccard", "cosine", "dice", "ngram"
func MostSimilar(target string, candidates []string, algorithm string, ngramSize int) SimilarityResult {
	if len(candidates) == 0 {
		return SimilarityResult{}
	}

	var best SimilarityResult
	best.Score = -1

	for _, candidate := range candidates {
		var score float64
		switch strings.ToLower(algorithm) {
		case "levenshtein", "lev":
			score = LevenshteinSimilarity(target, candidate)
		case "jaro":
			score = JaroSimilarity(target, candidate)
		case "jarowinkler", "jw", "jaro-winkler":
			score = JaroWinklerSimilarity(target, candidate)
		case "jaccard":
			score = JaccardSimilarity(target, candidate, ngramSize)
		case "cosine":
			score = CosineSimilarity(target, candidate, ngramSize)
		case "dice", "sorensen":
			score = SorensenDiceCoefficient(target, candidate, ngramSize)
		case "ngram":
			score = NGramSimilarity(target, candidate, ngramSize)
		case "soundex":
			score = SoundexSimilarity(target, candidate)
		default:
			score = LevenshteinSimilarity(target, candidate)
		}

		if score > best.Score {
			best = SimilarityResult{
				Text:      candidate,
				Score:     score,
				Algorithm: algorithm,
			}
		}
	}

	return best
}

// AllSimilarities returns all similarity scores for a target against candidates.
func AllSimilarities(target string, candidates []string, algorithm string, ngramSize int) []SimilarityResult {
	results := make([]SimilarityResult, len(candidates))

	for i, candidate := range candidates {
		var score float64
		switch strings.ToLower(algorithm) {
		case "levenshtein", "lev":
			score = LevenshteinSimilarity(target, candidate)
		case "jaro":
			score = JaroSimilarity(target, candidate)
		case "jarowinkler", "jw", "jaro-winkler":
			score = JaroWinklerSimilarity(target, candidate)
		case "jaccard":
			score = JaccardSimilarity(target, candidate, ngramSize)
		case "cosine":
			score = CosineSimilarity(target, candidate, ngramSize)
		case "dice", "sorensen":
			score = SorensenDiceCoefficient(target, candidate, ngramSize)
		case "ngram":
			score = NGramSimilarity(target, candidate, ngramSize)
		case "soundex":
			score = SoundexSimilarity(target, candidate)
		default:
			score = LevenshteinSimilarity(target, candidate)
		}

		results[i] = SimilarityResult{
			Text:      candidate,
			Score:     score,
			Algorithm: algorithm,
		}
	}

	sort.Slice(results, func(i, j int) bool {
		return results[i].Score > results[j].Score
	})

	return results
}

// ============================================================================
// Helper Functions
// ============================================================================

func getNgramSet(s string, n int) map[string]bool {
	set := make(map[string]bool)
	r := []rune(s)

	if n <= 0 {
		n = 2
	}

	for i := 0; i <= len(r)-n; i++ {
		gram := string(r[i : i+n])
		set[gram] = true
	}

	return set
}

func getNgramFreq(s string, n int) map[string]int {
	freq := make(map[string]int)
	r := []rune(s)

	if n <= 0 {
		n = 2
	}

	for i := 0; i <= len(r)-n; i++ {
		gram := string(r[i : i+n])
		freq[gram]++
	}

	return freq
}

func getWordSet(s string) map[string]bool {
	set := make(map[string]bool)
	words := strings.Fields(s)

	for _, word := range words {
		word = strings.ToLower(strings.TrimSpace(word))
		if word != "" {
			set[word] = true
		}
	}

	return set
}