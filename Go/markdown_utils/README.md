# Markdown Utils

A lightweight Markdown parser and renderer for Go with **zero external dependencies**.

## Features

- **Pure Go** - No external dependencies
- **CommonMark Support** - Parses standard Markdown elements
- **HTML Rendering** - Convert Markdown to HTML
- **Element Extraction** - Extract headings, links, images, code blocks
- **Utility Functions** - Word count, reading time estimation, plain text extraction
- **Table of Contents** - Auto-generate TOC from headings

## Installation

```bash
go get github.com/ayukyo/alltoolkit/markdown_utils
```

## Quick Start

```go
package main

import (
    "fmt"
    "github.com/ayukyo/alltoolkit/markdown_utils"
)

func main() {
    // Parse and render to HTML
    html := markdown_utils.ParseToHTML("# Hello World")
    fmt.Println(html)
    // Output: <h1>Hello World</h1>
}
```

## Supported Elements

| Element | Syntax |
|---------|--------|
| Headings | `# H1` through `###### H6` |
| Paragraphs | Plain text separated by blank lines |
| Bold | `**text**` or `__text__` |
| Italic | `*text*` or `_text_` |
| Bold + Italic | `***text***` |
| Links | `[text](url)` |
| Images | `![alt](url)` |
| Inline Code | `` `code` `` |
| Code Blocks | ` ```language ` fenced blocks |
| Blockquotes | `> quote` |
| Unordered Lists | `- item`, `* item`, `+ item` |
| Ordered Lists | `1. item` |
| Horizontal Rules | `---`, `***`, `___` |

## API Reference

### Parsing

```go
// Parse Markdown to elements
elements := markdown_utils.Parse("# Heading")

// Parse and render to HTML
html := markdown_utils.ParseToHTML("# Heading")

// Parse with custom options
html := markdown_utils.ParseToHTMLWithOptions(input, markdown_utils.RenderOptions{
    SkipParagraphTags: true,
})

// Get both elements and HTML
md := markdown_utils.ParseComplete("# Heading")
fmt.Println(md.Elements)
fmt.Println(md.HTML)
```

### Element Extraction

```go
elements := markdown_utils.Parse(input)

// Get all headings
headings := markdown_utils.GetHeadings(elements)

// Get all links
links := markdown_utils.GetLinks(elements)

// Get all images
images := markdown_utils.GetImages(elements)

// Get all code blocks
codeBlocks := markdown_utils.GetCodeBlocks(elements)
```

### Utilities

```go
// Generate table of contents
headings := markdown_utils.GetHeadings(elements)
toc := markdown_utils.CreateTableOfContents(headings)

// Strip Markdown formatting
plain := markdown_utils.StripMarkdown("**bold** and *italic*")
// Output: "bold and italic"

// Count words
words := markdown_utils.WordCount(input)

// Estimate reading time (minutes)
minutes := markdown_utils.ReadingTime(input)
```

### Element Types

```go
type ElementType int

const (
    ElementHeading
    ElementParagraph
    ElementBold
    ElementItalic
    ElementBoldItalic
    ElementLink
    ElementImage
    ElementCode
    ElementCodeBlock
    ElementBlockquote
    ElementUnorderedList
    ElementOrderedList
    ElementListItem
    ElementHorizontalRule
    ElementLineBreak
    ElementText
)
```

### Element Structure

```go
type Element struct {
    Type     ElementType
    Content  string
    Children []*Element
    Level    int    // For headings (1-6)
    URL      string // For links and images
    Alt      string // For images
    Language string // For code blocks
}
```

## Examples

### Complete Example

```go
package main

import (
    "fmt"
    "github.com/ayukyo/alltoolkit/markdown_utils"
)

func main() {
    input := `# My Article

This is a paragraph with **bold** text.

## Features

- Item 1
- Item 2

Visit [OpenClaw](https://openclaw.ai)!
`

    // Parse and render
    html := markdown_utils.ParseToHTML(input)
    fmt.Println(html)

    // Extract metadata
    elements := markdown_utils.Parse(input)
    headings := markdown_utils.GetHeadings(elements)
    links := markdown_utils.GetLinks(elements)

    fmt.Printf("Found %d headings\n", len(headings))
    fmt.Printf("Found %d links\n", len(links))
}
```

### Working with Code Blocks

```go
input := `Here is some code:

` + "```go" + `
func main() {
    fmt.Println("Hello!")
}
` + "```" + `

Inline ` + "`code`" + ` too!`

elements := markdown_utils.Parse(input)
codeBlocks := markdown_utils.GetCodeBlocks(elements)

for _, block := range codeBlocks {
    fmt.Printf("Language: %s\n", block.Language)
    fmt.Printf("Code: %s\n", block.Content)
}
```

### Table of Contents

```go
input := `# Main Title

## Section 1
### Subsection 1.1

## Section 2
### Subsection 2.1`

elements := markdown_utils.Parse(input)
headings := markdown_utils.GetHeadings(elements)
toc := markdown_utils.CreateTableOfContents(headings)

fmt.Println(toc)
// Output:
// <nav class="toc">
// <ul>
//   <li><a href="#main-title">Main Title</a></li>
//   <li><a href="#section-1">Section 1</a></li>
//   <li><a href="#subsection-11">Subsection 1.1</a></li>
//   <li><a href="#section-2">Section 2</a></li>
//   <li><a href="#subsection-21">Subsection 2.1</a></li>
// </ul>
// </nav>
```

## Performance

The parser is designed to be fast and memory-efficient:

- Single-pass parsing
- Minimal allocations
- No regex compilation overhead (pre-compiled patterns)

## License

MIT License