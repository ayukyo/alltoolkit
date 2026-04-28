// Package roman_numeral_utils provides utilities for converting between Roman numerals and integers.
// Roman numerals are a numeral system that originated in ancient Rome and remained the usual
// way of writing numbers throughout Europe well into the Late Middle Ages.
package roman_numeral_utils

import (
	"errors"
	"regexp"
	"strings"
)

// RomanNumeral represents a single Roman numeral symbol with its value
type RomanNumeral struct {
	Symbol string
	Value  int
}

// Standard Roman numeral symbols and their values
var romanNumerals = []RomanNumeral{
	{"M", 1000},
	{"CM", 900},
	{"D", 500},
	{"CD", 400},
	{"C", 100},
	{"XC", 90},
	{"L", 50},
	{"XL", 40},
	{"X", 10},
	{"IX", 9},
	{"V", 5},
	{"IV", 4},
	{"I", 1},
}

// Valid Roman numeral pattern (basic validation)
var romanPattern = regexp.MustCompile(`^M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$`)

// Errors
var (
	ErrEmptyString      = errors.New("empty string")
	ErrInvalidRoman     = errors.New("invalid Roman numeral")
	ErrOutOfRange       = errors.New("number out of range (1-3999)")
	ErrNegativeNumber   = errors.New("negative numbers cannot be converted to Roman numerals")
	ErrZeroNotAllowed   = errors.New("zero cannot be converted to Roman numeral")
)

// ToInt converts a Roman numeral string to its integer value.
// Returns an error if the string is empty, invalid, or represents a number > 3999.
func ToInt(roman string) (int, error) {
	if roman == "" {
		return 0, ErrEmptyString
	}

	// Normalize: convert to uppercase
	roman = strings.ToUpper(roman)

	// Validate format
	if !romanPattern.MatchString(roman) {
		return 0, ErrInvalidRoman
	}

	result := 0
	i := 0
	length := len(roman)

	for i < length {
		matched := false

		// Try to match two-character symbols first
		if i+1 < length {
			twoChar := roman[i : i+2]
			for _, numeral := range romanNumerals {
				if numeral.Symbol == twoChar {
					result += numeral.Value
					i += 2
					matched = true
					break
				}
			}
		}

		if matched {
			continue
		}

		// Match single character symbols
		oneChar := string(roman[i])
		for _, numeral := range romanNumerals {
			if numeral.Symbol == oneChar {
				result += numeral.Value
				i++
				matched = true
				break
			}
		}

		if !matched {
			return 0, ErrInvalidRoman
		}
	}

	return result, nil
}

// ToRoman converts an integer to its Roman numeral representation.
// Only supports numbers from 1 to 3999 (standard Roman numerals).
// Returns an error for zero, negative numbers, or numbers > 3999.
func ToRoman(num int) (string, error) {
	if num <= 0 {
		if num == 0 {
			return "", ErrZeroNotAllowed
		}
		return "", ErrNegativeNumber
	}
	if num > 3999 {
		return "", ErrOutOfRange
	}

	var result strings.Builder

	for _, numeral := range romanNumerals {
		for num >= numeral.Value {
			result.WriteString(numeral.Symbol)
			num -= numeral.Value
		}
	}

	return result.String(), nil
}

// MustToInt converts a Roman numeral to an integer and panics on error.
// Use this only when you are certain the input is valid.
func MustToInt(roman string) int {
	result, err := ToInt(roman)
	if err != nil {
		panic(err)
	}
	return result
}

// MustToRoman converts an integer to a Roman numeral and panics on error.
// Use this only when you are certain the input is valid.
func MustToRoman(num int) string {
	result, err := ToRoman(num)
	if err != nil {
		panic(err)
	}
	return result
}

// IsValid checks if a string is a valid Roman numeral.
func IsValid(roman string) bool {
	if roman == "" {
		return false
	}
	return romanPattern.MatchString(strings.ToUpper(roman))
}

// ParseWithAlternative parses Roman numerals with alternative notation.
// Supports vinculum (overline) notation for numbers > 3999 where an overline
// multiplies the value by 1000. In text, this is represented with underscores
// on both sides, e.g., _V_ for 5000.
func ParseWithAlternative(roman string) (int, error) {
	roman = strings.ToUpper(roman)

	// Check for vinculum notation (represented as _X_)
	if strings.Contains(roman, "_") {
		return parseVinculum(roman)
	}

	return ToInt(roman)
}

// parseVinculum handles vinculum (overline) notation
func parseVinculum(roman string) (int, error) {
	result := 0
	currentVinculum := false
	var current strings.Builder

	for i := 0; i < len(roman); i++ {
		char := roman[i]

		if char == '_' {
			if currentVinculum {
				// End of vinculum section
				value, err := ToInt(current.String())
				if err != nil {
					return 0, err
				}
				result += value * 1000
				current.Reset()
				currentVinculum = false
			} else {
				// Start of vinculum section
				// First convert any pending normal characters
				if current.Len() > 0 {
					value, err := ToInt(current.String())
					if err != nil {
						return 0, err
					}
					result += value
					current.Reset()
				}
				currentVinculum = true
			}
		} else {
			current.WriteByte(char)
		}
	}

	// Handle any remaining characters
	if current.Len() > 0 {
		value, err := ToInt(current.String())
		if err != nil {
			return 0, err
		}
		if currentVinculum {
			result += value * 1000
		} else {
			result += value
		}
	}

	return result, nil
}

// Add adds two Roman numerals and returns the result as a Roman numeral.
func Add(roman1, roman2 string) (string, error) {
	num1, err := ToInt(roman1)
	if err != nil {
		return "", err
	}
	num2, err := ToInt(roman2)
	if err != nil {
		return "", err
	}
	return ToRoman(num1 + num2)
}

// Subtract subtracts the second Roman numeral from the first and returns the result.
// Returns an error if the result is <= 0.
func Subtract(roman1, roman2 string) (string, error) {
	num1, err := ToInt(roman1)
	if err != nil {
		return "", err
	}
	num2, err := ToInt(roman2)
	if err != nil {
		return "", err
	}
	return ToRoman(num1 - num2)
}

// Multiply multiplies two Roman numerals and returns the result.
func Multiply(roman1, roman2 string) (string, error) {
	num1, err := ToInt(roman1)
	if err != nil {
		return "", err
	}
	num2, err := ToInt(roman2)
	if err != nil {
		return "", err
	}
	return ToRoman(num1 * num2)
}

// Divide divides the first Roman numeral by the second and returns the result.
// Uses integer division.
func Divide(roman1, roman2 string) (string, error) {
	num1, err := ToInt(roman1)
	if err != nil {
		return "", err
	}
	num2, err := ToInt(roman2)
	if err != nil {
		return "", err
	}
	if num2 == 0 {
		return "", errors.New("division by zero")
	}
	return ToRoman(num1 / num2)
}

// Compare compares two Roman numerals.
// Returns -1 if roman1 < roman2, 0 if equal, 1 if roman1 > roman2.
func Compare(roman1, roman2 string) (int, error) {
	num1, err := ToInt(roman1)
	if err != nil {
		return 0, err
	}
	num2, err := ToInt(roman2)
	if err != nil {
		return 0, err
	}

	if num1 < num2 {
		return -1, nil
	} else if num1 > num2 {
		return 1, nil
	}
	return 0, nil
}

// GetAll returns all standard Roman numerals and their values.
func GetAll() []RomanNumeral {
	return romanNumerals
}

// Range represents a range of Roman numerals
type Range struct {
	Start int
	End   int
}

// GenerateRange generates Roman numerals for a range of integers.
func GenerateRange(start, end int) ([]string, error) {
	if start < 1 || end > 3999 || start > end {
		return nil, errors.New("invalid range")
	}

	result := make([]string, end-start+1)
	for i := start; i <= end; i++ {
		roman, err := ToRoman(i)
		if err != nil {
			return nil, err
		}
		result[i-start] = roman
	}
	return result, nil
}

// FindHighest finds the highest Roman numeral from a list that is valid.
func FindHighest(romans []string) (string, int, error) {
	highest := ""
	highestValue := 0

	for _, roman := range romans {
		value, err := ToInt(roman)
		if err != nil {
			continue
		}
		if value > highestValue {
			highestValue = value
			highest = roman
		}
	}

	if highest == "" {
		return "", 0, errors.New("no valid Roman numerals found")
	}

	return highest, highestValue, nil
}