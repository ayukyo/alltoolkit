package main

import (
	"fmt"
	"strings"

	caseutils "github.com/ayukyo/alltoolkit/Go/case_utils"
)

func main() {
	fmt.Println("=== Case Utils Examples ===")
	fmt.Println()

	// Example 1: Basic case conversions
	fmt.Println("1. Basic Case Conversions:")
	examples := []string{
		"hello_world",
		"helloWorld",
		"HelloWorld",
		"hello-world",
		"HELLO_WORLD",
	}

	for _, ex := range examples {
		fmt.Printf("\n  Input: %q\n", ex)
		fmt.Printf("    camelCase:         %q\n", caseutils.ToCamelCase(ex))
		fmt.Printf("    PascalCase:        %q\n", caseutils.ToPascalCase(ex))
		fmt.Printf("    snake_case:        %q\n", caseutils.ToSnakeCase(ex))
		fmt.Printf("    kebab-case:        %q\n", caseutils.ToKebabCase(ex))
		fmt.Printf("    SCREAMING_SNAKE:   %q\n", caseutils.ToScreamingSnakeCase(ex))
		fmt.Printf("    Title Case:        %q\n", caseutils.ToTitleCase(ex))
	}

	fmt.Println()
	fmt.Println(strings.Repeat("-", 50))
	fmt.Println()

	// Example 2: Detect case type
	fmt.Println("2. Case Type Detection:")
	testCases := []string{
		"helloWorld",
		"HelloWorld",
		"hello_world",
		"hello-world",
		"HELLO_WORLD",
		"hello",
		"HELLO",
		"Hello World",
	}

	for _, tc := range testCases {
		detected := caseutils.DetectCase(tc)
		fmt.Printf("  %q -> %s\n", tc, detected.String())
	}

	fmt.Println()
	fmt.Println(strings.Repeat("-", 50))
	fmt.Println()

	// Example 3: Using Convert function
	fmt.Println("3. Using Convert Function:")
	input := "user_account_profile"
	fmt.Printf("  Input: %q\n", input)
	fmt.Printf("  To camelCase:        %q\n", caseutils.Convert(input, caseutils.CaseCamel))
	fmt.Printf("  To PascalCase:       %q\n", caseutils.Convert(input, caseutils.CasePascal))
	fmt.Printf("  To kebab-case:       %q\n", caseutils.Convert(input, caseutils.CaseKebab))
	fmt.Printf("  To SCREAMING_SNAKE:  %q\n", caseutils.Convert(input, caseutils.CaseScreamingSnake))

	fmt.Println()
	fmt.Println(strings.Repeat("-", 50))
	fmt.Println()

	// Example 4: Special case formats
	fmt.Println("4. Special Case Formats:")
	input = "helloWorld"
	fmt.Printf("  Input: %q\n", input)
	fmt.Printf("  dot.case:     %q\n", caseutils.ToDotCase(input))
	fmt.Printf("  path/case:     %q\n", caseutils.ToPathCase(input))
	fmt.Printf("  Train-Case:    %q\n", caseutils.ToTrainCase(input))
	fmt.Printf("  Sentence case: %q\n", caseutils.ToSentenceCase(input))

	fmt.Println()
	fmt.Println(strings.Repeat("-", 50))
	fmt.Println()

	// Example 5: Practical use cases
	fmt.Println("5. Practical Use Cases:")

	// Database column names to struct fields
	fmt.Println("\n  Database columns to Go struct fields:")
	columns := []string{"user_id", "first_name", "last_name", "created_at", "is_active"}
	for _, col := range columns {
		fmt.Printf("    %s -> %s (field), %s (JSON)\n",
			col,
			caseutils.ToPascalCase(col),
			caseutils.ToCamelCase(col))
	}

	// API route conversion
	fmt.Println("\n  API route paths from handler names:")
	handlers := []string{"getUserProfile", "updateUserProfile", "deleteUserAccount"}
	for _, h := range handlers {
		fmt.Printf("    %s -> /api/%s\n", h, caseutils.ToKebabCase(h))
	}

	// Environment variables
	fmt.Println("\n  Config keys to environment variables:")
	configKeys := []string{"databaseUrl", "maxConnections", "sessionTimeout", "enableLogging"}
	for _, key := range configKeys {
		fmt.Printf("    %s -> %s\n", key, caseutils.ToScreamingSnakeCase(key))
	}

	// Display names
	fmt.Println("\n  Machine names to display names:")
	machineNames := []string{"first_name", "last_name", "email_address", "phone_number"}
	for _, name := range machineNames {
		fmt.Printf("    %s -> %s\n", name, caseutils.ToTitleCase(name))
	}

	fmt.Println()
	fmt.Println(strings.Repeat("-", 50))
	fmt.Println()

	// Example 6: Auto-detect and convert
	fmt.Println("6. Auto-detect and Convert:")
	inputs := []string{
		"helloWorld",    // Will detect as camelCase
		"hello_world",   // Will detect as snake_case
		"hello-world",   // Will detect as kebab-case
	}

	fmt.Println("  Converting all to PascalCase:")
	for _, in := range inputs {
		detected := caseutils.DetectCase(in)
		converted := caseutils.AutoConvert(in, caseutils.CasePascal)
		fmt.Printf("    %q (%s) -> %q\n", in, detected.String(), converted)
	}

	fmt.Println()
	fmt.Println("=== All Examples Completed ===")
}