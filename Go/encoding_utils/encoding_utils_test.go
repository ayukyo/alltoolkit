package encoding_utils

import (
	"strings"
	"testing"
)

// ============================================================================
// Base64 Tests
// ============================================================================

func TestBase64Encode(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"Hello, World!", "SGVsbG8sIFdvcmxkIQ=="},
		{"Go", "R28="},
		{"", ""},
		{"中文测试", "5Lit5paH5rWL6K+V"},
	}

	for _, tt := range tests {
		result := Base64Encode([]byte(tt.input))
		if result != tt.expected {
			t.Errorf("Base64Encode(%q) = %q, want %q", tt.input, result, tt.expected)
		}
	}
}

func TestBase64Decode(t *testing.T) {
	tests := []struct {
		input    string
		expected string
		hasError bool
	}{
		{"SGVsbG8sIFdvcmxkIQ==", "Hello, World!", false},
		{"R28=", "Go", false},
		{"", "", false},
		{"invalid!!!", "", true},
	}

	for _, tt := range tests {
		result, err := Base64Decode(tt.input)
		if tt.hasError {
			if err == nil {
				t.Errorf("Base64Decode(%q) expected error, got none", tt.input)
			}
		} else {
			if err != nil {
				t.Errorf("Base64Decode(%q) unexpected error: %v", tt.input, err)
			}
			if string(result) != tt.expected {
				t.Errorf("Base64Decode(%q) = %q, want %q", tt.input, string(result), tt.expected)
			}
		}
	}
}

func TestBase64URLEncode(t *testing.T) {
	data := []byte{0xff, 0xfe, 0xfd}
	result := Base64URLEncode(data)
	// URL-safe encoding should not contain + or /
	if strings.ContainsAny(result, "+/") {
		t.Errorf("Base64URLEncode contains unsafe characters: %s", result)
	}
}

func TestBase64URLEncodeDecode(t *testing.T) {
	tests := []string{
		"test data",
		"binary\x00data\xff\xfe",
		"URL safe: /?&=",
	}

	for _, tt := range tests {
		encoded := Base64URLEncode([]byte(tt))
		decoded, err := Base64URLDecode(encoded)
		if err != nil {
			t.Errorf("Base64URLDecode error: %v", err)
		}
		if string(decoded) != tt {
			t.Errorf("Base64URL roundtrip failed: got %q, want %q", string(decoded), tt)
		}
	}
}

func TestBase64EncodeDecodeString(t *testing.T) {
	tests := []string{"Hello", "世界", "emoji 🎉"}

	for _, tt := range tests {
		encoded := Base64EncodeString(tt)
		decoded, err := Base64DecodeString(encoded)
		if err != nil {
			t.Errorf("Base64DecodeString error: %v", err)
		}
		if decoded != tt {
			t.Errorf("Base64 string roundtrip failed: got %q, want %q", decoded, tt)
		}
	}
}

// ============================================================================
// Hex Tests
// ============================================================================

func TestHexEncode(t *testing.T) {
	tests := []struct {
		input    []byte
		expected string
	}{
		{[]byte{0x00}, "00"},
		{[]byte{0xff}, "ff"},
		{[]byte{0x48, 0x65, 0x6c, 0x6c, 0x6f}, "48656c6c6f"},
		{[]byte{}, ""},
	}

	for _, tt := range tests {
		result := HexEncode(tt.input)
		if result != tt.expected {
			t.Errorf("HexEncode(%v) = %q, want %q", tt.input, result, tt.expected)
		}
	}
}

func TestHexDecode(t *testing.T) {
	tests := []struct {
		input    string
		expected []byte
		hasError bool
	}{
		{"00", []byte{0x00}, false},
		{"ff", []byte{0xff}, false},
		{"48656c6c6f", []byte("Hello"), false},
		{"", []byte{}, false},
		{"invalid", nil, true},
		{"gg", nil, true},
	}

	for _, tt := range tests {
		result, err := HexDecode(tt.input)
		if tt.hasError {
			if err == nil {
				t.Errorf("HexDecode(%q) expected error, got none", tt.input)
			}
		} else {
			if err != nil {
				t.Errorf("HexDecode(%q) unexpected error: %v", tt.input, err)
			}
			if string(result) != string(tt.expected) {
				t.Errorf("HexDecode(%q) = %v, want %v", tt.input, result, tt.expected)
			}
		}
	}
}

func TestHexEncodeDecodeString(t *testing.T) {
	input := "Hello, World!"
	encoded := HexEncodeString(input)
	decoded, err := HexDecodeString(encoded)
	if err != nil {
		t.Errorf("HexDecodeString error: %v", err)
	}
	if decoded != input {
		t.Errorf("Hex string roundtrip failed: got %q, want %q", decoded, input)
	}
}

// ============================================================================
// URL Encoding Tests
// ============================================================================

func TestURLEncodeDecode(t *testing.T) {
	tests := []struct {
		input    string
		encoded  string
	}{
		{"hello world", "hello+world"},
		{"a=1&b=2", "a%3D1%26b%3D2"},
		{"中文", "%E4%B8%AD%E6%96%87"},
	}

	for _, tt := range tests {
		encoded := URLEncode(tt.input)
		decoded, err := URLDecode(encoded)
		if err != nil {
			t.Errorf("URLDecode error: %v", err)
		}
		if decoded != tt.input {
			t.Errorf("URL roundtrip failed: got %q, want %q", decoded, tt.input)
		}
	}
}

func TestURLPathEncodeDecode(t *testing.T) {
	tests := []string{
		"path/to/file",
		"file with spaces",
		"文件",
	}

	for _, tt := range tests {
		encoded := URLPathEncode(tt)
		decoded, err := URLPathDecode(encoded)
		if err != nil {
			t.Errorf("URLPathDecode error: %v", err)
		}
		if decoded != tt {
			t.Errorf("URL path roundtrip failed: got %q, want %q", decoded, tt)
		}
	}
}

func TestURLEncodeDecodeMap(t *testing.T) {
	params := map[string]string{
		"name":  "John Doe",
		"email": "john@example.com",
		"page":  "1",
	}

	encoded := URLEncodeMap(params)
	decoded, err := URLDecodeMap(encoded)
	if err != nil {
		t.Errorf("URLDecodeMap error: %v", err)
	}

	for k, v := range params {
		if decoded[k] != v {
			t.Errorf("URL map roundtrip failed for key %q: got %q, want %q", k, decoded[k], v)
		}
	}
}

// ============================================================================
// HTML Tests
// ============================================================================

func TestHTMLEscape(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"<script>", "&lt;script&gt;"},
		{"a & b", "a &amp; b"},
		{`"quote"`, "&#34;quote&#34;"},
		{"normal text", "normal text"},
	}

	for _, tt := range tests {
		result := HTMLEscape(tt.input)
		if result != tt.expected {
			t.Errorf("HTMLEscape(%q) = %q, want %q", tt.input, result, tt.expected)
		}
	}
}

func TestHTMLUnescape(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"&lt;script&gt;", "<script>"},
		{"a &amp; b", "a & b"},
		{"&#34;quote&#34;", `"quote"`},
		{"&nbsp;", "\u00a0"},
	}

	for _, tt := range tests {
		result := HTMLUnescape(tt.input)
		if result != tt.expected {
			t.Errorf("HTMLUnescape(%q) = %q, want %q", tt.input, result, tt.expected)
		}
	}
}

// ============================================================================
// ROT13 Tests
// ============================================================================

func TestRot13(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"hello", "uryyb"},
		{"HELLO", "URYYB"},
		{"Hello, World!", "Uryyb, Jbeyq!"},
		{"abc123", "nop123"},
		{"中文", "中文"}, // Non-ASCII should remain unchanged
	}

	for _, tt := range tests {
		result := Rot13(tt.input)
		if result != tt.expected {
			t.Errorf("Rot13(%q) = %q, want %q", tt.input, result, tt.expected)
		}
	}
}

func TestRot13SelfInverse(t *testing.T) {
	tests := []string{
		"hello world",
		"The Quick Brown Fox",
		"Test 123!",
	}

	for _, tt := range tests {
		encoded := Rot13(tt)
		decoded := Rot13(encoded)
		if decoded != tt {
			t.Errorf("Rot13 not self-inverse: %q -> %q -> %q", tt, encoded, decoded)
		}
	}
}

func TestRotN(t *testing.T) {
	tests := []struct {
		input    string
		n        int
		expected string
	}{
		{"abc", 1, "bcd"},
		{"xyz", 3, "abc"},
		{"ABC", 5, "FGH"},
		{"test", 26, "test"}, // Full rotation
		{"test", 52, "test"}, // Double rotation
	}

	for _, tt := range tests {
		result := RotN(tt.input, tt.n)
		if result != tt.expected {
			t.Errorf("RotN(%q, %d) = %q, want %q", tt.input, tt.n, result, tt.expected)
		}
	}
}

// ============================================================================
// RLE Tests
// ============================================================================

func TestRLEncodeDecode(t *testing.T) {
	tests := []struct {
		input []byte
		name  string
	}{
		{[]byte("aaabbbccc"), "simple"},
		{[]byte("aaaaaaaaaa"), "single char"},
		{[]byte("abc"), "no repeats"},
		{[]byte{}, "empty"},
		{[]byte{0x00, 0x00, 0x00, 0x00}, "nulls"},
	}

	for _, tt := range tests {
		encoded := RLEncode(tt.input)
		decoded, err := RLDecode(encoded)
		if err != nil {
			t.Errorf("RLDecode error for %s: %v", tt.name, err)
		}
		if string(decoded) != string(tt.input) {
			t.Errorf("RLE roundtrip failed for %s: got %v, want %v", tt.name, decoded, tt.input)
		}
	}
}

func TestRLDecodeInvalid(t *testing.T) {
	_, err := RLDecode([]byte{0x01}) // Odd length
	if err == nil {
		t.Error("RLDecode should fail with odd length input")
	}
}

// ============================================================================
// Binary Tests
// ============================================================================

func TestBinaryEncode(t *testing.T) {
	tests := []struct {
		input    []byte
		expected string
	}{
		{[]byte{0x00}, "00000000"},
		{[]byte{0xff}, "11111111"},
		{[]byte{0xAA}, "10101010"},
		{[]byte{0x48, 0x65}, "0100100001100101"},
	}

	for _, tt := range tests {
		result := BinaryEncode(tt.input)
		if result != tt.expected {
			t.Errorf("BinaryEncode(%v) = %q, want %q", tt.input, result, tt.expected)
		}
	}
}

func TestBinaryDecode(t *testing.T) {
	tests := []struct {
		input    string
		expected []byte
		hasError bool
	}{
		{"00000000", []byte{0x00}, false},
		{"11111111", []byte{0xff}, false},
		{"10101010", []byte{0xAA}, false},
		{"0100100001100101", []byte{0x48, 0x65}, false},
		{"101", nil, true}, // Not multiple of 8
		{"abcdefgh", nil, true}, // Invalid characters
	}

	for _, tt := range tests {
		result, err := BinaryDecode(tt.input)
		if tt.hasError {
			if err == nil {
				t.Errorf("BinaryDecode(%q) expected error, got none", tt.input)
			}
		} else {
			if err != nil {
				t.Errorf("BinaryDecode(%q) unexpected error: %v", tt.input, err)
			}
			if string(result) != string(tt.expected) {
				t.Errorf("BinaryDecode(%q) = %v, want %v", tt.input, result, tt.expected)
			}
		}
	}
}

func TestBinaryRoundtrip(t *testing.T) {
	tests := [][]byte{
		{0x00, 0x01, 0x02, 0x03},
		{0xff, 0xfe, 0xfd, 0xfc},
		{0x48, 0x65, 0x6c, 0x6c, 0x6f},
	}

	for _, tt := range tests {
		encoded := BinaryEncode(tt)
		decoded, err := BinaryDecode(encoded)
		if err != nil {
			t.Errorf("BinaryDecode error: %v", err)
		}
		if string(decoded) != string(tt) {
			t.Errorf("Binary roundtrip failed: got %v, want %v", decoded, tt)
		}
	}
}

// ============================================================================
// Unicode Tests
// ============================================================================

func TestUnicodeEscape(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"hello", "hello"},
		{"世界", "\\u4E16\\u754C"},
		{"hi中文", "hi\\u4E2D\\u6587"},
		{"🎉", "\\u1F389"},
	}

	for _, tt := range tests {
		result := UnicodeEscape(tt.input)
		if result != tt.expected {
			t.Errorf("UnicodeEscape(%q) = %q, want %q", tt.input, result, tt.expected)
		}
	}
}

func TestUnicodeUnescape(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"hello", "hello"},
		{"\\u4E16\\u754C", "世界"},
		{"hi\\u4E2D\\u6587", "hi中文"},
		{"\\u1F389", "🎉"},
	}

	for _, tt := range tests {
		result, err := UnicodeUnescape(tt.input)
		if err != nil {
			t.Errorf("UnicodeUnescape error: %v", err)
		}
		if result != tt.expected {
			t.Errorf("UnicodeUnescape(%q) = %q, want %q", tt.input, result, tt.expected)
		}
	}
}

func TestUnicodeRoundtrip(t *testing.T) {
	tests := []string{
		"Hello World",
		"中文测试",
		"emoji 🎉",
		"mixed 中文 and English",
	}

	for _, tt := range tests {
		escaped := UnicodeEscape(tt)
		unescaped, err := UnicodeUnescape(escaped)
		if err != nil {
			t.Errorf("UnicodeUnescape error: %v", err)
		}
		if unescaped != tt {
			t.Errorf("Unicode roundtrip failed: got %q, want %q", unescaped, tt)
		}
	}
}

// ============================================================================
// Quoted-Printable Tests
// ============================================================================

func TestQuotedPrintableEncode(t *testing.T) {
	tests := []struct {
		input    string
		contains string
	}{
		{"hello", "hello"},
		{"hello world", "hello world"},
		{"=test", "=3Dtest"},
		{"中文", "=E4=B8=AD=E6=96=87"},
	}

	for _, tt := range tests {
		result := QuotedPrintableEncode(tt.input)
		if !strings.Contains(result, tt.contains) {
			t.Errorf("QuotedPrintableEncode(%q) = %q, should contain %q", tt.input, result, tt.contains)
		}
	}
}

func TestQuotedPrintableDecode(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"hello", "hello"},
		{"=3Dtest", "=test"},
		{"hello=20world", "hello world"},
	}

	for _, tt := range tests {
		result, err := QuotedPrintableDecode(tt.input)
		if err != nil {
			t.Errorf("QuotedPrintableDecode error: %v", err)
		}
		if result != tt.expected {
			t.Errorf("QuotedPrintableDecode(%q) = %q, want %q", tt.input, result, tt.expected)
		}
	}
}

// ============================================================================
// Utility Tests
// ============================================================================

func TestCharCount(t *testing.T) {
	tests := []struct {
		input     string
		runes     int
		byteCount int
	}{
		{"hello", 5, 5},
		{"中文", 2, 6},
		{"", 0, 0},
		{"🎉", 1, 4},
	}

	for _, tt := range tests {
		runes, bytes := CharCount(tt.input)
		if runes != tt.runes {
			t.Errorf("CharCount(%q) runes = %d, want %d", tt.input, runes, tt.runes)
		}
		if bytes != tt.byteCount {
			t.Errorf("CharCount(%q) bytes = %d, want %d", tt.input, bytes, tt.byteCount)
		}
	}
}

func TestIsPrintable(t *testing.T) {
	tests := []struct {
		input    string
		expected bool
	}{
		{"hello", true},
		{"hello world!", true},
		{"hello\tworld", true},
		{"hello\nworld", true},
		{"hello\x00world", false},
		{"中文", false},
	}

	for _, tt := range tests {
		result := IsPrintable(tt.input)
		if result != tt.expected {
			t.Errorf("IsPrintable(%q) = %v, want %v", tt.input, result, tt.expected)
		}
	}
}

// ============================================================================
// Chunked Base64 Tests
// ============================================================================

func TestBase64ChunkedEncodeDecode(t *testing.T) {
	data := make([]byte, 100)
	for i := range data {
		data[i] = byte(i)
	}

	encoded := Base64ChunkedEncode(data, 64)
	decoded, err := Base64ChunkedDecode(encoded)
	if err != nil {
		t.Errorf("Base64ChunkedDecode error: %v", err)
	}
	if string(decoded) != string(data) {
		t.Error("Chunked Base64 roundtrip failed")
	}

	// Check line breaks
	lines := strings.Split(encoded, "\n")
	for _, line := range lines[:len(lines)-1] {
		if len(line) != 64 {
			t.Errorf("Expected line length 64, got %d", len(line))
		}
	}
}

// ============================================================================
// Streaming Base64 Tests
// ============================================================================

func TestBase64StreamEncoder(t *testing.T) {
	encoder := NewBase64StreamEncoder()
	encoder.Write([]byte("Hello"))
	encoder.Write([]byte(", "))
	encoder.Write([]byte("World!"))
	encoded, err := encoder.Close()
	if err != nil {
		t.Errorf("Encoder close error: %v", err)
	}

	expected := Base64Encode([]byte("Hello, World!"))
	if encoded != expected {
		t.Errorf("Stream encode = %q, want %q", encoded, expected)
	}
}

func TestBase64StreamDecoder(t *testing.T) {
	encoded := Base64EncodeString("Hello, World!")
	decoder := NewBase64StreamDecoder(encoded)
	decoded, err := decoder.ReadAll()
	if err != nil {
		t.Errorf("Decoder read error: %v", err)
	}

	if string(decoded) != "Hello, World!" {
		t.Errorf("Stream decode = %q, want %q", string(decoded), "Hello, World!")
	}
}

// ============================================================================
// Benchmarks
// ============================================================================

func BenchmarkBase64Encode(b *testing.B) {
	data := []byte("Hello, World! This is a test string for benchmarking.")
	for i := 0; i < b.N; i++ {
		Base64Encode(data)
	}
}

func BenchmarkBase64Decode(b *testing.B) {
	encoded := Base64Encode([]byte("Hello, World! This is a test string for benchmarking."))
	for i := 0; i < b.N; i++ {
		Base64Decode(encoded)
	}
}

func BenchmarkRot13(b *testing.B) {
	text := "Hello, World! This is a test string for benchmarking."
	for i := 0; i < b.N; i++ {
		Rot13(text)
	}
}

func BenchmarkRLEncode(b *testing.B) {
	data := []byte("aaaaaaaaaabbbbbbbbbbccccccccccddddddddddeeeeeeeeee")
	for i := 0; i < b.N; i++ {
		RLEncode(data)
	}
}

func BenchmarkBinaryEncode(b *testing.B) {
	data := make([]byte, 256)
	for i := 0; i < b.N; i++ {
		BinaryEncode(data)
	}
}