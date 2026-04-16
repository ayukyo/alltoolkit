// Package base64_utils provides comprehensive Base64 encoding and decoding utilities.
// Supports standard Base64, URL-safe Base64, file operations, and validation.
package base64_utils

import (
	"encoding/base64"
	"errors"
	"fmt"
	"io"
	"os"
	"strings"
)

// Common errors
var (
	ErrInvalidBase64     = errors.New("invalid base64 encoding")
	ErrEmptyInput        = errors.New("empty input")
	ErrFileNotFound      = errors.New("file not found")
	ErrFileWriteFailed   = errors.New("failed to write file")
	ErrInvalidPadding    = errors.New("invalid padding")
)

// EncodingType defines the type of Base64 encoding
type EncodingType int

const (
	// Standard uses standard Base64 encoding with + and /
	Standard EncodingType = iota
	// URLSafe uses URL-safe encoding with - and _
	URLSafe
	// RawStandard uses standard encoding without padding
	RawStandard
	// RawURLSafe uses URL-safe encoding without padding
	RawURLSafe
)

// getEncoder returns the appropriate base64 encoding
func getEncoder(encType EncodingType) *base64.Encoding {
	switch encType {
	case URLSafe:
		return base64.URLEncoding
	case RawStandard:
		return base64.RawStdEncoding
	case RawURLSafe:
		return base64.RawURLEncoding
	default:
		return base64.StdEncoding
	}
}

// Encode encodes a byte slice to Base64 string
func Encode(data []byte, encType ...EncodingType) string {
	et := Standard
	if len(encType) > 0 {
		et = encType[0]
	}
	return getEncoder(et).EncodeToString(data)
}

// EncodeString encodes a string to Base64 string
func EncodeString(s string, encType ...EncodingType) string {
	return Encode([]byte(s), encType...)
}

// Decode decodes a Base64 string to byte slice
func Decode(encoded string, encType ...EncodingType) ([]byte, error) {
	if encoded == "" {
		return nil, ErrEmptyInput
	}

	et := Standard
	if len(encType) > 0 {
		et = encType[0]
	}

	decoded, err := getEncoder(et).DecodeString(encoded)
	if err != nil {
		return nil, fmt.Errorf("%w: %v", ErrInvalidBase64, err)
	}
	return decoded, nil
}

// DecodeString decodes a Base64 string to string
func DecodeString(encoded string, encType ...EncodingType) (string, error) {
	decoded, err := Decode(encoded, encType...)
	if err != nil {
		return "", err
	}
	return string(decoded), nil
}

// AutoDecode automatically detects encoding type and decodes
func AutoDecode(encoded string) ([]byte, error) {
	if encoded == "" {
		return nil, ErrEmptyInput
	}

	// Try different encodings in order
	encodings := []EncodingType{Standard, URLSafe, RawStandard, RawURLSafe}
	
	for _, et := range encodings {
		decoded, err := Decode(encoded, et)
		if err == nil {
			return decoded, nil
		}
	}

	// Try with padding fix
	padding := 4 - (len(encoded) % 4)
	if padding > 0 && padding < 4 {
		padded := encoded + strings.Repeat("=", padding)
		for _, et := range encodings {
			decoded, err := Decode(padded, et)
			if err == nil {
				return decoded, nil
			}
		}
	}

	return nil, ErrInvalidBase64
}

// EncodeFile encodes a file's content to Base64 string
func EncodeFile(filePath string, encType ...EncodingType) (string, error) {
	data, err := os.ReadFile(filePath)
	if err != nil {
		if os.IsNotExist(err) {
			return "", ErrFileNotFound
		}
		return "", fmt.Errorf("failed to read file: %w", err)
	}
	return Encode(data, encType...), nil
}

// DecodeToFile decodes a Base64 string and writes to a file
func DecodeToFile(encoded string, filePath string, encType ...EncodingType) error {
	decoded, err := Decode(encoded, encType...)
	if err != nil {
		return err
	}

	err = os.WriteFile(filePath, decoded, 0644)
	if err != nil {
		return fmt.Errorf("%w: %v", ErrFileWriteFailed, err)
	}
	return nil
}

// EncodeReader encodes all data from a reader to Base64 string
func EncodeReader(r io.Reader, encType ...EncodingType) (string, error) {
	data, err := io.ReadAll(r)
	if err != nil {
		return "", fmt.Errorf("failed to read: %w", err)
	}
	return Encode(data, encType...), nil
}

// DecodeWriter returns a writer that decodes Base64 data as it writes
type DecodeWriter struct {
	encoder   *base64.Encoding
	buffer    []byte
	output    io.Writer
	encType   EncodingType
}

// NewDecodeWriter creates a new DecodeWriter
func NewDecodeWriter(w io.Writer, encType ...EncodingType) *DecodeWriter {
	et := Standard
	if len(encType) > 0 {
		et = encType[0]
	}
	return &DecodeWriter{
		encoder: getEncoder(et),
		output:  w,
		encType: et,
	}
}

// Write decodes Base64 data and writes the decoded bytes
func (dw *DecodeWriter) Write(p []byte) (n int, err error) {
	dw.buffer = append(dw.buffer, p...)
	decoded, err := dw.encoder.DecodeString(string(dw.buffer))
	if err != nil {
		return len(p), err
	}
	dw.buffer = dw.buffer[:0]
	return dw.output.Write(decoded)
}

// IsValid checks if a string is valid Base64
func IsValid(s string, encType ...EncodingType) bool {
	if s == "" {
		return false
	}

	et := Standard
	if len(encType) > 0 {
		et = encType[0]
	}

	_, err := getEncoder(et).DecodeString(s)
	return err == nil
}

// IsValidAny checks if a string is valid in any Base64 encoding
func IsValidAny(s string) bool {
	_, err := AutoDecode(s)
	return err == nil
}

// GetEncodingType attempts to detect the encoding type of a Base64 string
func GetEncodingType(encoded string) (EncodingType, error) {
	if encoded == "" {
		return Standard, ErrEmptyInput
	}

	// Check for URL-safe characters
	hasURLSafe := strings.ContainsAny(encoded, "-_")
	hasStandard := strings.ContainsAny(encoded, "+/")

	// Check padding
	hasPadding := strings.HasSuffix(encoded, "=")
	
	// URL-safe encoding
	if hasURLSafe && !hasStandard {
		if hasPadding {
			return URLSafe, nil
		}
		return RawURLSafe, nil
	}

	// Standard encoding
	if hasStandard || hasPadding {
		if hasPadding {
			return Standard, nil
		}
		return RawStandard, nil
	}

	// Without special characters, try to decode with each
	encodings := []EncodingType{Standard, URLSafe, RawStandard, RawURLSafe}
	for _, et := range encodings {
		if IsValid(encoded, et) {
			return et, nil
		}
	}

	return Standard, ErrInvalidBase64
}

// AddPadding adds standard padding to a Base64 string
func AddPadding(encoded string) string {
	padding := 4 - (len(encoded) % 4)
	if padding > 0 && padding < 4 {
		return encoded + strings.Repeat("=", padding)
	}
	return encoded
}

// RemovePadding removes padding from a Base64 string
func RemovePadding(encoded string) string {
	return strings.TrimRight(encoded, "=")
}

// ConvertEncoding converts between Base64 encoding types
func ConvertEncoding(encoded string, from, to EncodingType) (string, error) {
	decoded, err := Decode(encoded, from)
	if err != nil {
		return "", err
	}
	return Encode(decoded, to), nil
}

// ChunkedEncode encodes data with line breaks every 76 characters (MIME format)
func ChunkedEncode(data []byte, encType ...EncodingType) string {
	encoded := Encode(data, encType...)
	return chunkString(encoded, 76)
}

// ChunkedDecode decodes a chunked Base64 string
func ChunkedDecode(encoded string, encType ...EncodingType) ([]byte, error) {
	// Remove whitespace and newlines
	cleaned := strings.ReplaceAll(encoded, "\n", "")
	cleaned = strings.ReplaceAll(cleaned, "\r", "")
	cleaned = strings.ReplaceAll(cleaned, " ", "")
	return Decode(cleaned, encType...)
}

// chunkString splits a string into chunks of specified size
func chunkString(s string, size int) string {
	if len(s) <= size {
		return s
	}
	
	var result strings.Builder
	for i := 0; i < len(s); i += size {
		end := i + size
		if end > len(s) {
			end = len(s)
		}
		result.WriteString(s[i:end])
		if end < len(s) {
			result.WriteByte('\n')
		}
	}
	return result.String()
}

// EncodeLines encodes multiple strings and returns as slice
func EncodeLines(lines []string, encType ...EncodingType) []string {
	result := make([]string, len(lines))
	for i, line := range lines {
		result[i] = EncodeString(line, encType...)
	}
	return result
}

// DecodeLines decodes multiple Base64 strings and returns as slice
func DecodeLines(encodedLines []string, encType ...EncodingType) ([]string, error) {
	result := make([]string, len(encodedLines))
	for i, line := range encodedLines {
		decoded, err := DecodeString(line, encType...)
		if err != nil {
			return nil, fmt.Errorf("line %d: %w", i, err)
		}
		result[i] = decoded
	}
	return result, nil
}

// SafeEncodeString encodes with guaranteed valid UTF-8 output
func SafeEncodeString(s string, encType ...EncodingType) string {
	return EncodeString(s, encType...)
}

// SafeDecodeString decodes with error recovery, returns original string on error
func SafeDecodeString(encoded string, encType ...EncodingType) string {
	decoded, err := DecodeString(encoded, encType...)
	if err != nil {
		return encoded
	}
	return decoded
}

// Size returns the size of encoded output for given input size
func Size(inputSize int) int {
	return (inputSize + 2) / 3 * 4
}

// DecodeSize returns the maximum decoded size for given encoded size
func DecodeSize(encodedSize int) int {
	return encodedSize / 4 * 3
}