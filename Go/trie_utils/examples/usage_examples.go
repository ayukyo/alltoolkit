// Package main demonstrates usage of the trie_utils package
package main

import (
	"fmt"
	"sort"

	"github.com/ayukyo/alltoolkit/Go/trie_utils"
)

func main() {
	fmt.Println("=== Trie Utils Examples ===\n")

	// Example 1: Basic Operations
	basicOperations()

	// Example 2: Autocomplete System
	autocompleteExample()

	// Example 3: Spell Checker
	spellCheckerExample()

	// Example 4: Word Frequency
	wordFrequencyExample()

	// Example 5: Pattern Matching
	patternMatchingExample()

	// Example 6: Longest Prefix Matching (URL Router)
	urlRouterExample()

	// Example 7: Unicode Support
	unicodeExample()
}

func basicOperations() {
	fmt.Println("--- Basic Operations ---")

	trie := trie_utils.NewTrie()

	// Insert words
	trie.InsertWord("apple")
	trie.InsertWord("app")
	trie.InsertWord("application")
	trie.Insert("banana", "fruit")

	// Search
	fmt.Printf("Search 'apple': %v\n", trie.Search("apple"))
	fmt.Printf("Search 'app': %v\n", trie.Search("app"))
	fmt.Printf("Search 'appl': %v\n", trie.Search("appl"))

	// Search with value
	if val, ok := trie.SearchWithValue("banana"); ok {
		fmt.Printf("Value for 'banana': %v\n", val)
	}

	// Check prefix
	fmt.Printf("StartsWith 'app': %v\n", trie.StartsWith("app"))
	fmt.Printf("StartsWith 'ban': %v\n", trie.StartsWith("ban"))

	// Delete
	fmt.Printf("Delete 'app': %v\n", trie.Delete("app"))
	fmt.Printf("Search 'app' after delete: %v\n", trie.Search("app"))

	// Size
	fmt.Printf("Trie size: %d\n", trie.Size())

	fmt.Println()
}

func autocompleteExample() {
	fmt.Println("--- Autocomplete System ---")

	trie := trie_utils.NewTrie()

	// Add dictionary words
	words := []string{
		"apple", "application", "apply", "approach", "approve",
		"banana", "band", "bandana", "bank",
		"coding", "code", "coder", "codes",
	}
	trie.BatchInsert(words)

	// Autocomplete suggestions
	fmt.Println("Autocomplete for 'app':")
	suggestions := trie.AutoComplete("app", 5)
	for _, s := range suggestions {
		fmt.Printf("  - %s\n", s)
	}

	fmt.Println("\nAutocomplete for 'ban':")
	suggestions = trie.AutoComplete("ban", 5)
	for _, s := range suggestions {
		fmt.Printf("  - %s\n", s)
	}

	fmt.Println("\nAutocomplete for 'cod':")
	suggestions = trie.AutoComplete("cod", 5)
	for _, s := range suggestions {
		fmt.Printf("  - %s\n", s)
	}

	fmt.Println()
}

func spellCheckerExample() {
	fmt.Println("--- Spell Checker ---")

	trie := trie_utils.NewTrie()

	// Build dictionary
	dictionary := []string{
		"hello", "help", "helicopter", "helium",
		"world", "word", "work", "worker",
		"the", "they", "there", "their",
	}
	trie.BatchInsert(dictionary)

	// Check spelling
	words := []string{"hello", "helo", "help", "world", "wordy"}
	for _, word := range words {
		if trie.Search(word) {
			fmt.Printf("'%s' - ✓ Correct\n", word)
		} else {
			// Find similar words (words that start with the same prefix)
			prefix := word
			if len(word) > 3 {
				prefix = word[:3]
			}
			suggestions := trie.WordsWithPrefixLimit(prefix, 3)
			fmt.Printf("'%s' - ✗ Not found. Suggestions: %v\n", word, suggestions)
		}
	}

	fmt.Println()
}

func wordFrequencyExample() {
	fmt.Println("--- Word Frequency Tracking ---")

	trie := trie_utils.NewTrie()

	// Simulate word usage (same word inserted multiple times)
	sentences := [][]string{
		{"hello", "world"},
		{"hello", "there"},
		{"hello", "how", "are", "you"},
		{"world", "is", "beautiful"},
		{"hello", "world", "again"},
	}

	for _, sentence := range sentences {
		for _, word := range sentence {
			trie.InsertWord(word)
		}
	}

	// Get words by frequency
	fmt.Println("Words sorted by frequency:")
	wf := trie.GetWordsByFrequency()
	for _, w := range wf {
		fmt.Printf("  %s: %d\n", w.Word, w.Count)
	}

	fmt.Println()
}

func patternMatchingExample() {
	fmt.Println("--- Pattern Matching ---")

	trie := trie_utils.NewTrie()

	// Add words
	words := []string{"cat", "bat", "rat", "car", "bar", "cart", "bark", "cab"}
	trie.BatchInsert(words)

	// Pattern with '?' (single character wildcard)
	fmt.Println("Pattern '?at' (any single char + 'at'):")
	matches := trie.PatternMatch("?at")
	sort.Strings(matches)
	fmt.Printf("  %v\n", matches)

	// Pattern with '*' (zero or more characters)
	fmt.Println("\nPattern 'ca*' (starts with 'ca'):")
	matches = trie.PatternMatch("ca*")
	sort.Strings(matches)
	fmt.Printf("  %v\n", matches)

	// Pattern 'ba*':")
	fmt.Println("\nPattern 'ba*' (starts with 'ba'):")
	matches = trie.PatternMatch("ba*")
	sort.Strings(matches)
	fmt.Printf("  %v\n", matches)

	fmt.Println()
}

func urlRouterExample() {
	fmt.Println("--- URL Router (Longest Prefix Match) ---")

	trie := trie_utils.NewTrie()

	// Define routes
	routes := map[string]interface{}{
		"/api":          "api_root",
		"/api/users":    "users_list",
		"/api/users/id": "user_detail",
		"/api/posts":    "posts_list",
		"/static":       "static_files",
	}
	trie.BatchInsertWithValues(routes)

	// Test longest prefix matching
	urls := []string{
		"/api/users/123",
		"/api/users",
		"/api/posts/456/comments",
		"/static/css/style.css",
		"/unknown/path",
	}

	for _, url := range urls {
		prefix := trie.LongestPrefixOf(url)
		if prefix != "" {
			val, _ := trie.SearchWithValue(prefix)
			fmt.Printf("URL: %-30s -> Route: %-20s (Handler: %v)\n", url, prefix, val)
		} else {
			fmt.Printf("URL: %-30s -> No matching route\n", url)
		}
	}

	fmt.Println()
}

func unicodeExample() {
	fmt.Println("--- Unicode Support ---")

	trie := trie_utils.NewTrie()

	// Add words in different languages
	trie.Insert("你好", "Hello in Chinese")
	trie.Insert("你好吗", "How are you in Chinese")
	trie.Insert("こんにちは", "Hello in Japanese")
	trie.Insert("안녕하세요", "Hello in Korean")
	trie.Insert("مرحبا", "Hello in Arabic")
	trie.Insert("😀🎉", "Emoji celebration")

	// Search Chinese
	fmt.Println("Search '你好':", trie.Search("你好"))
	if val, ok := trie.SearchWithValue("你好"); ok {
		fmt.Printf("Meaning: %v\n", val)
	}

	// Autocomplete Chinese
	fmt.Println("\nWords with prefix '你好':")
	words := trie.WordsWithPrefix("你好")
	for _, w := range words {
		fmt.Printf("  %s\n", w)
	}

	// Emoji support
	fmt.Println("\nSearch '😀🎉':", trie.Search("😀🎉"))

	fmt.Println()
}