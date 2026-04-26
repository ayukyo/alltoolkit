// Example usage of trie_utils package
package main

import (
	"fmt"
	"strings"
	
	trie_utils "github.com/ayukyo/alltoolkit/Go/trie_utils"
)

func main() {
	fmt.Println("=== Trie (Prefix Tree) Utils Examples ===")
	fmt.Println()

	// ========================================
	// 1. Basic Operations
	// ========================================
	fmt.Println("1. Basic Operations")
	fmt.Println(strings.Repeat("-", 40))

	trie := trie_utils.NewTrie()

	// Insert words
	words := []string{"apple", "app", "application", "apply", "banana"}
	inserted := trie.InsertBatch(words)
	fmt.Printf("Inserted %d new words\n", inserted)
	fmt.Printf("Trie size: %d words\n", trie.Size())

	// Search
	fmt.Printf("Search 'apple': %v\n", trie.Search("apple"))
	fmt.Printf("Search 'orange': %v\n", trie.Search("orange"))
	fmt.Printf("Search 'ap': %v (prefix exists but not a word)\n", trie.Search("ap"))
	fmt.Println()

	// ========================================
	// 2. Prefix Operations
	// ========================================
	fmt.Println("2. Prefix Operations")
	fmt.Println(strings.Repeat("-", 40))

	fmt.Printf("StartsWith 'app': %v\n", trie.StartsWith("app"))
	fmt.Printf("StartsWith 'xyz': %v\n", trie.StartsWith("xyz"))
	fmt.Printf("Longest common prefix: %q\n", trie.LongestCommonPrefix())
	fmt.Printf("Longest prefix of 'applicationx': %q\n", trie.LongestPrefixOf("applicationx"))
	fmt.Printf("Words with prefix 'app': %d\n", trie.CountPrefix("app"))
	fmt.Println()

	// ========================================
	// 3. AutoComplete
	// ========================================
	fmt.Println("3. AutoComplete")
	fmt.Println(strings.Repeat("-", 40))

	completions := trie.AutoComplete("app")
	fmt.Printf("AutoComplete('app'): %v\n", completions)

	completions = trie.AutoCompleteN("app", 2)
	fmt.Printf("AutoCompleteN('app', 2): %v\n", completions)

	// Frequency-based autocomplete
	trie.Insert("apple")
	trie.Insert("apple")
	trie.Insert("apple")
	trie.Insert("app")
	trie.Insert("app")

	frequentFirst := trie.AutoCompleteByFrequency("app", 10)
	fmt.Printf("By frequency: %v\n", frequentFirst)
	fmt.Println()

	// ========================================
	// 4. Case Sensitivity
	// ========================================
	fmt.Println("4. Case Sensitivity")
	fmt.Println(strings.Repeat("-", 40))

	caseTrie := trie_utils.NewTrieCaseInsensitive()
	caseTrie.Insert("Hello")
	caseTrie.Insert("WORLD")

	fmt.Printf("Case-sensitive search 'hello': %v\n", trie.Search("hello"))
	fmt.Printf("Case-insensitive search 'hello': %v\n", caseTrie.Search("hello"))
	fmt.Printf("Case-insensitive search 'world': %v\n", caseTrie.Search("world"))
	fmt.Println()

	// ========================================
	// 5. Pattern Matching
	// ========================================
	fmt.Println("5. Pattern Matching")
	fmt.Println(strings.Repeat("-", 40))

	patternTrie := trie_utils.NewTrie()
	patternTrie.InsertBatch([]string{"cat", "bat", "rat", "car", "bar", "cart", "cats"})

	fmt.Printf("Pattern '?at': %v\n", patternTrie.MatchPattern("?at"))
	fmt.Printf("Pattern 'c*t': %v\n", patternTrie.MatchPattern("c*t"))
	fmt.Printf("Pattern 'c??': %v\n", patternTrie.MatchPattern("c??"))
	fmt.Println()

	// ========================================
	// 6. Fuzzy Search
	// ========================================
	fmt.Println("6. Fuzzy Search (Levenshtein Distance)")
	fmt.Println(strings.Repeat("-", 40))

	fuzzyTrie := trie_utils.NewTrie()
	fuzzyTrie.InsertBatch([]string{"hello", "help", "held", "helmet", "world"})

	fmt.Printf("Fuzzy search 'helo' (distance 1): %v\n", fuzzyTrie.FuzzySearch("helo", 1))
	fmt.Printf("Fuzzy search 'hallo' (distance 2): %v\n", fuzzyTrie.FuzzySearch("hallo", 2))
	fmt.Println()

	// ========================================
	// 7. Delete Operations
	// ========================================
	fmt.Println("7. Delete Operations")
	fmt.Println(strings.Repeat("-", 40))

	deleteTrie := trie_utils.NewTrie()
	deleteTrie.InsertBatch([]string{"apple", "app", "application"})
	fmt.Printf("Before delete: %v\n", deleteTrie.GetAllWords())

	deleteTrie.Delete("apple")
	fmt.Printf("After deleting 'apple': %v\n", deleteTrie.GetAllWords())
	fmt.Printf("'app' still exists: %v\n", deleteTrie.Search("app"))
	fmt.Println()

	// ========================================
	// 8. Statistics
	// ========================================
	fmt.Println("8. Statistics")
	fmt.Println(strings.Repeat("-", 40))

	statsTrie := trie_utils.NewTrie()
	statsTrie.InsertBatch([]string{"a", "ab", "abc", "abcd", "abcde"})

	stats := statsTrie.GetStats()
	fmt.Printf("Total words: %d\n", stats.TotalWords)
	fmt.Printf("Total nodes: %d\n", stats.TotalNodes)
	fmt.Printf("Max depth: %d\n", stats.MaxDepth)
	fmt.Printf("Average depth: %.2f\n", stats.AverageDepth)
	fmt.Printf("Branching factor: %.2f\n", stats.BranchingFactor)
	fmt.Println()

	// ========================================
	// 9. Word Frequency Tracking
	// ========================================
	fmt.Println("9. Word Frequency Tracking")
	fmt.Println(strings.Repeat("-", 40))

	freqTrie := trie_utils.NewTrie()
	freqTrie.Insert("hello")
	freqTrie.Insert("hello")
	freqTrie.Insert("hello")
	freqTrie.Insert("world")
	freqTrie.Insert("world")

	fmt.Printf("'hello' count: %d\n", freqTrie.GetCount("hello"))
	fmt.Printf("'world' count: %d\n", freqTrie.GetCount("world"))
	fmt.Printf("'foo' count: %d\n", freqTrie.GetCount("foo"))
	fmt.Println()

	// ========================================
	// 10. Real-world Use Case: Spell Checker
	// ========================================
	fmt.Println("10. Real-world Use Case: Spell Checker")
	fmt.Println(strings.Repeat("-", 40))

	dictionary := trie_utils.NewTrieCaseInsensitive()
	// Simulate a dictionary
	dictionary.InsertBatch([]string{
		"the", "quick", "brown", "fox", "jumps", "over", "lazy", "dog",
		"hello", "world", "programming", "golang", "algorithm", "data", "structure",
	})

	// Check spelling and suggest corrections
	word := "progrmming"
	if !dictionary.Search(word) {
		fmt.Printf("'%s' is misspelled. Suggestions: %v\n", 
			word, dictionary.FuzzySearch(word, 2))
	}

	// Autocomplete suggestion
	userInput := "prog"
	fmt.Printf("User typed '%s'. Suggestions: %v\n", 
		userInput, dictionary.AutoComplete(userInput))
	fmt.Println()

	fmt.Println("=== Examples Complete ===")
}