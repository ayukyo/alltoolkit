// Example usage of credit_card_utils package
package main

import (
	"fmt"
	"strings"

	creditcard "github.com/ayukyo/alltoolkit/Go/credit_card_utils"
)

func main() {
	fmt.Println(strings.Repeat("=", 60))
	fmt.Println("Credit Card Utils - Examples")
	fmt.Println(strings.Repeat("=", 60))

	// Example 1: Basic Card Validation
	fmt.Println("\n📋 Example 1: Basic Card Validation")
	fmt.Println(strings.Repeat("-", 40))
	exampleCard := "4111111111111111"
	fmt.Printf("Card Number: %s\n", creditcard.FormatCardNumber(exampleCard))
	fmt.Printf("Valid (Luhn): %v\n", creditcard.LuhnCheck(exampleCard))
	fmt.Printf("Card Type: %s\n", creditcard.IdentifyCardType(exampleCard))
	fmt.Printf("Overall Valid: %v\n", creditcard.IsValidCardNumber(exampleCard))

	// Example 2: Card Type Identification
	fmt.Println("\n📋 Example 2: Card Type Identification")
	fmt.Println(strings.Repeat("-", 40))
	cards := []string{
		"4111111111111111", // Visa
		"5500000000000004", // Mastercard
		"378282246310005",  // Amex
		"6011111111111117", // Discover
		"3530111333300000", // JCB
		"30000000000004",   // Diners Club
		"6221260000000000", // UnionPay
	}

	for _, card := range cards {
		info := creditcard.GetCardInfo(card)
		fmt.Printf("%s → %s (Valid: %v)\n",
			creditcard.FormatCardNumber(card),
			info.Type,
			info.Valid)
	}

	// Example 3: Card Formatting and Masking
	fmt.Println("\n📋 Example 3: Card Formatting and Masking")
	fmt.Println(strings.Repeat("-", 40))
	rawCard := "4111111111111111"
	fmt.Printf("Raw: %s\n", rawCard)
	fmt.Printf("Formatted: %s\n", creditcard.FormatCardNumber(rawCard))

	// Custom formatting (e.g., Amex style: 4-6-5)
	amexCard := "378282246310005"
	fmt.Printf("Amex (default): %s\n", creditcard.FormatCardNumber(amexCard))
	fmt.Printf("Amex (custom): %s\n", creditcard.FormatCardNumberCustom(amexCard, []int{4, 6, 5}))

	// Masking
	fmt.Printf("Masked (default): %s\n", creditcard.MaskCardNumberDefault(rawCard))
	fmt.Printf("Masked (first 6, last 4): %s\n", creditcard.MaskCardNumber(rawCard, 6, 4))

	// Example 4: Luhn Algorithm Details
	fmt.Println("\n📋 Example 4: Luhn Algorithm")
	fmt.Println(strings.Repeat("-", 40))
	partialNumber := "411111111111111"
	checkDigit := creditcard.CalculateLuhnDigit(partialNumber)
	fullNumber := partialNumber + string(rune('0'+checkDigit))
	fmt.Printf("Partial number: %s\n", partialNumber)
	fmt.Printf("Calculated check digit: %d\n", checkDigit)
	fmt.Printf("Full valid number: %s\n", fullNumber)
	fmt.Printf("Luhn check: %v\n", creditcard.LuhnCheck(fullNumber))

	// Example 5: CVV and Expiry Validation
	fmt.Println("\n📋 Example 5: CVV and Expiry Validation")
	fmt.Println(strings.Repeat("-", 40))

	// CVV validation
	visaCard := "4111111111111111"
	fmt.Printf("Visa CVV '123' valid: %v\n", creditcard.IsValidCVVForNumber("123", visaCard))
	fmt.Printf("Visa CVV '1234' valid: %v\n", creditcard.IsValidCVVForNumber("1234", visaCard))

	amexCard2 := "378282246310005"
	fmt.Printf("Amex CVV '1234' valid: %v\n", creditcard.IsValidCVVForNumber("1234", amexCard2))
	fmt.Printf("Amex CVV '123' valid: %v\n", creditcard.IsValidCVVForNumber("123", amexCard2))

	// Expiry validation
	expiries := []string{"12/25", "01/26", "13/25", "00/25"}
	for _, exp := range expiries {
		fmt.Printf("Expiry '%s' valid: %v\n", exp, creditcard.IsValidExpiryDate(exp))
	}

	// Example 6: Complete Card Validation
	fmt.Println("\n📋 Example 6: Complete Card Validation")
	fmt.Println(strings.Repeat("-", 40))

	testCards := []struct {
		number string
		cvv    string
		expiry string
	}{
		{"4111111111111111", "123", "12/25"},
		{"5500000000000004", "123", "12/25"},
		{"378282246310005", "1234", "12/25"},
		{"4111111111111112", "123", "12/25"}, // Invalid Luhn
		{"4111111111111111", "1234", "12/25"}, // Wrong CVV length
	}

	for _, tc := range testCards {
		result := creditcard.ValidateCard(tc.number, tc.cvv, tc.expiry)
		fmt.Printf("\nCard: %s\n", creditcard.MaskCardNumberDefault(tc.number))
		fmt.Printf("  Type: %s\n", result.CardType)
		fmt.Printf("  Luhn Valid: %v\n", result.LuhnValid)
		fmt.Printf("  Length Valid: %v\n", result.LengthValid)
		fmt.Printf("  CVV Valid: %v\n", result.CVVValid)
		fmt.Printf("  Expiry Valid: %v\n", result.ExpiryValid)
		fmt.Printf("  Overall Valid: %v\n", result.Valid)
		if len(result.Errors) > 0 {
			fmt.Printf("  Errors: %v\n", result.Errors)
		}
	}

	// Example 7: Test Card Generation
	fmt.Println("\n📋 Example 7: Test Card Generation")
	fmt.Println(strings.Repeat("-", 40))

	cardTypes := []creditcard.CardType{
		creditcard.CardTypeVisa,
		creditcard.CardTypeMastercard,
		creditcard.CardTypeAmex,
		creditcard.CardTypeDiscover,
		creditcard.CardTypeJCB,
	}

	for _, ct := range cardTypes {
		number, cvv, expiry := creditcard.GenerateTestCard(ct)
		fmt.Printf("\n%s:\n", ct)
		fmt.Printf("  Number: %s\n", creditcard.FormatCardNumber(number))
		fmt.Printf("  CVV: %s\n", cvv)
		fmt.Printf("  Expiry: %s\n", expiry)

		// Verify generated card
		result := creditcard.ValidateCard(number, cvv, expiry)
		fmt.Printf("  Valid: %v\n", result.Valid)
	}

	// Example 8: Detailed Card Information
	fmt.Println("\n📋 Example 8: Detailed Card Information")
	fmt.Println(strings.Repeat("-", 40))

	card := "4111111111111111"
	info := creditcard.GetCardInfo(card)
	fmt.Printf("Card Number: %s\n", info.Formatted)
	fmt.Printf("Card Type: %s\n", info.Type)
	fmt.Printf("IIN (First 6): %s\n", info.IIN)
	fmt.Printf("Length: %d\n", info.Length)
	fmt.Printf("CVV Length: %d\n", info.CVVLength)
	fmt.Printf("Valid: %v\n", info.Valid)
	fmt.Printf("Networks: %v\n", info.Networks)

	// Example 9: Card Comparison (Masked vs Full)
	fmt.Println("\n📋 Example 9: Card Comparison")
	fmt.Println(strings.Repeat("-", 40))

	fullNumber = "4111111111111111"
	maskedNumber := "4111********1111"
	fmt.Printf("Full: %s\n", fullNumber)
	fmt.Printf("Masked: %s\n", maskedNumber)
	fmt.Printf("Match: %v\n", creditcard.CompareCards(fullNumber, maskedNumber))

	// Example 10: Practical Use Case - Payment Form
	fmt.Println("\n📋 Example 10: Practical Use Case - Payment Form Validation")
	fmt.Println(strings.Repeat("-", 40))

	type PaymentForm struct {
		CardNumber string
		CVV        string
		Expiry     string
	}

	forms := []PaymentForm{
		{"4111-1111-1111-1111", "123", "12/25"},
		{"5500-0000-0000-0004", "123", "12/25"},
		{"3782-8224-6310-005", "1234", "12/25"},
		{"1234-5678-9012-3456", "123", "12/25"}, // Invalid card
	}

	for i, form := range forms {
		fmt.Printf("\nForm %d:\n", i+1)
		fmt.Printf("  Card: %s\n", creditcard.MaskCardNumberDefault(form.CardNumber))
		fmt.Printf("  Type: %s\n", creditcard.IdentifyCardType(form.CardNumber))

		result := creditcard.ValidateCard(form.CardNumber, form.CVV, form.Expiry)
		if result.Valid {
			fmt.Printf("  ✅ Valid payment information\n")
		} else {
			fmt.Printf("  ❌ Invalid: %v\n", result.Errors)
		}
	}

	fmt.Println("\n" + strings.Repeat("=", 60))
	fmt.Println("All examples completed!")
	fmt.Println(strings.Repeat("=", 60))
}