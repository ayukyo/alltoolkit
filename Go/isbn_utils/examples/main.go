// Example usage of isbn_utils package
package main

import (
	"fmt"
	"log"
	
	isbn_utils "github.com/ayukyo/alltoolkit/go/isbn_utils"
)

func main() {
	fmt.Println("=== ISBN Utilities Demo ===")
	fmt.Println()
	
	// 1. ISBN Validation
	fmt.Println("--- ISBN Validation ---")
	
	isbns := []string{
		"0306406152",        // Valid ISBN-10
		"9783161484100",     // Valid ISBN-13
		"0-306-40615-2",     // Valid ISBN-10 with hyphens
		"080442957X",        // Valid ISBN-10 with X check digit
		"978-3-16-148410-0",  // Valid ISBN-13 with hyphens
		"123456789",         // Invalid - too short
		"0306406153",        // Invalid - wrong check digit
	}
	
	for _, isbn := range isbns {
		valid, err := isbn_utils.Validate(isbn)
		if valid {
			fmt.Printf("✓ %s is valid\n", isbn)
		} else {
			fmt.Printf("✗ %s is invalid: %v\n", isbn, err)
		}
	}
	fmt.Println()
	
	// 2. ISBN Type Detection
	fmt.Println("--- ISBN Type Detection ---")
	
	examples := []string{"0306406152", "9783161484100"}
	for _, ex := range examples {
		isbnType, err := isbn_utils.GetType(ex)
		if err != nil {
			log.Printf("Error getting type for %s: %v\n", ex, err)
			continue
		}
		fmt.Printf("ISBN %s is type: %s\n", ex, isbnType)
	}
	fmt.Println()
	
	// 3. ISBN Conversion
	fmt.Println("--- ISBN Conversion ---")
	
	// ISBN-10 to ISBN-13
	isbn10 := "0306406152"
	isbn13, err := isbn_utils.ToISBN13(isbn10)
	if err != nil {
		log.Printf("Error converting %s: %v\n", isbn10, err)
	} else {
		fmt.Printf("ISBN-10 %s → ISBN-13 %s\n", isbn10, isbn13)
	}
	
	// ISBN-13 to ISBN-10
	isbn13Input := "9780306406157"
	isbn10Result, err := isbn_utils.ToISBN10(isbn13Input)
	if err != nil {
		log.Printf("Error converting %s: %v\n", isbn13Input, err)
	} else {
		fmt.Printf("ISBN-13 %s → ISBN-10 %s\n", isbn13Input, isbn10Result)
	}
	fmt.Println()
	
	// 4. Check Digit Generation
	fmt.Println("--- Check Digit Generation ---")
	
	// Generate check digit for ISBN-10
	check10, err := isbn_utils.GenerateCheckDigit10("030640615")
	if err != nil {
		log.Printf("Error generating ISBN-10 check digit: %v\n", err)
	} else {
		fmt.Printf("Check digit for '030640615' (ISBN-10): %s\n", check10)
	}
	
	// Generate check digit for ISBN-13
	check13, err := isbn_utils.GenerateCheckDigit13("978316148410")
	if err != nil {
		log.Printf("Error generating ISBN-13 check digit: %v\n", err)
	} else {
		fmt.Printf("Check digit for '978316148410' (ISBN-13): %s\n", check13)
	}
	fmt.Println()
	
	// 5. ISBN Formatting
	fmt.Println("--- ISBN Formatting ---")
	
	unformatted := []string{"0306406152", "9783161484100", "080442957X"}
	for _, u := range unformatted {
		formatted := isbn_utils.Format(u)
		fmt.Printf("Format: %s → %s\n", u, formatted)
	}
	fmt.Println()
	
	// 6. ISBN Normalization
	fmt.Println("--- ISBN Normalization ---")
	
	// Normalize converts ISBN-10 to ISBN-13, or returns clean ISBN-13
	inputs := []string{"0306406152", "9783161484100", "0-306-40615-2"}
	for _, input := range inputs {
		normalized, err := isbn_utils.Normalize(input)
		if err != nil {
			log.Printf("Error normalizing %s: %v\n", input, err)
		} else {
			fmt.Printf("Normalize: %s → %s\n", input, normalized)
		}
	}
	fmt.Println()
	
	// 7. ISBN Generation
	fmt.Println("--- ISBN Generation ---")
	
	// Generate ISBN-10 from 9-digit prefix
	gen10, err := isbn_utils.GenerateISBN10("030640615")
	if err != nil {
		log.Printf("Error generating ISBN-10: %v\n", err)
	} else {
		fmt.Printf("Generated ISBN-10 from '030640615': %s\n", gen10)
	}
	
	// Generate ISBN-13 from 12-digit prefix
	gen13, err := isbn_utils.GenerateISBN13("978316148410")
	if err != nil {
		log.Printf("Error generating ISBN-13: %v\n", err)
	} else {
		fmt.Printf("Generated ISBN-13 from '978316148410': %s\n", gen13)
	}
	fmt.Println()
	
	// 8. ISBN Parsing
	fmt.Println("--- ISBN Parsing ---")
	
	parsed, err := isbn_utils.Parse("978-3-16-148410-0")
	if err != nil {
		log.Printf("Error parsing ISBN: %v\n", err)
	} else {
		fmt.Printf("Parsed ISBN:\n")
		fmt.Printf("  Number: %s\n", parsed.Number)
		fmt.Printf("  Type: %s\n", parsed.Type)
		fmt.Printf("  Prefix: %s\n", parsed.Prefix)
		fmt.Printf("  Check: %s\n", parsed.Check)
	}
	fmt.Println()
	
	// 9. Quick Validation Functions
	fmt.Println("--- Quick Validation ---")
	
	fmt.Printf("IsISBN('0306406152'): %v\n", isbn_utils.IsISBN("0306406152"))
	fmt.Printf("IsISBN10('0306406152'): %v\n", isbn_utils.IsISBN10("0306406152"))
	fmt.Printf("IsISBN13('0306406152'): %v\n", isbn_utils.IsISBN13("0306406152"))
	fmt.Printf("IsISBN13('9783161484100'): %v\n", isbn_utils.IsISBN13("9783161484100"))
	fmt.Println()
	
	// 10. Clean Function
	fmt.Println("--- ISBN Cleaning ---")
	
	dirty := []string{
		"ISBN 0-306-40615-2",
		"978-3-16-148410-0",
		"ISBN: 9783161484100",
		"  0306406152  ",
	}
	for _, d := range dirty {
		clean := isbn_utils.Clean(d)
		fmt.Printf("Clean: '%s' → '%s'\n", d, clean)
	}
	
	fmt.Println()
	fmt.Println("=== Demo Complete ===")
}