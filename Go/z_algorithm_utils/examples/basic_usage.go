// Basic usage examples for Z Algorithm Utilities (Go)

package main

import (
	"fmt"
	"strings"
	"zalgorithmutils"
)

func main() {
	fmt.Println("=" + strings.Repeat("-", 59))
	fmt.Println("Z Algorithm Utilities - Go Examples")
	fmt.Println("=" + strings.Repeat("-", 59))

	// 1. Z-Array Computation
	fmt.Println("\n1. Z-Array Computation")
	fmt.Println(strings.Repeat("-", 40))
	s := "aabcaabxaaz"
	z := zalgorithmutils.ZArray(s)
	fmt.Printf("String: %s\n", s)
	fmt.Printf("Z-array: %v\n", z)
	fmt.Println()

	// 2. Visualization
	fmt.Println("\n2. Visualization")
	fmt.Println(strings.Repeat("-", 40))
	fmt.Println(zalgorithmutils.VisualizeZArray("aaaa"))
	fmt.Println()

	// 3. Pattern Matching
	fmt.Println("\n3. Pattern Matching")
	fmt.Println(strings.Repeat("-", 40))
	text := "The quick brown fox jumps over the lazy dog. The fox is quick."
	pattern := "fox"
	positions := zalgorithmutils.FindAllOccurrences(pattern, text)
	fmt.Printf("Searching for '%s' in text:\n", pattern)
	fmt.Printf("  Found at positions: %v\n", positions)
	fmt.Printf("  Count: %d\n", zalgorithmutils.CountOccurrences(pattern, text))
	fmt.Println()

	// 4. Multi-pattern search
	fmt.Println("Multi-pattern search:")
	matcher := zalgorithmutils.NewZPatternMatcher([]string{"quick", "fox", "dog"})
	results := matcher.Search(text)
	fmt.Printf("  Found %d matches:\n", len(results))
	for _, r := range results {
		fmt.Printf("    '%s' at position %d\n", r.Pattern, r.Position)
	}
	fmt.Println()

	// 5. Substring Analysis
	fmt.Println("\n5. Substring Analysis")
	fmt.Println(strings.Repeat("-", 40))
	s1 := "abacababacab"
	lps := zalgorithmutils.LongestPrefixSuffix(s1)
	fmt.Printf("String: %s\n", s1)
	fmt.Printf("Longest prefix-suffix length: %d\n", lps)
	fmt.Println()

	s2 := "banana"
	substr, positions2 := zalgorithmutils.LongestRepeatedSubstring(s2)
	fmt.Printf("String: %s\n", s2)
	fmt.Printf("Longest repeated substring: '%s' at positions %v\n", substr, positions2)
	fmt.Println()

	// 6. Period Detection
	fmt.Println("\n6. Period Detection")
	fmt.Println(strings.Repeat("-", 40))
	s3 := "abcabcabcabc"
	period := zalgorithmutils.FindMinimalPeriod(s3)
	fmt.Printf("String: %s\n", s3)
	fmt.Printf("Minimal period: %d\n", period.Period)
	fmt.Printf("Is periodic: %v\n", period.IsPeriodic)
	fmt.Printf("Repeating unit: '%s'\n", period.PeriodString())
	fmt.Println()

	// 7. Rotation Check
	fmt.Println("\n7. Rotation Check")
	fmt.Println(strings.Repeat("-", 40))
	s4 := "waterbottle"
	s5 := "erbottlewat"
	fmt.Printf("Is '%s' a rotation of '%s'? %v\n", s5, s4, zalgorithmutils.IsRotation(s4, s5))
	fmt.Println()

	// 8. Compression
	fmt.Println("\n8. String Compression")
	fmt.Println(strings.Repeat("-", 40))
	s7 := "abcabcabcabcabc"
	pattern2, count := zalgorithmutils.CompressString(s7)
	fmt.Printf("Original: %s\n", s7)
	fmt.Printf("Compressed: pattern='%s', count=%d\n", pattern2, count)
	fmt.Println()

	// 9. Helper Functions
	fmt.Println("\n9. Helper Functions")
	fmt.Println(strings.Repeat("-", 40))
	fmt.Printf("Contains('abc', 'abcabc'): %v\n", zalgorithmutils.Contains("abc", "abcabc"))
	replaced := zalgorithmutils.ReplaceAll("abc", "xyz", "abcabcabc")
	fmt.Printf("ReplaceAll('abc'->'xyz'): %s\n", replaced)
	parts := zalgorithmutils.SplitByPattern(",", "a,b,c,d")
	fmt.Printf("SplitByPattern(',', 'a,b,c,d'): %v\n", parts)
	fmt.Println()

	fmt.Println("=" + strings.Repeat("-", 59))
	fmt.Println("All examples completed successfully!")
	fmt.Println("=" + strings.Repeat("-", 59))
}