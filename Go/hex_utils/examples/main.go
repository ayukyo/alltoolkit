// Example usage of hex_utils package
package main

import (
	"fmt"
	"log"

	hexutils "github.com/ayukyo/alltoolkit/Go/hex_utils"
)

func main() {
	fmt.Println("=== Hex Utils Examples ===\n")

	// Example 1: Basic encoding and decoding
	fmt.Println("--- Basic Encoding/Decoding ---")
	data := []byte("Hello, World!")
	encoded := hexutils.HexEncode(data)
	fmt.Printf("Original: %s\n", data)
	fmt.Printf("Encoded: %s\n", encoded)

	decoded, err := hexutils.HexDecode(encoded)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("Decoded: %s\n\n", decoded)

	// Example 2: String encoding/decoding
	fmt.Println("--- String Encoding/Decoding ---")
	text := "Hello, Hex!"
	hexStr := hexutils.HexEncodeString(text)
	fmt.Printf("Text: %s\n", text)
	fmt.Printf("Hex: %s\n", hexStr)

	original, err := hexutils.HexDecodeToString(hexStr)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("Back to text: %s\n\n", original)

	// Example 3: Validation
	fmt.Println("--- Validation ---")
	validHex := "48656c6c6f"
	invalidHex := "xyz123"
	fmt.Printf("'%s' is valid hex: %v\n", validHex, hexutils.IsHex(validHex))
	fmt.Printf("'%s' is valid hex: %v\n", invalidHex, hexutils.IsHex(invalidHex))
	fmt.Printf("Validation of '%s': %v\n\n", invalidHex, hexutils.ValidateHex(invalidHex))

	// Example 4: Uppercase encoding
	fmt.Println("--- Uppercase Encoding ---")
	upperHex := hexutils.HexEncodeUpper(data)
	fmt.Printf("Uppercase hex: %s\n\n", upperHex)

	// Example 5: Hex dump
	fmt.Println("--- Hex Dump ---")
	dumpData := []byte("This is a hex dump example showing the xxd-style output.")
	fmt.Println(hexutils.HexDump(dumpData))
	fmt.Println()

	// Example 6: Compact hex dump
	fmt.Println("--- Compact Hex Dump ---")
	fmt.Printf("Compact: %s\n\n", hexutils.HexDumpCompact([]byte("Hello")))

	// Example 7: C-style hex array
	fmt.Println("--- C-Style Hex Array ---")
	fmt.Println(hexutils.HexDumpCStyle([]byte{0x48, 0x65, 0x6c, 0x6c, 0x6f}, "hello"))
	fmt.Println()

	// Example 8: Python-style hex bytes
	fmt.Println("--- Python-Style Hex Bytes ---")
	fmt.Printf("%s\n\n", hexutils.HexDumpPythonStyle([]byte{0x48, 0x65, 0x6c, 0x6c, 0x6f}))

	// Example 9: Integer conversion
	fmt.Println("--- Integer Conversion ---")
	num, _ := hexutils.HexToInt("ff")
	fmt.Printf("HexToInt('ff'): %d\n", num)
	num2, _ := hexutils.HexToInt("0x10")
	fmt.Printf("HexToInt('0x10'): %d\n", num2)
	fmt.Printf("IntToHex(255): %s\n", hexutils.IntToHex(255))
	fmt.Printf("IntToHexPadded(255, 4): %s\n\n", hexutils.IntToHexPadded(255, 4))

	// Example 10: XOR operations
	fmt.Println("--- XOR Operations ---")
	xorResult, _ := hexutils.XorHex("aabbcc", "112233")
	fmt.Printf("aa XOR 11 = %s\n", xorResult)
	xorSelf, _ := hexutils.XorHex("abcdef", "abcdef")
	fmt.Printf("aa XOR aa (should be 00): %s\n\n", xorSelf)

	// Example 11: Reverse hex
	fmt.Println("--- Reverse Hex ---")
	reversed, _ := hexutils.ReverseHex("12345678")
	fmt.Printf("Original: 12345678\n")
	fmt.Printf("Reversed: %s\n\n", reversed)

	// Example 12: HexReader (streaming)
	fmt.Println("--- HexReader (Streaming) ---")
	reader, _ := hexutils.NewHexReader("48656c6c6f")
	buf := make([]byte, 3)
	n, _ := reader.Read(buf)
	fmt.Printf("Read %d bytes: %s\n", n, buf[:n])
	n, _ = reader.Read(buf)
	fmt.Printf("Read %d bytes: %s\n", n, buf[:n])
	fmt.Printf("Remaining bytes: %d\n", reader.Len())
	reader.Reset()
	fmt.Printf("After reset, remaining bytes: %d\n", reader.Len())
}