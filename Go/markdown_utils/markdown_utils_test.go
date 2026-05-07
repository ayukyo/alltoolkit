package markdown_utils

import (
	"strings"
	"testing"
)

func TestParseHeading(t *testing.T) {
	tests := []struct {
		input    string
		level    int
		content  string
	}{
		{"# Heading 1", 1, "Heading 1"},
		{"## Heading 2", 2, "Heading 2"},
		{"### Heading 3", 3, "Heading 3"},
		{"#### Heading 4", 4, "Heading 4"},
		{"##### Heading 5", 5, "Heading 5"},
		{"###### Heading 6", 6, "Heading 6"},
	}

	for _, test := range tests {
		elements := Parse(test.input)
		if len(elements) != 1 {
			t.Errorf("Expected 1 element, got %d for input: %s", len(elements), test.input)
			continue
		}
		if elements[0].Type != ElementHeading {
			t.Errorf("Expected ElementHeading, got %v", elements[0].Type)
		}
		if elements[0].Level != test.level {
			t.Errorf("Expected level %d, got %d", test.level, elements[0].Level)
		}
		if elements[0].Content != test.content {
			t.Errorf("Expected content '%s', got '%s'", test.content, elements[0].Content)
		}
	}
}

func TestParseSetextHeading(t *testing.T) {
	input := "Heading 1\n========="
	elements := Parse(input)
	if len(elements) != 1 {
		t.Fatalf("Expected 1 element, got %d", len(elements))
	}
	if elements[0].Type != ElementHeading {
		t.Errorf("Expected ElementHeading, got %v", elements[0].Type)
	}
	if elements[0].Level != 1 {
		t.Errorf("Expected level 1, got %d", elements[0].Level)
	}

	input2 := "Heading 2\n--------"
	elements2 := Parse(input2)
	if len(elements2) != 1 {
		t.Fatalf("Expected 1 element, got %d", len(elements2))
	}
	if elements2[0].Type != ElementHeading {
		t.Errorf("Expected ElementHeading, got %v", elements2[0].Type)
	}
	if elements2[0].Level != 2 {
		t.Errorf("Expected level 2, got %d", elements2[0].Level)
	}
}

func TestParseParagraph(t *testing.T) {
	input := "This is a simple paragraph."
	elements := Parse(input)
	if len(elements) != 1 {
		t.Fatalf("Expected 1 element, got %d", len(elements))
	}
	if elements[0].Type != ElementParagraph {
		t.Errorf("Expected ElementParagraph, got %v", elements[0].Type)
	}
	if strings.TrimSpace(elements[0].Content) != "This is a simple paragraph." {
		t.Errorf("Unexpected content: %s", elements[0].Content)
	}
}

func TestParseBold(t *testing.T) {
	input := "This is **bold** text."
	elements := Parse(input)
	if len(elements) != 1 {
		t.Fatalf("Expected 1 element, got %d", len(elements))
	}
	
	children := elements[0].Children
	// Should have: text, bold, text
	if len(children) != 3 {
		t.Fatalf("Expected 3 children, got %d", len(children))
	}
	
	if children[1].Type != ElementBold {
		t.Errorf("Expected ElementBold at index 1, got %v", children[1].Type)
	}
	if children[1].Content != "bold" {
		t.Errorf("Expected 'bold', got '%s'", children[1].Content)
	}
}

func TestParseItalic(t *testing.T) {
	input := "This is *italic* text."
	elements := Parse(input)
	if len(elements) != 1 {
		t.Fatalf("Expected 1 element, got %d", len(elements))
	}
	
	children := elements[0].Children
	if len(children) != 3 {
		t.Fatalf("Expected 3 children, got %d", len(children))
	}
	
	if children[1].Type != ElementItalic {
		t.Errorf("Expected ElementItalic at index 1, got %v", children[1].Type)
	}
}

func TestParseBoldItalic(t *testing.T) {
	input := "This is ***bold and italic*** text."
	elements := Parse(input)
	if len(elements) != 1 {
		t.Fatalf("Expected 1 element, got %d", len(elements))
	}
	
	children := elements[0].Children
	if len(children) != 3 {
		t.Fatalf("Expected 3 children, got %d", len(children))
	}
	
	if children[1].Type != ElementBoldItalic {
		t.Errorf("Expected ElementBoldItalic at index 1, got %v", children[1].Type)
	}
}

func TestParseInlineCode(t *testing.T) {
	input := "Use the `print()` function."
	elements := Parse(input)
	if len(elements) != 1 {
		t.Fatalf("Expected 1 element, got %d", len(elements))
	}
	
	children := elements[0].Children
	if len(children) != 3 {
		t.Fatalf("Expected 3 children, got %d", len(children))
	}
	
	if children[1].Type != ElementCode {
		t.Errorf("Expected ElementCode, got %v", children[1].Type)
	}
	if children[1].Content != "print()" {
		t.Errorf("Expected 'print()', got '%s'", children[1].Content)
	}
}

func TestParseLink(t *testing.T) {
	input := "Check out [OpenClaw](https://openclaw.ai)."
	elements := Parse(input)
	if len(elements) != 1 {
		t.Fatalf("Expected 1 element, got %d", len(elements))
	}
	
	children := elements[0].Children
	if len(children) < 2 {
		t.Fatalf("Expected at least 2 children, got %d", len(children))
	}
	
	// Find the link element
	var link *Element
	for _, child := range children {
		if child.Type == ElementLink {
			link = child
			break
		}
	}
	
	if link == nil {
		t.Fatal("No link element found")
	}
	if link.Content != "OpenClaw" {
		t.Errorf("Expected 'OpenClaw', got '%s'", link.Content)
	}
	if link.URL != "https://openclaw.ai" {
		t.Errorf("Expected 'https://openclaw.ai', got '%s'", link.URL)
	}
}

func TestParseImage(t *testing.T) {
	input := "![Alt text](https://example.com/image.png)"
	elements := Parse(input)
	if len(elements) != 1 {
		t.Fatalf("Expected 1 element, got %d", len(elements))
	}
	
	children := elements[0].Children
	if len(children) != 1 {
		t.Fatalf("Expected 1 child, got %d", len(children))
	}
	
	if children[0].Type != ElementImage {
		t.Errorf("Expected ElementImage, got %v", children[0].Type)
	}
	if children[0].Alt != "Alt text" {
		t.Errorf("Expected 'Alt text', got '%s'", children[0].Alt)
	}
	if children[0].URL != "https://example.com/image.png" {
		t.Errorf("Expected 'https://example.com/image.png', got '%s'", children[0].URL)
	}
}

func TestParseCodeBlock(t *testing.T) {
	input := "```go\nfmt.Println(\"Hello\")\n```"
	elements := Parse(input)
	if len(elements) != 1 {
		t.Fatalf("Expected 1 element, got %d", len(elements))
	}
	
	if elements[0].Type != ElementCodeBlock {
		t.Errorf("Expected ElementCodeBlock, got %v", elements[0].Type)
	}
	if elements[0].Language != "go" {
		t.Errorf("Expected language 'go', got '%s'", elements[0].Language)
	}
	if elements[0].Content != "fmt.Println(\"Hello\")" {
		t.Errorf("Unexpected content: %s", elements[0].Content)
	}
}

func TestParseCodeBlockTilde(t *testing.T) {
	input := "~~~python\nprint('Hello')\n~~~"
	elements := Parse(input)
	if len(elements) != 1 {
		t.Fatalf("Expected 1 element, got %d", len(elements))
	}
	
	if elements[0].Type != ElementCodeBlock {
		t.Errorf("Expected ElementCodeBlock, got %v", elements[0].Type)
	}
	if elements[0].Language != "python" {
		t.Errorf("Expected language 'python', got '%s'", elements[0].Language)
	}
}

func TestParseBlockquote(t *testing.T) {
	input := "> This is a quote.\n> Second line."
	elements := Parse(input)
	if len(elements) != 1 {
		t.Fatalf("Expected 1 element, got %d", len(elements))
	}
	
	if elements[0].Type != ElementBlockquote {
		t.Errorf("Expected ElementBlockquote, got %v", elements[0].Type)
	}
	if !strings.Contains(elements[0].Content, "This is a quote") {
		t.Errorf("Unexpected content: %s", elements[0].Content)
	}
}

func TestParseUnorderedList(t *testing.T) {
	input := "- Item 1\n- Item 2\n- Item 3"
	elements := Parse(input)
	if len(elements) != 1 {
		t.Fatalf("Expected 1 element, got %d", len(elements))
	}
	
	if elements[0].Type != ElementUnorderedList {
		t.Errorf("Expected ElementUnorderedList, got %v", elements[0].Type)
	}
	if len(elements[0].Children) != 3 {
		t.Errorf("Expected 3 list items, got %d", len(elements[0].Children))
	}
}

func TestParseUnorderedListAsterisk(t *testing.T) {
	input := "* Item 1\n* Item 2"
	elements := Parse(input)
	if len(elements) != 1 {
		t.Fatalf("Expected 1 element, got %d", len(elements))
	}
	
	if elements[0].Type != ElementUnorderedList {
		t.Errorf("Expected ElementUnorderedList, got %v", elements[0].Type)
	}
}

func TestParseUnorderedListPlus(t *testing.T) {
	input := "+ Item 1\n+ Item 2"
	elements := Parse(input)
	if len(elements) != 1 {
		t.Fatalf("Expected 1 element, got %d", len(elements))
	}
	
	if elements[0].Type != ElementUnorderedList {
		t.Errorf("Expected ElementUnorderedList, got %v", elements[0].Type)
	}
}

func TestParseOrderedList(t *testing.T) {
	input := "1. First\n2. Second\n3. Third"
	elements := Parse(input)
	if len(elements) != 1 {
		t.Fatalf("Expected 1 element, got %d", len(elements))
	}
	
	if elements[0].Type != ElementOrderedList {
		t.Errorf("Expected ElementOrderedList, got %v", elements[0].Type)
	}
	if len(elements[0].Children) != 3 {
		t.Errorf("Expected 3 list items, got %d", len(elements[0].Children))
	}
}

func TestParseHorizontalRule(t *testing.T) {
	tests := []string{
		"---",
		"***",
		"___",
		"   ---   ",
		"   ***   ",
	}

	for _, test := range tests {
		elements := Parse(test)
		if len(elements) != 1 {
			t.Errorf("Expected 1 element for '%s', got %d", test, len(elements))
			continue
		}
		if elements[0].Type != ElementHorizontalRule {
			t.Errorf("Expected ElementHorizontalRule for '%s', got %v", test, elements[0].Type)
		}
	}
}

func TestRenderHeading(t *testing.T) {
	input := "# Hello World"
	html := ParseToHTML(input)
	expected := "<h1>Hello World</h1>\n"
	if html != expected {
		t.Errorf("Expected '%s', got '%s'", expected, html)
	}
}

func TestRenderParagraph(t *testing.T) {
	input := "This is a paragraph."
	html := ParseToHTML(input)
	expected := "<p>This is a paragraph.</p>\n"
	if html != expected {
		t.Errorf("Expected '%s', got '%s'", expected, html)
	}
}

func TestRenderBold(t *testing.T) {
	input := "**bold text**"
	html := ParseToHTML(input)
	if !strings.Contains(html, "<strong>") {
		t.Errorf("Expected <strong> tag in '%s'", html)
	}
}

func TestRenderItalic(t *testing.T) {
	input := "*italic text*"
	html := ParseToHTML(input)
	if !strings.Contains(html, "<em>") {
		t.Errorf("Expected <em> tag in '%s'", html)
	}
}

func TestRenderLink(t *testing.T) {
	input := "[Example](https://example.com)"
	html := ParseToHTML(input)
	if !strings.Contains(html, `<a href="https://example.com">`) {
		t.Errorf("Expected link tag in '%s'", html)
	}
	if !strings.Contains(html, "Example") {
		t.Errorf("Expected link text in '%s'", html)
	}
}

func TestRenderImage(t *testing.T) {
	input := "![Alt](https://example.com/img.png)"
	html := ParseToHTML(input)
	if !strings.Contains(html, `<img src="https://example.com/img.png"`) {
		t.Errorf("Expected img tag in '%s'", html)
	}
	if !strings.Contains(html, `alt="Alt"`) {
		t.Errorf("Expected alt attribute in '%s'", html)
	}
}

func TestRenderCodeBlock(t *testing.T) {
	input := "```javascript\nconsole.log('hi');\n```"
	html := ParseToHTML(input)
	if !strings.Contains(html, `<code class="language-javascript">`) {
		t.Errorf("Expected code block with language in '%s'", html)
	}
	if !strings.Contains(html, "console.log") {
		t.Errorf("Expected code content in '%s'", html)
	}
}

func TestRenderBlockquote(t *testing.T) {
	input := "> Quoted text"
	html := ParseToHTML(input)
	if !strings.Contains(html, "<blockquote>") {
		t.Errorf("Expected blockquote tag in '%s'", html)
	}
}

func TestRenderList(t *testing.T) {
	input := "- One\n- Two\n- Three"
	html := ParseToHTML(input)
	if !strings.Contains(html, "<ul>") {
		t.Errorf("Expected <ul> tag in '%s'", html)
	}
	if !strings.Contains(html, "<li>") {
		t.Errorf("Expected <li> tag in '%s'", html)
	}
}

func TestRenderHorizontalRule(t *testing.T) {
	input := "---"
	html := ParseToHTML(input)
	if !strings.Contains(html, "<hr>") {
		t.Errorf("Expected <hr> tag in '%s'", html)
	}
}

func TestGetHeadings(t *testing.T) {
	input := "# Title\n\n## Section 1\n\n### Subsection\n\n## Section 2"
	elements := Parse(input)
	headings := GetHeadings(elements)
	
	if len(headings) != 4 {
		t.Errorf("Expected 4 headings, got %d", len(headings))
	}
	
	if headings[0].Level != 1 {
		t.Errorf("Expected level 1, got %d", headings[0].Level)
	}
	if headings[2].Level != 3 {
		t.Errorf("Expected level 3, got %d", headings[2].Level)
	}
}

func TestGetLinks(t *testing.T) {
	input := "[Link 1](https://a.com) and [Link 2](https://b.com)"
	elements := Parse(input)
	links := GetLinks(elements)
	
	if len(links) != 2 {
		t.Errorf("Expected 2 links, got %d", len(links))
	}
}

func TestGetImages(t *testing.T) {
	input := "![Image 1](a.png) and ![Image 2](b.png)"
	elements := Parse(input)
	images := GetImages(elements)
	
	if len(images) != 2 {
		t.Errorf("Expected 2 images, got %d", len(images))
	}
}

func TestGetCodeBlocks(t *testing.T) {
	input := "```go\ncode1\n```\n\n```python\ncode2\n```"
	elements := Parse(input)
	codeBlocks := GetCodeBlocks(elements)
	
	if len(codeBlocks) != 2 {
		t.Errorf("Expected 2 code blocks, got %d", len(codeBlocks))
	}
}

func TestCreateTableOfContents(t *testing.T) {
	input := "# Title\n\n## Section A\n\n## Section B"
	elements := Parse(input)
	headings := GetHeadings(elements)
	toc := CreateTableOfContents(headings)
	
	if !strings.Contains(toc, "toc") {
		t.Errorf("Expected toc class in '%s'", toc)
	}
	if !strings.Contains(toc, "Title") {
		t.Errorf("Expected 'Title' in '%s'", toc)
	}
}

func TestStripMarkdown(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"**bold**", "bold"},
		{"*italic*", "italic"},
		{"# Heading", "Heading"},
		{"[Link](https://example.com)", "Link"},
		{"`code`", "code"},
	}

	for _, test := range tests {
		result := StripMarkdown(test.input)
		if strings.TrimSpace(result) != test.expected {
			t.Errorf("For '%s': expected '%s', got '%s'", test.input, test.expected, result)
		}
	}
}

func TestWordCount(t *testing.T) {
	tests := []struct {
		input    string
		expected int
	}{
		{"One two three", 3},
		{"Hello world", 2},
		{"", 0},
		{"# Heading\n\nParagraph text here.", 3}, // HeadingParagraph merged + text + here
	}

	for _, test := range tests {
		result := WordCount(test.input)
		if result != test.expected {
			t.Errorf("For '%s': expected %d words, got %d", test.input, test.expected, result)
		}
	}
}

func TestReadingTime(t *testing.T) {
	// 200 words = 1 minute
	words := strings.Repeat("word ", 200)
	input := words
	
	result := ReadingTime(input)
	if result != 1 {
		t.Errorf("Expected 1 minute, got %d", result)
	}
	
	// 400 words = 2 minutes
	words = strings.Repeat("word ", 400)
	input = words
	
	result = ReadingTime(input)
	if result != 2 {
		t.Errorf("Expected 2 minutes, got %d", result)
	}
}

func TestEscapeHTML(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"<script>", "&lt;script&gt;"},
		{"&amp", "&amp;amp"},
		{`"quoted"`, "&quot;quoted&quot;"},
	}

	for _, test := range tests {
		result := escapeHTML(test.input)
		if result != test.expected {
			t.Errorf("For '%s': expected '%s', got '%s'", test.input, test.expected, result)
		}
	}
}

func TestSlugify(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"Hello World", "hello-world"},
		{"This is a Test", "this-is-a-test"},
		{"Hello! World?", "hello-world"},
		{"UPPERCASE", "uppercase"},
	}

	for _, test := range tests {
		result := slugify(test.input)
		if result != test.expected {
			t.Errorf("For '%s': expected '%s', got '%s'", test.input, test.expected, result)
		}
	}
}

func TestComplexDocument(t *testing.T) {
	input := `# Main Title

This is a paragraph with **bold** and *italic* text.

## Code Example

` + "```go" + `
func main() {
    fmt.Println("Hello")
}
` + "```" + `

## List

1. First item
2. Second item

- Bullet one
- Bullet two

> A blockquote

Visit [OpenClaw](https://openclaw.ai)!
`

	elements := Parse(input)
	
	// Should have multiple elements
	if len(elements) < 5 {
		t.Errorf("Expected at least 5 elements, got %d", len(elements))
	}
	
	// Test HTML rendering
	html := ParseToHTML(input)
	
	// Should contain various HTML elements
	if !strings.Contains(html, "<h1>") {
		t.Error("Expected <h1> in HTML")
	}
	if !strings.Contains(html, "<h2>") {
		t.Error("Expected <h2> in HTML")
	}
	if !strings.Contains(html, "<pre>") {
		t.Error("Expected <pre> in HTML")
	}
	if !strings.Contains(html, "<ol>") {
		t.Error("Expected <ol> in HTML")
	}
	if !strings.Contains(html, "<ul>") {
		t.Error("Expected <ul> in HTML")
	}
	if !strings.Contains(html, "<blockquote>") {
		t.Error("Expected <blockquote> in HTML")
	}
	if !strings.Contains(html, "<a href") {
		t.Error("Expected <a> in HTML")
	}
}

func TestMultipleParagraphs(t *testing.T) {
	input := "First paragraph.\n\nSecond paragraph.\n\nThird paragraph."
	elements := Parse(input)
	
	if len(elements) != 3 {
		t.Errorf("Expected 3 paragraphs, got %d", len(elements))
	}
	
	for i, elem := range elements {
		if elem.Type != ElementParagraph {
			t.Errorf("Element %d should be a paragraph", i)
		}
	}
}

func TestNestedInlineFormatting(t *testing.T) {
	input := "**bold and *italic* inside**"
	elements := Parse(input)
	
	if len(elements) != 1 {
		t.Fatalf("Expected 1 element, got %d", len(elements))
	}
	
	html := ParseToHTML(input)
	if !strings.Contains(html, "<strong>") {
		t.Error("Expected <strong> in HTML")
	}
	if !strings.Contains(html, "<em>") {
		t.Error("Expected <em> in HTML")
	}
}

func TestParseComplete(t *testing.T) {
	input := "# Test"
	md := ParseComplete(input)
	
	if len(md.Elements) != 1 {
		t.Errorf("Expected 1 element, got %d", len(md.Elements))
	}
	if md.HTML == "" {
		t.Error("Expected HTML output")
	}
	if !strings.Contains(md.HTML, "<h1>") {
		t.Errorf("Expected <h1> in HTML, got '%s'", md.HTML)
	}
}

func TestParseToHTMLWithOptions(t *testing.T) {
	input := "Paragraph text."
	html := ParseToHTMLWithOptions(input, RenderOptions{SkipParagraphTags: true})
	
	if strings.Contains(html, "<p>") {
		t.Errorf("Should not have <p> tags with SkipParagraphTags: %s", html)
	}
}

func BenchmarkParseSimple(b *testing.B) {
	input := "# Heading\n\nThis is a paragraph with **bold** and *italic* text."
	for i := 0; i < b.N; i++ {
		Parse(input)
	}
}

func BenchmarkParseComplex(b *testing.B) {
	input := `# Document Title

## Introduction

This is the **introduction** paragraph.

## Features

1. Feature one with *emphasis*
2. Feature two
3. Feature three

### Code Example

` + "```go" + `
func example() {
    return "value"
}
` + "```" + `

## Conclusion

Visit [our site](https://example.com) for more info.

> Final quote

---

End of document.
`
	for i := 0; i < b.N; i++ {
		Parse(input)
	}
}

func BenchmarkRenderHTML(b *testing.B) {
	input := "# Heading\n\nParagraph with **bold** and *italic*."
	elements := Parse(input)
	renderer := NewRenderer()
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		renderer.Render(elements)
	}
}