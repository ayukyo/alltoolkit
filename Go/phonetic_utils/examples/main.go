// Example usage of phonetic_utils package
package main

import (
	"fmt"
	"strings"

	phonetic "github.com/ayukyo/alltoolkit/Go/phonetic_utils"
)

func main() {
	fmt.Println("=== Phonetic Encoding Examples ===")
	fmt.Println()

	// Example 1: Soundex encoding
	fmt.Println("1. Soundex Encoding:")
	names := []string{"Robert", "Rupert", "Smith", "Schmidt", "Johnson", "Jonson"}
	for _, name := range names {
		code := phonetic.Soundex(name)
		fmt.Printf("   %s -> %s\n", name, code)
	}
	fmt.Println()

	// Example 2: Metaphone encoding
	fmt.Println("2. Metaphone Encoding:")
	names = []string{"Smith", "Schmidt", "phone", "knight", "psychology"}
	for _, name := range names {
		code := phonetic.Metaphone(name)
		fmt.Printf("   %s -> %s\n", name, code)
	}
	fmt.Println()

	// Example 3: NYSIIS encoding
	fmt.Println("3. NYSIIS Encoding:")
	names = []string{"Smith", "Schmidt", "Johnson", "O'Connor"}
	for _, name := range names {
		code := phonetic.NYSIIS(name)
		fmt.Printf("   %s -> %s\n", name, code)
	}
	fmt.Println()

	// Example 4: Match Rating Codex
	fmt.Println("4. Match Rating Codex:")
	names = []string{"Smith", "Johnson", "O'Connor"}
	for _, name := range names {
		code := phonetic.MatchRatingCodex(name)
		fmt.Printf("   %s -> %s\n", name, code)
	}
	fmt.Println()

	// Example 5: Encode all algorithms at once
	fmt.Println("5. Encode All Algorithms:")
	result := phonetic.EncodeAll("Smith")
	fmt.Printf("   Soundex:          %s\n", result.Soundex)
	fmt.Printf("   Metaphone:        %s\n", result.Metaphone)
	fmt.Printf("   RefinedSoundex:   %s\n", result.RefinedSoundex)
	fmt.Printf("   NYSIIS:           %s\n", result.NYSIIS)
	fmt.Printf("   MatchRatingCodex: %s\n", result.MatchRatingCodex)
	fmt.Println()

	// Example 6: Phonetic matching
	fmt.Println("6. Phonetic Matching:")
	fmt.Printf("   Soundex match (Smith vs Schmidt): %v\n", phonetic.PhoneticMatch("Smith", "Schmidt", phonetic.AlgorithmSoundex))
	fmt.Printf("   Metaphone match (Smith vs Schmidt): %v\n", phonetic.PhoneticMatch("Smith", "Schmidt", phonetic.AlgorithmMetaphone))
	fmt.Println()

	// Example 7: Phonetic similarity score
	fmt.Println("7. Phonetic Similarity Score:")
	similarity := phonetic.PhoneticSimilarity("Smith", "Schmidt")
	fmt.Printf("   Smith vs Schmidt: %.2f%%\n", similarity*100)

	similarity = phonetic.PhoneticSimilarity("John", "Jane")
	fmt.Printf("   John vs Jane: %.2f%%\n", similarity*100)
	fmt.Println()

	// Example 8: Find matches from candidates
	fmt.Println("8. Find Matches:")
	candidates := []string{"Smith", "Schmidt", "Smythe", "Johnson", "Jonson", "Williams"}
	matches := phonetic.FindMatches("Smith", candidates, phonetic.AlgorithmSoundex, 0.5)
	fmt.Println("   Matches for 'Smith':")
	for _, match := range matches {
		fmt.Printf("     %s (code: %s, similarity: %.2f%%)\n", match.Name, match.Code, match.Similarity*100)
	}
	fmt.Println()

	// Example 9: Batch encoding
	fmt.Println("9. Batch Encoding:")
	names = []string{"Smith", "Schmidt", "Johnson", "Williams"}
	batchResult := phonetic.BatchEncode(names, phonetic.AlgorithmSoundex)
	for name, code := range batchResult {
		fmt.Printf("   %s -> %s\n", name, code)
	}
	fmt.Println()

	// Example 10: Name deduplication example
	fmt.Println("10. Name Deduplication Example:")
	duplicateNames := []string{
		"John Smith", "Jon Smith", "J. Smith",
		"Robert Johnson", "Rupert Johnson", "Rob Johnson",
		"William Brown", "Wm Brown", "Bill Brown",
	}

	// Group by Soundex code
	groups := make(map[string][]string)
	for _, fullName := range duplicateNames {
		parts := strings.Fields(fullName)
		if len(parts) >= 2 {
			code := phonetic.Soundex(parts[0])
			key := code + "-" + phonetic.Soundex(parts[len(parts)-1])
			groups[key] = append(groups[key], fullName)
		}
	}

	fmt.Println("   Potential duplicate groups:")
	for key, names := range groups {
		if len(names) > 1 {
			fmt.Printf("     %s: %v\n", key, names)
		}
	}
	fmt.Println()

	// Example 11: Real-world search with fuzzy matching
	fmt.Println("11. Search with Phonetic Tolerance:")
	searchTerm := "Catherine"
	database := []string{
		"Catherine", "Katherine", "Kathryn", "Catherina",
		"Katarina", "Catharine", "Katharine", "John", "Jane",
	}

	fmt.Printf("   Searching for '%s' with tolerance:\n", searchTerm)
	for _, name := range database {
		sim := phonetic.PhoneticSimilarity(searchTerm, name)
		if sim >= 0.6 {
			fmt.Printf("     Found: %s (similarity: %.2f%%)\n", name, sim*100)
		}
	}
	fmt.Println()

	// Example 12: Using algorithm constants
	fmt.Println("12. Using Algorithm Constants:")
	algorithms := []phonetic.PhoneticAlgorithm{
		phonetic.AlgorithmSoundex,
		phonetic.AlgorithmMetaphone,
		phonetic.AlgorithmRefinedSoundex,
		phonetic.AlgorithmNYSIIS,
		phonetic.AlgorithmMatchRatingCodex,
	}

	testName := "Robert"
	fmt.Printf("   Encoding '%s' with all algorithms:\n", testName)
	for _, alg := range algorithms {
		code := alg.Encode(testName)
		fmt.Printf("     Algorithm %d: %s\n", alg, code)
	}
	fmt.Println()

	fmt.Println("=== All examples completed successfully! ===")
}