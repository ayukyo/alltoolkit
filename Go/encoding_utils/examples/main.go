// Example usage of encoding_utils package
package main

import (
	"fmt"
	"strings"

	encoding_utils "github.com/ayukyo/alltoolkit/Go/encoding_utils"
)

func main() {
	fmt.Println("=" + strings.Repeat("=", 50))
	fmt.Println("Encoding Utils Examples")
	fmt.Println("=" + strings.Repeat("=", 50))

	// =========================================================================
	// Base64 Encoding/Decoding
	// =========================================================================
	fmt.Println("\n📦 Base64 Encoding/Decoding")
	fmt.Println(strings.Repeat("-", 40))

	text := "Hello, World!"
	encoded := encoding_utils.Base64EncodeString(text)
	fmt.Printf("Original: %s\n", text)
	fmt.Printf("Encoded:  %s\n", encoded)

	decoded, _ := encoding_utils.Base64DecodeString(encoded)
	fmt.Printf("Decoded:  %s\n", decoded)

	// URL-safe Base64
	urlSafe := encoding_utils.Base64URLEncode([]byte{0xff, 0xfe, 0xfd})
	fmt.Printf("URL-safe Base64: %s\n", urlSafe)

	// =========================================================================
	// Hex Encoding/Decoding
	// =========================================================================
	fmt.Println("\n📦 Hex Encoding/Decoding")
	fmt.Println(strings.Repeat("-", 40))

	hexEncoded := encoding_utils.HexEncodeString("ABC")
	fmt.Printf("Hex of 'ABC': %s\n", hexEncoded)

	hexDecoded, _ := encoding_utils.HexDecodeString(hexEncoded)
	fmt.Printf("Decoded: %s\n", hexDecoded)

	// =========================================================================
	// URL Encoding/Decoding
	// =========================================================================
	fmt.Println("\n📦 URL Encoding/Decoding")
	fmt.Println(strings.Repeat("-", 40))

	query := "name=John Doe&email=test@example.com"
	urlEncoded := encoding_utils.URLEncode(query)
	fmt.Printf("URL encoded: %s\n", urlEncoded)

	urlDecoded, _ := encoding_utils.URLDecode(urlEncoded)
	fmt.Printf("URL decoded: %s\n", urlDecoded)

	// Encode map to query string
	params := map[string]string{
		"name":  "John Doe",
		"email": "john@example.com",
		"page":  "1",
	}
	queryString := encoding_utils.URLEncodeMap(params)
	fmt.Printf("Query string: %s\n", queryString)

	// =========================================================================
	// HTML Escape/Unescape
	// =========================================================================
	fmt.Println("\n📦 HTML Escape/Unescape")
	fmt.Println(strings.Repeat("-", 40))

	htmlInput := `<script>alert("XSS")</script>`
	htmlEscaped := encoding_utils.HTMLEscape(htmlInput)
	fmt.Printf("Original: %s\n", htmlInput)
	fmt.Printf("Escaped:  %s\n", htmlEscaped)

	htmlUnescaped := encoding_utils.HTMLUnescape(htmlEscaped)
	fmt.Printf("Unescaped: %s\n", htmlUnescaped)

	// =========================================================================
	// ROT13 Encoding/Decoding
	// =========================================================================
	fmt.Println("\n📦 ROT13 Encoding/Decoding")
	fmt.Println(strings.Repeat("-", 40))

	rotInput := "Hello, World!"
	rotEncoded := encoding_utils.Rot13(rotInput)
	fmt.Printf("Original:  %s\n", rotInput)
	fmt.Printf("ROT13:     %s\n", rotEncoded)
	fmt.Printf("ROT13 again: %s (self-inverse)\n", encoding_utils.Rot13(rotEncoded))

	// Custom rotation
	rot5 := encoding_utils.RotN("abc", 5)
	fmt.Printf("ROT5 on 'abc': %s\n", rot5)

	// =========================================================================
	// Run-Length Encoding
	// =========================================================================
	fmt.Println("\n📦 Run-Length Encoding")
	fmt.Println(strings.Repeat("-", 40))

	rleInput := "aaaaaaaaaabbbccccc"
	rleEncoded := encoding_utils.RLEncodeString(rleInput)
	fmt.Printf("Original: %s (len=%d)\n", rleInput, len(rleInput))
	fmt.Printf("RLE encoded bytes: %v (len=%d)\n", []byte(rleEncoded), len(rleEncoded))

	rleDecoded, _ := encoding_utils.RLDecodeString(rleEncoded)
	fmt.Printf("Decoded: %s\n", rleDecoded)

	// =========================================================================
	// Binary Encoding/Decoding
	// =========================================================================
	fmt.Println("\n📦 Binary Encoding/Decoding")
	fmt.Println(strings.Repeat("-", 40))

	binaryInput := []byte{0xAB, 0xCD}
	binaryEncoded := encoding_utils.BinaryEncode(binaryInput)
	fmt.Printf("Binary of [0xAB, 0xCD]: %s\n", binaryEncoded)

	binaryDecoded, _ := encoding_utils.BinaryDecode(binaryEncoded)
	fmt.Printf("Decoded: %v\n", binaryDecoded)

	// =========================================================================
	// Unicode Escape/Unescape
	// =========================================================================
	fmt.Println("\n📦 Unicode Escape/Unescape")
	fmt.Println(strings.Repeat("-", 40))

	unicodeInput := "Hello 世界 🎉"
	unicodeEscaped := encoding_utils.UnicodeEscape(unicodeInput)
	fmt.Printf("Original: %s\n", unicodeInput)
	fmt.Printf("Escaped:  %s\n", unicodeEscaped)

	unicodeUnescaped, _ := encoding_utils.UnicodeUnescape(unicodeEscaped)
	fmt.Printf("Unescaped: %s\n", unicodeUnescaped)

	// =========================================================================
	// Quoted-Printable Encoding
	// =========================================================================
	fmt.Println("\n📦 Quoted-Printable Encoding")
	fmt.Println(strings.Repeat("-", 40))

	qpInput := "Hello = World 中文"
	qpEncoded := encoding_utils.QuotedPrintableEncode(qpInput)
	fmt.Printf("Original: %s\n", qpInput)
	fmt.Printf("Encoded:  %s\n", qpEncoded)

	qpDecoded, _ := encoding_utils.QuotedPrintableDecode(qpEncoded)
	fmt.Printf("Decoded:  %s\n", qpDecoded)

	// =========================================================================
	// Character Count
	// =========================================================================
	fmt.Println("\n📦 Character Count")
	fmt.Println(strings.Repeat("-", 40))

	str := "Hello 世界 🎉"
	runes, bytes := encoding_utils.CharCount(str)
	fmt.Printf("String: %s\n", str)
	fmt.Printf("Runes: %d, Bytes: %d\n", runes, bytes)

	printable := encoding_utils.IsPrintable("Hello World!")
	fmt.Printf("Is 'Hello World!' printable: %v\n", printable)

	// =========================================================================
	// Chunked Base64
	// =========================================================================
	fmt.Println("\n📦 Chunked Base64")
	fmt.Println(strings.Repeat("-", 40))

	data := make([]byte, 50)
	for i := range data {
		data[i] = byte(i)
	}
	chunked := encoding_utils.Base64ChunkedEncode(data, 32)
	fmt.Printf("Chunked Base64 (32 chars/line):\n%s\n", chunked)

	// =========================================================================
	// Streaming Base64
	// =========================================================================
	fmt.Println("\n📦 Streaming Base64 Encoder")
	fmt.Println(strings.Repeat("-", 40))

	encoder := encoding_utils.NewBase64StreamEncoder()
	encoder.Write([]byte("Hello"))
	encoder.Write([]byte(", "))
	encoder.Write([]byte("World!"))
	streamEncoded, _ := encoder.Close()
	fmt.Printf("Stream encoded: %s\n", streamEncoded)

	decoder := encoding_utils.NewBase64StreamDecoder(streamEncoded)
	streamDecoded, _ := decoder.ReadAll()
	fmt.Printf("Stream decoded: %s\n", string(streamDecoded))

	fmt.Println("\n" + strings.Repeat("=", 51))
	fmt.Println("All examples completed!")
}