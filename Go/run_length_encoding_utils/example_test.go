package run_length_encoding_utils_test

import (
	"fmt"
	"strings"

	"github.com/ayukyo/alltoolkit/Go/run_length_encoding_utils"
)

// Example_basic demonstrates basic RLE encoding and decoding
func Example_basic() {
	// Encode some data with repeated bytes
	data := []byte("AAAAABBBCCCCCDD")
	encoded, err := run_length_encoding_utils.Encode(data)
	if err != nil {
		panic(err)
	}

	fmt.Printf("Original: %s\n", data)
	fmt.Printf("Encoded runs: %s\n", encoded.String())
	fmt.Printf("Number of runs: %d\n", encoded.NumRuns())
	fmt.Printf("Original size: %d bytes\n", encoded.OriginalSize())
	fmt.Printf("Compression ratio: %.2f\n", encoded.Ratio())

	// Decode back to original
	decoded, err := encoded.Decode()
	if err != nil {
		panic(err)
	}

	fmt.Printf("Decoded: %s\n", decoded)
	fmt.Printf("Match: %v\n", string(decoded) == string(data))

	// Output:
	// Original: AAAAABBBCCCCCDD
	// Encoded runs: 65:5, 66:3, 67:5, 68:2
	// Number of runs: 4
	// Original size: 15 bytes
	// Compression ratio: 1.25
	// Decoded: AAAAABBBCCCCCDD
	// Match: true
}

// Example_stringEncoding demonstrates encoding strings
func Example_stringEncoding() {
	// Encode a string
	encoded, err := run_length_encoding_utils.EncodeString("WWWWWWWWWWWWWWWWWWWWWWWW")
	if err != nil {
		panic(err)
	}

	fmt.Printf("Original: 24 W's\n")
	fmt.Printf("Runs: %s\n", encoded.String())

	decoded, _ := encoded.DecodeToString()
	fmt.Printf("Decoded: %s\n", decoded)

	// Output:
	// Original: 24 W's
	// Runs: 87:24
	// Decoded: WWWWWWWWWWWWWWWWWWWWWWWW
}

// Example_bytes demonstrates packing encoded data into bytes
func Example_bytes() {
	data := []byte("AAAAABBBBCCCCC")
	encoded, _ := run_length_encoding_utils.Encode(data)

	// Pack into compact byte format
	packed, err := encoded.Bytes()
	if err != nil {
		panic(err)
	}

	fmt.Printf("Original size: %d bytes\n", len(data))
	fmt.Printf("Packed size: %d bytes\n", len(packed))

	// Unpack and decode
	decoded, _ := run_length_encoding_utils.FromBytes(packed)
	result, _ := decoded.Decode()

	fmt.Printf("Match: %v\n", string(result) == string(data))

	// Output:
	// Original size: 14 bytes
	// Packed size: 9 bytes
	// Match: true
}

// Example_analyze demonstrates analyzing encoded data
func Example_analyze() {
	// Create some data with varying repetition
	data := []byte("AAAAABBBBBBBCCCCC")
	encoded, _ := run_length_encoding_utils.Encode(data)

	stats := encoded.Analyze()

	fmt.Printf("Original size: %d bytes\n", stats.OriginalSize)
	fmt.Printf("Encoded size: %d bytes\n", stats.EncodedSize)
	fmt.Printf("Number of runs: %d\n", stats.NumRuns)
	fmt.Printf("Compression ratio: %.2f\n", stats.CompressionRatio)
	fmt.Printf("Average run length: %.2f\n", stats.AverageRunLength)
	fmt.Printf("Longest run: %d\n", stats.LongestRun)
	fmt.Printf("Most common value: %q (ASCII %d)\n", stats.MostCommonValue, stats.MostCommonValue)

	// Output:
	// Original size: 17 bytes
	// Encoded size: 9 bytes
	// Number of runs: 3
	// Compression ratio: 1.89
	// Average run length: 5.67
	// Longest run: 7
	// Most common value: 'B' (ASCII 66)
}

// Example_ints demonstrates encoding integer slices
func Example_ints() {
	data := []int{1, 1, 1, 2, 2, 3, 3, 3, 3, 3, 4, 4}

	runs, err := run_length_encoding_utils.EncodeInts(data)
	if err != nil {
		panic(err)
	}

	fmt.Println("Runs:")
	for _, run := range runs {
		fmt.Printf("  Value: %d, Count: %d\n", run.Value, run.Count)
	}

	decoded, _ := run_length_encoding_utils.DecodeInts(runs)
	fmt.Printf("Decoded: %v\n", decoded)
	fmt.Printf("Match: %v\n", fmt.Sprintf("%v", data) == fmt.Sprintf("%v", decoded))

	// Output:
	// Runs:
	//   Value: 1, Count: 3
	//   Value: 2, Count: 2
	//   Value: 3, Count: 5
	//   Value: 4, Count: 2
	// Decoded: [1 1 1 2 2 3 3 3 3 3 4 4]
	// Match: true
}

// Example_runes demonstrates encoding Unicode strings
func Example_runes() {
	// Unicode string with repeated emojis
	text := "🚀🚀🚀🌟🌟🌟🌟"
	runs, _ := run_length_encoding_utils.EncodeStringRunes(text)

	fmt.Printf("Original: %s\n", text)
	fmt.Println("Runs:")
	for _, run := range runs {
		fmt.Printf("  Rune: %c, Count: %d\n", run.Value, run.Count)
	}

	decoded, _ := run_length_encoding_utils.DecodeRuneRunsToString(runs)
	fmt.Printf("Decoded: %s\n", decoded)
	fmt.Printf("Match: %v\n", text == decoded)

	// Output:
	// Original: 🚀🚀🚀🌟🌟🌟🌟
	// Runs:
	//   Rune: 🚀, Count: 3
	//   Rune: 🌟, Count: 4
	// Decoded: 🚀🚀🚀🌟🌟🌟🌟
	// Match: true
}

// Example_isCompressible demonstrates checking if data benefits from RLE
func Example_isCompressible() {
	tests := []string{
		"AAAAAAAAAAAAAA", // Highly compressible
		"ABABABABABAB",   // Not compressible
		"ABCDEFGHIJKLM",  // Not compressible
		"AAAABBBBCCCC",   // Compressible
	}

	for _, s := range tests {
		compressible := run_length_encoding_utils.IsCompressible([]byte(s))
		fmt.Printf("%q: compressible=%v\n", s, compressible)
	}

	// Output:
	// "AAAAAAAAAAAAAA": compressible=true
	// "ABABABABABAB": compressible=false
	// "ABCDEFGHIJKLM": compressible=false
	// "AAAABBBBCCCC": compressible=true
}

// Example_imageData demonstrates a practical use case
func Example_imageData() {
	// Simulate a simple grayscale image row (like in BMP compression)
	// Values: 0-255 representing pixel brightness
	imageRow := []byte{
		255, 255, 255, 255, 255, 255, 255, 255, 255, 255, // 10 white pixels
		0, 0, 0, 0, 0, // 5 black pixels
		128, 128, 128, // 3 gray pixels
		0, 0, 0, 0, 0, 0, 0, // 7 black pixels
		255, 255, 255, 255, 255, // 5 white pixels
	}

	encoded, _ := run_length_encoding_utils.Encode(imageRow)

	fmt.Printf("Original image row: %d bytes\n", len(imageRow))
	fmt.Printf("RLE encoded: %d runs\n", encoded.NumRuns())

	stats := encoded.Analyze()
	fmt.Printf("Compression ratio: %.2fx\n", stats.CompressionRatio)
	fmt.Printf("Space saved: %d%%\n",
		100-int(float64(stats.EncodedSize)/float64(stats.OriginalSize)*100))

	// Output:
	// Original image row: 30 bytes
	// RLE encoded: 5 runs
	// Compression ratio: 2.00x
	// Space saved: 50%
}

// Example_escapeEncoding demonstrates handling escape characters
func Example_escapeEncoding() {
	data := []byte("AAAA\x00BBBB") // Data with null bytes
	escape := byte(0x00)

	encoded, _ := run_length_encoding_utils.Encode(data)
	packed, _ := encoded.BytesWithEscape(escape)

	fmt.Printf("Original: %q (len=%d)\n", data, len(data))
	fmt.Printf("Packed: %d bytes\n", len(packed))

	// The packed format handles the escape character specially
	fmt.Printf("Contains null byte: %v\n", strings.Contains(fmt.Sprintf("%x", packed), "00"))

	// Output:
	// Original: "AAAA\x00BBBB" (len=9)
	// Packed: 7 bytes
	// Contains null byte: true
}