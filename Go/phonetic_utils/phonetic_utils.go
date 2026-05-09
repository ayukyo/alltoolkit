// Package phonetic_utils provides phonetic encoding algorithms for name matching
// and fuzzy string comparison.
//
// Supported algorithms:
//   - Soundex (American Soundex)
//   - Metaphone
//   - Refined Soundex
//   - NYSIIS (New York State Identification and Intelligence System)
//   - Match Rating Codex (MRC)
//
// Applications:
//   - Name matching and deduplication
//   - Search with spelling tolerance
//   - Genealogy and record linkage
//   - Customer database deduplication
//
// Author: AllToolkit Contributors
// License: MIT
package phonetic_utils

import (
	"strings"
	"unicode"
)

// Soundex encodes a string using the American Soundex algorithm.
// Soundex codes have the format: First letter + 3 digits.
// Vowels and H, W are ignored after the first letter.
// Adjacent letters with the same code are merged.
func Soundex(text string) string {
	if text == "" {
		return "0000"
	}

	// Clean and uppercase
	cleaned := cleanString(text)
	if cleaned == "" {
		return "0000"
	}

	// Soundex letter groups
	soundexGroups := map[rune]string{
		'B': "1", 'F': "1", 'P': "1", 'V': "1",
		'C': "2", 'G': "2", 'J': "2", 'K': "2", 'Q': "2", 'S': "2", 'X': "2", 'Z': "2",
		'D': "3", 'T': "3",
		'L': "4",
		'M': "5", 'N': "5",
		'R': "6",
	}

	// Keep the first letter
	first := rune(cleaned[0])
	result := strings.ToUpper(string(first))

	// Get code for first letter
	prevCode := soundexGroups[first]

	// Process remaining letters
	for _, char := range cleaned[1:] {
		code := soundexGroups[char]
		if code != "" && code != prevCode {
			result += code
		}
		if code != "" {
			prevCode = code
		}
	}

	// Pad with zeros or truncate to 4 characters
	for len(result) < 4 {
		result += "0"
	}
	return result[:4]
}

// SoundexWords encodes each word in a string using Soundex.
func SoundexWords(text string) []string {
	words := strings.Fields(text)
	result := make([]string, len(words))
	for i, word := range words {
		result[i] = Soundex(word)
	}
	return result
}

// Metaphone encodes a string using the Metaphone algorithm.
// Metaphone is more accurate than Soundex for English names,
// handling more complex pronunciation rules.
func Metaphone(text string) string {
	if text == "" {
		return ""
	}

	cleaned := cleanString(text)
	if cleaned == "" {
		return ""
	}

	length := len(cleaned)
	result := strings.Builder{}
	i := 0

	for i < length {
		char := rune(cleaned[i])
		var nextChar, prevChar, nextNextChar rune
		if i+1 < length {
			nextChar = rune(cleaned[i+1])
		}
		if i > 0 {
			prevChar = rune(cleaned[i-1])
		}
		if i+2 < length {
			nextNextChar = rune(cleaned[i+2])
		}

		// Handle vowels at the beginning
		if i == 0 && isVowel(char) {
			result.WriteRune(char)
			i++
			continue
		}

		// Skip vowels in other positions
		if isVowel(char) {
			i++
			continue
		}

		switch char {
		case 'B':
			// B -> B, unless at end after M
			if !(i == length-1 && prevChar == 'M') {
				result.WriteRune('B')
			}
			i++

		case 'C':
			// C -> X (SH) if -CIA- or -CH-
			// C -> S if -CI-, -CE-, -CY-
			// C -> K otherwise
			if nextChar == 'I' && nextNextChar == 'A' {
				result.WriteRune('X')
			} else if nextChar == 'H' {
				result.WriteRune('X')
				i++
			} else if nextChar == 'I' || nextChar == 'E' || nextChar == 'Y' {
				result.WriteRune('S')
			} else {
				result.WriteRune('K')
			}
			i++

		case 'D':
			// D -> J if -DGE-, -DGI-, -DGY-
			// D -> T otherwise
			if nextChar == 'G' && (nextNextChar == 'E' || nextNextChar == 'I' || nextNextChar == 'Y') {
				result.WriteRune('J')
				i++
			} else {
				result.WriteRune('T')
			}
			i++

		case 'F':
			result.WriteRune('F')
			i++

		case 'G':
			// G -> F if -GH and not at beginning
			// G -> silent if -GN or -GNED
			// G -> J if -GI-, -GE-, -GY-
			// G -> K otherwise
			if nextChar == 'H' {
				if i == 0 {
					result.WriteRune('K')
				} else if i+2 >= length {
					// GH at end, silent
				} else if !isVowel(nextNextChar) {
					result.WriteRune('K')
				}
				i++
			} else if nextChar == 'N' {
				if i+2 >= length || (nextNextChar == 'E' && i+3 >= length) {
					// GN at end or GNED, silent
				} else {
					result.WriteRune('K')
				}
			} else if nextChar == 'I' || nextChar == 'E' || nextChar == 'Y' {
				result.WriteRune('J')
			} else {
				result.WriteRune('K')
			}
			i++

		case 'H':
			// H -> H if before vowel and not after C,G,P,S,T
			if isVowel(nextChar) && prevChar != 'C' && prevChar != 'G' && prevChar != 'P' && prevChar != 'S' && prevChar != 'T' {
				result.WriteRune('H')
			}
			i++

		case 'J':
			result.WriteRune('J')
			i++

		case 'K':
			// K -> silent if after C
			if prevChar != 'C' {
				result.WriteRune('K')
			}
			i++

		case 'L':
			result.WriteRune('L')
			i++

		case 'M':
			result.WriteRune('M')
			i++

		case 'N':
			result.WriteRune('N')
			i++

		case 'P':
			// P -> F if before H, P otherwise
			if nextChar == 'H' {
				result.WriteRune('F')
				i++
			} else {
				result.WriteRune('P')
			}
			i++

		case 'Q':
			result.WriteRune('K')
			i++

		case 'R':
			result.WriteRune('R')
			i++

		case 'S':
			// S -> X (SH) if -SH-, -SIO-, -SIA-
			// S -> S otherwise
			if nextChar == 'H' {
				result.WriteRune('X')
				i++
			} else if nextChar == 'I' && (nextNextChar == 'A' || nextNextChar == 'O') {
				result.WriteRune('X')
				i += 2
			} else {
				result.WriteRune('S')
			}
			i++

		case 'T':
			// T -> X if -TIA-, -TIO-
			// T -> 0 (TH) if -TH-
			// T -> silent if -TCH-
			if nextChar == 'I' && (nextNextChar == 'A' || nextNextChar == 'O') {
				result.WriteRune('X')
				i += 2
			} else if nextChar == 'H' {
				result.WriteRune('0') // Using '0' for TH sound
				i++
			} else if nextChar == 'C' && nextNextChar == 'H' {
				// TCH, silent T
				i++
			} else {
				result.WriteRune('T')
			}
			i++

		case 'V':
			result.WriteRune('F')
			i++

		case 'W':
			// W -> W if before vowel
			if isVowel(nextChar) {
				result.WriteRune('W')
			}
			i++

		case 'X':
			result.WriteString("KS")
			i++

		case 'Y':
			// Y -> Y if before vowel
			if isVowel(nextChar) {
				result.WriteRune('Y')
			}
			i++

		case 'Z':
			result.WriteRune('S')
			i++

		default:
			i++
		}
	}

	return result.String()
}

// RefinedSoundex encodes a string using the Refined Soundex algorithm.
// Refined Soundex uses 8 digits instead of 6 and separates similar sounds.
func RefinedSoundex(text string) string {
	if text == "" {
		return "0000"
	}

	cleaned := cleanString(text)
	if cleaned == "" {
		return "0000"
	}

	// Refined Soundex letter groups (8 groups)
	refinedGroups := map[rune]string{
		'B': "1", 'P': "1",
		'F': "2", 'V': "2",
		'C': "3", 'S': "3", 'K': "3", 'G': "3", 'J': "3", 'Q': "3", 'X': "3", 'Z': "3",
		'D': "4", 'T': "4",
		'L': "5",
		'M': "6", 'N': "6",
		'R': "7",
		'H': "8", 'W': "8",
	}

	// Keep the first letter
	first := rune(cleaned[0])
	result := strings.ToUpper(string(first))

	// Get code for first letter (skip H and W for first char)
	prevCode := ""
	if code, ok := refinedGroups[first]; ok && code != "8" {
		prevCode = code
	}

	// Process remaining letters
	for _, char := range cleaned[1:] {
		code := refinedGroups[char]
		if code != "" && code != "8" && code != prevCode {
			result += code
		}
		if code != "8" {
			prevCode = code
		}
	}

	// Pad with zeros or truncate to 4 characters
	for len(result) < 4 {
		result += "0"
	}
	return result[:4]
}

// NYSIIS encodes a string using the NYSIIS algorithm.
// New York State Identification and Intelligence System (NYSIIS) was
// developed for name matching in law enforcement databases.
func NYSIIS(text string) string {
	if text == "" {
		return ""
	}

	cleaned := cleanString(text)
	if cleaned == "" {
		return ""
	}

	// Convert to lowercase for processing
	cleaned = strings.ToLower(cleaned)

	// Step 1: First character transformations
	if len(cleaned) >= 2 {
		twoChar := cleaned[:2]
		if twoChar == "kn" || twoChar == "gn" || twoChar == "pn" || twoChar == "ae" || twoChar == "wr" {
			cleaned = cleaned[1:]
		} else if twoChar == "wh" {
			cleaned = "w" + cleaned[2:]
		} else if twoChar == "ng" {
			cleaned = "n" + cleaned[2:]
		}
	}

	// Step 2: Handle first character if 'M', 'K', etc.
	if len(cleaned) > 0 {
		if cleaned[0] == 'm' && len(cleaned) > 1 && isVowelLower(rune(cleaned[1])) {
			cleaned = "m" + cleaned[1:]
		} else if cleaned[0] == 'k' && len(cleaned) > 1 && cleaned[1] == 'n' {
			cleaned = "n" + cleaned[2:]
		}
	}

	// Step 3: Main transformations
	result := strings.Builder{}
	for i, char := range cleaned {
		var nextChar, prevChar rune
		if i+1 < len(cleaned) {
			nextChar = rune(cleaned[i+1])
		}
		if i > 0 {
			prevChar = rune(cleaned[i-1])
		}

		// A, E, I, O, U -> A
		if isVowelLower(char) {
			result.WriteRune('A')
			continue
		}

		switch char {
		case 'q':
			result.WriteRune('G')
		case 'z':
			result.WriteRune('S')
		case 'm':
			result.WriteRune('N')
		case 'k':
			if nextChar == 'n' {
				continue // Skip KN
			}
			result.WriteRune('C')
		case 'p':
			if nextChar == 'h' {
				result.WriteRune('F')
				cleaned = cleaned[:i+1] + cleaned[i+2:] // Skip next char
			} else {
				result.WriteRune('P')
			}
		case 'h':
			if prevChar != 0 && nextChar != 0 {
				if !isVowelLower(prevChar) || !isVowelLower(nextChar) {
					if !isVowelLower(prevChar) {
						result.WriteRune(unicode.ToUpper(prevChar))
					}
				} else {
					result.WriteRune('H')
				}
			} else {
				result.WriteRune('H')
			}
		case 'w':
			if isVowelLower(prevChar) {
				result.WriteRune(unicode.ToUpper(prevChar))
			} else {
				result.WriteRune('W')
			}
		default:
			result.WriteRune(unicode.ToUpper(char))
		}
	}

	// Step 4: Remove adjacent duplicates
	deduped := removeAdjacentDuplicates(result.String())

	// Step 5: Remove trailing S and A
	for len(deduped) > 0 && (deduped[len(deduped)-1] == 'S' || deduped[len(deduped)-1] == 'A') {
		deduped = deduped[:len(deduped)-1]
	}

	// Step 6: Ensure at least one character
	if deduped == "" {
		return string(unicode.ToUpper(rune(cleaned[0])))
	}

	// Pad to at least 4 characters or truncate to 6
	for len(deduped) < 4 {
		deduped += "A"
	}

	if len(deduped) > 6 {
		deduped = deduped[:6]
	}

	return deduped
}

// MatchRatingCodex encodes a string using the Match Rating Codex (MRC) algorithm.
// MRC was developed by the Ontario Provincial Police for name matching
// in criminal justice systems.
func MatchRatingCodex(text string) string {
	if text == "" {
		return ""
	}

	cleaned := cleanString(text)
	if cleaned == "" {
		return ""
	}

	// Step 1: Remove vowels
	result := strings.Builder{}
	for _, char := range cleaned {
		if !isVowel(char) {
			result.WriteRune(char)
		}
	}
	strResult := result.String()

	// Step 2: Remove consecutive duplicates
	strResult = removeAdjacentDuplicates(strResult)

	// Step 3: Keep first and last, remove duplicates in between
	if len(strResult) > 2 {
		first := rune(strResult[0])
		last := rune(strResult[len(strResult)-1])
		middle := strResult[1 : len(strResult)-1]

		newMiddle := strings.Builder{}
		prev := first
		for _, char := range middle {
			if char != prev {
				newMiddle.WriteRune(char)
			}
			prev = char
		}

		middleStr := newMiddle.String()
		if len(middleStr) > 0 && rune(middleStr[len(middleStr)-1]) == last {
			middleStr = middleStr[:len(middleStr)-1]
		}

		strResult = string(first) + middleStr + string(last)
	}

	// Step 4: Limit to 6 characters
	if len(strResult) > 6 {
		return strResult[:6]
	}
	return strResult
}

// PhoneticResult contains all phonetic encodings for a name.
type PhoneticResult struct {
	Soundex          string
	Metaphone        string
	RefinedSoundex   string
	NYSIIS           string
	MatchRatingCodex string
}

// EncodeAll encodes a string using all phonetic algorithms.
func EncodeAll(text string) PhoneticResult {
	return PhoneticResult{
		Soundex:          Soundex(text),
		Metaphone:        Metaphone(text),
		RefinedSoundex:   RefinedSoundex(text),
		NYSIIS:           NYSIIS(text),
		MatchRatingCodex: MatchRatingCodex(text),
	}
}

// PhoneticAlgorithm represents a phonetic encoding algorithm.
type PhoneticAlgorithm int

const (
	AlgorithmSoundex PhoneticAlgorithm = iota
	AlgorithmMetaphone
	AlgorithmRefinedSoundex
	AlgorithmNYSIIS
	AlgorithmMatchRatingCodex
)

// Encode encodes a string using the specified algorithm.
func (a PhoneticAlgorithm) Encode(text string) string {
	switch a {
	case AlgorithmSoundex:
		return Soundex(text)
	case AlgorithmMetaphone:
		return Metaphone(text)
	case AlgorithmRefinedSoundex:
		return RefinedSoundex(text)
	case AlgorithmNYSIIS:
		return NYSIIS(text)
	case AlgorithmMatchRatingCodex:
		return MatchRatingCodex(text)
	default:
		return ""
	}
}

// Match checks if two names match using the specified algorithm.
func (a PhoneticAlgorithm) Match(name1, name2 string) bool {
	return a.Encode(name1) == a.Encode(name2)
}

// PhoneticMatch checks if two names match using the specified algorithm.
func PhoneticMatch(name1, name2 string, algorithm PhoneticAlgorithm) bool {
	return algorithm.Match(name1, name2)
}

// PhoneticSimilarity calculates a similarity score between two names
// based on how many algorithms agree they match.
// Returns a score from 0.0 to 1.0.
func PhoneticSimilarity(name1, name2 string) float64 {
	algorithms := []PhoneticAlgorithm{
		AlgorithmSoundex,
		AlgorithmMetaphone,
		AlgorithmRefinedSoundex,
		AlgorithmNYSIIS,
		AlgorithmMatchRatingCodex,
	}

	matches := 0
	for _, alg := range algorithms {
		if alg.Match(name1, name2) {
			matches++
		}
	}

	return float64(matches) / float64(len(algorithms))
}

// PhoneticMatchResult represents a match result with similarity score.
type PhoneticMatchResult struct {
	Name       string
	Code       string
	Similarity float64
}

// FindMatches finds phonetic matches for a name from a list of candidates.
func FindMatches(name string, candidates []string, algorithm PhoneticAlgorithm, threshold float64) []PhoneticMatchResult {
	results := []PhoneticMatchResult{}
	nameCode := algorithm.Encode(name)

	for _, candidate := range candidates {
		candidateCode := algorithm.Encode(candidate)
		var similarity float64

		if nameCode == candidateCode {
			similarity = 1.0
		} else {
			// Use general similarity for double matching
			similarity = PhoneticSimilarity(name, candidate)
		}

		if similarity >= threshold {
			results = append(results, PhoneticMatchResult{
				Name:       candidate,
				Code:       candidateCode,
				Similarity: similarity,
			})
		}
	}

	// Sort by similarity descending
	for i := 0; i < len(results)-1; i++ {
		for j := i + 1; j < len(results); j++ {
			if results[j].Similarity > results[i].Similarity {
				results[i], results[j] = results[j], results[i]
			}
		}
	}

	return results
}

// BatchEncode encodes multiple names using a single algorithm.
func BatchEncode(names []string, algorithm PhoneticAlgorithm) map[string]string {
	result := make(map[string]string)
	for _, name := range names {
		result[name] = algorithm.Encode(name)
	}
	return result
}

// Helper functions

// cleanString removes non-alphabetic characters and converts to uppercase.
func cleanString(text string) string {
	result := strings.Builder{}
	for _, char := range text {
		if unicode.IsLetter(char) {
			result.WriteRune(unicode.ToUpper(char))
		}
	}
	return result.String()
}

// isVowel checks if a character is a vowel (uppercase).
func isVowel(char rune) bool {
	return char == 'A' || char == 'E' || char == 'I' || char == 'O' || char == 'U'
}

// isVowelLower checks if a character is a vowel (lowercase).
func isVowelLower(char rune) bool {
	return char == 'a' || char == 'e' || char == 'i' || char == 'o' || char == 'u'
}

// removeAdjacentDuplicates removes consecutive duplicate characters.
func removeAdjacentDuplicates(s string) string {
	if len(s) <= 1 {
		return s
	}

	result := strings.Builder{}
	prev := rune(s[0])
	result.WriteRune(prev)

	for _, char := range s[1:] {
		if char != prev {
			result.WriteRune(char)
			prev = char
		}
	}

	return result.String()
}