// Package luhn_utils provides a comprehensive implementation of the Luhn algorithm
// (also known as the "modulus 10" or "mod 10" algorithm) for validating and
// generating check digits.
//
// The Luhn algorithm is used for validating:
//   - Credit card numbers
//   - IMEI numbers (International Mobile Equipment Identity)
//   - National Provider Identifier numbers (US healthcare)
//   - Canadian Social Insurance Numbers
//   - Greek Social Security Numbers (AMKA)
//   - South African ID numbers
//   - And many other identification numbers
//
// Reference: https://en.wikipedia.org/wiki/Luhn_algorithm
package luhn_utils

import (
	"errors"
	"math/rand"
	"regexp"
	"strconv"
	"strings"
	"time"
)

// Common card prefixes for identification
var cardPrefixes = map[string][]string{
	"visa":       {"4"},
	"mastercard": {"51", "52", "53", "54", "55", "2221", "2222", "2223", "2224", "2225"},
	"amex":       {"34", "37"},
	"discover":   {"6011", "622126", "644", "645", "646", "647", "648", "649", "65"},
	"jcb":        {"3528", "3529", "353", "354", "355", "356", "357", "358"},
	"diners":     {"300", "301", "302", "303", "304", "305", "36", "38", "39"},
	"unionpay":   {"62", "81"},
	"maestro":    {"5018", "5020", "5038", "5893", "6304", "6759", "6761", "6762", "6763"},
	"mir":        {"2200", "2201", "2202", "2203", "2204"},
}

// nonDigitRegex matches any non-digit character
var nonDigitRegex = regexp.MustCompile(`[^\d]`)

// Errors
var (
	ErrEmptyNumber    = errors.New("number must contain at least one digit")
	ErrInvalidLength  = errors.New("length must be greater than prefix length")
	ErrInvalidDigit   = errors.New("digit must be between 0 and 9")
	ErrInvalidNumber  = errors.New("number is not valid according to Luhn algorithm")
)

// StripFormatting removes all non-digit characters from a number string.
func StripFormatting(number string) string {
	return nonDigitRegex.ReplaceAllString(number, "")
}

// CalculateCheckDigit calculates the Luhn check digit for a given number.
// The check digit is the digit that, when appended to the number,
// makes it pass the Luhn validation.
//
// Returns the check digit (0-9) or an error if the number is invalid.
func CalculateCheckDigit(number string) (int, error) {
	cleanNumber := StripFormatting(number)
	
	if len(cleanNumber) == 0 {
		return 0, ErrEmptyNumber
	}
	
	total := 0
	digits := []rune(cleanNumber)
	
	// Double every other digit from right to left, starting with the first
	for i := len(digits) - 1; i >= 0; i-- {
		digit, err := strconv.Atoi(string(digits[i]))
		if err != nil {
			return 0, ErrInvalidDigit
		}
		
		position := len(digits) - 1 - i
		if position%2 == 0 {
			// Double this digit
			doubled := digit * 2
			if doubled > 9 {
				doubled -= 9
			}
			total += doubled
		} else {
			total += digit
		}
	}
	
	return (10 - (total % 10)) % 10, nil
}

// Validate validates a number using the Luhn algorithm.
// Returns true if the number is valid according to Luhn algorithm.
func Validate(number string) bool {
	cleanNumber := StripFormatting(number)
	
	if len(cleanNumber) < 2 {
		return false
	}
	
	total := 0
	digits := []rune(cleanNumber)
	
	// Double every second digit from right to left
	for i := len(digits) - 1; i >= 0; i-- {
		digit, err := strconv.Atoi(string(digits[i]))
		if err != nil {
			return false
		}
		
		position := len(digits) - 1 - i
		if position%2 == 1 {
			// Double this digit
			doubled := digit * 2
			if doubled > 9 {
				doubled -= 9
			}
			total += doubled
		} else {
			total += digit
		}
	}
	
	return total%10 == 0
}

// AddCheckDigit appends the Luhn check digit to a number.
// Returns the number with the check digit appended.
func AddCheckDigit(number string) (string, error) {
	checkDigit, err := CalculateCheckDigit(number)
	if err != nil {
		return "", err
	}
	cleanNumber := StripFormatting(number)
	return cleanNumber + strconv.Itoa(checkDigit), nil
}

// FormatNumber formats a number by grouping digits.
// groupSize is the number of digits per group (default: 4).
// separator is the separator between groups (default: space).
func FormatNumber(number string, groupSize int, separator string) string {
	cleanNumber := StripFormatting(number)
	
	if len(cleanNumber) == 0 {
		return ""
	}
	
	if groupSize <= 0 {
		groupSize = 4
	}
	if separator == "" {
		separator = " "
	}
	
	var groups []string
	for i := 0; i < len(cleanNumber); i += groupSize {
		end := i + groupSize
		if end > len(cleanNumber) {
			end = len(cleanNumber)
		}
		groups = append(groups, cleanNumber[i:end])
	}
	
	return strings.Join(groups, separator)
}

// GenerateValidNumber generates a valid Luhn number with the given prefix.
// This is useful for generating test credit card numbers.
//
// prefix is the prefix for the number (e.g., "4" for Visa).
// length is the desired total length of the number (default: 16).
func GenerateValidNumber(prefix string, length int) (string, error) {
	cleanPrefix := StripFormatting(prefix)
	
	if len(cleanPrefix) == 0 {
		return "", ErrEmptyNumber
	}
	
	if length <= len(cleanPrefix) {
		return "", ErrInvalidLength
	}
	
	// Initialize random source
	r := rand.New(rand.NewSource(time.Now().UnixNano()))
	
	// Fill remaining digits (except check digit) with random digits
	remainingLength := length - len(cleanPrefix) - 1
	randomDigits := make([]string, remainingLength)
	for i := 0; i < remainingLength; i++ {
		randomDigits[i] = strconv.Itoa(r.Intn(10))
	}
	
	// Combine prefix and random digits
	numberWithoutCheck := cleanPrefix + strings.Join(randomDigits, "")
	
	// Calculate and append check digit
	return AddCheckDigit(numberWithoutCheck)
}

// GenerateBatch generates multiple valid Luhn numbers with the given prefix.
func GenerateBatch(prefix string, count int, length int) ([]string, error) {
	results := make([]string, count)
	for i := 0; i < count; i++ {
		num, err := GenerateValidNumber(prefix, length)
		if err != nil {
			return nil, err
		}
		results[i] = num
	}
	return results, nil
}

// CardType represents a credit card type with its test numbers
type CardType struct {
	Type   string
	Number string
}

// GenerateTestCreditCards generates test credit card numbers for various card types.
// These are TEST numbers only and will not work for actual transactions.
// They are generated to pass Luhn validation.
func GenerateTestCreditCards(countPerType int) []CardType {
	// Initialize random source
	r := rand.New(rand.NewSource(time.Now().UnixNano()))
	
	var cards []CardType
	
	for cardType, prefixes := range cardPrefixes {
		for i := 0; i < countPerType; i++ {
			prefix := prefixes[r.Intn(len(prefixes))]
			
			// Use appropriate length based on card type
			length := 16
			switch cardType {
			case "amex":
				length = 15
			case "diners":
				length = 14
			}
			
			number, err := GenerateValidNumber(prefix, length)
			if err == nil {
				cards = append(cards, CardType{
					Type:   cardType,
					Number: number,
				})
			}
		}
	}
	
	return cards
}

// IdentifyCardType attempts to identify the card type based on the number prefix.
// This uses common prefix patterns and does not validate the number.
// Always validate the number separately before use.
func IdentifyCardType(number string) string {
	cleanNumber := StripFormatting(number)
	
	if len(cleanNumber) == 0 {
		return ""
	}
	
	for cardType, prefixes := range cardPrefixes {
		for _, prefix := range prefixes {
			if strings.HasPrefix(cleanNumber, prefix) {
				return cardType
			}
		}
	}
	
	return ""
}

// CalculateLuhnSum calculates the Luhn sum and returns both the sum and validity.
// This is useful for debugging or educational purposes.
func CalculateLuhnSum(number string) (int, bool) {
	cleanNumber := StripFormatting(number)
	
	if len(cleanNumber) == 0 {
		return 0, false
	}
	
	total := 0
	digits := []rune(cleanNumber)
	
	for i := len(digits) - 1; i >= 0; i-- {
		digit, err := strconv.Atoi(string(digits[i]))
		if err != nil {
			return 0, false
		}
		
		position := len(digits) - 1 - i
		if position%2 == 1 {
			doubled := digit * 2
			if doubled > 9 {
				doubled -= 9
			}
			total += doubled
		} else {
			total += digit
		}
	}
	
	return total, total%10 == 0
}

// FindCheckDigitErrors finds positions where a single digit error would make the number valid.
// This is useful for error detection and correction suggestions.
func FindCheckDigitErrors(number string) []int {
	cleanNumber := StripFormatting(number)
	
	if len(cleanNumber) == 0 {
		return nil
	}
	
	if Validate(cleanNumber) {
		return nil // Already valid
	}
	
	var errorPositions []int
	digits := []rune(cleanNumber)
	
	for i := 0; i < len(digits); i++ {
		original := digits[i]
		for newDigit := '0'; newDigit <= '9'; newDigit++ {
			if newDigit == original {
				continue
			}
			digits[i] = newDigit
			if Validate(string(digits)) {
				errorPositions = append(errorPositions, i)
				break
			}
		}
		digits[i] = original
	}
	
	return errorPositions
}

// Validator is a class-based validator for Luhn numbers.
// Provides a convenient interface for validating and generating Luhn-compliant numbers.
type Validator struct {
	groupSize int
	separator string
}

// NewValidator creates a new Validator with the given formatting options.
func NewValidator(groupSize int, separator string) *Validator {
	if groupSize <= 0 {
		groupSize = 4
	}
	if separator == "" {
		separator = " "
	}
	return &Validator{
		groupSize: groupSize,
		separator: separator,
	}
}

// Validate validates a number using the Luhn algorithm.
func (v *Validator) Validate(number string) bool {
	return Validate(number)
}

// CalculateCheckDigit calculates the check digit for a number.
func (v *Validator) CalculateCheckDigit(number string) (int, error) {
	return CalculateCheckDigit(number)
}

// AddCheckDigit appends the check digit to a number.
func (v *Validator) AddCheckDigit(number string) (string, error) {
	return AddCheckDigit(number)
}

// Format formats a number with the default group size and separator.
func (v *Validator) Format(number string) string {
	return FormatNumber(number, v.groupSize, v.separator)
}

// Strip removes formatting from a number.
func (v *Validator) Strip(number string) string {
	return StripFormatting(number)
}

// Generate generates a valid Luhn number with the given prefix.
func (v *Validator) Generate(prefix string, length int) (string, error) {
	return GenerateValidNumber(prefix, length)
}

// GenerateBatch generates multiple valid Luhn numbers.
func (v *Validator) GenerateBatch(prefix string, count int, length int) ([]string, error) {
	return GenerateBatch(prefix, count, length)
}