// Package main provides examples for uuid_utils usage
package main

import (
	"encoding/json"
	"fmt"
	"log"
	"time"

	uuid "github.com/ayukyo/alltoolkit/go/uuid_utils"
)

func main() {
	fmt.Println("=== UUID Utils Examples ===\n")

	// 1. Basic V4 UUID Generation
	exampleBasicV4()

	// 2. V3 and V5 UUID Generation
	exampleV3V5()

	// 3. Parsing UUIDs
	exampleParsing()

	// 4. UUID Properties
	exampleProperties()

	// 5. String Formatting
	exampleFormatting()

	// 6. JSON Serialization
	exampleJSON()

	// 7. Batch Generation
	exampleBatch()

	// 8. UUID Generator with Prefix
	exampleGenerator()

	// 9. Collection Operations
	exampleCollections()

	// 10. Analysis
	exampleAnalysis()
}

// 1. Basic V4 UUID Generation
func exampleBasicV4() {
	fmt.Println("1. Basic V4 UUID Generation")
	fmt.Println("---------------------------")

	// Generate a random UUID (version 4)
	uuid1, err := uuid.NewV4()
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("Generated UUID: %s\n", uuid1.String())

	// Quick generation (panics on error)
	uuid2 := uuid.MustNewV4()
	fmt.Printf("Another UUID:   %s\n", uuid2.String())

	// Nil UUID
	fmt.Printf("Nil UUID:        %s\n", uuid.NilUUID.String())

	// Check if nil
	fmt.Printf("Is nil? %v\n", uuid.NilUUID.IsNil())

	fmt.Println()
}

// 2. V3 and V5 UUID Generation
func exampleV3V5() {
	fmt.Println("2. V3 and V5 UUID Generation")
	fmt.Println("-----------------------------")

	// Well-known namespaces
	dnsNamespace := uuid.MustParse("6ba7b810-9dad-11d1-80b4-00c04fd430c8")
	urlNamespace := uuid.MustParse("6ba7b811-9dad-11d1-80b4-00c04fd430c8")
	oidNamespace := uuid.MustParse("6ba7b812-9dad-11d1-80b4-00c04fd430c8")
	x500Namespace := uuid.MustParse("6ba7b814-9dad-11d1-80b4-00c04fd430c8")

	name := "example.com"

	// V3 (MD5 based) - deterministic
	v3UUID := uuid.NewV3(dnsNamespace, name)
	fmt.Printf("V3 (MD5): %s\n", v3UUID.String())

	// V5 (SHA-1 based) - deterministic
	v5UUID := uuid.NewV5(dnsNamespace, name)
	fmt.Printf("V5 (SHA-1): %s\n", v5UUID.String())

	// Same input = same UUID
	v5Again := uuid.NewV5(dnsNamespace, name)
	fmt.Printf("Same again: %s\n", v5Again.String())
	fmt.Printf("Equal: %v\n", v5UUID.Equals(v5Again))

	// Different name = different UUID
	v5Different := uuid.NewV5(dnsNamespace, "different.com")
	fmt.Printf("Different: %s\n", v5Different.String())
	fmt.Printf("Equal: %v\n", v5UUID.Equals(v5Different))

	// Custom namespace for your application
	myAppNamespace := uuid.MustNewV4()
	userUUID := uuid.NewV5(myAppNamespace, "user@example.com")
	fmt.Printf("User UUID: %s\n", userUUID.String())

	// Other namespaces
	fmt.Printf("URL namespace: %s\n", urlNamespace.String())
	fmt.Printf("OID namespace: %s\n", oidNamespace.String())
	fmt.Printf("X500 namespace: %s\n", x500Namespace.String())

	fmt.Println()
}

// 3. Parsing UUIDs
func exampleParsing() {
	fmt.Println("3. Parsing UUIDs")
	fmt.Println("-----------------")

	// Standard format
	u1, _ := uuid.Parse("6ba7b810-9dad-11d1-80b4-00c04fd430c8")
	fmt.Printf("Standard: %s\n", u1.String())

	// Without dashes (also supported)
	u2, _ := uuid.Parse("6ba7b8109dad11d180b400c04fd430c8")
	fmt.Printf("No dashes: %s\n", u2.String())

	// With braces
	u3, _ := uuid.Parse("{6ba7b810-9dad-11d1-80b4-00c04fd430c8}")
	fmt.Printf("Braces: %s\n", u3.String())

	// URN format
	u4, _ := uuid.Parse("urn:uuid:6ba7b810-9dad-11d1-80b4-00c04fd430c8")
	fmt.Printf("URN: %s\n", u4.String())

	// ParseAny handles all formats
	u5, _ := uuid.ParseAny("6BA7B810-9DAD-11D1-80B4-00C04FD430C8")
	fmt.Printf("ParseAny (uppercase): %s\n", u5.String())

	// MustParse panics on error
	u6 := uuid.MustParse("6ba7b810-9dad-11d1-80b4-00c04fd430c8")
	fmt.Printf("MustParse: %s\n", u6.String())

	// ParseOrNil returns nil UUID on error
	u7 := uuid.ParseOrNil("invalid")
	fmt.Printf("ParseOrNil(invalid): %s (isNil: %v)\n", u7.String(), u7.IsNil())

	// Validate string
	fmt.Printf("Valid? %v\n", uuid.IsValidString("6ba7b810-9dad-11d1-80b4-00c04fd430c8"))
	fmt.Printf("Valid? %v\n", uuid.IsValidString("invalid"))

	fmt.Println()
}

// 4. UUID Properties
func exampleProperties() {
	fmt.Println("4. UUID Properties")
	fmt.Println("------------------")

	uuid1 := uuid.MustParse("d9428888-122b-11e1-b85c-61cd3cbb3210") // v1
	uuid2 := uuid.MustParse("d9428888-122b-41e1-b85c-61cd3cbb3210") // v4
	uuid3 := uuid.NewV5(uuid.MustParse("6ba7b810-9dad-11d1-80b4-00c04fd430c8"), "test")

	// Version
	fmt.Printf("UUID1 version: %d (v1=time-based)\n", uuid1.Version())
	fmt.Printf("UUID2 version: %d (v4=random)\n", uuid2.Version())
	fmt.Printf("UUID3 version: %d (v5=SHA-1)\n", uuid3.Version())

	// Variant
	fmt.Printf("UUID1 variant: %d (RFC 4122)\n", uuid1.Variant())

	// Nil check
	fmt.Printf("Is nil? %v\n", uuid1.IsNil())
	fmt.Printf("Is valid? %v\n", uuid1.IsValid())

	// Compare
	fmt.Printf("Compare(uuid1, uuid2): %d\n", uuid1.Compare(uuid2))

	// Equals
	uuidCopy := uuid1
	fmt.Printf("Equals copy: %v\n", uuid1.Equals(uuidCopy))

	fmt.Println()
}

// 5. String Formatting
func exampleFormatting() {
	fmt.Println("5. String Formatting")
	fmt.Println("--------------------")

	u := uuid.MustParse("6ba7b810-9dad-11d1-80b4-00c04fd430c8")

	// Standard format
	fmt.Printf("Standard: %s\n", u.String())

	// No dashes
	fmt.Printf("No dashes: %s\n", u.StringNoDash())

	// URN format
	fmt.Printf("URN: %s\n", u.URN())

	// Short (first 8 chars)
	fmt.Printf("Short: %s\n", u.Short())

	// Upper/lower case
	fmt.Printf("Upper: %s\n", u.ToUpper())
	fmt.Printf("Lower: %s\n", u.ToLower())

	// Using Format with various options
	fmt.Printf("Format default: %s\n", u.Format("default"))
	fmt.Printf("Format nodash: %s\n", u.Format("nodash"))
	fmt.Printf("Format urn: %s\n", u.Format("urn"))
	fmt.Printf("Format braces: %s\n", u.Format("braces"))
	fmt.Printf("Format short: %s\n", u.Format("short"))
	fmt.Printf("Format upper: %s\n", u.Format("upper"))

	// Bytes representation
	fmt.Printf("Bytes: %v\n", u.Bytes())

	fmt.Println()
}

// 6. JSON Serialization
func exampleJSON() {
	fmt.Println("6. JSON Serialization")
	fmt.Println("---------------------")

	type User struct {
		ID   uuid.UUID `json:"id"`
		Name string    `json:"name"`
	}

	// Create user with UUID
	user := User{
		ID:   uuid.MustNewV4(),
		Name: "John Doe",
	}

	// Marshal to JSON
	data, err := json.MarshalIndent(user, "", "  ")
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("JSON:\n%s\n", string(data))

	// Unmarshal from JSON
	var parsed User
	err = json.Unmarshal(data, &parsed)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("Parsed ID: %s\n", parsed.ID.String())
	fmt.Printf("IDs match: %v\n", user.ID.Equals(parsed.ID))

	fmt.Println()
}

// 7. Batch Generation
func exampleBatch() {
	fmt.Println("7. Batch Generation")
	fmt.Println("-------------------")

	// Generate multiple UUIDs at once
	uuids, err := uuid.GenerateV4Batch(5)
	if err != nil {
		log.Fatal(err)
	}

	fmt.Printf("Generated %d UUIDs:\n", len(uuids))
	for i, u := range uuids {
		fmt.Printf("  %d: %s\n", i+1, u.String())
	}

	fmt.Println()
}

// 8. UUID Generator with Prefix
func exampleGenerator() {
	fmt.Println("8. UUID Generator with Prefix")
	fmt.Println("-----------------------------")

	// Create generator with prefix
	userGen := uuid.NewGenerator("user_")
	orderGen := uuid.NewGenerator("order_")

	// Generate IDs
	userID, _ := userGen.Generate()
	orderID, _ := orderGen.Generate()

	fmt.Printf("User ID: %s\n", userID)
	fmt.Printf("Order ID: %s\n", orderID)

	// Extract UUID from prefixed string
	extracted, _ := userGen.ExtractUUID(userID)
	fmt.Printf("Extracted: %s\n", extracted.String())

	// MustGenerate (panics on error)
	quickID := userGen.MustGenerate()
	fmt.Printf("Quick ID: %s\n", quickID)

	fmt.Println()
}

// 9. Collection Operations
func exampleCollections() {
	fmt.Println("9. Collection Operations")
	fmt.Println("------------------------")

	uuid1 := uuid.MustParse("00000000-0000-0000-0000-000000000001")
	uuid2 := uuid.MustParse("00000000-0000-0000-0000-000000000002")
	uuid3 := uuid.MustParse("00000000-0000-0000-0000-000000000003")

	// Create collection
	uuids := []uuid.UUID{uuid3, uuid1, uuid2, uuid1}

	fmt.Printf("Original: %v\n", uuid.Strings(uuids))

	// Sort
	uuid.Sort(uuids)
	fmt.Printf("Sorted: %v\n", uuid.Strings(uuids))

	// Deduplicate
	deduped := uuid.Deduplicate(uuids)
	fmt.Printf("Deduplicated: %v\n", uuid.Strings(deduped))

	// Contains
	fmt.Printf("Contains uuid1? %v\n", uuid.Contains(uuids, uuid1))

	// IndexOf
	fmt.Printf("IndexOf uuid1: %d\n", uuid.IndexOf(uuids, uuid1))

	// Remove
	removed := uuid.Remove(uuids, uuid2)
	fmt.Printf("Removed uuid2: %v\n", uuid.Strings(removed))

	// Filter
	v4s := []uuid.UUID{}
	for i := 0; i < 3; i++ {
		u, _ := uuid.NewV4()
		v4s = append(v4s, u)
	}
	v4s = append(v4s, uuid.NilUUID)
	filtered := uuid.Filter(v4s, func(u uuid.UUID) bool {
		return !u.IsNil()
	})
	fmt.Printf("Filtered (non-nil): %d items\n", len(filtered))

	// Map
	upper := uuid.Map(v4s[:2], func(u uuid.UUID) string { return u.ToUpper() })
	fmt.Printf("Mapped to upper: %v\n", upper)

	// Strings
	strs := uuid.Strings(uuids[:3])
	fmt.Printf("Strings: %v\n", strs)

	// ParseStrings
	parsed, _ := uuid.ParseStrings(strs)
	fmt.Printf("Parsed back: %v\n", uuid.Strings(parsed))

	// Equal
	a := []uuid.UUID{uuid1, uuid2}
	b := []uuid.UUID{uuid1, uuid2}
	fmt.Printf("Equal? %v\n", uuid.Equal(a, b))

	// Clone
	clone := uuid.Clone(uuids)
	fmt.Printf("Cloned: %v\n", uuid.Strings(clone))

	fmt.Println()
}

// 10. Analysis
func exampleAnalysis() {
	fmt.Println("10. Analysis")
	fmt.Println("------------")

	// Create collection with various UUIDs
	uuids := make([]uuid.UUID, 0)

	// Add some v4 UUIDs
	for i := 0; i < 5; i++ {
		u, _ := uuid.NewV4()
		uuids = append(uuids, u)
	}

	// Add some v5 UUIDs
	namespace := uuid.MustParse("6ba7b810-9dad-11d1-80b4-00c04fd430c8")
	for _, name := range []string{"a", "b", "c"} {
		uuids = append(uuids, uuid.NewV5(namespace, name))
	}

	// Add nil UUID
	uuids = append(uuids, uuid.NilUUID)

	// Analyze
	stats := uuid.Analyze(uuids)

	fmt.Printf("Total UUIDs: %d\n", stats.Total)
	fmt.Printf("Version distribution:\n")
	for v, count := range stats.VersionMap {
		fmt.Printf("  v%d: %d\n", v, count)
	}
	fmt.Printf("Variant distribution:\n")
	for v, count := range stats.VariantMap {
		fmt.Printf("  %d: %d\n", v, count)
	}
	fmt.Printf("Nil UUIDs: %d\n", stats.NilCount)

	fmt.Println("\n=== Examples Complete ===")
}

// Additional: Time extraction for V1 UUIDs (for reference)
func exampleV1Time() {
	fmt.Println("\nBonus: V1 UUID Time Extraction")
	fmt.Println("-----------------------------")

	// Note: This example uses a synthetic V1 UUID
	// Real V1 UUIDs encode the creation timestamp
	v1UUID := uuid.MustParse("c232ab00-9214-11eb-a8b3-0242ac130003")

	if v1UUID.Version() == uuid.VersionV1 {
		t, err := v1UUID.Time()
		if err == nil {
			fmt.Printf("V1 UUID created at: %s\n", t.Format(time.RFC3339))
		}
		fmt.Printf("Node ID: %x\n", v1UUID.NodeID())
		fmt.Printf("Clock sequence: %d\n", v1UUID.ClockSeq())
	}
}