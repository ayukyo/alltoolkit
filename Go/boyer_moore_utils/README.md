# Boyer-Moore String Search Utils

A high-performance Go implementation of the Boyer-Moore string matching algorithm with multiple variants.

## Features

- ✅ **Standard Boyer-Moore** - Bad character + good suffix rules
- ✅ **Boyer-Moore-Horspool** - Simplified variant (last character optimization)
- ✅ **Turbo Boyer-Moore** - Memory-optimized variant
- ✅ **Case-sensitive & insensitive** search
- ✅ **Find first, last, all** occurrences
- ✅ **Replace** operations (all/first)
- ✅ **Multi-pattern** search
- ✅ **Pattern validation & analysis**
- ✅ **Match details** with position info
- ✅ **Unicode support** (Chinese, special characters)
- ✅ **Zero dependencies** - Pure Go implementation

## Algorithm Overview

Boyer-Moore achieves **O(n/m)** average-case complexity (n: text length, m: pattern length), making it one of the fastest string matching algorithms. It skips unnecessary comparisons using two heuristics:

1. **Bad Character Rule**: When a mismatch occurs, shift based on where the mismatched character appears in the pattern
2. **Good Suffix Rule**: When a suffix matches, shift to align with another occurrence of that suffix

## Quick Start

```go
import bm "github.com/ayukyo/alltoolkit/Go/boyer_moore_utils"

// Simple search
pos := bm.Find("hello", "hello world")  // Returns 0

// Find all occurrences
positions := bm.FindAll("ab", "ababab")  // Returns [0, 2, 4]

// Case-insensitive search
pos := bm.FindIgnoreCase("HELLO", "hello world")  // Returns 0

// Count occurrences
count := bm.Count("ab", "abababab")  // Returns 4

// Check existence
exists := bm.Contains("hello", "hello world")  // Returns true

// Replace
result := bm.Replace("cat", "cat cat cat", "dog")  // "dog dog dog"
```

## Usage

### Basic Functions

```go
// Find first occurrence
pos := bm.Find(pattern, text)  // Returns position or -1

// Find all occurrences
positions := bm.FindAll(pattern, text)  // Returns []int

// Case-insensitive
pos := bm.FindIgnoreCase(pattern, text)
positions := bm.FindAllIgnoreCase(pattern, text)

// Count
count := bm.Count(pattern, text)

// Contains
exists := bm.Contains(pattern, text)
exists = bm.ContainsIgnoreCase(pattern, text)

// Replace
replaced := bm.Replace(pattern, text, replacement)
replaced := bm.ReplaceFirst(pattern, text, replacement)
```

### BoyerMoore Struct

```go
// Create searcher
searcher := bm.New("pattern")

// Configure case sensitivity
searcher := bm.NewWithOptions("pattern", false)  // case-insensitive

// Search methods
pos := searcher.Find(text)           // First match
positions := searcher.FindAll(text)  // All matches
pos := searcher.FindLast(text)       // Last match
count := searcher.Count(text)        // Match count
exists := searcher.Contains(text)    // Check existence

// Replace methods
replaced := searcher.Replace(text, replacement)
replaced := searcher.ReplaceFirst(text, replacement)

// Pattern info
pattern := searcher.GetPattern()
length := searcher.GetPatternLength()
isCS := searcher.IsCaseSensitive()
```

### Horspool Algorithm

Simplified Boyer-Moore using only bad character rule (faster preprocessing):

```go
// Using functions
pos := bm.FindHorspool(pattern, text)
positions := bm.FindAllHorspool(pattern, text)

// Using struct
h := bm.NewHorspool("pattern")
pos := h.Find(text)
positions := h.FindAll(text)
count := h.Count(text)
exists := h.Contains(text)
```

### Turbo Boyer-Moore

Memory-optimized variant that remembers matched characters:

```go
tbm := bm.NewTurbo("pattern")
pos := tbm.Find(text)
```

### Match Details

```go
matches := bm.FindMatches("ab", "ababab")
for _, m := range matches {
    fmt.Printf("Position: %d, Text: %s, End: %d\n",
        m.Position, m.Text, m.EndPosition)
}
// Output:
// Position: 0, Text: ab, End: 2
// Position: 2, Text: ab, End: 4
// Position: 4, Text: ab, End: 6
```

### Multi-Pattern Search

```go
mp := bm.NewMultiPattern("hello", "world", "test")

// Find first occurrence of any pattern
idx, pos := mp.FindAny(text)  // Returns pattern index and position

// Find all occurrences of all patterns
allMatches := mp.FindAll(text)  // Returns map[int][]int

// Check if any pattern exists
exists := mp.ContainsAny(text)

// Count occurrences of each pattern
counts := mp.CountAll(text)  // Returns map[int]int
```

### Pattern Analysis

```go
// Validate pattern
err := bm.ValidatePattern("")  // Returns error message or empty string

// Analyze pattern
stats := bm.AnalyzePattern("abab")
fmt.Printf("Length: %d\n", stats.Length)
fmt.Printf("Unique chars: %d\n", stats.UniqueChars)
fmt.Printf("Has repeated: %v\n", stats.HasRepeated)
fmt.Printf("Is palindrome: %v\n", stats.IsPalindrome)
fmt.Printf("Char frequency: %v\n", stats.CharFreq)
```

## Performance

Boyer-Moore is especially efficient for:
- Long patterns (m > 4)
- Large texts (n >> m)
- Patterns with unique characters

Algorithm comparison for finding "target" in text of length 2000:

| Algorithm | Average Comparisons |
|-----------|---------------------|
| Naive | ~2000 |
| Boyer-Moore | ~334 (n/m) |
| Horspool | ~334 (n/m) |
| Turbo | ~250 (memory optimization) |

## API Reference

### Functions

| Function | Return | Description |
|----------|--------|-------------|
| `Find(p, t)` | int | First match position (-1 if not found) |
| `FindAll(p, t)` | []int | All match positions |
| `FindIgnoreCase(p, t)` | int | Case-insensitive first match |
| `FindAllIgnoreCase(p, t)` | []int | Case-insensitive all matches |
| `Count(p, t)` | int | Match count |
| `Contains(p, t)` | bool | Check existence |
| `ContainsIgnoreCase(p, t)` | bool | Case-insensitive check |
| `Replace(p, t, r)` | string | Replace all occurrences |
| `ReplaceFirst(p, t, r)` | string | Replace first occurrence |
| `FindHorspool(p, t)` | int | Horspool first match |
| `FindAllHorspool(p, t)` | []int | Horspool all matches |
| `FindMatches(p, t)` | []Match | Detailed match info |
| `FindMatchesIgnoreCase(p, t)` | []Match | Case-insensitive matches |
| `ValidatePattern(p)` | string | Pattern validation |
| `AnalyzePattern(p)` | PatternStats | Pattern statistics |

### BoyerMoore Methods

| Method | Return | Description |
|--------|--------|-------------|
| `Find(t)` | int | First match |
| `FindAll(t)` | []int | All matches |
| `FindLast(t)` | int | Last match |
| `Count(t)` | int | Match count |
| `Contains(t)` | bool | Check existence |
| `Replace(t, r)` | string | Replace all |
| `ReplaceFirst(t, r)` | string | Replace first |
| `GetPattern()` | string | Get pattern |
| `GetPatternLength()` | int | Pattern length |
| `IsCaseSensitive()` | bool | Case sensitivity flag |

### Match Structure

```go
type Match struct {
    Position    int    // Start position (0-indexed)
    Text        string // Matched text
    EndPosition int    // End position (exclusive)
}
```

### PatternStats Structure

```go
type PatternStats struct {
    Length       int
    UniqueChars  int
    CharFreq     map[rune]int
    HasRepeated  bool
    IsPalindrome bool
}
```

## Examples

See `examples/main.go` for comprehensive usage examples including:
- Basic searches
- Case-insensitive matching
- Replace operations
- Multi-pattern search
- Pattern analysis
- Chinese character support
- Special character handling
- Log file parsing

## Testing

```bash
go test -v
```

## Benchmarks

```bash
go test -bench=.
```

## License

MIT License - Free for personal and commercial use.

## Part of AllToolkit

This module is part of the AllToolkit collection - zero-dependency utility libraries for multiple programming languages.