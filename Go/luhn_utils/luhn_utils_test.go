package luhn_utils

import (
	"strings"
	"testing"
)

func TestStripFormatting(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"4532-0151-1283-0366", "4532015112830366"},
		{"4532 0151 1283 0366", "4532015112830366"},
		{"4532.0151.1283.0366", "4532015112830366"},
		{"4532015112830366", "4532015112830366"},
		{"", ""},
		{"abcd", ""},
	}

	for _, tt := range tests {
		result := StripFormatting(tt.input)
		if result != tt.expected {
			t.Errorf("StripFormatting(%q) = %q, want %q", tt.input, result, tt.expected)
		}
	}
}

func TestValidate(t *testing.T) {
	tests := []struct {
		number   string
		expected bool
	}{
		// Valid credit card numbers
		{"4532015112830366", true},   // Visa
		{"5500000000000004", true},   // MasterCard
		{"378282246310005", true},    // American Express
		{"6011111111111117", true},   // Discover
		{"3530111333300000", true},   // JCB
		{"30569309025904", true},     // Diners Club
		{"6221260000000000", true},   // UnionPay
		
		// Invalid numbers
		{"4532015112830367", false},  // Wrong check digit
		{"5500000000000005", false},  // Wrong check digit
		{"1234567890123456", false},  // Random invalid
		{"", false},
		{"123", false},  // Too short
		
		// With formatting
		{"4532-0151-1283-0366", true},  // Valid with dashes
		{"4532 0151 1283 0366", true},  // Valid with spaces
	}

	for _, tt := range tests {
		result := Validate(tt.number)
		if result != tt.expected {
			t.Errorf("Validate(%q) = %v, want %v", tt.number, result, tt.expected)
		}
	}
}

func TestCalculateCheckDigit(t *testing.T) {
	tests := []struct {
		number         string
		expectedDigit  int
		expectError    bool
	}{
		{"453201511283036", 6, false},
		{"550000000000000", 4, false},
		{"37828224631000", 5, false},
		{"601111111111111", 7, false},
		{"", 0, true},  // Empty should error
		{"abc", 0, true}, // No digits should error
	}

	for _, tt := range tests {
		result, err := CalculateCheckDigit(tt.number)
		if tt.expectError {
			if err == nil {
				t.Errorf("CalculateCheckDigit(%q) expected error, got none", tt.number)
			}
		} else {
			if err != nil {
				t.Errorf("CalculateCheckDigit(%q) unexpected error: %v", tt.number, err)
			}
			if result != tt.expectedDigit {
				t.Errorf("CalculateCheckDigit(%q) = %d, want %d", tt.number, result, tt.expectedDigit)
			}
		}
	}
}

func TestAddCheckDigit(t *testing.T) {
	tests := []struct {
		number         string
		expectedResult string
		expectError    bool
	}{
		{"453201511283036", "4532015112830366", false},
		{"550000000000000", "5500000000000004", false},
		{"37828224631000", "378282246310005", false},
	}

	for _, tt := range tests {
		result, err := AddCheckDigit(tt.number)
		if tt.expectError {
			if err == nil {
				t.Errorf("AddCheckDigit(%q) expected error, got none", tt.number)
			}
		} else {
			if err != nil {
				t.Errorf("AddCheckDigit(%q) unexpected error: %v", tt.number, err)
			}
			if result != tt.expectedResult {
				t.Errorf("AddCheckDigit(%q) = %q, want %q", tt.number, result, tt.expectedResult)
			}
			// Verify the result is valid
			if !Validate(result) {
				t.Errorf("AddCheckDigit(%q) result %q is not valid", tt.number, result)
			}
		}
	}
}

func TestFormatNumber(t *testing.T) {
	tests := []struct {
		number     string
		groupSize  int
		separator  string
		expected   string
	}{
		{"4532015112830366", 4, " ", "4532 0151 1283 0366"},
		{"4532015112830366", 4, "-", "4532-0151-1283-0366"},
		{"4532015112830366", 2, ".", "45.32.01.51.12.83.03.66"},
		{"378282246310005", 4, " ", "3782 8224 6310 005"},
		{"", 4, " ", ""},
	}

	for _, tt := range tests {
		result := FormatNumber(tt.number, tt.groupSize, tt.separator)
		if result != tt.expected {
			t.Errorf("FormatNumber(%q, %d, %q) = %q, want %q", 
				tt.number, tt.groupSize, tt.separator, result, tt.expected)
		}
	}
}

func TestGenerateValidNumber(t *testing.T) {
	tests := []struct {
		prefix      string
		length      int
		expectError bool
	}{
		{"4", 16, false},    // Visa-like
		{"5", 16, false},    // MasterCard-like
		{"34", 15, false},   // Amex-like
		{"", 16, true},      // Empty prefix
		{"4", 1, true},      // Length too short
	}

	for _, tt := range tests {
		result, err := GenerateValidNumber(tt.prefix, tt.length)
		if tt.expectError {
			if err == nil {
				t.Errorf("GenerateValidNumber(%q, %d) expected error, got none", tt.prefix, tt.length)
			}
		} else {
			if err != nil {
				t.Errorf("GenerateValidNumber(%q, %d) unexpected error: %v", tt.prefix, tt.length, err)
				continue
			}
			
			// Verify length
			if len(result) != tt.length {
				t.Errorf("GenerateValidNumber(%q, %d) length = %d, want %d", 
					tt.prefix, tt.length, len(result), tt.length)
			}
			
			// Verify prefix
			cleanPrefix := StripFormatting(tt.prefix)
			if !strings.HasPrefix(result, cleanPrefix) {
				t.Errorf("GenerateValidNumber(%q, %d) result %q doesn't start with prefix", 
					tt.prefix, tt.length, result)
			}
			
			// Verify it passes Luhn validation
			if !Validate(result) {
				t.Errorf("GenerateValidNumber(%q, %d) result %q is not valid", 
					tt.prefix, tt.length, result)
			}
		}
	}
}

func TestGenerateBatch(t *testing.T) {
	count := 5
	results, err := GenerateBatch("4", count, 16)
	if err != nil {
		t.Fatalf("GenerateBatch unexpected error: %v", err)
	}
	
	if len(results) != count {
		t.Errorf("GenerateBatch count = %d, want %d", len(results), count)
	}
	
	// Verify all are unique (with high probability for valid random generation)
	seen := make(map[string]bool)
	for _, num := range results {
		if seen[num] {
			t.Errorf("GenerateBatch generated duplicate: %s", num)
		}
		seen[num] = true
		
		if !Validate(num) {
			t.Errorf("GenerateBatch generated invalid number: %s", num)
		}
	}
}

func TestIdentifyCardType(t *testing.T) {
	tests := []struct {
		number          string
		expectedType    string
	}{
		{"4111111111111111", "visa"},
		{"5500000000000004", "mastercard"},
		{"378282246310005", "amex"},
		{"6011111111111117", "discover"},
		{"3530111333300000", "jcb"},
		{"30569309025904", "diners"},
		{"6222000000000000", "unionpay"},  // UnionPay (6222 prefix, not overlapping with Discover)
		{"1234567890123456", ""},  // Unknown type
		{"", ""},  // Empty
	}

	for _, tt := range tests {
		result := IdentifyCardType(tt.number)
		if result != tt.expectedType {
			t.Errorf("IdentifyCardType(%q) = %q, want %q", tt.number, result, tt.expectedType)
		}
	}
}

func TestCalculateLuhnSum(t *testing.T) {
	// Valid Visa card
	sum, valid := CalculateLuhnSum("4532015112830366")
	if !valid {
		t.Errorf("CalculateLuhnSum valid card should be valid")
	}
	if sum%10 != 0 {
		t.Errorf("CalculateLuhnSum sum = %d, should be divisible by 10", sum)
	}
	
	// Invalid number
	_, valid = CalculateLuhnSum("4532015112830367")
	if valid {
		t.Errorf("CalculateLuhnSum invalid card should be invalid")
	}
	
	// Empty string
	_, valid = CalculateLuhnSum("")
	if valid {
		t.Errorf("CalculateLuhnSum empty should be invalid")
	}
}

func TestFindCheckDigitErrors(t *testing.T) {
	// Valid number should return nil
	errors := FindCheckDigitErrors("4532015112830366")
	if errors != nil {
		t.Errorf("FindCheckDigitErrors valid number should return nil, got %v", errors)
	}
	
	// Invalid number should find some positions
	errors = FindCheckDigitErrors("4532015112830367")
	if len(errors) == 0 {
		t.Errorf("FindCheckDigitErrors invalid number should find errors")
	}
	
	// Empty should return nil
	errors = FindCheckDigitErrors("")
	if errors != nil {
		t.Errorf("FindCheckDigitErrors empty should return nil, got %v", errors)
	}
}

func TestValidator(t *testing.T) {
	v := NewValidator(4, "-")
	
	// Test Validate
	if !v.Validate("4532015112830366") {
		t.Error("Validator.Validate failed for valid number")
	}
	
	// Test CalculateCheckDigit
	digit, err := v.CalculateCheckDigit("453201511283036")
	if err != nil || digit != 6 {
		t.Errorf("Validator.CalculateCheckDigit = %d, want 6", digit)
	}
	
	// Test AddCheckDigit
	full, err := v.AddCheckDigit("453201511283036")
	if err != nil || full != "4532015112830366" {
		t.Errorf("Validator.AddCheckDigit = %q, want %q", full, "4532015112830366")
	}
	
	// Test Format
	formatted := v.Format("4532015112830366")
	if formatted != "4532-0151-1283-0366" {
		t.Errorf("Validator.Format = %q, want %q", formatted, "4532-0151-1283-0366")
	}
	
	// Test Strip
	stripped := v.Strip("4532-0151-1283-0366")
	if stripped != "4532015112830366" {
		t.Errorf("Validator.Strip = %q, want %q", stripped, "4532015112830366")
	}
	
	// Test Generate
	generated, err := v.Generate("4", 16)
	if err != nil {
		t.Errorf("Validator.Generate error: %v", err)
	}
	if len(generated) != 16 {
		t.Errorf("Validator.Generate length = %d, want 16", len(generated))
	}
	if !v.Validate(generated) {
		t.Errorf("Validator.Generate result %q is not valid", generated)
	}
	
	// Test GenerateBatch
	batch, err := v.GenerateBatch("4", 3, 16)
	if err != nil {
		t.Errorf("Validator.GenerateBatch error: %v", err)
	}
	if len(batch) != 3 {
		t.Errorf("Validator.GenerateBatch count = %d, want 3", len(batch))
	}
}

func TestGenerateTestCreditCards(t *testing.T) {
	cards := GenerateTestCreditCards(2)
	
	if len(cards) == 0 {
		t.Error("GenerateTestCreditCards should generate at least some cards")
	}
	
	// All cards should be valid
	for _, card := range cards {
		if !Validate(card.Number) {
			t.Errorf("GenerateTestCreditCards generated invalid card: %s (%s)", 
				card.Type, card.Number)
		}
		
		// Type should be non-empty
		if card.Type == "" {
			t.Error("GenerateTestCreditCards should have non-empty type")
		}
	}
}

// Benchmark tests
func BenchmarkValidate(b *testing.B) {
	for i := 0; i < b.N; i++ {
		Validate("4532015112830366")
	}
}

func BenchmarkCalculateCheckDigit(b *testing.B) {
	for i := 0; i < b.N; i++ {
		CalculateCheckDigit("453201511283036")
	}
}

func BenchmarkGenerateValidNumber(b *testing.B) {
	for i := 0; i < b.N; i++ {
		GenerateValidNumber("4", 16)
	}
}