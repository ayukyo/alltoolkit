package hexutils

import (
	"testing"
)

func TestHexEncode(t *testing.T) {
	tests := []struct {
		input    []byte
		expected string
	}{
		{[]byte{0x48, 0x65, 0x6c, 0x6c, 0x6f}, "48656c6c6f"}, // "Hello"
		{[]byte{0x00}, "00"},
		{[]byte{0xff}, "ff"},
		{[]byte{}, ""},
		{[]byte{0x0d, 0x0a}, "0d0a"},
	}

	for _, tt := range tests {
		result := HexEncode(tt.input)
		if result != tt.expected {
			t.Errorf("HexEncode(%v) = %s; want %s", tt.input, result, tt.expected)
		}
	}
}

func TestHexDecode(t *testing.T) {
	tests := []struct {
		input    string
		expected []byte
		hasError bool
	}{
		{"48656c6c6f", []byte{0x48, 0x65, 0x6c, 0x6c, 0x6f}, false},
		{"00", []byte{0x00}, false},
		{"ff", []byte{0xff}, false},
		{"FF", []byte{0xff}, false},
		{"", nil, true},      // empty
		{"0", nil, true},     // odd length
		{"xyz", nil, true},   // invalid chars
		{"0d0a", []byte{0x0d, 0x0a}, false},
	}

	for _, tt := range tests {
		result, err := HexDecode(tt.input)
		if tt.hasError {
			if err == nil {
				t.Errorf("HexDecode(%s) expected error, got nil", tt.input)
			}
		} else {
			if err != nil {
				t.Errorf("HexDecode(%s) unexpected error: %v", tt.input, err)
			}
			if string(result) != string(tt.expected) {
				t.Errorf("HexDecode(%s) = %v; want %v", tt.input, result, tt.expected)
			}
		}
	}
}

func TestHexEncodeString(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"Hello", "48656c6c6f"},
		{"", ""},
		{"ABC", "414243"},
		{"123", "313233"},
	}

	for _, tt := range tests {
		result := HexEncodeString(tt.input)
		if result != tt.expected {
			t.Errorf("HexEncodeString(%s) = %s; want %s", tt.input, result, tt.expected)
		}
	}
}

func TestHexDecodeToString(t *testing.T) {
	tests := []struct {
		input    string
		expected string
		hasError bool
	}{
		{"48656c6c6f", "Hello", false},
		{"414243", "ABC", false},
		{"", "", true},
		{"xyz", "", true},
	}

	for _, tt := range tests {
		result, err := HexDecodeToString(tt.input)
		if tt.hasError {
			if err == nil {
				t.Errorf("HexDecodeToString(%s) expected error, got nil", tt.input)
			}
		} else {
			if err != nil {
				t.Errorf("HexDecodeToString(%s) unexpected error: %v", tt.input, err)
			}
			if result != tt.expected {
				t.Errorf("HexDecodeToString(%s) = %s; want %s", tt.input, result, tt.expected)
			}
		}
	}
}

func TestIsHex(t *testing.T) {
	tests := []struct {
		input    string
		expected bool
	}{
		{"48656c6c6f", true},
		{"ABCDEF", true},
		{"abcdef", true},
		{"123456", true},
		{"", false},
		{"0", false},     // odd length
		{"xyz", false},   // invalid chars
		{"123g", false},  // invalid char 'g'
		{"GG", false},    // invalid chars
	}

	for _, tt := range tests {
		result := IsHex(tt.input)
		if result != tt.expected {
			t.Errorf("IsHex(%s) = %v; want %v", tt.input, result, tt.expected)
		}
	}
}

func TestHexEncodeUpper(t *testing.T) {
	input := []byte{0xab, 0xcd, 0xef}
	result := HexEncodeUpper(input)
	expected := "ABCDEF"
	if result != expected {
		t.Errorf("HexEncodeUpper(%v) = %s; want %s", input, result, expected)
	}
}

func TestHexDecodeIgnoreCase(t *testing.T) {
	// Lowercase
	result1, err := HexDecodeIgnoreCase("abcdef")
	if err != nil {
		t.Errorf("HexDecodeIgnoreCase(abcdef) unexpected error: %v", err)
	}
	if string(result1) != "\xab\xcd\xef" {
		t.Errorf("HexDecodeIgnoreCase(abcdef) = %v; want [ab cd ef]", result1)
	}

	// Uppercase
	result2, err := HexDecodeIgnoreCase("ABCDEF")
	if err != nil {
		t.Errorf("HexDecodeIgnoreCase(ABCDEF) unexpected error: %v", err)
	}
	if string(result2) != "\xab\xcd\xef" {
		t.Errorf("HexDecodeIgnoreCase(ABCDEF) = %v; want [ab cd ef]", result2)
	}

	// Mixed case
	result3, err := HexDecodeIgnoreCase("AbCdEf")
	if err != nil {
		t.Errorf("HexDecodeIgnoreCase(AbCdEf) unexpected error: %v", err)
	}
	if string(result3) != "\xab\xcd\xef" {
		t.Errorf("HexDecodeIgnoreCase(AbCdEf) = %v; want [ab cd ef]", result3)
	}
}

func TestHexDump(t *testing.T) {
	// Test with sample data
	data := []byte("Hello, World! This is a hex dump test.")
	result := HexDump(data)
	
	if result == "" {
		t.Error("HexDump returned empty string for non-empty input")
	}
	
	// Check that output contains expected elements
	if !containsStr(result, "00000000") {
		t.Error("HexDump output should contain offset")
	}
}

func TestHexDumpCompact(t *testing.T) {
	data := []byte{0x48, 0x65, 0x6c, 0x6c, 0x6f}
	result := HexDumpCompact(data)
	expected := "48 65 6c 6c 6f"
	if result != expected {
		t.Errorf("HexDumpCompact() = %s; want %s", result, expected)
	}

	// Empty input
	if HexDumpCompact([]byte{}) != "" {
		t.Error("HexDumpCompact([]byte{}) should return empty string")
	}
}

func TestHexDumpCStyle(t *testing.T) {
	data := []byte{0x48, 0x65, 0x6c, 0x6c, 0x6f}
	result := HexDumpCStyle(data, "myData")
	
	if !containsStr(result, "unsigned char myData[]") {
		t.Errorf("HexDumpCStyle should contain C array declaration, got: %s", result)
	}
	if !containsStr(result, "0x48") {
		t.Error("HexDumpCStyle should contain hex values")
	}

	// Empty input
	emptyResult := HexDumpCStyle([]byte{}, "empty")
	if emptyResult != "unsigned char empty[] = {};" {
		t.Errorf("HexDumpCStyle([]byte{}) = %s; want 'unsigned char empty[] = {};' ", emptyResult)
	}
}

func TestHexDumpPythonStyle(t *testing.T) {
	data := []byte{0x48, 0x65, 0x6c, 0x6c, 0x6f}
	result := HexDumpPythonStyle(data)
	
	if !containsStr(result, "b'") {
		t.Errorf("HexDumpPythonStyle should start with b', got: %s", result)
	}
	if !containsStr(result, "\\x48") {
		t.Error("HexDumpPythonStyle should contain hex escape sequences")
	}

	// Empty input
	if HexDumpPythonStyle([]byte{}) != "b''" {
		t.Error("HexDumpPythonStyle([]byte{}) should return b''")
	}
}

func TestReverseHex(t *testing.T) {
	tests := []struct {
		input    string
		expected string
		hasError bool
	}{
		{"12345678", "78563412", false},
		{"aabbccdd", "ddccbbaa", false},
		{"", "", true},
		{"xyz", "", true},
	}

	for _, tt := range tests {
		result, err := ReverseHex(tt.input)
		if tt.hasError {
			if err == nil {
				t.Errorf("ReverseHex(%s) expected error, got nil", tt.input)
			}
		} else {
			if err != nil {
				t.Errorf("ReverseHex(%s) unexpected error: %v", tt.input, err)
			}
			if result != tt.expected {
				t.Errorf("ReverseHex(%s) = %s; want %s", tt.input, result, tt.expected)
			}
		}
	}
}

func TestXorHex(t *testing.T) {
	// XOR with zeros should return the same value
	result, err := XorHex("aabbcc", "000000")
	if err != nil {
		t.Errorf("XorHex unexpected error: %v", err)
	}
	if result != "aabbcc" {
		t.Errorf("XorHex(aabbcc, 000000) = %s; want aabbcc", result)
	}

	// XOR with self should return zeros
	result2, err := XorHex("aabbcc", "aabbcc")
	if err != nil {
		t.Errorf("XorHex unexpected error: %v", err)
	}
	if result2 != "000000" {
		t.Errorf("XorHex(aabbcc, aabbcc) = %s; want 000000", result2)
	}

	// Different lengths should error
	_, err = XorHex("aa", "aaa")
	if err == nil {
		t.Error("XorHex should error on different length strings")
	}
}

func TestHexToInt(t *testing.T) {
	tests := []struct {
		input    string
		expected int64
		hasError bool
	}{
		{"ff", 255, false},
		{"0xff", 255, false},
		{"0XFF", 255, false},
		{"10", 16, false},
		{"", 0, true},
		{"xyz", 0, true},
	}

	for _, tt := range tests {
		result, err := HexToInt(tt.input)
		if tt.hasError {
			if err == nil {
				t.Errorf("HexToInt(%s) expected error, got nil", tt.input)
			}
		} else {
			if err != nil {
				t.Errorf("HexToInt(%s) unexpected error: %v", tt.input, err)
			}
			if result != tt.expected {
				t.Errorf("HexToInt(%s) = %d; want %d", tt.input, result, tt.expected)
			}
		}
	}
}

func TestIntToHex(t *testing.T) {
	tests := []struct {
		input    int64
		expected string
	}{
		{255, "ff"},
		{16, "10"},
		{0, "0"},
		{256, "100"},
	}

	for _, tt := range tests {
		result := IntToHex(tt.input)
		if result != tt.expected {
			t.Errorf("IntToHex(%d) = %s; want %s", tt.input, result, tt.expected)
		}
	}
}

func TestIntToHexPadded(t *testing.T) {
	result := IntToHexPadded(255, 4)
	expected := "00ff"
	if result != expected {
		t.Errorf("IntToHexPadded(255, 4) = %s; want %s", result, expected)
	}

	result2 := IntToHexPadded(255, 2)
	expected2 := "ff"
	if result2 != expected2 {
		t.Errorf("IntToHexPadded(255, 2) = %s; want %s", result2, expected2)
	}
}

func TestBytesToHexAndHexToBytes(t *testing.T) {
	original := []byte{0x48, 0x65, 0x6c, 0x6c, 0x6f}
	
	// Test BytesToHex (alias for HexEncode)
	encoded := BytesToHex(original)
	if encoded != "48656c6c6f" {
		t.Errorf("BytesToHex() = %s; want 48656c6c6f", encoded)
	}

	// Test HexToBytes (alias for HexDecode)
	decoded, err := HexToBytes("48656c6c6f")
	if err != nil {
		t.Errorf("HexToBytes unexpected error: %v", err)
	}
	if string(decoded) != string(original) {
		t.Errorf("HexToBytes() = %v; want %v", decoded, original)
	}
}

func TestValidateHex(t *testing.T) {
	tests := []struct {
		input    string
		hasError bool
	}{
		{"aabbcc", false},
		{"AABBCC", false},
		{"", true},      // empty
		{"aab", true},   // odd length
		{"gggg", true},  // invalid chars
	}

	for _, tt := range tests {
		err := ValidateHex(tt.input)
		if tt.hasError {
			if err == nil {
				t.Errorf("ValidateHex(%s) expected error, got nil", tt.input)
			}
		} else {
			if err != nil {
				t.Errorf("ValidateHex(%s) unexpected error: %v", tt.input, err)
			}
		}
	}
}

func TestHexReader(t *testing.T) {
	reader, err := NewHexReader("48656c6c6f")
	if err != nil {
		t.Fatalf("NewHexReader unexpected error: %v", err)
	}

	// Test Len
	if reader.Len() != 5 {
		t.Errorf("HexReader.Len() = %d; want 5", reader.Len())
	}

	// Test Read
	buf := make([]byte, 10)
	n, err := reader.Read(buf)
	if err != nil {
		t.Errorf("HexReader.Read unexpected error: %v", err)
	}
	if n != 5 {
		t.Errorf("HexReader.Read returned %d bytes; want 5", n)
	}
	if string(buf[:n]) != "Hello" {
		t.Errorf("HexReader.Read got %s; want Hello", string(buf[:n]))
	}

	// Test Len after reading
	if reader.Len() != 0 {
		t.Errorf("HexReader.Len() after read = %d; want 0", reader.Len())
	}

	// Test Reset
	reader.Reset()
	if reader.Len() != 5 {
		t.Errorf("HexReader.Len() after reset = %d; want 5", reader.Len())
	}
}

func TestHexReaderError(t *testing.T) {
	_, err := NewHexReader("invalid hex string xyz")
	if err == nil {
		t.Error("NewHexReader should return error for invalid hex")
	}
}

func TestRoundTrip(t *testing.T) {
	original := []byte("The quick brown fox jumps over the lazy dog! @#$%^&*()")
	
	encoded := HexEncode(original)
	decoded, err := HexDecode(encoded)
	if err != nil {
		t.Fatalf("Round trip failed: %v", err)
	}
	
	if string(decoded) != string(original) {
		t.Errorf("Round trip failed: got %s, want %s", decoded, original)
	}
}

// Helper function
func containsStr(s, substr string) bool {
	return len(s) >= len(substr) && 
		(s == substr || len(s) > 0 && containsSubstring(s, substr))
}

func containsSubstring(s, substr string) bool {
	for i := 0; i <= len(s)-len(substr); i++ {
		if s[i:i+len(substr)] == substr {
			return true
		}
	}
	return false
}

// Benchmark tests
func BenchmarkHexEncode(b *testing.B) {
	data := []byte("The quick brown fox jumps over the lazy dog")
	for i := 0; i < b.N; i++ {
		HexEncode(data)
	}
}

func BenchmarkHexDecode(b *testing.B) {
	hexStr := "54686520717569636b2062726f776e20666f78206a756d7073206f76657220746865206c617a7920646f67"
	for i := 0; i < b.N; i++ {
		HexDecode(hexStr)
	}
}

func BenchmarkIsHex(b *testing.B) {
	hexStr := "54686520717569636b2062726f776e20666f78206a756d7073206f76657220746865206c617a7920646f67"
	for i := 0; i < b.N; i++ {
		IsHex(hexStr)
	}
}

func BenchmarkHexDump(b *testing.B) {
	data := make([]byte, 1024)
	for i := range data {
		data[i] = byte(i % 256)
	}
	for i := 0; i < b.N; i++ {
		HexDump(data)
	}
}