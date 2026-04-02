package crypto_utils

import (
	"strings"
	"testing"
)

// ============================================================================
// Hash Function Tests
// ============================================================================

func TestMd5Hash(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"hello", "5d41402abc4b2a76b9719d911017c592"},
		{"", "d41d8cd98f00b204e9800998ecf8427e"},
		{"Hello, World!", "65a8e27d8879283831b664bd8b7f0ad4"},
		{"中文测试", "a7fc8e26e9be5b1b1c42f5a1c48c25d1"},
	}

	for _, test := range tests {
		result := Md5Hash(test.input)
		if result != test.expected {
			t.Errorf("Md5Hash(%q) = %q, expected %q", test.input, result, test.expected)
		}
	}
}

func TestSha1Hash(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"hello", "aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d"},
		{"", "da39a3ee5e6b4b0d3255bfef95601890afd80709"},
		{"Hello, World!", "0a0a9f2a6772942557ab5355d76af442f8f65e01"},
	}

	for _, test := range tests {
		result := Sha1Hash(test.input)
		if result != test.expected {
			t.Errorf("Sha1Hash(%q) = %q, expected %q", test.input, result, test.expected)
		}
	}
}

func TestSha256Hash(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"hello", "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"},
		{"", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"},
	}

	for _, test := range tests {
		result := Sha256Hash(test.input)
		if result != test.expected {
			t.Errorf("Sha256Hash(%q) = %q, expected %q", test.input, result, test.expected)
		}
	}
}

func TestSha512Hash(t *testing.T) {
	result := Sha512Hash("hello")
	if len(result) != 128 {
		t.Errorf("Sha512Hash length = %d, expected 128", len(result))
	}
}

func TestSha256HashBytes(t *testing.T) {
	data := []byte("hello")
	hash := Sha256HashBytes(data)
	if len(hash) != 32 {
		t.Errorf("Sha256HashBytes length = %d, expected 32", len(hash))
	}
}

// ============================================================================
// HMAC Function Tests
// ============================================================================

func TestHmacSha256(t *testing.T) {
	result := HmacSha256("hello", "secret")
	if len(result) != 64 {
		t.Errorf("HmacSha256 length = %d, expected 64", len(result))
	}

	// Same input should produce same output
	result2 := HmacSha256("hello", "secret")
	if result != result2 {
		t.Error("HmacSha256 should produce consistent results")
	}

	// Different key should produce different output
	result3 := HmacSha256("hello", "different")
	if result == result3 {
		t.Error("HmacSha256 with different keys should produce different results")
	}
}

// ============================================================================
// Base64 Function Tests
// ============================================================================

func TestBase64Encode(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"hello", "aGVsbG8="},
		{"", ""},
		{"Hello, World!", "SGVsbG8sIFdvcmxkIQ=="},
	}

	for _, test := range tests {
		result := Base64Encode(test.input)
		if result != test.expected {
			t.Errorf("Base64Encode(%q) = %q, expected %q", test.input, result, test.expected)
		}
	}
}

func TestBase64Decode(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"aGVsbG8=", "hello"},
		{"", ""},
		{"SGVsbG8sIFdvcmxkIQ==", "Hello, World!"},
	}

	for _, test := range tests {
		result := Base64Decode(test.input)
		if result != test.expected {
			t.Errorf("Base64Decode(%q) = %q, expected %q", test.input, result, test.expected)
		}
	}
}

func TestBase64RoundTrip(t *testing.T) {
	tests := []string{
		"hello",
		"Hello, World!",
		"中文测试",
		"Special chars: !@#$%",
		"",
	}

	for _, test := range tests {
		encoded := Base64Encode(test)
		decoded := Base64Decode(encoded)
		if decoded != test {
			t.Errorf("Base64 round-trip failed for %q: got %q", test, decoded)
		}
	}
}

func TestBase64UrlEncode(t *testing.T) {
	// Test that URL-safe encoding doesn't contain + or /
	input := "hello+world/test"
	encoded := Base64UrlEncode(input)
	if strings.Contains(encoded, "+") || strings.Contains(encoded, "/") {
		t.Error("Base64UrlEncode should not contain + or /")
	}
	if strings.Contains(encoded, "=") {
		t.Error("Base64UrlEncode should not contain padding =")
	}
}

func TestBase64UrlRoundTrip(t *testing.T) {
	tests := []string{
		"hello+world/test",
		"special>chars<here",
		"path/to/file.txt",
	}

	for _, test := range tests {
		encoded := Base64UrlEncode(test)
		decoded := Base64UrlDecode(encoded)
		if decoded != test {
			t.Errorf("Base64Url round-trip failed for %q: got %q", test, decoded)
		}
	}
}

func TestIsValidBase64(t *testing.T) {
	valid := []string{
		"aGVsbG8=",
		"SGVsbG8sIFdvcmxkIQ==",
		"",
	}
	invalid := []string{
		"not-valid!!!",
		"aGVsbG8",
	}

	for _, test := range valid {
		if !IsValidBase64(test) {
			t.Errorf("IsValidBase64(%q) should be true", test)
		}
	}

	for _, test := range invalid {
		if IsValidBase64(test) {
			t.Errorf("IsValidBase64(%q) should be false", test)
		}
	}
}

// ============================================================================
// Random Function Tests
// ============================================================================

func TestRandomString(t *testing.T) {
	// Test length
	for _, length := range []int{1, 8, 16, 32, 100} {
		result := RandomString(length, "")
		if len(result) != length {
			t.Errorf("RandomString(%d) length = %d, expected %d", length, len(result), length)
		}
	}

	// Test zero length
	result := RandomString(0, "")
	if result != "" {
		t.Error("RandomString(0) should return empty string")
	}

	// Test negative length
	result = RandomString(-1, "")
	if result != "" {
		t.Error("RandomString(-1) should return empty string")
	}

	// Test custom charset
	custom := "ABC"
	result = RandomString(10, custom)
	for _, c := range result {
		if c != 'A' && c != 'B' && c != 'C' {
			t.Error("RandomString with custom charset should only use provided characters")
		}
	}
}

func TestRandomStringUniqueness(t *testing.T) {
	// Generate multiple strings and check they're different
	seen := make(map[string]bool)
	for i := 0; i < 100; i++ {
		s := RandomString(16, "")
		if seen[s] {
			t.Error("RandomString should produce unique values")
			break
		}
		seen[s] = true
	}
}

func TestRandomPassword(t *testing.T) {
	// Test minimum length
	password := RandomPassword(2)
	if len(password) != 4 {
		t.Errorf("RandomPassword(2) length = %d, expected 4 (minimum)", len(password))
	}

	// Test specified length
	password = RandomPassword(16)
	if len(password) != 16 {
		t.Errorf("RandomPassword(16) length = %d, expected 16", len(password))
	}

	// Test character variety
	hasLower := false
	hasUpper := false
	hasDigit := false
	hasSpecial := false

	for _, c := range password {
		if c >= 'a' && c <= 'z' {
			hasLower = true
		} else if c >= 'A' && c <= 'Z' {
			hasUpper = true
		} else if c >= '0' && c <= '9' {
			hasDigit = true
		} else {
			hasSpecial = true
		}
	}

	if !hasLower {
		t.Error("RandomPassword should contain at least one lowercase letter")
	}
	if !hasUpper {
		t.Error("RandomPassword should contain at least one uppercase letter")
	}
	if !hasDigit {
		t.Error("RandomPassword should contain at least one digit")
	}
	if !hasSpecial {
		t.Error("RandomPassword should contain at least one special character")
	}
}

// ============================================================================
// UUID Function Tests
// ============================================================================

func TestGenerateUUID(t *testing.T) {
	uuid := GenerateUUID()

	// Check length
	if len(uuid) != 36 {
		t.Errorf("GenerateUUID length = %d, expected 36", len(uuid))
	}

	// Check format (8-4-4-4-12)
	if uuid[8] != '-' || uuid[13] != '-' || uuid[18] != '-' || uuid[23] != '-' {
		t.Error("GenerateUUID should have correct format with hyphens at positions 8, 13, 18, 23")
	}

	// Check version (4th segment should start with '4')
	if uuid[14] != '4' {
		t.Errorf("GenerateUUID version should be 4, got %c", uuid[14])
	}

	// Check variant (3rd segment should start with 8, 9, a, or b)
	variant := uuid[19]
	if variant != '8' && variant != '9' && variant != 'a' && variant != 'b' {
		t.Errorf("GenerateUUID variant should be 8, 9, a, or b, got %c", variant)
	}
}

func TestGenerateUUIDUniqueness(t *testing.T) {
	seen := make(map[string]bool)
	for i := 0; i < 100; i++ {
		uuid := GenerateUUID()
		if seen[uuid] {
			t.Error("GenerateUUID should produce unique values")
			break
		}
		seen[uuid] = true
	}
}

func TestGenerateUUIDSimple(t *testing.T) {
	uuid := GenerateUUIDSimple()

	// Check length (no hyphens)
	if len(uuid) != 32 {
		t.Errorf("GenerateUUIDSimple length = %d, expected 32", len(uuid))
	}

	// Check no hyphens
	if strings.Contains(uuid, "-") {
		t.Error("GenerateUUIDSimple should not contain hyphens")
	}
}

func TestIsValidUUID(t *testing.T) {
	validUUIDs := []string{
		"550e8400-e29b-41d4-a716-446655440000",
		"6ba7b810-9dad-11d1-80b4-00c04fd430c8",
		"00000000-0000-4000-8000-000000000000",
	}

	invalidUUIDs := []string{
		"not-a-uuid",
		"550e8400-e29b-11d4-a716-44665544000", // Too short
		"550e8400-e29b-11d4-a716-4466554400000", // Too long
		"550e8400_e29b_11d4_a716_446655440000", // Wrong separators
		"550e8400-e29b-11d4-g716-446655440000", // Invalid character 'g'
	}

	for _, uuid := range validUUIDs {
		if !IsValidUUID(uuid) {
			t.Errorf("IsValidUUID(%q) should be true", uuid)
		}
	}

	for _, uuid := range invalidUUIDs {
		if IsValidUUID(uuid) {
			t.Errorf("IsValidUUID(%q) should be false", uuid)
		}
	}
}

// ============================================================================
// XOR Function Tests
// ============================================================================

func TestXorEncryptDecrypt(t *testing.T) {
	tests := []struct {
		input string
		key   string
	}{
		{"hello", "secret"},
		{"Hello, World!", "mykey"},
		{"中文测试", "key"},
		{"", "key"},
		{"test", ""},
	}

	for _, test := range tests {
		encrypted := XorEncrypt(test.input, test.key)
		decrypted := XorDecrypt(encrypted, test.key)
		if decrypted != test.input {
			t.Errorf("XOR round-trip failed for %q with key %q: got %q", test.input, test.key, decrypted)
		}
	}
}

func TestXorDifferentKeys(t *testing.T) {
	input := "hello"
	key1 := "secret"
	key2 := "different"

	encrypted1 := XorEncrypt(input, key1)
	encrypted2 := XorEncrypt(input, key2)

	if encrypted1 == encrypted2 {
		t.Error("XOR encryption with different keys should produce different results")
	}
}

// ============================================================================
// Validation Function Tests
// ============================================================================

func TestIsValidHash(t *testing.T) {
	tests := []struct {
		hash      string
		algorithm string
		expected  bool
	}{
		{"5d41402abc4b2a76b9719d911017c592", "md5", true},
		{"5d41402abc4b2a76b9719d911017c59", "md5", false}, // Too short
		{"5d41402abc4b2a76b9719d911017c59g", "md5", false}, // Invalid char
		{"aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d", "sha1", true},
		{"2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824", "sha256", true},
		{"invalid", "sha256", false},
		{"valid", "unknown", false},
	}

	for _, test := range tests {
		result := IsValidHash(test.hash, test.algorithm)
		if result != test.expected {
			t.Errorf("IsValidHash(%q, %q) = %v, expected %v", test.hash, test.algorithm, result, test.expected)
		}
	}
}

func TestIsValidMd5(t *testing.T) {
	if !IsValidMd5("5d41402abc4b2a76b9719d911017c592") {
		t.Error("IsValidMd5 should return true for valid MD5")
	}
	if IsValidMd5("invalid") {
		t.Error("IsValidMd5 should return false for invalid MD5")
	}
}

func TestIsValidSha256(t *testing.T) {
	if !IsValidSha256("2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824") {
		t.Error("IsValidSha256 should return true for valid SHA256")
	}
	if IsValidSha256("invalid") {
		t.Error("IsValidSha256 should return false for invalid SHA256")
	}
}

// ============================================================================
// Constant Tests
// ============================================================================

func TestConstants(t *testing.T) {
	if len(LowerCaseLetters) != 26 {
		t.Error("LowerCaseLetters should have 26 characters")
	}
	if len(UpperCaseLetters) != 26 {
		t.Error("UpperCaseLetters should have 26 characters")
	}
	if len(Digits) != 10 {
		t.Error("Digits should have 10 characters")
	}
	if len(Alphanumeric) != 62 {
		t.Error("Alphanumeric should have 62 characters")
	}
}