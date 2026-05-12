package main

import (
	"fmt"
	"math/big"

	base58_utils "github.com/ayukyo/alltoolkit/Go/base58_utils"
)

func main() {
	fmt.Println("=== Base58 Utils Examples ===")
	fmt.Println()

	// Example 1: Basic encoding and decoding
	fmt.Println("1. Basic Encoding/Decoding:")
	{
		text := "Hello, World!"
		encoded := base58_utils.EncodeString(text)
		fmt.Printf("   Original: %s\n", text)
		fmt.Printf("   Encoded:  %s\n", encoded)

		decoded, _ := base58_utils.DecodeString(encoded)
		fmt.Printf("   Decoded:  %s\n", decoded)
	}
	fmt.Println()

	// Example 3: Different alphabets
	fmt.Println("3. Different Alphabets:")
	{
		text := "Test Data"
		bitcoin := base58_utils.EncodeString(text)
		flickr := base58_utils.EncodeStringWithAlphabet(text, base58_utils.FlickrAlphabet)
		ripple := base58_utils.EncodeStringWithAlphabet(text, base58_utils.RippleAlphabet)

		fmt.Printf("   Original:        %s\n", text)
		fmt.Printf("   Bitcoin alphabet: %s\n", bitcoin)
		fmt.Printf("   Flickr alphabet:  %s\n", flickr)
		fmt.Printf("   Ripple alphabet:  %s\n", ripple)
	}
	fmt.Println()

	// Example 4: Leading zeros handling
	fmt.Println("4. Leading Zeros (0x00 bytes):")
	{
		data := []byte{0x00, 0x00, 0x01, 0x02, 0x03}
		encoded := base58_utils.Encode(data)
		fmt.Printf("   Data:    [0x00, 0x00, 0x01, 0x02, 0x03]\n")
		fmt.Printf("   Encoded: %s\n", encoded)
		fmt.Printf("   Note: '1' represents leading zero bytes\n")

		// Trim leading zeros
		trimmed := base58_utils.TrimLeadingZeros(encoded)
		fmt.Printf("   Trimmed: %s\n", trimmed)
		fmt.Printf("   Count:   %d leading '1's\n", base58_utils.CountLeadingZeros(encoded))
	}
	fmt.Println()

	// Example 5: Integer encoding
	fmt.Println("5. Integer Encoding:")
	{
		numbers := []*big.Int{
			big.NewInt(0),
			big.NewInt(12345),
			big.NewInt(999999999),
			func() *big.Int { n, _ := new(big.Int).SetString("123456789012345678901234567890", 10); return n }(),
		}

		for _, n := range numbers {
			encoded := base58_utils.EncodeInt(n)
			decoded, _ := base58_utils.DecodeInt(encoded)
			fmt.Printf("   Number: %s -> Base58: %s -> Decoded: %s\n", n.String(), encoded, decoded.String())
		}
	}
	fmt.Println()

	// Example 6: Validation
	fmt.Println("6. Validation:")
	{
		testStrings := []string{
			"2NEpo7TZRRrL6Si7Hqy7jcQ", // Valid
			"9Ajdvzr",                  // Valid
			"invalid0",                 // Invalid (contains '0')
			"invalidO",                 // Invalid (contains 'O')
			"invalidI",                 // Invalid (contains 'I')
			"invalidl",                 // Invalid (contains lowercase 'l')
		}

		fmt.Println("   Base58 excludes: 0, O, I, l (ambiguous characters)")
		for _, s := range testStrings {
			valid := base58_utils.IsValid(s)
			fmt.Printf("   '%s' -> Valid: %v\n", s, valid)
		}
	}
	fmt.Println()

	// Example 7: Hex encoding
	fmt.Println("7. Hex String Encoding:")
	{
		hex := "deadbeef"
		encoded, _ := base58_utils.EncodeHex(hex)
		decoded, _ := base58_utils.DecodeHex(encoded)

		fmt.Printf("   Hex:     %s\n", hex)
		fmt.Printf("   Base58:  %s\n", encoded)
		fmt.Printf("   Decoded: %s\n", decoded)
	}
	fmt.Println()

	// Example 8: Alphabet conversion
	fmt.Println("8. Alphabet Conversion:")
	{
		text := "Hello"
		bitcoinEncoded := base58_utils.EncodeString(text)

		// Convert from Bitcoin to Flickr alphabet
		flickrEncoded, _ := base58_utils.ConvertAlphabet(bitcoinEncoded, base58_utils.BitcoinAlphabet, base58_utils.FlickrAlphabet)

		fmt.Printf("   Original:          %s\n", text)
		fmt.Printf("   Bitcoin encoded:   %s\n", bitcoinEncoded)
		fmt.Printf("   Flickr converted:  %s\n", flickrEncoded)

		// Decode with Flickr alphabet
		decoded, _ := base58_utils.DecodeStringWithAlphabet(flickrEncoded, base58_utils.FlickrAlphabet)
		fmt.Printf("   Decoded (Flickr):  %s\n", decoded)
	}
	fmt.Println()

	// Example 9: Size estimation
	fmt.Println("9. Size Estimation:")
	{
		data := []byte("This is a test string for size estimation")
		encoded := base58_utils.Encode(data)

		estimatedEncoded := base58_utils.Size(len(data))
		estimatedDecoded := base58_utils.DecodeSize(len(encoded))

		fmt.Printf("   Input size:         %d bytes\n", len(data))
		fmt.Printf("   Estimated encoded:  %d chars\n", estimatedEncoded)
		fmt.Printf("   Actual encoded:     %d chars\n", len(encoded))
		fmt.Printf("   Estimated decoded:  %d bytes\n", estimatedDecoded)
		fmt.Printf("   Actual decoded:     %d bytes\n", len(data))
	}
	fmt.Println()

	// Example 10: Binary data
	fmt.Println("10. Binary Data:")
	{
		binary := []byte{0xFF, 0xFE, 0xFD, 0xFC, 0xFB, 0xFA}
		encoded := base58_utils.Encode(binary)
		decoded, _ := base58_utils.Decode(encoded)

		fmt.Printf("   Binary:   %v\n", binary)
		fmt.Printf("   Encoded:  %s\n", encoded)
		fmt.Printf("   Decoded:  %v\n", decoded)
		fmt.Printf("   Match:    %v\n", string(binary) == string(decoded))
	}
	fmt.Println()

	// Example 11: Checksum verification failure
	fmt.Println("11. Checksum Verification Failure:")
	{
		data := []byte("Important data")
		encoded := base58_utils.EncodeCheck(data)
		fmt.Printf("   Original encoded: %s\n", encoded)

		// Corrupt the encoded string
		if len(encoded) > 0 {
			corrupted := encoded[:len(encoded)-1] + "X" // Change last character
			fmt.Printf("   Corrupted:        %s\n", corrupted)

			_, err := base58_utils.DecodeCheck(corrupted)
			if err != nil {
				fmt.Printf("   Result:           %v (checksum invalid)\n", err)
			}
		}
	}
	fmt.Println()

	// Example 12: All alphabet characters
	fmt.Println("12. Alphabet Characters:")
	{
		fmt.Println("   Bitcoin alphabet (58 chars):")
		fmt.Println("   123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz")
		fmt.Println("   Note: No 0, O, I, or l - all visually ambiguous characters removed")
	}
	fmt.Println()

	fmt.Println("=== All examples completed! ===")
}