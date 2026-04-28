package license_key_utils

import (
	"fmt"
	"regexp"
	"strings"
	"testing"
	"time"
)

func TestGenerate(t *testing.T) {
	key, err := Generate()
	if err != nil {
		t.Fatalf("Generate() error = %v", err)
	}
	
	if key == "" {
		t.Error("Generate() returned empty key")
	}
	
	// Check format: XXXX-XXXX-XXXX-XXXX
	pattern := regexp.MustCompile(`^[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}$`)
	if !pattern.MatchString(key) {
		t.Errorf("Generate() key format invalid: %s", key)
	}
}

func TestGenerateWithConfig_Standard(t *testing.T) {
	config := KeyConfig{
		Format:     FormatStandard,
		Segments:   4,
		SegmentLen: 5,
		Separator:  "-",
	}
	
	key, err := GenerateWithConfig(config)
	if err != nil {
		t.Fatalf("GenerateWithConfig() error = %v", err)
	}
	
	// Should have 4 segments of 5 chars each
	parts := strings.Split(key, "-")
	if len(parts) != 4 {
		t.Errorf("Expected 4 segments, got %d", len(parts))
	}
	
	for _, part := range parts {
		if len(part) != 5 {
			t.Errorf("Expected segment length 5, got %d", len(part))
		}
	}
}

func TestGenerateWithConfig_UUID(t *testing.T) {
	config := KeyConfig{
		Format: FormatUUID,
	}
	
	key, err := GenerateWithConfig(config)
	if err != nil {
		t.Fatalf("GenerateWithConfig() error = %v", err)
	}
	
	// UUID format: 8-4-4-4-12
	parts := strings.Split(key, "-")
	if len(parts) != 5 {
		t.Errorf("Expected 5 segments, got %d", len(parts))
	}
	
	expectedLengths := []int{8, 4, 4, 4, 12}
	for i, part := range parts {
		if len(part) != expectedLengths[i] {
			t.Errorf("Segment %d: expected length %d, got %d", i, expectedLengths[i], len(part))
		}
	}
}

func TestGenerateWithConfig_Compact(t *testing.T) {
	config := KeyConfig{
		Format:     FormatCompact,
		Segments:   4,
		SegmentLen: 4,
	}
	
	key, err := GenerateWithConfig(config)
	if err != nil {
		t.Fatalf("GenerateWithConfig() error = %v", err)
	}
	
	// Compact format: no separators
	if strings.Contains(key, "-") {
		t.Error("Compact format should not contain separators")
	}
	
	if len(key) != 16 {
		t.Errorf("Expected length 16, got %d", len(key))
	}
}

func TestGenerateWithPrefix(t *testing.T) {
	config := KeyConfig{
		Format:     FormatStandard,
		Segments:   4,
		SegmentLen: 4,
		Separator:  "-",
		Prefix:     "PROD-",
	}
	
	key, err := GenerateWithConfig(config)
	if err != nil {
		t.Fatalf("GenerateWithConfig() error = %v", err)
	}
	
	if !strings.HasPrefix(key, "PROD-") {
		t.Errorf("Key should start with prefix: %s", key)
	}
}

func TestGenerateWithSuffix(t *testing.T) {
	config := KeyConfig{
		Format:     FormatStandard,
		Segments:   4,
		SegmentLen: 4,
		Separator:  "-",
		Suffix:     "-ENT",
	}
	
	key, err := GenerateWithConfig(config)
	if err != nil {
		t.Fatalf("GenerateWithConfig() error = %v", err)
	}
	
	if !strings.HasSuffix(key, "-ENT") {
		t.Errorf("Key should end with suffix: %s", key)
	}
}

func TestGenerateWithChecksum(t *testing.T) {
	config := KeyConfig{
		Format:     FormatStandard,
		Segments:   4,
		SegmentLen: 4,
		Separator:  "-",
		Secret:     "test-secret",
	}
	
	key, err := GenerateWithChecksum(config)
	if err != nil {
		t.Fatalf("GenerateWithChecksum() error = %v", err)
	}
	
	// Should have 5 segments (4 + checksum)
	parts := strings.Split(key, "-")
	if len(parts) != 5 {
		t.Errorf("Expected 5 segments (4 + checksum), got %d", len(parts))
	}
	
	// Last segment should be 4 chars checksum
	if len(parts[4]) != 4 {
		t.Errorf("Checksum should be 4 chars, got %d", len(parts[4]))
	}
}

func TestValidateChecksum(t *testing.T) {
	config := KeyConfig{
		Format:     FormatStandard,
		Segments:   4,
		SegmentLen: 4,
		Separator:  "-",
		Secret:     "test-secret",
	}
	
	key, err := GenerateWithChecksum(config)
	if err != nil {
		t.Fatalf("GenerateWithChecksum() error = %v", err)
	}
	
	// Valid checksum
	err = ValidateChecksum(key, config)
	if err != nil {
		t.Errorf("ValidateChecksum() should pass for valid key: %v", err)
	}
	
	// Invalid checksum
	invalidKey := key[:len(key)-1] + "X"
	err = ValidateChecksum(invalidKey, config)
	if err == nil {
		t.Error("ValidateChecksum() should fail for invalid checksum")
	}
}

func TestGenerateBatch(t *testing.T) {
	config := DefaultConfig()
	
	keys, err := GenerateBatch(10, config)
	if err != nil {
		t.Fatalf("GenerateBatch() error = %v", err)
	}
	
	if len(keys) != 10 {
		t.Errorf("Expected 10 keys, got %d", len(keys))
	}
	
	// Check uniqueness
	seen := make(map[string]bool)
	for _, key := range keys {
		if seen[key] {
			t.Errorf("Duplicate key generated: %s", key)
		}
		seen[key] = true
	}
}

func TestParseKey(t *testing.T) {
	tests := []struct {
		name      string
		key       string
		wantError bool
	}{
		{"Valid standard", "ABCD-EFGH-IJKL-MNOP", false},
		{"Valid UUID", "A1B2C3D4-E5F6-7890-ABCD-EF1234567890", false},
		{"Valid compact", "ABCDEFGHIJKLMNOP", false},
		{"Too short", "ABC", true},
	}
	
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			lk, err := ParseKey(tt.key)
			if (err != nil) != tt.wantError {
				t.Errorf("ParseKey() error = %v, wantError %v", err, tt.wantError)
				return
			}
			if err == nil {
				if lk.Key == "" {
					t.Error("Parsed key should not be empty")
				}
			}
		})
	}
}

func TestFormatKey(t *testing.T) {
	config := KeyConfig{
		Format:     FormatStandard,
		Segments:   4,
		SegmentLen: 4,
		Separator:  "-",
	}
	
	// Test compact to standard conversion
	compactKey := "ABCDEFGHIJKLMNOP"
	formatted := FormatKey(compactKey, config)
	
	parts := strings.Split(formatted, "-")
	if len(parts) != 4 {
		t.Errorf("Expected 4 segments, got %d", len(parts))
	}
}

func TestMaskKey(t *testing.T) {
	config := DefaultConfig()
	
	key := "ABCD-EFGH-IJKL-MNOP"
	masked := MaskKey(key, config)
	
	if strings.Contains(masked, "ABCD") {
		t.Error("Masked key should not show first segment")
	}
	if !strings.Contains(masked, "MNOP") {
		t.Error("Masked key should show last segment")
	}
	
	parts := strings.Split(masked, "-")
	if parts[3] != "MNOP" {
		t.Errorf("Last segment should be visible, got %s", parts[3])
	}
}

func TestGenerateProductKey(t *testing.T) {
	productID := "MYAPP-001"
	config := DefaultConfig()
	
	key, err := GenerateProductKey(productID, config)
	if err != nil {
		t.Fatalf("GenerateProductKey() error = %v", err)
	}
	
	// Validate the product key
	err = ValidateProductKey(key, productID, config)
	if err != nil {
		t.Errorf("ValidateProductKey() should pass: %v", err)
	}
	
	// Different product ID should fail
	err = ValidateProductKey(key, "DIFFERENT-PRODUCT", config)
	if err == nil {
		t.Error("ValidateProductKey() should fail for different product ID")
	}
}

func TestGenerateWithExpiry(t *testing.T) {
	config := DefaultConfig()
	expiryDays := 30
	
	key, err := GenerateWithExpiry(config, expiryDays)
	if err != nil {
		t.Fatalf("GenerateWithExpiry() error = %v", err)
	}
	
	// Validate the key is not expired
	err = ValidateExpiry(key, config)
	if err != nil {
		t.Errorf("ValidateExpiry() should pass for new key: %v", err)
	}
}

func TestNoConfusingCharacters(t *testing.T) {
	// Generate many keys and check for confusing characters
	confusingChars := []string{"I", "O", "0", "1"}
	
	for i := 0; i < 100; i++ {
		key, err := Generate()
		if err != nil {
			t.Fatalf("Generate() error = %v", err)
		}
		
		for _, char := range confusingChars {
			if strings.Contains(key, char) {
				t.Errorf("Key contains confusing character '%s': %s", char, key)
			}
		}
	}
}

func TestUniqueness(t *testing.T) {
	config := DefaultConfig()
	keys := make(map[string]bool)
	
	// Generate 1000 keys and check uniqueness
	for i := 0; i < 1000; i++ {
		key, err := GenerateWithConfig(config)
		if err != nil {
			t.Fatalf("GenerateWithConfig() error = %v", err)
		}
		
		if keys[key] {
			t.Errorf("Duplicate key generated: %s", key)
		}
		keys[key] = true
	}
}

func BenchmarkGenerate(b *testing.B) {
	for i := 0; i < b.N; i++ {
		_, _ = Generate()
	}
}

func BenchmarkGenerateWithChecksum(b *testing.B) {
	config := DefaultConfig()
	config.Secret = "benchmark-secret"
	
	for i := 0; i < b.N; i++ {
		_, _ = GenerateWithChecksum(config)
	}
}

func BenchmarkValidateChecksum(b *testing.B) {
	config := DefaultConfig()
	config.Secret = "benchmark-secret"
	
	key, _ := GenerateWithChecksum(config)
	
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		_ = ValidateChecksum(key, config)
	}
}

// Example usage
func ExampleGenerate() {
	key, _ := Generate()
	fmt.Println("Generated key:", key)
	// Output format: XXXX-XXXX-XXXX-XXXX
}

func ExampleGenerateWithChecksum() {
	config := KeyConfig{
		Format:     FormatStandard,
		Segments:   4,
		SegmentLen: 4,
		Separator:  "-",
		Secret:     "my-secret-key",
	}
	
	key, _ := GenerateWithChecksum(config)
	fmt.Println("Key with checksum:", key)
	// Output format: XXXX-XXXX-XXXX-XXXX-XXXX (last 4 chars are checksum)
}

func ExampleGenerateBatch() {
	config := DefaultConfig()
	keys, _ := GenerateBatch(5, config)
	
	for i, key := range keys {
		fmt.Printf("Key %d: %s\n", i+1, key)
	}
}

func ExampleMaskKey() {
	config := DefaultConfig()
	key := "ABCD-EFGH-IJKL-MNOP"
	
	masked := MaskKey(key, config)
	fmt.Println(masked)
	// Output: ****-****-****-MNOP
}

func ExampleGenerateProductKey() {
	productID := "MY-APP-001"
	config := DefaultConfig()
	
	key, _ := GenerateProductKey(productID, config)
	
	err := ValidateProductKey(key, productID, config)
	if err != nil {
		fmt.Println("Invalid key")
	} else {
		fmt.Println("Valid product key")
	}
}

func ExampleGenerateWithExpiry() {
	config := DefaultConfig()
	
	// Generate key valid for 30 days
	key, _ := GenerateWithExpiry(config, 30)
	
	// Check if key is still valid
	err := ValidateExpiry(key, config)
	if err == ErrKeyExpired {
		fmt.Println("Key has expired")
	} else {
		fmt.Println("Key is valid")
	}
}

func TestDecodeExpiry(t *testing.T) {
	// Test encode/decode roundtrip
	days := 365
	encoded := encodeExpiry(days)
	
	decodedTime, err := decodeExpiry(encoded)
	if err != nil {
		t.Fatalf("decodeExpiry() error = %v", err)
	}
	
	expectedExpiry := time.Now().AddDate(0, 0, days)
	tolerance := 24 * time.Hour  // Allow 1 day tolerance for time calculations
	
	diff := decodedTime.Sub(expectedExpiry)
	if diff < -tolerance || diff > tolerance {
		t.Errorf("Decoded time off by %v", diff)
	}
	
	// Verify the decoded time is approximately the expected expiry
	if decodedTime.Before(time.Now()) {
		t.Error("Decoded time should be in the future")
	}
}