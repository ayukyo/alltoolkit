# Z Algorithm Utilities (Go)

A zero-dependency implementation of the Z-algorithm for efficient string matching and pattern searching in Go.

## Features

- **Z-Array Computation**: O(n) algorithm for computing Z-values
- **Pattern Matching**: Find all/first occurrences using Z-algorithm
- **Substring Analysis**: Longest repeated substring, common prefixes
- **Period Detection**: Minimal period, rotation detection
- **String Compression**: Find repeating patterns
- **Multi-Pattern Matching**: Batch search with ZPatternMatcher
- **Bytes Support**: Works with byte slices

## Installation

```go
import "zalgorithmutils"
```

## Quick Start

```go
package main

import (
    "fmt"
    "zalgorithmutils"
)

func main() {
    // Compute Z-array
    z := zalgorithmutils.ZArray("aabcaabxaaz")
    fmt.Println(z) // [0, 1, 0, 0, 3, 1, 0, 0, 2, 1, 0]

    // Find pattern occurrences
    positions := zalgorithmutils.FindAllOccurrences("abc", "abcabcabc")
    fmt.Println(positions) // [0, 3, 6]

    // Find minimal period
    period := zalgorithmutils.FindMinimalPeriod("abcabcabc")
    fmt.Println(period.Period) // 3

    // Multi-pattern search
    matcher := zalgorithmutils.NewZPatternMatcher([]string{"error", "warning"})
    results := matcher.Search("error: file not found")
}
```

## API Reference

### Core Functions

```go
// Z-array computation
func ZArray(s string) []int
func ZArrayBytes(data []byte) []int
func ZArrayWithSentinel(pattern, text, sentinel string) []int

// Pattern matching
func FindAllOccurrences(pattern, text string) []int
func FindFirstOccurrence(pattern, text string) int
func CountOccurrences(pattern, text string) int
func FindMatches(pattern, text string) []ZMatch

// Substring analysis
func LongestPrefixSuffix(s string) int
func LongestRepeatedSubstring(s string) (string, []int)
func LongestCommonPrefix(s1, s2 string) int

// Period detection
func FindMinimalPeriod(s string) StringPeriod
func IsRotation(s1, s2 string) bool
func FindAllRotations(s string) []string

// Compression
func CompressString(s string) (string, int)
func DecompressString(pattern string, count int) string

// Similarity
func SimilarityScore(s1, s2 string) float64
func BatchSimilarity(base string, strings []string) []float64

// Utility
func VisualizeZArray(s string) string
func ValidateZArray(s string, z []int) bool
func Contains(pattern, text string) bool
func ReplaceAll(pattern, replacement, text string) string
func SplitByPattern(pattern, text string) []string
```

### Types

```go
type ZMatch struct {
    Index  int
    Length int
    Text   string
}

type StringPeriod struct {
    String     string
    Period     int
    IsPeriodic bool
}

type ZPatternMatcher struct {
    // Efficient multi-pattern matcher
}
```

### ZPatternMatcher Methods

```go
matcher := zalgorithmutils.NewZPatternMatcher([]string{"pattern1", "pattern2"})

// Search all patterns
results := matcher.Search(text)

// Find first match
first := matcher.SearchFirst(text)

// Count all
counts := matcher.CountAll(text)
```

## Time Complexity

| Function | Time | Space |
|----------|------|-------|
| ZArray | O(n) | O(n) |
| FindAllOccurrences | O(n+m) | O(n+m) |
| LongestPrefixSuffix | O(n) | O(n) |
| FindMinimalPeriod | O(n) | O(n) |

## Zero Dependencies

Uses only Go standard library.

## License

MIT License - Part of AllToolkit