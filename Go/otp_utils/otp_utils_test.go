package otp_utils

import (
	"strings"
	"testing"
	"time"
)

// TestGenerateSecret tests secret generation
func TestGenerateSecret(t *testing.T) {
	// Test default length
	secret, err := GenerateSecret(20)
	if err != nil {
		t.Fatalf("GenerateSecret failed: %v", err)
	}
	if secret == "" {
		t.Fatal("Secret should not be empty")
	}
	if len(secret) < 26 { // Base32 encoding of 20 bytes should be ~32 chars
		t.Errorf("Secret too short: %s", secret)
	}

	// Test custom length
	secret2, err := GenerateSecret(32)
	if err != nil {
		t.Fatalf("GenerateSecret(32) failed: %v", err)
	}
	if len(secret2) < len(secret) {
		t.Errorf("Longer secret should be longer")
	}

	// Test uniqueness
	secret3, _ := GenerateSecret(20)
	if secret == secret3 {
		t.Error("Secrets should be unique")
	}
}

func TestGenerateSecretWithConfig(t *testing.T) {
	secret, err := GenerateSecretWithConfig()
	if err != nil {
		t.Fatalf("GenerateSecretWithConfig failed: %v", err)
	}
	if secret == "" {
		t.Fatal("Secret should not be empty")
	}
}

// TestValidateSecret tests secret validation
func TestValidateSecret(t *testing.T) {
	// Valid secret
	validSecret := "JBSWY3DPEHPK3PXP"
	if err := ValidateSecret(validSecret); err != nil {
		t.Errorf("Valid secret should pass: %v", err)
	}

	// Empty secret
	if err := ValidateSecret(""); err == nil {
		t.Error("Empty secret should fail")
	}

	// Invalid secret
	if err := ValidateSecret("INVALID!@#$"); err == nil {
		t.Error("Invalid secret should fail")
	}
}

// TestNormalizeSecret tests secret normalization
func TestNormalizeSecret(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"abcd efgh", "ABCDEFGH"},
		{"abcd efgh ijkl", "ABCDEFGHIJKL"},
		{"ABCD EFGH", "ABCDEFGH"},
		{"abcd", "ABCD"},
	}

	for _, tt := range tests {
		result := NormalizeSecret(tt.input)
		if result != tt.expected {
			t.Errorf("NormalizeSecret(%q) = %q, want %q", tt.input, result, tt.expected)
		}
	}
}

// TestGenerateTOTP tests TOTP generation
func TestGenerateTOTP(t *testing.T) {
	secret := "JBSWY3DPEHPK3PXP" // Base32 encoded "Hello!"

	// Generate code
	code, err := GenerateTOTP(secret, 6, 30)
	if err != nil {
		t.Fatalf("GenerateTOTP failed: %v", err)
	}

	if len(code) != 6 {
		t.Errorf("Code should be 6 digits, got %d", len(code))
	}

	// Verify it's all digits
	for _, c := range code {
		if c < '0' || c > '9' {
			t.Errorf("Code should only contain digits, got %c", c)
		}
	}
}

// TestGenerateTOTPAtTime tests TOTP at specific time
func TestGenerateTOTPAtTime(t *testing.T) {
	secret := "JBSWY3DPEHPK3PXP"

	// Test with specific timestamp (Unix timestamp 0)
	t0 := time.Unix(0, 0)
	code1, err := GenerateTOTPAtTime(secret, 6, 30, t0)
	if err != nil {
		t.Fatalf("GenerateTOTPAtTime failed: %v", err)
	}

	// Test with timestamp 30 seconds later (should be same period)
	t30 := time.Unix(29, 0)
	code2, err := GenerateTOTPAtTime(secret, 6, 30, t30)
	if err != nil {
		t.Fatalf("GenerateTOTPAtTime failed: %v", err)
	}

	if code1 != code2 {
		t.Errorf("Same period should produce same code: %s vs %s", code1, code2)
	}

	// Test with timestamp in next period
	t60 := time.Unix(60, 0)
	code3, err := GenerateTOTPAtTime(secret, 6, 30, t60)
	if err != nil {
		t.Fatalf("GenerateTOTPAtTime failed: %v", err)
	}

	// Different periods should produce different codes (usually)
	if code1 == code3 {
		t.Log("Note: Codes happen to be the same (rare but possible)")
	}
}

// TestGenerateTOTPWithConfig tests TOTP with config
func TestGenerateTOTPWithConfig(t *testing.T) {
	secret, _ := GenerateSecret(20)
	config := &OTPConfig{
		Secret:    secret,
		Digits:    8,
		Algorithm: AlgorithmSHA256,
		Period:    30,
	}

	code, err := GenerateTOTPWithConfig(config)
	if err != nil {
		t.Fatalf("GenerateTOTPWithConfig failed: %v", err)
	}

	if len(code) != 8 {
		t.Errorf("Code should be 8 digits, got %d", len(code))
	}
}

// TestValidateTOTP tests TOTP validation
func TestValidateTOTP(t *testing.T) {
	secret := "JBSWY3DPEHPK3PXP"

	// Generate and validate
	code, _ := GenerateTOTP(secret, 6, 30)
	valid, err := ValidateTOTP(secret, code, 6, 30, 1)
	if err != nil {
		t.Fatalf("ValidateTOTP failed: %v", err)
	}

	if !valid {
		t.Error("Valid code should pass validation")
	}

	// Wrong code
	valid, _ = ValidateTOTP(secret, "000000", 6, 30, 1)
	if valid {
		t.Error("Invalid code should fail validation")
	}

	// Wrong secret
	valid, _ = ValidateTOTP("ABCDABCDABCDABCD", code, 6, 30, 1)
	if valid {
		t.Error("Wrong secret should fail validation")
	}
}

// TestGenerateHOTP tests HOTP generation
func TestGenerateHOTP(t *testing.T) {
	// Test RFC 4226 test vectors
	// Using secret "12345678901234567890" in Base32
	testSecret := "GEZDGNBVGY3TQOJQGEZDGNBVGY3TQOJQ"

	expectedCodes := []string{
		"755224", "287082", "359152", "969429", "338314",
		"254676", "287922", "162583", "399871", "520489",
	}

	for i, expected := range expectedCodes {
		code, err := GenerateHOTP(testSecret, uint64(i), 6)
		if err != nil {
			t.Fatalf("GenerateHOTP failed at counter %d: %v", i, err)
		}

		if code != expected {
			t.Errorf("HOTP counter %d: got %s, want %s", i, code, expected)
		}
	}
}

// TestValidateHOTP tests HOTP validation
func TestValidateHOTP(t *testing.T) {
	secret := "JBSWY3DPEHPK3PXP"

	// Generate and validate
	code, _ := GenerateHOTP(secret, 0, 6)
	valid, err := ValidateHOTP(secret, code, 0, 6)
	if err != nil {
		t.Fatalf("ValidateHOTP failed: %v", err)
	}

	if !valid {
		t.Error("Valid HOTP should pass")
	}

	// Wrong counter
	valid, _ = ValidateHOTP(secret, code, 1, 6)
	if valid {
		t.Error("Wrong counter should fail")
	}
}

// TestGetTimeRemaining tests time remaining calculation
func TestGetTimeRemaining(t *testing.T) {
	remaining := GetTimeRemaining(30)

	if remaining < 0 || remaining > 30 {
		t.Errorf("Time remaining should be 0-30, got %d", remaining)
	}
}

// TestGetTOTPInfo tests TOTP info
func TestGetTOTPInfo(t *testing.T) {
	info := GetTOTPInfo(30)

	if info.Period != 30 {
		t.Errorf("Period should be 30, got %d", info.Period)
	}

	if info.TimeRemaining < 0 || info.TimeRemaining > 30 {
		t.Errorf("TimeRemaining should be 0-30, got %d", info.TimeRemaining)
	}

	if info.Progress < 0 || info.Progress > 100 {
		t.Errorf("Progress should be 0-100, got %f", info.Progress)
	}

	if info.ExpiresAt.Before(time.Now()) {
		t.Error("ExpiresAt should be in the future")
	}
}

// TestGenerateOTPAuthURL tests otpauth URL generation
func TestGenerateOTPAuthURL(t *testing.T) {
	config := &OTPConfig{
		Secret:      "JBSWY3DPEHPK3PXP",
		Issuer:      "TestApp",
		AccountName: "test@example.com",
		Digits:      6,
		Algorithm:   AlgorithmSHA1,
		Period:      30,
	}

	url, err := GenerateTOTPAuthURL(config)
	if err != nil {
		t.Fatalf("GenerateTOTPAuthURL failed: %v", err)
	}

	if !strings.HasPrefix(url, "otpauth://totp/") {
		t.Errorf("URL should start with otpauth://totp/, got %s", url)
	}

	if !strings.Contains(url, "secret=") {
		t.Error("URL should contain secret")
	}

	if !strings.Contains(url, "issuer=") {
		t.Error("URL should contain issuer")
	}

	// Test HOTP URL
	url, err = GenerateHOTPAuthURL(config, 0)
	if err != nil {
		t.Fatalf("GenerateHOTPAuthURL failed: %v", err)
	}

	if !strings.HasPrefix(url, "otpauth://hotp/") {
		t.Errorf("URL should start with otpauth://hotp/, got %s", url)
	}
}

// TestParseOTPAuthURL tests otpauth URL parsing
func TestParseOTPAuthURL(t *testing.T) {
	original := &OTPConfig{
		Secret:      "JBSWY3DPEHPK3PXP",
		Issuer:      "TestApp",
		AccountName: "test@example.com",
		Digits:      6,
		Algorithm:   AlgorithmSHA1,
		Period:      30,
	}

	url, _ := GenerateTOTPAuthURL(original)
	parsed, typ, err := ParseOTPAuthURL(url)
	if err != nil {
		t.Fatalf("ParseOTPAuthURL failed: %v", err)
	}

	if typ != "totp" {
		t.Errorf("Type should be totp, got %s", typ)
	}

	if parsed.Secret != NormalizeSecret(original.Secret) {
		t.Errorf("Secret mismatch: got %s, want %s", parsed.Secret, NormalizeSecret(original.Secret))
	}

	if parsed.Issuer != original.Issuer {
		t.Errorf("Issuer mismatch: got %s, want %s", parsed.Issuer, original.Issuer)
	}

	if parsed.AccountName != original.AccountName {
		t.Errorf("AccountName mismatch: got %s, want %s", parsed.AccountName, original.AccountName)
	}
}

// TestVerifyCodeLength tests code length verification
func TestVerifyCodeLength(t *testing.T) {
	tests := []struct {
		code     string
		digits   int
		expected bool
	}{
		{"123456", 6, true},
		{"12345", 6, false},
		{"1234567", 6, false},
		{"12345678", 8, true},
		{"12345a", 6, false}, // Contains letter
		{"", 6, false},
	}

	for _, tt := range tests {
		result := VerifyCodeLength(tt.code, tt.digits)
		if result != tt.expected {
			t.Errorf("VerifyCodeLength(%q, %d) = %v, want %v", tt.code, tt.digits, result, tt.expected)
		}
	}
}

// TestFormatCode tests code formatting
func TestFormatCode(t *testing.T) {
	tests := []struct {
		code      string
		separator string
		expected  string
	}{
		{"123456", " ", "123 456"},
		{"123456", "-", "123-456"},
		{"12345678", " ", "1234 5678"},
		{"1234", "-", "1234"}, // No format for short codes
	}

	for _, tt := range tests {
		result := FormatCode(tt.code, tt.separator)
		if result != tt.expected {
			t.Errorf("FormatCode(%q, %q) = %q, want %q", tt.code, tt.separator, result, tt.expected)
		}
	}
}

// TestCalculateBackupCodes tests backup code generation
func TestCalculateBackupCodes(t *testing.T) {
	codes, err := CalculateBackupCodes(10, 8)
	if err != nil {
		t.Fatalf("CalculateBackupCodes failed: %v", err)
	}

	if len(codes) != 10 {
		t.Errorf("Should generate 10 codes, got %d", len(codes))
	}

	// Check each code
	seen := make(map[string]bool)
	for _, code := range codes {
		if len(code) != 8 {
			t.Errorf("Code should be 8 digits, got %s", code)
		}
		for _, c := range code {
			if c < '0' || c > '9' {
				t.Errorf("Code should only contain digits, got %s", code)
			}
		}
		if seen[code] {
			t.Errorf("Duplicate code: %s", code)
		}
		seen[code] = true
	}
}

// TestBatchGenerateTOTP tests batch TOTP generation
func TestBatchGenerateTOTP(t *testing.T) {
	secret := "JBSWY3DPEHPK3PXP"
	codes, err := BatchGenerateTOTP(secret, 6, 30, 5)
	if err != nil {
		t.Fatalf("BatchGenerateTOTP failed: %v", err)
	}

	if len(codes) != 5 {
		t.Errorf("Should generate 5 codes, got %d", len(codes))
	}

	for _, code := range codes {
		if len(code) != 6 {
			t.Errorf("Code should be 6 digits, got %s", code)
		}
	}
}

// TestAlgorithm tests algorithm string representation
func TestAlgorithm(t *testing.T) {
	tests := []struct {
		algo    Algorithm
		str     string
	}{
		{AlgorithmSHA1, "SHA1"},
		{AlgorithmSHA256, "SHA256"},
		{AlgorithmSHA512, "SHA512"},
		{Algorithm(99), "SHA1"}, // Default
	}

	for _, tt := range tests {
		if tt.algo.String() != tt.str {
			t.Errorf("Algorithm(%d).String() = %s, want %s", tt.algo, tt.algo.String(), tt.str)
		}
	}
}

// TestEndToEnd tests complete TOTP workflow
func TestEndToEnd(t *testing.T) {
	// Generate secret
	secret, err := GenerateSecret(20)
	if err != nil {
		t.Fatalf("GenerateSecret failed: %v", err)
	}

	// Create config
	config := &OTPConfig{
		Secret:      secret,
		Issuer:      "TestApp",
		AccountName: "user@example.com",
		Digits:      6,
		Algorithm:   AlgorithmSHA1,
		Period:      30,
		Skew:        1,
	}

	// Generate auth URL
	authURL, err := GenerateTOTPAuthURL(config)
	if err != nil {
		t.Fatalf("GenerateTOTPAuthURL failed: %v", err)
	}

	// Parse it back
	parsedConfig, typ, err := ParseOTPAuthURL(authURL)
	if err != nil {
		t.Fatalf("ParseOTPAuthURL failed: %v", err)
	}

	if typ != "totp" {
		t.Errorf("Type should be totp, got %s", typ)
	}

	// Generate TOTP code
	code, err := GenerateTOTPWithConfig(parsedConfig)
	if err != nil {
		t.Fatalf("GenerateTOTPWithConfig failed: %v", err)
	}

	// Validate
	valid, err := ValidateTOTPWithConfig(parsedConfig, code)
	if err != nil {
		t.Fatalf("ValidateTOTPWithConfig failed: %v", err)
	}

	if !valid {
		t.Error("Generated code should be valid")
	}

	t.Logf("End-to-end test passed: code=%s, url=%s", code, authURL)
}

// Benchmark tests
func BenchmarkGenerateTOTP(b *testing.B) {
	secret := "JBSWY3DPEHPK3PXP"
	for i := 0; i < b.N; i++ {
		GenerateTOTP(secret, 6, 30)
	}
}

func BenchmarkValidateTOTP(b *testing.B) {
	secret := "JBSWY3DPEHPK3PXP"
	code, _ := GenerateTOTP(secret, 6, 30)
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		ValidateTOTP(secret, code, 6, 30, 1)
	}
}

func BenchmarkGenerateSecret(b *testing.B) {
	for i := 0; i < b.N; i++ {
		GenerateSecret(20)
	}
}