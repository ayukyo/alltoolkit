// Package markdown_utils provides a lightweight Markdown parser and renderer.
// This implementation has zero external dependencies and supports common Markdown elements.
package markdown_utils

import (
	"bytes"
	"fmt"
	"regexp"
	"strings"
)

// ElementType represents the type of a Markdown element
type ElementType int

const (
	ElementHeading ElementType = iota
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

// Element represents a parsed Markdown element
type Element struct {
	Type     ElementType
	Content  string
	Children []*Element
	Level    int    // For headings (1-6)
	URL      string // For links and images
	Alt      string // For images
	Language string // For code blocks
}

// Parser holds the state for parsing Markdown
type Parser struct {
	lines    []string
	pos     int
	elements []*Element
}

// NewParser creates a new Markdown parser
func NewParser(input string) *Parser {
	return &Parser{
		lines: strings.Split(input, "\n"),
		pos:   0,
	}
}

// Parse parses the Markdown input and returns a slice of elements
func (p *Parser) Parse() []*Element {
	var elements []*Element

	for p.pos < len(p.lines) {
		// Skip empty lines but preserve paragraph breaks
		if strings.TrimSpace(p.lines[p.pos]) == "" {
			p.pos++
			continue
		}

		element := p.parseBlock()
		if element != nil {
			elements = append(elements, element)
		}
	}

	return elements
}

// parseBlock parses a block-level element
func (p *Parser) parseBlock() *Element {
	line := p.lines[p.pos]

	// Try each block type in order
	if element := p.tryHeading(line); element != nil {
		return element
	}
	if element := p.tryCodeBlock(); element != nil {
		return element
	}
	if element := p.tryBlockquote(line); element != nil {
		return element
	}
	if element := p.tryHorizontalRule(line); element != nil {
		return element
	}
	if element := p.tryUnorderedList(line); element != nil {
		return element
	}
	if element := p.tryOrderedList(line); element != nil {
		return element
	}

	// Default: paragraph
	return p.parseParagraph()
}

// tryHeading attempts to parse a heading (h1-h6)
func (p *Parser) tryHeading(line string) *Element {
	// ATX-style headings (#)
	if matches := regexp.MustCompile(`^(#{1,6})\s+(.+)$`).FindStringSubmatch(line); matches != nil {
		level := len(matches[1])
		content := matches[2]
		p.pos++
		return &Element{
			Type:     ElementHeading,
			Level:    level,
			Content:  content,
			Children: p.parseInline(content),
		}
	}

	// Setext-style headings (underlined)
	if p.pos+1 < len(p.lines) {
		nextLine := p.lines[p.pos+1]
		if regexp.MustCompile(`^=+$`).MatchString(nextLine) {
			p.pos += 2
			return &Element{
				Type:     ElementHeading,
				Level:    1,
				Content:  line,
				Children: p.parseInline(line),
			}
		}
		if regexp.MustCompile(`^-+$`).MatchString(nextLine) {
			p.pos += 2
			return &Element{
				Type:     ElementHeading,
				Level:    2,
				Content:  line,
				Children: p.parseInline(line),
			}
		}
	}

	return nil
}

// tryCodeBlock attempts to parse a fenced code block
func (p *Parser) tryCodeBlock() *Element {
	line := p.lines[p.pos]

	// Fenced code block with ```
	if strings.HasPrefix(line, "```") {
		language := strings.TrimSpace(strings.TrimPrefix(line, "```"))
		p.pos++

		var codeLines []string
		for p.pos < len(p.lines) && !strings.HasPrefix(p.lines[p.pos], "```") {
			codeLines = append(codeLines, p.lines[p.pos])
			p.pos++
		}
		p.pos++ // Skip closing ```

		return &Element{
			Type:     ElementCodeBlock,
			Content:  strings.Join(codeLines, "\n"),
			Language: language,
		}
	}

	// Fenced code block with ~~~
	if strings.HasPrefix(line, "~~~") {
		language := strings.TrimSpace(strings.TrimPrefix(line, "~~~"))
		p.pos++

		var codeLines []string
		for p.pos < len(p.lines) && !strings.HasPrefix(p.lines[p.pos], "~~~") {
			codeLines = append(codeLines, p.lines[p.pos])
			p.pos++
		}
		p.pos++ // Skip closing ~~~

		return &Element{
			Type:     ElementCodeBlock,
			Content:  strings.Join(codeLines, "\n"),
			Language: language,
		}
	}

	return nil
}

// tryBlockquote attempts to parse a blockquote
func (p *Parser) tryBlockquote(line string) *Element {
	if !strings.HasPrefix(line, ">") {
		return nil
	}

	var lines []string
	for p.pos < len(p.lines) {
		currentLine := p.lines[p.pos]
		if strings.HasPrefix(currentLine, ">") {
			lines = append(lines, strings.TrimPrefix(currentLine, "> "))
			p.pos++
		} else if strings.TrimSpace(currentLine) == "" {
			p.pos++
		} else {
			break
		}
	}

	content := strings.Join(lines, "\n")
	return &Element{
		Type:     ElementBlockquote,
		Content:  content,
		Children: p.parseInline(content),
	}
}

// tryHorizontalRule attempts to parse a horizontal rule
func (p *Parser) tryHorizontalRule(line string) *Element {
	trimmed := strings.TrimSpace(line)
	if regexp.MustCompile(`^(-{3,}|\*{3,}|_{3,})$`).MatchString(trimmed) {
		p.pos++
		return &Element{Type: ElementHorizontalRule}
	}
	return nil
}

// tryUnorderedList attempts to parse an unordered list
func (p *Parser) tryUnorderedList(line string) *Element {
	markerPattern := regexp.MustCompile(`^(\s*)[-*+]\s+(.+)$`)

	if !markerPattern.MatchString(line) {
		return nil
	}

	list := &Element{Type: ElementUnorderedList}

	for p.pos < len(p.lines) {
		currentLine := p.lines[p.pos]
		matches := markerPattern.FindStringSubmatch(currentLine)

		if matches == nil {
			// Check if it's a continuation line
			if strings.TrimSpace(currentLine) != "" && !regexp.MustCompile(`^(\s*)([-*+]|\d+\.)\s`).MatchString(currentLine) {
				break
			}
			if strings.TrimSpace(currentLine) == "" {
				p.pos++
				continue
			}
			break
		}

		content := matches[2]
		list.Children = append(list.Children, &Element{
			Type:     ElementListItem,
			Content:  content,
			Children: p.parseInline(content),
		})
		p.pos++
	}

	return list
}

// tryOrderedList attempts to parse an ordered list
func (p *Parser) tryOrderedList(line string) *Element {
	markerPattern := regexp.MustCompile(`^(\s*)\d+\.\s+(.+)$`)

	if !markerPattern.MatchString(line) {
		return nil
	}

	list := &Element{Type: ElementOrderedList}

	for p.pos < len(p.lines) {
		currentLine := p.lines[p.pos]
		matches := markerPattern.FindStringSubmatch(currentLine)

		if matches == nil {
			if strings.TrimSpace(currentLine) != "" && !regexp.MustCompile(`^(\s*)([-*+]|\d+\.)\s`).MatchString(currentLine) {
				break
			}
			if strings.TrimSpace(currentLine) == "" {
				p.pos++
				continue
			}
			break
		}

		content := matches[2]
		list.Children = append(list.Children, &Element{
			Type:     ElementListItem,
			Content:  content,
			Children: p.parseInline(content),
		})
		p.pos++
	}

	return list
}

// parseParagraph parses a paragraph
func (p *Parser) parseParagraph() *Element {
	var lines []string

	for p.pos < len(p.lines) {
		line := p.lines[p.pos]

		// Stop at block-level elements
		if strings.TrimSpace(line) == "" ||
			strings.HasPrefix(line, "#") ||
			strings.HasPrefix(line, "```") ||
			strings.HasPrefix(line, "~~~") ||
			strings.HasPrefix(line, ">") ||
			regexp.MustCompile(`^[-*_]{3,}$`).MatchString(strings.TrimSpace(line)) ||
			regexp.MustCompile(`^(\s*)([-*+]|\d+\.)\s`).MatchString(line) {
			break
		}

		lines = append(lines, line)
		p.pos++
	}

	content := strings.Join(lines, " ")
	return &Element{
		Type:     ElementParagraph,
		Content:  content,
		Children: p.parseInline(content),
	}
}

// parseInline parses inline elements within a block
func (p *Parser) parseInline(text string) []*Element {
	// Use a simple state machine to parse inline elements
	var elements []*Element
	var buffer bytes.Buffer
	i := 0

	for i < len(text) {
		// Try to match inline patterns
		if element, consumed := p.tryInlineElement(text, i); element != nil {
			// Flush buffer as text element
			if buffer.Len() > 0 {
				elements = append(elements, &Element{
					Type:    ElementText,
					Content: buffer.String(),
				})
				buffer.Reset()
			}
			elements = append(elements, element)
			i += consumed
		} else {
			buffer.WriteByte(text[i])
			i++
		}
	}

	// Flush remaining buffer
	if buffer.Len() > 0 {
		elements = append(elements, &Element{
			Type:    ElementText,
			Content: buffer.String(),
		})
	}

	return elements
}

// tryInlineElement attempts to parse an inline element at the given position
func (p *Parser) tryInlineElement(text string, pos int) (*Element, int) {
	if pos >= len(text) {
		return nil, 0
	}

	// Bold and Italic (*** or ___)
	if pos+2 < len(text) && (text[pos:pos+3] == "***" || text[pos:pos+3] == "___") {
		marker := text[pos : pos+3]
		if end := strings.Index(text[pos+3:], marker); end != -1 {
			content := text[pos+3 : pos+3+end]
			return &Element{
				Type:     ElementBoldItalic,
				Content:  content,
				Children: p.parseInline(content),
			}, 3 + end + 3
		}
	}

	// Bold (** or __)
	if pos+1 < len(text) && ((text[pos:pos+2] == "**" && (pos+2 >= len(text) || text[pos+2] != '*')) ||
		(text[pos:pos+2] == "__" && (pos+2 >= len(text) || text[pos+2] != '_'))) {
		marker := text[pos : pos+2]
		searchText := text[pos+2:]
		end := findMatchingMarker(searchText, marker)
		if end != -1 {
			content := searchText[:end]
			return &Element{
				Type:     ElementBold,
				Content:  content,
				Children: p.parseInline(content),
			}, 2 + end + 2
		}
	}

	// Italic (* or _)
	if text[pos] == '*' || text[pos] == '_' {
		marker := string(text[pos])
		// Make sure it's not part of bold
		if pos+1 < len(text) && text[pos+1] == text[pos] {
			return nil, 0
		}
		searchText := text[pos+1:]
		end := findMatchingMarker(searchText, marker)
		if end != -1 && end > 0 {
			content := searchText[:end]
			return &Element{
				Type:     ElementItalic,
				Content:  content,
				Children: p.parseInline(content),
			}, 1 + end + 1
		}
	}

	// Inline code (`)
	if text[pos] == '`' {
		if end := strings.Index(text[pos+1:], "`"); end != -1 {
			content := text[pos+1 : pos+1+end]
			return &Element{
				Type:    ElementCode,
				Content: content,
			}, 1 + end + 1
		}
	}

	// Link [text](url)
	if text[pos] == '[' {
		if endText := strings.Index(text[pos:], "]"); endText != -1 {
			if pos+endText+1 < len(text) && text[pos+endText+1] == '(' {
				endURL := strings.Index(text[pos+endText+2:], ")")
				if endURL != -1 {
					linkText := text[pos+1 : pos+endText]
					url := text[pos+endText+2 : pos+endText+2+endURL]
					return &Element{
						Type:    ElementLink,
						Content: linkText,
						URL:     url,
					}, 1 + endText + 2 + endURL + 1
				}
			}
		}
	}

	// Image ![alt](url)
	if pos+1 < len(text) && text[pos:pos+2] == "![" {
		if endAlt := strings.Index(text[pos+2:], "]"); endAlt != -1 {
			if pos+2+endAlt+1 < len(text) && text[pos+2+endAlt+1] == '(' {
				endURL := strings.Index(text[pos+2+endAlt+2:], ")")
				if endURL != -1 {
					alt := text[pos+2 : pos+2+endAlt]
					url := text[pos+2+endAlt+2 : pos+2+endAlt+2+endURL]
					return &Element{
						Type:    ElementImage,
						Alt:     alt,
						URL:     url,
					}, 2 + endAlt + 2 + endURL + 1
				}
			}
		}
	}

	return nil, 0
}

// findMatchingMarker finds the matching closing marker, considering nesting
func findMatchingMarker(text, marker string) int {
	for i := 0; i < len(text); i++ {
		if strings.HasPrefix(text[i:], marker) {
			// Check if it's escaped
			if i > 0 && text[i-1] == '\\' {
				continue
			}
			return i
		}
	}
	return -1
}

// Renderer converts parsed elements to HTML
type Renderer struct {
	options RenderOptions
}

// RenderOptions configures the HTML output
type RenderOptions struct {
	SkipParagraphTags bool // Skip wrapping paragraphs in <p> tags
}

// NewRenderer creates a new HTML renderer
func NewRenderer(options ...RenderOptions) *Renderer {
	r := &Renderer{}
	if len(options) > 0 {
		r.options = options[0]
	}
	return r
}

// Render converts parsed elements to HTML
func (r *Renderer) Render(elements []*Element) string {
	var buffer bytes.Buffer
	for _, element := range elements {
		buffer.WriteString(r.renderElement(element))
	}
	return buffer.String()
}

// renderElement renders a single element to HTML
func (r *Renderer) renderElement(element *Element) string {
	switch element.Type {
	case ElementHeading:
		return fmt.Sprintf("<h%d>%s</h%d>\n", element.Level, r.renderChildren(element.Children), element.Level)

	case ElementParagraph:
		if r.options.SkipParagraphTags {
			return r.renderChildren(element.Children) + "\n"
		}
		return fmt.Sprintf("<p>%s</p>\n", r.renderChildren(element.Children))

	case ElementBold:
		return fmt.Sprintf("<strong>%s</strong>", r.renderChildren(element.Children))

	case ElementItalic:
		return fmt.Sprintf("<em>%s</em>", r.renderChildren(element.Children))

	case ElementBoldItalic:
		return fmt.Sprintf("<strong><em>%s</em></strong>", r.renderChildren(element.Children))

	case ElementLink:
		return fmt.Sprintf(`<a href="%s">%s</a>`, escapeHTML(element.URL), escapeHTML(element.Content))

	case ElementImage:
		return fmt.Sprintf(`<img src="%s" alt="%s">`, escapeHTML(element.URL), escapeHTML(element.Alt))

	case ElementCode:
		return fmt.Sprintf("<code>%s</code>", escapeHTML(element.Content))

	case ElementCodeBlock:
		if element.Language != "" {
			return fmt.Sprintf(`<pre><code class="language-%s">%s</code></pre>\n`, escapeHTML(element.Language), escapeHTML(element.Content))
		}
		return fmt.Sprintf("<pre><code>%s</code></pre>\n", escapeHTML(element.Content))

	case ElementBlockquote:
		return fmt.Sprintf("<blockquote>\n%s\n</blockquote>\n", r.renderChildren(element.Children))

	case ElementUnorderedList:
		return fmt.Sprintf("<ul>\n%s</ul>\n", r.renderListItems(element.Children))

	case ElementOrderedList:
		return fmt.Sprintf("<ol>\n%s</ol>\n", r.renderListItems(element.Children))

	case ElementListItem:
		return fmt.Sprintf("<li>%s</li>\n", r.renderChildren(element.Children))

	case ElementHorizontalRule:
		return "<hr>\n"

	case ElementText:
		return escapeHTML(element.Content)

	default:
		return ""
	}
}

// renderChildren renders child elements
func (r *Renderer) renderChildren(children []*Element) string {
	var buffer bytes.Buffer
	for _, child := range children {
		buffer.WriteString(r.renderElement(child))
	}
	return buffer.String()
}

// renderListItems renders list item elements
func (r *Renderer) renderListItems(items []*Element) string {
	var buffer bytes.Buffer
	for _, item := range items {
		buffer.WriteString(r.renderElement(item))
	}
	return buffer.String()
}

// escapeHTML escapes special HTML characters
func escapeHTML(s string) string {
	replacer := strings.NewReplacer(
		"&", "&amp;",
		"<", "&lt;",
		">", "&gt;",
		`"`, "&quot;",
		"'", "&#39;",
	)
	return replacer.Replace(s)
}

// Parse parses Markdown input and returns elements
func Parse(input string) []*Element {
	parser := NewParser(input)
	return parser.Parse()
}

// ParseToHTML parses Markdown and returns HTML
func ParseToHTML(input string) string {
	parser := NewParser(input)
	renderer := NewRenderer()
	return renderer.Render(parser.Parse())
}

// ParseToHTMLWithOptions parses Markdown and returns HTML with options
func ParseToHTMLWithOptions(input string, options RenderOptions) string {
	parser := NewParser(input)
	renderer := NewRenderer(options)
	return renderer.Render(parser.Parse())
}

// Markdown holds parsed Markdown content
type Markdown struct {
	Elements []*Element
	HTML     string
}

// ParseComplete parses Markdown and returns both elements and HTML
func ParseComplete(input string) *Markdown {
	elements := Parse(input)
	renderer := NewRenderer()
	return &Markdown{
		Elements: elements,
		HTML:     renderer.Render(elements),
	}
}

// GetHeadings extracts all headings from parsed elements
func GetHeadings(elements []*Element) []*Element {
	var headings []*Element
	for _, element := range elements {
		if element.Type == ElementHeading {
			headings = append(headings, element)
		}
	}
	return headings
}

// GetLinks extracts all links from parsed elements
func GetLinks(elements []*Element) []*Element {
	return extractElements(elements, ElementLink)
}

// GetImages extracts all images from parsed elements
func GetImages(elements []*Element) []*Element {
	return extractElements(elements, ElementImage)
}

// GetCodeBlocks extracts all code blocks from parsed elements
func GetCodeBlocks(elements []*Element) []*Element {
	return extractElements(elements, ElementCodeBlock)
}

// extractElements recursively extracts elements of a specific type
func extractElements(elements []*Element, targetType ElementType) []*Element {
	var result []*Element
	for _, element := range elements {
		if element.Type == targetType {
			result = append(result, element)
		}
		if len(element.Children) > 0 {
			result = append(result, extractElements(element.Children, targetType)...)
		}
	}
	return result
}

// CreateTableOfContents generates a table of contents from headings
func CreateTableOfContents(headings []*Element) string {
	var buffer bytes.Buffer
	buffer.WriteString("<nav class=\"toc\">\n<ul>\n")

	for _, heading := range headings {
		anchor := slugify(heading.Content)
		indent := strings.Repeat("  ", heading.Level)
		buffer.WriteString(fmt.Sprintf("%s<li><a href=\"#%s\">%s</a></li>\n", indent, anchor, heading.Content))
	}

	buffer.WriteString("</ul>\n</nav>")
	return buffer.String()
}

// slugify converts a string to a URL-friendly slug
func slugify(s string) string {
	// Convert to lowercase
	s = strings.ToLower(s)
	
	// Replace spaces with hyphens
	s = strings.ReplaceAll(s, " ", "-")
	
	// Remove non-alphanumeric characters except hyphens
	var buffer bytes.Buffer
	for _, r := range s {
		if (r >= 'a' && r <= 'z') || (r >= '0' && r <= '9') || r == '-' {
			buffer.WriteRune(r)
		}
	}
	
	return buffer.String()
}

// StripMarkdown removes Markdown formatting and returns plain text
func StripMarkdown(input string) string {
	elements := Parse(input)
	return stripElements(elements)
}

// stripElements recursively strips formatting from elements
func stripElements(elements []*Element) string {
	var buffer bytes.Buffer
	for _, element := range elements {
		switch element.Type {
		case ElementText:
			buffer.WriteString(element.Content)
		case ElementCode:
			buffer.WriteString(element.Content)
		default:
			if len(element.Children) > 0 {
				buffer.WriteString(stripElements(element.Children))
			} else if element.Content != "" {
				buffer.WriteString(element.Content)
			}
		}
	}
	return buffer.String()
}

// WordCount counts the number of words in Markdown content
func WordCount(input string) int {
	text := StripMarkdown(input)
	words := strings.Fields(text)
	return len(words)
}

// ReadingTime estimates reading time in minutes (assuming 200 words per minute)
func ReadingTime(input string) int {
	wordCount := WordCount(input)
	minutes := wordCount / 200
	if wordCount%200 > 0 {
		minutes++
	}
	if minutes == 0 {
		return 1
	}
	return minutes
}