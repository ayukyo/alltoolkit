// Example usage of license_key_utils package
package main

import (
	"fmt"
	"time"

	license "github.com/ayukyo/alltoolkit/Go/license_key_utils"
)

func main() {
	fmt.Println("=== License Key Utils Examples ===\n")

	// Example 1: Basic key generation
	fmt.Println("1. Basic Key Generation")
	fmt.Println("------------------------")
	key, _ := license.Generate()
	fmt.Printf("Generated key: %s\n\n", key)

	// Example 2: Different formats
	fmt.Println("2. Different Key Formats")
	fmt.Println("------------------------")

	// Standard format
	standardKey, _ := license.GenerateWithConfig(license.KeyConfig{
		Format:     license.FormatStandard,
		Segments:   4,
		SegmentLen: 4,
		Separator:  "-",
	})
	fmt.Printf("Standard:     %s\n", standardKey)

	// UUID format
	uuidKey, _ := license.GenerateWithConfig(license.KeyConfig{
		Format: license.FormatUUID,
	})
	fmt.Printf("UUID-style:   %s\n", uuidKey)

	// Compact format
	compactKey, _ := license.GenerateWithConfig(license.KeyConfig{
		Format:     license.FormatCompact,
		Segments:   4,
		SegmentLen: 4,
	})
	fmt.Printf("Compact:      %s\n\n", compactKey)

	// Example 3: Keys with prefix and suffix
	fmt.Println("3. Keys with Prefix/Suffix")
	fmt.Println("--------------------------")
	productKey, _ := license.GenerateWithConfig(license.KeyConfig{
		Format:     license.FormatStandard,
		Segments:   4,
		SegmentLen: 4,
		Separator:  "-",
		Prefix:     "PRO-",
		Suffix:     "-ENT",
	})
	fmt.Printf("Product key: %s\n\n", productKey)

	// Example 4: Keys with checksum
	fmt.Println("4. Keys with Checksum")
	fmt.Println("---------------------")
	config := license.KeyConfig{
		Format:     license.FormatStandard,
		Segments:   4,
		SegmentLen: 4,
		Separator:  "-",
		Secret:     "my-app-secret-2024",
	}

	keyWithChecksum, _ := license.GenerateWithChecksum(config)
	fmt.Printf("Key with checksum: %s\n", keyWithChecksum)

	err := license.ValidateChecksum(keyWithChecksum, config)
	if err == nil {
		fmt.Println("✓ Key validation passed")
	}

	// Tamper with key
	tamperedKey := keyWithChecksum[:len(keyWithChecksum)-1] + "X"
	err = license.ValidateChecksum(tamperedKey, config)
	if err == license.ErrInvalidChecksum {
		fmt.Println("✓ Tampered key detected")
	}
	fmt.Println()

	// Example 5: Product-bound keys
	fmt.Println("5. Product-Bound Keys")
	fmt.Println("----------------------")
	productID := "MYAPP-2024-PRO"
	proKey, _ := license.GenerateProductKey(productID, license.DefaultConfig())
	fmt.Printf("Product key: %s\n", proKey)

	err = license.ValidateProductKey(proKey, productID, license.DefaultConfig())
	if err == nil {
		fmt.Println("✓ Valid for product:", productID)
	}

	err = license.ValidateProductKey(proKey, "WRONG-PRODUCT", license.DefaultConfig())
	if err != nil {
		fmt.Println("✓ Invalid for other products")
	}
	fmt.Println()

	// Example 6: Keys with expiration
	fmt.Println("6. Keys with Expiration")
	fmt.Println("-------------------------")
	expiryKey, _ := license.GenerateWithExpiry(license.DefaultConfig(), 30)
	fmt.Printf("Key with expiry: %s\n", expiryKey)

	err = license.ValidateExpiry(expiryKey, license.DefaultConfig())
	if err == nil {
		fmt.Println("✓ Key is valid (not expired)")
	}
	fmt.Println()

	// Example 7: Batch generation
	fmt.Println("7. Batch Key Generation")
	fmt.Println("-------------------------")
	batchKeys, _ := license.GenerateBatch(5, license.DefaultConfig())
	fmt.Println("Generated 5 unique keys:")
	for i, k := range batchKeys {
		fmt.Printf("  %d. %s\n", i+1, k)
	}
	fmt.Println()

	// Example 8: Key masking
	fmt.Println("8. Key Masking (for display)")
	fmt.Println("-----------------------------")
	fullKey := "ABCD-EFGH-IJKL-MNOP"
	maskedKey := license.MaskKey(fullKey, license.DefaultConfig())
	fmt.Printf("Original: %s\n", fullKey)
	fmt.Printf("Masked:   %s\n\n", maskedKey)

	// Example 9: Key parsing
	fmt.Println("9. Key Parsing")
	fmt.Println("----------------")
	parsedKey, _ := license.ParseKey("ABCD-EFGH-IJKL-MNOP")
	fmt.Printf("Key:         %s\n", parsedKey.Key)
	fmt.Printf("Format:      %s\n", parsedKey.Metadata["format"])
	fmt.Printf("Issue Date:  %s\n", parsedKey.IssueDate.Format(time.RFC3339))
	fmt.Println()

	// Example 10: Custom segment configuration
	fmt.Println("10. Custom Configuration")
	fmt.Println("-------------------------")
	customKey, _ := license.GenerateWithConfig(license.KeyConfig{
		Format:     license.FormatCustom,
		Segments:   6,
		SegmentLen: 3,
		Separator:  ".",
		Prefix:     "LICENSE-",
	})
	fmt.Printf("Custom key: %s\n\n", customKey)

	// Example 11: Enterprise license generation
	fmt.Println("11. Enterprise License Example")
	fmt.Println("-------------------------------")
	enterpriseConfig := license.KeyConfig{
		Format:     license.FormatStandard,
		Segments:   5,
		SegmentLen: 4,
		Separator:  "-",
		Prefix:     "ENT-",
		Secret:     "enterprise-secret-2024",
	}

	// Generate enterprise license
	entLicense, _ := license.GenerateWithChecksum(enterpriseConfig)
	fmt.Printf("Enterprise License: %s\n", entLicense)
	fmt.Printf("Valid until: %s\n", time.Now().AddDate(1, 0, 0).Format("2006-01-02"))
	fmt.Println("Max activations: 100")

	fmt.Println("\n=== All examples completed ===")
}