package main

import (
	"fmt"
	"log"
	"github.com/ayukyo/alltoolkit/Go/xml_utils"
)

func main() {
	fmt.Println("=== XML Utils Example ===\n")

	// Example 1: Parse XML from string
	fmt.Println("1. Parse XML from string:")
	xmlData := `<?xml version="1.0" encoding="UTF-8"?>
<configuration>
	<database>
		<host>localhost</host>
		<port>5432</port>
		<name>myapp</name>
	</database>
	<cache enabled="true" ttl="3600">
		<provider>redis</provider>
	</cache>
</configuration>`

	doc, err := xml_utils.ParseString(xmlData)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println("Parsed successfully!")

	// Example 2: Navigate XML tree
	fmt.Println("\n2. Navigate XML tree:")
	host := doc.Find("configuration/database/host")
	if host != nil {
		fmt.Printf("Database host: %s\n", host.Text())
	}

	port := doc.Find("configuration/database/port")
	if port != nil {
		fmt.Printf("Database port: %s\n", port.Text())
	}

	// Example 3: Find all elements
	fmt.Println("\n3. Find all elements:")
	allNodes := doc.FindAll("*")
	fmt.Printf("Total nodes: %d\n", len(allNodes))

	// Example 4: Get attributes
	fmt.Println("\n4. Get attributes:")
	cache := doc.Find("configuration/cache")
	if cache != nil {
		enabled := cache.GetAttr("enabled")
		ttl := cache.GetAttr("ttl")
		fmt.Printf("Cache enabled: %s, TTL: %s seconds\n", enabled, ttl)
	}

	// Example 5: Create new XML document
	fmt.Println("\n5. Create new XML document:")
	newDoc := xml_utils.NewDocument("library")
	newDoc.SetVersion("1.0")
	newDoc.SetEncoding("UTF-8")

	// Add books
	book1 := newDoc.Root().CreateElement("book")
	book1.SetAttr("id", "1")
	book1.SetAttr("isbn", "978-3-16-148410-0")
	title1 := book1.CreateElement("title")
	title1.SetText("The Go Programming Language")
	author1 := book1.CreateElement("author")
	author1.SetText("Alan Donovan")

	book2 := newDoc.Root().CreateElement("book")
	book2.SetAttr("id", "2")
	book2.SetAttr("isbn", "978-0-13-419044-0")
	title2 := book2.CreateElement("title")
	title2.SetText("Clean Code")
	author2 := book2.CreateElement("author")
	author2.SetText("Robert C. Martin")

	// Output as pretty XML
	fmt.Println("Generated XML:")
	fmt.Println(newDoc.ToPrettyXML())

	// Example 6: Find by attribute
	fmt.Println("6. Find by attribute:")
	book := newDoc.FindByAttr("book", "id", "2")
	if book != nil {
		title := book.GetChildren()[0]
		fmt.Printf("Found book with id=2: %s\n", title.Text())
	}

	// Example 7: Modify XML
	fmt.Println("\n7. Modify XML:")
	book1.SetAttr("available", "true")
	fmt.Printf("Added attribute 'available=true' to book 1\n")

	// Example 8: Strip XML tags
	fmt.Println("\n8. Strip XML tags:")
	plainText := xml_utils.StripXML(xmlData)
	fmt.Printf("Plain text: %s\n", plainText)

	// Example 9: Validate XML
	fmt.Println("\n9. Validate XML:")
	validXML := `<root><item>value</item></root>`
	invalidXML := `<root><item>value</root>`
	
	fmt.Printf("Is '%s' valid? %v\n", validXML, xml_utils.IsValidXML(validXML))
	fmt.Printf("Is '%s' valid? %v\n", invalidXML, xml_utils.IsValidXML(invalidXML))

	// Example 10: Working with typed attributes
	fmt.Println("\n10. Typed attributes:")
	testDoc := xml_utils.NewDocument("settings")
	testDoc.Root().SetAttr("maxConnections", "100")
	testDoc.Root().SetAttr("timeout", "30.5")
	testDoc.Root().SetAttr("debug", "true")

	maxConn := testDoc.Root().GetIntAttr("maxConnections", 0)
	timeout := testDoc.Root().GetFloatAttr("timeout", 0.0)
	debug := testDoc.Root().GetBoolAttr("debug", false)

	fmt.Printf("Max connections: %d\n", maxConn)
	fmt.Printf("Timeout: %.1f seconds\n", timeout)
	fmt.Printf("Debug mode: %v\n", debug)

	fmt.Println("\n=== All examples completed! ===")
}
