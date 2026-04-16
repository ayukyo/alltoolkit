package base64_utils

import (
	"bytes"
	"os"
	"strings"
	"testing"
)

func TestEncode(t *testing.T) {
	tests := []struct {
		name     string
		input    []byte
		encType  EncodingType
		expected string
	}{
		{"Standard", []byte("Hello, World!"), Standard, "SGVsbG8sIFdvcmxkIQ=="},
		{"URLSafe", []byte("Hello, World!"), URLSafe, "SGVsbG8sIFdvcmxkIQ=="},
		{"RawStandard", []byte("Hello, World!"), RawStandard, "SGVsbG8sIFdvcmxkIQ"},
		{"RawURLSafe", []byte("Hello, World!"), RawURLSafe, "SGVsbG8sIFdvcmxkIQ"},
		{"Empty", []byte{}, Standard, ""},
		{"Binary", []byte{0x00, 0x01, 0x02, 0xFF}, Standard, "AAEC/w=="},
		{"URLChars", []byte("?query=value&foo=bar"), URLSafe, "P3F1ZXJ5PXZhbHVlJmZvbz1iYXI="},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := Encode(tt.input, tt.encType)
			if result != tt.expected {
				t.Errorf("Encode() = %v, want %v", result, tt.expected)
			}
		})
	}
}

func TestEncodeString(t *testing.T) {
	tests := []struct {
		name     string
		input    string
		encType  EncodingType
		expected string
	}{
		{"Standard", "Hello, World!", Standard, "SGVsbG8sIFdvcmxkIQ=="},
		{"Empty", "", Standard, ""},
		{"SpecialChars", "!@#$%^&*()", Standard, "IUAjJCVeJiooKQ=="},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := EncodeString(tt.input, tt.encType)
			if result != tt.expected {
				t.Errorf("EncodeString() = %v, want %v", result, tt.expected)
			}
		})
	}
}

func TestDecode(t *testing.T) {
	tests := []struct {
		name     string
		input    string
		encType  EncodingType
		expected string
		hasError bool
	}{
		{"Standard", "SGVsbG8sIFdvcmxkIQ==", Standard, "Hello, World!", false},
		{"URLSafe", "SGVsbG8sIFdvcmxkIQ==", URLSafe, "Hello, World!", false},
		{"RawStandard", "SGVsbG8sIFdvcmxkIQ", RawStandard, "Hello, World!", false},
		{"RawURLSafe", "SGVsbG8sIFdvcmxkIQ", RawURLSafe, "Hello, World!", false},
		{"Empty", "", Standard, "", true},
		{"Invalid", "!!!invalid!!!", Standard, "", true},
		{"Binary", "AAEC/w==", Standard, "\x00\x01\x02\xff", false},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := Decode(tt.input, tt.encType)
			if tt.hasError {
				if err == nil {
					t.Error("Decode() expected error, got nil")
				}
			} else {
				if err != nil {
					t.Errorf("Decode() unexpected error: %v", err)
				}
				if string(result) != tt.expected {
					t.Errorf("Decode() = %v, want %v", string(result), tt.expected)
				}
			}
		})
	}
}

func TestDecodeString(t *testing.T) {
	result, err := DecodeString("SGVsbG8sIFdvcmxkIQ==", Standard)
	if err != nil {
		t.Errorf("DecodeString() unexpected error: %v", err)
	}
	if result != "Hello, World!" {
		t.Errorf("DecodeString() = %v, want %v", result, "Hello, World!")
	}
}

func TestAutoDecode(t *testing.T) {
	tests := []struct {
		name     string
		input    string
		expected string
		hasError bool
	}{
		{"Standard", "SGVsbG8sIFdvcmxkIQ==", "Hello, World!", false},
		{"RawStandard", "SGVsbG8sIFdvcmxkIQ", "Hello, World!", false},
		{"NoPadding", "SGVsbG8sIFdvcmxkIQ", "Hello, World!", false},
		{"Empty", "", "", true},
		{"Invalid", "!!!invalid!!!", "", true},
		{"Special", "P3F1ZXJ5PXZhbHVl", "?query=value", false},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := AutoDecode(tt.input)
			if tt.hasError {
				if err == nil {
					t.Error("AutoDecode() expected error, got nil")
				}
			} else {
				if err != nil {
					t.Errorf("AutoDecode() unexpected error: %v", err)
				}
				if string(result) != tt.expected {
					t.Errorf("AutoDecode() = %v, want %v", string(result), tt.expected)
				}
			}
		})
	}
}

func TestEncodeDecodeRoundTrip(t *testing.T) {
	testStrings := []string{
		"Hello, World!",
		"The quick brown fox jumps over the lazy dog.",
		"12345",
		"!@#$%^&*()",
		"",
		"Binary: \x00\x01\x02\xFF",
		strings.Repeat("A", 1000),
	}

	for _, s := range testStrings {
		encoded := EncodeString(s)
		decoded, err := DecodeString(encoded)
		if err != nil {
			t.Errorf("Round trip failed for %q: %v", s, err)
		}
		if decoded != s {
			t.Errorf("Round trip mismatch: got %q, want %q", decoded, s)
		}
	}
}

func TestIsValid(t *testing.T) {
	tests := []struct {
		name     string
		input    string
		expected bool
	}{
		{"Valid", "SGVsbG8sIFdvcmxkIQ==", true},
		{"ValidNoPadding", "SGVsbG8sIFdvcmxkIQ", false}, // Standard requires padding
		{"Empty", "", false},
		{"InvalidChars", "!!!invalid!!!", false},
		{"ValidSimple", "YWJjZA==", true},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := IsValid(tt.input)
			if result != tt.expected {
				t.Errorf("IsValid() = %v, want %v", result, tt.expected)
			}
		})
	}
}

func TestIsValidAny(t *testing.T) {
	tests := []struct {
		name     string
		input    string
		expected bool
	}{
		{"ValidStandard", "SGVsbG8sIFdvcmxkIQ==", true},
		{"ValidRaw", "SGVsbG8sIFdvcmxkIQ", true},
		{"Empty", "", false},
		{"Invalid", "!!!invalid!!!", false},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := IsValidAny(tt.input)
			if result != tt.expected {
				t.Errorf("IsValidAny() = %v, want %v", result, tt.expected)
			}
		})
	}
}

func TestAddRemovePadding(t *testing.T) {
	tests := []struct {
		name     string
		input    string
		expected string
	}{
		{"NoPadding", "SGVsbG8sIFdvcmxkIQ", "SGVsbG8sIFdvcmxkIQ=="},
		{"WithPadding", "YWJjZA==", "YWJjZA=="},
		{"AlreadyPadded", "AAAA", "AAAA"},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := AddPadding(tt.input)
			if result != tt.expected {
				t.Errorf("AddPadding() = %v, want %v", result, tt.expected)
			}

			// Test RemovePadding
			removed := RemovePadding(tt.expected)
			if strings.Contains(tt.expected, "=") && strings.Contains(removed, "=") {
				t.Errorf("RemovePadding() should remove all =, got %v", removed)
			}
		})
	}
}

func TestGetEncodingType(t *testing.T) {
	tests := []struct {
		name        string
		input       string
		expected    EncodingType
		expectError bool
	}{
		{"Standard", "SGVsbG8sIFdvcmxkIQ==", Standard, false},
		{"URLSafe", "P3F1ZXJ5PXZhbHVlJmZvbz1iYXI=", URLSafe, false},
		{"Empty", "", Standard, true},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := GetEncodingType(tt.input)
			if tt.expectError {
				if err == nil {
					t.Error("GetEncodingType() expected error, got nil")
				}
			} else {
				if err != nil {
					t.Errorf("GetEncodingType() unexpected error: %v", err)
				}
				if result != tt.expected {
					t.Errorf("GetEncodingType() = %v, want %v", result, tt.expected)
				}
			}
		})
	}
}

func TestConvertEncoding(t *testing.T) {
	standard := "SGVsbG8sIFdvcmxkIQ=="
	
	// Convert standard to URLSafe
	result, err := ConvertEncoding(standard, Standard, URLSafe)
	if err != nil {
		t.Errorf("ConvertEncoding() error: %v", err)
	}
	if result != standard {
		t.Errorf("ConvertEncoding() = %v, want %v", result, standard)
	}

	// Convert standard to RawStandard
	rawResult, err := ConvertEncoding(standard, Standard, RawStandard)
	if err != nil {
		t.Errorf("ConvertEncoding() error: %v", err)
	}
	if rawResult != "SGVsbG8sIFdvcmxkIQ" {
		t.Errorf("ConvertEncoding() = %v, want %v", rawResult, "SGVsbG8sIFdvcmxkIQ")
	}
}

func TestChunkedEncodeDecode(t *testing.T) {
	// Create a string longer than 76 chars
	longStr := strings.Repeat("Hello World! ", 20)
	
	encoded := ChunkedEncode([]byte(longStr))
	
	// Check that lines are broken
	if len(encoded) > 76 && !strings.Contains(encoded, "\n") {
		t.Error("ChunkedEncode() should contain newlines for long strings")
	}

	decoded, err := ChunkedDecode(encoded)
	if err != nil {
		t.Errorf("ChunkedDecode() error: %v", err)
	}
	if string(decoded) != longStr {
		t.Error("ChunkedDecode() round trip failed")
	}
}

func TestEncodeDecodeLines(t *testing.T) {
	lines := []string{"Hello", "World", "Test"}
	
	encoded := EncodeLines(lines)
	if len(encoded) != len(lines) {
		t.Errorf("EncodeLines() length = %v, want %v", len(encoded), len(lines))
	}
	
	decoded, err := DecodeLines(encoded)
	if err != nil {
		t.Errorf("DecodeLines() error: %v", err)
	}
	
	for i, line := range lines {
		if decoded[i] != line {
			t.Errorf("DecodeLines()[%d] = %v, want %v", i, decoded[i], line)
		}
	}
}

func TestFileOperations(t *testing.T) {
	// Create temp file
	tmpFile := "/tmp/base64_test_file.txt"
	testContent := "Hello, File World!"
	
	err := os.WriteFile(tmpFile, []byte(testContent), 0644)
	if err != nil {
		t.Fatalf("Failed to create test file: %v", err)
	}
	defer os.Remove(tmpFile)

	// Test EncodeFile
	encoded, err := EncodeFile(tmpFile)
	if err != nil {
		t.Errorf("EncodeFile() error: %v", err)
	}
	if encoded != EncodeString(testContent) {
		t.Error("EncodeFile() content mismatch")
	}

	// Test DecodeToFile
	outputFile := "/tmp/base64_test_output.txt"
	defer os.Remove(outputFile)
	
	err = DecodeToFile(encoded, outputFile)
	if err != nil {
		t.Errorf("DecodeToFile() error: %v", err)
	}
	
	content, err := os.ReadFile(outputFile)
	if err != nil {
		t.Errorf("Failed to read output file: %v", err)
	}
	if string(content) != testContent {
		t.Errorf("DecodeToFile() content = %v, want %v", string(content), testContent)
	}

	// Test non-existent file
	_, err = EncodeFile("/nonexistent/file.txt")
	if err != ErrFileNotFound {
		t.Errorf("EncodeFile() should return ErrFileNotFound for missing file")
	}
}

func TestEncodeReader(t *testing.T) {
	testContent := "Hello, Reader!"
	reader := bytes.NewReader([]byte(testContent))
	
	encoded, err := EncodeReader(reader)
	if err != nil {
		t.Errorf("EncodeReader() error: %v", err)
	}
	
	expected := EncodeString(testContent)
	if encoded != expected {
		t.Errorf("EncodeReader() = %v, want %v", encoded, expected)
	}
}

func TestSafeEncodeDecode(t *testing.T) {
	original := "Hello, Safe World!"
	
	encoded := SafeEncodeString(original)
	if encoded != EncodeString(original) {
		t.Error("SafeEncodeString() should match EncodeString()")
	}
	
	// Test safe decode with valid input
	decoded := SafeDecodeString(encoded)
	if decoded != original {
		t.Errorf("SafeDecodeString() = %v, want %v", decoded, original)
	}
	
	// Test safe decode with invalid input - should return original
	invalid := "!!!invalid!!!"
	result := SafeDecodeString(invalid)
	if result != invalid {
		t.Errorf("SafeDecodeString() with invalid input should return original, got %v", result)
	}
}

func TestSize(t *testing.T) {
	tests := []struct {
		input    int
		expected int
	}{
		{0, 0},
		{1, 4},
		{2, 4},
		{3, 4},
		{4, 8},
		{5, 8},
		{6, 8},
		{100, 136},
	}

	for _, tt := range tests {
		result := Size(tt.input)
		if result != tt.expected {
			t.Errorf("Size(%d) = %v, want %v", tt.input, result, tt.expected)
		}
	}
}

func TestDecodeSize(t *testing.T) {
	tests := []struct {
		input    int
		expected int
	}{
		{0, 0},
		{4, 3},
		{8, 6},
		{100, 75},
	}

	for _, tt := range tests {
		result := DecodeSize(tt.input)
		if result != tt.expected {
			t.Errorf("DecodeSize(%d) = %v, want %v", tt.input, result, tt.expected)
		}
	}
}

func TestDecodeWriter(t *testing.T) {
	original := "Hello, Writer!"
	encoded := EncodeString(original)
	
	var buf bytes.Buffer
	writer := NewDecodeWriter(&buf)
	
	n, err := writer.Write([]byte(encoded))
	if err != nil {
		t.Errorf("DecodeWriter.Write() error: %v", err)
	}
	if n != len(encoded) {
		t.Errorf("DecodeWriter.Write() n = %v, want %v", n, len(encoded))
	}
	
	if buf.String() != original {
		t.Errorf("DecodeWriter output = %v, want %v", buf.String(), original)
	}
}

func BenchmarkEncode(b *testing.B) {
	data := []byte(strings.Repeat("Hello, World! ", 100))
	for i := 0; i < b.N; i++ {
		Encode(data)
	}
}

func BenchmarkDecode(b *testing.B) {
	data := []byte(strings.Repeat("Hello, World! ", 100))
	encoded := Encode(data)
	for i := 0; i < b.N; i++ {
		Decode(encoded)
	}
}

func BenchmarkAutoDecode(b *testing.B) {
	data := []byte(strings.Repeat("Hello, World! ", 100))
	encoded := Encode(data)
	for i := 0; i < b.N; i++ {
		AutoDecode(encoded)
	}
}