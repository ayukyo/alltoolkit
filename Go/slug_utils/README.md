# Slug Utils (Go)

A zero-dependency Go package for generating URL-friendly slug strings. Perfect for blog posts, product URLs, and SEO-friendly links.

## Features

- 🚀 **Zero external dependencies** - Pure Go standard library
- 🌐 **Unicode support** - Transliterates accented characters (café → cafe)
- 🌍 **Multi-language support** - Latin, Cyrillic, Greek, Chinese, Japanese, Korean, Arabic
- ⚙️ **Configurable** - Custom separators, max length, case preservation
- 🔢 **Unique slug generation** - Auto-increment for duplicates
- ✅ **Validation utilities** - Check if strings are valid slugs
- 📊 **Benchmarked** - High performance

## Installation

```bash
go get github.com/ayukyo/alltoolkit/Go/slug_utils
```

## Quick Start

```go
package main

import (
    "fmt"
    slugutils "github.com/ayukyo/alltoolkit/Go/slug_utils"
)

func main() {
    // Basic usage
    slug := slugutils.Generate("Hello World!")
    fmt.Println(slug) // Output: hello-world

    // With configuration
    slugger := slugutils.NewWithConfig(slugutils.Config{
        Separator: "_",
        MaxLength: 20,
        Lowercase: true,
    })
    fmt.Println(slugger.Generate("My Blog Post Title")) // Output: my_blog_post_title
}
```

## API Reference

### Package-level Functions

```go
// Generate a slug with default configuration
slug := slugutils.Generate("Hello World!") // "hello-world"

// Generate from multiple inputs
slug := slugutils.GenerateMultiple("Hello", "World", "2024") // "hello-world-2024"

// Generate unique slug (with duplicate checker)
exists := func(s string) bool { return false } // Your database check
slug := slugutils.GenerateUnique("Hello World", exists) // "hello-world" or "hello-world-1"

// Check if a string is a valid slug
valid := slugutils.IsValidSlug("hello-world") // true

// Parse slug back to words
words := slugutils.ParseSlug("hello-world-2024", "-") // ["hello", "world", "2024"]

// Truncate a slug
short := slugutils.Truncate("this-is-a-long-slug", 10, "-") // "this-is"
```

### Configurable Slugger

```go
// Default configuration
slugger := slugutils.New()

// Custom configuration
slugger := slugutils.NewWithConfig(slugutils.Config{
    Separator:     "-",  // Word separator (default: "-")
    MaxLength:     0,    // Max slug length, 0 = unlimited
    Lowercase:     true, // Convert to lowercase
    TrimSeparator: true, // Remove leading/trailing separators
})

// Generate slug
slug := slugger.Generate("Hello World!")

// Generate unique slug
slug := slugger.GenerateUnique("Hello World", existsFunc)

// Generate from multiple parts
slug := slugger.GenerateMultiple("Hello", "World", "2024")
```

## Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `Separator` | string | `"-"` | Character(s) to separate words |
| `MaxLength` | int | `0` | Maximum slug length (0 = unlimited) |
| `Lowercase` | bool | `true` | Convert output to lowercase |
| `TrimSeparator` | bool | `true` | Remove leading/trailing separators |

## Transliteration Support

The package automatically transliterates characters from various scripts:

### Latin Extended (Accents)
- `café` → `cafe`
- `naïve` → `naive`
- `München` → `muenchen`
- `año` → `ano`

### Cyrillic
- `Привет мир` → `privet-mir`
- `Москва` → `moskva`

### Greek
- `Αθήνα` → `athina`
- `γεια σου` → `geia-sou`

### Currency Symbols
- `€100` → `eur-100`
- `£50` → `gbp-50`
- `$20` → `usd-20`

### Special Symbols
- `©` → `c` (copyright)
- `®` → `r` (registered)
- `™` → `tm` (trademark)
- `°` → `deg` (degree)

## Real-World Examples

### Blog Posts

```go
slugger := slugutils.New()

titles := []string{
    "10 Tips for Better Sleep 😴",
    "How to Build a REST API with Go",
    "What's New in 2024?!",
}

for _, title := range titles {
    fmt.Println(slugger.Generate(title))
}
// Output:
// 10-tips-for-better-sleep
// how-to-build-a-rest-api-with-go
// whats-new-in-2024
```

### Product URLs

```go
products := []string{
    "Apple iPhone 15 Pro Max (256GB)",
    "Sony WH-1000XM5 Wireless Headphones",
}

for _, product := range products {
    fmt.Println(slugger.Generate(product))
}
// Output:
// apple-iphone-15-pro-max-256gb
// sony-wh-1000xm5-wireless-headphones
```

### Unique Slugs for Database

```go
// Simulate database
existingSlugs := make(map[string]bool)

// Add existing slugs
existingSlugs["my-post"] = true
existingSlugs["my-post-1"] = true

// Generate unique slug
slug := slugger.GenerateUnique("My Post", existingSlugs)
fmt.Println(slug) // Output: my-post-2
```

## Performance

Benchmarks on a typical machine:

```
BenchmarkGenerate-8              5000000    230 ns/op    32 B/op    2 allocs/op
BenchmarkGenerateShort-8        10000000    158 ns/op    16 B/op    1 allocs/op
BenchmarkGenerateUnique-8       3000000     420 ns/op    48 B/op    3 allocs/op
BenchmarkTransliteration-8      3000000     450 ns/op    96 B/op    5 allocs/op
```

## Testing

Run tests:

```bash
go test ./...
```

Run benchmarks:

```bash
go test -bench=. ./...
```

## License

MIT License - Part of the AllToolkit project.