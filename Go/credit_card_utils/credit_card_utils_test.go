package credit_card_utils

import (
	"strings"
	"testing"
)

// ============================================================================
// Luhn Algorithm Tests
// ============================================================================

func TestLuhnCheck(t *testing.T) {
	tests := []struct {
		number   string
		expected bool
	}{
		{"4111111111111111", true},  // Valid Visa
		{"5500000000000004", true},  // Valid Mastercard
		{"378282246310005", true},   // Valid Amex
		{"6011111111111117", true},  // Valid Discover
		{"3530111333300000", true},  // Valid JCB
		{"4111111111111112", false}, // Invalid check digit
		{"1234567890123456", false}, // Random invalid
		{"", false},                 // Empty
		{"123", false},              // Too short
		{"4111-1111-1111-1111", true}, // With dashes
		{"4111 1111 1111 1111", true}, // With spaces
		{"abcd1234efgh5678", false},   // Non-digits
	}

	for _, test := range tests {
		result := LuhnCheck(test.number)
		if result != test.expected {
			t.Errorf("LuhnCheck(%q) = %v, expected %v", test.number, result, test.expected)
		}
	}
}

func TestCalculateLuhnDigit(t *testing.T) {
	tests := []struct {
		number   string
		expected int
	}{
		{"411111111111111", 1}, // Visa test number
		{"550000000000000", 4}, // Mastercard test number
		{"37828224631000", 5},  // Amex test number
		{"1234567890", 3},     // Random number
	}

	for _, test := range tests {
		result := CalculateLuhnDigit(test.number)
		if result != test.expected {
			t.Errorf("CalculateLuhnDigit(%q) = %d, expected %d", test.number, result, test.expected)
		}
		// Verify: number + digit should pass Luhn
		fullNumber := test.number + string(rune('0'+result))
		if !LuhnCheck(fullNumber) {
			t.Errorf("LuhnCheck(%q) should be true after adding check digit", fullNumber)
		}
	}
}

// ============================================================================
// Card Number Cleaning and Formatting Tests
// ============================================================================

func TestCleanCardNumber(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"4111-1111-1111-1111", "4111111111111111"},
		{"4111 1111 1111 1111", "4111111111111111"},
		{"4111 1111-1111 1111", "4111111111111111"},
		{"  4111111111111111  ", "4111111111111111"},
		{"4111a1111b1111c1111", "4111111111111111"},
		{"4111111111111111", "4111111111111111"},
	}

	for _, test := range tests {
		result := CleanCardNumber(test.input)
		if result != test.expected {
			t.Errorf("CleanCardNumber(%q) = %q, expected %q", test.input, result, test.expected)
		}
	}
}

func TestFormatCardNumber(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"4111111111111111", "4111 1111 1111 1111"},
		{"378282246310005", "3782 8224 6310 005"},
		{"123", "123"},
	}

	for _, test := range tests {
		result := FormatCardNumber(test.input)
		if result != test.expected {
			t.Errorf("FormatCardNumber(%q) = %q, expected %q", test.input, result, test.expected)
		}
	}
}

func TestFormatCardNumberCustom(t *testing.T) {
	tests := []struct {
		input    string
		groups   []int
		expected string
	}{
		{"378282246310005", []int{4, 6, 5}, "3782 822463 10005"},
		{"4111111111111111", []int{4, 4, 4, 4}, "4111 1111 1111 1111"},
		{"12345678", []int{2, 2, 2, 2}, "12 34 56 78"},
	}

	for _, test := range tests {
		result := FormatCardNumberCustom(test.input, test.groups)
		if result != test.expected {
			t.Errorf("FormatCardNumberCustom(%q, %v) = %q, expected %q", test.input, test.groups, result, test.expected)
		}
	}
}

func TestMaskCardNumber(t *testing.T) {
	tests := []struct {
		number     string
		showFirst  int
		showLast   int
		expected   string
	}{
		{"4111111111111111", 4, 4, "4111********1111"}, // 16 digits: 4 + 8 stars + 4
		{"378282246310005", 4, 4, "3782*******0005"},  // 15 digits: 4 + 7 stars + 4
		{"123456", 2, 2, "12**56"},                    // 6 digits: 2 + 2 stars + 2
		{"12345", 2, 2, "12*45"},                      // 5 digits: 2 + 1 star + 2
		{"1234", 2, 2, "1234"},                        // Exactly 4 digits, no masking
	}

	for _, test := range tests {
		result := MaskCardNumber(test.number, test.showFirst, test.showLast)
		if result != test.expected {
			t.Errorf("MaskCardNumber(%q, %d, %d) = %q, expected %q", test.number, test.showFirst, test.showLast, result, test.expected)
		}
	}
}

func TestMaskCardNumberDefault(t *testing.T) {
	result := MaskCardNumberDefault("4111111111111111")
	expected := "4111********1111"
	if result != expected {
		t.Errorf("MaskCardNumberDefault() = %q, expected %q", result, expected)
	}
}

// ============================================================================
// Card Type Identification Tests
// ============================================================================

func TestIdentifyCardType(t *testing.T) {
	tests := []struct {
		number   string
		expected CardType
	}{
		{"4111111111111111", CardTypeVisa},
		{"4012888888881881", CardTypeVisa},
		{"5500000000000004", CardTypeMastercard},
		{"2221000000000009", CardTypeMastercard},
		{"378282246310005", CardTypeAmex},
		{"371449635398431", CardTypeAmex},
		{"6011111111111117", CardTypeDiscover},
		{"3530111333300000", CardTypeJCB},
		{"30000000000004", CardTypeDinersClub},
		{"6221260000000000", CardTypeUnionPay},
		{"5018000000000000", CardTypeMaestro},
		{"1234567890123456", CardTypeUnknown},
	}

	for _, test := range tests {
		result := IdentifyCardType(test.number)
		if result != test.expected {
			t.Errorf("IdentifyCardType(%q) = %q, expected %q", test.number, result, test.expected)
		}
	}
}

func TestGetCardInfo(t *testing.T) {
	info := GetCardInfo("4111111111111111")

	if info.Type != CardTypeVisa {
		t.Errorf("Expected CardTypeVisa, got %q", info.Type)
	}
	if !info.Valid {
		t.Error("Expected valid Luhn check")
	}
	if info.Length != 16 {
		t.Errorf("Expected length 16, got %d", info.Length)
	}
	if info.CVVLength != 3 {
		t.Errorf("Expected CVV length 3, got %d", info.CVVLength)
	}
	if info.IIN != "411111" {
		t.Errorf("Expected IIN 411111, got %q", info.IIN)
	}
}

func TestIsValidCardNumber(t *testing.T) {
	tests := []struct {
		number   string
		expected bool
	}{
		{"4111111111111111", true},  // Valid Visa
		{"5500000000000004", true},  // Valid Mastercard
		{"378282246310005", true},   // Valid Amex
		{"4111111111111112", false}, // Invalid Luhn
		{"41111111111111", false},   // Wrong length for Visa
		{"1234567890123456", false}, // Invalid Luhn
	}

	for _, test := range tests {
		result := IsValidCardNumber(test.number)
		if result != test.expected {
			t.Errorf("IsValidCardNumber(%q) = %v, expected %v", test.number, result, test.expected)
		}
	}
}

func TestGetExpectedLengths(t *testing.T) {
	visaLengths := GetExpectedLengths(CardTypeVisa)
	if len(visaLengths) == 0 {
		t.Error("Expected non-empty lengths for Visa")
	}
	found16 := false
	for _, l := range visaLengths {
		if l == 16 {
			found16 = true
		}
	}
	if !found16 {
		t.Error("Expected 16 in Visa lengths")
	}

	unknownLengths := GetExpectedLengths(CardTypeUnknown)
	if unknownLengths != nil {
		t.Error("Expected nil for unknown card type")
	}
}

func TestGetCVVLength(t *testing.T) {
	tests := []struct {
		cardType CardType
		expected int
	}{
		{CardTypeVisa, 3},
		{CardTypeMastercard, 3},
		{CardTypeAmex, 4},
		{CardTypeDiscover, 3},
		{CardTypeUnknown, 3},
	}

	for _, test := range tests {
		result := GetCVVLength(test.cardType)
		if result != test.expected {
			t.Errorf("GetCVVLength(%q) = %d, expected %d", test.cardType, result, test.expected)
		}
	}
}

// ============================================================================
// CVV Validation Tests
// ============================================================================

func TestIsValidCVV(t *testing.T) {
	tests := []struct {
		cvv      string
		cardType CardType
		expected bool
	}{
		{"123", CardTypeVisa, true},
		{"1234", CardTypeVisa, false},
		{"1234", CardTypeAmex, true},
		{"123", CardTypeAmex, false},
		{"12", CardTypeVisa, false},
		{"abc", CardTypeVisa, false},
		{"", CardTypeVisa, false},
	}

	for _, test := range tests {
		result := IsValidCVV(test.cvv, test.cardType)
		if result != test.expected {
			t.Errorf("IsValidCVV(%q, %q) = %v, expected %v", test.cvv, test.cardType, result, test.expected)
		}
	}
}

func TestIsValidCVVForNumber(t *testing.T) {
	// Visa (3-digit CVV)
	if !IsValidCVVForNumber("123", "4111111111111111") {
		t.Error("Expected valid CVV for Visa")
	}
	if IsValidCVVForNumber("1234", "4111111111111111") {
		t.Error("Expected invalid 4-digit CVV for Visa")
	}

	// Amex (4-digit CVV)
	if !IsValidCVVForNumber("1234", "378282246310005") {
		t.Error("Expected valid CVV for Amex")
	}
	if IsValidCVVForNumber("123", "378282246310005") {
		t.Error("Expected invalid 3-digit CVV for Amex")
	}
}

// ============================================================================
// Expiry Date Tests
// ============================================================================

func TestParseExpiryDate(t *testing.T) {
	tests := []struct {
		input        string
		expectedYear int
		expectedMon  int
		expectError  bool
	}{
		{"12/25", 2025, 12, false},
		{"01/26", 2026, 1, false},
		{"12/2025", 2025, 12, false},
		{"01-2026", 2026, 1, false},
		{"13/25", 0, 0, true},  // Invalid month
		{"00/25", 0, 0, true},  // Invalid month
		{"1/25", 0, 0, true},   // Invalid format
		{"abc", 0, 0, true},    // Invalid input
	}

	for _, test := range tests {
		year, month, err := ParseExpiryDate(test.input)
		if test.expectError {
			if err == nil {
				t.Errorf("ParseExpiryDate(%q) expected error, got none", test.input)
			}
		} else {
			if err != nil {
				t.Errorf("ParseExpiryDate(%q) unexpected error: %v", test.input, err)
			}
			if year != test.expectedYear {
				t.Errorf("ParseExpiryDate(%q) year = %d, expected %d", test.input, year, test.expectedYear)
			}
			if month != test.expectedMon {
				t.Errorf("ParseExpiryDate(%q) month = %d, expected %d", test.input, month, test.expectedMon)
			}
		}
	}
}

func TestFormatExpiryDate(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"12/25", "12/25"},
		{"01/26", "01/26"},
		{"12/2025", "12/25"},
	}

	for _, test := range tests {
		result := FormatExpiryDate(test.input)
		if result != test.expected {
			t.Errorf("FormatExpiryDate(%q) = %q, expected %q", test.input, result, test.expected)
		}
	}
}

// ============================================================================
// Test Card Generation Tests
// ============================================================================

func TestGenerateTestCardNumber(t *testing.T) {
	cardTypes := []CardType{
		CardTypeVisa,
		CardTypeMastercard,
		CardTypeAmex,
		CardTypeDiscover,
		CardTypeJCB,
		CardTypeDinersClub,
	}

	for _, cardType := range cardTypes {
		number := GenerateTestCardNumber(cardType)

		// Should pass Luhn check
		if !LuhnCheck(number) {
			t.Errorf("Generated number for %q failed Luhn check: %s", cardType, number)
		}

		// Should be identified as correct type
		identified := IdentifyCardType(number)
		if identified != cardType {
			t.Errorf("Generated number for %q identified as %q", cardType, identified)
		}

		// Should be valid
		if !IsValidCardNumber(number) {
			t.Errorf("Generated number for %q is not valid: %s", cardType, number)
		}
	}
}

func TestGenerateTestCard(t *testing.T) {
	number, cvv, expiry := GenerateTestCard(CardTypeVisa)

	// Validate generated values
	if !LuhnCheck(number) {
		t.Errorf("Generated card number failed Luhn check: %s", number)
	}

	if len(cvv) != 3 {
		t.Errorf("Generated CVV has wrong length: %s", cvv)
	}

	if len(expiry) != 5 {
		t.Errorf("Generated expiry has wrong format: %s", expiry)
	}
}

// ============================================================================
// Validation Tests
// ============================================================================

func TestValidateCard(t *testing.T) {
	// Valid card, no CVV/expiry
	result := ValidateCard("4111111111111111", "", "")
	if !result.Valid {
		t.Errorf("Expected valid card, got errors: %v", result.Errors)
	}
	if result.CardType != CardTypeVisa {
		t.Errorf("Expected Visa, got %q", result.CardType)
	}
	if !result.LuhnValid {
		t.Error("Expected Luhn valid")
	}
	if !result.LengthValid {
		t.Error("Expected length valid")
	}

	// Invalid card
	result = ValidateCard("4111111111111112", "", "")
	if result.Valid {
		t.Error("Expected invalid card")
	}
	if len(result.Errors) == 0 {
		t.Error("Expected errors for invalid card")
	}

	// With CVV
	result = ValidateCard("4111111111111111", "123", "")
	if !result.Valid {
		t.Errorf("Expected valid card with CVV, got errors: %v", result.Errors)
	}

	// Invalid CVV
	result = ValidateCard("4111111111111111", "1234", "")
	if result.Valid {
		t.Error("Expected invalid card with wrong CVV length")
	}
}

// ============================================================================
// Card Range Utilities Tests
// ============================================================================

func TestIsInCardRange(t *testing.T) {
	tests := []struct {
		number   string
		start    string
		end      string
		expected bool
	}{
		{"4111111111111111", "400000", "499999", true},  // Visa range
		{"5500000000000004", "510000", "559999", true},  // Mastercard range
		{"378282246310005", "340000", "349999", false}, // Amex starts with 37
	}

	for _, test := range tests {
		result := IsInCardRange(test.number, test.start, test.end)
		if result != test.expected {
			t.Errorf("IsInCardRange(%q, %q, %q) = %v, expected %v", test.number, test.start, test.end, result, test.expected)
		}
	}
}

func TestGetIIN(t *testing.T) {
	tests := []struct {
		number   string
		length   int
		expected string
	}{
		{"4111111111111111", 6, "411111"},
		{"378282246310005", 8, "37828224"},
		{"12345", 6, "12345"}, // Shorter than requested length
	}

	for _, test := range tests {
		result := GetIIN(test.number, test.length)
		if result != test.expected {
			t.Errorf("GetIIN(%q, %d) = %q, expected %q", test.number, test.length, result, test.expected)
		}
	}
}

func TestCompareCards(t *testing.T) {
	tests := []struct {
		card1    string
		card2    string
		expected bool
	}{
		{"4111111111111111", "4111111111111111", true},
		{"4111111111111111", "4111 1111 1111 1111", true},
		{"4111********1111", "4111111111111111", true},
		{"4111111111111111", "4111********1111", true},
		{"4111111111111111", "5500000000000004", false},
		{"1111", "4111111111111111", true}, // Suffix match
	}

	for _, test := range tests {
		result := CompareCards(test.card1, test.card2)
		if result != test.expected {
			t.Errorf("CompareCards(%q, %q) = %v, expected %v", test.card1, test.card2, result, test.expected)
		}
	}
}

// ============================================================================
// Edge Cases
// ============================================================================

func TestEmptyInput(t *testing.T) {
	// Empty number
	if LuhnCheck("") {
		t.Error("Expected LuhnCheck('') to be false")
	}
	if IdentifyCardType("") != CardTypeUnknown {
		t.Error("Expected empty number to be Unknown type")
	}

	// Clean
	if CleanCardNumber("") != "" {
		t.Error("Expected clean of empty to be empty")
	}

	// Format
	if FormatCardNumber("") != "" {
		t.Error("Expected format of empty to be empty")
	}
}

func TestSpecialCharacters(t *testing.T) {
	// Numbers with various separators
	number := "4111-1111-1111-1111"
	clean := CleanCardNumber(number)
	if strings.ContainsAny(clean, "- ") {
		t.Errorf("CleanCardNumber should remove all non-digits, got %q", clean)
	}
	if !LuhnCheck(number) {
		t.Error("LuhnCheck should handle numbers with separators")
	}
}

func TestAmexSpecialFormat(t *testing.T) {
	// Amex has 15 digits and 4-digit CVV
	info := GetCardInfo("378282246310005")
	if info.Type != CardTypeAmex {
		t.Errorf("Expected Amex, got %q", info.Type)
	}
	if info.Length != 15 {
		t.Errorf("Expected length 15, got %d", info.Length)
	}
	if info.CVVLength != 4 {
		t.Errorf("Expected CVV length 4, got %d", info.CVVLength)
	}

	// Amex format is typically 4-6-5
	formatted := FormatCardNumberCustom("378282246310005", []int{4, 6, 5})
	expected := "3782 822463 10005"
	if formatted != expected {
		t.Errorf("FormatCardNumberCustom = %q, expected %q", formatted, expected)
	}
}

func TestUnknownCardType(t *testing.T) {
	// Unknown card type
	info := GetCardInfo("1234567890123456")
	if info.Type != CardTypeUnknown {
		t.Errorf("Expected Unknown type, got %q", info.Type)
	}

	// Should still check Luhn
	if info.Valid {
		t.Error("Random number should fail Luhn check")
	}
}

// ============================================================================
// Benchmark Tests
// ============================================================================

func BenchmarkLuhnCheck(b *testing.B) {
	for i := 0; i < b.N; i++ {
		LuhnCheck("4111111111111111")
	}
}

func BenchmarkIdentifyCardType(b *testing.B) {
	for i := 0; i < b.N; i++ {
		IdentifyCardType("4111111111111111")
	}
}

func BenchmarkGenerateTestCardNumber(b *testing.B) {
	for i := 0; i < b.N; i++ {
		GenerateTestCardNumber(CardTypeVisa)
	}
}

func BenchmarkValidateCard(b *testing.B) {
	for i := 0; i < b.N; i++ {
		ValidateCard("4111111111111111", "123", "12/25")
	}
}