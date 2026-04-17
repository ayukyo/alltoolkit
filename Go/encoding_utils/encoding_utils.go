// Package encoding_utils provides various encoding and decoding utilities.
// All functions are implemented using Go standard library with zero external dependencies.
package encoding_utils

import (
	"bytes"
	"encoding/base64"
	"encoding/hex"
	"fmt"
	"html"
	"io"
	"net/url"
	"strconv"
	"strings"
	"unicode/utf8"
)

// ============================================================================
// Base64 Encoding/Decoding
// ============================================================================

// Base64Encode encodes a byte slice to standard Base64 string.
func Base64Encode(data []byte) string {
	return base64.StdEncoding.EncodeToString(data)
}

// Base64Decode decodes a standard Base64 string to byte slice.
func Base64Decode(encoded string) ([]byte, error) {
	return base64.StdEncoding.DecodeString(encoded)
}

// Base64URLEncode encodes a byte slice to URL-safe Base64 string (no padding).
func Base64URLEncode(data []byte) string {
	return base64.RawURLEncoding.EncodeToString(data)
}

// Base64URLDecode decodes a URL-safe Base64 string to byte slice.
func Base64URLDecode(encoded string) ([]byte, error) {
	return base64.RawURLEncoding.DecodeString(encoded)
}

// Base64EncodeString encodes a string to Base64.
func Base64EncodeString(text string) string {
	return Base64Encode([]byte(text))
}

// Base64DecodeString decodes a Base64 string to string.
func Base64DecodeString(encoded string) (string, error) {
	decoded, err := Base64Decode(encoded)
	if err != nil {
		return "", err
	}
	return string(decoded), nil
}

// ============================================================================
// Hex Encoding/Decoding
// ============================================================================

// HexEncode encodes a byte slice to hexadecimal string.
func HexEncode(data []byte) string {
	return hex.EncodeToString(data)
}

// HexDecode decodes a hexadecimal string to byte slice.
func HexDecode(encoded string) ([]byte, error) {
	return hex.DecodeString(encoded)
}

// HexEncodeString encodes a string to hexadecimal.
func HexEncodeString(text string) string {
	return HexEncode([]byte(text))
}

// HexDecodeString decodes a hexadecimal string to string.
func HexDecodeString(encoded string) (string, error) {
	decoded, err := HexDecode(encoded)
	if err != nil {
		return "", err
	}
	return string(decoded), nil
}

// ============================================================================
// URL Encoding/Decoding
// ============================================================================

// URLEncode encodes a string for use in URL query parameters.
func URLEncode(text string) string {
	return url.QueryEscape(text)
}

// URLDecode decodes a URL-encoded string.
func URLDecode(encoded string) (string, error) {
	return url.QueryUnescape(encoded)
}

// URLPathEncode encodes a string for use in URL path segments.
func URLPathEncode(text string) string {
	return url.PathEscape(text)
}

// URLPathDecode decodes a URL path-encoded string.
func URLPathDecode(encoded string) (string, error) {
	return url.PathUnescape(encoded)
}

// URLEncodeMap encodes a map of string key-values to URL query string.
func URLEncodeMap(params map[string]string) string {
	values := url.Values{}
	for k, v := range params {
		values.Set(k, v)
	}
	return values.Encode()
}

// URLDecodeMap decodes a URL query string to a map.
func URLDecodeMap(query string) (map[string]string, error) {
	values, err := url.ParseQuery(query)
	if err != nil {
		return nil, err
	}
	result := make(map[string]string)
	for k, v := range values {
		if len(v) > 0 {
			result[k] = v[0]
		}
	}
	return result, nil
}

// ============================================================================
// HTML Encoding/Decoding
// ============================================================================

// HTMLEscape escapes special HTML characters in a string.
func HTMLEscape(text string) string {
	return html.EscapeString(text)
}

// HTMLUnescape unescapes HTML entities in a string.
func HTMLUnescape(escaped string) string {
	return html.UnescapeString(escaped)
}

// ============================================================================
// ROT13 Encoding/Decoding
// ============================================================================

// Rot13 applies ROT13 transformation to a string.
// ROT13 is its own inverse, so encoding and decoding use the same function.
func Rot13(text string) string {
	var result strings.Builder
	result.Grow(len(text))

	for _, r := range text {
		switch {
		case r >= 'a' && r <= 'z':
			result.WriteRune('a' + (r-'a'+13)%26)
		case r >= 'A' && r <= 'Z':
			result.WriteRune('A' + (r-'A'+13)%26)
		default:
			result.WriteRune(r)
		}
	}

	return result.String()
}

// RotN applies ROT-N transformation to a string with custom rotation value.
func RotN(text string, n int) string {
	n = ((n % 26) + 26) % 26 // Normalize to 0-25
	var result strings.Builder
	result.Grow(len(text))

	for _, r := range text {
		switch {
		case r >= 'a' && r <= 'z':
			result.WriteRune('a' + (r-'a'+rune(n))%26)
		case r >= 'A' && r <= 'Z':
			result.WriteRune('A' + (r-'A'+rune(n))%26)
		default:
			result.WriteRune(r)
		}
	}

	return result.String()
}

// ============================================================================
// Run-Length Encoding (RLE)
// ============================================================================

// RLEncode performs run-length encoding on a byte slice.
// Returns encoded data in format: [count, byte, count, byte, ...]
func RLEncode(data []byte) []byte {
	if len(data) == 0 {
		return nil
	}

	var result bytes.Buffer
	var count byte = 1
	prev := data[0]

	for i := 1; i < len(data); i++ {
		if data[i] == prev && count < 255 {
			count++
		} else {
			result.WriteByte(count)
			result.WriteByte(prev)
			count = 1
			prev = data[i]
		}
	}
	result.WriteByte(count)
	result.WriteByte(prev)

	return result.Bytes()
}

// RLDecode performs run-length decoding.
func RLDecode(data []byte) ([]byte, error) {
	if len(data) == 0 {
		return nil, nil
	}
	if len(data)%2 != 0 {
		return nil, fmt.Errorf("invalid RLE data: length must be even")
	}

	var result bytes.Buffer
	for i := 0; i < len(data); i += 2 {
		count := data[i]
		char := data[i+1]
		for j := byte(0); j < count; j++ {
			result.WriteByte(char)
		}
	}

	return result.Bytes(), nil
}

// RLEncodeString performs run-length encoding on a string.
func RLEncodeString(text string) string {
	return string(RLEncode([]byte(text)))
}

// RLDecodeString performs run-length decoding on a string.
func RLDecodeString(encoded string) (string, error) {
	decoded, err := RLDecode([]byte(encoded))
	if err != nil {
		return "", err
	}
	return string(decoded), nil
}

// ============================================================================
// Binary Encoding/Decoding
// ============================================================================

// BinaryEncode encodes a byte slice to binary string representation.
func BinaryEncode(data []byte) string {
	var result strings.Builder
	for _, b := range data {
		result.WriteString(fmt.Sprintf("%08b", b))
	}
	return result.String()
}

// BinaryDecode decodes a binary string to byte slice.
func BinaryDecode(binary string) ([]byte, error) {
	if len(binary)%8 != 0 {
		return nil, fmt.Errorf("binary string length must be multiple of 8")
	}

	result := make([]byte, len(binary)/8)
	for i := 0; i < len(result); i++ {
		b, err := strconv.ParseUint(binary[i*8:(i+1)*8], 2, 8)
		if err != nil {
			return nil, fmt.Errorf("invalid binary at position %d: %v", i*8, err)
		}
		result[i] = byte(b)
	}
	return result, nil
}

// ============================================================================
// Unicode Escape/Unescape
// ============================================================================

// UnicodeEscape escapes non-ASCII characters to \uXXXX format.
func UnicodeEscape(text string) string {
	var result strings.Builder
	for _, r := range text {
		if r < 128 {
			result.WriteRune(r)
		} else {
			result.WriteString(fmt.Sprintf("\\u%04X", r))
		}
	}
	return result.String()
}

// UnicodeUnescape unescapes \uXXXX format to Unicode characters.
func UnicodeUnescape(escaped string) (string, error) {
	var result strings.Builder
	for i := 0; i < len(escaped); {
		if i+5 < len(escaped) && escaped[i:i+2] == "\\u" {
			hex := escaped[i+2 : i+6]
			r, err := strconv.ParseInt(hex, 16, 32)
			if err != nil {
				return "", fmt.Errorf("invalid unicode escape at position %d", i)
			}
			result.WriteRune(rune(r))
			i += 6
		} else {
			result.WriteByte(escaped[i])
			i++
		}
	}
	return result.String(), nil
}

// ============================================================================
// Quoted-Printable Encoding/Decoding (Basic Implementation)
// ============================================================================

// QuotedPrintableEncode encodes text using quoted-printable encoding.
func QuotedPrintableEncode(text string) string {
	var result strings.Builder
	for _, r := range text {
		if r == '\n' || r == '\r' {
			result.WriteRune(r)
		} else if r < 32 || r > 126 || r == '=' {
			result.WriteString(fmt.Sprintf("=%02X", r))
		} else {
			result.WriteRune(r)
		}
	}
	return result.String()
}

// QuotedPrintableDecode decodes quoted-printable encoded text.
func QuotedPrintableDecode(encoded string) (string, error) {
	var result strings.Builder
	for i := 0; i < len(encoded); {
		if encoded[i] == '=' && i+2 < len(encoded) {
			hex := encoded[i+1 : i+3]
			b, err := strconv.ParseInt(hex, 16, 8)
			if err != nil {
				return "", fmt.Errorf("invalid quoted-printable at position %d", i)
			}
			result.WriteByte(byte(b))
			i += 3
		} else {
			result.WriteByte(encoded[i])
			i++
		}
	}
	return result.String(), nil
}

// ============================================================================
// Character Count and Analysis
// ============================================================================

// CharCount returns character count (runes) and byte count of a string.
func CharCount(text string) (runes int, bytes int) {
	return utf8.RuneCountInString(text), len(text)
}

// IsPrintable checks if all characters in a string are printable ASCII.
func IsPrintable(text string) bool {
	for _, r := range text {
		if r < 32 || r > 126 {
			if r != '\n' && r != '\r' && r != '\t' {
				return false
			}
		}
	}
	return true
}

// ============================================================================
// Chunked Base64 Encoding for Large Data
// ============================================================================

// Base64ChunkedEncode encodes data to Base64 with line breaks.
func Base64ChunkedEncode(data []byte, lineLength int) string {
	encoded := base64.StdEncoding.EncodeToString(data)
	if lineLength <= 0 {
		return encoded
	}

	var result strings.Builder
	for i := 0; i < len(encoded); i += lineLength {
		end := i + lineLength
		if end > len(encoded) {
			end = len(encoded)
		}
		result.WriteString(encoded[i:end])
		if end < len(encoded) {
			result.WriteByte('\n')
		}
	}
	return result.String()
}

// Base64ChunkedDecode decodes chunked Base64 data (ignores whitespace).
func Base64ChunkedDecode(encoded string) ([]byte, error) {
	// Remove all whitespace
	cleaned := strings.Map(func(r rune) rune {
		if r == '\n' || r == '\r' || r == ' ' || r == '\t' {
			return -1
		}
		return r
	}, encoded)
	return base64.StdEncoding.DecodeString(cleaned)
}

// ============================================================================
// Streaming Base64 Encoding/Decoding
// ============================================================================

// Base64StreamEncoder wraps a writer for streaming Base64 encoding.
type Base64StreamEncoder struct {
	encoder *base64.Encoder
	buffer  *bytes.Buffer
}

// NewBase64StreamEncoder creates a new streaming Base64 encoder.
func NewBase64StreamEncoder() *Base64StreamEncoder {
	buf := &bytes.Buffer{}
	return &Base64StreamEncoder{
		encoder: base64.NewEncoder(base64.StdEncoding, buf),
		buffer:  buf,
	}
}

// Write writes data to be encoded.
func (e *Base64StreamEncoder) Write(data []byte) (int, error) {
	return e.encoder.Write(data)
}

// Close finalizes the encoding and returns the Base64 string.
func (e *Base64StreamEncoder) Close() (string, error) {
	err := e.encoder.Close()
	return e.buffer.String(), err
}

// Base64StreamDecoder wraps a reader for streaming Base64 decoding.
type Base64StreamDecoder struct {
	reader io.Reader
}

// NewBase64StreamDecoder creates a new streaming Base64 decoder.
func NewBase64StreamDecoder(encoded string) *Base64StreamDecoder {
	return &Base64StreamDecoder{
		reader: base64.NewDecoder(base64.StdEncoding, strings.NewReader(encoded)),
	}
}

// ReadAll reads all decoded data.
func (d *Base64StreamDecoder) ReadAll() ([]byte, error) {
	return io.ReadAll(d.reader)
}