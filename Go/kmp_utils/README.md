# KMP String Search Utils

A pure Go implementation of the **Knuth-Morris-Pratt (KMP)** string matching algorithm with zero external dependencies.

## Features

- **Linear Time Complexity**: O(n+m) where n is text length and m is pattern length
- **Zero Dependencies**: Uses only Go standard library
- **Multiple Search Modes**:
  - Find first occurrence
  - Find all occurrences (overlapping and non-overlapping)
  - Case-sensitive and case-insensitive search
- **Text Operations**:
  - Count occurrences
  - Check containment
  - Replace all/first occurrences
- **Advanced Features**:
  - Multi-pattern search
  - Streaming search for large inputs
  - Pattern analysis and validation
  - LPS array (failure function) inspection

## Installation

```bash
go get github.com/ayukyo/alltoolkit/Go/kmp_utils
```

## Quick Start

```go
package main

import (
    "fmt"
    kmp "github.com/ayukyo/alltoolkit/Go/kmp_utils"
)

func main() {
    // Basic search
    pos := kmp.Find("ABABCABAB", "ABABDABACDABABCABAB")
    fmt.Printf("Found at position: %d\n", pos) // Output: 10

    // Find all occurrences
    positions := kmp.FindAll("ABAB", "ABABABAB")
    fmt.Printf("All positions: %v\n", positions) // Output: [0 2 4]

    // Case-insensitive search
    posIgnoreCase := kmp.FindIgnoreCase("HELLO", "hello world")
    fmt.Printf("Found (case-insensitive): %d\n", posIgnoreCase) // Output: 0

    // Count occurrences
    count := kmp.Count("AA", "AAAAAA")
    fmt.Printf("Count: %d\n", count) // Output: 5

    // Replace
    replaced := kmp.Replace("fox", "The quick fox jumps", "dog")
    fmt.Printf("Replaced: %s\n", replaced) // Output: "The quick dog jumps"
}
```

## API Reference

### Basic Functions

```go
// Find first occurrence of pattern in text, returns -1 if not found
func Find(pattern, text string) int

// Find all occurrences of pattern in text
func FindAll(pattern, text string) []int

// Case-insensitive search
func FindIgnoreCase(pattern, text string) int
func FindAllIgnoreCase(pattern, text string) []int

// Count occurrences
func Count(pattern, text string) int

// Check if pattern exists in text
func Contains(pattern, text string) bool
func ContainsIgnoreCase(pattern, text string) bool

// Replace occurrences
func Replace(pattern, text, replacement string) string
func ReplaceFirst(pattern, text, replacement string) string
```

### KMP Object

```go
// Create a preprocessed searcher
kmp := kmp.New("pattern")
kmp := kmp.NewWithOptions("pattern", false) // case-insensitive

// Methods
pos := kmp.Find(text)
positions := kmp.FindAll(text)
count := kmp.Count(text)
exists := kmp.Contains(text)
replaced := kmp.Replace(text, replacement)
replaced := kmp.ReplaceFirst(text, replacement)
lps := kmp.GetLPS() // Get LPS array for analysis
```

### Multi-Pattern Search

```go
mp := kmp.NewMultiPattern("cat", "dog", "bird")

// Find first occurrence of any pattern
idx, pos := mp.FindAny("I have a cat and a dog")

// Find all occurrences of all patterns
all := mp.FindAll("cats and dogs and birds")

// Check if any pattern exists
exists := mp.ContainsAny(text)

// Count occurrences of each pattern
counts := mp.CountAll(text)
```

### Streaming Search

```go
// Create a streaming searcher for large inputs
stream := kmp.NewStreamingKMP("pattern")

// Process bytes one at a time
for _, b := range largeData {
    if stream.ProcessByte(b) {
        // Match found!
    }
}

// Or process in chunks
positions := stream.ProcessBytes(chunk)

// Get all matches found so far
matches := stream.GetMatches()

// Reset for new search
stream.Reset()
```

### Pattern Analysis

```go
// Validate a pattern
err := kmp.ValidatePattern(pattern)

// Analyze pattern characteristics
stats := kmp.AnalyzePattern("ABABABAB")
fmt.Printf("Length: %d\n", stats.Length)
fmt.Printf("Unique chars: %d\n", stats.UniqueChars)
fmt.Printf("Has repeated: %v\n", stats.HasRepeated)
fmt.Printf("Is palindrome: %v\n", stats.IsPalindrome)
fmt.Printf("LPS coefficient: %.2f\n", stats.LPSCoefficient)

// Build LPS array directly
lps := kmp.BuildLPS("ABABCABAB") // [0 0 1 2 0 1 2 3 4]
```

## Algorithm Overview

The KMP algorithm works by:

1. **Preprocessing**: Building a "failure function" (LPS array) that tells us how far to shift the pattern when a mismatch occurs
2. **Searching**: Using the LPS array to avoid backtracking in the text

### LPS Array

The LPS (Longest Prefix Suffix) array stores the length of the longest proper prefix that is also a suffix for each prefix of the pattern.

Example: Pattern "ABABCABAB"
```
Index:   0 1 2 3 4 5 6 7 8
Pattern: A B A B C A B A B
LPS:     0 0 1 2 0 1 2 3 4
```

### Time Complexity

| Operation | Time Complexity |
|-----------|-----------------|
| Preprocessing | O(m) |
| Search | O(n) |
| Total | O(n + m) |

Where n = text length, m = pattern length

## Use Cases

- **Text editors**: Find/replace functionality
- **Log analysis**: Pattern matching in large log files
- **DNA sequencing**: Finding patterns in genetic sequences
- **Network security**: Signature-based intrusion detection
- **Data validation**: Checking for specific patterns in input

## Comparison with Other Algorithms

| Algorithm | Preprocessing | Search | Best For |
|-----------|---------------|--------|----------|
| KMP | O(m) | O(n) | Patterns with repeated substrings |
| Boyer-Moore | O(m + σ) | O(n/m) avg | Long patterns, large alphabets |
| Rabin-Karp | O(m) | O(n+m) avg | Multiple patterns, plagiarism detection |
| Naive | - | O(nm) | Short texts, simple implementation |

## Benchmarks

Run benchmarks with:
```bash
go test -bench=. -benchmem
```

## License

MIT License - Part of the AllToolkit project.