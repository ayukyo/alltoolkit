// Package case_utils provides utilities for converting between different string case formats.
// Supports camelCase, PascalCase, snake_case, kebab-case, SCREAMING_SNAKE_CASE, and more.
package case_utils

import (
	"strings"
	"unicode"
)

// CaseType represents different string case formats
type CaseType int

const (
	CaseUnknown CaseType = iota
	CaseCamel           // camelCase
	CasePascal          // PascalCase
	CaseSnake           // snake_case
	CaseKebab           // kebab-case
	CaseScreamingSnake  // SCREAMING_SNAKE_CASE
	CaseUpper           // UPPERCASE
	CaseLower           // lowercase
	CaseTitle           // Title Case
)

// String returns the string representation of CaseType
func (ct CaseType) String() string {
	switch ct {
	case CaseCamel:
		return "camelCase"
	case CasePascal:
		return "PascalCase"
	case CaseSnake:
		return "snake_case"
	case CaseKebab:
		return "kebab-case"
	case CaseScreamingSnake:
		return "SCREAMING_SNAKE_CASE"
	case CaseUpper:
		return "UPPERCASE"
	case CaseLower:
		return "lowercase"
	case CaseTitle:
		return "Title Case"
	default:
		return "unknown"
	}
}

// ToCamelCase converts a string to camelCase
// Examples: "hello_world" -> "helloWorld", "HelloWorld" -> "helloWorld"
func ToCamelCase(s string) string {
	if s == "" {
		return s
	}

	// Split by common separators
	words := splitWords(s)
	if len(words) == 0 {
		return s
	}

	result := strings.ToLower(words[0])
	for i := 1; i < len(words); i++ {
		result += capitalize(strings.ToLower(words[i]))
	}

	return result
}

// ToPascalCase converts a string to PascalCase
// Examples: "hello_world" -> "HelloWorld", "hello-world" -> "HelloWorld"
func ToPascalCase(s string) string {
	if s == "" {
		return s
	}

	words := splitWords(s)
	if len(words) == 0 {
		return s
	}

	result := ""
	for _, word := range words {
		result += capitalize(strings.ToLower(word))
	}

	return result
}

// ToSnakeCase converts a string to snake_case
// Examples: "HelloWorld" -> "hello_world", "hello-world" -> "hello_world"
func ToSnakeCase(s string) string {
	if s == "" {
		return s
	}

	words := splitWords(s)
	return strings.Join(toLowerSlice(words), "_")
}

// ToKebabCase converts a string to kebab-case
// Examples: "HelloWorld" -> "hello-world", "hello_world" -> "hello-world"
func ToKebabCase(s string) string {
	if s == "" {
		return s
	}

	words := splitWords(s)
	return strings.Join(toLowerSlice(words), "-")
}

// ToScreamingSnakeCase converts a string to SCREAMING_SNAKE_CASE
// Examples: "helloWorld" -> "HELLO_WORLD", "hello-world" -> "HELLO_WORLD"
func ToScreamingSnakeCase(s string) string {
	if s == "" {
		return s
	}

	words := splitWords(s)
	return strings.Join(toUpperSlice(words), "_")
}

// ToUpperCase converts a string to UPPERCASE (no separators)
// Examples: "helloWorld" -> "HELLOWORLD", "hello_world" -> "HELLOWORLD"
func ToUpperCase(s string) string {
	words := splitWords(s)
	return strings.Join(toUpperSlice(words), "")
}

// ToLowerCase converts a string to lowercase (no separators)
// Examples: "HelloWorld" -> "helloworld", "HELLO_WORLD" -> "helloworld"
func ToLowerCase(s string) string {
	words := splitWords(s)
	return strings.Join(toLowerSlice(words), "")
}

// ToTitleCase converts a string to Title Case (with spaces)
// Examples: "hello_world" -> "Hello World", "helloWorld" -> "Hello World"
func ToTitleCase(s string) string {
	if s == "" {
		return s
	}

	words := splitWords(s)
	result := ""
	for i, word := range words {
		if i > 0 {
			result += " "
		}
		result += capitalize(strings.ToLower(word))
	}

	return result
}

// ToSentenceCase converts a string to Sentence case (first letter capitalized, spaces between words)
// Examples: "hello_world" -> "Hello world", "helloWorld" -> "Hello world"
func ToSentenceCase(s string) string {
	if s == "" {
		return s
	}

	words := splitWords(s)
	if len(words) == 0 {
		return s
	}

	result := capitalize(strings.ToLower(words[0]))
	for i := 1; i < len(words); i++ {
		result += " " + strings.ToLower(words[i])
	}

	return result
}

// ToConstantCase converts a string to CONSTANT_CASE (same as SCREAMING_SNAKE_CASE)
// Examples: "helloWorld" -> "HELLO_WORLD"
func ToConstantCase(s string) string {
	return ToScreamingSnakeCase(s)
}

// ToDotCase converts a string to dot.case
// Examples: "helloWorld" -> "hello.world", "HelloWorld" -> "hello.world"
func ToDotCase(s string) string {
	if s == "" {
		return s
	}

	words := splitWords(s)
	return strings.Join(toLowerSlice(words), ".")
}

// ToPathCase converts a string to path/case
// Examples: "helloWorld" -> "hello/world"
func ToPathCase(s string) string {
	if s == "" {
		return s
	}

	words := splitWords(s)
	return strings.Join(toLowerSlice(words), "/")
}

// ToTrainCase converts a string to Train-Case
// Examples: "helloWorld" -> "Hello-World"
func ToTrainCase(s string) string {
	if s == "" {
		return s
	}

	words := splitWords(s)
	result := ""
	for i, word := range words {
		if i > 0 {
			result += "-"
		}
		result += capitalize(strings.ToLower(word))
	}

	return result
}

// DetectCase attempts to detect the case type of a string
func DetectCase(s string) CaseType {
	if s == "" {
		return CaseUnknown
	}

	hasUnderscore := strings.Contains(s, "_")
	hasDash := strings.Contains(s, "-")
	hasUpper := hasUpperCase(s)
	hasLower := hasLowerCase(s)
	allUpper := s == strings.ToUpper(s) && hasLower == false
	allLower := s == strings.ToLower(s) && hasUpper == false

	// Check for SCREAMING_SNAKE_CASE
	if hasUnderscore && allUpper {
		return CaseScreamingSnake
	}

	// Check for snake_case
	if hasUnderscore && allLower {
		return CaseSnake
	}

	// Check for kebab-case
	if hasDash && allLower {
		return CaseKebab
	}

	// Check for UPPERCASE
	if allUpper && !hasUnderscore && !hasDash {
		return CaseUpper
	}

	// Check for lowercase
	if allLower && !hasUnderscore && !hasDash {
		return CaseLower
	}

	// Check for Title Case (spaces between words, each word capitalized)
	if strings.Contains(s, " ") {
		words := strings.Split(s, " ")
		allTitle := true
		for _, word := range words {
			if len(word) > 0 && !unicode.IsUpper(rune(word[0])) {
				allTitle = false
				break
			}
		}
		if allTitle {
			return CaseTitle
		}
	}

	// Check for camelCase or PascalCase
	if hasUpper && !hasUnderscore && !hasDash {
		if unicode.IsUpper(rune(s[0])) {
			return CasePascal
		}
		return CaseCamel
	}

	return CaseUnknown
}

// Convert converts a string from one case type to another
func Convert(s string, to CaseType) string {
	switch to {
	case CaseCamel:
		return ToCamelCase(s)
	case CasePascal:
		return ToPascalCase(s)
	case CaseSnake:
		return ToSnakeCase(s)
	case CaseKebab:
		return ToKebabCase(s)
	case CaseScreamingSnake:
		return ToScreamingSnakeCase(s)
	case CaseUpper:
		return ToUpperCase(s)
	case CaseLower:
		return ToLowerCase(s)
	case CaseTitle:
		return ToTitleCase(s)
	default:
		return s
	}
}

// AutoConvert automatically detects the input case and converts to the target case
func AutoConvert(s string, to CaseType) string {
	return Convert(s, to)
}

// splitWords splits a string into words based on various delimiters and case transitions
func splitWords(s string) []string {
	if s == "" {
		return nil
	}

	// Replace common separators with spaces
	s = strings.ReplaceAll(s, "_", " ")
	s = strings.ReplaceAll(s, "-", " ")
	s = strings.ReplaceAll(s, ".", " ")
	s = strings.ReplaceAll(s, "/", " ")

	var words []string
	var currentWord strings.Builder
	runes := []rune(s)

	for i, r := range runes {
		if r == ' ' {
			if currentWord.Len() > 0 {
				words = append(words, currentWord.String())
				currentWord.Reset()
			}
			continue
		}

		// Handle case transitions
		if i > 0 && unicode.IsUpper(r) {
			prevRune := runes[i-1]
			shouldSplit := false

			// Transition from lower to upper (helloWorld -> hello, World)
			if unicode.IsLower(prevRune) {
				shouldSplit = true
			} else if unicode.IsUpper(prevRune) && i < len(runes)-1 {
				// Acronym transition: last upper before lower (HTMLParser -> HTML, Parser)
				// Split when we have consecutive uppers followed by a lower
				nextRune := runes[i+1]
				if unicode.IsLower(nextRune) {
					shouldSplit = true
				}
			}

			if shouldSplit && currentWord.Len() > 0 {
				words = append(words, currentWord.String())
				currentWord.Reset()
			}
		}

		currentWord.WriteRune(r)
	}

	if currentWord.Len() > 0 {
		words = append(words, currentWord.String())
	}

	return words
}

// capitalize capitalizes the first letter of a string
func capitalize(s string) string {
	if s == "" {
		return s
	}
	runes := []rune(s)
	runes[0] = unicode.ToUpper(runes[0])
	return string(runes)
}

// hasUpperCase checks if string has any uppercase letters
func hasUpperCase(s string) bool {
	for _, r := range s {
		if unicode.IsUpper(r) {
			return true
		}
	}
	return false
}

// hasLowerCase checks if string has any lowercase letters
func hasLowerCase(s string) bool {
	for _, r := range s {
		if unicode.IsLower(r) {
			return true
		}
	}
	return false
}

// toLowerSlice converts all strings in a slice to lowercase
func toLowerSlice(words []string) []string {
	result := make([]string, len(words))
	for i, word := range words {
		result[i] = strings.ToLower(word)
	}
	return result
}

// toUpperSlice converts all strings in a slice to uppercase
func toUpperSlice(words []string) []string {
	result := make([]string, len(words))
	for i, word := range words {
		result[i] = strings.ToUpper(word)
	}
	return result
}