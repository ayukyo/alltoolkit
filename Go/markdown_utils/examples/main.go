// Example demonstrating markdown_utils usage
package main

import (
	"fmt"
	"strings"

	"github.com/ayukyo/alltoolkit/markdown_utils"
)

func main() {
	fmt.Println("=== Markdown Utils Demo ===")
	fmt.Println()

	// Example 1: Basic parsing
	fmt.Println("--- Example 1: Basic Parsing ---")
	markdown := `# Hello World

This is a paragraph with **bold** and *italic* text.

## Features

- Fast parsing
- Zero dependencies
- Full CommonMark support

Visit [OpenClaw](https://openclaw.ai)!`

	elements := markdown_utils.Parse(markdown)
	fmt.Printf("Parsed %d elements\n", len(elements))
	fmt.Println()

	// Example 2: Render to HTML
	fmt.Println("--- Example 2: HTML Rendering ---")
	html := markdown_utils.ParseToHTML(markdown)
	fmt.Println("Generated HTML:")
	fmt.Println(html)

	// Example 3: Extract headings
	fmt.Println("--- Example 3: Extract Headings ---")
	headings := markdown_utils.GetHeadings(elements)
	fmt.Printf("Found %d headings:\n", len(headings))
	for _, h := range headings {
		fmt.Printf("  H%d: %s\n", h.Level, h.Content)
	}
	fmt.Println()

	// Example 4: Extract links
	fmt.Println("--- Example 4: Extract Links ---")
	links := markdown_utils.GetLinks(elements)
	fmt.Printf("Found %d links:\n", len(links))
	for _, link := range links {
		fmt.Printf("  [%s](%s)\n", link.Content, link.URL)
	}
	fmt.Println()

	// Example 5: Table of Contents
	fmt.Println("--- Example 5: Table of Contents ---")
	toc := markdown_utils.CreateTableOfContents(headings)
	fmt.Println(toc)
	fmt.Println()

	// Example 6: Code blocks
	fmt.Println("--- Example 6: Code Blocks ---")
	codeMarkdown := `Here is some code:

` + "```go" + `
package main

import "fmt"

func main() {
    fmt.Println("Hello, World!")
}
` + "```" + `

And inline \`code\` too!`

	codeElements := markdown_utils.Parse(codeMarkdown)
	codeBlocks := markdown_utils.GetCodeBlocks(codeElements)
	fmt.Printf("Found %d code blocks\n", len(codeBlocks))
	for _, block := range codeBlocks {
		fmt.Printf("Language: %s\n", block.Language)
		fmt.Printf("Lines: %d\n", len(strings.Split(block.Content, "\n")))
	}
	fmt.Println()

	// Example 7: Lists
	fmt.Println("--- Example 7: Lists ---")
	listMarkdown := `Shopping list:

1. Apples
2. Oranges
3. Bananas

Todo:
- Buy groceries
- Clean house
- Walk dog`

	listElements := markdown_utils.Parse(listMarkdown)
	html = markdown_utils.ParseToHTML(listMarkdown)
	fmt.Println(html)

	// Example 8: Blockquotes
	fmt.Println("--- Example 8: Blockquotes ---")
	quoteMarkdown := `> The only way to do great work
> is to love what you do.
>
> — Steve Jobs`

	fmt.Println(markdown_utils.ParseToHTML(quoteMarkdown))

	// Example 9: Word count and reading time
	fmt.Println("--- Example 9: Word Count & Reading Time ---")
	article := strings.Repeat("word ", 400) // 400 words
	wordCount := markdown_utils.WordCount(article)
	readTime := markdown_utils.ReadingTime(article)
	fmt.Printf("Word count: %d\n", wordCount)
	fmt.Printf("Reading time: %d minutes\n", readTime)
	fmt.Println()

	// Example 10: Strip Markdown
	fmt.Println("--- Example 10: Strip Markdown ---")
	formatted := "**Bold** and *italic* with `code`"
	plain := markdown_utils.StripMarkdown(formatted)
	fmt.Printf("Original: %s\n", formatted)
	fmt.Printf("Stripped: %s\n", plain)
	fmt.Println()

	// Example 11: Complete document
	fmt.Println("--- Example 11: Complete Document ---")
	doc := `# Go Markdown Parser

A lightweight **Markdown** parser written in pure Go.

## Features

- Zero external dependencies
- Full CommonMark support
- Fast and memory efficient

## Installation

` + "```bash" + `
go get github.com/ayukyo/alltoolkit/markdown_utils
` + "```" + `

## Quick Start

` + "```go" + `
html := markdown_utils.ParseToHTML("# Hello")
fmt.Println(html) // <h1>Hello</h1>
` + "```" + `

## License

MIT License - see [LICENSE](LICENSE) for details.

---

Made with ❤️ by the OpenClaw team
`

	md := markdown_utils.ParseComplete(doc)
	fmt.Printf("Elements: %d\n", len(md.Elements))
	fmt.Printf("HTML length: %d bytes\n", len(md.HTML))
	fmt.Println()

	// Example 12: Images
	fmt.Println("--- Example 12: Images ---")
	imgMarkdown := `![OpenClaw Logo](https://openclaw.ai/logo.png)

Here's a diagram:

![Architecture Diagram](diagram.png)`
	imgElements := markdown_utils.Parse(imgMarkdown)
	images := markdown_utils.GetImages(imgElements)
	fmt.Printf("Found %d images:\n", len(images))
	for _, img := range images {
		fmt.Printf("  Alt: %s, URL: %s\n", img.Alt, img.URL)
	}
}