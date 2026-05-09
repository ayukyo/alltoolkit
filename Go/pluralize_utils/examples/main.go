// Example usage of pluralize_utils package
package main

import (
	"fmt"
	"strings"

	pluralize "github.com/ayukyo/alltoolkit/Go/pluralize_utils"
)

func main() {
	fmt.Println("=== Pluralize Utils Examples ===")
	fmt.Println()

	// 1. Basic singular to plural conversion
	fmt.Println("1. Singular to Plural:")
	words := []string{"cat", "dog", "box", "city", "knife", "child", "man", "woman"}
	for _, word := range words {
		plural := pluralize.SingularToPlural(word)
		fmt.Printf("   %s -> %s\n", word, plural)
	}
	fmt.Println()

	// 2. Plural to singular conversion
	fmt.Println("2. Plural to Singular:")
	plurals := []string{"cats", "dogs", "boxes", "cities", "knives", "children", "men", "women"}
	for _, word := range plurals {
		singular := pluralize.PluralToSingular(word)
		fmt.Printf("   %s -> %s\n", word, singular)
	}
	fmt.Println()

	// 3. Latin/Greek origin words
	fmt.Println("3. Latin/Greek Origin Words:")
	latinWords := []string{"analysis", "phenomenon", "criterion", "datum", "focus", "stimulus"}
	for _, word := range latinWords {
		plural := pluralize.SingularToPlural(word)
		fmt.Printf("   %s -> %s\n", word, plural)
	}
	fmt.Println()

	// 4. Uncountable nouns
	fmt.Println("4. Uncountable Nouns (No Change):")
	uncountable := []string{"sheep", "deer", "fish", "information", "news", "series"}
	for _, word := range uncountable {
		plural := pluralize.SingularToPlural(word)
		fmt.Printf("   %s -> %s (unchanged)\n", word, plural)
	}
	fmt.Println()

	// 5. Case preservation
	fmt.Println("5. Case Preservation:")
	caseWords := []string{"Cat", "CAT", "Child", "MAN"}
	for _, word := range caseWords {
		plural := pluralize.SingularToPlural(word)
		fmt.Printf("   %s -> %s\n", word, plural)
	}
	fmt.Println()

	// 6. With count parameter
	fmt.Println("6. With Count Parameter:")
	fmt.Printf("   cat with count 1: %s\n", pluralize.SingularToPlural("cat", 1))
	fmt.Printf("   cat with count 2: %s\n", pluralize.SingularToPlural("cat", 2))
	fmt.Printf("   cat with count 0: %s\n", pluralize.SingularToPlural("cat", 0))
	fmt.Println()

	// 7. Check if word is plural
	fmt.Println("7. Is Plural Check:")
	checkWords := []string{"cat", "cats", "box", "boxes", "man", "men", "news", "sheep"}
	for _, word := range checkWords {
		isPlural := pluralize.IsPlural(word)
		fmt.Printf("   %s: %v\n", word, isPlural)
	}
	fmt.Println()

	// 8. Get plural form based on count
	fmt.Println("8. Get Plural Form by Count:")
	fmt.Printf("   cat with count 1: %s\n", pluralize.GetPluralForm("cat", 1))
	fmt.Printf("   cat with count 5: %s\n", pluralize.GetPluralForm("cat", 5))
	fmt.Printf("   cats with count 1: %s\n", pluralize.GetPluralForm("cats", 1))
	fmt.Println()

	// 9. Batch operations
	fmt.Println("9. Batch Operations:")
	singulars := []string{"cat", "dog", "box", "city", "child"}
	pluralsBatch := pluralize.BatchPluralize(singulars)
	fmt.Printf("   Pluralize batch: %s\n", strings.Join(singulars, ", "))
	fmt.Printf("   Result:         %s\n", strings.Join(pluralsBatch, ", "))

	pluralsInput := []string{"cats", "dogs", "boxes", "cities", "children"}
	singularsBatch := pluralize.BatchSingularize(pluralsInput)
	fmt.Printf("   Singularize batch: %s\n", strings.Join(pluralsInput, ", "))
	fmt.Printf("   Result:           %s\n", strings.Join(singularsBatch, ", "))
	fmt.Println()

	// 10. Article handling
	fmt.Println("10. Article Handling:")
	fmt.Printf("   Article for 'cat': %s\n", pluralize.GetArticle("cat"))
	fmt.Printf("   Article for 'apple': %s\n", pluralize.GetArticle("apple"))
	fmt.Printf("   Article for 'orange': %s\n", pluralize.GetArticle("orange"))
	fmt.Printf("   Article for 'elephant': %s\n", pluralize.GetArticle("elephant"))
	fmt.Println()

	// 11. Format count
	fmt.Println("11. Format Count:")
	fmt.Printf("   %s\n", pluralize.FormatCount("cat", 1))
	fmt.Printf("   %s\n", pluralize.FormatCount("apple", 1))
	fmt.Printf("   %s\n", pluralize.FormatCount("cat", 2))
	fmt.Printf("   %s\n", pluralize.FormatCount("box", 5))
	fmt.Printf("   %s\n", pluralize.FormatCount("child", 10))
	fmt.Println()

	// 12. Hyphenated words
	fmt.Println("12. Hyphenated Words:")
	hyphenated := []string{"brother-in-law", "mother-in-law", "passer-by"}
	for _, word := range hyphenated {
		plural := pluralize.SingularToPlural(word)
		fmt.Printf("   %s -> %s\n", word, plural)
	}
	fmt.Println()

	// 13. Pronouns
	fmt.Println("13. Pronouns:")
	pronouns := []string{"he", "she", "it", "this", "that"}
	for _, word := range pronouns {
		plural := pluralize.SingularToPlural(word)
		fmt.Printf("   %s -> %s\n", word, plural)
	}
	fmt.Println()

	// 14. Words ending with special letters
	fmt.Println("14. Special Endings:")
	fmt.Println("   Words ending with -y (consonant+y -> ies):")
	yWords := []string{"city", "baby", "party", "fly"}
	for _, word := range yWords {
		fmt.Printf("      %s -> %s\n", word, pluralize.SingularToPlural(word))
	}
	fmt.Println("   Words ending with -y (vowel+y -> s):")
	vowelYWords := []string{"day", "boy", "toy", "key"}
	for _, word := range vowelYWords {
		fmt.Printf("      %s -> %s\n", word, pluralize.SingularToPlural(word))
	}
	fmt.Println()

	// 15. Real-world example: building a message
	fmt.Println("15. Real-world Example - Building Messages:")
	count := 3
	item := "box"
	message := fmt.Sprintf("You have %s in your cart.", pluralize.FormatCount(item, count))
	fmt.Printf("   %s\n", message)

	count = 1
	item = "apple"
	message = fmt.Sprintf("You have %s in your cart.", pluralize.FormatCount(item, count))
	fmt.Printf("   %s\n", message)
	fmt.Println()
}