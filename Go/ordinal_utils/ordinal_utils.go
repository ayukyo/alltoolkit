// Package ordinal_utils provides utilities for converting numbers to ordinal numbers.
// Ordinal numbers indicate position in a sequence (1st, 2nd, 3rd, 4th, etc.)
package ordinal_utils

import (
	"errors"
	"fmt"
	"regexp"
	"strconv"
	"strings"
)

// Language represents a supported language for ordinal conversion
type Language string

const (
	English Language = "en"
	Spanish Language = "es"
	French  Language = "fr"
	German  Language = "de"
	Italian Language = "it"
)

// OrdinalConverter handles conversion of numbers to ordinal strings
type OrdinalConverter struct {
	language Language
}

// NewOrdinalConverter creates a new OrdinalConverter for the specified language
func NewOrdinalConverter(lang Language) *OrdinalConverter {
	return &OrdinalConverter{language: lang}
}

// ToOrdinal converts a positive integer to its ordinal string representation
// Returns an error for negative numbers or zero
func (oc *OrdinalConverter) ToOrdinal(n int) (string, error) {
	if n <= 0 {
		return "", errors.New("ordinal numbers must be positive integers")
	}

	switch oc.language {
	case English:
		return toOrdinalEnglish(n), nil
	case Spanish:
		return toOrdinalSpanish(n), nil
	case French:
		return toOrdinalFrench(n), nil
	case German:
		return toOrdinalGerman(n), nil
	case Italian:
		return toOrdinalItalian(n), nil
	default:
		return toOrdinalEnglish(n), nil
	}
}

// ToOrdinalShort converts a number to a short ordinal (e.g., "1st", "2nd")
func (oc *OrdinalConverter) ToOrdinalShort(n int) (string, error) {
	if n <= 0 {
		return "", errors.New("ordinal numbers must be positive integers")
	}

	suffix := oc.getSuffix(n)
	return fmt.Sprintf("%d%s", n, suffix), nil
}

// getSuffix returns the English ordinal suffix for a number
func (oc *OrdinalConverter) getSuffix(n int) string {
	// Special cases for 11, 12, 13
	if n%100 >= 11 && n%100 <= 13 {
		return "th"
	}

	switch n % 10 {
	case 1:
		return "st"
	case 2:
		return "nd"
	case 3:
		return "rd"
	default:
		return "th"
	}
}

// ParseOrdinal parses an ordinal string back to a number
// Supports formats like "1st", "2nd", "3rd", "4th", "first", "second", etc.
func (oc *OrdinalConverter) ParseOrdinal(s string) (int, error) {
	s = strings.TrimSpace(strings.ToLower(s))

	// Try numeric ordinal format (1st, 2nd, etc.) - only accept valid suffixes
	re := regexp.MustCompile(`^(\d+)(st|nd|rd|th)$`)
	matches := re.FindStringSubmatch(s)
	if len(matches) > 1 {
		n, err := strconv.Atoi(matches[1])
		if err != nil {
			return 0, fmt.Errorf("invalid number in ordinal: %s", s)
		}
		return n, nil
	}

	// Try word format (first, second, etc.)
	if oc.language == English {
		return parseWordOrdinalEnglish(s)
	}

	return 0, fmt.Errorf("invalid ordinal format: %s", s)
}

// IsOrdinal checks if a string is a valid ordinal representation
func (oc *OrdinalConverter) IsOrdinal(s string) bool {
	_, err := oc.ParseOrdinal(s)
	return err == nil
}

// ToOrdinalRange generates a range of ordinals
func (oc *OrdinalConverter) ToOrdinalRange(start, end int) ([]string, error) {
	if start <= 0 || end <= 0 {
		return nil, errors.New("ordinal numbers must be positive integers")
	}
	if start > end {
		return nil, errors.New("start must be less than or equal to end")
	}

	result := make([]string, end-start+1)
	for i := start; i <= end; i++ {
		ordinal, err := oc.ToOrdinalShort(i)
		if err != nil {
			return nil, err
		}
		result[i-start] = ordinal
	}
	return result, nil
}

// English ordinal conversion
func toOrdinalEnglish(n int) string {
	// Special cases for 11, 12, 13
	if n%100 >= 11 && n%100 <= 13 {
		return fmt.Sprintf("%dth", n)
	}

	switch n % 10 {
	case 1:
		return fmt.Sprintf("%dst", n)
	case 2:
		return fmt.Sprintf("%dnd", n)
	case 3:
		return fmt.Sprintf("%drd", n)
	default:
		return fmt.Sprintf("%dth", n)
	}
}

// Spanish ordinal conversion
func toOrdinalSpanish(n int) string {
	// Spanish ordinals have gender (o/a) - we use masculine by default
	if n == 1 {
		return "1.º"
	} else if n == 2 {
		return "2.º"
	} else if n == 3 {
		return "3.º"
	}
	return fmt.Sprintf("%d.º", n)
}

// French ordinal conversion
func toOrdinalFrench(n int) string {
	// French uses superscript letters
	if n == 1 {
		return "1er"
	}
	return fmt.Sprintf("%de", n)
}

// German ordinal conversion
func toOrdinalGerman(n int) string {
	return fmt.Sprintf("%d.", n)
}

// Italian ordinal conversion
func toOrdinalItalian(n int) string {
	if n == 1 {
		return "1º"
	}
	return fmt.Sprintf("%dº", n)
}

// Parse English word ordinals
func parseWordOrdinalEnglish(s string) (int, error) {
	wordMap := map[string]int{
		"first":      1,
		"second":     2,
		"third":      3,
		"fourth":     4,
		"fifth":      5,
		"sixth":      6,
		"seventh":    7,
		"eighth":     8,
		"ninth":      9,
		"tenth":      10,
		"eleventh":   11,
		"twelfth":    12,
		"thirteenth": 13,
		"fourteenth": 14,
		"fifteenth":  15,
		"sixteenth":  16,
		"seventeenth": 17,
		"eighteenth": 18,
		"nineteenth": 19,
		"twentieth":  20,
	}

	if n, ok := wordMap[s]; ok {
		return n, nil
	}

	return 0, fmt.Errorf("unknown ordinal word: %s", s)
}

// ToWordOrdinal converts small numbers (1-20) to English word ordinals
func ToWordOrdinal(n int) (string, error) {
	if n < 1 || n > 20 {
		return "", errors.New("word ordinals only supported for 1-20")
	}

	wordOrdinals := []string{
		"", "first", "second", "third", "fourth", "fifth",
		"sixth", "seventh", "eighth", "ninth", "tenth",
		"eleventh", "twelfth", "thirteenth", "fourteenth", "fifteenth",
		"sixteenth", "seventeenth", "eighteenth", "nineteenth", "twentieth",
	}

	return wordOrdinals[n], nil
}

// ToOrdinalWithSuffix converts a number to ordinal with custom suffix pattern
// Useful for generating lists with specific formatting
func ToOrdinalWithSuffix(n int, suffixPattern string) (string, error) {
	if n <= 0 {
		return "", errors.New("ordinal numbers must be positive integers")
	}
	return fmt.Sprintf("%d%s", n, suffixPattern), nil
}

// OrdinalList generates a formatted list of ordinals
func OrdinalList(items []string) []string {
	result := make([]string, len(items))
	for i, item := range items {
		oc := NewOrdinalConverter(English)
		ordinal, _ := oc.ToOrdinalShort(i + 1)
		result[i] = fmt.Sprintf("%s %s", ordinal, item)
	}
	return result
}

// BatchToOrdinal converts multiple numbers to ordinals efficiently
func BatchToOrdinal(numbers []int, lang Language) ([]string, error) {
	oc := NewOrdinalConverter(lang)
	result := make([]string, len(numbers))

	for i, n := range numbers {
		ordinal, err := oc.ToOrdinalShort(n)
		if err != nil {
			return nil, fmt.Errorf("error at index %d: %w", i, err)
		}
		result[i] = ordinal
	}

	return result, nil
}

// GetOrdinalSuffix returns just the suffix for a number (without the number)
func GetOrdinalSuffix(n int) (string, error) {
	if n <= 0 {
		return "", errors.New("ordinal numbers must be positive integers")
	}

	// Special cases for 11, 12, 13
	if n%100 >= 11 && n%100 <= 13 {
		return "th", nil
	}

	switch n % 10 {
	case 1:
		return "st", nil
	case 2:
		return "nd", nil
	case 3:
		return "rd", nil
	default:
		return "th", nil
	}
}