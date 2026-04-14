// Example usage of slug_utils package
package main

import (
	"fmt"
	"strings"

	slugutils "github.com/ayukyo/alltoolkit/Go/slug_utils"
)

func main() {
	fmt.Println("=== Slug Utils Examples ===")
	fmt.Println()

	// Basic usage
	basicExamples()

	// Configuration examples
	configExamples()

	// Unique slug examples
	uniqueSlugExamples()

	// Real-world examples
	realWorldExamples()

	// Validation examples
	validationExamples()

	// Utility function examples
	utilityExamples()
}

func basicExamples() {
	fmt.Println("--- Basic Usage ---")

	// Simple slug generation
	slug1 := slugutils.Generate("Hello World")
	fmt.Printf("Generate(\"Hello World\") = \"%s\"\n", slug1)

	// With numbers
	slug2 := slugutils.Generate("Product ID 12345")
	fmt.Printf("Generate(\"Product ID 12345\") = \"%s\"\n", slug2)

	// With special characters
	slug3 := slugutils.Generate("What's New in 2024?!")
	fmt.Printf("Generate(\"What's New in 2024?!\") = \"%s\"\n", slug3)

	// Multiple words
	slug4 := slugutils.GenerateMultiple("How", "To", "Write", "Clean", "Code")
	fmt.Printf("GenerateMultiple(\"How\", \"To\", \"Write\", \"Clean\", \"Code\") = \"%s\"\n", slug4)

	fmt.Println()
}

func configExamples() {
	fmt.Println("--- Custom Configuration ---")

	// Custom separator (underscore)
	slugger := slugutils.NewWithConfig(slugutils.Config{
		Separator: "_",
		Lowercase: true,
	})
	slug := slugger.Generate("Hello World")
	fmt.Printf("Underscore separator: \"%s\"\n", slug)

	// Preserve case
	slugger2 := slugutils.NewWithConfig(slugutils.Config{
		Separator: "-",
		Lowercase: false,
	})
	slug2 := slugger2.Generate("Hello World")
	fmt.Printf("Preserve case: \"%s\"\n", slug2)

	// Max length
	slugger3 := slugutils.NewWithConfig(slugutils.Config{
		Separator: "-",
		MaxLength: 20,
		Lowercase: true,
	})
	slug3 := slugger3.Generate("This is a very long blog post title that needs truncation")
	fmt.Printf("Max length 20: \"%s\" (len=%d)\n", slug3, len(slug3))

	// Dot separator
	slugger4 := slugutils.NewWithConfig(slugutils.Config{
		Separator: ".",
		Lowercase: true,
	})
	slug4 := slugger4.Generate("Section Subsection Item")
	fmt.Printf("Dot separator: \"%s\"\n", slug4)

	fmt.Println()
}

func uniqueSlugExamples() {
	fmt.Println("--- Unique Slug Generation ---")

	// Simulating a database of existing slugs
	existingSlugs := make(map[string]bool)
	existingSlugs["hello-world"] = true
	existingSlugs["hello-world-1"] = true

	slugger := slugutils.New()

	// This will return "my-new-post" (not in existing)
	slug1 := slugger.GenerateUnique("My New Post", existingSlugs)
	fmt.Printf("First unique: \"%s\"\n", slug1)

	// This will return "hello-world-2" (1 already exists)
	slug2 := slugger.GenerateUnique("Hello World", existingSlugs)
	fmt.Printf("Conflict resolved: \"%s\"\n", slug2)

	// Using with a function that checks database
	checkExists := func(slug string) bool {
		// In real code, this would query a database
		return slug == "test-post" || slug == "test-post-1"
	}

	slug3 := slugger.GenerateUnique("Test Post", checkExists)
	fmt.Printf("With function checker: \"%s\"\n", slug3)

	fmt.Println()
}

func realWorldExamples() {
	fmt.Println("--- Real-World Use Cases ---")

	slugger := slugutils.New()

	// Blog post URLs
	titles := []string{
		"10 Tips for Better Sleep 😴",
		"How to Build a REST API with Go",
		"Understanding Machine Learning in 2024!",
		"C++ Best Practices: Memory Management",
		"What's New in JavaScript ES2024?",
	}

	fmt.Println("Blog post slugs:")
	for _, title := range titles {
		slug := slugger.Generate(title)
		fmt.Printf("  %s -> %s\n", truncate(title, 40), slug)
	}

	// Product URLs
	products := []string{
		"Apple iPhone 15 Pro Max (256GB)",
		"Samsung Galaxy S24 Ultra",
		"Sony WH-1000XM5 Wireless Headphones",
	}

	fmt.Println("\nProduct slugs:")
	for _, product := range products {
		slug := slugger.Generate(product)
		fmt.Printf("  %s -> %s\n", truncate(product, 40), slug)
	}

	// Category slugs
	categories := []string{
		"Electronics & Gadgets",
		"Men's Clothing",
		"Women's Fashion",
		"Home & Kitchen",
	}

	fmt.Println("\nCategory slugs:")
	for _, cat := range categories {
		slug := slugger.Generate(cat)
		fmt.Printf("  %s -> %s\n", cat, slug)
	}

	// User profile slugs
	users := []string{
		"John Doe",
		"Maria García-López",
		"张伟 (Zhang Wei)",
		"François Müller",
	}

	fmt.Println("\nUser profile slugs:")
	for _, user := range users {
		slug := slugger.Generate(user)
		fmt.Printf("  %s -> %s\n", user, slug)
	}

	fmt.Println()
}

func validationExamples() {
	fmt.Println("--- Slug Validation ---")

	testSlugs := []string{
		"hello-world",
		"hello_world",
		"hello123",
		"hello world",  // invalid - space
		"hello@world",  // invalid - @
		"hello/world",  // invalid - /
		"",             // invalid - empty
	}

	for _, slug := range testSlugs {
		valid := slugutils.IsValidSlug(slug)
		status := "✓ valid"
		if !valid {
			status = "✗ invalid"
		}
		fmt.Printf("  \"%s\" -> %s\n", slug, status)
	}

	fmt.Println()
}

func utilityExamples() {
	fmt.Println("--- Utility Functions ---")

	// Parse slug back to words
	slug := "hello-beautiful-world"
	words := slugutils.ParseSlug(slug, "-")
	fmt.Printf("ParseSlug(\"%s\") = %v\n", slug, words)

	// Truncate slug
	longSlug := "this-is-a-very-long-slug-that-needs-to-be-truncated"
	shortSlug := slugutils.Truncate(longSlug, 20, "-")
	fmt.Printf("Truncate(\"%s\", 20) = \"%s\"\n", truncate(longSlug, 30), shortSlug)

	// Different separator for parsing
	slugWithUnderscore := "product_id_12345"
	words2 := slugutils.ParseSlug(slugWithUnderscore, "_")
	fmt.Printf("ParseSlug(\"%s\", \"_\") = %v\n", slugWithUnderscore, words2)

	fmt.Println()
}

// Helper function to truncate strings for display
func truncate(s string, maxLen int) string {
	if len(s) <= maxLen {
		return s
	}
	return s[:maxLen-3] + "..."
}

func init() {
	// This ensures strings package is available
	_ = strings.Builder{}
}