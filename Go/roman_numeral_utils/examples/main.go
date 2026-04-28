// Package main demonstrates the usage of roman_numeral_utils package
package main

import (
	"fmt"
	"strings"

	roman "github.com/ayukyo/alltoolkit/Go/roman_numeral_utils"
)

func main() {
	fmt.Println("=== Roman Numeral Utils Demo ===")
	fmt.Println()

	// 1. Basic conversions
	fmt.Println("--- Basic Conversions ---")
	examples := []string{"I", "IV", "IX", "XIV", "XLII", "XCIX", "MCMXCIV", "MMXXIV"}
	for _, r := range examples {
		num, err := roman.ToInt(r)
		if err != nil {
			fmt.Printf("%s -> Error: %v\n", r, err)
		} else {
			fmt.Printf("%-8s -> %d\n", r, num)
		}
	}
	fmt.Println()

	// 2. Integer to Roman
	fmt.Println("--- Integer to Roman ---")
	numbers := []int{1, 4, 9, 14, 42, 99, 2024, 3999}
	for _, n := range numbers {
		r, err := roman.ToRoman(n)
		if err != nil {
			fmt.Printf("%4d -> Error: %v\n", n, err)
		} else {
			fmt.Printf("%4d -> %s\n", n, r)
		}
	}
	fmt.Println()

	// 3. Validation
	fmt.Println("--- Validation ---")
	testStrings := []string{"XIV", "IIII", "VV", "ABC", ""}
	for _, s := range testStrings {
		valid := roman.IsValid(s)
		fmt.Printf("%-6q -> Valid: %v\n", s, valid)
	}
	fmt.Println()

	// 4. Arithmetic operations
	fmt.Println("--- Arithmetic Operations ---")
	
	// Addition
	result, _ := roman.Add("X", "V")
	fmt.Printf("X + V = %s\n", result)
	
	// Subtraction
	result, _ = roman.Subtract("X", "I")
	fmt.Printf("X - I = %s\n", result)
	
	// Multiplication
	result, _ = roman.Multiply("V", "II")
	fmt.Printf("V × II = %s\n", result)
	
	// Division
	result, _ = roman.Divide("X", "II")
	fmt.Printf("X ÷ II = %s\n", result)
	fmt.Println()

	// 5. Comparison
	fmt.Println("--- Comparison ---")
	comparisons := []struct{ a, b string }{
		{"V", "I"},
		{"I", "V"},
		{"X", "X"},
	}
	for _, c := range comparisons {
		cmp, _ := roman.Compare(c.a, c.b)
		var relation string
		switch cmp {
		case -1:
			relation = "<"
		case 0:
			relation = "="
		case 1:
			relation = ">"
		}
		fmt.Printf("%s %s %s\n", c.a, relation, c.b)
	}
	fmt.Println()

	// 6. Generate range
	fmt.Println("--- Generate Range (1-20) ---")
	rangeResult, _ := roman.GenerateRange(1, 20)
	fmt.Println(strings.Join(rangeResult, " "))
	fmt.Println()

	// 7. Find highest
	fmt.Println("--- Find Highest ---")
	romanList := []string{"I", "V", "X", "L", "C", "D", "M"}
	highest, value, _ := roman.FindHighest(romanList)
	fmt.Printf("From %v\nHighest: %s (value: %d)\n", romanList, highest, value)
	fmt.Println()

	// 8. Vinculum notation (for numbers > 3999)
	fmt.Println("--- Vinculum Notation (Large Numbers) ---")
	// _V_ represents V with overline = 5 × 1000 = 5000
	largeExamples := []string{"_V_", "_X_", "M_V_", "_X_M"}
	for _, r := range largeExamples {
		num, err := roman.ParseWithAlternative(r)
		if err != nil {
			fmt.Printf("%-6s -> Error: %v\n", r, err)
		} else {
			fmt.Printf("%-6s -> %d\n", r, num)
		}
	}
	fmt.Println()

	// 9. All Roman numerals
	fmt.Println("--- All Roman Numeral Symbols ---")
	allNumerals := roman.GetAll()
	for _, n := range allNumerals {
		fmt.Printf("%-4s = %-4d  ", n.Symbol, n.Value)
	}
	fmt.Println()
	fmt.Println()

	// 10. Must functions (panic on error)
	fmt.Println("--- Must Functions ---")
	fmt.Printf("MustToInt(\"XIV\") = %d\n", roman.MustToInt("XIV"))
	fmt.Printf("MustToRoman(14) = %s\n", roman.MustToRoman(14))
	fmt.Println()

	// 11. Practical example: Year converter
	fmt.Println("--- Year Converter ---")
	years := []int{1776, 1984, 2000, 2024}
	for _, year := range years {
		r, _ := roman.ToRoman(year)
		fmt.Printf("Year %d -> %s\n", year, r)
	}
	fmt.Println()

	// 12. Round trip test
	fmt.Println("--- Round Trip Test ---")
	for i := 1; i <= 20; i++ {
		r, _ := roman.ToRoman(i)
		back, _ := roman.ToInt(r)
		fmt.Printf("%2d -> %-8s -> %2d ✓\n", i, r, back)
	}
}