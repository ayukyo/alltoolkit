package isbn_utils

import (
	"testing"
)

func TestClean(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"978-3-16-148410-0", "9783161484100"},
		{"0-306-40615-2", "0306406152"},
		{"ISBN 0-306-40615-2", "0306406152"},
		{"978 3 16 148410 0", "9783161484100"},
		{"0306406152", "0306406152"},
		{"0-19-852663-6", "0198526636"},
		{"0-8044-2957-X", "080442957X"},
	}

	for _, tt := range tests {
		result := Clean(tt.input)
		if result != tt.expected {
			t.Errorf("Clean(%q) = %q, want %q", tt.input, result, tt.expected)
		}
	}
}

func TestValidateISBN10(t *testing.T) {
	tests := []struct {
		isbn     string
		expected bool
	}{
		// Valid ISBN-10s
		{"0306406152", true},      // Valid
		{"0-306-40615-2", true},   // Valid with hyphens
		{"080442957X", true},      // Valid with X check digit
		{"0-8044-2957-X", true},   // Valid with X and hyphens
		{"0198526636", true},      // Valid
		{"0596007973", true},      // Valid
		{"0321334876", true},      // Valid
		
		// Invalid ISBN-10s
		{"0306406153", false},     // Wrong check digit
		{"0804429570", false},     // Wrong check digit (should be X)
		{"123456789", false},      // Too short
		{"12345678901", false},    // Too long
		{"ABCDEFGHIJ", false},     // Non-numeric
		{"", false},               // Empty
	}

	for _, tt := range tests {
		valid, _ := ValidateISBN10(tt.isbn)
		if valid != tt.expected {
			t.Errorf("ValidateISBN10(%q) = %v, want %v", tt.isbn, valid, tt.expected)
		}
	}
}

func TestValidateISBN13(t *testing.T) {
	tests := []struct {
		isbn     string
		expected bool
	}{
		// Valid ISBN-13s
		{"9783161484100", true},      // Valid
		{"978-3-16-148410-0", true},  // Valid with hyphens
		{"9780306406157", true},      // Valid
		{"9780596007977", true},      // Valid
		{"9791091146135", true},      // Valid 979 prefix
		{"9780321334876", true},      // Valid
		
		// Invalid ISBN-13s
		{"9783161484101", false},     // Wrong check digit
		{"9780306406158", false},     // Wrong check digit
		{"123456789012", false},      // Too short
		{"12345678901234", false},   // Too long
		{"ABCDEFGHIJKLM", false},    // Non-numeric
		{"", false},                  // Empty
	}

	for _, tt := range tests {
		valid, _ := ValidateISBN13(tt.isbn)
		if valid != tt.expected {
			t.Errorf("ValidateISBN13(%q) = %v, want %v", tt.isbn, valid, tt.expected)
		}
	}
}

func TestValidate(t *testing.T) {
	tests := []struct {
		isbn     string
		expected bool
	}{
		{"0306406152", true},        // Valid ISBN-10
		{"9783161484100", true},     // Valid ISBN-13
		{"0-306-40615-2", true},     // Valid ISBN-10 with hyphens
		{"080442957X", true},        // Valid ISBN-10 with X
		{"12345", false},            // Invalid length
		{"", false},                 // Empty
	}

	for _, tt := range tests {
		valid, _ := Validate(tt.isbn)
		if valid != tt.expected {
			t.Errorf("Validate(%q) = %v, want %v", tt.isbn, valid, tt.expected)
		}
	}
}

func TestGenerateCheckDigit10(t *testing.T) {
	tests := []struct {
		prefix   string
		expected string
		hasError bool
	}{
		{"030640615", "2", false},
		{"080442957", "X", false},
		{"019852663", "6", false},
		{"059600797", "3", false},
		{"12345678", "", true},   // Too short
		{"1234567890", "", true}, // Too long
		{"ABCDEFGHI", "", true},  // Non-numeric
	}

	for _, tt := range tests {
		result, err := GenerateCheckDigit10(tt.prefix)
		if tt.hasError {
			if err == nil {
				t.Errorf("GenerateCheckDigit10(%q) expected error, got none", tt.prefix)
			}
		} else {
			if err != nil {
				t.Errorf("GenerateCheckDigit10(%q) unexpected error: %v", tt.prefix, err)
			}
			if result != tt.expected {
				t.Errorf("GenerateCheckDigit10(%q) = %q, want %q", tt.prefix, result, tt.expected)
			}
		}
	}
}

func TestGenerateCheckDigit13(t *testing.T) {
	tests := []struct {
		prefix   string
		expected string
		hasError bool
	}{
		{"978316148410", "0", false},
		{"978030640615", "7", false},
		{"978059600797", "7", false},
		{"978032133487", "6", false},
		{"12345678901", "", true},   // Too short
		{"1234567890123", "", true}, // Too long
		{"ABCDEFGHIJKL", "", true},  // Non-numeric
	}

	for _, tt := range tests {
		result, err := GenerateCheckDigit13(tt.prefix)
		if tt.hasError {
			if err == nil {
				t.Errorf("GenerateCheckDigit13(%q) expected error, got none", tt.prefix)
			}
		} else {
			if err != nil {
				t.Errorf("GenerateCheckDigit13(%q) unexpected error: %v", tt.prefix, err)
			}
			if result != tt.expected {
				t.Errorf("GenerateCheckDigit13(%q) = %q, want %q", tt.prefix, result, tt.expected)
			}
		}
	}
}

func TestToISBN13(t *testing.T) {
	tests := []struct {
		isbn10   string
		expected string
		hasError bool
	}{
		{"0306406152", "9780306406157", false},
		{"0-306-40615-2", "9780306406157", false},
		{"080442957X", "9780804429571", false},
		{"0-8044-2957-X", "9780804429571", false},
		{"0198526636", "9780198526637", false},
		{"12345", "", true},  // Invalid length
	}

	for _, tt := range tests {
		result, err := ToISBN13(tt.isbn10)
		if tt.hasError {
			if err == nil {
				t.Errorf("ToISBN13(%q) expected error, got none", tt.isbn10)
			}
		} else {
			if err != nil {
				t.Errorf("ToISBN13(%q) unexpected error: %v", tt.isbn10, err)
			}
			if result != tt.expected {
				t.Errorf("ToISBN13(%q) = %q, want %q", tt.isbn10, result, tt.expected)
			}
		}
	}
}

func TestToISBN10(t *testing.T) {
	tests := []struct {
		isbn13   string
		expected string
		hasError bool
	}{
		{"9780306406157", "0306406152", false},
		{"978-0-306-40615-7", "0306406152", false},
		{"9780804429571", "080442957X", false},
		{"9780198526637", "0198526636", false},
		{"9791091146135", "", true},  // 979 prefix cannot be converted to ISBN-10
		{"12345", "", true},           // Invalid length
	}

	for _, tt := range tests {
		result, err := ToISBN10(tt.isbn13)
		if tt.hasError {
			if err == nil {
				t.Errorf("ToISBN10(%q) expected error, got none", tt.isbn13)
			}
		} else {
			if err != nil {
				t.Errorf("ToISBN10(%q) unexpected error: %v", tt.isbn13, err)
			}
			if result != tt.expected {
				t.Errorf("ToISBN10(%q) = %q, want %q", tt.isbn13, result, tt.expected)
			}
		}
	}
}

func TestFormat(t *testing.T) {
	tests := []struct {
		isbn     string
		expected string
	}{
		{"0306406152", "0-30640-615-2"},
		{"9783161484100", "978-3-16148-410-0"},
		{"080442957X", "0-80442-957-X"},
		{"9780306406157", "978-0-30640-615-7"},
	}

	for _, tt := range tests {
		result := Format(tt.isbn)
		if result != tt.expected {
			t.Errorf("Format(%q) = %q, want %q", tt.isbn, result, tt.expected)
		}
	}
}

func TestGetType(t *testing.T) {
	tests := []struct {
		isbn         string
		expectedType string
		hasError     bool
	}{
		{"0306406152", TypeISBN10, false},
		{"9783161484100", TypeISBN13, false},
		{"12345", "", true},
	}

	for _, tt := range tests {
		result, err := GetType(tt.isbn)
		if tt.hasError {
			if err == nil {
				t.Errorf("GetType(%q) expected error, got none", tt.isbn)
			}
		} else {
			if err != nil {
				t.Errorf("GetType(%q) unexpected error: %v", tt.isbn, err)
			}
			if result != tt.expectedType {
				t.Errorf("GetType(%q) = %q, want %q", tt.isbn, result, tt.expectedType)
			}
		}
	}
}

func TestIsISBN(t *testing.T) {
	if !IsISBN("0306406152") {
		t.Error("IsISBN('0306406152') should be true")
	}
	if !IsISBN("9783161484100") {
		t.Error("IsISBN('9783161484100') should be true")
	}
	if IsISBN("12345") {
		t.Error("IsISBN('12345') should be false")
	}
}

func TestIsISBN10(t *testing.T) {
	if !IsISBN10("0306406152") {
		t.Error("IsISBN10('0306406152') should be true")
	}
	if IsISBN10("9783161484100") {
		t.Error("IsISBN10('9783161484100') should be false")
	}
}

func TestIsISBN13(t *testing.T) {
	if !IsISBN13("9783161484100") {
		t.Error("IsISBN13('9783161484100') should be true")
	}
	if IsISBN13("0306406152") {
		t.Error("IsISBN13('0306406152') should be false")
	}
}

func TestNormalize(t *testing.T) {
	tests := []struct {
		isbn     string
		expected string
		hasError bool
	}{
		{"0306406152", "9780306406157", false},    // ISBN-10 to ISBN-13
		{"9783161484100", "9783161484100", false}, // Already ISBN-13
		{"12345", "", true},                       // Invalid
	}

	for _, tt := range tests {
		result, err := Normalize(tt.isbn)
		if tt.hasError {
			if err == nil {
				t.Errorf("Normalize(%q) expected error, got none", tt.isbn)
			}
		} else {
			if err != nil {
				t.Errorf("Normalize(%q) unexpected error: %v", tt.isbn, err)
			}
			if result != tt.expected {
				t.Errorf("Normalize(%q) = %q, want %q", tt.isbn, result, tt.expected)
			}
		}
	}
}

func TestGenerateISBN13(t *testing.T) {
	result, err := GenerateISBN13("978316148410")
	if err != nil {
		t.Errorf("GenerateISBN13 unexpected error: %v", err)
	}
	if result != "9783161484100" {
		t.Errorf("GenerateISBN13 = %q, want %q", result, "9783161484100")
	}

	_, err = GenerateISBN13("12345")
	if err == nil {
		t.Error("GenerateISBN13 should return error for invalid prefix length")
	}
}

func TestGenerateISBN10(t *testing.T) {
	result, err := GenerateISBN10("030640615")
	if err != nil {
		t.Errorf("GenerateISBN10 unexpected error: %v", err)
	}
	if result != "0306406152" {
		t.Errorf("GenerateISBN10 = %q, want %q", result, "0306406152")
	}

	result, err = GenerateISBN10("080442957")
	if err != nil {
		t.Errorf("GenerateISBN10 unexpected error: %v", err)
	}
	if result != "080442957X" {
		t.Errorf("GenerateISBN10 = %q, want %q", result, "080442957X")
	}

	_, err = GenerateISBN10("12345678")
	if err == nil {
		t.Error("GenerateISBN10 should return error for invalid prefix length")
	}
}

func TestParse(t *testing.T) {
	// Test ISBN-10
	isbn10, err := Parse("0306406152")
	if err != nil {
		t.Errorf("Parse ISBN-10 unexpected error: %v", err)
	}
	if isbn10.Type != TypeISBN10 {
		t.Errorf("Parse ISBN-10 type = %q, want %q", isbn10.Type, TypeISBN10)
	}
	if isbn10.Number != "0306406152" {
		t.Errorf("Parse ISBN-10 number = %q, want %q", isbn10.Number, "0306406152")
	}
	if isbn10.Check != "2" {
		t.Errorf("Parse ISBN-10 check = %q, want %q", isbn10.Check, "2")
	}

	// Test ISBN-13
	isbn13, err := Parse("9783161484100")
	if err != nil {
		t.Errorf("Parse ISBN-13 unexpected error: %v", err)
	}
	if isbn13.Type != TypeISBN13 {
		t.Errorf("Parse ISBN-13 type = %q, want %q", isbn13.Type, TypeISBN13)
	}
	if isbn13.Number != "9783161484100" {
		t.Errorf("Parse ISBN-13 number = %q, want %q", isbn13.Number, "9783161484100")
	}
	if isbn13.Prefix != "978" {
		t.Errorf("Parse ISBN-13 prefix = %q, want %q", isbn13.Prefix, "978")
	}

	// Test invalid
	_, err = Parse("12345")
	if err == nil {
		t.Error("Parse should return error for invalid ISBN")
	}
}

// Benchmark tests
func BenchmarkValidateISBN10(b *testing.B) {
	for i := 0; i < b.N; i++ {
		ValidateISBN10("0306406152")
	}
}

func BenchmarkValidateISBN13(b *testing.B) {
	for i := 0; i < b.N; i++ {
		ValidateISBN13("9783161484100")
	}
}

func BenchmarkToISBN13(b *testing.B) {
	for i := 0; i < b.N; i++ {
		ToISBN13("0306406152")
	}
}

func BenchmarkFormat(b *testing.B) {
	for i := 0; i < b.N; i++ {
		Format("9783161484100")
	}
}