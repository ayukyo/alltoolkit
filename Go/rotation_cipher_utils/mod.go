// Package rotationcipher provides rotation cipher utilities with zero external dependencies.
// Includes Caesar cipher, ROT13, ROT47, ROT5, ROT18, Atbash, Vigenère, and Affine ciphers.
package rotationcipher

import (
	"strings"
	"unicode"
)

// CipherResult holds the result of a cipher operation.
type CipherResult struct {
	Original string
	Result   string
	Shift    int
	Method   string
}

// BruteForceResult holds results from brute force attack.
type BruteForceResult struct {
	Shift     int
	Decrypted string
	Score     float64
}

// English letter frequencies (approximate percentages)
var englishLetterFreq = map[rune]float64{
	'e': 12.7, 't': 9.1, 'a': 8.2, 'o': 7.5, 'i': 7.0, 'n': 6.7,
	's': 6.3, 'h': 6.1, 'r': 6.0, 'd': 4.3, 'l': 4.0, 'c': 2.8,
	'u': 2.8, 'm': 2.4, 'w': 2.4, 'f': 2.2, 'g': 2.0, 'y': 2.0,
	'p': 1.9, 'b': 1.5, 'v': 1.0, 'k': 0.8, 'j': 0.15, 'x': 0.15,
	'q': 0.10, 'z': 0.07,
}

// Common English patterns for scoring
var commonPatterns = []string{"the", "and", "ing", "tion", "ed", "er", "ly"}
var unusualCombos = []string{"qx", "qz", "vj", "wz", "zx", "zz", "qq"}

// CaesarCipher applies Caesar cipher rotation to text.
// Preserves case and non-alphabetic characters.
func CaesarCipher(text string, shift int) string {
	// Normalize shift to 0-25 range
	shift = ((shift % 26) + 26) % 26

	var result strings.Builder
	result.Grow(len(text))

	for _, char := range text {
		if unicode.IsUpper(char) {
			// Uppercase letter
			rotated := 'A' + rune((int(char-'A')+shift)%26)
			result.WriteRune(rotated)
		} else if unicode.IsLower(char) {
			// Lowercase letter
			rotated := 'a' + rune((int(char-'a')+shift)%26)
			result.WriteRune(rotated)
		} else {
			// Non-alphabetic character
			result.WriteRune(char)
		}
	}

	return result.String()
}

// ROT13 applies ROT13 cipher (rotate by 13 positions).
// ROT13 is its own inverse: ROT13(ROT13(text)) == text.
func ROT13(text string) string {
	return CaesarCipher(text, 13)
}

// ROT5 applies ROT5 cipher (rotate digits by 5 positions).
// ROT5 is its own inverse for digits 0-9.
func ROT5(text string) string {
	var result strings.Builder
	result.Grow(len(text))

	for _, char := range text {
		if char >= '0' && char <= '9' {
			rotated := '0' + rune((int(char-'0')+5)%10)
			result.WriteRune(rotated)
		} else {
			result.WriteRune(char)
		}
	}

	return result.String()
}

// ROT18 applies ROT18 cipher (combination of ROT13 + ROT5).
// Letters are rotated by 13, digits by 5.
// ROT18 is its own inverse.
func ROT18(text string) string {
	var result strings.Builder
	result.Grow(len(text))

	for _, char := range text {
		if unicode.IsUpper(char) {
			rotated := 'A' + rune((int(char-'A')+13)%26)
			result.WriteRune(rotated)
		} else if unicode.IsLower(char) {
			rotated := 'a' + rune((int(char-'a')+13)%26)
			result.WriteRune(rotated)
		} else if char >= '0' && char <= '9' {
			rotated := '0' + rune((int(char-'0')+5)%10)
			result.WriteRune(rotated)
		} else {
			result.WriteRune(char)
		}
	}

	return result.String()
}

// ROT47 applies ROT47 cipher (rotate ASCII printable characters by 47).
// Uses the full range of ASCII printable characters (94 chars).
// ROT47 is its own inverse.
func ROT47(text string) string {
	var result strings.Builder
	result.Grow(len(text))

	for _, char := range text {
		if char >= 33 && char <= 126 {
			// Printable ASCII range: 33 (!) to 126 (~)
			rotated := rune(33 + ((int(char-33) + 47) % 94))
			result.WriteRune(rotated)
		} else {
			result.WriteRune(char)
		}
	}

	return result.String()
}

// AtbashCipher applies Atbash cipher (A↔Z, B↔Y, etc.).
// Atbash is its own inverse.
func AtbashCipher(text string) string {
	var result strings.Builder
	result.Grow(len(text))

	for _, char := range text {
		if unicode.IsUpper(char) {
			// A=0, Z=25 -> rotated = 25 - original
			rotated := 'Z' - (char - 'A')
			result.WriteRune(rotated)
		} else if unicode.IsLower(char) {
			rotated := 'z' - (char - 'a')
			result.WriteRune(rotated)
		} else {
			result.WriteRune(char)
		}
	}

	return result.String()
}

// VigenereCipher applies Vigenère cipher (polyalphabetic substitution).
// Key must contain at least one letter.
func VigenereCipher(text, key string, decrypt bool) string {
	if key == "" {
		return text
	}

	// Clean key: keep only letters, convert to uppercase
	keyRunes := make([]rune, 0, len(key))
	for _, c := range key {
		if unicode.IsLetter(c) {
			keyRunes = append(keyRunes, unicode.ToUpper(c))
		}
	}

	if len(keyRunes) == 0 {
		return text
	}

	var result strings.Builder
	result.Grow(len(text))
	keyIndex := 0

	for _, char := range text {
		if unicode.IsLetter(char) {
			shift := int(keyRunes[keyIndex%len(keyRunes)] - 'A')
			if decrypt {
				shift = -shift
			}

			if unicode.IsUpper(char) {
				rotated := 'A' + rune((int(char-'A')+shift+26)%26)
				result.WriteRune(rotated)
			} else {
				rotated := 'a' + rune((int(char-'a')+shift+26)%26)
				result.WriteRune(rotated)
			}
			keyIndex++
		} else {
			result.WriteRune(char)
		}
	}

	return result.String()
}

// AffineCipher applies Affine cipher (E(x) = (ax + b) mod 26).
// Parameter 'a' must be coprime with 26 (no common factors).
func AffineCipher(text string, a, b int, decrypt bool) string {
	// Check if 'a' is coprime with 26
	if a%2 == 0 || a%13 == 0 {
		return text // Invalid 'a', return unchanged
	}

	var result strings.Builder
	result.Grow(len(text))

	var aInv int
	if decrypt {
		aInv = modInverse(a, 26)
	}

	for _, char := range text {
		if unicode.IsUpper(char) {
			x := int(char - 'A')
			var y int
			if decrypt {
				y = (aInv * (x - b + 26)) % 26
			} else {
				y = (a*x + b) % 26
			}
			result.WriteRune(rune('A' + y))
		} else if unicode.IsLower(char) {
			x := int(char - 'a')
			var y int
			if decrypt {
				y = (aInv * (x - b + 26)) % 26
			} else {
				y = (a*x + b) % 26
			}
			result.WriteRune(rune('a' + y))
		} else {
			result.WriteRune(char)
		}
	}

	return result.String()
}

// modInverse finds modular multiplicative inverse using extended Euclidean algorithm.
func modInverse(a, m int) int {
	a = a % m
	for x := 1; x < m; x++ {
		if (a*x)%m == 1 {
			return x
		}
	}
	return 1
}

// CaesarEncrypt encrypts text using Caesar cipher and returns a CipherResult.
func CaesarEncrypt(text string, shift int) CipherResult {
	return CipherResult{
		Original: text,
		Result:   CaesarCipher(text, shift),
		Shift:    shift,
		Method:   "caesar",
	}
}

// CaesarDecrypt decrypts text using Caesar cipher and returns a CipherResult.
func CaesarDecrypt(text string, shift int) CipherResult {
	return CipherResult{
		Original: text,
		Result:   CaesarCipher(text, -shift),
		Shift:    -shift,
		Method:   "caesar",
	}
}

// BruteForceCaesar attempts all 25 possible shifts on Caesar cipher.
// Returns results sorted by score (highest first).
func BruteForceCaesar(ciphertext string, topN int) []BruteForceResult {
	results := make([]BruteForceResult, 25)

	for shift := 1; shift <= 25; shift++ {
		decrypted := CaesarCipher(ciphertext, -shift)
		score := scoreText(decrypted)
		results[shift-1] = BruteForceResult{
			Shift:     shift,
			Decrypted: decrypted,
			Score:     score,
		}
	}

	// Sort by score descending (bubble sort for simplicity)
	for i := 0; i < len(results)-1; i++ {
		for j := 0; j < len(results)-i-1; j++ {
			if results[j].Score < results[j+1].Score {
				results[j], results[j+1] = results[j+1], results[j]
			}
		}
	}

	if topN > 0 && topN < len(results) {
		return results[:topN]
	}
	return results
}

// scoreText scores text based on likelihood of being English.
func scoreText(text string) float64 {
	text = strings.ToLower(text)

	// Count letter frequencies
	letterCount := make(map[rune]int)
	totalLetters := 0

	for _, char := range text {
		if char >= 'a' && char <= 'z' {
			letterCount[char]++
			totalLetters++
		}
	}

	if totalLetters == 0 {
		return 0.0
	}

	// Calculate chi-squared-like score against expected frequencies
	invTotal := 100.0 / float64(totalLetters)
	var score float64

	for letter, expectedFreq := range englishLetterFreq {
		actualCount := letterCount[letter]
		actualFreq := float64(actualCount) * invTotal
		score -= absFloat(actualFreq - expectedFreq)
	}

	// Bonus for common English patterns
	for _, pattern := range commonPatterns {
		if strings.Contains(text, pattern) {
			score += 5
		}
	}

	// Penalty for unusual letter combinations
	for _, combo := range unusualCombos {
		if strings.Contains(text, combo) {
			score -= 10
		}
	}

	return score
}

// absFloat returns absolute value of a float64.
func absFloat(x float64) float64 {
	if x < 0 {
		return -x
	}
	return x
}

// FrequencyAnalysis performs frequency analysis on text.
// Returns a map of letter frequencies as percentages.
func FrequencyAnalysis(text string) map[rune]float64 {
	letterCount := make(map[rune]int)
	totalLetters := 0

	for _, char := range text {
		lower := unicode.ToLower(char)
		if lower >= 'a' && lower <= 'z' {
			letterCount[lower]++
			totalLetters++
		}
	}

	if totalLetters == 0 {
		return map[rune]float64{}
	}

	frequencies := make(map[rune]float64)
	for letter, count := range letterCount {
		frequencies[letter] = (float64(count) / float64(totalLetters)) * 100
	}

	return frequencies
}

// DetectCaesarShift detects the most likely Caesar cipher shift.
func DetectCaesarShift(ciphertext string) int {
	results := BruteForceCaesar(ciphertext, 1)
	if len(results) > 0 {
		return results[0].Shift
	}
	return 0
}

// MultiROT applies multiple ROT operations in sequence.
func MultiROT(text string, rotations []int) string {
	result := text
	for _, rot := range rotations {
		result = CaesarCipher(result, rot)
	}
	return result
}

// ROTAll applies all standard ROT ciphers and returns results as a map.
func ROTAll(text string) map[string]string {
	return map[string]string{
		"rot5":   ROT5(text),
		"rot13":  ROT13(text),
		"rot18":  ROT18(text),
		"rot47":  ROT47(text),
		"atbash": AtbashCipher(text),
	}
}

// ShiftToROTName converts shift amount to ROT naming convention.
func ShiftToROTName(shift int) string {
	normalized := ((shift % 26) + 26) % 26
	if normalized == 0 {
		return "ROT0 (no shift)"
	}
	return strings.ToUpper("ROT" + string(rune('0'+normalized/10)) + string(rune('0'+normalized%10)))
}

// IsROT13Encoded heuristically checks if text might be ROT13 encoded.
func IsROT13Encoded(text string, threshold float64) bool {
	if len(text) == 0 {
		return false
	}

	// Count vowels
	vowelCount := 0
	letterCount := 0
	nRCount := 0

	for _, char := range text {
		lower := unicode.ToLower(char)
		if unicode.IsLetter(char) {
			letterCount++
			if lower == 'a' || lower == 'e' || lower == 'i' || lower == 'o' || lower == 'u' {
				vowelCount++
			}
			if lower == 'n' || lower == 'r' {
				nRCount++
			}
		}
	}

	if letterCount == 0 {
		return false
	}

	vowelRatio := float64(vowelCount) / float64(letterCount)
	nRRatio := float64(nRCount) / float64(letterCount)

	// English text typically has ~38% vowels
	// ROT13 preserves vowel distribution differently
	return vowelRatio < threshold || nRRatio > 0.2
}

// CaesarCipherWithAlphabet applies Caesar cipher with a custom alphabet.
func CaesarCipherWithAlphabet(text, alphabet string, shift int) string {
	if alphabet == "" {
		return CaesarCipher(text, shift)
	}

	alphabetRunes := []rune(alphabet)
	alphabetLen := len(alphabetRunes)
	alphabetLower := strings.ToLower(alphabet)

	var result strings.Builder
	result.Grow(len(text))

	for _, char := range text {
		found := false
		for i, a := range alphabetRunes {
			if char == a {
				result.WriteRune(alphabetRunes[(i+shift+alphabetLen)%alphabetLen])
				found = true
				break
			}
		}
		if !found {
			lowerChar := unicode.ToLower(char)
			for i, a := range alphabetLower {
				if lowerChar == a {
					shiftedIdx := (i + shift + alphabetLen) % alphabetLen
					shiftedRune := []rune(strings.ToLower(alphabet))[shiftedIdx]
					result.WriteRune(shiftedRune)
					found = true
					break
				}
			}
		}
		if !found {
			result.WriteRune(char)
		}
	}

	return result.String()
}