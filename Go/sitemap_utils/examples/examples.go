// Package main demonstrates sitemap_utils usage
package main

import (
	"fmt"
	"os"
	"time"

	sitemap "github.com/alltoolkit/sitemap_utils"
)

func main() {
	fmt.Println("=== Sitemap Utils Examples ===\n")

	// Example 1: Basic sitemap creation
	basicExample()

	// Example 2: Sitemap with full URL details
	fullDetailsExample()

	// Example 3: Multi-language sitemap
	multiLanguageExample()

	// Example 4: Sitemap index
	sitemapIndexExample()

	// Example 5: Large site with batch generation
	batchGenerationExample()

	// Example 6: URL builder
	urlBuilderExample()

	// Example 7: Parse existing sitemap
	parseExample()

	// Example 8: Compressed sitemap
	compressedExample()
}

func basicExample() {
	fmt.Println("--- Example 1: Basic Sitemap ---")

	// Create a new sitemap generator
	gen := sitemap.NewGenerator()

	// Add simple URLs
	gen.AddSimpleURL("https://example.com/")
	gen.AddSimpleURL("https://example.com/about")
	gen.AddSimpleURL("https://example.com/products")
	gen.AddSimpleURL("https://example.com/contact")

	// Generate XML
	xmlData, err := gen.ToXML()
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		return
	}

	fmt.Println(string(xmlData))
}

func fullDetailsExample() {
	fmt.Println("\n--- Example 2: Sitemap with Full Details ---")

	gen := sitemap.NewGenerator(sitemap.WithPrettyPrint(true))

	// Add homepage with high priority
	now := time.Now()
	gen.AddURL(sitemap.URL{
		Loc:        "https://example.com/",
		LastMod:    &now,
		ChangeFreq: &sitemap.Daily,
		Priority:   floatPtr(1.0),
	})

	// Add blog section
	gen.AddURL(sitemap.URL{
		Loc:        "https://example.com/blog",
		LastMod:    &now,
		ChangeFreq: &sitemap.Weekly,
		Priority:   floatPtr(0.8),
	})

	// Add static pages with lower update frequency
	gen.AddURL(sitemap.URL{
		Loc:        "https://example.com/about",
		LastMod:    &now,
		ChangeFreq: &sitemap.Monthly,
		Priority:   floatPtr(0.5),
	})

	xmlData, _ := gen.ToXML()
	fmt.Println(string(xmlData))
}

func multiLanguageExample() {
	fmt.Println("\n--- Example 3: Multi-language Sitemap ---")

	gen := sitemap.NewGenerator()

	// Add English page with alternates
	gen.AddAlternateURL(
		"https://example.com/en/products",
		[]sitemap.Alternate{
			{Hreflang: "en", Href: "https://example.com/en/products"},
			{Hreflang: "es", Href: "https://example.com/es/products"},
			{Hreflang: "fr", Href: "https://example.com/fr/products"},
		},
		nil,
	)

	// Add Spanish page with alternates
	gen.AddAlternateURL(
		"https://example.com/es/products",
		[]sitemap.Alternate{
			{Hreflang: "en", Href: "https://example.com/en/products"},
			{Hreflang: "es", Href: "https://example.com/es/products"},
			{Hreflang: "fr", Href: "https://example.com/fr/products"},
		},
		nil,
	)

	xmlData, _ := gen.ToXML()
	fmt.Println(string(xmlData))
}

func sitemapIndexExample() {
	fmt.Println("\n--- Example 4: Sitemap Index ---")

	// Create sitemap index
	indexGen := sitemap.NewIndexGenerator()

	now := time.Now()

	// Add multiple sitemaps to the index
	indexGen.AddSitemap("https://example.com/sitemap-products.xml", &now)
	indexGen.AddSitemap("https://example.com/sitemap-blog.xml", &now)
	indexGen.AddSitemap("https://example.com/sitemap-news.xml", nil)

	xmlData, _ := indexGen.ToXML()
	fmt.Println(string(xmlData))
}

func batchGenerationExample() {
	fmt.Println("\n--- Example 5: Batch Generation for Large Sites ---")

	// Create batch generator with 3 URLs per sitemap (for demo)
	batch := sitemap.NewBatchGenerator(3)

	// Simulate adding many URLs
	for i := 1; i <= 10; i++ {
		batch.AddURL(sitemap.URL{
			Loc: fmt.Sprintf("https://example.com/page/%d", i),
		})
	}

	fmt.Printf("Total URLs: %d\n", batch.TotalCount())
	fmt.Printf("Number of sitemaps: %d\n", batch.SitemapCount())

	// Create index
	indexXML, _ := batch.CreateIndex("https://example.com/sitemap")
	fmt.Println("\nSitemap Index:")
	fmt.Println(string(indexXML))
}

func urlBuilderExample() {
	fmt.Println("\n--- Example 6: URL Builder ---")

	// Create URL builder
	builder := sitemap.NewURLBuilder("https://example.com")

	// Build various URLs
	url1 := builder.Path("products").Path("123").Build()
	fmt.Printf("Product URL: %s\n", url1)

	builder.Reset()
	url2 := builder.Path("search").Param("q", "golang").Param("page", "1").Build()
	fmt.Printf("Search URL: %s\n", url2)

	builder.Reset()
	url3 := builder.Path("api").Path("v1").Path("users").Param("limit", "10").Build()
	fmt.Printf("API URL: %s\n", url3)
}

func parseExample() {
	fmt.Println("\n--- Example 7: Parse Existing Sitemap ---")

	// First create a sitemap
	gen := sitemap.NewGenerator()
	gen.AddURL(sitemap.URL{Loc: "https://example.com/page1"})
	gen.AddURL(sitemap.URL{Loc: "https://example.com/page2"})
	gen.AddURL(sitemap.URL{Loc: "https://example.com/page3"})

	xmlData, _ := gen.ToXML()

	// Parse it back
	parser := sitemap.NewParser()
	sitemap, err := parser.Parse(xmlData)
	if err != nil {
		fmt.Printf("Parse error: %v\n", err)
		return
	}

	fmt.Printf("Parsed %d URLs:\n", len(sitemap.URLs))
	for i, url := range sitemap.URLs {
		fmt.Printf("  %d. %s\n", i+1, url.Loc)
	}
}

func compressedExample() {
	fmt.Println("\n--- Example 8: Compressed Sitemap ---")

	// Create generator with compression enabled
	gen := sitemap.NewGenerator(sitemap.WithCompression(true))

	for i := 1; i <= 5; i++ {
		gen.AddSimpleURL(fmt.Sprintf("https://example.com/page/%d", i))
	}

	// Save to file
	filename := "sitemap.xml.gz"
	err := gen.ToFile(filename)
	if err != nil {
		fmt.Printf("Error saving file: %v\n", err)
		return
	}
	defer os.Remove(filename)

	// Verify file size
	info, _ := os.Stat(filename)
	fmt.Printf("Compressed sitemap saved to: %s (%d bytes)\n", filename, info.Size())

	// Read it back
	parser := sitemap.NewParser()
	sitemap, _ := parser.ParseFile(filename)
	fmt.Printf("Parsed %d URLs from compressed file\n", len(sitemap.URLs))
}

// Helper function
func floatPtr(f float64) *float64 {
	return &f
}