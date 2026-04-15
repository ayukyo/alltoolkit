// Example usage of idgenerator package
// Run with: go run example/main.go
package main

import (
	"fmt"
	"time"

	idgen "github.com/ayukyo/alltoolkit/Go/id_generator"
)

func main() {
	fmt.Println("=====================================")
	fmt.Println("  ID Generator Examples")
	fmt.Println("=====================================")
	fmt.Println()

	// 1. UUID v4
	fmt.Println("1. UUID v4 (RFC 4122 compliant)")
	fmt.Println("-------------------------------------")
	for i := 0; i < 3; i++ {
		uuid, err := idgen.NewUUID()
		if err != nil {
			fmt.Printf("Error: %v\n", err)
			continue
		}
		fmt.Printf("  UUID:          %s\n", uuid.String())
		fmt.Printf("  No dashes:     %s\n", uuid.StringNoDash())
	}
	fmt.Println()

	// 2. Snowflake IDs
	fmt.Println("2. Snowflake IDs (distributed systems)")
	fmt.Println("-------------------------------------")
	config := idgen.DefaultSnowflakeConfig()
	config.NodeID = 42
	snowflake, err := idgen.NewSnowflakeGenerator(config)
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		return
	}

	for i := 0; i < 5; i++ {
		id, timestamp, err := snowflake.GenerateWithTime()
		if err != nil {
			fmt.Printf("Error: %v\n", err)
			continue
		}
		fmt.Printf("  ID: %-19d | Node: %d | Seq: %d | Time: %s\n",
			id,
			snowflake.ExtractNodeID(id),
			snowflake.ExtractSequence(id),
			timestamp.Format("15:04:05.000"))
		time.Sleep(time.Millisecond) // Ensure different timestamps
	}
	fmt.Println()

	// 3. NanoID
	fmt.Println("3. NanoID (URL-friendly, customizable)")
	fmt.Println("-------------------------------------")
	// Default NanoID
	nanoID, _ := idgen.NewNanoID()
	fmt.Printf("  Default (21 chars): %s\n", nanoID)

	// Custom size
	customSize, _ := idgen.NewNanoIDWithSize(10)
	fmt.Printf("  Custom size (10):   %s\n", customSize)

	// Different alphabets
	fmt.Println("\n  Different alphabets:")
	alphabets := []struct {
		name string
		abc  string
	}{
		{"Lowercase", idgen.AlphabetLower},
		{"Uppercase", idgen.AlphabetUpper},
		{"Hex", idgen.AlphabetHex},
		{"No ambiguous", idgen.AlphabetNoDups},
	}

	for _, a := range alphabets {
		gen, _ := idgen.NewNanoIDGenerator(a.abc, 12)
		id, _ := gen.Generate()
		fmt.Printf("    %-14s: %s\n", a.name, id)
	}
	fmt.Println()

	// 4. Custom Format IDs
	fmt.Println("4. Custom Format IDs (order numbers, invoice IDs, etc.)")
	fmt.Println("-------------------------------------")

	// Order ID format: ORD-YYYYMMDD-XXXX-NNNN
	orderConfig := idgen.FormatSpec{
		Prefix:    "ORD-",
		Separator: "-",
		Parts: []idgen.FormatPart{
			{Type: "timestamp", Format: "20060102"},
			{Type: "random", Length: 4},
			{Type: "sequence", Length: 4},
		},
	}
	orderGen, _ := idgen.NewCustomIDGenerator(orderConfig)
	fmt.Println("  Order IDs:")
	for i := 0; i < 3; i++ {
		id, _ := orderGen.Generate()
		fmt.Printf("    %s\n", id)
	}

	// Invoice ID format: INV-YYMM-XXXX
	invoiceConfig := idgen.FormatSpec{
		Prefix:    "INV-",
		Suffix:    "-CN",
		Separator: "-",
		Parts: []idgen.FormatPart{
			{Type: "timestamp", Format: "0601"},
			{Type: "sequence", Length: 4},
		},
	}
	invoiceGen, _ := idgen.NewCustomIDGenerator(invoiceConfig)
	fmt.Println("\n  Invoice IDs:")
	for i := 0; i < 3; i++ {
		id, _ := invoiceGen.Generate()
		fmt.Printf("    %s\n", id)
	}
	fmt.Println()

	// 5. Short IDs
	fmt.Println("5. Short IDs (for URLs, short links)")
	fmt.Println("-------------------------------------")
	shortGen := idgen.NewShortIDGenerator(8)
	fmt.Println("  8-character short IDs:")
	for i := 0; i < 5; i++ {
		id, _ := shortGen.Generate()
		fmt.Printf("    %s\n", id)
	}
	fmt.Println()

	// 6. Hash-based IDs (deterministic)
	fmt.Println("6. Hash-based IDs (deterministic, same content = same ID)")
	fmt.Println("-------------------------------------")
	hashGen := idgen.NewHashIDGenerator("H-", 8)
	contents := []string{
		"user@example.com",
		"product-12345",
		"session-abc-xyz",
		"user@example.com", // Same as first, should produce same ID
	}

	fmt.Println("  Content to ID mapping:")
	for _, c := range contents {
		id := hashGen.Generate(c)
		fmt.Printf("    %-20s -> %s\n", c, id)
	}
	fmt.Println()

	// 7. Sequential IDs
	fmt.Println("7. Sequential IDs (simple counters)")
	fmt.Println("-------------------------------------")
	seqGen := idgen.NewSequentialGenerator("TICKET-", 6, 1000)
	fmt.Println("  Support tickets:")
	for i := 0; i < 5; i++ {
		fmt.Printf("    %s\n", seqGen.Next())
	}
	fmt.Printf("  Current counter: %d\n", seqGen.Current())

	seqGen.Reset()
	fmt.Println("  After reset:")
	fmt.Printf("    %s\n", seqGen.Next())
	fmt.Println()

	// 8. Performance comparison
	fmt.Println("8. Usage recommendations")
	fmt.Println("-------------------------------------")
	fmt.Println("  UUID v4:      - Unique across systems, RFC standard")
	fmt.Println("  Snowflake:    - Time-ordered, extractable components")
	fmt.Println("  NanoID:       - URL-friendly, customizable length")
	fmt.Println("  Short ID:     - Minimal length, good for URLs")
	fmt.Println("  Custom Format: - Human-readable, domain-specific patterns")
	fmt.Println("  Hash-based:   - Deterministic, content-addressable")
	fmt.Println("  Sequential:   - Simple, ordered, easy to read")
	fmt.Println()

	fmt.Println("=====================================")
	fmt.Println("  All examples completed!")
	fmt.Println("=====================================")
}