// Example usage of huffman_utils package
package main

import (
	"fmt"
	"strings"

	huffman "github.com/ayukyo/alltoolkit/Go/huffman_utils"
)

func main() {
	fmt.Println("=== Huffman Encoding Utility Examples ===")
	fmt.Println()

	// Example 1: Basic encoding and decoding
	example1BasicEncoding()

	// Example 2: Frequency analysis
	example2FrequencyAnalysis()

	// Example 3: Compression statistics
	example3CompressionStats()

	// Example 4: Canonical Huffman codes
	example4CanonicalCodes()

	// Example 5: Streaming encoder
	example5StreamingEncoder()

	// Example 6: File operations
	example6FileOperations()

	// Example 7: Adaptive Huffman coding
	example7AdaptiveHuffman()

	// Example 8: Custom data encoding
	example8CustomData()

	// Example 9: Efficiency analysis
	example9EfficiencyAnalysis()

	// Example 10: Large data compression
	example10LargeDataCompression()
}

func example1BasicEncoding() {
	fmt.Println("=== Example 1: Basic Encoding and Decoding ===")

	// Original data
	data := []byte("hello world! this is a test for huffman encoding.")

	// Encode
	result := huffman.Encode(data)

	fmt.Printf("Original: %s\n", data)
	fmt.Printf("Original size: %d bytes (%d bits)\n", result.OriginalSize, result.OriginalSize*8)
	fmt.Printf("Encoded size: %d bytes (%d bits)\n", result.EncodedSize, result.BitLength)
	fmt.Printf("Compression ratio: %.2fx\n", result.CompressionRatio)
	fmt.Println()

	// Show code table
	fmt.Println("Code table:")
	for char, code := range result.CodeTable {
		fmt.Printf("  '%c' (%d): %s\n", char, char, code)
	}
	fmt.Println()

	// Decode
	tree := huffman.BuildTreeFromData(data)
	decoded := huffman.Decode(result.EncodedData, tree, result.BitLength)

	fmt.Printf("Decoded: %s\n", decoded.Data)
	fmt.Printf("Decode success: %v\n", decoded.Success)
	fmt.Println()
}

func example2FrequencyAnalysis() {
	fmt.Println("=== Example 2: Frequency Analysis ===")

	text := "the quick brown fox jumps over the lazy dog"

	// Count frequencies
	freq := huffman.CountFrequenciesFromString(text)

	fmt.Printf("Text: %s\n", text)
	fmt.Println("\nCharacter frequencies:")

	top := huffman.GetTopFrequencies(freq, 10)
	for i, item := range top {
		fmt.Printf("  %d. '%c': %d occurrences\n", i+1, item.Char, item.Count)
	}
	fmt.Println()

	// Calculate entropy
	entropy := huffman.CalculateEntropy(freq, len(text))
	fmt.Printf("Shannon entropy: %.4f bits/char\n", entropy)
	fmt.Printf("Minimum bits needed: %.0f\n", entropy*float64(len(text)))
	fmt.Println()
}

func example3CompressionStats() {
	fmt.Println("=== Example 3: Compression Statistics ===")

	// Different data patterns
	datasets := []struct {
		name string
		data string
	}{
		{"Uniform random", "abcdefghijklmnopqrstuvwxyz"},
		{"Repeated pattern", "abcabcabcabcabcabcabcabcabcabc"},
		{"Skewed distribution", "aaaaaaaaaabbbbcccd"},
		{"Single character", "aaaaaaaaaaaaaaa"},
		{"Binary data", "\x00\x00\x00\xff\xff\x00\xff"},
	}

	for _, ds := range datasets {
		data := []byte(ds.data)
		result := huffman.Encode(data)
		stats := huffman.GetCompressionStats(data, result.EncodedData, result.BitLength)

		fmt.Printf("%s:\n", ds.name)
		fmt.Printf("  Original: %d bytes\n", stats.OriginalSize)
		fmt.Printf("  Encoded: %d bytes (%d bits)\n", stats.EncodedSize, stats.BitLength)
		fmt.Printf("  Space saved: %.2f%%\n", stats.SpaceSaved)
		fmt.Printf("  Compression ratio: %.2fx\n", stats.CompressionRatio)
		fmt.Println()
	}
}

func example4CanonicalCodes() {
	fmt.Println("=== Example 4: Canonical Huffman Codes ===")

	// Define code lengths
	codeLengths := map[byte]int{
		'A': 2,
		'B': 2,
		'C': 3,
		'D': 3,
		'E': 3,
		'F': 4,
	}

	// Build canonical codes
	codes := huffman.BuildCanonicalCodes(codeLengths)

	fmt.Println("Canonical Huffman codes:")
	chars := []byte{'A', 'B', 'C', 'D', 'E', 'F'}
	for _, c := range chars {
		fmt.Printf("  '%c': %s (%d bits)\n", c, codes[c], codeLengths[c])
	}
	fmt.Println()

	// Build canonical tree
	tree := huffman.BuildCanonicalTree(codeLengths)

	// Verify tree
	stats := huffman.GetCodeTableStats(tree.CodeTable)
	fmt.Printf("Code statistics:\n")
	fmt.Printf("  Min length: %d\n", stats.MinLength)
	fmt.Printf("  Max length: %d\n", stats.MaxLength)
	fmt.Printf("  Avg length: %.2f\n", stats.AvgLength)
	fmt.Println()
}

func example5StreamingEncoder() {
	fmt.Println("=== Example 5: Streaming Encoder ===")

	// Build frequency table from training data
	trainData := "the quick brown fox jumps over the lazy dog"
	freq := huffman.CountFrequenciesFromString(trainData)

	// Create streaming encoder
	encoder := huffman.NewEncoder(freq)

	// Encode data in chunks
	chunks := []string{"hello ", "world ", "this ", "is ", "streaming"}
	for _, chunk := range chunks {
		encoder.WriteBytes([]byte(chunk))
	}

	result := encoder.GetResult()
	fmt.Printf("Streamed encoding:\n")
	fmt.Printf("  Total bits: %d\n", result.BitLength)
	fmt.Printf("  Encoded bytes: %d\n", len(result.EncodedData))

	// Decode
	tree := encoder.GetTree()
	decoder := huffman.NewDecoder(tree, result.EncodedData)
	decoded, _ := decoder.ReadAll()

	fmt.Printf("  Decoded: %s\n", decoded)
	fmt.Println()
}

func example6FileOperations() {
	fmt.Println("=== Example 6: File Operations ===")

	// Simulate file data
	data := []byte(strings.Repeat("This is test content for file operations. ", 50))

	// Encode
	result := huffman.Encode(data)

	// Serialize to bytes (for file storage)
	serialized := huffman.SerializeEncodedData(result)
	fmt.Printf("Original data: %d bytes\n", len(data))
	fmt.Printf("Serialized (with tree): %d bytes\n", len(serialized))
	fmt.Printf("Space saved: %.2f%%\n",
		float64(len(data)-len(serialized))/float64(len(data))*100)

	// Deserialize
	deserialized, err := huffman.DeserializeEncodedData(serialized)
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		return
	}

	// Decode
	tree := &huffman.HuffmanTree{
		CodeTable: deserialized.CodeTable,
		CharTable: make(map[string]byte),
	}
	for char, code := range deserialized.CodeTable {
		tree.CharTable[code] = char
	}

	decoded := huffman.Decode(deserialized.EncodedData, tree, deserialized.BitLength)
	fmt.Printf("Decoded data: %d bytes\n", len(decoded.Data))
	fmt.Printf("Round trip success: %v\n", decoded.Success && len(decoded.Data) == len(data))
	fmt.Println()
}

func example7AdaptiveHuffman() {
	fmt.Println("=== Example 7: Adaptive Huffman Coding ===")

	// Create adaptive encoder
	encoder := huffman.NewAdaptiveEncoder()

	data := []byte("aabbbc")

	fmt.Printf("Original: %s\n", data)
	fmt.Println("Adaptive encoding process:")

	for i, b := range data {
		code, first := encoder.EncodeByte(b)
		occurrence := "repeat"
		if first {
			occurrence = "first"
		}
		fmt.Printf("  '%c' [%s]: %s\n", b, occurrence, code)

		if i < 3 { // Show tree state for first few
			// Tree evolves with each character
		}
	}
	fmt.Println()
}

func example8CustomData() {
	fmt.Println("=== Example 8: Custom Data Encoding ===")

	// Encode structured data
	type Record struct {
		id   byte
		data string
	}

	records := []Record{
		{1, "apple"},
		{2, "banana"},
		{3, "cherry"},
	}

	// Combine all data for frequency analysis
	var allData []byte
	for _, r := range records {
		allData = append(allData, r.id)
		allData = append(allData, []byte(r.data)...)
	}

	// Build tree and encode
	tree := huffman.BuildTreeFromData(allData)
	result := huffman.EncodeWithTree(allData, tree)

	fmt.Printf("Records encoded: %d\n", len(records))
	fmt.Printf("Total data: %d bytes\n", len(allData))
	fmt.Printf("Encoded: %d bits (%.2f bytes)\n", result.BitLength, float64(result.BitLength)/8)
	fmt.Printf("Compression ratio: %.2fx\n", result.CompressionRatio)
	fmt.Println()

	// Show some codes
	fmt.Println("Sample codes:")
	count := 0
	for char, code := range result.CodeTable {
		if count >= 5 {
			break
		}
		fmt.Printf("  %d ('%c'): %s\n", char, char, code)
		count++
	}
	fmt.Println()
}

func example9EfficiencyAnalysis() {
	fmt.Println("=== Example 9: Efficiency Analysis ===")

	// Different text samples
	samples := []struct {
		name string
		text string
	}{
		{"English text", "the quick brown fox jumps over the lazy dog the quick brown fox"},
		{"Repeated pattern", "abcabcabcabcabcabcabcabcabcabcabcabcabc"},
		{"Limited alphabet", "aabbaabbaabbaabbaabb"},
		{"Random-ish", "q8w2e4r5t6y7u8i9o0p1a2s3d4f5g6h7j8k9l0"},
	}

	for _, sample := range samples {
		data := []byte(sample.text)
		freq := huffman.CountFrequencies(data)
		tree := huffman.BuildTreeFromData(data)

		entropy := huffman.CalculateEntropy(freq, len(data))
		expectedLen := huffman.CalculateExpectedCodeLength(tree, freq)
		efficiency := huffman.CalculateEfficiency(tree, freq)
		avgLen := huffman.GetAverageCodeLength(tree)

		fmt.Printf("%s:\n", sample.name)
		fmt.Printf("  Distinct chars: %d\n", huffman.CountDistinctCharacters(data))
		fmt.Printf("  Entropy: %.4f bits/char\n", entropy)
		fmt.Printf("  Expected code length: %.4f\n", expectedLen)
		fmt.Printf("  Average code length: %.4f\n", avgLen)
		fmt.Printf("  Efficiency: %.2f%%\n", efficiency*100)
		fmt.Println()
	}
}

func example10LargeDataCompression() {
	fmt.Println("=== Example 10: Large Data Compression ===")

	// Generate large data with known distribution
	size := 10000
	data := make([]byte, size)
	for i := 0; i < size; i++ {
		r := i % 100
		switch {
		case r < 50: // 50% 'e'
			data[i] = 'e'
		case r < 70: // 20% 't'
			data[i] = 't'
		case r < 85: // 15% 'a'
			data[i] = 'a'
		case r < 95: // 10% 'o'
			data[i] = 'o'
		default: // 5% 'i'
			data[i] = 'i'
		}
	}

	// Encode
	result := huffman.Encode(data)
	tree := huffman.BuildTreeFromData(data)

	// Calculate theoretical minimum
	entropy := huffman.CalculateEntropy(result.Frequencies, size)
	theoreticalMin := entropy * float64(size)

	// Validate tree
	err := huffman.ValidateTree(tree.Root)

	fmt.Printf("Large data test (%d bytes):\n", size)
	fmt.Printf("  Original size: %d bytes\n", size)
	fmt.Printf("  Encoded size: %d bytes (%d bits)\n", result.EncodedSize, result.BitLength)
	fmt.Printf("  Compression ratio: %.2fx\n", result.CompressionRatio)
	fmt.Printf("  Space saved: %.2f%%\n",
		float64(size*8-result.BitLength)/float64(size*8)*100)
	fmt.Println()
	fmt.Printf("Theoretical analysis:\n")
	fmt.Printf("  Entropy: %.4f bits/char\n", entropy)
	fmt.Printf("  Theoretical minimum: %.0f bits\n", theoreticalMin)
	fmt.Printf("  Actual bits: %d\n", result.BitLength)
	fmt.Printf("  Efficiency: %.2f%%\n", theoreticalMin/float64(result.BitLength)*100)
	fmt.Println()

	fmt.Printf("Code lengths:\n")
	fmt.Printf("  Min: %d\n", huffman.GetMinCodeLength(tree))
	fmt.Printf("  Max: %d\n", huffman.GetMaxCodeLength(tree))
	fmt.Printf("  Avg: %.2f\n", huffman.GetAverageCodeLength(tree))
	fmt.Println()

	fmt.Printf("Tree validation: %v\n", err == nil)

	// Decode and verify
	decoded := huffman.Decode(result.EncodedData, tree, result.BitLength)
	fmt.Printf("Decode success: %v\n", decoded.Success)
	fmt.Printf("Data integrity: %v\n", len(decoded.Data) == size && string(decoded.Data) == string(data))
	fmt.Println()
}