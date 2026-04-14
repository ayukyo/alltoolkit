// Example usage of text_similarity_utils package
package main

import (
	"fmt"
	"strings"

	tsu "github.com/ayukyo/alltoolkit/Go/text_similarity_utils"
)

func main() {
	fmt.Println("╔══════════════════════════════════════════════════════════════╗")
	fmt.Println("║        Text Similarity Utils - Complete Examples            ║")
	fmt.Println("╚══════════════════════════════════════════════════════════════╝")
	fmt.Println()

	// ============================================================
	// 1. Levenshtein Distance & Similarity
	// ============================================================
	fmt.Println("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
	fmt.Println("1. Levenshtein Distance & Similarity")
	fmt.Println("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

	examples := []struct {
		s1, s2 string
	}{
		{"kitten", "sitting"},
		{"saturday", "sunday"},
		{"algorithm", "logarithm"},
		{"hello", "hallo"},
	}

	for _, ex := range examples {
		dist := tsu.LevenshteinDistance(ex.s1, ex.s2)
		sim := tsu.LevenshteinSimilarity(ex.s1, ex.s2)
		fmt.Printf("  %q vs %q\n", ex.s1, ex.s2)
		fmt.Printf("    Distance: %d, Similarity: %.2f%%\n", dist, sim*100)
	}
	fmt.Println()

	// ============================================================
	// 2. Damerau-Levenshtein Distance (with transpositions)
	// ============================================================
	fmt.Println("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
	fmt.Println("2. Damerau-Levenshtein Distance (includes adjacent transpositions)")
	fmt.Println("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

	damerauExamples := []struct {
		s1, s2 string
	}{
		{"ca", "abc"},
		{"abcd", "acbd"}, // transposition: b↔c
		{"recieve", "receive"},
	}

	for _, ex := range damerauExamples {
		dist := tsu.DamerauLevenshteinDistance(ex.s1, ex.s2)
		levDist := tsu.LevenshteinDistance(ex.s1, ex.s2)
		fmt.Printf("  %q vs %q\n", ex.s1, ex.s2)
		fmt.Printf("    Damerau-Levenshtein: %d, Levenshtein: %d\n", dist, levDist)
	}
	fmt.Println()

	// ============================================================
	// 3. Jaccard Similarity
	// ============================================================
	fmt.Println("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
	fmt.Println("3. Jaccard Similarity (n-gram based)")
	fmt.Println("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

	jaccardExamples := []struct {
		s1, s2 string
		ngram  int
	}{
		{"night", "nacht", 2},
		{"hello world", "hello there", 2},
		{"apple", "apply", 2},
	}

	for _, ex := range jaccardExamples {
		sim := tsu.JaccardSimilarity(ex.s1, ex.s2, ex.ngram)
		wordSim := tsu.JaccardSimilarityWords(ex.s1, ex.s2)
		fmt.Printf("  %q vs %q (n=%d)\n", ex.s1, ex.s2, ex.ngram)
		fmt.Printf("    N-gram Jaccard: %.2f%%, Word Jaccard: %.2f%%\n", sim*100, wordSim*100)
	}
	fmt.Println()

	// ============================================================
	// 4. Cosine Similarity
	// ============================================================
	fmt.Println("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
	fmt.Println("4. Cosine Similarity (vector space model)")
	fmt.Println("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

	cosineExamples := []struct {
		s1, s2 string
		ngram  int
	}{
		{"the quick brown fox", "the quick fox jumps", 2},
		{"hello world", "hello there", 2},
		{"programming", "programmer", 3},
	}

	for _, ex := range cosineExamples {
		sim := tsu.CosineSimilarity(ex.s1, ex.s2, ex.ngram)
		fmt.Printf("  %q vs %q (n=%d)\n", ex.s1, ex.s2, ex.ngram)
		fmt.Printf("    Cosine Similarity: %.2f%%\n", sim*100)
	}
	fmt.Println()

	// ============================================================
	// 5. Sorensen-Dice Coefficient
	// ============================================================
	fmt.Println("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
	fmt.Println("5. Sørensen-Dice Coefficient")
	fmt.Println("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

	diceExamples := []struct {
		s1, s2 string
		ngram  int
	}{
		{"night", "nacht", 2},
		{"hello", "hallo", 2},
		{"comparing", "comparison", 2},
	}

	for _, ex := range diceExamples {
		sim := tsu.SorensenDiceCoefficient(ex.s1, ex.s2, ex.ngram)
		fmt.Printf("  %q vs %q\n", ex.s1, ex.s2)
		fmt.Printf("    Sørensen-Dice: %.2f%%\n", sim*100)
	}
	fmt.Println()

	// ============================================================
	// 6. Hamming Distance & Similarity
	// ============================================================
	fmt.Println("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
	fmt.Println("6. Hamming Distance (for equal-length strings)")
	fmt.Println("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

	hammingExamples := []struct {
		s1, s2 string
	}{
		{"karolin", "kathrin"},
		{"1011101", "1001001"},
		{"hello", "hallo"},
	}

	for _, ex := range hammingExamples {
		dist := tsu.HammingDistance(ex.s1, ex.s2)
		sim := tsu.HammingSimilarity(ex.s1, ex.s2)
		fmt.Printf("  %q vs %q\n", ex.s1, ex.s2)
		fmt.Printf("    Distance: %d, Similarity: %.2f%%\n", dist, sim*100)
	}
	fmt.Println()

	// ============================================================
	// 7. Jaro & Jaro-Winkler Similarity
	// ============================================================
	fmt.Println("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
	fmt.Println("7. Jaro & Jaro-Winkler Similarity")
	fmt.Println("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

	jaroExamples := []struct {
		s1, s2 string
	}{
		{"MARTHA", "MARHTA"},
		{"DWAYNE", "DUANE"},
		{"hello", "hallo"},
		{"crATE", "trace"},
	}

	for _, ex := range jaroExamples {
		jaro := tsu.JaroSimilarity(ex.s1, ex.s2)
		jw := tsu.JaroWinklerSimilarity(ex.s1, ex.s2)
		fmt.Printf("  %q vs %q\n", ex.s1, ex.s2)
		fmt.Printf("    Jaro: %.2f%%, Jaro-Winkler: %.2f%%\n", jaro*100, jw*100)
	}
	fmt.Println()

	// ============================================================
	// 8. Soundex (phonetic similarity)
	// ============================================================
	fmt.Println("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
	fmt.Println("8. Soundex (phonetic similarity)")
	fmt.Println("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

	soundexExamples := []string{
		"Robert", "Rupert", "Rubin", "Robin",
		"Ashcraft", "Ashcroft",
		"Tymczak", "Pfister",
	}

	for _, name := range soundexExamples {
		code := tsu.Soundex(name)
		fmt.Printf("  %-12s → %s\n", name, code)
	}

	// Soundex comparison
	fmt.Println("\n  Phonetically similar pairs:")
	pairs := [][2]string{
		{"Robert", "Rupert"},
		{"Ashcraft", "Ashcroft"},
		{"Smith", "Smythe"},
	}
	for _, pair := range pairs {
		sim := tsu.SoundexSimilarity(pair[0], pair[1])
		fmt.Printf("    %q vs %q: %.0f%%\n", pair[0], pair[1], sim*100)
	}
	fmt.Println()

	// ============================================================
	// 9. N-Gram Similarity
	// ============================================================
	fmt.Println("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
	fmt.Println("9. N-Gram Similarity")
	fmt.Println("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

	ngramExamples := []struct {
		s1, s2 string
		n      int
	}{
		{"hello", "hallo", 2},
		{"hello", "hallo", 3},
		{"programming", "programmer", 2},
		{"programming", "programmer", 3},
	}

	for _, ex := range ngramExamples {
		sim := tsu.NGramSimilarity(ex.s1, ex.s2, ex.n)
		fmt.Printf("  %q vs %q (n=%d)\n", ex.s1, ex.s2, ex.n)
		fmt.Printf("    Similarity: %.2f%%\n", sim*100)
	}
	fmt.Println()

	// ============================================================
	// 10. Most Similar (Best Match)
	// ============================================================
	fmt.Println("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
	fmt.Println("10. Most Similar (Finding Best Match)")
	fmt.Println("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

	target := "hello"
	candidates := []string{"hallo", "helo", "hell", "help", "held", "yellow", "helicopter"}

	algorithms := []string{"levenshtein", "jaro", "jarowinkler", "jaccard", "cosine", "dice"}

	fmt.Printf("  Target: %q\n", target)
	fmt.Printf("  Candidates: %v\n\n", candidates)

	for _, algo := range algorithms {
		result := tsu.MostSimilar(target, candidates, algo, 2)
		fmt.Printf("    %-15s → %q (%.2f%%)\n", algo+":", result.Text, result.Score*100)
	}
	fmt.Println()

	// ============================================================
	// 11. All Similarities (Ranked Results)
	// ============================================================
	fmt.Println("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
	fmt.Println("11. All Similarities (Ranked Results)")
	fmt.Println("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

	searchTarget := "apple"
	fruits := []string{"apply", "apples", "orange", "banana", "pineapple", "grape"}

	fmt.Printf("  Target: %q\n", searchTarget)
	fmt.Printf("  Candidates: %v\n\n", fruits)

	results := tsu.AllSimilarities(searchTarget, fruits, "jarowinkler", 2)

	fmt.Println("  Ranked by Jaro-Winkler similarity:")
	for i, r := range results {
		bar := strings.Repeat("█", int(r.Score*30))
		fmt.Printf("    %d. %-12s %s %.2f%%\n", i+1, r.Text, bar, r.Score*100)
	}
	fmt.Println()

	// ============================================================
	// 12. Unicode Support
	// ============================================================
	fmt.Println("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
	fmt.Println("12. Unicode Support (Chinese, Japanese, Emoji)")
	fmt.Println("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

	// Chinese
	fmt.Println("  Chinese characters:")
	chinese := [][2]string{
		{"北京", "南京"},
		{"你好世界", "你好中国"},
		{"数据库", "数理库"},
	}
	for _, pair := range chinese {
		sim := tsu.LevenshteinSimilarity(pair[0], pair[1])
		fmt.Printf("    %s vs %s: %.2f%%\n", pair[0], pair[1], sim*100)
	}

	// Japanese
	fmt.Println("\n  Japanese:")
	japanese := [][2]string{
		{"日本語", "日本語"},
		{"こんにちは", "こんばんは"},
	}
	for _, pair := range japanese {
		sim := tsu.JaroWinklerSimilarity(pair[0], pair[1])
		fmt.Printf("    %s vs %s: %.2f%%\n", pair[0], pair[1], sim*100)
	}

	// Emoji
	fmt.Println("\n  Emoji:")
	emoji := [][2]string{
		{"😀😁😂", "😀😃😂"},
		{"👍👎", "👍👍"},
	}
	for _, pair := range emoji {
		dist := tsu.LevenshteinDistance(pair[0], pair[1])
		sim := tsu.LevenshteinSimilarity(pair[0], pair[1])
		fmt.Printf("    %s vs %s: distance=%d, similarity=%.2f%%\n", pair[0], pair[1], dist, sim*100)
	}
	fmt.Println()

	// ============================================================
	// 13. Algorithm Comparison
	// ============================================================
	fmt.Println("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
	fmt.Println("13. Algorithm Comparison for Different Scenarios")
	fmt.Println("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

	fmt.Println("\n  Scenario: Spell checking (find closest match)")
	spellCheck := []string{"accomodate", "accommodate", "acommodate", "accomadate"}
	correct := "accommodate"
	for _, word := range spellCheck {
		result := tsu.MostSimilar(correct, []string{word}, "levenshtein", 2)
		fmt.Printf("    %q vs %q: %.2f%%\n", correct, word, result.Score*100)
	}

	fmt.Println("\n  Scenario: Fuzzy search (prefix preference)")
	searches := []string{"document", "documentary", "doc", "documentation"}
	query := "doc"
	for _, word := range searches {
		jw := tsu.JaroWinklerSimilarity(query, word)
		lev := tsu.LevenshteinSimilarity(query, word)
		fmt.Printf("    %q vs %q: J-W=%.2f%%, Lev=%.2f%%\n", query, word, jw*100, lev*100)
	}

	fmt.Println("\n  Scenario: Name matching (phonetic)")
	names := []string{"Smith", "Smythe", "Schmidt", "Smithe"}
	for _, name := range names {
		code := tsu.Soundex(name)
		fmt.Printf("    %q → Soundex: %s\n", name, code)
	}

	fmt.Println()
	fmt.Println("════════════════════════════════════════════════════════════════")
	fmt.Println("                    Examples Complete! ✓")
	fmt.Println("════════════════════════════════════════════════════════════════")
}