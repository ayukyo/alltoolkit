// Example usage of stringutils package
// Run: go run main.go
package main

import (
	"fmt"
	stringutils "github.com/yourusername/alltoolkit/go"
)

func main() {
	fmt.Println("=== AllToolkit - Go String Utils Demo ===\n")

	// Example 1: Basic ASCII truncation
	fmt.Println("1. Basic ASCII truncation:")
	result1 := stringutils.Truncate("Hello World, this is a long message", 20)
	fmt.Printf("   Input:  \"Hello World, this is a long message\"\n")
	fmt.Printf("   Output: \"%s\" (len=%d)\n\n", result1, len(result1))

	// Example 2: No truncation needed
	fmt.Println("2. Short string (no truncation):")
	result2 := stringutils.Truncate("Hello", 20)
	fmt.Printf("   Input:  \"Hello\"\n")
	fmt.Printf("   Output: \"%s\"\n\n", result2)

	// Example 3: Unicode (Chinese) truncation
	fmt.Println("3. Unicode (Chinese) truncation:")
	result3 := stringutils.Truncate("你好世界，这是一个很长的消息", 10)
	fmt.Printf("   Input:  \"你好世界，这是一个很长的消息\"\n")
	fmt.Printf("   Output: \"%s\"\n\n", result3)

	// Example 4: Emoji handling
	fmt.Println("4. Emoji handling:")
	result4 := stringutils.Truncate("Hello 👋 World 🌍! How are you?", 15)
	fmt.Printf("   Input:  \"Hello 👋 World 🌍! How are you?\"\n")
	fmt.Printf("   Output: \"%s\"\n\n", result4)

	// Example 5: TruncateSafe (byte-based)
	fmt.Println("5. TruncateSafe (byte-based, strict limit):")
	result5 := stringutils.TruncateSafe("Hello World, this is a long message", 20)
	fmt.Printf("   Input:  \"Hello World, this is a long message\"\n")
	fmt.Printf("   Output: \"%s\" (len=%d, guaranteed <= 20 bytes)\n\n", result5, len(result5))

	// Example 6: Edge cases
	fmt.Println("6. Edge cases:")
	fmt.Printf("   Empty string: \"%s\"\n", stringutils.Truncate("", 10))
	fmt.Printf("   MaxLen < 3:   \"%s\"\n", stringutils.Truncate("Hello", 2))
	fmt.Printf("   Exact fit:    \"%s\"\n", stringutils.Truncate("Hello", 5))

	fmt.Println("\n=== Demo Complete ===")
}
