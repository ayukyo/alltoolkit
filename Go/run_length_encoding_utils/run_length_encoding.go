// Package run_length_encoding_utils provides Run-Length Encoding (RLE) utilities.
// Zero external dependencies - pure Go implementation.
//
// Run-Length Encoding is a simple form of data compression where consecutive
// identical elements are stored as a single data value and its count.
package run_length_encoding_utils

import (
	"bytes"
	"errors"
	"fmt"
)

// Errors
var (
	ErrInvalidInput = errors.New("invalid input for encoding/decoding")
	ErrEmptyInput   = errors.New("empty input")
)

// Run represents a single run in RLE encoding
type Run struct {
	Value byte
	Count int
}

// Encoded holds the RLE encoded data
type Encoded struct {
	Runs []Run
}

// Encode compresses a byte slice using Run-Length Encoding.
// Returns the encoded data or an error if input is empty.
func Encode(data []byte) (*Encoded, error) {
	if len(data) == 0 {
		return nil, ErrEmptyInput
	}

	runs := make([]Run, 0)
	current := data[0]
	count := 1

	for i := 1; i < len(data); i++ {
		if data[i] == current {
			count++
		} else {
			runs = append(runs, Run{Value: current, Count: count})
			current = data[i]
			count = 1
		}
	}
	runs = append(runs, Run{Value: current, Count: count})

	return &Encoded{Runs: runs}, nil
}

// Decode decompresses RLE encoded data back to original bytes.
func (e *Encoded) Decode() ([]byte, error) {
	if e == nil || len(e.Runs) == 0 {
		return nil, ErrEmptyInput
	}

	// Calculate total size
	totalSize := 0
	for _, run := range e.Runs {
		totalSize += run.Count
	}

	result := make([]byte, 0, totalSize)
	for _, run := range e.Runs {
		if run.Count <= 0 {
			return nil, fmt.Errorf("%w: invalid count %d for value %d", ErrInvalidInput, run.Count, run.Value)
		}
		for i := 0; i < run.Count; i++ {
			result = append(result, run.Value)
		}
	}

	return result, nil
}

// String returns a human-readable representation of the encoded data.
// Format: "value:count, value:count, ..."
func (e *Encoded) String() string {
	if e == nil || len(e.Runs) == 0 {
		return ""
	}

	var buf bytes.Buffer
	for i, run := range e.Runs {
		if i > 0 {
			buf.WriteString(", ")
		}
		fmt.Fprintf(&buf, "%d:%d", run.Value, run.Count)
	}
	return buf.String()
}

// Bytes returns the encoded data as a compact byte slice.
// Format: [value1, count1_high, count1_low, value2, count2_high, count2_low, ...]
// Note: This format limits count to 65535 (uint16 max)
func (e *Encoded) Bytes() ([]byte, error) {
	if e == nil || len(e.Runs) == 0 {
		return nil, ErrEmptyInput
	}

	result := make([]byte, 0, len(e.Runs)*3)
	for _, run := range e.Runs {
		if run.Count > 65535 {
			return nil, fmt.Errorf("%w: count %d exceeds uint16 max (65535)", ErrInvalidInput, run.Count)
		}
		result = append(result, run.Value)
		result = append(result, byte(run.Count>>8), byte(run.Count&0xFF))
	}
	return result, nil
}

// FromBytes decodes the compact byte format back to Encoded struct.
func FromBytes(data []byte) (*Encoded, error) {
	if len(data) == 0 {
		return nil, ErrEmptyInput
	}

	if len(data)%3 != 0 {
		return nil, fmt.Errorf("%w: data length must be multiple of 3", ErrInvalidInput)
	}

	runs := make([]Run, 0, len(data)/3)
	for i := 0; i < len(data); i += 3 {
		value := data[i]
		count := int(data[i+1])<<8 | int(data[i+2])
		if count == 0 {
			return nil, fmt.Errorf("%w: count cannot be zero", ErrInvalidInput)
		}
		runs = append(runs, Run{Value: value, Count: count})
	}

	return &Encoded{Runs: runs}, nil
}

// EncodeString is a convenience function to encode a string.
func EncodeString(s string) (*Encoded, error) {
	return Encode([]byte(s))
}

// DecodeToString is a convenience function to decode to a string.
func (e *Encoded) DecodeToString() (string, error) {
	data, err := e.Decode()
	if err != nil {
		return "", err
	}
	return string(data), nil
}

// Ratio returns the compression ratio (original size / encoded size).
// A ratio > 1 means compression, < 1 means expansion.
func (e *Encoded) Ratio() float64 {
	if e == nil || len(e.Runs) == 0 {
		return 0
	}

	originalSize := 0
	for _, run := range e.Runs {
		originalSize += run.Count
	}

	encodedSize := len(e.Runs) * 3 // Using Bytes() format
	if encodedSize == 0 {
		return 0
	}

	return float64(originalSize) / float64(encodedSize)
}

// OriginalSize returns the size of the original uncompressed data.
func (e *Encoded) OriginalSize() int {
	if e == nil {
		return 0
	}
	total := 0
	for _, run := range e.Runs {
		total += run.Count
	}
	return total
}

// NumRuns returns the number of runs in the encoded data.
func (e *Encoded) NumRuns() int {
	if e == nil {
		return 0
	}
	return len(e.Runs)
}

// EncodeWithEscape encodes data using an escape character for runs > 255.
// Format: value, count (if count <= 255) or escape, value, count_high, count_low
func EncodeWithEscape(data []byte, escape byte) (*Encoded, error) {
	return Encode(data) // Standard encoding, escape handled in BytesWithEscape
}

// BytesWithEscape returns encoded bytes with escape sequence for large counts.
func (e *Encoded) BytesWithEscape(escape byte) ([]byte, error) {
	if e == nil || len(e.Runs) == 0 {
		return nil, ErrEmptyInput
	}

	result := make([]byte, 0)
	for _, run := range e.Runs {
		if run.Value == escape {
			// Need to escape the escape character itself
			if run.Count <= 255 {
				result = append(result, escape, escape, byte(run.Count))
			} else {
				result = append(result, escape, escape)
				result = append(result, byte(run.Count>>8), byte(run.Count&0xFF))
			}
		} else if run.Count <= 255 {
			result = append(result, run.Value, byte(run.Count))
		} else {
			// Large count: use escape sequence
			result = append(result, escape, run.Value, byte(run.Count>>8), byte(run.Count&0xFF))
		}
	}
	return result, nil
}

// EncodeInts encodes a slice of integers using RLE.
// Returns runs of value:count pairs.
func EncodeInts(data []int) ([]IntRun, error) {
	if len(data) == 0 {
		return nil, ErrEmptyInput
	}

	runs := make([]IntRun, 0)
	current := data[0]
	count := 1

	for i := 1; i < len(data); i++ {
		if data[i] == current {
			count++
		} else {
			runs = append(runs, IntRun{Value: current, Count: count})
			current = data[i]
			count = 1
		}
	}
	runs = append(runs, IntRun{Value: current, Count: count})

	return runs, nil
}

// IntRun represents a run for integer encoding
type IntRun struct {
	Value int
	Count int
}

// DecodeInts decodes integer runs back to a slice.
func DecodeInts(runs []IntRun) ([]int, error) {
	if len(runs) == 0 {
		return nil, ErrEmptyInput
	}

	// Calculate total size
	totalSize := 0
	for _, run := range runs {
		totalSize += run.Count
	}

	result := make([]int, 0, totalSize)
	for _, run := range runs {
		if run.Count <= 0 {
			return nil, fmt.Errorf("%w: invalid count %d", ErrInvalidInput, run.Count)
		}
		for i := 0; i < run.Count; i++ {
			result = append(result, run.Value)
		}
	}

	return result, nil
}

// EncodeRunes encodes a slice of runes using RLE.
func EncodeRunes(data []rune) ([]RuneRun, error) {
	if len(data) == 0 {
		return nil, ErrEmptyInput
	}

	runs := make([]RuneRun, 0)
	current := data[0]
	count := 1

	for i := 1; i < len(data); i++ {
		if data[i] == current {
			count++
		} else {
			runs = append(runs, RuneRun{Value: current, Count: count})
			current = data[i]
			count = 1
		}
	}
	runs = append(runs, RuneRun{Value: current, Count: count})

	return runs, nil
}

// RuneRun represents a run for rune encoding
type RuneRun struct {
	Value rune
	Count int
}

// DecodeRunes decodes rune runs back to a slice.
func DecodeRunes(runs []RuneRun) ([]rune, error) {
	if len(runs) == 0 {
		return nil, ErrEmptyInput
	}

	totalSize := 0
	for _, run := range runs {
		totalSize += run.Count
	}

	result := make([]rune, 0, totalSize)
	for _, run := range runs {
		if run.Count <= 0 {
			return nil, fmt.Errorf("%w: invalid count %d", ErrInvalidInput, run.Count)
		}
		for i := 0; i < run.Count; i++ {
			result = append(result, run.Value)
		}
	}

	return result, nil
}

// EncodeStringRunes encodes a string by runes (handles Unicode correctly).
func EncodeStringRunes(s string) ([]RuneRun, error) {
	return EncodeRunes([]rune(s))
}

// DecodeRuneRunsToString decodes rune runs to a string.
func DecodeRuneRunsToString(runs []RuneRun) (string, error) {
	runes, err := DecodeRunes(runs)
	if err != nil {
		return "", err
	}
	return string(runes), nil
}

// Stats holds statistics about RLE encoding
type Stats struct {
	OriginalSize   int     // Original data size in bytes
	EncodedSize    int     // Encoded size in bytes (using Bytes() format)
	NumRuns        int     // Number of runs
	CompressionRatio float64 // Original size / encoded size
	AverageRunLength float64 // Average length of runs
	LongestRun      int     // Length of longest run
	MostCommonValue byte    // Most common value in runs
}

// Analyze returns statistics about the encoded data.
func (e *Encoded) Analyze() *Stats {
	if e == nil || len(e.Runs) == 0 {
		return nil
	}

	originalSize := e.OriginalSize()
	encodedSize := len(e.Runs) * 3

	// Find longest run and most common value
	longestRun := 0
	valueCounts := make(map[byte]int)
	totalRuns := 0

	for _, run := range e.Runs {
		totalRuns += run.Count
		if run.Count > longestRun {
			longestRun = run.Count
		}
		valueCounts[run.Value] += run.Count
	}

	var mostCommonValue byte
	maxCount := 0
	for v, c := range valueCounts {
		if c > maxCount {
			maxCount = c
			mostCommonValue = v
		}
	}

	avgRunLength := 0.0
	if len(e.Runs) > 0 {
		avgRunLength = float64(totalRuns) / float64(len(e.Runs))
	}

	compressionRatio := 0.0
	if encodedSize > 0 {
		compressionRatio = float64(originalSize) / float64(encodedSize)
	}

	return &Stats{
		OriginalSize:     originalSize,
		EncodedSize:      encodedSize,
		NumRuns:          len(e.Runs),
		CompressionRatio: compressionRatio,
		AverageRunLength: avgRunLength,
		LongestRun:       longestRun,
		MostCommonValue:  mostCommonValue,
	}
}

// IsCompressible checks if data is likely to benefit from RLE compression.
// Returns true if compression ratio would be > 1.
func IsCompressible(data []byte) bool {
	if len(data) < 3 {
		return false
	}

	encoded, err := Encode(data)
	if err != nil {
		return false
	}

	return encoded.Ratio() > 1.0
}