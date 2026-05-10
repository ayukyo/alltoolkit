package ordinal_utils

import (
	"testing"
)

func TestToOrdinalEnglish(t *testing.T) {
	oc := NewOrdinalConverter(English)

	tests := []struct {
		input    int
		expected string
	}{
		{1, "1st"},
		{2, "2nd"},
		{3, "3rd"},
		{4, "4th"},
		{5, "5th"},
		{10, "10th"},
		{11, "11th"},
		{12, "12th"},
		{13, "13th"},
		{14, "14th"},
		{21, "21st"},
		{22, "22nd"},
		{23, "23rd"},
		{24, "24th"},
		{101, "101st"},
		{102, "102nd"},
		{103, "103rd"},
		{111, "111th"},
		{112, "112th"},
		{113, "113th"},
	}

	for _, tt := range tests {
		result, err := oc.ToOrdinal(tt.input)
		if err != nil {
			t.Errorf("ToOrdinal(%d) returned error: %v", tt.input, err)
			continue
		}
		if result != tt.expected {
			t.Errorf("ToOrdinal(%d) = %q, want %q", tt.input, result, tt.expected)
		}
	}
}

func TestToOrdinalShort(t *testing.T) {
	oc := NewOrdinalConverter(English)

	result, err := oc.ToOrdinalShort(1)
	if err != nil || result != "1st" {
		t.Errorf("ToOrdinalShort(1) = %q, %v, want 1st, nil", result, err)
	}

	result, err = oc.ToOrdinalShort(2)
	if err != nil || result != "2nd" {
		t.Errorf("ToOrdinalShort(2) = %q, %v, want 2nd, nil", result, err)
	}

	result, err = oc.ToOrdinalShort(3)
	if err != nil || result != "3rd" {
		t.Errorf("ToOrdinalShort(3) = %q, %v, want 3rd, nil", result, err)
	}

	result, err = oc.ToOrdinalShort(11)
	if err != nil || result != "11th" {
		t.Errorf("ToOrdinalShort(11) = %q, %v, want 11th, nil", result, err)
	}
}

func TestParseOrdinal(t *testing.T) {
	oc := NewOrdinalConverter(English)

	tests := []struct {
		input    string
		expected int
		hasError bool
	}{
		{"1st", 1, false},
		{"2nd", 2, false},
		{"3rd", 3, false},
		{"4th", 4, false},
		{"11th", 11, false},
		{"21st", 21, false},
		{"22nd", 22, false},
		{"23rd", 23, false},
		{"first", 1, false},
		{"second", 2, false},
		{"third", 3, false},
		{"tenth", 10, false},
		{"twentieth", 20, false},
		{"invalid", 0, true},
		{"", 0, true},
	}

	for _, tt := range tests {
		result, err := oc.ParseOrdinal(tt.input)
		if tt.hasError {
			if err == nil {
				t.Errorf("ParseOrdinal(%q) expected error, got none", tt.input)
			}
		} else {
			if err != nil {
				t.Errorf("ParseOrdinal(%q) returned error: %v", tt.input, err)
				continue
			}
			if result != tt.expected {
				t.Errorf("ParseOrdinal(%q) = %d, want %d", tt.input, result, tt.expected)
			}
		}
	}
}

func TestInvalidInput(t *testing.T) {
	oc := NewOrdinalConverter(English)

	_, err := oc.ToOrdinal(0)
	if err == nil {
		t.Error("ToOrdinal(0) should return error")
	}

	_, err = oc.ToOrdinal(-1)
	if err == nil {
		t.Error("ToOrdinal(-1) should return error")
	}

	_, err = oc.ToOrdinalShort(0)
	if err == nil {
		t.Error("ToOrdinalShort(0) should return error")
	}

	_, err = oc.ToOrdinalShort(-5)
	if err == nil {
		t.Error("ToOrdinalShort(-5) should return error")
	}
}

func TestToOrdinalRange(t *testing.T) {
	oc := NewOrdinalConverter(English)

	result, err := oc.ToOrdinalRange(1, 5)
	if err != nil {
		t.Errorf("ToOrdinalRange(1, 5) returned error: %v", err)
	}

	expected := []string{"1st", "2nd", "3rd", "4th", "5th"}
	if len(result) != len(expected) {
		t.Errorf("ToOrdinalRange(1, 5) returned %d items, want %d", len(result), len(expected))
	}

	for i, v := range result {
		if v != expected[i] {
			t.Errorf("ToOrdinalRange(1, 5)[%d] = %q, want %q", i, v, expected[i])
		}
	}

	_, err = oc.ToOrdinalRange(5, 1)
	if err == nil {
		t.Error("ToOrdinalRange(5, 1) should return error")
	}

	_, err = oc.ToOrdinalRange(0, 5)
	if err == nil {
		t.Error("ToOrdinalRange(0, 5) should return error")
	}
}

func TestOtherLanguages(t *testing.T) {
	tests := []struct {
		lang     Language
		n        int
		contains string
	}{
		{Spanish, 1, "1"},
		{Spanish, 2, "2"},
		{French, 1, "er"},
		{French, 2, "e"},
		{German, 1, "1."},
		{German, 2, "2."},
		{Italian, 1, "1"},
		{Italian, 2, "2"},
	}

	for _, tt := range tests {
		oc := NewOrdinalConverter(tt.lang)
		result, err := oc.ToOrdinal(tt.n)
		if err != nil {
			t.Errorf("ToOrdinal(%d, %s) returned error: %v", tt.n, tt.lang, err)
			continue
		}
		if result == "" {
			t.Errorf("ToOrdinal(%d, %s) returned empty string", tt.n, tt.lang)
		}
	}
}

func TestToWordOrdinal(t *testing.T) {
	tests := []struct {
		input    int
		expected string
		hasError bool
	}{
		{1, "first", false},
		{2, "second", false},
		{3, "third", false},
		{4, "fourth", false},
		{5, "fifth", false},
		{10, "tenth", false},
		{20, "twentieth", false},
		{0, "", true},
		{21, "", true},
	}

	for _, tt := range tests {
		result, err := ToWordOrdinal(tt.input)
		if tt.hasError {
			if err == nil {
				t.Errorf("ToWordOrdinal(%d) expected error, got none", tt.input)
			}
		} else {
			if err != nil {
				t.Errorf("ToWordOrdinal(%d) returned error: %v", tt.input, err)
				continue
			}
			if result != tt.expected {
				t.Errorf("ToWordOrdinal(%d) = %q, want %q", tt.input, result, tt.expected)
			}
		}
	}
}

func TestOrdinalList(t *testing.T) {
	items := []string{"apple", "banana", "cherry"}
	result := OrdinalList(items)

	expected := []string{"1st apple", "2nd banana", "3rd cherry"}
	for i, v := range result {
		if v != expected[i] {
			t.Errorf("OrdinalList()[%d] = %q, want %q", i, v, expected[i])
		}
	}
}

func TestBatchToOrdinal(t *testing.T) {
	numbers := []int{1, 2, 3, 11, 21, 22, 23}
	result, err := BatchToOrdinal(numbers, English)
	if err != nil {
		t.Errorf("BatchToOrdinal returned error: %v", err)
	}

	expected := []string{"1st", "2nd", "3rd", "11th", "21st", "22nd", "23rd"}
	for i, v := range result {
		if v != expected[i] {
			t.Errorf("BatchToOrdinal()[%d] = %q, want %q", i, v, expected[i])
		}
	}

	// Test with invalid number
	invalidNumbers := []int{1, 2, 0, 4}
	_, err = BatchToOrdinal(invalidNumbers, English)
	if err == nil {
		t.Error("BatchToOrdinal with 0 should return error")
	}
}

func TestGetOrdinalSuffix(t *testing.T) {
	tests := []struct {
		input    int
		expected string
	}{
		{1, "st"},
		{2, "nd"},
		{3, "rd"},
		{4, "th"},
		{11, "th"},
		{12, "th"},
		{13, "th"},
		{21, "st"},
		{22, "nd"},
		{23, "rd"},
		{101, "st"},
	}

	for _, tt := range tests {
		result, err := GetOrdinalSuffix(tt.input)
		if err != nil {
			t.Errorf("GetOrdinalSuffix(%d) returned error: %v", tt.input, err)
			continue
		}
		if result != tt.expected {
			t.Errorf("GetOrdinalSuffix(%d) = %q, want %q", tt.input, result, tt.expected)
		}
	}

	_, err := GetOrdinalSuffix(0)
	if err == nil {
		t.Error("GetOrdinalSuffix(0) should return error")
	}
}

func TestIsOrdinal(t *testing.T) {
	oc := NewOrdinalConverter(English)

	validOrdinals := []string{"1st", "2nd", "3rd", "11th", "first", "second"}
	invalidOrdinals := []string{"abc", "1xyz", ""}

	for _, s := range validOrdinals {
		if !oc.IsOrdinal(s) {
			t.Errorf("IsOrdinal(%q) should return true", s)
		}
	}

	for _, s := range invalidOrdinals {
		if oc.IsOrdinal(s) {
			t.Errorf("IsOrdinal(%q) should return false", s)
		}
	}
}

// Benchmark tests
func BenchmarkToOrdinal(b *testing.B) {
	oc := NewOrdinalConverter(English)
	for i := 0; i < b.N; i++ {
		_, _ = oc.ToOrdinal(i%1000 + 1)
	}
}

func BenchmarkToOrdinalShort(b *testing.B) {
	oc := NewOrdinalConverter(English)
	for i := 0; i < b.N; i++ {
		_, _ = oc.ToOrdinalShort(i%1000 + 1)
	}
}

func BenchmarkBatchToOrdinal(b *testing.B) {
	numbers := make([]int, 100)
	for i := range numbers {
		numbers[i] = i + 1
	}

	for i := 0; i < b.N; i++ {
		_, _ = BatchToOrdinal(numbers, English)
	}
}

func BenchmarkParseOrdinal(b *testing.B) {
	oc := NewOrdinalConverter(English)
	for i := 0; i < b.N; i++ {
		_, _ = oc.ParseOrdinal("123rd")
	}
}