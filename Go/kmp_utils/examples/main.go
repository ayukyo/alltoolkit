// Example demonstrating the kmp_utils package
package main

import (
	"fmt"
	"strings"
	
	kmp "github.com/ayukyo/alltoolkit/Go/kmp_utils"
)

func main() {
	fmt.Println("=== KMP String Search Algorithm Demo ===")
	fmt.Println()

	// Example 1: Basic pattern matching
	fmt.Println("1. Basic Pattern Matching")
	fmt.Println(strings.Repeat("-", 40))
	text := "ABABDABACDABABCABAB"
	pattern := "ABABCABAB"
	
	searcher := kmp.New(pattern)
	pos := searcher.Find(text)
	
	fmt.Printf("Text: %s\n", text)
	fmt.Printf("Pattern: %s\n", pattern)
	fmt.Printf("First match at position: %d\n", pos)
	fmt.Println()

	// Example 2: Find all occurrences
	fmt.Println("2. Find All Occurrences")
	fmt.Println(strings.Repeat("-", 40))
	text2 := "ABABABABABAB"
	pattern2 := "ABAB"
	
	positions := kmp.FindAll(pattern2, text2)
	fmt.Printf("Text: %s\n", text2)
	fmt.Printf("Pattern: %s\n", pattern2)
	fmt.Printf("All match positions: %v\n", positions)
	fmt.Printf("Total matches: %d\n", len(positions))
	fmt.Println()

	// Example 3: Case-insensitive search
	fmt.Println("3. Case-Insensitive Search")
	fmt.Println(strings.Repeat("-", 40))
	text3 := "Hello WORLD, hello World, HELLO world"
	pattern3 := "hello"
	
	positionsCase := kmp.FindAllIgnoreCase(pattern3, text3)
	fmt.Printf("Text: %s\n", text3)
	fmt.Printf("Pattern: %s (case-insensitive)\n", pattern3)
	fmt.Printf("Matches at positions: %v\n", positionsCase)
	fmt.Println()

	// Example 4: Replacement
	fmt.Println("4. Text Replacement")
	fmt.Println(strings.Repeat("-", 40))
	text4 := "The quick brown fox jumps over the lazy dog. The fox is fast."
	pattern4 := "fox"
	
	replacedAll := kmp.Replace(pattern4, text4, "cat")
	replacedFirst := kmp.ReplaceFirst(pattern4, text4, "wolf")
	
	fmt.Printf("Original: %s\n", text4)
	fmt.Printf("Replace all 'fox' with 'cat': %s\n", replacedAll)
	fmt.Printf("Replace first 'fox' with 'wolf': %s\n", replacedFirst)
	fmt.Println()

	// Example 5: LPS Array Analysis
	fmt.Println("5. LPS Array (Failure Function)")
	fmt.Println(strings.Repeat("-", 40))
	patterns := []string{"ABABCABAB", "AAAA", "ABCDE", "ABABABAB"}
	
	for _, p := range patterns {
		lps := kmp.BuildLPS(p)
		fmt.Printf("Pattern: %-12s LPS: %v\n", p, lps)
	}
	fmt.Println()

	// Example 6: Multi-pattern search
	fmt.Println("6. Multi-Pattern Search")
	fmt.Println(strings.Repeat("-", 40))
	text6 := "I love cats and dogs, but birds are also nice"
	mp := kmp.NewMultiPattern("cat", "dog", "bird", "love")
	
	idx, pos := mp.FindAny(text6)
	fmt.Printf("Text: %s\n", text6)
	fmt.Printf("First match: pattern index %d at position %d\n", idx, pos)
	
	allMatches := mp.FindAll(text6)
	fmt.Printf("All matches by pattern index: %v\n", allMatches)
	fmt.Println()

	// Example 7: Pattern Analysis
	fmt.Println("7. Pattern Analysis")
	fmt.Println(strings.Repeat("-", 40))
	testPatterns := []string{"ABABABAB", "AAAA", "ABCD", "ABBA"}
	
	for _, p := range testPatterns {
		stats := kmp.AnalyzePattern(p)
		fmt.Printf("Pattern: %-10s | Length: %d | Unique: %d | Repeated: %v | Palindrome: %v | LPS Coef: %.2f\n",
			p, stats.Length, stats.UniqueChars, stats.HasRepeated, stats.IsPalindrome, stats.LPSCoefficient)
	}
	fmt.Println()

	// Example 8: Streaming KMP
	fmt.Println("8. Streaming KMP Search")
	fmt.Println(strings.Repeat("-", 40))
	streamPattern := "ABC"
	streamText := []byte("XYZABCXYZ")
	
	streamSearcher := kmp.NewStreamingKMP(streamPattern)
	positions8 := streamSearcher.ProcessBytes(streamText)
	
	fmt.Printf("Pattern: %s\n", streamPattern)
	fmt.Printf("Stream: %s\n", streamText)
	fmt.Printf("Matches found at positions: %v\n", positions8)
	fmt.Println()

	// Example 9: Detailed Match Information
	fmt.Println("9. Detailed Match Information")
	fmt.Println(strings.Repeat("-", 40))
	text9 := "testing test tested tester"
	pattern9 := "test"
	
	matches := kmp.FindMatches(pattern9, text9)
	fmt.Printf("Text: %s\n", text9)
	fmt.Printf("Pattern: %s\n", pattern9)
	fmt.Printf("Matches:\n")
	for i, m := range matches {
		fmt.Printf("  Match %d: position=%d, text=%q, end=%d\n", i+1, m.Position, m.Text, m.EndPosition)
	}
	fmt.Println()

	// Example 10: Overlapping vs Non-overlapping
	fmt.Println("10. Overlapping vs Non-overlapping Matches")
	fmt.Println(strings.Repeat("-", 40))
	text10 := "AAAA"
	pattern10 := "AA"
	
	overlapping := kmp.FindOverlapping(pattern10, text10)
	nonOverlapping := kmp.FindNonOverlapping(pattern10, text10)
	
	fmt.Printf("Text: %s\n", text10)
	fmt.Printf("Pattern: %s\n", pattern10)
	fmt.Printf("Overlapping matches: %v (count: %d)\n", overlapping, len(overlapping))
	fmt.Printf("Non-overlapping matches: %v (count: %d)\n", nonOverlapping, len(nonOverlapping))
	fmt.Println()

	// Example 11: Performance comparison
	fmt.Println("11. Performance Note")
	fmt.Println(strings.Repeat("-", 40))
	fmt.Println("KMP Algorithm Complexity:")
	fmt.Println("  - Preprocessing: O(m) where m is pattern length")
	fmt.Println("  - Searching: O(n) where n is text length")
	fmt.Println("  - Total: O(n + m) - linear time")
	fmt.Println()
	fmt.Println("Advantages over naive search:")
	fmt.Println("  - No backtracking in the text")
	fmt.Println("  - Efficient for patterns with repeated substrings")
	fmt.Println("  - Streaming capability for large inputs")
	
	fmt.Println()
	fmt.Println("=== Demo Complete ===")
}