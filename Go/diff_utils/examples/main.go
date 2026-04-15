// Example usage of diff_utils package
// Run with: go run examples/main.go
package main

import (
	"fmt"
	"strings"

	diffutils "github.com/ayukyo/alltoolkit/Go/diff_utils"
)

func main() {
	fmt.Println("=== Diff Utils Examples ===")
	fmt.Println()

	// Example 1: Line-level diff
	fmt.Println("--- Example 1: Line Diff ---")
	oldCode := `package main

func hello() {
    println("Hello")
}

func main() {
    hello()
}`

	newCode := `package main

import "fmt"

func hello() {
    fmt.Println("Hello, World!")
}

func main() {
    hello()
    fmt.Println("Done!")
}`

	result := diffutils.DiffLines(oldCode, newCode)
	fmt.Printf("Lines: %d → %d\n", result.LinesA, result.LinesB)
	fmt.Printf("Changes: +%d added, -%d removed\n", result.Stats.Added, result.Stats.Removed)
	fmt.Println()

	// Example 2: Unified diff format
	fmt.Println("--- Example 2: Unified Diff ---")
	unified := diffutils.FormatUnified(result, 2, "old.go", "new.go")
	fmt.Println(unified)

	// Example 3: Character-level diff
	fmt.Println("--- Example 3: Character Diff ---")
	charDiffs := diffutils.DiffChars("kitten", "sitting")
	var charOutput strings.Builder
	for _, d := range charDiffs {
		switch d.Type {
		case diffutils.Delete:
			charOutput.WriteString("\033[31m[-" + d.Text + "]\033[0m")
		case diffutils.Insert:
			charOutput.WriteString("\033[32m[+" + d.Text + "]\033[0m")
		case diffutils.Equal:
			charOutput.WriteString(d.Text)
		}
	}
	fmt.Println("kitten → sitting:", charOutput.String())
	fmt.Println()

	// Example 4: Word-level diff
	fmt.Println("--- Example 4: Word Diff ---")
	wordDiffs := diffutils.DiffWords(
		"The quick brown fox jumps over the lazy dog",
		"The fast brown dog runs past the sleepy cat",
	)
	for _, d := range wordDiffs {
		switch d.Type {
		case diffutils.Delete:
			fmt.Printf("\033[31m[-%s]\033[0m ", d.Text)
		case diffutils.Insert:
			fmt.Printf("\033[32m[+%s]\033[0m ", d.Text)
		case diffutils.Equal:
			fmt.Printf("%s ", d.Text)
		}
	}
	fmt.Println()
	fmt.Println()

	// Example 5: Similarity score
	fmt.Println("--- Example 5: Similarity Score ---")
	pairs := [][2]string{
		{"hello world", "hello world"},
		{"hello world", "hallo world"},
		{"hello world", "goodbye world"},
		{"hello world", "completely different"},
		{"kitten", "sitting"},
	}
	for _, pair := range pairs {
		score := diffutils.Similarity(pair[0], pair[1])
		dist := diffutils.LevenshteinDistance(pair[0], pair[1])
		fmt.Printf("Similarity: %.2f | Distance: %2d | '%s' ↔ '%s'\n",
			score, dist, pair[0], pair[1])
	}
	fmt.Println()

	// Example 6: LCS (Longest Common Subsequence)
	fmt.Println("--- Example 6: LCS ---")
	lcs, length := diffutils.LCS("ABCBDAB", "BDCABA")
	fmt.Printf("String 1: ABCBDAB\n")
	fmt.Printf("String 2: BDCABA\n")
	fmt.Printf("LCS: '%s' (length: %d)\n", lcs, length)
	fmt.Println()

	// Example 7: Unicode support
	fmt.Println("--- Example 7: Unicode Support ---")
	unicodeResult := diffutils.DiffLines(
		"你好世界\nHello World\n👋",
		"你好中国\nHello Earth\n🌍",
	)
	fmt.Printf("Chinese & Emoji changes: +%d added, -%d removed\n",
		unicodeResult.Stats.Added, unicodeResult.Stats.Removed)
	fmt.Println()

	// Example 8: HTML output
	fmt.Println("--- Example 8: HTML Output ---")
	htmlDiffs := []diffutils.Diff{
		{Type: diffutils.Equal, Text: "Hello "},
		{Type: diffutils.Delete, Text: "World"},
		{Type: diffutils.Insert, Text: "Go"},
	}
	html := diffutils.FormatHTML(htmlDiffs)
	fmt.Println(html)

	// Example 9: Statistics
	fmt.Println("--- Example 9: Diff Statistics ---")
	bigOld := strings.Repeat("line\n", 100)
	bigNew := strings.Repeat("modified\n", 50) + strings.Repeat("line\n", 50)
	bigResult := diffutils.DiffLines(bigOld, bigNew)
	fmt.Printf("Original: %d lines\n", bigResult.LinesA)
	fmt.Printf("New:      %d lines\n", bigResult.LinesB)
	fmt.Printf("Added:    %d lines\n", bigResult.Stats.Added)
	fmt.Printf("Removed:  %d lines\n", bigResult.Stats.Removed)
	fmt.Printf("Unchanged: %d lines\n", bigResult.Stats.Equal)
}