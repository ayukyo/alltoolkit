package base58_utils

import (
	"math/big"
	"strings"
	"testing"
)

func TestEncode(t *testing.T) {
	tests := []struct {
		name     string
		input    []byte
		expected string
	}{
		{"Empty", []byte{}, ""},
		{"Hello World", []byte("Hello World"), "JxF12TrwUP45BMd"},
		{"Single zero", []byte{0x00}, "1"},
		{"Multiple zeros", []byte{0x00, 0x00, 0x00}, "111"},
		{"Binary", []byte{0x00, 0x01, 0x02, 0xFF}, "1LiA"},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := Encode(tt.input)
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
		expected string
	}{
		{"Empty", "", ""},
		{"Hello", "Hello", "9Ajdvzr"},
		{"Hello World", "Hello World", "JxF12TrwUP45BMd"},
		{"Test", "Test", "3A836b"},
		{"Bitcoin", "Bitcoin", "3WyEDWjcVB"},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := EncodeString(tt.input)
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
		expected string
		hasError bool
	}{
		{"Hello World", "JxF12TrwUP45BMd", "Hello World", false},
		{"Single zero", "1", "\x00", false},
		{"Multiple zeros", "111", "\x00\x00\x00", false},
		{"Empty", "", "", true},
		{"Invalid chars", "invalid!@", "", true},
		{"With O (invalid)", "Oinvalid", "", true},
		{"With 0 (invalid)", "0invalid", "", true},
		{"With I (invalid)", "Iinvalid", "", true},
		{"With l (invalid)", "linvalid", "", true},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := Decode(tt.input)
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
	result, err := DecodeString("JxF12TrwUP45BMd")
	if err != nil {
		t.Errorf("DecodeString() unexpected error: %v", err)
	}
	if result != "Hello World" {
		t.Errorf("DecodeString() = %v, want %v", result, "Hello World")
	}
}

func TestEncodeDecodeRoundTrip(t *testing.T) {
	testStrings := []string{
		"Hello, World!",
		"The quick brown fox jumps over the lazy dog.",
		"12345",
		"!@#$%^&*()",
		"Binary: \x00\x01\x02\xFF",
		strings.Repeat("A", 100),
		"Bitcoin",
		"IPFS",
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

	// Empty string is a special case - encoding returns "", decoding "" returns error
	emptyEncoded := EncodeString("")
	if emptyEncoded != "" {
		t.Errorf("EncodeString('') should return '', got %q", emptyEncoded)
	}
}

func TestAlphabets(t *testing.T) {
	testData := []byte("Test data for different alphabets")

	// Test Bitcoin alphabet
	encoded := EncodeWithAlphabet(testData, BitcoinAlphabet)
	decoded, err := DecodeWithAlphabet(encoded, BitcoinAlphabet)
	if err != nil {
		t.Errorf("Bitcoin alphabet decode error: %v", err)
	}
	if string(decoded) != string(testData) {
		t.Error("Bitcoin alphabet round trip failed")
	}

	// Test Flickr alphabet
	encodedFlickr := EncodeWithAlphabet(testData, FlickrAlphabet)
	decodedFlickr, err := DecodeWithAlphabet(encodedFlickr, FlickrAlphabet)
	if err != nil {
		t.Errorf("Flickr alphabet decode error: %v", err)
	}
	if string(decodedFlickr) != string(testData) {
		t.Error("Flickr alphabet round trip failed")
	}

	// Test Ripple alphabet
	encodedRipple := EncodeWithAlphabet(testData, RippleAlphabet)
	decodedRipple, err := DecodeWithAlphabet(encodedRipple, RippleAlphabet)
	if err != nil {
		t.Errorf("Ripple alphabet decode error: %v", err)
	}
	if string(decodedRipple) != string(testData) {
		t.Error("Ripple alphabet round trip failed")
	}

	// Different alphabets should produce different encodings
	if encoded == encodedFlickr || encoded == encodedRipple || encodedFlickr == encodedRipple {
		t.Error("Different alphabets should produce different encodings")
	}
}

func TestIsValid(t *testing.T) {
	tests := []struct {
		name     string
		input    string
		expected bool
	}{
		{"Valid", "JxF12TrwUP45BMd", true},
		{"Valid simple", "9Ajdvzr", true},
		{"Empty", "", false},
		{"With 0 (invalid)", "invalid0", false},
		{"With O (invalid)", "invalidO", false},
		{"With I (invalid)", "invalidI", false},
		{"With l (invalid)", "invalidl", false},
		{"All valid chars", "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz", true},
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

func TestEncodeDecodeInt(t *testing.T) {
	tests := []struct {
		name  string
		input *big.Int
	}{
		{"Zero", big.NewInt(0)},
		{"One", big.NewInt(1)},
		{"Small", big.NewInt(12345)},
		{"Large", func() *big.Int { n, _ := new(big.Int).SetString("123456789012345678901234567890", 10); return n }()},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			encoded := EncodeInt(tt.input)
			decoded, err := DecodeInt(encoded)
			if err != nil {
				t.Errorf("DecodeInt() error: %v", err)
			}
			if decoded.Cmp(tt.input) != 0 {
				t.Errorf("Round trip failed: got %v, want %v", decoded, tt.input)
			}
		})
	}

	// Test negative number (should return empty string)
	negative := big.NewInt(-1)
	result := EncodeInt(negative)
	if result != "" {
		t.Errorf("EncodeInt(-1) should return empty string, got %v", result)
	}
}

func TestEncodeCheckDecodeCheck(t *testing.T) {
	tests := []struct {
		name  string
		input []byte
	}{
		{"Simple", []byte("Hello")},
		{"With leading zeros", []byte{0x00, 0x00, 0x01, 0x02}},
		{"Binary", []byte{0xFF, 0xFE, 0xFD, 0xFC}},
		{"Longer", []byte("This is a longer string for testing checksum")},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			encoded := EncodeCheck(tt.input)
			decoded, err := DecodeCheck(encoded)
			if err != nil {
				t.Errorf("DecodeCheck() error: %v", err)
			}
			if string(decoded) != string(tt.input) {
				t.Errorf("Check round trip failed: got %v, want %v", decoded, tt.input)
			}
		})
	}

	// Test corrupted checksum
	encoded := EncodeCheck([]byte("test"))
	if len(encoded) > 2 {
		corrupted := encoded[:len(encoded)-1] + string(encoded[len(encoded)-1]+1)
		_, err := DecodeCheck(corrupted)
		if err == nil {
			t.Error("DecodeCheck() should fail with corrupted checksum")
		}
	}
}

func TestConvertAlphabet(t *testing.T) {
	testData := "Hello World"
	bitcoinEncoded := EncodeString(testData)

	// Convert Bitcoin to Flickr
	flickrEncoded, err := ConvertAlphabet(bitcoinEncoded, BitcoinAlphabet, FlickrAlphabet)
	if err != nil {
		t.Errorf("ConvertAlphabet() error: %v", err)
	}

	// Decode with Flickr alphabet should give same result
	decoded, err := DecodeStringWithAlphabet(flickrEncoded, FlickrAlphabet)
	if err != nil {
		t.Errorf("DecodeStringWithAlphabet() error: %v", err)
	}
	if decoded != testData {
		t.Errorf("ConvertAlphabet() round trip failed: got %v, want %v", decoded, testData)
	}
}

func TestTrimLeadingZeros(t *testing.T) {
	tests := []struct {
		name     string
		input    string
		expected string
	}{
		{"No zeros", "abc123", "abc123"},
		{"One zero", "1abc123", "abc123"},
		{"Multiple zeros", "111abc123", "abc123"},
		{"All zeros", "1111", ""},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := TrimLeadingZeros(tt.input)
			if result != tt.expected {
				t.Errorf("TrimLeadingZeros() = %v, want %v", result, tt.expected)
			}
		})
	}
}

func TestCountLeadingZeros(t *testing.T) {
	tests := []struct {
		name     string
		input    string
		expected int
	}{
		{"No zeros", "abc123", 0},
		{"One zero", "1abc123", 1},
		{"Multiple zeros", "111abc123", 3},
		{"All zeros", "1111", 4},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := CountLeadingZeros(tt.input)
			if result != tt.expected {
				t.Errorf("CountLeadingZeros() = %v, want %v", result, tt.expected)
			}
		})
	}
}

func TestEncodeDecodeHex(t *testing.T) {
	tests := []struct {
		name  string
		input string
	}{
		{"Simple", "48656c6c6f"},
		{"With leading zero", "00deadbeef"},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			encoded, err := EncodeHex(tt.input)
			if err != nil {
				t.Errorf("EncodeHex() error: %v", err)
			}
			decoded, err := DecodeHex(encoded)
			if err != nil {
				t.Errorf("DecodeHex() error: %v", err)
			}
			// Normalize hex for comparison
			if strings.ToLower(decoded) != strings.ToLower(tt.input) {
				t.Errorf("Hex round trip: got %v, want %v", decoded, tt.input)
			}
		})
	}

	// Empty string is a special case
	emptyEncoded, _ := EncodeHex("")
	if emptyEncoded != "" {
		t.Errorf("EncodeHex('') should return '', got %q", emptyEncoded)
	}
}

func TestSize(t *testing.T) {
	tests := []struct {
		input int
	}{
		{0},
		{10},
		{100},
		{1000},
	}

	for _, tt := range tests {
		data := make([]byte, tt.input)
		for i := range data {
			data[i] = byte(i)
		}
		encoded := Encode(data)
		estimated := Size(tt.input)
		if estimated < len(encoded) {
			t.Errorf("Size(%d) = %d, but actual encoded length is %d", tt.input, estimated, len(encoded))
		}
	}
}

func TestDecodeSize(t *testing.T) {
	tests := []struct {
		input int
	}{
		{10},
		{100},
		{1000},
	}

	for _, tt := range tests {
		encoded := strings.Repeat("a", tt.input)
		decoded, _ := Decode(encoded)
		estimated := DecodeSize(tt.input)
		if estimated > len(decoded) {
			t.Errorf("DecodeSize(%d) = %d, but actual decoded length is %d", tt.input, estimated, len(decoded))
		}
	}
}

// Benchmarks
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

func BenchmarkEncodeCheck(b *testing.B) {
	data := []byte(strings.Repeat("Hello, World! ", 10))
	for i := 0; i < b.N; i++ {
		EncodeCheck(data)
	}
}

func BenchmarkDecodeCheck(b *testing.B) {
	data := []byte(strings.Repeat("Hello, World! ", 10))
	encoded := EncodeCheck(data)
	for i := 0; i < b.N; i++ {
		DecodeCheck(encoded)
	}
}

func BenchmarkIsValid(b *testing.B) {
	encoded := Encode([]byte("Hello, World! Benchmark Test"))
	for i := 0; i < b.N; i++ {
		IsValid(encoded)
	}
}