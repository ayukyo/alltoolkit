package main

import (
	"fmt"
	"strings"

	ordinal "github.com/ayukyo/alltoolkit/Go/ordinal_utils"
)

func main() {
	fmt.Println("=== Ordinal Utils Examples ===")
	fmt.Println()

	// Example 1: Basic ordinal conversion
	fmt.Println("1. Basic Ordinal Conversion:")
	converter := ordinal.NewOrdinalConverter(ordinal.English)

	numbers := []int{1, 2, 3, 4, 5, 10, 11, 12, 13, 21, 22, 23, 100, 101}
	for _, n := range numbers {
		ordinalStr, _ := converter.ToOrdinal(n)
		fmt.Printf("   %d -> %s\n", n, ordinalStr)
	}
	fmt.Println()

	// Example 2: Parse ordinals back to numbers
	fmt.Println("2. Parse Ordinals to Numbers:")
	ordinals := []string{"1st", "2nd", "3rd", "21st", "100th", "first", "second", "tenth"}
	for _, ord := range ordinals {
		num, err := converter.ParseOrdinal(ord)
		if err != nil {
			fmt.Printf("   %s -> Error: %v\n", ord, err)
		} else {
			fmt.Printf("   %s -> %d\n", ord, num)
		}
	}
	fmt.Println()

	// Example 3: Generate ordinal range
	fmt.Println("3. Generate Ordinal Range (1-15):")
	ordinalRange, _ := converter.ToOrdinalRange(1, 15)
	fmt.Printf("   %s\n", strings.Join(ordinalRange, ", "))
	fmt.Println()

	// Example 4: Word ordinals
	fmt.Println("4. Word Ordinals (1-10):")
	for i := 1; i <= 10; i++ {
		word, _ := ordinal.ToWordOrdinal(i)
		fmt.Printf("   %d -> %s\n", i, word)
	}
	fmt.Println()

	// Example 5: Multiple languages
	fmt.Println("5. Multiple Languages:")
	languages := []ordinal.Language{
		ordinal.English,
		ordinal.Spanish,
		ordinal.French,
		ordinal.German,
		ordinal.Italian,
	}
	testNum := 5
	for _, lang := range languages {
		conv := ordinal.NewOrdinalConverter(lang)
		result, _ := conv.ToOrdinal(testNum)
		fmt.Printf("   %s: %s\n", lang, result)
	}
	fmt.Println()

	// Example 6: Create formatted lists
	fmt.Println("6. Create Formatted Lists:")
	items := []string{"Install dependencies", "Configure settings", "Run tests", "Deploy application"}
	formattedList := ordinal.OrdinalList(items)
	for _, item := range formattedList {
		fmt.Printf("   %s\n", item)
	}
	fmt.Println()

	// Example 7: Batch conversion
	fmt.Println("7. Batch Conversion:")
	numbers = []int{1, 5, 10, 25, 50, 100}
	results, _ := ordinal.BatchToOrdinal(numbers, ordinal.English)
	fmt.Printf("   Input: %v\n", numbers)
	fmt.Printf("   Output: %s\n", strings.Join(results, ", "))
	fmt.Println()

	// Example 8: Get suffix only
	fmt.Println("8. Get Ordinal Suffix Only:")
	for _, n := range []int{1, 2, 3, 4, 11, 12, 13, 21, 22, 23} {
		suffix, _ := ordinal.GetOrdinalSuffix(n)
		fmt.Printf("   %d -> %q\n", n, suffix)
	}
	fmt.Println()

	// Example 9: Validate ordinals
	fmt.Println("9. Validate Ordinals:")
	testStrings := []string{"1st", "2nd", "3rd", "abc", "1xyz", "first", "twenty-first"}
	for _, s := range testStrings {
		isValid := converter.IsOrdinal(s)
		fmt.Printf("   %q -> Valid: %v\n", s, isValid)
	}
}