# sitemap_utils - Sitemap Generator for Go

A zero-dependency, production-ready sitemap generator module for Go. Supports standard XML sitemaps, sitemap indexes, multi-language URLs, and batch generation for large sites.

## Features

- **Standard XML Sitemaps**: Generate sitemaps compliant with sitemap.org protocol
- **Sitemap Index**: Create index files for multiple sitemaps
- **Multi-language URLs**: Support for hreflang/alternate links
- **Batch Generation**: Handle large sites with automatic splitting
- **Compression**: Optional gzip compression
- **URL Builder**: Helper for constructing URLs
- **Parser**: Parse existing sitemap files
- **Thread-safe**: All operations are concurrency-safe

## Constants

```go
const (
    MaxURLsPerSitemap   = 50000   // Maximum URLs per sitemap
    MaxSitemapSize      = 50MB    // Maximum uncompressed size
    MaxSitemapsPerIndex = 50000   // Maximum sitemaps per index
)
```

## Change Frequency Constants

```go
const (
    Always    ChangeFreq = "always"
    Hourly    ChangeFreq = "hourly"
    Daily     ChangeFreq = "daily"
    Weekly    ChangeFreq = "weekly"
    Monthly   ChangeFreq = "monthly"
    Yearly    ChangeFreq = "yearly"
    Never     ChangeFreq = "never"
)
```

## Quick Start

### Basic Sitemap

```go
package main

import (
    "fmt"
    sitemap "github.com/alltoolkit/sitemap_utils"
)

func main() {
    gen := sitemap.NewGenerator()
    
    // Add URLs
    gen.AddSimpleURL("https://example.com/")
    gen.AddSimpleURL("https://example.com/about")
    
    // Generate XML
    xml, err := gen.ToXML()
    if err != nil {
        panic(err)
    }
    
    fmt.Println(string(xml))
}
```

### Sitemap with Details

```go
gen := sitemap.NewGenerator(sitemap.WithPrettyPrint(true))

now := time.Now()
priority := 0.8

gen.AddURL(sitemap.URL{
    Loc:        "https://example.com/",
    LastMod:    &now,
    ChangeFreq: &sitemap.Daily,
    Priority:   &priority,
})

xml, _ := gen.ToXML()
// Save to file
gen.ToFile("sitemap.xml")
```

### Multi-language Sitemap

```go
gen := sitemap.NewGenerator()

alternates := []sitemap.Alternate{
    {Hreflang: "en", Href: "https://example.com/en/page"},
    {Hreflang: "es", Href: "https://example.com/es/page"},
    {Hreflang: "fr", Href: "https://example.com/fr/page"},
}

gen.AddAlternateURL("https://example.com/en/page", alternates, nil)
```

## Configuration Options

```go
gen := sitemap.NewGenerator(
    sitemap.WithMaxURLs(1000),          // Limit URLs per sitemap
    sitemap.WithCompression(true),       // Enable gzip compression
    sitemap.WithPrettyPrint(true),       // Enable XML indentation
    sitemap.WithBaseURL("https://site"), // Base URL for relative paths
)
```

## Sitemap Index

For sites with many URLs, create a sitemap index:

```go
index := sitemap.NewIndexGenerator()

now := time.Now()
index.AddSitemap("https://example.com/sitemap-products.xml", &now)
index.AddSitemap("https://example.com/sitemap-blog.xml", &now)

xml, _ := index.ToXML()
index.ToFile("sitemap_index.xml")
```

## Batch Generation

For large sites, use batch generation:

```go
batch := sitemap.NewBatchGenerator(1000) // 1000 URLs per sitemap

// Add many URLs
for i := 0; i < 50000; i++ {
    batch.AddURL(sitemap.URL{Loc: fmt.Sprintf("https://site.com/page/%d", i)})
}

// Save all sitemaps
filenames, _ := batch.ToFiles("sitemap")

// Create index
indexXML, _ := batch.CreateIndex("https://site.com/sitemap")
```

## URL Builder

Helper for constructing URLs:

```go
builder := sitemap.NewURLBuilder("https://example.com")

url1 := builder.Path("products").Path("123").Build()
// => https://example.com/products/123

builder.Reset()
url2 := builder.Path("search").Param("q", "test").Param("page", "1").Build()
// => https://example.com/search?q=test&page=1
```

## Parser

Parse existing sitemaps:

```go
parser := sitemap.NewParser()

// Parse from bytes
sitemap, err := parser.Parse(xmlData)

// Parse from file
sitemap, err := parser.ParseFile("sitemap.xml")

// Parse compressed file
sitemap, err := parser.ParseFile("sitemap.xml.gz") // Auto-detects gzip

// Parse sitemap index
entries, err := parser.ParseIndex(indexData)
```

## URL Structure

```go
type URL struct {
    Loc        string      // Required: URL location
    LastMod    *time.Time  // Optional: Last modification time
    ChangeFreq *ChangeFreq // Optional: Change frequency
    Priority   *float64    // Optional: Priority (0.0-1.0)
    Alternates []Alternate // Optional: Language alternatives
}

type Alternate struct {
    Hreflang string // Language code
    Href     string // URL for this language
}
```

## Validation

The generator validates:
- URL length (max 2048 characters)
- Priority range (0.0 to 1.0)
- Empty URLs are rejected
- URLs are trimmed for whitespace

## Output Format

Standard sitemap.org format:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://example.com/</loc>
    <lastmod>2024-01-01</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>
```

For multi-language:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" 
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
  <url>
    <loc>https://example.com/en/page</loc>
    <xhtml:link hreflang="en" href="https://example.com/en/page"/>
    <xhtml:link hreflang="es" href="https://example.com/es/page"/>
  </url>
</urlset>
```

## Running Tests

```bash
go test ./...
go test -v ./...
```

## License

MIT License

## Author

AllToolkit