package jwt_utils

import (
	"testing"
	"time"
)

func TestGenerateAndValidate(t *testing.T) {
	secret := []byte("my-secret-key")
	jwt := NewJWTUtils(secret)
	
	payload := map[string]interface{}{
		"user_id": 123,
		"role":    "admin",
		"email":   "test@example.com",
	}
	
	token, err := jwt.Generate(payload)
	if err != nil {
		t.Fatalf("Failed to generate token: %v", err)
	}
	
	if token == "" {
		t.Fatal("Generated token is empty")
	}
	
	// Token should have 3 parts
	parts := splitToken(token)
	if len(parts) != 3 {
		t.Fatalf("Expected 3 parts, got %d", len(parts))
	}
	
	// Validate token
	decoded, err := jwt.Validate(token)
	if err != nil {
		t.Fatalf("Failed to validate token: %v", err)
	}
	
	// Check payload
	if decoded.Payload["user_id"].(float64) != 123 {
		t.Errorf("Expected user_id=123, got %v", decoded.Payload["user_id"])
	}
	
	if decoded.Payload["role"] != "admin" {
		t.Errorf("Expected role=admin, got %v", decoded.Payload["role"])
	}
}

func TestValidateWithExpiration(t *testing.T) {
	secret := []byte("my-secret-key")
	jwt := NewJWTUtils(secret, WithExpiration(time.Hour))
	
	payload := map[string]interface{}{
		"user_id": 456,
	}
	
	token, err := jwt.Generate(payload)
	if err != nil {
		t.Fatalf("Failed to generate token: %v", err)
	}
	
	decoded, err := jwt.Validate(token)
	if err != nil {
		t.Fatalf("Failed to validate token: %v", err)
	}
	
	// Check that exp is set
	if decoded.Claims.ExpirationTime == 0 {
		t.Error("Expected expiration time to be set")
	}
	
	// Check that iat is set
	if decoded.Claims.IssuedAt == 0 {
		t.Error("Expected issued at time to be set")
	}
}

func TestValidateExpiredToken(t *testing.T) {
	secret := []byte("my-secret-key")
	jwt := NewJWTUtils(secret)
	
	// Create token with past expiration
	claims := Claims{
		ExpirationTime: time.Now().Add(-time.Hour).Unix(),
		IssuedAt:       time.Now().Add(-2 * time.Hour).Unix(),
	}
	
	payload := map[string]interface{}{
		"user_id": 789,
	}
	
	token, err := jwt.GenerateWithClaims(payload, claims)
	if err != nil {
		t.Fatalf("Failed to generate token: %v", err)
	}
	
	_, err = jwt.Validate(token)
	if err != ErrTokenExpired {
		t.Errorf("Expected ErrTokenExpired, got %v", err)
	}
}

func TestValidateNotBeforeToken(t *testing.T) {
	secret := []byte("my-secret-key")
	jwt := NewJWTUtils(secret)
	
	// Create token that is not valid yet
	claims := Claims{
		NotBefore: time.Now().Add(time.Hour).Unix(),
		IssuedAt:  time.Now().Unix(),
	}
	
	payload := map[string]interface{}{
		"user_id": 101,
	}
	
	token, err := jwt.GenerateWithClaims(payload, claims)
	if err != nil {
		t.Fatalf("Failed to generate token: %v", err)
	}
	
	_, err = jwt.Validate(token)
	if err != ErrTokenNotValidYet {
		t.Errorf("Expected ErrTokenNotValidYet, got %v", err)
	}
}

func TestValidateInvalidSignature(t *testing.T) {
	secret := []byte("my-secret-key")
	jwt := NewJWTUtils(secret)
	
	payload := map[string]interface{}{
		"user_id": 202,
	}
	
	token, err := jwt.Generate(payload)
	if err != nil {
		t.Fatalf("Failed to generate token: %v", err)
	}
	
	// Validate with different secret
	jwt2 := NewJWTUtils([]byte("different-secret"))
	_, err = jwt2.Validate(token)
	if err != ErrInvalidSignature {
		t.Errorf("Expected ErrInvalidSignature, got %v", err)
	}
}

func TestValidateInvalidTokenFormat(t *testing.T) {
	secret := []byte("my-secret-key")
	jwt := NewJWTUtils(secret)
	
	// Invalid token format
	_, err := jwt.Validate("invalid.token")
	if err != ErrInvalidTokenFormat {
		t.Errorf("Expected ErrInvalidTokenFormat, got %v", err)
	}
	
	// Empty token
	_, err = jwt.Validate("")
	if err != ErrInvalidTokenFormat {
		t.Errorf("Expected ErrInvalidTokenFormat, got %v", err)
	}
}

func TestParseWithoutValidation(t *testing.T) {
	secret := []byte("my-secret-key")
	jwt := NewJWTUtils(secret)
	
	payload := map[string]interface{}{
		"user_id": 303,
		"name":    "John Doe",
	}
	
	token, err := jwt.Generate(payload)
	if err != nil {
		t.Fatalf("Failed to generate token: %v", err)
	}
	
	// Parse without validation
	decoded, err := Parse(token)
	if err != nil {
		t.Fatalf("Failed to parse token: %v", err)
	}
	
	if decoded.Payload["user_id"].(float64) != 303 {
		t.Errorf("Expected user_id=303, got %v", decoded.Payload["user_id"])
	}
	
	if decoded.Payload["name"] != "John Doe" {
		t.Errorf("Expected name=John Doe, got %v", decoded.Payload["name"])
	}
}

func TestWithIssuer(t *testing.T) {
	secret := []byte("my-secret-key")
	jwt := NewJWTUtils(secret, WithIssuer("my-app"))
	
	payload := map[string]interface{}{
		"user_id": 404,
	}
	
	token, err := jwt.Generate(payload)
	if err != nil {
		t.Fatalf("Failed to generate token: %v", err)
	}
	
	decoded, err := jwt.Validate(token)
	if err != nil {
		t.Fatalf("Failed to validate token: %v", err)
	}
	
	if decoded.Claims.Issuer != "my-app" {
		t.Errorf("Expected issuer=my-app, got %v", decoded.Claims.Issuer)
	}
}

func TestTokenIsExpired(t *testing.T) {
	// Not expired token
	token := &Token{
		Claims: Claims{
			ExpirationTime: time.Now().Add(time.Hour).Unix(),
		},
	}
	if token.IsExpired() {
		t.Error("Token should not be expired")
	}
	
	// Expired token
	token = &Token{
		Claims: Claims{
			ExpirationTime: time.Now().Add(-time.Hour).Unix(),
		},
	}
	if !token.IsExpired() {
		t.Error("Token should be expired")
	}
	
	// No expiration
	token = &Token{
		Claims: Claims{},
	}
	if token.IsExpired() {
		t.Error("Token without expiration should not be considered expired")
	}
}

func TestGetClaim(t *testing.T) {
	token := &Token{
		Payload: map[string]interface{}{
			"user_id": float64(505),
			"role":    "user",
			"active":  true,
		},
	}
	
	userID, ok := token.GetClaim("user_id")
	if !ok {
		t.Error("Expected claim user_id to exist")
	}
	if userID.(float64) != 505 {
		t.Errorf("Expected user_id=505, got %v", userID)
	}
	
	role, ok := token.GetClaim("role")
	if !ok {
		t.Error("Expected claim role to exist")
	}
	if role != "user" {
		t.Errorf("Expected role=user, got %v", role)
	}
	
	_, ok = token.GetClaim("nonexistent")
	if ok {
		t.Error("Expected nonexistent claim to not exist")
	}
}

func TestCustomClaims(t *testing.T) {
	secret := []byte("my-secret-key")
	jwt := NewJWTUtils(secret)
	
	customClaims := Claims{
		Subject:  "user-123",
		Audience: "api.example.com",
		JWTID:    "unique-token-id",
	}
	
	payload := map[string]interface{}{
		"user_id": 606,
	}
	
	token, err := jwt.GenerateWithClaims(payload, customClaims)
	if err != nil {
		t.Fatalf("Failed to generate token: %v", err)
	}
	
	decoded, err := jwt.Validate(token)
	if err != nil {
		t.Fatalf("Failed to validate token: %v", err)
	}
	
	if decoded.Claims.Subject != "user-123" {
		t.Errorf("Expected subject=user-123, got %v", decoded.Claims.Subject)
	}
	
	if decoded.Claims.Audience != "api.example.com" {
		t.Errorf("Expected audience=api.example.com, got %v", decoded.Claims.Audience)
	}
	
	if decoded.Claims.JWTID != "unique-token-id" {
		t.Errorf("Expected JWTID=unique-token-id, got %v", decoded.Claims.JWTID)
	}
}

func TestComplexPayload(t *testing.T) {
	secret := []byte("my-secret-key")
	jwt := NewJWTUtils(secret)
	
	payload := map[string]interface{}{
		"user_id": 707,
		"profile": map[string]interface{}{
			"name":  "Alice",
			"email": "alice@example.com",
			"roles": []string{"admin", "user"},
		},
		"settings": map[string]interface{}{
			"theme":    "dark",
			"language": "en",
		},
	}
	
	token, err := jwt.Generate(payload)
	if err != nil {
		t.Fatalf("Failed to generate token: %v", err)
	}
	
	decoded, err := jwt.Validate(token)
	if err != nil {
		t.Fatalf("Failed to validate token: %v", err)
	}
	
	profile, ok := decoded.Payload["profile"].(map[string]interface{})
	if !ok {
		t.Fatal("Expected profile to be a map")
	}
	
	if profile["name"] != "Alice" {
		t.Errorf("Expected name=Alice, got %v", profile["name"])
	}
	
	settings, ok := decoded.Payload["settings"].(map[string]interface{})
	if !ok {
		t.Fatal("Expected settings to be a map")
	}
	
	if settings["theme"] != "dark" {
		t.Errorf("Expected theme=dark, got %v", settings["theme"])
	}
}

// Helper function
func splitToken(token string) []string {
	result := []string{}
	start := 0
	for i := 0; i < len(token); i++ {
		if token[i] == '.' {
			result = append(result, token[start:i])
			start = i + 1
		}
	}
	result = append(result, token[start:])
	return result
}

// Benchmark tests
func BenchmarkGenerate(b *testing.B) {
	secret := []byte("my-secret-key")
	jwt := NewJWTUtils(secret)
	payload := map[string]interface{}{
		"user_id": 123,
		"role":    "admin",
	}
	
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		jwt.Generate(payload)
	}
}

func BenchmarkValidate(b *testing.B) {
	secret := []byte("my-secret-key")
	jwt := NewJWTUtils(secret)
	payload := map[string]interface{}{
		"user_id": 123,
		"role":    "admin",
	}
	token, _ := jwt.Generate(payload)
	
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		jwt.Validate(token)
	}
}