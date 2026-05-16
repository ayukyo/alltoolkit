# LCS Utils - Longest Common Subsequence Algorithms for Go

A comprehensive Go library implementing Longest Common Subsequence (LCS) algorithms for sequence comparison, diff operations, and text alignment.

## Features

### Core LCS Algorithms
- **LCS** - Standard dynamic programming LCS with O(m*n) time and space
- **LCSLength** - Space-optimized LCS length computation (O(min(m,n)) space)
- **LCSWithIndices** - LCS with indices in both sequences
- **LCSAll** - Find all possible LCS solutions
- **LCSOfMultiple** - LCS of multiple sequences (reduction approach)

### Specialized LCS
- **LCSString** - LCS for strings (character by character)
- **LCSStringLines** - LCS for multi-line text
- **LCSBytes** - LCS for byte slices
- **LCSHuntSzymanski** - Hunt-Szymanski algorithm (efficient for small match count)

### Diff Operations
- **Diff** - Compute differences between two sequences
- **DiffString** - Line-by-line diff for strings
- **ComputeDiffStats** - Statistics about changes (additions, deletions, similarity)

### Sequence Alignment
- **Align** - Sequence alignment based on LCS
- **AlignString** - String alignment

### Shortest Common Supersequence
- **SCS** - Compute Shortest Common Supersequence
- **SCSLength** - Length of SCS

### Edit Distance
- **EditDistance** - LCS-based edit distance (insert/delete only)
- **EditDistanceString** - Edit distance for strings

### Similarity Measures
- **SimilarityRatio** - Similarity between 0 and 1
- **SimilarityRatioString** - String similarity
- **JaccardSimilarity** - Jaccard similarity based on LCS

### Utility Functions
- **IsSubsequence** - Check if A is a subsequence of B
- **IsSubsequenceString** - Subsequence check for strings
- **AllSubsequences** - Generate all subsequences (2^n results)
- **CountCommonSubsequences** - Count common subsequences

## Installation

```go
import lcs "lcs_utils"
```

## Usage Examples

### Basic LCS

```go
a := []string{"A", "B", "C", "D", "G", "H"}
b := []string{"A", "E", "D", "F", "H", "R"}

lcsResult := lcs.LCS(a, b) // ["A", "D", "H"]
```

### LCS with Indices

```go
result := lcs.LCSWithIndices(a, b)
fmt.Println(result.Subsequence) // ["A", "D", "H"]
fmt.Println(result.IndicesA)    // [0, 3, 5]
fmt.Println(result.IndicesB)    // [0, 2, 4]
```

### String LCS

```go
str1 := "Hello, World!"
str2 := "Hlo ol!"
lcsStr := lcs.LCSString(str1, str2) // "Hlo ol!"
```

### Diff Operations

```go
seqA := []string{"a", "b", "c", "d"}
seqB := []string{"a", "x", "c", "y"}

diff := lcs.Diff(seqA, seqB)
for _, op := range diff {
    switch op.Type {
    case "equal":  // common element
    case "insert": // added in B
    case "delete": // removed from A
    }
}
```

### Similarity

```go
ratio := lcs.SimilarityRatio(a, b)    // value between 0 and 1
jaccard := lcs.JaccardSimilarity(a, b)
```

### Shortest Common Supersequence

```go
scsA := []string{"a", "b", "c"}
scsB := []string{"a", "c", "d"}
scs := lcs.SCS(scsA, scsB) // shortest sequence containing both
```

## Algorithm Complexity

| Algorithm | Time | Space |
|-----------|------|-------|
| LCS | O(m*n) | O(m*n) |
| LCSLength | O(m*n) | O(min(m,n)) |
| LCSAll | O(m*n + k) | O(m*n) |
| LCSHuntSzymanski | O((r+n)log n) | O(r) |

Where:
- m, n = lengths of sequences
- k = number of LCS solutions
- r = number of matches

## Applications

- **Version Control**: Diff algorithms for code comparison
- **Text Comparison**: Document similarity analysis
- **Bioinformatics**: DNA/RNA sequence alignment
- **Plagiarism Detection**: Text similarity measurement
- **Data Synchronization**: Finding common structure

## Test Coverage

48 unit tests covering:
- Basic LCS operations
- Edge cases (empty, single element, duplicates)
- Unicode support
- Large sequences
- Diff statistics
- Similarity measures
- Sequence alignment

Run tests:
```bash
go test -v
```

## Benchmarks

```bash
go test -bench=.
```

## License

MIT License