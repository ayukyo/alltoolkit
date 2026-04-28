package roman_numeral_utils

import (
	"testing"
)

func TestToInt(t *testing.T) {
	tests := []struct {
		input    string
		expected int
		hasError bool
	}{
		{"I", 1, false},
		{"II", 2, false},
		{"III", 3, false},
		{"IV", 4, false},
		{"V", 5, false},
		{"VI", 6, false},
		{"IX", 9, false},
		{"X", 10, false},
		{"XIV", 14, false},
		{"XIX", 19, false},
		{"XX", 20, false},
		{"XL", 40, false},
		{"L", 50, false},
		{"XC", 90, false},
		{"C", 100, false},
		{"CD", 400, false},
		{"D", 500, false},
		{"CM", 900, false},
		{"M", 1000, false},
		{"MCMXCIV", 1994, false},
		{"MMXXIV", 2024, false},
		{"MMMCMXCIX", 3999, false},
		{"", 0, true},           // Empty string
		{"IIII", 0, true},       // Invalid (should be IV)
		{"VV", 0, true},         // Invalid (should be X)
		{"IM", 0, true},         // Invalid
		{"ABC", 0, true},        // Invalid characters
		{"MMMM", 0, true},       // Out of range
	}

	for _, test := range tests {
		result, err := ToInt(test.input)
		if test.hasError {
			if err == nil {
				t.Errorf("ToInt(%q) expected error, got %d", test.input, result)
			}
		} else {
			if err != nil {
				t.Errorf("ToInt(%q) unexpected error: %v", test.input, err)
			}
			if result != test.expected {
				t.Errorf("ToInt(%q) = %d, expected %d", test.input, result, test.expected)
			}
		}
	}
}

func TestToIntCaseInsensitive(t *testing.T) {
	tests := []struct {
		lower    string
		upper    string
		expected int
	}{
		{"i", "I", 1},
		{"iv", "IV", 4},
		{"mcmxciv", "MCMXCIV", 1994},
		{"mmxxiv", "MMXXIV", 2024},
	}

	for _, test := range tests {
		resultLower, err := ToInt(test.lower)
		if err != nil {
			t.Errorf("ToInt(%q) error: %v", test.lower, err)
		}
		if resultLower != test.expected {
			t.Errorf("ToInt(%q) = %d, expected %d", test.lower, resultLower, test.expected)
		}

		resultUpper, err := ToInt(test.upper)
		if err != nil {
			t.Errorf("ToInt(%q) error: %v", test.upper, err)
		}
		if resultUpper != test.expected {
			t.Errorf("ToInt(%q) = %d, expected %d", test.upper, resultUpper, test.expected)
		}
	}
}

func TestToRoman(t *testing.T) {
	tests := []struct {
		input    int
		expected string
		hasError bool
	}{
		{1, "I", false},
		{2, "II", false},
		{3, "III", false},
		{4, "IV", false},
		{5, "V", false},
		{9, "IX", false},
		{10, "X", false},
		{14, "XIV", false},
		{19, "XIX", false},
		{40, "XL", false},
		{50, "L", false},
		{90, "XC", false},
		{100, "C", false},
		{400, "CD", false},
		{500, "D", false},
		{900, "CM", false},
		{1000, "M", false},
		{1994, "MCMXCIV", false},
		{2024, "MMXXIV", false},
		{3999, "MMMCMXCIX", false},
		{0, "", true},    // Zero not allowed
		{-1, "", true},   // Negative not allowed
		{4000, "", true}, // Out of range
		{-100, "", true}, // Negative not allowed
	}
	for _, test := range tests {
		result, err := ToRoman(test.input)
		if test.hasError {
			if err == nil {
				t.Errorf("ToRoman(%d) expected error, got %q", test.input, result)
			}
		} else {
			if err != nil {
				t.Errorf("ToRoman(%d) unexpected error: %v", test.input, err)
			}
			if result != test.expected {
				t.Errorf("ToRoman(%d) = %q, expected %q", test.input, result, test.expected)
			}
		}
	}
}

func TestRoundTrip(t *testing.T) {
	// Test that converting to Roman and back gives the same number
	for i := 1; i <= 3999; i++ {
		roman, err := ToRoman(i)
		if err != nil {
			t.Errorf("ToRoman(%d) error: %v", i, err)
			continue
		}

		back, err := ToInt(roman)
		if err != nil {
			t.Errorf("ToInt(%q) error: %v", roman, err)
			continue
		}

		if back != i {
			t.Errorf("Round trip failed: %d -> %q -> %d", i, roman, back)
		}
	}
}

func TestMustToInt(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("MustToInt should panic on invalid input")
		}
	}()

	// Valid case
	if result := MustToInt("XIV"); result != 14 {
		t.Errorf("MustToInt(\"XIV\") = %d, expected 14", result)
	}

	// Invalid case - should panic
	MustToInt("INVALID")
}

func TestMustToRoman(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("MustToRoman should panic on invalid input")
		}
	}()

	// Valid case
	if result := MustToRoman(14); result != "XIV" {
		t.Errorf("MustToRoman(14) = %q, expected \"XIV\"", result)
	}

	// Invalid case - should panic
	MustToRoman(0)
}

func TestIsValid(t *testing.T) {
	tests := []struct {
		input    string
		expected bool
	}{
		{"I", true},
		{"IV", true},
		{"MCMXCIV", true},
		{"", false},
		{"IIII", false},
		{"ABC", false},
		{"IM", false},
		{"xv", true}, // lowercase is valid (ToUpper is called)
	}

	for _, test := range tests {
		result := IsValid(test.input)
		if result != test.expected {
			t.Errorf("IsValid(%q) = %v, expected %v", test.input, result, test.expected)
		}
	}
}

func TestAdd(t *testing.T) {
	tests := []struct {
		roman1   string
		roman2   string
		expected string
		hasError bool
	}{
		{"I", "I", "II", false},
		{"IV", "I", "V", false},
		{"X", "X", "XX", false},
		{"C", "D", "DC", false},
		{"M", "CM", "MCM", false},
		{"", "I", "", true}, // Empty
	}

	for _, test := range tests {
		result, err := Add(test.roman1, test.roman2)
		if test.hasError {
			if err == nil {
				t.Errorf("Add(%q, %q) expected error, got %q", test.roman1, test.roman2, result)
			}
		} else {
			if err != nil {
				t.Errorf("Add(%q, %q) unexpected error: %v", test.roman1, test.roman2, err)
			}
			if result != test.expected {
				t.Errorf("Add(%q, %q) = %q, expected %q", test.roman1, test.roman2, result, test.expected)
			}
		}
	}
}

func TestSubtract(t *testing.T) {
	tests := []struct {
		roman1   string
		roman2   string
		expected string
		hasError bool
	}{
		{"V", "I", "IV", false},
		{"X", "I", "IX", false},
		{"XX", "X", "X", false},
		{"I", "I", "", true}, // Result is 0
		{"I", "V", "", true}, // Result is negative
	}

	for _, test := range tests {
		result, err := Subtract(test.roman1, test.roman2)
		if test.hasError {
			if err == nil {
				t.Errorf("Subtract(%q, %q) expected error, got %q", test.roman1, test.roman2, result)
			}
		} else {
			if err != nil {
				t.Errorf("Subtract(%q, %q) unexpected error: %v", test.roman1, test.roman2, err)
			}
			if result != test.expected {
				t.Errorf("Subtract(%q, %q) = %q, expected %q", test.roman1, test.roman2, result, test.expected)
			}
		}
	}
}

func TestMultiply(t *testing.T) {
	tests := []struct {
		roman1   string
		roman2   string
		expected string
		hasError bool
	}{
		{"I", "I", "I", false},
		{"II", "II", "IV", false},
		{"X", "X", "C", false},
		{"V", "X", "L", false},
		{"C", "X", "M", false},
	}

	for _, test := range tests {
		result, err := Multiply(test.roman1, test.roman2)
		if test.hasError {
			if err == nil {
				t.Errorf("Multiply(%q, %q) expected error, got %q", test.roman1, test.roman2, result)
			}
		} else {
			if err != nil {
				t.Errorf("Multiply(%q, %q) unexpected error: %v", test.roman1, test.roman2, err)
			}
			if result != test.expected {
				t.Errorf("Multiply(%q, %q) = %q, expected %q", test.roman1, test.roman2, result, test.expected)
			}
		}
	}
}

func TestDivide(t *testing.T) {
	tests := []struct {
		roman1   string
		roman2   string
		expected string
		hasError bool
	}{
		{"X", "II", "V", false},
		{"C", "X", "X", false},
		{"V", "I", "V", false},
		{"X", "V", "II", false}, // Integer division: 10 / 5 = 2
		{"I", "I", "I", false},
		{"I", "", "", true}, // Empty
	}

	for _, test := range tests {
		result, err := Divide(test.roman1, test.roman2)
		if test.hasError {
			if err == nil {
				t.Errorf("Divide(%q, %q) expected error, got %q", test.roman1, test.roman2, result)
			}
		} else {
			if err != nil {
				t.Errorf("Divide(%q, %q) unexpected error: %v", test.roman1, test.roman2, err)
			}
			if result != test.expected {
				t.Errorf("Divide(%q, %q) = %q, expected %q", test.roman1, test.roman2, result, test.expected)
			}
		}
	}
}

func TestCompare(t *testing.T) {
	tests := []struct {
		roman1   string
		roman2   string
		expected int
	}{
		{"I", "I", 0},
		{"V", "I", 1},
		{"I", "V", -1},
		{"X", "V", 1},
		{"M", "D", 1},
		{"C", "M", -1},
	}

	for _, test := range tests {
		result, err := Compare(test.roman1, test.roman2)
		if err != nil {
			t.Errorf("Compare(%q, %q) unexpected error: %v", test.roman1, test.roman2, err)
		}
		if result != test.expected {
			t.Errorf("Compare(%q, %q) = %d, expected %d", test.roman1, test.roman2, result, test.expected)
		}
	}
}

func TestGenerateRange(t *testing.T) {
	result, err := GenerateRange(1, 10)
	if err != nil {
		t.Errorf("GenerateRange(1, 10) error: %v", err)
	}

	expected := []string{"I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"}
	for i, exp := range expected {
		if result[i] != exp {
			t.Errorf("GenerateRange result[%d] = %q, expected %q", i, result[i], exp)
		}
	}

	// Test invalid range
	_, err = GenerateRange(0, 10)
	if err == nil {
		t.Error("GenerateRange should error for invalid start")
	}

	_, err = GenerateRange(1, 4000)
	if err == nil {
		t.Error("GenerateRange should error for invalid end")
	}
}

func TestFindHighest(t *testing.T) {
	romans := []string{"I", "V", "X", "L", "C"}
	result, value, err := FindHighest(romans)
	if err != nil {
		t.Errorf("FindHighest error: %v", err)
	}
	if result != "C" {
		t.Errorf("FindHighest result = %q, expected \"C\"", result)
	}
	if value != 100 {
		t.Errorf("FindHighest value = %d, expected 100", value)
	}

	// Test with invalid values mixed in
	romansMixed := []string{"I", "INVALID", "X", "NOTROMAN", "C"}
	result, value, err = FindHighest(romansMixed)
	if err != nil {
		t.Errorf("FindHighest error: %v", err)
	}
	if result != "C" {
		t.Errorf("FindHighest result = %q, expected \"C\"", result)
	}

	// Test with all invalid
	_, _, err = FindHighest([]string{"INVALID", "NOTROMAN"})
	if err == nil {
		t.Error("FindHighest should error when no valid numerals")
	}
}

func TestParseWithAlternative(t *testing.T) {
	// Test standard Roman numerals
	result, err := ParseWithAlternative("MCMXCIV")
	if err != nil {
		t.Errorf("ParseWithAlternative error: %v", err)
	}
	if result != 1994 {
		t.Errorf("ParseWithAlternative(\"MCMXCIV\") = %d, expected 1994", result)
	}

	// Test vinculum notation (for numbers > 3999)
	// _V_ represents V with overline = 5 * 1000 = 5000
	result, err = ParseWithAlternative("_V_")
	if err != nil {
		t.Errorf("ParseWithAlternative error: %v", err)
	}
	if result != 5000 {
		t.Errorf("ParseWithAlternative(\"_V_\") = %d, expected 5000", result)
	}

	// Test combined notation
	// M_V_ = 1000 + 5000 = 6000
	result, err = ParseWithAlternative("M_V_")
	if err != nil {
		t.Errorf("ParseWithAlternative error: %v", err)
	}
	if result != 6000 {
		t.Errorf("ParseWithAlternative(\"M_V_\") = %d, expected 6000", result)
	}
}

func TestGetAll(t *testing.T) {
	numerals := GetAll()
	if len(numerals) != 13 {
		t.Errorf("GetAll returned %d numerals, expected 13", len(numerals))
	}

	// Verify the order is correct (highest to lowest)
	for i := 1; i < len(numerals); i++ {
		if numerals[i].Value >= numerals[i-1].Value {
			t.Errorf("Numerals not in descending order at index %d", i)
		}
	}
}

// Benchmark tests
func BenchmarkToInt(b *testing.B) {
	for i := 0; i < b.N; i++ {
		ToInt("MCMXCIV")
	}
}

func BenchmarkToRoman(b *testing.B) {
	for i := 0; i < b.N; i++ {
		ToRoman(1994)
	}
}

func BenchmarkRoundTrip(b *testing.B) {
	for i := 0; i < b.N; i++ {
		roman, _ := ToRoman(i%3999 + 1)
		ToInt(roman)
	}
}