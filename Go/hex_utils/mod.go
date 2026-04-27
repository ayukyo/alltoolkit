// Package hexutils provides comprehensive hexadecimal encoding/decoding utilities.
// It offers zero-dependency functions for hex conversion, validation, and formatting.
package hexutils

import (
	"encoding/hex"
	"errors"
	"fmt"
	"strings"
)

var (
	// ErrInvalidHexLength indicates the hex string has an odd length
	ErrInvalidHexLength = errors.New("hex string must have even length")
	// ErrInvalidHexChar indicates the hex string contains invalid characters
	ErrInvalidHexChar = errors.New("hex string contains invalid characters")
	// ErrEmptyInput indicates the input is empty
	ErrEmptyInput = errors.New("input cannot be empty")
)

// HexEncode encodes a byte slice to a hexadecimal string.
func HexEncode(data []byte) string {
	return hex.EncodeToString(data)
}

// HexDecode decodes a hexadecimal string to a byte slice.
// Returns an error if the string is not valid hexadecimal.
func HexDecode(s string) ([]byte, error) {
	if len(s) == 0 {
		return nil, ErrEmptyInput
	}
	if len(s)%2 != 0 {
		return nil, ErrInvalidHexLength
	}
	result := make([]byte, hex.DecodedLen(len(s)))
	_, err := hex.Decode(result, []byte(s))
	if err != nil {
		return nil, ErrInvalidHexChar
	}
	return result, nil
}

// HexEncodeString encodes a string to its hexadecimal representation.
func HexEncodeString(s string) string {
	return hex.EncodeToString([]byte(s))
}

// HexDecodeToString decodes a hexadecimal string to a regular string.
// Returns an error if the input is not valid hexadecimal.
func HexDecodeToString(hexStr string) (string, error) {
	data, err := HexDecode(hexStr)
	if err != nil {
		return "", err
	}
	return string(data), nil
}

// IsHex checks if a string is a valid hexadecimal string.
func IsHex(s string) bool {
	if len(s) == 0 {
		return false
	}
	if len(s)%2 != 0 {
		return false
	}
	for _, c := range s {
		if !isHexChar(c) {
			return false
		}
	}
	return true
}

// isHexChar checks if a rune is a valid hexadecimal character
func isHexChar(c rune) bool {
	return (c >= '0' && c <= '9') || (c >= 'a' && c <= 'f') || (c >= 'A' && c <= 'F')
}

// HexEncodeUpper encodes a byte slice to an uppercase hexadecimal string.
func HexEncodeUpper(data []byte) string {
	return strings.ToUpper(hex.EncodeToString(data))
}

// HexDecodeIgnoreCase decodes a hexadecimal string to a byte slice,
// ignoring case (accepts both uppercase and lowercase).
func HexDecodeIgnoreCase(s string) ([]byte, error) {
	return HexDecode(strings.ToLower(s))
}

// HexDump generates a hex dump similar to xxd output.
// Shows offset, hex bytes, and ASCII representation.
func HexDump(data []byte) string {
	if len(data) == 0 {
		return ""
	}

	var builder strings.Builder
	lines := (len(data) + 15) / 16

	for i := 0; i < lines; i++ {
		start := i * 16
		end := start + 16
		if end > len(data) {
			end = len(data)
		}
		line := data[start:end]

		// Offset
		builder.WriteString(fmt.Sprintf("%08x: ", start))

		// Hex bytes (first 8 bytes)
		for j := 0; j < 8; j++ {
			if j < len(line) {
				builder.WriteString(fmt.Sprintf("%02x ", line[j]))
			} else {
				builder.WriteString("   ")
			}
		}

		builder.WriteString(" ")

		// Hex bytes (next 8 bytes)
		for j := 8; j < 16; j++ {
			if j < len(line) {
				builder.WriteString(fmt.Sprintf("%02x ", line[j]))
			} else {
				builder.WriteString("   ")
			}
		}

		builder.WriteString(" ")

		// ASCII representation
		for j := 0; j < len(line); j++ {
			if line[j] >= 32 && line[j] <= 126 {
				builder.WriteByte(line[j])
			} else {
				builder.WriteByte('.')
			}
		}

		if i < lines-1 {
			builder.WriteByte('\n')
		}
	}

	return builder.String()
}

// HexDumpCompact generates a compact hex dump (just hex bytes separated by spaces).
func HexDumpCompact(data []byte) string {
	if len(data) == 0 {
		return ""
	}

	parts := make([]string, len(data))
	for i, b := range data {
		parts[i] = fmt.Sprintf("%02x", b)
	}
	return strings.Join(parts, " ")
}

// HexDumpCStyle generates a C-style hex array representation.
func HexDumpCStyle(data []byte, varName string) string {
	if len(data) == 0 {
		return fmt.Sprintf("unsigned char %s[] = {};", varName)
	}

	var builder strings.Builder
	builder.WriteString(fmt.Sprintf("unsigned char %s[] = {\n", varName))

	for i := 0; i < len(data); i++ {
		if i%12 == 0 {
			if i > 0 {
				builder.WriteString("\n")
			}
			builder.WriteString("    ")
		}
		builder.WriteString(fmt.Sprintf("0x%02x", data[i]))
		if i < len(data)-1 {
			builder.WriteString(", ")
		}
	}

	builder.WriteString("\n};")
	return builder.String()
}

// HexDumpPythonStyle generates a Python-style hex bytes representation.
func HexDumpPythonStyle(data []byte) string {
	if len(data) == 0 {
		return "b''"
	}

	parts := make([]string, len(data))
	for i, b := range data {
		parts[i] = fmt.Sprintf("\\x%02x", b)
	}
	return fmt.Sprintf("b'%s'", strings.Join(parts, ""))
}

// ReverseHex reverses the byte order of a hex string.
// Useful for converting between big-endian and little-endian representations.
func ReverseHex(hexStr string) (string, error) {
	data, err := HexDecode(hexStr)
	if err != nil {
		return "", err
	}
	// Reverse the bytes
	for i, j := 0, len(data)-1; i < j; i, j = i+1, j-1 {
		data[i], data[j] = data[j], data[i]
	}
	return HexEncode(data), nil
}

// XorHex performs XOR operation on two hex strings.
// Returns an error if the strings have different lengths or are invalid hex.
func XorHex(hex1, hex2 string) (string, error) {
	if len(hex1) != len(hex2) {
		return "", errors.New("hex strings must have the same length")
	}

	data1, err := HexDecode(hex1)
	if err != nil {
		return "", fmt.Errorf("first hex string: %w", err)
	}

	data2, err := HexDecode(hex2)
	if err != nil {
		return "", fmt.Errorf("second hex string: %w", err)
	}

	result := make([]byte, len(data1))
	for i := range data1 {
		result[i] = data1[i] ^ data2[i]
	}

	return HexEncode(result), nil
}

// HexToInt converts a hex string to an integer.
func HexToInt(hexStr string) (int64, error) {
	if len(hexStr) == 0 {
		return 0, ErrEmptyInput
	}

	// Remove 0x prefix if present
	hexStr = strings.TrimPrefix(hexStr, "0x")
	hexStr = strings.TrimPrefix(hexStr, "0X")

	var result int64
	_, err := fmt.Sscanf(hexStr, "%x", &result)
	if err != nil {
		return 0, ErrInvalidHexChar
	}
	return result, nil
}

// IntToHex converts an integer to a hex string.
func IntToHex(n int64) string {
	return fmt.Sprintf("%x", n)
}

// IntToHexPadded converts an integer to a padded hex string with minimum width.
func IntToHexPadded(n int64, width int) string {
	return fmt.Sprintf("%0*x", width, n)
}

// BytesToHex is an alias for HexEncode.
func BytesToHex(data []byte) string {
	return HexEncode(data)
}

// HexToBytes is an alias for HexDecode.
func HexToBytes(s string) ([]byte, error) {
	return HexDecode(s)
}

// ValidateHex validates a hex string and returns detailed error information.
func ValidateHex(s string) error {
	if len(s) == 0 {
		return ErrEmptyInput
	}
	if len(s)%2 != 0 {
		return ErrInvalidHexLength
	}
	for i, c := range s {
		if !isHexChar(c) {
			return fmt.Errorf("%w: character '%c' at position %d", ErrInvalidHexChar, c, i)
		}
	}
	return nil
}

// HexReader provides a streaming hex decoder
type HexReader struct {
	data   []byte
	offset int
}

// NewHexReader creates a new HexReader from a hex string
func NewHexReader(hexStr string) (*HexReader, error) {
	data, err := HexDecode(hexStr)
	if err != nil {
		return nil, err
	}
	return &HexReader{data: data}, nil
}

// Read reads bytes into p, returns number of bytes read
func (r *HexReader) Read(p []byte) (int, error) {
	if r.offset >= len(r.data) {
		return 0, nil
	}
	n := copy(p, r.data[r.offset:])
	r.offset += n
	return n, nil
}

// Reset resets the reader to the beginning
func (r *HexReader) Reset() {
	r.offset = 0
}

// Len returns the remaining length of unread data
func (r *HexReader) Len() int {
	return len(r.data) - r.offset
}