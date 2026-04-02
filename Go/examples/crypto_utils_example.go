// Example program demonstrating crypto_utils functionality
// Run with: go run crypto_utils_example.go

package main

import (
	"fmt"
	"github.com/ayukyo/alltoolkit/Go/crypto_utils"
)

func main() {
	fmt.Println("========================================")
	fmt.Println("AllToolkit - Go Crypto Utils Examples")
	fmt.Println("========================================\n")

	// ============================================================================
	// Hash Functions
	// ============================================================================
	fmt.Println("--- Hash Functions ---")

	input := "hello world"
	fmt.Printf("Input: %q\n\n", input)

	fmt.Printf("MD5:    %s\n", crypto_utils.Md5Hash(input))
	fmt.Printf("SHA1:   %s\n", crypto_utils.Sha1Hash(input))
	fmt.Printf("SHA256: %s\n", crypto_utils.Sha256Hash(input))
	fmt.Printf("SHA512: %s\n", crypto_utils.Sha512Hash(input))

	// Verify hash lengths
	fmt.Printf("\nHash lengths:\n")
	fmt.Printf("  MD5:    %d chars (expected: 32)\n", len(crypto_utils.Md5Hash(input)))
	fmt.Printf("  SHA1:   %d chars (expected: 40)\n", len(crypto_utils.Sha1Hash(input)))
	fmt.Printf("  SHA256: %d chars (expected: 64)\n", len(crypto_utils.Sha256Hash(input)))
	fmt.Printf("  SHA512: %d chars (expected: 128)\n", len(crypto_utils.Sha512Hash(input)))

	// ============================================================================
	// HMAC
	// ============================================================================
	fmt.Println("\n--- HMAC-SHA256 ---")

	message := "hello"
	secret := "my_secret_key"
	hmac := crypto_utils.HmacSha256(message, secret)
	fmt.Printf("Message: %q\n", message)
	fmt.Printf("Secret:  %q\n", secret)
	fmt.Printf("HMAC:    %s\n", hmac)

	// ============================================================================
	// Base64 Encoding/Decoding
	// ============================================================================
	fmt.Println("\n--- Base64 Encoding/Decoding ---")

	text := "Hello, World! 你好世界"
	encoded := crypto_utils.Base64Encode(text)
	decoded := crypto_utils.Base64Decode(encoded)

	fmt.Printf("Original: %q\n", text)
	fmt.Printf("Encoded:  %s\n", encoded)
	fmt.Printf("Decoded:  %q\n", decoded)
	fmt.Printf("Match:    %v\n", text == decoded)

	// URL-safe Base64
	urlText := "hello+world/test"
	urlEncoded := crypto_utils.Base64UrlEncode(urlText)
	urlDecoded := crypto_utils.Base64UrlDecode(urlEncoded)
	fmt.Printf("\nURL-safe Base64:\n")
	fmt.Printf("  Original: %q\n", urlText)
	fmt.Printf("  Encoded:  %s\n", urlEncoded)
	fmt.Printf("  Decoded:  %q\n", urlDecoded)

	// Validation
	fmt.Printf("\nValidation:\n")
	fmt.Printf("  Is valid Base64: %v\n", crypto_utils.IsValidBase64(encoded))
	fmt.Printf("  Is valid Base64: %v\n", crypto_utils.IsValidBase64("not-valid!!!"))

	// ============================================================================
	// Random String Generation
	// ============================================================================
	fmt.Println("\n--- Random String Generation ---")

	fmt.Printf("Random string (8 chars):  %s\n", crypto_utils.RandomString(8, ""))
	fmt.Printf("Random string (16 chars): %s\n", crypto_utils.RandomString(16, ""))
	fmt.Printf("Random string (32 chars): %s\n", crypto_utils.RandomString(32, ""))

	// Custom charset
	custom := crypto_utils.RandomString(10, "ABCDEF")
	fmt.Printf("Custom charset (A-F only): %s\n", custom)

	// ============================================================================
	// Password Generation
	// ============================================================================
	fmt.Println("\n--- Password Generation ---")

	for i := 0; i < 5; i++ {
		password := crypto_utils.RandomPassword(16)
		fmt.Printf("Password %d: %s\n", i+1, password)
	}

	// ============================================================================
	// UUID Generation
	// ============================================================================
	fmt.Println("\n--- UUID Generation ---")

	for i := 0; i < 3; i++ {
		uuid := crypto_utils.GenerateUUID()
		fmt.Printf("UUID %d: %s (valid: %v)\n", i+1, uuid, crypto_utils.IsValidUUID(uuid))
	}

	fmt.Println("\nSimple UUIDs (no hyphens):")
	for i := 0; i < 3; i++ {
		uuid := crypto_utils.GenerateUUIDSimple()
		fmt.Printf("  %s\n", uuid)
	}

	// ============================================================================
	// XOR Encryption
	// ============================================================================
	fmt.Println("\n--- XOR Encryption ---")

	secretMessage := "This is a secret message!"
	key := "my_key"

	encrypted := crypto_utils.XorEncrypt(secretMessage, key)
	decrypted := crypto_utils.XorDecrypt(encrypted, key)

	fmt.Printf("Original:  %q\n", secretMessage)
	fmt.Printf("Key:       %q\n", key)
	fmt.Printf("Encrypted: %s\n", encrypted)
	fmt.Printf("Decrypted: %q\n", decrypted)
	fmt.Printf("Match:     %v\n", secretMessage == decrypted)

	// ============================================================================
	// Hash Validation
	// ============================================================================
	fmt.Println("\n--- Hash Validation ---")

	validMd5 := "5d41402abc4b2a76b9719d911017c592"
	invalidMd5 := "not-a-hash"

	fmt.Printf("MD5 hash %q is valid: %v\n", validMd5, crypto_utils.IsValidMd5(validMd5))
	fmt.Printf("MD5 hash %q is valid: %v\n", invalidMd5, crypto_utils.IsValidMd5(invalidMd5))

	validSha256 := "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
	fmt.Printf("SHA256 hash %q is valid: %v\n", validSha256, crypto_utils.IsValidSha256(validSha256))

	// ============================================================================
	// Constants
	// ============================================================================
	fmt.Println("\n--- Character Sets ---")

	fmt.Printf("Lowercase: %s\n", crypto_utils.LowerCaseLetters)
	fmt.Printf("Uppercase: %s\n", crypto_utils.UpperCaseLetters)
	fmt.Printf("Digits:    %s\n", crypto_utils.Digits)
	fmt.Printf("Special:   %s\n", crypto_utils.SpecialChars)
	fmt.Printf("All:       %s\n", crypto_utils.AllChars)

	fmt.Println("\n========================================")
	fmt.Println("Examples completed successfully!")
	fmt.Println("========================================")
}
