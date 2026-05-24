// Package jwt_utils provides a simple JWT (JSON Web Token) implementation
// using only Go standard library. Supports HS256 (HMAC-SHA256) algorithm.
package jwt_utils

import (
	"crypto/hmac"
	"crypto/sha256"
	"encoding/base64"
	"encoding/json"
	"fmt"
	"strings"
	"time"
)

// Algorithm represents the JWT signing algorithm
type Algorithm string

const (
	HS256 Algorithm = "HS256"
)

// Header represents the JWT header
type Header struct {
	Alg string `json:"alg"`
	Typ string `json:"typ"`
}

// Claims represents the standard JWT claims
type Claims struct {
	Issuer         string `json:"iss,omitempty"`         // Issuer
	Subject        string `json:"sub,omitempty"`         // Subject
	Audience       string `json:"aud,omitempty"`         // Audience
	ExpirationTime int64  `json:"exp,omitempty"`         // Expiration Time
	NotBefore      int64  `json:"nbf,omitempty"`         // Not Before
	IssuedAt       int64  `json:"iat,omitempty"`         // Issued At
	JWTID          string `json:"jti,omitempty"`         // JWT ID
}

// Token represents a decoded JWT token
type Token struct {
	Header  Header
	Claims  Claims
	Payload map[string]interface{}
}

// JWTConfig holds configuration for JWT operations
type JWTConfig struct {
	Secret      []byte
	Algorithm   Algorithm
	ExpDuration time.Duration
	Issuer      string
}

// JWTUtils provides JWT utility functions
type JWTUtils struct {
	config JWTConfig
}

// NewJWTUtils creates a new JWTUtils instance
func NewJWTUtils(secret []byte, opts ...Option) *JWTUtils {
	config := JWTConfig{
		Secret:      secret,
		Algorithm:   HS256,
		ExpDuration: time.Hour * 24,
	}
	
	for _, opt := range opts {
		opt(&config)
	}
	
	return &JWTUtils{config: config}
}

// Option is a functional option for JWTUtils
type Option func(*JWTConfig)

// WithExpiration sets token expiration duration
func WithExpiration(d time.Duration) Option {
	return func(c *JWTConfig) {
		c.ExpDuration = d
	}
}

// WithIssuer sets token issuer
func WithIssuer(issuer string) Option {
	return func(c *JWTConfig) {
		c.Issuer = issuer
	}
}

// Generate creates a new JWT token with custom payload
func (j *JWTUtils) Generate(payload map[string]interface{}) (string, error) {
	return j.GenerateWithClaims(payload, Claims{})
}

// GenerateWithClaims creates a new JWT token with custom payload and claims
func (j *JWTUtils) GenerateWithClaims(payload map[string]interface{}, customClaims Claims) (string, error) {
	// Build header
	header := Header{
		Alg: string(j.config.Algorithm),
		Typ: "JWT",
	}
	
	// Build claims
	now := time.Now().Unix()
	claims := customClaims
	if claims.IssuedAt == 0 {
		claims.IssuedAt = now
	}
	if claims.ExpirationTime == 0 && j.config.ExpDuration > 0 {
		claims.ExpirationTime = now + int64(j.config.ExpDuration.Seconds())
	}
	if claims.Issuer == "" && j.config.Issuer != "" {
		claims.Issuer = j.config.Issuer
	}
	
	// Merge payload with claims
	fullPayload := make(map[string]interface{})
	for k, v := range payload {
		fullPayload[k] = v
	}
	claimBytes, _ := json.Marshal(claims)
	var claimMap map[string]interface{}
	json.Unmarshal(claimBytes, &claimMap)
	for k, v := range claimMap {
		if v != nil && v != "" && v != float64(0) {
			fullPayload[k] = v
		}
	}
	
	// Encode header and payload
	headerJSON, err := json.Marshal(header)
	if err != nil {
		return "", fmt.Errorf("failed to marshal header: %w", err)
	}
	
	payloadJSON, err := json.Marshal(fullPayload)
	if err != nil {
		return "", fmt.Errorf("failed to marshal payload: %w", err)
	}
	
	encodedHeader := base64URLEncode(headerJSON)
	encodedPayload := base64URLEncode(payloadJSON)
	
	// Sign
	signature := j.sign(encodedHeader + "." + encodedPayload)
	encodedSignature := base64URLEncode(signature)
	
	return encodedHeader + "." + encodedPayload + "." + encodedSignature, nil
}

// Validate checks if a JWT token is valid and returns its claims
func (j *JWTUtils) Validate(tokenString string) (*Token, error) {
	parts := strings.Split(tokenString, ".")
	if len(parts) != 3 {
		return nil, ErrInvalidTokenFormat
	}
	
	// Decode header
	headerBytes, err := base64URLDecode(parts[0])
	if err != nil {
		return nil, fmt.Errorf("failed to decode header: %w", err)
	}
	
	var header Header
	if err := json.Unmarshal(headerBytes, &header); err != nil {
		return nil, fmt.Errorf("failed to parse header: %w", err)
	}
	
	// Verify algorithm
	if header.Alg != string(j.config.Algorithm) {
		return nil, ErrUnsupportedAlgorithm
	}
	
	// Verify signature
	expectedSig := j.sign(parts[0] + "." + parts[1])
	actualSig, err := base64URLDecode(parts[2])
	if err != nil {
		return nil, fmt.Errorf("failed to decode signature: %w", err)
	}
	
	if !hmac.Equal(expectedSig, actualSig) {
		return nil, ErrInvalidSignature
	}
	
	// Decode payload
	payloadBytes, err := base64URLDecode(parts[1])
	if err != nil {
		return nil, fmt.Errorf("failed to decode payload: %w", err)
	}
	
	var payload map[string]interface{}
	if err := json.Unmarshal(payloadBytes, &payload); err != nil {
		return nil, fmt.Errorf("failed to parse payload: %w", err)
	}
	
	// Extract standard claims
	claims := Claims{}
	if iss, ok := payload["iss"]; ok {
		claims.Issuer = toString(iss)
	}
	if sub, ok := payload["sub"]; ok {
		claims.Subject = toString(sub)
	}
	if aud, ok := payload["aud"]; ok {
		claims.Audience = toString(aud)
	}
	if exp, ok := payload["exp"]; ok {
		claims.ExpirationTime = toInt64(exp)
	}
	if nbf, ok := payload["nbf"]; ok {
		claims.NotBefore = toInt64(nbf)
	}
	if iat, ok := payload["iat"]; ok {
		claims.IssuedAt = toInt64(iat)
	}
	if jti, ok := payload["jti"]; ok {
		claims.JWTID = toString(jti)
	}
	
	// Check expiration
	if claims.ExpirationTime > 0 && time.Now().Unix() > claims.ExpirationTime {
		return nil, ErrTokenExpired
	}
	
	// Check not before
	if claims.NotBefore > 0 && time.Now().Unix() < claims.NotBefore {
		return nil, ErrTokenNotValidYet
	}
	
	return &Token{
		Header:  header,
		Claims:  claims,
		Payload: payload,
	}, nil
}

// Parse decodes a JWT token without validation
func Parse(tokenString string) (*Token, error) {
	parts := strings.Split(tokenString, ".")
	if len(parts) != 3 {
		return nil, ErrInvalidTokenFormat
	}
	
	headerBytes, err := base64URLDecode(parts[0])
	if err != nil {
		return nil, fmt.Errorf("failed to decode header: %w", err)
	}
	
	var header Header
	if err := json.Unmarshal(headerBytes, &header); err != nil {
		return nil, fmt.Errorf("failed to parse header: %w", err)
	}
	
	payloadBytes, err := base64URLDecode(parts[1])
	if err != nil {
		return nil, fmt.Errorf("failed to decode payload: %w", err)
	}
	
	var payload map[string]interface{}
	if err := json.Unmarshal(payloadBytes, &payload); err != nil {
		return nil, fmt.Errorf("failed to parse payload: %w", err)
	}
	
	claims := Claims{}
	if iss, ok := payload["iss"]; ok {
		claims.Issuer = toString(iss)
	}
	if sub, ok := payload["sub"]; ok {
		claims.Subject = toString(sub)
	}
	if aud, ok := payload["aud"]; ok {
		claims.Audience = toString(aud)
	}
	if exp, ok := payload["exp"]; ok {
		claims.ExpirationTime = toInt64(exp)
	}
	if nbf, ok := payload["nbf"]; ok {
		claims.NotBefore = toInt64(nbf)
	}
	if iat, ok := payload["iat"]; ok {
		claims.IssuedAt = toInt64(iat)
	}
	if jti, ok := payload["jti"]; ok {
		claims.JWTID = toString(jti)
	}
	
	return &Token{
		Header:  header,
		Claims:  claims,
		Payload: payload,
	}, nil
}

// GetClaim retrieves a claim value from the token
func (t *Token) GetClaim(key string) (interface{}, bool) {
	v, ok := t.Payload[key]
	return v, ok
}

// IsExpired checks if the token is expired
func (t *Token) IsExpired() bool {
	if t.Claims.ExpirationTime == 0 {
		return false
	}
	return time.Now().Unix() > t.Claims.ExpirationTime
}

// sign creates an HMAC-SHA256 signature
func (j *JWTUtils) sign(data string) []byte {
	h := hmac.New(sha256.New, j.config.Secret)
	h.Write([]byte(data))
	return h.Sum(nil)
}

// base64URLEncode encodes bytes using base64 URL encoding (no padding)
func base64URLEncode(data []byte) string {
	return base64.RawURLEncoding.EncodeToString(data)
}

// base64URLDecode decodes a base64 URL encoded string
func base64URLDecode(data string) ([]byte, error) {
	return base64.RawURLEncoding.DecodeString(data)
}

// toString converts interface{} to string
func toString(v interface{}) string {
	if v == nil {
		return ""
	}
	switch val := v.(type) {
	case string:
		return val
	default:
		return fmt.Sprintf("%v", val)
	}
}

// toInt64 converts interface{} to int64
func toInt64(v interface{}) int64 {
	if v == nil {
		return 0
	}
	switch val := v.(type) {
	case float64:
		return int64(val)
	case float32:
		return int64(val)
	case int:
		return int64(val)
	case int64:
		return val
	case int32:
		return int64(val)
	case json.Number:
		i, _ := val.Int64()
		return i
	default:
		return 0
	}
}