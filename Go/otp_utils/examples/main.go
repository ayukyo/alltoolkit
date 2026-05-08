package main

import (
	"fmt"
	"time"

	"github.com/ayukyo/alltoolkit/Go/otp_utils"
)

func main() {
	fmt.Println("=== OTP/TOTP/HOTP Utilities Demo ===")
	fmt.Println()

	// 1. Generate a new secret
	fmt.Println("1. Secret Generation")
	fmt.Println("---------------------")
	secret, err := otp_utils.GenerateSecret(20)
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		return
	}
	fmt.Printf("Generated Secret: %s\n", secret)
	fmt.Printf("Secret Length: %d characters\n\n", len(secret))

	// 2. TOTP Generation
	fmt.Println("2. TOTP (Time-based One-Time Password)")
	fmt.Println("---------------------------------------")
	config := &otp_utils.OTPConfig{
		Secret:      secret,
		Digits:      6,
		Algorithm:   otp_utils.AlgorithmSHA1,
		Period:      30,
		Skew:        1,
		Issuer:      "MyApp",
		AccountName: "user@example.com",
	}

	// Generate current TOTP code
	code, err := otp_utils.GenerateTOTPWithConfig(config)
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		return
	}
	fmt.Printf("Current TOTP Code: %s\n", otp_utils.FormatCode(code, " "))

	// Get time remaining
	info := otp_utils.GetTOTPInfo(30)
	fmt.Printf("Time Remaining: %d seconds\n", info.TimeRemaining)
	fmt.Printf("Progress: %.1f%%\n", info.Progress)
	fmt.Printf("Expires At: %s\n\n", info.ExpiresAt.Format("15:04:05"))

	// 3. TOTP Validation
	fmt.Println("3. TOTP Validation")
	fmt.Println("------------------")
	valid, err := otp_utils.ValidateTOTPWithConfig(config, code)
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		return
	}
	fmt.Printf("Code '%s' is valid: %v\n\n", code, valid)

	// Wrong code should fail
	valid, _ = otp_utils.ValidateTOTPWithConfig(config, "000000")
	fmt.Printf("Code '000000' is valid: %v\n\n", valid)

	// 4. Auth URL Generation (for QR codes)
	fmt.Println("4. Authenticator App URL")
	fmt.Println("-------------------------")
	authURL, err := otp_utils.GenerateTOTPAuthURL(config)
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		return
	}
	fmt.Printf("OTP Auth URL: %s\n\n", authURL)

	// 5. Parse Auth URL
	fmt.Println("5. Parse Auth URL")
	fmt.Println("-----------------")
	parsedConfig, typ, err := otp_utils.ParseOTPAuthURL(authURL)
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		return
	}
	fmt.Printf("Type: %s\n", typ)
	fmt.Printf("Secret: %s\n", parsedConfig.Secret)
	fmt.Printf("Issuer: %s\n", parsedConfig.Issuer)
	fmt.Printf("Account: %s\n\n", parsedConfig.AccountName)

	// 6. HOTP (Counter-based)
	fmt.Println("6. HOTP (HMAC-based One-Time Password)")
	fmt.Println("----------------------------------------")
	counter := uint64(0)
	hotpCode, err := otp_utils.GenerateHOTP(secret, counter, 6)
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		return
	}
	fmt.Printf("HOTP Code (counter=%d): %s\n", counter, hotpCode)

	// Next counter gives different code
	hotpCode2, _ := otp_utils.GenerateHOTP(secret, counter+1, 6)
	fmt.Printf("HOTP Code (counter=%d): %s\n\n", counter+1, hotpCode2)

	// 7. Different Algorithms
	fmt.Println("7. Different Hash Algorithms")
	fmt.Println("-----------------------------")
	algorithms := []otp_utils.Algorithm{
		otp_utils.AlgorithmSHA1,
		otp_utils.AlgorithmSHA256,
		otp_utils.AlgorithmSHA512,
	}

	for _, algo := range algorithms {
		config.Algorithm = algo
		code, _ := otp_utils.GenerateTOTPWithConfig(config)
		fmt.Printf("%-10s: %s\n", algo.String(), code)
	}
	fmt.Println()

	// 8. Different Digit Counts
	fmt.Println("8. Different Digit Counts")
	fmt.Println("-------------------------")
	config.Algorithm = otp_utils.AlgorithmSHA1
	for _, digits := range []int{6, 8} {
		config.Digits = digits
		code, _ := otp_utils.GenerateTOTPWithConfig(config)
		fmt.Printf("%d digits: %s\n", digits, code)
	}
	fmt.Println()

	// 9. Backup/Recovery Codes
	fmt.Println("9. Backup/Recovery Codes")
	fmt.Println("------------------------")
	backupCodes, err := otp_utils.CalculateBackupCodes(10, 8)
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		return
	}
	fmt.Println("Generated backup codes:")
	for i, code := range backupCodes {
		fmt.Printf("  %2d: %s\n", i+1, code)
	}
	fmt.Println()

	// 10. Real-world Example: 2FA Setup
	fmt.Println("10. Real-world Example: 2FA Setup")
	fmt.Println("---------------------------------")
	setup2FA()

	// 11. Continuous TOTP Display
	fmt.Println("\n11. Live TOTP Demo (10 seconds)")
	fmt.Println("--------------------------------")
	liveTOTPDemo(secret)
}

func setup2FA() {
	// Step 1: Generate secret
	secret, _ := otp_utils.GenerateSecret(20)
	fmt.Printf("Step 1: Secret generated: %s\n", secret)

	// Step 2: Create configuration
	config := &otp_utils.OTPConfig{
		Secret:      secret,
		Issuer:      "MySecureApp",
		AccountName: "john.doe@example.com",
		Digits:      6,
		Period:      30,
		Algorithm:   otp_utils.AlgorithmSHA1,
	}
	fmt.Printf("Step 2: Configuration created\n")

	// Step 3: Generate QR code URL
	url, _ := otp_utils.GenerateTOTPAuthURL(config)
	fmt.Printf("Step 3: Scan this URL with authenticator app:\n")
	fmt.Printf("        %s\n", url)

	// Step 4: Generate backup codes
	backupCodes, _ := otp_utils.CalculateBackupCodes(10, 8)
	fmt.Printf("Step 4: Backup codes generated (%d codes)\n", len(backupCodes))

	// Step 5: Validate a code
	code, _ := otp_utils.GenerateTOTPWithConfig(config)
	fmt.Printf("Step 5: Current code is %s, validating...\n", code)
	valid, _ := otp_utils.ValidateTOTPWithConfig(config, code)
	fmt.Printf("        Validation result: %v\n", valid)
}

func liveTOTPDemo(secret string) {
	config := &otp_utils.OTPConfig{
		Secret:    secret,
		Digits:    6,
		Period:    30,
		Algorithm: otp_utils.AlgorithmSHA1,
	}

	for i := 0; i < 10; i++ {
		code, _ := otp_utils.GenerateTOTPWithConfig(config)
		info := otp_utils.GetTOTPInfo(30)
		fmt.Printf("\rCode: %s | Remaining: %2ds | Progress: [%-20s] %.0f%%",
			code,
			info.TimeRemaining,
			generateProgress(info.Progress),
			info.Progress,
		)
		time.Sleep(1 * time.Second)
	}
	fmt.Println()
}

func generateProgress(percent float64) string {
	filled := int(percent / 5)
	bar := ""
	for i := 0; i < 20; i++ {
		if i < filled {
			bar += "█"
		} else {
			bar += "░"
		}
	}
	return bar
}