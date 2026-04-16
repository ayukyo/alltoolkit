// Package isbn_utils provides ISBN (International Standard Book Number) utilities
// for validation, generation, conversion, and formatting of ISBN-10 and ISBN-13.
package isbn_utils

import (
	"errors"
	"regexp"
	"strings"
)

// ISBN types
const (
	TypeISBN10 = "ISBN-10"
	TypeISBN13 = "ISBN-13"
)

// Common errors
var (
	ErrInvalidISBN      = errors.New("invalid ISBN format")
	ErrInvalidChecksum  = errors.New("invalid ISBN checksum")
	ErrInvalidLength    = errors.New("invalid ISBN length")
	ErrConversionNotPossible = errors.New("ISBN conversion not possible")
)

// ISBN represents a parsed ISBN number
type ISBN struct {
	Number    string // Clean ISBN number (digits and check character only)
	Type      string // TypeISBN10 or TypeISBN13
	Prefix    string // For ISBN-13: 978 or 979
	Group     string // Registration group
	Publisher string // Publisher code
	Title     string // Title code
	Check     string // Check digit/character
}

var (
	// isbnCleanRegex matches all non-alphanumeric characters except X
	isbnCleanRegex = regexp.MustCompile(`[^0-9Xx]`)
)

// Clean removes all non-essential characters from an ISBN string
func Clean(isbn string) string {
	return strings.ToUpper(isbnCleanRegex.ReplaceAllString(isbn, ""))
}

// Validate validates an ISBN (either ISBN-10 or ISBN-13)
func Validate(isbn string) (bool, error) {
	clean := Clean(isbn)
	
	switch len(clean) {
	case 10:
		return ValidateISBN10(clean)
	case 13:
		return ValidateISBN13(clean)
	default:
		return false, ErrInvalidLength
	}
}

// ValidateISBN10 validates an ISBN-10 number
func ValidateISBN10(isbn string) (bool, error) {
	clean := Clean(isbn)
	
	if len(clean) != 10 {
		return false, ErrInvalidLength
	}
	
	sum := 0
	for i := 0; i < 9; i++ {
		if clean[i] < '0' || clean[i] > '9' {
			return false, ErrInvalidISBN
		}
		sum += int(clean[i]-'0') * (10 - i)
	}
	
	// Check digit can be 0-9 or X (representing 10)
	checkChar := clean[9]
	var checkValue int
	if checkChar == 'X' {
		checkValue = 10
	} else if checkChar >= '0' && checkChar <= '9' {
		checkValue = int(checkChar - '0')
	} else {
		return false, ErrInvalidISBN
	}
	sum += checkValue
	
	if sum%11 != 0 {
		return false, ErrInvalidChecksum
	}
	
	return true, nil
}

// ValidateISBN13 validates an ISBN-13 number
func ValidateISBN13(isbn string) (bool, error) {
	clean := Clean(isbn)
	
	if len(clean) != 13 {
		return false, ErrInvalidLength
	}
	
	// Check if all characters are digits
	for i := 0; i < 13; i++ {
		if clean[i] < '0' || clean[i] > '9' {
			return false, ErrInvalidISBN
		}
	}
	
	sum := 0
	for i := 0; i < 12; i++ {
		digit := int(clean[i] - '0')
		if i%2 == 0 {
			sum += digit
		} else {
			sum += digit * 3
		}
	}
	
	checkDigit := (10 - (sum % 10)) % 10
	
	if int(clean[12]-'0') != checkDigit {
		return false, ErrInvalidChecksum
	}
	
	return true, nil
}

// GenerateCheckDigit10 calculates the check digit for an ISBN-10
func GenerateCheckDigit10(prefix string) (string, error) {
	clean := strings.ToUpper(strings.ReplaceAll(prefix, "-", ""))
	
	if len(clean) != 9 {
		return "", ErrInvalidLength
	}
	
	sum := 0
	for i := 0; i < 9; i++ {
		if clean[i] < '0' || clean[i] > '9' {
			return "", ErrInvalidISBN
		}
		sum += int(clean[i]-'0') * (10 - i)
	}
	
	check := (11 - (sum % 11)) % 11
	if check == 10 {
		return "X", nil
	}
	return string(rune('0' + check)), nil
}

// GenerateCheckDigit13 calculates the check digit for an ISBN-13
func GenerateCheckDigit13(prefix string) (string, error) {
	clean := strings.ReplaceAll(prefix, "-", "")
	
	if len(clean) != 12 {
		return "", ErrInvalidLength
	}
	
	sum := 0
	for i := 0; i < 12; i++ {
		if clean[i] < '0' || clean[i] > '9' {
			return "", ErrInvalidISBN
		}
		digit := int(clean[i] - '0')
		if i%2 == 0 {
			sum += digit
		} else {
			sum += digit * 3
		}
	}
	
	check := (10 - (sum % 10)) % 10
	return string(rune('0' + check)), nil
}

// ToISBN13 converts an ISBN-10 to ISBN-13
func ToISBN13(isbn10 string) (string, error) {
	clean := Clean(isbn10)
	
	if len(clean) != 10 {
		return "", ErrInvalidLength
	}
	
	// Validate the ISBN-10 first
	if valid, err := ValidateISBN10(clean); !valid {
		return "", err
	}
	
	// ISBN-13 prefix for books is 978
	prefix := "978" + clean[:9]
	
	checkDigit, err := GenerateCheckDigit13(prefix)
	if err != nil {
		return "", err
	}
	
	return prefix + checkDigit, nil
}

// ToISBN10 converts an ISBN-13 to ISBN-10
// Only works for ISBNs starting with 978
func ToISBN10(isbn13 string) (string, error) {
	clean := Clean(isbn13)
	
	if len(clean) != 13 {
		return "", ErrInvalidLength
	}
	
	// Validate the ISBN-13 first
	if valid, err := ValidateISBN13(clean); !valid {
		return "", err
	}
	
	// Can only convert 978-prefix ISBN-13 to ISBN-10
	if !strings.HasPrefix(clean, "978") {
		return "", ErrConversionNotPossible
	}
	
	// Get digits 4-12 (9 digits)
	prefix := clean[3:12]
	
	checkDigit, err := GenerateCheckDigit10(prefix)
	if err != nil {
		return "", err
	}
	
	return prefix + checkDigit, nil
}

// Format formats an ISBN with hyphens in standard positions
// ISBN-10: X-XXXXX-XXX-X
// ISBN-13: XXX-X-XXXXX-XXX-X (simplified format)
func Format(isbn string) string {
	clean := Clean(isbn)
	
	if len(clean) == 10 {
		// Standard ISBN-10 format: X-XXXXX-XXX-X
		return string(clean[0]) + "-" + 
			clean[1:6] + "-" + 
			clean[6:9] + "-" + 
			string(clean[9])
	}
	
	if len(clean) == 13 {
		// Standard ISBN-13 format: XXX-X-XXXXX-XXX-X
		return clean[0:3] + "-" + 
			string(clean[3]) + "-" + 
			clean[4:9] + "-" + 
			clean[9:12] + "-" + 
			string(clean[12])
	}
	
	return isbn
}

// GetType returns the ISBN type (ISBN-10 or ISBN-13)
func GetType(isbn string) (string, error) {
	clean := Clean(isbn)
	
	switch len(clean) {
	case 10:
		return TypeISBN10, nil
	case 13:
		return TypeISBN13, nil
	default:
		return "", ErrInvalidLength
	}
}

// IsISBN checks if a string is a valid ISBN (either format)
func IsISBN(isbn string) bool {
	valid, _ := Validate(isbn)
	return valid
}

// IsISBN10 checks if a string is a valid ISBN-10
func IsISBN10(isbn string) bool {
	valid, _ := ValidateISBN10(isbn)
	return valid
}

// IsISBN13 checks if a string is a valid ISBN-13
func IsISBN13(isbn string) bool {
	valid, _ := ValidateISBN13(isbn)
	return valid
}

// Normalize converts ISBN-10 to ISBN-13 and returns clean ISBN-13
// If already ISBN-13, returns clean version
func Normalize(isbn string) (string, error) {
	clean := Clean(isbn)
	
	switch len(clean) {
	case 10:
		return ToISBN13(clean)
	case 13:
		if valid, err := ValidateISBN13(clean); !valid {
			return "", err
		}
		return clean, nil
	default:
		return "", ErrInvalidLength
	}
}

// GenerateISBN13 generates a valid ISBN-13 from a 12-digit prefix
func GenerateISBN13(prefix string) (string, error) {
	clean := strings.ReplaceAll(prefix, "-", "")
	
	if len(clean) != 12 {
		return "", ErrInvalidLength
	}
	
	checkDigit, err := GenerateCheckDigit13(clean)
	if err != nil {
		return "", err
	}
	
	return clean + checkDigit, nil
}

// GenerateISBN10 generates a valid ISBN-10 from a 9-digit prefix
func GenerateISBN10(prefix string) (string, error) {
	clean := strings.ToUpper(strings.ReplaceAll(prefix, "-", ""))
	
	if len(clean) != 9 {
		return "", ErrInvalidLength
	}
	
	checkDigit, err := GenerateCheckDigit10(clean)
	if err != nil {
		return "", err
	}
	
	return clean + checkDigit, nil
}

// Parse parses an ISBN and returns its components (simplified version)
func Parse(isbn string) (*ISBN, error) {
	clean := Clean(isbn)
	
	var isbnType string
	switch len(clean) {
	case 10:
		isbnType = TypeISBN10
	case 13:
		isbnType = TypeISBN13
	default:
		return nil, ErrInvalidLength
	}
	
	valid, err := Validate(clean)
	if !valid {
		return nil, err
	}
	
	result := &ISBN{
		Number: clean,
		Type:   isbnType,
		Check:  string(clean[len(clean)-1]),
	}
	
	if isbnType == TypeISBN13 {
		result.Prefix = clean[:3]
	}
	
	return result, nil
}