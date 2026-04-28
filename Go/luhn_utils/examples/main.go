// Example application demonstrating Luhn algorithm utilities
package main

import (
	"fmt"
	
	"github.com/ayukyo/alltoolkit/Go/luhn_utils"
)

func main() {
	fmt.Println("=== Luhn Algorithm Utilities Demo ===")
	fmt.Println()
	
	// 1. Validation Examples
	fmt.Println("--- Validation Examples ---")
	testNumbers := []struct {
		name   string
		number string
	}{
		{"Valid Visa", "4532015112830366"},
		{"Valid MasterCard", "5500000000000004"},
		{"Valid Amex", "378282246310005"},
		{"Invalid (wrong check digit)", "4532015112830367"},
		{"With formatting", "4532-0151-1283-0366"},
	}
	
	for _, tt := range testNumbers {
		valid := luhn_utils.Validate(tt.number)
		status := "✓ Valid"
		if !valid {
			status = "✗ Invalid"
		}
		fmt.Printf("  %s: %s -> %s\n", tt.name, tt.number, status)
	}
	fmt.Println()
	
	// 2. Check Digit Calculation
	fmt.Println("--- Check Digit Calculation ---")
	partial := "453201511283036"
	checkDigit, err := luhn_utils.CalculateCheckDigit(partial)
	if err != nil {
		fmt.Printf("  Error: %v\n", err)
	} else {
		fmt.Printf("  Partial number: %s\n", partial)
		fmt.Printf("  Check digit: %d\n", checkDigit)
		
		full, _ := luhn_utils.AddCheckDigit(partial)
		fmt.Printf("  Full number: %s\n", full)
		fmt.Printf("  Validation: %v\n", luhn_utils.Validate(full))
	}
	fmt.Println()
	
	// 3. Number Formatting
	fmt.Println("--- Number Formatting ---")
	raw := "4532015112830366"
	fmt.Printf("  Raw: %s\n", raw)
	fmt.Printf("  With spaces: %s\n", luhn_utils.FormatNumber(raw, 4, " "))
	fmt.Printf("  With dashes: %s\n", luhn_utils.FormatNumber(raw, 4, "-"))
	fmt.Printf("  With dots: %s\n", luhn_utils.FormatNumber(raw, 4, "."))
	
	formatted := "4532-0151-1283-0366"
	fmt.Printf("  Stripped: %s -> %s\n", formatted, luhn_utils.StripFormatting(formatted))
	fmt.Println()
	
	// 4. Generate Test Numbers
	fmt.Println("--- Generate Test Numbers ---")
	
	// Generate single numbers
	visa, _ := luhn_utils.GenerateValidNumber("4", 16)
	mastercard, _ := luhn_utils.GenerateValidNumber("5", 16)
	amex, _ := luhn_utils.GenerateValidNumber("34", 15)
	
	fmt.Printf("  Visa (16 digits): %s (valid: %v)\n", visa, luhn_utils.Validate(visa))
	fmt.Printf("  MasterCard (16 digits): %s (valid: %v)\n", mastercard, luhn_utils.Validate(mastercard))
	fmt.Printf("  Amex (15 digits): %s (valid: %v)\n", amex, luhn_utils.Validate(amex))
	fmt.Println()
	
	// 5. Generate Batch
	fmt.Println("--- Generate Batch ---")
	batch, _ := luhn_utils.GenerateBatch("4", 3, 16)
	fmt.Printf("  Generated %d Visa-like numbers:\n", len(batch))
	for i, num := range batch {
		fmt.Printf("    %d: %s (valid: %v)\n", i+1, num, luhn_utils.Validate(num))
	}
	fmt.Println()
	
	// 6. Generate Test Credit Cards
	fmt.Println("--- Test Credit Cards by Type ---")
	cards := luhn_utils.GenerateTestCreditCards(1)
	fmt.Printf("  Generated %d test cards:\n", len(cards))
	for _, card := range cards {
		fmt.Printf("    %-12s: %s\n", card.Type, card.Number)
	}
	fmt.Println()
	
	// 7. Card Type Identification
	fmt.Println("--- Card Type Identification ---")
	identifyTests := []string{
		"4111111111111111",
		"5500000000000004",
		"378282246310005",
		"6011111111111117",
		"3530111333300000",
	}
	
	for _, num := range identifyTests {
		cardType := luhn_utils.IdentifyCardType(num)
		fmt.Printf("  %s -> %s\n", num, cardType)
	}
	fmt.Println()
	
	// 8. Luhn Sum Calculation
	fmt.Println("--- Luhn Sum Calculation ---")
	validNum := "4532015112830366"
	invalidNum := "4532015112830367"
	
	sum, valid := luhn_utils.CalculateLuhnSum(validNum)
	fmt.Printf("  %s: sum=%d, valid=%v\n", validNum, sum, valid)
	
	sum, valid = luhn_utils.CalculateLuhnSum(invalidNum)
	fmt.Printf("  %s: sum=%d, valid=%v\n", invalidNum, sum, valid)
	fmt.Println()
	
	// 9. Find Check Digit Errors
	fmt.Println("--- Find Check Digit Errors ---")
	invalidNumber := "4532015112830367"
	errors := luhn_utils.FindCheckDigitErrors(invalidNumber)
	if len(errors) > 0 {
		fmt.Printf("  Number: %s\n", invalidNumber)
		fmt.Printf("  Potential error positions: %v\n", errors)
		fmt.Printf("  (0-indexed from left)\n")
	} else {
		fmt.Printf("  Number is valid or has multiple errors\n")
	}
	fmt.Println()
	
	// 10. Validator Class
	fmt.Println("--- Validator Class ---")
	v := luhn_utils.NewValidator(4, " ")
	
	fmt.Printf("  Validate: %v\n", v.Validate("4532015112830366"))
	
	digit, _ := v.CalculateCheckDigit("453201511283036")
	fmt.Printf("  Check digit for '453201511283036': %d\n", digit)
	
	full, _ := v.AddCheckDigit("453201511283036")
	fmt.Printf("  Full number: %s\n", full)
	
	fmt.Printf("  Formatted: %s\n", v.Format(full))
	
	genNum, _ := v.Generate("4", 16)
	fmt.Printf("  Generated Visa: %s\n", genNum)
	fmt.Println()
	
	// 11. Summary Statistics
	fmt.Println("--- Summary ---")
	fmt.Printf("  Total card types supported: %d\n", countCardTypes())
	fmt.Println()
	
	fmt.Println("=== Demo Complete ===")
}

func countCardTypes() int {
	// Count unique card types from test generation
	cards := luhn_utils.GenerateTestCreditCards(1)
	types := make(map[string]bool)
	for _, card := range cards {
		types[card.Type] = true
	}
	return len(types)
}