package main

import (
	"bytes"
	"fmt"
	"strings"

	base64_utils "github.com/ayukyo/alltoolkit/Go/base64_utils"
)

func main() {
	fmt.Println("=== Base64 Utils Examples ===")
	fmt.Println()

	// Example 1: Basic encoding and decoding
	fmt.Println("1. Basic Encoding/Decoding:")
	{
		text := "Hello, World!"
		encoded := base64_utils.EncodeString(text)
		fmt.Printf("   Original: %s\n", text)
		fmt.Printf("   Encoded:  %s\n", encoded)

		decoded, _ := base64_utils.DecodeString(encoded)
		fmt.Printf("   Decoded:  %s\n", decoded)
	}
	fmt.Println()

	// Example 2: Different encoding types
	fmt.Println("2. Different Encoding Types:")
	{
		text := "Hello!"
		fmt.Printf("   Original:       %s\n", text)
		fmt.Printf("   Standard:       %s\n", base64_utils.EncodeString(text, base64_utils.Standard))
		fmt.Printf("   URLSafe:        %s\n", base64_utils.EncodeString(text, base64_utils.URLSafe))
		fmt.Printf("   RawStandard:    %s\n", base64_utils.EncodeString(text, base64_utils.RawStandard))
		fmt.Printf("   RawURLSafe:     %s\n", base64_utils.EncodeString(text, base64_utils.RawURLSafe))
	}
	fmt.Println()

	// Example 3: URL-safe encoding for query strings
	fmt.Println("3. URL-Safe Encoding (for URLs):")
	{
		query := "?name=John&age=30"
		standardEncoded := base64_utils.EncodeString(query, base64_utils.Standard)
		urlSafeEncoded := base64_utils.EncodeString(query, base64_utils.URLSafe)
		
		fmt.Printf("   Query:               %s\n", query)
		fmt.Printf("   Standard (with +/): %s\n", standardEncoded)
		fmt.Printf("   URLSafe (with -_):  %s\n", urlSafeEncoded)
		fmt.Println("   Note: URL-safe encoding replaces + and / with - and _")
	}
	fmt.Println()

	// Example 4: Auto-detect and decode
	fmt.Println("4. Auto-Detect Encoding:")
	{
		encodedStrings := []string{
			"SGVsbG8sIFdvcmxkIQ==",  // Standard with padding
			"SGVsbG8sIFdvcmxkIQ",    // Raw (no padding)
			"P3F1ZXJ5PXZhbHVl",      // URL-safe
		}

		for i, enc := range encodedStrings {
			decoded, err := base64_utils.AutoDecode(enc)
			if err != nil {
				fmt.Printf("   %d. Error: %v\n", i+1, err)
			} else {
				fmt.Printf("   %d. '%s' -> '%s'\n", i+1, enc, string(decoded))
			}
		}
	}
	fmt.Println()

	// Example 5: Validation
	fmt.Println("5. Validation:")
	{
		testStrings := []string{
			"SGVsbG8sIFdvcmxkIQ==",  // Valid standard
			"SGVsbG8sIFdvcmxkIQ",    // Valid raw
			"!!!invalid!!!",          // Invalid
			"",                       // Empty
		}

		for _, s := range testStrings {
			valid := base64_utils.IsValidAny(s)
			fmt.Printf("   '%s' -> Valid: %v\n", s, valid)
		}
	}
	fmt.Println()

	// Example 6: Padding operations
	fmt.Println("6. Padding Operations:")
	{
		encoded := "SGVsbG8sIFdvcmxkIQ"
		padded := base64_utils.AddPadding(encoded)
		unpadded := base64_utils.RemovePadding(padded)

		fmt.Printf("   Original:  %s\n", encoded)
		fmt.Printf("   Padded:   %s\n", padded)
		fmt.Printf("   Unpadded: %s\n", unpadded)
	}
	fmt.Println()

	// Example 7: Chunked encoding (MIME format)
	fmt.Println("7. Chunked Encoding (MIME format):")
	{
		longText := strings.Repeat("Hello World! ", 10)
		chunked := base64_utils.ChunkedEncode([]byte(longText))
		
		fmt.Printf("   Original length: %d\n", len(longText))
		fmt.Printf("   Chunked output:\n")
		lines := strings.Split(chunked, "\n")
		for i, line := range lines {
			fmt.Printf("     Line %d: %s\n", i+1, line)
		}

		decoded, _ := base64_utils.ChunkedDecode(chunked)
		fmt.Printf("   Decoded matches: %v\n", string(decoded) == longText)
	}
	fmt.Println()

	// Example 8: Batch operations
	fmt.Println("8. Batch Operations:")
	{
		lines := []string{"First line", "Second line", "Third line"}
		
		encoded := base64_utils.EncodeLines(lines)
		fmt.Println("   Encoded lines:")
		for i, e := range encoded {
			fmt.Printf("     %d: %s\n", i+1, e)
		}

		decoded, _ := base64_utils.DecodeLines(encoded)
		fmt.Println("   Decoded lines:")
		for i, d := range decoded {
			fmt.Printf("     %d: %s\n", i+1, d)
		}
	}
	fmt.Println()

	// Example 9: Encoding conversion
	fmt.Println("9. Encoding Conversion:")
	{
		standard := "SGVsbG8sIFdvcmxkIQ=="
		
		// Convert to URL-safe
		urlSafe, _ := base64_utils.ConvertEncoding(standard, base64_utils.Standard, base64_utils.URLSafe)
		fmt.Printf("   Standard:      %s\n", standard)
		fmt.Printf("   To URLSafe:   %s\n", urlSafe)
		
		// Convert to raw (no padding)
		raw, _ := base64_utils.ConvertEncoding(standard, base64_utils.Standard, base64_utils.RawStandard)
		fmt.Printf("   To Raw:       %s\n", raw)
	}
	fmt.Println()

	// Example 10: Binary data
	fmt.Println("10. Binary Data:")
	{
		binary := []byte{0x00, 0x01, 0x02, 0xFF, 0xFE, 0xFD}
		encoded := base64_utils.Encode(binary)
		decoded, _ := base64_utils.Decode(encoded)

		fmt.Printf("   Original bytes: %v\n", binary)
		fmt.Printf("   Encoded:        %s\n", encoded)
		fmt.Printf("   Decoded bytes:  %v\n", decoded)
		fmt.Printf("   Match:          %v\n", bytes.Equal(binary, decoded))
	}
	fmt.Println()

	// Example 11: Size calculations
	fmt.Println("11. Size Calculations:")
	{
		inputSize := 100
		encodedSize := base64_utils.Size(inputSize)
		maxDecodedSize := base64_utils.DecodeSize(encodedSize)

		fmt.Printf("   Input size:         %d bytes\n", inputSize)
		fmt.Printf("   Encoded size:       %d characters\n", encodedSize)
		fmt.Printf("   Max decoded size:   %d bytes\n", maxDecodedSize)
	}
	fmt.Println()

	// Example 12: Safe operations
	fmt.Println("12. Safe Operations:")
	{
		// Safe encode
		safe := base64_utils.SafeEncodeString("Hello!")
		fmt.Printf("   Safe encode: %s\n", safe)

		// Safe decode with valid input
		decoded := base64_utils.SafeDecodeString(safe)
		fmt.Printf("   Safe decode (valid): %s\n", decoded)

		// Safe decode with invalid input (returns original)
		invalid := "!!!not base64!!!"
		result := base64_utils.SafeDecodeString(invalid)
		fmt.Printf("   Safe decode (invalid): %s (returned original)\n", result)
	}
	fmt.Println()

	// Example 13: Encoding type detection
	fmt.Println("13. Encoding Type Detection:")
	{
		testCases := []string{
			"SGVsbG8sIFdvcmxkIQ==",  // Standard
			"SGVsbG8sIFdvcmxkIQ",    // Raw
			"P3F1ZXJ5PXZhbHVl",      // Could be any
		}

		for _, s := range testCases {
			encType, err := base64_utils.GetEncodingType(s)
			if err != nil {
				fmt.Printf("   '%s' -> Error: %v\n", s, err)
			} else {
				typeName := "Unknown"
				switch encType {
				case base64_utils.Standard:
					typeName = "Standard"
				case base64_utils.URLSafe:
					typeName = "URLSafe"
				case base64_utils.RawStandard:
					typeName = "RawStandard"
				case base64_utils.RawURLSafe:
					typeName = "RawURLSafe"
				}
				fmt.Printf("   '%s' -> Type: %s\n", s, typeName)
			}
		}
	}
	fmt.Println()

	fmt.Println("=== All examples completed! ===")
}