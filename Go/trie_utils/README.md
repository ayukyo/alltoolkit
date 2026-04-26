# Trie Utils - Go

A comprehensive Trie (prefix tree) data structure implementation for Go, featuring prefix search, autocomplete, pattern matching, and fuzzy search capabilities.

## Features

- **Basic Operations**: Insert, search, and delete words
- **Prefix Operations**: Prefix search, longest common prefix, longest prefix of string
- **Autocomplete**: With alphabetical or frequency-based ordering
- **Pattern Matching**: Support for `?` (single char) and `*` (multiple chars) wildcards
- **Fuzzy Search**: Find words within a given Levenshtein distance
- **Case Handling**: Case-sensitive and case-insensitive modes
- **Statistics**: Get trie statistics (word count, node count, depth, branching factor)
- **Frequency Tracking**: Track word insertion counts

## Installation

```go
import trie_utils "github.com/ayukyo/alltoolkit/Go/trie_utils"
```

## Quick Start

```go
package main

import (
    "fmt"
    trie_utils "github.com/ayukyo/alltoolkit/Go/trie_utils"
)

func main() {
    // Create a new trie
    trie := trie_utils.NewTrie()
    
    // Insert words
    trie.Insert("apple")
    trie.Insert("app")
    trie.Insert("application")
    trie.Insert("banana")
    
    // Search
    fmt.Println(trie.Search("apple"))  // true
    fmt.Println(trie.Search("orange")) // false
    
    // Autocomplete
    completions := trie.AutoComplete("app")
    fmt.Println(completions) // [app apple application]
    
    // Check prefix
    fmt.Println(trie.StartsWith("app")) // true
    
    // Fuzzy search (Levenshtein distance)
    results := trie.FuzzySearch("applx", 1)
    fmt.Println(results) // [apple]
}
```

## API Reference

### Creating a Trie

```go
// Case-sensitive (default)
trie := trie_utils.NewTrie()

// Case-insensitive
trie := trie_utils.NewTrieCaseInsensitive()
```

### Basic Operations

```go
// Insert a single word
trie.Insert("hello")

// Insert multiple words
count := trie.InsertBatch([]string{"hello", "world", "foo"})

// Search for a word
exists := trie.Search("hello")

// Get word frequency
count := trie.GetCount("hello")

// Delete a word
deleted := trie.Delete("hello")

// Get size
size := trie.Size()

// Check if empty
isEmpty := trie.IsEmpty()

// Clear all words
trie.Clear()

// Get all words
words := trie.GetAllWords()
```

### Prefix Operations

```go
// Check if any word starts with prefix
hasPrefix := trie.StartsWith("app")

// Get longest common prefix of all words
lcp := trie.LongestCommonPrefix()

// Get longest word that is a prefix of string
prefix := trie.LongestPrefixOf("applepie") // returns "apple" if in trie

// Count words with a prefix
count := trie.CountPrefix("app")
```

### Autocomplete

```go
// Get all words starting with prefix (sorted alphabetically)
words := trie.AutoComplete("app")

// Get up to N words
words := trie.AutoCompleteN("app", 5)

// Get words sorted by frequency (most frequent first)
words := trie.AutoCompleteByFrequency("app", 10)
```

### Pattern Matching

```go
// Use ? for any single character
results := trie.MatchPattern("?at") // matches "cat", "bat", "rat"

// Use * for any sequence of characters
results := trie.MatchPattern("c*t") // matches "cat", "cart", "coat"

// Combine patterns
results := trie.MatchPattern("c??") // matches "cat", "car", "can"
```

### Fuzzy Search

```go
// Find words within edit distance 2
results := trie.FuzzySearch("hello", 2)
// Returns words like "hello", "help", "held", "helmet"
```

### Statistics

```go
stats := trie.GetStats()
fmt.Printf("Words: %d\n", stats.TotalWords)
fmt.Printf("Nodes: %d\n", stats.TotalNodes)
fmt.Printf("Max Depth: %d\n", stats.MaxDepth)
fmt.Printf("Average Depth: %.2f\n", stats.AverageDepth)
fmt.Printf("Branching Factor: %.2f\n", stats.BranchingFactor)
```

## Use Cases

### 1. Autocomplete System

```go
trie := trie_utils.NewTrie()
trie.InsertBatch(dictionary)

// As user types, provide suggestions
suggestions := trie.AutoCompleteN(userInput, 10)
```

### 2. Spell Checker

```go
dictionary := trie_utils.NewTrieCaseInsensitive()
dictionary.InsertBatch(wordList)

if !dictionary.Search(word) {
    suggestions := dictionary.FuzzySearch(word, 2)
    fmt.Printf("Did you mean: %v?\n", suggestions)
}
```

### 3. IP Routing Table

```go
routes := trie_utils.NewTrie()
routes.Insert("192.168.1.0/24")
routes.Insert("192.168.0.0/16")

// Find longest matching prefix
route := routes.LongestPrefixOf("192.168.1.100")
```

### 4. Search Suggestions

```go
// Track search frequency
searchTrie := trie_utils.NewTrie()
searchTrie.Insert("golang tutorial")
searchTrie.Insert("golang tutorial") // increment count

// Get most popular suggestions
popular := searchTrie.AutoCompleteByFrequency("gol", 5)
```

## Performance

- **Insert**: O(m) where m is the word length
- **Search**: O(m) where m is the word length
- **Delete**: O(m) where m is the word length
- **Autocomplete**: O(m + n) where n is the number of matches
- **Fuzzy Search**: O(n × m) where n is word count, m is average length

## License

MIT License