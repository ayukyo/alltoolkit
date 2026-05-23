// Package typography_utils provides smart text typography and formatting utilities.
// Includes smart quotes conversion, dash normalization, ellipsis handling,
// text wrapping, whitespace normalization, character counting, and more.
//
// Zero external dependencies, pure Go implementation.
package typography_utils

import (
	"math"
	"regexp"
	"strconv"
	"strings"
	"unicode"
)

// DashStyle represents different dash styles
type DashStyle int

const (
	DashStyleAuto DashStyle = iota // Auto-detect context
	DashStyleEn                    // Use en dash (–) for ranges
	DashStyleEm                    // Use em dash (—) for breaks
	DashStyleHyphen                // Use hyphen (-)
)

// QuoteStyle represents different quote styles
type QuoteStyle struct {
	LeftDouble  string
	RightDouble string
	LeftSingle  string
	RightSingle string
}

// DefaultQuoteStyle returns the default quote style (curved quotes)
func DefaultQuoteStyle() QuoteStyle {
	return QuoteStyle{
		LeftDouble:  "\"",
		RightDouble: "\"",
		LeftSingle:  "'",
		RightSingle: "'",
	}
}

// ChineseQuoteStyle returns Chinese-style quotes
func ChineseQuoteStyle() QuoteStyle {
	return QuoteStyle{
		LeftDouble:  "\"",
		RightDouble: "\"",
		LeftSingle:  "'",
		RightSingle: "'",
	}
}

// StraightQuoteStyle returns straight quotes
func StraightQuoteStyle() QuoteStyle {
	return QuoteStyle{
		LeftDouble:  "\"",
		RightDouble: "\"",
		LeftSingle:  "'",
		RightSingle: "'",
	}
}

// ==================== Smart Quotes ====================

// SmartQuotes converts straight quotes to smart (curved) quotes.
// Handles both double and single quotes, including contractions.
func SmartQuotes(text string) string {
	return SmartQuotesWithStyle(text, DefaultQuoteStyle())
}

// SmartQuotesWithStyle converts straight quotes using custom quote style.
func SmartQuotesWithStyle(text string, style QuoteStyle) string {
	result := make([]rune, 0, len(text))
	doubleOpen := false
	singleOpen := false

	runes := []rune(text)
	for i, char := range runes {
		prevChar := getPrevChar(runes, i)
		nextChar := getNextChar(runes, i)

		if char == '"' {
			if doubleOpen {
				result = append(result, []rune(style.RightDouble)...)
				doubleOpen = false
			} else {
				result = append(result, []rune(style.LeftDouble)...)
				doubleOpen = true
			}
		} else if char == '\'' {
			// Handle contractions (it's, don't)
			if isAlpha(prevChar) && isAlpha(nextChar) {
				result = append(result, []rune(style.RightSingle)...)
			} else if singleOpen {
				result = append(result, []rune(style.RightSingle)...)
				singleOpen = false
			} else {
				result = append(result, []rune(style.LeftSingle)...)
				singleOpen = true
			}
		} else {
			result = append(result, char)
		}
	}

	return string(result)
}

// StraightenQuotes converts smart quotes back to straight quotes.
func StraightenQuotes(text string) string {
	// Process each replacement separately to avoid duplicate keys
	text = strings.ReplaceAll(text, "\u201C", "\"") // Left curved double quote
	text = strings.ReplaceAll(text, "\u201D", "\"") // Right curved double quote
	text = strings.ReplaceAll(text, "\u2018", "'")  // Left curved single quote
	text = strings.ReplaceAll(text, "\u2019", "'")  // Right curved single quote
	text = strings.ReplaceAll(text, "«", "\"")      // Left French quote
	text = strings.ReplaceAll(text, "»", "\"")      // Right French quote
	text = strings.ReplaceAll(text, "‹", "'")       // Left single angle quote
	text = strings.ReplaceAll(text, "›", "'")       // Right single angle quote
	text = strings.ReplaceAll(text, "„", "\"")      // German double quote
	text = strings.ReplaceAll(text, "‚", "'")       // German single quote
	text = strings.ReplaceAll(text, "「", "'")      // Chinese corner quote
	text = strings.ReplaceAll(text, "」", "'")      // Chinese corner quote
	text = strings.ReplaceAll(text, "『", "\"")     // Chinese double corner quote
	text = strings.ReplaceAll(text, "』", "\"")     // Chinese double corner quote

	return text
}

// ==================== Dash Normalization ====================

// NormalizeDashes normalizes dashes in text.
func NormalizeDashes(text string, style DashStyle) string {
	// Normalize all dash types first
	text = strings.ReplaceAll(text, "—", "--") // em dash
	text = strings.ReplaceAll(text, "–", "--") // en dash

	if style == DashStyleHyphen {
		return strings.ReplaceAll(text, "--", "-")
	}

	result := make([]rune, 0, len(text))
	runes := []rune(text)

	for i := 0; i < len(runes); i++ {
		if i < len(runes)-1 && runes[i] == '-' && runes[i+1] == '-' {
			// Check context for number ranges
			before := string(runes[:i])
			after := string(runes[i+2:])

			isRange := isNumberRange(before, after)

			if style == DashStyleEn || (style == DashStyleAuto && isRange) {
				result = append(result, '–') // en dash
			} else {
				result = append(result, '—') // em dash
			}
			i += 1 // Skip the second dash
		} else {
			result = append(result, runes[i])
		}
	}

	return string(result)
}

// EmDash converts double hyphens to em dash (—).
func EmDash(text string) string {
	return NormalizeDashes(text, DashStyleEm)
}

// EnDash converts double hyphens to en dash (–).
func EnDash(text string) string {
	return NormalizeDashes(text, DashStyleEn)
}

// ==================== Ellipsis Normalization ====================

// NormalizeEllipsis normalizes ellipsis in text.
// If useChar is true, uses ellipsis character (…), otherwise uses three dots (...).
func NormalizeEllipsis(text string, useChar bool) string {
	replacement := "…"
	if !useChar {
		replacement = "..."
	}

	// Match various ellipsis patterns
	patterns := []string{
		`\.{4,}`,    // Four or more dots
		`\.{3}`,     // Three dots
		`\. \. \.`,  // Dots with spaces
		`…+`,        // Multiple ellipsis chars
	}

	for _, pattern := range patterns {
		re := regexp.MustCompile(pattern)
		text = re.ReplaceAllString(text, replacement)
	}

	return text
}

// ==================== Smart Typography (All-in-one) ====================

// Smartify applies all smart typography transformations.
func Smartify(text string) string {
	result := text
	result = SmartQuotes(result)
	result = NormalizeDashes(result, DashStyleAuto)
	result = NormalizeEllipsis(result, true)
	result = NormalizeSpaces(result)
	return result
}

// ==================== Text Wrapping ====================

// WrapText wraps text at specified width.
func WrapText(text string, width int) string {
	if width <= 0 {
		return text
	}

	lines := strings.Split(text, "\n")
	result := make([]string, 0, len(lines))

	for _, line := range lines {
		if len(line) <= width {
			result = append(result, line)
			continue
		}

		wrapped := wrapLine(line, width)
		result = append(result, wrapped...)
	}

	return strings.Join(result, "\n")
}

// WrapParagraphs wraps paragraphs at specified width.
func WrapParagraphs(text string, width int) string {
	paragraphs := regexp.MustCompile(`\n\s*\n`).Split(text, -1)
	result := make([]string, 0, len(paragraphs))

	for _, para := range paragraphs {
		if strings.TrimSpace(para) == "" {
			result = append(result, "")
			continue
		}
		wrapped := WrapText(strings.TrimSpace(para), width)
		result = append(result, wrapped)
	}

	return strings.Join(result, "\n\n")
}

// wrapLine wraps a single line at specified width.
func wrapLine(line string, width int) []string {
	words := strings.Fields(line)
	if len(words) == 0 {
		return []string{""}
	}

	lines := make([]string, 0)
	currentLine := words[0]

	for i := 1; i < len(words); i++ {
		testLine := currentLine + " " + words[i]
		if len(testLine) <= width {
			currentLine = testLine
		} else {
			lines = append(lines, currentLine)
			currentLine = words[i]
		}
	}

	if currentLine != "" {
		lines = append(lines, currentLine)
	}

	return lines
}

// ==================== Whitespace Normalization ====================

// NormalizeSpaces normalizes whitespace in text.
// - Collapses multiple spaces to single space
// - Removes leading/trailing whitespace from lines
// - Reduces multiple blank lines to max 2
func NormalizeSpaces(text string) string {
	// Collapse multiple spaces
	spacePattern := regexp.MustCompile(`[ \t]+`)
	text = spacePattern.ReplaceAllString(text, " ")

	// Remove leading/trailing whitespace from lines
	lines := strings.Split(text, "\n")
	for i, line := range lines {
		lines[i] = strings.TrimSpace(line)
	}
	text = strings.Join(lines, "\n")

	// Reduce multiple blank lines
	blankPattern := regexp.MustCompile(`\n{3,}`)
	text = blankPattern.ReplaceAllString(text, "\n\n")

	return strings.TrimSpace(text)
}

// RemoveExtraBlankLines removes excess blank lines.
func RemoveExtraBlankLines(text string, maxBlank int) string {
	maxNewlines := maxBlank + 2
	pattern := regexp.MustCompile(`\n{` + strconv.Itoa(maxNewlines) + `,}`)
	replacement := strings.Repeat("\n", maxBlank+1)
	return pattern.ReplaceAllString(text, replacement)
}

// ==================== Character Statistics ====================

// TextStatistics holds text statistics.
type TextStatistics struct {
	Chars           int
	CharsNoSpaces   int
	Words           int
	Sentences       int
	Paragraphs      int
	Lines           int
	ChineseChars    int
	EnglishWords    int
	Digits          int
	Punctuation     int
}

// GetTextStatistics returns comprehensive text statistics.
func GetTextStatistics(text string) TextStatistics {
	return TextStatistics{
		Chars:           len(text),
		CharsNoSpaces:   countCharsNoSpaces(text),
		Words:           countWords(text),
		Sentences:       countSentences(text),
		Paragraphs:      countParagraphs(text),
		Lines:           len(strings.Split(text, "\n")),
		ChineseChars:    countChineseChars(text),
		EnglishWords:    countEnglishWords(text),
		Digits:          countDigits(text),
		Punctuation:     countPunctuation(text),
	}
}

// CountChars counts characters, optionally including spaces.
func CountChars(text string, includeSpaces bool) int {
	if includeSpaces {
		return len(text)
	}
	return countCharsNoSpaces(text)
}

// CountWords counts words (handles both English and Chinese).
func CountWords(text string) int {
	return countWords(text)
}

// CountSentences counts sentences.
func CountSentences(text string) int {
	return countSentences(text)
}

// CountParagraphs counts paragraphs.
func CountParagraphs(text string) int {
	return countParagraphs(text)
}

// ==================== HTML Escaping ====================

// EscapeHTML escapes HTML special characters.
func EscapeHTML(text string) string {
	replacements := []struct {
		from string
		to   string
	}{
		{"&", "&amp;"},
		{"<", "&lt;"},
		{">", "&gt;"},
		{"\"", "&quot;"},
		{"'", "&#39;"},
	}

	for _, r := range replacements {
		text = strings.ReplaceAll(text, r.from, r.to)
	}

	return text
}

// UnescapeHTML unescapes HTML entities.
func UnescapeHTML(text string) string {
	replacements := []struct {
		from string
		to   string
	}{
		{"&amp;", "&"},
		{"&lt;", "<"},
		{"&gt;", ">"},
		{"&quot;", "\""},
		{"&#39;", "'"},
		{"&nbsp;", " "},
		{"&copy;", "©"},
		{"&reg;", "®"},
		{"&trade;", "™"},
	}

	for _, r := range replacements {
		text = strings.ReplaceAll(text, r.from, r.to)
	}

	return text
}

// ==================== Markdown Escaping ====================

// EscapeMarkdown escapes Markdown special characters.
func EscapeMarkdown(text string) string {
	specialChars := []string{"\\", "`", "*", "_", "{", "}", "[", "]", "(", ")", "#", "+", "-", ".", "!", "|"}

	for _, char := range specialChars {
		text = strings.ReplaceAll(text, char, "\\"+char)
	}

	return text
}

// ==================== Title Handling ====================

// TitleCase converts text to title case format.
// Handles exceptions (small words that shouldn't be capitalized).
func TitleCase(text string) string {
	exceptions := []string{"a", "an", "the", "and", "but", "or", "for", "nor",
		"on", "at", "to", "by", "in", "of", "with", "from"}

	words := strings.Fields(strings.ToLower(text))
	result := make([]string, 0, len(words))

	for i, word := range words {
		if i == 0 || !containsWord(exceptions, word) {
			result = append(result, capitalize(word))
		} else {
			result = append(result, word)
		}
	}

	return strings.Join(result, " ")
}

// Slugify converts text to URL-friendly slug.
func Slugify(text string, separator string, lowercase bool) string {
	// Remove special characters, keep letters, digits, and Chinese
	// Instead of using regex with Unicode escapes, manually filter characters
	result := make([]rune, 0, len(text))
	for _, r := range text {
		if isAlphaNum(r) || r == '-' || r == ' ' || r == '\t' ||
			(r >= 0x4e00 && r <= 0x9fff) {
			result = append(result, r)
		}
	}
	text = string(result)

	// Replace whitespace with separator
	spacePattern := regexp.MustCompile(`\s+`)
	text = spacePattern.ReplaceAllString(text, separator)

	// Remove multiple separators
	sepPattern := regexp.MustCompile(regexp.QuoteMeta(separator) + `+`)
	text = sepPattern.ReplaceAllString(text, separator)

	// Remove leading/trailing separators
	text = strings.Trim(text, separator)

	if lowercase {
		text = strings.ToLower(text)
	}

	return text
}

// isAlphaNum checks if a rune is alphanumeric
func isAlphaNum(r rune) bool {
	return (r >= 'a' && r <= 'z') || (r >= 'A' && r <= 'Z') || (r >= '0' && r <= '9')
}

// ==================== Alignment ====================

// AlignLeft aligns text to the left with padding.
func AlignLeft(text string, width int, fillChar string) string {
	lines := strings.Split(text, "\n")
	result := make([]string, 0, len(lines))

	for _, line := range lines {
		padded := line
		if len(line) < width {
			padded = line + strings.Repeat(fillChar, width-len(line))
		}
		result = append(result, padded)
	}

	return strings.Join(result, "\n")
}

// AlignRight aligns text to the right with padding.
func AlignRight(text string, width int, fillChar string) string {
	lines := strings.Split(text, "\n")
	result := make([]string, 0, len(lines))

	for _, line := range lines {
		padded := line
		if len(line) < width {
			padded = strings.Repeat(fillChar, width-len(line)) + line
		}
		result = append(result, padded)
	}

	return strings.Join(result, "\n")
}

// AlignCenter centers text with padding.
func AlignCenter(text string, width int, fillChar string) string {
	lines := strings.Split(text, "\n")
	result := make([]string, 0, len(lines))

	for _, line := range lines {
		padded := line
		if len(line) < width {
			leftPad := int(math.Floor(float64(width - len(line)) / 2))
			rightPad := width - len(line) - leftPad
			padded = strings.Repeat(fillChar, leftPad) + line + strings.Repeat(fillChar, rightPad)
		}
		result = append(result, padded)
	}

	return strings.Join(result, "\n")
}

// AlignJustify justifies text to both sides.
func AlignJustify(text string, width int) string {
	lines := strings.Split(text, "\n")
	result := make([]string, 0, len(lines))

	for _, line := range lines {
		words := strings.Fields(line)
		if len(words) <= 1 {
			result = append(result, line)
			continue
		}

		// Calculate total character length
		totalLen := 0
		for _, w := range words {
			totalLen += len(w)
		}

		// Calculate spaces needed
		totalSpaces := width - totalLen
		gaps := len(words) - 1

		if gaps > 0 && totalSpaces > 0 {
			spacePerGap := totalSpaces / gaps
			extraSpaces := totalSpaces % gaps

			justified := make([]string, 0, len(words))
			for i, word := range words[:len(words)-1] {
				spaces := spacePerGap
				if i < extraSpaces {
					spaces++
				}
				justified = append(justified, word+strings.Repeat(" ", spaces))
			}
			justified = append(justified, words[len(words)-1])
			result = append(result, strings.Join(justified, ""))
		} else {
			result = append(result, line)
		}
	}

	return strings.Join(result, "\n")
}

// ==================== Line Numbers ====================

// AddLineNumbers adds line numbers to text.
func AddLineNumbers(text string, start int, width int) string {
	lines := strings.Split(text, "\n")
	result := make([]string, 0, len(lines))

	for i, line := range lines {
		lineNum := start + i
		lineNumStr := strconv.Itoa(lineNum)
		paddedNum := padLeft(lineNumStr, width, " ")
		result = append(result, paddedNum+" "+line)
	}

	return strings.Join(result, "\n")
}

// ==================== Chinese Typography ====================

// NormalizeChinesePunctuation converts English punctuation to Chinese.
func NormalizeChinesePunctuation(text string) string {
	replacements := map[string]string{
		",": "，",
		".": "。",
		"!": "！",
		"?": "？",
		":": "：",
		";": "；",
		"(": "（",
		")": "）",
		"[": "【",
		"]": "】",
	}

	for en, ch := range replacements {
		text = strings.ReplaceAll(text, en, ch)
	}

	return text
}

// ChineseParagraphIndent adds first-line indent to Chinese paragraphs.
func ChineseParagraphIndent(text string, indent string) string {
	paragraphs := regexp.MustCompile(`\n\s*\n`).Split(text, -1)
	result := make([]string, 0, len(paragraphs))

	for _, para := range paragraphs {
		trimmed := strings.TrimSpace(para)
		if trimmed != "" {
			result = append(result, indent+trimmed)
		} else {
			result = append(result, "")
		}
	}

	return strings.Join(result, "\n\n")
}

// ==================== Helper Functions ====================

func getPrevChar(runes []rune, i int) rune {
	if i > 0 {
		return runes[i-1]
	}
	return 0
}

func getNextChar(runes []rune, i int) rune {
	if i < len(runes)-1 {
		return runes[i+1]
	}
	return 0
}

func isAlpha(r rune) bool {
	return (r >= 'a' && r <= 'z') || (r >= 'A' && r <= 'Z')
}

func isNumberRange(before, after string) bool {
	beforePattern := regexp.MustCompile(`(\d+)\s*$`)
	afterPattern := regexp.MustCompile(`^\s*(\d+)`)

	return beforePattern.MatchString(before) && afterPattern.MatchString(after)
}

func capitalize(s string) string {
	if s == "" {
		return s
	}
	runes := []rune(s)
	runes[0] = unicode.ToUpper(runes[0])
	return string(runes)
}

func containsWord(words []string, word string) bool {
	for _, w := range words {
		if w == word {
			return true
		}
	}
	return false
}

func padLeft(s string, width int, fill string) string {
	if len(s) >= width {
		return s
	}
	return strings.Repeat(fill, width-len(s)) + s
}

func countCharsNoSpaces(text string) int {
	result := 0
	for _, r := range text {
		if r != ' ' && r != '\t' && r != '\n' {
			result++
		}
	}
	return result
}

func countWords(text string) int {
	// English words
	englishPattern := regexp.MustCompile(`[a-zA-Z]+`)
	englishCount := len(englishPattern.FindAllString(text, -1))

	// Chinese characters - use Unicode property or direct character range
	chineseCount := 0
	for _, r := range text {
		if r >= 0x4e00 && r <= 0x9fff {
			chineseCount++
		}
	}

	return englishCount + chineseCount
}

func countSentences(text string) int {
	pattern := regexp.MustCompile(`[.!?。！？]+`)
	sentences := pattern.Split(text, -1)
	count := 0
	for _, s := range sentences {
		if strings.TrimSpace(s) != "" {
			count++
		}
	}
	return count
}

func countParagraphs(text string) int {
	pattern := regexp.MustCompile(`\n\s*\n`)
	paragraphs := pattern.Split(text, -1)
	count := 0
	for _, p := range paragraphs {
		if strings.TrimSpace(p) != "" {
			count++
		}
	}
	return count
}

func countChineseChars(text string) int {
	count := 0
	for _, r := range text {
		if r >= 0x4e00 && r <= 0x9fff {
			count++
		}
	}
	return count
}

func countEnglishWords(text string) int {
	pattern := regexp.MustCompile(`[a-zA-Z]+`)
	return len(pattern.FindAllString(text, -1))
}

func countDigits(text string) int {
	pattern := regexp.MustCompile(`\d`)
	return len(pattern.FindAllString(text, -1))
}

func countPunctuation(text string) int {
	pattern := regexp.MustCompile(`[^\w\s]`)
	return len(pattern.FindAllString(text, -1))
}