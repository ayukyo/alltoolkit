package main

import (
	"fmt"
	"strings"

	lcs "lcs_utils"
)

func main() {
	fmt.Println("=== LCS (Longest Common Subsequence) Utils Examples ===")
	fmt.Println()

	// Example 1: Basic LCS
	fmt.Println("--- Example 1: Basic LCS ---")
	a := []string{"A", "B", "C", "D", "G", "H"}
	b := []string{"A", "E", "D", "F", "H", "R"}

	lcsResult := lcs.LCS(a, b)
	fmt.Printf("Sequence A: %v\n", a)
	fmt.Printf("Sequence B: %v\n", b)
	fmt.Printf("LCS: %v\n", lcsResult)
	fmt.Printf("LCS Length: %d\n", len(lcsResult))
	fmt.Println()

	// Example 2: LCS with Indices
	fmt.Println("--- Example 2: LCS with Indices ---")
	result := lcs.LCSWithIndices(a, b)
	fmt.Printf("LCS: %v\n", result.Subsequence)
	fmt.Printf("Indices in A: %v\n", result.IndicesA)
	fmt.Printf("Indices in B: %v\n", result.IndicesB)
	fmt.Println()

	// Example 3: LCS on Strings
	fmt.Println("--- Example 3: LCS on Strings ---")
	str1 := "Hello, World!"
	str2 := "Hlo ol!"

	lcsStr := lcs.LCSString(str1, str2)
	fmt.Printf("String 1: %s\n", str1)
	fmt.Printf("String 2: %s\n", str2)
	fmt.Printf("LCS: %s\n", lcsStr)
	fmt.Println()

	// Example 4: LCS on Lines (for diff-like operations)
	fmt.Println("--- Example 4: LCS on Lines ---")
	text1 := "line1\nline2\nline3\nline4"
	text2 := "line1\nlineX\nline3\nline5"

	lcsLines := lcs.LCSStringLines(text1, text2)
	fmt.Printf("Text 1: %s\n", strings.ReplaceAll(text1, "\n", " → "))
	fmt.Printf("Text 2: %s\n", strings.ReplaceAll(text2, "\n", " → "))
	fmt.Printf("Common lines: %v\n", lcsLines)
	fmt.Println()

	// Example 5: Diff Operations
	fmt.Println("--- Example 5: Diff Operations ---")
	seqA := []string{"a", "b", "c", "d"}
	seqB := []string{"a", "x", "c", "y"}

	diff := lcs.Diff(seqA, seqB)
	fmt.Printf("Sequence A: %v\n", seqA)
	fmt.Printf("Sequence B: %v\n", seqB)
	fmt.Println("Diff operations:")
	for _, op := range diff {
		switch op.Type {
		case "equal":
			fmt.Printf("  = %s (A:%d, B:%d)\n", op.Value, op.IndexA, op.IndexB)
		case "insert":
			fmt.Printf("  + %s (B:%d)\n", op.Value, op.IndexB)
		case "delete":
			fmt.Printf("  - %s (A:%d)\n", op.Value, op.IndexA)
		}
	}
	fmt.Println()

	// Example 6: Diff Statistics
	fmt.Println("--- Example 6: Diff Statistics ---")
	stats := lcs.ComputeDiffStats(diff)
	fmt.Printf("Additions: %d\n", stats.Additions)
	fmt.Printf("Deletions: %d\n", stats.Deletions)
	fmt.Printf("Unchanged: %d\n", stats.Unchanged)
	fmt.Printf("Similarity: %.2f%%\n", stats.Similarity*100)
	fmt.Println()

	// Example 7: Sequence Alignment
	fmt.Println("--- Example 7: Sequence Alignment ---")
	alignA := []string{"A", "B", "C", "D"}
	alignB := []string{"A", "X", "C", "Y"}

	alignment := lcs.Align(alignA, alignB)
	fmt.Printf("Sequence A: %v\n", alignA)
	fmt.Printf("Sequence B: %v\n", alignB)
	fmt.Printf("Aligned A: %v\n", alignment.AlignedA)
	fmt.Printf("Aligned B: %v\n", alignment.AlignedB)
	fmt.Printf("LCS: %v\n", alignment.LCS)
	fmt.Printf("Score: %d\n", alignment.Score)
	fmt.Println()

	// Example 8: Similarity Measures
	fmt.Println("--- Example 8: Similarity Measures ---")
	simA := []string{"hello", "world", "test"}
	simB := []string{"hello", "universe", "test"}

	ratio := lcs.SimilarityRatio(simA, simB)
	jaccard := lcs.JaccardSimilarity(simA, simB)
	fmt.Printf("Sequence A: %v\n", simA)
	fmt.Printf("Sequence B: %v\n", simB)
	fmt.Printf("Similarity Ratio: %.2f\n", ratio)
	fmt.Printf("Jaccard Similarity: %.2f\n", jaccard)
	fmt.Println()

	// Example 9: Shortest Common Supersequence
	fmt.Println("--- Example 9: Shortest Common Supersequence ---")
	scsA := []string{"a", "b", "c"}
	scsB := []string{"a", "c", "d"}

	scs := lcs.SCS(scsA, scsB)
	fmt.Printf("Sequence A: %v\n", scsA)
	fmt.Printf("Sequence B: %v\n", scsB)
	fmt.Printf("SCS: %v\n", scs)
	fmt.Printf("SCS Length: %d (expected: %d)\n", len(scs), lcs.SCSLength(scsA, scsB))
	fmt.Println()

	// Example 10: Edit Distance
	fmt.Println("--- Example 10: Edit Distance ---")
	editA := []string{"a", "b", "c", "d"}
	editB := []string{"a", "c"}

	editDist := lcs.EditDistance(editA, editB)
	fmt.Printf("Sequence A: %v\n", editA)
	fmt.Printf("Sequence B: %v\n", editB)
	fmt.Printf("Edit Distance (insert/delete only): %d\n", editDist)
	fmt.Println()

	// Example 11: Multiple Sequence LCS
	fmt.Println("--- Example 11: Multiple Sequence LCS ---")
	seq1 := []string{"a", "b", "c", "d", "e"}
	seq2 := []string{"a", "c", "e"}
	seq3 := []string{"a", "b", "e"}

	multiLcs := lcs.LCSOfMultiple(seq1, seq2, seq3)
	fmt.Printf("Sequence 1: %v\n", seq1)
	fmt.Printf("Sequence 2: %v\n", seq2)
	fmt.Printf("Sequence 3: %v\n", seq3)
	fmt.Printf("Common LCS: %v\n", multiLcs)
	fmt.Println()

	// Example 12: Subsequence Check
	fmt.Println("--- Example 12: Subsequence Check ---")
	sub := []string{"a", "c"}
	super := []string{"a", "b", "c", "d"}

	isSub := lcs.IsSubsequence(sub, super)
	fmt.Printf("Subsequence: %v\n", sub)
	fmt.Printf("Supersequence: %v\n", super)
	fmt.Printf("Is subsequence: %v\n", isSub)
	fmt.Println()

	// Example 13: Space-Optimized LCS Length
	fmt.Println("--- Example 13: Space-Optimized LCS Length ---")
	longA := make([]string, 1000)
	longB := make([]string, 1000)
	for i := 0; i < 1000; i++ {
		longA[i] = string(rune('a' + i%26))
		longB[i] = string(rune('a' + i%26))
	}

	lcsLen := lcs.LCSLength(longA, longB)
	fmt.Printf("Length of A: %d\n", len(longA))
	fmt.Printf("Length of B: %d\n", len(longB))
	fmt.Printf("LCS Length (space-optimized): %d\n", lcsLen)
	fmt.Println()

	// Example 14: Code Comparison
	fmt.Println("--- Example 14: Code Comparison ---")
	code1 := []string{
		"func main() {",
		"    fmt.Println(\"hello\")",
		"    fmt.Println(\"world\")",
		"}",
	}

	code2 := []string{
		"func main() {",
		"    fmt.Println(\"hello\")",
		"    fmt.Println(\"go\")",
		"    fmt.Println(\"lang\")",
		"}",
	}

	codeLcs := lcs.LCS(code1, code2)
	fmt.Println("Code 1:")
	for _, line := range code1 {
		fmt.Printf("  %s\n", line)
	}
	fmt.Println("Code 2:")
	for _, line := range code2 {
		fmt.Printf("  %s\n", line)
	}
	fmt.Printf("Common lines (%d):\n", len(codeLcs))
	for _, line := range codeLcs {
		fmt.Printf("  %s\n", line)
	}

	codeDiff := lcs.ComputeDiffStats(lcs.Diff(code1, code2))
	fmt.Printf("Similarity: %.2f%%\n", codeDiff.Similarity*100)
	fmt.Println()

	// Example 15: Unicode Support
	fmt.Println("--- Example 15: Unicode Support ---")
	unicode1 := "你好世界"
	unicode2 := "你好"

	unicodeLcs := lcs.LCSString(unicode1, unicode2)
	fmt.Printf("String 1: %s\n", unicode1)
	fmt.Printf("String 2: %s\n", unicode2)
	fmt.Printf("LCS: %s\n", unicodeLcs)
	fmt.Println()

	fmt.Println("=== All Examples Completed ===")
}