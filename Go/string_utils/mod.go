// Package string_utils provides comprehensive string manipulation utilities.
// Zero external dependencies - uses only Go standard library.
package string_utils

import (
	"math"
	"regexp"
	"strings"
	"unicode"
	"unicode/utf8"
)

// ==================== Case Conversion ====================

// ToCamelCase converts string to camelCase (lowercase first letter)
func ToCamelCase(s string) string {
	words := splitIntoWords(s)
	if len(words) == 0 {
		return ""
	}

	result := strings.ToLower(words[0])
	for i := 1; i < len(words); i++ {
		result += capitalizeFirst(words[i])
	}
	return result
}

// ToPascalCase converts string to PascalCase (capitalize each word)
func ToPascalCase(s string) string {
	words := splitIntoWords(s)
	if len(words) == 0 {
		return ""
	}

	result := ""
	for _, word := range words {
		result += capitalizeFirst(word)
	}
	return result
}

// ToSnakeCase converts string to snake_case
func ToSnakeCase(s string) string {
	words := splitIntoWords(s)
	if len(words) == 0 {
		return ""
	}

	result := strings.ToLower(words[0])
	for i := 1; i < len(words); i++ {
		result += "_" + strings.ToLower(words[i])
	}
	return result
}

// ToKebabCase converts string to kebab-case
func ToKebabCase(s string) string {
	words := splitIntoWords(s)
	if len(words) == 0 {
		return ""
	}

	result := strings.ToLower(words[0])
	for i := 1; i < len(words); i++ {
		result += "-" + strings.ToLower(words[i])
	}
	return result
}

// ToScreamingSnakeCase converts string to SCREAMING_SNAKE_CASE
func ToScreamingSnakeCase(s string) string {
	words := splitIntoWords(s)
	if len(words) == 0 {
		return ""
	}

	result := strings.ToUpper(words[0])
	for i := 1; i < len(words); i++ {
		result += "_" + strings.ToUpper(words[i])
	}
	return result
}

// ToTitleCase converts string to Title Case
func ToTitleCase(s string) string {
	words := splitIntoWords(s)
	if len(words) == 0 {
		return ""
	}

	result := ""
	for i, word := range words {
		if i > 0 {
			result += " "
		}
		result += capitalizeFirst(word)
	}
	return result
}

// splitIntoWords splits a string into words based on various delimiters and casing
func splitIntoWords(s string) []string {
	s = strings.TrimSpace(s)
	if s == "" {
		return nil
	}

	// Replace common separators with spaces
	s = strings.ReplaceAll(s, "_", " ")
	s = strings.ReplaceAll(s, "-", " ")
	s = strings.ReplaceAll(s, ".", " ")

	// Split camelCase and PascalCase
	var result []string
	var currentWord strings.Builder

	for i, r := range s {
		if unicode.IsSpace(r) {
			if currentWord.Len() > 0 {
				result = append(result, currentWord.String())
				currentWord.Reset()
			}
			continue
		}

		// Check if this is a word boundary
		if currentWord.Len() > 0 {
			lastRune, _ := utf8.DecodeLastRuneInString(currentWord.String())
			// Lowercase to uppercase boundary (camelCase)
			if unicode.IsLower(lastRune) && unicode.IsUpper(r) {
				result = append(result, currentWord.String())
				currentWord.Reset()
			}
			// Uppercase to lowercase boundary for acronyms (HTTPRequest -> HTTP, Request)
			if i > 0 {
				prevRune, _ := utf8.DecodeRuneInString(s[i-utf8.RuneLen(r):])
				if unicode.IsUpper(prevRune) && unicode.IsUpper(lastRune) && unicode.IsLower(r) {
					word := currentWord.String()
					if len(word) > 1 {
						result = append(result, word[:len(word)-1])
						currentWord.Reset()
						currentWord.WriteRune(lastRune)
					}
				}
			}
		}

		currentWord.WriteRune(r)
	}

	if currentWord.Len() > 0 {
		result = append(result, currentWord.String())
	}

	return result
}

func capitalizeFirst(s string) string {
	if s == "" {
		return ""
	}
	r, size := utf8.DecodeRuneInString(s)
	return string(unicode.ToUpper(r)) + strings.ToLower(s[size:])
}

// ==================== String Manipulation ====================

// Reverse reverses a string (handles Unicode properly)
func Reverse(s string) string {
	if s == "" {
		return ""
	}

	runes := []rune(s)
	for i, j := 0, len(runes)-1; i < j; i, j = i+1, j-1 {
		runes[i], runes[j] = runes[j], runes[i]
	}
	return string(runes)
}

// Truncate truncates a string to maxLen and adds suffix if truncated
func Truncate(s string, maxLen int, suffix string) string {
	if utf8.RuneCountInString(s) <= maxLen {
		return s
	}

	runes := []rune(s)
	suffixRunes := []rune(suffix)
	truncateAt := maxLen - len(suffixRunes)
	if truncateAt < 0 {
		truncateAt = 0
	}

	return string(runes[:truncateAt]) + suffix
}

// PadLeft pads string on the left with specified character
func PadLeft(s string, length int, padChar rune) string {
	currentLen := utf8.RuneCountInString(s)
	if currentLen >= length {
		return s
	}

	padding := strings.Repeat(string(padChar), length-currentLen)
	return padding + s
}

// PadRight pads string on the right with specified character
func PadRight(s string, length int, padChar rune) string {
	currentLen := utf8.RuneCountInString(s)
	if currentLen >= length {
		return s
	}

	padding := strings.Repeat(string(padChar), length-currentLen)
	return s + padding
}

// PadCenter centers string with specified character
func PadCenter(s string, length int, padChar rune) string {
	currentLen := utf8.RuneCountInString(s)
	if currentLen >= length {
		return s
	}

	totalPad := length - currentLen
	leftPad := totalPad / 2
	rightPad := totalPad - leftPad

	return strings.Repeat(string(padChar), leftPad) + s + strings.Repeat(string(padChar), rightPad)
}

// Repeat repeats string n times
func Repeat(s string, n int) string {
	if n <= 0 {
		return ""
	}
	return strings.Repeat(s, n)
}

// ==================== String Validation ====================

var (
	emailRegex    = regexp.MustCompile(`^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`)
	phoneRegex    = regexp.MustCompile(`^[\+]?[(]?[0-9]{1,4}[)]?[-\s\.]?[0-9]{1,4}[-\s\.]?[0-9]{1,9}$`)
	urlRegex      = regexp.MustCompile(`^https?://[^\s/$.?#].[^\s]*$`)
	uuidRegex     = regexp.MustCompile(`^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$`)
	ipv4Regex     = regexp.MustCompile(`^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$`)
	hexColorRegex = regexp.MustCompile(`^#?([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$`)
	slugRegex     = regexp.MustCompile(`^[a-z0-9]+(?:-[a-z0-9]+)*$`)
)

// IsEmail checks if string is a valid email
func IsEmail(s string) bool {
	return emailRegex.MatchString(s)
}

// IsPhone checks if string is a valid phone number
func IsPhone(s string) bool {
	return phoneRegex.MatchString(s)
}

// IsURL checks if string is a valid URL
func IsURL(s string) bool {
	return urlRegex.MatchString(s)
}

// IsUUID checks if string is a valid UUID
func IsUUID(s string) bool {
	return uuidRegex.MatchString(s)
}

// IsIPv4 checks if string is a valid IPv4 address
func IsIPv4(s string) bool {
	return ipv4Regex.MatchString(s)
}

// IsHexColor checks if string is a valid hex color
func IsHexColor(s string) bool {
	return hexColorRegex.MatchString(s)
}

// IsSlug checks if string is a valid URL slug
func IsSlug(s string) bool {
	return slugRegex.MatchString(s)
}

// IsEmpty checks if string is empty or whitespace only
func IsEmpty(s string) bool {
	return strings.TrimSpace(s) == ""
}

// IsAlpha checks if string contains only letters
func IsAlpha(s string) bool {
	if s == "" {
		return false
	}
	for _, r := range s {
		if !unicode.IsLetter(r) {
			return false
		}
	}
	return true
}

// IsAlphanumeric checks if string contains only letters and numbers
func IsAlphanumeric(s string) bool {
	if s == "" {
		return false
	}
	for _, r := range s {
		if !unicode.IsLetter(r) && !unicode.IsDigit(r) {
			return false
		}
	}
	return true
}

// IsNumeric checks if string contains only digits
func IsNumeric(s string) bool {
	if s == "" {
		return false
	}
	for _, r := range s {
		if !unicode.IsDigit(r) {
			return false
		}
	}
	return true
}

// IsASCII checks if string contains only ASCII characters
func IsASCII(s string) bool {
	for i := 0; i < len(s); i++ {
		if s[i] > 127 {
			return false
		}
	}
	return true
}

// IsLower checks if string is all lowercase
func IsLower(s string) bool {
	if s == "" {
		return false
	}
	for _, r := range s {
		if unicode.IsLetter(r) && !unicode.IsLower(r) {
			return false
		}
	}
	return true
}

// IsUpper checks if string is all uppercase
func IsUpper(s string) bool {
	if s == "" {
		return false
	}
	for _, r := range s {
		if unicode.IsLetter(r) && !unicode.IsUpper(r) {
			return false
		}
	}
	return true
}

// ==================== String Analysis ====================

// WordCount counts the number of words in a string
func WordCount(s string) int {
	words := strings.Fields(s)
	return len(words)
}

// CharCount counts characters in a string (handles Unicode)
func CharCount(s string) int {
	return utf8.RuneCountInString(s)
}

// ByteCount returns the byte length of a string
func ByteCount(s string) int {
	return len(s)
}

// LineCount counts the number of lines in a string
func LineCount(s string) int {
	if s == "" {
		return 0
	}
	return strings.Count(s, "\n") + 1
}

// Count counts occurrences of a substring
func Count(s, substr string) int {
	if substr == "" {
		return 0
	}
	return strings.Count(s, substr)
}

// Frequency returns a map of character frequencies
func Frequency(s string) map[rune]int {
	freq := make(map[rune]int)
	for _, r := range s {
		freq[r]++
	}
	return freq
}

// WordFrequency returns a map of word frequencies
func WordFrequency(s string) map[string]int {
	freq := make(map[string]int)
	words := strings.Fields(s)
	for _, word := range words {
		word = strings.ToLower(strings.TrimFunc(word, func(r rune) bool {
			return !unicode.IsLetter(r) && !unicode.IsDigit(r)
		}))
		if word != "" {
			freq[word]++
		}
	}
	return freq
}

// LongestWord returns the longest word in a string
func LongestWord(s string) string {
	words := strings.Fields(s)
	if len(words) == 0 {
		return ""
	}

	longest := words[0]
	for _, word := range words[1:] {
		if utf8.RuneCountInString(word) > utf8.RuneCountInString(longest) {
			longest = word
		}
	}
	return longest
}

// ShortestWord returns the shortest word in a string
func ShortestWord(s string) string {
	words := strings.Fields(s)
	if len(words) == 0 {
		return ""
	}

	shortest := words[0]
	for _, word := range words[1:] {
		if utf8.RuneCountInString(word) < utf8.RuneCountInString(shortest) {
			shortest = word
		}
	}
	return shortest
}

// ==================== String Similarity ====================

// LevenshteinDistance calculates the Levenshtein distance between two strings
func LevenshteinDistance(s1, s2 string) int {
	r1 := []rune(s1)
	r2 := []rune(s2)
	len1 := len(r1)
	len2 := len(r2)

	// Create matrix
	matrix := make([][]int, len1+1)
	for i := range matrix {
		matrix[i] = make([]int, len2+1)
	}

	// Initialize first column
	for i := 0; i <= len1; i++ {
		matrix[i][0] = i
	}

	// Initialize first row
	for j := 0; j <= len2; j++ {
		matrix[0][j] = j
	}

	// Fill in the rest
	for i := 1; i <= len1; i++ {
		for j := 1; j <= len2; j++ {
			cost := 0
			if r1[i-1] != r2[j-1] {
				cost = 1
			}
			matrix[i][j] = min3(
				matrix[i-1][j]+1,      // deletion
				matrix[i][j-1]+1,      // insertion
				matrix[i-1][j-1]+cost, // substitution
			)
		}
	}

	return matrix[len1][len2]
}

// Similarity returns a similarity ratio between 0 and 1
func Similarity(s1, s2 string) float64 {
	if s1 == "" && s2 == "" {
		return 1.0
	}
	if s1 == "" || s2 == "" {
		return 0.0
	}

	distance := LevenshteinDistance(s1, s2)
	maxLen := float64(max(utf8.RuneCountInString(s1), utf8.RuneCountInString(s2)))
	return 1.0 - float64(distance)/maxLen
}

// HammingDistance calculates the Hamming distance (strings must be equal length)
func HammingDistance(s1, s2 string) (int, bool) {
	r1 := []rune(s1)
	r2 := []rune(s2)

	if len(r1) != len(r2) {
		return 0, false
	}

	distance := 0
	for i := range r1 {
		if r1[i] != r2[i] {
			distance++
		}
	}
	return distance, true
}

// JaroSimilarity calculates the Jaro similarity between two strings
func JaroSimilarity(s1, s2 string) float64 {
	r1 := []rune(s1)
	r2 := []rune(s2)
	len1 := len(r1)
	len2 := len(r2)

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

	// Find matches
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

	// Count transpositions
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
		float64(matches-transpositions/2)/float64(matches)) / 3.0
}

// JaroWinklerSimilarity calculates Jaro-Winkler similarity
func JaroWinklerSimilarity(s1, s2 string) float64 {
	jaro := JaroSimilarity(s1, s2)

	// Calculate common prefix length (max 4)
	prefixLen := 0
	r1 := []rune(s1)
	r2 := []rune(s2)
	minLen := min(len(r1), len(r2))
	for i := 0; i < minLen && i < 4; i++ {
		if r1[i] == r2[i] {
			prefixLen++
		} else {
			break
		}
	}

	return jaro + float64(prefixLen)*0.1*(1-jaro)
}

// ==================== String Checks ====================

// Contains checks if string contains substring (case-insensitive)
func Contains(s, substr string, caseSensitive bool) bool {
	if caseSensitive {
		return strings.Contains(s, substr)
	}
	return strings.Contains(strings.ToLower(s), strings.ToLower(substr))
}

// ContainsAll checks if string contains all substrings
func ContainsAll(s string, substrs []string, caseSensitive bool) bool {
	for _, substr := range substrs {
		if !Contains(s, substr, caseSensitive) {
			return false
		}
	}
	return true
}

// ContainsAny checks if string contains any of the substrings
func ContainsAny(s string, substrs []string, caseSensitive bool) bool {
	for _, substr := range substrs {
		if Contains(s, substr, caseSensitive) {
			return true
		}
	}
	return false
}

// StartsWith checks if string starts with prefix (case-insensitive option)
func StartsWith(s, prefix string, caseSensitive bool) bool {
	if caseSensitive {
		return strings.HasPrefix(s, prefix)
	}
	return strings.HasPrefix(strings.ToLower(s), strings.ToLower(prefix))
}

// EndsWith checks if string ends with suffix (case-insensitive option)
func EndsWith(s, suffix string, caseSensitive bool) bool {
	if caseSensitive {
		return strings.HasSuffix(s, suffix)
	}
	return strings.HasSuffix(strings.ToLower(s), strings.ToLower(suffix))
}

// IsPalindrome checks if string is a palindrome
func IsPalindrome(s string) bool {
	// Remove non-alphanumeric characters and convert to lowercase
	var cleaned strings.Builder
	for _, r := range s {
		if unicode.IsLetter(r) || unicode.IsDigit(r) {
			cleaned.WriteRune(unicode.ToLower(r))
		}
	}
	clean := cleaned.String()

	// Check palindrome
	runes := []rune(clean)
	for i, j := 0, len(runes)-1; i < j; i, j = i+1, j-1 {
		if runes[i] != runes[j] {
			return false
		}
	}
	return true
}

// IsAnagram checks if two strings are anagrams
func IsAnagram(s1, s2 string) bool {
	// Normalize strings
	normalize := func(s string) string {
		var result strings.Builder
		for _, r := range s {
			if unicode.IsLetter(r) || unicode.IsDigit(r) {
				result.WriteRune(unicode.ToLower(r))
			}
		}
		return result.String()
	}

	n1 := normalize(s1)
	n2 := normalize(s2)

	if len(n1) != len(n2) {
		return false
	}

	freq := make(map[rune]int)
	for _, r := range n1 {
		freq[r]++
	}
	for _, r := range n2 {
		freq[r]--
		if freq[r] < 0 {
			return false
		}
	}
	return true
}

// IsPangram checks if string contains all letters of the alphabet
func IsPangram(s string) bool {
	letters := make(map[rune]bool)
	for _, r := range strings.ToLower(s) {
		if r >= 'a' && r <= 'z' {
			letters[r] = true
		}
	}
	return len(letters) == 26
}

// ==================== String Transformation ====================

// RemoveWhitespace removes all whitespace from string
func RemoveWhitespace(s string) string {
	var result strings.Builder
	for _, r := range s {
		if !unicode.IsSpace(r) {
			result.WriteRune(r)
		}
	}
	return result.String()
}

// RemoveAccents removes diacritical marks from string
func RemoveAccents(s string) string {
	var result strings.Builder
	for _, r := range s {
		// Simple accent removal for common cases
		switch r {
		case 'à', 'á', 'â', 'ã', 'ä', 'å':
			result.WriteRune('a')
		case 'À', 'Á', 'Â', 'Ã', 'Ä', 'Å':
			result.WriteRune('A')
		case 'è', 'é', 'ê', 'ë':
			result.WriteRune('e')
		case 'È', 'É', 'Ê', 'Ë':
			result.WriteRune('E')
		case 'ì', 'í', 'î', 'ï':
			result.WriteRune('i')
		case 'Ì', 'Í', 'Î', 'Ï':
			result.WriteRune('I')
		case 'ò', 'ó', 'ô', 'õ', 'ö':
			result.WriteRune('o')
		case 'Ò', 'Ó', 'Ô', 'Õ', 'Ö':
			result.WriteRune('O')
		case 'ù', 'ú', 'û', 'ü':
			result.WriteRune('u')
		case 'Ù', 'Ú', 'Û', 'Ü':
			result.WriteRune('U')
		case 'ý', 'ÿ':
			result.WriteRune('y')
		case 'Ý':
			result.WriteRune('Y')
		case 'ç':
			result.WriteRune('c')
		case 'Ç':
			result.WriteRune('C')
		case 'ñ':
			result.WriteRune('n')
		case 'Ñ':
			result.WriteRune('N')
		case 'ß':
			result.WriteString("ss")
		default:
			result.WriteRune(r)
		}
	}
	return result.String()
}

// Mask masks a string, showing only first n and last m characters
func Mask(s string, showFirst, showLast int, maskChar rune) string {
	r := []rune(s)
	length := len(r)

	if length <= showFirst+showLast {
		return strings.Repeat(string(maskChar), length)
	}

	result := string(r[:showFirst])
	result += strings.Repeat(string(maskChar), length-showFirst-showLast)
	result += string(r[length-showLast:])

	return result
}

// MaskEmail masks an email address
func MaskEmail(email string, maskChar rune) string {
	atIndex := strings.Index(email, "@")
	if atIndex == -1 {
		return Mask(email, 1, 2, maskChar)
	}

	localPart := email[:atIndex]
	domain := email[atIndex:]

	if len(localPart) <= 2 {
		return string(localPart[0]) + strings.Repeat(string(maskChar), len(localPart)-1) + domain
	}

	return string(localPart[0]) + strings.Repeat(string(maskChar), len(localPart)-2) + string(localPart[len(localPart)-1]) + domain
}

// MaskPhone masks a phone number
func MaskPhone(phone string, maskChar rune) string {
	// Extract digits only
	var digits strings.Builder
	for _, r := range phone {
		if unicode.IsDigit(r) {
			digits.WriteRune(r)
		}
	}

	d := digits.String()
	if len(d) <= 4 {
		return strings.Repeat(string(maskChar), len(d))
	}

	// Show last 4 digits
	return strings.Repeat(string(maskChar), len(d)-4) + d[len(d)-4:]
}

// CamelCaseToSnakeCase is an alias for ToSnakeCase
func CamelCaseToSnakeCase(s string) string {
	return ToSnakeCase(s)
}

// SnakeCaseToCamelCase is an alias for ToCamelCase
func SnakeCaseToCamelCase(s string) string {
	return ToCamelCase(s)
}

// Capitalize capitalizes the first character of each word
func Capitalize(s string) string {
	return ToTitleCase(s)
}

// CapitalizeFirst capitalizes only the first character of the string
func CapitalizeFirst(s string) string {
	if s == "" {
		return ""
	}
	r, size := utf8.DecodeRuneInString(s)
	return string(unicode.ToUpper(r)) + s[size:]
}

// Uncapitalize makes the first character lowercase
func Uncapitalize(s string) string {
	if s == "" {
		return ""
	}
	r, size := utf8.DecodeRuneInString(s)
	return string(unicode.ToLower(r)) + s[size:]
}

// SwapCase swaps the case of each character
func SwapCase(s string) string {
	var result strings.Builder
	for _, r := range s {
		if unicode.IsUpper(r) {
			result.WriteRune(unicode.ToLower(r))
		} else if unicode.IsLower(r) {
			result.WriteRune(unicode.ToUpper(r))
		} else {
			result.WriteRune(r)
		}
	}
	return result.String()
}

// ==================== String Utilities ====================

// Substring returns substring from start to end (handles Unicode)
func Substring(s string, start, end int) string {
	runes := []rune(s)
	if start < 0 {
		start = 0
	}
	if end > len(runes) {
		end = len(runes)
	}
	if start >= end {
		return ""
	}
	return string(runes[start:end])
}

// Left returns the left n characters of a string
func Left(s string, n int) string {
	runes := []rune(s)
	if n >= len(runes) {
		return s
	}
	if n <= 0 {
		return ""
	}
	return string(runes[:n])
}

// Right returns the right n characters of a string
func Right(s string, n int) string {
	runes := []rune(s)
	if n >= len(runes) {
		return s
	}
	if n <= 0 {
		return ""
	}
	return string(runes[len(runes)-n:])
}

// SplitLines splits a string into lines
func SplitLines(s string) []string {
	if s == "" {
		return nil
	}
	return strings.Split(strings.TrimRight(s, "\n"), "\n")
}

// Chunk splits a string into chunks of specified size
func Chunk(s string, size int) []string {
	if size <= 0 {
		return nil
	}

	runes := []rune(s)
	if len(runes) == 0 {
		return nil
	}

	var result []string
	for i := 0; i < len(runes); i += size {
		end := i + size
		if end > len(runes) {
			end = len(runes)
		}
		result = append(result, string(runes[i:end]))
	}
	return result
}

// Template replaces placeholders in format ${key} with values
func Template(template string, values map[string]string) string {
	result := template
	for key, value := range values {
		placeholder := "${" + key + "}"
		result = strings.ReplaceAll(result, placeholder, value)
	}
	return result
}

// ==================== Helper Functions ====================

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

func min3(a, b, c int) int {
	return min(min(a, b), c)
}

// ==================== Fuzzy Matching ====================

// FuzzyMatch checks if pattern fuzzy matches string (allowing typos)
func FuzzyMatch(s, pattern string) bool {
	s = strings.ToLower(s)
	pattern = strings.ToLower(pattern)
	
	sIdx := 0
	pIdx := 0

	for sIdx < len(s) && pIdx < len(pattern) {
		if s[sIdx] == pattern[pIdx] {
			pIdx++
		}
		sIdx++
	}

	return pIdx == len(pattern)
}

// FuzzyMatchScore returns a score for fuzzy match (higher is better)
func FuzzyMatchScore(s, pattern string) int {
	s = strings.ToLower(s)
	pattern = strings.ToLower(pattern)
	
	score := 0
	sIdx := 0
	pIdx := 0
	lastMatchIdx := -1

	for sIdx < len(s) && pIdx < len(pattern) {
		if s[sIdx] == pattern[pIdx] {
			// Bonus for consecutive matches
			if lastMatchIdx == sIdx-1 {
				score += 10
			}
			// Bonus for matching at word boundaries
			if sIdx == 0 || (sIdx > 0 && (s[sIdx-1] == ' ' || s[sIdx-1] == '_' || s[sIdx-1] == '-')) {
				score += 15
			} else {
				score += 5
			}
			lastMatchIdx = sIdx
			pIdx++
		}
		sIdx++
	}

	if pIdx < len(pattern) {
		return 0 // Not all pattern chars matched
	}

	// Bonus for shorter strings (more precise match)
	score += max(0, 20-(len(s)-len(pattern)))

	return score
}

// FindBestMatch finds the best matching string from a list
func FindBestMatch(s string, candidates []string) (bestMatch string, score int) {
	bestScore := math.MinInt
	var best string

	for _, candidate := range candidates {
		candidateScore := FuzzyMatchScore(candidate, s)
		if candidateScore > bestScore {
			bestScore = candidateScore
			best = candidate
		}
	}

	return best, bestScore
}