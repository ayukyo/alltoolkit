// Package otp_utils provides TOTP (Time-based One-Time Password) and HOTP (HMAC-based One-Time Password) utilities.
// Zero external dependencies - uses only Go standard library.
// Compatible with Google Authenticator, Authy, and other authenticator apps.
package otp_utils

import (
	"crypto/hmac"
	"crypto/rand"
	"crypto/sha1"
	"crypto/sha256"
	"crypto/sha512"
	"encoding/base32"
	"encoding/binary"
	"errors"
	"fmt"
	"hash"
	"net/url"
	"strconv"
	"strings"
	"time"
)

// Algorithm represents the hash algorithm used for OTP
type Algorithm int

const (
	AlgorithmSHA1 Algorithm = iota
	AlgorithmSHA256
	AlgorithmSHA512
)

// String returns the string representation of the algorithm
func (a Algorithm) String() string {
	switch a {
	case AlgorithmSHA1:
		return "SHA1"
	case AlgorithmSHA256:
		return "SHA256"
	case AlgorithmSHA512:
		return "SHA512"
	default:
		return "SHA1"
	}
}

// OTPConfig holds the configuration for OTP generation
type OTPConfig struct {
	Secret      string    // Base32 encoded secret
	Digits      int       // Number of digits (typically 6 or 8)
	Algorithm   Algorithm // Hash algorithm
	Period      int       // Time period in seconds (for TOTP, typically 30)
	Skew        int       // Allowed time skew in periods
	Issuer      string    // Issuer name for authenticator apps
	AccountName string    // Account name for authenticator apps
}

// DefaultTOTPConfig returns a default TOTP configuration
func DefaultTOTPConfig() *OTPConfig {
	return &OTPConfig{
		Digits:    6,
		Algorithm: AlgorithmSHA1,
		Period:    30,
		Skew:      1,
	}
}

// DefaultHOTPConfig returns a default HOTP configuration
func DefaultHOTPConfig() *OTPConfig {
	return &OTPConfig{
		Digits:    6,
		Algorithm: AlgorithmSHA1,
	}
}

// GenerateSecret generates a random secret key of the specified length
func GenerateSecret(length int) (string, error) {
	if length <= 0 {
		length = 20 // Default 160 bits
	}
	secret := make([]byte, length)
	_, err := rand.Read(secret)
	if err != nil {
		return "", fmt.Errorf("failed to generate random secret: %w", err)
	}
	return base32.StdEncoding.WithPadding(base32.NoPadding).EncodeToString(secret), nil
}

// GenerateSecretWithConfig generates a random secret using config defaults
func GenerateSecretWithConfig() (string, error) {
	return GenerateSecret(20)
}

// ValidateSecret checks if the provided secret is a valid base32 string
func ValidateSecret(secret string) error {
	if secret == "" {
		return errors.New("secret cannot be empty")
	}
	secret = strings.ToUpper(strings.ReplaceAll(secret, " ", ""))
	_, err := base32.StdEncoding.WithPadding(base32.NoPadding).DecodeString(secret)
	if err != nil {
		return fmt.Errorf("invalid base32 secret: %w", err)
	}
	return nil
}

// NormalizeSecret removes spaces and converts to uppercase
func NormalizeSecret(secret string) string {
	return strings.ToUpper(strings.ReplaceAll(secret, " ", ""))
}

// hotp generates an HOTP code
func hotp(secret string, counter uint64, digits int, algorithm Algorithm) (string, error) {
	// Decode base32 secret
	secret = NormalizeSecret(secret)
	key, err := base32.StdEncoding.WithPadding(base32.NoPadding).DecodeString(secret)
	if err != nil {
		return "", fmt.Errorf("invalid secret: %w", err)
	}

	// Create HMAC
	var h func() hash.Hash
	switch algorithm {
	case AlgorithmSHA256:
		h = sha256.New
	case AlgorithmSHA512:
		h = sha512.New
	default:
		h = sha1.New
	}

	mac := hmac.New(h, key)

	// Write counter as big-endian uint64
	counterBytes := make([]byte, 8)
	binary.BigEndian.PutUint64(counterBytes, counter)
	mac.Write(counterBytes)
	hash := mac.Sum(nil)

	// Dynamic truncation
	offset := hash[len(hash)-1] & 0x0f
	code := binary.BigEndian.Uint32(hash[offset:offset+4]) & 0x7fffffff

	// Generate digits
	mod := uint32(1)
	for i := 0; i < digits; i++ {
		mod *= 10
	}
	code = code % mod

	// Format with leading zeros
	return fmt.Sprintf("%0*d", digits, code), nil
}

// GenerateHOTP generates an HOTP code for the given counter
func GenerateHOTP(secret string, counter uint64, digits int) (string, error) {
	if digits <= 0 {
		digits = 6
	}
	return hotp(secret, counter, digits, AlgorithmSHA1)
}

// GenerateHOTPWithConfig generates an HOTP code using the provided config
func GenerateHOTPWithConfig(config *OTPConfig, counter uint64) (string, error) {
	if config == nil {
		return "", errors.New("config cannot be nil")
	}
	if err := ValidateSecret(config.Secret); err != nil {
		return "", err
	}
	return hotp(config.Secret, counter, config.Digits, config.Algorithm)
}

// GenerateTOTP generates a TOTP code for the current time
func GenerateTOTP(secret string, digits int, period int) (string, error) {
	if digits <= 0 {
		digits = 6
	}
	if period <= 0 {
		period = 30
	}
	return GenerateTOTPAtTime(secret, digits, period, time.Now())
}

// GenerateTOTPAtTime generates a TOTP code for a specific timestamp
func GenerateTOTPAtTime(secret string, digits int, period int, timestamp time.Time) (string, error) {
	counter := uint64(timestamp.Unix()) / uint64(period)
	return hotp(secret, counter, digits, AlgorithmSHA1)
}

// GenerateTOTPWithConfig generates a TOTP code using the provided config
func GenerateTOTPWithConfig(config *OTPConfig) (string, error) {
	return GenerateTOTPWithConfigAtTime(config, time.Now())
}

// GenerateTOTPWithConfigAtTime generates a TOTP code at a specific time
func GenerateTOTPWithConfigAtTime(config *OTPConfig, timestamp time.Time) (string, error) {
	if config == nil {
		return "", errors.New("config cannot be nil")
	}
	if err := ValidateSecret(config.Secret); err != nil {
		return "", err
	}
	if config.Period <= 0 {
		config.Period = 30
	}
	counter := uint64(timestamp.Unix()) / uint64(config.Period)
	return hotp(config.Secret, counter, config.Digits, config.Algorithm)
}

// ValidateTOTP validates a TOTP code against the secret
func ValidateTOTP(secret string, code string, digits int, period int, skew int) (bool, error) {
	if skew < 0 {
		skew = 0
	}
	return ValidateTOTPAtTime(secret, code, digits, period, skew, time.Now())
}

// ValidateTOTPAtTime validates a TOTP code at a specific time
func ValidateTOTPAtTime(secret string, code string, digits int, period int, skew int, timestamp time.Time) (bool, error) {
	if err := ValidateSecret(secret); err != nil {
		return false, err
	}
	if period <= 0 {
		period = 30
	}

	// Normalize code
	code = strings.TrimSpace(code)
	expectedLen := digits
	if expectedLen <= 0 {
		expectedLen = 6
	}
	if len(code) != expectedLen {
		return false, nil
	}

	currentCounter := uint64(timestamp.Unix()) / uint64(period)

	// Check current and surrounding periods based on skew
	for i := -skew; i <= skew; i++ {
		counter := currentCounter + uint64(i)
		expectedCode, err := hotp(secret, counter, digits, AlgorithmSHA1)
		if err != nil {
			return false, err
		}
		if hmac.Equal([]byte(code), []byte(expectedCode)) {
			return true, nil
		}
	}

	return false, nil
}

// ValidateTOTPWithConfig validates a TOTP code using the provided config
func ValidateTOTPWithConfig(config *OTPConfig, code string) (bool, error) {
	return ValidateTOTPWithConfigAtTime(config, code, time.Now())
}

// ValidateTOTPWithConfigAtTime validates a TOTP code at a specific time
func ValidateTOTPWithConfigAtTime(config *OTPConfig, code string, timestamp time.Time) (bool, error) {
	if config == nil {
		return false, errors.New("config cannot be nil")
	}
	if err := ValidateSecret(config.Secret); err != nil {
		return false, err
	}
	if config.Period <= 0 {
		config.Period = 30
	}

	// Normalize code
	code = strings.TrimSpace(code)
	if len(code) != config.Digits {
		return false, nil
	}

	currentCounter := uint64(timestamp.Unix()) / uint64(config.Period)

	// Check current and surrounding periods based on skew
	for i := -config.Skew; i <= config.Skew; i++ {
		counter := currentCounter + uint64(i)
		expectedCode, err := hotp(config.Secret, counter, config.Digits, config.Algorithm)
		if err != nil {
			return false, err
		}
		if hmac.Equal([]byte(code), []byte(expectedCode)) {
			return true, nil
		}
	}

	return false, nil
}

// ValidateHOTP validates an HOTP code
func ValidateHOTP(secret string, code string, counter uint64, digits int) (bool, error) {
	if err := ValidateSecret(secret); err != nil {
		return false, err
	}

	code = strings.TrimSpace(code)
	expectedLen := digits
	if expectedLen <= 0 {
		expectedLen = 6
	}
	if len(code) != expectedLen {
		return false, nil
	}

	expectedCode, err := hotp(secret, counter, digits, AlgorithmSHA1)
	if err != nil {
		return false, err
	}

	return hmac.Equal([]byte(code), []byte(expectedCode)), nil
}

// GetTimeRemaining returns the seconds remaining until the next TOTP period
func GetTimeRemaining(period int) int {
	if period <= 0 {
		period = 30
	}
	return period - int(time.Now().Unix()%int64(period))
}

// GetTOTPInfo returns information about the current TOTP period
func GetTOTPInfo(period int) TOTPInfo {
	if period <= 0 {
		period = 30
	}
	now := time.Now().Unix()
	currentPeriod := now / int64(period)
	remaining := period - int(now%int64(period))
	progress := float64(period-remaining) / float64(period) * 100

	return TOTPInfo{
		Period:        period,
		CurrentPeriod: currentPeriod,
		TimeRemaining: remaining,
		Progress:      progress,
		ExpiresAt:     time.Now().Add(time.Duration(remaining) * time.Second),
	}
}

// TOTPInfo holds information about the current TOTP period
type TOTPInfo struct {
	Period        int       // Period duration in seconds
	CurrentPeriod int64     // Current period number
	TimeRemaining int       // Seconds until next period
	Progress      float64   // Progress percentage (0-100)
	ExpiresAt     time.Time // When the current code expires
}

// GenerateOTPAuthURL generates an otpauth:// URL for QR code generation
func GenerateOTPAuthURL(typ string, config *OTPConfig) (string, error) {
	if config == nil {
		return "", errors.New("config cannot be nil")
	}
	if config.Secret == "" {
		return "", errors.New("secret is required")
	}
	if typ != "totp" && typ != "hotp" {
		return "", errors.New("type must be 'totp' or 'hotp'")
	}

	// Build URL
	var label string
	if config.Issuer != "" && config.AccountName != "" {
		label = fmt.Sprintf("%s:%s", config.Issuer, config.AccountName)
	} else if config.AccountName != "" {
		label = config.AccountName
	} else if config.Issuer != "" {
		label = config.Issuer
	} else {
		label = "Account"
	}

	u := url.URL{
		Scheme: "otpauth",
		Host:   typ,
		Path:   label,
	}

	q := url.Values{}
	q.Set("secret", NormalizeSecret(config.Secret))
	if config.Digits != 6 {
		q.Set("digits", strconv.Itoa(config.Digits))
	}
	if config.Algorithm != AlgorithmSHA1 {
		q.Set("algorithm", config.Algorithm.String())
	}
	if typ == "totp" && config.Period != 0 && config.Period != 30 {
		q.Set("period", strconv.Itoa(config.Period))
	}
	if config.Issuer != "" {
		q.Set("issuer", config.Issuer)
	}

	u.RawQuery = q.Encode()
	return u.String(), nil
}

// GenerateTOTPAuthURL generates an otpauth:// URL for TOTP
func GenerateTOTPAuthURL(config *OTPConfig) (string, error) {
	return GenerateOTPAuthURL("totp", config)
}

// GenerateHOTPAuthURL generates an otpauth:// URL for HOTP
func GenerateHOTPAuthURL(config *OTPConfig, counter uint64) (string, error) {
	url, err := GenerateOTPAuthURL("hotp", config)
	if err != nil {
		return "", err
	}
	// Add counter parameter
	if counter != 0 {
		if strings.Contains(url, "?") {
			return url + "&counter=" + strconv.FormatUint(counter, 10), nil
		}
		return url + "?counter=" + strconv.FormatUint(counter, 10), nil
	}
	return url, nil
}

// ParseOTPAuthURL parses an otpauth:// URL into an OTPConfig
func ParseOTPAuthURL(otpauthURL string) (*OTPConfig, string, error) {
	u, err := url.Parse(otpauthURL)
	if err != nil {
		return nil, "", fmt.Errorf("invalid URL: %w", err)
	}

	if u.Scheme != "otpauth" {
		return nil, "", errors.New("invalid scheme, expected otpauth")
	}

	typ := u.Host
	if typ != "totp" && typ != "hotp" {
		return nil, "", errors.New("type must be 'totp' or 'hotp'")
	}

	config := DefaultTOTPConfig()
	if typ == "hotp" {
		config = DefaultHOTPConfig()
	}

	// Parse path for issuer and account name
	path := strings.TrimPrefix(u.Path, "/")
	if strings.Contains(path, ":") {
		parts := strings.SplitN(path, ":", 2)
		config.Issuer = parts[0]
		config.AccountName = parts[1]
	} else {
		config.AccountName = path
	}

	// Parse query parameters
	q := u.Query()
	config.Secret = q.Get("secret")
	if config.Secret == "" {
		return nil, "", errors.New("secret is required")
	}

	if digits := q.Get("digits"); digits != "" {
		d, err := strconv.Atoi(digits)
		if err != nil {
			return nil, "", fmt.Errorf("invalid digits: %w", err)
		}
		config.Digits = d
	}

	if algo := q.Get("algorithm"); algo != "" {
		switch strings.ToUpper(algo) {
		case "SHA1":
			config.Algorithm = AlgorithmSHA1
		case "SHA256":
			config.Algorithm = AlgorithmSHA256
		case "SHA512":
			config.Algorithm = AlgorithmSHA512
		default:
			return nil, "", fmt.Errorf("unsupported algorithm: %s", algo)
		}
	}

	if period := q.Get("period"); period != "" {
		p, err := strconv.Atoi(period)
		if err != nil {
			return nil, "", fmt.Errorf("invalid period: %w", err)
		}
		config.Period = p
	}

	if issuer := q.Get("issuer"); issuer != "" {
		config.Issuer = issuer
	}

	return config, typ, nil
}

// VerifyCodeLength checks if a code has the expected number of digits
func VerifyCodeLength(code string, expectedDigits int) bool {
	code = strings.TrimSpace(code)
	if len(code) != expectedDigits {
		return false
	}
	for _, c := range code {
		if c < '0' || c > '9' {
			return false
		}
	}
	return true
}

// FormatCode formats a code with a separator for better readability
func FormatCode(code string, separator string) string {
	if len(code) == 6 {
		return code[:3] + separator + code[3:]
	}
	if len(code) == 8 {
		return code[:4] + separator + code[4:]
	}
	return code
}

// CalculateBackupCodes generates a set of backup/recovery codes
func CalculateBackupCodes(count int, length int) ([]string, error) {
	if count <= 0 {
		count = 10
	}
	if length <= 0 {
		length = 8
	}

	codes := make([]string, count)
	for i := 0; i < count; i++ {
		code, err := generateRandomCode(length)
		if err != nil {
			return nil, err
		}
		codes[i] = code
	}
	return codes, nil
}

// generateRandomCode generates a random numeric code
func generateRandomCode(length int) (string, error) {
	digits := "0123456789"
	code := make([]byte, length)
	randomBytes := make([]byte, length)

	_, err := rand.Read(randomBytes)
	if err != nil {
		return "", err
	}

	for i := range code {
		code[i] = digits[int(randomBytes[i])%len(digits)]
	}

	return string(code), nil
}

// BatchGenerateTOTP generates multiple TOTP codes for different periods
func BatchGenerateTOTP(secret string, digits int, period int, count int) ([]string, error) {
	if count <= 0 {
		count = 5
	}

	codes := make([]string, count)
	currentCounter := uint64(time.Now().Unix()) / uint64(period)

	for i := 0; i < count; i++ {
		code, err := hotp(secret, currentCounter+uint64(i), digits, AlgorithmSHA1)
		if err != nil {
			return nil, err
		}
		codes[i] = code
	}

	return codes, nil
}