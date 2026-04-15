# diff_utils - Text Diff Utilities for Go

A comprehensive Go package for comparing and analyzing text differences. Supports line-level, word-level, and character-level diffs with zero external dependencies.

## Features

- **Multiple Diff Algorithms**: Line-by-line, word-by-word, and character-by-character comparison
- **Unified Diff Format**: Generate classic unified diff output
- **Colored Output**: ANSI-colored terminal output
- **HTML Output**: Web-ready HTML diff generation
- **Similarity Scoring**: Calculate text similarity (0-1 scale)
- **Levenshtein Distance**: Compute minimum edit distance
- **LCS (Longest Common Subsequence)**: Find common sequences
- **Unicode Support**: Full UTF-8 support including emojis
- **Zero Dependencies**: Uses only Go standard library

## Installation

```bash
go get github.com/ayukyo/alltoolkit/Go/diff_utils
```

## Quick Start

```go
package main

import (
    "fmt"
    "github.com/ayukyo/alltoolkit/Go/diff_utils"
)

func main() {
    // Compare two texts line by line
    old := "hello\nworld\nfoo"
    new := "hello\ngo\nbar"
    
    result := diff_utils.DiffLines(old, new)
    
    // Print statistics
    fmt.Printf("Added: %d, Removed: %d\n", 
        result.Stats.Added, result.Stats.Removed)
    
    // Print colored diff
    fmt.Println(diff_utils.FormatColor(result.Diffs))
}
```

## API Reference

### DiffLines

Compare two strings line by line:

```go
result := diff_utils.DiffLines(oldText, newText)
// result.Diffs - slice of diff operations
// result.Stats - statistics (added, removed, equal)
// result.LinesA, result.LinesB - line counts
```

### DiffChars

Compare at character level:

```go
diffs := diff_utils.DiffChars("kitten", "sitting")
for _, d := range diffs {
    switch d.Type {
    case diff_utils.Insert:
        fmt.Printf("+%s", d.Text)
    case diff_utils.Delete:
        fmt.Printf("-%s", d.Text)
    case diff_utils.Equal:
        fmt.Printf(" %s", d.Text)
    }
}
```

### DiffWords

Compare at word level:

```go
diffs := diff_utils.DiffWords("hello world", "hello beautiful world")
// Shows: "beautiful" was inserted
```

### Similarity

Calculate similarity score (0.0 to 1.0):

```go
score := diff_utils.Similarity("hello", "hallo")
// score ≈ 0.8 (4 out of 5 characters match)
```

### LevenshteinDistance

Compute minimum edit distance:

```go
dist := diff_utils.LevenshteinDistance("kitten", "sitting")
// dist = 3 (k→s, e→i, +g)
```

### LCS

Find longest common subsequence:

```go
lcs, length := diff_utils.LCS("ABCBDAB", "BDCABA")
// lcs = "BCBA" or similar, length = 4
```

### Output Formats

#### Unified Diff Format

```go
result := diff_utils.DiffLines(oldText, newText)
unified := diff_utils.FormatUnified(result, 3, "old.txt", "new.txt")
fmt.Println(unified)
```

Output:
```
--- old.txt
+++ new.txt
@@ -1,3 +1,3 @@
 line1
-line2
+modified
 line3
```

#### ANSI Colored Output

```go
fmt.Println(diff_utils.FormatColor(result.Diffs))
// Red for deletions, green for insertions
```

#### HTML Output

```go
html := diff_utils.FormatHTML(result.Diffs)
// Returns <del>, <ins>, <span> tags
```

## Examples

### Compare Files

```go
package main

import (
    "fmt"
    "os"
    "github.com/ayukyo/alltoolkit/Go/diff_utils"
)

func main() {
    oldData, _ := os.ReadFile("old.txt")
    newData, _ := os.ReadFile("new.txt")
    
    result := diff_utils.DiffLines(
        string(oldData), 
        string(newData),
    )
    
    fmt.Printf("Changes: +%d -%d\n", 
        result.Stats.Added, 
        result.Stats.Removed,
    )
    
    // Print unified diff
    fmt.Println(diff_utils.FormatUnified(result, 3, "old.txt", "new.txt"))
}
```

### Character-Level Diff with Colors

```go
package main

import (
    "fmt"
    "github.com/ayukyo/alltoolkit/Go/diff_utils"
)

func main() {
    diffs := diff_utils.DiffChars("The quick brown fox", "The fast brown dog")
    
    for _, d := range diffs {
        switch d.Type {
        case diff_utils.Delete:
            fmt.Printf("\033[31m[-%s]\033[0m", d.Text)
        case diff_utils.Insert:
            fmt.Printf("\033[32m[+%s]\033[0m", d.Text)
        case diff_utils.Equal:
            fmt.Printf("%s", d.Text)
        }
    }
    fmt.Println()
}
```

### Calculate Text Similarity

```go
package main

import (
    "fmt"
    "github.com/ayukyo/alltoolkit/Go/diff_utils"
)

func main() {
    texts := []struct {
        a, b string
    }{
        {"hello world", "hello world"},
        {"hello world", "hallo world"},
        {"hello world", "goodbye world"},
        {"hello world", "completely different"},
    }
    
    for _, t := range texts {
        score := diff_utils.Similarity(t.a, t.b)
        fmt.Printf("Similarity: %.2f | '%s' vs '%s'\n", 
            score, t.a, t.b)
    }
}
```

Output:
```
Similarity: 1.00 | 'hello world' vs 'hello world'
Similarity: 0.90 | 'hello world' vs 'hallo world'
Similarity: 0.55 | 'hello world' vs 'goodbye world'
Similarity: 0.00 | 'hello world' vs 'completely different'
```

### Unicode Support

```go
package main

import (
    "fmt"
    "github.com/ayukyo/alltoolkit/Go/diff_utils"
)

func main() {
    // Chinese characters
    diffs := diff_utils.DiffChars("你好世界", "你好中国")
    // Shows: "世界" → "中国"
    
    // Emoji
    result := diff_utils.DiffLines(
        "Hello 👋 World\nEmoji 🌍",
        "Hello 🖐️ World\nEmoji 🌏",
    )
    fmt.Printf("Changed lines: %d\n", 
        result.Stats.Added + result.Stats.Removed)
}
```

## Performance

Optimized for performance with:
- O(mn) time complexity for LCS-based algorithms
- O(n) space optimization for Levenshtein distance
- Zero allocations for identical inputs
- Early termination for empty/different inputs

Benchmarks (on typical laptop):
- DiffLines (1000 lines): ~1ms
- LevenshteinDistance (1000 chars): ~0.5ms
- DiffChars (500 chars): ~0.3ms

## License

MIT License