// +build ignore

// Standalone example for the autocomplete package.
// Run with: cd Go/autocomplete_utils && go run examples/main.go
package main

import (
	"fmt"
	"github.com/ayukyo/alltoolkit/Go/autocomplete_utils"
)

func main() {
	basicExample()
	caseInsensitiveExample()
	frequencyExample()
	unicodeExample()
}

func basicExample() {
	fmt.Println("=== Basic Autocomplete ===")

	trie := autocomplete_utils.New()

	// Build dictionary with common programming terms
	words := []string{
		"function", "functionality", "functional",
		"interface", "internal", "internet",
		"variable", "variant", "variation",
		"constant", "construct", "context",
		"package", "packet", "padding",
	}
	trie.InsertBatch(words)

	// Get suggestions
	suggestions := trie.Complete("func", 10)
	fmt.Printf("Suggestions for 'func': %v\n", suggestions)

	suggestions = trie.Complete("var", 10)
	fmt.Printf("Suggestions for 'var': %v\n", suggestions)

	suggestions = trie.Complete("pack", 10)
	fmt.Printf("Suggestions for 'pack': %v\n", suggestions)
}

func caseInsensitiveExample() {
	fmt.Println("\n=== Case Insensitive Mode ===")

	// Case insensitive is useful for user input
	trie := autocomplete_utils.NewCaseInsensitive()

	trie.Insert("JavaScript")
	trie.Insert("JAVA")
	trie.Insert("javascript")
	trie.Insert("JaVaScRiPt")

	fmt.Printf("Total 'javascript' entries: %d\n", trie.GetFrequency("javascript"))
	fmt.Printf("Contains 'javascript': %v\n", trie.Contains("javascript"))
	fmt.Printf("Contains 'JAVASCRIPT': %v\n", trie.Contains("JAVASCRIPT"))
}

func frequencyExample() {
	fmt.Println("\n=== Frequency-based Ranking ===")

	trie := autocomplete_utils.New()

	// Add words with different frequencies
	trie.Insert("error")
	for i := 0; i < 10; i++ {
		trie.Insert("error")
	}

	trie.Insert("event")
	for i := 0; i < 5; i++ {
		trie.Insert("event")
	}

	trie.Insert("evaluate")

	trie.Insert("exception")
	for i := 0; i < 3; i++ {
		trie.Insert("exception")
	}

	// Get suggestions - ranked by frequency
	suggestions := trie.Complete("e", 10)
	fmt.Printf("Suggestions for 'e' (sorted by frequency): %v\n", suggestions)
}

func unicodeExample() {
	fmt.Println("\n=== Unicode Support ===")

	trie := autocomplete_utils.New()

	// Chinese vocabulary
	chinese := []string{
		"你好", "你好吗", "你好世界",
		"世界", "世界地图", "世界和平",
		"北京", "北京大学", "北京烤鸭",
	}
	trie.InsertBatch(chinese)

	suggestions := trie.Complete("北京", 10)
	fmt.Printf("Suggestions for '北京': %v\n", suggestions)

	// Japanese
	trie2 := autocomplete_utils.New()
	japanese := []string{
		"東京", "東京大学", "東京都",
		"大阪", "大阪市", "大阪城",
	}
	trie2.InsertBatch(japanese)

	suggestions = trie2.Complete("東京", 10)
	fmt.Printf("Suggestions for '東京': %v\n", suggestions)
}