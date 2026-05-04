package main

import (
	"fmt"
	"strings"
	
	bm "github.com/ayukyo/alltoolkit/Go/boyer_moore_utils"
)

func main() {
	fmt.Println("=== Boyer-Moore String Search Examples ===")
	fmt.Println()
	
	// ========================================
	// Example 1: Basic Search
	// ========================================
	fmt.Println("--- Example 1: Basic Search ---")
	fmt.Println()
	
	text := "Hello World, this is a test string with hello again"
	
	// Find first occurrence
	pos := bm.Find("hello", text)
	fmt.Printf("Find 'hello' in text: %d\n", pos)
	
	// Case-insensitive search
	pos = bm.FindIgnoreCase("hello", text)
	fmt.Printf("Find 'hello' (case-insensitive): %d\n", pos)
	
	// Find all occurrences
	positions := bm.FindAll("hello", text)
	fmt.Printf("Find all 'hello': %v\n", positions)
	
	// ========================================
	// Example 2: Using BoyerMoore struct
	// ========================================
	fmt.Println()
	fmt.Println("--- Example 2: Using BoyerMoore struct ---")
	fmt.Println()
	
	searcher := bm.New("pattern")
	
	text2 := "Find the pattern in this pattern text"
	
	// Get first match
	firstPos := searcher.Find(text2)
	fmt.Printf("First 'pattern' at position: %d\n", firstPos)
	
	// Get all matches
	allPos := searcher.FindAll(text2)
	fmt.Printf("All 'pattern' positions: %v\n", allPos)
	
	// Get last match
	lastPos := searcher.FindLast(text2)
	fmt.Printf("Last 'pattern' at position: %d\n", lastPos)
	
	// Count matches
	count := searcher.Count(text2)
	fmt.Printf("Total matches: %d\n", count)
	
	// Check if contains
	hasPattern := searcher.Contains(text2)
	fmt.Printf("Contains 'pattern': %v\n", hasPattern)
	
	// ========================================
	// Example 3: Case-Insensitive Search
	// ========================================
	fmt.Println()
	fmt.Println("--- Example 3: Case-Insensitive Search ---")
	fmt.Println()
	
	searcherIgnoreCase := bm.NewWithOptions("HELLO", false)
	
	text3 := "hello Hello HELLO hElLo"
	
	positions = searcherIgnoreCase.FindAll(text3)
	fmt.Printf("Find 'HELLO' (case-insensitive): %v\n", positions)
	
	// ========================================
	// Example 4: Replace Operations
	// ========================================
	fmt.Println()
	fmt.Println("--- Example 4: Replace Operations ---")
	fmt.Println()
	
	text4 := "The cat sat on the cat mat with the cat"
	
	// Replace all occurrences
	replaced := bm.Replace("cat", text4, "dog")
	fmt.Printf("Replace all 'cat' with 'dog':\n  %s\n", replaced)
	
	// Replace first occurrence
	replacedFirst := bm.ReplaceFirst("cat", text4, "dog")
	fmt.Printf("Replace first 'cat' with 'dog':\n  %s\n", replacedFirst)
	
	// Using struct method
	searcher2 := bm.New("cat")
	replaced = searcher2.Replace(text4, "dog")
	fmt.Printf("Using struct Replace:\n  %s\n", replaced)
	
	// ========================================
	// Example 5: Match Details
	// ========================================
	fmt.Println()
	fmt.Println("--- Example 5: Match Details ---")
	fmt.Println()
	
	text5 := "testing test tested test"
	
	matches := bm.FindMatches("test", text5)
	
	fmt.Println("Detailed matches:")
	for i, m := range matches {
		fmt.Printf("  Match %d: position=%d, text='%s', end=%d\n", 
			i+1, m.Position, m.Text, m.EndPosition)
	}
	
	// ========================================
	// Example 6: Horspool Algorithm
	// ========================================
	fmt.Println()
	fmt.Println("--- Example 6: Horspool Algorithm ---")
	fmt.Println()
	
	text6 := "ababababababab"
	
	// Using Horspool (simplified Boyer-Moore)
	pos = bm.FindHorspool("ab", text6)
	fmt.Printf("Horspool Find 'ab': %d\n", pos)
	
	positions = bm.FindAllHorspool("ab", text6)
	fmt.Printf("Horspool FindAll 'ab': %v\n", positions)
	
	// Using Horspool struct
	h := bm.NewHorspool("ab")
	count = h.Count(text6)
	fmt.Printf("Horspool Count 'ab': %d\n", count)
	
	// ========================================
	// Example 7: Turbo Boyer-Moore
	// ========================================
	fmt.Println()
	fmt.Println("--- Example 7: Turbo Boyer-Moore ---")
	fmt.Println()
	
	tbm := bm.NewTurbo("pattern")
	
	text7 := "Find the pattern here with pattern optimization"
	
	pos = tbm.Find(text7)
	fmt.Printf("Turbo Boyer-Moore Find 'pattern': %d\n", pos)
	
	// ========================================
	// Example 8: Multi-Pattern Search
	// ========================================
	fmt.Println()
	fmt.Println("--- Example 8: Multi-Pattern Search ---")
	fmt.Println()
	
	mp := bm.NewMultiPattern("hello", "world", "test")
	
	text8 := "hello world test hello"
	
	// Find first occurrence of any pattern
	idx, pos := mp.FindAny(text8)
	fmt.Printf("FindAny: pattern index=%d ('%s'), position=%d\n", 
		idx, mp.patterns[idx], pos)
	
	// Find all occurrences of all patterns
	allMatches := mp.FindAll(text8)
	fmt.Println("FindAll patterns:")
	for patternIdx, positions := range allMatches {
		fmt.Printf("  Pattern %d ('%s'): %v\n", 
			patternIdx, mp.patterns[patternIdx], positions)
	}
	
	// Check if any pattern exists
	hasAny := mp.ContainsAny(text8)
	fmt.Printf("ContainsAny: %v\n", hasAny)
	
	// Count each pattern
	counts := mp.CountAll(text8)
	fmt.Println("CountAll:")
	for patternIdx, count := range counts {
		fmt.Printf("  Pattern %d ('%s'): %d occurrences\n", 
			patternIdx, mp.patterns[patternIdx], count)
	}
	
	// ========================================
	// Example 9: Pattern Analysis
	// ========================================
	fmt.Println()
	fmt.Println("--- Example 9: Pattern Analysis ---")
	fmt.Println()
	
	pattern := "abab"
	
	// Validate pattern
	valid := bm.ValidatePattern(pattern)
	if valid == "" {
		fmt.Printf("Pattern '%s' is valid\n", pattern)
	} else {
		fmt.Printf("Pattern invalid: %s\n", valid)
	}
	
	// Analyze pattern
	stats := bm.AnalyzePattern(pattern)
	fmt.Printf("Pattern statistics:\n")
	fmt.Printf("  Length: %d\n", stats.Length)
	fmt.Printf("  Unique chars: %d\n", stats.UniqueChars)
	fmt.Printf("  Has repeated chars: %v\n", stats.HasRepeated)
	fmt.Printf("  Is palindrome: %v\n", stats.IsPalindrome)
	fmt.Printf("  Character frequency: %v\n", stats.CharFreq)
	
	// ========================================
	// Example 10: Chinese Text Search
	// ========================================
	fmt.Println()
	fmt.Println("--- Example 10: Chinese Text Search ---")
	fmt.Println()
	
	chineseText := "你好世界你好编程你好测试"
	
	searcherChinese := bm.New("你好")
	
	positions = searcherChinese.FindAll(chineseText)
	fmt.Printf("Find '你好' in Chinese text: %v\n", positions)
	
	count = searcherChinese.Count(chineseText)
	fmt.Printf("Count '你好': %d\n", count)
	
	// ========================================
	// Example 11: Special Characters
	// ========================================
	fmt.Println()
	fmt.Println("--- Example 11: Special Characters ---")
	fmt.Println()
	
	specialText := "Price: $100, Email: user@example.com, Tag: #programming"
	
	// Search for special characters
	pos = bm.Find("$100", specialText)
	fmt.Printf("Find '$100': %d\n", pos)
	
	pos = bm.Find("@example", specialText)
	fmt.Printf("Find '@example': %d\n", pos)
	
	pos = bm.Find("#programming", specialText)
	fmt.Printf("Find '#programming': %d\n", pos)
	
	// ========================================
	// Example 12: Real-World Use Case
	// ========================================
	fmt.Println()
	fmt.Println("--- Example 12: Real-World Use Case ---")
	fmt.Println()
	
	// Simulating log file search
	logContent := `[2024-01-01 10:00:00] INFO: Application started
[2024-01-01 10:01:00] ERROR: Database connection failed
[2024-01-01 10:02:00] INFO: Retrying connection
[2024-01-01 10:03:00] ERROR: Connection timeout
[2024-01-01 10:04:00] INFO: Connection restored
[2024-01-01 10:05:00] ERROR: Query failed`

	// Find all ERROR lines
	errorSearcher := bm.New("ERROR")
	errorPositions := errorSearcher.FindAll(logContent)
	fmt.Printf("Found %d ERROR entries at positions: %v\n", 
		len(errorPositions), errorPositions)
	
	// Extract ERROR lines
	lines := strings.Split(logContent, "\n")
	for _, pos := range errorPositions {
		lineNum := 0
		charCount := 0
		for i, line := range lines {
			if charCount <= pos && charCount+len(line) > pos {
				lineNum = i
				break
			}
			charCount += len(line) + 1
		}
		fmt.Printf("  Line %d: %s\n", lineNum+1, lines[lineNum])
	}
	
	// ========================================
	// Example 13: Performance Comparison
	// ========================================
	fmt.Println()
	fmt.Println("--- Example 13: Performance Comparison ---")
	fmt.Println()
	
	longText := strings.Repeat("ab", 1000) + "target" + strings.Repeat("ab", 1000)
	patternLong := "target"
	
	// Standard Boyer-Moore
	pos = bm.Find(patternLong, longText)
	fmt.Printf("Boyer-Moore Find 'target': %d\n", pos)
	
	// Horspool
	pos = bm.FindHorspool(patternLong, longText)
	fmt.Printf("Horspool Find 'target': %d\n", pos)
	
	// Turbo
	tbm2 := bm.NewTurbo(patternLong)
	pos = tbm2.Find(longText)
	fmt.Printf("Turbo Boyer-Moore Find 'target': %d\n", pos)
	
	fmt.Println()
	fmt.Println("=== All Examples Complete ===")
}