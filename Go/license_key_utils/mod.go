// Package license_key_utils provides license key generation and validation utilities.
// It supports multiple key formats including standard, UUID-based, and custom format keys.
package license_key_utils

import (
	"crypto/rand"
	"crypto/sha256"
	"encoding/hex"
	"errors"
	"fmt"
	"regexp"
	"strings"
	"time"
)

// KeyFormat defines the format of license keys
type KeyFormat int

const (
	// FormatStandard generates keys like: XXXX-XXXX-XXXX-XXXX
	FormatStandard KeyFormat = iota
	// FormatUUID generates UUID-like keys: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
	FormatUUID
	// FormatCompact generates keys without separators: XXXXXXXXXXXXXXXX
	FormatCompact
	// FormatCustom allows custom segment lengths
	FormatCustom
)

// KeyConfig holds configuration for key generation
type KeyConfig struct {
	Format      KeyFormat
	Segments    int    // Number of segments (for standard/custom format)
	SegmentLen  int    // Length of each segment (for custom format)
	Separator   string // Separator between segments
	Prefix      string // Optional prefix for keys
	Suffix      string // Optional suffix for keys
	Secret      string // Secret for HMAC-based keys
	ExpiryDays  int    // Days until expiration (0 = no expiration)
	MaxActivations int  // Maximum number of activations (0 = unlimited)
}

// LicenseKey represents a parsed license key with metadata
type LicenseKey struct {
	Key          string
	ProductID    string
	CustomerID   string
	IssueDate    time.Time
	ExpiryDate   *time.Time
	MaxActivations int
	Activations  int
	Metadata     map[string]string
}

var (
	// ErrInvalidKeyFormat is returned when key format is invalid
	ErrInvalidKeyFormat = errors.New("invalid license key format")
	// ErrKeyExpired is returned when key has expired
	ErrKeyExpired = errors.New("license key has expired")
	// ErrInvalidChecksum is returned when checksum validation fails
	ErrInvalidChecksum = errors.New("invalid key checksum")
	// ErrTooManyActivations is returned when activation limit is reached
	ErrTooManyActivations = errors.New("maximum activations reached")
)

// DefaultConfig returns default configuration for key generation
func DefaultConfig() KeyConfig {
	return KeyConfig{
		Format:     FormatStandard,
		Segments:   4,
		SegmentLen: 4,
		Separator:  "-",
	}
}

// Generate generates a random license key with default configuration
func Generate() (string, error) {
	return GenerateWithConfig(DefaultConfig())
}

// GenerateWithConfig generates a license key with custom configuration
func GenerateWithConfig(config KeyConfig) (string, error) {
	var segments []string
	totalLength := config.Segments * config.SegmentLen

	if config.Format == FormatStandard || config.Format == FormatCustom {
		if config.Segments <= 0 {
			config.Segments = 4
		}
		if config.SegmentLen <= 0 {
			config.SegmentLen = 4
		}
		totalLength = config.Segments * config.SegmentLen
		segments = make([]string, config.Segments)
	} else if config.Format == FormatUUID {
		config.Segments = 5
		segmentLengths := []int{8, 4, 4, 4, 12}
		segments = make([]string, 5)
		for i, length := range segmentLengths {
			segment, err := generateRandomString(length)
			if err != nil {
				return "", err
			}
			segments[i] = segment
		}
		return config.Prefix + strings.Join(segments, "-") + config.Suffix, nil
	} else if config.Format == FormatCompact {
		if config.Segments <= 0 {
			config.Segments = 4
		}
		if config.SegmentLen <= 0 {
			config.SegmentLen = 4
		}
		totalLength = config.Segments * config.SegmentLen
		str, err := generateRandomString(totalLength)
		if err != nil {
			return "", err
		}
		return config.Prefix + str + config.Suffix, nil
	}

	// Generate segments
	for i := 0; i < config.Segments; i++ {
		segment, err := generateRandomString(config.SegmentLen)
		if err != nil {
			return "", err
		}
		segments[i] = segment
	}

	// Join with separator
	key := strings.Join(segments, config.Separator)
	
	// Add prefix and suffix
	if config.Prefix != "" {
		key = config.Prefix + key
	}
	if config.Suffix != "" {
		key = key + config.Suffix
	}

	return key, nil
}

// GenerateWithChecksum generates a key with a built-in checksum
func GenerateWithChecksum(config KeyConfig) (string, error) {
	key, err := GenerateWithConfig(config)
	if err != nil {
		return "", err
	}

	// Calculate checksum from key
	checksum := calculateChecksum(key + config.Secret)
	
	// Append checksum
	separator := config.Separator
	if separator == "" {
		separator = "-"
	}
	
	return key + separator + checksum[:4], nil
}

// ValidateChecksum validates a key with checksum
func ValidateChecksum(key string, config KeyConfig) error {
	parts := strings.Split(key, config.Separator)
	if len(parts) < 2 {
		return ErrInvalidKeyFormat
	}

	// Extract key and checksum
	providedChecksum := parts[len(parts)-1]
	keyWithoutChecksum := strings.Join(parts[:len(parts)-1], config.Separator)

	// Calculate expected checksum
	expectedChecksum := calculateChecksum(keyWithoutChecksum + config.Secret)

	if !strings.EqualFold(providedChecksum, expectedChecksum[:4]) {
		return ErrInvalidChecksum
	}

	return nil
}

// GenerateWithExpiry generates a key with embedded expiry date
func GenerateWithExpiry(config KeyConfig, expiryDays int) (string, error) {
	key, err := GenerateWithConfig(config)
	if err != nil {
		return "", err
	}

	// Embed expiry info
	expiryCode := encodeExpiry(expiryDays)
	separator := config.Separator
	if separator == "" {
		separator = "-"
	}

	return key + separator + expiryCode, nil
}

// ValidateExpiry validates if a key is still valid
func ValidateExpiry(key string, config KeyConfig) error {
	parts := strings.Split(key, config.Separator)
	if len(parts) < 1 {
		return ErrInvalidKeyFormat
	}

	// Extract expiry code (last segment)
	expiryCode := parts[len(parts)-1]
	if len(expiryCode) != 6 {
		return nil // No expiry code, key is valid forever
	}

	// Decode expiry
	expiryDate, err := decodeExpiry(expiryCode)
	if err != nil {
		return nil // Invalid expiry code format, assume valid
	}

	if time.Now().After(expiryDate) {
		return ErrKeyExpired
	}

	return nil
}

// GenerateBatch generates multiple unique keys
func GenerateBatch(count int, config KeyConfig) ([]string, error) {
	keys := make([]string, 0, count)
	seen := make(map[string]bool)

	for len(keys) < count {
		key, err := GenerateWithConfig(config)
		if err != nil {
			return nil, err
		}

		if !seen[key] {
			seen[key] = true
			keys = append(keys, key)
		}
	}

	return keys, nil
}

// ParseKey parses a license key into its components
func ParseKey(key string) (*LicenseKey, error) {
	// Clean the key
	key = strings.TrimSpace(strings.ToUpper(key))
	
	// Basic validation
	if len(key) < 8 {
		return nil, ErrInvalidKeyFormat
	}

	// Standard format: XXXX-XXXX-XXXX-XXXX
	standardPattern := regexp.MustCompile(`^([A-Z0-9]{4}-){3}[A-Z0-9]{4}$`)
	// UUID format: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
	uuidPattern := regexp.MustCompile(`^[A-Z0-9]{8}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{12}$`)
	// Compact format: XXXXXXXXXXXXXXXX
	compactPattern := regexp.MustCompile(`^[A-Z0-9]{16,32}$`)

	now := time.Now()
	lk := &LicenseKey{
		Key:        key,
		IssueDate:  now,
		Metadata:   make(map[string]string),
	}

	switch {
	case standardPattern.MatchString(key):
		lk.Metadata["format"] = "standard"
	case uuidPattern.MatchString(key):
		lk.Metadata["format"] = "uuid"
	case compactPattern.MatchString(key):
		lk.Metadata["format"] = "compact"
	default:
		lk.Metadata["format"] = "unknown"
	}

	return lk, nil
}

// GenerateProductKey generates a key for a specific product
func GenerateProductKey(productID string, config KeyConfig) (string, error) {
	// Use productID as part of the secret for deterministic but unique keys
	config.Secret = productID
	return GenerateWithChecksum(config)
}

// ValidateProductKey validates a product-specific key
func ValidateProductKey(key, productID string, config KeyConfig) error {
	config.Secret = productID
	
	if err := ValidateChecksum(key, config); err != nil {
		return err
	}

	if err := ValidateExpiry(key, config); err != nil {
		return err
	}

	return nil
}

// FormatKey reformats a key to a specific format
func FormatKey(key string, config KeyConfig) string {
	// Remove all separators
	key = strings.ReplaceAll(key, "-", "")
	key = strings.ReplaceAll(key, " ", "")
	key = strings.ToUpper(key)

	if config.Format == FormatCompact {
		return config.Prefix + key + config.Suffix
	}

	// Determine segment length
	segLen := config.SegmentLen
	if segLen <= 0 {
		segLen = 4
	}

	// Split into segments
	var segments []string
	for i := 0; i < len(key); i += segLen {
		end := i + segLen
		if end > len(key) {
			end = len(key)
		}
		segments = append(segments, key[i:end])
	}

	result := strings.Join(segments, config.Separator)
	return config.Prefix + result + config.Suffix
}

// MaskKey masks a key for display (shows only last segment)
func MaskKey(key string, config KeyConfig) string {
	parts := strings.Split(key, config.Separator)
	if len(parts) < 2 {
		return "****-****"
	}
	
	masked := make([]string, len(parts))
	for i := range parts {
		if i == len(parts)-1 {
			masked[i] = parts[i]
		} else {
			masked[i] = strings.Repeat("*", len(parts[i]))
		}
	}
	return strings.Join(masked, config.Separator)
}

// Helper functions

func generateRandomString(length int) (string, error) {
	const charset = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789" // Removed confusing chars: I, O, 0, 1
	bytes := make([]byte, length)
	
	if _, err := rand.Read(bytes); err != nil {
		return "", err
	}
	
	for i := range bytes {
		bytes[i] = charset[int(bytes[i])%len(charset)]
	}
	
	return string(bytes), nil
}

func calculateChecksum(input string) string {
	hash := sha256.Sum256([]byte(input))
	return strings.ToUpper(hex.EncodeToString(hash[:]))
}

func encodeExpiry(days int) string {
	// Encode expiry as days from epoch in base36
	expiryDate := time.Now().AddDate(0, 0, days)
	daysFromEpoch := expiryDate.Unix() / (24 * 60 * 60)
	return strings.ToUpper(strings.TrimPrefix(
		fmt.Sprintf("%06X", daysFromEpoch), "0"))
}

func decodeExpiry(code string) (time.Time, error) {
	var daysFromEpoch int64
	_, err := fmt.Sscanf(code, "%X", &daysFromEpoch)
	if err != nil {
		return time.Time{}, err
	}
	
	expiryDate := time.Unix(daysFromEpoch*24*60*60, 0)
	return expiryDate, nil
}