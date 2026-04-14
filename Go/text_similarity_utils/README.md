# Text Similarity Utils (Go)

A comprehensive Go package for calculating text similarity using multiple algorithms. Zero external dependencies.

## Features

- **10+ Similarity Algorithms:**
  - Levenshtein Distance
  - Damerau-Levenshtein Distance (with transpositions)
  - Jaccard Similarity (n-gram and word-based)
  - Cosine Similarity
  - Sørensen-Dice Coefficient
  - Hamming Distance
  - Jaro Similarity
  - Jaro-Winkler Similarity
  - Soundex (phonetic matching)
  - N-Gram Similarity

- **Utility Functions:**
  - `MostSimilar()` - Find best match from candidates
  - `AllSimilarities()` - Get ranked similarity scores

- **Full Unicode Support:** Chinese, Japanese, Korean, Emoji
- **Zero Dependencies:** Pure Go standard library

## Installation

```bash
go get github.com/ayukyo/alltoolkit/Go/text_similarity_utils
```

## Quick Start

```go
package main

import (
    "fmt"
    tsu "github.com/ayukyo/alltoolkit/Go/text_similarity_utils"
)

func main() {
    // Levenshtein Distance
    dist := tsu.LevenshteinDistance("kitten", "sitting")
    fmt.Printf("Distance: %d\n", dist) // Output: 3
    
    // Levenshtein Similarity (0-1)
    sim := tsu.LevenshteinSimilarity("kitten", "sitting")
    fmt.Printf("Similarity: %.2f%%\n", sim*100) // Output: 57.14%
    
    // Jaro-Winkler (prefix-sensitive, great for names)
    jw := tsu.JaroWinklerSimilarity("MARTHA", "MARHTA")
    fmt.Printf("J-W: %.2f%%\n", jw*100) // Output: 96.11%
    
    // Find best match
    result := tsu.MostSimilar("hello", []string{"hallo", "helo", "world"}, "jarowinkler", 2)
    fmt.Printf("Best match: %s (%.2f%%)\n", result.Text, result.Score*100)
}
```

## API Reference

### Distance Functions

```go
// Levenshtein - minimum single-character edits
func LevenshteinDistance(s1, s2 string) int
func LevenshteinSimilarity(s1, s2 string) float64

// Damerau-Levenshtein - includes adjacent transpositions
func DamerauLevenshteinDistance(s1, s2 string) int

// Hamming - for equal-length strings only
func HammingDistance(s1, s2 string) int
func HammingSimilarity(s1, s2 string) float64
```

### Similarity Functions (0-1 scale)

```go
// Jaccard - set intersection/union
func JaccardSimilarity(s1, s2 string, ngramSize int) float64
func JaccardSimilarityWords(s1, s2 string) float64

// Cosine - vector space model
func CosineSimilarity(s1, s2 string, ngramSize int) float64

// Sørensen-Dice
func SorensenDiceCoefficient(s1, s2 string, ngramSize int) float64

// Jaro & Jaro-Winkler
func JaroSimilarity(s1, s2 string) float64
func JaroWinklerSimilarity(s1, s2 string) float64

// N-Gram
func NGramSimilarity(s1, s2 string, n int) float64
```

### Phonetic Matching

```go
// Soundex - phonetic encoding
func Soundex(s string) string
func SoundexSimilarity(s1, s2 string) float64
```

### Utility Functions

```go
type SimilarityResult struct {
    Text      string
    Score     float64
    Algorithm string
}

// Find most similar string
// Algorithms: "levenshtein", "jaro", "jarowinkler", "jaccard", "cosine", "dice", "ngram", "soundex"
func MostSimilar(target string, candidates []string, algorithm string, ngramSize int) SimilarityResult

// Get all similarities ranked by score
func AllSimilarities(target string, candidates []string, algorithm string, ngramSize int) []SimilarityResult
```

## Algorithm Selection Guide

| Use Case | Recommended Algorithm |
|----------|----------------------|
| Spell checking | Levenshtein |
| Name matching | Jaro-Winkler |
| Document similarity | Cosine |
| Fuzzy search | Jaro-Winkler or Dice |
| Phonetic matching | Soundex |
| Short strings | Jaccard |
| Equal-length comparison | Hamming |

## Examples

### Spell Checking

```go
// Find closest dictionary word
dictionary := []string{"accommodate", "necessary", "separate", "definitely"}
result := tsu.MostSimilar("accomodate", dictionary, "levenshtein", 2)
// result.Text = "accommodate"
```

### Name Matching

```go
// Match names despite typos
candidates := []string{"Robert", "Rupert", "Robin", "Ruben"}
result := tsu.MostSimilar("Robart", candidates, "jarowinkler", 2)
// result.Text = "Robert"
```

### Phonetic Search

```go
// Find phonetically similar names
tsu.Soundex("Robert")    // "R163"
tsu.Soundex("Rupert")    // "R163"
tsu.SoundexSimilarity("Robert", "Rupert")  // 1.0 (same soundex)
```

## Running Tests

```bash
go test ./...
```

With benchmarks:

```bash
go test -bench=. ./...
```

## License

MIT