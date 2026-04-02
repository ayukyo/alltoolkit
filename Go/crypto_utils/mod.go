// Package crypto_utils provides cryptographic utility functions for Go.
// All functions use only the Go standard library and are production-ready.
//
// Features:
//   - Hash functions: MD5, SHA1, SHA256, SHA512
//   - HMAC: HMAC-SHA256
//   - Base64: Standard and URL-safe encoding/decoding
//   - Random: Secure random string and password generation
//   - UUID: Version 4 UUID generation
//   - XOR: Simple XOR encryption/decryption
//
// Example usage:
//
//	// Hash a string
//	hash := crypto_utils.Sha256Hash("hello world")
//
//	// Base64 encode/decode
//	encoded := crypto_utils.Base64Encode("hello")
//	decoded := crypto_utils.Base64Decode(encoded)
//
//	// Generate UUID
//	uuid := crypto_utils.GenerateUUID()
//
//	// Generate random password
//	password := crypto_utils.RandomPassword(16)
//
package crypto_utils

import (
	"crypto/hmac"
	"crypto/md5"
	"crypto/rand"
	"crypto/sha1"
	"crypto/sha256"
	"crypto/sha512"
	"encoding/base64"
	"encoding/hex"
	"fmt"
	"io"
	"math/big"
	"strings"
	"time"
)

// ============================================================================
// Hash Functions
// ============================================================================

// Md5Hash calculates the MD5 hash of a string and returns it as a lowercase hex string.
// Note: MD5 is cryptographically broken and should not be used for security purposes.
// Use SHA256 for security-sensitive applications.
func Md5Hash(input string) string {
	hash := md5.Sum([]byte(input))
	return hex.EncodeToString(hash[:])
}

// Sha1Hash calculates the SHA1 hash of a string and returns it as a lowercase hex string.
// Note: SHA1 is considered weak for collision resistance. Use SHA256 for new applications.
func Sha1Hash(input string) string {
	hash := sha1.Sum([]byte(input))
	return hex.EncodeToString(hash[:])
}

// Sha256Hash calculates the SHA256 hash of a string and returns it as a lowercase hex string.
func Sha256Hash(input string) string {
	hash := sha256.Sum256([]byte(input))
	return hex.EncodeToString(hash[:])
}

// Sha512Hash calculates the SHA512 hash of a string and returns it as a lowercase hex string.
func Sha512Hash(input string) string {
	hash := sha512.Sum512([]byte(input))
	return hex.EncodeToString(hash[:])
}

// Sha256HashBytes calculates the SHA256 hash of a byte slice.
func Sha256HashBytes(data []byte) []byte {
	hash := sha256.Sum256(data)
	return hash[:]
}

// ============================================================================
// HMAC Functions
// ============================================================================

// HmacSha256 calculates the HMAC-SHA256 of a message using the provided secret key.
func HmacSha256(message, secret string) string {
	mac := hmac.New(sha256.New, []byte(secret))
	mac.Write([]byte(message))
	return hex.EncodeToString(mac.Sum(nil))
}

// ============================================================================
// Base64 Functions
// ============================================================================

// Base64Encode encodes a string to Base64.
func Base64Encode(input string) string {
	return base64.StdEncoding.EncodeToString([]byte(input))
}

// Base64Decode decodes a Base64 string. Returns empty string if decoding fails.
func Base64Decode(input string) string {
	decoded, err := base64.StdEncoding.DecodeString(input)
	if err != nil {
		return ""
	}
	return string(decoded)
}

// Base64UrlEncode encodes a string to URL-safe Base64 (RFC 4648).
// Replaces '+' with '-', '/' with '_', and removes padding '='.
func Base64UrlEncode(input string) string {
	encoded := base64.URLEncoding.EncodeToString([]byte(input))
	return strings.TrimRight(encoded, "=")
}

// Base64UrlDecode decodes a URL-safe Base64 string.
// Handles both padded and unpadded input.
func Base64UrlDecode(input string) string {
	padding := 4 - len(input)%4
	if padding != 4 {
		input += strings.Repeat("=", padding)
	}
	decoded, err := base64.URLEncoding.DecodeString(input)
	if err != nil {
		return ""
	}
	return string(decoded)
}

// IsValidBase64 checks if a string is valid Base64.
func IsValidBase64(input string) bool {
	_, err := base64.StdEncoding.DecodeString(input)
	return err == nil
}

// ============================================================================
// Random Functions
// ============================================================================

const (
	LowerCaseLetters = "abcdefghijklmnopqrstuvwxyz"
	UpperCaseLetters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	Digits           = "0123456789"
	SpecialChars     = "!@#$%^&*()-_=+[]{}|;:,.<>?"
	Alphanumeric     = LowerCaseLetters + UpperCaseLetters + Digits
	AllChars         = Alphanumeric + SpecialChars
)

// RandomString generates a cryptographically secure random string of the specified length.
// Uses the given character set or defaults to alphanumeric.
func RandomString(length int, chars string) string {
	if length <= 0 {
		return ""
	}
	if chars == "" {
		chars = Alphanumeric
	}

	result := make([]byte, length)
	charLen := big.NewInt(int64(len(chars)))

	for i := 0; i < length; i++ {
		randomIndex, err := rand.Int(rand.Reader, charLen)
		if err != nil {
			// Fallback to time-based seed if crypto/rand fails
			result[i] = chars[time.Now().UnixNano()%int64(len(chars))]
			continue
		}
		result[i] = chars[randomIndex.Int64()]
	}

	return string(result)
}

// RandomPassword generates a secure random password with mixed character types.
// Ensures at least one lowercase, one uppercase, one digit, and one special character.
func RandomPassword(length int) string {
	if length < 4 {
		length = 4
	}

	// Ensure we have at least one of each character type
	password := []byte{
		RandomString(1, LowerCaseLetters)[0],
		RandomString(1, UpperCaseLetters)[0],
		RandomString(1, Digits)[0],
		RandomString(1, SpecialChars)[0],
	}

	// Fill the rest with random characters from all sets
	if length > 4 {
		password = append(password, RandomString(length-4, AllChars)...)
	}

	// Shuffle the password
	for i := len(password) - 1; i > 0; i-- {
		randomIndex, _ := rand.Int(rand.Reader, big.NewInt(int64(i+1)))
		j := randomIndex.Int64()
		password[i], password[j] = password[j], password[i]
	}

	return string(password)
}

// ============================================================================
// UUID Functions
// ============================================================================

// GenerateUUID generates a version 4 UUID (random UUID) as a string.
// Format: xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx where y is 8, 9, a, or b.
func GenerateUUID() string {
	uuid := make([]byte, 16)
	_, err := io.ReadFull(rand.Reader, uuid)
	if err != nil {
		// Fallback to time-based generation
		return generateTimeBasedUUID()
	}

	// Set version (4) and variant (RFC 4122)
	uuid[6] = (uuid[6] & 0x0f) | 0x40 // Version 4
	uuid[8] = (uuid[8] & 0x3f) | 0x80 // Variant RFC 4122

	return fmt.Sprintf("%08x-%04x-%04x-%04x-%012x",
		uuid[0:4],
		uuid[4:6],
		uuid[6:8],
		uuid[8:10],
		uuid[10:16])
}

// GenerateUUIDSimple generates a UUID without hyphens (32 characters).
func GenerateUUIDSimple() string {
	uuid := GenerateUUID()
	return strings.ReplaceAll(uuid, "-", "")
}

// generateTimeBasedUUID generates a UUID using time as a fallback.
func generateTimeBasedUUID() string {
	timestamp := time.Now().UnixNano()
	return fmt.Sprintf("%08x-%04x-4%03x-8%03x-%012x",
		timestamp>>32,
		(timestamp>>16)&0xffff,
		timestamp&0xfff,
		timestamp&0xfff,
		timestamp)
}

// IsValidUUID checks if a string is a valid UUID format.
func IsValidUUID(uuid string) bool {
	if len(uuid) != 36 {
		return false
	}
	// Check format: 8-4-4-4-12
	for i, c := range uuid {
		if i == 8 || i == 13 || i == 18 || i == 23 {
			if c != '-' {
				return false
			}
		} else {
			if !((c >= '0' && c <= '9') || (c >= 'a' && c <= 'f') || (c >= 'A' && c <= 'F')) {
				return false
			}
		}
	}
	return true
}

// ============================================================================
// XOR Encryption Functions
// ============================================================================

// XorEncrypt encrypts a string using XOR with the provided key.
// Returns the encrypted data as Base64 string.
//
// Note: XOR encryption is NOT secure for sensitive data. It's provided for
// simple obfuscation only. Use proper encryption for security-sensitive data.
func XorEncrypt(input, key string) string {
	if key == "" {
		return Base64Encode(input)
	}
	encrypted := make([]byte, len(input))
	keyBytes := []byte(key)
	for i, c := range []byte(input) {
		encrypted[i] = c ^ keyBytes[i%len(keyBytes)]
	}
	return Base64Encode(string(encrypted))
}

// XorDecrypt decrypts a Base64 string that was encrypted with XorEncrypt.
func XorDecrypt(encrypted, key string) string {
	if key == "" {
		return Base64Decode(encrypted)
	}
	data := Base64Decode(encrypted)
	if data == "" {
		return ""
	}
	decrypted := make([]byte, len(data))
	keyBytes := []byte(key)
	for i, c := range []byte(data) {
		decrypted[i] = c ^ keyBytes[i%len(keyBytes)]
	}
	return string(decrypted)
}

// ============================================================================
// Validation Functions
// ============================================================================

// IsValidHash checks if a string is a valid hex hash of the specified algorithm.
// Supported algorithms: "md5", "sha1", "sha256", "sha512"
func IsValidHash(hash, algorithm string) bool {
	var expectedLen int
	switch strings.ToLower(algorithm) {
	case "md5":
		expectedLen = 32
	case "sha1":
		expectedLen = 40
	case "sha256":
		expectedLen = 64
	case "sha512":
		expectedLen = 128
	default:
		return false
	}

	if len(hash) != expectedLen {
		return false
	}

	for _, c := range hash {
		if !((c >= '0' && c <= '9') || (c >= 'a' && c <= 'f') || (c >= 'A' && c <= 'F')) {
			return false
		}
	}
	return true
}

// IsValidMd5 checks if a string is a valid MD5 hash format.
func IsValidMd5(hash string) bool {
	return IsValidHash(hash, "md5")
}

// IsValidSha1 checks if a string is a valid SHA1 hash format.
func IsValidSha1(hash string) bool {
	return IsValidHash(hash, "sha1")
}

// IsValidSha256 checks if a string is a valid SHA256 hash format.
func IsValidSha256(hash string) bool {
	return IsValidHash(hash, "sha256")
}

// IsValidSha512 checks if a string is a valid SHA512 hash format.
func IsValidSha512(hash string) bool {
	return IsValidHash(hash, "sha512")
}