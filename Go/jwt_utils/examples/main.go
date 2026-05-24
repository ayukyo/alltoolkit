// Example usage of jwt_utils package
package main

import (
	"fmt"
	"time"

	"github.com/ayukyo/alltoolkit/Go/jwt_utils"
)

func main() {
	fmt.Println("=== JWT Utils Examples ===\n")

	// Example 1: Basic token generation and validation
	basicExample()

	// Example 2: Token with custom claims
	customClaimsExample()

	// Example 3: Token with expiration
	expirationExample()

	// Example 4: Token with issuer
	issuerExample()

	// Example 5: Parse without validation
	parseExample()

	// Example 6: Check token expiration
	checkExpirationExample()

	// Example 7: Complex payload
	complexPayloadExample()

	// Example 8: Error handling
	errorHandlingExample()
}

func basicExample() {
	fmt.Println("--- Example 1: Basic Token ---")
	
	// Create JWT utility with secret key
	secret := []byte("my-super-secret-key")
	jwt := jwt_utils.NewJWTUtils(secret)
	
	// Define payload
	payload := map[string]interface{}{
		"user_id": 12345,
		"username": "john_doe",
		"role":     "admin",
	}
	
	// Generate token
	token, err := jwt.Generate(payload)
	if err != nil {
		fmt.Printf("Error generating token: %v\n", err)
		return
	}
	fmt.Printf("Generated Token: %s\n\n", token)
	
	// Validate token
	decoded, err := jwt.Validate(token)
	if err != nil {
		fmt.Printf("Error validating token: %v\n", err)
		return
	}
	
	fmt.Printf("Validation successful!\n")
	fmt.Printf("  User ID: %v\n", decoded.Payload["user_id"])
	fmt.Printf("  Username: %v\n", decoded.Payload["username"])
	fmt.Printf("  Role: %v\n", decoded.Payload["role"])
	fmt.Printf("  Issued At: %v\n\n", decoded.Claims.IssuedAt)
}

func customClaimsExample() {
	fmt.Println("--- Example 2: Custom Claims ---")
	
	secret := []byte("my-super-secret-key")
	jwt := jwt_utils.NewJWTUtils(secret)
	
	// Define custom claims
	claims := jwt_utils.Claims{
		Subject:  "user-12345",
		Audience: "api.myapp.com",
		JWTID:    "unique-identifier-001",
	}
	
	payload := map[string]interface{}{
		"user_id": 12345,
	}
	
	// Generate token with custom claims
	token, _ := jwt.GenerateWithClaims(payload, claims)
	fmt.Printf("Token with Custom Claims: %s...\n", token[:50])
	
	decoded, _ := jwt.Validate(token)
	fmt.Printf("Subject: %s\n", decoded.Claims.Subject)
	fmt.Printf("Audience: %s\n", decoded.Claims.Audience)
	fmt.Printf("JWT ID: %s\n\n", decoded.Claims.JWTID)
}

func expirationExample() {
	fmt.Println("--- Example 3: Token with Expiration ---")
	
	secret := []byte("my-super-secret-key")
	// Set token to expire in 1 hour
	jwt := jwt_utils.NewJWTUtils(secret, jwt_utils.WithExpiration(time.Hour))
	
	payload := map[string]interface{}{
		"user_id": 67890,
	}
	
	token, _ := jwt.Generate(payload)
	decoded, _ := jwt.Validate(token)
	
	expTime := time.Unix(decoded.Claims.ExpirationTime, 0)
	fmt.Printf("Token expires at: %s\n", expTime.Format(time.RFC3339))
	fmt.Printf("Issued at: %s\n\n", time.Unix(decoded.Claims.IssuedAt, 0).Format(time.RFC3339))
}

func issuerExample() {
	fmt.Println("--- Example 4: Token with Issuer ---")
	
	secret := []byte("my-super-secret-key")
	jwt := jwt_utils.NewJWTUtils(secret, 
		jwt_utils.WithIssuer("my-auth-service"),
		jwt_utils.WithExpiration(24*time.Hour),
	)
	
	payload := map[string]interface{}{
		"user_id": 11111,
	}
	
	token, _ := jwt.Generate(payload)
	decoded, _ := jwt.Validate(token)
	
	fmt.Printf("Issuer: %s\n\n", decoded.Claims.Issuer)
}

func parseExample() {
	fmt.Println("--- Example 5: Parse Without Validation ---")
	
	secret := []byte("my-super-secret-key")
	jwt := jwt_utils.NewJWTUtils(secret)
	
	payload := map[string]interface{}{
		"user_id": 22222,
		"role":    "viewer",
	}
	
	token, _ := jwt.Generate(payload)
	
	// Parse without validating signature
	decoded, err := jwt_utils.Parse(token)
	if err != nil {
		fmt.Printf("Parse error: %v\n", err)
		return
	}
	
	fmt.Printf("Parsed Token (no validation):\n")
	fmt.Printf("  Algorithm: %s\n", decoded.Header.Alg)
	fmt.Printf("  Type: %s\n", decoded.Header.Typ)
	fmt.Printf("  User ID: %v\n", decoded.Payload["user_id"])
	fmt.Printf("  Role: %v\n\n", decoded.Payload["role"])
}

func checkExpirationExample() {
	fmt.Println("--- Example 6: Check Token Expiration ---")
	
	// Create token that's already expired
	secret := []byte("my-super-secret-key")
	jwt := jwt_utils.NewJWTUtils(secret)
	
	claims := jwt_utils.Claims{
		ExpirationTime: time.Now().Add(-time.Hour).Unix(),
	}
	
	token, _ := jwt.GenerateWithClaims(map[string]interface{}{"user_id": 1}, claims)
	
	// Parse and check expiration
	decoded, _ := jwt_utils.Parse(token)
	if decoded.IsExpired() {
		fmt.Println("Token is expired!")
	}
	
	// Try to validate - should fail
	_, err := jwt.Validate(token)
	if err == jwt_utils.ErrTokenExpired {
		fmt.Println("Validation correctly returned: token expired\n")
	}
}

func complexPayloadExample() {
	fmt.Println("--- Example 7: Complex Payload ---")
	
	secret := []byte("my-super-secret-key")
	jwt := jwt_utils.NewJWTUtils(secret)
	
	payload := map[string]interface{}{
		"user_id": 33333,
		"profile": map[string]interface{}{
			"name":  "Jane Smith",
			"email": "jane@example.com",
			"age":   28,
		},
		"permissions": []string{"read", "write", "delete"},
		"metadata": map[string]interface{}{
			"created_at": time.Now().Unix(),
			"source":     "mobile-app",
		},
	}
	
	token, _ := jwt.Generate(payload)
	decoded, _ := jwt.Validate(token)
	
	fmt.Printf("Complex Payload:\n")
	if profile, ok := decoded.Payload["profile"].(map[string]interface{}); ok {
		fmt.Printf("  Profile Name: %v\n", profile["name"])
		fmt.Printf("  Profile Email: %v\n", profile["email"])
	}
	if metadata, ok := decoded.Payload["metadata"].(map[string]interface{}); ok {
		fmt.Printf("  Source: %v\n", metadata["source"])
	}
	fmt.Println()
}

func errorHandlingExample() {
	fmt.Println("--- Example 8: Error Handling ---")
	
	secret := []byte("my-super-secret-key")
	jwt := jwt_utils.NewJWTUtils(secret)
	
	// Invalid token format
	_, err := jwt.Validate("invalid-token-format")
	if err == jwt_utils.ErrInvalidTokenFormat {
		fmt.Println("Caught: Invalid token format")
	}
	
	// Wrong secret
	token, _ := jwt.Generate(map[string]interface{}{"user_id": 1})
	jwt2 := jwt_utils.NewJWTUtils([]byte("wrong-secret"))
	_, err = jwt2.Validate(token)
	if err == jwt_utils.ErrInvalidSignature {
		fmt.Println("Caught: Invalid signature (wrong secret)")
	}
	
	// Expired token
	claims := jwt_utils.Claims{
		ExpirationTime: time.Now().Add(-time.Hour).Unix(),
	}
	expiredToken, _ := jwt.GenerateWithClaims(map[string]interface{}{"user_id": 1}, claims)
	_, err = jwt.Validate(expiredToken)
	if err == jwt_utils.ErrTokenExpired {
		fmt.Println("Caught: Token expired\n")
	}
}