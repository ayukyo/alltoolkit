// Package credit_card_utils provides credit card validation, identification, and formatting utilities.
// All functions are implemented using Go standard library with zero external dependencies.
package credit_card_utils

import (
	"errors"
	"fmt"
	"math/rand"
	"regexp"
	"strconv"
	"strings"
	"time"
)

// CardType represents a credit card brand/type
type CardType string

const (
	CardTypeVisa       CardType = "Visa"
	CardTypeMastercard CardType = "Mastercard"
	CardTypeAmex       CardType = "American Express"
	CardTypeDiscover   CardType = "Discover"
	CardTypeJCB        CardType = "JCB"
	CardTypeDinersClub CardType = "Diners Club"
	CardTypeUnionPay   CardType = "UnionPay"
	CardTypeMaestro    CardType = "Maestro"
	CardTypeUnknown    CardType = "Unknown"
)

// CardInfo contains detailed information about a credit card
type CardInfo struct {
	Type      CardType
	IIN       string   // Issuer Identification Number (first 6-8 digits)
	Valid     bool     // Luhn check result
	Formatted string   // Formatted card number
	Length    int      // Number of digits
	CVVLength int      // Expected CVV length
	Networks  []string // Card networks
}

// cardPattern defines patterns for card type identification
type cardPattern struct {
	cardType  CardType
	pattern   *regexp.Regexp
	lengths   []int
	cvvLength int
}

var cardPatterns = []cardPattern{
	{CardTypeVisa, regexp.MustCompile(`^4`), []int{13, 16, 19}, 3},
	{CardTypeMastercard, regexp.MustCompile(`^(5[1-5]|2[2-7])`), []int{16}, 3},
	{CardTypeAmex, regexp.MustCompile(`^3[47]`), []int{15}, 4},
	{CardTypeDiscover, regexp.MustCompile(`^(6011|65|64[4-9])`), []int{16, 19}, 3},
	{CardTypeJCB, regexp.MustCompile(`^35`), []int{16}, 3},
	{CardTypeDinersClub, regexp.MustCompile(`^(30[0-5]|36|38|39)`), []int{14, 16, 19}, 3},
	{CardTypeUnionPay, regexp.MustCompile(`^(62|81)`), []int{16, 17, 18, 19}, 3},
	{CardTypeMaestro, regexp.MustCompile(`^(5018|5020|5038|5893|6304|6759|676[1-3])`), []int{12, 13, 14, 15, 16, 17, 18, 19}, 3},
}

// ============================================================================
// Luhn Algorithm
// ============================================================================

// LuhnCheck validates a number using the Luhn algorithm.
// Returns true if the number passes the Luhn check.
func LuhnCheck(number string) bool {
	// Remove spaces and dashes
	clean := CleanCardNumber(number)

	// Check if all characters are digits
	if _, err := strconv.Atoi(clean); err != nil {
		return false
	}

	// Must have at least 2 digits
	if len(clean) < 2 {
		return false
	}

	sum := 0
	alt := false

	// Process from right to left
	for i := len(clean) - 1; i >= 0; i-- {
		digit, _ := strconv.Atoi(string(clean[i]))

		if alt {
			digit *= 2
			if digit > 9 {
				digit -= 9
			}
		}
		sum += digit
		alt = !alt
	}

	return sum%10 == 0
}

// CalculateLuhnDigit calculates the Luhn check digit for a number.
// The input number should NOT include the check digit.
func CalculateLuhnDigit(number string) int {
	clean := CleanCardNumber(number)

	sum := 0
	alt := true // Start with true since we're calculating check digit

	for i := len(clean) - 1; i >= 0; i-- {
		digit, _ := strconv.Atoi(string(clean[i]))

		if alt {
			digit *= 2
			if digit > 9 {
				digit -= 9
			}
		}
		sum += digit
		alt = !alt
	}

	return (10 - (sum % 10)) % 10
}

// ============================================================================
// Card Number Cleaning and Formatting
// ============================================================================

// CleanCardNumber removes all non-digit characters from a card number.
func CleanCardNumber(number string) string {
	var result strings.Builder
	for _, r := range number {
		if r >= '0' && r <= '9' {
			result.WriteRune(r)
		}
	}
	return result.String()
}

// FormatCardNumber formats a card number with spaces for readability.
// Uses standard 4-digit grouping.
func FormatCardNumber(number string) string {
	clean := CleanCardNumber(number)
	var result strings.Builder
	for i, r := range clean {
		if i > 0 && i%4 == 0 {
			result.WriteRune(' ')
		}
		result.WriteRune(r)
	}
	return result.String()
}

// FormatCardNumberCustom formats a card number with custom grouping.
func FormatCardNumberCustom(number string, groups []int) string {
	clean := CleanCardNumber(number)
	var result strings.Builder
	pos := 0
	for i, groupSize := range groups {
		if i > 0 {
			result.WriteRune(' ')
		}
		end := pos + groupSize
		if end > len(clean) {
			end = len(clean)
		}
		result.WriteString(clean[pos:end])
		pos = end
		if pos >= len(clean) {
			break
		}
	}
	// Add remaining digits
	if pos < len(clean) {
		if len(groups) > 0 {
			result.WriteRune(' ')
		}
		result.WriteString(clean[pos:])
	}
	return result.String()
}

// MaskCardNumber masks the middle digits of a card number.
// Keeps first 'showFirst' and last 'showLast' digits visible.
func MaskCardNumber(number string, showFirst, showLast int) string {
	clean := CleanCardNumber(number)
	if len(clean) <= showFirst+showLast {
		return clean
	}

	masked := strings.Repeat("*", len(clean)-showFirst-showLast)
	return clean[:showFirst] + masked + clean[len(clean)-showLast:]
}

// MaskCardNumberDefault masks with default visibility (first 4, last 4).
func MaskCardNumberDefault(number string) string {
	return MaskCardNumber(number, 4, 4)
}

// ============================================================================
// Card Type Identification
// ============================================================================

// IdentifyCardType identifies the card type from the card number.
func IdentifyCardType(number string) CardType {
	clean := CleanCardNumber(number)

	for _, cp := range cardPatterns {
		if cp.pattern.MatchString(clean) {
			// Check if length is valid for this card type
			for _, l := range cp.lengths {
				if len(clean) == l {
					return cp.cardType
				}
			}
			// If length doesn't match but pattern does, still return type
			// (length validation should be done separately)
			return cp.cardType
		}
	}

	return CardTypeUnknown
}

// GetCardInfo returns comprehensive information about a card number.
func GetCardInfo(number string) CardInfo {
	clean := CleanCardNumber(number)

	cardType := IdentifyCardType(number)
	valid := LuhnCheck(number)
	cvvLength := 3 // default
	networks := []string{}

	for _, cp := range cardPatterns {
		if cp.cardType == cardType {
			cvvLength = cp.cvvLength
			break
		}
	}

	// Add networks based on card type
	switch cardType {
	case CardTypeVisa:
		networks = []string{"Visa", "Plus", "Visa Electron"}
	case CardTypeMastercard:
		networks = []string{"Mastercard", "Maestro", "Cirrus"}
	case CardTypeAmex:
		networks = []string{"American Express"}
	case CardTypeDiscover:
		networks = []string{"Discover", "Diners Club International"}
	case CardTypeJCB:
		networks = []string{"JCB"}
	case CardTypeDinersClub:
		networks = []string{"Diners Club", "Discover"}
	case CardTypeUnionPay:
		networks = []string{"UnionPay"}
	case CardTypeMaestro:
		networks = []string{"Maestro", "Mastercard"}
	}

	iin := ""
	if len(clean) >= 6 {
		iin = clean[:6]
	}

	return CardInfo{
		Type:      cardType,
		IIN:       iin,
		Valid:     valid,
		Formatted: FormatCardNumber(clean),
		Length:    len(clean),
		CVVLength: cvvLength,
		Networks:  networks,
	}
}

// IsValidCardNumber checks if a card number is valid (passes Luhn and has valid length).
func IsValidCardNumber(number string) bool {
	clean := CleanCardNumber(number)
	cardType := IdentifyCardType(clean)

	// Check Luhn
	if !LuhnCheck(clean) {
		return false
	}

	// Check length based on card type
	if cardType == CardTypeUnknown {
		// For unknown types, accept 13-19 digit cards
		return len(clean) >= 13 && len(clean) <= 19
	}

	// Check against known card type lengths
	for _, cp := range cardPatterns {
		if cp.cardType == cardType {
			for _, l := range cp.lengths {
				if len(clean) == l {
					return true
				}
			}
			return false
		}
	}

	return false
}

// GetExpectedLengths returns expected card number lengths for a card type.
func GetExpectedLengths(cardType CardType) []int {
	for _, cp := range cardPatterns {
		if cp.cardType == cardType {
			return cp.lengths
		}
	}
	return nil
}

// GetCVVLength returns expected CVV length for a card type.
func GetCVVLength(cardType CardType) int {
	for _, cp := range cardPatterns {
		if cp.cardType == cardType {
			return cp.cvvLength
		}
	}
	return 3 // default
}

// ============================================================================
// CVV Validation
// ============================================================================

// IsValidCVV checks if a CVV is valid for a given card type.
func IsValidCVV(cvv string, cardType CardType) bool {
	cleanCVV := strings.TrimSpace(cvv)

	// Check if all digits
	if _, err := strconv.Atoi(cleanCVV); err != nil {
		return false
	}

	expectedLength := GetCVVLength(cardType)
	return len(cleanCVV) == expectedLength
}

// IsValidCVVForNumber checks if a CVV is valid for a given card number.
func IsValidCVVForNumber(cvv, number string) bool {
	cardType := IdentifyCardType(number)
	return IsValidCVV(cvv, cardType)
}

// ============================================================================
// Expiry Date Validation
// ============================================================================

// ParseExpiryDate parses an expiry date in MM/YY or MM/YYYY format.
// Returns year, month, and error.
func ParseExpiryDate(expiry string) (year int, month int, err error) {
	clean := strings.ReplaceAll(expiry, " ", "")
	clean = strings.ReplaceAll(clean, "/", "")
	clean = strings.ReplaceAll(clean, "-", "")

	if len(clean) == 4 {
		// MM/YY format
		month, _ = strconv.Atoi(clean[:2])
		yearShort, _ := strconv.Atoi(clean[2:])
		year = 2000 + yearShort
	} else if len(clean) == 6 {
		// MM/YYYY format
		month, _ = strconv.Atoi(clean[:2])
		year, _ = strconv.Atoi(clean[2:])
	} else {
		return 0, 0, errors.New("invalid expiry date format")
	}

	if month < 1 || month > 12 {
		return 0, 0, errors.New("invalid month")
	}

	return year, month, nil
}

// IsValidExpiryDate checks if an expiry date is valid and not expired.
func IsValidExpiryDate(expiry string) bool {
	year, month, err := ParseExpiryDate(expiry)
	if err != nil {
		return false
	}

	now := time.Now()
	currentYear := now.Year()
	currentMonth := int(now.Month())

	// Check if expired
	if year < currentYear {
		return false
	}
	if year == currentYear && month < currentMonth {
		return false
	}

	// Check if too far in future (more than 20 years)
	if year > currentYear+20 {
		return false
	}

	return true
}

// IsExpired checks if an expiry date is expired.
func IsExpired(expiry string) bool {
	return !IsValidExpiryDate(expiry)
}

// FormatExpiryDate formats expiry date to MM/YY format.
func FormatExpiryDate(expiry string) string {
	year, month, err := ParseExpiryDate(expiry)
	if err != nil {
		return expiry
	}
	return fmt.Sprintf("%02d/%02d", month, year%100)
}

// ============================================================================
// Test Card Number Generation
// ============================================================================

// Test card number prefixes for different card types
var testCardPrefixes = map[CardType][]string{
	CardTypeVisa:       {"4111", "4012", "4000"},
	CardTypeMastercard: {"5500", "5555", "2222"},
	CardTypeAmex:       {"3782", "3714"},
	CardTypeDiscover:   {"6011", "65"},
	CardTypeJCB:        {"3530", "3566"},
	CardTypeDinersClub: {"3000", "38"},
}

// GenerateTestCardNumber generates a valid test card number for a given card type.
// The generated number will pass Luhn check but is NOT a real card number.
func GenerateTestCardNumber(cardType CardType) string {
	prefixes, ok := testCardPrefixes[cardType]
	if !ok {
		// Default to Visa prefix for unknown types
		prefixes = []string{"4"}
	}

	// Use random seed
	r := rand.New(rand.NewSource(time.Now().UnixNano()))
	prefix := prefixes[r.Intn(len(prefixes))]

	// Determine target length
	lengths := GetExpectedLengths(cardType)
	targetLength := 16 // default
	if len(lengths) > 0 {
		targetLength = lengths[0]
	}

	// Generate random digits (excluding check digit)
	number := prefix
	for len(number) < targetLength-1 {
		number += strconv.Itoa(r.Intn(10))
	}

	// Calculate and append check digit
	checkDigit := CalculateLuhnDigit(number)
	return number + strconv.Itoa(checkDigit)
}

// GenerateTestCard generates a complete test card with number, CVV, and expiry.
func GenerateTestCard(cardType CardType) (number, cvv, expiry string) {
	number = GenerateTestCardNumber(cardType)

	// Generate CVV
	cvvLength := GetCVVLength(cardType)
	r := rand.New(rand.NewSource(time.Now().UnixNano()))
	cvv = ""
	for i := 0; i < cvvLength; i++ {
		cvv += strconv.Itoa(r.Intn(10))
	}

	// Generate expiry (1-5 years in future)
	now := time.Now()
	monthsAhead := r.Intn(60) + 12 // 1-5 years
	future := now.AddDate(0, monthsAhead, 0)
	expiry = fmt.Sprintf("%02d/%02d", int(future.Month()), future.Year()%100)

	return number, cvv, expiry
}

// ============================================================================
// Validation Summary
// ============================================================================

// ValidationResult contains the result of a complete card validation.
type ValidationResult struct {
	Valid          bool     `json:"valid"`
	CardNumber     string   `json:"card_number"`
	CardType       CardType `json:"card_type"`
	LuhnValid      bool     `json:"luhn_valid"`
	LengthValid    bool     `json:"length_valid"`
	LengthExpected []int    `json:"length_expected,omitempty"`
	CVVValid       bool     `json:"cvv_valid,omitempty"`
	ExpiryValid    bool    `json:"expiry_valid,omitempty"`
	Errors         []string `json:"errors,omitempty"`
}

// ValidateCard performs complete validation of card number, CVV, and expiry.
func ValidateCard(number, cvv, expiry string) ValidationResult {
	result := ValidationResult{
		CardNumber: CleanCardNumber(number),
		CardType:   IdentifyCardType(number),
		Errors:     []string{},
	}

	// Luhn check
	result.LuhnValid = LuhnCheck(number)
	if !result.LuhnValid {
		result.Errors = append(result.Errors, "card number fails Luhn check")
	}

	// Length check
	clean := CleanCardNumber(number)
	result.LengthExpected = GetExpectedLengths(result.CardType)
	result.LengthValid = false
	for _, l := range result.LengthExpected {
		if len(clean) == l {
			result.LengthValid = true
			break
		}
	}
	if !result.LengthValid && len(result.LengthExpected) > 0 {
		result.Errors = append(result.Errors, fmt.Sprintf("invalid length, expected %v", result.LengthExpected))
	}

	// CVV check (if provided)
	if cvv != "" {
		result.CVVValid = IsValidCVVForNumber(cvv, number)
		if !result.CVVValid {
			result.Errors = append(result.Errors, "invalid CVV")
		}
	}

	// Expiry check (if provided)
	if expiry != "" {
		result.ExpiryValid = IsValidExpiryDate(expiry)
		if !result.ExpiryValid {
			result.Errors = append(result.Errors, "invalid or expired expiry date")
		}
	}

	// Overall validity
	result.Valid = result.LuhnValid && result.LengthValid && (cvv == "" || result.CVVValid) && (expiry == "" || result.ExpiryValid)

	return result
}

// ============================================================================
// Card Range Utilities
// ============================================================================

// IsInCardRange checks if a card number falls within a specific IIN range.
func IsInCardRange(number, startIIN, endIIN string) bool {
	clean := CleanCardNumber(number)

	startLen := len(startIIN)
	endLen := len(endIIN)
	minLen := startLen
	if endLen < minLen {
		minLen = endLen
	}

	if len(clean) < minLen {
		return false
	}

	prefix := clean[:minLen]
	return prefix >= startIIN[:minLen] && prefix <= endIIN[:minLen]
}

// GetIIN returns the Issuer Identification Number (first 6-8 digits).
func GetIIN(number string, length int) string {
	clean := CleanCardNumber(number)
	if len(clean) < length {
		return clean
	}
	return clean[:length]
}

// cleanCardForComparison removes separators but keeps asterisks for comparison.
func cleanCardForComparison(number string) string {
	var result strings.Builder
	for _, r := range number {
		if (r >= '0' && r <= '9') || r == '*' {
			result.WriteRune(r)
		}
	}
	return result.String()
}

// CompareCards compares two card numbers and returns if they might be the same card.
// Useful for comparing masked vs full numbers.
func CompareCards(number1, number2 string) bool {
	clean1 := cleanCardForComparison(number1)
	clean2 := cleanCardForComparison(number2)

	// Direct match
	if clean1 == clean2 {
		return true
	}

	// Must have same length for masked comparison
	if len(clean1) != len(clean2) {
		// Check suffix match for shorter all-digits number
		shorter := clean1
		longer := clean2
		if len(clean1) > len(clean2) {
			shorter = clean2
			longer = clean1
		}
		// If shorter is all digits (no asterisks), check suffix match
		if !strings.Contains(shorter, "*") {
			return strings.HasSuffix(longer, shorter)
		}
		return false
	}

	// Handle masked comparison - same length
	for i := 0; i < len(clean1); i++ {
		if clean1[i] == '*' || clean2[i] == '*' {
			continue // Asterisk matches anything
		}
		if clean1[i] != clean2[i] {
			return false
		}
	}

	return true
}